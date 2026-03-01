"""
Realm of Shadows — 8-bit Pixel Art Sprites
Wizardry / Ultima II aesthetic: chunky pixels, flat colors, hard edges.
No antialiasing — uses pygame.transform.scale exclusively.

Each sprite is defined as a list of strings, one character per pixel.
Color key (per sprite, overridable):
  '.' = transparent
  'S' = skin/flesh
  'H' = hair / hood base
  'C' = primary class color
  'D' = dark variant of C (shadow/outline)
  'M' = metal / armor
  'G' = gold / trim
  'W' = weapon color
  'E' = eye / accent (bright)
  'K' = dark background fill
  'R' = red accent
  'P' = purple accent
  'N' = brown / natural

Canonical grid size: 12 wide × 20 tall for characters,
                     14 wide × 18 tall for enemies.
Scaled to fit target rect with integer or float scaling (no smoothscale).

Public API (drop-in for silhouettes.py):
  draw_character_silhouette(surface, rect, class_name, ...)
  draw_enemy_silhouette(surface, rect, enemy_template_key, ...)
  CLASS_COLORS  — dict matching silhouettes.py export
"""

import pygame


# ═══════════════════════════════════════════════════════════════
#  CLASS COLOR PALETTE  (kept identical to silhouettes.py)
# ═══════════════════════════════════════════════════════════════

CLASS_COLORS = {
    # Base
    "Fighter":       (180, 100,  60),
    "Mage":          ( 80, 120, 220),
    "Cleric":        (220, 200, 100),
    "Thief":         (100, 180, 120),
    "Ranger":        ( 80, 160,  80),
    "Monk":          (200, 140,  60),
    # Hybrid
    "Warder":        (160,  80,  40),
    "Paladin":       (220, 200, 140),
    "Assassin":      ( 60, 160,  80),
    "Warden":        ( 60, 140,  60),
    "Spellblade":    (100, 100, 200),
    "Templar":       (200, 160,  80),
    # Advanced
    "Champion":      (220, 120,  60),
    "Crusader":      (240, 220, 140),
    "Shadow Master": ( 40, 140,  80),
    "Beastlord":     ( 80, 160,  80),
    "Archmage":      ( 80, 100, 240),
    "High Priest":   (240, 220, 160),
    # Special
    "Witch":         (160,  80, 200),
    "Necromancer":   ( 80,  60, 160),
}

# Knowledge tier tints for enemies
TIER_TINTS = {
    -1: ( 30,  25,  40),
     0: ( 70,  65,  85),
     1: (130, 120, 140),
     2: None,             # full color
}


# ═══════════════════════════════════════════════════════════════
#  SPRITE DEFINITIONS — 12×20 character grid
# ═══════════════════════════════════════════════════════════════
# Each entry: {"grid": [...], "palette": {...}, "base_w": 12, "base_h": 20}

def _c(r, g, b): return (r, g, b, 255)

SKIN   = _c(220, 175, 130)
SKIN_D = _c(175, 130,  90)
HAIR_B = _c( 60,  40,  20)  # dark brown hair
HAIR_R = _c(160,  60,  30)  # red hair
METAL  = _c(170, 170, 185)
METAL_D= _c(110, 110, 125)
GOLD   = _c(210, 180,  50)
WOOD   = _c(130,  85,  40)
WHITE  = _c(240, 240, 240)
BLACK  = _c( 20,  15,  25)

def _dim(c, factor=0.45):
    return _c(int(c[0]*factor), int(c[1]*factor), int(c[2]*factor))

def _bright(c, add=60):
    return _c(min(255,c[0]+add), min(255,c[1]+add), min(255,c[2]+add))


# ── CHARACTER GRIDS ─────────────────────────────────────────

# Shared: fighter-type body (upright, broad)
_FIGHTER_GRID = [
    ".....HH.....",  # 0
    "....HHHH....",  # 1 — helmet
    "....SMMS....",  # 2 — face visor gap
    "...MMMMMM...",  # 3 — gorget
    "..DMMMMMMD..",  # 4 — shoulders
    "..MMMMMMM...",  # 5 — chest
    "..MGGGGGM...",  # 6 — belt
    "...MMMMMM...",  # 7 — lower body
    "W..MM..MM.W.",  # 8 — arm + legs
    "WW.MM..MM.W.",  # 9
    ".WWMM..MM...",  # 10
    "...MM..MM...",  # 11
    "...MM..MM...",  # 12
    "...MM..MM...",  # 13
    "..DMM..MMD..",  # 14
    "..MMM..MMM..",  # 15
    ".KMMM..MMMK.",  # 16
    "..MMM..MMM..",  # 17
    "..DDD..DDD..",  # 18 — feet
    "............",  # 19
]

_FIGHTER_PAL = {
    'H': _c(80,80,100),   # helmet dark steel
    'S': SKIN,
    'M': METAL,
    'D': METAL_D,
    'G': GOLD,
    'W': _c(200,190,180), # sword blade
    'K': BLACK,
}

# Mage: tall robe, staff
_MAGE_GRID = [
    "....CCCCC...",  # 0  pointed hat
    "...CCCCCCC..",  # 1
    "...CCCCCCC..",  # 2
    "....SSSSS...",  # 3  face
    "....SESES...",  # 4  face+eyes
    ".W..DCCCD..W",  # 5  shoulders + staff
    ".W..CCCCC..W",  # 6
    ".W..CCCCC..W",  # 7  robe body
    ".W.CCCCCCC.W",  # 8
    ".W.CCCCCCC.W",  # 9
    ".W.CCCCCCC.W",  # 10
    ".WW.CCCCC.WW",  # 11  sleeves
    "..W.DCCCD.W.",  # 12
    "..W..CCC..W.",  # 13
    "..W..CCC..W.",  # 14
    "..EW.CCC..W.",  # 15  orb on staff
    "....DCCCD...",  # 16  robe hem
    "....DCDCD...",  # 17
    ".....DDD....",  # 18  feet
    "............",  # 19
]

