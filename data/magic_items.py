"""
Realm of Shadows — Magic Items
Unique items found in secret rooms and dropped by bosses.
Organized by tier (1=early, 2=mid, 3=late).
"""

# ══════════════════════════════════════════════════════════
#  SECRET ROOM ITEMS — Found in hidden chests
# ══════════════════════════════════════════════════════════

SECRET_ITEMS_T1 = [
    {"name": "Ring of Minor Fortitude", "appraised_name": "Ring of Minor Fortitude", "type": "accessory", "slot": "accessory1",
     "subtype": "ring", "rarity": "uncommon",
     "effect": {"con_bonus": 2, "max_hp_bonus": 10},
     "description": "A plain iron ring that makes the wearer feel hardier. +2 CON, +10 max HP.",
     "identified": False, "estimated_value": 60},

    {"name": "Boots of Quiet Steps", "appraised_name": "Boots of Quiet Steps", "type": "armor", "slot": "feet",
     "subtype": "boots", "rarity": "uncommon",
     "defense": 1, "speed_bonus": 2,
     "effect": {"dex_bonus": 1},
     "description": "Soft leather boots. +1 DEX, +2 speed. Helps avoid encounters.",
     "identified": False, "estimated_value": 55},

    {"name": "Cloak of Shadows", "appraised_name": "Cloak of Shadows", "type": "armor", "slot": "body",
     "subtype": "cloak", "rarity": "uncommon", "armor_tier": "clothing",
     "defense": 2, "magic_resist": 3,
     "effect": {"dex_bonus": 1},
     "description": "A dark cloak that seems to drink in light. +1 DEX, +3 magic resist.",
     "identified": False, "estimated_value": 70},

    {"name": "Wand of Sparks", "appraised_name": "Wand of Sparks", "type": "weapon", "slot": "weapon",
     "subtype": "Wand", "rarity": "uncommon", "damage": 4,
     "damage_stat": {"INT": 0.8},
     "phys_type": "blunt", "range": "melee",
     "spell_bonus": 3,
     "enchant_element": "lightning", "enchant_bonus": 3,
     "description": "A wand crackling with static. +3 spell power, deals lightning damage.",
     "identified": False, "estimated_value": 65},

    {"name": "Amulet of the Owl", "appraised_name": "Amulet of the Owl", "type": "accessory", "slot": "accessory1",
     "subtype": "amulet", "rarity": "uncommon",
     "effect": {"wis_bonus": 2, "int_bonus": 1},
     "description": "A silver owl pendant. +2 WIS, +1 INT.",
     "identified": False, "estimated_value": 55},
    {"name": "Scroll of Remove Curse", "appraised_name": "Scroll of Remove Curse",
     "type": "consumable", "subtype": "scroll", "effect": "remove_curse",
     "rarity": "uncommon",
     "description": "Lifts all curses from one character, freeing any cursed equipment.",
     "identified": True, "estimated_value": 75},
]

SECRET_ITEMS_T2 = [
    {"name": "Firebrand Blade", "appraised_name": "Firebrand Blade", "type": "weapon", "slot": "weapon",
     "subtype": "Longsword", "rarity": "rare", "damage": 16,
     "damage_stat": {"STR": 0.7, "DEX": 0.3},
     "phys_type": "slashing", "range": "melee",
     "enchant_element": "fire", "enchant_bonus": 5, "enchant_name": "Flame",
     "description": "A longsword wreathed in faint flames. Deals bonus fire damage.",
     "identified": False, "estimated_value": 160},

    {"name": "Frostbite Dagger", "appraised_name": "Frostbite Dagger", "type": "weapon", "slot": "weapon",
     "subtype": "Dagger", "rarity": "rare", "damage": 12,
     "damage_stat": {"DEX": 1.0},
     "phys_type": "piercing", "range": "melee",
     "enchant_element": "ice", "enchant_bonus": 5, "enchant_name": "Frost",
     "effect": {"dex_bonus": 2},
     "description": "An ice-cold dagger. +2 DEX, bonus ice damage.",
     "identified": False, "estimated_value": 150},

    {"name": "Ring of the Battlemage", "appraised_name": "Ring of the Battlemage", "type": "accessory", "slot": "accessory1",
     "subtype": "ring", "rarity": "rare",
     "effect": {"int_bonus": 3, "str_bonus": 1},
     "description": "Worn by warrior-mages of the old Wardens. +3 INT, +1 STR.",
     "identified": False, "estimated_value": 140},

    {"name": "Shield of the Sentinel", "appraised_name": "Shield of the Sentinel", "type": "armor", "slot": "off_hand",
     "subtype": "shield", "rarity": "rare",
     "defense": 6, "magic_resist": 4,
     "effect": {"con_bonus": 1},
     "description": "An ancient shield that still hums with protective magic. +1 CON.",
     "identified": False, "estimated_value": 180},

    {"name": "Orb of Fading Sight", "appraised_name": "Orb of Fading Sight", "type": "accessory", "slot": "accessory1",
     "subtype": "orb", "rarity": "rare",
     "effect": {"int_bonus": 3, "wis_bonus": 2},
     "spell_bonus": 4,
     "description": "A dark crystal orb. Glimpses of the Fading swirl within. +3 INT, +2 WIS, +4 spell.",
     "identified": False, "estimated_value": 200},

    {"name": "Boots of the Wind", "appraised_name": "Boots of the Wind", "type": "armor", "slot": "feet",
     "subtype": "boots", "rarity": "rare",
     "defense": 2, "speed_bonus": 4,
     "effect": {"dex_bonus": 2},
     "description": "Enchanted boots that make the wearer swift as wind. +2 DEX, +4 speed.",
     "identified": False, "estimated_value": 170},

    {"name": "Crown of Clarity", "appraised_name": "Crown of Clarity", "type": "armor", "slot": "head",
     "subtype": "circlet", "rarity": "rare",
     "defense": 2, "magic_resist": 6,
     "effect": {"wis_bonus": 3},
     "description": "A silver circlet that clears the mind. +3 WIS, +6 magic resist.",
     "identified": False, "estimated_value": 190},

    {"name": "Gauntlets of Might", "appraised_name": "Gauntlets of Might", "type": "armor", "slot": "hands",
     "subtype": "gauntlets", "rarity": "rare",
     "defense": 3,
     "effect": {"str_bonus": 3},
     "description": "Heavy gauntlets that make your blows land harder. +3 STR.",
     "identified": False, "estimated_value": 160},
]

