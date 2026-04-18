"""
Realm of Shadows — Equipment System

Equipment slots per character:
  Weapon     — one weapon (or unarmed)
  Off-hand   — shield or second light weapon (future: dual wield)
  Head       — helmet or Ki Stone
  Body       — armor (clothing/light/medium/heavy)
  Hands      — gloves/gauntlets
  Feet       — boots
  Crown      — ornament, ion stone, circlet (headwear adornment)
  Neck       — necklace, amulet, holy symbol
  Ring1/2/3  — rings (three slots; wands/rods/orbs also usable in off_hand)

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

SLOT_ORDER = ["weapon", "off_hand", "head", "crown", "body", "hands", "feet", "neck", "ring1", "ring2", "ring3"]

SLOT_NAMES = {
    "weapon":   "Weapon",
    "off_hand": "Off-Hand",
    "head":     "Head",
    "crown":    "Crown",
    "body":     "Body",
    "hands":    "Hands",
    "feet":     "Feet",
    "neck":     "Neck",
    "ring1":    "Ring 1",
    "ring2":    "Ring 2",
    "ring3":    "Ring 3",
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
    # ── Base classes ────────────────────────────────────────────────────────
    "Fighter":      "heavy",
    "Cleric":       "heavy",
    "Ranger":       "medium",
    "Thief":        "light",
    "Monk":         "clothing",
    "Mage":         "clothing",
    # ── Advanced classes ─────────────────────────────────────────────────────
    "Paladin":      "heavy",    # Fighter+Cleric
    "Spellblade":   "medium",   # Fighter+Mage
    "Warder":       "light",    # Fighter+Thief
    "Duskblade":    "medium",   # Fighter+Ranger
    "Guardian":     "heavy",    # Fighter+Monk
    "Witch":        "clothing", # Mage+Cleric
    "Necromancer":  "clothing", # Mage+Thief
    "Druid":        "light",    # Mage+Ranger
    "Mystic":       "clothing", # Mage+Monk
    "Warden":       "light",    # Cleric+Ranger
    "Inquisitor":   "light",    # Cleric+Thief
    "Templar":      "heavy",    # Cleric+Monk
    "Assassin":     "light",    # Ranger+Thief
    "Shaman":       "light",    # Ranger+Monk
    # ── Apex classes ─────────────────────────────────────────────────────────
    "Archmage":     "clothing",
    "High Priest":  "medium",
    "Shadow Master":"light",
    "Beastlord":    "medium",
    # ── Other classes ─────────────────────────────────────────────────────────
    "Knight":       "heavy",
    "Strider":      "medium",
    "Phantom":      "light",
    "Ascetic":      "clothing",
    "Warder":       "light",
    # Legacy names kept for backwards compat
    "Battlemage":   "light",
    "Spellthief":   "light",
    "Sage":         "clothing",
    "Warlock":      "light",
    "Ki Master":    "clothing",
    "Merchant":     "medium",
}

# Classes that can use shields
SHIELD_CLASSES = {
    "Fighter", "Cleric", "Paladin", "Knight", "Templar",  # heavy-armor types
    "Guardian", "Warden",                                   # monk/ranger hybrids
}

# Classes that can use focus items (wands, rods, orbs) as weapon or off-hand
FOCUS_CLASSES = {
    "Mage", "Cleric",                          # base casters
    "Spellblade", "Witch", "Necromancer",      # mage hybrids
    "Druid", "Mystic", "Warden",               # nature/monk casters
    "Inquisitor", "Templar",                   # cleric hybrids
    "Archmage", "High Priest",                 # apex casters
    "Phantom",                                 # arcane rogue
    # Legacy names
    "Warder", "Sage", "Warlock", "Battlemage",
}

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

def can_use_focus(class_name):
    return class_name in FOCUS_CLASSES


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


    # ═══════════════════════════════════════════════════════════════
    #  EXPANDED ARMOR — Body
    # ═══════════════════════════════════════════════════════════════

    # ── Clothing tier ──
    "Silk Robes": {
        "name": "Silk Robes", "slot": "body", "armor_tier": "clothing",
        "defense": 2, "magic_resist": 4, "speed_mod": 1,
        "stat_bonuses": {"INT": 1, "WIS": 1}, "rarity": "uncommon", "value": 45,
        "description": "Fine silk that shimmers with subtle enchantment. +1 INT, +1 WIS.",
    },
    "Arcane Vestments": {
        "name": "Arcane Vestments", "slot": "body", "armor_tier": "clothing",
        "defense": 3, "magic_resist": 8, "speed_mod": 1,
        "stat_bonuses": {"INT": 2, "WIS": 1}, "rarity": "rare", "value": 140,
        "description": "Robes inscribed with power-channeling runes. +2 INT, +1 WIS.",
    },
    "Blessed Vestments": {
        "name": "Blessed Vestments", "slot": "body", "armor_tier": "clothing",
        "defense": 3, "magic_resist": 6, "speed_mod": 0,
        "stat_bonuses": {"PIE": 2, "WIS": 1}, "rarity": "rare", "value": 130,
        "description": "Temple-blessed robes worn during high rites. +2 PIE, +1 WIS.",
    },
    "Shadowweave Cloak": {
        "name": "Shadowweave Cloak", "slot": "body", "armor_tier": "clothing",
        "defense": 2, "magic_resist": 3, "speed_mod": 2,
        "stat_bonuses": {"DEX": 2}, "rarity": "rare", "value": 150,
        "description": "A cloak woven from shadow-thread. Fades into darkness. +2 DEX.",
    },
    "Archmagus Robe": {
        "name": "Archmagus Robe", "slot": "body", "armor_tier": "clothing",
        "defense": 4, "magic_resist": 12, "speed_mod": 1,
        "stat_bonuses": {"INT": 3, "WIS": 2}, "rarity": "epic", "value": 450,
        "description": "A robe of absolute magical authority. +3 INT, +2 WIS.",
    },

    # ── Light armor tier ──
    "Padded Leather": {
        "name": "Padded Leather", "slot": "body", "armor_tier": "light",
        "defense": 5, "magic_resist": 0, "speed_mod": 0,
        "stat_bonuses": {}, "rarity": "common", "value": 22,
        "description": "Padded leather with an inner quilted layer.",
    },
    "Reinforced Leather": {
        "name": "Reinforced Leather", "slot": "body", "armor_tier": "light",
        "defense": 7, "magic_resist": 0, "speed_mod": 0,
        "stat_bonuses": {"CON": 1}, "rarity": "uncommon", "value": 65,
        "description": "Leather reinforced with metal plates at the joints. +1 CON.",
    },
    "Ranger's Leathers": {
        "name": "Ranger's Leathers", "slot": "body", "armor_tier": "light",
        "defense": 6, "magic_resist": 1, "speed_mod": 1,
        "stat_bonuses": {"DEX": 1, "WIS": 1}, "rarity": "uncommon", "value": 75,
        "description": "Light, flexible leather suited to forest scouts. +1 DEX, +1 WIS.",
    },
    "Assassin's Leathers": {
        "name": "Assassin's Leathers", "slot": "body", "armor_tier": "light",
        "defense": 7, "magic_resist": 2, "speed_mod": 2,
        "stat_bonuses": {"DEX": 2}, "rarity": "rare", "value": 160,
        "description": "Supple black leather worn by guild assassins. +2 DEX.",
    },
    "Elven Chainmail": {
        "name": "Elven Chainmail", "slot": "body", "armor_tier": "light",
        "defense": 9, "magic_resist": 3, "speed_mod": 1,
        "stat_bonuses": {"DEX": 1, "INT": 1}, "rarity": "epic", "value": 420,
        "description": "Elvish ringmail — light as cloth, strong as steel. +1 DEX, +1 INT.",
    },

    # ── Medium armor tier ──
    "Chainmail": {
        "name": "Chainmail", "slot": "body", "armor_tier": "medium",
        "defense": 11, "magic_resist": 0, "speed_mod": -1,
        "stat_bonuses": {}, "rarity": "common", "value": 70,
        "description": "A full shirt of interlocking rings.",
    },
    "Half-Plate": {
        "name": "Half-Plate", "slot": "body", "armor_tier": "medium",
        "defense": 14, "magic_resist": 0, "speed_mod": -1,
        "stat_bonuses": {"CON": 1}, "rarity": "uncommon", "value": 130,
        "description": "Plate covering the torso with chainmail at the joins. +1 CON.",
    },
    "Battle Armour": {
        "name": "Battle Armour", "slot": "body", "armor_tier": "medium",
        "defense": 13, "magic_resist": 1, "speed_mod": -1,
        "stat_bonuses": {"STR": 1, "CON": 1}, "rarity": "rare", "value": 200,
        "description": "Seasoned armour with many campaign scars. +1 STR, +1 CON.",
    },

    # ── Heavy armor tier ──
    "Plate Armour": {
        "name": "Plate Armour", "slot": "body", "armor_tier": "heavy",
        "defense": 18, "magic_resist": 0, "speed_mod": -3,
        "stat_bonuses": {"CON": 1}, "rarity": "uncommon", "value": 200,
        "description": "A full suit of articulated plate. +1 CON.",
    },
    "Knight's Plate": {
        "name": "Knight's Plate", "slot": "body", "armor_tier": "heavy",
        "defense": 22, "magic_resist": 2, "speed_mod": -3,
        "stat_bonuses": {"STR": 1, "CON": 2}, "rarity": "rare", "value": 380,
        "description": "Armour forged for a veteran knight. Blessed at the forge. +1 STR, +2 CON.",
    },
    "Dragonscale Armour": {
        "name": "Dragonscale Armour", "slot": "body", "armor_tier": "heavy",
        "defense": 26, "magic_resist": 8, "speed_mod": -2,
        "stat_bonuses": {"CON": 2, "STR": 1}, "rarity": "epic", "value": 600,
        "description": "Armour of true dragon scales. Fire-resistant and terrifying. +2 CON, +1 STR.",
    },
    "Mithral Plate": {
        "name": "Mithral Plate", "slot": "body", "armor_tier": "heavy",
        "defense": 24, "magic_resist": 5, "speed_mod": -1,
        "stat_bonuses": {"DEX": 1, "CON": 2}, "rarity": "epic", "value": 650,
        "description": "Mithral plate — lighter than iron, stronger than steel. +1 DEX, +2 CON.",
    },

    # ═══════════════════════════════════════════════════════════════
    #  EXPANDED ARMOR — Head
    # ═══════════════════════════════════════════════════════════════

    # ── Cloth / Mage head ──
    "Witch's Hat": {
        "name": "Witch's Hat", "slot": "head", "armor_tier": "clothing",
        "defense": 0, "magic_resist": 3, "speed_mod": 0,
        "stat_bonuses": {"INT": 1, "WIS": 1}, "rarity": "uncommon", "value": 40,
        "description": "A peaked hat that focuses arcane thought. +1 INT, +1 WIS.",
    },
    "Mage's Cowl": {
        "name": "Mage's Cowl", "slot": "head", "armor_tier": "clothing",
        "defense": 0, "magic_resist": 5, "speed_mod": 0,
        "stat_bonuses": {"INT": 2}, "rarity": "rare", "value": 110,
        "description": "A cowl woven with spell-amplifying thread. +2 INT.",
    },
    "Monk's Hood": {
        "name": "Monk's Hood", "slot": "head", "armor_tier": "clothing",
        "defense": 0, "magic_resist": 2, "speed_mod": 1,
        "stat_bonuses": {"WIS": 2}, "rarity": "uncommon", "value": 38,
        "description": "A meditative hood that aids Ki focus. +2 WIS.",
    },
    "High Priest's Mitre": {
        "name": "High Priest's Mitre", "slot": "head", "armor_tier": "clothing",
        "defense": 0, "magic_resist": 6, "speed_mod": 0,
        "stat_bonuses": {"PIE": 3, "WIS": 1}, "rarity": "epic", "value": 360,
        "description": "A towering mitre of divine office. +3 PIE, +1 WIS.",
    },

    # ── Light head ──
    "Scout's Cap": {
        "name": "Scout's Cap", "slot": "head", "armor_tier": "light",
        "defense": 1, "magic_resist": 0, "speed_mod": 1,
        "stat_bonuses": {"DEX": 1}, "rarity": "common", "value": 10,
        "description": "A light leather cap with a wide brim. +1 DEX.",
    },
    "Leather Hood": {
        "name": "Leather Hood", "slot": "head", "armor_tier": "light",
        "defense": 2, "magic_resist": 0, "speed_mod": 0,
        "stat_bonuses": {"DEX": 1}, "rarity": "common", "value": 12,
        "description": "A hooded leather coif that conceals the face. +1 DEX.",
    },
    "Shadow Hood": {
        "name": "Shadow Hood", "slot": "head", "armor_tier": "light",
        "defense": 2, "magic_resist": 2, "speed_mod": 1,
        "stat_bonuses": {"DEX": 2}, "rarity": "rare", "value": 130,
        "description": "A hood of shadow-dyed leather. The wearer seems to fade. +2 DEX.",
    },

    # ── Medium head ──
    "Chain Coif": {
        "name": "Chain Coif", "slot": "head", "armor_tier": "medium",
        "defense": 4, "magic_resist": 0, "speed_mod": 0,
        "stat_bonuses": {}, "rarity": "common", "value": 30,
        "description": "A head covering of chainmail. Deflects glancing blows.",
    },
    "Visored Helm": {
        "name": "Visored Helm", "slot": "head", "armor_tier": "medium",
        "defense": 5, "magic_resist": 0, "speed_mod": 0,
        "stat_bonuses": {"CON": 1}, "rarity": "uncommon", "value": 65,
        "description": "A medium helm with a pivoting visor. +1 CON.",
    },
    "War Helm": {
        "name": "War Helm", "slot": "head", "armor_tier": "medium",
        "defense": 6, "magic_resist": 0, "speed_mod": 0,
        "stat_bonuses": {"STR": 1, "CON": 1}, "rarity": "rare", "value": 140,
        "description": "A battered campaign helm worn by veterans. +1 STR, +1 CON.",
    },

    # ── Heavy head ──
    "Great Helm": {
        "name": "Great Helm", "slot": "head", "armor_tier": "heavy",
        "defense": 8, "magic_resist": 0, "speed_mod": -1,
        "stat_bonuses": {"CON": 1}, "rarity": "uncommon", "value": 80,
        "description": "A fully encasing helm. Excellent protection, limited vision. +1 CON.",
    },
    "Knight's Helm": {
        "name": "Knight's Helm", "slot": "head", "armor_tier": "heavy",
        "defense": 10, "magic_resist": 2, "speed_mod": -1,
        "stat_bonuses": {"CON": 2}, "rarity": "rare", "value": 200,
        "description": "A crested knight's helm of finest plate. +2 CON.",
    },
    "Dragon Helm": {
        "name": "Dragon Helm", "slot": "head", "armor_tier": "heavy",
        "defense": 13, "magic_resist": 5, "speed_mod": -1,
        "stat_bonuses": {"CON": 2, "STR": 1}, "rarity": "epic", "value": 420,
        "description": "A helm crowned with dragon-bone horns. Inspires fear. +2 CON, +1 STR.",
    },

    # ═══════════════════════════════════════════════════════════════
    #  EXPANDED ARMOR — Hands
    # ═══════════════════════════════════════════════════════════════

    "Silk Gloves": {
        "name": "Silk Gloves", "slot": "hands", "armor_tier": "clothing",
        "defense": 0, "magic_resist": 2, "speed_mod": 0,
        "stat_bonuses": {"INT": 1}, "rarity": "uncommon", "value": 30,
        "description": "Silk gloves threaded with arcane sigils. +1 INT.",
    },
    "Padded Gloves": {
        "name": "Padded Gloves", "slot": "hands", "armor_tier": "light",
        "defense": 1, "magic_resist": 0, "speed_mod": 0,
        "stat_bonuses": {}, "rarity": "common", "value": 8,
        "description": "Simple padded gloves. Protect the knuckles.",
    },
    "Archer's Glove": {
        "name": "Archer's Glove", "slot": "hands", "armor_tier": "light",
        "defense": 1, "magic_resist": 0, "speed_mod": 0,
        "stat_bonuses": {"DEX": 2}, "rarity": "uncommon", "value": 50,
        "description": "A single bracer-glove protecting the draw hand. +2 DEX.",
    },
    "Brawler's Wraps": {
        "name": "Brawler's Wraps", "slot": "hands", "armor_tier": "light",
        "defense": 2, "magic_resist": 0, "speed_mod": 0,
        "stat_bonuses": {"STR": 1, "CON": 1}, "rarity": "uncommon", "value": 55,
        "description": "Tight wraps around the knuckles and wrists. +1 STR, +1 CON.",
    },
    "Chain Gauntlets": {
        "name": "Chain Gauntlets", "slot": "hands", "armor_tier": "medium",
        "defense": 3, "magic_resist": 0, "speed_mod": 0,
        "stat_bonuses": {"CON": 1}, "rarity": "uncommon", "value": 60,
        "description": "Chainmail gloves with riveted knuckle-plates. +1 CON.",
    },
    "Mithral Gauntlets": {
        "name": "Mithral Gauntlets", "slot": "hands", "armor_tier": "heavy",
        "defense": 5, "magic_resist": 3, "speed_mod": 0,
        "stat_bonuses": {"STR": 2, "DEX": 1}, "rarity": "epic", "value": 380,
        "description": "Gauntlets of true mithral. Grip like iron, light as air. +2 STR, +1 DEX.",
    },
    "Ki-Infused Wraps": {
        "name": "Ki-Infused Wraps", "slot": "hands", "armor_tier": "clothing",
        "defense": 0, "magic_resist": 3, "speed_mod": 1,
        "stat_bonuses": {"WIS": 2, "DEX": 1}, "rarity": "rare", "value": 160,
        "description": "Wraps infused with dormant Ki energy. +2 WIS, +1 DEX.",
    },

    # ═══════════════════════════════════════════════════════════════
    #  EXPANDED ARMOR — Feet
    # ═══════════════════════════════════════════════════════════════

    "Soft Shoes": {
        "name": "Soft Shoes", "slot": "feet", "armor_tier": "clothing",
        "defense": 0, "magic_resist": 0, "speed_mod": 1,
        "stat_bonuses": {"DEX": 1}, "rarity": "common", "value": 7,
        "description": "Silent-soled cloth shoes. +1 DEX.",
    },
    "Pilgrim's Boots": {
        "name": "Pilgrim's Boots", "slot": "feet", "armor_tier": "light",
        "defense": 1, "magic_resist": 0, "speed_mod": 1,
        "stat_bonuses": {"CON": 1}, "rarity": "common", "value": 12,
        "description": "Well-worn boots of a long-road traveller. +1 CON.",
    },
    "Scout's Boots": {
        "name": "Scout's Boots", "slot": "feet", "armor_tier": "light",
        "defense": 2, "magic_resist": 0, "speed_mod": 2,
        "stat_bonuses": {"DEX": 2}, "rarity": "uncommon", "value": 70,
        "description": "Soft-soled boots with a reinforced toe. Silent movement. +2 DEX.",
    },
    "Ranger's Treads": {
        "name": "Ranger's Treads", "slot": "feet", "armor_tier": "light",
        "defense": 2, "magic_resist": 1, "speed_mod": 1,
        "stat_bonuses": {"DEX": 1, "WIS": 1}, "rarity": "uncommon", "value": 75,
        "description": "Boots made for rough terrain. Treat difficult ground as open. +1 DEX, +1 WIS.",
    },
    "Heavy Boots": {
        "name": "Heavy Boots", "slot": "feet", "armor_tier": "medium",
        "defense": 4, "magic_resist": 0, "speed_mod": -1,
        "stat_bonuses": {"STR": 1}, "rarity": "common", "value": 25,
        "description": "Iron-capped work boots that double as weapons. +1 STR.",
    },
    "Steel Sabatons": {
        "name": "Steel Sabatons", "slot": "feet", "armor_tier": "heavy",
        "defense": 6, "magic_resist": 0, "speed_mod": -1,
        "stat_bonuses": {"CON": 1, "STR": 1}, "rarity": "uncommon", "value": 90,
        "description": "Full plate foot armour. Stomps with authority. +1 CON, +1 STR.",
    },
    "Mithral Boots": {
        "name": "Mithral Boots", "slot": "feet", "armor_tier": "heavy",
        "defense": 5, "magic_resist": 2, "speed_mod": 1,
        "stat_bonuses": {"DEX": 1, "CON": 1}, "rarity": "epic", "value": 340,
        "description": "Mithral sabatons — heavy-duty without the weight penalty. +1 DEX, +1 CON.",
    },

    # ═══════════════════════════════════════════════════════════════
    #  EXPANDED SHIELDS
    # ═══════════════════════════════════════════════════════════════

    "Buckler": {
        "name": "Buckler", "slot": "off_hand", "armor_tier": "shield",
        "defense": 2, "magic_resist": 0, "speed_mod": 1,
        "stat_bonuses": {"DEX": 1}, "rarity": "common", "value": 15,
        "description": "A small round shield worn on the fist. Fast parrying. +1 DEX.",
    },
    "Heater Shield": {
        "name": "Heater Shield", "slot": "off_hand", "armor_tier": "shield",
        "defense": 6, "magic_resist": 1, "speed_mod": 0,
        "stat_bonuses": {"CON": 1}, "rarity": "uncommon", "value": 55,
        "description": "A triangular knight's shield bearing a blazon. +1 CON.",
    },
    "Kite Shield": {
        "name": "Kite Shield", "slot": "off_hand", "armor_tier": "shield",
        "defense": 9, "magic_resist": 2, "speed_mod": -1,
        "stat_bonuses": {"CON": 2}, "rarity": "rare", "value": 130,
        "description": "A large kite-shaped shield that covers the full torso. +2 CON.",
    },
    "Warden's Shield": {
        "name": "Warden's Shield", "slot": "off_hand", "armor_tier": "shield",
        "defense": 11, "magic_resist": 4, "speed_mod": -1,
        "stat_bonuses": {"CON": 2, "STR": 1}, "rarity": "epic", "value": 350,
        "description": "A shield etched with old Warden ward-runes. Resists shadow. +2 CON, +1 STR.",
    },

    # ═══════════════════════════════════════════════════════════════
    #  EXPANDED CROWN (Ion Stones and Circlets)
    # ═══════════════════════════════════════════════════════════════

    "Jade Circlet": {
        "name": "Jade Circlet", "slot": "crown", "subtype": "circlet",
        "armor_tier": "clothing", "defense": 0, "magic_resist": 3, "speed_mod": 0,
        "stat_bonuses": {"WIS": 2}, "rarity": "uncommon", "value": 65,
        "description": "A circlet of carved jade that calms the mind. +2 WIS.",
    },
    "Golden Diadem": {
        "name": "Golden Diadem", "slot": "crown", "subtype": "crown",
        "armor_tier": "clothing", "defense": 0, "magic_resist": 4, "speed_mod": 0,
        "stat_bonuses": {"PIE": 2, "INT": 1}, "rarity": "rare", "value": 200,
        "description": "A diadem of hammered gold set with divine opals. +2 PIE, +1 INT.",
    },
    "Moonstone Circlet": {
        "name": "Moonstone Circlet", "slot": "crown", "subtype": "circlet",
        "armor_tier": "clothing", "defense": 0, "magic_resist": 5, "speed_mod": 0,
        "stat_bonuses": {"INT": 2, "WIS": 1}, "rarity": "rare", "value": 210,
        "description": "A circlet set with a glowing moonstone. Sharpens the arcane mind. +2 INT, +1 WIS.",
    },
    "Amber Ion Stone": {
        "name": "Amber Ion Stone", "slot": "crown", "subtype": "ion stone",
        "armor_tier": "clothing", "defense": 0, "magic_resist": 4, "speed_mod": 0,
        "stat_bonuses": {"STR": 2}, "rarity": "rare", "value": 180,
        "description": "An amber stone that orbits the head, radiating strength. +2 STR.",
    },
    "Sapphire Ion Stone": {
        "name": "Sapphire Ion Stone", "slot": "crown", "subtype": "ion stone",
        "armor_tier": "clothing", "defense": 0, "magic_resist": 5, "speed_mod": 0,
        "stat_bonuses": {"INT": 2}, "rarity": "rare", "value": 200,
        "description": "A sapphire ion stone that resonates with arcane thought. +2 INT.",
    },
    "Ruby Ion Stone": {
        "name": "Ruby Ion Stone", "slot": "crown", "subtype": "ion stone",
        "armor_tier": "clothing", "defense": 0, "magic_resist": 5, "speed_mod": 0,
        "stat_bonuses": {"PIE": 2}, "rarity": "rare", "value": 200,
        "description": "A ruby ion stone infused with divine warmth. +2 PIE.",
    },

    # ═══════════════════════════════════════════════════════════════
    #  NECK SLOT ITEMS (Amulets, Necklaces, Pendants)
    # ═══════════════════════════════════════════════════════════════

    "Copper Chain": {
        "name": "Copper Chain", "slot": "neck", "subtype": "necklace",
        "armor_tier": "clothing", "defense": 0, "magic_resist": 1, "speed_mod": 0,
        "stat_bonuses": {"CON": 1}, "rarity": "common", "value": 18,
        "description": "A plain copper chain. Nothing fancy, but solid. +1 CON.",
    },
    "Hunter's Totem": {
        "name": "Hunter's Totem", "slot": "neck", "subtype": "pendant",
        "armor_tier": "clothing", "defense": 0, "magic_resist": 1, "speed_mod": 0,
        "stat_bonuses": {"DEX": 1, "WIS": 1}, "rarity": "common", "value": 22,
        "description": "A carved wooden pendant bearing a hunting beast. +1 DEX, +1 WIS.",
    },
    "Necklace of Fortitude": {
        "name": "Necklace of Fortitude", "slot": "neck", "subtype": "necklace",
        "armor_tier": "clothing", "defense": 0, "magic_resist": 2, "speed_mod": 0,
        "stat_bonuses": {"CON": 2, "STR": 1}, "rarity": "uncommon", "value": 75,
        "description": "A heavy iron chain with a bear-claw clasp. +2 CON, +1 STR.",
    },
    "Scholar's Medallion": {
        "name": "Scholar's Medallion", "slot": "neck", "subtype": "amulet",
        "armor_tier": "clothing", "defense": 0, "magic_resist": 3, "speed_mod": 0,
        "stat_bonuses": {"INT": 2, "WIS": 1}, "rarity": "uncommon", "value": 80,
        "description": "A bronze medallion engraved with an open tome. +2 INT, +1 WIS.",
    },
    "Amulet of the Warden": {
        "name": "Amulet of the Warden", "slot": "neck", "subtype": "amulet",
        "armor_tier": "clothing", "defense": 2, "magic_resist": 4, "speed_mod": 0,
        "stat_bonuses": {"WIS": 2, "CON": 1}, "rarity": "rare", "value": 160,
        "description": "An amulet bearing the Warden crest. Resists shadow. +2 WIS, +1 CON.",
    },
    "Shadowheart Pendant": {
        "name": "Shadowheart Pendant", "slot": "neck", "subtype": "pendant",
        "armor_tier": "clothing", "defense": 0, "magic_resist": 5, "speed_mod": 1,
        "stat_bonuses": {"DEX": 2, "INT": 1}, "rarity": "rare", "value": 170,
        "description": "A black obsidian pendant carved with a shadow-rune. +2 DEX, +1 INT.",
    },
    "Holy Symbol of Piety": {
        "name": "Holy Symbol of Piety", "slot": "neck", "subtype": "holy symbol",
        "armor_tier": "clothing", "defense": 0, "magic_resist": 5, "speed_mod": 0,
        "stat_bonuses": {"PIE": 3, "WIS": 1}, "rarity": "rare", "value": 175,
        "description": "A polished divine symbol worn close to the heart. +3 PIE, +1 WIS.",
    },
    "Dragon Fang Necklace": {
        "name": "Dragon Fang Necklace", "slot": "neck", "subtype": "necklace",
        "armor_tier": "clothing", "defense": 0, "magic_resist": 6, "speed_mod": 0,
        "stat_bonuses": {"STR": 2, "CON": 2}, "rarity": "epic", "value": 400,
        "description": "A necklace strung with true dragon fangs. +2 STR, +2 CON.",
    },
    "Archmage's Focus Chain": {
        "name": "Archmage's Focus Chain", "slot": "neck", "subtype": "amulet",
        "armor_tier": "clothing", "defense": 0, "magic_resist": 8, "speed_mod": 0,
        "stat_bonuses": {"INT": 3, "WIS": 2}, "rarity": "epic", "value": 480,
        "description": "A chain of linked focus-crystals. Amplifies all spells. +3 INT, +2 WIS.",
    },

    # ── Focus Items (Wand / Rod / Orb — weapon or off_hand) ──

    "Apprentice Wand": {
        "name": "Apprentice Wand", "type": "weapon", "slot": "weapon",
        "subtype": "Wand", "rarity": "common",
        "damage": 12, "damage_stat": {"INT": 0.35},
        "phys_type": "arcane", "range": "ranged", "is_focus": True,
        "speed_mod": 0, "stat_bonuses": {"INT": 1},
        "identify_difficulty": 1,
        "unidentified_name": "Plain Wand", "unidentified_desc": "A slender magical wand.",
        "appraised_name": "Apprentice Wand",
        "material_desc": "Ashwood tipped with a small crystal.",
        "magic_desc": "Channels arcane energy into ranged bolts.",
        "estimated_value": 40,
        "description": "A basic wand for trainee mages. Fires arcane bolts.",
        "identified": True,
    },
    "Battle Rod": {
        "name": "Battle Rod", "type": "weapon", "slot": "weapon",
        "subtype": "Rod", "rarity": "uncommon",
        "damage": 18, "damage_stat": {"INT": 0.30, "STR": 0.10},
        "phys_type": "blunt", "range": "melee", "is_focus": True,
        "speed_mod": 0, "stat_bonuses": {"INT": 2},
        "identify_difficulty": 2,
        "unidentified_name": "Metal Rod", "unidentified_desc": "A heavy metal rod with runes.",
        "appraised_name": "Battle Rod",
        "material_desc": "Iron shaft inscribed with combat sigils.",
        "magic_desc": "Enhances INT and can be used in melee or as focus.",
        "estimated_value": 90,
        "description": "An iron rod infused with battle magic. Viable in melee.",
        "identified": False,
    },
    "Thought Orb": {
        "name": "Thought Orb", "type": "weapon", "slot": "off_hand",
        "subtype": "Orb", "rarity": "uncommon",
        "damage": 14, "damage_stat": {"INT": 0.28, "WIS": 0.12},
        "phys_type": "arcane", "range": "ranged", "is_focus": True,
        "speed_mod": 0, "stat_bonuses": {"INT": 1, "WIS": 1},
        "identify_difficulty": 2,
        "unidentified_name": "Crystal Sphere", "unidentified_desc": "A glowing sphere.",
        "appraised_name": "Thought Orb",
        "material_desc": "Polished crystal that resonates with thought.",
        "magic_desc": "Held in the off-hand; amplifies magical attacks.",
        "estimated_value": 80,
        "description": "An off-hand focus orb. Boosts magical damage when held.",
        "identified": False,
    },

    # ── Crown Items (head ornament / ion stone slot) ──
    "Silver Circlet": {
        "name": "Silver Circlet", "type": "armor", "slot": "crown",
        "subtype": "circlet", "armor_tier": "clothing",
        "defense": 0, "magic_resist": 2, "speed_mod": 0,
        "stat_bonuses": {"INT": 1},
        "rarity": "uncommon", "value": 50,
        "description": "A delicate silver band worn above the brow. Aids concentration.",
    },
    "Ion Stone": {
        "name": "Ion Stone", "type": "armor", "slot": "crown",
        "subtype": "ion stone", "armor_tier": "clothing",
        "defense": 0, "magic_resist": 3, "speed_mod": 0,
        "stat_bonuses": {"CON": 1},
        "rarity": "rare", "value": 150,
        "description": "A stone that orbits the wearer's head, radiating protective energy.",
    },

    # ═══════════════════════════════════════════════════════════════
    #  CLASS-SPECIFIC BODY ARMOR
    # ═══════════════════════════════════════════════════════════════

    # ── Monk Gi / Training Wear (clothing — Ki-boosted) ──────────────────────
    "Novice Gi": {
        "name": "Novice Gi", "slot": "body", "armor_tier": "clothing",
        "defense": 3, "magic_resist": 1, "speed_mod": 1,
        "stat_bonuses": {"WIS": 1, "DEX": 1}, "rarity": "common", "value": 20,
        "description": "A simple training uniform. Light and unrestrictive. +1 WIS, +1 DEX.",
    },
    "Temple Gi": {
        "name": "Temple Gi", "slot": "body", "armor_tier": "clothing",
        "defense": 5, "magic_resist": 2, "speed_mod": 1,
        "stat_bonuses": {"WIS": 2, "DEX": 1}, "rarity": "uncommon", "value": 65,
        "description": "A gi woven at the temple, its threads blessed with Ki focus. +2 WIS, +1 DEX.",
    },
    "Master's Gi": {
        "name": "Master's Gi", "slot": "body", "armor_tier": "clothing",
        "defense": 7, "magic_resist": 3, "speed_mod": 1,
        "stat_bonuses": {"WIS": 3, "DEX": 1}, "rarity": "rare", "value": 160,
        "description": "A robe worn by temple masters. Channels Ki through its weave. +3 WIS, +1 DEX.",
    },
    "Grandmaster's Vestments": {
        "name": "Grandmaster's Vestments", "slot": "body", "armor_tier": "clothing",
        "defense": 10, "magic_resist": 5, "speed_mod": 2,
        "stat_bonuses": {"WIS": 4, "DEX": 2, "CON": 1}, "rarity": "epic", "value": 460,
        "description": "Robes of absolute martial mastery. Ki radiates from them. +4 WIS, +2 DEX, +1 CON.",
    },
    "Journeyman's Robe": {
        "name": "Journeyman's Robe", "slot": "body", "armor_tier": "clothing",
        "defense": 3, "magic_resist": 5, "speed_mod": 0,
        "stat_bonuses": {"INT": 1}, "rarity": "uncommon", "value": 55,
        "description": "A robe of a travelling scholar. Warded against magical feedback. +1 INT.",
    },
    "Wizard's Robe": {
        "name": "Wizard's Robe", "slot": "body", "armor_tier": "clothing",
        "defense": 4, "magic_resist": 7, "speed_mod": 0,
        "stat_bonuses": {"INT": 2, "WIS": 1}, "rarity": "rare", "value": 160,
        "description": "A robe of a trained wizard. Woven with power-channeling inscriptions. +2 INT, +1 WIS.",
    },
    "Nightweave Armour": {
        "name": "Nightweave Armour", "slot": "body", "armor_tier": "light",
        "defense": 8, "magic_resist": 2, "speed_mod": 2,
        "stat_bonuses": {"DEX": 2, "INT": 1}, "rarity": "rare", "value": 200,
        "description": "Armour woven from shadow-spider silk. Practically invisible in darkness. +2 DEX, +1 INT.",
    },
    "Phantom Armour": {
        "name": "Phantom Armour", "slot": "body", "armor_tier": "light",
        "defense": 10, "magic_resist": 3, "speed_mod": 3,
        "stat_bonuses": {"DEX": 3, "INT": 1}, "rarity": "epic", "value": 480,
        "description": "Legendary armour worn by the greatest assassins. The wearer moves like a ghost. +3 DEX, +1 INT.",
    },
    "Huntsman's Leathers": {
        "name": "Huntsman's Leathers", "slot": "body", "armor_tier": "light",
        "defense": 8, "magic_resist": 1, "speed_mod": 1,
        "stat_bonuses": {"DEX": 2, "WIS": 2}, "rarity": "rare", "value": 190,
        "description": "Supple leathers worked with woodland herbs. Noiseless in brush. +2 DEX, +2 WIS.",
    },
    "Ancient Bark Armour": {
        "name": "Ancient Bark Armour", "slot": "body", "armor_tier": "medium",
        "defense": 14, "magic_resist": 4, "speed_mod": 0,
        "stat_bonuses": {"WIS": 2, "DEX": 1, "CON": 1}, "rarity": "rare", "value": 260,
        "description": "Armour grown from living bark, blessed by old forest spirits. +2 WIS, +1 DEX, +1 CON.",
    },
    "Warden's Hauberk": {
        "name": "Warden's Hauberk", "slot": "body", "armor_tier": "medium",
        "defense": 16, "magic_resist": 5, "speed_mod": 0,
        "stat_bonuses": {"WIS": 3, "DEX": 2}, "rarity": "epic", "value": 440,
        "description": "A hauberk worn by the old Warden order. Nature and protection entwined. +3 WIS, +2 DEX.",
    },
    "Berserker's Plate": {
        "name": "Berserker's Plate", "slot": "body", "armor_tier": "heavy",
        "defense": 20, "magic_resist": 0, "speed_mod": -2,
        "stat_bonuses": {"STR": 3, "CON": 1}, "rarity": "rare", "value": 340,
        "description": "Thick plate built for attack over defence. +3 STR, +1 CON.",
    },
    "Sentinel's Armour": {
        "name": "Sentinel's Armour", "slot": "body", "armor_tier": "heavy",
        "defense": 28, "magic_resist": 3, "speed_mod": -3,
        "stat_bonuses": {"CON": 3, "STR": 2}, "rarity": "epic", "value": 640,
        "description": "The armour of an unbreakable sentinel. Few weapons find purchase. +3 CON, +2 STR.",
    },
    "Sanctified Chainmail": {
        "name": "Sanctified Chainmail", "slot": "body", "armor_tier": "medium",
        "defense": 12, "magic_resist": 4, "speed_mod": -1,
        "stat_bonuses": {"PIE": 1, "CON": 1}, "rarity": "uncommon", "value": 110,
        "description": "Chainmail blessed at the temple altar. Wards against shadow. +1 PIE, +1 CON.",
    },
    "Holy Plate": {
        "name": "Holy Plate", "slot": "body", "armor_tier": "heavy",
        "defense": 23, "magic_resist": 5, "speed_mod": -3,
        "stat_bonuses": {"PIE": 2, "CON": 1}, "rarity": "rare", "value": 380,
        "description": "Plate armour consecrated in a great cathedral. Shines with inner light. +2 PIE, +1 CON.",
    },
    "Archbishop's Armour": {
        "name": "Archbishop's Armour", "slot": "body", "armor_tier": "heavy",
        "defense": 27, "magic_resist": 8, "speed_mod": -2,
        "stat_bonuses": {"PIE": 3, "WIS": 2}, "rarity": "epic", "value": 600,
        "description": "Ceremonial plate worn only by the highest clergy. +3 PIE, +2 WIS.",
    },
    "Crusader's Plate": {
        "name": "Crusader's Plate", "slot": "body", "armor_tier": "heavy",
        "defense": 22, "magic_resist": 4, "speed_mod": -3,
        "stat_bonuses": {"STR": 2, "PIE": 2}, "rarity": "rare", "value": 370,
        "description": "Plate armour worn by holy warriors on crusade. +2 STR, +2 PIE.",
    },
    "Radiant Armour": {
        "name": "Radiant Armour", "slot": "body", "armor_tier": "heavy",
        "defense": 27, "magic_resist": 6, "speed_mod": -2,
        "stat_bonuses": {"STR": 2, "PIE": 3, "CON": 1}, "rarity": "epic", "value": 620,
        "description": "Armour that glows with divine radiance. Undead recoil from its wearer. +2 STR, +3 PIE, +1 CON.",
    },

    # ═══════════════════════════════════════════════════════════════
    #  CLASS-SPECIFIC HEAD ARMOR
    # ═══════════════════════════════════════════════════════════════

    "Monk's Training Band": {
        "name": "Monk's Training Band", "slot": "head", "armor_tier": "clothing",
        "defense": 0, "magic_resist": 2, "speed_mod": 0,
        "stat_bonuses": {"WIS": 2, "DEX": 1}, "rarity": "uncommon", "value": 35,
        "description": "A cloth band worn across the brow during Ki training. +2 WIS, +1 DEX.",
    },
    "Grandmaster's Crown": {
        "name": "Grandmaster's Crown", "slot": "head", "armor_tier": "clothing",
        "defense": 0, "magic_resist": 5, "speed_mod": 1,
        "stat_bonuses": {"WIS": 3, "DEX": 2}, "rarity": "epic", "value": 380,
        "description": "The headband of a true grandmaster. Ki flows freely through the wearer. +3 WIS, +2 DEX.",
    },
    "Ranger's Feathered Cap": {
        "name": "Ranger's Feathered Cap", "slot": "head", "armor_tier": "light",
        "defense": 1, "magic_resist": 1, "speed_mod": 0,
        "stat_bonuses": {"DEX": 1, "WIS": 1}, "rarity": "common", "value": 14,
        "description": "A wide-brimmed cap with a hawk feather. +1 DEX, +1 WIS.",
    },
    "Druid's Antler Crown": {
        "name": "Druid's Antler Crown", "slot": "head", "armor_tier": "medium",
        "defense": 3, "magic_resist": 4, "speed_mod": 0,
        "stat_bonuses": {"WIS": 2, "CON": 1}, "rarity": "rare", "value": 160,
        "description": "A helm adorned with stag antlers. The old forest remembers its wearer. +2 WIS, +1 CON.",
    },
    "Thief's Shadow Cowl": {
        "name": "Thief's Shadow Cowl", "slot": "head", "armor_tier": "light",
        "defense": 2, "magic_resist": 3, "speed_mod": 1,
        "stat_bonuses": {"DEX": 3}, "rarity": "rare", "value": 155,
        "description": "A cowl that bends shadow around the face. +3 DEX.",
    },
    "Phantom Cowl": {
        "name": "Phantom Cowl", "slot": "head", "armor_tier": "light",
        "defense": 3, "magic_resist": 4, "speed_mod": 1,
        "stat_bonuses": {"DEX": 4}, "rarity": "epic", "value": 360,
        "description": "A legendary hood from the guild vault. The wearer is almost impossible to track. +4 DEX.",
    },
    "Holy Helm": {
        "name": "Holy Helm", "slot": "head", "armor_tier": "heavy",
        "defense": 8, "magic_resist": 4, "speed_mod": -1,
        "stat_bonuses": {"CON": 1, "PIE": 1}, "rarity": "uncommon", "value": 90,
        "description": "A helm blessed at the temple. +1 CON, +1 PIE.",
    },
    "Paladin's Greathelm": {
        "name": "Paladin's Greathelm", "slot": "head", "armor_tier": "heavy",
        "defense": 12, "magic_resist": 6, "speed_mod": -1,
        "stat_bonuses": {"CON": 2, "PIE": 2}, "rarity": "epic", "value": 440,
        "description": "A magnificent helm bearing the sunburst of divine office. +2 CON, +2 PIE.",
    },
    "Arcane Cowl": {
        "name": "Arcane Cowl", "slot": "head", "armor_tier": "clothing",
        "defense": 0, "magic_resist": 6, "speed_mod": 0,
        "stat_bonuses": {"INT": 2, "WIS": 1}, "rarity": "rare", "value": 160,
        "description": "A dark cowl embroidered with sigils of power. +2 INT, +1 WIS.",
    },

    # ═══════════════════════════════════════════════════════════════
    #  CLASS-SPECIFIC HANDS
    # ═══════════════════════════════════════════════════════════════

    "Monk's Iron Knuckles": {
        "name": "Monk's Iron Knuckles", "slot": "hands", "armor_tier": "clothing",
        "defense": 1, "magic_resist": 1, "speed_mod": 0,
        "stat_bonuses": {"WIS": 2, "STR": 1}, "rarity": "rare", "value": 130,
        "description": "Iron knuckle-guards that channel Ki into each strike. +2 WIS, +1 STR.",
    },
    "Arcane Focus Gloves": {
        "name": "Arcane Focus Gloves", "slot": "hands", "armor_tier": "clothing",
        "defense": 0, "magic_resist": 4, "speed_mod": 0,
        "stat_bonuses": {"INT": 2}, "rarity": "rare", "value": 140,
        "description": "Gloves sewn with focus-crystals at the fingertips. Spells channel cleanly. +2 INT.",
    },
    "Ranger's Bracers": {
        "name": "Ranger's Bracers", "slot": "hands", "armor_tier": "light",
        "defense": 2, "magic_resist": 1, "speed_mod": 0,
        "stat_bonuses": {"DEX": 2, "WIS": 1}, "rarity": "uncommon", "value": 60,
        "description": "Vambraces of tooled leather. Protect the draw arm and improve aim. +2 DEX, +1 WIS.",
    },
    "Shadow Wraps": {
        "name": "Shadow Wraps", "slot": "hands", "armor_tier": "clothing",
        "defense": 0, "magic_resist": 2, "speed_mod": 1,
        "stat_bonuses": {"DEX": 3}, "rarity": "rare", "value": 140,
        "description": "Dark silk wraps dyed with shadow essence. +3 DEX.",
    },
    "Holy Gauntlets": {
        "name": "Holy Gauntlets", "slot": "hands", "armor_tier": "heavy",
        "defense": 4, "magic_resist": 3, "speed_mod": 0,
        "stat_bonuses": {"STR": 1, "PIE": 1}, "rarity": "uncommon", "value": 75,
        "description": "Gauntlets blessed in a temple forge. +1 STR, +1 PIE.",
    },
    "Fighter's Iron Fists": {
        "name": "Fighter's Iron Fists", "slot": "hands", "armor_tier": "heavy",
        "defense": 5, "magic_resist": 0, "speed_mod": 0,
        "stat_bonuses": {"STR": 2, "CON": 1}, "rarity": "rare", "value": 140,
        "description": "Reinforced plate gauntlets that add weight to every punch. +2 STR, +1 CON.",
    },
    "Warden's Bracers": {
        "name": "Warden's Bracers", "slot": "hands", "armor_tier": "medium",
        "defense": 3, "magic_resist": 3, "speed_mod": 0,
        "stat_bonuses": {"CON": 1, "WIS": 2}, "rarity": "rare", "value": 145,
        "description": "Bracers engraved with old Warden ward-runes. +1 CON, +2 WIS.",
    },

    # ═══════════════════════════════════════════════════════════════
    #  CLASS-SPECIFIC FEET
    # ═══════════════════════════════════════════════════════════════

    "Monk's Sandals": {
        "name": "Monk's Sandals", "slot": "feet", "armor_tier": "clothing",
        "defense": 0, "magic_resist": 1, "speed_mod": 2,
        "stat_bonuses": {"WIS": 2, "DEX": 1}, "rarity": "uncommon", "value": 42,
        "description": "Straw sandals tied with blessing-cords. Allow Ki to flow through the earth. +2 WIS, +1 DEX.",
    },
    "Temple Sandals": {
        "name": "Temple Sandals", "slot": "feet", "armor_tier": "clothing",
        "defense": 0, "magic_resist": 3, "speed_mod": 2,
        "stat_bonuses": {"WIS": 3, "DEX": 1}, "rarity": "rare", "value": 130,
        "description": "Ceremonial sandals worn during the highest rites. The wearer barely touches the ground. +3 WIS, +1 DEX.",
    },
    "Mage's Slippers": {
        "name": "Mage's Slippers", "slot": "feet", "armor_tier": "clothing",
        "defense": 0, "magic_resist": 2, "speed_mod": 1,
        "stat_bonuses": {"INT": 1}, "rarity": "uncommon", "value": 35,
        "description": "Enchanted slippers that glide silently. +1 INT.",
    },
    "Nature's Step Boots": {
        "name": "Nature's Step Boots", "slot": "feet", "armor_tier": "light",
        "defense": 3, "magic_resist": 2, "speed_mod": 1,
        "stat_bonuses": {"DEX": 2, "WIS": 1}, "rarity": "rare", "value": 160,
        "description": "Boots made from living bark and forest leather. Leave no tracks. +2 DEX, +1 WIS.",
    },
    "Shadow Stalker Boots": {
        "name": "Shadow Stalker Boots", "slot": "feet", "armor_tier": "light",
        "defense": 3, "magic_resist": 3, "speed_mod": 3,
        "stat_bonuses": {"DEX": 3}, "rarity": "epic", "value": 400,
        "description": "Legendary boots worn by the greatest assassins. +3 DEX.",
    },
    "Holy Sabatons": {
        "name": "Holy Sabatons", "slot": "feet", "armor_tier": "heavy",
        "defense": 6, "magic_resist": 2, "speed_mod": 0,
        "stat_bonuses": {"CON": 1, "PIE": 1}, "rarity": "uncommon", "value": 90,
        "description": "Plate sabatons blessed with a prayer of steadfastness. +1 CON, +1 PIE.",
    },
    "Battle Greaves": {
        "name": "Battle Greaves", "slot": "feet", "armor_tier": "heavy",
        "defense": 8, "magic_resist": 0, "speed_mod": -1,
        "stat_bonuses": {"STR": 1, "CON": 2}, "rarity": "rare", "value": 170,
        "description": "Heavy battle greaves that add punishing weight to every kick. +1 STR, +2 CON.",
    },

    # ═══════════════════════════════════════════════════════════════
    #  EXPANDED SHIELDS
    # ═══════════════════════════════════════════════════════════════

    "Holy Shield": {
        "name": "Holy Shield", "slot": "off_hand", "armor_tier": "shield",
        "defense": 7, "magic_resist": 5, "speed_mod": 0,
        "stat_bonuses": {"PIE": 1}, "rarity": "rare", "value": 190,
        "description": "A shield consecrated in a great temple. Effective against shadow. +1 PIE.",
    },
    "Champion's Shield": {
        "name": "Champion's Shield", "slot": "off_hand", "armor_tier": "shield",
        "defense": 10, "magic_resist": 2, "speed_mod": -1,
        "stat_bonuses": {"CON": 2, "STR": 1}, "rarity": "rare", "value": 210,
        "description": "A broad tournament shield of a grand champion. +2 CON, +1 STR.",
    },
    "Knight's Bulwark": {
        "name": "Knight's Bulwark", "slot": "off_hand", "armor_tier": "shield",
        "defense": 13, "magic_resist": 3, "speed_mod": -1,
        "stat_bonuses": {"CON": 3}, "rarity": "epic", "value": 420,
        "description": "A legendary shield passed down through the knightly order. +3 CON.",
    },
    "Warden's Ward": {
        "name": "Warden's Ward", "slot": "off_hand", "armor_tier": "shield",
        "defense": 8, "magic_resist": 8, "speed_mod": 0,
        "stat_bonuses": {"WIS": 2, "CON": 1}, "rarity": "epic", "value": 440,
        "description": "A shield carved from warding-wood. Exceptional magic resistance. +2 WIS, +1 CON.",
    },

    # ═══════════════════════════════════════════════════════════════
    #  EXPANDED CROWN (Ion Stones + Circlets)
    # ═══════════════════════════════════════════════════════════════

    "Emerald Ion Stone": {
        "name": "Emerald Ion Stone", "slot": "crown", "subtype": "ion stone",
        "armor_tier": "clothing", "defense": 0, "magic_resist": 4, "speed_mod": 1,
        "stat_bonuses": {"DEX": 2}, "rarity": "rare", "value": 185,
        "description": "An emerald ion stone orbiting the head, lending nimble grace. +2 DEX.",
    },
    "Topaz Ion Stone": {
        "name": "Topaz Ion Stone", "slot": "crown", "subtype": "ion stone",
        "armor_tier": "clothing", "defense": 0, "magic_resist": 4, "speed_mod": 0,
        "stat_bonuses": {"WIS": 2}, "rarity": "rare", "value": 185,
        "description": "A warm topaz stone that deepens spiritual insight. +2 WIS.",
    },
    "Onyx Ion Stone": {
        "name": "Onyx Ion Stone", "slot": "crown", "subtype": "ion stone",
        "armor_tier": "clothing", "defense": 0, "magic_resist": 6, "speed_mod": 0,
        "stat_bonuses": {"CON": 2}, "rarity": "rare", "value": 190,
        "description": "A black ion stone that absorbs shadow energy. +2 CON.",
    },
    "Monk's Third Eye": {
        "name": "Monk's Third Eye", "slot": "crown", "subtype": "ornament",
        "armor_tier": "clothing", "defense": 0, "magic_resist": 6, "speed_mod": 1,
        "stat_bonuses": {"WIS": 3, "DEX": 1}, "rarity": "epic", "value": 400,
        "description": "A crystal bound to the brow by a silk cord. Heightens Ki awareness. +3 WIS, +1 DEX.",
    },
    "Thief's Mark": {
        "name": "Thief's Mark", "slot": "crown", "subtype": "ornament",
        "armor_tier": "clothing", "defense": 0, "magic_resist": 4, "speed_mod": 2,
        "stat_bonuses": {"DEX": 3}, "rarity": "epic", "value": 390,
        "description": "A dark ornament worn by the guild's finest. Marks one as a master of the craft. +3 DEX.",
    },
    "Ranger's Brow Band": {
        "name": "Ranger's Brow Band", "slot": "crown", "subtype": "circlet",
        "armor_tier": "clothing", "defense": 0, "magic_resist": 2, "speed_mod": 1,
        "stat_bonuses": {"WIS": 1, "DEX": 1}, "rarity": "uncommon", "value": 45,
        "description": "A leather brow band worn by forest scouts. +1 WIS, +1 DEX.",
    },

    # ═══════════════════════════════════════════════════════════════
    #  EXPANDED NECK SLOT (Class-flavoured)
    # ═══════════════════════════════════════════════════════════════

    "Monk's Prayer Beads": {
        "name": "Monk's Prayer Beads", "slot": "neck", "subtype": "necklace",
        "armor_tier": "clothing", "defense": 0, "magic_resist": 3, "speed_mod": 0,
        "stat_bonuses": {"WIS": 2}, "rarity": "uncommon", "value": 55,
        "description": "A loop of carved bone beads used during meditation. +2 WIS.",
    },
    "Ki Master's Chain": {
        "name": "Ki Master's Chain", "slot": "neck", "subtype": "amulet",
        "armor_tier": "clothing", "defense": 0, "magic_resist": 5, "speed_mod": 1,
        "stat_bonuses": {"WIS": 4, "DEX": 2}, "rarity": "epic", "value": 460,
        "description": "A legendary chain worn by the greatest monks. The links pulse with Ki energy. +4 WIS, +2 DEX.",
    },
    "Mage's Spell Focus": {
        "name": "Mage's Spell Focus", "slot": "neck", "subtype": "amulet",
        "armor_tier": "clothing", "defense": 0, "magic_resist": 4, "speed_mod": 0,
        "stat_bonuses": {"INT": 2}, "rarity": "uncommon", "value": 70,
        "description": "A crystal amulet that reduces spell feedback. +2 INT.",
    },
    "Archmage's Pendant": {
        "name": "Archmage's Pendant", "slot": "neck", "subtype": "amulet",
        "armor_tier": "clothing", "defense": 0, "magic_resist": 7, "speed_mod": 0,
        "stat_bonuses": {"INT": 3, "WIS": 2}, "rarity": "epic", "value": 470,
        "description": "The pendant of a true archmage. +3 INT, +2 WIS.",
    },
    "Ranger's Nature Token": {
        "name": "Ranger's Nature Token", "slot": "neck", "subtype": "pendant",
        "armor_tier": "clothing", "defense": 0, "magic_resist": 2, "speed_mod": 0,
        "stat_bonuses": {"DEX": 2, "WIS": 2}, "rarity": "uncommon", "value": 65,
        "description": "A token carved from a tree that survived a Fading event. +2 DEX, +2 WIS.",
    },
    "Assassin's Mark": {
        "name": "Assassin's Mark", "slot": "neck", "subtype": "pendant",
        "armor_tier": "clothing", "defense": 0, "magic_resist": 3, "speed_mod": 1,
        "stat_bonuses": {"DEX": 4}, "rarity": "epic", "value": 450,
        "description": "A pendant marking the wearer as a master assassin. +4 DEX.",
    },
    "Warden's Ward Necklace": {
        "name": "Warden's Ward Necklace", "slot": "neck", "subtype": "amulet",
        "armor_tier": "clothing", "defense": 2, "magic_resist": 5, "speed_mod": 0,
        "stat_bonuses": {"WIS": 3, "CON": 1}, "rarity": "epic", "value": 465,
        "description": "A necklace bearing the last Warden ward-seal. +3 WIS, +1 CON.",
    },
    "Fighter's Trophy Chain": {
        "name": "Fighter's Trophy Chain", "slot": "neck", "subtype": "necklace",
        "armor_tier": "clothing", "defense": 0, "magic_resist": 1, "speed_mod": 0,
        "stat_bonuses": {"STR": 2, "CON": 2}, "rarity": "rare", "value": 165,
        "description": "A chain hung with trophies from past victories. +2 STR, +2 CON.",
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
    subtype = item.get("subtype", "").lower()
    # Legacy "accessory" slot: route by subtype
    if slot == "accessory":
        if subtype in ("amulet", "necklace", "pendant", "holy symbol", "talisman"):
            return "neck"
        if subtype in ("circlet", "crown", "ornament", "ion stone", "diadem"):
            return "crown"
        return "ring1"  # default accessory → ring
    # Legacy explicit accessory slots
    if slot == "accessory1": return "ring1"
    if slot == "accessory2": return "neck"
    return slot


def can_equip(character, item):
    """Check if a character can equip an item. Returns (can_equip, reason)."""
    slot = item.get("slot", "")
    class_name = character.class_name

    # Focus item check (wand, rod, orb) — must come before generic weapon pass
    subtype = item.get("subtype", "")
    if subtype in ("Wand", "Rod", "Orb") or item.get("is_focus"):
        if class_name not in FOCUS_CLASSES:
            return False, f"{class_name} cannot use focus items"
        return True, ""

    # Weapon check — handled by weapon proficiency (already in weapons.py)
    if slot == "weapon":
        return True, ""

    # Shield check
    if slot == "off_hand" and item.get("armor_tier") == "shield":
        if not can_use_shield(class_name):
            return False, f"{class_name} cannot use shields"
        return True, ""

    # (focus check handled above)

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
    if item_slot in ("accessory", "ring1", "ring2", "ring3"):
        # Route to appropriate slot: neck/crown/ring by subtype
        resolved = get_item_slot(item)
        if target_slot in ("ring1", "ring2", "ring3", "neck", "crown"):
            slot = target_slot
        elif resolved in ("neck", "crown"):
            slot = resolved
        elif character.equipment.get("ring1") is None:
            slot = "ring1"
        elif character.equipment.get("ring2") is None:
            slot = "ring2"
        elif character.equipment.get("ring3") is None:
            slot = "ring3"
        else:
            slot = "ring1"  # swap into ring1 by default
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

    # Cursed items cannot be unequipped without Remove Curse
    if item.get("cursed") and not item.get("curse_lifted"):
        name = item.get("name", "item")
        return False, item, f"{name} is cursed and cannot be removed!"

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
    """Get total stat bonuses from all equipment. Returns dict with uppercase stat keys.

    Reads two formats:
      - stat_bonuses: {"STR": 2, "DEX": 1}   (standard armor/weapons)
      - effect:       {"str_bonus": 2, "dex_bonus": 1}  (magic items)
    Also includes active item set bonuses.
    """
    # Map from effect-style lowercase keys to stat abbreviations
    _EFFECT_TO_STAT = {
        "str_bonus": "STR", "dex_bonus": "DEX", "con_bonus": "CON",
        "int_bonus": "INT", "wis_bonus": "WIS", "pie_bonus": "PIE",
    }

    bonuses = {}
    if not hasattr(character, "equipment") or not character.equipment:
        return bonuses
    for slot, item in character.equipment.items():
        if item is None:
            continue
        # Standard format — positive bonuses
        for stat, val in item.get("stat_bonuses", {}).items():
            bonuses[stat] = bonuses.get(stat, 0) + val
        # Cursed items: stat_penalty is the negative side. Previously unread,
        # so cursed items gave their perks with no downside. Now applied as
        # a negative bonus so cursed gear actually costs something.
        # Keys map directly to stats (e.g. "LCK": -5) just like stat_bonuses.
        # Non-stat keys (accuracy_bonus, attack_damage, speed_mod, magic_resist)
        # aren't handled here — they're applied by separate systems that read
        # stat_bonuses directly; see below for those.
        for stat, val in item.get("stat_penalty", {}).items():
            bonuses[stat] = bonuses.get(stat, 0) + val
        # Magic item effect format
        for effect_key, stat in _EFFECT_TO_STAT.items():
            val = item.get("effect", {}).get(effect_key, 0)
            if val:
                bonuses[stat] = bonuses.get(stat, 0) + val

    # Item set bonuses
    try:
        from data.magic_items import calc_set_stat_bonuses
        for stat, val in calc_set_stat_bonuses(character).items():
            bonuses[stat] = bonuses.get(stat, 0) + val
    except ImportError:
        pass

    return bonuses
