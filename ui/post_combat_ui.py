"""
Realm of Shadows — Post-Combat UI
Multi-phase screen after victory:
  Phase 1: XP & Level Up   — show awards, animate level ups
  Phase 2: Identification   — pick identifiers and items, roll results
  Phase 3: Loot Assignment  — assign items to party members
  Phase 4: Summary          — final summary + continue button
"""
import pygame
from ui.renderer import *
from core.identification import (
    get_identify_options, attempt_identify,
    get_item_display_name, get_item_display_desc,
    can_arcane_lore, can_appraisal,
    ARCANE_LORE_CLASSES, APPRAISAL_CLASSES,
)
from core.classes import CLASSES, STAT_NAMES, STAT_FULL_NAMES

# ═══════════════════════════════════════════════════════════════
#  COLORS (post-combat specific)
# ═══════════════════════════════════════════════════════════════

XP_BAR_BG    = (30, 25, 20)
XP_BAR_FILL  = (80, 180, 255)
XP_BAR_FULL  = (255, 215, 0)
LEVEL_UP_COL = (255, 215, 0)
GAIN_COL     = (80, 255, 120)
SECTION_BG   = (15, 12, 28)
ITEM_BG      = (25, 20, 45)
ITEM_HOVER   = (45, 38, 75)
ITEM_SELECTED= (55, 45, 90)
SUCCESS_COL  = (80, 255, 120)
FAIL_COL     = (255, 80, 80)
ASSIGNED_COL = (60, 140, 60)
UNASSIGNED   = (180, 160, 40)

RARITY_COLORS = {
    "common":    CREAM,
    "uncommon":  (80, 220, 80),
    "rare":      (80, 140, 255),
    "epic":      (180, 80, 255),
    "legendary": (255, 180, 40),
}


# ═══════════════════════════════════════════════════════════════
#  POST-COMBAT UI CLASS
# ═══════════════════════════════════════════════════════════════

