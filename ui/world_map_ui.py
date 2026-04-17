"""
Realm of Shadows — World Map UI

Pseudo-3D angled tile renderer (Dragon Warrior style).
Party token moves with arrow keys / WASD.
HUD shows location info, minimap, and camp/menu buttons.
"""
import pygame
import math
from ui.renderer import *
from data.world_map import (
    WorldState, TERRAIN_DATA, LOCATIONS, IMPASSABLE,
    T_GRASS, T_FOREST, T_DENSE_FOREST, T_MOUNTAIN, T_HILL,
    T_SWAMP, T_DESERT, T_SCRUBLAND, T_WATER, T_LAKE, T_RIVER,
    T_ROAD, T_BRIDGE, T_SHORE,
    LOC_TOWN, LOC_DUNGEON, LOC_POI, LOC_SECRET, LOC_PORT,
    MAP_W, MAP_H, PORT_ROUTES,
)
from core.classes import CLASSES

# ═══════════════════════════════════════════════════════════════
#  TILE RENDERING CONSTANTS
# ═══════════════════════════════════════════════════════════════

TILE_W = 56         # tile width in pixels
TILE_H = 40         # tile height (shorter = more angled look)
ELEVATION_PX = 6    # vertical offset per elevation level
VIEW_COLS = 22      # tiles visible horizontally
VIEW_ROWS = 16      # tiles visible vertically
MAP_OFFSET_X = 0
MAP_OFFSET_Y = 0

# Terrain colors: (base, accent, pattern_type)
TERRAIN_COLORS = {
    T_GRASS:        ((55, 140, 55),  (65, 160, 65),  "dots"),
    T_FOREST:       ((30, 95, 35),   (20, 75, 25),   "trees"),
    T_DENSE_FOREST: ((18, 65, 22),   (12, 50, 15),   "dense_trees"),
    T_MOUNTAIN:     ((110, 100, 90), (140, 130, 115), "peaks"),
    T_HILL:         ((90, 130, 70),  (100, 145, 80),  "gentle"),
    T_SWAMP:        ((50, 80, 40),   (35, 65, 30),    "wavy"),
    T_DESERT:       ((190, 170, 110),(210, 190, 130),  "sand"),
    T_SCRUBLAND:    ((140, 150, 80), (120, 135, 70),   "scrub"),
    T_WATER:        ((30, 60, 140),  (25, 50, 120),   "waves"),
    T_LAKE:         ((35, 75, 155),  (30, 65, 140),   "waves"),
    T_RIVER:        ((40, 80, 160),  (50, 95, 180),   "flow"),
    T_ROAD:         ((140, 120, 80), (160, 140, 95),   "path"),
    T_BRIDGE:       ((120, 90, 50),  (100, 75, 40),    "planks"),
    T_SHORE:        ((170, 160, 110),(140, 130, 90),   "sand"),
}

FOG_COLOR       = (8, 6, 16)
FOG_DIM         = (20, 16, 30)
PARTY_COLOR     = (255, 255, 80)
PARTY_OUTLINE   = (200, 160, 0)
LOC_TOWN_COL    = (255, 220, 80)
LOC_DUNGEON_COL = (200, 60, 60)
LOC_POI_COL     = (80, 200, 255)
LOC_SECRET_COL  = (180, 120, 255)
LOC_PORT_COL    = (80, 180, 220)

HUD_BG          = (12, 10, 24, 200)


