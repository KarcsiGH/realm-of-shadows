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
from core.combat_config import (
    STATUS_TICK_DAMAGE, STATUS_INCAPACITATE, STATUS_DURATION_TICK,
    CLASS_THREAT, CLASS_THREAT_DEFAULT,
    ENEMY_BUFF_DURATION, ENEMY_BUFF_DMG_MULT,
)
from data.weapons import get_weapon, is_proficient, STARTING_WEAPONS, WEAPONS
from data.weapons import NON_PROFICIENT_DAMAGE_MULT, NON_PROFICIENT_ACCURACY, NON_PROFICIENT_SPEED


# ═══════════════════════════════════════════════════════════════
#  COMBATANT WRAPPER
# ═══════════════════════════════════════════════════════════════

def make_player_combatant(character, row=FRONT):
    """Wrap a Character object into a combatant dict for combat."""
    # Use equipped weapon if available, otherwise starting weapon
    equipped_weapon = None
    if hasattr(character, "equipment") and character.equipment:
        equipped_weapon = character.equipment.get("weapon")
    if equipped_weapon:
        weapon = dict(equipped_weapon)
    else:
        weapon_key = STARTING_WEAPONS.get(character.class_name, "Unarmed")
        weapon = get_weapon(weapon_key)

    # Monk unarmed scaling
    if weapon.get("special", {}).get("monk_scaling"):
        weapon["damage"] = 3 + (character.level * 2)

    # Use effective stats (base + equipment bonuses)
    if hasattr(character, "effective_stats"):
        stats = character.effective_stats()
    else:
        stats = dict(character.stats)

    # Equipment defense/resist/speed bonuses
    equip_def = 0
    equip_mres = 0
    equip_speed = 0
    if hasattr(character, "equipment_defense"):
        equip_def = character.equipment_defense()
        equip_mres = character.equipment_magic_resist()
        equip_speed = character.equipment_speed()
        # Enchant resistance bonuses from armor
        if hasattr(character, "equipment") and character.equipment:
            for slot, item in character.equipment.items():
                if item and item.get("enchant_resist_bonus"):
                    equip_mres += item["enchant_resist_bonus"]

    # Get actual max resources (not current values)
    from core.classes import get_all_resources
    actual_max = get_all_resources(character.class_name, stats, character.level)
    max_hp = actual_max.get("HP", character.resources["HP"])

    return {
        "type": "player",
        "uid": id(character),
        "name": character.name,
        "class_name": character.class_name,
        "race_name": getattr(character, "race_name", "Human"),
        "level": character.level,
        "stats": stats,
        "hp": character.resources["HP"],
        "max_hp": max_hp,
        "resources": dict(character.resources),  # current values
        "max_resources": actual_max,             # TRUE max values
        "abilities": [dict(a) for a in character.abilities],
        "weapon": weapon,
        "row": row,
        "defense": int(stats["CON"] * DEF_CON_MULT) + equip_def,
        "magic_resist": int(stats["WIS"] * MRES_WIS_MULT) + equip_mres,
        "equip_speed_bonus": equip_speed,
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
        base += combatant.get("equip_speed_bonus", 0)
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


def get_adjusted_position_mods(weapon_range, attacker, defender, enemies, is_crossbow=False):
    """Get position modifiers with adjustment for empty intervening rows.
    If there are no living enemies in the rows between attacker and defender,
    penalties are reduced (attacker can move through freely)."""
    pos_dmg, pos_acc = get_position_mods(
        weapon_range, attacker["row"], defender["row"], is_crossbow
    )

    # Only adjust for melee/reach attacks (ranged already shoot over)
    if weapon_range not in ("melee", "reach"):
        return pos_dmg, pos_acc

    # Check if any living enemies exist in intervening rows
    atk_row = attacker["row"]
    def_row = defender["row"]

    # Determine which side's enemies to check (attacker hits defenders)
    atk_type = attacker["type"]
    # Get the opposing side's combatants
    if atk_type == "player":
        blockers = enemies  # check if enemy rows between are empty
    else:
        # Enemy attacking player — not applicable (enemies don't have row blocking issues the same way)
        return pos_dmg, pos_acc

    row_order = [FRONT, MID, BACK]
    atk_idx = row_order.index(atk_row) if atk_row in row_order else 0
    def_idx = row_order.index(def_row) if def_row in row_order else 0

    # Find intervening rows (rows between attacker's target side and defender)
    # For player attacking enemies: if no enemies in front, mid-row enemies are easier to reach
    if atk_idx < def_idx:
        # Attacker is closer to front, defender is further back
        between_rows = row_order[atk_idx + 1:def_idx]
    elif atk_idx > def_idx:
        between_rows = row_order[def_idx + 1:atk_idx]
    else:
        between_rows = []

    if not between_rows:
        return pos_dmg, pos_acc

    # Check if any living enemies exist in the intervening rows
    has_blockers = False
    for enemy in blockers:
        if enemy["alive"] and enemy["row"] in between_rows:
            has_blockers = True
            break

    if not has_blockers:
        # No blockers — reduce the penalty by moving toward 1.0/+0
        # Halve the penalty (move halfway toward no-penalty)
        pos_dmg = pos_dmg + (1.0 - pos_dmg) * 0.6
        pos_acc = int(pos_acc * 0.4)  # reduce accuracy penalty by 60%

    return pos_dmg, pos_acc


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

    # Racial damage bonus (Half-Orc physical, etc.)
    if attacker.get("type") == "player":
        from core.races import get_racial_damage_multiplier
        phys_type = weapon.get("phys_type", "slashing")
        final *= get_racial_damage_multiplier(attacker.get("race_name", "Human"), phys_type)

    # Active buff multipliers (war_cry, hawk_eye, last_stand)
    if attacker.get("type") == "player":
        for st in attacker.get("status_effects", []):
            n = st["name"]
            if n in ("war_cry", "WarCry"):        final *= 1.25
            if n == "hawk_eye":                   final *= 1.20
            if n == "last_stand":
                if attacker["hp"] / max(1, attacker.get("max_hp", 1)) <= 0.25:
                    final *= 1.50

    # Active defense buff on defender (defense_up, iron_skin)
    if defender.get("type") == "player":
        for st in defender.get("status_effects", []):
            n = st["name"]
            if n == "defense_up":  final -= 5
            if n == "iron_skin":   final -= 8

    # Weapon enchant bonus (elemental damage added after defense)
    enchant_elem = weapon.get("enchant_element")
    enchant_bonus = weapon.get("enchant_bonus", 0)
    if enchant_elem and enchant_bonus > 0:
        elem_resist = defender.get("resistances", {}).get(enchant_elem, NEUTRAL)
        enchant_dmg = enchant_bonus * elem_resist
        final += enchant_dmg

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

    # Racial resistance on defender (Elf shadow resist, Gnome arcane resist, etc.)
    if defender.get("type") == "player":
        from core.races import get_racial_resist_multiplier
        final *= get_racial_resist_multiplier(defender.get("race_name", "Human"), element)

    # Racial damage bonus on attacker (Fading-Touched shadow bonus)
    if attacker.get("type") == "player":
        from core.races import get_racial_damage_multiplier
        final *= get_racial_damage_multiplier(attacker.get("race_name", "Human"), element)

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

    # Racial crit bonus (Halfling)
    if attacker.get("type") == "player":
        from core.races import get_racial_crit_bonus
        chance += get_racial_crit_bonus(attacker.get("race_name", "Human")) * 100

    is_crit = random.randint(1, 100) <= int(chance)
    return is_crit, crit_data if is_crit else None


# ═══════════════════════════════════════════════════════════════
#  ACTION RESOLUTION
# ═══════════════════════════════════════════════════════════════

def resolve_basic_attack(attacker, defender, enemies=None):
    """Resolve a basic physical attack. Returns a result dict."""
    weapon = attacker.get("weapon")
    if not weapon:
        weapon = get_weapon("Unarmed")

    # Position modifiers (adjusted for empty rows if enemies list provided)
    weapon_range = weapon.get("range", "melee")
    is_xbow = weapon.get("special", {}).get("is_crossbow", False)
    if enemies is not None:
        pos_dmg, pos_acc = get_adjusted_position_mods(
            weapon_range, attacker, defender, enemies, is_xbow
        )
    else:
        pos_dmg, pos_acc = get_position_mods(
            weapon_range, attacker["row"], defender["row"], is_xbow
        )

    # Accuracy check
    accuracy = calc_physical_accuracy(attacker, defender, weapon, pos_acc)
    hit = roll_hit(accuracy)

    # Racial dodge bonus on defender (Halfling)
    if hit and defender.get("type") == "player":
        from core.races import get_racial_dodge_bonus
        dodge = get_racial_dodge_bonus(defender.get("race_name", "Human"))
        if dodge > 0 and random.random() < dodge:
            hit = False  # dodged!

    # Evasion/smoke_screen status dodge
    if hit and defender.get("type") == "player":
        for st in defender.get("status_effects", []):
            if st["name"] in ("evasion", "smoke_screen"):
                if random.random() < 0.45:
                    hit = False
                    break

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

    # War Cry damage buff
    if attacker.get("_temp_dmg_buff"):
        raw *= attacker["_temp_dmg_buff"]

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


def resolve_move_position(combatant, direction):
    """Move a combatant one row forward or backward. Costs full action.
    direction: 'forward' or 'backward'
    Returns result dict with messages."""
    row_order = [BACK, MID, FRONT]
    current_idx = row_order.index(combatant["row"])

    if direction == "forward" and current_idx < len(row_order) - 1:
        new_row = row_order[current_idx + 1]
    elif direction == "backward" and current_idx > 0:
        new_row = row_order[current_idx - 1]
    else:
        return {
            "action": "move",
            "combatant": combatant,
            "messages": [f"{combatant['name']} can't move further {direction}!"],
        }

    old_row = combatant["row"]
    combatant["row"] = new_row
    return {
        "action": "move",
        "combatant": combatant,
        "messages": [f"{combatant['name']} moves from {old_row} to {new_row} row."],
    }


def resolve_ability(attacker, target, ability, all_players=None, all_enemies=None):
    """
    Resolve a spell/ability use. Returns result dict.

    Fully handles:
      - attack, spell, heal, aoe, aoe_heal, buff, debuff, cure, revive, taunt types
      - stun_chance, slow_chance, apply_poison, dot/dot_duration
      - bonus_crit, execute_threshold, hits (multi-hit), self_damage_pct
      - targets: "all_allies", aoe hitting all enemies
      - armor_shred (permanent defense reduction)
      - mark_duration / mark_crit_bonus (Death Mark / Warden's Mark)
      - revive type (Resurrection)
      - Active buff effects: war_cry, defense_up, evasion/smoke_screen, iron_skin,
        magic_shield, bulwark, last_stand, hawk_eye, ki_deflect, empty_mind, courage_aura
    """
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
        "extra_hits": [],   # list of (damage, target_name) for multi-hit log
    }

    # ── Resource cost ──────────────────────────────────────────
    resource_key = ability.get("resource", "")
    cost = ability.get("cost", 0)
    if resource_key and attacker["type"] == "player":
        from core.races import get_racial_mp_reduction
        reduction = get_racial_mp_reduction(attacker.get("race_name", "Human"))
        if reduction > 0 and resource_key in ("MP", "Mana"):
            cost = max(1, cost - reduction)
        current = attacker["resources"].get(resource_key, 0)
        if current < cost:
            result["hit"] = False
            result["messages"].append(
                f"{attacker['name']} doesn't have enough {resource_key}! "
                f"(need {cost}, have {current})"
            )
            return result
        attacker["resources"][resource_key] -= cost

    ab_name  = ability["name"].lower()
    ab_type  = ability.get("type", "spell")
    is_heal  = ab_type in ("heal", "aoe_heal") or "heal" in ab_name
    is_buff  = ab_type == "buff"
    is_debuff= ab_type == "debuff"
    is_cure  = ab_type == "cure"
    is_revive= ab_type == "revive"
    is_taunt = ab_type == "taunt"
    is_aoe   = ab_type in ("aoe", "aoe_heal")
    is_offensive = not (is_heal or is_buff or is_cure or is_revive or is_taunt)

    # ── Helpers ────────────────────────────────────────────────
    def _apply_bonus_crit(base_chance):
        return base_chance + ability.get("bonus_crit", 0)

    def _check_crit_with_bonus(attack_type, weapon=None):
        is_crit, crit_data = check_crit(attacker, attack_type, weapon)
        bonus = ability.get("bonus_crit", 0)
        if bonus > 0 and not is_crit:
            is_crit = random.randint(1, 100) <= bonus
            if is_crit:
                crit_data = {"multiplier": 1.5}
        return is_crit, crit_data

    def _inflict_special_effects(tgt, msg_prefix=""):
        """Apply stun_chance, slow_chance, apply_poison, dot, armor_shred after a hit."""
        msgs = []
        if ability.get("stun_chance") and random.random() < ability["stun_chance"]:
            if apply_status_effect(tgt, "Stunned", 1, 1.0):
                msgs.append(f"{msg_prefix}{tgt['name']} is STUNNED!")
        if ability.get("slow_chance") and random.random() < ability["slow_chance"]:
            if apply_status_effect(tgt, "Slowed", ability.get("slow_duration", 2), 1.0):
                msgs.append(f"{msg_prefix}{tgt['name']} is Slowed!")
        if ability.get("apply_poison"):
            poison_key = ability["apply_poison"]
            # Map progression poison keys → combat status
            POISON_MAP = {
                "poison_weak":   ("Poisoned",      2),
                "poison_strong": ("Poisoned",      3),
                "poison_deadly": ("Poisoned",      4),
            }
            sname, sdur = POISON_MAP.get(poison_key, ("Poisoned", 2))
            if apply_status_effect(tgt, sname, sdur, 1.0):
                msgs.append(f"{msg_prefix}{tgt['name']} is Poisoned!")
        if ability.get("dot"):
            dot_map = {"burning": "Burning"}
            sname = dot_map.get(ability["dot"], ability["dot"].capitalize())
            sdur  = ability.get("dot_duration", 2)
            if apply_status_effect(tgt, sname, sdur, 1.0):
                msgs.append(f"{msg_prefix}{tgt['name']} is {sname}!")
        if ability.get("armor_shred"):
            shred = ability["armor_shred"]
            tgt["defense"] = max(0, tgt.get("defense", 0) - shred)
            msgs.append(f"{msg_prefix}{tgt['name']}'s defense reduced by {shred}!")
        if ability.get("mark_duration"):
            tgt.setdefault("marks", []).append({
                "type": "death_mark",
                "crit_bonus": ability.get("mark_crit_bonus", 30),
                "duration": ability["mark_duration"],
            })
            msgs.append(f"{msg_prefix}{tgt['name']} is marked!")
        return msgs

    def _active_buff_mods(combatant):
        """Return (dmg_mult, def_reduction, evasion_chance, absorb_next)."""
        dmg_mult = 1.0
        def_reduce = 0
        evade_chance = 0.0
        absorb_next = False
        for st in combatant.get("status_effects", []):
            n = st["name"]
            if n == "war_cry":       dmg_mult *= 1.25
            if n == "WarCry":        dmg_mult *= 1.25
            if n == "hawk_eye":      dmg_mult *= 1.20
            if n == "last_stand" and combatant["hp"] / max(1, combatant["max_hp"]) <= 0.25:
                dmg_mult *= 1.50
            if n == "defense_up":    def_reduce += 5
            if n == "iron_skin":     def_reduce += 8
            if n == "magic_shield":  def_reduce += 6
            if n == "bulwark":       absorb_next = True
            if n in ("evasion", "smoke_screen"):
                evade_chance = max(evade_chance, 0.45)
            if n == "ki_deflect":    absorb_next = True
        return dmg_mult, def_reduce, evade_chance, absorb_next

    def _apply_physical_hit(tgt, power_mult=1.0):
        """Apply one physical ability hit. Returns (damage, is_crit, msgs)."""
        weapon = attacker.get("weapon") or get_weapon("Unarmed")
        pos_dmg, pos_acc = get_position_mods(
            weapon.get("range", "melee"), attacker["row"], tgt["row"]
        )
        acc = calc_physical_accuracy(attacker, tgt, weapon, pos_acc)
        acc += ability.get("bonus_accuracy", 0)
        if not roll_hit(acc):
            return 0, False, [f"{attacker['name']} uses {ability['name']} — MISS!"]

        # Evasion check
        _, _, evade, absorb = _active_buff_mods(tgt)
        if evade > 0 and random.random() < evade:
            return 0, False, [f"{tgt['name']} evades {ability['name']}!"]
        if absorb:
            _remove_status(tgt, ("bulwark", "ki_deflect"))
            return 0, False, [f"{tgt['name']} absorbs {ability['name']}!"]

        is_crit, crit_data = _check_crit_with_bonus("physical", weapon)
        ab_power = ability.get("power", 1.0) * power_mult
        ability_bonus = cost * ab_power * 0.5

        # Attacker buff
        atk_mult, _, _, _ = _active_buff_mods(attacker)
        # Defender buff (defense bonus)
        _, def_bonus, _, _ = _active_buff_mods(tgt)

        dmg = calc_physical_damage(
            attacker, tgt, weapon,
            position_dmg_mod=pos_dmg,
            ability_bonus=ability_bonus,
            is_crit=is_crit, crit_data=crit_data,
        )
        dmg = max(MINIMUM_DAMAGE, int(dmg * atk_mult - def_bonus))

        # Mark bonus damage
        for mark in tgt.get("marks", []):
            if mark["type"] == "death_mark" and is_crit:
                dmg = int(dmg * 1.3)

        tgt["hp"] = max(0, tgt["hp"] - dmg)
        if tgt["hp"] <= 0:
            tgt["alive"] = False
        crit_str = " CRITICAL!" if is_crit else ""
        return dmg, is_crit, [f"{attacker['name']} uses {ability['name']} on {tgt['name']} for {dmg} damage!{crit_str}"]

    def _apply_magic_hit(tgt, power_mult=1.0):
        """Apply one magic ability hit. Returns (damage, is_crit, msgs)."""
        acc = calc_magic_accuracy(attacker, tgt)
        if not roll_hit(acc):
            return 0, False, [f"{attacker['name']} casts {ability['name']} at {tgt['name']} — RESISTED!"]

        _, _, evade, absorb = _active_buff_mods(tgt)
        if absorb:
            _remove_status(tgt, ("magic_shield",))
            return 0, False, [f"{tgt['name']}'s magic shield absorbs {ability['name']}!"]

        is_crit, _ = _check_crit_with_bonus("spell")
        ab_power = ability.get("power", 1.0) * power_mult

        # Determine element
        element = ability.get("element", "arcane")
        if not ability.get("element"):
            for elem, keywords in [
                ("fire",      ["fire", "flame", "burn", "inferno", "meteor"]),
                ("ice",       ["ice", "frost", "freeze", "blizzard"]),
                ("lightning", ["lightning", "shock", "thunder", "storm", "chain"]),
                ("divine",    ["smite", "holy", "divine", "judgment", "wrath"]),
                ("shadow",    ["shadow", "dark", "void", "dread", "death"]),
                ("nature",    ["nature", "thorn", "entangle"]),
            ]:
                if any(kw in ab_name for kw in keywords):
                    element = elem
                    break

        spell = {"power": cost * ab_power, "element": element}

        atk_mult, _, _, _ = _active_buff_mods(attacker)
        _, def_bonus, _, _ = _active_buff_mods(tgt)

        dmg = calc_magic_damage(attacker, tgt, spell, is_crit)
        dmg = max(MINIMUM_DAMAGE, int(dmg * atk_mult))

        tgt["hp"] = max(0, tgt["hp"] - dmg)
        if tgt["hp"] <= 0:
            tgt["alive"] = False
        crit_str = " CRITICAL!" if is_crit else ""
        return dmg, is_crit, [f"{attacker['name']} casts {ability['name']} on {tgt['name']} for {dmg} damage!{crit_str}"]

    def _remove_status(combatant, names):
        combatant["status_effects"] = [
            s for s in combatant.get("status_effects", [])
            if s["name"] not in names
        ]

    def _log_death(tgt):
        if not tgt["alive"]:
            if tgt["type"] == "player":
                result["messages"].append(f"{tgt['name']} falls unconscious!")
            else:
                result["messages"].append(f"{tgt['name']} has fallen!")

    # ── REVIVE ─────────────────────────────────────────────────
    if is_revive:
        revive_tgt = target if (target and not target["alive"]) else None
        if not revive_tgt and all_players:
            revive_tgt = next((p for p in all_players if not p["alive"]), None)
        if revive_tgt:
            revive_tgt["alive"] = True
            revive_hp = int(revive_tgt["max_hp"] * ability.get("revive_hp_pct", 0.5))
            revive_tgt["hp"] = revive_hp
            result["healing"] = revive_hp
            result["messages"].append(
                f"{attacker['name']} uses {ability['name']} — "
                f"{revive_tgt['name']} is revived with {revive_hp} HP!"
            )
        else:
            result["messages"].append(
                f"{attacker['name']} uses {ability['name']} — no fallen allies to revive."
            )
        return result

    # ── TAUNT ──────────────────────────────────────────────────
    if is_taunt:
        dur = ability.get("taunt_duration", 2)
        if target:
            apply_status_effect(target, "Taunted", dur, 1.0)
            target["taunt_target_uid"] = attacker.get("uid")
            result["messages"].append(
                f"{attacker['name']} uses {ability['name']} — "
                f"{target['name']} must target {attacker['name']} for {dur} turn(s)!"
            )
        return result

    # ── CURE ───────────────────────────────────────────────────
    if is_cure:
        cure_tgt = target if target else attacker
        cures_type = ability.get("cures", "")
        removed = False
        CURE_MAP = {"poison": {"Poisoned", "Burning"}, "any": None}
        cure_set = CURE_MAP.get(cures_type)
        for se in cure_tgt.get("status_effects", [])[:]:
            if cure_set is None or se["name"] in cure_set or se.get("negative", True):
                cure_tgt["status_effects"].remove(se)
                result["messages"].append(
                    f"{attacker['name']} uses {ability['name']} on {cure_tgt['name']} — "
                    f"{se['name']} removed!"
                )
                removed = True
                break
        if not removed:
            result["messages"].append(
                f"{attacker['name']} uses {ability['name']} on {cure_tgt['name']} — "
                f"no matching effects to cure."
            )
        # If ability also heals (e.g. Nature's Balm)
        if ability.get("power") and cure_tgt["alive"]:
            heal_sp = {"power": cost * ability.get("power", 0.5)}
            amount = min(cure_tgt["max_hp"] - cure_tgt["hp"],
                         calc_healing(attacker, heal_sp))
            if amount > 0:
                cure_tgt["hp"] += amount
                result["healing"] += amount
                result["messages"].append(f"  Also heals {cure_tgt['name']} for {amount} HP.")
        return result

    # ── BUFF ───────────────────────────────────────────────────
    if is_buff:
        buff_name = ability.get("buff", ability["name"])
        duration  = ability.get("duration", 3)
        tgt_spec  = ability.get("targets", "self")
        self_only = ability.get("self_only", False)

        if self_only or tgt_spec == "self":
            buff_targets = [attacker]
        elif tgt_spec == "all_allies":
            buff_targets = [p for p in (all_players or [attacker]) if p["alive"]]
            if attacker not in buff_targets:
                buff_targets.append(attacker)
        elif target and target.get("type") == "player":
            buff_targets = [target]
        else:
            buff_targets = [attacker]

        applied_to = []
        for bt in buff_targets:
            apply_status_effect(bt, buff_name, duration, 1.0)
            applied_to.append(bt["name"])

        if len(applied_to) == 1:
            result["messages"].append(
                f"{attacker['name']} uses {ability['name']}! "
                f"{applied_to[0]} gains {buff_name} for {duration} turn(s)."
            )
        else:
            result["messages"].append(
                f"{attacker['name']} uses {ability['name']}! "
                f"Party gains {buff_name} for {duration} turn(s)."
            )
        return result

    # ── DEBUFF ─────────────────────────────────────────────────
    if is_debuff:
        acc = calc_magic_accuracy(attacker, target)
        if not roll_hit(acc):
            result["hit"] = False
            result["messages"].append(
                f"{attacker['name']} uses {ability['name']} on {target['name']} — RESISTED!"
            )
            return result

        debuff_name = ability.get("debuff", ability["name"])
        duration    = ability.get("slow_duration", ability.get("duration", 2))
        apply_status_effect(target, debuff_name, duration, 1.0)
        result["messages"].append(
            f"{attacker['name']} uses {ability['name']} on {target['name']}! "
            f"{target['name']} is {debuff_name}."
        )
        # Secondary effects
        result["messages"] += _inflict_special_effects(target)
        return result

    # ── HEAL / AOE_HEAL ────────────────────────────────────────
    if is_heal:
        if ab_type == "aoe_heal":
            heal_targets = [p for p in (all_players or [target or attacker]) if p["alive"]]
        else:
            heal_targets = [target if target else attacker]

        heal_spell = {"power": cost * ability.get("power", 1.0)}
        is_crit, _ = check_crit(attacker, "heal")
        total_healed = 0
        for ht in heal_targets:
            was_downed = not ht["alive"]
            if was_downed:
                ht["alive"] = True; ht["hp"] = 0
            amount = calc_healing(attacker, heal_spell)
            if is_crit:
                amount = int(amount * CRIT_HEAL_MULT)
            old_hp = ht["hp"]
            ht["hp"] = min(ht["max_hp"], ht["hp"] + amount)
            actual = ht["hp"] - old_hp
            total_healed += actual
            crit_str = " CRITICAL HEAL!" if is_crit else ""
            if was_downed:
                result["messages"].append(f"{attacker['name']} uses {ability['name']} — {ht['name']} revived for {actual} HP!{crit_str}")
            else:
                result["messages"].append(f"{attacker['name']} uses {ability['name']} on {ht['name']} — heals {actual} HP.{crit_str}")
        result["healing"] = total_healed
        result["is_crit"] = is_crit
        return result

    # ── OFFENSIVE ──────────────────────────────────────────────
    if is_offensive:
        resource_key_r = ability.get("resource", "")
        is_magic = resource_key_r in ("INT-MP", "WIS-MP", "PIE-MP")
        n_hits   = ability.get("hits", 1)
        hit_power = 1.0 / n_hits if n_hits > 1 else 1.0  # split power across hits

        # AOE: gather all targets
        if is_aoe:
            raw_targets = [e for e in (all_enemies or [target])
                           if e and e["alive"]] if not is_magic or True else []
            # "target: row" — just hit all enemies (simplified to all alive)
            aoe_targets = [e for e in (all_enemies or ([target] if target else []))
                           if e and e["alive"]]
            if not aoe_targets and target:
                aoe_targets = [target]
        else:
            aoe_targets = [target] if target else []

        if not aoe_targets:
            result["hit"] = False
            result["messages"].append(f"{attacker['name']} has no valid target!")
            return result

        total_damage = 0
        any_crit = False

        for aoe_tgt in aoe_targets:
            for hit_n in range(n_hits):
                if is_magic:
                    dmg, is_crit, msgs = _apply_magic_hit(aoe_tgt, hit_power)
                else:
                    dmg, is_crit, msgs = _apply_physical_hit(aoe_tgt, hit_power)
                total_damage += dmg
                if is_crit:
                    any_crit = True
                result["messages"] += msgs
                if dmg > 0:
                    result["messages"] += _inflict_special_effects(aoe_tgt)
                if not aoe_tgt["alive"]:
                    _log_death(aoe_tgt)
                    break  # no more hits on dead target

            # Execute threshold (single-target only, not AOE)
            if not is_aoe and ability.get("execute_threshold"):
                threshold = ability["execute_threshold"]
                hp_pct = aoe_tgt["hp"] / max(1, aoe_tgt["max_hp"])
                if hp_pct <= threshold and aoe_tgt["alive"]:
                    aoe_tgt["hp"] = 0
                    aoe_tgt["alive"] = False
                    result["messages"].append(
                        f"EXECUTE! {aoe_tgt['name']} is slain by {ability['name']}!"
                    )
                    _log_death(aoe_tgt)

        result["damage"]  = total_damage
        result["is_crit"] = any_crit
        result["hit"]     = total_damage > 0 or any_crit

        # Self-damage recoil (Reckless Charge)
        if ability.get("self_damage_pct") and total_damage > 0:
            recoil = max(1, int(attacker["max_hp"] * ability["self_damage_pct"]))
            attacker["hp"] = max(0, attacker["hp"] - recoil)
            if attacker["hp"] <= 0:
                attacker["alive"] = False
            result["messages"].append(
                f"{attacker['name']} takes {recoil} recoil damage!"
            )

    return result



