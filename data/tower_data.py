"""
Realm of Shadows — Valdris' Spire (Tower Dungeon)

A crumbling arcane tower where Valdris conducted his research into the Fading.
6 ascending floors, each more corrupted than the last.
Theme: stone → arcane → fading corruption.

Floor 1-2: Abandoned study — constructs and vermin still guard the entrance
Floor 3-4: Arcane labs — experiments gone wrong, corrupted scholars
Floor 5:   Fading breach — reality warps, shadow creatures emerge
Floor 6:   Valdris' Sanctum — boss fight: The Lingering Will of Valdris
"""

from data.enemies import FRONT, MID, BACK, NEUTRAL

# Helper (same as bestiary_m9.py)
def _S(s, d, c, i, w, p):
    return {"STR": s, "DEX": d, "CON": c, "INT": i, "WIS": w, "PIE": p}

def _e(name, hp, df, mr, stats, spd, atk, atype, ptype,
       acc=0, row="front", ai="aggressive", xp=0, gold=(0,0),
       res=None, imm=None, ab=None, loot=None, desc=None):
    r = {
        "piercing": NEUTRAL, "slashing": NEUTRAL, "blunt": NEUTRAL,
        "fire": NEUTRAL, "ice": NEUTRAL, "lightning": NEUTRAL,
        "divine": NEUTRAL, "shadow": NEUTRAL, "nature": NEUTRAL, "arcane": NEUTRAL,
    }
    if res:
        for k, v in res.items():
            r[k] = v
    e = {
        "name": name, "hp": hp, "defense": df, "magic_resist": mr,
        "stats": stats, "speed_base": spd,
        "attack_damage": atk, "attack_type": atype, "phys_type": ptype,
        "accuracy_bonus": acc, "preferred_row": {"front": FRONT, "mid": MID, "back": BACK}.get(row, FRONT),
        "ai_type": ai, "xp_reward": xp, "gold_reward": gold,
        "resistances": r, "status_immunities": imm or [], "abilities": ab or [],
        "loot_table": loot or [],
        "description_tiers": desc or {},
    }
    return e


# ══════════════════════════════════════════════════════════
#  TOWER ENEMIES
# ══════════════════════════════════════════════════════════

