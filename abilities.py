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
        {"name": "Fireball",         "cost": 20, "resource": "INT-MP", "type": "aoe",
         "level": 4, "power": 1.4, "element": "fire", "target": "row",
         "desc": "Explosive fire blast hitting all enemies in a row."},
        {"name": "Ice Lance",        "cost": 14, "resource": "INT-MP", "type": "spell",
         "level": 5, "power": 1.5, "element": "ice", "slow_chance": 0.40, "desc": "Piercing ice shard. 40% chance to slow."},
        {"name": "Deep Freeze",      "cost": 18, "resource": "INT-MP", "type": "spell",
         "level": 7, "power": 1.6, "element": "ice", "stun_chance": 0.35,
         "desc": "Freezes target solid. 35% chance to stun for 1 turn."},
        {"name": "Chain Lightning",  "cost": 25, "resource": "INT-MP", "type": "aoe",
         "level": 8, "power": 1.3, "element": "lightning", "desc": "Lightning arcing between all enemies."},
        {"name": "Meteor",           "cost": 40, "resource": "INT-MP", "type": "aoe",
         "level": 12, "power": 1.8, "element": "fire", "desc": "Apocalyptic fire from the sky."},
    ],
    "Cleric": [
        {"name": "Heal",             "cost": 10, "resource": "PIE-MP", "type": "heal",
         "level": 1, "power": 1.0, "desc": "Restore HP to one ally."},
        {"name": "Smite",            "cost": 12, "resource": "PIE-MP", "type": "spell",
         "level": 1, "power": 1.4, "element": "divine", "desc": "Holy damage. Bonus vs undead."},
        {"name": "Bless",            "cost": 8,  "resource": "PIE-MP", "type": "buff",
         "level": 1, "buff": "blessed", "duration": 3, "target": "ally",
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
        {"name": "Divine Wrath",     "cost": 30, "resource": "PIE-MP", "type": "aoe",
         "level": 10, "power": 1.8, "element": "divine", "desc": "Holy fire consumes all enemies."},
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
    ],
    "Ranger": [
        {"name": "Aimed Shot",       "cost": 10, "resource": "DEX-SP", "type": "attack",
         "level": 1, "power": 1.5, "bonus_accuracy": 20, "desc": "Carefully aimed ranged attack. +20% accuracy."},
        {"name": "Splitting Arrow",  "cost": 8,  "resource": "DEX-SP", "type": "attack",
         "level": 1, "power": 0.8, "pierce_rows": True, "desc": "Arrow pierces front row, hitting back row too. Reduced damage."},
        {"name": "Entangle",         "cost": 12, "resource": "WIS-MP", "type": "debuff",
         "level": 3, "element": "nature", "slow_duration": 2, "desc": "Roots slow a target for 2 turns."},
        {"name": "Barrage",          "cost": 18, "resource": "DEX-SP", "type": "aoe",
         "level": 5, "power": 1.0, "desc": "Rapid volley of arrows at all enemies."},
        {"name": "Nature's Balm",    "cost": 14, "resource": "WIS-MP", "type": "heal",
         "level": 5, "power": 1.0, "cures": "poison", "desc": "Herbal remedy. Heals and cures poison."},
        {"name": "Lethal Shot",      "cost": 25, "resource": "DEX-SP", "type": "attack",
         "level": 10, "power": 2.5, "bonus_accuracy": 30, "desc": "Perfect shot for massive damage."},
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
         "level": 11, "power": 1.6, "element": "divine",
         "desc": "Radiant explosion. Damages all enemies, heals all allies."},
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
         "level": 10, "power": 1.3, "element": "nature",
         "desc": "Summon nature's fury. Deals nature damage to all enemies, heals all allies."},
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

    # ═══════════════════════════════════════════════════════════════
    #  HYBRID CLASSES (Level 10 Transition)
    # ═══════════════════════════════════════════════════════════════

    "Paladin": [
        {"name": "Holy Strike",       "cost": 12, "resource": "STR-SP", "type": "spell",
         "level": 1, "power": 1.5, "element": "divine",
         "desc": "Weapon strike infused with holy light. Bonus vs undead."},
        {"name": "Lay on Hands",      "cost": 0,  "resource": "STR-SP", "type": "heal",
         "level": 1, "power": 1.8, "self_only": False,
         "desc": "Channel divine energy to heal one ally. Free once per combat."},
        {"name": "Divine Shield",     "cost": 20, "resource": "STR-SP", "type": "buff",
         "level": 2, "buff": "divine_shield", "duration": 3, "self_only": True,
         "desc": "Sacred ward. Massively reduce damage taken for 3 turns."},
        {"name": "Smite Evil",        "cost": 18, "resource": "STR-SP", "type": "spell",
         "level": 4, "power": 2.0, "element": "divine",
         "desc": "Devastating holy blow. Triple damage vs undead and shadow."},
        {"name": "Consecrate",        "cost": 25, "resource": "STR-SP", "type": "aoe",
         "level": 7, "power": 1.2, "element": "divine",
         "desc": "Sanctify the battlefield. Holy damage to all enemies."},
        {"name": "Remove Curse",      "cost": 18, "resource": "STR-SP", "type": "cure",
         "level": 8, "cures": "curse",
         "desc": "Lay a holy hand on the afflicted. Remove any curse from one ally."},
        {"name": "Aura of Light",     "cost": 30, "resource": "STR-SP", "type": "buff",
         "level": 12, "buff": "blessed", "duration": 5, "targets": "all_allies",
         "desc": "Radiant aura blesses the entire party for 5 turns."},
    ],
    "Spellblade": [
        {"name": "Arcane Strike",     "cost": 12, "resource": "STR-SP", "type": "spell",
         "level": 1, "power": 1.4, "element": "arcane",
         "desc": "Weapon strike channeling raw arcane force. Bypasses physical defense."},
        {"name": "Blade Ward",        "cost": 10, "resource": "INT-MP", "type": "buff",
         "level": 1, "buff": "magic_shield", "duration": 3, "self_only": True,
         "desc": "Runic barrier absorbs spell damage for 3 turns."},
        {"name": "Flame Edge",        "cost": 15, "resource": "INT-MP", "type": "attack",
         "level": 3, "power": 1.6, "element": "fire", "dot": "burning", "dot_duration": 2,
         "desc": "Coat blade in fire. Physical strike plus burning DoT."},
        {"name": "Runic Armor",       "cost": 20, "resource": "INT-MP", "type": "buff",
         "level": 5, "buff": "runic_armor", "duration": 4, "self_only": True,
         "desc": "Inscribe runes on your armor. Massive defense for 4 turns."},
        {"name": "Spellsword Flurry", "cost": 30, "resource": "STR-SP", "type": "aoe",
         "level": 8, "power": 1.3, "element": "arcane",
         "desc": "Spinning arcane-blade attack hitting all front-row enemies."},
        {"name": "Null Blade",        "cost": 35, "resource": "INT-MP", "type": "attack",
         "level": 12, "power": 2.2, "element": "arcane",
         "desc": "Absolute arcane cut. Ignores all resistances and defenses."},
    ],
    "Warder": [
        {"name": "Crippling Strike",  "cost": 12, "resource": "STR-SP", "type": "attack",
         "level": 1, "power": 1.3, "weaken_duration": 2,
         "desc": "Precise strike weakens enemy. Target deals 30% less damage for 2 turns."},
        {"name": "Shadow Step",       "cost": 10, "resource": "DEX-SP", "type": "buff",
         "level": 1, "buff": "shadow_step", "duration": 2, "self_only": True,
         "desc": "Blend into shadows. +50% damage on next attack."},
        {"name": "Throat Cut",        "cost": 18, "resource": "DEX-SP", "type": "debuff",
         "level": 3, "slow_duration": 3,
         "desc": "Precise cut silences the target — prevents spellcasting for 3 turns."},
        {"name": "Ambush",            "cost": 20, "resource": "STR-SP", "type": "attack",
         "level": 6, "power": 2.0, "bonus_crit": 0.4,
         "desc": "Sudden brutal attack. +40% crit chance, massive damage on crit."},
        {"name": "Warden's Eye",      "cost": 15, "resource": "DEX-SP", "type": "buff",
         "level": 9, "buff": "hawk_eye", "duration": 4, "self_only": True,
         "desc": "Tactical awareness. +20% accuracy and damage for 4 turns."},
        {"name": "Execute",           "cost": 35, "resource": "STR-SP", "type": "attack",
         "level": 13, "power": 2.5, "execute_threshold": 0.30,
         "desc": "Instant kill if target below 30% HP. Massive damage otherwise."},
    ],
    "Strider": [
        {"name": "Skirmish Shot",     "cost": 10, "resource": "DEX-SP", "type": "attack",
         "level": 1, "power": 1.3, "bonus_accuracy": 0.15,
         "desc": "Quick shot during melee. High accuracy, hits any row."},
        {"name": "Hunter's Mark",     "cost": 12, "resource": "DEX-SP", "type": "debuff",
         "level": 1, "weaken_duration": 3,
         "desc": "Mark a target. All attacks against it deal 20% more damage."},
        {"name": "Flanking Strike",   "cost": 15, "resource": "STR-SP", "type": "attack",
         "level": 3, "power": 1.7,
         "desc": "Strike through front row to hit back row simultaneously."},
        {"name": "Rapid Fire",        "cost": 20, "resource": "DEX-SP", "type": "aoe",
         "level": 6, "power": 0.9,
         "desc": "Volley of arrows at all enemies. High total output."},
        {"name": "Wilderness Bond",   "cost": 18, "resource": "DEX-SP", "type": "heal",
         "level": 9, "power": 1.2, "cures": "poison",
         "desc": "Nature's resilience. Heal self and cure any poison effect."},
        {"name": "Death March",       "cost": 30, "resource": "STR-SP", "type": "attack",
         "level": 13, "power": 2.0, "hits": 3,
         "desc": "Three brutal strikes in sequence. Each at 200% weapon damage."},
    ],
    "Guardian": [
        {"name": "Iron Guard",        "cost": 10, "resource": "STR-SP", "type": "buff",
         "level": 1, "buff": "iron_skin", "duration": 3, "self_only": True,
         "desc": "Hardened body and shield. Massive damage reduction for 3 turns."},
        {"name": "Counter Strike",    "cost": 12, "resource": "STR-SP", "type": "attack",
         "level": 1, "power": 1.5,
         "desc": "Powerful riposte. Extra damage if defending last turn."},
        {"name": "Fortress Stance",   "cost": 18, "resource": "STR-SP", "type": "buff",
         "level": 3, "buff": "defense_up", "duration": 4, "targets": "all_allies",
         "desc": "Inspire allies to hold the line. Party defense +50% for 4 turns."},
        {"name": "Shockwave",         "cost": 22, "resource": "STR-SP", "type": "aoe",
         "level": 6, "power": 1.2, "stun_chance": 0.20,
         "desc": "Slam the ground. Hits all enemies. 20% stun chance each."},
        {"name": "Unbreakable",       "cost": 30, "resource": "STR-SP", "type": "buff",
         "level": 10, "buff": "unbreakable", "duration": 3, "self_only": True,
         "desc": "Cannot be killed for 3 turns. Survive at 1 HP if hit to zero."},
        {"name": "Titan's Grip",      "cost": 35, "resource": "STR-SP", "type": "attack",
         "level": 13, "power": 2.8, "stun_chance": 0.5,
         "desc": "Crushing two-handed blow. 50% stun chance. Devastating damage."},
    ],
    "Witch": [
        {"name": "Hex",               "cost": 12, "resource": "INT-MP", "type": "debuff",
         "level": 1, "weaken_duration": 3,
         "desc": "Cursed hex weakens target — deals 30% less damage for 3 turns."},
        {"name": "Life Drain",        "cost": 15, "resource": "INT-MP", "type": "spell",
         "level": 1, "power": 1.2, "element": "shadow", "life_drain": 0.5,
         "desc": "Drain life force. Damages enemy, heals caster for 50% of damage."},
        {"name": "Malison",           "cost": 18, "resource": "PIE-MP", "type": "aoe",
         "level": 3, "power": 0.9, "element": "shadow",
         "desc": "Wave of negative energy hits all enemies and saps their will."},
        {"name": "Soul Siphon",       "cost": 25, "resource": "INT-MP", "type": "spell",
         "level": 6, "power": 1.8, "element": "shadow",
         "desc": "Tear away a fragment of the target's soul. Massive shadow damage."},
        {"name": "Witch's Blessing",  "cost": 22, "resource": "PIE-MP", "type": "heal",
         "level": 9, "power": 1.5, "cures": "curse",
         "desc": "Twisted healing. Restores HP to one ally and lifts any curse."},
        {"name": "Death Coil",        "cost": 40, "resource": "INT-MP", "type": "aoe",
         "level": 13, "power": 1.6, "element": "shadow",
         "desc": "Spiral of death energy engulfs all enemies. Shadow damage to all."},
    ],
    "Necromancer": [
        {"name": "Bone Shard",        "cost": 10, "resource": "INT-MP", "type": "spell",
         "level": 1, "power": 1.3, "element": "shadow",
         "desc": "Splinter of conjured bone. High accuracy, medium shadow damage."},
        {"name": "Necrotic Touch",    "cost": 14, "resource": "INT-MP", "type": "debuff",
         "level": 1, "weaken_duration": 3,
         "desc": "Touch of death. Applies necrotic weakness — 30% less healing received."},
        {"name": "Dark Pact",         "cost": 20, "resource": "INT-MP", "type": "buff",
         "level": 3, "buff": "conqueror", "duration": 2, "self_only": True,
         "desc": "Bargain with shadow. Double damage next 2 turns, costs 10% HP."},
        {"name": "Wither",            "cost": 22, "resource": "INT-MP", "type": "aoe",
         "level": 6, "power": 1.0, "element": "shadow",
         "desc": "Wave of withering shadow. Damages all and reduces their speed."},
        {"name": "Soul Rend",         "cost": 35, "resource": "INT-MP", "type": "spell",
         "level": 10, "power": 2.2, "element": "shadow",
         "desc": "Rend the target's soul. Huge shadow damage, paralyze chance."},
        {"name": "Lich Touch",        "cost": 45, "resource": "INT-MP", "type": "spell",
         "level": 13, "power": 2.5, "element": "shadow",
         "desc": "The cold of undeath. Stun chance if target survives."},
    ],
    "Druid": [
        {"name": "Thorn Whip",        "cost": 10, "resource": "WIS-MP", "type": "spell",
         "level": 1, "power": 1.2, "element": "nature",
         "desc": "Lash of thorns. Pulls target to front row."},
        {"name": "Regrowth",          "cost": 14, "resource": "WIS-MP", "type": "heal",
         "level": 1, "power": 1.3, "cures": "poison",
         "desc": "Nature's renewal. Heal one ally and remove poison."},
        {"name": "Entangle",          "cost": 16, "resource": "WIS-MP", "type": "debuff",
         "level": 3, "slow_duration": 3, "element": "nature",
         "desc": "Roots slow target for 3 turns."},
        {"name": "Wild Growth",       "cost": 22, "resource": "WIS-MP", "type": "aoe_heal",
         "level": 6, "power": 1.1,
         "desc": "Surge of nature heals the entire party."},
        {"name": "Barkskin",          "cost": 20, "resource": "WIS-MP", "type": "buff",
         "level": 9, "buff": "iron_skin", "duration": 4, "targets": "all_allies",
         "desc": "Harden ally skin like bark. Party defense +40% for 4 turns."},
        {"name": "Wrath of Nature",   "cost": 40, "resource": "WIS-MP", "type": "aoe",
         "level": 13, "power": 1.8, "element": "nature",
         "desc": "Nature itself strikes. Massive nature damage to all enemies."},
    ],
    "Mystic": [
        {"name": "Ki Blast",          "cost": 10, "resource": "INT-MP", "type": "spell",
         "level": 1, "power": 1.4, "element": "arcane",
         "desc": "Focused ki as pure arcane force. Unerring accuracy."},
        {"name": "Mind Shield",       "cost": 12, "resource": "INT-MP", "type": "buff",
         "level": 1, "buff": "arcane_shield", "duration": 3, "self_only": True,
         "desc": "Psychic barrier. Reduces all damage for 3 turns."},
        {"name": "Thought Strike",    "cost": 16, "resource": "INT-MP", "type": "attack",
         "level": 3, "power": 1.6, "stun_chance": 0.30,
         "desc": "Mental force through a physical strike. 30% stun chance."},
        {"name": "Void Palm",         "cost": 22, "resource": "INT-MP", "type": "spell",
         "level": 6, "power": 1.9, "element": "arcane",
         "desc": "Strike the enemy's essence directly. Ignores magic resist."},
        {"name": "Meditative Surge",  "cost": 25, "resource": "INT-MP", "type": "aoe_heal",
         "level": 9, "power": 1.0,
         "desc": "Broadcast inner peace. Moderate party heal, removes Slowed."},
        {"name": "Psychic Storm",     "cost": 42, "resource": "INT-MP", "type": "aoe",
         "level": 13, "power": 1.7, "element": "arcane",
         "desc": "Mental detonation. Arcane damage to all, stun chance each."},
    ],
    "Warden": [
        {"name": "Ward Arrow",        "cost": 12, "resource": "PIE-MP", "type": "spell",
         "level": 1, "power": 1.3, "element": "divine",
         "desc": "Arrow blessed with divine light. Bonus vs shadow enemies."},
        {"name": "Nature's Grace",    "cost": 14, "resource": "WIS-MP", "type": "heal",
         "level": 1, "power": 1.4, "cures": "poison",
         "desc": "Channel nature and the divine. Heal and cleanse poison."},
        {"name": "Binding Roots",     "cost": 16, "resource": "WIS-MP", "type": "debuff",
         "level": 3, "slow_duration": 3, "element": "nature",
         "desc": "Divine roots hold the target in place for 3 turns."},
        {"name": "Warden's Weal",     "cost": 22, "resource": "PIE-MP", "type": "aoe_heal",
         "level": 6, "power": 1.2,
         "desc": "Ancient healing rite. Heal all allies significantly."},
        {"name": "Fading Ward",       "cost": 28, "resource": "PIE-MP", "type": "buff",
         "level": 9, "buff": "fading_ward", "duration": 4, "targets": "all_allies",
         "desc": "Old Warden magic. Party resists Fading energy for 4 turns."},
        {"name": "Hearthstone Pulse", "cost": 40, "resource": "PIE-MP", "type": "aoe",
         "level": 13, "power": 1.8, "element": "divine",
         "desc": "Channel a Hearthstone's energy. Divine damage to all shadow enemies."},
    ],
    "Inquisitor": [
        {"name": "Judgment",          "cost": 14, "resource": "PIE-MP", "type": "attack",
         "level": 1, "power": 1.5, "bonus_crit": 0.20,
         "desc": "Swift divine strike. +20% critical hit chance."},
        {"name": "Expose Weakness",   "cost": 12, "resource": "DEX-SP", "type": "debuff",
         "level": 1, "weaken_duration": 3,
         "desc": "Find and target the flaw. Enemy defense reduced 50% for 3 turns."},
        {"name": "Righteous Fury",    "cost": 18, "resource": "PIE-MP", "type": "buff",
         "level": 3, "buff": "war_cry", "duration": 3, "self_only": True,
         "desc": "Divine wrath fills you. Deal +25% damage for 3 turns."},
        {"name": "Confess",           "cost": 22, "resource": "PIE-MP", "type": "debuff",
         "level": 6, "weaken_duration": 4,
         "desc": "Break the enemy's will. They deal 40% less damage for 4 turns."},
        {"name": "Seal of Fate",      "cost": 30, "resource": "PIE-MP", "type": "attack",
         "level": 9, "power": 2.0, "execute_threshold": 0.25,
         "desc": "Divine sentence. Instant kill below 25% HP. Massive damage otherwise."},
        {"name": "Inquisition",       "cost": 40, "resource": "PIE-MP", "type": "aoe",
         "level": 13, "power": 1.4, "element": "divine",
         "desc": "Holy reckoning sweeps all enemies. Divine damage to all."},
    ],
    "Templar": [
        {"name": "Sacred Fist",       "cost": 12, "resource": "PIE-MP", "type": "spell",
         "level": 1, "power": 1.4, "element": "divine",
         "desc": "Unarmed strike channeling divine energy. Bonus vs undead."},
        {"name": "Monastic Healing",  "cost": 14, "resource": "PIE-MP", "type": "heal",
         "level": 1, "power": 1.5,
         "desc": "Focused divine and ki together. Heal one ally significantly."},
        {"name": "Templar's Vow",     "cost": 18, "resource": "PIE-MP", "type": "buff",
         "level": 3, "buff": "divine_shield", "duration": 2, "targets": "all_allies",
         "desc": "Sacred oath. Brief but powerful protection for the whole party."},
        {"name": "Purifying Strike",  "cost": 22, "resource": "PIE-MP", "type": "attack",
         "level": 6, "power": 1.8, "element": "divine",
         "desc": "Strike that purifies. Removes one buff from target."},
        {"name": "Battle Prayer",     "cost": 25, "resource": "PIE-MP", "type": "buff",
         "level": 9, "buff": "blessed", "duration": 5, "targets": "all_allies",
         "desc": "Ancient war prayer. Party accuracy and defense improved for 5 turns."},
        {"name": "Divine Retribution","cost": 40, "resource": "PIE-MP", "type": "aoe",
         "level": 13, "power": 1.9, "element": "divine",
         "desc": "The temple's justice falls on all enemies simultaneously."},
    ],
    "Assassin": [
        {"name": "Marked for Death",  "cost": 10, "resource": "DEX-SP", "type": "debuff",
         "level": 1, "weaken_duration": 3,
         "desc": "Mark the target. All party attacks against it deal +25% damage."},
        {"name": "Venom Shot",        "cost": 14, "resource": "DEX-SP", "type": "attack",
         "level": 1, "power": 1.2, "apply_poison": "poison_strong",
         "desc": "Envenomed shot. Applies Strong Poison DoT."},
        {"name": "Shadow Meld",       "cost": 16, "resource": "DEX-SP", "type": "buff",
         "level": 3, "buff": "evasion", "duration": 3, "self_only": True,
         "desc": "Vanish into shadow. 45% dodge chance for 3 turns."},
        {"name": "Death from Above",  "cost": 25, "resource": "DEX-SP", "type": "attack",
         "level": 6, "power": 2.2, "bonus_crit": 0.35,
         "desc": "Aerial archery with blade work. Massive damage, +35% crit."},
        {"name": "Smoke and Daggers", "cost": 22, "resource": "DEX-SP", "type": "buff",
         "level": 9, "buff": "smoke_screen", "duration": 3, "targets": "all_allies",
         "desc": "Smoke bomb covers retreat. Party evasion +45% for 3 turns."},
        {"name": "Perfect Kill",      "cost": 45, "resource": "DEX-SP", "type": "attack",
         "level": 13, "power": 3.0, "bonus_crit": 0.50,
         "desc": "The perfect assassination. 50% crit, catastrophic damage."},
    ],
    "Phantom": [
        {"name": "Ghost Strike",      "cost": 12, "resource": "DEX-SP", "type": "attack",
         "level": 1, "power": 1.4, "bonus_crit": 0.20,
         "desc": "Strike passes through defenses. Ignores 40% of target defense."},
        {"name": "Blur",              "cost": 12, "resource": "DEX-SP", "type": "buff",
         "level": 1, "buff": "evasion", "duration": 2, "self_only": True,
         "desc": "Blur your form. 45% dodge chance for 2 turns."},
        {"name": "Nerve Strike",      "cost": 16, "resource": "DEX-SP", "type": "attack",
         "level": 3, "power": 1.3, "stun_chance": 0.40,
         "desc": "Strike nerve clusters. 40% chance to stun."},
        {"name": "Phase Step",        "cost": 20, "resource": "DEX-SP", "type": "buff",
         "level": 6, "buff": "shadow_step", "duration": 2, "self_only": True,
         "desc": "Briefly phase out of reality. Next attack +60% damage."},
        {"name": "Soul Strike",       "cost": 28, "resource": "DEX-SP", "type": "spell",
         "level": 9, "power": 1.8, "element": "shadow",
         "desc": "Strike at the enemy's shadow-self. Shadow damage, bypasses armor."},
        {"name": "Void Rush",         "cost": 40, "resource": "DEX-SP", "type": "aoe",
         "level": 13, "power": 1.5,
         "desc": "Dash through all enemies in sequence. Hit every enemy once."},
    ],
    "Shaman": [
        {"name": "Spirit Arrow",      "cost": 12, "resource": "WIS-MP", "type": "spell",
         "level": 1, "power": 1.3, "element": "nature",
         "desc": "Arrow guided by spirits. Cannot miss."},
        {"name": "Spirit Mend",       "cost": 14, "resource": "WIS-MP", "type": "heal",
         "level": 1, "power": 1.4,
         "desc": "Call on ancestral spirits to heal one ally."},
        {"name": "Earth Shaker",      "cost": 18, "resource": "WIS-MP", "type": "aoe",
         "level": 3, "power": 1.1, "element": "nature",
         "desc": "Channel earth energy. Hits all grounded enemies."},
        {"name": "Spirit Bond",       "cost": 22, "resource": "WIS-MP", "type": "buff",
         "level": 6, "buff": "spirit_bond", "duration": 4, "targets": "all_allies",
         "desc": "Link the party through spirits. Shared defense, +20% resistances."},
        {"name": "Ancestral Wrath",   "cost": 30, "resource": "WIS-MP", "type": "spell",
         "level": 9, "power": 2.0, "element": "nature",
         "desc": "Ancestors channel through you. Nature damage, stun chance."},
        {"name": "Totem of Warding",  "cost": 35, "resource": "WIS-MP", "type": "buff",
         "level": 13, "buff": "ward_anchor", "duration": 5, "targets": "all_allies",
         "desc": "Plant a spiritual ward. Party resists all damage types for 5 turns."},
    ],

    # ═══════════════════════════════════════════════════════════════
    #  APEX CLASSES (Level 15 Transition)
    # ═══════════════════════════════════════════════════════════════

    "Knight": [
        {"name": "Champion's Blow",   "cost": 20, "resource": "STR-SP", "type": "attack",
         "level": 1, "power": 2.0,
         "desc": "The perfected strike of a master warrior. Overwhelming damage."},
        {"name": "Iron Will",         "cost": 0,  "resource": "STR-SP", "type": "buff",
         "level": 1, "buff": "unbreakable", "duration": 2, "self_only": True,
         "desc": "Absolute resolve. Cannot be killed for 2 turns. Costs no SP."},
        {"name": "Rally the Line",    "cost": 25, "resource": "STR-SP", "type": "buff",
         "level": 2, "buff": "war_cry", "duration": 4, "targets": "all_allies",
         "desc": "War cry rallies every ally. +25% damage for 4 turns."},
        {"name": "Knight's Wrath",    "cost": 35, "resource": "STR-SP", "type": "aoe",
         "level": 5, "power": 1.5,
         "desc": "Sweeping blade technique hits all enemies with full force."},
        {"name": "Last Stand",        "cost": 40, "resource": "STR-SP", "type": "buff",
         "level": 10, "buff": "last_stand", "duration": 5, "self_only": True,
         "desc": "Triple damage and defense below 25% HP for 5 turns."},
        {"name": "Conqueror",         "cost": 50, "resource": "STR-SP", "type": "buff",
         "level": 15, "buff": "conqueror", "duration": 3, "self_only": True,
         "desc": "Ultimate warrior state. Double damage for 3 turns."},
    ],
    "Archmage": [
        {"name": "Arcane Mastery",    "cost": 20, "resource": "INT-MP", "type": "buff",
         "level": 1, "buff": "arcane_shield", "duration": 5, "self_only": True,
         "desc": "True arcane mastery. Absolute damage reduction for 5 turns."},
        {"name": "Chain Spell",       "cost": 30, "resource": "INT-MP", "type": "aoe",
         "level": 2, "power": 1.5, "element": "arcane",
         "desc": "Spell bounces between all enemies for full damage each hit."},
        {"name": "Arcane Surge",      "cost": 0,  "resource": "INT-MP", "type": "buff",
         "level": 5, "buff": "conqueror", "duration": 2, "self_only": True,
         "desc": "Tap limitless power. Double spell damage for 2 turns. Free."},
        {"name": "Reality Fracture",  "cost": 50, "resource": "INT-MP", "type": "aoe",
         "level": 10, "power": 2.0, "element": "arcane",
         "desc": "Tear reality itself. Arcane damage to all — ignores all resistances."},
        {"name": "Time Warp",         "cost": 60, "resource": "INT-MP", "type": "buff",
         "level": 15, "buff": "empty_mind", "duration": 1, "targets": "all_allies",
         "desc": "Compress time. Party acts twice this round."},
    ],
    "High Priest": [
        {"name": "Turn Undead",       "cost": 15, "resource": "PIE-MP", "type": "debuff",
         "level": 1, "targets": "undead",
         "desc": "Channel divine power to terrify and weaken all undead enemies."},
        {"name": "Divine Intervention","cost": 0, "resource": "PIE-MP", "type": "buff",
         "level": 1, "buff": "divine_shield", "duration": 3, "targets": "all_allies",
         "desc": "Call on the divine. Party cannot be killed for 3 turns. Free once."},
        {"name": "Mass Resurrection", "cost": 50, "resource": "PIE-MP", "type": "revive",
         "level": 2, "revive_hp_pct": 0.5, "targets": "all_dead_allies",
         "desc": "Raise all fallen allies simultaneously at 50% HP."},
        {"name": "Holy Nova",         "cost": 35, "resource": "PIE-MP", "type": "aoe",
         "level": 5, "power": 1.8, "element": "divine",
         "desc": "Burst of pure holy energy. Massive divine damage to all enemies."},
        {"name": "Greater Heal",      "cost": 30, "resource": "PIE-MP", "type": "heal",
         "level": 8, "power": 3.0,
         "desc": "The greatest healing miracle. Fully restore one ally's HP."},
        {"name": "Sanctuary",         "cost": 40, "resource": "PIE-MP", "type": "buff",
         "level": 15, "buff": "divine_shield", "duration": 5, "targets": "all_allies",
         "desc": "Sacred sanctuary. The whole party takes 70% less damage for 5 turns."},
    ],
    "Shadow Master": [
        {"name": "Shadow Fade",       "cost": 15, "resource": "DEX-SP", "type": "buff",
         "level": 1, "buff": "evasion", "duration": 4, "self_only": True,
         "desc": "True invisibility. 70% dodge for 4 turns."},
        {"name": "Death Mark",        "cost": 25, "resource": "DEX-SP", "type": "debuff",
         "level": 2, "weaken_duration": 5,
         "desc": "Mark for death. All attacks deal +50% damage for 5 turns."},
        {"name": "Shadow Clone",      "cost": 30, "resource": "DEX-SP", "type": "buff",
         "level": 5, "buff": "hawk_eye", "duration": 3, "self_only": True,
         "desc": "Split into shadow copies. +30% accuracy and +30% damage for 3 turns."},
        {"name": "Thousand Cuts",     "cost": 40, "resource": "DEX-SP", "type": "attack",
         "level": 10, "power": 1.0, "hits": 5,
         "desc": "Five rapid strikes at full weapon damage each."},
        {"name": "Oblivion Strike",   "cost": 55, "resource": "DEX-SP", "type": "attack",
         "level": 15, "power": 4.0, "bonus_crit": 0.50,
         "desc": "The perfect assassination. 50% crit, catastrophic damage."},
    ],
    "Beastlord": [
        {"name": "Pack Tactics",      "cost": 20, "resource": "DEX-SP", "type": "buff",
         "level": 1, "buff": "hawk_eye", "duration": 4, "targets": "all_allies",
         "desc": "Coordinate the hunt. All allies +20% accuracy and +20% damage."},
        {"name": "Primal Fury",       "cost": 25, "resource": "DEX-SP", "type": "attack",
         "level": 2, "power": 2.5, "hits": 2,
         "desc": "Primal instinct. Two strikes at 250% weapon damage each."},
        {"name": "Aspect of the Beast","cost": 30, "resource": "WIS-MP", "type": "buff",
         "level": 5, "buff": "war_cry", "duration": 4, "self_only": True,
         "desc": "Channel the beast within. +25% damage, +25% speed for 4 turns."},
        {"name": "Nature's Fury",     "cost": 40, "resource": "WIS-MP", "type": "aoe",
         "level": 10, "power": 1.8, "element": "nature",
         "desc": "Unleash wild nature on all enemies. Full nature damage to all."},
        {"name": "King of the Wild",  "cost": 50, "resource": "WIS-MP", "type": "buff",
         "level": 15, "buff": "conqueror", "duration": 4, "targets": "all_allies",
         "desc": "The apex of natural power. Party deals double damage for 4 turns."},
    ],
    "Ascetic": [
        {"name": "Perfect Form",      "cost": 0,  "resource": "Ki", "type": "buff",
         "level": 1, "buff": "iron_skin", "duration": 5, "self_only": True,
         "desc": "Absolute physical perfection. Massive damage reduction. Free."},
        {"name": "Death Touch",       "cost": 30, "resource": "Ki", "type": "attack",
         "level": 2, "power": 2.5, "stun_chance": 0.60,
         "desc": "Ancient forbidden technique. 60% stun chance. Enormous damage."},
        {"name": "Transcend",         "cost": 25, "resource": "Ki", "type": "buff",
         "level": 5, "buff": "empty_mind", "duration": 3, "self_only": True,
         "desc": "Step beyond mortal limits. Immune to status, acts first for 3 turns."},
        {"name": "Thousand Palms",    "cost": 45, "resource": "Ki", "type": "aoe",
         "level": 10, "power": 1.6, "hits": 3,
         "desc": "Strike every enemy three times. 1.6x damage per hit."},
        {"name": "Void Fist",         "cost": 60, "resource": "Ki", "type": "attack",
         "level": 15, "power": 3.5, "element": "arcane",
         "desc": "The ultimate unarmed technique. Arcane damage through existence itself."},
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
    """
    Returns [option_A, option_B] if there's a branch choice at this level,
    or None if it's a normal auto-learn level.
    """
    branches = ABILITY_BRANCHES.get(class_name, {})
    return branches.get(level, None)


def has_branch_choice_pending(character):
    """
    Returns the branch options if the character has reached a branch level
    but hasn't yet chosen (i.e. neither option is in their abilities).
    Returns None if no pending choice.
    """
    next_lvl = character.level
    branch = get_branch_at_level(character.class_name, next_lvl)
    if not branch:
        return None
    known_names = {a["name"] for a in character.abilities}
    # If they already know one of the options, they've already chosen
    if any(opt["name"] in known_names for opt in branch):
        return None
    # Check if neither is known (pending choice)
    return branch


def choose_branch(character, chosen_ability):
    """
    Record the player's branch choice. Adds the chosen ability to the character.
    The unchosen ability is implicitly locked (not present in abilities list).
    """
    known_names = {a["name"] for a in character.abilities}
    if chosen_ability["name"] not in known_names:
        character.abilities.append(chosen_ability.copy())
    return True
