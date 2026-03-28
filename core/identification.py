"""
Realm of Shadows — Item Identification System

Two identification paths:
  Arcane Lore (Mage-type) — reveals magical properties, enchantments, stat bonuses
  Appraisal (Thief-type)  — reveals material, quality, crafting tier, value

Characters with access to both can do a Full Identify in one action.

Check formula:
  Arcane Lore:  INT + (level × 2)  vs  difficulty × 10
  Appraisal:    (INT + DEX) / 2 + (level × 2)  vs  difficulty × 8

Costs:
  Arcane Lore:  5 INT-MP (or WIS-MP for Cleric-type identifying divine items)
  Appraisal:    3 DEX-SP
  Full Identify: both costs combined
"""
import random


# ═══════════════════════════════════════════════════════════════
#  MUNDANE ITEM AUTO-IDENTIFICATION
# ═══════════════════════════════════════════════════════════════

# Item types/categories that don't need magical identification
MUNDANE_TYPES = {
    "material", "consumable", "potion", "food", "misc", "junk",
    "pelt", "hide", "bone", "ore", "gem", "trophy", "reagent",
    "herb", "arrow", "bolt",
}

# Item name substrings that indicate mundane items
MUNDANE_KEYWORDS = [
    "pelt", "fang", "ear", "tooth", "hide", "scraps",
    "bone", "skull", "crude", "rusty", "broken", "tattered",
    "herbs", "potion", "pouch", "rations", "torch", "rope",
    "arrows", "bolts", "bandage", "antidote", "coin",
    "bundle", "trophy",
]


def needs_identification(item):
    """Check if an item needs magical identification.
    Mundane items (pelts, common weapons, materials) are auto-identified.
    Only items with magical properties, enchantments, or explicit
    identify_difficulty > 0 need identification."""
    # Already identified
    if item.get("identified"):
        return False

    # Explicitly marked as needing identification
    if item.get("identify_difficulty", 0) > 0:
        return True

    # Has magical properties
    if item.get("enchant_element") or item.get("enchant_bonus"):
        return True
    if item.get("enhance_bonus", 0) > 0:
        return True
    if item.get("cursed"):
        return True
    if item.get("magic_item"):
        return True
    if item.get("rarity") in ("rare", "epic", "legendary"):
        return True

    # Check item type — mundane types auto-identify
    item_type = item.get("type", "").lower()
    if item_type in MUNDANE_TYPES:
        return False

    # Check name for mundane keywords
    item_name = item.get("name", "").lower()
    for kw in MUNDANE_KEYWORDS:
        if kw in item_name:
            return False

    # Default: common/uncommon non-magical items don't need identification
    rarity = item.get("rarity", "common")
    if rarity in ("common", "uncommon") and not item.get("enchant_element"):
        return False

    return True


def auto_identify_mundane(item):
    """Auto-identify items that don't need magical identification."""
    if not needs_identification(item):
        item["identified"] = True
        item["magic_identified"] = True
        item["material_identified"] = True
        return True
    return False

ARCANE_LORE_COST = 5       # MP cost
APPRAISAL_COST = 3         # SP cost
DIVINE_LORE_COST = 4       # PIE-MP cost for religious item identification
RETRY_COST_MULT = 1.5      # each retry on the same item costs 1.5× more

# Difficulty scaling
ARCANE_DIFF_SCALE = 10     # difficulty × this = target number
APPRAISAL_DIFF_SCALE = 8
DIVINE_DIFF_SCALE = 8

# INT threshold: any class can attempt Arcane Lore if INT meets this
INT_IDENTIFY_THRESHOLD = 10

# PIE threshold: any class can attempt Divine Lore if PIE meets this
PIE_DIVINE_THRESHOLD = 10


# ═══════════════════════════════════════════════════════════════
#  CLASS CAPABILITIES
# ═══════════════════════════════════════════════════════════════

# Classes with trained Arcane Lore get bonus to the roll
ARCANE_LORE_TRAINED = {
    # class_name: resource_key used for the cost
    "Mage":        "INT-MP",
    "Cleric":      "PIE-MP",
    "Battlemage":  "INT-MP",
    "Spellthief":  "INT-MP",
    "Sage":        "INT-MP",
    "Warlock":     "INT-MP",
    "Witch":       "INT-MP",
    "Necromancer": "INT-MP",
    "Druid":       "INT-MP",
    "Mystic":      "INT-MP",
    "Spellblade":  "INT-MP",
    "Archmage":    "INT-MP",
    "High Priest": "PIE-MP",
}

