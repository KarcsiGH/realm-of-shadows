"""
Realm of Shadows — Combat UI  (v2 — full layout rebuild)

Layout (1440×900):
  ┌─────────────────── TURN BAR (44px) ────────────────────────────────┐
  │ LEFT COL (280px)  │  ENEMY ZONE (1150px)                           │
  │                   │  ┌─ BACK ROW ──────────────────────────────┐   │
  │  Character cards  │  │  cards ...                               │   │
  │  class silhouette │  ├─ MID ROW ───────────────────────────────┤   │
  │  HP/MP/SP bars    │  │  cards ...                               │   │
  │  current turn hl  │  ├─ FRONT ROW ─────────────────────────────┤   │
  │                   │  │  cards ...                               │   │
  │  (extends to      │  ├─────────────────────────────────────────┤   │
  │   action bar)     │  │  COMBAT LOG (scrollable)                 │   │
  │                   │  └─────────────────────────────────────────┘   │
  ├───────────────── ACTION BAR (full width, 100px) ──────────────────┤
  │  [Attack]  [Spell]  [Skill]  [Item]  [Defend]  [Flee]              │
  └─────────────────────────────────────────────────────────────────────┘
  Popovers appear above the action bar when a button is clicked.
"""
import pygame
import math
from ui.renderer import (
    SCREEN_W, SCREEN_H, GOLD, CREAM, GREY, DARK_GREY, WHITE, BLACK,
    PANEL_BG, PANEL_BORDER, HIGHLIGHT, DIM_GOLD, ORANGE, RED, HEAL_COL,
    draw_text, get_font,
)
from ui.silhouettes import draw_character_silhouette, draw_enemy_silhouette, CLASS_COLORS
from core.combat_config import FRONT, MID, BACK
from core.party_knowledge import get_enemy_display_name

# ═══════════════════════════════════════════════════════════════
#  COLORS
# ═══════════════════════════════════════════════════════════════
HP_GREEN     = (40, 180,  60)
HP_YELLOW    = (200, 180,  40)
HP_RED       = (200,  40,  40)
HP_BG        = (30, 25, 20)
MP_BLUE      = (50,  90, 210)
SP_ORANGE    = (200, 140,  40)
KI_GREEN     = (40, 160,  80)
DEAD_COLOR   = (55,  50,  65)
CRIT_COLOR   = (255,  80,  80)
HEAL_COLOR   = (80, 255, 120)
MISS_COLOR   = (150, 150, 150)
LOG_BG       = (8,   6,  18)
LOG_BORDER   = (40,  35,  60)
ACT_BG       = (14,  11,  28)
ACT_HOVER    = (40,  32,  70)
ACT_ACTIVE   = (55,  44,  95)
POP_BG       = (18,  14,  35)
POP_BORDER   = (80,  65, 130)
POP_HOVER    = (38,  30,  68)
ROW_COLORS   = {FRONT: (200, 80, 80), MID: (200, 170, 50), BACK: (80, 130, 200)}
ENEMY_BG     = (22,  14,  20)
ENEMY_HOVER_BG = (45, 25, 35)
PLAYER_BG    = (16,  14,  28)
PLAYER_ACTIVE_BG = (30, 22, 50)

# ═══════════════════════════════════════════════════════════════
#  LAYOUT
# ═══════════════════════════════════════════════════════════════
TURN_H       = 44
ACTION_H     = 100
ACTION_Y     = SCREEN_H - ACTION_H

LEFT_W       = 285
LEFT_X       = 0
LEFT_Y       = TURN_H
LEFT_H       = ACTION_Y - TURN_H

RIGHT_X      = LEFT_W
RIGHT_W      = SCREEN_W - LEFT_W
RIGHT_Y      = TURN_H

ENEMY_H      = int((ACTION_Y - TURN_H) * 0.62)   # ~62% of middle area
LOG_Y        = TURN_H + ENEMY_H
LOG_H        = ACTION_Y - LOG_Y

# Row geometry inside enemy zone
ROW_LABEL_W  = 52
ROW_AREA_X   = RIGHT_X + ROW_LABEL_W
ROW_AREA_W   = RIGHT_W - ROW_LABEL_W - 6
ROW_H        = ENEMY_H // 3

# Action bar buttons
_ACT_LABELS  = ["Attack", "Spell", "Skill", "Item", "Defend", "Flee"]
_ACT_W       = SCREEN_W // len(_ACT_LABELS)

RES_COLORS = {
    "HP": (HP_BG,     HP_GREEN,  (190, 150, 145)),
    "MP": ((12,12,55), MP_BLUE,  (130, 140, 215)),
    "SP": ((40,30,10), SP_ORANGE,(210, 180, 80)),
    "Ki": ((10,35,20), KI_GREEN, (100, 200, 130)),
    "EP": ((35,10,35),(150,60,180),(180,120,210)),
}


