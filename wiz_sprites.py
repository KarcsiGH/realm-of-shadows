"""
wiz_sprites.py — Wizardry-style sprite renderer for Realm of Shadows

All sprites drawn with direct pixel operations on a 48×80 canvas,
then scaled to the target rect. Dark background (6,6,10), tonal fills,
signature outline colour per creature type.

Public API (mirrors pixel_art.py):
    draw_wiz_character(surface, rect, class_name, highlight=False, dead=False)
    draw_wiz_enemy(surface, rect, template_key, knowledge_tier=0, hover=False, dead=False)
"""

import pygame

BG     = (6, 6, 10)
W, H   = 48, 80        # native canvas size

# ─────────────────────────────────────────────────────────────────────────────
#  PRIMITIVE HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _px(s, x, y, c):
    if 0 <= x < W and 0 <= y < H:
        s.set_at((x, y), c)

def _hl(s, x1, x2, y, c):
    for x in range(x1, x2 + 1): _px(s, x, y, c)

def _vl(s, x, y1, y2, c):
    for y in range(y1, y2 + 1): _px(s, x, y, c)

def _fr(s, x, y, w, h, c):           # filled rect
    for dy in range(h): _hl(s, x, x + w - 1, y + dy, c)

def _or(s, x, y, w, h, c):           # outline rect
    _hl(s, x, x + w - 1, y, c)
    _hl(s, x, x + w - 1, y + h - 1, c)
    _vl(s, x, y, y + h - 1, c)
    _vl(s, x + w - 1, y, y + h - 1, c)

def _new():
    s = pygame.Surface((W, H), pygame.SRCALPHA)
    s.fill(BG)
    return s

# ─────────────────────────────────────────────────────────────────────────────
#  SHARED HUMANOID FACE (front-facing, parameterised)
# ─────────────────────────────────────────────────────────────────────────────

def _face(s, cx, ty, skin, shadow, eye, has_beard=False):
    """Generic humanoid face centred at cx, top at ty, height ~12px."""
    S = skin; D = shadow; E = eye
    for y in range(ty, ty+10):
        hw = 5 - abs(y - ty - 4) // 3
        _hl(s, cx-hw, cx+hw, y, S)
    _hl(s, cx-3, cx+3, ty, D)           # forehead shadow
    _px(s, cx-2, ty+3, E); _px(s, cx-1, ty+3, E)   # left eye
    _px(s, cx+1, ty+3, E); _px(s, cx+2, ty+3, E)   # right eye
    _px(s, cx-2, ty+4, D); _px(s, cx+2, ty+4, D)   # pupils
    if has_beard:
        for y in range(ty+8, ty+12):
            _hl(s, cx-3, cx+3, y, D)

# ─────────────────────────────────────────────────────────────────────────────
#  CHARACTER SPRITES
# ─────────────────────────────────────────────────────────────────────────────

def _char_fighter(s):
    O=(200,210,230); M=(110,115,135); D=(55,58,72); G=(180,160,80); R=(180,50,45)
    # helm
    _hl(s,19,28,5,O); _hl(s,17,30,6,M); _hl(s,17,30,7,M); _hl(s,16,31,8,M)
    _vl(s,16,6,16,O); _vl(s,31,6,16,O)
    for y in range(11,14): _hl(s,17,30,y,D); _hl(s,19,22,12,M); _hl(s,25,28,12,M)
    _hl(s,17,30,14,M); _hl(s,17,30,16,O); _hl(s,18,29,17,G); _hl(s,18,29,18,G)
    # pauldrons
    _hl(s,10,16,20,O); _hl(s,31,37,20,O)
    for y in range(21,26): _hl(s,10,16,y,M); _hl(s,31,37,y,M)
    _hl(s,10,16,25,O); _hl(s,31,37,25,O)
    _hl(s,11,15,21,O); _hl(s,32,36,21,O)
    # breastplate
    for y in range(20,42): _hl(s,17,30,y,M); _px(s,17,y,O); _px(s,30,y,O); _px(s,18,y,O)
    _vl(s,23,21,41,D); _vl(s,24,21,41,D)
    _hl(s,19,22,27,D); _hl(s,25,28,27,D)
    # belt + buckle
    for y in range(42,45): _hl(s,17,30,y,D); _px(s,17,y,O); _px(s,30,y,O)
    _fr(s,22,42,4,3,G); _or(s,22,42,4,3,O)
    # tabard
    for tx in range(18,30,2): _vl(s,tx,45,55,R)
    # sword right
    _vl(s,37,8,40,O); _vl(s,38,8,40,O); _px(s,37,7,O); _px(s,38,6,O)
    _hl(s,34,42,28,G); _hl(s,34,42,29,G); _vl(s,37,29,40,D)
    # upper arms
    for y in range(26,42): _hl(s,11,15,y,M); _px(s,11,y,O); _px(s,15,y,O)
    for y in range(26,42): _hl(s,32,36,y,M); _px(s,32,y,O); _px(s,36,y,O)
    # shield
    for y in range(24,52):
        hw=7-abs(y-37)//4; _hl(s,4,4+hw,y,D); _px(s,4,y,O); _px(s,4+hw,y,O); _px(s,5,y,O)
    _hl(s,4,12,24,O); _hl(s,4,10,51,O)
    _fr(s,6,36,4,4,G); _or(s,6,36,4,4,O)
    _vl(s,8,26,50,G); _hl(s,5,11,38,G)
    # legs
    for y in range(55,77): _hl(s,18,22,y,M); _px(s,18,y,O); _px(s,22,y,O)
    for y in range(55,77): _hl(s,25,29,y,M); _px(s,25,y,O); _px(s,29,y,O)
    _hl(s,18,22,64,D); _hl(s,25,29,64,D)
    # boots
    for y in range(77,80): _hl(s,17,23,y,D); _hl(s,24,30,y,D)
    _hl(s,16,24,79,O); _hl(s,23,31,79,O)

def _char_mage(s):
    O=(170,120,220); M=(100,65,160); D=(55,35,95); G=(160,220,255); Y=(240,220,80)
    # pointed hat
    for i in range(8): hw=i//2+1; _hl(s,23-hw,24+hw,4+i,D if i<4 else M)
    _hl(s,19,28,12,O); _hl(s,18,29,13,D)   # brim
    # face
    _face(s,23,14,(210,185,155),(150,120,90),G)
    # robe collar
    _hl(s,18,29,24,O); _hl(s,17,30,25,M)
    # robe body
    for y in range(25,62):
        hw=4+y//10; _hl(s,23-hw,24+hw,y,M); _px(s,23-hw,y,O); _px(s,24+hw,y,O)
    # belt sash
    _hl(s,17,30,42,Y); _hl(s,17,30,43,Y)
    # staff (left side)
    _vl(s,13,5,62,O); _vl(s,14,5,62,D)
    _fr(s,11,5,5,5,G); _or(s,11,5,5,5,O)   # staff crystal
    _px(s,13,3,G); _px(s,13,4,G)            # tip glow
    # spell hand (right) — glow orb
    _fr(s,33,35,5,5,G); _or(s,33,35,5,5,O)
    _px(s,35,33,O); _px(s,36,34,G)
    # robe hem + feet
    for y in range(62,67): _hl(s,19,28,y,D); _px(s,19,y,O); _px(s,28,y,O)
    _hl(s,20,23,67,D); _hl(s,24,27,67,D)
    _hl(s,19,24,70,O); _hl(s,23,28,70,O)

def _char_cleric(s):
    O=(220,215,200); M=(155,148,130); D=(85,80,65); G=(220,185,60); HL=(255,240,180)
    # hood
    for i in range(8): hw=3+i//2; _hl(s,23-hw,24+hw,4+i,M)
    _hl(s,18,29,11,O); _vl(s,18,4,11,O); _vl(s,29,4,11,O)
    # face
    _face(s,23,12,(210,185,155),(140,110,85),HL)
    # vestment
    _hl(s,16,31,22,O)
    for y in range(22,60): _hl(s,17,30,y,M); _px(s,17,y,O); _px(s,30,y,O)
    # holy symbol on chest
    _vl(s,23,26,36,G); _hl(s,20,26,30,G); _or(s,21,27,4,4,O)
    # mace (right)
    _vl(s,36,20,52,D); _vl(s,37,20,52,M)
    _fr(s,34,15,6,6,M); _or(s,34,15,6,6,O)
    # sleeves
    for y in range(24,42): _hl(s,12,16,y,M); _px(s,12,y,O); _px(s,16,y,O)
    # hem + sandals
    for y in range(60,67): _hl(s,17,30,y,D); _px(s,17,y,O); _px(s,30,y,O)
    _hl(s,19,23,70,D); _hl(s,24,28,70,D)
    _hl(s,18,24,73,O); _hl(s,23,29,73,O)

def _char_thief(s):
    O=(160,155,165); M=(85,82,95); D=(45,43,55); BR=(120,88,50); Y=(220,195,60)
    # dark hood
    for i in range(10): hw=4+i//3; _hl(s,23-hw,24+hw,4+i,D)
    _hl(s,18,29,13,O); _vl(s,17,5,13,O); _vl(s,30,5,13,O)
    # wrapped face — just eyes visible
    for y in range(9,13): _hl(s,18,29,y,D)
    _px(s,21,10,Y); _px(s,22,10,Y)
    _px(s,25,10,Y); _px(s,26,10,Y)
    # leather body
    for y in range(22,55): _hl(s,19,28,y,M); _px(s,19,y,O); _px(s,28,y,O)
    # straps/harness
    _vl(s,22,23,42,D); _vl(s,25,23,42,D)
    _hl(s,19,28,30,BR); _hl(s,19,28,38,BR)
    # daggers at hips
    for y in range(38,52): _px(s,17,y,O); _px(s,30,y,O)
    _px(s,17,52,O); _px(s,16,53,O)
    _px(s,30,52,O); _px(s,31,53,O)
    # arms — thin
    for y in range(24,50): _px(s,14,y,M); _px(s,15,y,M); _px(s,14,y,O)
    for y in range(24,46): _px(s,32,y,M); _px(s,33,y,M); _px(s,33,y,O)
    # legs — dark trousers
    for y in range(55,75): _hl(s,19,22,y,D); _px(s,19,y,O); _px(s,22,y,O)
    for y in range(55,75): _hl(s,25,28,y,D); _px(s,25,y,O); _px(s,28,y,O)
    _hl(s,18,23,75,O); _hl(s,24,29,75,O)

def _char_ranger(s):
    O=(140,175,110); M=(80,110,55); D=(42,65,25); BR=(130,95,55); G=(200,180,100)
    # leather cap
    _hl(s,20,27,5,BR); _hl(s,18,29,6,BR); _hl(s,18,29,7,BR); _hl(s,19,28,8,O)
    # face
    _face(s,23,9,(200,170,130),(140,105,75),(60,180,80))
    # leather armor
    _hl(s,17,30,20,O)
    for y in range(20,55): _hl(s,18,29,y,M); _px(s,18,y,O); _px(s,29,y,O)
    _hl(s,18,29,33,D); _hl(s,18,29,34,D)   # belt
    _fr(s,22,33,4,2,BR); _or(s,22,33,4,2,O)
    # quiver (right side)
    for y in range(15,42): _px(s,32,y,BR); _px(s,33,y,BR)
    for i in range(4): _px(s,32,15+i*4,G); _px(s,33,15+i*4,G)   # arrow fletches
    # bow (left side)
    for i in range(20): _px(s,12,10+i*3,O)   # crude bow arc
    for i in range(20): _px(s,11,12+i*3,O)
    _vl(s,12,10,70,O); _vl(s,11,12,68,O)
    # arms
    for y in range(22,46): _hl(s,13,17,y,M); _px(s,13,y,O)
    for y in range(22,42): _hl(s,30,34,y,M); _px(s,34,y,O)
    # legs
    for y in range(55,76): _hl(s,19,22,y,M); _px(s,19,y,O); _px(s,22,y,O)
    for y in range(55,76): _hl(s,25,28,y,M); _px(s,25,y,O); _px(s,28,y,O)
    _hl(s,18,23,76,O); _hl(s,24,29,76,O)

def _char_monk(s):
    O=(190,170,140); M=(120,100,75); D=(70,55,38); SK=(210,180,148); R=(180,50,45)
    # shaved head
    for y in range(5,13):
        hw=4-abs(y-8)//2; _hl(s,23-hw,24+hw,y,SK)
    _hl(s,19,28,5,D); _hl(s,19,28,12,D)
    # face
    _face(s,23,6,SK,(150,115,80),(240,200,80))
    # gi top — open chest
    for y in range(20,45): _hl(s,19,28,y,M); _px(s,19,y,O); _px(s,28,y,O)
    _vl(s,23,20,44,D)   # lapel
    for y in range(20,28): _hl(s,20,22,y,SK); _hl(s,25,27,y,SK)  # chest skin
    # red sash
    _hl(s,17,30,44,R); _hl(s,17,30,45,R); _hl(s,17,30,46,R)
    # fighting stance — arms raised/extended
    for y in range(16,34): _hl(s,11,16,y,SK); _px(s,11,y,O); _px(s,16,y,O)  # left arm
    for y in range(14,30): _hl(s,31,36,y,SK); _px(s,31,y,O); _px(s,36,y,O)  # right arm raised
    # fists
    _fr(s,9,34,6,5,SK); _or(s,9,34,6,5,O)
    _fr(s,30,8,6,5,SK); _or(s,30,8,6,5,O)
    # pants
    for y in range(46,76): _hl(s,18,22,y,D); _px(s,18,y,O); _px(s,22,y,O)
    for y in range(46,76): _hl(s,25,29,y,D); _px(s,25,y,O); _px(s,29,y,O)
    _hl(s,17,23,76,O); _hl(s,24,30,76,O)

def _char_paladin(s):
    O=(230,220,190); M=(165,158,130); D=(95,90,70); G=(220,185,60); HL=(255,240,200)
    BL=(140,160,220)
    # great helm — full face cover
    _hl(s,18,29,4,O); _hl(s,17,30,5,M); _hl(s,16,31,6,M); _hl(s,16,31,7,M)
    _hl(s,16,31,8,M); _hl(s,16,31,9,M); _hl(s,16,31,10,M)
    _vl(s,16,5,17,O); _vl(s,31,5,17,O)
    # cross-slit visor
    _hl(s,18,29,13,D); _hl(s,18,29,14,D)
    _vl(s,23,11,16,D); _vl(s,24,11,16,D)
    _px(s,21,13,M); _px(s,26,13,M)     # eye glow through cross
    _hl(s,17,30,17,G); _hl(s,17,30,18,G)
    # heavy pauldrons
    _hl(s,9,17,19,O); _hl(s,30,38,19,O)
    for y in range(20,27): _hl(s,9,17,y,M); _hl(s,30,38,y,M)
    _hl(s,9,17,26,O); _hl(s,30,38,26,O)
    # breastplate with holy symbol
    for y in range(19,44): _hl(s,17,30,y,M); _px(s,17,y,O); _px(s,30,y,O); _px(s,18,y,HL)
    _vl(s,23,22,42,G); _hl(s,19,27,30,G)    # golden cross
    _or(s,20,26,7,7,O)                        # circle around cross
    # arms
    for y in range(26,46): _hl(s,10,15,y,M); _px(s,10,y,O); _px(s,15,y,O)
    for y in range(26,46): _hl(s,32,37,y,M); _px(s,32,y,O); _px(s,37,y,O)
    # shield + sword same as fighter but gold trim
    for y in range(26,54):
        hw=7-abs(y-39)//4; _hl(s,3,3+hw,y,D); _px(s,3,y,O); _px(s,3+hw,y,O)
    _fr(s,5,37,4,4,G); _or(s,5,37,4,4,O)
    _vl(s,38,6,46,HL); _vl(s,39,6,46,M); _hl(s,35,43,28,G)
    # legs
    for y in range(44,77): _hl(s,18,22,y,M); _px(s,18,y,O); _px(s,22,y,O)
    for y in range(44,77): _hl(s,25,29,y,M); _px(s,25,y,O); _px(s,29,y,O)
    _hl(s,17,23,77,O); _hl(s,24,30,77,O)

