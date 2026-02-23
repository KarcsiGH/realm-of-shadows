"""
Realm of Shadows — Dialogue UI

Renders NPC dialogue with speaker name, text, portrait color indicator,
and clickable choices. Supports auto-advance for non-choice nodes.
"""
import pygame
from ui.renderer import (
    SCREEN_W, SCREEN_H, draw_text, draw_panel, draw_button, get_font,
    CREAM, GOLD, GREY, DARK_GREY, WHITE, PANEL_BG, PANEL_BORDER,
    HIGHLIGHT, DIM_GOLD, ORANGE, RED,
)

# Colors
DIALOGUE_BG = (12, 10, 25)
SPEAKER_COL = (255, 220, 120)
TEXT_COL = (220, 215, 200)
CHOICE_BG = (25, 22, 45)
CHOICE_HOVER = (45, 38, 70)
CHOICE_BORDER = (80, 70, 120)
CHOICE_HOVER_BORDER = GOLD
NARRATOR_COL = (160, 150, 180)
LOG_DIM = (120, 115, 130)

# Layout
PORTRAIT_SIZE = 60
DIALOGUE_MARGIN = 40
TEXT_AREA_Y = 200          # moved up to give more room
CHOICES_BOTTOM_MARGIN = 40 # space from bottom for choices
MAX_TEXT_LINES = 8         # scroll if more


