#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════╗
║           REALM OF SHADOWS                            ║
║   Advanced Class System Party-Based RPG               ║
║   Milestone 1: Character Creation & Life Path         ║
╚═══════════════════════════════════════════════════════╝

Run:  python3 main.py
"""
import sys, os, random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pygame
pygame.init()

from ui.renderer import *
from core.classes import STAT_NAMES, STAT_FULL_NAMES, CLASSES, CLASS_ORDER, get_all_resources
from core.character import Character
from data.life_path_events import (
    ALL_EVENTS_BY_SLOT, SLOT_TITLES, PHASE_FOR_SLOT, get_available_events,
)
from core.combat_engine import CombatState
from ui.combat_ui import CombatUI
from ui.post_combat_ui import PostCombatUI
from ui.inventory_ui import InventoryUI

FPS = 60
PARTY_SIZE = 6

# States
S_TITLE       = 0
S_MODE        = 1
S_NAME        = 2
S_LIFEPATH    = 3
S_RANDOM      = 4
S_CLASSSELECT = 5
S_SUMMARY     = 6
S_PARTY       = 7
S_COMBAT      = 8
S_POST_COMBAT = 9
S_INVENTORY   = 10


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Realm of Shadows")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = S_TITLE
        self.party = []
        self.current_char = None
        self.char_index = 0
        self.slot = 1
        self.history = []
        self.name_text = ""
        self.blink = 0
        self.timer = 0
        self.scroll = 0
        self.hover = -1
        self.choices = []
        self.random_evt = None
        self.random_ok = False
        self.class_choices = []
        self.class_hover = -1
        self.party_scroll = 0
        self.quick = False
        self.fade = 255
        self.title_t = 0
        # Combat
        self.combat_state = None
        self.combat_ui = None
        self.enemy_turn_delay = 0
        # Post-combat
        self.post_combat_ui = None
        # Inventory
        self.inventory_ui = None
        # Debug
        self.debug_mode = False
        self.debug_encounter = "tutorial"
        self.debug_enc_hover = -1

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS)
            self.title_t += dt
            self.blink += dt
            self.timer += dt
            mx, my = pygame.mouse.get_pos()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
                    return
                self.on_event(e, mx, my)
            self.screen.fill(BG_COLOR)
            self.draw_state(mx, my)
            # Fade
            if self.fade > 0:
                s = pygame.Surface((SCREEN_W, SCREEN_H)); s.fill(BLACK)
                s.set_alpha(self.fade); self.screen.blit(s, (0,0))
                self.fade = max(0, self.fade - 10)
            pygame.display.flip()
        pygame.quit()

    def go(self, state):
        self.state = state
        self.fade = 120
        self.timer = 0

    # ══════════════════════════════════════════════════════════
    #  EVENT HANDLING
    # ══════════════════════════════════════════════════════════

    def on_event(self, e, mx, my):
        if self.state == S_TITLE:
            if e.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                self.go(S_MODE)

        elif self.state == S_MODE:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                # Life Path button
                r1 = pygame.Rect(SCREEN_W//2 - 220, 350, 440, 60)
                r2 = pygame.Rect(SCREEN_W//2 - 220, 430, 440, 60)
                if r1.collidepoint(mx, my):
                    self.quick = False
                    self.new_char()
                    self.go(S_NAME)
                elif r2.collidepoint(mx, my):
                    self.quick = True
                    self.new_char()
                    self.go(S_NAME)

        elif self.state == S_NAME:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN and self.name_text.strip():
                    self.current_char.name = self.name_text.strip()
                    if self.quick:
                        self.setup_class_choices()
                        self.go(S_CLASSSELECT)
                    else:
                        self.slot = 1
                        self.history = []
                        self.setup_slot_choices()
                        self.go(S_LIFEPATH)
                elif e.key == pygame.K_BACKSPACE:
                    self.name_text = self.name_text[:-1]
                elif e.key == pygame.K_ESCAPE:
                    self.go(S_MODE)
                elif len(self.name_text) < 20 and e.unicode.isprintable():
                    self.name_text += e.unicode

        elif self.state == S_LIFEPATH:
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 4:
                    self.scroll = max(0, self.scroll - 1)
                elif e.button == 5:
                    max_scroll = max(0, len(self.choices) - 4)
                    self.scroll = min(max_scroll, self.scroll + 1)
                elif e.button == 1 and self.hover >= 0:
                    self.pick_event(self.choices[self.hover])

        elif self.state == S_RANDOM:
            if (e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.KEYDOWN) and self.timer > 1500:
                self.advance_slot()

        elif self.state == S_CLASSSELECT:
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 4:
                    self.scroll = max(0, self.scroll - 1)
                elif e.button == 5:
                    max_scroll = max(0, len(self.class_choices) - 6)
                    self.scroll = min(max_scroll, self.scroll + 1)
                elif e.button == 1 and self.class_hover >= 0:
                    cn = self.class_choices[self.class_hover][0]
                    if self.quick:
                        self.current_char.quick_roll(cn)
                    else:
                        self.current_char.finalize_with_class(cn)
                    self.go(S_SUMMARY)

        elif self.state == S_SUMMARY:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                r_acc = pygame.Rect(SCREEN_W//2 - 230, SCREEN_H - 70, 200, 45)
                r_redo = pygame.Rect(SCREEN_W//2 + 30, SCREEN_H - 70, 200, 45)
                if r_acc.collidepoint(mx, my):
                    self.party.append(self.current_char)
                    self.char_index += 1
                    if self.char_index >= PARTY_SIZE:
                        self.party_scroll = 0
                        self.go(S_PARTY)
                    else:
                        self.go(S_MODE)
                elif r_redo.collidepoint(mx, my):
                    self.go(S_MODE)

        elif self.state == S_PARTY:
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 4:
                    self.party_scroll = max(0, self.party_scroll - 1)
                elif e.button == 5:
                    self.party_scroll = min(max(0, len(self.party) - 3), self.party_scroll + 1)
                elif e.button == 1:
                    # Inventory button
                    inv_btn = pygame.Rect(SCREEN_W - 200, 40, 180, 40)
                    if inv_btn.collidepoint(mx, my) and self.party:
                        self.inventory_ui = InventoryUI(self.party)
                        self.go(S_INVENTORY)
                        return
                    if self.debug_mode:
                        # Check encounter buttons
                        from data.enemies import ENCOUNTERS
                        enc_keys = list(ENCOUNTERS.keys())
                        for i, key in enumerate(enc_keys):
                            bx = 40 + (i % 3) * 220
                            by = SCREEN_H - 180 + (i // 3) * 50
                            btn_rect = pygame.Rect(bx, by, 210, 42)
                            if btn_rect.collidepoint(mx, my):
                                self.start_combat(key)
                                return
                    else:
                        r = pygame.Rect(SCREEN_W//2 - 150, SCREEN_H - 65, 300, 45)
                        if r.collidepoint(mx, my):
                            self.start_combat("tutorial")

        elif self.state == S_INVENTORY:
            # Pass keyboard events (ESC)
            if e.type == pygame.KEYDOWN:
                result = self.inventory_ui.handle_event(e)
                if result == "back":
                    self.go(S_PARTY)
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button in (1, 3):  # left or right click
                    result = self.inventory_ui.handle_click(mx, my, button=e.button)
                    if result == "back":
                        self.go(S_PARTY)
                elif e.button == 4:
                    self.inventory_ui.handle_scroll(-1)
                elif e.button == 5:
                    self.inventory_ui.handle_scroll(1)

        elif self.state == S_COMBAT:
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    action = self.combat_ui.handle_click(mx, my)
                    if action:
                        self.process_combat_action(action)
                elif e.button == 4:
                    self.combat_ui.handle_scroll(-1)
                elif e.button == 5:
                    self.combat_ui.handle_scroll(1)

        elif self.state == S_POST_COMBAT:
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    result = self.post_combat_ui.handle_click(mx, my)
                    if result == "continue":
                        self.party_scroll = 0
                        # Heal party for next fight
                        for char in self.party:
                            char.resources = get_all_resources(
                                char.class_name, char.stats, char.level
                            )
                        self.go(S_PARTY)
                elif e.button == 4:
                    self.post_combat_ui.handle_scroll(-1)
                elif e.button == 5:
                    self.post_combat_ui.handle_scroll(1)
                    self.combat_ui.handle_scroll(1)

    # ══════════════════════════════════════════════════════════
    #  LOGIC
    # ══════════════════════════════════════════════════════════

    def new_char(self):
        self.current_char = Character()
        self.current_char.quick_rolled = self.quick
        self.name_text = ""
        self.history = []

    def setup_slot_choices(self):
        events = get_available_events(self.slot, self.history)
        self.choices = events
        self.scroll = 0
        self.hover = -1

    def pick_event(self, event):
        # Apply stats
        self.current_char.apply_stat_bonus(event.get("stats", {}))
        self.current_char.backstory_parts.append(event.get("backstory", ""))
        self.history.append(event)

        # Check for random outcome
        rand = event.get("random")
        if rand:
            success = random.random() < rand["chance"]
            outcome = rand["success"] if success else rand["fail"]
            self.current_char.apply_stat_bonus(outcome.get("stats", {}))
            if outcome.get("backstory"):
                self.current_char.backstory_parts.append(outcome["backstory"])
            self.random_evt = event
            self.random_ok = success
            self.go(S_RANDOM)
            return

        self.advance_slot()

    def advance_slot(self):
        self.slot += 1
        if self.slot > 9:
            self.setup_class_choices()
            self.go(S_CLASSSELECT)
        else:
            self.setup_slot_choices()
            self.go(S_LIFEPATH)

    def setup_class_choices(self):
        if not self.quick:
            fits = self.current_char.get_class_recommendations()
        else:
            fits = [(cn, "Available", 0) for cn in CLASS_ORDER]
        self.class_choices = fits
        self.scroll = 0
        self.class_hover = -1

    # ══════════════════════════════════════════════════════════
    #  DRAWING
    # ══════════════════════════════════════════════════════════

    def draw_state(self, mx, my):
        if self.state == S_TITLE:      self.draw_title()
        elif self.state == S_MODE:     self.draw_mode(mx, my)
        elif self.state == S_NAME:     self.draw_name()
        elif self.state == S_LIFEPATH: self.draw_lifepath(mx, my)
        elif self.state == S_RANDOM:   self.draw_random()
        elif self.state == S_CLASSSELECT: self.draw_class(mx, my)
        elif self.state == S_SUMMARY:  self.draw_summary(mx, my)
        elif self.state == S_PARTY:    self.draw_party(mx, my)
        elif self.state == S_COMBAT:   self.draw_combat(mx, my)
        elif self.state == S_POST_COMBAT: self.draw_post_combat(mx, my)
        elif self.state == S_INVENTORY: self.draw_inventory(mx, my)

    # ── Title Screen ──────────────────────────────────────────

    def draw_title(self):
        # Gradient atmosphere
        for i in range(40):
            c = max(0, 30 - i)
            s = pygame.Surface((SCREEN_W, 10)); s.fill((c, c//3, c*2))
            s.set_alpha(80); self.screen.blit(s, (0, SCREEN_H//2 - 200 + i*10))

        pulse = abs((self.title_t % 3000) - 1500) / 1500.0
        col = (int(200 + 55*pulse), int(180 + 35*pulse), 0)

        draw_text(self.screen, "REALM", SCREEN_W//2 - 120, SCREEN_H//2 - 80,
                  col, 48, bold=True)
        draw_text(self.screen, "of", SCREEN_W//2 - 22, SCREEN_H//2 - 25,
                  GREY, 24)
        draw_text(self.screen, "SHADOWS", SCREEN_W//2 - 150, SCREEN_H//2 + 10,
                  col, 48, bold=True)

        if (self.title_t // 800) % 2 == 0:
            draw_text(self.screen, "Press any key to begin", SCREEN_W//2 - 130,
                      SCREEN_H//2 + 120, DIM_GOLD, 16)

        draw_text(self.screen, "An Advanced Class System RPG", SCREEN_W//2 - 160,
                  SCREEN_H - 60, DARK_GREY, 14)

    # ── Choose Mode ───────────────────────────────────────────

    def draw_mode(self, mx, my):
        draw_text(self.screen, f"Character {self.char_index + 1} of {PARTY_SIZE}",
                  SCREEN_W//2 - 100, 40, GOLD, 20, bold=True)

        # Existing party
        if self.party:
            y = 80
            for c in self.party:
                cls_col = CLASSES[c.class_name]["color"]
                draw_text(self.screen, f"{c.name} — {c.class_name}", 40, y, cls_col, 14)
                y += 22

        draw_text(self.screen, "Every adventurer has a story.",
                  SCREEN_W//2 - 160, 250, CREAM, 18)
        draw_text(self.screen, "Would you like to discover yours?",
                  SCREEN_W//2 - 190, 280, GREY, 16)

        r1 = pygame.Rect(SCREEN_W//2 - 220, 350, 440, 60)
        r2 = pygame.Rect(SCREEN_W//2 - 220, 430, 440, 60)
        h1 = r1.collidepoint(mx, my)
        h2 = r2.collidepoint(mx, my)

        draw_button(self.screen, r1, "Tell My Story", hover=h1, size=18)
        draw_text(self.screen, "Shape your character through life events",
                  SCREEN_W//2 - 200, 418, DARK_GREY, 12)

        draw_button(self.screen, r2, "Quick Roll", hover=h2, size=18)
        draw_text(self.screen, "Pick a class and start immediately",
                  SCREEN_W//2 - 175, 498, DARK_GREY, 12)

    # ── Name Input ────────────────────────────────────────────

    def draw_name(self):
        mode = "Quick Roll" if self.quick else "Life Path"
        draw_text(self.screen, f"Character {self.char_index + 1} — {mode}",
                  SCREEN_W//2 - 140, 60, GOLD, 18, bold=True)

        draw_text(self.screen, "What is your name, adventurer?",
                  SCREEN_W//2 - 180, 200, CREAM, 20)

        # Input box
        box = pygame.Rect(SCREEN_W//2 - 200, 260, 400, 50)
        draw_panel(self.screen, box, border_color=HIGHLIGHT)

        display = self.name_text
        cursor = "|" if (self.blink // 500) % 2 == 0 else ""
        draw_text(self.screen, display + cursor, box.x + 15, box.y + 14, WHITE, 20)

        draw_text(self.screen, "Press ENTER to continue",
                  SCREEN_W//2 - 120, 340, DARK_GREY, 14)

    # ── Life Path ─────────────────────────────────────────────

    def draw_lifepath(self, mx, my):
        # Header
        phase = PHASE_FOR_SLOT.get(self.slot, "")
        slot_title = SLOT_TITLES.get(self.slot, "")
        draw_text(self.screen, f"{self.current_char.name}'s Story",
                  40, 20, GOLD, 20, bold=True)
        draw_text(self.screen, f"{phase} — {slot_title}",
                  40, 50, HIGHLIGHT, 16)

        # Current stats (small, mysterious hints)
        x_stats = SCREEN_W - 200
        draw_panel(self.screen, pygame.Rect(x_stats - 10, 15, 195, 160))
        draw_text(self.screen, "Character", x_stats, 20, DIM_GOLD, 12)
        y = 40
        for stat in STAT_NAMES:
            val = self.current_char.stats[stat]
            bar_w = min(100, val * 5)
            col = HIGHLIGHT if val > 8 else GREY if val > 5 else DARK_GREY
            draw_text(self.screen, f"{stat}", x_stats, y, GREY, 12)
            draw_text(self.screen, f"{val:2d}", x_stats + 40, y, col, 12)
            pygame.draw.rect(self.screen, DARKER_GREY, (x_stats + 65, y+3, 100, 10))
            pygame.draw.rect(self.screen, col, (x_stats + 65, y+3, bar_w, 10))
            y += 20

        # Progress dots
        dot_y = 195
        draw_text(self.screen, "Progress:", 40, dot_y, DARK_GREY, 12)
        for i in range(1, 10):
            dx = 130 + (i-1) * 28
            col = GREEN if i < self.slot else GOLD if i == self.slot else DARK_GREY
            r = 8 if i == self.slot else 5
            pygame.draw.circle(self.screen, col, (dx, dot_y + 7), r)
            if i in (3, 6):  # Phase dividers
                pygame.draw.line(self.screen, DARK_GREY, (dx+14, dot_y+7), (dx+18, dot_y+7))

        # Choice list
        self.hover = -1
        item_h = 95
        visible = 4
        cy = 230
        for i in range(visible):
            idx = self.scroll + i
            if idx >= len(self.choices):
                break
            ev = self.choices[idx]
            rect = pygame.Rect(40, cy, SCREEN_W - 80, item_h - 5)
            is_hover = rect.collidepoint(mx, my)
            if is_hover:
                self.hover = idx

            bg = (45, 38, 75) if is_hover else PANEL_BG
            brd = GOLD if is_hover else PANEL_BORDER
            draw_panel(self.screen, rect, border_color=brd, bg_color=bg)

            draw_text(self.screen, ev["title"], rect.x + 12, rect.y + 8,
                      GOLD if is_hover else CREAM, 16, bold=True)

            # Truncate text for preview
            txt = ev.get("text", "")
            draw_wrapped_text(self.screen, txt, rect.x + 12, rect.y + 30,
                              rect.width - 24, GREY if not is_hover else WHITE, get_font(13))
            cy += item_h

        # Scroll hints
        if self.scroll > 0:
            draw_text(self.screen, "^ more above ^", SCREEN_W//2 - 60, 218, DIM_GOLD, 11)
        if self.scroll + visible < len(self.choices):
            draw_text(self.screen, "v more below v", SCREEN_W//2 - 60, cy + 5, DIM_GOLD, 11)

    # ── Random Outcome ────────────────────────────────────────

    def draw_random(self):
        draw_text(self.screen, self.random_evt["title"],
                  SCREEN_W//2 - 200, 100, GOLD, 22, bold=True)

        # Show the base text
        draw_wrapped_text(self.screen, self.random_evt["text"],
                          80, 160, SCREEN_W - 160, CREAM, get_font(16))

        # Outcome
        rand = self.random_evt.get("random")
        if not rand:
            # No random element - just show continue
            if self.timer > 500:
                draw_text(self.screen, "Click to continue...",
                          SCREEN_W//2 - 100, SCREEN_H - 60, DIM_GOLD, 14)
            return

        outcome = rand.get("success") if self.random_ok else rand.get("fail")
        if not outcome:
            return
        outcome_text = outcome.get("text", "")

        # Dramatic reveal
        if self.timer > 600:
            col = GREEN if self.random_ok else ORANGE
            label = "Fortune smiles..." if self.random_ok else "Fate has other plans..."
            draw_text(self.screen, label, SCREEN_W//2 - 120, 340, col, 18, bold=True)

        if self.timer > 1000:
            draw_wrapped_text(self.screen, outcome_text,
                              80, 390, SCREEN_W - 160, WHITE, get_font(15))

        if self.timer > 1500:
            draw_text(self.screen, "Click to continue...",
                      SCREEN_W//2 - 100, SCREEN_H - 60, DIM_GOLD, 14)

    # ── Class Select ──────────────────────────────────────────

    def draw_class(self, mx, my):
        draw_text(self.screen, f"Choose {self.current_char.name}'s Class",
                  40, 25, GOLD, 22, bold=True)

        # Stats summary
        if not self.quick:
            draw_text(self.screen, "Your life has shaped these attributes:",
                      40, 60, GREY, 14)
            x = 40
            for stat in STAT_NAMES:
                val = self.current_char.stats[stat]
                draw_text(self.screen, f"{stat}: {val}", x, 85, HIGHLIGHT, 15, bold=True)
                x += 110

            # Backstory preview
            bs = self.current_char.get_backstory_text()
            if bs:
                draw_panel(self.screen, pygame.Rect(35, 115, SCREEN_W - 70, 60),
                           bg_color=(25, 20, 40))
                draw_wrapped_text(self.screen, bs, 45, 122, SCREEN_W - 90,
                                  GREY, get_font(12))

        start_y = 190 if not self.quick else 120
        item_h = 85
        visible = 6
        self.class_hover = -1

        for i in range(visible):
            idx = self.scroll + i
            if idx >= len(self.class_choices):
                break
            cn, fit, score = self.class_choices[idx]
            cls = CLASSES[cn]
            rect = pygame.Rect(40, start_y + i * item_h, SCREEN_W - 80, item_h - 5)
            is_hover = rect.collidepoint(mx, my)
            if is_hover:
                self.class_hover = idx

            bg = (45, 38, 75) if is_hover else PANEL_BG
            brd = cls["color"] if is_hover else PANEL_BORDER
            draw_panel(self.screen, rect, border_color=brd, bg_color=bg)

            # Class name and fit
            draw_text(self.screen, cn, rect.x + 12, rect.y + 8,
                      cls["color"], 18, bold=True)

            if not self.quick:
                fit_col = FIT_COLORS.get(fit, GREY)
                draw_text(self.screen, f"[ {fit} ]", rect.x + 180, rect.y + 10,
                          fit_col, 13)

            # Description
            draw_text(self.screen, cls["description"], rect.x + 12, rect.y + 32,
                      GREY if not is_hover else WHITE, 13,
                      max_width=rect.width - 24)

            # Starting abilities
            ab_text = "Starts with: " + ", ".join(a["name"] for a in cls["starting_abilities"])
            draw_text(self.screen, ab_text, rect.x + 12, rect.y + 55,
                      DIM_GOLD, 11)

    # ── Character Summary ─────────────────────────────────────

    def draw_summary(self, mx, my):
        c = self.current_char
        cls = CLASSES[c.class_name]

        draw_text(self.screen, c.name, 40, 25, cls["color"], 26, bold=True)
        draw_text(self.screen, f"{c.class_name}  —  Level {c.level}",
                  40, 60, CREAM, 16)

        # Stats
        draw_panel(self.screen, pygame.Rect(35, 95, 300, 175))
        draw_text(self.screen, "Attributes", 50, 102, GOLD, 14, bold=True)
        y = 125
        for stat in STAT_NAMES:
            val = c.stats[stat]
            draw_text(self.screen, f"{STAT_FULL_NAMES[stat]}", 50, y, CREAM, 13)
            draw_text(self.screen, f"{val}", 200, y, HIGHLIGHT, 14, bold=True)
            bar_w = min(80, val * 4)
            pygame.draw.rect(self.screen, DARKER_GREY, (230, y+3, 80, 10))
            pygame.draw.rect(self.screen, cls["color"], (230, y+3, bar_w, 10))
            y += 23

        # Resources
        draw_panel(self.screen, pygame.Rect(355, 95, 300, 175))
        draw_text(self.screen, "Resources", 370, 102, GOLD, 14, bold=True)
        y = 125
        for rname, rval in c.resources.items():
            draw_text(self.screen, f"{rname}:", 370, y, CREAM, 13)
            draw_text(self.screen, f"{rval}", 470, y, GREEN, 14, bold=True)
            y += 23

        # Abilities
        draw_panel(self.screen, pygame.Rect(675, 95, 310, 175))
        draw_text(self.screen, "Abilities", 690, 102, GOLD, 14, bold=True)
        y = 125
        for ab in c.abilities:
            draw_text(self.screen, ab["name"], 690, y, HIGHLIGHT, 14)
            draw_text(self.screen, f"{ab['cost']} {ab['resource']}", 690, y + 16,
                      DARK_GREY, 11)
            y += 38

        # Backstory
        draw_panel(self.screen, pygame.Rect(35, 285, SCREEN_W - 70, 100))
        draw_text(self.screen, "Backstory", 50, 292, GOLD, 14, bold=True)
        bs = c.get_backstory_text()
        draw_wrapped_text(self.screen, bs, 50, 315, SCREEN_W - 110, GREY, get_font(13))

        # Buttons
        r_acc = pygame.Rect(SCREEN_W//2 - 230, SCREEN_H - 70, 200, 45)
        r_redo = pygame.Rect(SCREEN_W//2 + 30, SCREEN_H - 70, 200, 45)
        draw_button(self.screen, r_acc, "Accept", hover=r_acc.collidepoint(mx,my), size=18)
        draw_button(self.screen, r_redo, "Start Over", hover=r_redo.collidepoint(mx,my), size=16)

    # ── Party Review ──────────────────────────────────────────

    def draw_party(self, mx, my):
        draw_text(self.screen, "Your Party", SCREEN_W//2 - 80, 20, GOLD, 24, bold=True)
        draw_text(self.screen, "The Realm of Shadows awaits...",
                  SCREEN_W//2 - 160, 55, GREY, 15)

        # Draw party members (2 columns, 3 rows visible with scroll)
        cols = 2
        card_w = (SCREEN_W - 80) // cols - 10
        card_h = 210
        visible_rows = 3

        for idx in range(len(self.party)):
            row = idx // cols - self.party_scroll
            col = idx % cols
            if row < 0 or row >= visible_rows:
                continue

            c = self.party[idx]
            cls = CLASSES[c.class_name]
            cx = 40 + col * (card_w + 20)
            cy = 90 + row * (card_h + 10)

            rect = pygame.Rect(cx, cy, card_w, card_h)
            draw_panel(self.screen, rect, border_color=cls["color"])

            # Name and class
            draw_text(self.screen, c.name, cx + 10, cy + 8, cls["color"], 16, bold=True)
            draw_text(self.screen, c.class_name, cx + 10, cy + 28, CREAM, 13)

            # Stats in compact form
            sy = cy + 50
            for i, stat in enumerate(STAT_NAMES):
                val = c.stats[stat]
                sx = cx + 10 + (i % 3) * 150
                sdy = sy + (i // 3) * 20
                draw_text(self.screen, f"{stat}: {val}", sx, sdy, HIGHLIGHT, 12)

            # Resources compact
            ry = sy + 50
            for rname, rval in c.resources.items():
                draw_text(self.screen, f"{rname}: {rval}", cx + 10, ry, DIM_GREEN, 11)
                ry += 16

            # Abilities
            ab_names = [a["name"] for a in c.abilities]
            draw_text(self.screen, "Skills: " + ", ".join(ab_names),
                      cx + 10, cy + card_h - 25, DARK_GREY, 10,
                      max_width=card_w - 20)

        # Begin button (or encounter picker in debug)
        if self.debug_mode:
            from data.enemies import ENCOUNTERS
            enc_keys = list(ENCOUNTERS.keys())
            draw_text(self.screen, "Pick an encounter:", SCREEN_W//2 - 100,
                      SCREEN_H - 210, GOLD, 16, bold=True)
            for i, key in enumerate(enc_keys):
                enc = ENCOUNTERS[key]
                bx = 40 + (i % 3) * 220
                by = SCREEN_H - 180 + (i // 3) * 50
                btn_rect = pygame.Rect(bx, by, 210, 42)
                hover = btn_rect.collidepoint(mx, my)
                diff_col = {"easy": GREEN, "medium": ORANGE, "hard": RED,
                            "boss": PURPLE}.get(enc["difficulty"], CREAM)
                label = f"{enc['name']}"
                draw_button(self.screen, btn_rect, label, hover=hover, size=13)
                draw_text(self.screen, enc["difficulty"],
                          bx + 215, by + 14, diff_col, 11)
        else:
            r = pygame.Rect(SCREEN_W//2 - 150, SCREEN_H - 65, 300, 45)
            draw_button(self.screen, r, "Begin Adventure!",
                        hover=r.collidepoint(mx, my), size=18)

        # Inventory button (always visible, top-right of party screen)
        if self.party:
            inv_btn = pygame.Rect(SCREEN_W - 200, 40, 180, 40)
            draw_button(self.screen, inv_btn, "Inventory",
                        hover=inv_btn.collidepoint(mx, my), size=16)

    # ══════════════════════════════════════════════════════════
    #  COMBAT
    # ══════════════════════════════════════════════════════════

    def start_combat(self, encounter_key):
        """Initialize combat with an encounter."""
        self.combat_state = CombatState(self.party, encounter_key)
        self.combat_ui = CombatUI(self.combat_state)
        self.enemy_turn_delay = 0
        self.go(S_COMBAT)

    def draw_combat(self, mx, my):
        """Draw the combat screen and handle enemy AI timing."""
        self.combat_ui.draw(self.screen, mx, my)

        # Auto-execute enemy turns with a small delay for readability
        if (self.combat_state.phase not in ("victory", "defeat") and
                not self.combat_state.is_player_turn()):
            self.enemy_turn_delay += self.clock.get_time()
            self.combat_ui.enemy_anim_timer += self.clock.get_time()
            if self.enemy_turn_delay > 600:  # 600ms delay between enemy actions
                self.combat_state.execute_enemy_turn()
                self.enemy_turn_delay = 0
                self.combat_ui.enemy_anim_timer = 0

    def start_post_combat(self):
        """Initialize the post-combat screen with rewards."""
        rewards = getattr(self.combat_state, "rewards", {})
        self.post_combat_ui = PostCombatUI(
            self.party, rewards, self.combat_state.players
        )
        self.go(S_POST_COMBAT)

    def draw_post_combat(self, mx, my):
        """Draw the post-combat results screen."""
        dt = self.clock.get_time()
        self.post_combat_ui.draw(self.screen, mx, my, dt)

    def draw_inventory(self, mx, my):
        """Draw the inventory/equipment screen."""
        dt = self.clock.get_time()
        self.inventory_ui.draw(self.screen, mx, my, dt)

    def process_combat_action(self, action):
        """Process a player combat action from the UI."""
        if action["type"] == "end_combat":
            if action["result"] == "victory":
                # Go to post-combat screen
                self.start_post_combat()
            else:
                # Defeat — retry
                self.start_combat("tutorial")
            return

        if action["type"] == "attack":
            self.combat_state.execute_player_action("attack", target=action["target"])
        elif action["type"] == "defend":
            self.combat_state.execute_player_action("defend")
        elif action["type"] == "ability":
            self.combat_state.execute_player_action(
                "ability", target=action["target"], ability=action["ability"]
            )
        elif action["type"] == "move":
            self.combat_state.execute_player_action("move", target=action["direction"])

        # Reset UI mode after action
        self.combat_ui.action_mode = "main"


# ── Entry Point ───────────────────────────────────────────────

DEBUG_PARTY_CLASSES = ["Fighter", "Mage", "Cleric", "Thief", "Ranger", "Monk"]
DEBUG_PARTY_NAMES = ["Aldric", "Lyra", "Sera", "Kael", "Wren", "Zhen"]


def make_debug_party():
    """Quick-roll a full party for testing."""
    party = []
    for name, cls in zip(DEBUG_PARTY_NAMES, DEBUG_PARTY_CLASSES):
        c = Character(name)
        c.quick_roll(cls)
        party.append(c)
    return party


if __name__ == "__main__":
    debug = "--debug" in sys.argv or "-d" in sys.argv
    game = Game()

    if debug:
        game.debug_mode = True
        game.party = make_debug_party()
        game.char_index = PARTY_SIZE
        game.state = S_PARTY
        print("\n══════ DEBUG MODE ══════")
        print("Auto-generated party — pick encounters in-game!")
        print("════════════════════════\n")

    game.run()
