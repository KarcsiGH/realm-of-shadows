"""
Realm of Shadows — Dungeon UI (M7 Enhanced 3D Renderer)
Textured walls, torch lighting, enemy sprites, ambient particles,
vignette, journal/object glows, enhanced object rendering.
"""
import pygame, math, time, random
from ui.renderer import *
from data.dungeon import (
    DungeonState, PASSABLE_TILES, DT_WALL, DT_FLOOR, DT_CORRIDOR,
    DT_DOOR, DT_STAIRS_DOWN, DT_STAIRS_UP, DT_TREASURE, DT_TRAP, DT_ENTRANCE,
)
from ui.dungeon_fx import gen_wall_texture, ParticleSystem, draw_vignette

VP_X, VP_Y, VP_W, VP_H = 40, 50, 720, 580
VP_CX, VP_CY = VP_X + VP_W // 2, VP_Y + VP_H // 2
VIEW_DEPTH = 5
DIR_DX = [0, 1, 0, -1]
DIR_DY = [-1, 0, 1, 0]
DIR_NAMES = ["North", "East", "South", "West"]

THEMES = {
    "cave":  {"wall":(65,55,45),"wd":(40,34,28),"wl":(80,68,55),"wa":(55,48,38),
              "fl":(50,44,36),"cl":(35,30,25),"fog":(12,10,8),"torch":(220,160,60)},
    "mine":  {"wall":(72,62,48),"wd":(48,40,30),"wl":(88,76,58),"wa":(62,52,40),
              "fl":(55,48,38),"cl":(38,32,26),"fog":(10,8,6),"torch":(240,180,70)},
    "crypt": {"wall":(52,55,68),"wd":(32,35,48),"wl":(65,68,82),"wa":(42,45,58),
              "fl":(40,42,52),"cl":(25,28,38),"fog":(8,8,14),"torch":(140,160,220)},
    "ruins": {"wall":(75,65,50),"wd":(50,42,32),"wl":(90,78,60),"wa":(60,52,42),
              "fl":(58,50,40),"cl":(40,34,28),"fog":(10,8,6),"torch":(230,170,60)},
}
DOOR_COL, DOOR_DARK, DOOR_FRAME = (130,90,40), (90,60,25), (70,45,18)
SD_COL, SU_COL = (180,160,60), (80,180,220)
TREAS_COL, TREAS_OPEN = (255,215,0), (120,100,50)
ENTRANCE_COL, TRAP_COL = (100,200,100), (200,60,60)
JOURNAL_COL = (200, 180, 120)


