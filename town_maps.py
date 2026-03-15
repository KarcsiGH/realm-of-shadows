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
BLD_GUILD     = "guild"      # adventurers/rangers guild

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



# ══════════════════════════════════════════════════════════
#  BRIARHOLLOW — Starter Village  (60x34)
# ══════════════════════════════════════════════════════════
#
#  Buildings are scattered and vary in size — players explore to find them.
#  Tile key: T=tree  #=wall  .=grass  P=path  D=door
#            S=sign  W=well  B=bench  E=exit
#
#  NW  — Inn (14×7, large): cols 2-15, rows 2-8       door @ (8,8)
#  N   — General Store (9×5, medium): cols 20-28, r 2-6  door @ (24,6)
#  NE  — Elder's House (7×5, small): cols 46-52, r 3-7   door @ (48,7)
#  SE  — Temple of Light (15×8, grand): cols 37-51, r 17-24  door @ (43,17)
#  SW  — Dunn's Forge (10×8, industrial): cols 2-11, r 19-26 door @ (6,19)
#  SC  — The Rusty Flagon/Tavern (12×7): cols 17-28, r 20-26  door @ (22,20)
#
#  Main E-W street: row 10   Secondary path: row 15   South road: row 28
#  Town square: rows 11-14 with well, benches, trees
#  Exit gate: row 29, cols 28-30

BRIARHOLLOW_MAP_RAW = [
    "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",  #  0
    "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",  #  1
    "TT##############....#########.............................TT",  #  2  Inn NW | Shop N
    "TT##############....#########.................#######.....TT",  #  3         | Elder NE starts
    "TT##############....#########.................#######.....TT",  #  4
    "TT##############....#########.................#######.....TT",  #  5
    "TT##############....####D####.................#######.....TT",  #  6  Shop door col 24
    "TT##############........P.....................##D####.....TT",  #  7  Elder door col 48
    "TT######D#######........P.......................P.........TT",  #  8  Inn door col 8
    "TT......P...............P.......................P.........TT",  #  9  paths → main street
    "TTPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPTT",  # 10  main cobblestone street
    "TT............T...T.S......W..........T.S.................TT",  # 11  square: sign(20,11) well(27,11) sign(40,11)
    "TT......T...............B.....T.....B...............T.....TT",  # 12  benches col 24 & 36
    "TT...............................T............T...........TT",  # 13
    "TT........................................................TT",  # 14
    "TTPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPTT",  # 15  secondary path
    "TT..T.P.....T.........P.........T..........P......T....T..TT",  # 16  scattered trees + door paths
    "TT....P...............P..............######D########......TT",  # 17  Temple door col 43
    "TT....P...............P..............###############......TT",  # 18
    "TT####D#####..........P..............###############......TT",  # 19  Forge door col 6
    "TT##########.....#####D######........###############......TT",  # 20  Tavern door col 22
    "TT##########.....############........###############......TT",  # 21
    "TT##########.....############........###############......TT",  # 22
    "TT##########.....############........###############......TT",  # 23
    "TT##########.....############........###############......TT",  # 24
    "TT##########.....############.............................TT",  # 25
    "TT##########.....############.............................TT",  # 26
    "TT...T.........T...................T............T.........TT",  # 27  south common with trees
    "TTPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPTT",  # 28  south road
    "TT..........................EEE...........................TT",  # 29  exit gate cols 28-30
    "TT........................................................TT",  # 30
    "TT........................................................TT",  # 31
    "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",  # 32
    "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",  # 33
]

BRIARHOLLOW_MAP = _pad_map(BRIARHOLLOW_MAP_RAW, 60)


BRIARHOLLOW_BUILDINGS = {
    # Inn — largest building, NW corner. Warm, welcoming amber colour.
    "inn": {
        "name": "The Wanderer's Rest",
        "type": BLD_INN,
        "door": (8, 8),
        "color": (180, 140, 80),
        "label_pos": (8, 2),
        "npc_name": "Innkeeper Bess",
        "wall_cols": (2, 15),
        "wall_rows": (2, 8),
        "indoor_npc": {"name": "Innkeeper Bess", "npc_type": "innkeeper", "title": "Innkeeper",
                       "description": "A warm, bustling woman drying her hands on her apron.",
                       "color": (210, 175, 120), "dialogue_id": "bess"},
    },
    # General Store — medium, north-centre.
    "shop": {
        "name": "General Store",
        "type": BLD_SHOP,
        "door": (24, 6),
        "color": (80, 155, 100),
        "label_pos": (24, 2),
        "npc_name": "Merchant Kira",
        "wall_cols": (20, 28),
        "wall_rows": (2, 6),
        "indoor_npc": {"name": "Merchant Kira", "npc_type": "merchant", "title": "Merchant",
                       "description": "A shrewd traveler arranging goods on a small table.",
                       "color": (120, 190, 140), "dialogue_id": "merchant_kira"},
    },
    # Elder's House — smallest building, tucked in NE corner. Players must explore to find it.
    "elder": {
        "name": "Elder's House",
        "type": BLD_HOUSE,
        "door": (48, 7),
        "color": (140, 125, 160),
        "label_pos": (48, 3),
        "npc_name": "Elder Thom",
        "wall_cols": (46, 52),
        "wall_rows": (3, 7),
        "indoor_npc": {"name": "Elder Thom", "npc_type": "elder", "title": "Village Elder",
                       "description": "The village elder with sharp, watchful eyes.",
                       "color": (185, 175, 140), "dialogue_id": "elder_thom"},
    },
    # Temple — grandest building, SE. Requires crossing town to reach.
    "temple": {
        "name": "Temple of Light",
        "type": BLD_TEMPLE,
        "door": (43, 17),
        "color": (210, 200, 120),
        "label_pos": (43, 17),
        "npc_name": "Priestess Alia",
        "wall_cols": (37, 51),
        "wall_rows": (17, 24),
        "indoor_npc": {"name": "Priestess Alia", "npc_type": "priestess", "title": "Priestess",
                       "description": "A serene priestess tending the altar flame.",
                       "color": (225, 225, 165), "dialogue_id": "priestess_alia"},
    },
    # Forge — industrial, SW. Wide low building.
    "forge": {
        "name": "Dunn's Forge",
        "type": BLD_FORGE,
        "door": (6, 19),
        "color": (210, 95, 35),
        "label_pos": (6, 19),
        "npc_name": "Forgemaster Dunn",
        "wall_cols": (2, 11),
        "wall_rows": (19, 26),
        "indoor_npc": {"name": "Forgemaster Dunn", "npc_type": "forger", "title": "Forgemaster",
                       "description": "A stocky dwarf, arms thick from years at the anvil.",
                       "color": (225, 145, 60), "dialogue_id": "forgemaster_dunn"},
    },
    # Tavern — south-centre. Medium, lively.
    "tavern": {
        "name": "The Rusty Flagon",
        "type": BLD_TAVERN,
        "door": (22, 20),
        "color": (195, 110, 50),
        "label_pos": (22, 20),
        "npc_name": "Barkeep Sylla",
        "wall_cols": (17, 28),
        "wall_rows": (20, 26),
        "indoor_npc": {"name": "Barkeep Sylla", "npc_type": "barkeep", "title": "Barkeep",
                       "description": "A sharp-eyed woman who misses nothing.",
                       "color": (185, 135, 80), "dialogue_id": "sylla"},
    },
}