SECRET_ITEMS_T3 = [
    {"name": "Warden's Oath", "appraised_name": "Warden's Oath", "type": "weapon", "slot": "weapon",
     "subtype": "Longsword", "rarity": "epic", "damage": 18,
     "damage_stat": {"STR": 0.7, "DEX": 0.3},
     "phys_type": "slashing", "range": "melee",
     "enchant_element": "divine", "enchant_bonus": 6, "enchant_name": "Holy",
     "effect": {"str_bonus": 2, "pie_bonus": 2},
     "description": "A holy blade of the old Wardens. +2 STR, +2 PIE, divine damage.",
     "identified": False, "estimated_value": 350},

    {"name": "Staff of the Fading", "appraised_name": "Staff of the Fading", "type": "weapon", "slot": "weapon",
     "subtype": "Staff", "rarity": "epic", "damage": 8,
     "damage_stat": {"INT": 0.6, "STR": 0.4},
     "phys_type": "blunt", "range": "melee",
     "spell_bonus": 8,
     "enchant_element": "shadow", "enchant_bonus": 6, "enchant_name": "Shadow",
     "effect": {"int_bonus": 4},
     "description": "A twisted staff that channels the Fading itself. +4 INT, +8 spell, shadow damage.",
     "identified": False, "estimated_value": 400},

    {"name": "Aegis of Dawn", "appraised_name": "Aegis of Dawn", "type": "armor", "slot": "off_hand",
     "subtype": "shield", "rarity": "epic",
     "defense": 8, "magic_resist": 8,
     "effect": {"con_bonus": 2, "pie_bonus": 2},
     "enchant_resist": "shadow", "enchant_resist_bonus": 5,
     "description": "A radiant shield that repels darkness. +2 CON, +2 PIE, shadow resist.",
     "identified": False, "estimated_value": 450},
]


# ══════════════════════════════════════════════════════════
#  BOSS LOOT — Guaranteed unique drops per boss
# ══════════════════════════════════════════════════════════

BOSS_BONUS_LOOT = {
    "Goblin King": [
        {"drop_chance": 0.40, "item": {
            "name": "Grak's Lucky Coin", "appraised_name": "Grak's Lucky Coin", "type": "accessory", "slot": "accessory1",
            "subtype": "trinket", "rarity": "uncommon",
            "effect": {"dex_bonus": 1},
            "description": "A strange coin Grak carried. Brings luck to the bearer. +1 DEX.",
            "identified": False, "estimated_value": 45}},
    ],
    "Giant Spider Queen": [
        {"drop_chance": 0.50, "item": {
            "name": "Venomstrike Fang", "appraised_name": "Venomstrike Fang", "type": "weapon", "slot": "weapon",
            "subtype": "Dagger", "rarity": "rare", "damage": 11,
            "phys_type": "piercing", "range": "melee",
            "enchant_element": "nature", "enchant_bonus": 4, "enchant_name": "Venom",
            "effect": {"dex_bonus": 2},
            "description": "A dagger carved from the Spider Queen's fang. +2 DEX, poison damage.",
            "identified": False, "estimated_value": 140}},
    ],
    "Undead Foreman": [
        {"drop_chance": 0.50, "item": {
            "name": "Foreman's Hard Hat", "appraised_name": "Foreman's Hard Hat", "type": "armor", "slot": "head",
            "subtype": "helmet", "rarity": "rare",
            "defense": 6, "magic_resist": 2,
            "effect": {"con_bonus": 2},
            "description": "A battered miner's helm, enchanted by the Fading. +2 CON.",
            "identified": False, "estimated_value": 120}},
    ],
    "Warden Revenant": [
        # Unique item — Korrath's blade (1.0 drop, but won't drop if party already has it)
        {"drop_chance": 1.0, "unique_key": "korrath_blade"},
        {"drop_chance": 0.60, "unique_key": "korrath_ring"},
    ],
    "Shadow Valdris": [
        {"drop_chance": 0.80, "item": {
            "name": "Valdris' Shadowstaff", "appraised_name": "Valdris' Shadowstaff", "type": "weapon", "slot": "weapon",
            "subtype": "Staff", "rarity": "epic", "damage": 8,
            "phys_type": "blunt", "range": "melee",
            "spell_bonus": 7,
            "enchant_element": "shadow", "enchant_bonus": 6, "enchant_name": "Shadow",
            "effect": {"int_bonus": 3},
            "description": "The shadow-echo of Valdris' staff. Crackling with dark power. +3 INT, +7 spell.",
            "identified": False, "estimated_value": 350}},
        {"drop_chance": 0.50, "item": {
            "name": "Fading Shard Amulet", "appraised_name": "Fading Shard Amulet", "type": "accessory", "slot": "accessory1",
            "subtype": "amulet", "rarity": "epic",
            "effect": {"int_bonus": 3, "wis_bonus": 2, "pie_bonus": 1},
            "magic_resist": 5,
            "description": "A crystallized fragment of the Fading. Whispers with dark knowledge. +3 INT, +2 WIS, +1 PIE.",
            "identified": False, "estimated_value": 400}},
    ],
    "Ashvar": [
        {"drop_chance": 1.0, "unique_key": "ashvar_robes"},
        {"drop_chance": 0.70, "unique_key": "ashvar_focus"},
    ],
    "Karreth": [
        # On kill path — scale drops as normal loot
        {"drop_chance": 0.80, "unique_key": "karreth_scale"},
    ],
    "The Pale Sentinel": [
        # On kill path — her buckler stays behind
        {"drop_chance": 1.0, "unique_key": "sirenne_buckler"},
    ],
    "The Last Keeper": [
        # Isle Keeper always drops its pendant
        {"drop_chance": 1.0, "unique_key": "keeper_pendant"},
    ],
    # NOTE: Lingering Will boss loot is defined in tower_data.py
}


