"""
Realm of Shadows — 8-bit Pixel Art Sprites  (v2)
Wizardry / Ultima II aesthetic: chunky pixels, 4-tone shading, distinct silhouettes.

Grid: 16w × 28h for characters,  16w × 22h for enemies.
4-tone palette per sprite: H=highlight, C=mid, D=shadow, K=dark outline.
No antialiasing — pygame.transform.scale only (hard pixel edges).

Public API (drop-in for silhouettes.py):
  draw_character_silhouette(surface, rect, class_name, ...)
  draw_enemy_silhouette(surface, rect, enemy_template_key, ...)
  CLASS_COLORS
"""

import pygame

# ═══════════════════════════════════════════════════════════════
#  CLASS COLORS
# ═══════════════════════════════════════════════════════════════
CLASS_COLORS = {
    "Fighter":       (180, 100,  60),
    "Mage":          ( 80, 120, 220),
    "Cleric":        (220, 200, 100),
    "Thief":         (100, 180, 120),
    "Ranger":        ( 80, 160,  80),
    "Monk":          (200, 140,  60),
    "Warder":        (160,  80,  40),
    "Paladin":       (220, 200, 140),
    "Assassin":      ( 60, 160,  80),
    "Warden":        ( 60, 140,  60),
    "Spellblade":    (100, 100, 200),
    "Templar":       (200, 160,  80),
    "Champion":      (220, 120,  60),
    "Crusader":      (240, 220, 140),
    "Shadow Master": ( 40, 140,  80),
    "Beastlord":     ( 80, 160,  80),
    "Archmage":      ( 80, 100, 240),
    "High Priest":   (240, 220, 160),
    "Witch":         (160,  80, 200),
    "Necromancer":   ( 80,  60, 160),
}

TIER_TINTS = {-1: (18,14,28), 0: (55,48,70), 1: (110,98,125), 2: None}

# ═══════════════════════════════════════════════════════════════
#  FIXED PALETTE ENTRIES  (H/C/D/K are dynamic per class/enemy)
# ═══════════════════════════════════════════════════════════════
_FIXED = {
    'S': (230,185,140,255),  # skin light
    's': (175,125, 90,255),  # skin shadow
    'M': (185,188,200,255),  # metal bright
    'm': (110,112,128,255),  # metal shadow
    'G': (218,188, 55,255),  # gold bright
    'g': (148,118, 28,255),  # gold shadow
    'W': (195,165,115,255),  # wood/weapon bright
    'w': (120, 88, 50,255),  # wood dark
    'E': (180,220,255,255),  # arcane glow / eye
    'N': (155,110, 60,255),  # natural/leather
    'n': ( 90, 58, 28,255),  # leather dark
    'R': (210, 45, 45,255),  # red accent
    'B': (230,225,208,255),  # bone light
    'b': (155,148,128,255),  # bone shadow
    'P': (170, 75,215,255),  # purple (witch hat)
    'p': (100, 38,135,255),  # purple dark
    '.': None,
}

# ═══════════════════════════════════════════════════════════════
#  CHARACTER GRIDS  (16 wide × 28 tall, exactly)
# ═══════════════════════════════════════════════════════════════

# FIGHTER: broad plate, greathelm, sword arm raised right
FIGHTER = [
    ".....mmmmmm.....",
    "....mMMMMMMm....",
    "....mMSssSMm....",
    "....mMSSSSMm....",
    "....mMMmmMMm....",
    "..mmmmmmmmmmmm..",
    "..mMHMMMMMMHMm..",
    "W.mMMMGgGMMMm..W",
    "W.mMMMMMMMMm...W",
    "WW.mMMMMMMMm..WW",
    ".W.mMMMMMMMm.W..",
    "...mMMMMMMMMm...",
    "...mMMMMMMMMm...",
    "..mmMMMMMMMMMmm.",
    "..mMMMm..mMMMm..",
    "..mMMm....mMMm..",
    "..mMm......mMm..",
    "..mMm......mMm..",
    "..mMm......mMm..",
    "..mMMm....mMMm..",
    "..KmMm....mMmK..",
    "..KmmK....KmmK..",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]

# MAGE: tall pointed hat, wide flowing robe, staff in each hand
MAGE = [
    "......CCCCC.....",
    ".....DCCCCCD....",
    "....DCCCCCCCD...",
    "...DCCCCCCCCCCD.",
    "....KDDDDDDDDK..",
    ".....SSSSSSS....",
    "....SsESSSEsS...",
    ".W..DCCCCCCCD..W",
    ".W..CCHCCCCCC.W.",
    ".W.DCCCCCCCCCD.W",
    ".W.CCCCCCCCCCEW.",
    ".WW.DCCCCCCCCD..",
    "..W.CCHCCCCCCC..",
    "..W.DCCCCCCCD...",
    "..WW.CCCCCCC....",
    "....DCCCCCCD....",
    "....DCCHDCCD....",
    "....DCCCCCCD....",
    "....KDDDDDDDK...",
    "....nNNNNNNNn...",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]