def _char_warder(s):
    O=(155,145,120); M=(95,88,70); D=(55,50,38); G=(180,155,65); BR=(130,95,55)
    # open-faced helm
    _hl(s,19,28,5,O); _hl(s,17,30,6,M); _hl(s,17,30,7,M)
    _hl(s,16,31,8,M); _hl(s,16,31,9,M)
    _vl(s,16,6,13,O); _vl(s,31,6,13,O); _hl(s,17,30,13,O)
    # face in helm
    _face(s,23,10,(200,170,130),(140,105,75),(180,140,80))
    # medium armor
    for y in range(20,44): _hl(s,17,30,y,M); _px(s,17,y,O); _px(s,30,y,O)
    _hl(s,17,30,32,D); _fr(s,22,32,4,3,BR)
    # spear (right)
    _vl(s,36,2,65,BR); _vl(s,37,2,65,D)
    _px(s,35,2,O); _px(s,36,1,O); _px(s,37,1,O); _px(s,38,2,O)  # spearhead
    _hl(s,34,39,3,O); _hl(s,34,39,4,O)
    # round shield (left)
    for y in range(26,48):
        hw=6-abs(y-37)*6//22; _hl(s,6,6+hw,y,D); _px(s,6,y,O); _px(s,6+hw,y,O)
    _hl(s,6,14,26,O); _hl(s,7,13,48,O)
    _fr(s,9,35,4,4,G); _or(s,9,35,4,4,O)
    # arms
    for y in range(22,44): _hl(s,11,16,y,M); _px(s,11,y,O)
    for y in range(22,44): _hl(s,31,36,y,M); _px(s,36,y,O)
    # legs
    for y in range(44,76): _hl(s,18,22,y,M); _px(s,18,y,O); _px(s,22,y,O)
    for y in range(44,76): _hl(s,25,29,y,M); _px(s,25,y,O); _px(s,29,y,O)
    _hl(s,17,23,76,O); _hl(s,24,30,76,O)

def _char_archmage(s):
    O=(200,140,255); M=(130,80,200); D=(70,35,130); G=(160,220,255); Y=(255,240,100)
    SK=(205,178,148)
    # wide-brimmed star hat
    for i in range(7): hw=i+1; _hl(s,23-hw,24+hw,4+i,D)
    _hl(s,16,31,11,O); _hl(s,15,32,12,D)  # wide brim
    # stars on hat
    for sx,sy in [(18,6),(27,7),(22,9),(25,5)]: _px(s,sx,sy,Y)
    # aged face
    _face(s,23,13,SK,(150,118,85),G,has_beard=True)
    # elaborate robes
    _hl(s,15,32,24,O)
    for y in range(24,64):
        hw=5+y//8; _hl(s,23-hw,24+hw,y,M); _px(s,23-hw,y,O); _px(s,24+hw,y,O)
    # gold trim on robe
    _hl(s,16,31,24,Y); _hl(s,17,30,42,Y); _hl(s,18,29,62,Y)
    # arcane runes on robe
    for rx,ry in [(21,32),(26,36),(20,44),(28,48)]: _px(s,rx,ry,G); _px(s,rx+1,ry,G)
    # staff with orb
    _vl(s,12,8,65,D); _vl(s,13,8,65,M)
    _fr(s,9,4,7,6,G); _or(s,9,4,7,6,O)
    _px(s,12,3,G); _px(s,13,3,G)
    # casting hand — crackling energy
    for ex,ey in [(35,28),(36,27),(37,29),(36,30),(38,28)]: _px(s,ex,ey,Y)
    _fr(s,33,31,5,5,G); _or(s,33,31,5,5,O)
    # feet
    _hl(s,20,24,70,D); _hl(s,23,27,70,D); _hl(s,19,25,73,O); _hl(s,22,28,73,O)

def _char_necromancer(s):
    O=(150,100,180); M=(85,50,120); D=(40,20,65); V=(200,200,215); G=(100,220,140)
    SK=(195,168,140)
    # skull-cowl hood
    for y in range(4,14):
        hw=4+y//4; _hl(s,23-hw,24+hw,y,D)
    _vl(s,17,4,13,O); _vl(s,30,4,13,O); _hl(s,17,30,13,O)
    # skull face pieces visible in hood
    _fr(s,19,8,4,4,D); _fr(s,25,8,4,4,D)   # eye sockets
    _px(s,20,9,G); _px(s,21,9,G)            # left soul-fire
    _px(s,26,9,G); _px(s,27,9,G)            # right soul-fire
    _hl(s,20,27,13,D)                        # jaw line
    for tx in range(20,28,2): _px(s,tx,13,V)  # teeth
    # dark robes
    for y in range(14,64):
        hw=4+y//7; _hl(s,23-hw,24+hw,y,M); _px(s,23-hw,y,O); _px(s,24+hw,y,O)
    # bone scepter
    _vl(s,13,6,62,D); _vl(s,14,6,62,M)
    _fr(s,11,4,6,5,V); _or(s,11,4,6,5,O)   # skull head
    _px(s,13,4,D); _px(s,14,4,D)            # skull eyes
    # death hand — skeletal fingers
    for fx in range(33,40): _vl(s,fx,42,50,V if fx%2==0 else D)
    _hl(s,33,39,42,O)
    # hem + feet
    _hl(s,19,28,64,D); _hl(s,20,24,68,D); _hl(s,23,27,68,D)
    _hl(s,19,25,72,O); _hl(s,22,28,72,O)

def _char_spellblade(s):
    O=(140,180,220); M=(80,110,160); D=(40,60,100); G=(180,155,65); GL=(160,220,255)
    # half-helm
    _hl(s,19,28,5,O); _hl(s,17,30,6,M); _hl(s,17,30,7,M)
    _vl(s,17,5,12,O); _vl(s,30,5,12,O); _hl(s,17,30,12,O)
    # face (lower half visible)
    _face(s,23,8,(200,170,130),(140,105,75),GL)
    # arcane-inscribed armor
    for y in range(20,44): _hl(s,17,30,y,M); _px(s,17,y,O); _px(s,30,y,O)
    # glowing runes on armor
    for rx,ry in [(19,26),(22,30),(26,28),(28,34)]: _px(s,rx,ry,GL); _px(s,rx+1,ry,GL)
    _hl(s,17,30,33,D)
    # enchanted sword (right) — blade glows
    _vl(s,37,5,40,GL); _vl(s,38,5,40,O)
    _px(s,37,4,GL); _px(s,38,3,GL); _px(s,37,3,GL)  # glowing tip
    _hl(s,34,42,26,G); _hl(s,34,42,27,G)
    # glow effect around blade
    for gy in range(5,40,3): _px(s,36,gy,GL); _px(s,39,gy,GL)
    # buckler
    for y in range(26,44): _hl(s,10,16,y,D); _px(s,10,y,O); _px(s,16,y,O)
    _hl(s,10,16,26,O); _hl(s,10,16,43,O); _fr(s,12,33,4,4,GL)
    # arms + legs same structure as fighter
    for y in range(26,44): _hl(s,31,36,y,M); _px(s,31,y,O); _px(s,36,y,O)
    for y in range(44,76): _hl(s,18,22,y,M); _px(s,18,y,O); _px(s,22,y,O)
    for y in range(44,76): _hl(s,25,29,y,M); _px(s,25,y,O); _px(s,29,y,O)
    _hl(s,17,23,76,O); _hl(s,24,30,76,O)

def _char_champion(s):
    O=(220,215,195); M=(145,140,120); D=(80,78,65); G=(220,185,60); R=(185,55,50)
    CL=(180,160,220)
    # plumed great helm
    for i in range(5): _px(s,23,2+i,R); _px(s,24,2+i,R)  # plume
    _hl(s,18,29,6,O); _hl(s,17,30,7,M); _hl(s,16,31,8,M)
    _hl(s,15,32,9,M); _hl(s,15,32,10,M); _hl(s,15,32,11,M)
    _vl(s,15,7,17,O); _vl(s,32,7,17,O)
    for y in range(12,15): _hl(s,16,31,y,D); _hl(s,19,22,13,M); _hl(s,25,28,13,M)
    _hl(s,16,31,15,M); _hl(s,16,31,17,O); _hl(s,17,30,18,G)
    # ornate pauldrons (bigger than fighter)
    for x in [9,10,36,37]: _vl(s,x,19,28,O)
    for y in range(19,27): _hl(s,9,17,y,M); _hl(s,30,38,y,M)
    _hl(s,9,17,27,O); _hl(s,30,38,27,O)
    for gx in range(10,17,2): _px(s,gx,20,G)  # gold studs
    for gx in range(31,38,2): _px(s,gx,20,G)
    # breastplate
    for y in range(19,44): _hl(s,17,30,y,M); _px(s,17,y,O); _px(s,30,y,O); _px(s,18,y,O)
    _vl(s,23,22,42,D); _vl(s,24,22,42,D)
    # heraldic lion on chest (simplified)
    _fr(s,21,28,6,6,CL); _or(s,21,28,6,6,O)
    # belt
    for y in range(44,47): _hl(s,17,30,y,D)
    _fr(s,22,44,4,3,G); _or(s,22,44,4,3,O)
    # great sword (two-handed, right side)
    _vl(s,36,4,50,O); _vl(s,37,4,50,M); _vl(s,38,4,50,D)
    _px(s,36,3,O); _px(s,37,2,O); _px(s,38,3,O)
    _hl(s,33,42,22,G); _hl(s,33,42,23,G); _hl(s,33,42,24,G)
    # arms — both on sword
    for y in range(26,50): _hl(s,30,36,y,M); _px(s,30,y,O); _px(s,36,y,O)
    _hl(s,12,17,22,O)
    for y in range(26,44): _hl(s,11,16,y,M); _px(s,11,y,O)
    # legs
    for y in range(47,77): _hl(s,18,22,y,M); _px(s,18,y,O); _px(s,22,y,O)
    for y in range(47,77): _hl(s,25,29,y,M); _px(s,25,y,O); _px(s,29,y,O)
    _hl(s,17,23,77,O); _hl(s,24,30,77,O)

def _char_assassin(s):
    O=(120,110,140); M=(65,60,80); D=(32,28,45); Y=(220,195,55); BL=(60,120,200)
    # full mask — only glowing eyes
    for y in range(5,15): _hl(s,18,29,y,D)
    _vl(s,17,5,15,O); _vl(s,30,5,15,O)
    _hl(s,18,29,5,O); _hl(s,18,29,15,O)
    _px(s,21,9,BL); _px(s,22,9,BL); _px(s,25,9,BL); _px(s,26,9,BL)  # cold eyes
    # lithe dark bodysuit
    for y in range(15,58): _hl(s,19,28,y,M); _px(s,19,y,O); _px(s,28,y,O)
    # blade straps
    _hl(s,17,30,26,D); _hl(s,17,30,38,D)
    _vl(s,22,26,38,D); _vl(s,25,26,38,D)
    # twin daggers — crossed on back
    _vl(s,14,16,44,O); _vl(s,33,16,44,O)
    for i in range(14): _px(s,14+i,16+i,Y); _px(s,32-i,16+i,Y)
    # poison vials at belt
    _fr(s,17,38,3,5,BL); _or(s,17,38,3,5,O)
    _fr(s,28,38,3,5,BL); _or(s,28,38,3,5,O)
    # legs — slim, dark
    for y in range(58,76): _hl(s,19,22,y,D); _px(s,19,y,O); _px(s,22,y,O)
    for y in range(58,76): _hl(s,25,28,y,D); _px(s,25,y,O); _px(s,28,y,O)
    _hl(s,18,23,76,O); _hl(s,24,29,76,O)

def _char_warden(s):
    O=(120,165,100); M=(68,110,52); D=(35,65,25); BR=(130,95,55); G=(200,175,80)
    # bark-and-leaf helm
    _hl(s,18,29,5,D); _hl(s,17,30,6,M); _hl(s,17,30,7,M)
    _hl(s,16,31,8,M); _vl(s,16,5,13,O); _vl(s,31,5,13,O); _hl(s,17,30,13,O)
    # leaf sprig from helm
    for i in range(4): _px(s,24+i,3-i,M); _px(s,22-i,4-i,M)
    # face
    _face(s,23,9,(195,168,138),(132,100,72),(200,190,100))
    # natural armor — bark/leather
    for y in range(20,50): _hl(s,17,30,y,M); _px(s,17,y,O); _px(s,30,y,O)
    # scale pattern
    for y in range(20,48,4):
        for x in range(18,29,3): _px(s,x,y,D); _px(s,x+1,y,D)
    # vine belt
    _hl(s,17,30,40,G); _hl(s,17,30,41,G)
    # druidic staff
    _vl(s,13,4,65,BR); _vl(s,14,4,65,D)
    for i in range(3): _px(s,11+i*2,5+i*2,M)  # branches
    _fr(s,11,2,5,4,M); _or(s,11,2,5,4,O)       # rough crystal
    # arms
    for y in range(22,48): _hl(s,12,16,y,M); _px(s,12,y,O)
    for y in range(22,44): _hl(s,31,35,y,M); _px(s,35,y,O)
    # legs
    for y in range(50,76): _hl(s,18,22,y,M); _px(s,18,y,O); _px(s,22,y,O)
    for y in range(50,76): _hl(s,25,29,y,M); _px(s,25,y,O); _px(s,29,y,O)
    _hl(s,17,23,76,O); _hl(s,24,30,76,O)

