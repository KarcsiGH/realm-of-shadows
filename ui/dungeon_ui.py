"""
Realm of Shadows — Dungeon UI (Wizardry-style First-Person 3D)

Renders a pseudo-3D first-person view of the dungeon.
The player sees walls, corridors, doors, and objects from a
first-person perspective, like Wizardry or Eye of the Beholder.
"""
import pygame
import math
import time
from ui.renderer import *
from data.dungeon import (
    DungeonState, PASSABLE_TILES,
    DT_WALL, DT_FLOOR, DT_CORRIDOR, DT_DOOR, DT_STAIRS_DOWN,
    DT_STAIRS_UP, DT_TREASURE, DT_TRAP, DT_ENTRANCE,
)

# ═══════════════════════════════════════════════════════════════
#  3D VIEWPORT
# ═══════════════════════════════════════════════════════════════

VP_X = 40           # viewport left edge
VP_Y = 50           # viewport top edge
VP_W = 720          # viewport width
VP_H = 580          # viewport height
VP_CX = VP_X + VP_W // 2   # center x
VP_CY = VP_Y + VP_H // 2   # center y

VIEW_DEPTH = 4      # how many tiles ahead to render

# Direction vectors: N, E, S, W
DIR_DX = [0, 1, 0, -1]
DIR_DY = [-1, 0, 1, 0]
DIR_NAMES = ["North", "East", "South", "West"]

# Theme color palettes
THEME_COLORS = {
    "cave": {
        "wall":      (65, 55, 45),
        "wall_dark":  (40, 34, 28),
        "wall_line":  (80, 68, 55),
        "floor":     (50, 44, 36),
        "ceiling":   (35, 30, 25),
        "fog":       (12, 10, 8),
    },
    "mine": {
        "wall":      (72, 62, 48),
        "wall_dark":  (48, 40, 30),
        "wall_line":  (88, 76, 58),
        "floor":     (55, 48, 38),
        "ceiling":   (38, 32, 26),
        "fog":       (10, 8, 6),
    },
    "crypt": {
        "wall":      (52, 55, 68),
        "wall_dark":  (32, 35, 48),
        "wall_line":  (65, 68, 82),
        "floor":     (40, 42, 52),
        "ceiling":   (25, 28, 38),
        "fog":       (8, 8, 14),
    },
    "ruins": {
        "wall":      (75, 65, 50),
        "wall_dark":  (50, 42, 32),
        "wall_line":  (90, 78, 60),
        "floor":     (58, 50, 40),
        "ceiling":   (40, 34, 28),
        "fog":       (10, 8, 6),
    },
}

DOOR_COL        = (130, 90, 40)
DOOR_DARK       = (90, 60, 25)
STAIRS_DOWN_COL = (180, 160, 60)
STAIRS_UP_COL   = (80, 180, 220)
TREASURE_COL    = (255, 215, 0)
TREASURE_OPEN   = (120, 100, 50)
ENTRANCE_COL    = (100, 200, 100)