def get_secret_item(floor_num, total_floors, rng, party=None):
    """Pick a random magic item appropriate to dungeon depth.
    Deep rooms (floor 3+) have a 12% chance to contain a unique item."""
    depth_ratio = floor_num / max(total_floors, 1)

    # Deep secret rooms: chance for unique items seeded into the world
    if depth_ratio >= 0.6 and rng.random() < 0.12:
        secret_uniques = ["shadowwalker_boots", "hearthwarden_helm"]
        rng.shuffle(secret_uniques)
        for key in secret_uniques:
            item = get_unique_item(key, party)
            if item:
                return item

    if depth_ratio >= 0.8 and rng.random() < 0.3:
        pool = SECRET_ITEMS_T3
    elif depth_ratio >= 0.4 or floor_num >= 2:
        pool = SECRET_ITEMS_T2
    else:
        pool = SECRET_ITEMS_T1

    # Rare chance to find a training book in a deep secret room
    if depth_ratio >= 0.6 and rng.random() < 0.08:   # 8% at mid-depth+
        return get_random_training_book()

    # Rare chance to find a relic in any secret room (deeper = better tier)
    if rng.random() < 0.10:   # 10% base relic chance
        max_tier = 3 if depth_ratio >= 0.8 else 2 if depth_ratio >= 0.4 else 1
        return get_random_relic(max_tier)

    return dict(rng.choice(pool))


def get_boss_bonus_drops(boss_name, rng, party=None):
    """Get bonus loot from a boss. Returns list of items that dropped."""
    bonus_table = BOSS_BONUS_LOOT.get(boss_name, [])
    drops = []
    for entry in bonus_table:
        if rng.random() < entry["drop_chance"]:
            if "unique_key" in entry:
                item = get_unique_item(entry["unique_key"], party)
                if item:
                    drops.append(item)
            elif "item" in entry:
                drops.append(dict(entry["item"]))
    return drops


# ═══════════════════════════════════════════════════════════════
#  CURSED ITEMS
#  These appear unidentified and are tempting — good stats that
#  hide a curse. Only revealed on identification or when equipped.
#  Require Remove Curse at the temple (100g) to unequip.
# ═══════════════════════════════════════════════════════════════

CURSED_ITEMS = [
    # ── Tier 1 — Early game traps ──
    {
        "name": "Ring of Misfortune",
        "type": "accessory", "subtype": "ring",
        "slot": "accessory",
        "rarity": "uncommon", "tier": 1,
        "cursed": True, "identified": False,
        "estimated_value": 80,
        "stat_bonus": {"DEX": 3},
        "stat_penalty": {"LCK": -5, "accuracy_bonus": -8},
        "description": "A silver ring that seems to shimmer with promise. "
                       "It pulls misfortune toward the wearer like a lodestone. "
                       "★ CURSED — cannot be removed without Remove Curse.",
        "lore": "Common thieves' trap — enchanted to look valuable, sold to the unwary.",
    },
    {
        "name": "Helm of Weakness",
        "type": "armor", "subtype": "helmet", "armor_slot": "head",
        "slot": "head",
        "rarity": "uncommon", "tier": 1,
        "cursed": True, "identified": False,
        "defense": 8,
        "estimated_value": 120,
        "stat_penalty": {"STR": -4, "attack_damage": -6},
        "description": "A well-crafted helm that slowly drains the wearer's strength. "
                       "★ CURSED — cannot be removed without Remove Curse.",
    },

    # ── Tier 2 — Mid-game ──
    {
        "name": "Shadowbind Gauntlets",
        "type": "armor", "subtype": "gloves", "armor_slot": "hands",
        "slot": "hands",
        "rarity": "rare", "tier": 2,
        "cursed": True, "identified": False,
        "defense": 12,
        "estimated_value": 220,
        "enchant_element": "shadow", "enchant_bonus": 6,
        "stat_penalty": {"speed_mod": -4},
        "description": "Gauntlets that crackle with shadow energy. Powerful, but they "
                       "slow the wearer's reactions as shadow seeps into the blood. "
                       "★ CURSED — cannot be removed without Remove Curse.",
        "lore": "Used by Valdris's early followers — gifts that became chains.",
    },
    {
        "name": "Greatsword of Bloodlust",
        "type": "weapon", "subtype": "sword",
        "slot": "main_hand",
        "rarity": "rare", "tier": 2,
        "cursed": True, "identified": False,
        "damage": 34,
        "damage_stat": {"STR": 0.7, "DEX": 0.3},
        "estimated_value": 300,
        "enchant_element": "fire", "enchant_bonus": 5,
        "stat_penalty": {"magic_resist": -10},
        "description": "A powerful blade that whispers of violence. Its edge is "
                       "unnaturally sharp, but it burns away the mind's defenses. "
                       "★ CURSED — cannot be removed without Remove Curse.",
    },

    # ── Tier 3 — Late game, high risk/reward ──
    {
        "name": "Crown of Dominion",
        "type": "armor", "subtype": "helmet", "armor_slot": "head",
        "slot": "head",
        "rarity": "legendary", "tier": 3,
        "cursed": True, "identified": False,
        "defense": 20,
        "estimated_value": 600,
        "stat_bonus": {"INT": 5, "WIS": 4, "magic_resist": 15},
        "stat_penalty": {"CON": -6},
        "description": "A crown of dark iron that amplifies magical power at the "
                       "cost of physical resilience. Those who wear it rarely "
                       "willingly remove it. ★ CURSED — cannot be removed without "
                       "Remove Curse.",
        "lore": "Said to have been worn by the last Warden Commander before the Fall. "
                "Whether it cursed him or he cursed it is debated.",
    },
    {
        "name": "Voidbound Shield",
        "type": "armor", "subtype": "shield", "armor_slot": "off_hand",
        "slot": "off_hand",
        "rarity": "legendary", "tier": 3,
        "cursed": True, "identified": False,
        "defense": 30,
        "estimated_value": 500,
        "enchant_resist": "shadow", "enchant_resist_bonus": 20,
        "stat_penalty": {"speed_mod": -6, "DEX": -3},
        "description": "An immense shield of void-steel that absorbs shadow damage "
                       "completely — but its weight seeps into the spirit, not just "
                       "the body. ★ CURSED — cannot be removed without Remove Curse.",
    },
]

