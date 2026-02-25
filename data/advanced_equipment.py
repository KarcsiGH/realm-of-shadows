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
       range_="melee", special=None):
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
    _w("Militia Sword", "Longsword", 11, "slashing", {"STR": 1},
       45, "common", "A standard-issue militia longsword. Reliable."),
    _w("Soldier's Axe", "Axe", 12, "slashing", {"STR": 1},
       40, "common", "A heavy hand axe favored by infantry."),
    _w("Iron Warhammer", "Warhammer", 10, "blunt", {"STR": 1, "CON": 1},
       50, "common", "Slow but devastating against armored foes."),

    # T2 Uncommon
    _w("Steel Longsword", "Longsword", 15, "slashing", {"STR": 2},
       120, "uncommon", "High-carbon steel holds an edge longer. +2 STR."),
    _w("Battleaxe", "Axe", 17, "slashing", {"STR": 2},
       130, "uncommon", "A true two-hand battleaxe — wide, heavy swings. +2 STR.",
       crit_mod=5),
    _w("Flanged Mace", "Mace", 14, "blunt", {"STR": 1, "CON": 2},
       110, "uncommon", "Flanges punch through armor gaps. +1 STR, +2 CON."),
    _w("Tower Shield Bash", "Shield", 8, "blunt", {"CON": 3},
       95, "uncommon", "Used offensively — ram foes with the shield edge. +3 CON.",
       special="shield_bash"),

    # T3 Rare
    _w("Forgemaster's Blade", "Greatsword", 22, "slashing", {"STR": 3},
       280, "rare", "Crafted by a master smith. The balance is perfect. +3 STR.",
       crit_mod=8),
    _w("Dawnbreaker Axe", "Greataxe", 24, "slashing", {"STR": 3, "CON": 1},
       300, "rare", "An axe so heavy only the strongest can wield it well. +3 STR, +1 CON.",
       enchant_element="fire", enchant_bonus=4, enchant_name="Flame"),
    _w("Stonebreaker Hammer", "Warhammer", 20, "blunt", {"STR": 2, "CON": 3},
       260, "rare",
       "Forged to shatter stone — and skulls. +2 STR, +3 CON. Ignores some armor.",
       special="armor_pierce"),

    # T4 Epic
    _w("Aldenmere Greatsword", "Greatsword", 30, "slashing", {"STR": 4, "CON": 2},
       500, "epic", "A royal-issue greatsword used by imperial guard captains. +4 STR, +2 CON.",
       crit_mod=10, enchant_element="fire", enchant_bonus=5, enchant_name="Flame"),
    _w("Voidcleaver", "Greataxe", 32, "slashing", {"STR": 5},
       550, "epic", "An axe said to cut the shadow itself. +5 STR. Shadow damage.",
       enchant_element="shadow", enchant_bonus=6, enchant_name="Shadow", crit_mod=12),
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
    _acc("Soldier's Ring", "ring", "accessory1", {"STR": 1, "CON": 1}, 60, "common",
         "A plain iron ring engraved with a crossed-swords sigil. +1 STR, +1 CON."),
    _acc("Warrior's Amulet", "amulet", "accessory2", {"STR": 2}, 100, "uncommon",
         "A bronze amulet worn by veteran soldiers. +2 STR."),
    _acc("Champion's Belt", "ring", "accessory1", {"STR": 3, "CON": 2}, 220, "rare",
         "A heavy leather belt reinforced with iron studs. +3 STR, +2 CON."),
    _acc("Ring of the Vanguard", "ring", "accessory1", {"STR": 4, "CON": 3}, 400, "epic",
         "Worn by generals who led from the front. +4 STR, +3 CON.",
         magic_resist=5),
]


