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
DT_INTERACTABLE = "interactable"  # healing pools, MP shrines, cursed objects

PASSABLE_TILES = {DT_FLOOR, DT_CORRIDOR, DT_DOOR, DT_STAIRS_DOWN,
                  DT_STAIRS_UP, DT_TREASURE, DT_TRAP, DT_ENTRANCE,
                  DT_SECRET_DOOR, DT_INTERACTABLE}

# ═══════════════════════════════════════════════════════════════
#  DUNGEON DEFINITIONS
# ═══════════════════════════════════════════════════════════════

DUNGEONS = {
    "goblin_warren": {
        "name": "Goblin Warren",
        "floors": 3,
        "width": 50, "height": 40,
        "encounter_table": {
            1: ["medium_goblins", "wolves"],
            2: ["medium_goblins", "wolves"],
            3: ["medium_goblins"],
        },
        "boss_floor": 3,
        "boss_encounter": "boss_goblin_king",
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
        "boss_encounter": "boss_spider_queen",
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
            4: ["hard_mixed"],
            5: ["hard_mixed"],
        },
        "boss_floor": 5,
        "boss_encounter": "boss_mine_warden",
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
        "boss_encounter": "boss_warden",
        "theme": "crypt",
        "encounter_rate": 9,
    },
    "ruins_ashenmoor": {
        "name": "Ruins of Ashenmoor",
        "floors": 4,
        "width": 38, "height": 30,
        "encounter_table": {
            1: ["hard_mixed"],
            2: ["hard_mixed"],
            3: ["hard_mixed"],
            4: ["hard_mixed"],
        },
        "boss_floor": 4,
        "boss_encounter": "boss_ashenmoor",
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
    "dragons_tooth": {
        "name": "Dragon's Tooth",
        "floors": 3,
        "width": 38, "height": 30,
        "encounter_table": {
            1: ["dt_hatchlings", "dt_beetles"],
            2: ["dt_drakes", "dt_troll", "dt_beetles"],
            3: ["dt_mixed", "dt_drake_swarm"],
        },
        "boss_floor": 3,
        "boss_encounter": "boss_karreth",
        "theme": "cave",
        "encounter_rate": 7,
    },

    # ── ACT 3 DUNGEONS ──────────────────────────────────────

    "pale_coast": {
        "name": "Pale Coast Catacombs",
        "floors": 4,
        "width": 35, "height": 28,
        "encounter_table": {
            1: ["pc_drowned", "pc_shades"],
            2: ["pc_tide", "pc_drowned_mob"],
            3: ["pc_golem", "pc_tide", "pc_drowned_mob"],
            4: ["pc_twin_golems", "pc_golem"],
        },
        "boss_floor": 4,
        "boss_encounter": "boss_pale_warden",
        "theme": "crypt",
        "encounter_rate": 7,
        "act": 3,
    },

    "windswept_isle": {
        "name": "Windswept Isle Ruins",
        "floors": 3,
        "width": 32, "height": 26,
        "encounter_table": {
            1: ["wi_wraiths", "wi_sprites"],
            2: ["wi_mixed", "wi_golem"],
            3: ["wi_storm_mob", "wi_golem"],
        },
        "boss_floor": 3,
        "boss_encounter": "boss_isle_keeper",
        "theme": "ruins",
        "encounter_rate": 7,
        "act": 3,
    },

    "shadow_throne": {
        "name": "The Shadow Throne",
        "floors": 8,
        "width": 40, "height": 32,
        "encounter_table": {
            1: ["st_shades", "st_mixed"],
            2: ["st_shades", "st_echoes"],
            3: ["st_echoes", "st_abominations"],
            4: ["st_elite", "st_abominations"],
            5: ["st_void", "st_elite"],
            6: ["st_shadow_squad", "st_warden_elite"],
            7: ["st_warden_elite", "st_shadow_squad", "st_elite"],
            8: ["st_void", "st_shadow_squad"],
        },
        "boss_floor": 8,
        "boss_encounter": "boss_valdris_phase1",
        "theme": "crypt",
        "encounter_rate": 6,
        "act": 3,
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


def _place_interactables(tiles, rooms, floor_num, total_floors, rng, dungeon_id):
    """Place healing pools, MP shrines, and cursed interactables in rooms.
    
    Types:
    - healing_pool: Restores ~30% HP to party. Single use per visit.
    - mp_shrine: Restores ~25% MP/SP. Single use per visit.
    - cursed_altar: Risky — 60% chance of buff, 40% chance of curse/damage.
    """
    # Only place in rooms that don't have events
    # 1-2 interactables per floor, more on deeper floors
    count = min(3, 1 + floor_num // 2)
    
    # Dungeon-specific theming
    pool_types = {
        "goblin_warren":   ["healing_pool", "mp_shrine"],
        "spiders_nest":    ["healing_pool", "cursed_altar"],
        "sunken_crypt":    ["mp_shrine", "cursed_altar", "cursed_altar"],
        "abandoned_mine":  ["healing_pool", "mp_shrine", "cursed_altar"],
        "ruins_ashenmoor": ["mp_shrine", "cursed_altar"],
        "valdris_spire":   ["mp_shrine", "cursed_altar", "healing_pool"],
    }
    available = pool_types.get(dungeon_id, ["healing_pool", "mp_shrine"])
    
    placed = 0
    # Shuffle room order (skip first room which has entrance)
    candidate_rooms = list(rooms[1:])
    rng.shuffle(candidate_rooms)
    
    for room in candidate_rooms:
        if placed >= count:
            break
        # Find an empty floor tile in this room
        rx, ry, rw, rh = room
        px = rx + rng.randint(1, max(1, rw - 2))
        py = ry + rng.randint(1, max(1, rh - 2))
        
        if (0 <= py < len(tiles) and 0 <= px < len(tiles[0]) and 
            tiles[py][px]["type"] == DT_FLOOR and not tiles[py][px].get("event")):
            
            itype = rng.choice(available)
            tiles[py][px]["type"] = DT_INTERACTABLE
            tiles[py][px]["event"] = _make_interactable(itype, floor_num, rng)
            placed += 1


def _make_interactable(itype, floor_num, rng):
    """Create an interactable event dict."""
    if itype == "healing_pool":
        names = ["Shimmering Pool", "Healing Spring", "Life Font", 
                 "Sacred Basin", "Crystal Pool"]
        hints = [
            "The water glows with a gentle warmth.",
            "You feel a soothing presence near the water.",
            "Faint motes of light drift up from the surface.",
        ]
        return {
            "type": "interactable",
            "subtype": "healing_pool",
            "name": rng.choice(names),
            "hint": rng.choice(hints),
            "used": False,
            "heal_pct": 0.30 + floor_num * 0.02,  # 30-40% HP
        }
    elif itype == "mp_shrine":
        names = ["Arcane Shrine", "Mana Wellspring", "Spirit Altar",
                 "Runic Pillar", "Glowing Obelisk"]
        hints = [
            "Arcane energy crackles in the air around it.",
            "The runes pulse with stored power.",
            "You feel your mind sharpen near the shrine.",
        ]
        return {
            "type": "interactable",
            "subtype": "mp_shrine",
            "name": rng.choice(names),
            "hint": rng.choice(hints),
            "used": False,
            "restore_pct": 0.25 + floor_num * 0.02,  # 25-35% MP/SP
        }
    elif itype == "cursed_altar":
        names = ["Dark Altar", "Shadowed Idol", "Twisted Shrine",
                 "Blood-stained Pillar", "Whispering Monolith"]
        hints = [
            "An unsettling aura radiates from it. Touch it?",
            "Dark whispers seem to emanate from within.",
            "The stone is warm despite the cold air.",
        ]
        # Outcomes determined when used, not at creation
        return {
            "type": "interactable",
            "subtype": "cursed_altar",
            "name": rng.choice(names),
            "hint": rng.choice(hints),
            "used": False,
            "buff_chance": 0.55,  # 55% chance of good outcome
            "buff_hp": int(15 + floor_num * 5),  # bonus max HP for rest of dungeon
            "curse_dmg": int(10 + floor_num * 8),  # damage on bad outcome
        }
    return {"type": "interactable", "subtype": itype, "used": False}


def _place_secret_room(tiles, rooms, width, height, floor_num, total_floors, rng, dungeon_id):
    """Try to carve a secret room adjacent to an existing room.
    The entrance is a DT_SECRET_DOOR tile that renders as wall until discovered."""
    from data.magic_items import get_secret_item, get_cursed_item

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
            # 8% chance the secret chest contains a cursed item instead
            if rng.random() < 0.08:
                magic_item = get_cursed_item(floor_num, total_floors, rng)
            else:
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


def _place_wall_door(tiles, scan_range, wall_coord, corr_coord, axis, height, width, rng):
    """Place at most one door per contiguous corridor segment along a room wall.
    
    axis="h": scanning x values, wall_coord/corr_coord are y values
    axis="v": scanning y values, wall_coord/corr_coord are x values
    
    Skip entirely if there is already an open floor connection on this wall segment.
    """
    # Pre-check: if any tile on the wall side is already floor/corridor (open connection), skip
    scan_list = list(scan_range)
    for pos in scan_list:
        if axis == "h":
            wy, wx = wall_coord, pos
        else:
            wy, wx = pos, wall_coord
        if 0 <= wy < height and 0 <= wx < width:
            wt = tiles[wy][wx]["type"]
            if wt in (DT_FLOOR, DT_CORRIDOR):
                return  # open connection already exists — no door

    in_segment = False
    segment_candidates = []

    for pos in scan_range:
        if axis == "h":
            wy, wx = wall_coord, pos
            cy, cx = corr_coord, pos
        else:  # "v"
            wy, wx = pos, wall_coord
            cy, cx = pos, corr_coord

        # Bounds check
        if not (0 <= wy < height and 0 <= wx < width):
            if in_segment and segment_candidates:
                _pick_door(tiles, segment_candidates, rng)
                segment_candidates = []
            in_segment = False
            continue
        if not (0 <= cy < height and 0 <= cx < width):
            if in_segment and segment_candidates:
                _pick_door(tiles, segment_candidates, rng)
                segment_candidates = []
            in_segment = False
            continue

        wall_tile = tiles[wy][wx]["type"]
        corr_tile = tiles[cy][cx]["type"]

        if wall_tile == DT_WALL and corr_tile == DT_CORRIDOR:
            in_segment = True
            segment_candidates.append((wx, wy))
        else:
            if in_segment and segment_candidates:
                _pick_door(tiles, segment_candidates, rng)
                segment_candidates = []
            in_segment = False

    # End of scan — flush last segment
    if in_segment and segment_candidates:
        _pick_door(tiles, segment_candidates, rng)


def _pick_door(tiles, candidates, rng):
    """From a list of wall positions in a contiguous corridor segment,
    pick one to become a door (prefer the middle). Never place at a corner."""
    if not candidates:
        return
    if rng.random() < 0.3:
        return  # 30% chance no door at all for this entry
    # Filter out corner positions (adjacent to walls on perpendicular axes)
    def is_corner(x, y):
        h = len(tiles); w = len(tiles[0])
        neighbors = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
        wall_neighbors = sum(
            1 for nx,ny in neighbors
            if 0<=nx<w and 0<=ny<h and tiles[ny][nx]["type"] == DT_WALL
        )
        return wall_neighbors >= 3  # corner = 3+ adjacent walls

    valid = [(x,y) for x,y in candidates if not is_corner(x,y)]
    if not valid:
        return  # all candidates are corners — skip
    mid = len(valid) // 2
    x, y = valid[mid]
    tiles[y][x]["type"] = DT_DOOR


def generate_floor(width, height, floor_num, total_floors, theme, rng, dungeon_id="goblin_warren"):
    """Generate a single dungeon floor grid.
    Returns 2D list of tile dicts and metadata."""

    tiles = [[{"type": DT_WALL, "discovered": False, "event": None}
              for _ in range(width)] for _ in range(height)]

    rooms = []
    max_rooms = 10 + floor_num * 2
    min_room = 5
    max_room = 10

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

    # ── Place doors at room entrances only ──
    # A door should ONLY appear where a corridor enters a room.
    # For each room wall, find corridor connections and place at most one door
    # per contiguous corridor segment.
    for (rx, ry, rw, rh) in rooms:
        # Top wall (y = ry-1): check for corridor at y = ry-2
        _place_wall_door(tiles, range(rx, rx + rw), ry - 1, ry - 2,
                         axis="h", height=height, width=width, rng=rng)
        # Bottom wall (y = ry+rh): check for corridor at y = ry+rh+1
        _place_wall_door(tiles, range(rx, rx + rw), ry + rh, ry + rh + 1,
                         axis="h", height=height, width=width, rng=rng)
        # Left wall (x = rx-1): check for corridor at x = rx-2
        _place_wall_door(tiles, range(ry, ry + rh), rx - 1, rx - 2,
                         axis="v", height=height, width=width, rng=rng)
        # Right wall (x = rx+rw): check for corridor at x = rx+rw+1
        _place_wall_door(tiles, range(ry, ry + rh), rx + rw, rx + rw + 1,
                         axis="v", height=height, width=width, rng=rng)

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

        # ── Place traps (floor 1: 3 traps, scales up) ──
        trap_count = 2 + floor_num * 2
        placed_traps = 0
        trap_tiles = []
        for y in range(height):
            for x in range(width):
                if tiles[y][x]["type"] in (DT_CORRIDOR, DT_FLOOR):
                    trap_tiles.append((x, y))
        rng.shuffle(trap_tiles)
        for tx2, ty2 in trap_tiles:
            if placed_traps >= trap_count:
                break
            if tiles[ty2][tx2]["type"] in (DT_CORRIDOR, DT_FLOOR):
                tiles[ty2][tx2]["type"] = DT_TRAP
                trap_tier = min(5, max(1, floor_num + _dungeon_trap_offset(dungeon_id)))
                tiles[ty2][tx2]["event"] = _make_tiered_trap(trap_tier, rng)
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

        # ── Place interactables (healing pools, MP shrines, cursed objects) ──
        _place_interactables(tiles, rooms, floor_num, total_floors, rng, dungeon_id)

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
            # Spawn visible enemies on the floor
            self._spawn_floor_enemies(floor_num, rng)

    def _spawn_floor_enemies(self, floor_num, rng):
        """Place visible enemy entities on floor tiles."""
        floor = self.floors[floor_num]
        tiles = floor["tiles"]
        fw, fh = floor["width"], floor["height"]

        # Collect walkable floor tiles NOT near entrance/stairs
        entrance = floor.get("entrance", (0, 0))
        stairs_down = floor.get("stairs_down")
        avoid = set()
        for ax, ay in [entrance] + ([stairs_down] if stairs_down else []):
            for ddx in range(-3, 4):
                for ddy in range(-3, 4):
                    avoid.add((ax + ddx, ay + ddy))

        walkable = []
        for y in range(fh):
            for x in range(fw):
                if tiles[y][x]["type"] in (DT_FLOOR, DT_CORRIDOR) and (x, y) not in avoid:
                    walkable.append((x, y))

        if not walkable:
            floor["enemies"] = []
            return

        # Number of enemies scales with floor and encounter rate
        base_count = 3 + floor_num * 2
        count = min(base_count, len(walkable) // 8)

        # Get encounter keys for this floor
        from data.enemies import DUNGEON_ENCOUNTER_TABLES
        table = DUNGEON_ENCOUNTER_TABLES.get(self.dungeon_id, {})
        enc_keys = table.get(floor_num, table.get(1, ["tutorial"]))
        if isinstance(enc_keys, str):
            enc_keys = [enc_keys]

        enemies = []
        used_positions = set()
        for _ in range(count):
            attempts = 0
            while attempts < 20:
                pos = rng.choice(walkable)
                if pos not in used_positions:
                    used_positions.add(pos)
                    break
                attempts += 1
            else:
                continue

            enc_key = rng.choice(enc_keys)
            enemy = {
                "x": pos[0],
                "y": pos[1],
                "enc_key": enc_key,
                "state": "patrol",     # patrol, chase, dead
                "patrol_dir": rng.choice([(0, 1), (0, -1), (1, 0), (-1, 0)]),
                "move_cooldown": 0,    # skip turns between moves
                "alert_range": 5,      # detect player within this range
                "chase_speed": 1,      # moves per player move when chasing
            }
            enemies.append(enemy)

        floor["enemies"] = enemies

    def _move_enemies(self):
        """Move all enemies on current floor. Returns enemy if one touches party."""
        floor = self.floors[self.current_floor]
        enemies = floor.get("enemies", [])
        tiles = floor["tiles"]
        fw, fh = floor["width"], floor["height"]
        px, py = self.party_x, self.party_y

        # Build occupied set for enemy-enemy collision avoidance
        occupied = {(e["x"], e["y"]) for e in enemies if e["state"] != "dead"}

        for enemy in enemies:
            if enemy["state"] == "dead":
                continue

            # Cooldown
            if enemy["move_cooldown"] > 0:
                enemy["move_cooldown"] -= 1
                continue

            ex, ey = enemy["x"], enemy["y"]
            dist = abs(ex - px) + abs(ey - py)  # Manhattan distance

            if dist <= 1:
                # Adjacent or same tile — trigger combat
                return enemy

            if dist <= enemy["alert_range"]:
                # Chase — move toward player
                enemy["state"] = "chase"
                dx = 0 if px == ex else (1 if px > ex else -1)
                dy = 0 if py == ey else (1 if py > ey else -1)
                # Prefer axis with larger gap
                if abs(px - ex) >= abs(py - ey):
                    moves = [(dx, 0), (0, dy), (dx, dy)]
                else:
                    moves = [(0, dy), (dx, 0), (dx, dy)]
            else:
                # Patrol — wander
                enemy["state"] = "patrol"
                pdx, pdy = enemy["patrol_dir"]
                moves = [(pdx, pdy)]
                # Random direction change
                if random.random() < 0.2:
                    enemy["patrol_dir"] = random.choice(
                        [(0, 1), (0, -1), (1, 0), (-1, 0)])

            # Try each move
            moved = False
            for mdx, mdy in moves:
                if mdx == 0 and mdy == 0:
                    continue
                nx, ny = ex + mdx, ey + mdy
                if (0 <= nx < fw and 0 <= ny < fh and
                        tiles[ny][nx]["type"] in PASSABLE_TILES and
                        (nx, ny) not in occupied):
                    occupied.discard((ex, ey))
                    enemy["x"] = nx
                    enemy["y"] = ny
                    occupied.add((nx, ny))
                    moved = True
                    break

            if not moved and enemy["state"] == "patrol":
                # Reverse direction if blocked
                pdx, pdy = enemy["patrol_dir"]
                enemy["patrol_dir"] = (-pdx, -pdy)

            # Set cooldown (patrol is slower, chase is faster)
            enemy["move_cooldown"] = 1 if enemy["state"] == "chase" else 2

        return None  # no contact

    def get_floor_enemies(self):
        """Get list of living enemies on current floor."""
        floor = self.floors[self.current_floor]
        return [e for e in floor.get("enemies", []) if e["state"] != "dead"]

    def kill_enemy_at(self, x, y):
        """Mark enemy at position as dead (called after combat victory)."""
        floor = self.floors[self.current_floor]
        for e in floor.get("enemies", []):
            if e["x"] == x and e["y"] == y and e["state"] != "dead":
                e["state"] = "dead"
                return True
        return False

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
        elif tile.get("event") and tile["event"].get("type") == "interactable":
            if not tile["event"].get("used"):
                return {"type": "interactable", "data": tile["event"]}
        elif tile.get("event") and tile["event"].get("type") == "boss_encounter":
            if not tile["event"].get("triggered"):
                # Check if boss already resolved (e.g., Grak spared/defeated)
                from core.story_flags import get_flag
                boss_flag = f"boss.{self.dungeon_id.split('_')[0]}.defeated"
                # Grak-specific check
                if self.dungeon_id == "goblin_warren" and get_flag("boss.grak.defeated"):
                    tile["event"]["triggered"] = True
                    return None
                tile["event"]["triggered"] = True
                return {
                    "type": "random_encounter",
                    "dungeon_id": self.dungeon_id,
                    "floor": self.current_floor,
                    "total_floors": self.total_floors,
                    "is_boss": True,
                }

        # ── Visible enemy movement + collision ──
        contact = self._move_enemies()
        if contact:
            # Peace path check
            if self.dungeon_id == "goblin_warren":
                from core.story_flags import get_flag
                if get_flag("choice.grak_spared"):
                    return None  # goblins are friendly

            # Store contacted enemy position for post-combat cleanup
            self._last_contact_enemy = (contact["x"], contact["y"])
            return {
                "type": "random_encounter",
                "dungeon_id": self.dungeon_id,
                "floor": self.current_floor,
                "total_floors": self.total_floors,
                "is_boss": False,
                "_enc_key": contact["enc_key"],
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
            # NEVER return boss from random encounters — boss only spawns
            # from the placed boss_encounter event tile on the map
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
        Thief/Ranger get bonuses. Dwarves get racial bonus.
        Detection just reveals the trap; the trap still fires unless disarmed."""
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
            # Racial trap bonus (Dwarf)
            from core.races import get_passive
            trap_bonus = get_passive(getattr(c, "race_name", "Human"), "trap_detect_bonus", 0)
            detect_bonus += trap_bonus

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
        not raw party stats. Elves get racial bonus. Repeated rolls on each step nearby."""
        # Only class bonuses matter for secrets (not raw stat stacking)
        secret_bonus = 0
        for c in self.party:
            if c.class_name == "Thief":
                secret_bonus += 15 + c.level * 3
            elif c.class_name == "Ranger":
                secret_bonus += 8 + c.level * 2
            # Racial secret door bonus (Elf)
            from core.races import get_passive
            sd_bonus = get_passive(getattr(c, "race_name", "Human"), "secret_door_bonus", 0)
            secret_bonus += sd_bonus
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
