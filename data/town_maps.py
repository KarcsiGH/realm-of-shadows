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
        "npc_name": "Innkeeper Bess",
    },
    "shop": {
        "name": "General Store",
        "type": BLD_SHOP,
        "door": (13, 5),
        "color": (100, 180, 120),
        "label_pos": (12, 3),
        "npc_name": "Merchant Kira",
    },
    "temple": {
        "name": "Shrine of Light",
        "type": BLD_TEMPLE,
        "door": (8, 12),
        "color": (200, 200, 140),
        "label_pos": (5, 10),
        "npc_name": "Priestess Alia",
    },
    "tavern": {
        "name": "The Rusty Flagon",
        "type": BLD_TAVERN,
        "door": (15, 12),
        "color": (200, 140, 80),
        "label_pos": (14, 10),
        "npc_name": "Barkeep Thom",
    },
    "forge": {
        "name": "Dunn's Forge",
        "type": BLD_FORGE,
        "door": (9, 17),
        "color": (220, 120, 50),
        "label_pos": (6, 15),
        "npc_name": "Forgemaster Dunn",
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
        "x": 16, "y": 14,  # near tavern, on grass
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
    # ── Building NPCs (shopkeepers standing near their doors) ──
    {
        "name": "Innkeeper Bess",
        "x": 11, "y": 5,  # walkable tile next to inn door (10,5)
        "service": "inn",
        "dialogue_id": "bess",
        "description": "A warm, bustling woman who runs the Wanderer's Rest.",
        "color": (200, 170, 120),
    },
    {
        "name": "Merchant Kira",
        "x": 14, "y": 5,  # walkable tile next to shop door (13,5)
        "service": "shop",
        "dialogue_id": "merchant_kira",
        "description": "A shrewd traveling merchant with goods from afar.",
        "color": (120, 180, 140),
    },
    {
        "name": "Priestess Alia",
        "x": 9, "y": 12,  # walkable tile next to temple door (8,12)
        "service": "temple",
        "dialogue_id": None,
        "description": "A serene priestess of the Shrine of Light.",
        "color": (220, 220, 160),
    },
    {
        "name": "Barkeep Thom",
        "x": 14, "y": 12,  # walkable tile next to tavern door (15,12)
        "service": "tavern",
        "dialogue_id": None,
        "description": "A grizzled barkeep who hears all the rumors.",
        "color": (180, 130, 80),
    },
    {
        "name": "Forgemaster Dunn",
        "x": 10, "y": 17,  # walkable tile next to forge door (9,17)
        "service": "forge",
        "dialogue_id": "forgemaster_dunn",
        "description": "A stocky dwarf who runs the town forge.",
        "color": (220, 140, 60),
    },
]

BRIARHOLLOW_SIGNS = {
    (11, 10): "Job Board — Check here for work.",
}

BRIARHOLLOW_SPAWN = (11, 18)  # on the path near bottom
BRIARHOLLOW_EXIT = [(10, 19), (11, 19)]  # exit tiles


# ══════════════════════════════════════════════════════════
#  WOODHAVEN — Forest Ranger Town (mid-tier)
# ══════════════════════════════════════════════════════════

# 28x22 tile map — forest town with a river running east-west through the middle
# Layout: Inn/Shop in NW, Guild in NE, Temple/Tavern in west-center,
#         Forge in SE, Ranger Hall in SW, bridge crosses river in center
WOODHAVEN_MAP_RAW = [
    "TTTTTTTTTTTTTTTTTTTTTTTTTTTT",  # 0
    "T.......................TTTT",  # 1
    "T..####..####..........TTTT",  # 2
    "T..#..#..#..#..........####",  # 3
    "T..#..D..D..#..........#..#",  # 4  inn(5,4) shop(8,4)      guild(25,4)
    "T..####..####..........D..#",  # 5                           guild(25,5)
    "T....P.P.......PPPPPPPP####",  # 6  stubs up to inn/shop, east path
    "T..PPPPPPPPPPPPPPPPPPPPPPPT",  # 7  main E-W street
    "T..P.........####.........T",  # 8
    "T..P.........#..#.........T",  # 9
    "T..P..####...D..#.........T",  # 10 temple(8,12)  tavern(13,10)
    "T..P..#..#...####.........T",  # 11
    "T..P..#..D...P............T",  # 12
    "T..P..####...P..S.........T",  # 13
    "T..P.........P....####....T",  # 14                forge(18,16)
    "WWWBWWWWWWWWWBWWWW#..#..WWW",  # 15 bridges at (3,15) and (13,15)
    "T..P.........P....D..#....T",  # 16
    "T..P.........P....####....T",  # 17
    "T..P.........PPPPPPPPP....T",  # 18 east path to forge
    "T..P..####................T",  # 19
    "T..P..#..D................T",  # 20 ranger_hall(8,20)
    "TPPPPPPPPEEPPPPPPPPPPPPPPPT",  # 21 exits(9,21)(10,21)
]

