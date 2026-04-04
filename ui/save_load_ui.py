"""
Realm of Shadows — Save / Load Slot UI

Full-screen overlay showing 3 manual save slots + 1 autosave card.
Each card shows:
  - Hero (party[0]) name + level + race + class  (prominent)
  - Rest of party as compact pills
  - Furthest dungeon reached
  - Locations discovered count
  - Gold, key items, travel unlocks (horse/boat/carpet)
  - Save timestamp

mode = "save"  →  clicking a slot saves into it (with confirm on overwrite)
mode = "load"  →  clicking a slot loads it (autosave is load-only)
"""

import json
import os
from datetime import datetime

import pygame

from ui.renderer import (
    SCREEN_W, SCREEN_H,
    draw_text, draw_panel, draw_button, get_font,
    CREAM, GOLD, GREY, DARK_GREY, WHITE,
    PANEL_BG, PANEL_BORDER,
    HIGHLIGHT, DIM_GOLD, ORANGE, RED, GREEN,
)
from core.save_load import (
    save_game, load_game, list_saves, delete_save, SAVE_DIR,
)

# ── Canonical dungeon progression for "furthest location" ───────────────────
_PROGRESS_ORDER = [
    "goblin_warren", "spiders_nest", "abandoned_mine", "sunken_crypt",
    "ruins_ashenmoor", "valdris_spire", "pale_coast",
    "dragons_tooth", "windswept_isle",
]

# ── Colours ─────────────────────────────────────────────────────────────────
BG_COL       = (8, 6, 16)
CARD_BG      = (18, 15, 32)
CARD_BG_HOV  = (26, 22, 46)
CARD_BORDER  = (60, 52, 100)
CARD_HOV_BOR = HIGHLIGHT
CARD_EMPTY   = (12, 10, 22)
AUTOSAVE_BOR = (60, 80, 60)        # greenish tint for autosave card
HERO_COL     = CREAM
PARTY_COL    = (170, 160, 200)
META_COL     = (130, 122, 155)
KEY_COL      = DIM_GOLD
CONFIRM_BG   = (30, 10, 10)
CONFIRM_BOR  = (160, 40, 40)

SLOT_NAMES = ["save1", "save2", "save3", "save4", "save5"]  # 5 manual slots

CARD_W = 560
CARD_H = 128             # reduced to fit 5 slots on screen
CARD_GAP = 10
CARDS_TOTAL_H = 5 * CARD_H + 4 * CARD_GAP
AUTOSAVE_H = 72          # narrower card for autosave

# ── Helper ───────────────────────────────────────────────────────────────────

def _fmt_date(ts: str) -> str:
    """'2026-03-10T15:24:33' → 'Mar 10,  3:24 PM'."""
    try:
        dt = datetime.fromisoformat(ts)
        return dt.strftime("%b %d,  %I:%M %p").replace("  0", "   ")
    except Exception:
        return ts[:16]


def _furthest(discovered: list) -> str:
    try:
        from data.world_map import LOCATIONS
        for loc_id in reversed(_PROGRESS_ORDER):
            if loc_id in discovered:
                return LOCATIONS[loc_id]["name"]
        for loc_id in discovered:
            if loc_id in LOCATIONS:
                return LOCATIONS[loc_id]["name"]
    except Exception:
        pass
    return ""


def _travel_icons(travel: dict) -> str:
    icons = []
    if travel.get("has_horse"):   icons.append("Horse")
    if travel.get("has_boat"):    icons.append("Boat")
    if travel.get("has_carpet"):  icons.append("Carpet")
    return "  ".join(icons)


def _load_slot_data(slot_name: str) -> dict | None:
    """Return parsed save JSON or None if slot is empty/corrupt."""
    path = os.path.join(SAVE_DIR, f"{slot_name}.json")
    if not os.path.exists(path):
        return None
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return None


def _build_card_info(data: dict) -> dict:
    """Distil raw save JSON into display-ready fields."""
    party_raw = data.get("party", [])
    ws = data.get("world_state") or {}
    travel = ws.get("travel", {})
    meta = data.get("metadata", {})

    # Hero = party[0]
    hero = party_raw[0] if party_raw else {}
    hero_str = (
        f"{hero.get('name', '?')}   "
        f"L{hero.get('level', 1)} "
        f"{hero.get('race_name', 'Human')} "
        f"{hero.get('class_name', '?')}"
    )

    # Remaining party members as compact pills
    companions = []
    for p in party_raw[1:]:
        companions.append(
            f"{p.get('name','?')} L{p.get('level',1)} {p.get('class_name','?')}"
        )

    discovered = ws.get("discovered_locations", [])
    furthest   = _furthest(discovered)
    n_locs     = len(discovered)

    gold = meta.get("total_gold", sum(p.get("gold", 0) for p in party_raw))

    key_items = ws.get("key_items", [])
    key_str   = ", ".join(key_items[:3])
    if len(key_items) > 3:
        key_str += f" +{len(key_items)-3}"

    travel_str = _travel_icons(travel)
    timestamp  = _fmt_date(data.get("timestamp", ""))

    return {
        "hero":       hero_str,
        "companions": companions,
        "furthest":   furthest,
        "n_locs":     n_locs,
        "gold":       gold,
        "key_items":  key_str,
        "travel":     travel_str,
        "timestamp":  timestamp,
    }


