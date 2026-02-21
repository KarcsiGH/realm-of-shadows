"""
Realm of Shadows — Crafting & Enchanting System (M10)

Three forge services:
  1. CRAFT — combine materials + gold to create new items
  2. UPGRADE — improve an existing weapon or armor piece (+1, +2, etc.)
  3. ENCHANT — add elemental effects to weapons, or resistances to armor

Materials come from enemy loot drops and dungeon treasure.
"""

# ══════════════════════════════════════════════════════════
#  MATERIALS REGISTRY
# ══════════════════════════════════════════════════════════

MATERIALS = {
    # Tier 1 — common, early dungeons
    "Goblin Ear":      {"tier": 1, "category": "trophy",  "value": 2},
    "Wolf Pelt":       {"tier": 1, "category": "leather", "value": 15},
    "Wolf Fang":       {"tier": 1, "category": "reagent", "value": 10},
    "Leather Scraps":  {"tier": 1, "category": "leather", "value": 3},
    "Spider Silk":     {"tier": 1, "category": "cloth",   "value": 12},
    "Lurker Fang":     {"tier": 1, "category": "reagent", "value": 8},
    "Orc Hide Scraps": {"tier": 1, "category": "leather", "value": 5},

    # Tier 2 — uncommon, mid dungeons
    "Chitinous Plate": {"tier": 2, "category": "armor_mat", "value": 20},
    "Crystal Shard":   {"tier": 2, "category": "gem",       "value": 25},
    "Dark Iron Shard": {"tier": 2, "category": "metal",     "value": 30},
    "Gargoyle Stone":  {"tier": 2, "category": "stone",     "value": 18},

    # Tier 3 — rare, deep / boss drops (future)
    "Shadow Essence":  {"tier": 3, "category": "essence",  "value": 50},
    "Warden Steel":    {"tier": 3, "category": "metal",    "value": 60},
    "Arcane Dust":     {"tier": 3, "category": "reagent",  "value": 40},
}


# ══════════════════════════════════════════════════════════
#  CRAFTING RECIPES
# ══════════════════════════════════════════════════════════