# ═══════════════════════════════════════════════════════════════
#  STATUS EFFECT HELPERS
# ═══════════════════════════════════════════════════════════════

def apply_status_effect(target, status_name, duration, chance=1.0):
    """Try to apply a status effect to a target. Respects immunities.
    Returns True if applied, False if resisted/immune."""
    # Immunity check
    if status_name in target.get("status_immunities", []):
        return False

    # Chance check
    if chance < 1.0 and random.random() > chance:
        return False

    # Check if already afflicted — refresh duration if longer
    for existing in target.get("status_effects", []):
        if existing["name"] == status_name:
            existing["duration"] = max(existing["duration"], duration)
            return True

    target.setdefault("status_effects", []).append({
        "name": status_name,
        "duration": duration,
    })
    return True


def tick_status_effects(combatant):
    """Process end-of-round status ticks: deal damage, decrement duration,
    remove expired effects. Returns list of log messages."""
    messages = []
    remaining = []

    for status in combatant.get("status_effects", []):
        name = status["name"]

        # Tick damage (Poison, Burn, etc.)
        tick_dmg = STATUS_TICK_DAMAGE.get(name, 0)
        if tick_dmg > 0:
            combatant["hp"] = max(0, combatant["hp"] - tick_dmg)
            messages.append(
                f"{combatant['name']} takes {tick_dmg} damage from {name}!"
            )
            if combatant["hp"] <= 0:
                combatant["alive"] = False
                messages.append(f"{combatant['name']} has fallen to {name}!")

        # Decrement duration
        status["duration"] -= 1
        if status["duration"] > 0:
            remaining.append(status)
        else:
            messages.append(f"{name} wears off {combatant['name']}.")

    combatant["status_effects"] = remaining
    return messages


