"""
Realm of Shadows — Extended Enemy Factions
All five new factions, wired to story, dungeons, and pixel art.

Factions:
  Fading-Touched Beasts  — wilderness & early dungeons (Act 1+)
  Fallen Wardens         — Shadow Throne (Act 3, floors 3-8)
  Pirates                — Dragon's Tooth (Act 2)
  Imperial Forces        — Roads & Governor's city (Act 2-3)
  Iron Ridge Dwarves     — Abandoned Mine depths (Act 1-2)
"""

from core.combat_config import (
    IMMUNE, RESISTANT, NEUTRAL, VULNERABLE, VERY_VULNERABLE,
    FRONT, MID, BACK,
)


# ── Inline ability helpers (avoid circular import) ──────────
def _ab_damage(name, power, element, desc, target="single_enemy", **kw):
    return {"name": name, "type": "damage", "target": target,
            "power": power, "element": element, "description": desc, **kw}

def _ab_debuff(name, effect, desc, target="single_enemy", **kw):
    return {"name": name, "type": "debuff", "target": target,
            "effect": effect, "description": desc, **kw}

def _ab_buff(name, buff, duration, desc, targets="all_allies", **kw):
    return {"name": name, "type": "buff", "buff": buff,
            "duration": duration, "targets": targets,
            "cost": 0, "resource": "", "desc": desc, **kw}

def _ab_heal(name, power, desc, target="self"):
    return {"name": name, "type": "heal", "target": target,
            "power": power, "description": desc}

def _ab_aoe(name, power, element, desc, **kw):
    return {"name": name, "type": "damage", "target": "aoe_enemy",
            "power": power, "element": element, "description": desc, **kw}


# ── Loot helpers ─────────────────────────────────────────────
def _res(**overrides):
    base = {k: NEUTRAL for k in
            ("piercing","slashing","blunt","fire","ice","lightning",
             "divine","shadow","nature","arcane")}
    base.update(overrides)
    return base

def _coin(lo, hi): return (lo, hi)

_WEAPON_DS = {
    "Dagger":      {"DEX": 0.40},
    "Short Sword": {"DEX": 0.28, "STR": 0.12},
    "Long Sword":  {"STR": 0.30, "DEX": 0.12},
    "Longsword":   {"STR": 0.30, "DEX": 0.12},
    "Broadsword":  {"STR": 0.30, "DEX": 0.12},
    "Greatsword":  {"STR": 0.40, "DEX": 0.10},
    "Axe":         {"STR": 0.40},
    "Greataxe":    {"STR": 0.40},
    "Warhammer":   {"STR": 0.40},
    "Mace":        {"STR": 0.40},
    "Club":        {"STR": 0.40},
    "Staff":       {"STR": 0.16, "INT": 0.24},
    "Wand":        {"INT": 0.32},
    "Orb":         {"INT": 0.24, "WIS": 0.16},
    "Shortbow":    {"DEX": 0.35, "STR": 0.08},
    "Longbow":     {"DEX": 0.35, "STR": 0.08},
    "Crossbow":    {"DEX": 0.28, "STR": 0.12},
    "Spear":       {"STR": 0.24, "DEX": 0.16},
    "Rapier":      {"DEX": 0.40},
    "Cutlass":     {"DEX": 0.28, "STR": 0.12},
    "Saber":       {"DEX": 0.28, "STR": 0.12},
    "Pick":        {"STR": 0.40},
    "Hammer":      {"STR": 0.40},
}

def _item(name, itype, subtype, rarity, dmg_or_def, phys, unid, unid_desc,
          appraised, mat_desc, magic_desc, val, desc, diff=1, **kw):
    d = {"name": name, "type": itype, "subtype": subtype, "rarity": rarity,
         "identify_difficulty": diff,
         "unidentified_name": unid, "unidentified_desc": unid_desc,
         "appraised_name": appraised, "material_desc": mat_desc,
         "magic_desc": magic_desc, "estimated_value": val, "description": desc}
    if itype == "weapon":
        d["damage"] = dmg_or_def + 10  # +10 base to account for stat scaling
        d["phys_type"] = phys
        if "damage_stat" not in kw:
            ds = _WEAPON_DS.get(subtype)
            if ds:
                d["damage_stat"] = ds
    elif itype == "armor":
        d["defense"] = dmg_or_def
    d.update(kw)
    return d

def _drop(chance, item): return {"drop_chance": chance, "item": item}
def _pelt(tier, val):
    return _item(f"Fading-Touched Pelt","material","leather","uncommon",0,None,
                 "Diseased Pelt","A pelt that seems to absorb light.",
                 f"Tier {tier} Fading Pelt",f"Leather infused with Fading corruption. Tier {tier}.",
                 "Fading resonance — not magical but deeply wrong.",val,
                 "A pelt from a creature touched by the Fading. Useful for corruption-resistant gear.",diff=2)


# ═══════════════════════════════════════════════════════════════
#  FACTION 1 — FADING-TOUCHED BEASTS
#  The creatures that fled — or were consumed — by the Fading.
#  First visible signs of the world's decay. Appear above ground
#  and in early dungeons. Story: these are what the goblins ran from.
# ═══════════════════════════════════════════════════════════════

