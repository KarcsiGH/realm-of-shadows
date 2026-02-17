"""
Realm of Shadows — World Map Data

120×120 tile overworld with terrain types, regions, encounter zones,
and discoverable locations. Procedurally generated with hand-placed landmarks.
"""
import random
import math

# ═══════════════════════════════════════════════════════════════
#  TERRAIN TYPES
# ═══════════════════════════════════════════════════════════════

# Terrain constants
T_GRASS        = "grass"
T_FOREST       = "forest"
T_DENSE_FOREST = "dense_forest"
T_MOUNTAIN     = "mountain"
T_HILL         = "hill"
T_SWAMP        = "swamp"
T_DESERT       = "desert"
T_WATER        = "water"
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
    T_WATER:        {"name": "Ocean",         "passable": False, "elevation": 0, "sight": 5, "encounter_rate": 0,  "move_cost": 0},
    T_RIVER:        {"name": "River",         "passable": True,  "elevation": 0, "sight": 4, "encounter_rate": 18, "move_cost": 2},
    T_ROAD:         {"name": "Road",          "passable": True,  "elevation": 1, "sight": 4, "encounter_rate": 25, "move_cost": 1},
    T_BRIDGE:       {"name": "Bridge",        "passable": True,  "elevation": 1, "sight": 4, "encounter_rate": 20, "move_cost": 1},
    T_SHORE:        {"name": "Shore",         "passable": True,  "elevation": 0, "sight": 4, "encounter_rate": 18, "move_cost": 1},
}

IMPASSABLE = {T_MOUNTAIN, T_WATER}

# Camp ambush chances per terrain
CAMP_AMBUSH_CHANCE = {
    T_ROAD: 5, T_GRASS: 10, T_SHORE: 8, T_HILL: 12,
    T_FOREST: 15, T_RIVER: 12, T_BRIDGE: 10,
    T_DENSE_FOREST: 25, T_SWAMP: 30, T_DESERT: 15,
}


# ═══════════════════════════════════════════════════════════════
#  LOCATIONS (Towns, Dungeons, POIs)
# ═══════════════════════════════════════════════════════════════

# Location type constants
LOC_TOWN    = "town"
LOC_DUNGEON = "dungeon"
LOC_POI     = "poi"      # point of interest
LOC_SECRET  = "secret"   # hidden, must discover

LOCATIONS = {
    "briarhollow": {
        "name": "Briarhollow",
        "type": LOC_TOWN,
        "x": 60, "y": 75,
        "region": "briarhollow",
        "visible": True,  # always visible on map
        "description": "A quiet settlement at the edge of the wilds.",
        "icon": "T",
    },
    "goblin_warren": {
        "name": "Goblin Warren",
        "type": LOC_DUNGEON,
        "x": 50, "y": 65,
        "region": "briarhollow",
        "visible": True,
        "description": "A cave system infested with goblins.",
        "icon": "D",
        "encounter_key": "easy_goblins",
        "floors": 3,
        "difficulty": "easy",
    },
    "woodhaven": {
        "name": "Woodhaven",
        "type": LOC_TOWN,
        "x": 30, "y": 50,
        "region": "thornwood",
        "visible": True,
        "description": "A lumber town deep in the Thornwood.",
        "icon": "T",
    },
    "spiders_nest": {
        "name": "Spider's Nest",
        "type": LOC_DUNGEON,
        "x": 22, "y": 42,
        "region": "thornwood",
        "visible": False,
        "discovery_radius": 2,
        "description": "Thick webs cover the entrance to this dark cave.",
        "icon": "D",
        "encounter_key": "wolves",
        "floors": 4,
        "difficulty": "medium",
    },
    "druids_grove": {
        "name": "Druid's Grove",
        "type": LOC_SECRET,
        "x": 18, "y": 55,
        "region": "thornwood",
        "visible": False,
        "discovery_radius": 1,
        "discovery_chance": 10,
        "description": "An ancient grove humming with natural magic.",
        "icon": "?",
    },
    "ironhearth": {
        "name": "Ironhearth",
        "type": LOC_TOWN,
        "x": 55, "y": 25,
        "region": "iron_ridge",
        "visible": True,
        "description": "A fortress town built into the mountain face.",
        "icon": "T",
    },
    "abandoned_mine": {
        "name": "Abandoned Mine",
        "type": LOC_DUNGEON,
        "x": 65, "y": 20,
        "region": "iron_ridge",
        "visible": True,
        "description": "An old mine that delves deep into the mountains.",
        "icon": "D",
        "encounter_key": "hard_mixed",
        "floors": 5,
        "difficulty": "hard",
    },
    "smugglers_cove": {
        "name": "Smuggler's Cove",
        "type": LOC_SECRET,
        "x": 70, "y": 95,
        "region": "pale_coast",
        "visible": False,
        "discovery_radius": 2,
        "discovery_chance": 12,
        "description": "A hidden cove used by smugglers and pirates.",
        "icon": "?",
    },
    "sunken_crypt": {
        "name": "Sunken Crypt",
        "type": LOC_DUNGEON,
        "x": 85, "y": 80,
        "region": "mirehollow",
        "visible": False,
        "discovery_radius": 2,
        "description": "Half-submerged ruins rising from the swamp.",
        "icon": "D",
        "encounter_key": "medium_bandits",
        "floors": 4,
        "difficulty": "medium",
    },
    "ruins_ashenmoor": {
        "name": "Ruins of Ashenmoor",
        "type": LOC_DUNGEON,
        "x": 95, "y": 40,
        "region": "ashlands",
        "visible": True,
        "description": "Scorched ruins of a once-great city.",
        "icon": "D",
        "encounter_key": "boss_orc",
        "floors": 4,
        "difficulty": "hard",
    },
}