# ── Main UI class ─────────────────────────────────────────────────────────────

class SaveLoadUI:
    """
    Full-screen save/load slot picker.

    mode: "save" | "load"
    result: None (open) | "cancelled" | ("saved", slot) | ("loaded", party, world_state)
    """

    def __init__(self, mode: str, party=None, world_state=None, dungeon_cache=None, dungeon_state=None):
        self.mode         = mode          # "save" or "load"
        self.party        = party         # current live party (for saving)
        self.world_state  = world_state
        self.dungeon_cache = dungeon_cache
        self.dungeon_state = dungeon_state  # active dungeon state (if saving inside dungeon)
        self.finished     = False
        self.result       = None

        # Slot data cache
        self._refresh_slots()

        # Hover / confirm state
        self._hover_slot  = None          # index 0-3 (3 = autosave)
        self._confirm_idx = None          # index awaiting overwrite confirm
        self._error_msg   = ""
        self._error_timer = 0

    # ── Public ───────────────────────────────────────────────────────────────

    def handle_event(self, event) -> str | None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._cancel()
        elif event.type == pygame.MOUSEMOTION:
            self._hover_slot = self._slot_at(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            # Confirm-overwrite modal
            if self._confirm_idx is not None:
                yes_r, no_r = self._confirm_buttons()
                if yes_r.collidepoint(mx, my):
                    self._do_save(self._confirm_idx)
                    self._confirm_idx = None
                elif no_r.collidepoint(mx, my):
                    self._confirm_idx = None
                return
            # Cancel button
            if self._cancel_rect().collidepoint(mx, my):
                self._cancel()
                return
            # Slot click
            idx = self._slot_at((mx, my))
            if idx is not None:
                self._on_slot_click(idx)
        return None

    def draw(self, surface, mx, my):
        # Dim background
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))

        title = "Save Game" if self.mode == "save" else "Load Game"
        draw_text(surface, title, SCREEN_W // 2 - get_font(26).size(title)[0] // 2,
                  28, GOLD, 26, bold=True)

        # Draw manual slot cards
        cx = (SCREEN_W - CARD_W) // 2
        start_y = 72
        for i, slot in enumerate(SLOT_NAMES):
            cy = start_y + i * (CARD_H + CARD_GAP)
            self._draw_slot_card(surface, i, slot, cx, cy, CARD_W, CARD_H)

        # Autosave card (index len(SLOT_NAMES), load-only)
        auto_y = start_y + len(SLOT_NAMES) * (CARD_H + CARD_GAP) + 8
        self._draw_autosave_card(surface, cx, auto_y, CARD_W, AUTOSAVE_H)

        # Cancel button
        cr = self._cancel_rect()
        draw_button(surface, cr, "Cancel",
                    hover=cr.collidepoint(mx, my), size=15)

        # Error toast
        if self._error_msg and self._error_timer > 0:
            self._error_timer -= 16
            err_font = get_font(14)
            ew = err_font.size(self._error_msg)[0] + 20
            ex = (SCREEN_W - ew) // 2
            ey = SCREEN_H - 70
            pygame.draw.rect(surface, (60, 10, 10), (ex, ey, ew, 28), border_radius=4)
            pygame.draw.rect(surface, RED, (ex, ey, ew, 28), 1, border_radius=4)
            draw_text(surface, self._error_msg, ex + 10, ey + 6, RED, 14)

        # Confirm-overwrite modal
        if self._confirm_idx is not None:
            self._draw_confirm(surface)

    # ── Layout helpers ────────────────────────────────────────────────────────

    def _card_rect(self, idx) -> pygame.Rect:
        cx = (SCREEN_W - CARD_W) // 2
        start_y = 72
        n = len(SLOT_NAMES)
        if idx < n:
            return pygame.Rect(cx, start_y + idx * (CARD_H + CARD_GAP), CARD_W, CARD_H)
        else:  # autosave
            auto_y = start_y + n * (CARD_H + CARD_GAP) + 8
            return pygame.Rect(cx, auto_y, CARD_W, AUTOSAVE_H)

    def _slot_at(self, pos) -> int | None:
        for i in range(len(SLOT_NAMES) + 1):  # +1 for autosave
            if self._card_rect(i).collidepoint(pos):
                return i
        return None

    def _cancel_rect(self) -> pygame.Rect:
        return pygame.Rect(SCREEN_W // 2 - 60, SCREEN_H - 44, 120, 34)

    def _confirm_buttons(self):
        cx = SCREEN_W // 2
        cy = SCREEN_H // 2 + 30
        yes = pygame.Rect(cx - 120, cy, 100, 36)
        no  = pygame.Rect(cx + 20,  cy, 100, 36)
        return yes, no

    # ── Drawing ───────────────────────────────────────────────────────────────

    def _draw_slot_card(self, surface, idx, slot_name, x, y, w, h):
        data  = self._slots[idx]
        hover = (self._hover_slot == idx)
        label = f"SAVE {idx + 1}"

        if data is None:
            # Empty slot
            rect = pygame.Rect(x, y, w, h)
            pygame.draw.rect(surface, CARD_EMPTY, rect, border_radius=6)
            border_col = CARD_HOV_BOR if hover else CARD_BORDER
            pygame.draw.rect(surface, border_col, rect, 2, border_radius=6)
            draw_text(surface, label, x + 16, y + 14, DIM_GOLD, 13, bold=True)
            empty_lbl = "— Empty —" if self.mode == "save" else "— No save found —"
            draw_text(surface, empty_lbl, x + w // 2 - get_font(16).size(empty_lbl)[0] // 2,
                      y + h // 2 - 10, GREY, 16)
            if self.mode == "save":
                draw_text(surface, "Click to save here", x + 16, y + h - 24, META_COL, 12)
        else:
            info = _build_card_info(data)
            bg   = CARD_BG_HOV if hover else CARD_BG
            rect = pygame.Rect(x, y, w, h)
            pygame.draw.rect(surface, bg, rect, border_radius=6)
            border_col = CARD_HOV_BOR if hover else CARD_BORDER
            pygame.draw.rect(surface, border_col, rect, 2, border_radius=6)

            # Slot label  +  timestamp (top row)
            draw_text(surface, label,            x + 16,       y + 10, DIM_GOLD, 12, bold=True)
            draw_text(surface, info["timestamp"], x + w - 160,  y + 10, META_COL, 12)

            # Thin divider
            pygame.draw.line(surface, CARD_BORDER,
                             (x + 12, y + 27), (x + w - 12, y + 27))

            # Hero line (prominent)
            draw_text(surface, info["hero"], x + 16, y + 33, HERO_COL, 15, bold=True, max_width=CARD_W - 170)

            # Companion pills — single line
            pill_y = y + 56
            self._draw_companions(surface, info["companions"], x + 16, pill_y, w - 32)

            # Thin divider before meta row
            pygame.draw.line(surface, CARD_BORDER,
                             (x + 12, y + 82), (x + w - 12, y + 82))

            # Meta row: locations · furthest
            loc_str = f"{info['n_locs']} locations explored"
            if info["furthest"]:
                loc_str += f"  ·  Last: {info['furthest']}"
            draw_text(surface, loc_str, x + 16, y + 89, META_COL, 12, max_width=CARD_W - 32)

            # Second meta row: gold · key items · travel
            row2_parts = []
            if info["gold"] > 0:
                row2_parts.append(f"Gold: {info['gold']}")
            if info["key_items"]:
                row2_parts.append(info["key_items"])
            row2 = "  ·  ".join(row2_parts)
            draw_text(surface, row2, x + 16, y + 106, KEY_COL, 11, max_width=CARD_W - 140)

            if info["travel"]:
                draw_text(surface, info["travel"], x + w - 120, y + 106, ORANGE, 11)

            # Action hint
            if self.mode == "save":
                hint = "Click to overwrite"
            else:
                hint = "Click to load"
            draw_text(surface, hint, x + 16, y + h - 14, META_COL, 10)

    def _draw_companions(self, surface, companions: list[str], x, y, max_w):
        """Draw companion pills, wrapping to a second line if needed."""
        if not companions:
            return
        font = get_font(13)
        PAD = 10
        GAP = 8
        cx = x
        cy = y
        for name in companions:
            tw = font.size(name)[0]
            pw = tw + PAD * 2
            if cx + pw > x + max_w and cx > x:
                cx  = x
                cy += 22
            pill = pygame.Rect(cx, cy, pw, 20)
            pygame.draw.rect(surface, (35, 28, 55), pill, border_radius=4)
            pygame.draw.rect(surface, CARD_BORDER, pill, 1, border_radius=4)
            draw_text(surface, name, cx + PAD, cy + 3, PARTY_COL, 13)
            cx += pw + GAP

    def _draw_autosave_card(self, surface, x, y, w, h):
        n     = len(SLOT_NAMES)
        data  = self._slots[n]
        hover = (self._hover_slot == n)
        label = "AUTOSAVE"

        rect = pygame.Rect(x, y, w, h)
        bg   = CARD_BG_HOV if hover else CARD_EMPTY
        pygame.draw.rect(surface, bg, rect, border_radius=6)
        border_col = CARD_HOV_BOR if hover else AUTOSAVE_BOR
        pygame.draw.rect(surface, border_col, rect, 2, border_radius=6)
        draw_text(surface, label, x + 16, y + 12, (100, 180, 100), 12, bold=True)

        if data is None:
            draw_text(surface, "— No autosave —",
                      x + w // 2 - get_font(14).size("— No autosave —")[0] // 2,
                      y + h // 2 - 8, GREY, 14)
        else:
            info = _build_card_info(data)
            draw_text(surface, info["timestamp"], x + w - 160, y + 12, META_COL, 12)

            hero_str = info["hero"]
            draw_text(surface, hero_str, x + 16, y + 34, HERO_COL, 15, bold=True)

            companions_short = "  ·  ".join(info["companions"][:3])
            if companions_short:
                draw_text(surface, companions_short, x + 16, y + 56, PARTY_COL, 12)

            loc_str = f"{info['n_locs']} locations"
            if info["furthest"]:
                loc_str += f"  ·  Last: {info['furthest']}"
            draw_text(surface, loc_str, x + 16, y + h - 22, META_COL, 12)

        # Load-only note
        if self.mode == "save":
            draw_text(surface, "Read-only (autosaves when you rest at an inn)",
                      x + w - 310, y + h - 22, META_COL, 11)
        else:
            if data:
                draw_text(surface, "Click to load", x + w - 110, y + h - 22, META_COL, 11)

    def _draw_confirm(self, surface):
        """Overwrite confirmation modal."""
        mw, mh = 420, 130
        mx_ = (SCREEN_W - mw) // 2
        my_ = (SCREEN_H - mh) // 2
        modal = pygame.Rect(mx_, my_, mw, mh)

        pygame.draw.rect(surface, CONFIRM_BG, modal, border_radius=8)
        pygame.draw.rect(surface, CONFIRM_BOR, modal, 2, border_radius=8)

        slot_n = self._confirm_idx + 1
        draw_text(surface, f"Overwrite Save Slot {slot_n}?",
                  mx_ + mw // 2 - get_font(18).size(f"Overwrite Save Slot {slot_n}?")[0] // 2,
                  my_ + 18, CREAM, 18, bold=True)
        draw_text(surface, "This will replace the existing save.",
                  mx_ + mw // 2 - get_font(13).size("This will replace the existing save.")[0] // 2,
                  my_ + 46, GREY, 13)

        yes_r, no_r = self._confirm_buttons()
        mx, my = pygame.mouse.get_pos()
        draw_button(surface, yes_r, "Overwrite",
                    hover=yes_r.collidepoint(mx, my), size=14)
        draw_button(surface, no_r, "Cancel",
                    hover=no_r.collidepoint(mx, my), size=14)

    # ── Actions ───────────────────────────────────────────────────────────────

    def _refresh_slots(self):
        """Re-read all save files from disk."""
        self._slots = [
            _load_slot_data(s) for s in SLOT_NAMES
        ] + [_load_slot_data("inn_autosave")]

    def _on_slot_click(self, idx: int):
        if self.mode == "save":
            if idx >= len(SLOT_NAMES):
                return  # autosave is read-only
            if self._slots[idx] is not None:
                self._confirm_idx = idx   # ask before overwriting
            else:
                self._do_save(idx)
        else:  # load
            if self._slots[idx] is None:
                return
            self._do_load(idx)

    def _do_save(self, idx: int):
        slot = SLOT_NAMES[idx]
        if not self.party:
            self._error_msg   = "Save failed: no active party."
            self._error_timer = 3000
            return
        try:
            ok, _path, msg = save_game(
                self.party,
                world_state=self.world_state,
                slot_name=slot,
                dungeon_cache=getattr(self, "dungeon_cache", None),
                dungeon_state=getattr(self, "dungeon_state", None),
            )
        except Exception as _e:
            ok  = False
            msg = f"Save failed: {_e}"
        if ok:
            self.result   = ("saved", slot)
            self.finished = True
        else:
            self._error_msg   = msg
            self._error_timer = 3000

    def _do_load(self, idx: int):
        slot = SLOT_NAMES[idx] if idx < len(SLOT_NAMES) else "inn_autosave"
        ok, party, world_state, msg, dungeon_explored, dungeon_position = load_game(slot)
        if ok:
            self.result   = ("loaded", party, world_state, dungeon_explored, dungeon_position)
            self.finished = True
        else:
            self._error_msg   = msg
            self._error_timer = 3000

    def _cancel(self):
        self.result   = "cancelled"
        self.finished = True
