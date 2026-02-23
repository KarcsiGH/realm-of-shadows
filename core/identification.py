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
RETRY_COST_MULT = 1.5      # each retry on the same item costs 1.5× more

# Difficulty scaling
ARCANE_DIFF_SCALE = 10     # difficulty × this = target number
APPRAISAL_DIFF_SCALE = 8


# ═══════════════════════════════════════════════════════════════
#  CLASS CAPABILITIES
# ═══════════════════════════════════════════════════════════════

# Classes that can use Arcane Lore (magic identification)
ARCANE_LORE_CLASSES = {
    # class_name: resource_key used for the cost
    "Mage":       "INT-MP",
    "Cleric":     "PIE-MP",
    # Future hybrid classes
    "Battlemage":  "INT-MP",
    "Spellthief":  "INT-MP",
    "Sage":        "INT-MP",
    "Warlock":     "INT-MP",
}

# Classes that can use Appraisal (material/value identification)
APPRAISAL_CLASSES = {
    "Thief":      "DEX-SP",
    "Ranger":     "DEX-SP",
    # Future hybrid classes
    "Assassin":   "DEX-SP",
    "Spellthief": "DEX-SP",
    "Merchant":   "DEX-SP",
}


# ═══════════════════════════════════════════════════════════════
#  CAPABILITY CHECKS
# ═══════════════════════════════════════════════════════════════

def can_arcane_lore(combatant):
    """Check if this character can perform Arcane Lore identification."""
    cls = combatant.get("class_name", "")
    if cls not in ARCANE_LORE_CLASSES:
        return False, None, 0
    resource_key = ARCANE_LORE_CLASSES[cls]
    current = combatant.get("resources", {}).get(resource_key, 0)
    if combatant.get("max_resources"):
        current = combatant["resources"].get(resource_key, 0)
    cost = ARCANE_LORE_COST
    return current >= cost, resource_key, cost


def can_appraisal(combatant):
    """Check if this character can perform Appraisal identification."""
    cls = combatant.get("class_name", "")
    if cls not in APPRAISAL_CLASSES:
        return False, None, 0
    resource_key = APPRAISAL_CLASSES[cls]
    current = combatant.get("resources", {}).get(resource_key, 0)
    if combatant.get("max_resources"):
        current = combatant["resources"].get(resource_key, 0)
    cost = APPRAISAL_COST
    return current >= cost, resource_key, cost


def can_full_identify(combatant):
    """Check if character can do both Arcane Lore and Appraisal."""
    can_arc, arc_res, arc_cost = can_arcane_lore(combatant)
    can_app, app_res, app_cost = can_appraisal(combatant)
    return can_arc and can_app, arc_res, arc_cost, app_res, app_cost


def get_identify_options(combatant):
    """Return list of identification actions available to this character.
    Each entry: (action_name, description, can_afford)"""
    options = []

    can_arc, arc_res, arc_cost = can_arcane_lore(combatant)
    cls = combatant.get("class_name", "")

    if cls in ARCANE_LORE_CLASSES:
        options.append({
            "action": "arcane_lore",
            "name": "Arcane Lore",
            "description": f"Reveal magical properties ({arc_cost} {arc_res})",
            "can_afford": can_arc,
            "cost": arc_cost,
            "resource": arc_res,
        })

    can_app, app_res, app_cost = can_appraisal(combatant)
    if cls in APPRAISAL_CLASSES:
        options.append({
            "action": "appraisal",
            "name": "Appraisal",
            "description": f"Reveal material & value ({app_cost} {app_res})",
            "can_afford": can_app,
            "cost": app_cost,
            "resource": app_res,
        })

    # Full identify only if character has both capabilities
    if cls in ARCANE_LORE_CLASSES and cls in APPRAISAL_CLASSES:
        can_full = can_arc and can_app
        options.append({
            "action": "full_identify",
            "name": "Full Identify",
            "description": f"Reveal all ({arc_cost} {arc_res} + {app_cost} {app_res})",
            "can_afford": can_full,
            "cost": (arc_cost, app_cost),
            "resource": (arc_res, app_res),
        })

    return options


# ═══════════════════════════════════════════════════════════════
#  IDENTIFICATION ROLLS
# ═══════════════════════════════════════════════════════════════

def roll_arcane_lore(combatant, item):
    """Attempt Arcane Lore identification.
    Returns (success, message)."""
    difficulty = item.get("identify_difficulty", 1)
    target = difficulty * ARCANE_DIFF_SCALE

    int_val = combatant.get("stats", {}).get("INT", 0)
    level = combatant.get("level", 1)
    check = int_val + (level * 2) + random.randint(0, 5)

    if check >= target:
        item["magic_identified"] = True
        return True, f"{combatant['name']} discerns the magical properties."
    else:
        return False, f"{combatant['name']} senses magic but can't discern its nature."


def roll_appraisal(combatant, item):
    """Attempt Appraisal identification.
    Returns (success, message)."""
    difficulty = item.get("identify_difficulty", 1)
    target = difficulty * APPRAISAL_DIFF_SCALE

    int_val = combatant.get("stats", {}).get("INT", 0)
    dex_val = combatant.get("stats", {}).get("DEX", 0)
    level = combatant.get("level", 1)
    check = (int_val + dex_val) // 2 + (level * 2) + random.randint(0, 5)

    if check >= target:
        item["material_identified"] = True
        return True, f"{combatant['name']} assesses the craftsmanship and value."
    else:
        return False, f"{combatant['name']} can't determine anything unusual about this."


def attempt_identify(combatant, item, action):
    """Perform an identification attempt. Deducts resources on attempt (hit or miss).
    
    action: 'arcane_lore', 'appraisal', or 'full_identify'
    Returns: (results_list, all_succeeded)
      results_list: [(check_name, success, message), ...]
    """
    results = []

    if action in ("arcane_lore", "full_identify"):
        # Deduct MP cost
        can_arc, arc_res, arc_cost = can_arcane_lore(combatant)
        if can_arc:
            combatant["resources"][arc_res] -= arc_cost
            success, msg = roll_arcane_lore(combatant, item)
            results.append(("Arcane Lore", success, msg))
        else:
            results.append(("Arcane Lore", False, "Not enough resources."))

    if action in ("appraisal", "full_identify"):
        # Deduct SP cost
        can_app, app_res, app_cost = can_appraisal(combatant)
        if can_app:
            combatant["resources"][app_res] -= app_cost
            success, msg = roll_appraisal(combatant, item)
            results.append(("Appraisal", success, msg))
        else:
            results.append(("Appraisal", False, "Not enough resources."))

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
        return item.get("name", "Unknown Item")
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
        return item.get("unidentified_name", f"??? {item.get('type', 'Item')}")


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
            val = item.get("effect", {}).get(effect_key, 0)
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

    # ── Unidentified items ──
    parts.append(item.get("unidentified_desc",
                          item.get("surface_desc", "You're not sure what this is.")))

    if item.get("material_identified"):
        mat_desc = item.get("material_desc")
        if mat_desc:
            parts.append(mat_desc)
        if item.get("estimated_value"):
            parts.append(f"Estimated value: ~{item['estimated_value']} gold")

    if item.get("magic_identified"):
        magic_desc = item.get("magic_desc")
        if magic_desc:
            parts.append(magic_desc)

    return " ".join(parts)
