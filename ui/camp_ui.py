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
            draw_text(surface, "Restores 25% HP, all SP/MP/Ki",
                      SCREEN_W // 2 - 115, top + 52, GREY, 13)
        else:
            draw_text(surface, "Ambush risk: Low", SCREEN_W // 2 - 60, top + 30, GREEN, 14)
            draw_text(surface, "Restores 40% HP, all SP/MP/Ki",
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

            # ── Item details panel ──────────────────────────
            self._draw_item_details(surface, item, by + 50)

    def _draw_item_details(self, surface, item, y):
        """Draw item attribute panel for a selected item."""
        from core.identification import get_item_display_name
        if not item:
            return

        identified = item.get("identified", True)
        panel = pygame.Rect(80, y, SCREEN_W - 160, 160)
        pygame.draw.rect(surface, (18, 14, 30), panel, border_radius=5)
        pygame.draw.rect(surface, EQUIP_SLOT_BORDER, panel, 1, border_radius=5)

        x, dy = panel.x + 14, panel.y + 10
        draw_text(surface, get_item_display_name(item), x, dy, GOLD, 14, bold=True)
        dy += 22

        if not identified:
            draw_text(surface, item.get("unidentified_desc", "Properties unknown."), x, dy, GREY, 12)
            dy += 18
            draw_text(surface, "[Unidentified — use Identify tab to appraise]", x, dy, ORANGE, 11)
            return

        # Description
        desc = item.get("description", "")
        if desc:
            draw_text(surface, desc, x, dy, GREY, 12)
            dy += 18

        # Type-specific stats
        itype = item.get("type", "")
        col2 = panel.x + panel.width // 2

        if itype == "weapon":
            base = item.get("damage", 0)
            ds   = item.get("damage_stat", {})
            ds_str = ", ".join(f"{k}×{v}" for k,v in ds.items()) if ds else "none"
            draw_text(surface, f"Damage: {base} base  |  Stat scaling: {ds_str}", x, dy, STAT_VAL, 12)
            dy += 16
            mods = []
            if item.get("accuracy_mod"): mods.append(f"Acc {item['accuracy_mod']:+d}%")
            if item.get("crit_mod"):     mods.append(f"Crit {item['crit_mod']:+d}%")
            if item.get("speed_mod"):    mods.append(f"Speed {item['speed_mod']:+d}")
            if item.get("spell_bonus"):  mods.append(f"+{item['spell_bonus']} Spell Power")
            if mods:
                draw_text(surface, "  ".join(mods), x, dy, STAT_LABEL, 11)
                dy += 16

        elif itype == "armor":
            draw_text(surface, f"Defense: {item.get('defense', 0)}  Magic Resist: {item.get('magic_resist', 0)}", x, dy, STAT_VAL, 12)
            dy += 16

        # Stat bonuses
        stat_bonuses = item.get("stat_bonuses", {})
        if stat_bonuses:
            bonuses = ", ".join(f"{k} {v:+d}" for k,v in stat_bonuses.items() if v)
            draw_text(surface, f"Bonuses: {bonuses}", x, dy, (140, 220, 160), 12)
            dy += 16

        # Enchant
        if item.get("enchant_element"):
            draw_text(surface, f"Enchant: {item['enchant_element'].title()} +{item.get('enchant_bonus',0)}",
                      x, dy, (180, 140, 255), 12)
            dy += 16

        # Rarity and value
        rarity = item.get("rarity", "").title()
        value  = item.get("estimated_value", item.get("sell_price", 0))
        draw_text(surface, f"{rarity}  |  Value: ~{value}g", x, dy, DIM_GOLD, 11)

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


    # ────────────────────────────────────────────────────────────────────────
    #  PARTY STATS TAB  (complete rewrite)
    # ────────────────────────────────────────────────────────────────────────

    def _draw_stats(self, surface, mx, my, top):
        """Rich party stats panel: tier badge, effective stats, resistances,
        known abilities/spells with scrollable descriptions."""
        self._draw_char_selector(surface, mx, my, top)
        c = self.party[self.selected_char]

        from core.classes import get_all_resources, STAT_NAMES
        from core.progression import PLANAR_TIERS, get_party_tier

        # ── Layout constants ───────────────────────────────────────────────
        LEFT_X   = 30
        MID_X    = 430
        RIGHT_X  = 850
        BODY_TOP = top + 52        # below char selector
        BODY_BOT = SCREEN_H - 60  # leave room for Manual button
        CONTENT_H = BODY_BOT - BODY_TOP

        # ── Clipping region for scroll ─────────────────────────────────────
        clip = pygame.Rect(0, BODY_TOP, SCREEN_W, CONTENT_H)
        surface.set_clip(clip)

        # ─────────────────────────────────────────────────────────────────
        #  LEFT COLUMN: Tier badge + Base stats + Resources + Resistances
        # ─────────────────────────────────────────────────────────────────
        y = BODY_TOP + 4

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
                  LEFT_X, y, CREAM, 13)
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
            bg_col = (14, 11, 22) if not is_locked else (10, 8, 16)
            pygame.draw.rect(surface, bg_col, card_rect, border_radius=4)

            ab_type = ab.get("type","attack")
            type_col = TYPE_COLORS.get(ab_type, GREY)
            if is_locked: type_col = (60,55,70)
            pygame.draw.rect(surface, type_col if not is_locked else (40,35,55),
                             card_rect, 1, border_radius=4)

            # Name + level unlock
            name_col = CREAM if not is_locked else (80,75,90)
            draw_text(surface, ab.get("name","?"), col_x + 8, ry2 + 5, name_col, 13, bold=not is_locked)

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

                # Cost
                cost = ab.get("cost", 0)
                res_key = ab.get("resource","STR-SP")
                if cost:
                    draw_text(surface, f"Cost: {cost} {res_key}",
                              col_x + 8, ry2 + 20, (160,140,100), 11)

                # Description
                desc = ab.get("desc") or ab.get("description","")
                if desc:
                    draw_text(surface, desc, col_x + 8, ry2 + 33,
                              GREY, 11, max_width=col_w - 16)

            ry2 += ROW_H

        # ─────────────────────────────────────────────────────────────────
        #  RIGHT COLUMN: Equipment summary
        # ─────────────────────────────────────────────────────────────────
        ex = RIGHT_X
        ey = BODY_TOP + 4

        draw_text(surface, "EQUIPPED", ex, ey, STAT_LABEL, 10, bold=True)
        ey += 16

        from core.equipment import SLOT_NAMES
        EQUIP_DISPLAY = [
            ("weapon","Weapon"), ("off_hand","Off-Hand"),
            ("head","Head"), ("crown","Crown"), ("body","Body"),
            ("hands","Hands"), ("feet","Feet"), ("neck","Neck"),
            ("ring1","Ring 1"), ("ring2","Ring 2"), ("ring3","Ring 3"),
        ]
        for slot_key, slot_label in EQUIP_DISPLAY:
            item = c.equipment.get(slot_key) if hasattr(c,"equipment") else None
            draw_text(surface, f"{slot_label}:", ex, ey, STAT_LABEL, 11)
            if item:
                iname = item.get("name","?")
                rar = item.get("rarity","")
                RAR_COL = {"common":CREAM,"uncommon":(140,200,255),
                           "rare":(180,120,255),"epic":(255,180,60)}.get(rar, CREAM)
                draw_text(surface, iname[:22], ex + 72, ey, RAR_COL, 11)
                # Show main bonus
                sb = item.get("stat_bonuses",{})
                if sb:
                    bonus_str = "  ".join(f"+{v}{k}" for k,v in list(sb.items())[:2])
                    draw_text(surface, bonus_str, ex + 72, ey + 12, (120,180,120), 10)
            else:
                draw_text(surface, "—", ex + 72, ey, (50,45,65), 11)
            ey += 28 if item and item.get("stat_bonuses") else 16

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
        """Handle clicks on the stats tab (ability scroll, manual)."""
        pass  # scroll handled by handle_scroll

    def handle_scroll(self, direction):
        """Handle mousewheel scrolling."""
        if self.tab == TAB_STATS:
            cur = getattr(self, "_stats_scroll", 0)
            self._stats_scroll = max(0, cur + direction * 24)
        elif self.tab == TAB_INVENTORY:
            self.scroll_offset = max(0, self.scroll_offset + direction)
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

    def _handle_spells_click(self, mx, my):
        from core.classes import get_all_resources
        caster = self.party[self.selected_char]
        CAMP_TYPES = ("heal", "aoe_heal", "cure", "revive")
        abilities = [a for a in caster.abilities if a.get("type") in CAMP_TYPES]

        # Spell list clicks
        for row, i, ab, can in getattr(self, "_spell_rects", []):
            if row.collidepoint(mx, my):
                self.spell_selected = i
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
            self._msg("No valid target.", ORANGE)
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
                from core.status_effects import get_status_effects, remove_status_effect
                effects = get_status_effects(tgt) if hasattr(tgt, "_status_effects") else []
                cured = [e for e in effects if e.get("type") in ("poison", "disease", "curse")]
                for e in cured:
                    remove_status_effect(tgt, e["name"])
                msgs.append(f"{tgt.name}: {len(cured)} effect(s) cured")

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