BEAST_ENEMIES = {

    "Fading Wolf": {
        "name": "Fading Wolf",
        "hp": 55, "defense": 4, "magic_resist": 5,
        "stats": {"STR": 11, "DEX": 14, "CON": 9, "INT": 3, "WIS": 4, "PIE": 1},
        "speed_base": 20,
        "attack_damage": 16, "attack_type": "melee", "phys_type": "piercing",
        "accuracy_bonus": 4,
        "preferred_row": FRONT,
        "ai_type": "aggressive",
        "xp_reward": 28, "gold_reward": _coin(0, 2),
        "resistances": _res(shadow=RESISTANT, nature=VULNERABLE, divine=VULNERABLE),
        "status_immunities": ["Poisoned"],
        "abilities": [
            _ab_buff("Fading Howl", "pack_howl", 2,
                     "A wrongly pitched howl that empowers its pack"),
            _ab_damage("Frenzied Lunge", 26, "shadow",
                       "Blurs forward with Fading-enhanced speed",
                       stun_chance=0.15),
        ],
        "loot_table": [
            _drop(0.25, _pelt(1, 12)),
            _drop(0.08, _item("Wolf Fang (Corrupted)","material","bone","uncommon",0,None,
                "Dark Fang","A blackened fang that refuses to break.",
                "Corrupted Wolf Fang","Bone infused with shadow energy.",
                "Shadow resonance.","12",
                "A fang from a Fading-touched wolf. Used in shadow-resistance crafting.",diff=2)),
        ],
        "description_tiers": {
            0: "A wolf whose eyes are hollow pits of grey light. It moves too fast.",
            1: "Fading Wolf",
            2: "Fading Wolf — fast, empowers its pack, shadow-resistant. Nature magic hits hard.",
        },
    },

    "Fading Hound": {
        "name": "Fading Hound",
        "hp": 45, "defense": 2, "magic_resist": 3,
        "stats": {"STR": 9, "DEX": 16, "CON": 7, "INT": 2, "WIS": 3, "PIE": 1},
        "speed_base": 23,
        "attack_damage": 11, "attack_type": "melee", "phys_type": "piercing",
        "accuracy_bonus": 6,
        "preferred_row": FRONT,
        "ai_type": "flanker",
        "pack_tactics": True,
        "xp_reward": 22, "gold_reward": _coin(0, 1),
        "resistances": _res(shadow=RESISTANT, nature=VULNERABLE, divine=VULNERABLE),
        "status_immunities": [],
        "abilities": [
            _ab_debuff("Tendon Tear", {"slow": True, "duration": 2},
                       "Bites through the back of the knee, slowing the target",
                       slow_chance=0.45),
        ],
        "loot_table": [
            _drop(0.18, _pelt(1, 8)),
        ],
        "description_tiers": {
            0: "A hunting dog reduced to grey-black fur and white silence.",
            1: "Fading Hound",
            2: "Fading Hound — fastest enemy in Act 1, hunts in packs, crippling bite.",
        },
    },

    "Fading Boar": {
        "name": "Fading Boar",
        "hp": 145, "defense": 9, "magic_resist": 5,
        "stats": {"STR": 15, "DEX": 7, "CON": 15, "INT": 2, "WIS": 2, "PIE": 1},
        "speed_base": 13,
        "attack_damage": 35, "attack_type": "melee", "phys_type": "slashing",
        "accuracy_bonus": 1,
        "preferred_row": FRONT,
        "ai_type": "aggressive",
        "xp_reward": 38, "gold_reward": _coin(0, 2),
        "resistances": _res(shadow=RESISTANT, nature=VULNERABLE, blunt=RESISTANT),
        "status_immunities": ["Slowed"],
        "abilities": [
            _ab_damage("Gore Charge", 42, "blunt",
                       "Lowers its head and charges through the front line",
                       target="aoe_enemy", armor_shred=2),
        ],
        "loot_table": [
            _drop(0.30, _pelt(1, 14)),
            _drop(0.15, _item("Fading Boar Tusk","material","bone","uncommon",0,None,
                "Twisted Tusk","A tusk grown at a wrong angle through the jaw.",
                "Corrupted Boar Tusk","Dense bone, shadow-infused.",
                "Fading resonance.",15,
                "A tusk from a Fading-touched boar. Extremely dense.",diff=2)),
        ],
        "description_tiers": {
            0: "A massive boar whose tusks have grown back through its own skull. Still alive.",
            1: "Fading Boar",
            2: "Fading Boar — armored, immune to slowing, charge hits the whole front line.",
        },
    },

    "Fading Bear": {
        "name": "Fading Bear",
        "hp": 195, "defense": 13, "magic_resist": 7,
        "stats": {"STR": 18, "DEX": 6, "CON": 18, "INT": 2, "WIS": 3, "PIE": 1},
        "speed_base": 11,
        "attack_damage": 42, "attack_type": "melee", "phys_type": "slashing",
        "accuracy_bonus": 2,
        "preferred_row": FRONT,
        "ai_type": "aggressive",
        "xp_reward": 55, "gold_reward": _coin(0, 3),
        "resistances": _res(shadow=RESISTANT, nature=VULNERABLE, fire=NEUTRAL),
        "status_immunities": ["Stunned", "Slowed"],
        "abilities": [
            _ab_damage("Fading Maul", 52, "shadow",
                       "A blow so heavy it leaves a shadow imprint in the air",
                       stun_chance=0.30, armor_shred=3),
            _ab_buff("Apex Predator", "enrage", 3,
                     "The Fading amplifies its killing drive",
                     targets="self"),
        ],
        "loot_table": [
            _drop(0.35, _pelt(2, 25)),
            _drop(0.12, _item("Fading Bear Claw","material","bone","rare",0,None,
                "Massive Claw","A claw the size of a shortsword, still warm.",
                "Corrupted Bear Claw","Bone and shadow fused.",
                "Strong Fading resonance.",30,
                "A claw from a fully corrupted bear. Rare tier 2 crafting material.",diff=3)),
        ],
        "description_tiers": {
            0: "Something enormous and wrong. Where a bear should be.",
            1: "Fading Bear",
            2: "Fading Bear — elite-tier beast, immune to stun/slow, enrages, can stun your party.",
        },
    },

    "Fading Stag": {
        "name": "Fading Stag",
        "hp": 110, "defense": 6, "magic_resist": 12,
        "stats": {"STR": 12, "DEX": 13, "CON": 11, "INT": 4, "WIS": 5, "PIE": 2},
        "speed_base": 18,
        "attack_damage": 28, "attack_type": "melee", "phys_type": "piercing",
        "accuracy_bonus": 3,
        "preferred_row": FRONT,
        "ai_type": "aggressive",
        "xp_reward": 35, "gold_reward": _coin(0, 2),
        "resistances": _res(shadow=RESISTANT, nature=NEUTRAL, divine=VULNERABLE,
                            arcane=RESISTANT),
        "status_immunities": [],
        "abilities": [
            _ab_aoe("Fading Pulse", 18, "shadow",
                    "The antlers shed waves of grey dissolution energy"),
            _ab_debuff("Dissolution Aura",
                       {"magic_resist_reduction": 8, "duration": 3},
                       "Proximity drains magical defenses"),
        ],
        "loot_table": [
            _drop(0.20, _pelt(2, 18)),
            _drop(0.25, _item("Fading Antler Fragment","material","arcane","uncommon",0,None,
                "Strange Horn","A fragment of antler that feels hollow.",
                "Fading Antler Shard","Bone that channels the Fading.",
                "Moderate Fading resonance — arcane dampening.",20,
                "A shard of antler from a Fading Stag. Drains nearby arcane energy.",diff=3)),
        ],
        "description_tiers": {
            0: "A stag whose antlers have grown into each other, forming a cage around its head.",
            1: "Fading Stag",
            2: "Fading Stag — AOE pulse, drains magic resist. Eerily calm until it charges.",
        },
    },
}


# ═══════════════════════════════════════════════════════════════
#  FACTION 2 — FALLEN WARDENS
#  Former members of the Warden order who followed Valdris,
#  then were consumed by the Shadow. They wear Warden colors.
#  Their abilities are corrupted — wards turned to curses,
#  consecration turned to desecration. Shadow Throne floors 3-8.
# ═══════════════════════════════════════════════════════════════