# ══════════════════════════════════════════════════════════════
#  MAGE  (INT/WIS — staves, wands, orbs, robes)
# ══════════════════════════════════════════════════════════════
MAGE_WEAPONS = [
    # T1
    _w("Apprentice Staff", "Staff", 5, "blunt", {"INT": 1},
       30, "common", "A basic carved staff for apprentice mages. +1 INT.",
       spell_bonus=3),
    _w("Birchwood Wand", "Wand", 3, "blunt", {"INT": 1, "WIS": 1},
       25, "common", "Light wand for directing magical energy. +1 INT, +1 WIS.",
       spell_bonus=2, speed_mod=1),

    # T2
    _w("Arcanist's Staff", "Staff", 7, "blunt", {"INT": 2},
       110, "uncommon", "Carved with runes that amplify spell power. +2 INT.",
       spell_bonus=6),
    _w("Crystal Wand", "Wand", 5, "blunt", {"INT": 2, "WIS": 1},
       100, "uncommon", "A wand tipped with a raw spell crystal. +2 INT, +1 WIS.",
       spell_bonus=5, speed_mod=1),
    _w("Spell Orb", "Orb", 4, "blunt", {"INT": 2, "WIS": 2},
       120, "uncommon", "An off-hand focus that enhances all spells. +2 INT, +2 WIS.",
       spell_bonus=7),

    # T3
    _w("Runemaster's Staff", "Staff", 10, "blunt", {"INT": 3, "WIS": 1},
       260, "rare", "Covered in layered runes of amplification. +3 INT, +1 WIS.",
       spell_bonus=10, enchant_element="arcane", enchant_bonus=4, enchant_name="Arcane"),
    _w("Frostweaver Wand", "Wand", 6, "blunt", {"INT": 3},
       240, "rare", "Channels cold energy into spells. +3 INT. Ice damage bonus.",
       spell_bonus=8, enchant_element="ice", enchant_bonus=5, enchant_name="Frost",
       speed_mod=1),
    _w("Void Orb", "Orb", 5, "blunt", {"INT": 3, "WIS": 2},
       280, "rare", "A dark glass sphere crackling with void energy. +3 INT, +2 WIS.",
       spell_bonus=11, enchant_element="shadow", enchant_bonus=4, enchant_name="Void"),

    # T4
    _w("Archmagus Staff", "Staff", 14, "blunt", {"INT": 5, "WIS": 2},
       500, "epic", "Said to amplify spells beyond normal limits. +5 INT, +2 WIS.",
       spell_bonus=16, enchant_element="arcane", enchant_bonus=7, enchant_name="Arcane"),
    _w("Starfire Wand", "Wand", 8, "blunt", {"INT": 4, "WIS": 3},
       480, "epic",
       "A wand that channels celestial fire. +4 INT, +3 WIS. Fire damage.",
       spell_bonus=14, speed_mod=2,
       enchant_element="fire", enchant_bonus=6, enchant_name="Starfire"),
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
    _acc("Apprentice Focus Ring", "ring", "accessory1", {"INT": 1}, 40, "common",
         "A ring set with a chip of spell crystal. +1 INT."),
    _acc("Scholar's Pendant", "amulet", "accessory2", {"INT": 2, "WIS": 1}, 90, "uncommon",
         "A pendant worn by wizards of the third circle. +2 INT, +1 WIS.",
         magic_resist=4),
    _acc("Arcanist's Signet", "ring", "accessory1", {"INT": 3, "WIS": 2}, 210, "rare",
         "A signet ring that resonates with spell energy. +3 INT, +2 WIS.",
         magic_resist=6),
    _acc("Ring of the Archmage", "ring", "accessory1", {"INT": 4, "WIS": 3}, 420, "epic",
         "Worn only by confirmed archmages. +4 INT, +3 WIS.",
         magic_resist=10,
         enchant_element="arcane", enchant_bonus=4, enchant_name="Arcane"),
]


