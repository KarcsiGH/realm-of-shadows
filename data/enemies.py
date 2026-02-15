"""
Realm of Shadows — Enemy Data
Starter roster from Combat_System_Design_v3.md.
Adding a new enemy = adding a dict here. No code changes needed.

Enemy resistance profiles from Elemental_Enchantment_System_Design_v1.md.
"""
from core.combat_config import (
    IMMUNE, RESISTANT, NEUTRAL, VULNERABLE, VERY_VULNERABLE,
    FRONT, MID, BACK,
)

# ═══════════════════════════════════════════════════════════════
#  ENEMY DEFINITIONS
# ═══════════════════════════════════════════════════════════════

ENEMIES = {
    "Goblin Warrior": {
        "name": "Goblin Warrior",
        "hp": 18, "defense": 2, "magic_resist": 1,
        "stats": {"STR": 6, "DEX": 10, "CON": 5, "INT": 4, "WIS": 4, "PIE": 2},
        "speed_base": 14,
        "attack_damage": 5, "attack_type": "melee", "phys_type": "slashing",
        "accuracy_bonus": 0,
        "preferred_row": FRONT,
        "ai_type": "aggressive",
        "xp_reward": 15, "gold_reward": (3, 8),
        "resistances": {
            "piercing": NEUTRAL, "slashing": NEUTRAL, "blunt": NEUTRAL,
            "fire": NEUTRAL, "ice": NEUTRAL, "lightning": NEUTRAL,
            "divine": NEUTRAL, "shadow": NEUTRAL, "nature": NEUTRAL,
            "arcane": NEUTRAL,
        },
        "status_immunities": [],
        "abilities": [],  # basic attack only
        "description_tiers": {
            0: "A small, snarling creature in crude leather.",
            1: "Goblin Warrior",
            2: "Goblin Warrior — weak but dangerous in numbers.",
        },
    },

    "Goblin Archer": {
        "name": "Goblin Archer",
        "hp": 14, "defense": 1, "magic_resist": 1,
        "stats": {"STR": 4, "DEX": 12, "CON": 4, "INT": 5, "WIS": 5, "PIE": 2},
        "speed_base": 16,
        "attack_damage": 6, "attack_type": "ranged", "phys_type": "piercing",
        "accuracy_bonus": 5,
        "preferred_row": MID,
        "ai_type": "aggressive",
        "xp_reward": 18, "gold_reward": (4, 10),
        "resistances": {
            "piercing": NEUTRAL, "slashing": NEUTRAL, "blunt": NEUTRAL,
            "fire": NEUTRAL, "ice": NEUTRAL, "lightning": NEUTRAL,
            "divine": NEUTRAL, "shadow": NEUTRAL, "nature": NEUTRAL,
            "arcane": NEUTRAL,
        },
        "status_immunities": [],
        "abilities": [],
        "description_tiers": {
            0: "A scrawny creature clutching a crude bow.",
            1: "Goblin Archer",
            2: "Goblin Archer — ranged attacker, fragile.",
        },
    },

    "Bandit": {
        "name": "Bandit",
        "hp": 30, "defense": 4, "magic_resist": 2,
        "stats": {"STR": 12, "DEX": 10, "CON": 10, "INT": 7, "WIS": 6, "PIE": 4},
        "speed_base": 16,
        "attack_damage": 9, "attack_type": "melee", "phys_type": "slashing",
        "accuracy_bonus": 2,
        "preferred_row": FRONT,
        "ai_type": "aggressive",
        "xp_reward": 30, "gold_reward": (8, 20),
        "resistances": {
            "piercing": NEUTRAL, "slashing": NEUTRAL, "blunt": NEUTRAL,
            "fire": NEUTRAL, "ice": NEUTRAL, "lightning": NEUTRAL,
            "divine": NEUTRAL, "shadow": NEUTRAL, "nature": NEUTRAL,
            "arcane": NEUTRAL,
        },
        "status_immunities": [],
        "abilities": [],
        "description_tiers": {
            0: "A rough-looking human with a scarred face.",
            1: "Bandit",
            2: "Bandit — standard melee fighter, moderate threat.",
        },
    },

    "Wolf": {
        "name": "Wolf",
        "hp": 22, "defense": 2, "magic_resist": 1,
        "stats": {"STR": 10, "DEX": 14, "CON": 8, "INT": 3, "WIS": 10, "PIE": 2},
        "speed_base": 22,
        "attack_damage": 8, "attack_type": "melee", "phys_type": "piercing",
        "accuracy_bonus": 5,
        "preferred_row": FRONT,
        "ai_type": "aggressive",
        "xp_reward": 22, "gold_reward": (0, 2),  # wolves don't carry gold
        "resistances": {
            "piercing": NEUTRAL, "slashing": NEUTRAL, "blunt": NEUTRAL,
            "fire": VULNERABLE, "ice": RESISTANT, "lightning": NEUTRAL,
            "divine": NEUTRAL, "shadow": NEUTRAL, "nature": RESISTANT,
            "arcane": NEUTRAL,
        },
        "status_immunities": [],
        "abilities": [],
        "description_tiers": {
            0: "A large grey predator with bared fangs.",
            1: "Wolf",
            2: "Wolf — fast, hits hard, hunts in packs.",
        },
    },

    "Skeleton Warrior": {
        "name": "Skeleton Warrior",
        "hp": 28, "defense": 6, "magic_resist": 3,
        "stats": {"STR": 10, "DEX": 8, "CON": 0, "INT": 2, "WIS": 4, "PIE": 0},
        "speed_base": 12,
        "attack_damage": 10, "attack_type": "melee", "phys_type": "slashing",
        "accuracy_bonus": 0,
        "preferred_row": FRONT,
        "ai_type": "defensive",
        "xp_reward": 35, "gold_reward": (5, 15),
        "resistances": {
            "piercing": RESISTANT, "slashing": RESISTANT, "blunt": VULNERABLE,
            "fire": NEUTRAL, "ice": RESISTANT, "lightning": NEUTRAL,
            "divine": VERY_VULNERABLE, "shadow": IMMUNE, "nature": NEUTRAL,
            "arcane": NEUTRAL,
        },
        "status_immunities": ["Poisoned", "Frostbitten", "Fear", "Sleep"],
        "abilities": [],
        "description_tiers": {
            0: "A shambling undead creature in rusted armor.",
            1: "Skeleton Warrior",
            2: "Skeleton Warrior — resistant to blades, weak to blunt and divine.",
        },
    },

    "Orc Fighter": {
        "name": "Orc Fighter",
        "hp": 45, "defense": 7, "magic_resist": 3,
        "stats": {"STR": 16, "DEX": 8, "CON": 14, "INT": 5, "WIS": 6, "PIE": 3},
        "speed_base": 13,
        "attack_damage": 14, "attack_type": "melee", "phys_type": "slashing",
        "accuracy_bonus": 0,
        "preferred_row": FRONT,
        "ai_type": "aggressive",
        "xp_reward": 50, "gold_reward": (10, 25),
        "resistances": {
            "piercing": NEUTRAL, "slashing": NEUTRAL, "blunt": NEUTRAL,
            "fire": NEUTRAL, "ice": NEUTRAL, "lightning": NEUTRAL,
            "divine": NEUTRAL, "shadow": NEUTRAL, "nature": NEUTRAL,
            "arcane": NEUTRAL,
        },
        "status_immunities": [],
        "abilities": [],
        "description_tiers": {
            0: "A hulking green-skinned brute in heavy armor.",
            1: "Orc Fighter",
            2: "Orc Fighter — tough, high damage, slow.",
        },
    },

    "Orc Chieftain": {
        "name": "Orc Chieftain",
        "hp": 80, "defense": 10, "magic_resist": 5,
        "stats": {"STR": 20, "DEX": 10, "CON": 18, "INT": 8, "WIS": 8, "PIE": 4},
        "speed_base": 14,
        "attack_damage": 18, "attack_type": "melee", "phys_type": "slashing",
        "accuracy_bonus": 5,
        "preferred_row": FRONT,
        "ai_type": "tactical",
        "xp_reward": 120, "gold_reward": (30, 60),
        "resistances": {
            "piercing": NEUTRAL, "slashing": NEUTRAL, "blunt": NEUTRAL,
            "fire": NEUTRAL, "ice": NEUTRAL, "lightning": NEUTRAL,
            "divine": NEUTRAL, "shadow": NEUTRAL, "nature": NEUTRAL,
            "arcane": NEUTRAL,
        },
        "status_immunities": ["Fear"],
        "abilities": [
            {"name": "War Cry", "type": "buff", "target": "all_allies",
             "effect": {"damage_boost": 1.2, "duration": 2},
             "description": "Rallies nearby orcs, boosting their damage."},
        ],
        "description_tiers": {
            0: "A massive warrior draped in trophies and scars.",
            1: "Orc Chieftain",
            2: "Orc Chieftain — boss-tier, rallies allies, hits very hard.",
        },
    },

    "Goblin Shaman": {
        "name": "Goblin Shaman",
        "hp": 16, "defense": 1, "magic_resist": 6,
        "stats": {"STR": 3, "DEX": 8, "CON": 4, "INT": 10, "WIS": 10, "PIE": 6},
        "speed_base": 14,
        "attack_damage": 4, "attack_type": "melee", "phys_type": "blunt",
        "accuracy_bonus": 0,
        "preferred_row": BACK,
        "ai_type": "tactical",
        "xp_reward": 35, "gold_reward": (5, 12),
        "resistances": {
            "piercing": NEUTRAL, "slashing": NEUTRAL, "blunt": NEUTRAL,
            "fire": NEUTRAL, "ice": NEUTRAL, "lightning": NEUTRAL,
            "divine": NEUTRAL, "shadow": NEUTRAL, "nature": RESISTANT,
            "arcane": NEUTRAL,
        },
        "status_immunities": [],
        "abilities": [
            {"name": "Heal", "type": "heal", "target": "single_ally",
             "power": 12,
             "description": "Mends wounds with crude nature magic."},
            {"name": "Poison Dart", "type": "damage", "target": "single_enemy",
             "power": 8, "element": "nature", "status": "Poisoned",
             "status_chance": 0.30, "status_duration": 3,
             "description": "Spits a venomous dart."},
        ],
        "description_tiers": {
            0: "A hunched figure muttering and waving a gnarled stick.",
            1: "Goblin Shaman",
            2: "Goblin Shaman — heals allies, casts poison. Priority target.",
        },
    },
}


