"""
Realm of Shadows — Equipment System

Equipment slots per character:
  Weapon     — one weapon (or unarmed)
  Off-hand   — shield or second light weapon (future: dual wield)
  Head       — helmet or Ki Stone
  Body       — armor (clothing/light/medium/heavy)
  Hands      — gloves/gauntlets
  Feet       — boots
  Accessory1 — ring, amulet, trinket
  Accessory2 — ring, amulet, trinket (cannot duplicate Accessory1)

Armor proficiency from Combat_System_Design_v2:
  Fighter: all armor, all shields
  Cleric:  up to heavy, shields
  Ranger:  up to medium, no shields
  Thief:   up to light, no shields
  Monk:    clothing only, no shields
  Mage:    clothing only, no shields
"""

# ═══════════════════════════════════════════════════════════════
#  EQUIPMENT SLOTS
# ═══════════════════════════════════════════════════════════════

SLOT_ORDER = ["weapon", "off_hand", "head", "body", "hands", "feet", "accessory1", "accessory2"]

SLOT_NAMES = {
    "weapon":     "Weapon",
    "off_hand":   "Off-Hand",
    "head":       "Head",
    "body":       "Body",
    "hands":      "Hands",
    "feet":       "Feet",
    "accessory1": "Accessory 1",
    "accessory2": "Accessory 2",
}


def empty_equipment():
    """Return a fresh empty equipment dict."""
    return {slot: None for slot in SLOT_ORDER}


# ═══════════════════════════════════════════════════════════════
#  ARMOR PROFICIENCY
# ═══════════════════════════════════════════════════════════════

# Armor weight classes in ascending order
ARMOR_TIERS = ["clothing", "light", "medium", "heavy"]

# Max armor tier each class can wear without penalty
CLASS_ARMOR_PROF = {
    "Fighter":  "heavy",
    "Cleric":   "heavy",
    "Ranger":   "medium",
    "Thief":    "light",
    "Monk":     "clothing",
    "Mage":     "clothing",
    # Hybrid classes (future)
    "Battlemage":  "light",
    "Paladin":     "heavy",
    "Knight":      "heavy",
    "Assassin":    "light",
    "Spellthief":  "light",
    "Sage":        "clothing",
    "Warlock":     "light",
    "Ki Master":   "clothing",
    "Merchant":    "medium",
}

# Classes that can use shields
SHIELD_CLASSES = {"Fighter", "Cleric", "Paladin", "Knight"}

# Non-proficient penalties
NON_PROF_ARMOR_DEF_MULT = 0.5    # only get 50% of armor defense
NON_PROF_ARMOR_SPEED = -3         # speed penalty
NON_PROF_SHIELD_DEF_MULT = 0.5


def can_wear_armor(class_name, armor_tier):
    """Check if a class is proficient with an armor tier."""
    max_tier = CLASS_ARMOR_PROF.get(class_name, "clothing")
    return ARMOR_TIERS.index(armor_tier) <= ARMOR_TIERS.index(max_tier)


def can_use_shield(class_name):
    return class_name in SHIELD_CLASSES


# ═══════════════════════════════════════════════════════════════
#  ARMOR DATABASE
# ═══════════════════════════════════════════════════════════════