RECIPES = [
    # ── Weapons ──
    {
        "name": "Fang Dagger",
        "materials": {"Wolf Fang": 2, "Leather Scraps": 1},
        "gold": 20,
        "result": {
            "name": "Fang Dagger", "type": "weapon", "slot": "weapon",
            "subtype": "Dagger", "rarity": "uncommon", "damage": 8,
            "phys_type": "piercing", "range": "melee",
            "description": "A dagger carved from wolf fangs. Quick and vicious.",
            "identified": True, "estimated_value": 40,
        },
    },
    {
        "name": "Silken Whip",
        "materials": {"Spider Silk": 3},
        "gold": 30,
        "result": {
            "name": "Silken Whip", "type": "weapon", "slot": "weapon",
            "subtype": "Whip", "rarity": "uncommon", "damage": 7,
            "phys_type": "slashing", "range": "melee",
            "effect": {"dex_bonus": 1},
            "description": "A whip woven from spider silk. Light and fast. +1 DEX.",
            "identified": True, "estimated_value": 55,
        },
    },
    {
        "name": "Dark Iron Mace",
        "materials": {"Dark Iron Shard": 2, "Leather Scraps": 1},
        "gold": 60,
        "result": {
            "name": "Dark Iron Mace", "type": "weapon", "slot": "weapon",
            "subtype": "Mace", "rarity": "uncommon", "damage": 14,
            "phys_type": "blunt", "range": "melee",
            "description": "A heavy mace forged from shadow-touched iron.",
            "identified": True, "estimated_value": 100,
        },
    },
    {
        "name": "Crystal Staff",
        "materials": {"Crystal Shard": 2, "Arcane Dust": 1},
        "gold": 80,
        "result": {
            "name": "Crystal Staff", "type": "weapon", "slot": "weapon",
            "subtype": "Staff", "rarity": "rare", "damage": 6,
            "phys_type": "blunt", "range": "melee",
            "spell_bonus": 5,
            "effect": {"int_bonus": 2},
            "description": "A staff tipped with a resonant crystal. +5 spell power, +2 INT.",
            "identified": True, "estimated_value": 180,
        },
    },

    # ── Armor ──
    {
        "name": "Wolf Pelt Cloak",
        "materials": {"Wolf Pelt": 2},
        "gold": 25,
        "result": {
            "name": "Wolf Pelt Cloak", "type": "armor", "slot": "body",
            "subtype": "cloak", "rarity": "uncommon", "armor_tier": "light",
            "defense": 3, "speed_bonus": 1,
            "description": "A warm cloak of wolf fur. Light protection, no speed penalty.",
            "identified": True, "estimated_value": 50,
        },
    },
    {
        "name": "Chitin Shield",
        "materials": {"Chitinous Plate": 2, "Leather Scraps": 2},
        "gold": 45,
        "result": {
            "name": "Chitin Shield", "type": "armor", "slot": "off_hand",
            "subtype": "shield", "rarity": "uncommon",
            "defense": 4, "magic_resist": 2,
            "description": "A shield made from giant spider chitin. Surprisingly light.",
            "identified": True, "estimated_value": 75,
        },
    },
    {
        "name": "Gargoyle Helm",
        "materials": {"Gargoyle Stone": 2},
        "gold": 40,
        "result": {
            "name": "Gargoyle Helm", "type": "armor", "slot": "head",
            "subtype": "helmet", "rarity": "uncommon",
            "defense": 5,
            "effect": {"con_bonus": 1},
            "description": "A helmet carved from gargoyle stone. Very sturdy. +1 CON.",
            "identified": True, "estimated_value": 65,
        },
    },
    {
        "name": "Silk-Weave Robes",
        "materials": {"Spider Silk": 4},
        "gold": 50,
        "result": {
            "name": "Silk-Weave Robes", "type": "armor", "slot": "body",
            "subtype": "robes", "rarity": "uncommon", "armor_tier": "clothing",
            "defense": 2, "magic_resist": 5,
            "effect": {"int_bonus": 1},
            "description": "Robes woven from enchanted spider silk. +5 magic resist, +1 INT.",
            "identified": True, "estimated_value": 90,
        },
    },

    # ── Accessories ──
    {
        "name": "Fang Necklace",
        "materials": {"Wolf Fang": 3, "Lurker Fang": 1},
        "gold": 30,
        "result": {
            "name": "Fang Necklace", "type": "accessory", "slot": "accessory1",
            "subtype": "amulet", "rarity": "uncommon",
            "effect": {"str_bonus": 2},
            "description": "A necklace of predator fangs. +2 STR.",
            "identified": True, "estimated_value": 60,
        },
    },
    {
        "name": "Crystal Pendant",
        "materials": {"Crystal Shard": 1},
        "gold": 35,
        "result": {
            "name": "Crystal Pendant", "type": "accessory", "slot": "accessory1",
            "subtype": "amulet", "rarity": "uncommon",
            "effect": {"wis_bonus": 2},
            "description": "A pendant with a glowing crystal. +2 WIS.",
            "identified": True, "estimated_value": 55,
        },
    },

    # ── Consumables ──
    {
        "name": "Antidote Potion",
        "materials": {"Lurker Fang": 1, "Goblin Ear": 2},
        "gold": 10,
        "result": {
            "name": "Antidote Potion", "type": "consumable", "slot": None,
            "subtype": "potion", "rarity": "common",
            "effect": {"cure_poison": True},
            "description": "Cures poison.",
            "identified": True, "estimated_value": 15,
        },
    },
]


# ══════════════════════════════════════════════════════════
#  UPGRADE SYSTEM
# ══════════════════════════════════════════════════════════
#  Upgrade a weapon or armor piece: +1, +2, +3 (max)
#  Each level costs materials + gold, scaling up.

UPGRADE_COSTS = {
    # level: (gold, material_count, min_tier)
    1: (40,  2, 1),   # +1: 40g + 2 tier-1 materials
    2: (100, 3, 2),   # +2: 100g + 3 tier-2 materials
    3: (250, 4, 2),   # +3: 250g + 4 tier-2 materials
}

MAX_UPGRADE = 3