WOODHAVEN_MAP = _pad_map(WOODHAVEN_MAP_RAW, 28)

WOODHAVEN_BUILDINGS = {
    "inn": {
        "name": "The Canopy Rest",
        "type": BLD_INN,
        "door": (6, 4),
        "color": (120, 100, 70),
        "label_pos": (3, 2),
        "npc_name": "Innkeeper Jessa",
    },
    "shop": {
        "name": "Woodhaven Trading Post",
        "type": BLD_SHOP,
        "door": (9, 4),
        "color": (100, 130, 80),
        "label_pos": (7, 2),
        "npc_name": "Trader Finn",
    },
    "temple": {
        "name": "Grove Shrine",
        "type": BLD_TEMPLE,
        "door": (9, 12),
        "color": (80, 150, 80),
        "label_pos": (5, 10),
        "npc_name": "Druid Rowan",
    },
    "tavern": {
        "name": "The Hunter's Horn",
        "type": BLD_TAVERN,
        "door": (13, 10),
        "color": (130, 100, 60),
        "label_pos": (12, 8),
        "npc_name": "Barkeep Holt",
    },
    "forge": {
        "name": "Ranger's Forge",
        "type": BLD_FORGE,
        "door": (18, 16),
        "color": (160, 100, 50),
        "label_pos": (17, 14),
        "npc_name": "Smith Wren",
    },
    "guild": {
        "name": "Ranger's Guild",
        "type": BLD_HOUSE,
        "door": (23, 5),
        "color": (80, 120, 70),
        "label_pos": (22, 3),
        "npc_name": "Guildmaster Oren",
    },
    "ranger_hall": {
        "name": "Scout Hall",
        "type": BLD_HOUSE,
        "door": (9, 20),
        "color": (90, 110, 70),
        "label_pos": (5, 19),
    },
}

WOODHAVEN_NPCS = [
    # Story NPCs
    {
        "name": "Ranger Lyric",
        "x": 14, "y": 7,
        "dialogue_id": "ranger_lyric",
        "description": "A sharp-eyed ranger keeping watch over the forest paths.",
        "color": (100, 160, 80),
    },
    {
        "name": "Old Moss",
        "x": 6, "y": 14,
        "dialogue_id": "old_moss",
        "description": "An ancient herbalist gathering mushrooms by the river.",
        "color": (140, 170, 110),
    },
    {
        "name": "Apprentice Scout",
        "x": 20, "y": 8,
        "dialogue_id": None,
        "description": "A young scout practicing her footwork in the open yard.",
        "color": (90, 150, 70),
    },
    # Service NPCs
    {
        "name": "Innkeeper Jessa",
        "x": 7, "y": 4,
        "service": "inn",
        "dialogue_id": None,
        "description": "A quiet woman who keeps the inn spotless.",
        "color": (180, 160, 120),
    },
    {
        "name": "Trader Finn",
        "x": 10, "y": 4,
        "service": "shop",
        "dialogue_id": None,
        "description": "A well-traveled merchant with ranger supplies.",
        "color": (120, 180, 100),
    },
    {
        "name": "Druid Rowan",
        "x": 10, "y": 12,
        "service": "temple",
        "dialogue_id": None,
        "description": "A druid who tends the forest shrine.",
        "color": (80, 200, 100),
    },
    {
        "name": "Barkeep Holt",
        "x": 14, "y": 10,
        "service": "tavern",
        "dialogue_id": None,
        "description": "A burly hunter who runs the tavern between seasons.",
        "color": (180, 140, 80),
    },
    {
        "name": "Smith Wren",
        "x": 19, "y": 16,
        "service": "forge",
        "dialogue_id": None,
        "description": "A wiry woman who crafts bows and arrowheads.",
        "color": (200, 130, 60),
    },
    {
        "name": "Guildmaster Oren",
        "x": 24, "y": 5,
        "service": None,
        "dialogue_id": None,
        "description": "A grizzled ranger who runs the guild. He eyes you appraisingly.",
        "color": (100, 140, 80),
    },
]

