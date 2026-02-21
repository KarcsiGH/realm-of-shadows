"""
Realm of Shadows — M9 Expanded Bestiary
New enemies, encounters, and encounter tables.
Merged into enemies.py at import time.
"""

# ══════════════════════════════════════════════════════════
#  HELPER
# ══════════════════════════════════════════════════════════

def _e(name, hp, df, mr, stats, spd, dmg, atype, phys,
       acc=0, row="front", ai="aggressive", xp=20, gold=(5,12),
       res=None, imm=None, ab=None, loot=None, desc=None):
    r = {"piercing":1.0,"slashing":1.0,"blunt":1.0,"fire":1.0,
         "ice":1.0,"lightning":1.0,"divine":1.0,"shadow":1.0,"nature":1.0,"arcane":1.0}
    if res: r.update(res)
    return {"name":name,"hp":hp,"defense":df,"magic_resist":mr,
            "stats":stats,"speed_base":spd,"attack_damage":dmg,
            "attack_type":atype,"phys_type":phys,"accuracy_bonus":acc,
            "preferred_row":row,"ai_type":ai,"xp_reward":xp,"gold_reward":gold,
            "resistances":r,"status_immunities":imm or [],"abilities":ab or [],
            "loot_table":loot or [],
            "description_tiers":desc or {0:name,1:name,2:name}}

S = lambda s,d,c,i,w,p: {"STR":s,"DEX":d,"CON":c,"INT":i,"WIS":w,"PIE":p}

# ══════════════════════════════════════════════════════════
#  NEW ENEMIES
# ══════════════════════════════════════════════════════════