# Classes with trained Appraisal get bonus
APPRAISAL_TRAINED = {
    "Thief":      "DEX-SP",
    "Ranger":     "DEX-SP",
    "Assassin":   "DEX-SP",
    "Spellthief": "DEX-SP",
    "Merchant":   "DEX-SP",
    "Shadow Master": "DEX-SP",
}

# Classes with trained Divine Lore
DIVINE_LORE_TRAINED = {
    "Cleric":      "PIE-MP",
    "Paladin":     "PIE-MP",
    "Templar":     "PIE-MP",
    "Inquisitor":  "PIE-MP",
    "Warden":      "PIE-MP",   # Warden hybrid class
    "High Priest": "PIE-MP",
    "Knight":      "PIE-MP",
}

# For untrained classes: which resource to drain for identification attempts
# (falls back to first available MP-type resource)
def _find_mp_resource(combatant):
    """Find the first available MP-type resource, or None."""
    resources = combatant.get("resources", {})
    for rk in ("INT-MP", "PIE-MP", "WIS-MP", "MP"):
        if rk in resources:
            return rk
    return None


# ═══════════════════════════════════════════════════════════════
#  CAPABILITY CHECKS
# ═══════════════════════════════════════════════════════════════

def can_arcane_lore(combatant):
    """Any character with INT >= threshold can attempt Arcane Lore.
    Returns (can_attempt, resource_key, cost, is_trained)."""
    int_val = combatant.get("stats", {}).get("INT", 0)
    cls = combatant.get("class_name", "")
    if int_val < INT_IDENTIFY_THRESHOLD:
        return False, None, 0, False
    is_trained = cls in ARCANE_LORE_TRAINED
    resource_key = ARCANE_LORE_TRAINED.get(cls) or _find_mp_resource(combatant)
    if not resource_key:
        return False, None, 0, False
    current = combatant.get("resources", {}).get(resource_key, 0)
    return current >= ARCANE_LORE_COST, resource_key, ARCANE_LORE_COST, is_trained


def can_appraisal(combatant):
    """Trained Appraisal classes get full access; any character with INT >= threshold
    can attempt a basic material appraisal using their resource pool.
    Returns (can_attempt, resource_key, cost, is_trained)."""
    cls = combatant.get("class_name", "")
    int_val = combatant.get("stats", {}).get("INT", 0)
    is_trained = cls in APPRAISAL_TRAINED
    if not is_trained and int_val < INT_IDENTIFY_THRESHOLD:
        return False, None, 0, False
    resource_key = APPRAISAL_TRAINED.get(cls) or _find_mp_resource(combatant)
    if not resource_key:
        return False, None, 0, False
    current = combatant.get("resources", {}).get(resource_key, 0)
    return current >= APPRAISAL_COST, resource_key, APPRAISAL_COST, is_trained


def can_divine_lore(combatant):
    """Any character with PIE >= threshold can attempt Divine Lore (religious items).
    Returns (can_attempt, resource_key, cost, is_trained)."""
    pie_val = combatant.get("stats", {}).get("PIE", 0)
    cls = combatant.get("class_name", "")
    if pie_val < PIE_DIVINE_THRESHOLD:
        return False, None, 0, False
    is_trained = cls in DIVINE_LORE_TRAINED
    resource_key = DIVINE_LORE_TRAINED.get(cls) or _find_mp_resource(combatant)
    if not resource_key:
        return False, None, 0, False
    current = combatant.get("resources", {}).get(resource_key, 0)
    return current >= DIVINE_LORE_COST, resource_key, DIVINE_LORE_COST, is_trained


def can_full_identify(combatant):
    """Check if character can do both Arcane Lore and Appraisal."""
    can_arc, arc_res, arc_cost, _ = can_arcane_lore(combatant)
    can_app, app_res, app_cost, _ = can_appraisal(combatant)
    return can_arc and can_app, arc_res, arc_cost, app_res, app_cost