_MAGE_PAL = {
    'C': None,           # primary class color (filled at render time)
    'D': None,           # dim of C
    'S': SKIN,
    'E': _c(200,220,255),
    'W': WOOD,
}

# Cleric: robes + holy symbol + mace
_CLERIC_GRID = [
    "....CCCCC...",  # 0  hood
    "...CCCCCCC..",  # 1
    "....SSSSS...",  # 2  face
    "....SESES...",  # 3
    "...DDDDDDD..",  # 4  collar
    "W..CCGGGCC.W",  # 5  robe top  G=cross
    "W..CGGGGCC.W",  # 6
    "W..CCGGGCC.W",  # 7
    "W..CCCCCCC.W",  # 8
    ".W.CCCCCCC.W",  # 9
    ".W.CCCCCCC.W",  # 10
    ".WW.CCCCC.WW",  # 11
    "..W.DCCCD.W.",  # 12
    "..WW.CCC.WW.",  # 13
    "....DCDCD...",  # 14
    "....DCDCD...",  # 15
    ".....DDD....",  # 16  feet
    "............",  # 17
    "............",  # 18
    "............",  # 19
]

_CLERIC_PAL = {
    'C': None,
    'D': None,
    'S': SKIN,
    'E': _c(60,60,60),
    'G': GOLD,
    'W': _c(190,180,170),
}

# Thief: lean, crouched, two daggers
_THIEF_GRID = [
    "......HHH...",  # 0
    ".....HHHH...",  # 1
    "....SSSSS...",  # 2
    "....SESES...",  # 3
    "....DCCCD...",  # 4  collar/cape
    "W...CCCCCC..",  # 5
    "WW..CCCCCC..",  # 6
    ".W..CCCCC...",  # 7
    ".W..CCCCC...",  # 8
    "....CCCCC..W",  # 9  other dagger
    "....CCCCC.WW",  # 10
    "....CCCCC.W.",  # 11
    "...DCCCCCD..",  # 12
    "...CC..CC...",  # 13
    "..DCC..CCD..",  # 14
    "..CC....CC..",  # 15
    "..CC....CC..",  # 16
    ".KCC....CCK.",  # 17  boots
    "..KK....KK..",  # 18
    "............",  # 19
]

_THIEF_PAL = {
    'H': HAIR_B,
    'C': None,
    'D': None,
    'S': SKIN,
    'E': _c(60,60,60),
    'W': _c(200,195,190),
    'K': BLACK,
}

# Ranger: lean, bow raised
_RANGER_GRID = [
    ".....HHH....",  # 0
    "....HHHH....",  # 1
    "....SSSS....",  # 2
    "....SESS....",  # 3
    "....DCCD....",  # 4  hood/collar
    "....CCCC...W",  # 5
    "WW..CCCC...W",  # 6  bow string
    "W...CCCC...W",  # 7
    ".W..CCCC..WW",  # 8
    "..W.CCCC.WW.",  # 9
    "...WCCCCCW..",  # 10
    "....CCCCC...",  # 11
    "...DCCCCCD..",  # 12
    "...CC..CCC..",  # 13
    "..DCC..CCD..",  # 14
    "..CC....CC..",  # 15
    "..CC....CC..",  # 16
    ".NCC....CCN.",  # 17  boots
    "..NN....NN..",  # 18
    "............",  # 19
]

_RANGER_PAL = {
    'H': _c(120,80,40),
    'C': None,
    'D': None,
    'S': SKIN,
    'E': _c(60,60,60),
    'W': _c(210,200,180),  # bow limb
    'N': _c(80,55,30),     # leather boots
}

# Monk: bare arms, fighting stance, ki aura hint
_MONK_GRID = [
    ".....HHH....",  # 0
    ".....HHH....",  # 1
    ".....SSS....",  # 2
    "....SSESS...",  # 3
    "....DCCD....",  # 4
    "...SSCCSS...",  # 5  bare arms
    "..SSSCCSS...",  # 6
    ".SSS.CCC.SS.",  # 7  arms wide
    "SSS..CCC..SS",  # 8
    "....CCCCC...",  # 9
    "....CCCCC...",  # 10
    "...DCCCCD...",  # 11
    "....CC.CC...",  # 12  legs split
    "...DCC.CCD..",  # 13
    "...CC...CC..",  # 14
    "...CC...CC..",  # 15
    "...CC...CC..",  # 16
    "..KCC...CCK.",  # 17
    "..KK.....KK.",  # 18
    "............",  # 19
]

_MONK_PAL = {
    'H': HAIR_B,
    'C': None,
    'D': None,
    'S': SKIN,
    'E': _c(60,60,60),
    'K': _c(60,45,30),
}

# Paladin: heavy fighter, golden halo dots, white cape
_PALADIN_GRID = [
    "..G.MMMMM.G.",  # 0  helmet + halo
    "...MMMMMMM..",  # 1
    "...MSMMSM..",   # 2  visor
    "..MMMMMMMM..",  # 3
    ".DMMMMMMMMD.",  # 4  pauldrons
    ".MMMMMMMMMM.",  # 5
    ".MGGGGGGGMM.",  # 6  tabard gold cross
    ".MMMMMMMMMM.",  # 7
    "WW.MMMMMM.WW",  # 8
    "W..MMMMMM..W",  # 9
    "...MMMMMM...",  # 10
    "...MMMMMM...",  # 11
    "..DMMMMMMD..",  # 12
    "..MMMMMMMM..",  # 13
    "..MMMMMMMM..",  # 14
    ".KMMMMMMMK..",  # 15
    "..MMMMMMMM..",  # 16
    "..MMMMMMMM..",  # 17
    "..DDDDDDDD..",  # 18
    "............",  # 19
]

_PALADIN_PAL = {
    'M': METAL,
    'D': METAL_D,
    'G': GOLD,
    'S': SKIN,
    'W': METAL,
    'K': BLACK,
}

