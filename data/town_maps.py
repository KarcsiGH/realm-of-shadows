"""
Realm of Shadows — Town Maps

Tile-based walkable town maps. Each town has:
- A tile grid (walkable outdoor area)
- Building definitions (name, entrance position, interior type)
- NPC placements (position, name, dialogue)
- Decoration tiles (trees, fences, wells, etc.)

Tile types:
  .  = grass/ground (walkable)
  #  = wall/building exterior (blocked)
  D  = door (walkable, triggers building entry)
  T  = tree (blocked)
  W  = water/well (blocked)
  F  = fence (blocked)
  P  = path/road (walkable)
  B  = bridge (walkable)
  S  = sign (blocked, readable)
  E  = town entrance/exit (walkable, triggers exit)
"""

# ══════════════════════════════════════════════════════════
#  TILE TYPES
# ══════════════════════════════════════════════════════════

TT_GRASS   = "."
TT_WALL    = "#"
TT_DOOR    = "D"
TT_TREE    = "T"
TT_WATER   = "W"
TT_FENCE   = "F"
TT_PATH    = "P"
TT_BRIDGE  = "B"
TT_SIGN    = "S"
TT_EXIT    = "E"

WALKABLE = {TT_GRASS, TT_DOOR, TT_PATH, TT_BRIDGE, TT_EXIT}

TILE_COLORS = {
    TT_GRASS:  (55, 85, 45),
    TT_WALL:   (75, 60, 45),
    TT_DOOR:   (130, 95, 50),
    TT_TREE:   (30, 65, 25),
    TT_WATER:  (40, 60, 110),
    TT_FENCE:  (100, 80, 55),
    TT_PATH:   (110, 95, 70),
    TT_BRIDGE: (120, 100, 65),
    TT_SIGN:   (140, 120, 70),
    TT_EXIT:   (80, 140, 80),
}

TILE_TOP_COLORS = {
    TT_WALL:  (95, 78, 58),
    TT_TREE:  (40, 80, 30),
    TT_FENCE: (120, 100, 70),
}


# ══════════════════════════════════════════════════════════
#  BUILDING TYPES — what service each building provides
# ══════════════════════════════════════════════════════════

BLD_INN       = "inn"
BLD_SHOP      = "shop"
BLD_TEMPLE    = "temple"
BLD_TAVERN    = "tavern"
BLD_FORGE     = "forge"
BLD_EXIT      = "exit"       # town gate
BLD_HOUSE     = "house"      # generic NPC house
BLD_JOBBOARD  = "jobboard"   # quest board (future)


# ══════════════════════════════════════════════════════════
#  BRIARHOLLOW — Starter Village
# ══════════════════════════════════════════════════════════

# Helper to ensure map rows are exactly the right width
def _pad_map(lines, w):
    result = []
    for line in lines:
        if len(line) < w:
            line = line + line[-1] * (w - len(line))
        elif len(line) > w:
            line = line[:w]
        result.append(line)
    return result


# 24x20 tile map
BRIARHOLLOW_MAP_RAW = [
    "TTTTTTTTTTTTTTTTTTTTTTTT",  # 0
    "T......................T",  # 1
    "T..TT..............TT.T",  # 2
    "T..TT..####..####..TT.T",  # 3
    "T......#..#..#..#.....T",  # 4
    "T......#..D..D..#.....T",  # 5  inn(10,5) shop(13,5)
    "T......####..####.....T",  # 6
    "T......................T",  # 7
    "T..PPPPPPPPPPPPPPPPPP.T",  # 8
    "T..P..................T",  # 9
    "T..P.####..S...####..T",  # 10
    "T..P.#..#......#..#..T",  # 11
    "T..P.#..D......D..#..T",  # 12 temple(8,12) tavern(15,12)
    "T..P.####......####..T",  # 13
    "T..P..................T",  # 14
    "T..P..####....####...T",  # 15
    "T..P..#..#....#..#...T",  # 16
    "T..P..#..D....D..#...T",  # 17 forge(9,17) home(14,17)
    "T..P..####....####...T",  # 18
    "TPPPPPPPPPEEPPPPPPPPPT",  # 19 exits(10,19)(11,19)
]

