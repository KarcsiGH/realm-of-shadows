"""
data/advanced_equipment.py
Class-specific equipment catalog — 4 tiers per class.

Tiers:
  T1 common    — starting villages, early dungeons
  T2 uncommon  — towns, mid dungeons
  T3 rare      — cities, late dungeons, boss loot
  T4 epic      — capital / Thornhaven, end-game

Each item uses the standard item dict format compatible with existing shop,
inventory, and combat systems.
"""

# ── Helpers ────────────────────────────────────────────────────
def _w(name, subtype, damage, phys, stat_bonuses, buy, rarity, desc,
       allowed=None, spell_bonus=0, crit_mod=0, accuracy_mod=0,
       speed_mod=0, enchant_element=None, enchant_bonus=0, enchant_name="",
       range_="melee", special=None, damage_stat=None):
    item = {
        "name": name, "type": "weapon", "slot": "weapon",
        "subtype": subtype, "rarity": rarity, "damage": damage,
        "phys_type": phys, "range": range_,
        "stat_bonuses": stat_bonuses,
        "buy_price": buy, "sell_price": buy // 4,
        "identified": True, "description": desc,
    }
    if allowed:       item["allowed_classes"] = allowed
    if spell_bonus:   item["spell_bonus"] = spell_bonus
    if crit_mod:      item["crit_mod"] = crit_mod
    if accuracy_mod:  item["accuracy_mod"] = accuracy_mod
    if speed_mod:     item["speed_mod"] = speed_mod
    if enchant_element:
        item["enchant_element"] = enchant_element
        item["enchant_bonus"] = enchant_bonus
        item["enchant_name"] = enchant_name
    if special:       item["special"] = special
    if damage_stat:   item["damage_stat"] = damage_stat
    return item

def _a(name, subtype, slot, defense, stat_bonuses, buy, rarity, desc,
       allowed=None, magic_resist=0, speed_mod=0,
       enchant_element=None, enchant_bonus=0, enchant_name=""):
    item = {
        "name": name, "type": "armor", "slot": slot,
        "subtype": subtype, "rarity": rarity, "defense": defense,
        "stat_bonuses": stat_bonuses,
        "buy_price": buy, "sell_price": buy // 4,
        "identified": True, "description": desc,
    }
    if allowed:       item["allowed_classes"] = allowed
    if magic_resist:  item["magic_resist"] = magic_resist
    if speed_mod:     item["speed_mod"] = speed_mod
    if enchant_element:
        item["enchant_element"] = enchant_element
        item["enchant_bonus"] = enchant_bonus
        item["enchant_name"] = enchant_name
    return item

def _acc(name, subtype, slot, stat_bonuses, buy, rarity, desc,
         allowed=None, magic_resist=0, enchant_element=None,
         enchant_bonus=0, enchant_name="", effect=None):
    item = {
        "name": name, "type": "accessory", "slot": slot,
        "subtype": subtype, "rarity": rarity,
        "stat_bonuses": stat_bonuses,
        "buy_price": buy, "sell_price": buy // 4,
        "identified": True, "description": desc,
    }
    if allowed:       item["allowed_classes"] = allowed
    if magic_resist:  item["magic_resist"] = magic_resist
    if enchant_element:
        item["enchant_element"] = enchant_element
        item["enchant_bonus"] = enchant_bonus
        item["enchant_name"] = enchant_name
    if effect:        item["effect"] = effect
    return item


# ══════════════════════════════════════════════════════════════
#  FIGHTER  (STR/CON — swords, axes, maces, heavy armor)
# ══════════════════════════════════════════════════════════════
FIGHTER_WEAPONS = [
    # T1 Common
    _w("Militia Sword", "Longsword", 18, "slashing", {"STR": 1},
       45, "common", "A standard-issue militia longsword. Reliable.",
       damage_stat={"STR": 0.3, "DEX": 0.12}),
    _w("Soldier's Axe", "Axe", 17, "slashing", {"STR": 1},
       40, "common", "A heavy hand axe favored by infantry.",
       damage_stat={"STR": 0.4}),
    _w("Iron Warhammer", "Warhammer", 16, "blunt", {"STR": 1, "CON": 1},
       50, "common", "Slow but devastating against armored foes.",
       damage_stat={"STR": 0.4}),

    # T2 Uncommon
    _w("Steel Longsword", "Longsword", 24, "slashing", {"STR": 2},
       120, "uncommon", "High-carbon steel holds an edge longer. +2 STR.",
       damage_stat={"STR": 0.3, "DEX": 0.12}),
    _w("Battleaxe", "Axe", 27, "slashing", {"STR": 2},
       130, "uncommon", "A true two-hand battleaxe — wide, heavy swings. +2 STR.",
       crit_mod=5,
       damage_stat={"STR": 0.4}),
    _w("Flanged Mace", "Mace", 22, "blunt", {"STR": 1, "CON": 2},
       110, "uncommon", "Flanges punch through armor gaps. +1 STR, +2 CON.",
       damage_stat={"STR": 0.4}),
    _w("Tower Shield Bash", "Shield", 13, "blunt", {"CON": 3},
       95, "uncommon", "Used offensively — ram foes with the shield edge. +3 CON.",
       special="shield_bash",
       damage_stat={"STR": 0.24, "CON": 0.16}),

    # T3 Rare
    _w("Forgemaster's Blade", "Greatsword", 35, "slashing", {"STR": 3},
       280, "rare", "Crafted by a master smith. The balance is perfect. +3 STR.",
       crit_mod=8,
       damage_stat={"STR": 0.4, "DEX": 0.1}),
    _w("Dawnbreaker Axe", "Greataxe", 38, "slashing", {"STR": 3, "CON": 1},
       300, "rare", "An axe so heavy only the strongest can wield it well. +3 STR, +1 CON.",
       enchant_element="fire", enchant_bonus=4, enchant_name="Flame",
       damage_stat={"STR": 0.40}),
    _w("Stonebreaker Hammer", "Warhammer", 32, "blunt", {"STR": 2, "CON": 3},
       260, "rare",
       "Forged to shatter stone — and skulls. +2 STR, +3 CON. Ignores some armor.",
       special="armor_pierce",
       damage_stat={"STR": 0.4}),

    # T4 Epic
    _w("Aldenmere Greatsword", "Greatsword", 48, "slashing", {"STR": 4, "CON": 2},
       500, "epic", "A royal-issue greatsword used by imperial guard captains. +4 STR, +2 CON.",
       crit_mod=10, enchant_element="fire", enchant_bonus=5, enchant_name="Flame",
       damage_stat={"STR": 0.4, "DEX": 0.1}),
    _w("Voidcleaver", "Greataxe", 51, "slashing", {"STR": 5},
       550, "epic", "An axe said to cut the shadow itself. +5 STR. Shadow damage.",
       enchant_element="shadow", enchant_bonus=6, enchant_name="Shadow", crit_mod=12,
       damage_stat={"STR": 0.40}),

    # ── Broadswords (STR + DEX balance) ──────────────────────────────────────
    _w("Iron Broadsword",    "Broadsword", 20, "slashing", {"STR": 1},
       55, "common",   "A heavy wide-bladed sword. Reliable in any hand. +1 STR.",
       damage_stat={"STR": 0.32, "DEX": 0.08}),
    _w("Steel Broadsword",   "Broadsword", 26, "slashing", {"STR": 2, "DEX": 1},
       130, "uncommon", "A well-forged broadsword, balanced for power. +2 STR, +1 DEX.",
       damage_stat={"STR": 0.30, "DEX": 0.10}),
    _w("Knight's Broadsword","Broadsword", 34, "slashing", {"STR": 3, "DEX": 1},
       260, "rare",    "A broadsword fit for a knight — heavy and authoritative. +3 STR, +1 DEX.",
       enchant_element="blunt", enchant_bonus=2, enchant_name="Weighty",
       damage_stat={"STR": 0.32, "DEX": 0.08}),
    _w("Kingsblade",         "Broadsword", 42, "slashing", {"STR": 4, "DEX": 2},
       480, "epic",    "A royal broadsword of legendary make. +4 STR, +2 DEX.",
       enchant_element="divine", enchant_bonus=5, enchant_name="Sovereign",
       damage_stat={"STR": 0.34, "DEX": 0.10}),

    # ── Longsword (rare + epic tier fill) ─────────────────────────────────────
    _w("War Longsword",      "Longsword", 28, "slashing", {"STR": 2, "DEX": 2},
       240, "rare",    "A battle-tested longsword. Long reach, high precision. +2 STR, +2 DEX.",
       accuracy_mod=6, damage_stat={"STR": 0.28, "DEX": 0.14}),
    _w("Dawnbreaker",        "Longsword", 38, "slashing", {"STR": 3, "DEX": 3},
       460, "epic",    "A longsword that catches morning light in its steel. +3 STR, +3 DEX.",
       enchant_element="divine", enchant_bonus=6, enchant_name="Dawnforged",
       damage_stat={"STR": 0.30, "DEX": 0.14}),

    # ── Halberd / Glaive (two-handed polearms) ────────────────────────────────
    _w("Iron Halberd",       "Glaive", 20, "slashing", {"STR": 2, "CON": 1},
       95, "common",   "A pole weapon combining axe, hook, and spear. +2 STR, +1 CON.",
       accuracy_mod=4, damage_stat={"STR": 0.38}),
    _w("War Halberd",        "Glaive", 29, "slashing", {"STR": 3, "CON": 1},
       200, "uncommon", "A heavy halberd favoured by heavy infantry. +3 STR, +1 CON.",
       accuracy_mod=4, damage_stat={"STR": 0.38}),
    _w("Champion's Glaive",  "Glaive", 38, "slashing", {"STR": 4, "CON": 2},
       380, "rare",    "A war glaive bearing the crest of a champion. +4 STR, +2 CON.",
       enchant_element="slashing", enchant_bonus=4, enchant_name="Razored",
       damage_stat={"STR": 0.40}),
    _w("Dragonhewn Glaive",  "Glaive", 50, "slashing", {"STR": 5, "CON": 2},
       550, "epic",    "Said to have split a dragon's scale. +5 STR, +2 CON.",
       enchant_element="fire", enchant_bonus=7, enchant_name="Dragonbane",
       damage_stat={"STR": 0.42}),

    # ── Lance (cavalry / charge weapon) ───────────────────────────────────────
    _w("War Lance",          "Lance", 24, "piercing", {"STR": 2},
       110, "uncommon", "A long cavalry weapon. Devastating on the charge. +2 STR.",
       accuracy_mod=-4, damage_stat={"STR": 0.40}),
    _w("Knight's Lance",     "Lance", 36, "piercing", {"STR": 3, "CON": 1},
       300, "rare",    "A heavy jousting lance reinforced for war. +3 STR, +1 CON.",
       accuracy_mod=-2, damage_stat={"STR": 0.42}),

    # ── Maul (slow, massive two-handed blunt) ─────────────────────────────────
    _w("Stone Maul",         "Warhammer", 26, "blunt", {"STR": 3, "CON": 2},
       160, "uncommon", "A huge stone-headed war maul. Slow but devastating. +3 STR, +2 CON.",
       speed_mod=-2, damage_stat={"STR": 0.44}),
    _w("Titan's Maul",       "Warhammer", 45, "blunt", {"STR": 5, "CON": 3},
       520, "epic",    "A maul forged for a giant. Barely wielded by mortals. +5 STR, +3 CON.",
       speed_mod=-3, enchant_element="blunt", enchant_bonus=8, enchant_name="Earthshaker",
       damage_stat={"STR": 0.46}),

    # ── More Axes ─────────────────────────────────────────────────────────────
    _w("Hand Axe",           "Hand Axe", 13, "slashing", {"STR": 1, "DEX": 1},
       45, "common",   "A light axe, throwable in a pinch. +1 STR, +1 DEX.",
       damage_stat={"STR": 0.28, "DEX": 0.12}),
    _w("Reinforced Hand Axe","Hand Axe", 19, "slashing", {"STR": 2, "DEX": 1},
       100, "uncommon", "A heavier hand axe with an iron-banded haft. +2 STR, +1 DEX.",
       damage_stat={"STR": 0.30, "DEX": 0.10}),
    _w("Champion's Axe",     "Axe",  32, "slashing", {"STR": 4, "CON": 1},
       300, "rare",    "A broad-headed axe, balanced for war. +4 STR, +1 CON.",
       damage_stat={"STR": 0.40}),

    # ── More Maces ────────────────────────────────────────────────────────────
    _w("War Mace",           "Mace", 21, "blunt", {"STR": 2, "CON": 1},
       105, "uncommon", "A heavy spiked mace. Good against armour. +2 STR, +1 CON.",
       damage_stat={"STR": 0.38}),
    _w("Blessed Mace",       "Mace", 30, "blunt", {"STR": 3, "PIE": 1},
       250, "rare",    "A mace consecrated by the temple. Bonus vs undead. +3 STR, +1 PIE.",
       enchant_element="divine", enchant_bonus=4, enchant_name="Consecrated",
       damage_stat={"STR": 0.36, "PIE": 0.06}),
    _w("Titan's Mace",       "Mace", 42, "blunt", {"STR": 5, "CON": 2},
       490, "epic",    "A mace of legendary weight. Dents armour on contact. +5 STR, +2 CON.",
       enchant_element="blunt", enchant_bonus=6, enchant_name="Crushing",
       damage_stat={"STR": 0.42}),

]

