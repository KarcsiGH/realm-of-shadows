"""
Realm of Shadows — Character Progression Framework

XP tables, per-level stat gains, class transitions, level up at inn.
"""
import random

# ═══════════════════════════════════════════════════════════════
#  XP TABLE (Level 1-30)
# ═══════════════════════════════════════════════════════════════

XP_TABLE = {
    1: 0, 2: 100, 3: 300, 4: 600, 5: 1000,
    6: 1500, 7: 2200, 8: 3100, 9: 4200, 10: 5500,
    11: 7000, 12: 8500, 13: 10000, 14: 11500, 15: 13000,
    16: 15000, 17: 17500, 18: 20500, 19: 24000, 20: 28000,
    21: 33000, 22: 39000, 23: 46000, 24: 54000, 25: 64000,
    26: 76000, 27: 90000, 28: 108000, 29: 130000, 30: 160000,
}

MAX_LEVEL = 30

def xp_for_level(level):
    return XP_TABLE.get(level, 999999999)

def xp_for_next_level(current_level):
    if current_level >= MAX_LEVEL:
        return 0
    return XP_TABLE.get(current_level + 1, 999999999)

def can_level_up(character):
    """Check if character has enough XP but hasn't leveled yet."""
    if character.level >= MAX_LEVEL:
        return False
    needed = xp_for_next_level(character.level)
    return character.xp >= needed


# ═══════════════════════════════════════════════════════════════
#  STAT GAINS PER LEVEL (automatic class-based)
# ═══════════════════════════════════════════════════════════════

# Each entry: {stat: (base_gain_per_level, bonus_at_even_levels)}
# Plus 1 free point player assigns

LEVEL_STAT_GAINS = {
    "Fighter": {
        "auto": {"STR": 1, "CON": 1},
        "even_bonus": {"DEX": 1},
        "hp_base": 10, "hp_random": 2,   # 10 + 0-2 per level
        "sp_base": 4,  "sp_random": 1,
        "mp_base": 0,  "mp_random": 0,
    },
    "Knight": {
        "auto": {"STR": 1, "CON": 1},
        "even_bonus": {"PIE": 1},
        "hp_base": 9, "hp_random": 1,
        "sp_base": 3,  "sp_random": 1,
        "mp_base": 0,  "mp_random": 0,
    },
    "Thief": {
        "auto": {"DEX": 1, "WIS": 1},
        "odd_bonus": {"STR": 1},
        "hp_base": 6, "hp_random": 1,
        "sp_base": 5,  "sp_random": 1,
        "mp_base": 0,  "mp_random": 0,
    },
    "Ranger": {
        "auto": {"DEX": 1, "WIS": 1},
        "even_bonus": {"CON": 1},
        "hp_base": 7, "hp_random": 1,
        "sp_base": 4,  "sp_random": 1,
        "mp_base": 2,  "mp_random": 1,
    },
    "Mage": {
        "auto": {"INT": 1, "WIS": 1},
        "even_bonus": {"DEX": 1},
        "hp_base": 4, "hp_random": 1,
        "sp_base": 0,  "sp_random": 0,
        "mp_base": 8,  "mp_random": 2,
    },
    "Cleric": {
        "auto": {"WIS": 1, "PIE": 1},
        "odd_bonus": {"CON": 1},
        "hp_base": 6, "hp_random": 1,
        "sp_base": 0,  "sp_random": 0,
        "mp_base": 6,  "mp_random": 2,
    },
    "Monk": {
        "auto": {"WIS": 1, "DEX": 1},
        "even_bonus": {"CON": 1},
        "hp_base": 7, "hp_random": 1,
        "sp_base": 3,  "sp_random": 1,
        "mp_base": 2,  "mp_random": 1,
    },
}