# Tier-bucketed for loot system
CURSED_ITEMS_T1 = [i for i in CURSED_ITEMS if i["tier"] == 1]
CURSED_ITEMS_T2 = [i for i in CURSED_ITEMS if i["tier"] == 2]
CURSED_ITEMS_T3 = [i for i in CURSED_ITEMS if i["tier"] == 3]


def get_cursed_item(floor_num, total_floors, rng):
    """Return a cursed item appropriate to dungeon depth, or None.
    Called with ~8% chance from the loot generator on chest/secret finds."""
    depth_ratio = floor_num / max(total_floors, 1)
    if depth_ratio >= 0.8 and CURSED_ITEMS_T3:
        pool = CURSED_ITEMS_T3
    elif depth_ratio >= 0.4 and CURSED_ITEMS_T2:
        pool = CURSED_ITEMS_T2
    else:
        pool = CURSED_ITEMS_T1
    item = dict(rng.choice(pool))
    # Copy stat_penalty into the item's stat_bonus so combat engine picks it up
    # Penalties are negative values in stat_bonus
    bonuses = dict(item.get("stat_bonus", {}))
    for stat, penalty in item.get("stat_penalty", {}).items():
        bonuses[stat] = bonuses.get(stat, 0) + penalty
    item["stat_bonus"] = bonuses
    return item


# ═══════════════════════════════════════════════════════════════
#  UNIQUE ITEMS
#  One-of-a-kind drops. "unique": True means only one can exist
#  in the world at once — if already in party inventory or
#  equipped, it won't drop again. Guaranteed boss drops are
#  flagged "unique_boss_drop": True.
# ═══════════════════════════════════════════════════════════════