ARMOR = {
    # ── Clothing (Tier: clothing) ──
    "Traveler's Clothes": {
        "name": "Traveler's Clothes", "slot": "body",
        "armor_tier": "clothing", "defense": 1, "magic_resist": 0,
        "speed_mod": 0, "stat_bonuses": {},
        "rarity": "common", "value": 5,
        "description": "Simple clothing. Offers minimal protection.",
    },
    "Mage's Robes": {
        "name": "Mage's Robes", "slot": "body",
        "armor_tier": "clothing", "defense": 2, "magic_resist": 3,
        "speed_mod": 0, "stat_bonuses": {"INT": 1},
        "rarity": "uncommon", "value": 30,
        "description": "Enchanted robes that enhance magical focus.",
    },
    "Monk's Wraps": {
        "name": "Monk's Wraps", "slot": "body",
        "armor_tier": "clothing", "defense": 2, "magic_resist": 2,
        "speed_mod": 1, "stat_bonuses": {"WIS": 1},
        "rarity": "uncommon", "value": 25,
        "description": "Light wraps that don't interfere with Ki flow.",
    },

    # ── Light Armor ──
    "Leather Vest": {
        "name": "Leather Vest", "slot": "body",
        "armor_tier": "light", "defense": 4, "magic_resist": 0,
        "speed_mod": 0, "stat_bonuses": {},
        "rarity": "common", "value": 20,
        "description": "Basic leather protection.",
    },
    "Studded Leather": {
        "name": "Studded Leather", "slot": "body",
        "armor_tier": "light", "defense": 6, "magic_resist": 0,
        "speed_mod": 0, "stat_bonuses": {},
        "rarity": "common", "value": 40,
        "description": "Leather armor reinforced with metal studs.",
    },
    "Shadow Leather": {
        "name": "Shadow Leather", "slot": "body",
        "armor_tier": "light", "defense": 7, "magic_resist": 1,
        "speed_mod": 1, "stat_bonuses": {"DEX": 1},
        "rarity": "uncommon", "value": 80,
        "description": "Dark-dyed leather favored by rogues.",
    },

    # ── Medium Armor ──
    "Chain Shirt": {
        "name": "Chain Shirt", "slot": "body",
        "armor_tier": "medium", "defense": 9, "magic_resist": 0,
        "speed_mod": -1, "stat_bonuses": {},
        "rarity": "common", "value": 60,
        "description": "A shirt of interlocking metal rings.",
    },
    "Scale Mail": {
        "name": "Scale Mail", "slot": "body",
        "armor_tier": "medium", "defense": 12, "magic_resist": 0,
        "speed_mod": -1, "stat_bonuses": {},
        "rarity": "common", "value": 90,
        "description": "Overlapping metal scales on a leather backing.",
    },
    "Ranger's Hauberk": {
        "name": "Ranger's Hauberk", "slot": "body",
        "armor_tier": "medium", "defense": 10, "magic_resist": 2,
        "speed_mod": 0, "stat_bonuses": {"WIS": 1},
        "rarity": "uncommon", "value": 120,
        "description": "Light chainmail woven with nature-blessed threads.",
    },

    # ── Heavy Armor ──
    "Breastplate": {
        "name": "Breastplate", "slot": "body",
        "armor_tier": "heavy", "defense": 15, "magic_resist": 0,
        "speed_mod": -2, "stat_bonuses": {},
        "rarity": "common", "value": 120,
        "description": "Solid steel chest plate.",
    },
    "Full Plate": {
        "name": "Full Plate", "slot": "body",
        "armor_tier": "heavy", "defense": 20, "magic_resist": 0,
        "speed_mod": -4, "stat_bonuses": {"CON": 1},
        "rarity": "rare", "value": 300,
        "description": "Complete suit of plate armor. Maximum protection.",
    },

    # ── Shields ──
    "Wooden Shield": {
        "name": "Wooden Shield", "slot": "off_hand",
        "armor_tier": "shield", "defense": 3, "magic_resist": 0,
        "speed_mod": 0, "stat_bonuses": {},
        "rarity": "common", "value": 10,
        "description": "A simple round wooden shield.",
    },
    "Iron Shield": {
        "name": "Iron Shield", "slot": "off_hand",
        "armor_tier": "shield", "defense": 5, "magic_resist": 1,
        "speed_mod": -1, "stat_bonuses": {},
        "rarity": "common", "value": 40,
        "description": "A sturdy iron-banded shield.",
    },
    "Tower Shield": {
        "name": "Tower Shield", "slot": "off_hand",
        "armor_tier": "shield", "defense": 8, "magic_resist": 2,
        "speed_mod": -2, "stat_bonuses": {"CON": 1},
        "rarity": "uncommon", "value": 100,
        "description": "A massive shield that covers your whole body.",
    },

    # ── Helmets ──
    "Leather Cap": {
        "name": "Leather Cap", "slot": "head",
        "armor_tier": "light", "defense": 1, "magic_resist": 0,
        "speed_mod": 0, "stat_bonuses": {},
        "rarity": "common", "value": 8,
        "description": "Simple leather head protection.",
    },
    "Iron Helm": {
        "name": "Iron Helm", "slot": "head",
        "armor_tier": "medium", "defense": 3, "magic_resist": 0,
        "speed_mod": 0, "stat_bonuses": {},
        "rarity": "common", "value": 25,
        "description": "An iron helmet with a nose guard.",
    },
    "Circlet of Focus": {
        "name": "Circlet of Focus", "slot": "head",
        "armor_tier": "clothing", "defense": 0, "magic_resist": 2,
        "speed_mod": 0, "stat_bonuses": {"INT": 2},
        "rarity": "rare", "value": 150,
        "description": "A silver circlet that sharpens the mind.",
    },

    # ── Gloves ──
    "Leather Gloves": {
        "name": "Leather Gloves", "slot": "hands",
        "armor_tier": "light", "defense": 1, "magic_resist": 0,
        "speed_mod": 0, "stat_bonuses": {},
        "rarity": "common", "value": 6,
        "description": "Basic leather gloves.",
    },
    "Gauntlets": {
        "name": "Gauntlets", "slot": "hands",
        "armor_tier": "heavy", "defense": 3, "magic_resist": 0,
        "speed_mod": 0, "stat_bonuses": {"STR": 1},
        "rarity": "uncommon", "value": 45,
        "description": "Steel gauntlets that add force to your strikes.",
    },
    "Thief's Gloves": {
        "name": "Thief's Gloves", "slot": "hands",
        "armor_tier": "clothing", "defense": 0, "magic_resist": 0,
        "speed_mod": 0, "stat_bonuses": {"DEX": 2},
        "rarity": "uncommon", "value": 60,
        "description": "Nimble gloves that enhance dexterity.",
    },

    # ── Boots ──
    "Leather Boots": {
        "name": "Leather Boots", "slot": "feet",
        "armor_tier": "light", "defense": 1, "magic_resist": 0,
        "speed_mod": 0, "stat_bonuses": {},
        "rarity": "common", "value": 8,
        "description": "Sturdy leather boots.",
    },
    "Boots of Swiftness": {
        "name": "Boots of Swiftness", "slot": "feet",
        "armor_tier": "light", "defense": 1, "magic_resist": 0,
        "speed_mod": 3, "stat_bonuses": {"DEX": 1},
        "rarity": "rare", "value": 120,
        "description": "Enchanted boots that quicken your step.",
    },
    "Iron Greaves": {
        "name": "Iron Greaves", "slot": "feet",
        "armor_tier": "heavy", "defense": 3, "magic_resist": 0,
        "speed_mod": -1, "stat_bonuses": {},
        "rarity": "common", "value": 30,
        "description": "Heavy iron leg protection.",
    },

    # ── Accessories ──
    "Ring of Strength": {
        "name": "Ring of Strength", "slot": "accessory",
        "armor_tier": "clothing", "defense": 0, "magic_resist": 0,
        "speed_mod": 0, "stat_bonuses": {"STR": 2},
        "rarity": "uncommon", "value": 80,
        "description": "A thick iron ring that bolsters strength.",
    },
    "Amulet of Wisdom": {
        "name": "Amulet of Wisdom", "slot": "accessory",
        "armor_tier": "clothing", "defense": 0, "magic_resist": 2,
        "speed_mod": 0, "stat_bonuses": {"WIS": 2},
        "rarity": "uncommon", "value": 80,
        "description": "A carved bone amulet radiating calm.",
    },
    "Talisman of Piety": {
        "name": "Talisman of Piety", "slot": "accessory",
        "armor_tier": "clothing", "defense": 0, "magic_resist": 3,
        "speed_mod": 0, "stat_bonuses": {"PIE": 2},
        "rarity": "rare", "value": 120,
        "description": "A holy relic blessed by the temple.",
    },
    "Scout's Pendant": {
        "name": "Scout's Pendant", "slot": "accessory",
        "armor_tier": "clothing", "defense": 0, "magic_resist": 0,
        "speed_mod": 2, "stat_bonuses": {"DEX": 1},
        "rarity": "uncommon", "value": 60,
        "description": "A feather pendant favored by scouts.",
    },
}