FIGHTER_ARMOR = [
    # T1
    _a("Leather Hauberk", "chest", "body", 6, {}, 40, "common",
       "Thick leather over the torso. Basic protection."),
    _a("Iron Helm", "helmet", "head", 4, {"CON": 1}, 35, "common",
       "Standard iron helmet. Dents but holds. +1 CON."),
    _a("Iron Gauntlets", "gloves", "hands", 3, {"STR": 1}, 30, "common",
       "Iron-plated gloves strengthen grip. +1 STR."),

    # T2
    _a("Chainmail Hauberk", "chest", "body", 10, {"CON": 1}, 100, "uncommon",
       "Interlocked rings — good balance of weight and protection. +1 CON."),
    _a("Steel Helm", "helmet", "head", 6, {"CON": 2}, 90, "uncommon",
       "Full-faced steel helm. Heavy but solid. +2 CON."),
    _a("Soldier's Boots", "boots", "feet", 4, {"CON": 1}, 70, "uncommon",
       "Reinforced boots for long campaigns. +1 CON."),

    # T3
    _a("Platemail Hauberk", "chest", "body", 16, {"CON": 2, "STR": 1}, 250, "rare",
       "Heavy plate covering torso and shoulders. +2 CON, +1 STR.",
       speed_mod=-1),
    _a("Warlord's Helm", "helmet", "head", 10, {"CON": 3}, 220, "rare",
       "Imposing full helm with cheek guards. +3 CON.",
       magic_resist=4),
    _a("Vanguard Greaves", "boots", "feet", 7, {"CON": 2}, 180, "rare",
       "Heavy leg armor — painful to the knees but worth it. +2 CON.",
       speed_mod=-1),

    # T4
    _a("Imperial Full Plate", "chest", "body", 22, {"CON": 4, "STR": 2}, 450, "epic",
       "The finest plate armor money can buy. +4 CON, +2 STR.",
       magic_resist=6, speed_mod=-2),
    _a("Crown Guard Helm", "helmet", "head", 14, {"CON": 3, "STR": 1}, 380, "epic",
       "Worn by the Empire's elite guard. +3 CON, +1 STR.",
       magic_resist=8),
]

FIGHTER_ACCESSORIES = [
    _acc("Soldier's Ring", "ring", "ring1", {"STR": 1, "CON": 1}, 60, "common",
         "A plain iron ring engraved with a crossed-swords sigil. +1 STR, +1 CON."),
    _acc("Warrior's Amulet", "amulet", "neck", {"STR": 2}, 100, "uncommon",
         "A bronze amulet worn by veteran soldiers. +2 STR."),
    _acc("Champion's Belt", "ring", "ring1", {"STR": 3, "CON": 2}, 220, "rare",
         "A heavy leather belt reinforced with iron studs. +3 STR, +2 CON."),
    _acc("Ring of the Vanguard", "ring", "ring1", {"STR": 4, "CON": 3}, 400, "epic",
         "Worn by generals who led from the front. +4 STR, +3 CON.",
         magic_resist=5),
]


# ══════════════════════════════════════════════════════════════
#  MAGE  (INT/WIS — staves, wands, orbs, robes)
# ══════════════════════════════════════════════════════════════
MAGE_WEAPONS = [
    # T1
    _w("Apprentice Staff", "Staff", 8, "blunt", {"INT": 1},
       30, "common", "A basic carved staff for apprentice mages. +1 INT.",
       spell_bonus=3,
       damage_stat={"STR": 0.16, "INT": 0.24}),
    _w("Birchwood Wand", "Wand", 5, "blunt", {"INT": 1, "WIS": 1},
       25, "common", "Light wand for directing magical energy. +1 INT, +1 WIS.",
       spell_bonus=2, speed_mod=1,
       damage_stat={"INT": 0.32}),

    # T2
    _w("Arcanist's Staff", "Staff", 11, "blunt", {"INT": 2},
       110, "uncommon", "Carved with runes that amplify spell power. +2 INT.",
       spell_bonus=6,
       damage_stat={"STR": 0.16, "INT": 0.24}),
    _w("Crystal Wand", "Wand", 8, "blunt", {"INT": 2, "WIS": 1},
       100, "uncommon", "A wand tipped with a raw spell crystal. +2 INT, +1 WIS.",
       spell_bonus=5, speed_mod=1,
       damage_stat={"INT": 0.32}),
    _w("Spell Orb", "Orb", 6, "blunt", {"INT": 2, "WIS": 2},
       120, "uncommon", "An off-hand focus that enhances all spells. +2 INT, +2 WIS.",
       spell_bonus=7,
       damage_stat={"INT": 0.24, "WIS": 0.16}),

    # T3
    _w("Runemaster's Staff", "Staff", 16, "blunt", {"INT": 3, "WIS": 1},
       260, "rare", "Covered in layered runes of amplification. +3 INT, +1 WIS.",
       spell_bonus=10, enchant_element="arcane", enchant_bonus=4, enchant_name="Arcane",
       damage_stat={"STR": 0.16, "INT": 0.24}),
    _w("Frostweaver Wand", "Wand", 10, "blunt", {"INT": 3},
       240, "rare", "Channels cold energy into spells. +3 INT. Ice damage bonus.",
       spell_bonus=8, enchant_element="ice", enchant_bonus=5, enchant_name="Frost",
       speed_mod=1,
       damage_stat={"INT": 0.32}),
    _w("Void Orb", "Orb", 8, "blunt", {"INT": 3, "WIS": 2},
       280, "rare", "A dark glass sphere crackling with void energy. +3 INT, +2 WIS.",
       spell_bonus=11, enchant_element="shadow", enchant_bonus=4, enchant_name="Void",
       damage_stat={"INT": 0.24, "WIS": 0.16}),

    # T4
    _w("Archmagus Staff", "Staff", 22, "blunt", {"INT": 5, "WIS": 2},
       500, "epic", "Said to amplify spells beyond normal limits. +5 INT, +2 WIS.",
       spell_bonus=16, enchant_element="arcane", enchant_bonus=7, enchant_name="Arcane",
       damage_stat={"STR": 0.16, "INT": 0.24}),
    _w("Starfire Wand", "Wand", 13, "blunt", {"INT": 4, "WIS": 3},
       480, "epic",
       "A wand that channels celestial fire. +4 INT, +3 WIS. Fire damage.",
       spell_bonus=14, speed_mod=2,
       enchant_element="fire", enchant_bonus=6, enchant_name="Starfire",
       damage_stat={"INT": 0.32}),

    # ── Rods (common → epic) ──────────────────────────────────────────────
    _w("Apprentice Rod", "Rod", 9, "blunt", {"INT": 1},
       35, "common", "A plain iron rod etched with basic sigils. +1 INT.",
       damage_stat={"INT": 0.32}),
    _w("Arcane Rod", "Rod", 14, "blunt", {"INT": 2},
       90, "uncommon", "A runed rod that channels arcane force. +2 INT.",
       damage_stat={"INT": 0.30, "STR": 0.10}),
    _w("Force Rod", "Rod", 20, "blunt", {"INT": 2, "STR": 1},
       180, "rare", "Heavy rod for arcane melee impact. +2 INT, +1 STR.",
       damage_stat={"INT": 0.28, "STR": 0.14}),
    _w("Void Rod", "Rod", 28, "blunt", {"INT": 3, "WIS": 2},
       380, "epic", "A rod of condensed void energy. +3 INT, +2 WIS.",
       spell_bonus=8, damage_stat={"INT": 0.32, "WIS": 0.10}),

    # ── Orbs — expanded progression ───────────────────────────────────────
    _w("Arcane Orb", "Orb", 7, "arcane", {"INT": 1},
       40, "common", "A crystalline orb that focuses arcane thought. +1 INT.",
       damage_stat={"INT": 0.28, "WIS": 0.12}),
    _w("Wisdom Orb", "Orb", 9, "arcane", {"WIS": 2, "INT": 1},
       80, "uncommon", "A jade orb resonant with natural insight. +2 WIS, +1 INT.",
       damage_stat={"WIS": 0.24, "INT": 0.16}),
    _w("Eclipse Orb", "Orb", 14, "arcane", {"INT": 2, "WIS": 2},
       200, "rare", "A dark orb that eclipses both mind and nature. +2 INT, +2 WIS.",
       spell_bonus=6, damage_stat={"INT": 0.22, "WIS": 0.18}),
    _w("Infinity Orb", "Orb", 20, "arcane", {"INT": 3, "WIS": 2, "PIE": 1},
       420, "epic", "A perfect orb containing all schools of magic. +3 INT, +2 WIS, +1 PIE.",
       spell_bonus=10, damage_stat={"INT": 0.20, "WIS": 0.15, "PIE": 0.05}),

    # ── Grimoire ──────────────────────────────────────────────────────────
    _w("Battlemage Grimoire", "Grimoire", 12, "blunt", {"INT": 2, "WIS": 2},
       220, "rare",
       "A tome bound in dragonhide, wielded as a weapon. +2 INT, +2 WIS.",
       spell_bonus=8, damage_stat={"INT": 0.26, "WIS": 0.14}),
]