BRIARHOLLOW_NPCS = [
    {
        "name": "Warden Liaison",
        "x": 9, "y": 9,
        "dialogue_id": "warden_liaison",
        "description": "A representative of the old Warden order. Weathered but watchful.",
        "color": (100, 175, 130),
        "npc_type": "warden",
    },
    # Elder Thom stands just outside his house in the NE — worth finding.
    {
        "name": "Elder Thom",
        "x": 48, "y": 8,
        "dialogue_id": "elder_thom",
        "description": "The village elder, watching the square with sharp eyes.",
        "color": (185, 175, 140),
        "npc_type": "elder",
    },
    # Guildmaster Oren can also be found near the guild door giving transition advice.
    {
        "name": "Guildmaster Oren",
        "x": 22, "y": 6,
        "dialogue_id": "trainer_briarhollow",
        "description": "The guild's veteran master. He speaks of paths beyond the first calling.",
        "color": (100, 140, 80),
        "npc_type": "guildmaster",
    },
    # Maren near the well in the town square.
    {
        "name": "Maren",
        "x": 27, "y": 12,
        "dialogue_id": "maren",
        "description": "A determined woman with knowing eyes, watching the gate.",
        "color": (180, 140, 220),
        "npc_type": "mage",
        "hide_if": "maren.left",
    },
    # Captain Aldric patrols the main street.
    {
        "name": "Captain Aldric",
        "x": 15, "y": 10,
        "dialogue_id": "captain_aldric",
        "description": "The guard captain, keeping a watchful eye on arrivals.",
        "color": (145, 165, 205),
        "npc_type": "guard",
    },
    {
        "name": "Old Petra",
        "x": 35, "y": 11,
        "dialogue_id": "old_petra",
        "description": "An elderly woman feeding pigeons near the well.",
        "color": (190, 180, 160),
        "npc_type": "elder",
    },
    {
        "name": "Young Tomas",
        "x": 10, "y": 12,
        "dialogue_id": "young_tomas",
        "description": "A restless young man who eyes your weapons with admiration.",
        "color": (160, 195, 160),
        "npc_type": "youth",
    },
    {
        "name": "Herb Seller",
        "x": 32, "y": 10,
        "dialogue_id": None,
        "description": "A wiry woman selling dried herbs from a wicker basket.",
        "color": (140, 195, 130),
        "npc_type": "merchant",
    },
    {
        "name": "Town Guard",
        "x": 29, "y": 28,
        "dialogue_id": None,
        "description": "A bored guard keeping watch on the south road.",
        "color": (140, 155, 185),
        "npc_type": "guard",
    },
]

BRIARHOLLOW_SIGNS = {
    (20, 11): "Briarhollow — Founded in the Third Age. Population: 312.",
    (40, 11): "Job Board — Adventurers wanted. Post your contracts here.",
}

