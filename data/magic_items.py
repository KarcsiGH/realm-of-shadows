"""
Realm of Shadows — Magic Items
Unique items found in secret rooms and dropped by bosses.
Organized by tier (1=early, 2=mid, 3=late).
"""

# ══════════════════════════════════════════════════════════
#  SECRET ROOM ITEMS — Found in hidden chests
# ══════════════════════════════════════════════════════════

SECRET_ITEMS_T1 = [
    {"name": "Ring of Minor Fortitude", "type": "accessory", "slot": "accessory1",
     "subtype": "ring", "rarity": "uncommon",
     "effect": {"con_bonus": 2, "max_hp_bonus": 10},
     "description": "A plain iron ring that makes the wearer feel hardier. +2 CON, +10 max HP.",
     "identified": True, "estimated_value": 60},

    {"name": "Boots of Quiet Steps", "type": "armor", "slot": "feet",
     "subtype": "boots", "rarity": "uncommon",
     "defense": 1, "speed_bonus": 2,
     "effect": {"dex_bonus": 1},
     "description": "Soft leather boots. +1 DEX, +2 speed. Helps avoid encounters.",
     "identified": True, "estimated_value": 55},

    {"name": "Cloak of Shadows", "type": "armor", "slot": "body",
     "subtype": "cloak", "rarity": "uncommon", "armor_tier": "clothing",
     "defense": 2, "magic_resist": 3,
     "effect": {"dex_bonus": 1},
     "description": "A dark cloak that seems to drink in light. +1 DEX, +3 magic resist.",
     "identified": True, "estimated_value": 70},

    {"name": "Wand of Sparks", "type": "weapon", "slot": "weapon",
     "subtype": "Wand", "rarity": "uncommon", "damage": 4,
     "phys_type": "blunt", "range": "melee",
     "spell_bonus": 3,
     "enchant_element": "lightning", "enchant_bonus": 3,
     "description": "A wand crackling with static. +3 spell power, deals lightning damage.",
     "identified": True, "estimated_value": 65},

    {"name": "Amulet of the Owl", "type": "accessory", "slot": "accessory1",
     "subtype": "amulet", "rarity": "uncommon",
     "effect": {"wis_bonus": 2, "int_bonus": 1},
     "description": "A silver owl pendant. +2 WIS, +1 INT.",
     "identified": True, "estimated_value": 55},
]

SECRET_ITEMS_T2 = [
    {"name": "Firebrand Blade", "type": "weapon", "slot": "weapon",
     "subtype": "Longsword", "rarity": "rare", "damage": 14,
     "phys_type": "slashing", "range": "melee",
     "enchant_element": "fire", "enchant_bonus": 5, "enchant_name": "Flame",
     "description": "A longsword wreathed in faint flames. Deals bonus fire damage.",
     "identified": True, "estimated_value": 160},

    {"name": "Frostbite Dagger", "type": "weapon", "slot": "weapon",
     "subtype": "Dagger", "rarity": "rare", "damage": 10,
     "phys_type": "piercing", "range": "melee",
     "enchant_element": "ice", "enchant_bonus": 5, "enchant_name": "Frost",
     "effect": {"dex_bonus": 2},
     "description": "An ice-cold dagger. +2 DEX, bonus ice damage.",
     "identified": True, "estimated_value": 150},

    {"name": "Ring of the Battlemage", "type": "accessory", "slot": "accessory1",
     "subtype": "ring", "rarity": "rare",
     "effect": {"int_bonus": 3, "str_bonus": 1},
     "description": "Worn by warrior-mages of the old Wardens. +3 INT, +1 STR.",
     "identified": True, "estimated_value": 140},

    {"name": "Shield of the Sentinel", "type": "armor", "slot": "off_hand",
     "subtype": "shield", "rarity": "rare",
     "defense": 6, "magic_resist": 4,
     "effect": {"con_bonus": 1},
     "description": "An ancient shield that still hums with protective magic. +1 CON.",
     "identified": True, "estimated_value": 180},

    {"name": "Orb of Fading Sight", "type": "accessory", "slot": "accessory1",
     "subtype": "orb", "rarity": "rare",
     "effect": {"int_bonus": 3, "wis_bonus": 2},
     "spell_bonus": 4,
     "description": "A dark crystal orb. Glimpses of the Fading swirl within. +3 INT, +2 WIS, +4 spell.",
     "identified": True, "estimated_value": 200},

    {"name": "Boots of the Wind", "type": "armor", "slot": "feet",
     "subtype": "boots", "rarity": "rare",
     "defense": 2, "speed_bonus": 4,
     "effect": {"dex_bonus": 2},
     "description": "Enchanted boots that make the wearer swift as wind. +2 DEX, +4 speed.",
     "identified": True, "estimated_value": 170},

    {"name": "Crown of Clarity", "type": "armor", "slot": "head",
     "subtype": "circlet", "rarity": "rare",
     "defense": 2, "magic_resist": 6,
     "effect": {"wis_bonus": 3},
     "description": "A silver circlet that clears the mind. +3 WIS, +6 magic resist.",
     "identified": True, "estimated_value": 190},

    {"name": "Gauntlets of Might", "type": "armor", "slot": "hands",
     "subtype": "gauntlets", "rarity": "rare",
     "defense": 3,
     "effect": {"str_bonus": 3},
     "description": "Heavy gauntlets that make your blows land harder. +3 STR.",
     "identified": True, "estimated_value": 160},
]