def has_status(combatant, status_name):
    """Check if a combatant currently has a given status effect."""
    return any(s["name"] == status_name for s in combatant.get("status_effects", []))


# ═══════════════════════════════════════════════════════════════
#  ENEMY AI — THREAT ASSESSMENT
# ═══════════════════════════════════════════════════════════════

def _calc_player_threat(player):
    """Score how threatening a player is to enemies.
    Higher = more dangerous = higher priority target."""
    base = CLASS_THREAT.get(player.get("class_name", ""), CLASS_THREAT_DEFAULT)

    # Wounded players are less threatening (and less worth targeting
    # unless you can finish them)
    hp_ratio = player["hp"] / max(1, player["max_hp"])

    # Scale threat by HP — full HP = full threat
    threat = base * (0.5 + 0.5 * hp_ratio)

    # Bonus threat if they're in a dangerous position (back row caster)
    if player["row"] == BACK and base >= 8:
        threat += 2  # casters in back row are extra valuable targets

    return threat


def _calc_finish_bonus(player, enemy):
    """If an enemy can likely one-shot a player, that's very attractive."""
    estimated_dmg = enemy.get("attack_damage", 5) + enemy["stats"].get("STR", 0) * 0.3
    if player["hp"] <= estimated_dmg * 1.2:
        return 8  # big bonus for finishable targets
    return 0


