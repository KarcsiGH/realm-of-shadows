"""
Headless story logic tests — no pygame required.
Run with: python3 tests/test_story_logic.py
"""
import sys
import os
import types

# ── Mock pygame BEFORE any game module loads ──────────────────────────────────
pg = types.ModuleType("pygame")
pg.init = lambda: None
pg.quit = lambda: None
pg.display = types.SimpleNamespace(set_mode=lambda *a,**k: None, flip=lambda:None)
pg.font   = types.SimpleNamespace(init=lambda:None, SysFont=lambda *a,**k: None, Font=lambda *a,**k: None)
pg.mixer  = types.SimpleNamespace(init=lambda *a,**k: None, music=types.SimpleNamespace(load=lambda *a:None, play=lambda *a:None))
pg.time   = types.SimpleNamespace(Clock=lambda: types.SimpleNamespace(tick=lambda *a:0, get_time=lambda:16))
pg.Surface = lambda *a,**k: types.SimpleNamespace(blit=lambda *a,**k:None, fill=lambda *a:None, get_size=lambda:(1280,800), get_width=lambda:1280, get_height=lambda:800, set_alpha=lambda *a:None, convert_alpha=lambda:None)
pg.SRCALPHA = 0
pg.KEYDOWN = 1
pg.MOUSEBUTTONDOWN = 2
pg.Color = lambda *a: (0,0,0,255)
pg.Rect  = lambda *a: types.SimpleNamespace(collidepoint=lambda *a:False, x=0, y=0, w=0, h=0)
sys.modules["pygame"] = pg
sys.modules["pygame.font"] = pg.font
sys.modules["pygame.mixer"] = pg.mixer

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ─────────────────────────────────────────────────────────────────────────────

import traceback

PASS = 0
FAIL = 0

def check(name, condition, detail=""):
    global PASS, FAIL
    if condition:
        print(f"  ✓ {name}")
        PASS += 1
    else:
        print(f"  ✗ {name}" + (f" — {detail}" if detail else ""))
        FAIL += 1

def section(title):
    print(f"\n{'─'*55}")
    print(f"  {title}")
    print(f"{'─'*55}")

# ═════════════════════════════════════════════════════════════
#  1. STORY FLAGS
# ═════════════════════════════════════════════════════════════
section("1. Story Flags")
try:
    from core.story_flags import (
        set_flag, get_flag, check_conditions,
        collect_hearthstone, hearthstone_count,
        defeat_boss, clear_all  # clear_all may not exist — handled below
    )
except ImportError:
    from core.story_flags import set_flag, get_flag, check_conditions, collect_hearthstone, hearthstone_count, defeat_boss
    clear_all = None

# Reset state if possible
if clear_all:
    clear_all()

set_flag("test.flag", True)
check("set/get flag", get_flag("test.flag") == True)
check("missing flag returns None/False", not get_flag("nonexistent.flag"))

collect_hearthstone(1)
check("hearthstone count after 1", hearthstone_count() == 1)
collect_hearthstone(2)
collect_hearthstone(3)
check("hearthstone count after 3", hearthstone_count() == 3)

set_flag("boss.korrath.defeated", True)
cond = [{"flag": "boss.korrath.defeated", "op": "==", "value": True}]
check("check_conditions pass", check_conditions(cond))
cond_fail = [{"flag": "boss.korrath.defeated", "op": "not_exists"}]
check("check_conditions fail when flag set", not check_conditions(cond_fail))

# ═════════════════════════════════════════════════════════════
#  2. KORRATH DIALOGUE TREE
# ═════════════════════════════════════════════════════════════
section("2. Korrath Boss Dialogue")
try:
    from data.story_data import NPC_DIALOGUES as BOSS_DIALOGUES
    korrath_variants = BOSS_DIALOGUES.get("korrath", [])
    check("korrath dialogue exists", len(korrath_variants) > 0)

    tree = korrath_variants[0]["tree"]
    nodes = tree["nodes"]
    check("korrath has start node", "start" in nodes)
    check("korrath has 'reason' node", "reason" in nodes)
    check("korrath has 'no_other_way' node", "no_other_way" in nodes)
    check("korrath has 'fight_accept' node", "fight_accept" in nodes)

    # Verify all choices point to valid nodes or end
    broken_links = []
    for node_id, node in nodes.items():
        for choice in node.get("choices", []):
            target = choice.get("next")
            if target and target not in nodes:
                broken_links.append(f"{node_id} -> {target}")
        if node.get("next") and node["next"] not in nodes:
            broken_links.append(f"{node_id} -> {node['next']}")
    check("all korrath node links are valid", len(broken_links) == 0,
          f"broken: {broken_links}")
