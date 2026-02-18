"""
Realm of Shadows — World Map Data (v2)

120×120 tile overworld generated from heightmap + moisture map.
Biomes follow geographic logic: mountains create rain shadows,
rivers flow downhill, terrain transitions are gradual.
"""
import random
import math

# ═══════════════════════════════════════════════════════════════
#  TERRAIN TYPES
# ═══════════════════════════════════════════════════════════════

T_GRASS        = "grass"
T_FOREST       = "forest"
T_DENSE_FOREST = "dense_forest"
T_MOUNTAIN     = "mountain"
T_HILL         = "hill"
T_SWAMP        = "swamp"
T_DESERT       = "desert"
T_SCRUBLAND    = "scrubland"
T_WATER        = "water"
T_LAKE         = "lake"
T_RIVER        = "river"
T_ROAD         = "road"
T_BRIDGE       = "bridge"
T_SHORE        = "shore"

TERRAIN_DATA = {
    T_GRASS:        {"name": "Grassland",     "passable": True,  "elevation": 1, "sight": 4, "encounter_rate": 15, "move_cost": 1},
    T_FOREST:       {"name": "Forest",        "passable": True,  "elevation": 1, "sight": 3, "encounter_rate": 12, "move_cost": 1},
    T_DENSE_FOREST: {"name": "Dense Forest",  "passable": True,  "elevation": 2, "sight": 2, "encounter_rate": 8,  "move_cost": 1},
    T_MOUNTAIN:     {"name": "Mountain",      "passable": False, "elevation": 3, "sight": 5, "encounter_rate": 0,  "move_cost": 0},
    T_HILL:         {"name": "Hills",         "passable": True,  "elevation": 2, "sight": 4, "encounter_rate": 12, "move_cost": 1},
    T_SWAMP:        {"name": "Swamp",         "passable": True,  "elevation": 0, "sight": 3, "encounter_rate": 6,  "move_cost": 1},
    T_DESERT:       {"name": "Desert",        "passable": True,  "elevation": 1, "sight": 5, "encounter_rate": 6,  "move_cost": 1},
    T_SCRUBLAND:    {"name": "Scrubland",     "passable": True,  "elevation": 1, "sight": 4, "encounter_rate": 10, "move_cost": 1},
    T_WATER:        {"name": "Ocean",         "passable": False, "elevation": 0, "sight": 5, "encounter_rate": 0,  "move_cost": 0},
    T_LAKE:         {"name": "Lake",          "passable": False, "elevation": 0, "sight": 4, "encounter_rate": 0,  "move_cost": 0},
    T_RIVER:        {"name": "River",         "passable": True,  "elevation": 0, "sight": 4, "encounter_rate": 18, "move_cost": 2},
    T_ROAD:         {"name": "Road",          "passable": True,  "elevation": 1, "sight": 4, "encounter_rate": 25, "move_cost": 1},
    T_BRIDGE:       {"name": "Bridge",        "passable": True,  "elevation": 1, "sight": 4, "encounter_rate": 20, "move_cost": 1},
    T_SHORE:        {"name": "Shore",         "passable": True,  "elevation": 0, "sight": 4, "encounter_rate": 18, "move_cost": 1},
}

IMPASSABLE = {T_MOUNTAIN, T_WATER, T_LAKE}
WATER_TILES = {T_WATER, T_LAKE, T_RIVER}

CAMP_AMBUSH_CHANCE = {
    T_ROAD: 5, T_GRASS: 10, T_SHORE: 8, T_HILL: 12,
    T_FOREST: 15, T_RIVER: 12, T_BRIDGE: 10,
    T_DENSE_FOREST: 25, T_SWAMP: 30, T_DESERT: 15,
    T_SCRUBLAND: 10, T_LAKE: 5,
}


# ═══════════════════════════════════════════════════════════════
#  LOCATIONS
# ═══════════════════════════════════════════════════════════════

LOC_TOWN    = "town"
LOC_DUNGEON = "dungeon"
LOC_POI     = "poi"
LOC_SECRET  = "secret"
LOC_PORT    = "port"
LOC_STABLE  = "stable"
LOC_RAIL    = "rail_station"