# CLERIC: robes, hood, glowing cross on chest, mace right hand
CLERIC = [
    ".....CCCCCC.....",
    "....DCCCCCCCD...",
    "....CCHCCCCCC...",
    "....SSSSSSSSS...",
    "...SsESSSSEsSS..",
    "....DCCCCCCCD...",
    ".W..CGgGGGgGCC..",
    ".W..CGgGGGgGCC..",
    ".W..CGgGGGgGCC..",
    ".W..CCCCCCCCCD.W",
    ".W.DCCCCCCCCCD.W",
    ".WW.CCCCCCCCC.WW",
    "..W.CCHCCCCCCC.W",
    "..WW.DCCCCCCD.WW",
    "....DCCCCCCCCD..",
    "....DCCCHCCCD...",
    "....DCCCCCCCCD..",
    "....KDDDDDDDDK..",
    "....nNNNNNNNn...",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]

# THIEF: low hood, crouched forward, two daggers at sides
THIEF = [
    ".....nNNNNn.....",
    "....nNNNNNNn....",
    "....nNNNNNNn....",
    "...nNSSSSSSNn...",
    "...nNSsESsNNn...",
    "..KKnCCCCCCnKK..",
    "W.KKnCCCHCCnKK.W",
    "W.KKnCCCCCCnKKKW",
    "WW.KnCCCCCCnKK.W",
    ".W.KKnCCHCCnKK..",
    "...KKnCCCCCCnKK.",
    "..KKnDCCCCCDnKK.",
    "...nCC......CCn.",
    "..DnCC......CCnD",
    "..nCCC......CCCn",
    "..nCC........CCn",
    "..nCC........CCn",
    "..nCC........CCn",
    "..nKCC......CCKn",
    "..KKnC......CnKK",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]

# RANGER: hooded, longbow drawn wide, quiver on back
RANGER = [
    ".....nNNNNn.....",
    "....nNNNNNNn....",
    "....nSSSSSSNn...",
    "....nSsESsNNn...",
    "....KnCCCCnK....",
    "WW..KnCCHCnK....",
    "W...KnCCCCnK...W",
    "W....CnCCCCnC..WW",
    ".W...KnCCCCnK.WW.",
    "..W..KnCCCCnK.W..",
    "...W.KDCCCDKWWW..",
    "....KKnCCCnKK...",
    "...KnDCCCCDnK...",
    "...nCC.....CCn..",
    "..DnCC.....CCnD.",
    "..nCC.......CCn.",
    "..nCC.......CCn.",
    "..nCC.......CCn.",
    "..NnCC.....CCnN.",
    "..KKnCC....CCnKK",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]

# MONK: wide fighting stance, bare arms extended, ki aura glow
MONK = [
    ".....nNNNNn.....",
    "....nNNNNNNn....",
    "....nSSSSSSn....",
    "....nSsESsNn....",
    "....KnCCCCnK....",
    ".SSSSKnCCCnKSSS.",
    "SSSSKnCCHCCnKSSS",
    "SsSSK.CCCCC.KSSS",
    "SsK...CCCCC...KSs",
    "SK....CCCCC....KS",
    "K.....DCCCD.....K",
    "......CCCCC......",
    "....KnDCCCDnK...",
    "....nCC...CCn...",
    "...DnCC...CCnD..",
    "...nCC.....CCn..",
    "...nCC.....CCn..",
    "...nCC.....CCn..",
    "...nKCC...CCKn..",
    "...KKK.....KKK..",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]

# PALADIN: gleaming full plate + holy golden glow + sword raised
PALADIN = [
    "...GgMMMMMMgG...",
    "...gMMMMMMMg....",
    "...gMSsSSSMg....",
    "..GgMMMMMMMMgG..",
    "..MmMMMMMMMmMM..",
    "..MHMmMGgGMmHM..",
    "..MGgGmGGGmGgGM.",
    "..MHMmMGgGMmHM..",
    "W..mMMMMMMMMm..W",
    "W..mMMMMMMMMMm.W",
    "...mMMMMMMMMMm..",
    "...mMMMMMMMMMm..",
    "..mmMMMMMMMMMmm.",
    "..MMMMMm.mMMMMM.",
    "..MMMMM...MMMMM.",
    "..MMmMM...MMMmMM",
    "..MMmMM...MMMmMM",
    "..KMmMM...MMMmMK",
    "..KmmMK...KMmmKK",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]

# WARDER: darker fighter, red trim, tower shield instead of sword
WARDER = [
    ".....mmmmmm.....",
    "....mMMMMMMm....",
    "....mMSssSMm....",
    "....mMSSSSMm....",
    "....mMMmmMMm....",
    "..mmmmmmmmmmmm..",
    "..mMHMMRRMHMm..",
    ".W.mMMMRRRMMMm.W",
    "WW.mMMMMRMMMMm.W",
    "W..mMMMMMMMMMm.W",
    "...mMMMMMMMMm...",
    "...mMMMMMMMMm...",
    "..mmMMMMMMMMMmm.",
    "..mMMMm..mMMMm..",
    "..mMMm....mMMm..",
    "..mMm......mMm..",
    "..mMm......mMm..",
    "..mMm......mMm..",
    "..mMMm....mMMm..",
    "..KmMm....mMmK..",
    "..KmmK....KmmK..",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]