except Exception as e:
    check("korrath dialogue load", False, str(e))

# ═════════════════════════════════════════════════════════════
#  3. ASHVAR DIALOGUE TREE
# ═════════════════════════════════════════════════════════════
section("3. Ashvar Boss Dialogue")
try:
    ashvar_variants = BOSS_DIALOGUES.get("ashvar", [])
    check("ashvar dialogue exists", len(ashvar_variants) > 0)

    tree = ashvar_variants[0]["tree"]
    nodes = tree["nodes"]
    check("ashvar has start node", "start" in nodes)
    check("ashvar has 'still_alive' node (Valdris reveal)", "still_alive" in nodes)

    # Check Valdris lore flag is set in still_alive
    still_alive = nodes.get("still_alive", {})
    actions = still_alive.get("on_enter", [])
    lore_flags = [a for a in actions if a.get("flag") == "lore.ashvar_truth"]
    check("still_alive sets lore.ashvar_truth flag", len(lore_flags) > 0)

    broken_links = []
    for node_id, node in nodes.items():
        for choice in node.get("choices", []):
            target = choice.get("next")
            if target and target not in nodes:
                broken_links.append(f"{node_id} -> {target}")
        if node.get("next") and node["next"] not in nodes:
            broken_links.append(f"{node_id} -> {node['next']}")
    check("all ashvar node links valid", len(broken_links) == 0,
          f"broken: {broken_links}")
except Exception as e:
    check("ashvar dialogue load", False, str(e))

# ═════════════════════════════════════════════════════════════
#  4. HEARTHSTONE DROP FROM KORRATH
# ═════════════════════════════════════════════════════════════
section("4. Korrath Loot — Hearthstone Fragment")
try:
    from data.enemies import ENEMIES
    korrath = ENEMIES.get("Korrath the Stone Warden")
    check("Korrath enemy exists", korrath is not None)

    loot = korrath.get("loot_table", [])
    hs_drops = [e for e in loot if "hearthstone" in e["item"].get("subtype","").lower()
                or "Hearthstone" in e["item"].get("name","")]
    check("Korrath has hearthstone in loot_table", len(hs_drops) > 0)
    check("Hearthstone drop chance is 1.0 (guaranteed)", hs_drops[0]["drop_chance"] == 1.0)
except Exception as e:
    check("korrath loot check", False, str(e))

# ═════════════════════════════════════════════════════════════
#  5. HEARTHSTONE FLAG CHAIN
# ═════════════════════════════════════════════════════════════
section("5. Hearthstone → Briarhollow Attack Flag Chain")
try:
    if clear_all:
        clear_all()

    # Simulate: Korrath defeated, hearthstone collected
    set_flag("hearthstone.abandoned_mine", True)
    hs1 = get_flag("hearthstone.abandoned_mine")
    already_done = get_flag("briarhollow_attack.done")
    should_trigger = bool(hs1 and not already_done)
    check("attack triggers when hs1 set and not done", should_trigger)

    # Simulate: attack already fired
    set_flag("briarhollow_attack.done", True)
    already_done = get_flag("briarhollow_attack.done")
    should_trigger = bool(hs1 and not already_done)
    check("attack does NOT re-trigger after done", not should_trigger)
except Exception as e:
    check("flag chain check", False, str(e))

