"""
Realm of Shadows — Town Hub UI

Town locations:
  General Store — buy weapons, armor, consumables; sell inventory items
  Temple        — rest/heal (free), identify items (15g), remove curse (50g)
  Tavern        — hear rumors, flavor text
  Exit          — leave town (back to world/encounters)
"""
import random
import core.sound as sfx
import pygame
from ui.renderer import *
from core.classes import CLASSES
from core.identification import get_item_display_name
from data.shop_inventory import (
    GENERAL_STORE, TEMPLE, TAVERN, get_sell_price, get_town_shop,
)
from ui.town_backgrounds import get_town_bg, get_building_bg

# ═══════════════════════════════════════════════════════════════
#  COLORS
# ═══════════════════════════════════════════════════════════════

TOWN_BG      = (10, 8, 20)
SHOP_BG      = (15, 12, 28)
ITEM_BG      = (22, 18, 40)
ITEM_HOVER   = (40, 34, 70)
BUY_COL      = (80, 220, 120)
SELL_COL     = (220, 180, 80)
HEAL_COL     = (80, 255, 180)
RUMOR_COL    = (180, 160, 220)
# Shared stat/bar colors (mirrors camp_ui.py values)
STAT_LABEL   = (160, 150, 180)
STAT_VAL     = (220, 220, 200)
HP_BAR       = (50, 180, 80)
HP_BAR_BG    = (30, 40, 30)
MP_BAR       = (60, 100, 200)
SP_BAR       = (200, 160, 60)

# Town display info
TOWN_DISPLAY = {
    "briarhollow": {
        "name": "Town of Briarhollow",
        "desc": "A quiet settlement at the edge of the wilds.",
    },
    "woodhaven": {
        "name": "Woodhaven",
        "desc": "A village sheltered beneath the ancient Great Grove.",
    },
    "ironhearth": {
        "name": "Ironhearth",
        "desc": "A mining town built on iron and stubbornness.",
    },
    "greenwood": {
        "name": "Greenwood",
        "desc": "A remote wilderness outpost. Few roads lead here.",
    },
    "saltmere": {
        "name": "Saltmere",
        "desc": "A rough port town where no questions are asked.",
    },
    "sanctum": {
        "name": "Sanctum",
        "desc": "A holy city built around the Grand Cathedral of Light.",
    },
    "crystalspire": {
        "name": "Crystalspire",
        "desc": "City of towers and ley lines. Home of the Mage Academy.",
    },
    "thornhaven": {
        "name": "Thornhaven — Capital of Aldenmere",
        "desc": "The seat of the Governor's power. The largest city in the realm.",
    },
    "emberveil": {
        "name": "Emberveil",
        "desc": "A volcanic outpost. The air smells of sulphur. The smith knows things.",
    },
    "the_anchorage": {
        "name": "The Anchorage",
        "desc": "A fishing village at the edge of the known sea. Researchers and fisherfolk.",
    },
    "the_holdfast": {
        "name": "The Holdfast",
        "desc": "A fortified ruin in the Ashlands. The last safe ground before the Spire.",
    },
}


# Per-town indoor NPCs shown in building service views.
# Format: town_id → {building_type: {"name", "npc_type", "color", "dialogue_id"}}
BUILDING_NPCS = {
    "briarhollow": {
        "inn":      {"name":"Innkeeper Bess",     "npc_type":"innkeeper", "color":(180,140,60),  "dialogue_id":"bess"},
        "shop":     {"name":"Merchant Gilda",     "npc_type":"merchant",  "color":(120,180,80),  "dialogue_id":"merchant_gilda"},
        "forge":    {"name":"Forgemaster Dunn",   "npc_type":"forger",    "color":(200,120,40),  "dialogue_id":"forgemaster_dunn"},
        "temple":   {"name":"Priest Korvan",      "npc_type":"priest",    "color":(100,180,220), "dialogue_id":"priest_korvan"},
        "tavern":   {"name":"Barkeep Holt",       "npc_type":"barkeep",   "color":(160,100,180), "dialogue_id":"barkeep_holt"},
        "guild":    {"name":"Warden Liaison",     "npc_type":"warden",    "color":(120,180,120), "dialogue_id":"warden_liaison"},
    },
    "woodhaven": {
        "inn":      {"name":"Innkeeper Jessa",    "npc_type":"innkeeper", "color":(160,140,80),  "dialogue_id":"innkeeper_jessa"},
        "shop":     {"name":"Merchant Kira",      "npc_type":"merchant",  "color":(120,160,80),  "dialogue_id":"merchant_kira"},
        "forge":    {"name":"Smith Wren",         "npc_type":"forger",    "color":(200,140,60),  "dialogue_id":"smith_wren"},
        "temple":   {"name":"Druid Rowan",        "npc_type":"priest",    "color":(80,180,100),  "dialogue_id":"druid_rowan"},
        "tavern":   {"name":"Barkeep Magda",      "npc_type":"barkeep",   "color":(160,80,120),  "dialogue_id":"barkeep_magda"},
        "guild":    {"name":"Warden Liaison",     "npc_type":"warden",    "color":(120,180,120), "dialogue_id":"warden_liaison"},
    },
    "ironhearth": {
        "inn":      {"name":"Innkeeper Bron",     "npc_type":"innkeeper", "color":(140,120,80),  "dialogue_id":"innkeeper_bron"},
        "shop":     {"name":"Armorer Ygrith",     "npc_type":"merchant",  "color":(140,140,160), "dialogue_id":"armorer_ygrith"},
        "forge":    {"name":"Master Smith Thardin","npc_type":"forger",   "color":(220,100,40),  "dialogue_id":"master_smith_thardin"},
        "temple":   {"name":"Elder Thom",         "npc_type":"elder",     "color":(160,160,200), "dialogue_id":"elder_thom"},
        "tavern":   {"name":"Barkeep Sylla",      "npc_type":"barkeep",   "color":(180,100,60),  "dialogue_id":"sylla"},
        "guild":    {"name":"Guildmaster",        "npc_type":"guildmaster","color":(180,160,60), "dialogue_id":"guildmaster_ironhearth"},
    },
    "crystalspire": {
        "inn":      {"name":"Innkeeper Bron",     "npc_type":"innkeeper", "color":(100,120,200), "dialogue_id":"innkeeper_bron"},
        "shop":     {"name":"Arcanist Veleth",    "npc_type":"mage",      "color":(120,100,220), "dialogue_id":"crystal_scholar"},
        "forge":    {"name":"Forgemaster Dunn",   "npc_type":"forger",    "color":(160,120,220), "dialogue_id":"forgemaster_dunn"},
        "temple":   {"name":"Oracle Thessaly",    "npc_type":"priestess", "color":(140,180,220), "dialogue_id":"crystalspire_priest"},
        "tavern":   {"name":"Barkeep Holt",       "npc_type":"barkeep",   "color":(100,120,180), "dialogue_id":"barkeep_holt"},
        "jobboard": {"name":"Guild Secretary Hald","npc_type":"merchant",  "color":(100,160,200), "dialogue_id":"apprentice_mage"},
        "guild":    {"name":"Warden Liaison",     "npc_type":"warden",    "color":(120,180,120), "dialogue_id":"warden_liaison"},
    },
    "thornhaven": {
        "inn":      {"name":"Innkeeper Jessa",    "npc_type":"innkeeper", "color":(180,160,80),  "dialogue_id":"innkeeper_thornhaven"},
        "shop":     {"name":"Trader Finn",        "npc_type":"merchant",  "color":(160,140,80),  "dialogue_id":"trader_finn"},
        "forge":    {"name":"Armorer Ygrith",     "npc_type":"forger",    "color":(180,140,60),  "dialogue_id":"armorer_ygrith"},
        "temple":   {"name":"Priestess Alia",     "npc_type":"priestess", "color":(200,180,100), "dialogue_id":"priestess_alia"},
        "tavern":   {"name":"Barkeep Magda",      "npc_type":"barkeep",   "color":(160,140,80),  "dialogue_id":"barkeep_magda"},
        "jobboard": {"name":"Chapter Master Aldren","npc_type":"guildmaster","color":(180,120,60),"dialogue_id":"guildmaster_oren"},
        "guild":    {"name":"Warden Liaison",     "npc_type":"warden",    "color":(120,180,120), "dialogue_id":"warden_liaison"},
    },
    "sanctum": {
        "inn":      {"name":"Innkeeper Bess",     "npc_type":"innkeeper", "color":(200,200,180), "dialogue_id":"innkeeper_bron"},
        "shop":     {"name":"Merchant Kira",      "npc_type":"merchant",  "color":(180,180,160), "dialogue_id":"merchant_kira"},
        "temple":   {"name":"Priestess Alia",     "npc_type":"priestess", "color":(220,200,140), "dialogue_id":"priestess_alia"},
        "tavern":   {"name":"Barkeep Holt",       "npc_type":"barkeep",   "color":(180,160,120), "dialogue_id":"barkeep_holt"},
        "guild":    {"name":"Holy Knight",        "npc_type":"guard",     "color":(200,200,160), "dialogue_id":"holy_knight"},
    },
    "saltmere": {
        "inn":      {"name":"Innkeeper Bron",     "npc_type":"innkeeper", "color":(100,140,160), "dialogue_id":"innkeeper_bron"},
        "shop":     {"name":"Trader Finn",        "npc_type":"merchant",  "color":(120,140,160), "dialogue_id":"trader_finn"},
        "forge":    {"name":"Foreman Drek",       "npc_type":"forger",    "color":(140,160,160), "dialogue_id":"foreman_drek"},
        "tavern":   {"name":"Barkeep Sylla",      "npc_type":"barkeep",   "color":(100,160,180), "dialogue_id":"sylla"},
        "guild":    {"name":"Guildmaster Sable",  "npc_type":"guildmaster","color":(100,180,160),"dialogue_id":"guildmaster_sable"},
    },
    "greenwood": {
        "inn":      {"name":"Ranger Cael",        "npc_type":"ranger",    "color":(80,160,80),   "dialogue_id":"ranger_cael"},
        "shop":     {"name":"Merchant Gilda",     "npc_type":"merchant",  "color":(100,160,80),  "dialogue_id":"merchant_gilda"},
        "temple":   {"name":"Druid Rowan",        "npc_type":"priest",    "color":(80,180,100),  "dialogue_id":"druid_rowan"},
        "guild":    {"name":"Scout Feryn",        "npc_type":"ranger",    "color":(100,160,80),  "dialogue_id":"scout_feryn"},
    },
    "emberveil": {
        "inn":      {"name":"Innkeeper Bess",     "npc_type":"innkeeper", "color":(180,120,60),  "dialogue_id":"innkeeper_bron"},
        "shop":     {"name":"Foreman Drek",       "npc_type":"merchant",  "color":(160,120,80),  "dialogue_id":"foreman_drek"},
        "forge":    {"name":"Master Smith Thardin","npc_type":"forger",   "color":(220,100,20),  "dialogue_id":"master_smith_thardin"},
        "guild":    {"name":"Warden Liaison",     "npc_type":"warden",    "color":(120,180,120), "dialogue_id":"warden_liaison"},
    },
    "the_anchorage": {
        "inn":      {"name":"Innkeeper Bron",     "npc_type":"innkeeper", "color":(100,160,180), "dialogue_id":"innkeeper_bron"},
        "tavern":   {"name":"Barkeep Holt",       "npc_type":"barkeep",   "color":(100,140,180), "dialogue_id":"barkeep_holt"},
        "guild":    {"name":"Warden Liaison",     "npc_type":"warden",    "color":(120,180,120), "dialogue_id":"warden_liaison"},
    },
    "the_holdfast": {
        "inn":      {"name":"Ranger Warden",      "npc_type":"ranger",    "color":(140,120,80),  "dialogue_id":"warden_liaison"},
        "guild":    {"name":"Warden Liaison",     "npc_type":"warden",    "color":(120,180,120), "dialogue_id":"warden_liaison"},
    },
}

RARITY_COLORS = {
    "common":    CREAM,
    "uncommon":  (80, 220, 80),
    "rare":      (80, 140, 255),
    "epic":      (180, 80, 255),
    "legendary": (255, 180, 40),
}

# ═══════════════════════════════════════════════════════════════
#  TOWN UI
# ═══════════════════════════════════════════════════════════════

