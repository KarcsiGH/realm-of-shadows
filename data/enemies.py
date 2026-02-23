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
        "hp": 76, "defense": 5, "magic_resist": 2,
        "stats": {"STR": 6, "DEX": 10, "CON": 5, "INT": 4, "WIS": 4, "PIE": 2},
        "speed_base": 14,
        "attack_damage": 25, "attack_type": "melee", "phys_type": "slashing",
        "accuracy_bonus": 0,
        "preferred_row": FRONT,
        "ai_type": "aggressive",
        "xp_reward": 15, "gold_reward": (5, 12),
        "resistances": {
            "piercing": NEUTRAL, "slashing": NEUTRAL, "blunt": NEUTRAL,
            "fire": NEUTRAL, "ice": NEUTRAL, "lightning": NEUTRAL,
            "divine": NEUTRAL, "shadow": NEUTRAL, "nature": NEUTRAL,
            "arcane": NEUTRAL,
        },
        "status_immunities": [],
        "abilities": [],  # basic attack only
        "loot_table": [
            {"drop_chance": 0.15, "item": {
                "name": "Goblin Shiv", "type": "weapon",
                "subtype": "Dagger", "rarity": "common",
                "damage": 3, "phys_type": "piercing",
                "identify_difficulty": 1,
                "unidentified_name": "Crude Blade",
                "unidentified_desc": "A jagged piece of metal lashed to a bone handle.",
                "appraised_name": "Scrap Iron Shiv",
                "material_desc": "Scrap iron, crudely shaped. Barely worth the metal.",
                "magic_desc": "No magical properties.",
                "estimated_value": 4,
                "description": "A goblin-forged shiv. Crude but sharp enough to draw blood.",
            }},
            {"drop_chance": 0.12, "item": {
                "name": "Goblin Ear", "type": "material",
                "subtype": "trophy", "rarity": "common", "tier": 1,
                "identify_difficulty": 1,
                "unidentified_name": "Severed Ear",
                "unidentified_desc": "A small, pointed ear. Proof of a kill.",
                "appraised_name": "Goblin Ear",
                "material_desc": "A goblin trophy. Some bounty boards pay for these.",
                "magic_desc": "No magical properties.",
                "estimated_value": 2,
                "description": "A goblin ear. Worth a few coins at a bounty board.",
            }},
        ],
        "description_tiers": {
            0: "A small, snarling creature in crude leather.",
            1: "Goblin Warrior",
            2: "Goblin Warrior — weak but dangerous in numbers.",
        },
    },

    "Goblin Archer": {
        "name": "Goblin Archer",
        "hp": 57, "defense": 3, "magic_resist": 2,
        "stats": {"STR": 4, "DEX": 12, "CON": 4, "INT": 5, "WIS": 5, "PIE": 2},
        "speed_base": 16,
        "attack_damage": 28, "attack_type": "ranged", "phys_type": "piercing",
        "accuracy_bonus": 5,
        "preferred_row": MID,
        "ai_type": "aggressive",
        "xp_reward": 18, "gold_reward": (6, 14),
        "resistances": {
            "piercing": NEUTRAL, "slashing": NEUTRAL, "blunt": NEUTRAL,
            "fire": NEUTRAL, "ice": NEUTRAL, "lightning": NEUTRAL,
            "divine": NEUTRAL, "shadow": NEUTRAL, "nature": NEUTRAL,
            "arcane": NEUTRAL,
        },
        "status_immunities": [],
        "abilities": [],
        "loot_table": [
            {"drop_chance": 0.12, "item": {
                "name": "Crude Shortbow", "type": "weapon",
                "subtype": "Shortbow", "rarity": "common",
                "damage": 4, "phys_type": "piercing",
                "identify_difficulty": 1,
                "unidentified_name": "Worn Shortbow",
                "unidentified_desc": "A small bow made from a bent branch and sinew string.",
                "appraised_name": "Crude Wooden Shortbow",
                "material_desc": "Cheap wood, poorly shaped. Might snap under heavy use.",
                "magic_desc": "No magical properties.",
                "estimated_value": 5,
                "description": "A goblin-made shortbow. Flimsy but functional.",
            }},
            {"drop_chance": 0.15, "item": {
                "name": "Bundle of Crude Arrows", "type": "consumable",
                "subtype": "ammunition", "rarity": "common",
                "identify_difficulty": 1,
                "unidentified_name": "Handful of Arrows",
                "unidentified_desc": "A bundle of crooked arrows with chipped stone tips.",
                "appraised_name": "Crude Stone-Tipped Arrows",
                "material_desc": "Stone arrowheads on warped shafts. Better than nothing.",
                "magic_desc": "No magical properties.",
                "estimated_value": 3,
                "description": "Goblin arrows. Inaccurate but they still hurt.",
            }},
        ],
        "description_tiers": {
            0: "A scrawny creature clutching a crude bow.",
            1: "Goblin Archer",
            2: "Goblin Archer — ranged attacker, fragile.",
        },
    },

    "Bandit": {
        "name": "Bandit",
        "hp": 114, "defense": 10, "magic_resist": 4,
        "stats": {"STR": 12, "DEX": 10, "CON": 10, "INT": 7, "WIS": 6, "PIE": 4},
        "speed_base": 16,
        "attack_damage": 28, "attack_type": "melee", "phys_type": "slashing",
        "accuracy_bonus": 2,
        "preferred_row": FRONT,
        "ai_type": "aggressive",
        "xp_reward": 30, "gold_reward": (10, 25),
        "resistances": {
            "piercing": NEUTRAL, "slashing": NEUTRAL, "blunt": NEUTRAL,
            "fire": NEUTRAL, "ice": NEUTRAL, "lightning": NEUTRAL,
            "divine": NEUTRAL, "shadow": NEUTRAL, "nature": NEUTRAL,
            "arcane": NEUTRAL,
        },
        "status_immunities": [],
        "abilities": [],
        "loot_table": [
            {"drop_chance": 0.12, "item": {
                "name": "Bandit's Shortsword", "type": "weapon",
                "subtype": "Short Sword", "rarity": "common",
                "damage": 6, "phys_type": "slashing",
                "identify_difficulty": 1,
                "unidentified_name": "Worn Short Sword",
                "unidentified_desc": "A short blade with a leather-wrapped grip. Well-used but serviceable.",
                "appraised_name": "Decent Steel Short Sword",
                "material_desc": "Common steel, mass-forged. Nothing special about the make.",
                "magic_desc": "No magical properties detected.",
                "estimated_value": 12,
                "description": "A well-used blade with nicks along the edge. Carried by a bandit who won't need it anymore.",
            }},
            {"drop_chance": 0.12, "item": {
                "name": "Leather Scraps", "type": "material",
                "subtype": "leather", "rarity": "common", "tier": 1,
                "identify_difficulty": 1,
                "unidentified_name": "Leather Scraps",
                "unidentified_desc": "Rough pieces of leather, cut from worn armor.",
                "appraised_name": "Boiled Leather Scraps",
                "material_desc": "Low-grade boiled leather. Tier 1 crafting material.",
                "magic_desc": "No magical properties.",
                "estimated_value": 3,
                "description": "Rough leather that could be useful for crafting.",
            }},
        ],
        "description_tiers": {
            0: "A rough-looking human with a scarred face.",
            1: "Bandit",
            2: "Bandit — standard melee fighter, moderate threat.",
        },
    },

    "Wolf": {
        "name": "Wolf",
        "hp": 85, "defense": 5, "magic_resist": 2,
        "stats": {"STR": 10, "DEX": 14, "CON": 8, "INT": 3, "WIS": 10, "PIE": 2},
        "speed_base": 22,
        "attack_damage": 32, "attack_type": "melee", "phys_type": "piercing",
        "accuracy_bonus": 5,
        "preferred_row": FRONT,
        "ai_type": "aggressive",
        "xp_reward": 22, "gold_reward": (2, 6),  # wolves carry some scraps
        "resistances": {
            "piercing": NEUTRAL, "slashing": NEUTRAL, "blunt": NEUTRAL,
            "fire": VULNERABLE, "ice": RESISTANT, "lightning": NEUTRAL,
            "divine": NEUTRAL, "shadow": NEUTRAL, "nature": RESISTANT,
            "arcane": NEUTRAL,
        },
        "status_immunities": [],
        "abilities": [],
        "loot_table": [
            {"drop_chance": 0.15, "item": {
                "name": "Wolf Pelt", "type": "material",
                "subtype": "leather", "rarity": "common", "tier": 1,
                "identify_difficulty": 1,
                "unidentified_name": "Animal Pelt",
                "unidentified_desc": "A thick grey pelt, still warm from the kill.",
                "appraised_name": "Wolf Pelt",
                "material_desc": "Good-quality wolf hide. Tier 1 leather, suitable for light armor crafting.",
                "magic_desc": "No magical properties.",
                "estimated_value": 15,
                "description": "A thick grey pelt, still warm. Useful for crafting leather armor.",
            }},
            {"drop_chance": 0.08, "item": {
                "name": "Wolf Fang", "type": "material",
                "subtype": "reagent", "rarity": "common", "tier": 1,
                "identify_difficulty": 1,
                "unidentified_name": "Large Fang",
                "unidentified_desc": "A sharp canine tooth, about the length of a finger.",
                "appraised_name": "Wolf Fang",
                "material_desc": "A predator's tooth. Tier 1 reagent for weapon enchanting or potion brewing.",
                "magic_desc": "Faint natural essence — could hold a minor enchantment.",
                "estimated_value": 10,
                "description": "A sharp canine tooth. Useful for crafting and enchanting.",
            }},
        ],
        "description_tiers": {
            0: "A large grey predator with bared fangs.",
            1: "Wolf",
            2: "Wolf — fast, hits hard, hunts in packs.",
        },
    },

    "Skeleton Warrior": {
        "name": "Skeleton Warrior",
        "hp": 105, "defense": 15, "magic_resist": 6,
        "stats": {"STR": 10, "DEX": 8, "CON": 0, "INT": 2, "WIS": 4, "PIE": 0},
        "speed_base": 12,
        "attack_damage": 28, "attack_type": "melee", "phys_type": "slashing",
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
        "hp": 168, "defense": 17, "magic_resist": 6,
        "stats": {"STR": 16, "DEX": 8, "CON": 14, "INT": 5, "WIS": 6, "PIE": 3},
        "speed_base": 13,
        "attack_damage": 51, "attack_type": "melee", "phys_type": "slashing",
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
        "loot_table": [
            {"drop_chance": 0.08, "item": {
                "name": "Orcish Blade", "type": "weapon",
                "subtype": "Broadsword", "rarity": "common",
                "damage": 9, "phys_type": "slashing",
                "identify_difficulty": 1,
                "unidentified_name": "Crude Broadsword",
                "unidentified_desc": "A heavy iron blade with rough hammer marks. Brutally functional.",
                "appraised_name": "Orcish Iron Broadsword",
                "material_desc": "Crude orcish ironwork. Heavy but effective. Poor resale value.",
                "magic_desc": "No magical properties.",
                "estimated_value": 15,
                "description": "A crude but heavy iron blade favored by orc warriors.",
            }},
            {"drop_chance": 0.05, "item": {
                "name": "Orc Hide Scraps", "type": "material",
                "subtype": "leather", "rarity": "common", "tier": 1,
                "identify_difficulty": 1,
                "unidentified_name": "Thick Hide Scraps",
                "unidentified_desc": "Pieces of unusually thick, green-tinged hide.",
                "appraised_name": "Orc Hide Scraps",
                "material_desc": "Tough orc skin. Tier 1 leather, excellent for heavy padding.",
                "magic_desc": "No magical properties.",
                "estimated_value": 5,
                "description": "Thick green hide, tough as boiled leather.",
            }},
        ],
        "description_tiers": {
            0: "A hulking green-skinned brute in heavy armor.",
            1: "Orc Fighter",
            2: "Orc Fighter — tough, high damage, slow.",
        },
    },

    "Orc Chieftain": {
        "name": "Orc Chieftain",
        "hp": 270, "defense": 25, "magic_resist": 10,
        "stats": {"STR": 20, "DEX": 10, "CON": 18, "INT": 8, "WIS": 8, "PIE": 4},
        "speed_base": 14,
        "attack_damage": 64, "attack_type": "melee", "phys_type": "slashing",
        "accuracy_bonus": 5,
        "preferred_row": FRONT,
        "ai_type": "boss",
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
        "loot_table": [
            {"drop_chance": 0.25, "item": {
                "name": "Chieftain's Cleaver", "type": "weapon",
                "subtype": "Broadsword", "rarity": "uncommon",
                "damage": 12, "phys_type": "slashing",
                "enhance_bonus": 1, "effect": {"str_bonus": 1},
                "identify_difficulty": 2,
                "unidentified_name": "Ornate Broadsword",
                "unidentified_desc": "A massive jagged blade with crude etchings along the fuller. Faintly warm to the touch.",
                "appraised_name": "Masterwork Orcish Broadsword",
                "material_desc": "Superior orcish steel, forged by a skilled weaponsmith. Rare quality for orc work.",
                "magic_desc": "+1 enhancement. Faint enchantment boosts the wielder's strength.",
                "estimated_value": 120,
                "description": "A massive jagged blade imbued with orcish battle rage. +1 enhancement, +1 STR when equipped.",
            }},
            {"drop_chance": 0.05, "item": {
                "name": "Orcish War Totem", "type": "accessory",
                "subtype": "trinket", "rarity": "uncommon",
                "effect": {"str_bonus": 2},
                "identify_difficulty": 3,
                "unidentified_name": "Bone Totem",
                "unidentified_desc": "A small totem carved from thick bone, etched with crude symbols.",
                "appraised_name": "Orcish Bone Totem",
                "material_desc": "Carved from troll bone — rare material. Ceremonial significance to orc clans.",
                "magic_desc": "Imbued with a war blessing. Grants +2 STR while carried.",
                "estimated_value": 200,
                "description": "A bone totem etched with crude symbols of power. +2 STR when equipped.",
            }},
            {"drop_chance": 0.12, "item": {
                "name": "Chieftain's Trophy Pouch", "type": "consumable",
                "subtype": "gold_pouch", "rarity": "common",
                "bonus_gold": 50,
                "identify_difficulty": 1,
                "unidentified_name": "Heavy Leather Pouch",
                "unidentified_desc": "A bulging leather pouch that clinks when shaken.",
                "appraised_name": "Coin Pouch (substantial)",
                "material_desc": "Contains roughly 50 gold worth of mixed coins and small valuables.",
                "magic_desc": "No magical properties.",
                "estimated_value": 50,
                "description": "A leather pouch stuffed with coins and trinkets worth about 50 gold.",
            }},
        ],
        "description_tiers": {
            0: "A massive warrior draped in trophies and scars.",
            1: "Orc Chieftain",
            2: "Orc Chieftain — boss-tier, rallies allies, hits very hard.",
        },
    },

    "Goblin Shaman": {
        "name": "Goblin Shaman",
        "hp": 66, "defense": 3, "magic_resist": 12,
        "stats": {"STR": 3, "DEX": 8, "CON": 4, "INT": 10, "WIS": 10, "PIE": 6},
        "speed_base": 14,
        "attack_damage": 16, "attack_type": "melee", "phys_type": "blunt",
        "accuracy_bonus": 0,
        "preferred_row": BACK,
        "ai_type": "supportive",
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
        "loot_table": [
            {"drop_chance": 0.08, "item": {
                "name": "Shaman's Herb Pouch", "type": "consumable",
                "subtype": "potion_ingredient", "rarity": "common", "tier": 1,
                "identify_difficulty": 1,
                "unidentified_name": "Dried Herb Pouch",
                "unidentified_desc": "A small leather pouch filled with dried plant matter. Pungent smell.",
                "appraised_name": "Medicinal Herb Bundle",
                "material_desc": "Mixed healing herbs. Tier 1 potion ingredient, enough for one basic potion.",
                "magic_desc": "Faint restorative essence. Suitable for brewing healing potions.",
                "estimated_value": 8,
                "description": "A pouch of dried herbs with a pungent smell. Useful for brewing healing potions.",
            }},
            {"drop_chance": 0.05, "item": {
                "name": "Crude Wand", "type": "weapon",
                "subtype": "Wand", "rarity": "common",
                "spell_bonus": 2,
                "identify_difficulty": 2,
                "unidentified_name": "Gnarled Stick",
                "unidentified_desc": "A twisted twig wrapped in leather strips. It tingles slightly when held.",
                "appraised_name": "Goblin Focus Wand",
                "material_desc": "Swamp oak wrapped in lizard leather. Crude but functional focus implement.",
                "magic_desc": "Channeling focus. Grants +2 to spell power when casting.",
                "estimated_value": 35,
                "description": "A gnarled twig wrapped in leather strips. +2 spell bonus when used as a focus.",
            }},
        ],
        "description_tiers": {
            0: "A hunched figure muttering and waving a gnarled stick.",
            1: "Goblin Shaman",
            2: "Goblin Shaman — heals allies, casts poison. Priority target.",
        },
    },

    # ═══════════════════════════════════════════════════════════
    #  BOSS ENEMIES
    # ═══════════════════════════════════════════════════════════

    "Goblin King": {
        "name": "Grak the Goblin King",
        "hp": 400, "defense": 12, "magic_resist": 8,
        "stats": {"STR": 18, "DEX": 10, "CON": 16, "INT": 6, "WIS": 8, "PIE": 4},
        "speed_base": 12,
        "attack_damage": 38, "attack_type": "melee", "phys_type": "blunt",
        "accuracy_bonus": 8,
        "preferred_row": FRONT,
        "ai_type": "boss",
        "xp_reward": 200, "gold_reward": (80, 150),
        "resistances": {
            "piercing": NEUTRAL, "slashing": NEUTRAL, "blunt": RESISTANT,
            "fire": VULNERABLE, "ice": NEUTRAL, "lightning": NEUTRAL,
            "divine": NEUTRAL, "shadow": NEUTRAL, "nature": NEUTRAL,
            "arcane": NEUTRAL,
        },
        "status_immunities": ["stun"],
        "abilities": ["Goblin King Smash", "Enrage"],
        "loot_table": [
            {"drop_chance": 1.0, "item": {
                "name": "Goblin King's Crown", "type": "armor", "subtype": "helmet",
                "rarity": "rare", "tier": 2, "defense": 12, "identified": False,
                "appraised_name": "Goblin King's Crown",
                "estimated_value": 200,
                "description": "A crude crown of bent metal and stolen gems. "
                               "+12 DEF. Surprisingly well-made for goblin craftsmanship.",
            }},
            {"drop_chance": 0.60, "item": {
                "name": "Goblin King's Coin", "type": "accessory", "subtype": "trinket",
                "rarity": "uncommon", "tier": 2, "identified": False,
                "appraised_name": "Goblin King's Lucky Coin",
                "estimated_value": 120,
                "stat_bonus": {"LCK": 2},
                "description": "A battered gold coin Grak carried for luck. +2 LCK.",
            }},
        ],
        "description_tiers": {
            0: "A massive goblin in crude armor, wielding an enormous club.",
            1: "Grak the Goblin King",
            2: "Grak — Boss. Heavy hitter, can enrage. Weak to fire.",
        },
    },

    "Giant Spider Queen": {
        "name": "Spider Queen",
        "hp": 480, "defense": 20, "magic_resist": 20,
        "stats": {"STR": 14, "DEX": 18, "CON": 14, "INT": 4, "WIS": 12, "PIE": 2},
        "speed_base": 18,
        "attack_damage": 41, "attack_type": "melee", "phys_type": "piercing",
        "accuracy_bonus": 12,
        "preferred_row": FRONT,
        "ai_type": "boss",
        "xp_reward": 220, "gold_reward": (60, 120),
        "resistances": {
            "piercing": RESISTANT, "slashing": NEUTRAL, "blunt": VULNERABLE,
            "fire": VERY_VULNERABLE, "ice": NEUTRAL, "lightning": NEUTRAL,
            "divine": NEUTRAL, "shadow": RESISTANT, "nature": IMMUNE,
            "arcane": NEUTRAL,
        },
        "status_immunities": ["poison"],
        "abilities": ["Poison Cloud"],
        "loot_table": [
            {"drop_chance": 0.80, "item": {
                "name": "Spider Silk Mantle", "type": "armor", "subtype": "cloak",
                "rarity": "rare", "tier": 2, "defense": 7, "magic_resist": 8, "identified": True,
                "estimated_value": 180,
                "description": "A shimmering cloak woven from spider silk. Light and magically resistant.",
            }},
        ],
        "description_tiers": {
            0: "A massive arachnid, dripping venom from its fangs.",
            1: "Spider Queen",
            2: "Spider Queen — Boss. Poison cloud, fast. Weak to fire and blunt.",
        },
    },

    "Undead Foreman": {
        "name": "The Foreman",
        "hp": 450, "defense": 37, "magic_resist": 24,
        "stats": {"STR": 20, "DEX": 8, "CON": 22, "INT": 10, "WIS": 14, "PIE": 2},
        "speed_base": 8,
        "attack_damage": 60, "attack_type": "melee", "phys_type": "blunt",
        "accuracy_bonus": 6,
        "preferred_row": FRONT,
        "ai_type": "boss",
        "xp_reward": 300, "gold_reward": (100, 200),
        "resistances": {
            "piercing": RESISTANT, "slashing": NEUTRAL, "blunt": VULNERABLE,
            "fire": VULNERABLE, "ice": RESISTANT, "lightning": NEUTRAL,
            "divine": VERY_VULNERABLE, "shadow": IMMUNE, "nature": NEUTRAL,
            "arcane": NEUTRAL,
        },
        "status_immunities": ["poison", "stun", "fear"],
        "abilities": ["Skull Crush", "Enrage"],
        "loot_table": [
            {"drop_chance": 0.80, "item": {
                "name": "Foreman's Pickaxe", "type": "weapon", "subtype": "axe",
                "rarity": "rare", "tier": 3, "damage": 22, "identified": True,
                "estimated_value": 250,
                "description": "A massive mining pick, still sharp after centuries. +22 base damage.",
            }},
        ],
        "description_tiers": {
            0: "A towering undead figure in tattered work clothes, clutching a massive pickaxe.",
            1: "The Foreman",
            2: "The Foreman — Boss. Undead. Slow but devastating. Weak to divine and fire.",
        },
    },

    "Giant Spider": {
        "name": "Giant Spider",
        "hp": 84, "defense": 10, "magic_resist": 6,
        "stats": {"STR": 10, "DEX": 16, "CON": 8, "INT": 2, "WIS": 8, "PIE": 1},
        "speed_base": 20,
        "attack_damage": 25, "attack_type": "melee", "phys_type": "piercing",
        "accuracy_bonus": 8,
        "preferred_row": FRONT,
        "ai_type": "aggressive",
        "xp_reward": 30, "gold_reward": (2, 5),
        "resistances": {
            "piercing": NEUTRAL, "slashing": NEUTRAL, "blunt": NEUTRAL,
            "fire": VULNERABLE, "ice": NEUTRAL, "lightning": NEUTRAL,
            "divine": NEUTRAL, "shadow": NEUTRAL, "nature": RESISTANT,
            "arcane": NEUTRAL,
        },
        "status_immunities": [],
        "abilities": [],
        "loot_table": [
            {"drop_chance": 0.12, "item": {
                "name": "Spider Silk", "type": "material", "subtype": "cloth",
                "rarity": "common", "tier": 1, "estimated_value": 12, "identified": True,
                "description": "Tough, lightweight silk from a giant spider.",
            }},
        ],
        "description_tiers": {0: "A dog-sized spider.", 1: "Giant Spider", 2: "Giant Spider — fast, venomous."},
    },
}
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
        "name": "Roadside Ambush",
        "difficulty": "easy",
        "groups": [
            {"enemy": "Goblin Warrior", "count": 2, "row": FRONT},
            {"enemy": "Goblin Archer", "count": 1, "row": MID},
            {"enemy": "Bandit", "count": 1, "row": FRONT},
        ],
    },
    # Boss encounters
    "boss_goblin_king": {
        "name": "Grak the Goblin King",
        "difficulty": "boss",
        "groups": [
            {"enemy": "Goblin King", "count": 1, "row": FRONT},
            {"enemy": "Goblin Warrior", "count": 2, "row": FRONT},
            {"enemy": "Goblin Shaman", "count": 1, "row": BACK},
        ],
    },
    "boss_spider_queen": {
        "name": "Spider Queen's Lair",
        "difficulty": "boss",
        "groups": [
            {"enemy": "Giant Spider Queen", "count": 1, "row": FRONT},
            {"enemy": "Giant Spider", "count": 3, "row": FRONT},
        ],
    },
    "boss_foreman": {
        "name": "The Foreman's Chamber",
        "difficulty": "boss",
        "groups": [
            {"enemy": "Undead Foreman", "count": 1, "row": FRONT},
            {"enemy": "Skeleton Warrior", "count": 2, "row": FRONT},
        ],
    },
    # Harder regular encounters for deeper floors
    "hard_goblins": {
        "name": "Goblin War Party",
        "difficulty": "hard",
        "groups": [
            {"enemy": "Goblin Warrior", "count": 4, "row": FRONT},
            {"enemy": "Goblin Archer", "count": 2, "row": MID},
            {"enemy": "Goblin Shaman", "count": 1, "row": BACK},
        ],
    },
    "orc_patrol": {
        "name": "Orc Patrol",
        "difficulty": "hard",
        "groups": [
            {"enemy": "Orc Fighter", "count": 3, "row": FRONT},
        ],
    },
    "spider_swarm": {
        "name": "Spider Swarm",
        "difficulty": "medium",
        "groups": [
            {"enemy": "Giant Spider", "count": 5, "row": FRONT},
        ],
    },
}