FALLEN_WARDEN_ENEMIES = {

    "Warden Shade": {
        "name": "Warden Shade",
        "hp": 108, "defense": 8, "magic_resist": 18,
        "stats": {"STR": 9, "DEX": 11, "CON": 8, "INT": 10, "WIS": 9, "PIE": 3},
        "speed_base": 14,
        "attack_damage": 26, "attack_type": "magic", "phys_type": "shadow",
        "accuracy_bonus": 4,
        "preferred_row": MID,
        "ai_type": "caster",
        "xp_reward": 52, "gold_reward": _coin(0, 4),
        "resistances": _res(shadow=RESISTANT, divine=VULNERABLE,
                            piercing=RESISTANT, slashing=RESISTANT),
        "status_immunities": ["Poisoned"],
        "tags": ["undead"],
        "abilities": [
            _ab_damage("Inverted Ward", 24, "shadow",
                       "Turns a ward-mark against its target, dealing shadow damage"),
            _ab_debuff("Ward Decay",
                       {"magic_resist_reduction": 10, "duration": 3},
                       "The Fading seeps through, reducing magical resistance"),
        ],
        "loot_table": [
            _drop(0.12, _item("Warden Fragment","material","arcane","uncommon",0,None,
                "Dim Medallion","A medallion with a half-erased symbol.",
                "Tarnished Warden Medallion","Former Warden insignia.",
                "Faint divine resonance — heavily corrupted.",18,
                "What remains of a Warden's insignia after years in the Shadow.",diff=3)),
        ],
        "description_tiers": {
            0: "A figure in familiar colors — the Warden order's deep blue. Wrong somehow.",
            1: "Warden Shade",
            2: "Warden Shade — former Warden, resists physical, corrupted ward abilities.",
        },
    },

    "Fallen Warden": {
        "name": "Fallen Warden",
        "hp": 165, "defense": 16, "magic_resist": 20,
        "stats": {"STR": 14, "DEX": 9, "CON": 13, "INT": 11, "WIS": 10, "PIE": 4},
        "speed_base": 12,
        "attack_damage": 36, "attack_type": "melee", "phys_type": "shadow",
        "accuracy_bonus": 3,
        "preferred_row": FRONT,
        "ai_type": "tactical",
        "xp_reward": 72, "gold_reward": _coin(0, 6),
        "resistances": _res(shadow=RESISTANT, divine=VULNERABLE,
                            fire=RESISTANT, ice=RESISTANT),
        "status_immunities": ["Poisoned", "Stunned"],
        "abilities": [
            _ab_damage("Oath Strike", 38, "shadow",
                       "A strike infused with a corrupted Warden oath",
                       stun_chance=0.20),
            # Ward Shatter - already defined in core ENEMY_ABILITIES
            "Ward Shatter",
        ],
        "loot_table": [
            _drop(0.20, _item("Fallen Warden's Blade","weapon","Long Sword","uncommon",
                10,"slashing","Dark Longsword","A longsword with ruined ward-marks etched in.",
                "Oathbroken Sword","Former Warden-issue blade.",
                "Shadow enchantment — ward-marks inverted.",50,
                "A sword that once carried Warden blessing. It carries something else now.",
                diff=3, element="shadow")),
            _drop(0.15, _item("Tarnished Warden Seal","material","arcane","rare",0,None,
                "Broken Seal","A seal whose engraving has reversed itself.",
                "Corrupted Warden Seal","Stone that once anchored wards.",
                "Shadow resonance — formerly divine.",35,
                "A Warden's seal, corrupted by prolonged shadow exposure.",diff=4)),
        ],
        "description_tiers": {
            0: "A heavily armored figure in the blue-and-silver of the Warden order. Hollow eyes.",
            1: "Fallen Warden",
            2: "Fallen Warden — elite. Ward Shatter strips your magic resist. Vulnerable to divine.",
        },
    },

    "Dark Consecrator": {
        "name": "Dark Consecrator",
        "hp": 138, "defense": 10, "magic_resist": 24,
        "stats": {"STR": 8, "DEX": 8, "CON": 10, "INT": 12, "WIS": 14, "PIE": 6},
        "speed_base": 11,
        "attack_damage": 30, "attack_type": "magic", "phys_type": "shadow",
        "accuracy_bonus": 3,
        "preferred_row": BACK,
        "ai_type": "support",
        "xp_reward": 68, "gold_reward": _coin(0, 5),
        "resistances": _res(shadow=RESISTANT, divine=VERY_VULNERABLE,
                            arcane=RESISTANT),
        "status_immunities": ["Cursed", "Poisoned"],
        "abilities": [
            _ab_debuff("Dark Consecration",
                       {"damage_taken_boost": 1.35, "divine_vulnerability": True,
                        "duration": 3},
                       "Inverts the blessing rite — targets become susceptible to all damage",
                       target="aoe_enemy"),
            _ab_heal("Shadow Mending", 35,
                     "Channels shadow energy to restore a fallen ally",
                     target="single_ally"),
            _ab_damage("Desecrate", 28, "shadow",
                       "Strips divine protection from the target",
                       armor_shred=2),
        ],
        "loot_table": [
            _drop(0.22, _item("Consecration Tome","weapon","Staff","rare",
                7,"shadow","Black Ritual Book","A book whose pages feel wrong.",
                "Tome of Desecration","Former Warden prayer book, inverted.",
                "Shadow enchantment — divine magic turned inside out.",65,
                "A prayer book whose every invocation now calls shadow.",
                diff=4, element="shadow")),
        ],
        "description_tiers": {
            0: "A robed figure kneeling in shadow, hands moving in ritual patterns.",
            1: "Dark Consecrator",
            2: "Dark Consecrator — former Warden priest, Dark Consecration makes the whole party take more damage.",
        },
    },

    "Oathbreaker Knight": {
        "name": "Oathbreaker Knight",
        "hp": 212, "defense": 20, "magic_resist": 18,
        "stats": {"STR": 17, "DEX": 8, "CON": 16, "INT": 9, "WIS": 9, "PIE": 4},
        "speed_base": 10,
        "attack_damage": 44, "attack_type": "melee", "phys_type": "shadow",
        "accuracy_bonus": 4,
        "preferred_row": FRONT,
        "ai_type": "guardian",
        "xp_reward": 95, "gold_reward": _coin(0, 8),
        "resistances": _res(shadow=RESISTANT, divine=VULNERABLE,
                            fire=RESISTANT, ice=RESISTANT,
                            piercing=RESISTANT, slashing=RESISTANT),
        "status_immunities": ["Stunned", "Slowed", "Poisoned", "Cursed"],
        "abilities": [
            _ab_damage("Oath Shatter", 50, "shadow",
                       "A devastating blow that resonates with broken vows — "
                       "targets with divine abilities take extra damage",
                       stun_chance=0.25, armor_shred=4),
            "Ward Shatter",
            _ab_buff("Unbreakable Will", "sentinel_resolve", 3,
                     "Raises damage reduction from the power of a broken oath",
                     targets="self"),
        ],
        "loot_table": [
            _drop(0.25, _item("Oathbreaker's Plate","armor","Heavy Armor","rare",
                6,None,"Dark Plate","Heavy armor etched with ruined inscriptions.",
                "Oathbreaker's Warden Plate",
                "Warden-forged plate, shadow-treated.",
                "Shadow enchantment — physical resistance, divine weakness.",80,
                "Armor from a Warden who swore the oath and broke it.",diff=4)),
            _drop(0.20, _item("Shattered Oath Fragment","material","arcane","rare",0,None,
                "Glowing Shard","A shard that radiates cold light.",
                "Broken Oath Crystal",
                "Crystallized vow-energy, corrupted.",
                "Both divine and shadow resonance — unstable.",45,
                "A fragment of crystallized broken oath. Key ingredient in shadow-ward crafting.",diff=4)),
        ],
        "description_tiers": {
            0: "A towering knight in blackened Warden plate. The oath-marks are cut out of the armor.",
            1: "Oathbreaker Knight",
            2: "Oathbreaker Knight — elite guard. Immune to most debuffs. Devastating vs divine users.",
        },
    },

    "Shadow Warden": {
        "name": "Shadow Warden",
        "hp": 185, "defense": 14, "magic_resist": 28,
        "stats": {"STR": 13, "DEX": 12, "CON": 14, "INT": 16, "WIS": 14, "PIE": 6},
        "speed_base": 13,
        "attack_damage": 40, "attack_type": "magic", "phys_type": "shadow",
        "accuracy_bonus": 5,
        "preferred_row": BACK,
        "ai_type": "tactical",
        "xp_reward": 88, "gold_reward": _coin(0, 10),
        "resistances": _res(shadow=IMMUNE, divine=VERY_VULNERABLE,
                            arcane=RESISTANT, fire=RESISTANT),
        "status_immunities": ["Stunned", "Slowed", "Cursed", "Poisoned"],
        "abilities": [
            _ab_damage("Void Rite", 38, "shadow",
                       "A full Warden ritual, corrupted to channel void energy",
                       target="aoe_enemy"),
            "Ward Shatter",
            _ab_debuff("Unravel Ward",
                       {"magic_resist_reduction": 15, "duration": 4},
                       "Systematically dismantles magical defenses",
                       target="aoe_enemy"),
            _ab_heal("Shadow Reconstitution", 50,
                     "Draws on shadow energy to rebuild fallen form",
                     target="self"),
        ],
        "loot_table": [
            _drop(0.30, _item("Shadow Warden Staff","weapon","Staff","rare",
                12,"shadow","Black Staff","A staff that seems to consume light.",
                "Staff of Unmade Wards","Warden channel-staff, shadow-bound.",
                "Shadow enchantment — unravels magical defenses.",90,
                "A staff built to channel ward-energy, now doing the opposite.",
                diff=4, element="shadow")),
            _drop(0.20, _item("Shattered Oath Fragment","material","arcane","rare",0,None,
                "Glowing Shard","A shard that radiates cold light.",
                "Broken Oath Crystal","Crystallized vow-energy, corrupted.",
                "Both divine and shadow resonance — unstable.",45,
                "A fragment of crystallized broken oath.",diff=4)),
        ],
        "description_tiers": {
            0: "A figure in Warden robes that seem to move in a wind you cannot feel.",
            1: "Shadow Warden",
            2: "Shadow Warden — high-tier. Immune to shadow, mass ward removal, AOE void rite. Devastated by divine.",
        },
    },
}


# ═══════════════════════════════════════════════════════════════
#  FACTION 3 — PIRATES
#  Dragon's Tooth archipelago — smugglers, treasure hunters,
#  sell-swords hired to guard the ruins. Journal on floor 1
#  reveals they were PAID by a lord from the capital.
#  (Governor covering his tracks on Hearthstone research.)
# ═══════════════════════════════════════════════════════════════

