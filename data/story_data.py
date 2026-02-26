"""
Realm of Shadows — Story Data

All narrative content: NPCs, dialogue trees, quest definitions,
lore entries, dungeon story events, and tavern rumors by act.
"""


# ═══════════════════════════════════════════════════════════════
#  OPENING NARRATIVE
# ═══════════════════════════════════════════════════════════════

OPENING_SEQUENCE = [
    ("", "The world of Aldenmere is dying."),
    ("", "They call it the Fading — a creeping emptiness that swallows villages whole. "
     "People vanish. Memories dissolve. The sun itself seems dimmer each season."),
    ("", "The ancient wards that held the darkness at bay for a thousand years "
     "are failing, one by one."),
    ("", "You arrived in Briarhollow three days ago — strangers, drawn together "
     "by rumor and desperation. Each of you carries the old blood, the mark of the "
     "Wardens — an order thought extinct for centuries."),
    ("", "A woman named Maren found you. She says the Fading can be stopped. "
     "She says you're the only ones who can do it."),
    ("", "She's waiting at the tavern. Whatever happens next, the world will never "
     "be the same."),
]


# ═══════════════════════════════════════════════════════════════
#  QUEST DEFINITIONS
# ═══════════════════════════════════════════════════════════════

QUESTS = {
    # ── Act 1 — Briarhollow & surroundings ─────────────────────────
    "main_meet_maren": {
        "name": "The Scholar's Plea",
        "description": "Elder Thom mentioned a scholar staying at the inn who knows "
                       "something about the land sickness. Meet Maren at the Wanderer's Rest.",
        "act": 1,
        "giver_npc": "Elder Thom",
        "turn_in_npc": "Maren",
        "reward_gold": 0,
        "reward_xp": 50,
        "reward_items": [],
        "objectives": [
            {
                "text": "Speak with Maren at the Wanderer's Rest",
                "flag": "npc.maren.met", "op": "==", "val": True,
            },
        ],
    },

    "main_goblin_warren": {
        "name": "The Goblin Problem",
        "description": "Maren believes the goblin raids aren't random — something is "
                       "driving them out of the Warren. Investigate.",
        "act": 1,
        "giver_npc": "Maren",
        "turn_in_npc": "Maren",
        "reward_gold": 150,
        "reward_xp": 200,
        "reward_items": [],
        "objectives": [
            {
                "text": "Enter the Goblin Warren",
                "flag": "explored.goblin_warren.floor1", "op": "==", "val": True,
            },
            {
                "text": "Defeat Grak, the Goblin King",
                "flag": "boss.grak.defeated", "op": "==", "val": True,
            },
        ],
    },

    "main_hearthstone_1": {
        "name": "The First Hearthstone",
        "description": "Maren has identified the Abandoned Mine as the site of the first "
                       "Hearthstone. A corrupted Warden guards it. Recover the fragment.",
        "act": 1,
        "giver_npc": "Maren",
        "turn_in_npc": "Maren",
        "reward_gold": 200,
        "reward_xp": 300,
        "reward_items": [],
        "objectives": [
            {
                "text": "Descend into the Abandoned Mine",
                "flag": "explored.abandoned_mine.floor1", "op": "==", "val": True,
            },
            {
                "text": "Defeat the Warden Korrath",
                "flag": "boss.korrath.defeated", "op": "==", "val": True,
            },
            {
                "text": "Recover the First Hearthstone",
                "flag": "item.hearthstone.1", "op": "==", "val": True,
            },
        ],
    },

    "main_spiders_nest": {
        "name": "Unnatural Growth",
        "description": "The Spider's Nest creatures have grown massive — a sign of Fading "
                       "corruption. Investigate and stop the spread.",
        "act": 1,
        "giver_npc": "Elder Theron",
        "turn_in_npc": "Maren",
        "reward_gold": 120,
        "reward_xp": 180,
        "reward_items": [],
        "objectives": [
            {
                "text": "Enter the Spider's Nest",
                "flag": "explored.spiders_nest.floor1", "op": "==", "val": True,
            },
            {
                "text": "Defeat the Spider Queen",
                "flag": "boss_defeated.spiders_nest", "op": "==", "val": True,
            },
        ],
    },

    "side_wolf_pelts": {
        "name": "Pelts for the Tanner",
        "description": "Captain Aldric mentioned the village tanner needs wolf pelts. "
                       "The wolves are aggressive and unusually large.",
        "act": 1,
        "giver_npc": "Captain Aldric",
        "turn_in_npc": "Captain Aldric",
        "reward_gold": 80,
        "reward_xp": 60,
        "reward_items": [],
        "objectives": [
            {
                "text": "Collect Wolf Pelts (5 needed)",
                "flag": "wolf_pelts_quest.count", "op": ">=", "val": 5,
            },
        ],
    },

    "side_missing_patrol": {
        "name": "The Missing Patrol",
        "description": "Captain Aldric's patrol never returned from the eastern road. "
                       "Find out what happened to them.",
        "act": 1,
        "giver_npc": "Captain Aldric",
        "turn_in_npc": "Captain Aldric",
        "reward_gold": 100,
        "reward_xp": 120,
        "reward_items": [],
        "objectives": [
            {
                "text": "Search the eastern road and mine area",
                "flag": "explored.abandoned_mine.floor2", "op": "==", "val": True,
            },
        ],
    },

    # ── Act 2 — Wider world ─────────────────────────────────────────
    "main_ashenmoor": {
        "name": "Secrets of Ashenmoor",
        "description": "The Ruins of Ashenmoor hold the truth about the first Fading event. "
                       "Maren insists the answers are buried there.",
        "act": 2,
        "giver_npc": "Maren",
        "turn_in_npc": "Maren",
        "reward_gold": 250,
        "reward_xp": 400,
        "reward_items": [],
        "objectives": [
            {
                "text": "Reach the Ruins of Ashenmoor",
                "flag": "explored.ruins_ashenmoor.floor1", "op": "==", "val": True,
            },
            {
                "text": "Defeat Ashvar, the Shadow Warden",
                "flag": "boss.ashvar.defeated", "op": "==", "val": True,
            },
        ],
    },

    "main_hearthstone_2": {
        "name": "The Sunken Stone",
        "description": "Tide Priest Oran revealed a Hearthstone sealed under the bay "
                       "centuries ago. Descend into the Sunken Crypt to reclaim it.",
        "act": 2,
        "giver_npc": "Tide Priest Oran",
        "turn_in_npc": "Tide Priest Oran",
        "reward_gold": 300,
        "reward_xp": 500,
        "reward_items": [],
        "objectives": [
            {
                "text": "Enter the Sunken Crypt",
                "flag": "explored.sunken_crypt.floor1", "op": "==", "val": True,
            },
            {
                "text": "Defeat the Sunken Warden",
                "flag": "boss.sunken_warden.defeated", "op": "==", "val": True,
            },
            {
                "text": "Recover the Second Hearthstone",
                "flag": "item.hearthstone.2", "op": "==", "val": True,
            },
        ],
    },

    "main_hearthstone_3": {
        "name": "Fire and Salt",
        "description": "The third Hearthstone lies in the Dragon's Tooth archipelago. "
                       "Arrange passage from Saltmere and survive what waits there.",
        "act": 2,
        "giver_npc": "Tide Priest Oran",
        "turn_in_npc": None,
        "auto_complete": True,
        "reward_gold": 350,
        "reward_xp": 550,
        "reward_items": [],
        "objectives": [
            {
                "text": "Arrange sea passage from Saltmere",
                "flag": "ship_passage.granted", "op": "==", "val": True,
            },
            {
                "text": "Reach Dragon's Tooth",
                "flag": "explored.dragons_tooth.floor1", "op": "==", "val": True,
            },
            {
                "text": "Defeat Karreth, the Dragon Warden",
                "flag": "boss.karreth.defeated", "op": "==", "val": True,
            },
            {
                "text": "Recover the Third Hearthstone",
                "flag": "item.hearthstone.3", "op": "==", "val": True,
            },
        ],
    },

    "main_thornhaven": {
        "name": "Audience with the Governor",
        "description": "Archmage Solen believes the Imperial Governor has access to "
                       "archives that can locate the remaining Hearthstones. Travel to Thornhaven.",
        "act": 2,
        "giver_npc": "Archmage Solen",
        "turn_in_npc": "Governor Aldric",
        "reward_gold": 0,
        "reward_xp": 200,
        "reward_items": [],
        "objectives": [
            {
                "text": "Travel to Thornhaven",
                "flag": "town.thornhaven.visited", "op": "==", "val": True,
            },
            {
                "text": "Speak with Governor Aldric",
                "flag": "npc.governor.met", "op": "==", "val": True,
            },
        ],
    },

    "main_maren_truth": {
        "name": "The Scholar's Secret",
        "description": "Court Mage Sira has revealed that Maren is the daughter of Valdris. "
                       "Confront her about what she truly intends to do with the Hearthstones.",
        "act": 2,
        "giver_npc": "Court Mage Sira",
        "turn_in_npc": "Maren",
        "reward_gold": 0,
        "reward_xp": 150,
        "reward_items": [],
        "objectives": [
            {
                "text": "Confront Maren about her true identity",
                "flag": "lore.maren_origin", "op": "==", "val": True,
            },
        ],
    },

    "main_act2_pursuit": {
        "name": "What Maren Took",
        "description": "Maren has vanished with two Hearthstone fragments. "
                       "She believes her father's ritual will save the world — "
                       "but Ashenmoor shows what his methods cost. Find her.",
        "act": 2,
        "giver_npc": None,
        "turn_in_npc": None,
        "auto_complete": True,
        "reward_gold": 0,
        "reward_xp": 0,
        "reward_items": [],
        "objectives": [
            {
                "text": "Track Maren to Valdris' Spire",
                "flag": "explored.valdris_spire.floor1", "op": "==", "val": True,
            },
        ],
    },

    "side_guild_initiation": {
        "name": "Proving Ground",
        "description": "Guildmaster Oren wants proof of your party's capabilities "
                       "before granting full Guild standing.",
        "act": 2,
        "giver_npc": "Guildmaster Oren",
        "turn_in_npc": "Guildmaster Oren",
        "reward_gold": 200,
        "reward_xp": 250,
        "reward_items": [],
        "objectives": [
            {
                "text": "Reach floor 3 of any major dungeon",
                "flag": "guild_trial.complete", "op": "==", "val": True,
            },
        ],
    },

    "side_academy_research": {
        "name": "Data for the Archmage",
        "description": "Archmage Solen needs ley line readings from three active Fading zones. "
                       "Dangerous work — but the Academy pays accordingly.",
        "act": 2,
        "giver_npc": "Archmage Solen",
        "turn_in_npc": "Archmage Solen",
        "reward_gold": 400,
        "reward_xp": 350,
        "reward_items": [],
        "objectives": [
            {
                "text": "Ley readings: Abandoned Mine (floor 3)",
                "flag": "explored.abandoned_mine.floor3", "op": "==", "val": True,
            },
            {
                "text": "Ley readings: Sunken Crypt (floor 2)",
                "flag": "explored.sunken_crypt.floor2", "op": "==", "val": True,
            },
            {
                "text": "Ley readings: Ruins of Ashenmoor (floor 2)",
                "flag": "explored.ruins_ashenmoor.floor2", "op": "==", "val": True,
            },
        ],
    },

    # ── Act 3 — The Spire ───────────────────────────────────────────
    "main_act3_spire": {
        "name": "The Long Road",
        "description": "Maren has a head start. Valdris' Spire stands at the edge "
                       "of the known world. Whatever she finds there, you cannot let "
                       "it end without you. Reach the Spire.",
        "act": 3,
        "giver_npc": "Guild Commander Varek",
        "turn_in_npc": None,
        "auto_complete": True,
        "reward_gold": 0,
        "reward_xp": 0,
        "reward_items": [],
        "objectives": [
            {
                "text": "Reach Valdris' Spire",
                "flag": "explored.valdris_spire.floor1", "op": "==", "val": True,
            },
        ],
    },

    "main_act3_finale": {
        "name": "The Last Warden",
        "description": "Inside Valdris' Spire. At the top waits what remains of the man "
                       "who broke the wards and unmade Ashenmoor. Maren is here too — "
                       "which side she lands on may depend on you. Reach the summit.",
        "act": 3,
        "giver_npc": None,
        "turn_in_npc": None,
        "auto_complete": True,
        "reward_gold": 0,
        "reward_xp": 1500,
        "reward_items": [],
        "objectives": [
            {
                "text": "Ascend to the summit of the Spire",
                "flag": "explored.valdris_spire.floor5", "op": "==", "val": True,
            },
            {
                "text": "Confront Valdris — or what remains of him",
                "flag": "boss_defeated.shadow_valdris", "op": "==", "val": True,
            },
        ],
    },
}


# ═══════════════════════════════════════════════════════════════
#  LORE ENTRIES
# ═══════════════════════════════════════════════════════════════

LORE_ENTRIES = {
    "fading_basics": {
        "title": "The Fading",
        "text": "A creeping magical entropy that dissolves reality itself. "
                "First observed decades ago as minor distortions, it has accelerated "
                "to consume entire settlements. Those caught in a Fading event "
                "are never seen again.",
    },
    "wardens_history": {
        "title": "The Wardens of Aldenmere",
        "text": "An ancient order charged with maintaining the wards that protect "
                "the world from the Shadow Realm. Their bloodline carries a natural "
                "resistance to the Fading. Thought extinct for over two centuries.",
    },
    "hearthstones": {
        "title": "The Hearthstones",
        "text": "Five crystallized fragments of pure ward-magic. Together they "
                "anchor the barrier between worlds. When all five were in place, "
                "the Fading could never breach the world. Now scattered and "
                "guarded by corrupted Wardens, they must be reunited.",
    },
    "grak_truth": {
        "title": "Grak's Burden",
        "text": "The Goblin King was no conqueror. His tribe fled underground "
                "when the Fading consumed their forest home. The Hearthstone fragment "
                "he carried was entrusted to him by a dying Warden — the last act "
                "of a guardian who could no longer resist the Shadow.",
    },
    "valdris_betrayal": {
        "title": "The Traitor Warden",
        "text": "Valdris, the most powerful Warden of his generation, believed "
                "the Shadow could be harnessed rather than sealed away. His experiments "
                "weakened the wards catastrophically. When confronted by his order, "
                "he destroyed three of the five Hearthstones' anchor points and "
                "vanished into the Shadow Realm.",
    },
    "maren_origin": {
        "title": "Maren's Secret",
        "text": "The scholar Maren is not what she claims. Her true name is "
                "Maren Valdris — daughter of the traitor. She seeks the Hearthstones "
                "not to restore the wards as they were, but to complete her father's "
                "original ritual — correctly this time. Whether her intentions are "
                "noble remains to be seen.",
    },
    "maren_gone": {
        "title": "The Scholar's Departure",
        "text": "Maren Valdris revealed herself before she left. She took two of the "
                "recovered Hearthstone fragments — enough, she said, to reach Valdris' Spire. "
                "Her stated goal: complete her father's original ritual, which she claims "
                "would make the ward-network self-sustaining, requiring no further sacrifice. "
                "Ashenmoor was, she insisted, a miscalculation — not the intended outcome. "
                "She left one fragment behind. It is unclear whether this was mercy, "
                "practicality, or something else entirely.",
    },
    "governor_knowledge": {
        "title": "The Governor's Files",
        "text": "The Imperial Governor of Thornhaven has quietly maintained Warden records "
                "for decades. The Empire's official policy is non-intervention, but the Governor "
                "has been preparing contingencies. He knows where two of the Hearthstones are "
                "believed to rest.",
    },
    "hearthstone_locations": {
        "title": "Hearthstone Resonance",
        "text": "Using the first recovered Hearthstone as a reference, the Mage Academy "
                "detected two strong resonance signals: one from the Sunken Crypt to the south, "
                "and one from the Dragon's Tooth archipelago to the east.",
    },
    "hearthstone_bloodlines": {
        "title": "The Bloodline Oaths",
        "text": "Each Hearthstone was placed by a Warden who swore an oath of their bloodline. "
                "While a bloodline descendant lives and holds the oath, the stone stays anchored. "
                "As bloodlines die out, the stones drift and the Fading accelerates. "
                "The last active Warden bloodlines are nearly gone.",
    },
    "fading_intention": {
        "title": "The Pattern in the Fading",
        "text": "Analysis of Fading events reveals a deliberate pattern — they occur first "
                "and most intensely near old Warden anchor points and undefended Hearthstone sites. "
                "The Fading is not random entropy. Something intelligent is targeting the ward network "
                "systematically.",
    },
    "fading_sea": {
        "title": "The Sea Fades Too",
        "text": "The Fading is not limited to land. Coastal priests report ships vanishing "
                "with no storms, no wreckage, no survivors. The barrier between worlds "
                "is dissolving wherever it is thinnest — including over open water.",
    },
    "imperial_hearthstone_records": {
        "title": "Imperial Warden Archives",
        "text": "The Governor's castle contains two centuries of Imperial observation of "
                "Warden activities — including the locations of three Hearthstone anchor sites "
                "and the bloodline names sworn to protect each one.",
    },
    "sunken_warden_truth": {
        "title": "The Price of the Binding",
        "text": "The Warden who guards the second Hearthstone is not a monster — he is "
                "a guardian bound by his own oath. His name was Deren. He died defending "
                "the stone and became its ward, unable to release it willingly. "
                "The only way to claim the stone is to defeat him in combat — which is what "
                "he wants, though it costs him everything.",
    },
    "valdris_true_plan": {
        "title": "Valdris's Vision",
        "text": "Valdris does not seek to destroy the world. He believes the barrier between "
                "the Shadow Realm and the mortal world is an unnatural cage that has weakened "
                "both sides for centuries. His goal is a full merger — one unified world of "
                "light and shadow. Whether this would be salvation or annihilation is unknown. "
                "He is utterly convinced it is the former.",
    },
    "dragon_karreth": {
        "title": "Karreth the Guardian",
        "text": "Before the Wardens existed, the dragon Karreth served as the first "
                "ward-guardian of the eastern archipelago. When the nearest Hearthstone anchor "
                "failed, the Fading entered the ancient creature and began corrupting it. "
                "Karreth does not understand what is happening to it. It only knows "
                "an imperative to protect the warm light at its center — the third Hearthstone.",
    },
    "ashenmoor_fall": {
        "title": "The Fall of Ashenmoor",
        "text": "Ashenmoor was a Warden garrison city — two hundred and twelve people, "
                "most of them support staff, scholars, and their families. "
                "The city was destroyed when Warden-Researcher Valdris opened a shadow rift "
                "inside the city's ward-anchor chamber. "
                "Commander Ashvar's execution order was signed but never carried out. "
                "Valdris was never found. "
                "The Council classified the incident and sealed all records.",
    },
    "korrath_truth": {
        "title": "The Stone Warden's Vigil",
        "text": "Korrath was the last surviving member of the Iron Ridge Warden chapter. "
                "Rather than abandon his post when the other Wardens fell, he used an old "
                "dwarven binding ritual to merge himself with the vault, becoming both its "
                "guardian and its lock. "
                "He has been aware, waiting, for over four hundred years. "
                "The binding cannot be dissolved — only satisfied.",
    },
    "ashvar_truth": {
        "title": "Commander Ashvar's Account",
        "text": "Ashvar commanded eighty-three Wardens at the time of Ashenmoor's destruction. "
                "He recognized the danger in Valdris's research long before anyone else, "
                "but acted too slowly. "
                "The Shadow energy released in the rift bound him to the ruins, "
                "preventing him from acting but preserving his awareness. "
                "He has spent centuries reconstructing exactly what Valdris planned — "
                "and is certain the spire is the final piece.",
    },
}


# ═══════════════════════════════════════════════════════════════
#  NPC DEFINITIONS
# ═══════════════════════════════════════════════════════════════

NPCS = {
    # ─── Briarhollow ───
    "maren": {
        "name": "Maren",
        "title": "Wandering Scholar",
        "location": "briarhollow",
        "portrait_color": (120, 80, 180),  # purple
    },
    "captain_rowan": {
        "name": "Captain Rowan",
        "title": "Town Guard Captain",
        "location": "briarhollow",
        "portrait_color": (180, 100, 60),  # brown-red
    },
    "bess": {
        "name": "Bess",
        "title": "Innkeeper, The Shadowed Flagon",
        "location": "briarhollow",
        "portrait_color": (200, 160, 80),  # warm gold
    },

    # ─── Woodhaven ───
    "elder_theron": {
        "name": "Elder Theron",
        "title": "Keeper of the Grove",
        "location": "woodhaven",
        "portrait_color": (60, 160, 80),  # forest green
    },
    "sylla": {
        "name": "Sylla",
        "title": "Herbalist",
        "location": "woodhaven",
        "portrait_color": (100, 180, 140),  # teal
    },

    # ─── Ironhearth ───
    "forgemaster_dunn": {
        "name": "Forgemaster Dunn",
        "title": "Master Blacksmith",
        "location": "ironhearth",
        "portrait_color": (200, 120, 60),  # forge orange
    },
    "merchant_kira": {
        "name": "Kira",
        "title": "Traveling Merchant",
        "location": "ironhearth",
        "portrait_color": (180, 80, 140),  # magenta
    },

    # ─── Greenwood ───
    "scout_feryn": {
        "name": "Scout Feryn",
        "title": "Forest Warden",
        "location": "greenwood",
        "portrait_color": (90, 150, 70),
    },

    # ─── Saltmere ───
    "guildmaster_sable": {
        "name": "Guildmaster Sable",
        "title": "Thieves' Guild, Saltmere Chapter",
        "location": "saltmere",
        "portrait_color": (120, 90, 160),
    },
    "tide_priest_oran": {
        "name": "Tide Priest Oran",
        "title": "Keeper of the Saltmere Shrine",
        "location": "saltmere",
        "portrait_color": (80, 130, 200),
    },

    # ─── Sanctum ───
    "high_priest_aldara": {
        "name": "High Priest Aldara",
        "title": "Grand Cathedral of Light",
        "location": "sanctum",
        "portrait_color": (230, 220, 160),
    },

    # ─── Crystalspire ───
    "archmage_solen": {
        "name": "Archmage Solen",
        "title": "Head of the Mage Academy",
        "location": "crystalspire",
        "portrait_color": (160, 180, 255),
    },
    "teleport_master": {
        "name": "Teleport Master Vaen",
        "title": "Keeper of the Circle",
        "location": "crystalspire",
        "portrait_color": (190, 160, 240),
    },

    # ─── Thornhaven ───
    "governor_aldric": {
        "name": "Governor Aldric",
        "title": "The Emperor's Voice in Aldenmere",
        "location": "thornhaven",
        "portrait_color": (200, 180, 100),
    },
    "guild_commander_varek": {
        "name": "Commander Varek",
        "title": "Adventurers' Guild, Imperial Chapter",
        "location": "thornhaven",
        "portrait_color": (140, 150, 180),
    },
    "court_mage_sira": {
        "name": "Court Mage Sira",
        "title": "Imperial Court Mage",
        "location": "thornhaven",
        "portrait_color": (150, 140, 220),
    },

    # ─── Dungeon NPCs ───
    "korrath": {
        "name": "Korrath the Stone Warden",
        "title": "Guardian of the First Hearthstone",
        "location": "abandoned_mine",
        "portrait_color": (140, 120, 80),  # warm stone brown
    },
    "ashvar": {
        "name": "Commander Ashvar",
        "title": "The Bound Commander",
        "location": "ruins_ashenmoor",
        "portrait_color": (80, 70, 65),  # ash grey
    },
    "grak": {
        "name": "Grak the Goblin King",
        "title": "King of the Warren",
        "location": "goblin_warren",
        "portrait_color": (100, 140, 60),  # goblin green
    },
    "sunken_warden": {
        "name": "The Sunken Warden",
        "title": "Undead Guardian of the Second Stone",
        "location": "sunken_crypt",
        "portrait_color": (80, 160, 180),
    },
    "valdris": {
        "name": "Valdris",
        "title": "The Traitor Warden",
        "location": "valdris_spire",
        "portrait_color": (160, 60, 80),
    },
    "karreth": {
        "name": "Karreth",
        "title": "The Corrupted Ward-Guardian",
        "location": "dragons_tooth",
        "portrait_color": (200, 80, 20),
    },
    "dockhand_riv": {
        "name": "Dockhand Riv",
        "title": "Harbor Hand, Saltmere",
        "location": "saltmere",
        "portrait_color": (100, 140, 180),
    },
    "spider_queen": {
        "name": "The Spider Queen",
        "title": "Between Worlds",
        "location": "spiders_nest",
        "portrait_color": (90, 40, 140),
    },
}


