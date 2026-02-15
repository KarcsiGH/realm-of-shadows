"""
Realm of Shadows — Combat Engine
Core turn-based combat system.

Handles: turn order, damage calculations, accuracy rolls, crits,
position modifiers, resource costs, regeneration, death/defeat.

References: Combat_System_Design_v3.md, Weapon_System_Design_v2.md
"""
import random
import math
from core.combat_config import *
from data.weapons import get_weapon, is_proficient, STARTING_WEAPONS, WEAPONS
from data.weapons import NON_PROFICIENT_DAMAGE_MULT, NON_PROFICIENT_ACCURACY, NON_PROFICIENT_SPEED


# ═══════════════════════════════════════════════════════════════
#  COMBATANT WRAPPER
# ═══════════════════════════════════════════════════════════════

def make_player_combatant(character, row=FRONT):
    """Wrap a Character object into a combatant dict for combat."""
    weapon_key = STARTING_WEAPONS.get(character.class_name, "Unarmed")
    weapon = get_weapon(weapon_key)

    # Monk unarmed scaling
    if weapon.get("special", {}).get("monk_scaling"):
        weapon["damage"] = 3 + (character.level * 2)

    return {
        "type": "player",
        "uid": id(character),
        "name": character.name,
        "class_name": character.class_name,
        "level": character.level,
        "stats": dict(character.stats),
        "hp": character.resources["HP"],
        "max_hp": character.resources["HP"],
        "resources": dict(character.resources),  # current values
        "max_resources": dict(character.resources),  # max values
        "abilities": [dict(a) for a in character.abilities],
        "weapon": weapon,
        "row": row,
        "defense": int(character.stats["CON"] * DEF_CON_MULT),
        "magic_resist": int(character.stats["WIS"] * MRES_WIS_MULT),
        "status_effects": [],
        "is_defending": False,
        "alive": True,
        "character_ref": character,  # back-reference
    }


# ═══════════════════════════════════════════════════════════════
#  SPEED & TURN ORDER
# ═══════════════════════════════════════════════════════════════

def calc_combatant_speed(combatant):
    """Calculate effective speed for turn ordering."""
    if combatant["type"] == "player":
        base = calc_speed(combatant["stats"], combatant.get("level", 1))
        base += combatant["weapon"].get("speed_mod", 0)
        # Non-proficient penalty
        if not is_proficient(combatant["class_name"], combatant["weapon"]["type"]):
            base += NON_PROFICIENT_SPEED
    else:
        # Enemy
        base = combatant["speed_base"]

    # Apply status modifiers
    multiplier = 1.0
    for status in combatant.get("status_effects", []):
        if status["name"] in SPEED_MODIFIERS:
            multiplier *= SPEED_MODIFIERS[status["name"]]

    return max(0, int(base * multiplier))


def build_turn_order(all_combatants):
    """Sort combatants by speed (highest first). Ties broken by DEX, then random."""
    living = [c for c in all_combatants if c["alive"] and c["hp"] > 0]
    order = []
    for c in living:
        speed = calc_combatant_speed(c)
        dex = c["stats"].get("DEX", 0)
        tiebreak = random.random()
        order.append((c, speed, dex, tiebreak))

    order.sort(key=lambda x: (-x[1], -x[2], -x[3]))
    return [entry[0] for entry in order]


# ═══════════════════════════════════════════════════════════════
#  ACCURACY
# ═══════════════════════════════════════════════════════════════