# ═══════════════════════════════════════════════════════════════
#  FLOOR-BASED ENCOUNTER SCALING
# ═══════════════════════════════════════════════════════════════

DUNGEON_ENCOUNTER_TABLES = {
    "goblin_warren": {
        1: ["easy_goblins", "medium_goblins", "wolves"],
        2: ["medium_goblins", "hard_goblins", "medium_bandits"],
        3: ["hard_goblins", "hard_mixed"],
        "boss": "boss_goblin_king",
    },
    "spiders_nest": {
        1: ["spider_swarm", "wolves"],
        2: ["spider_swarm", "medium_bandits"],
        3: ["spider_swarm", "hard_mixed"],
        "boss": "boss_spider_queen",
    },
    "abandoned_mine": {
        1: ["medium_goblins", "medium_bandits"],
        2: ["hard_mixed", "orc_patrol"],
        3: ["orc_patrol", "hard_mixed"],
        "boss": "boss_foreman",
    },
    "sunken_crypt": {
        1: ["hard_goblins", "hard_mixed"],
        2: ["hard_mixed", "orc_patrol"],
        3: ["boss_orc", "orc_patrol"],
        "boss": "boss_foreman",  # reuse until more bosses
    },
    "ruins_ashenmoor": {
        1: ["hard_mixed", "orc_patrol"],
        2: ["boss_orc", "orc_patrol"],
        3: ["boss_orc", "orc_patrol"],
        "boss": "boss_foreman",
    },
}