LOCATIONS = {
    # ── Briarhollow Region ──
    "briarhollow": {
        "name": "Briarhollow", "type": LOC_TOWN,
        "x": 60, "y": 70, "region": "briarhollow",
        "visible": True, "icon": "T",
        "description": "A quiet settlement at the edge of the wilds.",
        "has_stable": True, "has_teleport": True,
    },
    "briarhollow_dock": {
        "name": "Briarhollow Docks", "type": LOC_PORT,
        "x": 60, "y": 90, "region": "briarhollow",
        "visible": True, "icon": "P",
        "description": "A small dock on the southern coast.",
    },
    "goblin_warren": {
        "name": "Goblin Warren", "type": LOC_DUNGEON,
        "x": 55, "y": 66, "region": "briarhollow",
        "visible": True, "icon": "D",
        "description": "A cave system infested with goblins.",
        "encounter_key": "easy_goblins", "floors": 3, "difficulty": "easy",
        "required_key": None,
    },

    # ── Thornwood Region ──
    "woodhaven": {
        "name": "Woodhaven", "type": LOC_TOWN,
        "x": 28, "y": 50, "region": "thornwood",
        "visible": True, "icon": "T",
        "description": "A lumber town deep in the Thornwood.",
        "has_stable": True, "has_teleport": True,
    },
    "spiders_nest": {
        "name": "Spider's Nest", "type": LOC_DUNGEON,
        "x": 20, "y": 42, "region": "thornwood",
        "visible": False, "icon": "D",
        "description": "Thick webs cover the entrance to this dark cave.",
        "encounter_key": "wolves", "floors": 4, "difficulty": "medium",
        "required_key": "thornwood_map", "discovery_radius": 2,
    },
    "druids_grove": {
        "name": "Druid's Grove", "type": LOC_SECRET,
        "x": 18, "y": 58, "region": "thornwood",
        "visible": False, "icon": "?",
        "description": "An ancient grove humming with natural magic.",
        "discovery_radius": 1, "discovery_chance": 10,
    },

    # ── Iron Ridge Region ──
    "ironhearth": {
        "name": "Ironhearth", "type": LOC_TOWN,
        "x": 55, "y": 25, "region": "iron_ridge",
        "visible": True, "icon": "T",
        "description": "A fortress town built into the mountain face.",
        "has_stable": True, "has_teleport": True,
    },
    "abandoned_mine": {
        "name": "Abandoned Mine", "type": LOC_DUNGEON,
        "x": 65, "y": 20, "region": "iron_ridge",
        "visible": True, "icon": "D",
        "description": "An old mine that delves deep into the mountains.",
        "encounter_key": "hard_mixed", "floors": 5, "difficulty": "hard",
        "required_key": "mine_key",
    },

    # ── Ashlands Region ──
    "ruins_ashenmoor": {
        "name": "Ruins of Ashenmoor", "type": LOC_DUNGEON,
        "x": 95, "y": 40, "region": "ashlands",
        "visible": True, "icon": "D",
        "description": "Scorched ruins of a once-great city.",
        "encounter_key": "boss_orc", "floors": 4, "difficulty": "hard",
        "required_key": "ashenmoor_seal",
    },

    # ── Mirehollow Region ──
    "sunken_crypt": {
        "name": "Sunken Crypt", "type": LOC_DUNGEON,
        "x": 85, "y": 78, "region": "mirehollow",
        "visible": False, "icon": "D",
        "description": "Half-submerged ruins rising from the swamp.",
        "encounter_key": "medium_bandits", "floors": 4, "difficulty": "medium",
        "required_key": "crypt_amulet", "discovery_radius": 2,
    },

    # ── Pale Coast ──
    "pale_coast_dock": {
        "name": "Pale Coast Harbor", "type": LOC_PORT,
        "x": 35, "y": 88, "region": "pale_coast",
        "visible": True, "icon": "P",
        "description": "A weathered harbor on the southwestern coast.",
    },
    "smugglers_cove": {
        "name": "Smuggler's Cove", "type": LOC_SECRET,
        "x": 30, "y": 95, "region": "pale_coast",
        "visible": False, "icon": "?",
        "description": "A hidden cove used by smugglers and pirates.",
        "discovery_radius": 2, "discovery_chance": 12,
    },

    # ── Eastern Shore ──
    "eastern_dock": {
        "name": "Eastport", "type": LOC_PORT,
        "x": 100, "y": 60, "region": "ashlands",
        "visible": True, "icon": "P",
        "description": "A fortified port on the eastern coast.",
    },

    # ── Islands ──
    "windswept_isle": {
        "name": "Windswept Isle", "type": LOC_POI,
        "x": 45, "y": 108, "region": "ocean",
        "visible": False, "icon": "?",
        "description": "A storm-battered island with ancient ruins.",
        "discovery_radius": 3, "discovery_chance": 20,
    },
    "dragons_tooth": {
        "name": "Dragon's Tooth", "type": LOC_DUNGEON,
        "x": 112, "y": 55, "region": "ocean",
        "visible": False, "icon": "D",
        "description": "A volcanic island shaped like a fang.",
        "encounter_key": "boss_orc", "floors": 6, "difficulty": "legendary",
        "required_key": "dragon_scale", "discovery_radius": 3,
    },
}

