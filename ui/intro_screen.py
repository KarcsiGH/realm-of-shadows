"""
Realm of Shadows — Intro / Splash sequence
Three phases, each doubling as a loading screen:

  Phase SPLASH1  Bad Bat Enterprises retro logo.
                 While displayed: batch1 SFX generated (fast, ~1s).
  Phase SPLASH2  Realm of Shadows teaser card with lore quote.
                 While displayed: batch2 music generated (~20s on Mac).
                 Progress bar at bottom.
  Phase TITLE    Game title screen with retro dungeon art + title music.
  Phase MENU     New Game / Continue click buttons.

Caller checks .done (bool) and .action ('new_game' | 'continue' | None).
"""

import pygame
import math
import random
import os
import numpy as np

# ── renderer constants ────────────────────────────────────────────────────────
try:
    from ui.renderer import SCREEN_W, SCREEN_H, draw_text, BG_COLOR
except ImportError:
    SCREEN_W, SCREEN_H, BG_COLOR = 1440, 900, (12, 10, 24)
    def draw_text(surf, text, x, y, color, size, bold=False):
        f = pygame.font.SysFont("monospace", size, bold=bold)
        surf.blit(f.render(text, True, color), (x, y))

BLACK   = (0,   0,   0)
GREEN   = (0,   255, 0)
DKGREEN = (0,   140, 0)
GOLD    = (220, 180, 40)
GREY    = (120, 110, 130)
CREAM   = (220, 210, 190)
PURPLE  = (80,  20,  140)

_LOGO_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "assets", "bad_bat_logo.png"
)

# ── timing (ms) ───────────────────────────────────────────────────────────────
S1_FADE_IN      = 1200   # logo fades in
S1_HOLD         = 1400   # logo holds
S1_PRESENTS_IN  =  600   # "PRESENTS" fades in
S1_PRESENTS_HOLD=  900   # "PRESENTS" holds
S1_FADE_OUT     =  800   # everything fades out
S1_MIN_TOTAL    = S1_FADE_IN + S1_HOLD + S1_PRESENTS_IN + S1_PRESENTS_HOLD + S1_FADE_OUT  # ~4.9s

S2_FADE_IN      =  600   # teaser card fades in
S2_MIN_HOLD     = 3000   # minimum visible time (waits for batch2 after this)
S2_FADE_OUT     =  800

TITLE_FADE_IN   =  700
TITLE_MIN_HOLD  = 2500
MENU_APPEAR     =  600

PIXEL_BLOCK = 5


# ── logo helpers ──────────────────────────────────────────────────────────────

def _make_retro_logo(original_surf, block=PIXEL_BLOCK):
    """Max-pool downscale → neon green transparent surface."""
    w, h = original_surf.get_size()
    tiny_w = w // block
    tiny_h = h // block

    raw  = pygame.surfarray.array3d(original_surf)   # (w, h, 3)
    arr  = raw.transpose(1, 0, 2).astype(np.float32) # (h, w, 3)

    G = arr[:, :, 1]; R = arr[:, :, 0]; B = arr[:, :, 2]

    G_pool = G[:tiny_h*block, :tiny_w*block].reshape(
        tiny_h, block, tiny_w, block).max(axis=(1, 3))
    R_pool = R[:tiny_h*block, :tiny_w*block].reshape(
        tiny_h, block, tiny_w, block).max(axis=(1, 3))
    B_pool = B[:tiny_h*block, :tiny_w*block].reshape(
        tiny_h, block, tiny_w, block).max(axis=(1, 3))

    is_logo = (G_pool > 5) & (G_pool >= R_pool) & (G_pool >= B_pool)
    neon    = np.clip(G_pool * 4.0, 60, 255).astype(np.uint8)

    result = pygame.Surface((tiny_w, tiny_h), pygame.SRCALPHA)
    result.fill((0, 0, 0, 0))

    rgb_v   = pygame.surfarray.pixels3d(result)
    alpha_v = pygame.surfarray.pixels_alpha(result)
    is_T = is_logo.T;  n_T = neon.T
    rgb_v[:, :, 0] = 0
    rgb_v[:, :, 1] = np.where(is_T, n_T, 0)
    rgb_v[:, :, 2] = 0
    alpha_v[:, :]  = np.where(is_T, 255, 0).astype(np.uint8)
    del rgb_v, alpha_v

    return pygame.transform.scale(result, (tiny_w * block, tiny_h * block))


