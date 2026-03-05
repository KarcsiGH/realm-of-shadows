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
from ui.pixel_art import draw_character_silhouette, draw_enemy_silhouette, CLASS_COLORS
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

_ELEMENT_FLASH_COLORS = {
    "fire":      (255, 120,  40),
    "ice":       ( 80, 200, 255),
    "frost":     ( 80, 200, 255),
    "lightning": (240, 220,  60),
    "nature":    ( 80, 200,  80),
    "holy":      (255, 240, 180),
    "shadow":    (160,  80, 220),
    "poison":    (120, 200,  60),
    "heal":      (100, 255, 140),
    "crit":      (255, 220,  40),
}

def _ability_flash_color(ability, result):
    """Pick flash color based on ability element/type."""
    if not ability:
        return (255, 255, 255)
    elem = ability.get("element", "")
    if elem in _ELEMENT_FLASH_COLORS:
        return _ELEMENT_FLASH_COLORS[elem]
    ab_type = ability.get("type", "")
    if "heal" in ab_type or "heal" in ability.get("name","").lower():
        return _ELEMENT_FLASH_COLORS["heal"]
    if result.get("is_crit"):
        return _ELEMENT_FLASH_COLORS["crit"]
    return (220, 200, 255)
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

        # Stack popover (click stack card to pick individual target)
        self.stack_popover_key    = None   # template_key of open stack, or None
        self.stack_popover_rect   = None   # pygame.Rect of the open popover
        self.stack_popover_card_rect = None  # rect of the card that opened it
        self.hover_stack_enemy    = None   # enemy hovered inside stack popover

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
            draw_text(surface, name, r.x + 4, r.y + 4, GOLD if is_cur else CREAM, 13, bold=is_cur)
            x += slot_w

    # ─────────────────────────────────────────────────────────
    #  LEFT COLUMN — CHARACTER CARDS
    # ─────────────────────────────────────────────────────────
    def _draw_left_col(self, surface, mx, my):
        pygame.draw.rect(surface, (12, 10, 22), (LEFT_X, LEFT_Y, LEFT_W, LEFT_H))
        pygame.draw.line(surface, PANEL_BORDER, (LEFT_W, LEFT_Y), (LEFT_W, ACTION_Y))

        cur = self.combat.get_current_combatant()
        self.hover_player = None

        # ── Group players by row, display BACK→MID→FRONT (mirrors enemy side) ──
        row_order = [BACK, MID, FRONT]
        players_by_row = {r: [] for r in row_order}
        for p in self.combat.players:
            players_by_row.setdefault(p.get("row", FRONT), []).append(p)

        ROW_HDR_H = 16          # height of each row section header
        n_players = max(1, len(self.combat.players))
        non_empty_rows = [r for r in row_order if players_by_row[r]]
        n_hdrs = len(non_empty_rows)
        avail_h = LEFT_H - n_hdrs * ROW_HDR_H
        card_h  = min(avail_h // n_players, 130)

        cy = LEFT_Y
        for row_key in row_order:
            row_players = players_by_row[row_key]
            if not row_players:
                continue

            # ── Row section header ──
            rc = ROW_COLORS[row_key]
            hdr_r = pygame.Rect(LEFT_X, cy, LEFT_W, ROW_HDR_H)
            pygame.draw.rect(surface, (rc[0]//5, rc[1]//5, rc[2]//5), hdr_r)
            pygame.draw.line(surface, rc, (LEFT_X, cy), (LEFT_W, cy), 1)
            row_label = {BACK: "BACK ROW", MID: "MID ROW", FRONT: "FRONT ROW"}[row_key]
            draw_text(surface, row_label, LEFT_X + 6, cy + 2, rc, 9, bold=True)
            cy += ROW_HDR_H

            for p in row_players:
                r = pygame.Rect(LEFT_X + 3, cy + 2, LEFT_W - 6, card_h - 4)
                is_cur  = (p is cur)
                is_dead = not p.get("alive", True)
                is_target = (self.action_mode == "target_heal") and not is_dead

                bg     = PLAYER_ACTIVE_BG if is_cur else PLAYER_BG
                border = GOLD if is_cur else ((200, 200, 80) if (is_target and r.collidepoint(mx, my))
                                              else PANEL_BORDER)
                if r.collidepoint(mx, my):
                    self.hover_player = p
                    if not is_cur:
                        bg = (22, 18, 40)

                _draw_panel(surface, r, bg, border)

                # Silhouette (left side of card)
                sil_w = 44
                sil_h = card_h - 10
                sil_r = pygame.Rect(r.x + 3, r.y + 3, sil_w, sil_h)
                cls   = p.get("class_name", "Fighter")
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
                draw_text(surface, p["name"][:14], ix, iy, name_col, 13, bold=is_cur)
                draw_text(surface, f"Lv.{p.get('level', 1)} {cls[:10]}", ix, iy + 13, GREY, 11)

                if is_dead:
                    draw_text(surface, "FALLEN", ix, iy + 28, DEAD_COLOR, 12, bold=True)
                    cy += card_h
                    continue

                # Resource bars
                bar_y     = iy + 26
                bar_h_each = 6
                bar_gap    = 11

                hp  = p.get("hp", 0)
                mhp = p.get("max_hp", 1)
                _draw_resource_bar(surface, ix, bar_y, iw, bar_h_each, hp, mhp,
                                    RES_COLORS["HP"])
                draw_text(surface, f"HP {hp}/{mhp}", ix, bar_y + bar_h_each + 1,
                          (190, 150, 145), 9)
                bar_y += bar_gap + bar_h_each

                res   = p.get("resources", {})
                stats = p.get("stats", {})
                try:
                    from core.classes import get_all_resources
                    max_res = get_all_resources(cls, stats, p.get("level", 1))
                except Exception:
                    max_res = {}

                for rk in [k for k in res if k != "HP"][:2]:
                    cur_r = res.get(rk, 0)
                    max_r = max(1, max_res.get(rk, cur_r) or cur_r)
                    rc2   = RES_COLORS.get(rk, RES_COLORS["MP"])
                    _draw_resource_bar(surface, ix, bar_y, iw, bar_h_each, cur_r, max_r, rc2)
                    draw_text(surface, f"{rk} {cur_r}/{max_r}", ix, bar_y + bar_h_each + 1,
                              rc2[2], 9)
                    bar_y += bar_gap + bar_h_each
                    if bar_y > r.bottom - 10:
                        break

                # Status effect badges
                se = p.get("status_effects", [])
                if se:
                    BUFF_NAMES   = {"defense_up","iron_skin","magic_shield","bulwark","war_cry",
                                    "hawk_eye","ki_deflect","last_stand","evasion","smoke_screen",
                                    "courage_aura","empty_mind","WarCry","Defending","Blessed"}
                    DEBUFF_NAMES = {"Poisoned","Burning","Stunned","Slowed","Blinded","Confused",
                                    "Cursed","death_mark","Weakened"}
                    sx = ix
                    for effect in list(se)[:4]:
                        sname = effect["name"] if isinstance(effect, dict) else effect
                        dur   = effect.get("duration","") if isinstance(effect, dict) else ""
                        dur_s = f"{dur}" if dur else ""
                        if sname in BUFF_NAMES:      col = (100, 230, 130)
                        elif sname in DEBUFF_NAMES:  col = (230, 80, 60)
                        else:                        col = ORANGE
                        abbr  = sname[:3].upper()
                        bw    = 28
                        badge = pygame.Rect(sx, r.bottom - 15, bw, 12)
                        pygame.draw.rect(surface, (int(col[0]*0.25),int(col[1]*0.25),int(col[2]*0.25)), badge)
                        pygame.draw.rect(surface, col, badge, 1)
                        draw_text(surface, abbr, sx + 2, r.bottom - 13, col, 9)
                        if dur_s:
                            draw_text(surface, dur_s, sx + bw - 8, r.bottom - 13, col, 9)
                        sx += bw + 2

                cy += card_h

    # ─────────────────────────────────────────────────────────
    #  ENEMY ZONE
    # ─────────────────────────────────────────────────────────
    def _draw_enemy_zone(self, surface, mx, my):
        zone_r = pygame.Rect(RIGHT_X, RIGHT_Y, RIGHT_W, ENEMY_H)
        pygame.draw.rect(surface, (10, 8, 18), zone_r)

        is_targeting = self.action_mode in ("target_attack", "target_ability")
        self.hover_enemy = None
        self.hover_stack_enemy = None

        rows = [BACK, MID, FRONT]
        enemies_by_row = {r: [] for r in rows}
        for e in self.combat.enemies:
            enemies_by_row.setdefault(e["row"], []).append(e)

        # Track all card rects for this frame (used by click handler)
        self._card_rects = []        # [(card_rect, group_key, enemies_in_group)]
        self._stack_popover_draw = None  # set below if popover is open

        for ri, row_key in enumerate(rows):
            ry = RIGHT_Y + ri * ROW_H

            # Row label
            row_label = row_key[0].upper() + row_key[1:]
            rc = ROW_COLORS[row_key]
            pygame.draw.rect(surface, (rc[0]//5, rc[1]//5, rc[2]//5),
                             (RIGHT_X, ry, ROW_LABEL_W, ROW_H))
            draw_text(surface, row_label, RIGHT_X + 4, ry + ROW_H//2 - 7, rc, 13, bold=True)
            pygame.draw.line(surface, PANEL_BORDER, (RIGHT_X, ry), (SCREEN_W, ry))

            row_enemies = enemies_by_row.get(row_key, [])
            if not row_enemies:
                draw_text(surface, "—", ROW_AREA_X + ROW_AREA_W // 2 - 4,
                          ry + ROW_H // 2 - 7, DARK_GREY, 12)
                continue

            # ── Group enemies by template_key (stacking same-type) ──
            groups = {}   # template_key -> list of enemies
            group_order = []
            for e in row_enemies:
                key = e.get("template_key") or e.get("name", "Unknown")
                if key not in groups:
                    groups[key] = []
                    group_order.append(key)
                groups[key].append(e)

            num_groups = len(group_order)
            GAP = 6

            # Dynamic card width — fit all groups in available space
            MAX_CARD_W = 200
            card_w = min(MAX_CARD_W, (ROW_AREA_W - (num_groups - 1) * GAP) // num_groups)
            card_w = max(100, card_w)   # never go below readable minimum
            card_h = ROW_H - 14

            total_w = num_groups * card_w + (num_groups - 1) * GAP
            start_x = ROW_AREA_X + (ROW_AREA_W - total_w) // 2

            for gi, group_key in enumerate(group_order):
                group_enemies = groups[group_key]
                alive_enemies = [e for e in group_enemies if e.get("alive", True)]
                is_stack = len(group_enemies) > 1

                cx = start_x + gi * (card_w + GAP)
                cy = ry + 7
                card_r = pygame.Rect(cx, cy, card_w, card_h)
                self._card_rects.append((card_r, group_key, group_enemies))

                # Hover detection — entire card
                is_hover = card_r.collidepoint(mx, my)
                if is_hover and alive_enemies and not is_stack:
                    # Single enemy — hover sets target directly
                    self.hover_enemy = alive_enemies[0]
                elif is_hover and alive_enemies and is_stack:
                    # Stack — hover highlights card but doesn't set single target
                    pass

                # Pick representative enemy for display (topmost alive, or first dead)
                rep = alive_enemies[0] if alive_enemies else group_enemies[0]
                alive = bool(alive_enemies)

                # Card colours
                stack_open = (self.stack_popover_key == group_key)
                if not alive:
                    bg, border = (12, 8, 12), DEAD_COLOR
                elif stack_open:
                    bg, border = (50, 30, 50), (200, 140, 220)
                elif is_hover and is_targeting and alive:
                    bg, border = (60, 20, 20), (255, 100, 100)
                elif is_hover and alive:
                    bg, border = ENEMY_HOVER_BG, (180, 100, 80)
                else:
                    bg, border = ENEMY_BG, (80, 50, 55)

                _draw_panel(surface, card_r, bg, border, radius=5)

                # Silhouette — constrain to native 48:80 aspect ratio, centred
                sil_h = card_h - 50
                sil_w = max(20, int(sil_h * 48 / 80))   # 48:80 = 0.6
                sil_w = min(sil_w, card_w - 8)           # never wider than card
                sil_h = int(sil_w * 80 / 48)             # recalc height from constrained width
                sil_x = cx + (card_w - sil_w) // 2       # horizontally centred
                sil_r = pygame.Rect(sil_x, cy + 4, sil_w, sil_h)
                tier = rep.get("knowledge_tier", -1)
                tkey = rep.get("template_key") or rep.get("name", "")
                draw_enemy_silhouette(surface, sil_r, tkey,
                                      knowledge_tier=tier,
                                      hover=is_hover,
                                      dead=not alive)

                # Stack ×N badge (top-left corner)
                if is_stack:
                    alive_count = len(alive_enemies)
                    badge_label = f"×{len(group_enemies)}" if alive_count == len(group_enemies) \
                                  else f"×{alive_count}/{len(group_enemies)}"
                    badge_col = (220, 160, 80) if alive_count > 0 else DEAD_COLOR
                    pygame.draw.rect(surface, (30, 20, 10), (cx + 2, cy + 2, 28, 14), border_radius=3)
                    pygame.draw.rect(surface, badge_col, (cx + 2, cy + 2, 28, 14), 1, border_radius=3)
                    draw_text(surface, badge_label, cx + 4, cy + 3, badge_col, 9, bold=True)

                # Name
                name_y = cy + max(30, sil_h) + 5
                display_name = get_enemy_display_name(rep)
                font_s = get_font(10)
                max_name_w = card_w - 8
                while font_s.size(display_name)[0] > max_name_w and len(display_name) > 6:
                    display_name = display_name[:-4] + "…"
                    break
                name_col = DEAD_COLOR if not alive else (CREAM if not is_hover else GOLD)
                draw_text(surface, display_name, cx + 4, name_y, name_col, 13)

                # HP bar — for stacks show total HP of all alive enemies
                bar_y = name_y + 14
                if alive:
                    if is_stack:
                        total_hp  = sum(e.get("hp", 0) for e in alive_enemies)
                        total_mhp = sum(e.get("max_hp", 1) for e in alive_enemies)
                        _draw_resource_bar(surface, cx + 4, bar_y,
                                           card_w - 8, 7, total_hp, total_mhp,
                                           (HP_BG, _hp_color(total_hp, total_mhp), (190,150,145)))
                        draw_text(surface, f"{total_hp} HP total",
                                  cx + 4, bar_y + 9, _hp_color(total_hp, total_mhp), 9)
                    else:
                        hp, mhp = rep.get("hp", 0), rep.get("max_hp", 1)
                        _draw_resource_bar(surface, cx + 4, bar_y,
                                           card_w - 8, 7, hp, mhp,
                                           (HP_BG, _hp_color(hp, mhp), (190,150,145)))
                        draw_text(surface, f"{hp}/{mhp}",
                                  cx + 4, bar_y + 9, _hp_color(hp, mhp), 9)
                        # Row badge
                        rc2 = ROW_COLORS[rep.get("row", FRONT)]
                        draw_text(surface, f"[{row_key[0].upper()}]",
                                  card_r.right - 22, cy + 3, rc2, 9)
                        # Status effects on hover (single cards only)
                        if is_hover:
                            se = rep.get("status_effects", [])
                            if se:
                                sey = bar_y + 22
                                DEBUFF_C = (230,80,60); BUFF_C = (100,230,130)
                                DEBUFF_N = {"Poisoned","Burning","Stunned","Slowed",
                                            "Blinded","Weakened","Cursed"}
                                sex = cx + 4
                                for effect in list(se)[:4]:
                                    sname = effect["name"] if isinstance(effect,dict) else effect
                                    col = DEBUFF_C if sname in DEBUFF_N else BUFF_C
                                    bw = 28
                                    badge = pygame.Rect(sex, sey, bw, 12)
                                    pygame.draw.rect(surface,
                                        (int(col[0]*.2),int(col[1]*.2),int(col[2]*.2)), badge)
                                    pygame.draw.rect(surface, col, badge, 1)
                                    draw_text(surface, sname[:3].upper(), sex+2, sey+1, col, 9)
                                    sex += bw + 2
                                    if sex + bw > card_r.right:
                                        sex = cx + 4; sey += 14

                    # Stack hint text (when in targeting mode)
                    if is_stack and alive and is_targeting:
                        hint = "▲ click to pick"
                        draw_text(surface, hint, cx + 4, cy + card_h - 14,
                                  (160, 120, 200), 9)
                else:
                    draw_text(surface, "DEAD", cx + 4, bar_y, DEAD_COLOR, 12)

        # ── Draw stack popover on top of everything ──
        if self.stack_popover_key:
            self._draw_stack_popover(surface, mx, my)

        # Bottom border
        pygame.draw.line(surface, PANEL_BORDER,
                         (RIGHT_X, RIGHT_Y + ENEMY_H),
                         (SCREEN_W, RIGHT_Y + ENEMY_H))

    def _draw_stack_popover(self, surface, mx, my):
        """Draw the mini popover listing all enemies in an open stack."""
        key = self.stack_popover_key
        # Find the card rect that owns this stack
        card_r = None
        enemies_in_stack = []
        for cr, gk, ge in self._card_rects:
            if gk == key:
                card_r = cr
                enemies_in_stack = ge
                break
        if card_r is None:
            self.stack_popover_key = None
            return

        alive = [e for e in enemies_in_stack if e.get("alive", True)]
        if not alive:
            self.stack_popover_key = None
            return

        is_targeting = self.action_mode in ("target_attack", "target_ability")

        ITEM_H = 36
        PAD = 8
        POP_W = max(180, card_r.width + 20)
        POP_H = len(alive) * ITEM_H + PAD * 2 + 18

        # Position above the card, clamped to screen
        px = max(RIGHT_X + 2, min(card_r.centerx - POP_W // 2, SCREEN_W - POP_W - 2))
        py = max(RIGHT_Y + 2, card_r.top - POP_H - 6)
        pop_r = pygame.Rect(px, py, POP_W, POP_H)
        self.stack_popover_rect = pop_r

        # Background
        bg_surf = pygame.Surface((POP_W, POP_H), pygame.SRCALPHA)
        bg_surf.fill((20, 12, 32, 230))
        surface.blit(bg_surf, (px, py))
        pygame.draw.rect(surface, (180, 140, 220), pop_r, 1, border_radius=5)

        # Header
        draw_text(surface, "Select Target", px + PAD, py + 4, (180, 140, 220), 13, bold=True)
        pygame.draw.line(surface, (80, 60, 100), (px, py + 18), (px + POP_W, py + 18))

        # Enemy rows
        self.hover_stack_enemy = None
        for i, enemy in enumerate(alive):
            iy = py + 20 + i * ITEM_H
            item_r = pygame.Rect(px + 4, iy, POP_W - 8, ITEM_H - 4)
            is_hover = item_r.collidepoint(mx, my)
            if is_hover:
                self.hover_stack_enemy = enemy
                if is_targeting:
                    pygame.draw.rect(surface, (80, 30, 30), item_r, border_radius=3)
                    pygame.draw.rect(surface, (255, 100, 100), item_r, 1, border_radius=3)
                else:
                    pygame.draw.rect(surface, (50, 35, 55), item_r, border_radius=3)
                    pygame.draw.rect(surface, (180, 140, 220), item_r, 1, border_radius=3)

            # Enemy name with number
            name = enemy.get("name", "Enemy")
            hp, mhp = enemy.get("hp", 0), enemy.get("max_hp", 1)
            draw_text(surface, f"{i+1}. {name}", px + PAD + 2, iy + 3,
                      (255, 100, 100) if is_hover and is_targeting else CREAM, 11)
            # HP bar
            _draw_resource_bar(surface, px + PAD + 2, iy + 18,
                               POP_W - PAD * 2 - 4, 6, hp, mhp,
                               (HP_BG, _hp_color(hp, mhp), (190,150,145)))
            draw_text(surface, f"{hp}/{mhp}", px + PAD + POP_W - PAD*2 - 34,
                      iy + 19, _hp_color(hp, mhp), 9)

    # ─────────────────────────────────────────────────────────
    #  COMBAT LOG
    # ─────────────────────────────────────────────────────────
    def _draw_log(self, surface):
        r = pygame.Rect(RIGHT_X, LOG_Y, RIGHT_W, LOG_H)
        pygame.draw.rect(surface, LOG_BG, r)
        pygame.draw.rect(surface, LOG_BORDER, r, 1)

        draw_text(surface, "Combat Log", RIGHT_X + 6, LOG_Y + 3, GREY, 12, bold=True)

        log = self.combat.combat_log
        font = get_font(13)
        line_h = 17
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
                      GREY, 13)

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
        draw_text(surface, f"{actor['name']}'s Turn", 8, ACTION_Y + 4, GOLD, 15, bold=True)

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
            return any(
                "MP" in a.get("resource","") or "INT" in a.get("resource","") or "PIE" in a.get("resource","")
                or (not a.get("resource","") and a.get("type","") in ("spell","magic","heal","cure","aoe_heal"))
                for a in abilities)
        if label == "Skill":
            abilities = actor.get("abilities", [])
            return any(
                "SP" in a.get("resource","") or "Ki" in a.get("resource","") or "EP" in a.get("resource","")
                or (not a.get("resource","") and a.get("type","skill") not in ("spell","magic","heal","cure","aoe_heal"))
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
            for ab in abilities:
                resource = ab.get("resource", "")
                ab_type  = ab.get("type", "skill")
                # Primary signal: resource determines spell vs skill category
                if "MP" in resource or "INT" in resource or "PIE" in resource:
                    is_spell = True
                elif "SP" in resource or "Ki" in resource or "EP" in resource:
                    is_spell = False
                else:
                    # Fallback: use type field
                    spell_types = {"spell", "magic", "heal", "cure", "aoe_heal"}
                    is_spell = ab_type in spell_types
                if (label == "spell" and is_spell) or (label == "skill" and not is_spell):
                    res_cost = ab.get("cost", ab.get("mp_cost", 0))
                    res_name = "MP" if is_spell else (resource.split("-")[-1] if resource else "SP")
                    cost = f" [{res_cost} {res_name}]" if res_cost else ""
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
            draw_text(surface, str(real_i + 1), ir.x - 14, ir.y + 10, GREY, 13)

        # Scroll indicators
        if start > 0:
            draw_text(surface, "▲", pop_x + POP_W - 18, pop_y + 24, GREY, 13)
        if end < len(items):
            draw_text(surface, "▼", pop_x + POP_W - 18, pop_y + POP_H - 18, GREY, 13)

        # ESC hint
        draw_text(surface, "ESC to cancel", pop_x + PAD, pop_y + POP_H - 14,
                  GREY, 13)

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
            xp  = rw.get("total_xp", rw.get("xp", 0))
            gld = rw.get("total_gold", rw.get("gold", 0))
            draw_text(surface, f"+{xp} XP   +{gld} Gold",
                      SCREEN_W // 2 - 80, SCREEN_H // 3 + 62, GOLD, 20)

        btn = pygame.Rect(SCREEN_W // 2 - 120, SCREEN_H * 2 // 3, 240, 48)
        hov = btn.collidepoint(mx, my)
        _draw_panel(surface, btn, (40, 60, 40) if (phase == "victory" and hov) else (60, 30, 30) if hov else (20, 18, 35))
        lbl = "Continue" if phase == "victory" else "Retreat"
        lw  = get_font(18).size(lbl)[0]
        draw_text(surface, lbl, btn.x + (btn.w - lw) // 2, btn.y + 13, GOLD if hov else CREAM, 18)

    def _draw_enemy_thinking(self, surface):
        draw_text(surface, "Enemy acting...", 8, ACTION_Y + 6, (140, 120, 160), 15)

    def _draw_flash(self, surface):
        self.flash_messages = [(m, c, t - 16) for m, c, t in self.flash_messages if t > 0]
        font = get_font(16)
        for i, (msg, col, timer) in enumerate(self.flash_messages[-5:]):
            alpha = max(0, min(255, int(timer / 200 * 255)))
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

        # ── Stack popover open — check it first ──
        if self.stack_popover_key is not None:
            pop_r = self.stack_popover_rect
            if pop_r and pop_r.collidepoint(mx, my):
                # Click inside stack popover — pick enemy
                if self.hover_stack_enemy and self.hover_stack_enemy.get("alive"):
                    target = self.hover_stack_enemy
                    self.stack_popover_key = None
                    is_targeting = self.action_mode in ("target_attack", "target_ability")
                    if is_targeting:
                        mode = self.action_mode
                        self.action_mode = "main"
                        if mode == "target_attack":
                            return {"type": "attack", "target": target}
                        else:
                            return {"type": "ability", "ability": self.selected_ability,
                                    "target": target}
            else:
                # Click outside stack popover — close it
                self.stack_popover_key = None
            return None

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
            # Click on a stack card → open stack popover
            for card_r, group_key, group_enemies in getattr(self, "_card_rects", []):
                if card_r.collidepoint(mx, my) and len(group_enemies) > 1:
                    alive_in_group = [e for e in group_enemies if e.get("alive", True)]
                    if alive_in_group:
                        self.stack_popover_key = group_key
                        return None

        elif self.action_mode == "target_ability":
            if self.hover_enemy and self.hover_enemy["alive"]:
                self.action_mode = "main"
                return {"type": "ability", "ability": self.selected_ability,
                        "target": self.hover_enemy}
            # Click on a stack card → open stack popover
            for card_r, group_key, group_enemies in getattr(self, "_card_rects", []):
                if card_r.collidepoint(mx, my) and len(group_enemies) > 1:
                    alive_in_group = [e for e in group_enemies if e.get("alive", True)]
                    if alive_in_group:
                        self.stack_popover_key = group_key
                        return None

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
            ab_name = ab.get("name", "").lower()
            target_field = ab.get("target", "")

            # Buff abilities without explicit enemy target → always self/ally
            if ab_type == "buff" and target_field not in ("single_enemy", "all_enemies"):
                tgt_spec = ab.get("targets", ab.get("target", "self"))
                if tgt_spec == "all_allies":
                    return {"type": "ability", "ability": ab, "target": actor}  # engine handles aoe
                return {"type": "ability", "ability": ab, "target": actor}

            if ab_type in ("aoe", "aoe_heal") or "aoe" in target_field:
                return {"type": "ability", "ability": ab, "target": None}
            if target_field in ("self", "all_allies"):
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
            if self.stack_popover_key is not None:
                self.stack_popover_key = None
            elif self.popover:
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