def _row_weight(attack_type, attacker_row, target_row):
    """How much does position favor this target? Melee strongly prefers
    front row. Ranged slightly prefers mid/back targets."""
    if attack_type == "melee":
        weights = {FRONT: 3.0, MID: 1.5, BACK: 0.5}
    elif attack_type == "ranged":
        weights = {FRONT: 1.0, MID: 1.5, BACK: 1.2}
    else:
        weights = {FRONT: 1.0, MID: 1.0, BACK: 1.0}
    return weights.get(target_row, 1.0)


# ═══════════════════════════════════════════════════════════════
#  ENEMY AI — ABILITY DECISION LOGIC
# ═══════════════════════════════════════════════════════════════

def _should_use_heal(enemy, enemies):
    """Check if a healing ability should be used. Returns (should_heal, target, ability) or (False, None, None)."""
    heal_abilities = [a for a in enemy.get("abilities", []) if a.get("type") == "heal"]
    if not heal_abilities:
        return False, None, None

    # Find wounded allies below 50% HP
    wounded = [e for e in enemies if e["alive"] and e["hp"] < e["max_hp"] * 0.50
               and e["uid"] != enemy["uid"]]
    if not wounded:
        return False, None, None

    target = min(wounded, key=lambda e: e["hp"] / max(1, e["max_hp"]))
    return True, target, heal_abilities[0]