class WorldMapUI:
    """Renders the world map and handles movement input."""

    def __init__(self, world_state):
        self.world = world_state
        self.event_message = ""
        self.event_timer = 0
        self.event_color = CREAM
        self.show_camp_confirm = False
        self.port_modal        = None   # {"loc_id", "loc", "routes", "hover_idx"}

    def draw(self, surface, mx, my, dt):
        self.event_timer = max(0, self.event_timer - dt)
        surface.fill(FOG_COLOR)

        visible = self.world.get_visible_tiles(VIEW_COLS, VIEW_ROWS)

        # ── Render tiles back-to-front for overlap ──
        for vy, row in enumerate(visible):
            for vx, tile_data in enumerate(row):
                self._draw_tile(surface, vx, vy, tile_data)

        # ── Draw party token ──
        self._draw_party(surface)

        # ── HUD overlay ──
        self._draw_hud(surface, mx, my)

        # ── Camp confirmation dialog ──
        if self.show_camp_confirm:
            self._draw_camp_dialog(surface, mx, my)

        # ── Port destination picker ──
        if self.port_modal:
            self._draw_port_modal(surface, mx, my)

        # ── Fading world corruption overlay ──
        self._draw_fading_overlay(surface)

        # ── Event message ──
        if self.event_message and self.event_timer > 0:
            msg_rect = pygame.Rect(SCREEN_W // 2 - 300, SCREEN_H // 2 - 40, 600, 80)
            pygame.draw.rect(surface, (15, 12, 30), msg_rect, border_radius=5)
            pygame.draw.rect(surface, GOLD, msg_rect, 2, border_radius=5)
            draw_text(surface, self.event_message,
                      msg_rect.x + 20, msg_rect.y + 10, self.event_color, 16,
                      max_width=msg_rect.width - 40)

    def _draw_tile(self, surface, vx, vy, tile_data):
        """Draw a single tile with pseudo-3D offset."""
        if tile_data is None:
            return

        px = MAP_OFFSET_X + vx * TILE_W
        py = MAP_OFFSET_Y + vy * TILE_H

        terrain = tile_data["terrain"]
        discovered = tile_data["discovered"]
        is_party = tile_data["is_party"]

        # Fog of war
        if not discovered:
            pygame.draw.rect(surface, FOG_COLOR, (px, py, TILE_W, TILE_H))
            return

        # Check if currently visible (within sight range of party)
        wx, wy = tile_data["wx"], tile_data["wy"]
        dist = math.sqrt((wx - self.world.party_x) ** 2 + (wy - self.world.party_y) ** 2)
        current_sight = TERRAIN_DATA[self.world.get_current_tile()["terrain"]]["sight"]
        is_visible = dist <= current_sight

        # Get colors
        base_col, accent_col, pattern = TERRAIN_COLORS.get(
            terrain, ((80, 80, 80), (100, 100, 100), "dots")
        )

        # Dim if explored but not currently visible
        if not is_visible:
            base_col = tuple(max(0, c // 2) for c in base_col)
            accent_col = tuple(max(0, c // 2) for c in accent_col)

        # Elevation offset
        elev = TERRAIN_DATA[terrain]["elevation"]
        elev_offset = -elev * ELEVATION_PX

        tile_rect = pygame.Rect(px, py + elev_offset, TILE_W, TILE_H)

        # Draw base tile
        pygame.draw.rect(surface, base_col, tile_rect)

        # Draw side face for elevation (pseudo-3D)
        if elev > 0:
            side_h = elev * ELEVATION_PX
            side_col = tuple(max(0, c - 30) for c in base_col)
            side_rect = pygame.Rect(px, py + elev_offset + TILE_H, TILE_W, side_h)
            pygame.draw.rect(surface, side_col, side_rect)

        # Draw terrain patterns
        self._draw_terrain_detail(surface, px, py + elev_offset, terrain, accent_col, is_visible)

        # Tile border (subtle)
        border_col = tuple(max(0, c - 15) for c in base_col)
        pygame.draw.rect(surface, border_col, tile_rect, 1)

        # Location marker
        loc_id = tile_data.get("location_id")
        if loc_id and loc_id in LOCATIONS and loc_id in self.world.discovered_locations:
            loc = LOCATIONS[loc_id]
            self._draw_location_marker(surface, px, py + elev_offset, loc)

    def _draw_terrain_detail(self, surface, px, py, terrain, accent, is_visible):
        """Draw small details on tiles for visual variety."""
        if not is_visible:
            return  # don't draw details on dimmed tiles

        if terrain == T_FOREST:
            # Small triangle trees
            for ox, oy in [(12, 8), (35, 15), (22, 28)]:
                pts = [(px + ox, py + oy - 10), (px + ox - 6, py + oy + 2), (px + ox + 6, py + oy + 2)]
                pygame.draw.polygon(surface, accent, pts)

        elif terrain == T_DENSE_FOREST:
            for ox, oy in [(8, 6), (25, 5), (42, 8), (15, 22), (35, 25), (10, 35)]:
                pts = [(px + ox, py + oy - 8), (px + ox - 5, py + oy + 2), (px + ox + 5, py + oy + 2)]
                pygame.draw.polygon(surface, accent, pts)

        elif terrain == T_MOUNTAIN:
            # Peak triangles
            pts = [(px + 28, py + 2), (px + 14, py + 30), (px + 42, py + 30)]
            pygame.draw.polygon(surface, accent, pts)
            # Snow cap
            snow_pts = [(px + 28, py + 2), (px + 22, py + 12), (px + 34, py + 12)]
            pygame.draw.polygon(surface, (220, 220, 230), snow_pts)

        elif terrain == T_WATER:
            # Wave lines
            for oy in (12, 24):
                for ox in range(4, TILE_W - 4, 12):
                    pygame.draw.arc(surface, accent,
                                    (px + ox, py + oy, 10, 6), 0, 3.14, 1)

        elif terrain == T_RIVER:
            # Flow lines
            pygame.draw.line(surface, accent, (px + TILE_W // 2, py), (px + TILE_W // 2, py + TILE_H), 2)

        elif terrain == T_ROAD:
            # Dashed center line
            for oy in range(2, TILE_H - 2, 8):
                pygame.draw.rect(surface, accent, (px + TILE_W // 2 - 2, py + oy, 4, 4))

        elif terrain == T_HILL:
            # Gentle curve
            pygame.draw.arc(surface, accent, (px + 10, py + 10, 36, 20), 0, 3.14, 2)

        elif terrain == T_SWAMP:
            # Wavy lines
            for oy in (10, 25):
                for ox in range(6, TILE_W - 6, 14):
                    pygame.draw.arc(surface, accent,
                                    (px + ox, py + oy, 10, 6), 0, 3.14, 1)

    def _draw_location_marker(self, surface, px, py, loc):
        """Draw a distinct icon for each location type."""
        loc_type = loc["type"]
        is_capital = loc.get("is_capital", False)
        name = loc.get("name", "")

        # Base colors per type
        if loc_type == LOC_TOWN:
            col = LOC_TOWN_COL
        elif loc_type == LOC_DUNGEON:
            col = LOC_DUNGEON_COL
        elif loc_type == LOC_SECRET:
            col = LOC_SECRET_COL
        elif loc_type == LOC_PORT:
            col = LOC_PORT_COL
        else:
            col = LOC_POI_COL

        cx = px + TILE_W // 2
        cy = py + TILE_H // 2
        dark = tuple(max(0, c - 60) for c in col)

        if loc_type == LOC_TOWN:
            # House silhouette — roof triangle + square base
            sz = 14 if is_capital else 10
            # Base
            base = pygame.Rect(cx - sz//2, cy - sz//3, sz, sz//2 + 2)
            pygame.draw.rect(surface, dark, base)
            pygame.draw.rect(surface, col, base, 1)
            # Door
            dw, dh = max(2, sz//4), max(3, sz//3)
            pygame.draw.rect(surface, (40, 28, 16),
                             (cx - dw//2, base.bottom - dh, dw, dh))
            # Roof triangle
            roof_h = sz * 2 // 3
            roof_pts = [
                (cx - sz//2 - 2, cy - sz//3),
                (cx + sz//2 + 2, cy - sz//3),
                (cx, cy - sz//3 - roof_h),
            ]
            pygame.draw.polygon(surface, col, roof_pts)
            pygame.draw.polygon(surface, dark, roof_pts, 1)
            if is_capital:
                # Extra tower / banner
                pygame.draw.line(surface, (255, 220, 80), (cx, cy - sz//3 - roof_h),
                                 (cx, cy - sz//3 - roof_h - 6), 1)
                pygame.draw.polygon(surface, (255, 220, 80), [
                    (cx, cy - sz//3 - roof_h - 6),
                    (cx + 5, cy - sz//3 - roof_h - 3),
                    (cx, cy - sz//3 - roof_h),
                ])

        elif loc_type == LOC_DUNGEON:
            # Arch/skull entrance — pointed archway with dark interior
            sz = 12
            # Arch frame
            arch_rect = pygame.Rect(cx - sz//2, cy - sz//2, sz, sz)
            pygame.draw.rect(surface, dark, arch_rect)
            pygame.draw.rect(surface, col, arch_rect, 2)
            # Pointed arch interior
            inner = pygame.Rect(cx - sz//3, cy - sz//3 + 2, sz*2//3, sz*2//3)
            pygame.draw.ellipse(surface, (8, 4, 12), inner)
            # Skull dots (eye sockets)
            eye_y = cy - 2
            pygame.draw.circle(surface, col, (cx - 3, eye_y), 2)
            pygame.draw.circle(surface, col, (cx + 3, eye_y), 2)

        elif loc_type == LOC_PORT:
            # Anchor symbol
            sz = 10
            # Circle top
            pygame.draw.circle(surface, col, (cx, cy - sz//2), 3, 1)
            # Vertical shaft
            pygame.draw.line(surface, col, (cx, cy - sz//2 + 3), (cx, cy + sz//2), 2)
            # Horizontal crossbar
            pygame.draw.line(surface, col, (cx - sz//3, cy - sz//4),
                             (cx + sz//3, cy - sz//4), 2)
            # Flukes (curved ends)
            pygame.draw.arc(surface, col,
                            pygame.Rect(cx - sz//2, cy + sz//6, sz//2, sz//3),
                            math.pi, math.pi * 2, 1)
            pygame.draw.arc(surface, col,
                            pygame.Rect(cx, cy + sz//6, sz//2, sz//3),
                            0, math.pi, 1)

        elif loc_type == LOC_SECRET:
            # Question mark in a diamond
            sz = 10
            pts = [(cx, cy-sz), (cx+sz, cy), (cx, cy+sz), (cx-sz, cy)]
            pygame.draw.polygon(surface, (20, 14, 30), pts)
            pygame.draw.polygon(surface, col, pts, 1)
            draw_text(surface, "?", cx - 4, cy - 7, col, 12, bold=True)

        else:
            # POI — five-pointed star
            sz = 8
            star_pts = []
            for k in range(10):
                r_ = sz if k % 2 == 0 else sz // 2
                a  = math.pi * k / 5 - math.pi / 2
                star_pts.append((cx + int(r_ * math.cos(a)),
                                 cy + int(r_ * math.sin(a))))
            pygame.draw.polygon(surface, col, star_pts)
            pygame.draw.polygon(surface, dark, star_pts, 1)

        # Name labels removed — icons communicate location type clearly.
        # Name is shown in the HUD panel when the party stands on the location.

    def _draw_party(self, surface):
        """Draw the party token — animated cloaked figure with directional facing."""
        import time

        cx = MAP_OFFSET_X + (VIEW_COLS // 2) * TILE_W
        cy = MAP_OFFSET_Y + (VIEW_ROWS // 2) * TILE_H

        # Elevation offset
        tile = self.world.get_current_tile()
        elev = TERRAIN_DATA[tile["terrain"]]["elevation"]
        cy -= elev * ELEVATION_PX

        cx = cx + TILE_W // 2
        cy = cy + TILE_H // 2

        t = time.time()
        # Gentle bob: 2px up/down at ~1 Hz
        bob   = int(math.sin(t * 2.0) * 2)
        pulse = abs(math.sin(t * 2.5))

        facing_x = self.world.facing_dx if hasattr(self.world, "facing_dx") else 0
        facing_y = self.world.facing_dy if hasattr(self.world, "facing_dy") else -1
        # Normalise
        flen = math.sqrt(facing_x**2 + facing_y**2) or 1
        facing_x /= flen
        facing_y /= flen

        # ── Subtle glow ring beneath sprite ──────────────────────────
        glow_r = int(12 + pulse * 4)
        glow_surf = pygame.Surface((glow_r*2+6, glow_r*2+6), pygame.SRCALPHA)
        for gr in range(glow_r, glow_r - 5, -1):
            alpha = int(15 + (glow_r - gr) * 18)
            pygame.draw.circle(glow_surf, (*PARTY_OUTLINE, alpha),
                               (glow_r+3, glow_r+3), gr)
        surface.blit(glow_surf, (cx - glow_r - 3, cy - glow_r - 3 + bob))

        # ── Ultima-style pixel art party figure ───────────────────────
        # Map continuous facing vector to cardinal direction string
        if abs(facing_x) >= abs(facing_y):
            facing_str = "right" if facing_x >= 0 else "left"
        else:
            facing_str = "down" if facing_y >= 0 else "up"

        from ui.town_sprites import draw_party_figure
        draw_party_figure(surface, cx, cy + bob, TILE_H, facing_str)

    def _draw_hud(self, surface, mx, my):
        """Draw the HUD overlay with location info and buttons."""
        # Top bar — current location info
        top_bar = pygame.Rect(0, 0, SCREEN_W, 44)
        pygame.draw.rect(surface, (12, 10, 24), top_bar)
        pygame.draw.line(surface, PANEL_BORDER, (0, 44), (SCREEN_W, 44))

        tile = self.world.get_current_tile()
        terrain_name = TERRAIN_DATA[tile["terrain"]]["name"]
        region = tile["region"].replace("_", " ").title()
        draw_text(surface, f"{region} — {terrain_name}",
                  15, 12, CREAM, 16)

        # Coordinates
        draw_text(surface, f"({self.world.party_x}, {self.world.party_y})",
                  SCREEN_W // 2 - 30, 12, DARK_GREY, 14)

        # Location name if standing on one
        loc_id = tile.get("location_id")
        if loc_id and loc_id in LOCATIONS:
            loc = LOCATIONS[loc_id]
            loc_col = {LOC_TOWN: LOC_TOWN_COL, LOC_DUNGEON: LOC_DUNGEON_COL,
                       LOC_SECRET: LOC_SECRET_COL}.get(loc["type"], CREAM)
            draw_text(surface, loc["name"], SCREEN_W // 2 + 50, 12, loc_col, 16, bold=True)

        # Party gold
        total_gold = sum(c.gold for c in self.world.party)
        draw_text(surface, f"Gold: {total_gold}", SCREEN_W - 150, 12, DIM_GOLD, 14)

        # Travel mode indicator
        mode = self.world.travel.travel_mode.title()
        mode_col = GOLD if mode != "Walk" else GREY
        draw_text(surface, f"[{mode}]", SCREEN_W - 260, 12, mode_col, 14)

        # Bottom buttons
        btn_y = SCREEN_H - 55
        camp_btn = pygame.Rect(SCREEN_W - 320, btn_y, 140, 42)
        draw_button(surface, camp_btn, "Camp",
                    hover=camp_btn.collidepoint(mx, my), size=16)

        menu_btn = pygame.Rect(SCREEN_W - 160, btn_y, 140, 42)
        draw_button(surface, menu_btn, "Menu",
                    hover=menu_btn.collidepoint(mx, my), size=16)

        # Travel mode toggle button (if has horse or carpet)
        if self.world.travel.has_horse or self.world.travel.has_carpet:
            travel_btn = pygame.Rect(SCREEN_W - 480, btn_y, 140, 42)
            draw_button(surface, travel_btn, f"Mode: {mode}",
                        hover=travel_btn.collidepoint(mx, my), size=14)

        # Location-specific hints
        if loc_id and loc_id in LOCATIONS:
            loc = LOCATIONS[loc_id]
            if loc["type"] == LOC_TOWN:
                label = "★ CAPITAL — " if loc.get("is_capital") else ""
                draw_text(surface, f"{label}Press ENTER to enter town",
                          SCREEN_W // 2 - 120, SCREEN_H - 90, LOC_TOWN_COL, 15)
            elif loc["type"] == LOC_DUNGEON:
                can_enter, reason = self.world.can_enter_dungeon(loc_id)
                if can_enter:
                    draw_text(surface, "Press ENTER to enter dungeon",
                              SCREEN_W // 2 - 130, SCREEN_H - 90, LOC_DUNGEON_COL, 15)
                else:
                    # Word-wrap long lock messages so they don't run off the right edge.
                    # Use a centered block with a max width of 720px.
                    _msg_w = 720
                    _msg_x = SCREEN_W // 2 - _msg_w // 2
                    draw_text(surface, reason, _msg_x, SCREEN_H - 90, RED, 14,
                              max_width=_msg_w)
            elif loc["type"] == LOC_PORT:
                draw_text(surface, "Press ENTER to access port",
                          SCREEN_W // 2 - 120, SCREEN_H - 90, LOC_PORT_COL, 15)

        # Nearby undiscovered location hint — compass direction + distance
        import math as _math
        px, py = self.world.party_x, self.world.party_y
        best_hint = None
        best_dist = 999
        for _lid, _loc in LOCATIONS.items():
            if _lid in self.world.discovered_locations:
                continue
            req = _loc.get("required_key")
            if req and not self.world.has_key(req):
                continue
            _r = _loc.get("discovery_radius", 0)
            if _r <= 0:
                continue
            _dist = _math.sqrt((_loc["x"] - px)**2 + (_loc["y"] - py)**2)
            hint_dist = _r * 3   # show hint when within 3× discovery radius
            if _dist <= hint_dist and _dist < best_dist:
                best_dist = _dist
                dx = _loc["x"] - px; dy = _loc["y"] - py
                angle = _math.degrees(_math.atan2(dy, dx))
                dirs = ["E","SE","S","SW","W","NW","N","NE"]
                compass = dirs[int((angle + 22.5) / 45) % 8]
                best_hint = (f"Something lies to the {compass} ({int(_dist)} tiles away)",
                             (180, 200, 255))
        # Controls hint — bottom-left, clear of the Camp/Menu button row
        draw_text(surface, "Arrow keys / WASD  ·  C Camp  ·  M Menu",
                  15, SCREEN_H - 20, DARK_GREY, 12)

        if best_hint:
            draw_text(surface, best_hint[0], 15, SCREEN_H - 36, best_hint[1], 12)

        # Minimap
        self._draw_minimap(surface)

    def _draw_minimap(self, surface):
        """Draw a small minimap in the corner."""
        mm_size = 140
        mm_x = SCREEN_W - mm_size - 15
        mm_y = 55
        mm_scale = mm_size / max(MAP_W, MAP_H)

        # Background
        mm_rect = pygame.Rect(mm_x - 2, mm_y - 2, mm_size + 4, mm_size + 4)
        pygame.draw.rect(surface, (5, 4, 12), mm_rect)
        pygame.draw.rect(surface, PANEL_BORDER, mm_rect, 1)

        # Draw discovered tiles
        for y in range(MAP_H):
            for x in range(MAP_W):
                tile = self.world.tiles[y][x]
                if not tile["discovered"]:
                    continue

                terrain = tile["terrain"]
                base_col, _, _ = TERRAIN_COLORS.get(terrain, ((40, 40, 40), (40, 40, 40), ""))
                # Simplified color for minimap
                px = mm_x + int(x * mm_scale)
                py = mm_y + int(y * mm_scale)
                surface.set_at((px, py), base_col)

        # Draw discovered locations
        for loc_id in self.world.discovered_locations:
            if loc_id in LOCATIONS:
                loc = LOCATIONS[loc_id]
                lx = mm_x + int(loc["x"] * mm_scale)
                ly = mm_y + int(loc["y"] * mm_scale)
                col = {LOC_TOWN: LOC_TOWN_COL, LOC_DUNGEON: LOC_DUNGEON_COL,
                       LOC_SECRET: LOC_SECRET_COL}.get(loc["type"], WHITE)
                pygame.draw.rect(surface, col, (lx - 1, ly - 1, 3, 3))

        # Party position
        ppx = mm_x + int(self.world.party_x * mm_scale)
        ppy = mm_y + int(self.world.party_y * mm_scale)
        pygame.draw.rect(surface, PARTY_COLOR, (ppx - 2, ppy - 2, 4, 4))

    def _draw_fading_overlay(self, surface):
        """
        Draw a creeping Fading corruption overlay on the world map.
        Intensity rises with hearthstones collected (0-5).
        At 0: very faint edge vignette.
        At 5: heavy purple-black tide consuming the map edges.
        """
        import math, random
        from core.story_flags import hearthstone_count

        count     = hearthstone_count()
        # Base intensity: even with 0 stones there's a very light vignette
        intensity = 0.12 + count * 0.17   # 0.12 → 0.97 over 0-5 stones

        t = pygame.time.get_ticks() / 1000.0
        W, H = surface.get_size()

        # ── Edge vignette (always present, scaled by intensity) ──
        vig = pygame.Surface((W, H), pygame.SRCALPHA)
        depth = int(min(W, H) * intensity * 0.55)
        for i in range(depth):
            alpha = int(180 * intensity * ((depth - i) / depth) ** 1.8)
            alpha = min(220, alpha)
            col   = (20 + int(15 * intensity), 0, int(40 * intensity), alpha)
            # draw 1px border rect inset by i
            pygame.draw.rect(vig, col, (i, i, W - i*2, H - i*2), 1)
        surface.blit(vig, (0, 0))

        if count == 0:
            return   # pure vignette is enough at story start

        # ── Animated corruption tendrils along all four edges ──
        # Seeded per-frame so they wiggle but stay stable between frames
        rng    = random.Random(int(t * 2))   # changes twice per second
        stroke = pygame.Surface((W, H), pygame.SRCALPHA)

        def tendril(ox, oy, dx, dy, length, width, alpha):
            """Draw a single jagged tendril from (ox,oy) in direction (dx,dy)."""
            px, py = float(ox), float(oy)
            perp_x, perp_y = -dy, dx
            for _ in range(length):
                jitter = rng.uniform(-6, 6) * intensity
                nx = px + dx + perp_x * jitter
                ny = py + dy + perp_y * jitter
                a  = max(0, int(alpha * (1.0 - _ / length)))
                pygame.draw.line(stroke, (80, 0, 120, a),
                                 (int(px), int(py)), (int(nx), int(ny)), width)
                px, py = nx, ny

        # Number of tendrils scales with intensity
        n_edge = int(6 * intensity)
        step   = W // max(1, n_edge)
        fade_len = int(min(W, H) * intensity * 0.5)

        for i in range(n_edge):
            # Top edge
            ox = rng.randint(0, W)
            tendril(ox, 0, 0, 1, fade_len, 2, 120)
            # Bottom edge
            ox = rng.randint(0, W)
            tendril(ox, H, 0, -1, fade_len, 2, 120)
            # Left edge
            oy = rng.randint(0, H)
            tendril(0, oy, 1, 0, fade_len, 2, 100)
            # Right edge
            oy = rng.randint(0, H)
            tendril(W, oy, -1, 0, fade_len, 2, 100)

        surface.blit(stroke, (0, 0))

        # ── Pulsing dark bloom in corners at high intensity ──
        if count >= 3:
            bloom_alpha = int(80 * (count - 2) / 3 * (0.8 + 0.2 * math.sin(t * 0.9)))
            bloom       = pygame.Surface((W, H), pygame.SRCALPHA)
            bloom_r     = int(min(W, H) * 0.35 * ((count - 2) / 3))
            for cx, cy in [(0, 0), (W, 0), (0, H), (W, H)]:
                for ring in range(bloom_r, 0, -max(1, bloom_r // 12)):
                    a = int(bloom_alpha * (bloom_r - ring) / bloom_r)
                    pygame.draw.circle(bloom, (30, 0, 55, a), (cx, cy), ring)
            surface.blit(bloom, (0, 0))

    def _draw_port_modal(self, surface, mx, my):
        """Draw port destination picker modal."""
        m = self.port_modal
        routes = m["routes"]

        # Dim overlay
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))

        # Dialog box - height grows with number of destinations
        n_routes = len(routes)
        dlg_h = 130 + n_routes * 52 + 20
        dlg = pygame.Rect(SCREEN_W // 2 - 260, SCREEN_H // 2 - dlg_h // 2, 520, dlg_h)
        pygame.draw.rect(surface, (14, 20, 38), dlg, border_radius=6)
        pygame.draw.rect(surface, (80, 180, 220), dlg, 2, border_radius=6)

        # Header
        draw_text(surface, "⚓ Set Sail", dlg.x + 20, dlg.y + 16, (80, 180, 220), 22, bold=True)
        draw_text(surface, f"From: {m['loc']['name']}", dlg.x + 20, dlg.y + 46, CREAM, 14)
        draw_text(surface, "Where do you want to sail?", dlg.x + 20, dlg.y + 68, GREY, 13)
        pygame.draw.line(surface, (40, 80, 110),
                         (dlg.x + 10, dlg.y + 90), (dlg.right - 10, dlg.y + 90))

        # Destination buttons
        m["_dest_rects"] = []
        for i, dest_id in enumerate(routes):
            dest = LOCATIONS.get(dest_id, {})
            dest_name = dest.get("name", dest_id)
            dest_desc = dest.get("description", "")
            btn_y = dlg.y + 98 + i * 52
            btn = pygame.Rect(dlg.x + 20, btn_y, dlg.width - 40, 44)
            hover = btn.collidepoint(mx, my)
            bg = (40, 90, 130) if hover else (20, 40, 65)
            border = (80, 180, 220) if hover else (40, 80, 110)
            pygame.draw.rect(surface, bg, btn, border_radius=4)
            pygame.draw.rect(surface, border, btn, 1, border_radius=4)
            draw_text(surface, f"→  {dest_name}", btn.x + 14, btn.y + 6,
                      (140, 220, 255) if hover else CREAM, 14, bold=hover)
            if dest_desc:
                draw_text(surface, dest_desc[:60], btn.x + 14, btn.y + 26, GREY, 11)
            m["_dest_rects"].append((btn, dest_id, dest_name))

        # Cancel button
        cancel_y = dlg.y + 98 + n_routes * 52 + 4
        cancel_btn = pygame.Rect(dlg.x + dlg.width - 120, cancel_y, 100, 30)
        pygame.draw.rect(surface, (40, 30, 50),
                         cancel_btn, border_radius=4)
        pygame.draw.rect(surface, PANEL_BORDER, cancel_btn, 1, border_radius=4)
        draw_text(surface, "Cancel", cancel_btn.x + 16, cancel_btn.y + 6, GREY, 13)
        m["_cancel_rect"] = cancel_btn

    def _handle_port_modal_click(self, mx, my):
        """Handle clicks inside the port destination picker."""
        m = self.port_modal
        if not m:
            return None

        # Cancel
        cancel = m.get("_cancel_rect")
        if cancel and cancel.collidepoint(mx, my):
            self.port_modal = None
            return None

        # Destination selection
        for btn, dest_id, dest_name in m.get("_dest_rects", []):
            if btn.collidepoint(mx, my):
                dest = LOCATIONS.get(dest_id, {})
                self.port_modal = None
                self._show_event(
                    f"⚓ Set sail from {m['loc']['name']} → {dest_name}!",
                    (80, 180, 220))
                return {"type": "port_travel", "dest_id": dest_id, "dest": dest}

        return None  # click inside modal but not on a button — consume event

    def _draw_camp_dialog(self, surface, mx, my):
        """Draw camp confirmation dialog."""
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        surface.blit(overlay, (0, 0))

        dlg = pygame.Rect(SCREEN_W // 2 - 220, SCREEN_H // 2 - 100, 440, 200)
        pygame.draw.rect(surface, (20, 16, 36), dlg, border_radius=5)
        pygame.draw.rect(surface, GOLD, dlg, 2, border_radius=5)

        tile = self.world.get_current_tile()
        terrain_name = TERRAIN_DATA[tile["terrain"]]["name"]
        ambush = TERRAIN_DATA[tile["terrain"]].get("encounter_rate", 10)

        draw_text(surface, "Set Up Camp?", dlg.x + 140, dlg.y + 15, GOLD, 22, bold=True)
        draw_text(surface, f"Terrain: {terrain_name}", dlg.x + 20, dlg.y + 55, CREAM, 15)
        draw_text(surface, "Restores ~25% HP and ~15% MP/SP per rest.",
                  dlg.x + 20, dlg.y + 80, GREY, 14)
        draw_text(surface, "There is a chance of ambush during rest.",
                  dlg.x + 20, dlg.y + 100, ORANGE, 14)

        yes_btn = pygame.Rect(dlg.x + 60, dlg.y + 140, 140, 40)
        draw_button(surface, yes_btn, "Rest", hover=yes_btn.collidepoint(mx, my), size=16)

        no_btn = pygame.Rect(dlg.x + 240, dlg.y + 140, 140, 40)
        draw_button(surface, no_btn, "Cancel", hover=no_btn.collidepoint(mx, my), size=16)

    # ─────────────────────────────────────────────────────────
    #  EVENT HANDLING
    # ─────────────────────────────────────────────────────────

    def handle_key(self, key):
        """Handle keyboard input. Returns event dict or None."""
        if self.show_camp_confirm or self.port_modal:
            if self.port_modal and key == pygame.K_ESCAPE:
                self.port_modal = None
            return None  # handled by click

        # Movement
        dx, dy = 0, 0
        if key in (pygame.K_UP, pygame.K_w):
            dy = -1
        elif key in (pygame.K_DOWN, pygame.K_s):
            dy = 1
        elif key in (pygame.K_LEFT, pygame.K_a):
            dx = -1
        elif key in (pygame.K_RIGHT, pygame.K_d):
            dx = 1
        elif key == pygame.K_RETURN:
            # Enter location
            tile = self.world.get_current_tile()
            loc_id = tile.get("location_id")
            if loc_id and loc_id in LOCATIONS:
                loc = LOCATIONS[loc_id]
                if loc["type"] == LOC_DUNGEON:
                    can, reason = self.world.can_enter_dungeon(loc_id)
                    if not can:
                        self._show_event(reason, RED)
                        return None
                return {"type": "enter_location", "id": loc_id, "data": loc}
            return None
        elif key == pygame.K_c:
            return {"type": "open_camp"}

        if dx == 0 and dy == 0:
            return None

        event = self.world.move(dx, dy)
        if event:
            if event["type"] == "blocked":
                pass  # silent
            elif event["type"] == "discovery":
                self._show_event(f"Discovered: {event['data']['name']}!", LOC_SECRET_COL)
                return event
            elif event["type"] == "encounter":
                return event
            elif event["type"] == "location":
                pass  # just stepped onto it, don't auto-enter

        return None

    def handle_click(self, mx, my):
        """Handle mouse clicks. Returns event dict or None."""
        # Port modal
        if self.port_modal:
            return self._handle_port_modal_click(mx, my)

        # Camp dialog
        if self.show_camp_confirm:
            yes_btn = pygame.Rect(SCREEN_W // 2 - 220 + 60, SCREEN_H // 2 - 100 + 140, 140, 40)
            no_btn = pygame.Rect(SCREEN_W // 2 - 220 + 240, SCREEN_H // 2 - 100 + 140, 140, 40)
            if yes_btn.collidepoint(mx, my):
                self.show_camp_confirm = False
                return {"type": "camp"}
            elif no_btn.collidepoint(mx, my):
                self.show_camp_confirm = False
                return None
            return None

        # Camp button → open full camp screen
        btn_y = SCREEN_H - 55
        camp_btn = pygame.Rect(SCREEN_W - 320, btn_y, 140, 42)
        if camp_btn.collidepoint(mx, my):
            return {"type": "open_camp"}

        # Menu button
        menu_btn = pygame.Rect(SCREEN_W - 160, btn_y, 140, 42)
        if menu_btn.collidepoint(mx, my):
            return {"type": "menu"}

        # Travel mode toggle
        if self.world.travel.has_horse or self.world.travel.has_carpet:
            travel_btn = pygame.Rect(SCREEN_W - 480, btn_y, 140, 42)
            if travel_btn.collidepoint(mx, my):
                modes = ["walk"]
                if self.world.travel.has_horse:
                    modes.append("horse")
                if self.world.travel.has_carpet:
                    modes.append("carpet")
                cur = self.world.travel.travel_mode
                idx = modes.index(cur) if cur in modes else 0
                self.world.travel.travel_mode = modes[(idx + 1) % len(modes)]
                self._show_event(f"Travel mode: {self.world.travel.travel_mode.title()}", GOLD)
                return None

        return None

    def _show_event(self, msg, color=CREAM):
        self.event_message = msg
        self.event_color = color
        self.event_timer = 3000
