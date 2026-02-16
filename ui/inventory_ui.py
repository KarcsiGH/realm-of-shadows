"""
Realm of Shadows — Inventory & Equipment UI
Accessible from the party screen. Shows equipment slots, inventory list,
and allows equip/unequip/swap.
"""
import pygame
from ui.renderer import *
from core.equipment import (
    SLOT_ORDER, SLOT_NAMES, can_equip, equip_item, unequip_item,
    calc_equipment_defense, calc_equipment_magic_resist,
    calc_equipment_speed, calc_equipment_stat_bonuses,
)
from core.classes import CLASSES, STAT_NAMES, STAT_FULL_NAMES, get_all_resources
from core.identification import get_item_display_name, get_item_display_desc

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
STAT_SAME     = GREY

RARITY_COLORS = {
    "common":    CREAM,
    "uncommon":  (80, 220, 80),
    "rare":      (80, 140, 255),
    "epic":      (180, 80, 255),
    "legendary": (255, 180, 40),
}


class InventoryUI:
    """Full-screen inventory and equipment management."""

    def __init__(self, party):
        self.party = party
        self.selected_char = 0
        self.selected_slot = -1       # index into SLOT_ORDER
        self.selected_inv_item = -1   # index into character inventory
        self.inv_scroll = 0
        self.message = ""
        self.message_timer = 0
        self.message_color = CREAM
        self.finished = False

    def draw(self, surface, mx, my, dt):
        self.message_timer = max(0, self.message_timer - dt)
        surface.fill(BG_COLOR)

        # ── Header ──
        draw_text(surface, "Equipment & Inventory", 20, 12, GOLD, 22, bold=True)

        # Back button
        back_btn = pygame.Rect(SCREEN_W - 160, 8, 140, 36)
        hover_back = back_btn.collidepoint(mx, my)
        draw_button(surface, back_btn, "← Back to Party", hover=hover_back, size=13)

        # ── Character tabs ──
        tab_y = 50
        for i, char in enumerate(self.party):
            cls = CLASSES[char.class_name]
            tab_w = (SCREEN_W - 40) // len(self.party)
            tab_rect = pygame.Rect(20 + i * tab_w, tab_y, tab_w - 4, 36)
            is_sel = (i == self.selected_char)
            is_hover = tab_rect.collidepoint(mx, my)

            if is_sel:
                bg = (50, 40, 85)
                border = cls["color"]
            elif is_hover:
                bg = (35, 30, 60)
                border = HIGHLIGHT
            else:
                bg = (20, 18, 36)
                border = PANEL_BORDER

            pygame.draw.rect(surface, bg, tab_rect, border_radius=3)
            pygame.draw.rect(surface, border, tab_rect, 2, border_radius=3)
            draw_text(surface, f"{char.name} ({char.class_name})",
                      tab_rect.x + 8, tab_rect.y + 9,
                      cls["color"] if is_sel else GREY, 13, bold=is_sel)

        char = self.party[self.selected_char]
        cls = CLASSES[char.class_name]

        # ── Left: Equipment slots ──
        equip_panel = pygame.Rect(20, 100, 420, 500)
        draw_panel(surface, equip_panel, bg_color=INV_BG)
        draw_text(surface, "Equipment", equip_panel.x + 12, equip_panel.y + 8,
                  GOLD, 16, bold=True)

        slot_y = equip_panel.y + 35
        for si, slot_key in enumerate(SLOT_ORDER):
            slot_rect = pygame.Rect(equip_panel.x + 8, slot_y,
                                    equip_panel.width - 16, 52)
            item = char.equipment.get(slot_key) if char.equipment else None
            is_hover = slot_rect.collidepoint(mx, my)
            is_sel = (si == self.selected_slot)

            if is_sel:
                bg = SLOT_SELECTED
                border = GOLD
            elif is_hover:
                bg = SLOT_HOVER
                border = HIGHLIGHT
            elif item:
                bg = SLOT_FILLED
                border = PANEL_BORDER
            else:
                bg = SLOT_EMPTY
                border = (40, 35, 55)

            pygame.draw.rect(surface, bg, slot_rect, border_radius=3)
            pygame.draw.rect(surface, border, slot_rect, 2, border_radius=3)

            # Slot label
            slot_name = SLOT_NAMES.get(slot_key, slot_key)
            draw_text(surface, slot_name, slot_rect.x + 8, slot_rect.y + 4,
                      DIM_GOLD, 12)

            if item:
                rarity = item.get("rarity", "common")
                name_col = RARITY_COLORS.get(rarity, CREAM)
                display_name = get_item_display_name(item)
                draw_text(surface, display_name, slot_rect.x + 100, slot_rect.y + 4,
                          name_col, 14, bold=True)

                # Key stats
                parts = []
                if item.get("defense", 0) > 0:
                    parts.append(f"DEF +{item['defense']}")
                if item.get("magic_resist", 0) > 0:
                    parts.append(f"MRES +{item['magic_resist']}")
                if item.get("speed_mod", 0) != 0:
                    sign = "+" if item["speed_mod"] > 0 else ""
                    parts.append(f"SPD {sign}{item['speed_mod']}")
                for stat, val in item.get("stat_bonuses", {}).items():
                    parts.append(f"{stat} +{val}")
                if parts:
                    draw_text(surface, "  ".join(parts),
                              slot_rect.x + 100, slot_rect.y + 24, GREY, 11)
            else:
                draw_text(surface, "— empty —", slot_rect.x + 100, slot_rect.y + 18,
                          DARK_GREY, 13)

            slot_y += 56

        # Unequip button (if a slot with an item is selected)
        if (self.selected_slot >= 0 and self.selected_slot < len(SLOT_ORDER)):
            sel_slot_key = SLOT_ORDER[self.selected_slot]
            sel_item = char.equipment.get(sel_slot_key) if char.equipment else None
            if sel_item:
                unequip_btn = pygame.Rect(equip_panel.x + 8, slot_y + 4,
                                          180, 36)
                hover_unequip = unequip_btn.collidepoint(mx, my)
                draw_button(surface, unequip_btn, "Unequip",
                            hover=hover_unequip, size=14)

        # ── Stat summary below equipment ──
        stat_panel = pygame.Rect(20, 610, 420, 160)
        draw_panel(surface, stat_panel, bg_color=INV_BG)
        draw_text(surface, "Combat Stats", stat_panel.x + 12, stat_panel.y + 8,
                  GOLD, 14, bold=True)

        base_def = int(char.stats["CON"] * 0.5)
        equip_def = calc_equipment_defense(char)
        base_mres = int(char.stats["WIS"] * 0.5)
        equip_mres = calc_equipment_magic_resist(char)
        equip_spd = calc_equipment_speed(char)
        equip_stats = calc_equipment_stat_bonuses(char)

        sy = stat_panel.y + 30
        draw_text(surface, f"Defense: {base_def} + {equip_def} = {base_def + equip_def}",
                  stat_panel.x + 12, sy, CREAM, 13)
        sy += 20
        draw_text(surface, f"Magic Resist: {base_mres} + {equip_mres} = {base_mres + equip_mres}",
                  stat_panel.x + 12, sy, CREAM, 13)
        sy += 20
        if equip_spd != 0:
            sign = "+" if equip_spd > 0 else ""
            draw_text(surface, f"Speed modifier: {sign}{equip_spd}",
                      stat_panel.x + 12, sy, CREAM, 13)
            sy += 20
        if equip_stats:
            bonus_parts = [f"{stat} +{val}" for stat, val in equip_stats.items()]
            draw_text(surface, f"Stat bonuses: {', '.join(bonus_parts)}",
                      stat_panel.x + 12, sy, STAT_UP, 13)

        # ── Right: Inventory ──
        inv_panel = pygame.Rect(460, 100, SCREEN_W - 480, 670)
        draw_panel(surface, inv_panel, bg_color=INV_BG)
        draw_text(surface, f"Inventory ({len(char.inventory)} items)  |  Gold: {char.gold}",
                  inv_panel.x + 12, inv_panel.y + 8, GOLD, 16, bold=True)

        if not char.inventory:
            draw_text(surface, "Inventory is empty.",
                      inv_panel.x + 20, inv_panel.y + 45, DARK_GREY, 15)
        else:
            iy = inv_panel.y + 35
            max_visible = 10
            start = self.inv_scroll
            end = min(len(char.inventory), start + max_visible)

            if self.inv_scroll > 0:
                draw_text(surface, "▲ scroll up", inv_panel.x + inv_panel.width // 2 - 40,
                          iy - 14, DIM_GOLD, 11)

            for idx in range(start, end):
                item = char.inventory[idx]
                item_rect = pygame.Rect(inv_panel.x + 8, iy,
                                        inv_panel.width - 16, 58)
                is_hover = item_rect.collidepoint(mx, my)
                is_sel = (idx == self.selected_inv_item)

                # Check if equippable
                can_eq, reason = can_equip(char, item)
                item_slot = item.get("slot", "")
                is_equippable = item_slot in SLOT_ORDER or item_slot == "accessory"

                if is_sel:
                    bg = SLOT_SELECTED
                    border = GOLD
                elif is_hover:
                    bg = SLOT_HOVER
                    border = HIGHLIGHT
                else:
                    bg = (22, 18, 40)
                    border = PANEL_BORDER

                pygame.draw.rect(surface, bg, item_rect, border_radius=3)
                pygame.draw.rect(surface, border, item_rect, 2, border_radius=3)

                # Item name
                display_name = get_item_display_name(item)
                rarity = item.get("rarity", "common")
                name_col = RARITY_COLORS.get(rarity, CREAM) if item.get("identified") else GREY
                draw_text(surface, display_name, item_rect.x + 10, item_rect.y + 4,
                          name_col, 14, bold=True)

                # Type + slot info
                item_type = item.get("type", "misc")
                slot_label = item.get("slot", "")
                type_str = f"{item_type}"
                if slot_label:
                    type_str += f" ({slot_label})"
                draw_text(surface, type_str, item_rect.x + 10, item_rect.y + 22,
                          DARK_GREY, 11)

                # Quick stats
                parts = []
                if item.get("damage"):
                    parts.append(f"DMG {item['damage']}")
                if item.get("defense", 0) > 0:
                    parts.append(f"DEF +{item['defense']}")
                for stat, val in item.get("stat_bonuses", {}).items():
                    parts.append(f"{stat} +{val}")
                if parts:
                    draw_text(surface, "  ".join(parts),
                              item_rect.x + 10, item_rect.y + 38, GREY, 11)

                # Equip hint on hover
                if is_hover and is_equippable:
                    if can_eq:
                        draw_text(surface, "Click to equip",
                                  item_rect.x + item_rect.width - 100, item_rect.y + 4,
                                  EQUIP_COL, 11)
                    else:
                        draw_text(surface, reason,
                                  item_rect.x + item_rect.width - 200, item_rect.y + 4,
                                  STAT_DOWN, 11)

                iy += 62

            if end < len(char.inventory):
                draw_text(surface, "▼ scroll down",
                          inv_panel.x + inv_panel.width // 2 - 45,
                          iy + 4, DIM_GOLD, 11)

        # ── Status message ──
        if self.message and self.message_timer > 0:
            alpha = min(255, int(self.message_timer * 0.25))
            draw_text(surface, self.message, SCREEN_W // 2 - 150,
                      SCREEN_H - 30, self.message_color, 15)

    def handle_click(self, mx, my):
        """Handle click. Returns 'back' to exit inventory."""
        char = self.party[self.selected_char]

        # Back button
        back_btn = pygame.Rect(SCREEN_W - 160, 8, 140, 36)
        if back_btn.collidepoint(mx, my):
            self.finished = True
            return "back"

        # Character tabs
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

        # Equipment slot clicks
        equip_panel = pygame.Rect(20, 100, 420, 500)
        slot_y = equip_panel.y + 35
        for si, slot_key in enumerate(SLOT_ORDER):
            slot_rect = pygame.Rect(equip_panel.x + 8, slot_y,
                                    equip_panel.width - 16, 52)
            if slot_rect.collidepoint(mx, my):
                self.selected_slot = si
                self.selected_inv_item = -1
                return None
            slot_y += 56

        # Unequip button
        if self.selected_slot >= 0 and self.selected_slot < len(SLOT_ORDER):
            sel_slot_key = SLOT_ORDER[self.selected_slot]
            sel_item = char.equipment.get(sel_slot_key) if char.equipment else None
            if sel_item:
                unequip_btn = pygame.Rect(equip_panel.x + 8, slot_y + 4,
                                          180, 36)
                if unequip_btn.collidepoint(mx, my):
                    ok, item, msg = unequip_item(char, sel_slot_key)
                    self._show_message(msg, CREAM if ok else STAT_DOWN)
                    return None

        # Inventory item clicks
        inv_panel = pygame.Rect(460, 100, SCREEN_W - 480, 670)
        if char.inventory:
            iy = inv_panel.y + 35
            max_visible = 10
            start = self.inv_scroll
            end = min(len(char.inventory), start + max_visible)
            for idx in range(start, end):
                item = char.inventory[idx]
                item_rect = pygame.Rect(inv_panel.x + 8, iy,
                                        inv_panel.width - 16, 58)
                if item_rect.collidepoint(mx, my):
                    # Try to equip
                    item_slot = item.get("slot", "")
                    if item_slot in SLOT_ORDER or item_slot == "accessory":
                        target_slot = None
                        if self.selected_slot >= 0:
                            target_slot = SLOT_ORDER[self.selected_slot]
                        ok, old_item, msg = equip_item(char, item, target_slot)
                        self._show_message(msg, EQUIP_COL if ok else STAT_DOWN)
                        if ok:
                            self.selected_inv_item = -1
                    else:
                        self.selected_inv_item = idx
                    return None
                iy += 62

        return None

    def handle_scroll(self, direction):
        char = self.party[self.selected_char]
        max_scroll = max(0, len(char.inventory) - 10)
        if direction > 0:
            self.inv_scroll = min(max_scroll, self.inv_scroll + 1)
        else:
            self.inv_scroll = max(0, self.inv_scroll - 1)

    def _show_message(self, msg, color=CREAM):
        self.message = msg
        self.message_color = color
        self.message_timer = 2000