SECRET_ITEMS_T3 = [
    {"name": "Warden's Oath", "type": "weapon", "slot": "weapon",
     "subtype": "Longsword", "rarity": "epic", "damage": 18,
     "phys_type": "slashing", "range": "melee",
     "enchant_element": "divine", "enchant_bonus": 6, "enchant_name": "Holy",
     "effect": {"str_bonus": 2, "pie_bonus": 2},
     "description": "A holy blade of the old Wardens. +2 STR, +2 PIE, divine damage.",
     "identified": True, "estimated_value": 350},

    {"name": "Staff of the Fading", "type": "weapon", "slot": "weapon",
     "subtype": "Staff", "rarity": "epic", "damage": 8,
     "phys_type": "blunt", "range": "melee",
     "spell_bonus": 8,
     "enchant_element": "shadow", "enchant_bonus": 6, "enchant_name": "Shadow",
     "effect": {"int_bonus": 4},
     "description": "A twisted staff that channels the Fading itself. +4 INT, +8 spell, shadow damage.",
     "identified": True, "estimated_value": 400},

    {"name": "Aegis of Dawn", "type": "armor", "slot": "off_hand",
     "subtype": "shield", "rarity": "epic",
     "defense": 8, "magic_resist": 8,
     "effect": {"con_bonus": 2, "pie_bonus": 2},
     "enchant_resist": "shadow", "enchant_resist_bonus": 5,
     "description": "A radiant shield that repels darkness. +2 CON, +2 PIE, shadow resist.",
     "identified": True, "estimated_value": 450},
]


# ══════════════════════════════════════════════════════════
#  BOSS LOOT — Guaranteed unique drops per boss
# ══════════════════════════════════════════════════════════

BOSS_BONUS_LOOT = {
    "Goblin King": [
        {"drop_chance": 0.40, "item": {
            "name": "Grak's Lucky Coin", "type": "accessory", "slot": "accessory1",
            "subtype": "trinket", "rarity": "uncommon",
            "effect": {"dex_bonus": 1},
            "description": "A strange coin Grak carried. Brings luck to the bearer. +1 DEX.",
            "identified": True, "estimated_value": 45}},
    ],
    "Giant Spider Queen": [
        {"drop_chance": 0.50, "item": {
            "name": "Venomstrike Fang", "type": "weapon", "slot": "weapon",
            "subtype": "Dagger", "rarity": "rare", "damage": 11,
            "phys_type": "piercing", "range": "melee",
            "enchant_element": "nature", "enchant_bonus": 4, "enchant_name": "Venom",
            "effect": {"dex_bonus": 2},
            "description": "A dagger carved from the Spider Queen's fang. +2 DEX, poison damage.",
            "identified": True, "estimated_value": 140}},
    ],
    "Undead Foreman": [
        {"drop_chance": 0.50, "item": {
            "name": "Foreman's Hard Hat", "type": "armor", "slot": "head",
            "subtype": "helmet", "rarity": "rare",
            "defense": 6, "magic_resist": 2,
            "effect": {"con_bonus": 2},
            "description": "A battered miner's helm, enchanted by the Fading. +2 CON.",
            "identified": True, "estimated_value": 120}},
    ],
    "Warden Revenant": [
        {"drop_chance": 0.80, "item": {
            "name": "Revenant's Greatsword", "type": "weapon", "slot": "weapon",
            "subtype": "Greatsword", "rarity": "rare", "damage": 18,
            "phys_type": "slashing", "range": "melee",
            "enchant_element": "shadow", "enchant_bonus": 4, "enchant_name": "Shadow",
            "description": "The corrupted Warden's blade. Shadow-infused.",
            "identified": True, "estimated_value": 220}},
        {"drop_chance": 0.40, "item": {
            "name": "Warden's Signet Ring", "type": "accessory", "slot": "accessory1",
            "subtype": "ring", "rarity": "rare",
            "effect": {"str_bonus": 2, "con_bonus": 2},
            "description": "The signet of a fallen Warden. +2 STR, +2 CON.",
            "identified": True, "estimated_value": 180}},
    ],
    "Shadow Valdris": [
        {"drop_chance": 0.80, "item": {
            "name": "Valdris' Shadowstaff", "type": "weapon", "slot": "weapon",
            "subtype": "Staff", "rarity": "epic", "damage": 8,
            "phys_type": "blunt", "range": "melee",
            "spell_bonus": 7,
            "enchant_element": "shadow", "enchant_bonus": 6, "enchant_name": "Shadow",
            "effect": {"int_bonus": 3},
            "description": "The shadow-echo of Valdris' staff. Crackling with dark power. +3 INT, +7 spell.",
            "identified": True, "estimated_value": 350}},
        {"drop_chance": 0.50, "item": {
            "name": "Fading Shard Amulet", "type": "accessory", "slot": "accessory1",
            "subtype": "amulet", "rarity": "epic",
            "effect": {"int_bonus": 3, "wis_bonus": 2, "pie_bonus": 1},
            "magic_resist": 5,
            "description": "A crystallized fragment of the Fading. Whispers with dark knowledge. +3 INT, +2 WIS, +1 PIE.",
            "identified": True, "estimated_value": 400}},
    ],
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
