"""
Realm of Shadows — Achievement Tracker

Checks for newly unlocked achievements and maintains the earned set.
Achievements are stored in story_flags under "achievement.unlocked.<id>".

Usage:
    from core.achievement_tracker import check_achievements
    newly_unlocked = check_achievements(party)
    # Returns list of achievement dicts for newly earned achievements
"""

from achievements import ACHIEVEMENTS
from core.story_flags import get_flag, set_flag


def check_achievements(party) -> list:
    """Check all achievements and return list of newly unlocked ones.

    Call this after combat, after quest completion, and on town entry.
    """
    # Import _flags fresh each call — reset() creates a new dict object,
    # so a module-level reference becomes stale after any reset.
    from core.story_flags import _flags as current_flags
    newly = []
    for ach_id, ach in ACHIEVEMENTS.items():
        flag_key = f"achievement.unlocked.{ach_id}"
        if get_flag(flag_key):
            continue  # already earned
        try:
            if ach["check"](current_flags, party):
                set_flag(flag_key, True)
                newly.append({"id": ach_id, **ach})
        except Exception:
            pass  # never crash the game for achievements
    return newly


def get_all_unlocked() -> list:
    """Return list of all unlocked achievement dicts."""
    result = []
    for ach_id, ach in ACHIEVEMENTS.items():
        if get_flag(f"achievement.unlocked.{ach_id}"):
            result.append({"id": ach_id, **ach})
    return result


def get_progress_summary() -> dict:
    """Return {total, unlocked, pct} for display."""
    total = len(ACHIEVEMENTS)
    unlocked = sum(
        1 for ach_id in ACHIEVEMENTS
        if get_flag(f"achievement.unlocked.{ach_id}")
    )
    return {
        "total":    total,
        "unlocked": unlocked,
        "pct":      int(100 * unlocked / total) if total else 0,
    }