UNIQUE_ITEMS = {

    # ── Korrath (Warden Revenant boss) ──────────────────────
    "korrath_blade": {
        "name": "Korrath's Last Oath",
        "type": "weapon", "subtype": "Greatsword", "slot": "weapon",
        "rarity": "legendary", "unique": True,
        "damage": 30, "phys_type": "slashing", "range": "melee",
        "damage_stat": {"STR": 0.7, "DEX": 0.3},
        "enchant_element": "shadow", "enchant_bonus": 6, "enchant_name": "Shadow",
        "stat_bonuses": {"STR": 2},
        "set_id": "warden_set",
        "identified": False, "estimated_value": 350,
        "description": (
            "Korrath's own blade, still warm with the last oaths he swore "
            "before the Fading took him. The shadow enchantment is not evil — "
            "it is grief, solidified. +2 STR, shadow damage."
        ),
        "lore": (
            "Korrath was the last loyal Warden Commander. When Valdris ordered "
            "him to seal the miners inside the abandoned shafts to hide evidence "
            "of the Hearthstone extraction, Korrath refused — and Valdris had him "
            "killed. The Fading resurrected him as a revenant bound to guard the "
            "very mine he died protecting. He cannot rest."
        ),
    },

    "korrath_ring": {
        "name": "Warden's Oath Ring",
        "type": "accessory", "subtype": "ring", "slot": "accessory1",
        "rarity": "rare", "unique": True,
        "stat_bonuses": {"STR": 2, "CON": 2},
        "magic_resist": 4,
        "set_id": "warden_set",
        "identified": False, "estimated_value": 220,
        "description": (
            "The signet ring of the Warden order, passed down through commanders. "
            "Korrath wore it to his death. +2 STR, +2 CON, +4 magic resist."
        ),
        "lore": (
            "The ring bears the Warden crest — a torch over crossed blades — "
            "though the crest is worn nearly smooth. Dozens of Wardens have "
            "worn this ring. Most died in service. None were murdered by their own."
        ),
    },

    # ── Ashvar (Ruins of Ashenmoor boss) ─────────────────────
    "ashvar_robes": {
        "name": "Ashvar's Travelling Robes",
        "type": "armor", "subtype": "chest", "slot": "body",
        "rarity": "legendary", "unique": True,
        "defense": 6, "magic_resist": 14,
        "stat_bonuses": {"INT": 3, "WIS": 2},
        "set_id": "ashenmoor_set",
        "identified": False, "estimated_value": 380,
        "description": (
            "Ashvar wore these robes for thirty years of wandering before "
            "Valdris's agents caught him. Stitched with minor wards that have "
            "grown strong with age. +3 INT, +2 WIS, high magic resist."
        ),
        "lore": (
            "Ashvar survived the fall of the first Warden order and spent "
            "decades trying to warn city after city about Valdris. Nobody "
            "listened. The robes are patched in seventeen places — each patch "
            "marks a close call."
        ),
    },

    "ashvar_focus": {
        "name": "The Shattered Focus",
        "type": "accessory", "subtype": "amulet", "slot": "accessory2",
        "rarity": "legendary", "unique": True,
        "stat_bonuses": {"INT": 4, "WIS": 1},
        "magic_resist": 6,
        "enchant_element": "divine", "enchant_bonus": 5, "enchant_name": "Holy",
        "set_id": "ashenmoor_set",
        "identified": False, "estimated_value": 420,
        "description": (
            "Ashvar's spellcasting focus, cracked down the middle when Valdris "
            "overwhelmed him. Somehow the crack makes it resonate at two "
            "frequencies simultaneously. +4 INT, +1 WIS, holy damage bonus."
        ),
        "lore": (
            "The crack runs through a small rune of warding. Ashvar once said "
            "that broken things sometimes become more than they were — the "
            "crack lets light in from both sides at once."
        ),
    },

    # ── Secret room find — no specific boss ──────────────────
    "shadowwalker_boots": {
        "name": "Shadowwalker's Boots",
        "type": "armor", "subtype": "boots", "slot": "feet",
        "rarity": "legendary", "unique": True,
        "defense": 4, "speed_mod": 5,
        "stat_bonuses": {"DEX": 3},
        "enchant_resist": "shadow", "enchant_resist_bonus": 10,
        "identified": False, "estimated_value": 300,
        "description": (
            "Boots worn by a Fading-Touched scout who could run between shadows. "
            "The soles are made from shadow-silk — they make no sound at all. "
            "+3 DEX, +5 speed, shadow resist."
        ),
        "lore": (
            "Found on a skeleton in a sealed room. The scout apparently crawled "
            "in through a crack too small to escape through. The door had "
            "been locked from the outside."
        ),
    },

    "hearthwarden_helm": {
        "name": "Hearthwarden Helm",
        "type": "armor", "subtype": "helmet", "slot": "head",
        "rarity": "legendary", "unique": True,
        "defense": 10, "magic_resist": 8,
        "stat_bonuses": {"CON": 3, "WIS": 1},
        "set_id": "warden_set",
        "identified": False, "estimated_value": 340,
        "description": (
            "The ceremonial helm of the Warden order's High Commander. Last worn "
            "the night Valdris gave his first order. +3 CON, +1 WIS, solid "
            "defense and magic resist."
        ),
        "lore": (
            "The High Commander who wore this helm vanished the same night "
            "Korrath was killed. No body was ever found. The helm was "
            "discovered in a sealed vault beneath the ruins, still clean."
        ),
    },

    # ── Act 3 Quest Rewards ────────────────────────────────────────────
    "sirenne_buckler": {
        "name": "Sentinel's Vow",
        "type": "armor",
        "subtype": "shield",
        "slot": "offhand",
        "rarity": "legendary",
        "unique": True,
        "defense": 12,
        "magic_resist": 10,
        "stat_bonuses": {"CON": 2, "WIS": 2},
        "identified": False,
        "estimated_value": 360,
        "description": (
            "Warden Sirenne's buckler. She carried it for decades of exile — "
            "armored always, facing always inward, toward what she protected. "
            "+2 CON, +2 WIS, strong defense and magic resist."
        ),
        "lore": (
            "The buckler is old enough that the Warden crest has worn away, but "
            "the inner face is still polished bright. Sirenne looked at her own "
            "reflection every morning. She said it reminded her what she was "
            "guarding against."
        ),
    },

    "keeper_pendant": {
        "name": "The Nameless Keeper's Seal",
        "type": "accessory",
        "subtype": "amulet",
        "slot": "accessory2",
        "rarity": "legendary",
        "unique": True,
        "stat_bonuses": {"INT": 3, "WIS": 3},
        "magic_resist": 8,
        "enchant_element": "wind",
        "enchant_bonus": 5,
        "enchant_name": "Gale",
        "identified": False,
        "estimated_value": 400,
        "description": (
            "Left on the pedestal when the elemental dispersed. No inscription. "
            "The Will chose to be remembered only for its purpose — but it left "
            "this behind anyway. +3 INT, +3 WIS, wind damage bonus, magic resist."
        ),
        "lore": (
            "The survey record says the keeper requested its name not be recorded. "
            "It left no name on this seal either. But it left the seal. "
            "Perhaps that was the name."
        ),
    },

    "warden_seal": {
        "name": "The Last Warden's Seal",
        "type": "accessory",
        "subtype": "ring",
        "slot": "accessory1",
        "rarity": "legendary",
        "unique": True,
        "stat_bonuses": {"STR": 2, "INT": 2, "WIS": 2},
        "magic_resist": 12,
        "enchant_element": "divine",
        "enchant_bonus": 6,
        "enchant_name": "Ward",
        "identified": False,
        "estimated_value": 500,
        "description": (
            "Recovered from the rift after Valdris's dissolution. "
            "The seal of the Warden High Commander — the one who never came back. "
            "+2 STR, +2 INT, +2 WIS, high magic resist, ward damage bonus."
        ),
        "lore": (
            "The ring was found in the exact center of the rift, resting on "
            "nothing. The Warden order is gone. The wards are new. "
            "Someone has to hold what they protected."
        ),
    },

    # ── Karreth (peaceful resolution — Dragon's Tooth) ────────
    "karreth_scale": {
        "name": "Karreth's Willgift",
        "type": "armor",
        "subtype": "chest",
        "slot": "body",
        "rarity": "legendary",
        "unique": True,
        "defense": 16,
        "magic_resist": 10,
        "stat_bonuses": {"CON": 2, "STR": 2},
        "enchant_element": "fire",
        "enchant_bonus": 5,
        "enchant_name": "Dragonfire",
        "enchant_resist": "fire",
        "enchant_resist_bonus": 20,
        "identified": False,
        "estimated_value": 480,
        "description": (
            "A scale shed willingly by Karreth-sol-Amendar, worked into chest armor. "
            "Still warm. Always warm. +2 CON, +2 STR, fire damage, 20% fire resist."
        ),
        "lore": (
            "The scale was given freely — which matters in old draconic tradition. "
            "A willing gift from a guardian carries a fraction of the guardian's purpose. "
            "Wearing it, you feel a faint, constant warmth at your sternum. "
            "Not heat. Remembrance."
        ),
    },
}