WOODHAVEN_SIGNS = {
    (16, 13): "Job Board — Rangers needed for patrol work.",
}

WOODHAVEN_SPAWN = (11, 20)   # shifted right of ranger_hall door (9,20) to avoid auto-entry
WOODHAVEN_EXIT = [(9, 21), (10, 21)]


# ══════════════════════════════════════════════════════════
#  IRONHEARTH — Dwarven Mining City (high-tier)
# ══════════════════════════════════════════════════════════

# 30x24 tile map — stone city with forges and mineshaft entrance
IRONHEARTH_MAP_RAW = [
    "##############################",  # 0
    "#............................#",  # 1
    "#..####..####..####..####...#",  # 2
    "#..#..#..#..#..#..#..#..#...#",  # 3
    "#..#..D..D..#..#..D..D..#...#",  # 4  inn(5,4) shop(8,4) temple(17,4) tavern(20,4)
    "#..####..####..####..####...#",  # 5
    "#............................#",  # 6
    "#..PPPPPPPPPPPPPPPPPPPPPPPP.#",  # 7
    "#..P........................#",  # 8
    "#..P..########..########...#",  # 9
    "#..P..#......#..#......#...#",  # 10
    "#..P..#......D..D......#...#",  # 11 forge_main(11,11) armory(14,11)
    "#..P..#......#..#......#...#",  # 12
    "#..P..########..########...#",  # 13
    "#..P........................#",  # 14
    "#..P.S......................#",  # 15
    "#..P........................#",  # 16
    "#..P..####......####........#",  # 17
    "#..P..#..#......#..#........#",  # 18
    "#..P..#..D......D..#........#",  # 19 guild(8,19) mines_office(15,19)
    "#..P..####......####........#",  # 20
    "#..P........................#",  # 21
    "#..P........................#",  # 22
    "#PPPPPPPPPEEPPPPPPPPPPPPPPPP#",  # 23 exits(10,23)(11,23)
]

IRONHEARTH_MAP = _pad_map(IRONHEARTH_MAP_RAW, 30)

IRONHEARTH_BUILDINGS = {
    "inn": {
        "name": "The Iron Anvil Inn",
        "type": BLD_INN,
        "door": (6, 4),
        "color": (100, 90, 80),
        "label_pos": (3, 2),
        "npc_name": "Innkeeper Bron",
    },
    "shop": {
        "name": "Ironhearth Forge & Armory",
        "type": BLD_SHOP,
        "door": (9, 4),
        "color": (130, 110, 80),
        "label_pos": (7, 2),
        "npc_name": "Merchant Gilda",
    },
    "temple": {
        "name": "Shrine of the Deep",
        "type": BLD_TEMPLE,
        "door": (18, 4),
        "color": (120, 120, 160),
        "label_pos": (15, 2),
        "npc_name": "Priest Korvan",
    },
    "tavern": {
        "name": "The Molten Cup",
        "type": BLD_TAVERN,
        "door": (21, 4),
        "color": (160, 100, 50),
        "label_pos": (19, 2),
        "npc_name": "Barkeep Magda",
    },
    "forge_main": {
        "name": "The Grand Forge",
        "type": BLD_FORGE,
        "door": (13, 11),
        "color": (200, 120, 40),
        "label_pos": (7, 9),
        "npc_name": "Master Smith Thardin",
    },
    "armory": {
        "name": "City Armory",
        "type": BLD_SHOP,
        "door": (16, 11),
        "color": (140, 140, 150),
        "label_pos": (15, 9),
        "npc_name": "Quartermaster Helga",
    },
    "guild": {
        "name": "Miners' Guild",
        "type": BLD_HOUSE,
        "door": (9, 19),
        "color": (110, 100, 80),
        "label_pos": (5, 17),
        "npc_name": "Guildmaster Dorric",
    },
    "mines_office": {
        "name": "Mines Office",
        "type": BLD_HOUSE,
        "door": (16, 19),
        "color": (100, 100, 110),
        "label_pos": (14, 17),
    },
}