PIRATE_ENEMIES = {

    "Pirate Deckhand": {
        "name": "Pirate Deckhand",
        "hp": 96, "defense": 6, "magic_resist": 2,
        "stats": {"STR": 11, "DEX": 11, "CON": 10, "INT": 5, "WIS": 5, "PIE": 2},
        "speed_base": 15,
        "attack_damage": 24, "attack_type": "melee", "phys_type": "slashing",
        "accuracy_bonus": 2,
        "preferred_row": FRONT,
        "ai_type": "aggressive",
        "xp_reward": 28, "gold_reward": _coin(6, 20),
        "resistances": _res(fire=NEUTRAL, lightning=VULNERABLE),
        "status_immunities": [],
        "abilities": [],
        "loot_table": [
            _drop(0.20, _item("Cutlass","weapon","Short Sword","common",7,"slashing",
                "Sailor's Blade","A curved blade with a salt-pitted edge.",
                "Pirate Cutlass","Light iron, curved for close quarters.",
                "No magical properties.",12,
                "A cutlass worn by someone who's used it. Well-balanced for its class.")),
            _drop(0.15, {"name":"Coin Pouch","type":"consumable","subtype":"gold",
                "rarity":"common","gold_value":(6,18),"identify_difficulty":0,
                "identified":True,"description":"A pouch of assorted coin."}),
        ],
        "description_tiers": {
            0: "A sun-darkened sailor with a blade and no particular caution.",
            1: "Pirate Deckhand",
            2: "Pirate Deckhand — basic melee, weak to lightning, often guards cargo.",
        },
    },

    "Pirate Markswoman": {
        "name": "Pirate Markswoman",
        "hp": 88, "defense": 5, "magic_resist": 3,
        "stats": {"STR": 9, "DEX": 16, "CON": 8, "INT": 7, "WIS": 9, "PIE": 2},
        "speed_base": 18,
        "attack_damage": 26, "attack_type": "ranged", "phys_type": "piercing",
        "accuracy_bonus": 6,
        "preferred_row": BACK,
        "ai_type": "ranged",
        "xp_reward": 32, "gold_reward": _coin(8, 22),
        "resistances": _res(lightning=VULNERABLE),
        "status_immunities": [],
        "abilities": [
            _ab_debuff("Aimed Shot",
                       {"accuracy_reduction": 15, "duration": 2},
                       "Precisely targets the hands — reduces the victim's accuracy",
                       slow_chance=0.0),
        ],
        "loot_table": [
            _drop(0.22, _item("Sea Crossbow","weapon","Shortbow","common",8,"piercing",
                "Compact Crossbow","A short crossbow built for use on a ship deck.",
                "Pirate Crossbow","Saltwood and iron. Weatherproofed.",
                "No magical properties.",18,
                "A crossbow designed for accuracy at short range in cramped conditions.")),
        ],
        "description_tiers": {
            0: "A woman perched on anything high, crossbow already aimed.",
            1: "Pirate Markswoman",
            2: "Pirate Markswoman — accurate, debilitating shot, dangerous from back row.",
        },
    },

    "Pirate Witch Doctor": {
        "name": "Pirate Witch Doctor",
        "hp": 80, "defense": 4, "magic_resist": 14,
        "stats": {"STR": 6, "DEX": 9, "CON": 7, "INT": 13, "WIS": 12, "PIE": 8},
        "speed_base": 12,
        "attack_damage": 26, "attack_type": "magic", "phys_type": "nature",
        "accuracy_bonus": 3,
        "preferred_row": BACK,
        "ai_type": "support",
        "xp_reward": 40, "gold_reward": _coin(10, 28),
        "resistances": _res(nature=RESISTANT, fire=VULNERABLE),
        "status_immunities": ["Poisoned"],
        "abilities": [
            _ab_debuff("Hex Doll",
                       {"damage_taken_boost": 1.30, "duration": 3},
                       "Binds a hex doll — target takes 30% more damage"),
            _ab_heal("Crude Remedy", 28,
                     "Applies island medicine to restore an ally",
                     target="single_ally"),
            _ab_damage("Venom Spray", 22, "nature",
                       "Sprays venom harvested from island fauna",
                       target="aoe_enemy", apply_poison="poison_weak"),
        ],
        "loot_table": [
            _drop(0.25, _item("Witch Doctor's Fetish","weapon","Staff","uncommon",
                5,"nature","Bone-and-feather Staff","A staff bound with feathers and carved bone.",
                "Venom Channel","Islewood and venom-bone.",
                "Nature enchantment — amplifies poison.",35,
                "A witch doctor's focus staff. Smells of something you can't identify.")),
            _drop(0.20, _item("Venom Sac","material","nature","uncommon",0,None,
                "Pulsing Sac","A small sac that throbs on its own.",
                "Island Venom Sac","Concentrated island creature venom.",
                "Nature resonance — toxic.",20,
                "A harvested venom sac. Tier 1 poison crafting material.",diff=2)),
        ],
        "description_tiers": {
            0: "A pirate with a staff of bone and feather, muttering in a dialect you don't know.",
            1: "Pirate Witch Doctor",
            2: "Pirate Witch Doctor — hexes, heals, poisons. Kill before they hex your tank.",
        },
    },

    "Pirate First Mate": {
        "name": "Pirate First Mate",
        "hp": 148, "defense": 12, "magic_resist": 6,
        "stats": {"STR": 14, "DEX": 13, "CON": 13, "INT": 8, "WIS": 7, "PIE": 3},
        "speed_base": 17,
        "attack_damage": 36, "attack_type": "melee", "phys_type": "slashing",
        "accuracy_bonus": 4,
        "preferred_row": FRONT,
        "ai_type": "tactical",
        "xp_reward": 58, "gold_reward": _coin(22, 55),
        "resistances": _res(lightning=VULNERABLE),
        "status_immunities": [],
        "abilities": [
            _ab_damage("Boarding Strike", 40, "slashing",
                       "A vicious combo attack practiced for ship boarding",
                       stun_chance=0.20, target="single_enemy"),
            _ab_buff("Crew Rally", "war_cry", 3,
                     "Rallies pirates to fight harder",
                     targets="all_allies"),
        ],
        "loot_table": [
            _drop(0.30, _item("First Mate's Saber","weapon","Long Sword","uncommon",
                11,"slashing","Fine Curved Blade","A well-kept blade with notches for confirmed kills.",
                "Boarding Saber","Light steel, edge-weighted.",
                "No magical properties.",40,
                "A saber worn by someone who's fought on more than one ship deck.")),
            _drop(0.20, {"name":"Coin Pouch","type":"consumable","subtype":"gold",
                "rarity":"uncommon","gold_value":(20,55),"identify_difficulty":0,
                "identified":True,"description":"A first mate's cut."}),
        ],
        "description_tiers": {
            0: "A scarred figure with a notched blade and a commanding voice.",
            1: "Pirate First Mate",
            2: "Pirate First Mate — rallies crew, boarding combo, significant gold drop.",
        },
    },

    "Pirate Captain": {
        "name": "Pirate Captain",
        "hp": 185, "defense": 15, "magic_resist": 9,
        "stats": {"STR": 15, "DEX": 14, "CON": 14, "INT": 11, "WIS": 9, "PIE": 4},
        "speed_base": 16,
        "attack_damage": 44, "attack_type": "melee", "phys_type": "slashing",
        "accuracy_bonus": 5,
        "preferred_row": FRONT,
        "ai_type": "tactical",
        "xp_reward": 88, "gold_reward": _coin(45, 110),
        "resistances": _res(lightning=VULNERABLE),
        "status_immunities": ["Stunned"],
        "abilities": [
            _ab_damage("Cutlass Flourish", 48, "slashing",
                       "A blindingly fast sequence of strikes",
                       stun_chance=0.15, target="single_enemy"),
            _ab_buff("Dead Man's Resolve", "war_cry", 4,
                     "A captain's last-stand declaration that empowers the whole crew",
                     targets="all_allies"),
            _ab_debuff("Mark the Weakest",
                       {"damage_taken_boost": 1.40, "duration": 3},
                       "Identifies a party member as the priority target"),
        ],
        "loot_table": [
            _drop(0.35, _item("Captain's Plunder Sword","weapon","Long Sword","rare",
                13,"slashing","Ornate Blade",
                "A sword too fine for a pirate to own legitimately.",
                "Stolen Naval Sword","Naval-issue fine steel.",
                "No magical properties — but excellently crafted.",70,
                "A naval officer's sword. This pirate came from somewhere.")),
            _drop(0.25, {"name":"Coin Pouch","type":"consumable","subtype":"gold",
                "rarity":"rare","gold_value":(45,110),"identify_difficulty":0,
                "identified":True,"description":"A captain's cut. Substantial."}),
            _drop(0.18, _item("Commission Letter","quest_item","document","uncommon",0,None,
                "Sealed Letter","A letter bearing an Imperial-adjacent seal.",
                "Governor's Commission",
                "Written on official paper with an unofficial seal.",
                "Unusual — official seal but no Imperial registry mark.",30,
                "A letter commissioning this crew to 'discourage visitors' to Dragon's Tooth. "
                "The seal looks like the Governor's office. The signature is encoded.",diff=3)),
        ],
        "description_tiers": {
            0: "A tall figure in a coat too fine for a cave. Watching you with professional interest.",
            1: "Pirate Captain",
            2: "Pirate Captain — miniboss. Empowers crew, marks a target, significant loot. That letter is worth finding.",
        },
    },
}


