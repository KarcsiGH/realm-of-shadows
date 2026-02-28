"""
Realm of Shadows — UI Rendering Helpers
Retro pixel-art RPG styling.
"""
import pygame

# ── Colors ────────────────────────────────────────────────────
BLACK       = (0, 0, 0)
WHITE       = (255, 255, 255)
GREY        = (160, 160, 160)
DARK_GREY   = (80, 80, 80)
DARKER_GREY = (40, 40, 40)
BG_COLOR    = (12, 10, 24)
PANEL_BG    = (20, 18, 36)
PANEL_BORDER= (70, 60, 110)
GOLD        = (255, 215, 0)
DIM_GOLD    = (180, 150, 40)
CREAM       = (240, 230, 200)
HIGHLIGHT   = (100, 180, 255)
DIM_BLUE    = (60, 80, 140)
RED         = (220, 60, 60)
GREEN       = (60, 200, 80)
DIM_GREEN   = (40, 120, 50)
PURPLE      = (160, 100, 220)
ORANGE      = (220, 150, 40)
HEAL_COL    = (80, 255, 180)
RUMOR_COL   = (180, 160, 220)
BUY_COL     = (80, 220, 120)
SELL_COL    = (220, 180, 80)

FIT_COLORS = {
    "Natural Fit": GREEN,
    "Good Fit": HIGHLIGHT,
    "Unusual Choice": ORANGE,
}

# ── Screen Settings ───────────────────────────────────────────
SCREEN_W = 1280
SCREEN_H = 960

# ── Font Cache ────────────────────────────────────────────────
_font_cache = {}

def get_font(size, bold=False):
    key = (size, bold)
    if key not in _font_cache:
        font = pygame.font.SysFont("consolas,courier,monospace", size, bold=bold)
        _font_cache[key] = font
    return _font_cache[key]


# ── Text Rendering ────────────────────────────────────────────

def draw_text(surface, text, x, y, color=WHITE, size=16, bold=False, max_width=None):
    """Draw text, optionally word-wrapped. Returns the total height used."""
    font = get_font(size, bold)
    if max_width is None:
        rendered = font.render(text, True, color)
        surface.blit(rendered, (x, y))
        return rendered.get_height()
    else:
        return draw_wrapped_text(surface, text, x, y, max_width, color, font)


def draw_wrapped_text(surface, text, x, y, max_width, color, font):
    """Word-wrap text within max_width. Returns total height."""
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test = current_line + (" " if current_line else "") + word
        if font.size(test)[0] <= max_width:
            current_line = test
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    total_h = 0
    line_h = font.get_linesize()
    for line in lines:
        rendered = font.render(line, True, color)
        surface.blit(rendered, (x, y + total_h))
        total_h += line_h
    return total_h


# ── Panels & Boxes ────────────────────────────────────────────

def draw_panel(surface, rect, border_color=PANEL_BORDER, bg_color=PANEL_BG, border_width=2):
    """Draw a bordered panel/box."""
    pygame.draw.rect(surface, bg_color, rect)
    pygame.draw.rect(surface, border_color, rect, border_width)


def draw_button(surface, rect, text, color=CREAM, bg=DARKER_GREY,
                border=PANEL_BORDER, hover=False, size=16):
    """Draw a clickable button. Returns the rect for hit testing."""
    bg_actual = (60, 50, 90) if hover else bg
    pygame.draw.rect(surface, bg_actual, rect)
    pygame.draw.rect(surface, border if not hover else HIGHLIGHT, rect, 2)
    font = get_font(size)
    rendered = font.render(text, True, GOLD if hover else color)
    tx = rect.x + (rect.width - rendered.get_width()) // 2
    ty = rect.y + (rect.height - rendered.get_height()) // 2
    surface.blit(rendered, (tx, ty))
    return rect


# ── Stat Bar ──────────────────────────────────────────────────