# ═══════════════════════════════════════════════════════════════
#  ENCOUNTER ZONES — maps region names to encounter tables
# ═══════════════════════════════════════════════════════════════

ENCOUNTER_ZONES = {
    "briarhollow": {
        "easy":   ["tutorial", "easy_goblins"],
        "medium": ["medium_bandits", "wolves"],
    },
    "thornwood": {
        "easy":   ["wolves"],
        "medium": ["medium_goblins", "wolves"],
        "hard":   ["medium_bandits"],
    },
    "iron_ridge": {
        "medium": ["medium_bandits", "hard_mixed"],
        "hard":   ["hard_mixed", "boss_orc"],
    },
    "ashlands": {
        "medium": ["hard_mixed"],
        "hard":   ["boss_orc"],
    },
    "mirehollow": {
        "medium": ["medium_goblins", "medium_bandits"],
        "hard":   ["hard_mixed"],
    },
    "pale_coast": {
        "easy":   ["easy_goblins"],
        "medium": ["medium_bandits"],
    },
}


def get_encounter_for_zone(region, difficulty_tier="easy"):
    """Pick a random encounter key for a region and difficulty."""
    zone = ENCOUNTER_ZONES.get(region, {})
    # Try requested tier, fall back to easier
    for tier in [difficulty_tier, "medium", "easy"]:
        if tier in zone:
            return random.choice(zone[tier])
    # Fallback
    return "tutorial"


# ═══════════════════════════════════════════════════════════════
#  MAP GENERATION
# ═══════════════════════════════════════════════════════════════

MAP_W = 120
MAP_H = 120


