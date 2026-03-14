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



# ── Weapon save migration ────────────────────────────────────────────────────
# Injects damage_stat into old loot weapons that were saved before the
# weapon ratio fix. Also bumps base damage by +10 to match the fixed loot tables.
_WEAPON_SUBTYPE_DS = {
    "Dagger":      {"DEX": 0.40},
    "Short Sword": {"DEX": 0.28, "STR": 0.12},
    "Shortsword":  {"DEX": 0.28, "STR": 0.12},
    "Long Sword":  {"STR": 0.30, "DEX": 0.12},
    "Longsword":   {"STR": 0.30, "DEX": 0.12},
    "Broadsword":  {"STR": 0.30, "DEX": 0.12},
    "Greatsword":  {"STR": 0.40, "DEX": 0.10},
    "Axe":         {"STR": 0.40},
    "Greataxe":    {"STR": 0.40},
    "Warhammer":   {"STR": 0.40},
    "Mace":        {"STR": 0.40},
    "Club":        {"STR": 0.40},
    "Staff":       {"STR": 0.16, "INT": 0.24},
    "Wand":        {"INT": 0.32},
    "Orb":         {"INT": 0.24, "WIS": 0.16},
    "Shortbow":    {"DEX": 0.35, "STR": 0.08},
    "Longbow":     {"DEX": 0.35, "STR": 0.08},
    "Bow":         {"DEX": 0.35, "STR": 0.08},
    "Crossbow":    {"DEX": 0.28, "STR": 0.12},
    "Spear":       {"STR": 0.24, "DEX": 0.16},
    "Rapier":      {"DEX": 0.40},
    "Cutlass":     {"DEX": 0.28, "STR": 0.12},
    "Saber":       {"DEX": 0.28, "STR": 0.12},
    "Handwraps":   {"WIS": 0.20, "DEX": 0.20},
    "Kama":        {"DEX": 0.24, "WIS": 0.16},
    "Pick":        {"STR": 0.40},
    "Hammer":      {"STR": 0.40},
    "sword":       {"STR": 0.30, "DEX": 0.12},
}

def _migrate_weapon(item):
    """Upgrade a weapon item from an old save: inject damage_stat if missing."""
    if not item or item.get("type") != "weapon":
        return item
    if "damage_stat" in item:
        return item  # already upgraded
    subtype = item.get("subtype", "")
    ds = _WEAPON_SUBTYPE_DS.get(subtype)
    if not ds:
        # Try case-insensitive match
        for k, v in _WEAPON_SUBTYPE_DS.items():
            if k.lower() == subtype.lower():
                ds = v
                break
    if ds:
        item = dict(item)  # don't mutate the original
        item["damage_stat"] = ds
        # Bump base damage by +10 to match fixed loot tables
        item["damage"] = item.get("damage", 0) + 10
    return item

def _migrate_character_items(char):
    """Migrate all weapons in a character's inventory and equipment slots."""
    char.inventory = [_migrate_weapon(i) if i and i.get("type") == "weapon" else i
                      for i in char.inventory]
    if char.equipment:
        for slot, item in char.equipment.items():
            if item and item.get("type") == "weapon":
                char.equipment[slot] = _migrate_weapon(item)
    return char


def ensure_save_dir():
    os.makedirs(SAVE_DIR, exist_ok=True)


def serialize_character(char):
    """Convert a Character to a JSON-serializable dict."""
    return {
        "name": char.name,
        "class_name": char.class_name,
        "race_name": getattr(char, "race_name", "Human"),
        "level": char.level,
        "xp": char.xp,
        "gold": char.gold,
        "stats": dict(char.stats),
        "resources": dict(char.resources),
        "abilities": [dict(a) for a in char.abilities],
        "inventory": list(char.inventory),
        "equipment": {
            slot: dict(item) if item else None
            for slot, item in (char.equipment or {}).items()
        },
        "life_path": list(char.life_path),
        "backstory_parts": list(char.backstory_parts),
        "quick_rolled": char.quick_rolled,
        "human_bonus_stat": getattr(char, "human_bonus_stat", None),
        "planar_tier": getattr(char, "planar_tier", 0),
        "combat_row":  getattr(char, "combat_row", "front"),
    }


