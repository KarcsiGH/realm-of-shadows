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
from ui.town_ui import TownUI
from ui.world_map_ui import WorldMapUI
from ui.dungeon_ui import DungeonUI
from data.world_map import WorldState, LOCATIONS, LOC_TOWN, LOC_DUNGEON
from data.dungeon import DungeonState, DUNGEONS
from core.save_load import save_game, load_game

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
S_TOWN        = 11
S_WORLD_MAP   = 12
S_DUNGEON     = 13
S_OPENING     = 14   # opening narrative sequence
S_DIALOGUE    = 15   # standalone dialogue (e.g., boss pre-fight)


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
        self.inventory_return_state = S_PARTY
        # Town
        self.town_ui = None
        # Save/Load
        self.save_msg = ""
        self.save_msg_timer = 0
        self.save_msg_color = CREAM
        # World Map
        self.world_state = None
        self.world_map_ui = None
        # Dungeon
        self.dungeon_state = None
        self.dungeon_ui = None
        self.pre_dungeon_state = None  # state to return to after dungeon  # where to go back to
        self.dungeon_cache = {}  # dungeon_id -> DungeonState (persistent between visits)
        # Opening narrative
        self.opening_lines = []
        self.opening_idx = 0
        self.opening_chars = 0
        self.opening_speed = 1.5
        # Standalone dialogue (boss pre-fight, dungeon events)
        self.dialogue_ui = None
        self.dialogue_return_state = None
        self.dialogue_callback = None  # function to call after dialogue ends
        # Quest log
        self.quest_log_ui = None
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
                        # Show opening narrative on first playthrough
                        from core.story_flags import has
                        if not has("intro_seen"):
                            self._start_opening()
                        else:
                            self.go(S_PARTY)
                    else:
                        self.go(S_MODE)
                elif r_redo.collidepoint(mx, my):
                    self.go(S_MODE)

        elif self.state == S_PARTY:
            if e.type == pygame.MOUSEBUTTONDOWN:
                # Quest log overlay
                if self.quest_log_ui:
                    if e.button == 1:
                        result = self.quest_log_ui.handle_click(mx, my)
                        if result == "close" or self.quest_log_ui.finished:
                            self.quest_log_ui = None
                    elif e.button == 4:
                        self.quest_log_ui.handle_scroll(-1)
                    elif e.button == 5:
                        self.quest_log_ui.handle_scroll(1)
                    return
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE and self.quest_log_ui:
                    self.quest_log_ui = None
                    return
                if e.button == 4:
                    self.party_scroll = max(0, self.party_scroll - 1)
                elif e.button == 5:
                    self.party_scroll = min(max(0, len(self.party) - 3), self.party_scroll + 1)
                elif e.button == 1:
                    # Inventory button
                    inv_btn = pygame.Rect(SCREEN_W - 200, 40, 180, 40)
                    if inv_btn.collidepoint(mx, my) and self.party:
                        self.inventory_ui = InventoryUI(self.party)
                        # Return to where we came from
                        if self.dungeon_state:
                            self.inventory_return_state = S_DUNGEON
                        else:
                            self.inventory_return_state = S_PARTY
                        self.go(S_INVENTORY)
                        return
                    # Journal button
                    journal_btn = pygame.Rect(SCREEN_W - 200, 85, 180, 34)
                    if journal_btn.collidepoint(mx, my) and self.party:
                        from ui.quest_log_ui import QuestLogUI
                        self.quest_log_ui = QuestLogUI()
                        return
                    # Town button (only if not in dungeon)
                    if not self.dungeon_state:
                        town_btn = pygame.Rect(SCREEN_W - 400, 40, 180, 40)
                        if town_btn.collidepoint(mx, my) and self.party:
                            self.town_ui = TownUI(self.party)
                            self.go(S_TOWN)
                            return
                    # Save button
                    save_btn = pygame.Rect(20, 40, 120, 40)
                    if save_btn.collidepoint(mx, my) and self.party:
                        ok, path, msg = save_game(self.party)
                        self.save_msg = msg
                        self.save_msg_color = GREEN if ok else RED
                        self.save_msg_timer = 3000
                        return
                    # Load button
                    load_btn = pygame.Rect(150, 40, 120, 40)
                    if load_btn.collidepoint(mx, my):
                        ok, party, msg = load_game()
                        if ok:
                            self.party = party
                            self.save_msg = msg
                            self.save_msg_color = GREEN
                        else:
                            self.save_msg = msg
                            self.save_msg_color = RED
                        self.save_msg_timer = 3000
                        return
                    # World Map / Back button
                    world_btn = pygame.Rect(290, 40, 160, 40)
                    if world_btn.collidepoint(mx, my) and self.party:
                        if self.dungeon_state:
                            self.go(S_DUNGEON)
                        else:
                            self._init_world_map()
                            self.go(S_WORLD_MAP)
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
                    self.go(self.inventory_return_state)
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button in (1, 3):  # left or right click
                    result = self.inventory_ui.handle_click(mx, my, button=e.button)
                    if result == "back":
                        self.go(self.inventory_return_state)
                elif e.button == 4:
                    self.inventory_ui.handle_scroll(-1)
                elif e.button == 5:
                    self.inventory_ui.handle_scroll(1)

        elif self.state == S_TOWN:
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    result = self.town_ui.handle_click(mx, my)
                    if result == "exit":
                        self.go(S_WORLD_MAP)
                    elif result == "inn_save":
                        # Auto-save when resting at inn
                        from core.save_load import save_game
                        try:
                            save_game(self.party, self.world_state, "inn_autosave")
                        except Exception:
                            pass  # save is best-effort
                elif e.button == 4:
                    self.town_ui.handle_scroll(-1)
                elif e.button == 5:
                    self.town_ui.handle_scroll(1)

        elif self.state == S_WORLD_MAP:
            if e.type == pygame.KEYDOWN:
                event = self.world_map_ui.handle_key(e.key)
                self._process_world_event(event)
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                event = self.world_map_ui.handle_click(mx, my)
                self._process_world_event(event)

        elif self.state == S_DUNGEON:
            if e.type == pygame.KEYDOWN:
                event = self.dungeon_ui.handle_key(e.key)
                self._process_dungeon_event(event)
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                event = self.dungeon_ui.handle_click(mx, my)
                self._process_dungeon_event(event)

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
                    # Check inventory button first
                    inv_btn = pygame.Rect(SCREEN_W - 160, 8, 140, 36)
                    if inv_btn.collidepoint(mx, my) and self.party:
                        self.inventory_ui = InventoryUI(self.party)
                        self.inventory_return_state = S_POST_COMBAT
                        self.go(S_INVENTORY)
                        return
                    result = self.post_combat_ui.handle_click(mx, my)
                    if result == "continue":
                        self.party_scroll = 0
                        if self.dungeon_state:
                            self.go(S_DUNGEON)
                        elif self.world_state:
                            self.go(S_WORLD_MAP)
                        else:
                            self.go(S_PARTY)
                elif e.button == 4:
                    self.post_combat_ui.handle_scroll(-1)
                elif e.button == 5:
                    self.post_combat_ui.handle_scroll(1)
                    self.combat_ui.handle_scroll(1)

        elif self.state == S_OPENING:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                self._advance_opening()
            elif e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_SPACE, pygame.K_RETURN):
                    self._advance_opening()
                elif e.key == pygame.K_ESCAPE:
                    # Skip entire opening
                    from core.story_flags import set_flag, start_quest
                    set_flag("intro_seen", True)
                    start_quest("main_meet_maren")
                    self.go(S_PARTY)

        elif self.state == S_DIALOGUE:
            if self.dialogue_ui:
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    result = self.dialogue_ui.handle_click(mx, my)
                    if self.dialogue_ui.finished:
                        self._end_dialogue()
                elif e.type == pygame.KEYDOWN:
                    result = self.dialogue_ui.handle_event(e)
                    if self.dialogue_ui and self.dialogue_ui.finished:
                        self._end_dialogue()

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
        elif self.state == S_TOWN:      self.draw_town(mx, my)
        elif self.state == S_WORLD_MAP: self.draw_world_map(mx, my)
        elif self.state == S_DUNGEON:   self.draw_dungeon(mx, my)
        elif self.state == S_OPENING:   self.draw_opening()
        elif self.state == S_DIALOGUE:  self.draw_dialogue(mx, my)

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
        # Quest log overlay
        if self.quest_log_ui:
            self.quest_log_ui.draw(self.screen, mx, my)
            return

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

        # Top buttons (always visible)
        if self.party:
            inv_btn = pygame.Rect(SCREEN_W - 200, 40, 180, 40)
            draw_button(self.screen, inv_btn, "Inventory",
                        hover=inv_btn.collidepoint(mx, my), size=16)
            # Journal button
            journal_btn = pygame.Rect(SCREEN_W - 200, 85, 180, 34)
            draw_button(self.screen, journal_btn, "Journal",
                        hover=journal_btn.collidepoint(mx, my), size=14)
            if not self.dungeon_state:
                town_btn = pygame.Rect(SCREEN_W - 400, 40, 180, 40)
                draw_button(self.screen, town_btn, "Town",
                            hover=town_btn.collidepoint(mx, my), size=16)
            save_btn = pygame.Rect(20, 40, 120, 40)
            draw_button(self.screen, save_btn, "Save",
                        hover=save_btn.collidepoint(mx, my), size=16)
            load_btn = pygame.Rect(150, 40, 120, 40)
            draw_button(self.screen, load_btn, "Load",
                        hover=load_btn.collidepoint(mx, my), size=16)
            world_btn = pygame.Rect(290, 40, 160, 40)
            back_label = "Back to Dungeon" if self.dungeon_state else "World Map"
            draw_button(self.screen, world_btn, back_label,
                        hover=world_btn.collidepoint(mx, my), size=14 if self.dungeon_state else 16)

            # Save/load message
            if hasattr(self, 'save_msg') and self.save_msg_timer > 0:
                self.save_msg_timer -= self.clock.get_time()
                draw_text(self.screen, self.save_msg, 290, 52,
                          self.save_msg_color, 14)

    # ══════════════════════════════════════════════════════════
    #  COMBAT
    # ══════════════════════════════════════════════════════════

    # ══════════════════════════════════════════════════════════
    #  OPENING NARRATIVE
    # ══════════════════════════════════════════════════════════

    def _start_opening(self):
        """Begin the opening narrative sequence."""
        from data.story_data import OPENING_SEQUENCE
        from core.story_flags import set_flag, start_quest
        self.opening_lines = OPENING_SEQUENCE
        self.opening_idx = 0
        self.opening_chars = 0
        self.opening_speed = 1.5
        set_flag("intro_seen", True)
        start_quest("main_meet_maren")
        self.go(S_OPENING)

    def _advance_opening(self):
        """Advance the opening text — show full text or go to next line."""
        if self.opening_idx >= len(self.opening_lines):
            self.go(S_PARTY)
            return
        text = self.opening_lines[self.opening_idx][1]
        if self.opening_chars < len(text):
            # Show full text immediately
            self.opening_chars = len(text) + 1
        else:
            # Next line
            self.opening_idx += 1
            self.opening_chars = 0
            if self.opening_idx >= len(self.opening_lines):
                self.go(S_PARTY)

    def draw_opening(self):
        """Draw the opening narrative sequence."""
        self.screen.fill((5, 3, 12))

        if self.opening_idx >= len(self.opening_lines):
            return

        speaker, text = self.opening_lines[self.opening_idx]
        self.opening_chars = min(self.opening_chars + self.opening_speed, len(text))
        shown = text[:int(self.opening_chars)]

        # Wrap and draw centered
        font = get_font(18)
        max_w = SCREEN_W - 200
        words = shown.split()
        lines = []
        cur = ""
        for w in words:
            test = cur + (" " if cur else "") + w
            if font.size(test)[0] <= max_w:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        if not lines:
            lines = [""]

        total_h = len(lines) * 28
        start_y = SCREEN_H // 2 - total_h // 2
        for i, line in enumerate(lines):
            lw = font.size(line)[0]
            draw_text(self.screen, line,
                      SCREEN_W // 2 - lw // 2,
                      start_y + i * 28,
                      (200, 190, 170), 18)

        # Progress dots
        dot_y = SCREEN_H - 60
        for i in range(len(self.opening_lines)):
            col = GOLD if i == self.opening_idx else (40, 35, 55) if i > self.opening_idx else (80, 70, 100)
            pygame.draw.circle(self.screen, col,
                               (SCREEN_W // 2 - (len(self.opening_lines) * 12) // 2 + i * 12, dot_y), 4)

        if int(self.opening_chars) >= len(text):
            draw_text(self.screen, "Click to continue" if self.opening_idx < len(self.opening_lines) - 1 else "Click to begin",
                      SCREEN_W // 2 - 70, SCREEN_H - 35, (120, 110, 90), 13)

    # ══════════════════════════════════════════════════════════
    #  STANDALONE DIALOGUE
    # ══════════════════════════════════════════════════════════

    def start_dialogue(self, npc_id, return_state=None, callback=None):
        """Start a standalone dialogue (boss pre-fight, dungeon NPC, etc.)."""
        from data.story_data import NPC_DIALOGUES
        from core.dialogue import select_dialogue
        from ui.dialogue_ui import DialogueUI

        dialogues = NPC_DIALOGUES.get(npc_id, [])
        if not dialogues:
            return False

        ds = select_dialogue(npc_id, dialogues)
        if not ds:
            return False

        self.dialogue_ui = DialogueUI(ds)
        self.dialogue_return_state = return_state or self.state
        self.dialogue_callback = callback
        self.go(S_DIALOGUE)
        return True

    def _end_dialogue(self):
        """Handle dialogue completion."""
        result = None
        if self.dialogue_ui:
            result = self.dialogue_ui.result  # e.g., "fight" for boss combat
        callback = self.dialogue_callback
        return_state = self.dialogue_return_state

        self.dialogue_ui = None
        self.dialogue_callback = None
        self.dialogue_return_state = None

        if callback:
            callback(result)
        elif return_state is not None:
            self.go(return_state)

    def draw_dialogue(self, mx, my):
        """Draw standalone dialogue."""
        if self.dialogue_ui:
            self.dialogue_ui.draw(self.screen, mx, my)

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

    def draw_town(self, mx, my):
        """Draw the town hub screen."""
        dt = self.clock.get_time()
        self.town_ui.draw(self.screen, mx, my, dt)

    def draw_world_map(self, mx, my):
        """Draw the world map."""
        dt = self.clock.get_time()
        self.world_map_ui.draw(self.screen, mx, my, dt)

    def draw_dungeon(self, mx, my):
        """Draw the dungeon."""
        dt = self.clock.get_time()
        self.dungeon_ui.draw(self.screen, mx, my, dt)

    def _init_world_map(self):
        """Initialize world state if needed."""
        if not self.world_state:
            self.world_state = WorldState(self.party)
        self.world_map_ui = WorldMapUI(self.world_state)

    def _process_world_event(self, event):
        """Handle events from the world map."""
        if event is None:
            return

        if event["type"] == "encounter":
            print(f"[DEBUG] World encounter triggered: {event['key']}")
            self.start_combat(event["key"])

        elif event["type"] == "camp":
            result = self.world_state.camp()
            if result["type"] == "camp_ambush":
                self.world_map_ui._show_event("Ambush during rest!", RED)
                self.start_combat(result["key"])
            else:
                healed = result.get("healed", {})
                parts = [f"{name} +{hp}HP" for name, hp in healed.items() if hp > 0]
                msg = "Rested safely. " + ", ".join(parts) if parts else "Rested safely. Already at full health."
                self.world_map_ui._show_event(msg, GREEN)

        elif event["type"] == "enter_location":
            loc = event["data"]
            print(f"[DEBUG] enter_location: id={event.get('id')}, type={loc['type']}")
            if loc["type"] == LOC_TOWN:
                self.town_ui = TownUI(self.party)
                self.go(S_TOWN)
            elif loc["type"] == LOC_DUNGEON:
                # Find matching dungeon ID
                loc_id = event.get("id", "")
                dungeon_id = loc_id  # location ID matches dungeon ID
                print(f"[DEBUG] Dungeon entry: loc_id={loc_id}, in DUNGEONS={loc_id in DUNGEONS}")
                if dungeon_id in DUNGEONS:
                    can, reason = self.world_state.can_enter_dungeon(loc_id)
                    print(f"[DEBUG] Can enter: {can}, reason: {reason}")
                    if can:
                        # Use cached dungeon if revisiting, otherwise create new
                        if dungeon_id in self.dungeon_cache:
                            self.dungeon_state = self.dungeon_cache[dungeon_id]
                            self.dungeon_state.party = self.party  # update party ref
                            # Reset to entrance of floor 1
                            floor = self.dungeon_state.floors[1]
                            self.dungeon_state.party_x, self.dungeon_state.party_y = floor["entrance"]
                            self.dungeon_state.current_floor = 1
                        else:
                            self.dungeon_state = DungeonState(dungeon_id, self.party)
                            self.dungeon_cache[dungeon_id] = self.dungeon_state
                        self.dungeon_ui = DungeonUI(self.dungeon_state)
                        self.pre_dungeon_state = S_WORLD_MAP
                        self.go(S_DUNGEON)
                        # Show floor 1 story message
                        from data.story_data import get_dungeon_floor_message
                        msg = get_dungeon_floor_message(dungeon_id, 1)
                        if msg:
                            self.dungeon_ui.show_event(msg, (180, 160, 120))
                        print(f"[DEBUG] Entered dungeon! State={self.state}")
                    else:
                        self.world_map_ui._show_event(reason, RED)
                else:
                    # Dungeon not yet defined — generic combat
                    enc_key = loc.get("encounter_key", "tutorial")
                    self.start_combat(enc_key)
            elif loc["type"] == "port":
                # Port — show message for now (full port UI later)
                self.world_map_ui._show_event(
                    f"You arrive at {loc['name']}. (Boat travel coming soon!)",
                    (80, 180, 220))

        elif event["type"] == "discovery":
            pass  # handled by world_map_ui message display

        elif event["type"] == "menu":
            # Go to party screen (inventory, etc.)
            self.go(S_PARTY)

    def _process_dungeon_event(self, event):
        """Handle events from the dungeon."""
        # Show any step messages (poison ticks, curse effects, etc.)
        step_msgs = getattr(self.dungeon_state, '_last_step_messages', [])
        if step_msgs:
            for msg in step_msgs[:3]:  # limit to 3 messages
                self.dungeon_ui.show_event(msg, (120, 200, 50))  # green for poison
            self.dungeon_state._last_step_messages = []

        if event is None:
            return

        if event["type"] == "random_encounter":
            enc_key = self.dungeon_state.get_encounter_key()
            self.pre_dungeon_state = S_DUNGEON

            # Check for boss dialogue
            if event.get("is_boss"):
                from data.story_data import get_dungeon_boss_dialogue
                boss_npc = get_dungeon_boss_dialogue(self.dungeon_state.dungeon_id)
                if boss_npc:
                    # Show dialogue first, then start combat after
                    def after_boss_dialogue(result):
                        if result == "fight" or result is None:
                            # Grak killed path, or any "fight" outcome
                            boss_enc = DUNGEONS[self.dungeon_state.dungeon_id].get(
                                "boss_encounter", enc_key)
                            self.start_combat(boss_enc)
                        else:
                            # Peaceful resolution (e.g., Grak spared)
                            self.go(S_DUNGEON)
                    self.start_dialogue(boss_npc, return_state=S_DUNGEON,
                                        callback=after_boss_dialogue)
                    return
            self.start_combat(enc_key)

        elif event["type"] == "fixed_encounter":
            enc_key = self.dungeon_state.get_encounter_key()
            self.pre_dungeon_state = S_DUNGEON
            self.start_combat(enc_key)

        elif event["type"] == "stairs_down":
            if self.dungeon_state.go_downstairs():
                floor = self.dungeon_state.current_floor
                self.dungeon_ui.show_event(f"Descended to Floor {floor}.", GOLD)
                # Show story floor message if available
                from data.story_data import get_dungeon_floor_message
                msg = get_dungeon_floor_message(self.dungeon_state.dungeon_id, floor)
                if msg:
                    self.dungeon_ui.show_event(msg, (180, 160, 120))

        elif event["type"] == "stairs_up":
            if self.dungeon_state.go_upstairs():
                floor = self.dungeon_state.current_floor
                self.dungeon_ui.show_event(f"Ascended to Floor {floor}.", (80, 180, 220))

        elif event["type"] == "exit_dungeon":
            self.dungeon_state = None
            self.dungeon_ui = None
            if self.world_state:
                self.go(S_WORLD_MAP)
            else:
                self.go(S_PARTY)

        elif event["type"] == "treasure":
            data = event["data"]
            gold = data.get("gold", 0)
            items = data.get("items", [])
            # Distribute gold evenly across party
            if gold > 0:
                share = gold // len(self.party)
                remainder = gold % len(self.party)
                for i, c in enumerate(self.party):
                    c.gold += share + (1 if i < remainder else 0)
            # Items go to party leader's inventory — auto-ID if known
            from core.party_knowledge import auto_identify_if_known, mark_item_identified
            for item in items:
                item_copy = dict(item)
                auto_identify_if_known(item_copy)
                if item_copy.get("identified"):
                    mark_item_identified(item_copy.get("name", ""))
                self.party[0].inventory.append(item_copy)
            parts = []
            if gold > 0:
                parts.append(f"{gold} gold")
            for item in items:
                parts.append(item["name"])
            msg = "Found: " + ", ".join(parts) if parts else "The chest is empty."
            if items:
                msg += f" (Check {self.party[0].name}'s inventory)"
            self.dungeon_ui.show_event(msg, GOLD)

        elif event["type"] == "trap":
            data = event["data"]
            dmg_base = data.get("damage", 10)
            trap_name = data.get("name", "Trap")
            trap_target = data.get("target", "single")
            was_detected = data.get("detected", False)
            import random as rmod
            from data.dungeon import resolve_trap_saving_throw
            from core.status_effects import add_poison, add_curse

            # Determine targets
            if trap_target == "area":
                targets = list(self.party)
            else:
                targets = [rmod.choice(self.party)]

            # Apply damage with saving throws
            results = []
            for target in targets:
                save = resolve_trap_saving_throw(target, data)
                if save == "avoid":
                    results.append(f"{target.name} dodges!")
                elif save == "half":
                    actual_dmg = max(1, dmg_base // 2)
                    target.resources["HP"] = target.resources.get("HP", 0) - actual_dmg
                    results.append(f"{target.name}: {actual_dmg} dmg (half)")
                elif save == "crit_fail":
                    actual_dmg = dmg_base
                    target.resources["HP"] = target.resources.get("HP", 0) - actual_dmg
                    results.append(f"{target.name}: {actual_dmg} dmg!")
                    # Apply status effects on crit fail
                    if data.get("poison"):
                        add_poison(target, data["poison"])
                        results.append(f"{target.name} poisoned!")
                    if data.get("curse"):
                        add_curse(target, data["curse"])
                        results.append(f"{target.name} cursed!")
                else:  # full damage
                    actual_dmg = dmg_base
                    target.resources["HP"] = target.resources.get("HP", 0) - actual_dmg
                    results.append(f"{target.name}: {actual_dmg} dmg")
                    # Poison traps also apply poison on full hit (50% chance)
                    if data.get("poison") and rmod.random() < 0.5:
                        add_poison(target, data["poison"])
                        results.append(f"{target.name} poisoned!")

            # Build display message
            if was_detected:
                prefix = f"Detected {trap_name} (Tier {data.get('tier',1)})!"
                color = ORANGE
            else:
                prefix = f"{trap_name} (Tier {data.get('tier',1)})!"
                data["detected"] = True
                color = RED

            msg = prefix + " " + " | ".join(results[:4])  # limit display length
            self.dungeon_ui.show_event(msg, color)

        elif event["type"] == "camp":
            # Camping in dungeon — higher ambush risk
            import random
            ambush_chance = 25 + self.dungeon_state.current_floor * 5
            for c in self.party:
                if c.class_name == "Ranger":
                    ambush_chance -= 5
                if c.class_name == "Cleric":
                    ambush_chance -= 3

            if random.randint(1, 100) <= ambush_chance:
                enc_key = self.dungeon_state.get_encounter_key()
                self.dungeon_ui.show_event("Ambush during rest!", RED)
                self.pre_dungeon_state = S_DUNGEON
                self.start_combat(enc_key)
            else:
                from core.classes import get_all_resources
                for c in self.party:
                    max_res = get_all_resources(c.class_name, c.stats, c.level)
                    max_hp = max_res.get("HP", 1)
                    c.resources["HP"] = min(max_hp, c.resources.get("HP", 0) + int(max_hp * 0.25))
                    for res in c.resources:
                        if res != "HP":
                            max_val = max_res.get(res, 0)
                            c.resources[res] = min(max_val, c.resources[res] + int(max_val * 0.15))
                self.dungeon_ui.show_event("Rested safely in the dungeon.", GREEN)

        elif event["type"] == "menu":
            self.pre_dungeon_state = S_DUNGEON
            self.inventory_return_state = S_DUNGEON
            self.go(S_PARTY)

    def process_combat_action(self, action):
        """Process a player combat action from the UI."""
        if action["type"] == "end_combat":
            if action["result"] == "victory":
                # Sync HP, resources, and status effects from combat back to characters
                for p in self.combat_state.players:
                    char = p.get("character_ref")
                    if char:
                        char.resources["HP"] = max(0, p["hp"])
                        # Sync other resources (MP, SP, etc.)
                        for rk, rv in p.get("resources", {}).items():
                            char.resources[rk] = rv
                        # Unconscious characters wake at 1 HP
                        if char.resources["HP"] <= 0:
                            char.resources["HP"] = 1
                        # Sync combat status effects (poison, debuffs) back to character
                        combat_statuses = p.get("status_effects", [])
                        # Convert combat-style statuses to character-style if needed
                        from core.status_effects import add_poison, get_status_effects
                        for cs in combat_statuses:
                            if cs.get("name") == "Poison" and cs.get("duration", 0) > 0:
                                add_poison(char, "poison_weak")
                self.start_post_combat()
            else:
                # DEFEAT — TPK handling
                # All characters wake at 1 HP with resurrection sickness at last inn
                for c in self.party:
                    c.resources["HP"] = 1
                    # Lose 25% of gold
                    c.gold = int(c.gold * 0.75)
                from core.status_effects import add_resurrection_sickness
                for c in self.party:
                    add_resurrection_sickness(c)
                # Return to town
                self.dungeon_state = None
                self.dungeon_ui = None
                self.town_ui = TownUI(self.party)
                self.town_ui.inn_result = "Your party has fallen... You awaken at the inn, battered and bruised. (25% gold lost)"
                self.town_ui.view = self.town_ui.VIEW_INN
                self.go(S_TOWN)
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
        elif action["type"] == "switch_weapon":
            # Weapon switch — swap weapon in combatant and character, costs action
            item = action["item"]
            actor = self.combat_state.get_current_combatant()
            if actor:
                char_ref = actor.get("character_ref")
                if char_ref:
                    old_weapon = actor.get("weapon")
                    # Put old weapon back in inventory (if it's a real item, not starting)
                    if old_weapon and old_weapon.get("name") != "Unarmed":
                        old_copy = dict(old_weapon)
                        old_copy["type"] = "weapon"
                        old_copy["slot"] = "weapon"
                        char_ref.inventory.append(old_copy)
                    # Remove new weapon from inventory
                    if item in char_ref.inventory:
                        char_ref.inventory.remove(item)
                    # Equip new weapon on combatant
                    actor["weapon"] = dict(item)
                    self.combat_state.log.append(
                        f"{actor['name']} switches to {item.get('name', 'a weapon')}!"
                    )
                    # Advance turn (costs action)
                    self.combat_state._advance_turn()

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
        # Initialize world map and go there directly
        game.world_state = WorldState(game.party)
        game.world_map_ui = WorldMapUI(game.world_state)
        game.state = S_WORLD_MAP
        print("\n══════ DEBUG MODE ══════")
        print("Auto-generated party — exploring the world!")
        print("Arrow keys/WASD to move, ENTER on locations, C to camp")
        print("════════════════════════\n")

    game.run()
