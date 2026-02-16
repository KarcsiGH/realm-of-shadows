"""
Realm of Shadows — Combat Configuration
All formulas, constants, and tuning values in one centralized file.
Change a number here → combat changes everywhere.

References: Combat_System_Design_v3.md, Weapon_System_Design_v2.md,
            Elemental_Enchantment_System_Design_v1.md
"""

# ═══════════════════════════════════════════════════════════════
#  SPEED & TURN ORDER
# ═══════════════════════════════════════════════════════════════

def calc_speed(stats, level, equipment_bonus=0):
    """Speed = (DEX × 2) + (WIS × 0.5) + Level + Equipment Bonus"""
    return (stats["DEX"] * 2) + (stats["WIS"] * 0.5) + level + equipment_bonus


# Speed modifier multipliers for status effects
SPEED_MODIFIERS = {
    "Hasted":       1.50,   # +50%
    "Slowed":       0.75,   # -25%
    "Frostbitten":  0.50,   # -50%
    "Stunned":      0.0,    # skip turn
    "Frozen":       0.0,    # skip turn
    "Petrified":    0.0,    # skip turn
}


# ═══════════════════════════════════════════════════════════════
#  ACCURACY
# ═══════════════════════════════════════════════════════════════

ACCURACY_BASE_PHYSICAL  = 75  # %
ACCURACY_BASE_MAGIC     = 80  # %
ACCURACY_MIN            = 30  # % floor
ACCURACY_MAX            = 95  # % ceiling
ACCURACY_DEX_SCALE      = 2   # % per point of DEX difference
ACCURACY_STAT_SCALE     = 2   # % per point of casting stat vs WIS

# Status penalties to accuracy
ACCURACY_STATUS_PENALTIES = {
    "Burning":      -5,
    "Poisoned":     -5,
    "Frostbitten":  -5,
    "Shocked":      -10,
    "Blinded":      -30,
}


# ═══════════════════════════════════════════════════════════════
#  DAMAGE FORMULAS
# ═══════════════════════════════════════════════════════════════

DAMAGE_VARIANCE_MIN     = 0.85
DAMAGE_VARIANCE_MAX     = 1.15
MAGIC_VARIANCE_MIN      = 0.90
MAGIC_VARIANCE_MAX      = 1.10
MINIMUM_DAMAGE          = 1

# Magic stat multiplier: Stat Damage = Casting Stat × MAGIC_STAT_MULT
MAGIC_STAT_MULT         = 1.5

# Healing formula: (PIE × HEAL_PIE_MULT) + Spell Power + Focus + random(0, PIE/2)
HEAL_PIE_MULT           = 2.0


# ═══════════════════════════════════════════════════════════════
#  CRITICAL HITS
# ═══════════════════════════════════════════════════════════════

CRIT_BASE_CHANCE        = 5    # % base for all crits

# Precision crit (Thief, Ranger, Monk)
CRIT_PRECISION_SCALE    = 8    # DEX / this = bonus %
CRIT_PRECISION_MULT     = 1.5  # damage multiplier (2.0 for Assassin)
CRIT_PRECISION_CLASSES  = {"Thief": 2.0, "Assassin": 2.0}  # overrides

# Power crit (Fighter)
CRIT_POWER_SCALE        = 10   # STR / this = bonus %
CRIT_POWER_MULT         = 1.5  # multiplier, but ignores 50% defense
CRIT_POWER_DEF_IGNORE   = 0.50

# Ki crit (Monk)
CRIT_KI_SCALE           = 8    # WIS / this
CRIT_KI_MULT            = 1.75

# Spell crit
CRIT_SPELL_SCALE        = 10   # Casting stat / this
CRIT_SPELL_MULT         = 1.5

# Heal crit
CRIT_HEAL_SCALE         = 10   # PIE / this
CRIT_HEAL_MULT          = 1.5

# Weapon crit bonuses
CRIT_WEAPON_BONUS = {
    "Dagger":       5,   # piercing weapons +5%
    "Short Sword":  3,
    "Bow":          3,
    "Broadsword":   2,   # heavy weapons +2%
    "Mace":         2,
}


# ═══════════════════════════════════════════════════════════════
#  DEFENSE & RESISTANCE
# ═══════════════════════════════════════════════════════════════

# Physical Defense = (CON × DEF_CON_MULT) + Armor + Shield + Buffs
DEF_CON_MULT            = 0.5

# Magic Resistance = (WIS × MRES_WIS_MULT) + Equipment + Buffs
MRES_WIS_MULT           = 0.5

# Defend action bonuses
DEFEND_PHYS_MULT        = 1.5   # defense × this
DEFEND_MAGIC_MULT       = 1.25  # magic resist × this
DEFEND_ACC_PENALTY      = -15   # enemy accuracy penalty


# ═══════════════════════════════════════════════════════════════
#  POSITION-TO-POSITION MODIFIERS
#  Key: (attacker_row, defender_row) → (damage_mod, accuracy_mod)
# ═══════════════════════════════════════════════════════════════

# Row constants
FRONT = "front"
MID   = "mid"
BACK  = "back"

ROWS = [FRONT, MID, BACK]

# Standard Melee (swords, daggers, maces, fists)
POS_MELEE = {
    (FRONT, FRONT): (1.00,   0),
    (FRONT, MID):   (0.90,  -5),
    (MID,   FRONT): (0.85,  -5),
    (MID,   MID):   (0.80, -10),
    (BACK,  FRONT): (0.70, -15),
    (MID,   BACK):  (0.65, -15),
    (BACK,  MID):   (0.55, -20),
    (BACK,  BACK):  (0.40, -25),
    # Missing combos default to worst
    (FRONT, BACK):  (0.65, -15),
}

