"""
Realm of Shadows — Intro sequence

Phase 1  HIRES  — Original high-res Bad Bat Enterprises logo on black, 3s hold
Phase 2  RETRO  — Cross-fades to chunky pixel art version + "Presents" underneath
Phase 3  LOAD   — Atmospheric loading screen; music starts as soon as first
                  track is ready; progress bar shows each item by name
Phase 4  TITLE  — Game title: dungeon art centred, title text clearly above it,
                  tagline and credit below, no overlap
Phase 5  MENU   — New Game / Continue click buttons fade in
"""

import pygame, math, random, os
import numpy as np

# ── renderer constants ──────────────────────────────────────────────────────
try:
    from ui.renderer import SCREEN_W, SCREEN_H, draw_text
except ImportError:
    SCREEN_W, SCREEN_H = 1440, 900
    def draw_text(surf, text, x, y, color, size, bold=False):
        f = pygame.font.SysFont("monospace", size, bold=bold)
        surf.blit(f.render(text, True, color), (x, y))

BLACK  = (0, 0, 0)
BG     = (12, 10, 24)

_LOGO  = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                      "assets", "bad_bat_logo.png")

# ── timing (ms) ─────────────────────────────────────────────────────────────
T_HIRES_FADE_IN   =  800   # high-res logo fades in
T_HIRES_HOLD      = 2800   # high-res logo holds fully visible
T_CROSS_FADE      = 1000   # cross-fade hires → retro
T_RETRO_HOLD      = 1200   # retro + "Presents" holds
T_RETRO_OUT       =  700   # retro fades out

T_LOAD_FADE_IN    =  500
T_LOAD_MIN_HOLD   = 2500   # min time on loading screen
T_LOAD_FADE_OUT   =  700

T_TITLE_FADE_IN   =  600
T_TITLE_MIN_HOLD  = 2500
T_MENU_APPEAR     =  600

PIXEL_BLOCK = 5


# ── logo helpers ─────────────────────────────────────────────────────────────

def _load_hires():
    try:
        return pygame.image.load(_LOGO).convert_alpha()
    except Exception:
        return None


def _make_retro(orig, block=PIXEL_BLOCK):
    """Max-pool → neon green SRCALPHA surface."""
    w, h = orig.get_size()
    tw, th = w // block, h // block
    arr   = pygame.surfarray.array3d(orig).transpose(1, 0, 2).astype(np.float32)
    G, R, B = arr[:,:,1], arr[:,:,0], arr[:,:,2]
    Gp = G[:th*block,:tw*block].reshape(th,block,tw,block).max(axis=(1,3))
    Rp = R[:th*block,:tw*block].reshape(th,block,tw,block).max(axis=(1,3))
    Bp = B[:th*block,:tw*block].reshape(th,block,tw,block).max(axis=(1,3))
    logo = (Gp > 5) & (Gp >= Rp) & (Gp >= Bp)
    neon = np.clip(Gp * 4.0, 60, 255).astype(np.uint8)
    res  = pygame.Surface((tw, th), pygame.SRCALPHA); res.fill((0,0,0,0))
    rv   = pygame.surfarray.pixels3d(res)
    av   = pygame.surfarray.pixels_alpha(res)
    lT   = logo.T; nT = neon.T
    rv[:,:,0] = 0; rv[:,:,1] = np.where(lT, nT, 0); rv[:,:,2] = 0
    av[:,:] = np.where(lT, 255, 0).astype(np.uint8)
    del rv, av
    return pygame.transform.scale(res, (tw*block, th*block))


