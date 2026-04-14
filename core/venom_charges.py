"""
core/venom_charges.py
Venom charge system for weapons with a venom reservoir
(Assassin's Crossbow, Viper Rapier).

Charges are stored on the item dict:
  item["venom_charges"]     — current charges (0 = dry)
  item["max_venom_charges"] — maximum charges

One Venom Vial refills VIAL_CHARGES charges.
When charges > 0, each hit has a VENOM_PROC_CHANCE of poisoning the target.
When charges = 0, no poison proc fires.
"""

VENOM_SUBTYPES       = {"venom_reservoir"}   # tag set on qualifying weapons
VIAL_CHARGES         = 5      # charges per Venom Vial used
VENOM_PROC_CHANCE    = 0.35   # 35% chance to proc Poisoned per hit when loaded
VENOM_POISON_TURNS   = 3      # duration of applied Poison
VENOM_VIAL_NAME      = "Venom Vial"

# Default charges by weapon subtype (set at init time)
DEFAULT_VENOM_CHARGES = 10    # both reservoir weapons start with 10 charges


def is_venom_weapon(item):
    """True if item has a venom reservoir."""
    return bool(item.get("venom_reservoir"))


def init_venom_charges(item):
    """Ensure item has venom charge fields. Safe to call multiple times."""
    if not is_venom_weapon(item):
        return
    if "max_venom_charges" not in item:
        item["max_venom_charges"] = DEFAULT_VENOM_CHARGES
    if "venom_charges" not in item:
        item["venom_charges"] = item["max_venom_charges"]


def has_venom(item):
    """True if weapon has venom charges remaining."""
    if not is_venom_weapon(item):
        return False
    init_venom_charges(item)
    return item.get("venom_charges", 0) > 0


def consume_venom_charge(item):
    """Use 1 venom charge. Returns True if charge consumed."""
    if not is_venom_weapon(item):
        return False
    init_venom_charges(item)
    if item.get("venom_charges", 0) <= 0:
        return False
    item["venom_charges"] -= 1
    return True


def get_venom_label(item):
    """Return e.g. ' (Venom: 8/10)' or ' (Venom: DRY)'."""
    if not is_venom_weapon(item):
        return ""
    init_venom_charges(item)
    cur = item.get("venom_charges", 0)
    mx  = item.get("max_venom_charges", DEFAULT_VENOM_CHARGES)
    if cur <= 0:
        return " (Venom: DRY)"
    return f" (Venom: {cur}/{mx})"


def vials_needed(item):
    """Venom Vials needed to fully refill from current state."""
    if not is_venom_weapon(item):
        return 0
    init_venom_charges(item)
    import math
    missing = item.get("max_venom_charges", DEFAULT_VENOM_CHARGES) - item.get("venom_charges", 0)
    return max(0, math.ceil(missing / VIAL_CHARGES))


def refill_with_vials(item, party, count=None):
    """
    Consume Venom Vials from party inventory to refill the weapon.
    count=None means refill as much as possible.
    Returns (charges_gained, vials_used).
    """
    if not is_venom_weapon(item):
        return 0, 0
    init_venom_charges(item)
    missing = item.get("max_venom_charges", DEFAULT_VENOM_CHARGES) - item.get("venom_charges", 0)
    if missing <= 0:
        return 0, 0

    from core.crafting import count_material, consume_materials
    available = count_material(party, VENOM_VIAL_NAME)
    if available <= 0:
        return 0, 0

    import math
    max_by_vials = available * VIAL_CHARGES
    to_gain      = min(missing, max_by_vials if count is None else count * VIAL_CHARGES)
    vials        = math.ceil(to_gain / VIAL_CHARGES)
    actual_vials = min(vials, available)
    actual_gain  = min(missing, actual_vials * VIAL_CHARGES)

    consume_materials(party, {VENOM_VIAL_NAME: actual_vials})
    item["venom_charges"] = min(item["max_venom_charges"],
                                item.get("venom_charges", 0) + actual_gain)
    return actual_gain, actual_vials