# ═══════════════════════════════════════════════════════════════
#  NPC DIALOGUE TREES
#  Each NPC has a list of dialogues ordered by priority.
#  The first one whose conditions pass is used.
# ═══════════════════════════════════════════════════════════════

NPC_DIALOGUES = {
    # ─────────────────────────────────────────────────────────
    #  MAREN — Main quest giver
    # ─────────────────────────────────────────────────────────
    "maren": [
        # ── ACT 2 MIDPOINT: MAREN'S BETRAYAL ──────────────────────────────────
        # Fires the first time the player talks to Maren after all three
        # major Act 1/2 dungeons are cleared (mine, ashenmoor, sunken crypt).
        {
            "conditions": [
                {"flag": "boss_defeated.abandoned_mine",   "op": "==", "value": True},
                {"flag": "boss_defeated.ruins_ashenmoor",  "op": "==", "value": True},
                {"flag": "boss_defeated.sunken_crypt",     "op": "==", "value": True},
                {"flag": "maren.betrayal_done",            "op": "not_exists"},
            ],
            "tree": {
                "id": "maren_betrayal",
                "nodes": {
                    "start": {
                        "speaker": "Maren",
                        "text": "I need to speak with you privately.\n"
                                "Not here. Inside.",
                        "choices": [
                            {"text": "All right.", "next": "approach"},
                            {"text": "You're making me nervous.", "next": "approach"},
                        ],
                    },
                    "approach": {
                        "speaker": "Maren",
                        "text": "You know, don't you. About Thornhaven. About what Sira told you.\n"
                                "Don't bother denying it — I could see it in your faces when you "
                                "came back. The way you looked at me differently. Calculating "
                                "what I might do.",
                        "choices": [
                            {"text": "She said you're Valdris's daughter.",        "next": "confirm"},
                            {"text": "She said you might not be what you claimed.", "next": "confirm"},
                            {"text": "Then you know why we're concerned.",          "next": "confirm"},
                        ],
                    },
                    "confirm": {
                        "speaker": "Maren",
                        "text": "Yes. I am. I've never lied to you about what I want — "
                                "I want the wards restored. I want the Fading stopped. "
                                "What I didn't tell you is how.\n"
                                "My father's ritual wasn't meant to destroy anything. "
                                "The current ward-network requires Warden blood to maintain. "
                                "Someone has to keep giving, keep sacrificing, indefinitely. "
                                "My father found a way to make it self-sustaining.",
                        "choices": [
                            {"text": "Ashenmoor. Two hundred people.",      "next": "ashenmoor"},
                            {"text": "And the ritual failed catastrophically.", "next": "ashenmoor"},
                            {"text": "Why didn't you just tell us this?",   "next": "why_silent"},
                        ],
                    },
                    "ashenmoor": {
                        "speaker": "Maren",
                        "text": "I know.\n"
                                "He miscalculated the resonance cascade. He knew it immediately — "
                                "he wrote it in his notes, the ones the Council burned. "
                                "He understood what he'd done. And he spent the rest of his life "
                                "correcting the equation.\n"
                                "I've had thirty years to finish what he couldn't.",
                        "next": "why_silent",
                    },
                    "why_silent": {
                        "speaker": "Maren",
                        "text": "Because you would have done exactly what you're doing now. "
                                "You would have looked at Ashenmoor and decided the risk was too "
                                "great. You would have tried to stop me.\n"
                                "And I couldn't let you stop me. Not when I'm this close.",
                        "choices": [
                            {"text": "We could have helped you do this safely.", "next": "could_help"},
                            {"text": "What are you planning to do right now?",   "next": "the_plan"},
                            {"text": "We're going to stop you.",                  "next": "stop_her"},
                        ],
                    },
                    "could_help": {
                        "speaker": "Maren",
                        "text": "Maybe. But I've watched how people respond to risk when "
                                "it's theoretical versus when they're standing in front of it. "
                                "I've seen scholars abandon thirty years of work because "
                                "someone more powerful told them to.\n"
                                "I couldn't take that chance. I'm sorry.",
                        "next": "the_plan",
                    },
                    "stop_her": {
                        "speaker": "Maren",
                        "text": "I know. That's why I'm not asking permission.\n"
                                "I'm telling you because you deserve to understand why.",
                        "next": "the_plan",
                    },
                    "the_plan": {
                        "speaker": "Maren",
                        "text": "I'm taking two of the three fragments. I need them to reach "
                                "the Spire — Valdris' Spire, which my father built specifically "
                                "to complete this ritual.\n"
                                "I'm leaving you one. It will still slow the Fading. "
                                "You can find the remaining stones — there are two more — "
                                "and catch up to me, if you choose.\n"
                                "Or you can try to stop me here.",
                        "choices": [
                            {"text": "What happens if the ritual fails again?",          "next": "failure"},
                            {"text": "You're gambling with every life in this region.",   "next": "stakes"},
                            {"text": "We'll find the other stones. And we'll find you.",  "next": "farewell_resolved"},
                            {"text": "Then we stop you here.",                            "next": "resist"},
                        ],
                    },
                    "failure": {
                        "speaker": "Maren",
                        "text": "Then the wards collapse anyway, and whatever the Fading was "
                                "holding back comes through. Which is what happens if we do "
                                "nothing.\n"
                                "The difference is: if I succeed, we end this permanently. "
                                "If I fail, we're no worse off than we already are.\n"
                                "My father's miscalculation was in the containment ring. "
                                "I've solved the containment problem.",
                        "next": "farewell_resolved",
                    },
                    "stakes": {
                        "speaker": "Maren",
                        "text": "Yes.\n"
                                "So is doing nothing.\n"
                                "I've thought about this every day for thirty years. "
                                "I'm not making this decision lightly.",
                        "next": "farewell_resolved",
                    },
                    "resist": {
                        "speaker": "Maren",
                        "text": "I was hoping you wouldn't say that.\n"
                                "I've prepared for this possibility too.",
                        "next": "escape",
                    },
                    "escape": {
                        "speaker": "Maren",
                        "text": "A ward-pulse. Disorienting, not lethal — I owe you that much.\n"
                                "When you can see straight again, I'll already be gone. "
                                "The fragment is on the table. I left it there for you.\n"
                                "Come to the Spire. See what I build. "
                                "Or try to stop me. Either way, we'll meet again.",
                        "on_enter": [
                            {"action": "set_flag",       "flag": "maren.betrayal_done",    "value": True},
                            {"action": "set_flag",       "flag": "maren.left",             "value": True},
                            {"action": "set_flag",       "flag": "maren.betray_resisted",  "value": True},
                            {"action": "complete_quest", "quest": "main_maren_truth"},
                            {"action": "start_quest",    "quest": "main_act2_pursuit"},
                            {"action": "discover_lore",  "lore": "maren_gone"},
                        ],
                        "end": True,
                    },
                    "farewell_resolved": {
                        "speaker": "Maren",
                        "text": "Thank you. For listening.\n"
                                "I know that doesn't make it better. "
                                "But I didn't want to leave without you understanding.\n"
                                "The fragment is there.",
                        "on_enter": [
                            {"action": "set_flag",       "flag": "maren.betrayal_done",    "value": True},
                            {"action": "set_flag",       "flag": "maren.left",             "value": True},
                            {"action": "set_flag",       "flag": "maren.betray_heard",     "value": True},
                            {"action": "complete_quest", "quest": "main_maren_truth"},
                            {"action": "start_quest",    "quest": "main_act2_pursuit"},
                            {"action": "discover_lore",  "lore": "maren_gone"},
                        ],
                        "end": True,
                    },
                },
            },
        },
        # After Maren has left — show a brief "gone" note if player walks to her spot
        {
            "conditions": [
                {"flag": "maren.left", "op": "==", "value": True},
            ],
            "tree": {
                "id": "maren_gone_note",
                "nodes": {
                    "start": {
                        "speaker": "Innkeeper Bess",
                        "text": "She left before dawn. Paid her tab and everything — "
                                "which surprised me, honestly. Left a note for your party.\n"
                                "It just says: \"I meant what I said. Find me at the Spire.\"",
                        "end": True,
                    },
                },
            },
        },
        # After goblin warren cleared
        {
            "conditions": [
                {"flag": "boss.grak.defeated", "op": "==", "value": True},
                {"flag": "quest.main_goblin_warren.state", "op": "!=", "value": -2},
            ],
            "tree": {
                "id": "maren_post_warren",
                "nodes": {
                    "start": {
                        "speaker": "Maren",
                        "text": "You've returned from the Warren. Tell me — did you find anything unusual?",
                        "choices": [
                            {"text": "Grak had a Hearthstone fragment. He was protecting it.",
                             "next": "truth",
                             "conditions": [{"flag": "lore.grak_truth", "op": "==", "value": True}]},
                            {"text": "We killed the Goblin King. The area should be safe now.",
                             "next": "no_truth"},
                        ],
                    },
                    "truth": {
                        "speaker": "Maren",
                        "text": "Protecting it... yes. That confirms what I feared. The old Wardens "
                                "entrusted fragments to anyone they could before the end. Even goblins. "
                                "We need to find the rest. The Abandoned Mine is our next step — a dwarven "
                                "Warden was stationed there long ago.",
                        "on_enter": [
                            {"action": "complete_quest", "quest": "main_goblin_warren"},
                            {"action": "start_quest", "quest": "main_hearthstone_1"},
                        ],
                        "end": True,
                    },
                    "no_truth": {
                        "speaker": "Maren",
                        "text": "Safe. Yes. But the goblins weren't the real threat, were they? "
                                "Something drove them from their forest. The Fading. We need to "
                                "move faster. Head to the Abandoned Mine next — there may be answers there.",
                        "on_enter": [
                            {"action": "complete_quest", "quest": "main_goblin_warren"},
                            {"action": "start_quest", "quest": "main_hearthstone_1"},
                        ],
                        "end": True,
                    },
                },
            },
        },
        # After Abandoned Mine cleared — Korrath defeated, Hearthstone 1 recovered
        {
            "conditions": [
                {"flag": "boss.korrath.defeated", "op": "==", "value": True},
                {"flag": "quest.main_hearthstone_1.state", "op": "!=", "value": -2},
            ],
            "tree": {
                "id": "maren_post_mine",
                "nodes": {
                    "start": {
                        "speaker": "Maren",
                        "text": "You made it back from the mine. I felt something shift — "
                                "in the air, in the wards. You found it, didn't you?\n"
                                "A Hearthstone fragment.",
                        "choices": [
                            {"text": "Yes. The dwarven Warden — Korrath — he was still there.",
                             "next": "korrath_truth",
                             "conditions": [{"flag": "lore.korrath_truth", "op": "==", "value": True}]},
                            {"text": "We fought our way through. The fragment is ours.",
                             "next": "fought"},
                        ],
                    },
                    "korrath_truth": {
                        "speaker": "Maren",
                        "text": "Still there. Four hundred years.\n"
                                "That's — that's devotion beyond anything I've read about. "
                                "The binding he used... it's old dwarven oath-magic. "
                                "He couldn't release the stone without being defeated. "
                                "He was waiting for us, in a way.\n"
                                "I hope he's at rest now.",
                        "on_enter": [
                            {"action": "complete_quest", "quest": "main_hearthstone_1"},
                            {"action": "set_flag", "flag": "hearthstone.abandoned_mine", "value": True},
                        ],
                        "next": "next_steps",
                    },
                    "fought": {
                        "speaker": "Maren",
                        "text": "A dwarven Warden bound to a fragment for centuries. "
                                "You fought an oath made flesh. Whatever he was before, "
                                "I hope the binding released him.\n"
                                "The fragment is what matters now.",
                        "on_enter": [
                            {"action": "complete_quest", "quest": "main_hearthstone_1"},
                            {"action": "set_flag", "flag": "hearthstone.abandoned_mine", "value": True},
                        ],
                        "next": "next_steps",
                    },
                    "next_steps": {
                        "speaker": "Maren",
                        "text": "One fragment recovered. Three or four still to go — "
                                "I'm still not sure of the exact number. "
                                "The Ruins of Ashenmoor may have answers. "
                                "Something's been active there. Not alive, exactly — but aware.\n"
                                "Be careful. Ashenmoor was destroyed by Warden experiments. "
                                "Whatever's left in those ruins saw what happened.",
                        "on_enter": [{"action": "start_quest", "quest": "main_ashenmoor"}],
                        "end": True,
                    },
                },
            },
        },
        # After Ruins of Ashenmoor cleared — Ashvar defeated, Valdris betrayal confirmed
        {
            "conditions": [
                {"flag": "boss.ashvar.defeated", "op": "==", "value": True},
                {"flag": "quest.main_ashenmoor.state", "op": "!=", "value": -2},
            ],
            "tree": {
                "id": "maren_post_ashenmoor",
                "nodes": {
                    "start": {
                        "speaker": "Maren",
                        "text": "You've been to Ashenmoor. I can see it in how you're standing.\n"
                                "What did you find?",
                        "choices": [
                            {"text": "A bound Warden commander. He knew Valdris.",
                             "next": "ashvar",
                             "conditions": [{"flag": "lore.ashvar_truth", "op": "==", "value": True}]},
                            {"text": "Evidence of what Valdris actually did.",
                             "next": "evidence",
                             "conditions": [{"flag": "lore.valdris_betrayal", "op": "==", "value": True}]},
                            {"text": "The ruins are clear. Something was guarding them.",
                             "next": "general"},
                        ],
                    },
                    "ashvar": {
                        "speaker": "Maren",
                        "text": "A bound commander... That would be Ashvar. My father wrote about him "
                                "in his earliest journals — dismissed him as an obstacle. 'Too rigid, "
                                "too rule-bound.' That's how Valdris described anyone who got in his way.\n"
                                "What did Ashvar tell you?",
                        "next": "ashvar_detail",
                    },
                    "ashvar_detail": {
                        "speaker": "Maren",
                        "text": "He watched it happen. He tried to stop it. And he was bound to those "
                                "ruins by the same magic that destroyed them.\n"
                                "Valdris did that to a man who served alongside him.",
                        "on_enter": [{"action": "discover_lore", "lore": "ashvar_truth"}],
                        "next": "maren_reaction",
                    },
                    "evidence": {
                        "speaker": "Maren",
                        "text": "The Commander's Log. I've seen references to it — "
                                "it was sealed when the Council covered up Ashenmoor.\n"
                                "My father weakened a ward-anchor deliberately. "
                                "And two hundred people died because of it.",
                        "next": "maren_reaction",
                    },
                    "general": {
                        "speaker": "Maren",
                        "text": "Something that saw what Valdris did, and was left behind when "
                                "the city was destroyed. The ruins have a way of keeping things.\n"
                                "What matters is that you got through.",
                        "next": "maren_reaction",
                    },
                    "maren_reaction": {
                        "speaker": "Maren",
                        "text": "When I was a child, I thought my father was the most principled man "
                                "I'd ever known. Everything he did was for the greater good. "
                                "He said that a lot.\n"
                                "I'm beginning to understand what he meant by it.",
                        "on_enter": [
                            {"action": "complete_quest", "quest": "main_ashenmoor"},
                            {"action": "set_flag", "flag": "maren.ashenmoor_revelation", "value": True},
                        ],
                        "end": True,
                    },
                },
            },
        },
        # After Briarhollow shadow attack
        {
            "conditions": [
                {"flag": "briarhollow_attack.done", "op": "==", "value": True},
                {"flag": "maren.post_attack_spoken", "op": "not_exists"},
            ],
            "tree": {
                "id": "maren_post_attack",
                "nodes": {
                    "start": {
                        "speaker": "Maren",
                        "text": "They came here. To Briarhollow. I didn't think it would happen this fast.\n"
                                "The Fading doesn't just unmake things at the edges anymore — "
                                "it's pushing creatures through. Sending them somewhere specific.\n"
                                "They were here for us. For the fragment you're carrying.",
                        "choices": [
                            {"text": "How do we stop them coming back?", "next": "stop"},
                            {"text": "Are the people here in danger?", "next": "danger"},
                            {"text": "We need to move faster.", "next": "faster"},
                        ],
                    },
                    "stop": {
                        "speaker": "Maren",
                        "text": "The only way to stop them is to restore the wards. Which means "
                                "finding the rest of the Hearthstones. Every fragment we collect "
                                "strengthens the network a little — enough to make this town "
                                "less of a beacon.\n"
                                "Right now, carrying that fragment is like holding a torch in a dark room "
                                "full of things that hate light.",
                        "next": "urge",
                    },
                    "danger": {
                        "speaker": "Maren",
                        "text": "Yes. Not immediately — shadow creatures aren't interested in "
                                "ordinary people. They're drawn to Warden energy, to the fragments.\n"
                                "But the longer we stay here with what we're carrying, "
                                "the more attacks there will be. "
                                "We protect this town by leaving it.",
                        "next": "urge",
                    },
                    "faster": {
                        "speaker": "Maren",
                        "text": "Yes. I agree. I've been too cautious — treating this like an "
                                "academic investigation instead of what it actually is.\n"
                                "We need to move.",
                        "next": "urge",
                    },
                    "urge": {
                        "speaker": "Maren",
                        "text": "The Ashenmoor ruins should have answers about what Valdris was actually "
                                "building. If we understand the plan, we can stop it.\n"
                                "And there are more Hearthstones to find. I can feel them, dimly — "
                                "like embers in the dark. We have to reach them before the Fading does.",
                        "on_enter": [
                            {"action": "set_flag", "flag": "maren.post_attack_spoken", "value": True},
                        ],
                        "end": True,
                    },
                },
            },
        },
        # After Dragon's Tooth cleared
        {
            "conditions": [
                {"flag": "boss_defeated.dragons_tooth", "op": "==", "value": True},
                {"flag": "maren.post_dragon_spoken",    "op": "not_exists"},
            ],
            "tree": {
                "id": "maren_post_dragon",
                "nodes": {
                    "start": {
                        "speaker": "Maren",
                        "text": "Three stones.\n"
                                "I felt it when you brought it back. The network is... "
                                "I don't have the right word for it. Louder. More present.\n"
                                "How was the island?",
                        "choices": [
                            {"text": "Karreth was the first ward-guardian. Before the Wardens.",
                             "next": "karreth_knew",
                             "condition": {"flag": "lore.dragon_karreth", "op": "==", "value": True}},
                            {"text": "We fought a dragon.",         "next": "just_fought"},
                            {"text": "There was something there. Ancient.", "next": "ancient"},
                        ],
                    },
                    "karreth_knew": {
                        "speaker": "Maren",
                        "text": "I know. The records mention a \"first warden\" — something "
                                "that predated the whole system. But I never thought it would "
                                "still be there.\n"
                                "Was it... did it know what it was?",
                        "choices": [
                            {"text": "At the end. It asked us to free it.", "next": "karreth_freed"},
                            {"text": "No. It only knew to protect the stone.", "next": "karreth_lost"},
                        ],
                    },
                    "karreth_freed": {
                        "speaker": "Maren",
                        "text": "Then it understood, at the end, what you were doing for it.\n"
                                "I hope that counts for something.\n"
                                "I've been thinking about the other bound guardians. "
                                "Korrath. The Sunken Warden. Karreth. All of them waiting, "
                                "centuries, because the ritual bound them and no one came back "
                                "to complete the cycle.\n"
                                "My father did that. Indirectly. He broke the cycle when "
                                "Ashenmoor fell.",
                        "on_enter": [
                            {"action": "set_flag", "flag": "maren.post_dragon_spoken", "value": True},
                        ],
                        "end": True,
                    },
                    "karreth_lost": {
                        "speaker": "Maren",
                        "text": "Four hundred years of vigil and it never got a chance to "
                                "understand why. That's the worst part of what the Fading does — "
                                "it doesn't destroy things cleanly. It corrupts them. "
                                "Turns guardians into obstacles.\n"
                                "This is what I'm trying to stop. Permanently.",
                        "on_enter": [
                            {"action": "set_flag", "flag": "maren.post_dragon_spoken", "value": True},
                        ],
                        "end": True,
                    },
                    "just_fought": {
                        "speaker": "Maren",
                        "text": "You fought a dragon.\n"
                                "I sometimes forget what I've been asking of you.\n"
                                "The Hearthstone is safe?",
                        "on_enter": [
                            {"action": "set_flag", "flag": "maren.post_dragon_spoken", "value": True},
                        ],
                        "end": True,
                    },
                    "ancient": {
                        "speaker": "Maren",
                        "text": "Ancient and corrupted. That's the Dragon's Tooth in a sentence.\n"
                                "But you came back with the fragment. That's what matters.\n"
                                "Three stones. Two more to find.",
                        "on_enter": [
                            {"action": "set_flag", "flag": "maren.post_dragon_spoken", "value": True},
                        ],
                        "end": True,
                    },
                },
            },
        },
        # First meeting — intro quest
        {
            "conditions": [
                {"flag": "npc.maren.met", "op": "not_exists"},
            ],
            "tree": {
                "id": "maren_intro",
                "nodes": {
                    "start": {
                        "speaker": "Maren",
                        "text": "So you've come. I wasn't sure you would. Please, sit — "
                                "what I have to tell you will change everything you think you know.",
                        "on_enter": [{"action": "meet_npc", "npc": "maren"}],
                        "next": "explain",
                    },
                    "explain": {
                        "speaker": "Maren",
                        "text": "You carry the old blood — the mark of the Wardens. You can feel "
                                "it, can't you? That wrongness in the air. The way shadows linger "
                                "too long. The way the light seems... tired.",
                        "choices": [
                            {"text": "What are the Wardens?", "next": "wardens"},
                            {"text": "What is the Fading?", "next": "fading"},
                            {"text": "What do you need from us?", "next": "mission"},
                        ],
                    },
                    "wardens": {
                        "speaker": "Maren",
                        "text": "An ancient order charged with maintaining the wards between our "
                                "world and the Shadow Realm. Your ancestors held back the darkness "
                                "for a thousand years. Then something went wrong. The order fell. "
                                "The wards began to fail. And the Fading began.",
                        "on_enter": [{"action": "discover_lore", "lore": "wardens_history"}],
                        "next": "mission",
                    },
                    "fading": {
                        "speaker": "Maren",
                        "text": "The barrier between our world and the Shadow Realm is dissolving. "
                                "Where it thins, reality itself unravels. People, buildings, entire "
                                "villages — consumed. Erased. Not dead. Just... gone. As if they "
                                "never existed.",
                        "on_enter": [{"action": "discover_lore", "lore": "fading_basics"}],
                        "next": "mission",
                    },
                    "mission": {
                        "speaker": "Maren",
                        "text": "The wards can be restored, but only with the Hearthstones — five "
                                "ancient artifacts scattered across Aldenmere. I've been tracking them "
                                "for years. The first lead points to the Goblin Warren east of here. "
                                "The goblins have been raiding our farms, but I believe they're "
                                "fleeing something far worse.",
                        "on_enter": [{"action": "discover_lore", "lore": "hearthstones"}],
                        "choices": [
                            {"text": "We'll investigate the Warren.", "next": "accept"},
                            {"text": "Why should we trust you?", "next": "trust"},
                        ],
                    },
                    "trust": {
                        "speaker": "Maren",
                        "text": "You shouldn't. Not yet. But go to the Warren. See for yourself "
                                "what the Fading leaves behind. Then decide.",
                        "next": "accept",
                    },
                    "accept": {
                        "speaker": "Maren",
                        "text": "Good. Be careful in there. The goblins are desperate and "
                                "dangerous, but they're not the real enemy. Remember that.",
                        "on_enter": [
                            {"action": "start_quest", "quest": "main_goblin_warren"},
                            {"action": "complete_quest", "quest": "main_meet_maren"},
                        ],
                        "end": True,
                    },
                },
            },
        },
        # Default fallback — after first meeting
        {
            "conditions": [],
            "tree": {
                "id": "maren_default",
                "nodes": {
                    "start": {
                        "speaker": "Maren",
                        "text": "The Fading won't wait for us. Have you made progress?",
                        "choices": [
                            {"text": "Tell me about the Hearthstones again.", "next": "hearthstones"},
                            {"text": "What should we do next?", "next": "next_step"},
                            {"text": "Goodbye.", "next": "bye"},
                        ],
                    },
                    "hearthstones": {
                        "speaker": "Maren",
                        "text": "Five stones, each a fragment of the original ward-magic. "
                                "Reunite them and the barrier holds. Fail, and there won't "
                                "be a world left to save.",
                        "end": True,
                    },
                    "next_step": {
                        "speaker": "Maren",
                        "text": "The Goblin Warren. That's where the trail leads. "
                                "The goblins know something — or they have something. "
                                "Find out which.",
                        "end": True,
                    },
                    "bye": {
                        "speaker": "Maren",
                        "text": "Go safely. The shadows are thicker every day.",
                        "end": True,
                    },
                },
            },
        },
    ],

    # ─────────────────────────────────────────────────────────
    #  CAPTAIN ROWAN
    # ─────────────────────────────────────────────────────────
    "captain_rowan": [
        # After meeting Maren
        {
            "conditions": [
                {"flag": "npc.maren.met", "op": "==", "value": True},
                {"flag": "npc.captain_rowan.met", "op": "not_exists"},
            ],
            "tree": {
                "id": "rowan_intro",
                "nodes": {
                    "start": {
                        "speaker": "Captain Rowan",
                        "text": "So you're the ones Maren's been going on about. Wardens, is it? "
                                "I don't know about ancient orders, but I know my patrol hasn't "
                                "come back from the eastern road. That's real enough.",
                        "on_enter": [{"action": "meet_npc", "npc": "captain_rowan"}],
                        "choices": [
                            {"text": "What happened to your patrol?", "next": "patrol"},
                            {"text": "What do you know about the goblins?", "next": "goblins"},
                            {"text": "Goodbye.", "next": "bye"},
                        ],
                    },
                    "patrol": {
                        "speaker": "Captain Rowan",
                        "text": "Six guards, good people. Sent them to check the eastern road "
                                "three days ago. Nothing since. The road passes near that goblin "
                                "cave. If you're heading that way, keep an eye out.",
                        "on_enter": [{"action": "start_quest", "quest": "side_missing_patrol"}],
                        "next": "goblins",
                    },
                    "goblins": {
                        "speaker": "Captain Rowan",
                        "text": "The goblins have been a nuisance for months, but recently it's "
                                "gotten worse. They're desperate — raiding in daylight, taking risks "
                                "they never used to. Something's driving them. I don't have the "
                                "fighters to deal with it.",
                        "end": True,
                    },
                    "bye": {
                        "speaker": "Captain Rowan",
                        "text": "Stay sharp out there.",
                        "end": True,
                    },
                },
            },
        },
        # Default
        {
            "conditions": [],
            "tree": {
                "id": "rowan_default",
                "nodes": {
                    "start": {
                        "speaker": "Captain Rowan",
                        "text": "Any news? I'm stretched thin as it is.",
                        "choices": [
                            {"text": "Any bounties available?", "next": "bounties"},
                            {"text": "Goodbye.", "next": "bye"},
                        ],
                    },
                    "bounties": {
                        "speaker": "Captain Rowan",
                        "text": "Clear the roads and I'll see you're compensated. "
                                "Every bandit and beast you put down helps this town survive.",
                        "end": True,
                    },
                    "bye": {
                        "speaker": "Captain Rowan",
                        "text": "Watch yourself.",
                        "end": True,
                    },
                },
            },
        },
    ],

    # ─────────────────────────────────────────────────────────
    #  BESS — Innkeeper
    # ─────────────────────────────────────────────────────────
    "bess": [
        {
            "conditions": [],
            "tree": {
                "id": "bess_default",
                "nodes": {
                    "start": {
                        "speaker": "Bess",
                        "text": "Welcome to the Flagon. You look like you could use a drink "
                                "and a warm bed. Or are you here for the gossip?",
                        "on_enter": [{"action": "meet_npc", "npc": "bess"}],
                        "choices": [
                            {"text": "What's the word around town?", "next": "rumors"},
                            {"text": "Tell me about Maren.", "next": "about_maren",
                             "conditions": [{"flag": "npc.maren.met", "op": "==", "value": True}]},
                            {"text": "Just passing through.", "next": "bye"},
                        ],
                    },
                    "rumors": {
                        "speaker": "Bess",
                        "text": "Strange times. The farmers say their crops are wilting even "
                                "with rain. Old Tam swears he saw his barn fade like a mirage "
                                "and come back an hour later. And those goblins — they look "
                                "scared, not angry. Whatever's out there, it frightens them too.",
                        "end": True,
                    },
                    "about_maren": {
                        "speaker": "Bess",
                        "text": "Maren? She arrived a fortnight ago. Quiet, pays on time, "
                                "spends all day with her books and maps. She asked about you lot "
                                "before you even got here. Knew you were coming somehow. "
                                "Gives me the chills, honestly.",
                        "end": True,
                    },
                    "bye": {
                        "speaker": "Bess",
                        "text": "Rest well. The world'll still need saving tomorrow.",
                        "end": True,
                    },
                },
            },
        },
    ],

    # ─────────────────────────────────────────────────────────
    #  KORRATH — Pre-boss dialogue in Abandoned Mine (Act 1)
    # ─────────────────────────────────────────────────────────
    "korrath": [
        {
            "conditions": [
                {"flag": "boss.korrath.defeated", "op": "not_exists"},
            ],
            "tree": {
                "id": "korrath_confrontation",
                "nodes": {
                    "start": {
                        "speaker": "Korrath the Stone Warden",
                        "text": "Hold. State your purpose in the vault of the Wardens.\n"
                                "I am Korrath, last of the Iron Ridge Wardens. "
                                "I have stood this watch for four hundred and twelve years. "
                                "I will stand it four hundred more, if need be.",
                        "choices": [
                            {"text": "We seek the Hearthstone. The wards are failing.", "next": "reason"},
                            {"text": "Who were the Iron Ridge Wardens?", "next": "history"},
                            {"text": "[Attack]", "next": "fight_direct"},
                        ],
                    },
                    "history": {
                        "speaker": "Korrath the Stone Warden",
                        "text": "We were twelve. Dwarves, mostly, with a few humans who had the talent "
                                "and the patience for stone-work. We sealed this vault when the other "
                                "Wardens began to fall. Dug it deep enough that nothing walking the surface "
                                "could reach it. We were right about that, at least.\n"
                                "None of us expected to run out of living Wardens.",
                        "choices": [
                            {"text": "We seek the Hearthstone. The wards are failing.", "next": "reason"},
                            {"text": "[Attack]", "next": "fight_direct"},
                        ],
                    },
                    "reason": {
                        "speaker": "Korrath the Stone Warden",
                        "text": "Failing. Yes. I can feel it from down here — the stone gets "
                                "colder every decade. The warmth in the fragment dims.\n"
                                "You carry Warden blood. I can read it in the way you stand. "
                                "But the oath I swore was not 'protect until someone worthy comes.' "
                                "It was 'protect until the stone breaks free of you or you break free of it.'\n"
                                "There is only one way to satisfy that oath.",
                        "choices": [
                            {"text": "Then we fight.", "next": "fight_accept"},
                            {"text": "Is there no other way?", "next": "no_other_way"},
                        ],
                    },
                    "no_other_way": {
                        "speaker": "Korrath the Stone Warden",
                        "text": "I have had four centuries to find one. There is not.\n"
                                "The binding is dwarven work — it does not bend. "
                                "But hear me: I do not wish to destroy you. "
                                "I wish to be defeated. When you win, the fragment is yours by right. "
                                "That is what I have been waiting for. "
                                "A party strong enough to take it from me.",
                        "on_enter": [{"action": "set_flag", "flag": "lore.korrath_truth", "value": True}],
                        "end": True,
                    },
                    "fight_accept": {
                        "speaker": "Korrath the Stone Warden",
                        "text": "Good. No sentiment. That is the dwarven way.\n"
                                "Come, then. Let the stone judge you.",
                        "end": True,
                    },
                    "fight_direct": {
                        "speaker": "Korrath the Stone Warden",
                        "text": "Straight to it. I respect that.\n"
                                "You will not find me easy, surface-dweller.",
                        "end": True,
                    },
                },
            },
        },
    ],

    # ─────────────────────────────────────────────────────────
    #  COMMANDER ASHVAR — Pre-boss dialogue in Ashenmoor (Act 2)
    # ─────────────────────────────────────────────────────────
    "ashvar": [
        {
            "conditions": [
                {"flag": "boss.ashvar.defeated", "op": "not_exists"},
            ],
            "tree": {
                "id": "ashvar_confrontation",
                "nodes": {
                    "start": {
                        "speaker": "Commander Ashvar",
                        "text": "Wardens. Or something like Wardens. You have the look.\n"
                                "I commanded eighty-three of them, once. I watched Valdris "
                                "hollow them out one by one. Convinced them the Shadow was a tool. "
                                "By the time I understood what he was doing, "
                                "there was nothing left to command.",
                        "choices": [
                            {"text": "What happened to Ashenmoor?", "next": "what_happened"},
                            {"text": "You know Valdris?", "next": "know_valdris"},
                            {"text": "We've seen his work. He's still out there.", "next": "still_alive"},
                            {"text": "[Attack]", "next": "fight_direct"},
                        ],
                    },
                    "what_happened": {
                        "speaker": "Commander Ashvar",
                        "text": "He opened a rift. Not an accident — deliberate. Called it a 'controlled "
                                "experiment.' Said the ward-anchor here was already compromised and we would "
                                "lose nothing by testing the limits.\n"
                                "Two hundred people lived in this city. "
                                "The rift did not distinguish between the experiment and them.",
                        "on_enter": [{"action": "discover_lore", "lore": "ashenmoor_fall"}],
                        "choices": [
                            {"text": "You know Valdris?", "next": "know_valdris"},
                            {"text": "We've seen his work. He's still out there.", "next": "still_alive"},
                        ],
                    },
                    "know_valdris": {
                        "speaker": "Commander Ashvar",
                        "text": "Know him. I trained him. He was the most gifted Warden I ever "
                                "evaluated — and the most certain that the rules applied to everyone else.\n"
                                "I ordered his quarters sealed when the experiments started. "
                                "He had already moved them underground by then. "
                                "He was always three steps ahead of where I was looking.",
                        "next": "still_alive",
                    },
                    "still_alive": {
                        "speaker": "Commander Ashvar",
                        "text": "Still alive.\n"
                                "Of course he is. That's the nature of his work — the Shadow preserves "
                                "what it cannot consume. He would have used that. Turned himself into "
                                "something permanent.\n"
                                "I was bound here by the same force that destroyed this city. "
                                "I have been... reconsidering what I know about Valdris for a long time. "
                                "He must be stopped. But I cannot leave this place.\n"
                                "You can. Once you get past me.",
                        "on_enter": [{"action": "set_flag", "flag": "lore.ashvar_truth", "value": True},
                                     {"action": "discover_lore", "lore": "valdris_betrayal"}],
                        "choices": [
                            {"text": "We'll stop him. But we have to get through you first.", "next": "fight_accept"},
                            {"text": "Why can't you just let us pass?", "next": "cant_pass"},
                        ],
                    },
                    "cant_pass": {
                        "speaker": "Commander Ashvar",
                        "text": "Because the Shadow that holds me here is part of Valdris's work. "
                                "It tests everyone who comes. It doesn't care about my intentions — "
                                "only about whether you are strong enough to continue.\n"
                                "I don't like it either. I never liked his methods.",
                        "end": True,
                    },
                    "fight_accept": {
                        "speaker": "Commander Ashvar",
                        "text": "Good. Don't hold back on my account. "
                                "I've been waiting for someone to end this posting.",
                        "end": True,
                    },
                    "fight_direct": {
                        "speaker": "Commander Ashvar",
                        "text": "No questions. Reasonable choice, given the circumstances.\n"
                                "Let's see what you're made of.",
                        "end": True,
                    },
                },
            },
        },
    ],

    # ─────────────────────────────────────────────────────────
    #  GRAK — Pre-boss dialogue in Goblin Warren
    # ─────────────────────────────────────────────────────────
    "grak": [
        {
            "conditions": [
                {"flag": "boss.grak.defeated", "op": "not_exists"},
            ],
            "tree": {
                "id": "grak_confrontation",
                "nodes": {
                    "start": {
                        "speaker": "Grak",
                        "text": "STOP! You come to Grak's home! You kill Grak's people! "
                                "But you don't know — you don't understand!",
                        "choices": [
                            {"text": "Why are the goblins raiding Briarhollow?", "next": "why"},
                            {"text": "Surrender and we'll spare you.", "next": "surrender"},
                            {"text": "[Attack]", "next": "fight"},
                        ],
                    },
                    "why": {
                        "speaker": "Grak",
                        "text": "The forest... the forest is GONE. The nothing came and ate it. "
                                "Ate the trees. Ate the rivers. Ate Grak's village. We ran here. "
                                "We had no food. Your farms were... there. Grak is sorry. "
                                "But my people were dying.",
                        "choices": [
                            {"text": "What is the stone you carry?", "next": "stone"},
                            {"text": "That doesn't excuse the raids.", "next": "fight"},
                        ],
                    },
                    "stone": {
                        "speaker": "Grak",
                        "text": "The bright-stone? A dying man gave it to Grak. A human. "
                                "He said 'protect this' and then the nothing took him. "
                                "Grak has kept it safe. It glows when the nothing comes close. "
                                "It kept us alive.",
                        "on_enter": [{"action": "discover_lore", "lore": "grak_truth"}],
                        "choices": [
                            {"text": "Give us the stone and we'll help your people.",
                             "next": "peaceful"},
                            {"text": "We need that stone. Hand it over.", "next": "demand"},
                        ],
                    },
                    "peaceful": {
                        "speaker": "Grak",
                        "text": "You... you would help? No human has ever... "
                                "Take it. Save the world from the nothing. "
                                "Grak will stop the raids. Grak swears it.",
                        "on_enter": [
                            {"action": "set_flag", "flag": "choice.grak_spared", "value": True},
                            {"action": "set_flag", "flag": "boss.grak.defeated", "value": True},
                            {"action": "set_flag", "flag": "goblin_peace", "value": True},
                            {"action": "set_flag", "flag": "hearthstone.goblin_warren", "value": True},
                            {"action": "set_quest", "quest": "main_goblin_warren", "state": 3},
                        ],
                        "next": "peaceful_end",
                    },
                    "peaceful_end": {
                        "speaker": "",
                        "text": "Grak reaches into his pile of stolen furniture and "
                                "carefully retrieves a glowing fragment — a piece of a "
                                "Hearthstone. It pulses warm in your hands. The goblins "
                                "watch you leave in silence. Their eyes hold something "
                                "you didn't expect: hope.",
                        "end": True,
                    },
                    "demand": {
                        "speaker": "Grak",
                        "text": "You are no different from the nothing. You take and take. "
                                "Then Grak will fight. For his people!",
                        "next": "fight",
                    },
                    "surrender": {
                        "speaker": "Grak",
                        "text": "Surrender? SURRENDER?! Grak does not surrender! "
                                "Grak fights for his people! RAAAAGH!",
                        "next": "fight",
                    },
                    "fight": {
                        "speaker": "",
                        "text": "Grak raises his massive club. The fight begins!",
                        "on_enter": [
                            {"action": "set_flag", "flag": "choice.grak_killed", "value": True},
                        ],
                        "end": True,
                    },
                },
            },
        },
    ],

    # ─────────────────────────────────────────────────────────
    #  ELDER THERON — Woodhaven (Keeper of the Grove)
    # ─────────────────────────────────────────────────────────
    "elder_theron": [
        # After learning about the Fading
        {
            "conditions": [
                {"flag": "lore.fading_basics", "op": "==", "value": True},
                {"flag": "npc.elder_theron.met", "op": "not_exists"},
            ],
            "tree": {
                "id": "theron_fading",
                "nodes": {
                    "start": {
                        "speaker": "Elder Theron",
                        "text": "You carry the weight of knowledge, I see. The Fading — yes, "
                                "we feel it here too. The grove is dying. Trees that stood for "
                                "a thousand years are dissolving like mist.",
                        "on_enter": [{"action": "meet_npc", "npc": "elder_theron"}],
                        "choices": [
                            {"text": "Can the grove be saved?", "next": "grove"},
                            {"text": "What do you know about the Wardens?", "next": "wardens"},
                            {"text": "We're looking for Hearthstones.", "next": "stones"},
                        ],
                    },
                    "grove": {
                        "speaker": "Elder Theron",
                        "text": "The grove is connected to the wards — it draws power from the same "
                                "source. If you restore the Hearthstones, the grove will heal. "
                                "If you fail... there will be nothing left to heal.",
                        "end": True,
                    },
                    "wardens": {
                        "speaker": "Elder Theron",
                        "text": "My grandmother spoke of them. She said they walked among us "
                                "like ordinary folk, but they could feel the boundaries of the world. "
                                "When they vanished, we thought the danger had passed. We were wrong.",
                        "end": True,
                    },
                    "stones": {
                        "speaker": "Elder Theron",
                        "text": "Hearthstones... the old word is 'ancorae' — anchors. "
                                "I know of one. The Spider's Nest to the south — something "
                                "powerful pulses at its heart. The spiders guard it fiercely. "
                                "Perhaps that is why they've grown so large.",
                        "on_enter": [{"action": "start_quest", "quest": "main_spiders_nest"}],
                        "end": True,
                    },
                },
            },
        },
        # Default
        {
            "conditions": [],
            "tree": {
                "id": "theron_default",
                "nodes": {
                    "start": {
                        "speaker": "Elder Theron",
                        "text": "Welcome to Woodhaven. The grove provides shelter, but "
                                "these are troubled times. How may I help you?",
                        "on_enter": [{"action": "meet_npc", "npc": "elder_theron"}],
                        "choices": [
                            {"text": "Tell me about Woodhaven.", "next": "about"},
                            {"text": "Goodbye.", "next": "bye"},
                        ],
                    },
                    "about": {
                        "speaker": "Elder Theron",
                        "text": "Woodhaven has stood in the shadow of the Great Grove for "
                                "generations. The trees protect us. But lately, even the oldest "
                                "oaks seem... tired. As if the world itself is exhausted.",
                        "end": True,
                    },
                    "bye": {
                        "speaker": "Elder Theron",
                        "text": "Walk gently. The forest remembers those who respect it.",
                        "end": True,
                    },
                },
            },
        },
    ],

    # ─────────────────────────────────────────────────────────
    #  SYLLA — Woodhaven Herbalist
    # ─────────────────────────────────────────────────────────
    "sylla": [
        {
            "conditions": [],
            "tree": {
                "id": "sylla_default",
                "nodes": {
                    "start": {
                        "speaker": "Sylla",
                        "text": "Ah, adventurers! You look like you could use a poultice. "
                                "Or three. Come in, come in — mind the drying herbs.",
                        "on_enter": [{"action": "meet_npc", "npc": "sylla"}],
                        "choices": [
                            {"text": "What herbs do you work with?", "next": "herbs"},
                            {"text": "Have you noticed anything strange?", "next": "strange"},
                            {"text": "Just browsing.", "next": "bye"},
                        ],
                    },
                    "herbs": {
                        "speaker": "Sylla",
                        "text": "Everything the grove provides! Moonpetal for healing, "
                                "thornroot for poisons, silverbark for wards. Though lately "
                                "the moonpetal blooms have been... wrong. Grey instead of silver. "
                                "They still work, but they taste of ash.",
                        "end": True,
                    },
                    "strange": {
                        "speaker": "Sylla",
                        "text": "Strange? Ha! Everything is strange. My garden phases in and out "
                                "some mornings — I can see right through my tomatoes to the ground "
                                "below. Elder Theron says it's the Fading. I say it's deeply unsettling "
                                "is what it is.",
                        "end": True,
                    },
                    "bye": {
                        "speaker": "Sylla",
                        "text": "Take care out there. And eat something green occasionally!",
                        "end": True,
                    },
                },
            },
        },
    ],

    # ─────────────────────────────────────────────────────────
    #  FORGEMASTER DUNN — Ironhearth
    # ─────────────────────────────────────────────────────────
    "forgemaster_dunn": [
        # After finding Dwarven Inscription in Abandoned Mine
        {
            "conditions": [
                {"flag": "quest.main_hearthstone_1.state", "op": ">", "value": 0},
                {"flag": "npc.forgemaster_dunn.met", "op": "not_exists"},
            ],
            "tree": {
                "id": "dunn_hearthstone",
                "nodes": {
                    "start": {
                        "speaker": "Forgemaster Dunn",
                        "text": "Hold. I know that look — you've been in the old mine. "
                                "My grandfather worked those tunnels before they sealed them. "
                                "Said there was something down there that wasn't ore.",
                        "on_enter": [{"action": "meet_npc", "npc": "forgemaster_dunn"}],
                        "choices": [
                            {"text": "There are Warden runes in the mine.", "next": "runes"},
                            {"text": "We're looking for a Hearthstone.", "next": "stone"},
                            {"text": "Just here for supplies.", "next": "bye"},
                        ],
                    },
                    "runes": {
                        "speaker": "Forgemaster Dunn",
                        "text": "Warden runes! Grandfather said the same. The dwarves who built "
                                "those tunnels were partners with the Wardens — they forged the "
                                "casings for the Hearthstones. Runesteel, they called it. I still "
                                "have a few ingots if you ever need something... special... forged.",
                        "end": True,
                    },
                    "stone": {
                        "speaker": "Forgemaster Dunn",
                        "text": "A Hearthstone? Down in my mine? Well. That explains why the "
                                "deepest tunnels never collapsed, even when everything else did. "
                                "There's a vault at the bottom — grandfather said it needed Warden "
                                "blood to open. Looks like you're the right people for the job.",
                        "end": True,
                    },
                    "bye": {
                        "speaker": "Forgemaster Dunn",
                        "text": "Everything I sell is Ironhearth quality. No refunds.",
                        "end": True,
                    },
                },
            },
        },
        # Default
        {
            "conditions": [],
            "tree": {
                "id": "dunn_default",
                "nodes": {
                    "start": {
                        "speaker": "Forgemaster Dunn",
                        "text": "Welcome to the forge. I make the finest steel in Aldenmere. "
                                "What do you need?",
                        "on_enter": [{"action": "meet_npc", "npc": "forgemaster_dunn"}],
                        "choices": [
                            {"text": "Tell me about Ironhearth.", "next": "about"},
                            {"text": "How's business?", "next": "business"},
                            {"text": "Goodbye.", "next": "bye"},
                        ],
                    },
                    "about": {
                        "speaker": "Forgemaster Dunn",
                        "text": "Built on iron and stubbornness. The mines run deep under the "
                                "mountains. We've been forging here since before the old kingdom "
                                "fell. Good people. Hard workers. Lately though, the ore comes up "
                                "brittle. Grey. Like the life's been sucked out of it.",
                        "end": True,
                    },
                    "business": {
                        "speaker": "Forgemaster Dunn",
                        "text": "Terrible, if you want the truth. The ore quality's dropped off "
                                "a cliff. I can still make decent steel, but I'm working twice as "
                                "hard for half the output. Something's wrong underground. "
                                "Something deeper than mining can reach.",
                        "end": True,
                    },
                    "bye": {
                        "speaker": "Forgemaster Dunn",
                        "text": "Stay sharp. Literally.",
                        "end": True,
                    },
                },
            },
        },
    ],

    # ─────────────────────────────────────────────────────────
    #  KIRA — Traveling Merchant, Ironhearth
    # ─────────────────────────────────────────────────────────
    "merchant_kira": [
        {
            "conditions": [],
            "tree": {
                "id": "kira_default",
                "nodes": {
                    "start": {
                        "speaker": "Kira",
                        "text": "Well met, travelers! Kira's Curiosities, at your service. "
                                "I deal in the rare, the unusual, and the occasionally cursed. "
                                "What catches your eye?",
                        "on_enter": [{"action": "meet_npc", "npc": "merchant_kira"}],
                        "choices": [
                            {"text": "Where do you travel?", "next": "travel"},
                            {"text": "Any news from the road?", "next": "news"},
                            {"text": "Just looking.", "next": "bye"},
                        ],
                    },
                    "travel": {
                        "speaker": "Kira",
                        "text": "Everywhere and nowhere, as they say. Briarhollow, Woodhaven, "
                                "Ironhearth, and sometimes east to the ports — though the "
                                "eastern roads have been... unpredictable lately. I lost an "
                                "entire cart last month. Not stolen. Just gone. The road "
                                "it was on vanished overnight.",
                        "end": True,
                    },
                    "news": {
                        "speaker": "Kira",
                        "text": "The roads are dangerous, and I don't mean bandits. Whole "
                                "stretches disappear and reappear. A merchant I know walked "
                                "into a fog bank and came out three days later, convinced only "
                                "minutes had passed. The world is coming apart at the seams, "
                                "and nobody in charge seems to care.",
                        "end": True,
                    },
                    "bye": {
                        "speaker": "Kira",
                        "text": "Come back when you have coin! Or a good story. I accept both.",
                        "end": True,
                    },
                },
            },
        },
    ],

    # ─────────────────────────────────────────────────────────
    #  SCOUT FERYN — Greenwood, forest warden
    # ─────────────────────────────────────────────────────────
    "scout_feryn": [
        {
            "conditions": [],
            "tree": {
                "id": "scout_feryn_default",
                "nodes": {
                    "start": {
                        "speaker": "Scout Feryn",
                        "text": "You made it out here in one piece. That already puts you ahead of most. "
                                "These woods aren't safe — haven't been for months. "
                                "Something is killing the animals. Not hunters. Something else.",
                        "on_enter": [{"action": "meet_npc", "npc": "scout_feryn"}],
                        "choices": [
                            {"text": "What kind of something?", "next": "threat"},
                            {"text": "We're looking for work.", "next": "work"},
                            {"text": "Just passing through.", "next": "bye"},
                        ],
                    },
                    "threat": {
                        "speaker": "Scout Feryn",
                        "text": "Shadow-touched beasts. Animals that should be dead — still moving, "
                                "eyes black as coal. We've lost two wardens to them already. "
                                "Whatever's doing this is coming from the east. From the Fading zones.",
                        "next": "work",
                    },
                    "work": {
                        "speaker": "Scout Feryn",
                        "text": "The outpost pays for information. If you scout the eastern border "
                                "and come back alive, we'll make it worth your while. "
                                "Talk to the warden on duty if you want official work.",
                        "end": True,
                    },
                    "bye": {
                        "speaker": "Scout Feryn",
                        "text": "Watch the eastern tree line. And don't travel after dark.",
                        "end": True,
                    },
                },
            },
        },
    ],

    # ─────────────────────────────────────────────────────────
    #  GUILDMASTER SABLE — Saltmere, Thieves' Guild
    # ─────────────────────────────────────────────────────────
    "guildmaster_sable": [
        # After party has proven themselves (Act 2)
        {
            "conditions": [
                {"flag": "npc.guildmaster_sable.met", "op": "==", "value": True},
                {"flag": "lore.fading_basics", "op": "==", "value": True},
            ],
            "tree": {
                "id": "sable_act2",
                "nodes": {
                    "start": {
                        "speaker": "Guildmaster Sable",
                        "text": "You've been busy. Word travels, even out here. "
                                "The Governor's agents are asking questions about you. "
                                "That means you're either doing something important, "
                                "or something stupid. I'm betting on the former.",
                        "choices": [
                            {"text": "We need passage to the eastern islands.", "next": "passage"},
                            {"text": "What do the Governor's agents want?", "next": "governor"},
                            {"text": "Just browsing.", "next": "bye"},
                        ],
                    },
                    "passage": {
                        "speaker": "Guildmaster Sable",
                        "text": "Dragon's Tooth? That's a death run. I'll arrange it — "
                                "but you'll owe the Guild a favor. Real currency around here.",
                        "on_enter": [{"action": "set_flag", "flag": "quest.dragons_tooth.passage_offered", "value": True}],
                        "end": True,
                    },
                    "governor": {
                        "speaker": "Guildmaster Sable",
                        "text": "They want to know about the Hearthstones. The Governor knows "
                                "more than he admits. He's been sitting on old Warden records "
                                "for years. If you need them, the castle archive isn't as "
                                "secure as it looks.",
                        "on_enter": [{"action": "discover_lore", "lore": "governor_knowledge"}],
                        "end": True,
                    },
                    "bye": {
                        "speaker": "Guildmaster Sable",
                        "text": "Door's always open. For the right price.",
                        "end": True,
                    },
                },
            },
        },
        # First meeting
        {
            "conditions": [
                {"flag": "npc.guildmaster_sable.met", "op": "not_exists"},
            ],
            "tree": {
                "id": "sable_intro",
                "nodes": {
                    "start": {
                        "speaker": "Guildmaster Sable",
                        "text": "New faces. In Saltmere, that's either opportunity or trouble. "
                                "I prefer to decide which before you leave.",
                        "on_enter": [{"action": "meet_npc", "npc": "guildmaster_sable"}],
                        "choices": [
                            {"text": "We're adventurers. Looking for work.", "next": "work"},
                            {"text": "We heard about your Guild.", "next": "guild"},
                            {"text": "Just browsing.", "next": "bye"},
                        ],
                    },
                    "work": {
                        "speaker": "Guildmaster Sable",
                        "text": "Adventurers. Right. We have uses for people who can handle "
                                "themselves. Come back when you've proved you're worth the trouble. "
                                "Ask around town. Show me what you can do.",
                        "end": True,
                    },
                    "guild": {
                        "speaker": "Guildmaster Sable",
                        "text": "Then you know we don't advertise. What you see here is a "
                                "trading post. What happens in the back room is private commerce. "
                                "Any questions?",
                        "end": True,
                    },
                    "bye": {
                        "speaker": "Guildmaster Sable",
                        "text": "Mm. Come back if you change your mind.",
                        "end": True,
                    },
                },
            },
        },
        # Default
        {
            "conditions": [],
            "tree": {
                "id": "sable_default",
                "nodes": {
                    "start": {
                        "speaker": "Guildmaster Sable",
                        "text": "The Guild remembers its debts. Both kinds.",
                        "choices": [
                            {"text": "Do you have work for us?", "next": "work"},
                            {"text": "We need information.", "next": "info"},
                            {"text": "Goodbye.", "next": "bye"},
                        ],
                    },
                    "work": {
                        "speaker": "Guildmaster Sable",
                        "text": "Check the job board. Anything sensitive comes through me directly — "
                                "and those jobs don't get posted publicly.",
                        "end": True,
                    },
                    "info": {
                        "speaker": "Guildmaster Sable",
                        "text": "Information costs. What do you want to know, and what are you "
                                "willing to pay?",
                        "end": True,
                    },
                    "bye": {
                        "speaker": "Guildmaster Sable",
                        "text": "Watch the harbor. Interesting things wash ashore.",
                        "end": True,
                    },
                },
            },
        },
    ],

    # ─────────────────────────────────────────────────────────
    #  TIDE PRIEST ORAN — Saltmere shrine
    # ─────────────────────────────────────────────────────────
    "tide_priest_oran": [
        {
            "conditions": [],
            "tree": {
                "id": "oran_default",
                "nodes": {
                    "start": {
                        "speaker": "Tide Priest Oran",
                        "text": "The tides have been wrong for months. Coming in at the wrong hour. "
                                "Going out too far. The sea feels... thin. Like it's forgetting "
                                "what it is. I pray every dawn. I don't know if anyone is listening.",
                        "on_enter": [{"action": "meet_npc", "npc": "tide_priest_oran"}],
                        "choices": [
                            {"text": "What god do you pray to?", "next": "faith"},
                            {"text": "Have you heard of the Fading?", "next": "fading"},
                            {"text": "Can you heal us?", "next": "healing"},
                        ],
                    },
                    "faith": {
                        "speaker": "Tide Priest Oran",
                        "text": "The Tides. Not a god by name — a force. The eternal rhythm. "
                                "Life, death, the pull of the moon. When the tides are wrong, "
                                "the whole world is wrong. I feel it in my bones.",
                        "end": True,
                    },
                    "fading": {
                        "speaker": "Tide Priest Oran",
                        "text": "I've watched three fishing boats sail out and not return. "
                                "No storm. No wreck found. Just... gone. The Fading doesn't "
                                "only take land. It takes sea too. Be careful out there.",
                        "on_enter": [{"action": "set_flag", "flag": "lore.fading_sea", "value": True}],
                        "end": True,
                    },
                    "healing": {
                        "speaker": "Tide Priest Oran",
                        "text": "The shrine heals those who need it. Go — I'll ask the Tides "
                                "to be kind to you.",
                        "end": True,
                    },
                },
            },
        },
    ],

    # ─────────────────────────────────────────────────────────
    #  HIGH PRIEST ALDARA — Sanctum, grand cathedral
    # ─────────────────────────────────────────────────────────
    "high_priest_aldara": [
        # After party learns about the Fading
        {
            "conditions": [
                {"flag": "lore.fading_basics", "op": "==", "value": True},
                {"flag": "npc.high_priest_aldara.met", "op": "==", "value": True},
            ],
            "tree": {
                "id": "aldara_fading",
                "nodes": {
                    "start": {
                        "speaker": "High Priest Aldara",
                        "text": "You've learned the truth of the Fading. Good. Denial is a luxury "
                                "we can no longer afford. The Cathedral has records you should see — "
                                "accounts from the last time the wards nearly failed, three centuries ago. "
                                "The Wardens stopped it then. We must hope they can again.",
                        "choices": [
                            {"text": "What do the records say?", "next": "records"},
                            {"text": "Can the Cathedral help us?", "next": "help"},
                            {"text": "Thank you.", "next": "bye"},
                        ],
                    },
                    "records": {
                        "speaker": "High Priest Aldara",
                        "text": "That the Hearthstones were not merely artifacts — they were promises. "
                                "Each one placed by a Warden who swore their bloodline would protect it. "
                                "When the last Warden of a bloodline dies, the stone begins to drift. "
                                "That is what has been happening. Bloodlines dying. Promises breaking.",
                        "on_enter": [{"action": "discover_lore", "lore": "hearthstone_bloodlines"}],
                        "end": True,
                    },
                    "help": {
                        "speaker": "High Priest Aldara",
                        "text": "We can consecrate your weapons against shadow-touched creatures. "
                                "We can heal your wounds and restore your spirit. What we cannot do "
                                "is fight this battle for you. That burden falls on those with Warden blood.",
                        "end": True,
                    },
                    "bye": {
                        "speaker": "High Priest Aldara",
                        "text": "Light guide your steps into the dark.",
                        "end": True,
                    },
                },
            },
        },
        # First meeting
        {
            "conditions": [
                {"flag": "npc.high_priest_aldara.met", "op": "not_exists"},
            ],
            "tree": {
                "id": "aldara_intro",
                "nodes": {
                    "start": {
                        "speaker": "High Priest Aldara",
                        "text": "Travelers in Sanctum are always welcome, whatever their faith. "
                                "I am Aldara. I have served this Cathedral for forty years. "
                                "Something tells me you are not here for pilgrimage.",
                        "on_enter": [{"action": "meet_npc", "npc": "high_priest_aldara"}],
                        "choices": [
                            {"text": "We're looking for information about the Fading.", "next": "fading"},
                            {"text": "We need healing.", "next": "healing"},
                            {"text": "We're just passing through.", "next": "passing"},
                        ],
                    },
                    "fading": {
                        "speaker": "High Priest Aldara",
                        "text": "Then you already know more than most. Come back when you've "
                                "learned what you're truly up against. The Cathedral's archives "
                                "will be open to you.",
                        "on_enter": [{"action": "set_flag", "flag": "lore.sanctum_archives", "value": True}],
                        "end": True,
                    },
                    "healing": {
                        "speaker": "High Priest Aldara",
                        "text": "The shrine is always open. You need only ask.",
                        "end": True,
                    },
                    "passing": {
                        "speaker": "High Priest Aldara",
                        "text": "No one passes through Sanctum by accident. Rest, restore yourselves. "
                                "Whatever you're carrying, you needn't carry it alone.",
                        "end": True,
                    },
                },
            },
        },
        # Default
        {
            "conditions": [],
            "tree": {
                "id": "aldara_default",
                "nodes": {
                    "start": {
                        "speaker": "High Priest Aldara",
                        "text": "The light of the Cathedral is always here when you need it.",
                        "choices": [
                            {"text": "What have you heard from other pilgrims?", "next": "rumors"},
                            {"text": "Farewell.", "next": "bye"},
                        ],
                    },
                    "rumors": {
                        "speaker": "High Priest Aldara",
                        "text": "That entire villages are vanishing in the east. That the Governor "
                                "in Thornhaven knows more than he says. That a woman named Maren "
                                "has been asking about the old Warden bloodlines.",
                        "end": True,
                    },
                    "bye": {
                        "speaker": "High Priest Aldara",
                        "text": "Go with light.",
                        "end": True,
                    },
                },
            },
        },
    ],

    # ─────────────────────────────────────────────────────────
    #  ARCHMAGE SOLEN — Crystalspire
    # ─────────────────────────────────────────────────────────
    "archmage_solen": [
        # After hearthstone 1 found
        {
            "conditions": [
                {"flag": "quest.main_hearthstone_1.state", "op": "==", "value": -2},
                {"flag": "npc.archmage_solen.met", "op": "==", "value": True},
            ],
            "tree": {
                "id": "solen_hearthstone",
                "nodes": {
                    "start": {
                        "speaker": "Archmage Solen",
                        "text": "You found the first stone. Remarkable. I have spent forty years "
                                "studying these artifacts and never held one. The resonance signature "
                                "is extraordinary — pure ward-magic, undiluted. The Academy's instruments "
                                "can help you locate the others.",
                        "choices": [
                            {"text": "Can you track the other stones?", "next": "track"},
                            {"text": "What do you know about Valdris?", "next": "valdris"},
                            {"text": "Thank you.", "next": "bye"},
                        ],
                    },
                    "track": {
                        "speaker": "Archmage Solen",
                        "text": "With the first stone as a reference, yes. The others emit a "
                                "harmonic echo. I'm detecting two strong signals — one from the "
                                "Sunken Crypt to the south, another from somewhere in the eastern "
                                "sea. The Dragon's Tooth archipelago, I believe.",
                        "on_enter": [
                            {"action": "set_flag", "flag": "lore.hearthstone_locations", "value": True},
                            {"action": "discover_lore", "lore": "hearthstone_locations"},
                        ],
                        "end": True,
                    },
                    "valdris": {
                        "speaker": "Archmage Solen",
                        "text": "Valdris was the greatest mage this Academy ever produced. "
                                "That is not pride — it is a warning. He believed the Shadow "
                                "Realm was not a threat but a resource. His experiments are what "
                                "weakened the wards. I was his student. I watched him cross the line. "
                                "I should have stopped him.",
                        "on_enter": [{"action": "discover_lore", "lore": "valdris_betrayal"}],
                        "end": True,
                    },
                    "bye": {
                        "speaker": "Archmage Solen",
                        "text": "The Academy's resources are at your disposal.",
                        "end": True,
                    },
                },
            },
        },
        # First meeting
        {
            "conditions": [
                {"flag": "npc.archmage_solen.met", "op": "not_exists"},
            ],
            "tree": {
                "id": "solen_intro",
                "nodes": {
                    "start": {
                        "speaker": "Archmage Solen",
                        "text": "Visitors to the Academy. Unusual. I am Solen — Archmage, "
                                "and currently the only person in this city taking the Fading "
                                "seriously enough to actually study it. What brings you here?",
                        "on_enter": [{"action": "meet_npc", "npc": "archmage_solen"}],
                        "choices": [
                            {"text": "We're looking into the Fading.", "next": "fading"},
                            {"text": "We need access to the teleport network.", "next": "teleport"},
                            {"text": "Just exploring.", "next": "exploring"},
                        ],
                    },
                    "fading": {
                        "speaker": "Archmage Solen",
                        "text": "Then we have something in common. The Academy's official position "
                                "is that the Fading is a 'temporary magical weather event.' "
                                "My position is that that is catastrophically wrong. "
                                "Come back when you have proof I can put in front of the Council.",
                        "end": True,
                    },
                    "teleport": {
                        "speaker": "Archmage Solen",
                        "text": "Guild membership required. Alternatively, significant contribution "
                                "to Academy research. The circle is not free — the ley lines that "
                                "power it are weakening with the Fading. Every jump costs real energy.",
                        "end": True,
                    },
                    "exploring": {
                        "speaker": "Archmage Solen",
                        "text": "Crystalspire is worth exploring. Try not to touch anything "
                                "that's glowing without asking first.",
                        "end": True,
                    },
                },
            },
        },
        # Default
        {
            "conditions": [],
            "tree": {
                "id": "solen_default",
                "nodes": {
                    "start": {
                        "speaker": "Archmage Solen",
                        "text": "The ley line readings are worse today than yesterday. "
                                "They have been for months. What can I do for you?",
                        "choices": [
                            {"text": "What's the latest from the Academy?", "next": "research"},
                            {"text": "Goodbye.", "next": "bye"},
                        ],
                    },
                    "research": {
                        "speaker": "Archmage Solen",
                        "text": "We've confirmed that the Fading accelerates near Hearthstone "
                                "anchor points that are undefended. Whatever is driving it is "
                                "intelligent. It targets weakness. Find those stones.",
                        "end": True,
                    },
                    "bye": {
                        "speaker": "Archmage Solen",
                        "text": "Measure twice. The shadow doesn't give second chances.",
                        "end": True,
                    },
                },
            },
        },
    ],

    # ─────────────────────────────────────────────────────────
    #  TELEPORT MASTER VAEN — Crystalspire circle
    # ─────────────────────────────────────────────────────────
    "teleport_master": [
        {
            "conditions": [],
            "tree": {
                "id": "vaen_default",
                "nodes": {
                    "start": {
                        "speaker": "Teleport Master Vaen",
                        "text": "The circle is operational. I maintain it personally — "
                                "not the Academy, not the Guild. Me. If it fails, people die "
                                "mid-transit. So I take the work seriously.",
                        "on_enter": [{"action": "meet_npc", "npc": "teleport_master"}],
                        "choices": [
                            {"text": "How does the teleport network work?", "next": "explain"},
                            {"text": "Where can we travel from here?", "next": "destinations"},
                            {"text": "We'd like to travel.", "next": "travel"},
                        ],
                    },
                    "explain": {
                        "speaker": "Teleport Master Vaen",
                        "text": "The circles draw from the ley lines beneath the ground. "
                                "You step in, fix a destination in mind that you've previously "
                                "attuned to, and the network does the rest. The ley lines have been "
                                "weakening — the Fading is eating them. Some circles have gone dark permanently.",
                        "end": True,
                    },
                    "destinations": {
                        "speaker": "Teleport Master Vaen",
                        "text": "From Crystalspire you can reach Briarhollow, Woodhaven, Ironhearth, "
                                "and Sanctum — provided you've attuned to their circles. "
                                "Thornhaven's circle is still active but restricted. "
                                "Governor's orders.",
                        "end": True,
                    },
                    "travel": {
                        "speaker": "Teleport Master Vaen",
                        "text": "Fifty gold per person, per jump. Attunement to the destination "
                                "circle required — you must have stood in that circle before. "
                                "Ready when you are.",
                        "end": True,
                    },
                },
            },
        },
    ],

    # ─────────────────────────────────────────────────────────
    #  GOVERNOR ALDRIC — Thornhaven capital, Iron tier
    # ─────────────────────────────────────────────────────────
    "governor_aldric": [
        # After party has all 5 hearthstones (endgame)
        {
            "conditions": [
                {"flag": "quest.main_hearthstone_5.state", "op": "==", "value": -2},
            ],
            "tree": {
                "id": "governor_endgame",
                "nodes": {
                    "start": {
                        "speaker": "Governor Aldric",
                        "text": "You've done it. I doubted you — I will admit that freely. "
                                "The Empire has watched the Wardens fail before. I had no reason "
                                "to believe this generation would be different. I was wrong. "
                                "What do you need from me?",
                        "choices": [
                            {"text": "We need the castle's archives.", "next": "archives"},
                            {"text": "We need imperial soldiers.", "next": "soldiers"},
                            {"text": "Just your blessing.", "next": "blessing"},
                        ],
                    },
                    "archives": {
                        "speaker": "Governor Aldric",
                        "text": "Done. Every Warden record we have — and there are more than "
                                "you might expect. The Empire has been quietly preparing for "
                                "this possibility for a long time.",
                        "on_enter": [{"action": "set_flag", "flag": "lore.imperial_archives_unlocked", "value": True}],
                        "end": True,
                    },
                    "soldiers": {
                        "speaker": "Governor Aldric",
                        "text": "Against shadow-touched creatures? My soldiers would be slaughtered. "
                                "Bronze-tier warriors against whatever is driving the Fading — "
                                "I won't throw their lives away. But I'll secure the roads and "
                                "keep the population safe. You handle the source.",
                        "end": True,
                    },
                    "blessing": {
                        "speaker": "Governor Aldric",
                        "text": "You have it. And more than that — you have my respect. "
                                "Which, in this empire, is not nothing.",
                        "end": True,
                    },
                },
            },
        },
        # First meeting — cautious, politically careful
        {
            "conditions": [
                {"flag": "npc.governor_aldric.met", "op": "not_exists"},
            ],
            "tree": {
                "id": "governor_intro",
                "nodes": {
                    "start": {
                        "speaker": "Governor Aldric",
                        "text": "Adventurers in my court. An unusual occurrence. I am told "
                                "you have been asking questions about the Fading across the realm. "
                                "I find that... interesting. Tell me — what have you learned?",
                        "on_enter": [{"action": "meet_npc", "npc": "governor_aldric"}],
                        "choices": [
                            {"text": "The Hearthstones are the key to stopping it.", "next": "hearthstones"},
                            {"text": "We know you have Warden records.", "next": "records"},
                            {"text": "We're still investigating.", "next": "cautious"},
                        ],
                    },
                    "hearthstones": {
                        "speaker": "Governor Aldric",
                        "text": "Yes. The Empire has known about the Hearthstones for some time. "
                                "The Emperor's stance has been non-intervention — the Wardens "
                                "made their choices. I have been less certain that policy is wise. "
                                "What do you need?",
                        "next": "what_need",
                    },
                    "records": {
                        "speaker": "Governor Aldric",
                        "text": "Someone has been talking. Yes, we have records. Old ones. "
                                "The Empire keeps everything. I am not certain you have earned "
                                "access yet. Show me you can be trusted with what you already know.",
                        "end": True,
                    },
                    "cautious": {
                        "speaker": "Governor Aldric",
                        "text": "Honest, at least. Come back when you have more. "
                                "The Empire does not act on maybes.",
                        "end": True,
                    },
                    "what_need": {
                        "speaker": "Governor Aldric",
                        "text": "The castle archives contain records of every Warden bloodline "
                                "that swore fealty to the Empire. They are yours — on one condition. "
                                "Recover the Hearthstones. All of them. Whatever it takes.",
                        "on_enter": [
                            {"action": "set_flag", "flag": "lore.governor_alliance", "value": True},
                            {"action": "discover_lore", "lore": "imperial_hearthstone_records"},
                        ],
                        "end": True,
                    },
                },
            },
        },
        # Default
        {
            "conditions": [],
            "tree": {
                "id": "governor_default",
                "nodes": {
                    "start": {
                        "speaker": "Governor Aldric",
                        "text": "The situation in the eastern provinces worsens daily. "
                                "I hope your work is producing results.",
                        "choices": [
                            {"text": "We're making progress.", "next": "progress"},
                            {"text": "We need access to the archives.", "next": "archives"},
                            {"text": "Goodbye.", "next": "bye"},
                        ],
                    },
                    "progress": {
                        "speaker": "Governor Aldric",
                        "text": "Good. The Empire watches, and waits. Do not take too long.",
                        "end": True,
                    },
                    "archives": {
                        "speaker": "Governor Aldric",
                        "text": "Earn it. Bring me a Hearthstone — even one — and the archives "
                                "open. That is the deal.",
                        "end": True,
                    },
                    "bye": {
                        "speaker": "Governor Aldric",
                        "text": "Walk carefully, Warden.",
                        "end": True,
                    },
                },
            },
        },
    ],

    # ─────────────────────────────────────────────────────────
    #  GUILD COMMANDER VAREK — Thornhaven adventurers' guild
    # ─────────────────────────────────────────────────────────
    "guild_commander_varek": [
        {
            "conditions": [],
            "tree": {
                "id": "varek_default",
                "nodes": {
                    "start": {
                        "speaker": "Commander Varek",
                        "text": "Adventurers registered with the Imperial Guild get access to "
                                "better contracts, better pay, and the Empire's legal protection. "
                                "In exchange, you follow our codes and don't embarrass the crown. "
                                "Interested?",
                        "on_enter": [{"action": "meet_npc", "npc": "guild_commander_varek"}],
                        "choices": [
                            {"text": "Tell us about the best available contracts.", "next": "contracts"},
                            {"text": "What's the situation in the eastern provinces?", "next": "east"},
                            {"text": "Not right now.", "next": "bye"},
                        ],
                    },
                    "contracts": {
                        "speaker": "Commander Varek",
                        "text": "The high-value work right now is in the east — Fading recovery "
                                "operations, escort jobs through corrupted zones, creature culling. "
                                "Pays triple what frontier work does. Also three times the chance "
                                "you don't come back.",
                        "end": True,
                    },
                    "east": {
                        "speaker": "Commander Varek",
                        "text": "Three villages gone in the last month. No bodies, no debris. "
                                "Just empty land. I've sent twelve scouting parties. Four returned. "
                                "The Fading isn't just growing — it's accelerating.",
                        "end": True,
                    },
                    "bye": {
                        "speaker": "Commander Varek",
                        "text": "The door's open when you're ready.",
                        "end": True,
                    },
                },
            },
        },
    ],

    # ─────────────────────────────────────────────────────────
    #  COURT MAGE SIRA — Thornhaven, Maren's Act II reveal
    # ─────────────────────────────────────────────────────────
    "court_mage_sira": [
        # The Maren reveal — she is Valdris's daughter
        {
            "conditions": [
                {"flag": "quest.main_hearthstone_1.state", "op": "==", "value": -2},
                {"flag": "npc.court_mage_sira.met", "op": "==", "value": True},
                {"flag": "lore.maren_origin", "op": "not_exists"},
            ],
            "tree": {
                "id": "sira_maren_reveal",
                "nodes": {
                    "start": {
                        "speaker": "Court Mage Sira",
                        "text": "I've been waiting for the right moment to tell you something. "
                                "The scholar you've been working with — Maren. "
                                "I know her real name.",
                        "choices": [
                            {"text": "Tell us.", "next": "reveal"},
                            {"text": "What do you mean, her real name?", "next": "reveal"},
                        ],
                    },
                    "reveal": {
                        "speaker": "Court Mage Sira",
                        "text": "Maren Valdris. Daughter of the Traitor Warden. "
                                "She has been searching for the Hearthstones since she was a child — "
                                "but not, I fear, to restore the wards as they were. "
                                "Her father's ritual was incomplete. She means to finish it.",
                        "on_enter": [{"action": "discover_lore", "lore": "maren_origin"}],
                        "next": "question",
                    },
                    "question": {
                        "speaker": "Court Mage Sira",
                        "text": "Whether that means saving the world or consuming it — "
                                "I genuinely don't know. Valdris believed he was saving it too. "
                                "I thought you should have this information before you hand her "
                                "the second stone.",
                        "on_enter": [{"action": "set_flag", "flag": "lore.maren_revealed", "value": True}],
                        "end": True,
                    },
                },
            },
        },
        # First meeting
        {
            "conditions": [
                {"flag": "npc.court_mage_sira.met", "op": "not_exists"},
            ],
            "tree": {
                "id": "sira_intro",
                "nodes": {
                    "start": {
                        "speaker": "Court Mage Sira",
                        "text": "Court Mage — the title sounds grander than the reality. "
                                "I advise the Governor on magical matters. Mostly I sit in this "
                                "tower and watch the ley line readings get worse. "
                                "You're the Warden-blooded party, aren't you?",
                        "on_enter": [{"action": "meet_npc", "npc": "court_mage_sira"}],
                        "choices": [
                            {"text": "How do you know about us?", "next": "knows"},
                            {"text": "What have you learned about the Fading?", "next": "fading"},
                            {"text": "Just visiting.", "next": "bye"},
                        ],
                    },
                    "knows": {
                        "speaker": "Court Mage Sira",
                        "text": "The ley lines carry information as well as power. When someone "
                                "with Warden blood touches a Hearthstone, it resonates across the "
                                "entire network. I felt you find the first stone. So did Archmage Solen. "
                                "So, I suspect, did Maren.",
                        "end": True,
                    },
                    "fading": {
                        "speaker": "Court Mage Sira",
                        "text": "That something is driving it. It is not simply entropy — "
                                "there is intention behind the pattern of which areas Fade first. "
                                "Always the areas with old Warden presence. Always the anchor points. "
                                "Whatever is out there wants the wards down.",
                        "on_enter": [{"action": "discover_lore", "lore": "fading_intention"}],
                        "end": True,
                    },
                    "bye": {
                        "speaker": "Court Mage Sira",
                        "text": "Come back. I have a feeling we'll have more to discuss.",
                        "end": True,
                    },
                },
            },
        },
        # Default
        {
            "conditions": [],
            "tree": {
                "id": "sira_default",
                "nodes": {
                    "start": {
                        "speaker": "Court Mage Sira",
                        "text": "The readings are worse today. I say that every day now, "
                                "and every day it's true.",
                        "choices": [
                            {"text": "What are you tracking?", "next": "tracking"},
                            {"text": "Goodbye.", "next": "bye"},
                        ],
                    },
                    "tracking": {
                        "speaker": "Court Mage Sira",
                        "text": "The integrity of the barrier between worlds. Currently at "
                                "roughly forty percent of its original strength, down from seventy "
                                "when I started measuring three years ago. At this rate, full "
                                "collapse in eighteen months. Maybe less.",
                        "end": True,
                    },
                    "bye": {
                        "speaker": "Court Mage Sira",
                        "text": "Find those stones.",
                        "end": True,
                    },
                },
            },
        },
    ],

    # ─────────────────────────────────────────────────────────
    #  DOCKHAND RIV — Ship passage to Dragon's Tooth (Saltmere)
    # ─────────────────────────────────────────────────────────
    "dockhand_riv": [
        # Offers passage once Hearthstone 2 is collected
        {
            "conditions": [
                {"flag": "boss_defeated.sunken_crypt", "op": "==", "value": True},
                {"flag": "ship_passage.granted",       "op": "not_exists"},
            ],
            "tree": {
                "id": "riv_passage_offer",
                "nodes": {
                    "start": {
                        "speaker": "Dockhand Riv",
                        "text": "You're the ones people are talking about. The Warden-bloods.\n"
                                "I heard you came back from the Sunken Crypt. Alive, even.\n"
                                "I can get you to Dragon's Tooth if you want. I know the route — "
                                "the one that avoids the creature that circles the island.\n"
                                "Won't be cheap. Won't be safe either. But I'll get you there.",
                        "choices": [
                            {"text": "We need to get there. Book us passage.", "next": "booked"},
                            {"text": "What do you know about the island?",      "next": "island_info"},
                            {"text": "Not yet. We'll come back.",               "next": "later"},
                        ],
                    },
                    "island_info": {
                        "speaker": "Dockhand Riv",
                        "text": "Volcanic. Unstable. The Tiderunner went there eight years ago "
                                "and only two of the crew made it back. They said there was "
                                "something glowing at the center of the caldera — warm light, "
                                "not fire. And something enormous that protected it.\n"
                                "That's all I know. You still want to go?",
                        "choices": [
                            {"text": "Yes. Book us passage.", "next": "booked"},
                            {"text": "Not yet.",              "next": "later"},
                        ],
                    },
                    "booked": {
                        "speaker": "Dockhand Riv",
                        "text": "Right. I'll have the skiff ready. "
                                "She's small but she's fast. "
                                "Come find me at the dock when you're ready to leave.",
                        "on_enter": [
                            {"action": "set_flag", "flag": "ship_passage.granted", "value": True},
                        ],
                        "end": True,
                    },
                    "later": {
                        "speaker": "Dockhand Riv",
                        "text": "I'll be here. Don't take too long — "
                                "I've had other offers.",
                        "end": True,
                    },
                },
            },
        },
        # After passage granted — remind player
        {
            "conditions": [
                {"flag": "ship_passage.granted", "op": "==", "value": True},
                {"flag": "boss_defeated.dragons_tooth", "op": "not_exists"},
            ],
            "tree": {
                "id": "riv_passage_reminder",
                "nodes": {
                    "start": {
                        "speaker": "Dockhand Riv",
                        "text": "Skiff's ready when you are. Dragon's Tooth, whenever you want to go.\n"
                                "She'll be waiting at the eastern dock.",
                        "end": True,
                    },
                },
            },
        },
        # After Dragon's Tooth cleared
        {
            "conditions": [
                {"flag": "boss_defeated.dragons_tooth", "op": "==", "value": True},
            ],
            "tree": {
                "id": "riv_post_island",
                "nodes": {
                    "start": {
                        "speaker": "Dockhand Riv",
                        "text": "You came back. And you took something off that island.\n"
                                "I could feel it from the harbor. The air changed.\n"
                                "Whatever you're doing with these stones — I hope it works.",
                        "end": True,
                    },
                },
            },
        },
        # Default (too early)
        {
            "conditions": [],
            "tree": {
                "id": "riv_default",
                "nodes": {
                    "start": {
                        "speaker": "Dockhand Riv",
                        "text": "I run charters to the outer islands. "
                                "Nothing out there worth seeing right now, though.\n"
                                "Come back if that changes.",
                        "end": True,
                    },
                },
            },
        },
    ],

    # ─────────────────────────────────────────────────────────
    #  KARRETH — Boss of Dragon's Tooth (Act 2)
    # ─────────────────────────────────────────────────────────
    "karreth": [
        {
            "conditions": [
                {"flag": "boss.karreth.defeated", "op": "not_exists"},
            ],
            "tree": {
                "id": "karreth_confrontation",
                "nodes": {
                    "start": {
                        "speaker": "Karreth",
                        "text": "WARM THING. MINE. MINE SINCE BEFORE YOUR KIND WALKED.\n"
                                "The great head swings toward you. Twin fires burn in its eyes — "
                                "one orange-gold, natural and ancient. One a sickly grey-green, "
                                "wrong in a way you feel in your teeth.",
                        "choices": [
                            {"text": "We need what you're protecting. Stand aside.",   "next": "fight_direct"},
                            {"text": "We know what you are. What you were.",           "next": "lore_path",
                             "condition": {"flag": "lore.dragon_karreth", "op": "==", "value": True}},
                            {"text": "We're not here to fight you.",                   "next": "plea"},
                        ],
                    },
                    "plea": {
                        "speaker": "Karreth",
                        "text": "NOT. FIGHT.\n"
                                "The grey-green eye fixes on you. Something ancient and confused "
                                "moves behind it.\n"
                                "WARM THING CALLS DANGER. DANGER MUST DIE. THAT IS THE OATH.\n"
                                "The binding is too deep. It doesn't have a choice.",
                        "next": "fight_direct",
                    },
                    "fight_direct": {
                        "speaker": "Karreth",
                        "text": "OATH HOLDS.\n"
                                "The great wings unfurl. The chamber fills with heat.",
                        "end": True,
                    },
                    "lore_path": {
                        "speaker": "Karreth",
                        "text": "The grey-green eye narrows. Then something shifts — "
                                "a long, slow blink. When the eye opens again, the sickly light "
                                "is dimmer. The voice, when it comes, is quieter.\n"
                                "YOU. KNOW. WHAT I WAS.\n"
                                "BEFORE THE SICK THING CAME INTO ME.",
                        "next": "lore_conversation",
                    },
                    "lore_conversation": {
                        "speaker": "Karreth",
                        "text": "WAS. GUARDIAN. FIRST GUARDIAN. BEFORE YOUR WARDENS.\n"
                                "I REMEMBER... WARMTH. RIGHTNESS. THE STONES SANG.\n"
                                "NOW. ONLY PROTECT. CANNOT STOP. CANNOT REST.\n"
                                "It shudders. The grey-green eye pulses.\n"
                                "I AM. TIRED.",
                        "choices": [
                            {"text": "We can end this. Let us fight you. Be free.", "next": "karreth_release"},
                            {"text": "Is there another way?",                       "next": "no_other_way"},
                        ],
                    },
                    "no_other_way": {
                        "speaker": "Karreth",
                        "text": "NO OTHER WAY. BINDING TOO DEEP. TOO LONG.\n"
                                "DEFEAT. IS. RELEASE.\n"
                                "The second eye — the natural one — closes. "
                                "When it opens, something like peace is in it.\n"
                                "FIGHT. FREE ME.",
                        "next": "karreth_release",
                    },
                    "karreth_release": {
                        "speaker": "Karreth",
                        "text": "TAKE. THE STONE.\n"
                                "WHEN I AM GONE. GIVE IT. BACK. TO THE NETWORK.\n"
                                "TELL THEM. KARRETH. HELD. AS LONG. AS IT COULD.\n"
                                "The natural fire in both eyes burns brighter, briefly, "
                                "consuming the grey-green entirely.\n"
                                "Then it charges.",
                        "on_enter": [
                            {"action": "set_flag", "flag": "lore.karreth_freed", "value": True},
                        ],
                        "end": True,
                    },
                },
            },
        },
    ],

    # ─────────────────────────────────────────────────────────
    #  THE SUNKEN WARDEN — Boss of Sunken Crypt (Act 2)
    # ─────────────────────────────────────────────────────────
    "sunken_warden": [
        {
            "conditions": [
                {"flag": "boss.sunken_warden.defeated", "op": "not_exists"},
            ],
            "tree": {
                "id": "sunken_warden_boss",
                "nodes": {
                    "start": {
                        "speaker": "The Sunken Warden",
                        "text": "Warden blood. I can smell it from here. "
                                "How many centuries has it been? I have been waiting — "
                                "not by choice. The stone bound me here. "
                                "I cannot release it willingly. You understand what that means.",
                        "choices": [
                            {"text": "We need the stone. We're trying to restore the wards.", "next": "reason"},
                            {"text": "Step aside.", "next": "fight"},
                            {"text": "Who were you?", "next": "identity"},
                        ],
                    },
                    "identity": {
                        "speaker": "The Sunken Warden",
                        "text": "My name was Deren. I was Third Warden of the Western Coast, "
                                "two hundred and thirty years ago. I died defending this stone "
                                "from those who wanted to destroy it. Death was not the end. "
                                "I became the ward.",
                        "next": "reason",
                    },
                    "reason": {
                        "speaker": "The Sunken Warden",
                        "text": "I believe you. That is the tragedy. Every Warden who has come "
                                "for this stone has meant well. Valdris meant well. And yet. "
                                "The oath I swore cannot be reasoned with. I must guard until "
                                "I am defeated. That is the price of the binding. "
                                "Fight me. Take the stone. Complete what we started.",
                        "on_enter": [{"action": "set_flag", "flag": "lore.sunken_warden_truth", "value": True}],
                        "end": True,
                    },
                    "fight": {
                        "speaker": "The Sunken Warden",
                        "text": "Good. No more words. The stone calls for a worthy hand. "
                                "Prove yours.",
                        "end": True,
                    },
                },
            },
        },
    ],

    # ─────────────────────────────────────────────────────────
    #  VALDRIS — Final boss of Valdris Spire (Act 2/3)
    # ─────────────────────────────────────────────────────────
    "valdris": [
        {
            "conditions": [
                {"flag": "boss.valdris.defeated", "op": "not_exists"},
            ],
            "tree": {
                "id": "valdris_final",
                "nodes": {
                    "start": {
                        "speaker": "Valdris",
                        "text": "You made it all the way up.\n"
                                "And you brought my daughter's stones with you.\n"
                                "I wondered which of us she'd send to the top first.",
                        "choices": [
                            {"text": "Maren is with us. Against you.",
                             "next": "maren_with_party",
                             "condition": {"flag": "maren.fighting_with_party", "op": "==", "value": True}},
                            {"text": "You're the one who caused Ashenmoor.",
                             "next": "accuse"},
                            {"text": "What are you trying to do with the Hearthstones?",
                             "next": "plan"},
                            {"text": "We're not giving you anything.",
                             "next": "fight"},
                        ],
                    },
                    "maren_with_party": {
                        "speaker": "Valdris",
                        "text": "Ah.\n"
                                "She finally chose a side.\n"
                                "The silence stretches. Something moves in his face — "
                                "something that was a father, once.\n"
                                "Then it closes again.\n"
                                "That doesn't change what I have to do.",
                        "next": "plan",
                    },
                    "accuse": {
                        "speaker": "Valdris",
                        "text": "Ashenmoor.\n"
                                "They always bring up Ashenmoor.\n"
                                "Two hundred people. Yes. I know the count. "
                                "I've carried it longer than you've been alive.\n"
                                "But a world-merger requires a resonance cascade. "
                                "The living are part of the bridge. "
                                "Ashenmoor was the proof of concept. Not the goal.",
                        "on_enter": [{"action": "discover_lore", "lore": "valdris_true_plan"}],
                        "next": "final_choice",
                    },
                    "plan": {
                        "speaker": "Valdris",
                        "text": "A bridge. Between this world and the Shadow Realm.\n"
                                "Not a barrier — the Wardens built a barrier. It only delays. "
                                "The Fading will consume this world in eighteen months "
                                "whether you stop me or not.\n"
                                "What I offer is permanence. Merger. "
                                "One world, which cannot Fade, because Shadow is already within it.",
                        "on_enter": [{"action": "discover_lore", "lore": "valdris_true_plan"}],
                        "next": "final_choice",
                    },
                    "final_choice": {
                        "speaker": "Valdris",
                        "text": "You have the Hearthstones. I need them.\n"
                                "Give them to me — and I will build something that lasts.\n"
                                "Or use them yourselves — restoring a ward-network that will fail "
                                "again in a century and requires someone's blood to maintain forever.\n"
                                "Choose quickly. I have run out of patience.",
                        "choices": [
                            {"text": "The wards don't need blood anymore. Maren solved it.",
                             "next": "maren_solution",
                             "condition": {"flag": "maren.fighting_with_party", "op": "==", "value": True}},
                            {"text": "We choose the wards.",  "next": "fight"},
                            {"text": "We're not giving you anything.", "next": "fight"},
                        ],
                    },
                    "maren_solution": {
                        "speaker": "Valdris",
                        "text": "She solved the maintenance equation.\n"
                                "The long silence.\n"
                                "Show me.",
                        "next": "maren_shows",
                    },
                    "maren_shows": {
                        "speaker": "Maren",
                        "text": "It's in the resonance differential. You treated the stones "
                                "as static anchors. They're not — they're oscillators. "
                                "Phase them correctly and the ward-network generates its own "
                                "maintenance field. No blood. No vigil. Perpetual.\n"
                                "It's your own math, Father. You just didn't finish it.",
                        "next": "valdris_responds",
                    },
                    "valdris_responds": {
                        "speaker": "Valdris",
                        "text": "...\n"
                                "The figure is still for a very long time.\n"
                                "The grey-light flickers.\n"
                                "If that is true. If you've solved it.\n"
                                "Then everything I have done was unnecessary.\n"
                                "He looks at his hands.\n"
                                "It won't stop me. But I wanted you to know — "
                                "that I understood, at the end, what I cost.",
                        "on_enter": [{"action": "set_flag", "flag": "valdris.understood", "value": True}],
                        "end": True,
                    },
                    "fight": {
                        "speaker": "Valdris",
                        "text": "Then we have nothing more to discuss.\n"
                                "I have waited four hundred years for these stones.\n"
                                "You will not take them from me.",
                        "end": True,
                    },
                },
            },
        },
    ],

    # ─────────────────────────────────────────────────────────
    #  MAREN SPIRE REUNION — Fires on Valdris Spire floor 5
    #  Two variants based on how the betrayal went.
    # ─────────────────────────────────────────────────────────
    "maren_spire": [
        # Variant A — player listened (betray_heard)
        {
            "conditions": [
                {"flag": "maren.betray_heard",        "op": "==",        "value": True},
                {"flag": "maren.spire_reunion_done",  "op": "not_exists"},
            ],
            "tree": {
                "id": "maren_spire_heard",
                "nodes": {
                    "start": {
                        "speaker": "Maren",
                        "text": "You came.\n"
                                "I didn't know if you would — or if you'd come to stop me "
                                "rather than finish this.\n"
                                "Either way. I'm glad you're here.",
                        "choices": [
                            {"text": "We're here to stop Valdris. What he's doing is wrong.",
                             "next": "align"},
                            {"text": "We're not sure yet. What do you need?",
                             "next": "uncertain"},
                            {"text": "What did you find when you got here?",
                             "next": "what_found"},
                        ],
                    },
                    "what_found": {
                        "speaker": "Maren",
                        "text": "Him. My father — what's left of him.\n"
                                "He's not Valdris anymore. He's a Lingering Will — "
                                "a consciousness that refused to dissolve when the Fading consumed him. "
                                "The ritual bound him to the Spire instead of completing.\n"
                                "That's why the Hearthstones are needed. "
                                "They're the only thing that can break the binding — "
                                "and either restore the wards or finish what he started.",
                        "next": "align",
                    },
                    "uncertain": {
                        "speaker": "Maren",
                        "text": "That's fair. You've had good reason not to trust me.\n"
                                "I need — I need you to fight him. I can't do it myself. "
                                "He's still my father, whatever he's become, and I can't "
                                "make my hands do it.\n"
                                "After — after, I'll restore the wards the way the formula says. "
                                "No ritual. No sacrifice. Just the stones and the anchor points.\n"
                                "You have my word.",
                        "next": "final_deal",
                    },
                    "align": {
                        "speaker": "Maren",
                        "text": "Then we want the same thing. Finally.\n"
                                "The wards can be restored with just the stones — no ritual. "
                                "I've confirmed it. The ritual was my father's shortcut. "
                                "The stones themselves are enough, if placed correctly.\n"
                                "Fight him. I'll handle the placement. Deal?",
                        "next": "final_deal",
                    },
                    "final_deal": {
                        "speaker": "Maren",
                        "text": "He's on the top floor. He's been waiting — "
                                "he wants the Hearthstones too, but for the opposite reason.\n"
                                "Don't let him speak too long. He's very persuasive. "
                                "He was my father. I would know.",
                        "on_enter": [
                            {"action": "set_flag", "flag": "maren.spire_reunion_done", "value": True},
                            {"action": "set_flag", "flag": "maren.fighting_with_party",  "value": True},
                        ],
                        "end": True,
                    },
                },
            },
        },
        # Variant B — player resisted (betray_resisted)
        {
            "conditions": [
                {"flag": "maren.betray_resisted",     "op": "==",        "value": True},
                {"flag": "maren.spire_reunion_done",  "op": "not_exists"},
            ],
            "tree": {
                "id": "maren_spire_resisted",
                "nodes": {
                    "start": {
                        "speaker": "Maren",
                        "text": "You got up.\n"
                                "Good.\n"
                                "For what it's worth — the ward-pulse wasn't meant to hurt you. "
                                "It was meant to give me a head start.",
                        "choices": [
                            {"text": "We're here now. What do you want?",
                             "next": "what_want"},
                            {"text": "We should have stopped you when we had the chance.",
                             "next": "regret"},
                        ],
                    },
                    "regret": {
                        "speaker": "Maren",
                        "text": "Maybe. But then you wouldn't be here now.\n"
                                "And I need you here now.\n"
                                "I got inside the Spire. I found him. "
                                "I spent two days trying to do what I came to do "
                                "and I couldn't. He's too strong for one person.\n"
                                "I was wrong to think I could do this alone.",
                        "next": "offer",
                    },
                    "what_want": {
                        "speaker": "Maren",
                        "text": "I want what I've always wanted. The Fading stopped. "
                                "The wards restored.\n"
                                "But my father is a Lingering Will now — more dangerous than "
                                "he ever was alive. I can't fight him alone.\n"
                                "I'm asking. After everything. Please.",
                        "next": "offer",
                    },
                    "offer": {
                        "speaker": "Maren",
                        "text": "Help me fight him. Then I'll restore the wards — "
                                "properly, just the stones and the anchor points, "
                                "no ritual, no sacrifice.\n"
                                "And after that — if you want to drag me to the Imperial "
                                "courts or whatever — I'll go quietly.\n"
                                "But let me finish this first.",
                        "choices": [
                            {"text": "We'll fight him. Then we talk about after.",
                             "next": "accepted"},
                            {"text": "Fine. But we're watching you.",
                             "next": "accepted"},
                        ],
                    },
                    "accepted": {
                        "speaker": "Maren",
                        "text": "That's all I'm asking for.\n"
                                "He's at the top. He knows we're coming — "
                                "he's known since I arrived. He's been waiting.\n"
                                "Stay close.",
                        "on_enter": [
                            {"action": "set_flag", "flag": "maren.spire_reunion_done",   "value": True},
                            {"action": "set_flag", "flag": "maren.fighting_with_party",  "value": True},
                        ],
                        "end": True,
                    },
                },
            },
        },
    ],
}


