"""
Realm of Shadows — Intro / Splash sequence
Three phases:
  Phase 0 (SPLASH):  Bad Bat Enterprises retro-pixelated logo fades in,
                     holds, then "PRESENTS" appears beneath it, then fades out.
  Phase 1 (TITLE):   Game title screen with retro dungeon-crawl artwork,
                     animated starfield, title text, tagline — plays title music.
  Phase 2 (MENU):    "New Game" and "Continue" click-buttons appear.
                     No keypress navigation — mouse only.

The caller checks .done (bool) and .action ('new_game' | 'continue' | None).
"""

import pygame
import math
import random
import os

# ── constants pulled from renderer ────────────────────────────────────────────
try:
    from ui.renderer import SCREEN_W, SCREEN_H, draw_text, BG_COLOR
except ImportError:
    SCREEN_W, SCREEN_H, BG_COLOR = 1440, 900, (12, 10, 24)
    def draw_text(surf, text, x, y, color, size, bold=False):
        f = pygame.font.SysFont("monospace", size, bold=bold)
        surf.blit(f.render(text, True, color), (x, y))

BLACK  = (0,   0,   0)
WHITE  = (255, 255, 255)
GREEN  = (0,   255, 0)
DKGREEN= (0,   160, 0)
GOLD   = (220, 180, 40)
DIM_GOLD=(160, 130, 30)
GREY   = (120, 110, 130)
CREAM  = (220, 210, 190)

# ── logo path ─────────────────────────────────────────────────────────────────
_LOGO_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "assets", "bad_bat_logo.png"
)

# ── timing (ms) ───────────────────────────────────────────────────────────────
SPLASH_FADE_IN   = 1200
SPLASH_HOLD      = 1600
PRESENTS_FADE    =  700
PRESENTS_HOLD    = 1000
SPLASH_FADE_OUT  =  900
TITLE_FADE_IN    =  800
TITLE_HOLD_MIN   = 2000   # min time on title before menu appears
MENU_APPEAR_DUR  =  600

# ── pixel block size for retro effect ────────────────────────────────────────
PIXEL_BLOCK = 5   # 5×5 real pixels per "retro pixel"