def _retro_text(surf, text, x, y, size, block=PIXEL_BLOCK):
    try:
        f  = pygame.font.SysFont("monospace", size, bold=True)
        t  = f.render(text, False, (0, 255, 0))
        tw, th = t.get_size()
        chunky = pygame.transform.scale(
                     pygame.transform.scale(t, (max(1,tw//block), max(1,th//block))),
                     (tw, th))
        chunky.set_colorkey((0,0,0))
        surf.blit(chunky, (x, y))
    except Exception:
        pass


def _scanlines(surf, a=28):
    sl = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    for y in range(0, SCREEN_H, 2):
        pygame.draw.line(sl, (0,0,0,a), (0,y), (SCREEN_W,y))
    surf.blit(sl, (0,0))


def _scale_logo(surf, max_w, max_h):
    """Scale a surface to fit within max_w × max_h, preserving aspect ratio."""
    w, h = surf.get_size()
    scale = min(max_w / w, max_h / h, 1.0)
    nw, nh = int(w*scale), int(h*scale)
    return pygame.transform.smoothscale(surf, (nw, nh)), nw, nh


def _blit_alpha(dest, src, pos, alpha):
    """Blit src onto dest with an extra global alpha (works for SRCALPHA surfaces)."""
    if alpha <= 0:
        return
    if alpha >= 255:
        dest.blit(src, pos)
        return
    tmp = src.copy()
    # Multiply per-pixel alpha
    av = pygame.surfarray.pixels_alpha(tmp)
    av[:] = (av.astype(np.float32) * alpha / 255).astype(np.uint8)
    del av
    dest.blit(tmp, pos)


# ── dungeon art ──────────────────────────────────────────────────────────────

def _dungeon_art(surf, t, art_rect):
    """
    First-person dungeon corridor drawn with pure pygame geometry.
    Inspired by Wizardry / Ultima — 5-depth perspective walls, glowing
    doorway at the end, two animated torches, shadowy figure.
    """
    cx = art_rect.centerx
    ay = art_rect.top
    aw = art_rect.width
    ah = art_rect.height

    pygame.draw.rect(surf, (4, 3, 8), art_rect)

    # 5 depth layers, back to front
    for depth in [5, 4, 3, 2, 1]:
        shrink = 1.0 / (depth + 1)
        w2 = int(aw * shrink * 0.9)
        h2 = int(ah * shrink * 0.85)
        x2 = cx - w2 // 2
        y2 = ay + (ah - h2) // 2
        r  = pygame.Rect(x2, y2, w2, h2)
        sh = int(30 + depth * 18)
        wc = (sh, sh//2, sh//3)
        pygame.draw.rect(surf, wc, r)
        fh = r.height // 3
        pygame.draw.rect(surf, (sh+10, sh//3, sh//4),
                         pygame.Rect(r.x, r.bottom-fh, r.width, fh))
        pygame.draw.rect(surf, (sh//2, sh//4, sh//5),
                         pygame.Rect(r.x, r.y, r.width, fh))
        pygame.draw.rect(surf, (sh+20, sh//2+10, sh//3+8), r, 1)

    # Glowing doorway
    ga  = int(80 + 40*math.sin(t*1.2))
    dw, dh = 48, 72
    dx  = cx - dw//2
    dy  = ay + ah//2 - dh//2
    glow = pygame.Surface((dw+20, dh+20), pygame.SRCALPHA)
    glow.fill((40, 0, 80, ga)); surf.blit(glow, (dx-10, dy-10))
    pygame.draw.rect(surf, (8, 0, 20), (dx, dy, dw, dh))
    pygame.draw.rect(surf, (120, 60, 180), (dx, dy, dw, dh), 2)

    # Torches
    tf = 0.7 + 0.3*math.sin(t*8.3)
    for tx, ty in [(cx-180, ay+ah//2-20), (cx+140, ay+ah//2-20)]:
        pygame.draw.rect(surf, (100,60,30), (tx-3, ty, 6, 20))
        fh2 = int(18*tf)
        pygame.draw.ellipse(surf,
            (int(255*tf), int(140*tf), 20), (tx-5, ty-fh2, 10, fh2+4))
        hl = pygame.Surface((60,60), pygame.SRCALPHA)
        pygame.draw.circle(hl, (200,100,20,int(35*tf)), (30,30), 28)
        surf.blit(hl, (tx-30, ty-30))

    # Shadowy figure
    fa = int(60 + 30*math.sin(t*.6))
    fs = pygame.Surface((20,40), pygame.SRCALPHA); fs.fill((30,0,50,fa))
    surf.blit(fs, (cx-10, dy+14))

    # Border
    pygame.draw.rect(surf, (60,30,100), art_rect, 3)
    pygame.draw.rect(surf, (30,15,50), art_rect.inflate(6,6), 2)


# ════════════════════════════════════════════════════════════════════════════
class IntroScreen:
    """
    Manages all intro phases. Caller updates every frame, handles clicks,
    reads .done and .action when finished.
    """
    def __init__(self):
        self.phase  = 'hires'   # hires → retro → load → title → menu
        self.t      = 0          # ms elapsed in current phase
        self.done   = False
        self.action = None

        # Load logo surfaces
        orig = _load_hires()
        self._hires  = orig
        self._retro  = _make_retro(orig) if orig else None

        # Phase timing (all in ms)
        self._hires_total = T_HIRES_FADE_IN + T_HIRES_HOLD
        self._cross_total = T_CROSS_FADE + T_RETRO_HOLD + T_RETRO_OUT
        self._load_phase_start = self._hires_total + self._cross_total

        # Batch state
        self._b1_done    = False
        self._b2_done    = False
        self._b2_pct     = 0.0
        self._b2_label   = "Preparing…"
        self._music_on   = False

        # Title/menu
        self._title_t    = 0.0
        self._menu_alpha = 0
        self._new_rect   = None
        self._cont_rect  = None

        # Starfield
        rng = random.Random(77)
        self._stars = [(rng.randint(0,SCREEN_W), rng.randint(0,SCREEN_H),
                        rng.randint(1,2), rng.uniform(0.3,1.2), rng.random()*6.28)
                       for _ in range(120)]

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
            load_t = self.t
            if load_t >= T_LOAD_MIN_HOLD + T_LOAD_FADE_OUT and self._b2_done:
                self._go('title')

        elif self.phase == 'title':
            self._title_t += dt_ms / 1000.0
            if self._title_t * 1000 > T_TITLE_MIN_HOLD:
                self._menu_alpha = min(255,
                    self._menu_alpha + int(dt_ms * 255 / T_MENU_APPEAR))
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
        if   self.phase == 'hires':  self._draw_hires(surf)
        elif self.phase == 'retro':  self._draw_retro(surf)
        elif self.phase == 'load':   self._draw_load(surf)
        elif self.phase in ('title','menu'): self._draw_title(surf, mx, my)
        _scanlines(surf)

    # ── internal ─────────────────────────────────────────────────────────────

    def _go(self, phase):
        self.phase = phase
        self.t = 0

    def _step_batches(self):
        try:
            from core import sound as sfx
            if not sfx._enabled:
                self._b1_done = self._b2_done = True
                return
            if not self._b1_done:
                sfx.step_batch1()
                self._b1_done = True
            if not self._b2_done:
                done, idx, total, name = sfx.step_batch2()
                self._b2_pct   = idx / max(1, total)
                self._b2_label = name
                if done:
                    self._b2_done = True
                    self._b2_pct  = 1.0
                # Start music as soon as the first track (town_briarhollow) is ready
                if not self._music_on and sfx._sounds.get("town_briarhollow"):
                    self._music_on = True
                    try:
                        sfx.stop_music(); sfx.stop_ambient()
                        sfx.play_music("town_briarhollow")
                    except Exception:
                        pass
        except Exception:
            self._b1_done = self._b2_done = True

    # ── PHASE 1: high-res logo ────────────────────────────────────────────────

    def _draw_hires(self, surf):
        if not self._hires:
            return
        t = self.t
        if t < T_HIRES_FADE_IN:
            alpha = int(255 * t / T_HIRES_FADE_IN)
        else:
            alpha = 255

        max_w = int(SCREEN_W * 0.72)
        max_h = int(SCREEN_H * 0.55)
        logo_s, nw, nh = _scale_logo(self._hires, max_w, max_h)

        lx = SCREEN_W//2 - nw//2
        ly = SCREEN_H//2 - nh//2 - 20

        _blit_alpha(surf, logo_s, (lx, ly), alpha)

    # ── PHASE 2: cross-fade to retro + "Presents" ────────────────────────────

    def _draw_retro(self, surf):
        t = self.t

        # Cross-fade: hires fades out while retro fades in over T_CROSS_FADE ms
        if t < T_CROSS_FADE:
            frac       = t / T_CROSS_FADE
            hires_a    = int(255 * (1 - frac))
            retro_a    = int(255 * frac)
            presents_a = 0
        elif t < T_CROSS_FADE + T_RETRO_HOLD:
            hires_a    = 0
            retro_a    = 255
            presents_a = min(255, int(255 * (t - T_CROSS_FADE) / 400))
        else:
            fade_frac  = (t - T_CROSS_FADE - T_RETRO_HOLD) / T_RETRO_OUT
            hires_a    = 0
            retro_a    = max(0, int(255 * (1 - fade_frac)))
            presents_a = retro_a

        max_w = int(SCREEN_W * 0.72)
        max_h = int(SCREEN_H * 0.55)
        ly_base = SCREEN_H//2 - int(max_h//2) - 20

        # High-res layer
        if hires_a > 0 and self._hires:
            ls, nw, nh = _scale_logo(self._hires, max_w, max_h)
            _blit_alpha(surf, ls, (SCREEN_W//2-nw//2, ly_base), hires_a)

        # Retro layer
        if retro_a > 0 and self._retro:
            # Green phosphor glow backdrop
            gw, gh = int(max_w*1.05), int(max_h*0.9)
            gx = SCREEN_W//2 - gw//2
            gy = ly_base - 10
            gl = pygame.Surface((gw, gh), pygame.SRCALPHA)
            for r in range(0, min(gw,gh)//2, 4):
                frac2 = 1 - r/(min(gw,gh)//2)
                a = int(retro_a * 0.15 * frac2**2)
                if a > 0:
                    pygame.draw.ellipse(gl, (0,40,0,a),
                                        (gw//2-r*2, gh//2-r, r*4, r*2))
            surf.blit(gl, (gx, gy))

            # Retro logo
            rs, nw, nh = _scale_logo(self._retro, max_w, max_h)
            lx = SCREEN_W//2 - nw//2
            ly = ly_base
            _blit_alpha(surf, rs, (lx, ly), retro_a)

            # BAD / BAT text (black in source → draw fresh in retro green)
            if retro_a >= 30:
                ts  = max(18, int(nh * 0.22))
                ty  = ly + int(nh * 0.18)
                bad = pygame.Surface((int(nw*0.34), ts+8), pygame.SRCALPHA)
                bat = pygame.Surface((int(nw*0.34), ts+8), pygame.SRCALPHA)
                _retro_text(bad, "BAD", 0, 0, ts)
                _retro_text(bat, "BAT", 0, 0, ts)
                bad.set_alpha(retro_a); bat.set_alpha(retro_a)
                surf.blit(bad, (lx + int(nw*0.01), ty))
                surf.blit(bat, (lx + int(nw*0.65), ty))

        # "P R E S E N T S"
        if presents_a > 0 and self._retro:
            rs2, nw2, nh2 = _scale_logo(self._retro, max_w, max_h)
            pres_y = ly_base + nh2 + 18
            fp = pygame.font.SysFont("monospace", 20)
            pt = fp.render("P R E S E N T S", True, (0,200,0))
            ps = pygame.Surface(pt.get_size(), pygame.SRCALPHA)
            ps.blit(pt,(0,0)); ps.set_alpha(presents_a)
            surf.blit(ps, (SCREEN_W//2 - pt.get_width()//2, pres_y))

    # ── PHASE 3: loading screen ───────────────────────────────────────────────

    def _draw_load(self, surf):
        t_s = self.t

        # Fade-in / hold / fade-out
        if t_s < T_LOAD_FADE_IN:
            card_a = int(255 * t_s / T_LOAD_FADE_IN)
        elif self._b2_done and t_s >= T_LOAD_MIN_HOLD:
            elapsed = t_s - T_LOAD_MIN_HOLD
            card_a  = max(0, int(255 * (1 - elapsed / T_LOAD_FADE_OUT)))
        else:
            card_a = 255

        if card_a <= 0:
            return

        t_sec = t_s / 1000.0

        # Subtle purple atmospheric background
        for y in range(0, SCREEN_H, 4):
            d = abs(y - SCREEN_H//2) / (SCREEN_H//2)
            a = int(card_a * 0.10 * (1 - d**1.5))
            if a > 0:
                sl = pygame.Surface((SCREEN_W, 4), pygame.SRCALPHA)
                sl.fill((20, 0, 40, a)); surf.blit(sl, (0,y))

        # Drifting particles
        rng = random.Random(int(t_sec * 0.5))
        for _ in range(25):
            px = rng.randint(0, SCREEN_W)
            py = int((rng.randint(0, SCREEN_H) + t_s * 0.018) % SCREEN_H)
            pa = int(card_a * 0.22 * rng.random())
            if pa > 0:
                ps = pygame.Surface((2,2), pygame.SRCALPHA)
                ps.fill((120,60,180,pa)); surf.blit(ps, (px,py))

        # Lore quote — two lines with stagger
        cy = SCREEN_H//2 - 55
        for i, line in enumerate([
            "The Fading does not announce itself.",
            "It simply…  arrives."
        ]):
            delay = i * 700
            la = min(card_a, max(0, int(card_a * min(1.0, (t_s-delay)/800))))
            if la <= 0: continue
            fq = pygame.font.SysFont("serif", 22, italic=True)
            tq = fq.render(line, True, (180,150,220))
            ts = pygame.Surface(tq.get_size(), pygame.SRCALPHA)
            ts.blit(tq,(0,0)); ts.set_alpha(la)
            surf.blit(ts, (SCREEN_W//2 - tq.get_width()//2, cy + i*42))

        # Decorative separator
        sep_a = min(card_a, max(0, int(card_a * min(1.0, (t_s-1300)/600))))
        if sep_a > 0:
            sep = pygame.Surface((280,1), pygame.SRCALPHA)
            sep.fill((100,60,160,sep_a)); surf.blit(sep,(SCREEN_W//2-140, cy+98))

        # Game name
        gn_a = min(card_a, max(0, int(card_a * min(1.0, (t_s-1900)/600))))
        if gn_a > 0:
            fg = pygame.font.SysFont("monospace", 14)
            tg = fg.render("REALM  OF  SHADOWS", True, (100,80,140))
            tgs = pygame.Surface(tg.get_size(), pygame.SRCALPHA)
            tgs.blit(tg,(0,0)); tgs.set_alpha(gn_a)
            surf.blit(tgs, (SCREEN_W//2 - tg.get_width()//2, cy+110))

        # Progress bar
        bar_a = min(card_a, max(0, int(card_a * min(1.0, (t_s-600)/500))))
        if bar_a > 0:
            bw, bh = 420, 6
            bx = SCREEN_W//2 - bw//2
            by = SCREEN_H - 72

            # Track
            tr = pygame.Surface((bw, bh), pygame.SRCALPHA)
            tr.fill((40,20,60,bar_a)); surf.blit(tr, (bx,by))

            # Fill
            fw = int(bw * self._b2_pct)
            if fw > 0:
                for bxi in range(fw):
                    frac = bxi / bw
                    gc   = int(bar_a * (0.3 + 0.7*frac))
                    rc   = int(bar_a * 0.08 * frac)
                    fil  = pygame.Surface((1, bh), pygame.SRCALPHA)
                    fil.fill((rc, gc*2//3, min(255,gc)))
                    surf.blit(fil, (bx+bxi, by))

            # Border
            brd = pygame.Surface((bw+2, bh+2), pygame.SRCALPHA)
            pygame.draw.rect(brd, (80,40,120,bar_a), (0,0,bw+2,bh+2), 1)
            surf.blit(brd, (bx-1, by-1))

            # Label
            fl = pygame.font.SysFont("monospace", 11)
            if self._b2_done:
                lt, lc = "Ready", (0,200,0)
            else:
                lt, lc = self._b2_label[:50], (100,80,130)
            tl  = fl.render(lt, True, lc)
            tls = pygame.Surface(tl.get_size(), pygame.SRCALPHA)
            tls.blit(tl,(0,0)); tls.set_alpha(bar_a)
            surf.blit(tls, (SCREEN_W//2 - tl.get_width()//2, by+10))

    # ── PHASE 4/5: title + menu ───────────────────────────────────────────────

    def _draw_title(self, surf, mx, my):
        t = self._title_t

        # Starfield
        for sx,sy,sr,sp,ph in self._stars:
            a = int(55+45*math.sin(t*sp+ph))
            s = pygame.Surface((sr*2,sr*2), pygame.SRCALPHA)
            pygame.draw.circle(s,(200,180,255,a),(sr,sr),sr)
            surf.blit(s,(sx-sr,sy-sr))

        # Tendrils
        rng2 = random.Random(int(t*1.5))
        tend = pygame.Surface((SCREEN_W,SCREEN_H), pygame.SRCALPHA)
        for _ in range(8):
            ox=rng2.randint(0,SCREEN_W); ln=rng2.randint(60,160)
            px,py=float(ox),0.0
            for step in range(ln):
                nx=px+rng2.uniform(-5,5); ny=py+1
                a=max(0,int(60*(1-step/ln)))
                pygame.draw.line(tend,(60,0,100,a),(int(px),int(py)),(int(nx),int(ny)),2)
                px,py=nx,ny
        surf.blit(tend,(0,0))

        # ── Title text — top of screen ────────────────────────────────────────
        # Positioned clearly ABOVE the art, with enough breathing room
        pulse = abs(math.sin(t*1.05))
        rc = (int(210+45*pulse), int(180+30*pulse), int(20*pulse))
        sc = (int(140+60*pulse), int(110+50*pulse), int(180+40*pulse))

        # Soft glow behind title
        gw_surf = pygame.Surface((400, 110), pygame.SRCALPHA)
        gw_surf.fill((80,20,140,int(35+25*pulse)))
        surf.blit(gw_surf, (SCREEN_W//2-200, 18))

        draw_text(surf, "REALM",   SCREEN_W//2-130, 22,  rc, 52, bold=True)
        draw_text(surf, "of",      SCREEN_W//2-20,  80,  (180,160,220), 22)
        draw_text(surf, "SHADOWS", SCREEN_W//2-170, 104, sc, 52, bold=True)

        # ── Dungeon art — clearly below title, well separated ─────────────────
        # Art starts at y=175, height=390 → ends at y=565
        ART_Y = 175
        ART_W = 600
        ART_H = 360
        art_rect = pygame.Rect(SCREEN_W//2 - ART_W//2, ART_Y, ART_W, ART_H)
        _dungeon_art(surf, t, art_rect)

        # ── Tagline — below art ───────────────────────────────────────────────
        draw_text(surf, "The Fading comes for all things.",
                  SCREEN_W//2-178, ART_Y+ART_H+12, (140,110,180), 15)

        # ── Company credit ────────────────────────────────────────────────────
        draw_text(surf, "A Bad Bat Enterprises Game",
                  SCREEN_W//2-148, SCREEN_H-34, (0,120,0), 13)

        # ── Menu buttons ─────────────────────────────────────────────────────
        if self._menu_alpha > 10:
            self._draw_menu(surf, mx, my, self._menu_alpha)

    def _draw_menu(self, surf, mx, my, alpha):
        from core.save_load import list_saves
        has_saves = bool(list_saves())

        # Position buttons just below tagline
        ART_BOTTOM = 175 + 360
        btn_y = ART_BOTTOM + 55
        new_r  = pygame.Rect(SCREEN_W//2-220, btn_y, 200, 52)
        cont_r = pygame.Rect(SCREEN_W//2+20,  btn_y, 200, 52)
        self._new_rect  = new_r
        self._cont_rect = cont_r if has_saves else None

        def btn(rect, label, enabled, hov):
            bs = pygame.Surface((rect.width,rect.height), pygame.SRCALPHA)
            if hov and enabled:
                bg = (60,110,200,int(alpha*.9))
            elif enabled:
                bg = (40,80,140,int(alpha*.85))
            else:
                bg = (40,40,60,int(alpha*.5))
            pygame.draw.rect(bs,bg,(0,0,rect.width,rect.height),border_radius=6)
            bc=(100,160,255,alpha) if (enabled and hov) else (70,100,180,alpha)
            pygame.draw.rect(bs,bc,(0,0,rect.width,rect.height),2,border_radius=6)
            surf.blit(bs, rect.topleft)
            tc=(255,255,255) if (hov and enabled) else ((220,220,255) if enabled else (80,80,100))
            f=pygame.font.SysFont("monospace",17,bold=True)
            tl=f.render(label,True,tc)
            ta=pygame.Surface(tl.get_size(),pygame.SRCALPHA)
            ta.blit(tl,(0,0)); ta.set_alpha(alpha)
            surf.blit(ta,(rect.x+rect.width//2-tl.get_width()//2,
                          rect.y+rect.height//2-tl.get_height()//2))

        btn(new_r,  "New Game", True,      new_r.collidepoint(mx,my)  if alpha>=200 else False)
        btn(cont_r, "Continue", has_saves, cont_r.collidepoint(mx,my) if (has_saves and alpha>=200) else False)
        if not has_saves:
            fh=pygame.font.SysFont("monospace",11)
            ht=fh.render("(no saves found)",True,(80,80,100))
            hs=pygame.Surface(ht.get_size(),pygame.SRCALPHA)
            hs.blit(ht,(0,0)); hs.set_alpha(alpha)
            surf.blit(hs,(cont_r.x+cont_r.width//2-ht.get_width()//2,cont_r.bottom+6))
