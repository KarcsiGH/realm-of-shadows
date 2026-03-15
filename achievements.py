"""
Realm of Shadows — Achievement Definitions

Each achievement has:
  id:          unique string key
  name:        display name
  description: how to unlock it
  icon:        color tuple (used as visual identifier)
  check:       callable(story_flags, party) → bool

Achievements are checked after combat, after quests complete, and when
entering camps/towns.
"""

ACHIEVEMENTS = {
    # ── Story milestones ─────────────────────────────────────────────────────
    "first_dungeon": {
        "name": "Into the Dark",
        "description": "Complete your first dungeon.",
        "icon": (160, 120, 60),
        "check": lambda f, p: bool(f.get("boss_defeated.goblin_warren")),
    },
    "all_hearthstones": {
        "name": "The Ward Rekindled",
        "description": "Collect all five Hearthstones.",
        "icon": (255, 200, 60),
        "check": lambda f, p: all(f.get(f"item.hearthstone.{i}") for i in range(1, 6)),
    },
    "shadow_valdris": {
        "name": "Into the Shadow",
        "description": "Defeat Shadow Valdris and end the Fading.",
        "icon": (180, 100, 220),
        "check": lambda f, p: bool(f.get("boss_defeated.shadow_valdris")),
    },
    "maren_truth": {
        "name": "The Other Side",
        "description": "Discover the truth about Maren.",
        "icon": (100, 160, 220),
        "check": lambda f, p: bool(f.get("maren.truth_known")),
    },
    "goblin_peace": {
        "name": "The Peaceful Path",
        "description": "Spare Grak and forge peace with the goblins.",
        "icon": (80, 180, 80),
        "check": lambda f, p: bool(f.get("goblin_peace")),
    },
    "all_dungeons": {
        "name": "Delver Supreme",
        "description": "Clear all ten dungeons.",
        "icon": (200, 80, 80),
        "check": lambda f, p: all(
            f.get(f"boss_defeated.{d}") for d in [
                "goblin_warren", "spiders_nest", "abandoned_mine", "sunken_crypt",
                "ruins_ashenmoor", "dragons_tooth", "pale_coast", "windswept_isle",
                "valdris_spire", "shadow_throne",
            ]
        ),
    },

    # ── Progression ──────────────────────────────────────────────────────────
    "reach_level_10": {
        "name": "Veteran",
        "description": "Reach level 10 with any character.",
        "icon": (100, 180, 200),
        "check": lambda f, p: any(c.level >= 10 for c in p),
    },
    "class_transition": {
        "name": "The Path Splits",
        "description": "Complete a class transition.",
        "icon": (160, 80, 200),
        "check": lambda f, p: any(
            c.class_name not in ("Fighter","Mage","Cleric","Thief","Ranger","Monk")
            for c in p
        ),
    },
    "apex_class": {
        "name": "Ascension",
        "description": "Reach an apex class (level 15 transition).",
        "icon": (220, 180, 40),
        "check": lambda f, p: any(
            c.class_name in ("Knight","Archmage","High Priest","Shadow Master",
                              "Beastlord","Ascetic")
            for c in p
        ),
    },
    "full_party_level15": {
        "name": "The Warden Order",
        "description": "Bring your entire party to level 15.",
        "icon": (200, 200, 100),
        "check": lambda f, p: len(p) >= 4 and all(c.level >= 15 for c in p),
    },
    "high_planar_tier": {
        "name": "Beyond Mortal",
        "description": "Reach the Steel tier or higher.",
        "icon": (140, 200, 240),
        "check": lambda f, p: (f.get("planar_tier", 0) or 0) >= 3,
    },

    # ── Combat ───────────────────────────────────────────────────────────────
    "first_kill": {
        "name": "Baptism of Fire",
        "description": "Win your first combat.",
        "icon": (200, 100, 60),
        "check": lambda f, p: (f.get("total_kills", 0) or 0) >= 1,
    },
    "hundred_kills": {
        "name": "Bloodied",
        "description": "Defeat 100 enemies.",
        "icon": (200, 60, 60),
        "check": lambda f, p: (f.get("total_kills", 0) or 0) >= 100,
    },
    "flawless_victory": {
        "name": "Untouchable",
        "description": "Win a combat without any party member losing HP.",
        "icon": (120, 220, 120),
        "check": lambda f, p: bool(f.get("achievement.flawless_victory")),
    },
    "solo_survivor": {
        "name": "Last One Standing",
        "description": "Win a combat with only one party member alive.",
        "icon": (220, 100, 100),
        "check": lambda f, p: bool(f.get("achievement.solo_survivor")),
    },

    # ── Exploration ──────────────────────────────────────────────────────────
    "all_towns": {
        "name": "Wanderer",
        "description": "Visit all eight towns.",
        "icon": (80, 160, 120),
        "check": lambda f, p: all(
            f.get(f"visited.{t}") for t in [
                "briarhollow","woodhaven","ironhearth","greenwood",
                "saltmere","sanctum","crystalspire","thornhaven",
            ]
        ),
    },
    "all_quests": {
        "name": "Completionist",
        "description": "Complete all main quests.",
        "icon": (240, 200, 80),
        "check": lambda f, p: all(
            f.get(f"quest.{q}.state") == -2 for q in [
                "main_goblin_warren","main_hearthstone_1","main_spiders_nest",
                "main_ashenmoor","main_hearthstone_2","main_hearthstone_3",
                "main_thornhaven","main_act3_spire","main_pale_coast",
                "main_windswept_isle","main_act3_finale",
            ]
        ),
    },
    "side_quester": {
        "name": "Good Samaritan",
        "description": "Complete five side quests.",
        "icon": (100, 200, 160),
        "check": lambda f, p: sum(
            1 for q in ["side_wolf_pelts","side_missing_patrol","side_guild_initiation",
                        "side_academy_research","side_last_evacuees","side_warden_relic",
                        "side_arcane_salvage","side_deserters","side_tide_priest_request"]
            if f.get(f"quest.{q}.state") == -2
        ) >= 5,
    },
    "job_board": {
        "name": "Hired Sword",
        "description": "Complete 10 job board contracts.",
        "icon": (160, 140, 80),
        "check": lambda f, p: (f.get("total_jobs_completed", 0) or 0) >= 10,
    },

    # ── Secrets & special ────────────────────────────────────────────────────
    "dragon_tooth_boss": {
        "name": "Dragon Tamer",
        "description": "Defeat Karreth, the last dragon warden.",
        "icon": (220, 100, 40),
        "check": lambda f, p: bool(f.get("boss_defeated.dragons_tooth")),
    },
    "full_knowledge": {
        "name": "Encyclopaedist",
        "description": "Reach full knowledge tier for 20 different enemies.",
        "icon": (140, 160, 200),
        "check": lambda f, p: bool(f.get("achievement.full_knowledge")),
    },
}