def _should_use_buff(enemy, enemies):
    """Check if a buff ability should be used. Returns (should_buff, targets, ability) or (False, None, None)."""
    buff_abilities = [a for a in enemy.get("abilities", []) if a.get("type") == "buff"]
    if not buff_abilities:
        return False, None, None

    ability = buff_abilities[0]

    # Don't buff if most allies already have the buff active
    living_allies = [e for e in enemies if e["alive"] and e["uid"] != enemy["uid"]]
    if not living_allies:
        return False, None, None

    already_buffed = sum(1 for a in living_allies if has_status(a, "WarCry"))
    if already_buffed >= len(living_allies) * 0.6:
        return False, None, None

    return True, living_allies, ability


def _should_use_offensive_ability(enemy, players):
    """Check if an offensive ability should be used. Returns (should_use, target, ability) or (False, None, None)."""
    offense_abilities = [a for a in enemy.get("abilities", [])
                         if a.get("type") == "damage"]
    if not offense_abilities:
        return False, None, None

    ability = offense_abilities[0]
    living_players = [p for p in players if p["alive"]]
    if not living_players:
        return False, None, None

    # 60% chance to use offensive ability when available
    if random.random() > 0.60:
        return False, None, None

    # Prefer high-threat targets
    target = max(living_players, key=lambda p: _calc_player_threat(p))
    return True, target, ability