# ═══════════════════════════════════════════════════════════════
#  STARTING EQUIPMENT BY CLASS
# ═══════════════════════════════════════════════════════════════

STARTING_EQUIPMENT = {
    "Fighter":  {"body": "Leather Vest", "off_hand": "Wooden Shield"},
    "Mage":     {"body": "Traveler's Clothes"},
    "Cleric":   {"body": "Chain Shirt", "off_hand": "Wooden Shield"},
    "Thief":    {"body": "Leather Vest"},
    "Ranger":   {"body": "Leather Vest"},
    "Monk":     {"body": "Traveler's Clothes"},
}


# ═══════════════════════════════════════════════════════════════
#  EQUIP / UNEQUIP LOGIC
# ═══════════════════════════════════════════════════════════════

def get_item_slot(item):
    """Determine which equipment slot an item goes in."""
    slot = item.get("slot", "")
    # Accessories can go in either accessory slot
    if slot == "accessory":
        return "accessory1"  # default; caller handles picking slot
    return slot


def can_equip(character, item):
    """Check if a character can equip an item. Returns (can_equip, reason)."""
    slot = item.get("slot", "")
    class_name = character.class_name

    # Weapon check — handled by weapon proficiency (already in weapons.py)
    if slot == "weapon":
        return True, ""

    # Shield check
    if slot == "off_hand" and item.get("armor_tier") == "shield":
        if not can_use_shield(class_name):
            return False, f"{class_name} cannot use shields"
        return True, ""

    # Armor proficiency check (body, head, hands, feet)
    armor_tier = item.get("armor_tier", "clothing")
    if armor_tier != "clothing" and armor_tier != "shield":
        if not can_wear_armor(class_name, armor_tier):
            return False, f"{class_name} is not proficient with {armor_tier} armor"

    # Stat requirements
    for stat, req in item.get("stat_requirements", {}).items():
        if character.stats.get(stat, 0) < req:
            return False, f"Requires {stat} {req} (have {character.stats.get(stat, 0)})"

    return True, ""