def get_upgrade_level(item):
    """Get current upgrade level of an item."""
    return item.get("upgrade_level", 0)

def get_upgrade_cost(item):
    """Get cost to upgrade item to next level. Returns None if maxed."""
    cur = get_upgrade_level(item)
    nxt = cur + 1
    if nxt > MAX_UPGRADE:
        return None
    gold, mat_count, min_tier = UPGRADE_COSTS[nxt]
    return {"gold": gold, "material_count": mat_count, "min_material_tier": min_tier}

def apply_upgrade(item):
    """Apply +1 upgrade to item. Modifies in place."""
    cur = get_upgrade_level(item)
    nxt = cur + 1
    if nxt > MAX_UPGRADE:
        return False

    item["upgrade_level"] = nxt

    # Boost stats based on item type
    if item.get("type") == "weapon":
        item["damage"] = item.get("damage", 0) + 3  # +3 damage per level
    elif item.get("type") == "armor":
        item["defense"] = item.get("defense", 0) + 2  # +2 defense per level

    # Update name to show upgrade
    base = item.get("base_name", item["name"])
    item["base_name"] = base
    item["name"] = f"{base} +{nxt}"

    return True


# ══════════════════════════════════════════════════════════
#  ENCHANTING SYSTEM
# ══════════════════════════════════════════════════════════
#  Add an elemental property to a weapon or resistance to armor.
#  One enchant per item. Can overwrite.

ENCHANTMENTS = {
    # Weapon enchants — add elemental damage
    "Flame":     {"element": "fire",      "bonus": 4, "materials": {"Wolf Fang": 2},              "gold": 50,  "desc": "Adds fire damage."},
    "Frost":     {"element": "ice",       "bonus": 4, "materials": {"Crystal Shard": 1},          "gold": 50,  "desc": "Adds ice damage."},
    "Shock":     {"element": "lightning", "bonus": 4, "materials": {"Crystal Shard": 1},          "gold": 50,  "desc": "Adds lightning damage."},
    "Venom":     {"element": "nature",    "bonus": 3, "materials": {"Lurker Fang": 2},            "gold": 40,  "desc": "Adds poison damage."},
    "Shadow":    {"element": "shadow",    "bonus": 4, "materials": {"Dark Iron Shard": 1},        "gold": 60,  "desc": "Adds shadow damage."},
    "Holy":      {"element": "divine",    "bonus": 5, "materials": {"Crystal Shard": 1, "Gargoyle Stone": 1}, "gold": 70, "desc": "Adds divine damage."},

    # Armor enchants — add elemental resistance
    "Fire Ward":    {"resist": "fire",      "bonus": 3, "materials": {"Wolf Pelt": 2},            "gold": 45,  "desc": "Resist fire."},
    "Frost Ward":   {"resist": "ice",       "bonus": 3, "materials": {"Spider Silk": 2},          "gold": 45,  "desc": "Resist ice."},
    "Shock Ward":   {"resist": "lightning", "bonus": 3, "materials": {"Crystal Shard": 1},        "gold": 45,  "desc": "Resist lightning."},
    "Shadow Ward":  {"resist": "shadow",    "bonus": 3, "materials": {"Dark Iron Shard": 1},      "gold": 55,  "desc": "Resist shadow."},
    "Nature Ward":  {"resist": "nature",    "bonus": 3, "materials": {"Chitinous Plate": 1},      "gold": 40,  "desc": "Resist nature/poison."},
}


def get_applicable_enchants(item):
    """Return list of enchantment names valid for this item."""
    itype = item.get("type", "")
    result = []
    for name, ench in ENCHANTMENTS.items():
        if itype == "weapon" and "element" in ench:
            result.append(name)
        elif itype == "armor" and "resist" in ench:
            result.append(name)
    return result