# Reach Melee (spears, polearms, halberds)
POS_REACH = {
    (MID,   FRONT): (1.00,   5),
    (MID,   MID):   (0.95,   0),
    (FRONT, FRONT): (0.85,  -5),
    (FRONT, MID):   (0.90,   0),
    (MID,   BACK):  (0.80,  -5),
    (BACK,  FRONT): (0.75, -10),
    (FRONT, BACK):  (0.70, -10),
    (BACK,  MID):   (0.60, -15),
    (BACK,  BACK):  (0.45, -20),
}

# Ranged (bows, crossbows, slings)
POS_RANGED = {
    (MID,   FRONT): (1.00,   5),
    (MID,   MID):   (0.95,   0),
    (BACK,  FRONT): (0.95,   0),
    (MID,   BACK):  (0.85,  -5),
    (BACK,  MID):   (0.85,  -5),
    (FRONT, MID):   (0.75, -10),
    (FRONT, BACK):  (0.70, -10),
    (BACK,  BACK):  (0.70, -15),
    (FRONT, FRONT): (0.60, -20),
}

# Crossbow overrides at extremes
POS_CROSSBOW_OVERRIDES = {
    (FRONT, FRONT): (0.70, -15),
    (BACK,  BACK):  (0.75, -10),
}

# Thrown weapons
POS_THROWN = {
    (FRONT, FRONT): (1.00,   5),
    (FRONT, MID):   (0.95,   0),
    (MID,   FRONT): (0.90,   0),
    (MID,   MID):   (0.85,  -5),
    (FRONT, BACK):  (0.75, -10),
    (BACK,  FRONT): (0.70, -10),
    (MID,   BACK):  (0.65, -15),
    (BACK,  MID):   (0.60, -15),
    (BACK,  BACK):  (0.50, -20),
}


def get_position_mods(weapon_range, attacker_row, defender_row, is_crossbow=False):
    """Look up (damage_mult, accuracy_mod) for a position-to-position attack."""
    key = (attacker_row, defender_row)

    if weapon_range == "spell":
        return (1.0, 0)  # spells ignore position

    if weapon_range == "melee":
        table = POS_MELEE
    elif weapon_range == "reach":
        table = POS_REACH
    elif weapon_range == "ranged":
        table = POS_RANGED
        if is_crossbow and key in POS_CROSSBOW_OVERRIDES:
            return POS_CROSSBOW_OVERRIDES[key]
    elif weapon_range == "thrown":
        table = POS_THROWN
    else:
        return (1.0, 0)

    return table.get(key, (0.50, -20))  # fallback for unmapped combos


# ═══════════════════════════════════════════════════════════════
#  PHYSICAL DAMAGE SUBTYPES & RESISTANCES
# ═══════════════════════════════════════════════════════════════

# Resistance multipliers
IMMUNE          = 0.0
RESISTANT       = 0.5
NEUTRAL         = 1.0
VULNERABLE      = 1.5
VERY_VULNERABLE = 2.0


# ═══════════════════════════════════════════════════════════════
#  RESOURCE REGENERATION IN COMBAT
# ═══════════════════════════════════════════════════════════════

# Per turn: +(Relevant Stat / REGEN_STAT_DIV) + REGEN_PERCENT of max
REGEN_STAT_DIV      = 4
REGEN_PERCENT       = 0.03    # 3% of max
MONK_REGEN_PERCENT  = 0.0375  # 3.75% for monks (25% bonus)

# HP does NOT regenerate in combat


# ═══════════════════════════════════════════════════════════════
#  POTION DIMINISHING RETURNS
# ═══════════════════════════════════════════════════════════════

POTION_DIMINISH = [1.00, 0.75, 0.56, 0.42, 0.32]


# ═══════════════════════════════════════════════════════════════
#  MACE ARMOR BYPASS
# ═══════════════════════════════════════════════════════════════

MACE_ARMOR_BYPASS = 0.30  # maces ignore 30% of defense


# ═══════════════════════════════════════════════════════════════
#  STATUS EFFECT TICK DAMAGE (end of round)
# ═══════════════════════════════════════════════════════════════

# Status effects that deal damage each round.
# Value is flat damage per tick.  Tunable here.
STATUS_TICK_DAMAGE = {
    "Poisoned":     4,
    "Burning":      6,
    "Frostbitten":  3,
    "Shocked":      5,
}

# Status effects that prevent action (Speed = 0 handles skipping,
# these are listed for the tick system to decrement duration only)
STATUS_INCAPACITATE = {"Stunned", "Frozen", "Petrified", "Sleep"}

# All statuses that should tick down each round
STATUS_DURATION_TICK = (
    set(STATUS_TICK_DAMAGE.keys())
    | STATUS_INCAPACITATE
    | {"Blinded", "Fear", "Silenced", "Slowed", "Hasted"}
)


# ═══════════════════════════════════════════════════════════════
#  ENEMY AI — THREAT ASSESSMENT
# ═══════════════════════════════════════════════════════════════

# Threat rating by class archetype.  Higher = scarier to enemies.
# Used by tactical/boss AI to pick targets intelligently.
CLASS_THREAT = {
    # Healers are top priority — they undo your work
    "Cleric": 10,
    # Big damage casters next
    "Mage":   9,
    # Hybrid ranged/magic
    "Ranger": 6,
    # Melee damage dealers
    "Thief":  5,
    "Monk":   5,
    "Fighter": 4,
}
CLASS_THREAT_DEFAULT = 4

# Buff/debuff durations applied by enemy abilities
ENEMY_BUFF_DURATION = 3   # rounds for War Cry etc.
ENEMY_BUFF_DMG_MULT = 1.2  # War Cry damage multiplier