# ═════════════════════════════════════════════════════════════
#  6. MAREN BETRAYAL CONDITIONS
# ═════════════════════════════════════════════════════════════
section("6. Maren Betrayal Trigger Conditions")
try:
    if clear_all:
        clear_all()

    from data.story_data import NPC_DIALOGUES as BOSS_DIALOGUES
    maren_variants = BOSS_DIALOGUES.get("maren", [])
    betrayal = next((v for v in maren_variants if v.get("tree", {}).get("id") == "maren_betrayal"), None)
    check("maren_betrayal dialogue exists", betrayal is not None)

    if betrayal:
        conditions = betrayal.get("conditions", [])
        required_flags = [c["flag"] for c in conditions if c.get("op") == "=="]
        check("requires abandoned_mine defeat", "boss_defeated.abandoned_mine" in required_flags)
        check("requires ruins_ashenmoor defeat", "boss_defeated.ruins_ashenmoor" in required_flags)
        check("requires sunken_crypt defeat", "boss_defeated.sunken_crypt" in required_flags)

        # Conditions should FAIL before bosses beaten
        check("conditions fail before bosses beaten", not check_conditions(conditions))

        # Set the required flags
        for flag in required_flags:
            set_flag(flag, True)
        not_exists_conds = [c for c in conditions if c.get("op") == "not_exists"]
        check("conditions pass after bosses beaten", check_conditions(conditions))

        # Set betrayal_done — should block re-trigger
        set_flag("maren.betrayal_done", True)
        check("conditions fail after betrayal_done set", not check_conditions(conditions))
except Exception as e:
    check("maren betrayal check", False, str(e))

# ═════════════════════════════════════════════════════════════
#  7. MAREN TAKES HEARTHSTONES — inventory logic
# ═════════════════════════════════════════════════════════════
section("7. Maren Takes Hearthstones — Inventory")
try:
    class FakeMember:
        def __init__(self, items):
            self.inventory = list(items)

    class FakeParty:
        def __init__(self, members):
            self.members = members

    hs_item  = {"name": "Hearthstone Fragment (Mine)", "type": "key_item"}
    hs_item2 = {"name": "Hearthstone Fragment (Crypt)", "type": "key_item"}
    hs_item3 = {"name": "Hearthstone Fragment (Dragon)", "type": "key_item"}
    sword    = {"name": "Iron Sword", "type": "weapon"}

    member1 = FakeMember([hs_item, hs_item2, sword])
    member2 = FakeMember([hs_item3])
    party = FakeParty([member1, member2])

    # Replicate the _maren_takes_hearthstones logic
    taken = 0
    for member in party.members:
        if taken >= 2:
            break
        remove_these = []
        for item in member.inventory:
            if taken >= 2:
                break
            name = item.get("name", "")
            if "Hearthstone Fragment" in name or "hearthstone" in name.lower():
                remove_these.append(item)
                taken += 1
        for item in remove_these:
            if item in member.inventory:
                member.inventory.remove(item)

    check("exactly 2 hearthstones removed", taken == 2)
    check("non-hearthstone items preserved", sword in member1.inventory)
    remaining_hs = sum(
        1 for m in party.members
        for i in m.inventory
        if "Hearthstone Fragment" in i.get("name","")
    )
    check("1 hearthstone remains after betrayal", remaining_hs == 1)
except Exception as e:
    check("maren inventory logic", False, str(e))

# ═════════════════════════════════════════════════════════════
#  8. BOSS ENCOUNTER KEYS
# ═════════════════════════════════════════════════════════════
section("8. Boss Encounter Keys Exist in Enemies")
try:
    from data.enemies import ENCOUNTERS
    boss_encounters = ["boss_mine_warden", "boss_ashenmoor", "boss_goblin_king", "boss_spider_queen"]
    for key in boss_encounters:
        check(f"encounter '{key}' exists", key in ENCOUNTERS)
except Exception as e:
    check("encounter keys check", False, str(e))

