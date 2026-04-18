"""
Realm of Shadows — Humanoid Enemy Roster

Class-based human/humanoid enemies organized by faction.
Each enemy mirrors a player class archetype — visually reuses
character grids in pixel_art.py via the _ENEMY_GRIDS mapping.

Factions:
  Bandits        — wilderness / early dungeons (goblin_warren, abandoned_mine)
  Iron Mercenaries — mid-game hired swords (abandoned_mine, sunken_crypt, ruins_ashenmoor)
  Ashenmoor Cult — ruin cultists (ruins_ashenmoor, pale_coast)
  Corrupted Guard — undead former soldiers (sunken_crypt, shadow_throne)
"""

from core.combat_config import (
    IMMUNE, RESISTANT, NEUTRAL, VULNERABLE, VERY_VULNERABLE,
    FRONT, MID, BACK,
)

# ══════════════════════════════════════════════════════════════
#  SHARED LOOT HELPERS
# ══════════════════════════════════════════════════════════════

def _coin(lo, hi): return (lo, hi)

def _sword(name, unid, dmg, val, desc):
    return {"name": name, "type": "weapon", "slot": "weapon", "subtype": "Long Sword",
            "rarity": "common", "damage": dmg + 10,
            "damage_stat": {"STR": 0.3, "DEX": 0.12},
            "phys_type": "slashing", "range": "melee",
            "identify_difficulty": 1,
            "unidentified_name": unid, "unidentified_desc": "A serviceable blade.",
            "appraised_name": name, "material_desc": "Common steel.",
            "magic_desc": "No magical properties.", "estimated_value": val,
            "description": desc}

def _dagger(name, dmg, val, desc):
    return {"name": name, "type": "weapon", "slot": "weapon", "subtype": "Dagger",
            "rarity": "common", "damage": dmg + 10,
            "damage_stat": {"DEX": 0.40},
            "phys_type": "piercing",
            "identify_difficulty": 1,
            "unidentified_name": "Hidden Blade", "unidentified_desc": "A short, concealable blade.",
            "appraised_name": name, "material_desc": "Steel blade, edge honed repeatedly.",
            "magic_desc": "No magical properties.", "estimated_value": val,
            "description": desc}

def _staff(name, dmg, val, desc):
    return {"name": name, "type": "weapon", "slot": "weapon", "subtype": "Staff", "max_charges": 30,
            "rarity": "common", "damage": dmg + 10,
            "damage_stat": {"STR": 0.16, "INT": 0.24},
            "phys_type": "blunt",
            "identify_difficulty": 2,
            "unidentified_name": "Carved Staff", "unidentified_desc": "A staff with crude sigils carved into it.",
            "appraised_name": name, "material_desc": "Ashwood, reinforced with iron rings.",
            "magic_desc": "Faint magical residue.", "estimated_value": val,
            "description": desc}

def _leather(val=4):
    return {"name": "Leather Scraps", "type": "material", "subtype": "leather",
            "rarity": "common", "tier": 1, "identify_difficulty": 1,
            "unidentified_name": "Leather Scraps", "unidentified_desc": "Worn leather pieces.",
            "appraised_name": "Boiled Leather Scraps", "material_desc": "Tier 1 crafting material.",
            "magic_desc": "No magical properties.", "estimated_value": val,
            "description": "Scraps of boiled leather, useful for crafting."}

def _coin_pouch(lo, hi):
    return {"name": "Coin Pouch", "type": "consumable", "subtype": "gold",
            "rarity": "common", "gold_value": (lo, hi),
            "identify_difficulty": 0, "identified": True,
            "description": "A small pouch of coins."}

def _res(neutral_all=True, **overrides):
    base = {k: NEUTRAL for k in
            ("piercing","slashing","blunt","fire","ice","lightning",
             "divine","shadow","nature","arcane")}
    base.update(overrides)
    return base


# ══════════════════════════════════════════════════════════════
#  FACTION: BANDITS  (early game, levels 1-4)
# ══════════════════════════════════════════════════════════════