# Assassin: cloaked, shadowy, two sai
_ASSASSIN_GRID = [
    ".....KKK....",  # 0  cowl
    "....KKKKKK..",  # 1
    "....KKKKKKK.",  # 2
    "....KSKKSSK.",  # 3
    "...KCCCCCCCK",  # 4
    "W..KCCCCCCK..",# 5
    "WW.KCCCCCCK..",# 6
    ".W.KCCCCCCK..",# 7
    ".W.KCCCCCCK..",# 8
    "...KCCCCCK.WW",# 9
    "...KCCCCCK.W.",# 10
    "..DKCCCCCKD..",# 11
    "..KCCCCCCCK..",# 12
    "..KC....CK..",# 13
    ".DKC....CKD.",# 14
    ".KC......CK.",# 15
    ".KC......CK.",# 16
    ".KC......CK.",# 17
    ".KK......KK.",# 18
    "............",# 19
]

_ASSASSIN_PAL = {
    'K': BLACK,
    'C': None,
    'D': None,
    'S': SKIN,
    'W': _c(190,185,180),
}

# Warder: fighter variant — darker iron + red cape
_WARDER_GRID = _FIGHTER_GRID  # reuse fighter grid
_WARDER_PAL  = {
    'H': _c(50,40,35),
    'S': SKIN,
    'M': _c(140,130,140),
    'D': _c(80,70,80),
    'G': _c(160,40,30),    # red trim instead of gold
    'W': _c(180,170,165),
    'K': BLACK,
}

# Warden: ranger + antler accent
_WARDEN_GRID = [
    ".N..NHHHN.N.",  # 0  antlers + hood
    "..N.HHHHH.N.",  # 1
    "....HHHH....",  # 2
    "....SSSS....",  # 3
    "....SESS....",  # 4
    "....DCCD....",  # 5
    "....CCCC...W",  # 6
    "WW..CCCC...W",  # 7
    "W...CCCC...W",  # 8
    ".W..CCCC..WW",  # 9
    "..W.CCCC.WW.",  # 10
    "...WCCCCCW..",  # 11
    "....CCCCC...",  # 12
    "...DCCCCCD..",  # 13
    "...CC..CCC..",  # 14
    "..DCC..CCD..",  # 15
    "..CC....CC..",  # 16
    ".NCC....CCN.",  # 17
    "..NN....NN..",  # 18
    "............",  # 19
]

_WARDEN_PAL = {
    'H': _c(110,75,35),
    'C': None,
    'D': None,
    'S': SKIN,
    'E': _c(60,60,60),
    'W': _c(180,160,130),
    'N': _c(100,70,30),
}

# Spellblade: mage robe + sword in other hand
_SPELLBLADE_GRID = [
    "....CCCCC...",  # 0  pointed hat
    "...CCCCCCC..",  # 1
    "...CCCCCCC..",  # 2
    "....SSSSS...",  # 3
    "....SESES...",  # 4
    ".W..DCCCD..M",  # 5  staff left, sword right
    ".W..CCCCC..M",  # 6
    ".W..CCCCC..M",  # 7
    ".WW.CCCCC.MM",  # 8
    "..W.CCCCC.M.",  # 9
    "..W.CCCCC.M.",  # 10
    "...WCCCCCMM.",  # 11
    "....DCCCD...",  # 12
    "....DCDCD...",  # 13
    ".....DDD....",  # 14
    "....DDDDD...",  # 15
    "....DDDDD...",  # 16
    "....DDDDD...",  # 17
    ".....DDD....",  # 18
    "............",  # 19
]

_SPELLBLADE_PAL = {
    'C': None,
    'D': None,
    'S': SKIN,
    'E': _c(200,220,255),
    'W': WOOD,
    'M': METAL,
}

# Templar: heavy cleric — crusader style
_TEMPLAR_GRID = [
    "..G.MMMMM.G.",  # 0  plumed helmet
    "...MMMMMMM..",  # 1
    "...CMMMMCM..",  # 2  colored crest
    "...MSMMSM...",  # 3
    ".DMMMMMMMMD.",  # 4
    ".MMMCCCMMMM.",  # 5  cross on chest
    ".MMMCCCMMMM.",  # 6
    ".MMMMMMMMM..",  # 7
    "W..MMMMMM..W",  # 8
    "W..MMMMMM..W",  # 9
    "...MMMMMM...",  # 10
    "..CMMMMMMC..",  # 11
    "..MMMMMMMM..",  # 12
    "..MMMMMMMM..",  # 13
    "..MMMMMMMM..",  # 14
    "..MMMMMMMM..",  # 15
    "..MMMMMMMM..",  # 16
    "..MMMMMMMM..",  # 17
    "..DDDDDDDD..",  # 18
    "............",  # 19
]

_TEMPLAR_PAL = {
    'M': METAL,
    'D': METAL_D,
    'G': GOLD,
    'C': None,
    'S': SKIN,
    'W': METAL,
}

# Champion: massive fighter, battle aura
_CHAMPION_GRID = [
    "G..MMMMMMM.G",  # 0  crowned helmet + side flames
    "...MMMMMMM..",  # 1
    "...MSMSMM...",  # 2
    "..MMMMMMMM..",  # 3
    ".DMMMMMMMMMD", # 4  huge pauldrons
    "WMMMMMMMMMM.",  # 5
    "WMGGGGGGGMM.",  # 6
    "WMMMMMMMMMM.",  # 7
    "WWW.MMMMM.WW",  # 8
    "WW..MMMMM..W",  # 9
    "....MMMMM...",  # 10
    "....MMMMM...",  # 11
    "...DMMMMMD..",  # 12
    "...MMMMMMM..",  # 13
    "...MMMMMMM..",  # 14
    "..KMMMMMMK..",  # 15
    "..MMMMMMMM..",  # 16
    "..MMMMMMMM..",  # 17
    "..DDDDDDDD..",  # 18
    "............",  # 19
]