NEW_ENEMIES = {
    # ── Cave / Goblin Warren ──
    "Goblin Scout": _e("Goblin Scout",20,1,0,S(4,14,3,3,6,1),20,8,"melee","piercing",
        acc=3,xp=10,gold=(2,6),
        desc={0:"A scrawny goblin with a rusty knife.",1:"Goblin Scout",
              2:"Goblin Scout — fast, weak. Often in groups."}),
    "Goblin Brute": _e("Goblin Brute",48,4,1,S(14,6,12,2,3,1),10,18,"melee","blunt",
        xp=28,gold=(8,16),
        desc={0:"A hulking goblin with a wooden club.",1:"Goblin Brute",
              2:"Goblin Brute — slow but hits hard."}),
    "Goblin Trapper": _e("Goblin Trapper",26,2,2,S(5,12,5,7,8,2),15,10,"ranged","piercing",
        acc=4,row="mid",ai="supportive",xp=22,gold=(5,10),
        ab=[{"name":"Caltrops","type":"debuff","target":"single_enemy",
             "effect":{"speed_penalty":0.5,"duration":2},"description":"Slows an enemy."}],
        desc={0:"A goblin fiddling with strange devices.",1:"Goblin Trapper",
              2:"Goblin Trapper — throws caltrops to slow you."}),
    "Cave Bat": _e("Cave Bat",14,1,0,S(3,16,2,1,8,1),24,6,"melee","piercing",
        acc=6,xp=6,gold=(0,2),res={"lightning":1.5,"nature":0.5},
        desc={0:"A screeching bat.",1:"Cave Bat",2:"Cave Bat — fast, fragile."}),
    "Fungal Crawler": _e("Fungal Crawler",30,3,4,S(6,4,10,1,2,1),8,10,"melee","blunt",
        ai="defensive",xp=16,gold=(1,4),res={"nature":0.0,"fire":2.0,"ice":0.5},
        ab=[{"name":"Spore Cloud","type":"damage","target":"aoe_enemy","power":5,
             "element":"nature","status":"Poisoned","status_chance":0.35,
             "status_duration":3,"description":"Toxic spore cloud."}],
        desc={0:"A mushroom creature oozing slime.",1:"Fungal Crawler",
              2:"Fungal Crawler — poison spores. Weak to fire."}),

    # ── Spider's Nest ──
    "Spiderling": _e("Spiderling",12,1,1,S(4,14,3,1,4,1),22,5,"melee","piercing",
        acc=5,xp=6,gold=(0,2),res={"fire":1.5},
        desc={0:"A cat-sized spider.",1:"Spiderling",2:"Spiderling — tiny but numerous."}),
    "Web Spinner": _e("Web Spinner",28,3,5,S(6,12,6,6,8,2),14,8,"ranged","nature",
        acc=4,row="mid",ai="supportive",xp=24,gold=(3,8),res={"fire":2.0,"nature":0.0},
        ab=[{"name":"Web Shot","type":"debuff","target":"single_enemy",
             "effect":{"speed_penalty":0.3,"duration":3},"description":"Sticky web."}],
        desc={0:"A spider dangling silk.",1:"Web Spinner",
              2:"Web Spinner — webs slow your party."}),
    "Venomfang Spider": _e("Venomfang Spider",42,5,4,S(12,14,10,2,8,1),18,16,"melee","piercing",
        acc=8,xp=35,gold=(4,10),res={"fire":1.5,"nature":0.0},imm=["Poisoned"],
        ab=[{"name":"Venom Bite","type":"damage","target":"single_enemy","power":12,
             "element":"nature","status":"Poisoned","status_chance":0.5,
             "status_duration":4,"description":"Venomous bite."}],
        desc={0:"A spider with dripping green fangs.",1:"Venomfang Spider",
              2:"Venomfang Spider — potent venom. Priority target."}),

    # ── Abandoned Mine ──
    "Kobold Miner": _e("Kobold Miner",28,3,1,S(8,10,6,5,5,2),14,12,"melee","blunt",
        xp=18,gold=(6,14),
        desc={0:"A scaly humanoid with a pick.",1:"Kobold Miner",
              2:"Kobold Miner — moderate, often in groups."}),
    "Kobold Firebrand": _e("Kobold Firebrand",22,2,5,S(4,10,4,12,8,3),13,8,"ranged","fire",
        acc=3,row="mid",xp=24,gold=(6,14),res={"fire":0.0,"ice":2.0},
        ab=[{"name":"Fire Bolt","type":"damage","target":"single_enemy","power":14,
             "element":"fire","description":"Hurls fire."}],
        desc={0:"A kobold clutching a glowing ember.",1:"Kobold Firebrand",
              2:"Kobold Firebrand — fire magic. Weak to ice."}),
    "Mine Golem": _e("Mine Golem",65,12,6,S(18,4,20,1,2,0),6,22,"melee","blunt",
        ai="defensive",xp=45,gold=(8,20),
        res={"piercing":0.5,"slashing":0.5,"blunt":1.5,"fire":0.5,"lightning":2.0,"nature":0.0},
        imm=["Poisoned","Fear","Sleep"],
        desc={0:"Animated stone and iron.",1:"Mine Golem",
              2:"Mine Golem — very tough, slow. Weak to lightning."}),
    "Dust Wraith": _e("Dust Wraith",35,2,10,S(4,14,6,14,10,2),16,14,"ranged","shadow",
        acc=6,row="mid",xp=38,gold=(5,12),
        res={"piercing":0.3,"slashing":0.3,"blunt":0.5,"shadow":0.0,"divine":2.0,"fire":1.5},
        ab=[{"name":"Life Drain","type":"damage","target":"single_enemy","power":10,
             "element":"shadow","heal_percent":50,"description":"Drains life."}],
        desc={0:"A swirling dust cloud with glowing eyes.",1:"Dust Wraith",
              2:"Dust Wraith — drains life. Use divine/fire."}),
    "Cave-in Beetle": _e("Cave-in Beetle",40,10,2,S(14,6,14,1,3,0),8,14,"melee","blunt",
        ai="defensive",xp=25,gold=(2,6),res={"piercing":0.5,"fire":1.5},
        desc={0:"An armored insect.",1:"Cave-in Beetle",
              2:"Cave-in Beetle — heavy armor. Use blunt or magic."}),

    # ── Sunken Crypt ──
    "Zombie": _e("Zombie",50,3,1,S(12,4,14,1,2,0),6,14,"melee","blunt",
        xp=20,gold=(2,8),
        res={"piercing":0.5,"shadow":0.0,"divine":2.0,"fire":1.5,"nature":1.5},
        imm=["Poisoned","Fear","Sleep"],
        desc={0:"A shambling corpse.",1:"Zombie",
              2:"Zombie — slow, tough. Weak to divine and fire."}),
    "Skeletal Archer": _e("Skeletal Archer",32,3,3,S(6,12,0,3,4,0),14,14,"ranged","piercing",
        acc=5,row="mid",xp=28,gold=(4,12),
        res={"piercing":0.5,"slashing":0.5,"blunt":1.5,"shadow":0.0,"divine":2.0},
        imm=["Poisoned","Fear","Sleep"],
        desc={0:"A skeleton with a bow.",1:"Skeletal Archer",
              2:"Skeletal Archer — ranged undead. Weak to blunt/divine."}),
    "Crypt Shade": _e("Crypt Shade",30,1,12,S(2,16,4,12,12,2),20,10,"ranged","shadow",
        acc=8,row="back",xp=35,gold=(8,18),
        res={"piercing":0.0,"slashing":0.0,"blunt":0.0,"shadow":0.0,"divine":2.5,"fire":1.5,"arcane":1.5},
        imm=["Poisoned","Fear"],
        ab=[{"name":"Shadow Bolt","type":"damage","target":"single_enemy","power":16,
             "element":"shadow","description":"Dark energy bolt."}],
        desc={0:"A translucent dark figure.",1:"Crypt Shade",
              2:"Crypt Shade — immune to physical. Use divine/fire."}),
    "Ghoul": _e("Ghoul",55,5,4,S(14,12,12,3,6,1),14,18,"melee","slashing",
        acc=4,xp=40,gold=(5,15),
        res={"shadow":0.0,"divine":2.0,"fire":1.5},imm=["Poisoned"],
        ab=[{"name":"Paralyzing Touch","type":"debuff","target":"single_enemy",
             "effect":{"stun_chance":0.3,"duration":1},"description":"Can paralyze."}],
        desc={0:"A hunched cadaverous creature.",1:"Ghoul",
              2:"Ghoul — can paralyze. Dangerous in groups."}),
    "Bone Colossus": _e("Bone Colossus",90,10,6,S(20,6,18,2,4,0),8,26,"melee","blunt",
        ai="defensive",xp=60,gold=(15,30),
        res={"piercing":0.3,"slashing":0.5,"blunt":1.5,"shadow":0.0,"divine":2.5},
        imm=["Poisoned","Fear","Sleep","Stun"],
        ab=[{"name":"Bone Storm","type":"damage","target":"aoe_enemy","power":14,
             "element":"piercing","description":"Bone fragments hit all enemies."}],
        desc={0:"A towering mass of fused bones.",1:"Bone Colossus",
              2:"Bone Colossus — elite. AoE bone storm. Use divine/blunt."}),
    "Warden Revenant": _e("Warden Revenant",280,14,12,S(18,12,20,14,16,8),12,24,"melee","shadow",
        acc=8,ai="boss",xp=350,gold=(100,200),
        res={"piercing":0.5,"slashing":0.5,"shadow":0.0,"divine":2.0,"fire":1.5},
        imm=["Poisoned","Fear","Sleep"],ab=["Shadow Strike","Dark Ritual"],
        desc={0:"A spectral knight in Warden armor.",1:"Warden Revenant",
              2:"Warden Revenant — Boss. Corrupted Warden of the Fading."}),

    # ── Ruins of Ashenmoor ──
    "Ashenmoor Bandit": _e("Ashenmoor Bandit",55,6,3,S(14,12,10,6,6,3),15,16,"melee","slashing",
        acc=3,xp=35,gold=(12,28),
        desc={0:"A scarred bandit in mismatched armor.",1:"Ashenmoor Bandit",
              2:"Ashenmoor Bandit — tougher than common bandits."}),
    "Ruin Sentinel": _e("Ruin Sentinel",70,12,8,S(16,8,16,8,10,4),10,20,"melee","slashing",
        acc=4,ai="defensive",xp=50,gold=(10,25),res={"arcane":0.5,"nature":1.5},imm=["Fear"],
        ab=[{"name":"Shield Wall","type":"buff","target":"self",
             "effect":{"defense_boost":1.5,"duration":2},"description":"Raises a barrier."}],
        desc={0:"An animated suit of ancient armor.",1:"Ruin Sentinel",
              2:"Ruin Sentinel — high defense, shield wall. Use magic."}),
    "Fading Cultist": _e("Fading Cultist",38,3,8,S(6,10,6,14,12,8),14,10,"ranged","shadow",
        acc=5,row="back",ai="supportive",xp=40,gold=(8,20),res={"shadow":0.5,"divine":1.5},
        ab=[{"name":"Shadow Heal","type":"heal","target":"single_ally","power":20,
             "description":"Heals an ally with shadow magic."},
            {"name":"Curse","type":"debuff","target":"single_enemy",
             "effect":{"damage_taken_boost":1.3,"duration":3},"description":"Curses target."}],
        desc={0:"A robed figure chanting.",1:"Fading Cultist",
              2:"Fading Cultist — heals allies, curses you. Kill first."}),
    "Corrupted Treant": _e("Corrupted Treant",80,8,4,S(18,4,18,4,8,2),6,22,"melee","blunt",
        ai="defensive",xp=50,gold=(5,15),res={"fire":2.5,"nature":0.0,"slashing":0.5,"ice":0.5},
        ab=[{"name":"Root Slam","type":"damage","target":"aoe_enemy","power":12,
             "element":"nature","description":"Roots slam all enemies."}],
        desc={0:"A twisted tree animated by dark magic.",1:"Corrupted Treant",
              2:"Corrupted Treant — AoE roots. Very weak to fire."}),
    "Shadow Valdris": _e("Shadow Valdris",320,12,16,S(14,14,16,22,18,10),14,20,"ranged","shadow",
        acc=10,row="back",ai="boss",xp=450,gold=(150,300),
        res={"shadow":0.0,"divine":2.0,"arcane":0.5},
        imm=["Poisoned","Fear","Sleep","Stun"],ab=["Shadow Nova","Dark Ritual","Fading Pulse"],
        desc={0:"A dark mirror-image crackling with shadow.",1:"Shadow of Valdris",
              2:"Shadow Valdris — Boss. Echo of the Traitor Warden."}),

    # ── World map general ──
    "Dire Wolf": _e("Dire Wolf",52,4,2,S(14,14,12,3,10,2),20,18,"melee","piercing",
        acc=6,xp=30,gold=(3,8),res={"fire":1.5,"ice":0.5},
        desc={0:"A wolf twice normal size.",1:"Dire Wolf",2:"Dire Wolf — tough pack leader."}),
    "Highway Bandit": _e("Highway Bandit",42,5,2,S(12,12,8,6,6,3),16,14,"melee","slashing",
        acc=3,xp=25,gold=(10,22),
        ab=[{"name":"Cheap Shot","type":"damage","target":"single_enemy","power":18,
             "element":"piercing","description":"Dirty fighting."}],
        desc={0:"A masked figure.",1:"Highway Bandit",2:"Highway Bandit — fights dirty."}),
    "Bandit Crossbowman": _e("Bandit Crossbowman",34,3,2,S(8,14,6,6,8,3),14,16,"ranged","piercing",
        acc=6,row="mid",xp=25,gold=(8,18),
        desc={0:"A bandit with a crossbow.",1:"Bandit Crossbowman",
              2:"Bandit Crossbowman — ranged mid row."}),
    "Swamp Leech": _e("Swamp Leech",25,2,2,S(8,8,10,1,4,0),10,8,"melee","piercing",
        xp=12,gold=(0,3),res={"fire":2.0,"ice":0.5,"nature":0.0},
        ab=[{"name":"Blood Drain","type":"damage","target":"single_enemy","power":6,
             "element":"nature","heal_percent":100,"description":"Drains blood."}],
        desc={0:"A bloated worm.",1:"Swamp Leech",2:"Swamp Leech — heals by draining."}),
    "Marsh Troll": _e("Marsh Troll",75,6,3,S(18,6,16,3,6,2),8,22,"melee","blunt",
        xp=50,gold=(10,25),res={"fire":2.0,"nature":0.5},
        ab=[{"name":"Regenerate","type":"heal","target":"self","power":15,
             "description":"Regenerates HP."}],
        desc={0:"A massive green brute.",1:"Marsh Troll",
              2:"Marsh Troll — regenerates! Use fire."}),
}

