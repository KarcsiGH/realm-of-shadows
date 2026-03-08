"""
Realm of Shadows — Weapon Data
All weapon definitions from Weapon_System_Design_v2.md.
Adding a new weapon = adding a dict here. No code changes needed.
"""

# ═══════════════════════════════════════════════════════════════
#  WEAPON DEFINITIONS
# ═══════════════════════════════════════════════════════════════
#
#  Each weapon has:
#    name          - display name
#    type          - category key (for proficiency lookup)
#    damage        - base damage value
#    damage_stat   - dict of {stat: weight} for damage formula
#    range         - "melee", "reach", "ranged", "thrown"
#    speed_mod     - modifier to turn order
#    accuracy_mod  - bonus/penalty to hit chance (%)
#    crit_mod      - bonus to critical hit chance (%)
#    weight_class  - "light", "medium", "heavy"
#    phys_type     - "piercing", "slashing", "blunt"
#    requirements  - dict of {stat: min_value} or {}
#    spell_bonus   - bonus to spell damage (staves only)
#    special       - dict of extra properties (armor_bypass, etc.)

WEAPONS = {
    # ── FISTS / UNARMED ─────────────────────────────────────
    "Unarmed": {
        "name": "Unarmed", "type": "Fists",
        "damage": 2, "damage_stat": {"STR": 0.5, "DEX": 0.5},
        "range": "melee", "speed_mod": 2, "accuracy_mod": 5, "crit_mod": 0,
        "weight_class": "light", "phys_type": "blunt",
        "requirements": {}, "spell_bonus": 0, "special": {},
    },
    "Monk Unarmed": {
        "name": "Unarmed (Monk)", "type": "Fists",
        "damage": 2, "damage_stat": {"STR": 0.5, "DEX": 0.5},
        "range": "melee", "speed_mod": 2, "accuracy_mod": 5, "crit_mod": 0,
        "weight_class": "light", "phys_type": "blunt",
        "requirements": {}, "spell_bonus": 0,
        "special": {"monk_scaling": True},  # damage = 3 + level * 2
    },

    # ── DAGGERS ──────────────────────────────────────────────
    "Rusty Knife": {
        "name": "Rusty Knife", "type": "Dagger",
        "damage": 5, "damage_stat": {"DEX": 1.0},
        "range": "melee", "speed_mod": 2, "accuracy_mod": 5, "crit_mod": 5,
        "weight_class": "light", "phys_type": "piercing",
        "requirements": {}, "spell_bonus": 0, "special": {},
    },
    "Iron Dagger": {
        "name": "Iron Dagger", "type": "Dagger",
        "damage": 7, "damage_stat": {"DEX": 1.0},
        "range": "melee", "speed_mod": 2, "accuracy_mod": 5, "crit_mod": 5,
        "weight_class": "light", "phys_type": "piercing",
        "requirements": {"DEX": 8}, "spell_bonus": 0, "special": {},
    },

    # ── SHORT SWORDS ─────────────────────────────────────────
    "Worn Short Sword": {
        "name": "Worn Short Sword", "type": "Short Sword",
        "damage": 6, "damage_stat": {"DEX": 0.7, "STR": 0.3},
        "range": "melee", "speed_mod": 1, "accuracy_mod": 0, "crit_mod": 0,
        "weight_class": "light", "phys_type": "slashing",
        "requirements": {"DEX": 8}, "spell_bonus": 0, "special": {},
    },
    "Iron Short Sword": {
        "name": "Iron Short Sword", "type": "Short Sword",
        "damage": 8, "damage_stat": {"DEX": 0.7, "STR": 0.3},
        "range": "melee", "speed_mod": 1, "accuracy_mod": 0, "crit_mod": 0,
        "weight_class": "light", "phys_type": "slashing",
        "requirements": {"DEX": 10}, "spell_bonus": 0, "special": {},
    },

    # ── LONGSWORDS ───────────────────────────────────────────
    "Worn Longsword": {
        "name": "Worn Longsword", "type": "Longsword",
        "damage": 8, "damage_stat": {"STR": 0.7, "DEX": 0.3},
        "range": "melee", "speed_mod": 0, "accuracy_mod": 0, "crit_mod": 0,
        "weight_class": "medium", "phys_type": "slashing",
        "requirements": {"STR": 10}, "spell_bonus": 0, "special": {},
    },
    "Iron Longsword": {
        "name": "Iron Longsword", "type": "Longsword",
        "damage": 10, "damage_stat": {"STR": 0.7, "DEX": 0.3},
        "range": "melee", "speed_mod": 0, "accuracy_mod": 0, "crit_mod": 0,
        "weight_class": "medium", "phys_type": "slashing",
        "requirements": {"STR": 12}, "spell_bonus": 0, "special": {},
    },

    # ── BROADSWORDS ──────────────────────────────────────────
    "Iron Broadsword": {
        "name": "Iron Broadsword", "type": "Broadsword",
        "damage": 12, "damage_stat": {"STR": 1.0},
        "range": "melee", "speed_mod": -2, "accuracy_mod": -5, "crit_mod": 2,
        "weight_class": "heavy", "phys_type": "slashing",
        "requirements": {"STR": 13}, "spell_bonus": 0, "special": {},
    },

    # ── MACES / HAMMERS ──────────────────────────────────────
    "Wooden Club": {
        "name": "Wooden Club", "type": "Mace",
        "damage": 6, "damage_stat": {"STR": 1.0},
        "range": "melee", "speed_mod": -1, "accuracy_mod": -5, "crit_mod": 2,
        "weight_class": "medium", "phys_type": "blunt",
        "requirements": {"STR": 8}, "spell_bonus": 0,
        "special": {"armor_bypass": 0.30},
    },
    "Iron Mace": {
        "name": "Iron Mace", "type": "Mace",
        "damage": 9, "damage_stat": {"STR": 1.0},
        "range": "melee", "speed_mod": -1, "accuracy_mod": -5, "crit_mod": 2,
        "weight_class": "medium", "phys_type": "blunt",
        "requirements": {"STR": 11}, "spell_bonus": 0,
        "special": {"armor_bypass": 0.30},
    },

    # ── STAVES ───────────────────────────────────────────────
    "Walking Stick": {
        "name": "Walking Stick", "type": "Staff",
        "damage": 3, "damage_stat": {"STR": 0.4, "INT": 0.6},
        "range": "melee", "speed_mod": 0, "accuracy_mod": 0, "crit_mod": 0,
        "weight_class": "medium", "phys_type": "blunt",
        "requirements": {}, "spell_bonus": 2, "special": {},
    },
    "Wooden Staff": {
        "name": "Wooden Staff", "type": "Staff",
        "damage": 5, "damage_stat": {"STR": 0.4, "INT": 0.6},
        "range": "melee", "speed_mod": 0, "accuracy_mod": 0, "crit_mod": 0,
        "weight_class": "medium", "phys_type": "blunt",
        "requirements": {"INT": 8}, "spell_bonus": 4, "special": {},
    },
    "Sacred Staff": {
        "name": "Sacred Staff", "type": "Staff",
        "damage": 7, "damage_stat": {"STR": 0.4, "WIS": 0.6},
        "range": "melee", "speed_mod": 0, "accuracy_mod": 0, "crit_mod": 0,
        "weight_class": "medium", "phys_type": "blunt",
        "requirements": {"PIE": 12}, "spell_bonus": 8, "special": {},
    },

    # ── SPEARS ───────────────────────────────────────────────
    "Wooden Spear": {
        "name": "Wooden Spear", "type": "Spear",
        "damage": 7, "damage_stat": {"STR": 0.6, "DEX": 0.4},
        "range": "reach", "speed_mod": 0, "accuracy_mod": 5, "crit_mod": 0,
        "weight_class": "medium", "phys_type": "piercing",
        "requirements": {"STR": 9}, "spell_bonus": 0, "special": {},
    },
    "Iron Spear": {
        "name": "Iron Spear", "type": "Spear",
        "damage": 9, "damage_stat": {"STR": 0.6, "DEX": 0.4},
        "range": "reach", "speed_mod": 0, "accuracy_mod": 5, "crit_mod": 0,
        "weight_class": "medium", "phys_type": "piercing",
        "requirements": {"STR": 11, "DEX": 9}, "spell_bonus": 0, "special": {},
    },

    # ── SLINGS ───────────────────────────────────────────────
    "Simple Sling": {
        "name": "Simple Sling", "type": "Sling",
        "damage": 4, "damage_stat": {"DEX": 1.0},
        "range": "ranged", "speed_mod": 0, "accuracy_mod": -5, "crit_mod": 0,
        "weight_class": "light", "phys_type": "blunt",
        "requirements": {"DEX": 8}, "spell_bonus": 0, "special": {},
    },

    # ── BOWS ─────────────────────────────────────────────────
    "Short Bow": {
        "name": "Short Bow", "type": "Bow",
        "damage": 7, "damage_stat": {"DEX": 0.8, "STR": 0.2},
        "range": "ranged", "speed_mod": 0, "accuracy_mod": 5, "crit_mod": 3,
        "weight_class": "medium", "phys_type": "piercing",
        "requirements": {"DEX": 10, "STR": 8}, "spell_bonus": 0, "special": {},
    },
    "Hunting Bow": {
        "name": "Hunting Bow", "type": "Bow",
        "damage": 9, "damage_stat": {"DEX": 0.8, "STR": 0.2},
        "range": "ranged", "speed_mod": 0, "accuracy_mod": 5, "crit_mod": 3,
        "weight_class": "medium", "phys_type": "piercing",
        "requirements": {"DEX": 12, "STR": 9}, "spell_bonus": 0, "special": {},
    },

    # ── CROSSBOWS ────────────────────────────────────────────
    "Light Crossbow": {
        "name": "Light Crossbow", "type": "Crossbow",
        "damage": 11, "damage_stat": {"DEX": 0.2},  # mostly flat damage
        "range": "ranged", "speed_mod": -3, "accuracy_mod": 10, "crit_mod": 0,
        "weight_class": "medium", "phys_type": "piercing",
        "requirements": {"DEX": 8}, "spell_bonus": 0,
        "special": {"is_crossbow": True},
    },

    # ── THROWN ────────────────────────────────────────────────
    "Throwing Knife": {
        "name": "Throwing Knife", "type": "Thrown",
        "damage": 5, "damage_stat": {"DEX": 0.6, "STR": 0.4},
        "range": "thrown", "speed_mod": 1, "accuracy_mod": 0, "crit_mod": 0,
        "weight_class": "light", "phys_type": "piercing",
        "requirements": {"DEX": 10}, "spell_bonus": 0, "special": {},
    },
    "Throwing Axe": {
        "name": "Throwing Axe", "type": "Thrown",
        "damage": 8, "damage_stat": {"DEX": 0.6, "STR": 0.4},
        "range": "thrown", "speed_mod": 1, "accuracy_mod": 0, "crit_mod": 0,
        "weight_class": "light", "phys_type": "slashing",
        "requirements": {"DEX": 11, "STR": 10}, "spell_bonus": 0, "special": {},
    },
}


