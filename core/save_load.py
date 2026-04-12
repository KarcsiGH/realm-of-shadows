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
    if not item: return item
    t = item.get("type", "")
    if t not in ("weapon", "Fists"):  # Fists = Monk Unarmed
        return item
    # Special case: Monk Unarmed — inject WIS/DEX scaling if missing
    if t == "Fists" or item.get("special", {}).get("monk_scaling"):
        if not item.get("damage_stat"):
            item = dict(item)
            item["damage_stat"] = {"WIS": 0.30, "DEX": 0.20}
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

def _is_weapon_item(item):
    """True for any item that should go through weapon migration (weapons + Fists)."""
    if not item: return False
    t = item.get("type", "")
    return t == "weapon" or t == "Fists"  # Fists = Monk Unarmed

def _migrate_character_items(char):
    """Migrate all weapons in a character's inventory and equipment slots."""
    char.inventory = [_migrate_weapon(i) if _is_weapon_item(i) else i
                      for i in char.inventory]
    if char.equipment:
        for slot, item in char.equipment.items():
            if _is_weapon_item(item):
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
        "gender":             getattr(char, "gender", "male"),
        "catchup_target_level": getattr(char, "_catchup_target_level", 0),
        "catchup_xp_mult":      getattr(char, "_catchup_xp_mult", 1.0),
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
    # Retroactively patch any inventory items missing slot/damage_stat fields
    # (items saved before the slot-fix commits may lack these)
    try:
        from core.item_slot_fixer import ensure_slot
        for _inv_item in char.inventory:
            if isinstance(_inv_item, dict):
                ensure_slot(_inv_item)
    except Exception:
        pass
    char.equipment = data.get("equipment", empty_equipment())
    # Also patch equipped items
    try:
        from core.item_slot_fixer import ensure_slot as _es
        for _slot_val in char.equipment.values() if isinstance(char.equipment, dict) else []:
            if isinstance(_slot_val, dict):
                _es(_slot_val)
    except Exception:
        pass
    # Migrate old slot names → new names (save compatibility)
    _SLOT_MIGRATION = {"accessory1": "ring1", "accessory2": "neck"}
    for old_s, new_s in _SLOT_MIGRATION.items():
        if old_s in char.equipment and new_s not in char.equipment:
            char.equipment[new_s] = char.equipment.pop(old_s)
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
    char.gender                = data.get("gender", "male")
    char._catchup_target_level = data.get("catchup_target_level", 0)
    char._catchup_xp_mult      = data.get("catchup_xp_mult", 1.0)
    # Migrate old save weapons that lack damage_stat
    _migrate_character_items(char)
    return char