_CHAMPION_PAL = {
    'M': _c(190,195,210),
    'D': _c(120,125,140),
    'G': GOLD,
    'S': SKIN,
    'W': _c(215,210,200),
    'K': BLACK,
}

# Crusader: paladin upgraded — gold everywhere
_CRUSADER_GRID = _PALADIN_GRID
_CRUSADER_PAL  = {
    'M': _c(210,200,150),  # gilded armor
    'D': _c(160,145,80),
    'G': GOLD,
    'S': SKIN,
    'W': GOLD,
    'K': BLACK,
}

# Shadow Master: assassin, darker, shadow tendrils
_SHADOW_MASTER_GRID = _ASSASSIN_GRID
_SHADOW_MASTER_PAL  = {
    'K': _c(10,8,18),
    'C': None,
    'D': None,
    'S': _c(170,155,175),  # pale skin
    'W': _c(60,50,80),
}

# Beastlord: ranger with fur mantle
_BEASTLORD_GRID = [
    ".N..NHHHN.N.",  # 0  antlers
    "..N.HHHHH.N.",  # 1
    "....HHHH....",  # 2
    "....SSSS....",  # 3
    "....SESS....",  # 4
    "NNNN.CC.NNNN",  # 5  fur mantle
    "NNN..CC..NNN",  # 6
    ".N...CC...N.",  # 7
    "W....CC....W",  # 8
    ".W...CC...W.",  # 9
    "..WWCCCWW..",  # 10
    "....CCCCC...",  # 11
    "...DCCCCCD..",  # 12
    "...CC..CCC..",  # 13
    "..DCC..CCD..",  # 14
    "..CC....CC..",  # 15
    "..CC....CC..",  # 16
    ".NCC....CCN.",  # 17
    "..NN....NN..",  # 18
    "............",  # 19
]

_BEASTLORD_PAL = {
    'H': _c(115,80,40),
    'C': None,
    'D': None,
    'S': SKIN,
    'E': _c(60,60,60),
    'W': _c(180,160,130),
    'N': _c(130,90,45),
}

# Archmage: tall mage + arcane circle halo
_ARCHMAGE_GRID = [
    "E...CCCCC..E",  # 0  hat + arcane sparks
    "....CCCCCCC.",  # 1
    "E..CCCCCCCCE",  # 2
    "....SSSSSSS.",  # 3
    "....SESESES.",  # 4  multiple eye whites
    ".W.DDCCCCD.W",  # 5  dual staves
    ".W..CCCCC..W",  # 6
    ".W..CCCCC..W",  # 7
    ".W.CCCCCCC.W",  # 8
    "EW.CCCCCCC.W",  # 9
    ".W.CCCCCCC.W",  # 10
    ".WW.CCCCC.WW",  # 11
    "..W.DCCCD.W.",  # 12
    "..WE.CCC.EW.",  # 13
    "....DCCCD...",  # 14
    "....DCDCD...",  # 15
    ".E...DDD...E",  # 16
    ".....DDD.....",  # 17
    "............",  # 18
    "............",  # 19
]

_ARCHMAGE_PAL = {
    'C': None,
    'D': None,
    'S': SKIN,
    'E': _c(180,210,255),
    'W': _c(160,140,200),
}

# High Priest: elaborate cleric with radiant crown
_HIGH_PRIEST_GRID = [
    ".G.GCCCCCG.G",  # 0  radiant crown rays
    "..GCCCCCCG..",  # 1
    "...CCGGGCC..",  # 2  crown band
    "....SSSSS...",  # 3
    "....SESES...",  # 4
    "G..DCCCCCCD.",  # 5  mantle + glow
    ".W.CCCCCCC.W",  # 6
    ".W.CGCCCGC.W",  # 7  holy symbols
    ".W.CCCCCCC.W",  # 8
    ".W.CCCCCCC.W",  # 9
    ".W.CCCCCCC.W",  # 10
    ".WW.CCCCC.WW",  # 11
    "..W.DCCCD.W.",  # 12
    "....DCCCD...",  # 13
    "....DCDCD...",  # 14
    "....DCDCD...",  # 15
    ".G...DDD...G",  # 16
    ".....DDD.....",  # 17
    "............",  # 18
    "............",  # 19
]

_HIGH_PRIEST_PAL = {
    'C': None,
    'D': None,
    'S': SKIN,
    'E': _c(60,60,60),
    'G': GOLD,
    'W': GOLD,
}

# Witch: mage with big pointed hat + broom
_WITCH_GRID = [
    "....PPPPP...",  # 0  hat tip
    "...PPPPPPP..",  # 1
    "..PPPPPPPPP.",  # 2
    ".PPPPPPPPPP.",  # 3  wide brim
    "....SSSSS...",  # 4
    "....SESES...",  # 5
    ".W..PCCCP..W",  # 6  robe shoulders
    ".W..PCCCP..W",  # 7
    ".W..CCCCC..W",  # 8
    ".W.CCCCCCC.W",  # 9
    ".W.CCCCCCC.W",  # 10
    ".WW.CCCCC.WW",  # 11
    "..W.DCCCD.W.",  # 12
    "....DCCCD...",  # 13
    "....DCDCD...",  # 14
    "....DCDCD...",  # 15
    ".....DDD....",  # 16
    "............",  # 17
    "............",  # 18
    "............",  # 19
]

_WITCH_PAL = {
    'C': None,
    'D': None,
    'P': _c(100,30,120),  # hat
    'S': SKIN,
    'E': _c(60,60,60),
    'W': _c(140,110,60),  # broom handle
}

