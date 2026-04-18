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
        "hp": 70, "defense": 5, "magic_resist": 2,
        "stats": {"STR": 6, "DEX": 10, "CON": 5, "INT": 4, "WIS": 4, "PIE": 2},
        "speed_base": 14,
        "attack_damage": 18, "attack_type": "melee", "phys_type": "slashing",
        "accuracy_bonus": 0,
        "preferred_row": FRONT,
        "ai_type": "aggressive", "pack_tactics": True, "cowardly": True,
        "xp_reward": 22, "gold_reward": (5, 12),
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
                "damage": 13, "phys_type": "piercing",
                "damage_stat": {"DEX": 0.4},
                "identify_difficulty": 1,
                "unidentified_name": "Crude Blade",
                "unidentified_desc": "A jagged piece of metal lashed to a bone handle.",
                "appraised_name": "Scrap Iron Shiv",
                "material_desc": "Scrap iron, crudely shaped. Barely worth the metal.",
                "magic_desc": "No magical properties.",
                "estimated_value": 55,
                "description": "A goblin-forged shiv. Crude but sharp enough to draw blood.",
            }},
            {"drop_chance": 0.35, "item": {
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
        "hp": 48, "defense": 2, "magic_resist": 2,
        "stats": {"STR": 4, "DEX": 12, "CON": 4, "INT": 5, "WIS": 5, "PIE": 2},
        "speed_base": 16,
        "attack_damage": 14, "attack_type": "ranged", "phys_type": "piercing",
        "accuracy_bonus": 5,
        "preferred_row": MID,
        "ai_type": "aggressive", "pack_tactics": True, "cowardly": True,
        "xp_reward": 27, "gold_reward": (6, 14),
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
                "damage": 14, "phys_type": "piercing",
                "damage_stat": {"DEX": 0.35, "STR": 0.08},
                "identify_difficulty": 1,
                "unidentified_name": "Worn Shortbow",
                "unidentified_desc": "A small bow made from a bent branch and sinew string.",
                "appraised_name": "Crude Wooden Shortbow",
                "material_desc": "Cheap wood, poorly shaped. Might snap under heavy use.",
                "magic_desc": "No magical properties.",
                "estimated_value": 50,
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
        "xp_reward": 60, "gold_reward": (10, 25),
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
                "damage": 16, "phys_type": "slashing",
                "damage_stat": {"DEX": 0.28, "STR": 0.12},
                "identify_difficulty": 1,
                "unidentified_name": "Worn Short Sword",
                "unidentified_desc": "A short blade with a leather-wrapped grip. Well-used but serviceable.",
                "appraised_name": "Decent Steel Short Sword",
                "material_desc": "Common steel, mass-forged. Nothing special about the make.",
                "magic_desc": "No magical properties detected.",
                "estimated_value": 80,
                "description": "A well-used blade with nicks along the edge. Carried by a bandit who won't need it anymore.",
            }},
            {"drop_chance": 0.30, "item": {
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
        "hp": 55, "defense": 3, "magic_resist": 1,
        "stats": {"STR": 10, "DEX": 14, "CON": 8, "INT": 3, "WIS": 10, "PIE": 2},
        "speed_base": 22,
        "attack_damage": 16, "attack_type": "melee", "phys_type": "piercing",
        "accuracy_bonus": 5,
        "preferred_row": FRONT,
        "ai_type": "aggressive", "pack_tactics": True,
        "xp_reward": 33, "gold_reward": (2, 6),  # wolves carry some scraps
        "resistances": {
            "piercing": NEUTRAL, "slashing": NEUTRAL, "blunt": NEUTRAL,
            "fire": VULNERABLE, "ice": RESISTANT, "lightning": NEUTRAL,
            "divine": NEUTRAL, "shadow": NEUTRAL, "nature": RESISTANT,
            "arcane": NEUTRAL,
        },
        "status_immunities": [],
        "abilities": [],
        "loot_table": [
            {"drop_chance": 0.38, "item": {
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
            {"drop_chance": 0.22, "item": {
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

    "Stone Sentinel": {
        "name": "Stone Sentinel",
        "hp": 180, "defense": 28, "magic_resist": 12,
        "stats": {"STR": 16, "DEX": 4, "CON": 20, "INT": 4, "WIS": 8, "PIE": 2},
        "speed_base": 5,
        "attack_damage": 38, "attack_type": "melee", "phys_type": "blunt",
        "accuracy_bonus": 4,
        "preferred_row": FRONT,
        "ai_type": "defensive",
        "xp_reward": 80, "gold_reward": (10, 25),
        "resistances": {
            "piercing": RESISTANT, "slashing": RESISTANT, "blunt": NEUTRAL,
            "fire": NEUTRAL, "ice": NEUTRAL, "lightning": RESISTANT,
            "divine": NEUTRAL, "shadow": RESISTANT, "nature": NEUTRAL,
            "arcane": VULNERABLE,
        },
        "status_immunities": ["poison", "stun", "fear", "charm", "sleep"],
        "abilities": [],
        "loot_table": [
            {"drop_chance": 0.30, "item": {
                "name": "Ward-Carved Stone", "type": "material",
                "rarity": "uncommon", "identified": True,
                "estimated_value": 45,
                "description": "A piece of stone etched with fading warden runes. Used in crafting.",
            }},
        ],
        "description_tiers": {
            0: "A hulking construct of stone and ancient rune-work, animated by dwarven warden magic.",
            1: "Stone Sentinel",
            2: "Stone Sentinel — Dwarven construct. Slow but heavily armored. "
               "Resistant to blades and lightning. Arcane magic bypasses its defenses.",
        },
    },

    "Ash Revenant": {
        "name": "Ash Revenant",
        "hp": 145, "defense": 18, "magic_resist": 20,
        "stats": {"STR": 14, "DEX": 12, "CON": 16, "INT": 10, "WIS": 8, "PIE": 2},
        "speed_base": 14,
        "attack_damage": 32, "attack_type": "melee", "phys_type": "slashing",
        "accuracy_bonus": 6,
        "preferred_row": MID,
        "ai_type": "aggressive",
        "xp_reward": 70, "gold_reward": (15, 30),
        "resistances": {
            "piercing": NEUTRAL, "slashing": NEUTRAL, "blunt": NEUTRAL,
            "fire": IMMUNE, "ice": NEUTRAL, "lightning": NEUTRAL,
            "divine": VULNERABLE, "shadow": RESISTANT, "nature": NEUTRAL,
            "arcane": NEUTRAL,
        },
        "status_immunities": ["poison", "burn", "fear"],
        "tags": ["undead"],
        "abilities": ["Cinder Touch"],
        "loot_table": [
            {"drop_chance": 0.35, "item": {
                "name": "Ashenmoor Cinder", "type": "material",
                "rarity": "uncommon", "identified": True,
                "estimated_value": 38,
                "description": "Ash compacted into a dense, still-warm lump. Reeks of old magic.",
            }},
        ],
        "description_tiers": {
            0: "A humanoid shape woven from compressed ash and fading shadow energy, "
               "hollow where its eyes should be.",
            1: "Ash Revenant",
            2: "Ash Revenant — Undead. Immune to fire. Weak to divine. "
               "Moderate speed, hits at range. Cinder Touch inflicts Burning.",
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
        "xp_reward": 70, "gold_reward": (5, 15),
        "resistances": {
            "piercing": RESISTANT, "slashing": RESISTANT, "blunt": VULNERABLE,
            "fire": NEUTRAL, "ice": RESISTANT, "lightning": NEUTRAL,
            "divine": VERY_VULNERABLE, "shadow": IMMUNE, "nature": NEUTRAL,
            "arcane": NEUTRAL,
        },
        "status_immunities": ["Poisoned", "Frostbitten", "Fear", "Sleep"],
        "tags": ["undead"],
        "abilities": [],
        "loot_table": [
            {"drop_chance": 0.18, "item": {
                "name": "Rusted Sword", "type": "weapon",
                "subtype": "Short Sword", "rarity": "common",
                "damage": 15, "phys_type": "slashing",
                "damage_stat": {"DEX": 0.28, "STR": 0.12},
                "identify_difficulty": 1,
                "unidentified_name": "Corroded Blade",
                "unidentified_desc": "A blade pitted with rust, still holding an edge.",
                "appraised_name": "Rusted Grave Sword",
                "material_desc": "Old iron, badly corroded. Still functional if sharpened.",
                "magic_desc": "Faint traces of old enchantment — long since faded.",
                "estimated_value": 55,
                "description": "A sword reclaimed from a skeleton. Pitted with rust but serviceable.",
            }},
            {"drop_chance": 0.20, "item": {
                "name": "Bone Fragment", "type": "material",
                "subtype": "reagent", "rarity": "common", "tier": 1,
                "identify_difficulty": 1,
                "unidentified_name": "Bone Shard",
                "unidentified_desc": "A piece of old bone, hollow and light.",
                "appraised_name": "Undead Bone Fragment",
                "material_desc": "Bone from an animated skeleton. Tier 1 reagent for necromantic crafting.",
                "magic_desc": "Faint residual death-magic lingers in the marrow.",
                "estimated_value": 5,
                "description": "A hollow bone fragment. Reagent for crafting and alchemical use.",
            }},
            {"drop_chance": 0.08, "item": {
                "name": "Cracked Iron Buckler", "type": "armor",
                "slot": "off_hand", "subtype": "shield", "rarity": "common",
                "armor_tier": "light", "defense": 2,
                "identify_difficulty": 1,
                "unidentified_name": "Cracked Shield",
                "unidentified_desc": "A small shield with a stress fracture running across it.",
                "appraised_name": "Cracked Iron Buckler",
                "material_desc": "Cracked iron, structurally compromised. Barely worth carrying.",
                "magic_desc": "No magical properties.",
                "estimated_value": 65,
                "description": "A small iron shield, cracked but still deflecting.",
            }},
        ],
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
        "xp_reward": 100, "gold_reward": (10, 25),
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
                "damage": 19, "phys_type": "slashing",
                "damage_stat": {"STR": 0.3, "DEX": 0.12},
                "identify_difficulty": 1,
                "unidentified_name": "Crude Broadsword",
                "unidentified_desc": "A heavy iron blade with rough hammer marks. Brutally functional.",
                "appraised_name": "Orcish Iron Broadsword",
                "material_desc": "Crude orcish ironwork. Heavy but effective. Poor resale value.",
                "magic_desc": "No magical properties.",
                "estimated_value": 90,
                "description": "A crude but heavy iron blade favored by orc warriors.",
            }},
            {"drop_chance": 0.25, "item": {
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
        "hp": 250, "defense": 18, "magic_resist": 10,
        "stats": {"STR": 20, "DEX": 10, "CON": 18, "INT": 8, "WIS": 8, "PIE": 4},
        "speed_base": 14,
        "attack_damage": 44, "attack_type": "melee", "phys_type": "slashing",
        "accuracy_bonus": 5,
        "preferred_row": FRONT,
        "ai_type": "boss",
        "xp_reward": 240, "gold_reward": (30, 60),
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
                "damage": 22, "phys_type": "slashing",
                "damage_stat": {"STR": 0.3, "DEX": 0.12},
                "enhance_bonus": 1, "effect": {"str_bonus": 1},
                "identify_difficulty": 2,
                "unidentified_name": "Ornate Broadsword",
                "unidentified_desc": "A massive jagged blade with crude etchings along the fuller. Faintly warm to the touch.",
                "appraised_name": "Masterwork Orcish Broadsword",
                "material_desc": "Superior orcish steel, forged by a skilled weaponsmith. Rare quality for orc work.",
                "magic_desc": "+1 enhancement. Faint enchantment boosts the wielder's strength.",
                "estimated_value": 220,
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
                "estimated_value": 220,
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
            {"drop_chance": 0.15, "item": {
                "_training_book": True,
                "name": "Training Manual", "type": "consumable",
                "rarity": "uncommon", "identified": True,
                "description": "A worn training manual. Contains a stat boost.",
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
        "hp": 110, "defense": 3, "magic_resist": 12,
        "stats": {"STR": 3, "DEX": 8, "CON": 4, "INT": 10, "WIS": 10, "PIE": 6},
        "speed_base": 14,
        "attack_damage": 22, "attack_type": "melee", "phys_type": "blunt",
        "accuracy_bonus": 0,
        "preferred_row": BACK,
        "ai_type": "supportive",
        "xp_reward": 52, "gold_reward": (5, 12),
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
                "damage": 10, "damage_stat": {"INT": 0.32},
                "spell_bonus": 2,
                "cast_spell": "Magic Missile",
                "max_charges": 10,
                "identify_difficulty": 2,
                "unidentified_name": "Gnarled Stick",
                "unidentified_desc": "A twisted twig wrapped in leather strips. It tingles slightly when held.",
                "appraised_name": "Goblin Focus Wand",
                "material_desc": "Swamp oak wrapped in lizard leather. Crude but functional focus implement.",
                "magic_desc": "Casts Magic Missile. 10 charges.",
                "estimated_value": 80,
                "description": "A gnarled twig wrapped in leather strips. Casts Magic Missile. 10 charges.",
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
        "hp": 380, "defense": 12, "magic_resist": 8,
        "stats": {"STR": 18, "DEX": 10, "CON": 16, "INT": 6, "WIS": 8, "PIE": 4},
        "speed_base": 12,
        "attack_damage": 30, "attack_type": "melee", "phys_type": "blunt",
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
                "estimated_value": 260,
                "description": "A crude crown of bent metal and stolen gems. "
                               "+12 DEF. Surprisingly well-made for goblin craftsmanship.",
            }},
            {"drop_chance": 0.60, "item": {
                "name": "Goblin King's Coin", "type": "accessory", "subtype": "trinket",
                "rarity": "uncommon", "tier": 2, "identified": False,
                "appraised_name": "Goblin King's Lucky Coin",
                "estimated_value": 140,
                "stat_bonus": {"LCK": 2},
                "description": "A battered gold coin Grak carried for luck. +2 LCK.",
            }},
            {"drop_chance": 0.15, "item": {
                "_training_book": True,
                "name": "Training Manual", "type": "consumable",
                "rarity": "uncommon", "identified": True,
                "description": "A worn training manual. Contains a stat boost.",
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
        "hp": 480, "defense": 16, "magic_resist": 12,
        "stats": {"STR": 14, "DEX": 18, "CON": 14, "INT": 4, "WIS": 12, "PIE": 2},
        "speed_base": 18,
        "attack_damage": 35, "attack_type": "melee", "phys_type": "piercing",
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
                "estimated_value": 265,
                "description": "A shimmering cloak woven from spider silk. Light and magically resistant.",
            }},
            {"drop_chance": 0.15, "item": {
                "_training_book": True,
                "name": "Training Manual", "type": "consumable",
                "rarity": "uncommon", "identified": True,
                "description": "A worn training manual. Contains a stat boost.",
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
        "hp": 400, "defense": 20, "magic_resist": 14,
        "stats": {"STR": 20, "DEX": 8, "CON": 22, "INT": 10, "WIS": 14, "PIE": 2},
        "speed_base": 8,
        "attack_damage": 40, "attack_type": "melee", "phys_type": "blunt",
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
        "tags": ["undead"],
        "abilities": ["Skull Crush", "Enrage"],
        "loot_table": [
            {"drop_chance": 0.80, "item": {
                "name": "Foreman's Pickaxe", "type": "weapon", "subtype": "axe",
                "rarity": "rare", "tier": 3, "damage": 32, "identified": True,
                "damage_stat": {"STR": 0.4},
                "estimated_value": 295,
                "description": "A massive mining pick, still sharp after centuries. +22 base damage.",
            }},
            {"drop_chance": 0.15, "item": {
                "_training_book": True,
                "name": "Training Manual", "type": "consumable",
                "rarity": "uncommon", "identified": True,
                "description": "A worn training manual. Contains a stat boost.",
            }},
        ],
        "description_tiers": {
            0: "A towering undead figure in tattered work clothes, clutching a massive pickaxe.",
            1: "The Foreman",
            2: "The Foreman — Boss. Undead. Slow but devastating. Weak to divine and fire.",
        },
    },

    # ─── Abandoned Mine Boss ───────────────────────────────────────
    "Korrath the Stone Warden": {
        "name": "Korrath the Stone Warden",
        "hp": 480, "defense": 28, "magic_resist": 18,
        "stats": {"STR": 22, "DEX": 8, "CON": 26, "INT": 14, "WIS": 18, "PIE": 10},
        "speed_base": 6,
        "attack_damage": 46, "attack_type": "melee", "phys_type": "blunt",
        "accuracy_bonus": 8,
        "preferred_row": FRONT,
        "ai_type": "boss",
        "xp_reward": 380, "gold_reward": (120, 220),
        "resistances": {
            "piercing": RESISTANT, "slashing": RESISTANT, "blunt": NEUTRAL,
            "fire": NEUTRAL, "ice": NEUTRAL, "lightning": RESISTANT,
            "divine": NEUTRAL, "shadow": RESISTANT, "nature": NEUTRAL,
            "arcane": NEUTRAL,
        },
        "status_immunities": ["poison", "stun", "fear", "charm"],
        "abilities": ["Stone Slam", "Ward Pulse", "Enrage"],
        "loot_table": [
            {"drop_chance": 1.0, "item": {
                "name": "Hearthstone Fragment (Mine)", "type": "key_item",
                "subtype": "hearthstone_fragment", "identified": True,
                "rarity": "legendary", "tier": 3,
                "estimated_value": 0,
                "description": "A warm fragment of the First Hearthstone, glowing with amber light. "
                               "The dwarven Warden Korrath guarded this for centuries.",
            }},
            {"drop_chance": 0.85, "item": {
                "name": "Warden's Stone Hammer", "type": "weapon", "subtype": "hammer",
                "rarity": "rare", "tier": 3, "damage": 36, "identified": True,
                "damage_stat": {"STR": 0.4},
                "estimated_value": 380,
                "description": "A dwarven war-hammer inscribed with ward-runes. "
                               "+26 base damage, +8 magic resist to wielder.",
                "stat_bonus": {"magic_resist": 8},
            }},
            {"drop_chance": 0.15, "item": {
                "_training_book": True,
                "name": "Training Manual", "type": "consumable",
                "rarity": "uncommon", "identified": True,
                "description": "A worn training manual. Contains a stat boost.",
            }},
        ],
        "description_tiers": {
            0: "A massive stone-clad figure, translucent at the edges. "
               "The ghost of a dwarven Warden, still at his post.",
            1: "Korrath the Stone Warden",
            2: "Korrath the Stone Warden — Boss. Warden ghost. Resistant to most damage types. "
               "Weak to nothing in particular — endure and outlast.",
        },
    },

    # ─── Ruins of Ashenmoor Boss ───────────────────────────────────
    "Commander Ashvar": {
        "name": "Commander Ashvar",
        "hp": 440, "defense": 26, "magic_resist": 42,
        "stats": {"STR": 18, "DEX": 14, "CON": 20, "INT": 22, "WIS": 16, "PIE": 4},
        "speed_base": 10,
        "attack_damage": 42, "attack_type": "melee", "phys_type": "slashing",
        "accuracy_bonus": 10,
        "preferred_row": FRONT,
        "ai_type": "boss",
        "xp_reward": 360, "gold_reward": (140, 250),
        "resistances": {
            "piercing": NEUTRAL, "slashing": NEUTRAL, "blunt": NEUTRAL,
            "fire": IMMUNE, "ice": NEUTRAL, "lightning": NEUTRAL,
            "divine": VULNERABLE, "shadow": RESISTANT, "nature": NEUTRAL,
            "arcane": NEUTRAL,
        },
        "status_immunities": ["poison", "fear", "charm"],
        "abilities": ["Ashen Wave", "Shadow Bind", "Commander's Wrath"],
        "loot_table": [
            {"drop_chance": 0.90, "item": {
                "name": "Ashenmoor Commander's Seal", "type": "accessory",
                "subtype": "amulet", "rarity": "rare", "tier": 3,
                "identified": True, "estimated_value": 300,
                "description": "A cracked warden seal, still radiating residual authority. "
                               "+12 magic resist, +6 defense.",
                "stat_bonus": {"magic_resist": 12, "defense": 6},
            }},
            {"drop_chance": 0.60, "item": {
                "name": "Scorched Warden Blade", "type": "weapon", "subtype": "sword",
                "rarity": "uncommon", "tier": 3, "damage": 30, "identified": True,
                "damage_stat": {"STR": 0.3, "DEX": 0.12},
                "estimated_value": 300,
                "description": "A warden's sword, blackened by whatever destroyed Ashenmoor. "
                               "+20 base damage, deals bonus fire damage.",
                "stat_bonus": {"fire_damage_bonus": 6},
            }},
            {"drop_chance": 0.15, "item": {
                "_training_book": True,
                "name": "Training Manual", "type": "consumable",
                "rarity": "uncommon", "identified": True,
                "description": "A worn training manual. Contains a stat boost.",
            }},
        ],
        "description_tiers": {
            0: "A figure of scorched bone and hardened ash, encased in the charred remnants "
               "of warden plate. The ruins shaped something from what was left behind.",
            1: "Commander Ashvar",
            2: "Commander Ashvar — Boss. Ash-bound undead Warden. Immune to fire. "
               "Weak to divine. High magic resist — physical attacks hit harder.",
        },
    },

    "Giant Spider": {
        "name": "Giant Spider",
        "hp": 140, "defense": 13, "magic_resist": 6,
        "stats": {"STR": 10, "DEX": 16, "CON": 8, "INT": 2, "WIS": 8, "PIE": 1},
        "speed_base": 20,
        "attack_damage": 32, "attack_type": "melee", "phys_type": "piercing",
        "accuracy_bonus": 8,
        "preferred_row": FRONT,
        "ai_type": "aggressive",
        "xp_reward": 45, "gold_reward": (2, 5),
        "resistances": {
            "piercing": NEUTRAL, "slashing": NEUTRAL, "blunt": NEUTRAL,
            "fire": VULNERABLE, "ice": NEUTRAL, "lightning": NEUTRAL,
            "divine": NEUTRAL, "shadow": NEUTRAL, "nature": RESISTANT,
            "arcane": NEUTRAL,
        },
        "status_immunities": [],
        "abilities": [],
        "loot_table": [
            {"drop_chance": 0.35, "item": {
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
    "boss_mine_warden": {
        "name": "The Deep Vault",
        "difficulty": "boss",
        "groups": [
            {"enemy": "Korrath the Stone Warden", "count": 1, "row": FRONT},
            {"enemy": "Stone Sentinel", "count": 2, "row": FRONT},
        ],
    },
    "boss_ashenmoor": {
        "name": "The Commander's Court",
        "difficulty": "boss",
        "groups": [
            {"enemy": "Commander Ashvar", "count": 1, "row": FRONT},
            {"enemy": "Ash Revenant", "count": 2, "row": MID},
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
        # Spider's Nest encounters — added to replace goblin/bandit placeholders
    "easy_spiders": {
        "name": "Spider Nest",
        "difficulty": "easy",
        "groups": [
            {"enemy": "Spiderling", "count": 4, "row": FRONT},
            {"enemy": "Giant Spider", "count": 1, "row": FRONT},
        ],
    },
    "medium_spiders": {
        "name": "Spider Colony",
        "difficulty": "medium",
        "groups": [
            {"enemy": "Giant Spider", "count": 2, "row": FRONT},
            {"enemy": "Web Spinner", "count": 1, "row": BACK},
            {"enemy": "Spiderling", "count": 2, "row": FRONT},
        ],
    },
    "hard_spiders": {
        "name": "Brood Chamber",
        "difficulty": "hard",
        "groups": [
            {"enemy": "Venomfang Spider", "count": 2, "row": FRONT},
            {"enemy": "Web Spinner", "count": 1, "row": BACK},
            {"enemy": "Giant Spider", "count": 1, "row": FRONT},
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

# ── Fix missing slot fields on all loot items ─────────────────
from core.item_slot_fixer import fix_loot_table as _fix_loot
for _eid, _edata in ENEMIES.items():
    if _edata.get("loot_table"):
        _fix_loot(_edata["loot_table"])

DUNGEON_ENCOUNTER_TABLES = {
    "goblin_warren": {
        1: ["easy_goblins", "medium_goblins", "wolves"],
        2: ["medium_goblins", "hard_goblins", "medium_bandits"],
        3: ["hard_goblins", "hard_mixed"],
        "boss": "boss_goblin_king",
    },
    "spiders_nest": {
        1: ["easy_spiders", "medium_spiders"],
        2: ["medium_spiders", "hard_spiders"],
        3: ["hard_spiders", "spider_swarm"],
        4: ["spider_swarm", "hard_spiders"],
        "boss": "boss_spider_queen",
    },
    "abandoned_mine": {
        1: ["medium_goblins", "medium_bandits"],
        2: ["hard_mixed", "orc_patrol"],
        3: ["orc_patrol", "hard_mixed"],
        "boss": "boss_mine_warden",
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
        "boss": "boss_ashenmoor",
    },
    # ── Spider's Nest — proper escalation ─────────────────────────
    "sn_web_scouts": {
        "name": "Web Scouts",
        "difficulty": "easy",
        "groups": [
            {"enemy": "Spiderling", "count": 4, "row": "front"},
            {"enemy": "Spiderling", "count": 2, "row": "mid"},
        ],
    },
    "sn_patrol": {
        "name": "Spider Patrol",
        "difficulty": "easy",
        "groups": [
            {"enemy": "Spiderling", "count": 3, "row": "front"},
            {"enemy": "Giant Spider", "count": 1, "row": "mid"},
        ],
    },
    "sn_webbed": {
        "name": "Webbed Chamber",
        "difficulty": "medium",
        "groups": [
            {"enemy": "Giant Spider", "count": 2, "row": "front"},
            {"enemy": "Spiderling", "count": 3, "row": "mid"},
        ],
    },
    "sn_broodling": {
        "name": "Brood Cluster",
        "difficulty": "medium",
        "groups": [
            {"enemy": "Web Spinner", "count": 1, "row": "back"},
            {"enemy": "Giant Spider", "count": 1, "row": "front"},
            {"enemy": "Spiderling", "count": 4, "row": "front"},
        ],
    },
    # ── Abandoned Mine — proper escalation ─────────────────────────
    "mine_rats": {
        "name": "Rat Infestation",
        "difficulty": "easy",
        "groups": [
            {"enemy": "Rabid Rat", "count": 5, "row": "front"},
            {"enemy": "Mine Rat Swarm", "count": 2, "row": "mid"},
        ],
    },
    "mine_bandits": {
        "name": "Bandit Camp",
        "difficulty": "medium",
        "groups": [
            {"enemy": "Bandit", "count": 2, "row": "front"},
            {"enemy": "Bandit Thief", "count": 1, "row": "mid"},
        ],
    },
    "mine_mixed": {
        "name": "Bandit Warband",
        "difficulty": "hard",
        "groups": [
            {"enemy": "Bandit Fighter", "count": 2, "row": "front"},
            {"enemy": "Bandit Archer", "count": 2, "row": "mid"},
            {"enemy": "Bandit Mage", "count": 1, "row": "back"},
        ],
    },
    # ── Sunken Crypt — undead escalation ───────────────────────────
    "crypt_easy": {
        "name": "Risen Dead",
        "difficulty": "easy",
        "groups": [
            {"enemy": "Zombie", "count": 3, "row": "front"},
        ],
    },
    "crypt_medium": {
        "name": "Crypt Patrol",
        "difficulty": "medium",
        "groups": [
            {"enemy": "Skeleton Warrior", "count": 2, "row": "front"},
            {"enemy": "Skeletal Archer", "count": 2, "row": "mid"},
        ],
    },
    "crypt_hard": {
        "name": "Crypt Guard",
        "difficulty": "hard",
        "groups": [
            {"enemy": "Crypt Soldier", "count": 2, "row": "front"},
            {"enemy": "Crypt Shade", "count": 2, "row": "mid"},
            {"enemy": "Ghoul", "count": 1, "row": "front"},
        ],
    },
    # ── Ruins of Ashenmoor — escalation ────────────────────────────
    "ash_cultists": {
        "name": "Cultist Cell",
        "difficulty": "medium",
        "groups": [
            {"enemy": "Cultist Initiate", "count": 3, "row": "front"},
            {"enemy": "Cultist Warrior", "count": 1, "row": "front"},
        ],
    },
    "ash_ruin_guard": {
        "name": "Ruin Guard",
        "difficulty": "medium",
        "groups": [
            {"enemy": "Ruin Archer", "count": 2, "row": "mid"},
            {"enemy": "Ashenmoor Bandit", "count": 2, "row": "front"},
        ],
    },
    "ash_hard": {
        "name": "Ashenmoor Warband",
        "difficulty": "hard",
        "groups": [
            {"enemy": "Orc Fighter", "count": 2, "row": "front"},
            {"enemy": "Ashenmoor Crossbowman", "count": 2, "row": "mid"},
            {"enemy": "Cultist Hexblade", "count": 1, "row": "back"},
        ],
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
        "tags": list(template.get("tags", [])),
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

# ── Humanoid class-based enemies ──
from data.humanoid_enemies import (
    HUMANOID_ENEMIES, HUMANOID_ENCOUNTERS, HUMANOID_ENCOUNTER_TABLE_UPDATES,
)

ENEMIES.update(HUMANOID_ENEMIES)
ENCOUNTERS.update(HUMANOID_ENCOUNTERS)

# Merge encounter table additions (extend existing lists rather than replace)
for dungeon_id, floors in HUMANOID_ENCOUNTER_TABLE_UPDATES.items():
    if dungeon_id not in DUNGEON_ENCOUNTER_TABLES:
        DUNGEON_ENCOUNTER_TABLES[dungeon_id] = {}
    for floor, new_keys in floors.items():
        existing = DUNGEON_ENCOUNTER_TABLES[dungeon_id].get(floor, [])
        if isinstance(existing, str):
            existing = [existing]
        merged = list(dict.fromkeys(existing + new_keys))  # deduplicate, preserve order
        DUNGEON_ENCOUNTER_TABLES[dungeon_id][floor] = merged

# ── New faction enemies (beasts, fallen wardens, pirates, imperial, dwarves) ──
from data.new_factions import (
    ALL_NEW_FACTION_ENEMIES, ALL_NEW_FACTION_ENCOUNTERS,
    NEW_FACTION_ENCOUNTER_TABLE_UPDATES,
)

ENEMIES.update(ALL_NEW_FACTION_ENEMIES)
ENCOUNTERS.update(ALL_NEW_FACTION_ENCOUNTERS)

for dungeon_id, floors in NEW_FACTION_ENCOUNTER_TABLE_UPDATES.items():
    if dungeon_id not in DUNGEON_ENCOUNTER_TABLES:
        DUNGEON_ENCOUNTER_TABLES[dungeon_id] = {}
    for floor, new_keys in floors.items():
        existing = DUNGEON_ENCOUNTER_TABLES[dungeon_id].get(floor, [])
        if isinstance(existing, str):
            existing = [existing]
        merged = list(dict.fromkeys(existing + new_keys))
        DUNGEON_ENCOUNTER_TABLES[dungeon_id][floor] = merged


# ── Combat Balance Recalibration (Momentum system) ──────────────────────────
# Applied once after all enemy dicts are assembled.
# Standard enemies: HP ×0.65, Bosses (HP≥400): HP ×0.75, Attack ×0.80.
# These multipliers bring the "3-4 basic attacks to kill" design target into range.
_BOSS_THRESHOLD = 400
for _en_name, _en in ENEMIES.items():
    _old_hp = _en.get("hp", 0)
    _hp_mult = 0.75 if _old_hp >= _BOSS_THRESHOLD else 0.65
    _en["hp"] = max(12, round(_old_hp * _hp_mult))
    _old_atk = _en.get("attack_damage", 0)
    if isinstance(_old_atk, (list, tuple)):
        _en["attack_damage"] = [max(6, round(v * 0.80)) for v in _old_atk]
    elif _old_atk:
        _en["attack_damage"] = max(6, round(_old_atk * 0.80))


# ═══════════════════════════════════════════════════════════════
#  BOSS PHASE DEFINITIONS
#  Each boss can have up to 3 phases triggered by HP thresholds.
#  Phase data is injected into the enemy dict at runtime.
#
#  Structure per phase:
#    threshold   — HP % that triggers this phase (e.g. 0.60 = below 60%)
#    announce    — dramatic text shown in the combat log
#    dmg_mult    — damage multiplier applied from this phase forward
#    new_abilities — list of ability dicts added to the enemy's pool
#    status_immunity — new statuses the boss becomes immune to
#    heal_pct    — optional: boss heals this % of max HP on transition
# ═══════════════════════════════════════════════════════════════

BOSS_PHASES = {
    # ── Grak the Goblin King ────────────────────────────────────
    # Phase 1 (start): Normal chieftain. Can be reasoned with before fight.
    # Phase 2 (60% HP): Witnesses a warrior fall — crowd chants drive him.
    # Phase 3 (25% HP): Cornered animal. Rage overcomes him entirely.
    "Grak the Goblin King": [
        {
            "threshold": 0.60,
            "announce": "Grak ROARS as a warrior falls. The goblins drum their weapons "
                        "on the walls. He swells with fury — this is his TRIBE.",
            "dmg_mult": 1.25,
            "new_abilities": [
                {
                    "name": "Tribal Fury",
                    "type": "damage",
                    "power": 28,
                    "element": "blunt",
                    "target": "single",
                    "description": "A wild overhead swing charged with desperate rage.",
                },
            ],
            "status_immunity": [],
        },
        {
            "threshold": 0.25,
            "announce": "Grak sways. Blood mats his crown. He screams something in Goblin "
                        "— not a battle cry. A name. His people go silent. "
                        "Then he charges.",
            "dmg_mult": 1.55,
            "new_abilities": [
                {
                    "name": "Last Stand",
                    "type": "damage",
                    "power": 44,
                    "element": "blunt",
                    "target": "single",
                    "aoe_chance": 0.35,   # 35% chance hits adjacent target too
                    "description": "Grak throws everything into one desperate strike.",
                },
            ],
            "status_immunity": ["stun", "fear"],
        },
    ],

    # ── Korrath the Stone Warden ─────────────────────────────────
    # Phase 1: Testing the party with methodical Warden discipline.
    # Phase 2 (55% HP): Wards activate — he stops pulling his blows.
    # Phase 3 (20% HP): Centuries of patience break. The full ancient power.
    "Korrath the Stone Warden": [
        {
            "threshold": 0.55,
            "announce": "The ward-runes carved into Korrath's armor ignite with cold blue light. "
                        "His voice, when it comes, carries the weight of four centuries: "
                        "'You have made it past the first gate. There is no mercy beyond this one.'",
            "dmg_mult": 1.30,
            "new_abilities": [
                {
                    "name": "Warden's Judgment",
                    "type": "damage",
                    "power": 38,
                    "element": "divine",
                    "target": "single",
                    "description": "A crushing strike imbued with ancient warden authority.",
                },
                {
                    "name": "Stone Aegis",
                    "type": "buff",
                    "power": 0,
                    "stat": "defense",
                    "amount": 14,
                    "duration": 3,
                    "target": "self",
                    "description": "The stone plates of his armor fuse tighter.",
                },
            ],
            "status_immunity": [],
        },
        {
            "threshold": 0.20,
            "announce": "Korrath staggers. For a moment his form flickers — "
                        "ghost-light bleeding through the stone. "
                        "Then his eyes focus, and they are burning. "
                        "'The ward demands a verdict. Let it be NOW.'",
            "dmg_mult": 1.60,
            "heal_pct": 0.12,   # heals 12% max HP on phase 3 trigger
            "new_abilities": [
                {
                    "name": "Ancient Reckoning",
                    "type": "damage",
                    "power": 55,
                    "element": "blunt",
                    "target": "aoe",
                    "description": "A shockwave of warden power — hits the entire party.",
                },
            ],
            "status_immunity": ["stun", "fear", "charm", "sleep"],
        },
    ],

    # ── Warden Revenant (Sunken Crypt — Deren) ───────────────────
    # Phase 1: Sorrowful and restrained — he wants to be stopped.
    # Phase 2 (50% HP): The crypt's shadow energy floods in. He loses himself.
    # Phase 3 (15% HP): A moment of lucidity before the end.
    "Warden Revenant": [
        {
            "threshold": 0.50,
            "announce": "The water-logged walls pulse with shadow energy. "
                        "Deren's form darkens — the grief on his face twists into something older, "
                        "colder. When he speaks again his voice is not entirely his own: "
                        "'It hurts less... if I stop remembering.'",
            "dmg_mult": 1.35,
            "new_abilities": [
                {
                    "name": "Crypt Flood",
                    "type": "debuff",
                    "power": 0,
                    "status": "Slowed",
                    "duration": 2,
                    "target": "aoe",
                    "description": "Dark water surges through the chamber, "
                                   "dragging at the party's feet.",
                },
                {
                    "name": "Shadow Torrent",
                    "type": "damage",
                    "power": 34,
                    "element": "shadow",
                    "target": "single",
                    "description": "A focused blast of compressed shadow.",
                },
            ],
            "status_immunity": ["fear"],
        },
        {
            "threshold": 0.15,
            "announce": "The shadow energy sputters. Deren's form clears — just for a moment — "
                        "and his eyes are his own again. He looks at his hands. "
                        "'I remember now. I remember all of it.' "
                        "Then the darkness floods back. But something in him is *helping* you.",
            "dmg_mult": 0.75,   # phase 3: he's fighting himself — lower damage
            "new_abilities": [
                {
                    "name": "Final Release",
                    "type": "damage",
                    "power": 62,
                    "element": "shadow",
                    "target": "single",
                    "description": "One last surge of crypt energy — and then silence.",
                },
            ],
            "status_immunity": [],
            "announce_post": "Deren falters between strikes, his form flickering. "
                             "He is still in there, fighting the shadow from the inside.",
        },
    ],

    # ── Karreth — Dragon's Tooth ─────────────────────────────────
    # Phase 1: Corrupted guardian, still bound by ancient oath.
    # Phase 2 (55% HP): The corruption surges — fire fills the chamber.
    # Phase 3 (20% HP): Fading energy spikes as the binding weakens.
    "Karreth": [
        {
            "threshold": 0.55,
            "announce": "The chamber shudders. Karreth spreads his wings and screams — "
                        "not a battle cry but something older, something *broken*. "
                        "The corruption blazes through his scales like veins of black fire. "
                        "He is still in there. It is getting harder to tell.",
            "dmg_mult": 1.40,
            "new_abilities": [
                {
                    "name": "Corrupted Breath",
                    "type": "damage",
                    "power": 50,
                    "element": "fire",
                    "target": "aoe",
                    "description": "A torrent of black-tainted fire sweeps the chamber.",
                },
                {
                    "name": "Shadow Frenzy",
                    "type": "debuff",
                    "power": 0,
                    "status": "Burning",
                    "duration": 3,
                    "target": "aoe",
                    "description": "The shadow fire sticks — everyone who isn't "
                                   "fire-resistant is burning.",
                },
            ],
            "status_immunity": ["fire"],
        },
        {
            "threshold": 0.20,
            "announce": "A deep crack splits the stone beneath Karreth's feet. "
                        "Fading energy bleeds up through it — his roar becomes a shriek. "
                        "But his eye — the undamaged one — fixes on you with terrible clarity. "
                        "He is *trying* to lose. He has been trying this whole time.",
            "dmg_mult": 1.65,
            "heal_pct": 0.08,
            "new_abilities": [
                {
                    "name": "Void Ignition",
                    "type": "damage",
                    "power": 68,
                    "element": "shadow",
                    "target": "aoe",
                    "description": "The chamber erupts in shadow-fire. "
                                   "Neither holy nor natural — a mixing of worlds.",
                },
            ],
            "status_immunity": ["stun", "fear", "charm"],
        },
    ],

    # ── Valdris the Broken — Final Boss ─────────────────────────
    # Phase 1: The Traitor Warden, sustained by Shadow. Methodical, tragic.
    # Phase 2 (65% HP): Activates the Spire's ward network against the party.
    # Phase 3 (35% HP): Maren's ritual begins interfering — Valdris fights it.
    # Phase 4 (10% HP): The Shadow consumes him — becomes Valdris, Shadow Avatar.
    "Valdris the Broken": [
        {
            "threshold": 0.65,
            "announce": "Valdris raises one hand. The Spire *responds* — "
                        "the ward-runes carved into every wall ignite simultaneously. "
                        "'I spent forty years building this place. Did you think I would "
                        "fight you without it?'",
            "dmg_mult": 1.20,
            "new_abilities": [
                {
                    "name": "Ward Shatter",
                    "type": "debuff",
                    "power": 0,
                    "status": "Exposed",
                    "duration": 3,
                    "target": "aoe",
                    "description": "The Spire's corrupted wards pulse outward, "
                                   "tearing through magical defenses.",
                },
                {
                    "name": "Fading Pulse",
                    "type": "damage",
                    "power": 38,
                    "element": "shadow",
                    "target": "aoe",
                    "description": "A wave of entropy — "
                                   "everything it touches is briefly less real.",
                },
            ],
            "status_immunity": [],
        },
        {
            "threshold": 0.35,
            "announce": "Something shifts. Valdris staggers — clutches his chest. "
                        "For a moment the Shadow retreats from his eyes. "
                        "'Maren. You came.' Then it floods back. "
                        "When he straightens, his voice is cold iron: "
                        "'It doesn't matter. Nothing matters but the sealing.'",
            "dmg_mult": 1.45,
            "new_abilities": [
                {
                    "name": "Dark Ritual",
                    "type": "buff",
                    "power": 0,
                    "stat": "attack_damage",
                    "amount": 22,
                    "duration": 4,
                    "target": "self",
                    "description": "Valdris channels the Spire's full power into himself.",
                },
                {
                    "name": "Shadow Nova",
                    "type": "damage",
                    "power": 55,
                    "element": "shadow",
                    "target": "aoe",
                    "description": "A burst of compressed shadow energy — "
                                   "the weight of four centuries of regret.",
                },
            ],
            "status_immunity": ["fear", "charm"],
        },
        {
            "threshold": 0.10,
            "announce": "The Shadow tears through Valdris entirely. "
                        "The man disappears — what rises in his place is older, "
                        "colder, and has no name that can be spoken. "
                        "The last thing you hear in his voice: 'Finish it.'",
            "dmg_mult": 2.00,
            "heal_pct": 0.20,
            "status_immunity": ["stun", "fear", "charm", "sleep", "freeze"],
            "transform": "Valdris, Shadow Avatar",   # signals a full enemy swap
            "new_abilities": [
                {
                    "name": "Void Consumption",
                    "type": "damage",
                    "power": 75,
                    "element": "shadow",
                    "target": "aoe",
                    "description": "The Shadow Avatar reaches out and unmakes.",
                },
            ],
            "announce_post": "The chamber darkens to nothing. "
                             "Only the Shadow Avatar remains.",
        },
    ],
}