MAGE_ARMOR = [
    # T1
    _a("Cloth Robes", "robes", "body", 2, {"INT": 1}, 20, "common",
       "Simple robes stitched with minor warding sigils. +1 INT.",
       magic_resist=3),
    _a("Apprentice Hood", "helmet", "head", 1, {"INT": 1}, 18, "common",
       "A hooded cowl worn by magic students. +1 INT.", magic_resist=2),

    # T2
    _a("Runed Robes", "robes", "body", 4, {"INT": 2}, 90, "uncommon",
       "Fabric woven with spell-amplifying thread. +2 INT.", magic_resist=8),
    _a("Spellweave Hood", "helmet", "head", 2, {"INT": 1, "WIS": 1}, 80, "uncommon",
       "A fitted hood that sharpens focus. +1 INT, +1 WIS.", magic_resist=6),
    _a("Scholar's Slippers", "boots", "feet", 2, {"INT": 1}, 60, "uncommon",
       "Soft boots that don't distract from concentration. +1 INT.", speed_mod=1),

    # T3
    _a("Arcane Vestments", "robes", "body", 6, {"INT": 3, "WIS": 1}, 230, "rare",
       "Vestments enchanted by a senior arcanist. +3 INT, +1 WIS.", magic_resist=14),
    _a("Aetheric Cowl", "helmet", "head", 3, {"INT": 2, "WIS": 1}, 200, "rare",
       "A deep cowl that shields the mind from magical interference. +2 INT, +1 WIS.",
       magic_resist=10),

    # T4
    _a("Archmage Regalia", "robes", "body", 8, {"INT": 4, "WIS": 2}, 440, "epic",
       "The formal robes of an archmage. Covered in permanent enchantments. +4 INT, +2 WIS.",
       magic_resist=20),
    _a("Void-Threaded Cowl", "helmet", "head", 4, {"INT": 3, "WIS": 2}, 380, "epic",
       "Woven from thread pulled through a rift. +3 INT, +2 WIS.",
       magic_resist=15),
]

MAGE_ACCESSORIES = [
    _acc("Apprentice Focus Ring", "ring", "ring1", {"INT": 1}, 40, "common",
         "A ring set with a chip of spell crystal. +1 INT."),
    _acc("Scholar's Pendant", "amulet", "neck", {"INT": 2, "WIS": 1}, 90, "uncommon",
         "A pendant worn by wizards of the third circle. +2 INT, +1 WIS.",
         magic_resist=4),
    _acc("Arcanist's Signet", "ring", "ring1", {"INT": 3, "WIS": 2}, 210, "rare",
         "A signet ring that resonates with spell energy. +3 INT, +2 WIS.",
         magic_resist=6),
    _acc("Ring of the Archmage", "ring", "ring1", {"INT": 4, "WIS": 3}, 420, "epic",
         "Worn only by confirmed archmages. +4 INT, +3 WIS.",
         magic_resist=10,
         enchant_element="arcane", enchant_bonus=4, enchant_name="Arcane"),
]