BRIARHOLLOW_SPAWN = (29, 27)   # arriving from south, just north of exit road
BRIARHOLLOW_EXIT  = [(28, 29), (29, 29), (30, 29)]





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
    "T..###.P..###..........D..#",  # 5  stubs to inn(6) and shop(9)
    "T....PPP.P.....PPPPPPPP####",  # 6  stubs up to inn/shop, east path
    "T..PPPPPPPPPPPPPPPPPPPPPPPT",  # 7  main E-W street
    "T..P.........####.........T",  # 8
    "T..P.........#..#.........T",  # 9
    "T..P..##.#...D..#.........T",  # 10 temple(8,12)  tavern(13,10)
    "T..P..#..#...####.........T",  # 11
    "T..P..#..D...P............T",  # 12
    "T..P..####...P..S.........T",  # 13
    "T..P.........P.....###....T",  # 14                forge(18,16)
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
        "indoor_npc": {"name": "Innkeeper Jessa", "npc_type": "innkeeper", "title": "Innkeeper", "description": "A quiet woman who keeps the inn spotless.", "color": (180, 160, 120), "dialogue_id": None},
    },
    "shop": {
        "name": "Woodhaven Trading Post",
        "type": BLD_SHOP,
        "door": (9, 4),
        "color": (100, 130, 80),
        "label_pos": (7, 2),
        "npc_name": "Trader Finn",
        "indoor_npc": {"name": "Trader Finn", "npc_type": "merchant", "title": "Merchant", "description": "A well-traveled merchant with ranger supplies.", "color": (120, 180, 100), "dialogue_id": None},
    },
    "temple": {
        "name": "Grove Shrine",
        "type": BLD_TEMPLE,
        "door": (9, 12),
        "color": (80, 150, 80),
        "label_pos": (5, 10),
        "npc_name": "Druid Rowan",
        "indoor_npc": {"name": "Druid Rowan", "npc_type": "priestess", "title": "Druid", "description": "A druid who tends the forest shrine.", "color": (80, 200, 100), "dialogue_id": None},
    },
    "tavern": {
        "name": "The Hunter's Horn",
        "type": BLD_TAVERN,
        "door": (13, 10),
        "color": (130, 100, 60),
        "label_pos": (12, 8),
        "npc_name": "Barkeep Holt",
        "indoor_npc": {"name": "Barkeep Holt", "npc_type": "barkeep", "title": "Barkeep", "description": "A burly hunter who runs the tavern between seasons.", "color": (180, 140, 80), "dialogue_id": None},
    },
    "forge": {
        "name": "Ranger's Forge",
        "type": BLD_FORGE,
        "door": (18, 16),
        "color": (160, 100, 50),
        "label_pos": (17, 14),
        "npc_name": "Smith Wren",
        "indoor_npc": {"name": "Smith Wren", "npc_type": "forger", "title": "Smith", "description": "A wiry woman who crafts bows and arrowheads.", "color": (200, 130, 60), "dialogue_id": None},
    },
    "guild": {
        "name": "Ranger's Guild",
        "type": BLD_HOUSE,
        "door": (23, 5),
        "color": (80, 120, 70),
        "label_pos": (22, 3),
        "npc_name": "Guildmaster Oren",
        "indoor_npc": {"name": "Guildmaster Oren", "npc_type": "guildmaster", "title": "Guildmaster", "description": "A grizzled ranger who runs the guild.", "color": (100, 140, 80), "dialogue_id": "guildmaster_oren"},
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
    {
        "name": "Warden Liaison",
        "x": 10, "y": 8,
        "dialogue_id": "warden_liaison",
        "description": "A representative of the old Warden order. Weathered but watchful.",
        "color": (100, 175, 130),
        "npc_type": "warden",
    },
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
        "name": "Guildmaster Oren",
        "x": 24, "y": 5,
        "service": None,
        "dialogue_id": "guildmaster_oren",
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
        "indoor_npc": {"name": "Innkeeper Bron", "npc_type": "innkeeper", "title": "Innkeeper", "description": "A stout dwarf who pours strong ale.", "color": (160, 130, 90), "dialogue_id": None},
    },
    "shop": {
        "name": "Ironhearth Forge & Armory",
        "type": BLD_SHOP,
        "door": (9, 4),
        "color": (130, 110, 80),
        "label_pos": (7, 2),
        "npc_name": "Merchant Gilda",
        "indoor_npc": {"name": "Merchant Gilda", "npc_type": "merchant", "title": "Merchant", "description": "A sharp-tongued merchant with the finest goods.", "color": (180, 160, 100), "dialogue_id": None},
    },
    "temple": {
        "name": "Shrine of the Deep",
        "type": BLD_TEMPLE,
        "door": (18, 4),
        "color": (120, 120, 160),
        "label_pos": (15, 2),
        "npc_name": "Priest Korvan",
        "indoor_npc": {"name": "Priest Korvan", "npc_type": "priestess", "title": "Priest", "description": "A solemn priest of the deep stone.", "color": (140, 140, 200), "dialogue_id": None},
    },
    "tavern": {
        "name": "The Molten Cup",
        "type": BLD_TAVERN,
        "door": (21, 4),
        "color": (160, 100, 50),
        "label_pos": (19, 2),
        "npc_name": "Barkeep Magda",
        "indoor_npc": {"name": "Barkeep Magda", "npc_type": "barkeep", "title": "Barkeep", "description": "A boisterous dwarven woman who loves a good story.", "color": (200, 140, 80), "dialogue_id": None},
    },
    "forge_main": {
        "name": "The Grand Forge",
        "type": BLD_FORGE,
        "door": (13, 11),
        "color": (200, 120, 40),
        "label_pos": (7, 9),
        "npc_name": "Master Smith Thardin",
        "indoor_npc": {"name": "Master Smith Thardin", "npc_type": "forger", "title": "Master Smith", "description": "The finest weaponsmith in the region.", "color": (220, 140, 40), "dialogue_id": None},
    },
    "armory": {
        "name": "City Armory",
        "type": BLD_SHOP,
        "door": (16, 11),
        "color": (140, 140, 150),
        "label_pos": (15, 9),
        "npc_name": "Quartermaster Helga",
        "indoor_npc": {"name": "Quartermaster Helga", "npc_type": "merchant", "title": "Quartermaster", "description": "A no-nonsense quartermaster.", "color": (160, 150, 120), "dialogue_id": None},
    },
    "guild": {
        "name": "Miners' Guild",
        "type": BLD_HOUSE,
        "door": (9, 19),
        "color": (110, 100, 80),
        "label_pos": (5, 17),
        "npc_name": "Guildmaster Dorric",
        "indoor_npc": {"name": "Guildmaster Dorric", "npc_type": "guildmaster", "title": "Guildmaster", "description": "A weathered veteran who runs the guild with iron discipline.", "color": (140, 160, 180), "dialogue_id": None},
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
    {
        "name": "Warden Liaison",
        "x": 11, "y": 9,
        "dialogue_id": "warden_liaison",
        "description": "A representative of the old Warden order. Weathered but watchful.",
        "color": (100, 175, 130),
        "npc_type": "warden",
    },
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
    # Guildmaster Dorric outside guild — offers transition guidance
    {
        "name": "Guildmaster Dorric",
        "x": 9, "y": 18,
        "dialogue_id": "trainer_ironhearth",
        "description": "The guild's weathered master. He speaks of warriors who walked two paths.",
        "color": (140, 160, 180),
        "npc_type": "guildmaster",
    },
    # Ambient NPCs
    {
        "name": "Miner Durk",
        "x": 18, "y": 21,
        "dialogue_id": "miner_durk",
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
        "dialogue_id": "apprentice_tova",
        "description": "A young dwarven apprentice running errands between the forge and armory.",
        "color": (200, 160, 80),
    },
    # Service NPCs
]

IRONHEARTH_SIGNS = {
    (5, 15): "Job Board — Miners and fighters needed.",
}

IRONHEARTH_SPAWN = (10, 22)
IRONHEARTH_EXIT = [(10, 23), (11, 23)]


