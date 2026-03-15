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
        "damage": 9, "damage_stat": {"STR": 0.2, "DEX": 0.2},
        "range": "melee", "speed_mod": 2, "accuracy_mod": 5, "crit_mod": 0,
        "weight_class": "light", "phys_type": "blunt",
        "requirements": {}, "spell_bonus": 0, "special": {},
    },
    "Monk Unarmed": {
        "name": "Unarmed (Monk)", "type": "Fists",
        "damage": 9, "damage_stat": {"WIS": 0.30, "DEX": 0.20},
        "range": "melee", "speed_mod": 2, "accuracy_mod": 5, "crit_mod": 5,
        "weight_class": "light", "phys_type": "blunt",
        "requirements": {}, "spell_bonus": 0,
        "special": {"monk_scaling": True},  # damage = 4 + level * 2
    },

    # ── DAGGERS ──────────────────────────────────────────────
    "Rusty Knife": {
        "name": "Rusty Knife", "type": "Dagger",
        "damage": 12, "damage_stat": {"DEX": 0.4},
        "range": "melee", "speed_mod": 2, "accuracy_mod": 5, "crit_mod": 5,
        "weight_class": "light", "phys_type": "piercing",
        "requirements": {}, "spell_bonus": 0, "special": {},
    },
    "Iron Dagger": {
        "name": "Iron Dagger", "type": "Dagger",
        "damage": 14, "damage_stat": {"DEX": 0.4},
        "range": "melee", "speed_mod": 2, "accuracy_mod": 5, "crit_mod": 5,
        "weight_class": "light", "phys_type": "piercing",
        "requirements": {"DEX": 8}, "spell_bonus": 0, "special": {},
    },

    # ── SHORT SWORDS ─────────────────────────────────────────
    "Worn Short Sword": {
        "name": "Worn Short Sword", "type": "Short Sword",
        "damage": 13, "damage_stat": {"DEX": 0.3, "STR": 0.12},
        "range": "melee", "speed_mod": 1, "accuracy_mod": 0, "crit_mod": 0,
        "weight_class": "light", "phys_type": "slashing",
        "requirements": {"DEX": 8}, "spell_bonus": 0, "special": {},
    },
    "Iron Short Sword": {
        "name": "Iron Short Sword", "type": "Short Sword",
        "damage": 15, "damage_stat": {"DEX": 0.3, "STR": 0.12},
        "range": "melee", "speed_mod": 1, "accuracy_mod": 0, "crit_mod": 0,
        "weight_class": "light", "phys_type": "slashing",
        "requirements": {"DEX": 10}, "spell_bonus": 0, "special": {},
    },

    # ── LONGSWORDS ───────────────────────────────────────────
    "Worn Longsword": {
        "name": "Worn Longsword", "type": "Longsword",
        "damage": 15, "damage_stat": {"STR": 0.3, "DEX": 0.12},
        "range": "melee", "speed_mod": 0, "accuracy_mod": 0, "crit_mod": 0,
        "weight_class": "medium", "phys_type": "slashing",
        "requirements": {"STR": 10}, "spell_bonus": 0, "special": {},
    },
    "Iron Longsword": {
        "name": "Iron Longsword", "type": "Longsword",
        "damage": 17, "damage_stat": {"STR": 0.3, "DEX": 0.12},
        "range": "melee", "speed_mod": 0, "accuracy_mod": 0, "crit_mod": 0,
        "weight_class": "medium", "phys_type": "slashing",
        "requirements": {"STR": 12}, "spell_bonus": 0, "special": {},
    },

    # ── BROADSWORDS ──────────────────────────────────────────
    "Iron Broadsword": {
        "name": "Iron Broadsword", "type": "Broadsword",
        "damage": 20, "damage_stat": {"STR": 0.4},
        "range": "melee", "speed_mod": -2, "accuracy_mod": -5, "crit_mod": 2,
        "weight_class": "heavy", "phys_type": "slashing",
        "requirements": {"STR": 13}, "spell_bonus": 0, "special": {},
    },

    # ── MACES / HAMMERS ──────────────────────────────────────
    "Wooden Club": {
        "name": "Wooden Club", "type": "Mace",
        "damage": 14, "damage_stat": {"STR": 0.4},
        "range": "melee", "speed_mod": -1, "accuracy_mod": -5, "crit_mod": 2,
        "weight_class": "medium", "phys_type": "blunt",
        "requirements": {"STR": 8}, "spell_bonus": 0,
        "special": {"armor_bypass": 0.30},
    },
    "Iron Mace": {
        "name": "Iron Mace", "type": "Mace",
        "damage": 17, "damage_stat": {"STR": 0.4},
        "range": "melee", "speed_mod": -1, "accuracy_mod": -5, "crit_mod": 2,
        "weight_class": "medium", "phys_type": "blunt",
        "requirements": {"STR": 11}, "spell_bonus": 0,
        "special": {"armor_bypass": 0.30},
    },

    # ── STAVES ───────────────────────────────────────────────
    "Walking Stick": {
        "name": "Walking Stick", "type": "Staff",
        "damage": 11, "damage_stat": {"STR": 0.16, "INT": 0.25},
        "range": "melee", "speed_mod": 0, "accuracy_mod": 0, "crit_mod": 0,
        "weight_class": "medium", "phys_type": "blunt",
        "requirements": {}, "spell_bonus": 2, "special": {},
    },
    "Wooden Staff": {
        "name": "Wooden Staff", "type": "Staff",
        "damage": 13, "damage_stat": {"STR": 0.16, "INT": 0.25},
        "range": "melee", "speed_mod": 0, "accuracy_mod": 0, "crit_mod": 0,
        "weight_class": "medium", "phys_type": "blunt",
        "requirements": {"INT": 8}, "spell_bonus": 4, "special": {},
    },
    "Sacred Staff": {
        "name": "Sacred Staff", "type": "Staff",
        "damage": 14, "damage_stat": {"STR": 0.16, "WIS": 0.25},
        "range": "melee", "speed_mod": 0, "accuracy_mod": 0, "crit_mod": 0,
        "weight_class": "medium", "phys_type": "blunt",
        "requirements": {"PIE": 12}, "spell_bonus": 8, "special": {},
    },

    # ── SPEARS ───────────────────────────────────────────────
    "Wooden Spear": {
        "name": "Wooden Spear", "type": "Spear",
        "damage": 14, "damage_stat": {"STR": 0.25, "DEX": 0.16},
        "range": "reach", "speed_mod": 0, "accuracy_mod": 5, "crit_mod": 0,
        "weight_class": "medium", "phys_type": "piercing",
        "requirements": {"STR": 9}, "spell_bonus": 0, "special": {},
    },
    "Iron Spear": {
        "name": "Iron Spear", "type": "Spear",
        "damage": 16, "damage_stat": {"STR": 0.25, "DEX": 0.16},
        "range": "reach", "speed_mod": 0, "accuracy_mod": 5, "crit_mod": 0,
        "weight_class": "medium", "phys_type": "piercing",
        "requirements": {"STR": 11, "DEX": 9}, "spell_bonus": 0, "special": {},
    },

    # ── SLINGS ───────────────────────────────────────────────
    "Simple Sling": {
        "name": "Simple Sling", "type": "Sling",
        "damage": 11, "damage_stat": {"DEX": 0.4},
        "range": "ranged", "speed_mod": 0, "accuracy_mod": -5, "crit_mod": 0,
        "weight_class": "light", "phys_type": "blunt",
        "requirements": {"DEX": 8}, "spell_bonus": 0, "special": {},
    },

    # ── BOWS ─────────────────────────────────────────────────
    "Short Bow": {
        "name": "Short Bow", "type": "Bow",
        "damage": 14, "damage_stat": {"DEX": 0.35, "STR": 0.08},
        "range": "ranged", "speed_mod": 0, "accuracy_mod": 5, "crit_mod": 3,
        "weight_class": "medium", "phys_type": "piercing",
        "requirements": {"DEX": 10, "STR": 8}, "spell_bonus": 0, "special": {},
    },
    "Hunting Bow": {
        "name": "Hunting Bow", "type": "Bow",
        "damage": 16, "damage_stat": {"DEX": 0.35, "STR": 0.08},
        "range": "ranged", "speed_mod": 0, "accuracy_mod": 5, "crit_mod": 3,
        "weight_class": "medium", "phys_type": "piercing",
        "requirements": {"DEX": 12, "STR": 9}, "spell_bonus": 0, "special": {},
    },

    # ── CROSSBOWS ────────────────────────────────────────────
    "Light Crossbow": {
        "name": "Light Crossbow", "type": "Crossbow",
        "damage": 12, "damage_stat": {"DEX": 0.08},  # mostly flat damage
        "range": "ranged", "speed_mod": -3, "accuracy_mod": 10, "crit_mod": 0,
        "weight_class": "medium", "phys_type": "piercing",
        "requirements": {"DEX": 8}, "spell_bonus": 0,
        "special": {"is_crossbow": True},
    },

    # ── THROWN ────────────────────────────────────────────────
    "Throwing Knife": {
        "name": "Throwing Knife", "type": "Thrown",
        "damage": 12, "damage_stat": {"DEX": 0.25, "STR": 0.16},
        "range": "thrown", "speed_mod": 1, "accuracy_mod": 0, "crit_mod": 0,
        "weight_class": "light", "phys_type": "piercing",
        "requirements": {"DEX": 10}, "spell_bonus": 0, "special": {},
    },
    "Throwing Axe": {
        "name": "Throwing Axe", "type": "Thrown",
        "damage": 15, "damage_stat": {"DEX": 0.25, "STR": 0.16},
        "range": "thrown", "speed_mod": 1, "accuracy_mod": 0, "crit_mod": 0,
        "weight_class": "light", "phys_type": "slashing",
        "requirements": {"DEX": 11, "STR": 10}, "spell_bonus": 0, "special": {},
    },
}