def _make_retro_logo(original_surf, block=PIXEL_BLOCK):
    """
    Downscale → quantise to neon green/transparent → scale back up with big pixels.
    Black and near-black pixels become TRANSPARENT so the logo floats over any BG.
    Bright pixels become neon green (0, lum*1.2, 0).
    """
    import numpy as np

    w, h = original_surf.get_size()
    tiny_w = max(1, w // block)
    tiny_h = max(1, h // block)

    # Downscale (keep SRCALPHA so we see what's transparent in the source)
    tiny = pygame.transform.smoothscale(
        original_surf.convert_alpha(), (tiny_w, tiny_h)
    )

    # Pull RGB + alpha separately (array4d not available in all pygame builds)
    rgb  = pygame.surfarray.array3d(tiny).astype(float)    # [w, h, 3]
    alph = pygame.surfarray.array_alpha(tiny).astype(float) # [w, h]
    R, G, B = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]

    # Luminance weighted by source alpha
    lum = (0.299*R + 0.587*G + 0.114*B) * (alph / 255.0)

    # Threshold: bright → neon green opaque, dark → transparent
    bright = lum > 35
    green_vals = np.clip(lum * 1.3, 0, 255).astype(np.uint8)

    # Build result surface with SRCALPHA
    result_tiny = pygame.Surface((tiny_w, tiny_h), pygame.SRCALPHA)
    result_tiny.fill((0, 0, 0, 0))   # start fully transparent

    # Write green channel and alpha using surfarray
    rgb_view   = pygame.surfarray.pixels3d(result_tiny)
    alpha_view = pygame.surfarray.pixels_alpha(result_tiny)
    rgb_view[:,:,0] = 0
    rgb_view[:,:,1] = np.where(bright, green_vals, 0)
    rgb_view[:,:,2] = 0
    alpha_view[:,:] = np.where(bright, 255, 0).astype(np.uint8)
    del rgb_view, alpha_view

    # Scale up with nearest-neighbour for chunky retro pixels
    retro = pygame.transform.scale(result_tiny, (tiny_w * block, tiny_h * block))
    return retro


def _build_logo_surface():
    """Load the logo from the assets folder, return (original, retro) or (None, None)."""
    try:
        orig = pygame.image.load(_LOGO_PATH).convert_alpha()
        retro = _make_retro_logo(orig)
        return orig, retro
    except Exception:
        return None, None


def _draw_scanlines(surf, alpha=35):
    """Overlay CRT scanlines for extra retro feel."""
    sl = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    for y in range(0, SCREEN_H, 2):
        pygame.draw.line(sl, (0, 0, 0, alpha), (0, y), (SCREEN_W, y))
    surf.blit(sl, (0, 0))


def _draw_retro_dungeon_art(surf, t):
    """
    Draw a Wizardry/Ultima-style first-person dungeon corridor in low-res ASCII-art-ish
    pixels — all procedural, no image files needed.
    t: time in seconds for subtle animation
    """
    cx = SCREEN_W // 2
    art_y = 120          # top of art area
    art_h = 420          # height of art area
    art_w = 640

    # Dark vignette background for the art
    art_rect = pygame.Rect(cx - art_w//2, art_y, art_w, art_h)
    pygame.draw.rect(surf, (4, 3, 8), art_rect)

    # ── Draw 1st-person corridor in pure geometry ────────────────────────
    # Floor/ceiling using converging lines (perspective)
    def corridor_rect(depth, shade):
        shrink = 1.0 / (depth + 1)
        w = int(art_w * shrink * 0.9)
        h = int(art_h * shrink * 0.85)
        x = cx - w // 2
        y = art_y + (art_h - h) // 2
        return pygame.Rect(x, y, w, h), shade

    # Draw corridors back-to-front (far to near)
    for depth in [5, 4, 3, 2, 1]:
        r, shade = corridor_rect(depth, int(30 + depth * 18))
        # Wall fill
        wall_col = (shade, shade // 2, shade // 3)
        pygame.draw.rect(surf, wall_col, r)

        # Floor strip (slightly lighter)
        floor_h = r.height // 3
        floor_r = pygame.Rect(r.x, r.bottom - floor_h, r.width, floor_h)
        fc = (shade + 10, shade // 3, shade // 4)
        pygame.draw.rect(surf, fc, floor_r)

        # Ceiling strip (darker)
        ceil_r = pygame.Rect(r.x, r.y, r.width, floor_h)
        pygame.draw.rect(surf, (shade // 2, shade // 4, shade // 5), ceil_r)

        # Wall outline
        pygame.draw.rect(surf, (shade + 20, shade // 2 + 10, shade // 3 + 8), r, 1)

    # ── Doorway at the end ───────────────────────────────────────────────
    door_w, door_h = 48, 72
    door_x = cx - door_w // 2
    door_y = art_y + art_h // 2 - door_h // 2
    # Glowing void beyond
    glow_alpha = int(80 + 40 * math.sin(t * 1.2))
    glow = pygame.Surface((door_w + 20, door_h + 20), pygame.SRCALPHA)
    glow.fill((40, 0, 80, glow_alpha))
    surf.blit(glow, (door_x - 10, door_y - 10))
    pygame.draw.rect(surf, (8, 0, 20), (door_x, door_y, door_w, door_h))
    pygame.draw.rect(surf, (120, 60, 180), (door_x, door_y, door_w, door_h), 2)

    # ── Torches on the nearest walls ─────────────────────────────────────
    torch_flicker = 0.7 + 0.3 * math.sin(t * 8.3)
    for tx, ty in [(cx - 180, art_y + art_h // 2 - 20),
                   (cx + 140, art_y + art_h // 2 - 20)]:
        # Torch body
        pygame.draw.rect(surf, (100, 60, 30), (tx - 3, ty, 6, 20))
        # Flame
        flame_h = int(18 * torch_flicker)
        flame_col = (int(255 * torch_flicker), int(140 * torch_flicker), 20)
        pygame.draw.ellipse(surf, flame_col,
                            (tx - 5, ty - flame_h, 10, flame_h + 4))
        # Torch glow halo
        halo = pygame.Surface((60, 60), pygame.SRCALPHA)
        ha = int(35 * torch_flicker)
        pygame.draw.circle(halo, (200, 100, 20, ha), (30, 30), 28)
        surf.blit(halo, (tx - 30, ty - 30))

    # ── Shadowy figure in the doorway ────────────────────────────────────
    fig_alpha = int(60 + 30 * math.sin(t * 0.6))
    fig_surf = pygame.Surface((20, 40), pygame.SRCALPHA)
    fig_surf.fill((30, 0, 50, fig_alpha))
    surf.blit(fig_surf, (cx - 10, door_y + 14))

    # ── Floating rune text (retro ASCII art feel) ─────────────────────────
    rune_chars = ["◆", "◇", "○", "×", "✦"]
    rng = random.Random(99)
    for _ in range(8):
        rx = rng.randint(art_rect.left + 20, art_rect.right - 20)
        ry = rng.randint(art_rect.top + 20, art_rect.bottom - 40)
        ra = int(30 + 25 * math.sin(t * rng.uniform(0.5, 1.5) + rng.random() * 6))
        rc = rng.choice(rune_chars)
        rs = pygame.Surface((16, 16), pygame.SRCALPHA)
        try:
            f = pygame.font.SysFont("monospace", 12)
            txt = f.render(rc, True, (180, 100, 255, ra))
            surf.blit(txt, (rx, ry))
        except Exception:
            pass

    # Art border — chunky CRT pixel-art look
    pygame.draw.rect(surf, (60, 30, 100), art_rect, 3)
    pygame.draw.rect(surf, (30, 15, 50), art_rect.inflate(6, 6), 2)


class IntroScreen:
    """
    Manages the full intro sequence.

    States:
      'splash'   — company logo
      'title'    — game title art
      'menu'     — New Game / Continue buttons
    """

    def __init__(self):
        self.t = 0             # ms elapsed in current phase
        self.phase = 'splash'
        self.done = False
        self.action = None     # 'new_game' | 'continue'

        # Derived splash timing thresholds
        self._splash_presents_start = SPLASH_FADE_IN + SPLASH_HOLD
        self._splash_out_start      = (SPLASH_FADE_IN + SPLASH_HOLD
                                       + PRESENTS_FADE + PRESENTS_HOLD)
        self._splash_total          = self._splash_out_start + SPLASH_FADE_OUT

        # Load and retro-ify the logo
        self._logo_orig, self._logo_retro = _build_logo_surface()

        # Starfield for title screen
        rng = random.Random(77)
        self._stars = [
            (rng.randint(0, SCREEN_W),
             rng.randint(0, SCREEN_H),
             rng.randint(1, 2),
             rng.uniform(0.3, 1.2),
             rng.random() * 6.28)
            for _ in range(120)
        ]

        # Title screen state
        self._title_t = 0.0
        self._menu_alpha = 0

        # Button rects (set in draw)
        self._new_rect  = None
        self._cont_rect = None

        # Sound — play title music when we reach the title phase
        self._title_music_started = False

    # ── public API ────────────────────────────────────────────────────────────

    def update(self, dt_ms):
        """Call once per frame with millisecond delta."""
        self.t += dt_ms
        if self.phase == 'splash' and self.t >= self._splash_total:
            self._transition_to_title()
        elif self.phase == 'title':
            self._title_t += dt_ms / 1000.0
            if self._title_t * 1000 > TITLE_HOLD_MIN:
                self._menu_alpha = min(255,
                    self._menu_alpha + int(dt_ms * 255 / MENU_APPEAR_DUR))

    def handle_click(self, mx, my):
        """Return 'new_game', 'continue', or None."""
        if self.phase != 'menu':
            return None
        if self._new_rect and self._new_rect.collidepoint(mx, my):
            self.done = True
            self.action = 'new_game'
            return 'new_game'
        if self._cont_rect and self._cont_rect.collidepoint(mx, my):
            self.done = True
            self.action = 'continue'
            return 'continue'
        return None

    def draw(self, surf, mx, my):
        surf.fill(BLACK)
        if self.phase == 'splash':
            self._draw_splash(surf)
        elif self.phase in ('title', 'menu'):
            self._draw_title(surf, mx, my)
        _draw_scanlines(surf)

    # ── internal ─────────────────────────────────────────────────────────────

    def _transition_to_title(self):
        self.phase = 'title'
        self.t = 0
        self._title_t = 0.0
        # Start title music
        if not self._title_music_started:
            self._title_music_started = True
            try:
                from core import sound as sfx
                sfx.stop_music()
                sfx.stop_ambient()
                # Use town_briarhollow as the title theme (warm, folk, adventure-inviting)
                sfx.play_music("town_briarhollow")
            except Exception:
                pass

    def _splash_alpha(self):
        """Return current alpha (0-255) for the logo."""
        t = self.t
        if t < SPLASH_FADE_IN:
            return int(255 * t / SPLASH_FADE_IN)
        elif t < SPLASH_FADE_IN + SPLASH_HOLD:
            return 255
        elif t < self._splash_out_start:
            return 255
        else:
            elapsed = t - self._splash_out_start
            return max(0, int(255 * (1 - elapsed / SPLASH_FADE_OUT)))

    def _presents_alpha(self):
        t = self.t
        start = self._splash_presents_start
        if t < start:
            return 0
        elif t < start + PRESENTS_FADE:
            return int(255 * (t - start) / PRESENTS_FADE)
        elif t < self._splash_out_start:
            return 255
        else:
            elapsed = t - self._splash_out_start
            return max(0, int(255 * (1 - elapsed / SPLASH_FADE_OUT)))

    def _draw_splash(self, surf):
        logo_a = self._splash_alpha()
        pres_a = self._presents_alpha()

        surf.fill((0, 0, 0))

        # Dim green phosphor glow backdrop — makes the retro logo pop
        if logo_a > 0:
            glow_w, glow_h = 760, 260
            glow_x = SCREEN_W // 2 - glow_w // 2
            glow_y = SCREEN_H // 2 - glow_h // 2 - 30
            glow_surf = pygame.Surface((glow_w, glow_h), pygame.SRCALPHA)
            ga = int(logo_a * 0.18)
            # Radial gradient: dark center glow
            for r in range(0, min(glow_w, glow_h) // 2, 4):
                frac = 1.0 - r / (min(glow_w, glow_h) // 2)
                a = int(ga * frac ** 2)
                pygame.draw.ellipse(glow_surf, (0, 40, 0, a),
                    (glow_w//2 - r*2, glow_h//2 - r, r*4, r*2))
            surf.blit(glow_surf, (glow_x, glow_y))

        # Logo
        if self._logo_retro and logo_a > 0:
            lw, lh = self._logo_retro.get_size()
            # Scale to fit — max 700px wide, max 55% of screen height
            scale = min(0.85, 700 / lw, (SCREEN_H * 0.55) / lh)
            nw, nh = int(lw * scale), int(lh * scale)
            logo_scaled = pygame.transform.scale(self._logo_retro, (nw, nh))
            lx = SCREEN_W // 2 - nw // 2
            ly = SCREEN_H // 2 - nh // 2 - 30

            # Fade: composite via an alpha-multiplied copy
            # Since logo_scaled is SRCALPHA, we use a temp surface
            faded = pygame.Surface((nw, nh), pygame.SRCALPHA)
            faded.blit(logo_scaled, (0, 0))
            # Multiply per-pixel alpha by logo_a/255
            alpha_arr = pygame.surfarray.pixels_alpha(faded)
            import numpy as np
            alpha_arr[:] = (alpha_arr.astype(np.float32) * logo_a / 255).astype(np.uint8)
            del alpha_arr
            surf.blit(faded, (lx, ly))
        else:
            # Fallback text logo
            f_big = pygame.font.SysFont("monospace", 52, bold=True)
            f_sub = pygame.font.SysFont("monospace", 28, bold=True)
            txt1 = f_big.render("BAD BAT", True, (0, 220, 0))
            txt2 = f_sub.render("ENTERPRISES", True, (0, 180, 0))
            alpha_surf = pygame.Surface(txt1.get_size(), pygame.SRCALPHA)
            alpha_surf.blit(txt1, (0, 0))
            alpha_surf.set_alpha(logo_a)
            surf.blit(alpha_surf, (SCREEN_W // 2 - txt1.get_width() // 2,
                                   SCREEN_H // 2 - 80))
            alpha_surf2 = pygame.Surface(txt2.get_size(), pygame.SRCALPHA)
            alpha_surf2.blit(txt2, (0, 0))
            alpha_surf2.set_alpha(logo_a)
            surf.blit(alpha_surf2, (SCREEN_W // 2 - txt2.get_width() // 2,
                                    SCREEN_H // 2 - 10))

        # "PRESENTS" text
        if pres_a > 0:
            f_pres = pygame.font.SysFont("monospace", 22, bold=False)
            txt = f_pres.render("P R E S E N T S", True, (0, 200, 0))
            ps = pygame.Surface(txt.get_size(), pygame.SRCALPHA)
            ps.blit(txt, (0, 0))
            ps.set_alpha(pres_a)
            if self._logo_retro:
                lw, lh = self._logo_retro.get_size()
                scale = min(0.7, 700 / lw)
                nh = int(lh * scale)
                pres_y = SCREEN_H // 2 - nh // 2 - 40 + nh + 20
            else:
                pres_y = SCREEN_H // 2 + 60
            surf.blit(ps, (SCREEN_W // 2 - txt.get_width() // 2, pres_y))

    def _draw_title(self, surf, mx, my):
        t = self._title_t

        # ── Starfield ────────────────────────────────────────────────────────
        for sx, sy, sr, speed, phase in self._stars:
            alpha = int(55 + 45 * math.sin(t * speed + phase))
            s = pygame.Surface((sr * 2, sr * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (200, 180, 255, alpha), (sr, sr), sr)
            surf.blit(s, (sx - sr, sy - sr))

        # ── Shadow tendrils ───────────────────────────────────────────────────
        rng2 = random.Random(int(t * 1.5))
        tend = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        for i in range(10):
            ox = rng2.randint(0, SCREEN_W)
            ln = rng2.randint(80, 180)
            px, py = float(ox), 0.0
            for step in range(ln):
                nx = px + rng2.uniform(-5, 5)
                ny = py + 1
                a = max(0, int(70 * (1 - step / ln)))
                pygame.draw.line(tend, (60, 0, 100, a),
                                 (int(px), int(py)), (int(nx), int(ny)), 2)
                px, py = nx, ny
        surf.blit(tend, (0, 0))

        # ── Retro dungeon art ─────────────────────────────────────────────────
        _draw_retro_dungeon_art(surf, t)

        # ── Title text ────────────────────────────────────────────────────────
        pulse = abs(math.sin(t * 1.05))
        r_col = (int(210 + 45 * pulse), int(180 + 30 * pulse), int(20 * pulse))
        s_col = (int(140 + 60 * pulse), int(110 + 50 * pulse), int(180 + 40 * pulse))

        # Glow behind REALM
        gw = pygame.Surface((380, 80), pygame.SRCALPHA)
        gw.fill((80, 20, 140, int(40 + 30 * pulse)))
        surf.blit(gw, (SCREEN_W // 2 - 190, 30))

        draw_text(surf, "REALM",   SCREEN_W // 2 - 125, 36,   r_col, 52, bold=True)
        draw_text(surf, "of",      SCREEN_W // 2 - 22,  94,   (180, 160, 220), 22)
        draw_text(surf, "SHADOWS", SCREEN_W // 2 - 165, 118,  s_col, 52, bold=True)

        draw_text(surf, "The Fading comes for all things.",
                  SCREEN_W // 2 - 178, 180, (140, 110, 180), 15)

        # ── Company credit line ───────────────────────────────────────────────
        draw_text(surf, "A Bad Bat Enterprises Game",
                  SCREEN_W // 2 - 148, SCREEN_H - 38, (0, 130, 0), 14)

        # ── Menu buttons (fade in) ────────────────────────────────────────────
        if self._menu_alpha > 10:
            self._draw_menu(surf, mx, my, self._menu_alpha)
            if self._menu_alpha >= 255:
                self.phase = 'menu'

    def _draw_menu(self, surf, mx, my, alpha):
        from core.save_load import list_saves
        has_saves = bool(list_saves())

        btn_y = SCREEN_H // 2 + 230
        new_r  = pygame.Rect(SCREEN_W // 2 - 220, btn_y,       200, 52)
        cont_r = pygame.Rect(SCREEN_W // 2 + 20,  btn_y,       200, 52)
        self._new_rect  = new_r
        self._cont_rect = cont_r if has_saves else None

        # Draw buttons with alpha
        def draw_btn(rect, label, enabled, hovered):
            btn_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            bg_col = (40, 80, 140, int(alpha * 0.85)) if enabled else (40, 40, 60, int(alpha * 0.5))
            if hovered and enabled:
                bg_col = (60, 110, 200, int(alpha * 0.9))
            pygame.draw.rect(btn_surf, bg_col, (0, 0, rect.width, rect.height), border_radius=6)
            border_col = (100, 160, 255, alpha) if (enabled and hovered) else (70, 100, 180, alpha)
            pygame.draw.rect(btn_surf, border_col, (0, 0, rect.width, rect.height), 2, border_radius=6)
            surf.blit(btn_surf, rect.topleft)

            text_col = (220, 220, 255) if enabled else (80, 80, 100)
            if hovered and enabled:
                text_col = (255, 255, 255)
            f = pygame.font.SysFont("monospace", 17, bold=True)
            txt = f.render(label, True, text_col)
            # Alpha-blend text
            ta = pygame.Surface(txt.get_size(), pygame.SRCALPHA)
            ta.blit(txt, (0, 0))
            ta.set_alpha(alpha)
            surf.blit(ta, (rect.x + rect.width // 2 - txt.get_width() // 2,
                           rect.y + rect.height // 2 - txt.get_height() // 2))

        draw_btn(new_r, "New Game", True,
                 new_r.collidepoint(mx, my) if alpha >= 200 else False)
        draw_btn(cont_r, "Continue", has_saves,
                 cont_r.collidepoint(mx, my) if (has_saves and alpha >= 200) else False)

        if not has_saves:
            f_hint = pygame.font.SysFont("monospace", 11)
            hint = f_hint.render("(no saves found)", True, (80, 80, 100))
            hs = pygame.Surface(hint.get_size(), pygame.SRCALPHA)
            hs.blit(hint, (0, 0)); hs.set_alpha(alpha)
            surf.blit(hs, (cont_r.x + cont_r.width // 2 - hint.get_width() // 2,
                           cont_r.bottom + 6))