# Hybrid and advanced classes (framework — abilities filled in later milestones)
LEVEL_STAT_GAINS["Warder"] = {
    "auto": {"STR": 1, "PIE": 1}, "even_bonus": {"CON": 1},
    "hp_base": 8, "hp_random": 2, "sp_base": 3, "sp_random": 1,
    "mp_base": 3, "mp_random": 1,
}
LEVEL_STAT_GAINS["Paladin"] = {
    "auto": {"STR": 1, "PIE": 1}, "even_bonus": {"WIS": 1},
    "hp_base": 8, "hp_random": 1, "sp_base": 3, "sp_random": 1,
    "mp_base": 4, "mp_random": 1,
}
LEVEL_STAT_GAINS["Assassin"] = {
    "auto": {"DEX": 1, "STR": 1}, "even_bonus": {"INT": 1},
    "hp_base": 6, "hp_random": 1, "sp_base": 5, "sp_random": 1,
    "mp_base": 0, "mp_random": 0,
}
LEVEL_STAT_GAINS["Warden"] = {
    "auto": {"WIS": 1, "DEX": 1}, "even_bonus": {"PIE": 1},
    "hp_base": 7, "hp_random": 1, "sp_base": 3, "sp_random": 1,
    "mp_base": 4, "mp_random": 1,
}
LEVEL_STAT_GAINS["Spellblade"] = {
    "auto": {"INT": 1, "STR": 1}, "even_bonus": {"DEX": 1},
    "hp_base": 6, "hp_random": 2, "sp_base": 2, "sp_random": 1,
    "mp_base": 5, "mp_random": 2,
}
LEVEL_STAT_GAINS["Templar"] = {
    "auto": {"PIE": 1, "STR": 1}, "even_bonus": {"CON": 1},
    "hp_base": 7, "hp_random": 2, "sp_base": 2, "sp_random": 1,
    "mp_base": 4, "mp_random": 1,
}
LEVEL_STAT_GAINS["Champion"] = {
    "auto": {"STR": 2, "CON": 1}, "even_bonus": {"DEX": 1},
    "hp_base": 12, "hp_random": 2, "sp_base": 5, "sp_random": 1,
    "mp_base": 0, "mp_random": 0,
}
LEVEL_STAT_GAINS["Crusader"] = {
    "auto": {"STR": 1, "PIE": 1, "CON": 1}, "even_bonus": {},
    "hp_base": 10, "hp_random": 2, "sp_base": 4, "sp_random": 1,
    "mp_base": 3, "mp_random": 1,
}
LEVEL_STAT_GAINS["Shadow Master"] = {
    "auto": {"DEX": 2, "WIS": 1}, "even_bonus": {"INT": 1},
    "hp_base": 6, "hp_random": 1, "sp_base": 6, "sp_random": 1,
    "mp_base": 2, "mp_random": 1,
}
LEVEL_STAT_GAINS["Beastlord"] = {
    "auto": {"WIS": 2, "DEX": 1}, "even_bonus": {"CON": 1},
    "hp_base": 8, "hp_random": 1, "sp_base": 4, "sp_random": 1,
    "mp_base": 4, "mp_random": 1,
}
LEVEL_STAT_GAINS["Archmage"] = {
    "auto": {"INT": 2, "WIS": 1}, "even_bonus": {"PIE": 1},
    "hp_base": 4, "hp_random": 1, "sp_base": 0, "sp_random": 0,
    "mp_base": 10, "mp_random": 3,
}
LEVEL_STAT_GAINS["High Priest"] = {
    "auto": {"PIE": 2, "WIS": 1}, "even_bonus": {"INT": 1},
    "hp_base": 6, "hp_random": 1, "sp_base": 0, "sp_random": 0,
    "mp_base": 8, "mp_random": 2,
}
LEVEL_STAT_GAINS["Witch"] = {
    "auto": {"WIS": 1, "INT": 1}, "even_bonus": {"PIE": 1},
    "hp_base": 4, "hp_random": 1, "sp_base": 0, "sp_random": 0,
    "mp_base": 7, "mp_random": 2,
}
LEVEL_STAT_GAINS["Necromancer"] = {
    "auto": {"INT": 1, "PIE": 1}, "even_bonus": {"CON": 1},
    "hp_base": 5, "hp_random": 1, "sp_base": 0, "sp_random": 0,
    "mp_base": 8, "mp_random": 2,
}


