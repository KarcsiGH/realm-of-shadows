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

CLASS_ABILITIES = {
    "Fighter": [
        {"name": "Power Strike",     "cost": 10, "resource": "STR-SP", "type": "attack",
         "level": 1, "power": 1.6, "desc": "Heavy melee attack dealing 60% bonus damage."},
        {"name": "Defensive Stance", "cost": 8,  "resource": "STR-SP", "type": "buff",
         "level": 1, "buff": "defense_up", "duration": 2, "self_only": True, "desc": "Reduce incoming damage for 2 turns."},
        {"name": "Shield Bash",      "cost": 12, "resource": "STR-SP", "type": "attack",
         "level": 3, "power": 1.3, "stun_chance": 0.35, "desc": "Bash with shield. 35% chance to stun."},
        {"name": "Cleave",           "cost": 18, "resource": "STR-SP", "type": "aoe",
         "level": 5, "power": 1.0, "desc": "Wide slash hitting all front-row enemies."},
        {"name": "War Cry",          "cost": 15, "resource": "STR-SP", "type": "buff",
         "level": 8, "buff": "war_cry", "duration": 3, "targets": "all_allies", "desc": "Inspire allies, boosting damage for 3 turns."},
        {"name": "Executioner",      "cost": 25, "resource": "STR-SP", "type": "attack",
         "level": 12, "power": 2.5, "execute_threshold": 0.25, "desc": "Devastating blow. Instant kill if target below 25% HP."},
        # ─── Level-gap fill ───────────────────────────────────────────
        {"name": "Second Wind",      "cost": 0,  "resource": "STR-SP", "type": "heal",
         "level": 2, "power": 0.9, "self_only": True,
         "desc": "Draw on reserves to restore ~20% of max HP instantly."},
        {"name": "Taunt",            "cost": 8,  "resource": "STR-SP", "type": "taunt",
         "level": 2, "taunt_duration": 2,
         "desc": "Draw all enemy attention. Forces enemies to target you for 2 turns."},
        {"name": "Intimidating Shout", "cost": 10, "resource": "STR-SP", "type": "debuff",
         "level": 4, "debuff": "Weakened", "duration": 2,
         "desc": "Fierce war shout. Target deals 30% less damage for 2 turns."},
        {"name": "Battle Stance",    "cost": 8,  "resource": "STR-SP", "type": "buff",
         "level": 4, "buff": "battle_stance", "duration": 3, "self_only": True,
         "desc": "Adopt an aggressive stance. Your attacks deal 20% more damage for 3 turns."},
        {"name": "Cleave",           "cost": 12, "resource": "STR-SP", "type": "aoe",
         "level": 3, "power": 0.90, "target": "stack",
         "desc": "Broad swing through a group of identical enemies. Hits all enemies of the same type in the same row."},
        {"name": "Sweeping Strike",  "cost": 16, "resource": "STR-SP", "type": "aoe",
         "level": 6, "power": 0.85, "target": "front_row",
         "desc": "Wide horizontal swing hitting all front-row enemies for solid damage."},
        {"name": "Charge",           "cost": 14, "resource": "STR-SP", "type": "attack",
         "level": 7, "power": 1.6, "stun_chance": 0.25,
         "desc": "Crash into a target with full momentum. 25% chance to stun."},
        {"name": "Fortify",          "cost": 12, "resource": "STR-SP", "type": "buff",
         "level": 9, "buff": "fortify", "duration": 2, "self_only": True,
         "desc": "Brace for punishment. Incoming damage halved for 2 turns."},
        {"name": "Rallying Cry",     "cost": 22, "resource": "STR-SP", "type": "buff",
         "level": 9, "buff": "war_cry", "duration": 3, "targets": "all_allies",
         "desc": "Thunderous cry inspires the party. All allies deal bonus damage for 3 turns."},
        {"name": "Iron Will",        "cost": 0,  "resource": "",        "type": "passive",
         "level": 11, "passive": "iron_will",
         "desc": "Passive: You have 50% resistance to all status effects."},
    ],
    "Mage": [
        {"name": "Magic Missile",    "cost": 8,  "resource": "INT-MP", "type": "spell",
         "level": 1, "power": 1.0, "element": "arcane", "bonus_accuracy": 30, "desc": "Unerring arcane bolt. Very high hit chance."},
        {"name": "Arcane Shield",    "cost": 10, "resource": "INT-MP", "type": "buff",
         "level": 1, "buff": "magic_shield", "duration": 3, "self_only": True,
         "desc": "Erect a personal arcane barrier. Reduces all damage taken for 3 turns."},
        {"name": "Shock",            "cost": 9,  "resource": "INT-MP", "type": "spell",
         "level": 1, "power": 1.1, "element": "lightning", "stun_chance": 0.15,
         "desc": "Lightning strike. 15% chance to stun the target for 1 turn."},
        {"name": "Firebolt",         "cost": 10, "resource": "INT-MP", "type": "spell",
         "level": 2, "power": 1.3, "element": "fire", "dot": "burning", "dot_duration": 2,
         "desc": "Fire bolt that sets the target ablaze for 2 turns."},
        {"name": "Frostbolt",        "cost": 10, "resource": "INT-MP", "type": "spell",
         "level": 2, "power": 1.2, "element": "ice", "slow_chance": 0.50,
         "desc": "Ice bolt. 50% chance to slow target."},
        {"name": "Flame Spray",      "cost": 14, "resource": "INT-MP", "type": "aoe",
         "level": 3, "power": 0.95, "element": "fire", "target": "stack",
         "dot": "burning", "dot_duration": 2,
         "desc": "Cone of fire scorching a cluster of identical enemies. Sets each ablaze for 2 turns."},
        {"name": "Fireball",         "cost": 20, "resource": "INT-MP", "type": "aoe",
         "level": 4, "power": 1.4, "element": "fire", "target": "row",
         "dot": "burning", "dot_duration": 2,
         "desc": "Explosive fire blast hitting all enemies in a row. Applies Burn."},
        {"name": "Ice Lance",        "cost": 14, "resource": "INT-MP", "type": "spell",
         "level": 5, "power": 1.5, "element": "ice", "slow_chance": 0.40, "desc": "Piercing ice shard. 40% chance to slow."},
        {"name": "Deep Freeze",      "cost": 18, "resource": "INT-MP", "type": "spell",
         "level": 7, "power": 1.6, "element": "ice", "stun_chance": 0.35,
         "desc": "Freezes target solid. 35% chance to stun for 1 turn."},
        {"name": "Chain Lightning",  "cost": 25, "resource": "INT-MP", "type": "aoe",
         "level": 8, "power": 1.3, "element": "lightning", "desc": "Lightning arcing between all enemies."},
        {"name": "Meteor",           "cost": 40, "resource": "INT-MP", "type": "aoe",
         "level": 12, "power": 1.8, "element": "fire", "desc": "Apocalyptic fire from the sky."},
        # ─── Level-gap fill ───────────────────────────────────────────
        {"name": "Sleep",            "cost": 12, "resource": "INT-MP", "type": "spell",
         "level": 3, "power": 0, "element": "arcane",
         "status": "Sleep", "status_chance": 0.60, "status_duration": 2,
         "desc": "Arcane enchantment. 60% chance to put target to sleep for 2 turns. Breaks on damage."},
        {"name": "Arcane Surge",     "cost": 10, "resource": "INT-MP", "type": "buff",
         "level": 3, "buff": "arcane_surge", "duration": 2, "self_only": True,
         "desc": "Flood yourself with raw mana. Spell damage increased by 30% for 2 turns."},
        {"name": "Poison Mist",      "cost": 16, "resource": "INT-MP", "type": "aoe",
         "level": 6, "power": 0.5, "element": "nature",
         "apply_status": "Poisoned", "status_duration": 3, "status_chance": 0.55,
         "desc": "Toxic cloud drifts over all enemies. Low direct damage but 55% chance to poison each."},
        {"name": "Confuse",          "cost": 14, "resource": "INT-MP", "type": "debuff",
         "level": 6, "debuff": "Confused", "duration": 2,
         "desc": "Scramble a target's mind. Confused enemies attack random targets for 2 turns."},
        {"name": "Blizzard",         "cost": 28, "resource": "INT-MP", "type": "aoe",
         "level": 9, "power": 1.2, "element": "ice",
         "apply_status": "Slowed", "status_duration": 2, "status_chance": 0.70,
         "desc": "Howling ice storm hits all enemies. 70% chance to slow each for 2 turns."},
        {"name": "Mind Shatter",     "cost": 18, "resource": "INT-MP", "type": "spell",
         "level": 10, "power": 1.6, "element": "arcane", "stun_chance": 0.35,
         "desc": "Psyonic lance splinters concentration. 35% chance to stun for 1 turn."},
        {"name": "Arcane Nova",      "cost": 32, "resource": "INT-MP", "type": "aoe",
         "level": 11, "power": 1.6, "element": "arcane",
         "desc": "Explosive release of pure arcane force. Hits all enemies for heavy magic damage."},
    ],
    "Cleric": [
        {"name": "Heal",             "cost": 10, "resource": "PIE-MP", "type": "heal",
         "level": 1, "power": 1.0, "desc": "Restore HP to one ally."},
        {"name": "Smite",            "cost": 12, "resource": "PIE-MP", "type": "spell",
         "level": 1, "power": 1.4, "element": "divine", "desc": "Holy damage. Bonus vs undead."},
        {"name": "Bless",            "cost": 8,  "resource": "PIE-MP", "type": "buff",
         "level": 1, "buff": "blessed", "duration": 3, "targets": "ally",
         "desc": "Bless one ally. +10% accuracy and +10% to all saves for 3 turns."},
        {"name": "Cure Poison",      "cost": 8,  "resource": "PIE-MP", "type": "cure",
         "level": 3, "cures": "poison", "desc": "Remove poison from one ally."},
        {"name": "Prayer of Healing","cost": 20, "resource": "PIE-MP", "type": "aoe_heal",
         "level": 5, "power": 1.0, "desc": "Heal all allies for a moderate amount."},
        {"name": "Turn Undead",      "cost": 15, "resource": "PIE-MP", "type": "debuff",
         "level": 5, "targets": "undead", "fear_duration": 3, "desc": "Force undead to flee for 3 turns."},
        {"name": "Remove Curse",     "cost": 18, "resource": "PIE-MP", "type": "cure",
         "level": 7, "cures": "curse",
         "desc": "Lift a curse from one ally, freeing any cursed equipment they wear."},
        {"name": "Consecrate",       "cost": 16, "resource": "PIE-MP", "type": "aoe",
         "level": 4, "power": 1.0, "element": "divine", "target": "stack",
         "desc": "Channel holy energy into a cluster of enemies. Bonus damage vs undead and cursed. Hits all of the same type."},
        {"name": "Divine Wrath",     "cost": 30, "resource": "PIE-MP", "type": "aoe",
         "level": 10, "power": 1.8, "element": "divine", "desc": "Holy fire consumes all enemies."},
        # ─── Level-gap fill ───────────────────────────────────────────
        {"name": "Minor Heal",       "cost": 6,  "resource": "PIE-MP", "type": "heal",
         "level": 2, "power": 0.7,
         "desc": "Quick prayer that restores a modest amount of HP to one ally. Cheap and reliable."},
        {"name": "Shield of Faith",  "cost": 10, "resource": "PIE-MP", "type": "buff",
         "level": 2, "buff": "shield_of_faith", "duration": 3, "targets": "ally",
         "desc": "Wrap an ally in divine protection. Reduces all damage they take by 25% for 3 turns."},
        {"name": "Holy Aura",        "cost": 14, "resource": "PIE-MP", "type": "buff",
         "level": 4, "buff": "battle_prayer", "duration": 3, "targets": "all_allies",
         "desc": "Radiant aura surrounds the party. All allies regenerate a small amount of HP each turn for 3 turns."},
        {"name": "Purify",           "cost": 12, "resource": "PIE-MP", "type": "cure",
         "level": 4, "cures": "any",
         "desc": "Cleanse all negative status effects from one ally in a single cast."},
        {"name": "Revive",           "cost": 24, "resource": "PIE-MP", "type": "revive",
         "level": 6, "revive_hp_pct": 0.25,
         "desc": "Call a fallen ally back from unconsciousness. They return at 25% HP."},
        {"name": "Word of Courage",  "cost": 10, "resource": "PIE-MP", "type": "buff",
         "level": 6, "buff": "blessed", "duration": 4, "targets": "all_allies",
         "desc": "Spoken blessing bolsters the whole party. All allies gain +10% accuracy and saves for 4 turns."},
        {"name": "Group Bless",      "cost": 18, "resource": "PIE-MP", "type": "buff",
         "level": 8, "buff": "blessed", "duration": 5, "targets": "all_allies",
         "desc": "Powerful group blessing. Entire party gains +15% accuracy, +15% saves, +10% damage for 5 turns."},
        {"name": "Sanctuary",        "cost": 22, "resource": "PIE-MP", "type": "aoe_heal",
         "level": 8, "power": 0.8,
         "desc": "Sacred space envelops the party. Heals all allies and leaves a lingering regen effect."},
        {"name": "Mass Cure",        "cost": 20, "resource": "PIE-MP", "type": "cure",
         "level": 9, "cures": "any",
         "desc": "Purifying wave washes over the entire party, removing all negative status effects from everyone."},
        {"name": "Greater Heal",     "cost": 20, "resource": "PIE-MP", "type": "heal",
         "level": 11, "power": 1.8,
         "desc": "Potent channeled prayer. Restores a large amount of HP to one ally."},
        {"name": "Holy Storm",       "cost": 35, "resource": "PIE-MP", "type": "aoe",
         "level": 12, "power": 1.6, "element": "divine",
         "desc": "Pillar of holy light descends. Devastating divine damage to all enemies at once."},
        {"name": "Resurrection",     "cost": 40, "resource": "PIE-MP", "type": "revive",
         "level": 10, "revive_hp_pct": 0.5, "desc": "Revive a fallen ally at 50% HP."},
    ],
    "Thief": [
        {"name": "Quick Strike",     "cost": 8,  "resource": "DEX-SP", "type": "attack",
         "level": 1, "power": 1.3, "bonus_crit": 15, "desc": "Fast strike with +15% crit chance."},
        {"name": "Evade",            "cost": 6,  "resource": "DEX-SP", "type": "buff",
         "level": 1, "buff": "evasion", "duration": 2, "self_only": True, "desc": "Greatly increase dodge chance for 2 turns."},
        {"name": "Backstab",         "cost": 14, "resource": "DEX-SP", "type": "attack",
         "level": 3, "power": 2.0, "req_stealth": False, "bonus_crit": 25, "desc": "Vicious strike. +25% crit, huge damage on crit."},
        {"name": "Poison Blade",     "cost": 12, "resource": "DEX-SP", "type": "attack",
         "level": 5, "power": 1.2, "apply_poison": "poison_weak", "desc": "Envenomed strike. Applies Weak Poison."},
        {"name": "Smoke Bomb",       "cost": 16, "resource": "DEX-SP", "type": "buff",
         "level": 8, "buff": "smoke_screen", "duration": 2, "targets": "all_allies", "desc": "All allies gain evasion for 2 turns."},
        {"name": "Assassinate",      "cost": 30, "resource": "DEX-SP", "type": "attack",
         "level": 12, "power": 3.0, "bonus_crit": 30, "desc": "All-in lethal strike. Massive damage."},
        # ─── Level-gap fill ───────────────────────────────────────────
        {"name": "Pickpocket",       "cost": 6,  "resource": "DEX-SP", "type": "debuff",
         "level": 2, "debuff": "Weakened", "duration": 1,
         "desc": "Distract and fleece a target. Briefly disorients them (Weakened 1 turn) and may steal a small gold amount."},
        {"name": "Trick Shot",       "cost": 10, "resource": "DEX-SP", "type": "attack",
         "level": 2, "power": 1.1, "slow_chance": 0.40,
         "desc": "Cunning ranged strike. 40% chance to slow the target for 1 turn."},
        {"name": "Caltrops",         "cost": 12, "resource": "DEX-SP", "type": "aoe",
         "level": 4, "power": 0.3, "apply_status": "Slowed", "status_duration": 2, "status_chance": 0.80,
         "desc": "Scatter caltrops across the battlefield. All enemies have 80% chance to be slowed for 2 turns."},
        {"name": "Dirty Fighting",   "cost": 10, "resource": "DEX-SP", "type": "attack",
         "level": 4, "power": 1.2, "stun_chance": 0.25,
         "desc": "No-rules strike. Eye gouge, groin kick — 25% chance to stun."},
        {"name": "Garrote",          "cost": 16, "resource": "DEX-SP", "type": "attack",
         "level": 6, "power": 1.5, "apply_status": "Silenced", "status_duration": 2, "status_chance": 0.70,
         "desc": "Throttle a target. 70% chance to silence (block abilities) for 2 turns."},
        {"name": "Shadow Meld",      "cost": 14, "resource": "DEX-SP", "type": "buff",
         "level": 7, "buff": "evasion", "duration": 1, "self_only": True,
         "desc": "Melt into shadow. Your next action is guaranteed to crit if it connects."},
        {"name": "Fan of Knives",    "cost": 14, "resource": "DEX-SP", "type": "aoe",
         "level": 5, "power": 0.80, "target": "stack", "bonus_crit": 10,
         "desc": "Fling a spread of throwing knives at a tight cluster of enemies. Hits all of the same type."},
        {"name": "Venom Burst",      "cost": 20, "resource": "DEX-SP", "type": "aoe",
         "level": 9, "power": 0.6, "apply_status": "Poisoned", "status_duration": 3, "status_chance": 0.65,
         "desc": "Shatter a venom flask over all enemies. 65% chance to poison each for 3 turns."},
        {"name": "Hemorrhage",       "cost": 18, "resource": "DEX-SP", "type": "attack",
         "level": 11, "power": 1.4, "dot": "bleeding", "dot_duration": 3,
         "desc": "Deep slashing wound. Target bleeds for 3 turns, losing HP each turn."},
    ],
    "Ranger": [
        {"name": "Aimed Shot",       "cost": 10, "resource": "DEX-SP", "type": "attack",
         "level": 1, "power": 1.5, "bonus_accuracy": 20, "desc": "Carefully aimed ranged attack. +20% accuracy."},
        {"name": "Splitting Arrow",  "cost": 8,  "resource": "DEX-SP", "type": "attack",
         "level": 1, "power": 0.8, "pierce_rows": True, "desc": "Arrow pierces front row, hitting back row too. Reduced damage."},
        {"name": "Entangle",         "cost": 12, "resource": "WIS-MP", "type": "debuff",
         "level": 3, "element": "nature", "slow_duration": 2, "desc": "Roots slow a target for 2 turns."},
        {"name": "Barrage",          "cost": 18, "resource": "DEX-SP", "type": "aoe",
         "level": 5, "power": 1.0, "target": "row",
         "desc": "Concentrated volley at one row. Click any enemy in the target row. More damage than Volley."},
        {"name": "Nature's Balm",    "cost": 14, "resource": "WIS-MP", "type": "heal",
         "level": 5, "power": 1.0, "cures": "poison", "desc": "Herbal remedy. Heals and cures poison."},
        {"name": "Lethal Shot",      "cost": 25, "resource": "DEX-SP", "type": "attack",
         "level": 10, "power": 2.5, "bonus_accuracy": 30, "desc": "Perfect shot for massive damage."},
        # ─── Level-gap fill ───────────────────────────────────────────
        {"name": "Hunter's Mark",    "cost": 8,  "resource": "DEX-SP", "type": "debuff",
         "level": 2, "mark_duration": 3, "mark_type": "hunter_mark",
         "desc": "Mark a target. All party attacks against it deal +20% damage for 3 turns."},
        {"name": "Quick Nock",       "cost": 6,  "resource": "DEX-SP", "type": "attack",
         "level": 2, "power": 0.9, "bonus_accuracy": 15,
         "desc": "Rapid-fire arrow loosed without full aim. Fast, reliable, +15% accuracy."},
        {"name": "Scatter Shot",    "cost": 12, "resource": "DEX-SP", "type": "aoe",
         "level": 3, "power": 0.85, "target": "stack",
         "desc": "Arrow spread aimed at a tight cluster of identical enemies. Hits all of the same type in that row."},
        {"name": "Volley",           "cost": 14, "resource": "DEX-SP", "type": "aoe",
         "level": 4, "power": 0.75, "target": "row",
         "desc": "Rapid salvo aimed at one row. Click any enemy in the target row to fire. Lower damage than single shots."},
        {"name": "Snare Trap",       "cost": 10, "resource": "WIS-MP", "type": "debuff",
         "level": 4, "debuff": "Slowed", "duration": 3,
         "desc": "Set a foot snare. Target is rooted and slowed for 3 turns."},
        {"name": "Concussive Arrow", "cost": 14, "resource": "DEX-SP", "type": "attack",
         "level": 6, "power": 1.2, "stun_chance": 0.40,
         "desc": "Blunt-headed arrow aimed at the temple. 40% chance to stun for 1 turn."},
        {"name": "Tracking",         "cost": 10, "resource": "WIS-MP", "type": "buff",
         "level": 6, "buff": "keen_eye", "duration": 3, "self_only": True,
         "desc": "Read the battlefield. Gain +25% accuracy and +15% crit for 3 turns."},
        {"name": "Camouflage",       "cost": 12, "resource": "DEX-SP", "type": "buff",
         "level": 7, "buff": "evasion", "duration": 2, "self_only": True,
         "desc": "Blend into surroundings. Dodge chance greatly increased for 2 turns."},
        {"name": "Poison Arrow",     "cost": 12, "resource": "DEX-SP", "type": "attack",
         "level": 8, "power": 1.1, "apply_poison": "poison_weak",
         "desc": "Venomed broadhead. Deals damage and applies Weak Poison."},
        {"name": "Rain of Arrows",   "cost": 26, "resource": "DEX-SP", "type": "aoe",
         "level": 9, "power": 1.3,
         "desc": "Sustained arrow storm. Strongest AoE in the ranger arsenal — hits all enemies hard."},
        {"name": "Eagle Eye",        "cost": 0,  "resource": "",        "type": "passive",
         "level": 11, "passive": "eagle_eye",
         "desc": "Passive: All ranged attacks deal 20% more damage and can never miss on a natural 90+."},
        {"name": "Perfect Shot",     "cost": 30, "resource": "DEX-SP", "type": "attack",
         "level": 12, "power": 2.8, "bonus_accuracy": 50,
         "desc": "One shot, one kill. Enormous damage, near-perfect accuracy."},
    ],
    "Monk": [
        {"name": "Flurry of Blows",  "cost": 8,  "resource": "Ki", "type": "attack",
         "level": 1, "power": 0.6, "hits": 3, "desc": "Three rapid strikes at reduced power each."},
        {"name": "Iron Skin",        "cost": 10, "resource": "Ki", "type": "buff",
         "level": 1, "buff": "iron_skin", "duration": 3, "self_only": True,
         "desc": "Harden the body. Reduces physical damage taken for 3 turns (self only)."},
        {"name": "Stunning Fist",    "cost": 12, "resource": "Ki", "type": "attack",
         "level": 3, "power": 1.3, "stun_chance": 0.45, "desc": "Precise strike. 45% chance to stun."},
        {"name": "Inner Peace",      "cost": 15, "resource": "Ki", "type": "heal",
         "level": 5, "power": 1.2, "self_only": True, "desc": "Meditate to restore own HP."},
        {"name": "Pressure Point",   "cost": 18, "resource": "Ki", "type": "debuff",
         "level": 8, "weaken_duration": 3, "desc": "Strike nerve clusters. Target deals 30% less damage."},
        {"name": "Dragon Strike",    "cost": 30, "resource": "Ki", "type": "attack",
         "level": 12, "power": 2.8, "element": "fire", "desc": "Channel ki into a devastating fire strike."},
        # ─── Level-gap fill ───────────────────────────────────────────
        {"name": "Ki Pulse",         "cost": 10, "resource": "Ki", "type": "aoe",
         "level": 2, "power": 0.8, "element": "arcane", "target": "front_row",
         "desc": "Release a burst of ki energy. Hits all front-row enemies for arcane damage."},
        {"name": "Focused Breathing","cost": 8,  "resource": "Ki", "type": "heal",
         "level": 2, "power": 0.8, "self_only": True,
         "desc": "Meditate for one moment. Restore HP and a small amount of Ki."},
        {"name": "Focus Strike",     "cost": 12, "resource": "Ki", "type": "aoe",
         "level": 3, "power": 0.85, "target": "stack",
         "desc": "Focused ki discharge at a cluster of identical enemies. Hits all of the same type in that row."},
        {"name": "Whirlwind Kick",   "cost": 16, "resource": "Ki", "type": "aoe",
         "level": 4, "power": 0.9, "target": "front_row",
         "desc": "Spinning kick sweeping all front-row enemies. Solid AoE physical damage."},
        {"name": "Earth Strike",     "cost": 14, "resource": "Ki", "type": "attack",
         "level": 4, "power": 1.5, "slow_chance": 0.50,
         "desc": "Grounding palm strike. 50% chance to slow target for 2 turns."},
        {"name": "Ki Barrier",       "cost": 14, "resource": "Ki", "type": "buff",
         "level": 6, "buff": "ki_deflect", "duration": 2, "self_only": True,
         "desc": "Shape ki into a barrier. Absorbs the next physical attack directed at you."},
        {"name": "Nerve Strike",     "cost": 16, "resource": "Ki", "type": "debuff",
         "level": 7, "debuff": "Weakened", "duration": 3,
         "desc": "Precision strike on nerve clusters. Target deals 40% less damage for 3 turns."},
        {"name": "Thunderous Clap",  "cost": 20, "resource": "Ki", "type": "aoe",
         "level": 9, "power": 1.1, "stun_chance": 0.30,
         "desc": "Explosive ki shockwave hits all enemies. 30% chance to stun each."},
        {"name": "Void Fist",        "cost": 24, "resource": "Ki", "type": "attack",
         "level": 11, "power": 2.2, "element": "shadow",
         "desc": "Strike that bypasses physical defenses entirely. Pure ki resonance — ignores armor."},
    ],


    # ── Strider (Fighter+Ranger, L10) ────────────────────────────────────────
    "Strider": [
        {"name": "Skirmish",          "cost": 14, "resource": "DEX-SP", "type": "attack",
         "level": 10, "power": 0.9, "hits": 2,
         "desc": "Two rapid strikes at different enemies — split damage across two targets."},
        {"name": "Flanking Strike",   "cost": 16, "resource": "STR-SP", "type": "attack",
         "level": 10, "power": 1.8, "bonus_crit": 20,
         "desc": "Attack from the side. +20% crit. Bonus damage if an ally targets the same enemy."},
        {"name": "Rapid Advance",     "cost": 12, "resource": "DEX-SP", "type": "buff",
         "level": 11, "buff": "rapid_advance", "duration": 2, "self_only": True,
         "desc": "Sprint forward. For 2 turns ignore row penalties and gain +20% attack speed."},
        {"name": "Pinning Shot",      "cost": 14, "resource": "DEX-SP", "type": "attack",
         "level": 11, "power": 1.2, "apply_status": "Slowed", "status_duration": 3, "status_chance": 0.80,
         "desc": "Ranged strike that pins a target in place. 80% chance to slow for 3 turns."},
        {"name": "Blitz",             "cost": 28, "resource": "STR-SP", "type": "aoe",
         "level": 13, "power": 2.4, "bonus_crit": 10,
         "desc": "Explosive assault across the battlefield. Hits all enemies with crit chance; bonus damage to lowest-HP target."},
        {"name": "Whirlwind Strike",  "cost": 35, "resource": "STR-SP", "type": "aoe",
         "level": 15, "power": 2.8, "bonus_crit": 20,
         "desc": "Spinning blade storm at peak hybrid mastery. Hits all enemies with high crit chance — a Fighter-Ranger pinnacle."},
    ],

    # ── Guardian (Fighter+Monk, L10) ─────────────────────────────────────────
    "Guardian": [
        {"name": "Bastion Stance",    "cost": 14, "resource": "STR-SP", "type": "buff",
         "level": 10, "buff": "guardian_stance", "duration": 3, "self_only": True,
         "desc": "Plant your feet. Draw all enemy attacks to yourself and reduce incoming damage by 30%."},
        {"name": "Iron Guard",        "cost": 18, "resource": "STR-SP", "type": "buff",
         "level": 10, "buff": "iron_guard", "duration": 3, "targets": "all_allies",
         "desc": "Invoke ki discipline across the party. All allies reduce damage taken by 20% for 3 turns."},
        {"name": "Ki Shockwave",      "cost": 20, "resource": "Ki", "type": "aoe",
         "level": 11, "power": 2.6, "element": "arcane", "stun_chance": 0.35,
         "desc": "Release concentrated ki as a burst of force. Hits all enemies — 35% chance to stun each. Unique to the Fighter-Monk fusion."},
        {"name": "Intercept",         "cost": 10, "resource": "STR-SP", "type": "buff",
         "level": 12, "buff": "intercept", "duration": 1, "targets": "ally",
         "desc": "Step in front of an ally. Redirect the next attack aimed at them to yourself."},
        {"name": "Last Stand",        "cost": 25, "resource": "Ki", "type": "buff",
         "level": 13, "buff": "last_stand", "duration": 2, "self_only": True,
         "desc": "At 25% HP or below: gain massive damage and defense buff for 2 turns. Triggers automatically."},
        {"name": "Fortress",          "cost": 35, "resource": "STR-SP", "type": "buff",
         "level": 15, "buff": "fortress", "duration": 2, "targets": "all_allies",
         "desc": "Become an immovable bastion. Party cannot be moved, pushed, or instant-killed for 2 turns."},
    ],

    # ── Druid (Mage+Ranger, L10) ─────────────────────────────────────────────
    "Druid": [
        {"name": "Entangle",          "cost": 14, "resource": "WIS-MP", "type": "aoe",
         "level": 10, "power": 0.3, "element": "nature",
         "apply_status": "Slowed", "status_duration": 3, "status_chance": 0.85,
         "desc": "Roots erupt beneath all enemies. 85% chance to slow each for 3 turns."},
        {"name": "Rejuvenate",        "cost": 18, "resource": "WIS-MP", "type": "aoe_heal",
         "level": 10, "power": 0.6, "hot_duration": 3,
         "desc": "Herbal blessing on the whole party. Heals immediately and regenerates HP each turn for 3 turns."},
        {"name": "Stone Skin",        "cost": 16, "resource": "WIS-MP", "type": "buff",
         "level": 11, "buff": "stone_skin", "duration": 3, "targets": "all_allies",
         "desc": "Harden allies with earth magic. Party reduces physical damage taken by 25% for 3 turns."},
        {"name": "Slumber Spore",     "cost": 16, "resource": "WIS-MP", "type": "spell",
         "level": 11, "power": 0, "element": "nature",
         "target": "enemy_stack",
         "status": "Sleep", "status_chance": 0.65, "status_duration": 2,
         "desc": "Releases soporific spores that send a group of enemies into magical slumber. 65% chance per target."},
        {"name": "Lightning Storm",   "cost": 26, "resource": "INT-MP", "type": "aoe",
         "level": 12, "power": 2.2, "element": "lightning", "stun_chance": 0.35,
         "desc": "Call lightning that exceeds a Mage's control — nature-attuned channeling amplifies output. 35% stun per target."},
        {"name": "Wildshape",         "cost": 30, "resource": "WIS-MP", "type": "buff",
         "level": 13, "buff": "wildshape", "duration": 2, "self_only": True,
         "desc": "Transform into a beast form. Gain massive STR and HP bonus, lose spell access, for 2 turns."},
        {"name": "Nature's Wrath",    "cost": 40, "resource": "INT-MP", "type": "aoe",
         "level": 15, "power": 1.8, "element": "nature",
         "desc": "Summon nature's full fury. Massive nature damage to all enemies, bonus vs corrupted/shadow."},
    ],

    # ── Mystic (Mage+Monk, L10) ──────────────────────────────────────────────
    "Mystic": [
        {"name": "Force Pulse",       "cost": 16, "resource": "INT-MP", "type": "aoe",
         "level": 10, "power": 1.0, "element": "arcane",
         "desc": "Unleash pure arcane force. Hits all enemies — scales with INT, bypasses physical resistance."},
        {"name": "Ki Absorption",     "cost": 14, "resource": "Ki", "type": "buff",
         "level": 10, "buff": "ki_absorb", "duration": 1, "self_only": True,
         "desc": "Enter a receptive state. Next hit taken is absorbed and converted into MP."},
        {"name": "Arcane Palm",       "cost": 18, "resource": "INT-MP", "type": "attack",
         "level": 11, "power": 1.8, "element": "arcane",
         "apply_status": "Silenced", "status_duration": 2, "status_chance": 0.65,
         "desc": "Touch attack channeling pure arcane energy. 65% chance to silence the target for 2 turns."},
        {"name": "Lullaby",           "cost": 18, "resource": "INT-MP", "type": "spell",
         "level": 11, "power": 0, "element": "arcane",
         "target": "enemy_row",
         "status": "Sleep", "status_chance": 0.55, "status_duration": 2,
         "desc": "A haunting melody that lulls an entire row of enemies into deep sleep. 55% chance per target."},
        {"name": "Mindstrike",        "cost": 20, "resource": "INT-MP", "type": "attack",
         "level": 12, "power": 1.6, "element": "arcane", "targets_wis": True,
         "desc": "Attack targeting the mind, not the body. Damage scales vs target's WIS. Bonus vs spellcasters."},
        {"name": "Arcane Flurry",     "cost": 24, "resource": "INT-MP", "type": "attack",
         "level": 13, "power": 0.7, "hits": 4, "element": "arcane",
         "desc": "Four rapid arcane strikes at a single target. Each can trigger effects."},
        {"name": "Transcend",         "cost": 40, "resource": "Ki", "type": "buff",
         "level": 15, "buff": "transcendence", "duration": 1, "self_only": True,
         "desc": "Enter enlightened state for 1 turn. All abilities cost 0 and deal double damage."},
    ],

    # ── Inquisitor (Cleric+Thief, L10) ───────────────────────────────────────
    "Inquisitor": [
        {"name": "Expose Weakness",   "cost": 12, "resource": "WIS-MP", "type": "debuff",
         "level": 10, "debuff": "Exposed", "duration": 3,
         "desc": "Divine insight reveals all weaknesses. Target takes 25% more damage from all sources for 3 turns."},
        {"name": "Smite Shadow",      "cost": 16, "resource": "PIE-MP", "type": "attack",
         "level": 10, "power": 2.2, "element": "divine",
         "desc": "Holy-wreathed strike exceeding base Cleric output. Deals massive bonus damage to undead, shadow, and corrupted enemies."},
        {"name": "Sacred Snare",      "cost": 14, "resource": "PIE-MP", "type": "debuff",
         "level": 11, "debuff": "Slowed", "duration": 3, "element": "divine",
         "desc": "Holy binding holds a target in place, slowing them for 3 turns while dealing divine damage."},
        {"name": "Brand Heretic",     "cost": 18, "resource": "PIE-MP", "type": "debuff",
         "level": 12, "death_mark_duration": 4,
         "desc": "Brand a target as heretic. All party attacks deal +30% divine bonus damage to it for 4 turns."},
        {"name": "Shadow Smite",      "cost": 22, "resource": "DEX-SP", "type": "attack",
         "level": 13, "power": 2.2, "element": "divine", "bonus_crit": 25,
         "desc": "Strike from shadow wreathed in divine light. +25% crit, massive damage."},
        {"name": "Judgment Day",      "cost": 40, "resource": "PIE-MP", "type": "aoe",
         "level": 15, "power": 2.4, "element": "divine",
         "desc": "Holy reckoning at peak Inquisitor mastery — devastating divine AoE, maximum bonus vs undead and corrupted."},
    ],

    # ── Phantom (Thief+Monk, L10) ────────────────────────────────────────────
    "Phantom": [
        {"name": "Phase Strike",      "cost": 14, "resource": "DEX-SP", "type": "attack",
         "level": 10, "power": 1.6, "armor_pierce": True,
         "desc": "Ki-infused strike that phases through armor entirely. Ignores all physical defense."},
        {"name": "Shadow Clone",      "cost": 16, "resource": "Ki", "type": "buff",
         "level": 10, "buff": "shadow_clone", "duration": 1, "self_only": True,
         "desc": "Create a ki decoy. The next enemy attack automatically misses you."},
        {"name": "Ghost Step",        "cost": 12, "resource": "Ki", "type": "buff",
         "level": 11, "buff": "ghost_step", "duration": 2, "self_only": True,
         "desc": "Enter a half-real state. Automatically counter-attack the first enemy to strike you."},
        {"name": "Vanish",            "cost": 18, "resource": "DEX-SP", "type": "buff",
         "level": 12, "buff": "vanish", "duration": 1, "self_only": True,
         "desc": "Become invisible for 1 turn. Your next attack after re-appearing is a guaranteed critical hit."},
        {"name": "Void Touch",        "cost": 28, "resource": "Ki", "type": "attack",
         "level": 13, "power": 2.2, "element": "shadow",
         "desc": "Channel void energy through a touch. Massive shadow damage, reduces target's maximum HP."},
        {"name": "Wraith Form",       "cost": 35, "resource": "Ki", "type": "buff",
         "level": 15, "buff": "wraith_form", "duration": 2, "self_only": True,
         "desc": "Become partially incorporeal. For 2 turns all physical attacks pass through you harmlessly."},
    ],

    # ── Shaman (Ranger+Monk, L10) ────────────────────────────────────────────
    "Shaman": [
        {"name": "Spirit Bind",       "cost": 16, "resource": "WIS-MP", "type": "buff",
         "level": 10, "buff": "spirit_bond", "duration": 3, "targets": "all_allies",
         "desc": "Call nature spirits to aid the party. All allies gain +15% damage and regenerate HP each turn."},
        {"name": "Totemic Barrier",   "cost": 18, "resource": "WIS-MP", "type": "buff",
         "level": 10, "buff": "totem_ward", "duration": 3, "targets": "all_allies",
         "desc": "Erect a spirit ward. Party absorbs the first hit each round for 3 turns."},
        {"name": "Earth Pulse",       "cost": 20, "resource": "WIS-MP", "type": "aoe",
         "level": 11, "power": 1.8, "element": "nature", "apply_status": "Slowed",
         "status_duration": 2, "status_chance": 0.65,
         "desc": "Shockwave of earth energy stronger than any base Ranger or Monk can channel. Hits all enemies — 65% slow each."},
        {"name": "Ancestral Strike",  "cost": 24, "resource": "Ki", "type": "attack",
         "level": 12, "power": 3.4, "element": "nature", "armor_pierce": True,
         "desc": "Channel ancestor power through one devastating blow. Bypasses all armor and magical resistance — unique to the Ranger-Monk fusion."},
        {"name": "Spirit Cleanse",    "cost": 20, "resource": "WIS-MP", "type": "aoe_heal",
         "level": 13, "power": 0.7, "cures": "any",
         "desc": "Spirit energy washes over the party. Heals all allies and removes one status effect from each."},
        {"name": "Spirit Walk",       "cost": 40, "resource": "WIS-MP", "type": "buff",
         "level": 15, "buff": "spirit_walk", "duration": 1, "targets": "all_allies",
         "desc": "Party briefly enters the spirit world. All physical attacks pass through the party for 1 turn."},
    ],

    # ── Ascetic (Monk apex, L15) ─────────────────────────────────────────────
    "Ascetic": [
        {"name": "Perfect Defense",   "cost": 20, "resource": "Ki", "type": "buff",
         "level": 15, "buff": "perfect_defense", "duration": 1, "self_only": True,
         "desc": "Enter a state of perfect calm. Negate all damage from the next attack, regardless of source."},
        {"name": "Ki Burst",          "cost": 30, "resource": "Ki", "type": "aoe",
         "level": 15, "power": 1.6, "element": "arcane",
         "desc": "Release all stored ki at once. Massive arcane damage to all enemies — scales with WIS."},
        {"name": "Enlightened Strike","cost": 24, "resource": "Ki", "type": "attack",
         "level": 16, "power": 2.4, "armor_pierce": True, "element": "arcane",
         "desc": "A strike that bypasses all defenses, armor, and resistances. Pure ki resonance."},
        {"name": "Serenity",          "cost": 25, "resource": "Ki", "type": "aoe_heal",
         "level": 17, "power": 0.8, "cures": "any",
         "desc": "Perfect tranquility ripples through the party. Heals all allies and removes all status effects."},
        {"name": "Transcendence",     "cost": 50, "resource": "Ki", "type": "buff",
         "level": 20, "buff": "ascetic_transcendence", "duration": 2, "self_only": True,
         "desc": "Become invulnerable and deal double damage for 2 turns. The pinnacle of ki mastery."},
    ],

    # ── Beastlord (Ranger apex, L15) ─────────────────────────────────────────
    "Beastlord": [
        {"name": "Primal Roar",       "cost": 20, "resource": "DEX-SP", "type": "aoe",
         "level": 15, "power": 0.4, "element": "nature",
         "apply_status": "Weakened", "status_duration": 3, "status_chance": 0.80,
         "desc": "Terrifying primal roar. 80% chance to weaken all enemies for 3 turns (deal less damage)."},
        {"name": "Savage Rend",       "cost": 22, "resource": "DEX-SP", "type": "attack",
         "level": 15, "power": 2.0, "dot": "bleeding", "dot_duration": 4,
         "desc": "Animalistic rending attack. Massive physical damage with 4-turn bleed."},
        {"name": "Pack Tactics",      "cost": 18, "resource": "WIS-MP", "type": "buff",
         "level": 16, "buff": "pack_tactics", "duration": 3, "targets": "all_allies",
         "desc": "Inspire the party with predator instincts. All allies deal +20% damage and +10% crit for 3 turns."},
        {"name": "Nature's Fury",     "cost": 30, "resource": "WIS-MP", "type": "aoe",
         "level": 17, "power": 1.6, "element": "nature",
         "desc": "Summon primal nature's fury. Large nature AoE, bonus damage to shadow and corrupted."},
        {"name": "Apex Predator",     "cost": 40, "resource": "DEX-SP", "type": "attack",
         "level": 20, "power": 3.2, "execute_threshold": 0.30,
         "desc": "Final hunt. Instant kill if target below 30% HP. Otherwise deals enormous physical damage."},
    ],

    # ── Shadow Master (Thief apex, L15) ──────────────────────────────────────
    "Shadow Master": [
        {"name": "Thousand Cuts",     "cost": 24, "resource": "DEX-SP", "type": "aoe",
         "level": 15, "power": 0.7, "hits": 3, "dot": "bleeding", "dot_duration": 2,
         "desc": "A blur of blades hitting all enemies multiple times. Each hit applies 2-turn bleed."},
        {"name": "Soul Drain",        "cost": 20, "resource": "DEX-SP", "type": "attack",
         "level": 15, "power": 1.6, "element": "shadow", "lifesteal": 0.60,
         "desc": "Siphon life force from a target. 60% of damage dealt is restored as HP."},
        {"name": "Mark of Death",     "cost": 18, "resource": "DEX-SP", "type": "debuff",
         "level": 16, "death_mark_duration": 5,
         "desc": "Condemn a target. All party attacks deal +40% damage to it for 5 turns. Bonus crit chance."},
        {"name": "Shadow Nova",       "cost": 32, "resource": "DEX-SP", "type": "aoe",
         "level": 17, "power": 1.4, "element": "shadow",
         "desc": "Detonate a pocket of shadow energy. Massive AoE shadow damage to all enemies."},
        {"name": "Perfect Kill",      "cost": 45, "resource": "DEX-SP", "type": "attack",
         "level": 20, "power": 4.0, "bonus_crit": 40, "execute_threshold": 0.35,
         "desc": "The culmination of shadow mastery. Instant kill below 35% HP. Otherwise: catastrophic damage."},
    ],

    # ── Witch (Mage+Cleric, L10) ─────────────────────────────────────────────
    "Witch": [
        {"name": "Hex",               "cost": 16, "resource": "INT-MP", "type": "debuff",
         "level": 10, "debuff": "Hexed", "duration": 3,
         "desc": "Weave a dark curse. Target's STR, DEX, and INT are all reduced for 3 turns."},
        {"name": "Dark Bargain",      "cost": 0,  "resource": "INT-MP", "type": "buff",
         "level": 10, "buff": "dark_bargain", "duration": 3, "self_only": True,
         "desc": "Sacrifice 15% of max HP to fully restore MP. Also boost all spell power by 20% for 3 turns."},
        {"name": "Soul Siphon",       "cost": 18, "resource": "PIE-MP", "type": "attack",
         "level": 11, "power": 1.4, "element": "shadow", "lifesteal": 0.75,
         "desc": "Drain life force from target. 75% of damage dealt restores HP to self."},
        {"name": "Plague",            "cost": 22, "resource": "INT-MP", "type": "aoe",
         "level": 12, "power": 0.5, "element": "nature",
         "apply_status": "Poisoned", "status_duration": 4, "status_chance": 0.70,
         "desc": "Spread virulent disease across all enemies. 70% chance to poison each for 4 turns."},
        {"name": "Mass Sleep",        "cost": 22, "resource": "INT-MP", "type": "spell",
         "level": 12, "power": 0, "element": "shadow",
         "target": "all_enemies",
         "status": "Sleep", "status_chance": 0.40, "status_duration": 2,
         "desc": "A powerful hex that blankets all enemies in magical slumber simultaneously. 40% chance per target."},
        {"name": "Wither",            "cost": 28, "resource": "INT-MP", "type": "debuff",
         "level": 13, "debuff": "Withered", "duration": 4,
         "desc": "Inflict rapid physical decay. Target loses 40% attack, defense, and speed for 4 turns."},
        {"name": "Doom",              "cost": 40, "resource": "PIE-MP", "type": "attack",
         "level": 15, "power": 3.0, "element": "shadow", "execute_threshold": 0.40,
         "desc": "Weave a terminal curse. Instant kill below 40% HP. Otherwise: massive shadow damage."},
    ],

    # ── Necromancer (Mage+Thief, L10) ────────────────────────────────────────
    "Necromancer": [
        {"name": "Life Drain",        "cost": 16, "resource": "INT-MP", "type": "attack",
         "level": 10, "power": 1.3, "element": "shadow", "lifesteal": 0.80,
         "desc": "Drain life directly. 80% of damage dealt is restored as HP."},
        {"name": "Bone Cage",         "cost": 18, "resource": "INT-MP", "type": "debuff",
         "level": 10, "debuff": "Slowed", "duration": 3, "dot": "shadow_thorns", "dot_duration": 3,
         "desc": "Imprison target in spectral bone. Slowed for 3 turns and takes shadow damage each turn."},
        {"name": "Death Nova",        "cost": 24, "resource": "INT-MP", "type": "aoe",
         "level": 11, "power": 2.0, "element": "shadow",
         "desc": "Explosion of necrotic energy amplified by both arcane and shadow mastery. Hits all enemies for heavy shadow damage."},
        {"name": "Raise Fallen",      "cost": 28, "resource": "PIE-MP", "type": "revive",
         "level": 12, "revive_hp_pct": 0.30,
         "desc": "Temporarily animate a fallen ally as an undead — returns to fight at 30% HP for 2 turns."},
        {"name": "Lich Touch",        "cost": 30, "resource": "INT-MP", "type": "attack",
         "level": 13, "power": 2.2, "element": "shadow",
         "apply_status": "Cursed", "status_duration": 3, "status_chance": 0.90,
         "desc": "Necrotic touch. Massive shadow damage. 90% chance to curse — target cannot receive healing."},
        {"name": "Death Pact",        "cost": 0,  "resource": "INT-MP", "type": "buff",
         "level": 15, "buff": "death_pact", "duration": 3, "self_only": True,
         "desc": "Pact with death itself. If you fall in the next 3 turns, automatically revive at 50% HP once."},
    ],

    # ─── Hybrid Classes (unlock at level 8 via class transition) ───

    "Knight": [
        {"name": "Heavy Strike",      "cost": 12, "resource": "STR-SP", "type": "attack",
         "level": 1, "power": 1.7, "desc": "Powerful armored blow dealing heavy physical damage."},
        {"name": "Bulwark",           "cost": 10, "resource": "STR-SP", "type": "buff",
         "level": 1, "buff": "bulwark", "duration": 3, "self_only": True, "desc": "Full defensive stance — absorb the next attack for an ally."},
        {"name": "Challenge",         "cost": 8,  "resource": "STR-SP", "type": "taunt",
         "level": 3, "taunt_duration": 2, "desc": "Force an enemy to target you for 2 turns."},
        {"name": "Armor Crush",       "cost": 16, "resource": "STR-SP", "type": "attack",
         "level": 5, "power": 1.4, "armor_shred": 4, "desc": "Strike reduces enemy defense by 4 permanently."},
        {"name": "Rally",             "cost": 20, "resource": "STR-SP", "type": "buff",
         "level": 8, "buff": "rally", "duration": 3, "targets": "all_allies", "desc": "Inspire party — all allies deal bonus damage for 3 turns."},
        {"name": "Unbreakable",       "cost": 35, "resource": "STR-SP", "type": "buff",
         "level": 10, "buff": "unbreakable", "duration": 2, "self_only": True,
         "desc": "Become virtually invincible for 2 turns. Survive any hit with at least 1 HP."},
    ],
    "Warder": [
        {"name": "Holy Blade",        "cost": 14, "resource": "STR-SP", "type": "attack",
         "level": 8, "power": 1.6, "element": "divine", "desc": "Weapon infused with holy energy. Bonus vs corrupted."},
        {"name": "Lay on Hands",      "cost": 12, "resource": "PIE-MP", "type": "heal",
         "level": 8, "power": 1.5, "self_only": False, "desc": "Channel divine energy to restore an ally's HP."},
        {"name": "Warden's Mark",     "cost": 10, "resource": "PIE-MP", "type": "debuff",
         "level": 9, "mark_duration": 3, "desc": "Mark a target — all party attacks against it deal +20% damage."},
        {"name": "Consecrate",        "cost": 20, "resource": "PIE-MP", "type": "aoe",
         "level": 10, "power": 1.4, "element": "divine", "desc": "Holy fire damages all enemies. Bonus vs undead/shadow."},
        {"name": "Divine Shield",     "cost": 25, "resource": "PIE-MP", "type": "buff",
         "level": 12, "buff": "divine_shield", "duration": 2, "targets": "all_allies",
         "desc": "Surround all allies in divine light — reduce all incoming damage for 2 turns."},
    ],
    "Paladin": [
        {"name": "Crusader Strike",   "cost": 15, "resource": "STR-SP", "type": "attack",
         "level": 8, "power": 1.8, "element": "divine", "desc": "Holy-blessed melee attack. Extra damage vs undead."},
        {"name": "Remove Curse",       "cost": 18, "resource": "PIE-MP", "type": "cure",
         "level": 8, "cures": "curse",
         "desc": "Lay on hands to lift a curse from one ally, freeing any cursed equipment they wear."},
        {"name": "Aura of Courage",   "cost": 18, "resource": "PIE-MP", "type": "buff",
         "level": 8, "buff": "courage_aura", "duration": 4, "targets": "all_allies",
         "desc": "Holy aura — party immune to Fear and Confusion for 4 turns."},
        {"name": "Judgment",          "cost": 20, "resource": "PIE-MP", "type": "attack",
         "level": 9, "power": 2.2, "element": "divine",
         "desc": "Holy judgment on a singled-out enemy. Massive divine damage."},
        {"name": "Holy Nova",         "cost": 28, "resource": "PIE-MP", "type": "aoe",
         "level": 11, "power": 2.4, "element": "divine", "heal_power": 0.8,
         "desc": "Radiant explosion unique to the Fighter-Cleric fusion — damages all enemies AND heals all allies simultaneously."},
        {"name": "Resurrection",      "cost": 40, "resource": "PIE-MP", "type": "revive",
         "level": 13, "revive_hp_pct": 0.5, "desc": "Revive a fallen ally at 50% HP."},
    ],
    "Assassin": [
        {"name": "Shadow Step",       "cost": 12, "resource": "DEX-SP", "type": "buff",
         "level": 8, "buff": "shadow_step", "self_only": True, "desc": "Teleport behind a target — next attack is a guaranteed backstab."},
        {"name": "Crippling Strike",  "cost": 15, "resource": "DEX-SP", "type": "attack",
         "level": 8, "power": 1.5, "apply_slow": True, "slow_duration": 3,
         "desc": "Hamstring strike. Target speed reduced for 3 turns."},
        {"name": "Death Mark",        "cost": 16, "resource": "DEX-SP", "type": "debuff",
         "level": 9, "death_mark_duration": 3,
         "desc": "Mark for death — if target dies while marked, reset cooldowns."},
        {"name": "Fan of Knives",     "cost": 22, "resource": "DEX-SP", "type": "aoe",
         "level": 10, "power": 1.2, "desc": "Rain of blades hits all enemies. Each has 20% bleed chance."},
        {"name": "Throat Cut",        "cost": 35, "resource": "DEX-SP", "type": "attack",
         "level": 12, "power": 3.5, "silences": True, "silence_duration": 2,
         "desc": "Attempt to silence a target. Massive damage. Silenced targets can't use abilities."},
    ],
    "Warden": [
        {"name": "Spirit Bond",       "cost": 14, "resource": "WIS-MP", "type": "buff",
         "level": 8, "buff": "spirit_bond", "duration": 3, "targets": "all_allies",
         "desc": "Bond party spirits — all allies share 20% of healing received."},
        {"name": "Nature Strike",     "cost": 12, "resource": "DEX-SP", "type": "attack",
         "level": 8, "power": 1.5, "element": "nature",
         "desc": "Channel nature energy — deals bonus damage to corrupted/shadow enemies."},
        {"name": "Fading Ward",       "cost": 20, "resource": "PIE-MP", "type": "buff",
         "level": 9, "buff": "fading_ward", "duration": 3, "targets": "all_allies",
         "desc": "Ancient Warden ward — party gains resistance to Fading effects and shadow damage."},
        {"name": "Call of the Wild",  "cost": 18, "resource": "WIS-MP", "type": "aoe",
         "level": 10, "power": 1.8, "element": "nature", "heal_power": 0.6,
         "desc": "Summon nature's fury — deals nature damage to all enemies AND heals all allies. Dual function unique to the Cleric-Ranger fusion."},
        {"name": "Anchor the Wards",  "cost": 30, "resource": "PIE-MP", "type": "buff",
         "level": 12, "buff": "ward_anchor", "duration": 5, "targets": "all_allies",
         "desc": "Invoke old Warden magic. Party immune to status effects for 5 turns."},
    ],
    "Spellblade": [
        {"name": "Arcane Edge",       "cost": 14, "resource": "INT-MP", "type": "attack",
         "level": 8, "power": 1.8, "element": "arcane",
         "desc": "Imbue blade with arcane energy — magical melee strike ignores physical defense."},
        {"name": "Runic Armor",       "cost": 12, "resource": "INT-MP", "type": "buff",
         "level": 8, "buff": "runic_armor", "duration": 4, "self_only": True,
         "desc": "Inscribe runes on armor — reduces both physical and magical damage taken."},
        {"name": "Spellstrike",       "cost": 20, "resource": "INT-MP", "type": "attack",
         "level": 9, "power": 2.0, "element": "arcane", "combo_spell": True,
         "desc": "Deliver a spell through your weapon — melee hit triggers a bonus arcane explosion."},
        {"name": "Blade Barrier",     "cost": 22, "resource": "INT-MP", "type": "buff",
         "level": 10, "buff": "blade_barrier", "duration": 2, "reflect_pct": 0.25, "self_only": True,
         "desc": "Rotating blades of arcane force. Reflect 25% of incoming damage."},
        {"name": "Annihilate",        "cost": 40, "resource": "INT-MP", "type": "attack",
         "level": 12, "power": 3.2, "element": "arcane",
         "desc": "Total arcane destruction channeled through the blade. Ignores all defenses."},
    ],
    "Templar": [
        {"name": "Holy Wrath",        "cost": 16, "resource": "PIE-MP", "type": "attack",
         "level": 8, "power": 1.9, "element": "divine",
         "desc": "Armored charge infused with divine fire. Devastating to undead."},
        {"name": "Battle Prayer",     "cost": 14, "resource": "PIE-MP", "type": "buff",
         "level": 8, "buff": "battle_prayer", "duration": 3, "targets": "all_allies",
         "desc": "Short prayer before battle — all allies regenerate HP for 3 turns."},
        {"name": "Smite Evil",        "cost": 18, "resource": "PIE-MP", "type": "attack",
         "level": 9, "power": 2.4, "element": "divine", "bonus_vs_undead": 0.5,
         "desc": "Overwhelming holy force. 50% bonus damage vs undead and shadow-touched."},
        {"name": "Shield of Faith",   "cost": 20, "resource": "PIE-MP", "type": "buff",
         "level": 10, "buff": "shield_of_faith", "duration": 3, "targets": "all_allies",
         "desc": "Divine protection — reduce all incoming damage by 30% for 3 turns."},
        {"name": "Holy Avenger",      "cost": 35, "resource": "PIE-MP", "type": "attack",
         "level": 13, "power": 2.8, "element": "divine", "aoe_on_kill": True,
         "desc": "Empowered holy strike. On kill, triggers holy explosion hitting all enemies."},
    ],

    # ─── Advanced Classes (level 15+) ───

    "Champion": [
        {"name": "Titanfall",         "cost": 20, "resource": "STR-SP", "type": "attack",
         "level": 15, "power": 2.5, "stun_chance": 0.50, "desc": "Gravity-assisted leap strike. 50% stun."},
        {"name": "Last Stand",        "cost": 0, "resource": "STR-SP", "type": "passive",
         "level": 15, "passive": "last_stand", "desc": "Below 25% HP — deal double damage."},
        {"name": "Whirlwind",         "cost": 30, "resource": "STR-SP", "type": "aoe",
         "level": 16, "power": 1.8, "desc": "Spinning blade attack hitting every enemy."},
        {"name": "Blade Storm",       "cost": 45, "resource": "STR-SP", "type": "aoe",
         "level": 18, "power": 2.2, "hits": 2, "desc": "Unstoppable flurry — hits every enemy twice."},
        {"name": "Conqueror",         "cost": 50, "resource": "STR-SP", "type": "buff",
         "level": 20, "buff": "conqueror", "duration": 5, "self_only": True,
         "desc": "Legendary form — max damage on all attacks for 5 turns."},
    ],
    "Archmage": [
        {"name": "Spell Mastery",     "cost": 0, "resource": "",        "type": "passive",
         "level": 15, "passive": "spell_mastery", "desc": "All spells cost 25% less and deal 25% more damage."},
        {"name": "Time Stop",         "cost": 50, "resource": "INT-MP", "type": "buff",
         "level": 15, "buff": "time_stop", "duration": 1, "targets": "all_enemies",
         "desc": "Freeze time — all enemies skip their next turn."},
        {"name": "Arcane Torrent",    "cost": 35, "resource": "INT-MP", "type": "aoe",
         "level": 16, "power": 2.0, "element": "arcane", "desc": "Wave of pure arcane annihilation."},
        {"name": "Wish",              "cost": 80, "resource": "INT-MP", "type": "special",
         "level": 18, "desc": "Bend reality — fully heal the party, or deal maximum damage to all enemies."},
    ],
    "High Priest": [
        {"name": "Mass Resurrection", "cost": 60, "resource": "PIE-MP", "type": "revive",
         "level": 15, "revive_all": True, "revive_hp_pct": 0.30,
         "desc": "Revive all fallen allies at 30% HP."},
        {"name": "Divine Intervention","cost": 50, "resource": "PIE-MP", "type": "buff",
         "level": 15, "buff": "divine_intervention", "duration": 3, "targets": "all_allies",
         "desc": "Direct divine protection — party cannot die for 3 turns (survives any hit at 1 HP)."},
        {"name": "Holy Word",         "cost": 40, "resource": "PIE-MP", "type": "aoe",
         "level": 16, "power": 2.5, "element": "divine",
         "desc": "The word of light made manifest — devastating holy damage to all enemies."},
        {"name": "Miracle",           "cost": 70, "resource": "PIE-MP", "type": "special",
         "level": 18, "desc": "Divine miracle — fully restore all party HP and MP."},
    ],
}