def equip_item(character, item, target_slot=None):
    """Equip an item to a character. Returns (success, unequipped_item, message).
    Handles auto-slot detection and swapping."""
    if not hasattr(character, "equipment") or character.equipment is None:
        character.equipment = empty_equipment()

    ok, reason = can_equip(character, item)
    if not ok:
        return False, None, reason

    # Determine slot
    item_slot = item.get("slot", "")
    if item_slot == "accessory":
        # Try accessory1 first, then accessory2
        if target_slot in ("accessory1", "accessory2"):
            slot = target_slot
        elif character.equipment.get("accessory1") is None:
            slot = "accessory1"
        elif character.equipment.get("accessory2") is None:
            slot = "accessory2"
        else:
            slot = "accessory1"  # swap into slot 1 by default
    elif target_slot and target_slot in SLOT_ORDER:
        slot = target_slot
    else:
        slot = item_slot

    if slot not in SLOT_ORDER:
        return False, None, f"Unknown equipment slot: {slot}"

    # Unequip existing item in that slot
    old_item = character.equipment.get(slot)
    character.equipment[slot] = item

    # Remove item from inventory
    if item in character.inventory:
        character.inventory.remove(item)

    # Put old item back in inventory
    if old_item is not None:
        character.inventory.append(old_item)

    item_name = item.get("name", "item")
    return True, old_item, f"Equipped {item_name}"


def unequip_item(character, slot):
    """Unequip item from a slot, put it in inventory.
    Returns (success, item, message)."""
    if not hasattr(character, "equipment") or character.equipment is None:
        return False, None, "No equipment"

    item = character.equipment.get(slot)
    if item is None:
        return False, None, "Nothing equipped in that slot"

    character.equipment[slot] = None
    character.inventory.append(item)
    return True, item, f"Unequipped {item.get('name', 'item')}"


# ═══════════════════════════════════════════════════════════════
#  EQUIPMENT STAT CALCULATIONS
# ═══════════════════════════════════════════════════════════════

def calc_equipment_defense(character):
    """Total defense bonus from all equipped armor/shields."""
    if not hasattr(character, "equipment") or not character.equipment:
        return 0
    total = 0
    for slot, item in character.equipment.items():
        if item is None:
            continue
        defense = item.get("defense", 0)
        armor_tier = item.get("armor_tier", "clothing")

        # Proficiency check
        if armor_tier == "shield":
            if not can_use_shield(character.class_name):
                defense = int(defense * NON_PROF_SHIELD_DEF_MULT)
        elif armor_tier != "clothing":
            if not can_wear_armor(character.class_name, armor_tier):
                defense = int(defense * NON_PROF_ARMOR_DEF_MULT)

        total += defense
    return total


def calc_equipment_magic_resist(character):
    """Total magic resistance from equipment."""
    if not hasattr(character, "equipment") or not character.equipment:
        return 0
    total = 0
    for slot, item in character.equipment.items():
        if item is not None:
            total += item.get("magic_resist", 0)
    return total


def calc_equipment_speed(character):
    """Total speed modifier from equipment."""
    if not hasattr(character, "equipment") or not character.equipment:
        return 0
    total = 0
    for slot, item in character.equipment.items():
        if item is None:
            continue
        total += item.get("speed_mod", 0)
        # Non-proficient armor speed penalty
        armor_tier = item.get("armor_tier", "clothing")
        if armor_tier not in ("clothing", "shield"):
            if not can_wear_armor(character.class_name, armor_tier):
                total += NON_PROF_ARMOR_SPEED
    return total


def calc_equipment_stat_bonuses(character):
    """Get total stat bonuses from all equipment. Returns dict."""
    bonuses = {}
    if not hasattr(character, "equipment") or not character.equipment:
        return bonuses
    for slot, item in character.equipment.items():
        if item is None:
            continue
        for stat, val in item.get("stat_bonuses", {}).items():
            bonuses[stat] = bonuses.get(stat, 0) + val
    return bonuses