# ═══════════════════════════════════════════════════════════════
#  CLASS TRANSITIONS
# ═══════════════════════════════════════════════════════════════

CLASS_TRANSITIONS = {
    # Hybrid classes (level 8+)
    "Warder":       {"base_classes": ["Fighter"],       "min_level": 8,  "min_stats": {"PIE": 12}},
    "Paladin":      {"base_classes": ["Knight"],        "min_level": 8,  "min_stats": {"PIE": 14, "WIS": 12}},
    "Assassin":     {"base_classes": ["Thief"],         "min_level": 8,  "min_stats": {"STR": 12, "DEX": 16}},
    "Warden":       {"base_classes": ["Ranger"],        "min_level": 8,  "min_stats": {"WIS": 14, "PIE": 10}},
    "Spellblade":   {"base_classes": ["Mage"],          "min_level": 8,  "min_stats": {"STR": 12, "INT": 16}},
    "Templar":      {"base_classes": ["Cleric"],        "min_level": 8,  "min_stats": {"STR": 12, "CON": 12}},
    # Advanced classes (level 15+)
    "Champion":     {"base_classes": ["Fighter"],       "min_level": 15, "min_stats": {"STR": 20, "CON": 18}},
    "Crusader":     {"base_classes": ["Knight"],        "min_level": 15, "min_stats": {"STR": 18, "PIE": 16}},
    "Shadow Master":{"base_classes": ["Thief"],         "min_level": 15, "min_stats": {"DEX": 22}},
    "Beastlord":    {"base_classes": ["Ranger"],        "min_level": 15, "min_stats": {"WIS": 18, "DEX": 18}},
    "Archmage":     {"base_classes": ["Mage"],          "min_level": 15, "min_stats": {"INT": 22, "WIS": 16}},
    "High Priest":  {"base_classes": ["Cleric"],        "min_level": 15, "min_stats": {"PIE": 22, "WIS": 18}},
    # Special classes (level 10+)
    "Witch":        {"base_classes": ["Mage", "Cleric"],"min_level": 10, "min_stats": {"WIS": 16, "INT": 14, "PIE": 12}},
    "Necromancer":  {"base_classes": ["Mage"],          "min_level": 10, "min_stats": {"INT": 18, "PIE": 14, "CON": 12}},
}

def get_available_transitions(character):
    """Return list of class names this character can transition to."""
    available = []
    for cls_name, req in CLASS_TRANSITIONS.items():
        if character.class_name not in req["base_classes"]:
            continue
        if character.level < req["min_level"]:
            continue
        meets_stats = True
        for stat, minimum in req["min_stats"].items():
            if character.stats.get(stat, 0) < minimum:
                meets_stats = False
                break
        if meets_stats:
            available.append(cls_name)
    return available


# ═══════════════════════════════════════════════════════════════
#  TRAINING COSTS
# ═══════════════════════════════════════════════════════════════

def training_cost(level):
    """Gold cost to train to this level (on top of inn room).
    Designed so a first dungeon run covers full party level 2 training."""
    if level <= 3:   return level * 10     # 20g, 30g — very affordable early
    if level <= 5:   return level * 30     # 120g, 150g
    if level <= 8:   return level * 75     # 450-600g
    if level <= 12:  return level * 150    # 1350-1800g
    if level <= 16:  return level * 300    # 3900-4800g
    if level <= 20:  return level * 500    # 8500-10000g
    if level <= 25:  return level * 800    # 16800-20000g
    return level * 1500                     # 39000-45000g


# ═══════════════════════════════════════════════════════════════
#  LEVEL UP LOGIC
# ═══════════════════════════════════════════════════════════════