# ══════════════════════════════════════════════════════════════
#  CLERIC  (PIE/WIS — maces, warhammers, holy symbols, medium armor)
# ══════════════════════════════════════════════════════════════
CLERIC_WEAPONS = [
    # T1
    _w("Acolyte's Mace", "Mace", 7, "blunt", {"PIE": 1},
       35, "common", "A plain iron mace blessed by a village priest. +1 PIE.",
       spell_bonus=2),
    _w("Temple Stave", "Staff", 5, "blunt", {"PIE": 1, "WIS": 1},
       30, "common", "A staff carved with the Light's sigil. +1 PIE, +1 WIS.",
       spell_bonus=3),

    # T2
    _w("Blessed Warhammer", "Warhammer", 12, "blunt", {"PIE": 2, "STR": 1},
       115, "uncommon", "Consecrated iron — glows faintly against undead. +2 PIE, +1 STR.",
       enchant_element="divine", enchant_bonus=3, enchant_name="Holy"),
    _w("Divine Mace", "Mace", 10, "blunt", {"PIE": 2},
       100, "uncommon", "Etched with prayers to the Light. +2 PIE.",
       spell_bonus=5, enchant_element="divine", enchant_bonus=2, enchant_name="Holy"),
    _w("Healing Staff", "Staff", 7, "blunt", {"PIE": 2, "WIS": 2},
       110, "uncommon", "Channels healing power with every swing. +2 PIE, +2 WIS.",
       spell_bonus=6),

    # T3
    _w("Sunfire Warhammer", "Warhammer", 17, "blunt", {"PIE": 3, "STR": 1},
       270, "rare", "Blazes with holy fire against shadow creatures. +3 PIE, +1 STR.",
       enchant_element="divine", enchant_bonus=6, enchant_name="Sunfire",
       spell_bonus=5),
    _w("Archpriest's Mace", "Mace", 14, "blunt", {"PIE": 3, "WIS": 2},
       250, "rare", "Carried by high priests of the Order. +3 PIE, +2 WIS.",
       spell_bonus=9),

    # T4
    _w("Dawnhammer", "Warhammer", 22, "blunt", {"PIE": 5, "STR": 2},
       500, "epic", "The ceremonial hammer of the High Priest. +5 PIE, +2 STR.",
       enchant_element="divine", enchant_bonus=8, enchant_name="Dawnfire",
       spell_bonus=8),
    _w("Radiant Scepter", "Staff", 12, "blunt", {"PIE": 4, "WIS": 4},
       480, "epic", "A scepter that radiates pure divine energy. +4 PIE, +4 WIS.",
       spell_bonus=14, enchant_element="divine", enchant_bonus=6, enchant_name="Radiance"),
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
    _acc("Initiate's Holy Symbol", "amulet", "accessory2", {"PIE": 1}, 30, "common",
         "A plain silver symbol of the Light. +1 PIE.", magic_resist=3),
    _acc("Silver Censer Ring", "ring", "accessory1", {"PIE": 2, "WIS": 1}, 85, "uncommon",
         "A ring containing incense ash from the High Temple. +2 PIE, +1 WIS."),
    _acc("Archpriest's Pendant", "amulet", "accessory2", {"PIE": 3, "WIS": 2}, 200, "rare",
         "Worn by senior clerics who have performed miracles. +3 PIE, +2 WIS.",
         magic_resist=8),
    _acc("Divine Signet", "ring", "accessory1", {"PIE": 4, "WIS": 3}, 400, "epic",
         "The ring of office of the High Priest. +4 PIE, +3 WIS.",
         magic_resist=12, enchant_element="divine", enchant_bonus=4, enchant_name="Holy"),
]


# ══════════════════════════════════════════════════════════════
#  THIEF  (DEX/INT — daggers, short swords, light crossbows, light armor)
# ══════════════════════════════════════════════════════════════
THIEF_WEAPONS = [
    # T1
    _w("Street Knife", "Dagger", 6, "piercing", {"DEX": 1},
       20, "common", "A knife from the market district. Everyone has one. +1 DEX.",
       crit_mod=5, speed_mod=1),
    _w("Pickpocket's Blade", "Dagger", 7, "piercing", {"DEX": 1, "INT": 1},
       25, "common", "Thin enough to hide in a boot. +1 DEX, +1 INT.",
       crit_mod=5, speed_mod=1, accuracy_mod=5),

    # T2
    _w("Shadow Dagger", "Dagger", 10, "piercing", {"DEX": 2},
       95, "uncommon", "Dark-bladed and whisper-quiet. +2 DEX.",
       crit_mod=10, speed_mod=2,
       enchant_element="shadow", enchant_bonus=3, enchant_name="Shadow"),
    _w("Cutpurse Blade", "Short Sword", 11, "slashing", {"DEX": 2, "INT": 1},
       105, "uncommon", "Favored by guild thieves — fast and balanced. +2 DEX, +1 INT.",
       crit_mod=8, accuracy_mod=5),
    _w("Light Crossbow", "Crossbow", 12, "piercing", {"DEX": 1},
       90, "uncommon", "Compact crossbow used for ambushes. +1 DEX.",
       range_="ranged", accuracy_mod=8, crit_mod=12),

    # T3
    _w("Assassin's Blade", "Dagger", 14, "piercing", {"DEX": 3, "INT": 1},
       240, "rare", "A blade used by contract killers. +3 DEX, +1 INT.",
       crit_mod=15, speed_mod=2, accuracy_mod=8,
       enchant_element="shadow", enchant_bonus=4, enchant_name="Shadow"),
    _w("Twin Fang Daggers", "Dagger", 13, "piercing", {"DEX": 3},
       260, "rare", "Matched pair — one in each hand. +3 DEX.",
       crit_mod=18, special="dual_wield"),
    _w("Guild Recurve", "Crossbow", 16, "piercing", {"DEX": 2},
       250, "rare", "A masterwork crossbow from the Thieves' Guild armoury. +2 DEX.",
       range_="ranged", accuracy_mod=12, crit_mod=15),

    # T4
    _w("Shadowfang", "Dagger", 19, "piercing", {"DEX": 5},
       480, "epic", "A blade that seems to cut from within shadows. +5 DEX.",
       crit_mod=22, speed_mod=3,
       enchant_element="shadow", enchant_bonus=6, enchant_name="Shadowstrike"),
    _w("Guildmaster's Rapier", "Short Sword", 18, "piercing", {"DEX": 4, "INT": 2},
       500, "epic", "The weapon of a Guildmaster — precise as a surgeon. +4 DEX, +2 INT.",
       crit_mod=18, accuracy_mod=12, speed_mod=2),
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
    _acc("Nimble Fingers Ring", "ring", "accessory1", {"DEX": 1}, 35, "common",
         "A ring worn loose for faster hand movements. +1 DEX."),
    _acc("Guild Emblem", "amulet", "accessory2", {"DEX": 2, "INT": 1}, 80, "uncommon",
         "Marks you as a member of the Thieves' Guild. +2 DEX, +1 INT."),
    _acc("Shadow Signet", "ring", "accessory1", {"DEX": 3, "INT": 2}, 200, "rare",
         "A ring used to identify senior guild operatives. +3 DEX, +2 INT.",
         enchant_element="shadow", enchant_bonus=3, enchant_name="Shadow"),
    _acc("Ring of the Phantom", "ring", "accessory1", {"DEX": 5, "INT": 2}, 420, "epic",
         "Worn only by the Guild's most feared assassins. +5 DEX, +2 INT.",
         enchant_element="shadow", enchant_bonus=5, enchant_name="Shadow"),
]


