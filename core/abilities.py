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
         "level": 1, "buff": "defense_up", "duration": 2, "desc": "Reduce incoming damage for 2 turns."},
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
         "level": 1, "power": 1.0, "element": "arcane", "auto_hit": True, "desc": "Arcane bolt that never misses."},
        {"name": "Arcane Shield",    "cost": 10, "resource": "INT-MP", "type": "buff",
         "level": 1, "buff": "magic_shield", "duration": 3, "desc": "Magical barrier absorbing damage."},
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
        {"name": "Cure Poison",      "cost": 8,  "resource": "PIE-MP", "type": "cure",
         "level": 3, "cures": "poison", "desc": "Remove poison from one ally."},
        {"name": "Prayer of Healing","cost": 20, "resource": "PIE-MP", "type": "aoe_heal",
         "level": 5, "power": 1.0, "desc": "Heal all allies for a moderate amount."},
        {"name": "Turn Undead",      "cost": 15, "resource": "PIE-MP", "type": "debuff",
         "level": 5, "targets": "undead", "fear_duration": 3, "desc": "Force undead to flee for 3 turns."},
        {"name": "Divine Wrath",     "cost": 30, "resource": "PIE-MP", "type": "aoe",
         "level": 10, "power": 1.8, "element": "divine", "desc": "Holy fire consumes all enemies."},
    ],
    "Thief": [
        {"name": "Quick Strike",     "cost": 8,  "resource": "DEX-SP", "type": "attack",
         "level": 1, "power": 1.3, "bonus_crit": 15, "desc": "Fast strike with +15% crit chance."},
        {"name": "Evade",            "cost": 6,  "resource": "DEX-SP", "type": "buff",
         "level": 1, "buff": "evasion", "duration": 2, "desc": "Greatly increase dodge chance for 2 turns."},
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
        {"name": "Track",            "cost": 5,  "resource": "WIS-MP", "type": "buff",
         "level": 1, "buff": "tracking", "duration": 5, "desc": "Heighten awareness. Reveal hidden enemies."},
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
         "level": 1, "buff": "iron_skin", "duration": 3, "desc": "Harden body, reducing physical damage taken."},
        {"name": "Stunning Fist",    "cost": 12, "resource": "Ki", "type": "attack",
         "level": 3, "power": 1.3, "stun_chance": 0.45, "desc": "Precise strike. 45% chance to stun."},
        {"name": "Inner Peace",      "cost": 15, "resource": "Ki", "type": "heal",
         "level": 5, "power": 1.2, "self_only": True, "desc": "Meditate to restore own HP."},
        {"name": "Pressure Point",   "cost": 18, "resource": "Ki", "type": "debuff",
         "level": 8, "weaken_duration": 3, "desc": "Strike nerve clusters. Target deals 30% less damage."},
        {"name": "Dragon Strike",    "cost": 30, "resource": "Ki", "type": "attack",
         "level": 12, "power": 2.8, "element": "fire", "desc": "Channel ki into a devastating fire strike."},
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