# ASSASSIN: deep cowl, glowing eyes only visible, twin shadow blades
ASSASSIN = [
    "....KKKKKKKK....",
    "...KKKKKKKKKK...",
    "...KKKKKKKKKKk..",
    "...KKKsEsEKKK...",
    "...KKKKsEKKKK...",
    "..KKKnCCCCCnKKK.",
    "W.KKKnCCCHCnKKKW",
    "W.KKKnCCCCCnKKKW",
    "WW.KKnCCCCCnKK.W",
    ".W.KKKnCCHCnKKKW",
    "..KKKnDCCCCDnKK.",
    "..KKKnCCCCCCnKK.",
    "..KKnCC.....CCnK",
    ".KKnDCC.....CCDnK",
    ".KKnCC.......CCnK",
    ".KKnCC.......CCnK",
    ".KKnCC.......CCnK",
    ".KKKnCC.....CCnKK",
    "..KKKnK.....KnKKK",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]

# WARDEN: ranger + spectacular antler headdress, nature magic
WARDEN = [
    "N...N.NNNN.N...N",
    ".N...NNNNNn...N.",
    ".N...nNNNNn...N.",
    ".....nSSSSSSn...",
    "....nSsESsNSn...",
    "....KnCCCCCnK...",
    "WW..KnCCHCCnK..W",
    "W...KnCCCCCnK..W",
    "W....CnCCCCnC.WW",
    ".W...KnCCCCnK.W.",
    "..W..KnCCCCnK.W.",
    "...W.KDCCCDKWWW.",
    "....KKnCCCnKK...",
    "...KnDCCCCDnK...",
    "...nCC.....CCn..",
    "..DnCC.....CCnD.",
    "..nCC.......CCn.",
    "..nCC.......CCn.",
    "..nCC.......CCn.",
    "..NnCC.....CCnN.",
    "..KKnCC....CCnKK",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]

# SPELLBLADE: mage robes + glowing sword offhand
SPELLBLADE = [
    ".....CCCCC......",
    "....DCCCCCD.....",
    "...DCCCCCCCD....",
    "..DCCCCCCCCCCD..",
    "....KDDDDDDK....",
    ".....SSSSSSS....",
    "....SsESSSEsS...",
    ".W..DCCCCCD...M.",
    ".W..CCHCCCC...M.",
    ".W..CCCCCCC..MM.",
    ".W..DCCCCCD.MM..",
    ".WW.CCCCCCC.M...",
    "..W.CCHCCCCC....",
    "..W.DCCCCCCCD...",
    "..WW.CCCCCCC....",
    "....DCCCCCCD....",
    "....DCCHDCCD....",
    "....DCCCCCCD....",
    "....KDDDDDDK....",
    "....nNNNNNNn....",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]

# TEMPLAR: heavy cleric plate with class-color crusader cross
TEMPLAR = [
    "...GgMMMMMMMgG..",
    "...gMCCCCCCCMg..",
    "...mMSsSSSSsMm..",
    "...mMMMMMMMMMm..",
    "..mmMMMMMMMMMmm.",
    "..MHMmMCCCMmMHM.",
    "..MMmMmCCCMmMMM.",
    "..MHMmMCCCMmMHM.",
    "W..mMMMMMMMMm..W",
    "W..mMMMMMMMMMm.W",
    "...mMMMMMMMMMm..",
    "...mMMMMMMMMMm..",
    "..mmMMMMMMMMMmm.",
    "..MMMMm..mMMMMM.",
    "..MMMMM...MMMMM.",
    "..MMmMM...MMMmMM",
    "..MMmMM...MMMmMM",
    "..KMmMM...MMMmMK",
    "..KmmMK...KMmmKK",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]

# CHAMPION: massive fighter, extra-wide pauldrons, battle aura
CHAMPION = [
    "GG.mMMMMMMMMm.GG",
    "...mMMMMMMMMMm..",
    "...mMSsSSsSSMm..",
    "..mmMMMMMMMMMMm.",
    ".KmmMMMMMMMMMmmK",
    ".KMmMHMMMMMMHMmK",
    ".KMmMGgGGGGgGMmK",
    ".KMmMMMMMMMMMmMK",
    "WW.mMMMMMMMMm.WW",
    "W..mMMMMMMMMMm.W",
    "...mMMMMMMMMMm..",
    "...mMMMMMMMMMm..",
    "..mmMMMMMMMMMmm.",
    "..MMMMMm.mMMMMM.",
    "..MMMMM...MMMMM.",
    "..MMmMM...MMMmMM",
    "..MMmMM...MMMmMM",
    "..KMmMM...MMMmMK",
    "..KmmMK...KMmmKK",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]