# ══════════════════════════════════════════════════════════
#  NEW ENCOUNTERS
# ══════════════════════════════════════════════════════════

NEW_ENCOUNTERS = {
    # ── Goblin Warren ──
    "gw_scouts":      {"name":"Goblin Scouts","difficulty":"easy",
        "groups":[{"enemy":"Goblin Scout","count":4,"row":"front"}]},
    "gw_bats":        {"name":"Bat Swarm","difficulty":"easy",
        "groups":[{"enemy":"Cave Bat","count":6,"row":"front"}]},
    "gw_brute_pack":  {"name":"Goblin Brute & Friends","difficulty":"medium",
        "groups":[{"enemy":"Goblin Brute","count":1,"row":"front"},
                  {"enemy":"Goblin Scout","count":3,"row":"front"}]},
    "gw_trappers":    {"name":"Goblin Ambush","difficulty":"medium",
        "groups":[{"enemy":"Goblin Warrior","count":2,"row":"front"},
                  {"enemy":"Goblin Trapper","count":1,"row":"mid"},
                  {"enemy":"Goblin Archer","count":1,"row":"mid"}]},
    "gw_fungal":      {"name":"Fungal Nest","difficulty":"medium",
        "groups":[{"enemy":"Fungal Crawler","count":2,"row":"front"},
                  {"enemy":"Cave Bat","count":3,"row":"front"}]},
    "gw_deep_patrol": {"name":"Goblin War Band","difficulty":"hard",
        "groups":[{"enemy":"Goblin Brute","count":2,"row":"front"},
                  {"enemy":"Goblin Archer","count":2,"row":"mid"},
                  {"enemy":"Goblin Shaman","count":1,"row":"back"}]},

    # ── Spider's Nest ──
    "sn_spiderlings": {"name":"Spiderling Swarm","difficulty":"easy",
        "groups":[{"enemy":"Spiderling","count":6,"row":"front"}]},
    "sn_web_trap":    {"name":"Web Spinner Ambush","difficulty":"medium",
        "groups":[{"enemy":"Giant Spider","count":2,"row":"front"},
                  {"enemy":"Web Spinner","count":2,"row":"mid"}]},
    "sn_brood":       {"name":"Spider Brood","difficulty":"medium",
        "groups":[{"enemy":"Giant Spider","count":3,"row":"front"},
                  {"enemy":"Spiderling","count":4,"row":"front"}]},
    "sn_venomfang":   {"name":"Venomfang Hunters","difficulty":"hard",
        "groups":[{"enemy":"Venomfang Spider","count":2,"row":"front"},
                  {"enemy":"Spiderling","count":3,"row":"front"}]},
    "sn_nest_guard":  {"name":"Nest Guardians","difficulty":"hard",
        "groups":[{"enemy":"Venomfang Spider","count":1,"row":"front"},
                  {"enemy":"Giant Spider","count":2,"row":"front"},
                  {"enemy":"Web Spinner","count":2,"row":"mid"}]},

    # ── Abandoned Mine ──
    "am_kobolds":     {"name":"Kobold Miners","difficulty":"easy",
        "groups":[{"enemy":"Kobold Miner","count":4,"row":"front"}]},
    "am_kobold_fire": {"name":"Kobold Fire Team","difficulty":"medium",
        "groups":[{"enemy":"Kobold Miner","count":2,"row":"front"},
                  {"enemy":"Kobold Firebrand","count":2,"row":"mid"}]},
    "am_beetles":     {"name":"Beetle Nest","difficulty":"medium",
        "groups":[{"enemy":"Cave-in Beetle","count":3,"row":"front"}]},
    "am_golem":       {"name":"Golem Encounter","difficulty":"hard",
        "groups":[{"enemy":"Mine Golem","count":1,"row":"front"},
                  {"enemy":"Kobold Miner","count":3,"row":"front"}]},
    "am_wraith":      {"name":"Disturbed Spirits","difficulty":"hard",
        "groups":[{"enemy":"Dust Wraith","count":2,"row":"mid"},
                  {"enemy":"Cave-in Beetle","count":2,"row":"front"}]},
    "am_deep":        {"name":"Deep Mine Horrors","difficulty":"hard",
        "groups":[{"enemy":"Mine Golem","count":1,"row":"front"},
                  {"enemy":"Dust Wraith","count":1,"row":"mid"},
                  {"enemy":"Kobold Firebrand","count":2,"row":"mid"}]},

    # ── Sunken Crypt ──
    "sc_zombies":     {"name":"Shambling Dead","difficulty":"easy",
        "groups":[{"enemy":"Zombie","count":4,"row":"front"}]},
    "sc_skel_patrol": {"name":"Skeleton Patrol","difficulty":"medium",
        "groups":[{"enemy":"Skeleton Warrior","count":2,"row":"front"},
                  {"enemy":"Skeletal Archer","count":2,"row":"mid"}]},
    "sc_ghoul_pack":  {"name":"Ghoul Pack","difficulty":"hard",
        "groups":[{"enemy":"Ghoul","count":2,"row":"front"},
                  {"enemy":"Zombie","count":3,"row":"front"}]},
    "sc_shade_haunt": {"name":"Shade Haunting","difficulty":"hard",
        "groups":[{"enemy":"Crypt Shade","count":2,"row":"back"},
                  {"enemy":"Skeleton Warrior","count":2,"row":"front"}]},
    "sc_bone_elite":  {"name":"Bone Colossus Chamber","difficulty":"hard",
        "groups":[{"enemy":"Bone Colossus","count":1,"row":"front"},
                  {"enemy":"Skeletal Archer","count":2,"row":"mid"}]},
    "boss_warden":    {"name":"The Corrupted Warden","difficulty":"boss",
        "groups":[{"enemy":"Warden Revenant","count":1,"row":"front"},
                  {"enemy":"Crypt Shade","count":2,"row":"back"},
                  {"enemy":"Skeleton Warrior","count":2,"row":"front"}]},

    # ── Ruins of Ashenmoor ──
    "ra_bandits":     {"name":"Ashenmoor Raiders","difficulty":"medium",
        "groups":[{"enemy":"Ashenmoor Bandit","count":3,"row":"front"}]},
    "ra_sentinel":    {"name":"Ancient Guardians","difficulty":"hard",
        "groups":[{"enemy":"Ruin Sentinel","count":2,"row":"front"}]},
    "ra_cultists":    {"name":"Fading Cult Cell","difficulty":"hard",
        "groups":[{"enemy":"Ashenmoor Bandit","count":2,"row":"front"},
                  {"enemy":"Fading Cultist","count":2,"row":"back"}]},
    "ra_treant":      {"name":"Corrupted Grove","difficulty":"hard",
        "groups":[{"enemy":"Corrupted Treant","count":1,"row":"front"},
                  {"enemy":"Fading Cultist","count":1,"row":"back"}]},
    "ra_mixed":       {"name":"Ruin Defenders","difficulty":"hard",
        "groups":[{"enemy":"Ruin Sentinel","count":1,"row":"front"},
                  {"enemy":"Ashenmoor Bandit","count":2,"row":"front"},
                  {"enemy":"Fading Cultist","count":1,"row":"back"}]},
    "boss_shadow_v":  {"name":"Shadow of Valdris","difficulty":"boss",
        "groups":[{"enemy":"Shadow Valdris","count":1,"row":"back"},
                  {"enemy":"Ruin Sentinel","count":2,"row":"front"},
                  {"enemy":"Fading Cultist","count":1,"row":"back"}]},

    # ── World map ──
    "wm_wolves_dire": {"name":"Dire Wolf Pack","difficulty":"medium",
        "groups":[{"enemy":"Dire Wolf","count":1,"row":"front"},
                  {"enemy":"Wolf","count":3,"row":"front"}]},
    "wm_highway":     {"name":"Highway Robbery","difficulty":"medium",
        "groups":[{"enemy":"Highway Bandit","count":2,"row":"front"},
                  {"enemy":"Bandit Crossbowman","count":2,"row":"mid"}]},
    "wm_swamp":       {"name":"Swamp Creatures","difficulty":"medium",
        "groups":[{"enemy":"Swamp Leech","count":3,"row":"front"},
                  {"enemy":"Marsh Troll","count":1,"row":"front"}]},
    "wm_troll":       {"name":"Troll Attack","difficulty":"hard",
        "groups":[{"enemy":"Marsh Troll","count":2,"row":"front"}]},
    "wm_bandit_camp": {"name":"Bandit Camp","difficulty":"hard",
        "groups":[{"enemy":"Highway Bandit","count":3,"row":"front"},
                  {"enemy":"Bandit Crossbowman","count":2,"row":"mid"}]},
}

