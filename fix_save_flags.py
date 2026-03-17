#!/usr/bin/env python3
"""
Realm of Shadows — Save File Flag Inspector & Cleaner
======================================================
Run from ~/Documents/RealmOfShadows/:
    python3 fix_save_flags.py

This script:
  1. Shows you all save files and their current boss/quest flags
  2. Lets you pick a save to inspect
  3. Tells you which flags look stale vs earned
  4. Offers to remove specific stale flags so your save reflects
     what you've actually done in this playthrough
"""
import os, sys, json, glob, shutil
from datetime import datetime

SAVE_DIR = os.path.join(os.path.dirname(__file__), "saves")


def load_save(path):
    with open(path) as f:
        return json.load(f)


def backup_save(path):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = path.replace(".json", f"_backup_{ts}.json")
    shutil.copy2(path, backup)
    return backup


def describe_quest_state(state):
    if state is None:   return "not started (0)"
    if state == 0:      return "not started"
    if state == 1:      return "active"
    if state == -2:     return "completed"
    return str(state)


def analyse_save(data):
    """Return a dict of stale flags — boss flags that have no matching active quest."""
    flags = data.get("story_flags", {})

    # Map: boss flag → quest that should be active for it to be legitimate
    BOSS_TO_QUEST = {
        "boss.grak.defeated":          "quest.main_goblin_warren.state",
        "boss_defeated.goblin_warren":  "quest.main_goblin_warren.state",
        "boss.korrath.defeated":        "quest.main_hearthstone_1.state",
        "boss_defeated.abandoned_mine": "quest.main_hearthstone_1.state",
        "boss.spider_queen.defeated":   "quest.main_spiders_nest.state",
        "boss_defeated.spiders_nest":   "quest.main_spiders_nest.state",
        "boss.ashvar.defeated":         "quest.main_ashenmoor.state",
        "boss_defeated.ruins_ashenmoor":"quest.main_ashenmoor.state",
        "boss.sunken_warden.defeated":  "quest.main_hearthstone_2.state",
        "boss_defeated.sunken_crypt":   "quest.main_hearthstone_2.state",
        "boss.karreth.defeated":        "quest.main_hearthstone_2.state",
        "boss_defeated.dragons_tooth":  "quest.main_hearthstone_2.state",
    }

    stale = {}
    for boss_flag, quest_flag in BOSS_TO_QUEST.items():
        boss_val   = flags.get(boss_flag)
        quest_val  = flags.get(quest_flag, 0)

        if boss_val and quest_val != 1:
            # Boss flag is set, but the quest isn't currently active
            # This is the "stale flag" scenario
            stale[boss_flag] = {
                "boss_flag_value": boss_val,
                "quest_flag": quest_flag,
                "quest_state": quest_val,
                "quest_state_label": describe_quest_state(quest_val),
            }

    return stale


def show_save_summary(path, data):
    flags  = data.get("story_flags", {})
    meta   = data.get("metadata", {})
    name   = os.path.basename(path)
    ts     = data.get("timestamp", "unknown")
    party  = meta.get("party_summary", [])

    print(f"\n{'─'*55}")
    print(f"  {name}  |  saved: {ts[:19]}")
    for p in party:
        print(f"    {p}")

    print(f"\n  Quest states:")
    quest_flags = {k: v for k, v in flags.items() if k.startswith("quest.")}
    if quest_flags:
        for k, v in sorted(quest_flags.items()):
            print(f"    {k}: {describe_quest_state(v)}")
    else:
        print("    (none)")

    print(f"\n  Boss defeat flags:")
    boss_flags = {k: v for k, v in flags.items() if k.startswith("boss")}
    if boss_flags:
        for k, v in sorted(boss_flags.items()):
            print(f"    {k}: {v}")
    else:
        print("    (none)")


def main():
    print("=" * 55)
    print("  Realm of Shadows — Save Flag Inspector & Cleaner")
    print("=" * 55)

    if not os.path.isdir(SAVE_DIR):
        print(f"\n✗ Save directory not found: {SAVE_DIR}")
        print("  Make sure you're running this from ~/Documents/RealmOfShadows/")
        sys.exit(1)

    saves = sorted(glob.glob(os.path.join(SAVE_DIR, "*.json")))
    # Exclude backup files we created
    saves = [s for s in saves if "_backup_" not in s]

    if not saves:
        print(f"\nNo save files found in {SAVE_DIR}")
        sys.exit(0)

    # Show all saves
    print(f"\nFound {len(saves)} save file(s):\n")
    for i, s in enumerate(saves):
        data = load_save(s)
        show_save_summary(s, data)

    # If only one save, use it automatically
    if len(saves) == 1:
        chosen = saves[0]
        print(f"\nUsing: {os.path.basename(chosen)}")
    else:
        print(f"\nEnter save number to fix (1–{len(saves)}), or 'q' to quit: ", end="")
        choice = input().strip()
        if choice.lower() == "q":
            sys.exit(0)
        try:
            idx = int(choice) - 1
            chosen = saves[idx]
        except (ValueError, IndexError):
            print("Invalid choice.")
            sys.exit(1)

    data  = load_save(chosen)
    flags = data.get("story_flags", {})
    stale = analyse_save(data)

    print(f"\n{'='*55}")
    print(f"  Analysing: {os.path.basename(chosen)}")
    print(f"{'='*55}")

    if not stale:
        print("\n✓ No stale flags found — your save looks consistent.")
        print("  All boss defeat flags match quests that are currently active.")
        sys.exit(0)

    print(f"\n⚠  Found {len(stale)} stale boss flag(s):\n")
    print("  A 'stale' flag is a boss-defeated marker in your save that was")
    print("  set in a previous session, but the matching quest isn't currently")
    print("  active — so it causes Maren to offer turn-ins you haven't earned.\n")

    for boss_flag, info in sorted(stale.items()):
        print(f"  FLAG:  {boss_flag}")
        print(f"    value:       {info['boss_flag_value']}")
        print(f"    quest check: {info['quest_flag']}")
        print(f"    quest state: {info['quest_state_label']}")
        print()

    print("  Removing these flags will NOT affect your party, gold, XP,")
    print("  inventory, or any quests you've actually completed.")
    print("  A backup of your save will be created before any changes.\n")

    print("Remove stale flags? (y/n): ", end="")
    ans = input().strip().lower()

    if ans != "y":
        print("No changes made.")
        sys.exit(0)

    # Back up first
    backup = backup_save(chosen)
    print(f"\n  Backup created: {os.path.basename(backup)}")

    # Remove stale flags
    removed = []
    for boss_flag in stale:
        if boss_flag in flags:
            del flags[boss_flag]
            removed.append(boss_flag)

    data["story_flags"] = flags

    with open(chosen, "w") as f:
        json.dump(data, f, indent=2)

    print(f"\n✓ Removed {len(removed)} stale flag(s):")
    for r in removed:
        print(f"    {r}")

    print(f"\n✓ Save updated: {os.path.basename(chosen)}")
    print("\nYou can now load this save and Maren's dialogue will correctly")
    print("reflect what you've actually done in this playthrough.")
    print("\nIf anything seems wrong, restore from the backup:")
    print(f"  cp saves/{os.path.basename(backup)} saves/{os.path.basename(chosen)}")


if __name__ == "__main__":
    main()