def generate_world_map(seed=42):
    """Generate the overworld map. Returns a 2D list of tile dicts."""
    rng = random.Random(seed)

    # Initialize all as water
    tiles = [[None for _ in range(MAP_W)] for _ in range(MAP_H)]
    for y in range(MAP_H):
        for x in range(MAP_W):
            tiles[y][x] = {
                "terrain": T_WATER,
                "region": "ocean",
                "discovered": False,
                "location_id": None,
            }

    # ── Step 1: Carve landmass using noise-like blobs ──
    # Create continent shape with overlapping circles
    land_centers = [
        (60, 60, 45),   # main continent center
        (40, 50, 30),   # western bulge
        (80, 55, 28),   # eastern bulge
        (55, 30, 25),   # northern reach
        (65, 85, 22),   # southern peninsula
        (30, 65, 18),   # western peninsula
        (90, 70, 18),   # eastern peninsula
    ]

    for y in range(MAP_H):
        for x in range(MAP_W):
            for cx, cy, radius in land_centers:
                dist = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
                # Add noise to edge
                noise = rng.uniform(-5, 5)
                if dist < radius + noise:
                    tiles[y][x]["terrain"] = T_GRASS
                    tiles[y][x]["region"] = "briarhollow"  # default, overridden below
                    break

    # ── Step 2: Paint regions ──
    region_centers = {
        "briarhollow": (60, 75, 20),
        "thornwood":   (28, 50, 22),
        "iron_ridge":  (55, 25, 22),
        "ashlands":    (92, 40, 20),
        "mirehollow":  (85, 78, 18),
        "pale_coast":  (65, 95, 15),
    }

    for y in range(MAP_H):
        for x in range(MAP_W):
            if tiles[y][x]["terrain"] == T_WATER:
                continue
            # Assign to nearest region
            best_region = "briarhollow"
            best_dist = 9999
            for reg, (cx, cy, _) in region_centers.items():
                d = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
                if d < best_dist:
                    best_dist = d
                    best_region = reg
            tiles[y][x]["region"] = best_region

    # ── Step 3: Paint terrain by region ──
    for y in range(MAP_H):
        for x in range(MAP_W):
            t = tiles[y][x]
            if t["terrain"] == T_WATER:
                continue

            region = t["region"]
            r = rng.random()

            if region == "briarhollow":
                if r < 0.60:
                    t["terrain"] = T_GRASS
                elif r < 0.80:
                    t["terrain"] = T_FOREST
                elif r < 0.90:
                    t["terrain"] = T_HILL
                else:
                    t["terrain"] = T_DENSE_FOREST

            elif region == "thornwood":
                if r < 0.15:
                    t["terrain"] = T_GRASS
                elif r < 0.50:
                    t["terrain"] = T_FOREST
                elif r < 0.80:
                    t["terrain"] = T_DENSE_FOREST
                else:
                    t["terrain"] = T_HILL

            elif region == "iron_ridge":
                if r < 0.15:
                    t["terrain"] = T_GRASS
                elif r < 0.35:
                    t["terrain"] = T_HILL
                elif r < 0.60:
                    t["terrain"] = T_MOUNTAIN
                elif r < 0.80:
                    t["terrain"] = T_HILL
                else:
                    t["terrain"] = T_FOREST

            elif region == "ashlands":
                if r < 0.70:
                    t["terrain"] = T_DESERT
                elif r < 0.85:
                    t["terrain"] = T_HILL
                else:
                    t["terrain"] = T_MOUNTAIN

            elif region == "mirehollow":
                if r < 0.50:
                    t["terrain"] = T_SWAMP
                elif r < 0.70:
                    t["terrain"] = T_FOREST
                elif r < 0.85:
                    t["terrain"] = T_DENSE_FOREST
                else:
                    t["terrain"] = T_GRASS

            elif region == "pale_coast":
                if r < 0.50:
                    t["terrain"] = T_GRASS
                elif r < 0.70:
                    t["terrain"] = T_SHORE
                elif r < 0.85:
                    t["terrain"] = T_FOREST
                else:
                    t["terrain"] = T_HILL

    # ── Step 4: Shore tiles (land adjacent to water) ──
    for y in range(1, MAP_H - 1):
        for x in range(1, MAP_W - 1):
            if tiles[y][x]["terrain"] == T_WATER:
                continue
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ny, nx = y + dy, x + dx
                if 0 <= ny < MAP_H and 0 <= nx < MAP_W:
                    if tiles[ny][nx]["terrain"] == T_WATER:
                        if tiles[y][x]["terrain"] in (T_GRASS, T_FOREST):
                            tiles[y][x]["terrain"] = T_SHORE
                        break

    # ── Step 5: Roads between towns ──
    town_positions = [(loc["x"], loc["y"]) for loc in LOCATIONS.values() if loc["type"] == LOC_TOWN]
    # Connect towns with simple roads (A* would be better, but L-shaped paths work)
    road_pairs = [
        ("briarhollow", "woodhaven"),
        ("briarhollow", "ironhearth"),
        ("briarhollow", "smugglers_cove"),  # road toward coast
    ]
    for loc_a, loc_b in road_pairs:
        if loc_a in LOCATIONS and loc_b in LOCATIONS:
            ax, ay = LOCATIONS[loc_a]["x"], LOCATIONS[loc_a]["y"]
            bx, by = LOCATIONS[loc_b]["x"], LOCATIONS[loc_b]["y"]
            _carve_road(tiles, ax, ay, bx, by, rng)

    # ── Step 6: Rivers ──
    _carve_river(tiles, 45, 10, 45, 90, rng, "ns")   # North-south river
    _carve_river(tiles, 70, 60, 100, 60, rng, "ew")   # East river

    # ── Step 7: Place locations ──
    for loc_id, loc in LOCATIONS.items():
        lx, ly = loc["x"], loc["y"]
        if 0 <= lx < MAP_W and 0 <= ly < MAP_H:
            tiles[ly][lx]["location_id"] = loc_id
            # Ensure location tiles are passable
            if tiles[ly][lx]["terrain"] in IMPASSABLE:
                tiles[ly][lx]["terrain"] = T_GRASS
            # Towns get road terrain
            if loc["type"] == LOC_TOWN:
                tiles[ly][lx]["terrain"] = T_ROAD

    # ── Step 8: Clear area around starting town ──
    sx, sy = LOCATIONS["briarhollow"]["x"], LOCATIONS["briarhollow"]["y"]
    for dy in range(-3, 4):
        for dx in range(-3, 4):
            ny, nx = sy + dy, sx + dx
            if 0 <= ny < MAP_H and 0 <= nx < MAP_W:
                if tiles[ny][nx]["terrain"] in IMPASSABLE:
                    tiles[ny][nx]["terrain"] = T_GRASS
                # Discover starting area
                tiles[ny][nx]["discovered"] = True

    return tiles