# ══════════════════════════════════════════════════════════════
#  CLERIC  (PIE/WIS — maces, warhammers, holy symbols, medium armor)
# ══════════════════════════════════════════════════════════════
CLERIC_WEAPONS = [
    # T1
    _w("Acolyte's Mace", "Mace", 11, "blunt", {"PIE": 1},
       35, "common", "A plain iron mace blessed by a village priest. +1 PIE.",
       spell_bonus=2,
       damage_stat={"STR": 0.4}),
    _w("Temple Stave", "Staff", 8, "blunt", {"PIE": 1, "WIS": 1},
       30, "common", "A staff carved with the Light's sigil. +1 PIE, +1 WIS.",
       spell_bonus=3,
       damage_stat={"STR": 0.16, "INT": 0.24}),

    # T2
    _w("Blessed Warhammer", "Warhammer", 19, "blunt", {"PIE": 2, "STR": 1},
       115, "uncommon", "Consecrated iron — glows faintly against undead. +2 PIE, +1 STR.",
       enchant_element="divine", enchant_bonus=3, enchant_name="Holy",
       damage_stat={"STR": 0.4}),
    _w("Divine Mace", "Mace", 16, "blunt", {"PIE": 2},
       100, "uncommon", "Etched with prayers to the Light. +2 PIE.",
       spell_bonus=5, enchant_element="divine", enchant_bonus=2, enchant_name="Holy",
       damage_stat={"STR": 0.4}),
    _w("Healing Staff", "Staff", 11, "blunt", {"PIE": 2, "WIS": 2},
       110, "uncommon", "Channels healing power with every swing. +2 PIE, +2 WIS.",
       spell_bonus=6,
       damage_stat={"STR": 0.16, "INT": 0.24}),

    # T3
    _w("Sunfire Warhammer", "Warhammer", 27, "blunt", {"PIE": 3, "STR": 1},
       270, "rare", "Blazes with holy fire against shadow creatures. +3 PIE, +1 STR.",
       enchant_element="divine", enchant_bonus=6, enchant_name="Sunfire",
       spell_bonus=5,
       damage_stat={"STR": 0.4}),
    _w("Archpriest's Mace", "Mace", 22, "blunt", {"PIE": 3, "WIS": 2},
       250, "rare", "Carried by high priests of the Order. +3 PIE, +2 WIS.",
       spell_bonus=9,
       damage_stat={"STR": 0.4}),

    # T4
    _w("Dawnhammer", "Warhammer", 35, "blunt", {"PIE": 5, "STR": 2},
       500, "epic", "The ceremonial hammer of the High Priest. +5 PIE, +2 STR.",
       enchant_element="divine", enchant_bonus=8, enchant_name="Dawnfire",
       spell_bonus=8,
       damage_stat={"STR": 0.4}),
    _w("Radiant Scepter", "Staff", 19, "blunt", {"PIE": 4, "WIS": 4},
       480, "epic", "A scepter that radiates pure divine energy. +4 PIE, +4 WIS.",
       spell_bonus=14, enchant_element="divine", enchant_bonus=6, enchant_name="Radiance",
       damage_stat={"STR": 0.16, "INT": 0.24}),
    # ── Scepters (PIE+INT — divine focus) ──────────────────────────────────
    _w("Initiate's Scepter", "Scepter", 8, "blunt", {"PIE": 1, "INT": 1},
       30, "common", "A short bronze scepter engraved with holy script. +1 PIE, +1 INT.",
       damage_stat={"PIE": 0.30, "INT": 0.15}),
    _w("Holy Scepter", "Scepter", 13, "blunt", {"PIE": 2, "INT": 1},
       90, "uncommon", "A silver scepter crowned with a divine sun emblem. +2 PIE, +1 INT.",
       spell_bonus=4, damage_stat={"PIE": 0.32, "INT": 0.12}),
    _w("Grand Scepter", "Scepter", 20, "blunt", {"PIE": 3, "INT": 2},
       200, "rare", "An ornate ceremonial scepter charged with divine will. +3 PIE, +2 INT.",
       spell_bonus=8, enchant_element="divine", enchant_bonus=3, enchant_name="Sacred",
       damage_stat={"PIE": 0.34, "INT": 0.14}),
    _w("Archpriest's Scepter", "Scepter", 30, "blunt", {"PIE": 4, "WIS": 2, "INT": 2},
       420, "epic", "The scepter of the highest clergy. Radiates divine authority. +4 PIE, +2 WIS, +2 INT.",
       spell_bonus=12, enchant_element="divine", enchant_bonus=6, enchant_name="Consecrated",
       damage_stat={"PIE": 0.35, "WIS": 0.10, "INT": 0.10}),

    # ── Censers (PIE+WIS — holy rites weapons) ──────────────────────────
    _w("Bronze Censer", "Censer", 11, "blunt", {"PIE": 2, "WIS": 1},
       70, "uncommon", "A swinging incense censer, its smoke blessed. +2 PIE, +1 WIS.",
       damage_stat={"PIE": 0.28, "WIS": 0.14}),
    _w("Censer of Devotion", "Censer", 18, "blunt", {"PIE": 3, "WIS": 2},
       180, "rare", "A silver censer of sacred resin. +3 PIE, +2 WIS.",
       spell_bonus=6, enchant_element="divine", enchant_bonus=3, enchant_name="Blessed",
       damage_stat={"PIE": 0.30, "WIS": 0.16}),
    _w("Archpriest's Censer", "Censer", 26, "blunt", {"PIE": 4, "WIS": 3},
       380, "epic", "A golden censer of legendary piety. Fills foes with divine dread. +4 PIE, +3 WIS.",
       spell_bonus=10, enchant_element="divine", enchant_bonus=5, enchant_name="Hallowed",
       damage_stat={"PIE": 0.32, "WIS": 0.18}),

    # ── Sacred Wands (PIE-scaled) ────────────────────────────────────────
    _w("Wand of Mending", "Wand", 7, "arcane", {"PIE": 2},
       40, "common", "A simple wand that channels healing intent. +2 PIE.",
       spell_bonus=4, damage_stat={"PIE": 0.36}),
    _w("Wand of Smiting", "Wand", 13, "arcane", {"PIE": 2, "STR": 1},
       110, "uncommon", "A wand that delivers divine smite strikes. +2 PIE, +1 STR.",
       enchant_element="divine", enchant_bonus=4, enchant_name="Holy",
       damage_stat={"PIE": 0.30, "STR": 0.12}),
    _w("Wand of Divine Fury", "Wand", 22, "arcane", {"PIE": 3, "INT": 1},
       300, "rare", "A wand crackling with righteous energy. +3 PIE, +1 INT.",
       spell_bonus=8, enchant_element="divine", enchant_bonus=6, enchant_name="Radiant",
       damage_stat={"PIE": 0.32, "INT": 0.10}),

    # ── Morning Stars (STR+PIE) ──────────────────────────────────────────
    _w("Iron Morning Star", "Morning Star", 14, "blunt", {"STR": 1, "PIE": 1},
       65, "common", "A spiked iron ball on a chain. +1 STR, +1 PIE.",
       damage_stat={"STR": 0.30, "PIE": 0.14}),
    _w("Silver Morning Star", "Morning Star", 22, "blunt", {"STR": 2, "PIE": 2},
       180, "rare", "A silver-spiked morning star. Blessed metal burns undead. +2 STR, +2 PIE.",
       enchant_element="divine", enchant_bonus=4, enchant_name="Silver-Blessed",
       damage_stat={"STR": 0.28, "PIE": 0.18}),

    # ── Flails (STR+PIE) ─────────────────────────────────────────────────
    _w("Temple Flail", "Flail", 12, "blunt", {"STR": 1, "PIE": 1},
       60, "common", "A weighted flail used in temple defence. +1 STR, +1 PIE.",
       damage_stat={"STR": 0.32, "PIE": 0.12}),
    _w("War Flail", "Flail", 24, "blunt", {"STR": 3, "CON": 1},
       210, "rare", "A battle-hardened flail favoured by crusaders. +3 STR, +1 CON.",
       damage_stat={"STR": 0.40}),
]

CLERIC_ARMOR = [
    # T1
    _a("Initiate's Vestments", "robes", "body", 4, {"PIE": 1}, 35, "common",
       "Simple white cloth robes given to new initiates. +1 PIE.", magic_resist=3),
    _a("Priest's Hood", "helmet", "head", 2, {"WIS": 1}, 28, "common",
       "A cloth hood worn in service to the Light. +1 WIS.", magic_resist=2),

    # T2
    _a("Blessed Chainmail", "chest", "body", 9, {"PIE": 1, "CON": 1}, 110, "uncommon",
       "Chainmail rings blessed by a senior cleric. +1 PIE, +1 CON.", magic_resist=6),
    _a("Templar Helm", "helmet", "head", 5, {"PIE": 1, "CON": 1}, 90, "uncommon",
       "A steel helm engraved with holy scripture. +1 PIE, +1 CON.", magic_resist=4),
    _a("Sanctuary Robes", "robes", "body", 6, {"PIE": 2, "WIS": 1}, 100, "uncommon",
       "For clerics who prefer mobility over heavy plate. +2 PIE, +1 WIS.",
       magic_resist=10),

    # T3
    _a("Order Plate", "chest", "body", 14, {"PIE": 2, "CON": 2}, 240, "rare",
       "The formal armor of a full Cleric of the Order. +2 PIE, +2 CON.", magic_resist=10),
    _a("High Priest's Mitre", "helmet", "head", 4, {"PIE": 3, "WIS": 1}, 210, "rare",
       "A ceremonial helm worn by senior clerics. +3 PIE, +1 WIS.", magic_resist=12),

    # T4
    _a("Radiant Plate", "chest", "body", 18, {"PIE": 3, "CON": 3}, 420, "epic",
       "Plate armor that glows with divine light. +3 PIE, +3 CON.", magic_resist=16),
    _a("Dawn Crown", "helmet", "head", 6, {"PIE": 4, "WIS": 2}, 360, "epic",
       "Worn by archbishops of the Light. +4 PIE, +2 WIS.", magic_resist=18),
]

CLERIC_ACCESSORIES = [
    _acc("Initiate's Holy Symbol", "amulet", "neck", {"PIE": 1}, 30, "common",
         "A plain silver symbol of the Light. +1 PIE.", magic_resist=3),
    _acc("Silver Censer Ring", "ring", "ring1", {"PIE": 2, "WIS": 1}, 85, "uncommon",
         "A ring containing incense ash from the High Temple. +2 PIE, +1 WIS."),
    _acc("Archpriest's Pendant", "amulet", "neck", {"PIE": 3, "WIS": 2}, 200, "rare",
         "Worn by senior clerics who have performed miracles. +3 PIE, +2 WIS.",
         magic_resist=8),
    _acc("Divine Signet", "ring", "ring1", {"PIE": 4, "WIS": 3}, 400, "epic",
         "The ring of office of the High Priest. +4 PIE, +3 WIS.",
         magic_resist=12, enchant_element="divine", enchant_bonus=4, enchant_name="Holy"),
]


