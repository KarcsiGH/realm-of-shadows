"""
Realm of Shadows — Tutorial Hints
Contextual one-time hints shown at key first-time moments.

Each hint fires once, gated by a 'hint.shown.<id>' story flag so it
never repeats across sessions.  All hints use the existing dungeon
show_event() or combat add_flash() systems — no new UI needed.
"""

from core.story_flags import get_flag, set_flag

# ═══════════════════════════════════════════════════════════════
#  HINT DEFINITIONS
# ═══════════════════════════════════════════════════════════════

# Format: (hint_id, flag_that_must_NOT_exist, message, color_rgb)
# Colors: cream=navigation, gold=important, green=positive, steel_blue=combat

_HINT_COLOR_NAV    = (210, 195, 165)   # cream — movement/exploration
_HINT_COLOR_COMBAT = (140, 190, 230)   # steel blue — combat mechanics
_HINT_COLOR_SYSTEM = (210, 180, 100)   # gold — system tips


DUNGEON_HINTS = {
    "first_floor": [
        ("move_keys",
         "WASD or arrow keys to move.  Q / E to turn.  ENTER at stairs to descend.",
         _HINT_COLOR_NAV),
        ("camp_key",
         "Press C (or click Camp) to rest and restore HP — costs gold and dungeon resources.",
         _HINT_COLOR_SYSTEM),
    ],
    "second_floor": [
        ("back_row",
         "Back row enemies take reduced melee damage.  Kill front row first — or move them.",
         _HINT_COLOR_COMBAT),
    ],
    "first_trap": [
        ("trap_disarm",
         "Trap detected!  Stand adjacent and press T to attempt to disarm it.",
         (220, 150, 80)),
    ],
}

COMBAT_HINTS = {
    "first_combat": [
        ("combat_rows",
         "Rows matter: FRONT takes full damage, BACK takes reduced melee hits.  Use Move to reposition.",
         _HINT_COLOR_COMBAT),
        ("combat_defend",
         "Defend gives +50% defense until your next turn — useful when low on HP.",
         _HINT_COLOR_COMBAT),
    ],
    "first_item_unidentified": [
        ("identification",
         "Unidentified items need a Mage or Thief to appraise them — visit the post-combat loot screen.",
         _HINT_COLOR_SYSTEM),
    ],
    "first_flee": [
        ("flee_tip",
         "Flee has a chance to escape based on party Speed vs. enemy Speed.  Back row flees more easily.",
         _HINT_COLOR_NAV),
    ],
}


# ═══════════════════════════════════════════════════════════════
#  PUBLIC API
# ═══════════════════════════════════════════════════════════════

def _hint_key(hint_id):
    return f"hint.shown.{hint_id}"


def _should_show(hint_id):
    return not get_flag(_hint_key(hint_id))


def _mark_shown(hint_id):
    set_flag(_hint_key(hint_id), True)


def fire_dungeon_hints(context, dungeon_ui):
    """
    Call from main._process_dungeon_event or on_floor_change.
    context: one of 'first_floor', 'second_floor', 'first_trap'
    dungeon_ui: DungeonUI instance with show_event()
    """
    hints = DUNGEON_HINTS.get(context, [])
    for hint_id, message, color in hints:
        if _should_show(hint_id):
            dungeon_ui.show_event(message, color)
            _mark_shown(hint_id)


def fire_combat_hints(context, combat_ui):
    """
    Call from start_combat or process_combat_action.
    context: one of 'first_combat', 'first_item_unidentified', 'first_flee'
    combat_ui: CombatUI instance with add_flash()
    """
    hints = COMBAT_HINTS.get(context, [])
    for hint_id, message, color in hints:
        if _should_show(hint_id):
            combat_ui.add_flash(message, color)
            _mark_shown(hint_id)


def fire_combat_hints_delayed(context, combat_ui, delay_ms=2500):
    """
    Queue a hint to fire after delay_ms — used for hints that would be
    immediately covered by combat intro flashes.
    Returns a (context, deadline_ms) tuple for the caller to track.
    """
    hints = COMBAT_HINTS.get(context, [])
    pending = []
    for hint_id, message, color in hints:
        if _should_show(hint_id):
            pending.append((hint_id, message, color, delay_ms))
    return pending


def tick_pending_hints(pending_list, elapsed_ms, combat_ui):
    """
    Call each frame from draw_combat with dt.
    Fires hints whose delay has elapsed and removes them from the list.
    Returns the updated list.
    """
    remaining = []
    for hint_id, message, color, delay in pending_list:
        delay -= elapsed_ms
        if delay <= 0:
            if _should_show(hint_id):
                combat_ui.add_flash(message, color)
                _mark_shown(hint_id)
        else:
            remaining.append((hint_id, message, color, delay))
    return remaining