class TownUI:
    # Views
    VIEW_HUB = "hub"
    VIEW_WALK = "walk"       # walkable town map
    VIEW_SHOP = "shop"
    VIEW_SHOP_BUY = "shop_buy"
    VIEW_SHOP_SELL = "shop_sell"
    VIEW_TEMPLE = "temple"
    VIEW_TAVERN = "tavern"
    VIEW_INN = "inn"
    VIEW_INN_LEVELUP = "inn_levelup"
    VIEW_INN_LEVELUP_RESULT = "inn_levelup_result"   # fanfare screen
    VIEW_BRANCH_CHOICE = "branch_choice"              # ability fork selection
    VIEW_CLASSTREE = "classtree"                      # class progression viewer
    VIEW_CLASS_CHOOSE = "class_choose"                 # advanced class selection screen
    VIEW_FORGE = "forge"
    VIEW_FORGE_CRAFT = "forge_craft"
    VIEW_JOBBOARD = "jobboard"
    VIEW_FORGE_UPGRADE = "forge_upgrade"
    VIEW_FORGE_ENCHANT = "forge_enchant"
    VIEW_FORGE_REPAIR  = "forge_repair"
    VIEW_GUILD = "guild"
    VIEW_GUILD_TRANSITION = "guild_transition"
    VIEW_INN_TRAINER   = "inn_trainer"       # skill/ability training
    VIEW_INN_CHARSHEET = "inn_charsheet"     # consolidated character sheet

    def __init__(self, party, town_id="briarhollow"):
        self.party = party
        self.message = ""
        self.msg_timer = 0
        self.msg_color = CREAM
        self.finished = False
        self.pending_quest_completions = []  # drained by Game._notify_quests_done each draw

        # Shop state
        self.shop_tab = "weapons"  # weapons, armor, consumables
        self.shop_scroll = 0
        self.shop_char_idx = 0    # which character is selected for buying
        self.sell_char = 0
        self.sell_scroll = 0
        self.sold_items = []  # items sold by player, available for buyback

        # Temple state
        self.id_char = 0
        self.id_scroll = 0

        # Inn state
        self.inn_result = None  # stores rest result for display
        self.levelup_queue = []  # characters ready to level up
        self.levelup_current = 0  # index in queue
        self.levelup_free_stat = None  # selected stat for free point
        self.levelup_summary = None  # result dict from apply_level_up (for fanfare)
        self.branch_pending_char = None  # character awaiting branch choice
        self.branch_pending_opts = None  # [opt_A, opt_B] for branch screen
        self.branch_hover_idx = -1       # hovered option index
        # Class tree viewer
        self.classtree_char_idx = 0  # which party member to show
        self._tc_char_idx  = 0     # class_choose: which character is transitioning
        self._tc_selected  = None  # class_choose: currently hovered/selected class name
        self._tc_confirmed = False # class_choose: confirm button pressed
        self._tc_card_rects = []   # [(rect, class_name, can)]
        self._tc_close_rect = None # class_choose: close (X) button on expanded card
        # Trainer state
        self.trainer_char_idx = 0    # which character is training
        self.trainer_scroll = 0      # scroll offset for ability list
        # Character sheet state
        self.charsheet_idx = 0       # which character is shown

        # Tavern state
        self.tavern_drinks = {}      # patron_name -> drinks bought (int)
        self.tavern_selected = 0     # index of selected patron/tab
        self.tavern_tab = "patrons"  # "patrons" | "recruit" | "party"
        self.tavern_recruit_sel = 0
        self.tavern_party_sel = 0
        # Story-aware rumor — set on tavern open; pre-populate so it's never blank
        from data.story_data import get_rumor as _gr
        try:
            self.current_rumor = _gr()
        except Exception:
            self.current_rumor = "Strange times. Buy a round and listen."
        self._tavern_recruits = None        # cached recruit list
        self._tavern_recruits_at_level = -1 # party avg level when cache was built

        # NPC dialogue state
        self.active_dialogue = None  # DialogueUI when talking to an NPC
        self.town_id = town_id
        party_classes = [c.class_name for c in party if hasattr(c, "class_name")]
        self.shop = get_town_shop(town_id, party_classes)  # Town-specific shop inventory

        # Forge state
        self.forge_scroll = 0
        self.forge_item_scroll = 0
        self.forge_selected_item = None
        self.forge_selected_enchant = None

        # Always use hub menu — walkable town removed
        self.town_data = None
        # Safe defaults for walk attributes (walk mode disabled but referenced in draw)
        self.walk_x = 0
        self.walk_y = 0
        self.walk_facing = "down"
        self.walk_anim_t = 0
        self.walk_interact_msg = ""
        self.walk_interact_timer = 0
        self.current_bld_indoor_npc   = None
        self.current_bld_name         = ""
        self._bld_npc_portrait_rect   = None
        self.walk_tile_size = 24
        # Load walkable map data if this town has one
        from data.town_maps import get_town_data
        self.town_data = get_town_data(self.town_id)
        if self.town_data:
            spawn = self.town_data.get("spawn", (2, 2))
            self.walk_x, self.walk_y = spawn
        self._return_to_town()

    # ─────────────────────────────────────────────────────────
    #  MAIN DRAW
    # ─────────────────────────────────────────────────────────

    # ─── Background helpers ────────────────────────────────────────────

    def _draw_town_exterior(self, surface):
        """Draw town exterior background behind the hub menu.
        Full-screen. Falls back to plain dark fill if no image found."""
        bg = get_town_bg(self.town_id, SCREEN_W, SCREEN_H)
        if bg:
            surface.blit(bg, (0, 0))
            # Darken slightly so UI text stays readable
            overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 80))
            surface.blit(overlay, (0, 0))
        else:
            surface.fill((12, 10, 20))

    def _draw_building_interior(self, surface, building_type: str):
        """Draw split-screen building interior.
        Left 40% is reserved for the functional UI panel (caller draws on it).
        Right 60% shows the building interior image, or plain background.
        Returns the Rect of the left UI panel area."""
        panel_w = int(SCREEN_W * 0.42)
        scene_x = panel_w
        scene_w = SCREEN_W - scene_x

        # Right side — building interior scene
        bg = get_building_bg(self.town_id, building_type, scene_w, SCREEN_H)
        if bg:
            surface.blit(bg, (scene_x, 0))
            # Subtle vignette on left edge of scene so panel blends in
            vignette = pygame.Surface((60, SCREEN_H), pygame.SRCALPHA)
            for x in range(60):
                alpha = int(180 * (1 - x / 60))
                pygame.draw.line(vignette, (0, 0, 0, alpha), (x, 0), (x, SCREEN_H))
            surface.blit(vignette, (scene_x, 0))
        else:
            # No image — plain dark right side
            pygame.draw.rect(surface, (8, 6, 18), (scene_x, 0, scene_w, SCREEN_H))

        # Left side — solid dark panel for functional UI
        pygame.draw.rect(surface, (10, 8, 22), (0, 0, panel_w, SCREEN_H))
        # Divider line
        pygame.draw.line(surface, (40, 36, 60), (panel_w, 0), (panel_w, SCREEN_H), 1)

        return pygame.Rect(0, 0, panel_w, SCREEN_H)

    def draw(self, surface, mx, my, dt):
        self.msg_timer = max(0, self.msg_timer - dt)
        if getattr(self, "_inn_save_timer", 0) > 0:
            self._inn_save_timer = max(0, self._inn_save_timer - dt)

        # If dialogue is active, render it instead
        if self.active_dialogue and not self.active_dialogue.finished:
            self.active_dialogue.draw(surface, mx, my, dt)
            return

        # Clear dialogue if finished — distribute any quest rewards
        if self.active_dialogue and self.active_dialogue.finished:
            self.active_dialogue = None
            try:
                from core.story_flags import auto_advance_quests
                done = auto_advance_quests(self.party)
                self.pending_quest_completions.extend(done)
            except Exception:
                pass

        surface.fill(TOWN_BG)

        if self.view == self.VIEW_WALK:
            self.walk_anim_t += dt
            self.walk_interact_timer = max(0, self.walk_interact_timer - dt)
            self._draw_walk(surface, mx, my)
        elif self.view == self.VIEW_HUB:
            self._draw_hub(surface, mx, my)
        elif self.view == self.VIEW_SHOP:
            self._draw_shop_menu(surface, mx, my)
        elif self.view == self.VIEW_SHOP_BUY:
            self._draw_shop_buy(surface, mx, my)
        elif self.view == self.VIEW_SHOP_SELL:
            self._draw_shop_sell(surface, mx, my)
        elif self.view == self.VIEW_TEMPLE:
            self._draw_temple(surface, mx, my)
        elif self.view == self.VIEW_TAVERN:
            self._draw_tavern(surface, mx, my)
        elif self.view == self.VIEW_INN:
            self._draw_inn(surface, mx, my)
        elif self.view == self.VIEW_INN_LEVELUP:
            self._draw_inn_levelup(surface, mx, my)
        elif self.view == self.VIEW_INN_LEVELUP_RESULT:
            self._draw_levelup_result(surface, mx, my)
        elif self.view == self.VIEW_BRANCH_CHOICE:
            self._draw_branch_choice(surface, mx, my)
        elif self.view == self.VIEW_CLASSTREE:
            self._draw_classtree(surface, mx, my)
        elif self.view == self.VIEW_CLASS_CHOOSE:
            self._draw_class_choose(surface, mx, my)
        elif self.view in (self.VIEW_FORGE, self.VIEW_FORGE_CRAFT,
                           self.VIEW_FORGE_UPGRADE, self.VIEW_FORGE_ENCHANT,
                           self.VIEW_FORGE_REPAIR):
            self._draw_forge(surface, mx, my)
        elif self.view == self.VIEW_JOBBOARD:
            self._draw_jobboard(surface, mx, my)
        elif self.view in (self.VIEW_GUILD, self.VIEW_GUILD_TRANSITION):
            self._draw_guild(surface, mx, my)
        elif self.view == self.VIEW_INN_TRAINER:
            self._draw_inn_trainer(surface, mx, my)
        elif self.view == self.VIEW_INN_CHARSHEET:
            self._draw_inn_charsheet(surface, mx, my)

        # Message bar
        if self.message and self.msg_timer > 0:
            draw_text(surface, self.message, SCREEN_W // 2 - 250,
                      SCREEN_H - 30, self.msg_color, 15)

    # ─────────────────────────────────────────────────────────
    #  HUB — Main town menu
    # ─────────────────────────────────────────────────────────

    def _get_town_locations(self):
        """Return the list of (loc_key, display_name, desc, bg_tint, accent)
        for this town's hub — unique names per town, conditional buildings."""

        # Per-town building names and descriptions
        # Format: town_id → {building_key: (name, desc)}
        TOWN_BUILDINGS = {
            "briarhollow": {
                "inn":      ("The Wanderer's Rest",    "Rest, train, and save your progress"),
                "shop":     ("Harrow's Trading Post",  "Weapons, armor, and trail supplies"),
                "forge":    ("Aldric's Smithy",        "Repairs, upgrades, and basic crafting"),
                "temple":   ("Temple of the Flame",    "Healing, identification, and rites"),
                "tavern":   ("The Mossy Flagon",       "Rumors, ale, and warmth"),
                "jobboard": ("Aldric's Notice Board",  "Local work and contracts"),
                "guild":    ("Wardens' Post",          "Register with the Guild, train, and advance"),
            },
            "woodhaven": {
                "inn":      ("The Canopy Rest",        "Rest, train, and save your progress"),
                "shop":     ("Mira's Forest Goods",   "Provisions and wilderness gear"),
                "forge":    ("Oakbrand Smithy",        "Repairs and ironwork"),
                "temple":   ("Grove Shrine",           "Healing and nature rites"),
                "tavern":   ("The Hollow Stump",       "Rumors and forestfolk company"),
                "jobboard": ("Village Notice Post",    "Work posted by the village elder"),
                "guild":    ("Wardens' Post",          "Register with the Guild, train, and advance"),
            },
            "ironhearth": {
                "inn":      ("The Anvil & Hearth",     "Rest and recovery — dwarven hospitality"),
                "shop":     ("Stonebacker's Goods",    "Dwarven-quality equipment and supplies"),
                "forge":    ("The Deep Forge",         "Master crafting, upgrades, and enchanting"),
                "temple":   ("Hall of the Stone Father","Dwarven rites and restoration"),
                "tavern":   ("The Iron Mug",           "Strong ale and louder rumors"),
                "guild":    ("Wardens' Post",          "Register with the Guild, train, and advance"),
            },
            "crystalspire": {
                "inn":      ("The Ley Line Lodge",     "Rest, train, and save your progress"),
                "shop":     ("Arcane Provisions",      "Rare components and magical supplies"),
                "forge":    ("Resonance Forge",        "Enchanting and high-tier upgrades"),
                "temple":   ("The Spire Shrine",       "Healing and arcane identification"),
                "tavern":   ("The Flickering Glass",   "Rumors among mages and scholars"),
                "jobboard": ("Academy Commission Board","Research bounties and arcane contracts"),
            },
            "thornhaven": {
                "inn":      ("The Governor's Rest",    "Rest, train, and save your progress"),
                "shop":     ("Imperial Supply House",  "Well-stocked city equipment"),
                "forge":    ("Tanner's Armory",        "Imperial-grade crafting and repair"),
                "temple":   ("Cathedral Annex",        "Full temple services in the capital"),
                "tavern":   ("The Bronze Lantern",     "Political gossip and city news"),
                "jobboard": ("Imperial Contracts Office","Imperial-sanctioned work and bounties"),
            },
            "sanctum": {
                "inn":      ("The Pilgrim's House",    "Rest and reflection"),
                "shop":     ("Cathedral Market",       "Holy goods and supplies"),
                "temple":   ("The Grand Cathedral",    "Full rites, powerful identification, and restoration"),
                "tavern":   ("The Quiet Cup",          "Subdued conversation near the cathedral"),
                "guild":    ("Wardens' Post",          "Register with the Guild, train, and advance"),
            },
            "saltmere": {
                "inn":      ("The Saltwater Bunk",     "Rest — no questions asked"),
                "shop":     ("Finn's Dockside Goods",  "Salvage, supplies, and contraband-adjacent wares"),
                "forge":    ("Harker's Rivet Shop",    "Ship repairs, weapons, no receipts"),
                "tavern":   ("The Bilge",              "The worst rumors and the best leads"),
                "guild":    ("Wardens' Post",          "Register with the Guild, train, and advance"),
            },
            "greenwood": {
                "inn":      ("The Ranger's Post",      "Rest at the outpost"),
                "shop":     ("Trail Cache",            "Survival gear and expedition supplies"),
                "temple":   ("Wayside Shrine",         "Basic healing and rites"),
                "guild":    ("Wardens' Post",          "Register with the Guild, train, and advance"),
            },
            "emberveil": {
                "inn":      ("The Ash Bunk",           "Rest near the volcano — it's fine"),
                "shop":     ("Renn's Supplies",        "Volcanic materials and Act 3 provisions"),
                "forge":    ("Renn's Forge",           "Master-level volcanic-steel crafting"),
                "guild":    ("Wardens' Post",          "Register with the Guild, train, and advance"),
            },
            "the_anchorage": {
                "inn":      ("The Researcher's Bunk",  "Rest at the fishing outpost"),
                "tavern":   ("The Salt & Scholar",     "Fishermen and Crystalspire researchers"),
                "guild":    ("Wardens' Post",          "Register with the Guild, train, and advance"),
            },
            "the_holdfast": {
                "inn":      ("The Commander's Quarters","Rest — the last safe ground"),
                "guild":    ("Wardens' Command Post",  "The final Guild post before the Spire"),
            },
        }

        # Default fallbacks for towns not fully defined
        DEFAULT_NAMES = {
            "inn":      ("The Inn",         "Rest, train, and save your progress"),
            "shop":     ("General Store",   "Buy and sell weapons, armor, and supplies"),
            "forge":    ("The Forge",       "Craft, upgrade, and enchant equipment"),
            "temple":   ("Temple",          "Heal, identify items, remove curses"),
            "tavern":   ("The Tavern",      "Hear rumors and rest your feet"),
            "jobboard": ("Job Board",       "Browse available quests and contracts"),
        }

        town_blds = TOWN_BUILDINGS.get(self.town_id, {})

        # Accent colours per building type
        ACCENTS = {
            "inn":      (220, 180, 80),
            "shop":     (140, 200, 120),
            "forge":    (255, 140, 40),
            "temple":   (120, 200, 230),
            "tavern":   (180, 120, 220),
            "jobboard": (80, 200, 120),
            "guild":    (120, 200, 160),
        }
        BG_TINTS = {
            "inn":      (100, 80, 40),
            "shop":     (60, 100, 60),
            "forge":    (140, 80, 40),
            "temple":   (50, 100, 120),
            "tavern":   (100, 60, 100),
            "jobboard": (40, 80, 60),
            "guild":    (40, 100, 70),
        }

        # Build location list: only buildings this town has defined
        locations = []
        for key in ["inn", "shop", "forge", "temple", "tavern", "jobboard", "guild"]:
            if key in town_blds or self.town_id not in TOWN_BUILDINGS:
                name, desc = town_blds.get(key, DEFAULT_NAMES.get(key, (key.title(), "")))
                locations.append((key, name, desc, BG_TINTS.get(key, (40,60,80)), ACCENTS.get(key, (140,180,140))))

        # Always append Party and Leave Town
        locations.append(("party", "Party", "View and manage your characters", (40, 60, 80), (80, 160, 220)))
        locations.append(("exit",  "Leave Town", "Return to the wilds", (80, 40, 40), (200, 80, 80)))

        return locations

    def _draw_hub(self, surface, mx, my):
        # ── Town exterior background ──────────────────────────────────
        self._draw_town_exterior(surface)

        # ── Left-side UI panel (semi-transparent) ─────────────────────
        panel_w = int(SCREEN_W * 0.42)
        panel = pygame.Surface((panel_w, SCREEN_H), pygame.SRCALPHA)
        panel.fill((8, 6, 18, 210))
        surface.blit(panel, (0, 0))

        town_info = TOWN_DISPLAY.get(self.town_id, TOWN_DISPLAY["briarhollow"])
        PAD  = 28          # left margin inside panel
        BTN_W = panel_w - PAD * 2   # button fills panel width minus margins

        draw_text(surface, town_info["name"], PAD, 28, GOLD, 26, bold=True)
        draw_text(surface, town_info["desc"], PAD, 62, GREY, 13,
                  max_width=panel_w - PAD * 2)

        # Party gold
        total_gold = sum(c.gold for c in self.party)
        draw_text(surface, f"Party Gold: {total_gold}g",
                  PAD, 88, DIM_GOLD, 14)

        # Location buttons — within the left panel
        locations = self._get_town_locations()

        by = 116
        btn_h = 64
        gap   = 8
        for i, (loc_key, name, desc, bg_tint, accent) in enumerate(locations):
            btn_rect = pygame.Rect(PAD, by + i * (btn_h + gap), BTN_W, btn_h)
            hover = btn_rect.collidepoint(mx, my)

            bg = (bg_tint[0] + 20, bg_tint[1] + 20, bg_tint[2] + 20) if hover else bg_tint
            border = accent if hover else PANEL_BORDER

            pygame.draw.rect(surface, bg, btn_rect, border_radius=5)
            pygame.draw.rect(surface, border, btn_rect, 2, border_radius=5)

            draw_text(surface, name, btn_rect.x + 16, btn_rect.y + 10,
                      accent if hover else CREAM, 17, bold=True)
            draw_text(surface, desc, btn_rect.x + 16, btn_rect.y + 34,
                      GREY, 11, max_width=BTN_W - 24)

        # ── Menu button (top-right) ──
        menu_r = pygame.Rect(SCREEN_W - 160, 20, 140, 38)
        mhov = menu_r.collidepoint(mx, my)
        pygame.draw.rect(surface, (30, 28, 45) if not mhov else (50, 46, 70),
                         menu_r, border_radius=4)
        pygame.draw.rect(surface, PANEL_BORDER if not mhov else GOLD,
                         menu_r, 2, border_radius=4)
        _mf = get_font(16, bold=True)
        _ms = _mf.render("Menu [M]", True, GOLD if mhov else CREAM)
        surface.blit(_ms, (menu_r.x + (menu_r.w - _ms.get_width())//2,
                            menu_r.y + (menu_r.h - _ms.get_height())//2))

        # ── NPC panel — right side of scene, over background ──────────
        from data.story_data import get_town_npcs
        npcs = get_town_npcs(self.town_id)
        if npcs:
            npc_x = panel_w + 30
            # Semi-transparent backing for readability
            npc_panel_w = 230
            npc_panel_h = 32 + len(npcs) * 62
            npc_bg = pygame.Surface((npc_panel_w, npc_panel_h), pygame.SRCALPHA)
            npc_bg.fill((6, 4, 14, 180))
            surface.blit(npc_bg, (npc_x - 8, 130))
            draw_text(surface, "People in Town", npc_x, 136, GOLD, 14, bold=True)
            for j, (npc_id, npc_data) in enumerate(npcs):
                nr = pygame.Rect(npc_x, 168 + j * 62, 210, 54)
                hover = nr.collidepoint(mx, my)
                pc = npc_data.get("portrait_color", (80, 80, 80))
                bg = (pc[0] // 4 + 10, pc[1] // 4 + 10, pc[2] // 4 + 10)
                if hover:
                    bg = (bg[0] + 15, bg[1] + 15, bg[2] + 15)
                pygame.draw.rect(surface, bg, nr, border_radius=4)
                pygame.draw.rect(surface, pc if hover else PANEL_BORDER, nr, 2, border_radius=4)
                # Portrait indicator
                pi = pygame.Rect(nr.x + 5, nr.y + 5, 44, 44)
                pygame.draw.rect(surface, pc, pi, border_radius=3)
                initial = npc_data["name"][0]
                iw = get_font(22).size(initial)[0]
                draw_text(surface, initial, pi.x + (44 - iw) // 2, pi.y + 10,
                          WHITE, 22, bold=True)
                draw_text(surface, npc_data["name"], nr.x + 56, nr.y + 6, CREAM, 16, bold=True, max_width=150)
                draw_text(surface, npc_data.get("title", ""), nr.x + 56, nr.y + 24,
                          DARK_GREY, 11, max_width=150)

        # Party summary at bottom
        self._draw_party_bar(surface, mx, my)

    def _draw_party_bar(self, surface, mx, my):
        """Compact party display at bottom of screen."""
        bar_y = SCREEN_H - 100
        pygame.draw.rect(surface, (15, 12, 30), (0, bar_y, SCREEN_W, 100))
        pygame.draw.line(surface, PANEL_BORDER, (0, bar_y), (SCREEN_W, bar_y))

        cw = (SCREEN_W - 40) // len(self.party)
        for i, c in enumerate(self.party):
            cx = 20 + i * cw
            cls = CLASSES[c.class_name]
            draw_text(surface, c.name, cx, bar_y + 8, cls["color"], 15, bold=True)
            draw_text(surface, f"Lv.{c.level} {c.class_name}", cx, bar_y + 24, GREY, 13, max_width=cw - 4)
            hp = c.resources.get("HP", 0)
            draw_text(surface, f"HP: {hp}  Gold: {c.gold}  Items: {len(c.inventory)}",
                      cx, bar_y + 40, DIM_GREEN, 11)

            # Status effect indicators
            from core.status_effects import get_status_display
            statuses = get_status_display(c)
            if statuses:
                sx = cx
                for sname, scolor in statuses[:3]:  # max 3 shown
                    draw_text(surface, sname, sx, bar_y + 56, scolor, 11)
                    sx += 80

    # ─────────────────────────────────────────────────────────
    #  WALKABLE TOWN MAP
    # ─────────────────────────────────────────────────────────

    def _draw_walk(self, surface, mx, my):
        from data.town_maps import (
            TILE_COLORS, TILE_TOP_COLORS, TT_GRASS, TT_WALL, TT_TREE, TT_DOOR,
            TT_FENCE, TT_PATH, TT_EXIT, TT_SIGN, TT_WATER, TT_BRIDGE,
            get_tile, get_building_at, get_npc_at, get_sign_at,
        )

        td = self.town_data
        map_area_h = SCREEN_H - 110  # leave room for UI bar at bottom
        tw, th = td["width"], td["height"]

        # Scale tile size so the map fills the available screen area,
        # but cap at 52 (too large looks bad) and floor at 24.
        ts_from_w = SCREEN_W // max(1, tw)
        ts_from_h = map_area_h // max(1, th)
        ts = max(24, min(ts_from_w, ts_from_h, 52))
        self.walk_tile_size = ts  # keep in sync so minimap uses same scale

        cam_x = self.walk_x - (SCREEN_W // ts) // 2
        cam_y = self.walk_y - (map_area_h // ts) // 2
        cam_x = max(0, min(tw - SCREEN_W // ts, cam_x))
        cam_y = max(0, min(th - map_area_h // ts, cam_y))

        # ══════════════════════════════════════════════════════════
        # TILE PASS — ground, paths, trees, water, special tiles
        # ══════════════════════════════════════════════════════════
        from data.town_maps import (
            TILE_COLORS, TILE_TOP_COLORS, TT_GRASS, TT_WALL, TT_DOOR,
            TT_TREE, TT_FENCE, TT_PATH, TT_EXIT, TT_SIGN, TT_WATER,
            TT_BRIDGE, BLD_INN, BLD_FORGE, BLD_TAVERN, BLD_TEMPLE,
            get_tile, get_building_at, get_npc_at, get_sign_at,
        )

        # td, ts, tw, th, cam_x, cam_y already computed above

        # pre-build building-to-wall-tile map for fast facade lookup
        bld_col_map = {}
        for bld in td["buildings"].values():
            c0, c1 = bld.get("wall_cols", (0, 0))
            r0, r1 = bld.get("wall_rows", (0, 0))
            for wr in range(r0, r1 + 1):
                for wc in range(c0, c1 + 1):
                    bld_col_map[(wc, wr)] = bld

        for sy in range(map_area_h // ts + 2):
            for sx in range(SCREEN_W // ts + 2):
                tx = cam_x + sx
                ty = cam_y + sy
                if not (0 <= ty < th and 0 <= tx < tw):
                    continue
                tile = td["map"][ty][tx] if tx < len(td["map"][ty]) else TT_WALL
                px = sx * ts
                py = sy * ts

                if tile == TT_GRASS:
                    shade = 3 if (tx + ty) % 2 == 0 else 0

                    # ── Building interior detection ─────────────────────────
                    # Grass tiles inside a building footprint are interior floors,
                    # NOT outdoor grass. Render as wooden planks or stone tiles.
                    bld_interior = bld_col_map.get((tx, ty))
                    if bld_interior:
                        bc_i  = bld_interior.get("color", (130, 110, 85))
                        btype_i = bld_interior.get("type", "")
                        # Interior floor colour — warmer/lighter than outer walls
                        floor_c_i = tuple(min(255, int(c * 0.88)) for c in bc_i)
                        pygame.draw.rect(surface, floor_c_i, (px, py, ts, ts))
                        if btype_i in ("temple", "guild", "castle"):
                            # Checkerboard stone tile floor
                            tc_i = tuple(max(0, c - 16) for c in floor_c_i)
                            if (tx + ty) % 2 == 0:
                                pygame.draw.rect(surface, tc_i,
                                    (px + 2, py + 2, ts // 2 - 2, ts // 2 - 2))
                                pygame.draw.rect(surface, tc_i,
                                    (px + ts//2 + 1, py + ts//2 + 1, ts//2 - 2, ts//2 - 2))
                        elif btype_i == "forge":
                            # Soot-darkened stone floor
                            dark_i = tuple(max(0, c - 30) for c in floor_c_i)
                            pygame.draw.rect(surface, dark_i, (px, py, ts, ts))
                            if (tx * 3 + ty * 7) % 5 == 0:
                                pygame.draw.line(surface, floor_c_i,
                                    (px, py + ts // 2), (px + ts, py + ts // 2), 1)
                        else:
                            # Wooden plank floor — horizontal grain
                            plank_c = tuple(max(0, c - 22) for c in floor_c_i)
                            step = max(3, ts // 4)
                            for bl in range(0, ts, step):
                                pygame.draw.line(surface, plank_c,
                                    (px, py + bl), (px + ts, py + bl), 1)
                            # Knot detail
                            if (tx * 5 + ty * 9) % 7 == 0:
                                kr = max(2, ts // 8)
                                pygame.draw.circle(surface, plank_c,
                                    (px + ts // 3, py + ts // 2), kr, 1)
                    else:
                        # ── Path stub for tiles directly beside a door ─────────
                        # Extend 2 tiles from any door for a wider, clearer walkway
                        is_door_adj = False
                        for _dx, _dy in ((-1,0),(1,0),(0,-1),(0,1),
                                         (-2,0),(2,0),(0,-2),(0,2)):
                            if get_tile(td, tx+_dx, ty+_dy) == TT_DOOR:
                                # Check direct adjacency to the door or 1-step from adj grass
                                is_door_adj = True
                                break
                        # Only render stub for tiles that form a clear path TO main road
                        # (must also be adj to a P tile or another stub)
                        has_path_conn = any(
                            get_tile(td, tx+_dx, ty+_dy) in (TT_PATH, TT_DOOR)
                            for _dx, _dy in ((-1,0),(1,0),(0,-1),(0,1))
                        )
                        if is_door_adj and has_path_conn:
                            # Wider, cleaner approach path
                            pygame.draw.rect(surface, (88, 75, 56), (px, py, ts, ts))
                            stone_sz = max(3, ts // 3 - 1)
                            for ox, oy in [(1, 1), (ts//2, 1), (1, ts//2), (ts//2, ts//2)]:
                                sc2 = (100, 86, 64) if (ox+oy)%2==0 else (80, 68, 50)
                                pygame.draw.rect(surface, sc2,
                                    (px+ox, py+oy, stone_sz, stone_sz), border_radius=1)
                                pygame.draw.rect(surface, (68, 58, 42),
                                    (px+ox, py+oy, stone_sz, stone_sz), 1, border_radius=1)
                        else:
                            # Normal outdoor grass
                            pygame.draw.rect(surface, (52 + shade, 78 + shade, 42 + shade),
                                (px, py, ts, ts))
                            if (tx * 7 + ty * 13) % 11 == 0:
                                pygame.draw.line(surface, (38, 62, 30),
                                    (px + ts//3, py + ts//2), (px + ts//3 - 2, py + ts//4), 1)
                                pygame.draw.line(surface, (38, 62, 30),
                                    (px + ts*2//3, py + ts//2), (px + ts*2//3 + 2, py + ts//4), 1)

                elif tile == TT_PATH:
                    pygame.draw.rect(surface, (95, 82, 62), (px, py, ts, ts))
                    stone_sz = max(4, ts // 3 - 1)
                    for ox, oy in [(1, 1), (ts//2, 1), (1, ts//2), (ts//2, ts//2)]:
                        sc2 = (105, 90, 68) if (ox + oy) % 2 == 0 else (88, 76, 56)
                        pygame.draw.rect(surface, sc2, (px+ox, py+oy, stone_sz, stone_sz), border_radius=1)
                        pygame.draw.rect(surface, (70, 60, 44), (px+ox, py+oy, stone_sz, stone_sz), 1, border_radius=1)

                elif tile == TT_TREE:
                    pygame.draw.rect(surface, (28, 48, 22), (px, py, ts, ts))

                elif tile == TT_WATER:
                    shimmer = abs(((self.walk_anim_t + tx * 200) % 1500) - 750) / 750.0
                    wc2 = (35 + int(12 * shimmer), 55 + int(10 * shimmer), 125 + int(20 * shimmer))
                    pygame.draw.rect(surface, wc2, (px, py, ts, ts))
                    ry2 = py + ts // 3
                    rx2 = int(px + ts * 0.15 + shimmer * ts * 0.3)
                    pygame.draw.line(surface, (55, 80, 160), (rx2, ry2), (rx2 + ts//2, ry2), 1)

                elif tile == TT_BRIDGE:
                    pygame.draw.rect(surface, (100, 78, 50), (px, py, ts, ts))
                    for pi in range(3):
                        ply2 = py + pi * (ts//3) + ts//8
                        pygame.draw.rect(surface, (125, 98, 62), (px+2, ply2, ts-4, max(2, ts//4)))

                elif tile == TT_EXIT:
                    pygame.draw.rect(surface, (60, 110, 55), (px, py, ts, ts))
                    pulse = abs((self.walk_anim_t % 2000) - 1000) / 1000.0
                    s2 = pygame.Surface((ts, ts), pygame.SRCALPHA)
                    s2.fill((100, 220, 90, int(20 + 30 * pulse)))
                    surface.blit(s2, (px, py))

                elif tile == TT_SIGN:
                    pygame.draw.rect(surface, (90, 78, 55), (px, py, ts, ts))
                    pygame.draw.rect(surface, (80, 64, 40), (px + ts//2 - 1, py + ts//3, 2, ts*2//3))
                    pygame.draw.rect(surface, (140, 112, 68),
                        (px + ts//5, py + ts//6, ts*3//5, ts//3), border_radius=2)
                    pygame.draw.rect(surface, (100, 80, 46),
                        (px + ts//5, py + ts//6, ts*3//5, ts//3), 1, border_radius=2)

                elif tile == TT_WALL:
                    # ── Top-down building view ─────────────────────────────
                    bld = bld_col_map.get((tx, ty))
                    bc = bld["color"] if bld else (130, 110, 85)
                    r0_b, r1_b = bld.get("wall_rows", (ty, ty)) if bld else (ty, ty)
                    c0_b, c1_b = bld.get("wall_cols", (tx, tx)) if bld else (tx, tx)
                    btype      = bld.get("type", "") if bld else ""

                    is_top_row    = (ty == r0_b)
                    is_bottom_row = (ty == r1_b)
                    is_left_col   = (tx == c0_b)
                    is_right_col  = (tx == c1_b)
                    is_edge = is_top_row or is_bottom_row or is_left_col or is_right_col

                    # Outer wall colour — darker, stony
                    WALL_DARK = max(12, ts // 8)
                    wall_c  = tuple(max(0, int(c * 0.55)) for c in bc)
                    roof_c  = tuple(min(255, int(c * 0.90)) for c in bc)
                    inner_c = tuple(min(255, int(c * 1.00)) for c in bc)

                    if is_edge:
                        # Stone outer wall from above
                        pygame.draw.rect(surface, wall_c, (px, py, ts, ts))
                        # Mortar lines on wall face
                        mortar = tuple(max(0, c-20) for c in wall_c)
                        bw = max(2, ts // 6)
                        if is_top_row:
                            pygame.draw.rect(surface, mortar, (px, py+ts-bw, ts, bw))
                        if is_bottom_row:
                            # South wall gets a drop shadow — gives illusion of wall height
                            pygame.draw.rect(surface, (0, 0, 0), (px, py+ts-max(2,ts//5), ts, max(2,ts//5)))
                        if is_left_col:
                            pygame.draw.rect(surface, mortar, (px+ts-bw, py, bw, ts))
                        if is_right_col:
                            pygame.draw.rect(surface, (0, 0, 0), (px+ts-max(2,ts//5), py, max(2,ts//5), ts))
                        # Brick / stone texture on edge walls
                        brick_c = tuple(min(255, c+18) for c in wall_c)
                        step = max(4, ts // 3)
                        offset = (ty % 2) * (step // 2)
                        for bx2 in range(px + offset % step, px + ts, step):
                            for by2 in range(py, py + ts, step // 2):
                                bw2 = min(step - 2, px + ts - bx2 - 1)
                                bh2 = min(step // 2 - 1, py + ts - by2 - 1)
                                if bw2 > 1 and bh2 > 1:
                                    pygame.draw.rect(surface, brick_c, (bx2+1, by2+1, bw2, bh2))
                    else:
                        # Interior roof tile
                        pygame.draw.rect(surface, inner_c, (px, py, ts, ts))
                        # Roof texture: subtle shingle/beam pattern
                        tile_idx = (tx - c0_b) + (ty - r0_b) * 100
                        if btype in ("guild", "temple", "castle"):
                            # Stone tile roof
                            tc = tuple(max(0, c-15) for c in inner_c)
                            if (tx + ty) % 2 == 0:
                                pygame.draw.rect(surface, tc, (px, py, ts//2, ts//2))
                                pygame.draw.rect(surface, tc, (px+ts//2, py+ts//2, ts//2, ts//2))
                        else:
                            # Wooden beam roof — horizontal lines
                            beam_c = tuple(max(0, c-22) for c in inner_c)
                            for bl in range(0, ts, max(3, ts//4)):
                                pygame.draw.line(surface, beam_c, (px, py+bl), (px+ts, py+bl), 1)
                        # Chimney on inn/forge top-left interior
                        if btype in ("forge", "inn") and (tx - c0_b == 1) and (ty - r0_b == 1):
                            chim_c = (80, 70, 65)
                            cw = max(4, ts//3)
                            pygame.draw.rect(surface, chim_c,
                                (px + ts//2 - cw//2, py + ts//2 - cw//2, cw, cw))
                            pygame.draw.rect(surface, (50, 45, 40),
                                (px + ts//2 - cw//2, py + ts//2 - cw//2, cw, cw), 1)
                        # Forge: glowing embers through roof gap
                        if btype == "forge" and (tx - c0_b == 2) and (ty - r0_b == 1):
                            glow_a = int(80 + 60 * abs(((self.walk_anim_t % 1200) - 600) / 600))
                            gs = pygame.Surface((ts-4, ts-4), pygame.SRCALPHA)
                            gs.fill((220, 100, 20, glow_a))
                            surface.blit(gs, (px+2, py+2))

                elif tile == TT_DOOR:
                    # ── Top-down doorway ───────────────────────────────────
                    bld2 = get_building_at(td, tx, ty)
                    bc2    = bld2[1]["color"] if bld2 else (140, 110, 60)
                    wall_c2 = tuple(max(0, int(c * 0.55)) for c in bc2)
                    floor_c = (112, 96, 72)   # worn stone threshold

                    # Full wall tile background (matches adjacent walls)
                    pygame.draw.rect(surface, wall_c2, (px, py, ts, ts))

                    # Door opening — centred gap, full height, lighter than wall
                    gap = max(3, ts // 4)
                    pygame.draw.rect(surface, floor_c, (px + gap, py, ts - gap*2, ts))

                    # Doorstep / threshold slab at the outer edge
                    step_c = tuple(min(255, int(c * 1.1)) for c in floor_c)
                    step_h = max(3, ts // 5)
                    # Determine which side is "outside" (the tile below the door is usually outside)
                    outside_south = get_tile(td, tx, ty + 1) not in (TT_WALL,)
                    if outside_south:
                        pygame.draw.rect(surface, step_c,
                            (px + gap, py + ts - step_h, ts - gap*2, step_h))
                    else:
                        pygame.draw.rect(surface, step_c,
                            (px + gap, py, ts - gap*2, step_h))

                    # Door frame — bright edge strip on each side of the opening
                    frame_c = tuple(min(255, int(c * 1.2)) for c in wall_c2)
                    pygame.draw.line(surface, frame_c,
                        (px + gap, py), (px + gap, py + ts), 2)
                    pygame.draw.line(surface, frame_c,
                        (px + ts - gap, py), (px + ts - gap, py + ts), 2)

                    # Knocker / knob — small gold circle on the door edge
                    pygame.draw.circle(surface, (210, 175, 80),
                        (px + ts//2, py + ts*3//5), max(2, ts//9))
                    pygame.draw.circle(surface, (170, 135, 55),
                        (px + ts//2, py + ts*3//5), max(2, ts//9), 1)

                else:
                    # '.' open tiles adjacent to doors also show a path stub
                    adj_door2 = any(
                        get_tile(td, tx+_dx, ty+_dy) == TT_DOOR
                        for _dx, _dy in ((-1,0),(1,0),(0,-1),(0,1))
                    )
                    if adj_door2:
                        pygame.draw.rect(surface, (88, 75, 56), (px, py, ts, ts))
                        stone_sz = max(3, ts // 3 - 1)
                        for ox, oy in [(1, 1), (ts//2, 1), (1, ts//2), (ts//2, ts//2)]:
                            sc2 = (98, 84, 62) if (ox+oy)%2==0 else (80,68,50)
                            pygame.draw.rect(surface, sc2, (px+ox, py+oy, stone_sz, stone_sz), border_radius=1)
                    else:
                        pygame.draw.rect(surface, (40, 35, 28), (px, py, ts, ts))

                if tile not in (TT_WALL, TT_TREE):
                    ec = TILE_COLORS.get(tile, (40,40,40))
                    pygame.draw.rect(surface, tuple(max(0, ec[i]-12) for i in range(3)), (px, py, ts, ts), 1)

        # ══ ROOF RIDGE PASS ══
        # Draw a darker ridge strip along the top wall of each building to
        # visually signal "this is a roof viewed from above, not a flat surface"
        for bld in td["buildings"].values():
            c0, c1 = bld.get("wall_cols", (0, 0))
            r0 = bld.get("wall_rows", (0, 0))[0]
            bc_r = bld.get("color", (130, 110, 85))
            ridge_c = tuple(max(0, int(c * 0.42)) for c in bc_r)
            for wc in range(c0, c1 + 1):
                sx2 = wc - cam_x
                sy2 = r0 - cam_y
                if 0 <= sx2 * ts < SCREEN_W and 0 <= sy2 * ts < map_area_h:
                    px2 = sx2 * ts
                    py2 = sy2 * ts
                    # Ridge line at bottom of top wall tile (the eave)
                    ridge_h = max(3, ts // 5)
                    pygame.draw.rect(surface, ridge_c,
                        (px2, py2 + ts - ridge_h, ts, ridge_h))
                    # Bright highlight on the very top edge (roof peak catching light)
                    hi_c = tuple(min(255, int(c * 1.15)) for c in bc_r)
                    pygame.draw.line(surface, hi_c, (px2, py2), (px2 + ts, py2), 2)

        # ══ TREE CANOPY PASS ══
        for sy in range(map_area_h // ts + 2):
            for sx in range(SCREEN_W // ts + 2):
                tx = cam_x + sx
                ty = cam_y + sy
                if not (0 <= ty < th and 0 <= tx < tw):
                    continue
                tile = td["map"][ty][tx] if tx < len(td["map"][ty]) else TT_WALL
                if tile != TT_TREE:
                    continue
                px = sx * ts
                py = sy * ts
                pygame.draw.rect(surface, (62, 42, 24), (px + ts*3//8, py + ts//2, ts//4, ts//2))
                canopy_c  = (38 + (tx*5+ty*7)%18, 72 + (tx*3+ty*11)%20, 28)
                canopy_hi = tuple(min(255, c+22) for c in canopy_c)
                r_can = max(6, ts*5//8)
                pygame.draw.circle(surface, canopy_c,  (px+ts//2, py+ts*2//5), r_can)
                pygame.draw.circle(surface, canopy_hi, (px+ts//2, py+ts*2//5), r_can, 2)
                shd = pygame.Surface((ts, ts//3), pygame.SRCALPHA)
                shd.fill((0, 0, 0, 40))
                surface.blit(shd, (px, py + ts//2))

        # ══ NPC PASS ══
        for npc in td.get("npcs", []):
            hide_flag = npc.get("hide_if")
            if hide_flag:
                from core.story_flags import get_flag
                if get_flag(hide_flag):
                    continue
            nx, ny = npc["x"], npc["y"]
            # Don't render NPCs standing on door tiles — they're inside the building.
            # Displace them one tile south (toward open ground) for display.
            _npc_tile = get_tile(td, nx, ny)
            if _npc_tile == TT_DOOR:
                # Check if tile below is walkable
                _below = get_tile(td, nx, ny + 1)
                if _below in (TT_GRASS, TT_PATH):
                    ny = ny + 1
                else:
                    _above = get_tile(td, nx, ny - 1)
                    if _above in (TT_GRASS, TT_PATH):
                        ny = ny - 1
            # Also skip NPCs fully inside building walls (non-door wall tiles)
            elif _npc_tile == TT_WALL:
                continue
            npx2 = (nx - cam_x) * ts
            npy2 = (ny - cam_y) * ts
            if not (0 <= npx2 < SCREEN_W and -ts <= npy2 < map_area_h):
                continue

            nc2   = npc.get("color", (180, 180, 180))
            ntype = npc.get("npc_type", "default")
            light2= tuple(min(255, int(c*1.25)) for c in nc2)
            ncx   = npx2 + ts//2
            ncy   = npy2 + ts//2

            # Ultima-style pixel art figure
            from ui.town_sprites import draw_npc_figure
            draw_npc_figure(surface, ncx, ncy, ts, ntype, nc2)

            if npc.get("service"):
                badge_txt = {"inn":"INN","shop":"SHOP","forge":"FORGE",
                             "temple":"SHRINE","tavern":"TAVERN"}.get(npc["service"],"")
                if badge_txt:
                    iw2 = get_font(8).size(badge_txt)[0]
                    bdg = pygame.Rect(ncx - iw2//2 - 3, npy2 - 14, iw2+6, 10)
                    pygame.draw.rect(surface, (20, 16, 10), bdg, border_radius=2)
                    pygame.draw.rect(surface, nc2, bdg, 1, border_radius=2)
                    draw_text(surface, badge_txt, ncx - iw2//2, npy2 - 13, nc2, 8)

            dist2 = abs(nx - self.walk_x) + abs(ny - self.walk_y)
            if dist2 <= 3:
                nw2 = get_font(10).size(npc["name"])[0]
                draw_text(surface, npc["name"], ncx - nw2//2, npy2 - 24, light2, 10)

        # ══ PLAYER PASS ══
        ppx = (self.walk_x - cam_x) * ts
        ppy = (self.walk_y - cam_y) * ts
        pcx, pcy = ppx + ts//2, ppy + ts//2

        # Ultima-style pixel art party figure
        from ui.town_sprites import draw_party_figure
        draw_party_figure(surface, pcx, pcy, ts, self.walk_facing)

        # Building name labels — centered above the building's top wall
        for bld_id, bld in td["buildings"].items():
            c0, c1 = bld.get("wall_cols", (0, 0))
            r0, _r1 = bld.get("wall_rows", (0, 0))
            # Label centre X = midpoint of building width; Y = just above top wall
            label_cx = (c0 + c1) / 2.0
            label_ty = r0  # top wall row
            lpx3 = int((label_cx - cam_x) * ts)
            lpy3 = int((label_ty - cam_y) * ts) - 2  # just above top wall tile
            if 0 <= lpx3 < SCREEN_W and 4 <= lpy3 < map_area_h:
                bname2 = bld["name"]
                bfont  = get_font(11)
                bw2    = bfont.size(bname2)[0]
                bh2    = 15
                pad    = 5
                # Dark semi-transparent backing with building-colour border
                lbg2 = pygame.Surface((bw2 + pad*2, bh2), pygame.SRCALPHA)
                lbg2.fill((8, 6, 4, 200))
                surface.blit(lbg2, (lpx3 - bw2//2 - pad, lpy3 - 1))
                pygame.draw.rect(surface, bld["color"],
                    (lpx3 - bw2//2 - pad, lpy3 - 1, bw2 + pad*2, bh2),
                    1, border_radius=3)
                draw_text(surface, bname2, lpx3 - bw2//2, lpy3 + 1,
                    (245, 235, 215), 11, bold=True)


        # ── UI bar at bottom ──
        bar_y = map_area_h
        pygame.draw.rect(surface, (12, 10, 25), (0, bar_y, SCREEN_W, SCREEN_H - bar_y))
        pygame.draw.line(surface, PANEL_BORDER, (0, bar_y), (SCREEN_W, bar_y))

        # Town name + gold (left side)
        draw_text(surface, td["name"], 14, bar_y + 6, GOLD, 16, bold=True)
        total_gold = sum(c.gold for c in self.party)
        draw_text(surface, f"✦ {total_gold}g", 14, bar_y + 26, DIM_GOLD, 14)

        # Interaction prompt (center)
        prompt = self._get_walk_prompt()
        if prompt:
            pw = get_font(14).size(prompt)[0]
            draw_text(surface, prompt, SCREEN_W // 2 - pw // 2, bar_y + 8, HIGHLIGHT, 14)

        # Interact message (center, below prompt)
        if self.walk_interact_msg and self.walk_interact_timer > 0:
            mw = get_font(12).size(self.walk_interact_msg)[0]
            alpha_ratio = min(1.0, self.walk_interact_timer / 500.0)
            msg_col = tuple(int(c * alpha_ratio) for c in self.msg_color)
            draw_text(surface, self.walk_interact_msg,
                      SCREEN_W // 2 - min(mw // 2, 280), bar_y + 30, msg_col, 12)

        # Controls hint (bottom left)
        draw_text(surface, "WASD: Move   ENTER: Interact   ESC: Leave",
                  14, bar_y + 90, DARK_GREY, 10)

        # ── Minimap (center-right) ──
        mm_size = 90
        mm_x = SCREEN_W // 2 + 80
        mm_y = bar_y + 8
        mm_tw, mm_th = td["width"], td["height"]
        mm_tile_w = mm_size / mm_tw
        mm_tile_h = mm_size / mm_th
        # Background
        pygame.draw.rect(surface, (8, 6, 18), (mm_x, mm_y, mm_size, mm_size))
        pygame.draw.rect(surface, PANEL_BORDER, (mm_x, mm_y, mm_size, mm_size), 1)
        # Draw simplified tiles
        from data.town_maps import TT_GRASS, TT_WALL, TT_PATH, TT_WATER, TT_TREE, TT_EXIT
        mm_colors = {
            TT_GRASS: (35, 55, 28), TT_PATH: (80, 68, 48),
            TT_WALL: (65, 52, 40), TT_WATER: (25, 45, 90),
            TT_TREE: (20, 45, 18), TT_EXIT: (50, 110, 50),
        }
        for my_row in range(mm_th):
            for mx_col in range(mm_tw):
                tile = td["map"][my_row][mx_col] if mx_col < len(td["map"][my_row]) else TT_WALL
                col = mm_colors.get(tile, (50, 40, 30))
                rx = int(mm_x + mx_col * mm_tile_w)
                ry = int(mm_y + my_row * mm_tile_h)
                rw = max(1, int(mm_tile_w))
                rh = max(1, int(mm_tile_h))
                pygame.draw.rect(surface, col, (rx, ry, rw, rh))
        # Player dot on minimap
        pm_px = int(mm_x + self.walk_x * mm_tile_w)
        pm_py = int(mm_y + self.walk_y * mm_tile_h)
        pygame.draw.circle(surface, (255, 240, 60), (pm_px, pm_py), max(2, int(mm_tile_w)))
        # NPCs as tiny dots
        for npc in td.get("npcs", []):
            nx_mm = int(mm_x + npc["x"] * mm_tile_w)
            ny_mm = int(mm_y + npc["y"] * mm_tile_h)
            nc = npc.get("color", (180, 180, 180))
            pygame.draw.circle(surface, nc, (nx_mm, ny_mm), max(1, int(mm_tile_w * 0.6)))

        # ── Compact party status (right side) ──
        from core.classes import get_all_resources
        px_start = SCREEN_W - 290
        for i, c in enumerate(self.party):
            cls = CLASSES[c.class_name]
            cx = px_start + i * 72
            # Name
            draw_text(surface, c.name[:5], cx, bar_y + 6, cls["color"], 12, bold=True)
            # HP
            hp = c.resources.get("HP", 0)
            max_resources = get_all_resources(c.class_name, c.stats, c.level)
            max_hp = max_resources.get("HP", 1)
            hp_ratio = hp / max_hp if max_hp > 0 else 0
            hp_color = DIM_GREEN if hp_ratio > 0.5 else (220, 180, 40) if hp_ratio > 0.25 else (220, 70, 70)
            # HP bar
            bar_w = 60
            bar_h = 6
            pygame.draw.rect(surface, (30, 20, 20), (cx, bar_y + 20, bar_w, bar_h))
            pygame.draw.rect(surface, hp_color, (cx, bar_y + 20, int(bar_w * hp_ratio), bar_h))
            draw_text(surface, f"HP {hp}/{max_hp}", cx, bar_y + 29, hp_color, 11)
            # MP (if class has it)
            mp = c.resources.get("MP", -1)
            if mp >= 0:
                max_mp = max_resources.get("MP", 1)
                mp_ratio = mp / max_mp if max_mp > 0 else 0
                pygame.draw.rect(surface, (20, 20, 35), (cx, bar_y + 40, bar_w, 5))
                pygame.draw.rect(surface, (80, 120, 220), (cx, bar_y + 40, int(bar_w * mp_ratio), 5))
            # Dead indicator
            if hp <= 0:
                pygame.draw.line(surface, (200, 50, 50), (cx, bar_y + 6), (cx + 50, bar_y + 50), 2)

    def _get_walk_prompt(self):
        """Get context-sensitive prompt based on what's at the player's position or adjacent."""
        from data.town_maps import get_building_at, get_npc_at, get_sign_at, is_exit, get_tile, TT_DOOR
        td = self.town_data
        x, y = self.walk_x, self.walk_y

        # Check what's at player position
        tile = get_tile(td, x, y)
        if tile == TT_DOOR:
            result = get_building_at(td, x, y)
            if result:
                _, bld = result
                return f"[ENTER] Enter {bld['name']}"

        if is_exit(td, x, y):
            return "[ENTER] Leave Town"

        # Check facing tile for NPCs and signs
        dx_map = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
        fdx, fdy = dx_map.get(self.walk_facing, (0, 1))
        fx, fy = x + fdx, y + fdy

        npc = get_npc_at(td, fx, fy)
        if npc:
            service = npc.get("service", "")
            service_hint = f" ({service.title()})" if service else ""
            return f"[ENTER] Talk to {npc['name']}{service_hint}"

        sign_text = get_sign_at(td, fx, fy)
        if sign_text:
            return "[ENTER] Read Sign"

        return ""

    def handle_key(self, key):
        """Handle keyboard input. Returns 'exit' to leave town, or None."""
        # Dialogue takes priority in ALL views — must check before the walk guard
        # so SPACE/RETURN advances NPC dialogue even inside buildings.
        if self.active_dialogue and not self.active_dialogue.finished:
            import pygame as _pg
            event = _pg.event.Event(_pg.KEYDOWN, key=key, mod=0, unicode="")
            self.active_dialogue.handle_event(event)
            if self.active_dialogue.finished:
                self.active_dialogue = None
                try:
                    from core.story_flags import auto_advance_quests
                    done = auto_advance_quests(self.party)
                    self.pending_quest_completions.extend(done)
                except Exception:
                    pass
            return None

        if self.view != self.VIEW_WALK:
            return None

        from data.town_maps import is_walkable, get_building_at, get_npc_at, get_sign_at, is_exit, get_tile, TT_DOOR

        td = self.town_data
        dx, dy = 0, 0

        # Movement
        if key in (pygame.K_w, pygame.K_UP):
            dy = -1; self.walk_facing = "up"
        elif key in (pygame.K_s, pygame.K_DOWN):
            dy = 1; self.walk_facing = "down"
        elif key in (pygame.K_a, pygame.K_LEFT):
            dx = -1; self.walk_facing = "left"
        elif key in (pygame.K_d, pygame.K_RIGHT):
            dx = 1; self.walk_facing = "right"
        elif key in (pygame.K_RETURN, pygame.K_SPACE):
            return self._walk_interact()
        elif key == pygame.K_ESCAPE:
            self.finished = True
            return "exit"

        if dx != 0 or dy != 0:
            nx, ny = self.walk_x + dx, self.walk_y + dy
            npc_ahead = get_npc_at(td, nx, ny)
            is_service_npc = npc_ahead is not None and npc_ahead.get("service") is not None

            # All NPCs block movement; interact with ENTER when facing them
            npc_blocking = npc_ahead is not None
            if is_walkable(td, nx, ny) and not npc_blocking:
                self.walk_x = nx
                self.walk_y = ny
                sfx.play("step")
                # Auto-enter when stepping onto a door tile
                if get_tile(td, nx, ny) == TT_DOOR:
                    return self._walk_interact()

        return None

    def _walk_interact(self):
        """Handle ENTER press while walking. Returns 'exit' or None."""
        from data.town_maps import (
            get_building_at, get_npc_at, get_sign_at, is_exit,
            get_tile, TT_DOOR, BLD_INN, BLD_SHOP, BLD_TEMPLE,
            BLD_TAVERN, BLD_FORGE, BLD_HOUSE, BLD_JOBBOARD, BLD_GUILD,
        )

        td = self.town_data
        x, y = self.walk_x, self.walk_y

        # Check current tile for door
        tile = get_tile(td, x, y)
        if tile == TT_DOOR:
            result = get_building_at(td, x, y)
            if result:
                bld_id, bld = result
                btype = bld["type"]
                sfx.play("door_open")

                # Store indoor NPC and building name for service views
                self.current_bld_indoor_npc = bld.get("indoor_npc")
                self.current_bld_name       = bld.get("name", "building")

                if btype == BLD_INN:
                    self.view = self.VIEW_INN
                elif btype == BLD_SHOP:
                    self.view = self.VIEW_SHOP
                elif btype == BLD_TEMPLE:
                    self.view = self.VIEW_TEMPLE
                elif btype == BLD_TAVERN:
                    from data.story_data import get_rumor
                    self.current_rumor = get_rumor()
                    self._tavern_recruits = None   # force refresh on entry
                    self.view = self.VIEW_TAVERN
                elif btype == BLD_FORGE:
                    self.view = self.VIEW_FORGE
                    self.forge_scroll = 0
                elif btype == BLD_GUILD:
                    self._enter_guild(bld)
                elif btype == BLD_HOUSE:
                    self._show_walk_msg(f"The door to {bld['name']} is locked.", GREY)
                elif btype == BLD_JOBBOARD:
                    self._show_walk_msg("Checking the job board...", DIM_GOLD)
                    self.view = self.VIEW_JOBBOARD
                return None

        # Check exit tile
        if is_exit(td, x, y):
            self.finished = True
            return "exit"

        # Check facing tile for NPC
        dx_map = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
        fdx, fdy = dx_map.get(self.walk_facing, (0, 1))
        fx, fy = x + fdx, y + fdy

        npc = get_npc_at(td, fx, fy)
        if npc:
            sfx.play("npc_talk")

            # Service NPC — gives a greeting but does NOT open menu.
            # Enter the building door to access services.
            service = npc.get("service")
            greetings = {
                "inn":    lambda n: f"{n}: \"Rooms available inside — go on in!\"",
                "shop":   lambda n: f"{n}: \"Come inside, I'll get you a good price.\"",
                "temple": lambda n: f"{n}: \"The shrine is open. Enter freely.\"",
                "tavern": lambda n: f"{n}: \"Step inside — it's warmer in there!\"",
                "forge":  lambda n: f"{n}: \"Workshop's through the door if you need work done.\"",
            }
            if service and service in greetings:
                self._show_walk_msg(greetings[service](npc["name"]),
                                    npc.get("color", CREAM))
                return None

            # Regular dialogue NPC
            did = npc.get("dialogue_id")
            if did:
                from data.story_data import NPC_DIALOGUES
                from core.dialogue import select_dialogue
                from ui.dialogue_ui import DialogueUI
                from core._dialogue_party import set_party
                set_party(self.party)   # must be before select_dialogue (on_enter fires in __init__)
                dialogues = NPC_DIALOGUES.get(did, [])
                if dialogues:
                    ds = select_dialogue(did, dialogues)
                    if ds:
                        self.active_dialogue = DialogueUI(ds)
                        return None
            self._show_walk_msg(npc.get("description", f"{npc['name']} has nothing to say."),
                                npc.get("color", CREAM))
            return None

        # Check facing tile for sign
        sign_text = get_sign_at(td, fx, fy)
        if sign_text:
            if "Job Board" in sign_text:
                self._show_walk_msg("Checking the job board...", DIM_GOLD)
                self.view = self.VIEW_JOBBOARD
            else:
                # Show sign as a proper dialogue popup with a Close button
                from core.dialogue import DialogueState
                from ui.dialogue_ui import DialogueUI
                sign_tree = {
                    "id": "sign",
                    "nodes": {
                        "start": {
                            "speaker": "",
                            "text": sign_text,
                            "choices": [{"text": "[ Close ]", "next": None}],
                        }
                    },
                }
                self.active_dialogue = DialogueUI(DialogueState(sign_tree))
            return None

        return None

    def _show_walk_msg(self, text, color=CREAM):
        """Show a temporary message in the walk UI."""
        self.walk_interact_msg = text
        self.walk_interact_timer = 3000
        self.msg_color = color

    def _draw_bld_npc_header(self, surface, bld_name, subtitle="", mx=0, my=0,
                              building_type: str = ""):
        """Draw building title + indoor NPC portrait card at top of service views.
        Also draws the split-screen building interior background if an image exists.
        Draws the Back button at top-right of the left panel and stores it as
        self._back_btn for click handlers.
        """
        PW = int(SCREEN_W * 0.42)   # left panel width

        # ── Building interior background (split screen) ──────────────
        self._draw_building_interior(surface, building_type or
                                     getattr(self, "_current_bld_type", ""))

        # ── Back button — bottom of left panel, above party bar ──────────────
        # Party bar starts at SCREEN_H-100; button ends at SCREEN_H-106 (6px gap)
        back = pygame.Rect(8, SCREEN_H - 140, 120, 34)
        draw_button(surface, back, "← Back",
                    hover=back.collidepoint(mx, my), size=13,
                    bg=(50, 35, 70), border=(120, 90, 160), color=(220, 200, 255))
        self._back_btn = back

        # ── Title text — full left panel width right of NPC card ──────────────
        draw_text(surface, bld_name, 278, 14, GOLD, 22, bold=True,
                  max_width=PW - 290)
        if subtitle:
            draw_text(surface, subtitle, 278, 42, GREY, 13,
                      max_width=PW - 290)

        npc = self.current_bld_indoor_npc
        self._bld_npc_portrait_rect = None
        if not npc:
            return

        _npc_class = {
            "innkeeper": "Cleric",      "merchant":    "Thief",
            "barkeep":   "Fighter",     "priestess":   "High Priest",
            "priest":    "High Priest", "forger":      "Champion",
            "guildmaster": "Archmage",  "ranger":      "Ranger",
            "elder":     "Mage",        "guard":       "Fighter",
            "warden":    "Warden",      "mage":        "Mage",
            "youth":     "Thief",
        }
        cls = _npc_class.get(npc.get("npc_type", ""), "Fighter")
        col = npc.get("color", CREAM)
        did = npc.get("dialogue_id")

        # Portrait card — LEFT side, larger for AI portraits
        PORTRAIT_W, PORTRAIT_H = 80, 110
        CARD_W, CARD_H = PORTRAIT_W + 180, PORTRAIT_H + 16
        pr = pygame.Rect(8, 8, CARD_W, CARD_H)
        self._bld_npc_portrait_rect = pr if did else None
        hover = did and pr.collidepoint(mx, my)
        bg_col = (38, 28, 50) if hover else (22, 16, 32)
        border_col = col if hover else PANEL_BORDER
        pygame.draw.rect(surface, bg_col, pr, border_radius=6)
        pygame.draw.rect(surface, border_col, pr, 1, border_radius=6)

        # Portrait image — try NPC-specific PNG first, then class silhouette fallback
        sil_r = pygame.Rect(pr.x + 6, pr.y + 6, PORTRAIT_W, PORTRAIT_H)
        npc_name = npc.get("name", "")
        from ui.sprite_loader import draw_npc_portrait
        if not draw_npc_portrait(surface, sil_r, npc_name, hover=bool(hover)):
            from ui.pixel_art import draw_character_silhouette
            draw_character_silhouette(surface, sil_r, cls, highlight=bool(hover))

        # Thin colour accent bar on left edge of portrait
        pygame.draw.rect(surface, col,
                         pygame.Rect(pr.x, pr.y + 8, 3, PORTRAIT_H), border_radius=2)

        # Text — right of portrait
        tx = pr.x + PORTRAIT_W + 14
        draw_text(surface, npc_name,              tx, pr.y + 10, CREAM,   13, bold=True)
        draw_text(surface, npc.get("title", ""),  tx, pr.y + 28, GREY,    11)
        desc = npc.get("description", "")
        if desc:
            draw_text(surface, desc, tx, pr.y + 46, (140, 130, 150), 10,
                      max_width=CARD_W - PORTRAIT_W - 24)
        if did:
            talk_lbl = "[ Talk → ]" if hover else "[ Talk ]"
            draw_text(surface, talk_lbl, tx, pr.y + CARD_H - 28,
                      col if hover else DIM_GOLD, 11)
        else:
            draw_text(surface, "\"Hello, travellers.\"", tx, pr.y + CARD_H - 28,
                      DIM_GOLD, 10)


    def _open_indoor_npc_dialogue(self):
        """Open dialogue for the current building's indoor NPC (if they have one)."""
        npc = self.current_bld_indoor_npc
        if not npc:
            return
        did = npc.get("dialogue_id")
        if not did:
            self._show_walk_msg(npc.get("description", f"{npc['name']} has nothing to say."), npc.get("color", CREAM))
            return
        from data.story_data import NPC_DIALOGUES
        from core.dialogue import select_dialogue
        from ui.dialogue_ui import DialogueUI
        from core._dialogue_party import set_party
        set_party(self.party)   # must be before select_dialogue (on_enter fires in __init__)
        dialogues = NPC_DIALOGUES.get(did, [])
        if dialogues:
            ds = select_dialogue(did, dialogues)
            if ds:
                self.active_dialogue = DialogueUI(ds)
                return
        self._show_walk_msg(npc.get("description", f"{npc['name']} has nothing to say."), npc.get("color", CREAM))

    def _enter_guild(self, bld):
        """Enter a guild building.
        - If any party member has a pending ability branch choice, route directly to training.
        - Otherwise show the guild hub menu.
        """
        bld_name = bld.get("name", "Guild")
        self._show_walk_msg(f"Entered {bld_name}.", CREAM)
        self._guild_building_name = bld_name
        self._guild_hover = -1

        self.view = self.VIEW_GUILD

    def _draw_guild(self, surface, mx, my):
        """Draw the Guild hub menu."""
        surface.fill(TOWN_BG)
        self._bld_npc_portrait_rect = None   # no portrait card in guild view

        W, H = SCREEN_W, SCREEN_H
        name = getattr(self, "_guild_building_name", "Adventurers' Guild")

        # ── Header ──────────────────────────────────────────────────
        header = pygame.Rect(0, 0, W, 72)
        pygame.draw.rect(surface, (18, 14, 32), header)
        pygame.draw.line(surface, (60, 50, 90), (0, 72), (W, 72), 1)
        draw_text(surface, name.upper(), 28, 18, GOLD, 26, bold=True)
        draw_text(surface, "\"We take the jobs no one else will touch.\"",
                  28, 50, (100, 90, 130), 13)

        # ── Warden Rank Panel (below option cards) ──────────────────
        try:
            from core.progression import PLANAR_TIERS
            from core.story_flags import get_flag
            tier_num  = max((getattr(c, "planar_tier", 0) for c in self.party), default=0)
            tier_data = PLANAR_TIERS.get(tier_num, {})
            rank_name = tier_data.get("name", "Initiate")
            rank_col  = tier_data.get("color", (140, 130, 160))
            rank_sym  = tier_data.get("symbol", "◆")
            bonus     = tier_data.get("bonus", {})

            # Bonus summary
            bonus_parts = []
            if bonus.get("all_stats"):
                bonus_parts.append(f"+{bonus['all_stats']} all stats")
            if bonus.get("max_hp_pct"):
                bonus_parts.append(f"+{int(bonus['max_hp_pct']*100)}% HP")
            if bonus.get("damage_mult") and bonus["damage_mult"] > 1:
                bonus_parts.append(f"+{int((bonus['damage_mult']-1)*100)}% damage")
            if bonus.get("xp_mult") and bonus["xp_mult"] > 1:
                bonus_parts.append(f"+{int((bonus['xp_mult']-1)*100)}% XP")
            bonus_str = ", ".join(bonus_parts) if bonus_parts else "No bonuses yet."

            # Next tier progress
            next_tier_data = PLANAR_TIERS.get(tier_num + 1) if tier_num < 4 else None
            flag_labels = {
                "item.hearthstone.1": "1st Hearthstone (Abandoned Mine)",
                "item.hearthstone.3": "3rd Hearthstone (Dragon's Tooth)",
                "item.hearthstone.5": "5th Hearthstone (Windswept Isle)",
                "boss_defeated.shadow_valdris": "Defeat Valdris the Broken",
            }
            if next_tier_data:
                next_name  = next_tier_data.get("name", "")
                next_flag  = next_tier_data.get("unlock_flag", "")
                next_level = next_tier_data.get("min_level", 1)
                next_col   = next_tier_data.get("color", (140, 130, 160))
                flag_label = flag_labels.get(next_flag, next_flag.replace("_", " ").title())
                min_level  = min((c.level for c in self.party), default=1)
                flag_met   = bool(get_flag(next_flag)) if next_flag else False
                level_met  = min_level >= next_level
                reqs = []
                if not flag_met:
                    reqs.append(flag_label)
                if not level_met:
                    reqs.append(f"Party min level {next_level} (currently {min_level})")
                next_req_str = "  |  ".join(reqs) if reqs else "Ready to advance!"
                next_ready   = not reqs
            else:
                next_name    = ""
                next_col     = rank_col
                next_req_str = "Highest rank achieved."
                next_ready   = False

            # Draw panel — taller for richer display
            PANEL_Y = 110 + 3 * (88 + 16) + 10
            panel_r = pygame.Rect(40, PANEL_Y, W - 80, 110)
            pygame.draw.rect(surface, (22, 16, 36), panel_r, border_radius=6)
            pygame.draw.rect(surface, rank_col, panel_r, 1, border_radius=6)

            # ── Left: current rank ──────────────────────────────────
            draw_text(surface, "WARDEN RANK", panel_r.x + 20, panel_r.y + 10,
                      (90, 80, 110), 10, bold=True)
            draw_text(surface, f"{rank_sym}  {rank_name}",
                      panel_r.x + 20, panel_r.y + 26, rank_col, 22, bold=True)
            # Tier description
            tier_desc = tier_data.get("description", "")
            if tier_desc:
                draw_text(surface, tier_desc, panel_r.x + 20, panel_r.y + 56,
                          (130, 120, 150), 11, max_width=290)
            draw_text(surface, bonus_str, panel_r.x + 20, panel_r.y + 90,
                      (160, 145, 180), 11)

            # Hearthstone count pips
            hs_count = sum(
                1 for i in range(1, 6) if get_flag(f"item.hearthstone.{i}")
            )
            for hi in range(5):
                hx = panel_r.x + 20 + hi * 18
                hy = panel_r.y + 76
                col_hs = (220, 180, 60) if hi < hs_count else (60, 50, 80)
                pygame.draw.circle(surface, col_hs, (hx, hy), 6)
                pygame.draw.circle(surface, (90, 80, 110), (hx, hy), 6, 1)
            draw_text(surface, f"Hearthstones: {hs_count}/5",
                      panel_r.x + 116, panel_r.y + 70, (140, 130, 160), 10)

            # Vertical divider
            div_x = panel_r.x + 340
            pygame.draw.line(surface, (60, 50, 80),
                             (div_x, panel_r.y + 12), (div_x, panel_r.bottom - 12), 1)

            # ── Right: next rank ────────────────────────────────────
            if next_tier_data:
                draw_text(surface, "NEXT RANK", div_x + 20, panel_r.y + 10,
                          (90, 80, 110), 10, bold=True)
                draw_text(surface, f"◆  {next_name}",
                          div_x + 20, panel_r.y + 26,
                          next_col if next_ready else (100, 90, 120), 18, bold=True)

                # Requirements list
                req_y = panel_r.y + 54
                if next_ready:
                    draw_text(surface, "✓ Ready to advance!", div_x + 20, req_y,
                              (80, 200, 120), 12)
                else:
                    if not flag_met:
                        draw_text(surface, f"✗ {flag_label}",
                                  div_x + 20, req_y, (200, 120, 60), 11,
                                  max_width=W - div_x - 60)
                        req_y += 18
                    if not level_met:
                        # Party level progress bar
                        bar_w = min(200, W - div_x - 80)
                        pct = min(1.0, min_level / next_level)
                        pygame.draw.rect(surface, (40, 30, 60),
                                         (div_x + 20, req_y + 14, bar_w, 8),
                                         border_radius=4)
                        pygame.draw.rect(surface, next_col,
                                         (div_x + 20, req_y + 14, int(bar_w * pct), 8),
                                         border_radius=4)
                        draw_text(surface, f"Level {min_level} / {next_level} required",
                                  div_x + 20, req_y, (180, 150, 80), 11)
            else:
                draw_text(surface, "RANK COMPLETE", div_x + 20, panel_r.y + 10,
                          (90, 80, 110), 10, bold=True)
                draw_text(surface, "Warden-Commander", div_x + 20, panel_r.y + 26,
                          rank_col, 18, bold=True)
                draw_text(surface, "Highest rank of the mortal order.",
                          div_x + 20, panel_r.y + 54, (140, 200, 160), 12)
        except Exception:
            pass

        # ── Advance Rank button (shown when requirements met) ──────
        self._guild_advance_btn = None
        try:
            if next_tier_data and next_ready:
                adv_r = pygame.Rect(W - 280, 18, 128, 36)
                pygame.draw.rect(surface, (24, 18, 44), adv_r, border_radius=6)
                pygame.draw.rect(surface, next_col, adv_r, 2, border_radius=6)
                draw_text(surface, "▲ Advance Rank",
                          adv_r.x + 10, adv_r.y + 10, next_col, 13, bold=True)
                self._guild_advance_btn = adv_r
        except Exception:
            pass

        # Back button — top-right of header bar, stays within header height
        back = pygame.Rect(W - 150, 18, 120, 36)
        draw_button(surface, back, "← Leave", hover=back.collidepoint(mx, my),
                    size=13, bg=(50,35,70), border=(120,90,160), color=(220,200,255))
        self._guild_back_btn = back

        # ── Pending badge ───────────────────────────────────────────
        pending_chars = []  # branching removed

        # ── Menu options ────────────────────────────────────────────
        # Build next-unlock summary for each party member
        from core.abilities import CLASS_ABILITIES
        next_unlock_parts = []
        for _c in self.party:
            all_abs = CLASS_ABILITIES.get(_c.class_name, [])
            known_names = {a["name"] for a in _c.abilities}
            # Find the first ability not yet known that's within 3 levels
            upcoming = [a for a in all_abs
                        if a["name"] not in known_names and a.get("level", 1) > _c.level]
            upcoming.sort(key=lambda a: a.get("level", 99))
            if upcoming:
                nxt = upcoming[0]
                gap = nxt.get("level", 1) - _c.level
                gap_str = f"L{nxt.get('level',1)}" if gap > 1 else "next level"
                next_unlock_parts.append(f"{_c.name}: {nxt['name']} ({gap_str})")
        next_unlock_str = "  |  ".join(next_unlock_parts[:3]) if next_unlock_parts                           else "All known abilities trained."

        from core.progression import get_available_transitions
        chars_ready = [c for c in self.party if get_available_transitions(c)]

        options = [
            {
                "label":   "Take a Job",
                "sub":     "Browse bounties, fetch quests, and exploration contracts",
                "accent":  (80, 200, 120),
                "action":  "jobboard",
            },
            {
                "label":   "Train Abilities" + (" ⚡" if pending_chars else ""),
                "sub":     (f"{', '.join(c.name for c in pending_chars)} "
                            f"{'have' if len(pending_chars) > 1 else 'has'} a new path to choose!"
                            if pending_chars
                            else f"Next: {next_unlock_str}"),
                "accent":  (160, 120, 220) if pending_chars else (120, 100, 180),
                "action":  "train",
                "badge":   len(pending_chars),
            },
        ]
        # Insert "Choose Advanced Class" card when anyone qualifies
        if chars_ready:
            names_str = ", ".join(c.name for c in chars_ready[:3])
            options.append({
                "label":   "Choose Advanced Class  ✦",
                "sub":     (f"{names_str} {'are' if len(chars_ready)>1 else 'is'} ready "
                            f"to transcend {'their' if len(chars_ready)>1 else 'their'} "
                            f"base training. Choose a new path."),
                "accent":  (220, 160, 60),
                "action":  "class_choose",
                "badge":   len(chars_ready),
            })
        options.append(
            {
                "label":   "View Abilities",
                "sub":     "See your full class progression tree and what unlocks at each level",
                "accent":  (100, 160, 220),
                "action":  "classtree",
            }
        )

        CARD_W = W - 80
        CARD_H = 88
        START_Y = 110
        GAP = 16
        self._guild_option_rects = []

        for i, opt in enumerate(options):
            r = pygame.Rect(40, START_Y + i * (CARD_H + GAP), CARD_W, CARD_H)
            hover = (getattr(self, "_guild_hover", -1) == i) or r.collidepoint(mx, my)
            if r.collidepoint(mx, my):
                self._guild_hover = i

            accent = opt["accent"]
            bg = tuple(min(255, c + 12) for c in SHOP_BG) if hover else SHOP_BG
            bd = accent if hover else PANEL_BORDER
            pygame.draw.rect(surface, bg, r, border_radius=6)
            pygame.draw.rect(surface, bd, r, 2 if hover else 1, border_radius=6)

            # Accent strip on left
            strip = pygame.Rect(r.x, r.y + 8, 4, r.height - 16)
            pygame.draw.rect(surface, accent, strip, border_radius=2)

            # Label
            draw_text(surface, opt["label"], r.x + 24, r.y + 16,
                      accent if hover else CREAM, 20, bold=True)

            # Subtitle
            draw_text(surface, opt["sub"], r.x + 24, r.y + 50,
                      (160, 150, 170), 13, max_width=CARD_W - 100)

            # Badge for pending choices
            if opt.get("badge"):
                badge_r = pygame.Rect(r.right - 56, r.y + r.height // 2 - 14, 44, 28)
                pygame.draw.rect(surface, (120, 60, 200), badge_r, border_radius=14)
                draw_text(surface, str(opt["badge"]), badge_r.x + 14, badge_r.y + 6,
                          (255, 255, 255), 14, bold=True)

            self._guild_option_rects.append((r, opt["action"]))

        # ── Party bar ───────────────────────────────────────────────
        self._draw_party_bar(surface, mx, my)

    def _do_guild_advance(self):
        """Advance the party to the next Warden rank tier."""
        from core.progression import PLANAR_TIERS, apply_tier_stat_bonus
        from core.story_flags import get_flag
        import core.sound as sfx

        tier_num = max((getattr(c, "planar_tier", 0) for c in self.party), default=0)
        next_tier_num = tier_num + 1
        next_tier_data = PLANAR_TIERS.get(next_tier_num)
        if not next_tier_data:
            return

        # Final check: requirements still met
        flag    = next_tier_data.get("unlock_flag")
        min_lv  = next_tier_data.get("min_level", 1)
        flag_ok = (not flag) or bool(get_flag(flag))
        lv_ok   = min((c.level for c in self.party), default=1) >= min_lv
        if not (flag_ok and lv_ok):
            self._msg("Requirements not yet met.", (200, 80, 80))
            return

        # Apply the tier to every party member
        for c in self.party:
            old_tier = getattr(c, "planar_tier", 0)
            if old_tier < next_tier_num:
                apply_tier_stat_bonus(c, next_tier_num)
                c.planar_tier = next_tier_num

        sfx.play("quest_complete")
        rank_name = next_tier_data.get("name", "")
        self._msg(f"The party advances to {rank_name}! Warden bonuses applied.", (180, 220, 200))

    def _return_to_town(self):
        """Return to the hub menu. Walking map is disabled — hub is always the town view."""
        self.view = self.VIEW_HUB

    def _enter_building_from_hub(self, building_type: str):
        """Set indoor NPC and building name when entering via hub click."""
        town_blds = BUILDING_NPCS.get(self.town_id, {})
        npc_data  = town_blds.get(building_type)
        self.current_bld_indoor_npc = npc_data   # None if no NPC defined
        # Building name comes from _get_town_locations
        locs = self._get_town_locations()
        for key, name, desc, *_ in locs:
            if key == building_type:
                self.current_bld_name = name
                break

    # ─────────────────────────────────────────────────────────
    #  GENERAL STORE — Menu
    # ─────────────────────────────────────────────────────────

    def _draw_shop_menu(self, surface, mx, my):
        bld_name = self.current_bld_name or self.shop.get("name", "General Store")
        self._draw_bld_npc_header(surface, bld_name, self.shop.get("welcome", ""), mx, my, building_type="store")

        total_gold = sum(c.gold for c in self.party)
        draw_text(surface, f"Party Gold: {total_gold}", SCREEN_W // 2 - 60, 85, DIM_GOLD, 16)

        options = [
            ("Buy", "Browse weapons, armor, and supplies", BUY_COL),
            ("Sell", "Sell items from your inventory", SELL_COL),
            ("Back to Town", "Return to the town square", GREY),
        ]

        for i, (name, desc, accent) in enumerate(options):
            btn = pygame.Rect(SCREEN_W // 2 - 200, 148 + i * 90, 400, 75)
            hover = btn.collidepoint(mx, my)
            bg = (40, 35, 65) if hover else (25, 20, 45)
            pygame.draw.rect(surface, bg, btn, border_radius=4)
            pygame.draw.rect(surface, accent if hover else PANEL_BORDER, btn, 2, border_radius=4)
            draw_text(surface, name, btn.x + 20, btn.y + 12, accent if hover else CREAM, 20, bold=True)
            draw_text(surface, desc, btn.x + 20, btn.y + 42, GREY, 15)

        self._draw_party_bar(surface, mx, my)

    # ─────────────────────────────────────────────────────────
    #  GENERAL STORE — Buy
    # ─────────────────────────────────────────────────────────

    def _draw_shop_buy(self, surface, mx, my):
        from core.equipment import can_equip
        draw_text(surface, "Buy Items", 20, 12, GOLD, 22, bold=True)

        # Back button — bottom of left panel, above party bar
        _sb_back = pygame.Rect(8, SCREEN_H - 140, 120, 34)
        draw_button(surface, _sb_back, "← Back",
                    hover=_sb_back.collidepoint(mx, my), size=13,
                    bg=(50,35,70), border=(120,90,160), color=(220,200,255))

        # ── Character tabs (6a) ───────────────────────────────────────
        n = len(self.party)
        tab_w = min(180, (SCREEN_W - 170) // max(n, 1))
        self._shop_char_tab_rects = []
        for i, ch in enumerate(self.party):
            tr = pygame.Rect(20 + i * (tab_w + 4), 50, tab_w, 32)
            self._shop_char_tab_rects.append(tr)
            is_sel = (i == self.shop_char_idx)
            hover  = tr.collidepoint(mx, my)
            bg     = (50, 40, 85) if is_sel else (35, 30, 60) if hover else (20, 18, 36)
            border = GOLD if is_sel else HIGHLIGHT if hover else PANEL_BORDER
            pygame.draw.rect(surface, bg, tr, border_radius=3)
            pygame.draw.rect(surface, border, tr, 2, border_radius=3)
            label  = f"{ch.name}  {ch.gold}g"
            draw_text(surface, label, tr.x + 8, tr.y + 7,
                      GOLD if is_sel else CREAM, 13, bold=is_sel)

        # Clamp idx in case party shrank while shop was open
        if self.party:
            self.shop_char_idx = min(self.shop_char_idx, len(self.party) - 1)
        sel_char = self.party[self.shop_char_idx] if self.party else None

        # ── Category tabs ────────────────────────────────────────────
        tabs = [("weapons", "Weapons"), ("armor", "Armor"), ("consumables", "Supplies")]
        for i, (key, label) in enumerate(tabs):
            tr = pygame.Rect(20 + i * 140, 95, 130, 28)
            is_sel = (self.shop_tab == key)
            hover  = tr.collidepoint(mx, my)
            bg     = (50, 40, 85) if is_sel else (35, 30, 60) if hover else (20, 18, 36)
            border = GOLD if is_sel else HIGHLIGHT if hover else PANEL_BORDER
            pygame.draw.rect(surface, bg, tr, border_radius=3)
            pygame.draw.rect(surface, border, tr, 2, border_radius=3)
            draw_text(surface, label, tr.x + 10, tr.y + 6,
                      GOLD if is_sel else CREAM, 13, bold=is_sel)

        # ── Item list panel ──────────────────────────────────────────
        # Reserve right 240px for comparison panel on weapons/armor tabs
        is_equip_tab = self.shop_tab in ("weapons", "armor")
        list_w = SCREEN_W - 40 - (244 if is_equip_tab else 0)
        panel = pygame.Rect(20, 132, list_w, SCREEN_H - 237)
        draw_panel(surface, panel, bg_color=SHOP_BG)

        items = list(self.shop.get(self.shop_tab, []))
        buyback_start = len(items)
        items.extend(self.sold_items)

        if not items:
            draw_text(surface, "Nothing in this category.", panel.x + 20, panel.y + 20, DARK_GREY, 15)
        else:
            iy = panel.y + 8
            max_vis = 7
            start = self.shop_scroll
            end   = min(len(items), start + max_vis)

            # Track which row is hovered for comparison panel
            hovered_item = None

            for idx in range(start, end):
                item = items[idx]
                is_buyback = idx >= buyback_start
                row = pygame.Rect(panel.x + 6, iy, panel.width - 12, 64)
                hover = row.collidepoint(mx, my)
                if hover:
                    hovered_item = item

                # ── 6b: equippability check ──────────────────────────
                equippable = True
                equip_reason = ""
                if sel_char and self.shop_tab in ("weapons", "armor"):
                    ok, reason = can_equip(sel_char, item)
                    equippable = ok
                    equip_reason = reason

                # ── 6e: upgrade highlight ────────────────────────────
                is_upgrade = False
                if sel_char and equippable and self.shop_tab in ("weapons", "armor"):
                    slot = item.get("slot")
                    equipped = sel_char.equipment.get(slot) if sel_char.equipment else None
                    if equipped:
                        new_stat = item.get("damage", 0) or item.get("defense", 0)
                        old_stat = equipped.get("damage", 0) or equipped.get("defense", 0)
                        is_upgrade = new_stat > old_stat

                if is_buyback:
                    bg = (30, 28, 18) if hover else (22, 20, 12)
                elif is_upgrade and equippable:
                    bg = (28, 26, 10) if hover else (22, 20, 8)
                else:
                    bg = ITEM_HOVER if hover else ITEM_BG
                pygame.draw.rect(surface, bg, row, border_radius=3)

                # Gold border for upgrades (6e)
                border_col = (160, 130, 20) if is_upgrade and equippable else (HIGHLIGHT if hover else PANEL_BORDER)
                pygame.draw.rect(surface, border_col, row, 2 if is_upgrade else 1, border_radius=3)

                if is_buyback:
                    draw_text(surface, "BUYBACK", row.x + row.width - 80, row.y + 4, (180, 150, 60), 10, bold=True)

                rarity  = item.get("rarity", "common")
                name_col = RARITY_COLORS.get(rarity, CREAM)
                if not equippable:
                    name_col = DARK_GREY
                draw_text(surface, item["name"], row.x + 10, row.y + 4, name_col, 14, bold=True)

                # Can't-use label (6b)
                if not equippable and equip_reason:
                    short = equip_reason.split(" cannot ")[-1] if " cannot " in equip_reason else "Not usable"
                    draw_text(surface, f"✗ {short}", row.x + 10, row.y + 22, (140, 80, 80), 11)
                else:
                    desc = item.get("description", "")
                    if len(desc) > 70: desc = desc[:67] + "..."
                    draw_text(surface, desc, row.x + 10, row.y + 22, GREY, 12)

                # Stats line
                parts = []
                if item.get("damage"):   parts.append(f"DMG {item['damage']}")
                if item.get("defense", 0): parts.append(f"DEF +{item['defense']}")
                if item.get("heal_amount"): parts.append(f"Heal {item['heal_amount']}")
                for stat, val in item.get("stat_bonuses", {}).items():
                    parts.append(f"{stat}+{val}")
                if parts:
                    draw_text(surface, "  ".join(parts), row.x + 10, row.y + 42, GREY, 12)

                # Price — grey if unaffordable (6e), red if can't afford at all
                price = item.get("buy_price", 0)
                can_afford = sel_char and sel_char.gold >= price
                if not sel_char:
                    price_col = DIM_GOLD
                elif can_afford:
                    price_col = BUY_COL if hover else DIM_GOLD
                else:
                    price_col = (100, 90, 90)   # greyed price (6e)
                draw_text(surface, f"{price}g", row.x + row.width - 58, row.y + 4, price_col, 15, bold=True)

                if hover:
                    if not can_afford:
                        lbl = "Switch to a character who can afford this." if any(c.gold >= price for c in self.party) else "Not enough gold"
                    elif not equippable:
                        lbl = "Not usable by this character"
                    else:
                        lbl = "Click to buy"
                    draw_text(surface, lbl, row.x + 10, row.y + 50,
                              BUY_COL if (can_afford and equippable) else (180, 120, 60), 10)

                iy += 68

            if self.shop_scroll > 0:
                draw_text(surface, "▲ scroll", panel.x + 10, panel.y + 2, DIM_GOLD, 11)
            if end < len(items):
                draw_text(surface, "▼ scroll", panel.x + 10, iy + 2, DIM_GOLD, 11)

            # ── 6c: Comparison panel ─────────────────────────────────
            if is_equip_tab and sel_char:
                cp = pygame.Rect(panel.x + panel.width + 8, 132, 232, SCREEN_H - 237)
                draw_panel(surface, cp, bg_color=(18, 15, 30))
                draw_text(surface, "Equipped", cp.x + 8, cp.y + 8, GOLD, 13, bold=True)
                draw_text(surface, sel_char.name, cp.x + 8, cp.y + 24, GREY, 11)

                compare_item = hovered_item
                if compare_item and can_equip(sel_char, compare_item)[0]:
                    slot = compare_item.get("slot")
                    equipped = sel_char.equipment.get(slot) if sel_char.equipment else None
                    cy = cp.y + 44
                    if equipped:
                        draw_text(surface, equipped.get("name", "Unknown"), cp.x + 8, cy, CREAM, 12, bold=True)
                        cy += 18
                        new_dmg = compare_item.get("damage", 0)
                        old_dmg = equipped.get("damage", 0)
                        new_def = compare_item.get("defense", 0)
                        old_def = equipped.get("defense", 0)
                        if old_dmg or new_dmg:
                            diff = new_dmg - old_dmg
                            col  = (80, 200, 80) if diff > 0 else (200, 80, 80) if diff < 0 else GREY
                            draw_text(surface, f"DMG  {old_dmg} → {new_dmg}  ({'+' if diff>=0 else ''}{diff})",
                                      cp.x + 8, cy, col, 11)
                            cy += 16
                        if old_def or new_def:
                            diff = new_def - old_def
                            col  = (80, 200, 80) if diff > 0 else (200, 80, 80) if diff < 0 else GREY
                            draw_text(surface, f"DEF  {old_def} → {new_def}  ({'+' if diff>=0 else ''}{diff})",
                                      cp.x + 8, cy, col, 11)
                            cy += 16
                    else:
                        draw_text(surface, "Nothing equipped", cp.x + 8, cy, DARK_GREY, 11)
                        cy += 18
                        if compare_item.get("damage"):
                            draw_text(surface, f"DMG  — → {compare_item['damage']}", cp.x + 8, cy, (80, 200, 80), 11)
                        elif compare_item.get("defense"):
                            draw_text(surface, f"DEF  — → +{compare_item['defense']}", cp.x + 8, cy, (80, 200, 80), 11)
                else:
                    draw_text(surface, "Hover an item", cp.x + 8, cp.y + 44, DARK_GREY, 11)
                    draw_text(surface, "to compare",   cp.x + 8, cp.y + 60, DARK_GREY, 11)

        self._draw_party_bar(surface, mx, my)

    # ─────────────────────────────────────────────────────────
    #  GENERAL STORE — Sell
    # ─────────────────────────────────────────────────────────

    def _draw_shop_sell(self, surface, mx, my):
        draw_text(surface, "Sell Items", 20, 12, GOLD, 22, bold=True)

        total_gold = sum(c.gold for c in self.party)
        draw_text(surface, f"Party Gold: {total_gold}", SCREEN_W // 2 - 80, 15, DIM_GOLD, 16)

        # Back button — bottom of left panel, above party bar
        _ss_back = pygame.Rect(8, SCREEN_H - 140, 120, 34)
        draw_button(surface, _ss_back, "← Back",
                    hover=_ss_back.collidepoint(mx, my), size=13,
                    bg=(50,35,70), border=(120,90,160), color=(220,200,255))

        # Character tabs — below NPC portrait card (card bottom ~134px), clear of back button
        tab_area_w = SCREEN_W - 170  # leave 170px for back button
        for i, c in enumerate(self.party):
            cls = CLASSES[c.class_name]
            tw = tab_area_w // len(self.party)
            tr = pygame.Rect(20 + i * tw, 140, tw - 4, 32)
            is_sel = (i == self.sell_char)
            hover = tr.collidepoint(mx, my)
            bg = (50, 40, 85) if is_sel else (35, 30, 60) if hover else (20, 18, 36)
            border = cls["color"] if is_sel else HIGHLIGHT if hover else PANEL_BORDER
            pygame.draw.rect(surface, bg, tr, border_radius=3)
            pygame.draw.rect(surface, border, tr, 2, border_radius=3)
            draw_text(surface, f"{c.name} ({len(c.inventory)})",
                      tr.x + 8, tr.y + 7, cls["color"] if is_sel else GREY, 13, bold=is_sel)

        char = self.party[self.sell_char]
        panel = pygame.Rect(20, 182, SCREEN_W - 40, SCREEN_H - 287)
        draw_panel(surface, panel, bg_color=SHOP_BG)

        if not char.inventory:
            draw_text(surface, f"{char.name}'s inventory is empty.",
                      panel.x + 20, panel.y + 20, DARK_GREY, 15)
        else:
            iy = panel.y + 10
            max_vis = 8
            start = self.sell_scroll
            end = min(len(char.inventory), start + max_vis)

            for idx in range(start, end):
                item = char.inventory[idx]
                row = pygame.Rect(panel.x + 8, iy, panel.width - 16, 68)
                hover = row.collidepoint(mx, my)
                bg = ITEM_HOVER if hover else ITEM_BG
                pygame.draw.rect(surface, bg, row, border_radius=3)
                pygame.draw.rect(surface, HIGHLIGHT if hover else PANEL_BORDER, row, 1, border_radius=3)

                name = get_item_display_name(item)
                rarity = item.get("rarity", "common")
                name_col = RARITY_COLORS.get(rarity, CREAM) if item.get("identified") else GREY
                draw_text(surface, name, row.x + 10, row.y + 4, name_col, 15, bold=True)

                item_type = item.get("type", "misc")
                draw_text(surface, item_type, row.x + 10, row.y + 24, DARK_GREY, 12)

                # Sell price
                price = get_sell_price(item)
                draw_text(surface, f"Sell: {price}g", row.x + row.width - 100, row.y + 4,
                          SELL_COL if hover else DIM_GOLD, 16, bold=True)
                if hover:
                    draw_text(surface, "Click to sell", row.x + row.width - 110, row.y + 48,
                              SELL_COL, 11)

                iy += 72

            if self.sell_scroll > 0:
                draw_text(surface, "^ scroll up", panel.x + panel.width // 2 - 40, panel.y + 2, DIM_GOLD, 13)
            if end < len(char.inventory):
                draw_text(surface, "v scroll down", panel.x + panel.width // 2 - 45, iy + 2, DIM_GOLD, 13)

        self._draw_party_bar(surface, mx, my)

    # ─────────────────────────────────────────────────────────
    #  TEMPLE
    # ─────────────────────────────────────────────────────────

    def _draw_temple(self, surface, mx, my):
        bld_name = self.current_bld_name or "Temple of Light"
        self._draw_bld_npc_header(surface, bld_name, TEMPLE.get("welcome", ""), mx, my, building_type="temple")

        total_gold = sum(c.gold for c in self.party)
        draw_text(surface, f"Party Gold: {total_gold}", SCREEN_W // 2 - 60, 85, DIM_GOLD, 16)


        # Services
        services = list(TEMPLE["services"].values())
        by = 120

        # PIE disposition banner
        max_pie = max((c.stats.get("PIE", 0) for c in self.party), default=0)
        if max_pie >= 15:
            pct_off = min(20, (max_pie - 14) * 2)
            pie_msg = f"The temple senses the divine in your party. Services discounted {pct_off}%."
            draw_text(surface, pie_msg, SCREEN_W // 2 - 245, 108, (180, 220, 255), 12)
            by = 132

        for i, svc in enumerate(services):
            btn = pygame.Rect(SCREEN_W // 2 - 250, by + i * 80, 500, 68)
            hover = btn.collidepoint(mx, my)
            base_cost = svc["cost"]
            cost, pct_off = self._pie_disposition_discount(base_cost)
            can_afford = total_gold >= cost

            bg = (35, 50, 45) if (hover and can_afford) else (25, 20, 45)
            border = HEAL_COL if (hover and can_afford) else RED if (hover and not can_afford) else PANEL_BORDER

            pygame.draw.rect(surface, bg, btn, border_radius=4)
            pygame.draw.rect(surface, border, btn, 2, border_radius=4)

            draw_text(surface, svc["name"], btn.x + 15, btn.y + 8,
                      HEAL_COL if hover else CREAM, 18, bold=True)
            draw_text(surface, svc["description"], btn.x + 15, btn.y + 34, GREY, 13)

            if cost == 0:
                price_str = "Free"
                price_col = HEAL_COL
            elif pct_off > 0:
                price_str = f"{base_cost}g → {cost}g"
                price_col = (180, 220, 255) if can_afford else RED
            else:
                price_str = f"{cost}g"
                price_col = DIM_GOLD if can_afford else RED
            draw_text(surface, price_str, btn.x + btn.width - 110, btn.y + 8,
                      price_col, 16, bold=True)

        # Identify section: show unidentified items if any
        unid_items = []
        for ci, c in enumerate(self.party):
            for ii, item in enumerate(c.inventory):
                from core.identification import needs_identification
                if needs_identification(item):
                    unid_items.append((ci, ii, item, c))

        if unid_items:
            uy = by + len(services) * 80 + 20
            draw_text(surface, f"Unidentified items ({len(unid_items)}):",
                      SCREEN_W // 2 - 250, uy, DIM_GOLD, 14)
            uy += 25
            for ui_idx, (ci, ii, item, char) in enumerate(unid_items[:5]):
                row = pygame.Rect(SCREEN_W // 2 - 250, uy, 500, 40)
                hover = row.collidepoint(mx, my)
                bg = ITEM_HOVER if hover else ITEM_BG
                pygame.draw.rect(surface, bg, row, border_radius=3)
                pygame.draw.rect(surface, PANEL_BORDER, row, 1, border_radius=3)

                name = get_item_display_name(item)
                draw_text(surface, f"{char.name}: {name}", row.x + 10, row.y + 10, GREY, 13)

                can_id = total_gold >= 15
                if hover:
                    lbl = "Click to identify (15g)" if can_id else "Not enough gold"
                    col = HEAL_COL if can_id else RED
                    draw_text(surface, lbl, row.x + row.width - 180, row.y + 10, col, 12)

                uy += 44

        self._draw_party_bar(surface, mx, my)

    # ─────────────────────────────────────────────────────────
    #  INN
    # ─────────────────────────────────────────────────────────

    def _draw_inn(self, surface, mx, my):
        from core.progression import INN_TIERS, INN_TIER_ORDER, can_level_up
        bld_name = self.current_bld_name or "The Inn"
        self._draw_bld_npc_header(surface, bld_name, "Rest your weary bones, save your progress.", mx, my, building_type="inn")


        # Save button — top right, next to Back
        save_btn = pygame.Rect(SCREEN_W - 280, 20, 128, 34)
        draw_button(surface, save_btn, "💾 Save Game", hover=save_btn.collidepoint(mx, my), size=13)
        # Party management button — opens inventory/equip/stats/transfer
        party_btn = pygame.Rect(SCREEN_W - 420, 20, 130, 34)
        draw_button(surface, party_btn, "👥 Party", hover=party_btn.collidepoint(mx, my), size=13)
        # Character sheet button
        sheet_btn = pygame.Rect(SCREEN_W - 570, 20, 140, 34)
        draw_button(surface, sheet_btn, "📋 Characters", hover=sheet_btn.collidepoint(mx, my), size=12)
        # Save feedback label
        if getattr(self, "_inn_save_msg", "") and getattr(self, "_inn_save_timer", 0) > 0:
            smsg_col = (120, 220, 120) if self._inn_save_ok else (220, 80, 80)
            draw_text(surface, self._inn_save_msg, SCREEN_W - 420, 60, smsg_col, 12)

        total_gold = sum(c.gold for c in self.party)
        party_size = len(self.party)
        draw_text(surface, f"Party Gold: {total_gold}", SCREEN_W // 2 - 60, 80, DIM_GOLD, 14)

        # Check for characters ready to level up
        lvl_ready = [c for c in self.party if can_level_up(c)]

        by = 148
        for i, tier_key in enumerate(INN_TIER_ORDER):
            tier = INN_TIERS[tier_key]
            room_cost = tier["cost_per_char"] * party_size

            total_cost = room_cost

            btn = pygame.Rect(SCREEN_W // 2 - 280, by + i * 95, 560, 85)
            hover = btn.collidepoint(mx, my)
            can_afford = total_gold >= total_cost

            bg = (50, 40, 25) if hover and can_afford else (30, 24, 18)
            border = (220, 180, 80) if hover and can_afford else PANEL_BORDER
            if not can_afford:
                bg = (25, 20, 15)

            pygame.draw.rect(surface, bg, btn, border_radius=5)
            pygame.draw.rect(surface, border, btn, 2, border_radius=5)

            name_col = GOLD if can_afford else DARK_GREY
            draw_text(surface, tier["name"], btn.x + 15, btn.y + 8, name_col, 18, bold=True)

            if room_cost > 0:
                cost_str = f"{room_cost}g ({tier['cost_per_char']}g × {party_size})"
            else:
                cost_str = "Free"
            draw_text(surface, cost_str, btn.x + 250, btn.y + 10, DIM_GOLD if can_afford else DARK_GREY, 13)

            draw_text(surface, tier["description"], btn.x + 15, btn.y + 35, GREY, 12)

            if lvl_ready:
                draw_text(surface, f"{len(lvl_ready)} character(s) ready to level up at guild!",
                          btn.x + 15, btn.y + 55, (180, 220, 120), 12)

            if tier.get("buff"):
                draw_text(surface, f"Bonus: {tier['buff']['name']} (+{tier['buff']['hp_bonus_pct']}% HP next dungeon)",
                          btn.x + 15, btn.y + 68, (150, 200, 255), 11)

        # Show inn result if just rested
        if self.inn_result:
            rp = pygame.Rect(SCREEN_W // 2 - 250, by + len(INN_TIER_ORDER) * 95 + 10, 500, 60)
            pygame.draw.rect(surface, (20, 30, 15), rp, border_radius=5)
            pygame.draw.rect(surface, GREEN, rp, 1, border_radius=5)
            draw_text(surface, self.inn_result, rp.x + 15, rp.y + 10, GREEN, 14, max_width=470)

        self._draw_party_bar(surface, mx, my)

    # ─────────────────────────────────────────────────────────
    #  SKILL TRAINER
    # ─────────────────────────────────────────────────────────

    def _draw_inn_trainer(self, surface, mx, my):
        """Skill trainer view — learn unlearned abilities for gold."""
        from core.abilities import get_unlearned_abilities

        if getattr(self, "_trainer_origin", "inn") == "guild":
            bld_name = getattr(self, "_guild_building_name", "Adventurers' Guild")
            subtitle = "Purchase training — spend gold to master new abilities."
        else:
            bld_name = self.current_bld_name or "The Inn"
            subtitle = "Train your skills — spend gold to master new abilities."
        self._draw_bld_npc_header(surface, bld_name, subtitle, mx, my, building_type="inn")


        total_gold = sum(c.gold for c in self.party)
        draw_text(surface, f"Party Gold: {total_gold}g", SCREEN_W // 2 - 60, 80, DIM_GOLD, 14)

        # Character tabs
        tab_area_w = SCREEN_W - 170
        tw = tab_area_w // len(self.party)
        for i, c in enumerate(self.party):
            cls = CLASSES[c.class_name]
            tr = pygame.Rect(20 + i * tw, 108, tw - 4, 28)
            is_sel = (i == self.trainer_char_idx)
            hover = tr.collidepoint(mx, my)
            bg = (50, 40, 85) if is_sel else (35, 30, 60) if hover else (20, 18, 36)
            border = cls["color"] if is_sel else HIGHLIGHT if hover else PANEL_BORDER
            pygame.draw.rect(surface, bg, tr, border_radius=3)
            pygame.draw.rect(surface, border, tr, 2, border_radius=3)
            draw_text(surface, c.name, tr.x + 8, tr.y + 5,
                      cls["color"] if is_sel else GREY, 13, bold=is_sel)

        char = self.party[self.trainer_char_idx]
        unlearned = get_unlearned_abilities(char)

        y = 150
        if not unlearned:
            draw_text(surface,
                f"{char.name} has learned all available abilities for their current level.",
                40, y + 20, GREY, 14)
            draw_text(surface, "Level up at the inn to unlock more skills.",
                      40, y + 44, STAT_LABEL, 12)
            return

        draw_text(surface,
            f"Available to learn — {char.name} (Level {char.level}):",
            40, y, GOLD, 14, bold=True)
        y += 24

        VISIBLE = 7
        start = self.trainer_scroll
        visible_abs = unlearned[start:start + VISIBLE]
        self._trainer_rects = []

        TYPE_COL = {
            "spell": (140, 100, 255), "heal": (80, 220, 140),
            "aoe_heal": (80, 220, 140), "buff": (80, 180, 255),
            "attack": (220, 120, 80), "aoe": (255, 160, 60),
            "debuff": (200, 80, 120),
        }

        for i, ab in enumerate(visible_abs):
            ab_level = ab.get("level", 1)
            cost = ab_level * 20   # 20g per ability level — affordable but meaningful
            can_afford = total_gold >= cost

            row = pygame.Rect(40, y + i * 74, SCREEN_W - 80, 68)
            hover = row.collidepoint(mx, my)
            bg = (45, 35, 25) if (hover and can_afford) else (25, 20, 35)
            border = (220, 180, 80) if (hover and can_afford) else PANEL_BORDER
            pygame.draw.rect(surface, bg, row, border_radius=5)
            pygame.draw.rect(surface, border, row, 1, border_radius=5)

            ab_type = ab.get("type", "skill")
            type_col = TYPE_COL.get(ab_type, CREAM)
            draw_text(surface, ab["name"], row.x + 14, row.y + 8,
                      GOLD if can_afford else GREY, 16, bold=True)
            draw_text(surface, f"[{ab_type.title()}]",
                      row.x + 14, row.y + 30, type_col, 11)
            draw_text(surface, f"Unlocks at Level {ab_level}",
                      row.x + 120, row.y + 30, STAT_LABEL, 11)
            desc = ab.get("desc", ab.get("description", ""))[:70]
            draw_text(surface, desc, row.x + 14, row.y + 48, STAT_LABEL, 11)

            cost_col = DIM_GOLD if can_afford else (120, 60, 60)
            draw_text(surface, f"Cost: {cost}g",
                      row.x + row.width - 200, row.y + 10, cost_col, 13)
            btn = pygame.Rect(row.x + row.width - 130, row.y + 16, 100, 32)
            draw_button(surface, btn, "Learn",
                        hover=(btn.collidepoint(mx, my) and can_afford),
                        size=13)

            self._trainer_rects.append((row, btn, ab, cost, can_afford))

        if start > 0:
            draw_text(surface, "▲ More above", SCREEN_W // 2 - 40, 148, GREY, 11)
        if start + VISIBLE < len(unlearned):
            draw_text(surface, "▼ More below",
                      SCREEN_W // 2 - 40, y + VISIBLE * 74 + 2, GREY, 11)

    # ─────────────────────────────────────────────────────────
    #  CHARACTER SHEET
    # ─────────────────────────────────────────────────────────

    def _draw_inn_charsheet(self, surface, mx, my):
        """Consolidated single-character sheet — all info on one screen."""
        from core.classes import get_all_resources, STAT_NAMES
        from core.equipment import (SLOT_ORDER, SLOT_NAMES,
                                    calc_equipment_defense,
                                    calc_equipment_magic_resist)
        from core.progression import PLANAR_TIERS, get_party_tier
        from core.identification import get_item_display_name

        if not self.party:
            return

        # Back button — top-right of left panel area
        _cs_back = pygame.Rect(8, SCREEN_H - 140, 120, 34)
        draw_button(surface, _cs_back, "← Back",
                    hover=_cs_back.collidepoint(mx, my), size=13,
                    bg=(50,35,70), border=(120,90,160), color=(220,200,255))

        # Character navigation arrows
        n = len(self.party)
        if n > 1:
            larr = pygame.Rect(10, SCREEN_H // 2 - 22, 34, 44)
            rarr = pygame.Rect(SCREEN_W - 44, SCREEN_H // 2 - 22, 34, 44)
            for arr in (larr, rarr):
                pygame.draw.rect(surface, (40, 35, 60), arr, border_radius=4)
                pygame.draw.rect(surface, PANEL_BORDER, arr, 1, border_radius=4)
            draw_text(surface, "◀", larr.x + 8, larr.y + 12, GREY, 18)
            draw_text(surface, "▶", rarr.x + 8, rarr.y + 12, GREY, 18)

        c = self.party[self.charsheet_idx]
        cls = CLASSES.get(c.class_name, {})
        cls_col = cls.get("color", CREAM)

        # Header
        draw_class_badge(surface, c.class_name, 48, 14, 16)
        draw_text(surface, c.name, 90, 16, cls_col, 22, bold=True)
        race_str = getattr(c, "race_name", "Human")
        draw_text(surface, f"Level {c.level}  {race_str} {c.class_name}",
                  90, 42, CREAM, 14)
        draw_text(surface, f"[{self.charsheet_idx + 1}/{n}]", 90, 60, GREY, 11)

        # Tier badge
        try:
            from core.story_flags import _flags as _sf
            flags = dict(_sf)
        except Exception:
            flags = {}
        min_lvl = min(cc.level for cc in self.party) if self.party else 1
        tier_idx = get_party_tier(flags, min_lvl)
        tier_data = PLANAR_TIERS.get(tier_idx, PLANAR_TIERS[0])
        draw_text(surface,
                  f"{tier_data['symbol']} {tier_data['name']}",
                  SCREEN_W // 2 - 60, 20, tier_data["color"], 14, bold=True)

        eff = c.effective_stats() if hasattr(c, "effective_stats") else c.stats

        # Three columns
        L1 = 48   # Left: stats + resources
        L2 = 390  # Middle: abilities
        L3 = 760  # Right: equipment
        COL_Y = 90

        # ── LEFT COLUMN: Stats ────────────────────────────────
        pygame.draw.line(surface, (60, 50, 80), (L1, COL_Y), (L1 + 300, COL_Y))
        draw_text(surface, "ATTRIBUTES", L1, COL_Y + 4, STAT_LABEL, 10, bold=True)
        sy = COL_Y + 20
        FULL_NAMES = {"STR": "Strength", "DEX": "Dexterity", "CON": "Constitution",
                      "INT": "Intelligence", "WIS": "Wisdom", "PIE": "Piety"}
        for i, stat in enumerate(STAT_NAMES):
            base = c.stats.get(stat, 0)
            effective = eff.get(stat, base)
            col_v = (100, 200, 120) if effective > base else \
                    (200, 80, 80) if effective < base else STAT_VAL
            sx = L1 + (i % 2) * 155
            sdy = sy + (i // 2) * 20
            draw_text(surface, f"{FULL_NAMES.get(stat, stat)[:3]}:", sx, sdy, STAT_LABEL, 12)
            draw_text(surface, str(effective), sx + 36, sdy, col_v, 12, bold=True)
            if effective != base:
                diff = effective - base
                draw_text(surface,
                          f"({'+' if diff > 0 else ''}{diff})",
                          sx + 58, sdy, col_v, 10)
        sy += ((len(STAT_NAMES) + 1) // 2) * 20 + 8

        # Combat stats
        pygame.draw.line(surface, (60, 50, 80), (L1, sy), (L1 + 300, sy))
        draw_text(surface, "COMBAT", L1, sy + 4, STAT_LABEL, 10, bold=True)
        sy += 20
        try:
            equip_def = calc_equipment_defense(c)
            equip_mr  = calc_equipment_magic_resist(c)
            dex_bonus = max(0, (eff.get("DEX", 10) - 10) // 2)
            ac = 10 + dex_bonus + equip_def
            total_mr = equip_mr + eff.get("WIS", 0) * 2
            draw_text(surface,
                      f"AC: {ac}  (DEX {dex_bonus:+d} + Equip {equip_def})",
                      L1, sy, STAT_VAL, 11)
            sy += 16
            draw_text(surface,
                      f"MR: {total_mr}  (WIS {eff.get('WIS',0)*2} + Equip {equip_mr})",
                      L1, sy, STAT_VAL, 11)
            sy += 16
        except Exception:
            pass

        # Resources
        pygame.draw.line(surface, (60, 50, 80), (L1, sy), (L1 + 300, sy))
        draw_text(surface, "RESOURCES", L1, sy + 4, STAT_LABEL, 10, bold=True)
        sy += 20
        max_res = get_all_resources(c.class_name, eff, c.level)
        for rk, mval in max_res.items():
            cur = c.resources.get(rk, 0)
            pct = cur / mval if mval > 0 else 0
            draw_text(surface, f"{rk}:", L1, sy, STAT_LABEL, 12)
            bar = pygame.Rect(L1 + 70, sy + 3, 160, 9)
            pygame.draw.rect(surface, HP_BAR_BG, bar, border_radius=2)
            fc = HP_BAR if rk == "HP" else MP_BAR if "MP" in rk else SP_BAR
            fill = pygame.Rect(bar.x, bar.y, int(bar.width * pct), bar.height)
            pygame.draw.rect(surface, fc, fill, border_radius=2)
            draw_text(surface, f"{cur}/{mval}", bar.x + bar.width + 6, sy, GREY, 11)
            sy += 18

        # XP bar
        from core.progression import xp_for_level
        xp_this = xp_for_level(c.level)
        xp_next = xp_for_level(c.level + 1)
        xp_pct = min(1.0, (c.xp - xp_this) / max(1, xp_next - xp_this))
        sy += 4
        draw_text(surface, f"XP: {c.xp:,}", L1, sy, DIM_GOLD, 11)
        xpbar = pygame.Rect(L1 + 70, sy + 3, 160, 9)
        pygame.draw.rect(surface, (30, 25, 45), xpbar, border_radius=2)
        xpfill = pygame.Rect(xpbar.x, xpbar.y, int(xpbar.width * xp_pct), xpbar.height)
        pygame.draw.rect(surface, DIM_GOLD, xpfill, border_radius=2)

        # ── MIDDLE COLUMN: Abilities ──────────────────────────
        pygame.draw.line(surface, (60, 50, 80), (L2, COL_Y), (L2 + 330, COL_Y))
        draw_text(surface, "ABILITIES KNOWN", L2, COL_Y + 4, STAT_LABEL, 10, bold=True)
        ay = COL_Y + 20
        AB_TYPE_COL = {
            "spell": (160, 120, 255), "heal": (80, 200, 130),
            "aoe_heal": (80, 200, 130), "attack": (220, 120, 80),
            "buff": (80, 180, 255), "aoe": (255, 160, 60),
            "debuff": (200, 80, 120),
        }
        if c.abilities:
            for ab in c.abilities:
                ab_col = AB_TYPE_COL.get(ab.get("type", ""), CREAM)
                draw_text(surface, f"• {ab['name']}", L2, ay, ab_col, 12)
                rk = ab.get("resource", "")
                cost = ab.get("cost", 0)
                if cost and rk:
                    short = rk.split("-")[-1]
                    draw_text(surface, f"[{cost} {short}]",
                              L2 + 190, ay, STAT_LABEL, 11)
                ay += 17
                if ay > SCREEN_H - 80:
                    draw_text(surface, "…", L2, ay, GREY, 11)
                    break
        else:
            draw_text(surface, "No abilities learned.", L2, ay, GREY, 12)

        # ── RIGHT COLUMN: Equipment ───────────────────────────
        pygame.draw.line(surface, (60, 50, 80), (L3, COL_Y), (L3 + 650, COL_Y))
        draw_text(surface, "EQUIPMENT", L3, COL_Y + 4, STAT_LABEL, 10, bold=True)
        ey = COL_Y + 20
        equip = getattr(c, "equipment", {}) or {}
        RARITY_COLORS = {
            "common": CREAM, "uncommon": (80, 200, 140),
            "rare": (100, 150, 255), "epic": (200, 80, 220),
            "legendary": (255, 180, 40),
        }
        for slot in SLOT_ORDER:
            item = equip.get(slot)
            slot_label = SLOT_NAMES.get(slot, slot.replace("_", " ").title())
            draw_text(surface, f"{slot_label}:", L3, ey, STAT_LABEL, 11)
            if item:
                identified = item.get("identified", True)
                name = get_item_display_name(item) if identified \
                       else item.get("unidentified_name", "???")
                rarity = item.get("rarity", "common")
                name_col = RARITY_COLORS.get(rarity, CREAM) if identified else GREY
                draw_text(surface, name[:28], L3 + 110, ey, name_col, 11)
                # Key stat summary
                stat_parts = []
                if item.get("damage"):    stat_parts.append(f"dmg {item['damage']}")
                if item.get("defense"):   stat_parts.append(f"def {item['defense']}")
                if item.get("spell_bonus"): stat_parts.append(f"sp+{item['spell_bonus']}")
                eff_dict = item.get("effect", {})
                if isinstance(eff_dict, dict):
                    for k, v in eff_dict.items():
                        if v:
                            stat_parts.append(f"{k.replace('_bonus','')[0].upper()}{abs(v)}")
                if stat_parts:
                    draw_text(surface, "  ".join(stat_parts[:4]),
                              L3 + 390, ey, STAT_LABEL, 10)
            else:
                draw_text(surface, "—", L3 + 110, ey, (50, 45, 65), 11)
            ey += 17

    def _draw_inn_levelup(self, surface, mx, my):
        """
        Level-up screen: left panel = stat picker, right panel = full ability tree.
        Shows locked/unlocked/new abilities for the character's class.
        """
        from core.progression import training_cost
        from core.classes import STAT_NAMES
        from core.abilities import CLASS_ABILITIES, get_new_abilities_at_level

        if not self.levelup_queue:
            self.view = self.VIEW_INN
            return

        c    = self.levelup_queue[self.levelup_current]
        cost = training_cost(c.level + 1)
        cls  = CLASSES.get(c.class_name, {})
        col  = cls.get("color", CREAM)
        next_lvl = c.level + 1

        # Header
        draw_class_badge(surface, c.class_name, 20, 14, 16)
        draw_text(surface, f"{c.name}  —  Level {c.level} → {next_lvl}", 58, 18, col, 22, bold=True)
        draw_text(surface, f"Training cost: {cost}g", 58, 48, DIM_GOLD, 14)
        party_gold = sum(cc.gold for cc in self.party)
        gold_col = GREEN if party_gold >= cost else RED
        draw_text(surface, f"Party gold: {party_gold}g", 260, 48, gold_col, 14)

        # Left panel: stat picker
        left_panel = pygame.Rect(20, 80, 310, 420)
        draw_panel(surface, left_panel)
        draw_text(surface, "Assign 1 free stat point:", left_panel.x + 14, left_panel.y + 10, GOLD, 15, bold=True)

        growth = cls.get("stat_growth", {})
        for i, stat in enumerate(STAT_NAMES):
            btn     = pygame.Rect(left_panel.x + 10, left_panel.y + 38 + i * 60, left_panel.width - 20, 52)
            selected= self.levelup_free_stat == stat
            hover   = btn.collidepoint(mx, my)
            tier    = growth.get(stat, "low")
            tier_col= {"high":(180,220,120),"medium":(180,180,100),"low":(120,120,100)}.get(tier, GREY)
            bg      = (55, 45, 25) if selected else (38, 32, 20) if hover else (22, 18, 12)
            border  = GOLD if selected else tier_col if hover else (50, 45, 35)
            pygame.draw.rect(surface, bg,     btn, border_radius=4)
            pygame.draw.rect(surface, border, btn, 2 if selected else 1, border_radius=4)
            val = c.stats[stat]
            draw_text(surface, f"{stat}", btn.x + 10, btn.y + 4, tier_col, 18, bold=True)
            draw_text(surface, f"{val} → {val+1}", btn.x + 56, btn.y + 6, CREAM, 16)
            draw_text(surface, tier.upper(), btn.x + 10, btn.y + 30, tier_col, 10)
            if selected:
                pygame.draw.polygon(surface, GOLD,
                    [(btn.right-22, btn.y+18),(btn.right-10, btn.y+8),(btn.right-10, btn.y+28)])

        # Right panel: ability tree
        right_panel = pygame.Rect(340, 80, SCREEN_W - 360, 490)
        draw_panel(surface, right_panel, border_color=col)
        draw_text(surface, f"{c.class_name} Abilities", right_panel.x + 14, right_panel.y + 10, col, 15, bold=True)

        all_abs  = CLASS_ABILITIES.get(c.class_name, [])
        known    = {a["name"] for a in c.abilities}
        new_at   = {a["name"] for a in get_new_abilities_at_level(c.class_name, next_lvl)}

        row_h  = 68
        ab_x   = right_panel.x + 12
        ab_y   = right_panel.y + 38
        vis    = (right_panel.height - 48) // row_h

        for i, ab in enumerate(all_abs[:vis]):
            ry       = ab_y + i * row_h
            is_known = ab["name"] in known
            is_new   = ab["name"] in new_at
            is_next  = not is_known and not is_new and ab["level"] == next_lvl + 1
            locked   = ab["level"] > next_lvl and not is_known

            if is_new:
                bg_col, bd_col = (30,60,20), GREEN
            elif is_known:
                bg_col, bd_col = (20,30,50), (60,100,160)
            elif is_next:
                bg_col, bd_col = (35,28,15), (100,90,50)
            else:
                bg_col, bd_col = (18,14,10), (40,35,30)

            row_rect = pygame.Rect(ab_x, ry, right_panel.width - 24, row_h - 4)
            pygame.draw.rect(surface, bg_col, row_rect, border_radius=4)
            pygame.draw.rect(surface, bd_col, row_rect, 1, border_radius=4)

            lv_col = GREEN if is_new else (100,150,220) if is_known else (100,90,60) if is_next else (60,50,40)
            pygame.draw.rect(surface, (20,20,20), pygame.Rect(ab_x+4, ry+4, 36, 20), border_radius=3)
            draw_text(surface, f"Lv{ab['level']}", ab_x+5, ry+5, lv_col, 11, bold=True)

            if is_new:      tag, tag_col = "NEW!", GREEN
            elif is_known:  tag, tag_col = "Known", (100,150,220)
            elif locked:    tag, tag_col = f"Lv{ab['level']} req", (80,70,50)
            else:           tag, tag_col = "Next!", (180,160,80)
            draw_text(surface, tag, ab_x+46, ry+5, tag_col, 11)

            name_col = GOLD if is_new else (160,200,255) if is_known else (120,110,80) if not locked else (80,70,60)
            draw_text(surface, ab["name"], ab_x+46, ry+20, name_col, 14, bold=True)
            res_txt = f"{ab['cost']} {ab['resource']}" if ab.get("resource") else ""
            if res_txt:
                draw_text(surface, res_txt, ab_x + right_panel.width - 130, ry+22, (120,110,90), 11)
            desc_col = (160,160,140) if is_known or is_new else (80,75,60)
            draw_text(surface, ab.get("desc",""), ab_x+46, ry+40, desc_col, 11,
                      max_width=right_panel.width - 80)

        if len(all_abs) > vis:
            draw_text(surface, f"+ {len(all_abs)-vis} more at higher levels",
                      right_panel.x+14, right_panel.bottom-22, (80,80,60), 11)

        # Bottom buttons
        can_train = self.levelup_free_stat is not None and party_gold >= cost
        confirm = pygame.Rect(20, 516, 200, 46)
        draw_button(surface, confirm, "Train!", hover=confirm.collidepoint(mx, my) and can_train, size=16)
        if self.levelup_free_stat and not can_train:
            draw_text(surface, "Not enough gold!", confirm.x, confirm.y+50, RED, 12)
        elif not self.levelup_free_stat:
            draw_text(surface, "Pick a stat first", confirm.x+4, confirm.y+50, (100,90,60), 12)

        skip = pygame.Rect(240, 516, 130, 46)
        draw_button(surface, skip, "Skip", hover=skip.collidepoint(mx, my), size=14)

        tree_btn = pygame.Rect(390, 516, 200, 46)
        draw_button(surface, tree_btn, "Full Tree", hover=tree_btn.collidepoint(mx, my), size=13)

    def _draw_branch_choice(self, surface, mx, my):
        """
        Branch ability choice screen.
        Player selects ONE of two abilities, permanently locking the other path.
        Full-width dramatic presentation with flavour text.
        """
        c    = self.branch_pending_char
        opts = self.branch_pending_opts
        if not c or not opts:
            if getattr(self, "_guild_branch_origin", False):
                self._guild_branch_origin = False
                self.view = self.VIEW_GUILD
            else:
                self.view = self.VIEW_INN_LEVELUP_RESULT
            return

        cls     = CLASSES.get(c.class_name, {})
        col     = cls.get("color", CREAM)

        # Background atmosphere
        bg = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        bg.fill((10, 8, 20, 200))
        surface.blit(bg, (0, 0))

        # Header
        draw_class_badge(surface, c.class_name, 24, 20, 18)
        draw_text(surface, f"{c.name}  —  Level {c.level} Path Choice",
                  70, 24, col, 22, bold=True)
        draw_text(surface, "Your experience has opened a new path. Choose wisely — the other road closes forever.",
                  70, 56, (160, 140, 180), 14, max_width=SCREEN_W - 100)

        # "Choose your path" divider
        mid_x = SCREEN_W // 2
        pygame.draw.line(surface, (60, 50, 80), (mid_x, 90), (mid_x, SCREEN_H - 100), 1)
        draw_text(surface, "— OR —", mid_x - 28, SCREEN_H // 2 - 12, (120, 100, 160), 14)

        CARD_W = SCREEN_W // 2 - 40
        CARD_TOP = 90
        CARD_H   = SCREEN_H - 200

        for idx, opt in enumerate(opts):
            cx = 20 + idx * (SCREEN_W // 2)
            card = pygame.Rect(cx, CARD_TOP, CARD_W, CARD_H)
            hover = card.collidepoint(mx, my)
            if hover:
                self.branch_hover_idx = idx

            bg_col = (35, 55, 25) if (hover and idx == 0) else \
                     (25, 40, 65) if (hover and idx == 1) else \
                     (22, 18, 35)
            bd_col = col if hover else (60, 50, 90)
            pygame.draw.rect(surface, bg_col, card, border_radius=8)
            pygame.draw.rect(surface, bd_col, card, 2 if hover else 1, border_radius=8)

            # Branch label (big path identifier)
            label   = opt.get("branch_label", opt["name"])
            lbl_col = (200, 240, 140) if idx == 0 else (140, 180, 255)
            draw_text(surface, label.upper(), cx + 20, CARD_TOP + 18,
                      lbl_col, 20, bold=True)

            # Branch descriptor tagline
            tag = opt.get("branch_desc", "")
            draw_text(surface, tag, cx + 20, CARD_TOP + 48,
                      (160, 155, 170), 13, max_width=CARD_W - 40)

            # Divider line under tagline
            pygame.draw.line(surface, (50, 45, 70),
                             (cx + 20, CARD_TOP + 68), (cx + CARD_W - 20, CARD_TOP + 68))

            # Ability name
            draw_text(surface, opt["name"], cx + 20, CARD_TOP + 82,
                      col if hover else CREAM, 18, bold=True)

            # Cost / resource
            if opt.get("resource"):
                cost_str = f"{opt['cost']} {opt['resource']}"
                draw_text(surface, cost_str, cx + CARD_W - 120, CARD_TOP + 84,
                          DIM_GOLD, 13)

            # Description — wrapped generously
            draw_text(surface, opt.get("desc", ""), cx + 20, CARD_TOP + 114,
                      (190, 185, 160) if hover else (130, 125, 110), 13,
                      max_width=CARD_W - 40)

            # Type badge
            type_colors = {"attack": (200, 80, 80), "spell": (80, 120, 220),
                           "heal": (80, 200, 120), "buff": (200, 180, 60),
                           "debuff": (180, 80, 180), "aoe": (220, 120, 60)}
            type_col = type_colors.get(opt.get("type", ""), GREY)
            type_str = opt.get("type", "ability").upper()
            tr = pygame.Rect(cx + 20, CARD_TOP + CARD_H - 100, 80, 22)
            pygame.draw.rect(surface, (25, 20, 35), tr, border_radius=3)
            pygame.draw.rect(surface, type_col, tr, 1, border_radius=3)
            draw_text(surface, type_str, tr.x + 6, tr.y + 4, type_col, 11)

            # Element badge if applicable
            if opt.get("element"):
                elem_colors = {"fire": (220, 100, 40), "ice": (100, 180, 240),
                               "lightning": (240, 220, 60), "divine": (240, 220, 120),
                               "nature": (80, 180, 80), "arcane": (160, 100, 220)}
                ec = elem_colors.get(opt["element"], GREY)
                er = pygame.Rect(cx + 110, CARD_TOP + CARD_H - 100, 80, 22)
                pygame.draw.rect(surface, (25, 20, 35), er, border_radius=3)
                pygame.draw.rect(surface, ec, er, 1, border_radius=3)
                draw_text(surface, opt["element"].upper(), er.x + 6, er.y + 4, ec, 11)

            # Select button
            btn = pygame.Rect(cx + 20, CARD_TOP + CARD_H - 62, CARD_W - 40, 48)
            btn_hover = btn.collidepoint(mx, my)
            btn_col   = (lbl_col[0]//2, lbl_col[1]//2, lbl_col[2]//2)
            btn_bord  = lbl_col
            pygame.draw.rect(surface, btn_col, btn, border_radius=6)
            pygame.draw.rect(surface, btn_bord, btn, 2, border_radius=6)
            draw_text(surface, f"Choose {label}", btn.x + 20, btn.y + 14,
                      lbl_col, 15, bold=True)

    def _draw_levelup_result(self, surface, mx, my):
        """Fanfare screen after confirming level-up."""
        s = self.levelup_summary
        if not s:
            self.view = self.VIEW_INN
            return

        cls   = CLASSES.get(s.get("class_name",""), {})
        col   = cls.get("color", CREAM)

        # Glow
        glow = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        for r in range(260, 0, -4):
            a  = int(55 * (260-r)/260)
            rc, gc, bc = col
            pygame.draw.circle(glow, (rc//3, gc//3, bc//3, a), (SCREEN_W//2, SCREEN_H//2-60), r)
        surface.blit(glow, (0, 0))

        draw_class_badge(surface, s.get("class_name",""), SCREEN_W//2-220, 60, 22)
        draw_text(surface, "LEVEL UP!", SCREEN_W//2-100, 55, GOLD, 36, bold=True)
        draw_text(surface, f"{s.get('char_name','')}  is now Level {s.get('level','')}  {s.get('class_name','')}",
                  SCREEN_W//2-220, 105, col, 20)

        # Stat gains
        panel = pygame.Rect(SCREEN_W//2-320, 145, 300, 220)
        draw_panel(surface, panel, border_color=col)
        draw_text(surface, "Gains:", panel.x+14, panel.y+10, GOLD, 15, bold=True)
        gy = panel.y+40
        for stat, val in s.get("stat_gains",{}).items():
            draw_text(surface, f"+{val} {stat}", panel.x+20, gy, GREEN, 18); gy += 28
        if s.get("hp_gain"):
            draw_text(surface, f"+{s['hp_gain']} Max HP", panel.x+20, gy, (160,220,160), 16)

        # New ability panel
        ab_panel = pygame.Rect(SCREEN_W//2+20, 145, 340, 220)
        if s.get("new_abilities"):
            from core.abilities import CLASS_ABILITIES
            all_abs  = CLASS_ABILITIES.get(s.get("class_name",""), [])
            new_name = s["new_abilities"][0]
            ab_data  = next((a for a in all_abs if a["name"] == new_name), None)
            draw_panel(surface, ab_panel, border_color=(80,200,120))
            draw_text(surface, "Available to Train!", ab_panel.x+14, ab_panel.y+10, (80,200,120), 14, bold=True)
            draw_text(surface, "Visit the Guild to purchase training.", ab_panel.x+14, ab_panel.y+28, DIM_GOLD, 11)
            if ab_data:
                draw_text(surface, ab_data["name"], ab_panel.x+14, ab_panel.y+50, GOLD, 18, bold=True)
                draw_text(surface, f"{ab_data['cost']} {ab_data.get('resource','')}",
                          ab_panel.x+14, ab_panel.y+76, DIM_GOLD, 13)
                draw_wrapped_text(surface, ab_data.get("desc",""),
                                  ab_panel.x+14, ab_panel.y+98,
                                  ab_panel.width-28, (210,210,190), get_font(13))
            if len(s["new_abilities"]) > 1:
                draw_text(surface, f"+ {len(s['new_abilities'])-1} more available!",
                          ab_panel.x+14, ab_panel.bottom-22, (80,200,120), 11)
        else:
            draw_panel(surface, ab_panel, border_color=(60,50,40))
            draw_text(surface, "No new abilities this level.", ab_panel.x+14, ab_panel.y+80, (100,90,70), 14)
            from core.abilities import CLASS_ABILITIES
            all_abs = CLASS_ABILITIES.get(s.get("class_name",""), [])
            nxt = next((a for a in all_abs if a["level"] > s.get("level",1)), None)
            if nxt:
                draw_text(surface, "Coming next:", ab_panel.x+14, ab_panel.y+120, DIM_GOLD, 13)
                draw_text(surface, f"{nxt['name']}  (Level {nxt['level']})",
                          ab_panel.x+14, ab_panel.y+142, (160,150,100), 15)
                draw_text(surface, nxt.get("desc",""), ab_panel.x+14, ab_panel.y+168,
                          (100,95,80), 12, max_width=ab_panel.width-28)

        # Branch choice result (if applicable)
        if s.get("branch_chosen"):
            branch_panel = pygame.Rect(SCREEN_W//2 - 320, 380, 660, 100)
            draw_panel(surface, branch_panel, border_color=(160, 120, 220))
            draw_text(surface, "PATH CHOSEN:", branch_panel.x + 14, branch_panel.y + 10,
                      (160, 120, 220), 13, bold=True)
            draw_text(surface, s["branch_label"].upper(), branch_panel.x + 14,
                      branch_panel.y + 34, (200, 170, 255), 20, bold=True)
            draw_text(surface, s["branch_chosen"], branch_panel.x + 200, branch_panel.y + 38,
                      GOLD, 16)
            draw_text(surface, "The other path is now closed to you.",
                      branch_panel.x + 14, branch_panel.y + 70, (100, 90, 120), 12)

        # Continue button
        cont = pygame.Rect(SCREEN_W//2-100, SCREEN_H-90, 200, 50)
        draw_button(surface, cont, "Continue", hover=cont.collidepoint(mx, my), size=16)
        self._lvlresult_cont = cont

        # ── Class transition milestone banner ────────────────────────
        trans = s.get("class_transitions", [])
        if trans:
            banner = pygame.Rect(SCREEN_W//2 - 320, 385, 660, 88)
            draw_panel(surface, banner, border_color=(220, 160, 60))
            draw_text(surface, "✦ ADVANCED CLASS AVAILABLE ✦",
                      banner.x + 14, banner.y + 10, (220, 160, 60), 15, bold=True)
            names = ", ".join(trans[:4]) + (" +" + str(len(trans)-4) + " more" if len(trans) > 4 else "")
            draw_text(surface, f"Eligible for: {names}",
                      banner.x + 14, banner.y + 34, GOLD, 13)
            draw_text(surface, "Visit the Guild → View Abilities to choose your Advanced Class.",
                      banner.x + 14, banner.y + 58, (180, 160, 100), 12)

    def _draw_classtree(self, surface, mx, my):
        """Full class progression viewer: timeline of abilities with locked/known state."""
        from core.abilities import CLASS_ABILITIES
        from core.progression import CLASS_TRANSITIONS, get_available_transitions
        from collections import defaultdict

        if not self.party:
            self.view = self.VIEW_INN
            return

        self.classtree_char_idx = max(0, min(self.classtree_char_idx, len(self.party)-1))
        c   = self.party[self.classtree_char_idx]
        cls = CLASSES.get(c.class_name, {})
        col = cls.get("color", CREAM)
        known = {a["name"] for a in c.abilities}

        # Header + tabs
        draw_text(surface, "Class Progression", 20, 12, GOLD, 22, bold=True)
        self._classtree_tab_rects = []
        self._classtree_back = pygame.Rect(SCREEN_W-130, 12, 110, 34)
        draw_button(surface, self._classtree_back, "Back",
                    hover=self._classtree_back.collidepoint(mx, my), size=13)

        tab_x = 20
        for i, ch in enumerate(self.party):
            tc = CLASSES.get(ch.class_name, {}).get("color", CREAM)
            tw = max(110, get_font(13).size(ch.name)[0]+36)
            tr = pygame.Rect(tab_x, 48, tw, 30)
            self._classtree_tab_rects.append(tr)
            sel = (i == self.classtree_char_idx)
            pygame.draw.rect(surface, (40,35,25) if sel else (20,18,14), tr, border_radius=4)
            pygame.draw.rect(surface, tc if sel else (50,45,35), tr, 2, border_radius=4)
            draw_class_badge(surface, ch.class_name, tr.x+4, tr.y+3, 11)
            draw_text(surface, ch.name, tr.x+30, tr.y+7, tc if sel else GREY, 13)
            tab_x += tw + 6

        # Class info
        draw_class_badge(surface, c.class_name, 20, 90, 18)
        draw_text(surface, f"{c.class_name}  Level {c.level}", 62, 93, col, 18, bold=True, max_width=SCREEN_W - 180)
        draw_text(surface, cls.get("description",""), 62, 118, GREY, 12, max_width=SCREEN_W - 180)

        # Timeline
        all_abs = CLASS_ABILITIES.get(c.class_name, [])
        by_level = defaultdict(list)
        for ab in all_abs:
            by_level[ab["level"]].append(ab)
        levels = sorted(by_level.keys())

        if not levels:
            draw_text(surface, "No ability data.", 60, 200, GREY, 14)
        else:
            TL_X = 60; TL_Y = 150; TL_W = SCREEN_W-100; TL_H = SCREEN_H-TL_Y-80
            COL_W = max(160, TL_W // max(1, len(levels)))
            pygame.draw.line(surface, (60,55,40), (TL_X, TL_Y+22), (TL_X+TL_W, TL_Y+22), 2)

            for ci, lv in enumerate(levels):
                cx = TL_X + ci*COL_W + COL_W//2
                reached = c.level >= lv
                dot_col = col if reached else (55,50,38)
                pygame.draw.circle(surface, dot_col, (cx, TL_Y+22), 7 if reached else 4)
                if reached:
                    pygame.draw.circle(surface, GOLD, (cx, TL_Y+22), 3)
                draw_text(surface, f"Lv{lv}", cx-18, TL_Y+4, col if reached else (70,62,48), 11, bold=reached)

                ay = TL_Y + 40
                for ab in by_level[lv]:
                    is_known = ab["name"] in known
                    is_next  = lv == c.level + 1
                    if is_known:   ab_bg, ab_bd, nc = (18,32,55), (55,100,190), (140,190,255)
                    elif is_next:  ab_bg, ab_bd, nc = (38,30,12), (170,140,55), (210,180,90)
                    else:          ab_bg, ab_bd, nc = (16,13,10), (38,33,26),   (70,63,50)

                    ar = pygame.Rect(cx-COL_W//2+4, ay, COL_W-8, 74)
                    if ay + ar.height > TL_Y + TL_H: break
                    pygame.draw.rect(surface, ab_bg, ar, border_radius=4)
                    pygame.draw.rect(surface, ab_bd, ar, 1, border_radius=4)
                    tick = "✓" if is_known else ">" if is_next else "·"
                    draw_text(surface, tick, ar.x+4, ar.y+4, ab_bd, 12)
                    draw_text(surface, ab["name"], ar.x+16, ar.y+4, nc, 12, bold=True)
                    draw_text(surface, f"{ab['cost']} {ab.get('resource','')}", ar.x+16, ar.y+20, (90,82,62), 10)
                    draw_wrapped_text(surface, ab.get("desc",""), ar.x+6, ar.y+36,
                                      ar.width-12, (100,93,75) if not is_known else (120,125,150), get_font(10))
                    ay += ar.height + 4

        # Transitions bar — show only classes reachable from current class
        ty = SCREEN_H - 68
        draw_text(surface, "Transitions:", 20, ty, DIM_GOLD, 12)
        tx = 130
        self._classtree_transition_rects = []
        for tn, req in CLASS_TRANSITIONS.items():
            if c.class_name not in req.get("base_classes", []):
                continue  # not reachable from current class
            can = tn in get_available_transitions(c)
            tc2 = PURPLE if can else (60,50,50)
            bg2 = (35,16,50) if can else (20,16,16)
            tr2 = pygame.Rect(tx, ty-3, get_font(12).size(tn)[0]+20, 24)
            pygame.draw.rect(surface, bg2, tr2, border_radius=3)
            pygame.draw.rect(surface, tc2, tr2, 1, border_radius=3)
            draw_text(surface, tn, tr2.x+8, tr2.y+4, tc2, 11)
            _req_lv = req.get("min_level", 10)
            draw_text(surface, f"Lv{_req_lv}+", tr2.x+4, tr2.y-13, (72,66,50), 10)
            if can:
                draw_text(surface, "CLICK", tr2.x+4, tr2.y+tr2.height+2, (90,160,120), 9)
            self._classtree_transition_rects.append((tr2, tn, can))
            tx += tr2.width + 6

    # ──────────────────────────────────────────────────────────────────────────
    #  CLASS CHOOSE — Advanced class selection screen
    # ──────────────────────────────────────────────────────────────────────────

    def _draw_class_choose(self, surface, mx, my):
        """Full-screen advanced class selection. Shows eligible classes as rich
        cards with lore, stat requirements, and ability preview. Clicking a card
        expands it; a second click (or confirm button) commits the transition."""
        import pygame
        from core.progression import CLASS_TRANSITIONS, get_available_transitions
        from core.abilities import CLASS_ABILITIES
        from core.classes import CLASSES

        # Safety: always clear stale NPC portrait rect so guild clicks can't bleed through
        self._bld_npc_portrait_rect = None

        if not self.party:
            self.view = self.VIEW_GUILD
            return

        self._tc_char_idx = max(0, min(self._tc_char_idx, len(self.party)-1))
        c   = self.party[self._tc_char_idx]
        cls = CLASSES.get(c.class_name, {})
        char_col = cls.get("color", CREAM)

        available = get_available_transitions(c)  # class names the char qualifies for now
        all_possible = [(tn, req) for tn, req in CLASS_TRANSITIONS.items()
                        if c.class_name in req.get("base_classes", [])]  # reachable from current class

        # ── Background ────────────────────────────────────────────────────────
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((6, 4, 12, 220))
        surface.blit(overlay, (0, 0))

        # ── Header ────────────────────────────────────────────────────────────
        draw_text(surface, "Choose Your Advanced Class", SCREEN_W//2 - 240, 14,
                  GOLD, 26, bold=True)

        # Character context line
        draw_class_badge(surface, c.class_name, 20, 18, 16)
        draw_text(surface, f"{c.name}  —  {c.class_name}  Lv.{c.level}",
                  52, 20, char_col, 15, bold=True, max_width=SCREEN_W // 2 - 60)

        # Guildmaster contextual remark
        dungeon_count = sum(1 for f in ("boss_defeated.goblin_warren",
                                        "boss_defeated.spiders_nest",
                                        "boss_defeated.abandoned_mine")
                            if __import__('core.story_flags',
                                         fromlist=['get_flag']).get_flag(f))
        if dungeon_count >= 3:
            gm_line = (f"The Guildmaster studies {c.name} carefully. "
                       f"\"Three trials behind you. Your {c.class_name} training is complete. "
                       f"What you become next is your choice — and it cannot be undone.\"")
        elif dungeon_count >= 1:
            gm_line = (f"The Guildmaster looks {c.name} over. "
                       f"\"You've proven yourself in the field. "
                       f"The paths below are open to you. Choose carefully.\"")
        else:
            gm_line = (f"The Guildmaster nods at {c.name}. "
                       f"\"Your training has reached its limit as a {c.class_name}. "
                       f"The paths ahead will define what you become.\"")
        draw_wrapped_text(surface, gm_line, 20, 46, SCREEN_W - 40,
                          (160, 150, 110), get_font(12))

        # ── Character tabs ────────────────────────────────────────────────────
        self._tc_tab_rects = []
        tab_x = 20
        for i, ch in enumerate(self.party):
            from core.progression import get_available_transitions as _gat
            ch_cls  = CLASSES.get(ch.class_name, {})
            ch_col  = ch_cls.get("color", CREAM)
            tw      = max(120, get_font(12).size(ch.name)[0] + 50)
            tr      = pygame.Rect(tab_x, 72, tw, 28)
            self._tc_tab_rects.append((tr, i))
            sel     = (i == self._tc_char_idx)
            has_any = bool(_gat(ch))
            bg      = (30, 25, 15) if sel else (16, 14, 10)
            border  = ch_col if sel else ((160, 120, 40) if has_any else (40, 36, 28))
            pygame.draw.rect(surface, bg, tr, border_radius=3)
            pygame.draw.rect(surface, border, tr, 2 if sel else 1, border_radius=3)
            draw_class_badge(surface, ch.class_name, tr.x + 3, tr.y + 2, 11)
            name_col = ch_col if sel else (CREAM if has_any else GREY)
            draw_text(surface, ch.name, tr.x + 22, tr.y + 4, name_col, 11,
                      bold=sel, max_width=tw - 36)
            if has_any and not sel:
                draw_text(surface, "✦", tr.right - 14, tr.y + 4,
                          (200, 150, 40), 11)
            tab_x += tw + 6

        # ── Card grid ─────────────────────────────────────────────────────────
        GRID_TOP   = 100
        GRID_BOT   = SCREEN_H - 60  # leave room for back button

        n_cards    = max(1, len(all_possible))
        # 4 columns so 15 classes fit in 4 rows (4×4=16 slots) within screen height
        COLS       = min(4, n_cards)
        CARD_GAP   = 10
        CARD_W     = (SCREEN_W - 40 - CARD_GAP * (COLS - 1)) // COLS
        CARD_H_BASE= 140   # collapsed height
        GRID_X     = 20

        self._tc_card_rects   = []
        self._tc_confirm_rect = None
        self._tc_close_rect   = None
        self._tc_back_rect    = pygame.Rect(SCREEN_W - 140, SCREEN_H - 48, 120, 36)

        draw_button(surface, self._tc_back_rect, "Back",
                    hover=self._tc_back_rect.collidepoint(mx, my), size=13)

        # ── Pre-compute all card rects (needed for hit-testing) ───────────────
        card_data = []
        for idx, (tn, req) in enumerate(all_possible):
            col_i    = idx % COLS
            row_i    = idx // COLS
            cx       = GRID_X + col_i * (CARD_W + CARD_GAP)
            cy       = GRID_TOP + row_i * (CARD_H_BASE + CARD_GAP)
            can      = tn in available
            selected = (self._tc_selected == tn)
            card_h   = CARD_H_BASE + 180 if selected else CARD_H_BASE
            if cy + card_h > GRID_BOT - 4:
                card_h = max(CARD_H_BASE, GRID_BOT - cy - 4)
            card_r   = pygame.Rect(cx, cy, CARD_W, card_h)
            self._tc_card_rects.append((card_r, tn, can))
            card_data.append(dict(tn=tn, req=req, can=can,
                                  selected=selected, card_r=card_r,
                                  card_h=card_h))

        # ── Helper: draw one card ─────────────────────────────────────────────
        def _draw_card(d):
            tn       = d['tn']
            req      = d['req']
            can      = d['can']
            selected = d['selected']
            card_r   = d['card_r']
            card_h   = d['card_h']
            tc_data  = CLASSES.get(tn, {})
            tc_col   = tc_data.get("color", CREAM)

            # Background + border
            if selected and can:
                bg_col = (22, 35, 20);  bd_col = (80, 200, 120)
            elif can:
                bg_col = (20, 18, 28);  bd_col = tc_col
            else:
                bg_col = (14, 12, 14);  bd_col = (40, 36, 36)
            pygame.draw.rect(surface, bg_col, card_r, border_radius=6)
            pygame.draw.rect(surface, bd_col, card_r,
                             2 if not selected else 3, border_radius=6)

            # ── Close (X) button — top-right of card, only when expanded ─────
            if selected and can:
                close_r = pygame.Rect(card_r.right - 28, card_r.y + 8, 22, 22)
                self._tc_close_rect = close_r
                chov = close_r.collidepoint(mx, my)
                pygame.draw.rect(surface,
                                 (70, 20, 20) if chov else (40, 14, 14),
                                 close_r, border_radius=4)
                pygame.draw.rect(surface,
                                 (200, 80, 80) if chov else (120, 50, 50),
                                 close_r, 1, border_radius=4)
                draw_text(surface, "X", close_r.x + 5, close_r.y + 3,
                          (220, 100, 100) if chov else (160, 70, 70), 11, bold=True)

            # Class badge + name
            badge_x = card_r.x + 10
            badge_y = card_r.y + 10
            name_mw = (CARD_W - 70) if selected else (CARD_W - 24)
            draw_class_badge(surface, tn, badge_x, badge_y, 20)
            # Tier from actual min_level
            min_level = req.get("min_level", 10)
            if min_level >= 15:
                tier_label = "Apex"
                tier_col   = (220, 160, 80)
            else:
                tier_label = "Hybrid"
                tier_col   = (140, 180, 220)
            name_col   = tc_col if can else (60, 54, 50)
            draw_text(surface, tn, badge_x + 28, badge_y + 2,
                      name_col, 17, bold=True, max_width=name_mw)
            draw_text(surface, f"{tier_label}  ·  Level {min_level}+",
                      badge_x + 28, badge_y + 22, tier_col, 11)

            # Stat requirements
            req_y = card_r.y + 56
            for stat, minimum in req.get("min_stats", {}).items():
                actual = c.stats.get(stat, 0)
                met    = actual >= minimum
                draw_text(surface,
                          f"{'✓' if met else '✗'} {stat} {minimum}  ({actual})",
                          card_r.x + 10, req_y,
                          (80, 200, 100) if met else (200, 80, 80), 11)
                req_y += 16

            # Thematic description
            desc = req.get("description", tc_data.get("description", ""))
            draw_wrapped_text(surface, desc,
                              card_r.x + 10, req_y + 4, CARD_W - 20,
                              (140, 130, 100) if can else (70, 64, 58),
                              get_font(11))

            # ── Expanded section ──────────────────────────────────────────────
            if selected and can:
                exp_y = card_r.y + CARD_H_BASE + 4
                draw_text(surface, "Abilities you'll gain access to:",
                          card_r.x + 10, exp_y, (100, 180, 120), 11, bold=True)
                exp_y += 18
                class_abs = CLASS_ABILITIES.get(tn, [])[:6]
                if class_abs:
                    for ab in class_abs:
                        ab_str = f"  {ab['name']}  ({ab['cost']} {ab.get('resource','')})"
                        draw_text(surface, ab_str,
                                  card_r.x + 10, exp_y, (120, 160, 200), 11,
                                  max_width=CARD_W - 20)
                        exp_y += 14
                        if exp_y + 14 > card_r.bottom - 44:
                            remaining = len(class_abs) - class_abs.index(ab) - 1
                            if remaining > 0:
                                draw_text(surface,
                                          f"  + {remaining} more abilities...",
                                          card_r.x + 10, exp_y, (80, 100, 80), 10)
                            break
                else:
                    draw_text(surface,
                              "  (abilities unlocked at the Guild after transition)",
                              card_r.x + 10, exp_y, (80, 90, 80), 10)

                # Confirm button
                confirm_r = pygame.Rect(card_r.x + 10, card_r.bottom - 38,
                                        CARD_W - 20, 32)
                self._tc_confirm_rect = (confirm_r, tn)
                c_hover = confirm_r.collidepoint(mx, my)
                pygame.draw.rect(surface,
                                 (20, 60, 30) if c_hover else (14, 40, 20),
                                 confirm_r, border_radius=5)
                pygame.draw.rect(surface,
                                 (80, 200, 120) if c_hover else (50, 140, 80),
                                 confirm_r, 2, border_radius=5)
                draw_text(surface, f"Become {tn}  —  This cannot be undone",
                          confirm_r.x + 10, confirm_r.y + 8,
                          (140, 230, 150) if c_hover else (100, 180, 110), 12,
                          bold=c_hover)

            # Locked overlay
            if not can:
                lock_surf = pygame.Surface((CARD_W, CARD_H_BASE), pygame.SRCALPHA)
                lock_surf.fill((0, 0, 0, 100))
                surface.blit(lock_surf, (card_r.x, card_r.y))
                blocking = [(s, m) for s, m in req.get("min_stats", {}).items()
                            if c.stats.get(s, 0) < m]
                if blocking:
                    stat, need = blocking[0]
                    draw_text(surface,
                              f"Requires {stat} {need}  (have {c.stats.get(stat,0)})",
                              card_r.x + 10, card_r.y + card_h - 24,
                              (160, 80, 80), 11)
                else:
                    draw_text(surface, f"Requires Level {req.get('min_level', 10)}+",
                              card_r.x + 10, card_r.y + card_h - 24,
                              (140, 80, 60), 11)

        # ── Pass 1: draw all NON-selected cards ───────────────────────────────
        for d in card_data:
            if not d['selected']:
                _draw_card(d)

        # ── Pass 2: draw selected card LAST so it sits on top ─────────────────
        for d in card_data:
            if d['selected'] and d['can']:
                _draw_card(d)
    def _do_class_transition(self, char_idx, class_name):
        """Execute the class transition and show confirmation."""
        import core.sound as sfx
        from core.progression import apply_class_transition
        c = self.party[char_idx]
        success, msg = apply_class_transition(c, class_name)
        if success:
            sfx.play("quest_complete")
            self._msg(msg, (160, 220, 180))
            self._tc_selected  = None
            self._tc_confirmed = True
            self.view = self.VIEW_GUILD
        else:
            self._msg(msg, RED)

    def _rest_at_inn(self, tier_key, total_cost=None):
        """Process inn rest for the party. total_cost includes room + training."""
        from core.progression import INN_TIERS, can_level_up
        from core.classes import get_all_resources

        tier = INN_TIERS[tier_key]
        party_size = len(self.party)

        if total_cost is None:
            total_cost = tier["cost_per_char"] * party_size

        total_gold = sum(c.gold for c in self.party)
        if total_gold < total_cost:
            return False

        # Deduct total gold (room + training) evenly across party
        if total_cost > 0:
            remaining = total_cost
            for c in self.party:
                deduct = min(c.gold, remaining)
                c.gold -= deduct
                remaining -= deduct
                if remaining <= 0:
                    break

        # Restore resources
        for c in self.party:
            _eff = c.effective_stats() if hasattr(c, "effective_stats") else c.stats
            max_res = get_all_resources(c.class_name, _eff, c.level)
            for res_name, max_val in max_res.items():
                current = c.resources.get(res_name, 0)
                if res_name == "HP":
                    restore = tier["hp_restore"]
                elif "MP" in res_name or res_name == "Ki":
                    restore = tier["mp_restore"]
                else:
                    restore = tier["sp_restore"]
                gain = int(max_val * restore)
                c.resources[res_name] = min(max_val, current + gain)

        # Clear resurrection sickness
        for c in self.party:
            if hasattr(c, 'status_effects'):
                c.status_effects = [s for s in c.status_effects
                                    if s.get("type") != "resurrection_sickness"]

        # Check for level ups
        if tier["allows_level_up"]:
            self.levelup_queue = [c for c in self.party if can_level_up(c)]
            self.levelup_current = 0
            self.levelup_free_stat = None
        else:
            self.levelup_queue = []

        cost_str = f"{total_cost}g" if total_cost > 0 else "free"
        restore_str = f"{int(tier['hp_restore']*100)}%"
        self.inn_result = f"Rested at {tier['name']} ({cost_str}). Restored {restore_str} HP/MP/SP. Progress saved."

        return True

    # ─────────────────────────────────────────────────────────
    #  TAVERN
    # ─────────────────────────────────────────────────────────

    def _get_tavern_recruits(self):
        """Return cached recruit list, regenerating if party level has shifted."""
        from core.tavern_recruits import generate_recruits, avg_party_level
        current_avg = avg_party_level(self.party)
        if (self._tavern_recruits is None
                or abs(current_avg - self._tavern_recruits_at_level) >= 2):
            self._tavern_recruits = generate_recruits(self.party, self.town_id)
            self._tavern_recruits_at_level = current_avg
        return self._tavern_recruits

    def _draw_tavern(self, surface, mx, my):
        from data.shop_inventory import TAVERN, get_tavern_patrons
        from core.story_flags import get_flag

        self._bld_npc_portrait_rect = None   # no portrait card in tavern
        self._draw_building_interior(surface, "tavern")
        PW = int(SCREEN_W * 0.42)   # usable left-panel width
        H  = SCREEN_H

        draw_text(surface, TAVERN["name"], 24, 28, GOLD, 22, bold=True)

        # ── Tab bar ───────────────────────────────────────────────────────────
        tabs = [("patrons", "Patrons"), ("recruit", "Adventurers"), ("party", "My Party")]
        tx = 16
        self._tavern_tab_rects = []
        for key, label in tabs:
            tw2 = get_font(13).size(label)[0] + 24
            tr = pygame.Rect(tx, 62, tw2, 28)
            active = (self.tavern_tab == key)
            bg = (50, 40, 20) if active else (25, 18, 10)
            border = GOLD if active else PANEL_BORDER
            pygame.draw.rect(surface, bg, tr, border_radius=4)
            pygame.draw.rect(surface, border, tr, 1, border_radius=4)
            draw_text(surface, label, tr.x + 12, tr.y + 6,
                      GOLD if active else GREY, 13)
            self._tavern_tab_rects.append((key, tr))
            tx += tw2 + 8

        PW = int(SCREEN_W * 0.42)
        back = pygame.Rect(8, SCREEN_H - 140, 120, 34)
        draw_button(surface, back, "← Leave", hover=back.collidepoint(mx, my), size=13,
                    bg=(50,35,70), border=(120,90,160), color=(220,200,255))
        self._back_btn = back

        # ── PATRONS tab ───────────────────────────────────────────────────────
        if self.tavern_tab == "patrons":
            patrons = [p for p in get_tavern_patrons(self.town_id)
                       if not (p.get("hide_if") and get_flag(p["hide_if"]))]
            drink_cost = TAVERN.get("drink_cost", 2)

            # Left: patron list
            list_w = min(240, PW // 2 - 16)
            list_panel = pygame.Rect(12, 98, list_w, H - 200)
            draw_panel(surface, list_panel, bg_color=(18, 12, 8))
            draw_text(surface, "At the bar:", list_panel.x + 10, list_panel.y + 8, DIM_GOLD, 11)

            self._patron_rects = []
            for i, p in enumerate(patrons):
                py2 = list_panel.y + 28 + i * 54
                row = pygame.Rect(list_panel.x + 6, py2, list_panel.width - 12, 48)
                sel = (self.tavern_selected == i)
                bg2 = (40, 30, 12) if sel else (25, 18, 8)
                pygame.draw.rect(surface, bg2, row, border_radius=3)
                if sel:
                    pygame.draw.rect(surface, GOLD, row, 1, border_radius=3)
                pygame.draw.circle(surface, p["color"], (row.x + 16, row.y + 18), 10)
                pygame.draw.circle(surface, tuple(max(0,c-40) for c in p["color"]),
                                   (row.x + 16, row.y + 18), 10, 1)
                drinks = self.tavern_drinks.get(p["name"], 0)
                name_col = p["color"] if drinks > 0 else CREAM
                draw_text(surface, p["name"], row.x + 32, row.y + 6, name_col, 12, bold=True)
                tier_txt = f"loosened up" if drinks > 0 else "Sober"
                draw_text(surface, tier_txt, row.x + 32, row.y + 24, DIM_GOLD if drinks else GREY, 10)
                self._patron_rects.append((i, row))

            # Rumor below patron list
            rumor_y = list_panel.y + 28 + len(patrons) * 54 + 10
            rumor_panel = pygame.Rect(list_panel.x, rumor_y, list_panel.width, H - rumor_y - 100)
            if rumor_panel.height > 30:
                draw_panel(surface, rumor_panel, bg_color=(14, 10, 18))
                draw_text(surface, "Overheard:", rumor_panel.x + 10, rumor_panel.y + 8, RUMOR_COL, 10, bold=True)
                rumor_text = self.current_rumor or "Ask around — buy someone a drink."
                draw_text(surface, f'"{rumor_text}"',
                          rumor_panel.x + 10, rumor_panel.y + 24,
                          (200, 185, 230), 10, max_width=rumor_panel.width - 20)
                hear_btn = pygame.Rect(rumor_panel.x + 10, H - 110, rumor_panel.width - 20, 28)
                draw_button(surface, hear_btn, "Hear another (1g)",
                            hover=hear_btn.collidepoint(mx, my), size=10)
                self._tavern_hear_btn = hear_btn

            # Right: dialogue panel (within left panel)
            dlg_x = list_panel.right + 12
            dlg_panel = pygame.Rect(dlg_x, 98, PW - dlg_x - 8, H - 200)
            draw_panel(surface, dlg_panel, bg_color=(20, 14, 8))

            if 0 <= self.tavern_selected < len(patrons):
                p = patrons[self.tavern_selected]
                drinks = self.tavern_drinks.get(p["name"], 0)
                nc = p["color"]
                pygame.draw.circle(surface, nc, (dlg_panel.x + 36, dlg_panel.y + 40), 26)
                pygame.draw.circle(surface, tuple(max(0,c-50) for c in nc),
                                   (dlg_panel.x + 36, dlg_panel.y + 40), 26, 2)
                draw_text(surface, p["name"], dlg_panel.x + 72, dlg_panel.y + 18, nc, 16, bold=True)
                draw_text(surface, p.get("role","patron").capitalize(),
                          dlg_panel.x + 72, dlg_panel.y + 38, GREY, 11)
                lines2 = p["drunk"] if drinks > 0 else p["sober"]
                import random
                q_idx = hash((p["name"], drinks)) % len(lines2)
                quote = lines2[q_idx]
                draw_text(surface, f'"{quote}"',
                          dlg_panel.x + 16, dlg_panel.y + 80, CREAM, 13,
                          max_width=dlg_panel.width - 32)
                total_gold = sum(c.gold for c in self.party)
                can_afford = total_gold >= drink_cost
                drink_btn = pygame.Rect(dlg_panel.x + 16, H - 190, 200, 38)
                draw_button(surface, drink_btn, f"Buy a drink ({drink_cost}g)",
                            hover=drink_btn.collidepoint(mx, my) and can_afford, size=13)
                self._tavern_drink_btn = drink_btn
                self._tavern_drink_patron = p["name"]
                hint = "Buy them a drink to loosen their tongue." if drinks == 0 else "Another drink might reveal more..."
                draw_text(surface, hint, dlg_panel.x + 16, H - 142, DIM_GOLD, 11)
            else:
                self._tavern_drink_btn = None
                self._tavern_hear_btn = None

        # ── ADVENTURERS tab ───────────────────────────────────────────────────
        elif self.tavern_tab == "recruit":
            recruits = self._get_tavern_recruits()
            draw_text(surface, "Adventurers seeking work:", 16, 100, DIM_GOLD, 13)
            self._recruit_rects = []
            card_w = (PW - 40) // 2
            for i, rec in enumerate(recruits):
                cx2 = 16 + (i % 2) * (card_w + 8)
                ry = 124 + (i // 2) * 175
                panel = pygame.Rect(cx2, ry, card_w, 162)
                sel = (self.tavern_recruit_sel == i)
                draw_panel(surface, panel, bg_color=(35, 28, 12) if sel else (22, 16, 8))
                if sel:
                    pygame.draw.rect(surface, GOLD, panel, 1, border_radius=4)
                rc = rec["color"]
                pygame.draw.circle(surface, rc, (panel.x + 18, panel.y + 20), 14)
                draw_text(surface, rec["name"], panel.x + 38, panel.y + 8, rc, 13, bold=True, max_width=card_w - 44)
                draw_text(surface, f"{rec['race_name']} {rec['class_name']} — Lv.{rec['level']}",
                          panel.x + 38, panel.y + 26, GREY, 10)
                draw_text(surface, f'"{rec["pitch"]}"',
                          panel.x + 10, panel.y + 48, CREAM, 10, max_width=card_w - 20)
                stat_y = panel.y + 84
                for si, (sn, sv) in enumerate(rec["stats"].items()):
                    sx2 = panel.x + 8 + si * 46
                    draw_text(surface, sn, sx2, stat_y, GREY, 9)
                    draw_text(surface, str(sv), sx2, stat_y + 12, CREAM, 10, bold=True)
                party_full = len(self.party) >= 6
                already_in = any(c.name == rec["name"] for c in self.party)
                if already_in:
                    draw_text(surface, "In party", panel.x + 10, panel.y + 136, DIM_GOLD, 11)
                elif party_full:
                    draw_text(surface, "Party full", panel.x + 10, panel.y + 136, GREY, 11)
                else:
                    rbtn = pygame.Rect(panel.x + 10, panel.y + 132, 110, 24)
                    draw_button(surface, rbtn, "Recruit", hover=rbtn.collidepoint(mx, my), size=11)
                    self._recruit_rects.append((i, rbtn, rec))

        # ── MY PARTY tab ──────────────────────────────────────────────────────
        elif self.tavern_tab == "party":
            draw_text(surface, "Leave a member here (they wait safely):", 16, 100, DIM_GOLD, 13)
            draw_text(surface, "You must keep at least 1 member.", 16, 118, GREY, 11)
            self._leave_rects = []
            card_w = (PW - 40) // 3
            for i, char in enumerate(self.party):
                px3 = 16 + (i % 3) * (card_w + 8)
                py3 = 140 + (i // 3) * 155
                panel = pygame.Rect(px3, py3, card_w, 140)
                draw_panel(surface, panel, bg_color=(22, 16, 8))
                cc = getattr(char, "_walk_color", (180, 160, 120))
                pygame.draw.circle(surface, cc, (panel.x + 18, panel.y + 20), 13)
                draw_text(surface, char.name, panel.x + 38, panel.y + 8, CREAM, 13, bold=True, max_width=card_w - 44)
                draw_text(surface, f"Lv.{char.level} {getattr(char,'class_name','?')}",
                          panel.x + 38, panel.y + 26, GREY, 11)
                draw_text(surface, f"HP: {char.resources.get('HP',0)}", panel.x + 10, panel.y + 50, CREAM, 11)
                draw_text(surface, f"Gold: {char.gold}g", panel.x + 10, panel.y + 66, DIM_GOLD, 11)
                if len(self.party) > 1:
                    lbtn = pygame.Rect(panel.x + 10, panel.y + 106, 110, 24)
                    draw_button(surface, lbtn, "Leave here",
                                hover=lbtn.collidepoint(mx, my), size=11)
                    self._leave_rects.append((i, lbtn))

        self._tavern_back_btn = back
        self._draw_party_bar(surface, mx, my)



        # ─────────────────────────────────────────────────────────
    #  JOB BOARD
    # ─────────────────────────────────────────────────────────

    def _draw_jobboard(self, surface, mx, my):
        from data.job_board import get_town_jobs, check_job_ready, get_job_progress, JOBS
        self._draw_building_interior(surface, "jobboard")
        PW = int(SCREEN_W * 0.42)   # usable left-panel width

        draw_text(surface, "Job Board", 20, 28, GOLD, 22, bold=True)
        draw_text(surface, "Available contracts in the area.", 20, 58, GREY, 13)

        back = pygame.Rect(8, SCREEN_H - 140, 120, 34)
        draw_button(surface, back, "← Back", hover=back.collidepoint(mx, my), size=13,
                    bg=(50,35,70), border=(120,90,160), color=(220,200,255))
        self._back_btn = back
        jobs = get_town_jobs(self.town_id)
        if not jobs:
            draw_text(surface, "No jobs posted.", 20, 140, GREY, 16)
            self._draw_party_bar(surface, mx, my)
            return

        y = 92
        self._job_buttons = []
        panel_w = PW - 28
        for job_id, job, state in jobs:
            panel = pygame.Rect(14, y, panel_w, 76)
            draw_panel(surface, panel, bg_color=(25, 20, 35))

            type_col = {"bounty": (200, 100, 100), "fetch": (100, 180, 100),
                        "explore": (100, 140, 220)}.get(job["type"], GREY)
            tag = job["type"].upper()
            level_req = job.get("level_req", 1)
            draw_text(surface, f"[{tag}]", panel.x + 10, panel.y + 7, type_col, 11)
            draw_text(surface, job["name"], panel.x + 76, panel.y + 5, CREAM, 15, bold=True,
                      max_width=panel_w - 200)
            draw_text(surface, f"Lv.{level_req}+",
                      panel.x + panel_w - 160, panel.y + 7, (160, 140, 100), 11)
            draw_text(surface, f"Reward: {job['reward_gold']}g, {job['reward_xp']} XP",
                      panel.x + 10, panel.y + 28, DIM_GOLD, 12)
            desc = job["description"]
            if len(desc) > 72:
                desc = desc[:69] + "..."
            draw_text(surface, desc, panel.x + 10, panel.y + 48, GREY, 11,
                      max_width=panel_w - 150)

            btn_x = panel.x + panel_w - 128
            btn_w = 118
            if state == 0:
                party_level = max((c.level for c in self.party), default=1)
                too_low = party_level < level_req
                btn = pygame.Rect(btn_x, panel.y + 24, btn_w, 28)
                if too_low:
                    pygame.draw.rect(surface, (15, 12, 22), panel, border_radius=4)
                    draw_text(surface, f"Requires Lv.{level_req}", btn_x, panel.y + 30, (130, 100, 100), 12)
                else:
                    draw_button(surface, btn, "Accept", hover=btn.collidepoint(mx, my), size=12)
                    self._job_buttons.append((btn, "accept", job_id))
            elif state == 1:
                progress = get_job_progress(job_id)
                required = job.get("required", 0)
                ready = check_job_ready(job_id, self.party)
                if job["type"] == "bounty":
                    prog_text = f"{min(progress, required)}/{required} killed"
                elif job["type"] == "fetch":
                    count = sum(item.get("stack", 1)
                                for c in self.party for item in c.inventory
                                if item.get("name") == job.get("item_name"))
                    prog_text = f"{min(count, required)}/{required} collected"
                else:
                    prog_text = "Complete!" if ready else "In progress..."
                prog_col = (100, 220, 100) if ready else (220, 180, 80)
                draw_text(surface, prog_text, btn_x, panel.y + 14, prog_col, 12)
                if ready:
                    btn = pygame.Rect(btn_x, panel.y + 38, btn_w, 28)
                    draw_button(surface, btn, "Turn In",
                                hover=btn.collidepoint(mx, my), size=12)
                    self._job_buttons.append((btn, "turnin", job_id))
            elif state == -2:
                draw_text(surface, "COMPLETED", btn_x + 10, panel.y + 30,
                          (80, 180, 80), 13, bold=True)

            y += 84

        self._draw_party_bar(surface, mx, my)

    # ─────────────────────────────────────────────────────────
    #  CLICK HANDLING
    # ─────────────────────────────────────────────────────────

    def handle_click(self, mx, my):
        """Returns 'exit' to leave town, or None."""

        # Dialogue takes priority — handle and return immediately so other
        # click targets don't process on the same mouse event.
        if self.active_dialogue and not self.active_dialogue.finished:
            result = self.active_dialogue.handle_click(mx, my)
            if self.active_dialogue.finished:
                self.active_dialogue = None
                try:
                    from core.story_flags import auto_advance_quests
                    done = auto_advance_quests(self.party)
                    self.pending_quest_completions.extend(done)
                except Exception:
                    pass
            return None  # consume the click regardless

        # ── Indoor NPC portrait click (service views that draw the header) ──
        _NO_PORTRAIT_VIEWS = {
            self.VIEW_WALK, self.VIEW_HUB, self.VIEW_TAVERN,
            self.VIEW_JOBBOARD, self.VIEW_INN_LEVELUP,
        }
        if (self._bld_npc_portrait_rect and
                self._bld_npc_portrait_rect.collidepoint(mx, my) and
                self.view not in _NO_PORTRAIT_VIEWS):
            self._open_indoor_npc_dialogue()
            return None

        # ── Hub view ──
        if self.view == self.VIEW_HUB:
            # Menu button (top-right)
            menu_r = pygame.Rect(SCREEN_W - 160, 20, 140, 38)
            if menu_r.collidepoint(mx, my):
                return "show_menu"

            panel_w = int(SCREEN_W * 0.42)
            PAD   = 28
            BTN_W = panel_w - PAD * 2
            btn_h = 64
            gap   = 8
            locations = [loc[0] for loc in self._get_town_locations()]
            by = 116
            for i, loc_key in enumerate(locations):
                btn = pygame.Rect(PAD, by + i * (btn_h + gap), BTN_W, btn_h)
                if btn.collidepoint(mx, my):
                    if loc_key == "exit":
                        self.finished = True
                        return "exit"
                    elif loc_key == "shop":
                        self._enter_building_from_hub("shop")
                        self.view = self.VIEW_SHOP
                    elif loc_key == "forge":
                        self._enter_building_from_hub("forge")
                        self.view = self.VIEW_FORGE
                        self.forge_scroll = 0
                    elif loc_key == "temple":
                        self._enter_building_from_hub("temple")
                        self.view = self.VIEW_TEMPLE
                    elif loc_key == "tavern":
                        self._enter_building_from_hub("tavern")
                        from data.story_data import get_rumor
                        self.current_rumor = get_rumor()
                        self.view = self.VIEW_TAVERN
                    elif loc_key == "inn":
                        self._enter_building_from_hub("inn")
                        self.view = self.VIEW_INN
                    elif loc_key == "jobboard":
                        self._enter_building_from_hub("jobboard")
                        self.view = self.VIEW_JOBBOARD
                    elif loc_key == "guild":
                        self._enter_building_from_hub("guild")
                        self._enter_guild(BUILDING_NPCS.get(self.town_id, {}).get("guild", {}))
                    elif loc_key == "party":
                        return "open_party_review"
                    return None

            # NPC clicks — now on the right side of the scene
            from data.story_data import get_town_npcs, NPC_DIALOGUES
            from core.dialogue import select_dialogue
            from core._dialogue_party import set_party
            set_party(self.party)
            npcs = get_town_npcs(self.town_id)
            npc_x = panel_w + 30
            for j, (npc_id, npc_data) in enumerate(npcs):
                nr = pygame.Rect(npc_x, 168 + j * 62, 210, 54)
                if nr.collidepoint(mx, my):
                    sfx.play("npc_talk")
                    dialogues = NPC_DIALOGUES.get(npc_id, [])
                    if dialogues:
                        from ui.dialogue_ui import DialogueUI
                        ds = select_dialogue(npc_id, dialogues)
                        if ds:
                            self.active_dialogue = DialogueUI(ds)
                    return None

        # ── Shop menu ──
        elif self.view == self.VIEW_SHOP:
            options = ["buy", "sell", "back"]
            for i, opt in enumerate(options):
                btn = pygame.Rect(SCREEN_W // 2 - 200, 148 + i * 90, 400, 75)
                if btn.collidepoint(mx, my):
                    if opt == "buy":
                        self.view = self.VIEW_SHOP_BUY
                        self.shop_scroll = 0
                    elif opt == "sell":
                        self.view = self.VIEW_SHOP_SELL
                        self.sell_scroll = 0
                    elif opt == "back":
                        self._return_to_town()
                    return None

        # ── Shop buy ──
        elif self.view == self.VIEW_SHOP_BUY:
            # Back button
            back = pygame.Rect(8, SCREEN_H - 140, 120, 34)
            if back.collidepoint(mx, my):
                self.view = self.VIEW_SHOP
                return None

            # Character tabs (6a) — matches draw y=50
            n = len(self.party)
            tab_w = min(180, (SCREEN_W - 170) // max(n, 1))
            for i in range(n):
                tr = pygame.Rect(20 + i * (tab_w + 4), 50, tab_w, 32)
                if tr.collidepoint(mx, my):
                    self.shop_char_idx = i
                    self.shop_scroll = 0
                    return None

            # Category tabs — matches draw y=95
            tabs = ["weapons", "armor", "consumables"]
            for i, key in enumerate(tabs):
                tr = pygame.Rect(20 + i * 140, 95, 130, 28)
                if tr.collidepoint(mx, my):
                    self.shop_tab = key
                    self.shop_scroll = 0
                    return None

            # Item clicks — matches draw panel y=132, row h=68
            is_equip_tab = self.shop_tab in ("weapons", "armor")
            list_w = SCREEN_W - 40 - (244 if is_equip_tab else 0)
            items = list(self.shop.get(self.shop_tab, []))
            buyback_start = len(items)
            items.extend(self.sold_items)
            panel = pygame.Rect(20, 132, list_w, SCREEN_H - 237)
            iy = panel.y + 8
            start = self.shop_scroll
            end = min(len(items), start + 7)
            for idx in range(start, end):
                row = pygame.Rect(panel.x + 6, iy, panel.width - 12, 64)
                if row.collidepoint(mx, my):
                    is_buyback = idx >= buyback_start
                    if is_buyback:
                        self._buy_back_item(idx - buyback_start)
                    else:
                        self._buy_item(items[idx])
                    return None
                iy += 68

        # ── Shop sell ──
        elif self.view == self.VIEW_SHOP_SELL:
            back = pygame.Rect(8, SCREEN_H - 140, 120, 34)
            if back.collidepoint(mx, my):
                self.view = self.VIEW_SHOP
                return None

            # Character tabs — matches draw y=140
            for i in range(len(self.party)):
                tab_area_w = SCREEN_W - 170
                tw = tab_area_w // len(self.party)
                tr = pygame.Rect(20 + i * tw, 140, tw - 4, 32)
                if tr.collidepoint(mx, my):
                    self.sell_char = i
                    self.sell_scroll = 0
                    return None

            # Item clicks — matches draw panel y=182
            char = self.party[self.sell_char]
            panel = pygame.Rect(20, 182, SCREEN_W - 40, SCREEN_H - 287)
            iy = panel.y + 10
            start = self.sell_scroll
            end = min(len(char.inventory), start + 8)
            for idx in range(start, end):
                row = pygame.Rect(panel.x + 8, iy, panel.width - 16, 68)
                if row.collidepoint(mx, my):
                    self._sell_item(char, idx)
                    return None
                iy += 72

        # ── Temple ──
        elif self.view == self.VIEW_TEMPLE:
            back = pygame.Rect(8, SCREEN_H - 140, 120, 34)
            if back.collidepoint(mx, my):
                self._return_to_town()
                return None

            # Service buttons
            # by must match _draw_temple: starts at 120, bumps to 132 for PIE>=15
            services = list(TEMPLE["services"].keys())
            by = 120
            max_pie = max((c.stats.get("PIE", 0) for c in self.party), default=0)
            if max_pie >= 15:
                by = 132  # matches _draw_temple PIE discount banner bump
            for i, svc_key in enumerate(services):
                btn = pygame.Rect(SCREEN_W // 2 - 250, by + i * 80, 500, 68)
                if btn.collidepoint(mx, my):
                    self._use_temple_service(svc_key)
                    return None

            # Identify item clicks
            # uy must match _draw_temple: by + len(services)*80 + 20 (+25 for label)
            svc_count = len(services)
            unid_items = []
            for ci, c in enumerate(self.party):
                for ii, item in enumerate(c.inventory):
                    from core.identification import needs_identification
                    if needs_identification(item):
                        unid_items.append((ci, ii, item, c))

            if unid_items:
                uy = by + svc_count * 80 + 20 + 25  # +20 header gap, +25 label height
                for ui_idx, (ci, ii, item, char) in enumerate(unid_items[:5]):
                    row = pygame.Rect(SCREEN_W // 2 - 250, uy, 500, 40)
                    if row.collidepoint(mx, my):
                        self._temple_identify(ci, ii, item, char)
                        return None
                    uy += 44

        # ── Inn ──
        elif self.view == self.VIEW_INN:
            from core.progression import INN_TIERS, INN_TIER_ORDER

            back = pygame.Rect(8, SCREEN_H - 140, 120, 34)
            if back.collidepoint(mx, my):
                self._return_to_town()
                self.inn_result = None
                return None

            # Save button
            save_btn = pygame.Rect(SCREEN_W - 280, 20, 128, 34)
            if save_btn.collidepoint(mx, my):
                from core.save_load import save_game
                ok, path, msg = save_game(self.party)
                self._inn_save_msg = msg
                self._inn_save_ok  = ok
                self._inn_save_timer = 3000
                return None

            # Party management button
            party_btn = pygame.Rect(SCREEN_W - 420, 20, 130, 34)
            if party_btn.collidepoint(mx, my):
                return "open_party_review"

            # Character sheet button
            sheet_btn = pygame.Rect(SCREEN_W - 570, 20, 140, 34)
            if sheet_btn.collidepoint(mx, my):
                self.charsheet_idx = 0
                self.view = self.VIEW_INN_CHARSHEET
                return None

            by = 148
            for i, tier_key in enumerate(INN_TIER_ORDER):
                btn = pygame.Rect(SCREEN_W // 2 - 280, by + i * 95, 560, 85)
                if btn.collidepoint(mx, my):
                    from core.progression import can_level_up, training_cost
                    tier = INN_TIERS[tier_key]
                    room_cost = tier["cost_per_char"] * len(self.party)
                    total_cost = room_cost
                    total_gold = sum(c.gold for c in self.party)
                    if total_gold >= total_cost:
                        success = self._rest_at_inn(tier_key, total_cost)
                        if success and self.levelup_queue:
                            self.view = self.VIEW_INN_LEVELUP
                        return "inn_save"  # signal to main.py to auto-save
                    else:
                        self._msg(f"Not enough gold! Need {total_cost}g.", RED)
                    return None

        # ── Inn Trainer ──
        elif self.view == self.VIEW_INN_TRAINER:
            from core.abilities import get_unlearned_abilities, learn_ability

            back = pygame.Rect(8, SCREEN_H - 140, 120, 34)
            if back.collidepoint(mx, my):
                if getattr(self, "_trainer_origin", "inn") == "guild":
                    self._trainer_origin = "inn"
                    self.view = self.VIEW_GUILD
                else:
                    self.view = self.VIEW_INN
                return None

            # Character tabs (match draw: tab_area_w = SCREEN_W - 170)
            tab_area_w = SCREEN_W - 170
            tw = tab_area_w // len(self.party)
            for i, c in enumerate(self.party):
                tr = pygame.Rect(20 + i * tw, 108, tw - 4, 28)
                if tr.collidepoint(mx, my):
                    self.trainer_char_idx = i
                    self.trainer_scroll = 0
                    return None

            char = self.party[self.trainer_char_idx]

            # Learn button clicks
            for _row, btn, ab, cost, can_afford in getattr(self, "_trainer_rects", []):
                if btn.collidepoint(mx, my):
                    if not can_afford:
                        self._msg(f"Need {cost}g to learn {ab['name']}.", RED)
                        return None
                    learned = learn_ability(char, ab["name"])
                    if learned:
                        remaining = cost
                        for pc in self.party:
                            take = min(pc.gold, remaining)
                            pc.gold -= take
                            remaining -= take
                            if remaining <= 0:
                                break
                        sfx.play("quest_complete")
                        self._msg(f"{char.name} learned {ab['name']}!  (-{cost}g)", GOLD)
                        self.trainer_scroll = 0
                    else:
                        self._msg(f"{char.name} already knows {ab['name']}.", GREY)
                    return None

        # ── Inn Character Sheet ──
        elif self.view == self.VIEW_INN_CHARSHEET:
            n = len(self.party)

            back = pygame.Rect(8, SCREEN_H - 140, 120, 34)
            if back.collidepoint(mx, my):
                self.view = self.VIEW_INN
                return None

            if n > 1:
                larr = pygame.Rect(10, SCREEN_H // 2 - 22, 34, 44)
                rarr = pygame.Rect(SCREEN_W - 44, SCREEN_H // 2 - 22, 34, 44)
                if larr.collidepoint(mx, my):
                    self.charsheet_idx = (self.charsheet_idx - 1) % n
                    return None
                if rarr.collidepoint(mx, my):
                    self.charsheet_idx = (self.charsheet_idx + 1) % n
                    return None

        # ── Inn Level Up ──
        elif self.view == self.VIEW_INN_LEVELUP:
            from core.progression import apply_level_up, training_cost, can_level_up
            from core.classes import STAT_NAMES, get_all_resources

            if not self.levelup_queue:
                self.view = self.VIEW_INN
                return None

            c = self.levelup_queue[self.levelup_current]

            # Stat selection buttons (left panel, 60px rows starting at y=118)
            left_panel_x = 30
            for i, stat in enumerate(STAT_NAMES):
                btn = pygame.Rect(left_panel_x, 118 + i * 60, 290, 52)
                if btn.collidepoint(mx, my):
                    self.levelup_free_stat = stat
                    return None

            # Train button
            cost = training_cost(c.level + 1)
            party_gold = sum(cc.gold for cc in self.party)
            can_train = self.levelup_free_stat is not None and party_gold >= cost
            confirm = pygame.Rect(20, 516, 200, 46)
            if confirm.collidepoint(mx, my) and can_train:
                summary = apply_level_up(c, self.levelup_free_stat)
                if summary:
                    max_res = get_all_resources(c.class_name, c.stats, c.level)
                    for rn, mv in max_res.items():
                        if c.resources.get(rn, 0) > mv:
                            c.resources[rn] = mv
                    # Store for fanfare screen
                    summary["char_name"]   = c.name
                    summary["class_name"]  = c.class_name
                    summary["stats_after"] = dict(c.stats)
                    # Flag L10/L15 class transition milestone
                    from core.progression import get_available_transitions
                    available_trans = get_available_transitions(c)
                    summary["class_transitions"] = available_trans
                    self.levelup_summary   = summary
                    gains = ", ".join(f"+{v} {k}" for k, v in summary["stat_gains"].items())
                    ab_str = (" New to train: " + ", ".join(summary["new_abilities"])
                              if summary.get("new_abilities") else "")
                    self.inn_result = (f"{c.name} reached level {c.level}! "
                                      f"{gains}, +{summary['hp_gain']} base HP{ab_str}")
                    if available_trans:
                        self.inn_result += f" ✦ Class transition available at the Guild!"
                    sfx.play("level_up")


                self.levelup_current += 1
                self.levelup_free_stat = None
                # Go to fanfare before next character
                self.view = self.VIEW_INN_LEVELUP_RESULT
                return None

            # Skip button
            skip = pygame.Rect(240, 516, 130, 46)
            if skip.collidepoint(mx, my):
                self.levelup_current += 1
                self.levelup_free_stat = None
                if self.levelup_current >= len(self.levelup_queue):
                    self.view = self.VIEW_INN
                return None

            # Full tree button
            tree_btn = pygame.Rect(390, 516, 200, 46)
            if tree_btn.collidepoint(mx, my):
                # Find this char's index in party for the tree viewer
                idx = next((i for i, ch in enumerate(self.party)
                            if ch is c), 0)
                self.classtree_char_idx = idx
                self.view = self.VIEW_CLASSTREE
                return None

        elif self.view == self.VIEW_INN_LEVELUP_RESULT:
            # Continue button → next character or back to inn
            cont = pygame.Rect(SCREEN_W // 2 - 100, SCREEN_H - 90, 200, 50)
            if cont.collidepoint(mx, my):
                self.levelup_summary = None
                if self.levelup_current >= len(self.levelup_queue):
                    self.view = self.VIEW_INN
                else:
                    self.view = self.VIEW_INN_LEVELUP
                return None

        elif self.view == self.VIEW_BRANCH_CHOICE:
            from core.abilities import choose_branch
            c    = self.branch_pending_char
            opts = self.branch_pending_opts
            if not c or not opts:
                if getattr(self, "_guild_branch_origin", False):
                    self._guild_branch_origin = False
                    self.view = self.VIEW_GUILD
                else:
                    self.view = self.VIEW_INN_LEVELUP_RESULT
                return None

            CARD_W   = SCREEN_W // 2 - 40
            CARD_TOP = 90
            CARD_H   = SCREEN_H - 200

            for idx, opt in enumerate(opts):
                cx  = 20 + idx * (SCREEN_W // 2)
                btn = pygame.Rect(cx + 20, CARD_TOP + CARD_H - 62, CARD_W - 40, 48)
                if btn.collidepoint(mx, my):
                    choose_branch(c, opt)
                    label = opt.get("branch_label", opt["name"])
                    if self.levelup_summary:
                        self.levelup_summary["branch_chosen"] = opt["name"]
                        self.levelup_summary["branch_label"]  = label
                    self.branch_pending_char = None
                    self.branch_pending_opts = None
                    # Return to guild hub if that's where we came from
                    if getattr(self, "_guild_branch_origin", False):
                        self._guild_branch_origin = False
                        sfx.play("quest_accept")
                        self._msg(f"{c.name} chose: {label}", (200, 170, 255))
                        self.view = self.VIEW_GUILD
                    else:
                        self.view = self.VIEW_INN_LEVELUP_RESULT
                    return None

        elif self.view == self.VIEW_CLASSTREE:
            # Back button
            back_btn = pygame.Rect(SCREEN_W - 130, 12, 110, 34)
            if back_btn.collidepoint(mx, my):
                # Return to guild if entered from there
                if getattr(self, "_guild_classtree_origin", False):
                    self._guild_classtree_origin = False
                    self.view = self.VIEW_GUILD
                # Return to wherever we came from in the inn flow
                elif self.levelup_queue and self.levelup_current < len(self.levelup_queue):
                    self.view = self.VIEW_INN_LEVELUP
                else:
                    self.view = self.VIEW_INN
                return None
            # Character tabs
            tab_x = 20
            for i, ch in enumerate(self.party):
                tw = max(110, get_font(13).size(ch.name)[0] + 36)
                tr = pygame.Rect(tab_x, 48, tw, 30)
                if tr.collidepoint(mx, my):
                    self.classtree_char_idx = i
                    return None
                tab_x += tw + 6
            # Transition buttons → open full class-choose screen
            for tr2, class_name, can in getattr(self, "_classtree_transition_rects", []):
                if tr2.collidepoint(mx, my) and can:
                    c = self.party[self.classtree_char_idx]
                    self._tc_char_idx  = self.classtree_char_idx
                    self._tc_selected  = None
                    self._tc_confirmed = False
                    self._tc_card_rects = []
                    self._bld_npc_portrait_rect = None  # prevent guild NPC click bleed-through
                    self.view = self.VIEW_CLASS_CHOOSE
                    return None

        # ── Class Choose ──────────────────────────────────────────────────────
        elif self.view == self.VIEW_CLASS_CHOOSE:
            # Back button
            back_r = pygame.Rect(SCREEN_W - 140, SCREEN_H - 48, 120, 36)
            if back_r.collidepoint(mx, my):
                self._tc_selected = None
                self.view = self.VIEW_CLASSTREE
                return None

            # Character tabs
            for tr, tab_idx in getattr(self, "_tc_tab_rects", []):
                if tr.collidepoint(mx, my):
                    self._tc_char_idx = tab_idx
                    self._tc_selected = None
                    return None

            # ── If a card is expanded, it gets FIRST right of refusal ─────────
            # Any click within the expanded card's full rect is consumed here
            # before checking cards below/behind it.
            selected_card_rect = None
            for card_r, cls_name, can in getattr(self, "_tc_card_rects", []):
                if cls_name == self._tc_selected and can:
                    selected_card_rect = (card_r, cls_name)
                    break

            if selected_card_rect is not None:
                card_r, cls_name = selected_card_rect
                if card_r.collidepoint(mx, my):
                    # Close (X) button
                    close_r = getattr(self, "_tc_close_rect", None)
                    if close_r and close_r.collidepoint(mx, my):
                        self._tc_selected = None
                        return None
                    # Confirm button
                    confirm_info = getattr(self, "_tc_confirm_rect", None)
                    if confirm_info:
                        confirm_r, conf_cls = confirm_info
                        if confirm_r.collidepoint(mx, my):
                            self._do_class_transition(self._tc_char_idx, conf_cls)
                            return None
                    # Clicking anywhere else inside the expanded card
                    # collapses it (same-card toggle) — does NOT fall through
                    self._tc_selected = None
                    return None

            # ── No expanded card owns this click — normal card selection ───────
            for card_r, cls_name, can in getattr(self, "_tc_card_rects", []):
                if card_r.collidepoint(mx, my) and can:
                    self._tc_selected = cls_name
                    return None

        # ── Tavern ──
        elif self.view == self.VIEW_TAVERN:
            from data.shop_inventory import TAVERN
            from core.story_flags import get_flag
            # Tavern has no NPC portrait card — clear so stale rect from a
            # previously visited building doesn't intercept clicks here.
            self._bld_npc_portrait_rect = None

            # Tab switches
            for key, tr in getattr(self, '_tavern_tab_rects', []):
                if tr.collidepoint(mx, my):
                    self.tavern_tab = key
                    return None

            # Back
            if getattr(self, '_tavern_back_btn', None) and self._tavern_back_btn.collidepoint(mx, my):
                self._return_to_town()
                return None

            # ── PATRONS tab ───────────────────────────────────────────────────
            if self.tavern_tab == "patrons":
                for i, row in getattr(self, '_patron_rects', []):
                    if row.collidepoint(mx, my):
                        self.tavern_selected = i
                        return None

                drink_btn = getattr(self, '_tavern_drink_btn', None)
                patron_name = getattr(self, '_tavern_drink_patron', None)
                if drink_btn and patron_name and drink_btn.collidepoint(mx, my):
                    drink_cost = TAVERN.get("drink_cost", 2)
                    total_gold = sum(c.gold for c in self.party)
                    if total_gold >= drink_cost:
                        # Deduct gold
                        remaining = drink_cost
                        for c in self.party:
                            if c.gold >= remaining:
                                c.gold -= remaining
                                remaining = 0
                                break
                            elif c.gold > 0:
                                remaining -= c.gold
                                c.gold = 0
                        self.tavern_drinks[patron_name] = self.tavern_drinks.get(patron_name, 0) + 1
                        sfx.play("ui_confirm")
                        self._msg(f"You buy {patron_name} a drink. They seem more talkative.", RUMOR_COL)
                    else:
                        self._msg(f"You can't afford a drink! (need {drink_cost}g)", RED)

                # "Hear another" rumor button (costs 1g)
                hear_btn = getattr(self, '_tavern_hear_btn', None)
                if hear_btn and hear_btn.collidepoint(mx, my):
                    total_gold = sum(c.gold for c in self.party)
                    if total_gold >= 1:
                        remaining = 1
                        for c in self.party:
                            if c.gold >= remaining:
                                c.gold -= remaining; remaining = 0; break
                            elif c.gold > 0:
                                remaining -= c.gold; c.gold = 0
                        from data.story_data import get_rumor
                        self.current_rumor = get_rumor()
                        sfx.play("ui_confirm")
                        self._msg("You lean in and listen...", RUMOR_COL)
                    else:
                        self._msg("You need at least 1g to buy into the conversation.", RED)
                    return None

            # ── RECRUIT tab ───────────────────────────────────────────────────
            elif self.tavern_tab == "recruit":
                for i, rbtn, rec in getattr(self, '_recruit_rects', []):
                    if rbtn.collidepoint(mx, my):
                        if len(self.party) >= 6:
                            self._msg("Party is full! Leave someone at the tavern first.", RED)
                        else:
                            from core.character import Character
                            # Use pre-rolled Character if available (dynamic recruits)
                            if "_char" in rec and rec["_char"] is not None:
                                new_char = rec["_char"]
                                # Ensure HP is set
                                if not new_char.resources.get("HP"):
                                    new_char.resources["HP"] = new_char.resources.get("MAX_HP", 20)
                            else:
                                # Fallback: build from stat dict (legacy static recruits)
                                new_char = Character(name=rec["name"],
                                                     class_name=rec["class_name"],
                                                     race_name=rec["race_name"])
                                new_char.level = rec["level"]
                                for stat, val in rec["stats"].items():
                                    new_char.stats[stat] = val
                                from core.classes import get_all_resources
                                new_char.resources = get_all_resources(
                                    new_char.class_name, new_char.stats, new_char.level
                                )
                                new_char.gold = 0
                            self.party.append(new_char)
                            # Remove this recruit from the pool so they can't be hired twice
                            rec["_char"] = None
                            sfx.play("ui_confirm")
                            self._msg(f"{rec['name']} joins your party!", GOLD)
                        return None

            # ── PARTY tab ─────────────────────────────────────────────────────
            elif self.tavern_tab == "party":
                for i, lbtn in getattr(self, '_leave_rects', []):
                    if lbtn.collidepoint(mx, my):
                        if len(self.party) <= 1:
                            self._msg("You can't leave your last party member behind.", RED)
                        else:
                            left = self.party.pop(i)
                            sfx.play("ui_click")
                            self._msg(f"{left.name} waits at the tavern.", DIM_GOLD)
                        return None

        # ── Forge ──
        elif self.view in (self.VIEW_FORGE, self.VIEW_FORGE_CRAFT,
                           self.VIEW_FORGE_UPGRADE, self.VIEW_FORGE_ENCHANT,
                           self.VIEW_FORGE_REPAIR):
            return self._handle_forge_click(mx, my)

        # ── Guild Hub ──
        elif self.view == self.VIEW_GUILD:
            # Advance Rank button
            adv_btn = getattr(self, "_guild_advance_btn", None)
            if adv_btn and adv_btn.collidepoint(mx, my):
                self._do_guild_advance()
                return None

            # Back button
            back = getattr(self, "_guild_back_btn", None)
            if back and back.collidepoint(mx, my):
                self._return_to_town()
                return None

            for rect, action in getattr(self, "_guild_option_rects", []):
                if rect.collidepoint(mx, my):
                    if action == "jobboard":
                        self.view = self.VIEW_JOBBOARD
                    elif action == "train":
                        # Open the ability trainer shop (guild only)
                        self.trainer_char_idx = 0
                        self.trainer_scroll = 0
                        self._trainer_origin = "guild"
                        self.view = self.VIEW_INN_TRAINER
                    elif action == "classtree":
                        self.classtree_char_idx = 0
                        self._guild_classtree_origin = True
                        self.view = self.VIEW_CLASSTREE
                    elif action == "class_choose":
                        # Open class-choose for the first eligible character
                        from core.progression import get_available_transitions
                        for i, ch in enumerate(self.party):
                            if get_available_transitions(ch):
                                self._tc_char_idx  = i
                                self._tc_selected  = None
                                self._tc_confirmed = False
                                self._tc_card_rects = []
                                self.classtree_char_idx = i
                                self._bld_npc_portrait_rect = None  # prevent click bleed-through
                                self.view = self.VIEW_CLASS_CHOOSE
                                break
                    return None

        # ── Job Board ──
        elif self.view == self.VIEW_JOBBOARD:
            PW = int(SCREEN_W * 0.42)
            back = pygame.Rect(8, SCREEN_H - 140, 120, 34)
            if back.collidepoint(mx, my):
                self._return_to_town()
                return None

            from data.job_board import accept_job, complete_job
            for btn, action, job_id in getattr(self, '_job_buttons', []):
                if btn.collidepoint(mx, my):
                    if action == "accept":
                        accept_job(job_id)
                        sfx.play("quest_accept")
                        self._msg("Job accepted!", (100, 220, 100))
                    elif action == "turnin":
                        reward = complete_job(job_id, self.party)
                        if reward:
                            sfx.play("quest_complete")
                            self._msg(f"Job complete! +{reward['gold']}g, +{reward['xp']} XP",
                                      GOLD)
                    return None

        return None

    # ─────────────────────────────────────────────────────────
    #  ACTIONS
    # ─────────────────────────────────────────────────────────

    def _buy_item(self, shop_item):
        """Buy an item. Gold deducted from the selected character (6d).
        If they can't afford it but another party member can, show a hint."""
        price = shop_item.get("buy_price", 0)
        idx   = min(self.shop_char_idx, len(self.party) - 1) if self.party else 0
        sel   = self.party[idx] if self.party else None

        if not sel:
            return

        if sel.gold < price:
            # Check if another character could afford it
            if any(c.gold >= price for c in self.party):
                self._msg("Switch to a character who can afford this.", (200, 150, 60))
            else:
                self._msg("Not enough gold!", RED)
            return

        sel.gold -= price

        new_item = dict(shop_item)
        new_item.pop("buy_price", None)
        new_item.pop("sell_price", None)
        new_item["identified"] = True
        from core.party_knowledge import mark_item_identified
        mark_item_identified(new_item.get("name", ""))
        sel.inventory.append(new_item)

        self._msg(f"Bought {shop_item['name']} for {price}g — added to {sel.name}'s inventory", BUY_COL)
        sfx.play("shop_buy")

    def _buy_back_item(self, sold_idx):
        """Buy back a previously sold item. Uses selected character's gold."""
        if sold_idx >= len(self.sold_items):
            return
        item  = self.sold_items[sold_idx]
        price = item.get("buy_price", 0)
        idx   = min(self.shop_char_idx, len(self.party) - 1) if self.party else 0
        sel   = self.party[idx] if self.party else None

        if not sel:
            return

        if sel.gold < price:
            if any(c.gold >= price for c in self.party):
                self._msg("Switch to a character who can afford this.", (200, 150, 60))
            else:
                self._msg("Not enough gold!", RED)
            return

        sel.gold -= price
        self.sold_items.pop(sold_idx)

        new_item = dict(item)
        new_item.pop("buy_price", None)
        new_item.pop("sell_price", None)
        new_item.pop("_buyback", None)
        sel.add_item(new_item)

        name = get_item_display_name(new_item)
        self._msg(f"Bought back {name} for {price}g — added to {sel.name}'s inventory", BUY_COL)

    def _sell_item(self, char, item_idx):
        """Sell an item from a character's inventory."""
        if item_idx >= len(char.inventory):
            return
        item = char.inventory[item_idx]
        # Key items, quest items, and Warden badges cannot be sold
        if (item.get("quest_item") or
                item.get("type") in ("quest_item", "key_item") or
                "warden_rank" in item):
            self._msg(f"{item.get('name', 'This item')} cannot be sold — it is a key item.", (220, 80, 80))
            return
        sell_price = get_sell_price(item)
        char.inventory.pop(item_idx)
        char.gold += sell_price
        name = get_item_display_name(item)
        # Add to buyback list — buyback at sell price (same as what player received)
        buyback = dict(item)
        buyback["buy_price"] = sell_price
        buyback["_buyback"] = True
        self.sold_items.append(buyback)
        self._msg(f"Sold {name} for {sell_price}g", SELL_COL)
        sfx.play("shop_sell")

    def _draw_forge_repair(self, surface, mx, my, y, total_gold, accent):
        """Draw the forge repair tab — list damaged equipment and repair buttons."""
        from core.durability import (
            has_durability, get_durability_state, get_durability_color,
            get_durability_label, get_repair_cost, repair_item, init_durability
        )

        GREY = (120, 110, 100)
        RED  = (220, 60, 60)
        draw_text(surface, "Repair damaged equipment:", 20, y, accent, 14, bold=True)
        draw_text(surface, "(Repairs all durability for a fixed gold cost)", 20, y + 18, GREY, 11)
        y += 40

        found_any = False
        btn_w, btn_h = 120, 30
        row_h = 52

        for ci, char in enumerate(self.party):
            for slot, item in list((char.equipment or {}).items()):
                if not item or not has_durability(item):
                    continue
                init_durability(item)
                state = get_durability_state(item)
                if state == "full":
                    continue
                found_any = True
                cost = get_repair_cost(item)
                can_afford = total_gold >= cost
                dur_col = get_durability_color(item)
                dur_lbl = get_durability_label(item)

                row = pygame.Rect(20, y, SCREEN_W - 180, row_h)
                pygame.draw.rect(surface, (22, 18, 35), row, border_radius=3)
                pygame.draw.rect(surface, accent, row, 1, border_radius=3)

                draw_text(surface, item.get("name", "?"), row.x + 10, row.y + 6, CREAM, 14, bold=True)
                draw_text(surface, f"{char.name} — {slot}", row.x + 10, row.y + 26, GREY, 11)
                draw_text(surface, f"Durability: {dur_lbl}", row.x + 320, row.y + 6, dur_col, 13)
                draw_text(surface, state.upper(), row.x + 320, row.y + 26, dur_col, 11)

                btn_col = accent if can_afford else RED
                btn = pygame.Rect(SCREEN_W - 150, y + 8, btn_w, btn_h)
                pygame.draw.rect(surface, (40, 30, 15) if can_afford else (35, 15, 15), btn, border_radius=3)
                pygame.draw.rect(surface, btn_col, btn, 1, border_radius=3)
                lbl = f"Repair {cost}g" if can_afford else f"Need {cost}g"
                draw_text(surface, lbl, btn.x + 8, btn.y + 7, btn_col, 12)

                y += row_h + 6

        if not found_any:
            draw_text(surface, "All equipment is in good condition.", 20, y, (100, 200, 100), 14)

        # ── Focus weapon recharge section ────────────────────────────
        from core.focus_charges import is_focus, init_charges, crystals_needed, get_charge_label, CRYSTAL_NAME
        from core.crafting import count_material
        y += 30
        found_focus = False
        for char in self.party:
            eq = char.equipment or {}
            for slot, item in eq.items():
                if not item or not is_focus(item):
                    continue
                init_charges(item)
                cur = item.get("charges", 0)
                mx_c = item.get("max_charges", 20)
                if cur >= mx_c:
                    continue
                found_focus = True
                needed = crystals_needed(item)
                have   = count_material(self.party, CRYSTAL_NAME)
                can_rch = have >= needed > 0
                lbl_col = (120, 200, 255) if can_rch else GREY
                row = pygame.Rect(20, y, SCREEN_W - 180, 48)
                pygame.draw.rect(surface, (18, 22, 38), row, border_radius=3)
                pygame.draw.rect(surface, (80, 120, 200), row, 1, border_radius=3)
                draw_text(surface, item.get("name","?"), row.x + 10, row.y + 5, CREAM, 13, bold=True)
                draw_text(surface, f"{char.name} — {slot}", row.x + 10, row.y + 24, GREY, 11)
                draw_text(surface, get_charge_label(item).strip("()"),
                          row.x + 320, row.y + 5, lbl_col, 13)
                draw_text(surface, f"Need {needed} Mana Crystal{'s' if needed>1 else ''} (have {have})",
                          row.x + 320, row.y + 24, lbl_col, 11)
                btn_col = (80, 160, 255) if can_rch else (60, 60, 80)
                btn = pygame.Rect(SCREEN_W - 150, y + 9, 120, 30)
                pygame.draw.rect(surface, (12, 20, 40) if can_rch else (20, 20, 30), btn, border_radius=3)
                pygame.draw.rect(surface, btn_col, btn, 1, border_radius=3)
                lbl = "Recharge" if can_rch else "No Crystals"
                draw_text(surface, lbl, btn.x + 10, btn.y + 7, btn_col, 12)
                y += 54
        if not found_focus:
            pass  # no depleted focus weapons — nothing to show

    def _pie_disposition_discount(self, base_price: int) -> tuple:
        """Apply PIE-based temple/holy NPC discount.
        High-PIE parties are shown favour by divine servants.
        Returns (discounted_price, pct_off) where pct_off is 0 if no discount."""
        max_pie = max((c.stats.get("PIE", 0) for c in self.party), default=0)
        if max_pie < 15:
            return base_price, 0
        # +2% discount per PIE above 14, capped at 20%
        pct = min(20, (max_pie - 14) * 2)
        discounted = max(1, int(base_price * (1.0 - pct / 100)))
        return discounted, pct

    def _use_temple_service(self, service_key):
        """Use a temple service."""
        svc = TEMPLE["services"][service_key]
        base_cost = svc["cost"]
        cost, pct_off = self._pie_disposition_discount(base_cost)
        total_gold = sum(c.gold for c in self.party)

        if service_key == "cure_poison":
            # Find first poisoned character
            from core.status_effects import get_status_effects, remove_all_poison
            for c in self.party:
                effects = get_status_effects(c)
                if any(s.get("type") == "poison" for s in effects):
                    if total_gold < cost:
                        self._msg(f"Not enough gold! Need {cost}g.", RED)
                        return
                    self._deduct_gold(cost)
                    remove_all_poison(c)
                    self._msg(f"{c.name}'s poison has been purged! ({cost}g)", HEAL_COL)
                    return
            self._msg("No one in your party is poisoned.", GREY)

        elif service_key == "cure_disease":
            from core.status_effects import get_status_effects, remove_all_disease
            for c in self.party:
                effects = get_status_effects(c)
                if any(s.get("type") == "disease" for s in effects):
                    if total_gold < cost:
                        self._msg(f"Not enough gold! Need {cost}g.", RED)
                        return
                    self._deduct_gold(cost)
                    remove_all_disease(c)
                    self._msg(f"{c.name}'s disease has been cleansed! ({cost}g)", HEAL_COL)
                    return
            self._msg("No one in your party is diseased.", GREY)

        elif service_key == "remove_curse":
            from core.status_effects import get_status_effects, remove_all_curses
            # Check for cursed status effects OR cursed equipped items
            for c in self.party:
                effects = get_status_effects(c)
                has_curse_effect = any(s.get("type") == "curse" for s in effects)
                cursed_slots = [
                    slot for slot, item in (c.equipment or {}).items()
                    if item and item.get("cursed") and not item.get("curse_lifted")
                ]
                if has_curse_effect or cursed_slots:
                    if total_gold < cost:
                        self._msg(f"Not enough gold! Need {cost}g.", RED)
                        return
                    self._deduct_gold(cost)
                    if has_curse_effect:
                        remove_all_curses(c)
                    # Lift all cursed equipment — mark as removable and unequip
                    for slot in cursed_slots:
                        item = c.equipment[slot]
                        item["curse_lifted"] = True
                        c.equipment[slot] = None
                        c.inventory.append(item)
                    msg = f"{c.name}'s curses have been lifted! ({cost}g)"
                    if cursed_slots:
                        names = ", ".join(c.equipment.get(s, {}).get("name", s) or s for s in cursed_slots)
                        msg = f"{c.name} freed from cursed gear! ({cost}g)"
                    self._msg(msg, HEAL_COL)
                    return
            self._msg("No one in your party is cursed.", GREY)

        elif service_key == "resurrect":
            # Find first dead character (HP <= 0 and marked dead)
            # For now, resurrect any character at 0 HP
            for c in self.party:
                if c.resources.get("HP", 0) <= 0:
                    actual_cost = 200 + 100 * c.level
                    if total_gold < actual_cost:
                        self._msg(f"Not enough gold! Need {actual_cost}g to resurrect {c.name}.", RED)
                        return
                    self._deduct_gold(actual_cost)
                    c.resources["HP"] = 1
                    from core.status_effects import add_resurrection_sickness, remove_all_poison
                    remove_all_poison(c)  # resurrection clears poison
                    add_resurrection_sickness(c)
                    # 1% chance of 5% max HP loss
                    import random
                    if random.random() < 0.01:
                        from core.classes import get_all_resources
                        max_res = get_all_resources(c.class_name, c.stats, c.level)
                        max_hp = max_res.get("HP", 100)
                        loss = max(1, int(max_hp * 0.05))
                        self._msg(f"{c.name} resurrected but weakened! (-{loss} max HP permanently) ({actual_cost}g)", ORANGE)
                    else:
                        self._msg(f"{c.name} has been resurrected! ({actual_cost}g) Rest at the inn to recover.", HEAL_COL)
                    return
            self._msg("No fallen party members to resurrect.", GREY)

        elif service_key == "identify_item":
            self._msg("Click an unidentified item below to identify it (15g each).", DIM_GOLD)

        elif service_key == "blessing":
            if total_gold < cost:
                self._msg(f"Not enough gold! Need {cost}g.", RED)
                return
            self._deduct_gold(cost)
            self._msg("The priests bless your party. May the Light guide your path! (+5% accuracy)", HEAL_COL)

    def _temple_identify(self, char_idx, item_idx, item, char):
        """Identify an item at the temple for gold."""
        cost = 15
        total_gold = sum(c.gold for c in self.party)
        if total_gold < cost:
            self._msg("Not enough gold to identify! Need 15g.", RED)
            return

        self._deduct_gold(cost)
        item["identified"] = True
        item["magic_identified"] = True
        item["material_identified"] = True
        name = get_item_display_name(item)
        # Register in party knowledge
        from core.party_knowledge import mark_item_identified
        mark_item_identified(name)
        self._msg(f"Identified: {name} (15g)", HEAL_COL)

    def _deduct_gold(self, amount):
        """Deduct gold across party members."""
        remaining = amount
        for c in self.party:
            if remaining <= 0:
                break
            take = min(c.gold, remaining)
            c.gold -= take
            remaining -= take

    def _msg(self, text, color=CREAM):
        self.message = text
        self.msg_color = color
        self.msg_timer = 3000

    # ─────────────────────────────────────────────────────────
    #  SCROLL
    # ─────────────────────────────────────────────────────────

    def handle_scroll(self, direction):
        if self.view == self.VIEW_SHOP_BUY:
            items = list(self.shop.get(self.shop_tab, [])) + self.sold_items
            max_s = max(0, len(items) - 7)
            if direction > 0:
                self.shop_scroll = min(max_s, self.shop_scroll + 1)
            else:
                self.shop_scroll = max(0, self.shop_scroll - 1)
        elif self.view == self.VIEW_SHOP_SELL:
            char = self.party[self.sell_char]
            max_s = max(0, len(char.inventory) - 8)
            if direction > 0:
                self.sell_scroll = min(max_s, self.sell_scroll + 1)
            else:
                self.sell_scroll = max(0, self.sell_scroll - 1)
        elif self.view in (self.VIEW_FORGE_CRAFT, self.VIEW_FORGE_UPGRADE,
                           self.VIEW_FORGE_ENCHANT):
            if direction > 0:
                self.forge_scroll = min(self.forge_scroll + 1, 50)
            else:
                self.forge_scroll = max(0, self.forge_scroll - 1)

    # ─────────────────────────────────────────────────────────
    #  FORGE — Craft, Upgrade, Enchant
    # ─────────────────────────────────────────────────────────

    def _draw_forge(self, surface, mx, my):
        from core.crafting import (
            RECIPES, ENCHANTMENTS, UPGRADE_COSTS, MAX_UPGRADE,
            can_afford_recipe, count_material, get_upgrade_level,
            get_upgrade_cost, get_upgradeable_items, get_enchantable_items,
            get_applicable_enchants, get_materials_of_tier,
        )

        FORGE_ORANGE = (255, 140, 40)
        FORGE_DIM = (160, 100, 40)

        bld_name = self.current_bld_name or "The Forge"
        self._draw_bld_npc_header(surface, bld_name, "", mx, my, building_type="forge")
        total_gold = sum(c.gold for c in self.party)
        draw_text(surface, f"Gold: {total_gold}", SCREEN_W - 150, 20, DIM_GOLD, 14)

        # Tab bar — below NPC portrait card (card bottom ~134px)
        tabs = [("Craft", self.VIEW_FORGE_CRAFT),
                ("Upgrade", self.VIEW_FORGE_UPGRADE),
                ("Enchant", self.VIEW_FORGE_ENCHANT),
                ("Repair",  self.VIEW_FORGE_REPAIR)]
        for i, (label, view) in enumerate(tabs):
            tr = pygame.Rect(20 + i * 140, 140, 130, 32)
            active = self.view == view or (self.view == self.VIEW_FORGE and i == 0)
            col = FORGE_ORANGE if active else FORGE_DIM
            pygame.draw.rect(surface, col, tr, 0 if active else 1, 4)
            tc = BLACK if active else col
            draw_text(surface, label, tr.x + 35, tr.y + 7, tc, 15, bold=active)

        # Back button — aligned with tabs

        # Materials summary bar (below tabs)
        draw_text(surface, "Materials:", 20, 180, GREY, 12)
        mx_pos = 100
        shown_mats = {}
        for c in self.party:
            for item in c.inventory:
                if item.get("type") == "material":
                    n = item.get("name", "?")
                    shown_mats[n] = shown_mats.get(n, 0) + item.get("quantity", 1)
        for mat_name, count in list(shown_mats.items())[:8]:
            short = mat_name[:12]
            draw_text(surface, f"{short}×{count}", mx_pos, 180, CREAM, 11)
            mx_pos += 110

        active_view = self.view if self.view != self.VIEW_FORGE else self.VIEW_FORGE_CRAFT
        y = 200

        if active_view == self.VIEW_FORGE_CRAFT:
            self._draw_forge_craft(surface, mx, my, y, RECIPES, total_gold, FORGE_ORANGE)
        elif active_view == self.VIEW_FORGE_UPGRADE:
            self._draw_forge_upgrade(surface, mx, my, y, total_gold, FORGE_ORANGE)
        elif active_view == self.VIEW_FORGE_ENCHANT:
            self._draw_forge_enchant(surface, mx, my, y, total_gold, FORGE_ORANGE)
        elif active_view == self.VIEW_FORGE_REPAIR:
            self._draw_forge_repair(surface, mx, my, y, total_gold, FORGE_ORANGE)

    def _draw_forge_craft(self, surface, mx, my, y, recipes, total_gold, accent):
        from core.crafting import can_afford_recipe, count_material
        visible = recipes[self.forge_scroll:self.forge_scroll + 7]
        for i, recipe in enumerate(visible):
            ry = y + i * 76
            can = can_afford_recipe(self.party, recipe)
            box = pygame.Rect(20, ry, SCREEN_W - 40, 70)
            bc = (50, 40, 30) if can else (35, 30, 25)
            pygame.draw.rect(surface, bc, box, 0, 6)
            pygame.draw.rect(surface, accent if can else (60, 50, 40), box, 1, 6)

            # Item name and description
            res = recipe["result"]
            draw_text(surface, res["name"], 30, ry + 4, GOLD if can else GREY, 16, bold=True)
            desc = res.get("description", "")[:70]
            draw_text(surface, desc, 30, ry + 24, CREAM if can else (80, 70, 60), 12)

            # Cost — gold + per-material have/need with color coding
            total_gold = sum(c.gold for c in self.party)
            gold_col = (200, 180, 80) if total_gold >= recipe["gold"] else (220, 80, 80)
            cx = 30
            draw_text(surface, f"Cost: {recipe['gold']}g", cx, ry + 44, gold_col, 12, bold=True)
            cx += 90
            for mat, ct in recipe["materials"].items():
                have = count_material(self.party, mat)
                mat_col = (100, 220, 100) if have >= ct else (220, 100, 100)
                draw_text(surface, f"{mat}: {have}/{ct}", cx, ry + 44, mat_col, 12)
                cx += len(mat) * 7 + 70

            # Craft button
            if can:
                btn = pygame.Rect(SCREEN_W - 120, ry + 16, 80, 30)
                pygame.draw.rect(surface, accent, btn, 0, 4)
                draw_text(surface, "Craft", btn.x + 18, btn.y + 6, BLACK, 14, bold=True)

    def _draw_forge_upgrade(self, surface, mx, my, y, total_gold, accent):
        from core.crafting import get_upgradeable_items, get_upgrade_cost, get_materials_of_tier
        items = get_upgradeable_items(self.party)
        if not items:
            draw_text(surface, "No weapons or armor to upgrade.", 30, y + 20, GREY, 15)
            draw_text(surface, "Equip or carry weapons/armor to upgrade them here.", 30, y + 45, (80, 70, 60), 13)
            return

        visible = items[self.forge_scroll:self.forge_scroll + 7]
        for i, (char, idx, item, loc) in enumerate(visible):
            ry = y + i * 62
            cost = get_upgrade_cost(item)
            if not cost:
                continue
            avail_mats = get_materials_of_tier(self.party, cost["min_material_tier"])
            total_mats = sum(avail_mats.values())
            can = total_gold >= cost["gold"] and total_mats >= cost["material_count"]

            box = pygame.Rect(20, ry, SCREEN_W - 40, 58)
            bc = (50, 40, 30) if can else (35, 30, 25)
            pygame.draw.rect(surface, bc, box, 0, 6)
            pygame.draw.rect(surface, accent if can else (60, 50, 40), box, 1, 6)

            lvl = item.get("upgrade_level", 0)
            draw_text(surface, f"{item['name']}", 30, ry + 4, GOLD if can else GREY, 15, bold=True)
            draw_text(surface, f"{char.name} ({loc})  |  +{lvl} → +{lvl+1}", 30, ry + 24, CREAM if can else (80,70,60), 12)
            gold_col2 = (200, 180, 80) if total_gold >= cost["gold"] else (220, 80, 80)
            mat_col2 = (100, 220, 100) if total_mats >= cost["material_count"] else (220, 100, 100)
            draw_text(surface, f"Gold: {cost['gold']}g", 30, ry + 40, gold_col2, 12, bold=True)
            draw_text(surface,
                f"Materials: need {cost['material_count']}× tier-{cost['min_material_tier']}+  (have {total_mats})",
                175, ry + 40, mat_col2, 12)

            if can:
                btn = pygame.Rect(SCREEN_W - 130, ry + 12, 90, 30)
                pygame.draw.rect(surface, accent, btn, 0, 4)
                draw_text(surface, "Upgrade", btn.x + 12, btn.y + 6, BLACK, 14, bold=True)

    def _draw_forge_enchant(self, surface, mx, my, y, total_gold, accent):
        from core.crafting import get_enchantable_items, get_applicable_enchants, ENCHANTMENTS, count_material

        items = get_enchantable_items(self.party)
        if not items:
            draw_text(surface, "No weapons or armor to enchant.", 30, y + 20, GREY, 15)
            return

        # Phase 1: item selection
        if self.forge_selected_item is None:
            draw_text(surface, "Select an item to enchant:", 30, y, CREAM, 14)
            y += 22
            visible = items[self.forge_scroll:self.forge_scroll + 8]
            for i, (char, idx, item, loc) in enumerate(visible):
                ry = y + i * 46
                box = pygame.Rect(20, ry, SCREEN_W - 40, 40)
                hover = box.collidepoint(mx, my)
                bc = (55, 45, 35) if hover else (40, 35, 28)
                pygame.draw.rect(surface, bc, box, 0, 5)
                ench_str = f" [{item.get('enchant_name','')}]" if item.get('enchant_name') else ""
                draw_text(surface, f"{item['name']}{ench_str}", 30, ry + 4, GOLD, 14)
                draw_text(surface, f"{char.name} ({loc})", 30, ry + 22, GREY, 11)
        else:
            # Phase 2: enchant selection
            item_idx = self.forge_selected_item
            if item_idx >= len(items):
                self.forge_selected_item = None
                return
            char, idx, item, loc = items[item_idx]
            draw_text(surface, f"Enchant: {item['name']}", 30, y, GOLD, 16, bold=True)
            draw_text(surface, f"({char.name})", 200, y + 2, GREY, 13)

            enchants = get_applicable_enchants(item)
            y += 26
            for i, ench_name in enumerate(enchants):
                ench = ENCHANTMENTS[ench_name]
                ry = y + i * 52
                # Check affordability
                can = total_gold >= ench["gold"]
                for mat, ct in ench["materials"].items():
                    if count_material(self.party, mat) < ct:
                        can = False

                box = pygame.Rect(20, ry, SCREEN_W - 40, 46)
                bc = (50, 40, 30) if can else (35, 30, 25)
                pygame.draw.rect(surface, bc, box, 0, 5)
                pygame.draw.rect(surface, accent if can else (60,50,40), box, 1, 5)

                draw_text(surface, ench_name, 30, ry + 4, GOLD if can else GREY, 15, bold=True)
                draw_text(surface, ench["desc"], 150, ry + 6, CREAM if can else (80,70,60), 12)
                cost_parts = [f"{ench['gold']}g"]
                for mat, ct in ench["materials"].items():
                    have = count_material(self.party, mat)
                    cost_parts.append(f"{mat}:{have}/{ct}")
                enc_cx = 30
                enc_gold_col = (200, 180, 80) if total_gold >= ench["gold"] else (220, 80, 80)
                draw_text(surface, f"{ench['gold']}g", enc_cx, ry + 26, enc_gold_col, 12, bold=True)
                enc_cx += 55
                for mat, ct in ench["materials"].items():
                    have2 = count_material(self.party, mat)
                    mc = (100, 220, 100) if have2 >= ct else (220, 100, 100)
                    draw_text(surface, f"{mat}: {have2}/{ct}", enc_cx, ry + 26, mc, 12)
                    enc_cx += len(mat) * 7 + 65

                if can:
                    btn = pygame.Rect(SCREEN_W - 130, ry + 8, 90, 28)
                    pygame.draw.rect(surface, accent, btn, 0, 4)
                    draw_text(surface, "Enchant", btn.x + 10, btn.y + 5, BLACK, 13, bold=True)

            # Cancel button
            cancel = pygame.Rect(20, y + len(enchants) * 52 + 10, 100, 30)
            pygame.draw.rect(surface, (80, 50, 50), cancel, 1, 4)
            draw_text(surface, "Cancel", cancel.x + 25, cancel.y + 7, RED, 13)

    def _handle_forge_click(self, mx, my):
        from core.crafting import (
            RECIPES, ENCHANTMENTS, can_afford_recipe, craft_item,
            get_upgradeable_items, get_upgrade_cost, apply_upgrade,
            consume_gold, consume_materials, get_materials_of_tier,
            get_enchantable_items, get_applicable_enchants, apply_enchant,
            count_material,
        )

        # Back button — matches draw y=140
        back = pygame.Rect(8, SCREEN_H - 140, 120, 34)
        if back.collidepoint(mx, my):
            self._return_to_town()
            self.forge_selected_item = None
            return None

        # Tab clicks — matches draw y=140
        tabs = [(self.VIEW_FORGE_CRAFT, 20), (self.VIEW_FORGE_UPGRADE, 160),
                (self.VIEW_FORGE_ENCHANT, 300), (self.VIEW_FORGE_REPAIR, 440)]
        for view, tx in tabs:
            tr = pygame.Rect(tx, 140, 130, 32)
            if tr.collidepoint(mx, my):
                self.view = view
                self.forge_scroll = 0
                self.forge_selected_item = None
                return None

        active_view = self.view if self.view != self.VIEW_FORGE else self.VIEW_FORGE_CRAFT
        y = 200  # matches _draw_forge y=200

        if active_view == self.VIEW_FORGE_REPAIR:
            from core.durability import (
                has_durability, get_durability_state, get_repair_cost,
                repair_item, init_durability
            )
            from core.focus_charges import (
                is_focus, init_charges, crystals_needed, recharge_with_crystals, CRYSTAL_NAME
            )
            from core.crafting import count_material
            y_r = 200 + 40
            row_h = 52
            btn_w, btn_h = 120, 30
            for ci, char in enumerate(self.party):
                for slot, item in list((char.equipment or {}).items()):
                    if not item or not has_durability(item):
                        continue
                    init_durability(item)
                    if get_durability_state(item) == "full":
                        continue
                    cost = get_repair_cost(item)
                    total_gold = sum(c.gold for c in self.party)
                    btn = pygame.Rect(SCREEN_W - 150, y_r + 8, btn_w, btn_h)
                    if btn.collidepoint(mx, my):
                        if total_gold < cost:
                            self._msg(f"Not enough gold! Need {cost}g.", RED)
                            return None
                        self._deduct_gold(cost)
                        repair_item(item)
                        sfx.play("shop_buy")
                        self._msg(f"Repaired {item.get('name','item')} for {cost}g.", (100, 220, 100))
                        return None
                    y_r += row_h + 6
            # Focus weapon recharge buttons
            y_rc = 138 + 40 + y_r + 30  # approximate — after repair section
            # Re-iterate to find recharge button positions (must mirror draw order)
            y_rc = 200 + 40
            # Skip past repair rows
            for char in self.party:
                for slot, item in list((char.equipment or {}).items()):
                    if not item or not has_durability(item): continue
                    init_durability(item)
                    if get_durability_state(item) != "full":
                        y_rc += row_h + 6
            y_rc += 30   # gap before recharge section
            for char in self.party:
                for slot, item in list((char.equipment or {}).items()):
                    if not item or not is_focus(item): continue
                    init_charges(item)
                    cur = item.get("charges", 0); mx_c = item.get("max_charges", 20)
                    if cur >= mx_c: continue
                    btn = pygame.Rect(SCREEN_W - 150, y_rc + 9, 120, 30)
                    if btn.collidepoint(mx, my):
                        needed = crystals_needed(item)
                        have   = count_material(self.party, CRYSTAL_NAME)
                        if have < needed:
                            self._msg(f"Need {needed} Mana Crystals (have {have}).", RED)
                            return None
                        gained, used = recharge_with_crystals(item, self.party)
                        sfx.play("shop_buy")
                        self._msg(f"Recharged {item.get('name','wand')}: +{gained} charges "
                                  f"({used} crystal{'s' if used>1 else ''} used).", (120, 200, 255))
                        return None
                    y_rc += 54
            return None

        if active_view == self.VIEW_FORGE_CRAFT:
            visible = RECIPES[self.forge_scroll:self.forge_scroll + 7]
            for i, recipe in enumerate(visible):
                ry = y + i * 76
                if can_afford_recipe(self.party, recipe):
                    btn = pygame.Rect(SCREEN_W - 120, ry + 16, 80, 30)
                    if btn.collidepoint(mx, my):
                        result = craft_item(self.party, recipe)
                        if result:
                            self.party[0].inventory.append(result)
                            sfx.play("shop_buy")
                            self._msg(f"Crafted {result['name']}! Added to {self.party[0].name}'s inventory.", (255, 200, 80))
                        return None

        elif active_view == self.VIEW_FORGE_UPGRADE:
            items = get_upgradeable_items(self.party)
            visible = items[self.forge_scroll:self.forge_scroll + 7]
            for i, (char, idx, item, loc) in enumerate(visible):
                ry = y + i * 62
                cost = get_upgrade_cost(item)
                if not cost:
                    continue
                avail_mats = get_materials_of_tier(self.party, cost["min_material_tier"])
                total_mats = sum(avail_mats.values())
                can = sum(c.gold for c in self.party) >= cost["gold"] and total_mats >= cost["material_count"]
                if can:
                    btn = pygame.Rect(SCREEN_W - 130, ry + 12, 90, 30)
                    if btn.collidepoint(mx, my):
                        # Consume gold
                        consume_gold(self.party, cost["gold"])
                        # Consume materials (pick from available tier mats)
                        remaining = cost["material_count"]
                        for mat_name, have in avail_mats.items():
                            if remaining <= 0:
                                break
                            use = min(have, remaining)
                            consume_materials(self.party, {mat_name: use})
                            remaining -= use
                        old_name = item["name"]
                        apply_upgrade(item)
                        sfx.play("shop_buy")
                        self._msg(f"Upgraded {old_name} → {item['name']}!", (255, 200, 80))
                        return None

        elif active_view == self.VIEW_FORGE_ENCHANT:
            items = get_enchantable_items(self.party)
            if self.forge_selected_item is None:
                # Item selection phase
                visible = items[self.forge_scroll:self.forge_scroll + 8]
                y_start = y + 22
                for i, (char, idx, item, loc) in enumerate(visible):
                    ry = y_start + i * 46
                    box = pygame.Rect(20, ry, SCREEN_W - 40, 40)
                    if box.collidepoint(mx, my):
                        self.forge_selected_item = self.forge_scroll + i
                        return None
            else:
                # Enchant selection phase
                if self.forge_selected_item >= len(items):
                    self.forge_selected_item = None
                    return None
                char, idx, item, loc = items[self.forge_selected_item]
                enchants = get_applicable_enchants(item)
                ey = y + 26
                total_gold = sum(c.gold for c in self.party)
                for i, ench_name in enumerate(enchants):
                    ench = ENCHANTMENTS[ench_name]
                    ry = ey + i * 52
                    can = total_gold >= ench["gold"]
                    for mat, ct in ench["materials"].items():
                        if count_material(self.party, mat) < ct:
                            can = False
                    if can:
                        btn = pygame.Rect(SCREEN_W - 130, ry + 8, 90, 28)
                        if btn.collidepoint(mx, my):
                            consume_gold(self.party, ench["gold"])
                            consume_materials(self.party, ench["materials"])
                            old_name = item["name"]
                            apply_enchant(item, ench_name)
                            sfx.play("quest_complete")
                            self._msg(f"Enchanted! {old_name} → {item['name']}", (180, 140, 255))
                            self.forge_selected_item = None
                            return None

                # Cancel button
                cancel = pygame.Rect(20, ey + len(enchants) * 52 + 10, 100, 30)
                if cancel.collidepoint(mx, my):
                    self.forge_selected_item = None
                    return None

        return None
