"""
core/focus_charges.py
Charge system for focus weapons (Wand, Rod, Orb, Staff).

Charges are stored on the item dict:
  item["charges"]     — current charges  (0 = depleted)
  item["max_charges"] — maximum charges

One Mana Crystal recharges CRYSTAL_CHARGES charges.
"""

FOCUS_SUBTYPES  = {"Wand", "Rod", "Orb", "Staff", "wand", "rod", "orb", "staff"}
DEFAULT_CHARGES = {"Wand": 20, "Rod": 25, "Orb": 30, "Staff": 30,
                   "wand": 20, "rod": 25, "orb": 30, "staff": 30}
CRYSTAL_CHARGES = 5     # charges per Mana Crystal
CRYSTAL_NAME    = "Mana Crystal"

# Temple/NPC full-recharge cost per missing charge
TEMPLE_GOLD_PER_CHARGE = 8   # ~160g for a full 20-charge wand


def is_focus(item):
    return item.get("subtype", "") in FOCUS_SUBTYPES


def init_charges(item):
    """Ensure item has charge fields. Safe to call multiple times."""
    if not is_focus(item):
        return
    if "max_charges" not in item:
        item["max_charges"] = DEFAULT_CHARGES.get(item.get("subtype", "Wand"), 20)
    if "charges" not in item:
        item["charges"] = item["max_charges"]
    # Mark exempt from durability system
    item["no_durability"] = True


def has_charges(item):
    """True if focus weapon has charges remaining."""
    if not is_focus(item):
        return True   # non-focus weapons are always 'ready'
    init_charges(item)
    return item.get("charges", 0) > 0


def consume_charge(item):
    """Use 1 charge. Returns True if charge was consumed, False if depleted."""
    if not is_focus(item):
        return True
    init_charges(item)
    if item.get("charges", 0) <= 0:
        return False
    item["charges"] -= 1
    return True


def get_charge_label(item):
    """Return e.g. '(18/20)' or '(DEPLETED)'."""
    if not is_focus(item):
        return ""
    init_charges(item)
    cur = item.get("charges", 0)
    mx  = item.get("max_charges", 20)
    if cur <= 0:
        return " (DEPLETED)"
    return f" ({cur}/{mx})"


def crystals_needed(item):
    """How many Mana Crystals to fully recharge from current state."""
    if not is_focus(item):
        return 0
    init_charges(item)
    missing = item.get("max_charges", 20) - item.get("charges", 0)
    if missing <= 0:
        return 0
    import math
    return math.ceil(missing / CRYSTAL_CHARGES)


def recharge_with_crystals(item, party, count=None):
    """
    Consume Mana Crystals from party inventory to recharge the item.
    count=None means recharge as much as possible.
    Returns (charges_gained, crystals_used).
    """
    if not is_focus(item):
        return 0, 0
    init_charges(item)
    missing = item.get("max_charges", 20) - item.get("charges", 0)
    if missing <= 0:
        return 0, 0

    # Count available crystals
    from core.crafting import count_material, consume_materials
    available = count_material(party, CRYSTAL_NAME)
    if available <= 0:
        return 0, 0

    import math
    max_by_crystals = available * CRYSTAL_CHARGES
    to_gain   = min(missing, max_by_crystals if count is None else count * CRYSTAL_CHARGES)
    crystals  = math.ceil(to_gain / CRYSTAL_CHARGES)
    actual_crystals = min(crystals, available)
    actual_gain     = min(missing, actual_crystals * CRYSTAL_CHARGES)

    # Consume crystals
    consume_materials(party, {CRYSTAL_NAME: actual_crystals})
    item["charges"] = min(item["max_charges"], item.get("charges", 0) + actual_gain)
    return actual_gain, actual_crystals


def recharge_for_gold(item, party, full=True):
    """Recharge at temple/guild for gold. Returns (cost, success)."""
    if not is_focus(item):
        return 0, False
    init_charges(item)
    missing = item.get("max_charges", 20) - item.get("charges", 0)
    if missing <= 0:
        return 0, True
    cost = max(50, missing * TEMPLE_GOLD_PER_CHARGE)
    total_gold = sum(c.gold for c in party)
    if total_gold < cost:
        return cost, False
    # Deduct gold
    remaining = cost
    for c in party:
        deduct = min(c.gold, remaining)
        c.gold -= deduct
        remaining -= deduct
        if remaining <= 0:
            break
    item["charges"] = item["max_charges"]
    return cost, True
