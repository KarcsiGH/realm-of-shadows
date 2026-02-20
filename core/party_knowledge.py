"""
Realm of Shadows — Party Knowledge Registry

Tracks what the party collectively knows:
- Identified item names (once identified, always identified for the party)
- Known enemy types (once fully examined, always recognized)

This is a singleton-style module — all functions operate on module-level state.
State is saved/loaded with the game save.
"""

# ═══════════════════════════════════════════════════════════════
#  KNOWLEDGE STATE
# ═══════════════════════════════════════════════════════════════

_identified_items = set()   # set of item names that have been identified
_known_enemies = {}         # enemy_name -> highest description tier seen


def reset():
    """Clear all knowledge (new game)."""
    global _identified_items, _known_enemies
    _identified_items = set()
    _known_enemies = {}


# ═══════════════════════════════════════════════════════════════
#  ITEM IDENTIFICATION
# ═══════════════════════════════════════════════════════════════

def mark_item_identified(item_name):
    """Record that this item type has been identified by the party."""
    _identified_items.add(item_name)


def is_item_known(item_name):
    """Check if the party has previously identified this item type."""
    return item_name in _identified_items


def auto_identify_if_known(item):
    """If the party already knows this item type, auto-identify it.
    Returns True if auto-identified."""
    name = item.get("appraised_name") or item.get("name", "")
    if name and is_item_known(name):
        item["identified"] = True
        return True
    # Also check unidentified name mapping
    if item.get("name") and is_item_known(item["name"]):
        item["identified"] = True
        return True
    return False


# ═══════════════════════════════════════════════════════════════
#  ENEMY KNOWLEDGE
# ═══════════════════════════════════════════════════════════════

def mark_enemy_encountered(enemy_name, tier=1):
    """Record encountering an enemy. Tier increases with more encounters.
    tier 0 = first sighting, 1 = fought, 2 = fully known."""
    current = _known_enemies.get(enemy_name, -1)
    if tier > current:
        _known_enemies[enemy_name] = tier


def get_enemy_knowledge_tier(enemy_name):
    """Get how well the party knows this enemy type.
    Returns -1 (unknown), 0 (seen), 1 (fought), 2 (fully known)."""
    return _known_enemies.get(enemy_name, -1)


def is_enemy_known(enemy_name):
    """Check if party has fought this enemy type before."""
    return _known_enemies.get(enemy_name, -1) >= 1


# ═══════════════════════════════════════════════════════════════
#  SAVE / LOAD
# ═══════════════════════════════════════════════════════════════

def get_save_data():
    """Return serializable knowledge state."""
    return {
        "identified_items": list(_identified_items),
        "known_enemies": dict(_known_enemies),
    }


def load_save_data(data):
    """Restore knowledge state from save data."""
    global _identified_items, _known_enemies
    _identified_items = set(data.get("identified_items", []))
    _known_enemies = dict(data.get("known_enemies", {}))