# ═══════════════════════════════════════════════════════════════
#  ENCOUNTER TEMPLATES
# ═══════════════════════════════════════════════════════════════
#  Each encounter defines groups of enemies in rows.
#  Format: list of {"enemy": key, "count": N, "row": row}

ENCOUNTERS = {
    "easy_goblins": {
        "name": "Goblin Ambush",
        "difficulty": "easy",
        "groups": [
            {"enemy": "Goblin Warrior", "count": 3, "row": FRONT},
        ],
    },
    "medium_goblins": {
        "name": "Goblin Raiding Party",
        "difficulty": "medium",
        "groups": [
            {"enemy": "Goblin Warrior", "count": 3, "row": FRONT},
            {"enemy": "Goblin Archer", "count": 2, "row": MID},
        ],
    },
    "medium_bandits": {
        "name": "Bandit Ambush",
        "difficulty": "medium",
        "groups": [
            {"enemy": "Bandit", "count": 2, "row": FRONT},
            {"enemy": "Goblin Archer", "count": 1, "row": MID},
        ],
    },
    "wolves": {
        "name": "Wolf Pack",
        "difficulty": "medium",
        "groups": [
            {"enemy": "Wolf", "count": 4, "row": FRONT},
        ],
    },
    "hard_mixed": {
        "name": "Orc War Band",
        "difficulty": "hard",
        "groups": [
            {"enemy": "Orc Fighter", "count": 2, "row": FRONT},
            {"enemy": "Goblin Archer", "count": 3, "row": MID},
            {"enemy": "Goblin Shaman", "count": 1, "row": BACK},
        ],
    },
    "boss_orc": {
        "name": "Orc Chieftain's Guard",
        "difficulty": "boss",
        "groups": [
            {"enemy": "Orc Chieftain", "count": 1, "row": FRONT},
            {"enemy": "Orc Fighter", "count": 2, "row": FRONT},
            {"enemy": "Goblin Shaman", "count": 1, "row": BACK},
        ],
    },
    # Good first encounter — tutorial level
    "tutorial": {
        "name": "Roadside Goblins",
        "difficulty": "easy",
        "groups": [
            {"enemy": "Goblin Warrior", "count": 2, "row": FRONT},
            {"enemy": "Goblin Archer", "count": 1, "row": MID},
        ],
    },
}