# ═══════════════════════════════════════════════════════════════
#  TOWN NPC ASSIGNMENTS
#  Maps town_id → list of NPC IDs available there
# ═══════════════════════════════════════════════════════════════

TOWN_NPCS = {
    "briarhollow": ["maren", "captain_rowan", "bess"],
    "woodhaven":   ["elder_theron", "sylla"],
    "ironhearth":  ["forgemaster_dunn", "merchant_kira"],
    "greenwood":   ["scout_feryn"],
    "saltmere":    ["guildmaster_sable", "tide_priest_oran", "dockhand_riv"],
    "sanctum":     ["high_priest_aldara"],
    "crystalspire": ["archmage_solen", "teleport_master"],
    "thornhaven":  ["governor_aldric", "guild_commander_varek", "court_mage_sira"],
}


# ═══════════════════════════════════════════════════════════════
#  TAVERN RUMORS BY ACT
#  Rumors change as the story progresses
# ═══════════════════════════════════════════════════════════════

TAVERN_RUMORS = {
    1: [
        "The goblins have been massing east of town. More than usual.",
        "Old Tam swears his barn faded like a mirage and came back an hour later.",
        "A traveling mage says shadow magic is growing stronger. Bad omen.",
        "The wolves are aggressive this season. Something's driving them from the hills.",
        "That scholar woman — Maren — she's been asking about some kind of ancient order.",
        "The temple priests seem worried. They won't say about what.",
        "Farmers say their crops are wilting even with good rain. Never seen that before.",
        "Strange lights in the old mine at night. Nobody's had the nerve to check.",
        "Heard a whole patrol went into the eastern woods and didn't come back. Captain's keeping it quiet.",
        "The spiders in the Thornwood are getting bigger. And they're moving in groups now.",
        "My grandfather talked about the Wardens like they were gods. Said they kept something terrible locked away.",
        "The fishing boats say the sea has been wrong lately. Tides off. Water too dark.",
    ],
    2: [
        "A whole village disappeared north of Woodhaven. Just... gone. Empty land.",
        "The Fading — that's what they're calling it now. The nothing that eats the world.",
        "Maren left town in a hurry. Didn't say where she was going.",
        "The ruins of Ashenmoor are active again. Lights, sounds. Something woke up in there.",
        "I heard there was an order called the Wardens. Protected the world, once.",
        "The sun seems dimmer. That's not just me, right?",
        "Traders from Ironhearth say the mines are failing. Ore comes up wrong — brittle, grey.",
        "They say a dragon nests in the Dragon's Tooth. Corrupted by the shadow.",
        "The Governor in Thornhaven has locked down the castle archives. Why would he do that unless he knows something?",
        "Crystalspire's Archmage has been running calculations for months. I heard the numbers are bad.",
        "A woman came through asking about the old bloodlines. Warden bloodlines. Very intense eyes.",
        "The Sunken Crypt has been sealed by the Cathedral for two centuries. Nobody says why.",
        "I met a scholar who said the Fading isn't random — it always takes Warden places first.",
        "Saltmere's had three ships vanish. No storms. Just gone. The priests are praying double shifts.",
        "The teleport circles in Crystalspire are flickering. The ley lines are failing.",
    ],
    3: [
        "Eastport has gone dark. No ships, no messages. Nothing.",
        "The sky over the mountains is black. Not storm-black. Empty-black.",
        "Someone's building a fortress beyond the Pale Coast. Or something is.",
        "Maren came back. She looks... different. Haunted.",
        "The Fading is accelerating. We might have weeks, not months.",
        "The last Hearthstone — they say it's on the Windswept Isle. If it's not already gone.",
        "There's talk of a ritual that could end this. But the cost...",
        "Whatever happens next, I'm glad someone's fighting. That's worth something.",
        "I heard those adventurers found one of the old stones. Maybe there's hope yet.",
        "The Governor sent soldiers east. None came back. He's not sending more.",
        "Valdris's tower has been visible from the hills. Something in it is moving.",
        "The Cathedral in Sanctum is seeing a thousand pilgrims a day. People want somewhere to pray.",
        "If those Warden-blooded people fail... I don't think anyone's coming after them.",
    ],
}