# ═══════════════════════════════════════════════════════════════
#  FACTION 4 — IMPERIAL FORCES
#  The Governor's agents. Appear in Act 2 on roads near Thornhaven,
#  and as dungeon guards once the party exposes the Governor.
#  The Inquisitor is the only enemy in the game who argues a
#  morally coherent case for stopping you.
# ═══════════════════════════════════════════════════════════════

IMPERIAL_ENEMIES = {

    "Imperial Soldier": {
        "name": "Imperial Soldier",
        "hp": 132, "defense": 14, "magic_resist": 5,
        "stats": {"STR": 13, "DEX": 10, "CON": 12, "INT": 7, "WIS": 7, "PIE": 4},
        "speed_base": 13,
        "attack_damage": 30, "attack_type": "melee", "phys_type": "slashing",
        "accuracy_bonus": 3,
        "preferred_row": FRONT,
        "ai_type": "aggressive",
        "xp_reward": 42, "gold_reward": _coin(12, 28),
        "resistances": _res(),
        "status_immunities": [],
        "abilities": [
            _ab_buff("Shield Wall", "sentinel_resolve", 2,
                     "Locks shields with adjacent soldiers",
                     targets="all_allies"),
        ],
        "loot_table": [
            _drop(0.18, _item("Imperial Sword","weapon","Long Sword","common",
                9,"slashing","Regulation Blade","A sword stamped with the Imperial mark.",
                "Standard Imperial Longsword","Mass-produced Imperial steel.",
                "No magical properties.",22,
                "Standard issue. Well made. They give these to everyone.")),
            _drop(0.12, _item("Imperial Coin","consumable","gold","common",0,None,
                "Coin","A coin with the Emperor's face.",
                "Imperial Gold Coin","Standard Imperial currency.",
                "No magical properties.",10,
                "Worth more in some places than others.")),
        ],
        "description_tiers": {
            0: "A soldier in Imperial blue and gold, bearing the Governor's seal.",
            1: "Imperial Soldier",
            2: "Imperial Soldier — disciplined, Shield Wall buffs allies. They're just doing their job.",
        },
    },

    "Imperial Archer": {
        "name": "Imperial Archer",
        "hp": 108, "defense": 8, "magic_resist": 4,
        "stats": {"STR": 9, "DEX": 15, "CON": 9, "INT": 8, "WIS": 9, "PIE": 4},
        "speed_base": 16,
        "attack_damage": 24, "attack_type": "ranged", "phys_type": "piercing",
        "accuracy_bonus": 6,
        "preferred_row": BACK,
        "ai_type": "ranged",
        "xp_reward": 36, "gold_reward": _coin(10, 24),
        "resistances": _res(),
        "status_immunities": [],
        "abilities": [
            _ab_debuff("Suppression Fire",
                       {"accuracy_reduction": 20, "duration": 2},
                       "Volley of arrows forces the party to take cover",
                       target="aoe_enemy"),
        ],
        "loot_table": [
            _drop(0.18, _item("Imperial Shortbow","weapon","Shortbow","common",
                7,"piercing","Regulation Bow","A bow stamped with the Imperial mark.",
                "Standard Imperial Shortbow","Imperial-issue yew shortbow.",
                "No magical properties.",20,
                "Better than most. The Empire maintains its equipment.")),
        ],
        "description_tiers": {
            0: "An archer in light Imperial colors, moving to high ground.",
            1: "Imperial Archer",
            2: "Imperial Archer — suppression fire debuffs the whole party. Clear the back row first.",
        },
    },

    "Imperial Court Mage": {
        "name": "Imperial Court Mage",
        "hp": 95, "defense": 6, "magic_resist": 18,
        "stats": {"STR": 5, "DEX": 9, "CON": 7, "INT": 16, "WIS": 11, "PIE": 5},
        "speed_base": 12,
        "attack_damage": 40, "attack_type": "magic", "phys_type": "arcane",
        "accuracy_bonus": 5,
        "preferred_row": BACK,
        "ai_type": "caster",
        "xp_reward": 56, "gold_reward": _coin(14, 35),
        "resistances": _res(arcane=RESISTANT),
        "status_immunities": [],
        "abilities": [
            _ab_aoe("Arcane Suppression", 28, "arcane",
                    "Blanket arcane field that disrupts enemy casting"),
            _ab_damage("Imperial Bind", 34, "arcane",
                       "Chains of arcane force immobilize a target",
                       stun_chance=0.35),
        ],
        "loot_table": [
            _drop(0.22, _item("Imperial Mage Staff","weapon","Staff","uncommon",
                8,"arcane","Blue-banded Staff","A staff with Imperial blue rings.",
                "Arcane Court Staff","Ashwood, Imperial runed.",
                "Arcane enchantment — spell amplification.",40,
                "The Governor's mages carry these. Well-crafted.",diff=2, element="arcane")),
            _drop(0.18, _item("Arcane Containment Crystal","material","arcane","uncommon",0,None,
                "Blue Crystal","A crystal that hums when magic is used nearby.",
                "Suppression Crystal","Arcane-bound containment crystal.",
                "Strong arcane resonance — binding properties.",28,
                "Used in magical suppression barriers. Tier 2 arcane material.",diff=3)),
        ],
        "description_tiers": {
            0: "A mage in Imperial blue robes, looking at you like a problem to be solved.",
            1: "Imperial Court Mage",
            2: "Imperial Court Mage — AOE arcane suppression, binding stun. Not evil. Obedient.",
        },
    },

    "Imperial Inquisitor": {
        "name": "Imperial Inquisitor",
        "hp": 168, "defense": 13, "magic_resist": 14,
        "stats": {"STR": 12, "DEX": 11, "CON": 12, "INT": 13, "WIS": 14, "PIE": 10},
        "speed_base": 14,
        "attack_damage": 38, "attack_type": "melee", "phys_type": "slashing",
        "accuracy_bonus": 4,
        "preferred_row": FRONT,
        "ai_type": "tactical",
        "xp_reward": 80, "gold_reward": _coin(20, 50),
        "resistances": _res(divine=RESISTANT),
        "status_immunities": ["Stunned", "Cursed"],
        "abilities": [
            _ab_damage("Inquisitor's Verdict", 44, "divine",
                       "A judgment strike charged with genuine conviction",
                       stun_chance=0.25),
            _ab_debuff("Suppress Unorthodoxy",
                       {"magic_resist_reduction": 12, "duration": 3},
                       "Identifies and suppresses magical irregularities in the target"),
            _ab_buff("Righteous Cause", "war_cry", 3,
                     "Galvanizes the unit with genuine belief",
                     targets="all_allies"),
        ],
        "loot_table": [
            _drop(0.28, _item("Inquisitor's Seal","material","arcane","rare",0,None,
                "Ornate Seal","A seal of considerable authority.",
                "Imperial Inquisitor's Seal",
                "Gold-plated iron, Imperial insignia.",
                "Faint divine resonance — this person believed.",45,
                "The seal of an Imperial Inquisitor. Could be used or could be evidence.",diff=3)),
            _drop(0.20, _item("Inquisitor's Blade","weapon","Long Sword","uncommon",
                11,"slashing","Fine Official Sword",
                "A sword that has been maintained with religious care.",
                "Inquisitor's Judgment Sword","High-grade Imperial steel.",
                "Divine enchantment — genuine, not institutional.",55,
                "A sword carried by someone who never doubted the cause. It shows.",
                diff=3, element="divine")),
        ],
        "description_tiers": {
            0: "An Imperial official in formal armor, bearing a seal of considerable authority.",
            1: "Imperial Inquisitor",
            2: "Imperial Inquisitor — miniboss. Divine conviction, buffs allies, suppresses magic. "
               "He thinks he's stopping a threat to the Empire. He might not be entirely wrong.",
        },
    },

    "Imperial Commander": {
        "name": "Imperial Commander",
        "hp": 205, "defense": 17, "magic_resist": 10,
        "stats": {"STR": 16, "DEX": 11, "CON": 15, "INT": 12, "WIS": 10, "PIE": 6},
        "speed_base": 13,
        "attack_damage": 46, "attack_type": "melee", "phys_type": "slashing",
        "accuracy_bonus": 5,
        "preferred_row": FRONT,
        "ai_type": "tactical",
        "xp_reward": 105, "gold_reward": _coin(35, 80),
        "resistances": _res(divine=RESISTANT),
        "status_immunities": ["Stunned", "Slowed", "Cursed"],
        "abilities": [
            _ab_damage("Commander's Strike", 52, "slashing",
                       "A strike designed to break formation",
                       stun_chance=0.20, armor_shred=3, target="single_enemy"),
            _ab_buff("Formation Tactics", "war_cry", 4,
                     "The whole unit fights as one",
                     targets="all_allies"),
            _ab_aoe("Imperial Wrath", 36, "slashing",
                    "A sweeping blow that hits the entire enemy line"),
        ],
        "loot_table": [
            _drop(0.30, _item("Commander's Longsword","weapon","Long Sword","rare",
                14,"slashing","Commander's Sword",
                "A sword too fine for field use that has clearly seen field use.",
                "Imperial Commander's Blade","High-grade Imperial forging.",
                "No magical properties — doesn't need any.",75,
                "A commander's sword. This person earned it.")),
            _drop(0.22, _item("Imperial Command Seal","quest_item","document","rare",0,None,
                "High-authority Seal","A seal of the Governor's direct command.",
                "Governor's Direct Order Seal",
                "Gold Imperial seal with personal authorization.",
                "The Governor's direct signature.",60,
                "A sealed order directly from the Governor. This is what you needed.",diff=3)),
        ],
        "description_tiers": {
            0: "A tall figure in full Imperial regalia. Officers move differently from soldiers.",
            1: "Imperial Commander",
            2: "Imperial Commander — elite. Formation Tactics is a party-wide buff. Has evidence on him.",
        },
    },
}


