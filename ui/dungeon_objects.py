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
    Stairs going UP — wall face texture for the back wall of a U-alcove.
    Wide at bottom (near party), narrow toward the top (far).
    Near-black rectangle at top — the opening ascending into darkness above.
    No door, no torch. Stairs + near-black void only.
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

    RECT_H = int(h * 0.20)        # near-black rectangle at top
    y_void = oy + RECT_H           # where stairs begin

    pygame.draw.rect(surf, DARK, (ox, oy, w, h))

    lit    = _lerp_col(mid, light, 0.55)
    shd    = _lerp_col(dark, mid,  0.28)
    seed_l = hash((theme, "ul")) & 0xFFFFFF
    seed_r = hash((theme, "ur")) & 0xFFFFFF
    bh = max(3, w // 15); bw = max(5, w // 9)

    _draw_masonry(surf, ox, oy, oy + h,
                  lambda y: ox, lwr, lit, mortar, bh, bw, seed_l)
    _draw_masonry(surf, ox, oy, oy + h,
                  rwl, lambda y: ox + w, shd, mortar, bh, bw, seed_r)

    # Steps: wide at bottom (near), narrow toward y_void
    STEPS = 7
    for i in range(STEPS):
        near_y = int(_lerp(oy + h, y_void, i / STEPS))
        far_y  = int(_lerp(oy + h, y_void, (i + 1) / STEPS))
        lnear = lwr(near_y); rnear = rwl(near_y)
        lfar  = lwr(far_y);  rfar  = rwl(far_y)

        brightness = _lerp(0.18, 0.52, i / (STEPS - 1))
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

    # Near-black rectangle — the opening above the stairs (darkness beyond)
    lx_top = lwr(y_void); rx_top = rwl(y_void)
    rect_w  = rx_top - lx_top
    if rect_w > 0:
        pygame.draw.rect(surf, (4, 3, 8), (lx_top, oy, rect_w, RECT_H))
    pygame.draw.line(surf, shadow, (lx_top, y_void), (rx_top, y_void), 2)


def draw_stairs_down(surf, r, theme=None):
    """
    Stairs going DOWN — floor-perspective view of a stairwell opening.

    Looking at a floor tile where the stairwell descends:
      • Black rectangle flush at top-centre (the void / stairwell mouth)
      • Amorphous stone floor shapes either side — large organic blobs near
        the party edge, shrinking to tiny flecks near the void
      • Gradient: full floor colour at bottom → near-black at the void rect
      • 6 step treads recede in perspective from near (bright) to far (dark)
      • Faint ember glow at the void edge (heat from below)
    """
    w, h = r.w, r.h
    ox, oy = r.x, r.y
    cx = ox + w // 2
    th = _THEMES.get(theme or _DEFAULT_THEME, _THEMES[_DEFAULT_THEME])
    light, dark, mid = th["light"], th["dark"], th["mid"]

    shadow  = _clamp(tuple(c - 22 for c in dark))
    floor_n = _clamp(_lerp_col(dark, mid,  0.60))   # floor colour, near party
    floor_f = _clamp(_lerp_col(DARK, dark, 0.14))   # near-black, far edge

    # ── 1. Gradient background: floor_n at bottom → near-black at top ────
    for y in range(h):
        t_c = ((1.0 - y / max(1, h - 1)) ** 2.0)
        row_col = _clamp(_lerp_col(DARK, floor_n, t_c))
        pygame.draw.line(surf, row_col, (ox, oy + y), (ox + w - 1, oy + y))

    # ── 2. Stairwell geometry ─────────────────────────────────────────────
    RECT_W   = int(w * 0.44)
    RECT_H   = int(h * 0.18)
    RECT_X   = cx - RECT_W // 2
    RECT_Y   = oy
    NEAR_HALF = int(w * 0.43)
    FAR_HALF  = RECT_W // 2
    STEP_TOP  = oy + RECT_H
    STEP_BOT  = oy + h - 2

    def slx(y):
        t = max(0.0, min(1.0, (y - oy - RECT_H) / max(1, h - RECT_H - 2)))
        return int(cx - (FAR_HALF + (NEAR_HALF - FAR_HALF) * t))

    def srx(y):
        t = max(0.0, min(1.0, (y - oy - RECT_H) / max(1, h - RECT_H - 2)))
        return int(cx + (FAR_HALF + (NEAR_HALF - FAR_HALF) * t))

    # ── 3. Amorphous stone shapes — large near party, tiny near void ──────
    import random as _random
    rng = _random.Random(hash((theme or _DEFAULT_THEME, "sd3")) & 0xFFFFFF)
    N_BANDS = 10
    for band in range(N_BANDS):
        band_t   = band / N_BANDS
        band_bot = oy + h - 1 - int(band_t * h)
        band_top = oy + h - 1 - int((band_t + 1.0 / N_BANDS) * h)
        band_top = max(band_top, oy)

        max_rx = max(2, int(w * (0.14 - 0.12 * band_t)))
        max_ry = max(1, int(h * (0.08 - 0.07 * band_t)))
        t_col  = (1.0 - band_t) ** 2.0
        base_c = _clamp(_lerp_col(DARK, floor_n, t_col))
        v_rng  = int(20 * (1.0 - band_t))
        n_blobs = max(3, int(18 * (1.0 - band_t * 0.7)))

        for _ in range(n_blobs):
            bx = ox + rng.randint(0, w - 1)
            by = rng.randint(band_top, max(band_top, band_bot))
            lx_h = slx(by) if by >= STEP_TOP else cx - FAR_HALF
            rx_h = srx(by) if by >= STEP_TOP else cx + FAR_HALF
            if lx_h <= bx <= rx_h:
                continue    # skip blobs inside stairwell opening
            rx_b = rng.randint(max(1, max_rx // 2), max(2, max_rx))
            ry_b = max(1, rng.randint(max(1, max_ry // 2), max(1, max_ry)) * 6 // 10)
            v    = rng.randint(-v_rng, v_rng)
            col  = _clamp(tuple(c + v for c in base_c))
            if rx_b >= 3 and ry_b >= 2:
                pygame.draw.ellipse(surf, col, (bx - rx_b, by - ry_b, rx_b*2, ry_b*2))
                hi = _clamp(tuple(min(255, c + max(1, v_rng // 2)) for c in col))
                pygame.draw.ellipse(surf, hi, (bx - rx_b, by - ry_b, rx_b*2, ry_b*2), 1)
            elif rx_b >= 2:
                pygame.draw.circle(surf, col, (bx, by), rx_b)
            else:
                if 0 <= bx - ox < w and 0 <= by - oy < h:
                    surf.set_at((bx, by), col)

    # ── 4. Step treads ────────────────────────────────────────────────────
    STEPS = 6
    out_line = _clamp(tuple(max(0, c - 18) for c in dark))
    for i in range(STEPS):
        y_far  = int(STEP_TOP + (STEP_BOT - STEP_TOP) * i       / STEPS)
        y_near = int(STEP_TOP + (STEP_BOT - STEP_TOP) * (i + 1) / STEPS)
        lx_f = slx(y_far);  rx_f = srx(y_far)
        lx_n = slx(y_near); rx_n = srx(y_near)
        if rx_n <= lx_n or y_near <= y_far:
            continue
        brightness = _lerp(0.08, 0.78, i / max(1, STEPS - 1))
        sv  = _seeded(hash((theme or _DEFAULT_THEME, "st3", i)), 0, 0, -6, 6)
        sc  = _clamp(tuple(c + sv for c in _lerp_col(DARK, light, brightness)))
        rc  = _clamp(_lerp_col(DARK, shadow, brightness * 0.38))
        ehi = _clamp(tuple(min(255, c + 32) for c in sc))
        pygame.draw.polygon(surf, sc,
            [(lx_f,y_far),(rx_f,y_far),(rx_n,y_near),(lx_n,y_near)])
        pygame.draw.line(surf, ehi, (lx_n+1,y_near), (rx_n-1,y_near), 2)
        pygame.draw.polygon(surf, out_line,
            [(lx_f,y_far),(rx_f,y_far),(rx_n,y_near),(lx_n,y_near)], 1)
        riser_h = max(2, (y_near - y_far) // 3)
        bot_r   = min(oy + h - 1, y_near + riser_h)
        if rx_n > lx_n:
            pygame.draw.polygon(surf, rc,
                [(lx_n,y_near),(rx_n,y_near),(rx_n,bot_r),(lx_n,bot_r)])

    # ── 5. Black void rectangle flush at top ─────────────────────────────
    pygame.draw.rect(surf, (2, 1, 4), (RECT_X, RECT_Y, RECT_W, RECT_H))
    # Stone lip around void rect
    lip = _clamp(_lerp_col(DARK, mid, 0.30))
    pygame.draw.rect(surf, lip, (RECT_X, RECT_Y, RECT_W, RECT_H), 1)
    void_bot = RECT_Y + RECT_H
    pygame.draw.line(surf, _clamp(_lerp_col(DARK, dark, 0.28)),
                     (RECT_X, void_bot), (RECT_X + RECT_W, void_bot), 2)

    # ── 6. Faint ember glow at void base ─────────────────────────────────
    for gi in range(5):
        gy = void_bot + gi + 1
        gw = max(2, RECT_W - gi * 4)
        glow = (max(0, 40 - gi*8), max(0, 14 - gi*3), 1)
        pygame.draw.line(surf, _clamp(glow), (cx - gw//2, gy), (cx + gw//2, gy))


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


# ══════════════════════════════════════════════════════════════════════════════
#  DUNGEON EXIT  — grand stone archway with surface daylight beyond
# ══════════════════════════════════════════════════════════════════════════════

def draw_entrance(surf, r, theme=None):
    """
    Dungeon entrance/exit archway — seen from INSIDE the dungeon.

    The party looks at a grand stone arch through which warm surface
    daylight floods.  Voussoir keystones, iron sconce torches at the
    jamb shoulders, a stone threshold slab, and warm-amber floor glow
    spilling toward the party.
    """
    w, h = r.w, r.h
    ox, oy = r.x, r.y
    cx = ox + w // 2
    th = _THEMES.get(theme or _DEFAULT_THEME, _THEMES[_DEFAULT_THEME])
    light, dark, mid = th["light"], th["dark"], th["mid"]

    shadow  = _clamp(tuple(c - 22 for c in dark))
    mortar  = _clamp(tuple(c - 26 for c in dark))
    stone_l = _clamp(_lerp_col(dark, light, 0.55))
    stone_d = _clamp(_lerp_col(DARK, dark, 0.65))

    import random as _random, math as _math
    rng = _random.Random(hash((theme or _DEFAULT_THEME, "exit")) & 0xFFFFFF)

    # ── 1. Stone wall fill ────────────────────────────────────────────────
    surf.fill(mortar, (ox, oy, w, h))
    BH = max(4, h // 9); BW = max(5, w // 6)
    for row in range(h // BH + 2):
        ry = oy + row * BH
        off = (BW // 2) if row % 2 else 0
        for col2 in range(-1, w // BW + 2):
            bx2 = ox + col2 * BW + off
            bx_c = max(ox, bx2 + 1); by_c = max(oy, ry + 1)
            bw_c = min(BW - 2, ox + w - bx_c); bh_c = min(BH - 2, oy + h - by_c)
            if bw_c > 0 and bh_c > 0:
                tone = 0.82 + rng.random() * 0.28
                c_b  = _clamp(tuple(int(v * tone) for v in stone_l))
                pygame.draw.rect(surf, c_b, (bx_c, by_c, bw_c, bh_c))

    # ── 2. Archway geometry ───────────────────────────────────────────────
    jamb_w   = max(5, w // 7)
    door_l   = ox + jamb_w
    door_r   = ox + w - jamb_w
    door_w   = door_r - door_l
    arch_bot = oy + int(h * 0.88)
    rect_top = oy + int(h * 0.52)
    arch_cy  = rect_top
    arch_rx  = door_w // 2
    arch_ry  = int(h * 0.26)

    # ── 3. Outside light — warm surface daylight through the opening ──────
    for y in range(oy, oy + h):
        xl = door_l; xr = door_r
        in_rect = (rect_top <= y <= arch_bot)
        in_arch = False
        if oy <= y < rect_top:
            dy_a = y - arch_cy
            if arch_rx > 0 and arch_ry > 0:
                inside = 1.0 - (dy_a / arch_ry) ** 2
                if inside >= 0:
                    half = _math.sqrt(inside) * arch_rx
                    xl = int(cx - half); xr = int(cx + half)
                    in_arch = (xl < xr)
        if in_rect or in_arch:
            t_y = 1.0 - max(0.0, min(1.0, (y - oy) / max(1, arch_bot - oy)))
            sky_top = (200, 195, 175)
            sky_bot = (160, 115,  55)
            sky_col = _clamp(_lerp_col(sky_bot, sky_top, t_y ** 0.7))
            pygame.draw.line(surf, sky_col, (xl, y), (xr - 1, y))

    # ── 4. Silhouetted jambs ──────────────────────────────────────────────
    for y in range(rect_top, arch_bot + 2):
        pygame.draw.line(surf, stone_d, (ox, y), (door_l - 1, y))
        pygame.draw.line(surf, shadow,  (door_r, y), (ox + w - 1, y))

    # ── 5. Voussoir arch ring ─────────────────────────────────────────────
    n_stones = max(7, min(13, w // 11))
    if n_stones % 2 == 0: n_stones += 1
    thick_x = max(4, w // 9); thick_y = max(3, h // 11)
    outer_rx = arch_rx + thick_x; outer_ry = arch_ry + thick_y
    inner_rx = arch_rx;           inner_ry = arch_ry

    for i in range(n_stones):
        a0 = _math.pi * (1.0 - i / n_stones)
        a1 = _math.pi * (1.0 - (i + 1) / n_stones)
        is_ks = (i == n_stones // 2)
        tone  = 1.20 if is_ks else 0.78 + rng.random() * 0.32
        c_s   = _clamp(tuple(int(v * tone) for v in stone_l))
        steps = max(4, int(abs(a1 - a0) * outer_rx * 1.5))
        opts  = [(cx + outer_rx * _math.cos(a0 + t/steps*(a1-a0)),
                  arch_cy + outer_ry * _math.sin(a0 + t/steps*(a1-a0)))
                 for t in range(steps + 1)]
        ipts  = [(cx + inner_rx * _math.cos(a0 + t/steps*(a1-a0)),
                  arch_cy + inner_ry * _math.sin(a0 + t/steps*(a1-a0)))
                 for t in range(steps + 1)]
        pts   = [(int(x), int(y)) for x, y in opts + list(reversed(ipts))]
        if len(pts) >= 3:
            pygame.draw.polygon(surf, c_s, pts)
            pygame.draw.polygon(surf, mortar, pts, 1)
        # Highlight & joint
        hx = int(cx + outer_rx * _math.cos((a0+a1)/2))
        hy = int(arch_cy + outer_ry * _math.sin((a0+a1)/2))
        if 0 <= hx < surf.get_width() and 0 <= hy < surf.get_height():
            hi = _clamp(tuple(min(255, c + 25) for c in c_s))
            pygame.draw.circle(surf, hi, (hx, hy), max(1, w // 55))
        for edge_a in (a0, a1):
            ix = int(cx + inner_rx * _math.cos(edge_a))
            iy = int(arch_cy + inner_ry * _math.sin(edge_a))
            ex2 = int(cx + outer_rx * _math.cos(edge_a))
            ey2 = int(arch_cy + outer_ry * _math.sin(edge_a))
            pygame.draw.line(surf, mortar, (ix, iy), (ex2, ey2), 1)

    # ── 6. Keystone rune medallion ────────────────────────────────────────
    ks_y = int(arch_cy - outer_ry) - 1
    if ks_y > oy + 1:
        ks_r = max(3, w // 16)
        pygame.draw.circle(surf, mortar,  (cx, ks_y), ks_r + 2)
        pygame.draw.circle(surf, stone_l, (cx, ks_y), ks_r)
        pygame.draw.circle(surf, mortar,  (cx, ks_y), ks_r, 1)
        lw = max(1, w // 55)
        for ang in range(0, 360, 45):
            ex2 = cx + int((ks_r - 1) * _math.cos(_math.radians(ang)))
            ey2 = ks_y + int((ks_r - 1) * _math.sin(_math.radians(ang)))
            pygame.draw.line(surf, mortar, (cx, ks_y), (ex2, ey2), lw)

    # ── 7. Torches ────────────────────────────────────────────────────────
    torch_y = arch_cy + int(arch_ry * 0.25)
    _draw_torch(surf, ox + 1,                        torch_y, w)
    _draw_torch(surf, ox + w - max(12, w // 14) - 1, torch_y, w)

    # ── 8. Threshold slab ────────────────────────────────────────────────
    slab_y = arch_bot
    slab_h = max(3, h // 12)
    pygame.draw.rect(surf, stone_d,
                     (door_l - 2, slab_y, door_w + 4, slab_h), border_radius=2)
    pygame.draw.rect(surf, stone_l,
                     (door_l - 2, slab_y, door_w + 4, slab_h), 1, border_radius=2)
    pygame.draw.line(surf, _clamp(tuple(min(255, c + 20) for c in stone_l)),
                     (door_l - 1, slab_y + 1), (door_r + 1, slab_y + 1), 1)

    # ── 9. Warm floor glow spilling toward party ──────────────────────────
    for gi in range(6):
        gy = slab_y + slab_h + gi
        if gy >= oy + h: break
        gw   = max(2, door_w - gi * 6)
        glow = _clamp((max(0, 65 - gi*10), max(0, 40 - gi*7), max(0, 15 - gi*3)))
        pygame.draw.line(surf, glow, (cx - gw//2, gy), (cx + gw//2 - 1, gy))