def get_identify_options(combatant, item=None):
    """Return list of identification actions available to this character.
    Each entry: (action_name, description, can_afford)"""
    options = []
    is_relic = item and item.get("subtype") in ("relic", "holy_symbol", "divine_focus",
                                                  "sacred_text", "blessed_item")

    can_arc, arc_res, arc_cost, arc_trained = can_arcane_lore(combatant)
    if arc_res:
        label = "Arcane Lore" if arc_trained else "Scrutinize"
        options.append({
            "action": "arcane_lore",
            "name": label,
            "description": f"Reveal magical properties ({arc_cost} {arc_res})"
                           + ("" if arc_trained else " — untrained"),
            "can_afford": can_arc,
            "cost": arc_cost,
            "resource": arc_res,
        })

    can_app, app_res, app_cost, app_trained = can_appraisal(combatant)
    if app_res:
        label = "Appraisal" if app_trained else "Examine"
        options.append({
            "action": "appraisal",
            "name": label,
            "description": f"Reveal material & value ({app_cost} {app_res})"
                           + ("" if app_trained else " — untrained"),
            "can_afford": can_app,
            "cost": app_cost,
            "resource": app_res,
        })

    # Full identify only if character has both capabilities
    if arc_res and app_res:
        can_full = can_arc and can_app
        options.append({
            "action": "full_identify",
            "name": "Full Identify",
            "description": f"Reveal all ({arc_cost} {arc_res} + {app_cost} {app_res})",
            "can_afford": can_full,
            "cost": (arc_cost, app_cost),
            "resource": (arc_res, app_res),
        })

    # Divine Lore for religious items
    if is_relic or (item is None):  # show option if item unknown or is a relic
        can_div, div_res, div_cost, div_trained = can_divine_lore(combatant)
        if div_res:
            label = "Divine Lore" if div_trained else "Sense Divinity"
            options.append({
                "action": "divine_lore",
                "name": label,
                "description": f"Reveal sacred properties ({div_cost} {div_res})"
                               + ("" if div_trained else " — untrained"),
                "can_afford": can_div,
                "cost": div_cost,
                "resource": div_res,
            })

    return options


# ═══════════════════════════════════════════════════════════════
#  IDENTIFICATION ROLLS
# ═══════════════════════════════════════════════════════════════

def roll_arcane_lore(combatant, item, is_trained=False):
    """Attempt Arcane Lore identification.
    Trained classes get a bonus. Higher INT = better chance.
    Returns (success, message)."""
    difficulty = item.get("identify_difficulty", 1)
    target = difficulty * ARCANE_DIFF_SCALE

    int_val = combatant.get("stats", {}).get("INT", 0)
    level = combatant.get("level", 1)
    trained_bonus = 8 if is_trained else 0
    check = int_val + (level * 2) + trained_bonus + random.randint(0, 5)

    if check >= target:
        item["magic_identified"] = True
        return True, f"{combatant['name']} discerns the magical properties."
    else:
        return False, f"{combatant['name']} senses magic but can't discern its nature."


def roll_appraisal(combatant, item, is_trained=False):
    """Attempt Appraisal identification.
    Returns (success, message)."""
    difficulty = item.get("identify_difficulty", 1)
    target = difficulty * APPRAISAL_DIFF_SCALE

    int_val = combatant.get("stats", {}).get("INT", 0)
    dex_val = combatant.get("stats", {}).get("DEX", 0)
    level = combatant.get("level", 1)
    trained_bonus = 6 if is_trained else 0
    check = (int_val + dex_val) // 2 + (level * 2) + trained_bonus + random.randint(0, 5)

    if check >= target:
        item["material_identified"] = True
        return True, f"{combatant['name']} assesses the craftsmanship and value."
    else:
        return False, f"{combatant['name']} can't determine anything unusual about this."


def roll_divine_lore(combatant, item, is_trained=False):
    """Attempt Divine Lore identification (religious/sacred items).
    PIE is the primary stat. Works on relics, holy symbols, sacred texts.
    Returns (success, message)."""
    difficulty = item.get("identify_difficulty", 1)
    target = difficulty * DIVINE_DIFF_SCALE

    pie_val = combatant.get("stats", {}).get("PIE", 0)
    level = combatant.get("level", 1)
    trained_bonus = 8 if is_trained else 0
    check = pie_val + (level * 2) + trained_bonus + random.randint(0, 5)

    if check >= target:
        item["magic_identified"] = True
        item["material_identified"] = True
        item["identified"] = True
        return True, f"{combatant['name']} senses the sacred resonance within."
    else:
        return False, f"{combatant['name']} feels a presence but cannot read its nature."


