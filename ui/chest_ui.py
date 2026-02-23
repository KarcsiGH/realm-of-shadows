"""
Realm of Shadows — Chest Loot UI

Shown when the party opens a treasure chest or secret chest.
Displays found gold and items; lets the player assign each item
to any party member before closing.
"""
import pygame
from ui.renderer import (
    draw_text, draw_panel, draw_button, get_font,
    SCREEN_W, SCREEN_H, BG_COLOR, PANEL_BG, PANEL_BORDER,
    GOLD, DIM_GOLD, CREAM, GREY, DARK_GREY, HIGHLIGHT,
    GREEN, RED, ORANGE,
)
from core.identification import get_item_display_name, get_item_display_desc

# ── Colours ───────────────────────────────────────────────────
SECRET_COL   = (200, 140, 255)   # purple tint for secret chests
ITEM_BG      = (18, 15, 32)
ITEM_HOVER   = (40, 32, 65)
ITEM_BORDER  = (60, 50, 90)
ITEM_SEL     = (60, 80, 130)
TAKEN_BG     = (15, 28, 15)
TAKEN_BORDER = (40, 100, 40)
RARITY_COLORS = {
    "common":    CREAM,
    "uncommon":  (100, 220, 100),
    "rare":      (80, 160, 255),
    "epic":      (200, 100, 255),
    "legendary": (255, 160, 40),
}