BRIARHOLLOW_MAP = _pad_map(BRIARHOLLOW_MAP_RAW, 24)


BRIARHOLLOW_BUILDINGS = {
    "inn": {
        "name": "The Wanderer's Rest",
        "type": BLD_INN,
        "door": (10, 5),
        "color": (180, 160, 100),
        "label_pos": (7, 3),
    },
    "shop": {
        "name": "General Store",
        "type": BLD_SHOP,
        "door": (13, 5),
        "color": (100, 180, 120),
        "label_pos": (12, 3),
    },
    "temple": {
        "name": "Shrine of Light",
        "type": BLD_TEMPLE,
        "door": (8, 12),
        "color": (200, 200, 140),
        "label_pos": (5, 10),
    },
    "tavern": {
        "name": "The Rusty Flagon",
        "type": BLD_TAVERN,
        "door": (15, 12),
        "color": (200, 140, 80),
        "label_pos": (14, 10),
    },
    "forge": {
        "name": "Dunn's Forge",
        "type": BLD_FORGE,
        "door": (9, 17),
        "color": (220, 120, 50),
        "label_pos": (6, 15),
    },
    "home": {
        "name": "Elder's House",
        "type": BLD_HOUSE,
        "door": (14, 17),
        "color": (140, 140, 160),
        "label_pos": (13, 15),
    },
}

BRIARHOLLOW_NPCS = [
    {
        "name": "Maren",
        "x": 12, "y": 8,
        "dialogue_id": "maren",
        "description": "A determined woman with knowing eyes.",
        "color": (180, 140, 220),
    },
    {
        "name": "Captain Aldric",
        "x": 16, "y": 12,  # near tavern
        "dialogue_id": "captain_aldric",
        "description": "The town's guard captain, nursing an ale.",
        "color": (140, 160, 200),
    },
    {
        "name": "Elder Thom",
        "x": 15, "y": 17,  # near elder's house
        "dialogue_id": "elder_thom",
        "description": "The village elder, weathered but sharp.",
        "color": (180, 170, 140),
    },
]

BRIARHOLLOW_SIGNS = {
    (11, 10): "Job Board — Check here for work.",
}

BRIARHOLLOW_SPAWN = (11, 18)  # on the path near bottom
BRIARHOLLOW_EXIT = [(10, 19), (11, 19)]  # exit tiles


# ══════════════════════════════════════════════════════════
#  TOWN REGISTRY
# ══════════════════════════════════════════════════════════

TOWN_MAPS = {
    "briarhollow": {
        "name": "Briarhollow",
        "map": BRIARHOLLOW_MAP,
        "width": 24,
        "height": 20,
        "buildings": BRIARHOLLOW_BUILDINGS,
        "npcs": BRIARHOLLOW_NPCS,
        "signs": BRIARHOLLOW_SIGNS,
        "spawn": BRIARHOLLOW_SPAWN,
        "exits": BRIARHOLLOW_EXIT,
        "ambient": "town_ambient",
    },
}


def get_town_data(town_id):
    """Get town map data by ID. Returns None if town doesn't have a walkable map."""
    return TOWN_MAPS.get(town_id)


def get_tile(town_data, x, y):
    """Get tile character at (x,y). Returns '#' for out-of-bounds."""
    if 0 <= y < town_data["height"] and 0 <= x < town_data["width"]:
        return town_data["map"][y][x]
    return TT_WALL


def is_walkable(town_data, x, y):
    """Check if a tile is walkable."""
    return get_tile(town_data, x, y) in WALKABLE


def get_building_at(town_data, x, y):
    """Get building dict if there's a door at (x,y). Returns None otherwise."""
    for bld_id, bld in town_data["buildings"].items():
        if bld["door"] == (x, y):
            return bld_id, bld
    return None


def get_npc_at(town_data, x, y):
    """Get NPC dict at position (x,y). Returns None if no NPC."""
    for npc in town_data.get("npcs", []):
        if npc["x"] == x and npc["y"] == y:
            return npc
    return None


def get_sign_at(town_data, x, y):
    """Get sign text at position. Returns None if no sign."""
    return town_data.get("signs", {}).get((x, y))


def is_exit(town_data, x, y):
    """Check if tile is a town exit."""
    return (x, y) in town_data.get("exits", [])
