"""
Realm of Shadows — Quest Log UI

Two-panel journal: left sidebar lists all known quests grouped by status,
right panel shows the selected quest with full objectives checklist and rewards.
Also houses the Lore tab with the same two-panel layout.
"""
import pygame
from ui.renderer import (
    SCREEN_W, SCREEN_H, draw_text, draw_panel, draw_button, get_font,
    CREAM, GOLD, GREY, DARK_GREY, WHITE, PANEL_BG, PANEL_BORDER,
    HIGHLIGHT, DIM_GOLD, RED,
)

# ── Palette ──────────────────────────────────────────────────────────
LOG_BG         = (10, 8, 20)
SIDEBAR_BG     = (14, 11, 26)
DETAIL_BG      = (16, 13, 30)
QUEST_ACTIVE   = (90, 210, 130)
QUEST_COMPLETE = (110, 110, 135)
OBJ_DONE       = (80, 200, 110)
OBJ_PENDING    = (160, 155, 130)
LORE_COL       = (180, 160, 120)
ACT_LABEL      = (140, 120, 180)
TAB_SEL_BG     = (45, 36, 72)
TAB_DEF_BG     = (22, 18, 38)
REWARD_GOLD    = (210, 180, 80)
REWARD_XP      = (120, 200, 255)
SIDE_COL       = (100, 180, 220)
GIVER_COL      = (160, 140, 200)
DIVIDER        = (40, 34, 60)
BEAST_KNOWN    = (180, 220, 160)    # fully known enemy
BEAST_FOUGHT   = (200, 180, 120)    # fought but not fully catalogued
BEAST_UNKNOWN  = (80, 75, 70)       # never encountered
BEAST_BG_KNOWN = (18, 28, 16)
BEAST_BG_FIGHT = (28, 22, 12)
BEAST_BG_UNK   = (16, 14, 20)

SIDEBAR_W  = 256
PANEL_TOP  = 96
PAD_BOTTOM = 20



def _wrap_text(text, max_width, font_size):
    """Break text into lines that fit within max_width pixels."""
    font = None
    try:
        font = get_font(font_size)
    except Exception:
        font = None
    if font is not None:
        _f = font
        measure = lambda t, f=_f: f.size(t)[0]
    else:
        # Fallback for headless/test environments: estimate by character count
        chars_per_line = max(10, int(max_width / (font_size * 0.6)))
        measure = lambda t: len(t) * int(font_size * 0.6)
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        if measure(test) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


