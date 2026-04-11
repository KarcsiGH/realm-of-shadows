"""
Realm of Shadows — Ability & Spell System (M5)

Defines all learnable abilities for each class, organized by level requirement.
Characters learn abilities at the inn when they level up, IF they meet the level req.

Ability types:
  - "attack": Physical damage (uses weapon + STR/DEX)
  - "spell": Magic damage (uses INT/WIS/PIE, element-based)
  - "heal": Restores HP to target
  - "buff": Applies a beneficial status
  - "debuff": Applies a harmful status to enemy
  - "aoe": Hits all enemies (reduced damage per target)
  - "aoe_heal": Heals all allies
"""

# ═══════════════════════════════════════════════════════════════
#  ABILITY DEFINITIONS BY CLASS
# ═══════════════════════════════════════════════════════════════

"""
Realm of Shadows — Ability & Spell System (M6 — Momentum + Level 20 redesign)

Base classes: 6, levels 1-20, pruned to 10-13 abilities each.
Hybrid classes: 9, levels 10-20 (or 1-20 if started at creation).
All physical attack abilities use "momentum" resource.
Physical buffs/utilities use SP/Ki at half original cost.
Magic abilities unchanged (INT-MP, WIS-MP, PIE-MP).

Ability types:
  attack    — Physical damage (Momentum)
  spell     — Magic damage (MP)
  heal      — Restores HP
  buff      — Beneficial status
  debuff    — Harmful status on enemy
  aoe       — Hits all enemies
  aoe_heal  — Heals all allies
  cure      — Removes status effects
  revive    — Revives fallen character
  passive   — Always active, not directly usable
  special   — Unique mechanics
"""