# Necromancer: mage + skull motif + bone colors
_NECROMANCER_GRID = [
    "....CCCCC...",  # 0
    "...CCCCCCC..",  # 1
    "...CCCCCCC..",  # 2
    "....SSSSS...",  # 3
    "...EESEEE...",  # 4  glowing eyes
    ".W..DCCCD..W",  # 5
    ".W..CCCCC..W",  # 6
    ".W..CCCCC..W",  # 7
    ".W.CCCCCCC.W",  # 8
    ".W.CEECCEEC.W", # 9  skull motifs
    ".W.CCCCCCC.W",  # 10
    ".WW.CCCCC.WW",  # 11
    "..W.DCCCD.W.",  # 12
    "..W..CCC..W.",  # 13
    "....DCCCD...",  # 14
    "....DCDCD...",  # 15
    ".....DDD....",  # 16
    "............",  # 17
    "............",  # 18
    "............",  # 19
]

_NECROMANCER_PAL = {
    'C': None,
    'D': None,
    'S': _c(195,185,175),  # pale
    'E': _c(150,240,180),  # ghastly glow
    'W': _c(220,215,200),  # bone staff
}


# ── Master character sprite registry ─────────────────────────
_CHAR_SPRITES = {
    "Fighter":       (_FIGHTER_GRID,      _FIGHTER_PAL),
    "Mage":          (_MAGE_GRID,         _MAGE_PAL),
    "Cleric":        (_CLERIC_GRID,       _CLERIC_PAL),
    "Thief":         (_THIEF_GRID,        _THIEF_PAL),
    "Ranger":        (_RANGER_GRID,       _RANGER_PAL),
    "Monk":          (_MONK_GRID,         _MONK_PAL),
    "Warder":        (_WARDER_GRID,       _WARDER_PAL),
    "Paladin":       (_PALADIN_GRID,      _PALADIN_PAL),
    "Assassin":      (_ASSASSIN_GRID,     _ASSASSIN_PAL),
    "Warden":        (_WARDEN_GRID,       _WARDEN_PAL),
    "Spellblade":    (_SPELLBLADE_GRID,   _SPELLBLADE_PAL),
    "Templar":       (_TEMPLAR_GRID,      _TEMPLAR_PAL),
    "Champion":      (_CHAMPION_GRID,     _CHAMPION_PAL),
    "Crusader":      (_CRUSADER_GRID,     _CRUSADER_PAL),
    "Shadow Master": (_SHADOW_MASTER_GRID,_SHADOW_MASTER_PAL),
    "Beastlord":     (_BEASTLORD_GRID,    _BEASTLORD_PAL),
    "Archmage":      (_ARCHMAGE_GRID,     _ARCHMAGE_PAL),
    "High Priest":   (_HIGH_PRIEST_GRID,  _HIGH_PRIEST_PAL),
    "Witch":         (_WITCH_GRID,        _WITCH_PAL),
    "Necromancer":   (_NECROMANCER_GRID,  _NECROMANCER_PAL),
}


# ═══════════════════════════════════════════════════════════════
#  ENEMY SPRITE DEFINITIONS — 14×18 grid
# ═══════════════════════════════════════════════════════════════
# Enemy palette uses C = primary color, D = dark, E = eye/accent

_GOBLIN_WARRIOR_GRID = [
    "......HH......",  # 0
    ".....HHHH.....",  # 1  pointy ears
    "E...HSSSSHE...",  # 2  big ears + face
    "....SSSSSS....",  # 3
    "....SESSSES...",  # 4  eyes
    "....CCCCCC....",  # 5  rough armor
    "W...CCCCCC...W",  # 6
    "WW..CCCCCC..W.",  # 7
    "W...CCCCCC..WW",  # 8
    "....DCCCCD....",  # 9
    "....CC..CC....",  # 10
    "....CC..CC....",  # 11
    "...DCC..CCD...",  # 12
    "...CC....CC...",  # 13
    "..KCC....CCK..",  # 14
    "..KK......KK..",  # 15
    "..............",  # 16
    "..............",  # 17
]

_GOBLIN_ARCHER_GRID = [
    "......HH......",  # 0
    ".....HHHH.....",  # 1
    "E...HSSSSHE...",  # 2
    "....SSSSSS....",  # 3
    "....SESSSES...",  # 4
    "WW..CCCCCC....",  # 5  bow drawn
    "W...CCCCCC....",  # 6
    "W...CCCCCC..WW",  # 7  bow string right
    ".W..CCCCCC.W..",  # 8
    "..WWDCCCCD....",  # 9
    "....CC..CC....",  # 10
    "....CC..CC....",  # 11
    "...DCC..CCD...",  # 12
    "...CC....CC...",  # 13
    "..KCC....CCK..",  # 14
    "..KK......KK..",  # 15
    "..............",  # 16
    "..............",  # 17
]

_GOBLIN_BRUTE_GRID = [
    ".....CHHHHC...",  # 0
    "....CHHHHHHHC.",  # 1
    "E..HSSSSSSSH.E",  # 2
    "...SSSSSSSSSS.",  # 3
    "..DSESSSSESSD.",  # 4
    "..CCCCCCCCCC..",  # 5
    "W.DCCCCCCCCD.W",  # 6
    "WW.CCCCCCCC.WW",  # 7
    "W..CCCCCCCC..W",  # 8
    "W..DCCCCCCD..W",  # 9
    "...CC....CC...",  # 10
    "...CC....CC...",  # 11
    "..DCC....CCD..",  # 12
    "..CC......CC..",  # 13
    ".KCC......CCK.",  # 14
    ".KK........KK.",  # 15
    "..............",  # 16
    "..............",  # 17
]

_ORC_WARRIOR_GRID = [
    "....CHHHHC....",  # 0
    "...CHHHHHHHC..",  # 1
    "...CSSSSSSSC..",  # 2
    "..DSESESSSD...",  # 3  tusks visible
    "..STTSSSSTT...",  # 4  T=tusk white
    "..CMMMMMMMC..",  # 5  heavy armor
    "W.CMMMMMMMC.W",  # 6
    "WW.MMMMMMM.WW",  # 7
    ".W.MMMMMMM.W.",  # 8
    "...DMMMMMD...",  # 9
    "...MM....MM...",  # 10
    "...MM....MM...",  # 11
    "..DMM....MMD..",  # 12
    "..MM......MM..",  # 13
    ".KMM......MMK.",  # 14
    ".KK........KK.",  # 15
    "..............",  # 16
    "..............",  # 17
]