class PostCombatUI:
    """
    Manages the full post-combat flow.
    Receives: party (list of Character), combat rewards dict, player combatants list.
    """

    # Sub-phases
    PHASE_XP     = "xp"
    PHASE_ID     = "identify"
    PHASE_LOOT   = "loot"
    PHASE_DONE   = "done"

    def __init__(self, party, rewards, player_combatants):
        self.party = party                    # list of Character objects
        self.rewards = rewards                # from CombatState._calc_rewards
        self.combatants = player_combatants   # combat-state player dicts (have resources)
        self.phase = self.PHASE_XP
        self.finished = False

        # ── XP Phase state ──
        self.xp_applied = False
        self.xp_results = []        # [(char, xp_awarded, level_ups)]
        self.xp_anim_timer = 0
        self.xp_anim_done = False

        # ── Identification Phase state ──
        self.loot_items = list(rewards.get("loot_drops", []))
        self.id_selected_char = -1   # index into party
        self.id_selected_item = -1   # index into loot_items
        self.id_selected_action = -1 # index into available actions
        self.id_log = []             # [(message, color)]
        self.id_scroll = 0

        # ── Loot Phase state ──
        self.loot_selected_item = -1
        self.loot_hover_char = -1
        self.loot_assignments = {}   # item_index → char_index
        self.loot_scroll = 0

        # ── General ──
        self.hover_btn = -1
        self.timer = 0

    # ─────────────────────────────────────────────────────────
    #  APPLY XP (called once when entering XP phase)
    # ─────────────────────────────────────────────────────────

    def _apply_xp_and_gold(self):
        """Apply XP and gold to actual Character objects."""
        if self.xp_applied:
            return
        self.xp_applied = True

        xp_awards = self.rewards.get("xp_awards", {})
        gold_each = self.rewards.get("gold_each", 0)

        for char in self.party:
            # Find matching xp award by name
            award = None
            for uid, info in xp_awards.items():
                if info["name"] == char.name:
                    award = info
                    break

            if award:
                xp_amount = award["xp"]
                ready = char.add_xp(xp_amount)
                char.add_gold(gold_each)
                self.xp_results.append((char, xp_amount, ready))
            else:
                char.add_gold(gold_each)
                self.xp_results.append((char, 0, []))

    # ─────────────────────────────────────────────────────────
    #  MAIN DRAW
    # ─────────────────────────────────────────────────────────

    def draw(self, surface, mx, my, dt):
        self.timer += dt
        surface.fill(BG_COLOR)

        # Header bar
        pygame.draw.rect(surface, SECTION_BG, (0, 0, SCREEN_W, 50))
        draw_text(surface, "VICTORY", 20, 12, GOLD, 24, bold=True)

        # Inventory button
        inv_btn = pygame.Rect(SCREEN_W - 160, 8, 140, 36)
        inv_hover = inv_btn.collidepoint(mx, my)
        draw_button(surface, inv_btn, "Inventory", hover=inv_hover, size=13)

        # Gold display
        gold_total = self.rewards.get("total_gold", 0)
        draw_text(surface, f"Gold earned: {gold_total}", SCREEN_W - 350, 18, DIM_GOLD, 16)

        # Phase indicator
        phases = [("XP", self.PHASE_XP), ("Identify", self.PHASE_ID),
                  ("Loot", self.PHASE_LOOT), ("Done", self.PHASE_DONE)]
        current_idx = next((i for i, (_, pk) in enumerate(phases) if pk == self.phase), 0)
        px = SCREEN_W // 2 - 150
        for i, (label, phase_key) in enumerate(phases):
            is_current = (self.phase == phase_key)
            is_past = i < current_idx
            col = GOLD if is_current else GREEN if is_past else DARK_GREY
            draw_text(surface, label, px + i * 90, 18, col, 15, bold=is_current)
            if i < len(phases) - 1:
                draw_text(surface, "→", px + i * 90 + 65, 18, DARK_GREY, 15)

        # Draw current phase
        if self.phase == self.PHASE_XP:
            self._apply_xp_and_gold()
            self._draw_xp_phase(surface, mx, my, dt)
        elif self.phase == self.PHASE_ID:
            self._draw_identify_phase(surface, mx, my)
        elif self.phase == self.PHASE_LOOT:
            self._draw_loot_phase(surface, mx, my)
        elif self.phase == self.PHASE_DONE:
            self._draw_done_phase(surface, mx, my)

    # ─────────────────────────────────────────────────────────
    #  PHASE 1: XP & LEVEL UP
    # ─────────────────────────────────────────────────────────

    def _draw_xp_phase(self, surface, mx, my, dt):
        self.xp_anim_timer += dt

        draw_text(surface, "Experience Gained", 40, 65, CREAM, 20, bold=True)

        y = 100
        card_h = 120
        for i, (char, xp_amt, ready_to_level) in enumerate(self.xp_results):
            cls = CLASSES[char.class_name]
            rect = pygame.Rect(40, y, SCREEN_W - 80, card_h)
            draw_panel(surface, rect, border_color=cls["color"])

            # Name + class
            draw_text(surface, char.name, rect.x + 12, rect.y + 8,
                      cls["color"], 18, bold=True)
            draw_text(surface, f"Level {char.level}  {char.class_name}",
                      rect.x + 12, rect.y + 30, GREY, 14)

            # XP award
            draw_text(surface, f"+{xp_amt} XP", rect.x + 300, rect.y + 8,
                      XP_BAR_FILL, 16, bold=True)

            # XP bar
            xp_cur, xp_need = char.xp_progress()
            bar_x = rect.x + 300
            bar_y = rect.y + 32
            bar_w = 350
            bar_h = 16
            pygame.draw.rect(surface, XP_BAR_BG, (bar_x, bar_y, bar_w, bar_h))
            if xp_need > 0:
                fill = min(bar_w, int((xp_cur / xp_need) * bar_w))
                pygame.draw.rect(surface, XP_BAR_FILL, (bar_x, bar_y, fill, bar_h))
            pygame.draw.rect(surface, PANEL_BORDER, (bar_x, bar_y, bar_w, bar_h), 1)
            draw_text(surface, f"{xp_cur}/{xp_need}", bar_x + bar_w + 10, bar_y,
                      GREY, 13)

            # Ready to level up notice
            if ready_to_level:
                draw_text(surface, "★ Ready to Level Up! Visit the Inn to train. ★",
                          rect.x + 12, rect.y + 55, LEVEL_UP_COL, 16, bold=True)
            else:
                # Show gold
                draw_text(surface, f"+{self.rewards.get('gold_each', 0)} gold",
                          rect.x + 12, rect.y + 55, DIM_GOLD, 14)

                # Find xp_award info to show rounds data
                xp_awards = self.rewards.get("xp_awards", {})
                for uid, info in xp_awards.items():
                    if info["name"] == char.name:
                        status = " (KO)" if not info["alive"] else ""
                        pct = f"{info['share_pct']*100:.0f}%"
                        rounds_str = f"{info['rounds_alive']}/{info['total_rounds']} rounds"
                        draw_text(surface, f"Survived {rounds_str} ({pct}){status}",
                                  rect.x + 12, rect.y + 75, DARK_GREY, 12)
                        break

            y += card_h + 8

        # Continue button
        btn = pygame.Rect(SCREEN_W // 2 - 140, SCREEN_H - 65, 280, 45)
        has_loot = len(self.loot_items) > 0
        label = "Continue to Identification →" if has_loot else "Continue →"
        hover = btn.collidepoint(mx, my)
        self.hover_btn = 0 if hover else -1
        draw_button(surface, btn, label, hover=hover, size=16)

    # ─────────────────────────────────────────────────────────
    #  PHASE 2: IDENTIFICATION
    # ─────────────────────────────────────────────────────────

    def _draw_identify_phase(self, surface, mx, my):
        draw_text(surface, "Item Identification", 40, 65, CREAM, 20, bold=True)
        draw_text(surface, "Select a party member, then an item to identify.",
                  40, 90, DARK_GREY, 14)

        # ── Left panel: Party members with ID capabilities ──
        panel_l = pygame.Rect(20, 115, 380, 520)
        draw_panel(surface, panel_l, bg_color=SECTION_BG)
        draw_text(surface, "Identifiers", panel_l.x + 10, panel_l.y + 8,
                  GOLD, 16, bold=True)

        cy = panel_l.y + 35
        for i, char in enumerate(self.party):
            # Find matching combatant for current resources
            comb = self._find_combatant(char)
            cls = CLASSES[char.class_name]

            can_id = (char.class_name in ARCANE_LORE_CLASSES or
                      char.class_name in APPRAISAL_CLASSES)

            card_rect = pygame.Rect(panel_l.x + 8, cy, panel_l.width - 16, 72)
            is_hover = card_rect.collidepoint(mx, my)
            is_selected = (i == self.id_selected_char)

            if not can_id:
                bg = (18, 15, 25)
                border = (40, 35, 55)
            elif is_selected:
                bg = ITEM_SELECTED
                border = cls["color"]
            elif is_hover:
                bg = ITEM_HOVER
                border = HIGHLIGHT
            else:
                bg = ITEM_BG
                border = PANEL_BORDER

            pygame.draw.rect(surface, bg, card_rect, border_radius=3)
            pygame.draw.rect(surface, border, card_rect, 2, border_radius=3)

            name_col = cls["color"] if can_id else DARK_GREY
            draw_text(surface, char.name, card_rect.x + 10, card_rect.y + 6,
                      name_col, 15, bold=True)
            draw_text(surface, char.class_name, card_rect.x + 10, card_rect.y + 24,
                      GREY if can_id else DARK_GREY, 12)

            if can_id and comb:
                # Show available ID actions and resources
                options = get_identify_options(comb)
                ox = card_rect.x + 10
                oy = card_rect.y + 42
                for opt in options:
                    afford_col = GREEN if opt["can_afford"] else FAIL_COL
                    draw_text(surface, f"{opt['name']}", ox, oy, afford_col, 12)
                    ox += 120
            elif not can_id:
                draw_text(surface, "Cannot identify items", card_rect.x + 10,
                          card_rect.y + 42, DARK_GREY, 12)

            cy += 80

        # ── Right panel: Loot items ──
        panel_r = pygame.Rect(420, 115, SCREEN_W - 440, 340)
        draw_panel(surface, panel_r, bg_color=SECTION_BG)
        draw_text(surface, "Items to Identify", panel_r.x + 10, panel_r.y + 8,
                  GOLD, 16, bold=True)

        if not self.loot_items:
            draw_text(surface, "No items dropped.", panel_r.x + 20, panel_r.y + 40,
                      DARK_GREY, 15)
        else:
            iy = panel_r.y + 35
            for idx, item in enumerate(self.loot_items):
                item_rect = pygame.Rect(panel_r.x + 8, iy,
                                        panel_r.width - 16, 60)
                is_hover = item_rect.collidepoint(mx, my)
                is_sel = (idx == self.id_selected_item)

                if item.get("identified"):
                    bg = (20, 30, 20)
                    border = ASSIGNED_COL
                elif is_sel:
                    bg = ITEM_SELECTED
                    border = GOLD
                elif is_hover:
                    bg = ITEM_HOVER
                    border = HIGHLIGHT
                else:
                    bg = ITEM_BG
                    border = PANEL_BORDER

                pygame.draw.rect(surface, bg, item_rect, border_radius=3)
                pygame.draw.rect(surface, border, item_rect, 2, border_radius=3)

                display_name = get_item_display_name(item)
                rarity = item.get("rarity", "common")
                name_col = RARITY_COLORS.get(rarity, CREAM) if item.get("identified") else GREY
                draw_text(surface, display_name, item_rect.x + 10, item_rect.y + 6,
                          name_col, 15, bold=True)

                desc = get_item_display_desc(item)
                if len(desc) > 80:
                    desc = desc[:77] + "..."
                draw_text(surface, desc, item_rect.x + 10, item_rect.y + 26,
                          GREY, 12, max_width=item_rect.width - 20)

                # Status badges
                badge_x = item_rect.x + item_rect.width - 10
                if item.get("identified"):
                    lbl = "IDENTIFIED"
                    tw = get_font(11).size(lbl)[0]
                    draw_text(surface, lbl, badge_x - tw, item_rect.y + 6,
                              SUCCESS_COL, 11, bold=True)
                else:
                    if item.get("magic_identified"):
                        lbl = "Magic ✓"
                        tw = get_font(11).size(lbl)[0]
                        draw_text(surface, lbl, badge_x - tw, item_rect.y + 6,
                                  (80, 140, 255), 11)
                        badge_x -= tw - 8
                    if item.get("material_identified"):
                        lbl = "Material ✓"
                        tw = get_font(11).size(lbl)[0]
                        draw_text(surface, lbl, badge_x - tw, item_rect.y + 6,
                                  (200, 160, 60), 11)

                # Source
                src = item.get("source", "")
                if src:
                    draw_text(surface, f"from {src}", item_rect.x + 10,
                              item_rect.y + 44, DARK_GREY, 11)

                iy += 68

        # ── Identify action button (if char + item both selected) ──
        if (self.id_selected_char >= 0 and self.id_selected_item >= 0 and
                self.id_selected_item < len(self.loot_items)):
            char = self.party[self.id_selected_char]
            comb = self._find_combatant(char)
            item = self.loot_items[self.id_selected_item]

            if comb and not item.get("identified"):
                options = get_identify_options(comb)
                btn_y = panel_r.y + panel_r.height + 15
                bx = 420
                for ai, opt in enumerate(options):
                    btn_rect = pygame.Rect(bx, btn_y, 240, 40)
                    hover = btn_rect.collidepoint(mx, my) and opt["can_afford"]

                    if not opt["can_afford"]:
                        bg = (30, 15, 15)
                        border = (80, 30, 30)
                    elif hover:
                        bg = (60, 50, 90)
                        border = GOLD
                    else:
                        bg = ITEM_BG
                        border = PANEL_BORDER

                    pygame.draw.rect(surface, bg, btn_rect, border_radius=3)
                    pygame.draw.rect(surface, border, btn_rect, 2, border_radius=3)

                    col = GOLD if hover else (CREAM if opt["can_afford"] else DARK_GREY)
                    draw_text(surface, opt["name"], btn_rect.x + 10, btn_rect.y + 4,
                              col, 15, bold=True)
                    draw_text(surface, opt["description"], btn_rect.x + 10,
                              btn_rect.y + 22, DARK_GREY, 11)
                    bx += 252

        # ── Identification log ──
        log_rect = pygame.Rect(420, 680, SCREEN_W - 440, 200)
        draw_panel(surface, log_rect, bg_color=(10, 8, 18))
        draw_text(surface, "Identification Log", log_rect.x + 10, log_rect.y + 6,
                  DIM_GOLD, 13, bold=True)
        ly = log_rect.y + 26
        # Show last ~9 messages
        visible = min(9, len(self.id_log))
        start = max(0, len(self.id_log) - visible)
        for msg, col in self.id_log[start:]:
            draw_text(surface, msg, log_rect.x + 10, ly, col, 13,
                      max_width=log_rect.width - 20)
            ly += 18

        # ── Continue button ──
        btn = pygame.Rect(SCREEN_W // 2 - 140, SCREEN_H - 65, 280, 45)
        label = "Continue to Loot →" if self.loot_items else "Continue →"
        hover = btn.collidepoint(mx, my)
        self.hover_btn = 10 if hover else self.hover_btn
        draw_button(surface, btn, label, hover=hover, size=16)

    # ─────────────────────────────────────────────────────────
    #  PHASE 3: LOOT ASSIGNMENT
    # ─────────────────────────────────────────────────────────

    def _draw_loot_phase(self, surface, mx, my):
        draw_text(surface, "Assign Loot", 40, 65, CREAM, 20, bold=True)
        draw_text(surface, "Select an item, then click a party member to assign it.",
                  40, 90, DARK_GREY, 14)

        # ── Top: Item list ──
        panel_items = pygame.Rect(20, 115, SCREEN_W - 40, 280)
        draw_panel(surface, panel_items, bg_color=SECTION_BG)
        draw_text(surface, "Dropped Items", panel_items.x + 10, panel_items.y + 8,
                  GOLD, 16, bold=True)

        if not self.loot_items:
            draw_text(surface, "No items to assign.", panel_items.x + 20,
                      panel_items.y + 40, DARK_GREY, 15)
        else:
            ix = panel_items.x + 10
            iy = panel_items.y + 35
            col_w = (panel_items.width - 30) // 2
            for idx, item in enumerate(self.loot_items):
                col_idx = idx % 2
                row_idx = idx // 2
                item_rect = pygame.Rect(
                    ix + col_idx * (col_w + 10),
                    iy + row_idx * 68,
                    col_w, 62
                )
                is_hover = item_rect.collidepoint(mx, my)
                is_sel = (idx == self.loot_selected_item)
                is_assigned = idx in self.loot_assignments

                if is_assigned:
                    bg = (20, 30, 20)
                    border = ASSIGNED_COL
                elif is_sel:
                    bg = ITEM_SELECTED
                    border = GOLD
                elif is_hover:
                    bg = ITEM_HOVER
                    border = HIGHLIGHT
                else:
                    bg = ITEM_BG
                    border = PANEL_BORDER

                pygame.draw.rect(surface, bg, item_rect, border_radius=3)
                pygame.draw.rect(surface, border, item_rect, 2, border_radius=3)

                display_name = get_item_display_name(item)
                rarity = item.get("rarity", "common")
                name_col = RARITY_COLORS.get(rarity, CREAM) if item.get("identified") else GREY
                draw_text(surface, display_name, item_rect.x + 10, item_rect.y + 6,
                          name_col, 14, bold=True)

                desc = get_item_display_desc(item)
                if len(desc) > 60:
                    desc = desc[:57] + "..."
                draw_text(surface, desc, item_rect.x + 10, item_rect.y + 24,
                          GREY, 11, max_width=item_rect.width - 20)

                # Assignment label
                if is_assigned:
                    owner = self.party[self.loot_assignments[idx]]
                    draw_text(surface, f"→ {owner.name}", item_rect.x + 10,
                              item_rect.y + 44, ASSIGNED_COL, 12, bold=True)

        # ── Bottom: Party member targets ──
        panel_party = pygame.Rect(20, 415, SCREEN_W - 40, 260)
        draw_panel(surface, panel_party, bg_color=SECTION_BG)
        draw_text(surface, "Assign To:", panel_party.x + 10, panel_party.y + 8,
                  GOLD, 16, bold=True)

        self.loot_hover_char = -1
        cx = panel_party.x + 10
        cy_start = panel_party.y + 35
        card_w = (panel_party.width - 40) // 3
        card_h = 100

        for i, char in enumerate(self.party):
            col_idx = i % 3
            row_idx = i // 3
            cls = CLASSES[char.class_name]

            card_rect = pygame.Rect(
                cx + col_idx * (card_w + 10),
                cy_start + row_idx * (card_h + 8),
                card_w, card_h
            )
            is_hover = card_rect.collidepoint(mx, my)
            if is_hover:
                self.loot_hover_char = i

            if is_hover and self.loot_selected_item >= 0:
                bg = (45, 38, 75)
                border = cls["color"]
            else:
                bg = ITEM_BG
                border = PANEL_BORDER

            pygame.draw.rect(surface, bg, card_rect, border_radius=3)
            pygame.draw.rect(surface, border, card_rect, 2, border_radius=3)

            draw_text(surface, char.name, card_rect.x + 10, card_rect.y + 6,
                      cls["color"], 15, bold=True)
            draw_text(surface, f"Lv.{char.level} {char.class_name}",
                      card_rect.x + 10, card_rect.y + 26, GREY, 12)

            # Count items assigned to this char
            count = sum(1 for v in self.loot_assignments.values() if v == i)
            if count > 0:
                draw_text(surface, f"{count} item(s) assigned",
                          card_rect.x + 10, card_rect.y + 48, ASSIGNED_COL, 12)

            # Show inventory count
            draw_text(surface, f"Inventory: {len(char.inventory)} items",
                      card_rect.x + 10, card_rect.y + 68, DARK_GREY, 11)

        # ── Continue button ──
        btn = pygame.Rect(SCREEN_W // 2 - 140, SCREEN_H - 65, 280, 45)
        # Check if all items assigned
        all_assigned = all(i in self.loot_assignments for i in range(len(self.loot_items)))
        if not self.loot_items:
            all_assigned = True
        label = "Finish" if all_assigned else "Finish (unassigned items will be lost)"
        hover = btn.collidepoint(mx, my)
        self.hover_btn = 20 if hover else self.hover_btn
        draw_button(surface, btn, label, hover=hover, size=14)

    # ─────────────────────────────────────────────────────────
    #  PHASE 4: DONE SUMMARY
    # ─────────────────────────────────────────────────────────

    def _draw_done_phase(self, surface, mx, my):
        draw_text(surface, "Battle Complete!", SCREEN_W // 2 - 120, 80,
                  GOLD, 26, bold=True)

        y = 140
        for char in self.party:
            cls = CLASSES[char.class_name]
            draw_text(surface, f"{char.name}", 60, y, cls["color"], 18, bold=True)
            draw_text(surface, f"Level {char.level}  {char.class_name}  |  "
                      f"{char.gold} gold  |  {len(char.inventory)} items",
                      60, y + 24, GREY, 14)
            y += 60

        btn = pygame.Rect(SCREEN_W // 2 - 140, SCREEN_H - 80, 280, 50)
        hover = btn.collidepoint(mx, my)
        self.hover_btn = 30 if hover else self.hover_btn
        draw_button(surface, btn, "Return to Party", hover=hover, size=18)

    # ─────────────────────────────────────────────────────────
    #  EVENT HANDLING
    # ─────────────────────────────────────────────────────────

    def handle_click(self, mx, my):
        """Handle mouse click. Returns 'continue' when player finishes all phases."""
        # ── Continue/Next button ──
        btn = pygame.Rect(SCREEN_W // 2 - 140, SCREEN_H - 65, 280, 45)
        done_btn = pygame.Rect(SCREEN_W // 2 - 140, SCREEN_H - 80, 280, 50)

        if self.phase == self.PHASE_XP:
            if btn.collidepoint(mx, my):
                if self.loot_items:
                    self.phase = self.PHASE_ID
                else:
                    self.phase = self.PHASE_DONE
                return None

        elif self.phase == self.PHASE_ID:
            # Check identification action buttons
            if (self.id_selected_char >= 0 and self.id_selected_item >= 0 and
                    self.id_selected_item < len(self.loot_items)):
                char = self.party[self.id_selected_char]
                comb = self._find_combatant(char)
                item = self.loot_items[self.id_selected_item]

                if comb and not item.get("identified"):
                    # Find which panel_r position we used
                    panel_r = pygame.Rect(420, 115, SCREEN_W - 440, 340)
                    options = get_identify_options(comb)
                    btn_y = panel_r.y + panel_r.height + 15
                    bx = 420
                    for ai, opt in enumerate(options):
                        btn_rect = pygame.Rect(bx, btn_y, 240, 40)
                        if btn_rect.collidepoint(mx, my) and opt["can_afford"]:
                            self._do_identify(comb, item, opt["action"], char)
                            return None
                        bx += 252

            # Check char selection (left panel)
            panel_l = pygame.Rect(20, 115, 380, 520)
            cy = panel_l.y + 35
            for i, char in enumerate(self.party):
                card_rect = pygame.Rect(panel_l.x + 8, cy, panel_l.width - 16, 72)
                if card_rect.collidepoint(mx, my):
                    can_id = (char.class_name in ARCANE_LORE_CLASSES or
                              char.class_name in APPRAISAL_CLASSES)
                    if can_id:
                        self.id_selected_char = i
                    return None
                cy += 80

            # Check item selection (right panel)
            panel_r = pygame.Rect(420, 115, SCREEN_W - 440, 340)
            iy = panel_r.y + 35
            for idx, item in enumerate(self.loot_items):
                item_rect = pygame.Rect(panel_r.x + 8, iy, panel_r.width - 16, 60)
                if item_rect.collidepoint(mx, my):
                    self.id_selected_item = idx
                    return None
                iy += 68

            # Continue button
            if btn.collidepoint(mx, my):
                if self.loot_items:
                    self.phase = self.PHASE_LOOT
                else:
                    self.phase = self.PHASE_DONE
                return None

        elif self.phase == self.PHASE_LOOT:
            # Item selection
            panel_items = pygame.Rect(20, 115, SCREEN_W - 40, 280)
            ix = panel_items.x + 10
            iy = panel_items.y + 35
            col_w = (panel_items.width - 30) // 2
            for idx in range(len(self.loot_items)):
                col_idx = idx % 2
                row_idx = idx // 2
                item_rect = pygame.Rect(
                    ix + col_idx * (col_w + 10),
                    iy + row_idx * 68,
                    col_w, 62
                )
                if item_rect.collidepoint(mx, my):
                    self.loot_selected_item = idx
                    return None

            # Party member assignment
            if self.loot_selected_item >= 0 and self.loot_hover_char >= 0:
                panel_party = pygame.Rect(20, 415, SCREEN_W - 40, 260)
                cx = panel_party.x + 10
                cy_start = panel_party.y + 35
                card_w = (panel_party.width - 40) // 3
                card_h = 100
                for i in range(len(self.party)):
                    col_idx = i % 3
                    row_idx = i // 3
                    card_rect = pygame.Rect(
                        cx + col_idx * (card_w + 10),
                        cy_start + row_idx * (card_h + 8),
                        card_w, card_h
                    )
                    if card_rect.collidepoint(mx, my):
                        self.loot_assignments[self.loot_selected_item] = i
                        self.loot_selected_item = -1
                        return None

            # Continue button
            if btn.collidepoint(mx, my):
                self._finalize_loot()
                self.phase = self.PHASE_DONE
                return None

        elif self.phase == self.PHASE_DONE:
            if done_btn.collidepoint(mx, my):
                self.finished = True
                return "continue"

        return None

    def handle_scroll(self, direction):
        """Handle scroll in identification log."""
        if self.phase == self.PHASE_ID:
            self.id_scroll += direction

    # ─────────────────────────────────────────────────────────
    #  IDENTIFICATION LOGIC
    # ─────────────────────────────────────────────────────────

    def _do_identify(self, combatant, item, action, char):
        """Perform an identification attempt and log the result."""
        results, all_ok = attempt_identify(combatant, item, action)

        for check_name, success, msg in results:
            col = SUCCESS_COL if success else FAIL_COL
            self.id_log.append((f"[{char.name}] {msg}", col))

        if item.get("identified"):
            full_name = item.get("name", "Unknown")
            self.id_log.append((f"  → Fully identified: {full_name}", GOLD))

    # ─────────────────────────────────────────────────────────
    #  LOOT FINALIZATION
    # ─────────────────────────────────────────────────────────

    def _finalize_loot(self):
        """Move assigned items into character inventories."""
        for item_idx, char_idx in self.loot_assignments.items():
            if item_idx < len(self.loot_items) and char_idx < len(self.party):
                item = self.loot_items[item_idx]
                self.party[char_idx].add_item(item)

    # ─────────────────────────────────────────────────────────
    #  HELPERS
    # ─────────────────────────────────────────────────────────

    def _find_combatant(self, char):
        """Find the combatant dict for a given Character (has current resources)."""
        for c in self.combatants:
            if c.get("name") == char.name and c.get("class_name") == char.class_name:
                return c
        return None
