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
VP_W, VP_H   = 940, 820
HUD_H        = 90

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

def _gen_texture(wall_light, wall_dark, is_door=False):
    surf = pygame.Surface((TEX_W, TEX_H))
    rng  = random.Random(hash((wall_light, is_door)))

    if is_door:
        surf.fill(tuple(int(v * 0.85) for v in wall_light))
        for py in range(0, TEX_H, 12):
            pygame.draw.line(surf, tuple(int(v*0.55) for v in wall_light), (0,py),(TEX_W,py))
        for px in range(0, TEX_W, 8):
            c = tuple(int(v*(0.7+rng.random()*0.25)) for v in wall_light)
            pygame.draw.line(surf, c, (px,0),(px,TEX_H))
        return surf

    brick_h = 8
    brick_w = 16
    mortar  = tuple(int(v*0.55) for v in wall_dark)
    surf.fill(mortar)
    for row in range(TEX_H // brick_h + 1):
        oy = row * brick_h
        offset = (brick_w//2) if (row%2) else 0
        for col in range(-1, TEX_W // brick_w + 2):
            ox = col * brick_w + offset
            tone = 0.75 + rng.random()*0.35
            base = tuple(min(255,int(v*tone)) for v in wall_light)
            r = pygame.Rect(ox+1, oy+1, brick_w-2, brick_h-2)
            r.clamp_ip(pygame.Rect(0,0,TEX_W,TEX_H))
            pygame.draw.rect(surf, base, r)
    for _ in range(80):
        nx = rng.randint(0,TEX_W-1)
        ny = rng.randint(0,TEX_H-1)
        ex = surf.get_at((nx,ny))
        dim = tuple(max(0,v-rng.randint(0,30)) for v in ex[:3])
        surf.set_at((nx,ny), dim)
    return surf


# ═══════════════════════════════════════════════════════════════
#  SPRITE DATA
# ═══════════════════════════════════════════════════════════════

SPRITE_COLORS = {
    DT_TREASURE:     (255, 220, 50),
    DT_STAIRS_DOWN:  (100, 220, 255),
    DT_STAIRS_UP:    (80,  200, 255),
    DT_ENTRANCE:     (100, 230, 120),
    DT_TRAP:         (230, 50,  50),
    DT_INTERACTABLE: (80,  200, 255),
    "enemy":         (200, 40,  40),
    "boss":          (255, 20,  100),
    "journal":       (220, 200, 130),
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

        # Pre-generate textures
        self._tex_wall  = _gen_texture(self.wall_light, self.wall_dark)
        self._tex_door  = _gen_texture(self.wall_light, self.wall_dark, is_door=True)

        # Pre-bake column arrays from textures for speed
        self._wall_cols = self._bake_tex_cols(self._tex_wall)
        self._door_cols = self._bake_tex_cols(self._tex_door)

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

        self.fading_intensity = 0.0
        self._update_fading()

        self.t     = 0.0
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
        self.cx = -self.dy * 0.825
        self.cy =  self.dx * 0.825

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
        return tt == DT_WALL

    # ─────────────────────────────────────────────────────────

    def _cast_ray(self, ray_dx, ray_dy):
        """DDA ray → (dist, wall_x_frac, is_ns, is_door)."""
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

        fl   = self.dungeon.get_current_floor_data()
        fw   = fl["width"]
        fh   = fl["height"]
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
                return 20.0, 0.0, ns, False
            tile = tiles[map_y][map_x]
            tt   = tile["type"]
            is_s = tt == DT_SECRET_DOOR and not tile.get("secret_found")
            is_w = tt == DT_WALL or is_s
            is_d = tt == DT_DOOR
            if is_w or is_d:
                if not ns:
                    dist = (map_x - self.px + (1 - step_x)/2) / ray_dx
                else:
                    dist = (map_y - self.py + (1 - step_y)/2) / ray_dy
                if not ns:
                    wx = self.py + dist * ray_dy
                else:
                    wx = self.px + dist * ray_dx
                wx -= math.floor(wx)
                return max(0.01, dist), wx, ns, is_d
        return 20.0, 0.0, False, False

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

        # ── Ceiling / floor scanlines ──
        for sy in range(VH):
            if sy == HH:
                continue
            row_dist = PROJ_DIST / max(1, abs(sy - HH))
            fog_t    = min(1.0, row_dist * 0.35 / FOG)
            if sy < HH:
                c = tuple(int(self.ceil_c[i]*(1-fog_t) + self.fog_c[i]*fog_t) for i in range(3))
            else:
                c = tuple(int(self.floor_c[i]*(1-fog_t*0.85) + self.fog_c[i]*fog_t*0.85) for i in range(3))
            pygame.draw.line(view, c, (0, sy), (VW-1, sy))

        # ── Wall columns ──
        wall_cols = self._wall_cols
        door_cols = self._door_cols

        for col in range(VW):
            cam_x    = (2.0 * col / VW) - 1.0
            ray_dx   = self.dx + self.cx * cam_x
            ray_dy   = self.dy + self.cy * cam_x
            dist, wx, ns, is_door = self._cast_ray(ray_dx, ray_dy)
            zbuf[col] = dist

            wall_h = min(VH, int(PROJ_DIST / max(0.01, dist)))
            top    = HH - wall_h // 2
            # bot  = HH + wall_h // 2

            tex_x = int(wx * TEX_W) % TEX_W
            cols_src = door_cols[tex_x] if is_door else wall_cols[tex_x]

            # Lighting
            fog_t = min(1.0, dist / FOG)
            ns_f  = 0.70 if ns else 1.0
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
                if tt in SPRITE_COLORS:
                    icon_key = tt
                enc = tile.get("encounter")
                if enc and not enc.get("cleared"):
                    icon_key = "boss" if enc.get("is_boss") else "enemy"
                if tile.get("has_journal") and not tile.get("journal_read"):
                    icon_key = "journal"
                if icon_key is None:
                    continue
                sx = tx + 0.5 - self.px
                sy = ty + 0.5 - self.py
                d  = math.sqrt(sx*sx + sy*sy)
                if d < 0.3 or d > TORCH_DIST + 1:
                    continue
                sprites.append((d, sx, sy, icon_key))

        sprites.sort(key=lambda s: -s[0])

        font = pygame.font.SysFont("segoeuisymbol,symbola,unifont,dejavusans", 32)
        for dist, sx, sy, icon_key in sprites:
            inv = 1.0 / (self.cx * self.dy - self.dx * self.cy)
            tx_ = inv * (self.dy * sx - self.dx * sy)
            ty_ = inv * (-self.cy * sx + self.cx * sy)
            if ty_ <= 0.1:
                continue
            screen_x = int((VP_W/2) * (1 + tx_ / ty_))
            sp_h = max(1, abs(int(PROJ_DIST / ty_)))
            sp_w = sp_h
            start_y = max(0, VP_H//2 - sp_h//2)
            end_y   = min(VP_H, VP_H//2 + sp_h//2)
            start_x = max(0, screen_x - sp_w//2)
            end_x   = min(VP_W, screen_x + sp_w//2)
            if start_x >= end_x:
                continue

            color = SPRITE_COLORS.get(icon_key, (200, 200, 200))
            fog_t  = min(1.0, dist / TORCH_DIST)
            alpha  = int(255 * (1.0 - fog_t * 0.88))
            color_a = (*color, alpha)

            # Draw as a glowing circle with label
            cx = (start_x + end_x) // 2
            cy = (start_y + end_y) // 2
            r  = max(4, sp_h // 4)
            # Check z-buffer at center
            if 0 <= cx < VP_W and ty_ < zbuf[cx]:
                glow_surf = pygame.Surface((r*4, r*4), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (*color, alpha//3), (r*2, r*2), r*2)
                pygame.draw.circle(glow_surf, (*color, alpha),    (r*2, r*2), max(2,r//2))
                view.blit(glow_surf, (cx - r*2, cy - r*2))

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
                elif tt in (DT_STAIRS_DOWN, DT_STAIRS_UP):
                    c = (80,200,255,255)
                elif tt == DT_TREASURE:
                    c = (255,215,40,255)
                elif tt == DT_TRAP and tile.get("event",{}).get("detected"):
                    c = (220,50,50,255)
                else:
                    c = (88,78,62,200)
                sx = (tx-x0)*ts
                sy = (ty-y0)*ts
                pygame.draw.rect(bg, c, (sx,sy,ts-1,ts-1))

        # Party dot + facing arrow
        ppx = (px_i-x0)*ts + ts//2
        ppy = (py_i-y0)*ts + ts//2
        ax  = ppx + int(math.cos(self.angle)*ts*1.2)
        ay  = ppy + int(math.sin(self.angle)*ts*1.2)
        pygame.draw.line(bg, (255,255,80,255), (ppx,ppy), (ax,ay), 2)
        pygame.draw.circle(bg, (255,255,80,255), (ppx,ppy), ts//2)
        pygame.draw.rect(bg, (100,90,72,200), (0,0,cols*ts,rows*ts), 1)

        surface.blit(bg, (MM_X, MM_Y))
        font = pygame.font.SysFont("courier,monospace", 11)
        lbl  = font.render(f"Floor {self.dungeon.current_floor}", True, (170,160,130))
        surface.blit(lbl, (MM_X+2, MM_Y+rows*ts+2))

    # ─────────────────────────────────────────────────────────
    #  HUD
    # ─────────────────────────────────────────────────────────

    def _draw_hud(self, surface, mx, my):
        by = SCREEN_H - HUD_H
        pygame.draw.rect(surface, (14,11,8), (0, by, SCREEN_W, HUD_H))
        pygame.draw.line(surface, GOLD, (0, by), (SCREEN_W, by), 2)

        fb = pygame.font.SysFont("courier,consolas,monospace", 13, bold=True)
        fs = pygame.font.SysFont("courier,consolas,monospace", 11)

        party = self.dungeon.party
        if party:
            col_w = min(195, VP_W // max(1, len(party)))
            for i, ch in enumerate(party):
                cx_h = 8 + i*col_w
                cy_h = by + 5
                surface.blit(fb.render(ch.name[:12], True, GOLD), (cx_h, cy_h))
                cy_h += 16
                # Get resources
                try:
                    from core.classes import get_all_resources
                    max_res = get_all_resources(ch.class_name, ch.stats, ch.level)
                except Exception:
                    max_res = {}
                cur_hp  = ch.resources.get("HP", 0)
                max_hp  = max(1, max_res.get("HP", cur_hp) or cur_hp)
                hw = max(0, int((cur_hp/max_hp)*(col_w-12)))
                pygame.draw.rect(surface, (55,12,12), (cx_h, cy_h, col_w-12, 7))
                pygame.draw.rect(surface, (185,38,38), (cx_h, cy_h, hw, 7))
                surface.blit(fs.render(f"{cur_hp}/{max_hp}", True, (190,150,145)), (cx_h, cy_h+8))
                # Second resource (MP/Ki/etc.)
                res_keys = [k for k in ch.resources if k != "HP"]
                if res_keys:
                    cy_h += 20
                    rk     = res_keys[0]
                    cur_r  = ch.resources.get(rk, 0)
                    max_r  = max(1, max_res.get(rk, cur_r) or cur_r)
                    mw     = max(0, int((cur_r/max_r)*(col_w-12)))
                    pygame.draw.rect(surface, (12,12,55), (cx_h, cy_h, col_w-12, 7))
                    pygame.draw.rect(surface, (45,75,205), (cx_h, cy_h, mw, 7))
                    surface.blit(fs.render(f"{rk} {cur_r}/{max_r}", True, (130,140,215)), (cx_h, cy_h+8))

        # Buttons
        bx = 8
        bdata = [
            ("C Camp",   pygame.Rect(bx,           by+HUD_H-34, 108, 26)),
            ("M Menu",   pygame.Rect(bx+118,        by+HUD_H-34, 108, 26)),
            ("T Disarm", pygame.Rect(bx+236,        by+HUD_H-34, 118, 26)),
        ]
        for lbl, r in bdata:
            hov = r.collidepoint(mx,my)
            pygame.draw.rect(surface, (40,30,18) if not hov else (62,46,24), r, border_radius=3)
            pygame.draw.rect(surface, GOLD if hov else (75,60,38), r, 1, border_radius=3)
            surface.blit(fb.render(lbl, True, GOLD if hov else CREAM), (r.x+6, r.y+5))

        info = fb.render(
            f"{self.dungeon.dungeon_id.replace('_',' ').title()}  ·  Floor {self.dungeon.current_floor}/{self.dungeon.total_floors}",
            True, (150,138,110))
        surface.blit(info, (SCREEN_W - info.get_width() - 10, by + HUD_H - 28))

        ctrl = fs.render("WASD Move  QE/←→ Turn  ENTER Interact  C Camp  T Disarm", True, (72,64,50))
        surface.blit(ctrl, (VP_X+4, by+3))

    # ─────────────────────────────────────────────────────────
    #  DIALOGS
    # ─────────────────────────────────────────────────────────

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
            ts = font.render(msg, True, col)
            ts.set_alpha(min(255, int(timer/300*255)))
            surface.blit(ts, (VP_X + VP_W//2 - ts.get_width()//2, base_y - i*22))

    # ─────────────────────────────────────────────────────────
    #  INPUT
    # ─────────────────────────────────────────────────────────

    def _process_held_keys(self, dt):
        if self.show_camp_confirm or self.show_stairs_confirm:
            return
        keys = self._keys
        if pygame.K_LEFT in keys or pygame.K_q in keys:
            self.angle -= ROT_SPEED * dt
            self._recalc_camera()
        if pygame.K_RIGHT in keys or pygame.K_e in keys:
            self.angle += ROT_SPEED * dt
            self._recalc_camera()
        md = MOVE_SPEED * dt
        nx, ny = self.px, self.py
        moved = False
        if pygame.K_UP in keys or pygame.K_w in keys:
            nx += self.dx*md; ny += self.dy*md; moved = True
        if pygame.K_DOWN in keys or pygame.K_s in keys:
            nx -= self.dx*md; ny -= self.dy*md; moved = True
        if pygame.K_a in keys:
            nx += self.dy*md*0.7; ny -= self.dx*md*0.7; moved = True
        if pygame.K_d in keys:
            nx -= self.dy*md*0.7; ny += self.dx*md*0.7; moved = True
        if moved:
            if not self._is_solid(int(nx), int(self.py)):
                self.px = nx
            if not self._is_solid(int(self.px), int(ny)):
                self.py = ny
            self._sync_grid_pos()

    def handle_key(self, key):
        movement_keys = (
            pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,
            pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d,
            pygame.K_q, pygame.K_e,
        )
        if key in movement_keys:
            self._keys.add(key)
            return None

        if self.show_camp_confirm or self.show_stairs_confirm:
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

        by = SCREEN_H - HUD_H
        if pygame.Rect(8, by+HUD_H-34, 108, 26).collidepoint(mx,my):
            self.show_camp_confirm = True; return None
        if pygame.Rect(126, by+HUD_H-34, 108, 26).collidepoint(mx,my):
            return {"type":"menu"}
        if pygame.Rect(244, by+HUD_H-34, 118, 26).collidepoint(mx,my):
            return self._try_disarm()
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

