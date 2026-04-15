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
from ui.renderer import SCREEN_W, SCREEN_H, CREAM, GOLD, get_font
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
MM_H    = 390          # taller — uses more of the right-column space
MM_TS   = 9            # larger tiles — much easier to read

NUM_RAYS    = VP_W
FOV         = math.radians(66)
HALF_FOV    = FOV / 2
PROJ_DIST   = (VP_W / 2) / math.tan(HALF_FOV)

MOVE_SPEED  = 3.5
ROT_SPEED   = 2.2
TORCH_DIST  = 11.0         # brighter — extends visible range

# ═══════════════════════════════════════════════════════════════
#  DUNGEON THEMES
# ═══════════════════════════════════════════════════════════════

THEMES = {
    "cave":   ((110,90,70),  (45,35,26),  (55,45,34),  (18,14,10), (220,145,55), (12,8,6)  ),
    "spider": ((62,58,54),   (24,20,18),  (30,26,22),  (8,7,6),    (180,170,140),(6,5,4)   ),
    "mine":   ((120,100,75), (55,42,30),  (65,52,38),  (20,15,10), (240,175,65), (14,10,6) ),
    "crypt":  ((80,88,120),  (32,36,55),  (38,42,65),  (12,12,22), (100,130,210),(8,8,16)  ),
    "ruins":  ((115,95,72),  (50,40,30),  (62,50,38),  (18,13,9),  (225,160,55), (12,9,6)  ),
    "tower":  ((90,82,130),  (38,34,62),  (48,44,78),  (14,12,24), (145,115,230),(8,6,18)  ),
}

# ═══════════════════════════════════════════════════════════════
#  WALL TEXTURE GENERATOR
# ═══════════════════════════════════════════════════════════════

TEX_W, TEX_H = 64, 64
NUM_WALL_VARIANTS = 3   # variants per theme — assigned per tile coordinate hash

# ── Variant generators ───────────────────────────────────────────