_ORC_WARRIOR_PAL = {
    'C': _c(80,110,60),   # greenish orc skin
    'D': _c(50,70,35),
    'S': _c(110,145,80),  # lighter orc green
    'E': _c(200,30,30),   # red eyes
    'M': METAL,
    'T': WHITE,
    'H': _c(60,40,15),
    'W': METAL,
    'K': BLACK,
}

_SKELETON_GRID = [
    ".....BBBBB....",  # 0  B=bone white
    "....BBBBBBB...",  # 1  skull
    "...BBBDBBDBB..",  # 2  eye sockets
    "...BB.BBB.BB..",  # 3
    "....BBBBBBB...",  # 4
    "....BBBBBB....",  # 5  neck
    ".W..DBBBBD..W.",  # 6  ribcage
    ".W..BBBBBB..W.",  # 7
    ".W..BBBBBB..W.",  # 8
    "....BBBBBB....",  # 9
    "....BB..BB....",  # 10  hip
    "....BB..BB....",  # 11
    "...DBB..BBD...",  # 12
    "...BB....BB...",  # 13
    "..DBB....BBD..",  # 14
    "..BB......BB..",  # 15
    "..BB......BB..",  # 16
    "..BB......BB..",  # 17
]

_SKELETON_PAL = {
    'B': _c(220,215,195),
    'D': _c(140,135,115),
    'W': _c(190,175,160),  # rusty sword
    'K': _c(20,15,25),
}

_ZOMBIE_GRID = [
    ".....NNNNN....",  # 0
    "....NNNNNNNN..",  # 1
    "....NNSNSNNN..",  # 2
    "....NNNNNNN...",  # 3
    "....NREENNE..",  # 4  R=rot, E=empty eye
    "...DNNNNNNND..",  # 5  tattered clothes
    ".NNNNCCCCCNNN.",  # 6  outstretched arm
    "NNNN.CCCCC.NNN",  # 7
    "NNN..CCCCC..NN",  # 8
    "....DCCCCD....",  # 9
    "....CC..CC....",  # 10
    "....CC..CC....",  # 11
    "...DCC..CCD...",  # 12
    "...CC....CC...",  # 13
    "..KCC....CCK..",  # 14
    "..KK......KK..",  # 15
    "..............",  # 16
    "..............",  # 17
]

_ZOMBIE_PAL = {
    'N': _c(130,150,110),  # dead green flesh
    'D': _c(80,100,65),
    'S': _c(160,175,140),
    'C': _c(90,70,55),     # rotted clothes
    'R': _c(120,40,40),    # blood/rot
    'E': _c(180,220,150),  # glowing eyes
    'K': BLACK,
}

_SPIDER_GRID = [
    "..............",  # 0
    "L.........L...",  # 1  L=leg
    "LL..BBBBB.LL..",  # 2
    ".L.BBBBBBB.L..",  # 3  cephalothorax
    "LLBBBBBBBBBLL.",  # 4
    ".LBBBBBBBBB.L.",  # 5
    "LLBBBBBBBBBLL.",  # 6
    ".L..BBBBBBB.L.",  # 7  abdomen
    "L...BBBBBBB.L.",  # 8
    "L....BBBBB..L.",  # 9
    "L....BBBBB..L.",  # 10
    "L.....BBB...L.",  # 11
    "..............",  # 12
    "..............",  # 13
    "..............",  # 14
    "..............",  # 15
    "..............",  # 16
    "..............",  # 17
]

_SPIDER_PAL = {
    'B': _c(50,20,10),     # dark brown
    'D': _c(30,10,5),
    'L': _c(80,35,15),     # legs
    'E': _c(200,40,40),
}

_TROLL_GRID = [
    "...CCCCCCCCC..",  # 0  huge head
    "..DCCCCCCCCCD.",  # 1
    ".DCSSSSSSSSCD.",  # 2
    ".CSESSSSSSESC.",  # 3
    ".CSSSSSSSSSSC.",  # 4
    "DDCCCCCCCCCCDD",  # 5  massive shoulders
    "CCCCCCCCCCCCCC",  # 6
    "DCCCCCCCCCCCCD",  # 7
    "CCCCCCCCCCCCCC",  # 8
    ".DCCCCCCCCCCD.",  # 9
    ".CC......CCCC.",  # 10
    ".CC......CCCC.",  # 11
    ".DCC......CCD.",  # 12
    "..CC......CC..",  # 13
    "..KCC....CCK..",  # 14
    "..KK......KK..",  # 15
    "..............",  # 16
    "..............",  # 17
]

_DARK_MAGE_GRID = [
    ".....CCCCC....",  # 0
    "....CCCCCCC...",  # 1
    "....CCCCCCC...",  # 2
    ".....SSSSS....",  # 3
    ".....SESES....",  # 4
    "W....DCCCD...W",  # 5
    ".W...CCCCC..W.",  # 6
    "..W..CCCCC.W..",  # 7
    "EW...CCCCC..WE",  # 8  arcane wisps
    ".W..CCCCCCC.W.",  # 9
    "E...CCCCCCC..E",  # 10
    "....DCCCCCD...",  # 11
    "....DCCCCCD...",  # 12
    "....DCDCDCD...",  # 13
    ".....DDDDD....",  # 14
    ".....DDDDD....",  # 15
    "......DDD.....",  # 16
    "..............",  # 17
]

_DARK_MAGE_PAL = {
    'C': _c(90,60,130),
    'D': _c(55,35,80),
    'S': _c(170,155,175),
    'E': _c(150,100,220),
    'W': _c(100,80,120),
}