# CRUSADER: gilded knight, massive gold cross on tabard
CRUSADER = [
    "..GGgMMMMMMMgGG.",
    "...GgMMMMMMMMgG.",
    "...gMSsSSSSsMg..",
    "...gMMMMMMMMMg..",
    "..GgMMMMMMMMMgG.",
    "..GMHMGgGGgGMHMG",
    "..GMMGgggggGMMG.",
    "..GMHMGgGGgGMHMG",
    "WW.gMMMMMMMMg.WW",
    "W..gMMMMMMMMMg.W",
    "...gMMMMMMMMMg..",
    "...gMMMMMMMMMg..",
    "..GgMMMMMMMMMgG.",
    "..GMMMMg.gMMMMG.",
    "..GMMMM...MMMMG.",
    "..GMMgM...MMgMG.",
    "..GMMgM...MMgMG.",
    "..KGMgM...MMgGK.",
    "..KGgGK...KGgGK.",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]

# SHADOW MASTER: almost entirely black, twin blades, barely-visible form
SHADOW_MASTER = [
    "....KKKKKKKK....",
    "...KKKKKKKKKKk..",
    "...KKKKKKKKKKk..",
    "...KKKsEsKKKK...",
    "...KKKKEKEsKKK..",
    "..KKKnDCCCDnKKK.",
    "W.KKKnCCCHCnKKKW",
    "W.KKKnCCCCCnKKKW",
    "WW.KKnCCCCCnKK.W",
    ".W.KKKnCCHCnKKKW",
    "..KKKnDCCCCDnKK.",
    "..KKKnCCCCCCnKK.",
    "..KKnCC.....CCnK",
    ".KKnDCC.....CCDn",
    ".KKnCC.......CCn",
    ".KKnCC.......CCn",
    ".KKnCC.......CCn",
    ".KKKnCC.....CCnK",
    "..KKKnK.....KnKK",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]

# BEASTLORD: ranger + massive fur mantle + huge antlers
BEASTLORD = [
    "N..N..NNNN..N..N",
    ".N...NNNNNNn..N.",
    ".N...nNNNNNn..N.",
    ".....nSSSSSSn...",
    "....nSsESsNSn...",
    "NNNN.nCCCCCnNNNN",
    "NNNNKnCCHCCnKNNN",
    "NNN.KnCCCCCnK.NN",
    "NN..KnCCCCCnK..N",
    "N...KnCCCCCnK...",
    "....KDCCCCDnK...",
    "....KnCCCCnK....",
    "...KnDCCCCDnK...",
    "...nCC.....CCn..",
    "..DnCC.....CCnD.",
    "..nCC.......CCn.",
    "..nCC.......CCn.",
    "..nCC.......CCn.",
    "..NnCC.....CCnN.",
    "..KKnCC....CCnKK",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]

# ARCHMAGE: ornate mage, twin staves, arcane sparks floating
ARCHMAGE = [
    "E....CCCCC....E.",
    ".E..DCCCCCD..E..",
    "...DCCCCCCCD....",
    "..DCCCCCCCCCCD..",
    "E..KDDDDDDDK..E.",
    ".....SSSSSSS....",
    "....SsESSSEsS...",
    ".W..DCCCCCD...W.",
    ".W..CCHCCCCE..W.",
    ".W.ECCCCCCCE.W..",
    ".WW.DCCCCCD.WW..",
    "..W.CCHCCCCC.W..",
    "..W.DCCCCCD..W..",
    "..WW.CCCCCCC.WW.",
    "E...DCCCCCD...E.",
    "....DCCHDCCD....",
    "E...DCCCCCD...E.",
    "....KDDDDDDDK...",
    "....nNNNNNNNn...",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]

# HIGH PRIEST: elaborate vestments, radiant crown, holy staff
HIGH_PRIEST = [
    ".GG.GCCCCCG.GG..",
    "..GgGCCCCCGgG...",
    "...GgCGGGCgG....",
    "....SSSSSSSSS...",
    "....SsESSSEsS...",
    "GG..DCCCCCCCCD..",
    ".W.GCCHCCCCCG.W.",
    ".W.GCCGCCCCCG.W.",
    ".W.GCCHCCCCCG.W.",
    ".W..CCCCCCCCC.W.",
    ".WW.DCCCCCCD.WW.",
    "..W.CCHCCCCCC.W.",
    "..W.DCCCCCCD..W.",
    "..WW.CCCCCCC.WW.",
    "....DCCCCCCD....",
    "....DCCHDCCD....",
    "....DCCCCCCD....",
    "....KDDDDDDDK...",
    "....nNNNNNNNn...",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]

# WITCH: wide pointed hat, wild robe, broomstick in hand
WITCH = [
    ".....PPPPP......",
    "....DPPPPPPPD...",
    "...DPPPPPPPPPPD.",
    "..DPPPPPPPPPPPPD",
    "..pPpPPPPPPpPpP.",
    ".....SSSSSSS....",
    "....SsESSSEsS...",
    ".W..DCCCCCCCD...",
    ".W..CCHCCCCC....",
    ".WW.CCCCCCCCC...",
    "..W.DCCHCCCCC...",
    "..W.CCCCCCCCC...",
    "..WW.DCCCCCD....",
    "....DCCCCCCCCD..",
    "....DCCHCCCCD...",
    "....DCCCCCCCCD..",
    "....KDDDDDDDDDK.",
    "....nNNNNNNNNn..",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]

