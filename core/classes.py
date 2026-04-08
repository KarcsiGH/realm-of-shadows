"""
Realm of Shadows — Class Definitions & Resource Formulas
All formulas from the complete design document.
"""

# The 6 base stats
STAT_NAMES = ["STR", "DEX", "CON", "INT", "WIS", "PIE"]

STAT_FULL_NAMES = {
    "STR": "Strength",
    "DEX": "Dexterity",
    "CON": "Constitution",
    "INT": "Intelligence",
    "WIS": "Wisdom",
    "PIE": "Piety",
}

# ── Base Classes ──────────────────────────────────────────────

CLASSES = {
    "Fighter": {
        "description": "Front-line warrior. High HP, physical damage, heavy armor.",
        "primary": "STR",
        "secondary": "CON",
        "base_hp": 60,
        "starting_stats": {"STR": 14, "DEX": 10, "CON": 12, "INT": 6, "WIS": 8, "PIE": 4},
        "starting_abilities": [
            {"name": "Power Strike", "cost": 10, "resource": "STR-SP",
             "desc": "Heavy melee attack dealing bonus physical damage."},
            {"name": "Defensive Stance", "cost": 8, "resource": "STR-SP",
             "desc": "Reduce incoming damage for one turn."},
        ],
        "ki_formula": lambda s, lvl: (s["STR"] * 5) + (s["CON"] * 3) + (lvl * 10),
        "resources": ["HP", "STR-SP", "Ki"],
        "stat_growth": {
            "STR": "high", "CON": "high", "DEX": "medium",
            "INT": "low", "WIS": "low", "PIE": "low",
        },
        "color": (200, 60, 60),  # red
    },
    "Mage": {
        "description": "Powerful arcane spellcaster. Devastating magic, fragile body.",
        "primary": "INT",
        "secondary": "WIS",
        "base_hp": 30,
        "starting_stats": {"STR": 4, "DEX": 8, "CON": 6, "INT": 16, "WIS": 12, "PIE": 6},
        "starting_abilities": [
            {"name": "Magic Missile", "cost": 8, "resource": "INT-MP",
             "desc": "Basic arcane bolt that never misses."},
            {"name": "Arcane Shield", "cost": 10, "resource": "INT-MP", "self_only": True,
             "desc": "Conjure a magical barrier for protection."},
        ],
        "ki_formula": lambda s, lvl: (s["INT"] * 5) + (s["WIS"] * 3) + (lvl * 10),
        "resources": ["HP", "INT-MP", "WIS-MP", "Ki"],
        "stat_growth": {
            "INT": "high", "WIS": "high", "DEX": "medium",
            "STR": "low", "CON": "low", "PIE": "low",
        },
        "color": (80, 80, 220),  # blue
    },
    "Cleric": {
        "description": "Divine healer and support. Essential for party survival.",
        "primary": "PIE",
        "secondary": "WIS",
        "base_hp": 45,
        "starting_stats": {"STR": 8, "DEX": 8, "CON": 10, "INT": 10, "WIS": 12, "PIE": 16},
        "starting_abilities": [
            {"name": "Heal", "cost": 12, "resource": "PIE-MP",
             "desc": "Restore an ally's health with divine power."},
            {"name": "Smite", "cost": 10, "resource": "PIE-MP",
             "desc": "Strike an enemy with holy radiance."},
        ],
        "ki_formula": lambda s, lvl: (s["PIE"] * 5) + (s["WIS"] * 3) + (lvl * 10),
        "resources": ["HP", "PIE-MP", "WIS-MP", "Ki"],
        "stat_growth": {
            "PIE": "high", "WIS": "high", "CON": "medium", "INT": "medium",
            "STR": "low", "DEX": "low",
        },
        "color": (220, 200, 60),  # gold
    },
    "Thief": {
        "description": "Quick and cunning. High damage, stealth, critical hits.",
        "primary": "DEX",
        "secondary": "INT",
        "base_hp": 40,
        "starting_stats": {"STR": 10, "DEX": 16, "CON": 8, "INT": 10, "WIS": 8, "PIE": 4},
        "starting_abilities": [
            {"name": "Quick Strike", "cost": 8, "resource": "DEX-SP",
             "desc": "Fast attack with a chance to strike first."},
            {"name": "Evade", "cost": 6, "resource": "DEX-SP",
             "desc": "Dodge the next incoming attack entirely."},
        ],
        "ki_formula": lambda s, lvl: (s["DEX"] * 5) + (s["INT"] * 3) + (lvl * 10),
        "resources": ["HP", "DEX-SP", "Ki"],
        "stat_growth": {
            "DEX": "high", "INT": "high", "STR": "medium",
            "WIS": "low", "CON": "low", "PIE": "low",
        },
        "color": (100, 200, 100),  # green
    },
    "Ranger": {
        "description": "Balanced warrior of the wilds. Nature magic, ranged combat.",
        "primary": "WIS",
        "secondary": "DEX",
        "base_hp": 50,
        "starting_stats": {"STR": 11, "DEX": 14, "CON": 10, "INT": 10, "WIS": 14, "PIE": 6},
        "starting_abilities": [
            {"name": "Aimed Shot", "cost": 8, "resource": "DEX-SP",
             "desc": "Precise ranged attack with bonus accuracy."},
            {"name": "Splitting Arrow", "cost": 8, "resource": "DEX-SP",
             "desc": "Arrow pierces front row, hitting back row too. Reduced damage."},
        ],
        "ki_formula": lambda s, lvl: (s["WIS"] * 5) + (s["DEX"] * 3) + (lvl * 10),
        "resources": ["HP", "WIS-MP", "DEX-SP", "Ki"],
        "stat_growth": {
            "WIS": "high", "DEX": "high", "STR": "medium", "CON": "medium",
            "INT": "low", "PIE": "low",
        },
        "color": (60, 160, 60),  # forest green
    },
    "Monk": {
        "description": "Ki specialist. Unarmed combat, spiritual power, fast regeneration.",
        "primary": "WIS",
        "secondary": "DEX",
        "base_hp": 50,
        "starting_stats": {"STR": 12, "DEX": 14, "CON": 10, "INT": 8, "WIS": 16, "PIE": 10},
        "starting_abilities": [
            {"name": "Flurry of Blows", "cost": 10, "resource": "Ki",
             "desc": "Unleash multiple rapid unarmed strikes."},
            {"name": "Iron Skin", "cost": 8, "resource": "Ki", "self_only": True,
             "desc": "Harden your body to reduce incoming damage."},
        ],
        "ki_formula": lambda s, lvl: (s["WIS"] * 2) + (s["DEX"] * 1) + (lvl * 2),
        "resources": ["HP", "DEX-SP", "WIS-MP", "Ki"],
        "stat_growth": {
            "WIS": "high", "DEX": "high", "CON": "medium", "STR": "medium",
            "INT": "low", "PIE": "low",
        },
        "monk_ki_bonus": True,
        "color": (180, 140, 220),  # purple
    },
}


