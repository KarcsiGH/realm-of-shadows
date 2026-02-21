"""
Realm of Shadows — Dungeon System

Wizardry-style multi-floor dungeons with grid-based exploration.
Each floor is procedurally generated with rooms, corridors, encounters,
treasure, and stairs connecting floors.
"""
import random
import math

# ═══════════════════════════════════════════════════════════════
#  DUNGEON TILE TYPES
# ═══════════════════════════════════════════════════════════════

DT_WALL     = "wall"
DT_FLOOR    = "floor"
DT_CORRIDOR = "corridor"
DT_DOOR     = "door"
DT_STAIRS_DOWN = "stairs_down"
DT_STAIRS_UP   = "stairs_up"
DT_TREASURE = "treasure"
DT_TRAP     = "trap"
DT_ENTRANCE = "entrance"   # floor 1 entrance from overworld
DT_SECRET_DOOR = "secret_door"  # hidden door — looks like wall until found

PASSABLE_TILES = {DT_FLOOR, DT_CORRIDOR, DT_DOOR, DT_STAIRS_DOWN,
                  DT_STAIRS_UP, DT_TREASURE, DT_TRAP, DT_ENTRANCE,
                  DT_SECRET_DOOR}

# ═══════════════════════════════════════════════════════════════
#  DUNGEON DEFINITIONS
# ═══════════════════════════════════════════════════════════════

DUNGEONS = {
    "goblin_warren": {
        "name": "Goblin Warren",
        "floors": 3,
        "width": 30, "height": 25,
        "encounter_table": {
            1: ["medium_goblins", "wolves"],
            2: ["medium_goblins", "wolves"],
            3: ["medium_goblins", "medium_bandits"],
        },
        "boss_floor": 3,
        "boss_encounter": "medium_bandits",
        "theme": "cave",
        "encounter_rate": 9,
    },
    "spiders_nest": {
        "name": "Spider's Nest",
        "floors": 4,
        "width": 35, "height": 28,
        "encounter_table": {
            1: ["medium_goblins", "wolves"],
            2: ["medium_bandits", "wolves"],
            3: ["medium_bandits", "hard_mixed"],
            4: ["hard_mixed"],
        },
        "boss_floor": 4,
        "boss_encounter": "hard_mixed",
        "theme": "cave",
        "encounter_rate": 8,
    },
    "abandoned_mine": {
        "name": "Abandoned Mine",
        "floors": 5,
        "width": 40, "height": 30,
        "encounter_table": {
            1: ["medium_bandits"],
            2: ["medium_bandits", "hard_mixed"],
            3: ["hard_mixed"],
            4: ["hard_mixed", "boss_orc"],
            5: ["boss_orc"],
        },
        "boss_floor": 5,
        "boss_encounter": "boss_orc",
        "theme": "mine",
        "encounter_rate": 8,
    },
    "sunken_crypt": {
        "name": "Sunken Crypt",
        "floors": 4,
        "width": 35, "height": 28,
        "encounter_table": {
            1: ["medium_goblins"],
            2: ["medium_bandits"],
            3: ["medium_bandits", "hard_mixed"],
            4: ["hard_mixed"],
        },
        "boss_floor": 4,
        "boss_encounter": "hard_mixed",
        "theme": "crypt",
        "encounter_rate": 9,
    },
    "ruins_ashenmoor": {
        "name": "Ruins of Ashenmoor",
        "floors": 4,
        "width": 38, "height": 30,
        "encounter_table": {
            1: ["hard_mixed"],
            2: ["hard_mixed", "boss_orc"],
            3: ["boss_orc"],
            4: ["boss_orc"],
        },
        "boss_floor": 4,
        "boss_encounter": "boss_orc",
        "theme": "ruins",
        "encounter_rate": 7,
    },
    "valdris_spire": {
        "name": "Valdris' Spire",
        "floors": 6,
        "width": 22, "height": 18,  # smaller, tighter tower floors
        "encounter_table": {
            1: ["vs_rats", "vs_guardian"],
            2: ["vs_armor_pair", "vs_armor_sentry"],
            3: ["vs_scholars", "vs_tomes"],
            4: ["vs_golem", "vs_golem_wisps"],
            5: ["vs_wraiths", "vs_fracture"],
            6: ["vs_wraiths", "vs_fracture"],
        },
        "boss_floor": 6,
        "boss_encounter": "boss_lingering_will",
        "theme": "tower",
        "encounter_rate": 7,
    },
}