CLASS_ABILITIES = {

    # ══════════════════════════════════════════════════════════
    #  FIGHTER — L1-20  |  Warrior, tank, raw physical power
    # ══════════════════════════════════════════════════════════
    "Fighter": [
        {"name": "Power Strike",     "cost": 3, "resource": "momentum", "type": "attack",
         "level": 1, "power": 1.6, "desc": "Heavy melee attack, 60% bonus damage."},
        {"name": "Defensive Stance", "cost": 4, "resource": "STR-SP",   "type": "buff",
         "level": 2, "buff": "defense_up", "duration": 2, "self_only": True,
         "desc": "Reduce incoming physical damage for 2 turns."},
        {"name": "Shield Bash",      "cost": 3, "resource": "momentum", "type": "attack",
         "level": 3, "power": 1.3, "stun_chance": 0.35,
         "desc": "Bash with shield. 35% chance to stun."},
        {"name": "Cleave",           "cost": 2, "resource": "momentum", "type": "aoe",
         "level": 5, "power": 1.0, "target": "front_row",
         "desc": "Wide slash hitting all front-row enemies."},
        {"name": "War Cry",          "cost": 7, "resource": "STR-SP",   "type": "buff",
         "level": 7, "buff": "war_cry", "duration": 3, "targets": "all_allies",
         "desc": "Inspire allies, boosting damage for 3 turns."},
        {"name": "Charge",           "cost": 3, "resource": "momentum", "type": "attack",
         "level": 9, "power": 1.6, "desc": "Charging strike, bonus damage from back row."},
        {"name": "Rallying Cry",     "cost": 11, "resource": "STR-SP",  "type": "buff",
         "level": 11, "buff": "rally", "duration": 3, "targets": "all_allies",
         "desc": "Rally the party: +25% damage and fear immunity for 3 turns."},
        {"name": "Executioner",      "cost": 5, "resource": "momentum", "type": "attack",
         "level": 13, "power": 2.5, "execute_threshold": 0.25,
         "desc": "Devastating blow. Instant kill if target below 25% HP."},
        {"name": "Iron Will",        "cost": 0, "resource": "",         "type": "passive",
         "level": 15, "desc": "Passive: immune to Fear and Charm effects."},
        {"name": "Berserker Rage",   "cost": 12, "resource": "STR-SP",  "type": "buff",
         "level": 16, "buff": "berserk", "duration": 3, "self_only": True,
         "desc": "Massive damage boost when below 30% HP. Lasts 3 turns."},
        {"name": "Unbreakable",      "cost": 0, "resource": "",         "type": "passive",
         "level": 18, "desc": "Passive: survive one lethal hit per combat at 1 HP."},
        {"name": "Army of One",      "cost": 6, "resource": "momentum", "type": "aoe",
         "level": 20, "power": 1.8, "target": "all_enemies",
         "desc": "Strikes every enemy on the field simultaneously. The signature of a true warrior."},
    ],

    # ══════════════════════════════════════════════════════════
    #  MAGE — L1-20  |  Arcane power, crowd control, raw magic
    # ══════════════════════════════════════════════════════════
    "Mage": [
        {"name": "Magic Missile",  "cost": 8,  "resource": "INT-MP", "type": "spell",
         "level": 1, "power": 1.0, "element": "arcane",
         "desc": "Reliable arcane bolt. Never misses."},
        {"name": "Frostbolt",      "cost": 10, "resource": "INT-MP", "type": "spell",
         "level": 2, "power": 1.2, "element": "ice", "slow_chance": 0.40,
         "desc": "Ice projectile. 40% chance to slow."},
        {"name": "Arcane Surge",   "cost": 10, "resource": "INT-MP", "type": "buff",
         "level": 3, "buff": "arcane_surge", "duration": 2, "self_only": True,
         "desc": "Channel pure arcane energy: +30% spell damage for 2 turns."},
        {"name": "Fireball",       "cost": 20, "resource": "INT-MP", "type": "aoe",
         "level": 4, "power": 1.4, "element": "fire", "target": "front_row",
         "desc": "Explosive fire blast hitting the entire front row."},
        {"name": "Sleep",          "cost": 12, "resource": "INT-MP", "type": "spell",
         "level": 5, "power": 0, "status": "Sleep", "status_chance": 0.65,
         "desc": "Attempts to put one enemy to sleep. 65% success rate."},
        {"name": "Deep Freeze",    "cost": 18, "resource": "INT-MP", "type": "spell",
         "level": 7, "power": 1.6, "element": "ice", "status": "Freeze", "status_chance": 0.45,
         "desc": "Intense cold attack. 45% chance to freeze target solid."},
        {"name": "Chain Lightning", "cost": 25, "resource": "INT-MP", "type": "aoe",
         "level": 8, "power": 1.3, "element": "lightning", "target": "all_enemies",
         "desc": "Lightning arcs between all enemies."},
        {"name": "Disintegrate",   "cost": 28, "resource": "INT-MP", "type": "spell",
         "level": 10, "power": 2.0, "element": "arcane", "armor_pierce": True,
         "desc": "Arcane destruction. Completely ignores magic resistance."},
        {"name": "Confuse",        "cost": 14, "resource": "INT-MP", "type": "debuff",
         "level": 12, "status": "Confused", "status_chance": 0.55,
         "desc": "Befuddle an enemy. Confused enemies attack randomly."},
        {"name": "Void Rift",      "cost": 32, "resource": "INT-MP", "type": "aoe",
         "level": 14, "power": 1.5, "element": "shadow",  "target": "all_enemies",
         "desc": "Tears a rift in reality. Shadow + arcane AOE, pulls all enemies to front row."},
        {"name": "Time Warp",      "cost": 35, "resource": "INT-MP", "type": "buff",
         "level": 17, "buff": "time_warp", "duration": 1, "targets": "all_allies",
         "desc": "Party acts twice in the next turn. Once per combat."},
        {"name": "Meteor",         "cost": 45, "resource": "INT-MP", "type": "aoe",
         "level": 20, "power": 1.8, "element": "fire",    "target": "all_enemies",
         "desc": "Catastrophic fire strike. Partially affects party's front row — high risk, devastating reward."},
    ],

    # ══════════════════════════════════════════════════════════
    #  CLERIC — L1-20  |  Healer, divine caster, party anchor
    # ══════════════════════════════════════════════════════════
    "Cleric": [
        {"name": "Heal",            "cost": 10, "resource": "PIE-MP", "type": "heal",
         "level": 1, "power": 1.0, "desc": "Restore HP to one ally."},
        {"name": "Smite",           "cost": 12, "resource": "PIE-MP", "type": "spell",
         "level": 1, "power": 1.4, "element": "divine",
         "desc": "Channel divine wrath at an enemy."},
        {"name": "Bless",           "cost": 8,  "resource": "PIE-MP", "type": "buff",
         "level": 2, "buff": "blessed", "duration": 3, "targets": "all_allies",
         "desc": "Bless the party: +10% damage and defense for 3 turns."},
        {"name": "Cure Poison",     "cost": 8,  "resource": "PIE-MP", "type": "cure",
         "level": 3, "cures": "poison", "desc": "Cure poison from one ally."},
        {"name": "Consecrate",      "cost": 16, "resource": "PIE-MP", "type": "aoe",
         "level": 4, "power": 1.0, "element": "divine", "target": "all_enemies",
         "desc": "Consecrate the ground, dealing divine damage to all enemies."},
        {"name": "Prayer of Healing","cost": 20,"resource": "PIE-MP", "type": "aoe_heal",
         "level": 5, "power": 1.0, "desc": "Restore HP to all party members."},
        {"name": "Revive",          "cost": 24, "resource": "PIE-MP", "type": "revive",
         "level": 6, "desc": "Revive a fallen ally at 25% HP."},
        {"name": "Turn Undead",     "cost": 15, "resource": "PIE-MP", "type": "debuff",
         "level": 7, "status": "Turned", "status_chance": 0.70,
         "desc": "Command undead enemies to flee. 70% success."},
        {"name": "Mass Cure",       "cost": 20, "resource": "PIE-MP", "type": "cure",
         "level": 9, "cures": "all", "targets": "all_allies",
         "desc": "Cure all status effects from the entire party."},
        {"name": "Remove Curse",    "cost": 18, "resource": "PIE-MP", "type": "cure",
         "level": 7, "cures": "curse",
         "desc": "Lift a curse from one ally. Required to remove cursed equipment."},
        {"name": "Divine Wrath",    "cost": 30, "resource": "PIE-MP", "type": "aoe",
         "level": 11, "power": 1.8, "element": "divine", "target": "all_enemies",
         "desc": "Devastating divine blast hitting all enemies."},
        {"name": "Judgment",        "cost": 28, "resource": "PIE-MP", "type": "spell",
         "level": 14, "power": 2.2, "element": "divine",
         "desc": "Massive divine strike. Double damage against shadow-corrupted enemies."},
        {"name": "Martyr's Ward",   "cost": 20, "resource": "PIE-MP", "type": "buff",
         "level": 16, "buff": "martyrs_ward", "duration": 2, "self_only": True,
         "desc": "All damage to party members is redirected to Cleric instead for 2 turns."},
        {"name": "Miracle",         "cost": 50, "resource": "PIE-MP", "type": "aoe_heal",
         "level": 18, "power": 2.0, "desc": "Full party resurrection + 50% HP restore. Once per dungeon."},
        {"name": "Word of God",     "cost": 40, "resource": "PIE-MP", "type": "special",
         "level": 20, "power": 3.0, "element": "divine",
         "desc": "Instant kill undead/shadow enemies. Fully heals divine allies. The apex of faith."},
    ],

    # ══════════════════════════════════════════════════════════
    #  THIEF — L1-20  |  Burst damage, poison, evasion, setup
    # ══════════════════════════════════════════════════════════
    "Thief": [
        {"name": "Quick Strike",    "cost": 3, "resource": "momentum", "type": "attack",
         "level": 1, "power": 1.3, "desc": "Fast strike — lower power but builds Momentum quickly."},
        {"name": "Evade",           "cost": 4, "resource": "DEX-SP",   "type": "buff",
         "level": 1, "buff": "evasion", "duration": 2, "self_only": True,
         "desc": "Enter evasive stance. 45% chance to dodge attacks for 2 turns."},
        {"name": "Backstab",        "cost": 4, "resource": "momentum", "type": "attack",
         "level": 3, "power": 2.0, "bonus_crit": 0.30,
         "desc": "Vicious rear attack. +30% critical hit chance."},
        {"name": "Dirty Fighting",  "cost": 3, "resource": "momentum", "type": "attack",
         "level": 4, "power": 1.2, "status": "Weakened", "status_chance": 0.50,
         "desc": "Underhanded strike. 50% chance to weaken target."},
        {"name": "Poison Blade",    "cost": 3, "resource": "momentum", "type": "attack",
         "level": 5, "power": 1.2, "apply_poison": "poison_weak",
         "desc": "Coat blade in venom. Deals damage + poison."},
        {"name": "Smoke Bomb",      "cost": 8, "resource": "DEX-SP",   "type": "buff",
         "level": 6, "buff": "smoke_screen", "duration": 2, "targets": "all_allies",
         "desc": "Obscure the party. All allies gain evasion for 2 turns."},
        {"name": "Shadow Meld",     "cost": 7, "resource": "DEX-SP",   "type": "buff",
         "level": 7, "buff": "shadow_step", "duration": 1, "self_only": True,
         "desc": "Meld with shadows. Next attack deals +50% damage."},
        {"name": "Garrote",         "cost": 3, "resource": "momentum", "type": "attack",
         "level": 9, "power": 1.5, "status": "Silenced", "status_chance": 0.60,
         "desc": "Choke strike. 60% chance to silence — target cannot cast spells."},
        {"name": "Death Mark",      "cost": 11, "resource": "DEX-SP",  "type": "debuff",
         "level": 11, "mark_duration": 3, "mark_crit_bonus": 0.50,
         "desc": "Mark a target. All attacks on marked target have +50% critical hit chance."},
        {"name": "Hemorrhage",      "cost": 3, "resource": "momentum", "type": "attack",
         "level": 13, "power": 1.4, "dot": 8, "dot_duration": 3,
         "desc": "Deep wound that bleeds: 8 damage per turn for 3 turns."},
        {"name": "Coup de Grace",   "cost": 5, "resource": "momentum", "type": "attack",
         "level": 16, "power": 3.0, "execute_threshold": 0.15,
         "desc": "Finishing blow. Instant kill if target below 15% HP."},
        {"name": "Master of Shadows","cost": 0, "resource": "",        "type": "passive",
         "level": 18, "desc": "Passive: all Thief abilities generate +1 extra Momentum."},
        {"name": "Shadow Realm",    "cost": 14, "resource": "DEX-SP",  "type": "buff",
         "level": 20, "buff": "shadow_realm", "duration": 1, "targets": "all_allies",
         "desc": "The entire party becomes untargetable for 1 full round. The ultimate setup."},
    ],

    # ══════════════════════════════════════════════════════════
    #  RANGER — L1-20  |  Ranged damage, traps, nature magic
    # ══════════════════════════════════════════════════════════
    "Ranger": [
        {"name": "Aimed Shot",      "cost": 3, "resource": "momentum", "type": "attack",
         "level": 1, "power": 1.5, "desc": "Precise ranged attack."},
        {"name": "Hunter's Mark",   "cost": 4, "resource": "DEX-SP",   "type": "debuff",
         "level": 2, "mark_duration": 3, "mark_crit_bonus": 0.25,
         "desc": "Mark a target. +25% critical hit chance against them for 3 turns."},
        {"name": "Scatter Shot",    "cost": 2, "resource": "momentum", "type": "aoe",
         "level": 3, "power": 0.85, "target": "front_row",
         "desc": "Wide arrow spray hitting the front row."},
        {"name": "Snare Trap",      "cost": 10, "resource": "WIS-MP",  "type": "debuff",
         "level": 4, "status": "Slowed", "status_chance": 0.70,
         "desc": "Set a trap. 70% chance to slow and root target."},
        {"name": "Barrage",         "cost": 2, "resource": "momentum", "type": "aoe",
         "level": 5, "power": 1.0, "target": "all_enemies",
         "desc": "Rapid fire into the enemy group."},
        {"name": "Nature's Balm",   "cost": 14, "resource": "WIS-MP",  "type": "heal",
         "level": 5, "power": 1.0, "desc": "Draw on nature's energy to heal an ally."},
        {"name": "Camouflage",      "cost": 6, "resource": "DEX-SP",   "type": "buff",
         "level": 7, "buff": "camouflage", "duration": 2, "self_only": True,
         "desc": "Become nearly invisible. Enemies are less likely to target Ranger."},
        {"name": "Poison Arrow",    "cost": 3, "resource": "momentum", "type": "attack",
         "level": 8, "power": 1.1, "apply_poison": "poison_weak",
         "desc": "Venom-tipped arrow. Deals damage + poison."},
        {"name": "Rain of Arrows",  "cost": 3, "resource": "momentum", "type": "aoe",
         "level": 9, "power": 1.3, "target": "all_enemies",
         "desc": "Blanket the entire battlefield with arrows."},
        {"name": "Eagle Eye",       "cost": 0, "resource": "",         "type": "passive",
         "level": 11, "desc": "Passive: +15% accuracy on all ranged attacks. Never miss from back row."},
        {"name": "Lethal Shot",     "cost": 5, "resource": "momentum", "type": "attack",
         "level": 13, "power": 2.5, "execute_threshold": 0.30,
         "desc": "Perfect kill shot. Instant kill if target below 30% HP."},
        {"name": "Pack Hunt",       "cost": 20, "resource": "WIS-MP",  "type": "special",
         "level": 15, "desc": "Summon an animal companion (wolf or bear) for 3 turns. Fights alongside the party."},
        {"name": "Volley of Ruin",  "cost": 4, "resource": "momentum", "type": "aoe",
         "level": 17, "power": 1.4, "target": "all_enemies", "apply_poison": "poison_weak",
         "desc": "Unleash everything. Hits all enemies, each arrow has a poison chance."},
        {"name": "One With the Wild","cost": 30,"resource": "WIS-MP",  "type": "buff",
         "level": 20, "buff": "wild_bond", "duration": 3, "targets": "all_allies",
         "desc": "Party gains nature affinity: Fading resistance, +20% damage, Ranger regenerates resources each turn."},
    ],

    # ══════════════════════════════════════════════════════════
    #  MONK — L1-20  |  Ki-fuelled physical mastery, discipline
    # ══════════════════════════════════════════════════════════
    "Monk": [
        {"name": "Flurry of Blows",  "cost": 2, "resource": "momentum", "type": "attack",
         "level": 1, "power": 0.6, "hits": 3,
         "desc": "Three rapid strikes. Each hit builds Momentum."},
        {"name": "Iron Skin",        "cost": 5, "resource": "Ki",       "type": "buff",
         "level": 1, "buff": "iron_skin", "duration": 3, "self_only": True,
         "desc": "Harden the body. Reduce physical damage by 8 for 3 turns."},
        {"name": "Stunning Fist",    "cost": 3, "resource": "momentum", "type": "attack",
         "level": 3, "power": 1.3, "stun_chance": 0.45,
         "desc": "Strike a pressure point. 45% chance to stun."},
        {"name": "Earth Strike",     "cost": 3, "resource": "momentum", "type": "attack",
         "level": 4, "power": 1.5, "element": "earth",
         "desc": "Channel earth energy through a powerful strike."},
        {"name": "Inner Peace",      "cost": 7, "resource": "Ki",       "type": "heal",
         "level": 5, "power": 1.2, "self_only": True,
         "desc": "Restore HP through deep meditation."},
        {"name": "Ki Barrier",       "cost": 7, "resource": "Ki",       "type": "buff",
         "level": 6, "buff": "ki_deflect", "duration": 3, "self_only": True,
         "desc": "Erect a Ki barrier. +8 magic resistance for 3 turns."},
        {"name": "Pressure Point",   "cost": 9, "resource": "Ki",       "type": "debuff",
         "level": 8, "status": "Weakened", "status_chance": 0.65, "status_duration": 3,
         "desc": "Strike a nerve cluster. 65% chance to weaken for 3 turns."},
        {"name": "Thunderous Clap",  "cost": 3, "resource": "momentum", "type": "aoe",
         "level": 9, "power": 1.1, "target": "front_row", "stun_chance": 0.25,
         "desc": "Concussive clap. Hits front row, 25% stun chance."},
        {"name": "Void Fist",        "cost": 4, "resource": "momentum", "type": "attack",
         "level": 11, "power": 2.2, "armor_pierce": True,
         "desc": "Strike through all armor. Completely ignores physical defense."},
        {"name": "Dragon Strike",    "cost": 5, "resource": "momentum", "type": "attack",
         "level": 13, "power": 2.8,
         "desc": "The Monk's signature — a strike of absolute focus."},
        {"name": "Seven-Point Strike","cost": 5, "resource": "momentum","type": "aoe",
         "level": 15, "power": 1.2, "target": "all_enemies",
         "desc": "Strike every enemy simultaneously. Unique among AOE attacks."},
        {"name": "Enlightened Guard","cost": 15, "resource": "Ki",      "type": "buff",
         "level": 17, "buff": "enlightened_guard", "duration": 2, "targets": "all_allies",
         "desc": "Party shares Monk's physical damage reduction for 2 turns."},
        {"name": "Perfect Form",     "cost": 25, "resource": "Ki",      "type": "buff",
         "level": 20, "buff": "perfect_form", "duration": 1, "self_only": True,
         "desc": "Absolute focus: all Momentum abilities cost 0 for 1 full turn. Once per combat."},
    ],

    # ══════════════════════════════════════════════════════════
    #  PALADIN — L1-20 (or L10+ if transitioning)
    #  Divine warrior. Tanks, heals, smites. Does all three
    #  less powerfully than specialists — but no one else does all three.
    # ══════════════════════════════════════════════════════════
    "Paladin": [
        {"name": "Crusader Strike",  "cost": 3, "resource": "momentum", "type": "attack",
         "level": 1, "power": 1.8, "element": "divine",
         "desc": "A righteous blow dealing physical and divine damage."},
        {"name": "Lay on Hands",     "cost": 12, "resource": "PIE-MP",  "type": "heal",
         "level": 1, "power": 1.5, "desc": "Channel healing energy through touch."},
        {"name": "Aura of Courage",  "cost": 18, "resource": "PIE-MP",  "type": "buff",
         "level": 2, "buff": "courage_aura", "duration": 3, "targets": "all_allies",
         "desc": "Radiate courage: party immune to Fear, +15% damage for 3 turns."},
        {"name": "Divine Shield",    "cost": 25, "resource": "PIE-MP",  "type": "buff",
         "level": 4, "buff": "divine_shield", "duration": 1, "self_only": True,
         "desc": "Become nearly invulnerable for 1 turn. Absorbs massive damage."},
        {"name": "Holy Nova",        "cost": 28, "resource": "PIE-MP",  "type": "aoe",
         "level": 6, "power": 2.4, "element": "divine", "target": "all_enemies",
         "desc": "Radiate divine light, damaging all enemies."},
        {"name": "Remove Curse",     "cost": 18, "resource": "PIE-MP",  "type": "cure",
         "level": 8, "cures": "curse", "desc": "Lift curses from an ally."},
        {"name": "Judgment",         "cost": 20, "resource": "PIE-MP",  "type": "attack",
         "level": 10, "power": 2.2, "element": "divine",
         "desc": "Righteous strike. Double damage against shadow-corrupted enemies."},
        {"name": "Sacred Ground",    "cost": 30, "resource": "PIE-MP",  "type": "special",
         "level": 12, "buff": "sacred_ground", "duration": 3,
         "desc": "Consecrate the battlefield. Enemies take divine damage each turn they act."},
        {"name": "Champion",         "cost": 40, "resource": "PIE-MP",  "type": "buff",
         "level": 15, "buff": "champion", "duration": 3, "targets": "all_allies",
         "desc": "Party becomes immune to shadow effects. Paladin's attacks deal +50% divine for 3 turns."},
        {"name": "Divine Reckoning", "cost": 50, "resource": "PIE-MP",  "type": "aoe",
         "level": 20, "power": 2.8, "element": "divine", "target": "all_enemies",
         "heal_power": 0.5,
         "desc": "Massive divine explosion. Party heals for half the total damage dealt."},
    ],

    # ══════════════════════════════════════════════════════════
    #  SPELLBLADE — L1-20
    #  Arcane melee. Only class that scales both STR and INT.
    #  Every swing is also a spell.
    # ══════════════════════════════════════════════════════════
    "Spellblade": [
        {"name": "Arcane Edge",      "cost": 14, "resource": "INT-MP",  "type": "attack",
         "level": 1, "power": 1.8, "element": "arcane",
         "desc": "Melee strike channelling arcane energy through the blade."},
        {"name": "Runic Armor",      "cost": 12, "resource": "INT-MP",  "type": "buff",
         "level": 1, "buff": "runic_armor", "duration": 3, "self_only": True,
         "desc": "Inscribe protective runes: damage reflection for 3 turns."},
        {"name": "Spellstrike",      "cost": 20, "resource": "INT-MP",  "type": "attack",
         "level": 3, "power": 2.0, "element": "arcane",
         "desc": "Deliver a full spell through a melee hit. Bypasses magic resistance."},
        {"name": "Blade Barrier",    "cost": 22, "resource": "INT-MP",  "type": "buff",
         "level": 5, "buff": "blade_barrier", "duration": 2, "self_only": True,
         "desc": "Spinning blades of force: +15 reflected damage on each hit taken."},
        {"name": "Arcane Cleave",    "cost": 26, "resource": "INT-MP",  "type": "aoe",
         "level": 8, "power": 1.4, "element": "arcane", "target": "front_row",
         "desc": "Melee AOE that chains lightning between struck targets."},
        {"name": "Mana Burn",        "cost": 30, "resource": "INT-MP",  "type": "attack",
         "level": 11, "power": 0, "special": "mana_burn",
         "desc": "Deals damage equal to 2× the target's current MP."},
        {"name": "Runic Overload",   "cost": 35, "resource": "INT-MP",  "type": "buff",
         "level": 14, "buff": "runic_overload", "duration": 2, "self_only": True,
         "desc": "All attacks deal full arcane bonus for 2 turns. Take 10% of damage dealt as backlash."},
        {"name": "Annihilate",       "cost": 45, "resource": "INT-MP",  "type": "attack",
         "level": 20, "power": 3.2, "armor_pierce": True, "special": "stat_multiply",
         "desc": "Deals (STR + INT) × 3 damage. The math payoff for building both stats."},
    ],

    # ══════════════════════════════════════════════════════════
    #  DUSKBLADE — L1-20
    #  Shadow warrior. Channels the Fading itself.
    #  Grows stronger as enemies become corrupted.
    # ══════════════════════════════════════════════════════════
    "Duskblade": [
        {"name": "Void Strike",      "cost": 3, "resource": "momentum", "type": "attack",
         "level": 1, "power": 1.4, "element": "shadow", "armor_pierce": True,
         "desc": "Shadow-infused strike. Ignores armour, split physical/shadow damage."},
        {"name": "Shadow Mantle",    "cost": 8, "resource": "DEX-SP",   "type": "buff",
         "level": 1, "buff": "shadow_mantle", "duration": 2, "self_only": True,
         "desc": "Cloak in shadow: reduce incoming damage, next attack deals bonus shadow."},
        {"name": "Corruption",       "cost": 0, "resource": "",         "type": "passive",
         "level": 2, "desc": "Passive: attacks have 25% chance to apply Corrupted status to enemies."},
        {"name": "Dark Empowerment", "cost": 10, "resource": "DEX-SP",  "type": "buff",
         "level": 4, "buff": "dark_empowerment", "duration": 3, "self_only": True,
         "desc": "Embrace the shadow: damage increases by 5% per Corrupted enemy on the field."},
        {"name": "Shadow Dash",      "cost": 4, "resource": "momentum", "type": "attack",
         "level": 6, "power": 1.8, "bonus_crit": 0.50,
         "desc": "Teleport to any row, next attack is a guaranteed critical."},
        {"name": "Void Hunger",      "cost": 5, "resource": "momentum", "type": "attack",
         "level": 9, "power": 1.6, "lifesteal": 0.40,
         "desc": "Lifesteal scales with target's Corruption stacks. Full heal if fully corrupted."},
        {"name": "Shade Form",       "cost": 12, "resource": "DEX-SP",  "type": "buff",
         "level": 12, "buff": "shade_form", "duration": 2, "self_only": True,
         "desc": "Enter shadow state: untargetable by physical attacks, all strikes apply double Corruption."},
        {"name": "Consuming Dark",   "cost": 6, "resource": "momentum", "type": "aoe",
         "level": 15, "power": 1.0, "element": "shadow", "target": "all_enemies",
         "special": "detonate_corruption",
         "desc": "Detonate all Corruption stacks simultaneously. Damage scales massively with stacks."},
        {"name": "One With the Fading","cost": 0,"resource": "",        "type": "buff",
         "level": 20, "buff": "fading_union", "duration": 1, "self_only": True,
         "desc": "Merge with shadow for 1 turn: immune to all damage, every attack deals 50% of target's max HP as shadow. Powered by the Fading itself."},
    ],

    # ══════════════════════════════════════════════════════════
    #  WITCH — L1-20
    #  Curse weaver. Enemies unravel over time.
    #  Status effects stack. Attrition specialist.
    # ══════════════════════════════════════════════════════════
    "Witch": [
        {"name": "Hex Bolt",         "cost": 10, "resource": "INT-MP",  "type": "spell",
         "level": 1, "power": 1.0, "element": "shadow", "status": "Hexed", "status_chance": 0.30,
         "desc": "A bolt of dark magic. Deals shadow damage, 30% chance to Hex the target."},
        {"name": "Hex",              "cost": 16, "resource": "INT-MP",  "type": "debuff",
         "level": 1, "status": "Hexed", "status_chance": 0.75,
         "desc": "Apply a stacking curse. Hexed enemies take increasing damage."},
        {"name": "Dark Bargain",     "cost": 0,  "resource": "INT-MP",  "type": "buff",
         "level": 1, "buff": "dark_bargain", "self_only": True,
         "desc": "Sacrifice 15% HP to restore 30% MP. The Witch's core economy."},
        {"name": "Soul Siphon",      "cost": 18, "resource": "PIE-MP",  "type": "attack",
         "level": 3, "power": 1.4, "special": "drain_buff",
         "desc": "Drain enemy buffs. Each stolen buff restores Witch's MP."},
        {"name": "Mass Sleep",       "cost": 22, "resource": "INT-MP",  "type": "spell",
         "level": 5, "power": 0, "status": "Sleep", "status_chance": 0.50,
         "target": "all_enemies",
         "desc": "Attempt to put all enemies to sleep. 50% chance per enemy."},
        {"name": "Plague",           "cost": 22, "resource": "INT-MP",  "type": "aoe",
         "level": 6, "power": 0.5, "apply_poison": "poison_strong",
         "target": "all_enemies",
         "desc": "Infect all enemies with virulent poison that spreads."},
        {"name": "Wither",           "cost": 28, "resource": "INT-MP",  "type": "debuff",
         "level": 8, "status": "Withered", "status_chance": 0.70, "status_duration": 99,
         "desc": "Permanent stat drain for the duration of the fight. Does not expire."},
        {"name": "Coven's Curse",    "cost": 30, "resource": "INT-MP",  "type": "aoe",
         "level": 11, "status": "Cursed", "status_chance": 0.65,
         "target": "all_enemies",
         "desc": "All enemies gain a stacking curse: each hit they take deals double damage."},
        {"name": "Blood Moon",       "cost": 35, "resource": "PIE-MP",  "type": "buff",
         "level": 15, "buff": "blood_moon", "duration": 3, "self_only": True,
         "desc": "For 3 turns all Witch abilities cost 0 MP but drain HP instead. Maximum output."},
        {"name": "Doom",             "cost": 45, "resource": "PIE-MP",  "type": "attack",
         "level": 20, "power": 0, "special": "doom",
         "desc": "Mark a target with Doom. They die at the end of their next turn, regardless of HP."},
    ],

    # ══════════════════════════════════════════════════════════
    #  NECROMANCER — L1-20
    #  Death as resource. Fallen enemies = power.
    #  The longer the fight, the stronger they become.
    # ══════════════════════════════════════════════════════════
    "Necromancer": [
        {"name": "Life Drain",       "cost": 16, "resource": "INT-MP",  "type": "attack",
         "level": 1, "power": 1.3, "lifesteal": 0.50,
         "desc": "Drain life from an enemy. Heals Necromancer for 50% of damage dealt."},
        {"name": "Bone Cage",        "cost": 18, "resource": "INT-MP",  "type": "debuff",
         "level": 1, "status": "Immobilized", "status_chance": 0.65,
         "desc": "Cage an enemy in bone. 65% chance to immobilize."},
        {"name": "Death Nova",       "cost": 24, "resource": "INT-MP",  "type": "aoe",
         "level": 3, "power": 2.0, "element": "shadow", "target": "all_enemies",
         "desc": "Burst of necrotic energy hitting all enemies."},
        {"name": "Raise Fallen",     "cost": 28, "resource": "PIE-MP",  "type": "revive",
         "level": 5, "desc": "Revive a fallen ally at 30% HP. They fight on."},
        {"name": "Lich Touch",       "cost": 30, "resource": "INT-MP",  "type": "attack",
         "level": 7, "power": 2.2, "element": "shadow", "armor_pierce": True,
         "desc": "Necrotic strike. Bypasses all armor, deals shadow damage."},
        {"name": "Corpse Explosion", "cost": 22, "resource": "INT-MP",  "type": "aoe",
         "level": 9, "power": 2.5, "element": "shadow", "target": "all_enemies",
         "special": "consume_corpse",
         "desc": "Detonate a fallen enemy's corpse. Massive AOE. Consumes the corpse."},
        {"name": "Soul Harvest",     "cost": 0,  "resource": "INT-MP",  "type": "passive",
         "level": 11,
         "desc": "Passive: each enemy death this turn restores Necromancer 10% HP and 15% MP."},
        {"name": "Army of the Dead", "cost": 45, "resource": "PIE-MP",  "type": "special",
         "level": 15, "desc": "Raise up to 3 fallen enemies as temporary allies for 3 turns."},
        {"name": "Death Pact",       "cost": 0,  "resource": "",        "type": "passive",
         "level": 20,
         "desc": "Passive: when Necromancer would die, consume a raised ally instead. One extra life per raised ally."},
    ],

    # ══════════════════════════════════════════════════════════
    #  DRUID — L1-20
    #  Nature control. Wildshape is a second combat mode.
    #  Group healing + nature fury.
    # ══════════════════════════════════════════════════════════
    "Druid": [
        {"name": "Entangle",         "cost": 14, "resource": "WIS-MP",  "type": "aoe",
         "level": 1, "power": 0.3, "status": "Rooted", "status_chance": 0.65,
         "target": "all_enemies",
         "desc": "Vines entangle all enemies. 65% root chance each."},
        {"name": "Rejuvenate",       "cost": 18, "resource": "WIS-MP",  "type": "aoe_heal",
         "level": 1, "power": 0.6, "desc": "Regenerative energy washes over the party."},
        {"name": "Stone Skin",       "cost": 16, "resource": "WIS-MP",  "type": "buff",
         "level": 3, "buff": "stone_skin", "duration": 3, "targets": "all_allies",
         "desc": "Harden allies' skin. Party gains +10 physical defense for 3 turns."},
        {"name": "Slumber Spore",    "cost": 16, "resource": "WIS-MP",  "type": "spell",
         "level": 4, "power": 0, "status": "Sleep", "status_chance": 0.65,
         "target": "enemy_stack",
         "desc": "Sleep spores cloud an enemy group. 65% sleep chance."},
        {"name": "Lightning Storm",  "cost": 26, "resource": "INT-MP",  "type": "aoe",
         "level": 6, "power": 2.2, "element": "lightning", "target": "all_enemies",
         "stun_chance": 0.35,
         "desc": "Call lightning on all enemies. 35% stun chance each."},
        {"name": "Wildshape",        "cost": 30, "resource": "WIS-MP",  "type": "buff",
         "level": 8, "buff": "wildshape", "duration": 3, "self_only": True,
         "desc": "Transform into a great beast: all physical abilities enhanced, spells unavailable."},
        {"name": "Thorn Aura",       "cost": 20, "resource": "WIS-MP",  "type": "buff",
         "level": 10, "buff": "thorn_aura", "duration": 3, "targets": "all_allies",
         "desc": "Surround party in thorns. Enemies take nature damage each time they strike."},
        {"name": "Call Lightning",   "cost": 35, "resource": "INT-MP",  "type": "aoe",
         "level": 13, "power": 2.4, "element": "lightning", "target": "all_enemies",
         "desc": "Focused lightning blast. Double damage against wet or frozen targets."},
        {"name": "Great Wildshape",  "cost": 45, "resource": "WIS-MP",  "type": "buff",
         "level": 17, "buff": "great_wildshape", "duration": 4, "self_only": True,
         "desc": "Become a greater beast: enhanced Wildshape, party healed each turn you act."},
        {"name": "Nature's Wrath",   "cost": 50, "resource": "INT-MP",  "type": "aoe",
         "level": 20, "power": 1.8, "element": "nature", "target": "all_enemies",
         "desc": "The land itself attacks. Earthquake + lightning + roots simultaneously."},
    ],

    # ══════════════════════════════════════════════════════════
    #  MYSTIC — L1-20
    #  Arcane + Ki fusion. Two regenerating resources.
    #  Ki generates Momentum. MP fuels Ki. The longer the fight,
    #  the more fluid and powerful they become.
    # ══════════════════════════════════════════════════════════
    "Mystic": [
        {"name": "Force Pulse",      "cost": 16, "resource": "INT-MP",  "type": "aoe",
         "level": 1, "power": 1.0, "element": "arcane", "target": "front_row",
         "desc": "Release a pulse of pure force hitting the front row."},
        {"name": "Ki Absorption",    "cost": 7,  "resource": "Ki",       "type": "buff",
         "level": 1, "buff": "ki_absorption", "duration": 1, "self_only": True,
         "desc": "Absorb the next spell that hits you, converting it to Ki instead of damage."},
        {"name": "Arcane Palm",      "cost": 18, "resource": "INT-MP",  "type": "attack",
         "level": 3, "power": 1.8, "element": "arcane",
         "desc": "Deliver concentrated arcane energy through a melee palm strike."},
        {"name": "Lullaby",          "cost": 18, "resource": "INT-MP",  "type": "spell",
         "level": 4, "power": 0, "status": "Sleep", "status_chance": 0.55,
         "target": "enemy_row",
         "desc": "A mental lullaby. 55% sleep chance to an entire enemy row."},
        {"name": "Mindstrike",       "cost": 20, "resource": "INT-MP",  "type": "attack",
         "level": 6, "power": 1.6, "armor_pierce": True,
         "desc": "Pure mental force strike. Ignores all physical defense."},
        {"name": "Arcane Flurry",    "cost": 24, "resource": "INT-MP",  "type": "attack",
         "level": 8, "power": 0.7, "hits": 5,
         "desc": "Five rapid arcane strikes. Each hit can trigger passive Ki regeneration."},
        {"name": "Inner Sanctum",    "cost": 20, "resource": "Ki",       "type": "buff",
         "level": 11, "buff": "inner_sanctum", "duration": 2, "self_only": True,
         "desc": "For 2 turns, all damage Mystic takes restores Ki instead of depleting HP."},
        {"name": "Void Meditation",  "cost": 0,  "resource": "",        "type": "special",
         "level": 14, "desc": "Skip this turn to restore 40% MP and 40% Ki simultaneously. A calculated sacrifice."},
        {"name": "Fist of Heaven",   "cost": 5,  "resource": "momentum", "type": "attack",
         "level": 17, "power": 3.0, "element": "arcane", "special": "dual_resource",
         "resource2": "INT-MP", "cost2": 30,
         "desc": "Costs both Momentum AND MP. Deals (INT + WIS) × 4 damage. The fusion made flesh."},
        {"name": "Transcend",        "cost": 30, "resource": "Ki",       "type": "buff",
         "level": 20, "buff": "transcend", "duration": 1, "self_only": True,
         "desc": "Operate outside normal physics for 1 turn: all abilities cost 0, all attacks hit, all damage bypasses defense."},
    ],

    # ══════════════════════════════════════════════════════════
    #  ASSASSIN — L1-20
    #  Setup → perfect kill. Highest single-target burst.
    #  Every action either sets up the kill or IS the kill.
    # ══════════════════════════════════════════════════════════
    "Assassin": [
        {"name": "Shadow Step",      "cost": 6,  "resource": "DEX-SP",   "type": "buff",
         "level": 1, "buff": "shadow_step", "duration": 1, "self_only": True,
         "desc": "Vanish into shadow. Next attack deals +50% damage."},
        {"name": "Crippling Strike", "cost": 2,  "resource": "momentum", "type": "attack",
         "level": 1, "power": 1.5, "status": "Crippled", "status_chance": 0.60,
         "desc": "Cripple an enemy: reduce their speed and accuracy."},
        {"name": "Fan of Knives",    "cost": 2,  "resource": "momentum", "type": "aoe",
         "level": 3, "power": 1.2, "target": "front_row",
         "desc": "Spray blades at the front row."},
        {"name": "Throat Cut",       "cost": 3,  "resource": "momentum", "type": "attack",
         "level": 5, "power": 2.5, "status": "Silenced", "status_chance": 0.75,
         "desc": "Deep cut to the throat. Massive damage + 75% silence chance."},
        {"name": "Death Mark",       "cost": 8,  "resource": "DEX-SP",   "type": "debuff",
         "level": 7, "mark_duration": 3, "mark_crit_bonus": 0.50,
         "desc": "Mark a target. All attacks on them have +50% critical hit chance."},
        {"name": "Mark of Execution","cost": 10, "resource": "DEX-SP",   "type": "debuff",
         "level": 9, "status": "Execution_Mark", "status_duration": 2,
         "desc": "Execution Mark: target takes +50% damage from ALL sources for 2 turns."},
        {"name": "Shadowstrike",     "cost": 5,  "resource": "momentum", "type": "attack",
         "level": 12, "power": 2.8, "armor_pierce": True,
         "desc": "Strike from absolute shadow. Unblockable, cannot be defended against."},
        {"name": "One Thousand Cuts","cost": 6,  "resource": "momentum", "type": "aoe",
         "level": 16, "power": 0.8, "hits": 8, "target": "all_enemies",
         "desc": "Strike every enemy eight times with every available weapon simultaneously."},
        {"name": "Perfect Kill",     "cost": 8,  "resource": "momentum", "type": "attack",
         "level": 20, "power": 5.0, "execute_threshold": 1.0, "special": "marked_instant_kill",
         "desc": "If target is marked: instant kill regardless of HP. If not marked: 5× damage. Setup matters."},
    ],

    # ══════════════════════════════════════════════════════════
    #  SHAMAN — L1-20
    #  Bridge between living and ancestral. Calls power from beyond.
    #  The longer the fight, the more spirits answer.
    # ══════════════════════════════════════════════════════════
    "Shaman": [
        {"name": "Spirit Strike",    "cost": 2,  "resource": "momentum", "type": "attack",
         "level": 1, "power": 1.4, "element": "spirit",
         "desc": "A blow guided by ancestral spirits. Physical + spirit damage."},
        {"name": "Spirit Bind",      "cost": 16, "resource": "WIS-MP",  "type": "buff",
         "level": 1, "buff": "spirit_bond", "duration": 3, "targets": "all_allies",
         "desc": "Bind ancestral spirits to the party. Allies gain +6 to all defenses."},
        {"name": "Totemic Barrier",  "cost": 18, "resource": "WIS-MP",  "type": "buff",
         "level": 1, "buff": "totemic_barrier", "duration": 3, "targets": "all_allies",
         "desc": "Erect a totem ward. Party takes 20% less magic damage for 3 turns."},
        {"name": "Earth Pulse",      "cost": 20, "resource": "WIS-MP",  "type": "aoe",
         "level": 3, "power": 1.8, "element": "earth", "target": "all_enemies",
         "desc": "Shockwave through the earth. Hits all enemies, disrupts enemy spellcasting."},
        {"name": "Ancestral Strike", "cost": 2,  "resource": "momentum", "type": "attack",
         "level": 5, "power": 3.4,
         "desc": "Guided by ancestors. Devastating single strike."},
        {"name": "Spirit Cleanse",   "cost": 20, "resource": "WIS-MP",  "type": "aoe_heal",
         "level": 7, "power": 0.7,
         "desc": "Ancestral healing energy washes the party, restoring HP and removing minor ailments."},
        {"name": "Ancestor's Wrath", "cost": 30, "resource": "WIS-MP",  "type": "aoe",
         "level": 10, "power": 1.4, "element": "spirit", "target": "all_enemies",
         "special": "scales_with_fallen",
         "desc": "Ancestral spirits strike all enemies. Damage scales with number of fallen party members."},
        {"name": "Spirit Walk",      "cost": 40, "resource": "WIS-MP",  "type": "buff",
         "level": 13, "buff": "spirit_walk", "duration": 2, "self_only": True,
         "desc": "Leave body in spirit form: untargetable, party gains all Shaman buffs for 2 turns."},
        {"name": "Totem of the Ages","cost": 35, "resource": "WIS-MP",  "type": "special",
         "level": 16,
         "desc": "Place a powerful totem: heals party 10% HP per round, enemies take 20% more damage. Totem can be destroyed."},
        {"name": "Voice of Ancestors","cost": 0, "resource": "",        "type": "special",
         "level": 20,
         "desc": "Call all fallen party members back as ancestor spirits for 1 full round. They act again at full power before departing."},
    ],
}