def _carve_road(tiles, x1, y1, x2, y2, rng):
    """Carve a winding road between two points."""
    x, y = x1, y1
    while x != x2 or y != y2:
        if 0 <= y < MAP_H and 0 <= x < MAP_W:
            if tiles[y][x]["terrain"] not in (T_WATER,):
                if tiles[y][x]["terrain"] == T_RIVER:
                    tiles[y][x]["terrain"] = T_BRIDGE
                elif tiles[y][x]["terrain"] != T_BRIDGE:
                    tiles[y][x]["terrain"] = T_ROAD

        # Move toward target with slight wander
        dx = 1 if x2 > x else -1 if x2 < x else 0
        dy = 1 if y2 > y else -1 if y2 < y else 0

        if rng.random() < 0.6:
            # Prefer horizontal or vertical (not diagonal)
            if abs(x2 - x) > abs(y2 - y):
                x += dx
            else:
                y += dy
        else:
            # Wander
            if rng.random() < 0.5:
                x += dx
            else:
                y += dy


def _carve_river(tiles, x1, y1, x2, y2, rng, direction="ns"):
    """Carve a winding river."""
    x, y = x1, y1
    while (direction == "ns" and y != y2) or (direction == "ew" and x != x2):
        if 0 <= y < MAP_H and 0 <= x < MAP_W:
            if tiles[y][x]["terrain"] != T_WATER:
                if tiles[y][x]["terrain"] == T_ROAD:
                    tiles[y][x]["terrain"] = T_BRIDGE
                else:
                    tiles[y][x]["terrain"] = T_RIVER

        if direction == "ns":
            y += 1 if y2 > y else -1
            x += rng.choice([-1, 0, 0, 0, 1])  # wander
        else:
            x += 1 if x2 > x else -1
            y += rng.choice([-1, 0, 0, 0, 1])

        x = max(0, min(MAP_W - 1, x))
        y = max(0, min(MAP_H - 1, y))


# ═══════════════════════════════════════════════════════════════
#  WORLD STATE
# ═══════════════════════════════════════════════════════════════

