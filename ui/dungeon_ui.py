"""
Realm of Shadows — Dungeon UI (Top-Down View v2)
Large tiles, torch-lit radius, clear wall framing, object icons,
minimap overlay, smooth camera follow, themed palettes.
"""
import pygame, math, random
from ui.renderer import *
from data.dungeon import (
    DungeonState, PASSABLE_TILES, DT_WALL, DT_FLOOR, DT_CORRIDOR,
    DT_DOOR, DT_STAIRS_DOWN, DT_STAIRS_UP, DT_TREASURE, DT_TRAP, DT_ENTRANCE,
    DT_SECRET_DOOR,
)

# ── Layout ──
VP_X, VP_Y = 10, 50
VP_W, VP_H = 840, 630
TS = 32                  # tile size in pixels
TORCH_R = 8             # lit radius around party
FOG_B = 0.22            # brightness of discovered-but-dark tiles

# ── Theme palettes ──
THEMES = {
    "cave": {
        "wall_fill": (38, 32, 26),  "wall_top": (55, 48, 38),
        "floor": (90, 78, 62),      "corr": (82, 72, 58),
        "grid": (68, 58, 46),       "bg": (12, 10, 8),
        "torch": (220, 160, 60),
    },
    "mine": {
        "wall_fill": (48, 38, 28),  "wall_top": (65, 55, 42),
        "floor": (100, 88, 68),     "corr": (92, 80, 62),
        "grid": (75, 64, 50),       "bg": (10, 8, 6),
        "torch": (240, 180, 70),
    },
    "crypt": {
        "wall_fill": (30, 32, 45),  "wall_top": (48, 52, 68),
        "floor": (62, 66, 82),      "corr": (56, 60, 74),
        "grid": (44, 48, 60),       "bg": (8, 8, 14),
        "torch": (120, 140, 200),
    },
    "ruins": {
        "wall_fill": (42, 36, 28),  "wall_top": (62, 52, 40),
        "floor": (98, 85, 68),      "corr": (90, 78, 62),
        "grid": (72, 62, 50),       "bg": (10, 8, 6),
        "torch": (230, 170, 60),
    },
    "tower": {
        "wall_fill": (35, 30, 50),  "wall_top": (55, 48, 75),
        "floor": (70, 65, 90),      "corr": (62, 58, 82),
        "grid": (50, 46, 68),       "bg": (8, 6, 16),
        "torch": (140, 120, 220),
    },
}

# ── Colors ──
C_DOOR      = (160, 115, 55)
C_DOOR_BRD  = (100, 70, 30)
C_SDN       = (200, 180, 60)
C_SUP       = (80, 190, 230)
C_TREAS     = (255, 220, 50)
C_TREAS_O   = (110, 90, 50)
C_ENTRANCE  = (100, 210, 110)
C_TRAP      = (220, 55, 55)
C_JOURNAL   = (210, 190, 130)
C_ENEMY     = (190, 40, 40)
C_BOSS      = (230, 30, 90)
C_PARTY     = (255, 255, 80)
C_PARTY_OUT = (200, 190, 50)