# ═══════════════════════════════════════════════════════════════
#  CLASS WEAPON PROFICIENCIES
# ═══════════════════════════════════════════════════════════════

CLASS_PROFICIENCIES = {
    "Fighter": ["Fists", "Dagger", "Short Sword", "Longsword", "Broadsword",
                "Mace", "Spear", "Crossbow", "Thrown"],
    "Mage":    ["Fists", "Dagger", "Staff", "Sling"],
    "Cleric":  ["Fists", "Mace", "Staff", "Sling"],
    "Thief":   ["Fists", "Dagger", "Short Sword", "Sling", "Bow", "Thrown"],
    "Ranger":  ["Fists", "Dagger", "Short Sword", "Longsword", "Staff",
                "Spear", "Bow", "Crossbow", "Thrown"],
    "Monk":    ["Fists", "Staff", "Spear"],
}

# Penalty for using non-proficient weapon
NON_PROFICIENT_DAMAGE_MULT  = 0.80   # -20%
NON_PROFICIENT_ACCURACY     = -15    # -15%
NON_PROFICIENT_SPEED        = -2


# ═══════════════════════════════════════════════════════════════
#  STARTING WEAPONS BY CLASS
# ═══════════════════════════════════════════════════════════════

STARTING_WEAPONS = {
    "Fighter": "Worn Longsword",
    "Mage":    "Walking Stick",
    "Cleric":  "Wooden Club",
    "Thief":   "Rusty Knife",
    "Ranger":  "Short Bow",
    "Monk":    "Monk Unarmed",
}

STARTING_BACKUP_WEAPONS = {
    "Mage":   "Simple Sling",
    "Cleric": "Simple Sling",
    "Thief":  "Simple Sling",
    "Ranger": "Worn Short Sword",
}


def get_weapon(weapon_key):
    """Get weapon data by key. Returns a copy."""
    if weapon_key in WEAPONS:
        return dict(WEAPONS[weapon_key])
    return dict(WEAPONS["Unarmed"])


def is_proficient(class_name, weapon_type):
    """Check if a class is proficient with a weapon type."""
    return weapon_type in CLASS_PROFICIENCIES.get(class_name, [])
