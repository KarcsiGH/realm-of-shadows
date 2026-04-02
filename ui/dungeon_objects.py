"""
dungeon_objects.py — Procedural drawing for dungeon interactive objects.

All functions signature: draw_X(surface, rect, theme=None)
Called from dungeon_ui.py sprite loop; drawn at whatever size the raycaster requests.
"""

import math
import pygame

# ── Theme palettes (mirrors THEMES in dungeon_ui.py) ─────────────────────────
_THEMES = {
    "cave":   {"light":(110,90,70),  "dark":(45,35,26),  "mid":(78,62,46)},
    "mine":   {"light":(120,100,75), "dark":(55,42,30),  "mid":(86,68,50)},
    "crypt":  {"light":(80,88,120),  "dark":(32,36,55),  "mid":(54,60,88)},
    "ruins":  {"light":(115,95,72),  "dark":(50,40,30),  "mid":(80,64,48)},
    "tower":  {"light":(90,82,130),  "dark":(38,34,62),  "mid":(62,58,98)},
    "spider": {"light":(62,58,54),   "dark":(24,20,18),  "mid":(42,38,34)},
}
_DEFAULT_THEME = "cave"

DARK = (4, 2, 8)

# ── Helpers ───────────────────────────────────────────────────────────────────
def _lerp(a, b, t):
    return a + (b - a) * t

def _lerp_col(c1, c2, t):
    return tuple(int(_lerp(c1[i], c2[i], t)) for i in range(3))

def _clamp(c):
    return tuple(max(0, min(255, int(v))) for v in c)

def _seeded(seed, row, col, mn, mx):
    h = (seed ^ (row * 2654435761) ^ (col * 2246822519)) & 0xFFFFFF
    return mn + (h % max(1, mx - mn + 1))


