#!/usr/bin/env python3
"""
Realm of Shadows — Goblin Warren Quest Chain Repair
====================================================
Use when: boss.grak.defeated is True in a save but the quest was never
properly completed — leaving the party unable to progress the story.

Run from ~/Documents/RealmOfShadows/:
    python3 repair_warren_quest.py

What this fixes:
  1. Marks main_goblin_warren as completed
  2. Starts main_hearthstone_1 (if not already active)
  3. Adds thornwood_map key → Spider's Nest becomes accessible on world map
  4. Adds Spider's Nest to discovered locations
  5. Grants the quest's gold reward (150g) split across the party
  6. All changes are safe to apply even if some are already correct
"""
import os, sys, json, glob, shutil
from datetime import datetime

SAVE_DIR = os.path.join(os.path.dirname(__file__), "saves")


def load_save(path):
    with open(path) as f:
        return json.load(f)


def backup(path):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    bk = path.replace(".json", f"_backup_{ts}.json")
    shutil.copy2(path, bk)
    return bk


def describe_state(data):
    flags = data.get("story_flags", {})
    ws    = data.get("world_state", {}) or {}
    keys  = ws.get("key_items", [])
    disc  = ws.get("discovered_locations", [])

    gw_state  = flags.get("quest.main_goblin_warren.state",  "not started")
    hs1_state = flags.get("quest.main_hearthstone_1.state",  "not started")
    sn_state  = flags.get("quest.main_spiders_nest.state",   "not started")
    grak_dead = flags.get("boss.grak.defeated", False)
    gw_clear  = flags.get("boss_defeated.goblin_warren", False)

    print(f"\n  boss.grak.defeated:           {grak_dead}")
    print(f"  boss_defeated.goblin_warren:  {gw_clear}")
    print(f"  main_goblin_warren state:     {gw_state}")
    print(f"  main_hearthstone_1 state:     {hs1_state}")
    print(f"  main_spiders_nest state:      {sn_state}")
    print(f"  key_items:                    {keys}")
    print(f"  thornwood_map in keys:        {'thornwood_map' in keys}")
    print(f"  spiders_nest discovered:      {'spiders_nest' in disc}")

    return {
        "grak_dead": grak_dead,
        "gw_clear": gw_clear,
        "gw_state": gw_state,
        "hs1_state": hs1_state,
        "keys": keys,
        "disc": disc,
        "flags": flags,
        "ws": ws,
    }


def needs_repair(state):
    """Return True if the save has the broken state we can fix."""
    return (
        state["grak_dead"] and
        state["gw_clear"] and
        state["gw_state"] != -2  # quest not completed
    )


def apply_repair(data, state):
    flags = state["flags"]
    ws    = state["ws"]
    changes = []

    # 1. Complete the Goblin Warren quest
    if flags.get("quest.main_goblin_warren.state") != -2:
        flags["quest.main_goblin_warren.state"]    = -2
        flags["quest.main_goblin_warren.rewarded"] = True
        changes.append("main_goblin_warren: marked completed + rewarded")

    # 2. Start main_hearthstone_1 if not already active or done
    hs1 = flags.get("quest.main_hearthstone_1.state")
    if hs1 is None or hs1 == 0:
        flags["quest.main_hearthstone_1.state"] = 1
        changes.append("main_hearthstone_1: started (state = 1)")
    elif hs1 == 1:
        changes.append("main_hearthstone_1: already active — no change")
    elif hs1 == -2:
        changes.append("main_hearthstone_1: already completed — no change")

    # 3. Add thornwood_map key so Spider's Nest is accessible
    keys = ws.get("key_items", [])
    if "thornwood_map" not in keys:
        keys.append("thornwood_map")
        ws["key_items"] = keys
        changes.append("thornwood_map key added → Spider's Nest unlocked")

    # 4. Add Spider's Nest to discovered locations
    disc = ws.get("discovered_locations", [])
    if "spiders_nest" not in disc:
        disc.append("spiders_nest")
        ws["discovered_locations"] = disc
        changes.append("spiders_nest added to discovered_locations")

    # 5. Grant quest gold reward (150g) split evenly across party
    party = data.get("party", [])
    if party and not flags.get("quest.main_goblin_warren.rewarded_gold"):
        reward_per = 150 // max(1, len(party))
        for char in party:
            char["gold"] = char.get("gold", 0) + reward_per
        flags["quest.main_goblin_warren.rewarded_gold"] = True
        changes.append(f"Quest reward: +{reward_per}g per character (150g total)")

    # Write back
    data["story_flags"]  = flags
    data["world_state"]  = ws

    return changes


