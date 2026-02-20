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
TEXT_AREA_Y = 320
TEXT_AREA_H = 380


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
        log_y = 30
        # Show last 4 log entries
        visible_log = self.state.log[:-1][-4:] if len(self.state.log) > 1 else []
        for log_speaker, log_text in visible_log:
            if log_speaker == "You":
                prefix = f"  > {log_text}"
                col = DIM_GOLD
            elif log_speaker:
                prefix = f"  {log_speaker}: {log_text[:80]}{'...' if len(log_text) > 80 else ''}"
                col = LOG_DIM
            else:
                prefix = f"  {log_text[:80]}{'...' if len(log_text) > 80 else ''}"
                col = (100, 95, 110)
            draw_text(surface, prefix, DIALOGUE_MARGIN, log_y, col, 11)
            log_y += 18

        # ── Divider ──
        div_y = max(log_y + 10, TEXT_AREA_Y - 40)
        pygame.draw.line(surface, (40, 35, 60),
                         (DIALOGUE_MARGIN, div_y),
                         (SCREEN_W - DIALOGUE_MARGIN, div_y))

        # ── Speaker + Portrait indicator ──
        content_y = div_y + 15
        if speaker:
            # Portrait color block
            pr = pygame.Rect(DIALOGUE_MARGIN, content_y, PORTRAIT_SIZE, PORTRAIT_SIZE)
            pygame.draw.rect(surface, portrait_color, pr, border_radius=5)
            pygame.draw.rect(surface, PANEL_BORDER, pr, 2, border_radius=5)
            # Speaker initial
            initial = speaker[0].upper()
            iw = get_font(28).size(initial)[0]
            draw_text(surface, initial,
                      pr.x + (PORTRAIT_SIZE - iw) // 2,
                      pr.y + (PORTRAIT_SIZE - 28) // 2,
                      WHITE, 28, bold=True)

            # Speaker name
            draw_text(surface, speaker,
                      DIALOGUE_MARGIN + PORTRAIT_SIZE + 15, content_y,
                      SPEAKER_COL, 20, bold=True)
            text_x = DIALOGUE_MARGIN + PORTRAIT_SIZE + 15
            text_y = content_y + 28
        else:
            # Narrator (no speaker)
            text_x = DIALOGUE_MARGIN + 10
            text_y = content_y + 5

        # ── Text with typing effect ──
        self.displayed_chars = min(self.displayed_chars + self.type_speed, len(text))
        shown_text = text[:int(self.displayed_chars)]
        self.full_text_shown = self.displayed_chars >= len(text)

        # Word wrap
        max_w = SCREEN_W - text_x - DIALOGUE_MARGIN
        lines = self._wrap_text(shown_text, max_w, 15)
        for i, line in enumerate(lines):
            col = TEXT_COL if speaker else NARRATOR_COL
            draw_text(surface, line, text_x, text_y + i * 22, col, 15)

        # ── Choices or continue prompt ──
        choices_y = max(text_y + len(lines) * 22 + 20, SCREEN_H - 220)

        if self.full_text_shown:
            if self.state.has_choices():
                self._draw_choices(surface, mx, my, choices_y)
            elif self.state.should_auto_advance():
                # Show "click to continue"
                draw_text(surface, "Click to continue...",
                          SCREEN_W // 2 - 80, SCREEN_H - 50, DIM_GOLD, 14)
            else:
                # End of conversation
                draw_text(surface, "Click to close.",
                          SCREEN_W // 2 - 60, SCREEN_H - 50, DIM_GOLD, 14)
        else:
            draw_text(surface, "Click to show all...",
                      SCREEN_W // 2 - 70, SCREEN_H - 50, DARK_GREY, 12)

    def _draw_choices(self, surface, mx, my, top_y):
        self.hover_choice = -1
        choices = self.state.get_choices()

        for i, choice in enumerate(choices):
            rect = pygame.Rect(DIALOGUE_MARGIN + 20, top_y + i * 48,
                               SCREEN_W - DIALOGUE_MARGIN * 2 - 40, 42)
            hover = rect.collidepoint(mx, my)
            if hover:
                self.hover_choice = i

            bg = CHOICE_HOVER if hover else CHOICE_BG
            border = CHOICE_HOVER_BORDER if hover else CHOICE_BORDER
            pygame.draw.rect(surface, bg, rect, border_radius=4)
            pygame.draw.rect(surface, border, rect, 2, border_radius=4)

            col = GOLD if hover else CREAM
            draw_text(surface, choice["text"], rect.x + 15, rect.y + 10, col, 14)

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

                # Check if the new node is the "fight" node
                if self.state.finished:
                    node = self.state.current_node
                    if node.get("on_enter"):
                        for act in node["on_enter"]:
                            if act.get("flag", "").endswith(".killed"):
                                self.result = "fight"
                    return "done"
                return None
        elif self.state.should_auto_advance():
            self.state.advance()
            self.displayed_chars = 0
            if self.state.finished:
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