# Port routes (which ports connect)
PORT_ROUTES = {
    "briarhollow_dock": ["pale_coast_dock", "windswept_isle"],
    "pale_coast_dock": ["briarhollow_dock", "windswept_isle"],
    "eastern_dock": ["dragons_tooth"],
}

# Magical rail connections
RAIL_STATIONS = ["briarhollow", "woodhaven", "ironhearth"]


# ═══════════════════════════════════════════════════════════════
#  ENCOUNTER ZONES
# ═══════════════════════════════════════════════════════════════

ENCOUNTER_ZONES = {
    "briarhollow": {
        "easy": ["tutorial", "easy_goblins"],
        "medium": ["medium_bandits", "wolves"],
    },
    "thornwood": {
        "easy": ["wolves"],
        "medium": ["medium_goblins", "wolves"],
        "hard": ["medium_bandits"],
    },
    "iron_ridge": {
        "medium": ["medium_bandits", "hard_mixed"],
        "hard": ["hard_mixed", "boss_orc"],
    },
    "ashlands": {
        "medium": ["hard_mixed"],
        "hard": ["boss_orc"],
    },
    "mirehollow": {
        "medium": ["medium_goblins", "medium_bandits"],
        "hard": ["hard_mixed"],
    },
    "pale_coast": {
        "easy": ["easy_goblins"],
        "medium": ["medium_bandits"],
    },
    "ocean": {
        "medium": ["medium_bandits"],
        "hard": ["hard_mixed"],
    },
}


def get_encounter_for_zone(region, difficulty_tier="easy"):
    zone = ENCOUNTER_ZONES.get(region, ENCOUNTER_ZONES.get("briarhollow", {}))
    for tier in [difficulty_tier, "medium", "easy"]:
        if tier in zone:
            return random.choice(zone[tier])
    return "tutorial"


# ═══════════════════════════════════════════════════════════════
#  MAP GENERATION — Heightmap + Moisture Based
# ═══════════════════════════════════════════════════════════════

MAP_W = 120
MAP_H = 120


def _noise_2d(x, y, seed, scale=0.05):
    """Simple value noise using hash. Returns 0.0-1.0."""
    # Multiple octaves of pseudo-random noise
    val = 0.0
    amp = 1.0
    freq = scale
    for _ in range(4):
        # Hash-based noise
        ix = int(x * freq * 1000 + seed * 7)
        iy = int(y * freq * 1000 + seed * 13)
        h = ((ix * 374761393 + iy * 668265263 + seed * 1274126177) & 0xFFFFFFFF)
        h = ((h ^ (h >> 13)) * 1103515245 + 12345) & 0xFFFFFFFF
        n = (h & 0xFFFF) / 65535.0
        val += n * amp
        amp *= 0.5
        freq *= 2.0
    return val / 1.875  # normalize


def _smooth_map(grid, w, h, passes=2):
    """Smooth a 2D float grid with neighbor averaging."""
    for _ in range(passes):
        new = [[0.0] * w for _ in range(h)]
        for y in range(h):
            for x in range(w):
                total = grid[y][x]
                count = 1
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        if dy == 0 and dx == 0:
                            continue
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < h and 0 <= nx < w:
                            total += grid[ny][nx]
                            count += 1
                new[y][x] = total / count
        grid = new
    return grid