# ═══════════════════════════════════════════════════════════════
#  DUNGEON STORY EVENTS
#  Triggered at specific tiles or on specific floors.
#  Each dungeon has a list of story events.
# ═══════════════════════════════════════════════════════════════

DUNGEON_STORY_EVENTS = {
    "goblin_warren": {
        "floor_messages": {
            1: "The tunnel air is damp and stale. Crude goblin carvings mark the walls — "
               "not decorative, but warnings. Something drove these creatures underground.",
            2: "Deeper now. The carvings change — they show a forest dissolving into nothing. "
               "Stick figures fleeing. A large figure carrying something bright.",
            3: "The tunnels open into a wider cavern. Crude fortifications line the walls — "
               "overturned carts, sharpened stakes, the smell of cook-fires. "
               "This is not just a hideout. It's a home. Someone important is deeper in.",
        },
        "journal_entries": [
            {
                "floor": 1,
                "title": "Scratched Note",
                "text": "Found scratched into the wall in crude Common: "
                        "'Forest gone. Running. The nothing follows.'",
                "lore_id": None,
            },
            {
                "floor": 2,
                "title": "Dead Guard's Journal",
                "text": "A leather journal, water-damaged. The last entry reads: "
                        "'Patrol found goblin camp. They're not raiders — they're refugees. "
                        "Women, children, injured. Tried to report back but... the road. "
                        "Something's wrong with the road. It's not there anymore.'",
                "lore_id": None,
                "on_find": [{"action": "set_quest", "quest": "side_missing_patrol", "state": 2}],
            },
        ],
        # Boss dialogue triggers before combat on boss floor
        "boss_dialogue": "grak",
    },
    "spiders_nest": {
        "floor_messages": {
            1: "Thick webs cover the entrance. The silk has an unnatural shimmer — "
               "almost iridescent, shifting colors that shouldn't exist.",
            2: "The spiders here are wrong. Too many eyes, too many legs. "
               "Some seem to phase in and out of visibility, as if not fully in this world.",
            3: "The webs here pulse with a faint violet light. "
               "This isn't natural growth — it's Fading energy, woven into the silk.",
            4: "At the heart of the nest, the Spider Queen waits. "
               "She is enormous and partially translucent — half in this world, "
               "half in the Shadow Realm.",
        },
        "journal_entries": [
            {
                "floor": 2,
                "title": "Researcher's Notes",
                "text": "The specimens exhibit clear mutagenic effects consistent with "
                        "prolonged exposure to ward-decay energy. The Fading doesn't just "
                        "destroy — it transforms. These creatures are adapting to exist "
                        "between realities. — E.V.",
                "lore_id": "spider_queen_observed",
            },
        ],
        "boss_dialogue": "spider_queen",
    },
    "abandoned_mine": {
        "floor_messages": {
            1: "The mine entrance is solid dwarven stonework, now crumbling. "
               "Runes along the doorframe flicker with dying light.",
            2: "The runes grow stronger as you descend. Something down here "
               "is still powered by the old magic.",
            3: "Ancient ward-circles are carved into every wall. This wasn't "
               "just a mine — it was a vault. A place to protect something precious.",
        },
        "journal_entries": [
            {
                "floor": 2,
                "title": "Dwarven Inscription",
                "text": "Translated from Old Dwarvish: 'Here lies the charge of Warden "
                        "Korrath, sealed until the world has need again. "
                        "Let the stone judge the worthy.'",
                "lore_id": None,
            },
        ],
        "boss_dialogue": "korrath",
    },
    "ruins_ashenmoor": {
        "floor_messages": {
            1: "The ruins still smolder with a heat that has no source. "
               "This place was destroyed by magic, not fire.",
            2: "Faded murals line the halls — scenes of Wardens performing rituals. "
               "One figure stands apart from the others. His hands glow with shadow.",
            3: "You find a sealed chamber. The door bears the mark of the Wardens, "
               "broken deliberately. Someone wanted what was inside.",
            4: "The inner court. The air here is thick with ash. "
               "Something formed from it — shaped itself over centuries "
               "from what the destruction left behind. It waits at the center.",
        },
        "journal_entries": [
            {
                "floor": 2,
                "title": "Warden Commander's Log",
                "text": "'Valdris has gone too far. His experiments with the shadow energy "
                        "have weakened the northern ward-anchor beyond repair. We confronted him "
                        "today. He called us blind. Said the Shadow isn't our enemy — it's our "
                        "evolution. I've ordered his quarters sealed. Gods help us all.'",
                "lore_id": "valdris_betrayal",
                "on_find": [{"action": "discover_lore", "lore": "valdris_betrayal"},
                             {"action": "set_flag", "flag": "lore.valdris_betrayal", "value": True}],
            },
            {
                "floor": 3,
                "title": "Charred Order of Execution",
                "text": "'By authority of the Warden Council, the research and quarters of "
                        "Warden-Researcher Valdris are hereby sealed pending investigation "
                        "into the Ashenmoor ward-anchor collapse. The death toll is two hundred "
                        "and twelve. Valdris has not been located. — Signed, Commander Ashvar'",
                "lore_id": "ashenmoor_fall",
            },
        ],
        "boss_dialogue": "ashvar",
    },
    "valdris_spire": {
        "floor_messages": {
            1: "The tower entrance groans open. Dust cascades from ancient stone. "
               "Constructs stir in the darkness ahead.",
            2: "Armor lines the halls like silent sentinels. Some begin to move as you approach.",
            3: "Books and scrolls litter the floor. The air crackles with residual magic. "
               "Robed figures shuffle between the shelves, muttering.",
            4: "The stench of alchemical reagents fills the air. Something large "
               "stirs in the shadows — the failed experiments of a desperate man.",
            5: "Reality warps. The walls breathe. Tendrils of void seep through cracks "
               "in the stone. The Fading is strong here.",
            6: "The top of the tower. A great rift hangs in the air — "
               "and within it, a figure of shadow and light turns to face you. "
               "\"You've come at last. The Hearthstone calls to you as it once called to me.\"",
        },
        "journal_entries": [
            {"floor": 1, "title": "Entry Log — Year 412",
             "text": "The tower is sealed. Valdris ordered the lower halls warded with "
                     "constructs after the last intrusion. The Wardens grow suspicious "
                     "of his research, but he insists it's for the greater good.",
             "lore_id": "spire_log_1"},
            {"floor": 2, "title": "Research Notes — Animated Guardians",
             "text": "The animated armor works splendidly. A simple binding circle "
                     "imprints combat instinct into the metal. They never tire, "
                     "never question. If only the other Wardens were so obedient.",
             "lore_id": "spire_log_2"},
            {"floor": 3, "title": "Research Notes — The Fading",
             "text": "I've confirmed it. The Fading is not a disease — it's a boundary "
                     "collapse. The veil between our world and the Void thins where the "
                     "Hearthstones' influence wanes. If I can harness a Fading breach "
                     "directly... the power would be beyond anything the Wardens imagined.",
             "lore_id": "spire_log_3"},
            {"floor": 4, "title": "Personal Journal — Doubts",
             "text": "Maren visited today. She's growing. Bright child. Asked me why "
                     "the tower 'feels sad.' I told her towers don't feel. But she's "
                     "right. Something has changed here. The experiments pull at the "
                     "edges of things. I've started seeing shapes in the corners.",
             "lore_id": "spire_log_4"},
            {"floor": 5, "title": "Final Entry",
             "text": "The breach is open. The Fading pours through like water through "
                     "a cracked dam. I can feel it reshaping me — not destroying, but "
                     "rewriting. I understand now why the old Wardens hid the Hearthstones. "
                     "Not to protect the world from the Fading. To protect the Fading "
                     "from people like me. It's too late. Maren... forgive me.",
             "lore_id": "spire_log_5"},
        ],
        "boss_dialogue": "valdris",  # Triggers before final combat on floor 6
    },
    "sunken_crypt": {
        "floor_messages": {
            1: "Cold water seeps through the stone. The crypt was built to last — "
               "great carved archways still stand perfectly, despite centuries of flooding. "
               "Strange blue lichen casts a pale light. The air smells of salt and old magic.",
            2: "The deeper chambers are warmer, not colder. "
               "A low hum resonates through the walls — not mechanical, but magical. "
               "Ward-lines are carved into every surface. Something here is still active.",
            3: "Ancestor statues line the corridor. Each bears a broken ward-mark on its chest. "
               "Someone — or something — has been here before and deliberately damaged them. "
               "Yet the stone at the center still holds.",
            4: "The burial chamber of Deren, Third Warden of the Western Coast. "
               "A figure stands at the altar, back turned. It is still. It has been waiting. "
               "The air between you and it vibrates with ward-energy. "
               "He turns, and his eyes are cold blue fire.",
        },
        "journal_entries": [
            {
                "floor": 1,
                "title": "Crypt Inscription",
                "text": "Cut into the archway in old Aldenmere script: "
                        "'Here rests the line of Deren, who swore to the last stone. "
                        "He who passes with Warden blood — remember that some oaths "
                        "outlast death. He waits for the worthy. He cannot do otherwise.'",
                "lore_id": None,
            },
            {
                "floor": 2,
                "title": "Researcher's Fragment",
                "text": "A torn page, relatively recent: "
                        "'The Sunken Warden is not a haunt — it is a construct of oath-magic. "
                        "He retains full intelligence. He can speak, reason, even grieve. "
                        "He simply cannot choose to release the stone. "
                        "The binding doesn't allow for surrender. "
                        "It only allows for defeat.' — A.S. [Archmage Solen?]",
                "lore_id": "sunken_warden_truth",
            },
            {
                "floor": 3,
                "title": "Letter, Never Sent",
                "text": "Water-stained but legible: "
                        "'Deren — if you read this, we have failed to free you. "
                        "I tried everything. The binding is older than our order and stronger "
                        "than anything I know how to break. I'm sorry. "
                        "I hope the ones who come after us are worthy of what you protect. "
                        "— Warden-Commander Lira, Year 344'",
                "lore_id": None,
            },
        ],
        "boss_dialogue": "sunken_warden",
    },
    "dragons_tooth": {
        "floor_messages": {
            1: "The volcanic island reeks of sulfur and salt. "
               "The ground is black glass — cooled lava from some ancient eruption. "
               "Corrupted creatures patrol the shoreline. "
               "High above, something vast shifts in the caldera.",
            2: "The cave network beneath the island is extensive. "
               "Strange carvings mark the walls — older than any human civilization. "
               "Something lived here long before the dragon.",
            3: "The dragon's hoard chamber. Gold and bones in equal measure. "
               "At the center, something glows with a light that doesn't belong here — "
               "warm and golden against the volcanic dark. "
               "The third Hearthstone. And curled around it, something enormous stirs.",
        },
        "journal_entries": [
            {
                "floor": 1,
                "title": "Sailor's Log",
                "text": "Final entry of the merchant vessel Tiderunner: "
                        "'The island is inhabited. Not by men — something older. "
                        "Karreth keeps circling the caldera, won't approach. "
                        "We've lost two of the crew. The thing on the peak watches us. "
                        "Making for open water at dawn. "
                        "God help whoever comes here for the thing that glows.'",
                "lore_id": None,
            },
            {
                "floor": 2,
                "title": "Ancient Tablet",
                "text": "Translated from pre-Imperial script by Archmage Solen: "
                        "'The dragon Karreth was not always corrupted. "
                        "It was once a ward-guardian — the first, before the Wardens existed. "
                        "The Fading entered it when the nearest anchor failed. "
                        "It does not know what it has become. "
                        "It only knows it must protect the warm thing at its center.'",
                "lore_id": "dragon_karreth",
            },
        ],
        "boss_dialogue": "karreth",
    },
}