ENEMY_ABILITIES = {
    # Goblin Shaman
    "Hex Bolt": {
        "name": "Hex Bolt", "type": "spell", "power": 1.3, "element": "shadow",
        "cost": 0, "resource": "", "desc": "Dark magic bolt",
    },
    "Goblin Curse": {
        "name": "Goblin Curse", "type": "debuff", "apply_curse": "curse_jinx",
        "cost": 0, "resource": "", "chance": 0.50, "desc": "Jinx reducing accuracy",
    },
    # Orc Warchief
    "War Cry": {
        "name": "War Cry", "type": "buff", "buff": "war_cry", "duration": 3,
        "cost": 0, "resource": "", "targets": "all_allies", "desc": "Empower all allies",
    },
    "Skull Crush": {
        "name": "Skull Crush", "type": "attack", "power": 2.0, "stun_chance": 0.30,
        "cost": 0, "resource": "", "desc": "Devastating overhead blow",
    },
    # Wolf Alpha
    "Pack Howl": {
        "name": "Pack Howl", "type": "buff", "buff": "pack_howl", "duration": 2,
        "cost": 0, "resource": "", "targets": "all_allies", "desc": "Embolden the pack",
    },
    "Lunge": {
        "name": "Lunge", "type": "attack", "power": 1.8,
        "cost": 0, "resource": "", "desc": "Leaping strike",
    },
    # Bandit Leader
    "Dirty Trick": {
        "name": "Dirty Trick", "type": "debuff", "blind_duration": 2,
        "cost": 0, "resource": "", "chance": 0.40, "desc": "Throw dirt in eyes",
    },
    "Flurry": {
        "name": "Flurry", "type": "attack", "power": 0.7, "hits": 3,
        "cost": 0, "resource": "", "desc": "Rapid slashes",
    },
    # Bosses
    "Goblin King Smash": {
        "name": "Goblin King Smash", "type": "attack", "power": 2.5,
        "cost": 0, "resource": "", "stun_chance": 0.25, "desc": "Massive club slam",
    },
    "Summon Goblins": {
        "name": "Summon Goblins", "type": "summon", "summon_key": "Goblin Warrior", "count": 2,
        "cost": 0, "resource": "", "cooldown": 4, "desc": "Call goblin reinforcements",
    },
    "Poison Cloud": {
        "name": "Poison Cloud", "type": "aoe", "power": 0.8, "element": "nature",
        "apply_poison": "poison_strong", "cost": 0, "resource": "", "desc": "Toxic cloud",
    },
    "Enrage": {
        "name": "Enrage", "type": "buff", "buff": "enrage", "duration": 4,
        "cost": 0, "resource": "", "desc": "Become enraged, dealing double damage",
    },
    # Act 3 — Pale Sentinel
    "Tide of Judgment": {
        "name": "Tide of Judgment", "type": "aoe", "power": 1.4, "element": "divine",
        "cost": 0, "resource": "", "desc": "Wave of divine energy hits all enemies",
    },
    "Ward of Isolation": {
        "name": "Ward of Isolation", "type": "buff", "buff": "ward_isolation", "duration": 2,
        "cost": 0, "resource": "", "desc": "Reduces all incoming damage by 40% for 2 turns",
    },
    "Sentinel's Resolve": {
        "name": "Sentinel's Resolve", "type": "heal", "power": 180,
        "cost": 0, "resource": "", "cooldown": 5, "desc": "Draws on decades of vigil to restore vitality",
    },
    # Act 3 — Last Keeper
    "Tempest Barrage": {
        "name": "Tempest Barrage", "type": "aoe", "power": 1.3, "element": "lightning",
        "cost": 0, "resource": "", "desc": "Fires arcs of lightning at every enemy",
    },
    "Cyclone Ward": {
        "name": "Cyclone Ward", "type": "buff", "buff": "cyclone_ward", "duration": 2,
        "cost": 0, "resource": "", "desc": "Cyclone deflects physical attacks for 2 turns",
    },
    "Chain Lightning": {
        "name": "Chain Lightning", "type": "aoe", "power": 1.2, "element": "lightning",
        "cost": 0, "resource": "", "desc": "Lightning jumps between all enemies",
    },
    # Act 3 — Valdris Phase 1
    "Ward Shatter": {
        "name": "Ward Shatter", "type": "debuff", "apply_curse": "ward_shatter",
        "cost": 0, "resource": "", "desc": "Tears protective wards, reducing magic resist by 15 for 3 turns",
    },
    # Act 3 — Valdris Phase 2
    "Desperate Nova": {
        "name": "Desperate Nova", "type": "aoe", "power": 1.6, "element": "arcane",
        "cost": 0, "resource": "", "desc": "Last surge of power blasting all enemies",
    },
    "Last Ward": {
        "name": "Last Ward", "type": "buff", "buff": "last_ward", "duration": 1,
        "cost": 0, "resource": "", "desc": "Erects a final protective ward",
    },
    "Plea of the Fallen": {
        "name": "Plea of the Fallen", "type": "debuff",
        "effect": {"morale_break": True, "duration": 2},
        "cost": 0, "resource": "", "desc": "Sorrow radiates outward, reducing party attack by 20% for 2 turns",
    },

    # ── Korrath (Mine Boss) ───────────────────────────────────────
    "Stone Slam": {
        "name": "Stone Slam", "type": "attack", "power": 2.2,
        "stun_chance": 0.25, "phys_type": "blunt",
        "cost": 0, "resource": "", "desc": "A crushing two-handed blow that may stun",
    },
    "Ward Pulse": {
        "name": "Ward Pulse", "type": "aoe", "power": 0.7, "element": "divine",
        "cost": 0, "resource": "", "desc": "A burst of warden energy hits all enemies",
    },

    # ── Commander Ashvar (Ashenmoor Boss) ─────────────────────────
    "Ashen Wave": {
        "name": "Ashen Wave", "type": "aoe", "power": 0.9, "element": "fire",
        "cost": 0, "resource": "", "desc": "A wave of superheated ash engulfs the party",
    },
    "Shadow Bind": {
        "name": "Shadow Bind", "type": "debuff", "power": 0,
        "apply_status": "Immobilized", "status_duration": 2, "status_chance": 0.55,
        "cost": 0, "resource": "", "desc": "Shadow tendrils root a target in place",
    },
    "Commander's Wrath": {
        "name": "Commander's Wrath", "type": "attack", "power": 2.5,
        "phys_type": "slashing",
        "cost": 0, "resource": "", "desc": "An overwhelming strike that bypasses some defense",
    },

    # ── Ash Revenant ──────────────────────────────────────────────
    "Cinder Touch": {
        "name": "Cinder Touch", "type": "attack", "power": 1.4, "element": "fire",
        "apply_status": "Burning", "status_duration": 2, "status_chance": 0.45,
        "cost": 0, "resource": "", "desc": "A burning strike that may ignite the target",
    },

    # ── Bandits / Mercenaries / Cultists / Crypt ──────────────────
    "enemy_crippling_strike": {
        "name": "Crippling Strike", "type": "attack", "power": 1.5,
        "apply_status": "Slowed", "status_duration": 2, "status_chance": 0.50,
        "cost": 0, "resource": "", "desc": "A precise strike that slows the target",
    },
    "enemy_fireball": {
        "name": "Fireball", "type": "aoe", "power": 1.1, "element": "fire",
        "cost": 0, "resource": "", "desc": "An explosive ball of fire hits all party members",
    },
    "enemy_war_cry": {
        "name": "War Cry", "type": "buff", "buff": "war_cry",
        "duration": 3, "targets": "all_allies",
        "cost": 0, "resource": "", "desc": "Rally allies, boosting all attack damage",
    },
    "enemy_cleave": {
        "name": "Cleave", "type": "aoe", "power": 0.85, "phys_type": "slashing",
        "targets": "front_row",
        "cost": 0, "resource": "", "desc": "A wide swing hitting all front-row targets",
    },
    "enemy_pinning_shot": {
        "name": "Pinning Shot", "type": "attack", "power": 1.2, "element": "piercing",
        "apply_status": "Slowed", "status_duration": 2, "status_chance": 0.60,
        "cost": 0, "resource": "", "desc": "An arrow that pins the target, slowing movement",
    },
    "enemy_stunning_blow": {
        "name": "Stunning Blow", "type": "attack", "power": 1.6,
        "stun_chance": 0.35, "phys_type": "blunt",
        "cost": 0, "resource": "", "desc": "A calculated strike aimed at stunning the target",
    },
    "enemy_minor_heal": {
        "name": "Minor Heal", "type": "heal", "power": 30,
        "targets": "lowest_hp_ally",
        "cost": 0, "resource": "", "desc": "A quick healing prayer restoring moderate HP",
    },
    "enemy_smite": {
        "name": "Smite", "type": "attack", "power": 1.7, "element": "divine",
        "cost": 0, "resource": "", "desc": "A divinely-charged strike",
    },
    "enemy_arcane_slash": {
        "name": "Arcane Slash", "type": "attack", "power": 1.5, "element": "arcane",
        "cost": 0, "resource": "", "desc": "A blade strike channeling arcane energy",
    },
    "enemy_shadow_bolt": {
        "name": "Shadow Bolt", "type": "spell", "power": 1.2, "element": "shadow",
        "cost": 0, "resource": "", "desc": "A bolt of condensed shadow energy",
    },
    "enemy_weaken": {
        "name": "Weaken", "type": "debuff", "power": 0,
        "apply_status": "Weakened", "status_duration": 3, "status_chance": 0.65,
        "cost": 0, "resource": "", "desc": "A hex that reduces the target's attack power",
    },
    "enemy_mass_weaken": {
        "name": "Mass Weaken", "type": "aoe", "power": 0,
        "apply_status": "Weakened", "status_duration": 2, "status_chance": 0.55,
        "targets": "all_enemies",
        "cost": 0, "resource": "", "desc": "A ritual curse weakening the entire party",
    },
}


