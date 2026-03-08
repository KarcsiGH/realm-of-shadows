"""
core/durability.py
Item durability — gear degrades with use, broken gear loses stats,
repaired at the forge for gold + materials.

Durability is stored on the item dict:
  item["durability"]     — current durability  (0 = broken)
  item["max_durability"] — maximum durability
  item["durability_pct"] — convenience float 0.0-1.0

Items without durability fields are exempt (consumables, materials, etc.)
"""

# ── Constants ─────────────────────────────────────────────────
DUR_FULL      = 100
DUR_DAMAGED   = 60    # below this: "Damaged" — minor stat penalty
DUR_WORN      = 30    # below this: "Worn" — moderate stat penalty
DUR_BROKEN    = 0     # "Broken" — unusable / heavy penalties

# Damage dealt to weapon per successful hit
DUR_DECAY_WEAPON_HIT  = 1
# Damage dealt to armor per hit received
DUR_DECAY_ARMOR_HIT   = 1
# Accelerated decay for critical hits
DUR_DECAY_CRIT_MULT   = 2

# Stat penalties when degraded
# Keys match what combat_engine reads from item stats
DEGRADATION_PENALTIES = {
    "damaged": {   # 30%-60% durability
        "weapon": {"damage_pct": -0.10, "accuracy_mod": -5},
        "armor":  {"defense_pct": -0.10, "magic_resist_pct": -0.10},
    },
    "worn": {      # 1%-29% durability
        "weapon": {"damage_pct": -0.25, "accuracy_mod": -12},
        "armor":  {"defense_pct": -0.25, "magic_resist_pct": -0.25},
    },
    "broken": {    # 0% durability
        "weapon": {"damage_pct": -0.60, "accuracy_mod": -20},
        "armor":  {"defense_pct": -0.50, "magic_resist_pct": -0.50},
    },
}

# Repair costs (base gold, scales with item value)
REPAIR_GOLD_PER_DUR = 0.5  # gold per durability point restored
REPAIR_MIN_GOLD     = 5

# Item types that have durability (others are exempt)
DURABILITY_ITEM_TYPES = {"weapon", "armor"}


# ── Core Functions ────────────────────────────────────────────

def has_durability(item):
    """True if item tracks durability."""
    return item.get("type") in DURABILITY_ITEM_TYPES and not item.get("no_durability")


def init_durability(item):
    """Set initial durability on an item that doesn't have it yet."""
    if not has_durability(item):
        return
    if "durability" not in item:
        item["durability"] = DUR_FULL
        item["max_durability"] = DUR_FULL


def get_durability_state(item):
    """Return 'full', 'damaged', 'worn', or 'broken'."""
    if not has_durability(item):
        return "full"
    dur = item.get("durability", DUR_FULL)
    if dur <= DUR_BROKEN:
        return "broken"
    if dur < DUR_WORN:
        return "worn"
    if dur < DUR_DAMAGED:
        return "damaged"
    return "full"


def get_durability_color(item):
    """Return an RGB color reflecting durability state."""
    state = get_durability_state(item)
    return {
        "full":    (100, 220, 100),
        "damaged": (220, 200, 60),
        "worn":    (220, 120, 40),
        "broken":  (200, 50,  50),
    }[state]


def get_durability_label(item):
    """Return e.g. '85/100' or 'Broken'."""
    if not has_durability(item):
        return ""
    dur = item.get("durability", DUR_FULL)
    max_dur = item.get("max_durability", DUR_FULL)
    if dur <= 0:
        return "BROKEN"
    return f"{dur}/{max_dur}"


def degrade_weapon(item, is_crit=False):
    """Reduce weapon durability after a hit. Returns True if item broke."""
    if not has_durability(item):
        return False
    init_durability(item)
    decay = DUR_DECAY_WEAPON_HIT * (DUR_DECAY_CRIT_MULT if is_crit else 1)
    item["durability"] = max(0, item.get("durability", DUR_FULL) - decay)
    return item["durability"] <= 0


def degrade_armor(item, is_crit=False):
    """Reduce armor durability after being hit. Returns True if item broke."""
    if not has_durability(item):
        return False
    init_durability(item)
    decay = DUR_DECAY_ARMOR_HIT * (DUR_DECAY_CRIT_MULT if is_crit else 1)
    item["durability"] = max(0, item.get("durability", DUR_FULL) - decay)
    return item["durability"] <= 0


def apply_durability_penalties(item):
    """Return dict of effective stat modifiers based on current durability.
    Returns empty dict if item is fine."""
    state = get_durability_state(item)
    if state == "full":
        return {}
    item_category = "weapon" if item.get("type") == "weapon" else "armor"
    return DEGRADATION_PENALTIES.get(state, {}).get(item_category, {})


def get_effective_damage(item):
    """Return weapon damage after durability penalty."""
    base = item.get("damage", 0)
    if not base:
        return base
    penalties = apply_durability_penalties(item)
    pct = penalties.get("damage_pct", 0.0)
    return max(1, int(base * (1 + pct)))


def get_effective_defense(item):
    """Return armor defense after durability penalty."""
    base = item.get("defense", 0)
    if not base:
        return base
    penalties = apply_durability_penalties(item)
    pct = penalties.get("defense_pct", 0.0)
    return max(0, int(base * (1 + pct)))


def get_effective_magic_resist(item):
    """Return armor magic resist after durability penalty."""
    base = item.get("magic_resist", 0)
    if not base:
        return base
    penalties = apply_durability_penalties(item)
    pct = penalties.get("magic_resist_pct", 0.0)
    return max(0, int(base * (1 + pct)))


def get_effective_accuracy_mod(item):
    """Return weapon accuracy modifier after durability penalty."""
    base = item.get("accuracy_mod", 0)
    penalties = apply_durability_penalties(item)
    return base + penalties.get("accuracy_mod", 0)


# ── Repair ───────────────────────────────────────────────────

def get_repair_cost(item):
    """Calculate gold cost to fully repair an item."""
    if not has_durability(item):
        return 0
    dur = item.get("durability", DUR_FULL)
    max_dur = item.get("max_durability", DUR_FULL)
    missing = max_dur - dur
    if missing <= 0:
        return 0
    base_cost = int(missing * REPAIR_GOLD_PER_DUR)
    # Scale by item value (better items cost more to repair)
    value = item.get("estimated_value", item.get("buy_price", 50))
    value_mult = max(1.0, value / 100)
    return max(REPAIR_MIN_GOLD, int(base_cost * value_mult))


def repair_item(item):
    """Fully restore an item's durability."""
    if not has_durability(item):
        return
    item["durability"] = item.get("max_durability", DUR_FULL)


def needs_repair(character):
    """True if any equipped item is damaged/worn/broken."""
    for slot, item in (character.equipment or {}).items():
        if item and get_durability_state(item) != "full":
            return True
    return False


def get_damaged_equipment(character):
    """Return list of (slot, item) tuples for damaged equipped items."""
    result = []
    for slot, item in (character.equipment or {}).items():
        if item and has_durability(item) and get_durability_state(item) != "full":
            result.append((slot, item))
    return result
