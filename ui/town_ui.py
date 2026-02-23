"""
Realm of Shadows — Town Hub UI

Town locations:
  General Store — buy weapons, armor, consumables; sell inventory items
  Temple        — rest/heal (free), identify items (15g), remove curse (50g)
  Tavern        — hear rumors, flavor text
  Exit          — leave town (back to world/encounters)
"""
import random
import core.sound as sfx
import pygame
from ui.renderer import *
from core.classes import CLASSES
from core.identification import get_item_display_name
from data.shop_inventory import (
    GENERAL_STORE, TEMPLE, TAVERN, get_sell_price, get_town_shop,
)

# ═══════════════════════════════════════════════════════════════
#  COLORS
# ═══════════════════════════════════════════════════════════════

TOWN_BG      = (10, 8, 20)
SHOP_BG      = (15, 12, 28)
ITEM_BG      = (22, 18, 40)
ITEM_HOVER   = (40, 34, 70)
BUY_COL      = (80, 220, 120)
SELL_COL     = (220, 180, 80)
HEAL_COL     = (80, 255, 180)
RUMOR_COL    = (180, 160, 220)

# Town display info
TOWN_DISPLAY = {
    "briarhollow": {
        "name": "Town of Briarhollow",
        "desc": "A quiet settlement at the edge of the wilds.",
    },
    "woodhaven": {
        "name": "Woodhaven",
        "desc": "A village sheltered beneath the ancient Great Grove.",
    },
    "ironhearth": {
        "name": "Ironhearth",
        "desc": "A mining town built on iron and stubbornness.",
    },
}

RARITY_COLORS = {
    "common":    CREAM,
    "uncommon":  (80, 220, 80),
    "rare":      (80, 140, 255),
    "epic":      (180, 80, 255),
    "legendary": (255, 180, 40),
}

# ═══════════════════════════════════════════════════════════════
#  TOWN UI
# ═══════════════════════════════════════════════════════════════

