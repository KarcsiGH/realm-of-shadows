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
    "Goblin Scout": _e("Goblin Scout",50,4,1,S(4,14,3,3,6,1),20,16,"melee","piercing",
        acc=3,xp=10,gold=(2,6),
        desc={0:"A scrawny goblin with a rusty knife.",1:"Goblin Scout",
              2:"Goblin Scout — fast, weak. Often in groups."}),
    "Goblin Brute": _e("Goblin Brute",120,10,2,S(14,6,12,2,3,1),10,36,"melee","blunt",
        xp=28,gold=(8,16),
        desc={0:"A hulking goblin with a wooden club.",1:"Goblin Brute",
              2:"Goblin Brute — slow but hits hard."}),
    "Goblin Trapper": _e("Goblin Trapper",65,5,4,S(5,12,5,7,8,2),15,20,"ranged","piercing",
        acc=4,row="mid",ai="supportive",xp=22,gold=(5,10),
        ab=[{"name":"Caltrops","type":"debuff","target":"single_enemy",
             "effect":{"speed_penalty":0.5,"duration":2},"description":"Slows an enemy."}],
        desc={0:"A goblin fiddling with strange devices.",1:"Goblin Trapper",
              2:"Goblin Trapper — throws caltrops to slow you."}),
    "Cave Bat": _e("Cave Bat",35,4,1,S(3,16,2,1,8,1),24,12,"melee","piercing",
        acc=6,xp=6,gold=(0,2),res={"lightning":1.5,"nature":0.5},
        desc={0:"A screeching bat.",1:"Cave Bat",2:"Cave Bat — fast, fragile."}),
    "Fungal Crawler": _e("Fungal Crawler",75,7,8,S(6,4,10,1,2,1),8,20,"melee","blunt",
        ai="defensive",xp=16,gold=(1,4),res={"nature":0.0,"fire":2.0,"ice":0.5},
        ab=[{"name":"Spore Cloud","type":"damage","target":"aoe_enemy","power":5,
             "element":"nature","status":"Poisoned","status_chance":0.35,
             "status_duration":3,"description":"Toxic spore cloud."}],
        desc={0:"A mushroom creature oozing slime.",1:"Fungal Crawler",
              2:"Fungal Crawler — poison spores. Weak to fire."}),

    # ── Spider's Nest ──
    "Spiderling": _e("Spiderling",30,4,2,S(4,14,3,1,4,1),22,10,"melee","piercing",
        acc=5,xp=6,gold=(0,2),res={"fire":1.5},
        desc={0:"A cat-sized spider.",1:"Spiderling",2:"Spiderling — tiny but numerous."}),
    "Web Spinner": _e("Web Spinner",70,7,10,S(6,12,6,6,8,2),14,16,"ranged","nature",
        acc=4,row="mid",ai="supportive",xp=24,gold=(3,8),res={"fire":2.0,"nature":0.0},
        ab=[{"name":"Web Shot","type":"debuff","target":"single_enemy",
             "effect":{"speed_penalty":0.3,"duration":3},"description":"Sticky web."}],
        desc={0:"A spider dangling silk.",1:"Web Spinner",
              2:"Web Spinner — webs slow your party."}),
    "Venomfang Spider": _e("Venomfang Spider",105,12,8,S(12,14,10,2,8,1),18,32,"melee","piercing",
        acc=8,xp=35,gold=(4,10),res={"fire":1.5,"nature":0.0},imm=["Poisoned"],
        ab=[{"name":"Venom Bite","type":"damage","target":"single_enemy","power":12,
             "element":"nature","status":"Poisoned","status_chance":0.5,
             "status_duration":4,"description":"Venomous bite."}],
        desc={0:"A spider with dripping green fangs.",1:"Venomfang Spider",
              2:"Venomfang Spider — potent venom. Priority target."}),

    # ── Abandoned Mine ──
    "Kobold Miner": _e("Kobold Miner",70,7,2,S(8,10,6,5,5,2),14,24,"melee","blunt",
        xp=18,gold=(6,14),
        desc={0:"A scaly humanoid with a pick.",1:"Kobold Miner",
              2:"Kobold Miner — moderate, often in groups."}),
    "Kobold Firebrand": _e("Kobold Firebrand",55,5,10,S(4,10,4,12,8,3),13,16,"ranged","fire",
        acc=3,row="mid",xp=24,gold=(6,14),res={"fire":0.0,"ice":2.0},
        ab=[{"name":"Fire Bolt","type":"damage","target":"single_enemy","power":14,
             "element":"fire","description":"Hurls fire."}],
        desc={0:"A kobold clutching a glowing ember.",1:"Kobold Firebrand",
              2:"Kobold Firebrand — fire magic. Weak to ice."}),
    "Mine Golem": _e("Mine Golem",162,30,12,S(18,4,20,1,2,0),6,44,"melee","blunt",
        ai="defensive",xp=45,gold=(8,20),
        res={"piercing":0.5,"slashing":0.5,"blunt":1.5,"fire":0.5,"lightning":2.0,"nature":0.0},
        imm=["Poisoned","Fear","Sleep"],
        desc={0:"Animated stone and iron.",1:"Mine Golem",
              2:"Mine Golem — very tough, slow. Weak to lightning."}),
    "Dust Wraith": _e("Dust Wraith",87,5,20,S(4,14,6,14,10,2),16,28,"ranged","shadow",
        acc=6,row="mid",xp=38,gold=(5,12),
        res={"piercing":0.3,"slashing":0.3,"blunt":0.5,"shadow":0.0,"divine":2.0,"fire":1.5},
        ab=[{"name":"Life Drain","type":"damage","target":"single_enemy","power":10,
             "element":"shadow","heal_percent":50,"description":"Drains life."}],
        desc={0:"A swirling dust cloud with glowing eyes.",1:"Dust Wraith",
              2:"Dust Wraith — drains life. Use divine/fire."}),
    "Cave-in Beetle": _e("Cave-in Beetle",100,25,4,S(14,6,14,1,3,0),8,28,"melee","blunt",
        ai="defensive",xp=25,gold=(2,6),res={"piercing":0.5,"fire":1.5},
        desc={0:"An armored insect.",1:"Cave-in Beetle",
              2:"Cave-in Beetle — heavy armor. Use blunt or magic."}),

    # ── Sunken Crypt ──
    "Zombie": _e("Zombie",125,7,2,S(12,4,14,1,2,0),6,28,"melee","blunt",
        xp=20,gold=(2,8),
        res={"piercing":0.5,"shadow":0.0,"divine":2.0,"fire":1.5,"nature":1.5},
        imm=["Poisoned","Fear","Sleep"],
        desc={0:"A shambling corpse.",1:"Zombie",
              2:"Zombie — slow, tough. Weak to divine and fire."}),
    "Skeletal Archer": _e("Skeletal Archer",80,7,6,S(6,12,0,3,4,0),14,28,"ranged","piercing",
        acc=5,row="mid",xp=28,gold=(4,12),
        res={"piercing":0.5,"slashing":0.5,"blunt":1.5,"shadow":0.0,"divine":2.0},
        imm=["Poisoned","Fear","Sleep"],
        desc={0:"A skeleton with a bow.",1:"Skeletal Archer",
              2:"Skeletal Archer — ranged undead. Weak to blunt/divine."}),
    "Crypt Shade": _e("Crypt Shade",75,4,24,S(2,16,4,12,12,2),20,20,"ranged","shadow",
        acc=8,row="back",xp=35,gold=(8,18),
        res={"piercing":0.0,"slashing":0.0,"blunt":0.0,"shadow":0.0,"divine":2.5,"fire":1.5,"arcane":1.5},
        imm=["Poisoned","Fear"],
        ab=[{"name":"Shadow Bolt","type":"damage","target":"single_enemy","power":16,
             "element":"shadow","description":"Dark energy bolt."}],
        desc={0:"A translucent dark figure.",1:"Crypt Shade",
              2:"Crypt Shade — immune to physical. Use divine/fire."}),
    "Ghoul": _e("Ghoul",137,12,8,S(14,12,12,3,6,1),14,36,"melee","slashing",
        acc=4,xp=40,gold=(5,15),
        res={"shadow":0.0,"divine":2.0,"fire":1.5},imm=["Poisoned"],
        ab=[{"name":"Paralyzing Touch","type":"debuff","target":"single_enemy",
             "effect":{"stun_chance":0.3,"duration":1},"description":"Can paralyze."}],
        desc={0:"A hunched cadaverous creature.",1:"Ghoul",
              2:"Ghoul — can paralyze. Dangerous in groups."}),
    "Bone Colossus": _e("Bone Colossus",225,25,12,S(20,6,18,2,4,0),8,52,"melee","blunt",
        ai="defensive",xp=60,gold=(15,30),
        res={"piercing":0.3,"slashing":0.5,"blunt":1.5,"shadow":0.0,"divine":2.5},
        imm=["Poisoned","Fear","Sleep","Stun"],
        ab=[{"name":"Bone Storm","type":"damage","target":"aoe_enemy","power":14,
             "element":"piercing","description":"Bone fragments hit all enemies."}],
        desc={0:"A towering mass of fused bones.",1:"Bone Colossus",
              2:"Bone Colossus — elite. AoE bone storm. Use divine/blunt."}),
    "Warden Revenant": _e("Warden Revenant",1000,35,24,S(18,12,20,14,16,8),12,48,"melee","shadow",
        acc=8,ai="boss",xp=350,gold=(100,200),
        res={"piercing":0.5,"slashing":0.5,"shadow":0.0,"divine":2.0,"fire":1.5},
        imm=["Poisoned","Fear","Sleep"],ab=["Shadow Strike","Dark Ritual"],
        desc={0:"A spectral knight in Warden armor.",1:"Warden Revenant",
              2:"Warden Revenant — Boss. Corrupted Warden of the Fading."}),

    # ── Ruins of Ashenmoor ──
    "Ashenmoor Bandit": _e("Ashenmoor Bandit",137,15,6,S(14,12,10,6,6,3),15,32,"melee","slashing",
        acc=3,xp=35,gold=(12,28),
        desc={0:"A scarred bandit in mismatched armor.",1:"Ashenmoor Bandit",
              2:"Ashenmoor Bandit — tougher than common bandits."}),
    "Ruin Sentinel": _e("Ruin Sentinel",175,30,16,S(16,8,16,8,10,4),10,40,"melee","slashing",
        acc=4,ai="defensive",xp=50,gold=(10,25),res={"arcane":0.5,"nature":1.5},imm=["Fear"],
        ab=[{"name":"Shield Wall","type":"buff","target":"self",
             "effect":{"defense_boost":1.5,"duration":2},"description":"Raises a barrier."}],
        desc={0:"An animated suit of ancient armor.",1:"Ruin Sentinel",
              2:"Ruin Sentinel — high defense, shield wall. Use magic."}),
    "Fading Cultist": _e("Fading Cultist",95,7,16,S(6,10,6,14,12,8),14,20,"ranged","shadow",
        acc=5,row="back",ai="supportive",xp=40,gold=(8,20),res={"shadow":0.5,"divine":1.5},
        ab=[{"name":"Shadow Heal","type":"heal","target":"single_ally","power":20,
             "description":"Heals an ally with shadow magic."},
            {"name":"Curse","type":"debuff","target":"single_enemy",
             "effect":{"damage_taken_boost":1.3,"duration":3},"description":"Curses target."}],
        desc={0:"A robed figure chanting.",1:"Fading Cultist",
              2:"Fading Cultist — heals allies, curses you. Kill first."}),
    "Corrupted Treant": _e("Corrupted Treant",200,20,8,S(18,4,18,4,8,2),6,44,"melee","blunt",
        ai="defensive",xp=50,gold=(5,15),res={"fire":2.5,"nature":0.0,"slashing":0.5,"ice":0.5},
        ab=[{"name":"Root Slam","type":"damage","target":"aoe_enemy","power":12,
             "element":"nature","description":"Roots slam all enemies."}],
        desc={0:"A twisted tree animated by dark magic.",1:"Corrupted Treant",
              2:"Corrupted Treant — AoE roots. Very weak to fire."}),
    "Shadow Valdris": _e("Shadow Valdris",1125,30,32,S(14,14,16,22,18,10),14,40,"ranged","shadow",
        acc=10,row="back",ai="boss",xp=450,gold=(150,300),
        res={"shadow":0.0,"divine":2.0,"arcane":0.5},
        imm=["Poisoned","Fear","Sleep","Stun"],ab=["Shadow Nova","Dark Ritual","Fading Pulse"],
        desc={0:"A dark mirror-image crackling with shadow.",1:"Shadow of Valdris",
              2:"Shadow Valdris — Boss. Echo of the Traitor Warden."}),

    # ── World map general ──
    "Dire Wolf": _e("Dire Wolf",130,10,4,S(14,14,12,3,10,2),20,36,"melee","piercing",
        acc=6,xp=30,gold=(3,8),res={"fire":1.5,"ice":0.5},
        desc={0:"A wolf twice normal size.",1:"Dire Wolf",2:"Dire Wolf — tough pack leader."}),
    "Highway Bandit": _e("Highway Bandit",105,12,4,S(12,12,8,6,6,3),16,28,"melee","slashing",
        acc=3,xp=25,gold=(10,22),
        ab=[{"name":"Cheap Shot","type":"damage","target":"single_enemy","power":18,
             "element":"piercing","description":"Dirty fighting."}],
        desc={0:"A masked figure.",1:"Highway Bandit",2:"Highway Bandit — fights dirty."}),
    "Bandit Crossbowman": _e("Bandit Crossbowman",85,7,4,S(8,14,6,6,8,3),14,32,"ranged","piercing",
        acc=6,row="mid",xp=25,gold=(8,18),
        desc={0:"A bandit with a crossbow.",1:"Bandit Crossbowman",
              2:"Bandit Crossbowman — ranged mid row."}),
    "Swamp Leech": _e("Swamp Leech",62,5,4,S(8,8,10,1,4,0),10,16,"melee","piercing",
        xp=12,gold=(0,3),res={"fire":2.0,"ice":0.5,"nature":0.0},
        ab=[{"name":"Blood Drain","type":"damage","target":"single_enemy","power":6,
             "element":"nature","heal_percent":100,"description":"Drains blood."}],
        desc={0:"A bloated worm.",1:"Swamp Leech",2:"Swamp Leech — heals by draining."}),
    "Marsh Troll": _e("Marsh Troll",187,15,6,S(18,6,16,3,6,2),8,44,"melee","blunt",
        xp=50,gold=(10,25),res={"fire":2.0,"nature":0.5},
        ab=[{"name":"Regenerate","type":"heal","target":"self","power":15,
             "description":"Regenerates HP."}],
        desc={0:"A massive green brute.",1:"Marsh Troll",
              2:"Marsh Troll — regenerates! Use fire."}),

    # ══════════════════════════════════════════════════════════
    #  ADDITIONAL ENEMIES — More variety per theme
    # ══════════════════════════════════════════════════════════

    # ── More cave/goblin ──
    "Goblin Drummer": _e("Goblin Drummer",55,4,2,S(4,8,4,4,6,4),12,12,"melee","blunt",
        row="back",ai="supportive",xp=18,gold=(3,8),
        ab=[{"name":"War Drums","type":"buff","target":"all_allies",
             "effect":{"speed_boost":1.2,"duration":2},"description":"Drums speed allies up."}],
        desc={0:"A goblin beating a crude drum.",1:"Goblin Drummer",
              2:"Goblin Drummer — buffs ally speed. Low threat alone."}),
    "Rabid Rat": _e("Rabid Rat",25,3,1,S(3,14,3,1,4,0),22,10,"melee","piercing",
        acc=4,xp=4,gold=(0,1),
        ab=[{"name":"Rabid Bite","type":"damage","target":"single_enemy","power":4,
             "element":"nature","status":"Poisoned","status_chance":0.2,
             "status_duration":2,"description":"Diseased bite."}],
        desc={0:"A mangy, snarling rat.",1:"Rabid Rat",2:"Rabid Rat — weak but can poison."}),
    "Tunnel Lurker": _e("Tunnel Lurker",95,12,6,S(12,10,10,3,6,1),12,32,"melee","piercing",
        acc=5,xp=26,gold=(4,10),
        ab=[{"name":"Ambush Strike","type":"damage","target":"single_enemy","power":20,
             "element":"piercing","description":"Surprise lunge from darkness."}],
        loot=[{"drop_chance":0.10,"item":{"name":"Lurker Fang","type":"material",
             "subtype":"reagent","rarity":"common","tier":1,"identified":True,
             "estimated_value":8,"description":"A sharp fang from a tunnel lurker."}}],
        desc={0:"A pale, eyeless predator.",1:"Tunnel Lurker",
              2:"Tunnel Lurker — ambush attacks hit hard."}),

    # ── More spiders ──
    "Egg Sac": _e("Egg Sac",50,5,1,S(0,0,8,0,0,0),1,0,"melee","blunt",
        ai="defensive",xp=5,gold=(0,0),res={"fire":3.0},
        ab=[{"name":"Hatch","type":"summon","target":"self",
             "effect":{"spawn":"Spiderling","count":2},"description":"Hatches spiderlings."}],
        desc={0:"A pulsing silk egg sac.",1:"Egg Sac",2:"Egg Sac — destroy before it hatches!"}),
    "Broodmother Guard": _e("Broodmother Guard",137,17,10,S(16,10,14,2,8,1),14,40,"melee","piercing",
        acc=6,xp=42,gold=(5,14),res={"fire":1.5,"nature":0.0},imm=["Poisoned"],
        loot=[{"drop_chance":0.12,"item":{"name":"Chitinous Plate","type":"material",
             "subtype":"armor_mat","rarity":"uncommon","tier":2,"identified":True,
             "estimated_value":20,"description":"Hard spider chitin, useful for armor crafting."}}],
        desc={0:"An enormous armored spider.",1:"Broodmother Guard",
              2:"Broodmother Guard — elite spider. Tough and venomous."}),
    "Phase Spider": _e("Phase Spider",80,5,16,S(8,18,6,10,10,2),22,28,"melee","piercing",
        acc=10,xp=38,gold=(6,14),res={"arcane":0.0,"fire":1.5},
        ab=[{"name":"Phase Shift","type":"buff","target":"self",
             "effect":{"evasion_boost":1.5,"duration":1},"description":"Phases partially out of reality."}],
        desc={0:"A spider that flickers in and out of sight.",1:"Phase Spider",
              2:"Phase Spider — very fast, phases to dodge. Use magic."}),

    # ── More mine ──
    "Kobold Trapsmith": _e("Kobold Trapsmith",60,5,6,S(5,12,4,10,8,3),14,16,"ranged","piercing",
        acc=4,row="mid",ai="supportive",xp=22,gold=(5,12),
        ab=[{"name":"Blinding Bomb","type":"debuff","target":"single_enemy",
             "effect":{"accuracy_penalty":0.5,"duration":2},"description":"Blinds with flash powder."}],
        desc={0:"A kobold with pouches of strange powder.",1:"Kobold Trapsmith",
              2:"Kobold Trapsmith — blinds with flash bombs."}),
    "Crystal Elemental": _e("Crystal Elemental",125,35,20,S(14,4,16,8,6,0),6,36,"melee","piercing",
        ai="defensive",xp=45,gold=(12,30),
        res={"piercing":0.3,"slashing":0.5,"blunt":2.0,"lightning":0.5,"fire":0.5,"nature":1.5},
        imm=["Poisoned","Fear","Sleep"],
        loot=[{"drop_chance":0.15,"item":{"name":"Crystal Shard","type":"material",
             "subtype":"gem","rarity":"uncommon","tier":2,"identified":True,
             "estimated_value":25,"description":"A glowing crystal fragment with arcane resonance."}}],
        desc={0:"A living cluster of crystals.",1:"Crystal Elemental",
              2:"Crystal Elemental — very high armor. Weak to blunt."}),
    "Mine Rat Swarm": _e("Mine Rat Swarm",45,3,1,S(4,12,4,1,3,0),18,14,"melee","piercing",
        acc=3,xp=8,gold=(0,2),
        desc={0:"A chittering mass of rats.",1:"Rat Swarm",2:"Rat Swarm — annoying in numbers."}),

    # ── More crypt ──
    "Wailing Spirit": _e("Wailing Spirit",62,3,28,S(1,12,4,10,14,4),16,16,"ranged","shadow",
        acc=6,row="back",xp=30,gold=(3,10),
        res={"piercing":0.0,"slashing":0.0,"blunt":0.0,"shadow":0.0,"divine":2.5},
        imm=["Poisoned","Fear","Sleep","Stun"],
        ab=[{"name":"Wail","type":"debuff","target":"aoe_enemy",
             "effect":{"damage_penalty":0.8,"duration":2},"description":"Demoralizing wail."}],
        desc={0:"A translucent weeping figure.",1:"Wailing Spirit",
              2:"Wailing Spirit — AoE debuff wail. Immune to physical."}),
    "Plague Bearer": _e("Plague Bearer",150,10,4,S(14,6,16,2,4,0),8,24,"melee","blunt",
        xp=32,gold=(3,10),res={"shadow":0.0,"divine":2.0,"fire":1.5,"nature":0.5},
        imm=["Poisoned"],
        ab=[{"name":"Plague Touch","type":"damage","target":"single_enemy","power":8,
             "element":"nature","status":"Poisoned","status_chance":0.6,
             "status_duration":4,"description":"Spreads disease."}],
        desc={0:"A bloated undead oozing foul liquid.",1:"Plague Bearer",
              2:"Plague Bearer — high poison chance. Prioritize."}),
    "Death Knight": _e("Death Knight",187,30,16,S(18,8,16,6,8,2),10,48,"melee","slashing",
        acc=5,xp=55,gold=(15,35),
        res={"piercing":0.5,"shadow":0.0,"divine":2.0},imm=["Poisoned","Fear"],
        ab=[{"name":"Death Strike","type":"damage","target":"single_enemy","power":28,
             "element":"shadow","description":"A devastating shadow-infused blow."}],
        loot=[{"drop_chance":0.10,"item":{"name":"Dark Iron Shard","type":"material",
             "subtype":"metal","rarity":"uncommon","tier":2,"identified":True,
             "estimated_value":30,"description":"A shard of shadow-touched iron."}}],
        desc={0:"An armored undead knight radiating malice.",1:"Death Knight",
              2:"Death Knight — elite undead. Shadow attacks, high defense."}),

    # ── More ruins ──
    "Ashenmoor Crossbowman": _e("Ashenmoor Crossbowman",100,10,4,S(8,14,8,5,6,3),14,36,"ranged","piercing",
        acc=6,row="mid",xp=32,gold=(10,22),
        desc={0:"A bandit with a heavy crossbow.",1:"Ashenmoor Crossbowman",
              2:"Ashenmoor Crossbowman — ranged threat."}),
    "Fading Abomination": _e("Fading Abomination",212,15,20,S(20,6,18,4,6,2),8,52,"melee","shadow",
        acc=4,xp=60,gold=(10,25),res={"shadow":0.0,"divine":2.5,"fire":1.5},
        imm=["Poisoned","Fear","Stun"],
        ab=[{"name":"Corruption Slam","type":"damage","target":"aoe_enemy","power":16,
             "element":"shadow","description":"Slams with corrupted force."}],
        desc={0:"A twisted mass of flesh and shadow.",1:"Fading Abomination",
              2:"Fading Abomination — elite. AoE shadow. Use divine."}),
    "Ruin Archer": _e("Ruin Archer",87,7,8,S(6,14,6,6,8,4),16,28,"ranged","piercing",
        acc=6,row="mid",xp=28,gold=(6,16),res={"arcane":0.5},
        desc={0:"An animated skeleton drawing an ancient bow.",1:"Ruin Archer",
              2:"Ruin Archer — ranged, moderate threat."}),
    "Gargoyle": _e("Gargoyle",162,35,12,S(16,8,14,4,6,2),10,40,"melee","blunt",
        ai="defensive",xp=48,gold=(5,15),
        res={"piercing":0.3,"slashing":0.5,"blunt":1.5,"lightning":2.0},
        imm=["Poisoned","Fear","Sleep"],
        loot=[{"drop_chance":0.08,"item":{"name":"Gargoyle Stone","type":"material",
             "subtype":"stone","rarity":"uncommon","tier":2,"identified":True,
             "estimated_value":18,"description":"Enchanted stone from a gargoyle."}}],
        desc={0:"A stone figure that moves.",1:"Gargoyle",
              2:"Gargoyle — very high armor. Weak to blunt/lightning."}),

    # ── Briarhollow Attack (Act 1 Climax) ──
    "Shadow Stalker": _e("Shadow Stalker",110,6,28,S(8,18,8,10,10,2),22,30,"melee","shadow",
        acc=10,row="front",ai="aggressive",xp=55,gold=(12,22),
        res={"piercing":0.0,"slashing":0.0,"blunt":0.0,
             "fire":1.5,"ice":1.0,"lightning":1.0,
             "divine":2.5,"shadow":0.0,"nature":1.0,"arcane":1.5},
        imm=["Poisoned","Fear","Sleep"],
        ab=[{"name":"Shadow Strike","type":"damage","target":"single_enemy","power":18,
             "element":"shadow","description":"A blade of pure shadow energy."}],
        loot=[{"drop_chance":0.40,"item":{"name":"Shadow Essence","type":"material",
               "rarity":"uncommon","identified":True,"estimated_value":35,
               "description":"A dense droplet of shadow energy. Warm to the touch."}}],
        desc={0:"A humanoid shape woven from shadow, nearly invisible until it moves.",
              1:"Shadow Stalker",
              2:"Shadow Stalker — immune to physical damage. Use divine, fire, or arcane."}),

    "Shadow Brute": _e("Shadow Brute",220,12,20,S(18,8,20,6,6,2),8,48,"melee","shadow",
        acc=5,row="front",ai="defensive",xp=75,gold=(15,30),
        res={"piercing":0.0,"slashing":0.0,"blunt":0.5,
             "fire":1.5,"ice":1.0,"lightning":1.0,
             "divine":2.5,"shadow":0.0,"nature":1.0,"arcane":1.5},
        imm=["Poisoned","Fear","Charm"],
        ab=[{"name":"Shadow Slam","type":"damage","target":"single_enemy","power":30,
             "element":"shadow","description":"Crushes with shadow-hardened fists."}],
        loot=[{"drop_chance":0.50,"item":{"name":"Dense Shadow Core","type":"material",
               "rarity":"rare","identified":True,"estimated_value":70,
               "description":"A fist-sized mass of compacted shadow energy. Cold on one side, burning on the other."}}],
        desc={0:"A massive shadow-creature, hunched and slow but devastatingly powerful.",
              1:"Shadow Brute",
              2:"Shadow Brute — immune to piercing/slashing. Heavy hitter. Use divine or fire."}),

    # ── Dragon's Tooth (Act 2 volcanic island dungeon) ──
    "Corrupted Hatchling": _e("Corrupted Hatchling",95,8,18,S(10,16,8,4,4,0),18,28,"melee","fire",
        acc=6,row="front",ai="aggressive",xp=45,gold=(10,20),
        res={"piercing":1.0,"slashing":1.0,"blunt":1.0,"fire":0.0,"ice":2.0,
             "lightning":1.0,"divine":1.0,"shadow":1.5,"nature":1.0,"arcane":1.0},
        imm=["Poisoned","Burning"],
        ab=[{"name":"Fire Breath","type":"damage","target":"single_enemy","power":18,
             "element":"fire","description":"A gout of flame."}],
        loot=[{"drop_chance":0.30,"item":{"name":"Hatchling Scale","type":"material",
               "rarity":"common","identified":True,"estimated_value":12,
               "description":"A small scale, still warm."}}],
        desc={0:"A young dragon, twisted by corruption. Eyes glow sickly orange.",
              1:"Corrupted Hatchling",
              2:"Corrupted Hatchling — fire immune. Use ice."}),

    "Lava Beetle": _e("Lava Beetle",130,32,8,S(14,4,18,1,2,0),5,38,"melee","blunt",
        acc=0,row="front",ai="defensive",xp=50,gold=(8,16),
        res={"piercing":0.3,"slashing":0.5,"blunt":0.5,"fire":0.0,"ice":2.0,
             "lightning":1.5,"divine":1.0,"shadow":1.0,"nature":1.0,"arcane":1.0},
        imm=["Poisoned","Burning","Fear"],
        loot=[{"drop_chance":0.40,"item":{"name":"Lava Carapace Fragment","type":"material",
               "rarity":"uncommon","identified":True,"estimated_value":25,
               "description":"Volcanic shell, absorbs heat."}}],
        desc={0:"An armored insect crusted with cooled magma.",
              1:"Lava Beetle",
              2:"Lava Beetle — very high armor. Fire immune. Slow. Use ice or lightning."}),

    "Cinder Drake": _e("Cinder Drake",115,14,22,S(12,18,10,6,8,0),20,34,"ranged","fire",
        acc=8,row="mid",ai="aggressive",xp=55,gold=(12,24),
        res={"piercing":1.0,"slashing":1.0,"blunt":1.0,"fire":0.0,"ice":2.5,
             "lightning":1.0,"divine":1.0,"shadow":1.5,"nature":0.5,"arcane":1.0},
        imm=["Poisoned","Burning"],
        ab=[{"name":"Cinder Spit","type":"damage","target":"single_enemy","power":22,
             "element":"fire","description":"Spits burning embers."},
            {"name":"Ignite","type":"debuff","target":"single_enemy",
             "effect":{"burning_chance":0.35,"duration":2},"description":"Sets target ablaze."}],
        loot=[{"drop_chance":0.35,"item":{"name":"Drake Fire Gland","type":"material",
               "rarity":"uncommon","identified":True,"estimated_value":40,
               "description":"Still smoldering. Useful in fire-based alchemy."}}],
        desc={0:"A winged drake wreathed in cinders.",
              1:"Cinder Drake",
              2:"Cinder Drake — fire immune. Can inflict Burning. Vulnerable to ice."}),

    "Volcanic Troll": _e("Volcanic Troll",260,16,12,S(22,6,24,3,4,0),7,55,"melee","blunt",
        acc=2,row="front",ai="defensive",xp=70,gold=(15,28),
        res={"piercing":1.0,"slashing":1.0,"blunt":1.0,"fire":0.5,"ice":2.0,
             "lightning":1.0,"divine":1.0,"shadow":1.0,"nature":1.0,"arcane":1.0},
        imm=["Poisoned","Fear"],
        ab=[{"name":"Molten Slam","type":"damage","target":"single_enemy","power":32,
             "element":"fire","description":"Slams with magma-coated fists."}],
        loot=[{"drop_chance":0.25,"item":{"name":"Volcanic Stone","type":"material",
               "rarity":"uncommon","identified":True,"estimated_value":20,
               "description":"Porous volcanic rock, faintly warm."}}],
        desc={0:"A massive troll adapted to volcanic heat. Skin like cooling lava.",
              1:"Volcanic Troll",
              2:"Volcanic Troll — tough, slow. Ice doubles damage. Fire-resistant."}),

    "Karreth": _e("Karreth",680,46,40,S(26,10,28,16,20,8),12,80,"melee","fire",
        acc=8,row="front",ai="aggressive",xp=500,gold=(200,400),
        res={"piercing":0.5,"slashing":0.5,"blunt":0.5,"fire":0.0,"ice":2.5,
             "lightning":1.0,"divine":1.5,"shadow":1.5,"nature":0.5,"arcane":1.0},
        imm=["Poisoned","Burning","Fear","Charm","Sleep"],
        ab=[{"name":"Dragon's Breath","type":"damage","target":"aoe_enemy","power":40,
             "element":"fire","description":"A devastating cone of dragon fire."},
            {"name":"Wing Buffet","type":"debuff","target":"aoe_enemy",
             "effect":{"stun_chance":0.25,"duration":1},"description":"Sweeping wings can stun the party."},
            {"name":"Fading Claw","type":"damage","target":"single_enemy","power":50,
             "element":"shadow","description":"A claw strike with shadow corruption."}],
        loot=[{"drop_chance":1.00,"item":{"name":"Hearthstone Fragment (Dragon's Tooth)","type":"key_item",
               "rarity":"legendary","identified":True,"estimated_value":0,
               "description":"A Hearthstone fragment, warm with dragon-fire. The third recovered."}},
              {"drop_chance":0.85,"item":{"name":"Dragon Scale","type":"key_item",
               "rarity":"legendary","identified":True,"estimated_value":0,
               "description":"A scale from Karreth. It seems to resonate with ward-energy."}}],
        desc={0:"An enormous dragon, eyes burning with twin fires — natural and corrupted.",
              1:"Karreth",
              2:"Karreth — Final Boss. Fire immune. Ice deals 2.5x. AoE fire breath. Very high HP."}),
}

