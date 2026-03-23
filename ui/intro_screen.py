"""
Realm of Shadows — Intro / Splash sequence

Phase 0 (SPLASH):  Bad Bat Enterprises logo fades in as a retro pixel-art
                   version, holds, "PRESENTS" appears beneath, then fades out.
Phase 1 (TITLE):   Game title screen — retro dungeon-crawl art, animated
                   starfield, game title text, tagline, title music.
Phase 2 (MENU):    "New Game" and "Continue" click-buttons appear.
                   Mouse-click only — no keypress navigation.

Public API:
    intro = IntroScreen()
    intro.update(dt_ms)          # call each frame
    intro.draw(surf, mx, my)     # call each frame
    result = intro.handle_click(mx, my)   # returns 'new_game' / 'continue' / None
    intro.done   -> bool
    intro.action -> 'new_game' | 'continue' | None
"""

import pygame
import math
import random
import os
import numpy as np

try:
    from ui.renderer import SCREEN_W, SCREEN_H, draw_text, BG_COLOR
except ImportError:
    SCREEN_W, SCREEN_H, BG_COLOR = 1440, 900, (12, 10, 24)
    def draw_text(surf, text, x, y, color, size, bold=False):
        f = pygame.font.SysFont("monospace", size, bold=bold)
        surf.blit(f.render(text, True, color), (x, y))

BLACK   = (0,   0,   0)
NEON_G  = (0,   255, 0)
DIM_G   = (0,   160, 0)

# ── Logo path ─────────────────────────────────────────────────────────────────
_LOGO_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "assets", "bad_bat_logo.jpg"
)

# ── Timing (ms) ───────────────────────────────────────────────────────────────
SPLASH_FADE_IN   = 1400
SPLASH_HOLD      = 1800
PRESENTS_FADE    =  600
PRESENTS_HOLD    = 1000
SPLASH_FADE_OUT  =  900
TITLE_HOLD_MIN   = 2000   # min ms on title before menu fades in
MENU_APPEAR_DUR  =  700

PIXEL_BLOCK = 6   # retro pixel size


# ═══════════════════════════════════════════════════════════════════════════════
#  RETRO LOGO BUILDER
# ═══════════════════════════════════════════════════════════════════════════════

def _make_retro_logo(surf):
    """
    Convert logo to chunky retro pixels (SRCALPHA, black→transparent).
    Uses max-pooling per block so thin strokes are preserved.
    Green channel is boosted to neon.
    """
    w, h = surf.get_size()
    arr = pygame.surfarray.array3d(surf).astype(np.float32)  # (w, h, 3)
    G = arr[:,:,1]; R = arr[:,:,0]; B = arr[:,:,2]

    tw = w // PIXEL_BLOCK
    th = h // PIXEL_BLOCK

    # Max-pool: for each block keep the maximum green value
    Gp = G[:tw*PIXEL_BLOCK, :th*PIXEL_BLOCK].reshape(tw, PIXEL_BLOCK, th, PIXEL_BLOCK).max(axis=(1,3))
    Rp = R[:tw*PIXEL_BLOCK, :th*PIXEL_BLOCK].reshape(tw, PIXEL_BLOCK, th, PIXEL_BLOCK).max(axis=(1,3))
    Bp = B[:tw*PIXEL_BLOCK, :th*PIXEL_BLOCK].reshape(tw, PIXEL_BLOCK, th, PIXEL_BLOCK).max(axis=(1,3))

    # Logo pixel = green dominant and bright enough
    logo = (Gp > 60) & (Gp > Rp * 1.5) & (Gp > Bp * 1.5)
    neon = np.clip(Gp * 1.05, 120, 255).astype(np.uint8)

    # Build transparent SRCALPHA surface (pygame coord: w×h)
    result = pygame.Surface((tw, th), pygame.SRCALPHA)
    result.fill((0, 0, 0, 0))
    rgb_v   = pygame.surfarray.pixels3d(result)
    alph_v  = pygame.surfarray.pixels_alpha(result)
    rgb_v[:,:,0] = 0
    rgb_v[:,:,1] = np.where(logo, neon, 0)
    rgb_v[:,:,2] = 0
    alph_v[:,:] = np.where(logo, 255, 0).astype(np.uint8)
    del rgb_v, alph_v

    retro = pygame.transform.scale(result, (tw * PIXEL_BLOCK, th * PIXEL_BLOCK))
    return retro


def _load_logo():
    """Load the logo and return (original, retro). Returns (None, None) on failure."""
    try:
        orig  = pygame.image.load(_LOGO_PATH).convert()
        retro = _make_retro_logo(orig)
        return orig, retro
    except Exception:
        return None, None