# ══════════════════════════════════════════════════════════
#  NEW DUNGEON ENCOUNTER TABLES (replaces old ones)
# ══════════════════════════════════════════════════════════

NEW_DUNGEON_ENCOUNTER_TABLES = {
    "goblin_warren": {
        1: ["gw_scouts","gw_bats","easy_goblins"],
        2: ["gw_brute_pack","gw_trappers","gw_fungal","medium_goblins"],
        3: ["gw_deep_patrol","gw_brute_pack","gw_trappers"],
        "boss": "boss_goblin_king",
    },
    "spiders_nest": {
        1: ["sn_spiderlings","spider_swarm"],
        2: ["sn_web_trap","sn_brood"],
        3: ["sn_venomfang","sn_web_trap","sn_brood"],
        4: ["sn_nest_guard","sn_venomfang"],
        "boss": "boss_spider_queen",
    },
    "abandoned_mine": {
        1: ["am_kobolds","am_beetles"],
        2: ["am_kobold_fire","am_beetles","am_kobolds"],
        3: ["am_golem","am_kobold_fire","am_wraith"],
        4: ["am_wraith","am_deep","am_golem"],
        5: ["am_deep","am_wraith"],
        "boss": "boss_foreman",
    },
    "sunken_crypt": {
        1: ["sc_zombies","sc_skel_patrol"],
        2: ["sc_skel_patrol","sc_ghoul_pack"],
        3: ["sc_ghoul_pack","sc_shade_haunt"],
        4: ["sc_shade_haunt","sc_bone_elite"],
        "boss": "boss_warden",
    },
    "ruins_ashenmoor": {
        1: ["ra_bandits","ra_sentinel"],
        2: ["ra_cultists","ra_bandits","ra_sentinel"],
        3: ["ra_treant","ra_cultists","ra_mixed"],
        4: ["ra_mixed","ra_treant","ra_cultists"],
        "boss": "boss_shadow_v",
    },
}