HUMANOID_ENEMIES = {

    # ── Bandit Fighter ──────────────────────────────────────
    "Bandit Fighter": {
        "name": "Bandit Fighter",
        "hp": 108, "defense": 10, "magic_resist": 3,
        "stats": {"STR": 13, "DEX": 9,  "CON": 11, "INT": 5, "WIS": 5, "PIE": 3},
        "speed_base": 15,
        "attack_damage": 30, "attack_type": "melee", "phys_type": "slashing",
        "accuracy_bonus": 2,
        "preferred_row": FRONT,
        "ai_type": "aggressive",
        "xp_reward": 64, "gold_reward": _coin(8, 20),
        "resistances": _res(),
        "status_immunities": [],
        "abilities": [],
        "loot_table": [
            {"drop_chance": 0.15, "item": _sword(
                "Bandit Broadsword", "Heavy Sword", 8, 85,
                "A broad iron sword, notched from heavy use. Still cuts.")},
            {"drop_chance": 0.10, "item": _leather()},
        ],
        "description_tiers": {
            0: "A broad-shouldered human in battered leather armor.",
            1: "Bandit Fighter",
            2: "Bandit Fighter — heavy melee bruiser, hits hard and soaks punishment.",
        },
    },

    # ── Bandit Archer ──────────────────────────────────────
    "Bandit Archer": {
        "name": "Bandit Archer",
        "hp": 88, "defense": 6, "magic_resist": 3,
        "stats": {"STR": 9,  "DEX": 14, "CON": 8,  "INT": 6, "WIS": 7, "PIE": 3},
        "speed_base": 17,
        "attack_damage": 22, "attack_type": "ranged", "phys_type": "piercing",
        "accuracy_bonus": 4,
        "preferred_row": BACK,
        "ai_type": "ranged",
        "xp_reward": 56, "gold_reward": _coin(6, 16),
        "resistances": _res(),
        "status_immunities": [],
        "abilities": [],
        "loot_table": [
            {"drop_chance": 0.20, "item": {
                "name": "Bundle of Arrows", "type": "consumable", "subtype": "ammo",
                "rarity": "common", "quantity": 8, "identify_difficulty": 0, "identified": True,
                "description": "A bundle of crude iron-tipped arrows."}},
            {"drop_chance": 0.08, "item": _dagger("Backup Knife", 4, 60,
                "A short blade the archer kept hidden.")},
        ],
        "description_tiers": {
            0: "A lean figure at the back, drawing back a bowstring.",
            1: "Bandit Archer",
            2: "Bandit Archer — ranged attacker, dangerous from back row.",
        },
    },

    # ── Bandit Thief ──────────────────────────────────────
    "Bandit Thief": {
        "name": "Bandit Thief",
        "hp": 82, "defense": 7, "magic_resist": 4,
        "stats": {"STR": 9,  "DEX": 15, "CON": 8,  "INT": 8, "WIS": 7, "PIE": 3},
        "speed_base": 20,
        "attack_damage": 25, "attack_type": "melee", "phys_type": "piercing",
        "accuracy_bonus": 5,
        "preferred_row": FRONT,
        "ai_type": "flanker",
        "xp_reward": 52, "gold_reward": _coin(10, 28),
        "resistances": _res(),
        "status_immunities": [],
        "abilities": ["enemy_crippling_strike"],
        "loot_table": [
            {"drop_chance": 0.18, "item": _dagger("Serrated Stiletto", 5, 75,
                "A thin blade with a serrated edge. Designed to wound, not kill quickly.")},
            {"drop_chance": 0.15, "item": _coin_pouch(5, 20)},
        ],
        "description_tiers": {
            0: "A wiry, hooded figure who moves with unsettling quiet.",
            1: "Bandit Thief",
            2: "Bandit Thief — fast, hits weak spots, often carries stolen coin.",
        },
    },

    # ── Bandit Mage ──────────────────────────────────────
    "Bandit Mage": {
        "name": "Bandit Mage",
        "hp": 72, "defense": 4, "magic_resist": 10,
        "stats": {"STR": 6,  "DEX": 9,  "CON": 7,  "INT": 14, "WIS": 8, "PIE": 4},
        "speed_base": 14,
        "attack_damage": 28, "attack_type": "magic", "phys_type": "arcane",
        "accuracy_bonus": 3,
        "preferred_row": BACK,
        "ai_type": "caster",
        "xp_reward": 76, "gold_reward": _coin(8, 22),
        "resistances": _res(arcane=RESISTANT),
        "status_immunities": [],
        "abilities": ["enemy_fireball"],
        "loot_table": [
            {"drop_chance": 0.20, "item": _staff("Rough Ashwood Staff", 5, 80,
                "A staff carved with crude runes. Self-taught magic at its most dangerous.")},
            {"drop_chance": 0.25, "item": {
                "name": "Mana Shard", "type": "material", "subtype": "arcane",
                "rarity": "uncommon", "tier": 1, "identify_difficulty": 2,
                "unidentified_name": "Glowing Shard", "unidentified_desc": "A fragment that hums with energy.",
                "appraised_name": "Raw Mana Shard", "material_desc": "Unstable arcane crystal. Tier 1.",
                "magic_desc": "Strong magical resonance.", "estimated_value": 22,
                "description": "A crystallized fragment of raw magical energy."}},
        ],
        "description_tiers": {
            0: "A robed figure with glowing eyes, muttering words that make the air crackle.",
            1: "Bandit Mage",
            2: "Bandit Mage — self-taught spellcaster, unpredictable and fragile. Kill first.",
        },
    },

    # ── Bandit Captain ──────────────────────────────────────
    "Bandit Captain": {
        "name": "Bandit Captain",
        "hp": 145, "defense": 14, "magic_resist": 6,
        "stats": {"STR": 15, "DEX": 12, "CON": 13, "INT": 8, "WIS": 7, "PIE": 3},
        "speed_base": 16,
        "attack_damage": 38, "attack_type": "melee", "phys_type": "slashing",
        "accuracy_bonus": 4,
        "preferred_row": FRONT,
        "ai_type": "tactical",
        "xp_reward": 65, "gold_reward": _coin(25, 60),
        "resistances": _res(),
        "status_immunities": [],
        "abilities": ["enemy_war_cry", "enemy_cleave"],
        "loot_table": [
            {"drop_chance": 0.30, "item": _sword(
                "Captain's Longsword", "Fine Sword", 12, 115,
                "A proper sword — well-maintained and obviously the captain's pride.")},
            {"drop_chance": 0.20, "item": _coin_pouch(20, 50)},
            {"drop_chance": 0.12, "item": {
                "name": "Stolen Map Fragment", "type": "quest_item",
                "rarity": "uncommon", "identify_difficulty": 0, "identified": True,
                "description": "A torn piece of a map. Something valuable nearby?"}},
        ],
        "description_tiers": {
            0: "A scarred human in a patchwork of stolen armor, clearly in charge.",
            1: "Bandit Captain",
            2: "Bandit Captain — miniboss-tier, rallies allies, hits with brutal cleave attacks.",
        },
    },

    # ══════════════════════════════════════════════════════════
    #  FACTION: IRON MERCENARIES  (mid game, levels 4-7)
    # ══════════════════════════════════════════════════════════

    "Sellsword": {
        "name": "Sellsword",
        "hp": 138, "defense": 14, "magic_resist": 5,
        "stats": {"STR": 14, "DEX": 11, "CON": 13, "INT": 7, "WIS": 6, "PIE": 3},
        "speed_base": 15,
        "attack_damage": 34, "attack_type": "melee", "phys_type": "slashing",
        "accuracy_bonus": 3,
        "preferred_row": FRONT,
        "ai_type": "aggressive",
        "xp_reward": 450, "gold_reward": _coin(15, 35),
        "resistances": _res(),
        "status_immunities": [],
        "abilities": [],
        "loot_table": [
            {"drop_chance": 0.18, "item": _sword(
                "Iron Contract Blade", "Heavy Longsword", 10, 100,
                "Mercenary-issued iron sword. Functional, boring, deadly.")},
            {"drop_chance": 0.08, "item": _leather(6)},
        ],
        "description_tiers": {
            0: "An armored human with professional posture and cold eyes.",
            1: "Sellsword",
            2: "Sellsword — professional merc. Better discipline than a bandit, about as ruthless.",
        },
    },

    "Mercenary Scout": {
        "name": "Mercenary Scout",
        "hp": 105, "defense": 9, "magic_resist": 5,
        "stats": {"STR": 10, "DEX": 15, "CON": 9, "INT": 9, "WIS": 10, "PIE": 3},
        "speed_base": 20,
        "attack_damage": 26, "attack_type": "ranged", "phys_type": "piercing",
        "accuracy_bonus": 6,
        "preferred_row": BACK,
        "ai_type": "ranged",
        "xp_reward": 380, "gold_reward": _coin(12, 28),
        "resistances": _res(),
        "status_immunities": [],
        "abilities": ["enemy_pinning_shot"],
        "loot_table": [
            {"drop_chance": 0.15, "item": {
                "name": "Reinforced Shortbow", "type": "weapon", "subtype": "Shortbow",
                "rarity": "common", "damage_stat": {"DEX": 0.35, "STR": 0.08},
                "damage": 17, "phys_type": "piercing",
                "identify_difficulty": 1,
                "unidentified_name": "Well-made Bow", "unidentified_desc": "A compact bow, better than average.",
                "appraised_name": "Mercenary Shortbow", "material_desc": "Laminated hardwood, professionally strung.",
                "magic_desc": "No magical properties.", "estimated_value": 105,
                "description": "Standard-issue mercenary shortbow. Reliable."}},
        ],
        "description_tiers": {
            0: "A nimble figure in dark leathers, watching your every move.",
            1: "Mercenary Scout",
            2: "Mercenary Scout — fast and accurate, can pin targets in place.",
        },
    },

    "Mercenary Monk": {
        "name": "Mercenary Monk",
        "hp": 128, "defense": 11, "magic_resist": 8,
        "stats": {"STR": 12, "DEX": 14, "CON": 11, "INT": 8, "WIS": 12, "PIE": 5},
        "speed_base": 19,
        "attack_damage": 28, "attack_type": "melee", "phys_type": "blunt",
        "accuracy_bonus": 5,
        "preferred_row": FRONT,
        "ai_type": "tactical",
        "xp_reward": 500, "gold_reward": _coin(10, 24),
        "resistances": _res(nature=RESISTANT),
        "status_immunities": ["Stunned"],
        "abilities": ["enemy_stunning_blow"],
        "loot_table": [
            {"drop_chance": 0.12, "item": {
                "name": "Worn Prayer Beads", "type": "accessory", "slot": "neck", "subtype": "trinket",
                "rarity": "uncommon", "identify_difficulty": 2,
                "unidentified_name": "Carved Beads", "unidentified_desc": "Smooth wooden beads on a cord.",
                "appraised_name": "Monk's Focus Beads", "material_desc": "Rosewood beads.",
                "magic_desc": "Faint calming resonance.", "estimated_value": 90,
                "description": "Beads used for focus meditation. Still hold traces of ki."}},
        ],
        "description_tiers": {
            0: "A shaven-headed fighter with taped fists and an unnerving calm.",
            1: "Mercenary Monk",
            2: "Mercenary Monk — trained brawler, stunning strikes, immune to being stunned.",
        },
    },

    "Mercenary War-Cleric": {
        "name": "Mercenary War-Cleric",
        "hp": 132, "defense": 12, "magic_resist": 12,
        "stats": {"STR": 11, "DEX": 8,  "CON": 11, "INT": 8, "WIS": 14, "PIE": 12},
        "speed_base": 13,
        "attack_damage": 26, "attack_type": "melee", "phys_type": "blunt",
        "accuracy_bonus": 2,
        "preferred_row": MID,
        "ai_type": "support",
        "xp_reward": 550, "gold_reward": _coin(14, 30),
        "resistances": _res(divine=RESISTANT),
        "status_immunities": ["Cursed"],
        "abilities": ["enemy_minor_heal", "enemy_smite"],
        "loot_table": [
            {"drop_chance": 0.18, "item": {
                "name": "Mercenary's Iron Mace", "type": "weapon", "slot": "weapon", "subtype": "Mace",
                "rarity": "common", "damage_stat": {"STR": 0.4},
                "damage": 19, "phys_type": "blunt",
                "identify_difficulty": 1,
                "unidentified_name": "Heavy Mace", "unidentified_desc": "A sturdy iron mace.",
                "appraised_name": "Iron War Mace", "material_desc": "Cast iron head, hardwood haft.",
                "magic_desc": "No magical properties.", "estimated_value": 95,
                "description": "A mercenary cleric's tool of trade. Heals allies, bludgeons enemies."}},
            {"drop_chance": 0.15, "item": {
                "name": "Vial of Holy Water", "type": "consumable", "subtype": "potion",
                "rarity": "uncommon", "identify_difficulty": 1, "identified": False,
                "unidentified_name": "Clear Vial", "unidentified_desc": "A sealed vial of colorless liquid.",
                "appraised_name": "Holy Water", "damage_undead": 40,
                "description": "Blessed water. Deals divine damage to undead."}},
        ],
        "description_tiers": {
            0: "An armored figure touching a symbol at their neck, eyes lit with battle-calm.",
            1: "Mercenary War-Cleric",
            2: "Mercenary War-Cleric — dangerous support, heals allies, smites with divine force.",
        },
    },

    "Mercenary Spellblade": {
        "name": "Mercenary Spellblade",
        "hp": 122, "defense": 11, "magic_resist": 9,
        "stats": {"STR": 12, "DEX": 12, "CON": 10, "INT": 12, "WIS": 7, "PIE": 4},
        "speed_base": 16,
        "attack_damage": 30, "attack_type": "melee", "phys_type": "slashing",
        "accuracy_bonus": 3,
        "preferred_row": FRONT,
        "ai_type": "tactical",
        "xp_reward": 520, "gold_reward": _coin(18, 38),
        "resistances": _res(arcane=RESISTANT),
        "status_immunities": [],
        "abilities": ["enemy_arcane_slash"],
        "loot_table": [
            {"drop_chance": 0.22, "item": {
                "name": "Rune-Etched Sword", "type": "weapon", "slot": "weapon", "subtype": "Long Sword",
                "rarity": "uncommon", "damage_stat": {"STR": 0.3, "DEX": 0.12},
                "damage": 20, "phys_type": "slashing",
                "identify_difficulty": 3, "element": "arcane",
                "unidentified_name": "Glowing Blade", "unidentified_desc": "A sword with faintly glowing runes.",
                "appraised_name": "Arcane Longsword", "material_desc": "Steel blade with arcane runes.",
                "magic_desc": "Arcane enchantment — blade channels magic.", "estimated_value": 180,
                "description": "A sword whose edge crackles with channeled arcane energy."}},
        ],
        "description_tiers": {
            0: "A warrior whose sword glows with unsteady light.",
            1: "Mercenary Spellblade",
            2: "Mercenary Spellblade — melee fighter who channels arcane energy into every strike.",
        },
    },

    # ══════════════════════════════════════════════════════════
    #  FACTION: ASHENMOOR CULTISTS  (ruins / pale coast)
    # ══════════════════════════════════════════════════════════

    "Cultist Initiate": {
        "name": "Cultist Initiate",
        "hp": 78, "defense": 4, "magic_resist": 8,
        "stats": {"STR": 6,  "DEX": 8,  "CON": 7,  "INT": 12, "WIS": 9, "PIE": 6},
        "speed_base": 13,
        "attack_damage": 22, "attack_type": "magic", "phys_type": "shadow",
        "accuracy_bonus": 2,
        "preferred_row": MID,
        "ai_type": "caster",
        "xp_reward": 60, "gold_reward": _coin(5, 14),
        "resistances": _res(shadow=RESISTANT, divine=VULNERABLE),
        "status_immunities": [],
        "abilities": ["enemy_shadow_bolt"],
        "loot_table": [
            {"drop_chance": 0.18, "item": {
                "name": "Mana Crystal", "type": "material", "subtype": "reagent",
                "rarity": "uncommon", "quantity": 1, "identified": True,
                "description": "A dense crystal of condensed arcane energy. Recharges 5 charges on a focus weapon."}},

            {"drop_chance": 0.20, "item": {
                "name": "Cultist's Sigil", "type": "material", "subtype": "arcane",
                "rarity": "uncommon", "tier": 1, "identify_difficulty": 2,
                "unidentified_name": "Carved Token", "unidentified_desc": "A carved stone with strange markings.",
                "appraised_name": "Shadow Sigil", "material_desc": "Stone imbued with shadow energy.",
                "magic_desc": "Dark magical resonance.", "estimated_value": 18,
                "description": "A token of cult membership. Still hums with shadow energy."}},
        ],
        "description_tiers": {
            0: "A hooded figure in black robes, muttering in an unfamiliar tongue.",
            1: "Cultist Initiate",
            2: "Cultist Initiate — low-tier shadow mage, weak alone, dangerous in numbers.",
        },
    },

    "Cultist Warrior": {
        "name": "Cultist Warrior",
        "hp": 118, "defense": 11, "magic_resist": 7,
        "stats": {"STR": 13, "DEX": 10, "CON": 11, "INT": 7, "WIS": 8, "PIE": 6},
        "speed_base": 14,
        "attack_damage": 30, "attack_type": "melee", "phys_type": "slashing",
        "accuracy_bonus": 2,
        "preferred_row": FRONT,
        "ai_type": "aggressive",
        "xp_reward": 80, "gold_reward": _coin(8, 18),
        "resistances": _res(shadow=RESISTANT, divine=VULNERABLE),
        "status_immunities": [],
        "abilities": [],
        "loot_table": [
            {"drop_chance": 0.14, "item": _sword(
                "Ruin-Black Blade", "Dark Sword", 9, 95,
                "Blackened iron blade engraved with cult markings.")},
            {"drop_chance": 0.10, "item": _leather(5)},
        ],
        "description_tiers": {
            0: "A black-armored fighter with a symbol burned into the breastplate.",
            1: "Cultist Warrior",
            2: "Cultist Warrior — devoted melee fighter, resists shadow, vulnerable to divine.",
        },
    },

    "Cultist Hexblade": {
        "name": "Cultist Hexblade",
        "hp": 102, "defense": 9, "magic_resist": 11,
        "stats": {"STR": 10, "DEX": 11, "CON": 9,  "INT": 13, "WIS": 10, "PIE": 7},
        "speed_base": 15,
        "attack_damage": 28, "attack_type": "melee", "phys_type": "shadow",
        "accuracy_bonus": 3,
        "preferred_row": FRONT,
        "ai_type": "tactical",
        "xp_reward": 96, "gold_reward": _coin(12, 24),
        "resistances": _res(shadow=RESISTANT, divine=VULNERABLE),
        "status_immunities": [],
        "abilities": ["enemy_shadow_bolt", "enemy_weaken"],
        "loot_table": [
            {"drop_chance": 0.18, "item": {
                "name": "Mana Crystal", "type": "material", "subtype": "reagent",
                "rarity": "uncommon", "quantity": 1, "identified": True,
                "description": "A dense crystal of condensed arcane energy. Recharges 5 charges on a focus weapon."}},

            {"drop_chance": 0.20, "item": {
                "name": "Hexblade Saber", "type": "weapon", "slot": "weapon", "subtype": "Long Sword",
                "rarity": "uncommon", "damage_stat": {"STR": 0.3, "DEX": 0.12},
                "damage": 19, "phys_type": "slashing",
                "identify_difficulty": 3, "element": "shadow",
                "unidentified_name": "Dark-stained Blade",
                "unidentified_desc": "A sword with an oil-dark blade that seems to absorb light.",
                "appraised_name": "Shadow-Etched Saber",
                "material_desc": "Steel blade treated with shadow essence.",
                "magic_desc": "Shadow enchantment — weakens divine resistance.",
                "estimated_value": 170, "description": "A saber that inflicts shadow-infused wounds."}},
        ],
        "description_tiers": {
            0: "A warrior whose weapon seems to leave shadows hanging in the air.",
            1: "Cultist Hexblade",
            2: "Cultist Hexblade — melee fighter with shadow enchantments, can weaken targets.",
        },
    },

    "Cult Sorcerer": {
        "name": "Cult Sorcerer",
        "hp": 80, "defense": 5, "magic_resist": 16,
        "stats": {"STR": 5,  "DEX": 9,  "CON": 7,  "INT": 16, "WIS": 10, "PIE": 7},
        "speed_base": 12,
        "attack_damage": 38, "attack_type": "magic", "phys_type": "shadow",
        "accuracy_bonus": 4,
        "preferred_row": BACK,
        "ai_type": "caster",
        "xp_reward": 124, "gold_reward": _coin(15, 30),
        "resistances": _res(shadow=RESISTANT, arcane=RESISTANT, divine=VERY_VULNERABLE),
        "status_immunities": [],
        "abilities": ["enemy_shadow_bolt", "enemy_fireball", "enemy_mass_weaken"],
        "loot_table": [
            {"drop_chance": 0.25, "item": _staff(
                "Sorcerer's Blackwood Staff", 7, 110,
                "A staff carved from shadowwood, still resonating with channeled power.")},
            {"drop_chance": 0.30, "item": {
                "name": "Shadow Essence", "type": "material", "subtype": "arcane",
                "rarity": "uncommon", "tier": 2, "identify_difficulty": 3,
                "unidentified_name": "Dark Vial", "unidentified_desc": "A small vial of darkness that doesn't dissipate.",
                "appraised_name": "Bottled Shadow Essence",
                "material_desc": "Distilled shadow energy. Tier 2 enchanting material.",
                "magic_desc": "Strong shadow resonance.", "estimated_value": 40,
                "description": "Refined shadow essence used for dark enchantments."}},
        ],
        "description_tiers": {
            0: "A figure floating slightly above the ground, trailing wisps of darkness.",
            1: "Cult Sorcerer",
            2: "Cult Sorcerer — powerful shadow caster. Devastatingly weak to divine magic.",
        },
    },

    "High Cultist": {
        "name": "High Cultist",
        "hp": 155, "defense": 12, "magic_resist": 14,
        "stats": {"STR": 10, "DEX": 9, "CON": 11, "INT": 14, "WIS": 13, "PIE": 11},
        "speed_base": 13,
        "attack_damage": 36, "attack_type": "magic", "phys_type": "shadow",
        "accuracy_bonus": 4,
        "preferred_row": BACK,
        "ai_type": "support",
        "xp_reward": 160, "gold_reward": _coin(25, 55),
        "resistances": _res(shadow=IMMUNE, divine=VERY_VULNERABLE),
        "status_immunities": ["Cursed", "Stunned"],
        "abilities": ["enemy_shadow_bolt", "enemy_minor_heal", "enemy_mass_weaken", "enemy_smite"],
        "loot_table": [
            {"drop_chance": 0.18, "item": {
                "name": "Mana Crystal", "type": "material", "subtype": "reagent",
                "rarity": "uncommon", "quantity": 1, "identified": True,
                "description": "A dense crystal of condensed arcane energy. Recharges 5 charges on a focus weapon."}},

            {"drop_chance": 0.35, "item": {
                "name": "High Cultist's Grimoire", "type": "weapon", "slot": "weapon", "subtype": "Staff", "max_charges": 30,
                "rarity": "rare", "damage_stat": {"STR": 0.16, "INT": 0.24},
                "damage": 18, "phys_type": "shadow",
                "identify_difficulty": 4, "element": "shadow",
                "unidentified_name": "Black Tome", "unidentified_desc": "A heavy book sealed with dark sigils.",
                "appraised_name": "Tome of Unmaking",
                "material_desc": "Bound in shadow-cured leather.",
                "magic_desc": "Shadow enchantment — amplifies dark magic.",
                "estimated_value": 320, "description": "A grimoire of shadow rituals."}},
            {"drop_chance": 0.20, "item": _coin_pouch(30, 70)},
        ],
        "description_tiers": {
            0: "A tall robed figure whose shadow moves independently of their body.",
            1: "High Cultist",
            2: "High Cultist — elite leader, immune to shadow, heals allies, deadly in divine-poor parties.",
        },
    },

    # ══════════════════════════════════════════════════════════
    #  FACTION: CORRUPTED GUARD  (undead soldiers, crypt/throne)
    # ══════════════════════════════════════════════════════════

    "Crypt Soldier": {
        "name": "Crypt Soldier",
        "hp": 122, "defense": 13, "magic_resist": 5,
        "stats": {"STR": 13, "DEX": 7, "CON": 12, "INT": 4, "WIS": 4, "PIE": 2},
        "speed_base": 11,
        "attack_damage": 30, "attack_type": "melee", "phys_type": "slashing",
        "accuracy_bonus": 2,
        "preferred_row": FRONT,
        "ai_type": "aggressive",
        "xp_reward": 80, "gold_reward": _coin(0, 5),
        "resistances": _res(shadow=RESISTANT, divine=VULNERABLE,
                            poison=RESISTANT, blunt=NEUTRAL),
        "status_immunities": ["Poisoned"],
        "tags": ["undead"],
        "abilities": [],
        "loot_table": [
            {"drop_chance": 0.10, "item": {
                "name": "Corroded Sword", "type": "weapon", "slot": "weapon", "subtype": "Long Sword",
                "rarity": "common", "damage_stat": {"STR": 0.3, "DEX": 0.12},
                "damage": 17, "phys_type": "slashing",
                "identify_difficulty": 1,
                "unidentified_name": "Rusted Blade", "unidentified_desc": "A heavily corroded longsword.",
                "appraised_name": "Corroded Iron Sword", "material_desc": "Iron nearly eaten through by rust.",
                "magic_desc": "No magical properties.", "estimated_value": 50,
                "description": "A sword long-dead along with its owner. Still holds an edge, barely."}},
        ],
        "description_tiers": {
            0: "An armored figure moving with mechanical wrongness, jaw slack.",
            1: "Crypt Soldier",
            2: "Corrupted Soldier — undead ex-guard, slow but armored. Immune to poison.",
        },
    },

    "Crypt Ranger": {
        "name": "Crypt Ranger",
        "hp": 102, "defense": 8, "magic_resist": 5,
        "stats": {"STR": 9, "DEX": 13, "CON": 9, "INT": 5, "WIS": 6, "PIE": 2},
        "speed_base": 14,
        "attack_damage": 26, "attack_type": "ranged", "phys_type": "piercing",
        "accuracy_bonus": 5,
        "preferred_row": BACK,
        "ai_type": "ranged",
        "xp_reward": 72, "gold_reward": _coin(0, 4),
        "resistances": _res(shadow=RESISTANT, divine=VULNERABLE),
        "status_immunities": ["Poisoned"],
        "tags": ["undead"],
        "abilities": [],
        "loot_table": [
            {"drop_chance": 0.12, "item": {
                "name": "Blackened Arrow Bundle", "type": "consumable", "subtype": "ammo",
                "rarity": "uncommon", "quantity": 5, "identify_difficulty": 0, "identified": True,
                "description": "Arrows stained with grave-dark ichor."}},
        ],
        "description_tiers": {
            0: "A figure that was once a forest scout, eyes now blank and milky.",
            1: "Crypt Ranger",
            2: "Corrupted Ranger — undead archer, accurate and relentless from back row.",
        },
    },

    "Crypt Paladin": {
        "name": "Crypt Paladin",
        "hp": 175, "defense": 16, "magic_resist": 10,
        "stats": {"STR": 15, "DEX": 7, "CON": 14, "INT": 7, "WIS": 10, "PIE": 4},
        "speed_base": 11,
        "attack_damage": 38, "attack_type": "melee", "phys_type": "slashing",
        "accuracy_bonus": 3,
        "preferred_row": FRONT,
        "ai_type": "guardian",
        "xp_reward": 150, "gold_reward": _coin(0, 8),
        "resistances": _res(shadow=RESISTANT, divine=VULNERABLE,
                            fire=RESISTANT, ice=RESISTANT),
        "status_immunities": ["Poisoned", "Stunned", "Cursed"],
        "tags": ["undead"],
        "abilities": ["enemy_cleave", "enemy_war_cry"],
        "loot_table": [
            {"drop_chance": 0.18, "item": {
                "name": "Tarnished Paladin Shield", "type": "armor", "slot": "off_hand", "subtype": "Shield",
                "rarity": "uncommon", "defense": 4, "phys_type": "none",
                "identify_difficulty": 2,
                "unidentified_name": "Heavy Shield", "unidentified_desc": "A large kite shield, dented and tarnished.",
                "appraised_name": "Corrupted Knight's Shield", "material_desc": "Iron-faced hardwood.",
                "magic_desc": "Dark residual energy.", "estimated_value": 135,
                "description": "A paladin's shield, corrupted like its former owner."}},
        ],
        "description_tiers": {
            0: "A massive armored figure whose holy symbols are inverted and blackened.",
            1: "Crypt Paladin",
            2: "Corrupted Paladin — former holy warrior, extremely durable, cleaves multiple targets.",
        },
    },

    "Crypt Archmage": {
        "name": "Crypt Archmage",
        "hp": 95, "defense": 7, "magic_resist": 18,
        "stats": {"STR": 5, "DEX": 8, "CON": 8, "INT": 17, "WIS": 11, "PIE": 4},
        "speed_base": 11,
        "attack_damage": 48, "attack_type": "magic", "phys_type": "arcane",
        "accuracy_bonus": 5,
        "preferred_row": BACK,
        "ai_type": "caster",
        "xp_reward": 180, "gold_reward": _coin(0, 10),
        "resistances": _res(shadow=RESISTANT, arcane=RESISTANT, divine=VULNERABLE,
                            fire=RESISTANT, ice=RESISTANT),
        "status_immunities": ["Poisoned", "Cursed"],
        "tags": ["undead"],
        "abilities": ["enemy_fireball", "enemy_arcane_slash", "enemy_shadow_bolt"],
        "loot_table": [
            {"drop_chance": 0.18, "item": {
                "name": "Mana Crystal", "type": "material", "subtype": "reagent",
                "rarity": "uncommon", "quantity": 1, "identified": True,
                "description": "A dense crystal of condensed arcane energy. Recharges 5 charges on a focus weapon."}},

            {"drop_chance": 0.22, "item": {
                "name": "Crypt Archmage's Orb", "type": "weapon", "slot": "weapon", "subtype": "Orb", "max_charges": 30,
                "rarity": "rare", "damage_stat": {"INT": 0.24, "WIS": 0.16},
                "damage": 20, "phys_type": "arcane",
                "identify_difficulty": 4, "element": "arcane",
                "unidentified_name": "Cracked Orb", "unidentified_desc": "A sphere of glass criss-crossed with dark veins.",
                "appraised_name": "Void Orb",
                "material_desc": "Crystal infused with void energy.",
                "magic_desc": "Arcane and shadow enchantment.",
                "estimated_value": 310, "description": "A mage's focus orb, corrupted by prolonged shadow exposure."}},
        ],
        "description_tiers": {
            0: "A desiccated robed figure crackling with unstable arcane energy.",
            1: "Crypt Archmage",
            2: "Corrupted Archmage — high-tier undead caster. Massive spell damage, very fragile.",
        },
    },
}