def attempt_identify(combatant, item, action):
    """Perform an identification attempt. Deducts resources on attempt (hit or miss).
    
    action: 'arcane_lore', 'appraisal', 'full_identify', or 'divine_lore'
    Returns: (results_list, all_succeeded)
      results_list: [(check_name, success, message), ...]
    """
    results = []

    if action in ("arcane_lore", "full_identify"):
        can_arc, arc_res, arc_cost, arc_trained = can_arcane_lore(combatant)
        if can_arc:
            combatant["resources"][arc_res] -= arc_cost
            success, msg = roll_arcane_lore(combatant, item, arc_trained)
            results.append(("Arcane Lore", success, msg))
        else:
            results.append(("Arcane Lore", False, "Not enough resources."))

    if action in ("appraisal", "full_identify"):
        can_app, app_res, app_cost, app_trained = can_appraisal(combatant)
        if can_app:
            combatant["resources"][app_res] -= app_cost
            success, msg = roll_appraisal(combatant, item, app_trained)
            results.append(("Appraisal", success, msg))
        else:
            results.append(("Appraisal", False, "Not enough resources."))

    if action == "divine_lore":
        can_div, div_res, div_cost, div_trained = can_divine_lore(combatant)
        if can_div:
            combatant["resources"][div_res] -= div_cost
            success, msg = roll_divine_lore(combatant, item, div_trained)
            results.append(("Divine Lore", success, msg))
        else:
            results.append(("Divine Lore", False, "Not enough resources."))

    # Check if fully identified
    if item.get("magic_identified") and item.get("material_identified"):
        item["identified"] = True

    all_ok = all(r[1] for r in results)
    return results, all_ok


# ═══════════════════════════════════════════════════════════════
#  ITEM DISPLAY HELPERS
# ═══════════════════════════════════════════════════════════════

def get_item_display_name(item):
    """Return the appropriate display name based on identification state."""
    if item.get("identified"):
        base = item.get("name", "Unknown Item")
        # Append charge status for focus weapons
        try:
            from core.focus_charges import is_focus, get_charge_label
            if is_focus(item):
                base += get_charge_label(item)
        except Exception:
            pass
        return base
    elif item.get("magic_identified") and not item.get("material_identified"):
        # Know the magic, not the material — show enchantment hint
        base = item.get("unidentified_name", f"??? {item.get('type', 'Item')}")
        enchant = ""
        if item.get("element"):
            enchant = f" ({item['element'].title()} enchanted)"
        elif item.get("enhance_bonus"):
            enchant = f" (+{item['enhance_bonus']})"
        return f"{base}{enchant}"
    elif item.get("material_identified") and not item.get("magic_identified"):
        # Know the material, not the magic
        return item.get("appraised_name", item.get("unidentified_name",
                        f"??? {item.get('type', 'Item')}"))
    else:
        # Build a descriptive unidentified label using all available surface info
        unid = item.get("unidentified_name")
        if unid:
            return unid
        # Construct from subtype/slot/type — never just "armor" or "weapon"
        slot    = item.get("slot", "")
        subtype = item.get("subtype", "")
        itype   = item.get("type", "item")
        SLOT_LABELS = {
            "weapon": "weapon", "off_hand": "off-hand", "head": "helm",
            "body": "armor", "hands": "gloves", "feet": "boots",
            "neck": "amulet", "ring1": "ring", "ring2": "ring", "ring3": "ring",
            "crown": "circlet",
        }
        TYPE_LABELS = {
            "consumable": "vial", "potion": "potion", "food": "ration",
            "scroll": "scroll", "material": "component", "key_item": "key item",
        }
        # Colour / shape hints from unidentified_desc
        desc = item.get("unidentified_desc", "")
        color_words = ["red", "blue", "green", "black", "white", "yellow",
                       "purple", "silver", "golden", "glowing", "murky",
                       "clear", "dark", "bright"]
        color_hint = next((w.title() for w in color_words if w in desc.lower()), "")

        if itype in ("consumable", "potion"):
            label = f"{color_hint} Potion" if color_hint else "Unknown Potion"
        elif itype == "scroll":
            label = "Scroll (unread)"
        elif itype == "food":
            label = "Ration (unknown)"
        elif subtype:
            label = f"Unidentified {subtype.replace('_',' ').title()}"
        elif slot:
            label = f"Unidentified {SLOT_LABELS.get(slot, slot.title())}"
        else:
            label = f"Unidentified {itype.title()}"
        return label


