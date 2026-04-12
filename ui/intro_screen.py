"""
Realm of Shadows — Intro sequence  (5 phases)

  HIRES   Full-colour high-res logo on black, fades in and holds
  RETRO   Cross-fades to 5×5 pixel-art version + "P R E S E N T S"
  LOAD    Atmospheric card, lore quote, progress bar, music starts early
  TITLE   Game title + dungeon corridor art (no overlap), tagline, credit
  MENU    New Game / Continue click buttons
"""

import pygame, math, random, os
import numpy as np

try:
    from ui.renderer import SCREEN_W, SCREEN_H, draw_text
except ImportError:
    SCREEN_W, SCREEN_H = 1440, 900
    def draw_text(surf, text, x, y, color, size, bold=False):
        f = pygame.font.SysFont("monospace", size, bold=bold)
        surf.blit(f.render(text, True, color), (x, y))

BLACK = (0, 0, 0)

# Try .jpg first (new logo), fall back to .png (old)
_ASSETS = os.path.dirname(os.path.dirname(__file__)) + "/assets/"
_LOGO_JPG = _ASSETS + "bad_bat_logo.jpg"
_LOGO_PNG = _ASSETS + "bad_bat_logo.png"
_TITLE_BG = _ASSETS + "title_screen.png"

# ── timing (ms) ──────────────────────────────────────────────────────────────
T_HIRES_FADE_IN   =  900
T_HIRES_HOLD      = 3000
T_FADE_TO_BLACK   =  700   # hires fades out to black
T_BLACK_HOLD      =  350   # pure black pause between logos
T_RETRO_FADE_IN   =  900   # retro fades in from black
T_RETRO_HOLD      = 2200   # retro logo fully visible
T_RETRO_OUT       =  700   # retro fades out before load screen
# legacy alias used in update()
T_CROSS_FADE      = T_FADE_TO_BLACK + T_BLACK_HOLD + T_RETRO_FADE_IN

T_LOAD_FADE_IN    =  500
T_LOAD_MIN_HOLD   = 6500   # long enough to read the quote fully
T_LOAD_FADE_OUT   =  900

T_TITLE_FADE_IN   =  600
T_TITLE_MIN_HOLD  = 2500
T_MENU_APPEAR     =  600

PIXEL_BLOCK = 5


# ── logo helpers ──────────────────────────────────────────────────────────────

def _load_hires():
    for path in (_LOGO_JPG, _LOGO_PNG):
        if os.path.exists(path):
            try:
                raw = pygame.image.load(path).convert()
                # Zero out the outermost 2px on all sides — the JPEG has a
                # 1px grey border (130-208 grey) that smoothscale blurs into
                # a visible halo when downscaled.  Zeroing 2px ensures it is
                # fully eliminated after bilinear interpolation.
                arr = pygame.surfarray.pixels3d(raw)
                arr[:, :2, :]  = 0   # top 2 rows
                arr[:, -2:, :] = 0   # bottom 2 rows
                arr[:2, :, :]  = 0   # left 2 cols
                arr[-2:, :, :] = 0   # right 2 cols
                del arr
                return raw
            except Exception:
                pass
    return None


def _make_retro(orig, block=PIXEL_BLOCK):
    """
    Max-pool each block → keep brightest green → 
    neon green SRCALPHA surface (transparent bg).
    """
    w, h = orig.get_size()
    tw, th = w // block, h // block
    arr = pygame.surfarray.array3d(orig).transpose(1, 0, 2).astype(np.float32)
    G, R, B = arr[:,:,1], arr[:,:,0], arr[:,:,2]
    Gp = G[:th*block,:tw*block].reshape(th,block,tw,block).max(axis=(1,3))
    Rp = R[:th*block,:tw*block].reshape(th,block,tw,block).max(axis=(1,3))
    Bp = B[:th*block,:tw*block].reshape(th,block,tw,block).max(axis=(1,3))
    logo = (Gp > 60) & (Gp > Rp*1.3) & (Gp > Bp*1.3)
    neon  = np.clip(Gp * 1.15, 0, 255).astype(np.uint8)
    res   = pygame.Surface((tw, th), pygame.SRCALPHA); res.fill((0,0,0,0))
    rv    = pygame.surfarray.pixels3d(res)
    av    = pygame.surfarray.pixels_alpha(res)
    lT, nT = logo.T, neon.T
    rv[:,:,0] = 0; rv[:,:,1] = np.where(lT, nT, 0); rv[:,:,2] = 0
    av[:,:] = np.where(lT, 255, 0).astype(np.uint8)
    del rv, av
    return pygame.transform.scale(res, (tw*block, th*block))