# ═══════════════════════════════════════════════════════════════
#  FACTION 5 — IRON RIDGE DWARVES
#  The miners and Wardens who died in the Abandoned Mine when
#  Valdris's people came. Korrath's chapter, now bound to the
#  vault they died protecting. The mine has dwarven stonework
#  and dwarven wards — these enemies give it its own identity.
# ═══════════════════════════════════════════════════════════════

DWARF_ENEMIES = {

    "Iron Ridge Shade": {
        "name": "Iron Ridge Shade",
        "hp": 85, "defense": 4, "magic_resist": 16,
        "stats": {"STR": 8, "DEX": 12, "CON": 7, "INT": 7, "WIS": 6, "PIE": 4},
        "speed_base": 16,
        "attack_damage": 22, "attack_type": "magic", "phys_type": "shadow",
        "accuracy_bonus": 3,
        "preferred_row": MID,
        "ai_type": "aggressive",
        "xp_reward": 32, "gold_reward": _coin(0, 3),
        "resistances": _res(shadow=RESISTANT, divine=VULNERABLE,
                            piercing=RESISTANT, slashing=RESISTANT),
        "status_immunities": ["Poisoned"],
        "tags": ["undead"],
        "abilities": [
            _ab_debuff("Miner's Curse",
                       {"accuracy_reduction": 12, "duration": 2},
                       "The ghost of a miner's frustration settles over a target"),
        ],
        "loot_table": [
            _drop(0.15, _item("Iron Ridge Token","material","arcane","uncommon",0,None,
                "Dwarven Token","A small iron disc with dwarven runes.",
                "Iron Ridge Guild Token","Cast iron, Warden chapter insignia.",
                "Faint protection resonance.",18,
                "A token of the Iron Ridge Warden chapter. Still holds a trace of the oath.",diff=2)),
        ],
        "description_tiers": {
            0: "The ghost of a dwarf in mining gear. Staring at you from the dark.",
            1: "Iron Ridge Shade",
            2: "Iron Ridge Shade — ghost of a mine worker. Resists physical, curse reduces accuracy.",
        },
    },

    "Vault Automaton": {
        "name": "Vault Automaton",
        "hp": 162, "defense": 18, "magic_resist": 8,
        "stats": {"STR": 16, "DEX": 5, "CON": 18, "INT": 3, "WIS": 2, "PIE": 2},
        "speed_base": 9,
        "attack_damage": 40, "attack_type": "melee", "phys_type": "blunt",
        "accuracy_bonus": 1,
        "preferred_row": FRONT,
        "ai_type": "aggressive",
        "xp_reward": 52, "gold_reward": _coin(0, 0),
        "resistances": _res(shadow=IMMUNE, nature=IMMUNE, poison=IMMUNE,
                            fire=NEUTRAL, blunt=RESISTANT,
                            piercing=RESISTANT, slashing=RESISTANT,
                            lightning=VULNERABLE),
        "status_immunities": ["Poisoned","Stunned","Slowed","Cursed","Burning","Blinded"],
        "abilities": [
            _ab_damage("Iron Fist", 46, "blunt",
                       "A mechanically perfect crushing blow",
                       stun_chance=0.30),
            _ab_buff("Overdrive Protocol", "enrage", 2,
                     "Activates emergency battle protocols",
                     targets="self"),
        ],
        "loot_table": [
            _drop(0.20, _item("Dwarven Gear Assembly","material","metal","uncommon",0,None,
                "Gear Cluster","A cluster of interlocking gears, still turning.",
                "Dwarven Precision Gears","Iron and mithril alloy.",
                "No magical properties — pure craftsmanship.",30,
                "Still-functional gear assembly from a dwarven automaton. Tier 2 crafting.",diff=2)),
            _drop(0.12, _item("Iron Core","material","metal","rare",0,None,
                "Heavy Sphere","A dense iron sphere with runes on its surface.",
                "Dwarven Warden Core","Iron-rune core, ward-powered.",
                "Protection enchantment — moderate.",45,
                "The power core of a Vault Automaton. Still holds residual ward energy.",diff=3)),
        ],
        "description_tiers": {
            0: "An iron figure still walking its patrol route. It has been walking it for centuries.",
            1: "Vault Automaton",
            2: "Vault Automaton — construct, immune to shadow/nature/poison/status. Lightning destroys it.",
        },
    },

    "Dwarven Forge Guard": {
        "name": "Dwarven Forge Guard",
        "hp": 178, "defense": 16, "magic_resist": 10,
        "stats": {"STR": 15, "DEX": 6, "CON": 16, "INT": 6, "WIS": 5, "PIE": 6},
        "speed_base": 10,
        "attack_damage": 38, "attack_type": "melee", "phys_type": "blunt",
        "accuracy_bonus": 2,
        "preferred_row": FRONT,
        "ai_type": "guardian",
        "xp_reward": 62, "gold_reward": _coin(0, 4),
        "resistances": _res(fire=RESISTANT, lightning=RESISTANT, shadow=RESISTANT,
                            divine=NEUTRAL),
        "status_immunities": ["Poisoned","Slowed"],
        "abilities": [
            _ab_damage("Forge Hammer", 48, "blunt",
                       "A hammer blow that carries the heat of the forge",
                       stun_chance=0.25, dot="burning", dot_duration=2),
            _ab_buff("Warden's Stand", "sentinel_resolve", 3,
                     "Takes a defensive stance built into Warden training",
                     targets="self"),
        ],
        "loot_table": [
            _drop(0.25, _item("Forge Guard Hammer","weapon","Mace","uncommon",
                12,"blunt","Heavy Dwarven Hammer","A war hammer built to last centuries.",
                "Iron Ridge Forge Hammer","Dwarven alloy, heat-treated.",
                "Fire resistance enchantment.",55,
                "A hammer still used by the guard who died holding the vault.",diff=2)),
            _drop(0.18, _item("Dwarven Forge Plate Fragment","material","metal","uncommon",0,None,
                "Armored Fragment","A piece of heavy plate, fire-blackened.",
                "Iron Ridge Forge Plate",
                "Dwarven alloy — fire and shadow resistant.",
                "Dual resistance enchantment.",32,
                "Fragment of the finest armor the Iron Ridge chapter produced.",diff=2)),
        ],
        "description_tiers": {
            0: "A dwarf in ancient forge-plate, still at his post despite being dead for decades.",
            1: "Dwarven Forge Guard",
            2: "Dwarven Forge Guard — elite undead dwarf, fire+lightning resistant, burning hammer.",
        },
    },

    "Stone Warden Ghost": {
        "name": "Stone Warden Ghost",
        "hp": 148, "defense": 10, "magic_resist": 22,
        "stats": {"STR": 12, "DEX": 8, "CON": 11, "INT": 12, "WIS": 14, "PIE": 14},
        "speed_base": 11,
        "attack_damage": 34, "attack_type": "magic", "phys_type": "divine",
        "accuracy_bonus": 4,
        "preferred_row": BACK,
        "ai_type": "support",
        "xp_reward": 70, "gold_reward": _coin(0, 5),
        "resistances": _res(shadow=VULNERABLE, divine=RESISTANT,
                            piercing=RESISTANT, slashing=RESISTANT,
                            blunt=RESISTANT),
        "status_immunities": ["Cursed","Stunned","Poisoned"],
        "tags": ["undead"],
        "abilities": [
            _ab_damage("Ward Pulse", 32, "divine",
                       "A burst of genuine ward-energy — what Warden magic was supposed to be",
                       target="aoe_enemy"),
            _ab_buff("Oath Renewed", "sentinel_resolve", 3,
                     "The oath to guard the vault renews itself — buffs all allies",
                     targets="all_allies"),
            _ab_heal("Dwarven Resilience", 40,
                     "Channels dwarven stubbornness into a healing force",
                     target="single_ally"),
        ],
        "loot_table": [
            _drop(0.22, _item("Stone Warden Rune","material","arcane","rare",0,None,
                "Glowing Rune Stone","A stone that pulses with genuine ward-light.",
                "Iron Ridge Ward Rune","Granite, original Warden inscription.",
                "Strong divine resonance — uncorrupted.",50,
                "A genuine Warden ward-rune. Unlike everything else in this dungeon, "
                "it's not corrupted. Korrath's people maintained these until the end.",diff=4)),
        ],
        "description_tiers": {
            0: "A dwarven ghost in Warden robes. It looks at you with recognition, then grief.",
            1: "Stone Warden Ghost",
            2: "Stone Warden Ghost — former Warden, genuine divine abilities, "
               "heals allies, AOE ward pulse. Shadow magic is the key.",
        },
    },
}