class TownUI:
    # Views
    VIEW_HUB = "hub"
    VIEW_WALK = "walk"       # walkable town map
    VIEW_SHOP = "shop"
    VIEW_SHOP_BUY = "shop_buy"
    VIEW_SHOP_SELL = "shop_sell"
    VIEW_TEMPLE = "temple"
    VIEW_TAVERN = "tavern"
    VIEW_INN = "inn"
    VIEW_INN_LEVELUP = "inn_levelup"
    VIEW_FORGE = "forge"
    VIEW_FORGE_CRAFT = "forge_craft"
    VIEW_JOBBOARD = "jobboard"
    VIEW_FORGE_UPGRADE = "forge_upgrade"
    VIEW_FORGE_ENCHANT = "forge_enchant"

    def __init__(self, party, town_id="briarhollow"):
        self.party = party
        self.message = ""
        self.msg_timer = 0
        self.msg_color = CREAM
        self.finished = False

        # Shop state
        self.shop_tab = "weapons"  # weapons, armor, consumables
        self.shop_scroll = 0
        self.sell_char = 0
        self.sell_scroll = 0
        self.sold_items = []  # items sold by player, available for buyback

        # Temple state
        self.id_char = 0
        self.id_scroll = 0

        # Inn state
        self.inn_result = None  # stores rest result for display
        self.levelup_queue = []  # characters ready to level up
        self.levelup_current = 0  # index in queue
        self.levelup_free_stat = None  # selected stat for free point

        # Tavern state
        from data.story_data import get_rumor
        self.current_rumor = get_rumor()

        # NPC dialogue state
        self.active_dialogue = None  # DialogueUI when talking to an NPC
        self.town_id = town_id
        self.shop = get_town_shop(town_id)  # Town-specific shop inventory

        # Forge state
        self.forge_scroll = 0
        self.forge_item_scroll = 0
        self.forge_selected_item = None
        self.forge_selected_enchant = None

        # ── Walkable town state ──
        from data.town_maps import get_town_data
        self.town_data = get_town_data(town_id)
        if self.town_data:
            self.view = self.VIEW_WALK
            self.walk_x, self.walk_y = self.town_data["spawn"]
            self.walk_facing = "down"
            self.walk_interact_msg = ""   # message shown at bottom
            self.walk_interact_timer = 0
            self.walk_tile_size = 32
            self.walk_anim_t = 0
        else:
            self._return_to_town()

    # ─────────────────────────────────────────────────────────
    #  MAIN DRAW
    # ─────────────────────────────────────────────────────────

    def draw(self, surface, mx, my, dt):
        self.msg_timer = max(0, self.msg_timer - dt)

        # If dialogue is active, render it instead
        if self.active_dialogue and not self.active_dialogue.finished:
            self.active_dialogue.draw(surface, mx, my, dt)
            return

        # Clear dialogue if finished
        if self.active_dialogue and self.active_dialogue.finished:
            self.active_dialogue = None

        surface.fill(TOWN_BG)

        if self.view == self.VIEW_WALK:
            self.walk_anim_t += dt
            self.walk_interact_timer = max(0, self.walk_interact_timer - dt)
            self._draw_walk(surface, mx, my)
        elif self.view == self.VIEW_HUB:
            self._draw_hub(surface, mx, my)
        elif self.view == self.VIEW_SHOP:
            self._draw_shop_menu(surface, mx, my)
        elif self.view == self.VIEW_SHOP_BUY:
            self._draw_shop_buy(surface, mx, my)
        elif self.view == self.VIEW_SHOP_SELL:
            self._draw_shop_sell(surface, mx, my)
        elif self.view == self.VIEW_TEMPLE:
            self._draw_temple(surface, mx, my)
        elif self.view == self.VIEW_TAVERN:
            self._draw_tavern(surface, mx, my)
        elif self.view == self.VIEW_INN:
            self._draw_inn(surface, mx, my)
        elif self.view == self.VIEW_INN_LEVELUP:
            self._draw_inn_levelup(surface, mx, my)
        elif self.view in (self.VIEW_FORGE, self.VIEW_FORGE_CRAFT,
                           self.VIEW_FORGE_UPGRADE, self.VIEW_FORGE_ENCHANT):
            self._draw_forge(surface, mx, my)
        elif self.view == self.VIEW_JOBBOARD:
            self._draw_jobboard(surface, mx, my)

        # Message bar
        if self.message and self.msg_timer > 0:
            draw_text(surface, self.message, SCREEN_W // 2 - 250,
                      SCREEN_H - 30, self.msg_color, 15)

    # ─────────────────────────────────────────────────────────
    #  HUB — Main town menu
    # ─────────────────────────────────────────────────────────

    def _draw_hub(self, surface, mx, my):
        town_info = TOWN_DISPLAY.get(self.town_id, TOWN_DISPLAY["briarhollow"])
        draw_text(surface, town_info["name"], SCREEN_W // 2 - 130, 30,
                  GOLD, 28, bold=True)
        draw_text(surface, town_info["desc"],
                  SCREEN_W // 2 - 190, 70, GREY, 15)

        # Party gold
        total_gold = sum(c.gold for c in self.party)
        draw_text(surface, f"Party Gold: {total_gold}",
                  SCREEN_W // 2 - 60, 100, DIM_GOLD, 16)

        # Location buttons
        locations = [
            ("The Weary Traveler Inn", "Rest, recover, train, and save your progress",
             (100, 80, 40), (220, 180, 80)),
            ("General Store", "Buy and sell weapons, armor, and supplies",
             (120, 100, 50), SELL_COL),
            ("Dunn's Forge", "Craft, upgrade, and enchant equipment",
             (140, 80, 40), (255, 140, 40)),
            ("Temple of Light", "Heal, identify items, remove curses",
             (50, 100, 120), HEAL_COL),
            ("The Shadowed Flagon", "Hear rumors and rest your feet",
             (100, 60, 100), RUMOR_COL),
            ("Leave Town", "Return to the wilds",
             (80, 40, 40), RED),
        ]

        by = 140
        for i, (name, desc, bg_tint, accent) in enumerate(locations):
            btn_rect = pygame.Rect(SCREEN_W // 2 - 300, by + i * 90, 420, 78)
            hover = btn_rect.collidepoint(mx, my)

            bg = (bg_tint[0] + 20, bg_tint[1] + 20, bg_tint[2] + 20) if hover else bg_tint
            border = accent if hover else PANEL_BORDER

            pygame.draw.rect(surface, bg, btn_rect, border_radius=5)
            pygame.draw.rect(surface, border, btn_rect, 2, border_radius=5)

            draw_text(surface, name, btn_rect.x + 20, btn_rect.y + 12,
                      accent if hover else CREAM, 20, bold=True)
            draw_text(surface, desc, btn_rect.x + 20, btn_rect.y + 42,
                      GREY, 12)

        # ── NPC panel (right side) ──
        from data.story_data import get_town_npcs
        npcs = get_town_npcs(self.town_id)
        if npcs:
            npc_x = SCREEN_W // 2 + 150
            draw_text(surface, "People in Town", npc_x, 140, GOLD, 16, bold=True)
            for j, (npc_id, npc_data) in enumerate(npcs):
                nr = pygame.Rect(npc_x, 168 + j * 62, 210, 54)
                hover = nr.collidepoint(mx, my)
                pc = npc_data.get("portrait_color", (80, 80, 80))
                bg = (pc[0] // 4 + 10, pc[1] // 4 + 10, pc[2] // 4 + 10)
                if hover:
                    bg = (bg[0] + 15, bg[1] + 15, bg[2] + 15)
                pygame.draw.rect(surface, bg, nr, border_radius=4)
                pygame.draw.rect(surface, pc if hover else PANEL_BORDER, nr, 2, border_radius=4)
                # Portrait indicator
                pi = pygame.Rect(nr.x + 5, nr.y + 5, 44, 44)
                pygame.draw.rect(surface, pc, pi, border_radius=3)
                initial = npc_data["name"][0]
                iw = get_font(22).size(initial)[0]
                draw_text(surface, initial, pi.x + (44 - iw) // 2, pi.y + 10,
                          WHITE, 22, bold=True)
                draw_text(surface, npc_data["name"], nr.x + 56, nr.y + 6, CREAM, 14, bold=True)
                draw_text(surface, npc_data.get("title", ""), nr.x + 56, nr.y + 24,
                          DARK_GREY, 11)

        # Party summary at bottom
        self._draw_party_bar(surface, mx, my)

    def _draw_party_bar(self, surface, mx, my):
        """Compact party display at bottom of screen."""
        bar_y = SCREEN_H - 100
        pygame.draw.rect(surface, (15, 12, 30), (0, bar_y, SCREEN_W, 100))
        pygame.draw.line(surface, PANEL_BORDER, (0, bar_y), (SCREEN_W, bar_y))

        cw = (SCREEN_W - 40) // len(self.party)
        for i, c in enumerate(self.party):
            cx = 20 + i * cw
            cls = CLASSES[c.class_name]
            draw_text(surface, c.name, cx, bar_y + 8, cls["color"], 13, bold=True)
            draw_text(surface, f"Lv.{c.level} {c.class_name}", cx, bar_y + 24, GREY, 11)
            hp = c.resources.get("HP", 0)
            draw_text(surface, f"HP: {hp}  Gold: {c.gold}  Items: {len(c.inventory)}",
                      cx, bar_y + 40, DIM_GREEN, 11)

            # Status effect indicators
            from core.status_effects import get_status_display
            statuses = get_status_display(c)
            if statuses:
                sx = cx
                for sname, scolor in statuses[:3]:  # max 3 shown
                    draw_text(surface, sname, sx, bar_y + 56, scolor, 9)
                    sx += 80

    # ─────────────────────────────────────────────────────────
    #  WALKABLE TOWN MAP
    # ─────────────────────────────────────────────────────────

    def _draw_walk(self, surface, mx, my):
        from data.town_maps import (
            TILE_COLORS, TILE_TOP_COLORS, TT_WALL, TT_TREE, TT_DOOR,
            TT_FENCE, TT_PATH, TT_EXIT, TT_SIGN, TT_WATER, TT_BRIDGE,
            get_tile, get_building_at, get_npc_at, get_sign_at,
        )

        td = self.town_data
        ts = self.walk_tile_size
        tw, th = td["width"], td["height"]

        # Camera centered on player
        map_area_h = SCREEN_H - 110  # leave room for UI bar at bottom
        cam_x = self.walk_x - (SCREEN_W // ts) // 2
        cam_y = self.walk_y - (map_area_h // ts) // 2
        cam_x = max(0, min(tw - SCREEN_W // ts, cam_x))
        cam_y = max(0, min(th - map_area_h // ts, cam_y))

        # Draw tiles
        for sy in range(map_area_h // ts + 2):
            for sx in range(SCREEN_W // ts + 2):
                tx = cam_x + sx
                ty = cam_y + sy
                tile = get_tile(td, tx, ty)
                px = sx * ts - (cam_x * ts - int(cam_x) * ts)
                py = sy * ts - (cam_y * ts - int(cam_y) * ts)

                # Base tile
                color = TILE_COLORS.get(tile, (40, 40, 40))
                pygame.draw.rect(surface, color, (px, py, ts, ts))

                # Top face for walls/trees/fences (3D effect)
                top_color = TILE_TOP_COLORS.get(tile)
                if top_color:
                    pygame.draw.rect(surface, top_color, (px, py, ts, ts // 3))
                    # Dark edge
                    pygame.draw.line(surface, (color[0]//2, color[1]//2, color[2]//2),
                                     (px, py + ts//3), (px + ts, py + ts//3))

                # Door highlight
                if tile == TT_DOOR:
                    pygame.draw.rect(surface, (160, 120, 60), (px + ts//4, py + ts//6, ts//2, ts*2//3), border_radius=2)
                    pygame.draw.rect(surface, (200, 160, 80), (px + ts//4, py + ts//6, ts//2, ts*2//3), 1, border_radius=2)

                # Exit tiles — subtle glow
                if tile == TT_EXIT:
                    pulse = abs((self.walk_anim_t % 2000) - 1000) / 1000.0
                    glow = int(40 + 30 * pulse)
                    s = pygame.Surface((ts, ts), pygame.SRCALPHA)
                    s.fill((80, 200, 80, glow))
                    surface.blit(s, (px, py))

                # Sign icon
                if tile == TT_SIGN:
                    pygame.draw.rect(surface, (140, 120, 70), (px + ts//3, py + ts//4, ts//3, ts//2))
                    pygame.draw.line(surface, (100, 80, 40), (px + ts//2, py + ts//4 + ts//2), (px + ts//2, py + ts - 2), 2)

                # Water shimmer
                if tile == TT_WATER:
                    shimmer = abs(((self.walk_anim_t + tx * 200) % 1500) - 750) / 750.0
                    s = pygame.Surface((ts, ts), pygame.SRCALPHA)
                    s.fill((60, 90, 140, int(30 + 25 * shimmer)))
                    surface.blit(s, (px, py))

                # Bridge — draw wooden planks over base color
                if tile == TT_BRIDGE:
                    plank_color = (140, 110, 65)
                    gap_color = (110, 85, 45)
                    plank_h = max(2, ts // 4)
                    for pi in range(3):
                        ply = py + pi * (ts // 3) + ts // 8
                        pygame.draw.rect(surface, plank_color, (px + 2, ply, ts - 4, plank_h))
                    pygame.draw.rect(surface, gap_color, (px, py, ts, ts), 1)

                # Grid lines (subtle)
                pygame.draw.rect(surface, (color[0]-10, color[1]-10, color[2]-10),
                                 (px, py, ts, ts), 1)

        # Draw NPCs
        for npc in td.get("npcs", []):
            nx, ny = npc["x"], npc["y"]
            npx = (nx - cam_x) * ts
            npy = (ny - cam_y) * ts
            if 0 <= npx < SCREEN_W and 0 <= npy < map_area_h:
                nc = npc.get("color", (180, 180, 180))
                # Body
                pygame.draw.rect(surface, nc,
                                 (npx + ts//4, npy + ts//4, ts//2, ts//2), border_radius=3)
                # Head
                pygame.draw.circle(surface, (min(255, nc[0]+40), min(255, nc[1]+40), min(255, nc[2]+40)),
                                   (npx + ts//2, npy + ts//5), ts//5)
                # Name above
                nw = get_font(9).size(npc["name"])[0]
                draw_text(surface, npc["name"], npx + ts//2 - nw//2, npy - 12, nc, 9)

        # Draw building labels
        for bld_id, bld in td["buildings"].items():
            lx, ly = bld.get("label_pos", bld["door"])
            lpx = (lx - cam_x) * ts
            lpy = (ly - cam_y) * ts - 8
            if 0 <= lpx < SCREEN_W and 0 <= lpy < map_area_h:
                draw_text(surface, bld["name"], lpx, lpy,
                          bld.get("color", CREAM), 9)

        # Draw player
        ppx = (self.walk_x - cam_x) * ts
        ppy = (self.walk_y - cam_y) * ts
        # Yellow dot with outline
        pygame.draw.circle(surface, (60, 50, 20), (ppx + ts//2, ppy + ts//2), ts//3 + 1)
        pygame.draw.circle(surface, (255, 240, 80), (ppx + ts//2, ppy + ts//2), ts//3)
        # Direction indicator
        dx_map = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
        fdx, fdy = dx_map.get(self.walk_facing, (0, 1))
        pygame.draw.circle(surface, (255, 255, 200),
                           (ppx + ts//2 + fdx * ts//4, ppy + ts//2 + fdy * ts//4), ts//8)

        # ── UI bar at bottom ──
        bar_y = map_area_h
        pygame.draw.rect(surface, (12, 10, 25), (0, bar_y, SCREEN_W, SCREEN_H - bar_y))
        pygame.draw.line(surface, PANEL_BORDER, (0, bar_y), (SCREEN_W, bar_y))

        # Town name + gold (left side)
        draw_text(surface, td["name"], 14, bar_y + 6, GOLD, 16, bold=True)
        total_gold = sum(c.gold for c in self.party)
        draw_text(surface, f"✦ {total_gold}g", 14, bar_y + 26, DIM_GOLD, 12)

        # Interaction prompt (center)
        prompt = self._get_walk_prompt()
        if prompt:
            pw = get_font(14).size(prompt)[0]
            draw_text(surface, prompt, SCREEN_W // 2 - pw // 2, bar_y + 8, HIGHLIGHT, 14)

        # Interact message (center, below prompt)
        if self.walk_interact_msg and self.walk_interact_timer > 0:
            mw = get_font(12).size(self.walk_interact_msg)[0]
            alpha_ratio = min(1.0, self.walk_interact_timer / 500.0)
            msg_col = tuple(int(c * alpha_ratio) for c in self.msg_color)
            draw_text(surface, self.walk_interact_msg,
                      SCREEN_W // 2 - min(mw // 2, 280), bar_y + 30, msg_col, 12)

        # Controls hint (bottom left)
        draw_text(surface, "WASD: Move   ENTER: Interact   ESC: Leave",
                  14, bar_y + 90, DARK_GREY, 10)

        # ── Minimap (center-right) ──
        mm_size = 90
        mm_x = SCREEN_W // 2 + 80
        mm_y = bar_y + 8
        mm_tw, mm_th = td["width"], td["height"]
        mm_tile_w = mm_size / mm_tw
        mm_tile_h = mm_size / mm_th
        # Background
        pygame.draw.rect(surface, (8, 6, 18), (mm_x, mm_y, mm_size, mm_size))
        pygame.draw.rect(surface, PANEL_BORDER, (mm_x, mm_y, mm_size, mm_size), 1)
        # Draw simplified tiles
        from data.town_maps import TT_GRASS, TT_WALL, TT_PATH, TT_WATER, TT_TREE, TT_EXIT
        mm_colors = {
            TT_GRASS: (35, 55, 28), TT_PATH: (80, 68, 48),
            TT_WALL: (65, 52, 40), TT_WATER: (25, 45, 90),
            TT_TREE: (20, 45, 18), TT_EXIT: (50, 110, 50),
        }
        for my_row in range(mm_th):
            for mx_col in range(mm_tw):
                tile = td["map"][my_row][mx_col] if mx_col < len(td["map"][my_row]) else TT_WALL
                col = mm_colors.get(tile, (50, 40, 30))
                rx = int(mm_x + mx_col * mm_tile_w)
                ry = int(mm_y + my_row * mm_tile_h)
                rw = max(1, int(mm_tile_w))
                rh = max(1, int(mm_tile_h))
                pygame.draw.rect(surface, col, (rx, ry, rw, rh))
        # Player dot on minimap
        pm_px = int(mm_x + self.walk_x * mm_tile_w)
        pm_py = int(mm_y + self.walk_y * mm_tile_h)
        pygame.draw.circle(surface, (255, 240, 60), (pm_px, pm_py), max(2, int(mm_tile_w)))
        # NPCs as tiny dots
        for npc in td.get("npcs", []):
            nx_mm = int(mm_x + npc["x"] * mm_tile_w)
            ny_mm = int(mm_y + npc["y"] * mm_tile_h)
            nc = npc.get("color", (180, 180, 180))
            pygame.draw.circle(surface, nc, (nx_mm, ny_mm), max(1, int(mm_tile_w * 0.6)))

        # ── Compact party status (right side) ──
        from core.classes import get_all_resources
        px_start = SCREEN_W - 290
        for i, c in enumerate(self.party):
            cls = CLASSES[c.class_name]
            cx = px_start + i * 72
            # Name
            draw_text(surface, c.name[:5], cx, bar_y + 6, cls["color"], 10, bold=True)
            # HP
            hp = c.resources.get("HP", 0)
            max_resources = get_all_resources(c.class_name, c.stats, c.level)
            max_hp = max_resources.get("HP", 1)
            hp_ratio = hp / max_hp if max_hp > 0 else 0
            hp_color = DIM_GREEN if hp_ratio > 0.5 else (220, 180, 40) if hp_ratio > 0.25 else (220, 70, 70)
            # HP bar
            bar_w = 60
            bar_h = 6
            pygame.draw.rect(surface, (30, 20, 20), (cx, bar_y + 20, bar_w, bar_h))
            pygame.draw.rect(surface, hp_color, (cx, bar_y + 20, int(bar_w * hp_ratio), bar_h))
            draw_text(surface, f"HP {hp}/{max_hp}", cx, bar_y + 29, hp_color, 9)
            # MP (if class has it)
            mp = c.resources.get("MP", -1)
            if mp >= 0:
                max_mp = max_resources.get("MP", 1)
                mp_ratio = mp / max_mp if max_mp > 0 else 0
                pygame.draw.rect(surface, (20, 20, 35), (cx, bar_y + 40, bar_w, 5))
                pygame.draw.rect(surface, (80, 120, 220), (cx, bar_y + 40, int(bar_w * mp_ratio), 5))
            # Dead indicator
            if hp <= 0:
                pygame.draw.line(surface, (200, 50, 50), (cx, bar_y + 6), (cx + 50, bar_y + 50), 2)

    def _get_walk_prompt(self):
        """Get context-sensitive prompt based on what's at the player's position or adjacent."""
        from data.town_maps import get_building_at, get_npc_at, get_sign_at, is_exit, get_tile, TT_DOOR
        td = self.town_data
        x, y = self.walk_x, self.walk_y

        # Check what's at player position
        tile = get_tile(td, x, y)
        if tile == TT_DOOR:
            result = get_building_at(td, x, y)
            if result:
                _, bld = result
                return f"[ENTER] Enter {bld['name']}"

        if is_exit(td, x, y):
            return "[ENTER] Leave Town"

        # Check facing tile for NPCs and signs
        dx_map = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
        fdx, fdy = dx_map.get(self.walk_facing, (0, 1))
        fx, fy = x + fdx, y + fdy

        npc = get_npc_at(td, fx, fy)
        if npc:
            service = npc.get("service", "")
            service_hint = f" ({service.title()})" if service else ""
            return f"[ENTER] Talk to {npc['name']}{service_hint}"

        sign_text = get_sign_at(td, fx, fy)
        if sign_text:
            return "[ENTER] Read Sign"

        # Check current tile too for NPCs
        npc = get_npc_at(td, x, y)
        if npc:
            service = npc.get("service", "")
            service_hint = f" ({service.title()})" if service else ""
            return f"[ENTER] Talk to {npc['name']}{service_hint}"

        return ""

    def handle_key(self, key):
        """Handle keyboard input. Returns 'exit' to leave town, or None."""
        if self.view != self.VIEW_WALK:
            return None

        # Dialogue takes priority
        if self.active_dialogue and not self.active_dialogue.finished:
            return None

        from data.town_maps import is_walkable, get_building_at, get_npc_at, get_sign_at, is_exit, get_tile, TT_DOOR

        td = self.town_data
        dx, dy = 0, 0

        # Movement
        if key in (pygame.K_w, pygame.K_UP):
            dy = -1; self.walk_facing = "up"
        elif key in (pygame.K_s, pygame.K_DOWN):
            dy = 1; self.walk_facing = "down"
        elif key in (pygame.K_a, pygame.K_LEFT):
            dx = -1; self.walk_facing = "left"
        elif key in (pygame.K_d, pygame.K_RIGHT):
            dx = 1; self.walk_facing = "right"
        elif key == pygame.K_RETURN:
            return self._walk_interact()
        elif key == pygame.K_ESCAPE:
            self.finished = True
            return "exit"

        if dx != 0 or dy != 0:
            nx, ny = self.walk_x + dx, self.walk_y + dy
            # Can walk onto NPC tiles (they're on walkable ground)
            if is_walkable(td, nx, ny):
                self.walk_x = nx
                self.walk_y = ny
                sfx.play("step")

        return None

    def _walk_interact(self):
        """Handle ENTER press while walking. Returns 'exit' or None."""
        from data.town_maps import (
            get_building_at, get_npc_at, get_sign_at, is_exit,
            get_tile, TT_DOOR, BLD_INN, BLD_SHOP, BLD_TEMPLE,
            BLD_TAVERN, BLD_FORGE, BLD_HOUSE, BLD_JOBBOARD,
        )

        td = self.town_data
        x, y = self.walk_x, self.walk_y

        # Check current tile for door
        tile = get_tile(td, x, y)
        if tile == TT_DOOR:
            result = get_building_at(td, x, y)
            if result:
                bld_id, bld = result
                btype = bld["type"]
                sfx.play("door_open")

                # Show building entry message with NPC name
                npc_name = bld.get("npc_name", "")
                bld_name = bld.get("name", "building")
                if npc_name:
                    self._show_walk_msg(f"Entered {bld_name}. {npc_name} greets you.", CREAM)
                else:
                    self._show_walk_msg(f"Entered {bld_name}.", CREAM)

                if btype == BLD_INN:
                    self.view = self.VIEW_INN
                elif btype == BLD_SHOP:
                    self.view = self.VIEW_SHOP
                elif btype == BLD_TEMPLE:
                    self.view = self.VIEW_TEMPLE
                elif btype == BLD_TAVERN:
                    self.view = self.VIEW_TAVERN
                elif btype == BLD_FORGE:
                    self.view = self.VIEW_FORGE
                    self.forge_scroll = 0
                elif btype == BLD_HOUSE:
                    self._show_walk_msg(f"The door to {bld['name']} is locked.", GREY)
                elif btype == BLD_JOBBOARD:
                    self._show_walk_msg("Checking the job board...", DIM_GOLD)
                    self.view = self.VIEW_JOBBOARD
                return None

        # Check exit tile
        if is_exit(td, x, y):
            self.finished = True
            return "exit"

        # Check facing tile for NPC
        dx_map = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
        fdx, fdy = dx_map.get(self.walk_facing, (0, 1))
        fx, fy = x + fdx, y + fdy

        npc = get_npc_at(td, fx, fy)
        if not npc:
            npc = get_npc_at(td, x, y)  # also check current tile
        if npc:
            sfx.play("npc_talk")

            # Service NPC — opens building menu directly
            service = npc.get("service")
            if service:
                npc_name = npc["name"]
                if service == "inn":
                    self._show_walk_msg(f"{npc_name}: \"Welcome to the inn! Rest a while.\"",
                                        npc.get("color", CREAM))
                    self.view = self.VIEW_INN
                    return None
                elif service == "shop":
                    self._show_walk_msg(f"{npc_name}: \"Browse my wares, friend.\"",
                                        npc.get("color", CREAM))
                    self.view = self.VIEW_SHOP
                    return None
                elif service == "temple":
                    self._show_walk_msg(f"{npc_name}: \"The Light guides and heals.\"",
                                        npc.get("color", CREAM))
                    self.view = self.VIEW_TEMPLE
                    return None
                elif service == "tavern":
                    self._show_walk_msg(f"{npc_name}: \"Pull up a chair! What'll it be?\"",
                                        npc.get("color", CREAM))
                    self.view = self.VIEW_TAVERN
                    return None
                elif service == "forge":
                    self._show_walk_msg(f"{npc_name}: \"Fine steel, fair prices.\"",
                                        npc.get("color", CREAM))
                    self.view = self.VIEW_FORGE
                    self.forge_scroll = 0
                    return None

            # Regular dialogue NPC
            did = npc.get("dialogue_id")
            if did:
                from data.story_data import NPC_DIALOGUES
                from core.dialogue import select_dialogue
                from ui.dialogue_ui import DialogueUI
                dialogues = NPC_DIALOGUES.get(did, [])
                if dialogues:
                    ds = select_dialogue(did, dialogues)
                    if ds:
                        self.active_dialogue = DialogueUI(ds)
                        return None
            self._show_walk_msg(npc.get("description", f"{npc['name']} has nothing to say."),
                                npc.get("color", CREAM))
            return None

        # Check facing tile for sign
        sign_text = get_sign_at(td, fx, fy)
        if sign_text:
            if "Job Board" in sign_text:
                self._show_walk_msg("Checking the job board...", DIM_GOLD)
                self.view = self.VIEW_JOBBOARD
            else:
                self._show_walk_msg(sign_text, DIM_GOLD)
            return None

        return None

    def _show_walk_msg(self, text, color=CREAM):
        """Show a temporary message in the walk UI."""
        self.walk_interact_msg = text
        self.walk_interact_timer = 3000
        self.msg_color = color

    def _return_to_town(self):
        """Return to the main town view (walkable or hub)."""
        if self.town_data:
            self.view = self.VIEW_WALK
        else:
            self.view = self.VIEW_HUB

    # ─────────────────────────────────────────────────────────
    #  GENERAL STORE — Menu
    # ─────────────────────────────────────────────────────────

    def _draw_shop_menu(self, surface, mx, my):
        draw_text(surface, self.shop.get("name", "General Store"), SCREEN_W // 2 - 90, 20, GOLD, 24, bold=True)
        draw_text(surface, self.shop["welcome"], SCREEN_W // 2 - 150, 55, GREY, 14)

        total_gold = sum(c.gold for c in self.party)
        draw_text(surface, f"Party Gold: {total_gold}", SCREEN_W // 2 - 60, 85, DIM_GOLD, 16)

        options = [
            ("Buy", "Browse weapons, armor, and supplies", BUY_COL),
            ("Sell", "Sell items from your inventory", SELL_COL),
            ("Back to Town", "Return to the town square", GREY),
        ]

        for i, (name, desc, accent) in enumerate(options):
            btn = pygame.Rect(SCREEN_W // 2 - 200, 130 + i * 90, 400, 75)
            hover = btn.collidepoint(mx, my)
            bg = (40, 35, 65) if hover else (25, 20, 45)
            pygame.draw.rect(surface, bg, btn, border_radius=4)
            pygame.draw.rect(surface, accent if hover else PANEL_BORDER, btn, 2, border_radius=4)
            draw_text(surface, name, btn.x + 20, btn.y + 12, accent if hover else CREAM, 20, bold=True)
            draw_text(surface, desc, btn.x + 20, btn.y + 42, DARK_GREY, 13)

        self._draw_party_bar(surface, mx, my)

    # ─────────────────────────────────────────────────────────
    #  GENERAL STORE — Buy
    # ─────────────────────────────────────────────────────────

    def _draw_shop_buy(self, surface, mx, my):
        draw_text(surface, "Buy Items", 20, 12, GOLD, 22, bold=True)

        total_gold = sum(c.gold for c in self.party)
        draw_text(surface, f"Party Gold: {total_gold}", SCREEN_W - 220, 15, DIM_GOLD, 16)

        # Back button
        back = pygame.Rect(SCREEN_W - 140, 50, 120, 34)
        draw_button(surface, back, "Back", hover=back.collidepoint(mx, my), size=13)

        # Category tabs
        tabs = [("weapons", "Weapons"), ("armor", "Armor"), ("consumables", "Supplies")]
        for i, (key, label) in enumerate(tabs):
            tr = pygame.Rect(20 + i * 140, 50, 130, 32)
            is_sel = (self.shop_tab == key)
            hover = tr.collidepoint(mx, my)
            bg = (50, 40, 85) if is_sel else (35, 30, 60) if hover else (20, 18, 36)
            border = GOLD if is_sel else HIGHLIGHT if hover else PANEL_BORDER
            pygame.draw.rect(surface, bg, tr, border_radius=3)
            pygame.draw.rect(surface, border, tr, 2, border_radius=3)
            draw_text(surface, label, tr.x + 10, tr.y + 7,
                      GOLD if is_sel else CREAM, 14, bold=is_sel)

        # Item list — regular shop items + buyback items
        items = list(self.shop.get(self.shop_tab, []))
        # Append sold items to current tab (they appear in all tabs under "Buyback")
        buyback_start = len(items)
        items.extend(self.sold_items)
        panel = pygame.Rect(20, 95, SCREEN_W - 40, SCREEN_H - 200)
        draw_panel(surface, panel, bg_color=SHOP_BG)

        if not items:
            draw_text(surface, "Nothing in this category.", panel.x + 20, panel.y + 20, DARK_GREY, 15)
        else:
            iy = panel.y + 10
            max_vis = 8
            start = self.shop_scroll
            end = min(len(items), start + max_vis)

            for idx in range(start, end):
                item = items[idx]
                is_buyback = idx >= buyback_start
                row = pygame.Rect(panel.x + 8, iy, panel.width - 16, 68)
                hover = row.collidepoint(mx, my)

                if is_buyback:
                    bg = (30, 28, 18) if hover else (22, 20, 12)
                else:
                    bg = ITEM_HOVER if hover else ITEM_BG
                pygame.draw.rect(surface, bg, row, border_radius=3)
                pygame.draw.rect(surface, HIGHLIGHT if hover else PANEL_BORDER, row, 1, border_radius=3)

                # Buyback label
                if is_buyback:
                    draw_text(surface, "BUYBACK", row.x + row.width - 170, row.y + 26,
                              (180, 150, 60), 10, bold=True)

                # Name
                rarity = item.get("rarity", "common")
                name_col = RARITY_COLORS.get(rarity, CREAM)
                draw_text(surface, item["name"], row.x + 10, row.y + 4, name_col, 15, bold=True)

                # Description
                desc = item.get("description", "")
                if len(desc) > 80:
                    desc = desc[:77] + "..."
                draw_text(surface, desc, row.x + 10, row.y + 24, GREY, 12)

                # Stats
                parts = []
                if item.get("damage"):
                    parts.append(f"DMG {item['damage']}")
                if item.get("defense", 0):
                    parts.append(f"DEF +{item['defense']}")
                if item.get("heal_amount"):
                    parts.append(f"Heal {item['heal_amount']}")
                for stat, val in item.get("stat_bonuses", {}).items():
                    parts.append(f"{stat}+{val}")
                if parts:
                    draw_text(surface, "  ".join(parts), row.x + 10, row.y + 44, GREY, 11)

                # Price + buy hint
                price = item.get("buy_price", 0)
                can_afford = total_gold >= price
                price_col = BUY_COL if (hover and can_afford) else DIM_GOLD if can_afford else RED
                draw_text(surface, f"{price}g", row.x + row.width - 80, row.y + 4, price_col, 16, bold=True)
                if hover:
                    lbl = "Click to buy" if can_afford else "Not enough gold"
                    draw_text(surface, lbl, row.x + row.width - 140, row.y + 48,
                              BUY_COL if can_afford else RED, 11)

                iy += 72

            # Scroll hints
            if self.shop_scroll > 0:
                draw_text(surface, "^ scroll up", panel.x + panel.width // 2 - 40, panel.y + 2, DIM_GOLD, 11)
            if end < len(items):
                draw_text(surface, "v scroll down", panel.x + panel.width // 2 - 45, iy + 2, DIM_GOLD, 11)

        self._draw_party_bar(surface, mx, my)

    # ─────────────────────────────────────────────────────────
    #  GENERAL STORE — Sell
    # ─────────────────────────────────────────────────────────

    def _draw_shop_sell(self, surface, mx, my):
        draw_text(surface, "Sell Items", 20, 12, GOLD, 22, bold=True)

        total_gold = sum(c.gold for c in self.party)
        draw_text(surface, f"Party Gold: {total_gold}", SCREEN_W - 220, 15, DIM_GOLD, 16)

        back = pygame.Rect(SCREEN_W - 140, 50, 120, 34)
        draw_button(surface, back, "Back", hover=back.collidepoint(mx, my), size=13)

        # Character tabs
        for i, c in enumerate(self.party):
            cls = CLASSES[c.class_name]
            tw = (SCREEN_W - 40) // len(self.party)
            tr = pygame.Rect(20 + i * tw, 50, tw - 4, 32)
            is_sel = (i == self.sell_char)
            hover = tr.collidepoint(mx, my)
            bg = (50, 40, 85) if is_sel else (35, 30, 60) if hover else (20, 18, 36)
            border = cls["color"] if is_sel else HIGHLIGHT if hover else PANEL_BORDER
            pygame.draw.rect(surface, bg, tr, border_radius=3)
            pygame.draw.rect(surface, border, tr, 2, border_radius=3)
            draw_text(surface, f"{c.name} ({len(c.inventory)})",
                      tr.x + 8, tr.y + 7, cls["color"] if is_sel else GREY, 13, bold=is_sel)

        char = self.party[self.sell_char]
        panel = pygame.Rect(20, 95, SCREEN_W - 40, SCREEN_H - 200)
        draw_panel(surface, panel, bg_color=SHOP_BG)

        if not char.inventory:
            draw_text(surface, f"{char.name}'s inventory is empty.",
                      panel.x + 20, panel.y + 20, DARK_GREY, 15)
        else:
            iy = panel.y + 10
            max_vis = 8
            start = self.sell_scroll
            end = min(len(char.inventory), start + max_vis)

            for idx in range(start, end):
                item = char.inventory[idx]
                row = pygame.Rect(panel.x + 8, iy, panel.width - 16, 68)
                hover = row.collidepoint(mx, my)
                bg = ITEM_HOVER if hover else ITEM_BG
                pygame.draw.rect(surface, bg, row, border_radius=3)
                pygame.draw.rect(surface, HIGHLIGHT if hover else PANEL_BORDER, row, 1, border_radius=3)

                name = get_item_display_name(item)
                rarity = item.get("rarity", "common")
                name_col = RARITY_COLORS.get(rarity, CREAM) if item.get("identified") else GREY
                draw_text(surface, name, row.x + 10, row.y + 4, name_col, 15, bold=True)

                item_type = item.get("type", "misc")
                draw_text(surface, item_type, row.x + 10, row.y + 24, DARK_GREY, 12)

                # Sell price
                price = get_sell_price(item)
                draw_text(surface, f"Sell: {price}g", row.x + row.width - 100, row.y + 4,
                          SELL_COL if hover else DIM_GOLD, 16, bold=True)
                if hover:
                    draw_text(surface, "Click to sell", row.x + row.width - 110, row.y + 48,
                              SELL_COL, 11)

                iy += 72

            if self.sell_scroll > 0:
                draw_text(surface, "^ scroll up", panel.x + panel.width // 2 - 40, panel.y + 2, DIM_GOLD, 11)
            if end < len(char.inventory):
                draw_text(surface, "v scroll down", panel.x + panel.width // 2 - 45, iy + 2, DIM_GOLD, 11)

        self._draw_party_bar(surface, mx, my)

    # ─────────────────────────────────────────────────────────
    #  TEMPLE
    # ─────────────────────────────────────────────────────────

    def _draw_temple(self, surface, mx, my):
        draw_text(surface, "Temple of Light", SCREEN_W // 2 - 100, 20, GOLD, 24, bold=True)
        draw_text(surface, TEMPLE["welcome"], SCREEN_W // 2 - 180, 55, GREY, 14)

        total_gold = sum(c.gold for c in self.party)
        draw_text(surface, f"Party Gold: {total_gold}", SCREEN_W // 2 - 60, 85, DIM_GOLD, 16)

        back = pygame.Rect(SCREEN_W - 140, 20, 120, 34)
        draw_button(surface, back, "Back", hover=back.collidepoint(mx, my), size=13)

        # Services
        services = list(TEMPLE["services"].values())
        by = 120
        for i, svc in enumerate(services):
            btn = pygame.Rect(SCREEN_W // 2 - 250, by + i * 80, 500, 68)
            hover = btn.collidepoint(mx, my)
            cost = svc["cost"]
            can_afford = total_gold >= cost

            bg = (35, 50, 45) if (hover and can_afford) else (25, 20, 45)
            border = HEAL_COL if (hover and can_afford) else RED if (hover and not can_afford) else PANEL_BORDER

            pygame.draw.rect(surface, bg, btn, border_radius=4)
            pygame.draw.rect(surface, border, btn, 2, border_radius=4)

            draw_text(surface, svc["name"], btn.x + 15, btn.y + 8,
                      HEAL_COL if hover else CREAM, 18, bold=True)
            draw_text(surface, svc["description"], btn.x + 15, btn.y + 34, GREY, 13)

            price_str = "Free" if cost == 0 else f"{cost}g"
            price_col = HEAL_COL if cost == 0 else (DIM_GOLD if can_afford else RED)
            draw_text(surface, price_str, btn.x + btn.width - 70, btn.y + 8,
                      price_col, 18, bold=True)

        # Identify section: show unidentified items if any
        unid_items = []
        for ci, c in enumerate(self.party):
            for ii, item in enumerate(c.inventory):
                from core.identification import needs_identification
                if needs_identification(item):
                    unid_items.append((ci, ii, item, c))

        if unid_items:
            uy = by + len(services) * 80 + 20
            draw_text(surface, f"Unidentified items ({len(unid_items)}):",
                      SCREEN_W // 2 - 250, uy, DIM_GOLD, 14)
            uy += 25
            for ui_idx, (ci, ii, item, char) in enumerate(unid_items[:5]):
                row = pygame.Rect(SCREEN_W // 2 - 250, uy, 500, 40)
                hover = row.collidepoint(mx, my)
                bg = ITEM_HOVER if hover else ITEM_BG
                pygame.draw.rect(surface, bg, row, border_radius=3)
                pygame.draw.rect(surface, PANEL_BORDER, row, 1, border_radius=3)

                name = get_item_display_name(item)
                draw_text(surface, f"{char.name}: {name}", row.x + 10, row.y + 10, GREY, 13)

                can_id = total_gold >= 15
                if hover:
                    lbl = "Click to identify (15g)" if can_id else "Not enough gold"
                    col = HEAL_COL if can_id else RED
                    draw_text(surface, lbl, row.x + row.width - 180, row.y + 10, col, 12)

                uy += 44

        self._draw_party_bar(surface, mx, my)

    # ─────────────────────────────────────────────────────────
    #  INN
    # ─────────────────────────────────────────────────────────

    def _draw_inn(self, surface, mx, my):
        from core.progression import INN_TIERS, INN_TIER_ORDER, can_level_up, training_cost
        draw_text(surface, "The Weary Traveler Inn", SCREEN_W // 2 - 150, 20, GOLD, 24, bold=True)
        draw_text(surface, "Rest your bones, train your skills, save your progress.",
                  SCREEN_W // 2 - 220, 55, GREY, 14)

        back = pygame.Rect(SCREEN_W - 140, 20, 120, 34)
        draw_button(surface, back, "Back", hover=back.collidepoint(mx, my), size=13)

        total_gold = sum(c.gold for c in self.party)
        party_size = len(self.party)
        draw_text(surface, f"Party Gold: {total_gold}", SCREEN_W // 2 - 60, 80, DIM_GOLD, 14)

        # Check for characters ready to level up
        lvl_ready = [c for c in self.party if can_level_up(c)]

        by = 110
        for i, tier_key in enumerate(INN_TIER_ORDER):
            tier = INN_TIERS[tier_key]
            room_cost = tier["cost_per_char"] * party_size

            # Training cost is INCLUDED in room cost, not separate
            # Higher tier rooms include training as part of the service
            train_cost = 0
            train_count = 0
            if tier["allows_level_up"] and lvl_ready:
                for c in lvl_ready:
                    train_cost += training_cost(c.level + 1)
                train_count = len(lvl_ready)

            total_cost = room_cost + train_cost

            btn = pygame.Rect(SCREEN_W // 2 - 280, by + i * 95, 560, 85)
            hover = btn.collidepoint(mx, my)
            can_afford = total_gold >= total_cost

            bg = (50, 40, 25) if hover and can_afford else (30, 24, 18)
            border = (220, 180, 80) if hover and can_afford else PANEL_BORDER
            if not can_afford:
                bg = (25, 20, 15)

            pygame.draw.rect(surface, bg, btn, border_radius=5)
            pygame.draw.rect(surface, border, btn, 2, border_radius=5)

            name_col = GOLD if can_afford else DARK_GREY
            draw_text(surface, tier["name"], btn.x + 15, btn.y + 8, name_col, 18, bold=True)

            if train_cost > 0:
                cost_str = f"Room: {room_cost}g + Training: {train_cost}g = {total_cost}g total"
            elif room_cost > 0:
                cost_str = f"{room_cost}g ({tier['cost_per_char']}g × {party_size})"
            else:
                cost_str = "Free"
            draw_text(surface, cost_str, btn.x + 250, btn.y + 10, DIM_GOLD if can_afford else DARK_GREY, 13)

            draw_text(surface, tier["description"], btn.x + 15, btn.y + 35, GREY, 12)

            if tier["allows_level_up"] and lvl_ready:
                draw_text(surface, f"{train_count} character(s) ready to level up!",
                          btn.x + 15, btn.y + 55, (180, 220, 120), 12)
            elif not tier["allows_level_up"] and lvl_ready:
                draw_text(surface, "No training available at this tier", btn.x + 15, btn.y + 55, DARK_GREY, 11)

            if tier.get("buff"):
                draw_text(surface, f"Bonus: {tier['buff']['name']} (+{tier['buff']['hp_bonus_pct']}% HP next dungeon)",
                          btn.x + 15, btn.y + 68, (150, 200, 255), 11)

        # Show inn result if just rested
        if self.inn_result:
            rp = pygame.Rect(SCREEN_W // 2 - 250, by + len(INN_TIER_ORDER) * 95 + 10, 500, 60)
            pygame.draw.rect(surface, (20, 30, 15), rp, border_radius=5)
            pygame.draw.rect(surface, GREEN, rp, 1, border_radius=5)
            draw_text(surface, self.inn_result, rp.x + 15, rp.y + 10, GREEN, 14, max_width=470)

        self._draw_party_bar(surface, mx, my)

    def _draw_inn_levelup(self, surface, mx, my):
        """Level up screen for a character at the inn."""
        from core.progression import can_level_up, apply_level_up, training_cost
        from core.classes import STAT_NAMES

        if not self.levelup_queue:
            self.view = self.VIEW_INN
            return

        c = self.levelup_queue[self.levelup_current]
        cost = training_cost(c.level + 1)
        cls = CLASSES.get(c.class_name, {})

        draw_text(surface, f"Training: {c.name}", SCREEN_W // 2 - 120, 20, GOLD, 24, bold=True)
        class_col = cls.get("color", CREAM)
        draw_text(surface, f"Level {c.level} → {c.level + 1}  |  {c.class_name}  |  Cost: {cost}g",
                  SCREEN_W // 2 - 180, 55, CREAM, 16)
        # Show class with color
        draw_text(surface, c.class_name,
                  SCREEN_W // 2 - 180 + get_font(16).size(f"Level {c.level} → {c.level + 1}  |  ")[0],
                  55, class_col, 16, bold=True)

        # Class stat recommendation hint
        growth = cls.get("stat_growth", {})
        primary_stats = [s for s, tier in growth.items() if tier == "high"]
        if primary_stats:
            draw_text(surface, f"Key stats for {c.class_name}: {', '.join(primary_stats)}",
                      SCREEN_W // 2 - 180, 78, class_col, 13)

        # Current stats
        draw_text(surface, "Current Stats:", 60, 100, GOLD, 16, bold=True)
        for i, stat in enumerate(STAT_NAMES):
            val = c.stats[stat]
            sy = 130 + i * 30
            draw_text(surface, f"{stat}: {val}", 80, sy, CREAM, 15)

        # Free stat point selection
        draw_text(surface, "Assign 1 free stat point:", SCREEN_W // 2 - 50, 100, GOLD, 16, bold=True)
        for i, stat in enumerate(STAT_NAMES):
            btn = pygame.Rect(SCREEN_W // 2 - 30, 130 + i * 38, 200, 32)
            selected = self.levelup_free_stat == stat
            hover = btn.collidepoint(mx, my)
            bg = (60, 50, 30) if selected else (40, 35, 25) if hover else (25, 20, 15)
            border = GOLD if selected else PANEL_BORDER
            pygame.draw.rect(surface, bg, btn, border_radius=3)
            pygame.draw.rect(surface, border, btn, 1, border_radius=3)
            label = f"+1 {stat} ({c.stats[stat]} → {c.stats[stat]+1})"
            draw_text(surface, label, btn.x + 10, btn.y + 6, CREAM if hover or selected else GREY, 14)

        # Confirm button
        can_train = self.levelup_free_stat is not None and sum(cc.gold for cc in self.party) >= cost
        confirm = pygame.Rect(SCREEN_W // 2 + 200, 350, 180, 45)
        draw_button(surface, confirm, "Train!", hover=confirm.collidepoint(mx, my) and can_train, size=16)
        if not can_train and self.levelup_free_stat:
            draw_text(surface, "Not enough gold!", confirm.x, confirm.y + 50, RED, 12)

        # Skip button
        skip = pygame.Rect(SCREEN_W // 2 + 200, 410, 180, 40)
        draw_button(surface, skip, "Skip", hover=skip.collidepoint(mx, my), size=14)

    def _rest_at_inn(self, tier_key, total_cost=None):
        """Process inn rest for the party. total_cost includes room + training."""
        from core.progression import INN_TIERS, can_level_up
        from core.classes import get_all_resources

        tier = INN_TIERS[tier_key]
        party_size = len(self.party)

        if total_cost is None:
            total_cost = tier["cost_per_char"] * party_size

        total_gold = sum(c.gold for c in self.party)
        if total_gold < total_cost:
            return False

        # Deduct total gold (room + training) evenly across party
        if total_cost > 0:
            remaining = total_cost
            for c in self.party:
                deduct = min(c.gold, remaining)
                c.gold -= deduct
                remaining -= deduct
                if remaining <= 0:
                    break

        # Restore resources
        for c in self.party:
            max_res = get_all_resources(c.class_name, c.stats, c.level)
            for res_name, max_val in max_res.items():
                current = c.resources.get(res_name, 0)
                if res_name == "HP":
                    restore = tier["hp_restore"]
                elif "MP" in res_name or res_name == "Ki":
                    restore = tier["mp_restore"]
                else:
                    restore = tier["sp_restore"]
                gain = int(max_val * restore)
                c.resources[res_name] = min(max_val, current + gain)

        # Clear resurrection sickness
        for c in self.party:
            if hasattr(c, 'status_effects'):
                c.status_effects = [s for s in c.status_effects
                                    if s.get("type") != "resurrection_sickness"]

        # Check for level ups
        if tier["allows_level_up"]:
            self.levelup_queue = [c for c in self.party if can_level_up(c)]
            self.levelup_current = 0
            self.levelup_free_stat = None
        else:
            self.levelup_queue = []

        cost_str = f"{total_cost}g" if total_cost > 0 else "free"
        restore_str = f"{int(tier['hp_restore']*100)}%"
        self.inn_result = f"Rested at {tier['name']} ({cost_str}). Restored {restore_str} HP/MP/SP. Progress saved."

        return True

    # ─────────────────────────────────────────────────────────
    #  TAVERN
    # ─────────────────────────────────────────────────────────

    def _draw_tavern(self, surface, mx, my):
        draw_text(surface, "The Shadowed Flagon", SCREEN_W // 2 - 130, 30, GOLD, 24, bold=True)
        draw_text(surface, TAVERN["welcome"], SCREEN_W // 2 - 120, 70, GREY, 15)

        back = pygame.Rect(SCREEN_W - 140, 30, 120, 34)
        draw_button(surface, back, "Back", hover=back.collidepoint(mx, my), size=13)

        # Rumor panel
        rumor_panel = pygame.Rect(SCREEN_W // 2 - 300, 130, 600, 150)
        draw_panel(surface, rumor_panel, bg_color=(25, 18, 40))
        draw_text(surface, "A patron leans over and whispers:",
                  rumor_panel.x + 20, rumor_panel.y + 15, DIM_GOLD, 14)
        draw_text(surface, f'"{self.current_rumor}"',
                  rumor_panel.x + 20, rumor_panel.y + 45, RUMOR_COL, 16,
                  max_width=rumor_panel.width - 40)

        # Another round button
        another = pygame.Rect(SCREEN_W // 2 - 100, 310, 200, 45)
        draw_button(surface, another, "Buy a Round (1g)",
                    hover=another.collidepoint(mx, my), size=14)

        self._draw_party_bar(surface, mx, my)

    # ─────────────────────────────────────────────────────────
    #  JOB BOARD
    # ─────────────────────────────────────────────────────────

    def _draw_jobboard(self, surface, mx, my):
        from data.job_board import get_town_jobs, check_job_ready, get_job_progress, JOBS

        draw_text(surface, "Job Board", SCREEN_W // 2 - 60, 30, GOLD, 24, bold=True)
        draw_text(surface, "Available work in the area.",
                  SCREEN_W // 2 - 100, 65, GREY, 14)

        back = pygame.Rect(SCREEN_W - 140, 30, 120, 34)
        draw_button(surface, back, "Back", hover=back.collidepoint(mx, my), size=13)

        jobs = get_town_jobs(self.town_id)
        if not jobs:
            draw_text(surface, "No jobs posted.", SCREEN_W // 2 - 60, 150, GREY, 16)
            self._draw_party_bar(surface, mx, my)
            return

        y = 100
        self._job_buttons = []
        for job_id, job, state in jobs:
            panel = pygame.Rect(60, y, SCREEN_W - 120, 80)
            draw_panel(surface, panel, bg_color=(25, 20, 35))

            # Job name, type tag, and level requirement
            type_col = {"bounty": (200, 100, 100), "fetch": (100, 180, 100),
                        "explore": (100, 140, 220)}.get(job["type"], GREY)
            tag = job["type"].upper()
            level_req = job.get("level_req", 1)
            draw_text(surface, f"[{tag}]", panel.x + 10, panel.y + 8, type_col, 11)
            draw_text(surface, job["name"], panel.x + 80, panel.y + 6, CREAM, 16, bold=True)
            draw_text(surface, f"Lv.{level_req}+",
                      panel.x + panel.width - 180, panel.y + 8, (160, 140, 100), 11)

            # Rewards
            draw_text(surface, f"Reward: {job['reward_gold']}g, {job['reward_xp']} XP",
                      panel.x + 10, panel.y + 30, DIM_GOLD, 12)

            # Description
            desc = job["description"]
            if len(desc) > 80:
                desc = desc[:77] + "..."
            draw_text(surface, desc, panel.x + 10, panel.y + 50, GREY, 11,
                      max_width=panel.width - 160)

            # Progress / action button
            btn_x = panel.x + panel.width - 130
            btn_w = 120
            if state == 0:
                # Available — check level requirement
                level_req = job.get("level_req", 1)
                party_level = max((c.level for c in self.party), default=1)
                too_low = party_level < level_req

                btn = pygame.Rect(btn_x, panel.y + 25, btn_w, 30)
                if too_low:
                    # Grey out the panel and show level requirement instead of Accept
                    pygame.draw.rect(surface, (15, 12, 22), panel, border_radius=4)
                    draw_text(surface, f"Requires Lv.{level_req}",
                              btn_x, panel.y + 32, (130, 100, 100), 12)
                else:
                    draw_button(surface, btn, "Accept",
                                hover=btn.collidepoint(mx, my), size=12)
                    self._job_buttons.append((btn, "accept", job_id))
            elif state == 1:
                # Accepted — show progress
                progress = get_job_progress(job_id)
                required = job.get("required", 0)
                ready = check_job_ready(job_id, self.party)

                if job["type"] == "bounty":
                    prog_text = f"{min(progress, required)}/{required} killed"
                elif job["type"] == "fetch":
                    # Count items in party
                    count = 0
                    for c in self.party:
                        for item in c.inventory:
                            if item.get("name") == job["item_name"]:
                                count += item.get("stack", 1)
                    prog_text = f"{min(count, required)}/{required} collected"
                else:
                    prog_text = "Complete!" if ready else "In progress..."

                prog_col = (100, 220, 100) if ready else (220, 180, 80)
                draw_text(surface, prog_text, btn_x, panel.y + 15, prog_col, 12)

                if ready:
                    btn = pygame.Rect(btn_x, panel.y + 38, btn_w, 28)
                    draw_button(surface, btn, "Turn In",
                                hover=btn.collidepoint(mx, my), size=12)
                    self._job_buttons.append((btn, "turnin", job_id))
            elif state == -2:
                draw_text(surface, "COMPLETED", btn_x + 10, panel.y + 30,
                          (80, 180, 80), 13, bold=True)

            y += 88

        self._draw_party_bar(surface, mx, my)

    # ─────────────────────────────────────────────────────────
    #  CLICK HANDLING
    # ─────────────────────────────────────────────────────────

    def handle_click(self, mx, my):
        """Returns 'exit' to leave town, or None."""

        # Dialogue takes priority
        if self.active_dialogue and not self.active_dialogue.finished:
            result = self.active_dialogue.handle_click(mx, my)
            if self.active_dialogue.finished:
                self.active_dialogue = None
            return None

        # ── Hub view ──
        if self.view == self.VIEW_HUB:
            locations = ["inn", "shop", "forge", "temple", "tavern", "exit"]
            by = 140
            for i, loc in enumerate(locations):
                btn = pygame.Rect(SCREEN_W // 2 - 300, by + i * 90, 420, 78)
                if btn.collidepoint(mx, my):
                    if loc == "exit":
                        self.finished = True
                        return "exit"
                    elif loc == "shop":
                        self.view = self.VIEW_SHOP
                    elif loc == "forge":
                        self.view = self.VIEW_FORGE
                        self.forge_scroll = 0
                    elif loc == "temple":
                        self.view = self.VIEW_TEMPLE
                    elif loc == "tavern":
                        self.view = self.VIEW_TAVERN
                    elif loc == "inn":
                        self.view = self.VIEW_INN
                    return None

            # NPC clicks
            from data.story_data import get_town_npcs, NPC_DIALOGUES
            from core.dialogue import select_dialogue
            npcs = get_town_npcs(self.town_id)
            npc_x = SCREEN_W // 2 + 150
            for j, (npc_id, npc_data) in enumerate(npcs):
                nr = pygame.Rect(npc_x, 168 + j * 62, 210, 54)
                if nr.collidepoint(mx, my):
                    sfx.play("npc_talk")
                    dialogues = NPC_DIALOGUES.get(npc_id, [])
                    if dialogues:
                        from ui.dialogue_ui import DialogueUI
                        ds = select_dialogue(npc_id, dialogues)
                        if ds:
                            self.active_dialogue = DialogueUI(ds)
                    return None

        # ── Shop menu ──
        elif self.view == self.VIEW_SHOP:
            options = ["buy", "sell", "back"]
            for i, opt in enumerate(options):
                btn = pygame.Rect(SCREEN_W // 2 - 200, 130 + i * 90, 400, 75)
                if btn.collidepoint(mx, my):
                    if opt == "buy":
                        self.view = self.VIEW_SHOP_BUY
                        self.shop_scroll = 0
                    elif opt == "sell":
                        self.view = self.VIEW_SHOP_SELL
                        self.sell_scroll = 0
                    elif opt == "back":
                        self._return_to_town()
                    return None

        # ── Shop buy ──
        elif self.view == self.VIEW_SHOP_BUY:
            # Back button
            back = pygame.Rect(SCREEN_W - 140, 50, 120, 34)
            if back.collidepoint(mx, my):
                self.view = self.VIEW_SHOP
                return None

            # Tab clicks
            tabs = ["weapons", "armor", "consumables"]
            for i, key in enumerate(tabs):
                tr = pygame.Rect(20 + i * 140, 50, 130, 32)
                if tr.collidepoint(mx, my):
                    self.shop_tab = key
                    self.shop_scroll = 0
                    return None

            # Item clicks — regular shop + buyback
            items = list(self.shop.get(self.shop_tab, []))
            buyback_start = len(items)
            items.extend(self.sold_items)
            panel = pygame.Rect(20, 95, SCREEN_W - 40, SCREEN_H - 200)
            iy = panel.y + 10
            start = self.shop_scroll
            end = min(len(items), start + 8)
            for idx in range(start, end):
                row = pygame.Rect(panel.x + 8, iy, panel.width - 16, 68)
                if row.collidepoint(mx, my):
                    is_buyback = idx >= buyback_start
                    if is_buyback:
                        self._buy_back_item(idx - buyback_start)
                    else:
                        self._buy_item(items[idx])
                    return None
                iy += 72

        # ── Shop sell ──
        elif self.view == self.VIEW_SHOP_SELL:
            back = pygame.Rect(SCREEN_W - 140, 50, 120, 34)
            if back.collidepoint(mx, my):
                self.view = self.VIEW_SHOP
                return None

            # Character tabs
            for i in range(len(self.party)):
                tw = (SCREEN_W - 40) // len(self.party)
                tr = pygame.Rect(20 + i * tw, 50, tw - 4, 32)
                if tr.collidepoint(mx, my):
                    self.sell_char = i
                    self.sell_scroll = 0
                    return None

            # Item clicks
            char = self.party[self.sell_char]
            panel = pygame.Rect(20, 95, SCREEN_W - 40, SCREEN_H - 200)
            iy = panel.y + 10
            start = self.sell_scroll
            end = min(len(char.inventory), start + 8)
            for idx in range(start, end):
                row = pygame.Rect(panel.x + 8, iy, panel.width - 16, 68)
                if row.collidepoint(mx, my):
                    self._sell_item(char, idx)
                    return None
                iy += 72

        # ── Temple ──
        elif self.view == self.VIEW_TEMPLE:
            back = pygame.Rect(SCREEN_W - 140, 20, 120, 34)
            if back.collidepoint(mx, my):
                self._return_to_town()
                return None

            # Service buttons
            services = list(TEMPLE["services"].keys())
            by = 120
            for i, svc_key in enumerate(services):
                btn = pygame.Rect(SCREEN_W // 2 - 250, by + i * 80, 500, 68)
                if btn.collidepoint(mx, my):
                    self._use_temple_service(svc_key)
                    return None

            # Identify item clicks
            svc_count = len(services)
            unid_items = []
            for ci, c in enumerate(self.party):
                for ii, item in enumerate(c.inventory):
                    from core.identification import needs_identification
                    if needs_identification(item):
                        unid_items.append((ci, ii, item, c))

            if unid_items:
                uy = by + svc_count * 80 + 45
                for ui_idx, (ci, ii, item, char) in enumerate(unid_items[:5]):
                    row = pygame.Rect(SCREEN_W // 2 - 250, uy, 500, 40)
                    if row.collidepoint(mx, my):
                        self._temple_identify(ci, ii, item, char)
                        return None
                    uy += 44

        # ── Inn ──
        elif self.view == self.VIEW_INN:
            from core.progression import INN_TIERS, INN_TIER_ORDER

            back = pygame.Rect(SCREEN_W - 140, 20, 120, 34)
            if back.collidepoint(mx, my):
                self._return_to_town()
                self.inn_result = None
                return None

            by = 110
            for i, tier_key in enumerate(INN_TIER_ORDER):
                btn = pygame.Rect(SCREEN_W // 2 - 280, by + i * 95, 560, 85)
                if btn.collidepoint(mx, my):
                    from core.progression import can_level_up, training_cost
                    tier = INN_TIERS[tier_key]
                    room_cost = tier["cost_per_char"] * len(self.party)
                    # Include training cost upfront
                    train_cost = 0
                    if tier["allows_level_up"]:
                        for c in self.party:
                            if can_level_up(c):
                                train_cost += training_cost(c.level + 1)
                    total_cost = room_cost + train_cost
                    total_gold = sum(c.gold for c in self.party)
                    if total_gold >= total_cost:
                        success = self._rest_at_inn(tier_key, total_cost)
                        if success and self.levelup_queue:
                            self.view = self.VIEW_INN_LEVELUP
                        return "inn_save"  # signal to main.py to auto-save
                    else:
                        self._msg(f"Not enough gold! Need {total_cost}g.", RED)
                    return None

        # ── Inn Level Up ──
        elif self.view == self.VIEW_INN_LEVELUP:
            from core.progression import apply_level_up, training_cost, can_level_up
            from core.classes import STAT_NAMES, get_all_resources

            if not self.levelup_queue:
                self.view = self.VIEW_INN
                return None

            c = self.levelup_queue[self.levelup_current]

            # Stat selection buttons
            for i, stat in enumerate(STAT_NAMES):
                btn = pygame.Rect(SCREEN_W // 2 - 30, 130 + i * 38, 200, 32)
                if btn.collidepoint(mx, my):
                    self.levelup_free_stat = stat
                    return None

            # Confirm
            confirm = pygame.Rect(SCREEN_W // 2 + 200, 350, 180, 45)
            if confirm.collidepoint(mx, my) and self.levelup_free_stat:
                # Training cost already paid upfront at inn rest
                summary = apply_level_up(c, self.levelup_free_stat)
                if summary:
                    max_res = get_all_resources(c.class_name, c.stats, c.level)
                    for rn, mv in max_res.items():
                        if c.resources.get(rn, 0) > mv:
                            c.resources[rn] = mv
                    gains = ", ".join(f"+{v} {k}" for k, v in summary["stat_gains"].items())
                    ab_str = ""
                    if summary.get("new_abilities"):
                        ab_str = " Learned: " + ", ".join(summary["new_abilities"])
                    self.inn_result = f"{c.name} reached level {c.level}! {gains}, +{summary['hp_gain']} base HP{ab_str}"
                self.levelup_current += 1
                self.levelup_free_stat = None
                if self.levelup_current >= len(self.levelup_queue):
                    self.view = self.VIEW_INN
                return None

            skip = pygame.Rect(SCREEN_W // 2 + 200, 410, 180, 40)
            if skip.collidepoint(mx, my):
                self.levelup_current += 1
                self.levelup_free_stat = None
                if self.levelup_current >= len(self.levelup_queue):
                    self.view = self.VIEW_INN
                return None

        # ── Tavern ──
        elif self.view == self.VIEW_TAVERN:
            back = pygame.Rect(SCREEN_W - 140, 30, 120, 34)
            if back.collidepoint(mx, my):
                self._return_to_town()
                return None

            another = pygame.Rect(SCREEN_W // 2 - 100, 310, 200, 45)
            if another.collidepoint(mx, my):
                total_gold = sum(c.gold for c in self.party)
                if total_gold >= 1:
                    # Deduct 1g from whoever has it
                    for c in self.party:
                        if c.gold >= 1:
                            c.gold -= 1
                            break
                    self.current_rumor = random.choice(TAVERN["rumors"])
                    self._msg("You buy a round and hear a new rumor.", RUMOR_COL)
                else:
                    self._msg("You can't afford a drink!", RED)
                return None

        # ── Forge ──
        elif self.view in (self.VIEW_FORGE, self.VIEW_FORGE_CRAFT,
                           self.VIEW_FORGE_UPGRADE, self.VIEW_FORGE_ENCHANT):
            return self._handle_forge_click(mx, my)

        # ── Job Board ──
        elif self.view == self.VIEW_JOBBOARD:
            back = pygame.Rect(SCREEN_W - 140, 30, 120, 34)
            if back.collidepoint(mx, my):
                self._return_to_town()
                return None

            from data.job_board import accept_job, complete_job
            for btn, action, job_id in getattr(self, '_job_buttons', []):
                if btn.collidepoint(mx, my):
                    if action == "accept":
                        accept_job(job_id)
                        sfx.play("quest_accept")
                        self._msg("Job accepted!", (100, 220, 100))
                    elif action == "turnin":
                        reward = complete_job(job_id, self.party)
                        if reward:
                            sfx.play("quest_complete")
                            self._msg(f"Job complete! +{reward['gold']}g, +{reward['xp']} XP",
                                      GOLD)
                    return None

        return None

    # ─────────────────────────────────────────────────────────
    #  ACTIONS
    # ─────────────────────────────────────────────────────────

    def _buy_item(self, shop_item):
        """Buy an item. Deducts gold from party (first character who can pay)."""
        price = shop_item.get("buy_price", 0)
        total_gold = sum(c.gold for c in self.party)

        if total_gold < price:
            self._msg("Not enough gold!", RED)
            return

        # Deduct gold across party
        remaining = price
        for c in self.party:
            if remaining <= 0:
                break
            take = min(c.gold, remaining)
            c.gold -= take
            remaining -= take

        # Create a copy and give to first character (player can redistribute in inventory)
        new_item = dict(shop_item)
        # Remove shop-specific fields
        new_item.pop("buy_price", None)
        new_item.pop("sell_price", None)
        # Shop items are always identified
        new_item["identified"] = True
        from core.party_knowledge import mark_item_identified
        mark_item_identified(new_item.get("name", ""))
        self.party[0].inventory.append(new_item)

        self._msg(f"Bought {shop_item['name']} for {price}g — added to {self.party[0].name}'s inventory", BUY_COL)
        sfx.play("shop_buy")

    def _buy_back_item(self, sold_idx):
        """Buy back a previously sold item."""
        if sold_idx >= len(self.sold_items):
            return
        item = self.sold_items[sold_idx]
        price = item.get("buy_price", 0)
        total_gold = sum(c.gold for c in self.party)

        if total_gold < price:
            self._msg("Not enough gold!", RED)
            return

        # Deduct gold
        self._deduct_gold(price)

        # Remove from sold list
        self.sold_items.pop(sold_idx)

        # Create clean copy for inventory
        new_item = dict(item)
        new_item.pop("buy_price", None)
        new_item.pop("sell_price", None)
        new_item.pop("_buyback", None)
        self.party[0].add_item(new_item)

        name = get_item_display_name(new_item)
        self._msg(f"Bought back {name} for {price}g — added to {self.party[0].name}'s inventory", BUY_COL)

    def _sell_item(self, char, item_idx):
        """Sell an item from a character's inventory."""
        if item_idx >= len(char.inventory):
            return
        item = char.inventory[item_idx]
        sell_price = get_sell_price(item)
        char.inventory.pop(item_idx)
        char.gold += sell_price
        name = get_item_display_name(item)
        # Add to buyback list — buyback at sell price (same as what player received)
        buyback = dict(item)
        buyback["buy_price"] = sell_price
        buyback["_buyback"] = True
        self.sold_items.append(buyback)
        self._msg(f"Sold {name} for {sell_price}g", SELL_COL)
        sfx.play("shop_sell")

    def _use_temple_service(self, service_key):
        """Use a temple service."""
        svc = TEMPLE["services"][service_key]
        cost = svc["cost"]
        total_gold = sum(c.gold for c in self.party)

        if service_key == "cure_poison":
            # Find first poisoned character
            from core.status_effects import get_status_effects, remove_all_poison
            for c in self.party:
                effects = get_status_effects(c)
                if any(s.get("type") == "poison" for s in effects):
                    if total_gold < cost:
                        self._msg(f"Not enough gold! Need {cost}g.", RED)
                        return
                    self._deduct_gold(cost)
                    remove_all_poison(c)
                    self._msg(f"{c.name}'s poison has been purged! ({cost}g)", HEAL_COL)
                    return
            self._msg("No one in your party is poisoned.", GREY)

        elif service_key == "remove_curse":
            from core.status_effects import get_status_effects, remove_all_curses
            for c in self.party:
                effects = get_status_effects(c)
                if any(s.get("type") == "curse" for s in effects):
                    if total_gold < cost:
                        self._msg(f"Not enough gold! Need {cost}g.", RED)
                        return
                    self._deduct_gold(cost)
                    remove_all_curses(c)
                    self._msg(f"{c.name}'s curses have been lifted! ({cost}g)", HEAL_COL)
                    return
            self._msg("No one in your party is cursed.", GREY)

        elif service_key == "resurrect":
            # Find first dead character (HP <= 0 and marked dead)
            # For now, resurrect any character at 0 HP
            for c in self.party:
                if c.resources.get("HP", 0) <= 0:
                    actual_cost = 200 + 100 * c.level
                    if total_gold < actual_cost:
                        self._msg(f"Not enough gold! Need {actual_cost}g to resurrect {c.name}.", RED)
                        return
                    self._deduct_gold(actual_cost)
                    c.resources["HP"] = 1
                    from core.status_effects import add_resurrection_sickness, remove_all_poison
                    remove_all_poison(c)  # resurrection clears poison
                    add_resurrection_sickness(c)
                    # 1% chance of 5% max HP loss
                    import random
                    if random.random() < 0.01:
                        from core.classes import get_all_resources
                        max_res = get_all_resources(c.class_name, c.stats, c.level)
                        max_hp = max_res.get("HP", 100)
                        loss = max(1, int(max_hp * 0.05))
                        self._msg(f"{c.name} resurrected but weakened! (-{loss} max HP permanently) ({actual_cost}g)", ORANGE)
                    else:
                        self._msg(f"{c.name} has been resurrected! ({actual_cost}g) Rest at the inn to recover.", HEAL_COL)
                    return
            self._msg("No fallen party members to resurrect.", GREY)

        elif service_key == "identify_item":
            self._msg("Click an unidentified item below to identify it (15g each).", DIM_GOLD)

        elif service_key == "blessing":
            if total_gold < cost:
                self._msg(f"Not enough gold! Need {cost}g.", RED)
                return
            self._deduct_gold(cost)
            self._msg("The priests bless your party. May the Light guide your path! (+5% accuracy)", HEAL_COL)

    def _temple_identify(self, char_idx, item_idx, item, char):
        """Identify an item at the temple for gold."""
        cost = 15
        total_gold = sum(c.gold for c in self.party)
        if total_gold < cost:
            self._msg("Not enough gold to identify! Need 15g.", RED)
            return

        self._deduct_gold(cost)
        item["identified"] = True
        item["magic_identified"] = True
        item["material_identified"] = True
        name = get_item_display_name(item)
        # Register in party knowledge
        from core.party_knowledge import mark_item_identified
        mark_item_identified(name)
        self._msg(f"Identified: {name} (15g)", HEAL_COL)

    def _deduct_gold(self, amount):
        """Deduct gold across party members."""
        remaining = amount
        for c in self.party:
            if remaining <= 0:
                break
            take = min(c.gold, remaining)
            c.gold -= take
            remaining -= take

    def _msg(self, text, color=CREAM):
        self.message = text
        self.msg_color = color
        self.msg_timer = 3000

    # ─────────────────────────────────────────────────────────
    #  SCROLL
    # ─────────────────────────────────────────────────────────

    def handle_scroll(self, direction):
        if self.view == self.VIEW_SHOP_BUY:
            items = self.shop.get(self.shop_tab, [])
            max_s = max(0, len(items) - 8)
            if direction > 0:
                self.shop_scroll = min(max_s, self.shop_scroll + 1)
            else:
                self.shop_scroll = max(0, self.shop_scroll - 1)
        elif self.view == self.VIEW_SHOP_SELL:
            char = self.party[self.sell_char]
            max_s = max(0, len(char.inventory) - 8)
            if direction > 0:
                self.sell_scroll = min(max_s, self.sell_scroll + 1)
            else:
                self.sell_scroll = max(0, self.sell_scroll - 1)
        elif self.view in (self.VIEW_FORGE_CRAFT, self.VIEW_FORGE_UPGRADE,
                           self.VIEW_FORGE_ENCHANT):
            if direction > 0:
                self.forge_scroll = min(self.forge_scroll + 1, 50)
            else:
                self.forge_scroll = max(0, self.forge_scroll - 1)

    # ─────────────────────────────────────────────────────────
    #  FORGE — Craft, Upgrade, Enchant
    # ─────────────────────────────────────────────────────────

    def _draw_forge(self, surface, mx, my):
        from core.crafting import (
            RECIPES, ENCHANTMENTS, UPGRADE_COSTS, MAX_UPGRADE,
            can_afford_recipe, count_material, get_upgrade_level,
            get_upgrade_cost, get_upgradeable_items, get_enchantable_items,
            get_applicable_enchants, get_materials_of_tier,
        )

        FORGE_ORANGE = (255, 140, 40)
        FORGE_DIM = (160, 100, 40)

        draw_text(surface, "Dunn's Forge", SCREEN_W // 2 - 80, 15, FORGE_ORANGE, 24, bold=True)
        total_gold = sum(c.gold for c in self.party)
        draw_text(surface, f"Gold: {total_gold}", SCREEN_W - 150, 20, DIM_GOLD, 14)

        # Tab bar
        tabs = [("Craft", self.VIEW_FORGE_CRAFT),
                ("Upgrade", self.VIEW_FORGE_UPGRADE),
                ("Enchant", self.VIEW_FORGE_ENCHANT)]
        for i, (label, view) in enumerate(tabs):
            tr = pygame.Rect(20 + i * 140, 50, 130, 32)
            active = self.view == view or (self.view == self.VIEW_FORGE and i == 0)
            col = FORGE_ORANGE if active else FORGE_DIM
            pygame.draw.rect(surface, col, tr, 0 if active else 1, 4)
            tc = BLACK if active else col
            draw_text(surface, label, tr.x + 35, tr.y + 7, tc, 15, bold=active)

        # Back button
        back = pygame.Rect(SCREEN_W - 140, 50, 120, 34)
        pygame.draw.rect(surface, (100, 60, 60), back, 1, 4)
        draw_text(surface, "Back", back.x + 40, back.y + 8, RED, 14)

        # Materials summary bar
        draw_text(surface, "Materials:", 20, 90, GREY, 12)
        mx_pos = 100
        shown_mats = {}
        for c in self.party:
            for item in c.inventory:
                if item.get("type") == "material":
                    n = item.get("name", "?")
                    shown_mats[n] = shown_mats.get(n, 0) + item.get("quantity", 1)
        for mat_name, count in list(shown_mats.items())[:8]:
            short = mat_name[:12]
            draw_text(surface, f"{short}×{count}", mx_pos, 90, CREAM, 11)
            mx_pos += 110

        active_view = self.view if self.view != self.VIEW_FORGE else self.VIEW_FORGE_CRAFT
        y = 110

        if active_view == self.VIEW_FORGE_CRAFT:
            self._draw_forge_craft(surface, mx, my, y, RECIPES, total_gold, FORGE_ORANGE)
        elif active_view == self.VIEW_FORGE_UPGRADE:
            self._draw_forge_upgrade(surface, mx, my, y, total_gold, FORGE_ORANGE)
        elif active_view == self.VIEW_FORGE_ENCHANT:
            self._draw_forge_enchant(surface, mx, my, y, total_gold, FORGE_ORANGE)

    def _draw_forge_craft(self, surface, mx, my, y, recipes, total_gold, accent):
        from core.crafting import can_afford_recipe, count_material
        visible = recipes[self.forge_scroll:self.forge_scroll + 7]
        for i, recipe in enumerate(visible):
            ry = y + i * 72
            can = can_afford_recipe(self.party, recipe)
            box = pygame.Rect(20, ry, SCREEN_W - 40, 66)
            bc = (50, 40, 30) if can else (35, 30, 25)
            pygame.draw.rect(surface, bc, box, 0, 6)
            pygame.draw.rect(surface, accent if can else (60, 50, 40), box, 1, 6)

            # Item name and description
            res = recipe["result"]
            draw_text(surface, res["name"], 30, ry + 4, GOLD if can else GREY, 16, bold=True)
            desc = res.get("description", "")[:70]
            draw_text(surface, desc, 30, ry + 24, CREAM if can else (80, 70, 60), 12)

            # Cost
            cost_parts = [f"{recipe['gold']}g"]
            for mat, ct in recipe["materials"].items():
                have = count_material(self.party, mat)
                col_str = f"{mat}:{have}/{ct}"
                cost_parts.append(col_str)
            cost_text = "  |  ".join(cost_parts)
            draw_text(surface, cost_text, 30, ry + 44, (140, 120, 80) if can else (70, 60, 50), 11)

            # Craft button
            if can:
                btn = pygame.Rect(SCREEN_W - 120, ry + 16, 80, 30)
                pygame.draw.rect(surface, accent, btn, 0, 4)
                draw_text(surface, "Craft", btn.x + 18, btn.y + 6, BLACK, 14, bold=True)

    def _draw_forge_upgrade(self, surface, mx, my, y, total_gold, accent):
        from core.crafting import get_upgradeable_items, get_upgrade_cost, get_materials_of_tier
        items = get_upgradeable_items(self.party)
        if not items:
            draw_text(surface, "No weapons or armor to upgrade.", 30, y + 20, GREY, 15)
            draw_text(surface, "Equip or carry weapons/armor to upgrade them here.", 30, y + 45, (80, 70, 60), 13)
            return

        visible = items[self.forge_scroll:self.forge_scroll + 7]
        for i, (char, idx, item, loc) in enumerate(visible):
            ry = y + i * 62
            cost = get_upgrade_cost(item)
            if not cost:
                continue
            avail_mats = get_materials_of_tier(self.party, cost["min_material_tier"])
            total_mats = sum(avail_mats.values())
            can = total_gold >= cost["gold"] and total_mats >= cost["material_count"]

            box = pygame.Rect(20, ry, SCREEN_W - 40, 56)
            bc = (50, 40, 30) if can else (35, 30, 25)
            pygame.draw.rect(surface, bc, box, 0, 6)
            pygame.draw.rect(surface, accent if can else (60, 50, 40), box, 1, 6)

            lvl = item.get("upgrade_level", 0)
            draw_text(surface, f"{item['name']}", 30, ry + 4, GOLD if can else GREY, 15, bold=True)
            draw_text(surface, f"{char.name} ({loc})  |  +{lvl} → +{lvl+1}", 30, ry + 24, CREAM if can else (80,70,60), 12)
            draw_text(surface, f"Cost: {cost['gold']}g + {cost['material_count']} tier-{cost['min_material_tier']}+ materials (have {total_mats})",
                      30, ry + 40, (140,120,80) if can else (70,60,50), 11)

            if can:
                btn = pygame.Rect(SCREEN_W - 130, ry + 12, 90, 30)
                pygame.draw.rect(surface, accent, btn, 0, 4)
                draw_text(surface, "Upgrade", btn.x + 12, btn.y + 6, BLACK, 14, bold=True)

    def _draw_forge_enchant(self, surface, mx, my, y, total_gold, accent):
        from core.crafting import get_enchantable_items, get_applicable_enchants, ENCHANTMENTS, count_material

        items = get_enchantable_items(self.party)
        if not items:
            draw_text(surface, "No weapons or armor to enchant.", 30, y + 20, GREY, 15)
            return

        # Phase 1: item selection
        if self.forge_selected_item is None:
            draw_text(surface, "Select an item to enchant:", 30, y, CREAM, 14)
            y += 22
            visible = items[self.forge_scroll:self.forge_scroll + 8]
            for i, (char, idx, item, loc) in enumerate(visible):
                ry = y + i * 46
                box = pygame.Rect(20, ry, SCREEN_W - 40, 40)
                hover = box.collidepoint(mx, my)
                bc = (55, 45, 35) if hover else (40, 35, 28)
                pygame.draw.rect(surface, bc, box, 0, 5)
                ench_str = f" [{item.get('enchant_name','')}]" if item.get('enchant_name') else ""
                draw_text(surface, f"{item['name']}{ench_str}", 30, ry + 4, GOLD, 14)
                draw_text(surface, f"{char.name} ({loc})", 30, ry + 22, GREY, 11)
        else:
            # Phase 2: enchant selection
            item_idx = self.forge_selected_item
            if item_idx >= len(items):
                self.forge_selected_item = None
                return
            char, idx, item, loc = items[item_idx]
            draw_text(surface, f"Enchant: {item['name']}", 30, y, GOLD, 16, bold=True)
            draw_text(surface, f"({char.name})", 200, y + 2, GREY, 13)

            enchants = get_applicable_enchants(item)
            y += 26
            for i, ench_name in enumerate(enchants):
                ench = ENCHANTMENTS[ench_name]
                ry = y + i * 52
                # Check affordability
                can = total_gold >= ench["gold"]
                for mat, ct in ench["materials"].items():
                    if count_material(self.party, mat) < ct:
                        can = False

                box = pygame.Rect(20, ry, SCREEN_W - 40, 46)
                bc = (50, 40, 30) if can else (35, 30, 25)
                pygame.draw.rect(surface, bc, box, 0, 5)
                pygame.draw.rect(surface, accent if can else (60,50,40), box, 1, 5)

                draw_text(surface, ench_name, 30, ry + 4, GOLD if can else GREY, 15, bold=True)
                draw_text(surface, ench["desc"], 150, ry + 6, CREAM if can else (80,70,60), 12)
                cost_parts = [f"{ench['gold']}g"]
                for mat, ct in ench["materials"].items():
                    have = count_material(self.party, mat)
                    cost_parts.append(f"{mat}:{have}/{ct}")
                draw_text(surface, "  |  ".join(cost_parts), 30, ry + 26, (140,120,80) if can else (70,60,50), 11)

                if can:
                    btn = pygame.Rect(SCREEN_W - 130, ry + 8, 90, 28)
                    pygame.draw.rect(surface, accent, btn, 0, 4)
                    draw_text(surface, "Enchant", btn.x + 10, btn.y + 5, BLACK, 13, bold=True)

            # Cancel button
            cancel = pygame.Rect(20, y + len(enchants) * 52 + 10, 100, 30)
            pygame.draw.rect(surface, (80, 50, 50), cancel, 1, 4)
            draw_text(surface, "Cancel", cancel.x + 25, cancel.y + 7, RED, 13)

    def _handle_forge_click(self, mx, my):
        from core.crafting import (
            RECIPES, ENCHANTMENTS, can_afford_recipe, craft_item,
            get_upgradeable_items, get_upgrade_cost, apply_upgrade,
            consume_gold, consume_materials, get_materials_of_tier,
            get_enchantable_items, get_applicable_enchants, apply_enchant,
            count_material,
        )

        # Back button
        back = pygame.Rect(SCREEN_W - 140, 50, 120, 34)
        if back.collidepoint(mx, my):
            self._return_to_town()
            self.forge_selected_item = None
            return None

        # Tab clicks
        tabs = [(self.VIEW_FORGE_CRAFT, 20), (self.VIEW_FORGE_UPGRADE, 160),
                (self.VIEW_FORGE_ENCHANT, 300)]
        for view, tx in tabs:
            tr = pygame.Rect(tx, 50, 130, 32)
            if tr.collidepoint(mx, my):
                self.view = view
                self.forge_scroll = 0
                self.forge_selected_item = None
                return None

        active_view = self.view if self.view != self.VIEW_FORGE else self.VIEW_FORGE_CRAFT
        y = 110

        if active_view == self.VIEW_FORGE_CRAFT:
            visible = RECIPES[self.forge_scroll:self.forge_scroll + 7]
            for i, recipe in enumerate(visible):
                ry = y + i * 72
                if can_afford_recipe(self.party, recipe):
                    btn = pygame.Rect(SCREEN_W - 120, ry + 16, 80, 30)
                    if btn.collidepoint(mx, my):
                        result = craft_item(self.party, recipe)
                        if result:
                            self.party[0].inventory.append(result)
                            sfx.play("shop_buy")
                            self._msg(f"Crafted {result['name']}! Added to {self.party[0].name}'s inventory.", (255, 200, 80))
                        return None

        elif active_view == self.VIEW_FORGE_UPGRADE:
            items = get_upgradeable_items(self.party)
            visible = items[self.forge_scroll:self.forge_scroll + 7]
            for i, (char, idx, item, loc) in enumerate(visible):
                ry = y + i * 62
                cost = get_upgrade_cost(item)
                if not cost:
                    continue
                avail_mats = get_materials_of_tier(self.party, cost["min_material_tier"])
                total_mats = sum(avail_mats.values())
                can = sum(c.gold for c in self.party) >= cost["gold"] and total_mats >= cost["material_count"]
                if can:
                    btn = pygame.Rect(SCREEN_W - 130, ry + 12, 90, 30)
                    if btn.collidepoint(mx, my):
                        # Consume gold
                        consume_gold(self.party, cost["gold"])
                        # Consume materials (pick from available tier mats)
                        remaining = cost["material_count"]
                        for mat_name, have in avail_mats.items():
                            if remaining <= 0:
                                break
                            use = min(have, remaining)
                            consume_materials(self.party, {mat_name: use})
                            remaining -= use
                        old_name = item["name"]
                        apply_upgrade(item)
                        sfx.play("shop_buy")
                        self._msg(f"Upgraded {old_name} → {item['name']}!", (255, 200, 80))
                        return None

        elif active_view == self.VIEW_FORGE_ENCHANT:
            items = get_enchantable_items(self.party)
            if self.forge_selected_item is None:
                # Item selection phase
                visible = items[self.forge_scroll:self.forge_scroll + 8]
                y_start = y + 22
                for i, (char, idx, item, loc) in enumerate(visible):
                    ry = y_start + i * 46
                    box = pygame.Rect(20, ry, SCREEN_W - 40, 40)
                    if box.collidepoint(mx, my):
                        self.forge_selected_item = self.forge_scroll + i
                        return None
            else:
                # Enchant selection phase
                if self.forge_selected_item >= len(items):
                    self.forge_selected_item = None
                    return None
                char, idx, item, loc = items[self.forge_selected_item]
                enchants = get_applicable_enchants(item)
                ey = y + 26
                total_gold = sum(c.gold for c in self.party)
                for i, ench_name in enumerate(enchants):
                    ench = ENCHANTMENTS[ench_name]
                    ry = ey + i * 52
                    can = total_gold >= ench["gold"]
                    for mat, ct in ench["materials"].items():
                        if count_material(self.party, mat) < ct:
                            can = False
                    if can:
                        btn = pygame.Rect(SCREEN_W - 130, ry + 8, 90, 28)
                        if btn.collidepoint(mx, my):
                            consume_gold(self.party, ench["gold"])
                            consume_materials(self.party, ench["materials"])
                            old_name = item["name"]
                            apply_enchant(item, ench_name)
                            sfx.play("quest_complete")
                            self._msg(f"Enchanted! {old_name} → {item['name']}", (180, 140, 255))
                            self.forge_selected_item = None
                            return None

                # Cancel button
                cancel = pygame.Rect(20, ey + len(enchants) * 52 + 10, 100, 30)
                if cancel.collidepoint(mx, my):
                    self.forge_selected_item = None
                    return None

        return None