# ══════════════════════════════════════════════════════════
#  NEW ENCOUNTERS
# ══════════════════════════════════════════════════════════

NEW_ENCOUNTERS = {
    # ── Dragon's Tooth ──
    "dt_hatchlings":  {"name":"Hatchling Pack","difficulty":"easy",
        "groups":[{"enemy":"Corrupted Hatchling","count":3,"row":"front"}]},
    "dt_beetles":     {"name":"Lava Beetles","difficulty":"medium",
        "groups":[{"enemy":"Lava Beetle","count":2,"row":"front"},
                  {"enemy":"Corrupted Hatchling","count":2,"row":"front"}]},
    "dt_drakes":      {"name":"Cinder Drakes","difficulty":"medium",
        "groups":[{"enemy":"Cinder Drake","count":2,"row":"mid"},
                  {"enemy":"Corrupted Hatchling","count":1,"row":"front"}]},
    "dt_troll":       {"name":"Volcanic Troll","difficulty":"hard",
        "groups":[{"enemy":"Volcanic Troll","count":1,"row":"front"},
                  {"enemy":"Corrupted Hatchling","count":2,"row":"front"}]},
    "dt_drake_swarm": {"name":"Drake Swarm","difficulty":"hard",
        "groups":[{"enemy":"Cinder Drake","count":3,"row":"mid"},
                  {"enemy":"Lava Beetle","count":1,"row":"front"}]},
    "dt_mixed":       {"name":"Volcanic Pack","difficulty":"hard",
        "groups":[{"enemy":"Volcanic Troll","count":1,"row":"front"},
                  {"enemy":"Cinder Drake","count":2,"row":"mid"},
                  {"enemy":"Corrupted Hatchling","count":1,"row":"front"}]},
    "boss_karreth":   {"name":"Karreth the Corrupted","difficulty":"boss",
        "groups":[{"enemy":"Karreth","count":1,"row":"front"},
                  {"enemy":"Cinder Drake","count":2,"row":"mid"}]},

    # ── Story Events ──
    "briarhollow_attack": {"name":"Shadow Attack on Briarhollow","difficulty":"hard",
        "groups":[{"enemy":"Shadow Brute","count":1,"row":"front"},
                  {"enemy":"Shadow Stalker","count":2,"row":"front"}]},

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

    # ── Additional encounters for more variety ──

    # Goblin Warren extras
    "gw_rats":        {"name":"Rat Infestation","difficulty":"easy",
        "groups":[{"enemy":"Rabid Rat","count":5,"row":"front"}]},
    "gw_lurkers":     {"name":"Tunnel Lurkers","difficulty":"medium",
        "groups":[{"enemy":"Tunnel Lurker","count":2,"row":"front"},
                  {"enemy":"Cave Bat","count":3,"row":"front"}]},
    "gw_drummer":     {"name":"Goblin Drum Circle","difficulty":"medium",
        "groups":[{"enemy":"Goblin Warrior","count":3,"row":"front"},
                  {"enemy":"Goblin Drummer","count":1,"row":"back"}]},
    "gw_mixed_easy":  {"name":"Goblin Foragers","difficulty":"easy",
        "groups":[{"enemy":"Goblin Scout","count":2,"row":"front"},
                  {"enemy":"Rabid Rat","count":3,"row":"front"}]},
    "gw_brute_shaman":{"name":"Goblin Elite Guard","difficulty":"hard",
        "groups":[{"enemy":"Goblin Brute","count":1,"row":"front"},
                  {"enemy":"Goblin Warrior","count":2,"row":"front"},
                  {"enemy":"Goblin Shaman","count":1,"row":"back"},
                  {"enemy":"Goblin Drummer","count":1,"row":"back"}]},

    # Spider's Nest extras
    "sn_phase":       {"name":"Phase Spider Hunt","difficulty":"hard",
        "groups":[{"enemy":"Phase Spider","count":2,"row":"front"},
                  {"enemy":"Spiderling","count":4,"row":"front"}]},
    "sn_eggs":        {"name":"Egg Chamber","difficulty":"medium",
        "groups":[{"enemy":"Egg Sac","count":3,"row":"front"},
                  {"enemy":"Giant Spider","count":2,"row":"front"}]},
    "sn_brood_guard": {"name":"Broodmother's Guard","difficulty":"hard",
        "groups":[{"enemy":"Broodmother Guard","count":1,"row":"front"},
                  {"enemy":"Giant Spider","count":2,"row":"front"},
                  {"enemy":"Web Spinner","count":1,"row":"mid"}]},
    "sn_mixed_easy":  {"name":"Spider Scouts","difficulty":"easy",
        "groups":[{"enemy":"Spiderling","count":3,"row":"front"},
                  {"enemy":"Giant Spider","count":1,"row":"front"}]},
    "sn_venom_web":   {"name":"Venom & Web","difficulty":"hard",
        "groups":[{"enemy":"Venomfang Spider","count":1,"row":"front"},
                  {"enemy":"Web Spinner","count":2,"row":"mid"},
                  {"enemy":"Spiderling","count":2,"row":"front"}]},

    # Abandoned Mine extras
    "am_rats":        {"name":"Mine Rat Nest","difficulty":"easy",
        "groups":[{"enemy":"Mine Rat Swarm","count":4,"row":"front"}]},
    "am_crystal":     {"name":"Crystal Cavern","difficulty":"hard",
        "groups":[{"enemy":"Crystal Elemental","count":1,"row":"front"},
                  {"enemy":"Kobold Firebrand","count":2,"row":"mid"}]},
    "am_trap_squad":  {"name":"Kobold Trap Squad","difficulty":"medium",
        "groups":[{"enemy":"Kobold Miner","count":2,"row":"front"},
                  {"enemy":"Kobold Trapsmith","count":2,"row":"mid"}]},
    "am_mixed_med":   {"name":"Mine Denizens","difficulty":"medium",
        "groups":[{"enemy":"Kobold Miner","count":2,"row":"front"},
                  {"enemy":"Cave-in Beetle","count":2,"row":"front"}]},
    "am_golem_duo":   {"name":"Golem Guardians","difficulty":"hard",
        "groups":[{"enemy":"Mine Golem","count":2,"row":"front"}]},

    # Sunken Crypt extras
    "sc_plague":      {"name":"Plague Carriers","difficulty":"medium",
        "groups":[{"enemy":"Plague Bearer","count":2,"row":"front"},
                  {"enemy":"Zombie","count":2,"row":"front"}]},
    "sc_wailing":     {"name":"Wailing Spirits","difficulty":"medium",
        "groups":[{"enemy":"Wailing Spirit","count":2,"row":"back"},
                  {"enemy":"Zombie","count":3,"row":"front"}]},
    "sc_death_knight":{"name":"Death Knight Patrol","difficulty":"hard",
        "groups":[{"enemy":"Death Knight","count":1,"row":"front"},
                  {"enemy":"Skeleton Warrior","count":2,"row":"front"},
                  {"enemy":"Skeletal Archer","count":1,"row":"mid"}]},
    "sc_mixed_easy":  {"name":"Restless Dead","difficulty":"easy",
        "groups":[{"enemy":"Zombie","count":2,"row":"front"},
                  {"enemy":"Skeleton Warrior","count":1,"row":"front"}]},
    "sc_undead_horde":{"name":"Undead Horde","difficulty":"hard",
        "groups":[{"enemy":"Zombie","count":3,"row":"front"},
                  {"enemy":"Skeletal Archer","count":2,"row":"mid"},
                  {"enemy":"Plague Bearer","count":1,"row":"front"}]},

    # Ruins of Ashenmoor extras
    "ra_gargoyles":   {"name":"Gargoyle Perch","difficulty":"hard",
        "groups":[{"enemy":"Gargoyle","count":2,"row":"front"}]},
    "ra_abomination": {"name":"Fading Horrors","difficulty":"hard",
        "groups":[{"enemy":"Fading Abomination","count":1,"row":"front"},
                  {"enemy":"Fading Cultist","count":1,"row":"back"}]},
    "ra_patrol":      {"name":"Ruin Patrol","difficulty":"medium",
        "groups":[{"enemy":"Ashenmoor Bandit","count":2,"row":"front"},
                  {"enemy":"Ashenmoor Crossbowman","count":2,"row":"mid"}]},
    "ra_mixed_easy":  {"name":"Ruin Scavengers","difficulty":"easy",
        "groups":[{"enemy":"Ashenmoor Bandit","count":2,"row":"front"},
                  {"enemy":"Ruin Archer","count":1,"row":"mid"}]},
    "ra_full_force":  {"name":"Cult War Party","difficulty":"hard",
        "groups":[{"enemy":"Ruin Sentinel","count":1,"row":"front"},
                  {"enemy":"Ashenmoor Bandit","count":2,"row":"front"},
                  {"enemy":"Fading Cultist","count":1,"row":"back"},
                  {"enemy":"Ashenmoor Crossbowman","count":1,"row":"mid"}]},
}