# ═══════════════════════════════════════════════════════════════
#  FLOOR GENERATION
# ═══════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════
#  TIERED TRAP SYSTEM
# ═══════════════════════════════════════════════════════════════

TRAP_TIERS = {
    1: {
        "traps": [
            {"name": "Pit Trap",        "damage": (5, 8),   "target": "single", "save_stat": "DEX", "detect_base": 70, "disarm_base": 60},
            {"name": "Tripwire",        "damage": (4, 7),   "target": "single", "save_stat": "DEX", "detect_base": 70, "disarm_base": 60},
            {"name": "Loose Stones",    "damage": (3, 6),   "target": "single", "save_stat": "DEX", "detect_base": 75, "disarm_base": 65},
        ],
    },
    2: {
        "traps": [
            {"name": "Spike Trap",      "damage": (10, 16), "target": "single", "save_stat": "DEX", "detect_base": 50, "disarm_base": 45},
            {"name": "Poison Needle",   "damage": (6, 10),  "target": "single", "save_stat": "CON", "detect_base": 50, "disarm_base": 45, "poison": "poison_weak"},
            {"name": "Swinging Blade",  "damage": (12, 18), "target": "single", "save_stat": "DEX", "detect_base": 45, "disarm_base": 40},
        ],
    },
    3: {
        "traps": [
            {"name": "Gas Cloud",       "damage": (10, 15), "target": "area",   "save_stat": "CON", "detect_base": 35, "disarm_base": 30, "poison": "poison_strong"},
            {"name": "Collapsing Ceil", "damage": (20, 30), "target": "area",   "save_stat": "DEX", "detect_base": 35, "disarm_base": 30},
            {"name": "Fire Jet",        "damage": (18, 28), "target": "area",   "save_stat": "DEX", "detect_base": 40, "disarm_base": 30},
        ],
    },
    4: {
        "traps": [
            {"name": "Explosive Rune",  "damage": (30, 45), "target": "area",   "save_stat": "WIS", "detect_base": 20, "disarm_base": 20},
            {"name": "Acid Spray",      "damage": (25, 40), "target": "area",   "save_stat": "DEX", "detect_base": 25, "disarm_base": 20, "poison": "poison_strong"},
            {"name": "Blade Gauntlet",  "damage": (35, 50), "target": "single", "save_stat": "DEX", "detect_base": 20, "disarm_base": 15},
        ],
    },
    5: {
        "traps": [
            {"name": "Soul Drain",      "damage": (40, 60), "target": "area",   "save_stat": "WIS", "detect_base": 10, "disarm_base": 10, "curse": "curse_weakness"},
            {"name": "Petrify Glyph",   "damage": (30, 50), "target": "area",   "save_stat": "CON", "detect_base": 15, "disarm_base": 10, "curse": "curse_silence"},
            {"name": "Teleport Trap",   "damage": (20, 35), "target": "area",   "save_stat": "WIS", "detect_base": 10, "disarm_base": 10},
        ],
    },
}

def _dungeon_trap_offset(dungeon_id):
    """Trap tier offset based on dungeon difficulty."""
    offsets = {
        "goblin_warren": 0,     # Tier 1-3
        "spiders_nest": 1,      # Tier 2-4
        "abandoned_mine": 1,    # Tier 2-4
        "sunken_crypt": 2,      # Tier 3-5
        "ruins_ashenmoor": 2,   # Tier 3-5
    }
    return offsets.get(dungeon_id, 0)

def _make_tiered_trap(tier, rng):
    """Create a trap event dict of the given tier."""
    tier = max(1, min(5, tier))
    trap_def = rng.choice(TRAP_TIERS[tier]["traps"])
    dmg = rng.randint(trap_def["damage"][0], trap_def["damage"][1])
    event = {
        "type": "trap",
        "name": trap_def["name"],
        "tier": tier,
        "damage": dmg,
        "target": trap_def["target"],
        "save_stat": trap_def["save_stat"],
        "detect_base": trap_def["detect_base"],
        "disarm_base": trap_def["disarm_base"],
        "detected": False,
        "disarmed": False,
    }
    if "poison" in trap_def:
        event["poison"] = trap_def["poison"]
    if "curse" in trap_def:
        event["curse"] = trap_def["curse"]
    return event