# ── Hybrid Classes (Level 10 transitions) ─────────────────────
# These inherit resource pools from both parent classes.
# ki_formula uses the class's primary casting stat.

_HYBRIDS = {
    # Fighter hybrids
    "Paladin": {
        "description": "Holy warrior combining divine magic and martial power.",
        "primary": "PIE", "secondary": "STR", "base_hp": 55,
        "resources": ["HP", "STR-SP", "PIE-MP"],
        "ki_formula": lambda s, lvl: (s["PIE"] * 4) + (s["STR"] * 2) + (lvl * 10),
        "color": (220, 180, 60), "starting_abilities": [{"name": "Crusader Strike", "type": "attack"}, {"name": "Lay on Hands", "type": "heal"}],
        "starting_stats": {"STR": 14, "DEX": 10, "CON": 12, "INT": 6, "WIS": 10, "PIE": 14},
        "stat_growth": {"STR": "high", "PIE": "high", "CON": "medium", "DEX": "low", "INT": "low", "WIS": "low"},
    },
    "Spellblade": {
        "description": "Arcane warrior who channels spells through their blade.",
        "primary": "INT", "secondary": "STR", "base_hp": 48,
        "resources": ["HP", "STR-SP", "INT-MP"],
        "ki_formula": lambda s, lvl: (s["INT"] * 4) + (s["STR"] * 2) + (lvl * 10),
        "color": (140, 80, 200), "starting_abilities": [{"name": "Arcane Edge", "type": "attack"}, {"name": "Runic Armor", "type": "buff"}],
        "starting_stats": {"STR": 12, "DEX": 10, "CON": 10, "INT": 14, "WIS": 8, "PIE": 6},
        "stat_growth": {"INT": "high", "STR": "high", "DEX": "medium", "CON": "low", "WIS": "low", "PIE": "low"},
    },
    "Warder": {
        "description": "Tactical combatant combining heavy strikes and shadow techniques.",
        "primary": "STR", "secondary": "DEX", "base_hp": 52,
        "resources": ["HP", "STR-SP", "DEX-SP", "Ki"],
        "ki_formula": lambda s, lvl: (s["STR"] * 4) + (s["DEX"] * 2) + (lvl * 10),
        "color": (60, 160, 100), "starting_abilities": [],
        "starting_stats": {"STR": 12, "DEX": 14, "CON": 10, "INT": 8, "WIS": 8, "PIE": 4},
        "stat_growth": {"STR": "high", "DEX": "high", "CON": "medium", "INT": "low", "WIS": "low", "PIE": "low"},
    },
    "Strider": {
        "description": "Mobile skirmisher excelling at rapid movement and precise strikes.",
        "primary": "DEX", "secondary": "STR", "base_hp": 50,
        "resources": ["HP", "DEX-SP", "WIS-MP", "Ki"],
        "ki_formula": lambda s, lvl: (s["DEX"] * 4) + (s["STR"] * 2) + (lvl * 10),
        "color": (120, 160, 60), "starting_abilities": [],
        "starting_stats": {"STR": 12, "DEX": 14, "CON": 10, "INT": 8, "WIS": 10, "PIE": 4},
        "stat_growth": {"DEX": "high", "STR": "high", "WIS": "medium", "CON": "low", "INT": "low", "PIE": "low"},
    },
    "Guardian": {
        "description": "Armored protector channeling ki to defend allies.",
        "primary": "STR", "secondary": "CON", "base_hp": 62,
        "resources": ["HP", "STR-SP", "Ki"],
        "ki_formula": lambda s, lvl: (s["STR"] * 4) + (s["CON"] * 3) + (lvl * 10),
        "color": (60, 100, 200), "starting_abilities": [],
        "starting_stats": {"STR": 14, "DEX": 8, "CON": 14, "INT": 6, "WIS": 10, "PIE": 6},
        "stat_growth": {"STR": "high", "CON": "high", "WIS": "medium", "DEX": "low", "INT": "low", "PIE": "low"},
    },
    # Mage hybrids
    "Witch": {
        "description": "Dark spellcaster blending arcane and divine powers.",
        "primary": "INT", "secondary": "PIE", "base_hp": 35,
        "resources": ["HP", "INT-MP", "PIE-MP"],
        "ki_formula": lambda s, lvl: (s["INT"] * 4) + (s["PIE"] * 2) + (lvl * 10),
        "color": (160, 60, 180), "starting_abilities": [{"name": "Hex Bolt", "type": "spell"}, {"name": "Dark Bargain", "type": "buff"}],
        "starting_stats": {"STR": 4, "DEX": 8, "CON": 6, "INT": 14, "WIS": 14, "PIE": 12},
        "stat_growth": {"INT": "high", "WIS": "high", "PIE": "medium", "DEX": "low", "CON": "low", "STR": "low"},
    },
    "Necromancer": {
        "description": "Master of death magic, draining life and raising the fallen.",
        "primary": "INT", "secondary": "WIS", "base_hp": 36,
        "resources": ["HP", "INT-MP", "PIE-MP"],
        "ki_formula": lambda s, lvl: (s["INT"] * 5) + (s["WIS"] * 2) + (lvl * 10),
        "color": (100, 30, 120), "starting_abilities": [{"name": "Life Drain", "type": "attack"}, {"name": "Bone Cage", "type": "debuff"}],
        "starting_stats": {"STR": 4, "DEX": 10, "CON": 6, "INT": 16, "WIS": 12, "PIE": 6},
        "stat_growth": {"INT": "high", "WIS": "medium", "DEX": "medium", "CON": "low", "STR": "low", "PIE": "low"},
    },
    "Druid": {
        "description": "Nature spellcaster harnessing elemental and healing powers.",
        "primary": "WIS", "secondary": "INT", "base_hp": 40,
        "resources": ["HP", "WIS-MP", "INT-MP"],
        "ki_formula": lambda s, lvl: (s["WIS"] * 5) + (s["INT"] * 2) + (lvl * 10),
        "color": (80, 180, 60), "starting_abilities": [{"name": "Entangle", "type": "aoe"}, {"name": "Rejuvenate", "type": "aoe_heal"}],
        "starting_stats": {"STR": 6, "DEX": 10, "CON": 8, "INT": 12, "WIS": 16, "PIE": 8},
        "stat_growth": {"WIS": "high", "INT": "high", "CON": "medium", "DEX": "low", "STR": "low", "PIE": "low"},
    },
    "Mystic": {
        "description": "Arcane ki master fusing magical theory with inner discipline.",
        "primary": "INT", "secondary": "WIS", "base_hp": 40,
        "resources": ["HP", "INT-MP", "Ki"],
        "ki_formula": lambda s, lvl: (s["INT"] * 4) + (s["WIS"] * 3) + (lvl * 10),
        "color": (60, 180, 200), "starting_abilities": [{"name": "Force Pulse", "type": "aoe"}, {"name": "Ki Absorption", "type": "buff"}],
        "starting_stats": {"STR": 6, "DEX": 10, "CON": 8, "INT": 14, "WIS": 12, "PIE": 6},
        "stat_growth": {"INT": "high", "WIS": "high", "DEX": "medium", "CON": "low", "STR": "low", "PIE": "low"},
    },
    # Cleric hybrids
    "Warden": {
        "description": "Ancient guardian combining divine protection and nature's power.",
        "primary": "WIS", "secondary": "PIE", "base_hp": 48,
        "resources": ["HP", "PIE-MP", "WIS-MP", "DEX-SP", "Ki"],
        "ki_formula": lambda s, lvl: (s["WIS"] * 4) + (s["PIE"] * 3) + (lvl * 10),
        "color": (40, 140, 80), "starting_abilities": [],
        "starting_stats": {"STR": 8, "DEX": 12, "CON": 10, "INT": 8, "WIS": 14, "PIE": 12},
        "stat_growth": {"WIS": "high", "PIE": "high", "DEX": "medium", "CON": "medium", "INT": "low", "STR": "low"},
    },
    "Inquisitor": {
        "description": "Shadow-wielding divine agent who hunts the corrupt.",
        "primary": "PIE", "secondary": "DEX", "base_hp": 44,
        "resources": ["HP", "DEX-SP", "PIE-MP", "Ki"],
        "ki_formula": lambda s, lvl: (s["PIE"] * 4) + (s["DEX"] * 3) + (lvl * 10),
        "color": (180, 140, 40), "starting_abilities": [],
        "starting_stats": {"STR": 8, "DEX": 12, "CON": 8, "INT": 8, "WIS": 12, "PIE": 14},
        "stat_growth": {"PIE": "high", "DEX": "high", "WIS": "medium", "CON": "low", "STR": "low", "INT": "low"},
    },
    "Templar": {
        "description": "Devoted warrior combining divine faith and physical discipline.",
        "primary": "PIE", "secondary": "STR", "base_hp": 50,
        "resources": ["HP", "PIE-MP", "Ki"],
        "ki_formula": lambda s, lvl: (s["PIE"] * 4) + (s["STR"] * 2) + (lvl * 10),
        "color": (160, 180, 220), "starting_abilities": [],
        "starting_stats": {"STR": 10, "DEX": 8, "CON": 14, "INT": 6, "WIS": 10, "PIE": 12},
        "stat_growth": {"PIE": "high", "STR": "medium", "CON": "high", "DEX": "low", "INT": "low", "WIS": "low"},
    },
    # Thief hybrids
    "Duskblade": {
        "description": "Shadow warrior who channels the Fading itself as a weapon. Grows stronger as enemies become corrupted.",
        "primary": "STR", "secondary": "DEX", "base_hp": 52,
        "resources": ["HP", "STR-SP", "DEX-SP"],
        "color": (90, 60, 120), "starting_abilities": [{"name": "Void Strike", "type": "attack"}, {"name": "Shadow Mantle", "type": "buff"}],
        "starting_stats": {"STR": 14, "DEX": 14, "CON": 10, "INT": 8, "WIS": 8, "PIE": 4},
        "stat_growth": {"STR": "high", "DEX": "high", "CON": "medium", "WIS": "low", "INT": "low", "PIE": "low"},
    },
    "Assassin": {
        "description": "Lethal hunter combining tracking, poisons, and shadow strikes.",
        "primary": "DEX", "secondary": "WIS", "base_hp": 44,
        "resources": ["HP", "DEX-SP"],
        "ki_formula": lambda s, lvl: (s["DEX"] * 5) + (s["WIS"] * 2) + (lvl * 10),
        "color": (180, 40, 60), "starting_abilities": [{"name": "Shadow Step", "type": "buff"}, {"name": "Crippling Strike", "type": "attack"}],
        "starting_stats": {"STR": 10, "DEX": 16, "CON": 8, "INT": 10, "WIS": 10, "PIE": 4},
        "stat_growth": {"DEX": "high", "STR": "medium", "WIS": "medium", "CON": "low", "INT": "low", "PIE": "low"},
    },
    "Phantom": {
        "description": "Ki-powered shadow who phases through defenses.",
        "primary": "DEX", "secondary": "WIS", "base_hp": 44,
        "resources": ["HP", "DEX-SP", "Ki"],
        "ki_formula": lambda s, lvl: (s["DEX"] * 4) + (s["WIS"] * 3) + (lvl * 10),
        "color": (140, 140, 200), "starting_abilities": [],
        "starting_stats": {"STR": 8, "DEX": 14, "CON": 8, "INT": 8, "WIS": 12, "PIE": 6},
        "stat_growth": {"DEX": "high", "WIS": "high", "CON": "medium", "STR": "low", "INT": "low", "PIE": "low"},
    },
    # Ranger hybrid
    "Shaman": {
        "description": "Wilderness spiritualist drawing ki from the natural world.",
        "primary": "WIS", "secondary": "DEX", "base_hp": 46,
        "resources": ["HP", "WIS-MP", "DEX-SP"],
        "ki_formula": lambda s, lvl: (s["WIS"] * 5) + (s["DEX"] * 2) + (lvl * 10),
        "color": (120, 150, 80), "starting_abilities": [{"name": "Spirit Strike", "type": "attack"}, {"name": "Spirit Bind", "type": "buff"}],
        "starting_stats": {"STR": 10, "DEX": 12, "CON": 12, "INT": 8, "WIS": 14, "PIE": 8},
        "stat_growth": {"WIS": "high", "DEX": "medium", "CON": "medium", "STR": "low", "INT": "low", "PIE": "low"},
    },
}