def _gen_door_texture(theme_id="cave", wall_light=(110,90,70), wall_dark=(45,35,26)):
    """Generate a door texture appropriate for the given dungeon theme.

    Styles:
      cave  — banded wood planks with iron straps (goblin warren)
      mine  — heavy timber frame with cross-brace, iron bolts
      crypt — cut-stone pointed arch, iron-studded oak door
      ruins — crumbling stone round arch, weathered wood
      tower — narrow pointed arch, void-tinted stone surround
    Web / spider theme is handled in _gen_theme_textures via wall variant.
    """
    surf = pygame.Surface((TEX_W, TEX_H))
    rng  = random.Random(hash(("door", theme_id)) & 0xFFFFFFFF)

    if theme_id == "mine":
        # Heavy timber frame door — plank fill + thick frame + cross-brace
        WOOD   = (95, 62, 28)
        DARK   = (58, 36, 14)
        FRAME  = (72, 46, 18)
        IRON   = (55, 55, 60)
        surf.fill(DARK)
        # Vertical planks
        for px in range(2, TEX_W - 2, 7):
            tone = rng.uniform(0.88, 1.12)
            c = tuple(min(255, int(v * tone)) for v in WOOD)
            pygame.draw.rect(surf, c, (px, 2, 5, TEX_H - 4))
        # Plank shading (right edge of each plank)
        for px in range(2, TEX_W - 2, 7):
            pygame.draw.line(surf, DARK, (px + 5, 2), (px + 5, TEX_H - 4), 1)
        # Cross-brace (Z-brace)
        pygame.draw.line(surf, DARK,  (2, TEX_H//4),     (TEX_W-2, TEX_H*3//4), 3)
        pygame.draw.line(surf, DARK,  (2, TEX_H*3//4),   (TEX_W-2, TEX_H//4),   3)
        pygame.draw.line(surf, FRAME, (2, TEX_H//4 - 1), (TEX_W-2, TEX_H*3//4 - 1), 1)
        # Thick timber frame around the whole door
        pygame.draw.rect(surf, FRAME, (0, 0, TEX_W, 5))        # top beam
        pygame.draw.rect(surf, FRAME, (0, TEX_H-5, TEX_W, 5))  # bottom sill
        pygame.draw.rect(surf, FRAME, (0, 0, 5, TEX_H))        # left post
        pygame.draw.rect(surf, FRAME, (TEX_W-5, 0, 5, TEX_H))  # right post
        # Highlight top edge of beams
        pygame.draw.rect(surf, WOOD,  (0, 0, TEX_W, 1))
        pygame.draw.rect(surf, WOOD,  (0, 0, 1, TEX_H))
        # Iron bolt heads at frame corners and mid-points
        for bx, by in [(5,5),(TEX_W-8,5),(5,TEX_H-8),(TEX_W-8,TEX_H-8),
                       (TEX_W//2-2, 3),(TEX_W//2-2, TEX_H-7)]:
            pygame.draw.rect(surf, IRON, (bx, by, 4, 4))
            pygame.draw.rect(surf, (70,70,75), (bx+1, by+1, 2, 2))
        # Handle
        pygame.draw.rect(surf, IRON, (TEX_W-12, TEX_H//2-5, 5, 10))
        pygame.draw.rect(surf, (75,75,80), (TEX_W-11, TEX_H//2-4, 3, 8))

    elif theme_id in ("crypt", "ruins", "tower"):
        # Stone arch doorway — carved stone surround, arched opening, door recessed
        arch_r  = TEX_W // 2 - 2          # arch radius
        arch_cx = TEX_W // 2              # arch centre x
        arch_cy = TEX_H // 2 - arch_r + 2 # arch centre y (door top)
        door_top = arch_cy

        STONE  = wall_light
        MORTAR = tuple(max(0, int(v * 0.4)) for v in wall_dark)
        RECESSED = tuple(max(0, int(v * 0.55)) for v in wall_light)
        WOOD   = (85, 52, 22) if theme_id != "tower" else (48, 34, 62)
        IRON   = (52, 52, 58)

        # Stone wall fill
        BLOCK_H, BLOCK_W = 10, 20
        surf.fill(MORTAR)
        for row in range(TEX_H // BLOCK_H + 2):
            oy = row * BLOCK_H
            offset = (BLOCK_W // 2) if row % 2 else 0
            for col in range(-1, TEX_W // BLOCK_W + 2):
                ox = col * BLOCK_W + offset
                tone = 0.82 + rng.random() * 0.24
                c = tuple(min(255, int(v * tone)) for v in STONE)
                rx = max(0, ox+1); ry = max(0, oy+1)
                rw = min(BLOCK_W-2, TEX_W-rx); rh = min(BLOCK_H-2, TEX_H-ry)
                if rw > 0 and rh > 0:
                    pygame.draw.rect(surf, c, (rx, ry, rw, rh))

        # Carve arched opening (fill with dark recess)
        for y in range(TEX_H):
            for x in range(TEX_W):
                in_rect = (x >= 4 and x < TEX_W-4 and y >= door_top and y < TEX_H)
                in_arch = False
                if y < door_top:
                    dx = x - arch_cx; dy = y - arch_cy
                    in_arch = (dx*dx + dy*dy) <= arch_r*arch_r
                if in_rect or in_arch:
                    surf.set_at((x, y), RECESSED)

        # Draw the door itself inside the opening
        door_l, door_r = 5, TEX_W - 5
        for px in range(door_l, door_r, 6):
            tone = rng.uniform(0.88, 1.10)
            c = tuple(min(255, int(v * tone)) for v in WOOD)
            pygame.draw.line(surf, c, (px, door_top), (px, TEX_H - 1))
        # Horizontal door rails
        for py in [door_top + (TEX_H - door_top)//3, door_top + (TEX_H - door_top)*2//3]:
            pygame.draw.rect(surf, tuple(max(0,v-20) for v in WOOD), (door_l, py-2, door_r-door_l, 4))
            pygame.draw.rect(surf, tuple(min(255,v+15) for v in WOOD),(door_l, py-3, door_r-door_l, 1))

        # Arch voussoir lines (keystone joint marks)
        for angle_deg in range(-60, 62, 15):
            import math
            ang = math.radians(angle_deg - 90)
            ix = int(arch_cx + (arch_r-1) * math.cos(ang))
            iy = int(arch_cy + (arch_r-1) * math.sin(ang))
            ox = int(arch_cx + (arch_r+4) * math.cos(ang))
            oy = int(arch_cy + (arch_r+4) * math.sin(ang))
            pygame.draw.line(surf, MORTAR, (ix,iy), (ox,oy), 1)

        # Iron ring pull
        pygame.draw.circle(surf, IRON, (TEX_W//2, TEX_H*2//3), 4, 2)
        pygame.draw.circle(surf, (68,68,72), (TEX_W//2, TEX_H*2//3), 3, 1)

        # Tower-specific: faint void tint on arch frame
        if theme_id == "tower":
            void_surf = pygame.Surface((TEX_W, TEX_H), pygame.SRCALPHA)
            pygame.draw.circle(void_surf, (90, 40, 180, 35), (arch_cx, arch_cy), arch_r + 5, 4)
            surf.blit(void_surf, (0, 0))

    else:
        # Default cave/warren — crude banded wood planks + iron straps
        WOOD_BASE  = (105, 66, 30)
        WOOD_DARK  = (68,  42, 16)
        WOOD_LIGHT = (140, 90, 45)
        IRON       = (55, 55, 60)
        surf.fill(WOOD_BASE)
        # Vertical planks with grain
        for px in range(0, TEX_W, 6):
            tone = rng.uniform(0.84, 1.14)
            c = tuple(min(255, int(v * tone)) for v in WOOD_BASE)
            pygame.draw.line(surf, c, (px, 0), (px, TEX_H))
        # Rough grain texture (short horizontal scratches)
        for _ in range(18):
            gx = rng.randint(0, TEX_W - 8); gy = rng.randint(0, TEX_H - 1)
            gc = tuple(max(0, int(v * rng.uniform(0.7, 0.9))) for v in WOOD_BASE)
            pygame.draw.line(surf, gc, (gx, gy), (gx + rng.randint(3,7), gy))
        # Iron strap bands across the planks
        for py in [TEX_H//5, TEX_H*2//5, TEX_H*3//5, TEX_H*4//5]:
            pygame.draw.rect(surf, IRON,      (0, py-3, TEX_W, 6))
            pygame.draw.rect(surf, (70,70,75),(0, py-2, TEX_W, 4))
            # Rivet heads along the strap
            for rx in range(4, TEX_W - 4, 10):
                pygame.draw.circle(surf, (72,72,78), (rx, py), 3)
                pygame.draw.circle(surf, (85,85,90), (rx, py), 2)
        # Rough plank edge lines
        for px in range(0, TEX_W, 6):
            pygame.draw.line(surf, WOOD_DARK, (px, 0), (px, TEX_H), 1)
        # Door handle — crude iron ring
        pygame.draw.circle(surf, IRON, (TEX_W*3//4, TEX_H//2), 5, 2)
        pygame.draw.circle(surf, (70,70,76), (TEX_W*3//4, TEX_H//2), 4, 1)

    return surf


def _gen_arch_sprite(theme_id, wall_light, wall_dark, width, height):
    """Generate a stone arch frame sprite sized to (width, height).

    The arch frame is drawn as a pygame Surface with per-pixel alpha so it
    composites cleanly over the door wall slice.  Only the arch surround is
    drawn — the opening is fully transparent, preserving the door texture.
    """
    import math as _math
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    surf.fill((0, 0, 0, 0))   # fully transparent base

    if width < 6 or height < 6:
        return surf            # too small to draw

    rng_arch = random.Random(hash(("arch", theme_id, width, height)) & 0xFFFFFFFF)

    # Arch geometry
    jamb_w   = max(3, width  // 10)        # side jamb width in pixels
    arch_cx  = width  // 2
    arch_top = max(2, height // 6)         # y-coord of arch centre
    arch_r   = (width // 2) - jamb_w       # radius to inner arch edge
    arch_thick = max(3, width // 9)        # thickness of arch ring

    mortar   = tuple(max(0, int(v * 0.38)) for v in wall_dark) + (255,)
    stone_l  = tuple(min(255, int(v * 0.9)) for v in wall_light) + (255,)
    stone_h  = tuple(min(255, int(v * 1.12)) for v in wall_light) + (255,)

    BH = max(4, height // 9)
    BW = max(6, width  // 4)

    # ── Left jamb (stone blocks) ──────────────────────────────────────────
    y_start = int(arch_top + arch_r)        # jamb starts below arch curve
    for row in range(20):
        oy = y_start + row * BH
        if oy >= height: break
        tone = 0.80 + rng_arch.random() * 0.28
        c = tuple(min(255, int(v * tone)) for v in wall_light) + (255,)
        h = min(BH - 1, height - oy)
        if h > 0:
            pygame.draw.rect(surf, c, (0, oy, jamb_w, h))
            pygame.draw.rect(surf, mortar, (0, oy + h - 1, jamb_w, 1))
            # Highlight top of each block
            pygame.draw.rect(surf, stone_h, (0, oy, jamb_w, 1))
            # Shadow on right edge of jamb
            pygame.draw.rect(surf, mortar, (jamb_w - 1, oy, 1, h))

    # ── Right jamb ────────────────────────────────────────────────────────
    rng_arch2 = random.Random(hash(("arch2", theme_id)) & 0xFFFFFFFF)
    for row in range(20):
        oy = y_start + row * BH
        if oy >= height: break
        tone = 0.80 + rng_arch2.random() * 0.28
        c = tuple(min(255, int(v * tone)) for v in wall_light) + (255,)
        h = min(BH - 1, height - oy)
        if h > 0:
            pygame.draw.rect(surf, c, (width - jamb_w, oy, jamb_w, h))
            pygame.draw.rect(surf, mortar, (width - jamb_w, oy + h - 1, jamb_w, 1))
            pygame.draw.rect(surf, stone_h, (width - jamb_w, oy, jamb_w, 1))
            pygame.draw.rect(surf, mortar, (width - jamb_w, oy, 1, h))

    # ── Voussoir arch ring ────────────────────────────────────────────────
    n_stones = max(5, min(13, width // 14))   # odd number for keystone
    if n_stones % 2 == 0:
        n_stones += 1
    inner_r  = arch_r
    outer_r  = arch_r + arch_thick

    for i in range(n_stones):
        a0 = _math.pi + (i / n_stones) * _math.pi
        a1 = _math.pi + ((i + 1) / n_stones) * _math.pi

        is_keystone = (i == n_stones // 2)
        tone = 1.15 if is_keystone else (0.78 + rng_arch.random() * 0.30)
        c = tuple(min(255, int(v * tone)) for v in wall_light) + (255,)

        # Draw filled voussoir wedge
        pts = []
        steps = max(4, int((a1 - a0) * outer_r))
        for s in range(steps + 1):
            t = s / steps
            a = a0 + t * (a1 - a0)
            pts.append((int(arch_cx + outer_r * _math.cos(a)),
                         int(arch_top  + outer_r * _math.sin(a))))
        for s in range(steps, -1, -1):
            t = s / steps
            a = a0 + t * (a1 - a0)
            pts.append((int(arch_cx + inner_r * _math.cos(a)),
                         int(arch_top  + inner_r * _math.sin(a))))
        if len(pts) >= 3:
            pygame.draw.polygon(surf, c, pts)
            # Mortar joint lines at edges
            pygame.draw.polygon(surf, mortar, pts, 1)

        # Chisel highlight on outer edge (lighter line)
        mid_a = (a0 + a1) / 2
        for da in (_math.radians(2),):
            hx1 = int(arch_cx + outer_r * _math.cos(a0 + da))
            hy1 = int(arch_top  + outer_r * _math.sin(a0 + da))
            hx2 = int(arch_cx + outer_r * _math.cos(a1 - da))
            hy2 = int(arch_top  + outer_r * _math.sin(a1 - da))
            pygame.draw.line(surf, stone_h, (hx1, hy1), (hx2, hy2), 1)

        # Mortar joint line between voussoirs
        for edge_a in (a0, a1):
            ix = int(arch_cx + inner_r * _math.cos(edge_a))
            iy = int(arch_top  + inner_r * _math.sin(edge_a))
            ox = int(arch_cx + outer_r * _math.cos(edge_a))
            oy = int(arch_top  + outer_r * _math.sin(edge_a))
            pygame.draw.line(surf, mortar, (ix, iy), (ox, oy), max(1, width // 80))

    # Tower theme: add void glow on arch outer edge
    if theme_id == "tower":
        void_col = (110, 55, 210, 60)
        for i in range(max(5, int(outer_r * _math.pi / 2))):
            t = i / max(1, int(outer_r * _math.pi / 2))
            a = _math.pi + t * _math.pi
            gx = int(arch_cx + (outer_r + 2) * _math.cos(a))
            gy = int(arch_top  + (outer_r + 2) * _math.sin(a))
            if 0 <= gx < width and 0 <= gy < height:
                surf.set_at((gx, gy), void_col)

    return surf


def _gen_entrance_texture(theme_id, wall_light, wall_dark):
    """Generate the dungeon exit arch wall texture (64×64) using draw_entrance."""
    from ui.dungeon_objects import draw_entrance as _de
    surf = pygame.Surface((TEX_W, TEX_H))
    surf.fill((4, 2, 8))
    _de(surf, pygame.Rect(0, 0, TEX_W, TEX_H), theme_id)
    return surf


def _gen_stair_texture(going_down=True, light=(180,160,120), dark=(90,75,50)):
    """
    Full-wall stair texture (64×64).

    Stairs DOWN — floor-perspective view:
        Looking at a floor tile where the stairwell descends.
        Stairs are carved into the floor: wide near the party (bottom of
        texture), narrowing toward the far end (top). The floor beside the
        stairs runs at normal floor tone near the party edge and fades
        with soft, low-contrast gradients toward the stairwell opening.
        The opening itself is a dark void at the narrow/far end.

    Stairs UP — U-shaped alcove wall view:
        Party looks into a recessed U-shaped alcove. Side walls of the
        alcove angle inward; stairs rise at the back. Dim light from
        above + torch sconce for the UP direction.
    """
    W, H = TEX_W, TEX_H
    surf = pygame.Surface((W, H))
    DARK_PIX = (4, 2, 8)
    surf.fill(DARK_PIX)

    rng    = random.Random(0xF17E if going_down else 0xF17A)
    shadow = tuple(max(0, c - 18) for c in dark)
    mortar = tuple(max(0, c - 22) for c in dark)

    # ═══════════════════════════════════════════════════════════
    #  STAIRS DOWN — floor perspective, amorphous stone, black rect void
    # ═══════════════════════════════════════════════════════════
    if going_down:
        # ── Derive floor colour from theme dark/light tones ───────────
        floor_n = tuple(min(255, int(dark[i] * 1.35 + 8)) for i in range(3))
        floor_n = tuple(min(255, int(floor_n[i] * 1.10)) for i in range(3))

        # ── Gradient background: floor_n at bottom → near-black at top ─
        for y in range(H):
            t_c = ((1.0 - y / max(1, H - 1)) ** 2.0)
            row_col = tuple(int(DARK_PIX[i] + (floor_n[i] - DARK_PIX[i]) * t_c)
                            for i in range(3))
            pygame.draw.line(surf, row_col, (0, y), (W - 1, y))

        # ── Stairwell geometry ─────────────────────────────────────────
        RECT_W    = int(W * 0.44)
        RECT_H    = int(H * 0.18)
        RECT_X    = W // 2 - RECT_W // 2
        RECT_Y    = 0
        NEAR_HALF = int(W * 0.43)
        FAR_HALF  = RECT_W // 2
        STEP_TOP  = RECT_H
        STEP_BOT  = H - 2

        def slx(y):
            t = max(0.0, min(1.0, (y - RECT_H) / max(1, H - RECT_H - 2)))
            return int(W // 2 - (FAR_HALF + (NEAR_HALF - FAR_HALF) * t))

        def srx(y):
            t = max(0.0, min(1.0, (y - RECT_H) / max(1, H - RECT_H - 2)))
            return int(W // 2 + (FAR_HALF + (NEAR_HALF - FAR_HALF) * t))

        # ── Amorphous stone blobs — large near party, tiny near void ──
        N_BANDS = 10
        for band in range(N_BANDS):
            band_t   = band / N_BANDS
            band_bot = H - 1 - int(band_t * H)
            band_top = H - 1 - int((band_t + 1.0 / N_BANDS) * H)
            band_top = max(band_top, 0)

            max_rx = max(2, int(W * (0.14 - 0.12 * band_t)))
            max_ry = max(1, int(H * (0.08 - 0.07 * band_t)))
            t_col  = (1.0 - band_t) ** 2.0
            base_c = tuple(int(DARK_PIX[i] + (floor_n[i] - DARK_PIX[i]) * t_col)
                           for i in range(3))
            v_rng  = int(20 * (1.0 - band_t))
            n_blobs = max(3, int(18 * (1.0 - band_t * 0.7)))

            for _ in range(n_blobs):
                bx = rng.randint(0, W - 1)
                by = rng.randint(band_top, max(band_top, band_bot))
                lx_h = slx(by) if by >= STEP_TOP else W // 2 - FAR_HALF
                rx_h = srx(by) if by >= STEP_TOP else W // 2 + FAR_HALF
                if lx_h <= bx <= rx_h:
                    continue
                rx_b = rng.randint(max(1, max_rx // 2), max(2, max_rx))
                ry_b = max(1, rng.randint(max(1, max_ry // 2), max(1, max_ry)) * 6 // 10)
                v = rng.randint(-v_rng, v_rng)
                col = tuple(max(0, min(255, c + v)) for c in base_c)
                if rx_b >= 3 and ry_b >= 2:
                    pygame.draw.ellipse(surf, col, (bx-rx_b, by-ry_b, rx_b*2, ry_b*2))
                    hi = tuple(min(255, c + max(1, v_rng // 2)) for c in col)
                    pygame.draw.ellipse(surf, hi, (bx-rx_b, by-ry_b, rx_b*2, ry_b*2), 1)
                elif rx_b >= 2:
                    pygame.draw.circle(surf, col, (bx, by), rx_b)
                else:
                    if 0 <= bx < W and 0 <= by < H:
                        surf.set_at((bx, by), col)

        # ── Step treads ───────────────────────────────────────────────
        STEPS = 6
        out_ln = tuple(max(0, c - 18) for c in dark)
        for i in range(STEPS):
            y_far  = int(STEP_TOP + (STEP_BOT - STEP_TOP) * i       / STEPS)
            y_near = int(STEP_TOP + (STEP_BOT - STEP_TOP) * (i + 1) / STEPS)
            lx_f = slx(y_far);  rx_f = srx(y_far)
            lx_n = slx(y_near); rx_n = srx(y_near)
            if rx_n <= lx_n or y_near <= y_far:
                continue
            brightness = 0.08 + 0.70 * (i / max(1, STEPS - 1))
            sv  = rng.randint(-6, 6)
            sc  = tuple(max(0, min(255, int(dark[j] + (light[j]-dark[j])*brightness) + sv))
                        for j in range(3))
            rc  = tuple(max(0, int(sc[j] * 0.38)) for j in range(3))
            ehi = tuple(min(255, c + 32) for c in sc)
            pygame.draw.polygon(surf, sc,
                [(lx_f,y_far),(rx_f,y_far),(rx_n,y_near),(lx_n,y_near)])
            pygame.draw.line(surf, ehi, (lx_n+1,y_near), (rx_n-1,y_near), 2)
            pygame.draw.polygon(surf, out_ln,
                [(lx_f,y_far),(rx_f,y_far),(rx_n,y_near),(lx_n,y_near)], 1)
            riser_h = max(2, (y_near - y_far) // 3)
            bot_r   = min(H - 1, y_near + riser_h)
            if rx_n > lx_n:
                pygame.draw.polygon(surf, rc,
                    [(lx_n,y_near),(rx_n,y_near),(rx_n,bot_r),(lx_n,bot_r)])

        # ── Black void rectangle flush at top ─────────────────────────
        pygame.draw.rect(surf, DARK_PIX, (RECT_X, RECT_Y, RECT_W, RECT_H))
        lip = tuple(max(0, min(255, int(dark[i]*0.30))) for i in range(3))
        pygame.draw.rect(surf, lip, (RECT_X, RECT_Y, RECT_W, RECT_H), 1)
        void_bot = RECT_H
        pygame.draw.line(surf, tuple(max(0, int(dark[i]*0.28)) for i in range(3)),
                         (RECT_X, void_bot), (RECT_X+RECT_W, void_bot), 2)

        # ── Faint ember glow at void base ─────────────────────────────
        for gi in range(5):
            gy = void_bot + gi + 1
            gw = max(2, RECT_W - gi * 4)
            gcx = W // 2
            glow = (max(0,40-gi*8), max(0,14-gi*3), 1)
            pygame.draw.line(surf, glow, (gcx-gw//2, gy), (gcx+gw//2, gy))

        return surf

    # ═══════════════════════════════════════════════════════════
    #  STAIRS UP — wall face: stairs ascending + near-black rect at top
    # ═══════════════════════════════════════════════════════════
    # No torch, no door, no U-shape chrome — just the staircase
    # rising into a near-black rectangle (darkness above).
    RECT_H_UP = int(H * 0.20)      # near-black rectangle at top
    y_void_up  = RECT_H_UP          # where steps begin

    wall_near_w = int(W * 0.19)
    wall_far_w  = int(W * 0.46)

    def lwr(y): return int(wall_far_w + (wall_near_w - wall_far_w) * y / H)
    def rwl(y): return W - lwr(y)

    lit_up = tuple(min(255, int(light[i]*0.90 + dark[i]*0.10)) for i in range(3))
    shd_up = tuple(max(0, int(dark[i]*0.72)) for i in range(3))
    mortar_up = tuple(max(0, c - 22) for c in dark)
    seed_lu = hash(("stex_lu", False)) & 0xFFFFFF
    seed_ru = hash(("stex_ru", False)) & 0xFFFFFF

    # Stone walls either side
    from ui.dungeon_ui import _gen_stair_texture  # not needed — same module
    # Use same masonry loop pattern as down branch
    bh = max(3, H // 14); bw = max(4, W // 9)
    for side in ("left", "right"):
        get_lx = (lambda y: 0)       if side == "left"  else rwl
        get_rx = lwr                  if side == "left"  else (lambda y: W)
        base   = lit_up               if side == "left"  else shd_up
        seed   = seed_lu              if side == "left"  else seed_ru
        y = 0; row = 0
        while y < H:
            rh = max(2, min(bh + rng.randint(-bh//3, bh//2), H - y))
            lx = int(get_lx(y)); rx = int(get_rx(y))
            if rx > lx:
                off = rng.randint(bw//3, bw*2//3) if row % 2 else 0
                x = lx - off; ci = 0
                while x < rx:
                    bwi = max(3, bw + rng.randint(-bw//3, bw//2))
                    bx = max(lx, x); bx2 = min(rx, x + bwi - 1)
                    if bx2 > bx:
                        v = rng.randint(-16, 16)
                        sp = rng.randint(0, 12)
                        if sp == 0: v -= 12
                        elif sp == 1: v += 9
                        bc = tuple(max(0, min(255, c + v)) for c in base)
                        pygame.draw.rect(surf, bc, (bx, y, bx2 - bx, rh - 1))
                    x += bwi; ci += 1
                if y + rh < H:
                    pygame.draw.line(surf, mortar_up,
                                     (lx, y + rh - 1), (rx, y + rh - 1), 1)
            y += rh; row += 1

    # Steps: wide at bottom, narrow toward y_void_up
    STEPS_UP = 7
    shadow_up = tuple(max(0, c - 18) for c in dark)
    for i in range(STEPS_UP):
        near_y = int(H - (H - y_void_up) * (i     / STEPS_UP))
        far_y  = int(H - (H - y_void_up) * ((i+1) / STEPS_UP))
        lnear = lwr(near_y); rnear = rwl(near_y)
        lfar  = lwr(far_y);  rfar  = rwl(far_y)
        brightness = 0.18 + 0.34 * i / max(1, STEPS_UP - 1)
        tone = rng.uniform(0.92, 1.08)
        sv   = rng.randint(-8, 8)
        sc   = tuple(max(0, min(255, int(dark[j] + (light[j]-dark[j])*brightness*tone) + sv))
                     for j in range(3))
        rc   = tuple(max(0, int(sc[j] * 0.55)) for j in range(3))
        ec   = tuple(min(255, c + 22) for c in sc)
        pygame.draw.polygon(surf, sc,
            [(lnear,near_y),(rnear,near_y),(rfar,far_y),(lfar,far_y)])
        rh2 = max(1, (near_y - far_y) // 3)
        pygame.draw.polygon(surf, rc,
            [(lnear,near_y),(rnear,near_y),
             (rnear,near_y+rh2),(lnear,near_y+rh2)])
        pygame.draw.polygon(surf, shadow_up,
            [(lnear,near_y),(rnear,near_y),(rfar,far_y),(lfar,far_y)], 1)
        pygame.draw.line(surf, ec,
                         (lnear+1, near_y+1), (rnear-1, near_y+1), 1)

    # Near-black rectangle overlay at top — opening into darkness above
    lx_t = lwr(y_void_up); rx_t = rwl(y_void_up)
    rw_t  = rx_t - lx_t
    if rw_t > 0:
        pygame.draw.rect(surf, DARK_PIX, (lx_t, 0, rw_t, RECT_H_UP))
    pygame.draw.line(surf, shadow_up, (lx_t, y_void_up), (rx_t, y_void_up), 2)

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


def _gen_spider_textures(light, dark):
    """Spider's Nest: stone walls increasingly obscured by webbing across 3 variants.

    Variant 0 — stone with corner webs and sparse strands (early floors)
    Variant 1 — heavy web coverage, egg sacs, web curtains dropping from top
    Variant 2 — near-total web cover, barely see stone, dense layered silk
    """
    rng0 = random.Random(hash(("spider0", light)))
    rng1 = random.Random(hash(("spider1", light)))
    rng2 = random.Random(hash(("spider2", light)))
    out  = []

    # ── Stone base shared across all variants (increasingly dark) ────────
    def _stone_base(rng_st, tone_lo, tone_hi):
        s = pygame.Surface((TEX_W, TEX_H))
        mortar = tuple(int(v * 0.42) for v in dark)
        s.fill(mortar)
        for _ in range(140):
            x = rng_st.randint(0, TEX_W-1); y = rng_st.randint(0, TEX_H-1)
            w = rng_st.randint(2, 7);  h = rng_st.randint(1, 4)
            tone = rng_st.uniform(tone_lo, tone_hi)
            c = tuple(min(255, int(v * tone)) for v in light)
            pygame.draw.rect(s, c, (x, y, min(w, TEX_W-x), min(h, TEX_H-y)))
        return s, mortar

    WEB_LIGHT = (215, 208, 192)
    WEB_MID   = (190, 183, 165)
    WEB_OLD   = (165, 155, 130)   # yellowed older web

    def _draw_web_strand(surf, rng_w, x1, y1, x2, y2, col, width=1):
        pygame.draw.line(surf, col, (x1, y1), (x2, y2), width)

    def _draw_web_cluster(surf, rng_w, cx, cy, size, density, col):
        """Radial web cluster centred at (cx,cy)."""
        n = int(density * 14)
        for _ in range(n):
            ang = rng_w.uniform(0, 6.283)
            import math as _m
            r  = rng_w.uniform(2, size)
            ex = int(cx + _m.cos(ang) * r)
            ey = int(cy + _m.sin(ang) * r)
            _draw_web_strand(surf, rng_w, cx, cy, ex, ey, col)

    def _draw_egg_sac(surf, x, y, radius, col):
        pygame.draw.ellipse(surf, col,
                            (x - radius, y - int(radius * 1.3),
                             radius * 2, int(radius * 2.6)))
        outline = tuple(max(0, int(v * 0.7)) for v in col)
        pygame.draw.ellipse(surf, outline,
                            (x - radius, y - int(radius * 1.3),
                             radius * 2, int(radius * 2.6)), 1)

    # ── Variant 0: light web in corners, sparse strands ──────────────────
    s, mortar = _stone_base(rng0, 0.52, 1.08)

    # Corner web clusters
    for cx, cy in [(2, 2), (TEX_W-3, 2), (2, TEX_H-3), (TEX_W-3, TEX_H-3)]:
        _draw_web_cluster(s, rng0, cx, cy, 14, 0.55,
                          tuple(int(v * 0.85) for v in WEB_LIGHT))
    # 8 sparse strands
    for _ in range(8):
        x1 = rng0.randint(0, TEX_W-1)
        y1 = rng0.randint(0, TEX_H // 3)
        x2 = x1 + rng0.randint(-12, 12)
        y2 = y1 + rng0.randint(4, 18)
        alpha_col = tuple(int(v * 0.55) for v in WEB_LIGHT)
        _draw_web_strand(s, rng0, x1, y1,
                         max(0, min(TEX_W-1, x2)),
                         min(TEX_H-1, y2), alpha_col)
    out.append(s)

    # ── Variant 1: heavy coverage, egg sac, web curtain top ──────────────
    s, mortar = _stone_base(rng1, 0.40, 0.88)

    # Web curtain from ceiling
    for x in range(0, TEX_W, 2):
        drop = rng1.randint(6, 24)
        col  = WEB_MID if rng1.random() > 0.4 else WEB_OLD
        _draw_web_strand(s, rng1, x, 0,
                         x + rng1.randint(-2, 2), drop, col)
    # Diagonal cross-strands covering most of wall
    for _ in range(22):
        x1 = rng1.randint(0, TEX_W-1); y1 = rng1.randint(0, TEX_H-1)
        x2 = max(0, min(TEX_W-1, x1 + rng1.randint(-22, 22)))
        y2 = max(0, min(TEX_H-1, y1 + rng1.randint(-18, 18)))
        col = WEB_MID if rng1.random() > 0.35 else WEB_OLD
        _draw_web_strand(s, rng1, x1, y1, x2, y2, col)
    # One egg sac
    ex = rng1.randint(12, TEX_W-12)
    ey = rng1.randint(TEX_H//4, TEX_H*3//4)
    _draw_egg_sac(s, ex, ey, rng1.randint(4, 7),
                  (200, 186, 148))
    out.append(s)

    # ── Variant 2: near-total coverage, barely see stone ─────────────────
    s, mortar = _stone_base(rng2, 0.28, 0.65)

    # Dense web fill — draw many overlapping strands
    for _ in range(48):
        x1 = rng2.randint(0, TEX_W-1); y1 = rng2.randint(0, TEX_H-1)
        x2 = max(0, min(TEX_W-1, x1 + rng2.randint(-28, 28)))
        y2 = max(0, min(TEX_H-1, y1 + rng2.randint(-28, 28)))
        col = (WEB_LIGHT if rng2.random() > 0.6
               else WEB_MID if rng2.random() > 0.4
               else WEB_OLD)
        w = 1 if rng2.random() > 0.25 else 2
        _draw_web_strand(s, rng2, x1, y1, x2, y2, col, w)
    # Heavy curtain
    for x in range(0, TEX_W):
        drop = rng2.randint(14, 38)
        col  = WEB_LIGHT if rng2.random() > 0.5 else WEB_MID
        _draw_web_strand(s, rng2, x, 0,
                         x + rng2.randint(-1, 1), drop, col)
    # Two to three egg sacs
    for _ in range(rng2.randint(2, 3)):
        ex2 = rng2.randint(6, TEX_W-6)
        ey2 = rng2.randint(6, TEX_H-6)
        _draw_egg_sac(s, ex2, ey2, rng2.randint(3, 6),
                      (195, 180, 140))
    out.append(s)
    return out


def _gen_theme_textures(theme_id, wall_light, wall_dark):
    """Return list of NUM_WALL_VARIANTS texture surfaces for this theme."""
    fn = {
        "cave":   _gen_cave_textures,
        "spider": _gen_spider_textures,
        "mine":   _gen_mine_textures,
        "crypt":  _gen_crypt_textures,
        "ruins":  _gen_ruins_textures,
        "tower":  _gen_tower_textures,
    }.get(theme_id, _gen_cave_textures)
    return fn(wall_light, wall_dark)


def _gen_texture(wall_light, wall_dark, is_door=False, theme_id="cave"):
    """Backward-compat wrapper — returns a single texture."""
    if is_door:
        return _gen_door_texture(theme_id, wall_light, wall_dark)
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
        # Theme-matched door texture — arch style varies by dungeon
        self._tex_door       = _gen_door_texture(
            self.theme_id, self.wall_light, self.wall_dark)
        self._door_cols      = self._bake_tex_cols(self._tex_door)
        # Arch sprite cache: key=(width,height) -> Surface.
        # Generated lazily and cached so each unique door size is only built once.
        self._arch_cache: dict = {}
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
        # Numpy array of stair-down texture for floor-perspective projection
        import numpy as _np
        import pygame.surfarray as _sa
        self._np_stair_down = _sa.array3d(self._tex_stair_down).astype(_np.float32)

        # Exit arch wall texture
        self._tex_entrance    = _gen_entrance_texture(self.theme_id, self.wall_light, self.wall_dark)
        self._entrance_cols   = self._bake_tex_cols(self._tex_entrance)
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
        self._sprite_cache = {}   # (template_key, w, h) → Surface with colorkey set

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
        self.interactable_modal  = None   # fountain/shrine/altar modal state
        self.scroll_modal        = None   # None or {title, text, lines} for note/journal display
        self.spire_choice_modal  = None   # None or dict — post-Spire descent choice

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
        # Snap to new floor entrance immediately — cancel any in-progress animation
        self.px = float(self.dungeon.party_x) + 0.5
        self.py = float(self.dungeon.party_y) + 0.5
        # Reset movement animation so the next frame doesn't resume interpolating
        # toward a target on the previous floor
        self._move_anim_t   = 1.0
        self._turn_anim_t   = 1.0
        self._move_start_x  = self.px
        self._move_start_y  = self.py
        self._move_target_x = self.px
        self._move_target_y = self.py
        # Sync grid position immediately so minimap is correct on first frame
        self._sync_grid_pos()
        self._recalc_camera()

    def _is_solid(self, gx, gy):
        fl = self.dungeon.get_current_floor_data()
        if gx < 0 or gy < 0 or gx >= fl["width"] or gy >= fl["height"]:
            return True
        tile = fl["tiles"][gy][gx]
        tt   = tile["type"]
        if tt == DT_SECRET_DOOR and not tile.get("secret_found"):
            return True
        return tt in (DT_WALL, DT_STAIRS_UP, DT_ENTRANCE)

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
            is_stair = tt in (DT_STAIRS_UP, DT_ENTRANCE)
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

                # Stairs: only show stair texture on the entrance face.
                # The other three faces render as normal dungeon wall.
                show_stair = False
                if is_stair:
                    facing = tile.get("facing", "south")
                    if ns:
                        hit_face = "north" if step_y > 0 else "south"
                    else:
                        hit_face = "west"  if step_x > 0 else "east"
                    # Show texture on both faces along the stair's axis so the
                    # party sees it from either approach direction (north OR south
                    # for a N-S stair, east OR west for an E-W stair).
                    is_ns_facing = facing in ("north", "south")
                    show_stair   = (ns == is_ns_facing)

                return max(0.01, dist), wx, ns, False, map_x, map_y, show_stair, tt, 0.0

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
        if self.interactable_modal:
            self._draw_interactable_modal(surface, mx, my)
        if self.scroll_modal:
            self._draw_scroll_modal(surface, mx, my)
        if self.spire_choice_modal:
            self._draw_spire_choice_modal(surface, mx, my)

        if (self.event_message and self.event_timer > 0) or self.event_queue:
            self._draw_events(surface)



    # ─────────────────────────────────────────────────────────
    #  FLOOR-PROJECTED STAIR TEXTURE
    # ─────────────────────────────────────────────────────────

    def _render_stair_floor_tiles(self, view):
        """
        Floor perspective projection for DT_STAIRS_DOWN tiles.

        Standard raycaster floor-casting math: for each floor scanline sy,
        compute world (fx, fy) each screen pixel maps to.  Pixels on a
        discovered DT_STAIRS_DOWN tile sample _tex_stair_down with UV
        mapping that keeps the wide/near end facing the party.

        KEY: uses VP_H//2 as posZ (not PROJ_DIST) so tiles at 1-3 tile
        distance are actually visible within the 810-pixel viewport.
        """
        import numpy as _np
        import pygame.surfarray as _sa

        VH = VP_H; VW = VP_W; HH = VH // 2
        posZ = float(HH)   # <-- use VP_H/2, NOT PROJ_DIST
        FOG  = TORCH_DIST

        fl    = self.dungeon.get_current_floor_data()
        tiles = fl["tiles"]
        fw, fh = fl["width"], fl["height"]
        px, py = self.px, self.py

        # Collect nearby discovered DT_STAIRS_DOWN tiles
        SCAN_R = 8
        stair_tiles = []
        for gy in range(max(0, int(py) - SCAN_R), min(fh, int(py) + SCAN_R + 1)):
            for gx in range(max(0, int(px) - SCAN_R), min(fw, int(px) + SCAN_R + 1)):
                t = tiles[gy][gx]
                if t.get("type") == DT_STAIRS_DOWN and t.get("discovered"):
                    stair_tiles.append((gx, gy, t.get("facing", "south")))
        if not stair_tiles:
            return

        np_tex = self._np_stair_down
        fog_c  = _np.array(self.fog_c, dtype=_np.float32)

        # Floor-casting basis vectors (standard raycaster floor formula)
        dx, dy     = self.dx, self.dy
        cx_c, cy_c = self.cx, self.cy
        lrx = dx - cx_c   # direction of leftmost ray
        lry = dy - cy_c
        sx_u = 2.0 * cx_c / VW   # per-pixel lateral step (scaled by row_dist)
        sy_u = 2.0 * cy_c / VW

        xs = _np.arange(VW, dtype=_np.float32)
        sa = _sa.pixels3d(view)   # (VW, VH, 3) — locks surface

        for G_X, G_Y, facing in stair_tiles:
            for sy in range(HH + 1, VH):
                row_dist = posZ / (sy - HH)   # uses HH, not PROJ_DIST

                fx = px + row_dist * lrx + xs * (row_dist * sx_u)
                fy = py + row_dist * lry + xs * (row_dist * sy_u)

                mask = ((fx >= G_X) & (fx < G_X + 1) &
                        (fy >= G_Y) & (fy < G_Y + 1))
                if not _np.any(mask):
                    continue

                fx_m = fx[mask] - G_X
                fy_m = fy[mask] - G_Y

                # UV: wide/bright end of texture faces the open (approach) side
                if facing == "south":
                    tu = _np.clip((fx_m * TEX_W).astype(_np.int32), 0, TEX_W - 1)
                    tv = _np.clip((fy_m * TEX_H).astype(_np.int32), 0, TEX_H - 1)
                elif facing == "north":
                    tu = _np.clip((fx_m * TEX_W).astype(_np.int32), 0, TEX_W - 1)
                    tv = _np.clip(((1.0 - fy_m) * TEX_H).astype(_np.int32), 0, TEX_H - 1)
                elif facing == "east":
                    tu = _np.clip((fy_m * TEX_W).astype(_np.int32), 0, TEX_W - 1)
                    tv = _np.clip((fx_m * TEX_H).astype(_np.int32), 0, TEX_H - 1)
                else:  # west
                    tu = _np.clip((fy_m * TEX_W).astype(_np.int32), 0, TEX_W - 1)
                    tv = _np.clip(((1.0 - fx_m) * TEX_H).astype(_np.int32), 0, TEX_H - 1)

                colors = np_tex[tu, tv]

                horizon_t = float(sy - HH) / HH
                fog_t     = min(1.0, row_dist * 0.35 / FOG)
                bright    = 0.45 + 0.55 * horizon_t
                lit = colors * (bright * (1.0 - fog_t)) + fog_c * fog_t
                _np.clip(lit, 0, 255, out=lit)

                x_idx = _np.where(mask)[0].astype(_np.int32)
                sa[x_idx, sy] = lit.astype(_np.uint8)

        del sa  # release surface lock

    # ─────────────────────────────────────────────────────────
    #  3D RENDER
    # ─────────────────────────────────────────────────────────

    def _render_3d(self):
        view  = self._view
        VH    = VP_H
        VW    = VP_W
        HH    = VH // 2
        zbuf  = self._zbuf
        # Reset zbuf every frame — must be fresh before wall columns fill it.
        # Stale zeros from __init__ (or a dropped frame) make all sprites invisible.
        for _i in range(VW):
            zbuf[_i] = 20.0   # default to max torch distance (no wall)
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

        # ── Floor-projected stair texture (before wall columns) ──
        self._render_stair_floor_tiles(view)

        # ── Wall columns ──
        wall_variants = self._wall_cols_variants
        door_cols     = self._door_cols
        num_v         = len(wall_variants)

        # Track door screen bounds for arch sprite overlay (Option B)
        _door_col_min  = VW    # leftmost column of door
        _door_col_max  = -1    # rightmost column of door
        _door_top_min  = VH    # topmost pixel of door
        _door_bot_max  = 0     # bottommost pixel of door
        _door_h_sum    = 0     # sum of wall_h across door columns (for average)
        _door_h_count  = 0     # number of door columns rendered

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
                # Accumulate door screen bounds for arch sprite
                if col < _door_col_min: _door_col_min = col
                if col > _door_col_max: _door_col_max = col
                _door_top_this = max(0, top)
                _door_bot_this = min(VH, top + wall_h)
                if _door_top_this < _door_top_min: _door_top_min = _door_top_this
                if _door_bot_this > _door_bot_max: _door_bot_max = _door_bot_this
                # Track average height so arch sprite is sized for typical column
                _door_h_sum   += wall_h
                _door_h_count += 1
            elif is_stair:
                # Wall-face stair/entrance textures
                if hit_tt == DT_ENTRANCE:
                    cols_src = self._entrance_cols[tex_x]
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

        # ── Arch sprite overlay ──
        # Draw stone arch frame over the door wall slice.
        # Only fires when a door was actually visible this frame.
        if _door_col_max >= _door_col_min and _door_bot_max > _door_top_min:
            dw = _door_col_max - _door_col_min + 1
            # Use average door height so arch sizes to center column, not bounding box.
            # This prevents the arch frame mismatching the door wood when viewed at angle.
            if _door_h_count > 0:
                dh = _door_h_sum // _door_h_count
                avg_top = HH - dh // 2
            else:
                dh = _door_bot_max - _door_top_min
                avg_top = _door_top_min
            if dw >= 6 and dh >= 6:
                key = (dw, dh)
                if key not in self._arch_cache:
                    self._arch_cache[key] = _gen_arch_sprite(
                        self.theme_id, self.wall_light, self.wall_dark, dw, dh)
                arch_surf = self._arch_cache[key]
                view.blit(arch_surf, (_door_col_min, avg_top))
            # Reset bounds for next frame
            _door_col_min = VW; _door_col_max = -1
            _door_top_min = VH; _door_bot_max = 0
            _door_h_sum = 0; _door_h_count = 0

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
                # UP and ENTRANCE are wall tiles — skip sprite rendering
                # DOWN is now a floor tile — render as floor-anchored sprite
                if tt in (DT_STAIRS_DOWN, DT_STAIRS_UP, DT_ENTRANCE):
                    pass  # rendered as wall face texture — no sprite needed
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

        # Add visible patrol enemies from the floor enemy list.
        # Visibility is determined by torch range and zbuf (wall occlusion) only —
        # NOT by tile discovery. Enemies can move off discovered tiles but are still seen.
        for enemy in fl.get("enemies", []):
            if enemy.get("state") == "dead":
                continue
            ex, ey = enemy["x"], enemy["y"]
            esx = ex + 0.5 - self.px
            esy = ey + 0.5 - self.py
            d   = math.sqrt(esx*esx + esy*esy)
            if d < 0.3 or d > TORCH_DIST + 1:
                continue
            sprites.append((d, esx, esy, "enemy", enemy.get("enc_key")))

        sprites.sort(key=lambda s: -s[0])

        font = get_font(32)
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
                DT_STAIRS_DOWN:  0.40,   # floor stairwell — small sprite near floor
                DT_STAIRS_UP:    0.55,
                DT_INTERACTABLE: 0.72,   # shrine/fountain — taller, more visible
                DT_ENTRANCE:     0.80,   # archway — tall but not full wall
                DT_TRAP:         0.35,   # trap plate — raised rune plate, visible
                "trap_disarmed": 0.25,
                "trap_tripped":  0.20,
                "journal":       0.30,
                "enemy":         0.85,
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
                if icon_key == DT_STAIRS_UP:
                    sp_h = min(sp_h, VP_H // 3)
                    sp_w = sp_h
                elif icon_key == DT_STAIRS_DOWN:
                    # Floor stairwell: cap height so it never looks like a wall,
                    # and make it slightly wider than tall (floor perspective)
                    sp_h = min(sp_h, VP_H // 5)
                    sp_w = int(sp_h * 1.4)
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

            # Depth test: use cx_s (centre of visible sprite portion) for zbuf lookup.
            # This matches the occlusion test for chests/traps (which are never visible
            # through walls). zbuf < 1.0 means an entrance/stair tile is immediately
            # adjacent to the player — treat that column as unoccluded so sprites
            # deeper in the dungeon aren't culled by the adjacent tile.
            _zbuf_raw = zbuf[cx_s] if 0 <= cx_s < VP_W else 0.0
            _zbuf_val = _zbuf_raw if _zbuf_raw >= 1.0 else 20.0
            if 0 <= cx_s < VP_W and ty_ < _zbuf_val:
                surf_w = max(8, sp_w)
                surf_h = max(8, sp_h)
                spr = pygame.Surface((surf_w, surf_h), pygame.SRCALPHA)
                c_a = (*color, alpha)
                dim = (int(color[0]*0.4), int(color[1]*0.4), int(color[2]*0.4), alpha//2)

                if icon_key == DT_STAIRS_DOWN:
                    obj_r = pygame.Rect(0, 0, surf_w, surf_h)
                    from ui.dungeon_objects import draw_stairs_down as _dsd
                    _dsd(spr, obj_r, self.theme_id)

                elif icon_key == DT_STAIRS_UP:
                    obj_r = pygame.Rect(0, 0, surf_w, surf_h)
                    from ui.dungeon_objects import draw_stairs_up as _dsu
                    _dsu(spr, obj_r, self.theme_id)

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
                    draw_dungeon_object(spr, obj_r, obj_key, self.theme_id)

                elif icon_key == DT_TREASURE:
                    obj_r = pygame.Rect(0, 0, surf_w, surf_h)
                    draw_dungeon_object(spr, obj_r, "chest", self.theme_id)

                elif icon_key in ("enemy", "boss"):
                    from ui.pixel_art import draw_enemy_silhouette
                    from ui.wiz_sprites import BG as _WIZ_BG
                    template_key = enc_key or "Goblin Warrior"
                    try:
                        from data.enemies import ENCOUNTERS
                        if enc_key and enc_key in ENCOUNTERS:
                            grps = ENCOUNTERS[enc_key].get("groups", [])
                            if grps:
                                template_key = grps[0]["enemy"]
                    except Exception:
                        pass
                    # Use cached scaled sprite — avoids re-rendering 1024px PNG every frame
                    # Cache stores SRCALPHA surface so transparent regions are correct
                    # even if sprite pixels happen to match the colorkey value.
                    _cache_key = (template_key, surf_w, surf_h)
                    if _cache_key not in self._sprite_cache:
                        _scratch = pygame.Surface((surf_w, surf_h))
                        _scratch.fill(_WIZ_BG)
                        draw_enemy_silhouette(_scratch, pygame.Rect(0,0,surf_w,surf_h),
                                              template_key, knowledge_tier=1)
                        _scratch.set_colorkey(_WIZ_BG)
                        # Convert to SRCALPHA so colorkey transparency is baked in
                        _alpha = pygame.Surface((surf_w, surf_h), pygame.SRCALPHA)
                        _alpha.fill((0, 0, 0, 0))
                        _alpha.blit(_scratch, (0, 0))
                        self._sprite_cache[_cache_key] = _alpha
                    view.blit(self._sprite_cache[_cache_key], (cx_s - surf_w//2, blit_y))
                    continue

                elif icon_key == DT_TRAP:
                    # Armed trap — dark summoning glyph burned into floor
                    # Draw base glyph then add pulsing animation on top
                    from ui.dungeon_objects import draw_trap_armed as _dta
                    _dta(spr, pygame.Rect(0, 0, surf_w, surf_h), self.theme_id)
                    # Pulse the glow intensity using existing animation timer
                    pulse_scale = 0.75 + 0.25 * abs(math.sin(self.t * 3.5))
                    if pulse_scale < 0.85:
                        # Dim pass — darken glyph slightly at minimum pulse
                        dim_ov = pygame.Surface((surf_w, surf_h), pygame.SRCALPHA)
                        dim_ov.fill((0, 0, 0, int(40 * (1.0 - pulse_scale) * 2)))
                        spr.blit(dim_ov, (0, 0))

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
                elif tt == DT_FLOOR:
                    c = (88, 78, 62, 200)
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

        # ── Party figure — helm + body + directional facing indicator ──
        ppx = (px_i - x0) * ts + ts // 2
        ppy = (py_i - y0) * ts + ts // 2
        CYAN   = (0, 220, 200, 255)
        DARK_C = (0, 120, 110, 255)
        WHITE  = (240, 240, 230, 255)

        # Body: filled rounded rect (2/3 tile height below centre)
        body_w = max(4, ts // 3)
        body_h = max(4, ts // 2)
        body_r = pygame.Rect(ppx - body_w // 2, ppy - body_h // 6,
                             body_w, body_h)
        pygame.draw.rect(bg, CYAN,   body_r, border_radius=2)
        pygame.draw.rect(bg, DARK_C, body_r, 1, border_radius=2)

        # Head: small circle above body
        head_r = max(2, ts // 5)
        pygame.draw.circle(bg, CYAN,   (ppx, ppy - body_h // 6 - head_r), head_r)
        pygame.draw.circle(bg, DARK_C, (ppx, ppy - body_h // 6 - head_r), head_r, 1)

        # Facing: bright chevron / visor line pointing in view direction
        facing_len = max(3, ts // 2)
        fx = ppx + int(math.cos(self.angle) * facing_len)
        fy = ppy + int(math.sin(self.angle) * facing_len)
        pygame.draw.line(bg, WHITE, (ppx, ppy), (fx, fy), 2)
        # Chevron tip
        perp_x = -math.sin(self.angle)
        perp_y =  math.cos(self.angle)
        cw = max(1, ts // 5)
        c1 = (fx - int(math.cos(self.angle) * cw) + int(perp_x * cw),
              fy - int(math.sin(self.angle) * cw) + int(perp_y * cw))
        c2 = (fx - int(math.cos(self.angle) * cw) - int(perp_x * cw),
              fy - int(math.sin(self.angle) * cw) - int(perp_y * cw))
        pygame.draw.polygon(bg, WHITE, [(fx, fy), c1, c2])
        pygame.draw.rect(bg, (100,90,72,200), (0,0,cols*ts,rows*ts), 1)

        surface.blit(bg, (MM_X, MM_Y))
        font = get_font(14)
        lbl  = font.render(f"Floor {self.dungeon.current_floor}", True, (170,160,130))
        surface.blit(lbl, (MM_X+2, MM_Y+rows*ts+2))

    # ─────────────────────────────────────────────────────────
    #  HUD
    # ─────────────────────────────────────────────────────────

    def _draw_hud(self, surface, mx, my):
        by = SCREEN_H - HUD_H
        pygame.draw.rect(surface, (14,11,8), (0, by, SCREEN_W, HUD_H))
        pygame.draw.line(surface, GOLD, (0, by), (SCREEN_W, by), 2)

        fb = get_font(16, bold=True)
        fs = get_font(14)

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
                _hp_surf = fs.render(f"{cur_hp}/{max_hp}", True, (190,150,145))
                # Right-align text to bar end so all cards look uniform
                _hp_tx = text_x + bar_w - _hp_surf.get_width()
                surface.blit(_hp_surf, (max(text_x, _hp_tx), cy_h+8))
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
                    _rs_surf = fs.render(f"{rk}: {cur_r}/{max_r}", True, text_c)
                    _rs_tx = text_x + bar_w - _rs_surf.get_width()
                    surface.blit(_rs_surf, (max(text_x, _rs_tx), cy_h+8))

        # Buttons — vertical stack in right panel (x=MM_X), below minimap
        # This keeps them completely clear of the character card area (x=0-1100)
        _btn_x = MM_X + 4
        _btn_w = SCREEN_W - MM_X - 8
        _btn_y = by + 4
        bdata = [
            ("C Camp",   pygame.Rect(_btn_x, _btn_y,      _btn_w, 24)),
            ("M Menu",   pygame.Rect(_btn_x, _btn_y + 30, _btn_w, 24)),
            ("T Disarm", pygame.Rect(_btn_x, _btn_y + 60, _btn_w, 24)),
        ]
        for lbl, r in bdata:
            hov = r.collidepoint(mx,my)
            pygame.draw.rect(surface, (40,30,18) if not hov else (62,46,24), r, border_radius=3)
            pygame.draw.rect(surface, GOLD if hov else (75,60,38), r, 1, border_radius=3)
            surface.blit(fb.render(lbl, True, GOLD if hov else CREAM), (r.x+6, r.y+5))

        info_text = f"{self.dungeon.dungeon_id.replace('_',' ').title()}  ·  Floor {self.dungeon.current_floor}"
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

        ctrl = fs.render("WASD Move  QE/←→ Turn  ENTER Interact  C Camp  M Menu  T Disarm", True, (72,64,50))
        surface.blit(ctrl, (VP_X+4, by+3))

    # ─────────────────────────────────────────────────────────
    #  DIALOGS
    # ─────────────────────────────────────────────────────────


    def _draw_interactable_modal(self, surface, mx, my):
        """Draw the fountain/shrine/altar interaction modal."""
        data = self.interactable_modal
        if not data:
            return
        import pygame
        from ui.renderer import SCREEN_W, SCREEN_H, GOLD, CREAM, GREY, GREEN, RED, ORANGE
        from ui.renderer import draw_text, draw_button

        subtype = data.get("subtype", "")
        name    = data.get("name", "Strange Object")
        hint    = data.get("hint", "")
        desc    = data.get("description", hint)

        # Color scheme by subtype
        COLOR_MAP = {
            "healing_pool": ((80, 200, 255),   "🌊 Healing Pool"),
            "mp_shrine":    ((140, 100, 255),   "✨ Arcane Shrine"),
            "cursed_altar": ((180, 60,  220),   "🔮 Dark Altar"),
        }
        accent, icon_label = COLOR_MAP.get(subtype, (GOLD, "❓ Object"))

        # Modal box
        W, H = 520, 220
        mx2  = SCREEN_W // 2 - W // 2
        my2  = SCREEN_H // 2 - H // 2
        box  = pygame.Rect(mx2, my2, W, H)
        pygame.draw.rect(surface, (18, 14, 30), box, border_radius=8)
        pygame.draw.rect(surface, accent, box, 2, border_radius=8)

        # Header
        draw_text(surface, name,        box.x + 16, box.y + 14, accent, 20, bold=True)
        draw_text(surface, icon_label,  box.x + 16, box.y + 38, GREY,   13)

        # Description — what does this object do?
        EFFECT_DESC = {
            "healing_pool": f"Restores {int(data.get('heal_pct', 0.30)*100)}% HP to the entire party. Single use.",
            "mp_shrine":    f"Restores {int(data.get('restore_pct', 0.25)*100)}% SP/MP/Ki to the entire party. Single use.",
            "cursed_altar": "Offers dark power — may grant HP or curse the party. Risky. Single use.",
        }
        effect_str = EFFECT_DESC.get(subtype, desc or "An ancient object of unknown purpose.")
        draw_text(surface, effect_str, box.x + 16, box.y + 65, CREAM, 13, max_width=W - 32)

        # Flavour hint
        if hint and hint != effect_str:
            draw_text(surface, f'"{hint}"', box.x + 16, box.y + 105, (140, 130, 160), 12,
                      max_width=W - 32)

        # Buttons
        use_btn  = pygame.Rect(box.x + 40,      box.y + H - 55, 180, 38)
        leave_btn= pygame.Rect(box.x + W - 220, box.y + H - 55, 180, 38)
        draw_button(surface, use_btn,   "Use",   hover=use_btn.collidepoint(mx, my),  size=15)
        draw_button(surface, leave_btn, "Leave", hover=leave_btn.collidepoint(mx, my), size=15)

        self._interactable_use_btn   = use_btn
        self._interactable_leave_btn = leave_btn

    def _handle_interactable_modal_click(self, mx, my):
        """Handle clicks inside the interactable modal."""
        import pygame
        use_btn   = getattr(self, "_interactable_use_btn",   None)
        leave_btn = getattr(self, "_interactable_leave_btn", None)

        if leave_btn and leave_btn.collidepoint(mx, my):
            self.interactable_modal = None
            return None

        if use_btn and use_btn.collidepoint(mx, my):
            data = self.interactable_modal
            self.interactable_modal = None
            return {"type": "use_interactable", "data": data}

        return None  # click inside modal but not on a button — absorb it

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

        ft  = get_font(18, bold=True)
        fm  = get_font(14)
        fsm = get_font(12)

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
        ft = get_font(18, bold=True)
        fb = get_font(13)
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

    # ─────────────────────────────────────────────────────────
    #  SPIRE → THRONE CHOICE MODAL
    # ─────────────────────────────────────────────────────────
    def _draw_spire_choice_modal(self, surface, mx, my):
        """Post-Spire choice: descend to Shadow Throne now or return to surface."""
        import pygame
        from ui.renderer import (SCREEN_W, SCREEN_H, GOLD, CREAM, GREY,
                                 draw_text, draw_button, get_font)
        if not self.spire_choice_modal:
            return

        # Dim overlay
        dim = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        dim.fill((0, 0, 0, 190))
        surface.blit(dim, (0, 0))

        W, H = 700, 340
        bx = SCREEN_W // 2 - W // 2
        by = SCREEN_H // 2 - H // 2
        box = pygame.Rect(bx, by, W, H)
        pygame.draw.rect(surface, (10, 6, 20), box, border_radius=10)
        pygame.draw.rect(surface, GOLD, box, 2, border_radius=10)
        # Gold top accent bar
        pygame.draw.rect(surface, (180, 140, 40), (bx, by, W, 6), border_radius=10)

        # Header
        header = "✦  THE LINGERING WILL IS BROKEN  ✦"
        hw = get_font(15).size(header)[0]
        draw_text(surface, header, bx + (W - hw) // 2, by + 18, GOLD, 15, bold=True)

        pygame.draw.line(surface, (60, 50, 80), (bx + 20, by + 44), (bx + W - 20, by + 44))

        # Body text
        body_lines = [
            "The Spire's binding is undone. Maren seals the anchor points.",
            "Ahead, the Shadow Throne lies open — the seat of the Fading itself.",
            "The wards will hold only as long as the Throne remains uncontested.",
            "",
            "You may press on while the path is clear,",
            "or return to the surface to rest and resupply.",
        ]
        ty = by + 56
        for line in body_lines:
            if line:
                draw_text(surface, line, bx + 28, ty, CREAM if "You may" not in line else (200, 180, 120),
                          13, max_width=W - 56)
            ty += 20

        # Buttons
        btn_y = by + H - 68
        descend_btn = pygame.Rect(bx + 40,      btn_y, 280, 46)
        surface_btn = pygame.Rect(bx + W - 320, btn_y, 280, 46)

        dh = descend_btn.collidepoint(mx, my)
        sh = surface_btn.collidepoint(mx, my)

        # Descend button — more prominent
        pygame.draw.rect(surface, (40, 20, 60) if dh else (28, 14, 42), descend_btn, border_radius=6)
        pygame.draw.rect(surface, (180, 100, 255) if dh else (120, 70, 180), descend_btn, 2, border_radius=6)
        dlabel = "⬇  Descend to Shadow Throne"
        dw = get_font(14).size(dlabel)[0]
        draw_text(surface, dlabel, descend_btn.x + (descend_btn.w - dw) // 2,
                  descend_btn.y + 15, (200, 140, 255) if dh else (160, 110, 220), 14, bold=True)

        # Return button
        pygame.draw.rect(surface, (20, 30, 20) if sh else (14, 20, 14), surface_btn, border_radius=6)
        pygame.draw.rect(surface, (100, 180, 100) if sh else (60, 120, 60), surface_btn, 2, border_radius=6)
        slabel = "↑  Return to surface"
        sw = get_font(14).size(slabel)[0]
        draw_text(surface, slabel, surface_btn.x + (surface_btn.w - sw) // 2,
                  surface_btn.y + 15, (140, 220, 140) if sh else (100, 170, 100), 14, bold=True)

        self._spire_descend_btn = descend_btn
        self._spire_surface_btn = surface_btn

    def _handle_spire_choice_click(self, mx, my):
        """Handle clicks on the Spire->Throne choice modal."""
        descend_btn = getattr(self, "_spire_descend_btn", None)
        surface_btn = getattr(self, "_spire_surface_btn", None)
        if descend_btn and descend_btn.collidepoint(mx, my):
            self.spire_choice_modal = None
            return {"type": "spire_descend_throne"}
        if surface_btn and surface_btn.collidepoint(mx, my):
            self.spire_choice_modal = None
            return {"type": "spire_return_surface"}
        return None  # click inside modal but not on a button — consume

    def _draw_scroll_modal(self, surface, mx, my):
        """Draw a parchment/stone scroll overlay when the party finds a note."""
        import math as _m
        m = self.scroll_modal
        title = m.get("title", "")
        lines = m.get("lines", [])
        is_wall = m.get("wall_inscription", False)

        # ── Modal geometry — centred in the 3D viewport ──────────────────
        PAD   = 28
        MW    = min(640, VP_W - 80)
        MH    = min(480, VP_H - 60)
        MX    = VP_X + VP_W // 2 - MW // 2
        MY    = VP_Y + VP_H // 2 - MH // 2

        # ── Dim the viewport behind the scroll ───────────────────────────
        dim = pygame.Surface((VP_W, VP_H), pygame.SRCALPHA)
        dim.fill((0, 0, 0, 160))
        surface.blit(dim, (VP_X, VP_Y))

        if is_wall:
            # Stone wall inscription look
            bg_col    = (42, 35, 28)
            border1   = (90, 75, 55)
            border2   = (60, 50, 38)
            title_col = (200, 175, 120)
            text_col  = (175, 155, 110)
            hint_col  = (100, 88, 65)
            # Stone texture — horizontal score lines
            pygame.draw.rect(surface, bg_col,  (MX, MY, MW, MH), border_radius=4)
            pygame.draw.rect(surface, border1, (MX, MY, MW, MH), 3, border_radius=4)
            pygame.draw.rect(surface, border2, (MX+3, MY+3, MW-6, MH-6), 1, border_radius=3)
            for sy2 in range(MY + 12, MY + MH - 12, 14):
                pygame.draw.line(surface, (50, 42, 33), (MX+8, sy2), (MX+MW-8, sy2))
            # Chisel-mark icon top-centre
            icon_x = MX + MW // 2 - 10
            pygame.draw.line(surface, border1, (icon_x, MY+8), (icon_x+20, MY+8), 2)
            pygame.draw.line(surface, border1, (icon_x+10, MY+6), (icon_x+10, MY+14), 2)
        else:
            # Parchment scroll look
            bg_col    = (58, 46, 28)
            scroll_bg = (220, 195, 145)
            edge_col  = (175, 140, 85)
            title_col = (55, 35, 12)
            text_col  = (45, 30, 10)
            hint_col  = (120, 95, 55)
            # Outer shadow
            shd = pygame.Surface((MW+6, MH+6), pygame.SRCALPHA)
            shd.fill((0,0,0,80))
            surface.blit(shd, (MX-3, MY-3))
            # Parchment body
            pygame.draw.rect(surface, scroll_bg, (MX, MY, MW, MH), border_radius=6)
            pygame.draw.rect(surface, edge_col,  (MX, MY, MW, MH), 2, border_radius=6)
            # Rolled-edge bars top and bottom
            for bar_y, shade in [(MY, 0.80), (MY+MH-18, 0.85)]:
                bar_col = tuple(int(c*shade) for c in scroll_bg)
                pygame.draw.rect(surface, bar_col, (MX, bar_y, MW, 18), border_radius=6)
                pygame.draw.rect(surface, edge_col, (MX, bar_y, MW, 18), 1, border_radius=6)
            # Parchment grain lines
            for sy2 in range(MY+22, MY+MH-22, 18):
                a = 18 + int(10 * abs(_m.sin(sy2 * 0.3)))
                grain_c = tuple(max(0, int(c*0.88)) for c in scroll_bg)
                pygame.draw.line(surface, grain_c, (MX+12, sy2), (MX+MW-12, sy2))
            # Wax-seal decoration centre-top (red circle with ❧)
            seal_x, seal_y = MX + MW//2, MY + 18
            pygame.draw.circle(surface, (160, 40, 40), (seal_x, seal_y), 14)
            pygame.draw.circle(surface, (200, 60, 60), (seal_x, seal_y), 14, 2)
            pygame.draw.circle(surface, (220, 80, 80), (seal_x-3, seal_y-3), 5)

        # ── Title ────────────────────────────────────────────────────────
        font_title = get_font(17, bold=True)
        font_body  = get_font(14)
        font_hint  = get_font(11)

        ty = MY + PAD + (8 if not is_wall else 4)
        if title:
            ts = font_title.render(title, True, title_col)
            surface.blit(ts, (MX + MW//2 - ts.get_width()//2, ty))
            ty += ts.get_height() + 6
            # Divider
            div_col = border1 if is_wall else edge_col
            pygame.draw.line(surface, div_col, (MX+PAD, ty), (MX+MW-PAD, ty), 1)
            ty += 10

        # ── Body text ────────────────────────────────────────────────────
        max_text_h = MY + MH - PAD - 30
        for line in lines:
            if ty >= max_text_h:
                break
            if line == "":
                ty += 8
                continue
            ts = font_body.render(line, True, text_col)
            surface.blit(ts, (MX + PAD, ty))
            ty += ts.get_height() + 4

        # ── Dismiss hint ─────────────────────────────────────────────────
        hint = "[ SPACE / ENTER / CLICK  to close ]"
        hs = font_hint.render(hint, True, hint_col)
        surface.blit(hs, (MX + MW//2 - hs.get_width()//2, MY + MH - 22))

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
        if self.show_camp_confirm or self.show_stairs_confirm or self.chest_modal or self.scroll_modal:
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
        if self.show_camp_confirm or self.show_stairs_confirm or self.chest_modal or self.scroll_modal:
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
            # Play footstep sound on any movement (move or turn)
            try:
                import core.sound as _sfx
                _sfx.play("step")
            except Exception:
                pass

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

        # ESC, SPACE, RETURN all dismiss scroll_modal — must be before the blanket guard
        if self.scroll_modal:
            if key in (pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN):
                self.scroll_modal = None
            return None   # all other keys blocked while modal is open

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

        if self.show_camp_confirm or self.show_stairs_confirm or self.chest_modal or self.scroll_modal:
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
        if key == pygame.K_SPACE:
            # Skip turn — costs a turn, enemies may move
            ev = self.dungeon.wait()
            if ev and ev.get("type") != "waited":
                return ev
            return None
        if key == pygame.K_c:
            nearby = self.dungeon.enemies_nearby(threat_radius=6)
            if nearby:
                self.show_event(
                    f"Cannot camp — {len(nearby)} enem{'y' if len(nearby)==1 else 'ies'} "
                    f"within 6 tiles! Dispatch them first.",
                    (220, 80, 80))
            else:
                self.show_camp_confirm = True
            return None
        if key == pygame.K_t:
            return self._try_disarm()
        if key == pygame.K_m:
            return {"type": "menu"}
        return None

    def handle_keyup(self, key):
        pass   # no held-key state in grid-snap mode

    def handle_keyup(self, key):
        self._keys.discard(key)

    def handle_click(self, mx, my):
        # Scroll modal intercepts all clicks
        if self.scroll_modal:
            self.scroll_modal = None
            return None

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

        if self.spire_choice_modal:
            return self._handle_spire_choice_click(mx, my)
        if self.interactable_modal:
            return self._handle_interactable_modal_click(mx, my)
        if self.chest_modal:
            return self._handle_chest_modal_click(mx, my)

        by = SCREEN_H - HUD_H
        _btn_x = MM_X + 4
        _btn_w = SCREEN_W - MM_X - 8
        _btn_y = by + 4
        if pygame.Rect(_btn_x, _btn_y,      _btn_w, 24).collidepoint(mx,my):
            nearby = self.dungeon.enemies_nearby(threat_radius=6)
            if nearby:
                self.show_event(
                    f"Cannot camp — {len(nearby)} enem{'y' if len(nearby)==1 else 'ies'} "
                    f"within 6 tiles!",
                    (220, 80, 80))
                return None
            return {"type": "camp"}
        if pygame.Rect(_btn_x, _btn_y + 30, _btn_w, 24).collidepoint(mx,my):
            return {"type": "menu"}
        if pygame.Rect(_btn_x, _btn_y + 60, _btn_w, 24).collidepoint(mx,my):
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
                    # Play sound based on outcome
                    try:
                        import core.sound as _sfx
                        _sfx.play("ui_confirm" if success else "trap_trigger")
                    except Exception:
                        pass
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
                        try:
                            import core.sound as _sfx; _sfx.play("ui_confirm")
                        except Exception:
                            pass
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

