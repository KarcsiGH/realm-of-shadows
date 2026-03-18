"""
Realm of Shadows — Dungeon UI v3  (3D Raycaster)

First-person perspective dungeon renderer using a DDA raycaster.
Textured walls per dungeon theme, torch falloff, floor/ceiling shading,
sprite billboarding for enemies/objects, minimap overlay, full HUD.

Public interface (unchanged from v2):
    __init__(dungeon_state)
    draw(surface, mx, my, dt)
    handle_key(key) → result_dict or None
    handle_click(mx, my) → result_dict or None
    show_event(msg, color)
    on_floor_change()
"""

import pygame, math, random
from ui.renderer import SCREEN_W, SCREEN_H, CREAM, GOLD
from ui.pixel_art import draw_dungeon_object
from data.dungeon import (
    DungeonState, PASSABLE_TILES,
    DT_WALL, DT_FLOOR, DT_CORRIDOR,
    DT_DOOR, DT_STAIRS_DOWN, DT_STAIRS_UP, DT_TREASURE, DT_TRAP,
    DT_ENTRANCE, DT_SECRET_DOOR, DT_INTERACTABLE,
)

try:
    from ui.renderer import draw_panel, draw_text_shadow
except ImportError:
    draw_panel = None
    draw_text_shadow = None

# ═══════════════════════════════════════════════════════════════
#  LAYOUT CONSTANTS
# ═══════════════════════════════════════════════════════════════

VP_X, VP_Y   = 0,   50
VP_W, VP_H   = 1100, 810
HUD_H        = 110

MM_X    = VP_X + VP_W + 8
MM_Y    = VP_Y + 4
MM_W    = SCREEN_W - MM_X - 4
MM_H    = 200
MM_TS   = 5

NUM_RAYS    = VP_W
FOV         = math.radians(66)
HALF_FOV    = FOV / 2
PROJ_DIST   = (VP_W / 2) / math.tan(HALF_FOV)

MOVE_SPEED  = 3.5
ROT_SPEED   = 2.2
TORCH_DIST  = 8.0

# ═══════════════════════════════════════════════════════════════
#  DUNGEON THEMES
# ═══════════════════════════════════════════════════════════════

THEMES = {
    "cave":  ((110,90,70),  (45,35,26),  (55,45,34),  (18,14,10), (220,145,55), (12,8,6)  ),
    "mine":  ((120,100,75), (55,42,30),  (65,52,38),  (20,15,10), (240,175,65), (14,10,6) ),
    "crypt": ((80,88,120),  (32,36,55),  (38,42,65),  (12,12,22), (100,130,210),(8,8,16)  ),
    "ruins": ((115,95,72),  (50,40,30),  (62,50,38),  (18,13,9),  (225,160,55), (12,9,6)  ),
    "tower": ((90,82,130),  (38,34,62),  (48,44,78),  (14,12,24), (145,115,230),(8,6,18)  ),
}

# ═══════════════════════════════════════════════════════════════
#  WALL TEXTURE GENERATOR
# ═══════════════════════════════════════════════════════════════

TEX_W, TEX_H = 64, 64
NUM_WALL_VARIANTS = 3   # variants per theme — assigned per tile coordinate hash

# ── Variant generators ───────────────────────────────────────────