IRONHEARTH_NPCS = [
    # Story NPCs
    {
        "name": "Foreman Brak",
        "x": 20, "y": 14,
        "dialogue_id": "foreman_brak",
        "description": "A scarred dwarf who oversees the mine operations.",
        "color": (180, 140, 90),
    },
    {
        "name": "Scholar Petra",
        "x": 22, "y": 8,
        "dialogue_id": "scholar_petra",
        "description": "A human scholar studying dwarven runes.",
        "color": (160, 160, 200),
    },
    # Ambient NPCs
    {
        "name": "Miner Durk",
        "x": 18, "y": 21,
        "dialogue_id": None,
        "description": "A dusty dwarf heading home after a long shift underground.",
        "color": (150, 120, 80),
    },
    {
        "name": "City Guard",
        "x": 14, "y": 6,
        "dialogue_id": None,
        "description": "An armored guard keeping watch over the main road.",
        "color": (140, 150, 170),
    },
    {
        "name": "Apprentice Tova",
        "x": 20, "y": 19,
        "dialogue_id": None,
        "description": "A young dwarven apprentice running errands between the forge and armory.",
        "color": (200, 160, 80),
    },
    # Service NPCs
    {
        "name": "Innkeeper Bron",
        "x": 7, "y": 4,
        "service": "inn",
        "dialogue_id": None,
        "description": "A stout dwarf who pours strong ale.",
        "color": (160, 130, 90),
    },
    {
        "name": "Merchant Gilda",
        "x": 10, "y": 4,
        "service": "shop",
        "dialogue_id": None,
        "description": "A sharp-tongued merchant with the finest goods.",
        "color": (180, 160, 100),
    },
    {
        "name": "Priest Korvan",
        "x": 19, "y": 4,
        "service": "temple",
        "dialogue_id": None,
        "description": "A solemn priest of the deep stone.",
        "color": (140, 140, 200),
    },
    {
        "name": "Barkeep Magda",
        "x": 22, "y": 4,
        "service": "tavern",
        "dialogue_id": None,
        "description": "A boisterous dwarven woman who loves a good story.",
        "color": (200, 140, 80),
    },
    {
        "name": "Master Smith Thardin",
        "x": 12, "y": 11,
        "service": "forge",
        "dialogue_id": None,
        "description": "The finest weaponsmith in the region. His work is legendary.",
        "color": (220, 140, 40),
    },
]

IRONHEARTH_SIGNS = {
    (6, 15): "Job Board — Miners and fighters needed.",
}

IRONHEARTH_SPAWN = (10, 22)
IRONHEARTH_EXIT = [(10, 23), (11, 23)]


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
    "woodhaven": {
        "name": "Woodhaven",
        "map": WOODHAVEN_MAP,
        "width": 28,
        "height": 22,
        "buildings": WOODHAVEN_BUILDINGS,
        "npcs": WOODHAVEN_NPCS,
        "signs": WOODHAVEN_SIGNS,
        "spawn": WOODHAVEN_SPAWN,
        "exits": WOODHAVEN_EXIT,
        "ambient": "town_ambient",
    },
    "ironhearth": {
        "name": "Ironhearth",
        "map": IRONHEARTH_MAP,
        "width": 30,
        "height": 24,
        "buildings": IRONHEARTH_BUILDINGS,
        "npcs": IRONHEARTH_NPCS,
        "signs": IRONHEARTH_SIGNS,
        "spawn": IRONHEARTH_SPAWN,
        "exits": IRONHEARTH_EXIT,
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
