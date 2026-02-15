"""
Realm of Shadows — Combat UI
Renders the battlefield, turn order bar, action menu, and combat log.
"""
import pygame
from ui.renderer import *
from core.combat_config import FRONT, MID, BACK

# ═══════════════════════════════════════════════════════════════
#  COLORS (combat-specific)
# ═══════════════════════════════════════════════════════════════

HP_GREEN     = (40, 180, 60)
HP_YELLOW    = (200, 180, 40)
HP_RED       = (200, 40, 40)
HP_BG        = (30, 25, 20)
MP_BLUE      = (60, 100, 200)
KI_PURPLE    = (140, 80, 200)
SP_ORANGE    = (200, 130, 40)
ENEMY_RED    = (180, 50, 50)
ENEMY_BORDER = (120, 40, 40)
ACTIVE_GLOW  = (255, 220, 80)
ROW_COLORS   = {FRONT: (180, 80, 80), MID: (180, 160, 60), BACK: (80, 120, 180)}
DEAD_COLOR   = (60, 60, 60)
MISS_COLOR   = (150, 150, 150)
CRIT_COLOR   = (255, 80, 80)
HEAL_COLOR   = (80, 255, 120)
LOG_BG       = (10, 8, 20)
ACTION_BG    = (25, 20, 45)
ACTION_HOVER = (50, 40, 85)


# ═══════════════════════════════════════════════════════════════
#  LAYOUT CONSTANTS
# ═══════════════════════════════════════════════════════════════

TURN_BAR_H    = 50
BATTLEFIELD_Y = TURN_BAR_H + 5
BATTLEFIELD_H = 420
LOG_Y         = BATTLEFIELD_Y + BATTLEFIELD_H + 5
LOG_H         = 180
ACTION_Y      = LOG_Y + LOG_H + 5
ACTION_H      = SCREEN_H - ACTION_Y - 5

# Battlefield zones
PLAYER_ZONE_X = 20
PLAYER_ZONE_W = 480
ENEMY_ZONE_X  = SCREEN_W - 500
ENEMY_ZONE_W  = 480
MID_ZONE_X    = PLAYER_ZONE_X + PLAYER_ZONE_W
MID_ZONE_W    = ENEMY_ZONE_X - MID_ZONE_X


# ═══════════════════════════════════════════════════════════════
#  HP BAR HELPER
# ═══════════════════════════════════════════════════════════════

def get_hp_color(hp, max_hp):
    ratio = hp / max(1, max_hp)
    if ratio > 0.6:
        return HP_GREEN
    elif ratio > 0.3:
        return HP_YELLOW
    return HP_RED


def draw_hp_bar(surface, x, y, w, h, hp, max_hp):
    pygame.draw.rect(surface, HP_BG, (x, y, w, h))
    if max_hp > 0:
        fill = max(0, int((hp / max_hp) * w))
        col = get_hp_color(hp, max_hp)
        pygame.draw.rect(surface, col, (x, y, fill, h))
    pygame.draw.rect(surface, PANEL_BORDER, (x, y, w, h), 1)


def draw_resource_bar(surface, x, y, w, h, current, maximum, color):
    pygame.draw.rect(surface, HP_BG, (x, y, w, h))
    if maximum > 0:
        fill = max(0, int((current / maximum) * w))
        pygame.draw.rect(surface, color, (x, y, fill, h))
    pygame.draw.rect(surface, PANEL_BORDER, (x, y, w, h), 1)


# ═══════════════════════════════════════════════════════════════
#  COMBAT UI CLASS
# ═══════════════════════════════════════════════════════════════

