"""
Realm of Shadows — Camp Screen UI

Full-screen camp interface accessible from dungeons (C key) and world map.
Tabs: Rest, Inventory, Equipment, Identify, Party Stats

Replaces the simple "rest yes/no" confirm dialog with a rich camp experience.
"""
import pygame
from ui.renderer import (
    SCREEN_W, SCREEN_H, draw_text, draw_panel, draw_button, get_font,
    CREAM, GOLD, GREY, DARK_GREY, WHITE, PANEL_BG, PANEL_BORDER,
    HIGHLIGHT, DIM_GOLD, ORANGE, RED, GREEN,
)

# ── Colors ──
CAMP_BG = (10, 8, 18)
TAB_BG = (20, 16, 32)
TAB_ACTIVE = (40, 32, 60)
TAB_BORDER = (80, 70, 110)
STAT_LABEL = (160, 150, 180)
STAT_VAL = (220, 220, 200)
HP_BAR = (50, 180, 80)
HP_BAR_BG = (30, 40, 30)
MP_BAR = (60, 100, 200)
SP_BAR = (200, 160, 60)
ITEM_BG = (25, 22, 40)
ITEM_HOVER = (40, 35, 60)
EQUIP_SLOT_BG = (18, 14, 30)
EQUIP_SLOT_BORDER = (60, 50, 90)
HEAL_COL = (100, 255, 140)

# ── Tabs ──
TAB_REST = 0
TAB_INVENTORY = 1
TAB_EQUIP = 2
TAB_IDENTIFY = 3
TAB_STATS = 4
TAB_TRANSFER = 5
TAB_NAMES = ["Rest", "Inventory", "Equipment", "Identify", "Party", "Transfer"]
TAB_COUNT = len(TAB_NAMES)

# ── Slots ──
EQUIP_SLOTS = ["weapon", "body", "head", "accessory1", "accessory2"]
SLOT_LABELS = {"weapon": "Weapon", "body": "Body", "head": "Head",
               "accessory1": "Ring 1", "accessory2": "Ring 2"}