def deserialize_character(data):
    """Reconstruct a Character from a saved dict."""
    race = data.get("race_name", "Human")
    # Guard: class_name may be None in very old saves — fall back to Fighter
    class_name = data.get("class_name") or "Fighter"
    char = Character(data["name"], class_name, race)
    char.level = data.get("level", 1)
    char.xp = data.get("xp", 0)
    char.gold = data.get("gold", 0)
    char.stats = data.get("stats", {})
    # Safety: if stats is empty or missing keys, fill with defaults
    for stat in ("STR", "DEX", "CON", "INT", "WIS", "PIE"):
        if stat not in char.stats:
            char.stats[stat] = 5
    char.resources = data.get("resources", {})
    # Safety: if HP is missing from resources, recalculate it
    if "HP" not in char.resources:
        from core.classes import CLASSES, calc_hp
        cls = CLASSES.get(char.class_name, {})
        char.resources["HP"] = calc_hp(cls.get("base_hp", 20), char.stats.get("CON", 5), char.level)
    char.abilities = data.get("abilities", [])
    # Re-merge each ability from CLASS_ABILITIES so type/self_only/buff fields are always present.
    # This fixes old saves made before the ability-stub fix, and future-proofs saves.
    try:
        from core.abilities import CLASS_ABILITIES
        lookup = {ab["name"]: ab for ab in CLASS_ABILITIES.get(char.class_name, [])}
        merged = []
        for a in char.abilities:
            if isinstance(a, dict) and a.get("name") in lookup:
                # Use full CLASS_ABILITIES dict as base; overlay saved cost/resource in case
                # the player had a modified version, but always trust the full dict for type/buff/self_only
                full = dict(lookup[a["name"]])
                merged.append(full)
            else:
                merged.append(a)
        char.abilities = merged
    except Exception:
        pass  # non-critical — stubs still work, just miss type info
    char.inventory = data.get("inventory", [])
    char.equipment = data.get("equipment", empty_equipment())
    # Ensure all slots exist
    for slot in empty_equipment():
        if slot not in char.equipment:
            char.equipment[slot] = None
    char.life_path = data.get("life_path", [])
    char.backstory_parts = data.get("backstory_parts", [])
    char.quick_rolled = data.get("quick_rolled", False)
    char.human_bonus_stat = data.get("human_bonus_stat", None)
    char.planar_tier = data.get("planar_tier", 0)
    char.combat_row  = data.get("combat_row", "front")
    # Migrate old save weapons that lack damage_stat
    _migrate_character_items(char)
    return char


def serialize_world_state(ws):
    """Convert a WorldState to a JSON-serializable dict. Returns None if ws is None."""
    if ws is None:
        return None
    try:
        travel = ws.travel
        return {
            "party_x": ws.party_x,
            "party_y": ws.party_y,
            "step_counter": ws.step_counter,
            "discovered_locations": sorted(ws.discovered_locations),
            "key_items": list(ws.key_items),
            "seed": getattr(ws, "_seed", 42),
            "travel": {
                "has_horse": travel.has_horse,
                "has_boat": travel.has_boat,
                "has_carpet": travel.has_carpet,
                "travel_mode": travel.travel_mode,
                "boat_location": travel.boat_location,
                "attuned_circles": list(travel.attuned_circles),
                "rail_unlocked": travel.rail_unlocked,
            },
        }
    except Exception:
        return None


def deserialize_world_state(data, party):
    """Reconstruct a WorldState from saved dict. Returns None on failure."""
    if not data:
        return None
    try:
        from data.world_map import WorldState
        seed = data.get("seed", 42)
        ws = WorldState(party, seed=seed)
        ws.party_x = data.get("party_x", ws.party_x)
        ws.party_y = data.get("party_y", ws.party_y)
        ws.step_counter = data.get("step_counter", 0)
        ws.discovered_locations = set(data.get("discovered_locations", []))
        ws.key_items = list(data.get("key_items", []))
        travel_data = data.get("travel", {})
        ws.travel.has_horse = travel_data.get("has_horse", False)
        ws.travel.has_boat = travel_data.get("has_boat", False)
        ws.travel.has_carpet = travel_data.get("has_carpet", False)
        ws.travel.travel_mode = travel_data.get("travel_mode", "walk")
        ws.travel.boat_location = travel_data.get("boat_location", None)
        ws.travel.attuned_circles = list(travel_data.get("attuned_circles", []))
        ws.travel.rail_unlocked = travel_data.get("rail_unlocked", False)
        ws._update_fog()
        return ws
    except Exception:
        return None


def save_game(party, world_state=None, slot_name="save1", metadata=None):
    """Save the party (and optionally world state) to a JSON file.
    Returns (success, filepath, message)."""
    ensure_save_dir()

    # Party knowledge (identified items, known enemies)
    from core.party_knowledge import get_save_data as get_knowledge_data
    knowledge = get_knowledge_data()

    # Story flags
    from core.story_flags import get_save_data as get_story_data
    story = get_story_data()

    save_data = {
        "version": 4,
        "timestamp": datetime.now().isoformat(),
        "slot_name": slot_name,
        "metadata": metadata or {},
        "party": [],
        "knowledge": knowledge,
        "story_flags": story,
        "world_state": serialize_world_state(world_state),
    }

    # Serialize each character with individual error reporting
    for i, c in enumerate(party):
        try:
            save_data["party"].append(serialize_character(c))
        except Exception as e:
            return False, None, f"Save failed: could not serialize {getattr(c, 'name', f'character {i}')}: {e}"

    # Add summary metadata
    save_data["metadata"]["party_summary"] = [
        f"{c.name} Lv.{c.level} {getattr(c, 'race_name', 'Human')} {c.class_name}" for c in party
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
    """Load a party (and world state) from a JSON file.
    Returns (success, party, world_state, message).
    world_state may be None if the save predates v4 or had no world data."""
    filepath = os.path.join(SAVE_DIR, f"{slot_name}.json")

    if not os.path.exists(filepath):
        return False, None, None, f"No save found: {slot_name}"

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

        # Restore world state (v4+ saves only)
        world_state = deserialize_world_state(save_data.get("world_state"), party)

        return True, party, world_state, f"Loaded {slot_name}"
    except Exception as e:
        return False, None, None, f"Load failed: {e}"


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