def _auto_unidentified_desc(item):
    """Generate a surface-level description for an unidentified item.
    Reveals only visible traits: glow color, material feel, general shape.
    Never reveals stats, enchants, or curses."""
    base = item.get("unidentified_desc") or item.get("surface_desc")
    if base:
        return base
    # Auto-generate from item type
    itype = item.get("type", "")
    name  = item.get("name", "").lower()
    elem  = item.get("element", "") or item.get("enchant_element", "")
    # Visual glow hint if enchanted but not identified
    glow = ""
    if elem == "fire":     glow = "It glows with an orange light."
    elif elem == "ice":    glow = "It shimmers with frosty blue light."
    elif elem == "lightning": glow = "It crackles faintly with electricity."
    elif elem == "holy":   glow = "It radiates a soft golden warmth."
    elif elem == "shadow": glow = "It seems to drink in the light around it."
    elif elem == "nature": glow = "Faint green runes mark its surface."
    elif elem == "poison": glow = "A sickly green shimmer coats it."
    elif item.get("enhance_bonus") or item.get("magic_item"): glow = "It has a faint magical aura."
    elif item.get("cursed"): glow = "Something feels wrong about it."  # vague, no curse spoiler
    # Type hint
    if itype == "weapon":
        shape = "A weapon of unfamiliar make."
    elif itype == "armor":
        shape = "A piece of armor whose quality is unclear."
    elif itype in ("ring", "amulet", "accessory"):
        shape = f"An ornate {itype}."
    elif itype == "relic":
        shape = "An ancient relic of unknown origin."
    else:
        shape = "An item of unknown purpose."
    return f"{shape} {glow}".strip()


def _auto_partial_magic_desc(item):
    """Generate description revealing only magical properties (post magic-identify)."""
    parts = []
    elem = item.get("element") or item.get("enchant_element", "")
    if elem:
        parts.append(f"Enchanted with {elem.title()} magic.")
    bonus = item.get("enhance_bonus", 0)
    if bonus:
        parts.append(f"+{bonus} enhancement bonus.")
    if item.get("damage") and item.get("type") == "weapon":
        parts.append(f"Damage: {item['damage']}.")
    elem_dmg = item.get("element_damage")
    if elem_dmg:
        parts.append(f"+{elem_dmg} {elem.title()} damage." if elem else f"+{elem_dmg} elemental damage.")
    if item.get("accuracy_bonus"):
        parts.append(f"+{item['accuracy_bonus']} to hit.")
    stat_bonuses = item.get("stat_bonus", {})
    for stat, val in stat_bonuses.items():
        sign = "+" if val > 0 else ""
        parts.append(f"{sign}{val} {stat}.")
    if item.get("defense") and item.get("type") != "weapon":
        parts.append(f"+{item['defense']} Defense.")
    if item.get("magic_resist"):
        parts.append(f"+{item['magic_resist']} Magic Resist.")
    if not parts:
        parts.append("Magical properties detected but their nature is unclear.")
    return " ".join(parts)


def _auto_partial_material_desc(item):
    """Generate description revealing only material/quality (post appraisal)."""
    parts = []
    mat = item.get("material_desc") or item.get("material", "")
    if mat:
        parts.append(mat)
    val = item.get("estimated_value", 0)
    if val:
        parts.append(f"Estimated value: ~{val} gold.")
    itype = item.get("type", "")
    rarity = item.get("rarity", "common")
    if rarity != "common":
        parts.append(f"Quality: {rarity.title()}.")
    if not parts:
        parts.append("Good craftsmanship, but nothing stands out.")
    return " ".join(parts)