class CampUI:
    """Full camp screen with tabs."""

    def __init__(self, party, location="dungeon", dungeon_floor=1):
        self.party = party
        self.location = location  # "dungeon" or "overworld"
        self.dungeon_floor = dungeon_floor
        self.tab = TAB_REST
        self.finished = False
        self.result = None  # "rest", "cancel", etc.

        # State
        self.selected_char = 0
        self.selected_item = -1
        self.scroll_offset = 0
        self.message = ""
        self.msg_color = CREAM
        self.msg_timer = 0

        # Identify state
        self.identify_char = -1
        self.identify_target_char = -1
        self.identify_target_item = -1

        # Transfer state
        self.transfer_src_char = 0
        self.transfer_dst_char = 1 if len(party) > 1 else 0
        self.transfer_selected_item = -1

    def draw(self, surface, mx, my, dt=16):
        surface.fill(CAMP_BG)

        # Title
        title = "Camp — Dungeon" if self.location == "dungeon" else "Camp — Wilderness"
        draw_text(surface, title, SCREEN_W // 2 - 120, 8, GOLD, 22, bold=True)

        # Leave button
        leave = pygame.Rect(SCREEN_W - 130, 8, 110, 30)
        draw_button(surface, leave, "Break Camp", hover=leave.collidepoint(mx, my), size=12)

        # Tabs
        tw = SCREEN_W // TAB_COUNT
        for i, name in enumerate(TAB_NAMES):
            r = pygame.Rect(i * tw, 42, tw, 32)
            bg = TAB_ACTIVE if i == self.tab else TAB_BG
            pygame.draw.rect(surface, bg, r)
            pygame.draw.rect(surface, TAB_BORDER if i == self.tab else PANEL_BORDER, r, 1)
            col = GOLD if i == self.tab else GREY
            draw_text(surface, name, r.x + tw // 2 - len(name) * 4, r.y + 7, col, 14,
                      bold=(i == self.tab))

        # Tab content
        content_y = 80
        if self.tab == TAB_REST:
            self._draw_rest(surface, mx, my, content_y)
        elif self.tab == TAB_INVENTORY:
            self._draw_inventory(surface, mx, my, content_y)
        elif self.tab == TAB_EQUIP:
            self._draw_equipment(surface, mx, my, content_y)
        elif self.tab == TAB_IDENTIFY:
            self._draw_identify(surface, mx, my, content_y)
        elif self.tab == TAB_STATS:
            self._draw_stats(surface, mx, my, content_y)
        elif self.tab == TAB_TRANSFER:
            self._draw_transfer(surface, mx, my, content_y)

        # Message bar
        if self.msg_timer > 0:
            self.msg_timer -= dt
            draw_text(surface, self.message, SCREEN_W // 2 - 200, SCREEN_H - 30,
                      self.msg_color, 13)

    # ──────────────────────────────────────────────────────────
    #  REST TAB
    # ──────────────────────────────────────────────────────────

    def _draw_rest(self, surface, mx, my, top):
        from core.classes import get_all_resources

        draw_text(surface, "Set up camp and rest?", SCREEN_W // 2 - 100, top, CREAM, 18)

        if self.location == "dungeon":
            ambush_pct = 25 + self.dungeon_floor * 5
            for c in self.party:
                if c.class_name == "Ranger":
                    ambush_pct -= 5
                if c.class_name == "Cleric":
                    ambush_pct -= 3
            ambush_pct = max(5, ambush_pct)
            draw_text(surface, f"Ambush risk: {ambush_pct}%", SCREEN_W // 2 - 70,
                      top + 30, ORANGE, 14)
            draw_text(surface, "Restores ~25% HP, ~15% MP/SP",
                      SCREEN_W // 2 - 115, top + 52, GREY, 13)
        else:
            draw_text(surface, "Ambush risk: Low", SCREEN_W // 2 - 60, top + 30, GREEN, 14)
            draw_text(surface, "Restores ~40% HP, ~25% MP/SP",
                      SCREEN_W // 2 - 115, top + 52, GREY, 13)

        # Party status preview
        cy = top + 90
        for c in self.party:
            max_res = get_all_resources(c.class_name, c.stats, c.level)
            max_hp = max_res.get("HP", 1)
            cur_hp = c.resources.get("HP", 0)
            pct = cur_hp / max_hp if max_hp else 0

            row = pygame.Rect(60, cy, SCREEN_W - 120, 36)
            pygame.draw.rect(surface, ITEM_BG, row, border_radius=3)

            draw_text(surface, f"{c.name} ({c.class_name})", row.x + 10, row.y + 3,
                      CREAM, 13, bold=True)

            # HP bar
            bar_x, bar_w = row.x + 250, 200
            bar = pygame.Rect(bar_x, row.y + 6, bar_w, 10)
            pygame.draw.rect(surface, HP_BAR_BG, bar, border_radius=2)
            fill = pygame.Rect(bar_x, row.y + 6, int(bar_w * pct), 10)
            col = HP_BAR if pct > 0.3 else RED if pct > 0.1 else (180, 30, 30)
            pygame.draw.rect(surface, col, fill, border_radius=2)
            draw_text(surface, f"{cur_hp}/{max_hp}", bar_x + bar_w + 8, row.y + 2,
                      GREY, 12)

            # Other resources summary
            other = []
            for rn, mv in max_res.items():
                if rn == "HP":
                    continue
                cv = c.resources.get(rn, 0)
                if mv > 0:
                    other.append(f"{rn}:{cv}/{mv}")
            if other:
                draw_text(surface, "  ".join(other[:3]), bar_x + bar_w + 80, row.y + 2,
                          STAT_LABEL, 10)

            cy += 40

        # Rest button
        rest_btn = pygame.Rect(SCREEN_W // 2 - 80, cy + 20, 160, 45)
        draw_button(surface, rest_btn, "🔥 Rest", hover=rest_btn.collidepoint(mx, my), size=16)

    # ──────────────────────────────────────────────────────────
    #  INVENTORY TAB
    # ──────────────────────────────────────────────────────────

    def _draw_inventory(self, surface, mx, my, top):
        # Character selector
        self._draw_char_selector(surface, mx, my, top)
        c = self.party[self.selected_char]

        # Inventory list
        iy = top + 45
        if not c.inventory:
            draw_text(surface, "No items.", 80, iy, GREY, 14)
            return

        visible = c.inventory[self.scroll_offset:self.scroll_offset + 12]
        for i, item in enumerate(visible):
            idx = self.scroll_offset + i
            row = pygame.Rect(60, iy, SCREEN_W - 120, 34)
            hover = row.collidepoint(mx, my)
            bg = ITEM_HOVER if hover else ITEM_BG
            pygame.draw.rect(surface, bg, row, border_radius=3)
            if idx == self.selected_item:
                pygame.draw.rect(surface, GOLD, row, 2, border_radius=3)

            from core.identification import get_item_display_name
            name = get_item_display_name(item)
            stack = item.get("stack", 1)
            stack_str = f" ×{stack}" if stack > 1 else ""
            draw_text(surface, f"{name}{stack_str}", row.x + 10, row.y + 7, CREAM, 13)

            itype = item.get("type", "misc")
            draw_text(surface, itype, row.x + row.width - 80, row.y + 7, STAT_LABEL, 11)
            iy += 38

        # Item action buttons if something selected
        if 0 <= self.selected_item < len(c.inventory):
            item = c.inventory[self.selected_item]
            by = iy + 10
            if item.get("type") in ("consumable", "potion", "food"):
                use_btn = pygame.Rect(80, by, 120, 34)
                draw_button(surface, use_btn, "Use", hover=use_btn.collidepoint(mx, my), size=13)
            if item.get("slot"):
                equip_btn = pygame.Rect(210, by, 120, 34)
                draw_button(surface, equip_btn, "Equip",
                            hover=equip_btn.collidepoint(mx, my), size=13)
            drop_btn = pygame.Rect(340, by, 120, 34)
            draw_button(surface, drop_btn, "Drop", hover=drop_btn.collidepoint(mx, my), size=13)

    # ──────────────────────────────────────────────────────────
    #  EQUIPMENT TAB
    # ──────────────────────────────────────────────────────────

    def _draw_equipment(self, surface, mx, my, top):
        self._draw_char_selector(surface, mx, my, top)
        c = self.party[self.selected_char]
        equipment = c.equipment if hasattr(c, "equipment") and c.equipment else {}

        ey = top + 45
        for slot in EQUIP_SLOTS:
            row = pygame.Rect(60, ey, SCREEN_W - 120, 38)
            hover = row.collidepoint(mx, my)
            bg = ITEM_HOVER if hover else EQUIP_SLOT_BG
            pygame.draw.rect(surface, bg, row, border_radius=3)
            pygame.draw.rect(surface, EQUIP_SLOT_BORDER, row, 1, border_radius=3)

            label = SLOT_LABELS.get(slot, slot)
            draw_text(surface, f"{label}:", row.x + 10, row.y + 8, STAT_LABEL, 13)

            equipped = equipment.get(slot)
            if equipped:
                from core.identification import get_item_display_name
                name = get_item_display_name(equipped)
                draw_text(surface, name, row.x + 120, row.y + 8, CREAM, 13, bold=True)
                # Unequip hint on hover
                if hover:
                    draw_text(surface, "[Click to unequip]", row.x + row.width - 150,
                              row.y + 8, DIM_GOLD, 11)
            else:
                draw_text(surface, "— empty —", row.x + 120, row.y + 8, DARK_GREY, 13)

            ey += 42

        # Show equippable items from inventory
        draw_text(surface, "Equippable items in inventory:", 60, ey + 10, DIM_GOLD, 13)
        ey += 30
        for i, item in enumerate(c.inventory):
            if not item.get("slot"):
                continue
            row = pygame.Rect(80, ey, SCREEN_W - 160, 32)
            hover = row.collidepoint(mx, my)
            bg = ITEM_HOVER if hover else ITEM_BG
            pygame.draw.rect(surface, bg, row, border_radius=3)
            from core.identification import get_item_display_name
            name = get_item_display_name(item)
            slot = item["slot"]
            draw_text(surface, f"{name} [{slot}]", row.x + 10, row.y + 6, CREAM, 12)
            if hover:
                draw_text(surface, "[Click to equip]", row.x + row.width - 130,
                          row.y + 6, DIM_GOLD, 11)
            ey += 36
            if ey > SCREEN_H - 60:
                break

    # ──────────────────────────────────────────────────────────
    #  IDENTIFY TAB
    # ──────────────────────────────────────────────────────────

    def _draw_identify(self, surface, mx, my, top):
        from core.identification import needs_identification, get_identify_options

        # Find party members who can identify
        identifiers = []
        for i, c in enumerate(self.party):
            combatant = self._char_to_combatant(c)
            opts = get_identify_options(combatant)
            if opts:
                identifiers.append((i, c, opts))

        # Find unidentified items
        unid_items = []
        for ci, c in enumerate(self.party):
            for ii, item in enumerate(c.inventory):
                if needs_identification(item):
                    unid_items.append((ci, ii, item, c))

        if not unid_items:
            draw_text(surface, "No items need identification.", 80, top + 10, GREEN, 15)
            return

        draw_text(surface, f"Unidentified items: {len(unid_items)}", 60, top, DIM_GOLD, 14)

        if not identifiers:
            draw_text(surface, "No party members can identify items here.",
                      60, top + 25, RED, 13)
            draw_text(surface, "Visit a temple or recruit a Mage/Thief.",
                      60, top + 45, GREY, 12)
        else:
            names = ", ".join(f"{c.name} ({c.class_name})" for _, c, _ in identifiers)
            draw_text(surface, f"Can identify: {names}", 60, top + 25, HEAL_COL, 12)

        uy = top + 55
        for ui_idx, (ci, ii, item, char) in enumerate(unid_items[:8]):
            row = pygame.Rect(60, uy, SCREEN_W - 120, 36)
            hover = row.collidepoint(mx, my)
            bg = ITEM_HOVER if hover else ITEM_BG
            pygame.draw.rect(surface, bg, row, border_radius=3)

            from core.identification import get_item_display_name
            name = get_item_display_name(item)
            draw_text(surface, f"{char.name}: {name}", row.x + 10, row.y + 7, GREY, 13)

            if identifiers and hover:
                draw_text(surface, "[Click to identify]", row.x + row.width - 150,
                          row.y + 7, DIM_GOLD, 11)
            uy += 40

    # ──────────────────────────────────────────────────────────
    #  STATS TAB
    # ──────────────────────────────────────────────────────────

    def _draw_stats(self, surface, mx, my, top):
        self._draw_char_selector(surface, mx, my, top)
        c = self.party[self.selected_char]
        from core.classes import get_all_resources, STAT_NAMES

        sy = top + 45
        # Basic info
        draw_text(surface, f"{c.name}", 80, sy, GOLD, 18, bold=True)
        draw_text(surface, f"Level {c.level} {c.race_name} {c.class_name}",
                  80, sy + 24, CREAM, 14)
        draw_text(surface, f"XP: {c.xp}", 80, sy + 44, DIM_GOLD, 12)

        # Stats
        sy += 70
        stat_x = 80
        for i, stat in enumerate(STAT_NAMES):
            val = c.stats.get(stat, 0)
            col = STAT_VAL
            if hasattr(c, "effective_stats"):
                eff = c.effective_stats().get(stat, val)
                if eff > val:
                    col = GREEN
                elif eff < val:
                    col = RED
                val = eff

            draw_text(surface, f"{stat}:", stat_x, sy + i * 24, STAT_LABEL, 14)
            draw_text(surface, str(val), stat_x + 45, sy + i * 24, col, 14, bold=True)

        # Resources
        rx = 280
        max_res = get_all_resources(c.class_name, c.stats, c.level)
        ry = top + 115
        for rn, mv in max_res.items():
            cv = c.resources.get(rn, 0)
            pct = cv / mv if mv > 0 else 0
            draw_text(surface, f"{rn}:", rx, ry, STAT_LABEL, 13)
            # Bar
            bar = pygame.Rect(rx + 60, ry + 2, 150, 12)
            pygame.draw.rect(surface, HP_BAR_BG, bar, border_radius=2)
            if rn == "HP":
                fill_col = HP_BAR
            elif "MP" in rn:
                fill_col = MP_BAR
            else:
                fill_col = SP_BAR
            fill = pygame.Rect(bar.x, bar.y, int(bar.width * pct), bar.height)
            pygame.draw.rect(surface, fill_col, fill, border_radius=2)
            draw_text(surface, f"{cv}/{mv}", rx + 220, ry, GREY, 12)
            ry += 22

        # Status effects
        if hasattr(c, "status_effects") and c.status_effects:
            ry += 10
            draw_text(surface, "Status:", rx, ry, STAT_LABEL, 13)
            ry += 18
            for eff in c.status_effects:
                eff_name = eff.get("type", eff.get("name", "???"))
                draw_text(surface, f"• {eff_name}", rx + 10, ry, ORANGE, 12)
                ry += 16

    # ──────────────────────────────────────────────────────────
    #  SHARED WIDGETS
    # ──────────────────────────────────────────────────────────

    def _draw_char_selector(self, surface, mx, my, top):
        """Draw character tabs for selecting party member, with reorder arrows."""
        # Reorder arrows (◄ ►) for selected char
        self._reorder_left_rect  = None
        self._reorder_right_rect = None

        draw_text(surface, "Order:", 8, top + 7, GREY, 11)
        cx = 60
        for i, c in enumerate(self.party):
            w = max(80, len(c.name) * 8 + 20)
            r = pygame.Rect(cx, top, w, 30)
            hover = r.collidepoint(mx, my)
            bg = TAB_ACTIVE if i == self.selected_char else (TAB_BG if not hover else ITEM_HOVER)
            pygame.draw.rect(surface, bg, r, border_radius=3)
            if i == self.selected_char:
                pygame.draw.rect(surface, GOLD, r, 2, border_radius=3)
                # Draw ◄ left arrow if not first
                if i > 0:
                    lr = pygame.Rect(cx - 22, top + 4, 18, 22)
                    lhov = lr.collidepoint(mx, my)
                    pygame.draw.rect(surface, (50,40,20) if lhov else (30,25,12), lr, border_radius=3)
                    pygame.draw.rect(surface, GOLD if lhov else DIM_GOLD, lr, 1, border_radius=3)
                    draw_text(surface, "◄", lr.x + 2, lr.y + 3, GOLD if lhov else DIM_GOLD, 12)
                    self._reorder_left_rect = lr
                # Draw ► right arrow if not last
                if i < len(self.party) - 1:
                    rr = pygame.Rect(cx + w + 2, top + 4, 18, 22)
                    rhov = rr.collidepoint(mx, my)
                    pygame.draw.rect(surface, (50,40,20) if rhov else (30,25,12), rr, border_radius=3)
                    pygame.draw.rect(surface, GOLD if rhov else DIM_GOLD, rr, 1, border_radius=3)
                    draw_text(surface, "►", rr.x + 2, rr.y + 3, GOLD if rhov else DIM_GOLD, 12)
                    self._reorder_right_rect = rr
            col = GOLD if i == self.selected_char else CREAM
            draw_text(surface, c.name, r.x + 8, r.y + 6, col, 12, bold=(i == self.selected_char))
            cx += w + 6

    def _char_to_combatant(self, c):
        """Convert Character to a dict for identification system."""
        return {
            "name": c.name,
            "class_name": c.class_name,
            "level": c.level,
            "stats": dict(c.stats),
            "resources": dict(c.resources),
        }

    def _msg(self, text, color=CREAM):
        self.message = text
        self.msg_color = color
        self.msg_timer = 3000

    # ──────────────────────────────────────────────────────────
    #  TRANSFER TAB
    # ──────────────────────────────────────────────────────────

    def _draw_transfer(self, surface, mx, my, top):
        """Draw the item/equipment transfer screen between party members."""
        if len(self.party) < 2:
            draw_text(surface, "Need at least 2 party members to transfer items.",
                      80, top + 30, GREY, 15)
            return

        # ── Layout ──
        panel_w = SCREEN_W // 2 - 40
        left_x  = 30
        right_x = SCREEN_W // 2 + 10
        item_h  = 32

        # ── Source char selector (left panel header) ──
        draw_text(surface, "FROM:", left_x, top, STAT_LABEL, 13)
        for i, ch in enumerate(self.party):
            bx = left_x + i * 110
            by = top + 14
            btn = pygame.Rect(bx, by, 105, 26)
            active = (i == self.transfer_src_char)
            pygame.draw.rect(surface, TAB_ACTIVE if active else TAB_BG, btn)
            pygame.draw.rect(surface, TAB_BORDER if active else PANEL_BORDER, btn, 1)
            draw_text(surface, ch.name[:10], bx + 5, by + 5,
                      GOLD if active else GREY, 13, bold=active)

        # ── Destination char selector (right panel header) ──
        draw_text(surface, "TO:", right_x, top, STAT_LABEL, 13)
        for i, ch in enumerate(self.party):
            bx = right_x + i * 110
            by = top + 14
            btn = pygame.Rect(bx, by, 105, 26)
            active = (i == self.transfer_dst_char)
            pygame.draw.rect(surface, TAB_ACTIVE if active else TAB_BG, btn)
            pygame.draw.rect(surface, TAB_BORDER if active else PANEL_BORDER, btn, 1)
            draw_text(surface, ch.name[:10], bx + 5, by + 5,
                      GOLD if active else GREY, 13, bold=active)

        src  = self.party[self.transfer_src_char]
        dst  = self.party[self.transfer_dst_char]
        list_top = top + 50

        # ── Source inventory list ──
        draw_text(surface, f"{src.name}'s Items", left_x, list_top, CREAM, 14, bold=True)
        iy = list_top + 22
        all_items = list(src.inventory)
        # Also list equipped items
        if hasattr(src, "equipment") and src.equipment:
            for slot, item in src.equipment.items():
                if item:
                    all_items.append({**item, "_equipped_slot": slot})

        if not all_items:
            draw_text(surface, "No items.", left_x + 10, iy, GREY, 13)
        for idx, item in enumerate(all_items[:14]):
            row = pygame.Rect(left_x, iy + idx * item_h, panel_w, item_h - 2)
            selected = (idx == self.transfer_selected_item)
            hov = row.collidepoint(mx, my)
            pygame.draw.rect(surface, ITEM_HOVER if (selected or hov) else ITEM_BG, row)
            pygame.draw.rect(surface, GOLD if selected else PANEL_BORDER, row, 1)
            from core.identification import get_item_display_name
            name = get_item_display_name(item)
            slot_tag = f" [EQ:{item.get('_equipped_slot','').upper()}]" if "_equipped_slot" in item else ""
            stack = item.get("stack", 1)
            stack_str = f" x{stack}" if stack > 1 else ""
            draw_text(surface, f"{name}{slot_tag}{stack_str}", left_x + 6, iy + idx * item_h + 7,
                      GOLD if selected else CREAM, 13)

        # ── Transfer button (center) ──
        btn_x = SCREEN_W // 2 - 40
        btn_y = list_top + 22 + 7 * item_h
        transfer_btn = pygame.Rect(btn_x, btn_y, 80, 34)
        can_transfer = (self.transfer_selected_item >= 0 and
                        self.transfer_src_char != self.transfer_dst_char and
                        self.transfer_selected_item < len(all_items))
        hov = transfer_btn.collidepoint(mx, my)
        pygame.draw.rect(surface, (40,80,40) if (can_transfer and hov) else (25,40,25), transfer_btn)
        pygame.draw.rect(surface, (80,180,80) if can_transfer else DARK_GREY, transfer_btn, 1)
        draw_text(surface, "→ Give →", btn_x + 4, btn_y + 9,
                  GREEN if can_transfer else DARK_GREY, 13, bold=True)

        # ── Destination inventory list (read-only preview) ──
        draw_text(surface, f"{dst.name}'s Items", right_x, list_top, CREAM, 14, bold=True)
        dy = list_top + 22
        dst_items = list(dst.inventory)
        if hasattr(dst, "equipment") and dst.equipment:
            for slot, item in dst.equipment.items():
                if item:
                    dst_items.append({**item, "_equipped_slot": slot})
        if not dst_items:
            draw_text(surface, "No items.", right_x + 10, dy, GREY, 13)
        for idx, item in enumerate(dst_items[:14]):
            row = pygame.Rect(right_x, dy + idx * item_h, panel_w, item_h - 2)
            pygame.draw.rect(surface, ITEM_BG, row)
            pygame.draw.rect(surface, PANEL_BORDER, row, 1)
            from core.identification import get_item_display_name
            name = get_item_display_name(item)
            slot_tag = f" [EQ:{item.get('_equipped_slot','').upper()}]" if "_equipped_slot" in item else ""
            draw_text(surface, f"{name}{slot_tag}", right_x + 6, dy + idx * item_h + 7, GREY, 13)

        # ── Status message ──
        if self.message and self.msg_timer > 0:
            draw_text(surface, self.message, left_x, list_top + 14 * item_h + 30,
                      self.msg_color, 14)

        # store for click handler
        self._transfer_all_items = all_items
        self._transfer_list_top  = list_top
        self._transfer_item_h    = item_h
        self._transfer_left_x    = left_x
        self._transfer_panel_w   = panel_w
        self._transfer_btn       = transfer_btn

    def _handle_transfer_click(self, mx, my):
        if len(self.party) < 2:
            return None

        top = 80

        # Source char selector clicks
        for i in range(len(self.party)):
            bx = 30 + i * 110
            btn = pygame.Rect(bx, top + 14, 105, 26)
            if btn.collidepoint(mx, my):
                self.transfer_src_char = i
                if self.transfer_dst_char == i:
                    self.transfer_dst_char = (i + 1) % len(self.party)
                self.transfer_selected_item = -1
                return None

        # Destination char selector clicks
        right_x = SCREEN_W // 2 + 10
        for i in range(len(self.party)):
            bx = right_x + i * 110
            btn = pygame.Rect(bx, top + 14, 105, 26)
            if btn.collidepoint(mx, my):
                self.transfer_dst_char = i
                if self.transfer_src_char == i:
                    self.transfer_src_char = (i + 1) % len(self.party)
                return None

        # Item list clicks (source side)
        list_top = top + 50
        item_h = 32
        left_x = 30
        panel_w = SCREEN_W // 2 - 40

        src = self.party[self.transfer_src_char]
        all_items = list(src.inventory)
        if hasattr(src, "equipment") and src.equipment:
            for slot, item in src.equipment.items():
                if item:
                    all_items.append({**item, "_equipped_slot": slot})

        for idx in range(min(14, len(all_items))):
            row = pygame.Rect(left_x, list_top + 22 + idx * item_h, panel_w, item_h - 2)
            if row.collidepoint(mx, my):
                self.transfer_selected_item = idx
                return None

        # Transfer button
        btn_x = SCREEN_W // 2 - 40
        btn_y = list_top + 22 + 7 * item_h
        transfer_btn = pygame.Rect(btn_x, btn_y, 80, 34)
        if transfer_btn.collidepoint(mx, my):
            if (self.transfer_selected_item >= 0 and
                    self.transfer_src_char != self.transfer_dst_char and
                    self.transfer_selected_item < len(all_items)):
                item = all_items[self.transfer_selected_item]
                dst = self.party[self.transfer_dst_char]
                # Handle equipped vs inventory
                if "_equipped_slot" in item:
                    clean = {k: v for k, v in item.items() if k != "_equipped_slot"}
                    slot = item["_equipped_slot"]
                    src.equipment[slot] = None
                    dst.inventory.append(clean)
                    self.message = f"Unequipped & gave {clean.get('name','item')} to {dst.name}"
                else:
                    src.inventory.remove(item)
                    dst.inventory.append(item)
                    self.message = f"Gave {item.get('name','item')} to {dst.name}"
                self.msg_color = GREEN
                self.msg_timer = 180
                self.transfer_selected_item = -1
        return None

    # ──────────────────────────────────────────────────────────
    #  INPUT HANDLING
    # ──────────────────────────────────────────────────────────

    def handle_click(self, mx, my):
        """Handle mouse click. Returns result string or None."""
        # Leave camp
        leave = pygame.Rect(SCREEN_W - 130, 8, 110, 30)
        if leave.collidepoint(mx, my):
            self.finished = True
            self.result = "cancel"
            return "cancel"

        # Tab clicks
        tw = SCREEN_W // TAB_COUNT
        for i in range(TAB_COUNT):
            r = pygame.Rect(i * tw, 42, tw, 32)
            if r.collidepoint(mx, my):
                self.tab = i
                self.selected_item = -1
                self.scroll_offset = 0
                return None

        # Character reorder arrows (visible on all tabs)
        if getattr(self, "_reorder_left_rect", None) and self._reorder_left_rect.collidepoint(mx, my):
            i = self.selected_char
            if i > 0:
                self.party[i], self.party[i-1] = self.party[i-1], self.party[i]
                self.selected_char = i - 1
            return None
        if getattr(self, "_reorder_right_rect", None) and self._reorder_right_rect.collidepoint(mx, my):
            i = self.selected_char
            if i < len(self.party) - 1:
                self.party[i], self.party[i+1] = self.party[i+1], self.party[i]
                self.selected_char = i + 1
            return None

        # Character selector (tabs that have it)
        if self.tab in (TAB_INVENTORY, TAB_EQUIP, TAB_STATS):
            cx = 60
            for i, c in enumerate(self.party):
                w = max(80, len(c.name) * 8 + 20)
                r = pygame.Rect(cx, 80, w, 30)
                if r.collidepoint(mx, my):
                    self.selected_char = i
                    self.selected_item = -1
                    self.scroll_offset = 0
                    return None
                cx += w + 6

        # Tab-specific
        if self.tab == TAB_REST:
            return self._handle_rest_click(mx, my)
        elif self.tab == TAB_INVENTORY:
            return self._handle_inventory_click(mx, my)
        elif self.tab == TAB_EQUIP:
            return self._handle_equip_click(mx, my)
        elif self.tab == TAB_IDENTIFY:
            return self._handle_identify_click(mx, my)
        elif self.tab == TAB_TRANSFER:
            return self._handle_transfer_click(mx, my)

        return None

    def handle_key(self, key):
        """Handle keyboard input."""
        if key == pygame.K_ESCAPE:
            self.finished = True
            self.result = "cancel"
            return "cancel"
        if key == pygame.K_TAB:
            self.tab = (self.tab + 1) % TAB_COUNT
            return None
        # Arrow keys for char selection
        if key == pygame.K_LEFT and self.selected_char > 0:
            self.selected_char -= 1
        elif key == pygame.K_RIGHT and self.selected_char < len(self.party) - 1:
            self.selected_char += 1
        return None

    def _handle_rest_click(self, mx, my):
        from core.classes import get_all_resources
        # Rest button position
        top = 80
        cy = top + 90 + len(self.party) * 40
        rest_btn = pygame.Rect(SCREEN_W // 2 - 80, cy + 20, 160, 45)
        if rest_btn.collidepoint(mx, my):
            self.finished = True
            self.result = "rest"
            return "rest"
        return None

    def _handle_inventory_click(self, mx, my):
        c = self.party[self.selected_char]
        top = 80
        iy = top + 45

        # Item list clicks
        visible = c.inventory[self.scroll_offset:self.scroll_offset + 12]
        for i in range(len(visible)):
            idx = self.scroll_offset + i
            row = pygame.Rect(60, iy + i * 38, SCREEN_W - 120, 34)
            if row.collidepoint(mx, my):
                self.selected_item = idx
                return None

        # Action buttons
        if 0 <= self.selected_item < len(c.inventory):
            item = c.inventory[self.selected_item]
            by = iy + min(len(visible), 12) * 38 + 10

            if item.get("type") in ("consumable", "potion", "food"):
                use_btn = pygame.Rect(80, by, 120, 34)
                if use_btn.collidepoint(mx, my):
                    self._use_item(c, self.selected_item)
                    return None

            if item.get("slot"):
                equip_btn = pygame.Rect(210, by, 120, 34)
                if equip_btn.collidepoint(mx, my):
                    self._equip_item(c, self.selected_item)
                    return None

            drop_btn = pygame.Rect(340, by, 120, 34)
            if drop_btn.collidepoint(mx, my):
                name = item.get("name", "item")
                c.inventory.pop(self.selected_item)
                self.selected_item = -1
                self._msg(f"Dropped {name}.", ORANGE)
                return None

        return None

    def _handle_equip_click(self, mx, my):
        c = self.party[self.selected_char]
        equipment = c.equipment if hasattr(c, "equipment") and c.equipment else {}
        top = 80

        # Unequip slot clicks
        ey = top + 45
        for slot in EQUIP_SLOTS:
            row = pygame.Rect(60, ey, SCREEN_W - 120, 38)
            if row.collidepoint(mx, my) and equipment.get(slot):
                # Unequip
                item = equipment.pop(slot)
                c.inventory.append(item)
                self._msg(f"Unequipped {item.get('name', 'item')}.", DIM_GOLD)
                return None
            ey += 42

        # Equippable inventory items
        ey += 30
        for i, item in enumerate(c.inventory):
            if not item.get("slot"):
                continue
            row = pygame.Rect(80, ey, SCREEN_W - 160, 32)
            if row.collidepoint(mx, my):
                self._equip_item(c, i)
                return None
            ey += 36
            if ey > SCREEN_H - 60:
                break

        return None

    def _handle_identify_click(self, mx, my):
        from core.identification import needs_identification, get_identify_options, attempt_identify

        identifiers = []
        for i, c in enumerate(self.party):
            combatant = self._char_to_combatant(c)
            opts = get_identify_options(combatant)
            if opts:
                identifiers.append((i, c, opts))

        if not identifiers:
            return None

        # Click on unidentified items
        unid_items = []
        for ci, c in enumerate(self.party):
            for ii, item in enumerate(c.inventory):
                if needs_identification(item):
                    unid_items.append((ci, ii, item, c))

        top = 80
        uy = top + 55
        for ui_idx, (ci, ii, item, char) in enumerate(unid_items[:8]):
            row = pygame.Rect(60, uy + ui_idx * 40, SCREEN_W - 120, 36)
            if row.collidepoint(mx, my):
                # Use first available identifier
                id_idx, id_char, id_opts = identifiers[0]
                combatant = self._char_to_combatant(id_char)
                # Use first available option
                opt = id_opts[0]
                results, success = attempt_identify(combatant, item, opt["action"])
                # Sync resources back
                for rk, rv in combatant["resources"].items():
                    id_char.resources[rk] = rv
                if success:
                    item["identified"] = True
                    from core.identification import get_item_display_name
                    name = get_item_display_name(item)
                    self._msg(f"Identified: {name}!", HEAL_COL)
                else:
                    msg = results[0][2] if results else "Failed to identify."
                    self._msg(msg, ORANGE)
                return None

        return None

    # ──────────────────────────────────────────────────────────
    #  ITEM ACTIONS
    # ──────────────────────────────────────────────────────────

    def _use_item(self, char, item_idx):
        """Use a consumable item."""
        from core.classes import get_all_resources
        item = char.inventory[item_idx]
        name = item.get("name", "item")

        # Scroll of Remove Curse
        if item.get("effect") == "remove_curse" or item.get("name") == "Scroll of Remove Curse":
            from core.equipment import unequip_item as _ueq
            cursed_slots = [
                slot for slot, eq in (char.equipment or {}).items()
                if eq and eq.get("cursed") and not eq.get("curse_lifted")
            ]
            from core.status_effects import get_status_effects
            curse_effects = [s for s in get_status_effects(char) if s.get("type") == "curse"]
            if not cursed_slots and not curse_effects:
                self._msg(f"{char.name} is not cursed.", ORANGE)
                return
            for slot in cursed_slots:
                eq = char.equipment[slot]
                eq["curse_lifted"] = True
                char.equipment[slot] = None
                char.inventory.append(eq)
            for se in curse_effects:
                if se in char.status_effects:
                    char.status_effects.remove(se)
            self._msg(f"{char.name}'s curses have been lifted!", HEAL_COL)
            # Consume scroll
            stack = item.get("stack", 1)
            if stack > 1:
                item["stack"] = stack - 1
            else:
                char.inventory.pop(item_idx)
                self.selected_item = -1
            return

        # Scroll of Identify
        if item.get("subtype") == "scroll" and (
            item.get("name") == "Scroll of Identify" or item.get("effect") == "identify"
        ):
            from core.identification import attempt_identify
            from core.party_knowledge import mark_item_identified
            # Find first unidentified item across party
            for member in [char] + [m for m in self.party if m is not char]:
                for i, inv_item in enumerate(member.inventory):
                    if not inv_item.get("identified"):
                        inv_item["identified"] = True
                        inv_item["magic_identified"] = True
                        inv_item["material_identified"] = True
                        mark_item_identified(inv_item.get("name", ""))
                        self._msg(
                            f"Scroll identifies: {inv_item.get('name', 'item')} "
                            f"(in {member.name}'s pack)",
                            HEAL_COL
                        )
                        # Consume scroll
                        stack = item.get("stack", 1)
                        if stack > 1:
                            item["stack"] = stack - 1
                        else:
                            char.inventory.pop(item_idx)
                            self.selected_item = -1
                        return
            self._msg("No unidentified items to identify.", ORANGE)
            return

        # Healing items
        heal = item.get("heal", 0)
        if heal > 0:
            max_res = get_all_resources(char.class_name, char.stats, char.level)
            max_hp = max_res.get("HP", 1)
            old = char.resources.get("HP", 0)
            char.resources["HP"] = min(max_hp, old + heal)
            actual = char.resources["HP"] - old
            self._msg(f"{char.name} used {name}: +{actual} HP", HEAL_COL)
        elif item.get("restore_mp"):
            for rk in char.resources:
                if "MP" in rk:
                    max_res = get_all_resources(char.class_name, char.stats, char.level)
                    max_val = max_res.get(rk, 0)
                    old = char.resources[rk]
                    char.resources[rk] = min(max_val, old + item["restore_mp"])
                    self._msg(f"{char.name} used {name}: +{char.resources[rk] - old} {rk}", MP_BAR)
                    break
        else:
            self._msg(f"Can't use {name} here.", ORANGE)
            return

        # Consume
        stack = item.get("stack", 1)
        if stack > 1:
            item["stack"] = stack - 1
        else:
            char.inventory.pop(item_idx)
            self.selected_item = -1

    def _equip_item(self, char, item_idx):
        """Equip an item from inventory."""
        item = char.inventory[item_idx]
        slot = item.get("slot")
        if not slot:
            return

        if not hasattr(char, "equipment") or char.equipment is None:
            char.equipment = {}

        # Unequip current
        old = char.equipment.get(slot)
        if old:
            char.inventory.append(old)

        # Equip new
        char.equipment[slot] = item
        char.inventory.pop(item_idx)
        self.selected_item = -1

        name = item.get("name", "item")
        self._msg(f"{char.name} equipped {name}.", GOLD)