# ══════════════════════════════════════════════════════════
#  TOWN REGISTRY
# ══════════════════════════════════════════════════════════


GREENWOOD_MAP_RAW = [
    "TTTTTTTTTTTTTTTTTTTTTTTT",  # 0
    "TTTT................TTTT",  # 1
    "TTT..TT..####.....TTTTT",  # 2
    "TT...TT..#..#......TTTT",  # 3
    "TT...TT..#..D......TTTT",  # 4  inn(9,4)
    "TT...TT..####..TT..TTTT",  # 5
    "TT....PPPPP..TTTT..TTTT",  # 6
    "TT....P.....TT.....TTTT",  # 7
    "TT....PS####.......TTTT",  # 8
    "TT....P.#..#...S...TTTT",  # 9
    "TT....P....D.......TTTT",  # 10 tavern(10,10)
    "TT....P.####.......TTTT",  # 11
    "TT....P............TTTT",  # 12
    "TT....P..####......TTTT",  # 13
    "TT....P..#..#..####TTT",   # 14
    "TT....P..#..D..#..#TTT",   # 15 shop(11,15)  temple(15,15)
    "TT....P..####..####TTT",   # 16
    "TT....P............TTTT",  # 17
    "TT....P............TTTT",  # 18
    "TTTTPPPPEEPPPPTTTTTTTTT",  # 19 exits(8,19)(9,19)
]

GREENWOOD_MAP = _pad_map(GREENWOOD_MAP_RAW, 24)

GREENWOOD_BUILDINGS = {
    "inn": {
        "name": "The Hollow Log Inn",
        "type": BLD_INN,
        "door": (12, 4),        # D is at col 12 on row 4
        "color": (110, 90, 60),
        "label_pos": (9, 2),
        "npc_name": "Innkeeper Petra",
    },
    "tavern": {
        "name": "The Muddy Boot",
        "type": BLD_TAVERN,
        "door": (10, 10),       # D at col 10 row 10 (col 8='#', 9='.', 10='D')
        "color": (120, 100, 65),
        "label_pos": (8, 8),
        "npc_name": "Barkeep Oswin",
    },
    "shop": {
        "name": "Ranger Supplies",
        "type": BLD_SHOP,
        "door": (12, 15),       # D at col 12 on row 15
        "color": (90, 120, 70),
        "label_pos": (9, 13),
        "npc_name": "Trader Fen",
    },
    "temple": {
        "name": "Grove Sanctuary",
        "type": BLD_TEMPLE,
        "door": (12, 15),       # shares row 15 — temple uses same door row, different building side
        "color": (70, 140, 80),
        "label_pos": (14, 13),
        "npc_name": "Warden Sylk",
    },
}

GREENWOOD_NPCS = [
    {
        "name": "Warden Liaison",
        "x": 8, "y": 8,
        "dialogue_id": "warden_liaison",
        "description": "A representative of the old Warden order. Weathered but watchful.",
        "color": (100, 175, 130),
        "npc_type": "warden",
    },
    {
        "name": "Scout Feryn",
        "x": 7, "y": 7,        # on path (P)
        "dialogue_id": "scout_feryn",
        "description": "A lean ranger watching the treeline with sharp eyes.",
        "color": (90, 150, 70),
    },
    {
        "name": "Trapper Holt",
        "x": 10, "y": 12,      # on path
        "dialogue_id": "trapper_holt",
        "description": "A sun-weathered trapper sorting pelts on a wooden rack.",
        "color": (160, 130, 90),
    },
    {
        "name": "Old Moss",
        "x": 4, "y": 3,        # near the treeline, north-west open ground
        "dialogue_id": "old_moss",
        "description": "An ancient figure draped in moss and bark, watching the trees with patient eyes.",
        "color": (60, 110, 50),
    },
]

GREENWOOD_SIGNS = {
    (12, 9): "Notice Board — Bounties posted within.",
    (7, 8): "Job Board — Seek work or post contracts.",
}

GREENWOOD_SPAWN = (8, 18)
GREENWOOD_EXIT = [(8, 19), (9, 19)]


# ══════════════════════════════════════════════════════════
#  SALTMERE — Rough Port Town (Rogue/thief hub, no teleport)
# ══════════════════════════════════════════════════════════

# 28x22 — Waterfront town. Docks at south. Winding streets,
# cramped buildings, no open squares. Hidden alley feel.
SALTMERE_MAP_RAW = [
    "TTTTTTTTTTTTTTTTTTTTTTTTTTTT",  # 0
    "T..........................T",   # 1
    "T..####..####..............T",   # 2
    "T..#..#..#..#....####......T",   # 3
    "T..#..D..D..#....#..#......T",   # 4  inn(5,4) shop(8,4)
    "T..####..####....#..D......T",   # 5           black_market(17,5)
    "T.....PP.........####......T",   # 6
    "T.....PP.......PPPPPPPPPPPT",    # 7
    "T.....PP.......P.S.........T",   # 8
    "T.PPPPPP.......P...####....T",   # 9
    "T.P............P...#..#....T",   # 10
    "T.P..####......P...#..D....T",   # 11 thieves_den(11,11)  tavern(20,11)
    "T.P..#..#......P...####....T",   # 12
    "T.P..#..D......P...........T",   # 13
    "T.P..####......P...####....T",   # 14
    "T.P............P...#..#....T",   # 15
    "T.P..####......P...#..D....T",   # 16 temple(7,16)         forge(20,16)
    "T.P..#..#......P...####....T",   # 17
    "T.P..#..D......P...........T",   # 18
    "T.P..####......P...........T",   # 19
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",  # 20  harbor water
    "WWEEWWWWWWWWWWWWWWWWWWWWWWWW",  # 21  exits(2,21)(3,21) — dock exit
]

SALTMERE_MAP = _pad_map(SALTMERE_MAP_RAW, 28)