def get_item_display_desc(item):
    """Return the appropriate description based on identification state."""
    parts = []

    if item.get("identified"):
        # Base description
        base_desc = item.get("description", "")
        if base_desc:
            parts.append(base_desc)

        # ── Build stat summary for identified items ──
        stat_parts = []

        # Weapon stats
        if item.get("damage"):
            stat_parts.append(f"Dmg: {item['damage']}")
        if item.get("phys_type"):
            stat_parts.append(f"Type: {item['phys_type'].title()}")
        if item.get("range") and item["range"] != "melee":
            stat_parts.append(f"Range: {item['range'].title()}")
        if item.get("accuracy_bonus"):
            stat_parts.append(f"+{item['accuracy_bonus']} Hit")
        if item.get("speed_bonus"):
            stat_parts.append(f"+{item['speed_bonus']} Speed")
        if item.get("spell_bonus"):
            stat_parts.append(f"+{item['spell_bonus']} Spell Power")
        if item.get("crit_bonus"):
            stat_parts.append(f"+{int(item['crit_bonus']*100)}% Crit")
        if item.get("stat_scaling"):
            sc = item["stat_scaling"]
            scale_strs = [f"{k}×{v}" for k, v in sc.items() if v > 0]
            if scale_strs:
                stat_parts.append(f"Scales: {', '.join(scale_strs)}")
        elif item.get("damage_stat"):
            sc = item["damage_stat"]
            scale_strs = [f"{k}×{v}" for k, v in sc.items() if v > 0]
            if scale_strs:
                stat_parts.append(f"Scales: {', '.join(scale_strs)}")

        # Armor/defense stats
        if item.get("defense") and item.get("type") != "weapon":
            stat_parts.append(f"+{item['defense']} DEF")
        if item.get("magic_resist"):
            stat_parts.append(f"+{item['magic_resist']} MRES")
        if item.get("enchant_resist_bonus"):
            stat_parts.append(f"+{item['enchant_resist_bonus']} MRES")
        if item.get("evasion_bonus"):
            stat_parts.append(f"+{item['evasion_bonus']}% Evasion")

        # Stat bonuses — read both formats
        _EFFECT_TO_STAT = {
            "str_bonus": "STR", "dex_bonus": "DEX", "con_bonus": "CON",
            "int_bonus": "INT", "wis_bonus": "WIS", "pie_bonus": "PIE",
        }
        combined_stat_bonuses = dict(item.get("stat_bonus", {}))
        for effect_key, stat in _EFFECT_TO_STAT.items():
            eff = item.get("effect", {})
            val = eff.get(effect_key, 0) if isinstance(eff, dict) else 0
            if val:
                combined_stat_bonuses[stat] = combined_stat_bonuses.get(stat, 0) + val
        for stat, val in combined_stat_bonuses.items():
            sign = "+" if val > 0 else ""
            stat_parts.append(f"{sign}{val} {stat}")

        # Elemental/special damage
        if item.get("element"):
            stat_parts.append(f"Element: {item['element'].title()}")
        if item.get("element_damage"):
            stat_parts.append(f"+{item['element_damage']} {item.get('element','').title()} Dmg")
        if item.get("bonus_vs"):
            for enemy_type, mult in item["bonus_vs"].items():
                stat_parts.append(f"×{mult} vs {enemy_type.title()}")

        # Resistances
        if item.get("resistances"):
            for elem, level in item["resistances"].items():
                if level == "resistant":
                    stat_parts.append(f"Resist {elem.title()}")
                elif level == "immune":
                    stat_parts.append(f"Immune {elem.title()}")
                elif level == "vulnerable":
                    stat_parts.append(f"Weak {elem.title()}")

        # Status effects
        if item.get("status_on_hit"):
            se = item["status_on_hit"]
            stat_parts.append(f"On hit: {se.get('name', '???')} ({int(se.get('chance', 0)*100)}%)")
        if item.get("poison_chance"):
            stat_parts.append(f"Poison: {int(item['poison_chance']*100)}%")

        # Healing/consumable
        if item.get("heal_amount"):
            stat_parts.append(f"Heals {item['heal_amount']} HP")
        if item.get("mp_restore"):
            stat_parts.append(f"Restores {item['mp_restore']} MP")

        # Enhance bonus
        if item.get("enhance_bonus"):
            stat_parts.append(f"+{item['enhance_bonus']} Enhanced")

        # Special properties
        if item.get("two_handed"):
            stat_parts.append("Two-handed")
        if item.get("quest_item"):
            stat_parts.append("Quest Item")

        # Value
        if item.get("estimated_value"):
            stat_parts.append(f"Value: ~{item['estimated_value']}g")

        if stat_parts:
            parts.append("[" + " | ".join(stat_parts) + "]")

        return " ".join(parts) if parts else "No description."

    # ── Unidentified items — tiered partial info ──
    # Surface layer: always visible (visual clues, general shape — no spoilers)
    parts.append(_auto_unidentified_desc(item))

    # Appraisal layer: revealed if material was identified
    if item.get("material_identified"):
        parts.append(_auto_partial_material_desc(item))

    # Magic layer: revealed if magic was identified
    if item.get("magic_identified"):
        explicit = item.get("magic_desc")
        parts.append(explicit if explicit else _auto_partial_magic_desc(item))

    return " ".join(p for p in parts if p)