# ═════════════════════════════════════════════════════════════
#  SUMMARY
# ═════════════════════════════════════════════════════════════
# ═════════════════════════════════════════════════════════════
#  9. CURSED ITEMS
# ═════════════════════════════════════════════════════════════
section("9. Cursed Items")
try:
    from data.magic_items import CURSED_ITEMS, CURSED_ITEMS_T1, CURSED_ITEMS_T2, CURSED_ITEMS_T3, get_cursed_item
    check("cursed items defined", len(CURSED_ITEMS) >= 5)
    check("tier 1 cursed items exist", len(CURSED_ITEMS_T1) >= 1)
    check("tier 2 cursed items exist", len(CURSED_ITEMS_T2) >= 1)
    check("tier 3 cursed items exist", len(CURSED_ITEMS_T3) >= 1)

    import random as _rng
    item = get_cursed_item(1, 3, _rng)
    check("get_cursed_item returns item", item is not None)
    check("returned item has cursed=True", item.get("cursed") == True)
    check("returned item starts unidentified", item.get("identified") == False)

    # Test unequip blocked by curse
    from core.equipment import unequip_item
    class FakeChar:
        equipment = {"head": {"name": "Helm of Weakness", "cursed": True, "identified": True}}
        inventory = []
    char = FakeChar()
    ok, item_out, msg = unequip_item(char, "head")
    check("cursed item blocks unequip", ok == False)
    check("cursed item unequip message mentions cursed", "cursed" in msg.lower())

    # Test curse_lifted allows unequip
    char2 = FakeChar()
    char2.equipment = {"head": {"name": "Helm of Weakness", "cursed": True, "curse_lifted": True}}
    char2.inventory = []
    ok2, _, _ = unequip_item(char2, "head")
    check("curse_lifted allows unequip", ok2 == True)

except Exception as e:
    check("cursed items check", False, str(e))
    traceback.print_exc()

# ── re-print summary ──
# ═════════════════════════════════════════════════════════════
#  10. REMOVE CURSE — SPELLS & SCROLLS
# ═════════════════════════════════════════════════════════════
section("10. Remove Curse — Spells & Scrolls")
try:
    from core.abilities import CLASS_ABILITIES as ABILITIES

    # Cleric gets Remove Curse at level 7
    cleric_spells = ABILITIES.get("Cleric", [])
    rc_cleric = next((a for a in cleric_spells if a["name"] == "Remove Curse"), None)
    check("Cleric has Remove Curse spell", rc_cleric is not None)
    check("Cleric Remove Curse unlocks at level 7", rc_cleric and rc_cleric.get("level") == 7)
    check("Cleric Remove Curse has cures=curse", rc_cleric and rc_cleric.get("cures") == "curse")

    # Paladin gets Remove Curse at level 8
    paladin_spells = ABILITIES.get("Paladin", [])
    rc_paladin = next((a for a in paladin_spells if a["name"] == "Remove Curse"), None)
    check("Paladin has Remove Curse spell", rc_paladin is not None)
    check("Paladin Remove Curse unlocks at level 8", rc_paladin and rc_paladin.get("level") == 8)

    # Scroll exists in shop and dungeon loot
    from data.shop_inventory import TOWN_SHOP_PROFILES as TOWN_SHOPS
    all_shop_items = [
        i for shop in TOWN_SHOPS.values()
        for section in ("consumables", "weapons", "armor", "bonus_items")
        for i in (shop.get(section) or [])
    ]
    rc_scroll_shop = next((i for i in all_shop_items if "Remove Curse" in i.get("name", "")), None)
    check("Scroll of Remove Curse in a town shop", rc_scroll_shop is not None)

    from data.magic_items import SECRET_ITEMS_T1
    rc_scroll_dungeon = next((i for i in SECRET_ITEMS_T1 if "Remove Curse" in i.get("name", "")), None)
    check("Scroll of Remove Curse in dungeon loot (T1)", rc_scroll_dungeon is not None)

    # Scroll removes cursed gear when used
    class FakeMember:
        def __init__(self):
            self.equipment = {"head": {"name": "Helm of Weakness", "cursed": True, "identified": True}}
            self.inventory = [{"name": "Scroll of Remove Curse", "effect": "remove_curse"}]
            self.resources = {}
            self.name = "Test"
        def get_status_effects(self): return []

    import types
    char = FakeMember()
    # Simulate scroll use logic from camp_ui
    cursed_slots = [
        slot for slot, eq in (char.equipment or {}).items()
        if eq and eq.get("cursed") and not eq.get("curse_lifted")
    ]
    for slot in cursed_slots:
        eq = char.equipment[slot]
        eq["curse_lifted"] = True
        char.equipment[slot] = None
        char.inventory.append(eq)

    check("Scroll use lifts cursed gear", char.equipment.get("head") is None)
    check("Cursed item returned to inventory after scroll", 
          any(i.get("name") == "Helm of Weakness" for i in char.inventory))