def generate_world_map(seed=42):
    """Generate the overworld using heightmap + moisture."""
    rng = random.Random(seed)

    # ── Step 1: Generate heightmap ──
    height = [[0.0] * MAP_W for _ in range(MAP_H)]
    for y in range(MAP_H):
        for x in range(MAP_W):
            # Base noise
            h = _noise_2d(x, y, seed, scale=0.035)

            # Continental shape: higher in center, lower at edges
            cx, cy = MAP_W / 2, MAP_H / 2
            dist_edge = min(x, y, MAP_W - 1 - x, MAP_H - 1 - y) / 15.0
            dist_center = math.sqrt((x - cx) ** 2 + (y - cy) ** 2) / 60.0
            continent = max(0, 1.0 - dist_center) * 0.6
            edge_falloff = min(1.0, dist_edge)

            h = h * 0.5 + continent * 0.5
            h *= edge_falloff

            # Mountain ridges in north (Iron Ridge)
            if 15 < y < 40 and 40 < x < 80:
                ridge = max(0, 1.0 - abs(y - 28) / 12.0) * 0.35
                h += ridge * _noise_2d(x, y, seed + 100, 0.08)

            # Hills in west (Thornwood foothills)
            if 35 < y < 65 and 15 < x < 40:
                h += 0.1 * _noise_2d(x, y, seed + 200, 0.06)

            # Depression for Mirehollow swamp
            if 70 < y < 90 and 75 < x < 100:
                h -= 0.15

            height[y][x] = max(0, min(1, h))

    height = _smooth_map(height, MAP_W, MAP_H, passes=3)

    # ── Step 2: Generate moisture map ──
    moisture = [[0.0] * MAP_W for _ in range(MAP_H)]
    for y in range(MAP_H):
        for x in range(MAP_W):
            m = _noise_2d(x, y, seed + 500, scale=0.04)

            # More moisture near coasts (west and south)
            coast_west = max(0, 1.0 - x / 30.0) * 0.3
            coast_south = max(0, 1.0 - (MAP_H - 1 - y) / 25.0) * 0.2
            m += coast_west + coast_south

            # Rain shadow: east of mountains is dry (Ashlands)
            if x > 70 and 20 < y < 50:
                m -= 0.3

            # Wet: Mirehollow swamp
            if 70 < y < 90 and 75 < x < 100:
                m += 0.3

            # Wet: Thornwood
            if 35 < y < 65 and 15 < x < 40:
                m += 0.2

            moisture[y][x] = max(0, min(1, m))

    moisture = _smooth_map(moisture, MAP_W, MAP_H, passes=2)

    # ── Step 3: Assign biomes ──
    tiles = [[None] * MAP_W for _ in range(MAP_H)]
    sea_level = 0.28

    for y in range(MAP_H):
        for x in range(MAP_W):
            h = height[y][x]
            m = moisture[y][x]

            if h < sea_level:
                terrain = T_WATER
            elif h < sea_level + 0.03:
                terrain = T_SHORE
            elif h > 0.58:
                terrain = T_MOUNTAIN
            elif h > 0.50:
                terrain = T_HILL
            elif m > 0.7 and h < 0.4:
                terrain = T_SWAMP
            elif m > 0.65:
                terrain = T_DENSE_FOREST
            elif m > 0.50:
                terrain = T_FOREST
            elif m < 0.25:
                terrain = T_DESERT
            elif m < 0.35:
                terrain = T_SCRUBLAND
            else:
                terrain = T_GRASS

            # Assign region
            region = _get_region(x, y)

            tiles[y][x] = {
                "terrain": terrain,
                "region": region,
                "discovered": False,
                "location_id": None,
                "height": h,
                "moisture": m,
            }

    # ── Step 4: Biome transition smoothing ──
    _smooth_biome_transitions(tiles)

    # ── Step 5: Rivers ──
    _generate_rivers(tiles, height, rng, count=5)

    # ── Step 6: Lakes ──
    _generate_lakes(tiles, height, rng, count=4)

    # ── Step 7: Islands ──
    _generate_islands(tiles, rng)

    # ── Step 8: Shore pass (land next to water) ──
    _update_shores(tiles)

    # ── Step 9: Place locations ──
    for loc_id, loc in LOCATIONS.items():
        lx, ly = loc["x"], loc["y"]
        if 0 <= lx < MAP_W and 0 <= ly < MAP_H:
            tiles[ly][lx]["location_id"] = loc_id
            if tiles[ly][lx]["terrain"] in IMPASSABLE:
                tiles[ly][lx]["terrain"] = T_GRASS
            if loc["type"] == LOC_TOWN:
                tiles[ly][lx]["terrain"] = T_ROAD

    # ── Step 10: Roads between towns ──
    town_pairs = [
        ("briarhollow", "woodhaven"),
        ("briarhollow", "ironhearth"),
        ("briarhollow", "briarhollow_dock"),
        ("briarhollow", "pale_coast_dock"),
        ("briarhollow", "goblin_warren"),
        ("woodhaven", "ironhearth"),
    ]
    for a, b in town_pairs:
        if a in LOCATIONS and b in LOCATIONS:
            _carve_road(tiles, LOCATIONS[a]["x"], LOCATIONS[a]["y"],
                        LOCATIONS[b]["x"], LOCATIONS[b]["y"], rng)

    # ── Step 11: Clear and discover starting area ──
    sx, sy = LOCATIONS["briarhollow"]["x"], LOCATIONS["briarhollow"]["y"]
    for dy in range(-7, 8):
        for dx in range(-7, 8):
            ny, nx = sy + dy, sx + dx
            if 0 <= ny < MAP_H and 0 <= nx < MAP_W:
                if tiles[ny][nx]["terrain"] in IMPASSABLE:
                    if abs(dy) <= 4 and abs(dx) <= 4:
                        tiles[ny][nx]["terrain"] = T_GRASS
                tiles[ny][nx]["discovered"] = True

    return tiles