# NECROMANCER: dark mage, skulls on robe, bone staff
NECROMANCER = [
    ".....CCCCC......",
    "....DCCCCCD.....",
    "...DCCCCCCCD....",
    "..DCCCCCCCCCCD..",
    "....KDDDDDDDK...",
    ".....sSSSSss....",
    "....sEsKKsEss...",
    ".W..DsCCCCsD..W.",
    ".W..CsHCCCsC..W.",
    ".W.BCsBBBBsBCb.W",
    ".WW.CsCCCCsC.WW.",
    "..W.CsHCCCsC.W..",
    "..W.DsCCCCsD.W..",
    "..WW.sCCCCs.WW..",
    "....DsCCCCsD....",
    "....DsHCCCsD....",
    "....DsCCCCsD....",
    "....KDDDDDDDK...",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]

# ═══════════════════════════════════════════════════════════════
#  ENEMY GRIDS  (16 wide × 22 tall)
# ═══════════════════════════════════════════════════════════════

GOBLIN_WARRIOR = [
    ".......nn.......",
    "..E..nNNNNn..E..",
    "...nnNSSSSNnn...",
    "...nNSsESsNn....",
    "...nNSSSSSSNn...",
    "...KnCCCCCCnK...",
    "W..KnCHCCCCnK..W",
    "W..KnCCCCCCnK..W",
    "WW.KnCCCCCCnK.WW",
    ".W.KnDCCCCDnK.W.",
    "...KnCC..CCnK...",
    "...KnCC..CCnK...",
    "..KKnCC..CCnKK..",
    "..KnCC....CCnK..",
    "..KKnCC..CCnKK..",
    "..KKK......KKK..",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]

GOBLIN_ARCHER = [
    ".......nn.......",
    "..E..nNNNNn..E..",
    "...nnNSSSSNnn...",
    "...nNSsESsNn....",
    "WW.nNSSSSSSNn.W.",
    "W..KnCCCCCCnK..W",
    ".W.KnCHCCCCnK.WW",
    ".WWKnCCCCCCnK.W.",
    "...WKnCCCCCCnKW.",
    "...KnDCCCCDnKW..",
    "...KnCC..CCnK...",
    "...KnCC..CCnK...",
    "..KKnCC..CCnKK..",
    "..KnCC....CCnK..",
    "..KKnCC..CCnKK..",
    "..KKK......KKK..",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]

GOBLIN_BRUTE = [
    "....nnNNNNnn....",
    "..E.nNNNNNNn.E..",
    "...nNNSSSSNNn...",
    "...nNSsESsNNn...",
    "..nNNSSSSSSNNn..",
    "..KnnCCCCCCCnnK.",
    "W.KnCCHCCCCCCnKW",
    "W.KnCCCCCCCCCnKW",
    "WW.nCCCCCCCCCn.W",
    ".W.nCCCCCCCCCn.W",
    "...nDCCCCCCCDn..",
    "...nCC.....CCn..",
    "..KnCC.....CCnK.",
    "..KnCC.....CCnK.",
    "..KKnCC...CCnKK.",
    "..KKK.......KKK.",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]

ORC_WARRIOR = [
    "....XnnNNNnnX...",
    "...XnNNNNNNnX...",
    "...XnNSSSSNnX...",
    "...XnNSESENnX...",
    "...XnNSEEENnX...",
    "...KnMMMMMMnK...",
    "W..KnMHMMMMnK..W",
    "W..KnMMMMMmnK..W",
    "WW.KnMmMMMMnK.WW",
    ".W.KnMMMMMMnK.W.",
    "...KnDMMMMDnK...",
    "...KnMM..MMnK...",
    "..KKnMM..MMnKK..",
    "..KnMM....MMnK..",
    "..KKnMM..MMnKK..",
    "..KKK......KKK..",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]

SKELETON = [
    ".....BBBBBBB....",
    "....BBBBBBBBBb..",
    "....BbBbbBbBbb..",
    "....BbKBBBKbBb..",
    "....BBBbbbBBBb..",
    "....KBBBBBBBBk..",
    "W...KBbBBBBbBK.W",
    "W...KBBBBBBbBK.W",
    "W...KBbBBBBbBK.W",
    ".W..KBBBBBBbBK.W",
    "....KBbBBBBbBK..",
    "....KBBBBBBbBK..",
    "....KBB....BBK..",
    "....KBB....BBK..",
    "..bKBBB....BBBKb",
    "..bBBB......bBBb",
    "..bBB........bBb",
    "..bBB........bBb",
    "..bBbK......KbBb",
    "...bKK......KKb.",
    "................",
    "................",
]

