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
    "greenwood": {
        "name": "Greenwood Ranger Supplies",
        "welcome": "Basic supplies. Don't expect luxury out here.",
        "tier": "village",
        "max_weapon_price": 70,
        "max_armor_price": 60,
        "price_mult": 0.90,       # cheaper, remote frontier pricing
        "bonus_items": [
            {"name": "Camouflage Cloak", "type": "armor", "slot": "body",
             "rarity": "common", "defense": 2, "magic_resist": 1,
             "description": "Blends with the forest. Hard to spot at range.",
             "buy_price": 45, "sell_price": 18, "identified": True},
            {"name": "Herbal Antidote", "type": "consumable", "subtype": "potion",
             "rarity": "common", "cures": ["Poison", "Disease"],
             "description": "Brewed from forest roots. Cures poison and disease.",
             "buy_price": 20, "sell_price": 8, "identified": True},
        ],
    },
    "saltmere": {
        "name": "Saltmere Trader",
        "welcome": "Ask no questions, I'll tell no lies. What do you need?",
        "tier": "town",
        "max_weapon_price": 120,
        "max_armor_price": 100,
        "price_mult": 0.85,       # black market discount — some things fell off a ship
        "bonus_items": [
            {"name": "Smuggler's Blade", "type": "weapon", "slot": "weapon",
             "subtype": "Dagger", "rarity": "uncommon", "damage": 9,
             "phys_type": "piercing", "range": "melee",
             "special": {"first_strike": True},
             "description": "A thin blade easy to hide. Always strikes first.",
             "buy_price": 90, "sell_price": 36, "identified": True},
            {"name": "Lockpick Set", "type": "consumable", "subtype": "tool",
             "rarity": "uncommon",
             "description": "Professional lockpicks. Opens most locked chests.",
             "buy_price": 40, "sell_price": 16, "identified": True},
            {"name": "Smoke Bomb", "type": "consumable", "subtype": "thrown",
             "rarity": "common",
             "description": "Fills an area with smoke. Enemies lose accuracy for 2 turns.",
             "buy_price": 25, "sell_price": 10, "identified": True},
        ],
    },
    "sanctum": {
        "name": "Sacred Goods of Sanctum",
        "welcome": "May your purchases bring you peace and protection.",
        "tier": "city",
        "max_weapon_price": 150,
        "max_armor_price": 200,
        "price_mult": 1.05,
        "bonus_items": [
            {"name": "Holy Water (Flask)", "type": "consumable", "subtype": "potion",
             "rarity": "uncommon", "damage_undead": 60,
             "description": "Blessed water. Deals 60 holy damage to undead. No effect on living.",
             "buy_price": 35, "sell_price": 14, "identified": True},
            {"name": "Sanctified Shield", "type": "armor", "slot": "offhand",
             "rarity": "uncommon", "defense": 6, "magic_resist": 5,
             "special": {"undead_resist": 0.20},
             "description": "A shield blessed by the High Priest. +20% resist to undead abilities.",
             "buy_price": 140, "sell_price": 56, "identified": True},
            {"name": "Pilgrim's Staff", "type": "weapon", "slot": "weapon",
             "subtype": "Staff", "rarity": "uncommon", "damage": 8,
             "phys_type": "blunt", "range": "melee",
             "special": {"heal_on_kill": 15},
             "description": "A blessed walking staff. Restores 15 HP to the wielder on each kill.",
             "buy_price": 110, "sell_price": 44, "identified": True},
        ],
    },
    "crystalspire": {
        "name": "Components & Curios",
        "welcome": "Rare components and spell tomes. Knowledge has its price.",
        "tier": "city",
        "max_weapon_price": 999,
        "max_armor_price": 999,
        "price_mult": 1.15,       # premium — mage city prices
        "bonus_items": [
            {"name": "Spell Tome: Fireball", "type": "consumable", "subtype": "tome",
             "rarity": "rare", "teaches_spell": "fireball",
             "description": "Teaches the Fireball spell. Mages only.",
             "buy_price": 200, "sell_price": 80, "identified": True},
            {"name": "Crystal Focus", "type": "accessory", "slot": "accessory1",
             "rarity": "uncommon", "magic_resist": 3,
             "stat_bonus": {"INT": 3, "WIS": 1},
             "description": "A crystal lens that sharpens magical focus. +3 INT, +1 WIS.",
             "buy_price": 180, "sell_price": 72, "identified": True},
            {"name": "Mana Vial", "type": "consumable", "subtype": "potion",
             "rarity": "uncommon", "restore_mp": 60,
             "description": "Crystallized mana. Restores 60 MP to one character.",
             "buy_price": 55, "sell_price": 22, "identified": True},
            {"name": "Scroll of Identify", "type": "consumable", "subtype": "scroll",
             "rarity": "common",
             "description": "Identifies one unknown item instantly.",
             "buy_price": 30, "sell_price": 12, "identified": True},
            {"name": "Scroll of Remove Curse", "type": "consumable", "subtype": "scroll",
             "effect": "remove_curse", "rarity": "uncommon",
             "description": "Lifts all curses from one character, freeing any cursed equipment.",
             "buy_price": 90, "sell_price": 36, "identified": True},
        ],
    },
    "thornhaven": {
        "name": "Imperial Marketplace",
        "welcome": "The finest goods in Aldenmere. The Governor shops here himself.",
        "tier": "capital",
        "max_weapon_price": 999,
        "max_armor_price": 999,
        "price_mult": 1.20,       # capital prices — everything available but costly
        "bonus_items": [
            {"name": "Imperial Longsword", "type": "weapon", "slot": "weapon",
             "subtype": "Longsword", "rarity": "rare", "damage": 16,
             "phys_type": "slashing", "range": "melee",
             "stat_bonus": {"STR": 1},
             "description": "An imperial-forged blade bearing the seal of Aldenmere. +1 STR.",
             "buy_price": 280, "sell_price": 112, "identified": True},
            {"name": "Aldenmere Plate", "type": "armor", "slot": "body",
             "rarity": "rare", "defense": 14, "magic_resist": 4,
             "description": "Full plate armor from the imperial armory. The finest protection available.",
             "buy_price": 320, "sell_price": 128, "identified": True},
            {"name": "Ring of the Realm", "type": "accessory", "slot": "accessory1",
             "rarity": "rare",
             "stat_bonus": {"STR": 1, "INT": 1, "WIS": 1, "DEX": 1, "CON": 1},
             "description": "Bearing the imperial crest. Grants +1 to all stats.",
             "buy_price": 350, "sell_price": 140, "identified": True},
            {"name": "Elixir of Champions", "type": "consumable", "subtype": "potion",
             "rarity": "rare", "heal": 200, "restore_mp": 100,
             "description": "Restores 200 HP and 100 MP. The finest restorative in the realm.",
             "buy_price": 120, "sell_price": 48, "identified": True},
        ],
    },
}