# ── Apex Classes (Level 15 transitions) ───────────────────────

_APEX = {
    "Knight": {
        "description": "The pinnacle of martial prowess — legendary defender and warrior.",
        "primary": "STR", "secondary": "CON", "base_hp": 70,
        "resources": ["HP", "STR-SP", "Ki"],
        "ki_formula": lambda s, lvl: (s["STR"] * 5) + (s["CON"] * 4) + (lvl * 12),
        "color": (220, 100, 80), "starting_abilities": [],
        "starting_stats": {"STR": 14, "DEX": 10, "CON": 12, "INT": 6, "WIS": 8, "PIE": 4},
        "stat_growth": {"STR": "high", "CON": "high", "DEX": "medium", "INT": "low", "WIS": "low", "PIE": "low"},
    },
    "Archmage": {
        "description": "Master of all arcane disciplines. Reality bends to their will.",
        "primary": "INT", "secondary": "WIS", "base_hp": 32,
        "resources": ["HP", "INT-MP", "WIS-MP", "Ki"],
        "ki_formula": lambda s, lvl: (s["INT"] * 6) + (s["WIS"] * 3) + (lvl * 12),
        "color": (60, 100, 240), "starting_abilities": [],
        "starting_stats": {"STR": 4, "DEX": 8, "CON": 6, "INT": 16, "WIS": 12, "PIE": 6},
        "stat_growth": {"INT": "high", "WIS": "high", "DEX": "medium", "STR": "low", "CON": "low", "PIE": "low"},
    },
    "High Priest": {
        "description": "Divine conduit of staggering power. Miracles are within reach.",
        "primary": "PIE", "secondary": "WIS", "base_hp": 48,
        "resources": ["HP", "PIE-MP", "WIS-MP", "Ki"],
        "ki_formula": lambda s, lvl: (s["PIE"] * 6) + (s["WIS"] * 3) + (lvl * 12),
        "color": (240, 220, 80), "starting_abilities": [],
        "starting_stats": {"STR": 8, "DEX": 8, "CON": 10, "INT": 10, "WIS": 12, "PIE": 16},
        "stat_growth": {"PIE": "high", "WIS": "high", "CON": "medium", "INT": "medium", "STR": "low", "DEX": "low"},
    },
    "Shadow Master": {
        "description": "Absolute master of shadow. Death comes from darkness unseen.",
        "primary": "DEX", "secondary": "INT", "base_hp": 42,
        "resources": ["HP", "DEX-SP", "Ki"],
        "ki_formula": lambda s, lvl: (s["DEX"] * 6) + (s["INT"] * 3) + (lvl * 12),
        "color": (80, 60, 110), "starting_abilities": [],
        "starting_stats": {"STR": 10, "DEX": 16, "CON": 8, "INT": 10, "WIS": 8, "PIE": 4},
        "stat_growth": {"DEX": "high", "INT": "high", "STR": "medium", "WIS": "low", "CON": "low", "PIE": "low"},
    },
    "Beastlord": {
        "description": "One with the wild. Commands nature and hunts with primal fury.",
        "primary": "WIS", "secondary": "DEX", "base_hp": 54,
        "resources": ["HP", "WIS-MP", "DEX-SP", "Ki"],
        "ki_formula": lambda s, lvl: (s["WIS"] * 6) + (s["DEX"] * 3) + (lvl * 12),
        "color": (40, 120, 60), "starting_abilities": [],
        "starting_stats": {"STR": 11, "DEX": 14, "CON": 10, "INT": 10, "WIS": 14, "PIE": 6},
        "stat_growth": {"WIS": "high", "DEX": "high", "CON": "medium", "STR": "medium", "INT": "low", "PIE": "low"},
    },
    "Ascetic": {
        "description": "Enlightened master of ki. Transcends mortal limitations entirely.",
        "primary": "WIS", "secondary": "DEX", "base_hp": 52,
        "resources": ["HP", "Ki"],
        "ki_formula": lambda s, lvl: (s["WIS"] * 6) + (s["DEX"] * 4) + (lvl * 14),
        "color": (200, 180, 240), "starting_abilities": [],
        "starting_stats": {"STR": 12, "DEX": 14, "CON": 10, "INT": 8, "WIS": 16, "PIE": 10},
        "stat_growth": {"WIS": "high", "DEX": "high", "CON": "medium", "STR": "medium", "INT": "low", "PIE": "low"},
    },
}