class ChestUI:
    """
    Modal chest loot screen.

    State machine:
      "overview"    — list of all loot; player clicks an item to assign it
      "assign"      — choose which party member receives the selected item
    """

    def __init__(self, party, gold, items, is_secret=False):
        self.party      = party
        self.gold       = gold          # already distributed before showing
        self.items      = [dict(i) for i in items]   # copies
        self.is_secret  = is_secret
        self.finished   = False

        # Track who got each item: index → char index or None
        self.assignments = {i: None for i in range(len(self.items))}

        self.mode         = "overview"   # "overview" | "assign"
        self.selected_idx = -1          # item being assigned
        self.hover_item   = -1
        self.hover_char   = -1
        self.message      = ""
        self.message_timer = 0

        # Distribute gold automatically (already done in main, just display)
        self._gold_per_char = gold // max(len(party), 1) if gold else 0

        # Hover tracking rects (rebuilt each draw)
        self._item_rects = []
        self._char_rects = []
        self._close_rect = None

    # ─────────────────────────────────────────────────────────
    #  DRAWING
    # ─────────────────────────────────────────────────────────

    def draw(self, surface, mx, my, dt):
        self.message_timer = max(0, self.message_timer - dt)
        self.hover_item = -1
        self.hover_char = -1

        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        # Main panel
        pw, ph = 820, 640
        px = (SCREEN_W - pw) // 2
        py = (SCREEN_H - ph) // 2
        panel = pygame.Rect(px, py, pw, ph)
        draw_panel(surface, panel, bg_color=(16, 12, 28))

        # Title
        title_col = SECRET_COL if self.is_secret else GOLD
        title = "★ Secret Chest!" if self.is_secret else "Treasure Chest"
        draw_text(surface, title, px + pw // 2 - get_font(26).size(title)[0] // 2,
                  py + 14, title_col, 26, bold=True)

        # Gold line
        if self.gold > 0:
            g_txt = f"{self.gold} gold found — {self._gold_per_char}g each"
            draw_text(surface, g_txt,
                      px + pw // 2 - get_font(15).size(g_txt)[0] // 2,
                      py + 52, DIM_GOLD, 15)
        else:
            draw_text(surface, "No gold found.", px + 20, py + 52, DARK_GREY, 14)

        # Close / Done button
        close_rect = pygame.Rect(px + pw - 130, py + 14, 115, 34)
        self._close_rect = close_rect
        all_assigned = all(v is not None for v in self.assignments.values()) \
                       or not self.items
        close_label = "Done" if all_assigned else "Take All → Leader"
        draw_button(surface, close_rect, close_label,
                    hover=close_rect.collidepoint(mx, my), size=13)

        # ── Items list ──────────────────────────────────────
        list_top = py + 82
        self._item_rects = []

        if not self.items:
            draw_text(surface, "The chest is empty.", px + 30, list_top + 10,
                      DARK_GREY, 16)
        else:
            for i, item in enumerate(self.items):
                assigned_to = self.assignments[i]
                taken = assigned_to is not None

                item_rect = pygame.Rect(px + 16, list_top + i * 74,
                                        pw - 32, 68)
                self._item_rects.append(item_rect)

                is_hover = item_rect.collidepoint(mx, my) and not taken
                is_selected = (i == self.selected_idx)

                if taken:
                    bg = TAKEN_BG
                    border = TAKEN_BORDER
                elif is_selected:
                    bg = ITEM_SEL
                    border = HIGHLIGHT
                elif is_hover:
                    bg = ITEM_HOVER
                    border = HIGHLIGHT
                    self.hover_item = i
                else:
                    bg = ITEM_BG
                    border = ITEM_BORDER

                pygame.draw.rect(surface, bg, item_rect, border_radius=4)
                pygame.draw.rect(surface, border, item_rect, 2, border_radius=4)

                # Item name
                display = get_item_display_name(item)
                rarity  = item.get("rarity", "common")
                name_col = RARITY_COLORS.get(rarity, CREAM) if item.get("identified") \
                           else (160, 140, 200)
                draw_text(surface, display, item_rect.x + 12, item_rect.y + 6,
                          name_col, 15, bold=True)

                # Brief stats line
                desc = get_item_display_desc(item)
                if len(desc) > 85:
                    desc = desc[:82] + "..."
                draw_text(surface, desc, item_rect.x + 12, item_rect.y + 28,
                          GREY, 11, max_width=pw - 240)

                # Right side: assignment status / button
                rx = item_rect.x + item_rect.width - 160
                if taken:
                    char_name = self.party[assigned_to].name
                    draw_text(surface, f"✓ {char_name}",
                              rx, item_rect.y + 22, (80, 200, 80), 13, bold=True)
                elif is_selected:
                    draw_text(surface, "↑ choose below",
                              rx, item_rect.y + 22, HIGHLIGHT, 12)
                else:
                    btn = pygame.Rect(rx, item_rect.y + 16, 140, 30)
                    draw_button(surface, btn, "Assign to…",
                                hover=is_hover, size=12)

        # ── Party selector (shown when an item is selected) ──
        if self.mode == "assign" and self.selected_idx >= 0:
            self._draw_assign_panel(surface, mx, my, px, py, pw, ph)

        # ── Message bar ──
        if self.message and self.message_timer > 0:
            draw_text(surface, self.message,
                      px + pw // 2 - get_font(14).size(self.message)[0] // 2,
                      py + ph - 30, CREAM, 14)

    def _draw_assign_panel(self, surface, mx, my, px, py, pw, ph):
        """Bottom strip: choose which character gets the selected item."""
        strip_h = 110
        strip = pygame.Rect(px + 8, py + ph - strip_h - 12, pw - 16, strip_h)
        pygame.draw.rect(surface, (20, 16, 38), strip, border_radius=6)
        pygame.draw.rect(surface, HIGHLIGHT, strip, 2, border_radius=6)

        item = self.items[self.selected_idx]
        name = get_item_display_name(item)
        draw_text(surface, f"Give \"{name}\" to:",
                  strip.x + 16, strip.y + 8, CREAM, 14)

        self._char_rects = []
        cw = (strip.width - 32) // len(self.party)
        for ci, char in enumerate(self.party):
            crect = pygame.Rect(strip.x + 16 + ci * cw, strip.y + 34, cw - 8, 58)
            self._char_rects.append(crect)

            is_hover = crect.collidepoint(mx, my)
            if is_hover:
                self.hover_char = ci
            already_has = self.assignments[self.selected_idx] == ci

            bg = (40, 60, 40) if already_has else \
                 (50, 42, 80) if is_hover else (25, 20, 42)
            border = (80, 200, 80) if already_has else \
                     HIGHLIGHT if is_hover else PANEL_BORDER
            pygame.draw.rect(surface, bg, crect, border_radius=4)
            pygame.draw.rect(surface, border, crect, 2, border_radius=4)

            draw_text(surface, char.name, crect.x + 8, crect.y + 4,
                      CREAM, 13, bold=True)
            draw_text(surface, char.class_name, crect.x + 8, crect.y + 22,
                      GREY, 11)
            inv_count = len(char.inventory)
            draw_text(surface, f"{inv_count} items", crect.x + 8, crect.y + 38,
                      DARK_GREY, 10)

        # Cancel hint
        draw_text(surface, "ESC / click elsewhere to cancel",
                  strip.x + strip.width - 240, strip.y + strip.height - 18,
                  DARK_GREY, 11)

    # ─────────────────────────────────────────────────────────
    #  INPUT
    # ─────────────────────────────────────────────────────────

    def handle_click(self, mx, my):
        """Returns None normally, 'done' when finished."""
        # Done / Take-all button
        if self._close_rect and self._close_rect.collidepoint(mx, my):
            self._take_all_unassigned()
            self.finished = True
            return "done"

        # If in assign mode: character strip
        if self.mode == "assign":
            for ci, crect in enumerate(self._char_rects):
                if crect.collidepoint(mx, my):
                    self._assign_item(self.selected_idx, ci)
                    return None
            # Click outside assign panel → cancel selection
            self.mode = "overview"
            self.selected_idx = -1
            return None

        # Overview mode: item rows
        for i, rect in enumerate(self._item_rects):
            if rect.collidepoint(mx, my):
                if self.assignments[i] is not None:
                    return None   # already assigned, ignore
                self.selected_idx = i
                self.mode = "assign"
                return None

        return None

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.mode == "assign":
                    self.mode = "overview"
                    self.selected_idx = -1
                else:
                    self._take_all_unassigned()
                    self.finished = True
                    return "done"
            elif event.key == pygame.K_RETURN:
                if self.mode == "overview":
                    self._take_all_unassigned()
                    self.finished = True
                    return "done"
        return None

    # ─────────────────────────────────────────────────────────
    #  LOGIC
    # ─────────────────────────────────────────────────────────

    def _assign_item(self, item_idx, char_idx):
        item = self.items[item_idx]
        char = self.party[char_idx]
        char.add_item(dict(item))
        self.assignments[item_idx] = char_idx
        name = get_item_display_name(item)
        self._show_message(f"{name} → {char.name}")
        self.mode = "overview"
        self.selected_idx = -1

        # Auto-advance: if all assigned, leave assign mode cleanly
        if all(v is not None for v in self.assignments.values()):
            self._show_message("All items distributed! Press Done.")

    def _take_all_unassigned(self):
        """Give any unclaimed items to the party leader."""
        if not self.party:
            return
        leader = self.party[0]
        for i, item in enumerate(self.items):
            if self.assignments[i] is None:
                leader.add_item(dict(item))
                self.assignments[i] = 0

    def _show_message(self, msg):
        self.message = msg
        self.message_timer = 3.0