except Exception as e:
    check("remove curse spells/scrolls check", False, str(e))
    traceback.print_exc()

# ─────────────────────────────────────────────────────────────
# ═════════════════════════════════════════════════════════════
#  11. UNIQUE ITEMS & ITEM SETS
# ═════════════════════════════════════════════════════════════
section("11. Unique Items & Item Sets")
try:
    from data.magic_items import UNIQUE_ITEMS, ITEM_SETS, get_unique_item, party_has_unique, get_set_bonus, calc_set_stat_bonuses

    check("UNIQUE_ITEMS defined", len(UNIQUE_ITEMS) >= 5)
    check("ITEM_SETS defined", len(ITEM_SETS) >= 2)
    check("warden_set exists", "warden_set" in ITEM_SETS)
    check("ashenmoor_set exists", "ashenmoor_set" in ITEM_SETS)

    # get_unique_item returns copy
    blade = get_unique_item("korrath_blade")
    check("get_unique_item returns item", blade is not None)
    check("unique item has correct name", blade["name"] == "Korrath's Last Oath")
    check("unique item has set_id", blade.get("set_id") == "warden_set")
    check("unique item has lore", len(blade.get("lore", "")) > 20)

    # party_has_unique prevents duplicates
    class FakeMember2:
        def __init__(self):
            self.inventory = []
            self.equipment = {}

    party_test = [FakeMember2()]
    party_test[0].inventory.append(blade)
    check("party_has_unique detects item in inventory",
          party_has_unique(party_test, "Korrath's Last Oath"))
    check("get_unique_item returns None when party has it",
          get_unique_item("korrath_blade", party_test) is None)

    # Set bonuses — equip 2 warden pieces
    m = FakeMember2()
    m.equipment = {
        "weapon": get_unique_item("korrath_blade"),
        "accessory1": get_unique_item("korrath_ring"),
    }
    active = get_set_bonus(m)
    check("2pc warden set activates", "warden_set" in active)
    bonuses = calc_set_stat_bonuses(m)
    check("2pc warden set grants STR bonus", bonuses.get("STR", 0) >= 2)
    check("2pc warden set grants CON bonus", bonuses.get("CON", 0) >= 2)

except Exception as e:
    check("unique items / sets check", False, str(e))
    traceback.print_exc()

# ═════════════════════════════════════════════════════════════
#  12. DURABILITY SYSTEM
# ═════════════════════════════════════════════════════════════
section("12. Durability System")
try:
    from core.durability import (
        has_durability, init_durability, get_durability_state,
        get_durability_label, degrade_weapon, degrade_armor,
        get_repair_cost, repair_item, get_effective_damage
    )

    weapon = {"name": "Sword", "type": "weapon", "damage": 20}
    armor  = {"name": "Plate", "type": "armor",  "defense": 15}

    check("weapon has_durability", has_durability(weapon))
    check("armor has_durability", has_durability(armor))
    check("consumable no durability", not has_durability({"type": "consumable"}))

    init_durability(weapon)
    check("init sets durability=100", weapon["durability"] == 100)
    check("state full at 100", get_durability_state(weapon) == "full")
    check("label shows 100/100", get_durability_label(weapon) == "100/100")

    # Degrade to damaged
    weapon["durability"] = 50
    check("state damaged at 50", get_durability_state(weapon) == "damaged")

    # Degrade to worn
    weapon["durability"] = 20
    check("state worn at 20", get_durability_state(weapon) == "worn")
    check("effective damage reduced when worn", get_effective_damage(weapon) < 20)

    # Degrade to broken
    weapon["durability"] = 0
    check("state broken at 0", get_durability_state(weapon) == "broken")
    check("label shows BROKEN", get_durability_label(weapon) == "BROKEN")
    check("effective damage heavily reduced when broken", get_effective_damage(weapon) < 10)

    # Repair
    cost = get_repair_cost(weapon)
    check("repair cost > 0 when broken", cost > 0)
    repair_item(weapon)
    check("repair restores full durability", weapon["durability"] == 100)
    check("repair cost is 0 after repair", get_repair_cost(weapon) == 0)

    # degrade_weapon reduces durability
    weapon["durability"] = 100
    degrade_weapon(weapon)
    check("degrade_weapon reduces durability", weapon["durability"] < 100)