def calc_physical_accuracy(attacker, defender, weapon, position_acc_mod=0):
    """Calculate hit chance for a physical attack. Returns 0-100."""
    acc = ACCURACY_BASE_PHYSICAL

    # DEX difference
    atk_dex = attacker["stats"].get("DEX", 0)
    def_dex = defender["stats"].get("DEX", 0)
    acc += (atk_dex - def_dex) * ACCURACY_DEX_SCALE

    # Weapon accuracy mod
    acc += weapon.get("accuracy_mod", 0)

    # Enhancement bonus (future)
    acc += weapon.get("enhance_bonus", 0)

    # Position modifier
    acc += position_acc_mod

    # Non-proficient penalty
    if attacker["type"] == "player":
        if not is_proficient(attacker["class_name"], weapon["type"]):
            acc += NON_PROFICIENT_ACCURACY

    # Defender is defending
    if defender.get("is_defending"):
        acc += DEFEND_ACC_PENALTY

    # Status penalties on attacker
    for status in attacker.get("status_effects", []):
        if status["name"] in ACCURACY_STATUS_PENALTIES:
            acc += ACCURACY_STATUS_PENALTIES[status["name"]]

    return max(ACCURACY_MIN, min(ACCURACY_MAX, acc))


def calc_magic_accuracy(attacker, defender, spell=None):
    """Calculate hit chance for a spell. Returns 0-100."""
    acc = ACCURACY_BASE_MAGIC

    # Casting stat vs defender WIS
    casting_stat_val = get_casting_stat_value(attacker)
    def_wis = defender["stats"].get("WIS", 0)
    acc += (casting_stat_val - def_wis) * ACCURACY_STAT_SCALE

    # Spell-specific modifier
    if spell:
        acc += spell.get("accuracy_mod", 0)

    # Focus item bonus (future)
    acc += attacker.get("focus_bonus", 0)

    # Status penalties
    for status in attacker.get("status_effects", []):
        if status["name"] in ACCURACY_STATUS_PENALTIES:
            acc += ACCURACY_STATUS_PENALTIES[status["name"]]

    return max(ACCURACY_MIN, min(ACCURACY_MAX, acc))


def roll_hit(accuracy):
    """Roll to hit. Returns True if attack lands."""
    return random.randint(1, 100) <= accuracy


# ═══════════════════════════════════════════════════════════════
#  DAMAGE CALCULATIONS
# ═══════════════════════════════════════════════════════════════

def get_casting_stat_value(combatant):
    """Get the relevant casting stat for a spellcaster."""
    if combatant["type"] == "player":
        cn = combatant["class_name"]
        if cn in ("Mage",):
            return combatant["stats"].get("INT", 0)
        elif cn in ("Cleric",):
            return combatant["stats"].get("PIE", 0)
        elif cn in ("Ranger", "Monk"):
            return combatant["stats"].get("WIS", 0)
    # Enemies with spells use INT
    return combatant["stats"].get("INT", 0)


def calc_physical_damage(attacker, defender, weapon, position_dmg_mod=1.0,
                         ability_bonus=0, is_crit=False, crit_data=None):
    """
    Full physical damage formula from Combat Design v3:
    Stat Damage = sum(Weapon Stat × Weight for each damage stat)
    Raw Damage  = Stat Damage + Weapon Base + Enhancement + Ability Bonus
    Final       = (Raw × Position × Variance × PhysTypeMod) - Defense
    """
    # Stat damage from weapon scaling
    stat_damage = 0
    for stat_key, weight in weapon.get("damage_stat", {}).items():
        stat_damage += attacker["stats"].get(stat_key, 0) * weight

    # Raw damage
    weapon_base = weapon.get("damage", 0)
    enhance = weapon.get("enhance_bonus", 0)
    raw = stat_damage + weapon_base + enhance + ability_bonus

    # Non-proficient penalty
    if attacker["type"] == "player":
        if not is_proficient(attacker["class_name"], weapon["type"]):
            raw *= NON_PROFICIENT_DAMAGE_MULT

    # Position modifier
    raw *= position_dmg_mod

    # Variance
    variance = random.uniform(DAMAGE_VARIANCE_MIN, DAMAGE_VARIANCE_MAX)
    raw *= variance

    # Physical type resistance
    phys_type = weapon.get("phys_type", "slashing")
    type_mod = defender.get("resistances", {}).get(phys_type, NEUTRAL)
    raw *= type_mod

    # Defense calculation
    defense = defender.get("defense", 0)

    # Armor bypass for maces
    if weapon.get("special", {}).get("armor_bypass"):
        defense *= (1.0 - weapon["special"]["armor_bypass"])

    # Defending bonus
    if defender.get("is_defending"):
        defense *= DEFEND_PHYS_MULT

    # Crit: power crit ignores 50% defense
    if is_crit and crit_data and crit_data.get("ignore_defense"):
        defense *= (1.0 - crit_data["ignore_defense"])

    final = raw - defense

    # Crit multiplier
    if is_crit and crit_data:
        final *= crit_data.get("multiplier", 1.5)

    return max(MINIMUM_DAMAGE, int(final))