# ═══════════════════════════════════════════════════════════════
#  CLASS WEAPON PROFICIENCIES
# ═══════════════════════════════════════════════════════════════

CLASS_PROFICIENCIES = {
    "Fighter":      ["Fists", "Dagger", "Short Sword", "Longsword", "Broadsword",
                     "Mace", "Spear", "Crossbow", "Thrown", "Bow",
                     "Axe", "Greataxe", "Warhammer", "Greatsword", "Shield", "Glaive", "Lance"],
    "Mage":         ["Fists", "Dagger", "Staff", "Sling", "Wand", "Orb", "Rod", "Grimoire"],
    "Cleric":       ["Fists", "Mace", "Staff", "Sling", "Wand", "Warhammer", "Rod", "Scepter", "Censer", "Flail", "Morning Star"],
    "Thief":        ["Fists", "Dagger", "Short Sword", "Sling", "Bow", "Thrown", "Rapier", "Crossbow"],
    "Ranger":       ["Fists", "Dagger", "Short Sword", "Longsword", "Staff",
                     "Spear", "Bow", "Shortbow", "Longbow", "Crossbow", "Thrown", "Glaive"],
    "Monk":         ["Fists", "Staff", "Spear", "Handwraps", "Kama"],
    "Paladin":      ["Fists", "Dagger", "Short Sword", "Longsword", "Broadsword",
                     "Mace", "Spear", "Shield", "Axe", "Staff", "Wand"],
    "Spellblade":   ["Fists", "Dagger", "Short Sword", "Longsword", "Staff", "Wand", "Orb"],
    "Warden":       ["Fists", "Dagger", "Short Sword", "Longsword", "Spear", "Bow", "Staff", "Glaive"],
    "Shadowblade":  ["Fists", "Dagger", "Short Sword", "Rapier", "Bow", "Crossbow", "Thrown"],
    "Beastmaster":  ["Fists", "Dagger", "Spear", "Bow", "Crossbow", "Axe", "Staff"],
    "Psion":        ["Fists", "Dagger", "Staff", "Wand", "Orb"],
    "Battlemage":   ["Fists", "Dagger", "Staff", "Wand", "Longsword", "Short Sword"],
    "Runeblade":    ["Fists", "Longsword", "Broadsword", "Short Sword", "Staff", "Wand"],
    "Templar":      ["Fists", "Mace", "Longsword", "Shield", "Staff"],
    "Exemplar":     ["Fists", "Mace", "Longsword", "Shield", "Staff"],
    "Nightstalker": ["Fists", "Dagger", "Short Sword", "Rapier", "Bow", "Crossbow"],
    "Arcane Thief": ["Fists", "Dagger", "Short Sword", "Wand", "Staff"],
    "Druid":        ["Fists", "Staff", "Spear", "Dagger", "Sling"],
    "Shaman":       ["Fists", "Staff", "Mace", "Spear", "Sling"],
    "Warlord":      ["Fists", "Longsword", "Broadsword", "Axe", "Greataxe", "Spear", "Shield"],
    "Berserker":    ["Fists", "Axe", "Greataxe", "Warhammer", "Greatsword", "Longsword"],
    "Avenger":      ["Fists", "Longsword", "Greatsword", "Mace", "Shield", "Staff"],
    "Archon":       ["Fists", "Longsword", "Greatsword", "Mace", "Shield", "Wand"],
    "Transcendent": ["Fists", "Staff", "Handwraps", "Kama", "Spear"],
}