except Exception as e:
    check("durability system check", False, str(e))
    traceback.print_exc()

# ═════════════════════════════════════════════════════════════
#  13. ADVANCED EQUIPMENT CATALOG
# ═════════════════════════════════════════════════════════════
section("13. Advanced Equipment Catalog")
try:
    from data.advanced_equipment import (
        ALL_CLASS_WEAPONS, ALL_CLASS_ARMOR, ALL_CLASS_ACCESSORIES,
        WEAPONS_T1, WEAPONS_T2, WEAPONS_T3, WEAPONS_T4,
        get_shop_weapons, get_shop_armor, get_class_equipment,
    )
    from data.shop_inventory import get_town_shop

    classes = ["Fighter", "Mage", "Cleric", "Thief", "Ranger", "Monk"]
    check("All 6 classes have weapons", all(cls in ALL_CLASS_WEAPONS for cls in classes))
    check("All 6 classes have armor",   all(cls in ALL_CLASS_ARMOR   for cls in classes))
    check("T1 weapons exist", len(WEAPONS_T1) >= 10)
    check("T2 weapons exist", len(WEAPONS_T2) >= 10)
    check("T3 weapons exist", len(WEAPONS_T3) >= 10)
    check("T4 weapons exist", len(WEAPONS_T4) >= 5)

    # Each class has items at each rarity
    for cls in classes:
        for rarity in ("common", "uncommon", "rare", "epic"):
            w, a, acc = get_class_equipment(cls, rarity)
            check(f"{cls} has {rarity} items", len(w) + len(a) + len(acc) > 0)

    # Shop filtering works by tier
    village_wpn = get_shop_weapons("village", ["Fighter", "Mage"])
    town_wpn    = get_shop_weapons("town",    ["Thief"])
    city_wpn    = get_shop_weapons("city",    ["Ranger"])
    cap_wpn     = get_shop_weapons("capital", ["Monk"])

    check("Village has T1 weapons",  any(i["rarity"] == "common"   for i in village_wpn))
    check("Town has T2 weapons",     any(i["rarity"] == "uncommon" for i in town_wpn))
    check("City has T3 weapons",     any(i["rarity"] == "rare"     for i in city_wpn))
    check("Capital has T4 weapons",  any(i["rarity"] == "epic"     for i in cap_wpn))

    # Town shop integration
    shop = get_town_shop("briarhollow", ["Fighter"])
    check("Briarhollow shop has weapons",    len(shop["weapons"]) > 0)
    check("Briarhollow shop has armor",      len(shop["armor"]) > 0)
    check("Briarhollow weapons are T1",
          all(i["buy_price"] <= 80 for i in shop["weapons"] if i["rarity"] == "common"))

    shop_city = get_town_shop("ironhearth", ["Mage", "Cleric"])
    check("City shop has higher-tier items", any(i["rarity"] in ("uncommon","rare") for i in shop_city["weapons"]))

    # Items have required fields
    for item in WEAPONS_T2[:3]:
        check(f"{item['name']} has damage",  "damage" in item)
        check(f"{item['name']} has buy_price", "buy_price" in item)

except Exception as e:
    check("Advanced equipment check", False, str(e))
    traceback.print_exc()

