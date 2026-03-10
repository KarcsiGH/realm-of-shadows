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
pygame.mixer.pre_init(22050, -16, 1, 1024)  # Must match core/sound.py SR=22050, mono
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
from ui.chest_ui import ChestUI
from ui.world_map_ui import WorldMapUI
from ui.dungeon_ui import DungeonUI
from data.world_map import (WorldState, LOCATIONS, LOC_TOWN, LOC_DUNGEON,
                            LOC_PORT, LOC_SECRET, LOC_POI, LOC_STABLE, LOC_RAIL)
from data.dungeon import DungeonState, DUNGEONS
from core.save_load import save_game, load_game
import core.sound as sfx

FPS = 60
PARTY_SIZE = 6

# States
S_TITLE       = 0
S_MODE        = 1
S_NAME        = 2
S_RACE        = 16  # race selection (new)
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
S_CAMP        = 22   # full camp screen (dungeon/overworld)
S_CHEST       = 17   # chest loot assignment screen
S_ATTACK_CINEMATIC = 18  # Act 1 climax: shadow attack on Briarhollow
S_ENDING           = 19  # Epilogue / credits after Valdris defeated
S_GAME_OVER        = 20  # Party wipe screen before returning to title
S_SETTINGS         = 21  # Volume / settings overlay
S_INN_RECRUIT      = 23  # Inn: recruit 5 companions after hero creation
S_SPELL_PICK       = 24  # Choose starting spell for Mage/Cleric/spellcasters


