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
TAB_FORMATION = 6
TAB_SPELLS    = 7
TAB_NAMES = ["Rest", "Inventory", "Equipment", "Identify", "Party", "Transfer", "Formation", "Spells"]
TAB_COUNT = len(TAB_NAMES)

# ── Slots ──
# Import from equipment.py — single source of truth
from core.equipment import SLOT_ORDER as EQUIP_SLOTS, SLOT_NAMES as SLOT_LABELS


# ── Inventory stacking helper ─────────────────────────────────────────────
def _build_inv_groups(inventory):
    """Collapse inventory into display groups for stacked rendering.

    Returns list of dicts:
      {"name": str, "count": int, "indices": [int,...], "item": dict}

    Weapons/armor with enchant/bonus/unique fields never stack.
    Key items never stack. Everything else groups by (name, type, subtype).
    """
    groups = []
    group_map = {}
    for idx, item in enumerate(inventory):
        itype = item.get("type", "")
        if itype in ("key_item", "quest_item") or "warden_rank" in item:
            groups.append({"name": item.get("name","?"), "count": 1,
                           "indices": [idx], "item": item})
            continue
        if itype in ("weapon", "armor", "accessory"):
            if (item.get("enchant_element") or item.get("enchant_bonus") or
                    item.get("bonus") or item.get("unique") or
                    item.get("enchant_name")):
                groups.append({"name": item.get("name","?"), "count": 1,
                               "indices": [idx], "item": item})
                continue
        key = (item.get("name",""), itype, item.get("subtype",""))
        if key in group_map:
            gi = group_map[key]
            groups[gi]["count"] += 1
            groups[gi]["indices"].append(idx)
        else:
            group_map[key] = len(groups)
            groups.append({"name": item.get("name","?"), "count": 1,
                           "indices": [idx], "item": item})
    return groups


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
        self._stats_scroll = 0
        self._give_mode    = False
        self._equip_slot_rects    = []
        self._equip_tab_inv_rects = []
        self._inv_btn_rects       = {}
        self._stats_inv_rects     = []
        self._stats_inv_sel       = -1
        self._stats_spell_sel     = -1
        self._manual_open  = False
        self._manual_page  = 0
        self._manual_scroll = 0
        self._manual_tabs  = []
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

        # Spells tab state
        self.spell_selected = -1      # index of selected spell
        self.spell_target = 0         # index of target character

        # Formation state
        self.formation_selected = -1   # index of char being dragged/moved

    def draw(self, surface, mx, my, dt=16):
        surface.fill(CAMP_BG)

        # Guard: if party is empty or selected_char is out of range, clamp it
        if not self.party:
            draw_text(surface, "No party members.", SCREEN_W // 2 - 80, SCREEN_H // 2, GREY, 16)
            return
        self.selected_char = max(0, min(self.selected_char, len(self.party) - 1))

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
        elif self.tab == TAB_FORMATION:
            self._draw_formation(surface, mx, my, content_y)
        elif self.tab == TAB_SPELLS:
            self._draw_spells(surface, mx, my, content_y)

        # Manual button (bottom-left corner so it doesn't clash with "Break Camp")
        _mb = pygame.Rect(20, SCREEN_H - 48, 130, 34)
        _mhov = _mb.collidepoint(mx, my)
        pygame.draw.rect(surface, (30,25,50) if not _mhov else (50,40,70), _mb, border_radius=5)
        pygame.draw.rect(surface, GOLD if _mhov else (80,70,100), _mb, 1, border_radius=5)
        draw_text(surface, "◈ Manual  [M]", _mb.x + 8, _mb.y + 9,
                  GOLD if _mhov else CREAM, 12)
        self._manual_btn_rect = _mb

        # Manual overlay (drawn on top of everything)
        self._draw_manual(surface, mx, my)

        # Message bar
        if self.msg_timer > 0:
            self.msg_timer -= dt
            # Message bar drawn above manual button (manual is at y=SCREEN_H-48=852)
            msg_bg = pygame.Rect(SCREEN_W//2 - 220, SCREEN_H - 62, 440, 22)
            pygame.draw.rect(surface, (18, 14, 28), msg_bg, border_radius=3)
            draw_text(surface, self.message, SCREEN_W // 2 - 200, SCREEN_H - 60,
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
                      CREAM, 13, bold=True, max_width=232)

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
        # Reserve 320px at bottom for action buttons + item detail + compare panel
        BODY_BOT   = SCREEN_H - 320   # 580 at 900px screen
        ROW_H      = 36
        LIST_X     = 60
        SB_W       = 10           # scrollbar width
        ROW_W      = SCREEN_W - LIST_X - 26  # leave room for scrollbar
        list_top   = top + 52
        list_bot   = BODY_BOT          # list ends here; buttons + detail go below
        visible_n  = max(1, (list_bot - list_top) // ROW_H)

        iy = list_top

        if not c.inventory:
            draw_text(surface, "No items.", LIST_X, iy, GREY, 14)
            return

        # Build collapsed groups — identical stackable items share one row
        groups = _build_inv_groups(c.inventory)
        # Store groups for click handler
        self._inv_groups = groups
        total = len(groups)
        # Clamp scroll offset so we never scroll past the last group
        max_off = max(0, total - visible_n)
        self.scroll_offset = max(0, min(self.scroll_offset, max_off))

        visible_groups = groups[self.scroll_offset:self.scroll_offset + visible_n]
        for gi, grp in enumerate(visible_groups):
            g_idx = self.scroll_offset + gi   # index into groups list
            item  = grp["item"]
            row = pygame.Rect(LIST_X, iy, ROW_W, ROW_H - 2)
            hover = row.collidepoint(mx, my)
            bg = ITEM_HOVER if hover else ITEM_BG
            pygame.draw.rect(surface, bg, row, border_radius=3)
            # Highlight if selected_item points to any index in this group
            if self.selected_item in grp["indices"]:
                pygame.draw.rect(surface, GOLD, row, 2, border_radius=3)

            from core.identification import get_item_display_name
            name = get_item_display_name(item)
            count = grp["count"]
            count_str = f" ×{count}" if count > 1 else ""
            draw_text(surface, f"{name}{count_str}", row.x + 10, row.y + 7, CREAM, 13)

            itype = item.get("type", "misc")
            draw_text(surface, itype, row.x + ROW_W - 80, row.y + 7, STAT_LABEL, 11)
            iy += ROW_H

        # ── Scrollbar ──────────────────────────────────────────
        if total > visible_n:
            sb_x    = LIST_X + ROW_W + 4
            sb_top  = list_top
            sb_h    = iy - list_top   # height of rendered list area
            # Rail
            pygame.draw.rect(surface, (30, 25, 40),
                             (sb_x, sb_top, SB_W, list_bot - list_top), border_radius=4)
            # Thumb
            thumb_h = max(18, int((list_bot - list_top) * visible_n / total))
            thumb_y = sb_top + int((list_bot - list_top - thumb_h) *
                                   self.scroll_offset / max(1, max_off))
            pygame.draw.rect(surface, (100, 80, 140),
                             (sb_x, thumb_y, SB_W, thumb_h), border_radius=4)
            # Scroll hint
            draw_text(surface, f"{self.scroll_offset+1}-"
                      f"{min(total, self.scroll_offset+visible_n)}/{total}",
                      sb_x - 30, list_bot - list_top + list_top + 2, GREY, 10)

        # Item action buttons if something selected
        # Store rects on self so _handle_inventory_click uses exact draw-time positions
        self._inv_btn_rects = {}
        self._inv_btn_by    = -1
        if 0 <= self.selected_item < len(c.inventory):
            item = c.inventory[self.selected_item]
            # Retroactively patch slot for items saved before the slot-fix (old saves)
            if not item.get("slot") and item.get("type") in ("weapon", "armor", "accessory"):
                try:
                    from core.item_slot_fixer import ensure_slot
                    ensure_slot(item)
                except Exception:
                    pass
            by = iy + 10
            self._inv_btn_by = by
            protected = item.get("type") in ("key_item", "quest_item") or "warden_rank" in item

            if item.get("type") in ("consumable", "potion", "food"):
                use_btn = pygame.Rect(80, by, 100, 34)
                self._inv_btn_rects["use"] = use_btn
                draw_button(surface, use_btn, "Use", hover=use_btn.collidepoint(mx, my), size=13)

            if item.get("slot"):
                equip_btn = pygame.Rect(190, by, 100, 34)
                self._inv_btn_rects["equip"] = equip_btn
                draw_button(surface, equip_btn, "Equip",
                            hover=equip_btn.collidepoint(mx, my), size=13)

            # Drop — dimmed and disabled for protected items
            drop_btn = pygame.Rect(300, by, 100, 34)
            self._inv_btn_rects["drop"] = drop_btn
            if protected:
                draw_button(surface, drop_btn, "Drop [key]",
                            hover=False, size=11)  # always un-hovered = dimmed
            else:
                draw_button(surface, drop_btn, "Drop", hover=drop_btn.collidepoint(mx, my), size=13)

            # Give button
            if len(self.party) > 1:
                give_btn = pygame.Rect(410, by, 100, 34)
                self._inv_btn_rects["give"] = give_btn
                draw_button(surface, give_btn, "Give", hover=give_btn.collidepoint(mx, my), size=13)
                if getattr(self, "_give_mode", False):
                    gx = 80
                    for gi, gchar in enumerate(self.party):
                        if gi == self.selected_char:
                            continue
                        gb = pygame.Rect(gx, by + 44, max(80, len(gchar.name)*8+16), 28)
                        self._inv_btn_rects[f"give_{gi}"] = gb
                        draw_button(surface, gb, gchar.name,
                                    hover=gb.collidepoint(mx, my), size=12)
                        gx += gb.width + 8

            # ── Item details + compare panel (side by side, always on screen) ──
            detail_offset = 84 if getattr(self,"_give_mode",False) and len(self.party)>1 else 50
            panel_top  = min(by + detail_offset, SCREEN_H - 20)
            avail_h    = max(20, SCREEN_H - panel_top - 8)   # space down to bottom

            has_slot   = bool(item.get("slot"))
            if has_slot:
                # Detail panel: up to 200px — enough for any item (densest ~130px).
                # Never artificially capped below what content needs.
                detail_h   = min(avail_h, 200)
                detail_ph  = self._draw_item_details(surface, item, panel_top,
                                                     max_h=detail_h)
                # Compare panel: placed immediately below, self-clamps to screen bottom
                cmp_top = panel_top + detail_ph + 6
                if cmp_top < SCREEN_H - 40:
                    self._draw_equip_compare(surface, item, 80, cmp_top,
                                             SCREEN_W - 160)
            else:
                self._draw_item_details(surface, item, panel_top, max_h=avail_h)

    def _draw_item_details(self, surface, item, y, max_h=None):
        """Draw item attribute panel. max_h caps the panel height (default uncapped)."""
        from core.identification import get_item_display_name
        if not item:
            return 0

        identified = item.get("identified", True)
        avail = max_h if max_h else (SCREEN_H - y - 8)
        avail = max(40, avail)
        pw = SCREEN_W - 160

        # Collect lines first so we can size the panel
        lines = []   # (text, colour, size, bold)
        lines.append((get_item_display_name(item), GOLD, 14, True))

        if not identified:
            lines.append((item.get("unidentified_desc", "Properties unknown."), GREY, 12, False))
            lines.append(("[Unidentified — use Identify tab to appraise]", ORANGE, 11, False))
        else:
            desc = item.get("description", "")
            if desc:
                lines.append((desc, GREY, 12, False))

            itype = item.get("type", "")
            if itype == "weapon":
                base = item.get("damage", 0)
                ds   = item.get("damage_stat", {})
                ds_str = ", ".join(f"{k}×{v}" for k,v in ds.items()) if ds else "none"
                lines.append((f"Damage: {base}  |  Scaling: {ds_str}", STAT_VAL, 12, False))
                mods = []
                if item.get("accuracy_mod"): mods.append(f"Acc {item['accuracy_mod']:+d}%")
                if item.get("crit_mod"):     mods.append(f"Crit {item['crit_mod']:+d}%")
                if item.get("speed_mod"):    mods.append(f"Speed {item['speed_mod']:+d}")
                if item.get("spell_bonus"):  mods.append(f"+{item['spell_bonus']} Spell Power")
                if mods:
                    lines.append(("  ".join(mods), STAT_LABEL, 11, False))
            elif itype == "armor":
                lines.append((f"Defense: {item.get('defense',0)}   Magic Resist: {item.get('magic_resist',0)}",
                               STAT_VAL, 12, False))

            stat_bonuses = item.get("stat_bonuses", {})
            if stat_bonuses:
                bonuses = ",  ".join(f"{k} {v:+d}" for k,v in stat_bonuses.items() if v)
                lines.append((f"Bonuses:  {bonuses}", (140, 220, 160), 12, False))

            if item.get("enchant_element"):
                lines.append((f"Enchant: {item['enchant_element'].title()} +{item.get('enchant_bonus',0)}",
                               (180, 140, 255), 12, False))

            rarity = item.get("rarity", "").title()
            value  = item.get("estimated_value", item.get("sell_price", 0))
            lines.append((f"{rarity}   Value: ~{value}g", DIM_GOLD, 11, False))

        # Measure required height — lh paired with line so no fragile index lookup
        lh = [18 if l[2] >= 13 else 15 for l in lines]
        needed_h = 14 + sum(lh)
        ph = min(needed_h, avail)

        panel = pygame.Rect(80, y, pw, ph)
        pygame.draw.rect(surface, (18, 14, 30), panel, border_radius=5)
        pygame.draw.rect(surface, EQUIP_SLOT_BORDER, panel, 1, border_radius=5)

        dy = panel.y + 8
        for (text, col, size, bold), row_h in zip(lines, lh):
            if dy + size + 2 > panel.bottom - 4:
                break
            draw_text(surface, text, panel.x + 14, dy, col, size, bold=bold,
                      max_width=pw - 28)
            dy += row_h

        return ph   # return actual drawn height

    def _draw_equip_compare(self, surface, new_item, px, py, pw):
        """Side-by-side comparison panel: equipped vs new item.

        Dynamically sizes to fit stat rows; always clamped so it stays on screen.
        Layout: EQUIPPED (left half)  ↔  NEW (right half), delta highlighted.
        """
        from core.identification import get_item_display_name
        if not self.party or self.selected_char >= len(self.party):
            return
        c     = self.party[self.selected_char]
        equip = getattr(c, "equipment", {}) or {}
        slot  = new_item.get("slot")
        if not slot:
            return
        cur = equip.get(slot)

        # Build stat rows before sizing the panel
        stat_rows = []
        for label, ckey, nkey in [
            ("Damage",     "damage",       "damage"),
            ("Defense",    "defense",      "defense"),
            ("Mag.Resist", "magic_resist", "magic_resist"),
            ("Spell Pwr",  "spell_bonus",  "spell_bonus"),
            ("Accuracy",   "accuracy_mod", "accuracy_mod"),
            ("Crit",       "crit_mod",     "crit_mod"),
        ]:
            cv = cur.get(ckey, 0) if cur else 0
            nv = new_item.get(nkey, 0)
            if cv != 0 or nv != 0:
                stat_rows.append((label, cv, nv))

        nb = new_item.get("stat_bonuses", {}) or {}
        cb = cur.get("stat_bonuses", {}) or {} if cur else {}
        for k in sorted(set(nb) | set(cb)):
            cv = cb.get(k, 0); nv = nb.get(k, 0)
            if cv != 0 or nv != 0:
                stat_rows.append((k, cv, nv))

        # Height: header (40) + name row (18) + stat rows (15 each) + verdict (20) + pad
        ROW_H = 15
        if cur:
            needed_h = 40 + 18 + len(stat_rows) * ROW_H + 24
        else:
            needed_h = 40

        # Clamp so panel never goes below screen
        max_y_bottom = SCREEN_H - 8
        if py + needed_h > max_y_bottom:
            py = max(4, max_y_bottom - needed_h)
        ph = min(needed_h, max_y_bottom - py)

        panel = pygame.Rect(px, py, pw, ph)
        pygame.draw.rect(surface, (8, 14, 26), panel, border_radius=5)
        pygame.draw.rect(surface, (55, 90, 150), panel, 1, border_radius=5)

        cy = panel.y + 6
        # Column widths: label | equipped | arrow | new | delta
        lbl_w = 80; eq_w = pw // 3; new_w = pw // 3
        lx_lbl = panel.x + 10
        lx_eq  = lx_lbl + lbl_w
        lx_arr = lx_eq + eq_w
        lx_new = lx_arr + 18
        lx_del = lx_new + new_w

        # Header
        slot_label = slot.replace("_", " ").title()
        draw_text(surface, f"COMPARE  ·  Slot: {slot_label}",
                  lx_lbl, cy, (80, 120, 200), 11, bold=True)
        cy += 16
        pygame.draw.line(surface, (50, 80, 130),
                         (panel.x + 6, cy), (panel.x + pw - 6, cy))
        cy += 4

        if not cur:
            draw_text(surface, "Nothing equipped — equipping is a pure gain",
                      lx_lbl, cy, (80, 210, 100), 12)
            return

        # Name row — truncated to fit columns
        max_name = (eq_w - 4) // 6  # approx chars at size 10
        cur_name = get_item_display_name(cur)[:max_name]
        new_name = get_item_display_name(new_item)[:max_name]
        draw_text(surface, "EQUIPPED", lx_eq, cy, (130, 110, 80), 9, bold=True)
        draw_text(surface, "NEW",      lx_new, cy, (80, 150, 220), 9, bold=True)
        cy += 13

        # Column header divider
        pygame.draw.line(surface, (40, 60, 100),
                         (panel.x + 6, cy), (panel.x + pw - 6, cy))
        cy += 3

        # Truncated item names
        draw_text(surface, cur_name, lx_eq, cy, (180, 155, 110), 10)
        draw_text(surface, new_name, lx_new, cy, (100, 180, 240), 10)
        cy += 14

        # Stat comparison rows
        for label, cv, nv in stat_rows:
            if cy + ROW_H > panel.bottom - 22:
                draw_text(surface, "…", lx_lbl, cy, GREY, 10)
                break
            delta = nv - cv
            d_col = (80, 210, 100) if delta > 0 else (210, 80, 80) if delta < 0 else GREY
            d_str = (f"+{delta}" if delta > 0 else str(delta)) if delta != 0 else "="

            draw_text(surface, f"{label}:", lx_lbl, cy, STAT_LABEL, 10)
            draw_text(surface, str(cv) if cv != 0 else "—", lx_eq,  cy, GREY, 10)
            draw_text(surface, "→", lx_arr, cy, (70, 80, 100), 10)
            draw_text(surface, str(nv) if nv != 0 else "—", lx_new, cy,
                      d_col if delta != 0 else CREAM, 10, bold=(delta != 0))
            if delta != 0:
                draw_text(surface, d_str, lx_del, cy, d_col, 10, bold=True)
            cy += ROW_H

        # Verdict bar
        improvements = sum(1 for _, cv, nv in stat_rows if nv > cv)
        regressions  = sum(1 for _, cv, nv in stat_rows if nv < cv)
        if improvements > regressions:
            verdict, vc = "▲ Upgrade",    (80, 210, 100)
        elif regressions > improvements:
            verdict, vc = "▼ Downgrade",  (210, 80,  80)
        else:
            verdict, vc = "◆ Sidegrade",  (220, 200, 80)
        vbar_y = panel.bottom - 18
        pygame.draw.line(surface, (50, 80, 130),
                         (panel.x + 6, vbar_y - 2),
                         (panel.x + pw - 6, vbar_y - 2))
        draw_text(surface, verdict, panel.x + 10, vbar_y, vc, 11, bold=True)

    # ──────────────────────────────────────────────────────────
    #  EQUIPMENT TAB
    # ──────────────────────────────────────────────────────────

    def _draw_equipment(self, surface, mx, my, top):
        self._draw_char_selector(surface, mx, my, top)
        c = self.party[self.selected_char]
        equipment = c.equipment if hasattr(c, "equipment") and c.equipment else {}

        ey = top + 52
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
                if hover:
                    draw_text(surface, "[Click to unequip]", row.x + row.width - 150,
                              row.y + 8, DIM_GOLD, 11)
                    # Show stat details for equipped item on hover
                    detail_y = min(row.bottom + 4, SCREEN_H - 200)
                    avail = SCREEN_H - detail_y - 8
                    self._draw_item_details(surface, equipped, detail_y, max_h=avail)
            else:
                draw_text(surface, "— empty —", row.x + 120, row.y + 8, DARK_GREY, 13)

            ey += 42

        # Show equippable items from inventory
        draw_text(surface, "Equippable items in inventory:", 60, ey + 10, DIM_GOLD, 13)
        ey += 30
        self._equip_tab_inv_rects = []   # [(true_inventory_idx, rect)]
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
                # Show stat details + compare panel on hover — stack within screen
                detail_y = min(row.bottom + 4, SCREEN_H - 8)
                avail = SCREEN_H - detail_y - 8
                detail_ph = self._draw_item_details(surface, item, detail_y,
                                                    max_h=min(avail, 200))
                if item.get("slot") and detail_y + detail_ph + 6 < SCREEN_H - 40:
                    self._draw_equip_compare(surface, item, 80,
                                             detail_y + detail_ph + 6, SCREEN_W - 160)
            self._equip_tab_inv_rects.append((i, row))
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


    # ────────────────────────────────────────────────────────────────────────
    #  PARTY STATS TAB  (complete rewrite)
    # ────────────────────────────────────────────────────────────────────────

    def _draw_stats(self, surface, mx, my, top):
        """Rich party stats panel: tier badge, effective stats, resistances,
        known abilities/spells with scrollable descriptions."""
        # Guard: clamp selected_char to valid range
        if not self.party:
            draw_text(surface, "No party members.", 80, top + 60, GREY, 14)
            return
        self.selected_char = max(0, min(self.selected_char, len(self.party) - 1))

        self._draw_char_selector(surface, mx, my, top)
        c = self.party[self.selected_char]

        from core.classes import get_all_resources, STAT_NAMES
        from core.progression import PLANAR_TIERS, get_party_tier

        # ── Layout constants ───────────────────────────────────────────────
        LEFT_X   = 30
        MID_X    = 430
        RIGHT_X  = 850
        BODY_TOP = top + 60        # below char selector
        BODY_BOT = SCREEN_H - 60  # leave room for Manual button
        CONTENT_H = BODY_BOT - BODY_TOP

        # ── Clipping region for scroll ─────────────────────────────────────
        clip = pygame.Rect(0, BODY_TOP, SCREEN_W, CONTENT_H)
        surface.set_clip(clip)

        # ─────────────────────────────────────────────────────────────────
        #  LEFT COLUMN: Tier badge + Base stats + Resources + Resistances
        # ─────────────────────────────────────────────────────────────────
        y = BODY_TOP + 4

        # ── HP / Resources summary bar (always visible at top) ───────────
        hp_bar_y = y
        try:
            max_res_top = get_all_resources(c.class_name, c.stats, c.level)
            mhp = max(1, max_res_top.get("HP", 1))
            chp = c.resources.get("HP", mhp)
            hp_pct = max(0.0, chp / mhp)
            hp_col = (60,200,80) if hp_pct > 0.5 else (220,160,40) if hp_pct > 0.25 else (220,60,60)
            # HP label
            draw_text(surface, "HP", LEFT_X, y, STAT_LABEL, 11, bold=True)
            draw_text(surface, f"{chp} / {mhp}", LEFT_X + 28, y, hp_col, 13, bold=True)
            # HP bar
            bar_r = pygame.Rect(LEFT_X + 110, y + 3, 220, 10)
            pygame.draw.rect(surface, (40, 20, 20), bar_r, border_radius=3)
            fill_w = int(220 * hp_pct)
            if fill_w > 0:
                pygame.draw.rect(surface, hp_col,
                                 pygame.Rect(bar_r.x, bar_r.y, fill_w, 10), border_radius=3)
            # Other resources inline
            rx = LEFT_X + 340
            for rname, mval in max_res_top.items():
                if rname == "HP": continue
                cval = c.resources.get(rname, 0)
                fc = MP_BAR if "MP" in rname else SP_BAR
                draw_text(surface, f"{rname}: {cval}/{mval}", rx, y, GREY, 10)
                rx += 110
                if rx > SCREEN_W - 60:
                    break
            y += 20
            pygame.draw.line(surface, (60, 50, 80), (LEFT_X, y), (LEFT_X + 380, y))
            y += 8
        except Exception:
            pass

        # ── Tier badge ─────────────────────────────────────────────────────
        try:
            from core.story_flags import _flags as _sf
            party_flags = dict(_sf)
        except Exception:
            party_flags = {}
        min_lvl = min(ch.level for ch in self.party) if self.party else 1
        tier_idx = get_party_tier(party_flags, min_lvl)
        tier_data = PLANAR_TIERS.get(tier_idx, PLANAR_TIERS[0])
        tier_name  = tier_data["name"]
        tier_color = tier_data["color"]
        tier_sym   = tier_data.get("symbol", "◆")
        tier_desc  = tier_data.get("description", "")

        badge_rect = pygame.Rect(LEFT_X, y, 380, 52)
        pygame.draw.rect(surface, (20, 15, 35), badge_rect, border_radius=6)
        pygame.draw.rect(surface, tier_color, badge_rect, 2, border_radius=6)
        draw_text(surface, f"{tier_sym}  WARDEN RANK", LEFT_X + 10, y + 6, tier_color, 10, bold=True)
        draw_text(surface, tier_name, LEFT_X + 10, y + 20, tier_color, 18, bold=True)
        draw_text(surface, tier_desc, LEFT_X + 10, y + 40, GREY, 10, max_width=370)
        y += 66

        # Tier bonuses
        bonuses = tier_data.get("bonus", {})
        if bonuses:
            bonus_parts = []
            if bonuses.get("all_stats"): bonus_parts.append(f"+{bonuses['all_stats']} all stats")
            if bonuses.get("max_hp_pct"): bonus_parts.append(f"+{int(bonuses['max_hp_pct']*100)}% HP")
            if bonuses.get("damage_mult") and bonuses["damage_mult"] > 1:
                bonus_parts.append(f"+{int((bonuses['damage_mult']-1)*100)}% dmg")
            if bonuses.get("xp_mult") and bonuses["xp_mult"] > 1:
                bonus_parts.append(f"+{int((bonuses['xp_mult']-1)*100)}% XP")
            if bonus_parts:
                draw_text(surface, "Bonuses: " + "  •  ".join(bonus_parts),
                          LEFT_X, y, tier_color, 11)
                y += 18
        y += 6

        # ── Character name / class / race / level ──────────────────────────
        draw_text(surface, c.name, LEFT_X, y, GOLD, 18, bold=True)
        y += 22
        draw_text(surface, f"Level {c.level} {c.race_name} {c.class_name}",
                  LEFT_X, y, CREAM, 13, max_width=390)
        y += 16
        # XP progress
        from core.progression import xp_for_level
        xp_this = xp_for_level(c.level)
        xp_next = xp_for_level(c.level + 1)
        xp_pct = min(1.0, (c.xp - xp_this) / max(1, xp_next - xp_this))
        draw_text(surface, f"XP: {c.xp:,}", LEFT_X, y, DIM_GOLD, 11)
        bar = pygame.Rect(LEFT_X + 80, y + 2, 200, 8)
        pygame.draw.rect(surface, (30,25,45), bar, border_radius=3)
        fill = pygame.Rect(bar.x, bar.y, int(bar.width * xp_pct), bar.height)
        pygame.draw.rect(surface, DIM_GOLD, fill, border_radius=3)
        if c.level < 30:
            draw_text(surface, f"→ L{c.level+1}", LEFT_X + 288, y, GREY, 10)
        y += 22

        # ── Stats ──────────────────────────────────────────────────────────
        pygame.draw.line(surface, (60,50,80), (LEFT_X, y), (LEFT_X+380, y))
        y += 6
        draw_text(surface, "ATTRIBUTES", LEFT_X, y, STAT_LABEL, 10, bold=True)
        y += 14

        base_stats = dict(c.stats)
        eff_stats  = c.effective_stats() if hasattr(c, "effective_stats") else base_stats

        stat_col_w = 90
        FULL_NAMES = {"STR":"Strength","DEX":"Dexterity","CON":"Constitution",
                      "INT":"Intelligence","WIS":"Wisdom","PIE":"Piety"}
        for idx_s, stat in enumerate(STAT_NAMES):
            sx = LEFT_X + (idx_s % 2) * 195
            sy = y + (idx_s // 2) * 20
            base = base_stats.get(stat, 0)
            eff  = eff_stats.get(stat, base)
            col  = (100, 200, 120) if eff > base else RED if eff < base else STAT_VAL
            full = FULL_NAMES.get(stat, stat)
            draw_text(surface, f"{full[:3]}:", sx, sy, STAT_LABEL, 12)
            draw_text(surface, str(eff), sx + 36, sy, col, 12, bold=True)
            if eff != base:
                diff = eff - base
                sign = "+" if diff > 0 else ""
                draw_text(surface, f"({sign}{diff})", sx + 60, sy, col, 10)
        y += (len(STAT_NAMES) // 2 + 1) * 20 + 6

        # ── Resources ─────────────────────────────────────────────────────
        pygame.draw.line(surface, (60,50,80), (LEFT_X, y), (LEFT_X+380, y))
        y += 6
        draw_text(surface, "RESOURCES", LEFT_X, y, STAT_LABEL, 10, bold=True)
        y += 14
        max_res = get_all_resources(c.class_name, eff_stats, c.level)
        for rname, mval in max_res.items():
            cval = c.resources.get(rname, 0)
            pct  = cval / mval if mval > 0 else 0
            draw_text(surface, f"{rname}:", LEFT_X, y, STAT_LABEL, 12)
            bar2 = pygame.Rect(LEFT_X + 70, y + 3, 200, 10)
            pygame.draw.rect(surface, HP_BAR_BG, bar2, border_radius=2)
            fc = HP_BAR if rname == "HP" else MP_BAR if "MP" in rname else SP_BAR
            fill2 = pygame.Rect(bar2.x, bar2.y, int(bar2.width * pct), bar2.height)
            pygame.draw.rect(surface, fc, fill2, border_radius=2)
            draw_text(surface, f"{cval}/{mval}", LEFT_X + 278, y, GREY, 11)
            y += 18
        y += 4

        # ── Combat Stats (Defense / Magic Resist / Speed) ─────────────────
        pygame.draw.line(surface, (60,50,80), (LEFT_X, y), (LEFT_X+380, y))
        y += 6
        draw_text(surface, "COMBAT STATS", LEFT_X, y, STAT_LABEL, 10, bold=True)
        y += 14
        try:
            from core.equipment import calc_equipment_defense, calc_equipment_magic_resist
            from core.combat_config import DEF_CON_MULT
            equip_def = calc_equipment_defense(c)
            con_def   = int(eff_stats.get("CON", 0) * DEF_CON_MULT)
            total_def = con_def + equip_def
            equip_mr  = calc_equipment_magic_resist(c)
            base_mr   = int(eff_stats.get("WIS", 0) * 2)
            total_mr  = base_mr + equip_mr
            draw_text(surface, "Defense:", LEFT_X, y, STAT_LABEL, 12)
            draw_text(surface, str(total_def), LEFT_X + 65, y, STAT_VAL, 12, bold=True)
            draw_text(surface, f"({con_def} CON + {equip_def} gear)", LEFT_X + 90, y, GREY, 10)
            y += 18
            draw_text(surface, "Mag Resist:", LEFT_X, y, STAT_LABEL, 12)
            draw_text(surface, str(total_mr), LEFT_X + 65, y, STAT_VAL, 12, bold=True)
            draw_text(surface, f"({base_mr} WIS + {equip_mr} gear)", LEFT_X + 90, y, GREY, 10)
            y += 18
        except Exception:
            pass
        y += 4

        # ── Resistances ───────────────────────────────────────────────────
        pygame.draw.line(surface, (60,50,80), (LEFT_X, y), (LEFT_X+380, y))
        y += 6
        draw_text(surface, "RESISTANCES", LEFT_X, y, STAT_LABEL, 10, bold=True)
        y += 14
        # Calculate resistances from equipment
        res = {}
        if hasattr(c, "equipment") and c.equipment:
            for slot, item in c.equipment.items():
                if not item: continue
                for rtype, rval in item.get("resistances", {}).items():
                    res[rtype] = res.get(rtype, 0) + rval
        # Base magic resist
        base_mr = eff_stats.get("WIS", 0) * 2
        race_rs = {}
        try:
            from core.races import RACES
            race_data = RACES.get(c.race_name, {})
            race_rs = race_data.get("resistances", {})
        except Exception:
            pass

        RES_NAMES = [("fire","Fire"),("ice","Ice"),("lightning","Ltng"),
                     ("shadow","Shad"),("divine","Divn"),("nature","Natr"),("arcane","Arcn")]
        for idx_r, (rk, rl) in enumerate(RES_NAMES):
            rx = LEFT_X + (idx_r % 3) * 130
            ry = y + (idx_r // 3) * 18
            val = res.get(rk, 0) + race_rs.get(rk, 0)
            col = (100,200,120) if val > 0 else (200,100,100) if val < 0 else GREY
            sign = "+" if val > 0 else ""
            draw_text(surface, f"{rl}: {sign}{val}%", rx, ry, col, 11)
        y += (len(RES_NAMES)//3 + 1) * 18 + 4

        # ── Status effects ─────────────────────────────────────────────────
        if hasattr(c, "status_effects") and c.status_effects:
            pygame.draw.line(surface, (60,50,80), (LEFT_X, y), (LEFT_X+380, y))
            y += 6
            draw_text(surface, "ACTIVE EFFECTS", LEFT_X, y, STAT_LABEL, 10, bold=True)
            y += 14
            for eff in c.status_effects[:6]:
                ename = eff.get("type") or eff.get("name","?")
                dur   = eff.get("duration", 0)
                draw_text(surface, f"• {ename}" + (f" ({dur}t)" if dur else ""),
                          LEFT_X + 4, y, ORANGE, 11)
                y += 14

        # ─────────────────────────────────────────────────────────────────
        #  MIDDLE COLUMN: Known abilities / spells (scrollable)
        # ─────────────────────────────────────────────────────────────────
        from core.abilities import CLASS_ABILITIES

        # Initialise hit map here so middle column can add camp-castable cards
        self._stats_hit_map = {}   # key -> pygame.Rect

        col_x = MID_X
        col_w = RIGHT_X - MID_X - 20
        ay = BODY_TOP + 4

        draw_text(surface, "ABILITIES & SPELLS", col_x, ay, STAT_LABEL, 10, bold=True)
        ay += 16

        # Gather all abilities this character knows (unlocked by level)
        all_class_abs = CLASS_ABILITIES.get(c.class_name, [])
        known = [ab for ab in all_class_abs if ab.get("level",1) <= c.level]
        locked = [ab for ab in all_class_abs if ab.get("level",1) > c.level]

        scroll_offset = getattr(self, "_stats_scroll", 0)

        TYPE_COLORS = {
            "attack": (220,120,80), "spell": (100,160,255), "heal": (80,220,120),
            "aoe": (220,80,120), "aoe_heal": (80,220,160), "buff": (220,200,80),
            "debuff": (180,120,220), "cure": (100,240,160),
        }

        # Build all rows first to know total height
        rows = []
        for ab in known:
            rows.append(("known", ab))
        if locked:
            rows.append(("header", "NOT YET LEARNED"))
            for ab in locked[:8]:  # cap at 8 locked
                rows.append(("locked", ab))

        ROW_H = 58
        total_h = len(rows) * ROW_H
        max_scroll = max(0, total_h - (BODY_BOT - BODY_TOP - 20))

        # Clamp scroll
        scroll_offset = max(0, min(scroll_offset, max_scroll))
        self._stats_scroll = scroll_offset

        # Draw scrollbar if needed
        if max_scroll > 0:
            sb_x = col_x + col_w + 4
            sb_h = BODY_BOT - BODY_TOP - 20
            sb_rect = pygame.Rect(sb_x, ay, 6, sb_h)
            pygame.draw.rect(surface, (40,35,55), sb_rect, border_radius=3)
            thumb_h = max(20, int(sb_h * (sb_h / total_h)))
            thumb_y = ay + int((sb_h - thumb_h) * scroll_offset / max_scroll)
            pygame.draw.rect(surface, (100,80,140),
                             pygame.Rect(sb_x, thumb_y, 6, thumb_h), border_radius=3)

        ry2 = ay - scroll_offset
        for kind, ab in rows:
            if ry2 + ROW_H < ay or ry2 > BODY_BOT:
                ry2 += ROW_H
                continue
            if kind == "header":
                draw_text(surface, ab, col_x, ry2 + 4, (80,70,110), 10, bold=True)
                ry2 += ROW_H
                continue

            card_rect = pygame.Rect(col_x, ry2, col_w, ROW_H - 4)
            is_locked = (kind == "locked")
            ab_type = ab.get("type","attack")
            _CAMP = {"heal","aoe_heal","cure","revive"}
            is_camp = ab_type in _CAMP and not is_locked

            # Key: use ability name so click handler can find it reliably
            ab_name_key = f"midcol_camp:{ab.get('name','')}"
            if is_camp:
                self._stats_hit_map[ab_name_key] = card_rect

            # Is this card expanded (clicked)?
            sel_camp = getattr(self, "_stats_midcol_sel", None)
            is_expanded = (is_camp and sel_camp == ab.get("name"))

            # Background
            if is_expanded:
                bg_col = (28, 20, 46)
            elif is_camp and card_rect.collidepoint(mx, my):
                bg_col = (26, 19, 44)
            elif is_locked:
                bg_col = (10, 8, 16)
            else:
                bg_col = (14, 11, 22)
            pygame.draw.rect(surface, bg_col, card_rect, border_radius=4)

            type_col = TYPE_COLORS.get(ab_type, GREY)
            if is_locked: type_col = (60,55,70)

            # Border: green for expanded, bright green on hover, normal otherwise
            if is_expanded:
                border_col = (120, 220, 140)
            elif is_camp and card_rect.collidepoint(mx, my):
                border_col = (90, 180, 110)
            elif is_locked:
                border_col = (40,35,55)
            else:
                border_col = type_col
            pygame.draw.rect(surface, border_col, card_rect, 1, border_radius=4)

            # Name
            name_col = CREAM if not is_locked else (80,75,90)
            draw_text(surface, ab.get("name","?"), col_x + 8, ry2 + 5, name_col, 13, bold=not is_locked, max_width=col_w - 80)

            if is_locked:
                draw_text(surface, f"Unlocks at level {ab.get('level',1)}",
                          col_x + 8, ry2 + 20, (70,65,85), 11)
            else:
                # Type pill
                type_label = ab_type.upper().replace("_"," ")
                pill_w = get_font(9).size(type_label)[0] + 8
                pill = pygame.Rect(col_x + col_w - pill_w - 6, ry2 + 5, pill_w, 14)
                pygame.draw.rect(surface, type_col, pill, border_radius=3)
                draw_text(surface, type_label, pill.x + 4, pill.y + 2, (20,15,30), 9, bold=True)

                # Expand/collapse chevron for camp abilities
                if is_camp:
                    chev = "▼" if is_expanded else "▶"
                    draw_text(surface, chev, col_x + col_w - pill_w - 22, ry2 + 5,
                              (120,220,140) if is_expanded else (80,160,100), 11)

                # Cost
                cost = ab.get("cost", 0)
                res_key = ab.get("resource","STR-SP")
                if cost:
                    draw_text(surface, f"Cost: {cost} {res_key}",
                              col_x + 8, ry2 + 20, (160,140,100), 11)

                # Description row
                desc = ab.get("desc") or ab.get("description","")
                if not is_expanded and is_camp and card_rect.collidepoint(mx, my):
                    draw_text(surface, "▶ Click to expand & cast in camp",
                              col_x + 8, ry2 + 33, (120, 220, 140), 11)
                elif desc:
                    draw_text(surface, desc, col_x + 8, ry2 + 33,
                              GREY, 11, max_width=col_w - 16)

            ry2 += ROW_H

            # ── Inline expanded popup for camp-castable ability ───────────
            if is_expanded and not is_locked:
                # Check if this spell is awaiting target selection
                awaiting_target = (getattr(self, "_stats_midcol_target_ab", None) == ab.get("name"))
                is_aoe = (ab_type == "aoe_heal")
                needs_target = not is_aoe and awaiting_target

                popup_h = 58 if not needs_target else (58 + len(self.party) * 22 + 4)
                pop_r = pygame.Rect(col_x, ry2, col_w, popup_h)
                if pop_r.bottom < BODY_BOT:
                    self._stats_hit_map[f"midcol_popup:{ab.get('name','')}"] = pop_r
                    pygame.draw.rect(surface, (18,14,32), pop_r, border_radius=4)
                    border_c = (220,160,60) if needs_target else (80,160,100)
                    pygame.draw.rect(surface, border_c, pop_r, 1, border_radius=4)
                    desc2 = ab.get("desc") or ab.get("description","")
                    if desc2:
                        draw_text(surface, desc2, col_x+8, ry2+5, GREY, 10, max_width=col_w-12)
                    power = ab.get("power", 1.0)
                    stat_sum = c.stats.get("WIS",0) + c.stats.get("PIE",0)
                    est = int((stat_sum * power * 2) + (c.level * power * 3))
                    draw_text(surface, f"Est. {ab_type.replace('_',' ').title()}: ~{est} pts",
                              col_x+8, ry2+20, (140,200,140), 10)
                    cost2 = ab.get("cost",0); res2 = ab.get("resource","")
                    can_cast = c.resources.get(res2,0) >= cost2 if cost2 else True

                    if needs_target:
                        # Show target picker pills
                        draw_text(surface, "Choose target:", col_x+8, ry2+33, (220,180,60), 10, bold=True)
                        ty_pill = ry2 + 46
                        for gi, gch in enumerate(self.party):
                            hp = gch.resources.get("HP", 0)
                            can_target = (ab_type != "revive" or hp <= 0) and                                          (ab_type not in ("heal","cure") or hp > 0)
                            t_col = CREAM if can_target else (70,65,80)
                            hp_str = f"{hp}HP" if hp > 0 else "KO"
                            pill_r = pygame.Rect(col_x+8, ty_pill, col_w-16, 18)
                            if can_target:
                                self._stats_hit_map[f"midcol_target:{gi}"] = pill_r
                                hov_t = pill_r.collidepoint(mx, my)
                                bg_t = (50,38,20) if hov_t else (28,22,12)
                                bd_t = (200,160,60) if hov_t else (80,65,30)
                            else:
                                bg_t = (22,20,26); bd_t = (50,45,60)
                            pygame.draw.rect(surface, bg_t, pill_r, border_radius=3)
                            pygame.draw.rect(surface, bd_t, pill_r, 1, border_radius=3)
                            draw_text(surface, f"{gch.name}  ({hp_str})",
                                      col_x+12, ty_pill+3, t_col, 10)
                            ty_pill += 22
                    else:
                        cast_r = pygame.Rect(col_x+8, ry2+33, 70, 20)
                        if can_cast:
                            self._stats_hit_map[f"midcol_cast:{ab.get('name','')}"] = cast_r
                            draw_button(surface, cast_r, "Cast",
                                        hover=cast_r.collidepoint(mx,my), size=10)
                        else:
                            draw_text(surface, f"Need {cost2} {res2}", col_x+8, ry2+36, (180,80,80), 10)
                    ry2 += popup_h + 3

        # ─────────────────────────────────────────────────────────────────
        #  RIGHT COLUMN — single source of truth for all clickable elements
        #  Every interactive rect is stored in self._stats_hit_map so the
        #  click handler never recomputes positions independently.
        # ─────────────────────────────────────────────────────────────────
        self._stats_hit_map.setdefault   # already initialised above
        ex = RIGHT_X
        ey = BODY_TOP + 4
        COL_W = SCREEN_W - RIGHT_X - 10

        # ── STATUS PILLS ─────────────────────────────────────────────────
        from core.status_effects import get_status_effects
        try:
            from core.classes import get_all_resources as _gar
            max_hp = _gar(c.class_name, c.stats, c.level).get("HP", 1)
        except Exception:
            max_hp = max(1, c.resources.get("HP", 1))
        hp     = c.resources.get("HP", 0)
        effects = get_status_effects(c)
        pills = []
        if hp <= 0:
            pills.append(("DEAD",     (180, 40,  40)))
        elif hp < max_hp * 0.25:
            pills.append(("CRITICAL", (220, 80,  40)))
        else:
            pills.append(("OK",       (60,  180, 80)))
        _SEC = {
            "poison":(80,200,80),"disease":(140,200,60),"stun":(220,200,60),
            "sleep":(80,140,220),"blind":(160,100,180),"paralyze":(200,80,200),
            "burn":(220,120,40),"curse":(160,60,200),"bleed":(200,60,80),"slow":(140,140,200),
        }
        for s in effects:
            st = s.get("type", s.get("name",""))
            pills.append((st.upper()[:10], _SEC.get(st,(180,160,100))))
        px = ex
        for lbl, col in pills:
            pw = get_font(10).size(lbl)[0] + 10
            pr = pygame.Rect(px, ey, pw, 17)
            pygame.draw.rect(surface, (int(col[0]*.25),int(col[1]*.25),int(col[2]*.25)), pr, border_radius=3)
            pygame.draw.rect(surface, col, pr, 1, border_radius=3)
            draw_text(surface, lbl, px+5, ey+3, col, 10, bold=True)
            px += pw + 4
            if px > SCREEN_W - 30:
                px = ex; ey += 20
        ey += 21
        pygame.draw.line(surface, (50,42,65), (ex, ey-3), (SCREEN_W-10, ey-3))

        # ── EQUIPPED ITEMS (compact — 15px per slot) ─────────────────────
        draw_text(surface, "EQUIPPED  (click to unequip)", ex, ey, STAT_LABEL, 10, bold=True)
        ey += 14
        EQUIP_DISPLAY = [
            ("weapon","Weapon"),("off_hand","Off-Hand"),("head","Head"),("crown","Crown"),
            ("body","Body"),("hands","Hands"),("feet","Feet"),("neck","Neck"),
            ("ring1","Ring 1"),("ring2","Ring 2"),("ring3","Ring 3"),
        ]
        equipment = c.equipment if hasattr(c,"equipment") and c.equipment else {}
        hover_item = None
        for slot_key, slot_label in EQUIP_DISPLAY:
            item = equipment.get(slot_key)
            row_r = pygame.Rect(ex, ey, COL_W, 15)
            hover = row_r.collidepoint(mx, my)
            if item:
                self._stats_hit_map[f"unequip:{slot_key}"] = row_r
                if hover:
                    pygame.draw.rect(surface, (45,35,60), row_r, border_radius=2)
                    hover_item = item
            draw_text(surface, f"{slot_label}:", ex, ey, STAT_LABEL, 10)
            if item:
                rar_col = {"uncommon":(140,200,255),"rare":(180,120,255),"epic":(255,180,60)}.get(
                    item.get("rarity",""), CREAM)
                draw_text(surface, item.get("name","?")[:18], ex+60, ey, rar_col, 10)
                if hover:
                    cursed = item.get("cursed") and not item.get("curse_lifted")
                    draw_text(surface, "CURSED" if cursed else "× unequip",
                              ex+210, ey, RED if cursed else DIM_GOLD, 9)
            else:
                draw_text(surface, "—", ex+60, ey, (50,45,65), 10)
            ey += 15

        # Hover preview (compact — only show name + bonuses, not full panel)
        if hover_item:
            sb = hover_item.get("stat_bonuses",{})
            if sb:
                bs = "  ".join(f"+{v}{k}" for k,v in list(sb.items())[:3])
                draw_text(surface, bs, ex, ey, (120,200,120), 10)
                ey += 13

        ey += 5
        pygame.draw.line(surface, (50,42,65), (ex, ey-2), (SCREEN_W-10, ey-2))

        # ── INVENTORY — scrollable ────────────────────────────────────────
        draw_text(surface, "INVENTORY  (click item · then act)", ex, ey, STAT_LABEL, 10, bold=True)
        ey += 13
        sel_ii      = getattr(self, "_stats_inv_sel", -1)
        INV_ITEM_H  = 15
        BTN_RESERVE = 56     # space for action buttons at bottom
        inv_bot     = BODY_BOT - BTN_RESERVE
        vis_n       = max(1, (inv_bot - ey) // INV_ITEM_H)
        total_inv   = len(c.inventory)
        max_off     = max(0, total_inv - vis_n)
        # Clamp scroll offset
        inv_off = max(0, min(getattr(self, "_stats_inv_scroll", 0), max_off))
        self._stats_inv_scroll = inv_off
        SB_W = 8
        inv_col_w = COL_W - SB_W - 2

        for slot_i, ii in enumerate(range(inv_off, min(total_inv, inv_off + vis_n))):
            it   = c.inventory[ii]
            row_y = ey + slot_i * INV_ITEM_H
            it_r = pygame.Rect(ex, row_y, inv_col_w, INV_ITEM_H)
            self._stats_hit_map[f"inv:{ii}"] = it_r
            sel = (sel_ii == ii)
            hov = it_r.collidepoint(mx, my)
            if sel:
                pygame.draw.rect(surface, (50,38,72), it_r, border_radius=2)
                pygame.draw.rect(surface, DIM_GOLD, it_r, 1, border_radius=2)
            elif hov:
                pygame.draw.rect(surface, (32,26,50), it_r, border_radius=2)
            rc = {"uncommon":(140,200,255),"rare":(180,120,255),"epic":(255,180,60)}.get(
                it.get("rarity",""), CREAM)
            draw_text(surface, it.get("name","?")[:24], ex+3, row_y+2, rc, 10)
            draw_text(surface, it.get("type","")[:5], SCREEN_W-66, row_y+2, STAT_LABEL, 9)

        # Scrollbar
        if total_inv > vis_n:
            sb_x    = ex + inv_col_w + 2
            sb_top  = ey
            sb_full = vis_n * INV_ITEM_H
            pygame.draw.rect(surface, (28,22,40), (sb_x, sb_top, SB_W, sb_full), border_radius=3)
            th = max(12, int(sb_full * vis_n / max(1, total_inv)))
            ty = sb_top + int((sb_full - th) * inv_off / max(1, max_off))
            pygame.draw.rect(surface, (90,70,130), (sb_x, ty, SB_W, th), border_radius=3)

        ey += vis_n * INV_ITEM_H
        shown = min(total_inv, vis_n)

        # Action buttons for selected item
        if 0 <= sel_ii < len(c.inventory) and ey < BODY_BOT - 30:
            sel_it    = c.inventory[sel_ii]
            protected = sel_it.get("type") in ("key_item","quest_item") or "warden_rank" in sel_it
            bx = ex
            if sel_it.get("type") in ("consumable","potion","food"):
                r = pygame.Rect(bx, ey, 55, 22); self._stats_hit_map["act:use"] = r
                draw_button(surface, r, "Use", hover=r.collidepoint(mx,my), size=10); bx += 60
            if sel_it.get("slot"):
                r = pygame.Rect(bx, ey, 60, 22); self._stats_hit_map["act:equip"] = r
                draw_button(surface, r, "Equip", hover=r.collidepoint(mx,my), size=10); bx += 65
            if not protected:
                r = pygame.Rect(bx, ey, 55, 22); self._stats_hit_map["act:drop"] = r
                draw_button(surface, r, "Drop", hover=r.collidepoint(mx,my), size=10); bx += 60
            if len(self.party) > 1:
                r = pygame.Rect(bx, ey, 55, 22); self._stats_hit_map["act:give"] = r
                draw_button(surface, r, "Give", hover=r.collidepoint(mx,my), size=10)
            ey += 26
            if getattr(self,"_give_mode",False) and ey < BODY_BOT - 26:
                bx = ex
                for gi, gch in enumerate(self.party):
                    if gi == self.selected_char: continue
                    gw = max(55, len(gch.name)*7+10)
                    r  = pygame.Rect(bx, ey, gw, 20)
                    self._stats_hit_map[f"act:give_to:{gi}"] = r
                    draw_button(surface, r, gch.name, hover=r.collidepoint(mx,my), size=10)
                    bx += gw + 5
                ey += 24

            # ── Item detail + comparison panel for equippable items ──────
            if ey < BODY_BOT - 30:
                avail_detail = min(180, BODY_BOT - ey - 8)
                if sel_it.get("slot"):
                    detail_ph = self._draw_item_details(surface, sel_it, ey,
                                                        max_h=avail_detail)
                    cmp_top = ey + detail_ph + 4
                    if cmp_top < BODY_BOT - 20:
                        self._draw_equip_compare(surface, sel_it, ex, cmp_top, COL_W)
                elif sel_it.get("type") in ("consumable","potion","food"):
                    self._draw_item_details(surface, sel_it, ey,
                                            max_h=avail_detail)

        surface.set_clip(None)




    # ─────────────────────────────────────────────────────────────────
    #  MANUAL OVERLAY
    # ─────────────────────────────────────────────────────────────────

    _MANUAL_PAGES = [
        {
            "title": "Welcome to Realm of Shadows",
            "sections": [
                ("The World", "Aldenmere is dying — the Fading, a magical entropy, is dissolving reality at the edges. You are Wardens, an ancient order charged with recovering the five Hearthstones and confronting the source of the Shadow."),
                ("Moving Around", "On the World Map, click a location to travel to it. Towns show services. Dungeons require exploration. Ports allow sea travel to distant regions."),
                ("Saving the Game", "Use the Save button on the World Map or inside a dungeon. The game auto-saves when you rest at an inn."),
                ("Resting", "The Camp screen (C key in dungeon, or from the World Map) lets you rest, manage equipment, review your party, and access abilities."),
            ]
        },
        {
            "title": "Combat",
            "sections": [
                ("Turn Order", "Combatants act in speed order (DEX matters). Your party goes when the action bar shows your character. Enemies act automatically."),
                ("Actions", "Each turn: Attack (standard hit), Use Ability (costs resources), Defend (+50% physical defense this round), or Flee (attempt escape)."),
                ("Targeting", "Click an enemy to target them. Front-row enemies must be eliminated before you can target the back row."),
                ("Abilities", "Abilities cost SP (Strength Points), MP (Magic Points), or Ki. Your resources restore fully when you rest at an inn."),
                ("Status Effects", "Poisoned: lose HP each round. Stunned: skip turn. Slowed: act last. Burning: fire damage over time. Check the combat log for details."),
                ("Winning and Losing", "Victory: all enemies defeated. Defeat: whole party unconscious. You respawn at the last inn with a gold penalty."),
            ]
        },
        {
            "title": "Equipment",
            "sections": [
                ("Slots", "Each character has 11 equipment slots: Weapon, Off-Hand, Head, Crown, Body, Hands, Feet, Neck, and three Ring slots."),
                ("Proficiency", "Equipping a weapon your class isn't trained with deals 20% less damage. Check the Equipment tab to see what you can use."),
                ("Identification", "Items found in dungeons are often unidentified. Use the Identify tab in Camp, or visit a temple to identify items."),
                ("Rarity", "Common (white) → Uncommon (blue) → Rare (purple) → Epic (gold). Higher rarity means better stats."),
                ("Wands, Rods, Orbs", "Focus items used by casters. Scale with INT (wands, rods) or INT+WIS (orbs). Only caster classes can use them effectively."),
            ]
        },
        {
            "title": "Character Classes",
            "sections": [
                ("Fighter", "Front-line melee warrior. High HP, heavy armor, strong physical abilities. Power Strike, Shield Bash, War Cry."),
                ("Mage", "Arcane spellcaster. Fragile but devastating. Fireball, Chain Lightning, Meteor. Stays in the back row."),
                ("Cleric", "Divine healer and smiter. Heal, Prayer of Healing, Turn Undead. Can wear heavy armor and use blessed weapons."),
                ("Thief", "Agile striker with high dodge and crit. Backstab, Poison Blade, Assassinate. Wears light armor."),
                ("Ranger", "Versatile hunter: ranged attacks and nature magic. Aimed Shot, Barrage, Nature's Balm. Medium armor."),
                ("Monk", "Unarmed martial artist. Unarmed damage scales with level and WIS. Flurry of Blows, Stunning Fist, Dragon Strike. Clothing only."),
            ]
        },
        {
            "title": "The Warden Rank System",
            "sections": [
                ("Overview", "Your party earns Warden Rank as you recover Hearthstones and advance in level. Rank brings permanent bonuses to all characters."),
                ("Initiate", "Starting rank. No bonuses. Prove yourself."),
                ("Scout", "Earned after the first Hearthstone (Abandoned Mine, level 5+). +1 all stats, +5% XP."),
                ("Warden", "After the third Hearthstone (Dragon's Tooth, level 10+). +2 all stats, +5% HP, +10% XP."),
                ("Senior Warden", "After all five Hearthstones (level 13+). +4 all stats, +10% HP, +5% damage, +15% XP."),
                ("Warden-Commander", "After defeating Valdris (level 15+). +6 all stats, +15% HP, +10% damage, +25% XP. The highest rank."),
                ("Certification", "Visit the Warden Liaison NPC in any town to check your current rank and learn what is needed to advance."),
            ]
        },
        {
            "title": "Dungeons",
            "sections": [
                ("Exploring", "Move with WASD or arrow keys. The 3D view shows what's ahead. The minimap in the corner shows your position and explored tiles."),
                ("Encounters", "Moving through dungeons triggers random encounters. Boss encounters are fixed on the final floor."),
                ("Interactables", "Chests contain loot. Shrines restore HP/MP. Fountains have one-time effects. Traps can be disarmed by Thieves."),
                ("Floors", "Stairs down go deeper. Stairs up return toward the entrance. Floor 1 is easiest; deepest floors have the boss."),
                ("The Fading", "In Act 2 and 3, some dungeons are corrupted by the Fading. Enemies are tougher and the atmosphere changes."),
                ("Fleeing", "You can attempt to flee combat. Success chance depends on your DEX vs the enemies. Fleeing returns you to the dungeon corridor."),
            ]
        },
        {
            "title": "Towns & Services",
            "sections": [
                ("Shop", "Buy weapons, armor, and consumables. Sell found items. Prices vary by town."),
                ("Temple", "Revive fallen party members, remove curses, identify items, buy healing supplies."),
                ("Inn", "Rest to restore all HP, MP, and SP. Level up characters here. Choose between Common Room (50% restore, cheaper) or Private Room (full restore)."),
                ("Tavern", "Hear rumors — story-relevant whispers change as the world shifts. Buy drinks to learn more."),
                ("Guild", "Post and collect job board contracts for extra gold and XP. Bounties on specific dungeon enemies."),
                ("Warden Liaison", "Found in each town. Shows your current Warden Rank, active bonuses, and what is required to advance to the next rank."),
            ]
        },
        {
            "title": "Tips & Secrets",
            "sections": [
                ("Formation Matters", "Put your toughest characters in the front row. Back-row characters take less damage but deal less with melee weapons."),
                ("Resource Management", "Don't use all your abilities in every fight. Save big spells for boss encounters and hard fights."),
                ("Hearthstones Are Story", "Recovering Hearthstones advances the main story and unlocks new areas. Each one makes the whole party stronger."),
                ("Moral Choices", "Not every enemy is simply evil. Some bosses can be negotiated with. Listen to what they say before attacking."),
                ("Tavern Rumors", "The rumors in taverns change as the story progresses. They hint at where to go next and what threats are growing."),
                ("Explore Everything", "Secret locations are hidden on the world map. Some require specific keys to discover. Talk to everyone — NPCs give hints."),
            ]
        },
    ]

    def _draw_manual(self, surface, mx, my):
        """Draw the in-game manual overlay."""
        if not getattr(self, "_manual_open", False):
            return

        # Darken background
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))

        page = getattr(self, "_manual_page", 0)
        pages = self._MANUAL_PAGES
        page = max(0, min(page, len(pages)-1))
        self._manual_page = page

        # Panel
        PW, PH = 900, 680
        px = SCREEN_W//2 - PW//2
        py = SCREEN_H//2 - PH//2
        panel = pygame.Surface((PW, PH), pygame.SRCALPHA)
        panel.fill((8, 6, 20, 252))
        surface.blit(panel, (px, py))
        pygame.draw.rect(surface, GOLD, (px, py, PW, PH), 2, border_radius=8)
        pygame.draw.rect(surface, (60, 200, 100), (px, py, PW, 5), border_radius=8)

        # Title
        draw_text(surface, "◈  REALM OF SHADOWS — MANUAL  ◈",
                  px + PW//2 - get_font(14).size("◈  REALM OF SHADOWS — MANUAL  ◈")[0]//2,
                  py + 10, GOLD, 14, bold=True)

        # Page nav
        page_str = f"Page {page+1} of {len(pages)}"
        draw_text(surface, page_str,
                  px + PW//2 - get_font(11).size(page_str)[0]//2,
                  py + 30, GREY, 11)

        # Prev / Next buttons
        self._manual_prev_rect = pygame.Rect(px + 20, py + PH - 44, 110, 32)
        self._manual_next_rect = pygame.Rect(px + PW - 130, py + PH - 44, 110, 32)
        self._manual_close_rect = pygame.Rect(px + PW//2 - 55, py + PH - 44, 110, 32)

        for rect, label, enabled in [
            (self._manual_prev_rect, "◄  Previous", page > 0),
            (self._manual_next_rect, "Next  ►", page < len(pages)-1),
            (self._manual_close_rect, "Close  [M]", True),
        ]:
            col = (40,35,60) if enabled else (20,18,30)
            bcol = GOLD if enabled else (40,35,55)
            pygame.draw.rect(surface, col, rect, border_radius=5)
            pygame.draw.rect(surface, bcol, rect, 1, border_radius=5)
            tcol = CREAM if enabled else (60,55,75)
            tw = get_font(12).size(label)[0]
            draw_text(surface, label, rect.x + (rect.width - tw)//2,
                      rect.y + 8, tcol, 12)

        # Page tabs (small) along left
        tab_h = min(44, (PH - 100) // len(pages))
        for i, pg in enumerate(pages):
            tr = pygame.Rect(px - 22, py + 50 + i * tab_h, 22, tab_h - 2)
            is_cur = (i == page)
            pygame.draw.rect(surface, (40,35,60) if is_cur else (18,14,28), tr,
                             border_radius=3)
            if is_cur:
                pygame.draw.rect(surface, GOLD, tr, 1, border_radius=3)
            if tr.collidepoint(mx, my):
                pygame.draw.rect(surface, DIM_GOLD, tr, 1, border_radius=3)
            # Store for click detection
            if not hasattr(self, "_manual_tabs"):
                self._manual_tabs = []
            if i >= len(self._manual_tabs):
                self._manual_tabs.append(tr)
            else:
                self._manual_tabs[i] = tr
            # Page number in tab
            draw_text(surface, str(i+1),
                      tr.x + 6, tr.y + (tab_h - 14)//2,
                      GOLD if is_cur else GREY, 10)

        # Content area
        content_rect = pygame.Rect(px + 20, py + 50, PW - 40, PH - 110)
        surface.set_clip(content_rect)

        pg_data = pages[page]
        cy = py + 52

        # Page title
        draw_text(surface, pg_data["title"], px + 20, cy, GOLD, 18, bold=True)
        cy += 28
        pygame.draw.line(surface, (60, 200, 100), (px+20, cy), (px+PW-20, cy))
        cy += 10

        scroll = getattr(self, "_manual_scroll", 0)
        cy -= scroll

        for section_title, section_text in pg_data["sections"]:
            if cy > py + PH - 60:
                break
            draw_text(surface, section_title, px + 20, cy,
                      (100, 200, 255), 13, bold=True)
            cy += 17
            draw_text(surface, section_text, px + 28, cy,
                      CREAM, 12, max_width=PW - 56)
            # Estimate height of wrapped text
            words = section_text.split()
            char_per_line = (PW - 56) // 7  # rough
            lines_count = max(1, len(" ".join(words)) // char_per_line + 1)
            cy += lines_count * 15 + 12

        surface.set_clip(None)

    def _handle_stats_click(self, mx, my):
        """Party tab click handler — reads ONLY from _stats_hit_map populated by _draw_stats.
        Zero position arithmetic here; draw is the single source of truth."""
        c   = self.party[self.selected_char]
        hm  = getattr(self, "_stats_hit_map", {})

        for key, rect in hm.items():
            if not rect.collidepoint(mx, my):
                continue

            # ── Unequip equipped item ──────────────────────────────────
            if key.startswith("unequip:"):
                slot = key[len("unequip:"):]
                equipment = c.equipment if hasattr(c,"equipment") and c.equipment else {}
                item = equipment.get(slot)
                if item:
                    if item.get("cursed") and not item.get("curse_lifted"):
                        self._msg(f"{item.get('name','item')} is cursed — cannot unequip!", RED)
                    else:
                        c.equipment[slot] = None
                        c.inventory.append(item)
                        self._msg(f"Unequipped {item.get('name','item')}.", DIM_GOLD)
                return None

            # ── Inventory row — select item ────────────────────────────
            if key.startswith("inv:"):
                ii = int(key[4:])
                if getattr(self,"_stats_inv_sel",-1) == ii:
                    self._stats_inv_sel = -1   # deselect on second click
                else:
                    self._stats_inv_sel = ii
                    self._give_mode = False
                return None

            # ── Inventory action buttons ───────────────────────────────
            if key == "act:use":
                ii = getattr(self,"_stats_inv_sel",-1)
                if 0 <= ii < len(c.inventory):
                    self._use_item(c, ii)
                    self._stats_inv_sel = -1
                return None

            if key == "act:equip":
                ii = getattr(self,"_stats_inv_sel",-1)
                if 0 <= ii < len(c.inventory):
                    self._equip_item(c, ii)
                    self._stats_inv_sel = -1
                return None

            if key == "act:drop":
                ii = getattr(self,"_stats_inv_sel",-1)
                if 0 <= ii < len(c.inventory):
                    name = c.inventory[ii].get("name","item")
                    c.inventory.pop(ii)
                    self._stats_inv_sel = -1
                    self._msg(f"Dropped {name}.", ORANGE)
                return None

            if key == "act:give":
                self._give_mode = not getattr(self,"_give_mode",False)
                return None

            if key.startswith("act:give_to:"):
                gi = int(key[len("act:give_to:"):])
                ii = getattr(self,"_stats_inv_sel",-1)
                if 0 <= ii < len(c.inventory) and 0 <= gi < len(self.party):
                    xfer = c.inventory.pop(ii)
                    self.party[gi].inventory.append(xfer)
                    self._stats_inv_sel = -1
                    self._give_mode = False
                    self._msg(f"Gave {xfer.get('name','item')} to {self.party[gi].name}.", GOLD)
                return None

            # ── Middle column camp ability card — toggle expand ──────────
            if key.startswith("midcol_camp:"):
                ab_name = key[len("midcol_camp:"):]
                cur_sel = getattr(self, "_stats_midcol_sel", None)
                self._stats_midcol_sel = ab_name if cur_sel != ab_name else None
                return None

            # ── Middle column camp ability popup background (no-op click) ─
            if key.startswith("midcol_popup:"):
                return None   # click inside popup area but not Cast button

            # ── Middle column Cast button ─────────────────────────────────
            if key.startswith("midcol_cast:"):
                ab_name = key[len("midcol_cast:"):]
                CAMP_TYPES = ("heal","aoe_heal","cure","revive")
                for ab in c.abilities:
                    if ab.get("name") == ab_name and ab.get("type") in CAMP_TYPES:
                        if ab.get("type") == "aoe_heal":
                            # AoE: no target needed — cast immediately on all
                            self._cast_camp_spell(c, ab)
                            self._stats_midcol_sel = None
                        else:
                            # Single-target: open target picker in the popup
                            self._stats_midcol_target_ab = ab_name
                            if not hasattr(self, "_stats_midcol_target_ab"):
                                self._stats_midcol_target_ab = ab_name
                        break
                return None

            # ── Middle column target picker pill ─────────────────────────
            if key.startswith("midcol_target:"):
                gi = int(key[len("midcol_target:"):])
                ab_name = getattr(self, "_stats_midcol_target_ab", None)
                if ab_name:
                    CAMP_TYPES = ("heal","aoe_heal","cure","revive")
                    for ab in c.abilities:
                        if ab.get("name") == ab_name and ab.get("type") in CAMP_TYPES:
                            self.spell_target = gi
                            self._cast_camp_spell(c, ab)
                            self._stats_midcol_sel = None
                            self._stats_midcol_target_ab = None
                            break
                return None

        return None

    def handle_scroll(self, direction):
        """Handle mousewheel scrolling."""
        if self.tab == TAB_STATS:
            # Determine which sub-area the mouse is over
            import pygame as _pg
            mx, my = _pg.mouse.get_pos()
            RIGHT_X = 850
            if mx >= RIGHT_X:
                # Right column — inventory scroll
                cur = getattr(self, "_stats_inv_scroll", 0)
                self._stats_inv_scroll = max(0, cur + direction)
            else:
                # Middle column — abilities scroll
                cur = getattr(self, "_stats_scroll", 0)
                self._stats_scroll = max(0, cur + direction * 24)
        elif self.tab == TAB_INVENTORY:
            c = self.party[self.selected_char] if self.party else None
            if c:
                # Use same constants as _draw_inventory so scroll matches draw
                BODY_BOT_inv  = SCREEN_H - 320   # 580 at 900px
                list_top_inv  = 80 + 52           # content_y(80) + header(52) = 132
                ROW_H_inv     = 36
                visible_n = max(1, (BODY_BOT_inv - list_top_inv) // ROW_H_inv)
                from ui.camp_ui import _build_inv_groups
                groups  = _build_inv_groups(c.inventory)
                max_off = max(0, len(groups) - visible_n)
                self.scroll_offset = max(0, min(self.scroll_offset + direction, max_off))
        elif getattr(self, "_manual_open", False):
            cur = getattr(self, "_manual_scroll", 0)
            self._manual_scroll = max(0, cur + direction * 24)

    def toggle_manual(self):
        """Open or close the in-game manual."""
        self._manual_open = not getattr(self, "_manual_open", False)
        if self._manual_open:
            self._manual_page = 0
            self._manual_scroll = 0
            self._manual_tabs = []

    def handle_manual_click(self, mx, my):
        """Handle clicks within the manual overlay. Returns True if consumed."""
        if not getattr(self, "_manual_open", False):
            return False
        if getattr(self, "_manual_prev_rect", None) and self._manual_prev_rect.collidepoint(mx, my):
            self._manual_page = max(0, getattr(self,"_manual_page",0) - 1)
            self._manual_scroll = 0
            return True
        if getattr(self, "_manual_next_rect", None) and self._manual_next_rect.collidepoint(mx, my):
            self._manual_page = min(len(self._MANUAL_PAGES)-1, getattr(self,"_manual_page",0) + 1)
            self._manual_scroll = 0
            return True
        if getattr(self, "_manual_close_rect", None) and self._manual_close_rect.collidepoint(mx, my):
            self._manual_open = False
            return True
        for i, tr in enumerate(getattr(self, "_manual_tabs", [])):
            if tr.collidepoint(mx, my):
                self._manual_page = i
                self._manual_scroll = 0
                return True
        return True  # consume all clicks while manual is open
    def _draw_char_selector(self, surface, mx, my, top):
        """Draw character tabs for selecting party member, with reorder arrows."""
        # Reorder arrows (◄ ►) for selected char
        self._reorder_left_rect  = None
        self._reorder_right_rect = None

        draw_text(surface, "Order:", 8, top + 7, GREY, 11)
        cx = 60
        for i, c in enumerate(self.party):
            w = max(80, len(c.name) * 8 + 20)
            r = pygame.Rect(cx, top, w, 38)
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
            draw_text(surface, c.name, r.x + 8, r.y + 4, col, 11, bold=(i == self.selected_char))
            # HP bar under name
            try:
                from core.classes import get_all_resources
                max_r = get_all_resources(c.class_name, c.stats, c.level)
                mhp = max(1, max_r.get("HP", 1))
                chp = c.resources.get("HP", mhp)
                hp_pct = max(0.0, chp / mhp)
                bar_w2 = r.w - 10
                bar_r = pygame.Rect(r.x + 5, r.y + 18, bar_w2, 5)
                hp_col = (60,200,80) if hp_pct > 0.5 else (220,160,40) if hp_pct > 0.25 else (220,60,60)
                pygame.draw.rect(surface, (40,20,20), bar_r, border_radius=2)
                fill_w = int(bar_w2 * hp_pct)
                if fill_w > 0:
                    pygame.draw.rect(surface, hp_col,
                                     pygame.Rect(bar_r.x, bar_r.y, fill_w, 5), border_radius=2)
                draw_text(surface, f"{chp}/{mhp}", r.x + 5, r.y + 20, (160,130,130), 9)
            except Exception:
                pass
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
    #  SPELLS TAB  (out-of-combat healing, cures, revives)
    # ──────────────────────────────────────────────────────────

    def _draw_spells(self, surface, mx, my, top):
        """Draw the camp spells panel — heal/cure/revive abilities only."""
        from core.classes import get_all_resources

        # Character selector (caster)
        self._draw_char_selector(surface, mx, my, top)
        caster = self.party[self.selected_char]

        CAMP_TYPES = ("heal", "aoe_heal", "cure", "revive")
        abilities = [a for a in caster.abilities if a.get("type") in CAMP_TYPES]

        if not abilities:
            draw_text(surface, f"{caster.name} has no usable camp spells.", 80, top + 60, GREY, 14)
            draw_text(surface, "(Clerics, Rangers, Monks and some hybrid classes can heal.)",
                      80, top + 84, STAT_LABEL, 12)
            return

        # Caster resources
        max_res = get_all_resources(caster.class_name, caster.stats, caster.level)
        res_y = top + 48
        draw_text(surface, "Resources:", 80, res_y, STAT_LABEL, 12)
        rx = 180
        for rk, mv in max_res.items():
            if rk == "HP": continue
            cv = caster.resources.get(rk, 0)
            col = (100, 200, 140) if cv >= mv * 0.5 else ORANGE if cv > 0 else (180, 60, 60)
            draw_text(surface, f"{rk}: {cv}/{mv}", rx, res_y, col, 12)
            rx += 120

        # Spell list
        spell_y = res_y + 28
        draw_text(surface, "Spells:", 80, spell_y, STAT_LABEL, 12)
        spell_y += 20
        self._spell_rects = []
        for i, ab in enumerate(abilities):
            rk   = ab.get("resource", "")
            cost = ab.get("cost", 0)
            cur  = caster.resources.get(rk, 0)
            can  = cur >= cost
            row  = pygame.Rect(80, spell_y + i * 42, SCREEN_W // 2 - 100, 38)
            hover = row.collidepoint(mx, my)
            sel   = (i == self.spell_selected)
            bg    = (60, 45, 80) if sel else (ITEM_HOVER if hover else ITEM_BG)
            pygame.draw.rect(surface, bg, row, border_radius=4)
            pygame.draw.rect(surface, GOLD if sel else (PANEL_BORDER), row, 1, border_radius=4)
            name_col = CREAM if can else (100, 85, 110)
            draw_text(surface, ab["name"], row.x + 10, row.y + 5, name_col, 13, bold=True)
            cost_col = (100, 200, 140) if can else (200, 80, 80)
            draw_text(surface, f"{rk} -{cost}  ({ab.get('desc','')})",
                      row.x + 10, row.y + 22, cost_col, 10)
            self._spell_rects.append((row, i, ab, can))

        # Target selector (right panel)
        if self.spell_selected >= 0 and self.spell_selected < len(abilities):
            ab = abilities[self.spell_selected]
            tx = SCREEN_W // 2 + 20
            ty = res_y + 28
            draw_text(surface, "Target:", tx, ty, STAT_LABEL, 12)
            ty += 20
            self._spell_target_rects = []
            ab_type = ab.get("type", "")
            is_revive = (ab_type == "revive")
            is_aoe = (ab_type == "aoe_heal")
            if is_aoe:
                # AOE: auto-targets all — just show cast button
                draw_text(surface, "Targets all party members.", tx, ty, GREY, 12)
                ty += 24
                self._spell_target_rects = []
            else:
                for j, tgt in enumerate(self.party):
                    max_res_t = get_all_resources(tgt.class_name, tgt.stats, tgt.level)
                    mhp = max(1, max_res_t.get("HP", 1))
                    chp = tgt.resources.get("HP", 0)
                    dead = chp <= 0
                    if not is_revive and dead:
                        continue  # can't target dead with heals
                    if is_revive and not dead:
                        continue  # revive only targets dead

                    trow = pygame.Rect(tx, ty, SCREEN_W - tx - 40, 34)
                    thov = trow.collidepoint(mx, my)
                    tsel = (j == self.spell_target)
                    bg2  = (50, 40, 20) if tsel else (ITEM_HOVER if thov else ITEM_BG)
                    pygame.draw.rect(surface, bg2, trow, border_radius=3)
                    pygame.draw.rect(surface, DIM_GOLD if tsel else PANEL_BORDER, trow, 1, border_radius=3)
                    hp_col = HP_BAR if chp / mhp > 0.5 else ORANGE if chp / mhp > 0.2 else RED
                    label = f"{tgt.name} ({chp}/{mhp} HP)"
                    if dead: label = f"{tgt.name} — FALLEN"
                    draw_text(surface, label, trow.x + 8, trow.y + 8,
                              hp_col if not dead else (180, 60, 60), 12)
                    self._spell_target_rects.append((trow, j))
                    ty += 38

            # Cast button
            cast_btn = pygame.Rect(tx, ty + 10, 160, 38)
            rk   = ab.get("resource", "")
            cost = ab.get("cost", 0)
            can  = caster.resources.get(rk, 0) >= cost
            col  = (80, 50, 10) if not can else None
            draw_button(surface, cast_btn, f"Cast {ab['name']}",
                        hover=cast_btn.collidepoint(mx, my) and can, size=13)
            if not can:
                draw_text(surface, "Not enough points", tx, ty + 52, (180, 80, 80), 11)
            self._spell_cast_btn = cast_btn if can else None
        else:
            self._spell_target_rects = []
            self._spell_cast_btn = None

        # ── Focus weapon recharge section ────────────────────────────
        # Shown for any character — Mage or not — who has a depleted focus weapon
        from core.focus_charges import is_focus, init_charges, crystals_needed, get_charge_label, CRYSTAL_NAME
        from core.crafting import count_material
        self._recharge_btns = []   # (rect, item, char)
        recharge_y = top + 340
        found_depleted = False
        for ch in self.party:
            for slot, item in (ch.equipment or {}).items():
                if not item or not is_focus(item):
                    continue
                init_charges(item)
                cur = item.get("charges", 0)
                mx_c = item.get("max_charges", 20)
                if cur >= mx_c:
                    continue
                found_depleted = True
                needed = crystals_needed(item)
                have   = count_material(self.party, CRYSTAL_NAME)
                can_rch = have >= needed > 0
                # Row
                row_r = pygame.Rect(80, recharge_y, SCREEN_W // 2 - 60, 44)
                pygame.draw.rect(surface, (18, 22, 40), row_r, border_radius=4)
                pygame.draw.rect(surface, (80, 120, 200), row_r, 1, border_radius=4)
                lc = (120, 200, 255) if can_rch else GREY
                draw_text(surface, f"{item.get('name','?')} {get_charge_label(item)}",
                          row_r.x + 10, row_r.y + 5, CREAM, 13, bold=True)
                draw_text(surface,
                          f"{ch.name}  ·  Need {needed} {CRYSTAL_NAME}{'s' if needed>1 else ''} (have {have})",
                          row_r.x + 10, row_r.y + 24, lc, 11)
                btn_r = pygame.Rect(row_r.right + 10, recharge_y + 7, 130, 30)
                bc = (80, 160, 255) if can_rch else (55, 55, 70)
                pygame.draw.rect(surface, (12, 18, 38) if can_rch else (18, 18, 28), btn_r, border_radius=4)
                pygame.draw.rect(surface, bc, btn_r, 1, border_radius=4)
                lbl = "Recharge" if can_rch else "No Crystals"
                draw_text(surface, lbl, btn_r.x + 14, btn_r.y + 7, bc, 12)
                self._recharge_btns.append((btn_r, item, ch))
                recharge_y += 50

        if found_depleted and not self._recharge_btns:
            draw_text(surface, "No Mana Crystals in inventory.", 80, recharge_y, GREY, 12)

        # ── Venom reservoir refill section ──────────────────────────
        from core.venom_charges import (is_venom_weapon, init_venom_charges,
                                         vials_needed, get_venom_label, VENOM_VIAL_NAME)
        self._venom_refill_btns = []
        for ch in self.party:
            for slot, item in (ch.equipment or {}).items():
                if not item or not is_venom_weapon(item):
                    continue
                init_venom_charges(item)
                cur = item.get("venom_charges", 0)
                mx_v = item.get("max_venom_charges", 10)
                if cur >= mx_v:
                    continue
                needed_v = vials_needed(item)
                have_v   = count_material(self.party, VENOM_VIAL_NAME)
                can_refill = have_v >= needed_v > 0
                row_r = pygame.Rect(80, recharge_y, SCREEN_W // 2 - 60, 44)
                pygame.draw.rect(surface, (18, 30, 22), row_r, border_radius=4)
                pygame.draw.rect(surface, (60, 160, 80), row_r, 1, border_radius=4)
                draw_text(surface, f"{item.get('name','?')} {get_venom_label(item)}",
                          row_r.x + 10, row_r.y + 5, CREAM, 13, bold=True)
                lc = (120, 220, 140) if can_refill else GREY
                draw_text(surface,
                          f"{ch.name}  ·  Need {needed_v} Venom Vial{'s' if needed_v>1 else ''} (have {have_v})",
                          row_r.x + 10, row_r.y + 24, lc, 11)
                btn_r = pygame.Rect(row_r.right + 10, recharge_y + 7, 130, 30)
                bc = (60, 180, 80) if can_refill else (55, 55, 70)
                pygame.draw.rect(surface, (12, 24, 14) if can_refill else (18, 18, 28), btn_r, border_radius=4)
                pygame.draw.rect(surface, bc, btn_r, 1, border_radius=4)
                lbl = "Refill Venom" if can_refill else "No Vials"
                draw_text(surface, lbl, btn_r.x + 10, btn_r.y + 7, bc, 12)
                self._venom_refill_btns.append((btn_r, item, ch))
                recharge_y += 50

        # ── Arcane Containment Crystal — expand max_charges ──────────
        from core.focus_charges import (ACC_NAME, ACC_CHARGES_BONUS, ACC_MAX_EXPANSIONS,
                                         can_expand)
        have_acc = count_material(self.party, ACC_NAME)
        self._acc_expand_btns = []   # (rect, item, char)
        if have_acc > 0:
            expand_y = recharge_y + 20
            draw_text(surface, f"Arcane Containment Crystal  ×{have_acc}",
                      80, expand_y, (200, 160, 255), 13, bold=True)
            draw_text(surface,
                      f"Permanently expands a focus weapon by +{ACC_CHARGES_BONUS} max charges "
                      f"(up to {ACC_MAX_EXPANSIONS}× per item)",
                      80, expand_y + 16, GREY, 11)
            expand_y += 38
            for ch in self.party:
                for slot, item in (ch.equipment or {}).items():
                    if not item or not is_focus(item):
                        continue
                    init_charges(item)
                    if not can_expand(item):
                        continue
                    exps = item.get("_acc_expansions", 0)
                    row_r = pygame.Rect(80, expand_y, SCREEN_W // 2 - 60, 44)
                    pygame.draw.rect(surface, (22, 16, 38), row_r, border_radius=4)
                    pygame.draw.rect(surface, (150, 90, 220), row_r, 1, border_radius=4)
                    draw_text(surface,
                              f"{item.get('name','?')}  ({item.get('max_charges',20)} → "
                              f"{item.get('max_charges',20)+ACC_CHARGES_BONUS} charges)",
                              row_r.x + 10, row_r.y + 5, CREAM, 13, bold=True)
                    draw_text(surface,
                              f"{ch.name}  ·  Expansion {exps+1}/{ACC_MAX_EXPANSIONS}",
                              row_r.x + 10, row_r.y + 24, (180, 130, 255), 11)
                    btn_r = pygame.Rect(row_r.right + 10, expand_y + 7, 130, 30)
                    pygame.draw.rect(surface, (18, 12, 32), btn_r, border_radius=4)
                    pygame.draw.rect(surface, (160, 100, 240), btn_r, 1, border_radius=4)
                    draw_text(surface, "Expand", btn_r.x + 28, btn_r.y + 7, (180, 130, 255), 12)
                    self._acc_expand_btns.append((btn_r, item, ch))
                    expand_y += 50

    def _handle_spells_click(self, mx, my):
        from core.classes import get_all_resources

        # Character selector — char tabs at top of spells panel
        cx = 60
        for i, ch in enumerate(self.party):
            w = max(80, len(ch.name) * 8 + 20)
            r = pygame.Rect(cx, 80, w, 30)
            if r.collidepoint(mx, my):
                self.selected_char = i
                self.spell_selected = -1
                self.spell_target   = 0
                self._stats_inv_sel = -1    # clear cross-tab inv selection
                self.selected_item = -1
                self._give_mode = False
                return None
            cx += w + 6

        caster = self.party[self.selected_char]
        CAMP_TYPES = ("heal", "aoe_heal", "cure", "revive")
        abilities = [a for a in caster.abilities if a.get("type") in CAMP_TYPES]

        # Spell list clicks
        for row, i, ab, can in getattr(self, "_spell_rects", []):
            if row.collidepoint(mx, my):
                self.spell_selected = i
                self.spell_target = -1   # no target pre-selected — player must click one
                return None

        # Target clicks
        for trow, j in getattr(self, "_spell_target_rects", []):
            if trow.collidepoint(mx, my):
                self.spell_target = j
                return None

        # Cast button
        cast_btn = getattr(self, "_spell_cast_btn", None)
        if cast_btn and cast_btn.collidepoint(mx, my):
            if 0 <= self.spell_selected < len(abilities):
                ab = abilities[self.spell_selected]
                self._cast_camp_spell(caster, ab)

        # Recharge buttons
        from core.focus_charges import recharge_with_crystals, crystals_needed, CRYSTAL_NAME
        from core.crafting import count_material
        for btn_r, item, ch in getattr(self, "_recharge_btns", []):
            if btn_r.collidepoint(mx, my):
                needed = crystals_needed(item)
                have   = count_material(self.party, CRYSTAL_NAME)
                if have < needed:
                    self._msg(f"Need {needed} Mana Crystal{'s' if needed>1 else ''} (have {have}).")
                    return None
                gained, used = recharge_with_crystals(item, self.party)
                self._msg(f"{item.get('name','Wand')} recharged: +{gained} charges "
                          f"({used} crystal{'s' if used>1 else ''} used).")
                return None

        # Venom refill buttons
        from core.venom_charges import refill_with_vials, VENOM_VIAL_NAME
        for btn_r, item, ch in getattr(self, "_venom_refill_btns", []):
            if btn_r.collidepoint(mx, my):
                gained, used = refill_with_vials(item, self.party)
                if gained:
                    self._msg(f"{item.get('name','Weapon')} refilled: +{gained} venom charges "
                              f"({used} vial{'s' if used>1 else ''} used).")
                else:
                    self._msg(f"No {VENOM_VIAL_NAME}s in inventory.", (220, 80, 80))
                return None

        # ACC expand buttons
        from core.focus_charges import expand_with_acc
        for btn_r, item, ch in getattr(self, "_acc_expand_btns", []):
            if btn_r.collidepoint(mx, my):
                ok, msg = expand_with_acc(item, self.party)
                self._msg(msg, (180, 130, 255) if ok else (220, 80, 80))
                return None

        return None

    def _cast_camp_spell(self, caster, ability):
        """Apply a camp spell effect directly to party resources."""
        from core.classes import get_all_resources
        ab_type = ab_name = ability.get("type", "")
        rk   = ability.get("resource", "")
        cost = ability.get("cost", 0)

        # Deduct cost
        cur = caster.resources.get(rk, 0)
        if cur < cost:
            self._msg(f"Not enough {rk}!", RED)
            return
        caster.resources[rk] = cur - cost

        power  = ability.get("power", 1.0)
        # Heal amount based on caster primary stat + power
        stat   = caster.stats.get("WIS", 0) + caster.stats.get("PIE", 0)
        amount = int((stat * power * 2) + (caster.level * power * 3))

        targets = []
        ab_type_key = ability.get("type", "")
        if ab_type_key == "aoe_heal":
            targets = [c for c in self.party if c.resources.get("HP", 0) > 0]
        elif ab_type_key == "revive":
            if 0 <= self.spell_target < len(self.party):
                targets = [self.party[self.spell_target]]
        else:
            if 0 <= self.spell_target < len(self.party):
                targets = [self.party[self.spell_target]]

        if not targets:
            self._msg("Select a target first.", ORANGE)
            return

        msgs = []
        for tgt in targets:
            max_res = get_all_resources(tgt.class_name, tgt.stats, tgt.level)
            if ab_type_key == "revive":
                if tgt.resources.get("HP", 0) > 0:
                    msgs.append(f"{tgt.name} is not fallen.")
                    continue
                revive_hp = max(1, int(max_res.get("HP", 1) * 0.3))
                tgt.resources["HP"] = revive_hp
                msgs.append(f"{tgt.name} revived with {revive_hp} HP!")
            elif ab_type_key in ("heal", "aoe_heal"):
                mhp = max(1, max_res.get("HP", 1))
                old = tgt.resources.get("HP", 0)
                new_hp = min(mhp, old + amount)
                gained = new_hp - old
                tgt.resources["HP"] = new_hp
                if gained > 0:
                    msgs.append(f"{tgt.name} +{gained} HP")
                else:
                    msgs.append(f"{tgt.name} already full HP")
            elif ab_type_key == "cure":
                from core.status_effects import get_status_effects, remove_status
                effects = get_status_effects(tgt)   # creates list if missing
                cured = [e for e in effects if e.get("type") in ("poison", "disease", "curse")]
                for e in cured:
                    remove_status(tgt, e["id"])      # remove by "id", not "name"
                if cured:
                    msgs.append(f"{tgt.name}: cleared {', '.join(e['name'] for e in cured)}")
                else:
                    msgs.append(f"{tgt.name}: no status effects to cure")

        self._msg("  ".join(msgs) if msgs else "No effect.", HEAL_COL)

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

        # ── Gold transfer section ────────────────────────────────────────────
        gold_y = list_top + 14 * item_h + 12
        total_gold = sum(c.gold for c in self.party)
        draw_text(surface, f"Party Gold: {total_gold}g",
                  left_x, gold_y, DIM_GOLD, 13, bold=True)

        # Pool All / Split Evenly / Give 10g buttons
        pool_btn  = pygame.Rect(left_x + 160, gold_y - 2, 100, 22)
        split_btn = pygame.Rect(left_x + 268, gold_y - 2, 100, 22)
        give10_btn = pygame.Rect(left_x + 376, gold_y - 2, 90, 22)

        for btn, label, active in [
            (pool_btn,  "Pool All",    True),
            (split_btn, "Split Even",  len(self.party) > 1),
            (give10_btn, "Give 10g →", src.gold >= 10 and self.transfer_src_char != self.transfer_dst_char),
        ]:
            hov = btn.collidepoint(mx, my) and active
            pygame.draw.rect(surface, (30,40,20) if hov else (20,28,14), btn, border_radius=3)
            pygame.draw.rect(surface, (80,160,60) if active else DARK_GREY, btn, 1, border_radius=3)
            draw_text(surface, label, btn.x + 5, btn.y + 4,
                      (140, 220, 100) if active else DARK_GREY, 10)

        # Per-char gold display
        for i, ch in enumerate(self.party):
            draw_text(surface, f"{ch.name}: {ch.gold}g",
                      left_x + i * 180, gold_y + 26, DIM_GOLD, 11)

        self._camp_pool_btn  = pool_btn
        self._camp_split_btn = split_btn
        self._camp_give10_btn = give10_btn

        # ── Status message — below gold section ──────────────────────────────
        if self.message and self.msg_timer > 0:
            draw_text(surface, self.message, left_x, gold_y + 46,
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

        # ── Gold transfer buttons ─────────────────────────────────────────────
        if getattr(self, "_camp_pool_btn", None) and self._camp_pool_btn.collidepoint(mx, my):
            total = sum(c.gold for c in self.party)
            for c in self.party: c.gold = 0
            self.party[0].gold = total
            self.message = f"All gold ({total}g) held by {self.party[0].name}."
            self.msg_color = (200, 170, 60)
            self.msg_timer = 3000
            return None

        if getattr(self, "_camp_split_btn", None) and self._camp_split_btn.collidepoint(mx, my):
            total = sum(c.gold for c in self.party)
            share = total // len(self.party)
            rem   = total - share * len(self.party)
            for j, c in enumerate(self.party):
                c.gold = share + (rem if j == 0 else 0)
            self.message = f"Gold split: {share}g each."
            self.msg_color = (200, 170, 60)
            self.msg_timer = 3000
            return None

        if getattr(self, "_camp_give10_btn", None) and self._camp_give10_btn.collidepoint(mx, my):
            src_idx = self.transfer_src_char
            dst_idx = self.transfer_dst_char
            if src_idx != dst_idx:
                src = self.party[src_idx]
                dst = self.party[dst_idx]
                amount = min(10, src.gold)
                if amount > 0:
                    src.gold -= amount
                    dst.gold += amount
                    self.message = f"{src.name} gave {amount}g to {dst.name}."
                    self.msg_color = (200, 170, 60)
                    self.msg_timer = 3000
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
                    # Identity-based removal: two stack-1 items with same fields are
                    # == equal to list.remove, so we must pop by identity match.
                    removed = False
                    for idx, inv_item in enumerate(src.inventory):
                        if inv_item is item:
                            src.inventory.pop(idx)
                            removed = True
                            break
                    if not removed:
                        # Fallback: nothing matched by identity — use equality once
                        try:
                            src.inventory.remove(item)
                            removed = True
                        except ValueError:
                            pass
                    if removed:
                        dst.inventory.append(item)
                        self.message = f"Gave {item.get('name','item')} to {dst.name}"
                    else:
                        self.message = f"Transfer failed — item not found in inventory."
                        self.msg_color = (200, 80, 80)
                        self.msg_timer = 180
                        self.transfer_selected_item = -1
                        return None
                self.msg_color = GREEN
                self.msg_timer = 180
                self.transfer_selected_item = -1
        return None

    # ──────────────────────────────────────────────────────────
    #  INPUT HANDLING
    # ──────────────────────────────────────────────────────────

    def handle_click(self, mx, my):
        """Handle mouse click. Returns result string or None."""
        if not self.party:
            return None
        self.selected_char = max(0, min(self.selected_char, len(self.party) - 1))
        # Manual click handler (overlay consumes all clicks when open)
        if self.handle_manual_click(mx, my):
            return None
        # Manual button
        if getattr(self, "_manual_btn_rect", None) and self._manual_btn_rect.collidepoint(mx, my):
            self.toggle_manual()
            return None
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
                self._give_mode = False
                return None

        # Character reorder arrows (visible on all tabs)
        if getattr(self, "_reorder_left_rect", None) and self._reorder_left_rect.collidepoint(mx, my):
            i = self.selected_char
            if i > 0:
                self.party[i], self.party[i-1] = self.party[i-1], self.party[i]
                self.selected_char = i - 1
                self._stats_inv_sel = -1
                self.selected_item = -1
            return None
        if getattr(self, "_reorder_right_rect", None) and self._reorder_right_rect.collidepoint(mx, my):
            i = self.selected_char
            if i < len(self.party) - 1:
                self.party[i], self.party[i+1] = self.party[i+1], self.party[i]
                self.selected_char = i + 1
                self._stats_inv_sel = -1
                self.selected_item = -1
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
                    self._stats_inv_sel = -1   # reset inv selection — stale index would point at wrong character's item
                    self.scroll_offset = 0
                    self._give_mode = False
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
        elif self.tab == TAB_STATS:
            return self._handle_stats_click(mx, my)
        elif self.tab == TAB_TRANSFER:
            return self._handle_transfer_click(mx, my)
        elif self.tab == TAB_FORMATION:
            return self._handle_formation_click(mx, my)
        elif self.tab == TAB_SPELLS:
            return self._handle_spells_click(mx, my)

        return None

    def handle_key(self, key):
        """Handle keyboard input."""
        if key == pygame.K_m or key == pygame.K_F1:
            self.toggle_manual()
            return None
        if key == pygame.K_ESCAPE:
            self.finished = True
            self.result = "cancel"
            return "cancel"
        if key == pygame.K_TAB:
            self.tab = (self.tab + 1) % TAB_COUNT
            return None
        # Number keys 1-8 switch tabs directly
        _num_keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                     pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8]
        if key in _num_keys:
            idx = _num_keys.index(key)
            if idx < TAB_COUNT:
                self.tab = idx
                self.selected_item = -1
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

        # ── Item list clicks — use draw-time geometry ─────────────
        top      = 80
        list_top = top + 52
        ROW_H    = 36
        BODY_BOT = SCREEN_H - 320
        list_bot = BODY_BOT
        visible_n = max(1, (list_bot - list_top) // ROW_H)
        LIST_X   = 60
        ROW_W    = SCREEN_W - LIST_X - 26

        # Use same collapsed groups as draw — falls back to full list if not yet drawn
        groups = getattr(self, "_inv_groups", None) or _build_inv_groups(c.inventory)
        visible_groups = groups[self.scroll_offset:self.scroll_offset + visible_n]
        for i, grp in enumerate(visible_groups):
            row = pygame.Rect(LIST_X, list_top + i * ROW_H, ROW_W, ROW_H - 2)
            if row.collidepoint(mx, my):
                # Select the first inventory index in this group
                self.selected_item = grp["indices"][0]
                self._give_mode = False
                return None

        # ── Action buttons — use EXACT rects stored during draw ───
        # _inv_btn_rects and _inv_btn_by are set by _draw_inventory
        btn_rects = getattr(self, "_inv_btn_rects", {})
        by = getattr(self, "_inv_btn_by", -1)
        if by < 0 or not btn_rects:
            return None   # nothing drawn yet

        if 0 <= self.selected_item < len(c.inventory):
            item = c.inventory[self.selected_item]
            protected = item.get("type") in ("key_item", "quest_item") or "warden_rank" in item

            # Use button
            if "use" in btn_rects and btn_rects["use"].collidepoint(mx, my):
                self._give_mode = False
                self._use_item(c, self.selected_item)
                return None

            # Equip button
            if "equip" in btn_rects and btn_rects["equip"].collidepoint(mx, my):
                self._give_mode = False
                self._equip_item(c, self.selected_item)
                return None

            # Drop button
            if "drop" in btn_rects and btn_rects["drop"].collidepoint(mx, my):
                if protected:
                    self._msg(f"{item.get('name','item')} is a key item and cannot be dropped.", ORANGE)
                    return None
                self._give_mode = False
                name = item.get("name", "item")
                c.inventory.pop(self.selected_item)
                self.selected_item = -1
                self._msg(f"Dropped {name}.", ORANGE)
                return None

            # Give button
            if "give" in btn_rects and btn_rects["give"].collidepoint(mx, my):
                self._give_mode = not getattr(self, "_give_mode", False)
                return None

            # Give sub-buttons (character selection)
            if getattr(self, "_give_mode", False):
                gx = 80
                for gi, gchar in enumerate(self.party):
                    if gi == self.selected_char:
                        continue
                    gbw = max(80, len(gchar.name)*8+16)
                    if pygame.Rect(gx, by + 44, gbw, 28).collidepoint(mx, my):
                        if 0 <= self.selected_item < len(c.inventory):
                            xfer = c.inventory.pop(self.selected_item)
                            gchar.inventory.append(xfer)
                            self.selected_item = -1
                            self._give_mode = False
                            self._msg(f"Gave {xfer.get('name','item')} to {gchar.name}.", GOLD)
                        return None
                    gx += gbw + 8

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
                item = equipment.pop(slot)
                c.inventory.append(item)
                self._msg(f"Unequipped {item.get('name', 'item')}.", DIM_GOLD)
                return None
            ey += 42

        # Use draw-time stored rects — prevents stale-index crash
        for true_idx, row in getattr(self, "_equip_tab_inv_rects", []):
            if row.collidepoint(mx, my):
                self._equip_item(c, true_idx)
                return None

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

        # Healing items — accept both "heal" and "heal_amount" field conventions
        heal = item.get("heal", item.get("heal_amount", 0))
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
        # ── Spell scroll (subtype="scroll" with a "spell" or "effect" field) ──
        elif item.get("subtype") == "scroll" and item.get("spell"):
            spell_name = item["spell"]
            # Find the spell in any class abilities
            import abilities as _ab_root
            from core.abilities import CLASS_ABILITIES as _core_abs
            spell_ab = None
            for cls_abs in list(_ab_root.CLASS_ABILITIES.values()) + list(_core_abs.values()):
                for ab in cls_abs:
                    if ab.get("name") == spell_name:
                        spell_ab = dict(ab)
                        break
                if spell_ab:
                    break
            if not spell_ab:
                self._msg(f"Unknown spell on scroll: {spell_name}", ORANGE)
                return
            # Cast at minimal cost (scrolls bypass resource requirements)
            ab_type = spell_ab.get("type", "")
            CAMP_TYPES = ("heal", "aoe_heal", "cure", "revive")
            if ab_type in CAMP_TYPES:
                # Use the existing camp spell logic — scrolls cast for free
                spell_ab["cost"] = 0
                spell_ab["resource"] = ""
                self._cast_camp_spell(char, spell_ab)
            else:
                self._msg(f"{spell_name}: combat spell — cannot use outside battle.", ORANGE)
                return
        # ── Effect-based scrolls (Fireball, Protection, Recall) ──
        elif item.get("subtype") == "scroll" and item.get("effect"):
            _eff = item["effect"]
            if _eff == "fireball":
                # Out-of-combat fireball scrolls can't meaningfully target enemies here
                self._msg(f"{name}: must be used in combat.", ORANGE)
                return
            elif _eff == "protection":
                # Apply a party-wide protection buff (damage reduction) for 3 turns in next combat
                from core.status_effects import get_status_effects as _gse
                for member in self.party:
                    effects = _gse(member)
                    # avoid stacking
                    if not any(s.get("name") == "Protection" for s in effects):
                        effects.append({"name": "Protection", "duration": 3,
                                        "type": "combat_status", "defense_bonus": 0.25})
                self._msg(f"{name}: party gains Protection for their next battle.", HEAL_COL)
            elif _eff == "recall":
                # Dungeon-only: teleport party back to overland. In camp this is ambiguous.
                self._msg(f"{name}: recall scrolls work only from within a dungeon.", ORANGE)
                return
            else:
                self._msg(f"{name}: unknown scroll effect '{_eff}'.", ORANGE)
                return
        # ── Spell Tome: teach a spell to a compatible caster ──
        elif item.get("teaches_spell"):
            spell_name = item["teaches_spell"]
            # Check if char can learn this spell
            from core.abilities import CLASS_ABILITIES as _core_abs
            target_spell = None
            for cls_abs in _core_abs.values():
                for ab in cls_abs:
                    if ab.get("name") == spell_name:
                        target_spell = dict(ab)
                        break
                if target_spell:
                    break
            if not target_spell:
                self._msg(f"Unknown spell: {spell_name}", ORANGE)
                return
            # Check if character already knows this spell
            has_spell = any(a.get("name") == spell_name for a in getattr(char, "abilities", []))
            if has_spell:
                self._msg(f"{char.name} already knows {spell_name}.", ORANGE)
                return
            # Add to character's abilities list
            if not hasattr(char, "abilities"):
                char.abilities = []
            char.abilities.append(target_spell)
            self._msg(f"{char.name} learns {spell_name}!", HEAL_COL)
        # ── Gold pouches ──
        elif item.get("gold_value") or item.get("bonus_gold"):
            gold = item.get("gold_value", 0) + item.get("bonus_gold", 0)
            char.gold += gold
            self._msg(f"{char.name} finds {gold}g!", GOLD)
        # ── Holy Water: usable in combat only (to damage undead) ──
        elif item.get("damage_undead"):
            self._msg(f"{name}: useful only against undead in battle.", ORANGE)
            return
        # ── Cure (items with "cures" list) ──
        elif item.get("cures"):
            from core.status_effects import get_status_effects, remove_status
            cures = item["cures"] if isinstance(item["cures"], list) else [item["cures"]]
            tgt = self.party[self.spell_target] if 0 <= self.spell_target < len(self.party) else char
            effects = get_status_effects(tgt)
            cured = [e for e in effects if e.get("name") in cures or e.get("type") in cures]
            if cured:
                for e in cured:
                    remove_status(tgt, e["id"])
                self._msg(f"{tgt.name}: cleared {', '.join(e['name'] for e in cured)}", HEAL_COL)
            else:
                self._msg(f"{tgt.name}: nothing to cure.", ORANGE)
                return
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
        """Equip an item from inventory — delegates to core.equipment.equip_item
        which handles ring slot auto-detection (ring1→ring2→ring3) and all
        accessory routing correctly."""
        # Guard: stale index protection
        if item_idx < 0 or item_idx >= len(char.inventory):
            self._msg("Equip failed — stale item reference. Please re-select.", ORANGE)
            self.selected_item = -1
            return

        item = char.inventory[item_idx]
        if not item.get("slot"):
            return

        from core.equipment import equip_item as _core_equip
        success, displaced, msg = _core_equip(char, item)
        if success:
            # core.equipment already modified char.equipment; remove item from inventory
            if item in char.inventory:
                char.inventory.remove(item)
            elif item_idx < len(char.inventory):
                char.inventory.pop(item_idx)
            self.selected_item = -1
            # Displaced item goes back into inventory
            if displaced:
                char.inventory.append(displaced)
            name = item.get("name", "item")
            self._msg(f"{char.name} equipped {name}.", GOLD)
        else:
            self._msg(msg or "Cannot equip that item.", ORANGE)

    # ─────────────────────────────────────────────────────────
    #  FORMATION TAB
    # ─────────────────────────────────────────────────────────

    def _draw_formation(self, surface, mx, my, top):
        """Draw the formation editor: 3 rows (FRONT/MID/BACK), 2 player slots each."""
        from core.combat_config import FRONT, MID, BACK

        ROWS = [("BACK ROW",  BACK,  (80,  130, 200)),
                ("MID ROW",   MID,   (200, 170, 50)),
                ("FRONT ROW", FRONT, (200, 80,  80))]

        PAD       = 30
        ROW_H     = 140
        ROW_W     = SCREEN_W - PAD * 2
        SLOT_W    = 200
        SLOT_H    = 100
        SLOT_PAD  = 16

        # Store rects for click detection
        self._form_row_rects  = {}   # row_key → pygame.Rect of the row panel
        self._form_slot_rects = {}   # (row_key, slot_idx) → pygame.Rect

        y = top + 10
        draw_text(surface, "Click a character to select, then click a row slot to place them.",
                  PAD, y, GREY, 12)
        y += 22

        # Group party members (players only — no summons) by row
        from core.combat_config import ROWS as ROW_KEYS
        players = [p for p in self.party if not getattr(p, "is_summon", False)]
        summons  = [p for p in self.party if getattr(p, "is_summon", False)]

        chars_in_row = {FRONT: [], MID: [], BACK: []}
        for p in players:
            r = getattr(p, "combat_row", None) or FRONT
            if r not in chars_in_row:
                r = FRONT
            chars_in_row[r].append(p)

        for row_label, row_key, row_col in ROWS:
            panel_r = pygame.Rect(PAD, y, ROW_W, ROW_H)
            self._form_row_rects[row_key] = panel_r

            # Panel background
            bg = (28, 22, 40)
            pygame.draw.rect(surface, bg, panel_r, border_radius=6)
            border_col = row_col if self.formation_selected >= 0 else (60, 50, 80)
            pygame.draw.rect(surface, border_col, panel_r, 1, border_radius=6)

            draw_text(surface, row_label, PAD + 10, y + 8, row_col, 13, bold=True)

            # Draw 2 slots
            for slot_i in range(2):
                sx = PAD + 10 + slot_i * (SLOT_W + SLOT_PAD)
                sy = y + 28
                slot_r = pygame.Rect(sx, sy, SLOT_W, SLOT_H)
                self._form_slot_rects[(row_key, slot_i)] = slot_r

                # Find char in this slot
                chars = chars_in_row[row_key]
                char = chars[slot_i] if slot_i < len(chars) else None

                slot_hover = slot_r.collidepoint(mx, my)
                if char:
                    # Is this char selected?
                    char_idx = players.index(char)
                    is_sel = self.formation_selected == char_idx
                    slot_bg = (70, 55, 100) if is_sel else ((50, 40, 70) if slot_hover else (38, 30, 55))
                    pygame.draw.rect(surface, slot_bg, slot_r, border_radius=5)
                    sel_border = (180, 140, 255) if is_sel else (row_col if slot_hover else (80, 65, 110))
                    pygame.draw.rect(surface, sel_border, slot_r, 2, border_radius=5)

                    from core.classes import get_all_resources as _gar
                    _max_res = _gar(char.class_name, char.stats, char.level)
                    _cur_hp  = char.resources.get("HP", 0)
                    _max_hp  = max(1, _max_res.get("HP", 1))
                    hp_pct = _cur_hp / _max_hp
                    hp_col = (80, 200, 100) if hp_pct > 0.5 else (220, 160, 50) if hp_pct > 0.25 else (200, 60, 60)

                    draw_text(surface, char.name[:18],     sx + 8, sy + 8,  CREAM, 13, bold=True)
                    draw_text(surface, char.class_name or "",  sx + 8, sy + 26, GREY,  11)
                    draw_text(surface, f"HP {_cur_hp}/{_max_hp}", sx + 8, sy + 44, hp_col, 11)
                    if is_sel:
                        draw_text(surface, "SELECTED",     sx + 8, sy + 62, (180, 140, 255), 11, bold=True)
                    draw_text(surface, "Lv " + str(char.level), sx + SLOT_W - 40, sy + 8, GOLD, 11)
                else:
                    # Empty slot — highlight when a char is selected
                    if self.formation_selected >= 0:
                        slot_bg = (50, 40, 60) if slot_hover else (35, 28, 48)
                        pygame.draw.rect(surface, slot_bg, slot_r, border_radius=5)
                        pygame.draw.rect(surface, (100, 80, 140) if slot_hover else (60, 50, 80),
                                         slot_r, 1, border_radius=5)
                        draw_text(surface, "← Place here", sx + 30, sy + 38, GREY, 12)
                    else:
                        pygame.draw.rect(surface, (30, 24, 42), slot_r, border_radius=5)
                        pygame.draw.rect(surface, (55, 45, 70), slot_r, 1, border_radius=5)
                        draw_text(surface, "Empty", sx + 60, sy + 38, (70, 60, 90), 12)

            # Summons note on right side of row
            row_summons = [s for s in summons if getattr(s, "combat_row", None) == row_key]
            if row_summons:
                sx2 = PAD + 10 + 2 * (SLOT_W + SLOT_PAD) + 20
                draw_text(surface, "Summons:", sx2, y + 28, (120, 200, 120), 11, bold=True)
                for si, s in enumerate(row_summons[:2]):
                    draw_text(surface, s.get("name", "?")[:16], sx2, y + 46 + si * 18,
                              (100, 180, 100), 11)

            y += ROW_H + 10

        # Help footer
        if self.formation_selected >= 0:
            sel_name = players[self.formation_selected].name if self.formation_selected < len(players) else ""
            draw_text(surface, f"{sel_name} selected — click an empty slot or a character to swap.",
                      PAD, y + 4, (180, 140, 255), 12)
        else:
            draw_text(surface, "Max 2 characters per row. Summons occupy additional slots (chosen by the summoner).",
                      PAD, y + 4, GREY, 11)

    def _handle_formation_click(self, mx, my):
        from core.combat_config import FRONT, MID, BACK

        players = [p for p in self.party if not getattr(p, "is_summon", False)]

        # Check slot clicks
        for (row_key, slot_i), slot_r in getattr(self, "_form_slot_rects", {}).items():
            if not slot_r.collidepoint(mx, my):
                continue

            chars_in_row = {FRONT: [], MID: [], BACK: []}
            for p in players:
                r = getattr(p, "combat_row", None) or FRONT
                if r not in chars_in_row:
                    r = FRONT
                chars_in_row[r].append(p)

            chars = chars_in_row[row_key]
            occupant = chars[slot_i] if slot_i < len(chars) else None

            if self.formation_selected < 0:
                # No selection yet — select whoever is here
                if occupant:
                    self.formation_selected = players.index(occupant)
                    self._msg(f"{occupant.name} selected.", CREAM)
            else:
                mover = players[self.formation_selected]
                if occupant is None:
                    # Empty slot — just move
                    mover.combat_row = row_key
                    self.formation_selected = -1
                    self._msg(f"{mover.name} moved to {row_key} row.", GOLD)
                elif occupant is mover:
                    # Clicked self — deselect
                    self.formation_selected = -1
                elif len(chars_in_row[row_key]) < 2 or occupant:
                    # Swap the two characters
                    mover_row    = getattr(mover, "combat_row", None) or FRONT
                    occupant_row = getattr(occupant, "combat_row", None) or FRONT
                    mover.combat_row    = occupant_row
                    occupant.combat_row = mover_row
                    self.formation_selected = -1
                    self._msg(f"Swapped {mover.name} ↔ {occupant.name}.", GOLD)
                else:
                    # Row already has 2 — can't place
                    self._msg(f"{row_key.capitalize()} row is full (max 2).", (200, 80, 80))
            return None

        # Click outside all slots — deselect
        self.formation_selected = -1
        return None