# ═══════════════════════════════════════════════════════════════════════════════
#  CRT OVERLAY
# ═══════════════════════════════════════════════════════════════════════════════

def _scanlines(surf, alpha=28):
    sl = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    for y in range(0, SCREEN_H, 2):
        pygame.draw.line(sl, (0, 0, 0, alpha), (0, y), (SCREEN_W, y))
    surf.blit(sl, (0, 0))


# ═══════════════════════════════════════════════════════════════════════════════
#  RETRO DUNGEON ART
# ═══════════════════════════════════════════════════════════════════════════════

def _draw_dungeon_art(surf, t):
    """Wizardry/Ultima-style first-person corridor — pure geometry."""
    cx   = SCREEN_W // 2
    AY   = 118          # top of art panel
    AH   = 430
    AW   = 660
    art  = pygame.Rect(cx - AW//2, AY, AW, AH)
    pygame.draw.rect(surf, (3, 2, 7), art)

    for depth in [6, 5, 4, 3, 2, 1]:
        s = 1.0 / (depth + 1)
        rw = int(AW * s * 0.92); rh = int(AH * s * 0.88)
        rx = cx - rw//2;         ry = AY + (AH - rh)//2
        sh = int(22 + depth * 17)
        wc = (sh, sh//2, sh//3)
        pygame.draw.rect(surf, wc, (rx, ry, rw, rh))
        fc = (sh+10, sh//3, sh//5)
        fh = rh//3
        pygame.draw.rect(surf, fc,     (rx, ry+rh-fh, rw, fh))
        pygame.draw.rect(surf, (sh//2, sh//4, sh//6), (rx, ry, rw, fh))
        pygame.draw.rect(surf, (sh+18, sh//2+8, sh//3+6), (rx, ry, rw, rh), 1)

    # Glowing doorway
    dw, dh = 52, 78
    dx = cx - dw//2;  dy = AY + AH//2 - dh//2
    ga = int(70 + 35*math.sin(t*1.3))
    g = pygame.Surface((dw+24, dh+24), pygame.SRCALPHA)
    g.fill((35, 0, 70, ga))
    surf.blit(g, (dx-12, dy-12))
    pygame.draw.rect(surf, (6, 0, 18), (dx, dy, dw, dh))
    pygame.draw.rect(surf, (110, 55, 175), (dx, dy, dw, dh), 2)

    # Torches
    tf = 0.65 + 0.35*math.sin(t*7.8)
    for tx, ty in [(cx-185, AY+AH//2-22), (cx+145, AY+AH//2-22)]:
        pygame.draw.rect(surf, (90, 55, 25), (tx-3, ty, 6, 22))
        fh2 = int(20*tf)
        fc2 = (int(255*tf), int(130*tf), 18)
        pygame.draw.ellipse(surf, fc2, (tx-5, ty-fh2, 10, fh2+4))
        halo = pygame.Surface((64, 64), pygame.SRCALPHA)
        pygame.draw.circle(halo, (190, 90, 18, int(32*tf)), (32, 32), 30)
        surf.blit(halo, (tx-32, ty-32))

    # Shadow figure
    fa = int(50 + 25*math.sin(t*0.55))
    fig = pygame.Surface((18, 38), pygame.SRCALPHA)
    fig.fill((25, 0, 45, fa))
    surf.blit(fig, (cx-9, dy+16))

    # Art border
    pygame.draw.rect(surf, (55, 28, 95), art, 3)
    pygame.draw.rect(surf, (28, 14, 48), art.inflate(8, 8), 2)


# ═══════════════════════════════════════════════════════════════════════════════
#  INTRO SCREEN CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class IntroScreen:

    def __init__(self):
        self.t      = 0        # ms in current phase
        self.phase  = 'splash'
        self.done   = False
        self.action = None

        # Splash timing thresholds
        self._t_presents = SPLASH_FADE_IN + SPLASH_HOLD
        self._t_out      = self._t_presents + PRESENTS_FADE + PRESENTS_HOLD
        self._t_end      = self._t_out + SPLASH_FADE_OUT

        # Logo
        self._orig, self._retro = _load_logo()

        # Title screen
        self._title_t  = 0.0
        self._menu_a   = 0

        # Button rects
        self._new_r  = None
        self._cont_r = None

        # Starfield
        rng = random.Random(77)
        self._stars = [(rng.randint(0,SCREEN_W), rng.randint(0,SCREEN_H),
                        rng.randint(1,2), rng.uniform(.3,1.2), rng.random()*6.28)
                       for _ in range(120)]

        self._music_started = False

    # ── public ────────────────────────────────────────────────────────────────

    def update(self, dt):
        self.t += dt
        if self.phase == 'splash' and self.t >= self._t_end:
            self._go_title()
        elif self.phase in ('title', 'menu'):
            self._title_t += dt / 1000.0
            if self._title_t * 1000 > TITLE_HOLD_MIN:
                self._menu_a = min(255, self._menu_a + int(dt * 255 / MENU_APPEAR_DUR))

    def handle_click(self, mx, my):
        if self.phase != 'menu':
            return None
        if self._new_r and self._new_r.collidepoint(mx, my):
            self.done = True; self.action = 'new_game'; return 'new_game'
        if self._cont_r and self._cont_r.collidepoint(mx, my):
            self.done = True; self.action = 'continue'; return 'continue'
        return None

    def draw(self, surf, mx, my):
        surf.fill(BLACK)
        if self.phase == 'splash':
            self._draw_splash(surf)
        else:
            self._draw_title(surf, mx, my)
        _scanlines(surf)

    # ── internal ──────────────────────────────────────────────────────────────

    def _go_title(self):
        self.phase = 'title'; self.t = 0; self._title_t = 0.0
        if not self._music_started:
            self._music_started = True
            try:
                from core import sound as sfx
                sfx.stop_music(); sfx.stop_ambient()
                sfx.play_music("town_briarhollow")
            except Exception:
                pass

    def _logo_a(self):
        t = self.t
        if t < SPLASH_FADE_IN:
            return int(255 * t / SPLASH_FADE_IN)
        if t < self._t_presents:
            return 255
        if t < self._t_out:
            return 255
        return max(0, int(255 * (1 - (t - self._t_out) / SPLASH_FADE_OUT)))

    def _pres_a(self):
        t = self.t
        if t < self._t_presents:
            return 0
        if t < self._t_presents + PRESENTS_FADE:
            return int(255 * (t - self._t_presents) / PRESENTS_FADE)
        if t < self._t_out:
            return 255
        return max(0, int(255 * (1 - (t - self._t_out) / SPLASH_FADE_OUT)))

    # ── splash ────────────────────────────────────────────────────────────────

    def _draw_splash(self, surf):
        la = self._logo_a()
        pa = self._pres_a()

        if self._retro and la > 0:
            # Scale retro logo to fit — square source, limit to 680px wide or 70% screen height
            lw, lh = self._retro.get_size()
            scale  = min(680 / lw, SCREEN_H * 0.70 / lh)
            nw     = int(lw * scale)
            nh     = int(lh * scale)
            lx     = SCREEN_W // 2 - nw // 2
            ly     = SCREEN_H // 2 - nh // 2 - 50

            scaled = pygame.transform.scale(self._retro, (nw, nh))

            # Apply fade by multiplying per-pixel alpha
            faded      = scaled.copy()
            alpha_view = pygame.surfarray.pixels_alpha(faded)
            alpha_view[:] = (alpha_view.astype(np.float32) * la / 255).astype(np.uint8)
            del alpha_view

            surf.blit(faded, (lx, ly))

        else:
            # Fallback text logo
            if la > 0:
                f1 = pygame.font.SysFont("monospace", 56, bold=True)
                f2 = pygame.font.SysFont("monospace", 30, bold=True)
                t1 = f1.render("BAD BAT", True, NEON_G)
                t2 = f2.render("ENTERPRISES", True, DIM_G)
                for txt, y in [(t1, SCREEN_H//2 - 60), (t2, SCREEN_H//2 + 10)]:
                    s = pygame.Surface(txt.get_size(), pygame.SRCALPHA)
                    s.blit(txt, (0,0)); s.set_alpha(la)
                    surf.blit(s, (SCREEN_W//2 - txt.get_width()//2, y))

        if pa > 0:
            fp  = pygame.font.SysFont("monospace", 22)
            txt = fp.render("P R E S E N T S", True, NEON_G)
            ts  = pygame.Surface(txt.get_size(), pygame.SRCALPHA)
            ts.blit(txt, (0,0)); ts.set_alpha(pa)
            # Position below the logo
            if self._retro and la > 0:
                lw2, lh2 = self._retro.get_size()
                sc2      = min(680/lw2, SCREEN_H*0.70/lh2)
                nh2      = int(lh2 * sc2)
                py       = SCREEN_H//2 - nh2//2 - 50 + nh2 + 18
            else:
                py = SCREEN_H // 2 + 70
            surf.blit(ts, (SCREEN_W//2 - txt.get_width()//2, py))

    # ── title ─────────────────────────────────────────────────────────────────

    def _draw_title(self, surf, mx, my):
        t = self._title_t

        # Starfield
        for sx, sy, sr, sp, ph in self._stars:
            a = int(55 + 45*math.sin(t*sp+ph))
            s = pygame.Surface((sr*2, sr*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (200,180,255,a), (sr,sr), sr)
            surf.blit(s, (sx-sr, sy-sr))

        # Tendrils
        rng2 = random.Random(int(t*1.5))
        td = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        for _ in range(10):
            ox = rng2.randint(0, SCREEN_W); ln = rng2.randint(80, 180)
            px, py2 = float(ox), 0.0
            for step in range(ln):
                nx = px + rng2.uniform(-5,5); ny = py2+1
                a  = max(0, int(70*(1-step/ln)))
                pygame.draw.line(td,(60,0,100,a),(int(px),int(py2)),(int(nx),int(ny)),2)
                px, py2 = nx, ny
        surf.blit(td, (0,0))

        # Dungeon art
        _draw_dungeon_art(surf, t)

        # Title text
        pulse = abs(math.sin(t*1.05))
        rc = (int(210+45*pulse), int(180+30*pulse), int(20*pulse))
        sc = (int(140+60*pulse), int(110+50*pulse), int(180+40*pulse))
        gw = pygame.Surface((390,82), pygame.SRCALPHA)
        gw.fill((80,20,140, int(40+30*pulse)))
        surf.blit(gw, (SCREEN_W//2-195, 28))
        draw_text(surf, "REALM",   SCREEN_W//2-128, 34,  rc, 52, bold=True)
        draw_text(surf, "of",      SCREEN_W//2-22,  93,  (180,160,220), 22)
        draw_text(surf, "SHADOWS", SCREEN_W//2-168, 116, sc, 52, bold=True)
        draw_text(surf, "The Fading comes for all things.",
                  SCREEN_W//2-180, 178, (140,110,180), 15)

        # Company credit
        draw_text(surf, "A Bad Bat Enterprises Game",
                  SCREEN_W//2-150, SCREEN_H-38, DIM_G, 14)

        # Menu
        if self._menu_a > 10:
            self._draw_menu(surf, mx, my, self._menu_a)
            if self._menu_a >= 255:
                self.phase = 'menu'

    # ── menu ──────────────────────────────────────────────────────────────────

    def _draw_menu(self, surf, mx, my, alpha):
        from core.save_load import list_saves
        has_saves = bool(list_saves())

        btn_y  = SCREEN_H // 2 + 238
        new_r  = pygame.Rect(SCREEN_W//2 - 225, btn_y, 205, 54)
        cont_r = pygame.Rect(SCREEN_W//2 + 20,  btn_y, 205, 54)
        self._new_r  = new_r
        self._cont_r = cont_r if has_saves else None

        def btn(rect, label, enabled, hovered):
            bs = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            if enabled and hovered:
                bg = (60, 110, 200, int(alpha * .92))
            elif enabled:
                bg = (38, 78, 140, int(alpha * .85))
            else:
                bg = (36, 36, 56, int(alpha * .50))
            pygame.draw.rect(bs, bg, (0,0,rect.width,rect.height), border_radius=6)
            bc = (100,160,255,alpha) if (enabled and hovered) else (68,98,178,alpha)
            pygame.draw.rect(bs, bc, (0,0,rect.width,rect.height), 2, border_radius=6)
            surf.blit(bs, rect.topleft)
            tc = (255,255,255) if (enabled and hovered) else ((215,215,250) if enabled else (75,75,95))
            f  = pygame.font.SysFont("monospace", 18, bold=True)
            txt = f.render(label, True, tc)
            ts = pygame.Surface(txt.get_size(), pygame.SRCALPHA)
            ts.blit(txt, (0,0)); ts.set_alpha(alpha)
            surf.blit(ts, (rect.x + rect.width//2 - txt.get_width()//2,
                           rect.y + rect.height//2 - txt.get_height()//2))

        btn(new_r,  "New Game", True,
            new_r.collidepoint(mx, my) if alpha >= 200 else False)
        btn(cont_r, "Continue", has_saves,
            cont_r.collidepoint(mx, my) if (has_saves and alpha >= 200) else False)

        if not has_saves:
            fh = pygame.font.SysFont("monospace", 11)
            hint = fh.render("(no saves found)", True, (75,75,90))
            hs = pygame.Surface(hint.get_size(), pygame.SRCALPHA)
            hs.blit(hint, (0,0)); hs.set_alpha(alpha)
            surf.blit(hs, (cont_r.x + cont_r.width//2 - hint.get_width()//2,
                           cont_r.bottom + 5))