# ═══════════════════════════════════════════════════════════════
#  ABILITY LEARNING
# ═══════════════════════════════════════════════════════════════

def get_available_abilities(class_name, current_level):
    """Get all abilities available at or below current level for a class."""
    abilities = CLASS_ABILITIES.get(class_name, [])
    return [a for a in abilities if a["level"] <= current_level]

def get_new_abilities_at_level(class_name, level):
    """Get abilities that unlock exactly at this level."""
    abilities = CLASS_ABILITIES.get(class_name, [])
    return [a for a in abilities if a["level"] == level]

def get_unlearned_abilities(character):
    """Get abilities the character qualifies for but hasn't learned yet."""
    available = get_available_abilities(character.class_name, character.level)
    known_names = {a["name"] for a in character.abilities}
    return [a for a in available if a["name"] not in known_names]

def learn_ability(character, ability_name):
    """Add an ability to a character's known abilities. Returns True if learned."""
    class_name = character.class_name
    available = CLASS_ABILITIES.get(class_name, [])
    for a in available:
        if a["name"] == ability_name and a["level"] <= character.level:
            # Check not already known
            if any(known["name"] == ability_name for known in character.abilities):
                return False
            character.abilities.append(dict(a))
            return True
    return False


# ═══════════════════════════════════════════════════════════════
#  ENEMY ABILITY DEFINITIONS
# ═══════════════════════════════════════════════════════════════

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
            {"name": "Shield Bash", "cost": 12, "resource": "STR-SP", "type": "attack",
             "level": 3, "power": 1.3, "stun_chance": 0.35,
             "desc": "Bash with your shield. 35% chance to stun the target.",
             "branch_label": "Defender",
             "branch_desc": "Master of defense and crowd control."},
            {"name": "Reckless Charge", "cost": 12, "resource": "STR-SP", "type": "attack",
             "level": 3, "power": 1.8, "self_damage_pct": 0.05,
             "desc": "Charge headlong into the enemy. Huge damage but you take 5% of your HP in recoil.",
             "branch_label": "Berserker",
             "branch_desc": "High risk, high reward aggression."},
        ],
        7: [
            {"name": "War Cry", "cost": 15, "resource": "STR-SP", "type": "buff",
             "level": 7, "buff": "war_cry", "duration": 3, "targets": "all_allies",
             "desc": "Rallying shout. All allies deal +25% damage for 3 turns.",
             "branch_label": "Commander",
             "branch_desc": "Inspire and lead your party to victory."},
            {"name": "Cleave", "cost": 18, "resource": "STR-SP", "type": "aoe",
             "level": 7, "power": 1.1,
             "desc": "Wide sweeping blow that hits all front-row enemies.",
             "branch_label": "Slayer",
             "branch_desc": "Mow through crowds with sweeping attacks."},
        ],
        10: [
            {"name": "Last Stand", "cost": 20, "resource": "STR-SP", "type": "buff",
             "level": 10, "buff": "last_stand", "duration": 3, "self_only": True,
             "desc": "When below 25% HP, enter a fury state: +50% damage and cannot be stunned.",
             "branch_label": "Warlord",
             "branch_desc": "Thrive in the chaos of near-death."},
            {"name": "Executioner", "cost": 25, "resource": "STR-SP", "type": "attack",
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
            {"name": "Backstab", "cost": 14, "resource": "DEX-SP", "type": "attack",
             "level": 3, "power": 2.0, "bonus_crit": 25,
             "desc": "Brutal strike from the shadows. Massive damage on crits.",
             "branch_label": "Assassin",
             "branch_desc": "Alpha-strike for massive single-target damage."},
            {"name": "Cripple", "cost": 10, "resource": "DEX-SP", "type": "debuff",
             "level": 3, "slow_duration": 3, "armor_shred": 2,
             "desc": "Slash tendons to slow and weaken a target for 3 turns.",
             "branch_label": "Saboteur",
             "branch_desc": "Disable and weaken before moving in for the kill."},
        ],
        7: [
            {"name": "Poison Blade", "cost": 12, "resource": "DEX-SP", "type": "attack",
             "level": 7, "power": 1.2, "apply_poison": "poison_strong",
             "desc": "Envenomed blade. Applies Strong Poison (10dmg/3 steps, 6 ticks).",
             "branch_label": "Venomancer",
             "branch_desc": "Stack poisons for sustained damage over time."},
            {"name": "Smoke Bomb", "cost": 16, "resource": "DEX-SP", "type": "buff",
             "level": 7, "buff": "smoke_screen", "duration": 2, "targets": "all_allies",
             "desc": "Obscuring smoke: all allies gain high evasion for 2 turns.",
             "branch_label": "Tactician",
             "branch_desc": "Control the battlefield and protect the party."},
        ],
        10: [
            {"name": "Death Mark", "cost": 22, "resource": "DEX-SP", "type": "debuff",
             "level": 10, "mark_duration": 4, "mark_crit_bonus": 30,
             "desc": "Mark a target for death. All attacks on it gain +30% crit chance.",
             "branch_label": "Shadowblade",
             "branch_desc": "Designate one target for total annihilation."},
            {"name": "Assassinate", "cost": 30, "resource": "DEX-SP", "type": "attack",
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
            {"name": "Twin Shot", "cost": 12, "resource": "DEX-SP", "type": "attack",
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
            {"name": "Barrage", "cost": 18, "resource": "DEX-SP", "type": "aoe",
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
            {"name": "Lethal Shot", "cost": 25, "resource": "DEX-SP", "type": "attack",
             "level": 10, "power": 2.5, "bonus_accuracy": 30,
             "desc": "A single, perfectly aimed shot for massive damage.",
             "branch_label": "Deadeye",
             "branch_desc": "One perfect shot, guaranteed to land."},
        ],
    },

    "Monk": {
        3: [
            {"name": "Stunning Fist", "cost": 12, "resource": "Ki", "type": "attack",
             "level": 3, "power": 1.3, "stun_chance": 0.45,
             "desc": "Precise nerve strike. 45% chance to stun.",
             "branch_label": "Striker",
             "branch_desc": "Disable foes with precision nerve attacks."},
            {"name": "Ki Deflect", "cost": 10, "resource": "Ki", "type": "buff",
             "level": 3, "buff": "ki_deflect", "duration": 2,
             "desc": "Channel Ki to deflect the next physical attack entirely.",
             "branch_label": "Guardian",
             "branch_desc": "Protect yourself and allies through Ki mastery."},
        ],
        7: [
            {"name": "Inner Peace", "cost": 15, "resource": "Ki", "type": "heal",
             "level": 7, "power": 1.2, "self_only": True,
             "desc": "Deep meditation restores own HP by a significant amount.",
             "branch_label": "Contemplative",
             "branch_desc": "Sustain yourself through spiritual fortitude."},
            {"name": "Pressure Point", "cost": 18, "resource": "Ki", "type": "debuff",
             "level": 7, "weaken_duration": 3,
             "desc": "Strike vital points. Target deals 30% less damage for 3 turns.",
             "branch_label": "Tactician",
             "branch_desc": "Weaken enemies through anatomical expertise."},
        ],
        10: [
            {"name": "Dragon Strike", "cost": 30, "resource": "Ki", "type": "attack",
             "level": 10, "power": 2.8, "element": "fire",
             "desc": "Channel pure Ki into a devastating flaming strike.",
             "branch_label": "Dragon Fist",
             "branch_desc": "Unleash elemental power through raw Ki."},
            {"name": "Empty Mind", "cost": 20, "resource": "Ki", "type": "buff",
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


