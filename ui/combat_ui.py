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
        self.action_mode = "main"  # main, target_attack, target_ability, target_heal, choose_ability, choose_move
        self.selected_ability = None
        self.hover_target = -1
        self.hover_enemy = None
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
            is_heal_target = (self.action_mode == "target_heal")  # can heal downed allies too
            is_heal_hover = is_heal_target and rect.collidepoint(mx, my)

            if not p["alive"]:
                bg = (20, 15, 15)
                border = DEAD_COLOR
            elif is_heal_hover:
                bg = (25, 50, 30)
                border = (80, 255, 80)
            elif is_heal_target:
                bg = (20, 35, 25)
                border = (60, 180, 60)
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

                # Compact combat stats (damage range + defense)
                w = p.get("weapon", {})
                w_dmg = w.get("damage", 0)
                stat_d = 0
                for sk, wt in w.get("damage_stat", {}).items():
                    stat_d += p["stats"].get(sk, 0) * wt
                raw = stat_d + w_dmg
                d_lo, d_hi = max(1, int(raw * 0.85)), int(raw * 1.15)
                dfn = p.get("defense", 0)
                draw_text(surface, f"DMG:{d_lo}-{d_hi}  AC:{dfn}",
                          cx + 6, cy + card_h - 18, (160, 160, 180), 12)

                # Status effects (compact, right side)
                sx = cx + card_w - 6
                sy = cy + 54
                for status in p.get("status_effects", []):
                    sname = status["name"][:3].upper()
                    sdur = status["duration"]
                    s_col = self._status_color(status["name"])
                    label = f"{sname}:{sdur}"
                    tw = get_font(11).size(label)[0]
                    draw_text(surface, label, sx - tw, sy, s_col, 11)
                    sy += 14
            else:
                draw_text(surface, "UNCONSCIOUS", cx + 30, cy + 48, DEAD_COLOR, 14)

    def _draw_enemy_cards(self, surface, mx, my):
        """Draw individual enemy cards on the right side (one per enemy)."""
        row_positions = {FRONT: 2, MID: 1, BACK: 0}

        is_targeting = self.action_mode in ("target_attack", "target_ability", "target_heal")
        self.hover_enemy = None  # store the actual enemy dict on hover

        # Gather living enemies by row
        enemies_by_row = {FRONT: [], MID: [], BACK: []}
        for e in self.combat.enemies:
            enemies_by_row.setdefault(e["row"], []).append(e)

        for row_key in [BACK, MID, FRONT]:
            row_enemies = enemies_by_row.get(row_key, [])
            row_idx = row_positions.get(row_key, 0)

            for pos_in_row, enemy in enumerate(row_enemies):
                # Sizing: fit up to 4 enemies per row
                max_per_row = max(1, len(row_enemies))
                card_w = min(220, (ENEMY_ZONE_W - 10 * max_per_row) // max_per_row)
                card_h = 80
                cx = ENEMY_ZONE_X + pos_in_row * (card_w + 8)
                cy = BATTLEFIELD_Y + 10 + row_idx * 100

                rect = pygame.Rect(cx, cy, card_w, card_h)
                is_hover = rect.collidepoint(mx, my) and is_targeting and enemy["alive"]

                if not enemy["alive"]:
                    bg = (15, 10, 10)
                    border = DEAD_COLOR
                elif is_hover:
                    self.hover_enemy = enemy
                    bg = (50, 25, 25)
                    border = (255, 100, 100)
                else:
                    bg = (25, 15, 15)
                    border = ENEMY_BORDER

                pygame.draw.rect(surface, bg, rect, border_radius=3)
                pygame.draw.rect(surface, border, rect, 2, border_radius=3)

                # Name
                name_str = enemy["name"]
                # Append a letter suffix if multiple of same type (A, B, C...)
                same_name = [e for e in self.combat.enemies if e["name"] == enemy["name"]]
                if len(same_name) > 1:
                    idx = same_name.index(enemy)
                    name_str = f"{enemy['name']} {chr(65+idx)}"

                name_col = ENEMY_RED if enemy["alive"] else DEAD_COLOR
                draw_text(surface, name_str[:18], cx + 4, cy + 3, name_col, 12, bold=True)

                row_col = ROW_COLORS.get(row_key, DARK_GREY)
                draw_text(surface, f"[{row_key[0].upper()}]", cx + card_w - 22, cy + 3,
                          row_col, 10)

                # HP bar
                if enemy["alive"]:
                    draw_hp_bar(surface, cx + 4, cy + 22, card_w - 8, 9,
                                enemy["hp"], enemy["max_hp"])
                    draw_text(surface, f"{enemy['hp']}/{enemy['max_hp']}",
                              cx + 4, cy + 33, get_hp_color(enemy["hp"], enemy["max_hp"]), 10)
                else:
                    draw_text(surface, "DEAD", cx + 4, cy + 24, DEAD_COLOR, 11)

                # Status effects
                if enemy["alive"] and enemy.get("status_effects"):
                    sx = cx + 4
                    for status in enemy["status_effects"][:2]:
                        sname = status["name"][:3].upper()
                        sdur = status["duration"]
                        s_col = self._status_color(status["name"])
                        label = f"{sname}:{sdur}"
                        draw_text(surface, label, sx, cy + card_h - 16, s_col, 9)
                        sx += get_font(9).size(label)[0] + 4

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
            elif "Poisoned" in msg or "Burning" in msg or "Frostbitten" in msg or "Shocked" in msg:
                col = (80, 200, 80) if "Poisoned" in msg else (255, 120, 40) if "Burning" in msg else (100, 180, 255)
            elif "wears off" in msg:
                col = (140, 140, 180)
            elif "═══" in msg or "──" in msg:
                col = GOLD
            elif "empowered" in msg or "War Cry" in msg:
                col = (255, 120, 40)
            elif "moves from" in msg:
                col = (100, 180, 255)
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
            draw_text(surface, "Select a target (click an enemy above)",
                      15, ACTION_Y + 36, CREAM, 16)
            # Back button
            back_rect = pygame.Rect(SCREEN_W - 140, ACTION_Y + 8, 120, 34)
            hover = back_rect.collidepoint(mx, my)
            draw_button(surface, back_rect, "Back", hover=hover, size=14)
        elif self.action_mode == "target_heal":
            draw_text(surface, "Select an ally to heal (click a party member above)",
                      15, ACTION_Y + 36, GREEN, 16)
            # Back button
            back_rect = pygame.Rect(SCREEN_W - 140, ACTION_Y + 8, 120, 34)
            hover = back_rect.collidepoint(mx, my)
            draw_button(surface, back_rect, "Back", hover=hover, size=14)
        elif self.action_mode == "choose_ability":
            self._draw_ability_menu(surface, mx, my, actor)
        elif self.action_mode == "choose_move":
            self._draw_move_menu(surface, mx, my, actor)
        elif self.action_mode == "choose_item":
            self._draw_item_menu(surface, mx, my, actor)

    def _draw_main_actions(self, surface, mx, my, actor):
        """Draw the main action buttons."""
        self.hover_action = -1

        # Calculate weapon damage range for display
        w = actor.get("weapon", {})
        w_dmg = w.get("damage", 0)
        stat_d = sum(actor["stats"].get(sk, 0) * wt
                     for sk, wt in w.get("damage_stat", {}).items())
        raw = stat_d + w_dmg
        d_lo, d_hi = max(1, int(raw * 0.85)), int(raw * 1.15)

        actions = [
            ("Attack", f"Weapon attack ({d_lo}-{d_hi} dmg)"),
            ("Defend", "+50% defense until next turn"),
        ]

        # Add abilities if any
        if actor.get("abilities"):
            actions.append(("Abilities", "Use a combat skill or spell"))

        # Add move option with current position shown
        row_label = actor["row"].capitalize()
        actions.append(("Move", f"Change position (now: {row_label})"))

        # Add items option if character has usable inventory
        char_ref = actor.get("character_ref")
        if char_ref and (char_ref.inventory or any(char_ref.equipment.get(s) for s in ("weapon",))):
            actions.append(("Items", "Switch weapon or use an item"))

        bx = 15
        by = ACTION_Y + 36
        btn_w = 190
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

            # Cost + effect info
            cost_str = f"{cost} {resource_key}" if resource_key else "Free"
            # Show damage or healing power if available
            power = ab.get("power", 0)
            ab_type = ab.get("type", "")
            if power and ab_type == "attack":
                w = actor.get("weapon", {})
                w_dmg = w.get("damage", 0)
                stat_d = sum(actor["stats"].get(sk, 0) * wt
                             for sk, wt in w.get("damage_stat", {}).items())
                ab_raw = (stat_d + w_dmg) * power
                cost_str += f"  |  ~{int(ab_raw)} dmg"
            elif power and ab_type == "heal":
                cost_str += f"  |  ~{int(power * 10)} heal"
            cost_col = DARK_GREY if affordable else HP_RED
            draw_text(surface, cost_str, rect.x + 10, rect.y + 24, cost_col, 12)

        # Back button
        back_rect = pygame.Rect(SCREEN_W - 140, ACTION_Y + 8, 120, 34)
        hover = back_rect.collidepoint(mx, my)
        draw_button(surface, back_rect, "Back", hover=hover, size=14)

    def _draw_move_menu(self, surface, mx, my, actor):
        """Draw position movement options."""
        current_row = actor["row"]
        row_col = ROW_COLORS.get(current_row, DARK_GREY)
        draw_text(surface, f"Current position: {current_row.upper()}", 15, ACTION_Y + 32,
                  row_col, 16, bold=True)
        draw_text(surface, "Move costs your full action this turn.", 15, ACTION_Y + 52,
                  DARK_GREY, 13)

        self.hover_action = -1
        bx = 15
        by = ACTION_Y + 76
        btn_w = 250
        btn_h = 48

        # Build available directions
        directions = []
        if current_row != FRONT:
            target_row = MID if current_row == BACK else FRONT
            target_col = ROW_COLORS.get(target_row, DARK_GREY)
            directions.append(("forward", f"Move Forward → {target_row.upper()}", target_col))
        if current_row != BACK:
            target_row = MID if current_row == FRONT else BACK
            target_col = ROW_COLORS.get(target_row, DARK_GREY)
            directions.append(("backward", f"Move Back → {target_row.upper()}", target_col))

        for i, (direction, label, dir_col) in enumerate(directions):
            rect = pygame.Rect(bx + i * (btn_w + 12), by, btn_w, btn_h)
            hover = rect.collidepoint(mx, my)
            if hover:
                self.hover_action = i

            bg = ACTION_HOVER if hover else (30, 25, 50)
            border = GOLD if hover else PANEL_BORDER
            pygame.draw.rect(surface, bg, rect, border_radius=3)
            pygame.draw.rect(surface, border, rect, 2, border_radius=3)

            col = GOLD if hover else CREAM
            draw_text(surface, label, rect.x + 12, rect.y + 14, col, 16, bold=True)

        # Store directions for click handling
        self._move_directions = [d[0] for d in directions]

        if not directions:
            draw_text(surface, "Cannot move from this position!", bx, by + 10,
                      HP_RED, 16)

        # Back button
        back_rect = pygame.Rect(SCREEN_W - 140, ACTION_Y + 8, 120, 34)
        bhover = back_rect.collidepoint(mx, my)
        draw_button(surface, back_rect, "Back", hover=bhover, size=14)

    def _draw_item_menu(self, surface, mx, my, actor):
        """Draw combat item menu — weapon switching and usable items."""
        draw_text(surface, "Items (switching weapon costs your action)",
                  15, ACTION_Y + 32, CREAM, 14)

        self.hover_action = -1
        char_ref = actor.get("character_ref")
        if not char_ref:
            return

        bx = 15
        by = ACTION_Y + 56
        btn_w = 280
        btn_h = 38
        self._combat_items = []

        # Current weapon display
        cur_weapon = actor.get("weapon", {})
        draw_text(surface, f"Equipped: {cur_weapon.get('name', 'Unarmed')}",
                  15, ACTION_Y + 32, DIM_GOLD, 13)

        # List equippable weapons from inventory
        idx = 0
        for item in char_ref.inventory:
            item_type = item.get("type", "")
            if item_type == "weapon":
                name = item.get("name", item.get("unidentified_name", "Unknown"))
                dmg = item.get("damage", "?")
                label = f"Switch to: {name} (DMG {dmg})"
                rect = pygame.Rect(bx + (idx % 2) * (btn_w + 10),
                                   by + (idx // 2) * (btn_h + 6),
                                   btn_w, btn_h)
                hover = rect.collidepoint(mx, my)
                if hover:
                    self.hover_action = idx

                bg = ACTION_HOVER if hover else (30, 25, 50)
                border = GOLD if hover else PANEL_BORDER
                pygame.draw.rect(surface, bg, rect, border_radius=3)
                pygame.draw.rect(surface, border, rect, 2, border_radius=3)
                draw_text(surface, label, rect.x + 10, rect.y + 10,
                          GOLD if hover else CREAM, 13)

                self._combat_items.append(("weapon", item))
                idx += 1

        # Consumables — potions and scrolls usable in combat
        for item in char_ref.inventory:
            is_consumable = (
                item.get("type") in ("consumable", "potion", "food") or
                item.get("subtype") in ("potion", "scroll", "food")
            )
            if not is_consumable:
                continue
            name = item.get("name", "item")
            stack = item.get("stack", 1)
            stack_str = f" x{stack}" if stack > 1 else ""
            # Short description for combat readability
            if item.get("heal", 0):
                detail = f"+{item['heal']} HP"
            elif item.get("restore_mp", 0):
                detail = f"+{item['restore_mp']} MP"
            elif "Remove Curse" in name:
                detail = "lifts curse"
            elif "Identify" in name:
                detail = "identifies item"
            else:
                detail = item.get("subtype", "consumable")
            label = f"Use: {name}{stack_str}  ({detail})"
            rect = pygame.Rect(bx + (idx % 2) * (btn_w + 10),
                               by + (idx // 2) * (btn_h + 6),
                               btn_w, btn_h)
            hover = rect.collidepoint(mx, my)
            if hover:
                self.hover_action = idx
            bg = ACTION_HOVER if hover else (20, 40, 30)   # green tint for consumables
            border = (80, 200, 80) if hover else (40, 80, 40)
            pygame.draw.rect(surface, bg, rect, border_radius=3)
            pygame.draw.rect(surface, border, rect, 2, border_radius=3)
            draw_text(surface, label, rect.x + 10, rect.y + 10,
                      (140, 240, 140) if hover else (180, 220, 180), 13)
            self._combat_items.append(("consumable", item))
            idx += 1

        if idx == 0:
            draw_text(surface, "No weapons or usable items in inventory.",
                      bx, by + 10, DARK_GREY, 14)

        # Back button
        back_rect = pygame.Rect(SCREEN_W - 140, ACTION_Y + 8, 120, 34)
        bhover = back_rect.collidepoint(mx, my)
        draw_button(surface, back_rect, "Back", hover=bhover, size=14)

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
            rewards = getattr(self.combat, "rewards", {})
            draw_text(surface, "VICTORY!", 15, ACTION_Y + 8, GOLD, 24, bold=True)

            # Gold
            gold_each = rewards.get("gold_each", 0)
            draw_text(surface, f"Gold: {rewards.get('total_gold', 0)} ({gold_each} each)",
                      15, ACTION_Y + 38, CREAM, 15)

            # XP per character
            xp_awards = rewards.get("xp_awards", {})
            xy = ACTION_Y + 58
            for uid, info in xp_awards.items():
                pct = f"{info['share_pct']*100:.0f}%"
                rounds_str = f"{info['rounds_alive']}/{info['total_rounds']}r"
                status = "  [KO]" if not info["alive"] else ""
                col = DEAD_COLOR if not info["alive"] else CREAM
                draw_text(surface, f"{info['name']}: {info['xp']} XP ({pct}, {rounds_str}){status}",
                          30, xy, col, 13)
                xy += 18

            # Loot drops
            loot = rewards.get("loot_drops", [])
            if loot:
                draw_text(surface, f"Loot ({len(loot)} items):", 420, ACTION_Y + 38, GOLD, 15, bold=True)
                ly = ACTION_Y + 58
                for item in loot:
                    if item.get("identified"):
                        label = item["name"]
                        col = self._rarity_color(item.get("rarity", "common"))
                    else:
                        label = f"??? {item.get('type', 'Item')}"
                        col = GREY
                    draw_text(surface, label, 435, ly, col, 13)
                    ly += 18

            # Continue button
            btn = pygame.Rect(SCREEN_W // 2 - 120, ACTION_Y + ACTION_H - 52, 240, 42)
            hover = btn.collidepoint(mx, my)
            draw_button(surface, btn, "Continue", hover=hover, size=18)
        else:
            draw_text(surface, "DEFEAT", 15, ACTION_Y + 8, HP_RED, 24, bold=True)
            draw_text(surface, "Your party has fallen...", 15, ACTION_Y + 40, GREY, 17)
            # Retry button
            btn = pygame.Rect(SCREEN_W // 2 - 120, ACTION_Y + ACTION_H - 52, 240, 42)
            hover = btn.collidepoint(mx, my)
            draw_button(surface, btn, "Retry", hover=hover, size=18)

    RARITY_COLORS = {
        "common":    CREAM,
        "uncommon":  (80, 220, 80),
        "rare":      (80, 140, 255),
        "epic":      (180, 80, 255),
        "legendary": (255, 180, 40),
    }

    def _rarity_color(self, rarity):
        return self.RARITY_COLORS.get(rarity, CREAM)

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
    #  STATUS EFFECT COLORS
    # ─────────────────────────────────────────────────────────

    STATUS_COLORS = {
        # Debuffs / DoTs
        "Poisoned":    (80, 200, 80),
        "Burning":     (255, 120, 40),
        "Frostbitten": (100, 180, 255),
        "Shocked":     (255, 255, 80),
        "Stunned":     (200, 200, 60),
        "Frozen":      (80, 160, 255),
        "Petrified":   (140, 130, 120),
        "Blinded":     (120, 100, 80),
        "Fear":        (180, 80, 180),
        "Silenced":    (160, 80, 160),
        "Slowed":      (100, 100, 200),
        "Sleep":       (140, 140, 200),
        "Taunted":     (200, 80, 60),
        # Buffs (player)
        "Hasted":        (80, 255, 80),
        "WarCry":        (255, 100, 40),
        "war_cry":       (255, 100, 40),
        "defense_up":    (60, 180, 255),
        "iron_skin":     (140, 160, 100),
        "evasion":       (160, 220, 120),
        "smoke_screen":  (140, 140, 180),
        "magic_shield":  (100, 140, 255),
        "bulwark":       (200, 180, 80),
        "ki_deflect":    (180, 120, 220),
        "hawk_eye":      (220, 200, 80),
        "last_stand":    (255, 60, 60),
        "courage_aura":  (240, 220, 100),
        "empty_mind":    (180, 200, 255),
        "tracking":      (100, 200, 120),
    }

    def _status_color(self, name):
        return self.STATUS_COLORS.get(name, GREY)

    # ─────────────────────────────────────────────────────────
    #  INPUT HANDLING
    # ─────────────────────────────────────────────────────────

    def handle_click(self, mx, my):
        """Handle a mouse click. Returns an action dict or None."""
        if self.combat.phase in ("victory", "defeat"):
            btn = pygame.Rect(SCREEN_W // 2 - 120, ACTION_Y + ACTION_H - 52, 240, 42)
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
            actor = self.combat.get_current_combatant()
            # Rebuild action list to get the label at hover_action
            action_labels = ["Attack", "Defend"]
            if actor and actor.get("abilities"):
                action_labels.append("Abilities")
            action_labels.append("Move")
            char_ref = actor.get("character_ref") if actor else None
            if char_ref and (char_ref.inventory or any(char_ref.equipment.get(s) for s in ("weapon",))):
                action_labels.append("Items")

            if self.hover_action >= 0 and self.hover_action < len(action_labels):
                label = action_labels[self.hover_action]
                if label == "Attack":
                    self.action_mode = "target_attack"
                elif label == "Defend":
                    return {"type": "defend"}
                elif label == "Abilities":
                    self.action_mode = "choose_ability"
                elif label == "Move":
                    self.action_mode = "choose_move"
                elif label == "Items":
                    self.action_mode = "choose_item"
            return None

        elif self.action_mode == "choose_ability":
            actor = self.combat.get_current_combatant()
            if actor and self.hover_action >= 0:
                abilities = actor.get("abilities", [])
                if self.hover_action < len(abilities):
                    ab = abilities[self.hover_action]
                    ab_type = ab.get("type", "spell")
                    # Route to proper target mode based on ability type
                    if ab_type in ("heal", "buff", "cure") or "heal" in ab["name"].lower():
                        self.selected_ability = ab
                        self.action_mode = "target_heal"  # targets allies
                    else:
                        self.selected_ability = ab
                        self.action_mode = "target_ability"  # targets enemies
                    return None

        elif self.action_mode == "choose_move":
            if self.hover_action >= 0:
                directions = getattr(self, "_move_directions", [])
                if self.hover_action < len(directions):
                    direction = directions[self.hover_action]
                    self.action_mode = "main"
                    return {"type": "move", "direction": direction}
            return None

        elif self.action_mode == "choose_item":
            if self.hover_action >= 0:
                items = getattr(self, "_combat_items", [])
                if self.hover_action < len(items):
                    action_type, item = items[self.hover_action]
                    if action_type == "weapon":
                        # Switch weapon — costs action
                        self.action_mode = "main"
                        return {"type": "switch_weapon", "item": item}
                    elif action_type == "consumable":
                        # Use consumable — costs action, needs target selection for heals
                        self.action_mode = "main"
                        return {"type": "use_consumable", "item": item}
            return None

        elif self.action_mode in ("target_attack", "target_ability"):
            if self.hover_enemy and self.hover_enemy["alive"]:
                target = self.hover_enemy
                action_type = "attack" if self.action_mode == "target_attack" else "ability"
                self.action_mode = "main"
                result = {"type": action_type, "target": target}
                if action_type == "ability":
                    result["ability"] = self.selected_ability
                return result

        elif self.action_mode == "target_heal":
            # Click on a player card to heal them (including downed allies for revival)
            from core.combat_config import BACK, MID, FRONT
            row_positions = {BACK: 0, MID: 1, FRONT: 2}
            for p in self.combat.players:
                row_idx = row_positions.get(p["row"], 0)
                same_row = [pp for pp in self.combat.players if pp["row"] == p["row"]]
                pos_in_row = same_row.index(p)
                card_w = 220
                card_h = 115
                cx = PLAYER_ZONE_X + pos_in_row * (card_w + 10)
                cy = BATTLEFIELD_Y + 10 + row_idx * 135
                rect = pygame.Rect(cx, cy, card_w, card_h)
                if rect.collidepoint(mx, my):
                    self.action_mode = "main"
                    return {"type": "ability", "ability": self.selected_ability, "target": p}

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
