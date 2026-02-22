"""
Realm of Shadows — Story Flag System

Tracks quest progress, player choices, discovered lore, and world state.
Flags are simple key-value pairs: string keys with int/bool/string values.
Persisted in save files alongside party and knowledge.

Flag naming convention:
  quest.<quest_id>.state     — quest progress (0=unknown, 1=started, 2=complete, etc.)
  choice.<event_id>          — player choice at a branching point
  lore.<lore_id>             — whether a lore entry has been discovered
  world.<event_id>           — world state changes (town attacked, NPC moved, etc.)
  act                        — current story act (1, 2, 3)
  boss.<boss_id>.defeated    — boss kill tracking
  npc.<npc_id>.met           — whether an NPC has been spoken to
  item.hearthstone.<n>       — hearthstone collection progress
"""

# ═══════════════════════════════════════════════════════════════
#  FLAG STORAGE (module-level singleton)
# ═══════════════════════════════════════════════════════════════

_flags = {}


def reset():
    """Clear all flags (new game)."""
    global _flags
    _flags = {
        "act": 1,
        "intro_seen": False,
    }


def get(key, default=None):
    """Get a flag value."""
    return _flags.get(key, default)


def get_flag(key, default=None):
    """Get a flag value (alias for get)."""
    return _flags.get(key, default)


def set_flag(key, value):
    """Set a flag value."""
    _flags[key] = value


def has(key):
    """Check if a flag exists and is truthy."""
    return bool(_flags.get(key))


def increment(key, amount=1):
    """Increment a numeric flag."""
    _flags[key] = _flags.get(key, 0) + amount


def get_quest_state(quest_id):
    """Get quest progress. 0=unknown, 1=started, 2+=in progress, -1=failed."""
    return _flags.get(f"quest.{quest_id}.state", 0)


def set_quest_state(quest_id, state):
    """Set quest progress."""
    _flags[f"quest.{quest_id}.state"] = state


def start_quest(quest_id):
    """Start a quest (sets to 1 if not already started)."""
    key = f"quest.{quest_id}.state"
    if _flags.get(key, 0) == 0:
        _flags[key] = 1
        try:
            import core.sound as sfx
            sfx.play("quest_accept")
        except Exception:
            pass


def complete_quest(quest_id):
    """Mark a quest as complete."""
    _flags[f"quest.{quest_id}.state"] = -2  # -2 = complete
    try:
        import core.sound as sfx
        sfx.play("quest_complete")
    except Exception:
        pass


def is_quest_complete(quest_id):
    return _flags.get(f"quest.{quest_id}.state", 0) == -2


def is_quest_active(quest_id):
    state = _flags.get(f"quest.{quest_id}.state", 0)
    return state > 0  # started but not complete/failed


def discover_lore(lore_id):
    """Mark a lore entry as discovered."""
    _flags[f"lore.{lore_id}"] = True


def has_lore(lore_id):
    return bool(_flags.get(f"lore.{lore_id}"))


def defeat_boss(boss_id):
    """Record a boss defeat."""
    _flags[f"boss.{boss_id}.defeated"] = True


def is_boss_defeated(boss_id):
    return bool(_flags.get(f"boss.{boss_id}.defeated"))


def meet_npc(npc_id):
    """Record that the party has met an NPC."""
    _flags[f"npc.{npc_id}.met"] = True


def has_met_npc(npc_id):
    return bool(_flags.get(f"npc.{npc_id}.met"))


def collect_hearthstone(n):
    """Record collection of hearthstone #n (1-5)."""
    _flags[f"item.hearthstone.{n}"] = True


def hearthstone_count():
    """How many hearthstones collected."""
    return sum(1 for i in range(1, 6) if _flags.get(f"item.hearthstone.{i}"))


# ═══════════════════════════════════════════════════════════════
#  CONDITION EVALUATION
# ═══════════════════════════════════════════════════════════════

def check_conditions(conditions):
    """
    Evaluate a list of conditions. Returns True if ALL are met.
    Each condition is a dict:
      {"flag": "key", "op": "==", "value": X}
    Supported ops: ==, !=, >, <, >=, <=, "exists", "not_exists"
    """
    if not conditions:
        return True

    for cond in conditions:
        key = cond["flag"]
        op = cond.get("op", "==")
        expected = cond.get("value", True)
        actual = _flags.get(key)

        if op == "exists":
            if actual is None:
                return False
        elif op == "not_exists":
            if actual is not None:
                return False
        elif op == "==":
            if actual != expected:
                return False
        elif op == "!=":
            if actual == expected:
                return False
        elif op == ">":
            if actual is None or actual <= expected:
                return False
        elif op == "<":
            if actual is None or actual >= expected:
                return False
        elif op == ">=":
            if actual is None or actual < expected:
                return False
        elif op == "<=":
            if actual is None or actual > expected:
                return False

    return True


# ═══════════════════════════════════════════════════════════════
#  SAVE / LOAD
# ═══════════════════════════════════════════════════════════════

def get_save_data():
    return dict(_flags)


def load_save_data(data):
    global _flags
    _flags = dict(data) if data else {}
    # Ensure defaults
    if "act" not in _flags:
        _flags["act"] = 1


# Initialize with defaults
reset()