# ── Item Sets ─────────────────────────────────────────────────
# Bonuses applied when wearing N pieces of the same set.
# Keys are set_id values used in item dicts above.

ITEM_SETS = {
    "warden_set": {
        "name": "Warden's Oath",
        "pieces": ["Korrath's Last Oath", "Warden's Oath Ring", "Hearthwarden Helm"],
        "bonuses": {
            2: {
                "label": "2pc: Warden's Resolve",
                "stat_bonuses": {"STR": 2, "CON": 2},
                "description": "+2 STR, +2 CON. The Warden's training returns to muscle memory.",
            },
            3: {
                "label": "3pc: Oath Unbroken",
                "stat_bonuses": {"STR": 3, "CON": 3},
                "magic_resist": 8,
                "damage_bonus": 5,
                "description": "+3 STR, +3 CON, +8 MRES, +5 physical damage. Korrath's oath strengthens the bearer.",
            },
        },
    },

    "ashenmoor_set": {
        "name": "Ashvar's Legacy",
        "pieces": ["Ashvar's Travelling Robes", "The Shattered Focus"],
        "bonuses": {
            2: {
                "label": "2pc: Wanderer's Wisdom",
                "stat_bonuses": {"INT": 3, "WIS": 2},
                "magic_resist": 10,
                "description": "+3 INT, +2 WIS, +10 MRES. Decades of wandering encoded in the set.",
            },
        },
    },
}


def get_set_bonus(character):
    """Calculate active item set bonuses for a character.
    Returns dict: { set_id: (set_data, pieces_equipped, active_bonus_tier) }
    """
    if not hasattr(character, "equipment") or not character.equipment:
        return {}

    # Count set pieces equipped
    set_counts = {}
    for slot, item in character.equipment.items():
        if item and item.get("set_id"):
            sid = item["set_id"]
            set_counts[sid] = set_counts.get(sid, 0) + 1

    result = {}
    for sid, count in set_counts.items():
        if sid not in ITEM_SETS:
            continue
        set_data = ITEM_SETS[sid]
        # Find highest bonus tier active
        active_tier = max(
            (tier for tier in set_data["bonuses"] if tier <= count),
            default=0
        )
        if active_tier > 0:
            result[sid] = (set_data, count, active_tier)

    return result


def calc_set_stat_bonuses(character):
    """Return combined stat bonuses from all active item sets."""
    bonuses = {}
    for sid, (set_data, count, tier) in get_set_bonus(character).items():
        for stat, val in set_data["bonuses"][tier].get("stat_bonuses", {}).items():
            bonuses[stat] = bonuses.get(stat, 0) + val
    return bonuses


def party_has_unique(party, item_name):
    """Check if party already has a named unique item (equipped or in inventory)."""
    for char in party:
        for inv_item in char.inventory:
            if inv_item.get("name") == item_name and inv_item.get("unique"):
                return True
        for slot, eq in (char.equipment or {}).items():
            if eq and eq.get("name") == item_name and eq.get("unique"):
                return True
    return False


def get_unique_item(key, party=None):
    """Return a copy of a unique item, or None if party already has it."""
    item = UNIQUE_ITEMS.get(key)
    if item is None:
        return None
    if party and party_has_unique(party, item["name"]):
        return None
    return dict(item)


# ══════════════════════════════════════════════════════════════
#  RELIGIOUS ITEMS (Relics)
#  Identified with Divine Lore (PIE >= 10). Trained Cleric/Paladin
#  classes get a bonus to the check. Any character with sufficient
#  PIE can *use* a relic for its passive bonus, but its effects
#  are enhanced when equipped by a PIE-primary class.
# ══════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════
#  PANACEA — Cures both poison AND disease. Rare consumable.
# ══════════════════════════════════════════════════════════════

PANACEA = {
    "name": "Panacea",
    "type": "consumable",
    "rarity": "rare",
    "cures": ["Poison", "Disease"],
    "description": (
        "A golden vial of ancient alchemical remedy. Clears all poison "
        "and disease from the user. Brewed only by masters of the craft."
    ),
    "buy_price": 180,
    "sell_price": 45,
    "identified": True,
    "stack": 1,
    "lore": "Healers say true Panacea requires ingredients from three different biomes.",
}