ZOMBIE = [
    ".....NNNNNNNN...",
    "....NNNNNNNNN...",
    "....NNSSSSNNNn..",
    "...NNSsESsNNNn..",
    "..nNNSSSSSSNNn..",
    "..nNNCCCCCNNn...",
    "NNN.nCCHCCCn.NNN",
    "NN...nCCCCCn..NN",
    "N....nCCCCCn...N",
    ".....nDCCCDn....",
    ".....nCC.CCn....",
    ".....nCC.CCn....",
    "....KnCC.CCnK...",
    "....KnCC.CCnK...",
    "...KKnCC.CCnKK..",
    "...KKK.....KKK..",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]

GIANT_SPIDER = [
    "n..n.........n..n",
    "Nn.Nn.......nN.nN",
    ".NnNn.CCCCC.nNnN.",
    "..NNnDCCHCCDnNN..",
    ".NNNnDCCCCCDnNNN.",
    "NNNNnCCCCCCCnNNNN",
    "NNNNnCCHCCCCnNNNN",
    ".NNNnDCCCCCDnNNN.",
    "..NNn.CCCCC.nNN..",
    "...Nn.DCCCD.nN...",
    "....n.CCCCC.n....",
    "....n.CCCCC.n....",
    "....n.DCCCD.n....",
    ".....nDCCCDn.....",
    "......DDDDD......",
    ".................",
    ".................",
    ".................",
    ".................",
    ".................",
    ".................",
    ".................",
]

TROLL = [
    "..CCCCCCCCCCCC..",
    ".DCCCCCCCCCCCCCD",
    ".DCSSSSSSSSSSSCD",
    ".DCSESSSSSSSSSCD",
    ".DCSSSSSSSSSSSCD",
    "DCCCCCCCCCCCCCCD",
    "CHCCCCCCCCCCCCHC",
    "DCCCCCCCCCCCCCCCD",
    "DCCCCCCCCCCCCCCCD",
    ".DCCCCCCCCCCCCD.",
    ".DCC.......CCD..",
    ".DCC.......CCD..",
    ".KCC.......CCK..",
    "..DCC.....CCD...",
    "..KCC.....CCK...",
    "..KDC.....CDK...",
    "..KKC.....CKK...",
    "..KKK.....KKK...",
    "................",
    "................",
    "................",
    "................",
]

DARK_MAGE = [
    ".....CCCCC......",
    "....DCCCCCD.....",
    "...DCCCCCCCD....",
    "..DCCCCCCCCCCD..",
    "....KDDDDDDK....",
    ".....sSSSSSs....",
    "....sEsKKsEss...",
    ".W..DsCCCCsD..W.",
    ".W..CsHCCCsC..W.",
    ".W..CsCCCCsCC.W.",
    ".WW.DsCCCCsD.WW.",
    "..W.CsHCCCsC.W..",
    "..W.DsCCCCsD.W..",
    "..WW.sCCCCs.WW..",
    "....DsCCCCsD....",
    "....DsHCCCsD....",
    "....DsCCCCsD....",
    "....KDDDDDDK....",
    "................",
    "................",
    "................",
    "................",
]

VAMPIRE = [
    "....KKKKKKKKKK..",
    "...KKKKHKKKKKKk.",
    "...KKKsSSSKKKK..",
    "...KKSsRRRSKKKK.",
    "...KKSsREERSKKK.",
    "KK.KKnCCCCCnKK.K",
    "KKK.KnCHCCCnK.KK",
    "KK..KnCCCCCnKK.K",
    "KK..nCCCCCCCn..K",
    ".KK.nCCHCCCCn.KK",
    "..KKnCCCCCCCnKK.",
    "...KKnCCCCCnKK..",
    "....KnDCCCDnK...",
    "....KnCCCCCnK...",
    "....KnDCCCDnK...",
    "....KnCCCCCnK...",
    "....KKnDDDnKK...",
    "......KKKKKK....",
    "................",
    "................",
    "................",
    "................",
]

DRAGON = [
    "....WWWWWWWWW...",
    "..WWWWWWWWWWWWW.",
    ".WWWWWCCCCCCWWWW",
    "WWWWWCCCCCCCWWWW",
    ".WWWCCCCCCCCWWWW",
    "..WWCCCCCCCCCWW.",
    "..ECCCCCCCCCCE..",
    "...DCCCCCCCCCD..",
    "....CCCCCCCCC...",
    "....ECCCCCCCCE..",
    ".....CCCCCCCCC..",
    ".....CCHHHHHHCC.",
    "......BBBBBBBB..",
    "......CCCCCCCCC.",
    ".....DCCCCCCCD..",
    "....DDCCCCCDD...",
    "...KKD.CCCC.DKK.",
    "..KKK...CC...KKK",
    "................",
    "................",
    "................",
    "................",
]

ABOMINATION = [
    ".R.RCCCCCCCCRRR.",
    "RR.RCCCCCCCCCRRR",
    "RRCCCCCCCCCCCCRR",
    "RCCCCCCCCCCCCCCCR",
    "RCCCCCCCCCCCCCCCR",
    ".CCCCCCCCCCCCCC..",
    "RCCCEECEECCEECCCR",
    "RCCCCCCCCCCCCCCCR",
    "RCCCCCCCCCCCCCCR.",
    ".RCCCCCCCCCCCR...",
    "..RCCCCCCCCRR....",
    "...RCCCCCCCRR....",
    "....RCCCCCRR.....",
    "....RDCCCDRR.....",
    "....DCCCCCD......",
    "....DCCCCCD......",
    "....KDDDDDK......",
    ".................",
    ".................",
    ".................",
    ".................",
    ".................",
]