class DungeonUI:
    """First-person 3D dungeon renderer."""

    def __init__(self, dungeon_state):
        self.dungeon = dungeon_state
        self.theme = THEME_COLORS.get(dungeon_state.theme, THEME_COLORS["cave"])
        self.facing = 0  # 0=N, 1=E, 2=S, 3=W
        self.event_message = ""
        self.event_timer = 0
        self.event_color = CREAM
        self.show_camp_confirm = False
        self.show_stairs_confirm = False
        self.stairs_direction = None

    def draw(self, surface, mx, my, dt):
        self.event_timer = max(0, self.event_timer - dt)
        surface.fill(self.theme["fog"])

        # Draw the 3D viewport
        self._draw_3d_view(surface)

        # Draw minimap
        self._draw_minimap(surface)

        # HUD
        self._draw_hud(surface, mx, my)

        # Dialogs
        if self.show_camp_confirm:
            self._draw_camp_dialog(surface, mx, my)
        if self.show_stairs_confirm:
            self._draw_stairs_dialog(surface, mx, my)

        # Event message
        if self.event_message and self.event_timer > 0:
            msg_rect = pygame.Rect(VP_X + VP_W // 2 - 280, VP_Y + VP_H // 2 - 35, 560, 70)
            pygame.draw.rect(surface, (15, 12, 30), msg_rect, border_radius=5)
            pygame.draw.rect(surface, GOLD, msg_rect, 2, border_radius=5)
            draw_text(surface, self.event_message,
                      msg_rect.x + 20, msg_rect.y + 12, self.event_color, 16,
                      max_width=msg_rect.width - 40)

    # ─────────────────────────────────────────────────────────
    #  3D RENDERING — Wide-angle corridor view
    # ─────────────────────────────────────────────────────────

    def _get_wall_rect(self, depth, lateral):
        """Get screen rectangle for a tile position relative to player.
        depth: 0=player tile, 1=one ahead, etc.
        lateral: -2,-1,0,1,2 = left to right of center
        Returns (left, top, width, height) in screen coords, or None."""
        # Perspective scaling: each depth step shrinks toward vanishing point
        # We define "slots" — screen columns for each lateral position at each depth

        # Near and far edges for this depth
        def scale_at(d):
            """Returns (half_width_fraction, half_height_fraction) at depth d."""
            if d <= 0:
                return 1.0, 1.0
            t = 1.0 / (d * 0.65 + 1.0)
            return t, t

        sw, sh = scale_at(depth)
        sw_far, sh_far = scale_at(depth + 1)

        # Total corridor width at this depth (fraction of viewport)
        # At depth 0, fills viewport. At depth 4, small rectangle in center.
        near_half_w = VP_W * sw / 2
        near_half_h = VP_H * sh / 2
        far_half_w = VP_W * sw_far / 2
        far_half_h = VP_H * sh_far / 2

        # Each "tile column" at this depth occupies a fraction of the corridor width
        # Center tile (lateral=0) occupies the middle third
        tile_frac = sw / 3.0  # each tile = 1/3 of width at this depth

        cx = VP_CX + lateral * (VP_W * tile_frac)
        left = cx - VP_W * tile_frac / 2
        top = VP_CY - near_half_h
        w = VP_W * tile_frac
        h = near_half_h * 2

        return int(left), int(top), int(w), int(h)

    def _draw_3d_view(self, surface):
        """Render pseudo-3D first-person corridor view."""
        # Clip to viewport
        surface.set_clip(pygame.Rect(VP_X, VP_Y, VP_W, VP_H))

        # Background: ceiling and floor with gradients
        pygame.draw.rect(surface, self.theme["ceiling"], (VP_X, VP_Y, VP_W, VP_H // 2))
        pygame.draw.rect(surface, self.theme["floor"], (VP_X, VP_Y + VP_H // 2, VP_W, VP_H // 2))

        for i in range(10):
            y = VP_Y + VP_H // 2 + i * (VP_H // 20)
            bright = max(0.15, 1.0 - i * 0.08)
            col = tuple(int(c * bright) for c in self.theme["floor"])
            pygame.draw.rect(surface, col, (VP_X, y, VP_W, VP_H // 20 + 1))

        for i in range(10):
            y = VP_Y + VP_H // 2 - (i + 1) * (VP_H // 20)
            bright = max(0.15, 1.0 - i * 0.08)
            col = tuple(int(c * bright) for c in self.theme["ceiling"])
            pygame.draw.rect(surface, col, (VP_X, y, VP_W, VP_H // 20 + 1))

        # Direction vectors
        fdx = DIR_DX[self.facing]
        fdy = DIR_DY[self.facing]
        rdx = DIR_DX[(self.facing + 1) % 4]  # right
        rdy = DIR_DY[(self.facing + 1) % 4]

        px, py = self.dungeon.party_x, self.dungeon.party_y

        # Render back to front (depth 4 down to 1)
        for depth in range(VIEW_DEPTH, 0, -1):
            self._render_slice(surface, px, py, fdx, fdy, rdx, rdy, depth)

        # Current tile objects
        self._draw_current_tile_items(surface)

        # Remove clip
        surface.set_clip(None)

        # Viewport border
        pygame.draw.rect(surface, PANEL_BORDER, (VP_X, VP_Y, VP_W, VP_H), 2)

        # Torch flicker
        t = time.time()
        flicker = int(abs(math.sin(t * 6)) * 8)
        torch_surf = pygame.Surface((VP_W, VP_H), pygame.SRCALPHA)
        # Radial-ish glow: brighter in center
        for ring in range(3):
            r = VP_W // 2 - ring * 80
            alpha = flicker + ring * 2
            if r > 0:
                pygame.draw.ellipse(torch_surf, (200, 150, 50, alpha),
                                    (VP_W // 2 - r, VP_H // 2 - r, r * 2, r * 2))
        surface.blit(torch_surf, (VP_X, VP_Y))

    def _render_slice(self, surface, px, py, fdx, fdy, rdx, rdy, depth):
        """Render one depth slice: center, left, right walls and passages."""
        brightness = max(0.2, 1.0 - depth * 0.18)

        # Perspective parameters
        def near_far(d):
            near = 1.0 / (d * 0.6 + 0.8)
            far = 1.0 / ((d + 1) * 0.6 + 0.8)
            return near, far

        near_s, far_s = near_far(depth - 1)

        # Screen coordinates for the "corridor" at this depth
        # Near edge (closer to player)
        n_left = VP_CX - int(VP_W * near_s / 2)
        n_right = VP_CX + int(VP_W * near_s / 2)
        n_top = VP_CY - int(VP_H * near_s / 2)
        n_bot = VP_CY + int(VP_H * near_s / 2)

        # Far edge (further from player)
        f_left = VP_CX - int(VP_W * far_s / 2)
        f_right = VP_CX + int(VP_W * far_s / 2)
        f_top = VP_CY - int(VP_H * far_s / 2)
        f_bot = VP_CY + int(VP_H * far_s / 2)

        # World positions at this depth
        cx = px + fdx * depth
        cy = py + fdy * depth

        center = self._get_type(cx, cy)
        left = self._get_type(cx - rdx, cy - rdy)
        right = self._get_type(cx + rdx, cy + rdy)
        far_left = self._get_type(cx - rdx * 2, cy - rdy * 2)
        far_right = self._get_type(cx + rdx * 2, cy + rdy * 2)

        # ── Front wall if center is blocked ──
        if center == DT_WALL or center is None:
            self._draw_front_wall(surface, f_left, f_top,
                                  f_right - f_left, f_bot - f_top, brightness)
            return

        # ── Left side wall ──
        if left == DT_WALL or left is None:
            # Solid left wall
            pts = [(n_left, n_top), (f_left, f_top), (f_left, f_bot), (n_left, n_bot)]
            wall_col = self._dim(self.theme["wall_dark"], brightness * 0.8)
            pygame.draw.polygon(surface, wall_col, pts)
            # Mortar lines
            line_col = self._dim(self.theme["wall_line"], brightness * 0.6)
            for i in range(1, 4):
                frac = i / 4
                ly1 = n_top + int((n_bot - n_top) * frac)
                ly2 = f_top + int((f_bot - f_top) * frac)
                pygame.draw.line(surface, line_col, (n_left, ly1), (f_left, ly2), 1)
        else:
            # Open passage on left — draw passage opening
            # Back wall of the passage
            pass_w = n_left - f_left
            if pass_w > 4:
                # Floor/ceiling of side passage
                floor_col = self._dim(self.theme["floor"], brightness * 0.6)
                ceil_col = self._dim(self.theme["ceiling"], brightness * 0.6)
                mid_y = (n_top + n_bot) // 2
                pygame.draw.rect(surface, ceil_col, (f_left, f_top, n_left - f_left, mid_y - f_top))
                pygame.draw.rect(surface, floor_col, (f_left, mid_y, n_left - f_left, f_bot - mid_y))
                # If the tile beyond the passage is a wall, draw its face
                if far_left == DT_WALL or far_left is None:
                    back_col = self._dim(self.theme["wall"], brightness * 0.5)
                    pygame.draw.rect(surface, back_col, (f_left, f_top, max(2, pass_w // 3), f_bot - f_top))

        # ── Right side wall ──
        if right == DT_WALL or right is None:
            pts = [(n_right, n_top), (f_right, f_top), (f_right, f_bot), (n_right, n_bot)]
            wall_col = self._dim(self.theme["wall"], brightness * 0.9)
            pygame.draw.polygon(surface, wall_col, pts)
            line_col = self._dim(self.theme["wall_line"], brightness * 0.7)
            for i in range(1, 4):
                frac = i / 4
                ly1 = n_top + int((n_bot - n_top) * frac)
                ly2 = f_top + int((f_bot - f_top) * frac)
                pygame.draw.line(surface, line_col, (n_right, ly1), (f_right, ly2), 1)
        else:
            pass_w = f_right - n_right
            if pass_w > 4:
                floor_col = self._dim(self.theme["floor"], brightness * 0.6)
                ceil_col = self._dim(self.theme["ceiling"], brightness * 0.6)
                mid_y = (n_top + n_bot) // 2
                pygame.draw.rect(surface, ceil_col, (n_right, f_top, f_right - n_right, mid_y - f_top))
                pygame.draw.rect(surface, floor_col, (n_right, mid_y, f_right - n_right, f_bot - mid_y))
                if far_right == DT_WALL or far_right is None:
                    back_col = self._dim(self.theme["wall"], brightness * 0.5)
                    bx = f_right - max(2, pass_w // 3)
                    pygame.draw.rect(surface, back_col, (bx, f_top, f_right - bx, f_bot - f_top))

        # ── Objects at this depth ──
        tile = self.dungeon.get_tile(cx, cy)
        if tile:
            obj_w = f_right - f_left
            obj_h = f_bot - f_top
            self._draw_tile_object(surface, tile, f_left, f_top,
                                   obj_w, obj_h, brightness, depth)

    def _get_type(self, x, y):
        """Get tile type at position, or None if out of bounds."""
        tile = self.dungeon.get_tile(x, y)
        if tile is None:
            return None
        return tile["type"]

    def _dim(self, color, factor):
        """Dim a color by a factor."""
        return tuple(max(0, min(255, int(c * factor))) for c in color)

    def _draw_front_wall(self, surface, x, y, w, h, brightness):
        """Draw a wall facing the player."""
        col = self._dim(self.theme["wall"], brightness)
        dark = self._dim(self.theme["wall_dark"], brightness)
        line_col = self._dim(self.theme["wall_line"], brightness)

        pygame.draw.rect(surface, col, (x, y, w, h))

        # Brick/stone pattern
        brick_h = max(6, h // 6)
        for by in range(0, h, brick_h):
            offset = (brick_h // 2) if (by // brick_h) % 2 == 0 else 0
            for bx in range(offset, w, brick_h * 2):
                bw = min(brick_h * 2 - 2, w - bx)
                if bw > 4:
                    pygame.draw.rect(surface, dark, (x + bx, y + by, bw, brick_h - 2), 1)

        for by in range(0, h, brick_h):
            pygame.draw.line(surface, line_col, (x, y + by), (x + w, y + by), 1)

    def _draw_tile_object(self, surface, tile, x, y, w, h, brightness, depth):
        """Draw special objects at a depth (doors, stairs, treasure)."""
        tile_type = tile["type"]

        if tile_type == DT_DOOR:
            # Door frame and panels
            dw = int(w * 0.5)
            dh = int(h * 0.7)
            dx = x + (w - dw) // 2
            dy = y + h - dh
            frame_col = tuple(int(c * brightness) for c in DOOR_DARK)
            door_col = tuple(int(c * brightness) for c in DOOR_COL)
            pygame.draw.rect(surface, frame_col, (dx - 3, dy - 3, dw + 6, dh + 3))
            pygame.draw.rect(surface, door_col, (dx, dy, dw, dh))
            # Panels
            pw = dw // 2 - 4
            ph = dh // 2 - 4
            panel_dark = tuple(max(0, c - 20) for c in door_col)
            pygame.draw.rect(surface, panel_dark, (dx + 3, dy + 3, pw, ph))
            pygame.draw.rect(surface, panel_dark, (dx + dw - pw - 3, dy + 3, pw, ph))
            pygame.draw.rect(surface, panel_dark, (dx + 3, dy + dh - ph - 3, pw, ph))
            pygame.draw.rect(surface, panel_dark, (dx + dw - pw - 3, dy + dh - ph - 3, pw, ph))
            # Handle
            handle_y = dy + dh // 2
            pygame.draw.circle(surface, (200, 180, 80),
                               (dx + dw - max(8, dw // 6), handle_y), max(2, dw // 16))

        elif tile_type == DT_STAIRS_DOWN:
            # Descending stairs visual
            step_w = int(w * 0.4)
            step_h = max(4, h // 8)
            sx = x + (w - step_w) // 2
            for i in range(min(4, h // step_h)):
                sy = y + h - (i + 1) * step_h
                col = tuple(int(c * brightness * (1 - i * 0.15)) for c in STAIRS_DOWN_COL)
                pygame.draw.rect(surface, col, (sx + i * 3, sy, step_w - i * 6, step_h))

        elif tile_type == DT_STAIRS_UP:
            step_w = int(w * 0.4)
            step_h = max(4, h // 8)
            sx = x + (w - step_w) // 2
            for i in range(min(4, h // step_h)):
                sy = y + i * step_h
                col = tuple(int(c * brightness * (1 - i * 0.15)) for c in STAIRS_UP_COL)
                pygame.draw.rect(surface, col, (sx + i * 3, sy, step_w - i * 6, step_h))

        elif tile_type == DT_ENTRANCE:
            # Archway
            aw = int(w * 0.5)
            ah = int(h * 0.7)
            ax = x + (w - aw) // 2
            ay = y + h - ah
            col = tuple(int(c * brightness) for c in ENTRANCE_COL)
            pygame.draw.arc(surface, col, (ax, ay, aw, ah // 2), 0, 3.14, 3)
            pygame.draw.line(surface, col, (ax, ay + ah // 4), (ax, y + h), 3)
            pygame.draw.line(surface, col, (ax + aw, ay + ah // 4), (ax + aw, y + h), 3)

        elif tile_type == DT_TREASURE:
            ev = tile.get("event") or {}
            opened = ev.get("opened", False)
            cw = int(w * 0.25)
            ch = int(h * 0.2)
            cx_t = x + (w - cw) // 2
            cy_t = y + h - ch - int(h * 0.1)
            base_col = TREASURE_OPEN if opened else TREASURE_COL
            col = tuple(int(c * brightness) for c in base_col)
            dark = tuple(max(0, int(c * brightness) - 30) for c in base_col)
            pygame.draw.rect(surface, col, (cx_t, cy_t, cw, ch))
            if not opened:
                pygame.draw.rect(surface, dark, (cx_t, cy_t, cw, ch // 3))
                # Lock
                lock_col = tuple(int(c * brightness) for c in (200, 180, 80))
                pygame.draw.circle(surface, lock_col,
                                   (cx_t + cw // 2, cy_t + ch // 3), max(2, cw // 10))

    def _draw_current_tile_items(self, surface):
        """Draw indicators for items on the current tile."""
        tile = self.dungeon.get_tile(self.dungeon.party_x, self.dungeon.party_y)
        if not tile:
            return
        t = tile["type"]
        # Show small text indicator at bottom of viewport
        if t == DT_STAIRS_DOWN:
            draw_text(surface, "▼ Stairs Down ▼",
                      VP_CX - 60, VP_Y + VP_H - 30, STAIRS_DOWN_COL, 16, bold=True)
        elif t in (DT_STAIRS_UP, DT_ENTRANCE):
            label = "▲ Exit ▲" if self.dungeon.current_floor == 1 else "▲ Stairs Up ▲"
            draw_text(surface, label,
                      VP_CX - 50, VP_Y + VP_H - 30, STAIRS_UP_COL, 16, bold=True)

    # ─────────────────────────────────────────────────────────
    #  MINIMAP
    # ─────────────────────────────────────────────────────────

    def _draw_minimap(self, surface):
        """Draw automap in right panel."""
        floor = self.dungeon.get_current_floor_data()
        fw, fh = floor["width"], floor["height"]

        mm_area_w = SCREEN_W - VP_X - VP_W - 30
        mm_area_h = 340
        mm_x = VP_X + VP_W + 15
        mm_y = VP_Y + 90

        mm_scale = min(mm_area_w / fw, mm_area_h / fh)
        mm_w = int(fw * mm_scale)
        mm_h = int(fh * mm_scale)

        # Background
        bg = pygame.Rect(mm_x - 3, mm_y - 3, mm_w + 6, mm_h + 6)
        pygame.draw.rect(surface, (8, 6, 12), bg, border_radius=3)
        pygame.draw.rect(surface, PANEL_BORDER, bg, 1, border_radius=3)

        for y in range(fh):
            for x in range(fw):
                tile = floor["tiles"][y][x]
                if not tile["discovered"]:
                    continue
                px = mm_x + int(x * mm_scale)
                py_m = mm_y + int(y * mm_scale)
                s = max(1, int(mm_scale))
                t = tile["type"]
                if t == DT_WALL:
                    col = (50, 45, 40)
                elif t in (DT_FLOOR, DT_CORRIDOR):
                    col = (110, 100, 85)
                elif t == DT_DOOR:
                    col = (140, 100, 50)
                elif t == DT_STAIRS_DOWN:
                    col = STAIRS_DOWN_COL
                elif t in (DT_STAIRS_UP, DT_ENTRANCE):
                    col = STAIRS_UP_COL
                elif t == DT_TREASURE:
                    opened = (tile.get("event") or {}).get("opened", False)
                    col = TREASURE_OPEN if opened else TREASURE_COL
                elif t == DT_TRAP:
                    col = (200, 60, 60) if (tile.get("event") or {}).get("detected") else (110, 100, 85)
                else:
                    col = (80, 72, 60)
                pygame.draw.rect(surface, col, (px, py_m, s, s))

        # Party position and facing arrow
        ppx = mm_x + int(self.dungeon.party_x * mm_scale)
        ppy = mm_y + int(self.dungeon.party_y * mm_scale)
        pygame.draw.rect(surface, (255, 255, 80), (ppx - 1, ppy - 1, 3, 3))
        # Facing indicator
        fdx = DIR_DX[self.facing]
        fdy = DIR_DY[self.facing]
        pygame.draw.line(surface, (255, 100, 100),
                         (ppx + 1, ppy + 1),
                         (ppx + 1 + fdx * 4, ppy + 1 + fdy * 4), 2)

    # ─────────────────────────────────────────────────────────
    #  HUD
    # ─────────────────────────────────────────────────────────

    def _draw_hud(self, surface, mx, my):
        # Top bar
        top_bar = pygame.Rect(0, 0, SCREEN_W, 44)
        pygame.draw.rect(surface, (12, 10, 24), top_bar)
        pygame.draw.line(surface, PANEL_BORDER, (0, 44), (SCREEN_W, 44))

        draw_text(surface, self.dungeon.name, 15, 6, GOLD, 18, bold=True)
        draw_text(surface, f"Floor {self.dungeon.current_floor}/{self.dungeon.total_floors}  |  Facing {DIR_NAMES[self.facing]}",
                  15, 26, CREAM, 13)

        # Party HP in right panel area
        rp_x = VP_X + VP_W + 15
        draw_text(surface, "Party", rp_x, VP_Y, GOLD, 16, bold=True)
        for i, c in enumerate(self.dungeon.party):
            from core.classes import get_all_resources
            max_res = get_all_resources(c.class_name, c.stats, c.level)
            hp = c.resources.get("HP", 0)
            max_hp = max_res.get("HP", 1)
            hp_pct = hp / max_hp if max_hp > 0 else 0
            hp_col = GREEN if hp_pct > 0.5 else ORANGE if hp_pct > 0.25 else RED
            cy = VP_Y + 22 + i * 18
            name_short = c.name[:8]
            draw_text(surface, f"{name_short}", rp_x, cy, CREAM, 12)
            draw_text(surface, f"{hp}/{max_hp}", rp_x + 90, cy, hp_col, 12)

        # Current tile info
        tile = self.dungeon.get_tile(self.dungeon.party_x, self.dungeon.party_y)
        if tile:
            t = tile["type"]
            if t == DT_STAIRS_DOWN:
                draw_text(surface, "ENTER to descend",
                          VP_X + 10, VP_Y + VP_H + 8, STAIRS_DOWN_COL, 14)
            elif t in (DT_STAIRS_UP, DT_ENTRANCE):
                label = "ENTER to exit" if self.dungeon.current_floor == 1 else "ENTER to ascend"
                draw_text(surface, label, VP_X + 10, VP_Y + VP_H + 8, STAIRS_UP_COL, 14)

        # Bottom buttons
        btn_y = SCREEN_H - 55
        camp_btn = pygame.Rect(VP_X, btn_y, 120, 42)
        draw_button(surface, camp_btn, "Camp",
                    hover=camp_btn.collidepoint(mx, my), size=15)

        menu_btn = pygame.Rect(VP_X + 140, btn_y, 120, 42)
        draw_button(surface, menu_btn, "Menu",
                    hover=menu_btn.collidepoint(mx, my), size=15)

        # Direction buttons
        turn_l = pygame.Rect(VP_X + 280, btn_y, 100, 42)
        draw_button(surface, turn_l, "◄ Turn",
                    hover=turn_l.collidepoint(mx, my), size=14)

        turn_r = pygame.Rect(VP_X + 400, btn_y, 100, 42)
        draw_button(surface, turn_r, "Turn ►",
                    hover=turn_r.collidepoint(mx, my), size=14)

        # Controls hint
        draw_text(surface, "↑/W = Forward  ↓/S = Back  ←/→ or Q/E = Turn  C = Camp  ENTER = Interact",
                  VP_X, SCREEN_H - 8, DARK_GREY, 11)

    def _draw_camp_dialog(self, surface, mx, my):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        surface.blit(overlay, (0, 0))

        dlg = pygame.Rect(SCREEN_W // 2 - 220, SCREEN_H // 2 - 100, 440, 200)
        pygame.draw.rect(surface, (20, 16, 36), dlg, border_radius=5)
        pygame.draw.rect(surface, GOLD, dlg, 2, border_radius=5)

        draw_text(surface, "Camp in the Dungeon?", dlg.x + 100, dlg.y + 15, GOLD, 22, bold=True)
        draw_text(surface, "Restores ~25% HP and ~15% MP/SP.", dlg.x + 20, dlg.y + 55, CREAM, 14)
        draw_text(surface, "Higher ambush risk than the surface!",
                  dlg.x + 20, dlg.y + 80, ORANGE, 14)

        yes_btn = pygame.Rect(dlg.x + 60, dlg.y + 140, 140, 40)
        draw_button(surface, yes_btn, "Rest", hover=yes_btn.collidepoint(mx, my), size=16)
        no_btn = pygame.Rect(dlg.x + 240, dlg.y + 140, 140, 40)
        draw_button(surface, no_btn, "Cancel", hover=no_btn.collidepoint(mx, my), size=16)

    def _draw_stairs_dialog(self, surface, mx, my):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        surface.blit(overlay, (0, 0))

        dlg = pygame.Rect(SCREEN_W // 2 - 200, SCREEN_H // 2 - 80, 400, 160)
        pygame.draw.rect(surface, (20, 16, 36), dlg, border_radius=5)
        pygame.draw.rect(surface, GOLD, dlg, 2, border_radius=5)

        if self.stairs_direction == "down":
            text = f"Descend to Floor {self.dungeon.current_floor + 1}?"
            col = STAIRS_DOWN_COL
        elif self.stairs_direction == "exit":
            text = "Exit the dungeon?"
            col = ENTRANCE_COL
        else:
            text = f"Ascend to Floor {self.dungeon.current_floor - 1}?"
            col = STAIRS_UP_COL

        draw_text(surface, text, dlg.x + 80, dlg.y + 20, col, 20, bold=True)

        yes_btn = pygame.Rect(dlg.x + 40, dlg.y + 100, 140, 40)
        draw_button(surface, yes_btn, "Yes", hover=yes_btn.collidepoint(mx, my), size=16)
        no_btn = pygame.Rect(dlg.x + 220, dlg.y + 100, 140, 40)
        draw_button(surface, no_btn, "No", hover=no_btn.collidepoint(mx, my), size=16)

    # ─────────────────────────────────────────────────────────
    #  INPUT
    # ─────────────────────────────────────────────────────────

    def handle_key(self, key):
        if self.show_camp_confirm or self.show_stairs_confirm:
            return None

        # Forward/backward movement (relative to facing)
        if key in (pygame.K_UP, pygame.K_w):
            dx = DIR_DX[self.facing]
            dy = DIR_DY[self.facing]
            return self.dungeon.move(dx, dy)

        elif key in (pygame.K_DOWN, pygame.K_s):
            # Move backward
            dx = -DIR_DX[self.facing]
            dy = -DIR_DY[self.facing]
            return self.dungeon.move(dx, dy)

        elif key in (pygame.K_LEFT, pygame.K_q):
            # Turn left
            self.facing = (self.facing - 1) % 4
            return None

        elif key in (pygame.K_RIGHT, pygame.K_e):
            # Turn right
            self.facing = (self.facing + 1) % 4
            return None

        elif key in (pygame.K_a,):
            # Strafe left
            lf = (self.facing - 1) % 4
            return self.dungeon.move(DIR_DX[lf], DIR_DY[lf])

        elif key in (pygame.K_d,):
            # Strafe right
            rf = (self.facing + 1) % 4
            return self.dungeon.move(DIR_DX[rf], DIR_DY[rf])

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

        return None

    def handle_click(self, mx, my):
        if self.show_stairs_confirm:
            dlg = pygame.Rect(SCREEN_W // 2 - 200, SCREEN_H // 2 - 80, 400, 160)
            yes_btn = pygame.Rect(dlg.x + 40, dlg.y + 100, 140, 40)
            no_btn = pygame.Rect(dlg.x + 220, dlg.y + 100, 140, 40)
            if yes_btn.collidepoint(mx, my):
                self.show_stairs_confirm = False
                if self.stairs_direction == "down":
                    return {"type": "stairs_down"}
                elif self.stairs_direction == "up":
                    return {"type": "stairs_up"}
                else:
                    return {"type": "exit_dungeon"}
            elif no_btn.collidepoint(mx, my):
                self.show_stairs_confirm = False
            return None

        if self.show_camp_confirm:
            dlg = pygame.Rect(SCREEN_W // 2 - 220, SCREEN_H // 2 - 100, 440, 200)
            yes_btn = pygame.Rect(dlg.x + 60, dlg.y + 140, 140, 40)
            no_btn = pygame.Rect(dlg.x + 240, dlg.y + 140, 140, 40)
            if yes_btn.collidepoint(mx, my):
                self.show_camp_confirm = False
                return {"type": "camp"}
            elif no_btn.collidepoint(mx, my):
                self.show_camp_confirm = False
            return None

        btn_y = SCREEN_H - 55

        camp_btn = pygame.Rect(VP_X, btn_y, 120, 42)
        if camp_btn.collidepoint(mx, my):
            self.show_camp_confirm = True
            return None

        menu_btn = pygame.Rect(VP_X + 140, btn_y, 120, 42)
        if menu_btn.collidepoint(mx, my):
            return {"type": "menu"}

        turn_l = pygame.Rect(VP_X + 280, btn_y, 100, 42)
        if turn_l.collidepoint(mx, my):
            self.facing = (self.facing - 1) % 4
            return None

        turn_r = pygame.Rect(VP_X + 400, btn_y, 100, 42)
        if turn_r.collidepoint(mx, my):
            self.facing = (self.facing + 1) % 4
            return None

        return None

    def show_event(self, msg, color=CREAM):
        self.event_message = msg
        self.event_color = color
        self.event_timer = 3000