# ═══════════════════════════════════════════════════════════════
#  BOSS DEFINITIONS
# ═══════════════════════════════════════════════════════════════

BOSS_ENCOUNTERS = {
    "goblin_warren": {
        "name": "Grak the Goblin King",
        "enemy_key": "Goblin King",
        "escort": [("Goblin Warrior", 2), ("Goblin Shaman", 1)],
        "description": "The self-proclaimed king of the warren, Grak sits on a throne of scrap metal.",
    },
    "spiders_nest": {
        "name": "Shelob's Daughter",
        "enemy_key": "Giant Spider Queen",
        "escort": [("Giant Spider", 3)],
        "description": "A massive spider, her abdomen pulsing with venom.",
    },
    "abandoned_mine": {
        "name": "The Foreman",
        "enemy_key": "Undead Foreman",
        "escort": [("Skeleton Warrior", 2)],
        "description": "The mine's last overseer, still commanding the dead.",
    },
    "sunken_crypt": {
        "name": "Lord Vareth",
        "enemy_key": "Crypt Lord",
        "escort": [("Skeleton Warrior", 3)],
        "description": "An ancient lich lord, entombed for centuries.",
    },
    "ruins_ashenmoor": {
        "name": "Ashenmoor Guardian",
        "enemy_key": "Stone Golem",
        "escort": [("Orc Fighter", 2)],
        "description": "A massive construct of living stone, guardian of the ruins.",
    },
}