BOSS_VALDRIS = [
    "GG.mMMMMMMMMMm.GG",
    "...mMMMMMMMMMMm..",
    "...mMSsSSsSSsMm..",
    "..mmMMMMMMMMMMm..",
    ".KmmMMMMMMMMMMmmK",
    ".KMmMHMMMMMMMHMmK",
    ".KMmMGgGGGGGgGMmK",
    ".KMmMMMMMMMMMmMmK",
    "WW.mMMMMMMMMMMm.WW",
    "W..mMMMMMMMMMMMm.W",
    "...mMMMMMMMMMMMm..",
    "...mMMMMMMMMMMMm..",
    "..mmMMMMMMMMMMMmm.",
    "..MMMMMMm.mMMMMMM.",
    "..MMMMMM...MMMMM..",
    "..MMMmMM...MMMmMM.",
    "..KMMmMM...MMMmMK.",
    "..KmmMMK...KMmmKKK",
    "..KKmmKK...KKmmKKK",
    ".................",
    ".................",
    ".................",
]

# ═══════════════════════════════════════════════════════════════
#  REGISTRIES
# ═══════════════════════════════════════════════════════════════
_CHAR_GRIDS = {
    "Fighter": FIGHTER, "Mage": MAGE, "Cleric": CLERIC,
    "Thief": THIEF, "Ranger": RANGER, "Monk": MONK,
    "Warder": WARDER, "Paladin": PALADIN, "Assassin": ASSASSIN,
    "Warden": WARDEN, "Spellblade": SPELLBLADE, "Templar": TEMPLAR,
    "Champion": CHAMPION, "Crusader": CRUSADER, "Shadow Master": SHADOW_MASTER,
    "Beastlord": BEASTLORD, "Archmage": ARCHMAGE, "High Priest": HIGH_PRIEST,
    "Witch": WITCH, "Necromancer": NECROMANCER,
}

_ENEMY_GRIDS = {
    "Goblin Warrior":   GOBLIN_WARRIOR,
    "Goblin Archer":    GOBLIN_ARCHER,
    "Goblin Brute":     GOBLIN_BRUTE,
    "Orc Warrior":      ORC_WARRIOR,
    "Skeleton Warrior": SKELETON,
    "Zombie":           ZOMBIE,
    "Giant Spider":     GIANT_SPIDER,
    "Troll":            TROLL,
    "Dark Mage":        DARK_MAGE,
    "Vampire":          VAMPIRE,
    "Dragon Wyrmling":  DRAGON,
    "Abomination":      ABOMINATION,
    "Boss Valdris":     BOSS_VALDRIS,
}

# Per-enemy color overrides (C=mid, D=shadow, H=highlight, K=outline, plus others)
_ENEMY_PALETTE_OVERRIDES = {
    "Orc Warrior":      {'S':(100,140,70,255),'s':(65,95,42,255),'E':(255,240,120,255),
                         'C':(85,112,58,255),'D':(52,70,34,255),'H':(118,150,82,255),'K':(30,40,18,255)},
    "Skeleton Warrior": {'C':(225,220,200,255),'D':(160,153,130,255),'H':(245,240,225,255),'K':(100,92,75,255),
                         'B':(235,230,210,255),'b':(160,153,130,255)},
    "Zombie":           {'C':(100,125,80,255),'D':(65,82,50,255),'H':(130,155,105,255),'K':(40,50,28,255),
                         'N':(115,140,90,255),'n':(60,75,40,255),'E':(140,230,130,255)},
    "Giant Spider":     {'C':(55,25,10,255),'D':(32,12,4,255),'H':(90,45,20,255),'K':(20,8,2,255),
                         'N':(75,35,14,255),'n':(45,18,6,255)},
    "Dark Mage":        {'C':(95,65,140,255),'D':(58,38,90,255),'H':(130,100,185,255),'K':(30,18,55,255),
                         's':(195,185,210,255),'S':(220,215,230,255)},
    "Vampire":          {'C':(125,20,35,255),'D':(78,12,22,255),'H':(160,40,55,255),'K':(8,5,12,255),
                         'R':(200,35,35,255),'E':(210,60,60,255)},
    "Dragon Wyrmling":  {'C':(165,38,28,255),'D':(105,22,15,255),'H':(210,65,48,255),'K':(55,12,8,255),
                         'W':(140,30,22,255),'E':(245,205,30,255),'B':(240,235,215,255)},
    "Abomination":      {'C':(90,115,72,255),'D':(55,72,42,255),'H':(125,150,100,255),'K':(28,36,18,255),
                         'R':(140,48,48,255),'E':(245,80,80,255)},
    "Boss Valdris":     {'M':(75,82,100,255),'m':(45,50,65,255),'G':(175,135,20,255),'g':(110,82,12,255),
                         'C':(88,95,115,255),'D':(52,58,75,255),'H':(120,128,150,255),'K':(28,32,45,255)},
}