def create_enemy_instance(enemy_key, uid):
    """Create a live enemy instance from template data.
    uid is a unique int for this specific enemy in the encounter."""
    template = ENEMIES[enemy_key]
    return {
        "uid": uid,
        "type": "enemy",
        "template_key": enemy_key,
        "name": template["name"],
        "hp": template["hp"],
        "max_hp": template["hp"],
        "defense": template["defense"],
        "magic_resist": template["magic_resist"],
        "stats": dict(template["stats"]),
        "speed_base": template["speed_base"],
        "attack_damage": template["attack_damage"],
        "attack_type": template["attack_type"],
        "phys_type": template["phys_type"],
        "accuracy_bonus": template["accuracy_bonus"],
        "row": template["preferred_row"],
        "ai_type": template["ai_type"],
        "resistances": dict(template["resistances"]),
        "status_immunities": list(template["status_immunities"]),
        "abilities": [dict(a) for a in template["abilities"]],
        "status_effects": [],
        "is_defending": False,
        "alive": True,
        "knowledge_tier": 0,
    }


def build_encounter(encounter_key):
    """Build a full encounter — returns list of enemy instances."""
    encounter = ENCOUNTERS[encounter_key]
    enemies = []
    uid = 0
    for group in encounter["groups"]:
        for _ in range(group["count"]):
            enemy = create_enemy_instance(group["enemy"], uid)
            enemy["row"] = group["row"]
            enemy["group_key"] = group["enemy"]  # for group targeting
            enemies.append(enemy)
            uid += 1
    return enemies, encounter["name"]