def apply_level_up(character, free_stat=None):
    """Apply one level up to a character. Returns summary dict.
    free_stat: stat name for the player's free point, or None to skip."""
    if character.level >= MAX_LEVEL:
        return None
    if not can_level_up(character):
        return None

    character.level += 1
    new_level = character.level
    cls = character.class_name
    gains = LEVEL_STAT_GAINS.get(cls)
    if not gains:
        gains = LEVEL_STAT_GAINS.get("Fighter")  # fallback

    summary = {"level": new_level, "stat_gains": {}, "hp_gain": 0, "free_stat": free_stat}

    # Automatic stat gains
    for stat, amount in gains.get("auto", {}).items():
        character.stats[stat] = character.stats.get(stat, 0) + amount
        summary["stat_gains"][stat] = summary["stat_gains"].get(stat, 0) + amount

    # Even/odd level bonus
    if new_level % 2 == 0:
        for stat, amount in gains.get("even_bonus", {}).items():
            character.stats[stat] = character.stats.get(stat, 0) + amount
            summary["stat_gains"][stat] = summary["stat_gains"].get(stat, 0) + amount
    else:
        for stat, amount in gains.get("odd_bonus", {}).items():
            character.stats[stat] = character.stats.get(stat, 0) + amount
            summary["stat_gains"][stat] = summary["stat_gains"].get(stat, 0) + amount

    # Free stat point
    if free_stat and free_stat in character.stats:
        character.stats[free_stat] = character.stats.get(free_stat, 0) + 1
        summary["stat_gains"][free_stat] = summary["stat_gains"].get(free_stat, 0) + 1

    # HP gain (fixed base + random bonus)
    hp_gain = gains["hp_base"] + random.randint(0, gains["hp_random"])
    summary["hp_gain"] = hp_gain

    # Learn new abilities for this level
    from core.abilities import CLASS_ABILITIES, get_branch_at_level, ABILITY_BRANCHES
    class_abilities = CLASS_ABILITIES.get(cls, [])
    known_names = {a["name"] for a in character.abilities}
    new_abilities = []

    # Collect ALL branch ability names for this class (across every branch level),
    # not just the current level — prevents early auto-learn of future branch choices.
    all_branch_names = {
        opt["name"]
        for level_opts in ABILITY_BRANCHES.get(cls, {}).values()
        for opt in level_opts
    }

    # Get branch options exactly at this level (if any) — player must choose one
    branch_opts = get_branch_at_level(cls, new_level)

    for ab in class_abilities:
        if ab["name"] not in known_names and ab.get("level", 1) <= new_level:
            # Skip ALL branch abilities — player picks these at the right branch level
            if ab["name"] in all_branch_names:
                continue
            character.abilities.append(ab.copy())
            new_abilities.append(ab["name"])
    summary["new_abilities"] = new_abilities
    summary["branch_choice"] = branch_opts  # None or [opt_A, opt_B]

    # Recalculate all resources to new maxes (but don't heal — inn rest does that)
    # The caller should recalculate resources after this

    return summary


# ═══════════════════════════════════════════════════════════════
#  INN TIERS
# ═══════════════════════════════════════════════════════════════

INN_TIERS = {
    "stable": {
        "name": "Stable",
        "cost_per_char": 0,
        "description": "Sleep in the stable. No recovery, but your progress is saved.",
        "hp_restore": 0.0,
        "mp_restore": 0.0,
        "sp_restore": 0.0,
        "allows_level_up": False,
        "buff": None,
    },
    "common": {
        "name": "Common Room",
        "cost_per_char": 20,
        "description": "A bench and a meal. Restores 50% of HP, MP, and SP.",
        "hp_restore": 0.50,
        "mp_restore": 0.50,
        "sp_restore": 0.50,
        "allows_level_up": True,
        "buff": None,
    },
    "private": {
        "name": "Private Room",
        "cost_per_char": 75,
        "description": "A proper bed and hot food. Full restoration.",
        "hp_restore": 1.0,
        "mp_restore": 1.0,
        "sp_restore": 1.0,
        "allows_level_up": True,
        "buff": None,
    },
    "suite": {
        "name": "Suite",
        "cost_per_char": 200,
        "description": "Luxury quarters. Full restoration plus a blessing for your next venture.",
        "hp_restore": 1.0,
        "mp_restore": 1.0,
        "sp_restore": 1.0,
        "allows_level_up": True,
        "buff": {"name": "Well Rested", "hp_bonus_pct": 10, "duration": "next_dungeon"},
    },
}