# ══════════════════════════════════════════════════════════════
#  ENCOUNTERS
# ══════════════════════════════════════════════════════════════

HUMANOID_ENCOUNTERS = {

    # ── Bandit encounters ──────────────────────────────────
    "bandit_skirmish": {"name": "Bandit Skirmish", "difficulty": "easy",
        "groups": [{"enemy": "Bandit Fighter", "count": 2, "row": FRONT},
                   {"enemy": "Bandit Thief",   "count": 1, "row": FRONT}]},

    "bandit_ambush": {"name": "Bandit Ambush", "difficulty": "medium",
        "groups": [{"enemy": "Bandit Fighter", "count": 2, "row": FRONT},
                   {"enemy": "Bandit Archer",  "count": 2, "row": BACK}]},

    "bandit_with_mage": {"name": "Armed Bandits", "difficulty": "medium",
        "groups": [{"enemy": "Bandit Fighter", "count": 2, "row": FRONT},
                   {"enemy": "Bandit Mage",    "count": 1, "row": BACK}]},

    "bandit_gang": {"name": "Bandit Gang", "difficulty": "hard",
        "groups": [{"enemy": "Bandit Fighter", "count": 2, "row": FRONT},
                   {"enemy": "Bandit Thief",   "count": 1, "row": FRONT},
                   {"enemy": "Bandit Archer",  "count": 2, "row": BACK}]},

    "bandit_warband": {"name": "Bandit Warband", "difficulty": "hard",
        "groups": [{"enemy": "Bandit Captain", "count": 1, "row": FRONT},
                   {"enemy": "Bandit Fighter", "count": 2, "row": FRONT},
                   {"enemy": "Bandit Mage",    "count": 1, "row": BACK}]},

    "bandit_crossbows": {"name": "Crossbow Ambush", "difficulty": "medium",
        "groups": [{"enemy": "Bandit Archer",  "count": 3, "row": BACK},
                   {"enemy": "Bandit Thief",   "count": 1, "row": FRONT}]},

    # ── Mercenary encounters ───────────────────────────────
    "merc_patrol": {"name": "Mercenary Patrol", "difficulty": "medium",
        "groups": [{"enemy": "Sellsword",          "count": 2, "row": FRONT},
                   {"enemy": "Mercenary Scout",    "count": 1, "row": BACK}]},

    "merc_squad": {"name": "Mercenary Squad", "difficulty": "hard",
        "groups": [{"enemy": "Sellsword",          "count": 2, "row": FRONT},
                   {"enemy": "Mercenary Monk",     "count": 1, "row": FRONT},
                   {"enemy": "Mercenary Scout",    "count": 1, "row": BACK}]},

    "merc_warband": {"name": "Mercenary Warband", "difficulty": "hard",
        "groups": [{"enemy": "Sellsword",          "count": 2, "row": FRONT},
                   {"enemy": "Mercenary War-Cleric","count": 1, "row": MID},
                   {"enemy": "Mercenary Spellblade","count": 1, "row": FRONT}]},

    "merc_elite": {"name": "Elite Mercenaries", "difficulty": "hard",
        "groups": [{"enemy": "Mercenary Spellblade","count": 1, "row": FRONT},
                   {"enemy": "Mercenary War-Cleric","count": 1, "row": MID},
                   {"enemy": "Mercenary Scout",    "count": 2, "row": BACK}]},

    # ── Cultist encounters ─────────────────────────────────
    "cult_patrol": {"name": "Cult Patrol", "difficulty": "medium",
        "groups": [{"enemy": "Cultist Warrior",  "count": 2, "row": FRONT},
                   {"enemy": "Cultist Initiate", "count": 1, "row": MID}]},

    "cult_ritual": {"name": "Interrupted Ritual", "difficulty": "medium",
        "groups": [{"enemy": "Cultist Initiate", "count": 3, "row": MID},
                   {"enemy": "Cultist Warrior",  "count": 1, "row": FRONT}]},

    "cult_warband": {"name": "Cult Warband", "difficulty": "hard",
        "groups": [{"enemy": "Cultist Warrior",  "count": 2, "row": FRONT},
                   {"enemy": "Cultist Hexblade", "count": 1, "row": FRONT},
                   {"enemy": "Cultist Initiate", "count": 2, "row": MID}]},

    "cult_with_sorcerer": {"name": "Cult Coven", "difficulty": "hard",
        "groups": [{"enemy": "Cultist Warrior",  "count": 2, "row": FRONT},
                   {"enemy": "Cultist Hexblade", "count": 1, "row": FRONT},
                   {"enemy": "Cult Sorcerer",    "count": 1, "row": BACK}]},

    "cult_elite": {"name": "High Cult Guard", "difficulty": "hard",
        "groups": [{"enemy": "High Cultist",     "count": 1, "row": BACK},
                   {"enemy": "Cultist Hexblade", "count": 2, "row": FRONT},
                   {"enemy": "Cultist Initiate", "count": 2, "row": MID}]},

    # ── Corrupted Guard encounters ─────────────────────────
    "crypt_patrol": {"name": "Crypt Guard Patrol", "difficulty": "medium",
        "groups": [{"enemy": "Crypt Soldier", "count": 3, "row": FRONT}]},

    "crypt_mixed": {"name": "Crypt Guard", "difficulty": "hard",
        "groups": [{"enemy": "Crypt Soldier", "count": 2, "row": FRONT},
                   {"enemy": "Crypt Ranger",  "count": 2, "row": BACK}]},

    "crypt_heavy": {"name": "Crypt Knights", "difficulty": "hard",
        "groups": [{"enemy": "Crypt Paladin", "count": 1, "row": FRONT},
                   {"enemy": "Crypt Soldier", "count": 2, "row": FRONT}]},

    "crypt_elite": {"name": "Crypt Elite", "difficulty": "hard",
        "groups": [{"enemy": "Crypt Paladin",  "count": 1, "row": FRONT},
                   {"enemy": "Crypt Archmage", "count": 1, "row": BACK},
                   {"enemy": "Crypt Soldier",  "count": 1, "row": FRONT}]},
}