# ═════════════════════════════════════════════════════════════
#  14. NPC DIALOGUE COVERAGE
# ═════════════════════════════════════════════════════════════
section("14. NPC Dialogue Coverage")
try:
    from data.town_maps import TOWN_MAPS
    from data.story_data import NPC_DIALOGUES

    all_towns = list(TOWN_MAPS.keys())
    check("All 8 towns present", len(all_towns) == 8)

    for town_id in all_towns:
        td = TOWN_MAPS[town_id]
        npcs = td["npcs"]
        check(f"{town_id} has NPCs", len(npcs) >= 4)
        positioned = [n for n in npcs if "x" in n and "y" in n]
        check(f"{town_id} NPCs have positions", len(positioned) == len(npcs))

    # Dialogue completeness — every named dialogue_id resolves
    broken = []
    for town_id, td in TOWN_MAPS.items():
        for npc in td["npcs"]:
            did = npc.get("dialogue_id")
            if did and did not in NPC_DIALOGUES:
                broken.append(f"{town_id}/{npc['name']}:{did}")
    check("No broken dialogue_id references", len(broken) == 0, str(broken))

    # New dialogues present
    new_ids = [
        "captain_aldric", "elder_thom", "ranger_lyric", "old_moss",
        "guildmaster_oren", "foreman_brak", "scholar_petra",
        "scout_feryn", "trapper_holt", "shady_figure",
        "pilgrim_elder", "holy_knight", "novice_priest", "high_priest_aldara",
        "apprentice_mage", "crystal_scholar", "archmage_solen", "teleport_master",
        "city_guard_thornhaven", "imperial_crier", "merchant_noble", "refugee",
        "governor_aldric", "guild_commander_varek", "court_mage_sira",
    ]
    for did in new_ids:
        check(f"Dialogue exists: {did}", did in NPC_DIALOGUES)

    # Each new dialogue has at least one tree with nodes
    for did in new_ids:
        entries = NPC_DIALOGUES.get(did, [])
        has_tree = any("tree" in e and "nodes" in e["tree"] for e in entries)
        check(f"{did} has valid tree", has_tree)

    # Thornhaven has 3 new story NPCs
    th_npcs = [n["name"] for n in TOWN_MAPS["thornhaven"]["npcs"]]
    check("Thornhaven has Governor Aldric", "Governor Aldric" in th_npcs)
    check("Thornhaven has Guild Commander Varek", "Guild Commander Varek" in th_npcs)
    check("Thornhaven has Court Mage Sira", "Court Mage Sira" in th_npcs)

    # Total NPC count
    total_npcs = sum(len(td["npcs"]) for td in TOWN_MAPS.values())
    check("71+ total NPCs across towns", total_npcs >= 71)

except Exception as e:
    check("NPC dialogue check", False, str(e))
    import traceback; traceback.print_exc()