def resolve_trap_saving_throw(character, trap_event):
    """Roll a saving throw for a character against a trap.
    Returns: 'avoid' (no damage), 'half' (half damage), 'full' (full damage),
             or 'crit_fail' (full + status effect)."""
    import random as rmod
    save_stat = trap_event.get("save_stat", "DEX")
    stat_val = character.stats.get(save_stat, 10)

    # Base threshold scales with trap tier
    tier = trap_event.get("tier", 1)
    threshold = 30 + tier * 10  # 40, 50, 60, 70, 80 for tiers 1-5

    # Character bonuses
    bonus = stat_val * 2
    if character.class_name == "Thief":
        bonus += 15
    elif character.class_name == "Ranger":
        bonus += 10
    elif character.class_name in ("Knight", "Fighter"):
        bonus -= 5  # heavy armor penalty

    roll = rmod.randint(1, 100) + bonus

    if roll >= threshold + 20:
        return "avoid"
    elif roll >= threshold:
        return "half"
    elif roll <= threshold - 30:
        return "crit_fail"
    else:
        return "full"


def _place_secret_room(tiles, rooms, width, height, floor_num, total_floors, rng, dungeon_id):
    """Try to carve a secret room adjacent to an existing room.
    The entrance is a DT_SECRET_DOOR tile that renders as wall until discovered."""
    from data.magic_items import get_secret_item

    # Pick a room to attach the secret room to (not first or last)
    candidates = rooms[1:-1] if len(rooms) > 2 else rooms[1:]
    if not candidates:
        return
    rng.shuffle(candidates)

    for base_room in candidates:
        rx, ry, rw, rh = base_room
        # Try each direction: left, right, top, bottom
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        rng.shuffle(directions)

        for dx, dy in directions:
            # Secret room size: small (3x3 to 4x4)
            sw = rng.randint(3, 4)
            sh = rng.randint(3, 4)

            if dx == -1:  # left of room
                sx = rx - sw - 1
                sy = ry + rng.randint(0, max(0, rh - sh))
                door_x, door_y = rx - 1, sy + sh // 2
            elif dx == 1:  # right of room
                sx = rx + rw + 1
                sy = ry + rng.randint(0, max(0, rh - sh))
                door_x, door_y = rx + rw, sy + sh // 2
            elif dy == -1:  # above room
                sx = rx + rng.randint(0, max(0, rw - sw))
                sy = ry - sh - 1
                door_x, door_y = sx + sw // 2, ry - 1
            else:  # below room
                sx = rx + rng.randint(0, max(0, rw - sw))
                sy = ry + rh + 1
                door_x, door_y = sx + sw // 2, ry + rh

            # Bounds check
            if sx < 1 or sy < 1 or sx + sw >= width - 1 or sy + sh >= height - 1:
                continue
            if door_x < 1 or door_y < 1 or door_x >= width - 1 or door_y >= height - 1:
                continue

            # Check the secret room area is all wall (no overlaps)
            clear = True
            for cy in range(sy - 1, sy + sh + 1):
                for cx in range(sx - 1, sx + sw + 1):
                    if 0 <= cy < height and 0 <= cx < width:
                        if tiles[cy][cx]["type"] != DT_WALL:
                            clear = False
                            break
                if not clear:
                    break
            if not clear:
                continue

            # Carve the secret room
            for cy in range(sy, sy + sh):
                for cx in range(sx, sx + sw):
                    tiles[cy][cx]["type"] = DT_FLOOR
                    tiles[cy][cx]["secret_room"] = True

            # Place the secret door
            tiles[door_y][door_x]["type"] = DT_SECRET_DOOR
            tiles[door_y][door_x]["discovered"] = False
            tiles[door_y][door_x]["secret_found"] = False

            # Place magic item chest in center of secret room
            cx_center = sx + sw // 2
            cy_center = sy + sh // 2
            magic_item = get_secret_item(floor_num, total_floors, rng)
            gold_bonus = rng.randint(30, 80) * floor_num
            tiles[cy_center][cx_center]["type"] = DT_TREASURE
            tiles[cy_center][cx_center]["event"] = {
                "type": "treasure", "gold": gold_bonus,
                "items": [magic_item], "opened": False,
                "secret_chest": True,
            }
            tiles[cy_center][cx_center]["secret_room"] = True
            return  # placed successfully