# ══════════════════════════════════════════════════════════════
#  UPDATED DUNGEON ENCOUNTER TABLE ADDITIONS
# ══════════════════════════════════════════════════════════════

HUMANOID_ENCOUNTER_TABLE_UPDATES = {
    "abandoned_mine": {
        1: ["medium_goblins", "bandit_skirmish", "bandit_ambush"],
        2: ["hard_mixed", "orc_patrol", "bandit_with_mage", "merc_patrol"],
        3: ["orc_patrol", "bandit_warband", "merc_squad"],
    },
    "sunken_crypt": {
        1: ["hard_goblins", "hard_mixed", "crypt_patrol"],
        2: ["hard_mixed", "crypt_mixed", "merc_patrol"],
        3: ["crypt_heavy", "crypt_elite", "merc_warband"],
    },
    "ruins_ashenmoor": {
        1: ["hard_mixed", "cult_patrol", "bandit_gang"],
        2: ["cult_ritual", "cult_warband", "merc_squad"],
        3: ["cult_with_sorcerer", "cult_elite", "merc_elite"],
    },
    "pale_coast": {
        1: ["pc_shades", "cult_patrol"],
        2: ["pc_drowned", "cult_warband", "crypt_mixed"],
        3: ["cult_elite", "crypt_elite", "cult_with_sorcerer"],
    },
}


# ── Fix missing slot fields on all loot items ─────────────────
from core.item_slot_fixer import fix_loot_table as _fix_loot
for _eid, _edata in HUMANOID_ENEMIES.items():
    if _edata.get("loot_table"):
        _fix_loot(_edata["loot_table"])