def _char_witch(s):
    O=(180,100,200); M=(110,55,145); D=(55,20,80); G=(160,220,100); Y=(240,220,70)
    SK=(205,175,145); BR=(120,88,50)
    # tall crooked hat
    for i in range(12):
        ox=i//4 if i>6 else 0
        hw=max(1,3-i//5); _hl(s,22+ox-hw,23+ox+hw,3+i,D)
    _hl(s,16,31,14,O); _hl(s,15,32,15,D)
    # wild hair
    for i in range(4): _px(s,15,16+i*2,M); _px(s,32,15+i*2,M)
    # weathered face
    _face(s,23,16,SK,(148,110,75),Y,has_beard=False)
    # wart
    _px(s,27,20,D)
    # robes
    for y in range(26,65):
        hw=4+y//9; _hl(s,23-hw,24+hw,y,M); _px(s,23-hw,y,O); _px(s,24+hw,y,O)
    # cauldron stir (left arm)
    for y in range(28,50): _hl(s,12,16,y,M); _px(s,12,y,O)
    _fr(s,9,50,10,8,D); _or(s,9,50,10,8,O)   # cauldron
    _px(s,12,50,G); _px(s,13,50,G); _px(s,14,49,G)  # bubbles
    # broom / wand (right)
    _vl(s,35,10,62,BR if True else D); _vl(s,36,10,62,D)
    for i in range(5): _px(s,33+i,62,BR); _px(s,33+i,63,BR); _px(s,33+i,64,BR)
    # black cat familiar at feet
    for cx2,cy2 in [(20,70),(21,70),(22,70),(20,71),(22,71),(19,72),(23,72),(21,72)]:
        _px(s,cx2,cy2,D)
    _px(s,21,69,O); _px(s,22,69,O)  # ears
    # feet
    _hl(s,19,24,73,O); _hl(s,23,28,73,O)

def _char_beastlord(s):
    O=(175,140,90); M=(115,85,50); D=(65,45,22); G=(220,175,70); SK=(210,178,145)
    # horned barbarian helm (open)
    for i in range(3): _px(s,15+i,9-i,O); _px(s,32-i,9-i,O)  # horns
    _hl(s,18,29,7,M); _hl(s,17,30,8,M); _vl(s,17,7,12,O); _vl(s,30,7,12,O)
    _hl(s,17,30,12,O)
    # tattooed face
    _face(s,23,8,(195,158,122),(135,100,68),(220,180,50))
    for i in range(3): _px(s,18+i,11,D); _px(s,27+i,11,D)  # war paint
    # fur/hide torso
    for y in range(20,46): _hl(s,17,30,y,M); _px(s,17,y,O); _px(s,30,y,O)
    for y in range(20,30): _px(s,19,y,D); _px(s,28,y,D)     # fur texture
    # great axe
    _vl(s,36,8,62,D); _vl(s,37,8,62,M)
    _fr(s,33,8,8,12,M); _or(s,33,8,8,12,O)  # axe head
    _px(s,33,8,O); _px(s,40,8,O); _px(s,41,14,O); _px(s,32,14,O)  # sharp edges
    # arms — huge
    for y in range(20,50): _hl(s,11,16,y,M); _px(s,11,y,O); _px(s,16,y,O)
    for y in range(20,50): _hl(s,31,36,y,M); _px(s,31,y,O); _px(s,36,y,O)
    # legs
    for y in range(46,76): _hl(s,18,22,y,M); _px(s,18,y,O); _px(s,22,y,O)
    for y in range(46,76): _hl(s,25,29,y,M); _px(s,25,y,O); _px(s,29,y,O)
    _hl(s,17,23,76,O); _hl(s,24,30,76,O)

def _char_crusader(s):
    # Like paladin but warmer, more church militant
    O=(230,215,180); M=(165,152,118); D=(90,82,58); G=(220,185,60); R=(185,50,45)
    HL=(255,245,210)
    _hl(s,18,29,5,O); _hl(s,17,30,6,M); _hl(s,16,31,7,M); _hl(s,16,31,9,M)
    _vl(s,16,5,16,O); _vl(s,31,5,16,O)
    for y in range(11,14): _hl(s,17,30,y,D); _hl(s,19,22,12,M); _hl(s,25,28,12,M)
    _hl(s,17,30,16,O); _hl(s,17,30,17,G)
    _hl(s,10,17,19,O); _hl(s,30,37,19,O)
    for y in range(19,26): _hl(s,10,17,y,M); _hl(s,30,37,y,M)
    for y in range(20,44): _hl(s,17,30,y,M); _px(s,17,y,O); _px(s,30,y,O); _px(s,18,y,HL)
    # crusader cross
    _vl(s,23,22,42,R); _vl(s,24,22,42,R); _hl(s,19,28,30,R); _hl(s,19,28,31,R)
    for y in range(44,47): _hl(s,17,30,y,D)
    _fr(s,22,44,4,3,G); _or(s,22,44,4,3,O)
    _vl(s,38,6,40,HL); _vl(s,39,6,40,O); _hl(s,35,43,26,G)
    for y in range(26,44): _hl(s,10,15,y,M); _px(s,10,y,O)
    for y in range(26,44): _hl(s,32,37,y,M); _px(s,37,y,O)
    for y in range(24,52): _hl(s,4,13,y,D); _px(s,4,y,O); _px(s,13,y,O)
    _fr(s,7,36,4,4,G); _or(s,7,36,4,4,O)
    for y in range(47,77): _hl(s,18,22,y,M); _px(s,18,y,O); _px(s,22,y,O)
    for y in range(47,77): _hl(s,25,29,y,M); _px(s,25,y,O); _px(s,29,y,O)
    _hl(s,17,23,77,O); _hl(s,24,30,77,O)

def _char_high_priest(s):
    O=(230,225,210); M=(165,158,140); D=(90,85,70); G=(220,185,60); HL=(255,248,220)
    # mitre (tall pointed headdress)
    for i in range(14): hw=max(1,4-i//3); _hl(s,23-hw,24+hw,2+i,M if i<10 else D)
    _hl(s,16,31,15,O); _hl(s,17,30,16,D)
    _vl(s,23,2,15,G); _hl(s,18,29,8,G)  # cross on mitre
    # vestments — elaborate
    _face(s,23,17,( 205,178,148),(142,108,77),HL,has_beard=True)
    for y in range(27,64):
        hw=5+y//9; _hl(s,23-hw,24+hw,y,M); _px(s,23-hw,y,O); _px(s,24+hw,y,O)
    _vl(s,23,27,63,G); _hl(s,17,30,38,G); _hl(s,17,30,39,G)
    # jewel panels
    for jx,jy in [(20,30),(26,30),(19,46),(28,46)]:
        _fr(s,jx,jy,3,3,G); _or(s,jx,jy,3,3,O)
    # crozier
    _vl(s,13,6,65,D); _vl(s,14,6,65,M)
    for i in range(5): _px(s,14+i,6+i,O); _px(s,14+i,5+i,M)  # scroll top
    # blessing hand
    for fx in range(32,38): _vl(s,fx,40,47,M if fx%2==0 else D)
    _hl(s,32,37,40,O)
    _hl(s,19,24,70,D); _hl(s,23,28,70,D); _hl(s,18,25,73,O); _hl(s,22,29,73,O)

def _char_shadow_master(s):
    O=(140,130,160); M=(60,55,80); D=(25,20,40); BL=(80,130,220); G=(80,220,160)
    # void hood — pure darkness
    for y in range(4,16): _hl(s,17,30,y,D)
    _vl(s,16,4,15,O); _vl(s,31,4,15,O); _hl(s,17,30,4,O); _hl(s,17,30,15,O)
    # glowing eyes in void
    _px(s,21,9,BL); _px(s,22,9,BL); _px(s,25,9,BL); _px(s,26,9,BL)
    # shadow form body — partially transparent
    for y in range(15,62): _hl(s,19,28,y,M); _px(s,19,y,O); _px(s,28,y,O)
    # shadow tendrils
    for i in range(5): _px(s,14+i,25+i*3,M); _px(s,33-i,28+i*3,M)
    _vl(s,13,30,55,D); _vl(s,34,24,50,D)
    # twin shadow blades
    for i in range(16): _px(s,14+i,18+i,BL); _px(s,14+i,19+i,G)
    for i in range(14): _px(s,33-i,20+i,BL); _px(s,33-i,21+i,G)
    # legs fade to shadow
    for y in range(62,76): _hl(s,19,22,y,D); _hl(s,25,28,y,D)
    _hl(s,18,23,76,O); _hl(s,24,29,76,O)

def _char_templar(s):
    O=(215,208,195); M=(145,138,122); D=(78,74,64); G=(215,180,55); BL=(140,158,220)
    # fortress helm — flat top, full cover
    _hl(s,17,30,5,O); _hl(s,16,31,6,M); _hl(s,15,32,7,M); _hl(s,15,32,8,M)
    _hl(s,15,32,9,M); _hl(s,15,32,10,M)
    _vl(s,15,6,18,O); _vl(s,32,6,18,O); _hl(s,15,32,18,O)
    # narrow visor slot
    _hl(s,17,30,13,D); _hl(s,17,30,14,D); _hl(s,17,30,15,D)
    _hl(s,19,28,14,BL)  # blue tint through visor
    _hl(s,16,31,18,G)
    # tower shield — massive, left side
    for y in range(22,60): _hl(s,3,13,y,D); _px(s,3,y,O); _px(s,13,y,O)
    _hl(s,3,13,22,O); _hl(s,3,13,59,O)
    _fr(s,6,36,5,5,G); _or(s,6,36,5,5,O)
    _vl(s,8,24,58,G); _hl(s,4,12,40,G)  # shield cross
    # heavy plate body
    for y in range(18,48): _hl(s,15,30,y,M); _px(s,15,y,O); _px(s,30,y,O)
    _vl(s,22,19,47,D); _vl(s,23,19,47,D)
    for y in range(48,51): _hl(s,15,30,y,D)
    _fr(s,21,48,6,3,G)
    _vl(s,37,8,48,O); _vl(s,38,8,48,M); _hl(s,34,42,24,G)  # broadsword
    for y in range(20,48): _hl(s,31,36,y,M); _px(s,31,y,O); _px(s,36,y,O)
    for y in range(51,77): _hl(s,17,22,y,M); _px(s,17,y,O); _px(s,22,y,O)
    for y in range(51,77): _hl(s,25,30,y,M); _px(s,25,y,O); _px(s,30,y,O)
    _hl(s,16,23,77,O); _hl(s,24,31,77,O)

# ─────────────────────────────────────────────────────────────────────────────
#  ENEMY SPRITES
# ─────────────────────────────────────────────────────────────────────────────

def _enemy_goblin_warrior(s):
    O=(140,190,100); M=(70,110,45); D=(35,60,20); E=(255,220,40); T=(210,210,210); W=(140,130,120)
    for y,x1,x2 in [(8,19,28),(9,18,29),(10,17,30),(11,17,30),(12,18,29)]: _hl(s,x1,x2,y,M)
    _hl(s,19,28,8,O); _hl(s,18,29,12,O); _vl(s,17,9,12,O); _vl(s,30,9,12,O)
    for i in range(4): _px(s,16-i,8+i,O); _px(s,31+i,8+i,O)
    _fr(s,19,10,3,3,E); _fr(s,25,10,3,3,E)
    _px(s,20,11,D); _px(s,26,11,D)
    for y in range(13,17): _hl(s,19,28,y,M); _px(s,19,y,O); _px(s,28,y,O)
    _hl(s,19,28,16,D)
    for tx in [20,22,24,26]: _px(s,tx,16,T); _px(s,tx,17,T)
    for y in range(17,20): _hl(s,22,26,y,M)
    for y in range(20,42):
        x1=19-(y-20)//6; x2=28+(y-20)//6
        _hl(s,x1,x2,y,M); _px(s,x1,y,O); _px(s,x2,y,O)
    for y in range(20,24): _hl(s,18,30,y,D)
    for y in range(30,38): _hl(s,19,28,y,D)
    for y in range(22,55): _px(s,14,y,M); _px(s,15,y,M); _px(s,14,y,O)
    for y in range(45,68): _px(s,13,y,W); _px(s,12,y,W); _px(s,13,y,O)
    _px(s,12,68,O); _px(s,13,68,O)
    for y in range(20,48): _px(s,32,y,M); _px(s,33,y,M); _px(s,33,y,O)
    for y in range(5,24): _hl(s,33,36,y,W); _px(s,33,y,O); _px(s,36,y,O)
    _hl(s,33,36,5,O)
    for y in range(42,70):
        bow=(y-42)//4
        _hl(s,18-bow,21-bow,y,M); _px(s,18-bow,y,O); _px(s,21-bow,y,O)
        _hl(s,26+bow,29+bow,y,M); _px(s,26+bow,y,O); _px(s,29+bow,y,O)
    for y in range(70,76): _hl(s,11,22,y,D); _hl(s,25,36,y,D)
    _hl(s,10,23,75,O); _hl(s,24,37,75,O)

def _enemy_goblin_archer(s):
    O=(140,190,100); M=(70,110,45); D=(35,60,20); E=(255,220,40); T=(210,210,210)
    BR=(130,90,40)
    # same goblin body
    for y,x1,x2 in [(8,19,28),(9,18,29),(10,17,30),(11,17,30),(12,18,29)]: _hl(s,x1,x2,y,M)
    _hl(s,19,28,8,O); _hl(s,18,29,12,O); _vl(s,17,9,12,O); _vl(s,30,9,12,O)
    for i in range(4): _px(s,16-i,8+i,O); _px(s,31+i,8+i,O)
    _fr(s,19,10,3,3,E); _fr(s,25,10,3,3,E); _px(s,20,11,D); _px(s,26,11,D)
    for y in range(13,17): _hl(s,19,28,y,M); _px(s,19,y,O); _px(s,28,y,O)
    _hl(s,19,28,16,D); _hl(s,21,26,17,T)
    for y in range(17,20): _hl(s,22,26,y,M)
    for y in range(20,42): _hl(s,19,28,y,M); _px(s,19,y,O); _px(s,28,y,O)
    for y in range(20,24): _hl(s,19,28,y,D)
    # bow — held out front, drawing back
    _vl(s,12,15,48,BR)  # bow stave
    _px(s,12,14,O); _px(s,12,49,O)
    for i in range(18): _px(s,12+i//4,15+i,O)  # bow curve
    # arrow nocked
    _hl(s,12,32,30,E)   # arrow shaft
    _px(s,32,30,O); _px(s,33,29,O); _px(s,33,31,O)  # arrowhead
    _px(s,12,28,M); _px(s,12,29,M); _px(s,12,32,M)  # fletching
    # draw arm
    for y in range(26,38): _hl(s,28,35,y,M); _px(s,28,y,O); _px(s,35,y,O)
    # legs
    for y in range(42,70):
        bow=(y-42)//4; _hl(s,18-bow,21-bow,y,M); _px(s,18-bow,y,O); _px(s,21-bow,y,O)
        _hl(s,26+bow,29+bow,y,M); _px(s,26+bow,y,O); _px(s,29+bow,y,O)
    for y in range(70,76): _hl(s,11,22,y,D); _hl(s,25,36,y,D)
    _hl(s,10,23,75,O); _hl(s,24,37,75,O)

def _enemy_goblin_brute(s):
    O=(120,175,80); M=(60,100,35); D=(28,55,14); E=(255,200,30); W=(160,140,110)
    # massive head
    for y in range(5,17):
        hw=7-abs(y-10)//2; _hl(s,23-hw,24+hw,y,M); _px(s,23-hw,y,O); _px(s,24+hw,y,O)
    _hl(s,21,26,5,O)
    for i in range(5): _px(s,16-i,6+i,O); _px(s,31+i,6+i,O)
    _fr(s,18,9,4,4,E); _fr(s,26,9,4,4,E)
    _px(s,19,11,D); _px(s,27,11,D)
    # prominent tusks
    _px(s,19,16,W); _px(s,19,17,W); _px(s,20,18,W)
    _px(s,28,16,W); _px(s,28,17,W); _px(s,27,18,W)
    _hl(s,19,28,15,D); _hl(s,19,28,16,D)
    # massive body
    for y in range(17,52):
        hw=7+(y-17)//5; _hl(s,23-hw,24+hw,y,M); _px(s,23-hw,y,O); _px(s,24+hw,y,O)
    for y in range(17,30): _hl(s,19,28,y,D)  # chest shadow
    # giant club
    _vl(s,36,10,60,W); _vl(s,37,10,60,D)
    _fr(s,33,4,9,10,W); _or(s,33,4,9,10,O)  # club head
    # huge arms
    for y in range(19,54): _hl(s,11,16,y,M); _px(s,11,y,O)
    for y in range(19,54): _hl(s,31,37,y,M); _px(s,37,y,O)
    # bowed legs
    for y in range(52,72):
        bow=(y-52)//3; _hl(s,16-bow,20-bow,y,M); _px(s,16-bow,y,O); _px(s,20-bow,y,O)
        _hl(s,27+bow,31+bow,y,M); _px(s,27+bow,y,O); _px(s,31+bow,y,O)
    for y in range(72,79): _hl(s,10,21,y,D); _hl(s,26,37,y,D)
    _hl(s,9,22,78,O); _hl(s,25,38,78,O)

def _enemy_goblin_shaman(s):
    O=(140,190,100); M=(70,110,45); D=(35,60,20); E=(200,80,200); G=(160,220,255)
    # bone headdress
    for i in range(3): _hl(s,19+i*3,19+i*3+2,4,O)
    _hl(s,18,29,8,O); _hl(s,17,30,7,M)
    for y,x1,x2 in [(8,19,28),(9,18,29),(10,17,30),(11,17,30),(12,18,29)]: _hl(s,x1,x2,y,M)
    _hl(s,19,28,8,O); _hl(s,18,29,12,O); _vl(s,17,9,12,O); _vl(s,30,9,12,O)
    for i in range(4): _px(s,16-i,8+i,O); _px(s,31+i,8+i,O)
    _fr(s,19,10,3,3,E); _fr(s,25,10,3,3,E)  # purple magic eyes
    for y in range(13,17): _hl(s,19,28,y,M); _px(s,19,y,O); _px(s,28,y,O)
    _hl(s,19,28,16,D)
    for y in range(17,20): _hl(s,22,26,y,M)
    for y in range(20,42): _hl(s,19,28,y,M); _px(s,19,y,O); _px(s,28,y,O)
    # bone staff with skull
    _vl(s,14,8,62,D); _vl(s,13,8,62,M)
    _fr(s,11,4,6,6,O); _fr(s,12,5,4,4,D)
    _px(s,12,6,E); _px(s,13,6,E)  # skull eyes
    _hl(s,12,15,9,O)   # jaw
    # magic effects floating around
    for ex,ey in [(9,20),(8,28),(10,36),(16,14)]: _px(s,ex,ey,E); _px(s,ex+1,ey,G)
    # arms
    for y in range(22,55): _px(s,32,y,M); _px(s,33,y,M); _px(s,33,y,O)
    for y in range(42,70):
        bow=(y-42)//4; _hl(s,18-bow,21-bow,y,M); _px(s,18-bow,y,O); _px(s,21-bow,y,O)
        _hl(s,26+bow,29+bow,y,M); _px(s,26+bow,y,O); _px(s,29+bow,y,O)
    for y in range(70,76): _hl(s,11,22,y,D); _hl(s,25,36,y,D)
    _hl(s,10,23,75,O); _hl(s,24,37,75,O)

def _enemy_goblin_king(s):
    O=(200,60,40); M=(140,35,20); D=(80,18,10); G=(220,185,60); E=(255,220,40); W=(160,140,100)
    CR=(220,185,60)
    # crown
    for i in range(5): _px(s,17+i*3,3,CR); _px(s,17+i*3,4,CR)
    _hl(s,16,31,5,CR); _hl(s,16,31,6,CR)
    # large head
    for y in range(6,18):
        hw=8-abs(y-11)//2; _hl(s,23-hw,24+hw,y,M); _px(s,23-hw,y,O); _px(s,24+hw,y,O)
    for i in range(5): _px(s,14-i,7+i,O); _px(s,33+i,7+i,O)
    _fr(s,17,9,5,5,E); _fr(s,26,9,5,5,E)
    _px(s,19,11,D); _px(s,28,11,D)
    _px(s,18,15,W); _px(s,19,16,W); _px(s,19,17,W)  # tusks
    _px(s,29,15,W); _px(s,28,16,W); _px(s,28,17,W)
    _hl(s,18,29,17,D)
    for y in range(18,21): _hl(s,21,26,y,M)
    # royal patchwork armor
    for y in range(21,52):
        hw=8+(y-21)//6; _hl(s,23-hw,24+hw,y,M); _px(s,23-hw,y,O); _px(s,24+hw,y,O)
    for y in range(21,35): _hl(s,19,28,y,D)
    _hl(s,18,29,35,G); _hl(s,18,29,36,G)  # royal sash
    _fr(s,21,35,6,3,G); _or(s,21,35,6,3,O)
    # throne sword — massive
    _vl(s,37,4,52,W); _vl(s,38,4,52,D); _vl(s,39,4,52,W)
    _fr(s,34,4,9,4,W); _or(s,34,4,9,4,O)
    _hl(s,33,43,24,G); _hl(s,33,43,25,G)
    # heavy arms
    for y in range(22,56): _hl(s,10,16,y,M); _px(s,10,y,O)
    for y in range(22,56): _hl(s,30,37,y,M); _px(s,37,y,O)
    for y in range(52,72):
        bow=(y-52)//3; _hl(s,16-bow,21-bow,y,M); _px(s,16-bow,y,O); _px(s,21-bow,y,O)
        _hl(s,26+bow,31+bow,y,M); _px(s,26+bow,y,O); _px(s,31+bow,y,O)
    for y in range(72,79): _hl(s,9,22,y,D); _hl(s,25,38,y,D)
    _hl(s,8,23,78,O); _hl(s,24,39,78,O)

def _enemy_orc_warrior(s):
    O=(100,145,68); M=(58,95,36); D=(30,56,16); E=(255,235,50); W=(160,140,100); G=(170,140,60)
    for y in range(6,17):
        hw=6-abs(y-10)//2; _hl(s,23-hw,24+hw,y,M); _px(s,23-hw,y,O); _px(s,24+hw,y,O)
    for i in range(3): _px(s,17-i,7+i,O); _px(s,30+i,7+i,O)
    _fr(s,18,9,4,4,E); _fr(s,25,9,4,4,E)
    _px(s,19,11,D); _px(s,26,11,D)
    _px(s,19,15,W); _px(s,19,16,W)  # tusk
    _px(s,28,15,W); _px(s,28,16,W)
    _hl(s,19,28,15,D); _hl(s,20,27,16,D)
    for y in range(16,19): _hl(s,21,26,y,M)
    # iron-banded armor
    for y in range(19,48):
        hw=6+(y-19)//5; _hl(s,23-hw,24+hw,y,M); _px(s,23-hw,y,O); _px(s,24+hw,y,O)
    for by in range(22,45,5): _hl(s,18,29,by,D)  # armor bands
    _hl(s,18,29,38,G)  # belt
    # axe
    _vl(s,36,8,50,W); _vl(s,37,8,50,D)
    _fr(s,33,6,8,10,D); _or(s,33,6,8,10,O)
    _px(s,33,6,O); _px(s,40,6,O); _px(s,41,12,O)
    # shield
    for y in range(24,50): _hl(s,8,16,y,D); _px(s,8,y,O); _px(s,16,y,O)
    _hl(s,8,16,24,O); _hl(s,9,15,49,O)
    _fr(s,10,35,4,4,G); _or(s,10,35,4,4,O)
    # arms + legs
    for y in range(20,48): _hl(s,31,37,y,M); _px(s,31,y,O); _px(s,37,y,O)
    for y in range(48,72): _hl(s,19,23,y,M); _px(s,19,y,O); _px(s,23,y,O)
    for y in range(48,72): _hl(s,25,29,y,M); _px(s,25,y,O); _px(s,29,y,O)
    for y in range(72,79): _hl(s,17,24,y,D); _hl(s,24,31,y,D)
    _hl(s,16,25,78,O); _hl(s,23,32,78,O)

def _enemy_orc_chieftain(s):
    O=(80,125,50); M=(44,78,26); D=(22,44,10); E=(255,210,30); W=(170,145,90); G=(210,175,55)
    CR=(210,175,55)
    # skull-adorned helm
    _hl(s,17,30,5,D); _hl(s,16,31,6,M); _hl(s,15,32,7,M); _hl(s,15,32,8,M)
    _vl(s,15,5,15,O); _vl(s,32,5,15,O); _hl(s,16,31,15,O)
    _hl(s,17,30,11,D); _hl(s,17,30,12,D); _hl(s,17,30,13,D)
    _px(s,20,12,E); _px(s,21,12,E); _px(s,26,12,E); _px(s,27,12,E)
    # skull trophies on shoulders
    for sx,sy in [(11,16),(34,16)]:
        _fr(s,sx,sy,4,4,D); _or(s,sx,sy,4,4,O)
        _px(s,sx+1,sy+1,E); _px(s,sx+2,sy+1,E)
    _hl(s,16,31,16,G)
    # massive armored body
    for y in range(16,55):
        hw=8+(y-16)//6; _hl(s,23-hw,24+hw,y,M); _px(s,23-hw,y,O); _px(s,24+hw,y,O)
    for by in range(20,52,6): _hl(s,16,31,by,D)
    _hl(s,16,31,40,G); _hl(s,16,31,41,G)
    _fr(s,21,40,6,4,G); _or(s,21,40,6,4,O)
    # great cleaver
    _vl(s,37,5,55,W); _vl(s,38,5,55,D); _vl(s,39,5,55,W)
    _fr(s,33,3,10,14,W); _or(s,33,3,10,14,O)
    for gx in range(34,43): _px(s,gx,3,O); _px(s,gx,17,O)
    # huge arms
    for y in range(17,56): _hl(s,10,16,y,M); _px(s,10,y,O)
    for y in range(17,56): _hl(s,31,38,y,M); _px(s,38,y,O)
    for y in range(55,76): _hl(s,17,23,y,M); _px(s,17,y,O); _px(s,23,y,O)
    for y in range(55,76): _hl(s,25,31,y,M); _px(s,25,y,O); _px(s,31,y,O)
    for y in range(76,80): _hl(s,15,24,y,D); _hl(s,23,32,y,D)
    _hl(s,14,25,79,O); _hl(s,22,33,79,O)

def _enemy_skeleton(s):
    B=(225,220,200); M=(160,155,130); D=(90,85,65); E=(80,160,255)
    for y,x1,x2 in [(5,19,28),(6,17,30),(7,16,31),(8,16,31),(9,16,31),(10,16,31),(11,17,30)]: _hl(s,x1,x2,y,M)
    _hl(s,20,27,5,B); _hl(s,18,29,6,B); _px(s,16,7,B); _px(s,31,7,B)
    _fr(s,18,8,4,4,D); _fr(s,25,8,4,4,D)
    _px(s,19,9,E); _px(s,20,9,E); _px(s,19,10,E)
    _px(s,26,9,E); _px(s,27,9,E); _px(s,26,10,E)
    _px(s,23,11,D); _px(s,24,11,D); _px(s,23,12,D); _px(s,24,12,D)
    _hl(s,18,29,12,M)
    for tx in range(19,29,2): _vl(s,tx,13,15,B); _vl(s,tx+1,13,15,D)
    _hl(s,18,29,15,D)
    for y in range(16,20): _px(s,23,y,M); _px(s,24,y,M); _px(s,23,y,B)
    _hl(s,13,22,20,B); _hl(s,24,35,20,B); _hl(s,12,23,21,M); _hl(s,23,36,21,M)
    for ry,x1,x2 in [(22,14,22),(24,13,22),(26,13,21),(28,14,22),(22,24,33),(24,24,34),(26,24,34),(28,24,33)]:
        _hl(s,x1,x2,ry,M); _hl(s,x1,x2,ry+1,M); _px(s,x1,ry,B); _px(s,x2,ry,B)
    _vl(s,23,20,32,M); _vl(s,24,20,32,D)
    for sy in range(20,38,2): _px(s,23,sy,B); _px(s,24,sy,B)
    _hl(s,15,32,38,B); _hl(s,14,33,39,M); _hl(s,16,31,40,M)
    for y in range(21,52): _px(s,12,y,M); _px(s,13,y,M); _px(s,12,y,B)
    _vl(s,11,5,52,B); _vl(s,10,5,52,M); _px(s,10,5,B); _px(s,11,5,B)
    _hl(s,8,14,28,M); _hl(s,8,14,29,B)
    for y in range(21,46): _px(s,34,y,M); _px(s,35,y,M); _px(s,35,y,B)
    for fx in range(33,40): _vl(s,fx,46,52,M); _px(s,fx,46,B)
    for y in range(41,57): _hl(s,17,20,y,M); _px(s,17,y,B); _hl(s,27,30,y,M); _px(s,30,y,B)
    _hl(s,17,20,57,B); _hl(s,27,30,57,B)
    for y in range(59,75): _hl(s,18,20,y,M); _px(s,18,y,B); _hl(s,27,29,y,M); _px(s,29,y,B)
    for fx in range(15,23): _vl(s,fx,75,78,M if fx%2==0 else D)
    for fx in range(25,33): _vl(s,fx,75,78,M if fx%2==0 else D)
    _hl(s,15,22,75,B); _hl(s,25,32,75,B)

def _enemy_zombie(s):
    O=(100,140,80); M=(55,88,42); D=(25,48,16); SK=(145,168,130); DR=(90,110,75); R=(170,40,40)
    # bloated decomposed head
    for y in range(5,17):
        hw=7-abs(y-10)//2; _hl(s,23-hw,24+hw,y,SK)
        _px(s,23-hw,y,O); _px(s,24+hw,y,O)
    # milky dead eyes
    _fr(s,19,8,4,4,DR); _fr(s,25,8,4,4,DR)
    _px(s,20,10,SK); _px(s,26,10,SK)  # glazed
    # gaping rotten mouth
    _hl(s,19,28,14,R); _hl(s,19,28,15,D)
    for tx in range(20,28,3): _px(s,tx,14,DR)  # missing teeth
    # torn, decayed flesh
    for y in range(16,19): _hl(s,21,26,y,SK)
    for y in range(19,52):
        hw=6+(y-19)//6; _hl(s,23-hw,24+hw,y,DR)
        _px(s,23-hw,y,O); _px(s,24+hw,y,O)
    # wound marks
    for wx,wy in [(21,24),(27,30),(19,38),(26,42)]: _px(s,wx,wy,R); _px(s,wx+1,wy,R)
    _hl(s,20,27,32,D); _hl(s,20,27,33,D)
    # shambling arms — one reaching forward
    for y in range(20,56): _hl(s,11,16,y,DR); _px(s,11,y,O)
    for y in range(18,50): _hl(s,31,38,y,DR); _px(s,38,y,O)  # outstretched
    for fx in range(32,40): _vl(s,fx,50,56,DR); _px(s,fx,56,O)   # reaching fingers
    # shambling legs
    for y in range(52,75): _hl(s,18,23,y,DR); _px(s,18,y,O); _px(s,23,y,O)
    for y in range(52,75): _hl(s,25,30,y,DR); _px(s,25,y,O); _px(s,30,y,O)
    for y in range(75,80): _hl(s,16,24,y,D); _hl(s,24,32,y,D)
    _hl(s,15,25,79,O); _hl(s,23,33,79,O)

def _enemy_giant_spider(s):
    O=(80,50,80); M=(130,80,130); D=(55,28,55); E=(220,50,50)
    # body — two oval segments
    for y in range(32,50):  # abdomen (rear)
        hw=8-abs(y-40)//2; _hl(s,29,29+hw,y,M); _px(s,29,y,O); _px(s,29+hw,y,O)
    for y in range(26,38):  # cephalothorax (front)
        hw=6-abs(y-31)//2; _hl(s,19,19+hw,y,M); _px(s,19,y,O); _px(s,19+hw,y,O)
    _hl(s,25,28,34,D)  # waist
    # 8 eyes
    for ex,ey in [(20,27),(22,27),(24,27),(26,27),(20,29),(22,29),(24,29),(26,29)]:
        _px(s,ex,ey,E)
    # 8 legs — 4 pairs, fanning out
    legs = [
        (22,32,8,20),(22,32,12,22),(22,32,14,24),(22,32,16,28),   # left legs
        (26,32,38,20),(26,32,36,22),(26,32,34,24),(26,32,32,28),  # right legs
    ]
    for sx,sy,ex,ey in legs:
        dx=ex-sx; dy=ey-sy; steps=max(abs(dx),abs(dy))
        for i in range(steps+1):
            _px(s,round(sx+i*dx/max(1,steps)),round(sy+i*dy/max(1,steps)),M if i>0 else O)
        _px(s,ex,ey,O)  # paw tip
    # fangs
    _px(s,21,37,E); _px(s,22,38,E); _px(s,25,37,E); _px(s,24,38,E)

def _enemy_troll(s):
    O=(80,120,58); M=(44,78,28); D=(22,44,12); E=(220,190,40); W=(155,130,90); SK=(155,190,130)
    # massive craggy head
    for y in range(4,17):
        hw=8-abs(y-9)//2; _hl(s,23-hw,24+hw,y,M); _px(s,23-hw,y,O); _px(s,24+hw,y,O)
    _px(s,14,5,O); _px(s,33,5,O)  # rough horn nubs
    _fr(s,17,9,5,4,D); _fr(s,26,9,5,4,D)  # deep-set eyes
    _px(s,18,10,E); _px(s,19,10,E); _px(s,27,10,E); _px(s,28,10,E)
    _hl(s,19,28,15,D); _hl(s,20,27,16,D); _px(s,19,16,SK); _px(s,27,16,SK)  # jaw
    # enormous hulking body
    for y in range(16,60):
        hw=9+(y-16)//4; _hl(s,23-hw,24+hw,y,M); _px(s,23-hw,y,O); _px(s,24+hw,y,O)
    for y in range(16,35): _hl(s,20,27,y,D)  # shadow under neck
    # skin texture
    for tx,ty in [(15,28),(34,25),(12,40),(36,38),(18,50),(30,48)]: _px(s,tx,ty,D); _px(s,tx+1,ty,D)
    # club raised overhead
    _vl(s,36,2,28,W); _vl(s,37,2,28,D)
    _fr(s,33,2,8,10,W); _or(s,33,2,8,10,O)
    # massive arms
    for y in range(18,54): _hl(s,9,16,y,M); _px(s,9,y,O)
    for y in range(16,54): _hl(s,31,38,y,M); _px(s,38,y,O)
    # thick legs
    for y in range(60,76): _hl(s,16,23,y,M); _px(s,16,y,O); _px(s,23,y,O)
    for y in range(60,76): _hl(s,25,32,y,M); _px(s,25,y,O); _px(s,32,y,O)
    for y in range(76,80): _hl(s,14,24,y,D); _hl(s,24,34,y,D)
    _hl(s,13,25,79,O); _hl(s,23,35,79,O)

def _enemy_dark_mage(s):
    O=(160,80,200); M=(95,40,145); D=(48,15,82); G=(200,160,255); E=(255,80,80); Y=(240,220,80)
    # sinister hood + cowl
    for y in range(3,16):
        hw=4+y//4; _hl(s,23-hw,24+hw,y,D)
    _vl(s,16,3,15,O); _vl(s,31,3,15,O); _hl(s,16,31,3,O); _hl(s,16,31,15,O)
    # glowing eyes in shadow
    _px(s,20,9,E); _px(s,21,9,E); _px(s,25,9,E); _px(s,26,9,E)
    # flowing dark robes
    for y in range(15,64):
        hw=5+y//7; _hl(s,23-hw,24+hw,y,M); _px(s,23-hw,y,O); _px(s,24+hw,y,O)
    # arcane glyphs on robe
    for gx,gy in [(19,28),(26,32),(21,44),(28,40)]: _px(s,gx,gy,G); _px(s,gx+1,gy,G)
    _hl(s,18,29,40,D)
    # staff of power — right
    _vl(s,36,4,62,D); _vl(s,37,4,62,M)
    _fr(s,33,2,7,5,E); _or(s,33,2,7,5,O)  # blood crystal
    # spell casting left hand
    for ex,ey in [(14,32),(13,33),(15,33),(14,34),(13,31),(15,31)]: _px(s,ex,ey,G)
    _fr(s,11,34,5,5,D); _or(s,11,34,5,5,G)
    # hem
    for y in range(64,70): _hl(s,19,28,y,D); _px(s,19,y,O); _px(s,28,y,O)
    _hl(s,20,24,73,D); _hl(s,23,27,73,D); _hl(s,19,25,76,O); _hl(s,22,28,76,O)

def _enemy_vampire(s):
    O=(180,90,160); M=(110,45,110); D=(58,18,68); W=(230,220,210); E=(200,50,50); G=(200,180,120)
    # noble face — pale, sharp
    for y in range(6,16):
        hw=5-abs(y-10)//3; _hl(s,23-hw,24+hw,y,W)
        _px(s,23-hw,y,O); _px(s,24+hw,y,O)
    _hl(s,20,27,6,D); _hl(s,18,29,15,O)
    # piercing red eyes
    _px(s,20,9,E); _px(s,21,9,E); _px(s,25,9,E); _px(s,26,9,E)
    _px(s,20,10,D); _px(s,25,10,D)
    # bared fangs
    _hl(s,19,28,14,D)
    _px(s,21,14,W); _px(s,22,15,W)  # left fang
    _px(s,26,14,W); _px(s,25,15,W)  # right fang
    # cape / evening dress
    for y in range(16,64):
        hw=6+y//7; _hl(s,23-hw,24+hw,y,M); _px(s,23-hw,y,O); _px(s,24+hw,y,O)
    # cape lining (inner lighter strip)
    for y in range(20,60):
        _px(s,22,y,D); _px(s,25,y,D)
    # white cravat
    _fr(s,21,18,6,4,W); _or(s,21,18,6,4,D)
    # elegant hands — clawed
    for y in range(20,46): _hl(s,12,16,y,M); _px(s,12,y,O)
    for y in range(20,46): _hl(s,31,35,y,M); _px(s,35,y,O)
    for i in range(3): _px(s,11-i,46+i,O); _px(s,36+i,46+i,O)
    # hem / mist at feet
    for y in range(64,70): _hl(s,17,30,y,D); _px(s,17,y,O); _px(s,30,y,O)
    for y in range(70,76):
        for x in range(16,32):
            if (x+y)%3 == 0: _px(s,x,y,D)
    _hl(s,18,29,76,O)

def _enemy_dragon(s):
    O=(185,80,50); M=(130,45,25); D=(70,20,10); E=(255,220,30); WH=(230,215,185); SC=(165,60,35)
    # horned head
    _px(s,20,3,O); _px(s,19,4,O); _px(s,18,5,O)   # left horn
    _px(s,27,3,O); _px(s,28,4,O); _px(s,29,5,O)   # right horn
    for y in range(5,18):
        hw=7-abs(y-11)//2; _hl(s,23-hw,24+hw,y,M); _px(s,23-hw,y,O); _px(s,24+hw,y,O)
    _hl(s,18,29,5,O)
    # slitted eyes
    _px(s,19,9,E); _px(s,20,9,E); _px(s,25,9,E); _px(s,26,9,E)
    _px(s,20,10,D); _px(s,25,10,D)
    # teeth row
    _hl(s,18,29,16,D)
    for tx in range(19,29,2): _px(s,tx,16,WH); _px(s,tx,17,WH)
    # neck
    for y in range(17,24): _hl(s,20,27,y,M); _px(s,20,y,O); _px(s,27,y,O)
    for y in range(17,24,2): _hl(s,21,26,y,SC)  # scale ridge
    # body — barrel chest
    for y in range(24,55):
        hw=8-(y-24)//10; _hl(s,23-hw,24+hw,y,M); _px(s,23-hw,y,O); _px(s,24+hw,y,O)
    # scale pattern on body
    for sy in range(26,52,3):
        for sx in range(16,32,4): _px(s,sx,sy,SC); _px(s,sx+1,sy,SC)
    # wings (spread behind)
    for i in range(10):
        _px(s,14-i,20+i*2,D); _px(s,33+i,20+i*2,D)
        _px(s,13-i,21+i*2,M); _px(s,34+i,21+i*2,M)
    for i in range(8): _hl(s,14-i,15-i,20+i*3,D)  # wing membrane
    for i in range(8): _hl(s,33+i,34+i,20+i*3,D)
    # clawed feet
    for y in range(55,68): _hl(s,17,22,y,M); _px(s,17,y,O); _px(s,22,y,O)
    for y in range(55,68): _hl(s,25,30,y,M); _px(s,25,y,O); _px(s,30,y,O)
    for i in range(3): _px(s,15+i*2,68,O); _px(s,23+i*2,68,O)
    # tail
    for i,ty in enumerate(range(50,70)):
        tx=32+i
        if tx < W: _px(s,tx,ty,M)
        if tx+1 < W: _px(s,tx+1,ty,D)

def _enemy_abomination(s):
    O=(130,160,80); M=(75,110,40); D=(36,62,16); E=(220,80,200); R=(180,40,40)
    # amorphous mass — irregular blob
    for y in range(6,72):
        import math
        phase = y * 0.4
        hw = int(10 + 4*math.sin(phase) + 2*math.cos(phase*1.7))
        cx = 23 + int(2*math.sin(phase*0.8))
        _hl(s,cx-hw,cx+hw,y,M); _px(s,cx-hw,y,O); _px(s,cx+hw,y,O)
    # multiple eyes scattered throughout
    for ex,ey in [(18,12),(28,15),(15,25),(33,22),(20,34),(30,38),(22,50),(26,44)]:
        _fr(s,ex,ey,3,3,R); _or(s,ex,ey,3,3,O); _px(s,ex+1,ey+1,E)
    # mouths / orifices
    for mx,my in [(19,48),(27,52)]:
        _hl(s,mx,mx+5,my,D); _hl(s,mx,mx+5,my+3,D)
        _vl(s,mx,my,my+3,D); _vl(s,mx+5,my,my+3,D)
        for tx in range(mx+1,mx+5): _px(s,tx,my+1,O)  # teeth
    # tentacles
    for i in range(3):
        for j in range(8): _px(s,8+i*4,40+j*4,M if j%2==0 else O)
        for j in range(6): _px(s,36+i*3,35+j*5,M if j%2==0 else O)

def _enemy_boss_valdris(s):
    O=(200,160,255); M=(130,80,220); D=(65,30,140); G=(220,185,60); E=(255,80,80); W=(230,220,210)
    BL=(140,180,255)
    # imposing helm with dark crown
    for i in range(6): _px(s,19+i*2,2,G); _vl(s,19+i*2,2,5,G)
    _hl(s,16,31,5,O); _hl(s,15,32,6,M); _hl(s,14,33,7,M); _hl(s,14,33,8,M)
    _hl(s,14,33,9,M); _hl(s,14,33,10,M)
    _vl(s,14,6,16,O); _vl(s,33,6,16,O)
    for y in range(12,15): _hl(s,15,32,y,D)
    _px(s,19,13,E); _px(s,20,13,E); _px(s,26,13,E); _px(s,27,13,E)
    _hl(s,15,32,15,M); _hl(s,15,32,16,O); _hl(s,15,32,17,G)
    # massive armored shoulders
    _hl(s,8,16,18,O); _hl(s,31,39,18,O)
    for y in range(19,28): _hl(s,8,16,y,M); _hl(s,31,39,y,M)
    _hl(s,8,16,27,O); _hl(s,31,39,27,O)
    for gx in range(9,16,2): _px(s,gx,20,G)
    for gx in range(32,39,2): _px(s,gx,20,G)
    # ornate breastplate
    for y in range(18,52): _hl(s,15,32,y,M); _px(s,15,y,O); _px(s,32,y,O); _px(s,16,y,BL)
    _vl(s,23,19,50,D); _vl(s,24,19,50,D)
    _fr(s,19,28,10,10,D); _or(s,19,28,10,10,O)  # emblem
    _vl(s,23,29,37,E); _hl(s,20,26,33,E)         # emblem glyph
    _hl(s,15,32,52,G); _hl(s,15,32,53,G)
    _fr(s,21,52,6,4,G); _or(s,21,52,6,4,O)
    # void sword (right) — massive and crackling
    _vl(s,38,3,52,BL); _vl(s,39,3,52,O); _vl(s,40,3,52,BL)
    _px(s,38,2,BL); _px(s,39,1,O); _px(s,40,2,BL)
    _hl(s,35,45,24,G); _hl(s,35,45,25,G); _hl(s,35,45,26,G)
    for gy in range(3,52,4): _px(s,37,gy,BL); _px(s,41,gy,BL)
    # dark shield (left)
    for y in range(22,56): _hl(s,5,14,y,D); _px(s,5,y,O); _px(s,14,y,O)
    _hl(s,5,14,22,O); _hl(s,6,13,55,O)
    _fr(s,7,36,6,6,E); _or(s,7,36,6,6,O)
    # arms
    for y in range(26,52): _hl(s,8,15,y,M); _px(s,8,y,O)
    for y in range(26,52): _hl(s,33,40,y,M); _px(s,40,y,O)
    # legs
    for y in range(53,77): _hl(s,17,22,y,M); _px(s,17,y,O); _px(s,22,y,O)
    for y in range(53,77): _hl(s,25,30,y,M); _px(s,25,y,O); _px(s,30,y,O)
    _hl(s,16,23,77,O); _hl(s,24,31,77,O)

def _enemy_wolf(s):
    O=(170,150,110); F=(90,75,50); D=(50,40,25); B=(215,200,160); E=(220,180,30)
    for y,x1,x2 in [(18,5,16),(19,4,17),(20,3,18),(21,3,18),(22,4,17),(23,5,15)]:
        _hl(s,x1,x2,y,F); _px(s,x1,y,O); _px(s,x2,y,O)
    for i in range(5): _px(s,8+i,13+i,O); _px(s,13-i,13+i,O)
    _hl(s,9,12,13,O)
    for y,x1,x2 in [(21,0,4),(22,0,5)]: _hl(s,x1,x2,y,F); _px(s,x1,y,O); _px(s,x2,y,O)
    _hl(s,1,6,23,O); _px(s,2,23,B); _px(s,2,24,B); _px(s,4,23,B); _px(s,4,24,B)
    _px(s,12,19,E); _px(s,13,19,E); _px(s,12,20,E); _px(s,13,20,D)
    for y in range(19,34): _hl(s,14,42,y,F); _px(s,14,y,O); _px(s,42,y,O)
    _hl(s,5,42,19,O); _hl(s,5,42,20,D)
    _hl(s,14,42,31,B); _hl(s,14,42,32,B); _hl(s,14,42,33,O)
    for y in range(15,21): _hl(s,16,22,y,F); _px(s,16,y,O); _px(s,22,y,O)
    _hl(s,16,22,15,O)
    for lx,ly1,ly2 in [(15,34,52),(20,34,52),(32,34,52),(37,34,52)]:
        for y in range(ly1,ly2): _hl(s,lx,lx+2,y,F); _px(s,lx,y,O); _px(s,lx+2,y,O)
        for y in range(ly2,ly2+4): _hl(s,lx-1,lx+3,y,F); _px(s,lx-1,y,O); _px(s,lx+3,y,O)
        _hl(s,lx-1,lx+3,ly2+3,O)

def _enemy_hound(s):
    O=(160,120,70); F=(105,78,44); D=(62,44,20); B=(220,200,165); E=(210,170,30)
    # stocky dog — wider body, shorter legs, blockier head than wolf
    for y,x1,x2 in [(22,7,18),(23,6,19),(24,5,19),(25,5,19),(26,6,18)]:
        _hl(s,x1,x2,y,F); _px(s,x1,y,O); _px(s,x2,y,O)
    # floppy ears
    _vl(s,6,22,30,D); _vl(s,5,23,29,D)
    _vl(s,19,22,30,D); _vl(s,20,23,29,D)
    for y,x1,x2 in [(23,2,7),(24,1,7)]:
        _hl(s,x1,x2,y,F); _px(s,x1,y,O); _px(s,x2,y,O)
    _hl(s,1,6,26,O); _px(s,2,27,B); _px(s,3,27,B); _px(s,4,27,B)  # jowls
    _px(s,11,23,E); _px(s,12,23,E); _px(s,11,24,E); _px(s,12,24,D)
    # collar
    for y in range(27,30): _hl(s,8,19,y,D); _px(s,8,y,O); _px(s,19,y,O)
    # barrel body — shorter, wider than wolf
    for y in range(27,40): _hl(s,7,40,y,F); _px(s,7,y,O); _px(s,40,y,O)
    _hl(s,7,40,27,O); _hl(s,8,40,28,D)
    _hl(s,8,38,36,B); _hl(s,8,38,37,B); _hl(s,8,38,38,O)
    # shoulder & haunch
    for y in range(27,34): _hl(s,8,16,y,F); _hl(s,34,40,y,F)
    # short thick legs — 4
    for lx,ly1,ly2 in [(9,38,52),(16,38,52),(29,38,52),(36,38,52)]:
        for y in range(ly1,ly2): _hl(s,lx,lx+3,y,F); _px(s,lx,y,O); _px(s,lx+3,y,O)
        for y in range(ly2,ly2+3): _hl(s,lx-1,lx+4,y,D)
        _hl(s,lx-1,lx+4,ly2+2,O)
    # stub tail up
    for i in range(5): _px(s,41+i,30-i,F); _px(s,41+i,31-i,O)

def _enemy_bandit(s):
    O=(155,135,110); M=(95,82,62); D=(52,44,30); BR=(130,95,55); Y=(220,190,60); R=(165,45,40)
    # roughspun hood
    for y in range(5,15): _hl(s,18,29,y,D)
    _vl(s,17,5,15,O); _vl(s,30,5,15,O); _hl(s,17,30,5,O); _hl(s,17,30,15,O)
    for i in range(3): _px(s,17-i,5+i*2,O); _px(s,30+i,5+i*2,O)  # torn edges
    _px(s,20,9,Y); _px(s,21,9,Y); _px(s,25,9,Y); _px(s,26,9,Y)  # eyes
    _hl(s,19,28,13,D)  # face wrap
    # scruffy leather
    for y in range(15,50): _hl(s,18,29,y,M); _px(s,18,y,O); _px(s,29,y,O)
    # bandolier
    _vl(s,20,16,48,BR); _vl(s,27,16,48,BR)
    for by in range(20,46,6): _px(s,18,by,Y); _px(s,29,by,Y)  # buckles
    # sword at hip
    _vl(s,31,28,56,D); _vl(s,32,28,56,M)
    _hl(s,29,34,44,BR)  # grip wrap
    # arms
    for y in range(16,50): _hl(s,12,17,y,M); _px(s,12,y,O)
    for y in range(16,48): _hl(s,30,35,y,M); _px(s,35,y,O)
    # legs
    for y in range(50,76): _hl(s,18,22,y,D); _px(s,18,y,O); _px(s,22,y,O)
    for y in range(50,76): _hl(s,25,29,y,D); _px(s,25,y,O); _px(s,29,y,O)
    _hl(s,17,23,76,O); _hl(s,24,30,76,O)

def _enemy_stone_sentinel(s):
    O=(160,155,145); M=(105,100,92); D=(55,52,46); G=(200,175,60); E=(100,180,255)
    # rectangular stone helm/head — angular
    _fr(s,16,5,16,14,M); _or(s,16,5,16,14,O)
    _hl(s,17,30,5,D); _hl(s,17,30,7,O)  # highlight slab
    # engraved eye slit
    _hl(s,18,29,11,D); _hl(s,18,29,12,D); _hl(s,18,29,13,D)
    _hl(s,20,27,12,E)  # magical glow in slot
    # massive stone shoulders — rectilinear
    _fr(s,10,18,10,10,M); _or(s,10,18,10,10,O)
    _fr(s,28,18,10,10,M); _or(s,28,18,10,10,O)
    _hl(s,10,19,18,D); _hl(s,28,37,18,D)
    # chest slab
    _fr(s,16,19,16,24,M); _or(s,16,19,16,24,O)
    _hl(s,17,30,19,D)
    # carved glyphs
    for gx,gy in [(19,26),(24,28),(20,34),(27,32)]: _fr(s,gx,gy,2,3,G); _or(s,gx,gy,2,3,O)
    # belt stone
    _fr(s,16,43,16,4,D); _or(s,16,43,16,4,O); _fr(s,20,44,8,2,G)
    # arms — thick stone columns
    _fr(s,10,28,6,20,M); _or(s,10,28,6,20,O)
    _fr(s,32,28,6,20,M); _or(s,32,28,6,20,O)
    _hl(s,10,15,28,D); _hl(s,32,37,28,D)
    # fists
    _fr(s,9,48,8,8,M); _or(s,9,48,8,8,O)
    _fr(s,31,48,8,8,M); _or(s,31,48,8,8,O)
    # legs — stone pillars
    _fr(s,18,56,10,20,M); _or(s,18,56,10,20,O)
    _fr(s,20,56,8,20,D)
    _fr(s,30,56,10,20,M); _or(s,30,56,10,20,O)
    _fr(s,32,56,8,20,D)
    _hl(s,18,27,56,D); _hl(s,30,39,56,D)
    for y in range(76,80): _hl(s,17,28,y,D); _hl(s,29,40,y,D)
    _hl(s,16,29,79,O); _hl(s,28,41,79,O)

def _enemy_ash_revenant(s):
    O=(210,185,160); M=(140,110,85); D=(75,55,35); E=(255,120,40); ASH=(180,170,160)
    # burnt skull face
    for y in range(5,16):
        hw=5-abs(y-10)//2; _hl(s,23-hw,24+hw,y,D)
        _px(s,23-hw,y,O); _px(s,24+hw,y,O)
    _hl(s,20,27,5,ASH)
    _fr(s,19,8,4,4,D); _fr(s,25,8,4,4,D)
    _px(s,19,9,E); _px(s,20,9,E); _px(s,25,9,E); _px(s,26,9,E)  # ember eyes
    _hl(s,20,27,13,D); _hl(s,21,26,14,D)
    for tx in range(20,27,2): _px(s,tx,14,ASH)  # charred teeth
    # burned, charred body
    for y in range(15,55):
        hw=5+(y-15)//8; _hl(s,23-hw,24+hw,y,M)
        _px(s,23-hw,y,O); _px(s,24+hw,y,O)
    # ash and char texture
    for ay,ax in [(20,19),(24,27),(30,21),(36,26),(42,20),(46,28)]:
        _px(s,ax,ay,D); _px(s,ax+1,ay,ASH)
    # smouldering embers
    for ex,ey in [(16,28),(32,32),(14,40),(35,44)]:
        _px(s,ex,ey,E); _px(s,ex+1,ey,E)
    # arms — skeletal beneath charred skin
    for y in range(17,48): _px(s,13,y,M); _px(s,14,y,D); _px(s,13,y,O)
    for y in range(17,48): _px(s,33,y,M); _px(s,34,y,D); _px(s,34,y,O)
    # trailing ash cloak hem
    for y in range(55,70):
        for x in range(16,32):
            if (x+y)%3 == 0: _px(s,x,y,ASH)
    _hl(s,19,28,70,O)
    for y in range(70,76): _hl(s,19,23,y,D); _hl(s,24,28,y,D)
    _hl(s,18,24,76,O); _hl(s,23,29,76,O)

def _enemy_wraith(s):
    O=(80,90,160); M=(45,55,120); D=(20,25,75); E=(130,160,255); G=(180,200,255)
    # ethereal form — no solid body
    # drifting hood-shape
    for y in range(4,14):
        hw=4+y//4; _hl(s,23-hw,24+hw,y,D)
    _vl(s,17,4,13,O); _vl(s,30,4,13,O)
    # hollow void face
    _fr(s,19,7,4,5,D); _fr(s,25,7,4,5,D)
    _px(s,20,8,E); _px(s,21,8,E)   # haunting eyes
    _px(s,26,8,E); _px(s,27,8,E)
    _px(s,20,10,G); _px(s,26,10,G)  # pupil glow
    # vaporous body — tapering downward
    for y in range(13,66):
        import math
        hw = int(7 + 3*math.sin(y*0.22)) - (y-13)//12
        hw = max(1,hw)
        cx = 23 + int(1.5*math.sin(y*0.18))
        _hl(s,cx-hw,cx+hw,y,M if (y+cx)%3!=0 else D)
        if (y+cx)%3==0: _px(s,cx-hw,y,O); _px(s,cx+hw,y,O)
    # wispy arm tendrils
    for i in range(14): _px(s,14-i//3,24+i*3,M if i%2==0 else D)
    for i in range(12): _px(s,34+i//3,22+i*3,M if i%2==0 else D)
    # fade out at bottom
    for y in range(60,70):
        for x in range(18,30):
            if (x+y)%2 == 0 and (x+y)%4 != 0: _px(s,x,y,D)

def _enemy_kobold(s):
    O=(180,130,80); M=(120,82,40); D=(68,44,18); E=(200,160,50); SC=(160,140,100)
    # small lizard-humanoid
    for y in range(10,19):
        hw=4-abs(y-13)//2; _hl(s,23-hw,24+hw,y,M); _px(s,23-hw,y,O); _px(s,24+hw,y,O)
    # snout
    for y in range(14,18): _hl(s,19,22,y,M); _px(s,19,y,O); _px(s,22,y,O)
    _hl(s,19,22,17,D)  # mouth
    _px(s,19,14,D); _px(s,20,14,D)  # nostrils
    # eyes — bright amber
    _px(s,22,11,E); _px(s,23,11,E)
    _px(s,26,11,E); _px(s,27,11,E)
    # frilled neck
    for i in range(4): _px(s,18-i,18+i,SC); _px(s,29+i,18+i,SC)
    # small scrappy body
    for y in range(20,45): _hl(s,20,27,y,M); _px(s,20,y,O); _px(s,27,y,O)
    # scale pattern
    for sy in range(21,44,3):
        for sx in range(21,27,2): _px(s,sx,sy,SC); _px(s,sx+1,sy,SC)
    # crude iron pick (right)
    _vl(s,31,12,52,D); _vl(s,32,12,52,M)
    _fr(s,30,10,5,5,D); _or(s,30,10,5,5,O)
    # small shield (left)
    for y in range(24,40): _hl(s,14,20,y,D); _px(s,14,y,O); _px(s,20,y,O)
    _hl(s,14,20,24,O); _hl(s,15,19,39,O)
    # arms
    for y in range(21,40): _hl(s,14,19,y,M); _px(s,14,y,O)
    for y in range(21,38): _hl(s,28,33,y,M); _px(s,33,y,O)
    # short bowed legs + long tail
    for y in range(45,64): _hl(s,19,22,y,M); _px(s,19,y,O); _px(s,22,y,O)
    for y in range(45,64): _hl(s,25,28,y,M); _px(s,25,y,O); _px(s,28,y,O)
    for y in range(64,70): _hl(s,18,23,y,D); _hl(s,24,29,y,D)
    _hl(s,17,24,70,O); _hl(s,23,30,70,O)
    for i in range(12): _px(s,28+i,45+i,M); _px(s,29+i,45+i,D)  # tail

def _enemy_ghoul(s):
    O=(120,160,100); M=(68,110,52); D=(32,62,22); SK=(148,185,132); R=(170,40,40)
    # gaunt feral head
    for y in range(6,17):
        hw=5-abs(y-11)//2; _hl(s,23-hw,24+hw,y,SK); _px(s,23-hw,y,O); _px(s,24+hw,y,O)
    # sunken yellow eyes
    _px(s,20,9,( 220,190,50)); _px(s,21,9,(220,190,50))
    _px(s,25,9,(220,190,50)); _px(s,26,9,(220,190,50))
    _px(s,20,10,D); _px(s,25,10,D)
    # gaping maw
    _hl(s,19,28,15,D); _hl(s,19,28,16,R)
    for tx in range(20,28,2): _px(s,tx,15,SK); _px(s,tx,16,SK)  # teeth
    # hunched, clawed body
    for y in range(17,20): _hl(s,21,26,y,SK)
    for y in range(20,52):
        hw=5+(y-20)//8; _hl(s,23-hw,24+hw,y,M); _px(s,23-hw,y,O); _px(s,24+hw,y,O)
    for y in range(20,35): _hl(s,20,27,y,D)  # neck shadow
    # wound marks / decay
    for wx,wy in [(19,34),(27,40),(22,46)]: _px(s,wx,wy,R); _px(s,wx+1,wy,R)
    # long clawed arms — reaching
    for y in range(20,56): _hl(s,11,15,y,M); _px(s,11,y,O)
    for y in range(20,54): _hl(s,32,36,y,M); _px(s,36,y,O)
    for i in range(4): _px(s,9-i,56+i,O); _px(s,10-i,55+i,O)   # claws left
    for i in range(4): _px(s,37+i,54+i,O); _px(s,36+i,53+i,O)  # claws right
    for y in range(52,72): _hl(s,18,22,y,M); _px(s,18,y,O); _px(s,22,y,O)
    for y in range(52,72): _hl(s,25,29,y,M); _px(s,25,y,O); _px(s,29,y,O)
    for y in range(72,78): _hl(s,16,23,y,D); _hl(s,24,31,y,D)
    _hl(s,15,24,77,O); _hl(s,23,32,77,O)

def _enemy_death_knight(s):
    O=(160,160,185); M=(90,90,115); D=(40,40,62); G=(190,165,55); E=(180,50,200); R=(165,35,35)
    # death skull helm
    _hl(s,18,29,5,O); _hl(s,17,30,6,M); _hl(s,16,31,7,M)
    _hl(s,15,32,8,M); _hl(s,15,32,9,M); _hl(s,15,32,10,M)
    _vl(s,15,6,17,O); _vl(s,32,6,17,O)
    # skull face on visor
    _fr(s,18,11,5,5,D); _fr(s,25,11,5,5,D)
    _px(s,19,12,E); _px(s,20,12,E); _px(s,25,12,E); _px(s,26,12,E)
    _hl(s,19,28,15,D); _hl(s,20,27,16,D)
    for tx in range(20,28,2): _px(s,tx,16,O)  # jaw teeth
    _hl(s,15,32,17,G)
    # corrupted plate armor
    _hl(s,10,17,19,O); _hl(s,30,37,19,O)
    for y in range(20,27): _hl(s,10,17,y,M); _hl(s,30,37,y,M)
    _hl(s,10,17,26,O); _hl(s,30,37,26,O)
    for y in range(19,46): _hl(s,16,31,y,M); _px(s,16,y,O); _px(s,31,y,O)
    # dark energy cracks in armor
    for cx2,cy2 in [(19,26),(23,30),(28,28),(25,38),(20,42)]:
        _px(s,cx2,cy2,E); _px(s,cx2+1,cy2,E)
    _vl(s,23,20,44,R); _hl(s,19,27,32,R)  # bloody cross
    _hl(s,16,31,46,G); _fr(s,21,46,6,3,G)
    # death blade (right)
    _vl(s,37,4,46,O); _vl(s,38,4,46,M); _vl(s,39,4,46,D)
    _px(s,37,3,O); _px(s,38,2,E); _px(s,39,3,O)
    for gy in range(4,46,5): _px(s,37,gy,E); _px(s,39,gy,E)  # crackling edge
    _hl(s,34,43,24,G); _hl(s,34,43,25,G)
    # dark shield
    for y in range(24,52): _hl(s,6,14,y,D); _px(s,6,y,O); _px(s,14,y,O)
    _hl(s,6,14,24,O); _hl(s,7,13,51,O)
    _fr(s,8,36,5,5,R); _or(s,8,36,5,5,O)
    for y in range(26,46): _hl(s,10,16,y,M); _px(s,10,y,O)
    for y in range(26,46): _hl(s,31,37,y,M); _px(s,37,y,O)
    for y in range(46,76): _hl(s,18,22,y,M); _px(s,18,y,O); _px(s,22,y,O)
    for y in range(46,76): _hl(s,25,29,y,M); _px(s,25,y,O); _px(s,29,y,O)
    _hl(s,17,23,76,O); _hl(s,24,30,76,O)

def _enemy_cave_bat(s):
    O=(100,80,130); M=(65,48,95); D=(30,20,55); E=(200,60,60)
    # Combined head+body — one wide horizontal oval
    for y in range(24,46):
        hw = 8 - abs(y-34)*5//14
        _hl(s,20,20+hw*2,y,M); _px(s,20,y,O); _px(s,20+hw*2,y,O)
    # Bat ears — wide triangular on sides of head
    for i in range(7):
        _hl(s,18-i,18,24+i-i//2,O); _hl(s,19-i,18,25+i-i//2,M)
    for i in range(7):
        _hl(s,30,30+i,24+i-i//2,O); _hl(s,30,29+i,25+i-i//2,M)
    # Red eyes
    _px(s,22,28,E); _px(s,23,28,E); _px(s,25,28,E); _px(s,26,28,E)
    # Nose + fangs
    _hl(s,23,25,32,D); _px(s,23,35,M); _px(s,25,35,M)
    # Wings — sweep from shoulders up to wide tips
    for i in range(19):
        wx=21-i; wy=30-i
        if wx>=0: _px(s,wx,wy,O)
    for x in range(2,22):
        leading_y = 30-(21-x)
        for y in range(leading_y, min(44, leading_y+(22-x)//3+14)):
            _px(s,x,y, D if (x+y)%2==0 else M)
    for i in range(19):
        wx=27+i; wy=30-i
        if wx<48: _px(s,wx,wy,O)
    for x in range(27,46):
        leading_y = 30-(x-27)
        for y in range(leading_y, min(44, leading_y+(x-26)//3+14)):
            _px(s,x,y, D if (x+y)%2==0 else M)
    # Wing tip fingers
    for fx,fy in [(2,14),(6,11),(10,10)]: _px(s,fx,fy,O); _px(s,fx+1,fy,O)
    for fx,fy in [(46,14),(42,11),(38,10)]: _px(s,fx,fy,O); _px(s,fx-1,fy,O)
    # Feet/claws
    for cx in [22,24,26]: _vl(s,cx,46,50,M); _px(s,cx-1,50,O); _px(s,cx,50,O)

def _enemy_beetle(s):
    O=(100,140,60); M=(60,95,32); D=(28,52,12); SH=(130,170,80); Y=(220,195,50)
    # oval shell body
    for y in range(28,56):
        hw=9-abs(y-40)//3; _hl(s,23-hw,24+hw,y,M)
        _px(s,23-hw,y,O); _px(s,24+hw,y,O)
    # shell carapace
    _hl(s,15,32,28,SH); _hl(s,14,33,29,SH); _hl(s,13,34,30,SH)
    _vl(s,23,28,55,D); _vl(s,24,28,55,D)  # shell seam
    for sy in range(30,54,4): _hl(s,15,32,sy,D)  # shell segments
    # small head
    for y in range(21,30): _hl(s,20,27,y,M); _px(s,20,y,O); _px(s,27,y,O)
    _hl(s,20,27,21,O)
    # mandibles
    _px(s,19,26,O); _px(s,18,27,O); _px(s,17,28,O)
    _px(s,28,26,O); _px(s,29,27,O); _px(s,30,28,O)
    # antennae
    for i in range(8): _px(s,21-i,20-i,O); _px(s,26+i,20-i,O)
    # eyes
    _px(s,21,23,Y); _px(s,22,23,Y); _px(s,25,23,Y); _px(s,26,23,Y)
    # six legs — 3 per side
    for lx,ly,ex,ey in [(17,36,8,30),(17,40,6,38),(17,48,8,52),
                         (30,36,39,30),(30,40,41,38),(30,48,39,52)]:
        dx=ex-lx; dy=ey-ly; steps=max(abs(dx),abs(dy))
        for i in range(steps+1):
            _px(s,round(lx+i*dx/max(1,steps)),round(ly+i*dy/max(1,steps)),M if i>0 else O)
        _px(s,ex,ey,O)

def _enemy_hatchling(s):
    O=(185,90,60); M=(130,52,28); D=(72,24,10); E=(255,210,30); SC=(165,75,42)
    # dragon hatchling — small, energetic
    # head with ridge
    for y in range(10,20):
        hw=5-abs(y-14)//2; _hl(s,23-hw,24+hw,y,M); _px(s,23-hw,y,O); _px(s,24+hw,y,O)
    # small horns
    _px(s,21,9,O); _px(s,20,8,O)
    _px(s,26,9,O); _px(s,27,8,O)
    # bright eyes
    _px(s,21,12,E); _px(s,22,12,E); _px(s,25,12,E); _px(s,26,12,E)
    # teeth
    _hl(s,20,27,18,D)
    for tx in range(21,27,2): _px(s,tx,18,SC)
    # short neck
    for y in range(19,24): _hl(s,21,26,y,M); _px(s,21,y,O); _px(s,26,y,O)
    for y in range(19,24,2): _px(s,22,y,SC); _px(s,25,y,SC)  # scale ridge
    # compact body
    for y in range(24,48): _hl(s,18,29,y,M); _px(s,18,y,O); _px(s,29,y,O)
    for sy in range(26,46,3):
        for sx in range(19,28,3): _px(s,sx,sy,SC); _px(s,sx+1,sy,SC)
    # small wings folded
    _vl(s,14,18,35,O); _vl(s,13,19,34,D)
    _hl(s,13,17,18,O); _hl(s,14,18,35,O)
    _vl(s,33,18,35,O); _vl(s,34,19,34,D)
    _hl(s,30,34,18,O); _hl(s,30,34,35,O)
    # clawed feet
    for y in range(48,62): _hl(s,18,21,y,M); _px(s,18,y,O); _px(s,21,y,O)
    for y in range(48,62): _hl(s,26,29,y,M); _px(s,26,y,O); _px(s,29,y,O)
    for i in range(3): _px(s,17+i,62,O); _px(s,25+i,62,O)
    # curling tail
    for i,ty in enumerate(range(40,60)): _px(s,29+i//3,ty,SC if i%2==0 else M)

def _enemy_giant_rat(s):
    O=(140,120,90); F=(95,78,52); D=(56,44,26); B=(210,195,165); E=(200,50,50)
    # Main body — horizontal oval, properly centered
    for y in range(38,54):
        hw = 14 - abs(y-44)*2//3
        _hl(s,10, 10+hw*2, y, F)
        _px(s,10,y,O); _px(s,10+hw*2,y,O)
    # Hunched back ridge
    _hl(s,12,36,38,O); _hl(s,11,37,39,D)
    # Belly highlight
    _hl(s,13,35,52,B); _hl(s,14,34,53,B)
    # Head — at left end, y=33-45
    for y in range(33,45):
        hw = 6 - abs(y-39)*4//9
        _hl(s,4,4+hw*2,y,F); _px(s,4,y,O); _px(s,4+hw*2,y,O)
    # Long pointy snout
    for y in range(36,42): _hl(s,0,5,y,F); _px(s,0,y,O)
    _hl(s,0,2,40,O)
    _px(s,0,38,D); _px(s,1,38,D)  # nostrils
    # Beady red eyes
    _px(s,13,34,E); _px(s,14,34,E)
    # Round ears — bumps on top, not pillars
    for ex in [13,19]:
        _hl(s,ex,ex+4,29,O); _hl(s,ex,ex+4,30,F); _hl(s,ex,ex+4,31,F)
        _hl(s,ex+1,ex+3,32,F); _px(s,ex+1,30,B); _px(s,ex+2,30,B)
    # Whiskers
    for i in range(5): _px(s,i,36,O); _px(s,i,40,O)
    _px(s,3,38,O); _px(s,2,37,O); _px(s,2,39,O)
    # 4 short legs
    for lx,ly in [(12,54),(18,54),(28,54),(34,54)]:
        for y in range(ly, ly+7): _hl(s,lx,lx+3,y,F); _px(s,lx,y,O); _px(s,lx+3,y,O)
        _hl(s,lx-1,lx+4,ly+6,O)
    # Long curved tail — sweeps right and up
    for i in range(16):
        tx = 37+i; ty = 46 - int(i*i*0.07)
        _px(s,min(47,tx), max(20,ty), F if i%2==0 else D)
    for i in range(4): _px(s,min(47,46+i),20,O)

# ─────────────────────────────────────────────────────────────────────────────
#  UNIQUE CREATURE SPRITES (Act 2 / Act 3 enemies and bosses)
# ─────────────────────────────────────────────────────────────────────────────

def _enemy_swamp_leech(s):
    """Bloated blood-filled worm, dark mottled purplish-brown."""
    O=(90,50,80); M=(140,60,110); D=(50,25,45); E=(220,60,60); BL=(180,140,160)
    import math
    # main body — fat S-curve worm
    for y in range(12, 68):
        cx = 24 + int(5 * math.sin(y * 0.12))
        hw = max(2, 9 - abs(y - 38) // 8)
        _hl(s, cx - hw, cx + hw, y, M)
        _px(s, cx - hw, y, O); _px(s, cx + hw, y, O)
    # segmentation rings
    for sy in range(16, 68, 6):
        cx = 24 + int(5 * math.sin(sy * 0.12))
        _hl(s, cx - 7, cx + 7, sy, D)
    # sucker mouth (top)
    for y in range(8, 14):
        _hl(s, 20, 27, y, D)
    for tx in range(21, 27, 2): _px(s, tx, 10, O)  # teeth ring
    _px(s, 23, 11, E); _px(s, 24, 11, E)            # throat
    # eye-spots (vestigial)
    _px(s, 20, 15, E); _px(s, 21, 15, E)
    _px(s, 26, 15, E); _px(s, 27, 15, E)
    # belly sheen
    for y in range(20, 60, 3):
        cx = 24 + int(5 * math.sin(y * 0.12))
        _hl(s, cx - 2, cx + 2, y, BL)
    # tail taper
    for y in range(66, 74):
        cx = 24 + int(5 * math.sin(66 * 0.12))
        hw = max(1, 4 - (y - 66))
        _hl(s, cx - hw, cx + hw, y, O)

def _enemy_tunnel_lurker(s):
    """Pale eyeless predator — long limbs, hunched, translucent."""
    O=(210,200,185); M=(170,165,155); D=(120,115,108); E=(200,60,60); BL=(230,220,210)
    # elongated torso — hunched
    for y in range(20, 50):
        hw = 5 + (y - 20) // 8
        _hl(s, 22 - hw, 22 + hw, y, M)
        _px(s, 22 - hw, y, O); _px(s, 22 + hw, y, O)
    # no eyes — smooth pale head
    for y in range(10, 22):
        hw = 4 - abs(y - 15) // 3
        _hl(s, 22 - hw, 22 + hw, y, M)
        _px(s, 22 - hw, y, O); _px(s, 22 + hw, y, O)
    # mouth slit (wide)
    _hl(s, 16, 28, 19, D)
    for tx in range(17, 28, 2): _px(s, tx, 19, BL)  # pale teeth
    # four long spindly legs
    for lx, ly_start in [(10, 48), (16, 50), (26, 50), (34, 48)]:
        for y in range(ly_start, ly_start + 22, 1):
            _px(s, lx, y, D if y % 3 == 0 else O)
        # claws
        _px(s, lx - 1, ly_start + 22, D)
        _px(s, lx + 1, ly_start + 22, D)
    # long arms (reaching forward)
    for y in range(24, 42):
        _px(s, 8 - (y - 24) // 6, y, O)
        _px(s, 36 + (y - 24) // 6, y, O)
    # translucent internal organs hinted
    for oy in range(28, 44, 4):
        _hl(s, 20, 24, oy, D)

def _enemy_egg_sac(s):
    """Pulsing silk egg sac, spider-web wrapped, faintly glowing."""
    O=(200,185,150); M=(150,135,105); D=(80,70,50); G=(120,200,120); W=(230,225,215)
    import math
    # main sac — fat oval
    for y in range(8, 68):
        cx = 23
        hw = int(11 * math.sin(max(0, (y - 8) / 60 * math.pi)))
        if hw > 0:
            _hl(s, cx - hw, cx + hw, y, M)
            _px(s, cx - hw, y, O); _px(s, cx + hw, y, O)
    # silk wrap bands (diagonal)
    for i in range(6):
        y0 = 12 + i * 10
        for x in range(10, 36):
            dy = (x - 10) // 4
            if 0 <= y0 + dy < H: _px(s, x, y0 + dy, D)
            if 0 <= y0 - dy < H: _px(s, x, y0 - dy, D)
    # inner glow — eggs visible through silk
    for ey, ex in [(22, 19), (25, 26), (32, 21), (35, 27), (42, 23), (48, 25), (18, 23)]:
        _px(s, ex, ey, G); _px(s, ex + 1, ey, G)
        _px(s, ex, ey + 1, G)
    # attachment threads at top
    for tx in range(16, 30, 3):
        _vl(s, tx, 2, 8, W)
    # slight pulse highlight on surface
    for y in range(20, 55, 5):
        cx = 23 + int(2 * math.sin(y * 0.3))
        _hl(s, cx - 3, cx + 3, y, W)

def _enemy_void_tendril(s):
    """Writhing shadow tendril — inky black with purple-void highlights."""
    O=(100,40,160); M=(50,15,90); D=(15,5,30); E=(200,80,255); HL=(160,100,220)
    import math
    # multiple writhing tendrils from a base
    for t in range(4):
        phase = t * 1.5
        x0 = 10 + t * 9
        for y in range(75, 15, -1):
            cx = x0 + int(4 * math.sin((y * 0.18) + phase))
            thick = 1 + (y > 55)
            for dx in range(-thick, thick + 1):
                _px(s, cx + dx, y, M if (y + t) % 4 < 2 else D)
            # glow tip
            if y < 25:
                _px(s, cx, y, E if y < 18 else HL)
    # void core at base
    for y in range(68, 78):
        hw = 2 + (y - 68) // 2
        _hl(s, 23 - hw, 23 + hw, y, O)
        _px(s, 23 - hw, y, HL); _px(s, 23 + hw, y, HL)
    # swirling rune glows
    for ry, rx in [(40, 20), (35, 28), (45, 26), (30, 16)]:
        _px(s, rx, ry, E); _px(s, rx + 1, ry, E)

def _enemy_corrupted_treant(s):
    """Twisted dark tree animated by fading — bark cracked with shadow."""
    O=(80,55,30); M=(55,38,18); D=(25,16,6); E=(180,40,200); BK=(15,10,5)
    # thick trunk — tapers toward top
    for y in range(18, 75):
        hw = max(2, 9 - (y - 18) // 10)
        _hl(s, 23 - hw, 23 + hw, y, M)
        _px(s, 23 - hw, y, O); _px(s, 23 + hw, y, O)
    # bark cracks filled with shadow-purple
    for cy, cx in [(25, 19), (32, 26), (40, 21), (48, 27), (56, 22), (62, 25)]:
        _vl(s, cx, cy, cy + 5, E)
        _px(s, cx - 1, cy + 2, E)
    # root legs
    for rx, ry in [(14, 70), (10, 68), (30, 70), (34, 68), (20, 73), (26, 73)]:
        _vl(s, rx, ry, ry + 7, D)
        _px(s, rx - 1, ry + 6, O); _px(s, rx + 1, ry + 6, O)
    # branch arms (gnarled)
    for i in range(8):
        _px(s, 10 - i // 2, 22 + i * 3, O)
        _px(s, 36 + i // 2, 22 + i * 3, O)
    # dark canopy (corrupt foliage)
    for y in range(4, 20):
        hw = max(1, 8 - abs(y - 11) // 2)
        _hl(s, 23 - hw, 23 + hw, y, BK)
        _px(s, 23 - hw, y, D); _px(s, 23 + hw, y, D)
    # glowing eye-knots
    for ey, ex in [(28, 18), (28, 28), (38, 21)]:
        _px(s, ex, ey, E); _px(s, ex + 1, ey, E)
        _px(s, ex, ey + 1, E)

def _enemy_gargoyle(s):
    """Stone-skinned winged guardian — hunched, grey, cracked."""
    O=(130,125,120); M=(95,90,85); D=(55,52,50); E=(220,160,40); W=(200,195,190)
    # wings spread behind body
    for i in range(10):
        _px(s, 5 + i, 14 + i * 2, D); _px(s, 42 - i, 14 + i * 2, D)
        _px(s, 4 + i, 15 + i * 2, M); _px(s, 43 - i, 15 + i * 2, M)
    for i in range(8):
        _hl(s, 5 + i, 8 + i, 14 + i * 3, D)
        _hl(s, 40 - i, 43 - i, 14 + i * 3, D)
    # squat hunched torso
    for y in range(14, 56):
        hw = 7 + (y - 14) // 12
        _hl(s, 23 - hw, 23 + hw, y, M)
        _px(s, 23 - hw, y, O); _px(s, 23 + hw, y, O)
    # stone-cracked surface
    for cy, cx in [(20, 20), (28, 26), (36, 19), (44, 27), (22, 28)]:
        _px(s, cx, cy, D); _px(s, cx + 1, cy, D); _px(s, cx, cy + 1, D)
    # horned head
    _px(s, 20, 5, O); _px(s, 19, 6, O); _px(s, 18, 7, O)
    _px(s, 27, 5, O); _px(s, 28, 6, O); _px(s, 29, 7, O)
    for y in range(7, 16):
        hw = 4 - abs(y - 11) // 2
        _hl(s, 23 - hw, 23 + hw, y, M)
        _px(s, 23 - hw, y, O); _px(s, 23 + hw, y, O)
    # glowing amber eyes
    _px(s, 20, 10, E); _px(s, 21, 10, E)
    _px(s, 25, 10, E); _px(s, 26, 10, E)
    # bared fangs
    _hl(s, 19, 27, 15, D)
    for tx in range(20, 27, 2): _px(s, tx, 15, W); _px(s, tx, 16, W)
    # clawed feet
    for lx, ly in [(15, 55), (28, 55)]:
        for y in range(ly, ly + 12): _hl(s, lx, lx + 4, y, M)
        for i in range(3): _px(s, lx - 1 + i * 2, ly + 12, D)

def _enemy_karreth(s):
    """Karreth — Ancient volcanic dragon boss. Much larger than wyrmling."""
    O=(200,80,30); M=(145,45,15); D=(70,18,5); E=(255,230,20); SC=(175,55,20)
    BL=(255,180,60); WT=(240,220,180)
    # massive curved horns
    for i in range(6): _px(s, 17 - i, 3 + i, O); _px(s, 18 - i, 3 + i, SC)
    for i in range(6): _px(s, 30 + i, 3 + i, O); _px(s, 29 + i, 3 + i, SC)
    # massive head — fills top third
    for y in range(4, 22):
        hw = 9 - abs(y - 12) // 3
        _hl(s, 23 - hw, 23 + hw, y, M)
        _px(s, 23 - hw, y, O); _px(s, 23 + hw, y, O)
    _hl(s, 14, 33, 4, O)  # brow ridge
    # slitted fire-gold eyes
    _hl(s, 17, 19, 10, E); _hl(s, 27, 29, 10, E)
    _px(s, 18, 10, D); _px(s, 28, 10, D)  # slit pupils
    # scale-armored jaw and teeth
    _hl(s, 14, 33, 19, D)
    for tx in range(15, 33, 2): _px(s, tx, 19, WT); _px(s, tx, 20, WT)
    # thick neck
    for y in range(20, 30):
        hw = 7 - (y - 20) // 5
        _hl(s, 23 - hw, 23 + hw, y, M)
        _px(s, 23 - hw, y, O); _px(s, 23 + hw, y, O)
    # massive body — barrel chest, low and powerful
    for y in range(28, 65):
        hw = 12 - abs(y - 44) // 5
        _hl(s, 23 - hw, 23 + hw, y, M)
        _px(s, 23 - hw, y, O); _px(s, 23 + hw, y, O)
    # scale pattern (volcanic)
    for sy in range(30, 62, 4):
        for sx in range(13, 35, 3): _px(s, sx, sy, SC)
    # fire-glow cracks in scales
    for fy, fx in [(33,20),(38,28),(44,16),(50,30),(56,22),(42,35)]:
        _px(s,fx,fy,BL); _px(s,fx+1,fy,BL)
    # wings (huge — peek behind body)
    for i in range(12):
        _px(s, max(0, 8 - i), 22 + i * 2, D)
        _px(s, min(47, 40 + i), 22 + i * 2, D)
        _px(s, max(0, 7 - i), 23 + i * 2, M)
        _px(s, min(47, 41 + i), 23 + i * 2, M)
    # thick clawed feet
    for lx, ly in [(13, 63), (28, 63)]:
        for y in range(ly, ly + 10): _hl(s, lx, lx + 6, y, M)
        for i in range(4): _px(s, lx - 1 + i * 2, ly + 10, D)
    # tail tip
    for i, ty in enumerate(range(52, 72)):
        tx = 36 + i // 2
        if tx < 48: _px(s, tx, ty, SC if i % 2 == 0 else D)

# ─────────────────────────────────────────────────────────────────────────────
#  HUMANOID ENEMY VARIANTS (use character base with colour override)
# ─────────────────────────────────────────────────────────────────────────────

def _enemy_bandit_fighter(s):
    _char_fighter(s)
    # Repaint over the steel — dull iron and worn leather instead
    # (fighter draw calls already give rough approximation; just adjust accent colours)

def _enemy_bandit_archer(s):
    _char_ranger(s)

def _enemy_bandit_thief(s):
    _char_thief(s)

def _enemy_bandit_mage(s):
    _char_mage(s)

def _enemy_bandit_captain(s):
    _char_champion(s)

def _enemy_sellsword(s):
    _char_warder(s)

def _enemy_merc_monk(s):
    _char_monk(s)

def _enemy_merc_cleric(s):
    _char_cleric(s)

def _enemy_merc_spellblade(s):
    _char_spellblade(s)

def _enemy_cult_sorcerer(s):
    _char_archmage(s)

def _enemy_high_cultist(s):
    _char_necromancer(s)

def _enemy_crypt_paladin(s):
    _char_paladin(s)

# ─────────────────────────────────────────────────────────────────────────────
#  DISPATCH TABLES
# ─────────────────────────────────────────────────────────────────────────────

_CHAR_DRAW = {
    "Fighter":       _char_fighter,
    "Mage":          _char_mage,
    "Cleric":        _char_cleric,
    "Thief":         _char_thief,
    "Ranger":        _char_ranger,
    "Monk":          _char_monk,
    "Paladin":       _char_paladin,
    "Warder":        _char_warder,
    "Archmage":      _char_archmage,
    "Necromancer":   _char_necromancer,
    "Spellblade":    _char_spellblade,
    "Champion":      _char_champion,
    "Assassin":      _char_assassin,
    "Warden":        _char_warden,
    "Witch":         _char_witch,
    "Beastlord":     _char_beastlord,
    "Crusader":      _char_crusader,
    "High Priest":   _char_high_priest,
    "Shadow Master": _char_shadow_master,
    "Templar":       _char_templar,
}

# Maps template_key → draw function (covers all unique enemy grids)

def _enemy_bear(s):
    """Large quadruped bear: massive bulk, shoulder hump, round head, thick legs."""
    O=(100,75,50); F=(65,47,28); D=(38,24,12); B=(160,130,90); E=(220,190,50)
    # Huge barrel body — main mass
    for y in range(35,60):
        hw = 16 - abs(y-47)*3//10
        _hl(s,8,8+hw*2,y,F); _px(s,8,y,O); _px(s,8+hw*2,y,O)
    # Shoulder hump (bears are higher at shoulder than hip)
    for y in range(30,42):
        hw = 10 - abs(y-35)*3//9
        _hl(s,8,8+hw*2,y,F); _px(s,8,y,O); _px(s,8+hw*2,y,O)
    # Belly
    _hl(s,12,36,58,B); _hl(s,13,35,59,B)
    # Round heavy head
    for y in range(20,38):
        hw = 9 - abs(y-28)*5//16
        _hl(s,4,4+hw*2,y,F); _px(s,4,y,O); _px(s,4+hw*2,y,O)
    # Broad muzzle
    for y in range(28,36): _hl(s,3,13,y,B); _px(s,3,y,O); _px(s,13,y,O)
    _hl(s,5,11,35,O)
    _px(s,7,36,D); _px(s,8,36,D)  # nostrils
    # Small round ears
    _hl(s,9,13,20,O); _vl(s,10,20,24,O); _vl(s,12,20,24,O); _px(s,11,21,F)
    _hl(s,15,19,20,O); _vl(s,16,20,24,O); _vl(s,18,20,24,O); _px(s,17,21,F)
    # Eyes
    _px(s,10,26,E); _px(s,11,26,E); _px(s,14,26,E); _px(s,15,26,E)
    # 4 thick short legs
    for lx,ly in [(10,60),(17,60),(30,60),(37,60)]:
        for y in range(ly,ly+10): _hl(s,lx,lx+5,y,F); _px(s,lx,y,O); _px(s,lx+5,y,O)
        _hl(s,lx-1,lx+6,ly+9,O)
    # Short stub tail
    _px(s,40,45,F); _px(s,41,44,F); _px(s,41,45,O)


def _enemy_stag(s):
    """Fading-corrupted stag: slender deer body, long legs, prominent antlers, eerie eyes."""
    O=(110,90,60); F=(75,58,35); D=(44,32,15); B=(185,165,125); E=(140,220,120)
    # Slender body
    for y in range(38,58):
        hw = 8 - abs(y-46)*3//12
        _hl(s,14,14+hw*2,y,F); _px(s,14,y,O); _px(s,14+hw*2,y,O)
    # Neck angled up-left
    for i in range(10): _hl(s,15-i//2,19-i//2,38-i,F)
    # Small elegant head
    for y in range(20,34):
        hw = 4 - abs(y-26)*2//8
        _hl(s,7,7+hw*2,y,F); _px(s,7,y,O); _px(s,7+hw*2,y,O)
    # Long snout
    for y in range(28,34): _hl(s,3,9,y,F); _px(s,3,y,O)
    _hl(s,3,6,33,O); _px(s,4,33,D); _px(s,5,33,D)
    # Glowing green eyes (fading corruption)
    _px(s,10,22,E); _px(s,11,22,E); _px(s,10,23,E)
    # Tall branching antlers
    _vl(s,13,6,20,O); _vl(s,14,5,20,O)
    _hl(s,10,14,10,O); _hl(s,10,14,11,O)
    _hl(s,13,17,14,O); _hl(s,13,17,15,O)
    _vl(s,17,6,20,O); _vl(s,18,5,20,O)
    _hl(s,17,22,9,O); _hl(s,17,22,10,O)
    _hl(s,14,18,14,O)
    _px(s,9,10,O); _px(s,22,9,O); _px(s,23,8,O)
    # 4 slender long legs
    for lx,ly in [(15,58),(20,58),(27,58),(32,58)]:
        for y in range(ly,ly+14): _hl(s,lx,lx+2,y,F); _px(s,lx,y,O); _px(s,lx+2,y,O)
        _hl(s,lx-1,lx+3,ly+13,O)
    # White tail flash
    _px(s,38,44,B); _px(s,39,43,B); _px(s,39,44,O)


_ENEMY_DRAW = {
    "Goblin Warrior":     _enemy_goblin_warrior,
    "Goblin Archer":      _enemy_goblin_archer,
    "Goblin Brute":       _enemy_goblin_brute,
    "Goblin Shaman":      _enemy_goblin_shaman,
    "Goblin Scout":       _enemy_goblin_shaman,
    "Goblin Drummer":     _enemy_goblin_shaman,
    "Goblin Trapper":     _enemy_goblin_shaman,
    "Goblin King":        _enemy_goblin_king,
    "Grak the Goblin King": _enemy_goblin_king,
    "Goblin War Boss":    _enemy_goblin_king,
    "Orc Warrior":        _enemy_orc_warrior,
    "Orc Fighter":        _enemy_orc_warrior,
    "Orc Chieftain":      _enemy_orc_chieftain,
    "Skeleton Warrior":   _enemy_skeleton,
    "Skeletal Archer":    _enemy_skeleton,
    "Bone Colossus":      _enemy_skeleton,
    "Zombie":             _enemy_zombie,
    "Giant Spider":       _enemy_giant_spider,
    "Giant Spider Queen": _enemy_giant_spider,
    "Spider Queen":       _enemy_giant_spider,
    "Broodmother Guard":  _enemy_giant_spider,
    "Spiderling":         _enemy_giant_spider,
    "Web Spinner":        _enemy_giant_spider,
    "Phase Spider":       _enemy_giant_spider,
    "Venomfang Spider":   _enemy_giant_spider,
    "Troll":              _enemy_troll,
    "Marsh Troll":        _enemy_troll,
    "Volcanic Troll":     _enemy_troll,
    "Dark Mage":          _enemy_dark_mage,
    "Vampire":            _enemy_vampire,
    "Dragon Wyrmling":    _enemy_dragon,
    "Corrupted Hatchling": _enemy_hatchling,
    "Dragon Hatchling":   _enemy_hatchling,
    "Fire Lizard":        _enemy_hatchling,
    "Cinder Drake":       _enemy_hatchling,
    "Cave Drake":         _enemy_hatchling,
    "Abomination":        _enemy_abomination,
    "Boss Valdris":       _enemy_boss_valdris,
    "Wolf":               _enemy_wolf,
    "Dire Wolf":          _enemy_wolf,
    "Hound":              _enemy_hound,
    "War Hound":          _enemy_hound,
    "Guard Hound":        _enemy_hound,
    "Hunting Hound":      _enemy_hound,
    "Rabid Hound":        _enemy_hound,
    "Corrupted Hound":    _enemy_hound,
    "Bandit":             _enemy_bandit,
    "Highway Bandit":     _enemy_bandit,
    "Ashenmoor Bandit":   _enemy_bandit,
    "Bandit Crossbowman": _enemy_bandit_archer,
    "Ruin Archer":        _enemy_bandit_archer,
    "Stone Sentinel":     _enemy_stone_sentinel,
    "Stone Guardian":     _enemy_stone_sentinel,
    "Animated Armor":     _enemy_stone_sentinel,
    "Mine Golem":         _enemy_stone_sentinel,
    "Golem":              _enemy_stone_sentinel,
    "Coral Golem":        _enemy_stone_sentinel,
    "Storm Golem":        _enemy_stone_sentinel,
    "Flesh Golem":        _enemy_stone_sentinel,
    "Ash Revenant":       _enemy_ash_revenant,
    "Fading Wraith":      _enemy_wraith,
    "Crypt Shade":        _enemy_wraith,
    "Dust Wraith":        _enemy_wraith,
    "Wailing Spirit":     _enemy_wraith,
    "Isle Shade":         _enemy_wraith,
    "Saltwater Shade":    _enemy_wraith,
    "Throne Shade":       _enemy_wraith,
    "Tide Wraith":        _enemy_wraith,
    "Wind Wraith":        _enemy_wraith,
    "Lingering Will":     _enemy_wraith,
    "Shadow Stalker":     _enemy_wraith,
    "Shadow Brute":       _enemy_wraith,
    "Reality Fracture":   _enemy_wraith,
    "Kobold Firebrand":   _enemy_kobold,
    "Kobold Miner":       _enemy_kobold,
    "Kobold Trapsmith":   _enemy_kobold,
    "Kobold":             _enemy_kobold,
    "Ghoul":              _enemy_ghoul,
    "Plague Bearer":      _enemy_ghoul,
    "Drowned Revenant":   _enemy_ghoul,
    "Warden Revenant":    _enemy_ghoul,
    "Death Knight":       _enemy_death_knight,
    "Corrupted Scholar":  _enemy_death_knight,
    "Ruin Sentinel":      _enemy_death_knight,
    "Undead Foreman":     _enemy_death_knight,
    "Cave Bat":           _enemy_cave_bat,
    "Dungeon Bat":        _enemy_cave_bat,
    "Shadow Bat":         _enemy_cave_bat,
    "Lava Bat":           _enemy_cave_bat,
    "Cave-in Beetle":     _enemy_beetle,
    "Lava Beetle":        _enemy_beetle,
    "Tunnel Beetle":      _enemy_beetle,
    "Giant Rat":          _enemy_giant_rat,
    "Dungeon Rat":        _enemy_giant_rat,
    "Sewer Rat":          _enemy_giant_rat,
    "Rabid Rat":          _enemy_giant_rat,
    "Mine Rat Swarm":     _enemy_giant_rat,
    # ── Unique creatures ──────────────────────────────────────────
    "Swamp Leech":        _enemy_swamp_leech,
    "Tunnel Lurker":      _enemy_tunnel_lurker,
    "Egg Sac":            _enemy_egg_sac,
    "Void Tendril":       _enemy_void_tendril,
    "Corrupted Treant":   _enemy_corrupted_treant,
    "Gargoyle":           _enemy_gargoyle,
    # ── Bosses (unique sprites) ───────────────────────────────────
    "Karreth":                 _enemy_karreth,
    "Shadow Valdris":          _enemy_boss_valdris,
    "Valdris the Broken":      _enemy_boss_valdris,
    "Valdris, Shadow Avatar":  _enemy_boss_valdris,
    # ── Boss-adjacent (best visual fit) ───────────────────────────
    "Korrath the Stone Warden": _enemy_death_knight,
    "Commander Ashvar":         _enemy_dark_mage,
    "The Pale Sentinel":        _enemy_wraith,
    "The Last Keeper":          _enemy_stone_sentinel,
    "Corrupted Warden Echo":    _enemy_wraith,
    # ── Named crossbowman / cultist ───────────────────────────────
    "Ashenmoor Crossbowman":    _enemy_bandit_archer,
    "Fading Cultist":           _enemy_cult_sorcerer,
    "Crystal Elemental":        _enemy_stone_sentinel,
    "Tempest Sprite":           _enemy_cave_bat,
    "Fungal Crawler":           _enemy_beetle,
    # Humanoid variants
    "Bandit Fighter":     _enemy_bandit_fighter,
    "Bandit Archer":      _enemy_bandit_archer,
    "Bandit Thief":       _enemy_bandit_thief,
    "Bandit Mage":        _enemy_bandit_mage,
    "Bandit Captain":     _enemy_bandit_captain,
    "Sellsword":          _enemy_sellsword,
    "Mercenary Scout":    _enemy_bandit_archer,
    "Mercenary Monk":     _enemy_merc_monk,
    "Mercenary War-Cleric": _enemy_merc_cleric,
    "Mercenary Spellblade": _enemy_merc_spellblade,
    "Cultist Initiate":   _enemy_bandit_mage,
    "Cultist Warrior":    _enemy_bandit_fighter,
    "Cultist Hexblade":   _enemy_merc_spellblade,
    "Cult Sorcerer":      _enemy_cult_sorcerer,
    "High Cultist":       _enemy_high_cultist,
    "Crypt Soldier":      _enemy_death_knight,
    "Crypt Ranger":       _enemy_bandit_archer,
    "Crypt Paladin":      _enemy_crypt_paladin,
    "Crypt Archmage":     _enemy_cult_sorcerer,

    # ── Fading corrupted animals ──
    "Fading Wolf":           _enemy_wolf,
    "Fading Hound":          _enemy_hound,
    "Fading Bear":           _enemy_bear,
    "Fading Boar":           _enemy_hound,
    "Fading Stag":           _enemy_stag,
    "Fading Abomination":    _enemy_abomination,

    # ── Imperial soldiers ──
    "Imperial Soldier":      _enemy_bandit_fighter,
    "Imperial Archer":       _enemy_bandit_archer,
    "Imperial Commander":    _enemy_death_knight,
    "Imperial Court Mage":   _enemy_cult_sorcerer,
    "Imperial Inquisitor":   _enemy_crypt_paladin,

    # ── Pirates ──
    "Pirate Deckhand":       _enemy_bandit_fighter,
    "Pirate Markswoman":     _enemy_bandit_archer,
    "Pirate First Mate":     _enemy_bandit_captain,
    "Pirate Captain":        _enemy_sellsword,
    "Pirate Witch Doctor":   _enemy_cult_sorcerer,

    # ── Shadow / Warden variants ──
    "Shadow Warden":         _enemy_wraith,
    "Warden Shade":          _enemy_wraith,
    "Fallen Warden":         _enemy_death_knight,
    "Oathbreaker Knight":    _enemy_death_knight,
    "Stone Warden Ghost":    _enemy_wraith,
    "Iron Ridge Shade":      _enemy_wraith,
    "Dark Consecrator":      _enemy_high_cultist,

    # ── Arcane / Mechanical ──
    "Arcane Sentry":         _enemy_stone_sentinel,
    "Arcane Wisp":           _enemy_cave_bat,
    "Living Tome":           _enemy_cult_sorcerer,
    "Vault Automaton":       _enemy_stone_sentinel,
    "Tower Rat":             _enemy_giant_rat,
    "Dwarven Forge Guard":   _enemy_stone_sentinel,
}

# ─────────────────────────────────────────────────────────────────────────────
#  PUBLIC API
# ─────────────────────────────────────────────────────────────────────────────

def _apply_effect(spr, highlight=False, dead=False, hover=False, tier=-1):
    """Post-process: highlight, greyscale dead, fog unknown enemies."""
    if dead:
        for y in range(H):
            for x in range(W):
                r,g,b,a = spr.get_at((x,y))
                if (r,g,b) == BG: continue
                grey = int(r*0.2 + g*0.2 + b*0.2) + 14
                spr.set_at((x,y),(grey,grey,grey+8,a))
    elif highlight:
        for y in range(H):
            for x in range(W):
                r,g,b,a = spr.get_at((x,y))
                if (r,g,b) == BG: continue
                spr.set_at((x,y),(min(255,r+55),min(255,g+45),min(255,b+35),a))
    elif hover:
        for y in range(H):
            for x in range(W):
                r,g,b,a = spr.get_at((x,y))
                if (r,g,b) == BG: continue
                spr.set_at((x,y),(min(255,r+25),min(255,g+20),min(255,b+15),a))
    if tier == -1:
        ov = pygame.Surface((W,H), pygame.SRCALPHA)
        ov.fill((6,4,14,155))
        spr.blit(ov,(0,0))


def draw_wiz_character(surface, rect, class_name, highlight=False, dead=False):
    spr = pygame.Surface((W, H))
    spr.fill(BG)
    fn = _CHAR_DRAW.get(class_name, _char_fighter)
    fn(spr)
    _apply_effect(spr, highlight=highlight, dead=dead)
    scaled = pygame.transform.scale(spr, (rect.w, rect.h))
    surface.blit(scaled, rect.topleft)


def draw_wiz_enemy(surface, rect, template_key, knowledge_tier=0, hover=False, dead=False):
    spr = pygame.Surface((W, H))
    spr.fill(BG)
    # Try exact match, then prefix match
    fn = _ENEMY_DRAW.get(template_key)
    if fn is None:
        lo = template_key.lower()
        for k, f in _ENEMY_DRAW.items():
            if k.lower() in lo or lo in k.lower():
                fn = f; break
    if fn is None:
        fn = _enemy_goblin_warrior  # ultimate fallback
    fn(spr)
    _apply_effect(spr, dead=dead, hover=hover, tier=knowledge_tier)
    scaled = pygame.transform.scale(spr, (rect.w, rect.h))
    # Make background colour transparent so dungeon wall shows through
    scaled.set_colorkey(BG)
    surface.blit(scaled, rect.topleft)