# ═══════════════════════════════════════════════════════════════
#  ALL ENEMIES MERGED
# ═══════════════════════════════════════════════════════════════

ALL_NEW_FACTION_ENEMIES = {}
ALL_NEW_FACTION_ENEMIES.update(BEAST_ENEMIES)
ALL_NEW_FACTION_ENEMIES.update(FALLEN_WARDEN_ENEMIES)
ALL_NEW_FACTION_ENEMIES.update(PIRATE_ENEMIES)
ALL_NEW_FACTION_ENEMIES.update(IMPERIAL_ENEMIES)
ALL_NEW_FACTION_ENEMIES.update(DWARF_ENEMIES)


# ═══════════════════════════════════════════════════════════════
#  ENCOUNTERS
# ═══════════════════════════════════════════════════════════════

ALL_NEW_FACTION_ENCOUNTERS = {

    # ── Fading-Touched Beasts ──────────────────────────────
    "fading_hounds":      {"name": "Fading Hounds",       "difficulty": "easy",
        "groups": [{"enemy": "Fading Hound", "count": 3, "row": FRONT}]},

    "fading_wolves":      {"name": "Fading Pack",         "difficulty": "easy",
        "groups": [{"enemy": "Fading Wolf",  "count": 2, "row": FRONT},
                   {"enemy": "Fading Hound", "count": 2, "row": FRONT}]},

    "fading_boar_pack":   {"name": "Fading Sounder",      "difficulty": "medium",
        "groups": [{"enemy": "Fading Boar",  "count": 2, "row": FRONT},
                   {"enemy": "Fading Hound", "count": 1, "row": FRONT}]},

    "fading_stag_pack":   {"name": "Fading Herd",         "difficulty": "medium",
        "groups": [{"enemy": "Fading Stag",  "count": 1, "row": MID},
                   {"enemy": "Fading Wolf",  "count": 2, "row": FRONT}]},

    "fading_bear_solo":   {"name": "Fading Bear",         "difficulty": "hard",
        "groups": [{"enemy": "Fading Bear",  "count": 1, "row": FRONT}]},

    "fading_bear_pack":   {"name": "The Fading's Vanguard","difficulty": "hard",
        "groups": [{"enemy": "Fading Bear",  "count": 1, "row": FRONT},
                   {"enemy": "Fading Wolf",  "count": 2, "row": FRONT},
                   {"enemy": "Fading Stag",  "count": 1, "row": MID}]},

    "fading_beasts_easy": {"name": "Fading Strays",       "difficulty": "easy",
        "groups": [{"enemy": "Fading Wolf",  "count": 2, "row": FRONT},
                   {"enemy": "Fading Hound", "count": 1, "row": FRONT}]},

    # ── Fallen Wardens ─────────────────────────────────────
    "fallen_patrol":      {"name": "Fallen Patrol",       "difficulty": "hard",
        "groups": [{"enemy": "Fallen Warden",  "count": 2, "row": FRONT},
                   {"enemy": "Warden Shade",   "count": 1, "row": MID}]},

    "fallen_ritual":      {"name": "Dark Consecration",   "difficulty": "hard",
        "groups": [{"enemy": "Fallen Warden",    "count": 1, "row": FRONT},
                   {"enemy": "Dark Consecrator", "count": 1, "row": BACK},
                   {"enemy": "Warden Shade",     "count": 2, "row": MID}]},

    "fallen_knights":     {"name": "Oathbreakers",        "difficulty": "hard",
        "groups": [{"enemy": "Oathbreaker Knight", "count": 2, "row": FRONT},
                   {"enemy": "Warden Shade",        "count": 1, "row": MID}]},

    "fallen_elite":       {"name": "Fallen Warden Elite", "difficulty": "hard",
        "groups": [{"enemy": "Oathbreaker Knight", "count": 1, "row": FRONT},
                   {"enemy": "Dark Consecrator",   "count": 1, "row": BACK},
                   {"enemy": "Shadow Warden",      "count": 1, "row": BACK}]},

    "shadow_warden_solo": {"name": "Shadow Warden",       "difficulty": "hard",
        "groups": [{"enemy": "Shadow Warden",    "count": 1, "row": BACK},
                   {"enemy": "Fallen Warden",    "count": 2, "row": FRONT}]},

    # ── Pirates ────────────────────────────────────────────
    "pirate_crew":        {"name": "Pirate Crew",         "difficulty": "medium",
        "groups": [{"enemy": "Pirate Deckhand",    "count": 3, "row": FRONT}]},

    "pirate_ambush":      {"name": "Pirate Ambush",       "difficulty": "medium",
        "groups": [{"enemy": "Pirate Deckhand",    "count": 2, "row": FRONT},
                   {"enemy": "Pirate Markswoman",  "count": 2, "row": BACK}]},

    "pirate_with_witch":  {"name": "Hexed Crew",          "difficulty": "hard",
        "groups": [{"enemy": "Pirate Deckhand",    "count": 2, "row": FRONT},
                   {"enemy": "Pirate Witch Doctor","count": 1, "row": BACK},
                   {"enemy": "Pirate Markswoman",  "count": 1, "row": BACK}]},

    "pirate_officers":    {"name": "Pirate Officers",     "difficulty": "hard",
        "groups": [{"enemy": "Pirate First Mate",  "count": 1, "row": FRONT},
                   {"enemy": "Pirate Deckhand",    "count": 2, "row": FRONT},
                   {"enemy": "Pirate Witch Doctor","count": 1, "row": BACK}]},

    "pirate_captain_enc": {"name": "The Captain's Guard", "difficulty": "hard",
        "groups": [{"enemy": "Pirate Captain",     "count": 1, "row": FRONT},
                   {"enemy": "Pirate First Mate",  "count": 1, "row": FRONT},
                   {"enemy": "Pirate Markswoman",  "count": 2, "row": BACK}]},

    # ── Imperial Forces ────────────────────────────────────
    "imperial_patrol":    {"name": "Imperial Patrol",     "difficulty": "medium",
        "groups": [{"enemy": "Imperial Soldier", "count": 3, "row": FRONT}]},

    "imperial_squad":     {"name": "Imperial Squad",      "difficulty": "hard",
        "groups": [{"enemy": "Imperial Soldier", "count": 2, "row": FRONT},
                   {"enemy": "Imperial Archer",  "count": 2, "row": BACK}]},

    "imperial_with_mage": {"name": "Imperial Unit",       "difficulty": "hard",
        "groups": [{"enemy": "Imperial Soldier",    "count": 2, "row": FRONT},
                   {"enemy": "Imperial Court Mage", "count": 1, "row": BACK},
                   {"enemy": "Imperial Archer",     "count": 1, "row": BACK}]},

    "imperial_inquisitor_enc": {"name": "Inquisitor's Detail", "difficulty": "hard",
        "groups": [{"enemy": "Imperial Inquisitor","count": 1, "row": FRONT},
                   {"enemy": "Imperial Soldier",   "count": 2, "row": FRONT},
                   {"enemy": "Imperial Archer",    "count": 1, "row": BACK}]},

    "imperial_commander_enc": {"name": "Commander's Force", "difficulty": "hard",
        "groups": [{"enemy": "Imperial Commander", "count": 1, "row": FRONT},
                   {"enemy": "Imperial Soldier",   "count": 2, "row": FRONT},
                   {"enemy": "Imperial Court Mage","count": 1, "row": BACK}]},

    # ── Iron Ridge Dwarves ─────────────────────────────────
    "iron_ridge_shades":  {"name": "Mine Ghosts",         "difficulty": "medium",
        "groups": [{"enemy": "Iron Ridge Shade", "count": 3, "row": MID}]},

    "iron_ridge_automata":{"name": "Vault Patrol",        "difficulty": "medium",
        "groups": [{"enemy": "Vault Automaton",  "count": 2, "row": FRONT}]},

    "iron_ridge_guard":   {"name": "Forge Guard",         "difficulty": "hard",
        "groups": [{"enemy": "Dwarven Forge Guard","count": 1, "row": FRONT},
                   {"enemy": "Iron Ridge Shade",  "count": 2, "row": MID}]},

    "iron_ridge_warden":  {"name": "Stone Warden's Watch","difficulty": "hard",
        "groups": [{"enemy": "Stone Warden Ghost", "count": 1, "row": BACK},
                   {"enemy": "Vault Automaton",    "count": 1, "row": FRONT},
                   {"enemy": "Iron Ridge Shade",   "count": 2, "row": MID}]},

    "iron_ridge_full":    {"name": "Vault's Last Guard",  "difficulty": "hard",
        "groups": [{"enemy": "Stone Warden Ghost",  "count": 1, "row": BACK},
                   {"enemy": "Dwarven Forge Guard", "count": 1, "row": FRONT},
                   {"enemy": "Vault Automaton",     "count": 1, "row": FRONT}]},
}