CLASSES.update(_HYBRIDS)
CLASSES.update(_APEX)

CLASS_ORDER = [
    # Base classes — low stat gates, available to almost anyone
    "Fighter", "Mage", "Cleric", "Thief", "Ranger", "Monk",
    # Hybrid classes — two-stat gates, available at creation if qualified
    "Paladin", "Spellblade", "Duskblade",
    "Witch", "Necromancer", "Druid", "Mystic",
    "Assassin", "Shaman",
]

# Minimum stat requirements for each class.
# Base classes: single stat, low threshold.
# Hybrids: two stats, higher thresholds.
# If a character meets all requirements, the class is available.
CLASS_STAT_REQUIREMENTS = {
    # Base classes
    "Fighter":    {"STR": 11},
    "Mage":       {"INT": 11},
    "Cleric":     {"PIE": 11},
    "Thief":      {"DEX": 11},
    "Ranger":     {"DEX": 10, "WIS": 10},
    "Monk":       {"CON": 11, "WIS": 10},
    # Hybrids — two stats, genuinely high thresholds
    "Paladin":    {"STR": 13, "PIE": 14},
    "Spellblade": {"STR": 13, "INT": 14},
    "Duskblade":  {"STR": 12, "DEX": 15},
    "Witch":      {"INT": 13, "PIE": 13},
    "Necromancer":{"INT": 15, "DEX": 12},
    "Druid":      {"INT": 12, "WIS": 15},
    "Mystic":     {"INT": 13, "WIS": 12, "CON": 12},
    "Assassin":   {"DEX": 16, "WIS": 11},
    "Shaman":     {"WIS": 15, "CON": 13},
}