# Maps weapon subtype → proficiency key (resolves shop/loot weapons with type="weapon")
SUBTYPE_TO_PROF = {
    "Shortbow":    "Bow",        "Longbow":    "Bow",
    "Warhammer":   "Warhammer",  "Greatsword": "Greatsword",
    "Greataxe":    "Axe",        "Axe":        "Axe",
    "Hand Axe":    "Axe",        "Battleaxe":  "Axe",
    "Broadsword":  "Broadsword", "Long Sword":  "Longsword",
    "Short Sword": "Short Sword","Rapier":      "Rapier",
    "Kama":        "Kama",       "Handwraps":   "Handwraps",
    "Orb":         "Orb",        "Wand":        "Wand",
    "Shield":      "Shield",     "Glaive":      "Glaive",
    "Lance":       "Lance",      "Spear":       "Spear",
    "Mace":        "Mace",       "Club":        "Mace",
    "Staff":       "Staff",      "Dagger":      "Dagger",
    "Longsword":   "Longsword",  "Crossbow":    "Crossbow",
    "Cutlass":     "Short Sword", "Saber":       "Short Sword",
    # New subtypes for Mage/Cleric weapon expansion
    "Rod":          "Rod",
    "Scepter":      "Mace",
    "Censer":       "Mace",
    "Morning Star": "Mace",
    "Flail":        "Mace",
    "Grimoire":     "Staff",
    "Sling":        "Sling",
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