# ═══════════════════════════════════════════════════════════════
#  HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def get_town_npcs(town_id):
    """Get list of NPC data dicts for a given town."""
    npc_ids = TOWN_NPCS.get(town_id, [])
    return [(nid, NPCS[nid]) for nid in npc_ids if nid in NPCS]


def get_rumor(act=None):
    """Get a random rumor for the current act."""
    import random
    from core.story_flags import get
    if act is None:
        act = get("act", 1)
    rumors = TAVERN_RUMORS.get(act, TAVERN_RUMORS[1])
    return random.choice(rumors)


def get_dungeon_floor_message(dungeon_id, floor):
    """Get story message for entering a dungeon floor."""
    events = DUNGEON_STORY_EVENTS.get(dungeon_id, {})
    return events.get("floor_messages", {}).get(floor)


def get_dungeon_journals(dungeon_id, floor):
    """Get journal entries available on a dungeon floor."""
    events = DUNGEON_STORY_EVENTS.get(dungeon_id, {})
    journals = events.get("journal_entries", [])
    return [j for j in journals if j.get("floor") == floor]


def get_dungeon_boss_dialogue(dungeon_id):
    """Get the NPC dialogue key for a dungeon's boss, if any."""
    events = DUNGEON_STORY_EVENTS.get(dungeon_id, {})
    return events.get("boss_dialogue")