def _gen_door_texture():
    """Warm wood door — unchanged, shared by all themes."""
    surf = pygame.Surface((TEX_W, TEX_H))
    rng  = random.Random(0xD00D)
    WOOD_BASE  = (120, 75, 35)
    WOOD_DARK  = (80,  50, 20)
    WOOD_LIGHT = (160, 105, 55)
    surf.fill(WOOD_BASE)
    for px in range(0, TEX_W, 6):
        tone = rng.uniform(0.85, 1.15)
        c = tuple(min(255, int(v * tone)) for v in WOOD_BASE)
        pygame.draw.line(surf, c, (px, 0), (px, TEX_H))
    for py in [TEX_H//6, TEX_H//2, TEX_H*5//6]:
        pygame.draw.rect(surf, WOOD_DARK,  (0, py-2, TEX_W, 4))
        pygame.draw.rect(surf, WOOD_LIGHT, (0, py-3, TEX_W, 1))
    pygame.draw.circle(surf, (200, 160, 40), (TEX_W*3//4, TEX_H//2), 4)
    pygame.draw.circle(surf, (240, 200, 80), (TEX_W*3//4, TEX_H//2), 3)
    return surf


def _gen_stair_texture(going_down=True, light=(180,160,120), dark=(90,75,50)):
    """Full-wall stair texture: perspective step pattern floor-to-ceiling."""
    surf = pygame.Surface((TEX_W, TEX_H))
    rng  = random.Random(0xF17E if going_down else 0xF17A)

    STEP_COL   = light                         # step top face (lighter)
    RISER_COL  = dark                          # step riser face (darker)
    EDGE_COL   = tuple(max(0,c-30) for c in dark)  # step edge crease

    # 5 steps, each occupying TEX_H//5 rows
    n_steps = 5
    step_h  = TEX_H // n_steps

    for s in range(n_steps):
        if going_down:
            # Stairs going down: near step (s=0) is full width at top,
            # far steps get narrower — perspective shrink on x axis
            frac  = (n_steps - s) / n_steps      # 1.0→0.2 top to bottom
        else:
            frac  = (s + 1) / n_steps            # 0.2→1.0 top to bottom

        # Horizontal span of this step across the texture
        margin = int((1.0 - frac) * TEX_W * 0.45)
        x0, x1 = margin, TEX_W - margin

        y_top  = s * step_h
        y_mid  = y_top + max(1, step_h // 3)    # riser/tread divider
        y_bot  = y_top + step_h

        # Step tread (top face, lighter)
        for y in range(y_top, y_mid):
            tone = rng.uniform(0.88, 1.08)
            c = tuple(min(255, int(v * tone)) for v in STEP_COL)
            for x in range(x0, x1):
                surf.set_at((x, y), c)

        # Step riser (front face, darker)
        for y in range(y_mid, y_bot):
            tone = rng.uniform(0.80, 1.0)
            c = tuple(min(255, int(v * tone)) for v in RISER_COL)
            for x in range(x0, x1):
                surf.set_at((x, y), c)

        # Edge crease lines
        if y_top > 0:
            pygame.draw.line(surf, EDGE_COL, (x0, y_top), (x1, y_top), 1)
        pygame.draw.line(surf, EDGE_COL, (x0, y_mid), (x1, y_mid), 1)
        # Side walls (the rock beside the stair edges)
        for y in range(y_top, y_bot):
            for x in range(0, x0):
                surf.set_at((x, y), tuple(int(v*0.4) for v in RISER_COL))
            for x in range(x1, TEX_W):
                surf.set_at((x, y), tuple(int(v*0.4) for v in RISER_COL))

    return surf


def _gen_cave_textures(light, dark):
    """Cave: rough rock face / water-streaked / crumbling."""
    rng0 = random.Random(hash(("cave0", light)))
    rng1 = random.Random(hash(("cave1", light)))
    rng2 = random.Random(hash(("cave2", light)))
    out  = []

    # Variant 0 — rough jagged rock face
    s = pygame.Surface((TEX_W, TEX_H)); mortar = tuple(int(v*0.45) for v in dark); s.fill(mortar)
    for _ in range(220):
        x = rng0.randint(0, TEX_W-1); y = rng0.randint(0, TEX_H-1)
        w = rng0.randint(2, 8);  h = rng0.randint(1, 5)
        tone = rng0.uniform(0.55, 1.1)
        c = tuple(min(255, int(v*tone)) for v in light)
        pygame.draw.rect(s, c, (x, y, min(w, TEX_W-x), min(h, TEX_H-y)))
    # crack lines
    for _ in range(4):
        cx = rng0.randint(4, TEX_W-4); cy = rng0.randint(0, TEX_H//3)
        for _ in range(rng0.randint(8, 18)):
            ex = cx + rng0.randint(-2, 2); ey = cy + rng0.randint(2, 5)
            pygame.draw.line(s, mortar, (cx, cy), (ex, ey), 1)
            cx, cy = ex, ey
    out.append(s)

    # Variant 1 — water-stained: dark vertical streaks + wet sheen at base
    s = pygame.Surface((TEX_W, TEX_H)); s.fill(tuple(int(v*0.4) for v in dark))
    for _ in range(180):
        x = rng1.randint(0, TEX_W-1); y = rng1.randint(0, TEX_H-1)
        tone = rng1.uniform(0.5, 1.0)
        c = tuple(min(255, int(v*tone)) for v in light)
        pygame.draw.rect(s, c, (x, y, rng1.randint(2,7), rng1.randint(1,4)))
    # vertical water streaks
    for _ in range(6):
        sx = rng1.randint(0, TEX_W-1); sy = rng1.randint(0, TEX_H//4)
        streak_c = tuple(max(0, int(v*0.3)) for v in light)
        while sy < TEX_H:
            pygame.draw.line(s, streak_c, (sx, sy), (sx + rng1.randint(-1,1), sy+3), 1)
            sy += rng1.randint(2, 5)
    # wet sheen at bottom third — blend over pixels so texture stays visible
    for y in range(TEX_H*2//3, TEX_H):
        fade = (y - TEX_H*2//3) / max(1, TEX_H//3)
        for x in range(TEX_W):
            r2, g2, b2 = s.get_at((x, y))[:3]
            nr = int(r2 * (0.85 - 0.15 * fade))
            ng = int(g2 * (0.82 - 0.12 * fade))
            nb = int(min(255, b2 * (0.88 - 0.08 * fade) + 8 * fade))
            s.set_at((x, y), (max(0, nr), max(0, ng), max(0, nb)))
    out.append(s)

    # Variant 2 — crumbling: patches of exposed earth/rubble
    s = pygame.Surface((TEX_W, TEX_H)); s.fill(tuple(int(v*0.5) for v in dark))
    for _ in range(150):
        x = rng2.randint(0, TEX_W-1); y = rng2.randint(0, TEX_H-1)
        tone = rng2.uniform(0.6, 1.05)
        c = tuple(min(255, int(v*tone)) for v in light)
        pygame.draw.rect(s, c, (x, y, rng2.randint(3,10), rng2.randint(2,6)))
    # dirt/rubble patches (earth tones)
    for _ in range(5):
        px = rng2.randint(0, TEX_W-8); py = rng2.randint(0, TEX_H-8)
        pw = rng2.randint(6, 14); ph = rng2.randint(4, 10)
        ec = (max(0,int(light[0]*0.4+20)), max(0,int(light[1]*0.25+10)), max(0,int(light[2]*0.15)))
        pygame.draw.ellipse(s, ec, (px, py, pw, ph))
    out.append(s)
    return out


def _gen_mine_textures(light, dark):
    """Mine: hewn rock + ore veins / timber-supported / muddy damp."""
    rng0 = random.Random(hash(("mine0", light)))
    rng1 = random.Random(hash(("mine1", light)))
    rng2 = random.Random(hash(("mine2", light)))
    out  = []

    # Variant 0 — rough hewn with glinting ore veins
    s = pygame.Surface((TEX_W, TEX_H)); mortar = tuple(int(v*0.5) for v in dark); s.fill(mortar)
    for _ in range(200):
        x = rng0.randint(0,TEX_W-1); y = rng0.randint(0,TEX_H-1)
        tone = rng0.uniform(0.6, 1.1)
        c = tuple(min(255, int(v*tone)) for v in light)
        pygame.draw.rect(s, c, (x,y,rng0.randint(3,9),rng0.randint(2,5)))
    # gold ore veins
    for _ in range(3):
        vx = rng0.randint(4,TEX_W-4); vy = rng0.randint(4,TEX_H-20)
        for _ in range(rng0.randint(6,14)):
            ex = vx+rng0.randint(-3,3); ey = vy+rng0.randint(1,4)
            pygame.draw.line(s, (200,170,60), (vx,vy),(ex,ey), 1)
            vx,vy = ex,ey
    out.append(s)

    # Variant 1 — timber-supported: beams every ~20px
    s = pygame.Surface((TEX_W, TEX_H)); s.fill(mortar)
    for _ in range(180):
        x = rng1.randint(0,TEX_W-1); y = rng1.randint(0,TEX_H-1)
        tone = rng1.uniform(0.55, 1.0)
        c = tuple(min(255, int(v*tone)) for v in light)
        pygame.draw.rect(s, c, (x,y,rng1.randint(2,8),rng1.randint(1,4)))
    BEAM = (90, 60, 28)
    for beam_y in [TEX_H//5, TEX_H*2//5, TEX_H*3//5, TEX_H*4//5]:
        pygame.draw.rect(s, BEAM, (0, beam_y-3, TEX_W, 6))
        pygame.draw.rect(s, (120,80,38),(0,beam_y-4,TEX_W,1))
    # vertical supports at edges
    for bx in [2, TEX_W-7]:
        pygame.draw.rect(s, BEAM, (bx, 0, 5, TEX_H))
    out.append(s)

    # Variant 2 — muddy/damp: dark base, horizontal moisture lines
    s = pygame.Surface((TEX_W, TEX_H)); s.fill(tuple(int(v*0.38) for v in dark))
    for _ in range(160):
        x = rng2.randint(0,TEX_W-1); y = rng2.randint(0,TEX_H-1)
        tone = rng2.uniform(0.45, 0.9)
        c = tuple(min(255, int(v*tone)) for v in light)
        pygame.draw.rect(s, c, (x,y,rng2.randint(2,7),rng2.randint(1,4)))
    for _ in range(8):
        my = rng2.randint(0, TEX_H-1)
        mc = tuple(max(0,int(v*0.25)) for v in light)
        pygame.draw.line(s, mc, (0, my), (TEX_W-1, my), 1)
    out.append(s)
    return out


def _gen_crypt_textures(light, dark):
    """Crypt: carved smooth stone / moss-covered / cracked exposed earth."""
    rng0 = random.Random(hash(("crypt0", light)))
    rng1 = random.Random(hash(("crypt1", light)))
    rng2 = random.Random(hash(("crypt2", light)))
    out  = []

    # Variant 0 — smooth carved stone blocks (large, precise)
    BLOCK_H = 12; BLOCK_W = 24
    mortar = tuple(int(v*0.38) for v in dark)
    s = pygame.Surface((TEX_W, TEX_H)); s.fill(mortar)
    for row in range(TEX_H//BLOCK_H + 1):
        oy = row*BLOCK_H; offset = (BLOCK_W//2) if row%2 else 0
        for col in range(-1, TEX_W//BLOCK_W+2):
            ox = col*BLOCK_W+offset
            tone = 0.8 + rng0.random()*0.25
            c = tuple(min(255,int(v*tone)) for v in light)
            r = pygame.Rect(ox+1,oy+1,BLOCK_W-2,BLOCK_H-2)
            r.clamp_ip(pygame.Rect(0,0,TEX_W,TEX_H))
            pygame.draw.rect(s, c, r)
            # chisel marks on top edge of each block
            pygame.draw.line(s, tuple(min(255,int(v*1.1)) for v in light),
                             (max(0,ox+2),max(0,oy+1)), (min(TEX_W-1,ox+BLOCK_W-3),max(0,oy+1)), 1)
    out.append(s)

    # Variant 1 — moss-covered: stone base + green patches on lower half
    s = pygame.Surface((TEX_W, TEX_H)); s.fill(mortar)
    for row in range(TEX_H//BLOCK_H + 1):
        oy = row*BLOCK_H; offset = (BLOCK_W//2) if row%2 else 0
        for col in range(-1, TEX_W//BLOCK_W+2):
            ox = col*BLOCK_W+offset
            tone = 0.75 + rng1.random()*0.3
            c = tuple(min(255,int(v*tone)) for v in light)
            r = pygame.Rect(ox+1,oy+1,BLOCK_W-2,BLOCK_H-2)
            r.clamp_ip(pygame.Rect(0,0,TEX_W,TEX_H))
            pygame.draw.rect(s, c, r)
    # moss patches on lower 60%
    for _ in range(18):
        mx = rng1.randint(0, TEX_W-6); my = rng1.randint(TEX_H//4, TEX_H-4)
        mw = rng1.randint(3,10); mh = rng1.randint(2,5)
        mc = (max(0,int(light[0]*0.2+10)), min(255,int(light[1]*0.4+40)), max(0,int(light[2]*0.25+10)))
        pygame.draw.ellipse(s, mc, (mx,my,mw,mh))
    out.append(s)

    # Variant 2 — cracked stone with earth showing
    s = pygame.Surface((TEX_W, TEX_H)); s.fill(mortar)
    for row in range(TEX_H//BLOCK_H + 1):
        oy = row*BLOCK_H; offset = (BLOCK_W//2) if row%2 else 0
        for col in range(-1, TEX_W//BLOCK_W+2):
            ox = col*BLOCK_W+offset
            tone = 0.7 + rng2.random()*0.35
            c = tuple(min(255,int(v*tone)) for v in light)
            r = pygame.Rect(ox+1,oy+1,BLOCK_W-2,BLOCK_H-2)
            r.clamp_ip(pygame.Rect(0,0,TEX_W,TEX_H))
            pygame.draw.rect(s, c, r)
    # crack lines
    for _ in range(5):
        cx = rng2.randint(2,TEX_W-2); cy = rng2.randint(0,TEX_H//2)
        for _ in range(rng2.randint(10,22)):
            ex=cx+rng2.randint(-2,2); ey=cy+rng2.randint(2,6)
            pygame.draw.line(s, mortar, (cx,cy),(ex,ey), 1)
            cx,cy = ex,ey
    # exposed earth patches at cracks
    for _ in range(4):
        px = rng2.randint(0,TEX_W-6); py = rng2.randint(0,TEX_H-6)
        ec = (50+rng2.randint(0,20), 35+rng2.randint(0,15), 20+rng2.randint(0,10))
        pygame.draw.ellipse(s, ec, (px,py,rng2.randint(4,8),rng2.randint(3,6)))
    out.append(s)
    return out


def _gen_ruins_textures(light, dark):
    """Ruins: dressed masonry / overgrown vines / collapsed rubble."""
    rng0 = random.Random(hash(("ruins0", light)))
    rng1 = random.Random(hash(("ruins1", light)))
    rng2 = random.Random(hash(("ruins2", light)))
    out  = []
    mortar = tuple(int(v*0.48) for v in dark)

    # Variant 0 — dressed masonry (varied block sizes)
    s = pygame.Surface((TEX_W, TEX_H)); s.fill(mortar)
    y = 0
    while y < TEX_H:
        bh = rng0.choice([8, 10, 12]); x = 0
        while x < TEX_W:
            bw = rng0.choice([12, 16, 20])
            tone = 0.72 + rng0.random()*0.35
            c = tuple(min(255,int(v*tone)) for v in light)
            r = pygame.Rect(x+1,y+1,min(bw-2,TEX_W-x-1),min(bh-2,TEX_H-y-1))
            if r.w > 0 and r.h > 0: pygame.draw.rect(s, c, r)
            x += bw
        y += bh
    out.append(s)

    # Variant 1 — overgrown: masonry + vine patterns
    s = pygame.Surface((TEX_W, TEX_H)); s.fill(mortar)
    y = 0
    while y < TEX_H:
        bh = rng1.choice([8,10,12]); x = 0
        while x < TEX_W:
            bw = rng1.choice([12,16,20])
            tone = 0.68 + rng1.random()*0.3
            c = tuple(min(255,int(v*tone)) for v in light)
            r = pygame.Rect(x+1,y+1,min(bw-2,TEX_W-x-1),min(bh-2,TEX_H-y-1))
            if r.w > 0 and r.h > 0: pygame.draw.rect(s, c, r)
            x += bw
        y += bh
    # vine tendrils
    VINE = (30, 90, 28)
    for _ in range(5):
        vx = rng1.randint(0,TEX_W-1); vy = 0
        while vy < TEX_H:
            ex=vx+rng1.randint(-2,2); ey=vy+rng1.randint(3,6)
            pygame.draw.line(s, VINE, (vx,vy),(ex,min(TEX_H-1,ey)),1)
            if rng1.random() < 0.3:  # leaf
                pygame.draw.ellipse(s, VINE, (ex-2,ey-2,4,3))
            vx,vy = ex,ey
    out.append(s)

    # Variant 2 — partial collapse/rubble
    s = pygame.Surface((TEX_W, TEX_H)); s.fill(tuple(int(v*0.35) for v in dark))
    for _ in range(250):
        x=rng2.randint(0,TEX_W-1); y=rng2.randint(0,TEX_H-1)
        tone=rng2.uniform(0.5,1.15)
        c=tuple(min(255,int(v*tone)) for v in light)
        pygame.draw.rect(s,c,(x,y,rng2.randint(2,12),rng2.randint(1,6)))
    out.append(s)
    return out


def _gen_tower_textures(light, dark):
    """Tower: fitted stone / arcane-etched / weathered/stained."""
    rng0 = random.Random(hash(("tower0", light)))
    rng1 = random.Random(hash(("tower1", light)))
    rng2 = random.Random(hash(("tower2", light)))
    out  = []
    mortar = tuple(int(v*0.42) for v in dark)
    BRICK_H = 10; BRICK_W = 18

    # Variant 0 — precise fitted stone
    s = pygame.Surface((TEX_W, TEX_H)); s.fill(mortar)
    for row in range(TEX_H//BRICK_H + 1):
        oy = row*BRICK_H; offset = (BRICK_W//2) if row%2 else 0
        for col in range(-1, TEX_W//BRICK_W+2):
            ox = col*BRICK_W+offset
            tone = 0.78 + rng0.random()*0.28
            c = tuple(min(255,int(v*tone)) for v in light)
            r = pygame.Rect(ox+1,oy+1,BRICK_W-2,BRICK_H-2)
            r.clamp_ip(pygame.Rect(0,0,TEX_W,TEX_H))
            pygame.draw.rect(s,c,r)
    out.append(s)

    # Variant 1 — arcane-etched: fitted stone + faint glowing rune lines
    s = pygame.Surface((TEX_W, TEX_H)); s.fill(mortar)
    for row in range(TEX_H//BRICK_H + 1):
        oy = row*BRICK_H; offset = (BRICK_W//2) if row%2 else 0
        for col in range(-1, TEX_W//BRICK_W+2):
            ox = col*BRICK_W+offset
            tone = 0.76 + rng1.random()*0.28
            c = tuple(min(255,int(v*tone)) for v in light)
            r = pygame.Rect(ox+1,oy+1,BRICK_W-2,BRICK_H-2)
            r.clamp_ip(pygame.Rect(0,0,TEX_W,TEX_H))
            pygame.draw.rect(s,c,r)
    # faint rune marks
    RUNE = tuple(min(255,int(v*1.4)) for v in dark)
    for _ in range(6):
        rx = rng1.randint(4,TEX_W-12); ry = rng1.randint(4,TEX_H-12)
        pts = [(rx+rng1.randint(-3,3),ry+rng1.randint(-3,3)) for _ in range(4)]
        if len(pts) >= 2:
            pygame.draw.lines(s, RUNE, False, pts, 1)
    out.append(s)

    # Variant 2 — weathered/stained: darker tones, moisture gradients
    s = pygame.Surface((TEX_W, TEX_H)); s.fill(tuple(int(v*0.36) for v in dark))
    for row in range(TEX_H//BRICK_H + 1):
        oy = row*BRICK_H; offset = (BRICK_W//2) if row%2 else 0
        for col in range(-1, TEX_W//BRICK_W+2):
            ox = col*BRICK_W+offset
            tone = 0.5 + rng2.random()*0.45
            c = tuple(min(255,int(v*tone)) for v in light)
            r = pygame.Rect(ox+1,oy+1,BRICK_W-2,BRICK_H-2)
            r.clamp_ip(pygame.Rect(0,0,TEX_W,TEX_H))
            pygame.draw.rect(s,c,r)
    # stain bands
    for _ in range(4):
        sy = rng2.randint(0,TEX_H-1)
        sc = tuple(max(0,int(v*0.3)) for v in light)
        pygame.draw.line(s, sc, (0,sy),(TEX_W-1,sy),rng2.randint(1,3))
    out.append(s)
    return out


def _gen_theme_textures(theme_id, wall_light, wall_dark):
    """Return list of NUM_WALL_VARIANTS texture surfaces for this theme."""
    fn = {
        "cave":  _gen_cave_textures,
        "mine":  _gen_mine_textures,
        "crypt": _gen_crypt_textures,
        "ruins": _gen_ruins_textures,
        "tower": _gen_tower_textures,
    }.get(theme_id, _gen_cave_textures)
    return fn(wall_light, wall_dark)


def _gen_texture(wall_light, wall_dark, is_door=False):
    """Backward-compat wrapper — returns a single cave-style texture."""
    if is_door:
        return _gen_door_texture()
    return _gen_cave_textures(wall_light, wall_dark)[0]



# ═══════════════════════════════════════════════════════════════
#  SPRITE DATA
# ═══════════════════════════════════════════════════════════════

SPRITE_COLORS = {
    DT_TREASURE:        (255, 220, 50),
    DT_STAIRS_DOWN:     (60,  120, 255),   # blue — descending into darkness
    DT_STAIRS_UP:       (255, 160, 40),    # amber — ascending toward light
    DT_ENTRANCE:        (255, 200, 80),    # warm golden arch
    DT_TRAP:            (255, 140,  0),    # armed trap — pure orange (distinct from enemy red)
    "trap_disarmed":    (90,  140, 80),    # disarmed trap — green/grey flat plate
    "trap_tripped":     (110, 100, 90),    # tripped trap — dull grey plate
    DT_INTERACTABLE:    (80,  200, 255),
    "enemy":            (200, 40,  40),
    "boss":             (255, 20,  100),
    "boss_encounter":   (255, 40,  120),   # boss tile marker — vivid pink-red
    "journal":          (220, 200, 130),
}


# ═══════════════════════════════════════════════════════════════
#  DUNGEON UI CLASS
# ═══════════════════════════════════════════════════════════════

class DungeonUI:

    def __init__(self, ds: DungeonState):
        self.dungeon   = ds
        self.theme_id  = getattr(ds, "theme", "cave")
        th = THEMES.get(self.theme_id, THEMES["cave"])
        self.wall_light, self.wall_dark, self.floor_c, self.ceil_c, \
            self.torch_tint, self.fog_c = th

        # Player state
        self.px    = float(ds.party_x) + 0.5
        self.py    = float(ds.party_y) + 0.5
        self.angle = 0.0
        self._recalc_camera()

        self._keys: set = set()

        # Pre-generate textures — NUM_WALL_VARIANTS per theme
        self._tex_door       = _gen_door_texture()
        self._door_cols      = self._bake_tex_cols(self._tex_door)
        # Stairs down: cool blue-grey (going deeper into darkness)
        _sd_l = (max(0,self.wall_light[0]-20), max(0,self.wall_light[1]-10), min(255,self.wall_light[2]+40))
        _sd_d = (max(0,self.wall_dark[0]-15),  max(0,self.wall_dark[1]-8),   min(255,self.wall_dark[2]+25))
        self._tex_stair_down = _gen_stair_texture(going_down=True,  light=_sd_l, dark=_sd_d)
        # Stairs up: warm amber-tan (going toward the surface)
        _su_l = (min(255,self.wall_light[0]+30), min(255,self.wall_light[1]+15), max(0,self.wall_light[2]-20))
        _su_d = (min(255,self.wall_dark[0]+20),  min(255,self.wall_dark[1]+10),  max(0,self.wall_dark[2]-15))
        self._tex_stair_up   = _gen_stair_texture(going_down=False, light=_su_l, dark=_su_d)
        self._stair_down_cols = self._bake_tex_cols(self._tex_stair_down)
        self._stair_up_cols   = self._bake_tex_cols(self._tex_stair_up)
        _variant_surfs   = _gen_theme_textures(
            self.theme_id, self.wall_light, self.wall_dark)
        self._wall_cols_variants = [
            self._bake_tex_cols(s) for s in _variant_surfs
        ]
        # Fallback if theme returned fewer than NUM_WALL_VARIANTS
        while len(self._wall_cols_variants) < NUM_WALL_VARIANTS:
            self._wall_cols_variants.append(self._wall_cols_variants[0])

        # Z-buffer
        self._zbuf = [0.0] * VP_W

        # Render surface
        self._view = pygame.Surface((VP_W, VP_H))

        # Events
        self.event_message    = ""
        self.event_timer      = 0
        self.event_color      = CREAM
        self.event_queue: list = []

        self.show_camp_confirm   = False
        self.show_stairs_confirm = False
        self.stairs_direction    = None

        # Chest interaction modal
        self.chest_modal         = None   # None or dict with modal state

        self.fading_intensity = 0.0
        self._update_fading()

        self.t     = 0.0
        # Grid-snap movement animation
        self._move_start_x   = self.px
        self._move_start_y   = self.py
        self._move_target_x  = self.px
        self._move_target_y  = self.py
        self._move_anim_t    = 1.0   # start at 1.0 = no animation in progress
        self._turn_start     = self.angle
        self._turn_target    = self.angle
        self._turn_anim_t    = 1.0   # start at 1.0 = no animation in progress
        self._step_cooldown  = 0.0   # seconds before next input accepted
        self._pending_event  = None   # event returned by dungeon.move()
        self.pulse = 0.0

        self._sync_grid_pos()

    # ─────────────────────────────────────────────────────────

    def _bake_tex_cols(self, surf):
        """Pre-bake each column of a texture into a list of colour lists."""
        cols = []
        for x in range(TEX_W):
            col = [surf.get_at((x, y))[:3] for y in range(TEX_H)]
            cols.append(col)
        return cols

    def _recalc_camera(self):
        self.dx =  math.cos(self.angle)
        self.dy =  math.sin(self.angle)
        self.cx = -self.dy * 0.6494
        self.cy =  self.dx * 0.6494

    def _update_fading(self):
        f = self.dungeon.current_floor
        t = self.dungeon.total_floors
        self.fading_intensity = min(0.6, (f-1) / max(1,t) * 0.45)

    def _sync_grid_pos(self):
        self.dungeon.party_x = int(self.px)
        self.dungeon.party_y = int(self.py)

    def on_floor_change(self):
        self._update_fading()
        self.px = float(self.dungeon.party_x) + 0.5
        self.py = float(self.dungeon.party_y) + 0.5
        self._recalc_camera()

    def _is_solid(self, gx, gy):
        fl = self.dungeon.get_current_floor_data()
        if gx < 0 or gy < 0 or gx >= fl["width"] or gy >= fl["height"]:
            return True
        tile = fl["tiles"][gy][gx]
        tt   = tile["type"]
        if tt == DT_SECRET_DOOR and not tile.get("secret_found"):
            return True
        return tt in (DT_WALL, DT_STAIRS_DOWN, DT_STAIRS_UP)

    # ─────────────────────────────────────────────────────────

    def _cast_ray(self, ray_dx, ray_dy):
        """DDA ray → (dist, wall_x_frac, is_ns, is_door, hit_mx, hit_my).

        Doors use Wolfenstein-style half-tile offset: the door surface sits at
        the tile's midpoint, framed by wall texture on both sides. Rays that
        don't reach the midpoint hit the wall frame instead.
        hit_mx, hit_my are the tile coords of the wall that was hit (for
        texture variant selection).
        """
        if ray_dx == 0: ray_dx = 1e-10
        if ray_dy == 0: ray_dy = 1e-10

        delta_x = abs(1.0 / ray_dx)
        delta_y = abs(1.0 / ray_dy)
        step_x  = 1 if ray_dx > 0 else -1
        step_y  = 1 if ray_dy > 0 else -1

        map_x   = int(self.px)
        map_y   = int(self.py)
        frac_x  = self.px - map_x
        frac_y  = self.py - map_y

        sdx = (1.0 - frac_x) * delta_x if ray_dx > 0 else frac_x * delta_x
        sdy = (1.0 - frac_y) * delta_y if ray_dy > 0 else frac_y * delta_y

        fl    = self.dungeon.get_current_floor_data()
        fw    = fl["width"]
        fh    = fl["height"]
        tiles = fl["tiles"]

        for _ in range(64):
            if sdx < sdy:
                sdx  += delta_x
                map_x += step_x
                ns    = False
            else:
                sdy  += delta_y
                map_y += step_y
                ns    = True

            if map_x < 0 or map_y < 0 or map_x >= fw or map_y >= fh:
                return 20.0, 0.0, ns, False, 0, 0, 0.0
            tile = tiles[map_y][map_x]
            tt   = tile["type"]
            is_s     = tt == DT_SECRET_DOOR and not tile.get("secret_found")
            is_stair = tt in (DT_STAIRS_DOWN, DT_STAIRS_UP)
            is_w     = tt == DT_WALL or is_s or is_stair
            is_d     = tt == DT_DOOR

            if is_w:
                if not ns:
                    dist = (map_x - self.px + (1 - step_x)/2) / ray_dx
                else:
                    dist = (map_y - self.py + (1 - step_y)/2) / ray_dy
                if not ns:
                    wx = self.py + dist * ray_dy
                else:
                    wx = self.px + dist * ray_dx
                wx -= math.floor(wx)
                return max(0.01, dist), wx, ns, False, map_x, map_y, is_stair, tt, 0.0

            if is_d:
                # Determine door orientation from neighbors.
                # Doors in an E-W wall (wall above/below) must be hit from ns=True (N/S ray).
                # Doors in a N-S wall (wall left/right) must be hit from ns=False (E/W ray).
                wall_above = (map_y > 0 and tiles[map_y-1][map_x]["type"] == DT_WALL)
                wall_below = (map_y < fh-1 and tiles[map_y+1][map_x]["type"] == DT_WALL)
                wall_left  = (map_x > 0 and tiles[map_y][map_x-1]["type"] == DT_WALL)
                wall_right = (map_x < fw-1 and tiles[map_y][map_x+1]["type"] == DT_WALL)

                # Infer orientation: walls N/S → horizontal door (opens E-W, hit ns=False)
                #                    walls E/W → vertical door (opens N-S, hit ns=True)
                if (wall_above or wall_below) and not (wall_left or wall_right):
                    door_hit_ns = False   # horizontal door in N-S corridor
                elif (wall_left or wall_right) and not (wall_above or wall_below):
                    door_hit_ns = True    # vertical door in E-W corridor
                else:
                    door_hit_ns = ns      # ambiguous — accept any axis

                # If ray hits from the side (wrong axis), render as plain wall
                if ns != door_hit_ns:
                    if not ns:
                        dist = (map_x - self.px + (1 - step_x)/2) / ray_dx
                        wx = self.py + dist * ray_dy
                    else:
                        dist = (map_y - self.py + (1 - step_y)/2) / ray_dy
                        wx = self.px + dist * ray_dx
                    wx -= math.floor(wx)
                    return max(0.01, dist), wx, ns, False, map_x, map_y, False, tt, 0.0

                # Advance ray half a tile to door's midpoint (Wolfenstein style).
                if not ns:
                    ray_comp  = abs(ray_dx)
                    dist_face = (map_x - self.px + (1 - step_x)/2) / ray_dx
                else:
                    ray_comp  = abs(ray_dy)
                    dist_face = (map_y - self.py + (1 - step_y)/2) / ray_dy

                # If ray is too shallow to reliably sample the door midpoint,
                # render it as a plain wall frame instead of corrupted door texture.
                if ray_comp <= 0.65:
                    if not ns:
                        dist = dist_face
                        wx = self.py + dist * ray_dy
                    else:
                        dist = dist_face
                        wx = self.px + dist * ray_dx
                    wx -= math.floor(wx)
                    return max(0.01, dist), wx, ns, False, map_x, map_y, False, tt, 0.0

                dist_mid = dist_face + 0.5 / ray_comp

                # Where does the ray cross the door midplane?
                if not ns:
                    wx_mid = self.py + dist_mid * ray_dy
                else:
                    wx_mid = self.px + dist_mid * ray_dx
                wx_mid -= math.floor(wx_mid)

                # Edge frame (0.2/0.8 threshold) → wall texture
                if wx_mid < 0.2 or wx_mid > 0.8:
                    if not ns:
                        dist = (map_x - self.px + (1 - step_x)/2) / ray_dx
                        wx = self.py + dist * ray_dy
                    else:
                        dist = (map_y - self.py + (1 - step_y)/2) / ray_dy
                        wx = self.px + dist * ray_dx
                    wx -= math.floor(wx)
                    return max(0.01, dist), wx, ns, False, map_x, map_y, False, tt, 0.0
                else:
                    return max(0.01, dist_mid), wx_mid, ns, True, map_x, map_y, False, tt, max(0.01, dist_face)

        return 20.0, 0.0, False, False, 0, 0, False, DT_WALL, 0.0

    # ─────────────────────────────────────────────────────────
    #  MAIN DRAW
    # ─────────────────────────────────────────────────────────

    def draw(self, surface, mx, my, dt):
        ds          = dt / 1000.0
        self.t     += ds
        self.pulse  = math.sin(self.t * 3.2) * 0.5 + 0.5
        self.event_timer = max(0, self.event_timer - dt)
        self.event_queue = [(m,c,t-dt) for m,c,t in self.event_queue if t-dt > 0]

        self._process_held_keys(ds)
        self._render_3d()

        surface.blit(self._view, (VP_X, VP_Y))
        self._draw_minimap(surface)
        self._draw_hud(surface, mx, my)

        if self.show_camp_confirm:
            self._draw_confirm_dialog(surface, mx, my,
                "Make Camp?", "Rest and recover HP/MP.",
                "Camp", "Cancel", "camp")
        if self.show_stairs_confirm:
            if self.stairs_direction == "down":
                t, m = "Descend?", "Go deeper into the dungeon."
            elif self.stairs_direction == "up":
                t, m = "Ascend?", "Return to the previous floor."
            else:
                t, m = "Leave Dungeon?", "Return to the surface."
            self._draw_confirm_dialog(surface, mx, my, t, m, "Yes", "No", "stairs")
        if self.chest_modal:
            self._draw_chest_modal(surface, mx, my)


        if (self.event_message and self.event_timer > 0) or self.event_queue:
            self._draw_events(surface)

    # ─────────────────────────────────────────────────────────
    #  3D RENDER
    # ─────────────────────────────────────────────────────────

    def _render_3d(self):
        view  = self._view
        VH    = VP_H
        VW    = VP_W
        HH    = VH // 2
        zbuf  = self._zbuf
        flick = 0.95 + 0.05 * self.pulse
        FOG   = TORCH_DIST

        # ── Ceiling / floor scanlines with perspective gradient ──
        for sy in range(VH):
            if sy == HH:
                continue
            row_dist = PROJ_DIST / max(1, abs(sy - HH))
            fog_t    = min(1.0, row_dist * 0.35 / FOG)
            # Distance from horizon (0=horizon, 1=screen edge)
            horizon_t = abs(sy - HH) / HH
            if sy < HH:
                # Ceiling: dark at horizon, slightly lighter at top
                base = tuple(int(self.ceil_c[i]*(1-fog_t) + self.fog_c[i]*fog_t) for i in range(3))
                c = tuple(max(0, int(v * (0.35 + 0.65 * horizon_t))) for v in base)
            else:
                # Floor: dark at horizon, lighter at bottom
                base = tuple(int(self.floor_c[i]*(1-fog_t*0.85) + self.fog_c[i]*fog_t*0.85) for i in range(3))
                c = tuple(max(0, int(v * (0.45 + 0.55 * horizon_t))) for v in base)
            pygame.draw.line(view, c, (0, sy), (VW-1, sy))
        # Dark horizon band — separates floor from ceiling sharply
        for band_y in range(HH - 1, HH + 2):
            if 0 <= band_y < VH:
                pygame.draw.line(view, (4, 3, 5), (0, band_y), (VW-1, band_y))

        # ── Floor grid — perspective lines per tile square ──
        # Horizontal lines at integer tile distances (receding rows)
        for tile_d in range(1, 9):
            sy = int(HH + PROJ_DIST / tile_d)
            if HH < sy < VH:
                fog_t   = min(1.0, tile_d / FOG)
                alpha   = max(0, int(55 * (1.0 - fog_t)))
                base_g  = tuple(int(self.floor_c[i] * 0.55) for i in range(3))
                gc      = tuple(min(255, base_g[i] + alpha) for i in range(3))
                pygame.draw.line(view, gc, (0, sy), (VW - 1, sy))
        # Vertical lines — perspective-correct column dividers (fan out from horizon centre)
        # Number of tile columns visible at distance 1: roughly FOV / (pi/4) ≈ 1.5 tiles each side
        N_COLS = 5   # lines each side of centre (covers ~half-tile spacing at near dist)
        for ci in range(-N_COLS, N_COLS + 1):
            # Screen x at the horizon for this column boundary
            cam_frac = ci / N_COLS   # -1..1 across half-FOV
            hx = int(VW // 2 + cam_frac * (VW // 2))
            # Fan the line from (hx, HH) down to a spread-out bottom position
            spread = int((ci / N_COLS) * VW * 0.35)
            bx = VW // 2 + spread
            for tile_d in range(1, 8):
                sy_top = int(HH + PROJ_DIST / (tile_d + 0.5))
                sy_bot = int(HH + PROJ_DIST / tile_d)
                if sy_top >= VH:
                    break
                sy_bot = min(sy_bot, VH - 1)
                # Interpolate x position at each y between the two distances
                if sy_bot <= sy_top:
                    continue
                t_top = (tile_d + 0.5)
                t_bot = tile_d
                x_top = int(VW // 2 + cam_frac * (VW // 2) * (t_top / (t_top + 0.1)))
                x_bot = int(VW // 2 + (ci / N_COLS) * VW * 0.35 * min(1.0, tile_d / 3.0))
                fog_t  = min(1.0, tile_d / FOG)
                alpha  = max(0, int(40 * (1.0 - fog_t)))
                base_g = tuple(int(self.floor_c[i] * 0.55) for i in range(3))
                gc     = tuple(min(255, base_g[i] + alpha) for i in range(3))
                pygame.draw.line(view, gc, (x_top, sy_top), (x_bot, sy_bot))

        # ── Wall columns ──
        wall_variants = self._wall_cols_variants
        door_cols     = self._door_cols
        num_v         = len(wall_variants)

        for col in range(VW):
            cam_x    = (2.0 * col / VW) - 1.0
            ray_dx   = self.dx + self.cx * cam_x
            ray_dy   = self.dy + self.cy * cam_x
            dist, wx, ns, is_door, hit_mx, hit_my, is_stair, hit_tt, door_face_dist = self._cast_ray(ray_dx, ray_dy)
            zbuf[col] = dist

            # Doors: use face distance for height (door is full wall height),
            # dist is the midpoint distance used only for texture sampling.
            _height_dist = door_face_dist if is_door else dist
            wall_h = min(VH, int(PROJ_DIST / max(0.01, _height_dist)))
            top    = HH - wall_h // 2

            tex_x = int(wx * TEX_W) % TEX_W
            if is_door:
                cols_src = door_cols[tex_x]
            elif is_stair:
                # Dedicated stair texture — no sprite overlay needed
                if hit_tt == DT_STAIRS_DOWN:
                    cols_src = self._stair_down_cols[tex_x]
                else:
                    cols_src = self._stair_up_cols[tex_x]
            else:
                # Pick variant deterministically from tile coords — stable, no flicker
                v_idx    = (hit_mx * 2654435761 ^ hit_my * 2246822519) % num_v
                cols_src = wall_variants[v_idx][tex_x]

            stair_tint = None  # no longer needed — using dedicated texture

            # Lighting
            fog_t = min(1.0, dist / FOG)
            ns_f  = 0.52 if ns else 1.0
            bright = ns_f * (1.0 - fog_t * 0.82) * flick
            bright = max(0.0, min(1.0, bright))
            fog_c  = self.fog_c
            fb     = 1.0 - bright

            for screen_y in range(max(0, top), min(VH, top + wall_h)):
                tex_y = int((screen_y - top) / wall_h * TEX_H) % TEX_H
                r, g, b = cols_src[tex_y]
                rc = int(r * bright + fog_c[0] * fb)
                gc = int(g * bright + fog_c[1] * fb)
                bc = int(b * bright + fog_c[2] * fb)
                view.set_at((col, screen_y), (rc, gc, bc))

        # ── Sprites ──
        self._render_sprites(view, zbuf)

        # ── Fading overlay ──
        if self.fading_intensity > 0.05:
            self._fading_overlay(view)

        # ── Crosshair ──
        cx, cy = VW // 2, VH // 2
        pygame.draw.line(view, (255,255,255), (cx-10, cy), (cx+10, cy), 1)
        pygame.draw.line(view, (255,255,255), (cx, cy-10), (cx, cy+10), 1)

    def _render_sprites(self, view, zbuf):
        fl     = self.dungeon.get_current_floor_data()
        tiles  = fl["tiles"]
        fh, fw = fl["height"], fl["width"]

        sprites = []
        for ty in range(fh):
            for tx in range(fw):
                tile = tiles[ty][tx]
                if not tile.get("discovered"):
                    continue
                tt = tile["type"]
                icon_key = None
                enc_key  = None
                # Stairs are now solid walls in the raycaster — skip as sprites
                if tt in (DT_STAIRS_DOWN, DT_STAIRS_UP):
                    pass  # rendered as wall texture — no sprite needed
                elif tt == DT_TRAP:
                    # Only show trap sprite if the party knows about it
                    ev = tile.get("event", {})
                    if ev.get("disarmed"):
                        icon_key = "trap_disarmed"
                    elif ev.get("tripped"):
                        icon_key = "trap_tripped"
                    elif ev.get("detected"):
                        icon_key = DT_TRAP     # armed and detected — red spikes
                    # else undiscovered — no sprite shown
                elif tt in SPRITE_COLORS:
                    icon_key = tt
                enc = tile.get("encounter")
                if enc and not enc.get("cleared"):
                    icon_key = "boss" if enc.get("is_boss") else "enemy"
                    enc_key  = enc.get("enc_key")
                # Boss encounter event tile — show pulsing marker before triggered
                ev_t = tile.get("event") or {}
                if ev_t.get("type") == "boss_encounter" and not ev_t.get("triggered"):
                    icon_key = "boss_encounter"
                if tile.get("has_journal") and not tile.get("journal_read"):
                    icon_key = "journal"
                if icon_key is None:
                    continue
                sx = tx + 0.5 - self.px
                sy = ty + 0.5 - self.py
                d  = math.sqrt(sx*sx + sy*sy)
                if d < 0.3 or d > TORCH_DIST + 1:
                    continue
                sprites.append((d, sx, sy, icon_key, enc_key))

        # Add visible patrol enemies from the floor enemy list
        for enemy in fl.get("enemies", []):
            if enemy.get("state") == "dead":
                continue
            ex, ey = enemy["x"], enemy["y"]
            if not tiles[ey][ex].get("discovered"):
                continue
            esx = ex + 0.5 - self.px
            esy = ey + 0.5 - self.py
            d   = math.sqrt(esx*esx + esy*esy)
            if d < 0.3 or d > TORCH_DIST + 1:
                continue
            sprites.append((d, esx, esy, "enemy", enemy.get("enc_key")))

        sprites.sort(key=lambda s: -s[0])

        font = pygame.font.SysFont("segoeuisymbol,symbola,unifont,dejavusans", 32)
        for dist, sx, sy, icon_key, enc_key in sprites:
            inv = 1.0 / (self.cx * self.dy - self.dx * self.cy)
            tx_ = inv * (self.dy * sx - self.dx * sy)
            ty_ = inv * (-self.cy * sx + self.cx * sy)
            if ty_ <= 0.1:
                continue
            screen_x = int((VP_W/2) * (1 + tx_ / ty_))
            full_wall_h = max(1, abs(int(PROJ_DIST / ty_)))  # unscaled wall height
            sp_h = full_wall_h
            sp_w = sp_h

            # Scale objects down relative to wall height — walls fill the space,
            # objects should sit within it. Enemies stay full-ish, objects smaller.
            _OBJ_SCALE = {
                DT_TREASURE:     0.35,   # chest — squat, sits on floor
                DT_STAIRS_DOWN:  0.55,   # stairs — wide, not tall
                DT_STAIRS_UP:    0.55,
                DT_INTERACTABLE: 0.72,   # shrine/fountain — taller, more visible
                DT_ENTRANCE:     0.80,   # archway — tall but not full wall
                DT_TRAP:         0.35,   # trap plate — raised rune plate, visible
                "trap_disarmed": 0.25,
                "trap_tripped":  0.20,
                "journal":       0.30,
                "enemy":         0.85,
                "boss_encounter": 0.90,   # boss marker — tall, threatening
                "boss":          1.00,
            }
            type_scale = _OBJ_SCALE.get(icon_key, 0.60)

            # Distance-based scale: full size at ≤1 tile, minimum at SIGHT_RADIUS tiles
            SIGHT_RADIUS = 3.0
            MIN_DIST_SCALE = 0.25
            dist_scale = MIN_DIST_SCALE + (1.0 - MIN_DIST_SCALE) * max(0.0, (SIGHT_RADIUS - dist) / (SIGHT_RADIUS - 0.5))
            dist_scale = max(MIN_DIST_SCALE, min(1.0, dist_scale))

            scale = type_scale * dist_scale
            sp_h = max(1, int(sp_h * scale))
            sp_w = sp_h

            # Floor line: where the floor meets the wall at this distance
            floor_y = VP_H // 2 + full_wall_h // 2

            # Objects that sit ON the floor — bottom edge anchored to floor_y.
            # Objects that float (enemies, boss) — centered at horizon as before.
            # Stairs are also capped in height so they don't fill the view up close.
            _FLOOR_ANCHORED = {
                DT_TREASURE, DT_STAIRS_DOWN, DT_STAIRS_UP,
                DT_INTERACTABLE, DT_TRAP,
                "trap_disarmed", "trap_tripped", "journal",
            }
            if icon_key in _FLOOR_ANCHORED:
                # Cap stairs height so they don't run floor-to-ceiling up close
                if icon_key in (DT_STAIRS_DOWN, DT_STAIRS_UP):
                    sp_h = min(sp_h, VP_H // 3)
                    sp_w = sp_h
                blit_y = floor_y - sp_h   # bottom of sprite sits on floor
            else:
                blit_y = VP_H // 2 - sp_h // 2   # centered at horizon (enemies)

            start_y = max(0, blit_y)
            end_y   = min(VP_H, blit_y + sp_h)
            start_x = max(0, screen_x - sp_w//2)
            end_x   = min(VP_W, screen_x + sp_w//2)
            if start_x >= end_x:
                continue

            color = SPRITE_COLORS.get(icon_key, (200, 200, 200))
            fog_t  = min(1.0, dist / TORCH_DIST)
            alpha  = int(255 * (1.0 - fog_t * 0.88))

            cx_s = (start_x + end_x) // 2
            cy_s = (start_y + end_y) // 2
            r    = max(4, sp_h // 4)

            if 0 <= cx_s < VP_W and ty_ < zbuf[cx_s]:
                surf_w = max(8, sp_w)
                surf_h = max(8, sp_h)
                spr = pygame.Surface((surf_w, surf_h), pygame.SRCALPHA)
                c_a = (*color, alpha)
                dim = (int(color[0]*0.4), int(color[1]*0.4), int(color[2]*0.4), alpha//2)

                if icon_key == DT_ENTRANCE:
                    # Golden stone arch
                    aw = max(6, surf_w * 3 // 4)
                    ah = max(8, surf_h * 4 // 5)
                    ox, oy = (surf_w - aw) // 2, surf_h - ah
                    pygame.draw.rect(spr, dim, (ox, oy, aw, ah), border_radius=aw//2)
                    pygame.draw.rect(spr, c_a, (ox, oy, aw, ah), 2, border_radius=aw//2)
                    # Opening
                    iw, ih = max(2, aw//2), max(3, ah*2//3)
                    pygame.draw.rect(spr, (0,0,0,200), ((surf_w-iw)//2, surf_h-ih, iw, ih))

                elif icon_key == DT_STAIRS_DOWN:
                    obj_r = pygame.Rect(0, 0, surf_w, surf_h)
                    draw_dungeon_object(spr, obj_r, "stairs_down")

                elif icon_key == DT_STAIRS_UP:
                    obj_r = pygame.Rect(0, 0, surf_w, surf_h)
                    draw_dungeon_object(spr, obj_r, "stairs_up")

                elif icon_key == DT_INTERACTABLE:
                    # Distinguish fountain (healing_pool) vs shrine (mp_shrine)
                    fl_d2 = self.dungeon.get_current_floor_data()
                    _ity, _itx = int(ty), int(tx)
                    if 0<=_ity<fl_d2["height"] and 0<=_itx<fl_d2["width"]:
                        i_ev    = (fl_d2["tiles"][_ity][_itx].get("event") or {})
                        i_used  = i_ev.get("used", False)
                        i_subtp = i_ev.get("subtype", "mp_shrine")
                    else:
                        i_used = False; i_subtp = "mp_shrine"
                    obj_r = pygame.Rect(0, 0, surf_w, surf_h)
                    if i_subtp == "healing_pool":
                        obj_key = "fountain_used" if i_used else "fountain_active"
                    else:
                        obj_key = "shrine_used" if i_used else "shrine_active"
                    draw_dungeon_object(spr, obj_r, obj_key)

                elif icon_key == DT_TREASURE:
                    obj_r = pygame.Rect(0, 0, surf_w, surf_h)
                    draw_dungeon_object(spr, obj_r, "chest")

                elif icon_key in ("enemy", "boss"):
                    # Draw faction-specific enemy silhouette from pixel_art
                    from ui.pixel_art import draw_enemy_silhouette
                    from ui.wiz_sprites import BG as _WIZ_BG
                    obj_r = pygame.Rect(0, 0, surf_w, surf_h)
                    # Resolve enc_key → template name via ENCOUNTERS if needed
                    template_key = enc_key or "Goblin Warrior"
                    try:
                        from data.enemies import ENCOUNTERS
                        if enc_key and enc_key in ENCOUNTERS:
                            grps = ENCOUNTERS[enc_key].get("groups", [])
                            if grps:
                                template_key = grps[0]["enemy"]
                    except Exception:
                        pass
                    # Draw onto an SRCALPHA surface so the BG becomes truly transparent.
                    # _apply_effect shifts near-black pixels slightly, so colorkey alone
                    # is unreliable — use per-pixel alpha instead.
                    enemy_surf = pygame.Surface((surf_w, surf_h), pygame.SRCALPHA)
                    enemy_surf.fill((0, 0, 0, 0))          # fully transparent base
                    # Draw sprite onto a scratch surface first (wiz_sprites needs opaque)
                    scratch = pygame.Surface((surf_w, surf_h))
                    scratch.fill(_WIZ_BG)
                    draw_enemy_silhouette(scratch, obj_r, template_key, knowledge_tier=1)
                    scratch.set_colorkey(_WIZ_BG)
                    # Blit colorkeyed scratch onto SRCALPHA surface for clean transparency
                    enemy_surf.blit(scratch, (0, 0))
                    view.blit(enemy_surf, (cx_s - surf_w//2, blit_y))
                    continue  # skip the generic spr blit below

                elif icon_key == DT_TRAP:
                    # Armed detected trap — glowing rune pressure plate
                    pw = max(8, surf_w * 4 // 5)
                    ph = max(4, surf_h // 4)
                    ox = (surf_w - pw) // 2
                    oy = surf_h - ph - 1
                    # Plate base — dark stone
                    pygame.draw.rect(spr, dim, (ox, oy, pw, ph))
                    pygame.draw.rect(spr, c_a, (ox, oy, pw, ph), 1)
                    # Rune glow — pulsing red symbols on the plate
                    pulse_a = int(alpha * (0.75 + 0.25 * abs(math.sin(self.t * 3.5))))
                    glow_c = (*color, pulse_a)
                    # Central rune circle
                    cx_r, cy_r = surf_w // 2, oy + ph // 2
                    r_sz = max(2, ph // 3)
                    pygame.draw.circle(spr, glow_c, (cx_r, cy_r), r_sz, 1)
                    # Radiating rune lines from centre
                    for ang_i in range(4):
                        import math as _m
                        a_ = ang_i * _m.pi / 2
                        rx = cx_r + int(_m.cos(a_) * (pw // 3))
                        ry = cy_r + int(_m.sin(a_) * (ph // 2 - 1))
                        rx = max(ox+1, min(ox+pw-2, rx))
                        ry = max(oy+1, min(oy+ph-2, ry))
                        pygame.draw.line(spr, glow_c, (cx_r, cy_r), (rx, ry), 1)
                    # Outer glow halo — soft bleed above plate
                    halo_h = max(2, ph)
                    halo_a = pulse_a // 2
                    for hly in range(halo_h):
                        fade = int(halo_a * (1 - hly / halo_h))
                        hw = max(2, pw * (halo_h - hly) // halo_h)
                        hx = surf_w // 2 - hw // 2
                        pygame.draw.line(spr, (*color, fade),
                                         (hx, oy - hly), (hx + hw, oy - hly))

                elif icon_key == "trap_disarmed":
                    # Disarmed trap — flat green-grey plate with X mark
                    pw = max(6, surf_w * 4 // 5)
                    ph = max(3, surf_h // 5)
                    ox = (surf_w - pw) // 2
                    oy = surf_h - ph - 1
                    pygame.draw.rect(spr, dim, (ox, oy, pw, ph))
                    pygame.draw.rect(spr, c_a, (ox, oy, pw, ph), 1)
                    # X mark showing disarmed
                    cx2, cy2 = surf_w // 2, oy + ph // 2
                    m = max(2, ph // 2)
                    pygame.draw.line(spr, c_a, (cx2-m, cy2-m), (cx2+m, cy2+m), 1)
                    pygame.draw.line(spr, c_a, (cx2+m, cy2-m), (cx2-m, cy2+m), 1)

                elif icon_key == "trap_tripped":
                    # Tripped/sprung trap — depressed flat grey plate, spikes bent down
                    pw = max(6, surf_w * 4 // 5)
                    ph = max(2, surf_h // 8)
                    ox = (surf_w - pw) // 2
                    oy = surf_h - ph - 1
                    pygame.draw.rect(spr, dim, (ox, oy, pw, ph))
                    pygame.draw.rect(spr, c_a, (ox, oy, pw, ph), 1)
                    # Bent/broken spikes (horizontal lines suggesting sprung state)
                    for si in range(max(2, pw // 6)):
                        sx_ = ox + si * pw // max(2, pw // 6)
                        pygame.draw.line(spr, c_a, (sx_, oy - 1), (sx_ + 3, oy - 2), 1)

                elif icon_key == "boss_encounter":
                    # Pulsing boss marker — column of red-pink light
                    pulse2 = abs(math.sin(self.t * 2.2))
                    pulse_a2 = int(alpha * (0.65 + 0.35 * pulse2))
                    bc = (*color, pulse_a2)
                    bdc = (int(color[0]*0.4), int(color[1]*0.2), int(color[2]*0.3), pulse_a2//2)
                    # Central pillar
                    pw2 = max(4, surf_w // 4)
                    pygame.draw.rect(spr, bdc, ((surf_w-pw2)//2, 0, pw2, surf_h))
                    pygame.draw.rect(spr, bc,  ((surf_w-pw2)//2, 0, pw2, surf_h), 1)
                    # Skull-like top shape
                    skull_r = max(3, surf_w // 5)
                    pygame.draw.circle(spr, bc, (surf_w//2, skull_r + 2), skull_r, 1)
                    # Eye dots
                    eye_y2 = skull_r + 1
                    pygame.draw.circle(spr, bc, (surf_w//2 - skull_r//3, eye_y2), max(1, skull_r//4))
                    pygame.draw.circle(spr, bc, (surf_w//2 + skull_r//3, eye_y2), max(1, skull_r//4))
                    # Halo glow at top
                    for hl in range(max(2, skull_r)):
                        ha2 = int(pulse_a2 * 0.4 * (1 - hl / max(1, skull_r)))
                        pygame.draw.circle(spr, (*color, ha2),
                                           (surf_w//2, skull_r + 2), skull_r + hl, 1)

                elif icon_key == "journal":
                    # Book rectangle
                    bw, bh_ = max(4, surf_w//2), max(5, surf_h*2//3)
                    ox, oy = (surf_w-bw)//2, (surf_h-bh_)//2
                    pygame.draw.rect(spr, dim, (ox, oy, bw, bh_))
                    pygame.draw.rect(spr, c_a, (ox, oy, bw, bh_), 1)
                    pygame.draw.line(spr, c_a, (surf_w//2, oy+2), (surf_w//2, oy+bh_-2), 1)

                else:
                    # Generic: simple lit square
                    pygame.draw.rect(spr, dim, (2, 2, surf_w-4, surf_h-4), border_radius=2)
                    pygame.draw.rect(spr, c_a, (2, 2, surf_w-4, surf_h-4), 2, border_radius=2)

                view.blit(spr, (cx_s - surf_w//2, blit_y))

    def _fading_overlay(self, view):
        intensity = self.fading_intensity
        vign = pygame.Surface((VP_W, VP_H), pygame.SRCALPHA)
        pa   = int(intensity * 60 + intensity * 35 * self.pulse)
        rng  = random.Random(int(self.t * 8))
        for _ in range(int(intensity * 10)):
            x  = rng.randint(0, VP_W-1)
            ah = rng.randint(4, max(5, int(35*intensity)))
            pygame.draw.rect(vign, (0,0,0,rng.randint(5,pa)), (x,0,2,VP_H))
        for cx_, cy_ in [(0,0),(VP_W-100,0),(0,VP_H-100),(VP_W-100,VP_H-100)]:
            pygame.draw.rect(vign, (20,0,30,int(intensity*100)), (cx_,cy_,100,100))
        view.blit(vign, (0,0))

    # ─────────────────────────────────────────────────────────
    #  MINIMAP
    # ─────────────────────────────────────────────────────────

    def _draw_minimap(self, surface):
        fl    = self.dungeon.get_current_floor_data()
        tiles = fl["tiles"]
        fw, fh = fl["width"], fl["height"]
        ts = MM_TS
        cols = min(fw, MM_W // ts)
        rows = min(fh, MM_H // ts)
        px_i, py_i = int(self.px), int(self.py)
        x0 = max(0, min(px_i - cols//2, fw - cols))
        y0 = max(0, min(py_i - rows//2, fh - rows))

        bg = pygame.Surface((cols*ts, rows*ts), pygame.SRCALPHA)
        bg.fill((0,0,0,155))

        for ty in range(y0, y0+rows):
            for tx in range(x0, x0+cols):
                tile = tiles[ty][tx]
                if not tile.get("discovered"):
                    continue
                tt = tile["type"]
                if tt == DT_WALL or (tt == DT_SECRET_DOOR and not tile.get("secret_found")):
                    c = (55,50,45,220)
                elif tt == DT_DOOR:
                    c = (180,130,60,255)
                elif tt == DT_STAIRS_DOWN:
                    c = (60, 120, 255, 255)   # blue — going down (matches 3D)
                elif tt == DT_STAIRS_UP:
                    c = (255, 160, 40, 255)   # amber — going up (matches 3D)
                elif tt == DT_ENTRANCE:
                    c = (100, 220, 100, 255)  # green — dungeon exit back to overworld
                elif tt == DT_TREASURE:
                    c = (255,215,40,255)
                elif tt == DT_FLOOR and (tile.get("event") or {}).get("type") == "boss_encounter":
                    ev_be = tile.get("event") or {}
                    if not ev_be.get("triggered"):
                        c = (255, 30, 80, 255)    # bright red — boss marker
                    else:
                        c = (88, 78, 62, 200)     # floor — already triggered
                elif tt == DT_TRAP:
                    ev_t = tile.get("event") or {}
                    if ev_t.get("disarmed"):
                        c = (90, 140, 80, 220)    # green — disarmed
                    elif ev_t.get("tripped"):
                        c = (110, 100, 90, 200)   # grey — sprung
                    elif ev_t.get("detected"):
                        c = (255, 140, 0, 255)    # orange — armed and known (distinct from enemy red)
                    else:
                        c = (88, 78, 62, 200)     # floor colour — undetected trap blends in
                elif tt == DT_INTERACTABLE:
                    ev_i = tile.get("event") or {}
                    c = (80,80,75,150) if ev_i.get("used") else (80,200,255,255)
                else:
                    c = (88,78,62,200)
                sx = (tx-x0)*ts
                sy = (ty-y0)*ts
                pygame.draw.rect(bg, c, (sx,sy,ts-1,ts-1))

        # Enemy dots — only when tile is discovered AND currently in LOS
        for enemy in fl.get("enemies", []):
            if enemy.get("state") == "dead":
                continue
            ex, ey = enemy["x"], enemy["y"]
            if not tiles[ey][ex].get("discovered"):
                continue
            # Distance pre-filter (cheap) before the LOS ray cast
            edist_mm = math.sqrt((ex - px_i)**2 + (ey - py_i)**2)
            if edist_mm > TORCH_DIST:
                continue
            # LOS check — must NOT be behind a wall/door; on failure, skip
            try:
                visible = self.dungeon._has_los(fl, px_i, py_i, ex, ey)
            except Exception:
                visible = False
            if not visible:
                continue
            edx = ex - x0; edy = ey - y0
            if 0 <= edx < cols and 0 <= edy < rows:
                esx = edx * ts + ts // 2; esy = edy * ts + ts // 2
                ecol = (255, 60, 60, 255) if enemy.get("state") == "chase" else (200, 80, 80, 220)
                pygame.draw.circle(bg, ecol, (esx, esy), max(2, ts // 2 - 1))

        # Party dot + directional arrowhead (contained within tile square)
        ppx = (px_i-x0)*ts + ts//2
        ppy = (py_i-y0)*ts + ts//2
        # Arrow tip: stay within the tile (max ts//2 - 1 from centre)
        arrow_r = max(2, ts//2 - 1)
        ax  = ppx + int(math.cos(self.angle) * arrow_r)
        ay  = ppy + int(math.sin(self.angle) * arrow_r)
        # Draw filled party circle
        pygame.draw.circle(bg, (0,220,200,255), (ppx,ppy), max(2, ts//2 - 1))   # cyan — unique party color
        # Draw arrowhead triangle pointing in facing direction
        perp_x = -math.sin(self.angle)
        perp_y =  math.cos(self.angle)
        tip_x  = ppx + int(math.cos(self.angle) * arrow_r)
        tip_y  = ppy + int(math.sin(self.angle) * arrow_r)
        base_w = max(1, ts // 4)
        b1x = tip_x - int(math.cos(self.angle) * arrow_r * 0.7) + int(perp_x * base_w)
        b1y = tip_y - int(math.sin(self.angle) * arrow_r * 0.7) + int(perp_y * base_w)
        b2x = tip_x - int(math.cos(self.angle) * arrow_r * 0.7) - int(perp_x * base_w)
        b2y = tip_y - int(math.sin(self.angle) * arrow_r * 0.7) - int(perp_y * base_w)
        pygame.draw.polygon(bg, (0,220,200,255), [(tip_x,tip_y),(b1x,b1y),(b2x,b2y)])  # cyan party arrow
        pygame.draw.rect(bg, (100,90,72,200), (0,0,cols*ts,rows*ts), 1)

        surface.blit(bg, (MM_X, MM_Y))
        font = pygame.font.SysFont("courier,monospace", 14)
        lbl  = font.render(f"Floor {self.dungeon.current_floor}", True, (170,160,130))
        surface.blit(lbl, (MM_X+2, MM_Y+rows*ts+2))

    # ─────────────────────────────────────────────────────────
    #  HUD
    # ─────────────────────────────────────────────────────────

    def _draw_hud(self, surface, mx, my):
        by = SCREEN_H - HUD_H
        pygame.draw.rect(surface, (14,11,8), (0, by, SCREEN_W, HUD_H))
        pygame.draw.line(surface, GOLD, (0, by), (SCREEN_W, by), 2)

        fb = pygame.font.SysFont("courier,consolas,monospace", 16, bold=True)
        fs = pygame.font.SysFont("courier,consolas,monospace", 14)

        party = self.dungeon.party
        if party:
            PORTRAIT_W = 48
            col_w = min(195, VP_W // max(1, len(party)))
            for i, ch in enumerate(party):
                cx_h = 8 + i*col_w
                cy_h = by + 4

                # Class portrait — small silhouette to the left of the text block
                try:
                    from ui.pixel_art import draw_character_silhouette
                    port_rect = pygame.Rect(cx_h, cy_h, PORTRAIT_W, HUD_H - 12)
                    pygame.draw.rect(surface, (22, 18, 12), port_rect)
                    pygame.draw.rect(surface, (55, 44, 30), port_rect, 1)
                    draw_character_silhouette(surface, port_rect, ch.class_name)
                except Exception:
                    pass
                text_x = cx_h + PORTRAIT_W + 4

                surface.blit(fb.render(ch.name[:10], True, GOLD), (text_x, cy_h))
                cy_h += 16
                # Get resources
                try:
                    from core.classes import get_all_resources
                    max_res = get_all_resources(ch.class_name, ch.stats, ch.level)
                except Exception:
                    max_res = {}
                bar_w   = max(10, col_w - PORTRAIT_W - 20)
                cur_hp  = ch.resources.get("HP", 0)
                max_hp  = max(1, max_res.get("HP", cur_hp) or cur_hp)
                hw = max(0, int((cur_hp/max_hp)*bar_w))
                pygame.draw.rect(surface, (55,12,12),  (text_x, cy_h, bar_w, 7))
                pygame.draw.rect(surface, (185,38,38), (text_x, cy_h, hw, 7))
                surface.blit(fs.render(f"{cur_hp}/{max_hp}", True, (190,150,145)), (text_x, cy_h+8))
                # All secondary resources (MP, SP, Ki, etc.) — each with bar + cur/max
                res_keys = [k for k in ch.resources if k != "HP"]
                RES_COLORS = {
                    "MP":  ((12,12,55),  (45,75,205),  (130,140,215)),
                    "SP":  ((40,30,10),  (200,160,40), (210,180,80)),
                    "Ki":  ((10,35,20),  (40,160,80),  (100,200,130)),
                    "EP":  ((35,10,35),  (150,60,180), (180,120,210)),
                }
                for rk in res_keys[:2]:  # max 2 secondary resources shown
                    cy_h += 20
                    cur_r  = ch.resources.get(rk, 0)
                    max_r  = max(1, max_res.get(rk, cur_r) or cur_r)
                    mw     = max(0, int((cur_r/max_r)*bar_w))
                    bg_c, fill_c, text_c = RES_COLORS.get(rk, ((20,20,20),(100,100,200),(160,160,220)))
                    pygame.draw.rect(surface, bg_c,   (text_x, cy_h, bar_w, 7))
                    pygame.draw.rect(surface, fill_c, (text_x, cy_h, mw, 7))
                    surface.blit(fs.render(f"{rk}: {cur_r}/{max_r}", True, text_c), (text_x, cy_h+8))

        # Buttons — placed on right side of HUD to avoid overlapping char cards
        # char cards span x=8 to ~x=1100; buttons go from x=1108 rightward
        _btn_x = SCREEN_W - 360
        bdata = [
            ("C Camp",   pygame.Rect(_btn_x,       by + 4, 100, 24)),
            ("M Menu",   pygame.Rect(_btn_x + 110, by + 4, 100, 24)),
            ("T Disarm", pygame.Rect(_btn_x + 220, by + 4, 110, 24)),
        ]
        for lbl, r in bdata:
            hov = r.collidepoint(mx,my)
            pygame.draw.rect(surface, (40,30,18) if not hov else (62,46,24), r, border_radius=3)
            pygame.draw.rect(surface, GOLD if hov else (75,60,38), r, 1, border_radius=3)
            surface.blit(fb.render(lbl, True, GOLD if hov else CREAM), (r.x+6, r.y+5))

        info_text = f"{self.dungeon.dungeon_id.replace('_',' ').title()}  ·  Floor {self.dungeon.current_floor}/{self.dungeon.total_floors}"
        # Add tier badge if party has advanced beyond Bronze
        if self.dungeon.party:
            from core.progression import PLANAR_TIERS
            tier_idx = max((getattr(c, "planar_tier", 0) for c in self.dungeon.party), default=0)
            if tier_idx > 0:
                t = PLANAR_TIERS[tier_idx]
                info_text += f"  {t['symbol']} {t['name']}"
        info = fb.render(info_text,
            True, (150,138,110))
        surface.blit(info, (SCREEN_W - info.get_width() - 10, by + HUD_H - 28))

        ctrl = fs.render("WASD Move  QE/←→ Turn  ENTER Interact  C Camp  T Disarm", True, (72,64,50))
        surface.blit(ctrl, (VP_X+4, by+3))

    # ─────────────────────────────────────────────────────────
    #  DIALOGS
    # ─────────────────────────────────────────────────────────

    def _draw_chest_modal(self, surface, mx, my):
        """Render the multi-step chest interaction modal."""
        m = self.chest_modal
        if not m:
            return

        # ── Layout ────────────────────────────────────────────
        dw, dh = 520, 300
        dx = SCREEN_W // 2 - dw // 2
        dy = SCREEN_H // 2 - dh // 2

        # Backdrop
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        surface.blit(overlay, (0, 0))

        pygame.draw.rect(surface, (20, 14, 8), (dx, dy, dw, dh), border_radius=6)
        pygame.draw.rect(surface, GOLD, (dx, dy, dw, dh), 2, border_radius=6)

        ft  = pygame.font.SysFont("courier,monospace", 18, bold=True)
        fm  = pygame.font.SysFont("courier,monospace", 14)
        fsm = pygame.font.SysFont("courier,monospace", 12)

        def btn_rect(col, row, n_cols=2):
            bw = (dw - 60) // n_cols - 8
            bh = 36
            bx = dx + 30 + col * (bw + 8)
            by = dy + dh - 56 + row * 44
            return pygame.Rect(bx, by, bw, bh)

        def draw_btn(rect, label, enabled=True, danger=False):
            if not enabled:
                col_bg, col_bd, col_tx = (22, 18, 14), (40, 32, 20), GREY
            elif rect.collidepoint(mx, my):
                col_bg = (100, 30, 20) if danger else (70, 50, 18)
                col_bd, col_tx = (220, 60, 40) if danger else GOLD, GOLD
            else:
                col_bg = (55, 18, 12) if danger else (38, 28, 14)
                col_bd = (180, 50, 30) if danger else (70, 55, 32)
                col_tx = (220, 80, 60) if danger else GOLD
            pygame.draw.rect(surface, col_bg, rect, border_radius=3)
            pygame.draw.rect(surface, col_bd, rect, 1, border_radius=3)
            t = fm.render(label, True, col_tx)
            surface.blit(t, (rect.x + rect.w // 2 - t.get_width() // 2,
                             rect.y + rect.h // 2 - t.get_height() // 2))

        step = m["step"]
        trap = m["chest_ev"].get("trap")
        has_trap = bool(trap and not trap.get("disarmed"))

        # ── Step: APPROACH ─────────────────────────────────────
        if step == "approach":
            title = "A Chest!" if not has_trap else "A Chest!"
            t = ft.render(title, True, GOLD)
            surface.blit(t, (dx + dw // 2 - t.get_width() // 2, dy + 14))

            # Chest description line
            trap_hint = ""
            if trap and trap.get("detected"):
                trap_hint = f"  ⚠  Trapped: {trap['name']}"
            elif trap:
                trap_hint = "  (trap status unknown)"

            lines = [
                "You approach the chest.",
                trap_hint,
                "What does the party do?",
            ]
            for i, ln in enumerate(lines):
                if not ln:
                    continue
                col = (220, 80, 60) if "Trapped" in ln else CREAM
                s = fm.render(ln, True, col)
                surface.blit(s, (dx + 20, dy + 52 + i * 22))

            # Buttons: Search | Open | Leave
            b_search = btn_rect(0, 0, 3)
            b_open   = btn_rect(1, 0, 3)
            b_leave  = btn_rect(2, 0, 3)
            draw_btn(b_search, "Search")
            open_label = "Force Open" if (trap and trap.get("detected") and not trap.get("disarmed")) else "Open"
            draw_btn(b_open, open_label, danger=(trap and trap.get("detected") and not trap.get("disarmed")))
            draw_btn(b_leave, "Leave")
            m["_btns"] = {"search": b_search, "open": b_open, "leave": b_leave}

        # ── Step: PICK SEARCHER ────────────────────────────────
        elif step == "pick_searcher":
            t = ft.render("Who searches for traps?", True, GOLD)
            surface.blit(t, (dx + dw // 2 - t.get_width() // 2, dy + 14))
            hint = fm.render("Thieves & Rangers have higher detection skill.", True, CREAM)
            surface.blit(hint, (dx + dw // 2 - hint.get_width() // 2, dy + 44))

            party = self.dungeon.party
            btn_rects = {}
            for i, ch in enumerate(party):
                col_i = i % 2
                row_i = i // 2
                bw, bh = (dw - 60) // 2 - 6, 46
                bx = dx + 28 + col_i * (bw + 8)
                by = dy + 80 + row_i * (bh + 6)
                br = pygame.Rect(bx, by, bw, bh)
                hov = br.collidepoint(mx, my)
                bg = (55, 40, 18) if hov else (28, 22, 12)
                bd = GOLD if hov else (60, 48, 24)
                pygame.draw.rect(surface, bg, br, border_radius=3)
                pygame.draw.rect(surface, bd, br, 1, border_radius=3)
                # Name + class
                name_t = fm.render(ch.name, True, GOLD)
                cls_t  = fsm.render(f"{ch.class_name}  DEX:{ch.stats.get('DEX',0)}  WIS:{ch.stats.get('WIS',0)}", True, CREAM)
                surface.blit(name_t, (bx + 8, by + 4))
                surface.blit(cls_t, (bx + 8, by + 22))
                btn_rects[i] = br

            # Back button
            b_back = pygame.Rect(dx + dw // 2 - 60, dy + dh - 52, 120, 34)
            draw_btn(b_back, "Back")
            btn_rects["back"] = b_back
            m["_btns"] = btn_rects

        # ── Step: SEARCH RESULT ────────────────────────────────
        elif step == "search_result":
            found   = m.get("search_found", False)
            roll    = m.get("search_roll", 0)
            needed  = m.get("search_needed", 0)
            searcher = m.get("searcher_name", "")
            no_trap_on_chest = (needed == 0)   # search_chest_for_traps returns (False,0,0) if no trap exists

            t_title = "Trap Found!" if found else ("No Trap Exists" if no_trap_on_chest else "Nothing Found")
            col_title = (220, 80, 60) if found else (100, 220, 100)
            t = ft.render(t_title, True, col_title)
            surface.blit(t, (dx + dw // 2 - t.get_width() // 2, dy + 14))

            if no_trap_on_chest:
                result_line = f"{searcher} found no trap mechanism on this chest."
            else:
                result_line = f"{searcher} rolled {roll} (needed ≤{needed})"
            lines = [result_line]
            if found:
                lines.append(f"Trap: {trap['name']}  —  Tier {trap.get('tier',1)}")
                lines.append("What does the party do?")
            elif no_trap_on_chest:
                lines.append("This chest carries no trap. Safe to open.")
                lines.append("What does the party do?")
            else:
                lines.append("No trap detected. The chest looks safe.")
                lines.append("(There may still be one — they're not always visible.)")
                lines.append("What does the party do?")
            for i, ln in enumerate(lines):
                col = (220, 80, 60) if "Trap:" in ln else CREAM
                s = fm.render(ln, True, col)
                surface.blit(s, (dx + 20, dy + 52 + i * 22))

            if found:
                b_disarm = btn_rect(0, 0, 3)
                b_force  = btn_rect(1, 0, 3)
                b_leave  = btn_rect(2, 0, 3)
                draw_btn(b_disarm, "Disarm")
                draw_btn(b_force, "Force Open", danger=True)
                draw_btn(b_leave, "Leave")
                m["_btns"] = {"disarm": b_disarm, "force": b_force, "leave": b_leave}
            else:
                b_open  = btn_rect(0, 0, 2)
                b_leave = btn_rect(1, 0, 2)
                draw_btn(b_open, "Open")
                draw_btn(b_leave, "Leave")
                m["_btns"] = {"open": b_open, "leave": b_leave}

        # ── Step: PICK DISARMER ────────────────────────────────
        elif step == "pick_disarmer":
            t = ft.render("Who attempts to disarm?", True, GOLD)
            surface.blit(t, (dx + dw // 2 - t.get_width() // 2, dy + 14))
            trap_line = fm.render(f"Trap: {trap['name']}", True, (220, 80, 60))
            surface.blit(trap_line, (dx + dw // 2 - trap_line.get_width() // 2, dy + 44))

            party = self.dungeon.party
            btn_rects = {}
            for i, ch in enumerate(party):
                col_i = i % 2
                row_i = i // 2
                bw, bh = (dw - 60) // 2 - 6, 46
                bx = dx + 28 + col_i * (bw + 8)
                by = dy + 80 + row_i * (bh + 6)
                br = pygame.Rect(bx, by, bw, bh)
                hov = br.collidepoint(mx, my)
                bg = (55, 40, 18) if hov else (28, 22, 12)
                bd = GOLD if hov else (60, 48, 24)
                pygame.draw.rect(surface, bg, br, border_radius=3)
                pygame.draw.rect(surface, bd, br, 1, border_radius=3)
                name_t = fm.render(ch.name, True, GOLD)
                cls_t  = fsm.render(f"{ch.class_name}  DEX:{ch.stats.get('DEX',0)}", True, CREAM)
                surface.blit(name_t, (bx + 8, by + 4))
                surface.blit(cls_t, (bx + 8, by + 22))
                btn_rects[i] = br

            b_back = pygame.Rect(dx + dw // 2 - 60, dy + dh - 52, 120, 34)
            draw_btn(b_back, "Back")
            btn_rects["back"] = b_back
            m["_btns"] = btn_rects

        # ── Step: DISARM RESULT ────────────────────────────────
        elif step == "disarm_result":
            success  = m.get("disarm_success", False)
            roll     = m.get("disarm_roll", 0)
            needed   = m.get("disarm_needed", 0)
            disarmer = m.get("disarmer_name", "")
            t_title  = "Trap Disarmed!" if success else "Disarm Failed!"
            col_title = (100, 220, 100) if success else (220, 80, 60)
            t = ft.render(t_title, True, col_title)
            surface.blit(t, (dx + dw // 2 - t.get_width() // 2, dy + 14))

            result_line = f"{disarmer} rolled {roll} (needed ≤{needed})"
            lines = [result_line]
            if success:
                lines.append("The trap is safely disarmed.")
                lines.append("You may now open the chest.")
            else:
                lines.append("The trap fires!")
            for i, ln in enumerate(lines):
                s = fm.render(ln, True, CREAM)
                surface.blit(s, (dx + 20, dy + 52 + i * 22))

            if success:
                b_open = btn_rect(0, 0, 2)
                b_leave = btn_rect(1, 0, 2)
                draw_btn(b_open, "Open Chest")
                draw_btn(b_leave, "Leave")
                m["_btns"] = {"open": b_open, "leave": b_leave}
            else:
                # Trap fires — only a dismiss button, main.py handles damage
                b_ok = btn_rect(0, 0, 1)
                draw_btn(b_ok, "Continue", danger=True)
                m["_btns"] = {"continue_trap": b_ok}

    def _draw_confirm_dialog(self, surface, mx, my, title, msg, yes_lbl, no_lbl, tag):

        dw, dh = 400, 160
        dx = SCREEN_W//2 - dw//2
        dy = SCREEN_H//2 - dh//2
        pygame.draw.rect(surface, (20,16,10), (dx,dy,dw,dh), border_radius=6)
        pygame.draw.rect(surface, GOLD, (dx,dy,dw,dh), 2, border_radius=6)
        ft = pygame.font.SysFont("courier,monospace", 18, bold=True)
        fb = pygame.font.SysFont("courier,monospace", 13)
        t  = ft.render(title, True, GOLD)
        surface.blit(t, (dx+dw//2-t.get_width()//2, dy+12))
        m  = fb.render(msg, True, CREAM)
        surface.blit(m, (dx+dw//2-m.get_width()//2, dy+44))
        yb = pygame.Rect(dx+40, dy+dh-48, 120, 34)
        nb = pygame.Rect(dx+dw-160, dy+dh-48, 120, 34)
        for btn, lbl in [(yb,yes_lbl),(nb,no_lbl)]:
            hov = btn.collidepoint(mx,my)
            pygame.draw.rect(surface, (70,48,18) if hov else (38,28,14), btn, border_radius=3)
            pygame.draw.rect(surface, GOLD if hov else (70,55,32), btn, 1, border_radius=3)
            bt = fb.render(lbl, True, GOLD)
            surface.blit(bt, (btn.x+btn.w//2-bt.get_width()//2, btn.y+btn.h//2-bt.get_height()//2))

    def _draw_events(self, surface):
        font   = pygame.font.SysFont("courier,monospace", 15, bold=True)
        base_y = VP_Y + VP_H - 70
        for i, (msg, col, timer) in enumerate(reversed(list(self.event_queue[-4:]))):
            alpha  = min(255, int(timer/300*255))
            ts = font.render(msg, True, col)
            tw, th = ts.get_width(), ts.get_height()
            tx = VP_X + VP_W//2 - tw//2
            ty = base_y - i*22
            # Dark backdrop for readability
            pad = 4
            bg = pygame.Surface((tw + pad*2, th + pad), pygame.SRCALPHA)
            bg.fill((0, 0, 0, min(180, alpha)))
            surface.blit(bg, (tx - pad, ty - 1))
            ts.set_alpha(alpha)
            surface.blit(ts, (tx, ty))

    # ─────────────────────────────────────────────────────────
    #  INPUT
    # ─────────────────────────────────────────────────────────

    def _process_held_keys(self, ds):
        """Animate in-progress move/turn. Called every frame."""
        if self.show_camp_confirm or self.show_stairs_confirm or self.chest_modal:
            return

        MOVE_DUR = 0.12   # seconds to slide one tile
        TURN_DUR = 0.10   # seconds to snap 90°

        # Animate position
        if self._move_anim_t < 1.0:
            self._move_anim_t = min(1.0, self._move_anim_t + ds / MOVE_DUR)
            t = self._ease(self._move_anim_t)
            self.px = self._move_start_x + (self._move_target_x - self._move_start_x) * t
            self.py = self._move_start_y + (self._move_target_y - self._move_start_y) * t

        # Animate turn
        if self._turn_anim_t < 1.0:
            self._turn_anim_t = min(1.0, self._turn_anim_t + ds / TURN_DUR)
            t = self._ease(self._turn_anim_t)
            self.angle = self._turn_start + (self._turn_target - self._turn_start) * t
            self._recalc_camera()

        # Reduce input cooldown
        if self._step_cooldown > 0:
            self._step_cooldown = max(0.0, self._step_cooldown - ds)

    @staticmethod
    def _ease(t):
        """Smooth step easing."""
        return t * t * (3 - 2 * t)

    def _grid_step(self, key):
        """Handle a single discrete movement or turn keypress."""
        if self.show_camp_confirm or self.show_stairs_confirm or self.chest_modal:
            return
        if self._step_cooldown > 0:
            return

        COOLDOWN = 0.13   # min seconds between steps

        import math as _m
        TWO_PI = 2 * _m.pi

        # Snap current angle to nearest 90° before computing direction
        snapped = round(self.angle / (_m.pi / 2)) * (_m.pi / 2)
        fdx = round(_m.cos(snapped))   # -1, 0, or 1
        fdy = round(_m.sin(snapped))

        moved = False

        if key in (pygame.K_UP, pygame.K_w):
            # Move forward — route through dungeon.move() so fog/encounters work
            event = self.dungeon.move(fdx, fdy)
            tx, ty = self.dungeon.party_x, self.dungeon.party_y
            if tx != int(self.px) or ty != int(self.py):
                self._move_start_x = self.px
                self._move_start_y = self.py
                self._move_target_x = tx + 0.5
                self._move_target_y = ty + 0.5
                self._move_anim_t = 0.0
                moved = True
            if event:
                self._pending_event = event

        elif key in (pygame.K_DOWN, pygame.K_s):
            # Move backward — route through dungeon.move()
            event = self.dungeon.move(-fdx, -fdy)
            tx, ty = self.dungeon.party_x, self.dungeon.party_y
            if tx != int(self.px) or ty != int(self.py):
                self._move_start_x = self.px
                self._move_start_y = self.py
                self._move_target_x = tx + 0.5
                self._move_target_y = ty + 0.5
                self._move_anim_t = 0.0
                moved = True
            if event:
                self._pending_event = event

        elif key in (pygame.K_LEFT, pygame.K_q, pygame.K_a):
            # Turn left 90°
            self._turn_start  = self.angle
            self._turn_target = self.angle - _m.pi / 2
            self._turn_anim_t = 0.0
            moved = True

        elif key in (pygame.K_RIGHT, pygame.K_e, pygame.K_d):
            # Turn right 90°
            self._turn_start  = self.angle
            self._turn_target = self.angle + _m.pi / 2
            self._turn_anim_t = 0.0
            moved = True

        if moved:
            self._step_cooldown = COOLDOWN

    def handle_key(self, key):
        movement_keys = (
            pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,
            pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d,
            pygame.K_q, pygame.K_e,
        )
        if key in movement_keys:
            self._grid_step(key)
            # Return any dungeon event (encounter, stairs, trap, etc.)
            ev = self._pending_event
            self._pending_event = None
            return ev

        # ESC dismisses any active modal/confirm first
        if key == pygame.K_ESCAPE:
            if self.show_stairs_confirm:
                self.show_stairs_confirm = False
                return None
            if self.show_camp_confirm:
                self.show_camp_confirm = False
                return None
            if self.chest_modal:
                step = self.chest_modal.get("step", "approach")
                if step in ("pick_searcher",):
                    self.chest_modal["step"] = "approach"
                elif step in ("pick_disarmer",):
                    self.chest_modal["step"] = "search_result"
                elif step in ("approach", "search_result", "disarm_result"):
                    self.chest_modal = None
                else:
                    self.chest_modal = None
                return None
            return None

        if self.show_camp_confirm or self.show_stairs_confirm or self.chest_modal:
            return None

        if key == pygame.K_RETURN:
            tile = self.dungeon.get_tile(self.dungeon.party_x, self.dungeon.party_y)
            if tile:
                tt = tile["type"]
                if tt == DT_STAIRS_DOWN:
                    self.show_stairs_confirm = True; self.stairs_direction = "down"
                elif tt in (DT_STAIRS_UP, DT_ENTRANCE):
                    self.show_stairs_confirm = True
                    self.stairs_direction = "exit" if self.dungeon.current_floor == 1 else "up"
            return None
        if key == pygame.K_c:
            self.show_camp_confirm = True; return None
        if key == pygame.K_t:
            return self._try_disarm()
        return None

    def handle_keyup(self, key):
        pass   # no held-key state in grid-snap mode

    def handle_keyup(self, key):
        self._keys.discard(key)

    def handle_click(self, mx, my):
        dw, dh = 400, 160
        dx = SCREEN_W//2 - dw//2
        dy = SCREEN_H//2 - dh//2
        yb = pygame.Rect(dx+40, dy+dh-48, 120, 34)
        nb = pygame.Rect(dx+dw-160, dy+dh-48, 120, 34)

        if self.show_stairs_confirm:
            if yb.collidepoint(mx,my):
                self.show_stairs_confirm = False
                if self.stairs_direction == "down":   return {"type":"stairs_down"}
                elif self.stairs_direction == "up":   return {"type":"stairs_up"}
                else:                                 return {"type":"exit_dungeon"}
            elif nb.collidepoint(mx,my):
                self.show_stairs_confirm = False
            return None

        if self.show_camp_confirm:
            if yb.collidepoint(mx,my):
                self.show_camp_confirm = False; return {"type":"camp"}
            elif nb.collidepoint(mx,my):
                self.show_camp_confirm = False
            return None

        if self.chest_modal:
            return self._handle_chest_modal_click(mx, my)

        by = SCREEN_H - HUD_H
        _btn_x = SCREEN_W - 360
        if pygame.Rect(_btn_x,       by + 4, 100, 24).collidepoint(mx,my):
            return {"type": "camp"}
        if pygame.Rect(_btn_x + 110, by + 4, 100, 24).collidepoint(mx,my):
            return {"type": "menu"}
        if pygame.Rect(_btn_x + 220, by + 4, 110, 24).collidepoint(mx,my):
            return self._try_disarm()
        return None

    def _handle_chest_modal_click(self, mx, my):
        """Process clicks inside the chest modal. Returns event dict or None."""
        m = self.chest_modal
        btns = m.get("_btns", {})
        step = m["step"]
        chest_ev = m["chest_ev"]

        # ── APPROACH ──────────────────────────────────────────
        if step == "approach":
            if btns.get("leave") and btns["leave"].collidepoint(mx, my):
                self.chest_modal = None
                return None
            if btns.get("search") and btns["search"].collidepoint(mx, my):
                m["step"] = "pick_searcher"
                return None
            if btns.get("open") and btns["open"].collidepoint(mx, my):
                # Force open — fires trap if present and not disarmed
                trap = chest_ev.get("trap")
                if trap and not trap.get("disarmed"):
                    self.chest_modal = None
                    # Fire the trap immediately
                    return {"type": "chest_trap_fire", "trap_data": trap, "chest_ev": chest_ev}
                # Safe open
                self.chest_modal = None
                return {"type": "chest_open", "chest_ev": chest_ev}

        # ── PICK SEARCHER ──────────────────────────────────────
        elif step == "pick_searcher":
            if btns.get("back") and btns["back"].collidepoint(mx, my):
                m["step"] = "approach"
                return None
            for i, ch in enumerate(self.dungeon.party):
                if i in btns and btns[i].collidepoint(mx, my):
                    found, roll, needed = self.dungeon.search_chest_for_traps(chest_ev, ch)
                    m["step"]          = "search_result"
                    m["search_found"]  = found
                    m["search_roll"]   = roll
                    m["search_needed"] = needed
                    m["searcher_name"] = ch.name
                    return None

        # ── SEARCH RESULT ──────────────────────────────────────
        elif step == "search_result":
            if btns.get("leave") and btns["leave"].collidepoint(mx, my):
                self.chest_modal = None
                return None
            if btns.get("open") and btns["open"].collidepoint(mx, my):
                self.chest_modal = None
                return {"type": "chest_open", "chest_ev": chest_ev}
            if btns.get("disarm") and btns["disarm"].collidepoint(mx, my):
                m["step"] = "pick_disarmer"
                return None
            if btns.get("force") and btns["force"].collidepoint(mx, my):
                trap = chest_ev.get("trap")
                self.chest_modal = None
                return {"type": "chest_trap_fire", "trap_data": trap, "chest_ev": chest_ev}

        # ── PICK DISARMER ──────────────────────────────────────
        elif step == "pick_disarmer":
            if btns.get("back") and btns["back"].collidepoint(mx, my):
                m["step"] = "search_result"
                return None
            for i, ch in enumerate(self.dungeon.party):
                if i in btns and btns[i].collidepoint(mx, my):
                    success, roll, needed = self.dungeon.disarm_chest_trap(chest_ev, ch)
                    m["step"]           = "disarm_result"
                    m["disarm_success"] = success
                    m["disarm_roll"]    = roll
                    m["disarm_needed"]  = needed
                    m["disarmer_name"]  = ch.name
                    return None

        # ── DISARM RESULT ──────────────────────────────────────
        elif step == "disarm_result":
            if btns.get("leave") and btns["leave"].collidepoint(mx, my):
                self.chest_modal = None
                return None
            if btns.get("open") and btns["open"].collidepoint(mx, my):
                self.chest_modal = None
                return {"type": "chest_open", "chest_ev": chest_ev}
            if btns.get("continue_trap") and btns["continue_trap"].collidepoint(mx, my):
                trap = chest_ev.get("trap")
                self.chest_modal = None
                return {"type": "chest_trap_fire", "trap_data": trap, "chest_ev": chest_ev}

        return None


    def _try_disarm(self):
        px, py = self.dungeon.party_x, self.dungeon.party_y
        for ddx, ddy in [(0,-1),(0,1),(-1,0),(1,0)]:
            tile = self.dungeon.get_tile(px+ddx, py+ddy)
            if tile and tile["type"] == DT_TRAP:
                ev = tile.get("event") or {}
                if ev.get("detected") and not ev.get("disarmed"):
                    if self.dungeon.disarm_trap(px+ddx, py+ddy):
                        self.show_event("Trap disarmed!", (100,255,100))
                    else:
                        return {"type":"trap","data":ev}
                    return None
        self.show_event("No detected trap nearby.", CREAM)
        return None

    def show_event(self, msg, color=CREAM):
        self.event_message = msg
        self.event_color   = color
        self.event_timer   = 3500
        self.event_queue.append((msg, color, 3500))

    @property
    def facing(self):
        a = self.angle % (2 * math.pi)
        if a < 0: a += 2 * math.pi
        return int((a + math.pi/4) / (math.pi/2)) % 4

    @facing.setter
    def facing(self, v):
        self.angle = v * math.pi / 2
        self._recalc_camera()

