"""
Realm of Shadows — Quest Log UI

Shows active quests, completed quests, and discovered lore entries.
Accessible from the party screen or via hotkey.
"""
import pygame
from ui.renderer import (
    SCREEN_W, SCREEN_H, draw_text, draw_panel, draw_button, get_font,
    CREAM, GOLD, GREY, DARK_GREY, WHITE, PANEL_BG, PANEL_BORDER,
    HIGHLIGHT, DIM_GOLD, RED,
)


# Colors
LOG_BG = (12, 10, 22)
QUEST_ACTIVE = (80, 200, 120)
QUEST_COMPLETE = (120, 120, 140)
LORE_COL = (180, 160, 120)
TAB_ACTIVE = (50, 40, 80)
TAB_INACTIVE = (25, 20, 40)


class QuestLogUI:
    """Quest log and lore journal viewer."""

    def __init__(self):
        self.tab = "quests"  # "quests" or "lore"
        self.scroll = 0
        self.finished = False
        self.selected_lore = None

    def draw(self, surface, mx, my):
        surface.fill(LOG_BG)

        draw_text(surface, "Journal", SCREEN_W // 2 - 50, 15, GOLD, 24, bold=True)

        # Tabs
        tabs = [("quests", "Quests"), ("lore", "Lore")]
        for i, (key, label) in enumerate(tabs):
            tr = pygame.Rect(60 + i * 160, 55, 140, 34)
            is_sel = (self.tab == key)
            hover = tr.collidepoint(mx, my)
            bg = TAB_ACTIVE if is_sel else (35, 30, 55) if hover else TAB_INACTIVE
            border = GOLD if is_sel else HIGHLIGHT if hover else PANEL_BORDER
            pygame.draw.rect(surface, bg, tr, border_radius=3)
            pygame.draw.rect(surface, border, tr, 2, border_radius=3)
            draw_text(surface, label, tr.x + 20, tr.y + 7,
                      GOLD if is_sel else CREAM, 15, bold=is_sel)

        # Close button
        close = pygame.Rect(SCREEN_W - 120, 55, 100, 34)
        draw_button(surface, close, "Close", hover=close.collidepoint(mx, my), size=13)

        # Content area
        panel = pygame.Rect(40, 100, SCREEN_W - 80, SCREEN_H - 120)
        draw_panel(surface, panel, bg_color=(15, 12, 28))

        if self.tab == "quests":
            self._draw_quests(surface, mx, my, panel)
        else:
            self._draw_lore(surface, mx, my, panel)

    def _draw_quests(self, surface, mx, my, panel):
        from data.story_data import QUESTS
        from core.story_flags import get_quest_state

        active = []
        completed = []
        for qid, qdata in QUESTS.items():
            state = get_quest_state(qid)
            if state == -2:
                completed.append((qid, qdata))
            elif state > 0:
                active.append((qid, qdata))

        y = panel.y + 15
        if active:
            draw_text(surface, "Active Quests", panel.x + 15, y, GOLD, 16, bold=True)
            y += 28
            for qid, q in active:
                draw_text(surface, f"• {q['name']}", panel.x + 25, y, QUEST_ACTIVE, 14, bold=True)
                y += 20
                draw_text(surface, q.get("description", ""), panel.x + 40, y,
                          GREY, 12, max_width=panel.width - 80)
                # Estimate line count for spacing
                desc = q.get("description", "")
                lines = max(1, len(desc) // 70 + 1)
                y += lines * 16 + 10

        if completed:
            y += 10
            draw_text(surface, "Completed", panel.x + 15, y, QUEST_COMPLETE, 16, bold=True)
            y += 28
            for qid, q in completed:
                draw_text(surface, f"✓ {q['name']}", panel.x + 25, y, QUEST_COMPLETE, 13)
                y += 22

        if not active and not completed:
            draw_text(surface, "No quests yet. Speak to NPCs in town.",
                      panel.x + 40, panel.y + 60, DARK_GREY, 15)

    def _draw_lore(self, surface, mx, my, panel):
        from data.story_data import LORE_ENTRIES
        from core.story_flags import has_lore

        discovered = [(lid, ldata) for lid, ldata in LORE_ENTRIES.items()
                       if has_lore(lid)]

        y = panel.y + 15

        if self.selected_lore:
            # Show detailed lore entry
            ldata = LORE_ENTRIES.get(self.selected_lore, {})
            draw_text(surface, ldata.get("title", ""), panel.x + 20, y, LORE_COL, 18, bold=True)
            y += 30
            text = ldata.get("text", "")
            # Simple word wrap
            words = text.split()
            line = ""
            max_w = panel.width - 60
            for w in words:
                test = line + (" " if line else "") + w
                if get_font(14).size(test)[0] <= max_w:
                    line = test
                else:
                    draw_text(surface, line, panel.x + 30, y, CREAM, 14)
                    y += 20
                    line = w
            if line:
                draw_text(surface, line, panel.x + 30, y, CREAM, 14)
                y += 20

            # Back button
            back = pygame.Rect(panel.x + 20, y + 20, 100, 30)
            draw_button(surface, back, "Back", hover=back.collidepoint(mx, my), size=12)
        else:
            draw_text(surface, "Discovered Lore", panel.x + 15, y, GOLD, 16, bold=True)
            y += 28

            if not discovered:
                draw_text(surface, "No lore discovered yet. Explore dungeons and talk to NPCs.",
                          panel.x + 40, panel.y + 60, DARK_GREY, 15)
            else:
                for lid, ldata in discovered:
                    entry_rect = pygame.Rect(panel.x + 15, y, panel.width - 30, 36)
                    hover = entry_rect.collidepoint(mx, my)
                    bg = (30, 25, 50) if hover else (20, 17, 35)
                    pygame.draw.rect(surface, bg, entry_rect, border_radius=3)
                    pygame.draw.rect(surface, HIGHLIGHT if hover else PANEL_BORDER,
                                     entry_rect, 1, border_radius=3)
                    draw_text(surface, ldata["title"], entry_rect.x + 12, entry_rect.y + 8,
                              LORE_COL if hover else CREAM, 14)
                    y += 42

    def handle_click(self, mx, my):
        """Returns 'close' to exit, or None."""
        # Close button
        close = pygame.Rect(SCREEN_W - 120, 55, 100, 34)
        if close.collidepoint(mx, my):
            self.finished = True
            return "close"

        # Tab clicks
        tabs = ["quests", "lore"]
        for i, key in enumerate(tabs):
            tr = pygame.Rect(60 + i * 160, 55, 140, 34)
            if tr.collidepoint(mx, my):
                self.tab = key
                self.selected_lore = None
                return None

        # Lore entry clicks
        if self.tab == "lore":
            panel = pygame.Rect(40, 100, SCREEN_W - 80, SCREEN_H - 120)

            if self.selected_lore:
                # Back button in detail view
                from data.story_data import LORE_ENTRIES
                ldata = LORE_ENTRIES.get(self.selected_lore, {})
                text = ldata.get("text", "")
                lines = len(text) // 70 + 3
                back_y = panel.y + 15 + 30 + lines * 20 + 20
                back = pygame.Rect(panel.x + 20, back_y, 100, 30)
                if back.collidepoint(mx, my):
                    self.selected_lore = None
                    return None
            else:
                from data.story_data import LORE_ENTRIES
                from core.story_flags import has_lore
                discovered = [(lid, ldata) for lid, ldata in LORE_ENTRIES.items()
                               if has_lore(lid)]
                y = panel.y + 15 + 28
                for lid, ldata in discovered:
                    entry_rect = pygame.Rect(panel.x + 15, y, panel.width - 30, 36)
                    if entry_rect.collidepoint(mx, my):
                        self.selected_lore = lid
                        return None
                    y += 42

        return None

    def handle_scroll(self, direction):
        self.scroll += direction