TOWER_ENEMIES = {
    # ── Floor 1-2: Constructs & vermin ──
    "Stone Guardian": _e("Stone Guardian", 55, 14, 4,
        _S(16, 4, 14, 2, 4, 0), 6, 18, "melee", "blunt",
        xp=28, gold=(4, 12),
        res={"piercing": 0.3, "slashing": 0.5, "blunt": 1.5, "lightning": 2.0,
             "fire": 0.8, "ice": 0.8},
        imm=["Poisoned", "Fear", "Sleep"],
        desc={0: "A stone statue that grinds to life.", 1: "Stone Guardian",
              2: "Stone Guardian — very high armor. Weak to blunt/lightning."}),

    "Arcane Sentry": _e("Arcane Sentry", 35, 6, 10,
        _S(4, 10, 8, 14, 10, 2), 14, 12, "ranged", "arcane",
        acc=4, row="mid", xp=25, gold=(5, 14),
        res={"arcane": 0.0, "shadow": 1.5},
        imm=["Poisoned", "Sleep"],
        ab=[{"name": "Arcane Bolt", "type": "damage", "target": "single_enemy",
             "power": 14, "element": "arcane", "description": "Fires a bolt of arcane energy."}],
        desc={0: "A floating crystal orbiting a metal frame.", 1: "Arcane Sentry",
              2: "Arcane Sentry — ranged arcane damage. Immune to arcane."}),

    "Tower Rat": _e("Tower Rat", 12, 0, 0,
        _S(3, 14, 3, 1, 3, 0), 20, 5, "melee", "piercing",
        acc=3, xp=5, gold=(0, 2),
        desc={0: "An oversized rat.", 1: "Tower Rat", 2: "Tower Rat — fast, weak."}),

    "Animated Armor": _e("Animated Armor", 65, 16, 2,
        _S(18, 6, 14, 1, 2, 0), 6, 22, "melee", "slashing",
        xp=38, gold=(8, 18),
        res={"piercing": 0.5, "slashing": 0.5, "blunt": 1.5, "lightning": 1.8},
        imm=["Poisoned", "Fear", "Sleep", "Stun"],
        loot=[{"drop_chance": 0.10, "item": {
            "name": "Enchanted Iron Plate", "type": "material",
            "subtype": "metal", "rarity": "uncommon", "tier": 2,
            "identified": True, "estimated_value": 22,
            "description": "Iron animated by old magic. Still hums faintly."}}],
        desc={0: "A suit of armor moving on its own.", 1: "Animated Armor",
              2: "Animated Armor — heavy armor. Weak to blunt/lightning."}),

    # ── Floor 3-4: Corrupted scholars & experiments ──
    "Corrupted Scholar": _e("Corrupted Scholar", 40, 3, 12,
        _S(4, 8, 6, 16, 14, 4), 12, 8, "ranged", "arcane",
        acc=5, row="back", ai="supportive", xp=35, gold=(8, 20),
        res={"arcane": 0.5, "shadow": 0.5, "divine": 1.5},
        ab=[{"name": "Fading Bolt", "type": "damage", "target": "single_enemy",
             "power": 18, "element": "shadow", "description": "A bolt of Fading energy."},
            {"name": "Dark Mend", "type": "heal", "target": "ally_lowest",
             "power": 20, "description": "Heals an ally with dark magic."}],
        loot=[{"drop_chance": 0.08, "item": {
            "name": "Arcane Dust", "type": "material",
            "subtype": "reagent", "rarity": "rare", "tier": 3,
            "identified": True, "estimated_value": 40,
            "description": "Dust infused with residual arcane power."}}],
        desc={0: "A robed figure muttering incomprehensibly.", 1: "Corrupted Scholar",
              2: "Corrupted Scholar — casts shadow bolts and heals. Priority target."}),

    "Flesh Golem": _e("Flesh Golem", 90, 8, 4,
        _S(22, 4, 20, 2, 4, 0), 5, 26, "melee", "blunt",
        xp=48, gold=(5, 15),
        res={"lightning": 2.0, "fire": 1.5, "nature": 0.5, "shadow": 0.5},
        imm=["Poisoned", "Fear", "Sleep"],
        ab=[{"name": "Slam", "type": "damage", "target": "single_enemy",
             "power": 22, "element": "blunt", "description": "A devastating slam."}],
        desc={0: "A hulking mass of stitched flesh.", 1: "Flesh Golem",
              2: "Flesh Golem — very tough. Weak to lightning/fire."}),

    "Arcane Wisp": _e("Arcane Wisp", 18, 0, 14,
        _S(1, 16, 4, 12, 10, 2), 22, 10, "ranged", "arcane",
        acc=6, row="back", xp=18, gold=(3, 8),
        res={"piercing": 0.0, "slashing": 0.0, "blunt": 0.0, "arcane": 0.0, "shadow": 1.5, "divine": 1.5},
        imm=["Poisoned", "Fear"],
        desc={0: "A flickering mote of arcane light.", 1: "Arcane Wisp",
              2: "Arcane Wisp — immune to physical and arcane. Use shadow or divine."}),

    "Living Tome": _e("Living Tome", 28, 4, 12,
        _S(2, 10, 6, 16, 12, 4), 14, 6, "ranged", "arcane",
        acc=4, row="back", xp=22, gold=(6, 14),
        res={"fire": 3.0, "arcane": 0.0},
        ab=[{"name": "Spell Page", "type": "damage", "target": "single_enemy",
             "power": 16, "element": "arcane",
             "description": "A page tears free and detonates."}],
        desc={0: "A book flapping through the air on its own.", 1: "Living Tome",
              2: "Living Tome — casts arcane. Extremely weak to fire."}),

    # ── Floor 5-6: Fading creatures ──
    "Fading Wraith": _e("Fading Wraith", 45, 0, 18,
        _S(2, 14, 6, 16, 16, 4), 18, 14, "ranged", "shadow",
        acc=6, row="back", xp=42, gold=(5, 18),
        res={"piercing": 0.0, "slashing": 0.0, "blunt": 0.0, "shadow": 0.0,
             "divine": 2.5, "fire": 1.5, "arcane": 0.5},
        imm=["Poisoned", "Fear", "Sleep", "Stun"],
        ab=[{"name": "Fading Touch", "type": "damage", "target": "single_enemy",
             "power": 20, "element": "shadow",
             "status": "Weakened", "status_chance": 0.3, "status_duration": 3,
             "description": "Drains vitality with the Fading."}],
        desc={0: "A shape of emptiness in the air.", 1: "Fading Wraith",
              2: "Fading Wraith — immune to phys/shadow. Use divine."}),

    "Void Tendril": _e("Void Tendril", 30, 4, 8,
        _S(14, 8, 10, 2, 2, 0), 10, 16, "melee", "shadow",
        xp=28, gold=(0, 5),
        res={"shadow": 0.0, "divine": 2.0, "fire": 1.5},
        ab=[{"name": "Grasping Pull", "type": "debuff", "target": "single_enemy",
             "effect": {"speed_penalty": 0.5, "duration": 2},
             "description": "Pulls a target, slowing them."}],
        desc={0: "A writhing tendril of darkness.", 1: "Void Tendril",
              2: "Void Tendril — slows targets. Weak to divine/fire."}),

    "Reality Fracture": _e("Reality Fracture", 50, 0, 20,
        _S(1, 1, 12, 18, 18, 6), 8, 0, "ranged", "arcane",
        ai="supportive", row="back", xp=50, gold=(10, 25),
        res={"piercing": 0.0, "slashing": 0.0, "blunt": 0.0,
             "arcane": 0.0, "shadow": 0.0, "divine": 2.0, "fire": 1.5},
        imm=["Poisoned", "Fear", "Sleep", "Stun"],
        ab=[{"name": "Warp Pulse", "type": "damage", "target": "aoe_enemy",
             "power": 12, "element": "arcane", "description": "A pulse of distorted reality."},
            {"name": "Rift Heal", "type": "heal", "target": "ally_lowest",
             "power": 30, "description": "Pulls energy from the Fading to heal."}],
        desc={0: "A tear in reality itself, shimmering.", 1: "Reality Fracture",
              2: "Reality Fracture — heals allies, AoE arcane. Immune to phys. Kill fast."}),

    # ── Boss: The Lingering Will ──
    "Lingering Will": _e("Lingering Will", 320, 8, 18,
        _S(14, 12, 16, 22, 18, 8), 14, 20, "ranged", "shadow",
        acc=8, ai="boss", xp=200, gold=(80, 150),
        res={"piercing": 0.7, "slashing": 0.7, "blunt": 0.7,
             "shadow": 0.0, "arcane": 0.5, "divine": 2.0, "fire": 1.2},
        imm=["Poisoned", "Fear", "Sleep"],
        ab=[
            {"name": "Fading Storm", "type": "damage", "target": "aoe_enemy",
             "power": 22, "element": "shadow", "description": "A storm of Fading energy engulfs all."},
            {"name": "Arcane Barrage", "type": "damage", "target": "single_enemy",
             "power": 30, "element": "arcane", "description": "A focused barrage of arcane missiles."},
            {"name": "Mend Reality", "type": "heal", "target": "self",
             "power": 35, "description": "Draws power from the Fading to regenerate."},
            {"name": "Fading Curse", "type": "debuff", "target": "single_enemy",
             "effect": {"damage_penalty": 0.6, "duration": 3},
             "description": "Curses a target, weakening their attacks."},
        ],
        loot=[{"drop_chance": 0.80, "item": {
            "name": "Hearthstone Fragment", "type": "key_item",
            "subtype": "quest", "rarity": "legendary",
            "identified": True, "estimated_value": 0,
            "description": "A fragment of the Hearthstone. It pulses with warm light."}}],
        desc={0: "A towering figure of shadow and light.",
              1: "The Lingering Will of Valdris",
              2: "The Lingering Will — Valdris' shadow. AoE shadow, arcane barrage, self-heal. Use divine."}),
}