def apply_enchant(item, enchant_name):
    """Apply enchantment to item. Modifies in place."""
    ench = ENCHANTMENTS.get(enchant_name)
    if not ench:
        return False

    # Remove old enchant if any
    item.pop("enchant_element", None)
    item.pop("enchant_bonus", None)
    item.pop("enchant_resist", None)
    item.pop("enchant_resist_bonus", None)

    if "element" in ench:
        # Weapon enchant
        item["enchant_element"] = ench["element"]
        item["enchant_bonus"] = ench["bonus"]
    elif "resist" in ench:
        # Armor enchant
        item["enchant_resist"] = ench["resist"]
        item["enchant_resist_bonus"] = ench["bonus"]

    item["enchant_name"] = enchant_name

    # Update name
    base = item.get("base_name", item["name"].split(" [")[0])
    item["base_name"] = base
    upgrade = f" +{item['upgrade_level']}" if item.get("upgrade_level", 0) > 0 else ""
    item["name"] = f"{base}{upgrade} [{enchant_name}]"

    return True


# ══════════════════════════════════════════════════════════
#  HELPER: Count materials in party inventory
# ══════════════════════════════════════════════════════════

def count_material(party, mat_name):
    """Count how many of a material the party has across all inventories."""
    total = 0
    for c in party:
        for item in c.inventory:
            if item.get("type") == "material" and item.get("name") == mat_name:
                total += item.get("quantity", 1)
    return total


def consume_materials(party, materials_needed):
    """Remove materials from party inventories. Returns True if successful."""
    # First verify we have enough
    for mat, needed in materials_needed.items():
        if count_material(party, mat) < needed:
            return False

    # Remove them
    for mat, needed in materials_needed.items():
        remaining = needed
        for c in party:
            to_remove = []
            for i, item in enumerate(c.inventory):
                if remaining <= 0:
                    break
                if item.get("type") == "material" and item.get("name") == mat:
                    qty = item.get("quantity", 1)
                    if qty <= remaining:
                        to_remove.append(i)
                        remaining -= qty
                    else:
                        item["quantity"] = qty - remaining
                        remaining = 0
            for idx in reversed(to_remove):
                c.inventory.pop(idx)
    return True


def consume_gold(party, amount):
    """Remove gold from party, spreading across members. Returns True if enough."""
    total = sum(c.gold for c in party)
    if total < amount:
        return False
    remaining = amount
    for c in party:
        take = min(c.gold, remaining)
        c.gold -= take
        remaining -= take
        if remaining <= 0:
            break
    return True


def can_afford_recipe(party, recipe):
    """Check if party can afford a crafting recipe."""
    if sum(c.gold for c in party) < recipe["gold"]:
        return False
    for mat, needed in recipe["materials"].items():
        if count_material(party, mat) < needed:
            return False
    return True


def craft_item(party, recipe):
    """Craft an item. Returns the crafted item or None."""
    if not can_afford_recipe(party, recipe):
        return None
    if not consume_gold(party, recipe["gold"]):
        return None
    if not consume_materials(party, recipe["materials"]):
        return None
    return dict(recipe["result"])


def get_upgradeable_items(party):
    """Get all equipped and inventory items that can be upgraded."""
    items = []
    for c in party:
        # Equipped items
        for slot, item in c.equipment.items():
            if item and item.get("type") in ("weapon", "armor"):
                if get_upgrade_level(item) < MAX_UPGRADE:
                    items.append((c, slot, item, "equipped"))
        # Inventory items
        for i, item in enumerate(c.inventory):
            if item.get("type") in ("weapon", "armor"):
                if get_upgrade_level(item) < MAX_UPGRADE:
                    items.append((c, i, item, "inventory"))
    return items


def get_enchantable_items(party):
    """Get all equipped and inventory items that can be enchanted."""
    items = []
    for c in party:
        for slot, item in c.equipment.items():
            if item and item.get("type") in ("weapon", "armor"):
                items.append((c, slot, item, "equipped"))
        for i, item in enumerate(c.inventory):
            if item.get("type") in ("weapon", "armor"):
                items.append((c, i, item, "inventory"))
    return items


def get_materials_of_tier(party, min_tier):
    """Get a dict of {material_name: count} for materials at or above min_tier."""
    result = {}
    for c in party:
        for item in c.inventory:
            if item.get("type") == "material":
                mat_info = MATERIALS.get(item.get("name", ""))
                if mat_info and mat_info["tier"] >= min_tier:
                    name = item["name"]
                    result[name] = result.get(name, 0) + item.get("quantity", 1)
    return result