def generate_floor(width, height, floor_num, total_floors, theme, rng, dungeon_id="goblin_warren"):
    """Generate a single dungeon floor grid.
    Returns 2D list of tile dicts and metadata."""

    tiles = [[{"type": DT_WALL, "discovered": False, "event": None}
              for _ in range(width)] for _ in range(height)]

    rooms = []
    max_rooms = 6 + floor_num * 2
    min_room = 4
    max_room = 8

    # ── Place rooms ──
    for _ in range(max_rooms * 5):  # attempts
        if len(rooms) >= max_rooms:
            break
        rw = rng.randint(min_room, max_room)
        rh = rng.randint(min_room, max_room)
        rx = rng.randint(2, width - rw - 2)
        ry = rng.randint(2, height - rh - 2)

        # Check overlap
        overlap = False
        for (ox, oy, ow, oh) in rooms:
            if (rx - 1 < ox + ow and rx + rw + 1 > ox and
                ry - 1 < oy + oh and ry + rh + 1 > oy):
                overlap = True
                break
        if overlap:
            continue

        # Carve room
        for y in range(ry, ry + rh):
            for x in range(rx, rx + rw):
                tiles[y][x]["type"] = DT_FLOOR
        rooms.append((rx, ry, rw, rh))

    # ── Connect rooms with corridors ──
    for i in range(len(rooms) - 1):
        r1 = rooms[i]
        r2 = rooms[i + 1]
        cx1 = r1[0] + r1[2] // 2
        cy1 = r1[1] + r1[3] // 2
        cx2 = r2[0] + r2[2] // 2
        cy2 = r2[1] + r2[3] // 2

        # L-shaped corridor
        if rng.random() < 0.5:
            _carve_h_corridor(tiles, cx1, cx2, cy1, width)
            _carve_v_corridor(tiles, cy1, cy2, cx2, height)
        else:
            _carve_v_corridor(tiles, cy1, cy2, cx1, height)
            _carve_h_corridor(tiles, cx1, cx2, cy2, width)

    # ── Place doors at room-corridor transitions ──
    # A door belongs where a corridor tile is sandwiched between
    # a wall on one axis and transitions to floor on the perpendicular axis
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if tiles[y][x]["type"] != DT_CORRIDOR:
                continue
            # Check for horizontal doorway: wall above+below, floor/corridor left+right
            h_wall = (tiles[y-1][x]["type"] == DT_WALL and tiles[y+1][x]["type"] == DT_WALL)
            h_open = (tiles[y][x-1]["type"] in (DT_FLOOR, DT_CORRIDOR) and
                      tiles[y][x+1]["type"] in (DT_FLOOR, DT_CORRIDOR))
            # Check for vertical doorway: wall left+right, floor/corridor above+below
            v_wall = (tiles[y][x-1]["type"] == DT_WALL and tiles[y][x+1]["type"] == DT_WALL)
            v_open = (tiles[y-1][x]["type"] in (DT_FLOOR, DT_CORRIDOR) and
                      tiles[y+1][x]["type"] in (DT_FLOOR, DT_CORRIDOR))

            if (h_wall and h_open) or (v_wall and v_open):
                if rng.random() < 0.5:
                    tiles[y][x]["type"] = DT_DOOR

    # ── Place entrance (floor 1) or stairs up ──
    if rooms:
        first_room = rooms[0]
        entrance_x = first_room[0] + first_room[2] // 2
        entrance_y = first_room[1] + first_room[3] // 2
        if floor_num == 1:
            tiles[entrance_y][entrance_x]["type"] = DT_ENTRANCE
        else:
            tiles[entrance_y][entrance_x]["type"] = DT_STAIRS_UP

        # ── Place stairs down (except last floor) ──
        stairs_down_pos = None
        if floor_num < total_floors and len(rooms) > 1:
            last_room = rooms[-1]
            sdx = last_room[0] + last_room[2] // 2
            sdy = last_room[1] + last_room[3] // 2
            tiles[sdy][sdx]["type"] = DT_STAIRS_DOWN
            stairs_down_pos = (sdx, sdy)

        # ── Place boss encounter on last floor ──
        boss_pos = None
        if floor_num == total_floors and len(rooms) > 1:
            last_room = rooms[-1]
            bx = last_room[0] + last_room[2] // 2
            by = last_room[1] + last_room[3] // 2
            if tiles[by][bx]["type"] == DT_FLOOR:
                tiles[by][bx]["event"] = {
                    "type": "boss_encounter",
                    "triggered": False,
                }
                boss_pos = (bx, by)

        # ── Place treasure ──
        treasure_count = max(1, floor_num)
        placed_treasure = 0
        for room in rooms[1:]:
            if placed_treasure >= treasure_count:
                break
            tx = room[0] + rng.randint(1, room[2] - 2)
            ty = room[1] + rng.randint(1, room[3] - 2)
            if tiles[ty][tx]["type"] == DT_FLOOR:
                tiles[ty][tx]["type"] = DT_TREASURE
                tiles[ty][tx]["event"] = _make_treasure_event(floor_num, rng)
                placed_treasure += 1

        # ── Place traps (deeper floors = more traps) ──
        trap_count = floor_num
        placed_traps = 0
        for y in range(height):
            for x in range(width):
                if placed_traps >= trap_count:
                    break
                if tiles[y][x]["type"] == DT_CORRIDOR and rng.random() < 0.03:
                    tiles[y][x]["type"] = DT_TRAP
                    trap_tier = min(5, max(1, floor_num + _dungeon_trap_offset(dungeon_id)))
                    tiles[y][x]["event"] = _make_tiered_trap(trap_tier, rng)
                    placed_traps += 1

        # ── Fixed encounters in some rooms ──
        for ri, room in enumerate(rooms[1:], 1):
            if rng.random() < 0.35:
                ex = room[0] + room[2] // 2
                ey = room[1] + room[3] // 2
                if tiles[ey][ex]["type"] == DT_FLOOR:
                    tiles[ey][ex]["event"] = {
                        "type": "fixed_encounter",
                        "triggered": False,
                    }

        # ── Place journal/story pickups ──
        from data.story_data import get_dungeon_journals
        journals = get_dungeon_journals(dungeon_id, floor_num)
        for ji, journal in enumerate(journals):
            # Place in a room that doesn't already have an event
            room_idx = min(ji + 1, len(rooms) - 1)
            if room_idx < len(rooms):
                room = rooms[room_idx]
                jx = room[0] + rng.randint(1, max(1, room[2] - 2))
                jy = room[1] + rng.randint(1, max(1, room[3] - 2))
                if tiles[jy][jx]["type"] == DT_FLOOR and not tiles[jy][jx].get("event"):
                    tiles[jy][jx]["event"] = {
                        "type": "journal",
                        "triggered": False,
                        "title": journal["title"],
                        "text": journal["text"],
                        "lore_id": journal.get("lore_id"),
                        "on_find": journal.get("on_find", []),
                    }

        # ── Place secret rooms with magic item chests ──
        # 40% chance per floor, higher on deeper floors
        secret_chance = 0.35 + floor_num * 0.08
        if rng.random() < secret_chance and len(rooms) >= 3:
            _place_secret_room(tiles, rooms, width, height, floor_num,
                               total_floors, rng, dungeon_id)

        return {
            "tiles": tiles,
            "rooms": rooms,
            "entrance": (entrance_x, entrance_y),
            "stairs_down": stairs_down_pos,
            "width": width,
            "height": height,
        }

    # Fallback if no rooms generated
    tiles[height // 2][width // 2]["type"] = DT_ENTRANCE
    return {
        "tiles": tiles, "rooms": [], "width": width, "height": height,
        "entrance": (width // 2, height // 2), "stairs_down": None,
    }


def _carve_h_corridor(tiles, x1, x2, y, max_w):
    start, end = min(x1, x2), max(x1, x2)
    for x in range(start, end + 1):
        if 0 <= y < len(tiles) and 0 <= x < max_w:
            if tiles[y][x]["type"] == DT_WALL:
                tiles[y][x]["type"] = DT_CORRIDOR


def _carve_v_corridor(tiles, y1, y2, x, max_h):
    start, end = min(y1, y2), max(y1, y2)
    for y in range(start, end + 1):
        if 0 <= y < max_h and 0 <= x < len(tiles[0]):
            if tiles[y][x]["type"] == DT_WALL:
                tiles[y][x]["type"] = DT_CORRIDOR


def _make_treasure_event(floor_num, rng):
    gold = rng.randint(15, 35) * floor_num
    items = []
    # Higher chance of consumables on deeper floors
    if rng.random() < 0.35 + floor_num * 0.1:
        items.append(rng.choice([
            {"name": "Minor Healing Potion", "type": "consumable", "subtype": "potion",
             "heal_amount": 25, "identified": True, "estimated_value": 15},
            {"name": "Healing Potion", "type": "consumable", "subtype": "potion",
             "heal_amount": 50, "identified": True, "estimated_value": 30},
            {"name": "Antidote", "type": "consumable", "subtype": "potion",
             "cures": ["Poison"], "identified": True, "estimated_value": 20},
        ]))
    # Small chance of a bonus item on floor 2+
    if floor_num >= 2 and rng.random() < 0.2:
        items.append(rng.choice([
            {"name": "Scroll of Protection", "type": "consumable", "subtype": "scroll",
             "effect": "defense_buff", "identified": True, "estimated_value": 40},
            {"name": "Mana Crystal", "type": "consumable", "subtype": "crystal",
             "restore_mp": 30, "identified": True, "estimated_value": 35},
        ]))
    return {"type": "treasure", "gold": gold, "items": items, "opened": False}


# ═══════════════════════════════════════════════════════════════
#  DUNGEON STATE
# ═══════════════════════════════════════════════════════════════

class DungeonState:
    """Manages dungeon exploration state."""

    def __init__(self, dungeon_id, party):
        self.dungeon_id = dungeon_id
        self.party = party
        self.definition = DUNGEONS[dungeon_id]
        self.name = self.definition["name"]
        self.total_floors = self.definition["floors"]
        self.theme = self.definition["theme"]
        self.encounter_rate = self.definition["encounter_rate"]

        self.current_floor = 1
        self.floors = {}
        self.step_counter = 0

        # Generate first floor
        self._ensure_floor(1)
        floor = self.floors[1]
        self.party_x, self.party_y = floor["entrance"]
        self._update_fog()

    def _ensure_floor(self, floor_num):
        if floor_num not in self.floors:
            rng = random.Random(hash((self.dungeon_id, floor_num)))
            self.floors[floor_num] = generate_floor(
                self.definition["width"],
                self.definition["height"],
                floor_num,
                self.total_floors,
                self.theme,
                rng,
                self.dungeon_id,
            )

    def move(self, dx, dy):
        """Move party in dungeon. Returns event dict or None."""
        floor = self.floors[self.current_floor]
        nx = self.party_x + dx
        ny = self.party_y + dy

        if nx < 0 or nx >= floor["width"] or ny < 0 or ny >= floor["height"]:
            return None

        tile = floor["tiles"][ny][nx]
        if tile["type"] not in PASSABLE_TILES:
            return None
        # Secret doors block movement until found
        if tile["type"] == DT_SECRET_DOOR and not tile.get("secret_found"):
            return None

        self.party_x = nx
        self.party_y = ny
        self._update_fog()
        self._check_trap_detection(nx, ny)

        # Per-step resource trickle
        from core.progression import apply_step_regen
        from core.classes import get_all_resources
        for c in self.party:
            max_res = get_all_resources(c.class_name, c.stats, c.level)
            apply_step_regen(c, max_res)

        # Status effect ticking (poison, doom curse, etc.)
        from core.status_effects import tick_step
        step_messages = []
        for c in self.party:
            msgs = tick_step(c)
            step_messages.extend(msgs)
        if step_messages:
            self._last_step_messages = step_messages

        # Check tile events
        if tile["type"] == DT_STAIRS_DOWN:
            return {"type": "stairs_down"}
        elif tile["type"] == DT_STAIRS_UP:
            if self.current_floor == 1:
                return {"type": "exit_dungeon"}
            return {"type": "stairs_up"}
        elif tile["type"] == DT_ENTRANCE:
            return {"type": "exit_dungeon"}
        elif tile["type"] == DT_TREASURE and tile.get("event"):
            ev = tile["event"]
            if not ev.get("opened"):
                ev["opened"] = True
                return {"type": "treasure", "data": ev}
        elif tile["type"] == DT_TRAP and tile.get("event"):
            ev = tile["event"]
            if not ev.get("disarmed", False):
                # Trap fires if not disarmed, regardless of detection
                return {"type": "trap", "data": ev}
        elif tile.get("event") and tile["event"].get("type") == "fixed_encounter":
            if not tile["event"].get("triggered"):
                tile["event"]["triggered"] = True
                return {"type": "fixed_encounter"}
        elif tile.get("event") and tile["event"].get("type") == "journal":
            if not tile["event"].get("triggered"):
                tile["event"]["triggered"] = True
                return {"type": "journal", "data": tile["event"]}
        elif tile.get("event") and tile["event"].get("type") == "boss_encounter":
            if not tile["event"].get("triggered"):
                tile["event"]["triggered"] = True
                return {
                    "type": "random_encounter",
                    "dungeon_id": self.dungeon_id,
                    "floor": self.current_floor,
                    "total_floors": self.total_floors,
                    "is_boss": True,
                }

        # Random encounter check
        self.step_counter += 1
        rate = self.encounter_rate
        if self.step_counter >= random.randint(max(1, rate - 2), rate + 2):
            self.step_counter = 0
            # Check if this is the boss floor trigger (near stairs on last floor)
            is_boss = False
            if self.current_floor == self.total_floors:
                floor = self.floors[self.current_floor]
                sd = floor.get("stairs_down")
                if sd:
                    dist = abs(nx - sd[0]) + abs(ny - sd[1])
                    if dist <= 3:
                        is_boss = True
            return {
                "type": "random_encounter",
                "dungeon_id": self.dungeon_id,
                "floor": self.current_floor,
                "total_floors": self.total_floors,
                "is_boss": is_boss,
            }

        return None

    def go_downstairs(self):
        """Descend to the next floor."""
        if self.current_floor < self.total_floors:
            self.current_floor += 1
            self._ensure_floor(self.current_floor)
            floor = self.floors[self.current_floor]
            self.party_x, self.party_y = floor["entrance"]
            self._update_fog()
            return True
        return False

    def go_upstairs(self):
        """Ascend to the previous floor."""
        if self.current_floor > 1:
            self.current_floor -= 1
            floor = self.floors[self.current_floor]
            # Go to stairs down position of upper floor
            if floor["stairs_down"]:
                self.party_x, self.party_y = floor["stairs_down"]
            self._update_fog()
            return True
        return False

    def get_encounter_key(self):
        """Get random encounter key for current floor."""
        from data.enemies import DUNGEON_ENCOUNTER_TABLES
        table = DUNGEON_ENCOUNTER_TABLES.get(self.dungeon_id)
        if table:
            # Check for boss floor
            if self.current_floor >= self.total_floors and "boss" in table:
                return table["boss"]
            keys = table.get(self.current_floor, table.get(1, ["tutorial"]))
            if isinstance(keys, str):
                return keys
            return random.choice(keys)
        # Fallback to old embedded table
        table = self.definition["encounter_table"]
        keys = table.get(self.current_floor, table.get(1, ["tutorial"]))
        return random.choice(keys)

    def get_current_floor_data(self):
        return self.floors[self.current_floor]

    def get_tile(self, x, y):
        floor = self.floors[self.current_floor]
        if 0 <= x < floor["width"] and 0 <= y < floor["height"]:
            return floor["tiles"][y][x]
        return None

    def _update_fog(self):
        """Reveal tiles within sight range (3 tiles in dungeons)."""
        floor = self.floors[self.current_floor]
        sight = 3
        for dy in range(-sight, sight + 1):
            for dx in range(-sight, sight + 1):
                nx = self.party_x + dx
                ny = self.party_y + dy
                if 0 <= nx < floor["width"] and 0 <= ny < floor["height"]:
                    if math.sqrt(dx * dx + dy * dy) <= sight:
                        floor["tiles"][ny][nx]["discovered"] = True

    def _check_trap_detection(self, px, py):
        """Roll detection for traps on current and adjacent tiles.
        Thief/Ranger get bonuses. Detection just reveals the trap;
        the trap still fires unless disarmed."""
        floor = self.floors[self.current_floor]
        # Detection bonus from party composition
        detect_bonus = 0
        for c in self.party:
            if c.class_name == "Thief":
                detect_bonus += 25 + c.level * 3
            elif c.class_name == "Ranger":
                detect_bonus += 15 + c.level * 2
            # DEX/WIS contribute
            detect_bonus += c.stats.get("WIS", 0)
            detect_bonus += c.stats.get("DEX", 0) // 2

        base_chance = 30 + detect_bonus  # base 30% + bonuses

        for dy in range(-1, 2):
            for dx in range(-1, 2):
                tx, ty = px + dx, py + dy
                if 0 <= tx < floor["width"] and 0 <= ty < floor["height"]:
                    tile = floor["tiles"][ty][tx]
                    if tile["type"] == DT_TRAP and tile.get("event"):
                        ev = tile["event"]
                        if not ev.get("detected"):
                            if random.randint(1, 100) <= min(90, base_chance):
                                ev["detected"] = True

        # Also check for secret doors nearby
        self._check_secret_detection(px, py, floor, detect_bonus)

    def _check_secret_detection(self, px, py, floor, detect_bonus):
        """Roll to detect secret doors within 2 tiles.
        Harder than traps — only Thief/Ranger class bonuses count,
        not raw party stats. Repeated rolls on each step nearby."""
        # Only class bonuses matter for secrets (not raw stat stacking)
        secret_bonus = 0
        for c in self.party:
            if c.class_name == "Thief":
                secret_bonus += 15 + c.level * 3
            elif c.class_name == "Ranger":
                secret_bonus += 8 + c.level * 2
            # Only best WIS in party contributes (not all)
        best_wis = max((c.stats.get("WIS", 0) for c in self.party), default=0)
        secret_chance = 8 + secret_bonus + best_wis // 3  # much lower base

        for dy in range(-2, 3):
            for dx in range(-2, 3):
                tx, ty = px + dx, py + dy
                if 0 <= tx < floor["width"] and 0 <= ty < floor["height"]:
                    tile = floor["tiles"][ty][tx]
                    if tile["type"] == DT_SECRET_DOOR and not tile.get("secret_found"):
                        if random.randint(1, 100) <= min(60, secret_chance):
                            tile["secret_found"] = True

    def disarm_trap(self, x, y):
        """Attempt to disarm a detected trap. Returns success bool."""
        floor = self.floors[self.current_floor]
        if 0 <= x < floor["width"] and 0 <= y < floor["height"]:
            tile = floor["tiles"][y][x]
            if tile["type"] == DT_TRAP and tile.get("event"):
                ev = tile["event"]
                if ev.get("detected") and not ev.get("disarmed"):
                    # Disarm chance based on party
                    chance = 40
                    for c in self.party:
                        if c.class_name == "Thief":
                            chance += 30 + c.level * 4
                        chance += c.stats.get("DEX", 0)
                    if random.randint(1, 100) <= min(95, chance):
                        ev["disarmed"] = True
                        return True
        return False

    def get_visible_tiles(self, view_w=22, view_h=18):
        """Get tiles visible in viewport, centered on party."""
        floor = self.floors[self.current_floor]
        half_w = view_w // 2
        half_h = view_h // 2
        result = []
        for vy in range(view_h):
            row = []
            for vx in range(view_w):
                wx = self.party_x - half_w + vx
                wy = self.party_y - half_h + vy
                if 0 <= wx < floor["width"] and 0 <= wy < floor["height"]:
                    tile = floor["tiles"][wy][wx]
                    row.append({
                        "wx": wx, "wy": wy,
                        "type": tile["type"],
                        "discovered": tile["discovered"],
                        "event": tile.get("event"),
                        "is_party": (wx == self.party_x and wy == self.party_y),
                        "secret_found": tile.get("secret_found", False),
                        "secret_room": tile.get("secret_room", False),
                    })
                else:
                    row.append(None)
            result.append(row)
        return result