SALTMERE_BUILDINGS = {
    "inn": {
        "name": "The Barnacle",
        "type": BLD_INN,
        "door": (5, 4),
        "color": (100, 110, 80),
        "label_pos": (3, 2),
        "npc_name": "Innkeeper Cressa",
    },
    "shop": {
        "name": "Saltmere Trader",
        "type": BLD_SHOP,
        "door": (8, 4),
        "color": (90, 120, 90),
        "label_pos": (7, 2),
        "npc_name": "Merchant Dova",
    },
    "black_market": {
        "name": "The Back Room",
        "type": BLD_SHOP,
        "door": (20, 5),        # D is at col 20 on row 5
        "color": (80, 60, 90),
        "label_pos": (15, 3),
        "npc_name": "Fence Rael",
    },
    "thieves_den": {
        "name": "Thieves' Guild",
        "type": BLD_HOUSE,
        "door": (11, 13),
        "color": (60, 50, 80),
        "label_pos": (8, 11),
        "npc_name": "Guildmaster Sable",
    },
    "tavern": {
        "name": "The Drowned Anchor",
        "type": BLD_TAVERN,
        "door": (20, 11),
        "color": (110, 90, 70),
        "label_pos": (18, 9),
        "npc_name": "Barkeep Mick",
    },
    "temple": {
        "name": "Shrine of the Tides",
        "type": BLD_TEMPLE,
        "door": (7, 18),
        "color": (70, 100, 140),
        "label_pos": (4, 16),
        "npc_name": "Tide Priest Oran",
    },
    "forge": {
        "name": "Harbor Forge",
        "type": BLD_FORGE,
        "door": (20, 16),
        "color": (160, 100, 50),
        "label_pos": (18, 14),
        "npc_name": "Smith Crag",
    },
}

SALTMERE_NPCS = [
    {
        "name": "Warden Liaison",
        "x": 10, "y": 9,
        "dialogue_id": "warden_liaison",
        "description": "A representative of the old Warden order. Weathered but watchful.",
        "color": (100, 175, 130),
        "npc_type": "warden",
    },
    {
        "name": "Dockhand Riv",
        "x": 25, "y": 17,      # open area near the harbor wall
        "dialogue_id": "dockhand_riv",
        "description": "A weathered sailor with rope-burned hands, watching the harbor.",
        "color": (140, 160, 180),
    },
    {
        "name": "Shady Figure",
        "x": 13, "y": 8,
        "dialogue_id": "shady_figure",
        "description": "A cloaked figure who meets your gaze and looks away too quickly.",
        "color": (80, 70, 100),
    },

    {
        "name": "Tide Priest Oran",
        "x": 12, "y": 16,
        "dialogue_id": "tide_priest_oran",
        "description": "The Tide Priest stands at the water's edge, watching the horizon.",
        "color": (80, 130, 200),
        "npc_type": "priest",
    },
    {
        "name": "Guildmaster Sable",
        "x": 8, "y": 12,
        "dialogue_id": "guildmaster_sable",
        "description": "The Guildmaster leans against the wall, arms folded, watching everyone.",
        "color": (120, 90, 160),
        "npc_type": "guildmaster",
    },
]

SALTMERE_SIGNS = {
    (14, 9): "Harbor Master — All ships must register.",
    (17, 8): "Job Board — Mercenaries and merchants post work here.",
}

SALTMERE_SPAWN = (10, 19)
SALTMERE_EXIT = [(2, 21), (3, 21)]


# ══════════════════════════════════════════════════════════
#  SANCTUM — Holy City (WIS-focused, grand cathedral)
# ══════════════════════════════════════════════════════════

# 30x24 — Symmetrical holy city. Wide stone paths.
# Grand cathedral dominates the center-north.
# Pilgrims and priests everywhere.
SANCTUM_MAP_RAW = [
    "##############################",  # 0  stone walls
    "#............................#",  # 1
    "#..########..########........#",  # 2
    "#..#......#..#......#........#",  # 3
    "#..#......#..#......#........#",  # 4
    "#..#......D..D......#........#",  # 5  cathedral_l(11,5)  cathedral_r(14,5)
    "#..########P.########........#",  # 6  stub connecting cathedral_l(11) to path
    "#....PPPPPPPPPPPPPPPPPP......#",  # 7  main nave path
    "#....P..................P....#",  # 8
    "#....P..####......####..P...#",  # 9
    "#....P..#..#......#..#..P...#",  # 10
    "#....P..#..D......D..#..P...#",  # 11 inn(9,11)   shop(18,11)
    "#....P..####......####..P...#",  # 12
    "#....P..................P....#",  # 13
    "#..S.PPPPPPPPPPPPPPPPPPPP...#",  # 14
    "#....P..................P....#",  # 15
    "#....P..####......####..P...#",  # 16
    "#....P..#..#......#..#..P...#",  # 17
    "#....P..#..D......D..#..P...#",  # 18 temple(9,18)  tavern(18,18)
    "#....P..####......####..P...#",  # 19
    "#....P..................P....#",  # 20
    "#....P..####..............P.#",  # 21
    "#....P..#..D..............P.#",  # 22 reliquary(10,22)
    "#PPPPPPPPPEEPPPPPPPPPPPPPPPPP#",  # 23 exits(10,23)(11,23)
]

SANCTUM_MAP = _pad_map(SANCTUM_MAP_RAW, 30)

SANCTUM_BUILDINGS = {
    "cathedral_l": {
        "name": "Grand Cathedral of Light",
        "type": BLD_TEMPLE,
        "door": (11, 5),
        "color": (220, 220, 160),
        "label_pos": (3, 2),
        "npc_name": "High Priest Aldara",
    },
    "cathedral_r": {
        "name": "Grand Cathedral of Light",
        "type": BLD_TEMPLE,
        "door": (14, 5),
        "color": (220, 220, 160),
        "label_pos": (15, 2),
        "npc_name": "High Priest Aldara",
    },
    "inn": {
        "name": "The Pilgrim's Rest",
        "type": BLD_INN,
        "door": (9, 11),
        "color": (180, 170, 130),
        "label_pos": (6, 9),
        "npc_name": "Innkeeper Mala",
    },
    "shop": {
        "name": "Sacred Goods",
        "type": BLD_SHOP,
        "door": (18, 11),
        "color": (160, 180, 140),
        "label_pos": (17, 9),
        "npc_name": "Merchant Brin",
    },
    "temple": {
        "name": "Shrine of Healing",
        "type": BLD_TEMPLE,
        "door": (9, 18),
        "color": (200, 210, 180),
        "label_pos": (6, 16),
        "npc_name": "Healer Thessa",
    },
    "tavern": {
        "name": "The Candle and Cup",
        "type": BLD_TAVERN,
        "door": (18, 18),
        "color": (180, 160, 120),
        "label_pos": (17, 16),
        "npc_name": "Barkeep Pell",
    },
    "reliquary": {
        "name": "Reliquary",
        "type": BLD_HOUSE,
        "door": (10, 22),
        "color": (210, 200, 150),
        "label_pos": (8, 21),
        "npc_name": "Keeper Voss",
    },
}