# ══════════════════════════════════════════════════════════════
#  THIEF  (DEX/INT — daggers, short swords, light crossbows, light armor)
# ══════════════════════════════════════════════════════════════
THIEF_WEAPONS = [
    # T1
    _w("Street Knife", "Dagger", 10, "piercing", {"DEX": 1},
       20, "common", "A knife from the market district. Everyone has one. +1 DEX.",
       crit_mod=5, speed_mod=1,
       damage_stat={"DEX": 0.4}),
    _w("Pickpocket's Blade", "Dagger", 11, "piercing", {"DEX": 1, "INT": 1},
       25, "common", "Thin enough to hide in a boot. +1 DEX, +1 INT.",
       crit_mod=5, speed_mod=1, accuracy_mod=5,
       damage_stat={"DEX": 0.4}),

    # T2
    _w("Shadow Dagger", "Dagger", 16, "piercing", {"DEX": 2},
       95, "uncommon", "Dark-bladed and whisper-quiet. +2 DEX.",
       crit_mod=10, speed_mod=2,
       enchant_element="shadow", enchant_bonus=3, enchant_name="Shadow",
       damage_stat={"DEX": 0.4}),
    _w("Cutpurse Blade", "Short Sword", 15, "slashing", {"DEX": 2, "INT": 1},
       105, "uncommon", "Favored by guild thieves — fast and balanced. +2 DEX, +1 INT.",
       crit_mod=8, accuracy_mod=5,
       damage_stat={"DEX": 0.28, "STR": 0.12}),
    _w("Light Crossbow", "Crossbow", 19, "piercing", {"DEX": 1},
       90, "uncommon", "Compact crossbow used for ambushes. +1 DEX.",
       range_="ranged", accuracy_mod=8, crit_mod=12,
       damage_stat={"DEX": 0.28, "STR": 0.12}),

    # T3
    _w("Assassin's Blade", "Dagger", 22, "piercing", {"DEX": 3, "INT": 1},
       240, "rare", "A blade used by contract killers. +3 DEX, +1 INT.",
       crit_mod=15, speed_mod=2, accuracy_mod=8,
       enchant_element="shadow", enchant_bonus=4, enchant_name="Shadow",
       damage_stat={"DEX": 0.4}),
    _w("Twin Fang Daggers", "Dagger", 21, "piercing", {"DEX": 3},
       260, "rare", "Matched pair — one in each hand. +3 DEX.",
       crit_mod=18, special="dual_wield",
       damage_stat={"DEX": 0.4}),
    _w("Guild Recurve", "Crossbow", 26, "piercing", {"DEX": 2},
       250, "rare", "A masterwork crossbow from the Thieves' Guild armoury. +2 DEX.",
       range_="ranged", accuracy_mod=12, crit_mod=15,
       damage_stat={"DEX": 0.28, "STR": 0.12}),

    # T4
    _w("Shadowfang", "Dagger", 30, "piercing", {"DEX": 5},
       480, "epic", "A blade that seems to cut from within shadows. +5 DEX.",
       crit_mod=22, speed_mod=3,
       enchant_element="shadow", enchant_bonus=6, enchant_name="Shadowstrike",
       damage_stat={"DEX": 0.4}),
    _w("Guildmaster's Rapier", "Short Sword", 26, "piercing", {"DEX": 4, "INT": 2},
       500, "epic", "The weapon of a Guildmaster — precise as a surgeon. +4 DEX, +2 INT.",
       crit_mod=18, accuracy_mod=12, speed_mod=2,
       damage_stat={"DEX": 0.28, "STR": 0.12}),

    # ── Rapier (DEX-heavy, high crit/accuracy) ────────────────────────────────
    _w("Worn Rapier",        "Rapier", 9, "piercing", {"DEX": 1},
       28, "common",   "A thin, flexible blade. Fast and precise. +1 DEX.",
       crit_mod=8, accuracy_mod=6, speed_mod=1,
       damage_stat={"DEX": 0.44}),
    _w("Dueling Rapier",     "Rapier", 14, "piercing", {"DEX": 2},
       90, "uncommon", "A fencer's rapier with a swept guard. +2 DEX.",
       crit_mod=10, accuracy_mod=8, speed_mod=1,
       damage_stat={"DEX": 0.44}),
    _w("Viper Rapier",       "Rapier", 20, "piercing", {"DEX": 3, "INT": 1},
       210, "rare",    "A rapier etched with serpent scales. Venomous tip. +3 DEX, +1 INT.",
       crit_mod=12, accuracy_mod=10, speed_mod=1,
       enchant_element="nature", enchant_bonus=3, enchant_name="Venomed",
       damage_stat={"DEX": 0.44, "INT": 0.06}),
    _w("Shadowstrike",       "Rapier", 25, "piercing", {"DEX": 4, "INT": 2},
       430, "epic",    "A rapier forged in shadow-steel. Strikes before the eye can follow. +4 DEX, +2 INT.",
       crit_mod=16, accuracy_mod=14, speed_mod=2,
       enchant_element="shadow", enchant_bonus=6, enchant_name="Shadowforged",
       damage_stat={"DEX": 0.46, "INT": 0.08}),

    # ── Saber (DEX+STR curved blade) ─────────────────────────────────────────
    _w("Corsair's Saber",    "Saber", 13, "slashing", {"DEX": 1, "STR": 1},
       50, "common",   "A curved blade favoured by sailors and pirates. +1 DEX, +1 STR.",
       crit_mod=5, damage_stat={"DEX": 0.32, "STR": 0.12}),
    _w("Cutthroat's Saber",  "Saber", 19, "slashing", {"DEX": 2, "STR": 1},
       120, "uncommon", "A saber with a notched blade for disarming. +2 DEX, +1 STR.",
       crit_mod=6, accuracy_mod=4,
       damage_stat={"DEX": 0.32, "STR": 0.12}),
    _w("Pirate's Saber",     "Saber", 27, "slashing", {"DEX": 3, "STR": 2},
       240, "rare",    "A legendary saber from the Eastern Sea routes. +3 DEX, +2 STR.",
       crit_mod=8, accuracy_mod=6,
       enchant_element="slashing", enchant_bonus=3, enchant_name="Keen",
       damage_stat={"DEX": 0.34, "STR": 0.12}),

    # ── Short Sword (fill tiers) ───────────────────────────────────────────────
    _w("Worn Short Sword",   "Short Sword", 8, "slashing", {"DEX": 1},
       18, "common",   "A battered short sword. Gets the job done. +1 DEX.",
       damage_stat={"DEX": 0.36, "STR": 0.08}),
    _w("Assassin's Blade",   "Short Sword", 25, "slashing", {"DEX": 3, "INT": 1},
       210, "rare",    "A short sword with a false edge and fullers. +3 DEX, +1 INT.",
       crit_mod=10, accuracy_mod=6,
       damage_stat={"DEX": 0.40, "STR": 0.08}),

    # ── Hand Crossbow (light, fast) ───────────────────────────────────────────
    _w("Hand Crossbow",      "Crossbow", 14, "piercing", {"DEX": 2},
       70, "common",   "A compact wrist-mounted crossbow. Concealable. +2 DEX.",
       range_="ranged", accuracy_mod=4, speed_mod=1,
       damage_stat={"DEX": 0.36}),
    _w("Assassin's Crossbow","Crossbow", 21, "piercing", {"DEX": 3, "INT": 1},
       170, "uncommon", "A repeating hand crossbow with a venom reservoir. +3 DEX, +1 INT.",
       range_="ranged", accuracy_mod=6, speed_mod=1,
       enchant_element="nature", enchant_bonus=3, enchant_name="Envenomed",
       damage_stat={"DEX": 0.36, "INT": 0.06}),
    _w("Shadow Crossbow",    "Crossbow", 30, "piercing", {"DEX": 4},
       320, "rare",    "A crossbow of shadow-forged steel. Silent, fast, deadly. +4 DEX.",
       range_="ranged", accuracy_mod=10, speed_mod=2, crit_mod=8,
       enchant_element="shadow", enchant_bonus=4, enchant_name="Silenced",
       damage_stat={"DEX": 0.40}),

    # ── Throwing Knife ────────────────────────────────────────────────────────
    _w("Throwing Knife",     "Dagger", 11, "piercing", {"DEX": 2},
       35, "common",   "Balanced for throwing. Works in melee too. +2 DEX.",
       range_="ranged", accuracy_mod=6, speed_mod=2,
       damage_stat={"DEX": 0.42}),
    _w("Balanced Throwing Knife", "Dagger", 17, "piercing", {"DEX": 3},
       110, "uncommon", "Precision-balanced for maximum range and impact. +3 DEX.",
       range_="ranged", accuracy_mod=8, speed_mod=2, crit_mod=6,
       damage_stat={"DEX": 0.44}),

]

THIEF_ARMOR = [
    # T1
    _a("Traveler's Leathers", "chest", "body", 4, {"DEX": 1}, 35, "common",
       "Soft leather — good for moving quietly. +1 DEX.", speed_mod=1),
    _a("Hood and Wrap", "helmet", "head", 2, {"DEX": 1}, 25, "common",
       "Conceals the face while allowing peripheral vision. +1 DEX."),

    # T2
    _a("Shadowstitch Leathers", "chest", "body", 7, {"DEX": 2}, 105, "uncommon",
       "Treated with shadow-ash to muffle movement. +2 DEX.", speed_mod=1),
    _a("Rogue's Cowl", "helmet", "head", 3, {"DEX": 1, "INT": 1}, 90, "uncommon",
       "Fitted hood used by guild operatives. +1 DEX, +1 INT."),
    _a("Softfoot Boots", "boots", "feet", 3, {"DEX": 2}, 80, "uncommon",
       "Padded soles make footsteps nearly silent. +2 DEX.", speed_mod=2),

    # T3
    _a("Assassin's Garb", "chest", "body", 10, {"DEX": 3}, 235, "rare",
       "Full leather suit used by contract killers. +3 DEX.", speed_mod=2),
    _a("Shadowweave Hood", "helmet", "head", 4, {"DEX": 2, "INT": 1}, 200, "rare",
       "Woven from shadow-silk — absorbs light. +2 DEX, +1 INT.",
       enchant_element="shadow", enchant_bonus=3, enchant_name="Shadow"),

    # T4
    _a("Phantom Leathers", "chest", "body", 13, {"DEX": 4, "INT": 1}, 420, "epic",
       "Armor used by the Guild's top operatives. +4 DEX, +1 INT.",
       speed_mod=3, enchant_element="shadow", enchant_bonus=4, enchant_name="Shadow"),
    _a("Shadowmaster's Cowl", "helmet", "head", 5, {"DEX": 3, "INT": 2}, 360, "epic",
       "The hood of a Shadowmaster. +3 DEX, +2 INT.", speed_mod=2),
]

THIEF_ACCESSORIES = [
    _acc("Nimble Fingers Ring", "ring", "ring1", {"DEX": 1}, 35, "common",
         "A ring worn loose for faster hand movements. +1 DEX."),
    _acc("Guild Emblem", "amulet", "neck", {"DEX": 2, "INT": 1}, 80, "uncommon",
         "Marks you as a member of the Thieves' Guild. +2 DEX, +1 INT."),
    _acc("Shadow Signet", "ring", "ring1", {"DEX": 3, "INT": 2}, 200, "rare",
         "A ring used to identify senior guild operatives. +3 DEX, +2 INT.",
         enchant_element="shadow", enchant_bonus=3, enchant_name="Shadow"),
    _acc("Ring of the Phantom", "ring", "ring1", {"DEX": 5, "INT": 2}, 420, "epic",
         "Worn only by the Guild's most feared assassins. +5 DEX, +2 INT.",
         enchant_element="shadow", enchant_bonus=5, enchant_name="Shadow"),
]