def _build_logo():
    try:
        orig  = pygame.image.load(_LOGO_PATH).convert_alpha()
        retro = _make_retro_logo(orig)
        return orig, retro
    except Exception:
        return None, None


def _draw_retro_text(surf, text, x, y, size, block=PIXEL_BLOCK):
    try:
        font  = pygame.font.SysFont("monospace", size, bold=True)
        t_sf  = font.render(text, False, (0, 255, 0))
        tw, th = t_sf.get_size()
        tiny  = pygame.transform.scale(t_sf, (max(1, tw//block), max(1, th//block)))
        chunky = pygame.transform.scale(tiny, (tw, th))
        chunky.set_colorkey((0, 0, 0))
        surf.blit(chunky, (x, y))
    except Exception:
        pass


def _draw_scanlines(surf, alpha=28):
    sl = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    for y in range(0, SCREEN_H, 2):
        pygame.draw.line(sl, (0, 0, 0, alpha), (0, y), (SCREEN_W, y))
    surf.blit(sl, (0, 0))


# ── retro dungeon art (unchanged from before) ─────────────────────────────────

def _draw_retro_dungeon_art(surf, t):
    cx     = SCREEN_W // 2
    art_y  = 120
    art_h  = 420
    art_w  = 640
    art_rect = pygame.Rect(cx - art_w//2, art_y, art_w, art_h)
    pygame.draw.rect(surf, (4, 3, 8), art_rect)

    for depth in [5, 4, 3, 2, 1]:
        shrink = 1.0 / (depth + 1)
        w2  = int(art_w * shrink * 0.9)
        h2  = int(art_h * shrink * 0.85)
        x2  = cx - w2 // 2
        y2  = art_y + (art_h - h2) // 2
        r   = pygame.Rect(x2, y2, w2, h2)
        sh  = int(30 + depth * 18)
        wc  = (sh, sh//2, sh//3)
        pygame.draw.rect(surf, wc, r)
        fh  = r.height // 3
        pygame.draw.rect(surf, (sh+10, sh//3, sh//4), pygame.Rect(r.x, r.bottom-fh, r.width, fh))
        pygame.draw.rect(surf, (sh//2, sh//4, sh//5), pygame.Rect(r.x, r.y, r.width, fh))
        pygame.draw.rect(surf, (sh+20, sh//2+10, sh//3+8), r, 1)

    ga = int(80 + 40 * math.sin(t * 1.2))
    dw, dh = 48, 72
    dx = cx - dw//2; dy = art_y + art_h//2 - dh//2
    glow = pygame.Surface((dw+20, dh+20), pygame.SRCALPHA)
    glow.fill((40, 0, 80, ga)); surf.blit(glow, (dx-10, dy-10))
    pygame.draw.rect(surf, (8, 0, 20), (dx, dy, dw, dh))
    pygame.draw.rect(surf, (120, 60, 180), (dx, dy, dw, dh), 2)

    tf = 0.7 + 0.3 * math.sin(t * 8.3)
    for tx, ty in [(cx-180, art_y+art_h//2-20), (cx+140, art_y+art_h//2-20)]:
        pygame.draw.rect(surf, (100,60,30), (tx-3,ty,6,20))
        fh2 = int(18*tf)
        pygame.draw.ellipse(surf, (int(255*tf),int(140*tf),20), (tx-5,ty-fh2,10,fh2+4))
        hl = pygame.Surface((60,60), pygame.SRCALPHA)
        pygame.draw.circle(hl, (200,100,20,int(35*tf)), (30,30), 28)
        surf.blit(hl, (tx-30, ty-30))

    fa = int(60+30*math.sin(t*.6))
    fs = pygame.Surface((20,40), pygame.SRCALPHA); fs.fill((30,0,50,fa))
    surf.blit(fs, (cx-10, dy+14))

    pygame.draw.rect(surf, (60,30,100), art_rect, 3)
    pygame.draw.rect(surf, (30,15,50), art_rect.inflate(6,6), 2)


# ═══════════════════════════════════════════════════════════════════════════
#  IntroScreen
# ═══════════════════════════════════════════════════════════════════════════

class IntroScreen:
    PHASES = ('splash1', 'splash2', 'title', 'menu')

    def __init__(self):
        self.phase       = 'splash1'
        self.t           = 0      # ms in current phase
        self.done        = False
        self.action      = None

        # Pre-compute splash1 thresholds
        self._s1_pres_start = S1_FADE_IN + S1_HOLD
        self._s1_out_start  = self._s1_pres_start + S1_PRESENTS_IN + S1_PRESENTS_HOLD
        self._s1_total      = self._s1_out_start + S1_FADE_OUT

        # Logo surfaces
        self._logo_orig, self._logo_retro = _build_logo()

        # Splash2 / title timing
        self._batch1_done  = False
        self._batch2_done  = False
        self._s2_t         = 0     # ms in splash2
        self._title_t      = 0.0   # seconds in title
        self._menu_alpha   = 0

        # Starfield
        rng = random.Random(77)
        self._stars = [(rng.randint(0,SCREEN_W), rng.randint(0,SCREEN_H),
                        rng.randint(1,2), rng.uniform(0.3,1.2), rng.random()*6.28)
                       for _ in range(120)]

        # Button rects
        self._new_rect  = None
        self._cont_rect = None
        self._title_music_started = False

        # Batch2 progress info
        self._b2_label = "Preparing…"
        self._b2_pct   = 0.0

    # ── public API ────────────────────────────────────────────────────────────

    def update(self, dt_ms):
        """Call once per frame. Drives generation and phase transitions."""
        self.t += dt_ms
        try:
            from core import sound as sfx
            if not self._batch1_done and sfx._enabled:
                sfx.step_batch1()
                self._batch1_done = True
        except Exception:
            self._batch1_done = True

        if self.phase == 'splash1':
            if self.t >= self._s1_total and self._batch1_done:
                self._enter_splash2()

        elif self.phase == 'splash2':
            self._s2_t += dt_ms
            self._do_batch2_step()
            # Advance when BOTH min hold AND batch2 done
            if self._s2_t >= S2_MIN_HOLD + S2_FADE_OUT and self._batch2_done:
                self._enter_title()

        elif self.phase == 'title':
            self._title_t += dt_ms / 1000.0
            if self._title_t * 1000 > TITLE_MIN_HOLD:
                self._menu_alpha = min(255,
                    self._menu_alpha + int(dt_ms * 255 / MENU_APPEAR))
                if self._menu_alpha >= 255:
                    self.phase = 'menu'

    def handle_click(self, mx, my):
        if self.phase not in ('title', 'menu'):
            return None
        if self._new_rect and self._new_rect.collidepoint(mx, my):
            self.done = True; self.action = 'new_game'; return 'new_game'
        if self._cont_rect and self._cont_rect.collidepoint(mx, my):
            self.done = True; self.action = 'continue'; return 'continue'
        return None

    def draw(self, surf, mx, my):
        surf.fill(BLACK)
        if self.phase == 'splash1':
            self._draw_splash1(surf)
        elif self.phase == 'splash2':
            self._draw_splash2(surf)
        elif self.phase in ('title', 'menu'):
            self._draw_title(surf, mx, my)
        _draw_scanlines(surf)

    # ── phase transitions ─────────────────────────────────────────────────────

    def _enter_splash2(self):
        self.phase = 'splash2'
        self.t = 0; self._s2_t = 0

    def _enter_title(self):
        self.phase = 'title'
        self.t = 0; self._title_t = 0.0
        if not self._title_music_started:
            self._title_music_started = True
            try:
                from core import sound as sfx
                sfx.stop_music(); sfx.stop_ambient()
                sfx.play_music("town_briarhollow")
            except Exception:
                pass

    # ── batch2 stepping ───────────────────────────────────────────────────────

    def _do_batch2_step(self):
        if self._batch2_done:
            return
        try:
            from core import sound as sfx
            if not sfx._enabled:
                self._batch2_done = True
                return
            done, idx, total, name = sfx.step_batch2()
            self._b2_label = name
            self._b2_pct   = idx / max(1, total)
            if done:
                self._batch2_done = True
                self._b2_pct = 1.0
                self._b2_label = "Ready"
        except Exception:
            self._batch2_done = True

    # ── SPLASH 1 — Bad Bat Enterprises ───────────────────────────────────────

    def _s1_logo_alpha(self):
        t = self.t
        if t < S1_FADE_IN:
            return int(255 * t / S1_FADE_IN)
        if t < self._s1_pres_start:
            return 255
        if t < self._s1_out_start:
            return 255
        return max(0, int(255 * (1 - (t - self._s1_out_start) / S1_FADE_OUT)))

    def _s1_pres_alpha(self):
        t = self.t
        ps = self._s1_pres_start
        if t < ps: return 0
        if t < ps + S1_PRESENTS_IN:
            return int(255 * (t - ps) / S1_PRESENTS_IN)
        if t < self._s1_out_start: return 255
        return max(0, int(255 * (1 - (t - self._s1_out_start) / S1_FADE_OUT)))

    def _draw_splash1(self, surf):
        la = self._s1_logo_alpha()
        pa = self._s1_pres_alpha()

        # Green phosphor glow behind logo
        if la > 0:
            gw, gh = 760, 260
            gx = SCREEN_W//2 - gw//2; gy = SCREEN_H//2 - gh//2 - 30
            gl = pygame.Surface((gw, gh), pygame.SRCALPHA)
            for r in range(0, min(gw,gh)//2, 4):
                frac = 1 - r/(min(gw,gh)//2)
                a = int(la * 0.18 * frac**2)
                pygame.draw.ellipse(gl, (0,40,0,a), (gw//2-r*2, gh//2-r, r*4, r*2))
            surf.blit(gl, (gx, gy))

        if self._logo_retro and la > 0:
            lw, lh = self._logo_retro.get_size()
            scale = min(0.85, 700/lw, (SCREEN_H*0.55)/lh)
            nw, nh = int(lw*scale), int(lh*scale)
            logo_s = pygame.transform.scale(self._logo_retro, (nw, nh))
            lx = SCREEN_W//2 - nw//2
            ly = SCREEN_H//2 - nh//2 - 30

            # Fade via per-pixel alpha multiply
            faded = pygame.Surface((nw, nh), pygame.SRCALPHA)
            faded.blit(logo_s, (0, 0))
            av = pygame.surfarray.pixels_alpha(faded)
            av[:] = (av.astype(np.float32) * la / 255).astype(np.uint8)
            del av
            surf.blit(faded, (lx, ly))

            # BAD / BAT text (pure black in source → draw in retro green)
            if la >= 40:
                ts = max(18, int(nh * 0.22))
                ty = ly + int(nh * 0.18)
                # BAD — left third of logo
                bad_surf = pygame.Surface((int(nw*0.34), ts+8), pygame.SRCALPHA)
                _draw_retro_text(bad_surf, "BAD", 0, 0, ts)
                bad_surf.set_alpha(la)
                surf.blit(bad_surf, (lx + int(nw*0.01), ty))
                # BAT — right third
                bat_surf = pygame.Surface((int(nw*0.34), ts+8), pygame.SRCALPHA)
                _draw_retro_text(bat_surf, "BAT", 0, 0, ts)
                bat_surf.set_alpha(la)
                surf.blit(bat_surf, (lx + int(nw*0.65), ty))

        # "PRESENTS"
        if pa > 0:
            fp = pygame.font.SysFont("monospace", 20)
            pt = fp.render("P R E S E N T S", True, (0,200,0))
            ps_s = pygame.Surface(pt.get_size(), pygame.SRCALPHA)
            ps_s.blit(pt, (0,0)); ps_s.set_alpha(pa)
            if self._logo_retro:
                lw,lh=self._logo_retro.get_size(); scale=min(0.85,700/lw,(SCREEN_H*0.55)/lh)
                nh=int(lh*scale); pres_y=SCREEN_H//2-nh//2-30+nh+18
            else:
                pres_y=SCREEN_H//2+60
            surf.blit(ps_s, (SCREEN_W//2 - pt.get_width()//2, pres_y))

    # ── SPLASH 2 — Realm of Shadows teaser + loading ─────────────────────────

    def _draw_splash2(self, surf):
        t_s = self._s2_t

        # Fade-in alpha for the whole card
        if t_s < S2_FADE_IN:
            card_a = int(255 * t_s / S2_FADE_IN)
        elif t_s < S2_MIN_HOLD:
            card_a = 255
        elif self._batch2_done and t_s >= S2_MIN_HOLD:
            elapsed_out = t_s - S2_MIN_HOLD
            card_a = max(0, int(255 * (1 - elapsed_out / S2_FADE_OUT)))
        else:
            card_a = 255

        if card_a <= 0:
            return

        # Dark atmospheric background with very slow pulse
        t_sec = t_s / 1000.0
        pulse = 0.5 + 0.5 * math.sin(t_sec * 0.4)

        # Background shimmer — faint purple mist
        for y in range(0, SCREEN_H, 3):
            d = abs(y - SCREEN_H//2) / (SCREEN_H//2)
            a = int(card_a * 0.12 * (1 - d**1.5) * (0.7 + 0.3 * pulse))
            if a > 0:
                sl = pygame.Surface((SCREEN_W, 3), pygame.SRCALPHA)
                sl.fill((20, 0, 40, a))
                surf.blit(sl, (0, y))

        # Vertical gradient vignette
        for y in range(0, SCREEN_H, 4):
            edge = min(y, SCREEN_H-y) / (SCREEN_H//2)
            a = int(card_a * 0.5 * (1-edge))
            if a > 0:
                sv = pygame.Surface((SCREEN_W, 4), pygame.SRCALPHA)
                sv.fill((0,0,0,a)); surf.blit(sv, (0,y))

        # Sparse drifting particles
        rng = random.Random(int(t_sec * 0.5))
        for _ in range(30):
            px = rng.randint(0, SCREEN_W)
            py = int((rng.randint(0, SCREEN_H) + t_s * 0.02) % SCREEN_H)
            pa2 = int(card_a * 0.25 * rng.random())
            if pa2 > 0:
                ps = pygame.Surface((2,2), pygame.SRCALPHA)
                ps.fill((120,60,180,pa2)); surf.blit(ps, (px,py))

        # ── Central quote ────────────────────────────────────────────────────
        quote_lines = [
            "The Fading does not announce itself.",
            "It simply… arrives."
        ]
        cy = SCREEN_H//2 - 60
        for i, line in enumerate(quote_lines):
            # Stagger appearance
            line_delay = i * 600
            line_a = min(card_a, max(0, int(card_a * min(1.0, (t_s - line_delay) / 800))))
            if line_a <= 0:
                continue
            fq = pygame.font.SysFont("serif", 22, italic=True)
            tq = fq.render(line, True, (180, 150, 220))
            ts_q = pygame.Surface(tq.get_size(), pygame.SRCALPHA)
            ts_q.blit(tq, (0,0)); ts_q.set_alpha(line_a)
            surf.blit(ts_q, (SCREEN_W//2 - tq.get_width()//2, cy + i*40))

        # Decorative line
        line_a2 = min(card_a, max(0, int(card_a * min(1.0, (t_s - 1200) / 600))))
        if line_a2 > 0:
            ls = pygame.Surface((300, 1), pygame.SRCALPHA)
            ls.fill((100, 60, 160, line_a2))
            surf.blit(ls, (SCREEN_W//2-150, cy + 90))

        # Game name (small, atmospheric)
        gn_a = min(card_a, max(0, int(card_a * min(1.0, (t_s - 1800) / 700))))
        if gn_a > 0:
            fg = pygame.font.SysFont("monospace", 14)
            tg = fg.render("REALM  OF  SHADOWS", True, (100, 80, 140))
            tgs = pygame.Surface(tg.get_size(), pygame.SRCALPHA)
            tgs.blit(tg,(0,0)); tgs.set_alpha(gn_a)
            surf.blit(tgs, (SCREEN_W//2 - tg.get_width()//2, cy + 108))

        # ── Loading progress bar ─────────────────────────────────────────────
        bar_a = min(card_a, max(0, int(card_a * min(1.0, (t_s - 800) / 500))))
        if bar_a > 0:
            bar_w, bar_h = 400, 6
            bar_x = SCREEN_W//2 - bar_w//2
            bar_y = SCREEN_H - 70

            # Track
            track = pygame.Surface((bar_w, bar_h), pygame.SRCALPHA)
            track.fill((40, 20, 60, bar_a))
            surf.blit(track, (bar_x, bar_y))

            # Fill
            fill_w = int(bar_w * self._b2_pct)
            if fill_w > 0:
                fill = pygame.Surface((fill_w, bar_h), pygame.SRCALPHA)
                # Gradient: dim purple → bright neon
                for bx in range(fill_w):
                    frac = bx / bar_w
                    gc = int(bar_a * (0.3 + 0.7 * frac))
                    rc = int(bar_a * 0.1 * frac)
                    fill.fill((rc, gc*2//3, gc),
                               pygame.Rect(bx, 0, 1, bar_h))
                surf.blit(fill, (bar_x, bar_y))

            # Border
            bord = pygame.Surface((bar_w+2, bar_h+2), pygame.SRCALPHA)
            pygame.draw.rect(bord, (80, 40, 120, bar_a), (0,0,bar_w+2,bar_h+2), 1)
            surf.blit(bord, (bar_x-1, bar_y-1))

            # Label
            fl = pygame.font.SysFont("monospace", 11)
            if self._batch2_done:
                label_text = "Ready"
                label_col  = (0, 200, 0)
            else:
                label_text = self._b2_label[:48]
                label_col  = (100, 80, 130)
            tl = fl.render(label_text, True, label_col)
            tls = pygame.Surface(tl.get_size(), pygame.SRCALPHA)
            tls.blit(tl,(0,0)); tls.set_alpha(bar_a)
            surf.blit(tls, (SCREEN_W//2 - tl.get_width()//2, bar_y + 10))

    # ── TITLE + MENU ──────────────────────────────────────────────────────────

    def _draw_title(self, surf, mx, my):
        t = self._title_t

        # Starfield
        for sx,sy,sr,speed,phase in self._stars:
            a = int(55 + 45*math.sin(t*speed+phase))
            s = pygame.Surface((sr*2,sr*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (200,180,255,a), (sr,sr), sr)
            surf.blit(s, (sx-sr, sy-sr))

        # Shadow tendrils
        rng2 = random.Random(int(t*1.5))
        tend = pygame.Surface((SCREEN_W,SCREEN_H), pygame.SRCALPHA)
        for _ in range(10):
            ox=rng2.randint(0,SCREEN_W); ln=rng2.randint(80,180)
            px,py=float(ox),0.0
            for step in range(ln):
                nx=px+rng2.uniform(-5,5); ny=py+1
                a=max(0,int(70*(1-step/ln)))
                pygame.draw.line(tend,(60,0,100,a),(int(px),int(py)),(int(nx),int(ny)),2)
                px,py=nx,ny
        surf.blit(tend,(0,0))

        _draw_retro_dungeon_art(surf, t)

        pulse = abs(math.sin(t*1.05))
        rc=(int(210+45*pulse),int(180+30*pulse),int(20*pulse))
        sc=(int(140+60*pulse),int(110+50*pulse),int(180+40*pulse))
        gw=pygame.Surface((380,80),pygame.SRCALPHA)
        gw.fill((80,20,140,int(40+30*pulse))); surf.blit(gw,(SCREEN_W//2-190,30))
        draw_text(surf,"REALM",  SCREEN_W//2-125,36,  rc,52,bold=True)
        draw_text(surf,"of",     SCREEN_W//2-22, 94,  (180,160,220),22)
        draw_text(surf,"SHADOWS",SCREEN_W//2-165,118, sc,52,bold=True)
        draw_text(surf,"The Fading comes for all things.",
                  SCREEN_W//2-178,180,(140,110,180),15)
        draw_text(surf,"A Bad Bat Enterprises Game",
                  SCREEN_W//2-148,SCREEN_H-38,(0,130,0),14)

        if self._menu_alpha > 10:
            self._draw_menu(surf, mx, my, self._menu_alpha)

    def _draw_menu(self, surf, mx, my, alpha):
        from core.save_load import list_saves
        has_saves = bool(list_saves())

        btn_y = SCREEN_H//2 + 230
        new_r  = pygame.Rect(SCREEN_W//2-220, btn_y, 200, 52)
        cont_r = pygame.Rect(SCREEN_W//2+20,  btn_y, 200, 52)
        self._new_rect  = new_r
        self._cont_rect = cont_r if has_saves else None

        def btn(rect, label, enabled, hov):
            bs = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            bg = (60,110,200,int(alpha*.9)) if (hov and enabled) else \
                 ((40,80,140,int(alpha*.85)) if enabled else (40,40,60,int(alpha*.5)))
            pygame.draw.rect(bs, bg, (0,0,rect.width,rect.height), border_radius=6)
            bc = (100,160,255,alpha) if (enabled and hov) else (70,100,180,alpha)
            pygame.draw.rect(bs, bc, (0,0,rect.width,rect.height), 2, border_radius=6)
            surf.blit(bs, rect.topleft)
            tc = (255,255,255) if (hov and enabled) else ((220,220,255) if enabled else (80,80,100))
            f  = pygame.font.SysFont("monospace", 17, bold=True)
            t  = f.render(label, True, tc)
            ta = pygame.Surface(t.get_size(), pygame.SRCALPHA)
            ta.blit(t,(0,0)); ta.set_alpha(alpha)
            surf.blit(ta, (rect.x+rect.width//2-t.get_width()//2,
                           rect.y+rect.height//2-t.get_height()//2))

        btn(new_r,  "New Game", True,      new_r.collidepoint(mx,my)  if alpha>=200 else False)
        btn(cont_r, "Continue", has_saves, cont_r.collidepoint(mx,my) if (has_saves and alpha>=200) else False)
        if not has_saves:
            fh = pygame.font.SysFont("monospace", 11)
            ht = fh.render("(no saves found)", True, (80,80,100))
            hs = pygame.Surface(ht.get_size(), pygame.SRCALPHA)
            hs.blit(ht,(0,0)); hs.set_alpha(alpha)
            surf.blit(hs, (cont_r.x+cont_r.width//2-ht.get_width()//2, cont_r.bottom+6))