# ═══════════════════════════════════════════════════════════════
#  ABILITY BRANCHES — Forking Path Choices
# ═══════════════════════════════════════════════════════════════
#
# At certain levels each class must choose ONE of two abilities,
# permanently locking out the other branch.
# Format: {class_name: {level: [option_A, option_B]}}
#
# Design philosophy:
#   • Each pair represents a clear playstyle fork (offense vs utility,
#     single-target vs AoE, melee vs ranged, etc.)
#   • Both options are equally valid — no "wrong" choice
#   • The unchosen ability is permanently locked (adds identity)
#   • Branches at levels 3, 7, and 10 for base classes


ABILITY_BRANCHES = {

    "Fighter": {
        3: [
            {"name": "Shield Bash", "cost": 3, "resource": "momentum", "type": "attack",
             "level": 3, "power": 1.3, "stun_chance": 0.35,
             "desc": "Bash with your shield. 35% chance to stun the target.",
             "branch_label": "Defender",
             "branch_desc": "Master of defense and crowd control."},
            {"name": "Reckless Charge", "cost": 4, "resource": "momentum", "type": "attack",
             "level": 3, "power": 1.8, "self_damage_pct": 0.05,
             "desc": "Charge headlong into the enemy. Huge damage but you take 5% of your HP in recoil.",
             "branch_label": "Berserker",
             "branch_desc": "High risk, high reward aggression."},
        ],
        7: [
            {"name": "War Cry", "cost": 7, "resource": "STR-SP", "type": "buff",
             "level": 7, "buff": "war_cry", "duration": 3, "targets": "all_allies",
             "desc": "Rallying shout. All allies deal +25% damage for 3 turns.",
             "branch_label": "Commander",
             "branch_desc": "Inspire and lead your party to victory."},
            {"name": "Cleave", "cost": 2, "resource": "momentum", "type": "aoe",
             "level": 7, "power": 1.1,
             "desc": "Wide sweeping blow that hits all front-row enemies.",
             "branch_label": "Slayer",
             "branch_desc": "Mow through crowds with sweeping attacks."},
        ],
        10: [
            {"name": "Last Stand", "cost": 10, "resource": "STR-SP", "type": "buff",
             "level": 10, "buff": "last_stand", "duration": 3, "self_only": True,
             "desc": "When below 25% HP, enter a fury state: +50% damage and cannot be stunned.",
             "branch_label": "Warlord",
             "branch_desc": "Thrive in the chaos of near-death."},
            {"name": "Executioner", "cost": 5, "resource": "momentum", "type": "attack",
             "level": 10, "power": 2.5, "execute_threshold": 0.25,
             "desc": "Devastating blow. Instantly kills targets below 25% HP.",
             "branch_label": "Executioner",
             "branch_desc": "End weakened foes with brutal efficiency."},
        ],
    },

    "Mage": {
        3: [
            {"name": "Firebolt", "cost": 10, "resource": "INT-MP", "type": "spell",
             "level": 3, "power": 1.3, "element": "fire", "dot": "burning", "dot_duration": 2,
             "desc": "Fire bolt that ignites the target, dealing burn damage for 2 turns.",
             "branch_label": "Pyromancer",
             "branch_desc": "Burning DoTs and explosive fire magic."},
            {"name": "Frostbolt", "cost": 10, "resource": "INT-MP", "type": "spell",
             "level": 3, "power": 1.2, "element": "ice", "slow_chance": 0.50,
             "desc": "Shard of ice. 50% chance to slow the target.",
             "branch_label": "Frostweaver",
             "branch_desc": "Slow and control with ice magic."},
        ],
        7: [
            {"name": "Fireball", "cost": 20, "resource": "INT-MP", "type": "aoe",
             "level": 7, "power": 1.4, "element": "fire", "target": "row",
             "desc": "Explosive fire blast hitting all enemies in a row.",
             "branch_label": "Bombardier",
             "branch_desc": "Devastate enemy rows with area explosions."},
            {"name": "Deep Freeze", "cost": 18, "resource": "INT-MP", "type": "spell",
             "level": 7, "power": 1.6, "element": "ice", "stun_chance": 0.35,
             "desc": "Encase target in ice. 35% chance to stun for 1 turn.",
             "branch_label": "Glaciomancer",
             "branch_desc": "Lock down powerful single targets."},
        ],
        10: [
            {"name": "Chain Lightning", "cost": 25, "resource": "INT-MP", "type": "aoe",
             "level": 10, "power": 1.3, "element": "lightning",
             "desc": "Arc of lightning jumping between all enemies.",
             "branch_label": "Stormcaller",
             "branch_desc": "Electrify the battlefield with chain effects."},
            {"name": "Meteor", "cost": 40, "resource": "INT-MP", "type": "aoe",
             "level": 10, "power": 1.8, "element": "fire",
             "desc": "Call down a cataclysmic meteor strike on all enemies.",
             "branch_label": "Armageddon",
             "branch_desc": "Single devastating nuke to end the fight."},
        ],
    },

    "Cleric": {
        3: [
            {"name": "Cure Poison", "cost": 8, "resource": "PIE-MP", "type": "cure",
             "level": 3, "cures": "poison",
             "desc": "Purge poison from any ally. Removes all poison stacks.",
             "branch_label": "Healer",
             "branch_desc": "Cleanse and protect your allies."},
            {"name": "Smite Evil", "cost": 14, "resource": "PIE-MP", "type": "spell",
             "level": 3, "power": 1.8, "element": "divine", "targets": "undead_extra",
             "desc": "Radiant strike. Triple damage against undead and shadow enemies.",
             "branch_label": "Crusader",
             "branch_desc": "Destroy undead and shadow creatures."},
        ],
        7: [
            {"name": "Prayer of Healing", "cost": 20, "resource": "PIE-MP", "type": "aoe_heal",
             "level": 7, "power": 1.0,
             "desc": "Bathe all allies in divine light. Heals the whole party.",
             "branch_label": "High Priest",
             "branch_desc": "Sustain your entire party through any trial."},
            {"name": "Turn Undead", "cost": 15, "resource": "PIE-MP", "type": "debuff",
             "level": 7, "targets": "undead", "fear_duration": 3,
             "desc": "Command undead enemies to flee in terror for 3 turns.",
             "branch_label": "Inquisitor",
             "branch_desc": "Break the will of darkness with holy authority."},
        ],
        10: [
            {"name": "Resurrection", "cost": 35, "resource": "PIE-MP", "type": "revive",
             "level": 10, "revive_hp_pct": 0.5,
             "desc": "Call a fallen ally back from death at 50% HP.",
             "branch_label": "Life Warden",
             "branch_desc": "No ally stays down when you watch over them."},
            {"name": "Divine Wrath", "cost": 30, "resource": "PIE-MP", "type": "aoe",
             "level": 10, "power": 1.8, "element": "divine",
             "desc": "Unleash divine fury on all enemies simultaneously.",
             "branch_label": "Avenger",
             "branch_desc": "Punish evil with righteous devastation."},
        ],
    },

    "Thief": {
        3: [
            {"name": "Backstab", "cost": 4, "resource": "momentum", "type": "attack",
             "level": 3, "power": 2.0, "bonus_crit": 25,
             "desc": "Brutal strike from the shadows. Massive damage on crits.",
             "branch_label": "Assassin",
             "branch_desc": "Alpha-strike for massive single-target damage."},
            {"name": "Cripple", "cost": 5, "resource": "DEX-SP", "type": "debuff",
             "level": 3, "slow_duration": 3, "armor_shred": 2,
             "desc": "Slash tendons to slow and weaken a target for 3 turns.",
             "branch_label": "Saboteur",
             "branch_desc": "Disable and weaken before moving in for the kill."},
        ],
        7: [
            {"name": "Poison Blade", "cost": 3, "resource": "momentum", "type": "attack",
             "level": 7, "power": 1.2, "apply_poison": "poison_strong",
             "desc": "Envenomed blade. Applies Strong Poison (10dmg/3 steps, 6 ticks).",
             "branch_label": "Venomancer",
             "branch_desc": "Stack poisons for sustained damage over time."},
            {"name": "Smoke Bomb", "cost": 8, "resource": "DEX-SP", "type": "buff",
             "level": 7, "buff": "smoke_screen", "duration": 2, "targets": "all_allies",
             "desc": "Obscuring smoke: all allies gain high evasion for 2 turns.",
             "branch_label": "Tactician",
             "branch_desc": "Control the battlefield and protect the party."},
        ],
        10: [
            {"name": "Death Mark", "cost": 11, "resource": "DEX-SP", "type": "debuff",
             "level": 10, "mark_duration": 4, "mark_crit_bonus": 30,
             "desc": "Mark a target for death. All attacks on it gain +30% crit chance.",
             "branch_label": "Shadowblade",
             "branch_desc": "Designate one target for total annihilation."},
            {"name": "Assassinate", "cost": 5, "resource": "momentum", "type": "attack",
             "level": 10, "power": 3.0, "bonus_crit": 30,
             "desc": "All-or-nothing lethal strike. Devastating damage on crit.",
             "branch_label": "Nightstalker",
             "branch_desc": "One perfect strike to end the fight."},
        ],
    },

    "Ranger": {
        3: [
            {"name": "Entangle", "cost": 12, "resource": "WIS-MP", "type": "debuff",
             "level": 3, "element": "nature", "slow_duration": 2,
             "desc": "Magical roots slow and hold a target for 2 turns.",
             "branch_label": "Warden",
             "branch_desc": "Command nature to restrain and control."},
            {"name": "Twin Shot", "cost": 2, "resource": "momentum", "type": "attack",
             "level": 3, "power": 0.9, "hits": 2,
             "desc": "Loose two arrows in quick succession. Hits twice at 90% power each.",
             "branch_label": "Sharpshooter",
             "branch_desc": "Double your arrow output for maximum damage."},
        ],
        7: [
            {"name": "Nature's Balm", "cost": 14, "resource": "WIS-MP", "type": "heal",
             "level": 7, "power": 1.0, "cures": "poison",
             "desc": "Natural remedy. Heals one ally and cures poison.",
             "branch_label": "Naturalist",
             "branch_desc": "Sustain your party with nature's healing power."},
            {"name": "Barrage", "cost": 2, "resource": "momentum", "type": "aoe",
             "level": 7, "power": 1.0,
             "desc": "Unleash a volley of arrows at all enemies.",
             "branch_label": "Volley Master",
             "branch_desc": "Suppress entire enemy groups with arrows."},
        ],
        10: [
            {"name": "Hawk Eye", "cost": 20, "resource": "WIS-MP", "type": "buff",
             "level": 10, "buff": "hawk_eye", "duration": 4, "self_only": True,
             "desc": "Perfect focus: +40% accuracy and +20% damage for 4 turns.",
             "branch_label": "Eagle Eye",
             "branch_desc": "Transcendent marksmanship under focus."},
            {"name": "Lethal Shot", "cost": 5, "resource": "momentum", "type": "attack",
             "level": 10, "power": 2.5, "bonus_accuracy": 30,
             "desc": "A single, perfectly aimed shot for massive damage.",
             "branch_label": "Deadeye",
             "branch_desc": "One perfect shot, guaranteed to land."},
        ],
    },

    "Monk": {
        3: [
            {"name": "Stunning Fist", "cost": 3, "resource": "momentum", "type": "attack",
             "level": 3, "power": 1.3, "stun_chance": 0.45,
             "desc": "Precise nerve strike. 45% chance to stun.",
             "branch_label": "Striker",
             "branch_desc": "Disable foes with precision nerve attacks."},
            {"name": "Ki Deflect", "cost": 5, "resource": "Ki", "type": "buff",
             "level": 3, "buff": "ki_deflect", "duration": 2,
             "desc": "Channel Ki to deflect the next physical attack entirely.",
             "branch_label": "Guardian",
             "branch_desc": "Protect yourself and allies through Ki mastery."},
        ],
        7: [
            {"name": "Inner Peace", "cost": 7, "resource": "Ki", "type": "heal",
             "level": 7, "power": 1.2, "self_only": True,
             "desc": "Deep meditation restores own HP by a significant amount.",
             "branch_label": "Contemplative",
             "branch_desc": "Sustain yourself through spiritual fortitude."},
            {"name": "Pressure Point", "cost": 9, "resource": "Ki", "type": "debuff",
             "level": 7, "weaken_duration": 3,
             "desc": "Strike vital points. Target deals 30% less damage for 3 turns.",
             "branch_label": "Tactician",
             "branch_desc": "Weaken enemies through anatomical expertise."},
        ],
        10: [
            {"name": "Dragon Strike", "cost": 5, "resource": "momentum", "type": "attack",
             "level": 10, "power": 2.8, "element": "fire",
             "desc": "Channel pure Ki into a devastating flaming strike.",
             "branch_label": "Dragon Fist",
             "branch_desc": "Unleash elemental power through raw Ki."},
            {"name": "Empty Mind", "cost": 10, "resource": "Ki", "type": "buff",
             "level": 10, "buff": "empty_mind", "duration": 3,
             "desc": "Achieve perfect clarity: immune to debuffs, +2 actions per turn.",
             "branch_label": "Void Walker",
             "branch_desc": "Transcend combat through perfect emptiness."},
        ],
    },
}