# ══════════════════════════════════════════════════════════
#  NEW DUNGEON ENCOUNTER TABLES (replaces old ones)
# ══════════════════════════════════════════════════════════

NEW_DUNGEON_ENCOUNTER_TABLES = {
    "goblin_warren": {
        1: ["gw_scouts","gw_bats","gw_rats","gw_mixed_easy","easy_goblins"],
        2: ["gw_brute_pack","gw_trappers","gw_fungal","gw_drummer","gw_lurkers","medium_goblins"],
        3: ["gw_deep_patrol","gw_brute_shaman","gw_brute_pack","gw_trappers","gw_lurkers"],
        "boss": "boss_goblin_king",
    },
    "spiders_nest": {
        1: ["sn_spiderlings","sn_mixed_easy","spider_swarm","sn_eggs"],
        2: ["sn_web_trap","sn_brood","sn_eggs","sn_mixed_easy"],
        3: ["sn_venomfang","sn_web_trap","sn_brood","sn_phase","sn_venom_web"],
        4: ["sn_nest_guard","sn_venomfang","sn_brood_guard","sn_phase","sn_venom_web"],
        "boss": "boss_spider_queen",
    },
    "abandoned_mine": {
        1: ["am_kobolds","am_beetles","am_rats","am_mixed_med"],
        2: ["am_kobold_fire","am_beetles","am_trap_squad","am_mixed_med","am_kobolds"],
        3: ["am_golem","am_kobold_fire","am_wraith","am_crystal","am_trap_squad"],
        4: ["am_wraith","am_deep","am_golem","am_crystal","am_golem_duo"],
        5: ["am_deep","am_wraith","am_golem_duo","am_crystal"],
        "boss": "boss_mine_warden",
    },
    "sunken_crypt": {
        1: ["sc_zombies","sc_skel_patrol","sc_mixed_easy","sc_plague"],
        2: ["sc_skel_patrol","sc_ghoul_pack","sc_plague","sc_wailing"],
        3: ["sc_ghoul_pack","sc_shade_haunt","sc_wailing","sc_death_knight","sc_undead_horde"],
        4: ["sc_shade_haunt","sc_bone_elite","sc_death_knight","sc_undead_horde"],
        "boss": "boss_warden",
    },
    "ruins_ashenmoor": {
        1: ["ra_bandits","ra_mixed_easy","ra_patrol","ra_sentinel"],
        2: ["ra_cultists","ra_bandits","ra_sentinel","ra_patrol","ra_gargoyles"],
        3: ["ra_treant","ra_cultists","ra_mixed","ra_abomination","ra_gargoyles"],
        4: ["ra_mixed","ra_treant","ra_full_force","ra_abomination","ra_gargoyles"],
        "boss": "boss_ashenmoor",
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


# ══════════════════════════════════════════════════════════
#  ACT 3 ENEMIES — Pale Coast, Windswept Isle, Shadow Throne
# ══════════════════════════════════════════════════════════

ACT3_ENEMIES = {

    # ─── Pale Coast ────────────────────────────────────────

    "Drowned Revenant": {
        "name": "Drowned Revenant",
        "hp": 145, "defense": 12, "magic_resist": 18,
        "stats": {"STR": 14, "DEX": 8, "CON": 14, "INT": 6, "WIS": 6, "PIE": 2},
        "speed_base": 9,
        "attack_damage": 30, "attack_type": "melee", "phys_type": "blunt",
        "accuracy_bonus": 3, "preferred_row": "front",
        "ai_type": "aggressive",
        "xp_reward": 50, "gold_reward": (8, 18),
        "resistances": {"piercing": 0.5, "slashing": 0.5, "blunt": 1.0,
                        "fire": 1.5, "ice": 0.5, "lightning": 1.5,
                        "divine": 2.0, "shadow": 0.5, "nature": 1.0, "arcane": 1.0},
        "status_immunities": ["Poisoned", "Fear"],
        "abilities": [{"name": "Waterlogged Strike", "type": "damage",
                       "target": "single_enemy", "power": 20, "element": "ice",
                       "description": "A sodden blow that chills the target."}],
        "loot_table": [
            {"drop_chance": 0.25, "item": {
                "name": "Waterlogged Armor Fragment", "type": "material",
                "rarity": "common", "identified": True, "estimated_value": 20,
                "description": "Rusted plate, still dripping. Useless as armor, but the metal holds alchemical value."
            }}
        ],
        "description_tiers": {
            0: "A body washed up from the deep, still walking.",
            1: "Drowned Revenant",
            2: "Drowned Revenant — cold-resistant, weak to fire and divine."
        }
    },

    "Saltwater Shade": {
        "name": "Saltwater Shade",
        "hp": 90, "defense": 4, "magic_resist": 30,
        "stats": {"STR": 6, "DEX": 16, "CON": 8, "INT": 12, "WIS": 10, "PIE": 4},
        "speed_base": 18,
        "attack_damage": 22, "attack_type": "ranged", "phys_type": "shadow",
        "accuracy_bonus": 8, "preferred_row": "back",
        "ai_type": "coward",
        "xp_reward": 45, "gold_reward": (5, 15),
        "resistances": {"piercing": 0.0, "slashing": 0.0, "blunt": 0.5,
                        "fire": 1.5, "ice": 0.5, "lightning": 1.0,
                        "divine": 2.5, "shadow": 0.0, "nature": 1.0, "arcane": 1.5},
        "status_immunities": ["Poisoned", "Sleep", "Fear"],
        "abilities": [{"name": "Salt Corrode", "type": "debuff",
                       "target": "single_enemy", "effect": {"defense_reduction": 6, "duration": 3},
                       "description": "Saltwater mist corrodes armor and weakens defenses."}],
        "loot_table": [],
        "description_tiers": {
            0: "A wisp of briny fog shaped like a drowned sailor.",
            1: "Saltwater Shade",
            2: "Saltwater Shade — immune to physical. Use fire, divine, or arcane."
        }
    },

    "Coral Golem": {
        "name": "Coral Golem",
        "hp": 280, "defense": 22, "magic_resist": 8,
        "stats": {"STR": 20, "DEX": 4, "CON": 22, "INT": 2, "WIS": 4, "PIE": 0},
        "speed_base": 5,
        "attack_damage": 55, "attack_type": "melee", "phys_type": "blunt",
        "accuracy_bonus": 2, "preferred_row": "front",
        "ai_type": "defensive",
        "xp_reward": 90, "gold_reward": (20, 40),
        "resistances": {"piercing": 0.25, "slashing": 0.25, "blunt": 0.5,
                        "fire": 0.5, "ice": 1.0, "lightning": 1.5,
                        "divine": 1.0, "shadow": 1.0, "nature": 0.5, "arcane": 1.5},
        "status_immunities": ["Poisoned", "Fear", "Stun", "Sleep", "Charm"],
        "abilities": [{"name": "Coral Barrage", "type": "damage",
                       "target": "aoe_enemy", "power": 18,
                       "description": "Fires shards of razor coral at all enemies."}],
        "loot_table": [
            {"drop_chance": 0.40, "item": {
                "name": "Enchanted Coral Shard", "type": "material",
                "rarity": "uncommon", "identified": True, "estimated_value": 45,
                "description": "A shard of magically-hardened coral. Excellent for defensive enchantments."
            }}
        ],
        "description_tiers": {
            0: "A hulking form built from living coral, calcified by shadow.",
            1: "Coral Golem",
            2: "Coral Golem — massive HP, resistant to physical. Weak to lightning and arcane."
        }
    },

    "Tide Wraith": {
        "name": "Tide Wraith",
        "hp": 110, "defense": 6, "magic_resist": 25,
        "stats": {"STR": 8, "DEX": 14, "CON": 10, "INT": 16, "WIS": 12, "PIE": 6},
        "speed_base": 15,
        "attack_damage": 28, "attack_type": "melee", "phys_type": "shadow",
        "accuracy_bonus": 7, "preferred_row": "mid",
        "ai_type": "aggressive",
        "xp_reward": 55, "gold_reward": (10, 25),
        "resistances": {"piercing": 0.0, "slashing": 0.0, "blunt": 0.5,
                        "fire": 1.5, "ice": 0.5, "lightning": 1.0,
                        "divine": 2.5, "shadow": 0.0, "nature": 1.0, "arcane": 1.5},
        "status_immunities": ["Poisoned", "Fear"],
        "abilities": [{"name": "Undertow Curse", "type": "debuff",
                       "target": "single_enemy",
                       "effect": {"speed_penalty": 0.4, "mp_drain": 8, "duration": 3},
                       "description": "Pulls the target under with crushing tidal force, slowing them and draining magic."}],
        "loot_table": [],
        "description_tiers": {
            0: "A roiling mass of saltwater and shadow that crests like a wave.",
            1: "Tide Wraith",
            2: "Tide Wraith — immune to physical, drains MP. Use fire and divine."
        }
    },

    # Boss: The Pale Sentinel
    "The Pale Sentinel": {
        "name": "The Pale Sentinel",
        "hp": 750, "defense": 28, "magic_resist": 35,
        "stats": {"STR": 18, "DEX": 14, "CON": 20, "INT": 16, "WIS": 22, "PIE": 18},
        "speed_base": 12,
        "attack_damage": 45, "attack_type": "melee", "phys_type": "divine",
        "accuracy_bonus": 8, "preferred_row": "mid",
        "ai_type": "boss",
        "xp_reward": 380, "gold_reward": (100, 220),
        "resistances": {"piercing": 0.5, "slashing": 0.5, "blunt": 0.5,
                        "fire": 1.0, "ice": 0.5, "lightning": 1.0,
                        "divine": 0.0, "shadow": 2.0, "nature": 0.5, "arcane": 1.0},
        "status_immunities": ["Poisoned", "Fear", "Stun", "Sleep", "Charm"],
        "abilities": ["Tide of Judgment", "Ward of Isolation", "Sentinel's Resolve"],
        "loot_table": [
            {"drop_chance": 1.0, "item": {
                "name": "Hearthstone (Pale Coast)", "type": "key_item",
                "rarity": "legendary", "identified": True, "estimated_value": 0,
                "description": "The fourth Hearthstone, cold as coastal winter. It hums with ward energy.",
                "on_pickup": {"action": "collect_hearthstone", "n": 4}
            }}
        ],
        "description_tiers": {
            0: "An armored figure, ancient and still. Eyes like frozen seafoam.",
            1: "The Pale Sentinel",
            2: "The Pale Sentinel — Boss. Immune to divine, crushed by shadow... but she's waiting to be freed."
        }
    },

    # ─── Windswept Isle ─────────────────────────────────────

    "Wind Wraith": {
        "name": "Wind Wraith",
        "hp": 95, "defense": 3, "magic_resist": 28,
        "stats": {"STR": 6, "DEX": 22, "CON": 8, "INT": 12, "WIS": 8, "PIE": 2},
        "speed_base": 24,
        "attack_damage": 18, "attack_type": "ranged", "phys_type": "lightning",
        "accuracy_bonus": 12, "preferred_row": "back",
        "ai_type": "coward",
        "xp_reward": 45, "gold_reward": (5, 12),
        "resistances": {"piercing": 0.0, "slashing": 0.0, "blunt": 0.5,
                        "fire": 1.0, "ice": 1.5, "lightning": 0.0,
                        "divine": 2.0, "shadow": 1.5, "nature": 0.5, "arcane": 1.0},
        "status_immunities": ["Poisoned", "Fear", "Sleep"],
        "abilities": [{"name": "Gust Burst", "type": "damage",
                       "target": "aoe_enemy", "power": 10, "element": "lightning",
                       "description": "Unleashes a burst of electrified wind."}],
        "loot_table": [],
        "description_tiers": {
            0: "A howling shape woven from wind and static charge.",
            1: "Wind Wraith",
            2: "Wind Wraith — immune to physical and lightning. Use ice or divine."
        }
    },

    "Tempest Sprite": {
        "name": "Tempest Sprite",
        "hp": 65, "defense": 2, "magic_resist": 22,
        "stats": {"STR": 4, "DEX": 20, "CON": 6, "INT": 14, "WIS": 8, "PIE": 4},
        "speed_base": 26,
        "attack_damage": 14, "attack_type": "ranged", "phys_type": "lightning",
        "accuracy_bonus": 14, "preferred_row": "back",
        "ai_type": "coward",
        "xp_reward": 38, "gold_reward": (4, 10),
        "resistances": {"piercing": 0.0, "slashing": 0.0, "blunt": 0.5,
                        "fire": 1.0, "ice": 1.5, "lightning": 0.0,
                        "divine": 2.0, "shadow": 1.5, "nature": 0.5, "arcane": 1.0},
        "status_immunities": ["Poisoned", "Sleep"],
        "abilities": [{"name": "Static Bolt", "type": "damage",
                       "target": "single_enemy", "power": 12, "element": "lightning",
                       "description": "A crackling bolt of static energy."}],
        "loot_table": [
            {"drop_chance": 0.30, "item": {
                "name": "Sprite Dust", "type": "material",
                "rarity": "uncommon", "identified": True, "estimated_value": 30,
                "description": "Fine sparkling dust from a tempest sprite. Used in lightning enchantments."
            }}
        ],
        "description_tiers": {
            0: "A tiny crackling figure, too fast to track.",
            1: "Tempest Sprite",
            2: "Tempest Sprite — immune to physical/lightning, very fast. Use ice or divine."
        }
    },

    "Storm Golem": {
        "name": "Storm Golem",
        "hp": 240, "defense": 16, "magic_resist": 14,
        "stats": {"STR": 18, "DEX": 8, "CON": 18, "INT": 6, "WIS": 4, "PIE": 0},
        "speed_base": 8,
        "attack_damage": 50, "attack_type": "melee", "phys_type": "lightning",
        "accuracy_bonus": 4, "preferred_row": "front",
        "ai_type": "aggressive",
        "xp_reward": 80, "gold_reward": (18, 35),
        "resistances": {"piercing": 0.5, "slashing": 0.5, "blunt": 0.75,
                        "fire": 0.5, "ice": 1.5, "lightning": 0.0,
                        "divine": 1.0, "shadow": 1.0, "nature": 0.5, "arcane": 1.5},
        "status_immunities": ["Poisoned", "Stun", "Fear", "Sleep", "Charm"],
        "abilities": [{"name": "Lightning Crash", "type": "damage",
                       "target": "aoe_enemy", "power": 22, "element": "lightning",
                       "description": "Slams the ground releasing a shockwave of lightning."}],
        "loot_table": [
            {"drop_chance": 0.35, "item": {
                "name": "Storm Core Shard", "type": "material",
                "rarity": "rare", "identified": True, "estimated_value": 65,
                "description": "A fragment of solidified lightning. Still crackles in the hand."
            }}
        ],
        "description_tiers": {
            0: "Stone and storm, animated by elemental fury.",
            1: "Storm Golem",
            2: "Storm Golem — immune to lightning. High physical defense. Use ice or arcane."
        }
    },

    "Isle Shade": {
        "name": "Isle Shade",
        "hp": 105, "defense": 5, "magic_resist": 26,
        "stats": {"STR": 10, "DEX": 16, "CON": 10, "INT": 10, "WIS": 8, "PIE": 2},
        "speed_base": 16,
        "attack_damage": 26, "attack_type": "melee", "phys_type": "shadow",
        "accuracy_bonus": 8, "preferred_row": "mid",
        "ai_type": "aggressive",
        "xp_reward": 48, "gold_reward": (8, 18),
        "resistances": {"piercing": 0.0, "slashing": 0.0, "blunt": 0.5,
                        "fire": 1.5, "ice": 1.0, "lightning": 1.5,
                        "divine": 2.5, "shadow": 0.0, "nature": 1.0, "arcane": 1.5},
        "status_immunities": ["Poisoned", "Fear"],
        "abilities": [{"name": "Isle Miasma", "type": "debuff",
                       "target": "single_enemy",
                       "effect": {"accuracy_reduction": 20, "duration": 2},
                       "description": "Exhales a disorienting sea mist."}],
        "loot_table": [],
        "description_tiers": {
            0: "A shadow clinging to the island ruins, fed by the Fading.",
            1: "Isle Shade",
            2: "Isle Shade — immune to physical. Reduces accuracy. Use divine or fire."
        }
    },

    # Boss: The Last Keeper
    "The Last Keeper": {
        "name": "The Last Keeper",
        "hp": 680, "defense": 18, "magic_resist": 28,
        "stats": {"STR": 14, "DEX": 18, "CON": 16, "INT": 18, "WIS": 14, "PIE": 8},
        "speed_base": 16,
        "attack_damage": 40, "attack_type": "ranged", "phys_type": "lightning",
        "accuracy_bonus": 10, "preferred_row": "back",
        "ai_type": "boss",
        "xp_reward": 360, "gold_reward": (90, 200),
        "resistances": {"piercing": 0.5, "slashing": 0.5, "blunt": 0.5,
                        "fire": 1.0, "ice": 1.5, "lightning": 0.0,
                        "divine": 1.0, "shadow": 2.0, "nature": 0.5, "arcane": 1.0},
        "status_immunities": ["Poisoned", "Fear", "Stun", "Sleep"],
        "abilities": ["Tempest Barrage", "Cyclone Ward", "Chain Lightning"],
        "loot_table": [
            {"drop_chance": 1.0, "item": {
                "name": "Hearthstone (Windswept Isle)", "type": "key_item",
                "rarity": "legendary", "identified": True, "estimated_value": 0,
                "description": "The fifth and final Hearthstone, crackling with stored storm energy.",
                "on_pickup": {"action": "collect_hearthstone", "n": 5}
            }}
        ],
        "description_tiers": {
            0: "A being of living storm, ancient and indifferent.",
            1: "The Last Keeper",
            2: "The Last Keeper — Boss. Immune to lightning. Pure elemental guardian — no reasoning with this one."
        }
    },

    # ─── Shadow Throne ─────────────────────────────────────

    "Throne Shade": {
        "name": "Throne Shade",
        "hp": 140, "defense": 8, "magic_resist": 32,
        "stats": {"STR": 12, "DEX": 18, "CON": 12, "INT": 14, "WIS": 10, "PIE": 2},
        "speed_base": 18,
        "attack_damage": 35, "attack_type": "melee", "phys_type": "shadow",
        "accuracy_bonus": 10, "preferred_row": "mid",
        "ai_type": "aggressive",
        "xp_reward": 65, "gold_reward": (15, 30),
        "resistances": {"piercing": 0.0, "slashing": 0.0, "blunt": 0.5,
                        "fire": 1.5, "ice": 1.0, "lightning": 1.0,
                        "divine": 3.0, "shadow": 0.0, "nature": 1.0, "arcane": 2.0},
        "status_immunities": ["Poisoned", "Fear", "Sleep"],
        "abilities": [{"name": "Shadow Rend", "type": "damage",
                       "target": "single_enemy", "power": 22, "element": "shadow",
                       "description": "Tears at the target's soul with shadow claws."}],
        "loot_table": [
            {"drop_chance": 0.35, "item": {
                "name": "Shadow Essence", "type": "material",
                "rarity": "uncommon", "identified": True, "estimated_value": 40,
                "description": "Dense shadow energy. Warm and unsettling to hold."
            }}
        ],
        "description_tiers": {
            0: "A sentinel of the Shadow Throne. Loyal only to Valdris.",
            1: "Throne Shade",
            2: "Throne Shade — immune to physical. Extremely weak to divine (3×)."
        }
    },

    "Corrupted Warden Echo": {
        "name": "Corrupted Warden Echo",
        "hp": 195, "defense": 18, "magic_resist": 22,
        "stats": {"STR": 16, "DEX": 12, "CON": 16, "INT": 14, "WIS": 12, "PIE": 8},
        "speed_base": 12,
        "attack_damage": 44, "attack_type": "melee", "phys_type": "shadow",
        "accuracy_bonus": 8, "preferred_row": "front",
        "ai_type": "aggressive",
        "xp_reward": 80, "gold_reward": (20, 40),
        "resistances": {"piercing": 0.5, "slashing": 0.5, "blunt": 0.75,
                        "fire": 1.0, "ice": 1.0, "lightning": 1.0,
                        "divine": 2.5, "shadow": 0.0, "nature": 1.0, "arcane": 1.5},
        "status_immunities": ["Poisoned", "Fear", "Charm"],
        "abilities": [{"name": "Echo Strike", "type": "damage",
                       "target": "single_enemy", "power": 26, "element": "shadow",
                       "description": "A shadow-infused blow that echoes with fallen warden power."}],
        "loot_table": [
            {"drop_chance": 0.20, "item": {
                "name": "Warden's Remnant Badge", "type": "material",
                "rarity": "rare", "identified": True, "estimated_value": 80,
                "description": "The badge of a Warden long since fallen to shadow. The inscription is still legible."
            }}
        ],
        "description_tiers": {
            0: "A ghost of a Warden, face twisted, still wearing the order's colors.",
            1: "Corrupted Warden Echo",
            2: "Corrupted Warden Echo — elite. Decent defenses. Divine is the key."
        }
    },

    # Shadow Throne — Void Tendril (swarm horror, fast, fragile)
    "Void Tendril": {
        "name": "Void Tendril",
        "hp": 55, "defense": 2, "magic_resist": 6,
        "stats": {"STR": 6, "DEX": 20, "CON": 4, "INT": 2, "WIS": 4, "PIE": 1},
        "speed_base": 28,
        "attack_damage": 18, "attack_type": "melee", "phys_type": "shadow",
        "accuracy_bonus": 10, "preferred_row": "front",
        "ai_type": "aggressive",
        "xp_reward": 45, "gold_reward": (0, 5),
        "resistances": {"piercing": 1.5, "slashing": 1.5, "blunt": 0.75,
                        "fire": 2.0, "ice": 0.75, "lightning": 1.0,
                        "divine": 2.0, "shadow": 0.0, "nature": 1.0, "arcane": 1.0},
        "status_immunities": ["Poisoned", "Sleep"],
        "abilities": [],
        "loot_table": [],
        "description_tiers": {
            0: "A thrashing tendril of pure void-matter, reaching hungrily from the walls.",
            1: "Void Tendril",
            2: "Void Tendril — swarm horror. Very fast, very fragile. Fire and divine shred them. Watch for the Abomination behind them."
        }
    },

    # Boss: Valdris (Phase 1) — shadow avatar form
    "Valdris, Shadow Avatar": {
        "name": "Valdris, Shadow Avatar",
        "hp": 900, "defense": 25, "magic_resist": 38,
        "stats": {"STR": 18, "DEX": 16, "CON": 20, "INT": 26, "WIS": 22, "PIE": 10},
        "speed_base": 14,
        "attack_damage": 55, "attack_type": "ranged", "phys_type": "shadow",
        "accuracy_bonus": 12, "preferred_row": "back",
        "ai_type": "boss",
        "xp_reward": 500, "gold_reward": (200, 400),
        "resistances": {"piercing": 0.75, "slashing": 0.75, "blunt": 0.75,
                        "fire": 1.0, "ice": 1.0, "lightning": 1.0,
                        "divine": 2.0, "shadow": 0.0, "nature": 1.0, "arcane": 0.5},
        "status_immunities": ["Poisoned", "Fear", "Stun", "Sleep", "Charm"],
        "abilities": ["Shadow Nova", "Dark Ritual", "Fading Pulse", "Ward Shatter"],
        "loot_table": [],  # phase 2 triggers on defeat, no loot yet
        "description_tiers": {
            0: "Valdris — but not the man. A shell of pure shadow wearing his face.",
            1: "Valdris, Shadow Avatar",
            2: "Valdris — Phase 1. Immune to shadow, vulnerable to divine and arcane. Defeat the avatar to reach the man."
        }
    },

    # Boss: Valdris (Phase 2) — diminished, broken form
    "Valdris the Broken": {
        "name": "Valdris the Broken",
        "hp": 420, "defense": 12, "magic_resist": 20,
        "stats": {"STR": 10, "DEX": 10, "CON": 12, "INT": 22, "WIS": 18, "PIE": 14},
        "speed_base": 10,
        "attack_damage": 35, "attack_type": "ranged", "phys_type": "arcane",
        "accuracy_bonus": 6, "preferred_row": "back",
        "ai_type": "boss",
        "xp_reward": 600, "gold_reward": (250, 500),
        "resistances": {"piercing": 1.0, "slashing": 1.0, "blunt": 1.0,
                        "fire": 1.0, "ice": 1.0, "lightning": 1.0,
                        "divine": 1.0, "shadow": 1.5, "nature": 1.0, "arcane": 0.5},
        "status_immunities": ["Fear", "Charm"],
        "abilities": ["Desperate Nova", "Last Ward", "Plea of the Fallen"],
        "loot_table": [
            {"drop_chance": 1.0, "item": {
                "name": "Valdris's Warden Seal", "type": "key_item",
                "rarity": "legendary", "identified": True, "estimated_value": 0,
                "description": "The seal of the order Valdris once served. He never stopped wearing it. "
                               "Choosing to end him or spare him — both paths open from here."
            }}
        ],
        "description_tiers": {
            0: "The shadow is stripped away. What remains is an old, exhausted man.",
            1: "Valdris the Broken",
            2: "Valdris — Phase 2. Weakened but dangerous. Shadow now hurts him. This is the real decision."
        }
    },
}

NEW_ENEMIES.update(ACT3_ENEMIES)


# ──────────────────────────────────────────────────────────
#  ACT 3 ENCOUNTERS
# ──────────────────────────────────────────────────────────

ACT3_ENCOUNTERS = {

    # ─── Pale Coast ───────────────────────────────────────

    "pc_drowned":    {"name": "Risen Dead", "difficulty": "medium",
        "groups": [{"enemy": "Drowned Revenant", "count": 2, "row": "front"}]},
    "pc_shades":     {"name": "Saltwater Shades", "difficulty": "medium",
        "groups": [{"enemy": "Saltwater Shade", "count": 3, "row": "back"}]},
    "pc_tide":       {"name": "Tide Wraiths", "difficulty": "medium",
        "groups": [{"enemy": "Tide Wraith", "count": 2, "row": "mid"},
                   {"enemy": "Saltwater Shade", "count": 1, "row": "back"}]},
    "pc_golem":      {"name": "Coral Guardian", "difficulty": "hard",
        "groups": [{"enemy": "Coral Golem", "count": 1, "row": "front"},
                   {"enemy": "Saltwater Shade", "count": 2, "row": "back"}]},
    "pc_drowned_mob":{"name": "Drowned Legion", "difficulty": "hard",
        "groups": [{"enemy": "Drowned Revenant", "count": 3, "row": "front"},
                   {"enemy": "Tide Wraith", "count": 1, "row": "mid"}]},
    "pc_twin_golems":{"name": "Twin Coral Guardians", "difficulty": "hard",
        "groups": [{"enemy": "Coral Golem", "count": 2, "row": "front"}]},
    "boss_pale_warden": {"name": "The Pale Sentinel", "difficulty": "boss",
        "groups": [{"enemy": "The Pale Sentinel", "count": 1, "row": "mid"},
                   {"enemy": "Drowned Revenant", "count": 2, "row": "front"},
                   {"enemy": "Tide Wraith", "count": 2, "row": "back"}]},

    # ─── Windswept Isle ────────────────────────────────────

    "wi_wraiths":     {"name": "Wind Wraiths", "difficulty": "medium",
        "groups": [{"enemy": "Wind Wraith", "count": 3, "row": "back"}]},
    "wi_sprites":     {"name": "Tempest Sprites", "difficulty": "medium",
        "groups": [{"enemy": "Tempest Sprite", "count": 4, "row": "back"}]},
    "wi_mixed":       {"name": "Storm Pack", "difficulty": "medium",
        "groups": [{"enemy": "Wind Wraith", "count": 2, "row": "back"},
                   {"enemy": "Isle Shade", "count": 1, "row": "mid"}]},
    "wi_golem":       {"name": "Storm Golem", "difficulty": "hard",
        "groups": [{"enemy": "Storm Golem", "count": 1, "row": "front"},
                   {"enemy": "Tempest Sprite", "count": 2, "row": "back"}]},
    "wi_storm_mob":   {"name": "Storm Surge", "difficulty": "hard",
        "groups": [{"enemy": "Wind Wraith", "count": 2, "row": "back"},
                   {"enemy": "Storm Golem", "count": 1, "row": "front"},
                   {"enemy": "Isle Shade", "count": 1, "row": "mid"}]},
    "boss_isle_keeper": {"name": "The Last Keeper", "difficulty": "boss",
        "groups": [{"enemy": "The Last Keeper", "count": 1, "row": "back"},
                   {"enemy": "Storm Golem", "count": 1, "row": "front"},
                   {"enemy": "Wind Wraith", "count": 3, "row": "back"}]},

    # ─── Shadow Throne ─────────────────────────────────────

    "st_shades":      {"name": "Throne Sentinels", "difficulty": "hard",
        "groups": [{"enemy": "Throne Shade", "count": 3, "row": "mid"}]},
    "st_mixed":       {"name": "Throne Guard", "difficulty": "hard",
        "groups": [{"enemy": "Shadow Brute", "count": 1, "row": "front"},
                   {"enemy": "Throne Shade", "count": 2, "row": "mid"}]},
    "st_echoes":      {"name": "Fallen Wardens", "difficulty": "hard",
        "groups": [{"enemy": "Corrupted Warden Echo", "count": 2, "row": "front"},
                   {"enemy": "Throne Shade", "count": 1, "row": "mid"}]},
    "st_abominations":{"name": "Fading Made Flesh", "difficulty": "hard",
        "groups": [{"enemy": "Fading Abomination", "count": 2, "row": "front"},
                   {"enemy": "Throne Shade", "count": 2, "row": "back"}]},
    "st_elite":       {"name": "Elite Guard", "difficulty": "hard",
        "groups": [{"enemy": "Corrupted Warden Echo", "count": 1, "row": "front"},
                   {"enemy": "Shadow Stalker", "count": 2, "row": "mid"},
                   {"enemy": "Throne Shade", "count": 2, "row": "back"}]},
    "st_void":        {"name": "Void Breach", "difficulty": "hard",
        "groups": [{"enemy": "Void Tendril", "count": 4, "row": "front"},
                   {"enemy": "Fading Abomination", "count": 1, "row": "front"}]},
    "st_warden_elite":{"name": "Warden Echoes", "difficulty": "hard",
        "groups": [{"enemy": "Corrupted Warden Echo", "count": 3, "row": "front"}]},
    "st_shadow_squad":{"name": "Shadow Squad", "difficulty": "hard",
        "groups": [{"enemy": "Shadow Brute", "count": 2, "row": "front"},
                   {"enemy": "Shadow Stalker", "count": 2, "row": "mid"}]},
    "boss_valdris_phase1": {"name": "Valdris — Shadow Avatar", "difficulty": "boss",
        "groups": [{"enemy": "Valdris, Shadow Avatar", "count": 1, "row": "back"},
                   {"enemy": "Throne Shade", "count": 2, "row": "mid"},
                   {"enemy": "Shadow Brute", "count": 1, "row": "front"}]},
    "boss_valdris_phase2": {"name": "Valdris the Broken", "difficulty": "boss",
        "groups": [{"enemy": "Valdris the Broken", "count": 1, "row": "back"}]},
}

NEW_ENCOUNTERS.update(ACT3_ENCOUNTERS)