# ══════════════════════════════════════════════════════════════
#  RANGER  (DEX/WIS — bows, spears, swords, medium armor)
# ══════════════════════════════════════════════════════════════
RANGER_WEAPONS = [
    # T1
    _w("Scout's Bow", "Shortbow", 13, "piercing", {"DEX": 1},
       35, "common", "A lightweight bow for scouts. +1 DEX.",
       range_="ranged", accuracy_mod=3,
       damage_stat={"DEX": 0.35, "STR": 0.08}),
    _w("Hunting Spear", "Spear", 14, "piercing", {"STR": 1, "DEX": 1},
       38, "common", "A balanced spear for both hunting and fighting. +1 STR, +1 DEX.",
       range_="reach",
       damage_stat={"STR": 0.24, "DEX": 0.16}),

    # T2
    _w("Wildwood Longbow", "Longbow", 21, "piercing", {"DEX": 2},
       115, "uncommon", "Crafted from aged wildwood. +2 DEX.",
       range_="ranged", accuracy_mod=6, crit_mod=5,
       damage_stat={"DEX": 0.35, "STR": 0.08}),
    _w("Tracker's Blade", "Short Sword", 15, "slashing", {"DEX": 1, "WIS": 1},
       100, "uncommon", "Used when the bow won't do. +1 DEX, +1 WIS.",
       damage_stat={"DEX": 0.28, "STR": 0.12}),
    _w("Ironwood Spear", "Spear", 21, "piercing", {"STR": 2, "WIS": 1},
       110, "uncommon", "Hardened ironwood shaft — won't splinter. +2 STR, +1 WIS.",
       range_="reach",
       damage_stat={"STR": 0.24, "DEX": 0.16}),

    # T3
    _w("Composite War Bow", "Longbow", 29, "piercing", {"DEX": 3},
       265, "rare", "A laminated bow with serious draw weight. +3 DEX.",
       range_="ranged", accuracy_mod=10, crit_mod=10,
       enchant_element="nature", enchant_bonus=4, enchant_name="Verdant",
       damage_stat={"DEX": 0.35, "STR": 0.08}),
    _w("Ranger's Glaive", "Spear", 27, "slashing", {"DEX": 2, "WIS": 2},
       250, "rare", "A bladed spear for mid-range control. +2 DEX, +2 WIS.",
       range_="reach",
       damage_stat={"STR": 0.24, "DEX": 0.16}),
    _w("Beastslayer Bow", "Longbow", 26, "piercing", {"DEX": 2, "STR": 1},
       280, "rare", "Designed for large prey. +2 DEX, +1 STR. Extra damage vs beasts.",
       range_="ranged", special="beast_slayer", crit_mod=8,
       damage_stat={"DEX": 0.35, "STR": 0.08}),

    # T4
    _w("Windwhisper Bow", "Longbow", 38, "piercing", {"DEX": 4, "WIS": 2},
       500, "epic", "So precise it seems to anticipate the target. +4 DEX, +2 WIS.",
       range_="ranged", accuracy_mod=15, crit_mod=15,
       enchant_element="nature", enchant_bonus=6, enchant_name="Gale",
       damage_stat={"DEX": 0.35, "STR": 0.08}),
    _w("Thornwood Lance", "Spear", 35, "piercing", {"DEX": 3, "WIS": 3},
       480, "epic", "A living spear — the wood grows and repairs itself. +3 DEX, +3 WIS.",
       range_="reach", enchant_element="nature", enchant_bonus=5, enchant_name="Thorn",
       damage_stat={"STR": 0.24, "DEX": 0.16}),

    # ── Shortbow fill (uncommon→epic) ─────────────────────────────────────────
    _w("Ashwood Shortbow",   "Shortbow", 13, "piercing", {"DEX": 2},
       60, "uncommon", "A shortbow of flexible ashwood. Reliable draw. +2 DEX.",
       range_="ranged", accuracy_mod=6,
       damage_stat={"DEX": 0.36, "STR": 0.06}),
    _w("Forest Shortbow",    "Shortbow", 19, "piercing", {"DEX": 3, "WIS": 1},
       140, "rare",    "Carved from a single piece of living yew. +3 DEX, +1 WIS.",
       range_="ranged", accuracy_mod=8,
       enchant_element="nature", enchant_bonus=3, enchant_name="Living",
       damage_stat={"DEX": 0.36, "WIS": 0.06}),
    _w("Hawk's Shortbow",    "Shortbow", 27, "piercing", {"DEX": 4, "WIS": 2},
       320, "epic",    "A bow of hawk-wing wood that guided every arrow true. +4 DEX, +2 WIS.",
       range_="ranged", accuracy_mod=12, crit_mod=8,
       enchant_element="nature", enchant_bonus=5, enchant_name="Trueflight",
       damage_stat={"DEX": 0.38, "WIS": 0.08}),

    # ── More Longbows ─────────────────────────────────────────────────────────
    _w("Scout's Longbow",    "Longbow", 14, "piercing", {"DEX": 1},
       45, "common",   "A light longbow for scouting in dense terrain. +1 DEX.",
       range_="ranged", accuracy_mod=4,
       damage_stat={"DEX": 0.34, "STR": 0.08}),
    _w("Stormwood Longbow",  "Longbow", 36, "piercing", {"DEX": 4, "WIS": 2},
       400, "epic",    "Heartwood from a storm-struck oak. Lightning-fast release. +4 DEX, +2 WIS.",
       range_="ranged", accuracy_mod=14, crit_mod=8, speed_mod=1,
       enchant_element="lightning", enchant_bonus=6, enchant_name="Stormforged",
       damage_stat={"DEX": 0.38, "WIS": 0.10}),

    # ── Javelin (thrown + melee) ──────────────────────────────────────────────
    _w("Iron Javelin",       "Spear", 15, "piercing", {"STR": 2, "DEX": 1},
       55, "common",   "A throwing spear that works equally well in melee. +2 STR, +1 DEX.",
       range_="ranged", accuracy_mod=4,
       damage_stat={"STR": 0.26, "DEX": 0.16}),
    _w("Weighted Javelin",   "Spear", 22, "piercing", {"STR": 2, "DEX": 2},
       120, "uncommon", "A javelin with a lead-weighted tip for longer throws. +2 STR, +2 DEX.",
       range_="ranged", accuracy_mod=6,
       damage_stat={"STR": 0.24, "DEX": 0.18}),
    _w("Warden Javelin",     "Spear", 32, "piercing", {"STR": 3, "DEX": 3, "WIS": 1},
       280, "rare",    "A javelin engraved with old Warden runes. +3 STR, +3 DEX, +1 WIS.",
       range_="ranged", accuracy_mod=8,
       enchant_element="nature", enchant_bonus=4, enchant_name="Wardenbless'd",
       damage_stat={"STR": 0.24, "DEX": 0.20}),

    # ── Short Sword for Rangers (light melee backup) ──────────────────────────
    _w("Hunter's Blade",     "Short Sword", 12, "slashing", {"DEX": 2, "STR": 1},
       42, "common",   "A wide hunting blade for close-quarters work. +2 DEX, +1 STR.",
       damage_stat={"DEX": 0.32, "STR": 0.12}),
    _w("Ranger's Shortsword","Short Sword", 16, "slashing", {"DEX": 3, "WIS": 1},
       130, "uncommon", "A balanced short sword for the ambush hunter. +3 DEX, +1 WIS.",
       crit_mod=6, damage_stat={"DEX": 0.34, "WIS": 0.08}),
    _w("Stalker's Blade",    "Short Sword", 22, "slashing", {"DEX": 4, "WIS": 2},
       270, "rare",    "A blade that seems to find gaps in armour naturally. +4 DEX, +2 WIS.",
       crit_mod=8, accuracy_mod=6,
       damage_stat={"DEX": 0.36, "WIS": 0.10}),

    # ── Hunting Crossbow ─────────────────────────────────────────────────────
    _w("Hunting Crossbow",   "Crossbow", 18, "piercing", {"DEX": 2, "STR": 1},
       85, "common",   "A crossbow built for hunting large game. +2 DEX, +1 STR.",
       range_="ranged", accuracy_mod=6,
       damage_stat={"DEX": 0.30, "STR": 0.12}),
    _w("War Crossbow",       "Crossbow", 27, "piercing", {"DEX": 3, "STR": 2},
       200, "uncommon", "A heavy military crossbow. Punches through armour. +3 DEX, +2 STR.",
       range_="ranged", accuracy_mod=8,
       damage_stat={"DEX": 0.28, "STR": 0.14}),
    _w("Siege Crossbow",     "Crossbow", 38, "piercing", {"DEX": 4, "STR": 2},
       380, "rare",    "A crossbow powerful enough to pin a man to a wall. +4 DEX, +2 STR.",
       range_="ranged", accuracy_mod=10,
       enchant_element="piercing", enchant_bonus=5, enchant_name="Armorbane",
       damage_stat={"DEX": 0.30, "STR": 0.14}),

]

RANGER_ARMOR = [
    # T1
    _a("Scout Leathers", "chest", "body", 5, {"DEX": 1}, 40, "common",
       "Light leather for scouts in the field. +1 DEX.", speed_mod=1),
    _a("Ranger's Cap", "helmet", "head", 2, {"WIS": 1}, 28, "common",
       "A simple cap that doesn't block peripheral vision. +1 WIS."),

    # T2
    _a("Warden Leathers", "chest", "body", 8, {"DEX": 1, "WIS": 1}, 110, "uncommon",
       "Stiffened leather used by forest wardens. +1 DEX, +1 WIS.", speed_mod=1),
    _a("Pathfinder Hood", "helmet", "head", 3, {"WIS": 2}, 90, "uncommon",
       "A deep hood for tracking in shadow and rain. +2 WIS."),
    _a("Tracker Boots", "boots", "feet", 4, {"DEX": 1, "WIS": 1}, 80, "uncommon",
       "Soft-soled boots for moving through underbrush. +1 DEX, +1 WIS.", speed_mod=1),

    # T3
    _a("Verdant Leathers", "chest", "body", 12, {"DEX": 2, "WIS": 2}, 240, "rare",
       "Ranger armor treated with plant oils for camouflage. +2 DEX, +2 WIS.",
       speed_mod=1),
    _a("Huntmaster's Hood", "helmet", "head", 4, {"WIS": 3}, 210, "rare",
       "Worn by the most senior rangers of the order. +3 WIS.", magic_resist=6),

    # T4
    _a("Wildborn Armor", "chest", "body", 16, {"DEX": 3, "WIS": 3}, 420, "epic",
       "Armor woven from living vines and hardened bark. +3 DEX, +3 WIS.",
       speed_mod=2, magic_resist=8,
       enchant_element="nature", enchant_bonus=4, enchant_name="Growth"),
    _a("Crown of the Forest", "helmet", "head", 5, {"WIS": 4, "DEX": 1}, 360, "epic",
       "A crown of petrified antlers. +4 WIS, +1 DEX.", magic_resist=10),
]