def get_town_shop(town_id, party_classes=None):
    """Return a shop inventory tailored to the given town.
    Falls back to GENERAL_STORE if town not defined.
    party_classes: list of class names to filter class-specific items.
    """
    from data.advanced_equipment import get_shop_weapons, get_shop_armor, get_shop_accessories
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

    tier = profile.get("tier", "village")

    # Class-specific weapons from advanced catalog
    seen_names = set()
    for item in get_shop_weapons(tier, party_classes):
        if item["buy_price"] <= max_wpn and item["name"] not in seen_names:
            it = dict(item)
            it["buy_price"] = int(it["buy_price"] * mult)
            it["sell_price"] = it["buy_price"] // 4
            shop["weapons"].append(it)
            seen_names.add(item["name"])

    # Generic weapons from GENERAL_STORE as variety fallback
    for item in GENERAL_STORE.get("weapons", []):
        if item.get("buy_price", 0) <= max_wpn and item["name"] not in seen_names:
            it = dict(item)
            it["buy_price"] = int(it["buy_price"] * mult)
            shop["weapons"].append(it)
            seen_names.add(item["name"])

    # Class-specific armor + accessories
    seen_names = set()
    for item in get_shop_armor(tier, party_classes):
        if item["buy_price"] <= max_arm and item["name"] not in seen_names:
            it = dict(item)
            it["buy_price"] = int(it["buy_price"] * mult)
            it["sell_price"] = it["buy_price"] // 4
            shop["armor"].append(it)
            seen_names.add(item["name"])

    for item in get_shop_accessories(tier, party_classes):
        if item["buy_price"] <= max_arm and item["name"] not in seen_names:
            it = dict(item)
            it["buy_price"] = int(it["buy_price"] * mult)
            it["sell_price"] = it["buy_price"] // 4
            shop["armor"].append(it)
            seen_names.add(item["name"])

    # GENERAL_STORE armor fallback
    for item in GENERAL_STORE.get("armor", []):
        if item.get("buy_price", 0) <= max_arm and item["name"] not in seen_names:
            it = dict(item)
            it["buy_price"] = int(it["buy_price"] * mult)
            shop["armor"].append(it)
            seen_names.add(item["name"])

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