class DungeonUI:
    def __init__(self, ds):
        self.dungeon = ds
        self.th = THEMES.get(ds.theme, THEMES["cave"])
        self.facing = 0  # kept for API compat

        # Smooth camera (pixel coords)
        self.cam_x = float(ds.party_x * TS)
        self.cam_y = float(ds.party_y * TS)

        # Events
        self.event_message = ""
        self.event_timer = 0
        self.event_color = CREAM
        self.event_queue = []

        # Dialogs
        self.show_camp_confirm = False
        self.show_stairs_confirm = False
        self.stairs_direction = None

        # Animation
        self.t = 0.0
        self.pulse = 0.0

        # Fading
        self.fading_intensity = 0.0
        self._update_fading()

    def _update_fading(self):
        f = self.dungeon.current_floor
        t = self.dungeon.total_floors
        self.fading_intensity = min(0.5, (f - 1) / max(1, t) * 0.4)

    def on_floor_change(self):
        self._update_fading()
        self.cam_x = float(self.dungeon.party_x * TS)
        self.cam_y = float(self.dungeon.party_y * TS)

    @staticmethod
    def _dim(c, f):
        return tuple(max(0, min(255, int(v * f))) for v in c)

    # ══════════════════════════════════════════════════════════
    #  MAIN DRAW
    # ══════════════════════════════════════════════════════════

    def draw(self, surface, mx, my, dt):
        ds = dt / 1000.0
        self.event_timer = max(0, self.event_timer - dt)
        self.t += ds
        self.pulse = math.sin(self.t * 3.0) * 0.5 + 0.5
        self.event_queue = [(m, c, t - dt) for m, c, t in self.event_queue if t - dt > 0]

        # Smooth cam
        tx = float(self.dungeon.party_x * TS)
        ty = float(self.dungeon.party_y * TS)
        lr = min(1.0, 10.0 * ds)
        self.cam_x += (tx - self.cam_x) * lr
        self.cam_y += (ty - self.cam_y) * lr

        surface.fill(self.th["bg"])
        self._draw_map(surface)
        self._draw_minimap(surface)
        self._draw_hud(surface, mx, my)
        if self.show_camp_confirm:
            self._draw_camp_dlg(surface, mx, my)
        if self.show_stairs_confirm:
            self._draw_stairs_dlg(surface, mx, my)
        if (self.event_message and self.event_timer > 0) or self.event_queue:
            self._draw_events(surface)

    # ══════════════════════════════════════════════════════════
    #  MAP
    # ══════════════════════════════════════════════════════════

    def _draw_map(self, surface):
        clip = pygame.Rect(VP_X, VP_Y, VP_W, VP_H)
        surface.set_clip(clip)

        fl = self.dungeon.get_current_floor_data()
        fw, fh = fl["width"], fl["height"]
        px, py = self.dungeon.party_x, self.dungeon.party_y

        # Camera offset — party centred in viewport
        ox = VP_X + VP_W // 2 - int(self.cam_x) - TS // 2
        oy = VP_Y + VP_H // 2 - int(self.cam_y) - TS // 2

        # Visible range
        x0 = max(0, (-ox) // TS - 1)
        y0 = max(0, (-oy) // TS - 1)
        x1 = min(fw, x0 + VP_W // TS + 3)
        y1 = min(fh, y0 + VP_H // TS + 3)

        flicker = 0.92 + 0.08 * math.sin(self.t * 6.7)
        tiles = fl["tiles"]

        # ── Pass 1: floor + walls ──
        for ty in range(y0, y1):
            row = tiles[ty]
            for tx in range(x0, x1):
                tile = row[tx]
                if not tile["discovered"]:
                    continue
                sx = ox + tx * TS
                sy = oy + ty * TS
                if sx + TS < VP_X or sx > VP_X + VP_W or sy + TS < VP_Y or sy > VP_Y + VP_H:
                    continue

                dist = math.sqrt((tx - px) ** 2 + (ty - py) ** 2)
                lit = dist <= TORCH_R
                if lit:
                    b = max(0.35, 1.0 - (dist / TORCH_R) * 0.60) * flicker
                else:
                    b = FOG_B

                tt = tile["type"]
                # Undetected secret doors look like walls
                if tt == DT_SECRET_DOOR and not tile.get("secret_found"):
                    self._draw_wall(surface, sx, sy, b, tx, ty, tiles, fw, fh)
                elif tt == DT_WALL:
                    self._draw_wall(surface, sx, sy, b, tx, ty, tiles, fw, fh)
                else:
                    self._draw_floor_tile(surface, sx, sy, b, tt, tile)

        # ── Pass 2: objects on top ──
        for ty in range(y0, y1):
            row = tiles[ty]
            for tx in range(x0, x1):
                tile = row[tx]
                if not tile["discovered"]:
                    continue
                sx = ox + tx * TS
                sy = oy + ty * TS
                if sx + TS < VP_X or sx > VP_X + VP_W or sy + TS < VP_Y or sy > VP_Y + VP_H:
                    continue
                dist = math.sqrt((tx - px) ** 2 + (ty - py) ** 2)
                lit = dist <= TORCH_R
                b = (max(0.35, 1.0 - (dist / TORCH_R) * 0.60) * flicker) if lit else FOG_B
                self._draw_obj(surface, sx, sy, b, tile)

        # ── Party ──
        psx = ox + px * TS
        psy = oy + py * TS
        self._draw_party(surface, psx, psy)

        # ── Fading ──
        if self.fading_intensity > 0.05:
            self._draw_fading(surface)

        surface.set_clip(None)
        pygame.draw.rect(surface, PANEL_BORDER, clip, 2)

    # ── Wall drawing ──

    def _draw_wall(self, surface, sx, sy, b, tx, ty, tiles, fw, fh):
        th = self.th
        # Filled dark wall
        pygame.draw.rect(surface, self._dim(th["wall_fill"], b), (sx, sy, TS, TS))

        # Top surface highlight — gives 3D depth illusion
        top_h = max(2, TS // 5)
        pygame.draw.rect(surface, self._dim(th["wall_top"], b * 0.9),
                         (sx + 1, sy + 1, TS - 2, top_h))

        # Only draw border edges that face a non-wall tile (creates clear room outlines)
        edge = self._dim(th["wall_top"], b * 0.55)
        for dx, dy, x1, y1, x2, y2 in [
            (0, -1, sx, sy, sx + TS, sy),               # top
            (0,  1, sx, sy + TS - 1, sx + TS, sy + TS - 1),  # bottom
            (-1, 0, sx, sy, sx, sy + TS),                # left
            ( 1, 0, sx + TS - 1, sy, sx + TS - 1, sy + TS),  # right
        ]:
            nx, ny = tx + dx, ty + dy
            if 0 <= nx < fw and 0 <= ny < fh:
                if tiles[ny][nx]["type"] != DT_WALL:
                    pygame.draw.line(surface, edge, (x1, y1), (x2, y2), 2)

    # ── Floor tile ──

    def _draw_floor_tile(self, surface, sx, sy, b, tt, tile):
        th = self.th
        base = th["floor"] if tt == DT_FLOOR else th["corr"]
        col = self._dim(base, b)
        pygame.draw.rect(surface, col, (sx, sy, TS, TS))
        # Subtle grid
        if b > 0.28:
            gc = self._dim(th["grid"], b * 0.5)
            pygame.draw.rect(surface, gc, (sx, sy, TS, TS), 1)

    # ── Objects overlay (doors, stairs, treasure etc.) ──

    def _draw_obj(self, surface, sx, sy, b, tile):
        tt = tile["type"]
        cx, cy = sx + TS // 2, sy + TS // 2
        r = TS // 3  # icon radius

        if tt == DT_DOOR:
            dc = self._dim(C_DOOR, b)
            m = TS // 5
            pygame.draw.rect(surface, dc, (sx + m, sy + m, TS - m * 2, TS - m * 2), border_radius=2)
            pygame.draw.rect(surface, self._dim(C_DOOR_BRD, b),
                             (sx + m, sy + m, TS - m * 2, TS - m * 2), 2, border_radius=2)
            # Doorknob
            pygame.draw.circle(surface, self._dim((220, 200, 100), b),
                               (sx + TS - m - 4, cy), max(2, TS // 10))

        elif tt == DT_STAIRS_DOWN:
            c = self._dim(C_SDN, b)
            # Bold down arrow
            pygame.draw.polygon(surface, c,
                                [(cx, cy + r + 2), (cx - r - 1, cy - r // 2), (cx + r + 1, cy - r // 2)])
            pygame.draw.line(surface, c, (cx, cy - r - 2), (cx, cy + 2), 2)

        elif tt == DT_STAIRS_UP:
            c = self._dim(C_SUP, b)
            pygame.draw.polygon(surface, c,
                                [(cx, cy - r - 2), (cx - r - 1, cy + r // 2), (cx + r + 1, cy + r // 2)])
            pygame.draw.line(surface, c, (cx, cy + r + 2), (cx, cy - 2), 2)

        elif tt == DT_ENTRANCE:
            c = self._dim(C_ENTRANCE, b)
            m = TS // 5
            pygame.draw.rect(surface, c, (sx + m, sy + m, TS - m * 2, TS - m * 2), 3, border_radius=3)
            if b > 0.4:
                gs = pygame.Surface((TS, TS), pygame.SRCALPHA)
                gs.fill((*C_ENTRANCE[:3], 12))
                surface.blit(gs, (sx, sy))

        elif tt == DT_TREASURE:
            ev = tile.get("event") or {}
            opened = ev.get("opened", False)
            base = C_TREAS_O if opened else C_TREAS
            c = self._dim(base, b)
            # Chest
            bw, bh = TS // 2 + 2, TS // 3
            bx, by = cx - bw // 2, cy - bh // 2 + 2
            pygame.draw.rect(surface, c, (bx, by, bw, bh), border_radius=2)
            pygame.draw.rect(surface, self._dim((80, 60, 20) if opened else (180, 150, 30), b),
                             (bx, by, bw, bh), 1, border_radius=2)
            if not opened:
                # Lock
                pygame.draw.circle(surface, self._dim((240, 220, 100), b), (cx, cy + 1), max(2, TS // 9))
                # Pulse glow
                gl = int(self.pulse * 28) + 5
                gs = pygame.Surface((TS, TS), pygame.SRCALPHA)
                gs.fill((255, 220, 50, gl))
                surface.blit(gs, (sx, sy))

        elif tt == DT_TRAP:
            ev = tile.get("event") or {}
            det = ev.get("detected", False)
            dis = ev.get("disarmed", False)
            if det and not dis:
                c = self._dim(C_TRAP, b)
                pygame.draw.line(surface, c, (cx - r, cy - r), (cx + r, cy + r), 3)
                pygame.draw.line(surface, c, (cx + r, cy - r), (cx - r, cy + r), 3)
                # Danger pulse
                gl = int(self.pulse * 22) + 5
                gs = pygame.Surface((TS, TS), pygame.SRCALPHA)
                gs.fill((220, 55, 55, gl))
                surface.blit(gs, (sx, sy))
            elif dis:
                dc = self._dim((70, 70, 70), b)
                pygame.draw.line(surface, dc, (cx - r, cy), (cx + r, cy), 1)

        elif tt == DT_SECRET_DOOR:
            found = tile.get("secret_found", False)
            if found:
                # Render as a special door with a "?" mark
                dc = self._dim((100, 60, 140), b)  # purple-ish
                m = TS // 5
                pygame.draw.rect(surface, dc, (sx + m, sy + m, TS - m*2, TS - m*2), border_radius=2)
                pygame.draw.rect(surface, self._dim((160, 100, 200), b),
                                 (sx + m, sy + m, TS - m*2, TS - m*2), 2, border_radius=2)
                # Question mark hint
                if b > 0.3 and TS >= 12:
                    fc = self._dim((200, 160, 240), b)
                    try:
                        font = pygame.font.Font(None, max(10, TS // 2))
                        txt = font.render("?", True, fc)
                        surface.blit(txt, (cx - txt.get_width() // 2, cy - txt.get_height() // 2))
                    except Exception:
                        pass
                # Subtle glow
                gl = int(self.pulse * 20) + 4
                gs = pygame.Surface((TS, TS), pygame.SRCALPHA)
                gs.fill((140, 80, 200, gl))
                surface.blit(gs, (sx, sy))
            # If not found, render as wall (handled by the wall check above)

        # ── Event overlays ──
        ev = tile.get("event")
        if ev and isinstance(ev, dict):
            etype = ev.get("type", "")
            triggered = ev.get("triggered", False)

            if etype == "journal" and not triggered and b > 0.28:
                c = self._dim(C_JOURNAL, b)
                # Scroll icon
                sw, sh = TS // 3, TS // 2 - 1
                rx, ry = cx - sw // 2, cy - sh // 2
                pygame.draw.rect(surface, c, (rx, ry, sw, sh), border_radius=1)
                pygame.draw.line(surface, c, (rx + 2, ry + sh // 3), (rx + sw - 2, ry + sh // 3), 1)
                pygame.draw.line(surface, c, (rx + 2, ry + 2 * sh // 3), (rx + sw - 2, ry + 2 * sh // 3), 1)
                # Glow
                gl = int(self.pulse * 18) + 4
                gs = pygame.Surface((TS, TS), pygame.SRCALPHA)
                gs.fill((210, 190, 130, gl))
                surface.blit(gs, (sx, sy))

            elif etype in ("fixed_encounter", "boss_encounter") and not triggered and b > 0.28:
                boss = etype == "boss_encounter"
                ec = self._dim(C_BOSS if boss else C_ENEMY, b)
                er = r if boss else r - 1
                pygame.draw.circle(surface, ec, (cx, cy), er)
                # Eyes
                ep = 0.6 + 0.4 * self.pulse
                eye = self._dim((255, 80, 80), b * ep)
                gap = max(2, er // 2)
                pygame.draw.circle(surface, eye, (cx - gap, cy - 1), max(1, er // 4))
                pygame.draw.circle(surface, eye, (cx + gap, cy - 1), max(1, er // 4))
                if boss:
                    # Crown-like spikes
                    sc = self._dim((255, 200, 50), b)
                    for dx in [-er + 1, 0, er - 1]:
                        pygame.draw.line(surface, sc, (cx + dx, cy - er), (cx + dx, cy - er - 3), 1)

    # ── Party marker ──

    def _draw_party(self, surface, sx, sy):
        cx, cy = sx + TS // 2, sy + TS // 2
        r = TS // 3 + 1
        # Glow
        gs = pygame.Surface((TS + 8, TS + 8), pygame.SRCALPHA)
        gl = int(self.pulse * 18) + 12
        pygame.draw.circle(gs, (*C_PARTY[:3], gl), (TS // 2 + 4, TS // 2 + 4), r + 6)
        surface.blit(gs, (sx - 4, sy - 4))
        # Solid marker
        pygame.draw.circle(surface, C_PARTY, (cx, cy), r)
        pygame.draw.circle(surface, C_PARTY_OUT, (cx, cy), r, 2)
        # Inner shine
        pygame.draw.circle(surface, (255, 255, 220), (cx - 1, cy - 2), max(2, r // 3))

    # ── Fading overlay ──

    def _draw_fading(self, surface):
        ov = pygame.Surface((VP_W, VP_H), pygame.SRCALPHA)
        t = self.t
        a = int(self.fading_intensity * 35 * (0.7 + 0.3 * math.sin(t * 1.5)))
        ov.fill((80, 20, 120, a))
        for i in range(2):
            by = int((math.sin(t * 0.7 + i * 2.5) * 0.5 + 0.5) * VP_H)
            bh = int(15 + self.fading_intensity * 30)
            ba = int(self.fading_intensity * 25 * (0.5 + 0.5 * math.sin(t * 2.1 + i)))
            pygame.draw.rect(ov, (120, 40, 180, ba), (0, by, VP_W, bh))
        surface.blit(ov, (VP_X, VP_Y))

    # ══════════════════════════════════════════════════════════
    #  MINIMAP
    # ══════════════════════════════════════════════════════════

    def _draw_minimap(self, surface):
        fl = self.dungeon.get_current_floor_data()
        fw, fh = fl["width"], fl["height"]
        # Fit minimap in corner
        mm_max = 160
        ms = max(2, min(mm_max // fw, mm_max // fh))
        mw, mh = fw * ms, fh * ms
        mx0 = SCREEN_W - mw - 12
        my0 = VP_Y + VP_H - mh - 12

        # Background
        bg = pygame.Surface((mw + 4, mh + 4), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 160))
        surface.blit(bg, (mx0 - 2, my0 - 2))

        tiles = fl["tiles"]
        for ty in range(fh):
            row = tiles[ty]
            for tx in range(fw):
                tile = row[tx]
                if not tile["discovered"]:
                    continue
                tt = tile["type"]
                if tt == DT_WALL:
                    c = (45, 40, 35)
                elif tt in (DT_FLOOR, DT_CORRIDOR):
                    c = (100, 90, 75)
                elif tt == DT_DOOR:
                    c = (130, 95, 45)
                elif tt == DT_STAIRS_DOWN:
                    c = C_SDN
                elif tt in (DT_STAIRS_UP, DT_ENTRANCE):
                    c = C_SUP
                elif tt == DT_TREASURE:
                    ev = tile.get("event") or {}
                    c = C_TREAS_O if ev.get("opened") else C_TREAS
                elif tt == DT_TRAP:
                    ev = tile.get("event") or {}
                    c = C_TRAP if ev.get("detected") and not ev.get("disarmed") else (100, 90, 75)
                elif tt == DT_SECRET_DOOR:
                    if tile.get("secret_found"):
                        c = (140, 80, 200)  # purple for found secret doors
                    else:
                        c = (45, 40, 35)  # looks like wall
                else:
                    c = (80, 72, 60)
                pygame.draw.rect(surface, c, (mx0 + tx * ms, my0 + ty * ms, ms, ms))

        # Party dot
        ppx = mx0 + self.dungeon.party_x * ms + ms // 2
        ppy = my0 + self.dungeon.party_y * ms + ms // 2
        pr = max(2, ms)
        pygame.draw.circle(surface, C_PARTY, (ppx, ppy), pr)

        # Border
        pygame.draw.rect(surface, PANEL_BORDER, (mx0 - 2, my0 - 2, mw + 4, mh + 4), 1)

    # ══════════════════════════════════════════════════════════
    #  HUD
    # ══════════════════════════════════════════════════════════

    def _draw_hud(self, surface, mx, my):
        # Top bar
        pygame.draw.rect(surface, (12, 10, 24), (0, 0, SCREEN_W, 44))
        pygame.draw.line(surface, PANEL_BORDER, (0, 44), (SCREEN_W, 44))
        draw_text(surface, self.dungeon.name, 15, 6, GOLD, 18, bold=True)
        draw_text(surface, f"Floor {self.dungeon.current_floor}/{self.dungeon.total_floors}",
                  15, 26, CREAM, 13)

        # Party HP — right of dungeon name
        hpx = 320
        for i, c in enumerate(self.dungeon.party):
            from core.classes import get_all_resources
            mr = get_all_resources(c.class_name, c.stats, c.level)
            hp, mhp = c.resources.get("HP", 0), mr.get("HP", 1)
            pct = hp / mhp if mhp > 0 else 0
            hc = GREEN if pct > 0.5 else ORANGE if pct > 0.25 else RED
            draw_text(surface, f"{c.name[:6]}:{hp}/{mhp}", hpx, 8 + (i % 2) * 16, hc, 11)
            if i % 2 == 1:
                hpx += 130
            if i == 0:
                hpx = hpx  # first goes to second row same x
            if i % 2 == 1:
                pass  # already advanced

        # Tile hint
        tile = self.dungeon.get_tile(self.dungeon.party_x, self.dungeon.party_y)
        if tile:
            t = tile["type"]
            if t == DT_STAIRS_DOWN:
                draw_text(surface, "▼ ENTER to descend", VP_X + 10, VP_Y + VP_H + 6,
                          C_SDN, 14, bold=True)
            elif t in (DT_STAIRS_UP, DT_ENTRANCE):
                lbl = "exit" if self.dungeon.current_floor == 1 else "ascend"
                draw_text(surface, f"▲ ENTER to {lbl}", VP_X + 10, VP_Y + VP_H + 6,
                          C_SUP, 14, bold=True)

        # Buttons
        by = SCREEN_H - 46
        btns = [
            (pygame.Rect(VP_X, by, 100, 36), "Camp (C)", 13),
            (pygame.Rect(VP_X + 112, by, 100, 36), "Menu", 13),
            (pygame.Rect(VP_X + 224, by, 120, 36), "Disarm (T)", 13),
        ]
        for rect, label, sz in btns:
            draw_button(surface, rect, label, hover=rect.collidepoint(mx, my), size=sz)

        draw_text(surface, "Arrows/WASD = Move   ENTER = Use   C = Camp   T = Disarm",
                  VP_X, SCREEN_H - 6, DARK_GREY, 10)

    # ══════════════════════════════════════════════════════════
    #  EVENT MESSAGES
    # ══════════════════════════════════════════════════════════

    def _draw_events(self, surface):
        lines = []
        if self.event_message and self.event_timer > 0:
            lines.append((self.event_message, self.event_color))
        for m, c, _ in self.event_queue:
            if (m, c) not in lines:
                lines.append((m, c))
        if not lines:
            return
        h = max(36, len(lines) * 20 + 12)
        r = pygame.Rect(VP_X + VP_W // 2 - 280, VP_Y + 8, 560, h)
        ov = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
        ov.fill((10, 8, 20, 210))
        surface.blit(ov, r.topleft)
        pygame.draw.rect(surface, GOLD, r, 1, border_radius=4)
        for i, (msg, col) in enumerate(lines[:5]):
            draw_text(surface, msg, r.x + 14, r.y + 6 + i * 18, col, 13, max_width=r.w - 28)

    # ══════════════════════════════════════════════════════════
    #  DIALOGS
    # ══════════════════════════════════════════════════════════

    def _draw_camp_dlg(self, surface, mx, my):
        ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 140))
        surface.blit(ov, (0, 0))
        d = pygame.Rect(SCREEN_W // 2 - 220, SCREEN_H // 2 - 100, 440, 200)
        pygame.draw.rect(surface, (20, 16, 36), d, border_radius=5)
        pygame.draw.rect(surface, GOLD, d, 2, border_radius=5)
        draw_text(surface, "Camp in the Dungeon?", d.x + 100, d.y + 15, GOLD, 22, bold=True)
        draw_text(surface, "Restores ~25% HP, ~15% MP/SP.", d.x + 20, d.y + 55, CREAM, 14)
        draw_text(surface, "Higher ambush risk underground!", d.x + 20, d.y + 80, ORANGE, 14)
        yb = pygame.Rect(d.x + 60, d.y + 140, 140, 40)
        draw_button(surface, yb, "Rest", hover=yb.collidepoint(mx, my), size=16)
        nb = pygame.Rect(d.x + 240, d.y + 140, 140, 40)
        draw_button(surface, nb, "Cancel", hover=nb.collidepoint(mx, my), size=16)

    def _draw_stairs_dlg(self, surface, mx, my):
        ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 120))
        surface.blit(ov, (0, 0))
        d = pygame.Rect(SCREEN_W // 2 - 200, SCREEN_H // 2 - 80, 400, 160)
        pygame.draw.rect(surface, (20, 16, 36), d, border_radius=5)
        pygame.draw.rect(surface, GOLD, d, 2, border_radius=5)
        if self.stairs_direction == "down":
            txt, col = f"Descend to Floor {self.dungeon.current_floor + 1}?", C_SDN
        elif self.stairs_direction == "exit":
            txt, col = "Exit the dungeon?", C_ENTRANCE
        else:
            txt, col = f"Ascend to Floor {self.dungeon.current_floor - 1}?", C_SUP
        draw_text(surface, txt, d.x + 80, d.y + 20, col, 20, bold=True)
        yb = pygame.Rect(d.x + 40, d.y + 100, 140, 40)
        draw_button(surface, yb, "Yes", hover=yb.collidepoint(mx, my), size=16)
        nb = pygame.Rect(d.x + 220, d.y + 100, 140, 40)
        draw_button(surface, nb, "No", hover=nb.collidepoint(mx, my), size=16)

    # ══════════════════════════════════════════════════════════
    #  INPUT
    # ══════════════════════════════════════════════════════════

    def handle_key(self, key):
        if self.show_camp_confirm or self.show_stairs_confirm:
            return None

        dx, dy = 0, 0
        if key in (pygame.K_UP, pygame.K_w):       dy = -1
        elif key in (pygame.K_DOWN, pygame.K_s):    dy = 1
        elif key in (pygame.K_LEFT, pygame.K_a):    dx = -1
        elif key in (pygame.K_RIGHT, pygame.K_d):   dx = 1
        elif key == pygame.K_RETURN:
            tile = self.dungeon.get_tile(self.dungeon.party_x, self.dungeon.party_y)
            if tile:
                if tile["type"] == DT_STAIRS_DOWN:
                    self.show_stairs_confirm = True
                    self.stairs_direction = "down"
                elif tile["type"] in (DT_STAIRS_UP, DT_ENTRANCE):
                    self.show_stairs_confirm = True
                    self.stairs_direction = "exit" if self.dungeon.current_floor == 1 else "up"
            return None
        elif key == pygame.K_c:
            self.show_camp_confirm = True
            return None
        elif key == pygame.K_t:
            return self._try_disarm()

        if dx == 0 and dy == 0:
            return None
        result = self.dungeon.move(dx, dy)
        if result is not None or (dx != 0 or dy != 0):
            # Only play if we actually moved (check position changed)
            import core.sound as _sfx
            _sfx.play("footstep")
        return result

    def _try_disarm(self):
        px, py = self.dungeon.party_x, self.dungeon.party_y
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            tile = self.dungeon.get_tile(px + dx, py + dy)
            if tile and tile["type"] == DT_TRAP:
                ev = tile.get("event") or {}
                if ev.get("detected") and not ev.get("disarmed"):
                    if self.dungeon.disarm_trap(px + dx, py + dy):
                        self.show_event("Trap disarmed!", (100, 255, 100))
                    else:
                        return {"type": "trap", "data": ev}
                    return None
        self.show_event("No detected trap nearby.", CREAM)
        return None

    def handle_click(self, mx, my):
        if self.show_stairs_confirm:
            d = pygame.Rect(SCREEN_W // 2 - 200, SCREEN_H // 2 - 80, 400, 160)
            yb = pygame.Rect(d.x + 40, d.y + 100, 140, 40)
            nb = pygame.Rect(d.x + 220, d.y + 100, 140, 40)
            if yb.collidepoint(mx, my):
                self.show_stairs_confirm = False
                if self.stairs_direction == "down":   return {"type": "stairs_down"}
                elif self.stairs_direction == "up":   return {"type": "stairs_up"}
                else:                                 return {"type": "exit_dungeon"}
            elif nb.collidepoint(mx, my):
                self.show_stairs_confirm = False
            return None

        if self.show_camp_confirm:
            d = pygame.Rect(SCREEN_W // 2 - 220, SCREEN_H // 2 - 100, 440, 200)
            yb = pygame.Rect(d.x + 60, d.y + 140, 140, 40)
            nb = pygame.Rect(d.x + 240, d.y + 140, 140, 40)
            if yb.collidepoint(mx, my):
                self.show_camp_confirm = False
                return {"type": "camp"}
            elif nb.collidepoint(mx, my):
                self.show_camp_confirm = False
            return None

        by = SCREEN_H - 46
        if pygame.Rect(VP_X, by, 100, 36).collidepoint(mx, my):
            self.show_camp_confirm = True
            return None
        if pygame.Rect(VP_X + 112, by, 100, 36).collidepoint(mx, my):
            return {"type": "menu"}
        if pygame.Rect(VP_X + 224, by, 120, 36).collidepoint(mx, my):
            return self._try_disarm()
        return None

    def show_event(self, msg, color=CREAM):
        self.event_message = msg
        self.event_color = color
        self.event_timer = 3500
        self.event_queue.append((msg, color, 3500))