RANGER_ACCESSORIES = [
    _acc("Scout's Ring", "ring", "ring1", {"DEX": 1, "WIS": 1}, 40, "common",
         "A simple ring worn by scouts. +1 DEX, +1 WIS."),
    _acc("Warden's Pendant", "amulet", "neck", {"WIS": 2, "DEX": 1}, 90, "uncommon",
         "A carved bone pendant — a ranger tradition. +2 WIS, +1 DEX."),
    _acc("Ranger's Signet", "ring", "ring1", {"DEX": 2, "WIS": 3}, 210, "rare",
         "Worn by rangers who have earned their full title. +2 DEX, +3 WIS.",
         magic_resist=5),
    _acc("Ring of the Wild", "ring", "ring1", {"DEX": 3, "WIS": 4}, 420, "epic",
         "Bound to the forest itself. +3 DEX, +4 WIS.",
         magic_resist=8, enchant_element="nature", enchant_bonus=4, enchant_name="Wild"),
]


# ══════════════════════════════════════════════════════════════
#  MONK  (WIS/DEX — handwraps, staves, very light armor)
# ══════════════════════════════════════════════════════════════
MONK_WEAPONS = [
    # T1
    _w("Wrappings of Focus", "Handwraps", 10, "blunt", {"WIS": 1, "DEX": 1},
       20, "common", "Simple cloth strips that channel ki through the knuckles. +1 WIS, +1 DEX.",
       speed_mod=2, crit_mod=5,
       damage_stat={"WIS": 0.2, "DEX": 0.2}),
    _w("Quarterstaff", "Staff", 11, "blunt", {"WIS": 1},
       22, "common", "A balanced wooden staff. +1 WIS.",
       speed_mod=1,
       damage_stat={"STR": 0.16, "INT": 0.24}),

    # T2
    _w("Iron Strike Wraps", "Handwraps", 16, "blunt", {"WIS": 2, "DEX": 1},
       95, "uncommon", "Wrapped with iron-thread for harder strikes. +2 WIS, +1 DEX.",
       speed_mod=2, crit_mod=10,
       damage_stat={"WIS": 0.2, "DEX": 0.2}),
    _w("Ironwood Staff", "Staff", 18, "blunt", {"WIS": 2},
       100, "uncommon", "Dense and balanced. +2 WIS.",
       speed_mod=1, crit_mod=5,
       damage_stat={"STR": 0.16, "INT": 0.24}),
    _w("Kama", "Kama", 14, "slashing", {"DEX": 2, "WIS": 1},
       90, "uncommon", "A curved blade mounted on a short handle. +2 DEX, +1 WIS.",
       crit_mod=8, speed_mod=2,
       damage_stat={"DEX": 0.24, "WIS": 0.16}),

    # T3
    _w("Spirit Wrappings", "Handwraps", 22, "blunt", {"WIS": 3, "DEX": 2},
       255, "rare", "Blessed cloth that conducts ki directly. +3 WIS, +2 DEX.",
       speed_mod=3, crit_mod=15,
       enchant_element="divine", enchant_bonus=3, enchant_name="Ki",
       damage_stat={"WIS": 0.2, "DEX": 0.2}),
    _w("Void Staff", "Staff", 24, "blunt", {"WIS": 3, "DEX": 1},
       260, "rare", "A staff carved from shadow-touched wood. +3 WIS, +1 DEX.",
       speed_mod=2, crit_mod=8,
       enchant_element="shadow", enchant_bonus=4, enchant_name="Void",
       damage_stat={"STR": 0.16, "INT": 0.24}),
    _w("Twin Kama", "Kama", 21, "slashing", {"DEX": 3, "WIS": 1},
       270, "rare", "Matched pair — spinning techniques become deadly. +3 DEX, +1 WIS.",
       crit_mod=15, speed_mod=3, special="dual_wield",
       damage_stat={"DEX": 0.24, "WIS": 0.16}),

    # T4
    _w("Celestial Wraps", "Handwraps", 29, "blunt", {"WIS": 5, "DEX": 2},
       490, "epic", "Made from the hide of a celestial beast. +5 WIS, +2 DEX.",
       speed_mod=4, crit_mod=20,
       enchant_element="divine", enchant_bonus=7, enchant_name="Celestial",
       damage_stat={"WIS": 0.2, "DEX": 0.2}),
    _w("Dragon Bone Staff", "Staff", 32, "blunt", {"WIS": 4, "DEX": 3},
       510, "epic", "A staff made from the bones of an elder dragon. +4 WIS, +3 DEX.",
       speed_mod=3, crit_mod=12,
       enchant_element="fire", enchant_bonus=5, enchant_name="Dragonfire",
       damage_stat={"STR": 0.16, "INT": 0.24}),

    # ── Nunchaku (DEX+WIS, fast, multi-hit feel) ──────────────────────────────
    _w("Wooden Nunchaku",    "Kama", 8, "blunt", {"DEX": 1, "WIS": 1},
       22, "common",   "Two hardwood sticks linked by a short chain. +1 DEX, +1 WIS.",
       speed_mod=1, crit_mod=4,
       damage_stat={"DEX": 0.24, "WIS": 0.20}),
    _w("Iron Nunchaku",      "Kama", 13, "blunt", {"DEX": 2, "WIS": 1},
       65, "uncommon", "Iron-weighted nunchaku. Hits harder, spins faster. +2 DEX, +1 WIS.",
       speed_mod=1, crit_mod=6,
       damage_stat={"DEX": 0.26, "WIS": 0.20}),
    _w("Temple Nunchaku",    "Kama", 20, "blunt", {"DEX": 3, "WIS": 2},
       155, "rare",    "Sacred nunchaku carved with meditative scripture. +3 DEX, +2 WIS.",
       speed_mod=1, crit_mod=8, spell_bonus=4,
       enchant_element="arcane", enchant_bonus=3, enchant_name="Focused",
       damage_stat={"DEX": 0.26, "WIS": 0.22}),
    _w("Storm Nunchaku",     "Kama", 30, "blunt", {"DEX": 4, "WIS": 3},
       350, "epic",    "Nunchaku that blur into a storm of strikes. +4 DEX, +3 WIS.",
       speed_mod=2, crit_mod=12, spell_bonus=6,
       enchant_element="lightning", enchant_bonus=5, enchant_name="Stormspun",
       damage_stat={"DEX": 0.28, "WIS": 0.24}),

    # ── Tonfa (STR+WIS, defensive striker) ───────────────────────────────────
    _w("Wooden Tonfa",       "Kama", 9, "blunt", {"STR": 1, "WIS": 1},
       24, "common",   "Side-handled club. Excellent for blocking. +1 STR, +1 WIS.",
       damage_stat={"STR": 0.22, "WIS": 0.22}),
    _w("Iron Tonfa",         "Kama", 15, "blunt", {"STR": 2, "WIS": 1},
       75, "uncommon", "Iron-capped tonfa — a monk's answer to plate armour. +2 STR, +1 WIS.",
       damage_stat={"STR": 0.24, "WIS": 0.22}),
    _w("Jade Tonfa",         "Kama", 24, "blunt", {"STR": 2, "WIS": 3},
       230, "rare",    "Carved jade tonfa — Ki flows through the stone. +2 STR, +3 WIS.",
       spell_bonus=5, damage_stat={"STR": 0.20, "WIS": 0.28}),
    _w("Void Tonfa",         "Kama", 34, "blunt", {"STR": 3, "WIS": 4},
       400, "epic",    "Tonfa etched with void glyphs. Strikes from unexpected angles. +3 STR, +4 WIS.",
       speed_mod=1, spell_bonus=8, crit_mod=8,
       enchant_element="shadow", enchant_bonus=5, enchant_name="Voidtouched",
       damage_stat={"STR": 0.20, "WIS": 0.30}),

    # ── Kama (fill common + epic) ─────────────────────────────────────────────
    _w("Worn Kama",          "Kama", 8, "slashing", {"DEX": 1, "WIS": 1},
       18, "common",   "A farm sickle repurposed as a weapon. Crude but effective. +1 DEX, +1 WIS.",
       damage_stat={"DEX": 0.24, "WIS": 0.20}),
    _w("Dragon Kama",        "Kama", 35, "slashing", {"DEX": 4, "WIS": 4},
       440, "epic",    "Twin kama with dragon-tooth blades. +4 DEX, +4 WIS.",
       crit_mod=12, speed_mod=1,
       enchant_element="fire", enchant_bonus=7, enchant_name="Dragonblessed",
       damage_stat={"DEX": 0.30, "WIS": 0.26}),

    # ── Handwraps (fill rare + more variety) ──────────────────────────────────
    _w("Silk Handwraps",     "Handwraps", 7, "blunt", {"DEX": 1, "WIS": 2},
       20, "common",   "Soft silk wraps that don't restrict movement. +1 DEX, +2 WIS.",
       speed_mod=1, damage_stat={"WIS": 0.28, "DEX": 0.16}),
    _w("Blessed Handwraps",  "Handwraps", 16, "blunt", {"WIS": 2, "PIE": 1},
       100, "uncommon", "Temple-blessed wraps that channel divine Ki. +2 WIS, +1 PIE.",
       spell_bonus=4, damage_stat={"WIS": 0.28, "PIE": 0.10}),
    _w("Iron-Knuckle Wraps", "Handwraps", 22, "blunt", {"STR": 2, "WIS": 2},
       180, "rare",    "Wraps with iron knuckle plates sewn in. +2 STR, +2 WIS.",
       damage_stat={"STR": 0.20, "WIS": 0.24}),

    # ── Staff fill (fill gaps) ────────────────────────────────────────────────
    _w("Battle Staff",       "Staff", 16, "blunt", {"STR": 2, "WIS": 1},
       80, "common",   "A thick iron-capped battle staff for aggressive monks. +2 STR, +1 WIS.",
       damage_stat={"STR": 0.24, "WIS": 0.18}),
    _w("Spirit Staff",       "Staff", 22, "blunt", {"WIS": 3, "DEX": 1},
       160, "uncommon", "A staff resonant with spiritual energy. +3 WIS, +1 DEX.",
       spell_bonus=5, damage_stat={"WIS": 0.28, "DEX": 0.12}),
    _w("Ancestor's Staff",   "Staff", 30, "blunt", {"WIS": 3, "STR": 2},
       290, "rare",    "A staff carved with the faces of revered ancestors. +3 WIS, +2 STR.",
       spell_bonus=6, damage_stat={"WIS": 0.26, "STR": 0.18}),

]

