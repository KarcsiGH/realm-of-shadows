"""
Realm of Shadows — Save/Load System

Saves party state to JSON files.
Save location: ~/Documents/RealmOfShadows/saves/
"""
import json
import os
from datetime import datetime
from core.character import Character
from core.equipment import empty_equipment

SAVE_DIR = os.path.expanduser("~/Documents/RealmOfShadows/saves")


def ensure_save_dir():
    os.makedirs(SAVE_DIR, exist_ok=True)


def serialize_character(char):
    """Convert a Character to a JSON-serializable dict."""
    return {
        "name": char.name,
        "class_name": char.class_name,
        "level": char.level,
        "xp": char.xp,
        "gold": char.gold,
        "stats": dict(char.stats),
        "resources": dict(char.resources),
        "abilities": [dict(a) for a in char.abilities],
        "inventory": list(char.inventory),  # list of dicts, already serializable
        "equipment": {
            slot: dict(item) if item else None
            for slot, item in (char.equipment or {}).items()
        },
        "life_path": list(char.life_path),
        "backstory_parts": list(char.backstory_parts),
        "quick_rolled": char.quick_rolled,
    }


def deserialize_character(data):
    """Reconstruct a Character from a saved dict."""
    char = Character(data["name"], data["class_name"])
    char.level = data.get("level", 1)
    char.xp = data.get("xp", 0)
    char.gold = data.get("gold", 0)
    char.stats = data.get("stats", {})
    char.resources = data.get("resources", {})
    char.abilities = data.get("abilities", [])
    char.inventory = data.get("inventory", [])
    char.equipment = data.get("equipment", empty_equipment())
    # Ensure all slots exist
    for slot in empty_equipment():
        if slot not in char.equipment:
            char.equipment[slot] = None
    char.life_path = data.get("life_path", [])
    char.backstory_parts = data.get("backstory_parts", [])
    char.quick_rolled = data.get("quick_rolled", False)
    return char


def save_game(party, slot_name="save1", metadata=None):
    """Save the party to a JSON file. Returns (success, filepath, message)."""
    ensure_save_dir()

    # Party knowledge (identified items, known enemies)
    from core.party_knowledge import get_save_data as get_knowledge_data
    knowledge = get_knowledge_data()

    # Story flags
    from core.story_flags import get_save_data as get_story_data
    story = get_story_data()

    save_data = {
        "version": 3,
        "timestamp": datetime.now().isoformat(),
        "slot_name": slot_name,
        "metadata": metadata or {},
        "party": [serialize_character(c) for c in party],
        "knowledge": knowledge,
        "story_flags": story,
    }

    # Add summary metadata
    save_data["metadata"]["party_summary"] = [
        f"{c.name} Lv.{c.level} {c.class_name}" for c in party
    ]
    save_data["metadata"]["total_gold"] = sum(c.gold for c in party)

    filepath = os.path.join(SAVE_DIR, f"{slot_name}.json")
    try:
        with open(filepath, "w") as f:
            json.dump(save_data, f, indent=2)
        return True, filepath, f"Game saved to {slot_name}"
    except Exception as e:
        return False, None, f"Save failed: {e}"


def load_game(slot_name="save1"):
    """Load a party from a JSON file. Returns (success, party, message)."""
    filepath = os.path.join(SAVE_DIR, f"{slot_name}.json")

    if not os.path.exists(filepath):
        return False, None, f"No save found: {slot_name}"

    try:
        with open(filepath, "r") as f:
            save_data = json.load(f)

        party = [deserialize_character(cd) for cd in save_data["party"]]

        # Restore party knowledge
        knowledge = save_data.get("knowledge")
        if knowledge:
            from core.party_knowledge import load_save_data as load_knowledge
            load_knowledge(knowledge)

        # Restore story flags
        story = save_data.get("story_flags")
        if story:
            from core.story_flags import load_save_data as load_story
            load_story(story)

        return True, party, f"Loaded {slot_name}"
    except Exception as e:
        return False, None, f"Load failed: {e}"


def list_saves():
    """List all save files. Returns list of (slot_name, metadata, timestamp)."""
    ensure_save_dir()
    saves = []
    for fname in sorted(os.listdir(SAVE_DIR)):
        if fname.endswith(".json"):
            filepath = os.path.join(SAVE_DIR, fname)
            try:
                with open(filepath, "r") as f:
                    data = json.load(f)
                slot = data.get("slot_name", fname.replace(".json", ""))
                meta = data.get("metadata", {})
                timestamp = data.get("timestamp", "")
                saves.append((slot, meta, timestamp))
            except Exception:
                continue
    return saves


def delete_save(slot_name):
    """Delete a save file."""
    filepath = os.path.join(SAVE_DIR, f"{slot_name}.json")
    if os.path.exists(filepath):
        os.remove(filepath)
        return True, f"Deleted {slot_name}"
    return False, f"Save not found: {slot_name}"