# ══════════════════════════════════════════════════════════
#  ADDITIONAL NPC DIALOGUES  (wired in town_maps.py)
# ══════════════════════════════════════════════════════════

_NEW_DIALOGUES = {

    # ── Briarhollow ────────────────────────────────────────

    "captain_aldric": [
        # Turn-in: missing patrol found (journal on goblin warren floor 2)
        {
            "conditions": [
                {"flag": "quest.side_missing_patrol.state", "op": ">=", "value": 2},
                {"flag": "quest.side_missing_patrol.state", "op": "!=", "value": -2},
            ],
            "tree": {
                "id": "aldric_patrol_turnin",
                "nodes": {
                    "start": {
                        "speaker": "Captain Aldric",
                        "text": "You found the journal? So they're gone. All six of them. I'll need a moment. The road just... wasn't there anymore. That's not wolves or goblins — that's something else entirely.\nThank you for bringing it back. Their families deserved to know.",
                        "on_enter": [{"action": "complete_quest", "quest": "side_missing_patrol"}],
                        "choices": [
                            {"text": "The Fading took the road. It's spreading.", "next": "fading"},
                            {"text": "We're sorry for your loss.", "next": "sorry"},
                        ],
                    },
                    "fading": {
                        "speaker": "Captain Aldric",
                        "text": "The Fading. Maren's word for it. I thought it was superstition. Now I don't know what to believe. How do you fight something that erases roads?",
                        "choices": [{"text": "That's what we're trying to find out.", "next": None}],
                    },
                    "sorry": {
                        "speaker": "Captain Aldric",
                        "text": "So am I. Good soldiers. Keep moving — I'll handle the paperwork. You have bigger problems to deal with.",
                        "choices": [{"text": "We will.", "next": None}],
                    },
                },
            },
        },
        # Turn-in: wolf pelts collected
        {
            "conditions": [
                {"flag": "wolf_pelts_quest.count", "op": ">=", "value": 5},
                {"flag": "quest.side_wolf_pelts.state", "op": "!=", "value": -2},
            ],
            "tree": {
                "id": "aldric_wolf_turnin",
                "nodes": {
                    "start": {
                        "speaker": "Captain Aldric",
                        "text": "You've got the pelts? Good. The tanner's been waiting. Here's your coin — well earned.",
                        "on_enter": [
                            {"action": "complete_quest", "quest": "side_wolf_pelts"},
                        ],
                        "choices": [{"text": "Happy to help.", "next": None}],
                    },
                },
            },
        },
        {
            "conditions": [{"flag": "boss_defeated.abandoned_mine", "op": "==", "value": True}],
            "tree": {
                "id": "aldric_post_mine",
                "nodes": {
                    "start": {
                        "speaker": "Captain Aldric",
                        "text": "You cleared the mine. I won't pretend I thought you'd pull it off. The townsfolk are sleeping better. I suppose I owe you a drink.",
                        "choices": [
                            {"text": "What happens to the mine now?", "next": "mine_fate"},
                            {"text": "Just doing our job.", "next": "modest"},
                        ],
                    },
                    "mine_fate": {
                        "speaker": "Captain Aldric",
                        "text": "The Guild wants to reopen it. I say leave it sealed. Whatever Valdris was doing down there — I don't want it under our feet again. But nobody asks guards.",
                        "choices": [{"text": "Thanks, Captain.", "next": None}],
                    },
                    "modest": {
                        "speaker": "Captain Aldric",
                        "text": "Don't be modest. Half my garrison wouldn't have gone in. Take the compliment.",
                        "choices": [{"text": "We'll be moving on soon.", "next": None}],
                    },
                },
            },
        },
        {
            "conditions": [],
            "tree": {
                "id": "aldric_default",
                "nodes": {
                    "start": {
                        "speaker": "Captain Aldric",
                        "text": "I'm the town guard captain. Twelve men, one broken crossbow, and a gate that sticks. If trouble comes, I'm counting on adventurers more than I should be.",
                        "choices": [
                            {"text": "What kind of trouble?", "next": "trouble"},
                            {"text": "Any missing patrols?", "next": "patrol"},
                            {"text": "The mine — what do you know about it?", "next": "mine"},
                            {"text": "We can handle ourselves.", "next": "confident"},
                        ],
                    },
                    "patrol": {
                        "speaker": "Captain Aldric",
                        "text": "Six guards. Good people. I sent them east to check the road near the goblin caves three days ago. Nothing since. If you're heading that way — keep an eye out. Whatever happened to them, I want answers.",
                        "on_enter": [{"action": "start_quest", "quest": "side_missing_patrol"}],
                        "choices": [{"text": "We'll find out what happened.", "next": None}],
                    },
                    "trouble": {
                        "speaker": "Captain Aldric",
                        "text": "Goblin raids getting bolder. And something's wrong in the old Hearthstone mine — workers won't go near it after dark. I've sent two patrols. Neither came back with good news. Oh — if you're heading east, the village tanner needs wolf pelts. Unusually large pack out there.",
                        "on_enter": [{"action": "start_quest", "quest": "side_wolf_pelts"}],
                        "choices": [{"text": "We'll look into it.", "next": None}],
                    },
                    "mine": {
                        "speaker": "Captain Aldric",
                        "text": "It was a good vein once. Then Valdris's people showed up, bought out the contracts, started working night shifts. No one knows what they pulled out. Then — silence. Workers left. Something's still in there.",
                        "choices": [{"text": "Understood.", "next": None}],
                    },
                    "confident": {
                        "speaker": "Captain Aldric",
                        "text": "Good. Because I can't spare anyone.",
                        "choices": [{"text": "Fair enough.", "next": None}],
                    },
                },
            },
        },
    ],

    "elder_thom": [
        {
            "conditions": [{"flag": "lore.fading_basics", "op": "==", "value": True}],
            "tree": {
                "id": "elder_thom_knows",
                "nodes": {
                    "start": {
                        "speaker": "Elder Thom",
                        "text": "So. You know about the Fading now. I've watched it creep closer for twenty years. We call it shadow sickness here, pretend it's natural. It isn't.",
                        "choices": [
                            {"text": "How long has Briarhollow known?", "next": "how_long"},
                            {"text": "What can we do?", "next": "what_do"},
                        ],
                    },
                    "how_long": {
                        "speaker": "Elder Thom",
                        "text": "The forest started dying when I was a young man. Forty years ago, give or take. About when Valdris first started his 'research.' The timing was never a coincidence.",
                        "choices": [{"text": "We'll stop him.", "next": None}],
                    },
                    "what_do": {
                        "speaker": "Elder Thom",
                        "text": "Find the Hearthstones. The scholar — Maren — she's right about them. They're not power sources. They're seals. Break the pattern of extraction and you break his hold.",
                        "choices": [{"text": "We understand.", "next": None}],
                    },
                },
            },
        },
        {
            "conditions": [],
            "tree": {
                "id": "elder_thom_default",
                "nodes": {
                    "start": {
                        "speaker": "Elder Thom",
                        "text": "I've been elder here for thirty years. In that time I've seen three harvests fail, a river run dry, and the forest creep back from the edge of town. Something is wrong with this land.",
                        "on_enter": [{"action": "set_flag", "flag": "npc.elder_thom.met", "value": True}],
                        "choices": [
                            {"text": "What do you think is causing it?", "next": "cause"},
                            {"text": "Who should we speak to?", "next": "refer"},
                        ],
                    },
                    "cause": {
                        "speaker": "Elder Thom",
                        "text": "I'm an old man, not a scholar. But the decline matched when the miners came — the ones who took contracts from some lord up north. I never learned his name. Maren might know.",
                        "choices": [{"text": "We'll ask her.", "next": None}],
                    },
                    "refer": {
                        "speaker": "Elder Thom",
                        "text": "Maren, the scholar staying at the inn. She's been researching the land sickness longer than anyone. She has theories I don't fully understand, but her eyes are honest.",
                        "choices": [{"text": "Thank you, Elder.", "next": None}],
                    },
                },
            },
        },
    ],

    # ── Woodhaven ──────────────────────────────────────────

    "ranger_lyric": [
        {
            "conditions": [{"flag": "quest.main_spiders_nest.state", "op": ">", "value": 0}],
            "tree": {
                "id": "lyric_spider_quest",
                "nodes": {
                    "start": {
                        "speaker": "Ranger Lyric",
                        "text": "The Spider Queen's nest is growing. Two of my scouts didn't come back from the eastern ridge. Whatever she is now, she wasn't natural to begin with — something sped up her growth.",
                        "choices": [
                            {"text": "We're on it.", "next": "good"},
                            {"text": "What changed?", "next": "changed"},
                        ],
                    },
                    "good": {
                        "speaker": "Ranger Lyric",
                        "text": "Don't go in without fire. The webs are thick enough to stop a spear.",
                        "choices": [{"text": "Noted.", "next": None}],
                    },
                    "changed": {
                        "speaker": "Ranger Lyric",
                        "text": "Six months ago she was just a big spider. Now she's the size of a cart horse and her brood covers the whole eastern slope. Something's feeding her growth. The same thing that's killing the trees, maybe.",
                        "choices": [{"text": "We'll find out.", "next": None}],
                    },
                },
            },
        },
        {
            "conditions": [],
            "tree": {
                "id": "lyric_default",
                "nodes": {
                    "start": {
                        "speaker": "Ranger Lyric",
                        "text": "These woods used to be safe enough for children to wander. Now I don't let my scouts go east without a full squad. Something is wrong in the deep forest — worse every season.",
                        "on_enter": [{"action": "set_flag", "flag": "npc.lyric.met", "value": True}],
                        "choices": [
                            {"text": "What's out there?", "next": "threats"},
                            {"text": "Any work for adventurers?", "next": "work"},
                        ],
                    },
                    "threats": {
                        "speaker": "Ranger Lyric",
                        "text": "Giant spiders, mostly. Bigger than they should be. A few wolf packs that act wrong — too coordinated, like they're being driven. And the trees themselves are sick. Brown at the roots.",
                        "choices": [{"text": "We'll investigate.", "next": None}],
                    },
                    "work": {
                        "speaker": "Ranger Lyric",
                        "text": "Check the job board. Guildmaster Oren posts contracts. But between us — the real problem is the spider nest to the east. It's getting out of hand.",
                        "choices": [{"text": "We'll look into it.", "next": None}],
                    },
                },
            },
        },
    ],

    "old_moss": [
        {
            "conditions": [],
            "tree": {
                "id": "old_moss_default",
                "nodes": {
                    "start": {
                        "speaker": "Old Moss",
                        "text": "Mm. Travelers. Sit. These mushrooms won't pick themselves, but they'll wait a moment. You have the look of people carrying more trouble than they admit.",
                        "on_enter": [{"action": "set_flag", "flag": "npc.old_moss.met", "value": True}],
                        "choices": [
                            {"text": "What do you know about the forest dying?", "next": "forest"},
                            {"text": "What are those mushrooms for?", "next": "mushrooms"},
                            {"text": "Just passing through.", "next": "passing"},
                        ],
                    },
                    "forest": {
                        "speaker": "Old Moss",
                        "text": "I've watched this forest since before your parents were born. The sickness comes from below, not above. The roots feel it before the leaves do. Something underground is draining them. Has been for years.",
                        "choices": [
                            {"text": "The mines?", "next": "mines"},
                            {"text": "Thank you, elder.", "next": None},
                        ],
                    },
                    "mines": {
                        "speaker": "Old Moss",
                        "text": "Probably. The old Hearthstone veins. They were sealed for a reason — the miners who dug them three hundred years ago sealed them themselves, which tells you something. Now someone's opened them again.",
                        "choices": [{"text": "Who?", "next": "who"},
                                    {"text": "Thank you.", "next": None}],
                    },
                    "who": {
                        "speaker": "Old Moss",
                        "text": "A name from the capital. Valdris. He sent agents years ago, smooth-talking with Imperial letters. The Guild approved it. Nobody listened to an old herbalist. They never do.",
                        "choices": [{"text": "We're listening.", "next": "listening"}],
                    },
                    "listening": {
                        "speaker": "Old Moss",
                        "text": "Then find the stones before he does. Or find them after, and take them away from him. Either works.",
                        "choices": [{"text": "We will.", "next": None}],
                    },
                    "mushrooms": {
                        "speaker": "Old Moss",
                        "text": "This one cures fever. This one cures poison if you eat it before the venom sets. This one will kill you in an interesting way if you eat it after dark. I keep them separate.",
                        "choices": [{"text": "Useful.", "next": None}],
                    },
                    "passing": {
                        "speaker": "Old Moss",
                        "text": "Nobody just passes through anymore. The roads aren't safe enough. Stay careful.",
                        "choices": [{"text": "We will.", "next": None}],
                    },
                },
            },
        },
    ],

    "guildmaster_oren": [
        {
            "conditions": [
                {"flag": "guild_trial.complete", "op": "==", "value": True},
                {"flag": "quest.side_guild_initiation.state", "op": "!=", "value": -2},
            ],
            "tree": {
                "id": "oren_trial_done",
                "nodes": {
                    "start": {
                        "speaker": "Guildmaster Oren",
                        "text": "Word reached me. Floor 3 and back. You've earned the charter. Here's your payment — and my respect, which is worth more in this business.",
                        "on_enter": [
                            {"action": "complete_quest", "quest": "side_guild_initiation"},
                        ],
                        "choices": [{"text": "Good to be in business with you.", "next": None}],
                    },
                },
            },
        },
        {
            "conditions": [],
            "tree": {
                "id": "oren_default",
                "nodes": {
                    "start": {
                        "speaker": "Guildmaster Oren",
                        "text": "You want to register with the Guild? Smart. Registered parties get access to contract work, priority lodging, and a legal standing the Empire recognizes. Unregistered adventurers are just bandits with better intentions.",
                        "choices": [
                            {"text": "How do we register?", "next": "register"},
                            {"text": "What contracts are available?", "next": "contracts"},
                            {"text": "We'll think about it.", "next": "think"},
                        ],
                    },
                    "register": {
                        "speaker": "Guildmaster Oren",
                        "text": "Five gold. I write your names in the ledger, you get a charter, and you're recognized from here to the capital. Best investment you'll make. I'll also need you to prove your worth — reach floor 3 of any major dungeon and come back to me.",
                        "on_enter": [{"action": "start_quest", "quest": "side_guild_initiation"}],
                        "choices": [{"text": "Sounds reasonable.", "next": None},
                                    {"text": "Maybe later.", "next": None}],
                    },
                    "contracts": {
                        "speaker": "Guildmaster Oren",
                        "text": "Check the job board outside. I post what comes in. Right now it's mostly patrol work and pest control. The spider situation to the east is getting serious — I'm offering a premium for proof of the nest being cleared.",
                        "choices": [{"text": "Noted.", "next": None}],
                    },
                    "think": {
                        "speaker": "Guildmaster Oren",
                        "text": "Don't think too long. Guild charter protects you if a job goes wrong and a lord wants someone to blame. Without it, that someone is you.",
                        "choices": [{"text": "Fair point.", "next": None}],
                    },
                },
            },
        },
    ],

    # ── Ironhearth ─────────────────────────────────────────

    "foreman_brak": [
        {
            "conditions": [{"flag": "boss_defeated.abandoned_mine", "op": "==", "value": True}],
            "tree": {
                "id": "brak_post_mine",
                "nodes": {
                    "start": {
                        "speaker": "Foreman Brak",
                        "text": "Word came from Briarhollow. You dealt with whatever was in that shaft. I owe you more than thanks — half my workers came from that mine before they shut it. They deserve to know it's over.",
                        "choices": [
                            {"text": "What was Valdris extracting?", "next": "extraction"},
                            {"text": "The Warden is gone.", "next": "warden"},
                        ],
                    },
                    "extraction": {
                        "speaker": "Foreman Brak",
                        "text": "Something older than iron. The veins weren't ore — they were crystallized energy. Hearthstone, the old records call it. We dug it out for fifty years not knowing what it was, just following Imperial orders.",
                        "choices": [{"text": "And what happens when it's all gone?", "next": "gone"}],
                    },
                    "gone": {
                        "speaker": "Foreman Brak",
                        "text": "Ask the forest. Ask the rivers. Ask the villages that went dark two generations back. The land bleeds when the stones are taken. But someone's still taking them.",
                        "choices": [{"text": "We know.", "next": None}],
                    },
                    "warden": {
                        "speaker": "Foreman Brak",
                        "text": "Korrath. I knew him before he turned. Good soldier. Didn't deserve what happened to him. Rest easy, old ghost.",
                        "choices": [{"text": "We'll find who ordered it.", "next": None}],
                    },
                },
            },
        },
        {
            "conditions": [],
            "tree": {
                "id": "brak_default",
                "nodes": {
                    "start": {
                        "speaker": "Foreman Brak",
                        "text": "I run three shifts underground and I can't fill half my roster. Workers quit, won't say why. Those that stay come up looking wrong — pale, shaky. The deep shafts are doing something to them.",
                        "on_enter": [{"action": "set_flag", "flag": "npc.brak.met", "value": True}],
                        "choices": [
                            {"text": "What's in the deep shafts?", "next": "deep"},
                            {"text": "Is this related to Valdris?", "next": "valdris"},
                        ],
                    },
                    "deep": {
                        "speaker": "Foreman Brak",
                        "text": "Officially? Iron ore and old granite. Unofficially — something glows down there that isn't lantern light. The old foreman sealed off level five and wouldn't talk about it before he disappeared.",
                        "choices": [{"text": "Disappeared?", "next": "disappeared"},
                                    {"text": "We'll investigate.", "next": None}],
                    },
                    "disappeared": {
                        "speaker": "Foreman Brak",
                        "text": "Walked into level five on a Tuesday. Nobody saw him leave. I reported it. Got a letter back from the capital saying he'd been reassigned. Right.",
                        "choices": [{"text": "We'll look into it.", "next": None}],
                    },
                    "valdris": {
                        "speaker": "Foreman Brak",
                        "text": "The contracts came through his office. I never met the man. But the extraction quotas, the sealed levels, the silence about what we pulled up — all signed by his agents. It smells wrong.",
                        "choices": [{"text": "It is wrong.", "next": None}],
                    },
                },
            },
        },
    ],

    "scholar_petra": [
        {
            "conditions": [],
            "tree": {
                "id": "petra_default",
                "nodes": {
                    "start": {
                        "speaker": "Scholar Petra",
                        "text": "Oh! Travelers. I'm studying the runic inscriptions on the mine supports. They're not just structural — they're warnings. The dwarves who built these shafts knew something was down there and wanted no one to forget it.",
                        "on_enter": [{"action": "set_flag", "flag": "npc.petra.met", "value": True}],
                        "choices": [
                            {"text": "What do the warnings say?", "next": "warnings"},
                            {"text": "Do you know about the Hearthstones?", "next": "hearthstones"},
                        ],
                    },
                    "warnings": {
                        "speaker": "Scholar Petra",
                        "text": "Roughly: 'Do not consume the deep flame. It is not fuel. It is blood.' That's my best translation. Poetic for a mine support. I've found the same phrase in three different shafts.",
                        "choices": [
                            {"text": "Blood?", "next": "blood"},
                            {"text": "Thank you.", "next": None},
                        ],
                    },
                    "blood": {
                        "speaker": "Scholar Petra",
                        "text": "The land's blood, I think. The Hearthstones aren't a resource — they're part of a living system. Extract them and something essential is lost. I've been trying to publish this for two years. My faculty keeps losing my letters.",
                        "choices": [{"text": "Someone doesn't want it published.", "next": "suppressed"}],
                    },
                    "suppressed": {
                        "speaker": "Scholar Petra",
                        "text": "That thought occurred to me. I'm being careful. You should be too, if you're asking these questions.",
                        "choices": [{"text": "We will be.", "next": None}],
                    },
                    "hearthstones": {
                        "speaker": "Scholar Petra",
                        "text": "You know about those? Good — someone should. They're crystallized ley energy, nodes in a network that runs under the whole region. Extracting one causes instability. Extracting all of them... I don't know. But nothing good.",
                        "choices": [{"text": "We're working to stop it.", "next": "stop"}],
                    },
                    "stop": {
                        "speaker": "Scholar Petra",
                        "text": "Then you need the scholar Maren's research. And you need to get to the stones before whoever's been clearing the sites. Move fast.",
                        "choices": [{"text": "We intend to.", "next": None}],
                    },
                },
            },
        },
    ],

    "miner_durk": [
        {
            "conditions": [],
            "tree": {
                "id": "durk_default",
                "nodes": {
                    "start": {
                        "speaker": "Miner Durk",
                        "text": "Don't ask me about the lower levels. I work the upper shafts, I go home, I sleep, I do it again. That's all. I've got a family.",
                        "choices": [
                            {"text": "What happened on the lower levels?", "next": "lower"},
                            {"text": "Fair enough.", "next": None},
                        ],
                    },
                    "lower": {
                        "speaker": "Miner Durk",
                        "text": "Two men I knew. Went down to level five because they heard something. Came up... not right. Quiet. Eyes wrong. They transferred out a week later. Company transfer. That's all I know.",
                        "choices": [{"text": "We'll leave it at that.", "next": None}],
                    },
                },
            },
        },
    ],

    "apprentice_tova": [
        {
            "conditions": [],
            "tree": {
                "id": "tova_default",
                "nodes": {
                    "start": {
                        "speaker": "Apprentice Tova",
                        "text": "Oh! Sorry, I'm in a hurry. Master Thardin will have my ears if this delivery's late. He's not mean, just very... precise.",
                        "choices": [
                            {"text": "What are you delivering?", "next": "delivery"},
                            {"text": "Go ahead, we won't keep you.", "next": None},
                        ],
                    },
                    "delivery": {
                        "speaker": "Apprentice Tova",
                        "text": "Temper salts from the Armory. You add them to the quench bath to harden steel. The Grand Forge uses twice what any normal forge does — Master Thardin says it's because he works to higher tolerances. I believe him.",
                        "choices": [{"text": "Learn from the best.", "next": "learn"}],
                    },
                    "learn": {
                        "speaker": "Apprentice Tova",
                        "text": "That's the plan! Right after I survive the apprenticeship.",
                        "choices": [{"text": "Good luck.", "next": None}],
                    },
                },
            },
        },
    ],

    # ── Greenwood ──────────────────────────────────────────

    "scout_feryn": [
        {
            "conditions": [{"flag": "quest.main_spiders_nest.state", "op": ">", "value": 0}],
            "tree": {
                "id": "feryn_spider",
                "nodes": {
                    "start": {
                        "speaker": "Scout Feryn",
                        "text": "You found the nest? Good. I tried to map it two weeks ago. Got halfway in before the webbing sealed the path behind me. Nearly didn't get out.",
                        "choices": [
                            {"text": "What's in there?", "next": "inside"},
                            {"text": "We'll handle it.", "next": "handle"},
                        ],
                    },
                    "inside": {
                        "speaker": "Scout Feryn",
                        "text": "Queen's brood, hundreds of them. And the Queen herself — she's not a normal spider. Something changed her. She moves like she's thinking.",
                        "choices": [{"text": "We'll go prepared.", "next": None}],
                    },
                    "handle": {
                        "speaker": "Scout Feryn",
                        "text": "Bring fire. Lots of it. And watch the ceiling.",
                        "choices": [{"text": "Thanks for the warning.", "next": None}],
                    },
                },
            },
        },
        {
            "conditions": [],
            "tree": {
                "id": "feryn_default",
                "nodes": {
                    "start": {
                        "speaker": "Scout Feryn",
                        "text": "You made it out here. Good. These woods get worse every season — even the birds have been acting strange. I scout this territory and I've been doing it fifteen years. Something has changed.",
                        "on_enter": [{"action": "set_flag", "flag": "npc.feryn.met", "value": True}],
                        "choices": [
                            {"text": "What's changed specifically?", "next": "changed"},
                            {"text": "Any threats we should know about?", "next": "threats"},
                        ],
                    },
                    "changed": {
                        "speaker": "Scout Feryn",
                        "text": "The spider population tripled in two seasons. Wolves are ranging further than I've ever seen. And there's a low sound in the deep forest, just at the edge of hearing. The trees around the old stone sites have all gone black at the root.",
                        "choices": [{"text": "Old stone sites?", "next": "stones"}],
                    },
                    "stones": {
                        "speaker": "Scout Feryn",
                        "text": "Places the old settlers marked. Rings of flat stones, mostly grown over now. I leave them alone. Started going wrong around the time workers showed up from the capital. Coincidence, maybe.",
                        "choices": [{"text": "Probably not a coincidence.", "next": None}],
                    },
                    "threats": {
                        "speaker": "Scout Feryn",
                        "text": "Giant spiders to the east — I mean giant, house-sized. Don't go alone. To the north, wolves that don't run when you shout at them. And something worse I can't pin down, south of the river.",
                        "choices": [{"text": "We'll stay sharp.", "next": None}],
                    },
                },
            },
        },
    ],

    "trapper_holt": [
        {
            "conditions": [],
            "tree": {
                "id": "holt_default",
                "nodes": {
                    "start": {
                        "speaker": "Trapper Holt",
                        "text": "Haven't pulled a decent pelt in three weeks. Animals are either gone or wrong. Found a fox last Tuesday — twice normal size, moving like a drunk. Left it alone.",
                        "choices": [
                            {"text": "Something's affecting the animals?", "next": "animals"},
                            {"text": "Any idea what's causing it?", "next": "cause"},
                        ],
                    },
                    "animals": {
                        "speaker": "Trapper Holt",
                        "text": "Not just size. They're more aggressive. A deer charged me last week. A deer. I've been trapping since I was ten. That doesn't happen.",
                        "choices": [{"text": "We're looking into it.", "next": None}],
                    },
                    "cause": {
                        "speaker": "Trapper Holt",
                        "text": "Something underground, I reckon. The animals near the old mine sites go wrong first. I mark them on my trap maps — always the same spots. Close to where the Hearthstone veins run, the old-timers say.",
                        "choices": [{"text": "Thank you, that's useful.", "next": None}],
                    },
                },
            },
        },
    ],

    # ── Saltmere ───────────────────────────────────────────

    "shady_figure": [
        {
            "conditions": [],
            "tree": {
                "id": "shady_default",
                "nodes": {
                    "start": {
                        "speaker": "Shady Figure",
                        "text": "Eyes forward, don't stare. People who stare in Saltmere end up with fewer fingers. You need something? Information costs. Everything in this town costs.",
                        "choices": [
                            {"text": "What's going on in this port?", "next": "port"},
                            {"text": "What do you know about Valdris?", "next": "valdris"},
                            {"text": "Nothing. Carry on.", "next": None},
                        ],
                    },
                    "port": {
                        "speaker": "Shady Figure",
                        "text": "Same as any port. Ships come in, cargo goes out, nobody asks what's in the crates. Lately there are more private ships — no markings, fast hulls. They unload at the south dock at midnight. I stay away from midnight cargoes.",
                        "choices": [{"text": "What's in the crates?", "next": "crates"}],
                    },
                    "crates": {
                        "speaker": "Shady Figure",
                        "text": "I didn't say I had that information. I said I stay away. Smart is different from curious.",
                        "choices": [{"text": "Fair enough.", "next": None}],
                    },
                    "valdris": {
                        "speaker": "Shady Figure",
                        "text": "That name. Lower your voice. He has agents in every port — some of them aren't even trying to be subtle anymore. If you're working against him, you need to already be ahead of him. Are you?",
                        "choices": [
                            {"text": "We're getting there.", "next": "getting_there"},
                            {"text": "We're trying.", "next": "trying"},
                        ],
                    },
                    "getting_there": {
                        "speaker": "Shady Figure",
                        "text": "Then I'll tell you one thing free: the stones he's moving go south, not east. Whatever he's building, it's not in the capital. Check the sea routes.",
                        "choices": [{"text": "Useful. Thank you.", "next": None}],
                    },
                    "trying": {
                        "speaker": "Shady Figure",
                        "text": "Try faster.",
                        "choices": [{"text": "Right.", "next": None}],
                    },
                },
            },
        },
    ],

        "tide_priest_oran": [
        {
            "conditions": [{"flag": "item.hearthstone.2", "op": "==", "value": True}],
            "tree": {
                "id": "oran_hs3",
                "nodes": {
                    "start": {
                        "speaker": "Tide Priest Oran",
                        "text": "You recovered the bay stone. The third is in Dragon's Tooth archipelago. I've known its location for twenty years and dreaded this moment. The warden there isn't dead — he's worse than dead.",
                        "on_enter": [{"action": "start_quest", "quest": "main_hearthstone_3"}],
                        "choices": [
                            {"text": "How do we get there?", "next": "passage"},
                            {"text": "What's waiting for us?", "next": "waiting"},
                        ],
                    },
                    "passage": {
                        "speaker": "Tide Priest Oran",
                        "text": "Dockhand Riv can arrange passage — she knows every captain who owes a favor. Tell her I sent you. Two days crossing in good weather.",
                        "choices": [{"text": "We'll find her.", "next": None}],
                    },
                    "waiting": {
                        "speaker": "Tide Priest Oran",
                        "text": "Karreth. The last Warden of the outer islands — a dragon-tamer before the Fading took his mind. He commands the creatures there. Bring fire.",
                        "choices": [{"text": "Understood.", "next": None}],
                    },
                },
            },
        },
        {
            "conditions": [],
            "tree": {
                "id": "oran_default",             "nodes": {
                    "start": {
                        "speaker": "Tide Priest Oran",
                        "text": "The tides have been wrong for months. Coming in at the wrong hour. Going out too fast. The sea knows something is out of balance — she always does, long before the land catches on.",
                        "on_enter": [{"action": "set_flag", "flag": "npc.oran.met", "value": True}],
                        "choices": [
                            {"text": "What does the sea know?", "next": "sea_knows"},
                            {"text": "Is it related to the Fading?", "next": "fading"},
                        ],
                    },
                    "sea_knows": {
                        "speaker": "Tide Priest Oran",
                        "text": "That the ley lines are shifting. The Hearthstone network — you've heard of it? — runs under the sea floor too. Pull a stone on land and the whole web trembles. Including the tides.",
                        "choices": [
                            {"text": "You know about the Hearthstones?", "next": "knows_stones"},
                            {"text": "What can be done?", "next": "what_done"},
                        ],
                    },
                    "knows_stones": {
                        "speaker": "Tide Priest Oran",
                        "text": "Every tide priest knows. We've been tracking the disruptions for generations. But knowledge and power are different things. We watch. We record. We pray. It helps less than I'd like.",
                        "choices": [{"text": "We're doing more than watching.", "next": "active"}],
                    },
                    "active": {
                        "speaker": "Tide Priest Oran",
                        "text": "Then the sea favors you. There's a stone under the bay — it was sealed there centuries ago by the first tide priests. If Valdris finds it, the tides won't be the only thing that goes wrong.",
                        "on_enter": [{"action": "start_quest", "quest": "main_hearthstone_2"}],
                        "choices": [{"text": "We'll protect it.", "next": None}],
                    },
                    "fading": {
                        "speaker": "Tide Priest Oran",
                        "text": "It's the same phenomenon. Different name — we call it the Emptying. The land dries, the sea shifts, the sky goes thin. All from the same wound.",
                        "choices": [{"text": "What wound?", "next": "wound"}],
                    },
                    "wound": {
                        "speaker": "Tide Priest Oran",
                        "text": "The extraction of what should never be extracted. The stones aren't ore. They're the world's own vitality, crystallized. Take enough of them and nothing grows back.",
                        "choices": [{"text": "We'll stop it.", "next": None}],
                    },
                    "what_done": {
                        "speaker": "Tide Priest Oran",
                        "text": "Return what was taken, if any remain. Or at minimum, stop more from being taken. Either buys time.",
                        "choices": [{"text": "We're working on it.", "next": None}],
                    },
                },
            },
        },
    ],

    # ── Sanctum ────────────────────────────────────────────

    "pilgrim_elder": [
        {
            "conditions": [],
            "tree": {
                "id": "pilgrim_default",
                "nodes": {
                    "start": {
                        "speaker": "Pilgrim Elder",
                        "text": "I walked four hundred miles to reach this city. To stand in the Cathedral and know the Light is still here. Some days that's all that keeps me moving.",
                        "choices": [
                            {"text": "Is the Light in danger?", "next": "danger"},
                            {"text": "What draws pilgrims here?", "next": "draws"},
                        ],
                    },
                    "danger": {
                        "speaker": "Pilgrim Elder",
                        "text": "The priests say no. But I've walked through three villages that were empty. Not attacked — just empty. Doors open, fires cold, food on tables. People don't abandon meals. Something took them all at once.",
                        "choices": [{"text": "When?", "next": "when"}],
                    },
                    "when": {
                        "speaker": "Pilgrim Elder",
                        "text": "Three months ago. Six months ago. Longer, further east. It's spreading west, slowly. I came here to warn the High Priest. I don't think she believed me.",
                        "choices": [{"text": "We'll look into it.", "next": None}],
                    },
                    "draws": {
                        "speaker": "Pilgrim Elder",
                        "text": "The Radiant Archive — manuscripts going back two thousand years. The reliquary. And the Cathedral itself, which the High Priest says was built on a site of power. I believe her.",
                        "choices": [{"text": "Thank you.", "next": None}],
                    },
                },
            },
        },
    ],

    "holy_knight": [
        {
            "conditions": [],
            "tree": {
                "id": "knight_default",
                "nodes": {
                    "start": {
                        "speaker": "Holy Knight",
                        "text": "The Order does not discuss its missions with outsiders. If you have business in Sanctum, conduct it and move on. The city is not a waystation.",
                        "choices": [
                            {"text": "We're hunting the Fading.", "next": "fading"},
                            {"text": "Just passing through.", "next": None},
                        ],
                    },
                    "fading": {
                        "speaker": "Holy Knight",
                        "text": "Then you have the Cathedral's support, if not its resources. Speak to the High Priest. She has been expecting someone like you — or hoping for it, at least. Second building on the left.",
                        "choices": [{"text": "Thank you.", "next": None}],
                    },
                },
            },
        },
    ],

    "novice_priest": [
        {
            "conditions": [],
            "tree": {
                "id": "novice_default",
                "nodes": {
                    "start": {
                        "speaker": "Novice Priest",
                        "text": "Oh! Visitors. I'm supposed to be sweeping the courtyard. If Sister Aldara sees me standing still she'll assign me another floor. She assigns things by observation.",
                        "choices": [
                            {"text": "What's it like here?", "next": "life"},
                            {"text": "We won't keep you.", "next": None},
                        ],
                    },
                    "life": {
                        "speaker": "Novice Priest",
                        "text": "Harder than I expected. More prayers, less sleep. But when the healing works — when someone walks out better than they came in — it's worth it. The High Priest says doubt is part of faith. I'm very faithful then.",
                        "choices": [{"text": "Honest answer.", "next": "honest"}],
                    },
                    "honest": {
                        "speaker": "Novice Priest",
                        "text": "She also says there's something coming that will test all of us. She says it quietly, late at night, to herself. I don't think she knows I can hear.",
                        "choices": [{"text": "She's right.", "next": None}],
                    },
                },
            },
        },
    ],

    "high_priest_aldara": [
        {
            "conditions": [{"flag": "lore.fading_basics", "op": "==", "value": True}],
            "tree": {
                "id": "aldara_knows",
                "nodes": {
                    "start": {
                        "speaker": "High Priest Aldara",
                        "text": "You've learned the truth of the Fading. Good. Denial is a luxury we can no longer afford. Sanctum sits on a ley convergence — if the Hearthstone network collapses, this city goes with it.",
                        "choices": [
                            {"text": "Can the Cathedral help?", "next": "help"},
                            {"text": "How much time do we have?", "next": "time"},
                        ],
                    },
                    "help": {
                        "speaker": "High Priest Aldara",
                        "text": "We can sustain the convergence point here if you can stabilize the others. The Reliquary holds an amplification relic — it would strengthen a Hearthstone if you find one. You may take it.",
                        "on_exit": [{"action": "set_flag", "flag": "lore.aldara_relic", "value": True}],
                        "choices": [{"text": "Thank you, High Priest.", "next": None}],
                    },
                    "time": {
                        "speaker": "High Priest Aldara",
                        "text": "Weeks if he accelerates extraction. Months if he hasn't found the deep nodes yet. I don't know which. Move as though it's weeks.",
                        "choices": [{"text": "We will.", "next": None}],
                    },
                },
            },
        },
        {
            "conditions": [],
            "tree": {
                "id": "aldara_default",
                "nodes": {
                    "start": {
                        "speaker": "High Priest Aldara",
                        "text": "Travelers. The Cathedral is open to those who seek the Light. If you seek something else — answers, guidance, healing — I may be able to help. Sanctum has been a place of knowledge longer than it has been a city.",
                        "choices": [
                            {"text": "What do you know about the Fading?", "next": "fading"},
                            {"text": "We need healing.", "next": "heal"},
                        ],
                    },
                    "fading": {
                        "speaker": "High Priest Aldara",
                        "text": "Everything. It's been the central concern of the Order for fifty years — we simply haven't had the courage to say so publicly. Come back when you've learned more. I will tell you what I can when I know you're committed.",
                        "choices": [{"text": "We're committed.", "next": "committed"}],
                    },
                    "committed": {
                        "speaker": "High Priest Aldara",
                        "text": "Then pursue the Hearthstones. Find the scholar Maren's research if you haven't already. The truth is all in there. Return when you have it.",
                        "choices": [{"text": "We will.", "next": None}],
                    },
                    "heal": {
                        "speaker": "High Priest Aldara",
                        "text": "The temple services are available to all who enter in good faith.",
                        "choices": [{"text": "Thank you.", "next": None}],
                    },
                },
            },
        },
    ],

    # ── Crystalspire ───────────────────────────────────────

    "apprentice_mage": [
        {
            "conditions": [],
            "tree": {
                "id": "app_mage_default",
                "nodes": {
                    "start": {
                        "speaker": "Apprentice Mage",
                        "text": "Third-year apprentice. I've been here long enough to know which professors to avoid and which theories are actually taught versus which ones get you failed. Both categories are interesting.",
                        "choices": [
                            {"text": "Which theories get you failed?", "next": "failed"},
                            {"text": "What's the Academy studying?", "next": "studying"},
                        ],
                    },
                    "failed": {
                        "speaker": "Apprentice Mage",
                        "text": "Ley line disruption. Hearthstone mechanics. Anything that implies the extraction program is causing damage. The administration gets very quiet when you raise those topics in seminar.",
                        "choices": [{"text": "Who's behind the silence?", "next": "silence"}],
                    },
                    "silence": {
                        "speaker": "Apprentice Mage",
                        "text": "The funding comes from the capital. And the capital's funding comes from someone who really doesn't want this research published. That's my theory. Written nowhere.",
                        "choices": [{"text": "Keep it that way.", "next": None}],
                    },
                    "studying": {
                        "speaker": "Apprentice Mage",
                        "text": "Officially? Crystallomancy, conjuration theory, the mechanics of the Arcane. Unofficially, Archmage Solen has been running a private project on ley resonance. He doesn't discuss it with students. At all.",
                        "choices": [{"text": "We should speak with Solen.", "next": None}],
                    },
                },
            },
        },
    ],

    "crystal_scholar": [
        {
            "conditions": [],
            "tree": {
                "id": "scholar_default",
                "nodes": {
                    "start": {
                        "speaker": "Crystal Scholar",
                        "text": "The crystals in this city aren't decorative. The whole district is built on a natural amplification node — the founders knew. Every building is aligned to the same axis. It's the largest unbroken arcane resonator in the known world.",
                        "on_enter": [{"action": "set_flag", "flag": "npc.crystal_scholar.met", "value": True}],
                        "choices": [
                            {"text": "What does that mean for the Fading?", "next": "fading"},
                            {"text": "Can it be used as a weapon?", "next": "weapon"},
                        ],
                    },
                    "fading": {
                        "speaker": "Crystal Scholar",
                        "text": "It means this city is both the most vulnerable and most defensible point in the region. If the ley network fails, the resonator collapses — Crystalspire goes dark in minutes. If it holds, it can sustain the network long past any single node failure.",
                        "choices": [{"text": "Which will it do?", "next": "which"}],
                    },
                    "which": {
                        "speaker": "Crystal Scholar",
                        "text": "Depends on what's taken from the network and what's left. The Archmage is trying to model it. I don't think he likes the projections.",
                        "choices": [{"text": "We need to speak with him.", "next": None}],
                    },
                    "weapon": {
                        "speaker": "Crystal Scholar",
                        "text": "Please don't.",
                        "choices": [{"text": "Fair enough.", "next": None}],
                    },
                },
            },
        },
    ],

    "archmage_solen": [
        {
            "conditions": [
                {"flag": "explored.abandoned_mine.floor3", "op": "==", "value": True},
                {"flag": "explored.sunken_crypt.floor2", "op": "==", "value": True},
                {"flag": "explored.ruins_ashenmoor.floor2", "op": "==", "value": True},
                {"flag": "quest.side_academy_research.state", "op": "!=", "value": -2},
            ],
            "tree": {
                "id": "solen_research_done",
                "nodes": {
                    "start": {
                        "speaker": "Archmage Solen",
                        "text": "You returned. And you have all three readings. Extraordinary — most adventurers wouldn't survive two of these sites, let alone three. Here is your payment, and my genuine gratitude.",
                        "on_enter": [
                            {"action": "complete_quest", "quest": "side_academy_research"},
                        ],
                        "choices": [{"text": "What does the data show?", "next": "data"},
                                    {"text": "Glad to help.", "next": None}],
                    },
                    "data": {
                        "speaker": "Archmage Solen",
                        "text": "Exactly what I feared. The ley resonance at each site has dropped by thirty to forty percent since my last readings. At this rate, the primary network fails within the year. We need those Hearthstones.",
                        "choices": [{"text": "Then we keep moving.", "next": None}],
                    },
                },
            },
        },
        {
            "conditions": [{"flag": "main_hearthstone_1.found", "op": "==", "value": True}],
            "tree": {
                "id": "solen_knows",
                "nodes": {
                    "start": {
                        "speaker": "Archmage Solen",
                        "text": "You found the first stone. Remarkable. I have spent forty years studying these — and feared they were all gone. Let me see it.",
                        "choices": [
                            {"text": "What can you tell us about it?", "next": "analyze"},
                            {"text": "How many are there?", "next": "count"},
                        ],
                    },
                    "analyze": {
                        "speaker": "Archmage Solen",
                        "text": "This one is from the Briarhollow vein. Still resonant — which means the network there hasn't fully collapsed. Each stone is unique to its node. Together they form a web. Without even one, the web... frays.",
                        "choices": [{"text": "How do we use them?", "next": "use"}],
                    },
                    "use": {
                        "speaker": "Archmage Solen",
                        "text": "Don't use them. Return them, or seal them from Valdris. The teleport circle here can help you move fast enough to get ahead of his agents. Talk to the Teleport Master.",
                        "choices": [{"text": "We will.", "next": None}],
                    },
                    "count": {
                        "speaker": "Archmage Solen",
                        "text": "Seven primary nodes in this region. He has at least two already. You have one. That leaves four. Whoever gets the remaining four first wins whatever this ends up being.",
                        "choices": [{"text": "We'll move fast.", "next": None}],
                    },
                },
            },
        },
        {
            "conditions": [],
            "tree": {
                "id": "solen_default",
                "nodes": {
                    "start": {
                        "speaker": "Archmage Solen",
                        "text": "I don't typically receive unannounced visitors. My time is limited. If you've come about the ley disruptions, speak quickly — I'm already late for something.",
                        "on_enter": [{"action": "set_flag", "flag": "npc.solen.met", "value": True}],
                        "choices": [
                            {"text": "The Hearthstones — what do you know?", "next": "stones"},
                            {"text": "What are the ley disruptions?", "next": "ley"},
                        ],
                    },
                    "stones": {
                        "speaker": "Archmage Solen",
                        "text": "More than anyone else alive, probably. They're ley crystallizations — natural nodes in the network that runs under this whole continent. Extracting them is like removing vertebrae from a spine. Do enough of it and the creature stops moving.",
                        "choices": [
                            {"text": "Someone is doing that now.", "next": "doing"},
                            {"text": "Can they be restored?", "next": "restore"},
                        ],
                    },
                    "doing": {
                        "speaker": "Archmage Solen",
                        "text": "I know. I've known for years. I sent three reports to the Imperial Council. Got back three letters thanking me for my service and telling me to stay in my lane. Whoever Valdris is, he has friends in high places.",
                        "choices": [{"text": "We don't answer to the Council.", "next": "free"}],
                    },
                    "free": {
                        "speaker": "Archmage Solen",
                        "text": "Then perhaps you can succeed where letters have failed. Find the stones — don't let him have them. Come back here when you do, the teleport circle can help you move faster than his agents. I also need ley readings from three Fading zones — dangerous work but vital for my models. I'll pay well.",
                        "on_enter": [
                            {"action": "start_quest", "quest": "main_thornhaven"},
                            {"action": "start_quest", "quest": "side_academy_research"},
                        ],
                        "choices": [{"text": "We'll return.", "next": None}],
                    },
                    "restore": {
                        "speaker": "Archmage Solen",
                        "text": "Theoretically. If you returned a stone to its original node, the resonance would rebuild. But the nodes themselves must still be intact — if Valdris has destroyed the physical site, restoration may not be possible.",
                        "choices": [{"text": "We'll work quickly.", "next": None}],
                    },
                    "ley": {
                        "speaker": "Archmage Solen",
                        "text": "The magical equivalent of a failing heart. The ley lines carry energy that sustains life, weather, growth. They've been weakening for decades. I think I know why, but proving it is another matter.",
                        "choices": [{"text": "The Hearthstones.", "next": "stones"}],
                    },
                },
            },
        },
    ],

    "teleport_master": [
        {
            "conditions": [{"flag": "npc.solen.met", "op": "==", "value": True}],
            "tree": {
                "id": "teleport_ready",
                "nodes": {
                    "start": {
                        "speaker": "Teleport Master",
                        "text": "The circle is operational. I maintain it personally — not the Academy, not the Guild. Me. The Archmage told me you might be coming. Where do you need to go?",
                        "choices": [
                            {"text": "Can you send us to Thornhaven?", "next": "thornhaven"},
                            {"text": "To Sanctum.", "next": "sanctum"},
                            {"text": "Not yet — we'll be back.", "next": None},
                        ],
                    },
                    "thornhaven": {
                        "speaker": "Teleport Master",
                        "text": "I can send you to the circle in the Mage's Hall there. It'll cost you twenty gold for the activation — pure material cost, no markup. Ready?",
                        "choices": [
                            {"text": "Ready.", "next": None},
                            {"text": "Not yet.", "next": None},
                        ],
                    },
                    "sanctum": {
                        "speaker": "Teleport Master",
                        "text": "Sanctum circle is maintained by the High Priest. Twenty gold. Ready?",
                        "choices": [
                            {"text": "Ready.", "next": None},
                            {"text": "Not yet.", "next": None},
                        ],
                    },
                },
            },
        },
        {
            "conditions": [],
            "tree": {
                "id": "teleport_default",
                "nodes": {
                    "start": {
                        "speaker": "Teleport Master",
                        "text": "The circle works. I don't run tours. If you have business with the Archmage and he's sent you here, fine. Otherwise I'm not in the habit of flinging strangers across the countryside.",
                        "choices": [
                            {"text": "The Archmage sent us.", "next": "archmage"},
                            {"text": "Understood.", "next": None},
                        ],
                    },
                    "archmage": {
                        "speaker": "Teleport Master",
                        "text": "Then get the clearance from him first. Come back with it. I'll be here.",
                        "choices": [{"text": "Fine.", "next": None}],
                    },
                },
            },
        },
    ],

    # ── Thornhaven ─────────────────────────────────────────

    "city_guard_thornhaven": [
        {
            "conditions": [],
            "tree": {
                "id": "guard_thornhaven",
                "nodes": {
                    "start": {
                        "speaker": "City Guard",
                        "text": "Keep your weapons sheathed in the capital. The city watch doesn't ask twice. You're registered with the Imperial Guild? Good. That makes this easier.",
                        "choices": [
                            {"text": "What's the situation in the city?", "next": "situation"},
                            {"text": "We understand.", "next": None},
                        ],
                    },
                    "situation": {
                        "speaker": "City Guard",
                        "text": "Tense. There are refugees from the eastern villages — hundreds came in last month. Nobody knows where the villages went. The Governor is managing public order but it's fragile. Don't start anything.",
                        "choices": [{"text": "We won't.", "next": None}],
                    },
                },
            },
        },
    ],

    "imperial_crier": [
        {
            "conditions": [],
            "tree": {
                "id": "crier_default",
                "nodes": {
                    "start": {
                        "speaker": "Imperial Crier",
                        "text": "HEAR YE! The Governor of Thornhaven invites all registered adventurers to the Imperial Guild Hall for contract work. REWARDS OFFERED for information on the eastern village disappearances. HEAR YE!",
                        "choices": [
                            {"text": "What happened to the villages?", "next": "villages"},
                            {"text": "Thank you.", "next": None},
                        ],
                    },
                    "villages": {
                        "speaker": "Imperial Crier",
                        "text": "Officially? Unknown. Unofficially? I've heard the word 'Fading' from three separate officers and a priest this week. Whatever it is, it's spreading west. Fast.",
                        "choices": [{"text": "We're handling it.", "next": None}],
                    },
                },
            },
        },
    ],

    "merchant_noble": [
        {
            "conditions": [],
            "tree": {
                "id": "noble_default",
                "nodes": {
                    "start": {
                        "speaker": "Merchant Noble",
                        "text": "The market disruptions are insufferable. My eastern supply routes are gone — three trade houses vanished with the villages. I've lost forty thousand gold in contracts this season alone.",
                        "choices": [
                            {"text": "People lost their lives.", "next": "lives"},
                            {"text": "Do you know what caused it?", "next": "cause"},
                        ],
                    },
                    "lives": {
                        "speaker": "Merchant Noble",
                        "text": "Yes, yes. Tragic. But the practical reality is the supply chain is broken and nobody in this city has a plan. At least I'm honest about why I'm upset.",
                        "choices": [{"text": "We're working on a plan.", "next": None}],
                    },
                    "cause": {
                        "speaker": "Merchant Noble",
                        "text": "I heard the name Valdris from a colleague who did trade with his operation for years. Then that colleague stopped responding to letters. Then his entire trading house closed. I don't investigate further than that.",
                        "choices": [{"text": "We will.", "next": None}],
                    },
                },
            },
        },
    ],

    "refugee": [
        {
            "conditions": [],
            "tree": {
                "id": "refugee_default",
                "nodes": {
                    "start": {
                        "speaker": "Refugee",
                        "text": "I'm from Ashford. It was a good village — hundred and forty people, mill, a chapel, everything proper. Then the ground went cold. The crops didn't come up. We woke up one morning and half the livestock were dead. We left.",
                        "choices": [
                            {"text": "What happened to those who stayed?", "next": "stayed"},
                            {"text": "Did you see anything strange?", "next": "strange"},
                        ],
                    },
                    "stayed": {
                        "speaker": "Refugee",
                        "text": "We don't talk about it.",
                        "choices": [{"text": "I'm sorry.", "next": None}],
                    },
                    "strange": {
                        "speaker": "Refugee",
                        "text": "The shadows moved wrong at night. And there was a sound — low, like something breathing underground. Very slow. Very big. Three days before we left it got louder every night. We stopped sleeping.",
                        "choices": [{"text": "We'll make sure it doesn't spread.", "next": "promise"}],
                    },
                    "promise": {
                        "speaker": "Refugee",
                        "text": "They all say that. No offense.",
                        "choices": [{"text": "None taken.", "next": None}],
                    },
                },
            },
        },
    ],

    "governor_aldric": [
        {
            "conditions": [{"flag": "boss_defeated.shadow_valdris", "op": "==", "value": True}],
            "tree": {
                "id": "aldric_post_valdris",
                "nodes": {
                    "start": {
                        "speaker": "Governor Aldric",
                        "text": "You've done it. I doubted you — I will admit that freely. The Empire has watched the east collapse for years and done nothing. You did something. Whatever comes next, the histories will note it.",
                        "choices": [
                            {"text": "Is it truly over?", "next": "over"},
                            {"text": "Valdris had help.", "next": "help"},
                        ],
                    },
                    "over": {
                        "speaker": "Governor Aldric",
                        "text": "The shadow he built — yes. What he uncovered about the Hearthstones, what he set in motion... that will take years to fully understand. But the immediate threat is gone. The land can start to heal.",
                        "choices": [{"text": "That's enough for now.", "next": None}],
                    },
                    "help": {
                        "speaker": "Governor Aldric",
                        "text": "I know. The Council inquiry is already underway. Some of those names will surprise people. Others won't. Let me handle that part — you've earned the rest.",
                        "choices": [{"text": "Don't let them bury it.", "next": None}],
                    },
                },
            },
        },
        {
            "conditions": [],
            "tree": {
                "id": "aldric_default",
                "nodes": {
                    "start": {
                        "speaker": "Governor Aldric",
                        "text": "I govern the capital and three hundred miles of territory, half of which is now silent. The eastern villages — gone. Thousands of people. No bodies, no struggle. The Empire calls it 'regional instability.' I call it a catastrophe.",
                        "on_enter": [{"action": "set_flag", "flag": "npc.governor.met", "value": True}],
                        "choices": [
                            {"text": "We know what's causing it.", "next": "know"},
                            {"text": "What resources do you have?", "next": "resources"},
                        ],
                    },
                    "know": {
                        "speaker": "Governor Aldric",
                        "text": "Then you know more than my intelligence reports. Tell me. I've been waiting two years for someone to come in here and say those words.",
                        "choices": [
                            {"text": "The Hearthstone extraction. Valdris.", "next": "valdris"},
                        ],
                    },
                    "valdris": {
                        "speaker": "Governor Aldric",
                        "text": "That name. It keeps appearing. He has Imperial letters — real ones. Someone in the Council signed off on his operations. I cannot move against him officially without evidence he hasn't buried. Can you get me that evidence?",
                        "choices": [{"text": "That's what we're doing.", "next": None}],
                    },
                    "resources": {
                        "speaker": "Governor Aldric",
                        "text": "Limited. The Imperial military won't act without an order from the Council. I have city guards, a treasury that's being bled by refugee costs, and an extremely good Guild Commander. The Guild is your best ally here.",
                        "choices": [{"text": "We'll work with them.", "next": None}],
                    },
                },
            },
        },
    ],

    "guild_commander_varek": [
        {
            "conditions": [],
            "tree": {
                "id": "varek_default",
                "nodes": {
                    "start": {
                        "speaker": "Guild Commander Varek",
                        "text": "Adventurers registered with the Imperial Guild get access to better contracts, better information, and my personal backing if things go sideways politically. If you're doing what I think you're doing, you'll want all three.",
                        "on_enter": [{"action": "set_flag", "flag": "npc.varek.met", "value": True}],
                        "choices": [
                            {"text": "What do you think we're doing?", "next": "think"},
                            {"text": "What contracts are available?", "next": "contracts"},
                        ],
                    },
                    "think": {
                        "speaker": "Guild Commander Varek",
                        "text": "Chasing Valdris. You have the look. Determined, tired, slightly haunted. I've seen it before — anyone who digs deep enough into the eastern question gets that look. Most of them stop digging.",
                        "choices": [
                            {"text": "We're not stopping.", "next": "not_stopping"},
                        ],
                    },
                    "not_stopping": {
                        "speaker": "Guild Commander Varek",
                        "text": "Good. I have an operative who's been tracking his supply routes for six months. I'll arrange a meeting. Don't mention this to the Council — half of them are his. When you're ready to move on the Spire, I can get you resources.",
                        "on_exit": [
                            {"action": "start_quest", "quest": "main_act3_spire"},
                            {"action": "set_flag", "flag": "lore.varek_contact", "value": True},
                        ],
                        "choices": [{"text": "Understood.", "next": None}],
                    },
                    "contracts": {
                        "speaker": "Guild Commander Varek",
                        "text": "Refugee escort work, mostly. Dangerous — the roads east are not safe. Also: information bounties on Valdris's operations. I pay well for verified intelligence. Better than you'd expect from a man with limited official authority.",
                        "choices": [{"text": "We'll check back.", "next": None}],
                    },
                },
            },
        },
    ],

    "court_mage_sira": [
        {
            "conditions": [],
            "tree": {
                "id": "sira_default",
                "nodes": {
                    "start": {
                        "speaker": "Court Mage Sira",
                        "text": "I've been waiting for the right moment to tell you something. The scholar you've been working with — Maren — her research is correct. More than she even knows. There's a second network beneath the primary one.",
                        "on_enter": [{"action": "set_flag", "flag": "npc.sira.met", "value": True}],
                        "choices": [
                            {"text": "A second network?", "next": "second"},
                            {"text": "How do you know?", "next": "how"},
                        ],
                    },
                    "second": {
                        "speaker": "Court Mage Sira",
                        "text": "The Hearthstone network everyone knows about is the visible layer. Beneath it is an older one — the original ley system, pre-human. Valdris doesn't know about it. Yet. If he discovers it, the primary network becomes irrelevant.",
                        "choices": [{"text": "What can we do about it?", "next": "do"}],
                    },
                    "do": {
                        "speaker": "Court Mage Sira",
                        "text": "Stabilize the primary network before he finds the secondary one. Every Hearthstone you protect buys us time to locate the deep nodes. The Archmage in Crystalspire has a theory about where they are.",
                        "choices": [{"text": "We've spoken to him.", "next": "solen"}],
                    },
                    "solen": {
                        "speaker": "Court Mage Sira",
                        "text": "Good. Between his models and my position here, we might actually map the full network before Valdris does. Come back to me when you have all the primary stones accounted for.",
                        "choices": [{"text": "We will.", "next": None}],
                    },
                    "how": {
                        "speaker": "Court Mage Sira",
                        "text": "I'm the court mage of the Empire's capital. I have access to archives that haven't been opened in four hundred years. The information was always there. Nobody thought to look.",
                        "choices": [{"text": "What does it mean for us?", "next": "second"}],
                    },
                },
            },
        },
    ],
}

# Merge into main NPC_DIALOGUES
NPC_DIALOGUES.update(_NEW_DIALOGUES)