class QuestLogUI:
    """Quest journal with sidebar list + detail panel."""

    def __init__(self):
        self.tab           = "quests"   # "quests" | "lore" | "bestiary" | "guild"
        self.selected_qid  = None
        self.selected_lid  = None
        self.selected_eid  = None       # selected enemy key for bestiary
        self.scroll_list   = 0          # px offset for sidebar
        self.scroll_detail = 0          # px offset for detail panel
        self.finished      = False
        self._list_rects   = []         # [(Rect, id)] for click detection
        self._lore_rects   = []
        self._beast_rects  = []         # [(Rect, enemy_name)] for bestiary clicks

    # ─── Public draw ─────────────────────────────────────────────────

    def draw(self, surface, mx, my):
        surface.fill(LOG_BG)
        draw_text(surface, "Journal", SCREEN_W // 2 - 38, 12, GOLD, 21, bold=True)

        # Tabs
        for i, (key, label) in enumerate([("quests", "Quests"), ("lore", "Lore"), ("bestiary", "Bestiary"), ("guild", "Guild")]):
            r = pygame.Rect(20 + i * 116, 48, 108, 30)
            sel   = self.tab == key
            hover = r.collidepoint(mx, my)
            bg  = TAB_SEL_BG if sel else (32, 26, 52) if hover else TAB_DEF_BG
            brd = GOLD if sel else HIGHLIGHT if hover else PANEL_BORDER
            pygame.draw.rect(surface, bg, r, border_radius=3)
            pygame.draw.rect(surface, brd, r, 1, border_radius=3)
            draw_text(surface, label, r.x + 10, r.y + 6,
                      GOLD if sel else CREAM, 13, bold=sel)

        # Close
        close_r = pygame.Rect(SCREEN_W - 112, 48, 96, 30)
        draw_button(surface, close_r, "Close",
                    hover=close_r.collidepoint(mx, my), size=12)

        if self.tab == "quests":
            self._draw_quests(surface, mx, my)
        elif self.tab == "lore":
            self._draw_lore(surface, mx, my)
        elif self.tab == "guild":
            self._draw_guild_tier(surface, mx, my)
        else:
            self._draw_bestiary(surface, mx, my)

    # ─── Quest tab ────────────────────────────────────────────────────

    def _draw_quests(self, surface, mx, my):
        from data.story_data import QUESTS
        from core.story_flags import get_quest_state

        ph = SCREEN_H - PANEL_TOP - PAD_BOTTOM

        # Sidebar background
        sb = pygame.Rect(28, PANEL_TOP, SIDEBAR_W, ph)
        pygame.draw.rect(surface, SIDEBAR_BG, sb, border_radius=4)
        pygame.draw.rect(surface, PANEL_BORDER, sb, 1, border_radius=4)

        # Detail panel background
        dp_x = 28 + SIDEBAR_W + 6
        dp = pygame.Rect(dp_x, PANEL_TOP, SCREEN_W - dp_x - 28, ph)
        pygame.draw.rect(surface, DETAIL_BG, dp, border_radius=4)
        pygame.draw.rect(surface, PANEL_BORDER, dp, 1, border_radius=4)

        # Categorise quests
        active, completed = [], []
        for qid, q in QUESTS.items():
            s = get_quest_state(qid)
            if   s == -2: completed.append((qid, q))
            elif s  >  0: active.append((qid, q))

        # Draw with clip
        old_clip = surface.get_clip()
        surface.set_clip(sb.inflate(-2, -2))
        self._draw_sidebar(surface, mx, my, sb, active, completed)
        surface.set_clip(old_clip)

        if self.selected_qid and self.selected_qid in QUESTS:
            surface.set_clip(dp.inflate(-2, -2))
            self._draw_detail(surface, mx, my, dp,
                              self.selected_qid, QUESTS[self.selected_qid])
            surface.set_clip(old_clip)
        else:
            mid_y = dp.y + dp.height // 2 - 8
            draw_text(surface, "Select a quest to view details.",
                      dp.x + 18, mid_y, DARK_GREY, 13)

    def _draw_sidebar(self, surface, mx, my, sb, active, completed):
        from core.story_flags import check_quest_objectives
        self._list_rects = []
        y = sb.y + 8 - self.scroll_list

        def section_header(label, col):
            nonlocal y
            if sb.y <= y <= sb.y + sb.height:
                draw_text(surface, label, sb.x + 10, y, col, 10, bold=True)
            y += 18

        def quest_row(qid, q, state):
            nonlocal y
            is_main = not qid.startswith("side_")
            sel     = (qid == self.selected_qid)
            hover   = False
            ir = pygame.Rect(sb.x + 5, y, sb.width - 10, 26)

            if sb.y < y + 26 and y < sb.y + sb.height:
                hover = ir.collidepoint(mx, my)
                bg  = (40, 32, 64) if sel else (30, 24, 50) if hover else SIDEBAR_BG
                brd = GOLD if sel else HIGHLIGHT if hover else DIVIDER
                pygame.draw.rect(surface, bg,  ir, border_radius=3)
                pygame.draw.rect(surface, brd, ir, 1, border_radius=3)

                if state == -2:
                    draw_text(surface, "✓", ir.x + 6,  ir.y + 5, OBJ_DONE,      11, bold=True)
                    draw_text(surface, q["name"], ir.x + 20, ir.y + 5, QUEST_COMPLETE, 12, max_width=196)
                else:
                    dot = "●" if is_main else "◆"
                    dot_col = QUEST_ACTIVE if is_main else SIDE_COL
                    draw_text(surface, dot, ir.x + 6, ir.y + 5, dot_col, 11)
                    draw_text(surface, q["name"], ir.x + 20, ir.y + 5,
                              QUEST_ACTIVE if is_main else SIDE_COL, 12, max_width=180)
                    # objective progress badge
                    objs = check_quest_objectives(qid)
                    if objs:
                        n_done  = sum(1 for _, d in objs if d)
                        n_total = len(objs)
                        prog = f"{n_done}/{n_total}"
                        pw = get_font(10).size(prog)[0]
                        badge_col = OBJ_DONE if n_done == n_total else GREY
                        draw_text(surface, prog, ir.right - pw - 6, ir.y + 7, badge_col, 10)

                self._list_rects.append((pygame.Rect(ir), qid))
            y += 30

        if active:
            section_header("── ACTIVE ──", QUEST_ACTIVE)
            mains = sorted([(qid,q) for qid,q in active if not qid.startswith("side_")],
                           key=lambda x: x[1].get("act", 1))
            sides = sorted([(qid,q) for qid,q in active if     qid.startswith("side_")],
                           key=lambda x: x[1].get("act", 1))
            for qid, q in mains: quest_row(qid, q, 1)
            for qid, q in sides: quest_row(qid, q, 1)

        if completed:
            section_header("── COMPLETED ──", QUEST_COMPLETE)
            for qid, q in completed: quest_row(qid, q, -2)

        if not active and not completed:
            if y > sb.y:
                draw_text(surface, "No quests yet.", sb.x + 14, y, DARK_GREY, 12)
                y += 18
                draw_text(surface, "Speak to NPCs in town.", sb.x + 14, y, DARK_GREY, 11)

    def _draw_detail(self, surface, mx, my, dp, qid, q):
        from core.story_flags import check_quest_objectives, is_quest_complete, get_flag

        x0 = dp.x + 16
        y  = dp.y + 12 - self.scroll_detail
        rw = dp.width - 32

        is_main  = not qid.startswith("side_")
        done     = is_quest_complete(qid)
        act      = q.get("act", 1)
        name_col = GOLD if is_main else SIDE_COL

        # Title + act badge
        draw_text(surface, q["name"], x0, y, name_col, 16, bold=True, max_width=rw - 60)
        act_lbl = f"Act {act}"
        aw = get_font(10).size(act_lbl)[0] + 8
        ar = pygame.Rect(dp.right - aw - 12, y + 2, aw, 16)
        pygame.draw.rect(surface, (38, 30, 65), ar, border_radius=3)
        pygame.draw.rect(surface, ACT_LABEL, ar, 1, border_radius=3)
        draw_text(surface, act_lbl, ar.x + 4, ar.y + 2, ACT_LABEL, 10)
        y += 24

        # Status chip
        if done:
            chip_lbl, chip_col = "COMPLETED",  OBJ_DONE
        elif is_main:
            chip_lbl, chip_col = "MAIN QUEST", QUEST_ACTIVE
        else:
            chip_lbl, chip_col = "SIDE QUEST", SIDE_COL
        draw_text(surface, chip_lbl, x0, y, chip_col, 10, bold=True)
        y += 16

        # Divider
        pygame.draw.line(surface, DIVIDER, (x0, y), (dp.right - 16, y))
        y += 10

        # Description
        y = self._wrap(surface, q.get("description",""), x0, y, rw, CREAM, 13)
        y += 6

        # Giver / turn-in
        giver  = q.get("giver_npc")
        turnin = q.get("turn_in_npc")
        if giver:
            draw_text(surface, f"Given by: {giver}", x0, y, GIVER_COL, 11)
            y += 16
        if turnin and turnin != giver:
            draw_text(surface, f"Turn in to: {turnin}", x0, y, GIVER_COL, 11)
            y += 16
        if giver or turnin:
            y += 4

        # Divider
        pygame.draw.line(surface, DIVIDER, (x0, y), (dp.right - 16, y))
        y += 10

        # Objectives
        draw_text(surface, "Objectives", x0, y, GOLD, 12, bold=True)
        y += 18

        objs = check_quest_objectives(qid)
        if objs:
            for obj, obj_done in objs:
                text = obj.get("text", "")
                # Inject live count for >= objectives
                if obj.get("op") == ">=" and not obj_done:
                    cur = get_flag(obj.get("flag","")) or 0
                    needed = obj.get("val", 1)
                    if isinstance(cur, (int, float)):
                        base = text.split("(")[0].strip()
                        text = f"{base} ({int(cur)}/{needed})"

                icon     = "✓" if obj_done else "○"
                icon_col = OBJ_DONE     if obj_done else (85, 80, 100)
                text_col = OBJ_DONE     if obj_done else OBJ_PENDING
                draw_text(surface, icon, x0 + 2, y, icon_col, 11, bold=True)
                y = self._wrap(surface, text, x0 + 18, y, rw - 20, text_col, 12)
                y += 3
        else:
            draw_text(surface, "— no tracked objectives —", x0 + 10, y, DARK_GREY, 11)
            y += 16

        y += 8
        pygame.draw.line(surface, DIVIDER, (x0, y), (dp.right - 16, y))
        y += 10

        # Rewards
        draw_text(surface, "Rewards", x0, y, GOLD, 12, bold=True)
        y += 18

        if done:
            draw_text(surface, "✓  Rewards already collected.", x0 + 10, y, OBJ_DONE, 11)
            y += 16
        else:
            rg = q.get("reward_gold", 0)
            rx = q.get("reward_xp",   0)
            ri = q.get("reward_items", [])
            if rg > 0:
                draw_text(surface, f"◈  {rg} gold", x0 + 10, y, REWARD_GOLD, 12)
                y += 17
            if rx > 0:
                draw_text(surface, f"★  {rx} XP",   x0 + 10, y, REWARD_XP, 12)
                y += 17
            for itm in ri:
                label = itm["name"] if isinstance(itm, dict) else itm
                draw_text(surface, f"⚔  {label}",     x0 + 10, y, (200, 160, 220), 12)
                y += 17
            if not rg and not rx and not ri:
                draw_text(surface, "— story progression —", x0 + 10, y, DARK_GREY, 11)
                y += 16

    # ─── Lore tab ─────────────────────────────────────────────────────

    def _draw_lore(self, surface, mx, my):
        from data.story_data import LORE_ENTRIES
        from core.story_flags import has_lore

        ph  = SCREEN_H - PANEL_TOP - PAD_BOTTOM
        sb  = pygame.Rect(28, PANEL_TOP, SIDEBAR_W, ph)
        dp_x = 28 + SIDEBAR_W + 6
        dp  = pygame.Rect(dp_x, PANEL_TOP, SCREEN_W - dp_x - 28, ph)

        pygame.draw.rect(surface, SIDEBAR_BG, sb, border_radius=4)
        pygame.draw.rect(surface, PANEL_BORDER, sb, 1, border_radius=4)
        pygame.draw.rect(surface, DETAIL_BG, dp, border_radius=4)
        pygame.draw.rect(surface, PANEL_BORDER, dp, 1, border_radius=4)

        discovered = [(lid, ld) for lid, ld in LORE_ENTRIES.items() if has_lore(lid)]

        old_clip = surface.get_clip()
        # Sidebar
        surface.set_clip(sb.inflate(-2, -2))
        self._lore_rects = []
        y = sb.y + 10 - self.scroll_list
        draw_text(surface, "── DISCOVERED ──", sb.x + 10, y, LORE_COL, 10, bold=True)
        y += 18
        for lid, ld in discovered:
            ir = pygame.Rect(sb.x + 5, y, sb.width - 10, 26)
            if sb.y < y + 26 and y < sb.y + sb.height:
                sel   = (lid == self.selected_lid)
                hover = ir.collidepoint(mx, my)
                bg  = (40, 32, 64) if sel else (30, 24, 50) if hover else SIDEBAR_BG
                brd = GOLD if sel else HIGHLIGHT if hover else DIVIDER
                pygame.draw.rect(surface, bg,  ir, border_radius=3)
                pygame.draw.rect(surface, brd, ir, 1, border_radius=3)
                draw_text(surface, ld["title"], ir.x + 10, ir.y + 5,
                          LORE_COL if sel else CREAM, 12)
                self._lore_rects.append((pygame.Rect(ir), lid))
            y += 30
        if not discovered:
            draw_text(surface, "Nothing discovered yet.", sb.x + 14, y, DARK_GREY, 11)
        surface.set_clip(old_clip)

        # Detail
        if self.selected_lid and self.selected_lid in LORE_ENTRIES:
            ld = LORE_ENTRIES[self.selected_lid]
            surface.set_clip(dp.inflate(-2, -2))
            x0, y0 = dp.x + 16, dp.y + 14 - self.scroll_detail
            rw = dp.width - 32
            draw_text(surface, ld["title"], x0, y0, LORE_COL, 15, bold=True)
            y0 += 24
            pygame.draw.line(surface, DIVIDER, (x0, y0), (dp.right - 16, y0))
            y0 += 10
            self._wrap(surface, ld.get("text", ""), x0, y0, rw, CREAM, 13)
            surface.set_clip(old_clip)
        else:
            draw_text(surface, "Select an entry to read.",
                      dp.x + 18, dp.y + dp.height // 2 - 8, DARK_GREY, 13)

    # ─── Helpers ──────────────────────────────────────────────────────

    def _wrap(self, surface, text, x, y, max_w, color, size):
        """Word-wrap text, return new y."""
        font  = get_font(size)
        words = text.split()
        line  = ""
        for w in words:
            test = line + (" " if line else "") + w
            if font.size(test)[0] <= max_w:
                line = test
            else:
                if line:
                    draw_text(surface, line, x, y, color, size)
                    y += size + 4
                line = w
        if line:
            draw_text(surface, line, x, y, color, size)
            y += size + 4
        return y

    # ─── Input ────────────────────────────────────────────────────────

    # ─── Bestiary tab ─────────────────────────────────────────────────

    # ─── Guild / Warden Rank tab ──────────────────────────────────────

    def _draw_guild_tier(self, surface, mx, my):
        """Draw Warden rank progression, active bonuses, and next milestone."""
        from core.progression import PLANAR_TIERS, get_party_tier
        from core.story_flags import get_save_data

        story_flags = get_save_data()
        # Find current tier from story flags (use tier 0 if none)
        from core.story_flags import get_flag
        current_tier = 0
        for tier_idx in sorted(PLANAR_TIERS.keys(), reverse=True):
            t = PLANAR_TIERS[tier_idx]
            flag = t.get("unlock_flag")
            if flag and get_flag(flag):
                current_tier = tier_idx
                break

        tier_data = PLANAR_TIERS.get(current_tier, PLANAR_TIERS[0])

        panel_x, panel_y = 20, 86
        panel_w = SCREEN_W - 40
        col_w   = panel_w // 2 - 16

        # ── Left panel: current rank ──────────────────────────────────
        lp = pygame.Rect(panel_x, panel_y, col_w, SCREEN_H - 120)
        pygame.draw.rect(surface, (18, 14, 30), lp, border_radius=4)
        pygame.draw.rect(surface, PANEL_BORDER, lp, 1, border_radius=4)

        y = panel_y + 16
        tier_col = tuple(tier_data["color"])

        draw_text(surface, "Current Rank", lp.x + 16, y, GREY, 11)
        y += 18
        draw_text(surface, tier_data["name"], lp.x + 16, y, tier_col, 24, bold=True)
        y += 32

        # Rank description
        draw_text(surface, tier_data["description"], lp.x + 16, y, CREAM, 13,
                  max_width=col_w - 32)
        y += 48

        # Active bonuses
        bonus = tier_data.get("bonus", {})
        if bonus:
            draw_text(surface, "Active Bonuses", lp.x + 16, y, GOLD, 12, bold=True)
            y += 20
            bonus_lines = []
            if bonus.get("all_stats"):
                bonus_lines.append(f"+{bonus['all_stats']} to all stats")
            if bonus.get("max_hp_pct"):
                bonus_lines.append(f"+{int(bonus['max_hp_pct']*100)}% max HP")
            if bonus.get("damage_mult"):
                pct = int((bonus["damage_mult"] - 1) * 100)
                bonus_lines.append(f"+{pct}% damage dealt")
            if bonus.get("xp_mult"):
                pct = int((bonus["xp_mult"] - 1) * 100)
                bonus_lines.append(f"+{pct}% XP earned")
            for bl in bonus_lines:
                draw_text(surface, f"  ◆  {bl}", lp.x + 16, y, (120, 220, 160), 13)
                y += 18
        else:
            draw_text(surface, "No bonuses yet — advance your rank.", lp.x + 16, y, GREY, 12)
            y += 18

        y += 12

        # Next rank preview
        next_tier = current_tier + 1
        if next_tier in PLANAR_TIERS:
            nt = PLANAR_TIERS[next_tier]
            pygame.draw.rect(surface, (28, 22, 44),
                             (lp.x + 10, y, col_w - 20, 90), border_radius=4)
            pygame.draw.rect(surface, (60, 55, 80),
                             (lp.x + 10, y, col_w - 20, 90), 1, border_radius=4)
            y += 10
            draw_text(surface, "Next Rank", lp.x + 20, y, GREY, 10)
            y += 14
            draw_text(surface, nt["name"], lp.x + 20, y, tuple(nt["color"]), 16, bold=True)
            y += 20
            flag_needed = nt.get("unlock_flag", "")
            flag_label  = flag_needed.replace("_", " ").replace("boss defeated.", "Defeat ").replace("item.", "Obtain ").title()
            draw_text(surface, f"Unlock: {flag_label}", lp.x + 20, y, (160, 140, 100), 11,
                      max_width=col_w - 40)
            y += 16
        else:
            draw_text(surface, "Maximum rank achieved.", lp.x + 16, y, GOLD, 13, bold=True)

        # ── Right panel: rank ladder ──────────────────────────────────
        rp = pygame.Rect(panel_x + col_w + 32, panel_y, col_w, SCREEN_H - 120)
        pygame.draw.rect(surface, (18, 14, 30), rp, border_radius=4)
        pygame.draw.rect(surface, PANEL_BORDER, rp, 1, border_radius=4)

        draw_text(surface, "Warden Order — All Ranks", rp.x + 16, panel_y + 16, GOLD, 13, bold=True)

        ry = panel_y + 38
        for tier_idx, t in sorted(PLANAR_TIERS.items()):
            is_current  = (tier_idx == current_tier)
            is_unlocked = (tier_idx <= current_tier)
            tc = tuple(t["color"])

            row_h = 42
            row_r = pygame.Rect(rp.x + 10, ry, col_w - 20, row_h)

            if is_current:
                pygame.draw.rect(surface, (30, 50, 35), row_r, border_radius=3)
                pygame.draw.rect(surface, tc, row_r, 1, border_radius=3)
            elif is_unlocked:
                pygame.draw.rect(surface, (24, 22, 36), row_r, border_radius=3)
                pygame.draw.rect(surface, (50, 48, 65), row_r, 1, border_radius=3)
            else:
                pygame.draw.rect(surface, (18, 16, 26), row_r, border_radius=3)

            name_col = tc if is_unlocked else (60, 55, 75)
            status   = "► CURRENT" if is_current else ("✓" if is_unlocked else "–")
            st_col   = (100, 220, 130) if is_current else ((160, 160, 180) if is_unlocked else (50, 45, 65))

            draw_text(surface, status,          row_r.x + 8,  ry + 6,  st_col,   10)
            draw_text(surface, t["name"],       row_r.x + 60, ry + 4,  name_col, 14, bold=is_current)
            draw_text(surface, t["description"][:50] + ("…" if len(t["description"]) > 50 else ""),
                      row_r.x + 60, ry + 22, GREY if is_unlocked else (45, 42, 58), 10,
                      max_width=col_w - 80)

            ry += row_h + 6
            if ry > rp.bottom - 16:
                break

    def _draw_bestiary(self, surface, mx, my):
        """Bestiary: left sidebar lists known enemy types by region/dungeon.
        Right panel shows full stats, description, and resistance profile."""
        from data.enemies import ENEMIES, ENCOUNTERS
        from data.dungeon import DUNGEONS
        from core.party_knowledge import get_enemy_knowledge_tier

        ph = SCREEN_H - PANEL_TOP - PAD_BOTTOM

        # ── Build dungeon→enemy mapping once ──
        dungeon_buckets = {}  # dungeon_id -> [enemy_name, ...]
        for did, d in DUNGEONS.items():
            table = d.get("encounter_table", {})
            enc_keys = {enc for fl in table.values() for enc in fl}
            boss_enc = d.get("boss_encounter")
            if boss_enc:
                enc_keys.add(boss_enc)
            names = set()
            for ek in enc_keys:
                if ek in ENCOUNTERS:
                    for g in ENCOUNTERS[ek].get("groups", []):
                        ename = g.get("enemy", "")
                        if ename and ename in ENEMIES:
                            names.add(ename)
            if names:
                dungeon_buckets[did] = sorted(names)

        DUNGEON_LABELS = {
            "goblin_warren":   "Goblin Warren",
            "spiders_nest":    "Spider's Nest",
            "abandoned_mine":  "Abandoned Mine",
            "sunken_crypt":    "Sunken Crypt",
            "ruins_ashenmoor": "Ruins of Ashenmoor",
            "valdris_spire":   "Valdris' Spire",
            "dragons_tooth":   "Dragon's Tooth",
        }

        def dungeon_discovered(did):
            names = dungeon_buckets.get(did, [])
            known = sum(1 for n in names if get_enemy_knowledge_tier(n) >= 1)
            return known, len(names)

        # ── Sidebar ──────────────────────────────────────────────────
        sb = pygame.Rect(28, PANEL_TOP, SIDEBAR_W, ph)
        pygame.draw.rect(surface, SIDEBAR_BG, sb, border_radius=4)
        pygame.draw.rect(surface, PANEL_BORDER, sb, 1, border_radius=4)

        self._beast_rects = []
        clip_sb = surface.get_clip()
        surface.set_clip(sb.inflate(-2, -2))

        GROUP_H  = 22
        ENTRY_H  = 36
        y        = PANEL_TOP + 8 - self.scroll_list
        max_y    = PANEL_TOP + 8

        for did in DUNGEONS:
            names = dungeon_buckets.get(did, [])
            if not names:
                continue
            disc, total = dungeon_discovered(did)

            if y + GROUP_H >= PANEL_TOP and y < PANEL_TOP + ph:
                badge_col = (90, 200, 120) if disc == total else (160, 140, 80)
                draw_text(surface, DUNGEON_LABELS.get(did, did),
                          sb.x + 10, y + 3, badge_col, 11, bold=True)
                draw_text(surface, f"{disc}/{total}",
                          sb.right - 34, y + 3, badge_col, 11)
            y += GROUP_H

            for ename in names:
                tier = get_enemy_knowledge_tier(ename)
                if tier < 0:
                    display = "???"
                    col = BEAST_UNKNOWN
                    bg  = BEAST_BG_UNK
                else:
                    display = ename
                    col = BEAST_KNOWN if tier >= 2 else BEAST_FOUGHT
                    bg  = BEAST_BG_KNOWN if tier >= 2 else BEAST_BG_FIGHT

                row = pygame.Rect(sb.x + 4, y, SIDEBAR_W - 8, ENTRY_H - 2)
                max_y = max(max_y, y + ENTRY_H)

                if y + ENTRY_H >= PANEL_TOP and y < PANEL_TOP + ph:
                    sel = self.selected_eid == ename and tier >= 1
                    bg_col = (35, 55, 30) if sel else bg
                    bd_col = (80, 180, 80) if sel else (40, 35, 50)
                    pygame.draw.rect(surface, bg_col, row, border_radius=3)
                    pygame.draw.rect(surface, bd_col, row, 1, border_radius=3)

                    pip_col = (80, 200, 110) if tier >= 2 else (200, 180, 80) if tier >= 1 else (60, 55, 65)
                    pygame.draw.circle(surface, pip_col, (row.x + 10, row.y + row.h // 2), 4)

                    draw_text(surface, display, row.x + 20, row.y + 4, col, 12, bold=(tier >= 1))
                    if tier >= 1:
                        e = ENEMIES.get(ename, {})
                        hp_txt = f"HP {e.get('hp', '?')}"
                        draw_text(surface, hp_txt, row.x + 20, row.y + 18, (100, 120, 100), 10)

                if tier >= 1:
                    self._beast_rects.append((row, ename))

                y += ENTRY_H

            y += 6

        surface.set_clip(clip_sb)

        content_h = max_y - (PANEL_TOP + 8) + 20
        if content_h > ph:
            ratio     = ph / content_h
            bar_h     = max(24, int(ph * ratio))
            bar_y     = PANEL_TOP + int(self.scroll_list / content_h * ph)
            bar_y     = min(bar_y, PANEL_TOP + ph - bar_h)
            pygame.draw.rect(surface, (50, 45, 70),
                             pygame.Rect(sb.right - 6, bar_y, 4, bar_h), border_radius=2)

        # ── Detail Panel ─────────────────────────────────────────────
        dp_x = 28 + SIDEBAR_W + 8
        dp_w = SCREEN_W - dp_x - 20
        dp   = pygame.Rect(dp_x, PANEL_TOP, dp_w, ph)
        pygame.draw.rect(surface, DETAIL_BG, dp, border_radius=4)
        pygame.draw.rect(surface, PANEL_BORDER, dp, 1, border_radius=4)

        eid  = self.selected_eid
        tier = get_enemy_knowledge_tier(eid) if eid else -1

        if not eid or eid not in ENEMIES or tier < 1:
            draw_text(surface, "Select an enemy to view its entry.",
                      dp.x + 20, dp.y + ph // 2 - 20, GREY, 14)
            draw_text(surface, "Fight enemies in dungeons to unlock their bestiary entries.",
                      dp.x + 20, dp.y + ph // 2 + 2, BEAST_UNKNOWN, 11)
            return

        e = ENEMIES[eid]
        clip_dp = surface.get_clip()
        surface.set_clip(dp.inflate(-4, -4))

        dy = dp.y + 10 - self.scroll_detail

        tier_label = "Fully Catalogued" if tier >= 2 else "Encountered"
        tier_col   = (80, 200, 120) if tier >= 2 else (200, 180, 80)
        draw_text(surface, eid, dp.x + 14, dy, GOLD, 20, bold=True)
        draw_text(surface, f"◆ {tier_label}", dp.x + 14, dy + 26, tier_col, 11)
        dy += 48

        pygame.draw.line(surface, DIVIDER, (dp.x + 10, dy), (dp.right - 10, dy))
        dy += 8

        desc_tiers = e.get("description_tiers", {})
        desc = desc_tiers.get(min(tier, 2), desc_tiers.get(0, "No description available."))
        if desc and desc != eid:
            for line in _wrap_text(desc, dp_w - 28, 13):
                if dp.y <= dy < dp.y + ph:
                    draw_text(surface, line, dp.x + 14, dy, (190, 180, 160), 13)
                dy += 18
            dy += 6

        # Stats (tier 1+)
        if tier >= 1:
            pygame.draw.line(surface, DIVIDER, (dp.x + 10, dy), (dp.right - 10, dy))
            dy += 8
            draw_text(surface, "Combat Stats", dp.x + 14, dy, BEAST_FOUGHT, 12, bold=True)
            dy += 18

            stats_data = [
                ("HP",      str(e.get("hp", "?"))),
                ("Defense", str(e.get("defense", "?"))),
                ("Mag.Res", str(e.get("magic_resist", "?"))),
                ("Attack",  f"{e.get('attack_damage', '?')} ({e.get('attack_type', '?')})" ),
                ("Speed",   str(e.get("speed_base", "?"))),
                ("XP",      str(e.get("xp_reward", "?"))),
                ("Row",     e.get("preferred_row", "?").upper()),
                ("AI",      e.get("ai_type", "?").upper()),
            ]
            col_w = (dp_w - 28) // 2
            for idx, (label, val) in enumerate(stats_data):
                col_x = dp.x + 14 + (idx % 2) * col_w
                row_y = dy + (idx // 2) * 18
                if dp.y <= row_y < dp.y + ph:
                    draw_text(surface, f"{label}:", col_x, row_y, BEAST_UNKNOWN, 11)
                    draw_text(surface, val, col_x + 60, row_y, CREAM, 11)
            dy += ((len(stats_data) + 1) // 2) * 18 + 8

        # Resistances + abilities (tier 2)
        if tier >= 2:
            pygame.draw.line(surface, DIVIDER, (dp.x + 10, dy), (dp.right - 10, dy))
            dy += 8
            draw_text(surface, "Resistances", dp.x + 14, dy, BEAST_KNOWN, 12, bold=True)
            dy += 18

            resistances = e.get("resistances", {})
            immunities  = e.get("status_immunities", [])
            ELEMENTS = ["fire", "ice", "lightning", "divine", "shadow",
                        "nature", "arcane", "piercing", "slashing", "blunt"]
            col_w = (dp_w - 28) // 3
            for idx, elem in enumerate(ELEMENTS):
                val = resistances.get(elem, 1.0)
                if val == 0.0:
                    val_str, val_col = "Immune", (100, 200, 255)
                elif val < 1.0:
                    val_str, val_col = f"{val:.0%}", (100, 220, 130)
                elif val > 1.0:
                    val_str, val_col = f"{val:.0%}", (220, 100, 80)
                else:
                    val_str, val_col = "Normal", (100, 95, 90)
                col_x = dp.x + 14 + (idx % 3) * col_w
                row_y = dy + (idx // 3) * 16
                if dp.y <= row_y < dp.y + ph:
                    draw_text(surface, f"{elem.capitalize()}:", col_x, row_y, BEAST_UNKNOWN, 10)
                    draw_text(surface, val_str, col_x + 72, row_y, val_col, 10)
            dy += ((len(ELEMENTS) + 2) // 3) * 16 + 6

            if immunities:
                dy += 4
                if dp.y <= dy < dp.y + ph:
                    draw_text(surface, "Status Immune: " + ", ".join(immunities),
                              dp.x + 14, dy, (100, 200, 255), 10)
                dy += 16

            abilities = e.get("abilities", [])
            if abilities:
                pygame.draw.line(surface, DIVIDER, (dp.x + 10, dy), (dp.right - 10, dy))
                dy += 8
                draw_text(surface, "Abilities", dp.x + 14, dy, BEAST_KNOWN, 12, bold=True)
                dy += 18
                for ab in abilities:
                    ab_name = ab.get("name") or ab.get("description", "Unknown")
                    ab_desc = ab.get("description", "")
                    if dp.y <= dy < dp.y + ph:
                        draw_text(surface, f"• {ab_name}", dp.x + 18, dy,
                                  (200, 190, 130), 11, bold=True)
                    dy += 15
                    if ab_desc:
                        for line in _wrap_text(ab_desc, dp_w - 50, 10):
                            if dp.y <= dy < dp.y + ph:
                                draw_text(surface, line, dp.x + 28, dy, (140, 135, 120), 10)
                            dy += 14
                        dy += 2

        surface.set_clip(clip_dp)

        # Scrollbar
        content_h = dy - (dp.y + 10 - self.scroll_detail) + self.scroll_detail + 20
        if content_h > ph:
            ratio = ph / content_h
            bar_h = max(24, int(ph * ratio))
            bar_y = dp.y + int(self.scroll_detail / content_h * ph)
            bar_y = min(bar_y, dp.y + ph - bar_h)
            pygame.draw.rect(surface, (50, 45, 70),
                             pygame.Rect(dp.right - 6, bar_y, 4, bar_h), border_radius=2)

    def handle_click(self, mx, my):
        close_r = pygame.Rect(SCREEN_W - 112, 48, 96, 30)
        if close_r.collidepoint(mx, my):
            self.finished = True
            return "close"

        for i, key in enumerate(["quests", "lore", "bestiary", "guild"]):
            r = pygame.Rect(20 + i * 116, 48, 108, 30)
            if r.collidepoint(mx, my):
                self.tab          = key
                self.scroll_list  = 0
                self.scroll_detail= 0
                return None

        if self.tab == "quests":
            for rect, qid in self._list_rects:
                if rect.collidepoint(mx, my):
                    self.selected_qid  = qid
                    self.scroll_detail = 0
                    return None
        elif self.tab == "lore":
            for rect, lid in self._lore_rects:
                if rect.collidepoint(mx, my):
                    self.selected_lid  = lid
                    self.scroll_detail = 0
                    return None
        else:
            for rect, eid in self._beast_rects:
                if rect.collidepoint(mx, my):
                    self.selected_eid  = eid
                    self.scroll_detail = 0
                    return None
        return None

    def handle_scroll(self, direction, mx=None, my=None):
        """Scroll sidebar (left side) or detail (right side) based on mouse x."""
        sidebar_x_max = 28 + SIDEBAR_W
        if mx is not None and mx <= sidebar_x_max:
            self.scroll_list  = max(0, self.scroll_list  + direction * 26)
        else:
            self.scroll_detail = max(0, self.scroll_detail + direction * 26)
