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
    "greenwood": {
        "name": "Greenwood",
        "desc": "A remote wilderness outpost. Few roads lead here.",
    },
    "saltmere": {
        "name": "Saltmere",
        "desc": "A rough port town where no questions are asked.",
    },
    "sanctum": {
        "name": "Sanctum",
        "desc": "A holy city built around the Grand Cathedral of Light.",
    },
    "crystalspire": {
        "name": "Crystalspire",
        "desc": "City of towers and ley lines. Home of the Mage Academy.",
    },
    "thornhaven": {
        "name": "Thornhaven — Capital of Aldenmere",
        "desc": "The seat of the Governor's power. The largest city in the realm.",
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
    VIEW_INN_LEVELUP_RESULT = "inn_levelup_result"   # fanfare screen
    VIEW_BRANCH_CHOICE = "branch_choice"              # ability fork selection
    VIEW_CLASSTREE = "classtree"                      # class progression viewer
    VIEW_FORGE = "forge"
    VIEW_FORGE_CRAFT = "forge_craft"
    VIEW_JOBBOARD = "jobboard"
    VIEW_FORGE_UPGRADE = "forge_upgrade"
    VIEW_FORGE_ENCHANT = "forge_enchant"
    VIEW_FORGE_REPAIR  = "forge_repair"
    VIEW_GUILD = "guild"
    VIEW_GUILD_TRANSITION = "guild_transition"

    def __init__(self, party, town_id="briarhollow"):
        self.party = party
        self.message = ""
        self.msg_timer = 0
        self.msg_color = CREAM
        self.finished = False
        self.pending_quest_completions = []  # drained by Game._notify_quests_done each draw

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
        self.levelup_summary = None  # result dict from apply_level_up (for fanfare)
        self.branch_pending_char = None  # character awaiting branch choice
        self.branch_pending_opts = None  # [opt_A, opt_B] for branch screen
        self.branch_hover_idx = -1       # hovered option index
        # Class tree viewer
        self.classtree_char_idx = 0  # which party member to show

        # Tavern state
        self.tavern_drinks = {}      # patron_name -> drinks bought (int)
        self.tavern_selected = 0     # index of selected patron/tab
        self.tavern_tab = "patrons"  # "patrons" | "recruit" | "party"
        self.tavern_recruit_sel = 0
        self.tavern_party_sel = 0

        # NPC dialogue state
        self.active_dialogue = None  # DialogueUI when talking to an NPC
        self.town_id = town_id
        party_classes = [c.class_name for c in party if hasattr(c, "class_name")]
        self.shop = get_town_shop(town_id, party_classes)  # Town-specific shop inventory

        # Forge state
        self.forge_scroll = 0
        self.forge_item_scroll = 0
        self.forge_selected_item = None
        self.forge_selected_enchant = None

        # Always use hub menu — walkable town removed
        self.town_data = None
        # Safe defaults for walk attributes (walk mode disabled but referenced in draw)
        self.walk_x = 0
        self.walk_y = 0
        self.walk_facing = "down"
        self.walk_anim_t = 0
        self.walk_interact_msg = ""
        self.walk_interact_timer = 0
        self.current_bld_indoor_npc   = None
        self.current_bld_name         = ""
        self._bld_npc_portrait_rect   = None
        self.walk_tile_size = 24
        # Load walkable map data if this town has one
        from data.town_maps import get_town_data
        self.town_data = get_town_data(self.town_id)
        if self.town_data:
            spawn = self.town_data.get("spawn", (2, 2))
            self.walk_x, self.walk_y = spawn
        self._return_to_town()

    # ─────────────────────────────────────────────────────────
    #  MAIN DRAW
    # ─────────────────────────────────────────────────────────

    def draw(self, surface, mx, my, dt):
        self.msg_timer = max(0, self.msg_timer - dt)
        if getattr(self, "_inn_save_timer", 0) > 0:
            self._inn_save_timer = max(0, self._inn_save_timer - dt)

        # If dialogue is active, render it instead
        if self.active_dialogue and not self.active_dialogue.finished:
            self.active_dialogue.draw(surface, mx, my, dt)
            return

        # Clear dialogue if finished — distribute any quest rewards
        if self.active_dialogue and self.active_dialogue.finished:
            self.active_dialogue = None
            try:
                from core.story_flags import auto_advance_quests
                done = auto_advance_quests(self.party)
                self.pending_quest_completions.extend(done)
            except Exception:
                pass

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
        elif self.view == self.VIEW_INN_LEVELUP_RESULT:
            self._draw_levelup_result(surface, mx, my)
        elif self.view == self.VIEW_BRANCH_CHOICE:
            self._draw_branch_choice(surface, mx, my)
        elif self.view == self.VIEW_CLASSTREE:
            self._draw_classtree(surface, mx, my)
        elif self.view in (self.VIEW_FORGE, self.VIEW_FORGE_CRAFT,
                           self.VIEW_FORGE_UPGRADE, self.VIEW_FORGE_ENCHANT,
                           self.VIEW_FORGE_REPAIR):
            self._draw_forge(surface, mx, my)
        elif self.view == self.VIEW_JOBBOARD:
            self._draw_jobboard(surface, mx, my)
        elif self.view in (self.VIEW_GUILD, self.VIEW_GUILD_TRANSITION):
            self._draw_guild(surface, mx, my)

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
            ("Job Board", "Browse available quests and contracts",
             (40, 80, 60), (80, 200, 120)),
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
                draw_text(surface, npc_data["name"], nr.x + 56, nr.y + 6, CREAM, 16, bold=True)
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
            draw_text(surface, c.name, cx, bar_y + 8, cls["color"], 15, bold=True)
            draw_text(surface, f"Lv.{c.level} {c.class_name}", cx, bar_y + 24, GREY, 13)
            hp = c.resources.get("HP", 0)
            draw_text(surface, f"HP: {hp}  Gold: {c.gold}  Items: {len(c.inventory)}",
                      cx, bar_y + 40, DIM_GREEN, 11)

            # Status effect indicators
            from core.status_effects import get_status_display
            statuses = get_status_display(c)
            if statuses:
                sx = cx
                for sname, scolor in statuses[:3]:  # max 3 shown
                    draw_text(surface, sname, sx, bar_y + 56, scolor, 11)
                    sx += 80

    # ─────────────────────────────────────────────────────────
    #  WALKABLE TOWN MAP
    # ─────────────────────────────────────────────────────────

    def _draw_walk(self, surface, mx, my):
        from data.town_maps import (
            TILE_COLORS, TILE_TOP_COLORS, TT_GRASS, TT_WALL, TT_TREE, TT_DOOR,
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

        # ══════════════════════════════════════════════════════════
        # TILE PASS — ground, paths, trees, water, special tiles
        # ══════════════════════════════════════════════════════════
        from data.town_maps import (
            TILE_COLORS, TILE_TOP_COLORS, TT_GRASS, TT_WALL, TT_DOOR,
            TT_TREE, TT_FENCE, TT_PATH, TT_EXIT, TT_SIGN, TT_WATER,
            TT_BRIDGE, get_tile, get_building_at, get_npc_at,
            get_sign_at,
        )

        td = self.town_data
        ts = self.walk_tile_size
        tw, th = td["width"], td["height"]

        map_area_h = SCREEN_H - 110
        cam_x = self.walk_x - (SCREEN_W // ts) // 2
        cam_y = self.walk_y - (map_area_h // ts) // 2
        cam_x = max(0, min(tw - SCREEN_W // ts, cam_x))
        cam_y = max(0, min(th - map_area_h // ts, cam_y))

        # pre-build building-to-wall-tile map for fast facade lookup
        bld_col_map = {}
        for bld in td["buildings"].values():
            c0, c1 = bld.get("wall_cols", (0, 0))
            r0, r1 = bld.get("wall_rows", (0, 0))
            for wr in range(r0, r1 + 1):
                for wc in range(c0, c1 + 1):
                    bld_col_map[(wc, wr)] = bld

        for sy in range(map_area_h // ts + 2):
            for sx in range(SCREEN_W // ts + 2):
                tx = cam_x + sx
                ty = cam_y + sy
                if not (0 <= ty < th and 0 <= tx < tw):
                    continue
                tile = td["map"][ty][tx] if tx < len(td["map"][ty]) else TT_WALL
                px = sx * ts
                py = sy * ts

                if tile == TT_GRASS:
                    shade = 3 if (tx + ty) % 2 == 0 else 0
                    # If this grass tile is directly adjacent to a door, render as a path stub
                    # so there is a visual walkway connection to every building entrance.
                    adj_door = any(
                        get_tile(td, tx+_dx, ty+_dy) == TT_DOOR
                        for _dx, _dy in ((-1,0),(1,0),(0,-1),(0,1))
                    )
                    if adj_door:
                        pygame.draw.rect(surface, (88, 75, 56), (px, py, ts, ts))
                        stone_sz = max(3, ts // 3 - 1)
                        for ox, oy in [(1, 1), (ts//2, 1), (1, ts//2), (ts//2, ts//2)]:
                            sc2 = (98, 84, 62) if (ox+oy)%2==0 else (80,68,50)
                            pygame.draw.rect(surface, sc2, (px+ox, py+oy, stone_sz, stone_sz), border_radius=1)
                    else:
                        pygame.draw.rect(surface, (52 + shade, 78 + shade, 42 + shade), (px, py, ts, ts))
                        if (tx * 7 + ty * 13) % 11 == 0:
                            pygame.draw.line(surface, (38, 62, 30),
                                (px + ts//3, py + ts//2), (px + ts//3 - 2, py + ts//4), 1)
                            pygame.draw.line(surface, (38, 62, 30),
                                (px + ts*2//3, py + ts//2), (px + ts*2//3 + 2, py + ts//4), 1)

                elif tile == TT_PATH:
                    pygame.draw.rect(surface, (95, 82, 62), (px, py, ts, ts))
                    stone_sz = max(4, ts // 3 - 1)
                    for ox, oy in [(1, 1), (ts//2, 1), (1, ts//2), (ts//2, ts//2)]:
                        sc2 = (105, 90, 68) if (ox + oy) % 2 == 0 else (88, 76, 56)
                        pygame.draw.rect(surface, sc2, (px+ox, py+oy, stone_sz, stone_sz), border_radius=1)
                        pygame.draw.rect(surface, (70, 60, 44), (px+ox, py+oy, stone_sz, stone_sz), 1, border_radius=1)

                elif tile == TT_TREE:
                    pygame.draw.rect(surface, (28, 48, 22), (px, py, ts, ts))

                elif tile == TT_WATER:
                    shimmer = abs(((self.walk_anim_t + tx * 200) % 1500) - 750) / 750.0
                    wc2 = (35 + int(12 * shimmer), 55 + int(10 * shimmer), 125 + int(20 * shimmer))
                    pygame.draw.rect(surface, wc2, (px, py, ts, ts))
                    ry2 = py + ts // 3
                    rx2 = int(px + ts * 0.15 + shimmer * ts * 0.3)
                    pygame.draw.line(surface, (55, 80, 160), (rx2, ry2), (rx2 + ts//2, ry2), 1)

                elif tile == TT_BRIDGE:
                    pygame.draw.rect(surface, (100, 78, 50), (px, py, ts, ts))
                    for pi in range(3):
                        ply2 = py + pi * (ts//3) + ts//8
                        pygame.draw.rect(surface, (125, 98, 62), (px+2, ply2, ts-4, max(2, ts//4)))

                elif tile == TT_EXIT:
                    pygame.draw.rect(surface, (60, 110, 55), (px, py, ts, ts))
                    pulse = abs((self.walk_anim_t % 2000) - 1000) / 1000.0
                    s2 = pygame.Surface((ts, ts), pygame.SRCALPHA)
                    s2.fill((100, 220, 90, int(20 + 30 * pulse)))
                    surface.blit(s2, (px, py))

                elif tile == TT_SIGN:
                    pygame.draw.rect(surface, (90, 78, 55), (px, py, ts, ts))
                    pygame.draw.rect(surface, (80, 64, 40), (px + ts//2 - 1, py + ts//3, 2, ts*2//3))
                    pygame.draw.rect(surface, (140, 112, 68),
                        (px + ts//5, py + ts//6, ts*3//5, ts//3), border_radius=2)
                    pygame.draw.rect(surface, (100, 80, 46),
                        (px + ts//5, py + ts//6, ts*3//5, ts//3), 1, border_radius=2)

                elif tile == TT_WALL:
                    bld = bld_col_map.get((tx, ty))
                    if bld:
                        bc = bld["color"]
                        r0_b, r1_b = bld.get("wall_rows", (ty, ty))
                        c0_b, c1_b = bld.get("wall_cols", (tx, tx))
                        door_x = bld["door"][0]
                        is_top_row    = (ty == r0_b)
                        is_left_col   = (tx == c0_b)
                        is_right_col  = (tx == c1_b)

                        wall_c = tuple(min(255, int(c * 0.85)) for c in bc)
                        pygame.draw.rect(surface, wall_c, (px, py, ts, ts))

                        if is_top_row:
                            roof_c = tuple(max(0, int(c * 0.55)) for c in bc)
                            pygame.draw.rect(surface, roof_c, (px, py, ts, ts//3))
                            pygame.draw.line(surface, tuple(max(0, c-30) for c in roof_c),
                                             (px, py + ts//3), (px+ts, py+ts//3), 1)

                        mortar_c = tuple(max(0, int(c * 0.6)) for c in bc)
                        for ml in range(1, 3):
                            pygame.draw.line(surface, mortar_c,
                                (px, py + ml * ts//3), (px+ts, py + ml * ts//3), 1)

                        if is_left_col or is_right_col:
                            pillar_c = tuple(min(255, int(c * 1.15)) for c in bc)
                            pygame.draw.rect(surface, pillar_c, (px, py, max(3, ts//4), ts))

                        if (r0_b + 1 <= ty <= r1_b - 1 and not is_left_col
                                and not is_right_col and tx != door_x
                                and (tx - c0_b) % 3 == 1):
                            win_m = max(3, ts//4)
                            wx, wy = px + win_m, py + win_m
                            ww, wh = ts - win_m*2, ts - win_m*2
                            pygame.draw.rect(surface, tuple(max(0, c-40) for c in bc), (wx, wy, ww, wh))
                            glass_c = (180, 210, 230) if bld.get("type") != "forge" else (220, 160, 80)
                            pygame.draw.rect(surface, glass_c, (wx+2, wy+2, ww-4, wh-4))
                            pygame.draw.line(surface, tuple(max(0, c-40) for c in bc),
                                (wx+ww//2, wy), (wx+ww//2, wy+wh), 1)
                            pygame.draw.line(surface, tuple(max(0, c-40) for c in bc),
                                (wx, wy+wh//2), (wx+ww, wy+wh//2), 1)

                        if bld.get("type") == "forge" and is_top_row and tx == c1_b - 1:
                            for si in range(3):
                                drift = int(((self.walk_anim_t // 300 + si) % 6) - 3)
                                sa = max(0, 80 - si * 20)
                                sc3 = pygame.Surface((ts//2, ts//3), pygame.SRCALPHA)
                                sc3.fill((80, 80, 80, sa))
                                surface.blit(sc3, (px + ts//4 + drift, py - ts//3 - si * ts//3))
                    else:
                        pygame.draw.rect(surface, (62, 50, 38), (px, py, ts, ts))
                        pygame.draw.rect(surface, (75, 62, 48), (px, py, ts, ts//3))

                elif tile == TT_DOOR:
                    bld2 = get_building_at(td, tx, ty)
                    bc2 = bld2[1]["color"] if bld2 else (140, 110, 60)
                    pygame.draw.rect(surface, tuple(max(0, int(c*0.6)) for c in bc2), (px, py, ts, ts))
                    pygame.draw.rect(surface, tuple(max(0, int(c*0.5)) for c in bc2), (px+2, py+1, ts-4, ts-2))
                    pygame.draw.rect(surface, tuple(min(255, int(c*1.1)) for c in bc2),
                        (px + ts//5, py + ts//10, ts*3//5, ts*4//5), border_radius=2)
                    pygame.draw.rect(surface, tuple(max(0, int(c*0.5)) for c in bc2),
                        (px + ts//5, py + ts//10, ts*3//5, ts*4//5), 1, border_radius=2)
                    pygame.draw.circle(surface, (220, 185, 90),
                        (px + ts*3//4, py + ts//2), max(2, ts//7))
                    pygame.draw.rect(surface, tuple(max(0, int(c*0.7)) for c in bc2), (px, py, ts, ts//5))

                else:
                    # '.' open tiles adjacent to doors also show a path stub
                    adj_door2 = any(
                        get_tile(td, tx+_dx, ty+_dy) == TT_DOOR
                        for _dx, _dy in ((-1,0),(1,0),(0,-1),(0,1))
                    )
                    if adj_door2:
                        pygame.draw.rect(surface, (88, 75, 56), (px, py, ts, ts))
                        stone_sz = max(3, ts // 3 - 1)
                        for ox, oy in [(1, 1), (ts//2, 1), (1, ts//2), (ts//2, ts//2)]:
                            sc2 = (98, 84, 62) if (ox+oy)%2==0 else (80,68,50)
                            pygame.draw.rect(surface, sc2, (px+ox, py+oy, stone_sz, stone_sz), border_radius=1)
                    else:
                        pygame.draw.rect(surface, (40, 35, 28), (px, py, ts, ts))

                if tile not in (TT_WALL, TT_TREE):
                    ec = TILE_COLORS.get(tile, (40,40,40))
                    pygame.draw.rect(surface, tuple(max(0, ec[i]-12) for i in range(3)), (px, py, ts, ts), 1)

        # ══ TREE CANOPY PASS ══
        for sy in range(map_area_h // ts + 2):
            for sx in range(SCREEN_W // ts + 2):
                tx = cam_x + sx
                ty = cam_y + sy
                if not (0 <= ty < th and 0 <= tx < tw):
                    continue
                tile = td["map"][ty][tx] if tx < len(td["map"][ty]) else TT_WALL
                if tile != TT_TREE:
                    continue
                px = sx * ts
                py = sy * ts
                pygame.draw.rect(surface, (62, 42, 24), (px + ts*3//8, py + ts//2, ts//4, ts//2))
                canopy_c  = (38 + (tx*5+ty*7)%18, 72 + (tx*3+ty*11)%20, 28)
                canopy_hi = tuple(min(255, c+22) for c in canopy_c)
                r_can = max(6, ts*5//8)
                pygame.draw.circle(surface, canopy_c,  (px+ts//2, py+ts*2//5), r_can)
                pygame.draw.circle(surface, canopy_hi, (px+ts//2, py+ts*2//5), r_can, 2)
                shd = pygame.Surface((ts, ts//3), pygame.SRCALPHA)
                shd.fill((0, 0, 0, 40))
                surface.blit(shd, (px, py + ts//2))

        # ══ NPC PASS ══
        for npc in td.get("npcs", []):
            hide_flag = npc.get("hide_if")
            if hide_flag:
                from core.story_flags import get_flag
                if get_flag(hide_flag):
                    continue
            nx, ny = npc["x"], npc["y"]
            npx2 = (nx - cam_x) * ts
            npy2 = (ny - cam_y) * ts
            if not (0 <= npx2 < SCREEN_W and -ts <= npy2 < map_area_h):
                continue

            nc2   = npc.get("color", (180, 180, 180))
            ntype = npc.get("npc_type", "default")
            dark2 = tuple(max(0, int(c*0.5)) for c in nc2)
            light2= tuple(min(255, int(c*1.25)) for c in nc2)
            ncx   = npx2 + ts//2
            ncy   = npy2 + ts//2

            shd2 = pygame.Surface((ts, ts//4), pygame.SRCALPHA)
            shd2.fill((0, 0, 0, 50))
            surface.blit(shd2, (npx2, npy2 + ts*3//4))

            body_w2 = max(6, ts*5//12)
            body_h2 = max(8, ts*5//12)
            bx2 = ncx - body_w2//2
            by2 = ncy - body_h2//8
            pygame.draw.rect(surface, nc2, (bx2, by2, body_w2, body_h2), border_radius=2)
            pygame.draw.line(surface, dark2, (ncx, by2+2), (ncx, by2+body_h2-2), 1)
            pygame.draw.rect(surface, nc2, (bx2-2, by2+2, 3, body_h2//2), border_radius=1)
            pygame.draw.rect(surface, nc2, (bx2+body_w2-1, by2+2, 3, body_h2//2), border_radius=1)

            head_r2 = max(4, ts*3//14)
            hcx = ncx
            hcy = by2 - head_r2 + 2
            pygame.draw.circle(surface, (220, 185, 155), (hcx, hcy), head_r2)
            pygame.draw.circle(surface, dark2, (hcx, hcy), head_r2, 1)

            if ntype == "guard":
                pygame.draw.ellipse(surface, (130, 145, 175),
                    (hcx-head_r2, hcy-head_r2, head_r2*2, head_r2+2))
                pygame.draw.rect(surface, (110, 125, 155),
                    (hcx-head_r2-2, hcy, head_r2*2+4, 3))
            elif ntype == "elder":
                pygame.draw.arc(surface, (180, 175, 170),
                    pygame.Rect(hcx-head_r2, hcy-head_r2, head_r2*2, head_r2*2),
                    0, 3.14, max(1, head_r2//2))
            elif ntype == "priestess":
                vl = pygame.Surface((head_r2*2+4, head_r2*2+4), pygame.SRCALPHA)
                pygame.draw.ellipse(vl, (240, 235, 200, 170),
                    (0, 0, head_r2*2+4, head_r2*2+4))
                surface.blit(vl, (hcx-head_r2-2, hcy-head_r2-2))
            elif ntype == "merchant":
                pygame.draw.ellipse(surface, dark2,
                    (hcx-head_r2-3, hcy-1, head_r2*2+6, 4))
                pygame.draw.ellipse(surface, nc2,
                    (hcx-head_r2+1, hcy-head_r2-2, head_r2*2-2, head_r2+2))
            elif ntype == "innkeeper":
                pygame.draw.rect(surface, (235, 230, 215),
                    (bx2+2, by2+body_h2//3, body_w2-4, body_h2*2//3), border_radius=1)
            elif ntype == "forger":
                pygame.draw.rect(surface, (90, 64, 30),
                    (bx2, by2+body_h2//4, body_w2, body_h2*3//4))
            elif ntype == "mage":
                hat_pts = [(ncx, hcy-head_r2*2), (ncx-head_r2, hcy), (ncx+head_r2, hcy)]
                pygame.draw.polygon(surface, nc2, hat_pts)
                pygame.draw.polygon(surface, dark2, hat_pts, 1)
            elif ntype == "barkeep":
                pygame.draw.ellipse(surface, (155, 105, 50),
                    (hcx-head_r2+1, hcy+head_r2//2, head_r2*2-2, head_r2))

            if npc.get("service"):
                badge_txt = {"inn":"INN","shop":"SHOP","forge":"FORGE",
                             "temple":"SHRINE","tavern":"TAVERN"}.get(npc["service"],"")
                if badge_txt:
                    iw2 = get_font(8).size(badge_txt)[0]
                    bdg = pygame.Rect(ncx - iw2//2 - 3, npy2 - 14, iw2+6, 10)
                    pygame.draw.rect(surface, (20, 16, 10), bdg, border_radius=2)
                    pygame.draw.rect(surface, nc2, bdg, 1, border_radius=2)
                    draw_text(surface, badge_txt, ncx - iw2//2, npy2 - 13, nc2, 8)

            dist2 = abs(nx - self.walk_x) + abs(ny - self.walk_y)
            if dist2 <= 3:
                nw2 = get_font(10).size(npc["name"])[0]
                draw_text(surface, npc["name"], ncx - nw2//2, npy2 - 24, light2, 10)

        # ══ PLAYER PASS ══
        ppx = (self.walk_x - cam_x) * ts
        ppy = (self.walk_y - cam_y) * ts
        pcx, pcy = ppx + ts//2, ppy + ts//2

        pshd = pygame.Surface((ts, ts//4), pygame.SRCALPHA)
        pshd.fill((0, 0, 0, 60))
        surface.blit(pshd, (ppx, ppy + ts*3//4))
        pygame.draw.rect(surface, (80, 65, 30),
            (pcx-ts//4, pcy, ts//2, ts*5//12), border_radius=2)
        pygame.draw.rect(surface, (200, 175, 80),
            (pcx-ts//5, pcy+2, ts*2//5, ts*5//12-4), border_radius=2)
        pygame.draw.circle(surface, (225, 190, 155), (pcx, pcy-ts//5), max(5, ts*3//14))
        pygame.draw.circle(surface, (180, 150, 80), (pcx, pcy-ts//5), max(5, ts*3//14), 1)
        dx_map2 = {"up":(0,-1),"down":(0,1),"left":(-1,0),"right":(1,0)}
        fdx2, fdy2 = dx_map2.get(self.walk_facing, (0,1))
        pygame.draw.circle(surface, (255, 240, 120),
            (pcx + fdx2*ts//4, pcy - ts//5 + fdy2*ts//4), max(2, ts//8))

        # Building name labels over facades
        for bld_id, bld in td["buildings"].items():
            lx2, ly2 = bld.get("label_pos", bld["door"])
            lpx3 = (lx2 - cam_x) * ts
            lpy3 = (ly2 - cam_y) * ts + ts//3
            if 0 <= lpx3 < SCREEN_W and 0 <= lpy3 < map_area_h:
                bname2 = bld["name"]
                bw2 = get_font(11).size(bname2)[0]
                lbg2 = pygame.Surface((bw2+8, 14), pygame.SRCALPHA)
                lbg2.fill((10, 8, 5, 160))
                surface.blit(lbg2, (lpx3 - bw2//2 - 4, lpy3 - 1))
                draw_text(surface, bname2, lpx3 - bw2//2, lpy3, bld["color"], 11, bold=True)


        # ── UI bar at bottom ──
        bar_y = map_area_h
        pygame.draw.rect(surface, (12, 10, 25), (0, bar_y, SCREEN_W, SCREEN_H - bar_y))
        pygame.draw.line(surface, PANEL_BORDER, (0, bar_y), (SCREEN_W, bar_y))

        # Town name + gold (left side)
        draw_text(surface, td["name"], 14, bar_y + 6, GOLD, 16, bold=True)
        total_gold = sum(c.gold for c in self.party)
        draw_text(surface, f"✦ {total_gold}g", 14, bar_y + 26, DIM_GOLD, 14)

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
            draw_text(surface, c.name[:5], cx, bar_y + 6, cls["color"], 12, bold=True)
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
            draw_text(surface, f"HP {hp}/{max_hp}", cx, bar_y + 29, hp_color, 11)
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

        return ""

    def handle_key(self, key):
        """Handle keyboard input. Returns 'exit' to leave town, or None."""
        if self.view != self.VIEW_WALK:
            return None

        # Dialogue takes priority — forward key events to dialogue UI
        if self.active_dialogue and not self.active_dialogue.finished:
            import pygame as _pg
            event = _pg.event.Event(_pg.KEYDOWN, key=key, mod=0, unicode="")
            self.active_dialogue.handle_event(event)
            if self.active_dialogue.finished:
                self.active_dialogue = None
                try:
                    from core.story_flags import auto_advance_quests
                    done = auto_advance_quests(self.party)
                    self.pending_quest_completions.extend(done)
                except Exception:
                    pass
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
            npc_ahead = get_npc_at(td, nx, ny)
            is_service_npc = npc_ahead is not None and npc_ahead.get("service") is not None

            # All NPCs block movement; interact with ENTER when facing them
            npc_blocking = npc_ahead is not None
            if is_walkable(td, nx, ny) and not npc_blocking:
                self.walk_x = nx
                self.walk_y = ny
                sfx.play("step")
                # Auto-enter when stepping onto a door tile
                if get_tile(td, nx, ny) == TT_DOOR:
                    return self._walk_interact()

        return None

    def _walk_interact(self):
        """Handle ENTER press while walking. Returns 'exit' or None."""
        from data.town_maps import (
            get_building_at, get_npc_at, get_sign_at, is_exit,
            get_tile, TT_DOOR, BLD_INN, BLD_SHOP, BLD_TEMPLE,
            BLD_TAVERN, BLD_FORGE, BLD_HOUSE, BLD_JOBBOARD, BLD_GUILD,
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

                # Store indoor NPC and building name for service views
                self.current_bld_indoor_npc = bld.get("indoor_npc")
                self.current_bld_name       = bld.get("name", "building")

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
                elif btype == BLD_GUILD:
                    self._enter_guild(bld)
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
        if npc:
            sfx.play("npc_talk")

            # Service NPC — gives a greeting but does NOT open menu.
            # Enter the building door to access services.
            service = npc.get("service")
            greetings = {
                "inn":    lambda n: f"{n}: \"Rooms available inside — go on in!\"",
                "shop":   lambda n: f"{n}: \"Come inside, I'll get you a good price.\"",
                "temple": lambda n: f"{n}: \"The shrine is open. Enter freely.\"",
                "tavern": lambda n: f"{n}: \"Step inside — it's warmer in there!\"",
                "forge":  lambda n: f"{n}: \"Workshop's through the door if you need work done.\"",
            }
            if service and service in greetings:
                self._show_walk_msg(greetings[service](npc["name"]),
                                    npc.get("color", CREAM))
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

    def _draw_bld_npc_header(self, surface, bld_name, subtitle="", mx=0, my=0):
        """Draw building title + indoor NPC portrait card at top of service views.
        Portrait is on the LEFT so it never overlaps the Back button (top-right).
        Click handling is done in handle_click via self._bld_npc_portrait_rect."""
        draw_text(surface, bld_name, 220, 18, GOLD, 22, bold=True)
        if subtitle:
            draw_text(surface, subtitle, 220, 46, GREY, 13)

        npc = self.current_bld_indoor_npc
        self._bld_npc_portrait_rect = None
        if not npc:
            return

        _npc_class = {
            "innkeeper": "Cleric",      "merchant":    "Thief",
            "barkeep":   "Fighter",     "priestess":   "High Priest",
            "priest":    "High Priest", "forger":      "Champion",
            "guildmaster": "Archmage",  "ranger":      "Ranger",
            "elder":     "Mage",        "guard":       "Fighter",
        }
        cls = _npc_class.get(npc.get("npc_type", ""), "Fighter")
        col = npc.get("color", CREAM)
        did = npc.get("dialogue_id")

        # Portrait card — LEFT side, y=8 so it sits under the title area
        pr = pygame.Rect(8, 8, 200, 62)
        self._bld_npc_portrait_rect = pr if did else None
        hover = did and pr.collidepoint(mx, my)
        bg_col = (38, 28, 50) if hover else (22, 16, 32)
        border_col = col if hover else PANEL_BORDER
        pygame.draw.rect(surface, bg_col, pr, border_radius=5)
        pygame.draw.rect(surface, border_col, pr, 1, border_radius=5)

        from ui.pixel_art import draw_character_silhouette
        sil_r = pygame.Rect(pr.x + 4, pr.y + 5, 36, 52)
        draw_character_silhouette(surface, sil_r, cls, highlight=bool(hover))

        draw_text(surface, npc["name"],          pr.x + 44, pr.y + 7,  CREAM,  12, bold=True)
        draw_text(surface, npc.get("title", ""), pr.x + 44, pr.y + 21, GREY,   11)
        if did:
            talk_lbl = "[ Talk → ]" if hover else "[ Talk ]"
            draw_text(surface, talk_lbl, pr.x + 44, pr.y + 36, col if hover else DIM_GOLD, 11)
        else:
            draw_text(surface, "\"Hello, travellers.\"", pr.x + 44, pr.y + 36, DIM_GOLD, 10)


    def _open_indoor_npc_dialogue(self):
        """Open dialogue for the current building's indoor NPC (if they have one)."""
        npc = self.current_bld_indoor_npc
        if not npc:
            return
        did = npc.get("dialogue_id")
        if not did:
            self._show_walk_msg(npc.get("description", f"{npc['name']} has nothing to say."), npc.get("color", CREAM))
            return
        from data.story_data import NPC_DIALOGUES
        from core.dialogue import select_dialogue
        from ui.dialogue_ui import DialogueUI
        dialogues = NPC_DIALOGUES.get(did, [])
        if dialogues:
            ds = select_dialogue(did, dialogues)
            if ds:
                self.active_dialogue = DialogueUI(ds)
                return
        self._show_walk_msg(npc.get("description", f"{npc['name']} has nothing to say."), npc.get("color", CREAM))

    def _enter_guild(self, bld):
        """Enter a guild building.
        - If any party member has a pending ability branch choice, route directly to training.
        - Otherwise show the guild hub menu.
        """
        bld_name = bld.get("name", "Guild")
        self._show_walk_msg(f"Entered {bld_name}.", CREAM)
        self._guild_building_name = bld_name
        self._guild_hover = -1

        # Check for pending branch choices across the whole party
        from core.abilities import has_branch_choice_pending
        for c in self.party:
            pending = has_branch_choice_pending(c)
            if pending:
                self.branch_pending_char = c
                self.branch_pending_opts = pending
                self.branch_hover_idx = -1
                self._guild_branch_origin = True   # so Back returns to guild, not inn
                self.view = self.VIEW_BRANCH_CHOICE
                return

        self.view = self.VIEW_GUILD

    def _draw_guild(self, surface, mx, my):
        """Draw the Guild hub menu."""
        from core.abilities import has_branch_choice_pending
        surface.fill(TOWN_BG)

        W, H = SCREEN_W, SCREEN_H
        name = getattr(self, "_guild_building_name", "Adventurers' Guild")

        # ── Header ──────────────────────────────────────────────────
        header = pygame.Rect(0, 0, W, 72)
        pygame.draw.rect(surface, (18, 14, 32), header)
        pygame.draw.line(surface, (60, 50, 90), (0, 72), (W, 72), 1)
        draw_text(surface, name.upper(), 28, 18, GOLD, 26, bold=True)
        draw_text(surface, "\"We take the jobs no one else will touch.\"",
                  28, 50, (100, 90, 130), 13)

        # Back button
        back = pygame.Rect(W - 140, 18, 120, 36)
        draw_button(surface, back, "← Leave", hover=back.collidepoint(mx, my), size=13)
        self._guild_back_btn = back

        # ── Pending badge ───────────────────────────────────────────
        pending_chars = [c for c in self.party if has_branch_choice_pending(c)]

        # ── Menu options ────────────────────────────────────────────
        options = [
            {
                "label":   "Take a Job",
                "sub":     "Browse bounties, fetch quests, and exploration contracts",
                "accent":  (80, 200, 120),
                "action":  "jobboard",
            },
            {
                "label":   "Train Abilities" + (" ⚡" if pending_chars else ""),
                "sub":     (f"{', '.join(c.name for c in pending_chars)} "
                            f"{'have' if len(pending_chars) > 1 else 'has'} a new path to choose!"
                            if pending_chars
                            else "View your class progression and ability paths"),
                "accent":  (160, 120, 220) if pending_chars else (120, 100, 180),
                "action":  "train",
                "badge":   len(pending_chars),
            },
            {
                "label":   "View Abilities",
                "sub":     "See your full class progression tree",
                "accent":  (100, 160, 220),
                "action":  "classtree",
            },
        ]

        CARD_W = W - 80
        CARD_H = 88
        START_Y = 110
        GAP = 16
        self._guild_option_rects = []

        for i, opt in enumerate(options):
            r = pygame.Rect(40, START_Y + i * (CARD_H + GAP), CARD_W, CARD_H)
            hover = (getattr(self, "_guild_hover", -1) == i) or r.collidepoint(mx, my)
            if r.collidepoint(mx, my):
                self._guild_hover = i

            accent = opt["accent"]
            bg = tuple(min(255, c + 12) for c in SHOP_BG) if hover else SHOP_BG
            bd = accent if hover else PANEL_BORDER
            pygame.draw.rect(surface, bg, r, border_radius=6)
            pygame.draw.rect(surface, bd, r, 2 if hover else 1, border_radius=6)

            # Accent strip on left
            strip = pygame.Rect(r.x, r.y + 8, 4, r.height - 16)
            pygame.draw.rect(surface, accent, strip, border_radius=2)

            # Label
            draw_text(surface, opt["label"], r.x + 24, r.y + 16,
                      accent if hover else CREAM, 20, bold=True)

            # Subtitle
            draw_text(surface, opt["sub"], r.x + 24, r.y + 50,
                      (160, 150, 170), 13, max_width=CARD_W - 100)

            # Badge for pending choices
            if opt.get("badge"):
                badge_r = pygame.Rect(r.right - 56, r.y + r.height // 2 - 14, 44, 28)
                pygame.draw.rect(surface, (120, 60, 200), badge_r, border_radius=14)
                draw_text(surface, str(opt["badge"]), badge_r.x + 14, badge_r.y + 6,
                          (255, 255, 255), 14, bold=True)

            self._guild_option_rects.append((r, opt["action"]))

        # ── Party bar ───────────────────────────────────────────────
        self._draw_party_bar(surface, mx, my)

    def _return_to_town(self):
        """Return to the main town view — walkable if the town has a map, hub menu otherwise."""
        from data.town_maps import get_town_data
        if get_town_data(self.town_id):
            self.view = self.VIEW_WALK
        else:
            self.view = self.VIEW_HUB

    # ─────────────────────────────────────────────────────────
    #  GENERAL STORE — Menu
    # ─────────────────────────────────────────────────────────

    def _draw_shop_menu(self, surface, mx, my):
        bld_name = self.current_bld_name or self.shop.get("name", "General Store")
        self._draw_bld_npc_header(surface, bld_name, self.shop.get("welcome", ""), mx, my)

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
            draw_text(surface, desc, btn.x + 20, btn.y + 42, GREY, 15)

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
                draw_text(surface, desc, row.x + 10, row.y + 24, GREY, 15)

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
                    draw_text(surface, "  ".join(parts), row.x + 10, row.y + 44, GREY, 13)

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
                draw_text(surface, "^ scroll up", panel.x + panel.width // 2 - 40, panel.y + 2, DIM_GOLD, 13)
            if end < len(items):
                draw_text(surface, "v scroll down", panel.x + panel.width // 2 - 45, iy + 2, DIM_GOLD, 13)

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
                draw_text(surface, "^ scroll up", panel.x + panel.width // 2 - 40, panel.y + 2, DIM_GOLD, 13)
            if end < len(char.inventory):
                draw_text(surface, "v scroll down", panel.x + panel.width // 2 - 45, iy + 2, DIM_GOLD, 13)

        self._draw_party_bar(surface, mx, my)

    # ─────────────────────────────────────────────────────────
    #  TEMPLE
    # ─────────────────────────────────────────────────────────

    def _draw_temple(self, surface, mx, my):
        bld_name = self.current_bld_name or "Temple of Light"
        self._draw_bld_npc_header(surface, bld_name, TEMPLE.get("welcome", ""), mx, my)

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
        bld_name = self.current_bld_name or "The Inn"
        self._draw_bld_npc_header(surface, bld_name, "Rest your bones, train your skills, save your progress.", mx, my)

        back = pygame.Rect(SCREEN_W - 140, 20, 120, 34)
        draw_button(surface, back, "Back", hover=back.collidepoint(mx, my), size=13)

        # Save button — top right, next to Back
        save_btn = pygame.Rect(SCREEN_W - 280, 20, 128, 34)
        draw_button(surface, save_btn, "💾 Save Game", hover=save_btn.collidepoint(mx, my), size=13)
        # Save feedback label
        if getattr(self, "_inn_save_msg", "") and getattr(self, "_inn_save_timer", 0) > 0:
            smsg_col = (120, 220, 120) if self._inn_save_ok else (220, 80, 80)
            draw_text(surface, self._inn_save_msg, SCREEN_W - 420, 60, smsg_col, 12)

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
        """
        Level-up screen: left panel = stat picker, right panel = full ability tree.
        Shows locked/unlocked/new abilities for the character's class.
        """
        from core.progression import training_cost
        from core.classes import STAT_NAMES
        from core.abilities import CLASS_ABILITIES, get_new_abilities_at_level

        if not self.levelup_queue:
            self.view = self.VIEW_INN
            return

        c    = self.levelup_queue[self.levelup_current]
        cost = training_cost(c.level + 1)
        cls  = CLASSES.get(c.class_name, {})
        col  = cls.get("color", CREAM)
        next_lvl = c.level + 1

        # Header
        draw_class_badge(surface, c.class_name, 20, 14, 16)
        draw_text(surface, f"{c.name}  —  Level {c.level} → {next_lvl}", 58, 18, col, 22, bold=True)
        draw_text(surface, f"Training cost: {cost}g", 58, 48, DIM_GOLD, 14)
        party_gold = sum(cc.gold for cc in self.party)
        gold_col = GREEN if party_gold >= cost else RED
        draw_text(surface, f"Party gold: {party_gold}g", 260, 48, gold_col, 14)

        # Left panel: stat picker
        left_panel = pygame.Rect(20, 80, 310, 420)
        draw_panel(surface, left_panel)
        draw_text(surface, "Assign 1 free stat point:", left_panel.x + 14, left_panel.y + 10, GOLD, 15, bold=True)

        growth = cls.get("stat_growth", {})
        for i, stat in enumerate(STAT_NAMES):
            btn     = pygame.Rect(left_panel.x + 10, left_panel.y + 38 + i * 60, left_panel.width - 20, 52)
            selected= self.levelup_free_stat == stat
            hover   = btn.collidepoint(mx, my)
            tier    = growth.get(stat, "low")
            tier_col= {"high":(180,220,120),"medium":(180,180,100),"low":(120,120,100)}.get(tier, GREY)
            bg      = (55, 45, 25) if selected else (38, 32, 20) if hover else (22, 18, 12)
            border  = GOLD if selected else tier_col if hover else (50, 45, 35)
            pygame.draw.rect(surface, bg,     btn, border_radius=4)
            pygame.draw.rect(surface, border, btn, 2 if selected else 1, border_radius=4)
            val = c.stats[stat]
            draw_text(surface, f"{stat}", btn.x + 10, btn.y + 4, tier_col, 18, bold=True)
            draw_text(surface, f"{val} → {val+1}", btn.x + 56, btn.y + 6, CREAM, 16)
            draw_text(surface, tier.upper(), btn.x + 10, btn.y + 30, tier_col, 10)
            if selected:
                pygame.draw.polygon(surface, GOLD,
                    [(btn.right-22, btn.y+18),(btn.right-10, btn.y+8),(btn.right-10, btn.y+28)])

        # Right panel: ability tree
        right_panel = pygame.Rect(340, 80, SCREEN_W - 360, 490)
        draw_panel(surface, right_panel, border_color=col)
        draw_text(surface, f"{c.class_name} Abilities", right_panel.x + 14, right_panel.y + 10, col, 15, bold=True)

        all_abs  = CLASS_ABILITIES.get(c.class_name, [])
        known    = {a["name"] for a in c.abilities}
        new_at   = {a["name"] for a in get_new_abilities_at_level(c.class_name, next_lvl)}

        row_h  = 68
        ab_x   = right_panel.x + 12
        ab_y   = right_panel.y + 38
        vis    = (right_panel.height - 48) // row_h

        for i, ab in enumerate(all_abs[:vis]):
            ry       = ab_y + i * row_h
            is_known = ab["name"] in known
            is_new   = ab["name"] in new_at
            is_next  = not is_known and not is_new and ab["level"] == next_lvl + 1
            locked   = ab["level"] > next_lvl and not is_known

            if is_new:
                bg_col, bd_col = (30,60,20), GREEN
            elif is_known:
                bg_col, bd_col = (20,30,50), (60,100,160)
            elif is_next:
                bg_col, bd_col = (35,28,15), (100,90,50)
            else:
                bg_col, bd_col = (18,14,10), (40,35,30)

            row_rect = pygame.Rect(ab_x, ry, right_panel.width - 24, row_h - 4)
            pygame.draw.rect(surface, bg_col, row_rect, border_radius=4)
            pygame.draw.rect(surface, bd_col, row_rect, 1, border_radius=4)

            lv_col = GREEN if is_new else (100,150,220) if is_known else (100,90,60) if is_next else (60,50,40)
            pygame.draw.rect(surface, (20,20,20), pygame.Rect(ab_x+4, ry+4, 36, 20), border_radius=3)
            draw_text(surface, f"Lv{ab['level']}", ab_x+5, ry+5, lv_col, 11, bold=True)

            if is_new:      tag, tag_col = "NEW!", GREEN
            elif is_known:  tag, tag_col = "Known", (100,150,220)
            elif locked:    tag, tag_col = f"Lv{ab['level']} req", (80,70,50)
            else:           tag, tag_col = "Next!", (180,160,80)
            draw_text(surface, tag, ab_x+46, ry+5, tag_col, 11)

            name_col = GOLD if is_new else (160,200,255) if is_known else (120,110,80) if not locked else (80,70,60)
            draw_text(surface, ab["name"], ab_x+46, ry+20, name_col, 14, bold=True)
            res_txt = f"{ab['cost']} {ab['resource']}" if ab.get("resource") else ""
            if res_txt:
                draw_text(surface, res_txt, ab_x + right_panel.width - 130, ry+22, (120,110,90), 11)
            desc_col = (160,160,140) if is_known or is_new else (80,75,60)
            draw_text(surface, ab.get("desc",""), ab_x+46, ry+40, desc_col, 11,
                      max_width=right_panel.width - 80)

        if len(all_abs) > vis:
            draw_text(surface, f"+ {len(all_abs)-vis} more at higher levels",
                      right_panel.x+14, right_panel.bottom-22, (80,80,60), 11)

        # Bottom buttons
        can_train = self.levelup_free_stat is not None and party_gold >= cost
        confirm = pygame.Rect(20, 516, 200, 46)
        draw_button(surface, confirm, "Train!", hover=confirm.collidepoint(mx, my) and can_train, size=16)
        if self.levelup_free_stat and not can_train:
            draw_text(surface, "Not enough gold!", confirm.x, confirm.y+50, RED, 12)
        elif not self.levelup_free_stat:
            draw_text(surface, "Pick a stat first", confirm.x+4, confirm.y+50, (100,90,60), 12)

        skip = pygame.Rect(240, 516, 130, 46)
        draw_button(surface, skip, "Skip", hover=skip.collidepoint(mx, my), size=14)

        tree_btn = pygame.Rect(390, 516, 200, 46)
        draw_button(surface, tree_btn, "Full Tree", hover=tree_btn.collidepoint(mx, my), size=13)

    def _draw_branch_choice(self, surface, mx, my):
        """
        Branch ability choice screen.
        Player selects ONE of two abilities, permanently locking the other path.
        Full-width dramatic presentation with flavour text.
        """
        c    = self.branch_pending_char
        opts = self.branch_pending_opts
        if not c or not opts:
            if getattr(self, "_guild_branch_origin", False):
                self._guild_branch_origin = False
                self.view = self.VIEW_GUILD
            else:
                self.view = self.VIEW_INN_LEVELUP_RESULT
            return

        cls     = CLASSES.get(c.class_name, {})
        col     = cls.get("color", CREAM)

        # Background atmosphere
        bg = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        bg.fill((10, 8, 20, 200))
        surface.blit(bg, (0, 0))

        # Header
        draw_class_badge(surface, c.class_name, 24, 20, 18)
        draw_text(surface, f"{c.name}  —  Level {c.level} Path Choice",
                  70, 24, col, 22, bold=True)
        draw_text(surface, "Your experience has opened a new path. Choose wisely — the other road closes forever.",
                  70, 56, (160, 140, 180), 14, max_width=SCREEN_W - 100)

        # "Choose your path" divider
        mid_x = SCREEN_W // 2
        pygame.draw.line(surface, (60, 50, 80), (mid_x, 90), (mid_x, SCREEN_H - 100), 1)
        draw_text(surface, "— OR —", mid_x - 28, SCREEN_H // 2 - 12, (120, 100, 160), 14)

        CARD_W = SCREEN_W // 2 - 40
        CARD_TOP = 90
        CARD_H   = SCREEN_H - 200

        for idx, opt in enumerate(opts):
            cx = 20 + idx * (SCREEN_W // 2)
            card = pygame.Rect(cx, CARD_TOP, CARD_W, CARD_H)
            hover = card.collidepoint(mx, my)
            if hover:
                self.branch_hover_idx = idx

            bg_col = (35, 55, 25) if (hover and idx == 0) else \
                     (25, 40, 65) if (hover and idx == 1) else \
                     (22, 18, 35)
            bd_col = col if hover else (60, 50, 90)
            pygame.draw.rect(surface, bg_col, card, border_radius=8)
            pygame.draw.rect(surface, bd_col, card, 2 if hover else 1, border_radius=8)

            # Branch label (big path identifier)
            label   = opt.get("branch_label", opt["name"])
            lbl_col = (200, 240, 140) if idx == 0 else (140, 180, 255)
            draw_text(surface, label.upper(), cx + 20, CARD_TOP + 18,
                      lbl_col, 20, bold=True)

            # Branch descriptor tagline
            tag = opt.get("branch_desc", "")
            draw_text(surface, tag, cx + 20, CARD_TOP + 48,
                      (160, 155, 170), 13, max_width=CARD_W - 40)

            # Divider line under tagline
            pygame.draw.line(surface, (50, 45, 70),
                             (cx + 20, CARD_TOP + 68), (cx + CARD_W - 20, CARD_TOP + 68))

            # Ability name
            draw_text(surface, opt["name"], cx + 20, CARD_TOP + 82,
                      col if hover else CREAM, 18, bold=True)

            # Cost / resource
            if opt.get("resource"):
                cost_str = f"{opt['cost']} {opt['resource']}"
                draw_text(surface, cost_str, cx + CARD_W - 120, CARD_TOP + 84,
                          DIM_GOLD, 13)

            # Description — wrapped generously
            draw_text(surface, opt.get("desc", ""), cx + 20, CARD_TOP + 114,
                      (190, 185, 160) if hover else (130, 125, 110), 13,
                      max_width=CARD_W - 40)

            # Type badge
            type_colors = {"attack": (200, 80, 80), "spell": (80, 120, 220),
                           "heal": (80, 200, 120), "buff": (200, 180, 60),
                           "debuff": (180, 80, 180), "aoe": (220, 120, 60)}
            type_col = type_colors.get(opt.get("type", ""), GREY)
            type_str = opt.get("type", "ability").upper()
            tr = pygame.Rect(cx + 20, CARD_TOP + CARD_H - 100, 80, 22)
            pygame.draw.rect(surface, (25, 20, 35), tr, border_radius=3)
            pygame.draw.rect(surface, type_col, tr, 1, border_radius=3)
            draw_text(surface, type_str, tr.x + 6, tr.y + 4, type_col, 11)

            # Element badge if applicable
            if opt.get("element"):
                elem_colors = {"fire": (220, 100, 40), "ice": (100, 180, 240),
                               "lightning": (240, 220, 60), "divine": (240, 220, 120),
                               "nature": (80, 180, 80), "arcane": (160, 100, 220)}
                ec = elem_colors.get(opt["element"], GREY)
                er = pygame.Rect(cx + 110, CARD_TOP + CARD_H - 100, 80, 22)
                pygame.draw.rect(surface, (25, 20, 35), er, border_radius=3)
                pygame.draw.rect(surface, ec, er, 1, border_radius=3)
                draw_text(surface, opt["element"].upper(), er.x + 6, er.y + 4, ec, 11)

            # Select button
            btn = pygame.Rect(cx + 20, CARD_TOP + CARD_H - 62, CARD_W - 40, 48)
            btn_hover = btn.collidepoint(mx, my)
            btn_col   = (lbl_col[0]//2, lbl_col[1]//2, lbl_col[2]//2)
            btn_bord  = lbl_col
            pygame.draw.rect(surface, btn_col, btn, border_radius=6)
            pygame.draw.rect(surface, btn_bord, btn, 2, border_radius=6)
            draw_text(surface, f"Choose {label}", btn.x + 20, btn.y + 14,
                      lbl_col, 15, bold=True)

    def _draw_levelup_result(self, surface, mx, my):
        """Fanfare screen after confirming level-up."""
        s = self.levelup_summary
        if not s:
            self.view = self.VIEW_INN
            return

        cls   = CLASSES.get(s.get("class_name",""), {})
        col   = cls.get("color", CREAM)

        # Glow
        glow = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        for r in range(260, 0, -4):
            a  = int(55 * (260-r)/260)
            rc, gc, bc = col
            pygame.draw.circle(glow, (rc//3, gc//3, bc//3, a), (SCREEN_W//2, SCREEN_H//2-60), r)
        surface.blit(glow, (0, 0))

        draw_class_badge(surface, s.get("class_name",""), SCREEN_W//2-220, 60, 22)
        draw_text(surface, "LEVEL UP!", SCREEN_W//2-100, 55, GOLD, 36, bold=True)
        draw_text(surface, f"{s.get('char_name','')}  is now Level {s.get('level','')}  {s.get('class_name','')}",
                  SCREEN_W//2-220, 105, col, 20)

        # Stat gains
        panel = pygame.Rect(SCREEN_W//2-320, 145, 300, 220)
        draw_panel(surface, panel, border_color=col)
        draw_text(surface, "Gains:", panel.x+14, panel.y+10, GOLD, 15, bold=True)
        gy = panel.y+40
        for stat, val in s.get("stat_gains",{}).items():
            draw_text(surface, f"+{val} {stat}", panel.x+20, gy, GREEN, 18); gy += 28
        if s.get("hp_gain"):
            draw_text(surface, f"+{s['hp_gain']} Max HP", panel.x+20, gy, (160,220,160), 16)

        # New ability panel
        ab_panel = pygame.Rect(SCREEN_W//2+20, 145, 340, 220)
        if s.get("new_abilities"):
            from core.abilities import CLASS_ABILITIES
            all_abs  = CLASS_ABILITIES.get(s.get("class_name",""), [])
            new_name = s["new_abilities"][0]
            ab_data  = next((a for a in all_abs if a["name"] == new_name), None)
            draw_panel(surface, ab_panel, border_color=GREEN)
            draw_text(surface, "New Ability!", ab_panel.x+14, ab_panel.y+10, GREEN, 14, bold=True)
            if ab_data:
                draw_text(surface, ab_data["name"], ab_panel.x+14, ab_panel.y+38, GOLD, 20, bold=True)
                draw_text(surface, f"{ab_data['cost']} {ab_data.get('resource','')}",
                          ab_panel.x+14, ab_panel.y+68, DIM_GOLD, 13)
                draw_wrapped_text(surface, ab_data.get("desc",""),
                                  ab_panel.x+14, ab_panel.y+92,
                                  ab_panel.width-28, (210,210,190), get_font(13))
            if len(s["new_abilities"]) > 1:
                draw_text(surface, f"+ {len(s['new_abilities'])-1} more learned!",
                          ab_panel.x+14, ab_panel.bottom-22, GREEN, 11)
        else:
            draw_panel(surface, ab_panel, border_color=(60,50,40))
            draw_text(surface, "No new abilities this level.", ab_panel.x+14, ab_panel.y+80, (100,90,70), 14)
            from core.abilities import CLASS_ABILITIES
            all_abs = CLASS_ABILITIES.get(s.get("class_name",""), [])
            nxt = next((a for a in all_abs if a["level"] > s.get("level",1)), None)
            if nxt:
                draw_text(surface, "Coming next:", ab_panel.x+14, ab_panel.y+120, DIM_GOLD, 13)
                draw_text(surface, f"{nxt['name']}  (Level {nxt['level']})",
                          ab_panel.x+14, ab_panel.y+142, (160,150,100), 15)
                draw_text(surface, nxt.get("desc",""), ab_panel.x+14, ab_panel.y+168,
                          (100,95,80), 12, max_width=ab_panel.width-28)

        # Branch choice result (if applicable)
        if s.get("branch_chosen"):
            branch_panel = pygame.Rect(SCREEN_W//2 - 320, 380, 660, 100)
            draw_panel(surface, branch_panel, border_color=(160, 120, 220))
            draw_text(surface, "PATH CHOSEN:", branch_panel.x + 14, branch_panel.y + 10,
                      (160, 120, 220), 13, bold=True)
            draw_text(surface, s["branch_label"].upper(), branch_panel.x + 14,
                      branch_panel.y + 34, (200, 170, 255), 20, bold=True)
            draw_text(surface, s["branch_chosen"], branch_panel.x + 200, branch_panel.y + 38,
                      GOLD, 16)
            draw_text(surface, "The other path is now closed to you.",
                      branch_panel.x + 14, branch_panel.y + 70, (100, 90, 120), 12)

        # Continue button
        cont = pygame.Rect(SCREEN_W//2-100, SCREEN_H-90, 200, 50)
        draw_button(surface, cont, "Continue", hover=cont.collidepoint(mx, my), size=16)
        self._lvlresult_cont = cont

    def _draw_classtree(self, surface, mx, my):
        """Full class progression viewer: timeline of abilities with locked/known state."""
        from core.abilities import CLASS_ABILITIES
        from core.progression import CLASS_TRANSITIONS, get_available_transitions
        from collections import defaultdict

        if not self.party:
            self.view = self.VIEW_INN
            return

        self.classtree_char_idx = max(0, min(self.classtree_char_idx, len(self.party)-1))
        c   = self.party[self.classtree_char_idx]
        cls = CLASSES.get(c.class_name, {})
        col = cls.get("color", CREAM)
        known = {a["name"] for a in c.abilities}

        # Header + tabs
        draw_text(surface, "Class Progression", 20, 12, GOLD, 22, bold=True)
        self._classtree_tab_rects = []
        self._classtree_back = pygame.Rect(SCREEN_W-130, 12, 110, 34)
        draw_button(surface, self._classtree_back, "Back",
                    hover=self._classtree_back.collidepoint(mx, my), size=13)

        tab_x = 20
        for i, ch in enumerate(self.party):
            tc = CLASSES.get(ch.class_name, {}).get("color", CREAM)
            tw = max(110, get_font(13).size(ch.name)[0]+36)
            tr = pygame.Rect(tab_x, 48, tw, 30)
            self._classtree_tab_rects.append(tr)
            sel = (i == self.classtree_char_idx)
            pygame.draw.rect(surface, (40,35,25) if sel else (20,18,14), tr, border_radius=4)
            pygame.draw.rect(surface, tc if sel else (50,45,35), tr, 2, border_radius=4)
            draw_class_badge(surface, ch.class_name, tr.x+4, tr.y+3, 11)
            draw_text(surface, ch.name, tr.x+30, tr.y+7, tc if sel else GREY, 13)
            tab_x += tw + 6

        # Class info
        draw_class_badge(surface, c.class_name, 20, 90, 18)
        draw_text(surface, f"{c.class_name}  Level {c.level}", 62, 93, col, 18, bold=True)
        draw_text(surface, cls.get("description",""), 62, 118, GREY, 12)

        # Timeline
        all_abs = CLASS_ABILITIES.get(c.class_name, [])
        by_level = defaultdict(list)
        for ab in all_abs:
            by_level[ab["level"]].append(ab)
        levels = sorted(by_level.keys())

        if not levels:
            draw_text(surface, "No ability data.", 60, 200, GREY, 14)
        else:
            TL_X = 60; TL_Y = 150; TL_W = SCREEN_W-100; TL_H = SCREEN_H-TL_Y-80
            COL_W = max(160, TL_W // max(1, len(levels)))
            pygame.draw.line(surface, (60,55,40), (TL_X, TL_Y+22), (TL_X+TL_W, TL_Y+22), 2)

            for ci, lv in enumerate(levels):
                cx = TL_X + ci*COL_W + COL_W//2
                reached = c.level >= lv
                dot_col = col if reached else (55,50,38)
                pygame.draw.circle(surface, dot_col, (cx, TL_Y+22), 7 if reached else 4)
                if reached:
                    pygame.draw.circle(surface, GOLD, (cx, TL_Y+22), 3)
                draw_text(surface, f"Lv{lv}", cx-18, TL_Y+4, col if reached else (70,62,48), 11, bold=reached)

                ay = TL_Y + 40
                for ab in by_level[lv]:
                    is_known = ab["name"] in known
                    is_next  = lv == c.level + 1
                    if is_known:   ab_bg, ab_bd, nc = (18,32,55), (55,100,190), (140,190,255)
                    elif is_next:  ab_bg, ab_bd, nc = (38,30,12), (170,140,55), (210,180,90)
                    else:          ab_bg, ab_bd, nc = (16,13,10), (38,33,26),   (70,63,50)

                    ar = pygame.Rect(cx-COL_W//2+4, ay, COL_W-8, 74)
                    if ay + ar.height > TL_Y + TL_H: break
                    pygame.draw.rect(surface, ab_bg, ar, border_radius=4)
                    pygame.draw.rect(surface, ab_bd, ar, 1, border_radius=4)
                    tick = "✓" if is_known else ">" if is_next else "·"
                    draw_text(surface, tick, ar.x+4, ar.y+4, ab_bd, 12)
                    draw_text(surface, ab["name"], ar.x+16, ar.y+4, nc, 12, bold=True)
                    draw_text(surface, f"{ab['cost']} {ab.get('resource','')}", ar.x+16, ar.y+20, (90,82,62), 10)
                    draw_wrapped_text(surface, ab.get("desc",""), ar.x+6, ar.y+36,
                                      ar.width-12, (100,93,75) if not is_known else (120,125,150), get_font(10))
                    ay += ar.height + 4

        # Transitions bar
        ty = SCREEN_H - 68
        draw_text(surface, "Transitions:", 20, ty, DIM_GOLD, 12)
        tx = 130
        for tn, req in CLASS_TRANSITIONS.items():
            if c.class_name not in req["base_classes"]: continue
            can = tn in get_available_transitions(c)
            tc2 = PURPLE if can else (60,50,50)
            bg2 = (35,16,50) if can else (20,16,16)
            tr2 = pygame.Rect(tx, ty-3, get_font(12).size(tn)[0]+20, 24)
            pygame.draw.rect(surface, bg2, tr2, border_radius=3)
            pygame.draw.rect(surface, tc2, tr2, 1, border_radius=3)
            draw_text(surface, tn, tr2.x+8, tr2.y+4, tc2, 11)
            draw_text(surface, f"Lv{req['min_level']}", tr2.x+4, tr2.y-13, (72,66,50), 10)
            tx += tr2.width + 6


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
        from data.shop_inventory import TAVERN
        from core.story_flags import get_flag

        W, H = SCREEN_W, SCREEN_H
        draw_text(surface, TAVERN["name"], W//2 - 130, 28, GOLD, 22, bold=True)

        # ── Tab bar ───────────────────────────────────────────────────────────
        tabs = [("patrons", "Patrons"), ("recruit", "Adventurers"), ("party", "My Party")]
        tx = 30
        self._tavern_tab_rects = []
        for key, label in tabs:
            tw2 = get_font(13).size(label)[0] + 24
            tr = pygame.Rect(tx, 62, tw2, 28)
            active = (self.tavern_tab == key)
            bg = (50, 40, 20) if active else (25, 18, 10)
            border = GOLD if active else PANEL_BORDER
            pygame.draw.rect(surface, bg, tr, border_radius=4)
            pygame.draw.rect(surface, border, tr, 1, border_radius=4)
            draw_text(surface, label, tr.x + 12, tr.y + 6,
                      GOLD if active else GREY, 13)
            self._tavern_tab_rects.append((key, tr))
            tx += tw2 + 8

        back = pygame.Rect(W - 140, 28, 120, 34)
        draw_button(surface, back, "Leave", hover=back.collidepoint(mx, my), size=13)

        # ── PATRONS tab ───────────────────────────────────────────────────────
        if self.tavern_tab == "patrons":
            patrons = [p for p in TAVERN["patrons"]
                       if not (p.get("hide_if") and get_flag(p["hide_if"]))]
            drink_cost = TAVERN.get("drink_cost", 2)

            # Left panel — patron list
            list_panel = pygame.Rect(20, 100, 280, H - 200)
            draw_panel(surface, list_panel, bg_color=(18, 12, 8))
            draw_text(surface, "At the bar:", list_panel.x + 10, list_panel.y + 8, DIM_GOLD, 11)

            self._patron_rects = []
            for i, p in enumerate(patrons):
                py2 = list_panel.y + 28 + i * 54
                row = pygame.Rect(list_panel.x + 6, py2, list_panel.width - 12, 48)
                sel = (self.tavern_selected == i)
                bg2 = (40, 30, 12) if sel else (25, 18, 8)
                pygame.draw.rect(surface, bg2, row, border_radius=3)
                if sel:
                    pygame.draw.rect(surface, GOLD, row, 1, border_radius=3)

                # NPC color dot
                pygame.draw.circle(surface, p["color"],
                                   (row.x + 16, row.y + 18), 10)
                pygame.draw.circle(surface, tuple(max(0,c-40) for c in p["color"]),
                                   (row.x + 16, row.y + 18), 10, 1)

                drinks = self.tavern_drinks.get(p["name"], 0)
                name_col = p["color"] if drinks > 0 else CREAM
                draw_text(surface, p["name"], row.x + 32, row.y + 6, name_col, 12, bold=True)
                tier_txt = f"{'🍺'*min(drinks,3)} loosened up" if drinks > 0 else "Sober"
                draw_text(surface, tier_txt, row.x + 32, row.y + 24, DIM_GOLD if drinks else GREY, 10)
                self._patron_rects.append((i, row))

            # Right panel — dialogue
            dlg_panel = pygame.Rect(316, 100, W - 336, H - 200)
            draw_panel(surface, dlg_panel, bg_color=(20, 14, 8))

            if 0 <= self.tavern_selected < len(patrons):
                p = patrons[self.tavern_selected]
                drinks = self.tavern_drinks.get(p["name"], 0)
                nc = p["color"]

                # Portrait circle
                pygame.draw.circle(surface, nc,
                                   (dlg_panel.x + 36, dlg_panel.y + 40), 26)
                pygame.draw.circle(surface, tuple(max(0,c-50) for c in nc),
                                   (dlg_panel.x + 36, dlg_panel.y + 40), 26, 2)
                draw_text(surface, p["name"], dlg_panel.x + 72, dlg_panel.y + 18,
                          nc, 16, bold=True)
                draw_text(surface, p.get("role","patron").capitalize(),
                          dlg_panel.x + 72, dlg_panel.y + 38, GREY, 11)

                # Quote
                lines2 = p["drunk"] if drinks > 0 else p["sober"]
                import random
                rng_key = (p["name"], drinks)
                q_idx = hash(rng_key) % len(lines2)
                quote = lines2[q_idx]
                draw_text(surface, f'"{quote}"',
                          dlg_panel.x + 16, dlg_panel.y + 80, CREAM, 13,
                          max_width=dlg_panel.width - 32)

                # Buy drink button
                total_gold = sum(c.gold for c in self.party)
                can_afford = total_gold >= drink_cost
                btn_label = f"Buy a drink ({drink_cost}g)"
                btn_col = CREAM if can_afford else GREY
                drink_btn = pygame.Rect(dlg_panel.x + 16, H - 190, 220, 38)
                draw_button(surface, drink_btn, btn_label,
                            hover=drink_btn.collidepoint(mx, my) and can_afford,
                            size=13)
                self._tavern_drink_btn = drink_btn
                self._tavern_drink_patron = p["name"]

                if drinks == 0:
                    draw_text(surface, "Buy them a drink to loosen their tongue.",
                              dlg_panel.x + 16, H - 142, DIM_GOLD, 11)
                else:
                    draw_text(surface, "Another drink might reveal more...",
                              dlg_panel.x + 16, H - 142, DIM_GOLD, 11)
            else:
                self._tavern_drink_btn = None

        # ── ADVENTURERS tab ───────────────────────────────────────────────────
        elif self.tavern_tab == "recruit":
            recruits = TAVERN.get("recruits", [])
            draw_text(surface, "Adventurers seeking work:", 30, 105, DIM_GOLD, 13)

            self._recruit_rects = []
            col_x = [30, W//2 + 10]
            for i, rec in enumerate(recruits):
                cx2 = col_x[i % 2]
                ry = 130 + (i // 2) * 180
                panel = pygame.Rect(cx2, ry, W//2 - 50, 165)
                sel = (self.tavern_recruit_sel == i)
                bg3 = (35, 28, 12) if sel else (22, 16, 8)
                draw_panel(surface, panel, bg_color=bg3)
                if sel:
                    pygame.draw.rect(surface, GOLD, panel, 1, border_radius=4)

                rc = rec["color"]
                pygame.draw.circle(surface, rc, (panel.x + 22, panel.y + 22), 16)
                draw_text(surface, rec["name"], panel.x + 44, panel.y + 8, rc, 15, bold=True)
                draw_text(surface, f"{rec['race_name']} {rec['class_name']} — Lv.{rec['level']}",
                          panel.x + 44, panel.y + 28, GREY, 11)
                draw_text(surface, f'"{rec["pitch"]}"',
                          panel.x + 12, panel.y + 52, CREAM, 11,
                          max_width=panel.width - 24)

                # Stats
                stat_y = panel.y + 88
                for si, (sn, sv) in enumerate(rec["stats"].items()):
                    sx2 = panel.x + 12 + si * 54
                    draw_text(surface, sn, sx2, stat_y, GREY, 9)
                    draw_text(surface, str(sv), sx2, stat_y + 12, CREAM, 11, bold=True)

                # Recruit button
                party_full = len(self.party) >= 6
                already_in = any(c.name == rec["name"] for c in self.party)
                if already_in:
                    draw_text(surface, "In party", panel.x + 12, panel.y + 138, DIM_GOLD, 11)
                elif party_full:
                    draw_text(surface, "Party full (6 max)", panel.x + 12, panel.y + 138, GREY, 11)
                else:
                    rbtn = pygame.Rect(panel.x + 12, panel.y + 132, 130, 26)
                    draw_button(surface, rbtn, "Recruit", hover=rbtn.collidepoint(mx, my), size=11)
                    self._recruit_rects.append((i, rbtn, rec))

        # ── MY PARTY tab ──────────────────────────────────────────────────────
        elif self.tavern_tab == "party":
            draw_text(surface, "Leave a party member here (they wait safely):",
                      30, 108, DIM_GOLD, 13)
            draw_text(surface, "You must keep at least 1 member.",
                      30, 126, GREY, 11)

            self._leave_rects = []
            for i, char in enumerate(self.party):
                px3 = 30 + (i % 3) * (W // 3 - 10)
                py3 = 150 + (i // 3) * 160
                panel = pygame.Rect(px3, py3, W//3 - 20, 145)
                draw_panel(surface, panel, bg_color=(22, 16, 8))

                cc = getattr(char, "_walk_color", (180, 160, 120))
                pygame.draw.circle(surface, cc, (panel.x + 22, panel.y + 22), 14)
                draw_text(surface, char.name, panel.x + 42, panel.y + 8, CREAM, 14, bold=True)
                draw_text(surface, f"Lv.{char.level} {getattr(char,'class_name','?')}",
                          panel.x + 42, panel.y + 26, GREY, 11)
                draw_text(surface, f"HP: {char.resources.get('HP',0)}/{char.resources.get('MAX_HP',0)}",
                          panel.x + 12, panel.y + 50, CREAM, 11)
                draw_text(surface, f"Gold: {char.gold}g",
                          panel.x + 12, panel.y + 66, DIM_GOLD, 11)

                if len(self.party) > 1:
                    lbtn = pygame.Rect(panel.x + 12, panel.y + 110, 120, 26)
                    draw_button(surface, lbtn, "Leave here",
                                hover=lbtn.collidepoint(mx, my), size=11)
                    self._leave_rects.append((i, lbtn))

        self._tavern_back_btn = back
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

        # Dialogue takes priority — handle and return immediately so other
        # click targets don't process on the same mouse event.
        if self.active_dialogue and not self.active_dialogue.finished:
            result = self.active_dialogue.handle_click(mx, my)
            if self.active_dialogue.finished:
                self.active_dialogue = None
                try:
                    from core.story_flags import auto_advance_quests
                    done = auto_advance_quests(self.party)
                    self.pending_quest_completions.extend(done)
                except Exception:
                    pass
            return None  # consume the click regardless

        # ── Indoor NPC portrait click (any service view) ──
        if (self._bld_npc_portrait_rect and
                self._bld_npc_portrait_rect.collidepoint(mx, my) and
                self.view not in (self.VIEW_WALK, self.VIEW_HUB)):
            self._open_indoor_npc_dialogue()
            return None

        # ── Hub view ──
        if self.view == self.VIEW_HUB:
            locations = ["inn", "shop", "forge", "temple", "tavern", "jobboard", "exit"]
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
                        # Refresh rumor based on current story act
                        from data.story_data import get_rumor
                        self.current_rumor = get_rumor()
                        self.view = self.VIEW_TAVERN
                    elif loc == "inn":
                        self.view = self.VIEW_INN
                    elif loc == "jobboard":
                        self.view = self.VIEW_JOBBOARD
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

            # Save button
            save_btn = pygame.Rect(SCREEN_W - 280, 20, 128, 34)
            if save_btn.collidepoint(mx, my):
                from core.save_load import save_game
                ok, path, msg = save_game(self.party)
                self._inn_save_msg = msg
                self._inn_save_ok  = ok
                self._inn_save_timer = 3000
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

            # Stat selection buttons (left panel, 60px rows starting at y=118)
            left_panel_x = 30
            for i, stat in enumerate(STAT_NAMES):
                btn = pygame.Rect(left_panel_x, 118 + i * 60, 290, 52)
                if btn.collidepoint(mx, my):
                    self.levelup_free_stat = stat
                    return None

            # Train button
            cost = training_cost(c.level + 1)
            party_gold = sum(cc.gold for cc in self.party)
            can_train = self.levelup_free_stat is not None and party_gold >= cost
            confirm = pygame.Rect(20, 516, 200, 46)
            if confirm.collidepoint(mx, my) and can_train:
                summary = apply_level_up(c, self.levelup_free_stat)
                if summary:
                    max_res = get_all_resources(c.class_name, c.stats, c.level)
                    for rn, mv in max_res.items():
                        if c.resources.get(rn, 0) > mv:
                            c.resources[rn] = mv
                    # Store for fanfare screen
                    summary["char_name"]   = c.name
                    summary["class_name"]  = c.class_name
                    summary["stats_after"] = dict(c.stats)
                    self.levelup_summary   = summary
                    gains = ", ".join(f"+{v} {k}" for k, v in summary["stat_gains"].items())
                    ab_str = (" Learned: " + ", ".join(summary["new_abilities"])
                              if summary.get("new_abilities") else "")
                    self.inn_result = (f"{c.name} reached level {c.level}! "
                                      f"{gains}, +{summary['hp_gain']} base HP{ab_str}")
                    sfx.play("level_up")

                    # If there's a branch choice pending, show that screen first
                    if summary.get("branch_choice"):
                        self.branch_pending_char = c
                        self.branch_pending_opts  = summary["branch_choice"]
                        self.branch_hover_idx     = -1
                        self.levelup_current += 1
                        self.levelup_free_stat = None
                        self.view = self.VIEW_BRANCH_CHOICE
                        return None

                self.levelup_current += 1
                self.levelup_free_stat = None
                # Go to fanfare before next character
                self.view = self.VIEW_INN_LEVELUP_RESULT
                return None

            # Skip button
            skip = pygame.Rect(240, 516, 130, 46)
            if skip.collidepoint(mx, my):
                self.levelup_current += 1
                self.levelup_free_stat = None
                if self.levelup_current >= len(self.levelup_queue):
                    self.view = self.VIEW_INN
                return None

            # Full tree button
            tree_btn = pygame.Rect(390, 516, 200, 46)
            if tree_btn.collidepoint(mx, my):
                # Find this char's index in party for the tree viewer
                idx = next((i for i, ch in enumerate(self.party)
                            if ch is c), 0)
                self.classtree_char_idx = idx
                self.view = self.VIEW_CLASSTREE
                return None

        elif self.view == self.VIEW_INN_LEVELUP_RESULT:
            # Continue button → next character or back to inn
            cont = pygame.Rect(SCREEN_W // 2 - 100, SCREEN_H - 90, 200, 50)
            if cont.collidepoint(mx, my):
                self.levelup_summary = None
                if self.levelup_current >= len(self.levelup_queue):
                    self.view = self.VIEW_INN
                else:
                    self.view = self.VIEW_INN_LEVELUP
                return None

        elif self.view == self.VIEW_BRANCH_CHOICE:
            from core.abilities import choose_branch
            c    = self.branch_pending_char
            opts = self.branch_pending_opts
            if not c or not opts:
                if getattr(self, "_guild_branch_origin", False):
                    self._guild_branch_origin = False
                    self.view = self.VIEW_GUILD
                else:
                    self.view = self.VIEW_INN_LEVELUP_RESULT
                return None

            CARD_W   = SCREEN_W // 2 - 40
            CARD_TOP = 90
            CARD_H   = SCREEN_H - 200

            for idx, opt in enumerate(opts):
                cx  = 20 + idx * (SCREEN_W // 2)
                btn = pygame.Rect(cx + 20, CARD_TOP + CARD_H - 62, CARD_W - 40, 48)
                if btn.collidepoint(mx, my):
                    choose_branch(c, opt)
                    label = opt.get("branch_label", opt["name"])
                    if self.levelup_summary:
                        self.levelup_summary["branch_chosen"] = opt["name"]
                        self.levelup_summary["branch_label"]  = label
                    self.branch_pending_char = None
                    self.branch_pending_opts = None
                    # Return to guild hub if that's where we came from
                    if getattr(self, "_guild_branch_origin", False):
                        self._guild_branch_origin = False
                        sfx.play("quest_accept")
                        self._msg(f"{c.name} chose: {label}", (200, 170, 255))
                        self.view = self.VIEW_GUILD
                    else:
                        self.view = self.VIEW_INN_LEVELUP_RESULT
                    return None

        elif self.view == self.VIEW_CLASSTREE:
            # Back button
            back_btn = pygame.Rect(SCREEN_W - 130, 12, 110, 34)
            if back_btn.collidepoint(mx, my):
                # Return to guild if entered from there
                if getattr(self, "_guild_classtree_origin", False):
                    self._guild_classtree_origin = False
                    self.view = self.VIEW_GUILD
                # Return to wherever we came from in the inn flow
                elif self.levelup_queue and self.levelup_current < len(self.levelup_queue):
                    self.view = self.VIEW_INN_LEVELUP
                else:
                    self.view = self.VIEW_INN
                return None
            # Character tabs
            tab_x = 20
            for i, ch in enumerate(self.party):
                tw = max(110, get_font(13).size(ch.name)[0] + 36)
                tr = pygame.Rect(tab_x, 48, tw, 30)
                if tr.collidepoint(mx, my):
                    self.classtree_char_idx = i
                    return None
                tab_x += tw + 6

        # ── Tavern ──
        elif self.view == self.VIEW_TAVERN:
            from data.shop_inventory import TAVERN
            from core.story_flags import get_flag

            # Tab switches
            for key, tr in getattr(self, '_tavern_tab_rects', []):
                if tr.collidepoint(mx, my):
                    self.tavern_tab = key
                    return None

            # Back
            if getattr(self, '_tavern_back_btn', None) and self._tavern_back_btn.collidepoint(mx, my):
                self._return_to_town()
                return None

            # ── PATRONS tab ───────────────────────────────────────────────────
            if self.tavern_tab == "patrons":
                for i, row in getattr(self, '_patron_rects', []):
                    if row.collidepoint(mx, my):
                        self.tavern_selected = i
                        return None

                drink_btn = getattr(self, '_tavern_drink_btn', None)
                patron_name = getattr(self, '_tavern_drink_patron', None)
                if drink_btn and patron_name and drink_btn.collidepoint(mx, my):
                    drink_cost = TAVERN.get("drink_cost", 2)
                    total_gold = sum(c.gold for c in self.party)
                    if total_gold >= drink_cost:
                        # Deduct gold
                        remaining = drink_cost
                        for c in self.party:
                            if c.gold >= remaining:
                                c.gold -= remaining
                                remaining = 0
                                break
                            elif c.gold > 0:
                                remaining -= c.gold
                                c.gold = 0
                        self.tavern_drinks[patron_name] = self.tavern_drinks.get(patron_name, 0) + 1
                        sfx.play("ui_confirm")
                        self._msg(f"You buy {patron_name} a drink. They seem more talkative.", RUMOR_COL)
                    else:
                        self._msg(f"You can't afford a drink! (need {drink_cost}g)", RED)

            # ── RECRUIT tab ───────────────────────────────────────────────────
            elif self.tavern_tab == "recruit":
                for i, rbtn, rec in getattr(self, '_recruit_rects', []):
                    if rbtn.collidepoint(mx, my):
                        if len(self.party) >= 6:
                            self._msg("Party is full! Leave someone at the tavern first.", RED)
                        else:
                            from core.character import Character
                            # Use pre-rolled Character if available (dynamic recruits)
                            if "_char" in rec and rec["_char"] is not None:
                                new_char = rec["_char"]
                                # Ensure HP is set
                                if not new_char.resources.get("HP"):
                                    new_char.resources["HP"] = new_char.resources.get("MAX_HP", 20)
                            else:
                                # Fallback: build from stat dict (legacy static recruits)
                                new_char = Character(name=rec["name"],
                                                     class_name=rec["class_name"],
                                                     race_name=rec["race_name"])
                                new_char.level = rec["level"]
                                for stat, val in rec["stats"].items():
                                    new_char.stats[stat] = val
                                from core.progression import recalculate_max_hp
                                try:
                                    recalculate_max_hp(new_char)
                                except Exception:
                                    new_char.resources["MAX_HP"] = 20 + new_char.stats.get("CON", 5) * 2
                                new_char.resources["HP"] = new_char.resources.get("MAX_HP", 20)
                                new_char.gold = 0
                            self.party.append(new_char)
                            # Remove this recruit from the pool so they can't be hired twice
                            rec["_char"] = None
                            sfx.play("ui_confirm")
                            self._msg(f"{rec['name']} joins your party!", GOLD)
                        return None

            # ── PARTY tab ─────────────────────────────────────────────────────
            elif self.tavern_tab == "party":
                for i, lbtn in getattr(self, '_leave_rects', []):
                    if lbtn.collidepoint(mx, my):
                        if len(self.party) <= 1:
                            self._msg("You can't leave your last party member behind.", RED)
                        else:
                            left = self.party.pop(i)
                            sfx.play("ui_click")
                            self._msg(f"{left.name} waits at the tavern.", DIM_GOLD)
                        return None

        # ── Forge ──
        elif self.view in (self.VIEW_FORGE, self.VIEW_FORGE_CRAFT,
                           self.VIEW_FORGE_UPGRADE, self.VIEW_FORGE_ENCHANT,
                           self.VIEW_FORGE_REPAIR):
            return self._handle_forge_click(mx, my)

        # ── Guild Hub ──
        elif self.view == self.VIEW_GUILD:
            # Back button
            back = getattr(self, "_guild_back_btn", None)
            if back and back.collidepoint(mx, my):
                self._return_to_town()
                return None

            for rect, action in getattr(self, "_guild_option_rects", []):
                if rect.collidepoint(mx, my):
                    if action == "jobboard":
                        self.view = self.VIEW_JOBBOARD
                    elif action == "train":
                        from core.abilities import has_branch_choice_pending
                        # Route to branch choice if anyone has a pending decision
                        pending_chars = [c for c in self.party if has_branch_choice_pending(c)]
                        if pending_chars:
                            c = pending_chars[0]
                            self.branch_pending_char = c
                            self.branch_pending_opts = has_branch_choice_pending(c)
                            self.branch_hover_idx = -1
                            self._guild_branch_origin = True
                            self.view = self.VIEW_BRANCH_CHOICE
                        else:
                            # No choices pending — open class tree
                            self.classtree_char_idx = 0
                            self._guild_classtree_origin = True
                            self.view = self.VIEW_CLASSTREE
                    elif action == "classtree":
                        self.classtree_char_idx = 0
                        self._guild_classtree_origin = True
                        self.view = self.VIEW_CLASSTREE
                    return None

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

    def _draw_forge_repair(self, surface, mx, my, y, total_gold, accent):
        """Draw the forge repair tab — list damaged equipment and repair buttons."""
        from core.durability import (
            has_durability, get_durability_state, get_durability_color,
            get_durability_label, get_repair_cost, repair_item, init_durability
        )

        GREY = (120, 110, 100)
        RED  = (220, 60, 60)
        draw_text(surface, "Repair damaged equipment:", 20, y, accent, 14, bold=True)
        draw_text(surface, "(Repairs all durability for a fixed gold cost)", 20, y + 18, GREY, 11)
        y += 40

        found_any = False
        btn_w, btn_h = 120, 30
        row_h = 52

        for ci, char in enumerate(self.party):
            for slot, item in list((char.equipment or {}).items()):
                if not item or not has_durability(item):
                    continue
                init_durability(item)
                state = get_durability_state(item)
                if state == "full":
                    continue
                found_any = True
                cost = get_repair_cost(item)
                can_afford = total_gold >= cost
                dur_col = get_durability_color(item)
                dur_lbl = get_durability_label(item)

                row = pygame.Rect(20, y, SCREEN_W - 180, row_h)
                pygame.draw.rect(surface, (22, 18, 35), row, border_radius=3)
                pygame.draw.rect(surface, accent, row, 1, border_radius=3)

                draw_text(surface, item.get("name", "?"), row.x + 10, row.y + 6, CREAM, 14, bold=True)
                draw_text(surface, f"{char.name} — {slot}", row.x + 10, row.y + 26, GREY, 11)
                draw_text(surface, f"Durability: {dur_lbl}", row.x + 320, row.y + 6, dur_col, 13)
                draw_text(surface, state.upper(), row.x + 320, row.y + 26, dur_col, 11)

                btn_col = accent if can_afford else RED
                btn = pygame.Rect(SCREEN_W - 150, y + 8, btn_w, btn_h)
                pygame.draw.rect(surface, (40, 30, 15) if can_afford else (35, 15, 15), btn, border_radius=3)
                pygame.draw.rect(surface, btn_col, btn, 1, border_radius=3)
                lbl = f"Repair {cost}g" if can_afford else f"Need {cost}g"
                draw_text(surface, lbl, btn.x + 8, btn.y + 7, btn_col, 12)

                y += row_h + 6

        if not found_any:
            draw_text(surface, "All equipment is in good condition.", 20, y, (100, 200, 100), 14)

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
            # Check for cursed status effects OR cursed equipped items
            for c in self.party:
                effects = get_status_effects(c)
                has_curse_effect = any(s.get("type") == "curse" for s in effects)
                cursed_slots = [
                    slot for slot, item in (c.equipment or {}).items()
                    if item and item.get("cursed") and not item.get("curse_lifted")
                ]
                if has_curse_effect or cursed_slots:
                    if total_gold < cost:
                        self._msg(f"Not enough gold! Need {cost}g.", RED)
                        return
                    self._deduct_gold(cost)
                    if has_curse_effect:
                        remove_all_curses(c)
                    # Lift all cursed equipment — mark as removable and unequip
                    for slot in cursed_slots:
                        item = c.equipment[slot]
                        item["curse_lifted"] = True
                        c.equipment[slot] = None
                        c.inventory.append(item)
                    msg = f"{c.name}'s curses have been lifted! ({cost}g)"
                    if cursed_slots:
                        names = ", ".join(c.equipment.get(s, {}).get("name", s) or s for s in cursed_slots)
                        msg = f"{c.name} freed from cursed gear! ({cost}g)"
                    self._msg(msg, HEAL_COL)
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

        bld_name = self.current_bld_name or "The Forge"
        self._draw_bld_npc_header(surface, bld_name, "", mx, my)
        total_gold = sum(c.gold for c in self.party)
        draw_text(surface, f"Gold: {total_gold}", SCREEN_W - 150, 20, DIM_GOLD, 14)

        # Tab bar
        tabs = [("Craft", self.VIEW_FORGE_CRAFT),
                ("Upgrade", self.VIEW_FORGE_UPGRADE),
                ("Enchant", self.VIEW_FORGE_ENCHANT),
                ("Repair",  self.VIEW_FORGE_REPAIR)]
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
        elif active_view == self.VIEW_FORGE_REPAIR:
            self._draw_forge_repair(surface, mx, my, y, total_gold, FORGE_ORANGE)

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
                (self.VIEW_FORGE_ENCHANT, 300), (self.VIEW_FORGE_REPAIR, 440)]
        for view, tx in tabs:
            tr = pygame.Rect(tx, 50, 130, 32)
            if tr.collidepoint(mx, my):
                self.view = view
                self.forge_scroll = 0
                self.forge_selected_item = None
                return None

        active_view = self.view if self.view != self.VIEW_FORGE else self.VIEW_FORGE_CRAFT
        y = 110

        if active_view == self.VIEW_FORGE_REPAIR:
            from core.durability import (
                has_durability, get_durability_state, get_repair_cost,
                repair_item, init_durability
            )
            y_r = 110 + 40
            row_h = 52
            btn_w, btn_h = 120, 30
            for ci, char in enumerate(self.party):
                for slot, item in list((char.equipment or {}).items()):
                    if not item or not has_durability(item):
                        continue
                    init_durability(item)
                    if get_durability_state(item) == "full":
                        continue
                    cost = get_repair_cost(item)
                    total_gold = sum(c.gold for c in self.party)
                    btn = pygame.Rect(SCREEN_W - 150, y_r + 8, btn_w, btn_h)
                    if btn.collidepoint(mx, my):
                        if total_gold < cost:
                            self._msg(f"Not enough gold! Need {cost}g.", RED)
                            return None
                        self._deduct_gold(cost)
                        repair_item(item)
                        sfx.play("shop_buy")
                        self._msg(f"Repaired {item.get('name','item')} for {cost}g.", (100, 220, 100))
                        return None
                    y_r += row_h + 6
            return None

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