# ══════════════════════════════════════════════════════════
#  TOWER ENCOUNTERS
# ══════════════════════════════════════════════════════════

TOWER_ENCOUNTERS = {
    # Floor 1: Entry hall
    "vs_rats":      {"name": "Tower Vermin", "difficulty": "easy",
        "groups": [{"enemy": "Tower Rat", "count": 5, "row": "front"}]},
    "vs_guardian":   {"name": "Stone Sentinel", "difficulty": "easy",
        "groups": [{"enemy": "Stone Guardian", "count": 1, "row": "front"},
                   {"enemy": "Tower Rat", "count": 3, "row": "front"}]},
    "vs_sentries":   {"name": "Sentry Post", "difficulty": "easy",
        "groups": [{"enemy": "Arcane Sentry", "count": 2, "row": "mid"}]},
    "vs_entry":      {"name": "Tower Guards", "difficulty": "medium",
        "groups": [{"enemy": "Stone Guardian", "count": 1, "row": "front"},
                   {"enemy": "Arcane Sentry", "count": 1, "row": "mid"}]},

    # Floor 2: Guard halls
    "vs_armor_pair": {"name": "Animated Guards", "difficulty": "medium",
        "groups": [{"enemy": "Animated Armor", "count": 2, "row": "front"}]},
    "vs_armor_sentry":{"name": "Armor & Sentry", "difficulty": "medium",
        "groups": [{"enemy": "Animated Armor", "count": 1, "row": "front"},
                   {"enemy": "Arcane Sentry", "count": 2, "row": "mid"}]},
    "vs_guardian_duo":{"name": "Twin Guardians", "difficulty": "medium",
        "groups": [{"enemy": "Stone Guardian", "count": 2, "row": "front"},
                   {"enemy": "Tower Rat", "count": 2, "row": "front"}]},
    "vs_sentry_nest": {"name": "Sentry Cluster", "difficulty": "medium",
        "groups": [{"enemy": "Arcane Sentry", "count": 3, "row": "mid"},
                   {"enemy": "Tower Rat", "count": 2, "row": "front"}]},

    # Floor 3: Corrupted studies
    "vs_scholars":   {"name": "Corrupted Researchers", "difficulty": "medium",
        "groups": [{"enemy": "Corrupted Scholar", "count": 2, "row": "back"},
                   {"enemy": "Arcane Sentry", "count": 1, "row": "mid"}]},
    "vs_tomes":      {"name": "Living Library", "difficulty": "medium",
        "groups": [{"enemy": "Living Tome", "count": 3, "row": "back"},
                   {"enemy": "Arcane Wisp", "count": 2, "row": "back"}]},
    "vs_wisps":      {"name": "Wisp Swarm", "difficulty": "medium",
        "groups": [{"enemy": "Arcane Wisp", "count": 4, "row": "back"}]},
    "vs_lab_guard":  {"name": "Lab Guardians", "difficulty": "hard",
        "groups": [{"enemy": "Animated Armor", "count": 1, "row": "front"},
                   {"enemy": "Corrupted Scholar", "count": 1, "row": "back"},
                   {"enemy": "Living Tome", "count": 1, "row": "back"}]},

    # Floor 4: Experiments
    "vs_golem":      {"name": "Failed Experiment", "difficulty": "hard",
        "groups": [{"enemy": "Flesh Golem", "count": 1, "row": "front"},
                   {"enemy": "Corrupted Scholar", "count": 1, "row": "back"}]},
    "vs_golem_wisps": {"name": "Golem & Wisps", "difficulty": "hard",
        "groups": [{"enemy": "Flesh Golem", "count": 1, "row": "front"},
                   {"enemy": "Arcane Wisp", "count": 3, "row": "back"}]},
    "vs_twin_golems": {"name": "Twin Abominations", "difficulty": "hard",
        "groups": [{"enemy": "Flesh Golem", "count": 2, "row": "front"}]},
    "vs_scholar_lab": {"name": "Dark Research Team", "difficulty": "hard",
        "groups": [{"enemy": "Corrupted Scholar", "count": 2, "row": "back"},
                   {"enemy": "Animated Armor", "count": 1, "row": "front"},
                   {"enemy": "Living Tome", "count": 2, "row": "back"}]},

    # Floor 5: Fading breach
    "vs_wraiths":    {"name": "Fading Manifestation", "difficulty": "hard",
        "groups": [{"enemy": "Fading Wraith", "count": 2, "row": "back"},
                   {"enemy": "Void Tendril", "count": 2, "row": "front"}]},
    "vs_tendrils":   {"name": "Grasping Void", "difficulty": "hard",
        "groups": [{"enemy": "Void Tendril", "count": 4, "row": "front"}]},
    "vs_fracture":   {"name": "Reality Tear", "difficulty": "hard",
        "groups": [{"enemy": "Reality Fracture", "count": 1, "row": "back"},
                   {"enemy": "Void Tendril", "count": 2, "row": "front"},
                   {"enemy": "Fading Wraith", "count": 1, "row": "back"}]},
    "vs_breach_full": {"name": "Full Breach", "difficulty": "boss",
        "groups": [{"enemy": "Reality Fracture", "count": 1, "row": "back"},
                   {"enemy": "Fading Wraith", "count": 2, "row": "back"},
                   {"enemy": "Void Tendril", "count": 3, "row": "front"}]},

    # Boss
    "boss_lingering_will": {"name": "The Lingering Will of Valdris", "difficulty": "boss",
        "groups": [{"enemy": "Lingering Will", "count": 1, "row": "back"},
                   {"enemy": "Fading Wraith", "count": 2, "row": "back"}]},
}


