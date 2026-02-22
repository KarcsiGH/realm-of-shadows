"""
Realm of Shadows — Shop Inventory Data
Items available for purchase at shops, organized by tier/location.
"""

from core.equipment import ARMOR

# ═══════════════════════════════════════════════════════════════
#  GENERAL STORE — Weapons, Armor, Basic Supplies
# ═══════════════════════════════════════════════════════════════

GENERAL_STORE = {
    "name": "General Store",
    "welcome": "Welcome, travelers. Browse my wares.",

    # Weapons for sale (dict format matching loot items)
    "weapons": [
        {"name": "Iron Dagger", "type": "weapon", "slot": "weapon",
         "subtype": "Dagger", "rarity": "common", "damage": 5,
         "phys_type": "piercing", "range": "melee",
         "description": "A simple iron dagger. Quick but light.",
         "buy_price": 15, "sell_price": 6, "identified": True},

        {"name": "Short Sword", "type": "weapon", "slot": "weapon",
         "subtype": "Short Sword", "rarity": "common", "damage": 7,
         "phys_type": "slashing", "range": "melee",
         "description": "A reliable short sword.",
         "buy_price": 30, "sell_price": 12, "identified": True},

        {"name": "Longsword", "type": "weapon", "slot": "weapon",
         "subtype": "Longsword", "rarity": "common", "damage": 10,
         "phys_type": "slashing", "range": "melee",
         "description": "A well-forged longsword. Standard fighter's weapon.",
         "buy_price": 60, "sell_price": 25, "identified": True},

        {"name": "Hand Axe", "type": "weapon", "slot": "weapon",
         "subtype": "Axe", "rarity": "common", "damage": 9,
         "phys_type": "slashing", "range": "melee",
         "description": "A sturdy hand axe.",
         "buy_price": 40, "sell_price": 16, "identified": True},

        {"name": "Mace", "type": "weapon", "slot": "weapon",
         "subtype": "Mace", "rarity": "common", "damage": 8,
         "phys_type": "blunt", "range": "melee",
         "description": "A heavy iron mace. Good against armored foes.",
         "buy_price": 35, "sell_price": 14, "identified": True},

        {"name": "Shortbow", "type": "weapon", "slot": "weapon",
         "subtype": "Shortbow", "rarity": "common", "damage": 6,
         "phys_type": "piercing", "range": "ranged",
         "description": "A simple shortbow for ranged attacks.",
         "buy_price": 25, "sell_price": 10, "identified": True},

        {"name": "Longbow", "type": "weapon", "slot": "weapon",
         "subtype": "Longbow", "rarity": "common", "damage": 9,
         "phys_type": "piercing", "range": "ranged",
         "description": "A proper longbow with good range and power.",
         "buy_price": 55, "sell_price": 22, "identified": True},

        {"name": "Wooden Staff", "type": "weapon", "slot": "weapon",
         "subtype": "Staff", "rarity": "common", "damage": 5,
         "phys_type": "blunt", "range": "melee",
         "stat_bonuses": {"INT": 1},
         "description": "A carved wooden staff. Enhances spellcasting.",
         "buy_price": 20, "sell_price": 8, "identified": True},

        {"name": "Spear", "type": "weapon", "slot": "weapon",
         "subtype": "Spear", "rarity": "common", "damage": 8,
         "phys_type": "piercing", "range": "reach",
         "description": "A long spear. Reach weapon — effective from mid row.",
         "buy_price": 35, "sell_price": 14, "identified": True},
    ],

    # Armor — pull from ARMOR database and add prices
    "armor": [],  # populated at import time below

    "consumables": [
        {"name": "Minor Healing Potion", "type": "consumable", "subtype": "potion",
         "rarity": "common", "heal_amount": 25,
         "description": "Restores 25 HP to one character.",
         "buy_price": 10, "sell_price": 4, "identified": True},

        {"name": "Healing Potion", "type": "consumable", "subtype": "potion",
         "rarity": "common", "heal_amount": 50,
         "description": "Restores 50 HP to one character.",
         "buy_price": 25, "sell_price": 10, "identified": True},

        {"name": "Antidote", "type": "consumable", "subtype": "potion",
         "rarity": "common", "cures": ["Poison"],
         "description": "Cures poison.",
         "buy_price": 15, "sell_price": 6, "identified": True},
    ],
}