RELIGIOUS_ITEMS = [
    # ── Tier 1 Relics ─────────────────────────────────────────
    {
        "name": "Warden's Talisman",
        "unidentified_name": "Worn Talisman",
        "unidentified_desc": "A talisman bearing a faint mark. The stone is warm to the touch.",
        "appraised_name": "Talisman of Warden Craft",
        "material_desc": "Carved from hearthstone. Old Warden workmanship.",
        "magic_desc": "Hums with protective resonance. Divine in nature.",
        "type": "accessory", "slot": "accessory1", "subtype": "relic",
        "rarity": "uncommon",
        "effect": {"pie_bonus": 2, "wis_bonus": 1},
        "stat_bonus": {"PIE": 2, "WIS": 1},
        "description": "A Warden-carved talisman. +2 PIE, +1 WIS. Heals +8% from divine sources.",
        "healing_received_bonus": 0.08,  # extra healing when equipped
        "identify_difficulty": 1,
        "identified": False, "estimated_value": 80,
        "lore": "Made by the first Wardens before the Fading began.",
    },
    {
        "name": "Pale Candle Amulet",
        "unidentified_name": "Wax Amulet",
        "unidentified_desc": "A tiny candle molded in wax, threaded on a cord. Never melts.",
        "appraised_name": "Amulet of the Pale Order",
        "material_desc": "Hardened ceremonial wax, Pale Coast origin.",
        "magic_desc": "Resists fear effects. Faint divine warmth.",
        "type": "accessory", "slot": "accessory1", "subtype": "relic",
        "rarity": "uncommon",
        "effect": {"pie_bonus": 1},
        "stat_bonus": {"PIE": 1},
        "description": "A Pale Order ward-token. +1 PIE. Fear resistance +15%.",
        "fear_resist_bonus": 0.15,
        "identify_difficulty": 1,
        "identified": False, "estimated_value": 70,
        "lore": "Issued to villagers in Pale Coast fishing towns as wards against sea-spirits.",
    },

    # ── Tier 2 Relics ─────────────────────────────────────────
    {
        "name": "Icon of the Hearthkeepers",
        "unidentified_name": "Stone Icon",
        "unidentified_desc": "A smooth stone carved into a vaguely humanoid shape. Five notches on its base.",
        "appraised_name": "Hearthkeeper Icon",
        "material_desc": "Carved hearthstone. Pre-Fading craftsmanship.",
        "magic_desc": "Radiates warmth. Strong divine resonance across all five Hearthstone sites.",
        "type": "accessory", "slot": "accessory2", "subtype": "relic",
        "rarity": "rare",
        "effect": {"pie_bonus": 3, "wis_bonus": 2},
        "stat_bonus": {"PIE": 3, "WIS": 2},
        "description": "A pre-Fading Warden artifact. +3 PIE, +2 WIS. Heals +12% from any source.",
        "healing_received_bonus": 0.12,
        "fear_resist_bonus": 0.20,
        "identify_difficulty": 2,
        "identified": False, "estimated_value": 200,
        "lore": "These icons were distributed to each of the five Hearthstone sites. "
                "Four are lost. This one survived.",
    },
    {
        "name": "Inquisitor's Brand",
        "unidentified_name": "Branded Medallion",
        "unidentified_desc": "A heavy medallion branded with an unfamiliar mark. Warm metal.",
        "appraised_name": "Brand of the Old Inquisition",
        "material_desc": "Hammered iron and silver. Formal religious workmanship.",
        "magic_desc": "Detects undead and shadow-touched within 30 paces. Divine sight.",
        "type": "accessory", "slot": "accessory1", "subtype": "relic",
        "rarity": "rare",
        "effect": {"pie_bonus": 2, "wis_bonus": 1},
        "stat_bonus": {"PIE": 2, "WIS": 1},
        "description": "Old Inquisition writ of authority. +2 PIE, +1 WIS. Sense undead passively.",
        "passive_ability": "detect_undead",
        "identify_difficulty": 2,
        "identified": False, "estimated_value": 180,
        "lore": "The Inquisition predates the Warden Order. Most of their relics were melted down.",
    },

    # ── Tier 3 Relics ─────────────────────────────────────────
    {
        "name": "The Shepherd's Crook",
        "damage_stat": {"PIE": 0.6, "WIS": 0.4},
        "unidentified_name": "Carved Staff Fragment",
        "unidentified_desc": "A carved wooden fragment from a larger piece. The grain shimmers slightly.",
        "appraised_name": "Fragment of the Shepherd's Crook",
        "material_desc": "Livingwood, first-growth. Extremely old.",
        "magic_desc": "Resonates with divine and natural energies both. A rare convergence.",
        "type": "weapon", "slot": "weapon", "subtype": "Staff",
        "rarity": "epic",
        "damage": 8, "phys_type": "blunt", "range": "melee",
        "spell_bonus": 6,
        "effect": {"pie_bonus": 4, "wis_bonus": 3},
        "stat_bonus": {"PIE": 4, "WIS": 3},
        "description": "A Warden shepherd's weapon, fragment restored. +4 PIE, +3 WIS, +6 Spell Power.",
        "healing_received_bonus": 0.15,
        "fear_resist_bonus": 0.30,
        "identify_difficulty": 3,
        "identified": False, "estimated_value": 450,
        "lore": "The Shepherd of the Old Wardens was a rank above Warden-Commander. "
                "There has not been one since before the Fading.",
    },
]


# ══════════════════════════════════════════════════════════════
#  TRAINING BOOKS
#  Rare loot found in deep dungeons and on boss drops.
#  Using a training book permanently raises one stat by 1.
#  Each book is consumed on use. A character may only benefit
#  from a given book once (second use has no effect).
#
#  Identified with INT (Arcane Lore) or found already legible.
#  No class restriction on use — anyone can read them.
#  Narrative: these are survivor texts from the pre-Fading world,
#  each encoding a philosophy of personal development.
# ══════════════════════════════════════════════════════════════