class DialogueUI:
    """Renders and handles input for a dialogue conversation."""

    def __init__(self, dialogue_state):
        self.state = dialogue_state
        self.finished = False
        self.hover_choice = -1
        self.auto_advance_timer = 0
        self.result = None  # can hold outcome info (e.g., "fight" for boss dialogues)

        # Typing effect
        self.displayed_chars = 0
        self.type_speed = 2  # chars per frame
        self.full_text_shown = False

        # Text scroll
        self.text_scroll = 0

    def draw(self, surface, mx, my, dt=16):
        surface.fill(DIALOGUE_BG)

        if self.state.finished:
            self.finished = True
            return

        node = self.state.current_node
        speaker = node.get("speaker", "")
        text = node.get("text", "")
        portrait_color = self._get_portrait_color(speaker)

        # ── Log (previous dialogue, scrolled up) ──
        log_y = 20
        visible_log = self.state.log[:-1][-5:] if len(self.state.log) > 1 else []
        for log_speaker, log_text in visible_log:
            if log_speaker == "You":
                prefix = f"  > {log_text}"
                col = DIM_GOLD
            elif log_speaker:
                prefix = f"  {log_speaker}: {log_text[:90]}{'...' if len(log_text) > 90 else ''}"
                col = LOG_DIM
            else:
                prefix = f"  {log_text[:90]}{'...' if len(log_text) > 90 else ''}"
                col = (100, 95, 110)
            draw_text(surface, prefix, DIALOGUE_MARGIN, log_y, col, 11)
            log_y += 16

        # ── Divider ──
        div_y = max(log_y + 8, TEXT_AREA_Y - 30)
        pygame.draw.line(surface, (40, 35, 60),
                         (DIALOGUE_MARGIN, div_y),
                         (SCREEN_W - DIALOGUE_MARGIN, div_y))

        # ── Speaker + Portrait indicator ──
        content_y = div_y + 12
        if speaker:
            pr = pygame.Rect(DIALOGUE_MARGIN, content_y, PORTRAIT_SIZE, PORTRAIT_SIZE)
            pygame.draw.rect(surface, portrait_color, pr, border_radius=5)
            pygame.draw.rect(surface, PANEL_BORDER, pr, 2, border_radius=5)
            initial = speaker[0].upper()
            iw = get_font(28).size(initial)[0]
            draw_text(surface, initial,
                      pr.x + (PORTRAIT_SIZE - iw) // 2,
                      pr.y + (PORTRAIT_SIZE - 28) // 2,
                      WHITE, 28, bold=True)
            draw_text(surface, speaker,
                      DIALOGUE_MARGIN + PORTRAIT_SIZE + 15, content_y,
                      SPEAKER_COL, 20, bold=True)
            text_x = DIALOGUE_MARGIN + PORTRAIT_SIZE + 15
            text_y = content_y + 26
        else:
            text_x = DIALOGUE_MARGIN + 10
            text_y = content_y + 5

        # ── Text with typing effect ──
        self.displayed_chars = min(self.displayed_chars + self.type_speed, len(text))
        shown_text = text[:int(self.displayed_chars)]
        self.full_text_shown = self.displayed_chars >= len(text)

        max_w = SCREEN_W - text_x - DIALOGUE_MARGIN
        lines = self._wrap_text(shown_text, max_w, 15)

        # Determine how much space choices need
        choices = self.state.get_choices() if self.full_text_shown else []
        choice_count = len(choices)
        choice_height = choice_count * 44 + 20 if choice_count > 0 else 50
        available_text_height = SCREEN_H - text_y - choice_height - CHOICES_BOTTOM_MARGIN - 10

        # Calculate visible text lines
        line_h = 20
        max_visible = max(3, available_text_height // line_h)

        # Auto-scroll to show latest text
        if len(lines) > max_visible:
            self.text_scroll = len(lines) - max_visible

        visible_lines = lines[self.text_scroll:self.text_scroll + max_visible]
        for i, line in enumerate(visible_lines):
            col = TEXT_COL if speaker else NARRATOR_COL
            draw_text(surface, line, text_x, text_y + i * line_h, col, 15)

        # Scroll indicator
        if len(lines) > max_visible:
            draw_text(surface, "▼ more ▼", text_x, text_y + max_visible * line_h,
                      DARK_GREY, 10)

        # ── Choices or continue prompt ──
        choices_y = SCREEN_H - choice_height - CHOICES_BOTTOM_MARGIN

        if self.full_text_shown:
            if self.state.has_choices():
                self._draw_choices(surface, mx, my, choices_y)
            elif self.state.should_auto_advance():
                draw_text(surface, "Click or press SPACE to continue...",
                          SCREEN_W // 2 - 130, SCREEN_H - 45, DIM_GOLD, 14)
            else:
                draw_text(surface, "Click or press SPACE to close.",
                          SCREEN_W // 2 - 115, SCREEN_H - 45, DIM_GOLD, 14)
        else:
            draw_text(surface, "Click to show all...",
                      SCREEN_W // 2 - 70, SCREEN_H - 45, DARK_GREY, 12)

    def _draw_choices(self, surface, mx, my, top_y):
        self.hover_choice = -1
        choices = self.state.get_choices()

        for i, choice in enumerate(choices):
            rect = pygame.Rect(DIALOGUE_MARGIN + 20, top_y + i * 44,
                               SCREEN_W - DIALOGUE_MARGIN * 2 - 40, 38)
            hover = rect.collidepoint(mx, my)
            if hover:
                self.hover_choice = i

            bg = CHOICE_HOVER if hover else CHOICE_BG
            border = CHOICE_HOVER_BORDER if hover else CHOICE_BORDER
            pygame.draw.rect(surface, bg, rect, border_radius=4)
            pygame.draw.rect(surface, border, rect, 2, border_radius=4)

            # Number prefix for keyboard selection
            num = str(i + 1)
            col = GOLD if hover else CREAM
            draw_text(surface, f"{num}.", rect.x + 8, rect.y + 9, DIM_GOLD, 13)
            draw_text(surface, choice["text"], rect.x + 28, rect.y + 9, col, 14)

    def handle_click(self, mx, my):
        """Handle mouse click. Returns action string or None."""
        if self.state.finished:
            self.finished = True
            return "done"

        # If text not fully shown, show it all
        if not self.full_text_shown:
            self.displayed_chars = 999999
            return None

        # If choices available, check click
        if self.state.has_choices():
            if self.hover_choice >= 0:
                choice = self.state.get_choices()[self.hover_choice]
                # Check if this choice leads to a fight
                next_id = choice.get("next", "")

                self.state.select_choice(self.hover_choice)
                self.displayed_chars = 0
                self.text_scroll = 0

                # Check if the new node is the "fight" node
                if self.state.finished:
                    node = self.state.current_node
                    if node.get("on_enter"):
                        for act in node["on_enter"]:
                            if act.get("flag", "").endswith(".killed"):
                                self.result = "fight"
                            elif act.get("flag", "").endswith("_spared") or \
                                 act.get("flag", "") == "goblin_peace":
                                self.result = "peace"
                    return "done"
                return None
        elif self.state.should_auto_advance():
            self.state.advance()
            self.displayed_chars = 0
            if self.state.finished:
                # Check final node for result
                node = self.state.current_node
                if node.get("on_enter"):
                    for act in node["on_enter"]:
                        if act.get("flag", "").endswith(".killed"):
                            self.result = "fight"
                        elif act.get("flag", "").endswith("_spared") or \
                             act.get("flag", "") == "goblin_peace":
                            self.result = "peace"
                # Also check if peace was already set in earlier nodes
                from core.story_flags import get_flag
                if get_flag("choice.grak_spared"):
                    self.result = "peace"
                return "done"
            return None
        else:
            self.finished = True
            return "done"

        return None

    def handle_event(self, event):
        """Handle keyboard events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                return self.handle_click(0, 0)
            elif event.key == pygame.K_ESCAPE:
                self.finished = True
                return "done"
            # Number keys 1-9 for choice selection
            elif self.full_text_shown and self.state.has_choices():
                choices = self.state.get_choices()
                num = event.key - pygame.K_1  # K_1 = 0, K_2 = 1, etc.
                if 0 <= num < len(choices):
                    choice = choices[num]
                    self.state.select_choice(num)
                    self.displayed_chars = 0
                    self.text_scroll = 0
                    if self.state.finished:
                        node = self.state.current_node
                        if node.get("on_enter"):
                            for act in node["on_enter"]:
                                if act.get("flag", "").endswith(".killed"):
                                    self.result = "fight"
                                elif act.get("flag", "").endswith("_spared") or \
                                     act.get("flag", "") == "goblin_peace":
                                    self.result = "peace"
                        from core.story_flags import get_flag
                        if get_flag("choice.grak_spared"):
                            self.result = "peace"
                        return "done"
                    return None
        return None

    def _get_portrait_color(self, speaker):
        """Get portrait color for a speaker."""
        from data.story_data import NPCS
        for npc_id, npc in NPCS.items():
            if npc["name"] == speaker:
                return npc.get("portrait_color", (80, 80, 80))
        if speaker == "You":
            return (60, 80, 160)
        return (60, 55, 80)  # default narrator

    def _wrap_text(self, text, max_width, font_size):
        """Simple word-wrap for dialogue text."""
        font = get_font(font_size)
        words = text.split()
        lines = []
        current = ""
        for word in words:
            test = current + (" " if current else "") + word
            if font.size(test)[0] <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines if lines else [""]