# ═══════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════
def _hp_color(hp, max_hp):
    if max_hp <= 0: return DEAD_COLOR
    r = hp / max_hp
    if r > 0.5:  return HP_GREEN
    if r > 0.25: return HP_YELLOW
    return HP_RED

def _draw_resource_bar(surface, x, y, w, h, cur, mx_, colors):
    bg, fill, _ = colors
    frac = max(0, min(1, cur / max(1, mx_)))
    pygame.draw.rect(surface, bg,   (x, y, w, h))
    if frac > 0:
        pygame.draw.rect(surface, fill, (x, y, int(w * frac), h))

def _draw_panel(surface, rect, bg=PANEL_BG, border=PANEL_BORDER, radius=4):
    pygame.draw.rect(surface, bg,     rect, border_radius=radius)
    pygame.draw.rect(surface, border, rect, 1, border_radius=radius)

def _wrap(text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if font.size(test)[0] <= max_w:
            cur = test
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines or [""]


# ═══════════════════════════════════════════════════════════════
#  COMBAT UI
# ═══════════════════════════════════════════════════════════════
class CombatUI:
    def __init__(self, combat_state):
        self.combat = combat_state

        # Targeting / popover state
        self.action_mode    = "main"       # main | target_attack | target_ability | target_heal
        self.selected_ability = None
        self.popover        = None         # None | "attack"|"spell"|"skill"|"item"|"move"
        self.popover_scroll = 0
        self._popover_items = []           # list of (label, data) for current popover
        self._combat_items  = []
        self._move_directions = []

        # Hover tracking
        self.hover_enemy    = None         # enemy dict under cursor
        self.hover_player   = None         # player dict under cursor
        self.hover_action   = -1
        self.hover_pop_item = -1

        # Log
        self.log_scroll     = 0

        # Flash / animations
        self.flash_messages = []           # [(msg, color, timer_ms)]
        self.enemy_anim_timer = 0
        self.auto_advance_timer = 0

    # ─────────────────────────────────────────────────────────
    #  MAIN DRAW
    # ─────────────────────────────────────────────────────────
    def draw(self, surface, mx, my):
        surface.fill((8, 6, 16))

        self._draw_turn_bar(surface, mx, my)
        self._draw_left_col(surface, mx, my)
        self._draw_enemy_zone(surface, mx, my)
        self._draw_log(surface)
        self._draw_action_bar(surface, mx, my)

        # Popover on top of everything
        if self.popover:
            self._draw_popover(surface, mx, my)

        # End screen
        if self.combat.phase in ("victory", "defeat"):
            self._draw_end_screen(surface, mx, my)

        # Enemy thinking indicator
        if not self.combat.is_player_turn() and self.combat.phase == "player_turn":
            self._draw_enemy_thinking(surface)

        self._draw_flash(surface)

    # ─────────────────────────────────────────────────────────
    #  TURN ORDER BAR
    # ─────────────────────────────────────────────────────────
    def _draw_turn_bar(self, surface, mx, my):
        pygame.draw.rect(surface, (14, 11, 26), (0, 0, SCREEN_W, TURN_H))
        pygame.draw.line(surface, PANEL_BORDER, (0, TURN_H), (SCREEN_W, TURN_H))

        order = self.combat.turn_order
        cur   = self.combat.get_current_combatant()
        slot_w = min(120, SCREEN_W // max(1, len(order)))
        x = 6
        for c in order:
            is_cur = (c is cur)
            is_p   = c in self.combat.players
            r = pygame.Rect(x, 4, slot_w - 4, TURN_H - 8)
            bg = PLAYER_ACTIVE_BG if (is_p and is_cur) else \
                 (ENEMY_HOVER_BG  if (not is_p and is_cur) else
                 (PLAYER_BG       if is_p else ENEMY_BG))
            border = GOLD if is_cur else PANEL_BORDER
            _draw_panel(surface, r, bg, border)
            name = c.get("name", "?")[:10]
            hp, mhp = c.get("hp", 0), c.get("max_hp", 1)
            col = _hp_color(hp, mhp) if c.get("alive") else DEAD_COLOR
            fw = max(0, int((r.w - 2) * hp / max(1, mhp)))
            pygame.draw.rect(surface, (30, 10, 10), (r.x + 1, r.y + r.h - 5, r.w - 2, 4))
            if fw: pygame.draw.rect(surface, col, (r.x + 1, r.y + r.h - 5, fw, 4))
            draw_text(surface, name, r.x + 4, r.y + 4, GOLD if is_cur else CREAM, 11, bold=is_cur)
            x += slot_w

    # ─────────────────────────────────────────────────────────
    #  LEFT COLUMN — CHARACTER CARDS
    # ─────────────────────────────────────────────────────────
    def _draw_left_col(self, surface, mx, my):
        pygame.draw.rect(surface, (12, 10, 22), (LEFT_X, LEFT_Y, LEFT_W, LEFT_H))
        pygame.draw.line(surface, PANEL_BORDER, (LEFT_W, LEFT_Y), (LEFT_W, ACTION_Y))

        cur = self.combat.get_current_combatant()
        n   = max(1, len(self.combat.players))
        card_h = min(LEFT_H // n, 140)
        self.hover_player = None

        for i, p in enumerate(self.combat.players):
            cy = LEFT_Y + i * card_h
            r  = pygame.Rect(LEFT_X + 3, cy + 2, LEFT_W - 6, card_h - 4)
            is_cur = (p is cur)
            is_dead = not p.get("alive", True)
            is_target = (self.action_mode == "target_heal") and not is_dead

            bg = PLAYER_ACTIVE_BG if is_cur else PLAYER_BG
            border = GOLD if is_cur else ((200, 200, 80) if (is_target and r.collidepoint(mx, my))
                                          else PANEL_BORDER)
            if r.collidepoint(mx, my):
                self.hover_player = p
                if not is_cur:
                    bg = (22, 18, 40)

            _draw_panel(surface, r, bg, border)

            # Silhouette (left side of card)
            sil_w, sil_h = 52, card_h - 10
            sil_r = pygame.Rect(r.x + 3, r.y + 3, sil_w, sil_h)
            cls = p.get("class_name", "Fighter")
            equip = p.get("equipment", {})
            armor_tier = None
            if equip.get("armor"): armor_tier = equip["armor"].get("armor_tier")
            draw_character_silhouette(surface, sil_r, cls,
                                       equipped_weapon=equip.get("weapon"),
                                       armor_tier=armor_tier,
                                       highlight=is_cur and not is_dead)

            # Info right of silhouette
            ix = r.x + sil_w + 8
            iy = r.y + 3
            iw = r.w - sil_w - 12

            name_col = DEAD_COLOR if is_dead else (GOLD if is_cur else CREAM)
            draw_text(surface, p["name"][:14], ix, iy, name_col, 12, bold=is_cur)
            draw_text(surface, f"Lv.{p.get('level', 1)} {cls[:10]}", ix, iy + 14,
                      DARK_GREY, 10)

            if is_dead:
                draw_text(surface, "FALLEN", ix, iy + 30, DEAD_COLOR, 11, bold=True)
                continue

            # Resource bars
            bar_y = iy + 28
            bar_h_each = 7
            bar_gap = 12

            # HP always first
            hp  = p.get("hp", 0)
            mhp = p.get("max_hp", 1)
            _draw_resource_bar(surface, ix, bar_y, iw, bar_h_each, hp, mhp,
                                RES_COLORS["HP"])
            draw_text(surface, f"HP {hp}/{mhp}", ix, bar_y + bar_h_each + 1,
                      (190, 150, 145), 9)
            bar_y += bar_gap + bar_h_each

            # Other resources
            res = p.get("resources", {})
            stats = p.get("stats", {})
            try:
                from core.classes import get_all_resources
                max_res = get_all_resources(cls, stats, p.get("level", 1))
            except Exception:
                max_res = {}

            for rk in [k for k in res if k != "HP"][:2]:
                cur_r = res.get(rk, 0)
                max_r = max(1, max_res.get(rk, cur_r) or cur_r)
                rc = RES_COLORS.get(rk, RES_COLORS["MP"])
                _draw_resource_bar(surface, ix, bar_y, iw, bar_h_each, cur_r, max_r, rc)
                draw_text(surface, f"{rk} {cur_r}/{max_r}", ix, bar_y + bar_h_each + 1,
                          rc[2], 9)
                bar_y += bar_gap + bar_h_each
                if bar_y > r.bottom - 10:
                    break

            # Status effects
            se = p.get("status_effects", {})
            if se:
                sx = ix
                for sname in list(se.keys())[:3]:
                    draw_text(surface, sname[:6], sx, r.bottom - 13, ORANGE, 9)
                    sx += 40

    # ─────────────────────────────────────────────────────────
    #  ENEMY ZONE
    # ─────────────────────────────────────────────────────────
    def _draw_enemy_zone(self, surface, mx, my):
        zone_r = pygame.Rect(RIGHT_X, RIGHT_Y, RIGHT_W, ENEMY_H)
        pygame.draw.rect(surface, (10, 8, 18), zone_r)

        is_targeting = self.action_mode in ("target_attack", "target_ability")
        self.hover_enemy = None

        rows = [BACK, MID, FRONT]
        enemies_by_row = {r: [] for r in rows}
        for e in self.combat.enemies:
            enemies_by_row.setdefault(e["row"], []).append(e)

        for ri, row_key in enumerate(rows):
            ry = RIGHT_Y + ri * ROW_H
            # Row label
            row_label = row_key[0].upper() + row_key[1:]
            rc = ROW_COLORS[row_key]
            pygame.draw.rect(surface, (rc[0]//5, rc[1]//5, rc[2]//5),
                             (RIGHT_X, ry, ROW_LABEL_W, ROW_H))
            draw_text(surface, row_label, RIGHT_X + 4, ry + ROW_H//2 - 7, rc, 11, bold=True)
            pygame.draw.line(surface, PANEL_BORDER, (RIGHT_X, ry), (SCREEN_W, ry))

            row_enemies = enemies_by_row.get(row_key, [])
            if not row_enemies:
                draw_text(surface, "—", ROW_AREA_X + ROW_AREA_W // 2 - 4,
                          ry + ROW_H // 2 - 7, DARK_GREY, 12)
                continue

            n = len(row_enemies)
            # Each card normally; hovered card is larger
            NORM_W, NORM_H = 180, ROW_H - 14
            HOVERED_W, HOVERED_H = 230, ROW_H + 20  # expands

            # Calculate positions
            total_norm_w = n * NORM_W + (n - 1) * 8
            start_x = ROW_AREA_X + (ROW_AREA_W - total_norm_w) // 2

            for ei, enemy in enumerate(row_enemies):
                cx = start_x + ei * (NORM_W + 8)
                cy = ry + 7

                is_hover = False
                card_r = pygame.Rect(cx, cy, NORM_W, NORM_H)
                if card_r.collidepoint(mx, my) and enemy.get("alive"):
                    is_hover = True
                    self.hover_enemy = enemy

                # Expanded hover card renders larger and on top
                if is_hover:
                    draw_r = pygame.Rect(cx - (HOVERED_W - NORM_W) // 2,
                                         cy - (HOVERED_H - NORM_H) // 2,
                                         HOVERED_W, HOVERED_H)
                else:
                    draw_r = card_r

                alive = enemy.get("alive", True)
                if not alive:
                    bg, border = (12, 8, 12), DEAD_COLOR
                elif is_hover and is_targeting:
                    bg, border = (60, 20, 20), (255, 100, 100)
                elif is_hover:
                    bg, border = ENEMY_HOVER_BG, (180, 100, 80)
                else:
                    bg, border = ENEMY_BG, (80, 50, 55)

                _draw_panel(surface, draw_r, bg, border, radius=5)

                # Silhouette (top portion of card)
                sil_h = draw_r.h - 50
                sil_r = pygame.Rect(draw_r.x + 4, draw_r.y + 4,
                                     draw_r.w - 8, max(30, sil_h))
                tier = enemy.get("knowledge_tier", -1)
                tkey = enemy.get("template_key") or enemy.get("name", "")
                draw_enemy_silhouette(surface, sil_r, tkey,
                                       knowledge_tier=tier,
                                       hover=is_hover,
                                       dead=not alive)

                # Name (knowledge-tier based)
                name_y = draw_r.y + max(30, sil_h) + 5
                display_name = get_enemy_display_name(enemy)
                # Truncate display name for card width
                font_s = get_font(10)
                max_name_w = draw_r.w - 8
                while font_s.size(display_name)[0] > max_name_w and len(display_name) > 4:
                    display_name = display_name[:-4] + "..."
                    break
                name_col = DEAD_COLOR if not alive else (CREAM if not is_hover else GOLD)
                draw_text(surface, display_name, draw_r.x + 4, name_y, name_col, 10)

                # HP bar
                hp, mhp = enemy.get("hp", 0), enemy.get("max_hp", 1)
                bar_y = name_y + 14
                if alive:
                    _draw_resource_bar(surface, draw_r.x + 4, bar_y,
                                        draw_r.w - 8, 7, hp, mhp,
                                        (HP_BG, _hp_color(hp, mhp), (190,150,145)))
                    hp_text = f"{hp}/{mhp}"
                    draw_text(surface, hp_text, draw_r.x + 4, bar_y + 9,
                               _hp_color(hp, mhp), 9)
                    # Row badge top-right
                    rc2 = ROW_COLORS[enemy.get("row", FRONT)]
                    draw_text(surface, f"[{row_key[0].upper()}]",
                               draw_r.right - 22, draw_r.y + 3, rc2, 9)
                    # Status effects (hover only)
                    if is_hover:
                        se = enemy.get("status_effects", {})
                        if se:
                            sey = bar_y + 22
                            for sname in list(se.keys())[:3]:
                                draw_text(surface, sname[:8], draw_r.x + 4, sey, ORANGE, 9)
                                sey += 11
                else:
                    draw_text(surface, "DEAD", draw_r.x + 4, bar_y, DEAD_COLOR, 10)

        # Bottom border of enemy zone
        pygame.draw.line(surface, PANEL_BORDER,
                         (RIGHT_X, RIGHT_Y + ENEMY_H),
                         (SCREEN_W, RIGHT_Y + ENEMY_H))

    # ─────────────────────────────────────────────────────────
    #  COMBAT LOG
    # ─────────────────────────────────────────────────────────
    def _draw_log(self, surface):
        r = pygame.Rect(RIGHT_X, LOG_Y, RIGHT_W, LOG_H)
        pygame.draw.rect(surface, LOG_BG, r)
        pygame.draw.rect(surface, LOG_BORDER, r, 1)

        draw_text(surface, "Combat Log", RIGHT_X + 6, LOG_Y + 3, DARK_GREY, 10, bold=True)

        log = self.combat.combat_log
        font = get_font(11)
        line_h = 14
        visible = max(1, (LOG_H - 18) // line_h)
        total = len(log)
        start = max(0, total - visible - self.log_scroll)
        end   = max(0, total - self.log_scroll)
        shown = log[start:end]

        for i, msg in enumerate(shown):
            col = GOLD if ("Round" in msg or "VICTORY" in msg or "DEFEAT" in msg) else \
                  HEAL_COLOR if ("heal" in msg.lower() or "restore" in msg.lower()) else \
                  (255, 80, 80) if ("CRITICAL" in msg or "FATAL" in msg or "falls" in msg) else \
                  CREAM
            y = LOG_Y + 16 + i * line_h
            if y < LOG_Y + LOG_H - 4:
                surface.blit(font.render(msg[:90], True, col), (RIGHT_X + 6, y))

        # Scroll indicator
        if self.log_scroll > 0:
            draw_text(surface, f"↑ {self.log_scroll} more", SCREEN_W - 90, LOG_Y + 4,
                      DARK_GREY, 9)

    # ─────────────────────────────────────────────────────────
    #  ACTION BAR
    # ─────────────────────────────────────────────────────────
    def _draw_action_bar(self, surface, mx, my):
        pygame.draw.rect(surface, ACT_BG, (0, ACTION_Y, SCREEN_W, ACTION_H))
        pygame.draw.line(surface, PANEL_BORDER, (0, ACTION_Y), (SCREEN_W, ACTION_Y), 2)

        if not self.combat.is_player_turn() or self.combat.phase in ("victory", "defeat"):
            return

        actor = self.combat.get_current_combatant()
        if not actor:
            return

        # Actor name banner
        draw_text(surface, f"{actor['name']}'s Turn", 8, ACTION_Y + 4, GOLD, 13, bold=True)

        self.hover_action = -1
        for i, label in enumerate(_ACT_LABELS):
            bx = i * _ACT_W
            btn = pygame.Rect(bx + 2, ACTION_Y + 24, _ACT_W - 4, ACTION_H - 30)
            is_hover = btn.collidepoint(mx, my)
            is_open  = (self.popover == label.lower())

            # Grayed out if not applicable
            available = self._action_available(label, actor)

            if is_hover and available:
                self.hover_action = i

            bg     = ACT_ACTIVE if is_open else (ACT_HOVER if (is_hover and available) else ACT_BG)
            border = GOLD if is_open else (DIM_GOLD if (is_hover and available) else
                     (DARK_GREY if not available else PANEL_BORDER))
            col    = GOLD if is_open else (CREAM if available else DARK_GREY)

            _draw_panel(surface, btn, bg, border, radius=5)
            lw = get_font(16).size(label)[0]
            draw_text(surface, label, btn.x + (btn.w - lw) // 2, btn.y + 14, col, 16,
                      bold=(is_open or is_hover))

    def _action_available(self, label, actor):
        if label == "Spell":
            abilities = actor.get("abilities", [])
            return any(a.get("type") in ("spell", "magic", "heal", "buff", "aoe", "curse")
                       for a in abilities)
        if label == "Skill":
            abilities = actor.get("abilities", [])
            return any(a.get("type") not in ("spell", "magic", "heal", "buff", "aoe", "curse")
                       for a in abilities)
        if label == "Item":
            ref = actor.get("character_ref")
            if not ref: return False
            # Check for usable consumables or alt weapons
            inv = getattr(ref, "inventory", []) or []
            has_consumable = any(i.get("slot") == "consumable" or i.get("usable_in_combat")
                                  for i in inv)
            cur_weapon = (getattr(ref, "equipment", {}) or {}).get("weapon")
            has_alt_weapon = any(i.get("slot") == "weapon" and i != cur_weapon for i in inv)
            return has_consumable or has_alt_weapon
        return True

    # ─────────────────────────────────────────────────────────
    #  POPOVER
    # ─────────────────────────────────────────────────────────
    def _build_popover_items(self, label, actor):
        """Populate self._popover_items for the given action label."""
        items = []
        if label == "attack":
            items = [("Basic Attack", {"type": "attack_select"})]

        elif label in ("spell", "skill"):
            abilities = actor.get("abilities", [])
            spell_types = {"spell", "magic", "heal", "buff", "aoe", "curse"}
            for ab in abilities:
                ab_type = ab.get("type", "skill")
                is_spell = ab_type in spell_types
                if (label == "spell" and is_spell) or (label == "skill" and not is_spell):
                    mp   = ab.get("mp_cost", ab.get("cost", 0))
                    cost = f" [{mp} MP]" if mp else ""
                    items.append((f"{ab['name']}{cost}", {"type": "ability", "ability": ab}))

        elif label == "item":
            ref = actor.get("character_ref")
            if ref:
                self._combat_items = []
                inv = getattr(ref, "inventory", []) or []
                equip = getattr(ref, "equipment", {}) or {}
                cur_weapon = equip.get("weapon")
                for it in inv:
                    slot = it.get("slot", "")
                    if slot == "consumable" or it.get("usable_in_combat"):
                        self._combat_items.append(("consumable", it))
                        items.append((it.get("name", "Item"), {"type": "use_item", "item": it}))
                    elif slot == "weapon" and it != cur_weapon:
                        self._combat_items.append(("weapon", it))
                        items.append((f"Equip: {it.get('name','')}", {"type": "switch_weapon", "item": it}))

        elif label == "move":
            actor_row = actor.get("row", FRONT)
            self._move_directions = []
            dirs = []
            if actor_row == BACK:  dirs = ["forward"]
            elif actor_row == MID: dirs = ["forward", "back"]
            elif actor_row == FRONT: dirs = ["back"]
            self._move_directions = dirs
            items = [(f"Move {d.capitalize()}", {"type": "move", "direction": d}) for d in dirs]

        return items

    def _draw_popover(self, surface, mx, my):
        """Draw the action popover above the action bar."""
        label = self.popover
        if not label:
            return

        actor = self.combat.get_current_combatant()
        if not actor:
            return

        VISIBLE = 8
        ITEM_H  = 36
        PAD     = 10
        POP_W   = 400
        POP_H   = min(len(self._popover_items), VISIBLE) * ITEM_H + PAD * 2 + 24

        # Find which button column this popover belongs to
        idx = [l.lower() for l in _ACT_LABELS].index(label) if label in [l.lower() for l in _ACT_LABELS] else 0
        pop_cx = idx * _ACT_W + _ACT_W // 2
        pop_x  = max(4, min(pop_cx - POP_W // 2, SCREEN_W - POP_W - 4))
        pop_y  = ACTION_Y - POP_H - 6

        pop_r  = pygame.Rect(pop_x, pop_y, POP_W, POP_H)
        _draw_panel(surface, pop_r, POP_BG, POP_BORDER, radius=6)

        title_map = {"attack": "Choose Attack", "spell": "Spells",
                     "skill": "Skills", "item": "Items", "move": "Move"}
        draw_text(surface, title_map.get(label, label.title()),
                  pop_x + PAD, pop_y + PAD, GOLD, 13, bold=True)

        items = self._popover_items
        start = self.popover_scroll
        end   = start + VISIBLE

        self.hover_pop_item = -1
        for i, (lbl, data) in enumerate(items[start:end]):
            real_i = i + start
            ir = pygame.Rect(pop_x + PAD, pop_y + 24 + i * ITEM_H,
                             POP_W - PAD * 2, ITEM_H - 4)
            is_h = ir.collidepoint(mx, my)
            if is_h:
                self.hover_pop_item = real_i
            bg = POP_HOVER if is_h else POP_BG
            _draw_panel(surface, ir, bg, (100, 80, 150) if is_h else LOG_BORDER)

            # Item description color
            item_col = GOLD if is_h else CREAM
            if data.get("type") in ("use_item",):
                item_col = HEAL_COLOR if is_h else (100, 220, 140)
            draw_text(surface, lbl[:40], ir.x + 8, ir.y + 10, item_col, 13)

            # Number shortcut
            draw_text(surface, str(real_i + 1), ir.x - 14, ir.y + 10, DARK_GREY, 11)

        # Scroll indicators
        if start > 0:
            draw_text(surface, "▲", pop_x + POP_W - 18, pop_y + 24, GREY, 11)
        if end < len(items):
            draw_text(surface, "▼", pop_x + POP_W - 18, pop_y + POP_H - 18, GREY, 11)

        # ESC hint
        draw_text(surface, "ESC to cancel", pop_x + PAD, pop_y + POP_H - 14,
                  DARK_GREY, 9)

    # ─────────────────────────────────────────────────────────
    #  END / THINKING
    # ─────────────────────────────────────────────────────────
    def _draw_end_screen(self, surface, mx, my):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        phase = self.combat.phase
        title = "VICTORY!" if phase == "victory" else "DEFEAT"
        title_col = (100, 255, 140) if phase == "victory" else (255, 80, 80)
        tw = get_font(48).size(title)[0]
        draw_text(surface, title, SCREEN_W // 2 - tw // 2, SCREEN_H // 3, title_col, 48, bold=True)

        if phase == "victory":
            rw = getattr(self.combat, "rewards", {})
            xp  = rw.get("xp", 0)
            gld = rw.get("gold", 0)
            draw_text(surface, f"+{xp} XP   +{gld} Gold",
                      SCREEN_W // 2 - 80, SCREEN_H // 3 + 62, GOLD, 20)

        btn = pygame.Rect(SCREEN_W // 2 - 120, SCREEN_H * 2 // 3, 240, 48)
        hov = btn.collidepoint(mx, my)
        _draw_panel(surface, btn, (40, 60, 40) if (phase == "victory" and hov) else (60, 30, 30) if hov else (20, 18, 35))
        lbl = "Continue" if phase == "victory" else "Retreat"
        lw  = get_font(18).size(lbl)[0]
        draw_text(surface, lbl, btn.x + (btn.w - lw) // 2, btn.y + 13, GOLD if hov else CREAM, 18)

    def _draw_enemy_thinking(self, surface):
        draw_text(surface, "Enemy acting...", 8, ACTION_Y + 6, (140, 120, 160), 13)

    def _draw_flash(self, surface):
        self.flash_messages = [(m, c, t - 16) for m, c, t in self.flash_messages if t > 0]
        font = get_font(16)
        for i, (msg, col, timer) in enumerate(self.flash_messages[-5:]):
            alpha = min(255, int(timer / 200 * 255))
            ts = font.render(msg, True, col)
            ts.set_alpha(alpha)
            x = RIGHT_X + RIGHT_W // 2 - ts.get_width() // 2
            y = SCREEN_H // 2 - 60 + i * 28
            bg = pygame.Surface((ts.get_width() + 10, ts.get_height() + 4), pygame.SRCALPHA)
            bg.fill((0, 0, 0, min(160, alpha)))
            surface.blit(bg, (x - 5, y - 2))
            surface.blit(ts, (x, y))

    # ─────────────────────────────────────────────────────────
    #  INPUT — CLICK
    # ─────────────────────────────────────────────────────────
    def handle_click(self, mx, my):
        """Handle mouse click. Returns action dict or None."""
        # End screen button
        if self.combat.phase in ("victory", "defeat"):
            btn = pygame.Rect(SCREEN_W // 2 - 120, SCREEN_H * 2 // 3, 240, 48)
            if btn.collidepoint(mx, my):
                return {"type": "end_combat", "result": self.combat.phase}
            return None

        if not self.combat.is_player_turn():
            return None

        actor = self.combat.get_current_combatant()

        # ── Popover open — handle popover clicks ──
        if self.popover:
            label = self.popover
            idx   = [l.lower() for l in _ACT_LABELS].index(label) if label in [l.lower() for l in _ACT_LABELS] else 0
            POP_W, VISIBLE, ITEM_H, PAD = 400, 8, 36, 10
            POP_H = min(len(self._popover_items), VISIBLE) * ITEM_H + PAD * 2 + 24
            pop_cx = idx * _ACT_W + _ACT_W // 2
            pop_x  = max(4, min(pop_cx - POP_W // 2, SCREEN_W - POP_W - 4))
            pop_y  = ACTION_Y - POP_H - 6
            pop_r  = pygame.Rect(pop_x, pop_y, POP_W, POP_H)

            if not pop_r.collidepoint(mx, my):
                # Click outside popover — check if on action bar (switch popover) or close
                for i, lbl in enumerate(_ACT_LABELS):
                    bx = i * _ACT_W
                    btn = pygame.Rect(bx + 2, ACTION_Y + 24, _ACT_W - 4, ACTION_H - 30)
                    if btn.collidepoint(mx, my):
                        ll = lbl.lower()
                        if ll == label:
                            self.popover = None
                        elif ll in ("defend",):
                            self.popover = None
                            return {"type": "defend"}
                        elif ll == "flee":
                            self.popover = None
                            return {"type": "flee"}
                        elif self._action_available(lbl, actor):
                            self._open_popover(lbl.lower(), actor)
                        return None
                self.popover = None
                return None

            # Click inside popover — select item
            if self.hover_pop_item >= 0 and self.hover_pop_item < len(self._popover_items):
                _, data = self._popover_items[self.hover_pop_item]
                self.popover = None
                return self._resolve_popover_item(data, actor)
            return None

        # ── Targeting modes ──
        if self.action_mode == "target_attack":
            if self.hover_enemy and self.hover_enemy["alive"]:
                self.action_mode = "main"
                return {"type": "attack", "target": self.hover_enemy}

        elif self.action_mode == "target_ability":
            if self.hover_enemy and self.hover_enemy["alive"]:
                self.action_mode = "main"
                return {"type": "ability", "ability": self.selected_ability,
                        "target": self.hover_enemy}

        elif self.action_mode == "target_heal":
            if self.hover_player and self.hover_player.get("alive"):
                self.action_mode = "main"
                return {"type": "ability", "ability": self.selected_ability,
                        "target": self.hover_player}
            # Also allow targeting downed allies for revival
            if self.hover_player:
                ab = self.selected_ability
                if ab and "revive" in ab.get("name", "").lower():
                    self.action_mode = "main"
                    return {"type": "ability", "ability": ab, "target": self.hover_player}

        # Cancel targeting on ESC / clicking void
        if self.action_mode != "main":
            self.action_mode = "main"
            self.selected_ability = None
            return None

        # ── Action bar ──
        for i, label in enumerate(_ACT_LABELS):
            bx = i * _ACT_W
            btn = pygame.Rect(bx + 2, ACTION_Y + 24, _ACT_W - 4, ACTION_H - 30)
            if not btn.collidepoint(mx, my):
                continue
            ll = label.lower()
            if ll == "attack":
                self.action_mode = "target_attack"
                self.popover = None
            elif ll == "defend":
                return {"type": "defend"}
            elif ll == "flee":
                return {"type": "flee"}
            elif self._action_available(label, actor):
                self._open_popover(ll, actor)
            return None

        return None

    def _open_popover(self, label_lower, actor):
        self.popover = label_lower
        self.popover_scroll = 0
        self._popover_items = self._build_popover_items(label_lower, actor)

    def _resolve_popover_item(self, data, actor):
        """Turn a popover item data dict into a combat action or mode change."""
        t = data.get("type")
        if t == "attack_select":
            self.action_mode = "target_attack"
            return None
        if t == "ability":
            ab = data["ability"]
            ab_type = ab.get("type", "skill")
            target_field = ab.get("target", "single_enemy")
            ab_name = ab.get("name", "").lower()

            if ab_type in ("aoe", "aoe_heal") or "aoe" in target_field:
                return {"type": "ability", "ability": ab, "target": None}
            if target_field in ("self", "all_allies") or (ab_type == "buff" and "enemy" not in target_field):
                return {"type": "ability", "ability": ab, "target": actor}
            if ab_type in ("heal", "cure", "revive") or "heal" in ab_name or "revive" in ab_name:
                self.selected_ability = ab
                self.action_mode = "target_heal"
                return None
            # Default: target an enemy
            self.selected_ability = ab
            self.action_mode = "target_ability"
            return None

        if t == "use_item":
            return {"type": "use_consumable", "item": data["item"]}
        if t == "switch_weapon":
            return {"type": "switch_weapon", "item": data["item"]}
        if t == "move":
            return {"type": "move", "direction": data["direction"]}
        return None

    def handle_scroll(self, direction):
        """Scroll combat log or popover."""
        if self.popover and self._popover_items:
            VISIBLE = 8
            if direction > 0:
                self.popover_scroll = min(
                    max(0, len(self._popover_items) - VISIBLE),
                    self.popover_scroll + 1)
            else:
                self.popover_scroll = max(0, self.popover_scroll - 1)
        else:
            total = len(self.combat.combat_log)
            if direction > 0:
                self.log_scroll = min(max(0, total - 5), self.log_scroll + 1)
            else:
                self.log_scroll = max(0, self.log_scroll - 1)

    def handle_key(self, key):
        """Keyboard shortcuts: ESC closes popover/targeting, number keys select popover items."""
        if key == pygame.K_ESCAPE:
            if self.popover:
                self.popover = None
            elif self.action_mode != "main":
                self.action_mode = "main"
                self.selected_ability = None
            return None

        # Number keys 1-9 for popover item selection
        if self.popover and pygame.K_1 <= key <= pygame.K_9:
            idx = key - pygame.K_1 + self.popover_scroll
            if 0 <= idx < len(self._popover_items):
                _, data = self._popover_items[idx]
                self.popover = None
                actor = self.combat.get_current_combatant()
                return self._resolve_popover_item(data, actor)

        return None

    # ─────────────────────────────────────────────────────────
    #  FLASH MESSAGES
    # ─────────────────────────────────────────────────────────
    def add_flash(self, msg, color=WHITE):
        self.flash_messages.append((msg, color, 1800))