# ═══════════════════════════════════════════════════════════════
#  DUNGEON ENCOUNTER TABLE UPDATES
# ═══════════════════════════════════════════════════════════════

NEW_FACTION_ENCOUNTER_TABLE_UPDATES = {
    # ── Goblin Warren — NO bandits, only beasts and goblins ──
    "goblin_warren": {
        1: ["gw_scouts", "gw_bats", "gw_mixed_easy", "fading_hounds", "fading_wolves"],
        2: ["medium_goblins", "hard_goblins", "fading_wolves", "fading_stag_pack"],
        3: ["hard_goblins", "hard_mixed", "fading_bear_pack"],
    },
    # ── Abandoned Mine — mercs as Valdris's agents, dwarven ghosts deep ──
    "abandoned_mine": {
        1: ["am_kobolds", "am_beetles", "fading_hounds", "bandit_skirmish"],
        2: ["medium_goblins", "merc_patrol", "iron_ridge_shades", "iron_ridge_automata"],
        3: ["merc_squad", "iron_ridge_guard", "bandit_with_mage"],
        4: ["merc_warband", "iron_ridge_warden", "merc_elite"],
        5: ["iron_ridge_full", "merc_warband", "iron_ridge_warden"],
    },
    # ── Sunken Crypt — Crypt Guard (renamed) and spectral ──
    "sunken_crypt": {
        1: ["sc_zombies", "sc_skel_patrol", "crypt_patrol"],
        2: ["sc_ghoul_pack", "crypt_mixed", "sc_shade_haunt"],
        3: ["crypt_heavy", "sc_death_knight", "sc_undead_horde"],
        4: ["crypt_elite", "sc_bone_elite"],
    },
    # ── Ruins of Ashenmoor — cultists + mercs hired by Governor ──
    "ruins_ashenmoor": {
        1: ["ra_bandits", "cult_patrol", "fading_beasts_easy"],
        2: ["cult_warband", "merc_patrol", "cult_ritual"],
        3: ["cult_with_sorcerer", "merc_squad", "cult_warband"],
        4: ["cult_elite", "merc_warband", "cult_with_sorcerer"],
    },
    # ── Dragon's Tooth — pirates camped near the entrance, volcanic creatures
    #    deeper in the tunnels. Floor 1 mixes both; floors 2-3 shift toward
    #    native creatures with pirates still present. ──
    "dragons_tooth": {
        1: ["pirate_crew", "pirate_ambush", "dt_hatchlings", "dt_beetles"],
        2: ["pirate_with_witch", "pirate_ambush", "dt_drakes", "dt_beetles", "dt_troll"],
        3: ["dt_mixed", "dt_drake_swarm", "dt_drakes", "pirate_officers", "pirate_captain_enc"],
    },
    # ── Pale Coast — cultists drawn to the coast, Crypt Guard drowned variant ──
    "pale_coast": {
        1: ["pc_shades", "cult_patrol", "fading_hounds"],
        2: ["pc_drowned", "cult_warband", "crypt_mixed"],
        3: ["cult_with_sorcerer", "crypt_heavy", "cult_elite"],
        4: ["crypt_elite", "cult_elite"],
    },
    # ── Windswept Isle — elemental creatures only, no humanoids ──
    "windswept_isle": {
        1: ["wi_sprites", "wi_mixed"],
        2: ["wi_golem", "wi_mixed", "wi_storm_mob"],
        3: ["wi_storm_mob", "wi_golem"],
    },
    # ── Shadow Throne — cultists low floors, Fallen Wardens mid, elite high ──
    "shadow_throne": {
        1: ["cult_patrol", "st_shades", "fading_beasts_easy"],
        2: ["cult_warband", "st_mixed", "st_shades"],
        3: ["fallen_patrol", "st_echoes", "cult_with_sorcerer"],
        4: ["fallen_ritual", "fallen_knights", "st_mixed"],
        5: ["fallen_knights", "fallen_elite", "st_elite"],
        6: ["shadow_warden_solo", "fallen_elite", "st_abominations"],
        7: ["shadow_warden_solo", "st_warden_elite", "fallen_elite"],
        8: ["st_void", "shadow_warden_solo"],
    },
    # ── Overworld/road random encounters (Act 1) ──────────────
    # These use key "overworld_act1", "overworld_act2" etc.
    "overworld_act1": {
        1: ["fading_hounds", "fading_wolves", "bandit_skirmish", "wolves"],
        2: ["fading_boar_pack", "fading_stag_pack", "bandit_ambush", "bandit_with_mage"],
        3: ["fading_bear_solo", "bandit_warband", "fading_wolves"],
    },
    "overworld_act2": {
        1: ["merc_patrol", "imperial_patrol", "fading_wolves"],
        2: ["merc_squad", "imperial_squad", "fading_boar_pack"],
        3: ["imperial_with_mage", "imperial_inquisitor_enc", "merc_warband"],
    },
}