def _scale_logo(surf, max_w, max_h):
    w, h = surf.get_size()
    scale = min(max_w/w, max_h/h, 1.0)
    nw, nh = int(w*scale), int(h*scale)
    if surf.get_flags() & pygame.SRCALPHA:
        return pygame.transform.smoothscale(surf, (nw,nh)), nw, nh
    else:
        return pygame.transform.smoothscale(surf, (nw,nh)), nw, nh


def _blit_alpha(dest, src, pos, alpha):
    if alpha <= 0: return
    if alpha >= 255: dest.blit(src, pos); return
    if src.get_flags() & pygame.SRCALPHA:
        tmp = src.copy()
        av = pygame.surfarray.pixels_alpha(tmp)
        av[:] = (av.astype(np.float32)*alpha/255).astype(np.uint8)
        del av
        dest.blit(tmp, pos)
    else:
        tmp = src.copy(); tmp.set_alpha(alpha); dest.blit(tmp, pos)


def _scanlines(surf, a=25):
    sl = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    for y in range(0, SCREEN_H, 2):
        pygame.draw.line(sl,(0,0,0,a),(0,y),(SCREEN_W,y))
    surf.blit(sl,(0,0))


# ── dungeon corridor art ─────────────────────────────────────────────────────

def _dungeon_art(surf, t, art_rect):
    """
    Wizardry/Ultima-style first-person dungeon corridor.
    - 5-layer perspective walls (stone shading, floor/ceiling strips)
    - Portcullis door: stone arch + iron bar grate + glowing void through bars
    - Two wall-mounted torches correctly positioned on depth-1 wall face
    - Visible humanoid figure behind the portcullis
    """
    cx = art_rect.centerx
    ay = art_rect.top
    aw = art_rect.width
    ah = art_rect.height

    # Background
    pygame.draw.rect(surf, (6, 4, 10), art_rect)

    # ── 5 depth layers (back → front) ────────────────────────────────────────
    wall_rects = {}
    for depth in [5, 4, 3, 2, 1]:
        shrink = 1.0 / (depth + 1)
        w2 = int(aw * shrink * 0.90)
        h2 = int(ah * shrink * 0.82)
        x2 = cx - w2 // 2
        y2 = ay + (ah - h2) // 2
        r  = pygame.Rect(x2, y2, w2, h2)
        wall_rects[depth] = r
        sh = int(28 + depth * 20)
        # Wall fill
        pygame.draw.rect(surf, (sh, sh//2, sh//3), r)
        # Floor (lower third, lighter)
        fh = r.height // 3
        pygame.draw.rect(surf, (sh+12, sh//3+4, sh//4), pygame.Rect(r.x, r.bottom-fh, r.width, fh))
        # Ceiling (upper third, darker)
        pygame.draw.rect(surf, (sh//2-2, sh//4, sh//5), pygame.Rect(r.x, r.y, r.width, fh))
        # Wall outline
        pygame.draw.rect(surf, (sh+24, sh//2+12, sh//3+10), r, 1)

    # ── Portcullis door ───────────────────────────────────────────────────────
    # Positioned at depth-3 scale for visual depth
    d3 = wall_rects[3]
    door_w = d3.width // 3
    door_h = int(d3.height * 0.65)
    door_x = cx - door_w // 2
    # Bottom of door sits on the floor of the depth-3 corridor
    door_y = d3.bottom - door_h - fh // 2

    # Stone archway frame (thick, chunky stone blocks)
    arch_thick = max(8, door_w // 8)
    # Left jamb
    pygame.draw.rect(surf, (55, 45, 35),
                     (door_x - arch_thick, door_y, arch_thick, door_h))
    pygame.draw.rect(surf, (75, 60, 45),
                     (door_x - arch_thick, door_y, arch_thick, door_h), 1)
    # Right jamb
    pygame.draw.rect(surf, (55, 45, 35),
                     (door_x + door_w, door_y, arch_thick, door_h))
    pygame.draw.rect(surf, (75, 60, 45),
                     (door_x + door_w, door_y, arch_thick, door_h), 1)
    # Lintel (top beam)
    pygame.draw.rect(surf, (55, 45, 35),
                     (door_x - arch_thick, door_y - arch_thick,
                      door_w + arch_thick*2, arch_thick))
    pygame.draw.rect(surf, (75, 60, 45),
                     (door_x - arch_thick, door_y - arch_thick,
                      door_w + arch_thick*2, arch_thick), 1)

    # Glowing void beyond the door (pulsing purple/amber)
    glow_pulse = 0.6 + 0.4 * math.sin(t * 1.3)
    void_surf = pygame.Surface((door_w, door_h), pygame.SRCALPHA)
    void_surf.fill((10, 4, 20))
    # Radial glow from centre
    for r2 in range(min(door_w, door_h)//2, 0, -3):
        frac = r2 / (min(door_w, door_h)//2)
        ga = int(glow_pulse * 45 * (1-frac)**1.5)
        if ga > 0:
            pygame.draw.ellipse(void_surf, (40, 15, 70, ga),
                                (door_w//2-r2, door_h//2-r2, r2*2, r2*2))
    surf.blit(void_surf, (door_x, door_y))

    # Portcullis iron bars — vertical bars with 2 horizontal crossbars
    bar_col   = (80, 70, 60)
    bar_count = max(3, door_w // 10)
    bar_gap   = door_w / (bar_count + 1)
    for i in range(bar_count):
        bx = int(door_x + bar_gap * (i + 1))
        pygame.draw.rect(surf, bar_col, (bx-2, door_y, 4, door_h))
        pygame.draw.rect(surf, (110, 95, 80), (bx-2, door_y, 4, door_h), 1)
    # Horizontal crossbars at 1/3 and 2/3 height
    for frac_h in (0.32, 0.66):
        by2 = int(door_y + door_h * frac_h)
        pygame.draw.rect(surf, bar_col, (door_x, by2-2, door_w, 4))
        pygame.draw.rect(surf, (110, 95, 80), (door_x, by2-2, door_w, 4), 1)

    # ── Figure behind portcullis ──────────────────────────────────────────────
    # Visible humanoid silhouette — glowing eyes, visible shape
    fig_alpha = int(155 + 40 * math.sin(t * 0.55))
    fig_cx  = cx
    fig_bot = door_y + door_h - 4
    fig_h   = int(door_h * 0.72)
    fig_w   = int(door_w * 0.38)
    # Body (dark purple-grey, clearly visible)
    fig_surf = pygame.Surface((fig_w, fig_h), pygame.SRCALPHA)
    body_col = (45, 25, 65, fig_alpha)
    # Head (circle)
    head_r = fig_w // 3
    pygame.draw.circle(fig_surf, body_col,
                       (fig_w//2, head_r + 2), head_r)
    # Torso (tapered rectangle)
    torso_top = head_r * 2 + 2
    torso_h   = fig_h - torso_top
    pygame.draw.polygon(fig_surf, body_col, [
        (fig_w//2 - fig_w//3, torso_top),
        (fig_w//2 + fig_w//3, torso_top),
        (fig_w//2 + fig_w//4, torso_top + torso_h),
        (fig_w//2 - fig_w//4, torso_top + torso_h),
    ])
    # Glowing eyes
    eye_y   = head_r + 2 - head_r // 3
    eye_off = head_r // 2
    eye_col = (180, 80, 255, min(255, fig_alpha + 60))
    for ex in (fig_w//2 - eye_off, fig_w//2 + eye_off):
        pygame.draw.circle(fig_surf, eye_col, (ex, eye_y), 2)
        # Soft eye glow
        eg = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(eg, (150, 40, 220, 60), (5,5), 4)
        fig_surf.blit(eg, (ex-5, eye_y-5))
    surf.blit(fig_surf, (fig_cx - fig_w//2, fig_bot - fig_h))

    # ── Torches on depth-1 wall face ─────────────────────────────────────────
    # depth-1 wall: x from 585 to 855 (for 600w art centred at 720)
    d1 = wall_rects[1]
    # Place torches 18% in from each side of the depth-1 wall
    torch_inset = int(d1.width * 0.18)
    torch_y     = d1.top + int(d1.height * 0.38)   # upper-middle of wall
    torch_lx    = d1.left  + torch_inset
    torch_rx    = d1.right - torch_inset

    tf = 0.65 + 0.35 * math.sin(t * 9.1)   # fast flicker
    tf2= 0.65 + 0.35 * math.sin(t * 8.3 + 1.2)  # offset for right torch

    for tx, flicker in ((torch_lx, tf), (torch_rx, tf2)):
        # Torch bracket (small iron L-shape on the wall)
        pygame.draw.rect(surf, (70, 50, 30), (tx-2, torch_y+12, 12, 4))   # horizontal arm
        pygame.draw.rect(surf, (70, 50, 30), (tx+8, torch_y+12, 4, 14))   # vertical pin
        # Torch body
        pygame.draw.rect(surf, (120, 75, 30), (tx, torch_y+14, 8, 18))
        # Flame (animated height + colour)
        flame_h = int(16 * flicker)
        flame_w = 10
        flame_y = torch_y + 14 - flame_h
        flame_col = (int(255*flicker), int(130*flicker), 15)
        # Base of flame is wider
        for fy in range(flame_h):
            fw2 = max(2, int(flame_w * (1 - fy/flame_h) * 0.8 + 2))
            fc  = (int(255*flicker*(1-fy/flame_h*0.4)),
                   int((80+50*flicker)*(1-fy/flame_h*0.6)),
                   10)
            pygame.draw.line(surf, fc,
                             (tx+4-fw2//2, flame_y+fy),
                             (tx+4+fw2//2, flame_y+fy))
        # Torch glow halo
        hl = pygame.Surface((50, 50), pygame.SRCALPHA)
        ha = int(50 * flicker)
        pygame.draw.circle(hl, (220, 110, 20, ha), (25,25), 22)
        surf.blit(hl, (tx+4-25, torch_y-11))

    # (no border — art bleeds into the screen)


# ═══════════════════════════════════════════════════════════════════════════
class IntroScreen:
    def __init__(self):
        self.phase  = 'hires'
        self.t      = 0
        self.done   = False
        self.action = None

        orig = _load_hires()
        self._hires = orig
        self._retro = _make_retro(orig) if orig else None

        # Splash timing
        self._hires_total = T_HIRES_FADE_IN + T_HIRES_HOLD
        self._cross_total = T_FADE_TO_BLACK + T_BLACK_HOLD + T_RETRO_FADE_IN + T_RETRO_HOLD + T_RETRO_OUT

        # Batch state
        self._b1_done  = False
        self._b2_done  = False
        self._b2_pct   = 0.0
        self._b2_label = "Preparing…"
        self._music_on = False

        # Title/menu
        self._title_t    = 0.0
        self._menu_alpha = 0
        self._new_rect   = None
        self._cont_rect  = None

        # Starfield
        rng = random.Random(77)
        self._stars = [(rng.randint(0,SCREEN_W),rng.randint(0,SCREEN_H),
                        rng.randint(1,2),rng.uniform(0.3,1.2),rng.random()*6.28)
                       for _ in range(120)]

        # Title screen background image (pixel art — replaces procedural dungeon)
        self._title_bg = None
        if os.path.exists(_TITLE_BG):
            try:
                raw = pygame.image.load(_TITLE_BG).convert_alpha()
                self._title_bg = pygame.transform.scale(raw, (SCREEN_W, 530))
            except Exception:
                self._title_bg = None

    # ── public ───────────────────────────────────────────────────────────────

    def update(self, dt_ms):
        self.t += dt_ms
        self._step_batches()
        if self.phase == 'hires':
            if self.t >= self._hires_total:
                self._go('retro')
        elif self.phase == 'retro':
            if self.t >= self._cross_total:
                self._go('load')
        elif self.phase == 'load':
            if self.t >= T_LOAD_MIN_HOLD + T_LOAD_FADE_OUT and self._b2_done:
                self._go('title')
        elif self.phase == 'title':
            self._title_t += dt_ms / 1000.0
            if self._title_t * 1000 > T_TITLE_MIN_HOLD:
                self._menu_alpha = min(255,
                    self._menu_alpha + int(dt_ms * 255 / T_MENU_APPEAR))
                if self._menu_alpha >= 255:
                    self.phase = 'menu'

    def handle_click(self, mx, my):
        if self.phase not in ('title','menu'): return None
        if self._new_rect  and self._new_rect.collidepoint(mx,my):
            self.done=True; self.action='new_game'; return 'new_game'
        if self._cont_rect and self._cont_rect.collidepoint(mx,my):
            self.done=True; self.action='continue'; return 'continue'
        return None

    def draw(self, surf, mx, my):
        surf.fill(BLACK)
        if   self.phase == 'hires':            self._draw_hires(surf)
        elif self.phase == 'retro':            self._draw_retro(surf)
        elif self.phase == 'load':             self._draw_load(surf)
        elif self.phase in ('title','menu'):   self._draw_title(surf, mx, my)
        _scanlines(surf)

    # ── internal ─────────────────────────────────────────────────────────────

    def _go(self, phase): self.phase=phase; self.t=0

    def _step_batches(self):
        try:
            from core import sound as sfx
            if not sfx._enabled:
                self._b1_done=self._b2_done=True; return
            if not self._b1_done:
                sfx.step_batch1(); self._b1_done=True
            if not self._b2_done:
                done,idx,total,name = sfx.step_batch2()
                self._b2_pct=idx/max(1,total); self._b2_label=name
                if done: self._b2_done=True; self._b2_pct=1.0
                if not self._music_on and sfx._sounds.get("town_briarhollow"):
                    self._music_on=True
                    try: sfx.stop_music(); sfx.stop_ambient(); sfx.play_music("town_briarhollow")
                    except Exception: pass
        except Exception:
            self._b1_done=self._b2_done=True

    # ── PHASE 1: high-res logo ────────────────────────────────────────────────

    def _draw_hires(self, surf):
        if not self._hires: return
        t = self.t
        alpha = min(255, int(255 * t / T_HIRES_FADE_IN)) if t < T_HIRES_FADE_IN else 255
        max_w = int(SCREEN_W * 0.68); max_h = int(SCREEN_H * 0.72)
        ls, nw, nh = _scale_logo(self._hires, max_w, max_h)
        lx = SCREEN_W//2 - nw//2; ly = SCREEN_H//2 - nh//2
        _blit_alpha(surf, ls, (lx, ly), alpha)

    # ── PHASE 2: cross-fade to retro + "PRESENTS" ────────────────────────────

    def _draw_retro(self, surf):
        t = self.t
        max_w = int(SCREEN_W * 0.68); max_h = int(SCREEN_H * 0.72)

        # ── Phase breakdown ──────────────────────────────────────────────────
        # [0 … T_FADE_TO_BLACK]           hires fades out to black
        # [T_FADE_TO_BLACK … +T_BLACK_HOLD]  pure black
        # [+T_BLACK_HOLD … +T_RETRO_FADE_IN]  retro fades in
        # [+T_RETRO_FADE_IN … +T_RETRO_HOLD]  retro holds, "PRESENTS" appears
        # [+T_RETRO_HOLD … +T_RETRO_OUT]   retro fades out

        t1 = T_FADE_TO_BLACK
        t2 = t1 + T_BLACK_HOLD
        t3 = t2 + T_RETRO_FADE_IN
        t4 = t3 + T_RETRO_HOLD
        # t5 = t4 + T_RETRO_OUT  (end)

        # Hires alpha — fades out during first segment
        if t < t1:
            hi_a = max(0, int(255 * (1 - t / t1)))
        else:
            hi_a = 0

        # Retro alpha — fades in during third segment, holds, then fades out
        if t < t2:
            re_a = 0
        elif t < t3:
            re_a = int(255 * (t - t2) / T_RETRO_FADE_IN)
        elif t < t4:
            re_a = 255
        else:
            frac_out = (t - t4) / max(1, T_RETRO_OUT)
            re_a = max(0, int(255 * (1 - frac_out)))

        # "PRESENTS" alpha — fades in once retro is fully up
        if t < t3:
            pr_a = 0
        elif t < t4:
            pr_a = min(255, int(255 * (t - t3) / 600))
        else:
            pr_a = re_a   # fade out with the logo

        # ── Draw ─────────────────────────────────────────────────────────────

        # Hires layer (fading out)
        if hi_a > 0 and self._hires:
            ls, nw, nh = _scale_logo(self._hires, max_w, max_h)
            _blit_alpha(surf, ls, (SCREEN_W // 2 - nw // 2, SCREEN_H // 2 - nh // 2), hi_a)

        # Retro layer
        if re_a > 0 and self._retro:
            rs, nw, nh = _scale_logo(self._retro, max_w, max_h)
            lx = SCREEN_W // 2 - nw // 2; ly = SCREEN_H // 2 - nh // 2

            # Phosphor glow halo
            gw, gh = int(nw * 1.04), int(nh * 1.04)
            gl = pygame.Surface((gw, gh), pygame.SRCALPHA)
            for r2 in range(0, min(gw, gh) // 2, 4):
                frac2 = 1 - r2 / (min(gw, gh) // 2)
                a = int(re_a * 0.12 * frac2 ** 2)
                if a > 0:
                    pygame.draw.ellipse(gl, (0, 40, 0, a),
                                        (gw // 2 - r2 * 2, gh // 2 - r2, r2 * 4, r2 * 2))
            surf.blit(gl, (lx - int(nw * .02), ly - int(nh * .02)))
            _blit_alpha(surf, rs, (lx, ly), re_a)

        # "P R E S E N T S"
        if pr_a > 0 and self._retro:
            rs2, nw2, nh2 = _scale_logo(self._retro, max_w, max_h)
            pres_y = SCREEN_H // 2 + nh2 // 2 + 20
            fp = pygame.font.SysFont("monospace", 20)
            pt = fp.render("P R E S E N T S", True, (0, 210, 0))
            ps = pygame.Surface(pt.get_size(), pygame.SRCALPHA)
            ps.blit(pt, (0, 0)); ps.set_alpha(pr_a)
            surf.blit(ps, (SCREEN_W // 2 - pt.get_width() // 2, pres_y))

    # ── PHASE 3: loading ──────────────────────────────────────────────────────

    def _draw_load(self, surf):
        t_s = self.t
        if t_s < T_LOAD_FADE_IN:
            card_a = int(255*t_s/T_LOAD_FADE_IN)
        elif self._b2_done and t_s >= T_LOAD_MIN_HOLD:
            card_a = max(0,int(255*(1-(t_s-T_LOAD_MIN_HOLD)/T_LOAD_FADE_OUT)))
        else:
            card_a = 255
        if card_a <= 0: return

        t_sec = t_s/1000.0

        # Purple atmospheric bg
        for y in range(0, SCREEN_H, 4):
            d = abs(y-SCREEN_H//2)/(SCREEN_H//2)
            a = int(card_a*0.10*(1-d**1.5))
            if a>0:
                sl=pygame.Surface((SCREEN_W,4),pygame.SRCALPHA)
                sl.fill((18,0,36,a)); surf.blit(sl,(0,y))

        # Drifting particles
        rng=random.Random(int(t_sec*0.5))
        for _ in range(22):
            px=rng.randint(0,SCREEN_W)
            py=int((rng.randint(0,SCREEN_H)+t_s*0.018)%SCREEN_H)
            pa=int(card_a*0.20*rng.random())
            if pa>0:
                ps=pygame.Surface((2,2),pygame.SRCALPHA); ps.fill((120,60,180,pa))
                surf.blit(ps,(px,py))

        # Lore quote
        cy = SCREEN_H//2 - 55
        for i,line in enumerate(["The Fading does not announce itself.","It simply…  arrives."]):
            delay=i*700
            la=min(card_a,max(0,int(card_a*min(1.0,(t_s-delay)/800))))
            if la<=0: continue
            fq=pygame.font.SysFont("serif",22,italic=True)
            tq=fq.render(line,True,(180,150,220))
            ts=pygame.Surface(tq.get_size(),pygame.SRCALPHA)
            ts.blit(tq,(0,0)); ts.set_alpha(la)
            surf.blit(ts,(SCREEN_W//2-tq.get_width()//2,cy+i*42))

        # Separator
        sep_a=min(card_a,max(0,int(card_a*min(1.0,(t_s-1300)/600))))
        if sep_a>0:
            sep=pygame.Surface((280,1),pygame.SRCALPHA)
            sep.fill((100,60,160,sep_a)); surf.blit(sep,(SCREEN_W//2-140,cy+98))

        gn_a=min(card_a,max(0,int(card_a*min(1.0,(t_s-1900)/600))))
        if gn_a>0:
            fg=pygame.font.SysFont("monospace",14)
            tg=fg.render("REALM  OF  SHADOWS",True,(100,80,140))
            tgs=pygame.Surface(tg.get_size(),pygame.SRCALPHA)
            tgs.blit(tg,(0,0)); tgs.set_alpha(gn_a)
            surf.blit(tgs,(SCREEN_W//2-tg.get_width()//2,cy+110))

        # Progress bar
        bar_a=min(card_a,max(0,int(card_a*min(1.0,(t_s-600)/500))))
        if bar_a>0:
            bw,bh=420,6; bx=SCREEN_W//2-bw//2; by=SCREEN_H-72
            tr=pygame.Surface((bw,bh),pygame.SRCALPHA); tr.fill((40,20,60,bar_a))
            surf.blit(tr,(bx,by))
            fw=int(bw*self._b2_pct)
            if fw>0:
                for bxi in range(fw):
                    frac=bxi/bw; gc=int(bar_a*(0.3+0.7*frac))
                    fil=pygame.Surface((1,bh),pygame.SRCALPHA)
                    fil.fill((int(bar_a*0.08*frac),gc*2//3,min(255,gc)))
                    surf.blit(fil,(bx+bxi,by))
            brd=pygame.Surface((bw+2,bh+2),pygame.SRCALPHA)
            pygame.draw.rect(brd,(80,40,120,bar_a),(0,0,bw+2,bh+2),1)
            surf.blit(brd,(bx-1,by-1))
            fl=pygame.font.SysFont("monospace",11)
            lt,lc=("Ready",(0,200,0)) if self._b2_done else (self._b2_label[:50],(100,80,130))
            tl=fl.render(lt,True,lc)
            tls=pygame.Surface(tl.get_size(),pygame.SRCALPHA)
            tls.blit(tl,(0,0)); tls.set_alpha(bar_a)
            surf.blit(tls,(SCREEN_W//2-tl.get_width()//2,by+10))

    # ── PHASE 4 / 5: title + menu ────────────────────────────────────────────

    def _draw_title(self, surf, mx, my):
        t = self._title_t

        # Starfield
        for sx,sy,sr,sp,ph in self._stars:
            a=int(55+45*math.sin(t*sp+ph))
            s=pygame.Surface((sr*2,sr*2),pygame.SRCALPHA)
            pygame.draw.circle(s,(200,180,255,a),(sr,sr),sr); surf.blit(s,(sx-sr,sy-sr))

        # Tendrils
        rng2=random.Random(int(t*1.5))
        tend=pygame.Surface((SCREEN_W,SCREEN_H),pygame.SRCALPHA)
        for _ in range(8):
            ox=rng2.randint(0,SCREEN_W); ln=rng2.randint(60,160)
            px,py=float(ox),0.0
            for step in range(ln):
                nx=px+rng2.uniform(-5,5); ny=py+1
                a=max(0,int(60*(1-step/ln)))
                pygame.draw.line(tend,(60,0,100,a),(int(px),int(py)),(int(nx),int(ny)),2)
                px,py=nx,ny
        surf.blit(tend,(0,0))

        # ── Title text ────────────────────────────────────────────────────────
        pulse=abs(math.sin(t*1.05))
        rc=(int(210+45*pulse),int(180+30*pulse),int(20*pulse))
        sc=(int(140+60*pulse),int(110+50*pulse),int(180+40*pulse))

        # Measure "REALM" and "SHADOWS" widths to perfectly centre "of"
        try:
            f52 = pygame.font.SysFont("monospace", 52, bold=True)
            realm_w   = f52.size("REALM")[0]
            shadows_w = f52.size("SHADOWS")[0]
        except Exception:
            realm_w = 260; shadows_w = 340
        realm_x   = SCREEN_W//2 - realm_w//2
        shadows_x = SCREEN_W//2 - shadows_w//2
        try:
            f22   = pygame.font.SysFont("monospace", 22)
            of_w  = f22.size("of")[0]
        except Exception:
            of_w = 30
        of_x = SCREEN_W//2 - of_w//2

        draw_text(surf,"REALM",  realm_x,   20, rc, 52, bold=True)
        draw_text(surf,"of",     of_x,       78, (180,160,220), 22)
        draw_text(surf,"SHADOWS",shadows_x, 102, sc, 52, bold=True)

        # ── Dungeon art — full-width, no border box ──────────────────────────
        # Starts just below title text, fills to just above tagline
        ART_Y=160; ART_W=SCREEN_W; ART_H=530
        art_rect=pygame.Rect(0, ART_Y, ART_W, ART_H)
        if self._title_bg is not None:
            surf.blit(self._title_bg, (0, ART_Y))
        else:
            _dungeon_art(surf, t, art_rect)

        # ── Below-art text ────────────────────────────────────────────────────
        draw_text(surf,"The Fading comes for all things.",
                  SCREEN_W//2-178, ART_Y+ART_H+8,(140,110,180),15)
        draw_text(surf,"A Bad Bat Enterprises Game",
                  SCREEN_W//2-148,SCREEN_H-28,(0,120,0),13)

        if self._menu_alpha>10:
            self._draw_menu(surf,mx,my,self._menu_alpha)

    def _draw_menu(self, surf, mx, my, alpha):
        from core.save_load import list_saves
        has_saves=bool(list_saves())
        btn_y=160+530+42
        new_r =pygame.Rect(SCREEN_W//2-220,btn_y,200,52)
        cont_r=pygame.Rect(SCREEN_W//2+20, btn_y,200,52)
        self._new_rect =new_r
        self._cont_rect=cont_r if has_saves else None

        def btn(rect,label,enabled,hov):
            bs=pygame.Surface((rect.width,rect.height),pygame.SRCALPHA)
            if hov and enabled: bg=(60,110,200,int(alpha*.9))
            elif enabled:       bg=(40,80,140,int(alpha*.85))
            else:               bg=(40,40,60,int(alpha*.5))
            pygame.draw.rect(bs,bg,(0,0,rect.width,rect.height),border_radius=6)
            bc=(100,160,255,alpha) if (enabled and hov) else (70,100,180,alpha)
            pygame.draw.rect(bs,bc,(0,0,rect.width,rect.height),2,border_radius=6)
            surf.blit(bs,rect.topleft)
            tc=(255,255,255) if (hov and enabled) else ((220,220,255) if enabled else (80,80,100))
            f=pygame.font.SysFont("monospace",17,bold=True)
            tl=f.render(label,True,tc); ta=pygame.Surface(tl.get_size(),pygame.SRCALPHA)
            ta.blit(tl,(0,0)); ta.set_alpha(alpha)
            surf.blit(ta,(rect.x+rect.width//2-tl.get_width()//2,
                          rect.y+rect.height//2-tl.get_height()//2))

        btn(new_r, "New Game",True,     new_r.collidepoint(mx,my)  if alpha>=200 else False)
        btn(cont_r,"Continue",has_saves,cont_r.collidepoint(mx,my) if (has_saves and alpha>=200) else False)
        if not has_saves:
            fh=pygame.font.SysFont("monospace",11)
            ht=fh.render("(no saves found)",True,(80,80,100))
            hs=pygame.Surface(ht.get_size(),pygame.SRCALPHA)
            hs.blit(ht,(0,0)); hs.set_alpha(alpha)
            surf.blit(hs,(cont_r.x+cont_r.width//2-ht.get_width()//2,cont_r.bottom+6))