INN_TIER_ORDER = ["stable", "common", "private", "suite"]


# ═══════════════════════════════════════════════════════════════
#  RESOURCE TRICKLE (per step recovery)
# ═══════════════════════════════════════════════════════════════

TRICKLE_HP_PCT = 0.005  # 0.5% max HP per step
TRICKLE_MP_PCT = 0.01   # 1% max MP per step
TRICKLE_SP_PCT = 0.015  # 1.5% max SP per step

def apply_step_regen(character, max_resources):
    """Apply per-step resource trickle. Call after each movement step."""
    for res_name, current in character.resources.items():
        max_val = max_resources.get(res_name, 0)
        if max_val <= 0 or current >= max_val:
            continue
        if res_name == "HP":
            gain = max(1, int(max_val * TRICKLE_HP_PCT))
        elif "MP" in res_name or res_name == "Ki":
            gain = max(1, int(max_val * TRICKLE_MP_PCT))
        elif "SP" in res_name:
            gain = max(1, int(max_val * TRICKLE_SP_PCT))
        else:
            continue
        character.resources[res_name] = min(max_val, current + gain)


# ═══════════════════════════════════════════════════════════════
#  STATUS EFFECTS (poison, curse, resurrection sickness)
# ═══════════════════════════════════════════════════════════════

STATUS_EFFECTS = {
    "poison_weak":    {"name": "Weak Poison",    "type": "poison", "dmg_per_tick": 4,  "tick_steps": 3, "total_ticks": 4},
    "poison_strong":  {"name": "Strong Poison",  "type": "poison", "dmg_per_tick": 10, "tick_steps": 3, "total_ticks": 6},
    "poison_deadly":  {"name": "Deadly Poison",  "type": "poison", "dmg_per_tick": 18, "tick_steps": 3, "total_ticks": 8},
    "resurrection_sickness": {"name": "Resurrection Sickness", "type": "debuff",
                              "stat_penalty_pct": 15, "cure": "inn_rest"},
    "curse_weakness":  {"name": "Weakness",  "type": "curse", "effect": "dmg_dealt_mult",  "value": 0.80},
    "curse_fragility": {"name": "Fragility", "type": "curse", "effect": "max_hp_mult",     "value": 0.80},
    "curse_silence":   {"name": "Silence",   "type": "curse", "effect": "no_spells",        "value": True},
    "curse_jinx":      {"name": "Jinx",      "type": "curse", "effect": "accuracy_penalty", "value": 0.85},
    "curse_doom":      {"name": "Doom",       "type": "curse", "effect": "hp_drain",        "value": 1, "drain_steps": 10},
}

# ═══════════════════════════════════════════════════════════════
#  DEATH THRESHOLDS
# ═══════════════════════════════════════════════════════════════

def death_threshold(max_hp):
    """HP value at which character is truly dead (negative 50% max)."""
    return -(max_hp // 2)

def is_unconscious(hp):
    """Character is unconscious at 0 or below but not dead."""
    return hp <= 0

def is_dead(hp, max_hp):
    """Character is dead when below the threshold."""
    return hp <= death_threshold(max_hp)

REVIVAL_STAT_LOSS_CHANCE = 0.01  # 1% chance per revival
REVIVAL_HP_LOSS_PCT = 0.05       # 5% max HP loss if triggered