# ═══════════════════════════════════════════════════════════════
#  ENEMY AI — MAIN DECISION FUNCTION
# ═══════════════════════════════════════════════════════════════

def enemy_choose_action(enemy, players, enemies):
    """AI decision-making for enemy turns. Returns (action_type, target, ability).
    
    AI Types:
      random     — picks a random living player
      aggressive — targets the highest-threat player
      defensive  — targets the weakest player (finish them off)
      tactical   — smart targeting: threat + position + finish potential
      supportive — healer AI: heal first, offense second, melee fallback
      boss       — buff allies, smart targeting, can't be kited
    """
    living_players = [p for p in players if p["alive"]]
    if not living_players:
        return None, None, None

    # ── Taunted override: must target the taunting player ──
    if has_status(enemy, "Taunted"):
        taunt_uid = enemy.get("taunt_target_uid")
        if taunt_uid:
            taunt_tgt = next((p for p in living_players if p.get("uid") == taunt_uid), None)
            if taunt_tgt:
                return "attack", taunt_tgt, None

    ai_type = enemy.get("ai_type", "random")
    attack_type = enemy.get("attack_type", "melee")

    # ── Position correction: move toward preferred row if mispositioned ──
    # Skip for boss AI (they hold position) and supportive AI (they stay safe)
    preferred = enemy.get("preferred_row", FRONT)
    if ai_type not in ("boss", "supportive") and enemy["row"] != preferred:
        # Decide if repositioning is worth it
        should_move = False
        if attack_type == "ranged" and enemy["row"] == FRONT:
            # Ranged enemy stuck in front — big penalty, definitely move
            should_move = True
        elif attack_type == "melee" and enemy["row"] == BACK:
            # Melee enemy in back — huge damage penalty, move forward
            should_move = True
        elif enemy["row"] != preferred:
            # General preference to be in right row, 30% chance to reposition
            should_move = random.random() < 0.30

        if should_move:
            row_order = [BACK, MID, FRONT]
            current_idx = row_order.index(enemy["row"])
            preferred_idx = row_order.index(preferred)
            if preferred_idx > current_idx:
                return "move", "forward", None
            elif preferred_idx < current_idx:
                return "move", "backward", None

    # Supportive AI repositions only if in front row (get to safety)
    if ai_type == "supportive" and enemy["row"] == FRONT:
        return "move", "backward", None
    if ai_type == "supportive" and enemy["row"] == MID and preferred == BACK:
        if random.random() < 0.50:
            return "move", "backward", None

    # ── Supportive AI (Shamans, Healers) ──────────────────────
    if ai_type == "supportive" or (ai_type == "tactical" and
            any(a.get("type") == "heal" for a in enemy.get("abilities", []))):

        # Priority 1: Heal wounded allies
        should_heal, heal_target, heal_ability = _should_use_heal(enemy, enemies)
        if should_heal:
            return "ability", heal_target, heal_ability

        # Priority 2: Offensive ability
        should_attack, atk_target, atk_ability = _should_use_offensive_ability(enemy, living_players)
        if should_attack:
            return "ability", atk_target, atk_ability

        # Priority 3: Basic attack on highest-threat target
        target = max(living_players, key=lambda p: _calc_player_threat(p))
        return "attack", target, None

    # ── Boss AI ───────────────────────────────────────────────
    if ai_type == "boss":
        # Priority 1: Buff allies if available and not already buffed
        should_buff, buff_targets, buff_ability = _should_use_buff(enemy, enemies)
        if should_buff:
            return "ability", buff_targets, buff_ability

        # Priority 2: Tactical targeting (threat + finish potential)
        target = _pick_tactical_target(enemy, living_players)
        return "attack", target, None

    # ── Tactical AI ───────────────────────────────────────────
    if ai_type == "tactical":
        # Check for offensive abilities first
        should_attack, atk_target, atk_ability = _should_use_offensive_ability(enemy, living_players)
        if should_attack:
            return "ability", atk_target, atk_ability

        target = _pick_tactical_target(enemy, living_players)
        return "attack", target, None

    # ── Aggressive AI ─────────────────────────────────────────
    if ai_type == "aggressive":
        # Target the most threatening player, weighted by position
        scored = []
        for p in living_players:
            threat = _calc_player_threat(p)
            row_w = _row_weight(attack_type, enemy["row"], p["row"])
            scored.append((p, threat * row_w))
        scored.sort(key=lambda x: -x[1])

        # Pick from top 2 with some randomness
        top = scored[:min(2, len(scored))]
        target = random.choices(
            [t[0] for t in top],
            weights=[t[1] for t in top],
            k=1
        )[0]
        return "attack", target, None

    # ── Defensive AI ──────────────────────────────────────────
    if ai_type == "defensive":
        # Target lowest HP player (finish them off)
        # Bonus for targets we can actually kill
        scored = []
        for p in living_players:
            score = (1.0 - p["hp"] / max(1, p["max_hp"])) * 10
            score += _calc_finish_bonus(p, enemy)
            score *= _row_weight(attack_type, enemy["row"], p["row"])
            scored.append((p, score))
        scored.sort(key=lambda x: -x[1])
        target = scored[0][0]
        return "attack", target, None

    # ── Random AI (fallback) ──────────────────────────────────
    # Still slightly weighted by position (melee prefers front)
    weighted = []
    for p in living_players:
        w = _row_weight(attack_type, enemy["row"], p["row"])
        weighted.append((p, w))
    target = random.choices(
        [t[0] for t in weighted],
        weights=[t[1] for t in weighted],
        k=1
    )[0]
    return "attack", target, None