SANCTUM_NPCS = [
    {
        "name": "Warden Liaison",
        "x": 12, "y": 10,
        "dialogue_id": "warden_liaison",
        "description": "A representative of the old Warden order. Weathered but watchful.",
        "color": (100, 175, 130),
        "npc_type": "warden",
    },
    {
        "name": "Pilgrim Elder",
        "x": 14, "y": 8,
        "dialogue_id": "pilgrim_elder",
        "description": "An old pilgrim who has walked to Sanctum three times in his life.",
        "color": (200, 190, 160),
    },
    {
        "name": "Holy Knight",
        "x": 14, "y": 13,
        "dialogue_id": "holy_knight",
        "description": "A knight in white and gold armor standing guard at the crossing.",
        "color": (220, 220, 200),
    },
    {
        "name": "Novice Priest",
        "x": 22, "y": 20,
        "dialogue_id": "novice_priest",
        "description": "A young priest walking the cloister path in quiet prayer.",
        "color": (180, 180, 220),
    },
]

SANCTUM_SIGNS = {
    (6, 14): "Notice: All weapons must be peace-bound within Sanctum's walls.",
    (3, 14): "Job Board — The Church posts charitable and protective work here.",
}

SANCTUM_SPAWN = (14, 22)
SANCTUM_EXIT = [(10, 23), (11, 23)]


# ══════════════════════════════════════════════════════════
#  CRYSTALSPIRE — Mage City (INT-focused, teleport hub)
# ══════════════════════════════════════════════════════════

# 32x24 — The Mage Academy dominates the north.
# Crystal tower in the center. Arcane feel.
# Teleport circle marked on path.
CRYSTALSPIRE_MAP_RAW = [
    "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",  # 0
    "T..............................T",  # 1
    "T..##########..####............T",  # 2
    "T..#........#..#..#............T",  # 3
    "T..#........#..#..#............T",  # 4
    "T..#........D..D..#............T",  # 5  academy(11,5)  library(15,5)
    "T..#........#..####............T",  # 6
    "T..##########..................T",  # 7
    "T......PPPPPPPPPPPPPPPPPPP.....T",  # 8  main street
    "T......P............P.....P....T",  # 9
    "T......P...####......P.####.P..T",  # 10
    "T......P...#..#......P.#..#.P..T",  # 11
    "T......P...#..D........D..#.P..T",  # 12 inn(12,12)      shop(21,12)
    "T......P...####......P.####.P..T",  # 13
    "T......P.....P.......P.P...P...T",  # 14
    "T......PPPPPP.P.PPP.PPPPPP.....T",  # 15 teleport circle at (16,15)
    "T......P......P..P..P..........T",  # 16
    "T......P..####...P.####........T",  # 17
    "T......P..#..#...P.#..#........T",  # 18
    "T......P..#..D.....D..#........T",  # 19 tavern(10,19)   temple(17,19)
    "T......P..####...P.####........T",  # 20
    "T......P........P..........P...T",  # 21
    "T......P..S.....P..........P...T",  # 22
    "TPPPPPPPPEEPPPPPPPPPPPPPPPPPPPPPT",  # 23 exits(9,23)(10,23)
]

CRYSTALSPIRE_MAP = _pad_map(CRYSTALSPIRE_MAP_RAW, 32)

CRYSTALSPIRE_BUILDINGS = {
    "academy": {
        "name": "Mage Academy",
        "type": BLD_HOUSE,
        "door": (11, 5),
        "color": (140, 160, 220),
        "label_pos": (3, 2),
        "npc_name": "Archmage Solen",
    },
    "library": {
        "name": "Arcane Library",
        "type": BLD_SHOP,
        "door": (15, 5),
        "color": (120, 140, 200),
        "label_pos": (13, 2),
        "npc_name": "Librarian Vex",
    },
    "inn": {
        "name": "The Floating Lantern",
        "type": BLD_INN,
        "door": (12, 12),
        "color": (160, 140, 200),
        "label_pos": (9, 10),
        "npc_name": "Innkeeper Zara",
    },
    "shop": {
        "name": "Components & Curios",
        "type": BLD_SHOP,
        "door": (21, 12),
        "color": (140, 160, 180),
        "label_pos": (19, 10),
        "npc_name": "Merchant Pell",
    },
    "tavern": {
        "name": "The Alembic",
        "type": BLD_TAVERN,
        "door": (13, 19),       # D is at col 13 on row 19
        "color": (160, 120, 180),
        "label_pos": (8, 17),
        "npc_name": "Barkeep Nim",
    },
    "temple": {
        "name": "Shrine of Arcane Truth",
        "type": BLD_TEMPLE,
        "door": (17, 19),
        "color": (180, 160, 220),
        "label_pos": (16, 17),
        "npc_name": "Priest Sael",
    },
}

