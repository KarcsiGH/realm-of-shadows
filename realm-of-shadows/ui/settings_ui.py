"""
Realm of Shadows — Settings UI
Volume controls: Master, SFX, Music, Ambient.
All sliders give live audio feedback.  Changes persist to settings.json on Close.
"""
import pygame
from ui.renderer import (
    SCREEN_W, SCREEN_H, GOLD, CREAM, GREY, DARK_GREY, PANEL_BORDER,
    draw_text, draw_panel, draw_button, get_font,
)

# ──────────────────────────────────────────────────────────────
#  Layout
# ──────────────────────────────────────────────────────────────
PANEL_W  = 520
PANEL_H  = 540
PANEL_X  = SCREEN_W  // 2 - PANEL_W // 2
PANEL_Y  = SCREEN_H  // 2 - PANEL_H // 2

SLIDER_X       = PANEL_X + 200
SLIDER_W       = 240
SLIDER_H       = 14
SLIDER_Y_START = PANEL_Y + 100
SLIDER_GAP     = 72

LABEL_X    = PANEL_X + 30
VALUE_X    = PANEL_X + PANEL_W - 70

CLOSE_RECT  = pygame.Rect(PANEL_X + PANEL_W // 2 - 80, PANEL_Y + PANEL_H - 56, 160, 38)
RESET_DISPLAY_NOTE = "(takes effect on restart)"
RESET_RECT  = pygame.Rect(PANEL_X + 30, PANEL_Y + PANEL_H - 56, 110, 38)

# Default volumes (mirroring sound.py defaults)
_DEFAULTS = {
    "Master":  0.6,
    "SFX":     0.7,
    "Music":   0.35,
    "Ambient": 0.25,
}

# ──────────────────────────────────────────────────────────────
#  Colours
# ──────────────────────────────────────────────────────────────
TRACK_BG    = (30, 26, 45)
TRACK_FILL  = (100, 70, 160)
KNOB_IDLE   = (200, 180, 240)
KNOB_HOVER  = (255, 240, 120)
KNOB_DRAG   = (255, 200, 60)


class SettingsUI:
    """
    Volume settings panel with four sliders.
    Call draw(surface, mx, my) each frame.
    Call handle_event(event) for mouse input; returns "close" when done.
    Changes are saved to settings.json when the panel closes.
    """

    def __init__(self):
        import core.sound as sfx
        self._sliders = [
            ("Master",  sfx.get_master_volume()),
            ("SFX",     sfx.get_sfx_volume()),
            ("Music",   sfx.get_music_volume()),
            ("Ambient", sfx.get_ambient_volume()),
        ]
        self._dragging = None   # index of slider being dragged
        self.finished  = False
        self._display_mode = sfx.get_display_mode()
        self._display_options = ["fullscreen", "1440x900", "1280x800"]
        self._display_labels  = ["Fullscreen (native)", "Windowed 1440×900", "Windowed 1280×800"]
        self._display_changed = False

    # ── helpers ───────────────────────────────────────────────

    def _slider_rect(self, idx):
        y = SLIDER_Y_START + idx * SLIDER_GAP
        return pygame.Rect(SLIDER_X, y, SLIDER_W, SLIDER_H)

    def _knob_rect(self, idx):
        val = self._sliders[idx][1]
        r   = self._slider_rect(idx)
        kx  = r.x + int(val * r.w)
        ky  = r.centery
        return pygame.Rect(kx - 10, ky - 10, 20, 20)

    def _set_value(self, idx, mx):
        import core.sound as sfx
        r   = self._slider_rect(idx)
        val = max(0.0, min(1.0, (mx - r.x) / r.w))
        name = self._sliders[idx][0]
        self._sliders[idx] = (name, val)
        # Live update
        if name == "Master":  sfx.set_master_volume(val)
        elif name == "SFX":   sfx.set_sfx_volume(val)
        elif name == "Music": sfx.set_music_volume(val)
        else:                 sfx.set_ambient_volume(val)

    def _display_btn_rect(self, idx):
        """Rect for display mode button at index idx."""
        base_y = SLIDER_Y_START + 4 * SLIDER_GAP + 20
        btn_w = (PANEL_W - 60) // 3
        return pygame.Rect(PANEL_X + 30 + idx * (btn_w + 8), base_y, btn_w, 32)

    def _save_and_close(self):
        import core.sound as sfx
        sfx.save_settings()
        self.finished = True

    # ── public ────────────────────────────────────────────────

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            # Close button
            if CLOSE_RECT.collidepoint(mx, my):
                self._save_and_close()
                return "close"
            # Reset button
            if RESET_RECT.collidepoint(mx, my):
                import core.sound as sfx
                self._sliders = [(k, v) for k, v in _DEFAULTS.items()]
                sfx.set_master_volume(_DEFAULTS["Master"])
                sfx.set_sfx_volume(_DEFAULTS["SFX"])
                sfx.set_music_volume(_DEFAULTS["Music"])
                sfx.set_ambient_volume(_DEFAULTS["Ambient"])
                return None
            # Display mode buttons
            for di, opt in enumerate(self._display_options):
                btn = self._display_btn_rect(di)
                if btn.collidepoint(mx, my):
                    import core.sound as sfx
                    self._display_mode = opt
                    sfx.set_display_mode(opt)
                    self._display_changed = True
                    return None

            # Start dragging a knob or clicking the track
            for i in range(len(self._sliders)):
                r = self._slider_rect(i)
                k = self._knob_rect(i)
                if k.collidepoint(mx, my) or r.collidepoint(mx, my):
                    self._dragging = i
                    self._set_value(i, mx)
                    return None

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self._dragging = None

        elif event.type == pygame.MOUSEMOTION:
            if self._dragging is not None:
                self._set_value(self._dragging, event.pos[0])

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._save_and_close()
                return "close"

        return None

    def draw(self, surface, mx, my):
        # Dim the screen behind the panel
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        surface.blit(overlay, (0, 0))

        # Panel background
        panel_rect = pygame.Rect(PANEL_X, PANEL_Y, PANEL_W, PANEL_H)
        draw_panel(surface, panel_rect, border_color=(120, 90, 180))

        # Title
        draw_text(surface, "SETTINGS", PANEL_X + PANEL_W // 2 - 62,
                  PANEL_Y + 22, GOLD, 26, bold=True)
        draw_text(surface, "Volume Controls", PANEL_X + PANEL_W // 2 - 64,
                  PANEL_Y + 56, GREY, 15)

        # Sliders
        for i, (name, val) in enumerate(self._sliders):
            r    = self._slider_rect(i)
            k    = self._knob_rect(i)
            ly   = r.centery - 8
            pct  = int(val * 100)

            # Label
            draw_text(surface, name, LABEL_X, ly, CREAM, 16, bold=True)

            # Subtitle hint
            hints = {
                "Master":  "overall volume",
                "SFX":     "combat & interaction sounds",
                "Music":   "background music",
                "Ambient": "dungeon atmosphere",
            }
            draw_text(surface, hints.get(name, ""), LABEL_X, ly + 18,
                      DARK_GREY, 11)

            # Track background
            pygame.draw.rect(surface, TRACK_BG, r, border_radius=7)

            # Track fill
            fill_r = pygame.Rect(r.x, r.y, int(val * r.w), r.h)
            if fill_r.w > 0:
                pygame.draw.rect(surface, TRACK_FILL, fill_r, border_radius=7)

            # Track border
            pygame.draw.rect(surface, PANEL_BORDER, r, 1, border_radius=7)

            # Knob
            dragging = self._dragging == i
            hovering = k.collidepoint(mx, my)
            knob_col = KNOB_DRAG if dragging else (KNOB_HOVER if hovering else KNOB_IDLE)
            pygame.draw.circle(surface, knob_col,
                               (k.centerx, k.centery), 10)
            pygame.draw.circle(surface, PANEL_BORDER,
                               (k.centerx, k.centery), 10, 2)

            # Value label
            draw_text(surface, f"{pct}%", VALUE_X, ly, CREAM, 15, bold=True)

        # ── Display Mode Section ──
        disp_y = SLIDER_Y_START + 4 * SLIDER_GAP + 5
        draw_text(surface, "Display Mode", LABEL_X, disp_y, CREAM, 14, bold=True)
        if self._display_changed:
            draw_text(surface, "(restart required)", LABEL_X + 150, disp_y + 2, (180, 130, 80), 11)

        for di, (opt, lbl) in enumerate(zip(self._display_options, self._display_labels)):
            btn = self._display_btn_rect(di)
            is_active = (self._display_mode == opt)
            is_hover  = btn.collidepoint(mx, my)
            bg = (60, 50, 90) if is_active else ((40, 35, 60) if is_hover else (25, 20, 42))
            border = GOLD if is_active else ((140, 110, 200) if is_hover else PANEL_BORDER)
            pygame.draw.rect(surface, bg, btn, border_radius=4)
            pygame.draw.rect(surface, border, btn, 2 if is_active else 1, border_radius=4)
            txt_col = GOLD if is_active else (CREAM if is_hover else GREY)
            tw = get_font(12).size(lbl)[0]
            draw_text(surface, lbl, btn.x + (btn.w - tw) // 2, btn.y + 9, txt_col, 12,
                      bold=is_active)

        # Buttons
        draw_button(surface, RESET_RECT, "Reset",
                    hover=RESET_RECT.collidepoint(mx, my), size=14)
        draw_button(surface, CLOSE_RECT, "Save & Close",
                    hover=CLOSE_RECT.collidepoint(mx, my), size=15)

        draw_text(surface, "ESC to close",
                  PANEL_X + PANEL_W // 2 - 42, PANEL_Y + PANEL_H - 14,
                  DARK_GREY, 11)
