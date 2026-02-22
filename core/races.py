"""
Realm of Shadows — Race System

Each race provides:
- stat_mods: permanent stat adjustments at character creation
- passives: gameplay-affecting bonuses checked in combat, dungeon, etc.
- description, lore: display text for character creation
- color: UI accent color for the race name
"""

RACES = {
    "Human": {
        "stat_mods": {},  # +1 to any stat (chosen at creation)
        "passives": {
            "bonus_xp": 0.05,          # 5% bonus XP from all sources
            "flexible_stat": True,      # gets to pick +1 to any stat
        },
        "description": "Versatile and ambitious. Humans adapt to any role.",
        "lore": "The most common folk of the realm. What they lack in innate gifts, "
                "they make up for in determination and sheer variety. Many of the "
                "greatest Wardens were human.",
        "color": (200, 200, 190),
    },
    "Elf": {
        "stat_mods": {"INT": 2, "DEX": 1, "CON": -1},
        "passives": {
            "secret_door_bonus": 15,    # +15% to secret door detection
            "shadow_resist": 0.85,      # 15% less shadow damage taken
        },
        "description": "Graceful and perceptive. +2 INT, +1 DEX, -1 CON. Sense hidden doors.",
        "lore": "Long-lived and attuned to the unseen currents of the world. Elves "
                "were the first to notice the Fading's encroachment, though few "
                "believed their warnings.",
        "color": (140, 220, 180),
    },
    "Dwarf": {
        "stat_mods": {"CON": 2, "STR": 1, "DEX": -1},
        "passives": {
            "trap_detect_bonus": 12,    # +12% trap detection
            "poison_resist": 0.70,      # 30% less poison damage
        },
        "description": "Sturdy and resolute. +2 CON, +1 STR, -1 DEX. Resist poison, spot traps.",
        "lore": "Children of the deep earth, dwarves built the great halls beneath "
                "the mountains long before the Wardens arose. Their stonework endures "
                "even where the Fading has consumed everything else.",
        "color": (200, 160, 100),
    },
    "Halfling": {
        "stat_mods": {"DEX": 2, "WIS": 1, "STR": -2},
        "passives": {
            "crit_bonus": 0.05,         # +5% crit chance
            "dodge_bonus": 0.08,        # +8% dodge chance
        },
        "description": "Quick and lucky. +2 DEX, +1 WIS, -2 STR. Better crits and dodge.",
        "lore": "Small in stature but large in courage. Halflings are natural wanderers "
                "whose luck is the stuff of legend. They say a halfling's coin always "
                "lands face up — at least when it matters.",
        "color": (220, 190, 120),
    },
    "Half-Orc": {
        "stat_mods": {"STR": 3, "INT": -1, "PIE": -1},
        "passives": {
            "damage_bonus": 0.08,       # +8% physical damage dealt
            "intimidate": True,         # dialogue/encounter bonus (future)
        },
        "description": "Powerful and fierce. +3 STR, -1 INT, -1 PIE. Hit harder.",
        "lore": "Caught between two worlds, half-orcs are often mistrusted but rarely "
                "underestimated. In the frontier towns, strength speaks louder than lineage.",
        "color": (160, 200, 120),
    },
    "Gnome": {
        "stat_mods": {"WIS": 2, "INT": 1, "STR": -1},
        "passives": {
            "mp_reduction": 1,          # spells cost 1 less MP (min 1)
            "arcane_resist": 0.85,      # 15% less arcane damage taken
        },
        "description": "Clever and magically gifted. +2 WIS, +1 INT, -1 STR. Spells cost less.",
        "lore": "Gnomes have an innate connection to the arcane threads that bind reality. "
                "Their scholars were the first to theorize that the Fading is not destruction "
                "but unraveling — the world's stitches coming loose.",
        "color": (180, 140, 220),
    },
    "Fading-Touched": {
        "stat_mods": {"INT": 2, "PIE": 1, "CON": -2},
        "passives": {
            "shadow_resist": 0.65,      # 35% less shadow damage taken
            "divine_vulnerability": 1.15,  # 15% more divine damage taken
            "fading_sense": True,       # can detect Fading corruption (quest/lore bonus)
            "shadow_damage_bonus": 0.10,  # +10% shadow spell damage
        },
        "description": "Marked by the Fading. +2 INT, +1 PIE, -2 CON. Shadow resist, divine weakness.",
        "lore": "Descendants of those who survived direct Fading exposure. Their eyes hold "
                "a faint violet shimmer, and they can sense the boundary between worlds. "
                "Feared by the superstitious, invaluable to the wise.",
        "color": (160, 120, 220),
    },
}

RACE_ORDER = ["Human", "Elf", "Dwarf", "Halfling", "Half-Orc", "Gnome", "Fading-Touched"]


def get_race(race_name):
    """Get race data by name. Returns None if not found."""
    return RACES.get(race_name)


def get_stat_mods(race_name):
    """Get stat modifications for a race."""
    race = RACES.get(race_name, {})
    return dict(race.get("stat_mods", {}))


def get_passive(race_name, passive_key, default=None):
    """Get a specific passive value for a race."""
    race = RACES.get(race_name, {})
    return race.get("passives", {}).get(passive_key, default)


def apply_racial_stats(stats, race_name):
    """Apply racial stat modifications to a stat dict. Modifies in place."""
    mods = get_stat_mods(race_name)
    for stat, mod in mods.items():
        if stat in stats:
            stats[stat] = max(1, stats[stat] + mod)  # minimum 1 in any stat


def get_racial_xp_multiplier(race_name):
    """Returns XP multiplier (1.0 = normal, 1.05 = human bonus)."""
    bonus = get_passive(race_name, "bonus_xp", 0)
    return 1.0 + bonus


def get_racial_mp_reduction(race_name):
    """Returns MP cost reduction for spells (0 for most races, 1 for gnome)."""
    return get_passive(race_name, "mp_reduction", 0)


def get_racial_damage_multiplier(race_name, damage_element=None):
    """Returns damage multiplier based on race and element."""
    mult = 1.0
    # Physical damage bonus (Half-Orc)
    if damage_element in (None, "physical", "slashing", "piercing", "blunt"):
        mult += get_passive(race_name, "damage_bonus", 0)
    # Shadow damage bonus (Fading-Touched)
    if damage_element == "shadow":
        mult += get_passive(race_name, "shadow_damage_bonus", 0)
    return mult


def get_racial_resist_multiplier(race_name, damage_element):
    """Returns incoming damage multiplier for elemental resistance/vulnerability."""
    if damage_element == "shadow":
        return get_passive(race_name, "shadow_resist", 1.0)
    if damage_element == "arcane":
        return get_passive(race_name, "arcane_resist", 1.0)
    if damage_element == "divine":
        return get_passive(race_name, "divine_vulnerability", 1.0)
    if damage_element in ("nature",) and get_passive(race_name, "poison_resist", 1.0) < 1.0:
        return get_passive(race_name, "poison_resist", 1.0)
    return 1.0


def get_racial_crit_bonus(race_name):
    """Extra crit chance from race (0.0-1.0 scale)."""
    return get_passive(race_name, "crit_bonus", 0.0)


def get_racial_dodge_bonus(race_name):
    """Extra dodge chance from race (0.0-1.0 scale)."""
    return get_passive(race_name, "dodge_bonus", 0.0)