class CombatUI:
    """Handles all combat rendering and input state."""

    def __init__(self, combat_state):
        self.combat = combat_state
        self.action_mode = "main"  # main, target_attack, target_ability, choose_ability
        self.selected_ability = None
        self.hover_target = -1
        self.hover_action = -1
        self.log_scroll = 0
        self.flash_timer = 0
        self.flash_messages = []  # [(msg, color, timer)]
        self.enemy_anim_timer = 0
        self.auto_advance_timer = 0

    # ─────────────────────────────────────────────────────────
    #  MAIN DRAW
    # ─────────────────────────────────────────────────────────

    def draw(self, surface, mx, my):
        self.draw_turn_bar(surface, mx, my)
        self.draw_battlefield(surface, mx, my)
        self.draw_combat_log(surface)

        if self.combat.phase in ("victory", "defeat"):
            self.draw_end_screen(surface, mx, my)
        elif self.combat.is_player_turn():
            self.draw_action_menu(surface, mx, my)
        else:
            self.draw_enemy_thinking(surface)

        # Flash messages
        self.draw_flash_messages(surface)

    # ─────────────────────────────────────────────────────────
    #  TURN ORDER BAR
    # ─────────────────────────────────────────────────────────

    def draw_turn_bar(self, surface, mx, my):
        bar_rect = pygame.Rect(0, 0, SCREEN_W, TURN_BAR_H)
        pygame.draw.rect(surface, (15, 12, 28), bar_rect)
        pygame.draw.line(surface, PANEL_BORDER, (0, TURN_BAR_H), (SCREEN_W, TURN_BAR_H))

        draw_text(surface, f"Round {self.combat.round_num}", 10, 5, DIM_GOLD, 14, bold=True)
        draw_text(surface, "Turn Order:", 10, 26, DARK_GREY, 12)

        x = 130
        for i, c in enumerate(self.combat.turn_order):
            if not c["alive"]:
                continue
            is_current = (i == self.combat.current_turn_index)
            is_player = c["type"] == "player"

            # Background pill
            pill_w = max(100, len(c["name"]) * 10 + 20)
            pill_rect = pygame.Rect(x, 8, pill_w, 34)

            if is_current:
                pygame.draw.rect(surface, (60, 50, 20), pill_rect, border_radius=4)
                pygame.draw.rect(surface, ACTIVE_GLOW, pill_rect, 2, border_radius=4)
            else:
                bg = (25, 22, 45) if is_player else (35, 18, 18)
                pygame.draw.rect(surface, bg, pill_rect, border_radius=4)
                border = HIGHLIGHT if is_player else ENEMY_RED
                pygame.draw.rect(surface, border, pill_rect, 1, border_radius=4)

            col = WHITE if is_current else (CREAM if is_player else (200, 120, 120))
            draw_text(surface, c["name"], x + 8, 15, col, 13)

            x += pill_w + 8
            if x > SCREEN_W - 120:
                break

    # ─────────────────────────────────────────────────────────
    #  BATTLEFIELD
    # ─────────────────────────────────────────────────────────

    def draw_battlefield(self, surface, mx, my):
        bf_rect = pygame.Rect(0, BATTLEFIELD_Y, SCREEN_W, BATTLEFIELD_H)
        pygame.draw.rect(surface, (8, 6, 16), bf_rect)

        # Row labels in center
        center_x = SCREEN_W // 2
        for i, (label, row_key) in enumerate([("BACK", BACK), ("MID", MID), ("FRONT", FRONT)]):
            ly = BATTLEFIELD_Y + 20 + i * 135
            col = ROW_COLORS.get(row_key, DARK_GREY)
            # Left label (player side)
            draw_text(surface, label, PLAYER_ZONE_X + PLAYER_ZONE_W + 10, ly + 50,
                      (col[0]//2, col[1]//2, col[2]//2), 13)
            # Right label (enemy side)
            draw_text(surface, label, ENEMY_ZONE_X - 55, ly + 50,
                      (col[0]//2, col[1]//2, col[2]//2), 13)
            # Divider line
            pygame.draw.line(surface, (30, 25, 50),
                             (PLAYER_ZONE_X, ly + 120),
                             (SCREEN_W - 20, ly + 120))

        # Draw players
        self._draw_player_cards(surface, mx, my)

        # Draw enemies
        self._draw_enemy_cards(surface, mx, my)

        # VS divider
        pygame.draw.line(surface, (50, 40, 80),
                         (center_x, BATTLEFIELD_Y + 10),
                         (center_x, BATTLEFIELD_Y + BATTLEFIELD_H - 10))

    def _draw_player_cards(self, surface, mx, my):
        """Draw player character cards on the left side."""
        row_positions = {BACK: 0, MID: 1, FRONT: 2}

        for p in self.combat.players:
            row_idx = row_positions.get(p["row"], 0)
            # Find position within this row
            same_row = [pp for pp in self.combat.players if pp["row"] == p["row"]]
            pos_in_row = same_row.index(p)

            card_w = 220
            card_h = 115
            cx = PLAYER_ZONE_X + pos_in_row * (card_w + 10)
            cy = BATTLEFIELD_Y + 10 + row_idx * 135

            rect = pygame.Rect(cx, cy, card_w, card_h)
            is_active = (p == self.combat.get_current_combatant())

            if not p["alive"]:
                bg = (20, 15, 15)
                border = DEAD_COLOR
            elif is_active:
                bg = (35, 30, 55)
                border = ACTIVE_GLOW
            else:
                bg = PANEL_BG
                border = HIGHLIGHT

            pygame.draw.rect(surface, bg, rect, border_radius=3)
            pygame.draw.rect(surface, border, rect, 2, border_radius=3)

            # Name + class
            name_col = DEAD_COLOR if not p["alive"] else (WHITE if is_active else CREAM)
            draw_text(surface, p["name"], cx + 6, cy + 4, name_col, 15, bold=is_active)

            row_col = ROW_COLORS.get(p["row"], DARK_GREY)
            draw_text(surface, f"[{p['row'][0].upper()}]", cx + card_w - 28, cy + 4,
                      row_col, 13)

            if p["alive"]:
                # HP bar
                draw_hp_bar(surface, cx + 6, cy + 24, card_w - 12, 12,
                            p["hp"], p["max_hp"])
                draw_text(surface, f"{p['hp']}/{p['max_hp']}", cx + 6, cy + 38,
                          get_hp_color(p["hp"], p["max_hp"]), 12)

                # Key resources (compact)
                ry = cy + 54
                for rname in ("Ki", "INT-MP", "WIS-MP", "PIE-MP", "STR-SP", "DEX-SP"):
                    if rname in p["resources"]:
                        cur = p["resources"][rname]
                        mx_r = p["max_resources"][rname]
                        r_col = KI_PURPLE if rname == "Ki" else MP_BLUE if "MP" in rname else SP_ORANGE
                        short = rname.replace("-", "")
                        draw_text(surface, f"{short}:{cur}", cx + 6, ry, r_col, 12)
                        ry += 15
                        if ry > cy + card_h - 14:
                            break

                # Defending indicator
                if p.get("is_defending"):
                    draw_text(surface, "DEF", cx + card_w - 36, cy + 38, GOLD, 12, bold=True)
            else:
                draw_text(surface, "UNCONSCIOUS", cx + 30, cy + 48, DEAD_COLOR, 14)

    def _draw_enemy_cards(self, surface, mx, my):
        """Draw enemy cards on the right side."""
        row_positions = {FRONT: 2, MID: 1, BACK: 0}
        groups = self.combat.get_enemy_groups()

        is_targeting = self.action_mode in ("target_attack", "target_ability")
        self.hover_target = -1

        for gi, group in enumerate(groups):
            row_idx = row_positions.get(group["row"], 0)
            # Position within row
            same_row_groups = [g for g in groups if g["row"] == group["row"]]
            pos_in_row = same_row_groups.index(group)

            card_w = 220
            card_h = 110
            cx = ENEMY_ZONE_X + pos_in_row * (card_w + 10)
            cy = BATTLEFIELD_Y + 10 + row_idx * 135

            rect = pygame.Rect(cx, cy, card_w, card_h)
            is_hover = rect.collidepoint(mx, my) and is_targeting

            if is_hover:
                self.hover_target = gi
                bg = (50, 25, 25)
                border = (255, 100, 100)
            else:
                bg = (25, 15, 15)
                border = ENEMY_BORDER

            pygame.draw.rect(surface, bg, rect, border_radius=3)
            pygame.draw.rect(surface, border, rect, 2, border_radius=3)

            # Group name + count
            count = len(group["members"])
            name = group["name"]
            count_str = f" x{count}" if count > 1 else ""
            draw_text(surface, f"{name}{count_str}", cx + 6, cy + 4, ENEMY_RED, 15, bold=True)

            row_col = ROW_COLORS.get(group["row"], DARK_GREY)
            draw_text(surface, f"[{group['row'][0].upper()}]", cx + card_w - 28, cy + 4,
                      row_col, 13)

            # Show HP for each member
            ey = cy + 26
            for member in group["members"]:
                if member["alive"]:
                    draw_hp_bar(surface, cx + 6, ey, card_w - 12, 10,
                                member["hp"], member["max_hp"])
                    draw_text(surface, f"{member['hp']}/{member['max_hp']}",
                              cx + 6, ey + 12, get_hp_color(member["hp"], member["max_hp"]), 11)
                    ey += 26
                else:
                    draw_text(surface, "DEAD", cx + 6, ey, DEAD_COLOR, 11)
                    ey += 18

    # ─────────────────────────────────────────────────────────
    #  COMBAT LOG
    # ─────────────────────────────────────────────────────────

    def draw_combat_log(self, surface):
        log_rect = pygame.Rect(0, LOG_Y, SCREEN_W, LOG_H)
        pygame.draw.rect(surface, LOG_BG, log_rect)
        pygame.draw.rect(surface, PANEL_BORDER, log_rect, 1)

        draw_text(surface, "Combat Log", 10, LOG_Y + 4, DIM_GOLD, 13, bold=True)

        # Show last N messages
        visible = LOG_H // 18 - 1
        msgs = self.combat.combat_log
        start = max(0, len(msgs) - visible - self.log_scroll)
        end = start + visible

        y = LOG_Y + 22
        for i in range(start, min(end, len(msgs))):
            msg = msgs[i]
            # Color code messages
            if "CRITICAL" in msg:
                col = CRIT_COLOR
            elif "MISS" in msg or "RESISTED" in msg:
                col = MISS_COLOR
            elif "heals" in msg:
                col = HEAL_COLOR
            elif "fallen" in msg or "unconscious" in msg:
                col = ENEMY_RED
            elif "═══" in msg or "──" in msg:
                col = GOLD
            elif "regenerates" in msg:
                col = KI_PURPLE
            else:
                col = GREY
            draw_text(surface, msg, 10, y, col, 14, max_width=SCREEN_W - 20)
            y += 18

    # ─────────────────────────────────────────────────────────
    #  ACTION MENU (Player's Turn)
    # ─────────────────────────────────────────────────────────

    def draw_action_menu(self, surface, mx, my):
        action_rect = pygame.Rect(0, ACTION_Y, SCREEN_W, ACTION_H)
        pygame.draw.rect(surface, ACTION_BG, action_rect)
        pygame.draw.rect(surface, PANEL_BORDER, action_rect, 1)

        actor = self.combat.get_current_combatant()
        if not actor:
            return

        draw_text(surface, f"{actor['name']}'s Turn", 15, ACTION_Y + 8, GOLD, 18, bold=True)

        if self.action_mode == "main":
            self._draw_main_actions(surface, mx, my, actor)
        elif self.action_mode in ("target_attack", "target_ability"):
            draw_text(surface, "Select a target (click an enemy group above)",
                      15, ACTION_Y + 36, CREAM, 16)
            # Back button
            back_rect = pygame.Rect(SCREEN_W - 140, ACTION_Y + 8, 120, 34)
            hover = back_rect.collidepoint(mx, my)
            draw_button(surface, back_rect, "Back", hover=hover, size=14)
        elif self.action_mode == "choose_ability":
            self._draw_ability_menu(surface, mx, my, actor)

    def _draw_main_actions(self, surface, mx, my, actor):
        """Draw the main action buttons."""
        self.hover_action = -1
        actions = [
            ("Attack", "Basic weapon attack"),
            ("Defend", "+50% defense until next turn"),
        ]

        # Add abilities if any
        if actor.get("abilities"):
            actions.append(("Abilities", "Use a combat skill or spell"))

        bx = 15
        by = ACTION_Y + 36
        btn_w = 200
        btn_h = 48

        for i, (name, desc) in enumerate(actions):
            rect = pygame.Rect(bx + i * (btn_w + 12), by, btn_w, btn_h)
            hover = rect.collidepoint(mx, my)
            if hover:
                self.hover_action = i

            bg = ACTION_HOVER if hover else (30, 25, 50)
            border = GOLD if hover else PANEL_BORDER
            pygame.draw.rect(surface, bg, rect, border_radius=3)
            pygame.draw.rect(surface, border, rect, 2, border_radius=3)

            col = GOLD if hover else CREAM
            draw_text(surface, name, rect.x + 12, rect.y + 5, col, 17, bold=True)
            draw_text(surface, desc, rect.x + 12, rect.y + 28, DARK_GREY, 12)

    def _draw_ability_menu(self, surface, mx, my, actor):
        """Draw ability selection list."""
        draw_text(surface, "Choose an ability:", 15, ACTION_Y + 32, CREAM, 16)
        self.hover_action = -1

        bx = 15
        by = ACTION_Y + 56
        btn_w = 290
        btn_h = 42

        abilities = actor.get("abilities", [])
        for i, ab in enumerate(abilities):
            col_idx = i % 4
            row_idx = i // 4
            rect = pygame.Rect(bx + col_idx * (btn_w + 10),
                               by + row_idx * (btn_h + 6),
                               btn_w, btn_h)
            hover = rect.collidepoint(mx, my)
            if hover:
                self.hover_action = i

            # Check if affordable
            resource_key = ab.get("resource", "")
            cost = ab.get("cost", 0)
            affordable = True
            if resource_key and actor["type"] == "player":
                affordable = actor["resources"].get(resource_key, 0) >= cost

            bg = ACTION_HOVER if hover else (30, 25, 50)
            if not affordable:
                bg = (30, 15, 15)
            border = GOLD if hover else (PANEL_BORDER if affordable else (80, 30, 30))

            pygame.draw.rect(surface, bg, rect, border_radius=3)
            pygame.draw.rect(surface, border, rect, 2, border_radius=3)

            name_col = GOLD if hover else (CREAM if affordable else DEAD_COLOR)
            draw_text(surface, ab["name"], rect.x + 10, rect.y + 4, name_col, 15, bold=True)

            cost_str = f"{cost} {resource_key}" if resource_key else "Free"
            cost_col = DARK_GREY if affordable else HP_RED
            draw_text(surface, cost_str, rect.x + 10, rect.y + 24, cost_col, 12)

        # Back button
        back_rect = pygame.Rect(SCREEN_W - 140, ACTION_Y + 8, 120, 34)
        hover = back_rect.collidepoint(mx, my)
        draw_button(surface, back_rect, "Back", hover=hover, size=14)

    # ─────────────────────────────────────────────────────────
    #  ENEMY THINKING INDICATOR
    # ─────────────────────────────────────────────────────────

    def draw_enemy_thinking(self, surface):
        action_rect = pygame.Rect(0, ACTION_Y, SCREEN_W, ACTION_H)
        pygame.draw.rect(surface, ACTION_BG, action_rect)
        pygame.draw.rect(surface, PANEL_BORDER, action_rect, 1)

        actor = self.combat.get_current_combatant()
        name = actor["name"] if actor else "Enemy"
        dots = "." * (1 + (self.enemy_anim_timer // 400) % 3)
        draw_text(surface, f"{name} is acting{dots}",
                  15, ACTION_Y + 20, ENEMY_RED, 18)

    # ─────────────────────────────────────────────────────────
    #  END SCREEN (Victory / Defeat)
    # ─────────────────────────────────────────────────────────

    def draw_end_screen(self, surface, mx, my):
        action_rect = pygame.Rect(0, ACTION_Y, SCREEN_W, ACTION_H)
        pygame.draw.rect(surface, ACTION_BG, action_rect)
        pygame.draw.rect(surface, PANEL_BORDER, action_rect, 1)

        if self.combat.phase == "victory":
            draw_text(surface, "VICTORY!", 15, ACTION_Y + 8, GOLD, 24, bold=True)
            rewards = getattr(self.combat, "rewards", {})
            draw_text(surface, f"XP: {rewards.get('xp', 0)}    Gold: {rewards.get('gold', 0)}",
                      15, ACTION_Y + 40, CREAM, 17)
            # Continue button
            btn = pygame.Rect(SCREEN_W // 2 - 120, ACTION_Y + 65, 240, 42)
            hover = btn.collidepoint(mx, my)
            draw_button(surface, btn, "Continue", hover=hover, size=18)
        else:
            draw_text(surface, "DEFEAT", 15, ACTION_Y + 8, HP_RED, 24, bold=True)
            draw_text(surface, "Your party has fallen...", 15, ACTION_Y + 40, GREY, 17)
            # Retry button
            btn = pygame.Rect(SCREEN_W // 2 - 120, ACTION_Y + 65, 240, 42)
            hover = btn.collidepoint(mx, my)
            draw_button(surface, btn, "Retry", hover=hover, size=18)

    # ─────────────────────────────────────────────────────────
    #  FLASH MESSAGES (floating combat text)
    # ─────────────────────────────────────────────────────────

    def draw_flash_messages(self, surface):
        remaining = []
        for msg, col, timer in self.flash_messages:
            timer -= 16  # approx per frame
            if timer > 0:
                alpha = min(255, timer)
                y_offset = int((1000 - timer) * 0.03)
                surf = get_font(16, bold=True).render(msg, True, col)
                surf.set_alpha(alpha)
                surface.blit(surf, (SCREEN_W // 2 - surf.get_width() // 2,
                                    BATTLEFIELD_Y + 150 - y_offset))
                remaining.append((msg, col, timer))
        self.flash_messages = remaining

    def add_flash(self, msg, color=WHITE):
        self.flash_messages.append((msg, color, 1000))

    # ─────────────────────────────────────────────────────────
    #  INPUT HANDLING
    # ─────────────────────────────────────────────────────────

    def handle_click(self, mx, my):
        """Handle a mouse click. Returns an action dict or None."""
        if self.combat.phase in ("victory", "defeat"):
            btn = pygame.Rect(SCREEN_W // 2 - 100, ACTION_Y + 55, 200, 38)
            if btn.collidepoint(mx, my):
                return {"type": "end_combat", "result": self.combat.phase}
            return None

        if not self.combat.is_player_turn():
            return None

        # Check back button in targeting/ability modes
        back_rect = pygame.Rect(SCREEN_W - 120, ACTION_Y + 5, 100, 30)
        if self.action_mode != "main" and back_rect.collidepoint(mx, my):
            self.action_mode = "main"
            return None

        if self.action_mode == "main":
            if self.hover_action == 0:
                # Attack → enter targeting mode
                self.action_mode = "target_attack"
                return None
            elif self.hover_action == 1:
                # Defend
                return {"type": "defend"}
            elif self.hover_action == 2:
                # Abilities
                self.action_mode = "choose_ability"
                return None

        elif self.action_mode == "choose_ability":
            actor = self.combat.get_current_combatant()
            if actor and self.hover_action >= 0:
                abilities = actor.get("abilities", [])
                if self.hover_action < len(abilities):
                    ab = abilities[self.hover_action]
                    # Check if it's a heal (target allies) or offensive (target enemies)
                    if "heal" in ab["name"].lower():
                        # For now, auto-target lowest HP ally
                        living = self.combat.get_living_players()
                        if living:
                            target = min(living, key=lambda p: p["hp"] / max(1, p["max_hp"]))
                            self.action_mode = "main"
                            return {"type": "ability", "ability": ab, "target": target}
                    else:
                        self.selected_ability = ab
                        self.action_mode = "target_ability"
                    return None

        elif self.action_mode in ("target_attack", "target_ability"):
            if self.hover_target >= 0:
                groups = self.combat.get_enemy_groups()
                if self.hover_target < len(groups):
                    group = groups[self.hover_target]
                    # Pick first living member of the group
                    living = [m for m in group["members"] if m["alive"]]
                    if living:
                        target = living[0]
                        action_type = "attack" if self.action_mode == "target_attack" else "ability"
                        self.action_mode = "main"
                        result = {"type": action_type, "target": target}
                        if action_type == "ability":
                            result["ability"] = self.selected_ability
                        return result

        return None

    def handle_scroll(self, direction):
        """Handle mouse wheel scroll on combat log."""
        if direction > 0:
            self.log_scroll = min(
                max(0, len(self.combat.combat_log) - 5),
                self.log_scroll + 1
            )
        else:
            self.log_scroll = max(0, self.log_scroll - 1)