class DungeonUI:
    def __init__(self, ds):
        self.dungeon = ds
        self.theme_key = ds.theme
        self.th = THEMES.get(ds.theme, THEMES["cave"])
        self.facing = 0
        self.event_message = ""
        self.event_timer = 0
        self.event_color = CREAM
        self.event_queue = []
        self.show_camp_confirm = False
        self.show_stairs_confirm = False
        self.stairs_direction = None
        self.torch_time = 0.0
        self.torch_brightness = 1.0
        self.particles = ParticleSystem(VP_X, VP_Y, VP_W, VP_H)
        self.dust_timer = 0.0
        for sz in [128, 96, 64]:
            gen_wall_texture(self.th, sz, sz)

    def _dim(self, c, f):
        return tuple(max(0, min(255, int(v * f))) for v in c)

    def _sr(self, s):
        hw, hh = int(VP_W * s / 2), int(VP_H * s / 2)
        return VP_CX - hw, VP_CY - hh, VP_CX + hw, VP_CY + hh

    def _persp(self, d):
        return 1.0 / (d * 0.55 + 0.7)

    def _gtype(self, x, y):
        t = self.dungeon.get_tile(x, y)
        return t["type"] if t else None

    # ══════════════════════════════════════════════════════════
    #  MAIN DRAW
    # ══════════════════════════════════════════════════════════
    def draw(self, surface, mx, my, dt):
        dt_sec = dt / 1000.0
        self.event_timer = max(0, self.event_timer - dt)
        t = self.torch_time = self.torch_time + dt_sec
        self.torch_brightness = 0.82 + 0.18 * (
            0.5 * math.sin(t * 8.3) + 0.3 * math.sin(t * 5.7 + 1.2) + 0.2 * math.sin(t * 13.1))
        self.dust_timer += dt_sec
        if self.dust_timer > 0.4:
            self.dust_timer = 0; self.particles.emit_dust(1)
        self.particles.update(dt_sec)
        self.event_queue = [(m, c, tmr - dt) for m, c, tmr in self.event_queue if tmr - dt > 0]

        surface.fill(self.th["fog"])
        self._draw_3d(surface)
        self.particles.draw(surface)
        draw_vignette(surface, VP_X, VP_Y, VP_W, VP_H)
        self._draw_minimap(surface)
        self._draw_hud(surface, mx, my)
        if self.show_camp_confirm: self._draw_camp_dlg(surface, mx, my)
        if self.show_stairs_confirm: self._draw_stairs_dlg(surface, mx, my)
        if (self.event_message and self.event_timer > 0) or self.event_queue:
            self._draw_events(surface)

    def _draw_events(self, surface):
        lines = []
        if self.event_message and self.event_timer > 0:
            lines.append((self.event_message, self.event_color))
        for m, c, _ in self.event_queue:
            if (m, c) not in lines: lines.append((m, c))
        if not lines: return
        h = max(50, len(lines) * 24 + 16)
        r = pygame.Rect(VP_CX - 320, VP_CY - h // 2, 640, h)
        ov = pygame.Surface((r.w, r.h), pygame.SRCALPHA); ov.fill((10, 8, 20, 190))
        surface.blit(ov, r.topleft)
        pygame.draw.rect(surface, GOLD, r, 2, border_radius=5)
        for i, (msg, col) in enumerate(lines[:5]):
            draw_text(surface, msg, r.x + 18, r.y + 8 + i * 22, col, 14, max_width=r.w - 36)

    # ══════════════════════════════════════════════════════════
    #  3D VIEWPORT
    # ══════════════════════════════════════════════════════════
    def _draw_3d(self, surface):
        surface.set_clip(pygame.Rect(VP_X, VP_Y, VP_W, VP_H))
        tb = self.torch_brightness
        # Ceiling
        for i in range(14):
            f = i / 14.0; b = max(0.06, 0.55 - f * 0.45) * tb
            ch = max(1, VP_H // 28 + 1)
            surface.fill(self._dim(self.th["cl"], b), (VP_X, VP_CY - int(VP_H * 0.5 * (1 - f)), VP_W, ch))
        # Floor
        for i in range(14):
            f = i / 14.0; b = max(0.10, 0.80 - f * 0.60) * tb
            fh = max(1, VP_H // 28 + 1); fy = VP_CY + int(VP_H * 0.5 * f)
            surface.fill(self._dim(self.th["fl"], b), (VP_X, fy, VP_W, fh))
            if i % 3 == 0 and i > 0:
                pygame.draw.line(surface, self._dim(self.th["wd"], b * 0.5), (VP_X, fy), (VP_X + VP_W, fy), 1)

        fdx, fdy = DIR_DX[self.facing], DIR_DY[self.facing]
        rdx, rdy = DIR_DX[(self.facing + 1) % 4], DIR_DY[(self.facing + 1) % 4]
        px, py = self.dungeon.party_x, self.dungeon.party_y
        for depth in range(VIEW_DEPTH, 0, -1):
            self._render_slice(surface, px, py, fdx, fdy, rdx, rdy, depth)
        self._draw_nearby(surface, px, py, fdx, fdy, rdx, rdy)
        self._draw_enemies(surface, px, py, fdx, fdy, rdx, rdy)
        surface.set_clip(None)
        pygame.draw.rect(surface, PANEL_BORDER, (VP_X, VP_Y, VP_W, VP_H), 2)
        # Torch glow
        gs = pygame.Surface((VP_W, VP_H), pygame.SRCALPHA)
        tc = self.th.get("torch", (220, 160, 60))
        fl = int(abs(math.sin(self.torch_time * 6)) * 7) + 2
        for r in range(3):
            rad = VP_W // 2 - r * 55
            if rad > 0:
                pygame.draw.ellipse(gs, (*tc, fl + r), (VP_W // 2 - rad, VP_H // 2 - rad, rad * 2, rad * 2))
        surface.blit(gs, (VP_X, VP_Y))

    def _render_slice(self, surface, px, py, fdx, fdy, rdx, rdy, depth):
        ns, fs = self._persp(depth - 1), self._persp(depth)
        nl, nt, nr, nb = self._sr(ns); fl, ft, fr, fb = self._sr(fs)
        bright = max(0.15, 1.0 - depth * 0.17) * self.torch_brightness
        cx, cy = px + fdx * depth, py + fdy * depth
        center = self._gtype(cx, cy)
        if center == DT_WALL or center is None:
            self._front_wall(surface, fl, ft, fr - fl, fb - ft, bright, depth); return
        left_dist = right_dist = 0
        for d in range(1, 5):
            if self._gtype(cx - rdx * d, cy - rdy * d) in (DT_WALL, None): break
            left_dist = d
        for d in range(1, 5):
            if self._gtype(cx + rdx * d, cy + rdy * d) in (DT_WALL, None): break
            right_dist = d
        ch = (nr - nl) // 2; wp = 0.25
        # Left
        if left_dist == 0:
            lt = self._gtype(cx - rdx, cy - rdy)
            if lt == DT_WALL or lt is None:
                self._side_wall(surface, nl, nt, nb, fl, ft, fb, bright, "L", depth)
            else:
                fl2 = self._gtype(cx - rdx * 2, cy - rdy * 2)
                self._side_open(surface, nl, nt, nb, fl, ft, fb, bright, fl2, "L")
                lt2 = self.dungeon.get_tile(cx - rdx, cy - rdy)
                if lt2 and lt2["type"] not in (DT_WALL, DT_FLOOR, DT_CORRIDOR):
                    self._side_obj(surface, lt2, nl, nt, nb, fl, ft, fb, bright, "L")
        else:
            p = int(ch * wp * left_dist); wb = bright * max(0.4, 1 - left_dist * 0.15)
            self._side_wall(surface, nl - p, nt, nb, fl - p, ft, fb, wb, "L", depth)
            for d in range(1, left_dist + 1):
                lt2 = self.dungeon.get_tile(cx - rdx * d, cy - rdy * d)
                if lt2 and lt2["type"] not in (DT_WALL, DT_FLOOR, DT_CORRIDOR):
                    frac = d / (left_dist + 1)
                    self._side_obj(surface, lt2, int(nl - p * frac), nt, nb, int(fl - p * frac), ft, fb, bright * 0.8, "L")
        # Right
        if right_dist == 0:
            rt = self._gtype(cx + rdx, cy + rdy)
            if rt == DT_WALL or rt is None:
                self._side_wall(surface, nr, nt, nb, fr, ft, fb, bright, "R", depth)
            else:
                fr2 = self._gtype(cx + rdx * 2, cy + rdy * 2)
                self._side_open(surface, nr, nt, nb, fr, ft, fb, bright, fr2, "R")
                rt2 = self.dungeon.get_tile(cx + rdx, cy + rdy)
                if rt2 and rt2["type"] not in (DT_WALL, DT_FLOOR, DT_CORRIDOR):
                    self._side_obj(surface, rt2, nr, nt, nb, fr, ft, fb, bright, "R")
        else:
            p = int(ch * wp * right_dist); wb = bright * max(0.4, 1 - right_dist * 0.15)
            self._side_wall(surface, nr + p, nt, nb, fr + p, ft, fb, wb, "R", depth)
            for d in range(1, right_dist + 1):
                rt2 = self.dungeon.get_tile(cx + rdx * d, cy + rdy * d)
                if rt2 and rt2["type"] not in (DT_WALL, DT_FLOOR, DT_CORRIDOR):
                    frac = d / (right_dist + 1)
                    self._side_obj(surface, rt2, int(nr + p * frac), nt, nb, int(fr + p * frac), ft, fb, bright * 0.8, "R")
        tile = self.dungeon.get_tile(cx, cy)
        if tile and tile["type"] not in (DT_FLOOR, DT_CORRIDOR, DT_WALL):
            self._center_obj(surface, tile, fl, ft, fr - fl, fb - ft, bright, depth)

    # ── TEXTURED FRONT WALL ──
    def _front_wall(self, surface, x, y, w, h, b, depth):
        if w < 2 or h < 2: return
        tsz = 128 if w > 80 else 64
        tex = gen_wall_texture(self.th, tsz, tsz)
        scaled = pygame.transform.scale(tex, (max(1, int(w)), max(1, int(h))))
        darkness = int(255 * (1.0 - min(1.0, b)))
        if darkness > 0:
            dk = pygame.Surface((scaled.get_width(), scaled.get_height()), pygame.SRCALPHA)
            dk.fill((0, 0, 0, darkness)); scaled.blit(dk, (0, 0))
        surface.blit(scaled, (int(x), int(y)))
        hl = self._dim(self.th["wl"], b * 0.35)
        pygame.draw.line(surface, hl, (int(x), int(y)), (int(x + w), int(y)), 1)
        pygame.draw.line(surface, hl, (int(x), int(y)), (int(x), int(y + h)), 1)

    # ── SIDE WALL (with torch sconces) ──
    def _side_wall(self, surface, ne, nt, nb, fe, ft, fb, b, side, depth=1):
        col = self._dim(self.th["wd"], b * 0.8)
        ln = self._dim(self.th["wl"], b * 0.4)
        pygame.draw.polygon(surface, col, [(ne, nt), (fe, ft), (fe, fb), (ne, nb)])
        for i in range(1, 6):
            f = i / 6; y1 = int(nt + (nb - nt) * f); y2 = int(ft + (fb - ft) * f)
            pygame.draw.line(surface, ln, (ne, y1), (fe, y2), 1)
        mx = (ne + fe) // 2
        pygame.draw.line(surface, ln, (mx, (nt + ft) // 2), (mx, (nb + fb) // 2), 1)
        if depth <= 2 and abs(ne - fe) > 25:
            ty = (nt + nb) // 2 - 8; tx = ne + (fe - ne) // 3
            tc = self.th.get("torch", (220, 160, 60))
            fl = 0.75 + 0.25 * math.sin(self.torch_time * 7 + ne * 0.1)
            pygame.draw.rect(surface, self._dim((60, 40, 20), b), (tx - 2, ty, 5, 10))
            pygame.draw.circle(surface, self._dim(tc, b * fl), (tx, ty - 2), 4)
            pygame.draw.circle(surface, self._dim((255, 240, 180), b * fl * 0.5), (tx, ty - 4), 2)
            if random.random() < 0.04: self.particles.emit_torch(tx, ty - 4, 1)

    def _side_open(self, surface, ne, nt, nb, fe, ft, fb, b, back, side):
        fc, cc = self._dim(self.th["fl"], b * 0.5), self._dim(self.th["cl"], b * 0.5)
        mn, mf = (nt + nb) // 2, (ft + fb) // 2
        pygame.draw.polygon(surface, cc, [(ne, nt), (fe, ft), (fe, mf), (ne, mn)])
        pygame.draw.polygon(surface, fc, [(ne, mn), (fe, mf), (fe, fb), (ne, nb)])
        if back == DT_WALL or back is None:
            bc = self._dim(self.th["wall"], b * 0.35); pw = abs(ne - fe); bw = max(3, pw // 3)
            if side == "L": pygame.draw.rect(surface, bc, (fe, ft, bw, fb - ft))
            else: pygame.draw.rect(surface, bc, (fe - bw, ft, bw, fb - ft))

    def _side_obj(self, surface, tile, ne, nt, nb, fe, ft, fb, b, side):
        mx, my = (ne + fe) // 2, (nt + nb + ft + fb) // 4; sz = max(6, abs(ne - fe) // 4)
        t = tile["type"]
        if t == DT_DOOR:
            pygame.draw.rect(surface, self._dim(DOOR_COL, b), (mx - sz, my - sz, sz * 2, sz * 2))
            pygame.draw.rect(surface, self._dim(DOOR_DARK, b), (mx - sz, my - sz, sz * 2, sz * 2), 1)
        elif t == DT_STAIRS_DOWN:
            pygame.draw.polygon(surface, self._dim(SD_COL, b), [(mx, my + sz), (mx - sz, my - sz), (mx + sz, my - sz)])
        elif t == DT_STAIRS_UP:
            pygame.draw.polygon(surface, self._dim(SU_COL, b), [(mx, my - sz), (mx - sz, my + sz), (mx + sz, my + sz)])
        elif t == DT_TREASURE:
            ev = tile.get("event") or {}
            if not ev.get("opened"):
                pygame.draw.rect(surface, self._dim(TREAS_COL, b), (mx - sz, my, sz * 2, sz))
                gl = int(abs(math.sin(self.torch_time * 2)) * 20) + 5
                gs = pygame.Surface((sz * 3, sz * 2), pygame.SRCALPHA); gs.fill((255, 215, 0, gl))
                surface.blit(gs, (mx - sz - sz // 2, my - sz // 2))
        elif t == DT_TRAP:
            ev = tile.get("event") or {}
            if ev.get("detected") and not ev.get("disarmed"):
                c = self._dim(TRAP_COL, b)
                pygame.draw.line(surface, c, (mx - sz, my - sz), (mx + sz, my + sz), 2)
                pygame.draw.line(surface, c, (mx + sz, my - sz), (mx - sz, my + sz), 2)

    def _center_obj(self, surface, tile, x, y, w, h, b, depth):
        t = tile["type"]
        if t == DT_DOOR:
            dw, dh = int(w * 0.85), int(h * 0.85); dx, dy = x + (w - dw) // 2, y + h - dh
            pygame.draw.rect(surface, self._dim(DOOR_FRAME, b), (dx - 4, dy - 4, dw + 8, dh + 4))
            pygame.draw.rect(surface, self._dim(DOOR_COL, b), (dx, dy, dw, dh))
            pw, ph = dw // 2 - 6, dh // 2 - 6
            if pw > 4 and ph > 4:
                dc = self._dim(DOOR_DARK, b)
                for ox, oy in [(4, 4), (dw // 2 + 2, 4), (4, dh // 2 + 2), (dw // 2 + 2, dh // 2 + 2)]:
                    pygame.draw.rect(surface, dc, (dx + ox, dy + oy, pw, ph))
            band = self._dim((60, 55, 50), b)
            pygame.draw.rect(surface, band, (dx, dy + dh // 4, dw, max(2, dh // 20)))
            pygame.draw.rect(surface, band, (dx, dy + 3 * dh // 4, dw, max(2, dh // 20)))
            pygame.draw.circle(surface, self._dim((200, 180, 80), b), (dx + dw - max(10, dw // 8), dy + dh // 2), max(3, dw // 14))
        elif t == DT_STAIRS_DOWN:
            sw, ns = int(w * 0.6), min(6, max(3, h // 20)); sh = h // (ns + 1); sx = x + (w - sw) // 2
            for i in range(ns):
                sy = y + h - (i + 1) * sh; shrk = i * 4; sb = b * (1 - i * 0.12)
                pygame.draw.rect(surface, self._dim(SD_COL, sb), (sx + shrk, sy, sw - shrk * 2, sh - 2))
                pygame.draw.rect(surface, self._dim((60, 55, 20), sb), (sx + shrk, sy + sh - 3, sw - shrk * 2, 3))
            acx = x + w // 2
            pygame.draw.polygon(surface, self._dim(SD_COL, b * 1.2), [(acx, y + h - 10), (acx - 8, y + h - 22), (acx + 8, y + h - 22)])
        elif t == DT_STAIRS_UP:
            sw, ns = int(w * 0.6), min(6, max(3, h // 20)); sh = h // (ns + 1); sx = x + (w - sw) // 2
            for i in range(ns):
                sy = y + i * sh + sh; shrk = (ns - 1 - i) * 4; sb = b * (0.7 + i * 0.08)
                pygame.draw.rect(surface, self._dim(SU_COL, sb), (sx + shrk, sy, sw - shrk * 2, sh - 2))
                pygame.draw.line(surface, self._dim((120, 220, 255), sb), (sx + shrk, sy), (sx + sw - shrk * 2, sy), 1)
            acx = x + w // 2
            pygame.draw.polygon(surface, self._dim(SU_COL, b * 1.2), [(acx, y + 10), (acx - 8, y + 22), (acx + 8, y + 22)])
            gs = pygame.Surface((sw, sh * 2), pygame.SRCALPHA); gs.fill((180, 220, 255, 12)); surface.blit(gs, (sx, y))
        elif t == DT_ENTRANCE:
            aw, ah = int(w * 0.7), int(h * 0.8); ax, ay = x + (w - aw) // 2, y + h - ah
            c = self._dim(ENTRANCE_COL, b)
            pygame.draw.arc(surface, c, (ax, ay, aw, ah // 2), 0, 3.14, 4)
            pygame.draw.line(surface, c, (ax, ay + ah // 4), (ax, y + h), 3)
            pygame.draw.line(surface, c, (ax + aw, ay + ah // 4), (ax + aw, y + h), 3)
            gs = pygame.Surface((aw, ah), pygame.SRCALPHA); gs.fill((180, 255, 180, 8)); surface.blit(gs, (ax, ay))
        elif t == DT_TREASURE:
            ev = tile.get("event") or {}; opened = ev.get("opened", False)
            cw, ch = max(16, int(w * 0.3)), max(12, int(h * 0.22))
            cx, cy = x + (w - cw) // 2, y + h - ch - max(4, int(h * 0.08))
            base = TREAS_OPEN if opened else TREAS_COL; col = self._dim(base, b)
            dk = self._dim(tuple(max(0, c - 50) for c in base), b)
            pygame.draw.rect(surface, col, (cx, cy, cw, ch))
            if opened: pygame.draw.rect(surface, dk, (cx - 2, cy - ch // 3, cw + 4, ch // 3))
            else:
                pygame.draw.rect(surface, dk, (cx, cy, cw, ch // 3))
                pygame.draw.circle(surface, self._dim((220, 200, 100), b), (cx + cw // 2, cy + ch // 3), max(2, cw // 10))
                gl = int(abs(math.sin(self.torch_time * 2)) * 30) + 5
                gs = pygame.Surface((cw, ch), pygame.SRCALPHA); gs.fill((255, 255, 200, gl)); surface.blit(gs, (cx, cy))
        elif t == DT_TRAP:
            ev = tile.get("event") or {}
            if ev.get("detected") and not ev.get("disarmed"):
                tc = self._dim(TRAP_COL, b); tcx, tcy = x + w // 2, y + h - h // 4; sz = max(8, w // 8)
                pygame.draw.line(surface, tc, (tcx - sz, tcy - sz), (tcx + sz, tcy + sz), 3)
                pygame.draw.line(surface, tc, (tcx + sz, tcy - sz), (tcx - sz, tcy + sz), 3)
                if w > 40: draw_text(surface, "!", tcx - 4, tcy - sz - 14, tc, 14, bold=True)

    # ── ENEMY SPRITES ──
    def _draw_enemies(self, surface, px, py, fdx, fdy, rdx, rdy):
        for depth in range(1, VIEW_DEPTH):
            ex, ey = px + fdx * depth, py + fdy * depth
            tile = self.dungeon.get_tile(ex, ey)
            if not tile or tile["type"] == DT_WALL: break
            ev = tile.get("event")
            if ev and isinstance(ev, dict) and ev.get("type") in ("fixed_encounter", "boss_encounter") and not ev.get("triggered"):
                self._draw_enemy_at(surface, depth, ev.get("type") == "boss_encounter")

    def _draw_enemy_at(self, surface, depth, is_boss=False):
        s = self._persp(depth); hw = int(VP_W * s * 0.10); hh = int(VP_H * s * 0.22)
        cx, cy = VP_CX, VP_CY + int(VP_H * s * 0.08)
        b = max(0.2, 1 - depth * 0.22)
        col = self._dim((160, 25, 25) if is_boss else (80, 35, 35), b)
        pygame.draw.ellipse(surface, col, (cx - hw, cy - hh, hw * 2, hh * 2))
        hr = max(3, hw // 2)
        pygame.draw.circle(surface, col, (cx, cy - hh - hr + 2), hr)
        if depth <= 3:
            pulse = 0.5 + 0.5 * abs(math.sin(self.torch_time * 3.5))
            ec = self._dim((255, 50, 50), pulse); es = max(1, hr // 3)
            pygame.draw.circle(surface, ec, (cx - es - 1, cy - hh - hr + 2), es)
            pygame.draw.circle(surface, ec, (cx + es + 1, cy - hh - hr + 2), es)

    def _draw_nearby(self, surface, px, py, fdx, fdy, rdx, rdy):
        tile = self.dungeon.get_tile(px, py)
        if not tile: return
        t = tile["type"]; my = VP_Y + VP_H - 30
        if t == DT_STAIRS_DOWN:
            draw_text(surface, "▼ Stairs Down — ENTER ▼", VP_CX - 110, my, SD_COL, 16, bold=True)
        elif t in (DT_STAIRS_UP, DT_ENTRANCE):
            lbl = "Exit" if self.dungeon.current_floor == 1 else "Stairs Up"
            draw_text(surface, f"▲ {lbl} — ENTER ▲", VP_CX - 80, my, SU_COL, 16, bold=True)
        for label, dx, dy in [("left", -rdx, -rdy), ("right", rdx, rdy), ("ahead", fdx, fdy)]:
            adj = self.dungeon.get_tile(px + dx, py + dy)
            if adj and adj["type"] == DT_TRAP:
                ev = adj.get("event") or {}
                if ev.get("detected") and not ev.get("disarmed"):
                    draw_text(surface, f"⚠ Trap {label}!", VP_X + 10, my - 22, TRAP_COL, 14)
            if adj:
                jev = adj.get("event")
                if jev and isinstance(jev, dict) and jev.get("type") == "journal" and not jev.get("triggered"):
                    draw_text(surface, f"📜 Something {label}...", VP_X + 10, my - 42, JOURNAL_COL, 13)

    # ══════════════════════════════════════════════════════════
    #  MINIMAP
    # ══════════════════════════════════════════════════════════
    def _draw_minimap(self, surface):
        floor = self.dungeon.get_current_floor_data()
        fw, fh = floor["width"], floor["height"]
        mm_max_w = SCREEN_W - VP_X - VP_W - 30; mm_max_h = 320
        mm_x = VP_X + VP_W + 15; mm_y = VP_Y + 100
        ts = max(2, min(mm_max_w // fw, mm_max_h // fh))
        mm_w, mm_h = fw * ts, fh * ts
        bg = pygame.Rect(mm_x - 3, mm_y - 3, mm_w + 6, mm_h + 6)
        pygame.draw.rect(surface, (8, 6, 12), bg, border_radius=3)
        pygame.draw.rect(surface, PANEL_BORDER, bg, 1, border_radius=3)
        for y in range(fh):
            for x in range(fw):
                tile = floor["tiles"][y][x]
                if not tile["discovered"]: continue
                px_m, py_m = mm_x + x * ts, mm_y + y * ts
                tt = tile["type"]
                if tt == DT_WALL: col = (50, 45, 40)
                elif tt in (DT_FLOOR, DT_CORRIDOR): col = (110, 100, 85)
                elif tt == DT_DOOR: col = (140, 100, 50)
                elif tt == DT_STAIRS_DOWN: col = SD_COL
                elif tt in (DT_STAIRS_UP, DT_ENTRANCE): col = SU_COL
                elif tt == DT_TREASURE: col = TREAS_OPEN if (tile.get("event") or {}).get("opened") else TREAS_COL
                elif tt == DT_TRAP:
                    ev = tile.get("event") or {}
                    col = TRAP_COL if ev.get("detected") and not ev.get("disarmed") else (110, 100, 85)
                else: col = (80, 72, 60)
                pygame.draw.rect(surface, col, (px_m, py_m, ts, ts))
        ppx = mm_x + self.dungeon.party_x * ts + ts // 2
        ppy = mm_y + self.dungeon.party_y * ts + ts // 2
        ps = max(2, ts // 2)
        pygame.draw.rect(surface, (255, 255, 80), (ppx - ps, ppy - ps, ps * 2, ps * 2))
        fdx, fdy = DIR_DX[self.facing], DIR_DY[self.facing]
        ax, ay = ppx + fdx * (ts + 1), ppy + fdy * (ts + 1)
        pygame.draw.line(surface, (255, 100, 100), (ppx, ppy), (ax, ay), 2)

    # ══════════════════════════════════════════════════════════
    #  HUD
    # ══════════════════════════════════════════════════════════
    def _draw_hud(self, surface, mx, my):
        top = pygame.Rect(0, 0, SCREEN_W, 44)
        pygame.draw.rect(surface, (12, 10, 24), top)
        pygame.draw.line(surface, PANEL_BORDER, (0, 44), (SCREEN_W, 44))
        draw_text(surface, self.dungeon.name, 15, 6, GOLD, 18, bold=True)
        draw_text(surface, f"Floor {self.dungeon.current_floor}/{self.dungeon.total_floors}  |  {DIR_NAMES[self.facing]}", 15, 26, CREAM, 13)
        rp_x = VP_X + VP_W + 15
        draw_text(surface, "Party", rp_x, VP_Y, GOLD, 16, bold=True)
        for i, c in enumerate(self.dungeon.party):
            from core.classes import get_all_resources
            mr = get_all_resources(c.class_name, c.stats, c.level)
            hp, mhp = c.resources.get("HP", 0), mr.get("HP", 1)
            pct = hp / mhp if mhp > 0 else 0
            hc = GREEN if pct > 0.5 else ORANGE if pct > 0.25 else RED
            draw_text(surface, f"{c.name[:8]}", rp_x, VP_Y + 22 + i * 18, CREAM, 12)
            draw_text(surface, f"{hp}/{mhp}", rp_x + 90, VP_Y + 22 + i * 18, hc, 12)
            from core.status_effects import get_status_display
            statuses = get_status_display(c)
            if statuses:
                sx = rp_x + 150
                for sname, scolor in statuses[:2]:
                    draw_text(surface, sname[:6], sx, VP_Y + 22 + i * 18, scolor, 9); sx += 50
        tile = self.dungeon.get_tile(self.dungeon.party_x, self.dungeon.party_y)
        if tile:
            t = tile["type"]
            if t == DT_STAIRS_DOWN: draw_text(surface, "ENTER to descend", VP_X + 10, VP_Y + VP_H + 8, SD_COL, 14)
            elif t in (DT_STAIRS_UP, DT_ENTRANCE):
                draw_text(surface, "ENTER to exit" if self.dungeon.current_floor == 1 else "ENTER to ascend", VP_X + 10, VP_Y + VP_H + 8, SU_COL, 14)
        by = SCREEN_H - 55
        for rect, label, sz in [(pygame.Rect(VP_X, by, 120, 42), "Camp", 15), (pygame.Rect(VP_X + 140, by, 120, 42), "Menu", 15),
                                 (pygame.Rect(VP_X + 280, by, 100, 42), "◄ Turn", 14), (pygame.Rect(VP_X + 400, by, 100, 42), "Turn ►", 14)]:
            draw_button(surface, rect, label, hover=rect.collidepoint(mx, my), size=sz)
        draw_text(surface, "↑/W=Fwd  ↓/S=Back  ←→/QE=Turn  A/D=Strafe  C=Camp  T=Disarm  ENTER=Use", VP_X, SCREEN_H - 8, DARK_GREY, 11)

    # ══════════════════════════════════════════════════════════
    #  DIALOGS
    # ══════════════════════════════════════════════════════════
    def _draw_camp_dlg(self, surface, mx, my):
        ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA); ov.fill((0, 0, 0, 140)); surface.blit(ov, (0, 0))
        d = pygame.Rect(SCREEN_W // 2 - 220, SCREEN_H // 2 - 100, 440, 200)
        pygame.draw.rect(surface, (20, 16, 36), d, border_radius=5); pygame.draw.rect(surface, GOLD, d, 2, border_radius=5)
        draw_text(surface, "Camp in the Dungeon?", d.x + 100, d.y + 15, GOLD, 22, bold=True)
        draw_text(surface, "Restores ~25% HP, ~15% MP/SP.", d.x + 20, d.y + 55, CREAM, 14)
        draw_text(surface, "Higher ambush risk underground!", d.x + 20, d.y + 80, ORANGE, 14)
        yb = pygame.Rect(d.x + 60, d.y + 140, 140, 40); draw_button(surface, yb, "Rest", hover=yb.collidepoint(mx, my), size=16)
        nb = pygame.Rect(d.x + 240, d.y + 140, 140, 40); draw_button(surface, nb, "Cancel", hover=nb.collidepoint(mx, my), size=16)

    def _draw_stairs_dlg(self, surface, mx, my):
        ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA); ov.fill((0, 0, 0, 120)); surface.blit(ov, (0, 0))
        d = pygame.Rect(SCREEN_W // 2 - 200, SCREEN_H // 2 - 80, 400, 160)
        pygame.draw.rect(surface, (20, 16, 36), d, border_radius=5); pygame.draw.rect(surface, GOLD, d, 2, border_radius=5)
        if self.stairs_direction == "down": txt, col = f"Descend to Floor {self.dungeon.current_floor + 1}?", SD_COL
        elif self.stairs_direction == "exit": txt, col = "Exit the dungeon?", ENTRANCE_COL
        else: txt, col = f"Ascend to Floor {self.dungeon.current_floor - 1}?", SU_COL
        draw_text(surface, txt, d.x + 80, d.y + 20, col, 20, bold=True)
        yb = pygame.Rect(d.x + 40, d.y + 100, 140, 40); draw_button(surface, yb, "Yes", hover=yb.collidepoint(mx, my), size=16)
        nb = pygame.Rect(d.x + 220, d.y + 100, 140, 40); draw_button(surface, nb, "No", hover=nb.collidepoint(mx, my), size=16)

    # ══════════════════════════════════════════════════════════
    #  INPUT
    # ══════════════════════════════════════════════════════════
    def handle_key(self, key):
        if self.show_camp_confirm or self.show_stairs_confirm: return None
        if key in (pygame.K_UP, pygame.K_w): return self.dungeon.move(DIR_DX[self.facing], DIR_DY[self.facing])
        elif key in (pygame.K_DOWN, pygame.K_s): return self.dungeon.move(-DIR_DX[self.facing], -DIR_DY[self.facing])
        elif key in (pygame.K_LEFT, pygame.K_q): self.facing = (self.facing - 1) % 4; return None
        elif key in (pygame.K_RIGHT, pygame.K_e): self.facing = (self.facing + 1) % 4; return None
        elif key == pygame.K_a: lf = (self.facing - 1) % 4; return self.dungeon.move(DIR_DX[lf], DIR_DY[lf])
        elif key == pygame.K_d: rf = (self.facing + 1) % 4; return self.dungeon.move(DIR_DX[rf], DIR_DY[rf])
        elif key == pygame.K_RETURN:
            tile = self.dungeon.get_tile(self.dungeon.party_x, self.dungeon.party_y)
            if tile:
                if tile["type"] == DT_STAIRS_DOWN: self.show_stairs_confirm = True; self.stairs_direction = "down"
                elif tile["type"] in (DT_STAIRS_UP, DT_ENTRANCE):
                    self.show_stairs_confirm = True; self.stairs_direction = "exit" if self.dungeon.current_floor == 1 else "up"
            return None
        elif key == pygame.K_c: self.show_camp_confirm = True; return None
        elif key == pygame.K_t:
            fdx, fdy = DIR_DX[self.facing], DIR_DY[self.facing]
            rdx, rdy = DIR_DX[(self.facing + 1) % 4], DIR_DY[(self.facing + 1) % 4]
            px, py = self.dungeon.party_x, self.dungeon.party_y
            for dx, dy in [(fdx, fdy), (-fdx, -fdy), (rdx, rdy), (-rdx, -rdy)]:
                tile = self.dungeon.get_tile(px + dx, py + dy)
                if tile and tile["type"] == DT_TRAP:
                    ev = tile.get("event") or {}
                    if ev.get("detected") and not ev.get("disarmed"):
                        if self.dungeon.disarm_trap(px + dx, py + dy): self.show_event("Trap disarmed!", (100, 255, 100))
                        else: return {"type": "trap", "data": ev}
                        return None
            self.show_event("No detected trap nearby.", CREAM); return None
        return None

    def handle_click(self, mx, my):
        if self.show_stairs_confirm:
            d = pygame.Rect(SCREEN_W // 2 - 200, SCREEN_H // 2 - 80, 400, 160)
            yb = pygame.Rect(d.x + 40, d.y + 100, 140, 40); nb = pygame.Rect(d.x + 220, d.y + 100, 140, 40)
            if yb.collidepoint(mx, my):
                self.show_stairs_confirm = False
                if self.stairs_direction == "down": return {"type": "stairs_down"}
                elif self.stairs_direction == "up": return {"type": "stairs_up"}
                else: return {"type": "exit_dungeon"}
            elif nb.collidepoint(mx, my): self.show_stairs_confirm = False
            return None
        if self.show_camp_confirm:
            d = pygame.Rect(SCREEN_W // 2 - 220, SCREEN_H // 2 - 100, 440, 200)
            yb = pygame.Rect(d.x + 60, d.y + 140, 140, 40); nb = pygame.Rect(d.x + 240, d.y + 140, 140, 40)
            if yb.collidepoint(mx, my): self.show_camp_confirm = False; return {"type": "camp"}
            elif nb.collidepoint(mx, my): self.show_camp_confirm = False
            return None
        by = SCREEN_H - 55
        if pygame.Rect(VP_X, by, 120, 42).collidepoint(mx, my): self.show_camp_confirm = True; return None
        if pygame.Rect(VP_X + 140, by, 120, 42).collidepoint(mx, my): return {"type": "menu"}
        if pygame.Rect(VP_X + 280, by, 100, 42).collidepoint(mx, my): self.facing = (self.facing - 1) % 4; return None
        if pygame.Rect(VP_X + 400, by, 100, 42).collidepoint(mx, my): self.facing = (self.facing + 1) % 4; return None
        return None

    def show_event(self, msg, color=CREAM):
        self.event_message = msg; self.event_color = color; self.event_timer = 3500
        self.event_queue.append((msg, color, 3500))
