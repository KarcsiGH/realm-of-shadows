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
        "rest_heal": {
            "name": "Rest & Heal",
            "description": "Restore all HP and resources for the entire party.",
            "cost": 0,  # free — resting is free at temple
        },
        "identify_item": {
            "name": "Identify Item",
            "description": "Fully identify one item (magical and material properties).",
            "cost": 15,
        },
        "remove_curse": {
            "name": "Remove Curse",
            "description": "Remove a curse from one character or item.",
            "cost": 50,
        },
        "resurrect": {
            "name": "Resurrect",
            "description": "Bring a fallen party member back to life.",
            "cost": 100,
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