_ENEMY_BASE_COLORS = {
    "Goblin Warrior":   (92,118,62,255),
    "Goblin Archer":    (92,118,62,255),
    "Goblin Brute":     (82,108,52,255),
    "Troll":            (62,98,52,255),
}

# ═══════════════════════════════════════════════════════════════
#  PALETTE BUILDERS
# ═══════════════════════════════════════════════════════════════

def _make_tones(base_rgb):
    r,g,b = base_rgb[0],base_rgb[1],base_rgb[2]
    def shade(f): return (max(0,min(255,int(r*f))),max(0,min(255,int(g*f))),max(0,min(255,int(b*f))),255)
    H = shade(1.38); C = (*base_rgb[:3],255); D = shade(0.56); K = shade(0.28)
    return H,C,D,K

def _build_char_palette(class_name):
    base = CLASS_COLORS.get(class_name,(160,150,170))
    H,C,D,K = _make_tones(base)
    pal = dict(_FIXED); pal['H']=H; pal['C']=C; pal['D']=D; pal['K']=K
    return pal

def _build_enemy_palette(template_key, knowledge_tier, hover=False, dead=False):
    base = _ENEMY_BASE_COLORS.get(template_key,(130,120,145))
    H,C,D,K = _make_tones(base)
    pal = dict(_FIXED); pal['H']=H; pal['C']=C; pal['D']=D; pal['K']=K
    overrides = _ENEMY_PALETTE_OVERRIDES.get(template_key,{})
    pal.update(overrides)

    if dead:
        out={}
        for k,v in pal.items():
            if v is None: out[k]=None; continue
            r,g,b,a = v[0],v[1],v[2],v[3] if len(v)>3 else 255
            grey=int(r*0.22+g*0.22+b*0.22); out[k]=(grey+15,grey+12,grey+22,a)
        return out

    tint = TIER_TINTS.get(knowledge_tier,None)
    if tint is not None:
        out={}
        for k,v in pal.items():
            if v is None: out[k]=None; continue
            tr,tg,tb=tint; a=v[3] if len(v)>3 else 255
            lum=int(v[0]*0.3+v[1]*0.59+v[2]*0.11)
            delta=(lum-128)//5
            out[k]=(max(0,min(255,tr+delta)),max(0,min(255,tg+delta)),max(0,min(255,tb+delta)),a)
        if hover:
            out={k:(min(255,v[0]+30),min(255,v[1]+30),min(255,v[2]+30),v[3]) if v else None for k,v in out.items()}
        return out

    if hover:
        pal={k:(min(255,v[0]+30),min(255,v[1]+30),min(255,v[2]+30),v[3]) if v else None for k,v in pal.items()}
    return pal

# ═══════════════════════════════════════════════════════════════
#  RENDERER
# ═══════════════════════════════════════════════════════════════

def _render(grid, pal, w, h):
    rows=len(grid); cols=max((len(r) for r in grid),default=16)
    native=pygame.Surface((cols,rows),pygame.SRCALPHA); native.fill((0,0,0,0))
    for y,row in enumerate(grid):
        for x,ch in enumerate(row):
            c=pal.get(ch)
            if c is None: continue
            native.set_at((x,y),c[:4] if len(c)>=4 else (*c,255))
    return pygame.transform.scale(native,(w,h))

def _find_enemy_grid(key):
    if key in _ENEMY_GRIDS: return _ENEMY_GRIDS[key]
    lo=key.lower()
    for k,g in _ENEMY_GRIDS.items():
        if k.lower()==lo: return g
    for k,g in _ENEMY_GRIDS.items():
        if lo in k.lower() or k.lower() in lo: return g
    return GOBLIN_WARRIOR

# ═══════════════════════════════════════════════════════════════
#  PUBLIC API
# ═══════════════════════════════════════════════════════════════

def draw_character_silhouette(surface, rect, class_name,
                               equipped_weapon=None, armor_tier=None, highlight=False):
    grid = _CHAR_GRIDS.get(class_name, FIGHTER)
    pal  = _build_char_palette(class_name)
    if highlight:
        pal = {k:(min(255,v[0]+45),min(255,v[1]+45),min(255,v[2]+45),v[3]) if v else None
               for k,v in pal.items()}
    sprite = _render(grid, pal, rect.w, rect.h)
    surface.blit(sprite, rect.topleft)

def draw_enemy_silhouette(surface, rect, enemy_template_key,
                           knowledge_tier=0, hover=False, dead=False):
    grid = _find_enemy_grid(enemy_template_key)
    tier = max(-1, min(2, knowledge_tier))
    pal  = _build_enemy_palette(enemy_template_key, tier, hover=hover, dead=dead)
    sprite = _render(grid, pal, rect.w, rect.h)
    surface.blit(sprite, rect.topleft)
    if tier == -1 and not dead:
        ov = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        ov.fill((6,4,14,155))
        surface.blit(ov, rect.topleft)
