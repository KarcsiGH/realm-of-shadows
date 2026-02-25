"""
Realm of Shadows — Inventory & Equipment UI
Accessible from the party screen. Shows equipment slots, inventory list,
and allows equip/unequip/swap/transfer.

Controls:
  Left-click equipped slot  → unequip that item
  Left-click inventory item → equip it (if equippable)
  Right-click inventory item → enter "give to" mode, then click a character tab
  ESC → cancel give-to mode or exit inventory
"""
import pygame
from ui.renderer import *
from core.equipment import (
    SLOT_ORDER, SLOT_NAMES, can_equip, equip_item, unequip_item,
    calc_equipment_defense, calc_equipment_magic_resist,
    calc_equipment_speed, calc_equipment_stat_bonuses,
)
from core.classes import CLASSES, STAT_NAMES, STAT_FULL_NAMES, get_all_resources
from core.identification import (
    get_item_display_name, get_item_display_desc,
    needs_identification, get_identify_options, attempt_identify,
)
from core.combat_engine import make_player_combatant

# ═══════════════════════════════════════════════════════════════
#  COLORS
# ═══════════════════════════════════════════════════════════════

SLOT_BG       = (25, 20, 45)
SLOT_HOVER    = (45, 38, 75)
SLOT_SELECTED = (55, 45, 90)
SLOT_FILLED   = (30, 28, 55)
SLOT_EMPTY    = (18, 15, 30)
INV_BG        = (15, 12, 28)
EQUIP_COL     = (80, 180, 255)
STAT_UP       = (80, 255, 120)
STAT_DOWN     = (255, 80, 80)

RARITY_COLORS = {
    "common":    CREAM,
    "uncommon":  (80, 220, 80),
    "rare":      (80, 140, 255),
    "epic":      (180, 80, 255),
    "legendary": (255, 180, 40),
}


# ═══════════════════════════════════════════════════════════════
#  ITEM SLOT DETECTION
# ═══════════════════════════════════════════════════════════════

def resolve_item_slot(item):
    """Figure out which equipment slot an item belongs to.
    Handles items with explicit 'slot' fields AND loot items
    that only have 'type'/'subtype'."""
    slot = item.get("slot", "")
    if slot and slot in SLOT_ORDER:
        return slot
    if slot == "accessory":
        return "accessory1"

    item_type = item.get("type", "")
    if item_type == "weapon":
        return "weapon"
    elif item_type == "shield":
        return "off_hand"
    elif item_type == "armor":
        # Check subtype and armor_slot for specific armor pieces
        subtype = item.get("subtype", "")
        armor_slot = item.get("armor_slot", "")
        if subtype in ("helmet", "helm", "head") or armor_slot == "head":
            return "head"
        elif subtype in ("gloves", "gauntlets", "hands") or armor_slot == "hands":
            return "hands"
        elif subtype in ("boots", "greaves", "feet") or armor_slot == "feet":
            return "feet"
        elif subtype in ("shield",) or armor_slot == "off_hand":
            return "off_hand"
        return armor_slot if armor_slot else "body"
    elif item_type == "accessory":
        return "accessory1"
    elif item_type in ("helmet", "head"):
        return "head"
    elif item_type in ("gloves", "hands"):
        return "hands"
    elif item_type in ("boots", "feet"):
        return "feet"

    return ""


def item_is_equippable(item):
    """Check if an item can go in an equipment slot."""
    return resolve_item_slot(item) != ""


# ═══════════════════════════════════════════════════════════════
#  INVENTORY UI CLASS
# ═══════════════════════════════════════════════════════════════