def draw_stat_bar(surface, x, y, label, value, max_val=30, width=200, color=HIGHLIGHT):
    """Draw a labeled stat bar."""
    font = get_font(14)
    # Label
    lbl = font.render(f"{label}:", True, CREAM)
    surface.blit(lbl, (x, y))
    # Value
    val = font.render(str(value), True, GOLD)
    surface.blit(val, (x + 50, y))
    # Bar background
    bar_x = x + 80
    bar_h = 14
    pygame.draw.rect(surface, DARKER_GREY, (bar_x, y + 2, width, bar_h))
    # Bar fill
    fill_w = max(0, min(width, int((value / max_val) * width)))
    pygame.draw.rect(surface, color, (bar_x, y + 2, fill_w, bar_h))
    pygame.draw.rect(surface, PANEL_BORDER, (bar_x, y + 2, width, bar_h), 1)


# ── Scrollable Text Choices ───────────────────────────────────

class ChoiceList:
    """A scrollable list of clickable choices."""

    def __init__(self, x, y, width, max_visible=4):
        self.x = x
        self.y = y
        self.width = width
        self.max_visible = max_visible
        self.choices = []     # list of dicts with 'title', 'text', and arbitrary data
        self.scroll = 0
        self.hover_idx = -1
        self.selected_idx = -1
        self.item_height = 80  # will be computed

    def set_choices(self, choices):
        self.choices = choices
        self.scroll = 0
        self.hover_idx = -1
        self.selected_idx = -1

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # scroll up
                self.scroll = max(0, self.scroll - 1)
            elif event.button == 5:  # scroll down
                self.scroll = min(max(0, len(self.choices) - self.max_visible), self.scroll + 1)
            elif event.button == 1:
                if self.hover_idx >= 0:
                    self.selected_idx = self.hover_idx
                    return self.choices[self.selected_idx]
        return None

    def update_hover(self, mx, my):
        self.hover_idx = -1
        for i in range(self.max_visible):
            idx = self.scroll + i
            if idx >= len(self.choices):
                break
            rect = pygame.Rect(self.x, self.y + i * self.item_height, self.width, self.item_height - 4)
            if rect.collidepoint(mx, my):
                self.hover_idx = idx

    def draw(self, surface):
        for i in range(self.max_visible):
            idx = self.scroll + i
            if idx >= len(self.choices):
                break
            choice = self.choices[idx]
            rect = pygame.Rect(self.x, self.y + i * self.item_height,
                               self.width, self.item_height - 4)
            is_hover = (idx == self.hover_idx)
            is_selected = (idx == self.selected_idx)

            bg = (50, 40, 80) if is_hover else (30, 25, 50) if is_selected else PANEL_BG
            border = GOLD if is_selected else HIGHLIGHT if is_hover else PANEL_BORDER

            draw_panel(surface, rect, border_color=border, bg_color=bg)

            # Title
            draw_text(surface, choice["title"], rect.x + 10, rect.y + 6,
                      color=GOLD if is_hover or is_selected else CREAM, size=16, bold=True)
            # Preview text (truncated)
            preview = choice.get("text", "")
            if len(preview) > 90:
                preview = preview[:87] + "..."
            draw_text(surface, preview, rect.x + 10, rect.y + 28,
                      color=GREY, size=13, max_width=self.width - 20)

        # Scroll indicators
        if self.scroll > 0:
            draw_text(surface, "^ scroll up ^", self.x + self.width // 2 - 50,
                      self.y - 18, DIM_GOLD, 12)
        if self.scroll + self.max_visible < len(self.choices):
            bottom_y = self.y + self.max_visible * self.item_height
            draw_text(surface, "v scroll down v", self.x + self.width // 2 - 55,
                      bottom_y, DIM_GOLD, 12)


# ── Class Icons ───────────────────────────────────────────────
# Colored geometric symbols drawn with pygame primitives.
# Each class has a distinct shape so they're readable at small sizes.