class Game:
    def __init__(self):
        self.screen = self._create_window()
        pygame.display.set_caption("Realm of Shadows")
        self.clock = pygame.time.Clock()
        self.running = True
        sfx.init()  # Initialize sound system
        sfx.load_settings()  # Apply saved volume settings
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
        # Chest loot screen
        self.chest_ui = None
        self.chest_return_state = S_DUNGEON
        # Inventory
        self.inventory_ui = None
        self.inventory_return_state = S_PARTY
        # Settings overlay
        self.settings_ui = None
        self._settings_return_state = S_PARTY
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
        self._post_combat_town = None  # if set, post-combat routes to this town
        # Camp screen
        self.camp_ui = None
        self.camp_return_state = None
        # Quest log
        self.quest_log_ui = None
        self._toasts = []   # [(message, color, timer_ms, max_timer_ms)]
        self._quest_notifications = []  # queue of {name, gold, xp, timer, max_timer}
        # Track current/last town for shortcuts
        self.current_town_id = "briarhollow"
        # Debug
        self.debug_mode = False
        self.debug_encounter = "tutorial"
        self.debug_enc_hover = -1

    def _create_window(self):
        """Create display surface based on saved display_mode preference."""
        try:
            import core.sound as sfx_mod
            sfx_mod.load_settings()
            mode = sfx_mod.get_display_mode()
        except Exception:
            mode = "windowed"
        try:
            if mode == "fullscreen":
                return pygame.display.set_mode((SCREEN_W, SCREEN_H),
                                               pygame.FULLSCREEN | pygame.SCALED)
            elif mode == "1280x800":
                return pygame.display.set_mode((1280, 800), pygame.SCALED)
            else:
                return pygame.display.set_mode((SCREEN_W, SCREEN_H))
        except Exception:
            return pygame.display.set_mode((SCREEN_W, SCREEN_H))

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
                try:
                    self.on_event(e, mx, my)
                except Exception as _exc:
                    self._show_crash(_exc)
                    return
            self.screen.fill(BG_COLOR)
            try:
                self.draw_state(mx, my)
            except Exception as _exc:
                self._show_crash(_exc)
                return
            # Journal overlay — never draw on top of active dialogue
            if self.quest_log_ui and not self._is_dialogue_active():
                try:
                    self.quest_log_ui.draw(self.screen, mx, my)
                except Exception:
                    pass
            self._draw_toasts(self.screen)
            self._draw_quest_banner(self.screen, dt)
            self._tick_toasts(dt)
            # Fade
            if self.fade > 0:
                s = pygame.Surface((SCREEN_W, SCREEN_H)); s.fill(BLACK)
                s.set_alpha(self.fade); self.screen.blit(s, (0,0))
                self.fade = max(0, self.fade - 10)
            pygame.display.flip()
        pygame.quit()

    def _show_crash(self, exc):
        """Display a readable crash screen with full traceback instead of silent close."""
        import traceback as _tb
        tb_str = _tb.format_exc()
        print("\n\n--- CRASH ---")
        print(tb_str)
        # Write to crash log
        try:
            import os, datetime
            log_dir = os.path.expanduser("~/Documents/RealmOfShadows")
            os.makedirs(log_dir, exist_ok=True)
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            log_path = os.path.join(log_dir, f"crash_{ts}.log")
            with open(log_path, "w") as f:
                f.write(f"State: {self.state}\n")
                f.write(f"Party size: {len(self.party)}\n\n")
                f.write(tb_str)
            print(f"Crash log written to: {log_path}")
        except Exception:
            pass
        # Show on-screen error panel for 10 seconds
        try:
            self.screen.fill((8, 4, 16))
            lines = tb_str.strip().split("\n")
            font = pygame.font.SysFont("courier,monospace", 13)
            y = 20
            draw_text(self.screen, "CRASH — please share the log file with the developer",
                      20, y, (255, 80, 80), 16, bold=True)
            y += 36
            for line in lines[-30:]:   # last 30 lines of traceback
                surf = font.render(line[:120], True, (200, 180, 160))
                self.screen.blit(surf, (20, y))
                y += 16
                if y > SCREEN_H - 40:
                    break
            draw_text(self.screen, "Window will close in 10 seconds",
                      20, SCREEN_H - 30, (150, 130, 120), 13)
            pygame.display.flip()
            pygame.time.wait(10000)
        except Exception:
            pass
        pygame.quit()

    def go(self, state):
        self.state = state
        self.fade = 120
        self.timer = 0
        # Ambient sound management on state change
        if state == S_TOWN:
            sfx.stop_music()
            sfx.stop_ambient()
            sfx.play_music("town_ambient")   # town music on main music channel
            sfx.play_ambient("town_env")     # soft crowd/bell ambience layer
        elif state == S_WORLD_MAP:
            sfx.stop_music()
            sfx.stop_ambient()
            sfx.play_ambient("world_ambient")
            self._sync_flag_keys()
        elif state == S_DUNGEON:
            sfx.stop_music()
            sfx.stop_ambient()
            sfx.play_ambient("dungeon_ambient")
        elif state == S_COMBAT:
            sfx.stop_ambient()
            sfx.stop_music()
            sfx.play("combat_start")
        elif state in (S_PARTY, S_POST_COMBAT):
            sfx.stop_music()
            sfx.stop_ambient()

    def go_fade(self, state):
        """Fade-out current screen, switch state, then fade-in."""
        # Fade out over ~200ms (20 frames at 60fps, step 13/frame)
        mx, my = pygame.mouse.get_pos()
        for alpha in range(0, 256, 13):
            self.screen.fill(BG_COLOR)
            self.draw_state(mx, my)
            s = pygame.Surface((SCREEN_W, SCREEN_H))
            s.fill(BLACK)
            s.set_alpha(min(255, alpha))
            self.screen.blit(s, (0, 0))
            pygame.display.flip()
            self.clock.tick(FPS)
        self.go(state)

    # ══════════════════════════════════════════════════════════
    #  EVENT HANDLING
    # ══════════════════════════════════════════════════════════

    def on_event(self, e, mx, my):
        # ── Quest banner dismissal (any click/key dismisses front banner) ──
        if self._quest_notifications:
            if e.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                self._dismiss_quest_banner()
                return
        # ── Global UI sounds ─────────────────────────────────────────
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            sfx.play("ui_click")
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                sfx.play("ui_cancel")
            elif e.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                sfx.play("ui_confirm")
        # ─────────────────────────────────────────────────────────────
        # ── Global journal overlay (J key, any state with a party) ───
        if not self._is_dialogue_active():
            if e.type == pygame.KEYDOWN and e.key == pygame.K_j and self.party:
                self._open_journal()
                return
            if self._handle_journal_event(e, mx, my):
                return

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
                    # Go to race selection
                    self.race_scroll = 0
                    self.race_hover = -1
                    self.human_stat_pick = None
                    self.go(S_RACE)
                elif e.key == pygame.K_BACKSPACE:
                    self.name_text = self.name_text[:-1]
                elif e.key == pygame.K_ESCAPE:
                    self.go(S_MODE)
                elif len(self.name_text) < 20 and e.unicode.isprintable():
                    self.name_text += e.unicode

        elif self.state == S_RACE:
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 4:
                    self.race_scroll = max(0, self.race_scroll - 1)
                elif e.button == 5:
                    from core.races import RACE_ORDER
                    max_scroll = max(0, len(RACE_ORDER) - 5)
                    self.race_scroll = min(max_scroll, self.race_scroll + 1)
                elif e.button == 1:
                    from core.races import RACE_ORDER, RACES
                    if self.human_stat_pick:
                        # Human stat pick mode — check stat buttons
                        from core.classes import STAT_NAMES
                        for i, stat in enumerate(STAT_NAMES):
                            bx = 360 + (i % 3) * 130
                            by = 440 + (i // 3) * 50
                            r = pygame.Rect(bx, by, 110, 40)
                            if r.collidepoint(mx, my):
                                self.current_char.human_bonus_stat = stat
                                self.current_char.stats[stat] = self.current_char.stats.get(stat, 5) + 1
                                self._after_race_picked()
                                break
                    elif self.race_hover >= 0 and self.race_hover < len(RACE_ORDER):
                        race_name = RACE_ORDER[self.race_hover]
                        if race_name == "Human":
                            self.human_stat_pick = True
                            self.current_char.race_name = "Human"
                        else:
                            self.current_char.race_name = race_name
                            self._after_race_picked()
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.human_stat_pick = None
                self.go(S_NAME)

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
                    # Route through spell-pick only for full character creation (not quick-roll)
                    # and only for classes with 3+ L1 spell options
                    from core.abilities import CLASS_ABILITIES
                    all_l1 = [a for a in CLASS_ABILITIES.get(cn, []) if a.get("level") == 1]
                    if not self.quick and len(all_l1) > 2:
                        from core.classes import CLASSES as _CLS
                        start_names = [a["name"] for a in _CLS.get(cn, {}).get("starting_abilities", [])]
                        self.spell_pick_pool = all_l1
                        self.spell_pick_chosen = list(start_names)
                        self.spell_pick_hover = -1
                        self.go(S_SPELL_PICK)
                    else:
                        self.go(S_SUMMARY)

        elif self.state == S_SPELL_PICK:
            pool = getattr(self, "spell_pick_pool", [])
            chosen = getattr(self, "spell_pick_chosen", [])
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                start_y = 160
                for i, ab in enumerate(pool):
                    btn = pygame.Rect(SCREEN_W//2 - 280, start_y + i * 80, 560, 72)
                    if btn.collidepoint(mx, my):
                        name = ab["name"]
                        if name in chosen:
                            if len(chosen) > 1:
                                chosen.remove(name)
                        else:
                            if len(chosen) < 2:
                                chosen.append(name)
                            else:
                                chosen.pop(0)
                                chosen.append(name)
                        self.spell_pick_chosen = chosen
                        break
                r_confirm = pygame.Rect(SCREEN_W//2 - 100, SCREEN_H - 65, 200, 45)
                if r_confirm.collidepoint(mx, my) and len(chosen) >= 1:
                    from core.abilities import CLASS_ABILITIES
                    from core.classes import CLASSES as _CLS2
                    cn = self.current_char.class_name
                    all_l1 = [a for a in CLASS_ABILITIES.get(cn, []) if a.get("level") == 1]
                    # Remove starting L1 abilities by name, then add chosen ones
                    all_l1_names = {a["name"] for a in all_l1}
                    non_starting = [a for a in self.current_char.abilities
                                    if a["name"] not in all_l1_names]
                    selected = [a for a in all_l1 if a["name"] in chosen]
                    self.current_char.abilities = non_starting + selected
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
                        from core.story_flags import has
                        if not has("intro_seen"):
                            self._start_opening()
                        else:
                            self.go(S_PARTY)
                    elif self.char_index == 1:
                        # Hero created — now recruit companions from the Inn
                        self._gen_inn_recruits()
                        self._gen_tavern_recruits()  # also pre-roll tavern pool
                        self.inn_selected = set()
                        self.inn_max_flash = 0.0
                        self.inn_hover = -1
                        self.go(S_INN_RECRUIT)
                    else:
                        self.go(S_MODE)
                elif r_redo.collidepoint(mx, my):
                    self.go(S_MODE)

        elif self.state == S_INN_RECRUIT:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                self._handle_inn_click(mx, my)

        elif self.state == S_PARTY:
            if e.type == pygame.MOUSEBUTTONDOWN:
                # Quest log overlay
                if self.quest_log_ui:
                    if e.button == 1:
                        result = self.quest_log_ui.handle_click(mx, my)
                        if result == "close" or self.quest_log_ui.finished:
                            self.quest_log_ui = None
                    elif e.button == 4:
                        self.quest_log_ui.handle_scroll(-1, mx, my)
                    elif e.button == 5:
                        self.quest_log_ui.handle_scroll(1, mx, my)
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
                        sfx.play("ui_open")
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
                            self.town_ui = TownUI(self.party, town_id=self.current_town_id)
                            self.go_fade(S_TOWN)
                            return
                    # Save button
                    save_btn = pygame.Rect(20, 40, 120, 40)
                    if save_btn.collidepoint(mx, my) and self.party:
                        ok, path, msg = save_game(self.party,
                                                  world_state=self.world_state)
                        self.save_msg = msg
                        self.save_msg_color = GREEN if ok else RED
                        self.save_msg_timer = 3000
                        toast_col = (80, 200, 120) if ok else (220, 80, 80)
                        toast_msg = "✓ Game saved." if ok else f"✗ Save failed: {msg}"
                        self.add_toast(toast_msg, toast_col)
                        return
                    # Load button
                    load_btn = pygame.Rect(150, 40, 120, 40)
                    if load_btn.collidepoint(mx, my):
                        ok, party, world_state, msg = load_game()
                        if ok:
                            self.party = party
                            if world_state:
                                self.world_state = world_state
                                self.world_state.party = self.party
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
                            self.go_fade(S_DUNGEON)
                        else:
                            self._init_world_map()
                            self.go_fade(S_WORLD_MAP)
                        return
                    # Settings button
                    settings_btn = pygame.Rect(20, 88, 120, 32)
                    if settings_btn.collidepoint(mx, my):
                        from ui.settings_ui import SettingsUI
                        self.settings_ui = SettingsUI()
                        self._settings_return_state = S_PARTY
                        sfx.play("ui_open")
                        self.go(S_SETTINGS)
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
                            self._init_world_map()
                            self.go_fade(S_WORLD_MAP)

        elif self.state == S_INVENTORY:
            # Pass keyboard events (ESC)
            if e.type == pygame.KEYDOWN:
                result = self.inventory_ui.handle_event(e)
                if result == "back":
                    sfx.play("ui_close")
                    self.go(self.inventory_return_state)
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button in (1, 2, 3):  # left, middle, or right click
                    result = self.inventory_ui.handle_click(mx, my, button=e.button)
                    if result == "back":
                        sfx.play("ui_close")
                        self.go(self.inventory_return_state)
                elif e.button == 4:
                    self.inventory_ui.handle_scroll(-1)
                elif e.button == 5:
                    self.inventory_ui.handle_scroll(1)

        elif self.state == S_CHEST:
            if self.chest_ui:
                if e.type == pygame.KEYDOWN:
                    result = self.chest_ui.handle_event(e)
                    if self.chest_ui.finished:
                        self.chest_ui = None
                        self._fire_chest_hint_if_pending()
                        self.go(self.chest_return_state)
                elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    result = self.chest_ui.handle_click(mx, my)
                    if self.chest_ui.finished:
                        self.chest_ui = None
                        self._fire_chest_hint_if_pending()
                        self.go(self.chest_return_state)

        elif self.state == S_TOWN:
            if e.type == pygame.KEYDOWN:
                # Forward keyboard to town UI (for walkable movement)
                result = self.town_ui.handle_key(e.key)
                if result == "exit":
                    self._init_world_map()
                    self.go_fade(S_WORLD_MAP)
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    result = self.town_ui.handle_click(mx, my)
                    if result == "exit":
                        self._init_world_map()
                        self.go_fade(S_WORLD_MAP)
                    elif result == "inn_save":
                        # Auto-save when resting at inn
                        try:
                            ok, _path, _msg = save_game(
                                self.party,
                                world_state=self.world_state,
                                slot_name="inn_autosave"
                            )
                            toast_col = (80, 200, 120) if ok else (220, 80, 80)
                            toast_msg = "✓ Progress saved at inn." if ok else "✗ Autosave failed."
                            self.add_toast(toast_msg, toast_col)
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
            elif e.type == pygame.KEYUP:
                if hasattr(self.dungeon_ui, 'handle_keyup'):
                    self.dungeon_ui.handle_keyup(e.key)
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
                        sfx.play("ui_open")
                        self.go(S_INVENTORY)
                        return
                    result = self.post_combat_ui.handle_click(mx, my)
                    if result == "continue":
                        self.party_scroll = 0
                        # Special routing: story combat that drops into a town
                        if getattr(self, "_post_combat_town", None):
                            town_id = self._post_combat_town
                            self._post_combat_town = None
                            self.town_ui = TownUI(self.party, town_id=town_id)
                            self.go_fade(S_TOWN)
                        elif self.dungeon_state:
                            self.go_fade(S_DUNGEON)
                        elif self.world_state:
                            self.go_fade(S_WORLD_MAP)
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

        elif self.state == S_ATTACK_CINEMATIC:
            self._handle_attack_cinematic_input(e)
        elif self.state == S_ENDING:
            self._handle_ending_input(e)
        elif self.state == S_GAME_OVER:
            self._handle_game_over_input(e)

        elif self.state == S_SETTINGS:
            if self.settings_ui:
                result = self.settings_ui.handle_event(e)
                if result == "close" or self.settings_ui.finished:
                    self.settings_ui = None
                    sfx.play("ui_close")
                    self.go(self._settings_return_state)

        elif self.state == S_CAMP:
            if self.camp_ui:
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    result = self.camp_ui.handle_click(mx, my)
                    if self.camp_ui.finished:
                        self._end_camp()
                elif e.type == pygame.KEYDOWN:
                    result = self.camp_ui.handle_key(e.key)
                    if self.camp_ui and self.camp_ui.finished:
                        self._end_camp()

    # ══════════════════════════════════════════════════════════
    #  LOGIC
    # ══════════════════════════════════════════════════════════


    # ══════════════════════════════════════════════════════════
    #  JOURNAL / TOAST HELPERS
    # ══════════════════════════════════════════════════════════

    def _is_dialogue_active(self):
        """Return True if an NPC dialogue or dedicated dialogue state is on screen."""
        if self.state == S_DIALOGUE:
            return True
        if (self.state == S_TOWN and hasattr(self, "town_ui") and
                self.town_ui is not None and
                getattr(self.town_ui, "active_dialogue", None) is not None and
                not self.town_ui.active_dialogue.finished):
            return True
        return False

    def _open_journal(self):
        """Open the quest log overlay (from any game state)."""
        if not self.party:
            return
        if self._is_dialogue_active():
            return   # never open journal over dialogue
        if self.quest_log_ui:
            self.quest_log_ui = None   # toggle off
        else:
            from ui.quest_log_ui import QuestLogUI
            self.quest_log_ui = QuestLogUI()
            sfx.play("ui_open")

    def _handle_journal_event(self, e, mx, my):
        """Handle all input for the quest-log overlay. Returns True if consumed."""
        if not self.quest_log_ui:
            return False
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                result = self.quest_log_ui.handle_click(mx, my)
                if result == "close" or self.quest_log_ui.finished:
                    self.quest_log_ui = None
            elif e.button == 4:
                self.quest_log_ui.handle_scroll(-1, mx, my)
            elif e.button == 5:
                self.quest_log_ui.handle_scroll(1, mx, my)
            return True
        if e.type == pygame.KEYDOWN and e.key in (pygame.K_ESCAPE, pygame.K_j):
            self.quest_log_ui = None
            return True
        return True   # swallow all input while overlay is open

    def add_toast(self, message, color=None):
        """Queue a toast notification (e.g. 'New Quest: …')."""
        from ui.renderer import GOLD
        self._toasts.append([message, color or GOLD, 3500, 3500])

    def _draw_toasts(self, surface):
        """Draw all active toasts; called at the very end of every draw."""
        import pygame
        from ui.renderer import draw_text, get_font, SCREEN_W
        y = 8
        for toast in self._toasts[:]:
            msg, col, timer, max_t = toast
            alpha = min(255, int(255 * min(timer, max_t - timer * 0.3) / (max_t * 0.3)))
            alpha = max(60, min(255, alpha))
            font = get_font(13)
            tw = font.size(msg)[0]
            bg = pygame.Surface((tw + 24, 28), pygame.SRCALPHA)
            bg.fill((8, 6, 18, min(220, alpha)))
            bx = SCREEN_W // 2 - (tw + 24) // 2
            surface.blit(bg, (bx, y))
            pygame.draw.rect(surface, col, (bx, y, tw + 24, 28), 1, border_radius=3)
            draw_text(surface, msg, bx + 12, y + 6, col, 13)
            y += 32

    def _tick_toasts(self, dt):
        """Advance toast timers each frame."""
        self._toasts = [t for t in self._toasts if t[2] > 0]
        for t in self._toasts:
            t[2] -= dt

    def _notify_quests_done(self, quest_ids):
        """Queue a prominent banner for each newly-completed quest."""
        if not quest_ids:
            return
        from data.story_data import QUESTS
        for qid in quest_ids:
            q = QUESTS.get(qid, {})
            name  = q.get("name", qid)
            gold  = q.get("reward_gold", 0)
            xp    = q.get("reward_xp", 0)
            items = q.get("reward_items", [])
            self._quest_notifications.append({
                "name":      name,
                "gold":      gold,
                "xp":        xp,
                "items":     items,
                "timer":     7000,
                "max_timer": 7000,
                "slide":     0.0,
                "kind":      "quest",
            })

    def _notify_tier_up(self, tier_info):
        """Queue a tier advancement banner using the quest notification system."""
        self._quest_notifications.append({
            "name":       f"{tier_info['name']} Tier",
            "gold":       0,
            "xp":         0,
            "items":      [],
            "timer":      6000,
            "max_timer":  6000,
            "slide":      0.0,
            "kind":       "tier",
            "tier_color": tier_info["color"],
            "tier_desc":  tier_info["description"],
        })

    def _draw_quest_banner(self, surface, dt):
        """Draw the front-of-queue quest completion banner and tick its timer.
        Shows one at a time; auto-advances to next when dismissed."""
        import math
        if not self._quest_notifications:
            return

        n = self._quest_notifications[0]
        n["timer"] -= dt

        # Slide in over 200 ms, slide out over 300 ms at end
        if n["timer"] > n["max_timer"] - 200:
            t = (n["max_timer"] - n["timer"]) / 200.0
        elif n["timer"] < 350:
            t = n["timer"] / 350.0
        else:
            t = 1.0
        t = max(0.0, min(1.0, t))
        ease = t * t * (3 - 2 * t)  # smoothstep

        if n["timer"] <= 0:
            self._quest_notifications.pop(0)
            return

        from ui.renderer import (
            SCREEN_W, SCREEN_H, draw_text, get_font,
            GOLD, CREAM, GREY, PANEL_BG,
        )

        is_tier = n.get("kind") == "tier"
        accent  = n.get("tier_color", (60, 200, 100)) if is_tier else (60, 220, 120)

        # Build reward lines first so we know height
        reward_lines = []
        if not is_tier:
            if n["xp"]:
                reward_lines.append((f"+{n['xp']} XP", (120, 200, 255)))
            if n["gold"]:
                reward_lines.append((f"+{n['gold']} gold", (220, 190, 80)))
            for item in n["items"]:
                iname = item.get("name", "") if isinstance(item, dict) else str(item)
                if iname:
                    reward_lines.append((f"Item: {iname}", (200, 160, 255)))

        # Panel sizing: taller for quests with rewards
        PW = 520
        PH = 80 + max(len(reward_lines), 1) * 26 + 50
        if is_tier:
            PH = 160

        px = SCREEN_W // 2 - PW // 2
        # Slide down from above center
        py_hidden = -PH - 10
        py_shown  = SCREEN_H // 2 - PH // 2 - 30
        py = int(py_hidden + (py_shown - py_hidden) * ease)

        # Dim overlay behind the panel
        overlay = pygame.Surface((PW + 60, PH + 60), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 110))
        surface.blit(overlay, (px - 30, py - 30))

        # Panel background
        panel = pygame.Surface((PW, PH), pygame.SRCALPHA)
        panel.fill((10, 8, 26, 245))
        surface.blit(panel, (px, py))

        # Gold border + thick accent top bar
        pygame.draw.rect(surface, GOLD, (px, py, PW, PH), 2, border_radius=8)
        pygame.draw.rect(surface, accent, (px, py, PW, 6), border_radius=8)

        # Header label
        if is_tier:
            header = "\u2726  TIER ADVANCE  \u2726"
        else:
            header = "\u2726  QUEST COMPLETE  \u2726"
        hw = get_font(15).size(header)[0]
        draw_text(surface, header, px + (PW - hw) // 2, py + 14, accent, 15, bold=True)

        # Quest / tier name — centered, large
        font_name = get_font(20)
        name_text = n["name"]
        while font_name.size(name_text)[0] > PW - 40:
            name_text = name_text[:-4] + "\u2026"
        nw = font_name.size(name_text)[0]
        draw_text(surface, name_text, px + (PW - nw) // 2, py + 38,
                  GOLD if not is_tier else accent, 20, bold=True)

        # Separator line
        sep_y = py + 68
        pygame.draw.line(surface, (60, 50, 80), (px + 20, sep_y), (px + PW - 20, sep_y))

        # Body — tier desc or reward lines
        ry = sep_y + 10
        if is_tier:
            desc = n.get("tier_desc", "")
            draw_text(surface, desc, px + 20, ry, CREAM, 13, max_width=PW - 40)
        elif reward_lines:
            draw_text(surface, "Rewards:", px + 20, ry, GREY, 13)
            rx = px + 100
            for text, col in reward_lines:
                tw = get_font(14).size(text)[0]
                if rx + tw > px + PW - 20:
                    rx = px + 100
                    ry += 24
                draw_text(surface, text, rx, ry, col, 14, bold=True)
                rx += tw + 20
        else:
            draw_text(surface, "Objectives fulfilled.", px + 20, ry, GREY, 13)

        # Dismiss hint at bottom
        hint = "[ click anywhere or press any key to continue ]"
        hw2 = get_font(11).size(hint)[0]
        draw_text(surface, hint, px + (PW - hw2) // 2, py + PH - 18, (80, 80, 110), 11)

    def _dismiss_quest_banner(self):
        """Dismiss the front banner early (on click/keypress)."""
        if self._quest_notifications:
            self._quest_notifications.pop(0)

    def new_char(self):
        self.current_char = Character()
        self.current_char.quick_rolled = self.quick
        self.name_text = ""
        self.history = []
        self.race_scroll = 0
        self.race_hover = -1
        self.human_stat_pick = None

    def _after_race_picked(self):
        """Called after race is selected — proceed to lifepath or class select."""
        self.human_stat_pick = None
        if self.quick:
            self.setup_class_choices()
            self.go(S_CLASSSELECT)
        else:
            self.slot = 1
            self.history = []
            self.setup_slot_choices()
            self.go(S_LIFEPATH)

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
    #  INN RECRUITMENT
    # ══════════════════════════════════════════════════════════

    _INN_NAMES = [
        ("Brom","Male"),("Syla","Female"),("Garrett","Male"),("Enna","Female"),
        ("Torvin","Male"),("Mira","Female"),("Cade","Male"),("Vesna","Female"),
        ("Aldus","Male"),("Kyra","Female"),("Renn","Male"),("Shael","Female"),
        ("Dax","Male"),("Lira","Female"),("Wulf","Male"),("Asha","Female"),
    ]
    _INN_BLURBS = {
        "Fighter":    ["Veteran of the Border Wars, looking for steady work.",
                       "Ex-city-guard, left after seeing too much corruption.",
                       "Raised in the fighting pits, knows no other life."],
        "Mage":       ["Left the Academy before graduation — too many rules.",
                       "Discovered a talent for fire; now no guild will have them.",
                       "Studies ancient runes in their spare time."],
        "Cleric":     ["Wandering priest of the Old Faith, oath of service.",
                       "Left the monastery to see what the gods really want.",
                       "Carries a relic of uncertain holiness."],
        "Thief":      ["Claims to be a retired locksmith. Nobody believes it.",
                       "Owes a debt to someone dangerous; adventure is the way out.",
                       "Light fingers, quick feet, questionable morals."],
        "Ranger":     ["Spent ten years mapping the Ashwood alone.",
                       "Follows a trail only they can read.",
                       "Their wolf companion died last winter; haven't been the same."],
        "Monk":       ["Seven years in a mountain monastery, now seeking truth outside it.",
                       "Practices a forbidden martial form banned by the temples.",
                       "Quiet, fast, and terrifyingly calm in a fight."],
        "Paladin":    ["Champion of a fallen order, still holding to the oath.",
                       "Blessed by a god who never speaks to them directly.",
                       "Believes deeply in justice; has a flexible definition of it."],
        "Assassin":   ["Won't say who trained them. Won't say who they've killed.",
                       "Claims to be a traveling merchant. The blades suggest otherwise.",
                       "Retired from the guild; the guild hasn't agreed yet."],
        "Warden":     ["Protector of a forest that no longer exists.",
                       "Their shield has stopped a hundred blows. The dents prove it.",
                       "Slow to anger, devastating when it arrives."],
        "Warder":     ["Last survivor of a legendary warband.",
                       "Carries a chip in their axe from the night everything went wrong."],
        "Spellblade": ["Taught themselves to weave magic into swordplay. Painfully.",
                       "Expelled from both the mages' college and the fighters' guild."],
        "Templar":    ["Holy warrior. The holy part is debatable.",
                       "Wears faith like armor. Also wears actual armor."],
        "Witch":      ["Collects odd herbs and odder secrets.",
                       "The townsfolk made them leave. Their loss."],
        "Necromancer":["Academic interest in the undead. Purely academic.",
                       "The smell follows them everywhere. They've stopped noticing."],
    }

    def _gen_inn_recruits(self):
        """Generate 16 pre-rolled adventurers available at the Inn (4×4 grid)."""
        from core.character import Character
        from core.classes import CLASS_ORDER
        from core.races import RACE_ORDER
        import random

        TOTAL = 16
        hero_class = self.party[0].class_name if self.party else None
        pool = [c for c in CLASS_ORDER if c != hero_class]   # 5 non-hero classes
        all_races = list(RACE_ORDER)   # all 7 races

        # Strategy: 16 slots total.
        # — Each non-hero class appears at least twice (5×2 = 10 slots)
        # — Fill remaining 6 with random picks from pool (good class spread)
        chosen_classes = pool * 2                              # each class ×2 = 10
        extras = [random.choice(pool) for _ in range(TOTAL - len(chosen_classes))]
        chosen_classes = chosen_classes + extras               # 16 total
        random.shuffle(chosen_classes)

        # Race assignment: every race at least once (7 races),
        # fill remaining 9 slots randomly.
        race_pool = all_races[:]
        extras_r  = [random.choice(all_races) for _ in range(TOTAL - len(race_pool))]
        race_assignments = race_pool + extras_r
        random.shuffle(race_assignments)

        used_names = set()
        self.inn_recruits = []
        name_pool = list(self._INN_NAMES)
        random.shuffle(name_pool)

        for cls, race in zip(chosen_classes, race_assignments):
            for name, _ in name_pool:
                if name not in used_names:
                    used_names.add(name)
                    break
            c = Character(name, race_name=race)
            c.quick_roll(cls)
            blurbs = self._INN_BLURBS.get(cls, ["A seasoned adventurer seeking work."])
            c.inn_blurb = random.choice(blurbs)
            self.inn_recruits.append(c)

    def _gen_tavern_recruits(self):
        """Generate 6 tavern adventurers via quick_roll — same quality as inn recruits.
        Injects them into TAVERN['recruits'] as stat dicts so town_ui can render them."""
        from core.character import Character
        from core.classes import CLASS_ORDER
        from core.races import RACE_ORDER
        from data.shop_inventory import TAVERN
        import random

        # Names distinct from inn pool
        TAVERN_NAMES = [
            ("Oswyn", "Male"), ("Verryn", "Female"), ("Harken", "Male"),
            ("Sable", "Female"), ("Dunric", "Male"), ("Lisse", "Female"),
            ("Bael", "Male"), ("Corva", "Female"),
        ]
        TAVERN_COLORS = {
            "Fighter": (210, 120, 80), "Mage": (120, 160, 240),
            "Cleric":  (220, 200, 100), "Thief": (140, 200, 130),
            "Ranger":  (100, 180, 120), "Monk": (200, 160, 220),
        }

        used = set(m.name for m in self.party) | \
               set(c.name for c in getattr(self, "inn_recruits", []))

        pool = list(CLASS_ORDER)
        races = list(RACE_ORDER)
        random.shuffle(pool)
        random.shuffle(races)

        # 6 recruits: one per class for the first 6 classes, shuffled
        classes_6 = (pool * 2)[:6]
        random.shuffle(classes_6)
        races_6 = (races * 2)[:6]
        random.shuffle(races_6)

        name_pool = [n for n in TAVERN_NAMES if n[0] not in used]
        random.shuffle(name_pool)

        recruits = []
        for i, (cls, race) in enumerate(zip(classes_6, races_6)):
            name = name_pool[i % len(name_pool)][0] if name_pool else f"Wanderer {i+1}"
            c = Character(name, race_name=race)
            c.quick_roll(cls)
            blurbs = self._INN_BLURBS.get(cls, ["Looking for work."])
            color = TAVERN_COLORS.get(cls, (160, 150, 160))
            recruits.append({
                "name":       c.name,
                "class_name": cls,
                "race_name":  race,
                "level":      1,
                "color":      color,
                "pitch":      random.choice(blurbs),
                "hire_cost":  0,
                "stats":      dict(c.stats),
                "_char":      c,   # keep the Character object for full hire
            })

        TAVERN["recruits"] = recruits

    def _handle_inn_click(self, mx, my):
        """Handle clicks on the Inn recruitment screen."""
        from core.classes import CLASSES
        SCREEN_W = pygame.display.get_surface().get_width()
        SCREEN_H = pygame.display.get_surface().get_height()
        NEED = 5

        # Recruit cards layout: 4 per row, 4 rows (16 recruits)
        card_w, card_h = 338, 148
        cols = 4
        gap_x, gap_y = 10, 6
        start_x = (SCREEN_W - cols * (card_w + gap_x)) // 2
        start_y = 102

        for i, c in enumerate(self.inn_recruits):
            col = i % cols
            row = i // cols
            rx = start_x + col * (card_w + gap_x)
            ry = start_y + row * (card_h + gap_y)
            r = pygame.Rect(rx, ry, card_w, card_h)
            if r.collidepoint(mx, my):
                if i in self.inn_selected:
                    self.inn_selected.discard(i)
                    self.inn_max_flash = 0.0
                elif len(self.inn_selected) < NEED:
                    self.inn_selected.add(i)
                else:
                    self.inn_max_flash = 2.0  # flash "Party full" for 2 seconds
                return

        # Confirm button
        if len(self.inn_selected) == NEED:
            btn = pygame.Rect(SCREEN_W//2 - 160, SCREEN_H - 58, 320, 46)
            if btn.collidepoint(mx, my):
                for i in sorted(self.inn_selected):
                    self.party.append(self.inn_recruits[i])
                self.char_index = PARTY_SIZE  # set directly — don't increment per-recruit
                self.party_scroll = 0
                from core.story_flags import has
                if not has("intro_seen"):
                    self._start_opening()
                else:
                    self.go(S_PARTY)


    def _draw_inn_recruit(self, mx, my):
        """Draw the Inn recruitment screen — 16 candidates in a 4x4 grid."""
        from ui.renderer import (SCREEN_W, SCREEN_H, draw_text, draw_panel,
                                  draw_button, GOLD, CREAM, GREY, DARK_GREY,
                                  PANEL_BG, PANEL_BORDER, HIGHLIGHT, DIM_GOLD,
                                  GREEN, RED, ORANGE)
        from ui.pixel_art import draw_character_silhouette
        from core.classes import CLASSES, STAT_NAMES

        BG = (8, 6, 16)
        self.screen.fill(BG)

        draw_text(self.screen, "The Wanderer's Inn", SCREEN_W//2 - 140, 18,
                  GOLD, 26, bold=True)
        hero = self.party[0]
        draw_text(self.screen,
                  f"{hero.name} surveys the common room. Five companions are needed.",
                  SCREEN_W//2 - 310, 54, CREAM, 15)

        NEED = 5
        n_sel = len(self.inn_selected)
        sel_col = GREEN if n_sel == NEED else ORANGE
        draw_text(self.screen, f"Selected: {n_sel} / {NEED}",
                  SCREEN_W//2 - 55, 76, sel_col, 14, bold=True)

        # Cards — 4 columns x 4 rows to show all 16 recruits
        card_w, card_h = 338, 148
        cols = 4
        gap_x, gap_y = 10, 6
        start_x = (SCREEN_W - cols * (card_w + gap_x)) // 2
        start_y = 102

        for i, c in enumerate(self.inn_recruits):
            col_i = i % cols
            row_i = i // cols
            rx = start_x + col_i * (card_w + gap_x)
            ry = start_y + row_i * (card_h + gap_y)
            r = pygame.Rect(rx, ry, card_w, card_h)
            selected = (i in self.inn_selected)
            hover = r.collidepoint(mx, my)
            cls_data = CLASSES.get(c.class_name, {})
            cls_col = cls_data.get("color", (160, 150, 170))

            if selected:
                border = GREEN
                bg = (12, 28, 12)
            elif hover:
                border = cls_col
                bg = (22, 18, 35)
            else:
                border = PANEL_BORDER
                bg = PANEL_BG

            draw_panel(self.screen, r, bg_color=bg, border_color=border)

            # Portrait
            sil_r = pygame.Rect(rx + 4, ry + 4, 68, 90)
            draw_character_silhouette(self.screen, sil_r, c.class_name,
                                       highlight=selected or hover)

            # Name + race + class
            tx = rx + 82
            draw_text(self.screen, c.name, tx, ry + 4, cls_col, 13, bold=True)
            race_str = getattr(c, "race_name", "Human")
            draw_text(self.screen, f"{race_str}  {c.class_name}",
                      tx, ry + 19, CREAM, 11)

            # Stats — two rows of 3
            sy = ry + 34
            for si, stat in enumerate(["STR", "DEX", "CON", "INT", "WIS", "PIE"]):
                val = c.stats.get(stat, 0)
                col_v = GREEN if val >= 13 else (CREAM if val >= 9 else GREY)
                sx2 = tx + (si % 3) * 62
                sy2 = sy + (si // 3) * 15
                draw_text(self.screen, f"{stat}:{val}", sx2, sy2, col_v, 12)

            # Resources
            ry2 = sy + 34
            for rname, rval in list(c.resources.items())[:2]:
                draw_text(self.screen, f"{rname} {rval}", tx, ry2, DIM_GOLD, 11)
                ry2 += 11

            # Blurb
            blurb = getattr(c, "inn_blurb", "")
            if blurb:
                draw_text(self.screen, f'"{blurb}"',
                          rx + 6, ry + card_h - 22, GREY, 11,
                          max_width=card_w - 12)

            if selected:
                draw_text(self.screen, "✓", rx + card_w - 22, ry + 4,
                          GREEN, 14, bold=True)

        if n_sel == NEED:
            btn = pygame.Rect(SCREEN_W//2 - 160, SCREEN_H - 58, 320, 46)
            draw_button(self.screen, btn, "Set Forth Together!",
                        hover=btn.collidepoint(mx, my), size=17)
        else:
            rem = NEED - n_sel
            flash = getattr(self, "inn_max_flash", 0.0)
            if flash > 0:
                self.inn_max_flash = max(0.0, flash - (1 / 60))
                draw_text(self.screen, "Party full! Deselect someone first.",
                          SCREEN_W//2 - 145, SCREEN_H - 42, RED, 14, bold=True)
            else:
                draw_text(self.screen,
                          f"Choose {rem} more companion{'s' if rem != 1 else ''}.",
                          SCREEN_W//2 - 100, SCREEN_H - 42, CREAM, 15)


    def draw_state(self, mx, my):
        if self.state == S_TITLE:      self.draw_title()
        elif self.state == S_MODE:     self.draw_mode(mx, my)
        elif self.state == S_NAME:     self.draw_name()
        elif self.state == S_RACE:     self.draw_race(mx, my)
        elif self.state == S_LIFEPATH: self.draw_lifepath(mx, my)
        elif self.state == S_RANDOM:   self.draw_random()
        elif self.state == S_CLASSSELECT: self.draw_class(mx, my)
        elif self.state == S_SPELL_PICK:  self.draw_spell_pick(mx, my)
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
        elif self.state == S_CAMP:      self._draw_camp(mx, my)
        elif self.state == S_CHEST:     self._draw_chest(mx, my)
        elif self.state == S_ATTACK_CINEMATIC: self._draw_attack_cinematic(mx, my)
        elif self.state == S_ENDING:           self._draw_ending(mx, my)
        elif self.state == S_INN_RECRUIT:       self._draw_inn_recruit(mx, my)
        elif self.state == S_SETTINGS:         self._draw_settings(mx, my)
        elif self.state == S_GAME_OVER:        self._draw_game_over(mx, my)

    # ── Title Screen ──────────────────────────────────────────

    def draw_title(self):
        import math, random

        t = self.title_t / 1000.0

        # ── Animated starfield / mist background ──
        rng = random.Random(42)
        for _ in range(80):
            sx = rng.randint(0, SCREEN_W)
            sy = rng.randint(0, SCREEN_H)
            sr = rng.randint(1, 2)
            alpha = int(60 + 40 * math.sin(t * rng.uniform(0.4, 1.2) + rng.random() * 6))
            s = pygame.Surface((sr*2, sr*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (200, 180, 255, alpha), (sr, sr), sr)
            self.screen.blit(s, (sx - sr, sy - sr))

        # ── Fading tendrils from edges (title atmosphere) ──
        rng2 = random.Random(int(t * 1.5))
        tendril_surf = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        for i in range(12):
            ox = rng2.randint(0, SCREEN_W)
            length = rng2.randint(80, 200)
            px, py = float(ox), 0.0
            for step in range(length):
                jitter = rng2.uniform(-5, 5)
                nx = px + jitter
                ny = py + 1
                a  = max(0, int(90 * (1 - step / length)))
                pygame.draw.line(tendril_surf, (60, 0, 100, a),
                                 (int(px), int(py)), (int(nx), int(ny)), 2)
                px, py = nx, ny
        # Bottom tendrils reaching up
        for i in range(8):
            ox = rng2.randint(0, SCREEN_W)
            length = rng2.randint(60, 140)
            px, py = float(ox), float(SCREEN_H)
            for step in range(length):
                jitter = rng2.uniform(-4, 4)
                nx = px + jitter
                ny = py - 1
                a  = max(0, int(70 * (1 - step / length)))
                pygame.draw.line(tendril_surf, (80, 0, 120, a),
                                 (int(px), int(py)), (int(nx), int(ny)), 2)
                px, py = nx, ny
        self.screen.blit(tendril_surf, (0, 0))

        # ── Gradient atmosphere band across center ──
        band = pygame.Surface((SCREEN_W, 320), pygame.SRCALPHA)
        for i in range(320):
            d = abs(i - 160) / 160.0
            a = int(60 * (1 - d ** 1.5))
            pygame.draw.line(band, (20, 0, 40, a), (0, i), (SCREEN_W, i))
        self.screen.blit(band, (0, SCREEN_H // 2 - 200))

        # ── Logo ──
        pulse = abs((self.title_t % 3000) - 1500) / 1500.0   # 0→1→0
        r_col = (int(210 + 45 * pulse), int(180 + 30 * pulse), int(20 * pulse))
        s_col = (int(160 + 60 * pulse), int(130 + 50 * pulse), int(180 + 40 * pulse))

        # Soft glow behind "REALM"
        glow_alpha = int(40 + 30 * pulse)
        gw = pygame.Surface((360, 70), pygame.SRCALPHA)
        gw.fill((80, 20, 140, glow_alpha))
        self.screen.blit(gw, (SCREEN_W // 2 - 180, SCREEN_H // 2 - 105))

        draw_text(self.screen, "REALM",   SCREEN_W // 2 - 120, SCREEN_H // 2 - 90,
                  r_col, 52, bold=True)
        draw_text(self.screen, "of",      SCREEN_W // 2 - 22,  SCREEN_H // 2 - 28,
                  (180, 160, 220), 22)
        draw_text(self.screen, "SHADOWS", SCREEN_W // 2 - 160, SCREEN_H // 2 + 4,
                  s_col, 52, bold=True)

        # ── Tagline ──
        draw_text(self.screen, "The Fading comes for all things.",
                  SCREEN_W // 2 - 175, SCREEN_H // 2 + 80, (140, 110, 180), 15)

        # ── Blinking prompt ──
        if (self.title_t // 800) % 2 == 0:
            draw_text(self.screen, "Press any key to begin",
                      SCREEN_W // 2 - 130, SCREEN_H // 2 + 130, DIM_GOLD, 16)

        # ── Version / credit ──
        draw_text(self.screen, "An Advanced Class System RPG",
                  SCREEN_W // 2 - 160, SCREEN_H - 42, GREY, 14)

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
                  SCREEN_W//2 - 200, 418, GREY, 14)

        draw_button(self.screen, r2, "Quick Roll", hover=h2, size=18)
        draw_text(self.screen, "Pick a class and start immediately",
                  SCREEN_W//2 - 175, 498, GREY, 14)

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
                  SCREEN_W//2 - 120, 340, GREY, 15)

    # ── Race Selection ─────────────────────────────────────────

    def draw_race(self, mx, my):
        from core.races import RACES, RACE_ORDER
        from core.classes import STAT_NAMES, STAT_FULL_NAMES

        draw_text(self.screen, f"Choose {self.current_char.name}'s Race",
                  40, 25, GOLD, 22, bold=True)

        mode = "Quick Roll" if self.quick else "Life Path"
        draw_text(self.screen, f"Mode: {mode}",
                  40, 55, CREAM, 14)

        # If human stat pick mode — show stat selection
        if self.human_stat_pick:
            draw_text(self.screen, "Human — Choose a stat to boost (+1):",
                      SCREEN_W//2 - 200, 380, CREAM, 18)
            draw_text(self.screen, "Humans are versatile. Pick one attribute to enhance.",
                      SCREEN_W//2 - 240, 410, GREY, 14)
            for i, stat in enumerate(STAT_NAMES):
                bx = 360 + (i % 3) * 130
                by = 440 + (i // 3) * 50
                r = pygame.Rect(bx, by, 110, 40)
                hover = r.collidepoint(mx, my)
                draw_button(self.screen, r, f"+1 {STAT_FULL_NAMES[stat]}", hover=hover, size=13)

        # Race list
        start_y = 85
        item_h = 90
        visible = 5 if not self.human_stat_pick else 3
        self.race_hover = -1

        for i in range(visible):
            idx = self.race_scroll + i
            if idx >= len(RACE_ORDER):
                break
            race_name = RACE_ORDER[idx]
            race = RACES[race_name]
            rect = pygame.Rect(40, start_y + i * item_h, SCREEN_W - 80, item_h - 5)
            is_hover = rect.collidepoint(mx, my) and not self.human_stat_pick
            if is_hover:
                self.race_hover = idx

            bg = (45, 38, 75) if is_hover else PANEL_BG
            sel = race_name == getattr(self.current_char, "race_name", None) and self.human_stat_pick
            brd = race["color"] if (is_hover or sel) else PANEL_BORDER
            draw_panel(self.screen, rect, border_color=brd, bg_color=bg)

            # Race name
            draw_text(self.screen, race_name, rect.x + 12, rect.y + 8,
                      race["color"], 18, bold=True)

            # Stat mods
            mods = race.get("stat_mods", {})
            if mods:
                mod_parts = []
                for s, v in mods.items():
                    sign = "+" if v > 0 else ""
                    mod_parts.append(f"{sign}{v} {s}")
                mod_str = "  ".join(mod_parts)
            else:
                mod_str = "+1 to any stat (your choice)"
            draw_text(self.screen, mod_str, rect.x + 200, rect.y + 10,
                      HIGHLIGHT, 13)

            # Description
            draw_text(self.screen, race["description"], rect.x + 12, rect.y + 34,
                      GREY if not is_hover else CREAM, 15,
                      max_width=rect.width - 24)

            # Lore preview on hover
            if is_hover:
                draw_text(self.screen, race["lore"][:120] + "...",
                          rect.x + 12, rect.y + 56,
                          DIM_GOLD, 11, max_width=rect.width - 24)

        # Scroll hint
        if len(RACE_ORDER) > visible:
            draw_text(self.screen, "↑↓ Scroll for more races",
                      SCREEN_W//2 - 100, start_y + visible * item_h + 5, GREY, 13)

        # ESC hint
        draw_text(self.screen, "ESC to go back",
                  40, SCREEN_H - 30, GREY, 13)

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
            draw_text(self.screen, f"{stat}", x_stats, y, CREAM, 14)
            draw_text(self.screen, f"{val:2d}", x_stats + 40, y, col, 12)
            pygame.draw.rect(self.screen, DARKER_GREY, (x_stats + 65, y+3, 100, 10))
            pygame.draw.rect(self.screen, col, (x_stats + 65, y+3, bar_w, 10))
            y += 20

        # Progress dots
        dot_y = 195
        draw_text(self.screen, "Progress:", 40, dot_y, GREY, 13)
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
            draw_text(self.screen, "^ more above ^", SCREEN_W//2 - 60, 218, DIM_GOLD, 13)
        if self.scroll + visible < len(self.choices):
            draw_text(self.screen, "v more below v", SCREEN_W//2 - 60, cy + 5, DIM_GOLD, 13)

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
                                  GREY, get_font(14))

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

            # Class icon badge (left side of row)
            draw_class_badge(self.screen, cn, rect.x + 8, rect.y + rect.h//2 - 18, 14)

            # Class name and fit (shifted right to make room for badge)
            draw_text(self.screen, cn, rect.x + 46, rect.y + 8,
                      cls["color"], 18, bold=True)

            if not self.quick:
                fit_col = FIT_COLORS.get(fit, GREY)
                draw_text(self.screen, f"[ {fit} ]", rect.x + 180, rect.y + 10,
                          fit_col, 13)

            # Description
            draw_text(self.screen, cls["description"], rect.x + 46, rect.y + 32,
                      GREY if not is_hover else CREAM, 15,
                      max_width=rect.width - 58)

            # Starting abilities
            ab_text = "Starts with: " + ", ".join(a["name"] for a in cls["starting_abilities"])
            draw_text(self.screen, ab_text, rect.x + 46, rect.y + 55,
                      DIM_GOLD, 11)

    # ── Spell Selection ────────────────────────────────────────

    def draw_spell_pick(self, mx, my):
        c = self.current_char
        pool    = getattr(self, "spell_pick_pool", [])
        chosen  = getattr(self, "spell_pick_chosen", [])

        draw_text(self.screen, f"Choose {c.name}'s Starting Abilities",
                  40, 22, GOLD, 22, bold=True)
        draw_text(self.screen,
                  f"{c.class_name}s begin knowing 2 of the following. Choose wisely — you can learn the rest later.",
                  40, 55, GREY, 14)
        draw_text(self.screen, f"Selected: {len(chosen)}/2", 40, 78, HIGHLIGHT, 15, bold=True)

        start_y = 120
        item_h = 80
        for i, ab in enumerate(pool):
            name     = ab["name"]
            is_sel   = name in chosen
            rect     = pygame.Rect(SCREEN_W//2 - 280, start_y + i * item_h, 560, item_h - 6)
            is_hover = rect.collidepoint(mx, my)

            bg  = (40, 55, 35) if is_sel else ((45, 38, 75) if is_hover else PANEL_BG)
            brd = (100, 200, 80) if is_sel else (GOLD if is_hover else PANEL_BORDER)
            draw_panel(self.screen, rect, border_color=brd, bg_color=bg)

            # Ability name
            draw_text(self.screen, name, rect.x + 14, rect.y + 8,
                      (130, 230, 100) if is_sel else (GOLD if is_hover else CREAM),
                      18, bold=True)

            # Type badge
            ab_type = ab.get("type", "")
            type_cols = {"spell":"arcane","aoe":"fire","buff":"gold","heal":"heal",
                         "attack":"red","buff":"buff"}
            TYPE_COL = {"spell":(140,180,255),"aoe":(255,140,80),"buff":(255,220,80),
                        "heal":(100,220,130),"attack":(255,100,100),"cure":(80,200,200)}
            tc = TYPE_COL.get(ab_type, GREY)
            draw_text(self.screen, f"[{ab_type}]", rect.x + 14, rect.y + 32, tc, 12)

            # Description
            draw_text(self.screen, ab.get("desc",""), rect.x + 90, rect.y + 28,
                      GREY if not is_hover else CREAM, 13, max_width=rect.width - 110)

            # Cost
            cost_str = f"{ab.get('cost',0)} {ab.get('resource','MP')}"
            draw_text(self.screen, cost_str, rect.x + rect.width - 140, rect.y + 8, DIM_GOLD, 13)

            # Selected indicator
            if is_sel:
                draw_text(self.screen, "✓ Selected", rect.x + rect.width - 110,
                          rect.y + 28, (130, 230, 100), 12, bold=True)

        # Confirm button
        can_confirm = len(chosen) >= 1
        r_confirm = pygame.Rect(SCREEN_W//2 - 100, SCREEN_H - 65, 200, 45)
        hover_c = r_confirm.collidepoint(mx, my)
        draw_button(self.screen, r_confirm, "Confirm",
                    hover=(hover_c and can_confirm),
                    disabled=not can_confirm)

    # ── Character Summary ─────────────────────────────────────

    def draw_summary(self, mx, my):
        c = self.current_char
        cls = CLASSES[c.class_name]
        from ui.pixel_art import draw_character_silhouette as _dcs

        # Large portrait — right column
        por_w, por_h = 130, 196
        por_x = SCREEN_W - por_w - 40
        por_r = pygame.Rect(por_x, 25, por_w, por_h)
        draw_panel(self.screen, pygame.Rect(por_x - 4, 21, por_w + 8, por_h + 8),
                   border_color=cls["color"])
        equip = getattr(c, "equipment", {})
        armor_t = equip.get("armor", {}).get("armor_tier") if equip.get("armor") else None
        _dcs(self.screen, por_r, c.class_name,
             equipped_weapon=equip.get("weapon"), armor_tier=armor_t, highlight=True)

        draw_text(self.screen, c.name, 80, 25, cls["color"], 26, bold=True)
        # Class badge next to name
        draw_class_badge(self.screen, c.class_name, 40, 20, 16)
        race_str = getattr(c, "race_name", "Human")
        from core.races import RACES
        race_col = RACES.get(race_str, {}).get("color", CREAM)
        draw_text(self.screen, f"{race_str} {c.class_name}  —  Level {c.level}",
                  40, 60, CREAM, 16)
        # Race name in its color
        draw_text(self.screen, race_str, 40, 60, race_col, 16)

        # Stats
        draw_panel(self.screen, pygame.Rect(35, 95, 300, 175))
        draw_text(self.screen, "Attributes", 50, 102, GOLD, 14, bold=True)
        y = 125
        for stat in STAT_NAMES:
            val = c.stats[stat]
            draw_text(self.screen, f"{STAT_FULL_NAMES[stat]}", 50, y, CREAM, 15)
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
            draw_text(self.screen, f"{rname}:", 370, y, CREAM, 15)
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

            # Portrait silhouette (right side of card) — preserve sprite aspect ratio
            from ui.pixel_art import draw_character_silhouette as _dcs
            from ui.wiz_sprites import W as SPR_W, H as SPR_H
            por_w = 62
            por_h = int(por_w * SPR_H / SPR_W)   # ~103px, matches 48:80 ratio
            por_r = pygame.Rect(cx + card_w - por_w - 4, cy + (card_h - por_h) // 2, por_w, por_h)
            equip = getattr(c, "equipment", {})
            armor_t = equip.get("armor", {}).get("armor_tier") if equip.get("armor") else None
            _dcs(self.screen, por_r, c.class_name,
                 equipped_weapon=equip.get("weapon"), armor_tier=armor_t)

            # Class badge + Name and class (left side)
            draw_class_badge(self.screen, c.class_name, cx + 6, cy + 6, 14)
            draw_text(self.screen, c.name, cx + 44, cy + 8, cls["color"], 16, bold=True)
            race_str = getattr(c, "race_name", "Human")
            draw_text(self.screen, f"{race_str} {c.class_name}", cx + 44, cy + 28, CREAM, 15)

            # Tier badge + level (right of class label)
            from core.progression import PLANAR_TIERS
            tier_idx = getattr(c, "planar_tier", 0)
            tier_info = PLANAR_TIERS[tier_idx]
            tier_label = f"Lv.{c.level}  {tier_info['symbol']} {tier_info['name']}"
            draw_text(self.screen, tier_label, cx + 44, cy + 44, tier_info["color"], 12)
            sy = cy + 64
            stat_w = card_w - por_w - 20
            for i, stat in enumerate(STAT_NAMES):
                val = c.stats[stat]
                col_v = (120, 200, 120) if val >= 13 else HIGHLIGHT if val >= 9 else GREY
                sx = cx + 10 + (i % 2) * (stat_w // 2)
                sdy = sy + (i // 2) * 20
                draw_text(self.screen, f"{stat}: {val}", sx, sdy, col_v, 14)

            # Resources compact
            ry = sy + 68
            for rname, rval in list(c.resources.items())[:3]:
                draw_text(self.screen, f"{rname}: {rval}", cx + 10, ry, DIM_GREEN, 13)
                ry += 14

            # Abilities
            ab_names = [a["name"] for a in c.abilities]
            draw_text(self.screen, "Skills: " + ", ".join(ab_names),
                      cx + 10, cy + card_h - 25, DARK_GREY, 10,
                      max_width=card_w - por_w - 20)

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
            settings_btn = pygame.Rect(20, 88, 120, 32)
            draw_button(self.screen, settings_btn, "⚙ Settings",
                        hover=settings_btn.collidepoint(mx, my), size=13)

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

    # ── Location Type Handlers ─────────────────────────────────

    def _handle_port(self, loc_id, loc):
        """Port location — show fast travel options to other ports."""
        from data.world_map import PORT_ROUTES
        routes = PORT_ROUTES.get(loc_id, [])

        # Filter to only discovered destinations
        discovered = self.world_state.discovered_locations
        available = [
            r for r in routes
            if r in LOCATIONS and r in discovered
        ]

        if not available:
            self.world_map_ui._show_event(
                f"{loc['name']}: No known ports in range. Explore to find routes.",
                (80, 180, 220))
            return

        # Build a simple destination list in the event message area.
        # For now we show the first reachable port and teleport there.
        # A full port UI (Phase 5) will replace this with a proper menu.
        dest_id = available[0]
        dest = LOCATIONS[dest_id]
        self.world_state.party_x = dest["x"]
        self.world_state.party_y = dest["y"]
        self.world_map_ui._show_event(
            f"Set sail from {loc['name']} → {dest['name']}!", (80, 180, 220))

    def _handle_secret(self, loc_id, loc):
        """Secret location — reward on first visit, flavour text always."""
        visited_key = f"visited.{loc_id}"
        from core.story_flags import get_flag, set_flag

        if not get_flag(visited_key):
            set_flag(visited_key, True)
            # One-time reward: a small gold find
            reward_gold = 25
            if self.party:
                self.party[0].add_gold(reward_gold)
            self.world_map_ui._show_event(
                f"Discovered: {loc['name']}! {loc.get('description','')} "
                f"(+{reward_gold}g found here)",
                (200, 160, 220))
        else:
            self.world_map_ui._show_event(
                f"{loc['name']}: {loc.get('description', 'A mysterious place.')}",
                (160, 120, 200))

    def _handle_poi(self, loc_id, loc):
        """Point of interest — flavour text, possible random encounter."""
        visited_key = f"visited.{loc_id}"
        from core.story_flags import get_flag, set_flag

        first_visit = not get_flag(visited_key)
        if first_visit:
            set_flag(visited_key, True)

        desc = loc.get("description", "An interesting location.")
        self.world_map_ui._show_event(f"{loc['name']}: {desc}", (180, 200, 140))

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
        dialogue_id = None
        if self.dialogue_ui:
            result = self.dialogue_ui.result  # e.g., "fight" for boss combat
            try:
                dialogue_id = self.dialogue_ui.state.tree.get("id")
            except Exception:
                pass
        callback = self.dialogue_callback
        return_state = self.dialogue_return_state

        self.dialogue_ui = None
        self.dialogue_callback = None
        self.dialogue_return_state = None

        # Post-betrayal: remove 2 Hearthstone Fragments from party inventory
        if dialogue_id == "maren_betrayal":
            self._maren_takes_hearthstones()
            # Safety: ensure maren.left is set even if the dialogue was
            # closed early (e.g. old save, edge case). maren_betrayal is
            # locked so Escape is suppressed, but we guard here anyway.
            from core.story_flags import get_flag, set_flag
            if not get_flag("maren.left"):
                set_flag("maren.betrayal_done", True)
                set_flag("maren.left", True)

        if callback:
            callback(result)
        elif return_state is not None:
            self.go(return_state)

    def _maren_takes_hearthstones(self):
        """Remove 2 Hearthstone Fragment items from party inventory after Maren's betrayal."""
        if not self.party:
            return
        taken = 0
        for member in self.party.members:
            if taken >= 2:
                break
            remove_these = []
            for item in member.inventory:
                if taken >= 2:
                    break
                name = item.get("name", "")
                if "Hearthstone Fragment" in name or "hearthstone" in name.lower():
                    remove_these.append(item)
                    taken += 1
            for item in remove_these:
                if item in member.inventory:
                    member.inventory.remove(item)

    def draw_dialogue(self, mx, my):
        """Draw standalone dialogue."""
        if self.dialogue_ui:
            self.dialogue_ui.draw(self.screen, mx, my)

    # ──────────────────────────────────────────────────────────
    #  PEACEFUL RESOLUTION  (boss spared / yielded without combat)
    # ──────────────────────────────────────────────────────────

    def _handle_peaceful_resolution(self, dungeon_id, res):
        """Grant hearthstone + bonus items for a peaceful boss outcome, then
        run the post-boss flavour dialogue and return to the dungeon."""
        from core.story_flags import collect_hearthstone, set_flag, defeat_boss, auto_advance_quests
        from data.magic_items import get_unique_item, get_boss_bonus_drops
        import random

        # 1. Grant hearthstone
        hs_num = res.get("hearthstone")
        if hs_num:
            hs_item = {
                "name":        res.get("hearthstone_name", f"Hearthstone Fragment ({dungeon_id})"),
                "type":        "quest_item",
                "description": "A warm, faintly glowing stone fragment. "
                               "Part of the Hearthstone of Aldenmere.",
                "identified":  True,
                "quest_item":  True,
                "rarity":      "legendary",
            }
            self.party[0].add_item(hs_item)
            collect_hearthstone(hs_num)
            set_flag(f"hearthstone.{dungeon_id}", True)

        # 2. Grant guaranteed unique bonus items
        granted_items = []
        rng = random.Random()
        for ukey in res.get("bonus_loot", []):
            item = get_unique_item(ukey, self.party)
            if item:
                self.party[0].add_item(item)
                granted_items.append(item["name"])

        # 3. Set story flags
        set_flag(f"boss_defeated.{dungeon_id}", True)
        boss_npc = res.get("boss_npc")
        if boss_npc:
            defeat_boss(boss_npc)

        # 4. Unlock next dungeon key
        world_key = res.get("world_key")
        if world_key and self.world_state and not self.world_state.has_key(world_key):
            self.world_state.add_key(world_key)
            from data.world_map import LOCATIONS
            for lid, loc in LOCATIONS.items():
                if loc.get("required_key") == world_key:
                    self.world_state.discovered_locations.add(lid)

        # 5. Advance quests
        _done = auto_advance_quests(self.party)
        self._notify_quests_done(_done)

        # 6. Show brief item-received notifications
        if hs_num:
            self.dungeon_ui.show_event("Received: Hearthstone Fragment!", GOLD)
        for iname in granted_items:
            self.dungeon_ui.show_event(f"Received: {iname}!", (180, 220, 255))

        # 7. Run post-boss flavour dialogue (peaceful variant), then return to dungeon
        self._show_post_boss_dialogue(dungeon_id, peaceful=True,
                                      callback=lambda _: self.go_fade(S_DUNGEON))

    # ──────────────────────────────────────────────────────────
    #  POST-BOSS DIALOGUE  (cutscene after boss killed/spared)
    # ──────────────────────────────────────────────────────────

    def _show_post_boss_dialogue(self, dungeon_id, peaceful=False, callback=None):
        """Show multi-line post-boss cutscene text using the dungeon event overlay,
        then call callback (or return to dungeon) when done."""
        from data.story_data import get_boss_post_dialogue
        post = get_boss_post_dialogue(dungeon_id, peaceful=peaceful)
        if not post:
            if callback:
                callback(None)
            return

        lines = post.get("lines", [])
        speaker = post.get("speaker", "")
        if not lines:
            if callback:
                callback(None)
            return

        # Build a synthetic dialogue tree from the lines so we get the
        # cinematic dialogue UI with "Continue" advances rather than a wall of text.
        nodes = {}
        for i, line in enumerate(lines):
            nid   = f"p{i}"
            nxt   = f"p{i+1}" if i + 1 < len(lines) else None
            nodes[nid] = {
                "speaker": speaker if i == 0 else ("" if not speaker else speaker),
                "text":    line,
                "choices": [{"text": "Continue", "next": nxt}] if nxt else [],
                "end":     nxt is None,
            }

        synth_tree = {
            "id":    post["id"],
            "nodes": nodes,
            "start": "p0",
        }

        # Reuse the standalone dialogue system with a synthetic NPC id
        _synth_npc = f"__post_boss_{dungeon_id}"
        from data.story_data import NPC_DIALOGUES
        NPC_DIALOGUES[_synth_npc] = [{"conditions": [], "tree": synth_tree}]

        self.start_dialogue(_synth_npc, return_state=S_DUNGEON, callback=callback)

    def start_chest(self, gold, items, is_secret=False, return_state=None):
        """Open the chest loot assignment screen."""
        self.chest_ui = ChestUI(self.party, gold, items, is_secret=is_secret)
        self.chest_return_state = return_state if return_state is not None else S_DUNGEON
        # Tutorial: hint on first unidentified item
        if any(not item.get("identified", True) for item in items):
            from core.tutorial import fire_combat_hints, _should_show, _mark_shown
            if _should_show("identification"):
                # Queue it so it shows after returning from chest to dungeon
                self._chest_hint_unidentified = True
        self.go(S_CHEST)

    def _draw_chest(self, mx, my):
        """Draw the chest loot screen over the dungeon background."""
        # Draw the dungeon behind it so the overlay looks right
        if self.dungeon_ui and self.dungeon_state:
            dt = self.clock.get_time() / 1000.0
            self.dungeon_ui.draw(self.screen, mx, my, dt)
        else:
            self.screen.fill((12, 10, 24))
        if self.chest_ui:
            dt = self.clock.get_time() / 1000.0
            self.chest_ui.draw(self.screen, mx, my, dt)

    def _fire_chest_hint_if_pending(self):
        """Fire the unidentified-item hint if queued and dungeon_ui is available."""
        if getattr(self, "_chest_hint_unidentified", False) and self.dungeon_ui:
            from core.tutorial import _should_show, _mark_shown
            if _should_show("identification"):
                self.dungeon_ui.show_event(
                    "Unidentified items need appraisal — Mage or Thief can identify in Inventory.",
                    (210, 180, 100)
                )
                _mark_shown("identification")
            self._chest_hint_unidentified = False

    def start_camp(self, location="dungeon", dungeon_floor=1, return_state=None):
        """Open the full camp screen."""
        from ui.camp_ui import CampUI
        self.camp_ui = CampUI(self.party, location=location, dungeon_floor=dungeon_floor)
        self.camp_return_state = return_state or self.state
        self.go(S_CAMP)

    def _end_camp(self):
        """Handle camp screen closing."""
        if not self.camp_ui:
            return
        result = self.camp_ui.result
        return_state = self.camp_return_state
        self.camp_ui = None
        self.camp_return_state = None

        if result == "rest":
            # Process the rest execution
            self.go(return_state)
            if return_state == S_DUNGEON:
                self._process_dungeon_event({"type": "camp_rest_execute"})
            elif return_state == S_WORLD_MAP:
                self._process_world_event({"type": "camp"})
        else:
            # Cancel — just go back
            self.go(return_state)

    def _draw_settings(self, mx, my):
        """Draw the volume settings overlay."""
        # Draw whatever was underneath (party screen)
        self.draw_party(mx, my)
        if self.settings_ui:
            self.settings_ui.draw(self.screen, mx, my)

    def _draw_camp(self, mx, my):
        """Draw the camp screen."""
        if self.camp_ui:
            self.camp_ui.draw(self.screen, mx, my)

    def start_combat(self, encounter_key, surprise=None):
        """Initialize combat with an encounter."""
        self.combat_state = CombatState(self.party, encounter_key, surprise=surprise)
        self.combat_ui = CombatUI(self.combat_state)
        self.enemy_turn_delay = 0
        # Tutorial hints — queue first-combat hints with a short delay
        from core.tutorial import fire_combat_hints_delayed
        self._pending_hints = fire_combat_hints_delayed("first_combat", self.combat_ui, delay_ms=2800)
        self.go(S_COMBAT)

    def draw_combat(self, mx, my):
        """Draw the combat screen and handle enemy AI timing."""
        self.combat_ui.draw(self.screen, mx, my)

        # Tick pending tutorial hints
        if getattr(self, "_pending_hints", None):
            from core.tutorial import tick_pending_hints
            self._pending_hints = tick_pending_hints(
                self._pending_hints, self.clock.get_time(), self.combat_ui
            )

        # Auto-execute enemy turns with a small delay for readability
        if (self.combat_state.phase not in ("victory", "defeat", "fled") and
                not self.combat_state.is_player_turn()):
            self.enemy_turn_delay += self.clock.get_time()
            self.combat_ui.enemy_anim_timer += self.clock.get_time()
            if self.enemy_turn_delay > 600:  # 600ms delay between enemy actions
                result = self.combat_state.execute_enemy_turn()
                # Pick sound from what actually happened
                if result.get("hit") is False:
                    sfx.play("miss")
                elif result.get("is_crit"):
                    sfx.play("hit_critical")
                elif result.get("action") == "enemy_attack":
                    sfx.play("hit_physical")
                # Play death sound if a player just went down
                if result.get("defender", {}).get("alive") is False:
                    sfx.play("death")
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

    def _grant_boss_rewards(self, dungeon_id):
        """Grant key items and story flags when a boss is defeated."""
        # Map dungeon bosses to key rewards
        BOSS_KEY_GRANTS = {
            "goblin_warren":   "thornwood_map",    # unlocks Spider's Nest area
            "spiders_nest":    "mine_key",          # unlocks Abandoned Mine
            "abandoned_mine":  "ashenmoor_seal",    # unlocks Ruins of Ashenmoor
            "sunken_crypt":    "spire_key",         # unlocks Valdris' Spire
            "ruins_ashenmoor": "crypt_amulet",      # unlocks Sunken Crypt
            "dragons_tooth":   "pale_coast_access", # unlocks Pale Coast Catacombs
            "pale_coast":      "pale_coast_cleared",
            "windswept_isle":  "isle_cleared",
        }
        # Hearthstone numbers per dungeon
        HEARTHSTONE_MAP = {
            "abandoned_mine": 1,
            "sunken_crypt":   2,
            "dragons_tooth":  3,
            "pale_coast":     4,
            "windswept_isle": 5,
        }
        # Map dungeon IDs to boss NPC IDs (for dialogue conditions)
        BOSS_NPC_IDS = {
            "goblin_warren":   "grak",
            "abandoned_mine":  "korrath",
            "spiders_nest":    "spider_queen",
            "sunken_crypt":    "sunken_warden",
            "ruins_ashenmoor": "ashvar",
            "dragons_tooth":   "karreth",
            "pale_coast":      "pale_sentinel",
            "windswept_isle":  "isle_keeper",
            "valdris_spire":   "valdris",
            "shadow_throne":   "shadow_valdris",
        }
        key = BOSS_KEY_GRANTS.get(dungeon_id)
        if key and self.world_state:
            if not self.world_state.has_key(key):
                self.world_state.add_key(key)
                # Reveal matching locations — only update discovered_locations,
                # never mutate the module-level LOCATIONS dict (that persists
                # across WorldState instances and causes phantom reveals).
                from data.world_map import LOCATIONS
                for loc_id, loc in LOCATIONS.items():
                    if loc.get("required_key") == key:
                        self.world_state.discovered_locations.add(loc_id)

        # Set story flags
        from core.story_flags import set_flag, defeat_boss, collect_hearthstone
        set_flag(f"boss_defeated.{dungeon_id}", True)

        # Collect hearthstone for relevant dungeons
        hs_num = HEARTHSTONE_MAP.get(dungeon_id)
        if hs_num:
            collect_hearthstone(hs_num)
            set_flag(f"hearthstone.{dungeon_id}", True)

        # Set boss NPC defeated flag (used by dialogue conditions)
        boss_npc = BOSS_NPC_IDS.get(dungeon_id)
        if boss_npc:
            defeat_boss(boss_npc)

        # Pale Sentinel — if she yielded peacefully, skip the "boss defeated" fanfare tone
        if dungeon_id == "pale_coast" and get_flag("sentinel.yielded"):
            set_flag("boss_defeated.pale_coast", True)  # already set by dialogue, ensure consistency

        # Valdris Phase 1 → trigger Phase 2 immediately
        if dungeon_id == "shadow_throne":
            phase1_enc = "boss_valdris_phase1"
            current_enc = getattr(self, "_last_boss_encounter", None)
            if current_enc == phase1_enc and not get_flag("valdris.phase2_done"):
                # Queue phase 2 combat
                set_flag("valdris.phase2_triggered", True)
                from data.bestiary_m9 import NEW_ENCOUNTERS
                phase2 = NEW_ENCOUNTERS.get("boss_valdris_phase2", {})
                if phase2:
                    self._queue_phase2_boss = phase2
                    return  # don't fire ending yet

        # Valdris Phase 2 done → trigger ending
        if dungeon_id == "shadow_throne" and get_flag("valdris.phase2_triggered"):
            set_flag("valdris.phase2_done", True)
            set_flag("boss_defeated.shadow_valdris", True)
            self._trigger_ending()
        elif dungeon_id == "shadow_throne":
            self._trigger_ending()

    def _sync_flag_keys(self):
        """Sync story-flag-based world keys.

        Ensures world_state.key_items reflects story flags — critical after
        loading a save where key_items is restored, but also as a safety net
        if WorldState was re-created without going through _grant_boss_rewards.
        """
        if not self.world_state:
            return
        from core.story_flags import get_flag
        from data.world_map import LOCATIONS

        # Flag → world key pairs (includes all boss grants + ship passage)
        FLAG_KEYS = {
            "ship_passage.granted":          "ship_passage",
            "boss_defeated.goblin_warren":   "thornwood_map",
            "boss_defeated.spiders_nest":    "mine_key",
            "boss_defeated.abandoned_mine":  "ashenmoor_seal",
            "boss_defeated.ruins_ashenmoor": "crypt_amulet",
            "boss_defeated.sunken_crypt":    "spire_key",
            "boss_defeated.dragons_tooth":   "pale_coast_access",
            "boss_defeated.pale_coast":      "pale_coast_cleared",
            "boss_defeated.windswept_isle":  "isle_cleared",
        }
        for flag, key in FLAG_KEYS.items():
            if get_flag(flag) and not self.world_state.has_key(key):
                self.world_state.add_key(key)
                for loc_id, loc in LOCATIONS.items():
                    if loc.get("required_key") == key:
                        self.world_state.discovered_locations.add(loc_id)

        # windswept_isle has no key gate — discover it when Varek sends you there
        # (quest main_pale_coast or main_windswept_isle active in Act 3)
        from core.story_flags import get_flag as gf
        if gf("maren.left") and "windswept_isle" not in self.world_state.discovered_locations:
            if gf("quest.main_windswept_isle.state", 0) >= 1 or gf("item.hearthstone.3"):
                self.world_state.discovered_locations.add("windswept_isle")

    def _trigger_ending(self):
        """Fire after Valdris is defeated. Transition to the epilogue sequence."""
        from core.story_flags import hearthstone_count, get_flag
        self._ending_timer  = 0.0
        self._ending_phase  = "fade_in"   # fade_in → text → credits → done
        self._ending_hs     = hearthstone_count()
        self._ending_freed  = get_flag("lore.karreth_freed")
        self._ending_heard  = get_flag("maren.betray_heard")
        self._ending_key_index = 0
        self._ending_input_ready = False
        self.go(S_ENDING)

    # ── Game Over Screen ──────────────────────────────────────────

    def _handle_game_over_input(self, event):
        import pygame
        if not self._game_over_ready:
            return
        if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            # Build inn UI with the recovery message, then fade to town
            self.town_ui = TownUI(self.party, town_id=self.current_town_id)
            self.town_ui.inn_result = (
                "Your party has fallen...\n"
                "You awaken at the inn, battered and bruised.\n"
                "(25% of your gold was lost)"
            )
            self.town_ui.view = self.town_ui.VIEW_INN
            self.go_fade(S_TOWN)

    def _draw_game_over(self, mx, my):
        import pygame
        dt = self.clock.get_time() / 1000.0
        self._game_over_timer = getattr(self, "_game_over_timer", 0.0) + dt
        t = self._game_over_timer

        surf = self.screen
        W, H = surf.get_size()

        # Dark red-tinged background
        surf.fill((8, 2, 2))

        def fnt(sz):
            try:    return pygame.font.SysFont("georgia", sz)
            except: return pygame.font.Font(None, sz + 4)

        def txt(text, y, size=18, color=(220, 200, 190), alpha=255):
            f = fnt(size)
            s = f.render(text, True, color)
            s.set_alpha(min(255, alpha))
            surf.blit(s, (W // 2 - s.get_width() // 2, y))

        # Fade in over 1.5s
        fade = min(1.0, t / 1.5)
        alpha = int(255 * fade)

        # Title
        txt("YOUR PARTY HAS FALLEN", H // 2 - 120, 38, (200, 60, 60), alpha)

        # Thin red divider
        if fade > 0.3:
            line_alpha = int(255 * min(1.0, (t - 0.4) / 0.8))
            line_surf = pygame.Surface((320, 1), pygame.SRCALPHA)
            line_surf.fill((160, 40, 40, line_alpha))
            surf.blit(line_surf, (W // 2 - 160, H // 2 - 72))

        # Character names and HP
        if fade > 0.5:
            char_alpha = int(255 * min(1.0, (t - 0.7) / 0.8))
            y_start = H // 2 - 50
            for i, c in enumerate(self.party):
                name_color = (160, 80, 80) if c.resources.get("HP", 0) <= 0 else (180, 160, 140)
                status = "Fallen" if c.resources.get("HP", 0) <= 0 else "Unconscious"
                txt(f"{c.name}  —  {status}", y_start + i * 26, 16, name_color, char_alpha)

        # Penalty reminder
        if fade > 0.8:
            pen_alpha = int(255 * min(1.0, (t - 1.1) / 0.6))
            txt("25% of your gold has been lost.", H // 2 + 70, 15, (140, 110, 110), pen_alpha)
            txt("Your party wakes at the last inn.", H // 2 + 94, 15, (140, 110, 110), pen_alpha)

        # Prompt — appears after 2.5s
        if t > 2.5:
            self._game_over_ready = True
            pulse = int(100 + 80 * abs((t * 1.2) % 2 - 1))
            txt("Press any key to continue", H - 55, 14, (pulse, pulse // 2, pulse // 2))

    def _handle_ending_input(self, event):
        import pygame
        if not self._ending_input_ready:
            return
        if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            self._ending_key_index += 1
            self._ending_input_ready = False
            self._ending_timer = 0.0

    def _draw_ending(self, mx, my):
        import pygame
        dt = self.clock.get_time() / 1000.0
        self._ending_timer = getattr(self, "_ending_timer", 0.0) + dt

        surf  = self.screen
        W, H  = surf.get_size()
        surf.fill((4, 3, 10))

        def fnt(sz):
            try:
                return pygame.font.SysFont("georgia", sz)
            except Exception:
                return pygame.font.Font(None, sz + 4)

        def txt(text, y, size=18, color=(220, 210, 190), alpha=255):
            f = fnt(size)
            s = f.render(text, True, color)
            s.set_alpha(min(255, alpha))
            surf.blit(s, (W // 2 - s.get_width() // 2, y))

        hs   = getattr(self, "_ending_hs",    0)
        freed = getattr(self, "_ending_freed", False)
        heard = getattr(self, "_ending_heard", False)
        ki   = getattr(self, "_ending_key_index", 0)
        t    = self._ending_timer

        # Pages indexed by ki
        PAGES = [
            # Page 0 — the ward network restored
            [("THE FADING RECEDES", H // 2 - 80, 36, (255, 220, 120)),
             ("The Hearthstone network pulses once — twice —", H // 2 - 10, 17, (210, 195, 165)),
             ("and then holds.", H // 2 + 14, 17, (210, 195, 165)),
             ("Across the region, the grey at the edges of things", H // 2 + 50, 15, (170, 160, 140)),
             ("begins, slowly, to pull back.", H // 2 + 72, 15, (170, 160, 140))],
            # Page 1 — Maren outcome (varies)
            [("MAREN VALDRIS", H // 2 - 80, 28,
              (200, 170, 220) if heard else (180, 120, 100)),
             ("She was at the Spire when it fell.", H // 2 - 20, 17, (210, 195, 165)),
             ("Whether the ritual she had planned would have worked",
              H // 2 + 14, 15, (170, 160, 140)),
             ("remains an open question.", H // 2 + 36, 15, (170, 160, 140)),
             ("She left no notes behind — only one stone.", H // 2 + 70, 15, (170, 160, 140))
             ] if not heard else
            [("MAREN VALDRIS", H // 2 - 80, 28, (200, 170, 220)),
             ("She listened when you explained what had happened.", H // 2 - 20, 17, (210, 195, 165)),
             ("She helped carry the last stone to the anchor point.", H // 2 + 14, 15, (170, 160, 140)),
             ("She left before dawn, as she always had.", H // 2 + 50, 15, (170, 160, 140)),
             ("She left no forwarding address.", H // 2 + 72, 15, (170, 160, 140))],
            # Page 2 — Karreth (varies)
            [("KARRETH", H // 2 - 80, 28, (200, 140, 80)),
             ("The first guardian. The one who held longest.", H // 2 - 20, 17, (210, 195, 165)),
             ("Its vigil is over.", H // 2 + 14, 17, (210, 195, 165)),
             ("The network remembers what it was.", H // 2 + 50, 15, (170, 160, 140))
             ] if freed else
            [("KARRETH", H // 2 - 80, 28, (160, 100, 60)),
             ("The first guardian.", H // 2 - 20, 17, (210, 195, 165)),
             ("The Corrupted drove it to a final charge.", H // 2 + 14, 17, (210, 195, 165)),
             ("It did not know what it protected until the end.", H // 2 + 50, 15, (170, 160, 140))],
            # Page 3 — hearthstones
            [(f"{'ALL FIVE' if hs >= 5 else str(hs).upper() + ' OF FIVE'} HEARTHSTONES RESTORED",
              H // 2 - 80, 24,
              (255, 230, 100) if hs >= 5 else (200, 200, 150)),
             ("The wards are not what they were —", H // 2 - 10, 17, (210, 195, 165)),
             ("they are something new.", H // 2 + 14, 17, (210, 195, 165)),
             ("They do not require blood. They do not require vigil.", H // 2 + 50, 15, (170, 160, 140)),
             ("They simply hold.", H // 2 + 72, 15, (170, 160, 140))],
            # Page 4 — party names
            [("THE WARDENS", H // 2 - 110, 30, (255, 240, 200)),
             ("The order is gone.", H // 2 - 60, 17, (210, 195, 165)),
             ("But the work continues.", H // 2 - 38, 17, (210, 195, 165))] +
            [(c.name, H // 2 - 5 + i * 26, 18, (220, 200, 160))
             for i, c in enumerate(self.party)] +
            [("Their names are not recorded.", H // 2 + 90, 14, (140, 130, 115)),
             ("Only the holding matters.", H // 2 + 110, 14, (140, 130, 115))],
            # Page 5 — THE END / credits
            [("REALM OF SHADOWS", H // 2 - 80, 40, (255, 240, 200)),
             ("", H // 2 - 20, 1, (0, 0, 0)),
             ("A game by Charles Gasper", H // 2 + 10, 16, (170, 160, 140)),
             ("", H // 2 + 35, 1, (0, 0, 0)),
             ("Thank you for playing.", H // 2 + 60, 18, (210, 195, 165))],
        ]

        if ki >= len(PAGES):
            # After all pages — return to title
            if t > 2.0:
                self.go(S_TITLE)
            return

        page = PAGES[ki]
        fade = min(1.0, t / 1.2)

        for (text, y, size, color) in page:
            if text:
                txt(text, y, size, color, int(255 * fade))

        # Prompt
        if t > 1.5:
            self._ending_input_ready = True
            pulse = int(140 + 80 * abs((t * 1.5) % 2 - 1))
            is_last = ki == len(PAGES) - 1
            prompt = "Press any key to continue" if not is_last else "Press any key"
            txt(prompt, H - 50, 13, (pulse, pulse, pulse))

    def _handle_fled_combat(self):
        """Handle successful flee from combat.
        Returns party to dungeon or world map — no rewards granted."""
        self.combat_state = None
        self.combat_ui = None
        if self.dungeon_state:
            # Fled from a dungeon encounter — return to dungeon
            self.go_fade(S_DUNGEON)
        elif self.current_town_id:
            # Fled from a town-adjacent encounter
            self.go_fade(S_TOWN)
        else:
            self.go_fade(S_WORLD_MAP)

    def _trigger_briarhollow_attack(self):
        """Trigger the Act 1 climax: shadow creatures attack Briarhollow.
        Called once when the party returns after collecting Hearthstone 1."""
        self._attack_phase = "cinematic"
        self._attack_timer = 0.0
        self.go(S_ATTACK_CINEMATIC)

    def _draw_attack_cinematic(self, mx, my):
        """Full-screen dramatic cinematic before the Briarhollow battle."""
        import pygame
        dt = self.clock.get_time() / 1000.0
        self._attack_timer = getattr(self, "_attack_timer", 0.0) + dt

        surf = self.screen
        W, H = surf.get_size()
        surf.fill((0, 0, 0))

        t = self._attack_timer
        # Fade in over first 0.8s
        alpha = min(255, int(t / 0.8 * 255))

        lines = [
            ("THE FADING FOLLOWS", 2.0, 42, (220, 80, 80)),
            ("Something has tracked the Hearthstone fragment", 3.5, 20, (200, 170, 130)),
            ("back to Briarhollow.", 3.5, 20, (200, 170, 130)),
            ("", 0, 0, (0,0,0)),
            ("Shadow creatures emerge from the tree line.", 5.0, 20, (180, 150, 110)),
            ("", 0, 0, (0,0,0)),
            ("DEFEND THE TOWN", 6.5, 34, (240, 100, 60)),
        ]

        font_cache = {}
        def get_font(size):
            if size not in font_cache:
                font_cache[size] = pygame.font.SysFont("Georgia", size)
            return font_cache[size]

        y = H // 2 - 120
        for text, appear_at, size, color in lines:
            if not text or size == 0:
                y += 20
                continue
            if t >= appear_at:
                line_alpha = min(255, int((t - appear_at) / 0.6 * 255))
                font = get_font(size)
                rendered = font.render(text, True, color)
                rendered.set_alpha(line_alpha)
                x = W // 2 - rendered.get_width() // 2
                surf.blit(rendered, (x, y))
            y += size + 14

        # Show "Press any key" after all lines appear
        if t >= 8.5:
            prompt_font = pygame.font.SysFont("Georgia", 16)
            pulse = abs((t * 2) % 2 - 1)  # 0→1→0 pulse
            prompt_alpha = int(80 + 175 * pulse)
            prompt = prompt_font.render("[ Press any key to continue ]", True, (160, 140, 120))
            prompt.set_alpha(prompt_alpha)
            surf.blit(prompt, (W // 2 - prompt.get_width() // 2, H - 60))

    def _handle_attack_cinematic_input(self, event):
        """Handle input during attack cinematic — any key/click advances."""
        import pygame
        t = getattr(self, "_attack_timer", 0.0)
        if t < 1.5:
            return  # prevent accidental skip
        if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            # Transition to the actual combat
            from core.story_flags import set_flag
            set_flag("briarhollow_attack.done", True)
            self._post_combat_town = "briarhollow"  # after fight, enter town
            self.pre_dungeon_state = None
            self.start_combat("briarhollow_attack")

    def draw_inventory(self, mx, my):
        """Draw the inventory/equipment screen."""
        dt = self.clock.get_time()
        self.inventory_ui.draw(self.screen, mx, my, dt)

    def draw_town(self, mx, my):
        """Draw the town hub screen."""
        dt = self.clock.get_time()
        self.town_ui.draw(self.screen, mx, my, dt)
        # Drain quest completions queued during dialogue → show banners
        pending = getattr(self.town_ui, "pending_quest_completions", [])
        if pending:
            self._notify_quests_done(pending)
            self.town_ui.pending_quest_completions = []

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
            sfx.play("encounter")
            self.start_combat(event["key"])

        elif event["type"] == "camp":
            result = self.world_state.camp()
            if result["type"] == "camp_ambush":
                sfx.play("encounter")
                self.world_map_ui._show_event("Ambush during rest!", RED)
                self.start_combat(result["key"])
            else:
                sfx.play("camp_rest")
                healed = result.get("healed", {})
                parts = [f"{name} +{hp}HP" for name, hp in healed.items() if hp > 0]
                msg = "Rested safely. " + ", ".join(parts) if parts else "Rested safely. Already at full health."
                self.world_map_ui._show_event(msg, GREEN)

        elif event["type"] == "enter_location":
            loc = event["data"]
            print(f"[DEBUG] enter_location: id={event.get('id')}, type={loc['type']}")
            if loc["type"] == LOC_TOWN:
                town_id = event.get("id", "briarhollow")
                self.current_town_id = town_id
                self.town_ui = TownUI(self.party, town_id=town_id)

                # ── Track town visits for quest objectives ──
                from core.story_flags import set_flag, start_quest, get_flag as _gf
                set_flag(f"town.{town_id}.visited", True)
                # Auto-start act3 finale when entering Valdris' Spire (treated as dungeon,
                # but thornhaven visit starts main_thornhaven objective)
                if town_id == "thornhaven":
                    start_quest("main_thornhaven")  # safe: no-op if already started
                if town_id == "briarhollow":
                    start_quest("main_meet_maren")  # auto-start intro quest (Elder Thom not in TOWN_NPCS)

                # ── Act 1 Climax: Shadow attack on Briarhollow ──
                # Fires once, after Hearthstone 1 is collected, on next visit to Briarhollow
                if town_id == "briarhollow":
                    from core.story_flags import get_flag
                    hs1 = get_flag("hearthstone.abandoned_mine")
                    already_done = get_flag("briarhollow_attack.done")
                    if hs1 and not already_done:
                        self._trigger_briarhollow_attack()
                        return  # attack handler takes over

                self.go_fade(S_TOWN)
            elif loc["type"] == LOC_DUNGEON:
                # Find matching dungeon ID
                loc_id = event.get("id", "")
                dungeon_id = loc_id  # location ID matches dungeon ID
                print(f"[DEBUG] Dungeon entry: loc_id={loc_id}, in DUNGEONS={loc_id in DUNGEONS}")
                if dungeon_id in DUNGEONS:
                    can, reason = self.world_state.can_enter_dungeon(loc_id)
                    print(f"[DEBUG] Can enter: {can}, reason: {reason}")
                    if can:
                        # ── Fading entry warning (Act 2+) ──────────────────
                        from core.story_flags import hearthstone_count, get_flag
                        _hs = hearthstone_count()
                        _act = get_flag("act", 1)
                        _fading_dungeons = {
                            # dungeons that are narratively deep in Fading territory
                            "ruins_ashenmoor": 2, "sunken_crypt": 2,
                            "dragons_tooth": 2,   "valdris_spire": 3,
                            "pale_coast": 3,      "windswept_isle": 3,
                            "shadow_throne": 3,
                        }
                        _fading_threshold = _fading_dungeons.get(dungeon_id, 0)
                        if _fading_threshold and _act >= _fading_threshold:
                            # Show a brief red-tinted Fading warning in the event strip
                            _intensity = min(3, _hs)
                            _warnings = [
                                "A faint grey veil hangs over the entrance. The air tastes wrong.",
                                "Shadow energy seeps from the entrance. Your senses feel dulled.",
                                "The Fading is strong here. Enemies will be more aggressive.",
                            ]
                            _w = _warnings[_intensity - 1] if _intensity >= 1 else None
                            if _w:
                                self.world_map_ui._show_event(
                                    f"⚠ Fading Zone — {_w}", (180, 80, 80))
                            # Store fading intensity on the dungeon session for encounter modifier
                            self._pending_fading_level = _intensity
                        else:
                            self._pending_fading_level = 0
                        # ── End Fading warning ─────────────────────────────
                        # Use cached dungeon if revisiting, otherwise create new
                        if dungeon_id in self.dungeon_cache:
                            self.dungeon_state = self.dungeon_cache[dungeon_id]
                            self.dungeon_state.party = self.party  # update party ref
                            # Update fading level in case story has progressed since last visit
                            self.dungeon_state.fading_level = getattr(self, "_pending_fading_level", 0)
                            # Reset to entrance of floor 1
                            floor = self.dungeon_state.floors[1]
                            self.dungeon_state.party_x, self.dungeon_state.party_y = floor["entrance"]
                            self.dungeon_state.current_floor = 1
                        else:
                            self.dungeon_state = DungeonState(dungeon_id, self.party,
                                                                fading_level=getattr(self, "_pending_fading_level", 0))
                            self.dungeon_cache[dungeon_id] = self.dungeon_state
                        self.dungeon_ui = DungeonUI(self.dungeon_state)
                        self.pre_dungeon_state = S_WORLD_MAP
                        self.go_fade(S_DUNGEON)
                        # Track floor 1 for job board
                        from data.job_board import on_dungeon_floor_reached
                        on_dungeon_floor_reached(dungeon_id, 1)
                        # Set explored flag (quest objectives check these)
                        from core.story_flags import set_flag as _sf_fl
                        _sf_fl(f"explored.{dungeon_id}.floor1", True)
                        auto_advance_quests = __import__("core.story_flags", fromlist=["auto_advance_quests"]).auto_advance_quests
                        _done = auto_advance_quests(self.party)
                        self._notify_quests_done(_done)
                        # Show floor 1 story message
                        from data.story_data import get_dungeon_floor_message
                        msg = get_dungeon_floor_message(dungeon_id, 1)
                        if msg:
                            self.dungeon_ui.show_event(msg, (180, 160, 120))
                        # Tutorial hints — first dungeon floor
                        from core.tutorial import fire_dungeon_hints
                        fire_dungeon_hints("first_floor", self.dungeon_ui)
                        print(f"[DEBUG] Entered dungeon! State={self.state}")
                    else:
                        self.world_map_ui._show_event(reason, RED)
                else:
                    # Dungeon not yet defined — generic combat
                    enc_key = loc.get("encounter_key", "tutorial")
                    self.start_combat(enc_key)
            elif loc["type"] == LOC_PORT:
                # Port — offer fast travel to other connected ports
                self._handle_port(event.get("id", ""), loc)

            elif loc["type"] == LOC_SECRET:
                # Secret location — show flavour + small reward on first visit
                self._handle_secret(event.get("id", ""), loc)

            elif loc["type"] == LOC_POI:
                # Point of interest — show description, possible encounter
                self._handle_poi(event.get("id", ""), loc)

            elif loc["type"] == LOC_STABLE:
                # Stable — handled via town has_stable flag; standalone stables not yet placed
                self.world_map_ui._show_event(
                    f"{loc['name']}: Horses available here.", (180, 140, 80))

        elif event["type"] == "discovery":
            sfx.play("discovery")

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
            # Use specific encounter key from visible enemy, or fall back to random
            enc_key = event.get("_enc_key") or self.dungeon_state.get_encounter_key()
            self.pre_dungeon_state = S_DUNGEON

            # Check for boss dialogue
            if event.get("is_boss"):
                from data.story_data import get_dungeon_boss_dialogue
                boss_npc = get_dungeon_boss_dialogue(self.dungeon_state.dungeon_id)
                if boss_npc:
                    dungeon_id = self.dungeon_state.dungeon_id
                    # Show dialogue first, then start combat or handle peaceful resolution
                    def after_boss_dialogue(result, _dungeon_id=dungeon_id, _enc_key=enc_key):
                        from data.story_data import get_peaceful_resolution
                        from core.story_flags import get_flag
                        res = get_peaceful_resolution(_dungeon_id)
                        if res and get_flag(res["flag"]):
                            # Peaceful path — grant items, then show post-boss dialogue
                            self._handle_peaceful_resolution(_dungeon_id, res)
                        else:
                            # Fight path
                            boss_enc = DUNGEONS[_dungeon_id].get("boss_encounter", _enc_key)
                            self.start_combat(boss_enc)
                    self.start_dialogue(boss_npc, return_state=S_DUNGEON,
                                        callback=after_boss_dialogue)
                    return
            self.start_combat(enc_key, surprise=event.get("surprise"))

        elif event["type"] == "fixed_encounter":
            enc_key = self.dungeon_state.get_encounter_key()
            self.pre_dungeon_state = S_DUNGEON
            self.start_combat(enc_key)

        elif event["type"] == "journal":
            data = event["data"]
            title = data.get("title", "Journal Entry")
            text = data.get("text", "")
            lore_id = data.get("lore_id")
            on_find = data.get("on_find", [])
            sfx.play("journal_find")
            from core.dialogue import _execute_action
            for action in on_find:
                _execute_action(action)
            # Discover lore if specified
            if lore_id:
                from core.story_flags import discover_lore
                discover_lore(lore_id)
            # Show journal text as dungeon event
            self.dungeon_ui.show_event(f"📜 {title}", GOLD)
            self.dungeon_ui.show_event(text, (180, 160, 120))
            # Mark the tile as read so the book icon clears
            t = self.dungeon_state.get_tile(self.dungeon_state.party_x,
                                            self.dungeon_state.party_y)
            if t:
                t["journal_read"] = True

        elif event["type"] == "interactable":
            data = event["data"]
            subtype = data.get("subtype", "")
            name = data.get("name", "Strange Object")
            hint = data.get("hint", "")

            if data.get("used"):
                self.dungeon_ui.show_event(f"{name} — already used.", GREY)
            elif subtype == "healing_pool":
                data["used"] = True
                heal_pct = data.get("heal_pct", 0.30)
                from core.classes import get_all_resources
                healed = []
                for c in self.party:
                    max_res = get_all_resources(c.class_name, c.stats, c.level)
                    max_hp = max_res.get("HP", 1)
                    old = c.resources.get("HP", 0)
                    c.resources["HP"] = min(max_hp, old + int(max_hp * heal_pct))
                    gained = c.resources["HP"] - old
                    if gained > 0:
                        healed.append(f"{c.name} +{gained}")
                sfx.play("camp_rest")
                self.dungeon_ui.show_event(f"🌊 {name}", (80, 200, 255))
                if healed:
                    self.dungeon_ui.show_event("  ".join(healed), GREEN)
                else:
                    self.dungeon_ui.show_event("Already at full health.", GREY)

            elif subtype == "mp_shrine":
                data["used"] = True
                restore_pct = data.get("restore_pct", 0.25)
                from core.classes import get_all_resources
                restored = []
                for c in self.party:
                    max_res = get_all_resources(c.class_name, c.stats, c.level)
                    for rk, mv in max_res.items():
                        if rk == "HP":
                            continue
                        cur = c.resources.get(rk, 0)
                        c.resources[rk] = min(mv, cur + int(mv * restore_pct))
                        gained = c.resources[rk] - cur
                        if gained > 0:
                            restored.append(f"{c.name} +{gained} {rk}")
                sfx.play("camp_rest")
                self.dungeon_ui.show_event(f"✨ {name}", (120, 100, 220))
                if restored:
                    self.dungeon_ui.show_event("  ".join(restored[:4]), (140, 180, 255))
                else:
                    self.dungeon_ui.show_event("Resources already full.", GREY)

            elif subtype == "cursed_altar":
                data["used"] = True
                import random as _rmod
                buff_chance = data.get("buff_chance", 0.55)
                if _rmod.random() < buff_chance:
                    # Good outcome — temporary HP boost
                    bonus = data.get("buff_hp", 20)
                    for c in self.party:
                        c.resources["HP"] = c.resources.get("HP", 0) + bonus
                    sfx.play("camp_rest")
                    self.dungeon_ui.show_event(f"🔮 {name} — dark power flows through you!", (180, 120, 255))
                    self.dungeon_ui.show_event(f"Party gained +{bonus} temporary HP!", GREEN)
                else:
                    # Bad outcome — damage
                    dmg = data.get("curse_dmg", 15)
                    for c in self.party:
                        c.resources["HP"] = max(1, c.resources.get("HP", 0) - dmg)
                    sfx.play("trap_trigger")
                    self.dungeon_ui.show_event(f"💀 {name} — a curse lashes out!", RED)
                    self.dungeon_ui.show_event(f"Party took {dmg} shadow damage!", ORANGE)
            else:
                self.dungeon_ui.show_event(f"{name}: {hint}", CREAM)

        elif event["type"] == "stairs_down":
            if self.dungeon_state.go_downstairs():
                sfx.play("stairs")
                floor = self.dungeon_state.current_floor
                self.dungeon_ui.show_event(f"Descended to Floor {floor}.", GOLD)
                self.dungeon_ui.on_floor_change()
                # Track exploration for job board
                from data.job_board import on_dungeon_floor_reached
                on_dungeon_floor_reached(self.dungeon_state.dungeon_id, floor)
                # Quest hooks: guild trial, act3 finale
                from core.story_flags import set_flag as _sf, start_quest as _sq, get_flag as _gf
                if floor >= 3:
                    _sf("guild_trial.complete", True)
                if self.dungeon_state.dungeon_id == "valdris_spire":
                    _sq("main_act3_finale")  # auto-start finale quest
                # Set explored flag (quest objectives check these)
                _sf(f"explored.{self.dungeon_state.dungeon_id}.floor{floor}", True)

                # Auto-advance quests (explore objectives)
                from core.story_flags import auto_advance_quests
                _done = auto_advance_quests(self.party)
                self._notify_quests_done(_done)
                # Show story floor message if available
                from data.story_data import get_dungeon_floor_message
                msg = get_dungeon_floor_message(self.dungeon_state.dungeon_id, floor)
                if msg:
                    self.dungeon_ui.show_event(msg, (180, 160, 120))
                # Tutorial hint — back row tip fires on second floor first visit
                if floor == 2:
                    from core.tutorial import fire_dungeon_hints
                    fire_dungeon_hints("second_floor", self.dungeon_ui)
                # Maren reunion — fires on Valdris Spire floor 5, once
                dungeon_id = self.dungeon_state.dungeon_id
                if dungeon_id == "valdris_spire" and floor == 5:
                    from core.story_flags import get_flag
                    if get_flag("maren.left") and not get_flag("maren.spire_reunion_done"):
                        from data.story_data import NPC_DIALOGUES
                        from core.dialogue import select_dialogue
                        dlg_list = NPC_DIALOGUES.get("maren_spire", [])
                        ds = select_dialogue("maren_spire", dlg_list)
                        if ds:
                            from ui.dialogue_ui import DialogueUI
                            self.dialogue_ui = DialogueUI(ds)
                            self.dialogue_return_state = S_DUNGEON
                            self.dialogue_callback = None
                            self.go(S_DIALOGUE)

        elif event["type"] == "stairs_up":
            if self.dungeon_state.go_upstairs():
                sfx.play("stairs")
                floor = self.dungeon_state.current_floor
                self.dungeon_ui.show_event(f"Ascended to Floor {floor}.", (80, 180, 220))

        elif event["type"] == "exit_dungeon":
            self.dungeon_state = None
            self.dungeon_ui = None
            if self.world_state:
                self.go_fade(S_WORLD_MAP)
            else:
                self.go(S_PARTY)

        elif event["type"] == "chest_approach":
            # Party stepped onto a chest — open the interaction modal
            chest_ev = event["data"]
            if self.dungeon_ui:
                self.dungeon_ui.chest_modal = {
                    "step":     "approach",
                    "chest_ev": chest_ev,
                    "chest_x":  event.get("x"),
                    "chest_y":  event.get("y"),
                }

        elif event["type"] == "chest_open":
            # Party chose to open the chest
            chest_ev = event["chest_ev"]
            # Bug 2 fix: if chest has an undiscovered/undisarmed trap, fire it now
            trap = chest_ev.get("trap")
            if trap and not trap.get("disarmed"):
                # Trap fires — redirect to trap handler
                sfx.play("trap_trigger")
                from data.dungeon import resolve_trap_saving_throw
                from core.status_effects import add_poison, add_curse
                trap_name   = trap.get("name", "Trap")
                dmg_base    = trap.get("damage", 10)
                trap_target = trap.get("target", "single")
                targets = list(self.party) if trap_target == "area" else [self.party[0]]
                msgs = []
                for ch in targets:
                    result = resolve_trap_saving_throw(ch, trap)
                    if result == "avoid":
                        msgs.append(f"{ch.name} dives clear of the {trap_name}!")
                    elif result == "half":
                        dmg = max(1, dmg_base // 2)
                        ch.hp = max(0, ch.hp - dmg)
                        msgs.append(f"{ch.name} partly evades {trap_name} — {dmg} damage!")
                    elif result == "crit_fail":
                        dmg = dmg_base
                        ch.hp = max(0, ch.hp - dmg)
                        msgs.append(f"{ch.name} CRITICALLY FAILS — {trap_name} hits for {dmg} damage!")
                    else:
                        dmg = dmg_base
                        ch.hp = max(0, ch.hp - dmg)
                        msgs.append(f"{ch.name} hit by {trap_name} for {dmg} damage!")
                    is_hit = result != "avoid"
                    if trap.get("poison") and is_hit:
                        add_poison(ch, trap["poison"])
                        sfx.play("poison")
                        msgs.append(f"{ch.name} is poisoned!")
                    if trap.get("curse") and is_hit:
                        add_curse(ch, trap["curse"])
                    if ch.hp <= 0:
                        ch.hp = 0
                        msgs.append(f"{ch.name} has fallen!")
                if self.dungeon_ui:
                    for msg in msgs:
                        self.dungeon_ui.show_event(msg, (220, 80, 60))
                trap["disarmed"] = True  # mark as fired so it doesn't re-trigger
            self.dungeon_state.open_chest(chest_ev)
            sfx.play("treasure_open")
            is_secret = chest_ev.get("secret_chest", False)
            gold  = chest_ev.get("gold", 0)
            items = chest_ev.get("items", [])
            if gold > 0:
                share = gold // len(self.party)
                remainder = gold % len(self.party)
                for i, c in enumerate(self.party):
                    c.gold += share + (1 if i < remainder else 0)
            from core.party_knowledge import auto_identify_if_known, mark_item_identified
            processed = []
            for item in items:
                item_copy = dict(item)
                if is_secret:
                    item_copy["identified"] = True
                auto_identify_if_known(item_copy)
                if item_copy.get("identified"):
                    mark_item_identified(item_copy.get("name", ""))
                processed.append(item_copy)

            # WIS chest bonus: high-WIS party notices hidden compartments
            best_wis = max((c.stats.get("WIS", 0) for c in self.party), default=0)
            if best_wis >= 15:
                bonus_chance = min(0.40, (best_wis - 14) * 0.04)  # +4% per WIS above 14, cap 40%
                if random.random() < bonus_chance:
                    try:
                        from data.magic_items import get_secret_item
                        floor_num = self.dungeon_state.current_floor + 1
                        total_floors = self.dungeon_state.total_floors
                        bonus_item = get_secret_item(floor_num, total_floors, random)
                        if bonus_item:
                            bonus_item["identified"] = False
                            bonus_item["_wis_bonus"] = True
                            processed.append(bonus_item)
                            if self.dungeon_ui:
                                self.dungeon_ui.show_event(
                                    "Sharp eyes find a hidden compartment!", (180, 220, 255))
                    except Exception:
                        pass

            self.start_chest(gold, processed, is_secret=is_secret, return_state=S_DUNGEON)

        elif event["type"] == "chest_trap_fire":
            # Party triggered a chest trap (force opened or failed disarm)
            sfx.play("trap_trigger")
            trap     = event["trap_data"]
            chest_ev = event["chest_ev"]
            import random as rmod
            from data.dungeon import resolve_trap_saving_throw
            from core.status_effects import add_poison, add_curse

            trap_name   = trap.get("name", "Trap")
            dmg_base    = trap.get("damage", 10)
            trap_target = trap.get("target", "single")

            if trap_target == "area":
                targets = list(self.party)
            else:
                targets = [self.party[0]]  # front character

            msgs = []
            for ch in targets:
                # resolve_trap_saving_throw returns a string: "avoid","half","full","crit_fail"
                result = resolve_trap_saving_throw(ch, trap)
                if result == "avoid":
                    msgs.append(f"{ch.name} dives clear of the {trap_name}!")
                elif result == "half":
                    dmg = max(1, dmg_base // 2)
                    ch.hp = max(0, ch.hp - dmg)
                    msgs.append(f"{ch.name} partly evades {trap_name} — {dmg} damage!")
                elif result == "crit_fail":
                    dmg = dmg_base
                    ch.hp = max(0, ch.hp - dmg)
                    msgs.append(f"{ch.name} CRITICALLY FAILS — {trap_name} hits for {dmg} damage!")
                else:  # "full"
                    dmg = dmg_base
                    ch.hp = max(0, ch.hp - dmg)
                    msgs.append(f"{ch.name} hit by {trap_name} for {dmg} damage!")
                is_hit = result != "avoid"
                if trap.get("poison") and is_hit:
                    add_poison(ch, trap["poison"])
                    sfx.play("poison")
                    msgs.append(f"{ch.name} is poisoned!")
                if trap.get("curse") and is_hit:
                    add_curse(ch, trap["curse"])
                    msgs.append(f"{ch.name} is cursed!")
                if ch.hp <= 0:
                    ch.hp = 0
                    msgs.append(f"{ch.name} has fallen!")

            if self.dungeon_ui:
                for msg in msgs:
                    self.dungeon_ui.show_event(msg, (220, 80, 60))

            # Chest still opens after the trap fires — contents aren't destroyed
            self.dungeon_state.open_chest(chest_ev)
            gold  = chest_ev.get("gold", 0)
            items = chest_ev.get("items", [])
            if gold > 0:
                share = gold // len(self.party)
                remainder = gold % len(self.party)
                for i, c in enumerate(self.party):
                    c.gold += share + (1 if i < remainder else 0)
            from core.party_knowledge import auto_identify_if_known, mark_item_identified
            processed = []
            for item in items:
                item_copy = dict(item)
                auto_identify_if_known(item_copy)
                if item_copy.get("identified"):
                    mark_item_identified(item_copy.get("name", ""))
                processed.append(item_copy)
            self.start_chest(gold, processed, return_state=S_DUNGEON)

        elif event["type"] == "treasure":

            sfx.play("treasure_open")
            data = event["data"]
            is_secret = data.get("secret_chest", False)
            gold = data.get("gold", 0)
            items = data.get("items", [])

            # Distribute gold evenly across party immediately
            if gold > 0:
                share = gold // len(self.party)
                remainder = gold % len(self.party)
                for i, c in enumerate(self.party):
                    c.gold += share + (1 if i < remainder else 0)

            # Auto-identify items as needed
            from core.party_knowledge import auto_identify_if_known, mark_item_identified
            processed = []
            for item in items:
                item_copy = dict(item)
                if is_secret:
                    item_copy["identified"] = True
                auto_identify_if_known(item_copy)
                if item_copy.get("identified"):
                    mark_item_identified(item_copy.get("name", ""))
                processed.append(item_copy)

            # Open chest loot UI so player can assign items to party members
            self.start_chest(gold, processed, is_secret=is_secret,
                             return_state=S_DUNGEON)

        elif event["type"] == "trap":
            sfx.play("trap_trigger")
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
                        sfx.play("poison")
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
                        sfx.play("poison")
                        results.append(f"{target.name} poisoned!")

            # Build display message
            if was_detected:
                prefix = f"Detected {trap_name} (Tier {data.get('tier',1)})!"
                color = ORANGE
                # Tutorial: first detected trap — hint about disarming
                from core.tutorial import fire_dungeon_hints
                fire_dungeon_hints("first_trap", self.dungeon_ui)
            else:
                prefix = f"{trap_name} (Tier {data.get('tier',1)})!"
                data["detected"] = True
                color = RED

            msg = prefix + " " + " | ".join(results[:4])  # limit display length
            self.dungeon_ui.show_event(msg, color)

        elif event["type"] == "camp":
            # Open camp screen instead of instant rest
            floor = self.dungeon_state.current_floor if self.dungeon_state else 1
            self.start_camp(location="dungeon", dungeon_floor=floor,
                            return_state=S_DUNGEON)

        elif event["type"] == "camp_rest_execute":
            # Actual rest execution (called from _end_camp)
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
                sfx.stop_music()
                sfx.play("victory")
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
                                sfx.play("poison")

                # ── Grant dungeon keys on boss victory ──
                if self.dungeon_state:
                    self._grant_boss_rewards(self.dungeon_state.dungeon_id)

                    # Mark visible enemy as dead on the map
                    contact_pos = getattr(self.dungeon_state, '_last_contact_enemy', None)
                    if contact_pos:
                        self.dungeon_state.kill_enemy_at(*contact_pos)
                        self.dungeon_state._last_contact_enemy = None

                # ── Track kills for job board bounties ──
                from data.job_board import on_enemy_killed
                for e in self.combat_state.enemies:
                    if not e.get("alive", True):
                        on_enemy_killed(e["name"])
                        # Track wolf pelts for side quest
                        if "Wolf" in e.get("name", "") or "wolf" in e.get("name", ""):
                            from core.story_flags import increment
                            increment("wolf_pelts_quest.count")

                # ── Auto-advance any quests whose objectives are now met ──
                from core.story_flags import auto_advance_quests, get_all_flags
                newly_done = auto_advance_quests(self.party)
                self._notify_quests_done(newly_done)

                # ── Auto-advance planar tier if story flags warrant it ──
                from core.progression import auto_advance_party_tier, PLANAR_TIERS
                tier_advances = auto_advance_party_tier(self.party, get_all_flags())
                if tier_advances:
                    _, old_t, new_t = tier_advances[0]
                    tier_info = PLANAR_TIERS[new_t]
                    self._notify_tier_up(tier_info)

                # ── Post-boss cutscene dialogue (fight path) ──
                # Fires for boss encounters only; regular enemies skip straight to loot.
                _dungeon_id = getattr(self.dungeon_state, "dungeon_id", None) if self.dungeon_state else None
                _is_boss_enc = getattr(self.combat_state, "is_boss", False)
                if _dungeon_id and _is_boss_enc:
                    self._show_post_boss_dialogue(
                        _dungeon_id, peaceful=False,
                        callback=lambda _: self.start_post_combat()
                    )
                else:
                    self.start_post_combat()
            else:
                # DEFEAT — TPK: show game over screen, then restore at inn
                sfx.stop_music()
                sfx.play("defeat")
                # Apply penalties immediately (seen on game over screen)
                for c in self.party:
                    c.resources["HP"] = 1
                    c.gold = int(c.gold * 0.75)  # 25% gold lost
                from core.status_effects import add_resurrection_sickness
                for c in self.party:
                    add_resurrection_sickness(c)
                # Store context for the game over screen
                self._game_over_dungeon = getattr(self.dungeon_state, "dungeon_id", None)
                self._game_over_timer   = 0.0
                self._game_over_ready   = False
                # Clear dungeon state — recovery happens after screen
                self.dungeon_state = None
                self.dungeon_ui    = None
                self.go(S_GAME_OVER)
            return

        if action["type"] == "attack":
            result = self.combat_state.execute_player_action("attack", target=action["target"])
            # Pick sound from what actually happened
            if result and result.get("hit") is False:
                sfx.play("miss")
            elif result and result.get("is_crit"):
                sfx.play("hit_critical")
            else:
                sfx.play("hit_physical")
            # Enemy killed?
            if result and result.get("defender", {}).get("alive") is False:
                sfx.play("death")
        elif action["type"] == "defend":
            self.combat_state.execute_player_action("defend")
            sfx.play("block")
        elif action["type"] == "ability":
            result = self.combat_state.execute_player_action(
                "ability", target=action["target"], ability=action["ability"]
            )
            # Pick sound and flash color based on ability type
            ab = action.get("ability", {})
            ab_type = ab.get("type", "") if isinstance(ab, dict) else ""
            ab_elem = ab.get("element", "") if isinstance(ab, dict) else ""
            ab_name = ab.get("name", "Ability") if isinstance(ab, dict) else "Ability"

            # Element → flash color
            _ELEM_COL = {
                "fire": (255, 110, 30), "ice": (80, 210, 255), "frost": (80, 210, 255),
                "lightning": (245, 225, 55), "nature": (80, 210, 80),
                "holy": (255, 245, 180), "shadow": (180, 80, 240),
                "poison": (130, 215, 65),
            }
            if ab_type in ("heal", "aoe_heal"):
                sfx.play("heal")
                if result:
                    amt = result.get("healing", 0)
                    self.combat_ui.add_flash(f"♥ {ab_name} +{amt} HP", (100, 255, 140))
            elif ab_type == "buff":
                sfx.play("buff")
                buff_name = ab.get("buff", ab_name)
                self.combat_ui.add_flash(f"✦ {buff_name.upper()} active!", (100, 220, 130))
            elif ab_type in ("debuff",):
                sfx.play("debuff")
                self.combat_ui.add_flash(f"↓ {ab_name}!", (220, 160, 60))
            else:
                sfx.play("hit_magic")
                if result and result.get("hit") is False:
                    self.combat_ui.add_flash(f"{ab_name} — RESISTED!", (150, 120, 180))
                elif result:
                    dmg = result.get("damage", 0)
                    is_crit = result.get("is_crit", False)
                    col = _ELEM_COL.get(ab_elem, (200, 160, 255))
                    if is_crit:
                        self.combat_ui.add_flash(f"✦ CRITICAL! {ab_name} {dmg}", (255, 215, 40))
                    elif ab_type == "aoe":
                        self.combat_ui.add_flash(f"◈ {ab_name} hits all! {dmg}", col)
                    else:
                        self.combat_ui.add_flash(f"◆ {ab_name} {dmg}", col)
        elif action["type"] == "move":
            self.combat_state.execute_player_action("move", target=action["direction"])
        elif action["type"] == "switch_weapon":
            self.combat_state.execute_player_action("switch_weapon", item=action["item"])

        elif action["type"] == "use_consumable":
            self.combat_state.execute_player_action("use_consumable", item=action["item"])
            sfx.play("heal")  # generic item sound

        elif action["type"] == "flee":
            # Tutorial: hint fires the first time flee is attempted
            from core.tutorial import fire_combat_hints
            fire_combat_hints("first_flee", self.combat_ui)
            self.combat_state.execute_player_action("flee")
            # Check if flee succeeded
            if self.combat_state.phase == "fled":
                self._handle_fled_combat()
                return

        # Reset UI mode after action
        self.combat_ui.action_mode = "main"


# ── Entry Point ───────────────────────────────────────────────

DEBUG_PARTY_CLASSES = ["Fighter", "Mage", "Cleric", "Thief", "Ranger", "Monk"]
DEBUG_PARTY_NAMES = ["Aldric", "Lyra", "Sera", "Kael", "Wren", "Zhen"]


def make_debug_party():
    """Quick-roll a full party for testing."""
    debug_races = ["Human", "Elf", "Dwarf", "Halfling", "Gnome", "Half-Orc"]
    party = []
    for i, (name, cls) in enumerate(zip(DEBUG_PARTY_NAMES, DEBUG_PARTY_CLASSES)):
        race = debug_races[i % len(debug_races)]
        c = Character(name, race_name=race)
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