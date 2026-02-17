"""
Realm of Shadows — Town Hub UI

Town locations:
  General Store — buy weapons, armor, consumables; sell inventory items
  Temple        — rest/heal (free), identify items (15g), remove curse (50g)
  Tavern        — hear rumors, flavor text
  Exit          — leave town (back to world/encounters)
"""
import random
import pygame
from ui.renderer import *
from core.classes import CLASSES
from core.identification import get_item_display_name
from data.shop_inventory import (
    GENERAL_STORE, TEMPLE, TAVERN, get_sell_price,
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
    VIEW_SHOP = "shop"
    VIEW_SHOP_BUY = "shop_buy"
    VIEW_SHOP_SELL = "shop_sell"
    VIEW_TEMPLE = "temple"
    VIEW_TAVERN = "tavern"

    def __init__(self, party):
        self.party = party
        self.view = self.VIEW_HUB
        self.message = ""
        self.msg_timer = 0
        self.msg_color = CREAM
        self.finished = False

        # Shop state
        self.shop_tab = "weapons"  # weapons, armor, consumables
        self.shop_scroll = 0
        self.sell_char = 0
        self.sell_scroll = 0

        # Temple state
        self.id_char = 0
        self.id_scroll = 0

        # Tavern state
        self.current_rumor = random.choice(TAVERN["rumors"])

    # ─────────────────────────────────────────────────────────
    #  MAIN DRAW
    # ─────────────────────────────────────────────────────────

    def draw(self, surface, mx, my, dt):
        self.msg_timer = max(0, self.msg_timer - dt)
        surface.fill(TOWN_BG)

        if self.view == self.VIEW_HUB:
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

        # Message bar
        if self.message and self.msg_timer > 0:
            draw_text(surface, self.message, SCREEN_W // 2 - 250,
                      SCREEN_H - 30, self.msg_color, 15)

    # ─────────────────────────────────────────────────────────
    #  HUB — Main town menu
    # ─────────────────────────────────────────────────────────

    def _draw_hub(self, surface, mx, my):
        draw_text(surface, "Town of Briarhollow", SCREEN_W // 2 - 130, 30,
                  GOLD, 28, bold=True)
        draw_text(surface, "A quiet settlement at the edge of the wilds.",
                  SCREEN_W // 2 - 190, 70, GREY, 15)

        # Party gold
        total_gold = sum(c.gold for c in self.party)
        draw_text(surface, f"Party Gold: {total_gold}",
                  SCREEN_W // 2 - 60, 100, DIM_GOLD, 16)

        # Location buttons
        locations = [
            ("General Store", "Buy and sell weapons, armor, and supplies",
             (120, 100, 50), SELL_COL),
            ("Temple of Light", "Rest, heal, identify items, remove curses",
             (50, 100, 120), HEAL_COL),
            ("The Shadowed Flagon", "Hear rumors and rest your feet",
             (100, 60, 100), RUMOR_COL),
            ("Leave Town", "Return to the wilds",
             (80, 40, 40), RED),
        ]

        by = 160
        for i, (name, desc, bg_tint, accent) in enumerate(locations):
            btn_rect = pygame.Rect(SCREEN_W // 2 - 250, by + i * 120, 500, 100)
            hover = btn_rect.collidepoint(mx, my)

            bg = (bg_tint[0] + 20, bg_tint[1] + 20, bg_tint[2] + 20) if hover else bg_tint
            border = accent if hover else PANEL_BORDER

            pygame.draw.rect(surface, bg, btn_rect, border_radius=5)
            pygame.draw.rect(surface, border, btn_rect, 2, border_radius=5)

            draw_text(surface, name, btn_rect.x + 20, btn_rect.y + 15,
                      accent if hover else CREAM, 22, bold=True)
            draw_text(surface, desc, btn_rect.x + 20, btn_rect.y + 50,
                      GREY, 14)

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

    # ─────────────────────────────────────────────────────────
    #  GENERAL STORE — Menu
    # ─────────────────────────────────────────────────────────

    def _draw_shop_menu(self, surface, mx, my):
        draw_text(surface, "General Store", SCREEN_W // 2 - 90, 20, GOLD, 24, bold=True)
        draw_text(surface, GENERAL_STORE["welcome"], SCREEN_W // 2 - 150, 55, GREY, 14)

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

        # Item list
        items = GENERAL_STORE.get(self.shop_tab, [])
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
                row = pygame.Rect(panel.x + 8, iy, panel.width - 16, 68)
                hover = row.collidepoint(mx, my)
                bg = ITEM_HOVER if hover else ITEM_BG
                pygame.draw.rect(surface, bg, row, border_radius=3)
                pygame.draw.rect(surface, HIGHLIGHT if hover else PANEL_BORDER, row, 1, border_radius=3)

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
                if not item.get("identified"):
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
    #  CLICK HANDLING
    # ─────────────────────────────────────────────────────────

    def handle_click(self, mx, my):
        """Returns 'exit' to leave town, or None."""

        # ── Hub view ──
        if self.view == self.VIEW_HUB:
            locations = ["shop", "temple", "tavern", "exit"]
            by = 160
            for i, loc in enumerate(locations):
                btn = pygame.Rect(SCREEN_W // 2 - 250, by + i * 120, 500, 100)
                if btn.collidepoint(mx, my):
                    if loc == "exit":
                        self.finished = True
                        return "exit"
                    elif loc == "shop":
                        self.view = self.VIEW_SHOP
                    elif loc == "temple":
                        self.view = self.VIEW_TEMPLE
                    elif loc == "tavern":
                        self.view = self.VIEW_TAVERN
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
                        self.view = self.VIEW_HUB
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

            # Item clicks
            items = GENERAL_STORE.get(self.shop_tab, [])
            panel = pygame.Rect(20, 95, SCREEN_W - 40, SCREEN_H - 200)
            iy = panel.y + 10
            start = self.shop_scroll
            end = min(len(items), start + 8)
            for idx in range(start, end):
                row = pygame.Rect(panel.x + 8, iy, panel.width - 16, 68)
                if row.collidepoint(mx, my):
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
                self.view = self.VIEW_HUB
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
                    if not item.get("identified"):
                        unid_items.append((ci, ii, item, c))

            if unid_items:
                uy = by + svc_count * 80 + 45
                for ui_idx, (ci, ii, item, char) in enumerate(unid_items[:5]):
                    row = pygame.Rect(SCREEN_W // 2 - 250, uy, 500, 40)
                    if row.collidepoint(mx, my):
                        self._temple_identify(ci, ii, item, char)
                        return None
                    uy += 44

        # ── Tavern ──
        elif self.view == self.VIEW_TAVERN:
            back = pygame.Rect(SCREEN_W - 140, 30, 120, 34)
            if back.collidepoint(mx, my):
                self.view = self.VIEW_HUB
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
        self.party[0].inventory.append(new_item)

        self._msg(f"Bought {shop_item['name']} for {price}g — added to {self.party[0].name}'s inventory", BUY_COL)

    def _sell_item(self, char, item_idx):
        """Sell an item from a character's inventory."""
        if item_idx >= len(char.inventory):
            return
        item = char.inventory[item_idx]
        price = get_sell_price(item)
        char.inventory.pop(item_idx)
        char.gold += price
        name = get_item_display_name(item)
        self._msg(f"Sold {name} for {price}g", SELL_COL)

    def _use_temple_service(self, service_key):
        """Use a temple service."""
        svc = TEMPLE["services"][service_key]
        cost = svc["cost"]
        total_gold = sum(c.gold for c in self.party)

        if cost > 0 and total_gold < cost:
            self._msg(f"Not enough gold! Need {cost}g.", RED)
            return

        if service_key == "rest_heal":
            from core.classes import get_all_resources
            for c in self.party:
                c.resources = get_all_resources(c.class_name, c.stats, c.level)
            self._msg("The temple's warm light washes over you. Party fully restored!", HEAL_COL)

        elif service_key == "identify_item":
            # Just show the message — actual identification is via item clicks below
            self._msg("Click an unidentified item below to identify it (15g each).", DIM_GOLD)

        elif service_key == "remove_curse":
            self._deduct_gold(cost)
            self._msg("The priests perform a cleansing ritual. Curses removed!", HEAL_COL)

        elif service_key == "resurrect":
            self._deduct_gold(cost)
            self._msg("Divine light restores the fallen! Party member resurrected.", HEAL_COL)

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
            items = GENERAL_STORE.get(self.shop_tab, [])
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