CRYSTALSPIRE_NPCS = [
    {
        "name": "Warden Liaison",
        "x": 13, "y": 10,
        "dialogue_id": "warden_liaison",
        "description": "A representative of the old Warden order. Weathered but watchful.",
        "color": (100, 175, 130),
        "npc_type": "warden",
    },
    {
        "name": "Apprentice Mage",
        "x": 20, "y": 1,       # open area row 1 away from buildings
        "dialogue_id": "apprentice_mage",
        "description": "A student in blue robes practicing gestures under her breath.",
        "color": (160, 180, 240),
    },
    {
        "name": "Crystal Scholar",
        "x": 14, "y": 9,       # on main street path
        "dialogue_id": "crystal_scholar",
        "description": "A scholar studying the crystal formations in the street cobbles.",
        "color": (180, 200, 230),
    },
    {
        "name": "Teleport Master",
        "x": 14, "y": 15,      # adjacent to teleport circle (O tile), standing on P
        "dialogue_id": "teleport_master",
        "description": "A robed mage standing at the teleport circle. He nods in greeting.",
        "color": (200, 180, 255),
    },
    {
        "name": "Archmage Solen",
        "x": 12, "y": 5,
        "service": None,
        "dialogue_id": "archmage_solen",
        "description": "The Archmage of Crystalspire. Ancient, precise, and watching everything.",
        "color": (180, 200, 255),
    },
]

CRYSTALSPIRE_SIGNS = {
    (10, 22): "Teleport Circle — Guild members only. 50g per jump.",
    (10, 22): "Job Board — Arcane contracts and scholarly missions.",
}

CRYSTALSPIRE_SPAWN = (14, 22)
CRYSTALSPIRE_EXIT = [(9, 23), (10, 23)]


# ══════════════════════════════════════════════════════════
#  THORNHAVEN — Capital City (largest town, Act 2 hub)
# ══════════════════════════════════════════════════════════

# 38x28 — The capital. Castle in the NE. Imperial marketplace.
# Three distinct districts: market (west), civic (center), castle (east).
# Multiple guards, Iron-tier Governor inside the castle.
THORNHAVEN_MAP_RAW = [
    "######################################",  # 0
    "#....................................#",  # 1
    "#..####..####..####..............####",  # 2
    "#..#..#..#..#..#..#..............#..#",  # 3
    "#..#..D..D..#..#..D..............D..#",  # 4  inn(5,4) shop(8,4) guild(14,4)  castle_gate(33,4)
    "#..####.P####.P####..............####",  # 5  stubs for shop(8) guild(14)
    "#.......P.....P......................#",  # 6  stubs down to main road
    "#..PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP.#",  # 7  main imperial road
    "#..P................................#",  # 8
    "#..P..####..####....................#",  # 9
    "#..P..#..#..#..#....................#",  # 10
    "#..P..#..D..D..#....................#",  # 11 temple(9,11)  tavern(12,11)
    "#..P..####..####....................#",  # 12
    "#..P................................#",  # 13
    "#..P..S.............................#",  # 14
    "#..P................................#",  # 15
    "#..P..##########..####..............#",  # 16
    "#..P..#........#..#..#..............#",  # 17
    "#..P..#........#..#..#..............#",  # 18
    "#..P..#........D..D..#..............#",  # 19  marketplace(13,19) forge(17,19)
    "#..P..##########.P####..............##",  # 20
    "#..P.............P..................##",  # 21
    "#..P..####..####.P..................##",  # 22
    "#..P..#..#..#..#.P..................##",  # 23
    "#..P..#..D..D..#.P..................##",  # 24  barracks(9,24)  mages_hall(12,24)
    "#..P..####..####.P..................##",  # 25
    "#..P.............P..................##",  # 26
    "#PPPPPPPPPEEPPPPPPPPPPPPPPPPPPPPPPP#",  # 27  exits(10,27)(11,27)
]

THORNHAVEN_MAP = _pad_map(THORNHAVEN_MAP_RAW, 38)

THORNHAVEN_BUILDINGS = {
    "inn": {
        "name": "The Imperial Rest",
        "type": BLD_INN,
        "door": (5, 4),
        "color": (160, 140, 100),
        "label_pos": (3, 2),
        "npc_name": "Innkeeper Vance",
    },
    "shop": {
        "name": "Imperial Marketplace",
        "type": BLD_SHOP,
        "door": (8, 4),
        "color": (140, 160, 120),
        "label_pos": (6, 2),
        "npc_name": "Chief Merchant Ora",
    },
    "guild": {
        "name": "Adventurers' Guild",
        "type": BLD_HOUSE,
        "door": (14, 4),
        "color": (120, 130, 160),
        "label_pos": (12, 2),
        "npc_name": "Guild Commander Varek",
    },
    "castle_gate": {
        "name": "Governor's Castle",
        "type": BLD_HOUSE,
        "door": (33, 4),
        "color": (100, 100, 120),
        "label_pos": (27, 2),
        "npc_name": "Gate Captain Brynn",
    },
    "temple": {
        "name": "Grand Temple",
        "type": BLD_TEMPLE,
        "door": (9, 11),
        "color": (200, 200, 160),
        "label_pos": (7, 9),
        "npc_name": "Archpriest Davan",
    },
    "tavern": {
        "name": "The Crown & Candle",
        "type": BLD_TAVERN,
        "door": (12, 11),
        "color": (180, 140, 80),
        "label_pos": (10, 9),
        "npc_name": "Barkeep Lissa",
    },
    "marketplace": {
        "name": "Grand Bazaar",
        "type": BLD_SHOP,
        "door": (13, 19),
        "color": (160, 150, 110),
        "label_pos": (5, 16),
        "npc_name": "Bazaar Master Tren",
    },
    "forge": {
        "name": "Royal Forge",
        "type": BLD_FORGE,
        "door": (17, 19),
        "color": (200, 130, 50),
        "label_pos": (16, 17),
        "npc_name": "Royal Smith Hadra",
    },
    "barracks": {
        "name": "City Barracks",
        "type": BLD_HOUSE,
        "door": (9, 24),
        "color": (120, 130, 150),
        "label_pos": (6, 22),
        "npc_name": "Captain of the Guard",
    },
    "mages_hall": {
        "name": "Mages' Hall",
        "type": BLD_HOUSE,
        "door": (12, 24),
        "color": (130, 120, 180),
        "label_pos": (10, 22),
        "npc_name": "Court Mage Sira",
    },
}