def class_qualifies(stats: dict, class_name: str) -> bool:
    """Return True if the given stats meet the requirements for class_name."""
    reqs = CLASS_STAT_REQUIREMENTS.get(class_name, {})
    return all(stats.get(stat, 0) >= minimum for stat, minimum in reqs.items())

def get_available_classes(stats: dict) -> list:
    """Return list of (class_name, is_hybrid) tuples the character qualifies for."""
    result = []
    for cls in CLASS_ORDER:
        if class_qualifies(stats, cls):
            is_hybrid = cls not in ("Fighter","Mage","Cleric","Thief","Ranger","Monk")
            result.append((cls, is_hybrid))
    return result


# ── Resource Calculations ─────────────────────────────────────

def calc_hp(base_hp, con, level):
    return base_hp + (con * 2) + (level * 3)

def calc_ki(class_name, stats, level):
    cls = CLASSES.get(class_name, CLASSES["Fighter"])
    return cls["ki_formula"](stats, level)

def calc_int_mp(int_val, level):
    return (int_val * 2) + (level * 4)

def calc_wis_mp(wis_val, level):
    return (wis_val * 2) + (level * 4)

def calc_pie_mp(pie_val, level):
    return (pie_val * 2) + (level * 4)

def calc_str_sp(str_val, level):
    return (str_val * 2) + (level * 4)