# ═════════════════════════════════════════════════════════════
#  15. QUEST SYSTEM DEPTH
# ═════════════════════════════════════════════════════════════
section("15. Quest System Depth")
try:
    from data.story_data import QUESTS, NPC_DIALOGUES
    from core.story_flags import (
        reset, set_flag, start_quest, complete_quest,
        check_quest_objectives, all_objectives_complete,
        auto_advance_quests, increment,
    )

    # All 16 quests present
    check("16 quests defined", len(QUESTS) == 16)

    # Required fields on every quest
    required_fields = ["name", "description", "act", "objectives",
                       "reward_gold", "reward_xp", "reward_items", "giver_npc"]
    all_have_fields = all(
        all(f in q for f in required_fields)
        for q in QUESTS.values()
    )
    check("All quests have required fields", all_have_fields)

    # Every quest has at least one objective
    all_have_objs = all(len(q.get("objectives", [])) >= 1 for q in QUESTS.values())
    check("All quests have ≥1 objective", all_have_objs)

    # Objective flag evaluation
    reset()
    set_flag("boss.grak.defeated", True)
    set_flag("explored.goblin_warren.floor1", True)
    start_quest("main_goblin_warren")
    objs = check_quest_objectives("main_goblin_warren")
    check("goblin_warren objectives tracked", len(objs) == 2)
    check("goblin_warren all objectives complete", all_objectives_complete("main_goblin_warren"))

    # Wolf pelt >= objective
    reset()
    start_quest("side_wolf_pelts")
    for _ in range(4):
        increment("wolf_pelts_quest.count")
    objs = check_quest_objectives("side_wolf_pelts")
    check("wolf pelts: 4/5 not complete", not objs[0][1])
    increment("wolf_pelts_quest.count")
    objs = check_quest_objectives("side_wolf_pelts")
    check("wolf pelts: 5/5 complete", objs[0][1])

    # Multi-objective quest: all must be done
    reset()
    start_quest("main_hearthstone_1")
    set_flag("explored.abandoned_mine.floor1", True)
    check("hs1: 1/3 not complete", not all_objectives_complete("main_hearthstone_1"))
    set_flag("boss.korrath.defeated", True)
    set_flag("item.hearthstone.1", True)
    check("hs1: 3/3 complete", all_objectives_complete("main_hearthstone_1"))

    # Auto-advance: quests with turn_in_npc should NOT auto-complete
    reset()
    set_flag("boss.grak.defeated", True)
    set_flag("explored.goblin_warren.floor1", True)
    start_quest("main_goblin_warren")
    done = auto_advance_quests([])
    check("main_goblin_warren NOT auto-completed (has turn_in)", "main_goblin_warren" not in done)

    # Auto-advance: quests with auto_complete=True DO auto-complete
    reset()
    set_flag("explored.valdris_spire.floor1", True)
    start_quest("main_act3_spire")
    done = auto_advance_quests([])
    check("main_act3_spire auto-completed", "main_act3_spire" in done)

    # Reward distribution
    class _FC:
        def __init__(self): self.gold = 100; self.xp = 50
    reset()
    set_flag("explored.sunken_crypt.floor1", True)
    set_flag("boss.sunken_warden.defeated", True)
    set_flag("item.hearthstone.2", True)
    start_quest("main_hearthstone_2")
    # main_hearthstone_2 has turn_in=Tide Priest Oran, NOT auto_complete
    # manually complete to test reward distribution
    from core.story_flags import _distribute_quest_rewards
    fc = [_FC(), _FC()]
    _distribute_quest_rewards("main_hearthstone_2", fc)
    expected_gold = 300 // 2
    check("quest rewards distributed correctly", fc[0].gold == 100 + expected_gold)

    # Quest log UI integrity
    from ui.quest_log_ui import QuestLogUI
    ui = QuestLogUI()
    check("QuestLogUI instantiates", ui.tab == "quests")
    check("QuestLogUI has required attrs",
          hasattr(ui, "selected_qid") and hasattr(ui, "scroll_list") and
          hasattr(ui, "scroll_detail") and hasattr(ui, "_list_rects"))

    # Dialogue quest references valid
    bad_refs = []
    for did, entries in NPC_DIALOGUES.items():
        for entry in entries:
            for nid, node in entry.get("tree", {}).get("nodes", {}).items():
                for act in node.get("on_enter", []) + node.get("on_exit", []):
                    if act.get("action") in ("start_quest", "complete_quest"):
                        qref = act.get("quest")
                        if qref and qref not in QUESTS:
                            bad_refs.append(f"{did}/{nid}->{qref}")
    check("No broken quest refs in dialogues", len(bad_refs) == 0, str(bad_refs))

    # All 15 dialogue-wired quests found
    import re
    with open("data/story_data.py") as f:
        sdata = f.read()
    wired = {m.group(1) for m in re.finditer(r'"quest": "([^"]+)"', sdata)}
    unwired = [qid for qid in QUESTS if qid not in wired
               and qid != "main_act3_finale"]  # auto-started by floor hook
    check("All quests except finale are dialogue-wired", len(unwired) == 0, str(unwired))

except Exception as e:
    check("Quest system check", False, str(e))
    import traceback; traceback.print_exc()

# ─────────────────────────────────────────────────────────────
total = PASS + FAIL
print(f"\n{'═'*55}")
print(f"  Results: {PASS}/{total} passed", "✓" if FAIL == 0 else f"— {FAIL} FAILED")
print(f"{'═'*55}\n")
sys.exit(0 if FAIL == 0 else 1)