TRAINING_BOOKS = [
    {
        "name": "Way of Light",
        "unidentified_name": "Tattered Devotional",
        "unidentified_desc": "A worn book with pages of closely-written prayers. The ink never fades.",
        "appraised_name": "Way of Light — Devotional Manual",
        "material_desc": "Pale vellum, Pale Order origin. Preserved by divine ward.",
        "magic_desc": "Reading it leaves a warmth in the chest. Spiritual resonance.",
        "type": "consumable", "subtype": "training_book",
        "rarity": "rare",
        "trains_stat": "PIE", "trains_amount": 1,
        "description": "A pre-Fading devotional on faith and presence. Permanently +1 PIE.",
        "identify_difficulty": 2,
        "identified": False, "estimated_value": 300,
        "use_message": "The words settle into you — a conviction you didn't have before.",
        "lore": "Compiled by the Pale Order before the first Hearthstone flickered.",
    },
    {
        "name": "Way of the Quiet Mind",
        "unidentified_name": "Small Philosophy Text",
        "unidentified_desc": "A slim volume, densely written in a careful hand. No title on the cover.",
        "appraised_name": "Way of the Quiet Mind — Sage's Meditations",
        "material_desc": "Quality paper, tower-scholar binding. Pre-Fading academic press.",
        "magic_desc": "Reading it sharpens focus. Mental resonance.",
        "type": "consumable", "subtype": "training_book",
        "rarity": "rare",
        "trains_stat": "INT", "trains_amount": 1,
        "description": "Scholar meditations on observation and reason. Permanently +1 INT.",
        "identify_difficulty": 2,
        "identified": False, "estimated_value": 300,
        "use_message": "A pattern you'd never seen before suddenly seems obvious.",
        "lore": "Attributed to a tower scholar who survived the first year of the Fading by pure analysis.",
    },
    {
        "name": "Way of the Still Water",
        "unidentified_name": "Worn Meditation Guide",
        "unidentified_desc": "A guide with hand-drawn diagrams of posture and breathing. Some pages water-stained.",
        "appraised_name": "Way of the Still Water — Ki Foundation",
        "material_desc": "Monastery paper, monk binding. Very old.",
        "magic_desc": "A meditative resonance. Natural and spiritual both.",
        "type": "consumable", "subtype": "training_book",
        "rarity": "rare",
        "trains_stat": "WIS", "trains_amount": 1,
        "description": "Monastery meditation techniques for natural perception. Permanently +1 WIS.",
        "identify_difficulty": 2,
        "identified": False, "estimated_value": 300,
        "use_message": "You sit with it for an hour. Something in the world feels quieter now.",
        "lore": "A foundation text of the Order of the Still River, now disbanded.",
    },
    {
        "name": "Way of the Living Body",
        "unidentified_name": "Field Surgeon's Manual",
        "unidentified_desc": "A medical manual with anatomical diagrams. Practical, thorough.",
        "appraised_name": "Way of the Living Body — Endurance Manual",
        "material_desc": "Heavy paper, field-bound. Military origin.",
        "magic_desc": "Subtle physical resonance — reads like it was written to be used, not studied.",
        "type": "consumable", "subtype": "training_book",
        "rarity": "rare",
        "trains_stat": "CON", "trains_amount": 1,
        "description": "Practical endurance and recovery techniques. Permanently +1 CON.",
        "identify_difficulty": 2,
        "identified": False, "estimated_value": 300,
        "use_message": "You work through the exercises. Your body remembers something it didn't before.",
        "lore": "Standard issue in the old Imperial Army. Most copies were burned after the Fading.",
    },
    {
        "name": "Way of the Striking Hand",
        "unidentified_name": "Combat Theory Manual",
        "unidentified_desc": "A training manual with detailed strike diagrams. The pages are well-worn.",
        "appraised_name": "Way of the Striking Hand — Combat Foundation",
        "material_desc": "Durable pressed paper, Guild binding. Fighter's Guild origin.",
        "magic_desc": "Physical resonance — the technique is almost encoded in the paper.",
        "type": "consumable", "subtype": "training_book",
        "rarity": "rare",
        "trains_stat": "STR", "trains_amount": 1,
        "description": "Core physical power development from the old Fighter's Guild. Permanently +1 STR.",
        "identify_difficulty": 2,
        "identified": False, "estimated_value": 300,
        "use_message": "The drills in the last chapter are brutal. You feel different afterward.",
        "lore": "Fighter's Guild training manual, last edition before the Guild dissolved.",
    },
    {
        "name": "Way of the Open Hand",
        "unidentified_name": "Thief's Craft Manual",
        "unidentified_desc": "A slim manual written in a compact cipher. Clever layout — easy to conceal.",
        "appraised_name": "Way of the Open Hand — Precision Manual",
        "material_desc": "Thin paper, hand-copied. Thieves' Guild tradition.",
        "magic_desc": "Precision resonance. Almost seems to move in your hands.",
        "type": "consumable", "subtype": "training_book",
        "rarity": "rare",
        "trains_stat": "DEX", "trains_amount": 1,
        "description": "Precision and reflex techniques from the old Thieves' Guild. Permanently +1 DEX.",
        "identify_difficulty": 2,
        "identified": False, "estimated_value": 300,
        "use_message": "Your fingers work through the drills without thinking. That's the point.",
        "lore": "The cipher was broken long ago. The techniques were never meant to be secret.",
    },
]


def get_random_training_book():
    """Return a copy of a random training book for loot drops."""
    import random as _random
    return dict(_random.choice(TRAINING_BOOKS))


def get_random_relic(max_tier=2):
    """Return a copy of a random religious item, filtered by tier."""
    import random as _random
    # difficulty 1 = tier 1, 2 = tier 2, 3 = tier 3
    pool = [r for r in RELIGIOUS_ITEMS
            if r.get("identify_difficulty", 1) <= max_tier]
    if not pool:
        return dict(RELIGIOUS_ITEMS[0])
    return dict(_random.choice(pool))