def calc_magic_damage(attacker, defender, spell, is_crit=False):
    """
    Magic damage formula from Combat Design v3:
    Stat Damage = Casting Stat × 1.5 + Focus Bonus
    Raw         = Stat Damage + Spell Power
    Final       = (Raw × Variance × ElemTypeMod) - Magic Resist
    """
    casting_val = get_casting_stat_value(attacker)
    focus_bonus = attacker.get("focus_bonus", 0)

    # Staff spell bonus
    if attacker["type"] == "player":
        weapon = attacker.get("weapon", {})
        focus_bonus += weapon.get("spell_bonus", 0)

    stat_damage = (casting_val * MAGIC_STAT_MULT) + focus_bonus
    spell_power = spell.get("power", 10)
    raw = stat_damage + spell_power

    # Variance
    variance = random.uniform(MAGIC_VARIANCE_MIN, MAGIC_VARIANCE_MAX)
    raw *= variance

    # Elemental resistance
    element = spell.get("element", "arcane")
    type_mod = defender.get("resistances", {}).get(element, NEUTRAL)
    raw *= type_mod

    # Magic resistance
    m_resist = defender.get("magic_resist", 0)
    if defender.get("is_defending"):
        m_resist *= DEFEND_MAGIC_MULT

    final = raw - m_resist

    # Crit
    if is_crit:
        final *= CRIT_SPELL_MULT

    return max(MINIMUM_DAMAGE, int(final))