# ── Irregular stone masonry ───────────────────────────────────────────────────
def _draw_masonry(surf, ox, oy_start, oy_end,
                  get_left, get_right,
                  base_col, mortar_col,
                  base_bh, base_bw, seed):
    """Draw irregular stone masonry blocks between get_left(y) and get_right(y)."""
    y = oy_start; row = 0
    while y < oy_end:
        rh = _seeded(seed, row, 999, int(base_bh * 0.65), int(base_bh * 1.55))
        rh = max(2, rh); y2 = min(oy_end, y + rh)
        lx = int(get_left(y)); rx = int(get_right(y))
        if rx <= lx:
            y = y2; row += 1; continue
        offset = _seeded(seed, row, 998, base_bw // 3, base_bw * 2 // 3) if row % 2 else 0
        ci = 0; x = lx - offset
        while x < rx:
            bw = _seeded(seed, row, ci, int(base_bw * 0.6), int(base_bw * 1.5))
            bw = max(3, bw)
            bx = max(lx, x); bx2 = min(rx, x + bw - 1)
            if bx2 > bx:
                v  = _seeded(seed, row * 37 + ci, 0, -18, 18)
                sp = _seeded(seed, row + ci * 7, 1, 0, 12)
                if sp == 0:   v -= 14
                elif sp == 1: v += 10
                bc = _clamp(tuple(c + v for c in base_col))
                pygame.draw.rect(surf, bc, (bx, y, bx2 - bx, y2 - y - 1))
            x += bw; ci += 1
        pmx = lx; st = max(8, (rx - lx) // 6)
        while pmx < rx:
            nmx = min(rx, pmx + st)
            j = _seeded(seed, row * 13 + pmx, 3, -1, 1)
            pygame.draw.line(surf, mortar_col, (pmx, y2 - 1 + j), (nmx, y2 - 1 + j), 1)
            pmx = nmx
        x = lx - offset; ci = 0
        while x < rx:
            bw = _seeded(seed, row, ci, int(base_bw * 0.6), int(base_bw * 1.5))
            bw = max(3, bw); vx = x + bw - 1
            if lx < vx < rx:
                jv = _seeded(seed, row * 17 + ci, 4, -1, 1)
                pygame.draw.line(surf, mortar_col, (vx + jv, y), (vx + jv, y2 - 2), 1)
            x += bw; ci += 1
        y = y2; row += 1


# ── Torch sconce ──────────────────────────────────────────────────────────────
def _draw_torch(surf, wall_x, torch_y, size):
    if size < 48:
        return
    s = size / 180.0
    IRON = (80, 82, 88); IRON_L = (115, 118, 126)
    al = int(10 * s); ay = torch_y + int(4 * s)
    pygame.draw.rect(surf, IRON,   (wall_x, ay, al, max(2, int(3 * s))))
    pygame.draw.rect(surf, IRON_L, (wall_x, ay, al, max(2, int(3 * s))), 1)
    cx2 = wall_x + al - int(2 * s); cw = max(3, int(5 * s)); ch = max(3, int(5 * s))
    pygame.draw.rect(surf, IRON,   (cx2, ay - ch // 2, cw, ch))
    pygame.draw.rect(surf, IRON_L, (cx2, ay - ch // 2, cw, ch), 1)
    fcx = cx2 + cw // 2; fby = ay - ch // 2
    fh = max(4, int(14 * s)); fw = max(2, int(5 * s))
    pygame.draw.polygon(surf, (210, 75, 15), [
        (fcx - fw, fby), (fcx + fw, fby),
        (fcx + fw // 2, fby - fh * 6 // 10), (fcx, fby - fh),
        (fcx - fw // 2, fby - fh * 6 // 10)])
    pygame.draw.polygon(surf, (255, 160, 20), [
        (fcx - fw // 2, fby), (fcx + fw // 2, fby), (fcx, fby - fh * 8 // 10)])
    pygame.draw.circle(surf, (255, 220, 100), (fcx, fby - fh + 1), max(1, int(2 * s)))


# ══════════════════════════════════════════════════════════════════════════════
#  STAIRS
# ══════════════════════════════════════════════════════════════════════════════

def draw_stairs_up(surf, r, theme=None):
    """
    Stairs going up — viewed from the base.
    Wide at bottom (near), narrow at top (far).
    Steps end in an expanding black void that fans to full image width.
    Torch sconce on left wall.
    """
    w, h = r.w, r.h
    ox, oy = r.x, r.y
    th = _THEMES.get(theme or _DEFAULT_THEME, _THEMES[_DEFAULT_THEME])
    light, dark, mid = th["light"], th["dark"], th["mid"]
    shadow = _clamp(tuple(c - 18 for c in dark))
    mortar = _clamp(tuple(c - 22 for c in dark))

    wall_near_w = int(w * 0.19)   # small wall at near (bottom) → wide corridor
    wall_far_w  = int(w * 0.46)   # large wall at far  (top)   → narrow corridor

    def lwr(y): return ox + int(_lerp(wall_far_w, wall_near_w, (y - oy) / h))
    def rwl(y): return ox + w - int(_lerp(wall_far_w, wall_near_w, (y - oy) / h))

    y_void = oy + int(h * 0.20)   # void starts here

    pygame.draw.rect(surf, DARK, (ox, oy, w, h))

    lit  = _lerp_col(mid, light, 0.55)
    shd  = _lerp_col(dark, mid,  0.28)
    seed_l = hash((theme, "ul")) & 0xFFFFFF
    seed_r = hash((theme, "ur")) & 0xFFFFFF
    bh = max(3, w // 15); bw = max(5, w // 9)

    _draw_masonry(surf, ox, oy, oy + h,
                  lambda y: ox, lwr, lit, mortar, bh, bw, seed_l)
    _draw_masonry(surf, ox, oy, oy + h,
                  rwl, lambda y: ox + w, shd, mortar, bh, bw, seed_r)

    # Steps: wide at bottom, narrow toward y_void
    STEPS = 7
    for i in range(STEPS):
        near_y = int(_lerp(oy + h, y_void, i / STEPS))
        far_y  = int(_lerp(oy + h, y_void, (i + 1) / STEPS))
        lnear = lwr(near_y); rnear = rwl(near_y)
        lfar  = lwr(far_y);  rfar  = rwl(far_y)

        brightness = _lerp(0.18, 0.48, i / (STEPS - 1))
        sv = _seeded(hash((theme, "s", i)), 0, 0, -8, 8)
        sc = _clamp(tuple(c + sv for c in _lerp_col(shadow, light, brightness)))
        rc = _clamp(_lerp_col(DARK, shadow, brightness * 0.55))

        pygame.draw.polygon(surf, sc,
            [(lnear, near_y), (rnear, near_y), (rfar, far_y), (lfar, far_y)])
        rh2 = max(1, (near_y - far_y) // 3)
        pygame.draw.polygon(surf, rc,
            [(lnear, near_y), (rnear, near_y),
             (rnear, near_y + rh2), (lnear, near_y + rh2)])
        pygame.draw.polygon(surf, shadow,
            [(lnear, near_y), (rnear, near_y), (rfar, far_y), (lfar, far_y)], 1)
        ec = _clamp(tuple(c + 26 for c in sc))
        pygame.draw.line(surf, ec, (lnear + 1, near_y + 1), (rnear - 1, near_y + 1), 1)

    # Expanding black void — starts at corridor width at y_void, fans to full width
    lx_v = lwr(y_void); rx_v = rwl(y_void)
    pygame.draw.polygon(surf, DARK,
        [(ox, oy), (ox + w, oy), (rx_v, y_void), (lx_v, y_void)])
    pygame.draw.line(surf, shadow, (lx_v, y_void), (rx_v, y_void), 2)

    # Torch on left wall
    _draw_torch(surf, ox, oy + int(h * 0.35), w)


def draw_stairs_down(surf, r, theme=None):
    """
    Stairs going down — viewed from the top landing.
    Wide at bottom (near base of stairs), narrow toward top.
    A constant-width black rectangle (doorway in the far wall) sits above
    the top step and extends to the top of the image.
    """
    w, h = r.w, r.h
    ox, oy = r.x, r.y
    th = _THEMES.get(theme or _DEFAULT_THEME, _THEMES[_DEFAULT_THEME])
    light, dark, mid = th["light"], th["dark"], th["mid"]
    shadow = _clamp(tuple(c - 18 for c in dark))
    mortar = _clamp(tuple(c - 22 for c in dark))

    wall_near_w = int(w * 0.19)
    wall_far_w  = int(w * 0.46)

    def lwr(y): return ox + int(_lerp(wall_far_w, wall_near_w, (y - oy) / h))
    def rwl(y): return ox + w - int(_lerp(wall_far_w, wall_near_w, (y - oy) / h))

    y_stop = oy + int(h * 0.48)   # steps stop here
    lx_stop = lwr(y_stop); rx_stop = rwl(y_stop)
    rect_w = rx_stop - lx_stop; rect_x = lx_stop

    pygame.draw.rect(surf, DARK, (ox, oy, w, h))

    lit  = _lerp_col(mid, light, 0.55)
    shd  = _lerp_col(dark, mid,  0.28)
    seed_l = hash((theme, "dl")) & 0xFFFFFF
    seed_r = hash((theme, "dr")) & 0xFFFFFF
    bh = max(3, w // 15); bw = max(5, w // 9)

    _draw_masonry(surf, ox, oy, oy + h,
                  lambda y: ox, lwr, lit, mortar, bh, bw, seed_l)
    _draw_masonry(surf, ox, oy, oy + h,
                  rwl, lambda y: ox + w, shd, mortar, bh, bw, seed_r)

    # Constant-width black rectangle — the doorway in the far wall
    if rect_w > 0:
        pygame.draw.rect(surf, DARK, (rect_x, oy, rect_w, y_stop - oy))
        pygame.draw.line(surf, shadow,
                         (rect_x, y_stop), (rect_x + rect_w, y_stop), 2)
        edge_col = _clamp(tuple(c - 10 for c in dark))
        pygame.draw.line(surf, edge_col, (rect_x, oy),         (rect_x, y_stop), 1)
        pygame.draw.line(surf, edge_col, (rect_x + rect_w, oy), (rect_x + rect_w, y_stop), 1)

    # Steps: wide at bottom, narrow toward y_stop
    STEPS = 5
    for i in range(STEPS):
        near_y = int(_lerp(oy + h, y_stop, i / STEPS))
        far_y  = int(_lerp(oy + h, y_stop, (i + 1) / STEPS))
        lnear = lwr(near_y); rnear = rwl(near_y)
        lfar  = lwr(far_y);  rfar  = rwl(far_y)

        brightness = _lerp(0.26, 0.06, i / (STEPS - 1))
        sv = _seeded(hash((theme, "ds", i)), 0, 0, -6, 6)
        sc = _clamp(tuple(c + sv for c in
                    _clamp(_lerp_col(DARK, dark, brightness * 3.2))))
        rc = _clamp(_lerp_col(DARK, shadow, brightness * 1.5))

        pygame.draw.polygon(surf, sc,
            [(lnear, near_y), (rnear, near_y), (rfar, far_y), (lfar, far_y)])
        rh2 = max(1, (far_y - near_y) // 3)
        pygame.draw.polygon(surf, rc,
            [(lnear, near_y), (rnear, near_y),
             (rnear, near_y + rh2), (lnear, near_y + rh2)])
        pygame.draw.polygon(surf, shadow,
            [(lnear, near_y), (rnear, near_y), (rfar, far_y), (lfar, far_y)], 1)
        if brightness > 0.10:
            ec = _clamp(tuple(c + 18 for c in sc))
            pygame.draw.line(surf, ec,
                             (lnear + 1, near_y + 1), (rnear - 1, near_y + 1), 1)


# ══════════════════════════════════════════════════════════════════════════════
#  SHRINE  (Option B — stone arch niche with glowing idol)
# ══════════════════════════════════════════════════════════════════════════════

def draw_shrine_active(surf, r, theme=None):
    w, h = r.w, r.h; cx = r.x + w // 2
    th = _THEMES.get(theme or _DEFAULT_THEME, _THEMES[_DEFAULT_THEME])
    light, dark, mid = th["light"], th["dark"], th["mid"]

    niche_w = int(w * 0.68); niche_h = int(h * 0.72)
    niche_x = cx - niche_w // 2; niche_y = r.y + int(h * 0.06)
    pygame.draw.rect(surf, _clamp(tuple(c // 2 for c in dark)),
                     (niche_x, niche_y, niche_w, niche_h), border_radius=4)

    arch_w = int(w * 0.54); arch_h = int(h * 0.62)
    arch_x = cx - arch_w // 2; arch_y = niche_y + int(h * 0.04)
    for i in range(5, 0, -1):
        glow_col = (min(255, 100 + i * 18), min(255, 40 + i * 10), min(255, 200 + i * 8))
        pygame.draw.rect(surf, glow_col,
            (arch_x + i * 2, arch_y + i * 2, arch_w - i * 4, arch_h - i * 4),
            border_radius=i * 3)
    pygame.draw.rect(surf, (80, 30, 160),
                     (arch_x + 10, arch_y + 10, arch_w - 20, arch_h - 20),
                     border_radius=6)
    pygame.draw.rect(surf, _lerp_col(dark, light, 0.6),
                     (arch_x, arch_y, arch_w, arch_h),
                     4, border_radius=int(arch_w * 0.4))
    pygame.draw.rect(surf, _clamp(tuple(min(255, c + 30) for c in light)),
                     (arch_x, arch_y, arch_w, arch_h),
                     2, border_radius=int(arch_w * 0.4))

    idol_cx, idol_cy = cx, niche_y + int(niche_h * 0.42)
    idol_r = int(w * 0.12)
    for a in range(0, 360, 45):
        rx2 = idol_cx + int(math.cos(math.radians(a)) * idol_r * 1.8)
        ry2 = idol_cy + int(math.sin(math.radians(a)) * idol_r * 1.8)
        pygame.draw.line(surf, (160, 80, 255), (idol_cx, idol_cy), (rx2, ry2),
                         max(1, w // 55))
    diamond_pts = [(idol_cx, idol_cy - idol_r),
                   (idol_cx + int(idol_r * 0.6), idol_cy),
                   (idol_cx, idol_cy + idol_r),
                   (idol_cx - int(idol_r * 0.6), idol_cy)]
    pygame.draw.polygon(surf, (200, 140, 255), diamond_pts)
    pygame.draw.polygon(surf, (255, 220, 255), diamond_pts, 2)
    pygame.draw.circle(surf, (255, 255, 255), (idol_cx, idol_cy), max(2, idol_r // 3))

    base_w = int(w * 0.84); base_h = int(h * 0.14)
    pygame.draw.rect(surf, _lerp_col(dark, mid, 0.5),
                     (cx - base_w // 2, niche_y + niche_h - 4, base_w, base_h),
                     border_radius=3)
    pygame.draw.rect(surf, _lerp_col(mid, light, 0.4),
                     (cx - base_w // 2, niche_y + niche_h - 4, base_w, base_h),
                     2, border_radius=3)


def draw_shrine_used(surf, r, theme=None):
    w, h = r.w, r.h; cx = r.x + w // 2
    th = _THEMES.get(theme or _DEFAULT_THEME, _THEMES[_DEFAULT_THEME])
    light, dark, mid = th["light"], th["dark"], th["mid"]

    niche_w = int(w * 0.68); niche_h = int(h * 0.72)
    niche_x = cx - niche_w // 2; niche_y = r.y + int(h * 0.06)
    pygame.draw.rect(surf, _clamp(tuple(c // 2 for c in dark)),
                     (niche_x, niche_y, niche_w, niche_h), border_radius=4)

    arch_w = int(w * 0.54); arch_h = int(h * 0.62)
    arch_x = cx - arch_w // 2; arch_y = niche_y + int(h * 0.04)
    pygame.draw.rect(surf, _clamp(tuple(c // 3 for c in dark)),
                     (arch_x + 10, arch_y + 10, arch_w - 20, arch_h - 20),
                     border_radius=6)
    pygame.draw.rect(surf, _lerp_col(dark, mid, 0.4),
                     (arch_x, arch_y, arch_w, arch_h),
                     3, border_radius=int(arch_w * 0.4))

    # Dark cracked idol
    idol_cx, idol_cy = cx, niche_y + int(niche_h * 0.42)
    idol_r = int(w * 0.10)
    pygame.draw.polygon(surf, _lerp_col(DARK, dark, 0.5), [
        (idol_cx, idol_cy - idol_r),
        (idol_cx + int(idol_r * 0.6), idol_cy),
        (idol_cx, idol_cy + idol_r),
        (idol_cx - int(idol_r * 0.6), idol_cy)])
    pygame.draw.line(surf, _clamp(tuple(c - 5 for c in dark)),
                     (idol_cx, idol_cy - idol_r + 2),
                     (idol_cx + 3, idol_cy + idol_r - 2), max(1, w // 70))

    base_w = int(w * 0.84); base_h = int(h * 0.14)
    pygame.draw.rect(surf, _lerp_col(DARK, dark, 0.4),
                     (cx - base_w // 2, niche_y + niche_h - 4, base_w, base_h),
                     border_radius=3)


# ══════════════════════════════════════════════════════════════════════════════
#  FOUNTAIN  (Option B — jewelled pool with hovering gem, ripple rings)
# ══════════════════════════════════════════════════════════════════════════════

def draw_fountain_active(surf, r, theme=None):
    w, h = r.w, r.h; cx = r.x + w // 2
    th = _THEMES.get(theme or _DEFAULT_THEME, _THEMES[_DEFAULT_THEME])
    light, dark, mid = th["light"], th["dark"], th["mid"]

    basin_rx = int(w * 0.46); basin_ry = int(h * 0.16)
    basin_cy = r.y + int(h * 0.74)
    pygame.draw.ellipse(surf, _clamp(tuple(c - 10 for c in dark)),
        (cx - basin_rx - 4, basin_cy - basin_ry - 3,
         (basin_rx + 4) * 2, (basin_ry + 3) * 2))
    pygame.draw.ellipse(surf, _lerp_col(dark, light, 0.55),
        (cx - basin_rx, basin_cy - basin_ry, basin_rx * 2, basin_ry * 2))
    water_rx = int(basin_rx * 0.84); water_ry = int(basin_ry * 0.78)
    pygame.draw.ellipse(surf, (18, 48, 92),
        (cx - water_rx, basin_cy - water_ry, water_rx * 2, water_ry * 2))
    for i, (rscale, col) in enumerate([(0.82, (40,100,168)),
                                        (0.62, (65,140,205)),
                                        (0.40, (95,170,228))]):
        pygame.draw.ellipse(surf, col,
            (cx - int(water_rx * rscale), basin_cy - int(water_ry * rscale),
             int(water_rx * rscale * 2), int(water_ry * rscale * 2)),
            max(1, w // 70 + 1 - i))
    pygame.draw.ellipse(surf, (200, 235, 255),
        (cx - int(water_rx * 0.22), basin_cy - int(water_ry * 0.28),
         int(water_rx * 0.44), int(water_ry * 0.26)))
    pygame.draw.ellipse(surf, _clamp(tuple(min(255, c + 25) for c in light)),
        (cx - basin_rx, basin_cy - basin_ry, basin_rx * 2, max(4, basin_ry // 2)), 2)

    stub_w = int(w * 0.08); stub_h = int(h * 0.22)
    stub_y = basin_cy - basin_ry - stub_h + 4
    pygame.draw.rect(surf, _lerp_col(dark, mid, 0.5),
                     (cx - stub_w, stub_y, stub_w * 2, stub_h), border_radius=2)
    pygame.draw.rect(surf, _lerp_col(mid, light, 0.3),
                     (cx - stub_w, stub_y, stub_w * 2, stub_h), 2, border_radius=2)

    gem_cx, gem_cy = cx, stub_y - int(h * 0.06)
    gem_r = int(w * 0.10)
    for gi in range(5, 0, -1):
        pygame.draw.circle(surf,
            (max(0, 20 + gi * 15), max(0, gi * 8), max(0, 150 + gi * 18)),
            (gem_cx, gem_cy), gem_r + gi * 3)
    gem_pts = [(gem_cx, gem_cy - gem_r),
               (gem_cx + int(gem_r * 0.7), gem_cy - int(gem_r * 0.3)),
               (gem_cx + int(gem_r * 0.7), gem_cy + int(gem_r * 0.3)),
               (gem_cx, gem_cy + gem_r),
               (gem_cx - int(gem_r * 0.7), gem_cy + int(gem_r * 0.3)),
               (gem_cx - int(gem_r * 0.7), gem_cy - int(gem_r * 0.3))]
    pygame.draw.polygon(surf, (40, 180, 255), gem_pts)
    pygame.draw.polygon(surf, (140, 220, 255), gem_pts, 2)
    pygame.draw.polygon(surf, (200, 240, 255),
        [gem_pts[0], gem_pts[1], (gem_cx, gem_cy)])
    pygame.draw.circle(surf, (240, 252, 255),
                       (gem_cx, gem_cy - gem_r // 3), max(1, gem_r // 5))

    base_w = int(w * 0.72)
    pygame.draw.rect(surf, _lerp_col(DARK, dark, 0.5),
        (cx - base_w // 2, basin_cy + basin_ry, base_w, int(h * 0.08)),
        border_radius=2)


def draw_fountain_used(surf, r, theme=None):
    w, h = r.w, r.h; cx = r.x + w // 2
    th = _THEMES.get(theme or _DEFAULT_THEME, _THEMES[_DEFAULT_THEME])
    light, dark, mid = th["light"], th["dark"], th["mid"]

    basin_rx = int(w * 0.46); basin_ry = int(h * 0.16)
    basin_cy = r.y + int(h * 0.74)
    pygame.draw.ellipse(surf, _clamp(tuple(c - 12 for c in dark)),
        (cx - basin_rx - 4, basin_cy - basin_ry - 3,
         (basin_rx + 4) * 2, (basin_ry + 3) * 2))
    pygame.draw.ellipse(surf, _lerp_col(DARK, dark, 0.65),
        (cx - basin_rx, basin_cy - basin_ry, basin_rx * 2, basin_ry * 2))
    water_rx = int(basin_rx * 0.84); water_ry = int(basin_ry * 0.78)
    pygame.draw.ellipse(surf, _clamp(tuple(c - 8 for c in DARK)),
        (cx - water_rx, basin_cy - water_ry, water_rx * 2, water_ry * 2))
    pygame.draw.line(surf, _clamp(tuple(c - 4 for c in DARK)),
                     (cx - int(water_rx * 0.4), basin_cy),
                     (cx + int(water_rx * 0.3), basin_cy + int(water_ry * 0.3)),
                     max(1, w // 60))

    stub_w = int(w * 0.08); stub_h = int(h * 0.22)
    stub_y = basin_cy - basin_ry - stub_h + 4
    pygame.draw.rect(surf, _clamp(tuple(c - 6 for c in dark)),
                     (cx - stub_w, stub_y, stub_w * 2, stub_h), border_radius=2)

    base_w = int(w * 0.72)
    pygame.draw.rect(surf, _clamp(tuple(c - 6 for c in DARK)),
        (cx - base_w // 2, basin_cy + basin_ry, base_w, int(h * 0.08)),
        border_radius=2)


# ══════════════════════════════════════════════════════════════════════════════
#  TRAP  (Option D — dark summoning glyph burned into floor)
# ══════════════════════════════════════════════════════════════════════════════

def draw_trap_armed(surf, r, theme=None):
    # No background fill — let the dungeon floor show through (SRCALPHA surface)
    w, h = r.w, r.h; cx = r.x + w // 2

    scorch_rx = int(w * 0.42); scorch_ry = int(h * 0.20)
    scorch_cy = r.y + int(h * 0.62)
    pygame.draw.ellipse(surf, (22, 16, 12),
        (cx - scorch_rx, scorch_cy - scorch_ry,
         scorch_rx * 2, scorch_ry * 2))

    GLYPH = (220, 80, 30); GLYPH_G = (255, 160, 60)
    outer_r = int(w * 0.36); outer_cy = scorch_cy
    pygame.draw.ellipse(surf, GLYPH,
        (cx - outer_r, outer_cy - int(outer_r * 0.45),
         outer_r * 2, int(outer_r * 0.9)), max(2, w // 45))
    inner_r = int(outer_r * 0.65)
    pygame.draw.ellipse(surf, GLYPH,
        (cx - inner_r, outer_cy - int(inner_r * 0.45),
         inner_r * 2, int(inner_r * 0.9)), max(1, w // 60))
    for a in range(0, 360, 60):
        ax = cx + int(outer_r * math.cos(math.radians(a)))
        ay = outer_cy + int(outer_r * 0.45 * math.sin(math.radians(a)))
        bx = cx + int(inner_r * math.cos(math.radians(a + 60)))
        by = outer_cy + int(inner_r * 0.45 * math.sin(math.radians(a + 60)))
        pygame.draw.line(surf, GLYPH, (ax, ay), (bx, by), max(1, w // 60))
    centre_r = int(outer_r * 0.18)
    pygame.draw.ellipse(surf, GLYPH_G,
        (cx - centre_r, outer_cy - int(centre_r * 0.45),
         centre_r * 2, int(centre_r * 0.9)))
    pygame.draw.ellipse(surf, (255, 220, 180),
        (cx - centre_r // 2, outer_cy - int(centre_r * 0.22),
         centre_r, int(centre_r * 0.44)))
    for gi in range(3, 0, -1):
        pygame.draw.ellipse(surf,
            (max(0, 180 - gi * 50), max(0, 55 - gi * 16), 0),
            (cx - outer_r - gi * 3, outer_cy - int((outer_r + gi * 3) * 0.45),
             (outer_r + gi * 3) * 2, int((outer_r + gi * 3) * 0.9)), 1)


def draw_trap_tripped(surf, r, theme=None):
    """Tripped trap — glyph dark and inert."""
    w, h = r.w, r.h; cx = r.x + w // 2
    scorch_rx = int(w * 0.42); scorch_cy = r.y + int(h * 0.62)
    scorch_ry = int(h * 0.20)
    pygame.draw.ellipse(surf, (16, 11, 8),
        (cx - scorch_rx, scorch_cy - scorch_ry, scorch_rx * 2, scorch_ry * 2))
    outer_r = int(w * 0.36)
    pygame.draw.ellipse(surf, (55, 30, 15),
        (cx - outer_r, scorch_cy - int(outer_r * 0.45),
         outer_r * 2, int(outer_r * 0.9)), max(1, w // 55))


# ══════════════════════════════════════════════════════════════════════════════
#  CHEST  (unchanged from previous version — already approved)
# ══════════════════════════════════════════════════════════════════════════════

def draw_chest(surf, r, theme=None):
    w, h = r.w, r.h; cx = r.x + w // 2
    WOOD = (120, 72, 28); WOOD_D = (80, 46, 16); WOOD_L = (158, 100, 42)
    IRON = (80, 82, 88); IRON_L = (115, 118, 125)
    GOLD = (210, 175, 55); GOLD_L = (245, 215, 100)

    body_x = r.x + int(w * 0.08); body_y = r.y + int(h * 0.50)
    body_w = int(w * 0.84);       body_h = int(h * 0.36)
    pygame.draw.rect(surf, WOOD, (body_x, body_y, body_w, body_h), border_radius=3)
    for px in range(body_x + 8, body_x + body_w - 4, max(8, body_w // 6)):
        pygame.draw.line(surf, WOOD_D, (px, body_y + 2), (px, body_y + body_h - 2),
                         max(1, w // 60))
    band_h = max(4, h // 12)
    pygame.draw.rect(surf, IRON,
        (body_x, body_y + body_h - band_h, body_w, band_h), border_radius=2)
    pygame.draw.rect(surf, IRON_L,
        (body_x, body_y + body_h - band_h, body_w, band_h), 1, border_radius=2)
    pygame.draw.rect(surf, WOOD_D, (body_x, body_y, body_w, body_h), 2, border_radius=3)
    pygame.draw.line(surf, WOOD_L,
                     (body_x + 3, body_y + 2), (body_x + body_w - 3, body_y + 2), 2)

    lid_x = r.x + int(w * 0.06); lid_y = r.y + int(h * 0.22)
    lid_w = int(w * 0.88);       lid_h = int(h * 0.32)
    pygame.draw.rect(surf, WOOD,
        (lid_x, lid_y + lid_h // 3, lid_w, lid_h * 2 // 3), border_radius=3)
    pygame.draw.ellipse(surf, WOOD, (lid_x, lid_y, lid_w, lid_h * 2 // 3))
    for px in range(lid_x + 8, lid_x + lid_w - 4, max(8, lid_w // 6)):
        pygame.draw.line(surf, WOOD_D,
            (px, lid_y + lid_h // 3 + 2), (px, lid_y + lid_h - 2), max(1, w // 60))
    band2_y = lid_y + lid_h * 2 // 5
    pygame.draw.rect(surf, IRON,   (lid_x, band2_y, lid_w, band_h), border_radius=1)
    pygame.draw.rect(surf, IRON_L, (lid_x, band2_y, lid_w, band_h), 1, border_radius=1)
    pygame.draw.rect(surf, WOOD_D, (lid_x, lid_y, lid_w, lid_h), 2, border_radius=3)
    pygame.draw.arc(surf, WOOD_L,
                    (lid_x + 3, lid_y + 3, lid_w - 6, lid_h * 2 // 3 - 4), 0, math.pi, 2)

    lock_w = max(10, w // 6); lock_h = max(10, w // 6)
    lock_x = cx - lock_w // 2; lock_y = body_y - lock_h // 2 + 2
    pygame.draw.rect(surf, GOLD,   (lock_x, lock_y + lock_h // 3, lock_w, lock_h * 2 // 3),
                     border_radius=2)
    pygame.draw.rect(surf, GOLD_L, (lock_x, lock_y + lock_h // 3, lock_w, lock_h * 2 // 3),
                     1, border_radius=2)
    shackle_rect = (lock_x + lock_w // 5, lock_y, lock_w * 3 // 5, lock_h * 3 // 4)
    pygame.draw.arc(surf, GOLD, shackle_rect, 0, math.pi, max(2, lock_w // 6))
    pygame.draw.circle(surf, DARK, (cx, lock_y + lock_h * 2 // 3), max(2, lock_w // 8))
    pygame.draw.rect(surf, DARK,
        (cx - max(1, lock_w // 14), lock_y + lock_h * 2 // 3,
         max(2, lock_w // 7), lock_h // 4))
    for bx in [body_x + int(body_w * 0.18), body_x + int(body_w * 0.82)]:
        pygame.draw.rect(surf, IRON,   (bx - 3, body_y - 3, 6, 6))
        pygame.draw.rect(surf, IRON_L, (bx - 3, body_y - 3, 6, 6), 1)