def _get_region(x, y):
    """Assign region based on coordinates."""
    regions = {
        "briarhollow": (60, 70, 20),
        "thornwood":   (25, 50, 22),
        "iron_ridge":  (55, 28, 20),
        "ashlands":    (92, 40, 22),
        "mirehollow":  (85, 80, 18),
        "pale_coast":  (35, 88, 16),
    }
    best = "briarhollow"
    best_d = 9999
    for name, (cx, cy, _) in regions.items():
        d = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        if d < best_d:
            best_d = d
            best = name
    return best


def _smooth_biome_transitions(tiles):
    """Fix forbidden adjacencies by inserting transition biomes."""
    forbidden = {
        (T_DESERT, T_FOREST): T_SCRUBLAND,
        (T_DESERT, T_DENSE_FOREST): T_SCRUBLAND,
        (T_FOREST, T_DESERT): T_SCRUBLAND,
        (T_DENSE_FOREST, T_DESERT): T_SCRUBLAND,
        (T_DESERT, T_SWAMP): T_SCRUBLAND,
        (T_SWAMP, T_DESERT): T_GRASS,
    }

    for _pass in range(3):
        changes = []
        for y in range(MAP_H):
            for x in range(MAP_W):
                t = tiles[y][x]["terrain"]
                if t in IMPASSABLE or t in (T_ROAD, T_BRIDGE, T_RIVER):
                    continue
                for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < MAP_H and 0 <= nx < MAP_W:
                        nt = tiles[ny][nx]["terrain"]
                        pair = (t, nt)
                        if pair in forbidden:
                            changes.append((y, x, forbidden[pair]))
                            break
        for cy, cx, new_t in changes:
            tiles[cy][cx]["terrain"] = new_t


def _generate_rivers(tiles, height, rng, count=5):
    """Generate rivers flowing from high to low terrain."""
    # Find highest land tiles as sources
    sources = []
    for y in range(10, MAP_H - 10):
        for x in range(10, MAP_W - 10):
            h = height[y][x]
            t = tiles[y][x]["terrain"]
            if t in (T_HILL, T_MOUNTAIN) or (h > 0.48 and t not in (T_WATER, T_LAKE)):
                sources.append((x, y, h))

    # Sort by height descending, pick from top
    sources.sort(key=lambda s: -s[2])
    rng.shuffle(sources[:30])  # randomize among top 30 highest
    rivers_made = 0

    for sx, sy, sh in sources:
        if rivers_made >= count:
            break

        # Flow downhill
        path = []
        x, y = sx, sy
        visited = set()
        for _ in range(200):
            if (x, y) in visited:
                break
            visited.add((x, y))

            if tiles[y][x]["terrain"] in (T_WATER, T_LAKE):
                break  # reached water

            path.append((x, y))

            # Find lowest neighbor
            best_h = height[y][x]
            best_pos = None
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ny, nx = y + dy, x + dx
                if 0 <= ny < MAP_H and 0 <= nx < MAP_W:
                    nh = height[ny][nx]
                    if nh < best_h:
                        best_h = nh
                        best_pos = (nx, ny)

            if best_pos is None:
                # Stuck — add random walk toward edge
                x += rng.choice([-1, 0, 1])
                y += 1  # bias southward (toward coast)
                x = max(0, min(MAP_W - 1, x))
                y = max(0, min(MAP_H - 1, y))
            else:
                x, y = best_pos

        if len(path) > 8:
            for rx, ry in path:
                if tiles[ry][rx]["terrain"] == T_ROAD:
                    tiles[ry][rx]["terrain"] = T_BRIDGE
                elif tiles[ry][rx]["terrain"] not in (T_WATER, T_BRIDGE):
                    tiles[ry][rx]["terrain"] = T_RIVER
            rivers_made += 1