def draw_class_icon(surface, class_name, cx, cy, size=18):
    """
    Draw a colored geometric class icon centred at (cx, cy).
    size is the bounding box half-width (icon fits in size*2 x size*2).

    Shapes:
      Fighter  → crossed swords (two diagonal lines + crossguard)
      Mage     → 6-point star
      Cleric   → bold cross
      Thief    → downward dagger
      Ranger   → leaf / arrowhead
      Monk     → circle with inner ring
    """
    from core.classes import CLASSES
    color = CLASSES.get(class_name, {}).get("color", (160, 160, 160))
    dim   = tuple(max(0, c - 60) for c in color)   # darker shadow tint
    s = int(size * 0.85)   # inner draw radius

    if class_name == "Fighter":
        # Two crossed diagonal lines (swords) with tiny crossguards
        pygame.draw.line(surface, color,  (cx - s, cy - s), (cx + s, cy + s), 3)
        pygame.draw.line(surface, color,  (cx + s, cy - s), (cx - s, cy + s), 3)
        # Crossguards
        g = s // 2
        pygame.draw.line(surface, dim, (cx - g, cy), (cx + g, cy), 2)
        pygame.draw.line(surface, dim, (cx, cy - g), (cx, cy + g), 2)

    elif class_name == "Mage":
        # 6-point star (two overlapping triangles)
        import math
        pts_up   = [(cx + s*math.cos(math.radians(a - 90)),
                     cy + s*math.sin(math.radians(a - 90)))
                    for a in (0, 120, 240)]
        pts_down = [(cx + s*math.cos(math.radians(a + 90)),
                     cy + s*math.sin(math.radians(a + 90)))
                    for a in (0, 120, 240)]
        pygame.draw.polygon(surface, dim,   pts_up,   0)
        pygame.draw.polygon(surface, color, pts_up,   2)
        pygame.draw.polygon(surface, dim,   pts_down, 0)
        pygame.draw.polygon(surface, color, pts_down, 2)

    elif class_name == "Cleric":
        # Bold cross
        t = max(2, s // 3)   # arm thickness
        pygame.draw.rect(surface, color, (cx - t, cy - s, t*2, s*2))
        pygame.draw.rect(surface, color, (cx - s, cy - t, s*2, t*2))
        # Bright centre dot
        pygame.draw.circle(surface, (255, 255, 200), (cx, cy), t - 1)

    elif class_name == "Thief":
        # Downward-pointing dagger (triangle blade + small hilt)
        tip = (cx, cy + s)
        blade = [(cx - s//3, cy - s//2), tip, (cx + s//3, cy - s//2)]
        pygame.draw.polygon(surface, dim, blade, 0)
        pygame.draw.polygon(surface, color, blade, 2)
        # Hilt crossbar
        pygame.draw.line(surface, color, (cx - s//2, cy - s//2), (cx + s//2, cy - s//2), 2)
        # Pommel
        pygame.draw.circle(surface, color, (cx, cy - s), s//5)

    elif class_name == "Ranger":
        # Upward arrowhead / leaf
        tip  = (cx,       cy - s)
        left = (cx - s,   cy + s//2)
        right= (cx + s,   cy + s//2)
        notch= (cx,       cy + s//4)
        pts  = [tip, right, notch, left]
        pygame.draw.polygon(surface, dim,   pts, 0)
        pygame.draw.polygon(surface, color, pts, 2)
        # Centre vein
        pygame.draw.line(surface, color, (cx, cy - s + 2), (cx, cy + s//4), 1)

    elif class_name == "Monk":
        # Outer circle + inner ring + centre dot  (energy / ki)
        pygame.draw.circle(surface, dim,   (cx, cy), s,       0)
        pygame.draw.circle(surface, color, (cx, cy), s,       2)
        pygame.draw.circle(surface, color, (cx, cy), s*2//3,  1)
        pygame.draw.circle(surface, color, (cx, cy), s//4,    0)

    else:
        # Generic: filled diamond
        pts = [(cx, cy - s), (cx + s, cy), (cx, cy + s), (cx - s, cy)]
        pygame.draw.polygon(surface, dim,   pts, 0)
        pygame.draw.polygon(surface, color, pts, 2)


def draw_class_badge(surface, class_name, x, y, size=18):
    """
    Draw a small circular badge with a class icon inside.
    Top-left corner at (x, y).  Total footprint: (size*2+4) x (size*2+4).
    """
    from core.classes import CLASSES
    color = CLASSES.get(class_name, {}).get("color", (100, 100, 100))
    r     = size + 2
    cx, cy = x + r, y + r
    pygame.draw.circle(surface, (20, 16, 36),  (cx, cy), r)        # bg
    pygame.draw.circle(surface, color,         (cx, cy), r, 2)     # border
    draw_class_icon(surface, class_name, cx, cy, size)