TOWER_ENCOUNTER_TABLE = {
    "valdris_spire": {
        1: ["vs_rats", "vs_guardian", "vs_sentries", "vs_entry"],
        2: ["vs_armor_pair", "vs_armor_sentry", "vs_guardian_duo", "vs_sentry_nest"],
        3: ["vs_scholars", "vs_tomes", "vs_wisps", "vs_lab_guard"],
        4: ["vs_golem", "vs_golem_wisps", "vs_twin_golems", "vs_scholar_lab"],
        5: ["vs_wraiths", "vs_tendrils", "vs_fracture", "vs_breach_full"],
        "boss": "boss_lingering_will",
    },
}


# ══════════════════════════════════════════════════════════
#  TOWER BOSS LOOT
# ══════════════════════════════════════════════════════════

TOWER_BOSS_LOOT = {
    "Lingering Will": [
        {"drop_chance": 0.80, "item": {
            "name": "Valdris' Tome of Binding", "type": "weapon", "slot": "weapon",
            "subtype": "Tome", "rarity": "epic", "damage": 6,
            "phys_type": "blunt", "range": "melee",
            "spell_bonus": 10,
            "enchant_element": "arcane", "enchant_bonus": 7, "enchant_name": "Arcane",
            "effect": {"int_bonus": 4, "wis_bonus": 2},
            "identified": True, "estimated_value": 500,
            "description": "Valdris' personal grimoire. Crackles with arcane and shadow. +4 INT, +2 WIS, +10 spell."}},
        {"drop_chance": 0.50, "item": {
            "name": "Spire Warden's Mantle", "type": "armor", "slot": "body",
            "subtype": "robes", "rarity": "epic", "armor_tier": "clothing",
            "defense": 4, "magic_resist": 10,
            "effect": {"int_bonus": 2, "wis_bonus": 2},
            "enchant_resist": "shadow", "enchant_resist_bonus": 5,
            "identified": True, "estimated_value": 450,
            "description": "Robes worn by the tower's master. +2 INT, +2 WIS, +10 magic resist, shadow ward."}},
        {"drop_chance": 0.35, "item": {
            "name": "Ring of the Spire", "type": "accessory", "slot": "accessory1",
            "subtype": "ring", "rarity": "epic",
            "effect": {"int_bonus": 3, "pie_bonus": 2},
            "magic_resist": 4,
            "identified": True, "estimated_value": 350,
            "description": "A ring that resonates with the tower itself. +3 INT, +2 PIE."}},
    ],
}