MONK_ARMOR = [
    # T1
    _a("Novice Gi", "robes", "body", 3, {"WIS": 1}, 22, "common",
       "Plain training robes. Allows full range of motion. +1 WIS.", speed_mod=2),
    _a("Meditation Sash", "helmet", "head", 1, {"WIS": 1}, 15, "common",
       "Worn tied around the forehead. +1 WIS."),

    # T2
    _a("Disciple's Gi", "robes", "body", 5, {"WIS": 2, "DEX": 1}, 95, "uncommon",
       "Reinforced training robes. +2 WIS, +1 DEX.", speed_mod=2, magic_resist=4),
    _a("Focused Mind Wrap", "helmet", "head", 2, {"WIS": 2}, 80, "uncommon",
       "A tight wrap to clear the mind in combat. +2 WIS.", magic_resist=4),
    _a("Spirit Sandals", "boots", "feet", 2, {"WIS": 1, "DEX": 1}, 65, "uncommon",
       "Sandals worn by traveling monks. +1 WIS, +1 DEX.", speed_mod=2),

    # T3
    _a("Master's Gi", "robes", "body", 8, {"WIS": 3, "DEX": 1}, 235, "rare",
       "The gi of a fully trained monk. +3 WIS, +1 DEX.", speed_mod=3, magic_resist=8),
    _a("Temple Guardian Band", "helmet", "head", 3, {"WIS": 2, "DEX": 1}, 195, "rare",
       "Worn by monks who guard temples. +2 WIS, +1 DEX.", magic_resist=8),

    # T4
    _a("Transcendence Robes", "robes", "body", 11, {"WIS": 4, "DEX": 2}, 430, "epic",
       "Robes worn by monks who have achieved inner harmony. +4 WIS, +2 DEX.",
       speed_mod=4, magic_resist=14,
       enchant_element="divine", enchant_bonus=4, enchant_name="Ki"),
    _a("Mind's Eye Cowl", "helmet", "head", 4, {"WIS": 4}, 370, "epic",
       "Allows the monk to perceive without sight. +4 WIS.", magic_resist=16),
]

MONK_ACCESSORIES = [
    _acc("Novice Bead Bracelet", "ring", "ring1", {"WIS": 1}, 25, "common",
         "Prayer beads worn around the wrist. +1 WIS."),
    _acc("Spirit Focus Ring", "ring", "ring1", {"WIS": 2, "DEX": 1}, 80, "uncommon",
         "A ring that steadies ki flow. +2 WIS, +1 DEX."),
    _acc("Temple Elder's Pendant", "amulet", "neck", {"WIS": 3, "DEX": 2}, 200, "rare",
         "Given to monks who become elders. +3 WIS, +2 DEX.", magic_resist=6),
    _acc("Ring of Inner Flame", "ring", "ring1", {"WIS": 4, "DEX": 3}, 420, "epic",
         "Burns with a blue ki flame only the wearer can see. +4 WIS, +3 DEX.",
         magic_resist=10, enchant_element="divine", enchant_bonus=4, enchant_name="Ki"),
]


# ══════════════════════════════════════════════════════════════
#  MASTER CATALOG — organized for shop/loot use
# ══════════════════════════════════════════════════════════════

ALL_CLASS_WEAPONS = {
    "Fighter": FIGHTER_WEAPONS,
    "Mage":    MAGE_WEAPONS,
    "Cleric":  CLERIC_WEAPONS,
    "Thief":   THIEF_WEAPONS,
    "Ranger":  RANGER_WEAPONS,
    "Monk":    MONK_WEAPONS,
}

ALL_CLASS_ARMOR = {
    "Fighter": FIGHTER_ARMOR,
    "Mage":    MAGE_ARMOR,
    "Cleric":  CLERIC_ARMOR,
    "Thief":   THIEF_ARMOR,
    "Ranger":  RANGER_ARMOR,
    "Monk":    MONK_ARMOR,
}

ALL_CLASS_ACCESSORIES = {
    "Fighter": FIGHTER_ACCESSORIES,
    "Mage":    MAGE_ACCESSORIES,
    "Cleric":  CLERIC_ACCESSORIES,
    "Thief":   THIEF_ACCESSORIES,
    "Ranger":  RANGER_ACCESSORIES,
    "Monk":    MONK_ACCESSORIES,
}

# Flat lists by rarity tier (for shops / loot tables)
RARITY_ORDER = ["common", "uncommon", "rare", "epic"]

def _by_rarity(catalog, rarity):
    return [i for items in catalog.values() for i in items if i["rarity"] == rarity]

WEAPONS_T1 = _by_rarity(ALL_CLASS_WEAPONS, "common")
WEAPONS_T2 = _by_rarity(ALL_CLASS_WEAPONS, "uncommon")
WEAPONS_T3 = _by_rarity(ALL_CLASS_WEAPONS, "rare")
WEAPONS_T4 = _by_rarity(ALL_CLASS_WEAPONS, "epic")

ARMOR_T1 = _by_rarity(ALL_CLASS_ARMOR, "common")
ARMOR_T2 = _by_rarity(ALL_CLASS_ARMOR, "uncommon")
ARMOR_T3 = _by_rarity(ALL_CLASS_ARMOR, "rare")
ARMOR_T4 = _by_rarity(ALL_CLASS_ARMOR, "epic")

ACCESSORIES_T1 = _by_rarity(ALL_CLASS_ACCESSORIES, "common")
ACCESSORIES_T2 = _by_rarity(ALL_CLASS_ACCESSORIES, "uncommon")
ACCESSORIES_T3 = _by_rarity(ALL_CLASS_ACCESSORIES, "rare")
ACCESSORIES_T4 = _by_rarity(ALL_CLASS_ACCESSORIES, "epic")


def get_shop_weapons(town_tier, party_classes=None):
    """Return weapons appropriate for a shop at a given town tier.
    Filters to classes present in party if provided.
    town_tier: 'village', 'town', 'city', 'capital'
    """
    tier_pools = {
        "village": WEAPONS_T1,
        "town":    WEAPONS_T1 + WEAPONS_T2,
        "city":    WEAPONS_T2 + WEAPONS_T3,
        "capital": WEAPONS_T3 + WEAPONS_T4,
    }
    pool = tier_pools.get(town_tier, WEAPONS_T1)
    if not party_classes:
        return pool
    # Include items with no class restriction, or matching a party class
    return [
        i for i in pool
        if not i.get("allowed_classes") or
           any(c in i.get("allowed_classes", []) for c in party_classes)
    ]


def get_shop_armor(town_tier, party_classes=None):
    """Return armor appropriate for a shop at a given town tier."""
    tier_pools = {
        "village": ARMOR_T1,
        "town":    ARMOR_T1 + ARMOR_T2,
        "city":    ARMOR_T2 + ARMOR_T3,
        "capital": ARMOR_T3 + ARMOR_T4,
    }
    pool = tier_pools.get(town_tier, ARMOR_T1)
    if not party_classes:
        return pool
    return [
        i for i in pool
        if not i.get("allowed_classes") or
           any(c in i.get("allowed_classes", []) for c in party_classes)
    ]


def get_shop_accessories(town_tier, party_classes=None):
    """Return accessories appropriate for a shop at a given town tier."""
    tier_pools = {
        "village": ACCESSORIES_T1,
        "town":    ACCESSORIES_T1 + ACCESSORIES_T2,
        "city":    ACCESSORIES_T2 + ACCESSORIES_T3,
        "capital": ACCESSORIES_T3 + ACCESSORIES_T4,
    }
    pool = tier_pools.get(town_tier, ACCESSORIES_T1)
    if not party_classes:
        return pool
    return [
        i for i in pool
        if not i.get("allowed_classes") or
           any(c in i.get("allowed_classes", []) for c in party_classes)
    ]


def get_class_equipment(class_name, rarity="uncommon"):
    """Get a list of weapons, armor, and accessories for a specific class at a given rarity."""
    weapons    = [i for i in ALL_CLASS_WEAPONS.get(class_name, [])    if i["rarity"] == rarity]
    armor      = [i for i in ALL_CLASS_ARMOR.get(class_name, [])      if i["rarity"] == rarity]
    accessories= [i for i in ALL_CLASS_ACCESSORIES.get(class_name, []) if i["rarity"] == rarity]
    return weapons, armor, accessories