_VAMPIRE_GRID = [
    ".....KHHHHK...",  # 0  slicked hair
    "....KHHHHHHK..",  # 1
    "....KSSSSSK...",  # 2  pale face
    "....KSESESKK..",  # 3  red eyes
    "....KSSTTSKK..",  # 4  fangs T=white
    "KK..KKCCCK..KK",  # 5  cape wings out
    "KKK.KCCCCK.KKK",  # 6
    "KK..KCCCCCK.KK",  # 7
    "KK..CCCCCCCKK.",  # 8
    ".KK.CCCCCCC.KK",  # 9
    "..KKCCCCCCKK..",  # 10
    "...KKCCCCCKK..",  # 11
    "....KCCCCK....",  # 12
    "....DCCCCD....",  # 13
    "....DCCDCD....",  # 14
    ".....DCDCD....",  # 15
    ".....DDDDD....",  # 16
    "..............",  # 17
]

_VAMPIRE_PAL = {
    'K': BLACK,
    'H': _c(40,20,50),
    'C': _c(120,25,35),  # dark crimson cloak
    'D': _c(75,15,22),
    'S': _c(210,200,215),
    'E': _c(220,40,40),
    'T': WHITE,
}

_DRAGON_GRID = [
    "....WWWWWW....",  # 0  W=wings
    "..WWWWWWWWWW..",  # 1
    ".WWWWCCCCWWWW.",  # 2  body center
    "WWWWCCCCCCCWWW",  # 3
    ".WWCCCCCCCCCW.",  # 4
    "..WCCCCCCCCW..",  # 5
    "..ECCCCCCCCE..",  # 6  E=eye
    "..CCCCCCCCC...",  # 7  head
    "...CCCCCCCC...",  # 8
    "...ECCCCCE....",  # 9
    "....CCCCCC....",  # 10
    "....TTTTTT....",  # 11  T=teeth
    ".....CCCC.....",  # 12  neck
    ".....CCCC.....",  # 13
    "....DCCCD.....",  # 14  body
    "...DDCCCCDD...",  # 15
    "..KK.CCCC.KK..",  # 16  claws
    ".KK...CC...KK.",  # 17
]

_DRAGON_PAL = {
    'C': _c(160,40,30),  # red dragon
    'D': _c(100,25,18),
    'W': _c(130,30,25),  # darker wings
    'E': _c(240,200,30),
    'T': WHITE,
    'K': BLACK,
}

_ABOMINATION_GRID = [
    "..R.CCCCCCC.R.",  # 0  tentacle arms
    ".RRCCCCCCCCRR.",  # 1
    "RRCCCCCCCCCCR.",  # 2
    "RCCCCCCCCCCCR.",  # 3
    "RCCCCCCCCCCCC.",  # 4
    ".CCCCCCCCCCCC.",  # 5
    "RCCCCCCCCCCCC.",  # 6
    "RCEECEECCEECR.",  # 7  many eyes
    "RCCCCCCCCCCCR.",  # 8
    ".RCCCCCCCCCC..",  # 9
    "..RCCCCCCCR...",  # 10  
    "...RCCCCCRR...",  # 11
    "....RCCCR.....",  # 12
    "...RDCCCDR....",  # 13
    "...DCCCCCD....",  # 14
    "...DCCCCCD....",  # 15
    "....DDDDD.....",  # 16
    "..............",  # 17
]

_ABOMINATION_PAL = {
    'C': _c(90,110,70),   # sickly green-grey
    'D': _c(55,68,42),
    'R': _c(120,50,50),   # bloodred tendrils
    'E': _c(255,80,80),   # red eyes
}

_BOSS_VALDRIS_GRID = [
    "G..MMMMMMMM.G.",  # 0  crowned helmet
    "...MMMMMMMMM..",  # 1
    "...MSMMMMSM...",  # 2
    "..MMMMMMMMM...",  # 3
    "DDMMMMMMMMMDD.",  # 4  HUGE pauldrons
    "DMMMMMMMMMMMD.",  # 5
    "DMGGGGGGGGGMD.",  # 6  dark gold
    "DMMMMMMMMMMMD.",  # 7
    "WWMMMMMMMMMWW.",  # 8
    "W..MMMMMMM..W.",  # 9
    "...MMMMMMM....",  # 10
    "...MMMMMMM....",  # 11
    "..DMMMMMMMD...",  # 12
    "..MMMMMMMM....",  # 13
    "..MMMMMMMM....",  # 14
    ".KMMMMMMMMMK..",  # 15
    "..MMMMMMMM....",  # 16
    "..DDDDDDDD....",  # 17
]

_BOSS_VALDRIS_PAL = {
    'M': _c(80,85,100),   # dark steel
    'D': _c(45,48,60),
    'G': _c(170,130,20),  # tarnished gold
    'S': SKIN,
    'W': _c(160,155,170),
    'K': BLACK,
}

# Master enemy registry
_ENEMY_SPRITES = {
    "Goblin Warrior":    (_GOBLIN_WARRIOR_GRID, None),
    "Goblin Archer":     (_GOBLIN_ARCHER_GRID,  None),
    "Goblin Brute":      (_GOBLIN_BRUTE_GRID,   None),
    "Orc Warrior":       (_ORC_WARRIOR_GRID,    _ORC_WARRIOR_PAL),
    "Skeleton Warrior":  (_SKELETON_GRID,       _SKELETON_PAL),
    "Zombie":            (_ZOMBIE_GRID,          _ZOMBIE_PAL),
    "Giant Spider":      (_SPIDER_GRID,          _SPIDER_PAL),
    "Troll":             (_TROLL_GRID,           None),
    "Dark Mage":         (_DARK_MAGE_GRID,       _DARK_MAGE_PAL),
    "Vampire":           (_VAMPIRE_GRID,          _VAMPIRE_PAL),
    "Dragon Wyrmling":   (_DRAGON_GRID,           _DRAGON_PAL),
    "Abomination":       (_ABOMINATION_GRID,      _ABOMINATION_PAL),
    "Boss Valdris":      (_BOSS_VALDRIS_GRID,     _BOSS_VALDRIS_PAL),
}