# ══════════════════════════════════════════════════════════════
#  RANGER  (DEX/WIS — bows, spears, swords, medium armor)
# ══════════════════════════════════════════════════════════════
RANGER_WEAPONS = [
    # T1
    _w("Scout's Bow", "Shortbow", 8, "piercing", {"DEX": 1},
       35, "common", "A lightweight bow for scouts. +1 DEX.",
       range_="ranged", accuracy_mod=3),
    _w("Hunting Spear", "Spear", 9, "piercing", {"STR": 1, "DEX": 1},
       38, "common", "A balanced spear for both hunting and fighting. +1 STR, +1 DEX.",
       range_="reach"),

    # T2
    _w("Wildwood Longbow", "Longbow", 13, "piercing", {"DEX": 2},
       115, "uncommon", "Crafted from aged wildwood. +2 DEX.",
       range_="ranged", accuracy_mod=6, crit_mod=5),
    _w("Tracker's Blade", "Short Sword", 11, "slashing", {"DEX": 1, "WIS": 1},
       100, "uncommon", "Used when the bow won't do. +1 DEX, +1 WIS."),
    _w("Ironwood Spear", "Spear", 13, "piercing", {"STR": 2, "WIS": 1},
       110, "uncommon", "Hardened ironwood shaft — won't splinter. +2 STR, +1 WIS.",
       range_="reach"),

    # T3
    _w("Composite War Bow", "Longbow", 18, "piercing", {"DEX": 3},
       265, "rare", "A laminated bow with serious draw weight. +3 DEX.",
       range_="ranged", accuracy_mod=10, crit_mod=10,
       enchant_element="nature", enchant_bonus=4, enchant_name="Verdant"),
    _w("Ranger's Glaive", "Spear", 17, "slashing", {"DEX": 2, "WIS": 2},
       250, "rare", "A bladed spear for mid-range control. +2 DEX, +2 WIS.",
       range_="reach"),
    _w("Beastslayer Bow", "Longbow", 16, "piercing", {"DEX": 2, "STR": 1},
       280, "rare", "Designed for large prey. +2 DEX, +1 STR. Extra damage vs beasts.",
       range_="ranged", special="beast_slayer", crit_mod=8),

    # T4
    _w("Windwhisper Bow", "Longbow", 24, "piercing", {"DEX": 4, "WIS": 2},
       500, "epic", "So precise it seems to anticipate the target. +4 DEX, +2 WIS.",
       range_="ranged", accuracy_mod=15, crit_mod=15,
       enchant_element="nature", enchant_bonus=6, enchant_name="Gale"),
    _w("Thornwood Lance", "Spear", 22, "piercing", {"DEX": 3, "WIS": 3},
       480, "epic", "A living spear — the wood grows and repairs itself. +3 DEX, +3 WIS.",
       range_="reach", enchant_element="nature", enchant_bonus=5, enchant_name="Thorn"),
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
    _acc("Scout's Ring", "ring", "accessory1", {"DEX": 1, "WIS": 1}, 40, "common",
         "A simple ring worn by scouts. +1 DEX, +1 WIS."),
    _acc("Warden's Pendant", "amulet", "accessory2", {"WIS": 2, "DEX": 1}, 90, "uncommon",
         "A carved bone pendant — a ranger tradition. +2 WIS, +1 DEX."),
    _acc("Ranger's Signet", "ring", "accessory1", {"DEX": 2, "WIS": 3}, 210, "rare",
         "Worn by rangers who have earned their full title. +2 DEX, +3 WIS.",
         magic_resist=5),
    _acc("Ring of the Wild", "ring", "accessory1", {"DEX": 3, "WIS": 4}, 420, "epic",
         "Bound to the forest itself. +3 DEX, +4 WIS.",
         magic_resist=8, enchant_element="nature", enchant_bonus=4, enchant_name="Wild"),
]


