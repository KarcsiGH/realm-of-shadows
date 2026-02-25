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
     "subtype": "Longsword", "rarity": "rare", "damage": 14,
     "phys_type": "slashing", "range": "melee",
     "enchant_element": "fire", "enchant_bonus": 5, "enchant_name": "Flame",
     "description": "A longsword wreathed in faint flames. Deals bonus fire damage.",
     "identified": False, "estimated_value": 160},

    {"name": "Frostbite Dagger", "appraised_name": "Frostbite Dagger", "type": "weapon", "slot": "weapon",
     "subtype": "Dagger", "rarity": "rare", "damage": 10,
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
     "phys_type": "slashing", "range": "melee",
     "enchant_element": "divine", "enchant_bonus": 6, "enchant_name": "Holy",
     "effect": {"str_bonus": 2, "pie_bonus": 2},
     "description": "A holy blade of the old Wardens. +2 STR, +2 PIE, divine damage.",
     "identified": False, "estimated_value": 350},

    {"name": "Staff of the Fading", "appraised_name": "Staff of the Fading", "type": "weapon", "slot": "weapon",
     "subtype": "Staff", "rarity": "epic", "damage": 8,
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
        {"drop_chance": 0.80, "item": {
            "name": "Revenant's Greatsword", "appraised_name": "Revenant's Greatsword", "type": "weapon", "slot": "weapon",
            "subtype": "Greatsword", "rarity": "rare", "damage": 18,
            "phys_type": "slashing", "range": "melee",
            "enchant_element": "shadow", "enchant_bonus": 4, "enchant_name": "Shadow",
            "description": "The corrupted Warden's blade. Shadow-infused.",
            "identified": False, "estimated_value": 220}},
        {"drop_chance": 0.40, "item": {
            "name": "Warden's Signet Ring", "appraised_name": "Warden's Signet Ring", "type": "accessory", "slot": "accessory1",
            "subtype": "ring", "rarity": "rare",
            "effect": {"str_bonus": 2, "con_bonus": 2},
            "description": "The signet of a fallen Warden. +2 STR, +2 CON.",
            "identified": False, "estimated_value": 180}},
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
    # NOTE: Lingering Will boss loot is defined in tower_data.py
}


def get_secret_item(floor_num, total_floors, rng):
    """Pick a random magic item appropriate to dungeon depth."""
    depth_ratio = floor_num / max(total_floors, 1)
    if depth_ratio >= 0.8 and rng.random() < 0.3:
        pool = SECRET_ITEMS_T3
    elif depth_ratio >= 0.4 or floor_num >= 2:
        pool = SECRET_ITEMS_T2
    else:
        pool = SECRET_ITEMS_T1
    return dict(rng.choice(pool))


def get_boss_bonus_drops(boss_name, rng):
    """Get bonus loot from a boss. Returns list of items that dropped."""
    bonus_table = BOSS_BONUS_LOOT.get(boss_name, [])
    drops = []
    for entry in bonus_table:
        if rng.random() < entry["drop_chance"]:
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