def _generate_lakes(tiles, height, rng, count=4):
    """Place lakes in low-elevation areas."""
    candidates = []
    for y in range(15, MAP_H - 15):
        for x in range(15, MAP_W - 15):
            h = height[y][x]
            if 0.30 < h < 0.40 and tiles[y][x]["terrain"] not in (T_WATER, T_RIVER):
                candidates.append((x, y, h))

    rng.shuffle(candidates)
    lakes_made = 0

    for lx, ly, _ in candidates:
        if lakes_made >= count:
            break
        # Check not too close to another lake
        too_close = False
        for dy in range(-8, 9):
            for dx in range(-8, 9):
                ny, nx = ly + dy, lx + dx
                if 0 <= ny < MAP_H and 0 <= nx < MAP_W:
                    if tiles[ny][nx]["terrain"] == T_LAKE:
                        too_close = True
                        break
            if too_close:
                break
        if too_close:
            continue

        # Create lake blob
        size = rng.randint(3, 6)
        for dy in range(-size, size + 1):
            for dx in range(-size, size + 1):
                ny, nx = ly + dy, lx + dx
                if 0 <= ny < MAP_H and 0 <= nx < MAP_W:
                    dist = math.sqrt(dx * dx + dy * dy)
                    if dist < size + rng.uniform(-1, 1):
                        if tiles[ny][nx]["terrain"] not in (T_ROAD, T_BRIDGE):
                            tiles[ny][nx]["terrain"] = T_LAKE
        lakes_made += 1


def _generate_islands(tiles, rng):
    """Create small islands off the coast."""
    island_specs = [
        (45, 108, 5, "Windswept Isle"),
        (112, 55, 4, "Dragon's Tooth"),
        (15, 105, 3, "Hermit's Rock"),
    ]
    for ix, iy, size, name in island_specs:
        for dy in range(-size, size + 1):
            for dx in range(-size, size + 1):
                ny, nx = iy + dy, ix + dx
                if 0 <= ny < MAP_H and 0 <= nx < MAP_W:
                    dist = math.sqrt(dx * dx + dy * dy)
                    if dist < size + rng.uniform(-1, 0.5):
                        if dist < size - 1:
                            tiles[ny][nx]["terrain"] = T_GRASS
                        else:
                            tiles[ny][nx]["terrain"] = T_SHORE
                        tiles[ny][nx]["region"] = "ocean"


def _update_shores(tiles):
    """Ensure land tiles adjacent to water become shore."""
    for y in range(MAP_H):
        for x in range(MAP_W):
            t = tiles[y][x]["terrain"]
            if t in (T_WATER, T_LAKE, T_RIVER, T_SHORE, T_ROAD, T_BRIDGE, T_MOUNTAIN):
                continue
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ny, nx = y + dy, x + dx
                if 0 <= ny < MAP_H and 0 <= nx < MAP_W:
                    if tiles[ny][nx]["terrain"] in (T_WATER, T_LAKE):
                        tiles[y][x]["terrain"] = T_SHORE
                        break


def _carve_road(tiles, x1, y1, x2, y2, rng):
    """Carve road between two points, avoiding water/mountains."""
    x, y = x1, y1
    for _ in range(300):
        if x == x2 and y == y2:
            break
        if 0 <= y < MAP_H and 0 <= x < MAP_W:
            t = tiles[y][x]["terrain"]
            if t == T_RIVER:
                tiles[y][x]["terrain"] = T_BRIDGE
            elif t not in (T_WATER, T_LAKE, T_MOUNTAIN, T_BRIDGE):
                tiles[y][x]["terrain"] = T_ROAD

        dx = 1 if x2 > x else -1 if x2 < x else 0
        dy = 1 if y2 > y else -1 if y2 < y else 0

        if rng.random() < 0.65:
            if abs(x2 - x) > abs(y2 - y):
                x += dx
            else:
                y += dy
        else:
            if rng.random() < 0.5:
                x += dx
            else:
                y += dy
        x = max(0, min(MAP_W - 1, x))
        y = max(0, min(MAP_H - 1, y))