# ══════════════════════════════════════════════════════════════
#  MONK  (WIS/DEX — handwraps, staves, very light armor)
# ══════════════════════════════════════════════════════════════
MONK_WEAPONS = [
    # T1
    _w("Wrappings of Focus", "Handwraps", 6, "blunt", {"WIS": 1, "DEX": 1},
       20, "common", "Simple cloth strips that channel ki through the knuckles. +1 WIS, +1 DEX.",
       speed_mod=2, crit_mod=5),
    _w("Quarterstaff", "Staff", 7, "blunt", {"WIS": 1},
       22, "common", "A balanced wooden staff. +1 WIS.",
       speed_mod=1),

    # T2
    _w("Iron Strike Wraps", "Handwraps", 10, "blunt", {"WIS": 2, "DEX": 1},
       95, "uncommon", "Wrapped with iron-thread for harder strikes. +2 WIS, +1 DEX.",
       speed_mod=2, crit_mod=10),
    _w("Ironwood Staff", "Staff", 11, "blunt", {"WIS": 2},
       100, "uncommon", "Dense and balanced. +2 WIS.",
       speed_mod=1, crit_mod=5),
    _w("Kama", "Kama", 9, "slashing", {"DEX": 2, "WIS": 1},
       90, "uncommon", "A curved blade mounted on a short handle. +2 DEX, +1 WIS.",
       crit_mod=8, speed_mod=2),

    # T3
    _w("Spirit Wrappings", "Handwraps", 14, "blunt", {"WIS": 3, "DEX": 2},
       255, "rare", "Blessed cloth that conducts ki directly. +3 WIS, +2 DEX.",
       speed_mod=3, crit_mod=15,
       enchant_element="divine", enchant_bonus=3, enchant_name="Ki"),
    _w("Void Staff", "Staff", 15, "blunt", {"WIS": 3, "DEX": 1},
       260, "rare", "A staff carved from shadow-touched wood. +3 WIS, +1 DEX.",
       speed_mod=2, crit_mod=8,
       enchant_element="shadow", enchant_bonus=4, enchant_name="Void"),
    _w("Twin Kama", "Kama", 13, "slashing", {"DEX": 3, "WIS": 1},
       270, "rare", "Matched pair — spinning techniques become deadly. +3 DEX, +1 WIS.",
       crit_mod=15, speed_mod=3, special="dual_wield"),

    # T4
    _w("Celestial Wraps", "Handwraps", 18, "blunt", {"WIS": 5, "DEX": 2},
       490, "epic", "Made from the hide of a celestial beast. +5 WIS, +2 DEX.",
       speed_mod=4, crit_mod=20,
       enchant_element="divine", enchant_bonus=7, enchant_name="Celestial"),
    _w("Dragon Bone Staff", "Staff", 20, "blunt", {"WIS": 4, "DEX": 3},
       510, "epic", "A staff made from the bones of an elder dragon. +4 WIS, +3 DEX.",
       speed_mod=3, crit_mod=12,
       enchant_element="fire", enchant_bonus=5, enchant_name="Dragonfire"),
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
    _acc("Novice Bead Bracelet", "ring", "accessory1", {"WIS": 1}, 25, "common",
         "Prayer beads worn around the wrist. +1 WIS."),
    _acc("Spirit Focus Ring", "ring", "accessory1", {"WIS": 2, "DEX": 1}, 80, "uncommon",
         "A ring that steadies ki flow. +2 WIS, +1 DEX."),
    _acc("Temple Elder's Pendant", "amulet", "accessory2", {"WIS": 3, "DEX": 2}, 200, "rare",
         "Given to monks who become elders. +3 WIS, +2 DEX.", magic_resist=6),
    _acc("Ring of Inner Flame", "ring", "accessory1", {"WIS": 4, "DEX": 3}, 420, "epic",
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
