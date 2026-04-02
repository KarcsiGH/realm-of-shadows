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


# ── WOLF: low quadruped body, head forward-left, tail up ──
WOLF = [
    "................",
    ".....nn.........",
    "....NNNNn.......",
    "...NNSSsSNn.....",
    "...NSsESSNn.....",
    "..KNNSSSSNNk....",
    "..KNNCCCCCNNk...",
    ".KKNCCHCCCCNKk..",
    ".KKNCCCCCCCNKk..",
    "..KNNDCCCDNNk...",
    "....Nn...nNK....",
    "....N.....Nn....",
    "...KNK...KNNk...",
    "....K.....Kn....",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]


# ── HOUND: stocky dog, lower-slung than wolf, floppy ears ──
HOUND = [
    "................",
    "....ww..........",
    "...wWWWw........",
    "..wWNNNWw.......",
    "..wWNsENWw......",
    "..KwWNNNWwK.....",
    "..KwWCCCWwKk....",
    ".KKwWCHCCWwKk...",
    ".KKwWCCCCWwKk...",
    "..KwWDCCDWwK....",
    "...wWNw.wWN.....",
    "...wW...wWNw....",
    "..KwWK.KwWNwk...",
    "...wK...KwNw....",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]


# ── BANDIT: hooded rogue, no pointy ears, short cloak ──
BANDIT = [
    ".....nNNNNn.....",
    "....nNNNNNNn....",
    "....nNSSSSNNn...",
    "...nNSsESsNNn...",
    "....nNSSSSNn....",
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

# ── GOBLIN_SHAMAN: goblin body, tall spirit-orb staff, glowing eyes ──
GOBLIN_SHAMAN = [
    ".......nn.......",
    "...E.nNNNNn.E...",
    "...nnNSSSSNnn...",
    "...nNSsEEsNn....",
    "...nNSSSSSSNn...",
    ".W.KnCCCCCCnK.W.",
    "WW.KnCHCCCCnK.W.",
    "W..KnCCCCCCnK.WW",
    "...KnCCCCCCnK..W",
    "...KnDCCCCDnK...",
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

# ── STONE_SENTINEL: blocky golem, no neck, heavy limbs ──
STONE_SENTINEL = [
    "....MMMMMMMM....",
    "...MMMMMMMMMMm..",
    "...MMmSSSSmmMm..",
    "...MMmSKKSmmMm..",
    "...MMmSSSSmmMm..",
    "..mMMMMMMMMMMMm.",
    ".KmMHMMMMMMMMmK.",
    "WKmMMMMMMMMMMmKW",
    "WKmMMMMMMMMMMmKW",
    "WKmMMmMMMMmMMmKW",
    ".KmMMMMMMMMMmK..",
    "..mMMMm..mMMMm..",
    "..mMMMm..mMMMm..",
    "..mMMMm..mMMMm..",
    "..KmMmK..KmMmK..",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]

# ── ASH_REVENANT: spectral undead, wispy/burning form ──
ASH_REVENANT = [
    "...R.RRRRRR.R...",
    "...RRRsSSsRRR...",
    "...RRSSSSSSRRn..",
    "...RSsESSEsRRn..",
    "...RRSSSSSSRnn..",
    "...RRCCCCCRRR...",
    "..RRRRCCCRRRn...",
    "..RRRRCHCRRRn...",
    "..RRRRCCCRRRRn..",
    "..RRRRDCDRRRRn..",
    "...RRnCC.CCRRn..",
    "....RnCC.CCnR...",
    "....RnCC.CCnR...",
    "....RRnCCCnRR...",
    ".....RRnRnRR....",
    "......RRRRRR....",
    "......RRRRR.....",
    "................",
    "................",
    "................",
    "................",
    "................",
]

# ── WRAITH: pure ghostly form, barely-there body, glowing eyes ──
WRAITH = [
    "....KKKKKKKK....",
    "...KKKKKKKKKKk..",
    "...KKKsSSSKKKK..",
    "...KKSsEEESKKKK.",
    "...KKKsSSSKKKK..",
    "..KKKnCCCCCnKKK.",
    "W.KKKnCCHCCnKKKW",
    "W.KKKnCCCCCnKKKW",
    "..KKKnCCCCCnKKK.",
    "...KKKnCHCnKKK..",
    "..KKKnDCCCDnKKK.",
    "...KKKnCCCnKKK..",
    "....KKnCCCnKK...",
    ".....KnCCCnK....",
    "......KnCnK.....",
    ".......KCK......",
    "......KKKKK.....",
    "................",
    "................",
    "................",
    "................",
    "................",
]

# ── KOBOLD: small lizard-humanoid, shorter than goblin ──
KOBOLD = [
    "................",
    "......nNNn......",
    ".....NNSSNN.....",
    ".....NSsENNn....",
    ".....NSSSSNN....",
    "..W.KnCCCCnK.W..",
    ".W..KnCHCCnK..W.",
    "..W.KnCCCCnK.W..",
    "....KnCCCCnK....",
    "....KnDCCDnK....",
    "....KnCC.CnK....",
    "....KnCC.CnK....",
    "...KKnCC.CnKK...",
    "...KnCC...CCnK..",
    "...KKnCC.CnKK...",
    "...KKK.....KKK..",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]

# ── GHOUL: hunched undead, one arm dragging, sunken eyes ──
GHOUL = [
    ".....NNNNNN.....",
    "....NNNNNNNNn...",
    "....NNSSSSNNn...",
    "...NNSsEEsNNnn..",
    "....NNSSSSNNn...",
    "...KNNCCCCCNNk..",
    "W..KNNCHCCCNNk.W",
    "W..KNNCCCCCNNk.W",
    "WW.KNNCCCCCNNk..",
    ".W.KNNDCCCDNNk..",
    "...KNNCCCCCNNk..",
    "...KNNDCCCDNNk..",
    "..NNNnCC.CCNNn..",
    "..NNNnCC.CCNNn..",
    ".NNNKnCC.CCnKNN.",
    "..NNK.....KNNn..",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]

# ── DEATH_KNIGHT: skeleton in heavy plate, glowing sword ──
DEATH_KNIGHT = [
    "...BbMMMMMMbB...",
    "...bMMMMMMMmb...",
    "...bMSbbbSMmb...",
    "...bMbKKKbMMb...",
    "...bMMMMMMMmb...",
    "..bbMMMMMMMMMbb.",
    "..MHMmMGgGMmMHM.",
    "WW.mMMMMMMMMm.WW",
    "W..mMMMMMMMMMm.W",
    "...mMMMMMMMMMm..",
    "...mMMMMMMMMMm..",
    "..bbMMMMMMMMMbb.",
    "..MMMMMb.bMMMMM.",
    "..MMMMM...MMMMM.",
    "..MbMMM...MMbMM.",
    "..KbMMK...KMbMK.",
    "..KbbMK...KMbbK.",
    "................",
    "................",
    "................",
    "................",
    "................",
]

# ── ORC_CHIEFTAIN: bigger orc, crown/helmet, axe raised ──
ORC_CHIEFTAIN = [
    "GG.GnnNNNNnnG.GG",
    "...XnNNNNNNnX...",
    "...XnNSSSSNnX...",
    "...XnNSESENnX...",
    "...XnNSEEENnX...",
    "..mmMMMMMMMMMmm.",
    ".KmMHMMMMMMMMmK.",
    "WW.mMGgGGgGMm.WW",
    "W..mMMMMMMMMm..W",
    "...mMGgGGgGMm...",
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
]

# ── GOBLIN_KING: massive goblin, crown, two weapons ──
GOBLIN_KING = [
    "GG.nNNNNNNnN.GG.",
    "..EnnNNNNNNnE...",
    "...nnNSSSSNnn...",
    "...nNSsEEsNNn...",
    "...nNSSSSSSNn...",
    "..mmCCCCCCCCmm..",
    ".KmCCHCCCCCCCmK.",
    "WW.mCCCCCCCCm.WW",
    "W..mCGgGGgGCm..W",
    "...mCCCCCCCCm...",
    "...mCCCCCCCCm...",
    "...mCCCCCCCCm...",
    "..mmCCCCCCCCmm..",
    "..mCCCm..mCCCm..",
    "..mCCm....mCCm..",
    "..KmCm....mCmK..",
    "..KmmK....KmmK..",
    "................",
    "................",
    "................",
    "................",
    "................",
]

# ── CAVE_BAT: wings sweep from outer corners inward to a tiny body.
#    Silhouette reads immediately as a bat — mostly wing, barely body.
#    N/n = dark wing membrane (palette overrides to deep purple)
#    E = red glowing eyes (palette override), C/H/D = tiny body
CAVE_BAT = [
    "N..............N",   # wing tips at outer top corners
    ".N............N.",   # wings angle inward
    "..N..........N..",   # wings continue
    "..NN........NN..",   # wings thicken
    "..NNNn....nNNN..",   # ears appear (n = darker)
    "..NNNNnNNnNNNN..",   # head between ear peaks
    "...NNNNENNNNn...",   # single glowing eye (E = red for bat)
    "...NNNCHCnNNN...",   # tiny body
    "....NNnDnNN.....",   # lower body / belly
    ".....NnnnN......",   # feet/claws
    "......NNN.......",   # claws
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
    "................",
]

# ═══════════════════════════════════════════════════════════════
#  DUNGEON OBJECT GRIDS
#  16 wide, variable height. Use only _FIXED palette chars.
#  S s M m G g W w E N n R B b P p .
# ═══════════════════════════════════════════════════════════════

# TREASURE CHEST: arched lid, wood body, gold lock, metal bands
DUNGEON_CHEST = [
    "................",
    "................",
    "..mmmmmmmmmmmm..",   # lid outline top
    ".mBBBBBBBBBBBBm.",   # lid highlight face
    ".mBBBBBBBBBBBBm.",   # lid face
    ".mMMMMMMMMMMMMMm",   # lid bottom / metal trim
    "..mmmmmmmmmmmmm.",   # metal band (lid-body divider)
    "..mWWWWWWWWWWWm.",   # body top
    "..mWWWWGgGWWWWm.",   # lock row
    "..mWWWGgGgGWWWm.",   # lock center
    "..mWWWWGgGWWWWm.",   # lock row bottom
    "..mWWWWWWWWWWWm.",   # body lower
    "..mwwwwwwwwwwwm.",   # base dark band
    "...mmmmmmmmmmm..",   # base trim
    "................",
    "................",
]

# STAIRS DOWN: wide nearest step at top, each narrows descending
# Stone palette: B=lit face, b=shadow, m=deep edge
DUNGEON_STAIRS_DOWN = [
    "................",
    "mmmmmmmmmmmmmmmm",   # near step edge (widest)
    "BBBBBBBBBBBBBBBB",   # near step face
    "bbbbbbbbbbbbbbbb",   # near step underside
    ".mmmmmmmmmmmmm..",   # step 2 edge
    ".BBBBBBBBBBBBB..",   # step 2 face
    ".bbbbbbbbbbbbb..",   # step 2 underside
    "..mmmmmmmmmm....",   # step 3 edge
    "..BBBBBBBBBB....",   # step 3 face
    "..bbbbbbbbbb....",   # step 3 underside
    "...mmmmmmmmm....",   # step 4 edge
    "...BBBBBBBBB....",   # step 4 face
    "...bbbbbbbbb....",   # step 4 underside
    "....mmmmmm......",   # step 5 (deepest)
    "....BBBBBB......",   # step 5 face
    "................",
]

# STAIRS UP: narrow top, widens toward viewer at bottom
DUNGEON_STAIRS_UP = [
    "................",
    "....mmmmmm......",   # step 5 top (furthest, narrowest)
    "....BBBBBB......",   # step 5 face
    "....bbbbbb......",   # step 5 underside
    "...mmmmmmmmm....",   # step 4
    "...BBBBBBBBB....",
    "...bbbbbbbbb....",
    "..mmmmmmmmmm....",   # step 3
    "..BBBBBBBBBB....",
    "..bbbbbbbbbb....",
    ".mmmmmmmmmmmmm..",   # step 2
    ".BBBBBBBBBBBBB..",
    ".bbbbbbbbbbbbb..",
    "mmmmmmmmmmmmmmmm",   # step 1 (nearest, widest)
    "BBBBBBBBBBBBBBBB",
    "bbbbbbbbbbbbbbbb",
]

# SHRINE ACTIVE: stone pedestal with glowing arcane basin
# E=arcane glow, B=stone face, b=stone shadow, M=pillar bright, m=pillar shadow
DUNGEON_SHRINE_ACTIVE = [
    "................",
    "......EEEEEE....",   # glow halo top
    ".....EEEEEEEEb..",   # glow wide
    "....EEbbbbbbEEb.",   # basin rim glow
    "....EbBBBBBBbEb.",   # basin rim stone face
    "....EbBEEEEBbEb.",   # basin interior (glowing water)
    "....EbBEEEEBbEb.",   # basin interior
    "....EbBBBBBBbEb.",   # basin lower rim
    "....EEbbbbbbEE..",   # basin base glow
    ".....MMMMMMMM...",   # pedestal cap
    "......mMMMMm....",   # shaft top
    "......mMMMMm....",   # shaft
    "......mMMMMm....",   # shaft
    ".....mmMMMMmm...",   # base flare
    "....mmMMMMMMMm..",   # base wide
    "...mMMMMMMMMMMm.",   # base widest
    "..mmmmmmmmmmmmm.",   # base trim
    "................",
    "................",
    "................",
]

# SHRINE USED: same shape, no glow, dry and cracked
DUNGEON_SHRINE_USED = [
    "................",
    "................",
    "................",
    "....bbbbbbbbbb..",   # dry basin rim
    "....bBBBBBBBbb..",   # basin face
    "....bBbbbbbbBb..",   # dry dark interior
    "....bBbbbbbbBb..",   # dry dark interior
    "....bBBBBBBBbb..",   # basin lower
    "....bbbbbbbbbb..",   # basin base dry
    ".....MMMMMMMM...",   # pedestal cap
    "......mMMMMm....",   # shaft
    "......mMMMMm....",   # shaft
    "......mMbMbm....",   # cracked shaft
    ".....mmMMMMmm...",   # base flare
    "....mmMMMMMMMm..",   # base wide
    "...mMMMMMMMMMMm.",   # base widest
    "..mmmmmmmmmmmmm.",   # base trim
    "................",
    "................",
    "................",
]


# FOUNTAIN ACTIVE: stone basin with arcing water jets
# W=water arc, w=water drops, B=basin stone, b=basin shadow, M=base stone
DUNGEON_FOUNTAIN_ACTIVE = [
    "................",
    "....W......W....",   # water arc peaks
    "...WWW....WWW...",   # arcs
    "..WWWWW..WWWWW..",   # arcs wide
    "...WWW....WWW...",   # arcs falling
    "....w..bb..w....",   # drops + basin rim
    "...wbBBBBBBbw...",   # basin rim stone
    "....bBBBBBBBb...",   # basin outer
    "....bBwwwwwBb...",   # water surface
    "....bBwwwwwBb...",   # water surface
    "....bBBBBBBBb...",   # basin lower rim
    ".....bbbbbbb....",   # basin base
    "......MMMMM.....",   # pedestal top
    "......MMMMM.....",   # pedestal
    ".....MMMMMMM....",   # pedestal base
    "....mmmmmmmmm...",   # ground trim
    "................",
    "................",
    "................",
    "................",
]

# FOUNTAIN USED: empty dry basin, no water
DUNGEON_FOUNTAIN_USED = [
    "................",
    "................",
    "................",
    "................",
    "................",
    ".....bbbbbb.....",   # dry basin rim
    "....bBBBBBBb....",   # basin rim
    "....bBBBBBBBb...",   # basin outer
    "....bBbbbbbbBb..",   # dry dark interior
    "....bBbbbbbbBb..",   # dry interior
    "....bBBBBBBBb...",   # basin lower
    ".....bbbbbbb....",   # basin base
    "......MMMMM.....",   # pedestal top
    "......MMMMM.....",   # pedestal
    ".....MMMMMMM....",   # pedestal base
    "....mmmmmmmmm...",   # ground trim
    "................",
    "................",
    "................",
    "................",
]


# ── BEETLE: hard rounded carapace, antennae, segmented abdomen, leg stubs.
#    Reads as insect/arthropod — oval dome, NOT humanoid.
#    N/n = chitin/legs, C/H/D = carapace body
BEETLE = [
    "................",
    ".....n....n.....",   # antennae tips
    "......n..n......",   # antennae stalks
    "...nCCCCCCCCn...",   # carapace top
    "..nCCHCCCCCCCn..",   # carapace highlight
    "..nCCCCCCCCCCn..",   # carapace widest
    "n.nCCCCCCCCCCn.n",   # front legs
    "n.nCDCCCCCDCn..n",   # wing-case seam
    "n.nCCCCCCCCCn..n",   # mid legs
    ".nnCCCCCCCCCnn..",   # rear legs
    "..nDCCCCCCCDn...",   # abdomen
    "...nDDDDDDDn....",   # abdomen tip
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

# ── GIANT_RAT: wide oval body, huge round ears, pointed snout.
#    Silhouette is low and wide — completely unlike any humanoid.
#    N/n = fur, S/s = face fur, E = beady eye
GIANT_RAT = [
    "................",
    "..nN.......Nn...",   # big round ears
    "..NNNNNNNNNNNn..",   # wide head
    "..NNNsENNNNNNn..",   # eye + face
    "..NNNNsNNNNNNn..",   # snout/muzzle
    "..NNNCnCNNNNNn..",   # chin
    ".nNNCCCCCCNNNn..",   # body top
    ".nNNCCHCCCNNNn..",   # body highlight
    ".nNNCCCCCCNNNn..",   # body
    ".nNNDCCCCDNNNn..",   # body lower
    "..nNNDCCDNNnn...",   # haunches
    "...nNnDDnNn.....",   # back feet
    "....nnn.........",   # tail base
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

# ── HATCHLING: small dragon/lizard — crest, long neck, four limbs.
#    Clearly a creature, not a humanoid. Crest frill + scale accents.
#    R = scale/fire accent, N/n = scales, C/H/D = body mass
HATCHLING = [
    "................",
    ".....RNRRRNR....",   # head crest/frill
    "....NNNNNNNNn...",   # head top
    "....NNsENNNNn...",   # eye
    "....NNNNNNNnn...",   # snout/jaw
    "...RNNCCCNNRn...",   # neck
    "..RNNCCCCCNNRn..",   # chest
    ".RNNCCHCCCCNNRn.",   # chest highlight
    ".RNNCCCCCCCNNRn.",   # body
    "RNNNDCCCCCDNNNn.",   # body + limb attachment
    ".NN..nCCCn..NN..",   # legs
    "..N..nDCDn..Nn..",   # lower body
    "..n..nDDn...n...",   # feet/claws
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

_DUNGEON_OBJECT_GRIDS = {
    "chest":         DUNGEON_CHEST,
    "stairs_down":   DUNGEON_STAIRS_DOWN,
    "stairs_up":     DUNGEON_STAIRS_UP,
    "shrine_active":   DUNGEON_SHRINE_ACTIVE,
    "shrine_used":     DUNGEON_SHRINE_USED,
    "fountain_active": DUNGEON_FOUNTAIN_ACTIVE,
    "fountain_used":   DUNGEON_FOUNTAIN_USED,
}


def draw_dungeon_object(surface, rect, obj_type, theme=None):
    """
    Render a dungeon object using procedural drawing.
    obj_type: 'chest' | 'stairs_down' | 'stairs_up' | 'shrine_active' | 'shrine_used'
              'fountain_active' | 'fountain_used' | 'trap_armed' | 'trap_tripped'
    """
    from ui.dungeon_objects import (
        draw_stairs_up, draw_stairs_down,
        draw_shrine_active, draw_shrine_used,
        draw_fountain_active, draw_fountain_used,
        draw_trap_armed, draw_trap_tripped,
        draw_chest,
    )
    _dispatch = {
        "stairs_up":       draw_stairs_up,
        "stairs_down":     draw_stairs_down,
        "shrine_active":   draw_shrine_active,
        "shrine_used":     draw_shrine_used,
        "fountain_active": draw_fountain_active,
        "fountain_used":   draw_fountain_used,
        "trap_armed":      draw_trap_armed,
        "trap_tripped":    draw_trap_tripped,
        "chest":           draw_chest,
    }
    fn = _dispatch.get(obj_type)
    if fn:
        fn(surface, rect, theme)
    else:
        # Legacy fallback for any unrecognised type
        grid = _DUNGEON_OBJECT_GRIDS.get(obj_type, DUNGEON_CHEST)
        pal  = dict(_FIXED)
        sprite = _render(grid, pal, rect.w, rect.h)
        surface.blit(sprite, rect.topleft)


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
    # ── Original enemies ──
    "Goblin Warrior":       GOBLIN_WARRIOR,
    "Goblin Archer":        GOBLIN_ARCHER,
    "Goblin Brute":         GOBLIN_BRUTE,
    "Orc Warrior":          ORC_WARRIOR,
    "Skeleton Warrior":     SKELETON,
    "Zombie":               ZOMBIE,
    "Giant Spider":         GIANT_SPIDER,
    "Troll":                TROLL,
    "Dark Mage":            DARK_MAGE,
    "Vampire":              VAMPIRE,
    "Dragon Wyrmling":      DRAGON,
    "Abomination":          ABOMINATION,
    "Boss Valdris":         BOSS_VALDRIS,
    # ── New enemies ──
    "Wolf":                 WOLF,
    "Dire Wolf":            WOLF,
    "Hound":                HOUND,
    "War Hound":            HOUND,
    "Guard Hound":          HOUND,
    "Hunting Hound":        HOUND,
    "Rabid Hound":          HOUND,
    "Corrupted Hound":      HOUND,
    "Bandit":               BANDIT,
    "Highway Bandit":       BANDIT,
    "Ashenmoor Bandit":     BANDIT,
    "Bandit Crossbowman":   BANDIT,
    "Ashenmoor Crossbowman":BANDIT,
    "Ruin Archer":          BANDIT,
    "Goblin Shaman":        GOBLIN_SHAMAN,
    "Goblin Scout":         GOBLIN_SHAMAN,
    "Goblin Drummer":       GOBLIN_SHAMAN,
    "Goblin Trapper":       GOBLIN_SHAMAN,
    "Stone Sentinel":       STONE_SENTINEL,
    "Stone Guardian":       STONE_SENTINEL,
    "Animated Armor":       STONE_SENTINEL,
    "Mine Golem":           STONE_SENTINEL,
    "Golem":                STONE_SENTINEL,
    "Coral Golem":          STONE_SENTINEL,
    "Storm Golem":          STONE_SENTINEL,
    "Flesh Golem":          STONE_SENTINEL,
    "Ash Revenant":         ASH_REVENANT,
    "Fading Wraith":        WRAITH,
    "Crypt Shade":          WRAITH,
    "Dust Wraith":          WRAITH,
    "Wailing Spirit":       WRAITH,
    "Isle Shade":           WRAITH,
    "Saltwater Shade":      WRAITH,
    "Throne Shade":         WRAITH,
    "Tide Wraith":          WRAITH,
    "Wind Wraith":          WRAITH,
    "Lingering Will":       WRAITH,
    "Shadow Stalker":       WRAITH,
    "Shadow Brute":         WRAITH,
    "Fading Wraith":        WRAITH,
    "Reality Fracture":     WRAITH,
    "Kobold Firebrand":     KOBOLD,
    "Kobold Miner":         KOBOLD,
    "Kobold Trapsmith":     KOBOLD,
    "Kobold":               KOBOLD,
    "Ghoul":                GHOUL,
    "Plague Bearer":        GHOUL,
    "Drowned Revenant":     GHOUL,
    "Warden Revenant":      GHOUL,
    "Death Knight":         DEATH_KNIGHT,
    "Corrupted Scholar":    DEATH_KNIGHT,
    "Ruin Sentinel":        DEATH_KNIGHT,
    "Orc Chieftain":        ORC_CHIEFTAIN,
    "Orc Fighter":          ORC_WARRIOR,
    "Goblin King":          GOBLIN_KING,
    "Grak the Goblin King": GOBLIN_KING,
    "Goblin War Boss":      GOBLIN_KING,
    "Cave Bat":             CAVE_BAT,
    "Lava Bat":             CAVE_BAT,
    "Cave-in Beetle":       BEETLE,
    "Lava Beetle":          BEETLE,
    "Tunnel Beetle":        BEETLE,
    "Corrupted Hatchling":  HATCHLING,
    "Dragon Hatchling":     HATCHLING,
    "Fire Lizard":          HATCHLING,
    "Cinder Drake":         HATCHLING,
    "Cave Drake":           HATCHLING,
    "Giant Rat":            GIANT_RAT,
    "Dungeon Rat":          GIANT_RAT,
    "Sewer Rat":            GIANT_RAT,
    "Giant Spider Queen":   GIANT_SPIDER,
    "Spider Queen":         GIANT_SPIDER,
    "Broodmother Guard":    GIANT_SPIDER,
    "Spiderling":           GIANT_SPIDER,
    "Web Spinner":          GIANT_SPIDER,
    "Phase Spider":         GIANT_SPIDER,
    "Venomfang Spider":     GIANT_SPIDER,
    "Marsh Troll":          TROLL,
    "Volcanic Troll":       TROLL,
    "Skeletal Archer":      SKELETON,
    "Bone Colossus":        SKELETON,
    "Undead Foreman":       DEATH_KNIGHT,
    # ── Humanoid enemies: use character class grids ──
    # Bandits — rough fighters using base class shapes
    "Bandit Fighter":       FIGHTER,
    "Bandit Archer":        RANGER,
    "Bandit Thief":         THIEF,
    "Bandit Mage":          MAGE,
    "Bandit Captain":       CHAMPION,
    # Iron Mercenaries — professional soldiers
    "Sellsword":            WARDER,
    "Mercenary Scout":      RANGER,
    "Mercenary Monk":       MONK,
    "Mercenary War-Cleric": CLERIC,
    "Mercenary Spellblade": SPELLBLADE,
    # Ashenmoor Cultists — corrupted spellcasters
    "Cultist Initiate":     MAGE,
    "Cultist Warrior":      WARDER,
    "Cultist Hexblade":     SPELLBLADE,
    "Cult Sorcerer":        ARCHMAGE,
    "High Cultist":         NECROMANCER,
    # Corrupted Guard — undead former soldiers
    "Crypt Soldier":    FIGHTER,
    "Crypt Ranger":     RANGER,
    "Crypt Paladin":    PALADIN,
    "Crypt Archmage":   ARCHMAGE,
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
    # ── New enemy palette overrides ──
    "Wolf":             {'C':(130,105,70,255),'D':(82,62,40,255),'H':(175,148,105,255),'K':(45,32,18,255),
                         'N':(148,118,78,255),'n':(88,65,38,255),'E':(255,220,80,255)},
    "Dire Wolf":        {'C':(80,75,90,255),'D':(48,44,58,255),'H':(115,108,130,255),'K':(25,22,32,255),
                         'N':(95,88,108,255),'n':(55,50,68,255),'E':(200,80,80,255)},
    "Bandit":           {'C':(105,88,70,255),'D':(65,52,38,255),'H':(148,128,105,255),'K':(32,25,15,255),
                         'N':(90,75,55,255),'n':(55,42,28,255)},
    "Highway Bandit":   {'C':(78,70,62,255),'D':(45,40,35,255),'H':(112,102,90,255),'K':(22,18,14,255),
                         'N':(68,58,48,255),'n':(38,32,24,255)},
    "Goblin Shaman":    {'C':(68,105,58,255),'D':(40,65,32,255),'H':(95,148,80,255),'K':(22,38,14,255),
                         'N':(75,112,62,255),'n':(40,68,30,255),'E':(180,120,255,255)},
    "Stone Sentinel":   {'M':(148,138,118,255),'m':(88,80,65,255),'H':(185,175,155,255),'K':(40,35,25,255),
                         'S':(158,148,128,255),'C':(138,128,108,255),'D':(82,75,58,255)},
    "Ash Revenant":     {'C':(140,95,60,255),'D':(88,58,32,255),'H':(188,138,95,255),'K':(42,25,10,255),
                         'R':(225,140,40,255),'S':(200,175,140,255),'s':(160,130,95,255),
                         'E':(255,210,80,255)},
    "Wraith":           {'C':(95,80,130,255),'D':(55,45,80,255),'H':(138,118,175,255),'K':(22,16,38,255),
                         's':(175,160,210,255),'S':(200,188,230,255),'E':(220,200,255,255)},
    "Crypt Shade":      {'C':(60,55,90,255),'D':(35,30,60,255),'H':(95,85,130,255),'K':(15,12,30,255),
                         's':(140,130,175,255),'S':(168,160,200,255),'E':(160,120,255,255)},
    "Kobold Firebrand": {'C':(88,55,38,255),'D':(52,30,18,255),'H':(128,82,58,255),'K':(28,12,5,255),
                         'N':(100,65,42,255),'n':(58,35,20,255),'E':(255,180,40,255)},
    "Ghoul":            {'C':(80,110,70,255),'D':(48,68,40,255),'H':(112,148,98,255),'K':(22,35,15,255),
                         'N':(92,122,78,255),'n':(52,72,38,255),'E':(200,255,140,255)},
    "Death Knight":     {'M':(62,68,88,255),'m':(35,40,55,255),'H':(98,108,135,255),'K':(15,18,28,255),
                         'B':(215,210,225,255),'b':(140,135,152,255),'G':(155,20,20,255),'g':(95,12,12,255)},
    "Undead Foreman":   {'M':(55,62,72,255),'m':(32,38,48,255),'H':(88,98,115,255),'K':(12,15,22,255),
                         'B':(205,200,215,255),'b':(130,125,140,255),'G':(120,40,40,255),'g':(75,20,20,255)},
    "Orc Chieftain":    {'M':(88,112,55,255),'m':(52,68,30,255),'H':(122,152,78,255),'K':(28,38,12,255),
                         'G':(205,165,25,255),'g':(130,100,15,255),'S':(95,130,60,255),'E':(255,240,100,255)},
    "Goblin King":      {'C':(72,112,58,255),'D':(42,68,32,255),'H':(102,152,82,255),'K':(18,38,10,255),
                         'G':(215,172,30,255),'g':(138,108,18,255)},
    "Grak the Goblin King": {'C':(72,112,58,255),'D':(42,68,32,255),'H':(102,152,82,255),'K':(18,38,10,255),
                         'G':(215,172,30,255),'g':(138,108,18,255)},
    "Cave Bat":         {'C':(52,38,68,255),'D':(30,20,42,255),'H':(82,62,105,255),'K':(15,8,25,255),
                         'N':(65,48,85,255),'n':(38,25,52,255),'E':(240,80,80,255)},
    "Lava Bat":         {'C':(52,38,68,255),'D':(30,20,42,255),'H':(82,62,105,255),'K':(15,8,25,255),
                         'N':(65,48,85,255),'n':(38,25,52,255),'E':(240,80,80,255)},
    # ── Beetles: dark chitinous carapace, glowing spots ──
    "Lava Beetle":      {'C':(55,35,18,255),'D':(32,18,8,255),'H':(90,55,28,255),'K':(18,8,2,255),
                         'N':(42,28,12,255),'n':(22,12,4,255),'E':(255,130,20,255)},
    "Cave-in Beetle":   {'C':(38,38,38,255),'D':(20,20,20,255),'H':(65,62,58,255),'K':(8,8,8,255),
                         'N':(30,28,25,255),'n':(15,12,10,255),'E':(180,210,255,255)},
    "Tunnel Beetle":    {'C':(42,35,22,255),'D':(25,18,10,255),'H':(70,58,38,255),'K':(12,8,3,255),
                         'N':(32,25,14,255),'n':(16,12,5,255),'E':(200,200,100,255)},
    # ── Giant Rats / Rodents ──
    "Giant Rat":        {'C':(105,88,72,255),'D':(65,52,38,255),'H':(148,128,105,255),'K':(32,22,12,255),
                         'N':(118,98,78,255),'n':(70,55,38,255),'E':(220,80,80,255)},
    "Dungeon Rat":      {'C':(82,75,65,255),'D':(48,42,32,255),'H':(118,108,92,255),'K':(22,18,12,255),
                         'N':(95,85,70,255),'n':(55,48,35,255),'E':(200,80,80,255)},
    "Sewer Rat":        {'C':(78,80,72,255),'D':(45,48,38,255),'H':(112,115,102,255),'K':(20,22,15,255),
                         'N':(88,92,78,255),'n':(48,52,38,255),'E':(200,200,80,255)},
    # ── Hatchlings / Small Drakes ──
    "Corrupted Hatchling": {'C':(55,85,48,255),'D':(32,52,25,255),'H':(80,122,68,255),'K':(15,28,10,255),
                         'N':(62,92,52,255),'n':(35,55,28,255),'R':(200,80,40,255),'E':(255,210,80,255)},
    "Cinder Drake":     {'C':(130,48,22,255),'D':(80,25,10,255),'H':(180,75,38,255),'K':(42,10,3,255),
                         'N':(148,55,25,255),'n':(88,30,12,255),'R':(255,165,30,255),'E':(255,220,50,255)},
    "Fire Lizard":      {'C':(120,55,20,255),'D':(72,30,8,255),'H':(168,82,32,255),'K':(38,12,2,255),
                         'N':(135,62,22,255),'n':(80,35,10,255),'R':(255,140,20,255),'E':(255,200,40,255)},
}

_ENEMY_BASE_COLORS = {
    "Goblin Warrior":   (92,118,62,255),
    "Goblin Archer":    (92,118,62,255),
    "Goblin Brute":     (82,108,52,255),
    "Goblin Shaman":    (68,105,58,255),
    "Goblin Scout":     (75,112,62,255),
    "Troll":            (62,98,52,255),
    "Marsh Troll":      (52,88,52,255),
    "Wolf":             (130,105,70,255),
    "Dire Wolf":        (80,75,90,255),
    "Bandit":           (105,88,70,255),
    "Stone Sentinel":   (148,138,118,255),
    "Ash Revenant":     (140,95,60,255),
    "Wraith":           (95,80,130,255),
    "Kobold Firebrand": (88,55,38,255),
    "Kobold Miner":     (78,48,32,255),
    "Ghoul":            (80,110,70,255),
    "Death Knight":     (62,68,88,255),
    "Orc Chieftain":    (88,112,55,255),
    "Goblin King":      (72,112,58,255),
    "Cave Bat":         (52,38,68,255),
    "Lava Bat":         (52,38,68,255),
    "Lava Beetle":      (55,35,18,255),
    "Cave-in Beetle":   (38,38,38,255),
    "Tunnel Beetle":    (42,35,22,255),
    "Giant Rat":        (105,88,72,255),
    "Dungeon Rat":      (82,75,65,255),
    "Sewer Rat":        (78,80,72,255),
    "Corrupted Hatchling": (55,85,48,255),
    "Cinder Drake":     (130,48,22,255),
    "Fire Lizard":      (120,55,20,255),
    # ── Bandits: rough leathers, browns and tawny rusts ──
    "Bandit Fighter":   (115, 82, 52, 255),
    "Bandit Archer":    (88, 102, 58, 255),
    "Bandit Thief":     (62, 58, 72, 255),
    "Bandit Mage":      (72, 52, 95, 255),
    "Bandit Captain":   (130, 75, 40, 255),
    # ── Iron Mercenaries: cold steel blues and greens ──
    "Sellsword":              (90, 105, 120, 255),
    "Mercenary Scout":        (68, 95, 68, 255),
    "Mercenary Monk":         (95, 88, 68, 255),
    "Mercenary War-Cleric":   (110, 105, 80, 255),
    "Mercenary Spellblade":   (75, 88, 130, 255),
    # ── Cultists: deep purples and blacks ──
    "Cultist Initiate":  (72, 42, 95, 255),
    "Cultist Warrior":   (55, 35, 75, 255),
    "Cultist Hexblade":  (48, 30, 80, 255),
    "Cult Sorcerer":     (35, 18, 72, 255),
    "High Cultist":      (25, 12, 58, 255),
    # ── Corrupted Guard: sickly greys and rot greens ──
    "Crypt Soldier":  (72, 78, 68, 255),
    "Crypt Ranger":   (65, 72, 60, 255),
    "Crypt Paladin":  (62, 68, 58, 255),
    "Crypt Archmage": (58, 60, 75, 255),
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
    # Try PNG first, fall back to procedural
    from ui.sprite_loader import draw_character_silhouette as _png_char
    if _png_char(surface, rect, class_name,
                 equipped_weapon=equipped_weapon,
                 armor_tier=armor_tier, highlight=highlight):
        return
    from ui.wiz_sprites import draw_wiz_character
    draw_wiz_character(surface, rect, class_name, highlight=highlight)

def draw_enemy_silhouette(surface, rect, enemy_template_key,
                           knowledge_tier=0, hover=False, dead=False):
    # Try PNG first, fall back to procedural
    from ui.sprite_loader import draw_enemy_silhouette as _png_enemy
    if _png_enemy(surface, rect, enemy_template_key,
                  knowledge_tier=knowledge_tier, hover=hover, dead=dead):
        return
    from ui.wiz_sprites import draw_wiz_enemy
    tier = max(-1, min(2, knowledge_tier))
    draw_wiz_enemy(surface, rect, enemy_template_key,
                   knowledge_tier=tier, hover=hover, dead=dead)