def get_floor_encounter(dungeon_id, floor_num, total_floors, is_boss_floor=False):
    """Get a random encounter key appropriate for this dungeon floor."""
    import random
    table = DUNGEON_ENCOUNTER_TABLES.get(dungeon_id)
    if not table:
        return "medium_goblins"

    if is_boss_floor or floor_num >= total_floors:
        return table.get("boss", "hard_mixed")

    floor_table = table.get(floor_num, table.get(1, ["medium_goblins"]))
    return random.choice(floor_table)


def create_enemy_instance(enemy_key, uid):
    """Create a live enemy instance from template data.
    uid is a unique int for this specific enemy in the encounter."""
    from core.abilities import ENEMY_ABILITIES
    template = ENEMIES[enemy_key]

    # Resolve ability references (strings → dicts)
    abilities = []
    for a in template.get("abilities", []):
        if isinstance(a, str):
            ab_def = ENEMY_ABILITIES.get(a)
            if ab_def:
                abilities.append(dict(ab_def))
        elif isinstance(a, dict):
            abilities.append(dict(a))

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
        "preferred_row": template["preferred_row"],
        "ai_type": template.get("ai_type", "balanced"),
        "resistances": dict(template["resistances"]),
        "status_immunities": list(template.get("status_immunities", [])),
        "abilities": abilities,
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