# Default per-creature colors (used when palette has C/D as None)
_ENEMY_COLORS = {
    "Goblin Warrior":   (_c( 90,120, 60), _c(55, 75,35)),
    "Goblin Archer":    (_c( 90,120, 60), _c(55, 75,35)),
    "Goblin Brute":     (_c( 80,110, 50), _c(50, 68,30)),
    "Troll":            (_c( 60, 95, 50), _c(35, 58,28)),
}


# ═══════════════════════════════════════════════════════════════
#  RENDER ENGINE
# ═══════════════════════════════════════════════════════════════

def _parse_grid(grid, palette):
    """Convert string grid + palette dict → Surface at native pixel size."""
    rows = len(grid)
    cols = max(len(row) for row in grid) if rows else 12
    surf = pygame.Surface((cols, rows), pygame.SRCALPHA)
    surf.fill((0, 0, 0, 0))
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch == '.':
                continue
            color = palette.get(ch)
            if color is None:
                continue
            if len(color) == 3:
                color = (*color, 255)
            surf.set_at((x, y), color)
    return surf


def _build_char_palette(class_name, palette_template, highlight=False):
    """Fill in class-specific C/D entries in a palette template."""
    pal = dict(palette_template)
    base = CLASS_COLORS.get(class_name, (160, 150, 170))
    if highlight:
        base = tuple(min(255, c + 55) for c in base)
    dark = tuple(max(0, int(c * 0.55)) for c in base)
    if pal.get('C') is None:
        pal['C'] = (*base, 255)
    if pal.get('D') is None:
        pal['D'] = (*dark, 255)
    # Ensure all values have alpha
    return {k: ((*v, 255) if v and len(v) == 3 else v) for k, v in pal.items() if v is not None}


def _build_enemy_palette(template_key, palette_template, knowledge_tier, hover=False, dead=False):
    """Build enemy palette respecting knowledge tier."""
    if palette_template is None:
        palette_template = {}

    # Base colors for C/D
    col, dark = _ENEMY_COLORS.get(template_key, (_c(140,130,150), _c(90,82,98)))
    pal = dict(palette_template)
    if pal.get('C') is None:
        pal['C'] = col
    if pal.get('D') is None:
        pal['D'] = dark

    # Ensure alpha on all
    pal = {k: ((*v, 255) if v and len(v) == 3 else v) for k, v in pal.items() if v is not None}

    if dead:
        # Desaturate to grey-purple
        pal = _tier_shift_palette(pal, (60, 55, 70))
        return pal

    tint = TIER_TINTS.get(knowledge_tier, None)
    if tint is not None:
        pal = _tier_shift_palette(pal, tint)

    if hover and knowledge_tier >= 1:
        pal = {k: _hover_brighten(v) for k, v in pal.items()}

    return pal


def _tier_shift_palette(pal, tint_rgb):
    """Replace all colors in palette with tint (silhouette effect)."""
    result = {}
    for k, v in pal.items():
        if v is None: continue
        # Blend toward tint; higher tint = more visible
        result[k] = (*tint_rgb, v[3] if len(v) > 3 else 255)
    return result


def _hover_brighten(c):
    if c is None: return c
    return (min(255, c[0]+35), min(255, c[1]+35), min(255, c[2]+35), c[3] if len(c)>3 else 255)


def _scale_to_rect(surf, target_w, target_h):
    """Scale surf to target dimensions using nearest-neighbor (chunky pixels)."""
    if surf.get_width() == 0 or surf.get_height() == 0:
        return surf
    return pygame.transform.scale(surf, (target_w, target_h))


def _render_sprite(grid, palette, target_w, target_h):
    """Full pipeline: parse → scale → return Surface."""
    native = _parse_grid(grid, palette)
    return _scale_to_rect(native, target_w, target_h)


def _find_enemy_entry(template_key):
    """Find enemy grid/palette, with fallback fuzzy match."""
    if template_key in _ENEMY_SPRITES:
        return _ENEMY_SPRITES[template_key]
    lower = template_key.lower()
    for k, v in _ENEMY_SPRITES.items():
        if k.lower() == lower:
            return v
    for k, v in _ENEMY_SPRITES.items():
        if lower in k.lower() or k.lower() in lower:
            return v
    return (_GOBLIN_WARRIOR_GRID, None)  # fallback


# ═══════════════════════════════════════════════════════════════
#  PUBLIC API  (drop-in for silhouettes.py)
# ═══════════════════════════════════════════════════════════════

def draw_character_silhouette(surface, rect, class_name, equipped_weapon=None,
                               armor_tier=None, highlight=False):
    """Draw an 8-bit pixel art character portrait into rect on surface."""
    grid, pal_template = _CHAR_SPRITES.get(class_name, (_FIGHTER_GRID, _FIGHTER_PAL))
    palette = _build_char_palette(class_name, pal_template, highlight=highlight)
    sprite = _render_sprite(grid, palette, rect.w, rect.h)
    surface.blit(sprite, rect.topleft)


def draw_enemy_silhouette(surface, rect, enemy_template_key, knowledge_tier=0,
                           hover=False, dead=False):
    """Draw an 8-bit pixel art enemy sprite into rect on surface.
    
    Knowledge tier affects appearance:
      -1 : very dark silhouette
       0 : dim silhouette
       1 : partial/muted color
       2 : full color
    """
    grid, pal_template = _find_enemy_entry(enemy_template_key)
    tier = max(-1, min(2, knowledge_tier))
    palette = _build_enemy_palette(enemy_template_key, pal_template, tier, hover=hover, dead=dead)
    sprite = _render_sprite(grid, palette, rect.w, rect.h)
    surface.blit(sprite, rect.topleft)

    # Tier -1: extra dark overlay
    if tier == -1 and not dead:
        overlay = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        overlay.fill((8, 6, 16, 140))
        surface.blit(overlay, rect.topleft)