# ══════════════════════════════════════════════════════════
#  NEW WORLD MAP ENCOUNTER ZONES (replaces old ones)
# ══════════════════════════════════════════════════════════

NEW_ENCOUNTER_ZONES = {
    "briarhollow": {
        "easy": ["tutorial","easy_goblins","gw_scouts"],
        "medium": ["wolves","wm_wolves_dire","medium_bandits"],
    },
    "thornwood": {
        "easy": ["wolves","gw_bats"],
        "medium": ["wm_wolves_dire","medium_goblins","gw_fungal"],
        "hard": ["wm_highway","medium_bandits"],
    },
    "iron_ridge": {
        "medium": ["am_kobolds","medium_bandits","wm_highway"],
        "hard": ["am_kobold_fire","wm_bandit_camp","hard_mixed"],
    },
    "ashlands": {
        "medium": ["ra_bandits","hard_mixed"],
        "hard": ["ra_cultists","wm_bandit_camp","orc_patrol"],
    },
    "mirehollow": {
        "medium": ["wm_swamp","medium_goblins"],
        "hard": ["wm_troll","wm_swamp","hard_mixed"],
    },
    "pale_coast": {
        "easy": ["easy_goblins","gw_scouts"],
        "medium": ["medium_bandits","wolves"],
    },
    "ocean": {
        "medium": ["medium_bandits"],
        "hard": ["wm_highway"],
    },
}

# ══════════════════════════════════════════════════════════
#  NEW ENEMY ABILITIES (for boss string references)
# ══════════════════════════════════════════════════════════

NEW_ENEMY_ABILITIES = {
    "Shadow Strike": {
        "name": "Shadow Strike", "type": "damage", "target": "single_enemy",
        "power": 28, "element": "shadow",
        "description": "A devastating shadow-infused blade strike.",
    },
    "Dark Ritual": {
        "name": "Dark Ritual", "type": "heal", "target": "self",
        "power": 40,
        "description": "Channels dark energy to restore vitality.",
    },
    "Shadow Nova": {
        "name": "Shadow Nova", "type": "damage", "target": "aoe_enemy",
        "power": 20, "element": "shadow",
        "description": "Erupts shadow energy hitting all enemies.",
    },
    "Fading Pulse": {
        "name": "Fading Pulse", "type": "debuff", "target": "aoe_enemy",
        "effect": {"damage_taken_boost": 1.25, "duration": 2},
        "description": "The Fading weakens all enemies' resistance.",
    },
}