# ══════════════════════════════════════════════════════════
#  TOWER JOURNALS / LORE
# ══════════════════════════════════════════════════════════

TOWER_JOURNALS = {
    1: [
        {"title": "Entry Log — Year 412",
         "text": "The tower is sealed. Valdris ordered the lower halls warded with "
                 "constructs after the last intrusion. The Wardens grow suspicious "
                 "of his research, but he insists it's for the greater good.",
         "lore_id": "spire_log_1"},
    ],
    2: [
        {"title": "Research Notes — Animated Guardians",
         "text": "The animated armor works splendidly. A simple binding circle "
                 "imprints combat instinct into the metal. They never tire, "
                 "never question. If only the other Wardens were so obedient.",
         "lore_id": "spire_log_2"},
    ],
    3: [
        {"title": "Research Notes — The Fading",
         "text": "I've confirmed it. The Fading is not a disease — it's a boundary "
                 "collapse. The veil between our world and the Void thins where the "
                 "Hearthstones' influence wanes. If I can harness a Fading breach "
                 "directly... the power would be beyond anything the Wardens imagined.",
         "lore_id": "spire_log_3"},
    ],
    4: [
        {"title": "Personal Journal — Doubts",
         "text": "Maren visited today. She's growing. Bright child. Asked me why "
                 "the tower 'feels sad.' I told her towers don't feel. But she's "
                 "right. Something has changed here. The experiments pull at the "
                 "edges of things. I've started seeing shapes in the corners.",
         "lore_id": "spire_log_4"},
    ],
    5: [
        {"title": "Final Entry",
         "text": "The breach is open. The Fading pours through like water through "
                 "a cracked dam. I can feel it reshaping me — not destroying, but "
                 "rewriting. I understand now why the old Wardens hid the Hearthstones. "
                 "Not to protect the world from the Fading. To protect the Fading "
                 "from people like me. It's too late to close this. It's too late "
                 "for everything. Maren... forgive me.",
         "lore_id": "spire_log_5"},
    ],
}

TOWER_FLOOR_MESSAGES = {
    1: "The tower entrance groans open. Dust cascades from ancient stone. Constructs stir in the darkness.",
    2: "Armor lines the halls like silent sentinels. Some begin to move as you pass.",
    3: "Books and scrolls litter the floor. The air crackles with residual magic.",
    4: "The stench of alchemical reagents fills the air. Something large stirs in the shadows.",
    5: "Reality warps. The walls seem to breathe. Tendrils of void seep through cracks in the stone.",
    6: "The top of the tower. A great rift hangs in the air, and within it — a figure of shadow and light.",
}