# ═══════════════════════════════════════════════════════════════
#  TRAVEL STATE
# ═══════════════════════════════════════════════════════════════

class TravelState:
    """Tracks travel mode and owned vehicles."""
    def __init__(self):
        self.has_horse = False
        self.has_boat = False       # owns sailing ship
        self.has_carpet = False
        self.travel_mode = "walk"   # walk, horse, carpet
        self.boat_location = None   # port ID where boat is docked
        self.attuned_circles = []   # town IDs with active teleport
        self.rail_unlocked = False

    def get_move_speed(self, terrain):
        """Return tiles per move based on mode and terrain."""
        if self.travel_mode == "carpet":
            return 3  # flies over everything
        elif self.travel_mode == "horse":
            if terrain in (T_ROAD, T_GRASS, T_SHORE, T_SCRUBLAND):
                return 2
            elif terrain in (T_DENSE_FOREST, T_SWAMP, T_MOUNTAIN):
                return 0  # can't ride here
            else:
                return 1
        return 1  # walking

    def can_ride_terrain(self, terrain):
        """Check if horse can enter this terrain."""
        return terrain not in (T_DENSE_FOREST, T_SWAMP, T_MOUNTAIN, T_WATER, T_LAKE)


# ═══════════════════════════════════════════════════════════════
#  WORLD STATE
# ═══════════════════════════════════════════════════════════════