THORNHAVEN_NPCS = [
    {
        "name": "Warden Liaison",
        "x": 14, "y": 11,
        "dialogue_id": "warden_liaison",
        "description": "A representative of the old Warden order. Weathered but watchful.",
        "color": (100, 175, 130),
        "npc_type": "warden",
    },
    # Story/ambient NPCs
    {
        "name": "City Guard",
        "x": 16, "y": 7,
        "dialogue_id": "city_guard_thornhaven",
        "description": "An armored guard in imperial livery. There are more of them than you'd like.",
        "color": (160, 170, 190),
    },
    {
        "name": "City Guard",
        "x": 25, "y": 7,
        "dialogue_id": "city_guard_thornhaven",
        "description": "Another imperial guard. They nod at each other on the hour.",
        "color": (160, 170, 190),
    },
    {
        "name": "Imperial Crier",
        "x": 16, "y": 13,
        "dialogue_id": "imperial_crier",
        "description": "A herald reading proclamations from a scroll. Nobody is listening.",
        "color": (200, 180, 130),
    },
    {
        "name": "Merchant Noble",
        "x": 22, "y": 4,
        "dialogue_id": "merchant_noble",
        "description": "A wealthy merchant in silk and furs, looking impatient.",
        "color": (200, 160, 100),
    },
    {
        "name": "Refugee",
        "x": 6, "y": 26,
        "dialogue_id": "refugee",
        "description": "A gaunt figure sitting against the wall. Fading scars on their hands.",
        "color": (140, 130, 120),
    },
    # Key story NPCs
    {
        "name": "Governor Aldric",
        "x": 32, "y": 4,  # near castle gate
        "dialogue_id": "governor_aldric",
        "description": "The Imperial Governor of Thornhaven. Looks like he hasn't slept in a week.",
        "color": (180, 160, 120),
    },
    {
        "name": "Guild Commander Varek",
        "x": 13, "y": 4,  # near guild hall door (14,4)
        "dialogue_id": "guild_commander_varek",
        "description": "A hard-faced woman running the Imperial Guild. She knows more than she says.",
        "color": (140, 150, 180),
    },
    {
        "name": "Court Mage Sira",
        "x": 13, "y": 24,  # near mages_hall door (12,24)
        "dialogue_id": "court_mage_sira",
        "description": "The court mage of the Empire. Her eyes track more than they let on.",
        "color": (160, 140, 220),
    },
    # Service NPCs
]

THORNHAVEN_SIGNS = {
    (7, 14): "Imperial Notice Board — By order of the Governor.",
    (6, 14): "Job Board — Military contracts and civic duties posted daily.",
}

THORNHAVEN_SPAWN = (14, 26)
THORNHAVEN_EXIT = [(10, 27), (11, 27)]

TOWN_MAPS = {
    "briarhollow": {
        "name": "Briarhollow",
        "map": BRIARHOLLOW_MAP,
        "width": 60,
        "height": 34,
        "buildings": BRIARHOLLOW_BUILDINGS,
        "npcs": BRIARHOLLOW_NPCS,
        "signs": BRIARHOLLOW_SIGNS,
        "spawn": BRIARHOLLOW_SPAWN,
        "exits": BRIARHOLLOW_EXIT,
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
    },
    "greenwood": {
        "name": "Greenwood",
        "map": GREENWOOD_MAP,
        "width": 24,
        "height": 20,
        "buildings": GREENWOOD_BUILDINGS,
        "npcs": GREENWOOD_NPCS,
        "signs": GREENWOOD_SIGNS,
        "spawn": GREENWOOD_SPAWN,
        "exits": GREENWOOD_EXIT,
    },
    "saltmere": {
        "name": "Saltmere",
        "map": SALTMERE_MAP,
        "width": 28,
        "height": 22,
        "buildings": SALTMERE_BUILDINGS,
        "npcs": SALTMERE_NPCS,
        "signs": SALTMERE_SIGNS,
        "spawn": SALTMERE_SPAWN,
        "exits": SALTMERE_EXIT,
    },
    "sanctum": {
        "name": "Sanctum",
        "map": SANCTUM_MAP,
        "width": 30,
        "height": 24,
        "buildings": SANCTUM_BUILDINGS,
        "npcs": SANCTUM_NPCS,
        "signs": SANCTUM_SIGNS,
        "spawn": SANCTUM_SPAWN,
        "exits": SANCTUM_EXIT,
    },
    "crystalspire": {
        "name": "Crystalspire",
        "map": CRYSTALSPIRE_MAP,
        "width": 32,
        "height": 24,
        "buildings": CRYSTALSPIRE_BUILDINGS,
        "npcs": CRYSTALSPIRE_NPCS,
        "signs": CRYSTALSPIRE_SIGNS,
        "spawn": CRYSTALSPIRE_SPAWN,
        "exits": CRYSTALSPIRE_EXIT,
    },
    "thornhaven": {
        "name": "Thornhaven",
        "map": THORNHAVEN_MAP,
        "width": 38,
        "height": 28,
        "buildings": THORNHAVEN_BUILDINGS,
        "npcs": THORNHAVEN_NPCS,
        "signs": THORNHAVEN_SIGNS,
        "spawn": THORNHAVEN_SPAWN,
        "exits": THORNHAVEN_EXIT,
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
    """Get NPC dict at position (x,y). Returns None if no NPC or if NPC is hidden."""
    from core.story_flags import get_flag
    for npc in town_data.get("npcs", []):
        if npc["x"] == x and npc["y"] == y:
            hide_flag = npc.get("hide_if")
            if hide_flag and get_flag(hide_flag):
                return None
            return npc
    return None


def get_sign_at(town_data, x, y):
    """Get sign text at position. Returns None if no sign."""
    return town_data.get("signs", {}).get((x, y))


def is_exit(town_data, x, y):
    """Check if tile is a town exit."""
    return (x, y) in town_data.get("exits", [])


# ══════════════════════════════════════════════════════════
#  GREENWOOD — Wilderness Outpost (remote, no teleport)
# ══════════════════════════════════════════════════════════

# 24x20 — Small forest clearing. Dense trees on all sides.
# One winding path, basic services only. Feels remote and rough.