def main():
    print("=" * 55)
    print("  Realm of Shadows — Warren Quest Chain Repair")
    print("=" * 55)

    if not os.path.isdir(SAVE_DIR):
        print(f"\n✗ Save directory not found: {SAVE_DIR}")
        print("  Run from ~/Documents/RealmOfShadows/")
        sys.exit(1)

    saves = sorted(glob.glob(os.path.join(SAVE_DIR, "*.json")))
    saves = [s for s in saves if "_backup_" not in s]

    if not saves:
        print("\nNo save files found.")
        sys.exit(0)

    # Find saves that need repair
    repairable = []
    for s in saves:
        data  = load_save(s)
        state = describe_state.__wrapped__(data) if hasattr(describe_state, '__wrapped__') else None
        flags = data.get("story_flags", {})
        ws    = data.get("world_state", {}) or {}
        disc  = ws.get("discovered_locations", [])
        keys  = ws.get("key_items", [])

        grak_dead = flags.get("boss.grak.defeated", False)
        gw_clear  = flags.get("boss_defeated.goblin_warren", False)
        gw_state  = flags.get("quest.main_goblin_warren.state")

        st = {
            "grak_dead": grak_dead, "gw_clear": gw_clear,
            "gw_state": gw_state, "keys": keys, "disc": disc,
            "hs1_state": flags.get("quest.main_hearthstone_1.state"),
            "flags": flags, "ws": ws,
        }

        broken = grak_dead and gw_clear and gw_state != -2
        print(f"\n{'─'*55}")
        print(f"  {os.path.basename(s)}")
        print(f"  Boss defeated: {grak_dead}  |  Quest complete: {gw_state == -2}")
        print(f"  thornwood_map key: {'yes' if 'thornwood_map' in keys else 'NO'}")
        print(f"  hearthstone_1 quest: {flags.get('quest.main_hearthstone_1.state', 'not started')}")
        if broken:
            print(f"  ⚠  NEEDS REPAIR — boss killed but quest not completed")
            repairable.append((s, data, st))
        else:
            print(f"  ✓  Looks consistent")

    if not repairable:
        print("\n\nNo saves need repair. If you're still stuck, run:")
        print("  python3 fix_save_flags.py")
        sys.exit(0)

    print(f"\n\nFound {len(repairable)} save(s) to repair.")

    if len(repairable) == 1:
        chosen_path, chosen_data, chosen_state = repairable[0]
        print(f"Repairing: {os.path.basename(chosen_path)}")
    else:
        print("\nWhich save to repair? Enter number: ", end="")
        for i, (p, _, _) in enumerate(repairable):
            print(f"  {i+1}) {os.path.basename(p)}")
        choice = input().strip()
        try:
            idx = int(choice) - 1
            chosen_path, chosen_data, chosen_state = repairable[idx]
        except (ValueError, IndexError):
            print("Invalid choice."); sys.exit(1)

    print(f"\nChanges to apply:")
    changes = apply_repair(chosen_data, chosen_state)
    for c in changes:
        print(f"  • {c}")

    print(f"\nApply these changes? (y/n): ", end="")
    if input().strip().lower() != "y":
        print("No changes made.")
        sys.exit(0)

    bk = backup(chosen_path)
    print(f"\nBackup: {os.path.basename(bk)}")

    with open(chosen_path, "w") as f:
        json.dump(chosen_data, f, indent=2)

    print(f"\n✓ {os.path.basename(chosen_path)} repaired successfully.")
    print("\nWhat happens next in the game:")
    print("  • Return to Maren in Briarhollow")
    print("  • She will give you the Goblin Warren turn-in dialogue")
    print("  • After the conversation, the Abandoned Mine quest begins")
    print("  • Spider's Nest is now accessible on the world map")
    print("  • Clear Spider's Nest to unlock the Abandoned Mine key")
    print("  • The Hearthstone Fragment is in the Abandoned Mine (boss floor)")


if __name__ == "__main__":
    main()