class WorldState:
    """Tracks the party's position and world map state."""

    def __init__(self, party, seed=42):
        self.party = party
        self.tiles = generate_world_map(seed)
        self.discovered_locations = set()

        # Party position — start at Briarhollow
        start = LOCATIONS["briarhollow"]
        self.party_x = start["x"]
        self.party_y = start["y"]

        # Steps since last encounter
        self.step_counter = 0

        # Discover starting area
        self._update_fog()

        # Mark visible towns as discovered
        for loc_id, loc in LOCATIONS.items():
            if loc.get("visible"):
                self.discovered_locations.add(loc_id)

    def move(self, dx, dy):
        """Move party by (dx, dy). Returns event dict or None.
        Events: {'type': 'encounter', 'key': ...}
                {'type': 'location', 'id': ..., 'data': ...}
                {'type': 'blocked'}
                {'type': 'discovery', 'id': ..., 'data': ...}
        """
        nx = self.party_x + dx
        ny = self.party_y + dy

        if nx < 0 or nx >= MAP_W or ny < 0 or ny >= MAP_H:
            return {"type": "blocked"}

        tile = self.tiles[ny][nx]
        terrain = tile["terrain"]
        tdata = TERRAIN_DATA[terrain]

        if not tdata["passable"]:
            return {"type": "blocked"}

        # Move
        self.party_x = nx
        self.party_y = ny
        self._update_fog()

        # Check for location
        loc_id = tile.get("location_id")
        if loc_id and loc_id in LOCATIONS:
            loc = LOCATIONS[loc_id]
            if loc_id not in self.discovered_locations:
                self.discovered_locations.add(loc_id)
                return {"type": "discovery", "id": loc_id, "data": loc}
            return {"type": "location", "id": loc_id, "data": loc}

        # Check for hidden location discovery nearby
        discovery = self._check_nearby_discoveries()
        if discovery:
            return discovery

        # Check for random encounter
        self.step_counter += 1
        enc_rate = tdata["encounter_rate"]
        if enc_rate > 0 and self.step_counter >= random.randint(max(1, enc_rate - 3), enc_rate + 3):
            self.step_counter = 0
            region = tile["region"]
            # Determine difficulty based on distance from starting town
            dist = math.sqrt((nx - 60) ** 2 + (ny - 75) ** 2)
            if dist < 15:
                tier = "easy"
            elif dist < 35:
                tier = "medium"
            else:
                tier = "hard"
            enc_key = get_encounter_for_zone(region, tier)
            return {"type": "encounter", "key": enc_key}

        return None

    def camp(self):
        """Rest the party. Returns event dict.
        {'type': 'camp_safe', 'healed': {...}}
        {'type': 'camp_ambush', 'key': ...}
        """
        tile = self.tiles[self.party_y][self.party_x]
        terrain = tile["terrain"]
        region = tile["region"]

        # Ambush check
        ambush_chance = CAMP_AMBUSH_CHANCE.get(terrain, 10)
        # Ranger reduces ambush chance
        for c in self.party:
            if c.class_name == "Ranger":
                ambush_chance = max(0, ambush_chance - 5)
            if c.class_name == "Cleric":
                ambush_chance = max(0, ambush_chance - 3)

        if random.randint(1, 100) <= ambush_chance:
            enc_key = get_encounter_for_zone(region, "easy")
            return {"type": "camp_ambush", "key": enc_key}

        # Safe rest — heal 25% HP, 15% MP/SP
        healed = {}
        from core.classes import get_all_resources
        for c in self.party:
            max_res = get_all_resources(c.class_name, c.stats, c.level)
            old_hp = c.resources.get("HP", 0)
            max_hp = max_res.get("HP", 1)
            heal_hp = int(max_hp * 0.25)
            c.resources["HP"] = min(max_hp, old_hp + heal_hp)

            # Regen MP/SP
            for res_name in c.resources:
                if res_name == "HP":
                    continue
                max_val = max_res.get(res_name, 0)
                old_val = c.resources[res_name]
                regen = int(max_val * 0.15)
                c.resources[res_name] = min(max_val, old_val + regen)

            healed[c.name] = c.resources["HP"] - old_hp

        return {"type": "camp_safe", "healed": healed}

    def get_tile(self, x, y):
        if 0 <= x < MAP_W and 0 <= y < MAP_H:
            return self.tiles[y][x]
        return None

    def get_current_tile(self):
        return self.tiles[self.party_y][self.party_x]

    def get_current_region(self):
        return self.get_current_tile()["region"]

    def _update_fog(self):
        """Reveal tiles within sight range of party."""
        tile = self.tiles[self.party_y][self.party_x]
        terrain = tile["terrain"]
        sight = TERRAIN_DATA[terrain]["sight"]

        for dy in range(-sight, sight + 1):
            for dx in range(-sight, sight + 1):
                nx = self.party_x + dx
                ny = self.party_y + dy
                if 0 <= nx < MAP_W and 0 <= ny < MAP_H:
                    dist = math.sqrt(dx * dx + dy * dy)
                    if dist <= sight:
                        self.tiles[ny][nx]["discovered"] = True

    def _check_nearby_discoveries(self):
        """Check if party is near any undiscovered hidden locations."""
        for loc_id, loc in LOCATIONS.items():
            if loc_id in self.discovered_locations:
                continue
            if loc.get("visible"):
                continue

            lx, ly = loc["x"], loc["y"]
            dist = abs(self.party_x - lx) + abs(self.party_y - ly)
            disc_radius = loc.get("discovery_radius", 2)

            if dist <= disc_radius:
                # Roll for discovery
                base_chance = loc.get("discovery_chance", 15)
                # Party bonuses
                for c in self.party:
                    if c.class_name == "Thief":
                        base_chance += 10
                    elif c.class_name == "Ranger":
                        region = self.tiles[self.party_y][self.party_x]["region"]
                        if region in ("thornwood", "mirehollow", "pale_coast"):
                            base_chance += 10
                    elif c.class_name == "Mage":
                        base_chance += 5

                if random.randint(1, 100) <= base_chance:
                    self.discovered_locations.add(loc_id)
                    return {"type": "discovery", "id": loc_id, "data": loc}

        return None

    def get_visible_tiles(self, view_w=22, view_h=16):
        """Get tiles visible in the viewport, centered on party."""
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