def serialize_world_state(ws):
    """Convert a WorldState to a JSON-serializable dict. Returns None if ws is None."""
    if ws is None:
        return None
    try:
        travel = ws.travel
        # Serialize tile-level fog-of-war as compact [x,y] list
        fog = []
        try:
            from data.world_map import MAP_W, MAP_H
            for wy in range(MAP_H):
                for wx in range(MAP_W):
                    if ws.tiles[wy][wx].get("discovered"):
                        fog.append([wx, wy])
        except Exception:
            pass
        return {
            "party_x": ws.party_x,
            "party_y": ws.party_y,
            "step_counter": ws.step_counter,
            "discovered_locations": sorted(ws.discovered_locations),
            "fog_discovered": fog,
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
        # Restore tile-level fog BEFORE _update_fog so previously seen tiles
        # remain visible after loading, not just the immediate vicinity.
        fog = data.get("fog_discovered", [])
        try:
            from data.world_map import MAP_W, MAP_H
            for wx, wy in fog:
                if 0 <= wy < MAP_H and 0 <= wx < MAP_W:
                    ws.tiles[wy][wx]["discovered"] = True
        except Exception:
            pass
        ws._update_fog()   # also reveal current position neighbourhood
        return ws
    except Exception:
        return None



def _serialize_dungeon_explored(dungeon_cache):
    """Serialize full dungeon state per floor:
    - discovered tiles
    - opened chests (from tile["event"])
    - found notes   (from tile["event"])
    - trap states: disarmed, triggered, detected (from tile["event"])
    - dead patrol enemies (by position)
    """
    if not dungeon_cache:
        return {}
    result = {}
    try:
        for dungeon_id, dstate in dungeon_cache.items():
            try:
                floors_data = {}
                for floor_num, floor in dstate.floors.items():
                    tiles = floor.get("tiles", [])
                    discovered   = []
                    opened_chests = []
                    found_notes   = []
                    trap_states   = []   # [[x, y, disarmed, triggered, detected], ...]
                    dead_enemies  = []   # [[x, y], ...]

                    for ty, row in enumerate(tiles):
                        for tx, tile in enumerate(row):
                            if tile.get("discovered"):
                                discovered.append([tx, ty])
                            # All event state lives in tile["event"], not floor["events"]
                            ev = tile.get("event")
                            if ev:
                                etype = ev.get("type", "")
                                if etype == "treasure" and ev.get("opened"):
                                    opened_chests.append([tx, ty])
                                elif etype in ("note", "journal", "scroll") and ev.get("found"):
                                    found_notes.append([tx, ty])
                                elif etype == "trap":
                                    # Save any non-default trap state
                                    dis  = bool(ev.get("disarmed", False))
                                    tri  = bool(ev.get("triggered", False))
                                    det  = bool(ev.get("detected", False))
                                    if dis or tri or det:
                                        trap_states.append([tx, ty, dis, tri, det])
                                elif etype == "fixed_encounter" and ev.get("triggered"):
                                    # Triggered fixed encounters — don't re-fire
                                    trap_states.append([tx, ty, False, True, False])

                    # Dead patrol enemies
                    for e in floor.get("enemies", []):
                        if e.get("state") == "dead":
                            dead_enemies.append([e["x"], e["y"]])

                    floor_entry = {}
                    if discovered:    floor_entry["discovered"]    = discovered
                    if opened_chests: floor_entry["opened_chests"] = opened_chests
                    if found_notes:   floor_entry["found_notes"]   = found_notes
                    if trap_states:   floor_entry["trap_states"]   = trap_states
                    if dead_enemies:  floor_entry["dead_enemies"]  = dead_enemies
                    if floor_entry:
                        floors_data[str(floor_num)] = floor_entry

                if floors_data:
                    result[dungeon_id] = floors_data
            except Exception:
                pass
    except Exception:
        pass
    return result

def save_game(party, world_state=None, slot_name="save1", metadata=None, dungeon_cache=None, dungeon_state=None, character_bank=None, **kwargs):
    """Save the party (and optionally world state) to a JSON file.
    Returns (success, filepath, message)."""
    ensure_save_dir()

    # Party knowledge (identified items, known enemies)
    from core.party_knowledge import get_save_data as get_knowledge_data
    knowledge = get_knowledge_data()

    # Story flags
    from core.story_flags import get_save_data as get_story_data
    story = get_story_data()

    # Runtime lore entries (notes found in dungeons without a static lore_id)
    from data.story_data import LORE_ENTRIES as _LE
    from core.story_flags import has_lore as _hl
    runtime_lore = {
        lid: ld for lid, ld in _LE.items()
        if lid.startswith("note_") and _hl(lid)
    }

    # Serialize active dungeon position (if saving inside a dungeon)
    dungeon_pos = None
    if dungeon_state is not None:
        try:
            dungeon_pos = {
                "dungeon_id":    dungeon_state.dungeon_id,
                "current_floor": dungeon_state.current_floor,
                "party_x":       dungeon_state.party_x,
                "party_y":       dungeon_state.party_y,
            }
        except Exception:
            pass

    save_data = {
        "version": 4,
        "timestamp": datetime.now().isoformat(),
        "slot_name": slot_name,
        "metadata": metadata or {},
        "party": [],
        "character_bank": [],
        "knowledge": knowledge,
        "story_flags": story,
        "runtime_lore": runtime_lore,
        "world_state": serialize_world_state(world_state),
        "dungeon_explored": _serialize_dungeon_explored(dungeon_cache),
        "dungeon_position": dungeon_pos,
    }

    # Serialize each character with individual error reporting
    for i, c in enumerate(party):
        try:
            save_data["party"].append(serialize_character(c))
        except Exception as e:
            return False, None, f"Save failed: could not serialize {getattr(c, 'name', f'character {i}')}: {e}"

    # Serialize character bank (Adventurers Guild roster)
    bank = character_bank or []
    for i, c in enumerate(bank):
        try:
            save_data["character_bank"].append(serialize_character(c))
        except Exception:
            pass  # bank serialization is non-critical — skip broken entries

    # Add summary metadata
    save_data["metadata"]["party_summary"] = [
        f"{c.name} Lv.{c.level} {getattr(c, 'race_name', 'Human')} {c.class_name}" for c in party
    ]
    save_data["metadata"]["total_gold"] = sum(c.gold for c in party)

    filepath = os.path.join(SAVE_DIR, f"{slot_name}.json")
    tmp_path  = filepath + ".tmp"
    try:
        # Atomic write: write to a temp file first, fsync, then rename.
        # This means the real save file is never in a partial/corrupt state —
        # the rename only happens after all bytes are safely on disk.
        with open(tmp_path, "w") as f:
            json.dump(save_data, f, indent=2)
            f.flush()
            os.fsync(f.fileno())   # force kernel buffer → physical disk
        # Verify temp file looks valid before replacing the real save
        if not os.path.exists(tmp_path) or os.path.getsize(tmp_path) < 10:
            return False, None, "Save failed: file not written to disk"
        os.replace(tmp_path, filepath)  # atomic on POSIX/macOS
        return True, filepath, f"Game saved to {slot_name}"
    except Exception as e:
        # Clean up temp file if it exists
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            pass
        return False, None, f"Save failed: {e}"


def load_game(slot_name="save1"):
    """Load a party (and world state) from a JSON file.
    Returns (success, party, world_state, message).
    world_state may be None if the save predates v4 or had no world data."""
    filepath = os.path.join(SAVE_DIR, f"{slot_name}.json")

    if not os.path.exists(filepath):
        return False, None, None, f"No save found: {slot_name}", {}, None

    try:
        with open(filepath, "r") as f:
            save_data = json.load(f)

        party = [deserialize_character(cd) for cd in save_data["party"]]

        # Restore character bank (Adventurers Guild roster)
        character_bank = []
        for cd in save_data.get("character_bank", []):
            try:
                character_bank.append(deserialize_character(cd))
            except Exception:
                pass  # skip broken bank entries gracefully

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

        # Restore runtime lore entries (notes found in dungeons)
        runtime_lore = save_data.get("runtime_lore", {})
        if runtime_lore:
            from data.story_data import LORE_ENTRIES as _LE
            for lid, ld in runtime_lore.items():
                if lid not in _LE:
                    _LE[lid] = ld

        # Restore world state (v4+ saves only)
        world_state = deserialize_world_state(save_data.get("world_state"), party)

        dungeon_explored = save_data.get("dungeon_explored", {})
        dungeon_position = save_data.get("dungeon_position")
        return True, party, world_state, f"Loaded {slot_name}", dungeon_explored, dungeon_position, character_bank
    except Exception as e:
        return False, None, None, f"Load failed: {e}", {}, None, []


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


def export_party(party):
    """Export party summary to a text file at game end.
    Returns (success: bool, path: str|None, message: str)."""
    import datetime
    try:
        ensure_save_dir()
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"party_export_{timestamp}.txt"
        filepath = os.path.join(SAVE_DIR, filename)
        lines = ["=" * 50, "REALM OF SHADOWS — PARTY EXPORT", "=" * 50, ""]
        for c in party:
            lines.append(f"{c.name}  —  Lv.{c.level} {getattr(c, 'race_name', 'Human')} {c.class_name}")
            lines.append(f"  Stats: " + "  ".join(f"{k}:{v}" for k, v in c.stats.items()))
            lines.append(f"  Gold: {c.gold}g")
            lines.append(f"  Abilities: {', '.join(a['name'] for a in c.abilities[:5])}")
            lines.append("")
        with open(filepath, "w") as f:
            f.write("\n".join(lines))
        return True, filepath, f"Party exported to {filename}"
    except Exception as e:
        return False, None, f"Export failed: {e}"