# Populate armor shop from ARMOR database
for name, data in ARMOR.items():
    shop_item = dict(data)
    shop_item["type"] = "armor" if data["slot"] == "body" else data["slot"]
    shop_item["buy_price"] = data.get("value", 10)
    shop_item["sell_price"] = max(1, data.get("value", 10) // 3)
    shop_item["identified"] = True
    GENERAL_STORE["armor"].append(shop_item)


# ═══════════════════════════════════════════════════════════════
#  TEMPLE — Healing, Identification, Curse Removal
# ═══════════════════════════════════════════════════════════════

TEMPLE = {
    "name": "Temple of Light",
    "welcome": "Blessings upon you, travelers. How may the Temple serve?",

    "services": {
        "cure_poison": {
            "name": "Cure Poison",
            "description": "Purge all poisons from one character.",
            "cost": 30,
            "action": "cure_poison",
        },
        "remove_curse": {
            "name": "Remove Curse",
            "description": "Lift a curse from one character.",
            "cost": 100,
            "action": "remove_curse",
        },
        "resurrect": {
            "name": "Resurrect",
            "description": "Revive a fallen party member. Cost scales with level.",
            "cost": 200,  # base — actual cost = 200 + 100*level
            "action": "resurrect",
        },
        "identify_item": {
            "name": "Identify Item",
            "description": "Fully identify one item (magical and material properties).",
            "cost": 15,
            "action": "identify",
        },
        "blessing": {
            "name": "Temple Blessing",
            "description": "Receive a minor blessing for your next venture. (+5% accuracy for next dungeon)",
            "cost": 50,
            "action": "blessing",
        },
    },
}


# ═══════════════════════════════════════════════════════════════
#  TAVERN — Info, Rumors, Flavor
# ═══════════════════════════════════════════════════════════════

TAVERN = {
    "name": "The Shadowed Flagon",
    "welcome": "Pull up a chair! What'll it be?",

    "rumors": [
        "I heard goblins have been massing in the eastern woods. More than usual.",
        "A merchant was robbed on the north road last week. Bandits are getting bolder.",
        "They say the old mine is haunted. Strange lights at night.",
        "The orc chieftain in the hills has been gathering warriors. Trouble's coming.",
        "A traveling mage passed through here. Said something about shadow magic growing stronger.",
        "The wolves have been unusually aggressive this season. Something's driving them.",
        "The temple priests seem worried. They won't say about what.",
        "An old adventurer told me there's a forgotten dungeon beneath the ruins to the south.",
        "The blacksmith says ore quality has dropped. Something's wrong with the mines.",
        "I've seen strange folk in dark robes passing through at night. Gives me the chills.",
    ],
}


# ═══════════════════════════════════════════════════════════════
#  SELL PRICE CALCULATOR
# ═══════════════════════════════════════════════════════════════

def get_sell_price(item):
    """Calculate sell price for an item. Identified items sell for more."""
    if "sell_price" in item:
        return item["sell_price"]
    # Estimate from buy price or value
    value = item.get("buy_price", item.get("estimated_value", item.get("value", 5)))
    if item.get("identified"):
        return max(1, value // 3)
    else:
        return max(1, value // 5)


# ═══════════════════════════════════════════════════════════════
#  TOWN-SPECIFIC SHOP INVENTORY
# ═══════════════════════════════════════════════════════════════

# Town shop profiles: which categories to stock, price modifiers, bonus items
TOWN_SHOP_PROFILES = {
    "briarhollow": {
        "name": "Briarhollow General Store",
        "welcome": "Welcome to Briarhollow! We've got the basics.",
        "tier": "village",
        "max_weapon_price": 60,   # only cheap weapons
        "max_armor_price": 50,
        "price_mult": 1.0,        # standard prices
        "bonus_items": [
            {"name": "Torch", "type": "consumable", "subtype": "light",
             "rarity": "common", "description": "Lights dark areas. Lasts one floor.",
             "buy_price": 5, "sell_price": 1, "identified": True},
            {"name": "Rope", "type": "consumable", "subtype": "tool",
             "rarity": "common", "description": "50ft of hempen rope.",
             "buy_price": 8, "sell_price": 2, "identified": True},
        ],
    },
    "woodhaven": {
        "name": "Woodhaven Trading Post",
        "welcome": "Forest goods and ranger supplies. Take a look.",
        "tier": "town",
        "max_weapon_price": 100,
        "max_armor_price": 80,
        "price_mult": 0.95,        # slightly cheaper
        "bonus_items": [
            {"name": "Ranger's Cloak", "type": "armor", "slot": "body",
             "rarity": "uncommon", "defense": 3, "magic_resist": 2,
             "description": "A forest cloak that helps avoid detection.",
             "buy_price": 75, "sell_price": 30, "identified": True},
            {"name": "Herbal Poultice", "type": "consumable", "subtype": "potion",
             "rarity": "common", "heal": 35, "cures": ["Poison"],
             "description": "Heals 35 HP and cures mild poison.",
             "buy_price": 30, "sell_price": 12, "identified": True},
            {"name": "Hunter's Bow", "type": "weapon", "slot": "weapon",
             "subtype": "Longbow", "rarity": "uncommon", "damage": 11,
             "phys_type": "piercing", "range": "ranged",
             "description": "A well-crafted forest bow. +1 accuracy.",
             "accuracy_bonus": 5,
             "buy_price": 80, "sell_price": 32, "identified": True},
        ],
    },
    "ironhearth": {
        "name": "Ironhearth Forge & Armory",
        "welcome": "Dwarven steel, finest in Aldenmere. Name your needs.",
        "tier": "city",
        "max_weapon_price": 999,   # everything available
        "max_armor_price": 999,
        "price_mult": 1.10,        # premium prices
        "bonus_items": [
            {"name": "Dwarven War Hammer", "type": "weapon", "slot": "weapon",
             "subtype": "Mace", "rarity": "uncommon", "damage": 14,
             "phys_type": "blunt", "range": "melee",
             "special": {"armor_bypass": 0.20},
             "description": "Heavy dwarven hammer. Bypasses 20% armor.",
             "buy_price": 120, "sell_price": 50, "identified": True},
            {"name": "Steel Breastplate", "type": "armor", "slot": "body",
             "rarity": "uncommon", "defense": 10, "magic_resist": 2,
             "description": "Solid dwarven steel armor. Premium protection.",
             "buy_price": 150, "sell_price": 60, "identified": True},
            {"name": "Runic Amulet", "type": "accessory", "slot": "accessory1",
             "rarity": "uncommon", "magic_resist": 4,
             "stat_bonus": {"INT": 2},
             "description": "A dwarf-forged amulet inscribed with protective runes.",
             "buy_price": 100, "sell_price": 40, "identified": True},
            {"name": "Greater Healing Potion", "type": "consumable", "subtype": "potion",
             "rarity": "uncommon", "heal": 100,
             "description": "Restores 100 HP to one character.",
             "buy_price": 60, "sell_price": 24, "identified": True},
        ],
    },
}


def get_town_shop(town_id):
    """Return a shop inventory tailored to the given town.
    Falls back to GENERAL_STORE if town not defined."""
    profile = TOWN_SHOP_PROFILES.get(town_id)
    if not profile:
        return GENERAL_STORE

    max_wpn = profile["max_weapon_price"]
    max_arm = profile["max_armor_price"]
    mult = profile.get("price_mult", 1.0)

    shop = {
        "name": profile["name"],
        "welcome": profile["welcome"],
        "weapons": [],
        "armor": [],
        "consumables": [],
    }

    # Filter weapons by price cap
    for item in GENERAL_STORE.get("weapons", []):
        if item.get("buy_price", 0) <= max_wpn:
            it = dict(item)
            it["buy_price"] = int(it["buy_price"] * mult)
            shop["weapons"].append(it)

    # Filter armor by price cap
    for item in GENERAL_STORE.get("armor", []):
        if item.get("buy_price", 0) <= max_arm:
            it = dict(item)
            it["buy_price"] = int(it["buy_price"] * mult)
            shop["armor"].append(it)

    # Always include all consumables
    for item in GENERAL_STORE.get("consumables", []):
        it = dict(item)
        it["buy_price"] = int(it["buy_price"] * mult)
        shop["consumables"].append(it)

    # Add bonus items to appropriate category
    for bonus in profile.get("bonus_items", []):
        it = dict(bonus)
        if it.get("type") == "weapon":
            shop["weapons"].append(it)
        elif it.get("type") in ("armor", "accessory"):
            shop["armor"].append(it)
        else:
            shop["consumables"].append(it)

    return shop