def calc_healing(healer, spell):
    """Healing formula: (PIE × 2.0) + Spell Power + Focus + random(0, PIE/2)"""
    pie = healer["stats"].get("PIE", 0)
    spell_power = spell.get("power", 10)
    focus = healer.get("focus_bonus", 0)

    # Staff bonus
    if healer["type"] == "player":
        weapon = healer.get("weapon", {})
        focus += weapon.get("spell_bonus", 0)

    amount = (pie * HEAL_PIE_MULT) + spell_power + focus + random.randint(0, max(1, pie // 2))
    return int(amount)


# ═══════════════════════════════════════════════════════════════
#  CRITICAL HIT SYSTEM
# ═══════════════════════════════════════════════════════════════

def check_crit(attacker, attack_type="physical", weapon=None):
    """
    Check for critical hit. Returns (is_crit, crit_data) where crit_data
    has 'multiplier' and optionally 'ignore_defense'.
    """
    if attacker["type"] != "player":
        # Enemies don't crit (for now)
        return False, None

    cn = attacker["class_name"]
    chance = CRIT_BASE_CHANCE

    if attack_type == "physical":
        # Weapon crit bonus
        if weapon:
            wtype = weapon.get("type", "")
            chance += CRIT_WEAPON_BONUS.get(wtype, 0)
            chance += weapon.get("crit_mod", 0)

        if cn in ("Thief", "Ranger", "Assassin"):
            # Precision crit: DEX-based
            chance += attacker["stats"].get("DEX", 0) / CRIT_PRECISION_SCALE
            mult = CRIT_PRECISION_CLASSES.get(cn, CRIT_PRECISION_MULT)
            crit_data = {"multiplier": mult}
        elif cn in ("Fighter", "Knight"):
            # Power crit: STR-based, ignores defense
            chance += attacker["stats"].get("STR", 0) / CRIT_POWER_SCALE
            crit_data = {"multiplier": CRIT_POWER_MULT,
                         "ignore_defense": CRIT_POWER_DEF_IGNORE}
        elif cn in ("Monk", "Ki Master"):
            # Ki crit: WIS-based
            chance += attacker["stats"].get("WIS", 0) / CRIT_KI_SCALE
            crit_data = {"multiplier": CRIT_KI_MULT}
        else:
            crit_data = {"multiplier": 1.5}

    elif attack_type == "spell":
        casting = get_casting_stat_value(attacker)
        chance += casting / CRIT_SPELL_SCALE
        crit_data = {"multiplier": CRIT_SPELL_MULT}

    elif attack_type == "heal":
        chance += attacker["stats"].get("PIE", 0) / CRIT_HEAL_SCALE
        crit_data = {"multiplier": CRIT_HEAL_MULT}

    else:
        crit_data = {"multiplier": 1.5}

    is_crit = random.randint(1, 100) <= int(chance)
    return is_crit, crit_data if is_crit else None


# ═══════════════════════════════════════════════════════════════
#  ACTION RESOLUTION
# ═══════════════════════════════════════════════════════════════

def resolve_basic_attack(attacker, defender):
    """Resolve a basic physical attack. Returns a result dict."""
    weapon = attacker.get("weapon")
    if not weapon:
        weapon = get_weapon("Unarmed")

    # Position modifiers
    weapon_range = weapon.get("range", "melee")
    is_xbow = weapon.get("special", {}).get("is_crossbow", False)
    pos_dmg, pos_acc = get_position_mods(
        weapon_range, attacker["row"], defender["row"], is_xbow
    )

    # Accuracy check
    accuracy = calc_physical_accuracy(attacker, defender, weapon, pos_acc)
    hit = roll_hit(accuracy)

    result = {
        "action": "attack",
        "attacker": attacker,
        "defender": defender,
        "weapon": weapon,
        "accuracy": accuracy,
        "hit": hit,
        "damage": 0,
        "is_crit": False,
        "crit_data": None,
        "messages": [],
    }

    if not hit:
        result["messages"].append(f"{attacker['name']} attacks {defender['name']} — MISS!")
        return result

    # Crit check
    is_crit, crit_data = check_crit(attacker, "physical", weapon)
    result["is_crit"] = is_crit
    result["crit_data"] = crit_data

    # Calculate damage
    damage = calc_physical_damage(
        attacker, defender, weapon,
        position_dmg_mod=pos_dmg,
        is_crit=is_crit,
        crit_data=crit_data,
    )

    result["damage"] = damage

    # Apply damage
    defender["hp"] = max(0, defender["hp"] - damage)
    if defender["hp"] <= 0:
        defender["alive"] = False

    # Build message
    crit_str = " CRITICAL HIT!" if is_crit else ""
    msg = f"{attacker['name']} attacks {defender['name']} with {weapon['name']} for {damage} damage!{crit_str}"
    result["messages"].append(msg)

    if not defender["alive"]:
        result["messages"].append(f"{defender['name']} has fallen!")

    return result


def resolve_enemy_attack(attacker, defender):
    """Resolve an enemy's basic attack against a player."""
    weapon_range = attacker.get("attack_type", "melee")
    pos_dmg, pos_acc = get_position_mods(
        weapon_range, attacker["row"], defender["row"]
    )

    # Accuracy
    acc = ACCURACY_BASE_PHYSICAL
    acc += (attacker["stats"].get("DEX", 0) - defender["stats"].get("DEX", 0)) * ACCURACY_DEX_SCALE
    acc += attacker.get("accuracy_bonus", 0)
    acc += pos_acc

    if defender.get("is_defending"):
        acc += DEFEND_ACC_PENALTY

    for status in attacker.get("status_effects", []):
        if status["name"] in ACCURACY_STATUS_PENALTIES:
            acc += ACCURACY_STATUS_PENALTIES[status["name"]]

    acc = max(ACCURACY_MIN, min(ACCURACY_MAX, acc))
    hit = roll_hit(acc)

    result = {
        "action": "enemy_attack",
        "attacker": attacker,
        "defender": defender,
        "accuracy": acc,
        "hit": hit,
        "damage": 0,
        "is_crit": False,
        "messages": [],
    }

    if not hit:
        result["messages"].append(f"{attacker['name']} attacks {defender['name']} — MISS!")
        return result

    # Enemy damage: attack_damage + STR scaling + variance - defense
    base_dmg = attacker.get("attack_damage", 5)
    str_bonus = attacker["stats"].get("STR", 0) * 0.3
    raw = (base_dmg + str_bonus) * pos_dmg
    raw *= random.uniform(DAMAGE_VARIANCE_MIN, DAMAGE_VARIANCE_MAX)

    # Physical type vs resistance
    phys_type = attacker.get("phys_type", "slashing")
    type_mod = defender.get("resistances", {}).get(phys_type, NEUTRAL)
    raw *= type_mod

    # Defense
    defense = defender.get("defense", 0)
    if defender.get("is_defending"):
        defense *= DEFEND_PHYS_MULT

    damage = max(MINIMUM_DAMAGE, int(raw - defense))
    result["damage"] = damage

    defender["hp"] = max(0, defender["hp"] - damage)
    if defender["hp"] <= 0:
        defender["alive"] = False

    msg = f"{attacker['name']} attacks {defender['name']} for {damage} damage!"
    result["messages"].append(msg)

    if not defender["alive"]:
        result["messages"].append(f"{defender['name']} falls unconscious!")

    return result


def resolve_defend(combatant):
    """Set defending stance until next turn."""
    combatant["is_defending"] = True
    return {
        "action": "defend",
        "combatant": combatant,
        "messages": [f"{combatant['name']} takes a defensive stance."],
    }


def resolve_ability(attacker, target, ability):
    """Resolve a spell/ability use. Returns result dict."""
    result = {
        "action": "ability",
        "attacker": attacker,
        "target": target,
        "ability": ability,
        "damage": 0,
        "healing": 0,
        "hit": True,
        "is_crit": False,
        "messages": [],
    }

    # Check resource cost
    resource_key = ability.get("resource", "")
    cost = ability.get("cost", 0)
    if resource_key and attacker["type"] == "player":
        current = attacker["resources"].get(resource_key, 0)
        if current < cost:
            result["hit"] = False
            result["messages"].append(
                f"{attacker['name']} doesn't have enough {resource_key}! (need {cost}, have {current})"
            )
            return result
        attacker["resources"][resource_key] -= cost

    # Determine ability type based on name/resource
    ab_name = ability["name"].lower()
    is_heal = "heal" in ab_name
    is_offensive = not is_heal

    if is_heal:
        # Healing ability
        heal_spell = {"power": cost * 1.5}  # Scale heal power off cost
        is_crit, crit_data = check_crit(attacker, "heal")
        amount = calc_healing(attacker, heal_spell)
        if is_crit:
            amount = int(amount * CRIT_HEAL_MULT)
            result["is_crit"] = True

        old_hp = target["hp"]
        target["hp"] = min(target["max_hp"], target["hp"] + amount)
        actual = target["hp"] - old_hp
        result["healing"] = actual

        crit_str = " CRITICAL HEAL!" if is_crit else ""
        result["messages"].append(
            f"{attacker['name']} uses {ability['name']} on {target['name']} — heals {actual} HP!{crit_str}"
        )

    elif is_offensive:
        # Offensive ability — check if magic or physical
        is_magic = resource_key in ("INT-MP", "WIS-MP", "PIE-MP")

        if is_magic:
            # Magic accuracy
            acc = calc_magic_accuracy(attacker, target)
            hit = roll_hit(acc)
            result["accuracy"] = acc

            if not hit:
                result["hit"] = False
                result["messages"].append(
                    f"{attacker['name']} casts {ability['name']} at {target['name']} — RESISTED!"
                )
                return result

            is_crit, crit_data = check_crit(attacker, "spell")
            spell = {"power": cost * 1.2, "element": "arcane"}

            # Try to determine element from ability name
            for elem, keywords in [
                ("fire", ["fire", "flame", "burn", "inferno"]),
                ("ice", ["ice", "frost", "freeze", "blizzard"]),
                ("lightning", ["lightning", "shock", "thunder", "storm"]),
                ("divine", ["smite", "holy", "divine", "judgment"]),
                ("shadow", ["shadow", "dark", "void", "dread"]),
                ("nature", ["nature", "thorn", "entangle", "earthquake"]),
            ]:
                if any(kw in ab_name for kw in keywords):
                    spell["element"] = elem
                    break

            damage = calc_magic_damage(attacker, target, spell, is_crit)
            result["damage"] = damage
            result["is_crit"] = is_crit

            target["hp"] = max(0, target["hp"] - damage)
            if target["hp"] <= 0:
                target["alive"] = False

            crit_str = " CRITICAL!" if is_crit else ""
            result["messages"].append(
                f"{attacker['name']} casts {ability['name']} on {target['name']} for {damage} damage!{crit_str}"
            )
        else:
            # Physical ability (STR-SP, DEX-SP, Ki)
            weapon = attacker.get("weapon", get_weapon("Unarmed"))
            pos_dmg, pos_acc = get_position_mods(
                weapon.get("range", "melee"), attacker["row"], target["row"]
            )

            acc = calc_physical_accuracy(attacker, target, weapon, pos_acc)
            hit = roll_hit(acc)
            result["accuracy"] = acc

            if not hit:
                result["hit"] = False
                result["messages"].append(
                    f"{attacker['name']} uses {ability['name']} at {target['name']} — MISS!"
                )
                return result

            is_crit, crit_data = check_crit(attacker, "physical", weapon)
            ability_bonus = cost * 0.8  # Abilities scale with their cost

            damage = calc_physical_damage(
                attacker, target, weapon,
                position_dmg_mod=pos_dmg,
                ability_bonus=ability_bonus,
                is_crit=is_crit, crit_data=crit_data,
            )
            result["damage"] = damage
            result["is_crit"] = is_crit

            target["hp"] = max(0, target["hp"] - damage)
            if target["hp"] <= 0:
                target["alive"] = False

            crit_str = " CRITICAL!" if is_crit else ""
            result["messages"].append(
                f"{attacker['name']} uses {ability['name']} on {target['name']} for {damage} damage!{crit_str}"
            )

    if target.get("type") != "player" and not target["alive"]:
        result["messages"].append(f"{target['name']} has fallen!")
    elif target.get("type") == "player" and not target["alive"]:
        result["messages"].append(f"{target['name']} falls unconscious!")

    return result


# ═══════════════════════════════════════════════════════════════
#  ENEMY AI
# ═══════════════════════════════════════════════════════════════

def enemy_choose_action(enemy, players, enemies):
    """Simple AI: choose action and target for an enemy."""
    living_players = [p for p in players if p["alive"]]
    if not living_players:
        return None, None, None

    ai_type = enemy.get("ai_type", "random")

    # Check if enemy has usable abilities (healing, buffs)
    for ability in enemy.get("abilities", []):
        if ability.get("type") == "heal":
            # Heal most wounded ally
            living_allies = [e for e in enemies if e["alive"] and e["hp"] < e["max_hp"] * 0.6]
            if living_allies:
                target = min(living_allies, key=lambda e: e["hp"] / e["max_hp"])
                return "ability", target, ability

    # Basic attack — choose target
    if ai_type == "aggressive":
        # Target highest damage dealer (approximate: class-based)
        target = random.choice(living_players)
    elif ai_type == "defensive":
        # Target lowest HP player
        target = min(living_players, key=lambda p: p["hp"])
    elif ai_type == "tactical":
        # Target healers/mages first (back row)
        back_row = [p for p in living_players if p["row"] == BACK]
        if back_row:
            target = random.choice(back_row)
        else:
            target = random.choice(living_players)
    else:
        target = random.choice(living_players)

    # Melee enemies prefer front-row targets (weighted)
    if enemy.get("attack_type") == "melee":
        weighted = []
        for p in living_players:
            if p["row"] == FRONT:
                weighted.extend([p] * 5)
            elif p["row"] == MID:
                weighted.extend([p] * 3)
            else:
                weighted.extend([p] * 2)
        if weighted:
            target = random.choice(weighted)

    return "attack", target, None


# ═══════════════════════════════════════════════════════════════
#  RESOURCE REGENERATION
# ═══════════════════════════════════════════════════════════════

def end_of_round_regen(combatant):
    """Apply end-of-round resource regeneration. HP does NOT regen in combat."""
    if combatant["type"] != "player":
        return []

    messages = []
    cn = combatant.get("class_name", "")

    # Map resource pools to their governing stat
    regen_map = {
        "INT-MP": "INT",
        "WIS-MP": "WIS",
        "PIE-MP": "PIE",
        "STR-SP": "STR",
        "DEX-SP": "DEX",
    }

    # Ki regeneration
    if "Ki" in combatant["resources"]:
        wis = combatant["stats"].get("WIS", 0)
        max_ki = combatant["max_resources"].get("Ki", 0)
        pct = MONK_REGEN_PERCENT if cn in ("Monk", "Ki Master") else REGEN_PERCENT
        regen = int((wis / REGEN_STAT_DIV) + (max_ki * pct))
        if regen > 0:
            old = combatant["resources"]["Ki"]
            combatant["resources"]["Ki"] = min(max_ki, old + regen)
            gained = combatant["resources"]["Ki"] - old
            if gained > 0:
                messages.append(f"{combatant['name']} regenerates {gained} Ki")

    # Other resource pools
    for pool, stat_key in regen_map.items():
        if pool in combatant["resources"]:
            stat_val = combatant["stats"].get(stat_key, 0)
            max_val = combatant["max_resources"].get(pool, 0)
            regen = int((stat_val / REGEN_STAT_DIV) + (max_val * REGEN_PERCENT))
            if regen > 0:
                old = combatant["resources"][pool]
                combatant["resources"][pool] = min(max_val, old + regen)

    # Clear defending stance
    combatant["is_defending"] = False

    return messages


# ═══════════════════════════════════════════════════════════════
#  COMBAT STATE MANAGER
# ═══════════════════════════════════════════════════════════════

class CombatState:
    """
    Manages the full state of a combat encounter.
    Tracks turn order, round number, combat log, victory/defeat.
    """

    def __init__(self, party_chars, encounter_key):
        from data.enemies import build_encounter

        self.round_num = 1
        self.encounter_name = ""
        self.combat_log = []
        self.phase = "player_turn"  # player_turn, enemy_turn, victory, defeat
        self.current_turn_index = 0
        self.turn_order = []
        self.pending_action = None  # set by UI when player chooses

        # Build player combatants — assign rows based on class
        self.players = []
        row_assignments = self._assign_party_rows(party_chars)
        for i, char in enumerate(party_chars):
            row = row_assignments[i]
            combatant = make_player_combatant(char, row)
            self.players.append(combatant)

        # Build enemies
        self.enemies, self.encounter_name = build_encounter(encounter_key)

        # Initial turn order
        self.all_combatants = self.players + self.enemies
        self.turn_order = build_turn_order(self.all_combatants)

        self.log(f"═══ {self.encounter_name} ═══")
        self.log(f"Round {self.round_num}")

    def _assign_party_rows(self, party_chars):
        """Auto-assign party to rows based on class archetypes."""
        rows = []
        for char in party_chars:
            cn = char.class_name
            if cn in ("Fighter", "Monk"):
                rows.append(FRONT)
            elif cn in ("Ranger", "Thief"):
                rows.append(MID)
            else:  # Mage, Cleric
                rows.append(BACK)
        return rows

    def log(self, msg):
        """Add message to combat log."""
        self.combat_log.append(msg)

    def get_current_combatant(self):
        """Get whoever's turn it is."""
        if self.current_turn_index < len(self.turn_order):
            return self.turn_order[self.current_turn_index]
        return None

    def is_player_turn(self):
        """Check if the current combatant is a player character."""
        c = self.get_current_combatant()
        return c is not None and c["type"] == "player"

    def advance_turn(self):
        """Move to the next combatant's turn. Handle end-of-round."""
        self.current_turn_index += 1

        # Skip dead combatants
        while (self.current_turn_index < len(self.turn_order) and
               not self.turn_order[self.current_turn_index]["alive"]):
            self.current_turn_index += 1

        # Check victory/defeat
        if not any(p["alive"] for p in self.players):
            self.phase = "defeat"
            self.log("═══ DEFEAT — Your party has fallen! ═══")
            return

        if not any(e["alive"] for e in self.enemies):
            self.phase = "victory"
            self.log("═══ VICTORY! ═══")
            self._calc_rewards()
            return

        # End of round — start new round
        if self.current_turn_index >= len(self.turn_order):
            self._end_round()

    def _end_round(self):
        """Handle end-of-round: regen, status ticks, rebuild turn order."""
        self.round_num += 1

        # Regeneration for all living combatants
        for c in self.all_combatants:
            if c["alive"]:
                msgs = end_of_round_regen(c)
                for m in msgs:
                    self.log(m)
                # Clear defending
                c["is_defending"] = False

        # Rebuild turn order
        self.turn_order = build_turn_order(self.all_combatants)
        self.current_turn_index = 0

        self.log(f"── Round {self.round_num} ──")

    def execute_player_action(self, action_type, target=None, ability=None):
        """Execute a player's chosen action."""
        actor = self.get_current_combatant()
        if not actor or actor["type"] != "player":
            return

        if action_type == "attack":
            result = resolve_basic_attack(actor, target)
        elif action_type == "defend":
            result = resolve_defend(actor)
        elif action_type == "ability":
            result = resolve_ability(actor, target, ability)
        else:
            return

        for msg in result.get("messages", []):
            self.log(msg)

        self.advance_turn()

    def execute_enemy_turn(self):
        """Let the current enemy take its AI-controlled action."""
        actor = self.get_current_combatant()
        if not actor or actor["type"] != "enemy":
            return

        # Skip stunned/frozen
        for status in actor.get("status_effects", []):
            if status["name"] in ("Stunned", "Frozen", "Petrified"):
                self.log(f"{actor['name']} is {status['name']} and cannot act!")
                self.advance_turn()
                return

        action, target, ability = enemy_choose_action(actor, self.players, self.enemies)

        if action == "attack" and target:
            result = resolve_enemy_attack(actor, target)
            for msg in result.get("messages", []):
                self.log(msg)
        elif action == "ability" and target and ability:
            # Simple enemy ability resolution
            if ability.get("type") == "heal":
                power = ability.get("power", 10)
                amount = power + random.randint(0, 5)
                old_hp = target["hp"]
                target["hp"] = min(target["max_hp"], target["hp"] + amount)
                actual = target["hp"] - old_hp
                self.log(f"{actor['name']} uses {ability['name']} on {target['name']} — heals {actual} HP!")
        else:
            self.log(f"{actor['name']} hesitates...")

        self.advance_turn()

    def _calc_rewards(self):
        """Calculate XP and gold from defeated enemies."""
        from data.enemies import ENEMIES
        total_xp = 0
        total_gold = 0
        for e in self.enemies:
            template = ENEMIES.get(e["template_key"], {})
            total_xp += template.get("xp_reward", 0)
            gold_range = template.get("gold_reward", (0, 0))
            total_gold += random.randint(gold_range[0], gold_range[1])

        self.rewards = {"xp": total_xp, "gold": total_gold}
        self.log(f"Earned {total_xp} XP and {total_gold} gold!")

    def get_living_enemies(self):
        return [e for e in self.enemies if e["alive"]]

    def get_living_players(self):
        return [p for p in self.players if p["alive"]]

    def get_enemy_groups(self):
        """Get enemies grouped by type and row for targeting display."""
        groups = {}
        for e in self.enemies:
            if not e["alive"]:
                continue
            key = (e["group_key"], e["row"])
            if key not in groups:
                groups[key] = {"name": e["name"], "row": e["row"],
                               "members": [], "group_key": e["group_key"]}
            groups[key]["members"].append(e)
        return list(groups.values())
