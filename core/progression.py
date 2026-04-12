"""
Realm of Shadows — Character Progression Framework

XP tables, per-level stat gains, class transitions, level up at inn.
"""
import random

# ═══════════════════════════════════════════════════════════════
#  XP TABLE (Level 1-30)
# ═══════════════════════════════════════════════════════════════

XP_TABLE = {
    # Rebalanced for 6-player party, 2-3 levels per dungeon, final ~L22
    # Early (L1-5): fast and satisfying — earn each level in one dungeon wing
    1: 0,       2: 600,     3: 1400,    4: 2400,    5: 3600,
    # Mid (L6-10): dungeon-paced — one major dungeon per level
    6: 5100,    7: 7100,    8: 9600,    9: 12800,   10: 16800,
    # Late (L11-15): milestone levels — advanced class territory
    11: 21800,  12: 27800,  13: 34800,  14: 43300,  15: 53300,
    # Endgame (L16-20): earned through Act 3 dungeons
    16: 65300,  17: 79300,  18: 95300,  19: 113800, 20: 134800,
    # Prestige (L21-30): for completionists
    21: 158800, 22: 185800, 23: 215800, 24: 248800, 25: 285800,
    26: 326800, 27: 371800, 28: 421800, 29: 476800, 30: 536800,
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


LEVEL_STAT_GAINS["Strider"] = {
    # Fighter+Ranger: mobile skirmisher — DEX primary, STR secondary, some WIS
    "auto": {"DEX": 1, "STR": 1}, "even_bonus": {"WIS": 1},
    "hp_base": 8, "hp_random": 1, "sp_base": 5, "sp_random": 1,
    "mp_base": 1, "mp_random": 1,
}
LEVEL_STAT_GAINS["Guardian"] = {
    # Fighter+Monk: armored ki protector — STR+CON, WIS at even levels
    "auto": {"STR": 1, "CON": 1}, "even_bonus": {"WIS": 1},
    "hp_base": 10, "hp_random": 2, "sp_base": 3, "sp_random": 1,
    "mp_base": 2, "mp_random": 1,
}
LEVEL_STAT_GAINS["Druid"] = {
    # Mage+Ranger: nature spellcaster — WIS primary, INT secondary, CON at even
    "auto": {"WIS": 1, "INT": 1}, "even_bonus": {"CON": 1},
    "hp_base": 5, "hp_random": 1, "sp_base": 0, "sp_random": 0,
    "mp_base": 7, "mp_random": 2,
}
LEVEL_STAT_GAINS["Mystic"] = {
    # Mage+Monk: arcane ki master — INT+WIS, DEX at even
    "auto": {"INT": 1, "WIS": 1}, "even_bonus": {"DEX": 1},
    "hp_base": 5, "hp_random": 1, "sp_base": 2, "sp_random": 1,
    "mp_base": 6, "mp_random": 2,
}
LEVEL_STAT_GAINS["Inquisitor"] = {
    # Cleric+Thief: divine shadow hunter — WIS+DEX auto, PIE at odd
    "auto": {"WIS": 1, "DEX": 1}, "odd_bonus": {"PIE": 1},
    "hp_base": 6, "hp_random": 1, "sp_base": 4, "sp_random": 1,
    "mp_base": 3, "mp_random": 1,
}
LEVEL_STAT_GAINS["Phantom"] = {
    # Thief+Monk: ki shadow — DEX+WIS auto, CON at even
    "auto": {"DEX": 1, "WIS": 1}, "even_bonus": {"CON": 1},
    "hp_base": 6, "hp_random": 1, "sp_base": 5, "sp_random": 1,
    "mp_base": 2, "mp_random": 1,
}
LEVEL_STAT_GAINS["Shaman"] = {
    # Ranger+Monk: wilderness spiritualist — WIS primary, DEX secondary, CON even
    "auto": {"WIS": 1, "DEX": 1}, "even_bonus": {"CON": 1},
    "hp_base": 7, "hp_random": 1, "sp_base": 3, "sp_random": 1,
    "mp_base": 5, "mp_random": 1,
}
LEVEL_STAT_GAINS["Ascetic"] = {
    # Monk apex (L15): transcendent ki master — WIS+DEX, CON even, solid HP
    "auto": {"WIS": 2, "DEX": 1}, "even_bonus": {"CON": 1},
    "hp_base": 8, "hp_random": 2, "sp_base": 4, "sp_random": 1,
    "mp_base": 4, "mp_random": 2,
}

# ═══════════════════════════════════════════════════════════════
#  CLASS TRANSITIONS
# ═══════════════════════════════════════════════════════════════

CLASS_TRANSITIONS = {
    # ── HYBRID CLASSES (level 10) ────────────────────────────────────────────
    # Two base classes merge. A character qualifies if their current class is
    # EITHER parent class and they meet the stat minimums.
    # Fighter hybrids
    "Paladin":      {"base_classes": ["Fighter", "Cleric"],  "min_level": 10,
                     "min_stats": {"STR": 14, "PIE": 14},
                     "description": "Holy warrior combining divine magic and combat prowess."},
    "Spellblade":   {"base_classes": ["Fighter", "Mage"],    "min_level": 10,
                     "min_stats": {"STR": 12, "INT": 14},
                     "description": "Arcane warrior who channels spells through their blade."},
    "Warder":       {"base_classes": ["Fighter", "Thief"],   "min_level": 10,
                     "min_stats": {"STR": 12, "DEX": 14},
                     "description": "Tactical combatant combining heavy strikes and shadow techniques."},
    "Duskblade":    {"base_classes": ["Fighter", "Ranger"],  "min_level": 10,
                     "min_stats": {"STR": 12, "DEX": 14},
                     "description": "Mobile skirmisher excelling at rapid movement and precise strikes."},
    "Guardian":     {"base_classes": ["Fighter", "Monk"],    "min_level": 10,
                     "min_stats": {"STR": 14, "CON": 14},
                     "description": "Armored protector channeling ki to defend allies."},
    # Mage hybrids
    "Witch":        {"base_classes": ["Mage", "Cleric"],     "min_level": 10,
                     "min_stats": {"INT": 14, "PIE": 12, "WIS": 14},
                     "description": "Dark spellcaster blending arcane and divine powers."},
    "Necromancer":  {"base_classes": ["Mage", "Thief"],      "min_level": 10,
                     "min_stats": {"INT": 16, "WIS": 12},
                     "description": "Master of death magic, draining life and raising the fallen."},
    "Druid":        {"base_classes": ["Mage", "Ranger"],     "min_level": 10,
                     "min_stats": {"INT": 12, "WIS": 16},
                     "description": "Nature spellcaster harnessing elemental and healing powers."},
    "Mystic":       {"base_classes": ["Mage", "Monk"],       "min_level": 10,
                     "min_stats": {"INT": 14, "WIS": 12},
                     "description": "Arcane ki master fusing magical theory with inner discipline."},
    # Cleric hybrids
    "Warden":       {"base_classes": ["Cleric", "Ranger"],   "min_level": 10,
                     "min_stats": {"PIE": 12, "WIS": 14},
                     "description": "Ancient guardian combining divine protection and nature's power."},
    "Inquisitor":   {"base_classes": ["Cleric", "Thief"],    "min_level": 10,
                     "min_stats": {"PIE": 14, "DEX": 12},
                     "description": "Shadow-wielding divine agent who hunts the corrupt."},
    "Templar":      {"base_classes": ["Cleric", "Monk"],     "min_level": 10,
                     "min_stats": {"PIE": 12, "CON": 14},
                     "description": "Devoted warrior combining divine faith and physical discipline."},
    # Thief/Ranger hybrids
    "Assassin":     {"base_classes": ["Ranger", "Thief"],    "min_level": 10,
                     "min_stats": {"DEX": 16, "WIS": 10},
                     "description": "Lethal hunter combining tracking, poisons, and shadow strikes."},
    "Shaman":       {"base_classes": ["Ranger", "Monk"],     "min_level": 10,
                     "min_stats": {"WIS": 14, "CON": 12},
                     "description": "Wilderness spiritualist drawing ki from the natural world."},

    # ── APEX CLASSES (level 15, pure-line) ───────────────────────────────────
    # One base class perfected. Requires reaching level 15 in that lineage.
    "Warder":       None,  # placeholder — see above (Warder is also a hybrid)
    "Archmage":     {"base_classes": ["Mage"],        "min_level": 15,
                     "min_stats": {"INT": 20, "WIS": 16},
                     "description": "Master of all arcane disciplines. Reality bends to their will."},
    "High Priest":  {"base_classes": ["Cleric"],      "min_level": 15,
                     "min_stats": {"PIE": 20, "WIS": 18},
                     "description": "Divine conduit of staggering power. Miracles are within reach."},
    "Shadow Master":{"base_classes": ["Thief"],       "min_level": 15,
                     "min_stats": {"DEX": 20, "WIS": 14},
                     "description": "Absolute master of shadow. Death comes from darkness unseen."},
    "Beastlord":    {"base_classes": ["Ranger"],      "min_level": 15,
                     "min_stats": {"DEX": 18, "WIS": 18},
                     "description": "One with the wild. Commands nature and hunts with primal fury."},
}
# Remove None placeholders
CLASS_TRANSITIONS = {k: v for k, v in CLASS_TRANSITIONS.items() if v is not None}


def get_available_transitions(character):
    """Return list of class names this character can transition to."""
    available = []
    for cls_name, req in CLASS_TRANSITIONS.items():
        if cls_name == character.class_name:
            continue
        # Must be from a valid base class
        if character.class_name not in req.get("base_classes", []):
            continue
        # Must meet minimum level
        if character.level < req.get("min_level", 1):
            continue
        # Must meet stat minimums
        if all(character.stats.get(stat, 0) >= minimum
               for stat, minimum in req.get("min_stats", {}).items()):
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

    # Report newly trainable abilities (available to purchase at guild)
    from core.abilities import CLASS_ABILITIES
    class_abilities = CLASS_ABILITIES.get(cls, [])
    known_names = {a["name"] for a in character.abilities}
    new_abilities = []

    for ab in class_abilities:
        if ab["name"] not in known_names and ab.get("level", 1) <= new_level:
            # All abilities are freely trainable at the guild — no branches
            new_abilities.append(ab["name"])
    summary["new_abilities"] = new_abilities   # available to train, not yet learned
    summary["branch_choice"] = None            # branches removed

    return summary


# ═══════════════════════════════════════════════════════════════
#  PLANAR ASCENSION TIERS  (Bronze → Iron → Steel → Mithril → Adamantine)
# ═══════════════════════════════════════════════════════════════
# A separate prestige track unlocked by story milestones.
# Each tier grants a passive bonus applied in combat and shown in the party screen.
# Characters advance together — tier is checked from story flags, not stored per-char.

PLANAR_TIERS = {
    # ── In-Game 1 Warden Ranks ────────────────────────────────────────────────
    # These are Warden Order designations tied to Hearthstone recovery.
    # NOTE: "Bronze / Iron / Steel" are reserved for the cosmological tier system
    # spanning Games 1-3 (per GAME_BIBLE). These in-world ranks are separate.
    0: {
        "name":   "Initiate",
        "color":  (160, 140, 100),    # worn leather
        "symbol": "◆",
        "bonus":  {},                  # no bonus at starting rank
        "description": "You have answered the Warden call. The first step of many.",
        "unlock_flag": None,           # everyone starts here
    },
    1: {
        "name":   "Scout",
        "color":  (160, 175, 190),    # field grey
        "symbol": "◆",
        "bonus":  {"all_stats": 1, "xp_mult": 1.05},
        "description": "Tested by the first trials. +1 all stats, +5% XP.",
        "unlock_flag": "item.hearthstone.1",        # first Hearthstone (Abandoned Mine)
        "min_level": 5,
    },
    2: {
        "name":   "Warden",
        "color":  (100, 160, 120),    # Warden green
        "symbol": "◆",
        "bonus":  {"all_stats": 2, "max_hp_pct": 0.05, "xp_mult": 1.10},
        "description": "A proven Warden. +2 all stats, +5% max HP, +10% XP.",
        "unlock_flag": "item.hearthstone.3",        # third Hearthstone (Dragon's Tooth)
        "min_level": 10,
    },
    3: {
        "name":   "Senior Warden",
        "color":  (140, 200, 170),    # elder green-silver
        "symbol": "◆",
        "bonus":  {"all_stats": 4, "max_hp_pct": 0.10, "damage_mult": 1.05, "xp_mult": 1.15},
        "description": "Keeper of the deeper wards. +4 all stats, +10% HP, +5% damage, +15% XP.",
        "unlock_flag": "item.hearthstone.5",        # fifth (final) Hearthstone
        "min_level": 13,
    },
    4: {
        "name":   "Warden-Commander",
        "color":  (180, 220, 200),    # bright silver-green
        "symbol": "◆",
        "bonus":  {"all_stats": 6, "max_hp_pct": 0.15, "damage_mult": 1.10, "xp_mult": 1.25},
        "description": "The highest rank of the mortal order. +6 all stats, +15% HP, +10% damage.",
        "unlock_flag": "boss_defeated.shadow_valdris",  # endgame
        "min_level": 15,
    },
}

TIER_ORDER = [0, 1, 2, 3, 4]


def get_party_tier(story_flags: dict, min_level: int = 1) -> int:
    """Return the highest tier index the party has earned based on story flags and level."""
    best = 0
    for tier_idx in TIER_ORDER:
        t = PLANAR_TIERS[tier_idx]
        flag = t.get("unlock_flag")
        req_level = t.get("min_level", 1)
        if flag is None:
            continue  # tier 0 is always available
        if story_flags.get(flag) and min_level >= req_level:
            best = tier_idx
    return best


def get_tier_bonus(tier_idx: int) -> dict:
    """Return the bonus dict for the given tier."""
    return PLANAR_TIERS.get(tier_idx, PLANAR_TIERS[0])["bonus"]


def apply_tier_stat_bonus(character, tier_idx: int):
    """Apply a tier's all_stats bonus to a character's stat dict (additive, no double-apply).
    Call this only during resource recalculation, not persistently on the stored stats."""
    bonus = get_tier_bonus(tier_idx)
    flat = bonus.get("all_stats", 0)
    if flat:
        return {s: character.stats.get(s, 0) + flat for s in character.stats}
    return dict(character.stats)


def get_tier_max_hp_mult(tier_idx: int) -> float:
    """Return the max-HP multiplier for the given tier (1.0 = no bonus)."""
    return 1.0 + PLANAR_TIERS.get(tier_idx, {}).get("bonus", {}).get("max_hp_pct", 0.0)


def get_tier_damage_mult(tier_idx: int) -> float:
    """Return the damage multiplier for the given tier (1.0 = no bonus)."""
    return PLANAR_TIERS.get(tier_idx, {}).get("bonus", {}).get("damage_mult", 1.0)


def get_tier_xp_mult(tier_idx: int) -> float:
    """Return the XP gain multiplier for the given tier."""
    return PLANAR_TIERS.get(tier_idx, {}).get("bonus", {}).get("xp_mult", 1.0)


def auto_advance_party_tier(party: list, story_flags: dict) -> list:
    """Check if any character's tier should advance. Returns list of (char, old_tier, new_tier) tuples."""
    if not party:
        return []
    min_level = min(c.level for c in party)
    new_tier = get_party_tier(story_flags, min_level)
    advanced = []
    for char in party:
        old = getattr(char, "planar_tier", 0)
        if new_tier > old:
            char.planar_tier = new_tier
            advanced.append((char, old, new_tier))
    return advanced


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
    """No trickle regen — resources only restored at camp, inn, or via spells/potions."""
    pass


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


# ═══════════════════════════════════════════════════════════════
#  TRAINING BOOK SYSTEM
# ═══════════════════════════════════════════════════════════════

# Track which books a character has already benefited from
# (stored as a set on character: character.books_read)
VALID_TRAINING_STATS = {"STR", "DEX", "CON", "INT", "WIS", "PIE"}

def use_training_book(character, item):
    """Apply a training book's stat increase to a character.
    Returns (success, message).
    - Consumed on use regardless of outcome.
    - Each unique book title can only benefit a character once.
    - Stat cap: training books cannot raise a stat above 25.
    """
    if item.get("subtype") != "training_book":
        return False, "This isn't a training book."

    book_name = item.get("name", "Unknown")
    stat = item.get("trains_stat", "")
    amount = item.get("trains_amount", 1)

    if stat not in VALID_TRAINING_STATS:
        return False, f"Unknown stat '{stat}' in training book."

    # Initialize books_read set if needed
    if not hasattr(character, "books_read"):
        character.books_read = set()

    if book_name in character.books_read:
        return False, (f"{character.name} has already absorbed the lessons of "
                       f"'{book_name}'. There is nothing more to gain from it.")

    # Stat cap
    current_val = character.stats.get(stat, 0)
    TRAINING_BOOK_CAP = 25
    if current_val >= TRAINING_BOOK_CAP:
        return False, (f"{character.name}'s {stat} is already at the limit "
                       f"that training alone can reach ({TRAINING_BOOK_CAP}).")

    # Apply the increase
    actual_gain = min(amount, TRAINING_BOOK_CAP - current_val)
    character.stats[stat] = current_val + actual_gain

    character.books_read.add(book_name)

    use_msg = item.get("use_message", f"+{actual_gain} {stat}.")
    return True, f"{character.name}: {use_msg} ({stat} +{actual_gain})"


# ═══════════════════════════════════════════════════════════════
#  CLASS TRANSITION
# ═══════════════════════════════════════════════════════════════

def apply_class_transition(character, new_class_name: str) -> tuple:
    """Apply a mid-game class transition (Wizardry-style with catch-up XP).

    - Must meet stat_req for new class
    - Keeps top 3 highest-level mastered abilities from old class
    - Level resets to 1; XP +60% until former level re-reached
    - Stats preserved; resources recalculated for new class
    Returns (success: bool, message: str).
    """
    from core.classes import CLASSES, get_all_resources
    from core.abilities import CLASS_ABILITIES

    req = CLASS_TRANSITIONS.get(new_class_name)
    if not req:
        return False, f"Unknown class: {new_class_name}"

    if character.class_name == new_class_name:
        return False, f"{character.name} is already a {new_class_name}."

    stat_req = req.get("stat_req", {})
    for stat, minimum in stat_req.items():
        if character.stats.get(stat, 0) < minimum:
            return False, (
                f"Requires {stat} {minimum} "
                f"(you have {character.stats.get(stat, 0)}, need {minimum - character.stats.get(stat, 0)} more)."
            )

    old_class = character.class_name
    old_level = character.level

    # Keep top 3 highest-level mastered abilities (not passives)
    sorted_abs = sorted(character.abilities, key=lambda a: a.get("level", 0), reverse=True)
    kept, kept_names = [], set()
    for ab in sorted_abs:
        if ab.get("type") == "passive":
            continue
        if ab["name"] not in kept_names and len(kept) < 3:
            kept.append(dict(ab))
            kept_names.add(ab["name"])

    # New class L1 abilities
    new_l1 = [a for a in CLASS_ABILITIES.get(new_class_name, []) if a.get("level", 1) <= 1]
    new_abilities = kept[:]
    for ab in new_l1:
        if ab["name"] not in kept_names:
            new_abilities.append(dict(ab))

    # Apply transition
    character.class_name               = new_class_name
    character.abilities                = new_abilities
    character.level                    = 1
    character.xp                       = 0
    character._catchup_target_level    = old_level   # XP boost window
    character._catchup_xp_mult         = 1.60        # +60% XP until target level

    # Recalculate resources for new class at level 1
    new_max = get_all_resources(new_class_name, character.stats, 1)
    character.resources = dict(new_max)

    kept_str = ", ".join(a["name"] for a in kept) if kept else "none"
    return True, (
        f"{character.name} transitions to {new_class_name} (was {old_class} level {old_level}). "
        f"Mastered abilities kept: {kept_str}. "
        f"XP +60%% until level {old_level} reached again."
    )