# ═══════════════════════════════════════════════════════════════
#  M9 EXPANDED BESTIARY — merge new enemies, encounters, tables
# ═══════════════════════════════════════════════════════════════

from data.bestiary_m9 import (
    NEW_ENEMIES, NEW_ENCOUNTERS,
    NEW_DUNGEON_ENCOUNTER_TABLES, NEW_ENCOUNTER_ZONES,
    NEW_ENEMY_ABILITIES,
)

ENEMIES.update(NEW_ENEMIES)
ENCOUNTERS.update(NEW_ENCOUNTERS)
DUNGEON_ENCOUNTER_TABLES.update(NEW_DUNGEON_ENCOUNTER_TABLES)

# Merge new enemy abilities into core.abilities
try:
    from core.abilities import ENEMY_ABILITIES
    ENEMY_ABILITIES.update(NEW_ENEMY_ABILITIES)
except ImportError:
    pass

# ── Tower dungeon (Valdris' Spire) ──
try:
    from data.tower_data import (
        TOWER_ENEMIES, TOWER_ENCOUNTERS, TOWER_ENCOUNTER_TABLE,
        TOWER_BOSS_LOOT,
    )
    ENEMIES.update(TOWER_ENEMIES)
    ENCOUNTERS.update(TOWER_ENCOUNTERS)
    DUNGEON_ENCOUNTER_TABLES.update(TOWER_ENCOUNTER_TABLE)

    # Add tower boss loot to magic_items
    try:
        from data.magic_items import BOSS_BONUS_LOOT
        BOSS_BONUS_LOOT.update(TOWER_BOSS_LOOT)
    except ImportError:
        pass
except ImportError:
    pass