def calc_dex_sp(dex_val, level):
    return (dex_val * 2) + (level * 4)


def get_all_resources(class_name, stats, level):
    """Calculate all resource pools for a character."""
    cls = CLASSES[class_name]
    resources = {}
    resources["HP"] = calc_hp(cls["base_hp"], stats["CON"], level)

    if "Ki" in cls["resources"] and "ki_formula" in cls:
        resources["Ki"] = calc_ki(class_name, stats, level)

    if "INT-MP" in cls["resources"]:
        resources["INT-MP"] = calc_int_mp(stats["INT"], level)
    if "WIS-MP" in cls["resources"]:
        resources["WIS-MP"] = calc_wis_mp(stats["WIS"], level)
    if "PIE-MP" in cls["resources"]:
        resources["PIE-MP"] = calc_pie_mp(stats["PIE"], level)
    if "STR-SP" in cls["resources"]:
        resources["STR-SP"] = calc_str_sp(stats["STR"], level)
    if "DEX-SP" in cls["resources"]:
        resources["DEX-SP"] = calc_dex_sp(stats["DEX"], level)

    return resources


def get_class_fit(stats):
    """Return available classes sorted by fit, respecting stat gate requirements.

    Returns list of (class_name, fit_category, score) tuples.
    Fit categories:
      'Hybrid — Qualified'  : meets stat gate for a hybrid class (special!)
      'Natural Fit'         : base class, primary stat is character's strength
      'Good Fit'            : base class, reasonable stat alignment
      'Unusual Choice'      : base class, stats don't align well but still valid
    """
    result = []

    for name in CLASS_ORDER:
        cls  = CLASSES.get(name, {})
        reqs = CLASS_STAT_REQUIREMENTS.get(name, {})
        is_hybrid = name not in ("Fighter","Mage","Cleric","Thief","Ranger","Monk")

        # Check stat gate — hybrids and base classes both have requirements
        qualifies = all(stats.get(stat, 0) >= minimum for stat, minimum in reqs.items())
        if not qualifies:
            continue  # doesn't qualify — don't show

        primary   = cls.get("primary", "STR")
        secondary = cls.get("secondary", "STR")

        # Score: alignment of character stats with class priorities
        score = stats.get(primary, 0) * 3 + stats.get(secondary, 0) * 2
        sorted_stats = sorted(stats.items(), key=lambda x: -x[1])
        top_2 = [s[0] for s in sorted_stats[:2]]
        if primary   in top_2: score += 10
        if secondary in top_2: score += 5

        if is_hybrid:
            cat = "✦ Hybrid Class"   # special category — highlight in UI
        else:
            # Fit category based on score
            max_possible = max(
                CLASSES[n].get("primary","STR") and
                stats.get(CLASSES[n]["primary"],0)*3 + stats.get(CLASSES[n]["secondary"],0)*2
                for n in ("Fighter","Mage","Cleric","Thief","Ranger","Monk")
            )
            diff = max_possible - score
            if diff <= 8:   cat = "Natural Fit"
            elif diff <= 25: cat = "Good Fit"
            else:            cat = "Unusual Choice"

        result.append((name, cat, score))

    # Sort: hybrids first (they're rare and exciting), then by score
    result.sort(key=lambda x: (0 if "Hybrid" in x[1] else 1, -x[2]))
    return result
