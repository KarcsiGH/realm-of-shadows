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


def check_quest_objectives(quest_id):
    """
    Evaluate each objective in a quest.
    Returns list of (objective_dict, is_complete: bool).
    Requires data.story_data.QUESTS — lazy import to avoid circular deps.
    """
    from data.story_data import QUESTS
    q = QUESTS.get(quest_id, {})
    results = []
    for obj in q.get("objectives", []):
        flag = obj.get("flag")
        op = obj.get("op", "==")
        val = obj.get("val", True)
        actual = _flags.get(flag)
        if op == "==":
            done = actual == val
        elif op == "!=":
            done = actual != val
        elif op == ">=":
            done = actual is not None and actual >= val
        elif op == ">":
            done = actual is not None and actual > val
        elif op == "<=":
            done = actual is not None and actual <= val
        elif op == "==":
            done = actual == val
        else:
            done = bool(actual)
        results.append((obj, done))
    return results


def all_objectives_complete(quest_id):
    """True if every objective for a quest is satisfied."""
    results = check_quest_objectives(quest_id)
    return bool(results) and all(done for _, done in results)


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


# ═══════════════════════════════════════════════════════════════
#  QUEST AUTO-COMPLETE
# ═══════════════════════════════════════════════════════════════

def auto_advance_quests(party=None):
    """
    For any active quest whose all objectives are now satisfied,
    auto-complete it and distribute rewards.
    Also distributes rewards for quests just completed via dialogue
    (state == -2 but not yet rewarded).
    Returns list of completed quest IDs.
    """
    from data.story_data import QUESTS
    completed_now = []
    for qid, q in QUESTS.items():
        state = _flags.get(f"quest.{qid}.state", 0)
        rewarded_key = f"quest.{qid}.rewarded"

        # Distribute rewards for quests recently completed via dialogue
        if state == -2 and not _flags.get(rewarded_key):
            _distribute_quest_rewards(qid, party)
            _flags[rewarded_key] = True
            completed_now.append(qid)
            continue

        if state <= 0 or state == -2:
            continue  # not active or already fully handled
        if not all_objectives_complete(qid):
            continue
        # Auto-complete: no turn_in, or flagged for auto
        turnin = q.get("turn_in_npc")
        if turnin is None or q.get("auto_complete"):
            complete_quest(qid)
            _distribute_quest_rewards(qid, party)
            _flags[rewarded_key] = True
            completed_now.append(qid)
    return completed_now


def _distribute_quest_rewards(qid, party):
    """Hand out gold + XP for a completed quest."""
    from data.story_data import QUESTS
    q = QUESTS.get(qid, {})
    gold = q.get("reward_gold", 0)
    xp   = q.get("reward_xp", 0)
    if not party or (not gold and not xp):
        return
    gold_each = gold // len(party)
    xp_each   = xp   // len(party)
    for c in party:
        if gold_each:
            c.gold += gold_each
        if xp_each:
            c.xp   += xp_each