class WorldState:
    """Tracks party position, world map, travel, and discovery."""

    def __init__(self, party, seed=42):
        self.party = party
        self.tiles = generate_world_map(seed)
        self.discovered_locations = set()
        self.travel = TravelState()
        self.key_items = []  # list of key item ID strings

        start = LOCATIONS["briarhollow"]
        self.party_x = start["x"]
        self.party_y = start["y"]
        self.step_counter = 0

        self._update_fog()
        for loc_id, loc in LOCATIONS.items():
            if loc.get("visible"):
                self.discovered_locations.add(loc_id)

    def has_key(self, key_id):
        return key_id in self.key_items

    def add_key(self, key_id):
        if key_id not in self.key_items:
            self.key_items.append(key_id)

    def move(self, dx, dy):
        """Move party. Returns event dict or None."""
        nx = self.party_x + dx
        ny = self.party_y + dy

        if nx < 0 or nx >= MAP_W or ny < 0 or ny >= MAP_H:
            return {"type": "blocked"}

        tile = self.tiles[ny][nx]
        terrain = tile["terrain"]
        tdata = TERRAIN_DATA[terrain]

        # Carpet flies over anything
        if self.travel.travel_mode == "carpet":
            pass  # always passable
        elif not tdata["passable"]:
            return {"type": "blocked"}
        elif self.travel.travel_mode == "horse" and not self.travel.can_ride_terrain(terrain):
            return {"type": "blocked", "reason": "horse_terrain"}

        # Multi-tile movement for fast travel
        speed = self.travel.get_move_speed(terrain)
        if speed <= 0:
            return {"type": "blocked", "reason": "horse_terrain"}

        # Move (for now, always 1 tile — speed affects encounter rate)
        self.party_x = nx
        self.party_y = ny
        self._update_fog()

        # Location check
        loc_id = tile.get("location_id")
        if loc_id and loc_id in LOCATIONS:
            loc = LOCATIONS[loc_id]
            if loc_id not in self.discovered_locations:
                self.discovered_locations.add(loc_id)
                return {"type": "discovery", "id": loc_id, "data": loc}
            return {"type": "location", "id": loc_id, "data": loc}

        # Hidden discovery
        discovery = self._check_nearby_discoveries()
        if discovery:
            return discovery

        # Encounter check (reduced by speed)
        self.step_counter += 1
        enc_rate = tdata["encounter_rate"]
        if speed > 1:
            enc_rate = int(enc_rate * 1.5)  # faster = fewer encounters

        if enc_rate > 0 and self.step_counter >= random.randint(max(1, enc_rate - 3), enc_rate + 3):
            self.step_counter = 0
            region = tile["region"]
            dist = math.sqrt((nx - 60) ** 2 + (ny - 70) ** 2)
            tier = "easy" if dist < 15 else "medium" if dist < 35 else "hard"
            enc_key = get_encounter_for_zone(region, tier)
            return {"type": "encounter", "key": enc_key}

        return None

    def camp(self):
        """Rest the party. Returns event dict."""
        tile = self.tiles[self.party_y][self.party_x]
        terrain = tile["terrain"]
        region = tile["region"]

        ambush_chance = CAMP_AMBUSH_CHANCE.get(terrain, 10)
        for c in self.party:
            if c.class_name == "Ranger":
                ambush_chance = max(0, ambush_chance - 5)
            if c.class_name == "Cleric":
                ambush_chance = max(0, ambush_chance - 3)

        if random.randint(1, 100) <= ambush_chance:
            enc_key = get_encounter_for_zone(region, "easy")
            return {"type": "camp_ambush", "key": enc_key}

        healed = {}
        from core.classes import get_all_resources
        for c in self.party:
            max_res = get_all_resources(c.class_name, c.stats, c.level)
            old_hp = c.resources.get("HP", 0)
            max_hp = max_res.get("HP", 1)
            heal_hp = int(max_hp * 0.25)
            c.resources["HP"] = min(max_hp, old_hp + heal_hp)
            for res_name in c.resources:
                if res_name == "HP":
                    continue
                max_val = max_res.get(res_name, 0)
                c.resources[res_name] = min(max_val, c.resources[res_name] + int(max_val * 0.15))
            healed[c.name] = c.resources["HP"] - old_hp

        return {"type": "camp_safe", "healed": healed}

    def can_enter_dungeon(self, loc_id):
        """Check if party can enter a dungeon. Returns (can_enter, reason)."""
        loc = LOCATIONS.get(loc_id)
        if not loc:
            return False, "Unknown location"
        req = loc.get("required_key")
        if req and not self.has_key(req):
            key_name = req.replace("_", " ").title()
            return False, f"Requires: {key_name}"
        return True, "OK"

    def get_tile(self, x, y):
        if 0 <= x < MAP_W and 0 <= y < MAP_H:
            return self.tiles[y][x]
        return None

    def get_current_tile(self):
        return self.tiles[self.party_y][self.party_x]

    def get_current_region(self):
        return self.get_current_tile()["region"]

    def _update_fog(self):
        tile = self.tiles[self.party_y][self.party_x]
        terrain = tile["terrain"]
        sight = TERRAIN_DATA.get(terrain, {}).get("sight", 4)
        for dy in range(-sight, sight + 1):
            for dx in range(-sight, sight + 1):
                nx = self.party_x + dx
                ny = self.party_y + dy
                if 0 <= nx < MAP_W and 0 <= ny < MAP_H:
                    if math.sqrt(dx * dx + dy * dy) <= sight:
                        self.tiles[ny][nx]["discovered"] = True

    def _check_nearby_discoveries(self):
        for loc_id, loc in LOCATIONS.items():
            if loc_id in self.discovered_locations:
                continue
            if loc.get("visible"):
                continue
            lx, ly = loc["x"], loc["y"]
            dist = abs(self.party_x - lx) + abs(self.party_y - ly)
            if dist <= loc.get("discovery_radius", 2):
                base_chance = loc.get("discovery_chance", 15)
                for c in self.party:
                    if c.class_name == "Thief":
                        base_chance += 10
                    elif c.class_name == "Ranger":
                        base_chance += 10
                    elif c.class_name == "Mage":
                        base_chance += 5
                if random.randint(1, 100) <= base_chance:
                    self.discovered_locations.add(loc_id)
                    return {"type": "discovery", "id": loc_id, "data": loc}
        return None

    def get_visible_tiles(self, view_w=22, view_h=16):
        half_w = view_w // 2
        half_h = view_h // 2
        result = []
        for vy in range(view_h):
            row = []
            for vx in range(view_w):
                wx = self.party_x - half_w + vx
                wy = self.party_y - half_h + vy
                if 0 <= wx < MAP_W and 0 <= wy < MAP_H:
                    tile = self.tiles[wy][wx]
                    row.append({
                        "wx": wx, "wy": wy,
                        "terrain": tile["terrain"],
                        "discovered": tile["discovered"],
                        "location_id": tile["location_id"],
                        "region": tile["region"],
                        "is_party": (wx == self.party_x and wy == self.party_y),
                    })
                else:
                    row.append(None)
            result.append(row)
        return result