def _pick_tactical_target(enemy, living_players):
    """Smart target selection combining threat, position, and finish potential."""
    attack_type = enemy.get("attack_type", "melee")
    scored = []
    for p in living_players:
        threat = _calc_player_threat(p)
        finish = _calc_finish_bonus(p, enemy)
        row_w = _row_weight(attack_type, enemy["row"], p["row"])
        total = (threat + finish) * row_w
        scored.append((p, total))

    scored.sort(key=lambda x: -x[1])

    # Pick from top 2 with weighted randomness (not purely deterministic)
    top = scored[:min(2, len(scored))]
    return random.choices(
        [t[0] for t in top],
        weights=[t[1] for t in top],
        k=1
    )[0]


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

        # XP tracking: count rounds each player was alive (conscious)
        self.rounds_alive = {p["uid"]: 0 for p in self.players}

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
        """Handle end-of-round: status ticks, regen, rebuild turn order."""
        self.round_num += 1

        # Status effect ticks FIRST (poison can kill)
        for c in self.all_combatants:
            if c["alive"]:
                status_msgs = tick_status_effects(c)
                for m in status_msgs:
                    self.log(m)

        # Check for deaths from status ticks
        if not any(p["alive"] for p in self.players):
            self.phase = "defeat"
            self.log("═══ DEFEAT — Your party has fallen! ═══")
            return
        if not any(e["alive"] for e in self.enemies):
            self.phase = "victory"
            self.log("═══ VICTORY! ═══")
            self._calc_rewards()
            return

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

        # Tally XP: credit players who were alive this round
        for p in self.players:
            if p["alive"] and p["uid"] in self.rounds_alive:
                self.rounds_alive[p["uid"]] += 1

        self.log(f"── Round {self.round_num} ──")

    def execute_player_action(self, action_type, target=None, ability=None):
        """Execute a player's chosen action."""
        actor = self.get_current_combatant()
        if not actor or actor["type"] != "player":
            return

        if action_type == "attack":
            result = resolve_basic_attack(actor, target, enemies=self.enemies)
        elif action_type == "defend":
            result = resolve_defend(actor)
        elif action_type == "ability":
            result = resolve_ability(actor, target, ability,
                                     all_players=self.players,
                                     all_enemies=self.enemies)
        elif action_type == "move":
            result = resolve_move_position(actor, target)  # target is direction string
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

        # Skip stunned/frozen/petrified/sleeping
        for status in actor.get("status_effects", []):
            if status["name"] in STATUS_INCAPACITATE:
                self.log(f"{actor['name']} is {status['name']} and cannot act!")
                self.advance_turn()
                return

        action, target, ability = enemy_choose_action(actor, self.players, self.enemies)

        if action == "attack" and target:
            # Apply War Cry damage buff if active
            if has_status(actor, "WarCry"):
                actor["_temp_dmg_buff"] = ENEMY_BUFF_DMG_MULT
            result = resolve_enemy_attack(actor, target)
            actor.pop("_temp_dmg_buff", None)
            for msg in result.get("messages", []):
                self.log(msg)

        elif action == "move" and target:
            # target is direction string for move action
            result = resolve_move_position(actor, target)
            for msg in result.get("messages", []):
                self.log(msg)

        elif action == "ability" and ability:
            ab_type = ability.get("type", "")

            if ab_type == "heal" and target:
                # Healing ability
                power = ability.get("power", 10)
                amount = power + random.randint(0, 5)
                old_hp = target["hp"]
                target["hp"] = min(target["max_hp"], target["hp"] + amount)
                actual = target["hp"] - old_hp
                self.log(f"{actor['name']} uses {ability['name']} on {target['name']} — heals {actual} HP!")

            elif ab_type == "damage" and target:
                # Offensive ability (e.g., Poison Dart)
                power = ability.get("power", 8)
                element = ability.get("element", "arcane")

                # Accuracy check — magic-style
                casting_val = actor["stats"].get("INT", 0)
                def_wis = target["stats"].get("WIS", 0)
                acc = ACCURACY_BASE_MAGIC + (casting_val - def_wis) * ACCURACY_STAT_SCALE
                acc = max(ACCURACY_MIN, min(ACCURACY_MAX, acc))
                hit = roll_hit(acc)

                if not hit:
                    self.log(f"{actor['name']} uses {ability['name']} on {target['name']} — RESISTED!")
                else:
                    # Damage: power + INT scaling
                    raw = power + casting_val * 0.5
                    raw *= random.uniform(MAGIC_VARIANCE_MIN, MAGIC_VARIANCE_MAX)

                    # Elemental resistance
                    type_mod = target.get("resistances", {}).get(element, NEUTRAL)
                    raw *= type_mod

                    # Magic resistance
                    m_resist = target.get("magic_resist", 0)
                    damage = max(MINIMUM_DAMAGE, int(raw - m_resist))

                    target["hp"] = max(0, target["hp"] - damage)
                    if target["hp"] <= 0:
                        target["alive"] = False

                    self.log(f"{actor['name']} uses {ability['name']} on {target['name']} for {damage} damage!")

                    if not target["alive"]:
                        self.log(f"{target['name']} falls unconscious!")

                    # Apply status effect if ability has one
                    status_name = ability.get("status")
                    status_chance = ability.get("status_chance", 0)
                    status_dur = ability.get("status_duration", 2)
                    if status_name and target["alive"]:
                        applied = apply_status_effect(
                            target, status_name, status_dur, status_chance
                        )
                        if applied:
                            self.log(f"{target['name']} is now {status_name}!")

            elif ab_type == "buff":
                # Buff ability (e.g., War Cry — targets all allies)
                if isinstance(target, list):
                    # Multi-target buff
                    buff_targets = [t for t in target if t["alive"]]
                    for t in buff_targets:
                        apply_status_effect(t, "WarCry", ENEMY_BUFF_DURATION, 1.0)
                    self.log(f"{actor['name']} uses {ability['name']}! Allies are empowered!")
                elif target:
                    apply_status_effect(target, "WarCry", ENEMY_BUFF_DURATION, 1.0)
                    self.log(f"{actor['name']} uses {ability['name']} on {target['name']}!")
        else:
            self.log(f"{actor['name']} hesitates...")

        self.advance_turn()

    def _calc_rewards(self):
        """Calculate XP (round-conscious %), gold (even split), and loot drops."""
        from data.enemies import ENEMIES

        # ── Flush final round: credit alive players ──
        for p in self.players:
            if p["alive"] and p["uid"] in self.rounds_alive:
                self.rounds_alive[p["uid"]] += 1

        total_rounds = max(1, self.round_num)

        # ── Total XP and gold from enemies ──
        total_xp = 0
        total_gold = 0
        for e in self.enemies:
            template = ENEMIES.get(e["template_key"], {})
            total_xp += template.get("xp_reward", 0)
            gold_range = template.get("gold_reward", (0, 0))
            total_gold += random.randint(gold_range[0], gold_range[1])

        # ── XP distribution: percentage-based on rounds alive ──
        # Formula: share_pct = max(0.25, rounds_alive / total_rounds)
        #          character_xp = share_pct × (total_xp / party_size)
        XP_FLOOR = 0.25
        party_size = len(self.players)
        per_member_full = total_xp / max(1, party_size)

        xp_awards = {}
        for p in self.players:
            alive_rounds = self.rounds_alive.get(p["uid"], 0)
            share_pct = max(XP_FLOOR, alive_rounds / total_rounds)
            awarded = int(per_member_full * share_pct)
            xp_awards[p["uid"]] = {
                "name": p["name"],
                "xp": awarded,
                "rounds_alive": alive_rounds,
                "total_rounds": total_rounds,
                "share_pct": share_pct,
                "alive": p["alive"],
            }

        # ── Gold: even split across all party members ──
        gold_each = total_gold // max(1, party_size)
        gold_remainder = total_gold % max(1, party_size)

        # ── Loot drops from enemies ──
        loot_drops = []
        for e in self.enemies:
            template = ENEMIES.get(e["template_key"], {})
            loot_table = template.get("loot_table", [])
            for entry in loot_table:
                if random.random() <= entry.get("drop_chance", 0):
                    item = dict(entry["item"])
                    item["identified"] = False  # all drops start unidentified
                    item["source"] = e["name"]
                    loot_drops.append(item)

        # ── Boss bonus loot (unique magic items) ──
        try:
            from data.magic_items import get_boss_bonus_drops
            for e in self.enemies:
                if e.get("ai_type") == "boss" or ENEMIES.get(e["template_key"], {}).get("ai_type") == "boss":
                    bonus = get_boss_bonus_drops(e["template_key"], random)
                    for item in bonus:
                        item["source"] = e["name"]
                        item["identified"] = True  # boss uniques come identified
                        loot_drops.append(item)
        except ImportError:
            pass

        # ── Store results ──
        enemy_names = list(set(e["name"] for e in self.enemies))
        self.rewards = {
            "total_xp": total_xp,
            "total_gold": total_gold,
            "gold_each": gold_each,
            "gold_remainder": gold_remainder,
            "xp_awards": xp_awards,
            "loot_drops": loot_drops,
            "loot_assigned": {},  # uid → list of items (filled by UI)
            "enemy_names": enemy_names,
        }

        # ── Log summary ──
        self.log(f"Gold: {total_gold} ({gold_each} each)")
        self.log(f"XP distribution:")
        for uid, info in xp_awards.items():
            status = "" if info["alive"] else " (unconscious)"
            pct_str = f"{info['share_pct']*100:.0f}%"
            rounds_str = f"{info['rounds_alive']}/{info['total_rounds']} rounds"
            self.log(f"  {info['name']}: {info['xp']} XP ({pct_str} — {rounds_str}){status}")

        if loot_drops:
            self.log(f"{len(loot_drops)} item(s) dropped!")
            for item in loot_drops:
                self.log(f"  ??? {item.get('type', 'Item')} (unidentified)")

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