class InventoryUI:
    """Full-screen inventory and equipment management."""

    def __init__(self, party):
        self.party = party
        self.selected_char = 0
        self.selected_slot = -1
        self.selected_inv_item = -1
        self.inv_scroll = 0
        self.mode = "normal"          # normal, give_to, identify
        self.give_item = None
        self.identify_item = None     # item pending identification
        self.identify_item_idx = -1   # index in current char's inventory
        self.identify_char_options = []  # [(char_idx, combatant, options), ...]
        self.message = ""
        self.message_timer = 0
        self.message_color = CREAM
        self.finished = False

    # ─────────────────────────────────────────────────────────
    #  DRAWING
    # ─────────────────────────────────────────────────────────

    def draw(self, surface, mx, my, dt):
        self.message_timer = max(0, self.message_timer - dt)
        surface.fill(BG_COLOR)

        char = self.party[self.selected_char]
        cls = CLASSES[char.class_name]

        # ── Header ──
        draw_text(surface, "Equipment & Inventory", 20, 12, GOLD, 22, bold=True)
        back_btn = pygame.Rect(SCREEN_W - 160, 8, 140, 36)
        draw_button(surface, back_btn, "Back to Party",
                    hover=back_btn.collidepoint(mx, my), size=13)

        # ── Character tabs ──
        self._draw_char_tabs(surface, mx, my)

        # ── Give-to / Identify banner ──
        content_y = 100
        if self.mode == "give_to" and self.give_item:
            banner = pygame.Rect(20, 92, SCREEN_W - 40, 28)
            pygame.draw.rect(surface, (50, 35, 15), banner, border_radius=3)
            pygame.draw.rect(surface, ORANGE, banner, 2, border_radius=3)
            name = get_item_display_name(self.give_item)
            draw_text(surface,
                      f"Click a character tab to give: {name}   (ESC to cancel)",
                      banner.x + 12, banner.y + 6, ORANGE, 13)
            content_y = 126
        elif self.mode == "identify" and self.identify_item:
            banner = pygame.Rect(20, 92, SCREEN_W - 40, 28)
            pygame.draw.rect(surface, (20, 30, 55), banner, border_radius=3)
            pygame.draw.rect(surface, HIGHLIGHT, banner, 2, border_radius=3)
            name = get_item_display_name(self.identify_item)
            draw_text(surface,
                      f"Identify: {name}   — choose a method below   (ESC to cancel)",
                      banner.x + 12, banner.y + 6, HIGHLIGHT, 13)
            content_y = 126

        # ── Left: Equipment slots ──
        self._draw_equipment(surface, mx, my, char, content_y)

        # ── Stat summary ──
        self._draw_stat_summary(surface, char, content_y + 480)

        # ── Right: Inventory ──
        self._draw_inventory(surface, mx, my, char, content_y)

        # ── Identify panel (overlays bottom when active) ──
        if self.mode == "identify" and self.identify_item:
            self._draw_identify_panel(surface, mx, my)

        # ── Message bar ──
        if self.message and self.message_timer > 0:
            draw_text(surface, self.message, SCREEN_W // 2 - 200,
                      SCREEN_H - 30, self.message_color, 15)

    def _draw_identify_panel(self, surface, mx, my):
        """Bottom overlay panel: shows which characters can identify and at what cost."""
        ph = 160
        panel = pygame.Rect(20, SCREEN_H - ph - 10, SCREEN_W - 40, ph)
        pygame.draw.rect(surface, (14, 18, 38), panel, border_radius=6)
        pygame.draw.rect(surface, HIGHLIGHT, panel, 2, border_radius=6)

        draw_text(surface, "Who identifies it?", panel.x + 16, panel.y + 10,
                  HIGHLIGHT, 15, bold=True)

        self._identify_buttons = []
        x = panel.x + 16
        for ci, combatant, options in self.identify_char_options:
            char = self.party[ci]
            col_w = 220
            # Character name
            draw_text(surface, f"{char.name} ({char.class_name})",
                      x, panel.y + 36, CREAM, 13, bold=True)

            if not options:
                draw_text(surface, "No identify skills", x, panel.y + 56,
                          DARK_GREY, 11)
            else:
                for oi, opt in enumerate(options):
                    by = panel.y + 56 + oi * 38
                    can = opt["can_afford"]
                    btn = pygame.Rect(x, by, col_w - 16, 32)
                    hover = btn.collidepoint(mx, my) and can
                    bg = (40, 60, 100) if hover else (25, 22, 44)
                    border = HIGHLIGHT if hover else (70, 60, 110)
                    if not can:
                        bg = (20, 18, 32)
                        border = DARK_GREY
                    pygame.draw.rect(surface, bg, btn, border_radius=3)
                    pygame.draw.rect(surface, border, btn, 2, border_radius=3)
                    lbl_col = CREAM if can else DARK_GREY
                    draw_text(surface, opt["name"], btn.x + 8, btn.y + 4,
                              lbl_col, 12, bold=True)
                    draw_text(surface, opt["description"], btn.x + 8, btn.y + 18,
                              GREY if can else DARK_GREY, 10)
                    if can:
                        self._identify_buttons.append((btn, ci, combatant, opt))
            x += col_w

        draw_text(surface, "ESC to cancel",
                  panel.x + panel.width - 120, panel.y + panel.height - 20,
                  DARK_GREY, 11)

    def _draw_char_tabs(self, surface, mx, my):
        tab_y = 50
        for i, ch in enumerate(self.party):
            cl = CLASSES[ch.class_name]
            tab_w = (SCREEN_W - 40) // len(self.party)
            tab_rect = pygame.Rect(20 + i * tab_w, tab_y, tab_w - 4, 36)
            is_sel = (i == self.selected_char)
            is_hover = tab_rect.collidepoint(mx, my)

            if self.mode == "give_to" and not is_sel:
                bg = (40, 30, 20) if is_hover else (30, 22, 15)
                border = ORANGE if is_hover else DIM_GOLD
            elif is_sel:
                bg = (50, 40, 85)
                border = cl["color"]
            elif is_hover:
                bg = (35, 30, 60)
                border = HIGHLIGHT
            else:
                bg = (20, 18, 36)
                border = PANEL_BORDER

            pygame.draw.rect(surface, bg, tab_rect, border_radius=3)
            pygame.draw.rect(surface, border, tab_rect, 2, border_radius=3)

            label = f"{ch.name} ({ch.class_name})"
            if self.mode == "give_to" and not is_sel and is_hover:
                label += " <- Give"
            draw_text(surface, label, tab_rect.x + 8, tab_rect.y + 9,
                      cl["color"] if is_sel else GREY, 13, bold=is_sel)

    def _draw_equipment(self, surface, mx, my, char, top_y):
        panel = pygame.Rect(20, top_y, 420, 470)
        draw_panel(surface, panel, bg_color=INV_BG)
        draw_text(surface, "Equipment", panel.x + 12, panel.y + 8, GOLD, 16, bold=True)
        draw_text(surface, "Click a slot to unequip", panel.x + 160, panel.y + 10,
                  DARK_GREY, 11)

        slot_y = panel.y + 35
        for si, slot_key in enumerate(SLOT_ORDER):
            rect = pygame.Rect(panel.x + 8, slot_y, panel.width - 16, 48)
            item = char.equipment.get(slot_key) if char.equipment else None
            is_hover = rect.collidepoint(mx, my)

            if is_hover and item:
                bg = SLOT_HOVER
                border = HIGHLIGHT
            elif item:
                bg = SLOT_FILLED
                border = PANEL_BORDER
            else:
                bg = SLOT_EMPTY
                border = (40, 35, 55)

            pygame.draw.rect(surface, bg, rect, border_radius=3)
            pygame.draw.rect(surface, border, rect, 2, border_radius=3)

            slot_name = SLOT_NAMES.get(slot_key, slot_key)
            draw_text(surface, slot_name, rect.x + 8, rect.y + 4, DIM_GOLD, 12)

            if item:
                rarity = item.get("rarity", "common")
                name_col = RARITY_COLORS.get(rarity, CREAM)
                # Cursed items glow sickly purple when identified
                is_cursed_known = item.get("cursed") and item.get("identified") and not item.get("curse_lifted")
                if is_cursed_known:
                    name_col = (180, 80, 220)  # curse purple
                draw_text(surface, get_item_display_name(item),
                          rect.x + 100, rect.y + 4, name_col, 14, bold=True)
                if is_cursed_known:
                    draw_text(surface, "★ CURSED", rect.x + 100, rect.y + 44, (180, 80, 220), 10)

                parts = []
                if item.get("defense", 0):
                    parts.append(f"DEF +{item['defense']}")
                if item.get("magic_resist", 0):
                    parts.append(f"MRES +{item['magic_resist']}")
                if item.get("speed_mod", 0):
                    s = "+" if item["speed_mod"] > 0 else ""
                    parts.append(f"SPD {s}{item['speed_mod']}")
                for stat, val in item.get("stat_bonuses", {}).items():
                    parts.append(f"{stat} +{val}")
                if item.get("damage"):
                    parts.append(f"DMG {item['damage']}")
                if parts:
                    draw_text(surface, "  ".join(parts),
                              rect.x + 100, rect.y + 26, GREY, 11)

                if is_hover:
                    draw_text(surface, "[unequip]",
                              rect.x + rect.width - 70, rect.y + 4, DARK_GREY, 10)
            else:
                draw_text(surface, "- empty -", rect.x + 100, rect.y + 16,
                          DARK_GREY, 13)

            slot_y += 52

    def _draw_stat_summary(self, surface, char, top_y):
        panel = pygame.Rect(20, top_y, 420, 180)
        draw_panel(surface, panel, bg_color=INV_BG)
        draw_text(surface, "Combat Stats", panel.x + 12, panel.y + 8,
                  GOLD, 14, bold=True)

        from core.combat_config import DEF_CON_MULT, MRES_WIS_MULT
        from data.weapons import STARTING_WEAPONS, get_weapon

        # Defense / AC
        base_def = int(char.stats["CON"] * DEF_CON_MULT)
        eq_def = calc_equipment_defense(char)
        total_def = base_def + eq_def
        base_mr = int(char.stats["WIS"] * MRES_WIS_MULT)
        eq_mr = calc_equipment_magic_resist(char)
        eq_spd = calc_equipment_speed(char)
        eq_stats = calc_equipment_stat_bonuses(char)

        # Weapon stats
        weapon = char.equipment.get("weapon")
        if not weapon:
            wkey = STARTING_WEAPONS.get(char.class_name, "Unarmed")
            weapon = get_weapon(wkey)
        eff_stats = char.effective_stats()
        stat_dmg = 0
        for stat_key, weight in weapon.get("damage_stat", {}).items():
            stat_dmg += eff_stats.get(stat_key, 0) * weight
        weapon_base = weapon.get("damage", 0)
        raw_dmg = stat_dmg + weapon_base
        # Approximate range using variance (0.85-1.15)
        dmg_low = max(1, int(raw_dmg * 0.85))
        dmg_high = int(raw_dmg * 1.15)

        # To-hit: base 75% + accuracy_mod + DEX scaling (shown vs avg enemy DEX 10)
        from core.combat_config import ACCURACY_BASE_PHYSICAL, ACCURACY_DEX_SCALE
        acc_mod = weapon.get("accuracy_mod", 0)
        dex_val = eff_stats.get("DEX", 10)
        # Show vs average enemy DEX of 10
        dex_diff_bonus = int((dex_val - 10) * ACCURACY_DEX_SCALE)
        to_hit = min(95, max(25, ACCURACY_BASE_PHYSICAL + acc_mod + dex_diff_bonus))

        sy = panel.y + 28
        # Row 1: AC and To-Hit
        draw_text(surface, f"AC (Defense): {total_def}", panel.x + 12, sy, CREAM, 13)
        draw_text(surface, f"({base_def} base + {eq_def} armor)", panel.x + 150, sy, DARK_GREY, 11)
        sy += 18
        draw_text(surface, f"Magic Resist: {base_mr + eq_mr}", panel.x + 12, sy, CREAM, 13)
        draw_text(surface, f"({base_mr} base + {eq_mr} equip)", panel.x + 150, sy, DARK_GREY, 11)
        sy += 22

        # Row 2: Weapon damage
        wname = weapon.get("name", "Unarmed")
        draw_text(surface, f"Weapon: {wname}", panel.x + 12, sy, EQUIP_COL, 13, bold=True)
        sy += 18
        draw_text(surface, f"Damage: {dmg_low}-{dmg_high}", panel.x + 12, sy, CREAM, 13)
        draw_text(surface, f"(stat {stat_dmg:.0f} + base {weapon_base})", panel.x + 140, sy, DARK_GREY, 11)
        sy += 18
        draw_text(surface, f"To-Hit: {to_hit}%", panel.x + 12, sy, CREAM, 13)
        draw_text(surface, f"(base {ACCURACY_BASE_PHYSICAL} + weap {acc_mod:+d} + DEX {dex_diff_bonus:+d})", panel.x + 110, sy, DARK_GREY, 11)
        sy += 22

        # Row 3: Speed and stat bonuses
        if eq_spd:
            s = "+" if eq_spd > 0 else ""
            draw_text(surface, f"Speed modifier: {s}{eq_spd}",
                      panel.x + 12, sy, CREAM, 13)
            sy += 18
        if eq_stats:
            parts = [f"{st} +{v}" for st, v in eq_stats.items()]
            draw_text(surface, f"Stat bonuses: {', '.join(parts)}",
                      panel.x + 12, sy, STAT_UP, 13)

    def _draw_inventory(self, surface, mx, my, char, top_y):
        panel = pygame.Rect(460, top_y, SCREEN_W - 480, 660)
        draw_panel(surface, panel, bg_color=INV_BG)
        draw_text(surface, f"Inventory ({len(char.inventory)})  |  Gold: {char.gold}",
                  panel.x + 12, panel.y + 8, GOLD, 16, bold=True)
        draw_text(surface, "Left=Equip  Right=Give", panel.x + panel.width - 180,
                  panel.y + 10, DARK_GREY, 11)

        if not char.inventory:
            draw_text(surface, "Inventory is empty.",
                      panel.x + 20, panel.y + 45, DARK_GREY, 15)
            return

        iy = panel.y + 35
        max_vis = 9
        start = self.inv_scroll
        end = min(len(char.inventory), start + max_vis)

        if self.inv_scroll > 0:
            draw_text(surface, "^ scroll up",
                      panel.x + panel.width // 2 - 40, iy - 14, DIM_GOLD, 11)

        for idx in range(start, end):
            item = char.inventory[idx]
            rect = pygame.Rect(panel.x + 8, iy, panel.width - 16, 64)
            is_hover = rect.collidepoint(mx, my)
            equippable = item_is_equippable(item)

            if is_hover:
                bg = SLOT_HOVER
                border = HIGHLIGHT
            else:
                bg = (22, 18, 40)
                border = PANEL_BORDER

            pygame.draw.rect(surface, bg, rect, border_radius=3)
            pygame.draw.rect(surface, border, rect, 2, border_radius=3)

            display_name = get_item_display_name(item)
            stack = item.get("stack", 1)
            if stack > 1:
                display_name = f"{display_name} x{stack}"
            rarity = item.get("rarity", "common")
            name_col = RARITY_COLORS.get(rarity, CREAM) if item.get("identified") else GREY
            draw_text(surface, display_name, rect.x + 10, rect.y + 4,
                      name_col, 14, bold=True)

            # Type label
            item_type = item.get("type", "misc")
            slot = resolve_item_slot(item)
            type_str = item_type
            if slot:
                type_str += f" [{slot}]"
            draw_text(surface, type_str, rect.x + 10, rect.y + 22, DARK_GREY, 11)

            # Stats
            parts = []
            if item.get("damage"):
                parts.append(f"DMG {item['damage']}")
            if item.get("defense", 0):
                parts.append(f"DEF +{item['defense']}")
            for stat, val in item.get("stat_bonuses", {}).items():
                parts.append(f"{stat} +{val}")
            if parts:
                draw_text(surface, "  ".join(parts),
                          rect.x + 10, rect.y + 38, GREY, 11)

            # Unidentified badge
            if needs_identification(item):
                draw_text(surface, "?? Unidentified",
                          rect.x + 10, rect.y + 38, (180, 120, 220), 11)

            # Hover hints
            if is_hover:
                hx = rect.x + rect.width - 10
                is_consumable = item.get("type") in ("consumable", "potion", "food") or item.get("subtype") in ("potion", "scroll", "food")
                if is_consumable:
                    lbl = "L-Click: Use"
                    draw_text(surface, lbl, hx - get_font(11).size(lbl)[0],
                              rect.y + 4, HEAL_COL, 11)
                elif equippable:
                    lbl = "L-Click: Equip"
                    draw_text(surface, lbl, hx - get_font(11).size(lbl)[0],
                              rect.y + 4, EQUIP_COL, 11)
                lbl2 = "R-Click: Give"
                draw_text(surface, lbl2, hx - get_font(11).size(lbl2)[0],
                          rect.y + 48, DIM_GOLD, 11)
                if needs_identification(item):
                    lbl3 = "M-Click: Identify"
                    draw_text(surface, lbl3, hx - get_font(11).size(lbl3)[0],
                              rect.y + 26, (180, 120, 220), 11)

            iy += 68

        if end < len(char.inventory):
            draw_text(surface, "v scroll down",
                      panel.x + panel.width // 2 - 45, iy + 4, DIM_GOLD, 11)

    # ─────────────────────────────────────────────────────────
    #  EVENT HANDLING
    # ─────────────────────────────────────────────────────────

    def handle_click(self, mx, my, button=1):
        """Handle mouse click. button: 1=left, 2=middle, 3=right.
        Returns 'back' to exit inventory."""
        char = self.party[self.selected_char]

        # Back button
        back_btn = pygame.Rect(SCREEN_W - 160, 8, 140, 36)
        if back_btn.collidepoint(mx, my):
            self.finished = True
            return "back"

        # ── Identify mode — check identify panel buttons ──
        if self.mode == "identify" and self.identify_item:
            for btn, ci, combatant, opt in getattr(self, "_identify_buttons", []):
                if btn.collidepoint(mx, my) and opt["can_afford"]:
                    results, all_ok = attempt_identify(combatant, self.identify_item, opt["action"])
                    # Sync resources back to character object
                    char_obj = self.party[ci]
                    char_obj.resources = dict(combatant["resources"])
                    # Compose result message
                    msgs = [f"{name}: {'✓' if ok else '✗'} {msg}"
                            for name, ok, msg in results]
                    if self.identify_item.get("identified"):
                        from core.party_knowledge import mark_item_identified
                        mark_item_identified(self.identify_item.get("name", ""))
                        self._show_message("Identified! " + " | ".join(msgs), (100, 220, 100))
                    else:
                        self._show_message(" | ".join(msgs), (220, 180, 80))
                    self.mode = "normal"
                    self.identify_item = None
                    self.identify_item_idx = -1
                    return None
            # Click outside panel → cancel
            self.mode = "normal"
            self.identify_item = None
            self.identify_item_idx = -1
            return None

        # ── Give-to mode ──
        if self.mode == "give_to" and self.give_item:
            tab_y = 50
            for i in range(len(self.party)):
                if i == self.selected_char:
                    continue
                tab_w = (SCREEN_W - 40) // len(self.party)
                tab_rect = pygame.Rect(20 + i * tab_w, tab_y, tab_w - 4, 36)
                if tab_rect.collidepoint(mx, my):
                    target = self.party[i]
                    if self.give_item in char.inventory:
                        char.inventory.remove(self.give_item)
                        target.add_item(self.give_item)
                        name = get_item_display_name(self.give_item)
                        self._show_message(f"Gave {name} to {target.name}", STAT_UP)
                    self.mode = "normal"
                    self.give_item = None
                    return None
            # Click elsewhere cancels
            self.mode = "normal"
            self.give_item = None
            return None

        # ── Character tabs (normal mode) ──
        tab_y = 50
        for i in range(len(self.party)):
            tab_w = (SCREEN_W - 40) // len(self.party)
            tab_rect = pygame.Rect(20 + i * tab_w, tab_y, tab_w - 4, 36)
            if tab_rect.collidepoint(mx, my):
                self.selected_char = i
                self.selected_slot = -1
                self.selected_inv_item = -1
                self.inv_scroll = 0
                return None

        content_y = 100

        # ── Equipment slot clicks → unequip ──
        panel_l = pygame.Rect(20, content_y, 420, 470)
        slot_y = panel_l.y + 35
        for si, slot_key in enumerate(SLOT_ORDER):
            rect = pygame.Rect(panel_l.x + 8, slot_y, panel_l.width - 16, 48)
            if rect.collidepoint(mx, my):
                item = char.equipment.get(slot_key) if char.equipment else None
                if item:
                    ok, unequipped, msg = unequip_item(char, slot_key)
                    self._show_message(msg, CREAM if ok else STAT_DOWN)
                return None
            slot_y += 52

        # ── Inventory clicks ──
        panel_r = pygame.Rect(460, content_y, SCREEN_W - 480, 660)
        if char.inventory:
            iy = panel_r.y + 35
            max_vis = 9
            start = self.inv_scroll
            end = min(len(char.inventory), start + max_vis)
            for idx in range(start, end):
                item = char.inventory[idx]
                rect = pygame.Rect(panel_r.x + 8, iy, panel_r.width - 16, 64)
                if rect.collidepoint(mx, my):
                    if button == 3:
                        # Right-click → give to another character
                        self.mode = "give_to"
                        self.give_item = item
                        name = get_item_display_name(item)
                        self._show_message(f"Click a character to give: {name}", DIM_GOLD)
                        return None
                    elif button == 2:
                        # Middle-click → identify panel
                        if needs_identification(item):
                            self._enter_identify_mode(item, idx)
                        else:
                            self._show_message("Item is already identified.", DARK_GREY)
                        return None
                    else:
                        # Left-click → use if consumable, otherwise equip
                        is_consumable = item.get("type") in ("consumable", "potion", "food") or item.get("subtype") in ("potion", "scroll", "food")
                        if is_consumable:
                            msg, col = self._use_consumable(char, idx)
                            self._show_message(msg, col)
                        else:
                            slot = resolve_item_slot(item)
                            if slot:
                                item["slot"] = slot
                                ok, old_item, msg = equip_item(char, item, slot)
                                self._show_message(msg, EQUIP_COL if ok else STAT_DOWN)
                            else:
                                self._show_message("This item cannot be equipped", DARK_GREY)
                    return None
                iy += 68

        return None

    def handle_event(self, event):
        """Handle raw pygame events (ESC key)."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self.mode == "give_to":
                self.mode = "normal"
                self.give_item = None
                return None
            if self.mode == "identify":
                self.mode = "normal"
                self.identify_item = None
                self.identify_item_idx = -1
                return None
            self.finished = True
            return "back"
        return None

    def _enter_identify_mode(self, item, item_idx):
        """Switch to identify mode for a given inventory item."""
        self.identify_item = item
        self.identify_item_idx = item_idx
        self.mode = "identify"
        self._identify_buttons = []

        # Build combatant options for every party member who has identify skills
        self.identify_char_options = []
        for ci, char in enumerate(self.party):
            combatant = make_player_combatant(char)
            options = get_identify_options(combatant)
            if options:  # only show characters who have at least one skill
                self.identify_char_options.append((ci, combatant, options))

        if not self.identify_char_options:
            name = get_item_display_name(item)
            self._show_message(
                f"No one in the party can identify {name}. Visit a temple.",
                (180, 100, 100))
            self.mode = "normal"
            self.identify_item = None

    def _use_consumable(self, char, item_idx):
        """Use a consumable item from inventory. Returns (message, color)."""
        from core.classes import get_all_resources
        from ui.renderer import HEAL_COL, ORANGE, GREY
        MP_COL = (100, 180, 255)
        item = char.inventory[item_idx]
        name = item.get("name", "item")

        # Scroll of Remove Curse
        if item.get("effect") == "remove_curse" or name == "Scroll of Remove Curse":
            cursed_slots = [
                s for s, eq in (char.equipment or {}).items()
                if eq and eq.get("cursed") and not eq.get("curse_lifted")
            ]
            from core.status_effects import get_status_effects
            curse_fx = [s for s in get_status_effects(char) if s.get("type") == "curse"]
            if not cursed_slots and not curse_fx:
                return (f"{char.name} is not cursed.", ORANGE)
            for slot in cursed_slots:
                eq = char.equipment[slot]
                eq["curse_lifted"] = True
                char.equipment[slot] = None
                char.inventory.append(eq)
            for se in curse_fx:
                if hasattr(char, "status_effects") and se in char.status_effects:
                    char.status_effects.remove(se)
            self._consume(char, item_idx)
            return (f"{char.name}'s curses lifted!", HEAL_COL)

        # Scroll of Identify
        if item.get("subtype") == "scroll" and (
            name == "Scroll of Identify" or item.get("effect") == "identify"
        ):
            from core.party_knowledge import mark_item_identified
            for member in self.party:
                for i, inv_item in enumerate(member.inventory):
                    if not inv_item.get("identified"):
                        inv_item["identified"] = True
                        inv_item["magic_identified"] = True
                        inv_item["material_identified"] = True
                        mark_item_identified(inv_item.get("name", ""))
                        self._consume(char, item_idx)
                        return (
                            f"Identified: {inv_item.get('name', 'item')} ({member.name})",
                            HEAL_COL
                        )
            return ("No unidentified items to identify.", ORANGE)

        # Healing potion
        heal = item.get("heal", 0)
        if heal > 0:
            max_res = get_all_resources(char.class_name, char.stats, char.level)
            max_hp = max_res.get("HP", 1)
            old_hp = char.resources.get("HP", 0)
            char.resources["HP"] = min(max_hp, old_hp + heal)
            actual = char.resources["HP"] - old_hp
            self._consume(char, item_idx)
            return (f"{char.name} used {name}: +{actual} HP", HEAL_COL)

        # MP restore
        restore_mp = item.get("restore_mp", 0)
        if restore_mp > 0:
            max_res = get_all_resources(char.class_name, char.stats, char.level)
            for rk in char.resources:
                if "MP" in rk:
                    max_val = max_res.get(rk, 0)
                    old_val = char.resources[rk]
                    char.resources[rk] = min(max_val, old_val + restore_mp)
                    actual = char.resources[rk] - old_val
                    self._consume(char, item_idx)
                    return (f"{char.name} used {name}: +{actual} {rk}", MP_COL)

        return (f"Can't use {name} here.", ORANGE)

    def _consume(self, char, item_idx):
        """Reduce stack by 1 or remove item from inventory."""
        if item_idx >= len(char.inventory):
            return
        item = char.inventory[item_idx]
        stack = item.get("stack", 1)
        if stack > 1:
            item["stack"] = stack - 1
        else:
            char.inventory.pop(item_idx)

    def handle_scroll(self, direction):
        char = self.party[self.selected_char]
        max_scroll = max(0, len(char.inventory) - 9)
        if direction > 0:
            self.inv_scroll = min(max_scroll, self.inv_scroll + 1)
        else:
            self.inv_scroll = max(0, self.inv_scroll - 1)

    def _show_message(self, msg, color=CREAM):
        self.message = msg
        self.message_color = color
        self.message_timer = 2500