def get_branch_at_level(class_name, level):
    """Branches removed — all abilities are freely trainable at the guild.
    Always returns None so no branch-choice UI is triggered."""
    return None


def has_branch_choice_pending(character):
    """Branches removed — all abilities are freely trainable at the guild.
    Always returns None."""
    return None


def choose_branch(character, chosen_ability):
    """
    Record the player's branch choice. Adds the chosen ability to the character.
    The unchosen ability is implicitly locked (not present in abilities list).
    """
    known_names = {a["name"] for a in character.abilities}
    if chosen_ability["name"] not in known_names:
        character.abilities.append(chosen_ability.copy())
    return True
def get_new_abilities_at_level(class_name: str, level: int) -> list:
    """Return list of abilities that unlock at exactly the given level for a class."""
    return [a for a in CLASS_ABILITIES.get(class_name, [])
            if a.get("level", 1) == level]


# ── Merge branch abilities into CLASS_ABILITIES ──────────────────────────────
# Since branching is removed, all branch-choice abilities are now regular
# trainable abilities available at the guild at the appropriate level.
for _cls, _branch_levels in ABILITY_BRANCHES.items():
    _existing_names = {a["name"] for a in CLASS_ABILITIES.get(_cls, [])}
    for _level, _opts in _branch_levels.items():
        for _opt in _opts:
            if _opt["name"] not in _existing_names:
                _ab = dict(_opt)
                _ab.setdefault("level", _level)
                CLASS_ABILITIES.setdefault(_cls, []).append(_ab)
                _existing_names.add(_opt["name"])


