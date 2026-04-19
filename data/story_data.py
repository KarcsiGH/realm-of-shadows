"""
Realm of Shadows — Story Data

All narrative content: NPCs, dialogue trees, quest definitions,
lore entries, dungeon story events, and tavern rumors by act.
"""


# ═══════════════════════════════════════════════════════════════
#  OPENING NARRATIVE
# ═══════════════════════════════════════════════════════════════

OPENING_SEQUENCE = [
    ("", "Aldenmere is dying."),
    ("", "Not from war. Not from plague. From forgetting. "
         "Villages vanish overnight — not burned, not fled. "
         "Simply gone, as if they had never existed. "
         "People wake with no memory of their children's faces."),
    ("", "They call it the Fading."),
    ("", "The ancient wards that held the darkness at bay for a thousand years "
         "are failing. The Wardens who built them have been dead for generations. "
         "Their order is a myth. Their bloodlines, supposedly, extinct."),
    ("", "You know that last part isn't true."),
    ("", "You've always been different. Drawn to old places. "
         "Resistant to things that should hurt you. "
         "Haunted by a sense that something enormous is waiting just outside your sight."),
    ("", "Three days ago a woman named Maren found you in Briarhollow. "
         "She had a list of names — yours among them. "
         "She said: 'I have been looking for you for seven years. "
         "I am sorry it took this long. And I am sorry for what I am about to ask.'"),
    ("", "She's waiting at the tavern. "
         "Outside, the eastern sky is the wrong shade of grey. "
         "It's been that way for a week, and getting worse."),
    ("", "Whatever she asks — the answer is probably yes. "
         "You know that. You've known it since she said your name."),
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
        "reward_xp": 200,
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
        "reward_gold": 200,
        "reward_xp": 750,
        "reward_items": [{"name": "Healing Potion", "type": "consumable", "subtype": "potion", "heal_amount": 50, "description": "Restores 50 HP to one character.", "buy_price": 25, "sell_price": 10, "identified": True}],
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
        "reward_gold": 275,
        "reward_xp": 950,
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
        "reward_gold": 175,
        "reward_xp": 650,
        "reward_items": [{"name": "Antidote", "type": "consumable", "subtype": "potion", "cures": ["Poison"], "description": "Cures poison.", "buy_price": 15, "sell_price": 6, "identified": True}, {"name": "Antidote", "type": "consumable", "subtype": "potion", "cures": ["Poison"], "description": "Cures poison.", "buy_price": 15, "sell_price": 6, "identified": True}],
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
        "reward_gold": 120,
        "reward_xp": 250,
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
        "reward_gold": 160,
        "reward_xp": 380,
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
        "reward_gold": 375,
        "reward_xp": 1200,
        "reward_items": [{"name": "Healing Potion", "type": "consumable", "subtype": "potion", "heal_amount": 50, "description": "Restores 50 HP to one character.", "buy_price": 25, "sell_price": 10, "identified": True}],
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
        "reward_gold": 425,
        "reward_xp": 1450,
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
        "reward_gold": 475,
        "reward_xp": 1650,
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
        "reward_gold": 300,
        "reward_xp": 600,
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
        "reward_xp": 500,
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
        "reward_gold": 525,
        "reward_xp": 1800,
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
        "reward_gold": 300,
        "reward_xp": 600,
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
        "reward_gold": 500,
        "reward_xp": 850,
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
        "reward_gold": 650,
        "reward_xp": 2200,
        "reward_items": [],
        "objectives": [
            {
                "text": "Reach Valdris' Spire",
                "flag": "explored.valdris_spire.floor1", "op": "==", "val": True,
            },
        ],
    },

    "main_pale_coast": {
        "name": "The Fourth Stone",
        "description": "A Warden who chose exile sealed herself at the Pale Coast "
                       "rather than risk corruption. She still guards the fourth "
                       "Hearthstone. Whether you fight her or reason with her "
                       "may depend on how many stones you already carry.",
        "act": 3,
        "giver_npc": "Guild Commander Varek",
        "turn_in_npc": None,
        "auto_complete": True,
        "reward_gold": 750,
        "reward_xp": 2800,
        "reward_items": [{"id": "sirenne_buckler", "name": "Sentinel's Vow"}],
        "objectives": [
            {
                "text": "Recover the fourth Hearthstone from the Pale Coast Catacombs",
                "flag": "item.hearthstone.4", "op": "==", "val": True,
            },
        ],
    },

    "main_windswept_isle": {
        "name": "The Fifth Stone",
        "description": "The final Hearthstone is bound to the ruins of an old "
                       "ward-station on a windswept island. An elemental guardian "
                       "was bound there by the original order to protect it. "
                       "It has no reasoning — only purpose.",
        "act": 3,
        "giver_npc": "Guild Commander Varek",
        "turn_in_npc": None,
        "auto_complete": True,
        "reward_gold": 850,
        "reward_xp": 3300,
        "reward_items": [{"id": "keeper_pendant", "name": "The Nameless Keeper's Seal"}],
        "objectives": [
            {
                "text": "Recover the fifth Hearthstone from the Windswept Isle Ruins",
                "flag": "item.hearthstone.5", "op": "==", "val": True,
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
        "reward_gold": 1500,
        "reward_xp": 5000,
        "reward_items": [{"id": "warden_seal", "name": "The Last Warden's Seal"}],
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
    "elder_thom": {
        "name": "Elder Thom",
        "title": "Village Elder",
        "location": "briarhollow",
        "portrait_color": (150, 140, 120),  # aged grey
    },
    "captain_aldric": {
        "name": "Captain Aldric",
        "title": "Captain of the Briarhollow Patrol",
        "location": "briarhollow",
        "portrait_color": (140, 120, 80),  # weathered bronze
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
    "old_moss": {
        "name": "Old Moss",
        "title": "Forest Hermit",
        "location": "greenwood",
        "portrait_color": (60, 110, 50),
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
    "old_petra": {
        "name": "Old Petra",
        "title": "Briarhollow Elder",
        "location": "briarhollow",
        "portrait_color": (190, 180, 160),
    },
    "young_tomas": {
        "name": "Young Tomas",
        "title": "Local Youth",
        "location": "briarhollow",
        "portrait_color": (160, 195, 160),
    },
}


# ═══════════════════════════════════════════════════════════════
#  NPC DIALOGUE TREES
#  Each NPC has a list of dialogues ordered by priority.
#  The first one whose conditions pass is used.
# ═══════════════════════════════════════════════════════════════

NPC_DIALOGUES = {
    # ─────────────────────────────────────────────────────────
    #  WARDEN LIAISON — Rank system, guidance, badges
    #  Five conditional trees, evaluated in order (most advanced first)
    # ─────────────────────────────────────────────────────────
    "warden_liaison": [
        # ── Rank 4: Warden-Commander (endgame cleared) ──────────────
        {
            "conditions": [{"flag": "boss_defeated.shadow_valdris", "op": "==", "value": True}],
            "tree": {
                "id": "warden_rank4",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Warden Liaison",
                        "text": "Warden-Commander. The title sits heavier than it sounds.\nThe Spire is silent. The wards hold. I never thought I'd say that in my lifetime.",
                        "on_enter": [
                            {"action": "give_item",
                             "once_flag": "warden.badge4.given",
                             "item": {
                                "name": "Warden-Commander Badge",
                                "type": "misc", "slot": None,
                                "identified": True, "stack": 1,
                                "description": "A silver clasp bearing the crossed wards of the Warden-Commander rank. The highest honour the Order can bestow.",
                                "rarity": "epic",
                                "warden_rank": 4
                             }}
                        ],
                        "choices": [
                            {"text": "What happens to the Order now?", "next": "future"},
                            {"text": "Any threats I should watch for?", "next": "threats"},
                            {"text": "Farewell.", "next": None}
                        ]
                    },
                    "future": {
                        "speaker": "Warden Liaison",
                        "text": "The Order rebuilds. Slowly. There are six other Liaisons I know of still living — we'll need every one of them.\nYou've bought us time. Use it.",
                        "choices": [{"text": "We will.", "next": None}]
                    },
                    "threats": {
                        "speaker": "Warden Liaison",
                        "text": "The Fading recedes, but doesn't vanish overnight. The outer settlements — Thornhaven's eastern roads, the Pale Coast villages — will see echoes for months.\nKeep your weapons sharp.",
                        "choices": [{"text": "Understood.", "next": None}]
                    }
                }
            }
        },
        # ── Rank 3: Senior Warden (5th hearthstone recovered) ───────
        {
            "conditions": [{"flag": "item.hearthstone.5", "op": "==", "value": True}],
            "tree": {
                "id": "warden_rank3",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Warden Liaison",
                        "text": "Five Hearthstones. All of them.\nI'm authorised to present you with the rank of Senior Warden. Take this.",
                        "on_enter": [
                            {"action": "give_item",
                             "once_flag": "warden.badge3.given",
                             "item": {
                                "name": "Senior Warden Badge",
                                "type": "misc", "slot": None,
                                "identified": True, "stack": 1,
                                "description": "A deep green enamel badge bearing three ward-runes. Marks the bearer as a keeper of the deeper wards.",
                                "rarity": "rare",
                                "warden_rank": 3
                             }}
                        ],
                        "choices": [
                            {"text": "What's left?", "next": "valdris"},
                            {"text": "What does this rank mean?", "next": "rank_meaning"},
                            {"text": "Thank you.", "next": None}
                        ]
                    },
                    "valdris": {
                        "speaker": "Warden Liaison",
                        "text": "Valdris' Spire. That's what's left.\nThe wards are almost restored — but they need someone to seal them from the inside. Valdris knows the ritual. Whether he'll help or fight you, I cannot say.\nThe Spire is north-east of Thornhaven. Find it.",
                        "choices": [{"text": "We'll go.", "next": None}]
                    },
                    "rank_meaning": {
                        "speaker": "Warden Liaison",
                        "text": "Four bonus to all attributes, ten percent more health, five percent more damage. The Order's deepest wards augment those who carry its mark.\nMore importantly — it means the Order trusts you with its secrets.",
                        "choices": [{"text": "We won't waste it.", "next": None}]
                    }
                }
            }
        },
        # ── Rank 2: Warden (3rd hearthstone recovered) ──────────────
        {
            "conditions": [{"flag": "item.hearthstone.3", "op": "==", "value": True}],
            "tree": {
                "id": "warden_rank2",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Warden Liaison",
                        "text": "Three Hearthstones recovered. The old Wardens would be proud — if any of them were still alive to say it.\nI'm raising your designation to Warden. Formally.",
                        "on_enter": [
                            {"action": "give_item",
                             "once_flag": "warden.badge2.given",
                             "item": {
                                "name": "Warden Badge",
                                "type": "misc", "slot": None,
                                "identified": True, "stack": 1,
                                "description": "A green-lacquered iron badge bearing the twin ward-runes. Standard issue for a confirmed Warden.",
                                "rarity": "uncommon",
                                "warden_rank": 2
                             }}
                        ],
                        "choices": [
                            {"text": "Where are the remaining Hearthstones?", "next": "remaining"},
                            {"text": "What should we watch out for?", "next": "dangers"},
                            {"text": "Thank you.", "next": None}
                        ]
                    },
                    "remaining": {
                        "speaker": "Warden Liaison",
                        "text": "Two left. The Windswept Isle, off the Pale Coast — sea travel required, probably from Pale Coast Harbor.\n"
                                "But before you sail — return to Briarhollow. "
                                "Something is building there. My scouts have seen shadow-touched activity "
                                "near the village perimeter. If Briarhollow falls, we lose our earliest "
                                "supply line. Go back. Secure it. Then the Isle.",
                        "choices": [{"text": "We'll head to the coast.", "next": None}]
                    },
                    "dangers": {
                        "speaker": "Warden Liaison",
                        "text": "The Governor's men are growing bolder. I've seen Imperial patrols pushing into areas they have no business in — near the Pale Coast, near the old mine roads.\nSomeone is directing them. Be careful who you trust in Thornhaven.",
                        "choices": [{"text": "Noted.", "next": None}]
                    }
                }
            }
        },
        # ── Post-Sunken Crypt: HS2 recovered, Dragon's Tooth next ────
        {
            "conditions": [
                {"flag": "item.hearthstone.2", "op": "==", "value": True},
                {"flag": "item.hearthstone.3", "op": "!=", "value": True},
            ],
            "tree": {
                "id": "warden_post_sunken_crypt",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Warden Liaison",
                        "text": "Two Hearthstones. You came back from the Sunken Crypt.\n"
                                "The Warden who guarded that fragment held for a long time. "
                                "Longer than anyone had a right to ask.\n"
                                "Three remain. Dragon's Tooth is next — volcanic island, "
                                "off the southern coast. Sea passage from Saltmere. "
                                "The dockhand Riv can arrange the route — mention the Wardens.",
                        "choices": [
                            {"text": "What should we expect on Dragon's Tooth?", "next": "dragons_tooth"},
                            {"text": "Any other threats we should know about?",   "next": "threats"},
                            {"text": "We head to Saltmere.",                       "next": None},
                        ],
                    },
                    "dragons_tooth": {
                        "speaker": "Warden Liaison",
                        "text": "Volcanic. The Fading has been drawn there — heat and shadow "
                                "make for strange combinations.\n"
                                "The fragment there predates the Order. Whatever is guarding it "
                                "is old. Don't assume the rules you've learned still apply.",
                        "choices": [{"text": "Understood.", "next": None}],
                    },
                    "threats": {
                        "speaker": "Warden Liaison",
                        "text": "Imperial patrols have been pushing further east. Someone is "
                                "directing them — and that someone knows where the Hearthstones are.\n"
                                "Be careful in Thornhaven. Not everyone the Governor trusts "
                                "deserves to be trusted.",
                        "choices": [{"text": "We'll be careful.", "next": None}],
                    },
                },
            },
        },
        # ── Post-Ashenmoor: Ruins cleared, Act 2 mid ────────────────
        {
            "conditions": [
                {"flag": "boss_defeated.ruins_ashenmoor", "op": "==", "value": True},
                {"flag": "item.hearthstone.3",            "op": "!=", "value": True},
            ],
            "tree": {
                "id": "warden_post_ashenmoor",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Warden Liaison",
                        "text": "Ashenmoor cleared. The Commander's Log confirms what we suspected "
                                "about Valdris — I've already sent word to the other Liaisons.\n"
                                "And you have the Crypt Amulet — the ward-key from the Commander. "
                                "The Sunken Crypt entrance will open for you now. "
                                "It's beneath the Pale Coast, flooded passages, old Warden anchor site. "
                                "Second Hearthstone is inside.\n"
                                "Dragon's Tooth after that — volcanic island, needs sea passage. "
                                "Saltmere is your port for both.",
                        "choices": [
                            {"text": "How do we get to Saltmere?",    "next": "saltmere"},
                            {"text": "What's in the Sunken Crypt?",   "next": "crypt"},
                            {"text": "We'll head to the coast.",       "next": None},
                        ],
                    },
                    "saltmere": {
                        "speaker": "Warden Liaison",
                        "text": "Coastal town south of the Pale Coast highlands. "
                                "There's a dockhand named Riv who arranges passage — "
                                "mention the Wardens and he'll know what you need. "
                                "Don't overpay.",
                        "choices": [{"text": "Understood.", "next": None}],
                    },
                    "crypt": {
                        "speaker": "Warden Liaison",
                        "text": "A drowned Warden stronghold. The garrison there tried to "
                                "seal the Hearthstone fragment when the Fading reached them — "
                                "they didn't make it out. "
                                "Whatever's guarding it now has had centuries to settle in.",
                        "choices": [{"text": "We'll be ready.", "next": None}],
                    },
                },
            },
        },
        # ── Rank 1: Scout (1st hearthstone recovered) ───────────────
        {
            "conditions": [{"flag": "item.hearthstone.1", "op": "==", "value": True}],
            "tree": {
                "id": "warden_rank1",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Warden Liaison",
                        "text": "You recovered the first Hearthstone. I wasn't sure you'd make it back.\nThe Order recognises your service. Scout rank — take this badge.",
                        "on_enter": [
                            {"action": "give_item",
                             "once_flag": "warden.badge1.given",
                             "item": {
                                "name": "Scout Badge",
                                "type": "misc", "slot": None,
                                "identified": True, "stack": 1,
                                "description": "A grey iron badge bearing a single ward-rune. Marks the bearer as a recognised Scout of the Warden Order.",
                                "rarity": "common",
                                "warden_rank": 1
                             }}
                        ],
                        "choices": [
                            {"text": "Where should we go next?", "next": "guidance"},
                            {"text": "What is the Scout rank?", "next": "rank_info"},
                            {"text": "Thank you.", "next": None}
                        ]
                    },
                    "guidance": {
                        "speaker": "Warden Liaison",
                        "text": "Four Hearthstones remain. Maren will know more than I do about their locations.\nWhat I know: the Ruins of Ashenmoor first — south-west. Clear it. The Commander there holds a Crypt Amulet — a ward-key the old Order used to seal the Sunken Crypt. Without it, the Crypt entrance won't open, no matter what you try.\nOnce you have the amulet, the Sunken Crypt opens. It's beneath the Pale Coast, flooded passages, dangerous. After that, two sea crossings — Saltmere is the port.\nBefore any of that — visit Sanctum to the east. High Priest Aldara holds records from the old Order. Don't skip her.",
                        "choices": [{"text": "We'll find them.", "next": None}]
                    },
                    "rank_info": {
                        "speaker": "Warden Liaison",
                        "text": "Scout rank grants one point to all attributes and a small experience bonus. The Order's mark strengthens those who carry it — the deeper your rank, the stronger the effect.\nProve yourself on the remaining Hearthstones.",
                        "choices": [
                            {"text": "We will.", "next": None},
                            {"text": "How do warriors advance beyond their starting class?", "next": "class_advance"},
                        ]
                    },
                    "class_advance": {
                        "speaker": "Warden Liaison",
                        "text": "Around level ten, a warrior's base training is complete. Two paths exist from there.\n"
                                "The first: deepen into a true apex class — a Fighter becomes a Knight, a Mage becomes an Archmage. Pure mastery.\n"
                                "The second: merge two disciplines. A Fighter who has trained under a Cleric can become a Paladin — drawing on both, transcending either.\n"
                                "Visit any Guild and look at the Abilities board. The options appear there when your people are ready.",
                        "choices": [{"text": "We'll visit the Guild.", "next": None}],
                    }
                }
            }
        },
        # ── Rank 0.4: Reached Ironhearth — Act 1 late ──────────────
        {
            "conditions": [{"flag": "town.ironhearth.visited", "op": "==", "value": True},
                           {"flag": "boss_defeated.spiders_nest", "op": "!=", "value": True}],
            "tree": {
                "id": "warden_ironhearth",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Warden Liaison",
                        "text": "You made it to Ironhearth. The dwarves don't trust outsiders easily "
                                "— if they're talking to you, you've earned something.\n"
                                "The Spider's Nest to the northwest still needs clearing. "
                                "You have the map. Use it.",
                        "choices": [
                            {"text": "What's in the nest?", "next": "nest"},
                            {"text": "What comes after?", "next": "after"},
                            {"text": "We're working on it.", "next": None},
                        ],
                    },
                    "nest": {
                        "speaker": "Warden Liaison",
                        "text": "A brood queen and her spawn. The Fading has accelerated her growth "
                                "unnaturally — she's larger and more aggressive than any spider "
                                "has a right to be. Kill her and the brood collapses.\n"
                                "There's a Hearthstone fragment in that cave. The spiders are "
                                "nesting around it.",
                        "choices": [{"text": "We'll clear it.", "next": None}],
                    },
                    "after": {
                        "speaker": "Warden Liaison",
                        "text": "The Abandoned Mine north of Ironhearth. A former Warden garrison "
                                "held it — they didn't make it out. The first Hearthstone "
                                "fragment is sealed inside. You'll need the mine key from the "
                                "Spider's Nest to get in.",
                        "choices": [{"text": "One thing at a time.", "next": None}],
                    },
                },
            },
        },
        # ── Rank 0.3: Spider's Nest cleared ─────────────────────────
        {
            "conditions": [{"flag": "boss_defeated.spiders_nest", "op": "==", "value": True},
                           {"flag": "boss_defeated.abandoned_mine", "op": "!=", "value": True}],
            "tree": {
                "id": "warden_post_spiders",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Warden Liaison",
                        "text": "The Spider's Nest cleared. I've had three patrols confirm it "
                                "— the northwest trail is open again.\n"
                                "The mine key you recovered opens the Abandoned Mine north "
                                "of Ironhearth. That's your next target. The first Hearthstone "
                                "fragment is inside — a Fallen Warden named Korrath is guarding it.",
                        "choices": [
                            {"text": "Tell me about Korrath.", "next": "korrath"},
                            {"text": "What happened to the garrison?", "next": "garrison"},
                            {"text": "We're headed there now.", "next": None},
                        ],
                    },
                    "korrath": {
                        "speaker": "Warden Liaison",
                        "text": "Senior Warden. One of the last. When the Order fell apart, "
                                "some held their posts out of duty. Some out of madness. "
                                "Korrath stayed in the mine. The Fading got to him eventually.\n"
                                "He's not what he was. But he was a Warden. If you can reach "
                                "him before the fight, there may be a way to resolve this without "
                                "destroying what's left of him.",
                        "choices": [{"text": "We'll try.", "next": None}],
                    },
                    "garrison": {
                        "speaker": "Warden Liaison",
                        "text": "The mine was a critical ward anchor point. When the wards "
                                "began failing, the garrison stayed to hold the anchor manually. "
                                "One by one the Fading took them. Korrath was the last.\n"
                                "They died doing their job. The least we can do is finish it.",
                        "choices": [{"text": "We will.", "next": None}],
                    },
                },
            },
        },
        # ── Rank 0.2: Goblin Warren cleared ─────────────────────────
        {
            "conditions": [{"flag": "boss_defeated.goblin_warren", "op": "==", "value": True},
                           {"flag": "boss_defeated.spiders_nest", "op": "!=", "value": True}],
            "tree": {
                "id": "warden_post_warren",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Warden Liaison",
                        "text": "The Warren is clear. I didn't expect results this quickly.\n"
                                "The map fragment you recovered from Grak marks a cave to the "
                                "northwest — the Spider's Nest. That's your next objective. "
                                "There's a Hearthstone fragment inside, protected by a brood queen.",
                        "choices": [
                            {"text": "Why was Grak holding a map?", "next": "map"},
                            {"text": "How do we get to the Spider's Nest?", "next": "directions"},
                            {"text": "We're already moving.", "next": None},
                        ],
                    },
                    "map": {
                        "speaker": "Warden Liaison",
                        "text": "Goblins are territorial and surprisingly methodical about "
                                "documenting their territory. The Warren is directly connected "
                                "to the Thornwood trail system.\n"
                                "The map shows the web cave to the northwest — the Spider's Nest. "
                                "Grak was avoiding it. Wise, in his way.",
                        "choices": [{"text": "Northwest. Got it.", "next": None}],
                    },
                    "directions": {
                        "speaker": "Warden Liaison",
                        "text": "Head northwest from Woodhaven along the Thornwood path. "
                                "Follow the old trail markers — you'll smell the webs before "
                                "you see them. The entrance is about a day's travel from here.",
                        "choices": [{"text": "Understood.", "next": None}],
                    },
                },
            },
        },
        # ── Rank 0.1: Met Maren, before Goblin Warren ────────────────
        {
            "conditions": [{"flag": "npc.maren.met", "op": "==", "value": True},
                           {"flag": "boss_defeated.goblin_warren", "op": "!=", "value": True}],
            "tree": {
                "id": "warden_post_maren",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Warden Liaison",
                        "text": "You found Maren. Good. She understands the Hearthstone "
                                "mechanics better than anyone alive — you'll want her guidance.\n"
                                "The Goblin Warren east of Briarhollow is your first target. "
                                "The goblin raids are being driven by Fading pressure — clearing "
                                "the Warren will reveal what's behind it.",
                        "choices": [
                            {"text": "What can you tell us about the Warren?", "next": "warren_info"},
                            {"text": "Why are the goblins raiding?", "next": "goblins"},
                            {"text": "We're on our way there.", "next": None},
                        ],
                    },
                    "warren_info": {
                        "speaker": "Warden Liaison",
                        "text": "Three floors. Mixed goblin forces — shamans in the back, "
                                "warriors up front. Their king, Grak, commands from the deepest "
                                "level.\nThe Fading is strong near the lower floors. "
                                "Watch for shadow-touched creatures mixed in with the regular troops.",
                        "choices": [{"text": "Any weaknesses?", "next": "weakness"}],
                    },
                    "weakness": {
                        "speaker": "Warden Liaison",
                        "text": "Goblin shamans disrupt spellcasting if you let them. "
                                "Take them out before they can establish a hex. "
                                "Grak himself is dangerous in rage — hit him hard before he "
                                "gets a chance to build up.",
                        "choices": [{"text": "We'll be ready.", "next": None}],
                    },
                    "goblins": {
                        "speaker": "Warden Liaison",
                        "text": "The Fading moves creatures like a flood moves debris — "
                                "everything runs ahead of it. The goblins aren't raiding "
                                "because they want to. They're raiding because something worse "
                                "is behind them.\nClear the Warren and you'll find out what.",
                        "choices": [{"text": "We understand.", "next": None}],
                    },
                },
            },
        },
        # ── Cross-town quest hints: active main quest → where to go ─
        # These run BEFORE the rank-0 fallback so players who have wandered
        # into a different town than the quest giver still get pointed at the
        # right town and NPC. The first matching tree wins, so they are
        # ordered from latest quest backward (later quests take priority
        # if multiple are somehow active at once).
        #
        # Pattern per tree:
        #   conditions: quest state is active (not 0, not -2)
        #                AND the next prereq flag is not yet set
        #   tree: one-node hint telling the player where to go next
        {
            "conditions": [
                {"flag": "quest.main_act3_finale.state", "op": ">=", "value": 1},
                {"flag": "quest.main_act3_finale.state", "op": "!=", "value": -2},
            ],
            "tree": {
                "id": "hint_act3_finale",
                "nodes": {
                    "start": {
                        "speaker": "Warden Liaison",
                        "text": "All five Hearthstones recovered. The Spire's approach "
                                "will let you through now.\n"
                                "The summit is where it ends. Ascend the Spire — "
                                "Valdris is waiting. Or what's left of him.",
                        "choices": [{"text": "We're ready.", "next": None}]
                    }
                }
            }
        },
        # Windswept Isle is active but Pale Coast not yet cleared — send them to Pale Coast first.
        # (windswept_isle requires pale_coast_cleared key internally.)
        {
            "conditions": [
                {"flag": "quest.main_windswept_isle.state", "op": ">=", "value": 1},
                {"flag": "quest.main_windswept_isle.state", "op": "!=", "value": -2},
                {"flag": "boss_defeated.pale_coast",        "op": "not_exists"},
            ],
            "tree": {
                "id": "hint_windswept_isle_blocked",
                "nodes": {
                    "start": {
                        "speaker": "Warden Liaison",
                        "text": "The Windswept Isle is out there, yes — but the storms "
                                "around it won't let a ship through. Not yet.\n"
                                "The Pale Coast Catacombs have to fall first. A Warden "
                                "sealed inside holds what calms the storms.\n"
                                "South of Saltmere, on the peninsula. Guild Commander "
                                "Varek in Thornhaven has the approach charts.",
                        "choices": [{"text": "Pale Coast first. Got it.", "next": None}]
                    }
                }
            }
        },
        {
            "conditions": [
                {"flag": "quest.main_windswept_isle.state", "op": ">=", "value": 1},
                {"flag": "quest.main_windswept_isle.state", "op": "!=", "value": -2},
                {"flag": "boss_defeated.windswept_isle",    "op": "not_exists"},
            ],
            "tree": {
                "id": "hint_windswept_isle",
                "nodes": {
                    "start": {
                        "speaker": "Warden Liaison",
                        "text": "With the Pale Coast cleared, the storms around the "
                                "Windswept Isle will calm enough for a ship to land.\n"
                                "Sail from Briarhollow Docks, Saltmere Docks, or Pale "
                                "Coast Dock. The fifth Hearthstone is in the ruins there.",
                        "choices": [{"text": "Understood.", "next": None}]
                    }
                }
            }
        },
        {
            "conditions": [
                {"flag": "quest.main_pale_coast.state", "op": ">=", "value": 1},
                {"flag": "quest.main_pale_coast.state", "op": "!=", "value": -2},
                {"flag": "boss_defeated.pale_coast",    "op": "not_exists"},
            ],
            "tree": {
                "id": "hint_pale_coast",
                "nodes": {
                    "start": {
                        "speaker": "Warden Liaison",
                        "text": "The Pale Coast Catacombs hold the fourth Hearthstone.\n"
                                "South of Saltmere, out on the peninsula. "
                                "Pale Coast Dock is the jumping-off point — "
                                "reachable from any of the three main ports by sea.\n"
                                "A Warden sealed herself in there decades ago to "
                                "guard the stone. Approach carefully. Guild "
                                "Commander Varek in Thornhaven knows more if you "
                                "want the full briefing.",
                        "choices": [{"text": "South of Saltmere. Understood.", "next": None}]
                    }
                }
            }
        },
        {
            "conditions": [
                {"flag": "quest.main_act3_spire.state", "op": ">=", "value": 1},
                {"flag": "quest.main_act3_spire.state", "op": "!=", "value": -2},
                {"flag": "boss_defeated.valdris_spire", "op": "not_exists"},
            ],
            "tree": {
                "id": "hint_act3_spire",
                "nodes": {
                    "start": {
                        "speaker": "Warden Liaison",
                        "text": "Valdris' Spire stands in the Ashlands to the north. "
                                "You'll need all five Hearthstones before the approach "
                                "will let you through.\n"
                                "Speak with Guild Commander Varek in Thornhaven — "
                                "he's coordinating the Order's final push.",
                        "choices": [{"text": "We'll see him.", "next": None}]
                    }
                }
            }
        },
        {
            "conditions": [
                {"flag": "quest.main_act2_pursuit.state", "op": ">=", "value": 1},
                {"flag": "quest.main_act2_pursuit.state", "op": "!=", "value": -2},
            ],
            "tree": {
                "id": "hint_act2_pursuit",
                "nodes": {
                    "start": {
                        "speaker": "Warden Liaison",
                        "text": "Maren left in a hurry — north, toward Valdris' Spire.\n"
                                "Whatever she took, she's not planning on giving back. "
                                "Your fastest route is through Thornhaven — "
                                "Guild Commander Varek can arrange your next steps.",
                        "choices": [{"text": "We'll go.", "next": None}]
                    }
                }
            }
        },
        {
            "conditions": [
                {"flag": "quest.main_maren_truth.state", "op": ">=", "value": 1},
                {"flag": "quest.main_maren_truth.state", "op": "!=", "value": -2},
            ],
            "tree": {
                "id": "hint_maren_truth",
                "nodes": {
                    "start": {
                        "speaker": "Warden Liaison",
                        "text": "Court Mage Sira in Thornhaven spoke with you — "
                                "now go back and confront Maren. "
                                "She'll be at the Wanderer's Rest in Briarhollow, "
                                "same as always.\n"
                                "Don't let her leave until she answers.",
                        "choices": [{"text": "We'll find her.", "next": None}]
                    }
                }
            }
        },
        {
            "conditions": [
                {"flag": "quest.main_thornhaven.state", "op": ">=", "value": 1},
                {"flag": "quest.main_thornhaven.state", "op": "!=", "value": -2},
            ],
            "tree": {
                "id": "hint_thornhaven",
                "nodes": {
                    "start": {
                        "speaker": "Warden Liaison",
                        "text": "Archmage Solen in Crystalspire sent you east — "
                                "Governor Aldric of Thornhaven is waiting for your report.\n"
                                "Thornhaven is the capital. Take the road east through "
                                "Crystalspire and the Imperial checkpoints will wave you through "
                                "once you show the Archmage's seal.",
                        "choices": [{"text": "We'll travel east.", "next": None}]
                    }
                }
            }
        },
        {
            "conditions": [
                {"flag": "quest.main_hearthstone_3.state",  "op": ">=", "value": 1},
                {"flag": "quest.main_hearthstone_3.state",  "op": "!=", "value": -2},
                {"flag": "boss_defeated.dragons_tooth",     "op": "not_exists"},
            ],
            "tree": {
                "id": "hint_hearthstone_3",
                "nodes": {
                    "start": {
                        "speaker": "Warden Liaison",
                        "text": "Dragon's Tooth — volcanic island to the far east. "
                                "The third Hearthstone is in the caldera.\n"
                                "Sea passage only. Speak with Dockhand Riv at "
                                "Saltmere Docks. He runs the Tiderunner route; "
                                "he'll take you once you've cleared the Sunken Crypt.",
                        "choices": [{"text": "We'll find Riv.", "next": None}]
                    }
                }
            }
        },
        {
            "conditions": [
                {"flag": "quest.main_hearthstone_2.state",  "op": ">=", "value": 1},
                {"flag": "quest.main_hearthstone_2.state",  "op": "!=", "value": -2},
                {"flag": "boss_defeated.sunken_crypt",      "op": "not_exists"},
            ],
            "tree": {
                "id": "hint_hearthstone_2",
                "nodes": {
                    "start": {
                        "speaker": "Warden Liaison",
                        "text": "The Sunken Crypt holds the second Hearthstone.\n"
                                "Tide Priest Oran in Saltmere is the one to speak with — "
                                "the crypt is just off the coast there, and he knows "
                                "the old wards that keep it sealed.",
                        "choices": [{"text": "Saltmere, then.", "next": None}]
                    }
                }
            }
        },
        {
            "conditions": [
                {"flag": "quest.main_ashenmoor.state",  "op": ">=", "value": 1},
                {"flag": "quest.main_ashenmoor.state",  "op": "!=", "value": -2},
                {"flag": "boss_defeated.ruins_ashenmoor", "op": "not_exists"},
            ],
            "tree": {
                "id": "hint_ashenmoor",
                "nodes": {
                    "start": {
                        "speaker": "Warden Liaison",
                        "text": "The Ruins of Ashenmoor lie east of the Abandoned Mine — "
                                "follow the road past Ironhearth until the trees die out.\n"
                                "Maren in Briarhollow has the context you'll need. "
                                "Check in with her before and after.",
                        "choices": [{"text": "We will.", "next": None}]
                    }
                }
            }
        },
        {
            "conditions": [
                {"flag": "quest.main_spiders_nest.state",  "op": ">=", "value": 1},
                {"flag": "quest.main_spiders_nest.state",  "op": "!=", "value": -2},
                {"flag": "boss_defeated.spiders_nest",     "op": "not_exists"},
            ],
            "tree": {
                "id": "hint_spiders_nest",
                "nodes": {
                    "start": {
                        "speaker": "Warden Liaison",
                        "text": "Elder Theron of Woodhaven asked for help with the spiders.\n"
                                "The Spider's Nest is in the Thornwood west of Woodhaven. "
                                "When you've cleared it, bring word back to Maren "
                                "in Briarhollow — she'll want to hear what you saw.",
                        "choices": [{"text": "Understood.", "next": None}]
                    }
                }
            }
        },
        {
            "conditions": [
                {"flag": "quest.main_hearthstone_1.state",  "op": ">=", "value": 1},
                {"flag": "quest.main_hearthstone_1.state",  "op": "!=", "value": -2},
                {"flag": "boss_defeated.abandoned_mine",    "op": "not_exists"},
            ],
            "tree": {
                "id": "hint_hearthstone_1",
                "nodes": {
                    "start": {
                        "speaker": "Warden Liaison",
                        "text": "Maren sent you after the first Hearthstone. "
                                "The Abandoned Mine is north of Ironhearth.\n"
                                "You'll need the Mine Key — the Spider Queen carries it. "
                                "Clear the Spider's Nest first if you haven't.",
                        "choices": [{"text": "North of Ironhearth. Got it.", "next": None}]
                    }
                }
            }
        },
        {
            "conditions": [
                {"flag": "quest.main_goblin_warren.state",  "op": ">=", "value": 1},
                {"flag": "quest.main_goblin_warren.state",  "op": "!=", "value": -2},
                {"flag": "boss_defeated.goblin_warren",     "op": "not_exists"},
            ],
            "tree": {
                "id": "hint_goblin_warren",
                "nodes": {
                    "start": {
                        "speaker": "Warden Liaison",
                        "text": "Maren sent you to the Goblin Warren. It's east of "
                                "Briarhollow, through the forest — the goblins carved "
                                "tunnels into an old warren.\n"
                                "Clear it out and return to Maren at the Wanderer's Rest.",
                        "choices": [{"text": "East of Briarhollow.", "next": None}]
                    }
                }
            }
        },
        {
            "conditions": [
                {"flag": "quest.main_meet_maren.state",  "op": ">=", "value": 1},
                {"flag": "quest.main_meet_maren.state",  "op": "!=", "value": -2},
            ],
            "tree": {
                "id": "hint_meet_maren",
                "nodes": {
                    "start": {
                        "speaker": "Warden Liaison",
                        "text": "Elder Thom mentioned a scholar — Maren. She's staying "
                                "at the Wanderer's Rest inn in Briarhollow.\n"
                                "If you're serious about this work, she's the one to talk to first.",
                        "choices": [{"text": "Briarhollow, then.", "next": None}]
                    }
                }
            }
        },
        # ── Rank 0: Initiate (first meeting, gives starter badge) ───
        {
            "conditions": [],
            "tree": {
                "id": "warden_rank0",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Warden Liaison",
                        "text": "You have the look of people who've answered the old call.\nI'm a Liaison of the Warden Order — we track those who take up the work. If you're serious, take this. It marks you as Initiates.",
                        "on_enter": [
                            {"action": "give_item",
                             "once_flag": "warden.badge0.given",
                             "item": {
                                "name": "Warden Initiate Badge",
                                "type": "misc", "slot": None,
                                "identified": True, "stack": 1,
                                "description": "A worn leather badge bearing the Warden mark. Simple, but it opens certain doors.",
                                "rarity": "common",
                                "warden_rank": 0
                             }}
                        ],
                        "choices": [
                            {"text": "What should we do first?", "next": "first_steps"},
                            {"text": "What is the Warden Order?", "next": "about_order"},
                            {"text": "What's happening to the land?", "next": "the_fading"},
                            {"text": "Thanks.", "next": None}
                        ]
                    },
                    "first_steps": {
                        "speaker": "Warden Liaison",
                        "text": "There's a scholar named Maren in Briarhollow. She's been studying the land sickness longer than anyone I know of. Find her first.\nThe Abandoned Mine is north of Ironhearth — but don't go alone and don't go unprepared — but don't go alone and don't go unprepared.",
                        "choices": [{"text": "We'll find Maren.", "next": None}]
                    },
                    "about_order": {
                        "speaker": "Warden Liaison",
                        "text": "An old guild. We maintained the wards that kept the Shadow Realm from bleeding into ours.\nWe failed two hundred years ago. Most of the Order died in the collapse. What you see now is what survives — Liaisons like me, spread thin across the settlements, watching.",
                        "choices": [
                            {"text": "What do we need to do?", "next": "first_steps"},
                            {"text": "Understood.", "next": None}
                        ]
                    },
                    "the_fading": {
                        "speaker": "Warden Liaison",
                        "text": "The wards that hold the Shadow Realm at bay are failing. When they fail completely, the world dissolves — people, stone, memory, all of it.\nFive Hearthstone fragments once anchored the wards. They were scattered. Recovering them is the only path I know of.",
                        "choices": [
                            {"text": "Where do we start?", "next": "first_steps"},
                            {"text": "That's grim.", "next": None}
                        ]
                    }
                }
            }
        },
    ],

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
                "locked": True,
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
        # After goblin warren — peaceful resolution (Grak spared)
        # Checked BEFORE the kill path so it takes priority when both flags exist
        {
            "conditions": [
                {"flag": "choice.grak_spared",          "op": "==", "value": True},
                {"flag": "boss_defeated.goblin_warren",  "op": "==", "value": True},
                {"flag": "quest.main_goblin_warren.state", "op": "!=", "value": -2},
            ],
            "tree": {
                "id": "maren_post_warren_peaceful",
                "nodes": {
                    "start": {
                        "speaker": "Maren",
                        "text": "You're back. I expected... I don't know what I expected. "
                                "But not this. The goblins are calm. The scouts say they've "
                                "stopped raiding entirely.\nWhat happened in that Warren?",
                        "choices": [
                            {"text": "Grak was protecting a Hearthstone fragment. We made peace.",
                             "next": "peace_truth",
                             "conditions": [{"flag": "lore.grak_truth", "op": "==", "value": True}]},
                            {"text": "We found a way to end the fighting without bloodshed.",
                             "next": "peace_simple"},
                        ],
                    },
                    "peace_truth": {
                        "speaker": "Maren",
                        "text": "He was... protecting it.\n"
                                "The goblins weren't driven mad by the Fading — they were guarding "
                                "against it. A Warden must have given the fragment to them generations "
                                "ago, and Grak honoured that trust.\n"
                                "This changes things. The old Wardens didn't just fight the Fading — "
                                "they made alliances. Built networks.\n"
                                "We need to find the others. The Abandoned Mine is our next step.",
                        "on_enter": [
                            {"action": "complete_quest", "quest": "main_goblin_warren"},
                            {"action": "start_quest", "quest": "main_hearthstone_1"},
                            {"action": "discover_lore", "lore": "warden_alliances"},
                        ],
                        "end": True,
                    },
                    "peace_simple": {
                        "speaker": "Maren",
                        "text": "Without bloodshed. I admit I didn't think that was possible once "
                                "the raids started.\n"
                                "The goblins were protecting something in that Warren — something "
                                "connected to the Fading. That's what matters.\n"
                                "We need to keep moving. The Abandoned Mine is our next destination.",
                        "on_enter": [
                            {"action": "complete_quest", "quest": "main_goblin_warren"},
                            {"action": "start_quest", "quest": "main_hearthstone_1"},
                        ],
                        "end": True,
                    },
                },
            },
        },
        # After goblin warren — kill path (Grak defeated in combat)
        {
            "conditions": [
                {"flag": "choice.grak_killed",          "op": "==", "value": True},
                {"flag": "boss_defeated.goblin_warren",  "op": "==", "value": True},
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
                                "move faster.\n"
                                "Head north from Woodhaven to the Spider's Nest next — the colony "
                                "has been blocking the road to Ironhearth. Clear it, and the way "
                                "to the Abandoned Mine opens up.",
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
                {"flag": "boss.korrath.defeated",      "op": "==",        "value": True},
                {"flag": "maren.post_mine_spoken",     "op": "not_exists"},
            ],
            "tree": {
                "id": "maren_post_mine",
                "nodes": {
                    "start": {
                        "speaker": "Maren",
                        "text": "You made it back from the mine. I felt something shift — "
                                "in the air, in the wards. You found it, didn't you?\n"
                                "A Hearthstone fragment.",
                        "on_enter": [
                            {"action": "set_flag", "flag": "maren.post_mine_spoken", "value": True},
                        ],
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
                        "text": "One fragment recovered. Four still to go — I know that now.\n"
                                "Two things. First: Sanctum, to the east. "
                                "High Priest Aldara keeps the old Warden records there — "
                                "she may know the exact location of the remaining fragments "
                                "and what's guarding them. Don't skip her.\n"
                                "Second: the Ruins of Ashenmoor. Something's been active there. "
                                "Not alive, exactly — but aware. "
                                "Whatever's left in those ruins saw what Valdris did.\n"
                                "One more thing — important. The Sunken Crypt is your next Hearthstone after Ashenmoor, "
                                "but the entrance is warded. Sealed with an old Order lock. "
                                "The ward-key is a Crypt Amulet — I believe it's still in Ashenmoor. "
                                "Don't try the Crypt without it. The entrance won't open.",
                        "on_enter": [{"action": "start_quest", "quest": "main_ashenmoor"}],
                        "end": True,
                    },
                },
            },
        },
        # After Sunken Crypt cleared — HS2 found, Dragon's Tooth next
        {
            "conditions": [
                {"flag": "boss_defeated.sunken_crypt",  "op": "==",        "value": True},
                {"flag": "boss_defeated.dragons_tooth", "op": "!=",        "value": True},
                {"flag": "maren.post_crypt_spoken",     "op": "not_exists"},
            ],
            "tree": {
                "id": "maren_post_sunken_crypt",
                "nodes": {
                    "start": {
                        "speaker": "Maren",
                        "text": "Two stones. You made it back from the Crypt.\n"
                                "The Sunken Warden — I've read about the garrison that went down "
                                "with the crypt. They knew the Fading was coming and they stayed.\n"
                                "What happened in there?",
                        "on_enter": [
                            {"action": "set_flag", "flag": "maren.post_crypt_spoken", "value": True},
                        ],
                        "choices": [
                            {"text": "The Warden guardian was still at his post.",  "next": "warden_held"},
                            {"text": "The Fading had been there a long time.",      "next": "fading_old"},
                            {"text": "We have the stone. That's what matters.",     "next": "just_the_stone"},
                            {"text": "Farewell.",                                   "next": None},
                        ],
                    },
                    "warden_held": {
                        "speaker": "Maren",
                        "text": "Of course he did. That's what they did — the old ones. "
                                "Bound themselves to the anchors and waited.\n"
                                "I used to think that was heroic. Now I think it was the Order "
                                "asking too much of people who couldn't say no.\n"
                                "Dragon's Tooth next. Volcanic island, south of Saltmere. "
                                "The fragment there is old — older than the Order itself.",
                        "choices": [{"text": "We sail from Saltmere.", "next": None}],
                    },
                    "fading_old": {
                        "speaker": "Maren",
                        "text": "The coast took the Fading early. Tidal — it spread along the "
                                "waterways. The crypt was one of the first places to go dark.\n"
                                "The fragment survived because the Warden sealed it properly. "
                                "Whatever else the Order did wrong, they built things that lasted.\n"
                                "Dragon's Tooth is next. Sea passage from Saltmere — ask for Riv.",
                        "choices": [{"text": "We head south.", "next": None}],
                    },
                    "just_the_stone": {
                        "speaker": "Maren",
                        "text": "Fair enough. I'll take what you don't want to talk about.\n"
                                "Two stones. Three to go. Dragon's Tooth — volcanic island "
                                "south of here, sea passage from Saltmere.\n"
                                "I'll be here when you get back.",
                        "choices": [{"text": "We sail south.", "next": None}],
                    },
                },
            },
        },
        # After Ruins of Ashenmoor cleared — Ashvar defeated, Valdris betrayal confirmed
        {
            "conditions": [
                {"flag": "boss.ashvar.defeated",        "op": "==",        "value": True},
                {"flag": "maren.post_ashvar_spoken",    "op": "not_exists"},
            ],
            "tree": {
                "id": "maren_post_ashenmoor",
                "nodes": {
                    "start": {
                        "speaker": "Maren",
                        "text": "You've been to Ashenmoor. I can see it in how you're standing.\n"
                                "What did you find?",
                        "on_enter": [
                            {"action": "set_flag", "flag": "maren.post_ashvar_spoken", "value": True},
                        ],
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
                                "I'm beginning to understand what he meant by it.\n"
                                "The Crypt Amulet you recovered from the Commander — that's the ward-key. "
                                "The Sunken Crypt entrance is sealed with old Order magic; "
                                "the Amulet is what opens it. You can go there now.\n"
                                "After the Crypt — Dragon's Tooth, volcanic island to the south. "
                                "Both need sea passage. Saltmere is the port.",
                        "on_enter": [
                            {"action": "complete_quest", "quest": "main_ashenmoor"},
                            {"action": "set_flag", "flag": "maren.ashenmoor_revelation", "value": True},
                        ],
                        "choices": [
                            {"text": "We head to Saltmere.", "next": None},
                        ],
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
                        "text": "Two Hearthstones left — the Pale Coast and the Windswept Isle. "
                                "Both need sea passage.\n"
                                "Saltmere is the port. It's south along the coast road. "
                                "Find the dockhand there — ask about passage to the Pale Coast first, "
                                "then the Isle beyond it. "
                                "We don't have time to do them in the wrong order.\n"
                                "Move fast. The attack on Briarhollow was a message — "
                                "Valdris knows we have three fragments and he's running out of patience.",
                        "on_enter": [
                            {"action": "set_flag", "flag": "maren.post_attack_spoken", "value": True},
                        ],
                        "choices": [{"text": "We head to Saltmere.", "next": None}],
                    },
                },
            },
        },
        # After Spider's Nest cleared — turn-in for main_spiders_nest
        {
            "conditions": [
                {"flag": "boss_defeated.spiders_nest", "op": "==",        "value": True},
                {"flag": "maren.spiders_spoken",       "op": "not_exists"},
            ],
            "tree": {
                "id": "maren_post_spiders",
                "nodes": {
                    "start": {
                        "speaker": "Maren",
                        "text": "The Spider's Nest. I could feel the corruption easing "
                                "when you killed the queen — the Fading had taken root in her, "
                                "accelerated the whole colony's growth. "
                                "It's spreading through anything living near the ley lines. "
                                "You stopped one thread. There are more.",
                        "on_enter": [
                            {"action": "set_flag", "flag": "maren.spiders_spoken", "value": True},
                            {"action": "complete_quest", "quest": "main_spiders_nest"},
                        ],
                        "choices": [
                            {"text": "The queen was enormous. Unnatural.", "next": "unnatural"},
                            {"text": "The corruption is in the animals too?", "next": "animals"},
                            {"text": "What's our next move?", "next": "mine_nav"},
                        ],
                    },
                    "mine_nav": {
                        "speaker": "Maren",
                        "text": "The queen had a key on her — an iron mine key. "
                                "The Abandoned Mine north of Ironhearth. That's where we go next.\n"
                                "Stock up in Ironhearth before you enter — the dwarves have "
                                "better provisions than anywhere else at this range, "
                                "and the mine is deeper than it looks.",
                        "end": True,
                    },
                    "unnatural": {
                        "speaker": "Maren",
                        "text": "Yes. The Fading doesn't kill — not at first. "
                                "It warps. Makes things grow beyond their nature, "
                                "feeds on the energy they produce, then collapses them. "
                                "Like a fire that burns its own fuel. "
                                "The mine will be the same if we don't act.",
                        "end": True,
                    },
                    "animals": {
                        "speaker": "Maren",
                        "text": "Everything near a ley disruption. The goblins, the spiders, "
                                "the wolves Captain Aldric mentioned. They're not rabid — "
                                "they're corrupted. Driven by something they can't understand "
                                "or escape. That's what makes this worse than a plague. "
                                "A plague you can quarantine.",
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
                                "Three stones. Two more to find.\n"
                                "Before we sail again — we need to go back to Briarhollow. "
                                "I've been getting reports. Shadow activity near the village, "
                                "more than the usual Fading pressure. Something is being directed there.\n"
                                "If we ignore it and it falls, we lose everything behind us. "
                                "Briarhollow first. Then the Pale Coast.",
                        "on_enter": [
                            {"action": "set_flag", "flag": "maren.post_dragon_spoken", "value": True},
                        ],
                        "choices": [{"text": "Briarhollow. Then the coast.", "next": None}],
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
                                "for years. The first lead points to the Goblin Warren — it's just to the northwest of here. "
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
        # When goblin_warren complete but mine quest hasn't been cleared yet —
        # give a contextual "what's next" pointing at the Abandoned Mine
        # (prevents maren_default from saying "The Warren..." after it's done)
        {
            "conditions": [
                {"flag": "quest.main_goblin_warren.state", "op": "==", "value": -2},
                {"flag": "quest.main_hearthstone_1.state", "op": "==", "value": 1},
                {"flag": "boss_defeated.abandoned_mine", "op": "not_exists"},
            ],
            "tree": {
                "id": "maren_post_warren_hint",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Maren",
                        "text": "The Warren is clear \u2014 good. But the Fading runs deeper. "
                                "There's an old mine northwest of here. The goblins were hauling "
                                "crates marked with the Warden seal out of it.\n\n"
                                "Whatever they were doing in there matters. That's your next move.",
                        "choices": [
                            {"text": "The Abandoned Mine. Understood.", "next": "understood"},
                            {"text": "What do you know about the Wardens?", "next": "wardens"},
                            {"text": "Goodbye.", "next": None},
                        ]
                    },
                    "understood": {
                        "speaker": "Maren",
                        "text": "Northeast of the forest road. You'll need to pass the Thornwood. "
                                "Stay on the main trail \u2014 the trees are wrong there at night.",
                        "choices": [
                            {"text": "We'll find it.", "next": None},
                        ]
                    },
                    "wardens": {
                        "speaker": "Maren",
                        "text": "The last order to stand against the Fading. They failed \u2014 "
                                "or we thought they did.\n\n"
                                "The fragment Grak had was Warden-made. If there are more, "
                                "they're in that mine.",
                        "choices": [{"text": "We'll go.", "next": None}],
                    },
                }
            }
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
        # Turn-in: missing patrol journal found in goblin warren
        {
            "conditions": [
                {"flag": "quest.side_missing_patrol.state", "op": ">=", "value": 2},
                {"flag": "quest.side_missing_patrol.state", "op": "!=", "value": -2},
            ],
            "tree": {
                "id": "rowan_patrol_turnin",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Captain Rowan",
                        "text": "You found the journal? So they're gone. All six of them. "
                                "I'll need a moment. The road just... wasn't there anymore. "
                                "That's not wolves or goblins — that's something else entirely.\n"
                                "Thank you for bringing it back. Their families deserved to know.",
                        "on_enter": [{"action": "complete_quest", "quest": "side_missing_patrol"}],
                        "choices": [
                            {"text": "The Fading took the road. It's spreading.", "next": "fading"},
                            {"text": "We're sorry for your loss.", "next": "sorry"},
                        ],
                    },
                    "fading": {
                        "speaker": "Captain Rowan",
                        "text": "The Fading. Maren's word for it. I thought it was superstition. "
                                "Now I don't know what to believe. How do you fight something "
                                "that erases roads?",
                        "choices": [{"text": "That's what we're trying to find out.", "next": None}],
                    },
                    "sorry": {
                        "speaker": "Captain Rowan",
                        "text": "So am I. Good soldiers. Keep moving — I'll handle the paperwork. "
                                "You have bigger problems to deal with.",
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
                "id": "rowan_wolf_turnin",
                "nodes": {
                    "start": {
                        "speaker": "Captain Rowan",
                        "text": "You've got the pelts? Good. The tanner's been waiting. "
                                "Here's your coin — well earned.",
                        "on_enter": [
                            {"action": "complete_quest", "quest": "side_wolf_pelts"},
                        ],
                        "choices": [{"text": "Happy to help.", "next": None}],
                    },
                },
            },
        },
        # Post-warren: goblin warren cleared, road to Woodhaven safer
        {
            "conditions": [
                {"flag": "boss_defeated.goblin_warren", "op": "==", "value": True},
                {"flag": "boss_defeated.abandoned_mine", "op": "not_exists"},
            ],
            "tree": {
                "id": "rowan_post_warren",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Captain Rowan",
                        "text": "The Warren is clear. My scouts confirmed it this morning — "
                                "the eastern road to Woodhaven is passable again for the first "
                                "time in months.\n"
                                "If you're heading north, the road's safer than it was. "
                                "I'd still travel in daylight.",
                        "choices": [
                            {"text": "Good to know.", "next": None},
                            {"text": "What's in Woodhaven?", "next": "woodhaven"},
                        ],
                    },
                    "woodhaven": {
                        "speaker": "Captain Rowan",
                        "text": "Lumber town. Elder Theron runs it — sensible man. "
                                "They've had their own troubles with the Spider's Nest to the north. "
                                "If Maren's right about what's in that mine, "
                                "Woodhaven is your best staging point.",
                        "choices": [{"text": "We'll head there.", "next": None}],
                    },
                },
            },
        },
        # Post-mine: abandoned mine cleared
        {
            "conditions": [{"flag": "boss_defeated.abandoned_mine", "op": "==", "value": True}],
            "tree": {
                "id": "rowan_post_mine",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Captain Rowan",
                        "text": "You cleared the mine. I won't pretend I thought you'd pull it off. "
                                "The townsfolk are sleeping better. I suppose I owe you a drink.",
                        "choices": [
                            {"text": "What happens to the mine now?", "next": "mine_fate"},
                            {"text": "Just doing our job.", "next": "modest"},
                        ],
                    },
                    "mine_fate": {
                        "speaker": "Captain Rowan",
                        "text": "The Guild wants to reopen it. I say leave it sealed. "
                                "Whatever Valdris was doing down there — I don't want it under "
                                "our feet again. But nobody asks guards.",
                        "choices": [{"text": "Thanks, Captain.", "next": None}],
                    },
                    "modest": {
                        "speaker": "Captain Rowan",
                        "text": "Don't be modest. Half my garrison wouldn't have gone in. "
                                "Take the compliment.",
                        "choices": [{"text": "We'll be moving on soon.", "next": None}],
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
                        "text": "The wolves are worse than usual this season — driving them off would help. "
                                "Bring me five pelts as proof and I'll see you compensated. "
                                "Beyond that, clear the roads and every beast you put down helps.",
                        "on_enter": [{"action": "start_quest", "quest": "side_wolf_pelts"}],
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
        # ── Act 3: after Spire known / explored ──────────────────────
        {
            "conditions": [
                {"flag": "maren.left",              "op": "==", "value": True},
                {"flag": "explored.valdris_spire.floor1", "op": "==", "value": True},
            ],
            "tree": {
                "id": "bess_act3_spire",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Bess",
                        "text": "You've been to the Spire, then. I can see it on you.\n"
                                "A traveller came through yesterday — said the tower wards "
                                "are still active. Whatever Maren went in to stop, "
                                "it hasn't happened yet. There's still time.",
                        "on_enter": [{"action": "meet_npc", "npc": "bess"}],
                        "choices": [
                            {"text": "Have you heard anything else about the Spire?",
                             "next": "spire_word"},
                            {"text": "We'll bring her back if we can.", "next": "bring_back"},
                            {"text": "Just checking in.", "next": "bye"},
                        ],
                    },
                    "spire_word": {
                        "speaker": "Bess",
                        "text": "Only what travellers bring through, and most of them are "
                                "too frightened to go near the Ashlands.\n"
                                "One thing stands out: no one who's gone in has come out. "
                                "But the wards pulse every few hours, like a heartbeat. "
                                "Whatever is happening in there, it isn't finished.",
                        "next": "start",
                    },
                    "bring_back": {
                        "speaker": "Bess",
                        "text": "That's all I ask. She paid for three more nights "
                                "when she left — in advance.\n"
                                "I think that was her way of saying she planned to come back.",
                        "next": "bye",
                    },
                    "bye": {
                        "speaker": "Bess",
                        "text": "The Rusty Flagon will be here when you're done. "
                                "It always is.",
                        "end": True,
                    },
                },
            },
        },
        # ── After Maren leaves (Act 2+) ──────────────────────────────
        {
            "conditions": [{"flag": "maren.left", "op": "==", "value": True}],
            "tree": {
                "id": "bess_post_maren",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Bess",
                        "text": "She left before dawn. Paid her tab in full — in advance, "
                                "actually, which surprised me. Maren didn't seem like someone "
                                "who planned to leave. Something must have pushed her.",
                        "on_enter": [{"action": "meet_npc", "npc": "bess"}],
                        "choices": [
                            {"text": "Did she say anything before she went?", "next": "last_words"},
                            {"text": "Do you know where she went?", "next": "where_she_went"},
                            {"text": "Was she alone?", "next": "alone"},
                            {"text": "Any word from the road since?", "next": "road_word"},
                            {"text": "Thanks, Bess.", "next": "bye"},
                        ],
                    },
                    "last_words": {
                        "speaker": "Bess",
                        "text": "She came down before first light and left a note on the bar. "
                                "Just said: 'Tell them I'm sorry. Tell them I know what I'm doing.' "
                                "I don't know who 'them' was. I figure it was you.",
                        "next": "start",
                    },
                    "where_she_went": {
                        "speaker": "Bess",
                        "text": "The note she left said one thing clearly: 'Find me at the Spire.' "
                                "I don't know what that means, but a merchant who passed through "
                                "yesterday said there's a black tower far out in the Ashlands — "
                                "Valdris' Spire, they call it. Sounds like where she was headed. "
                                "You'll need whatever opened the crypt to get there, I'd wager. "
                                "She had that look — the one that means she's already planned past you.",
                        "next": "start",
                    },
                    "alone": {
                        "speaker": "Bess",
                        "text": "As far as I could tell. One bedroll, one satchel. "
                                "She took all her maps and journals — left nothing behind "
                                "except that note and a lot of unanswered questions.",
                        "next": "start",
                    },
                    "road_word": {
                        "speaker": "Bess",
                        "text": "A carter passed through from the Ashlands — said the tower "
                                "wards are still active. 'Pulsing like a second sun,' "
                                "his words.\n"
                                "That means whatever she went to stop hasn't happened yet. "
                                "She hasn't failed. Go find her.",
                        "next": "start",
                    },
                    "bye": {
                        "speaker": "Bess",
                        "text": "Find her before she does something she can't undo. "
                                "That's my only request.",
                        "end": True,
                    },
                },
            },
        },
        # ── After meeting Maren but before she leaves (Act 1) ────────
        {
            "conditions": [{"flag": "npc.maren.met", "op": "==", "value": True}],
            "tree": {
                "id": "bess_knows_maren",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Bess",
                        "text": "Your scholar friend is still at it — maps spread across "
                                "the whole table, candles burning past midnight. "
                                "Whatever she's looking for, she won't stop until she finds it. "
                                "Can I get you anything?",
                        "on_enter": [{"action": "meet_npc", "npc": "bess"}],
                        "choices": [
                            {"text": "What's the talk in town these days?", "next": "rumors"},
                            {"text": "Has Maren said anything useful?", "next": "maren_talk"},
                            {"text": "Just a drink and a moment's quiet.", "next": "bye"},
                        ],
                    },
                    "rumors": {
                        "speaker": "Bess",
                        "text": "Old Petra's been complaining about giant spider silk on the "
                                "path to the Thornwood. Not normal size — thick as rope, she says. "
                                "Half the village thinks she's losing her mind. "
                                "The other half won't go near that road after dark.",
                        "next": "start",
                    },
                    "maren_talk": {
                        "speaker": "Bess",
                        "text": "She keeps to herself mostly. Once she said something about "
                                "'the land remembering what people forget.' I didn't press her. "
                                "Some guests you let talk, some you let think. She's the second kind.",
                        "next": "start",
                    },
                    "bye": {
                        "speaker": "Bess",
                        "text": "Coming right up. Rest while you can.",
                        "end": True,
                    },
                },
            },
        },
        # ── Default (first arrival, no Maren met yet) ─────────────────
        {
            "conditions": [],
            "tree": {
                "id": "bess_default",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Bess",
                        "text": "Welcome to the Rusty Flagon. You look like you could use "
                                "a drink and a warm bed. Or are you here for the gossip?",
                        "on_enter": [{"action": "meet_npc", "npc": "bess"}],
                        "choices": [
                            {"text": "What's the word around town?", "next": "rumors"},
                            {"text": "Is there a scholar staying here?", "next": "about_maren"},
                            {"text": "Just passing through.", "next": "bye"},
                        ],
                    },
                    "rumors": {
                        "speaker": "Bess",
                        "text": "Strange times. The farmers say their crops are wilting even "
                                "with rain. Old Tam swears he saw his barn fade like a mirage "
                                "and come back an hour later. And those goblins — they look "
                                "scared, not angry. Whatever's out there, it frightens them too.",
                        "next": "start",
                    },
                    "about_maren": {
                        "speaker": "Bess",
                        "text": "Maren? Arrived a fortnight ago. Quiet, pays on time, "
                                "spends all day with her books and maps. She asked about you lot "
                                "before you even got here — knew you were coming somehow. "
                                "Gives me the chills, if I'm honest. She's in the corner if you want to speak with her.",
                        "next": "start",
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
    #  OLD PETRA — Briarhollow townsfolk, Spider's Nest hook
    # ─────────────────────────────────────────────────────────
    "old_petra": [
        # Hearthstone 1 found
        {
            "conditions": [{"flag": "item.hearthstone.1", "op": "==", "value": True}],
            "tree": {"id": "petra_hearthstone", "loop": True, "nodes": {
                "start": {"speaker": "Old Petra",
                    "text": "A Hearthstone fragment. I heard you found one in the Mine. "
                            "My grandmother used to speak of them — she said they were "
                            "older than the kingdom, older than the Warden Order, older "
                            "than anything she could name. She died before I understood "
                            "what she meant. I think I understand now.",
                    "choices": [
                        {"text": "What did she say about them?", "next": "grandmother"},
                        {"text": "There are more to find.", "next": None},
                    ]},
                "grandmother": {"speaker": "Old Petra",
                    "text": "She said the Hearthstones don't store power — they store "
                            "memory. The land's memory. When they fail, the land starts "
                            "to forget itself. The Fading isn't a disease. It's amnesia.",
                    "on_enter": [{"action": "discover_lore", "lore": "hearthstone_memory"}],
                    "choices": [{"text": "That's a remarkable thing to know.", "next": None}]},
            }},
        },
        # Act 1 complete
        {
            "conditions": [{"flag": "boss_defeated.abandoned_mine", "op": "==", "value": True}],
            "tree": {"id": "petra_act1_done", "loop": True, "nodes": {
                "start": {"speaker": "Old Petra",
                    "text": "Three dungeons cleared. The Warren, the spider cave, the Mine. "
                            "I've lived here sixty years and the town has never been this safe. "
                            "I can hear the difference at night — fewer sounds from the forest. "
                            "Fewer wrong sounds.",
                    "choices": [
                        {"text": "The Fading is still spreading though.", "next": "fading"},
                        {"text": "Stay vigilant. It's not over.", "next": None},
                    ]},
                "fading": {"speaker": "Old Petra",
                    "text": "I know. I can smell it on the east wind. Something burning that "
                            "isn't fire. It's been getting closer for months. Whatever you're "
                            "doing — keep doing it.",
                    "choices": [{"text": "We will.", "next": None}]},
            }},
        },
        # After goblin warren
        {
            "conditions": [{"flag": "boss_defeated.goblin_warren", "op": "==", "value": True}],
            "tree": {"id": "petra_post_warren", "loop": True, "nodes": {
                "start": {"speaker": "Old Petra",
                    "text": "I've lived on this square for sixty years. I know every face "
                            "and every fence post. I saw the goblins start their raids twelve "
                            "years ago — small thefts first, then worse. "
                            "You've done what the militia couldn't. "
                            "What happens to their warren now?",
                    "choices": [
                        {"text": "It's cleared. Won't be a problem.", "next": "cleared"},
                        {"text": "Something was driving them out of it.", "next": "driving"},
                    ]},
                "cleared": {"speaker": "Old Petra",
                    "text": "Good. The Thornwood trail's been impassable for two seasons. "
                            "My granddaughter lives in Woodhaven — I haven't been able to "
                            "visit. That matters more to me than any goblin chief.",
                    "choices": [{"text": "The road should be safer now.", "next": None}]},
                "driving": {"speaker": "Old Petra",
                    "text": "Something worse. I worried about that. The forest has been "
                            "wrong for longer than the goblin trouble. The two are connected.",
                    "choices": [{"text": "We think so too.", "next": None}]},
            }},
        },
        # Default
        {
            "conditions": [],
            "tree": {"id": "petra_default", "loop": True, "nodes": {
                "start": {"speaker": "Old Petra",
                    "text": "I've lived on this square for sixty years. I know every face "
                            "and every fence post. And I know something's wrong with the "
                            "Thornwood path east of here.",
                    "on_enter": [{"action": "meet_npc", "npc": "old_petra"}],
                    "choices": [
                        {"text": "What's wrong with the Thornwood path?", "next": "path"},
                        {"text": "How long has it been like this?", "next": "duration"},
                        {"text": "We'll look into it.", "next": None},
                    ]},
                "path": {"speaker": "Old Petra",
                    "text": "Goblins, mostly. The Warren east of town has been raiding the "
                            "road for two seasons. But there's something else — animals "
                            "acting strange. Too quiet, then too loud. Wrong.",
                    "choices": [{"text": "We'll investigate.", "next": None}]},
                "duration": {"speaker": "Old Petra",
                    "text": "Two seasons for the raids. But the forest has been wrong for "
                            "longer than that — three years at least. Since the first Fading "
                            "reports from the east.",
                    "choices": [{"text": "We'll look into it.", "next": None}]},
            }},
        },
    ],

    # ─────────────────────────────────────────────────────────
    #  YOUNG TOMAS — Briarhollow townsfolk, world-building
    # ─────────────────────────────────────────────────────────
    "young_tomas": [
        # Act 1 complete — Mine cleared, he's inspired
        {
            "conditions": [{"flag": "boss_defeated.abandoned_mine", "op": "==", "value": True}],
            "tree": {"id": "tomas_act1_done", "loop": True, "nodes": {
                "start": {"speaker": "Young Tomas",
                    "text": "You cleared the mine! And the spider cave AND the goblin warrens? "
                            "Mister Gareth at the smithy said a party like yours only comes along "
                            "once a generation. Are you going to keep going? Where are you going next?",
                    "choices": [
                        {"text": "East. There are more places like that.", "next": "east"},
                        {"text": "We go where we're needed.", "next": "needed"},
                        {"text": "Stay safe, Tomas.", "next": None},
                    ]},
                "east": {"speaker": "Young Tomas",
                    "text": "East is where the Fading is worst. My dad used to say you could see it "
                            "at night — a darkness that moved wrong. He stopped talking about it. "
                            "I think it scared him. I think it should scare you too. But I'm glad "
                            "someone's going.",
                    "choices": [{"text": "It should scare us. That's healthy.", "next": None}]},
                "needed": {"speaker": "Young Tomas",
                    "text": "My mother says that. 'Go where you're needed, Tomas.' She means the "
                            "market, not abandoned mines full of monsters. I think you're doing "
                            "it right though.",
                    "choices": [{"text": "Your mother sounds wise.", "next": None}]},
            }},
        },
        # Spider's Nest cleared
        {
            "conditions": [{"flag": "boss_defeated.spiders_nest", "op": "==", "value": True}],
            "tree": {"id": "tomas_post_spiders", "loop": True, "nodes": {
                "start": {"speaker": "Young Tomas",
                    "text": "You killed the spider queen! Old Brennan the cartographer told me "
                            "she was as big as a house. Is that true? Were you scared?",
                    "choices": [
                        {"text": "She was enormous. Yes, we were scared.", "next": "honest"},
                        {"text": "We've seen worse.", "next": "worse"},
                    ]},
                "honest": {"speaker": "Young Tomas",
                    "text": "Good. My dad says anyone who isn't scared before a fight is either "
                            "lying or stupid. The brave ones are scared and go anyway. "
                            "That's what I want to be.",
                    "choices": [{"text": "That's exactly right.", "next": None}]},
                "worse": {"speaker": "Young Tomas",
                    "text": "What's WORSE than a house-sized spider? "
                            "...Actually don't tell me. I'll have nightmares.",
                    "choices": [{"text": "Probably for the best.", "next": None}]},
            }},
        },
        # Goblin Warren cleared
        {
            "conditions": [{"flag": "boss_defeated.goblin_warren", "op": "==", "value": True}],
            "tree": {"id": "tomas_post_warren", "loop": True, "nodes": {
                "start": {"speaker": "Young Tomas",
                    "text": "I heard you cleared the Goblin Warren! The militia has been trying "
                            "to do that for a year. Grak was their chief — did he surrender? "
                            "Or did you have to fight?",
                    "on_enter": [{"action": "meet_npc", "npc": "young_tomas"}],
                    "choices": [
                        {"text": "We fought.", "next": "fought"},
                        {"text": "It was complicated.", "next": "complicated"},
                    ]},
                "fought": {"speaker": "Young Tomas",
                    "text": "I knew it. The town watch said goblins never surrender, "
                            "but Mister Harlan said they do if you're scary enough. "
                            "Were you scary enough?",
                    "choices": [{"text": "Apparently so.", "next": None}]},
                "complicated": {"speaker": "Young Tomas",
                    "text": "My mother says 'it's complicated' means someone made a hard choice "
                            "and doesn't want to explain it. That's okay. I understand.",
                    "choices": [{"text": "Smarter than you look, Tomas.", "next": None}]},
            }},
        },
        # Default
        {
            "conditions": [],
            "tree": {"id": "tomas_default", "loop": True, "nodes": {
                "start": {"speaker": "Young Tomas",
                    "text": "I'm not supposed to talk to adventurers. My mother says it gives me ideas. "
                            "She's right, but I don't see what's wrong with ideas.",
                    "on_enter": [{"action": "meet_npc", "npc": "young_tomas"}],
                    "choices": [
                        {"text": "What kind of ideas?", "next": "ideas"},
                        {"text": "Smart mother.", "next": "smart"},
                        {"text": "Good luck with that.", "next": None},
                    ]},
                "ideas": {"speaker": "Young Tomas",
                    "text": "Going somewhere. Doing something. The Goblin Warren east of town — "
                            "nobody's cleared it out. The militia tried twice. I think someone "
                            "better should try.",
                    "choices": [{"text": "We'll look into it.", "next": None}]},
                "smart": {"speaker": "Young Tomas",
                    "text": "She is. She survived the first Fading wave three years ago by "
                            "not doing what everyone else did. She just... stayed calm and stayed put. "
                            "I want to be brave like the adventurers though. Not calm.",
                    "choices": [{"text": "Both can save you.", "next": None}]},
            }},
        },
    ],

    # ─────────────────────────────────────────────────────────
    #  KORRATH — Pre-boss dialogue in Abandoned Mine (Act 1)
    # ─────────────────────────────────────────────────────────
    # ─────────────────────────────────────────────────────────
    #  SPIDER QUEEN — Spiders' Nest boss
    # ─────────────────────────────────────────────────────────
    "spider_queen": [
        {
            "conditions": [
                {"flag": "boss.spider_queen.defeated", "op": "not_exists"},
            ],
            "tree": {
                "id": "spider_queen_confrontation",
                "nodes": {
                    "start": {
                        "speaker": "The Spider Queen",
                        "text": "You smell of iron and urgency.\nYou are not the first to come here seeking the brightness at my center.\nThey all wanted it. None understood what it is.\nDo you?",
                        "choices": [
                            {"text": "It's a Hearthstone. Part of the ward network.", "next": "knows"},
                            {"text": "A fragment of the Fading ward. We need it.", "next": "need"},
                            {"text": "[Attack] We don't have time for conversation.", "next": "fight"},
                        ],
                    },
                    "knows": {
                        "speaker": "The Spider Queen",
                        "text": "So you do know.\nI have fed on the Fading for decades. The ward-anchor buried here is why my children were born wrong — too many legs, too many thoughts, too much space between the moments.\nI did not choose this. The anchor did.\nYou want it. I want it gone. We may have common ground.",
                        "choices": [
                            {"text": "Let us take it and we'll leave you in peace.", "next": "peace"},
                            {"text": "Why haven't you destroyed it?", "next": "why_not"},
                        ],
                    },
                    "need": {
                        "speaker": "The Spider Queen",
                        "text": "Everything here needs it.\nIt radiates something that the Fading cannot digest — a counter-frequency. My nest is the only place within a day's travel that the grey has not reached.\nYou taking it would doom my children. You know this?",
                        "choices": [
                            {"text": "The ward network will protect more than just your nest.", "next": "greater_good"},
                            {"text": "Then we fight.", "next": "fight"},
                        ],
                    },
                    "why_not": {
                        "speaker": "The Spider Queen",
                        "text": "I tried. Three times.\nEach attempt undid something in me.\nThe stone and I are not separate things anymore. Taking it without consent — it would leave a wound that does not close.\nIf you take it, take it knowing that.",
                        "choices": [
                            {"text": "We're sorry. But the network needs it.", "next": "greater_good"},
                            {"text": "Then yield it freely. It matters.", "next": "peace"},
                        ],
                    },
                    "greater_good": {
                        "speaker": "The Spider Queen",
                        "text": "The greater good.\nI have heard that phrase before from smaller creatures justifying larger cruelties.\nBut I have watched the grey take the forest for fifteen years.\nPerhaps your network holds better than my nest.\nThe ward-anchor is in the eastern wall of my chamber. Take it. And remember what it cost.",
                        "on_enter": [
                            {"action": "set_flag", "flag": "choice.spider_queen_spared", "value": True},
                            {"action": "set_flag", "flag": "boss.spider_queen.defeated", "value": True},
                        ],
                        "choices": [{"text": "We will remember.", "next": None}],
                    },
                    "peace": {
                        "speaker": "The Spider Queen",
                        "text": "Then there is no fight today.\nThe ward-anchor is embedded in the eastern wall of my chamber. You will know it — it hums wrong, like a note held too long.\nPry it free. Take it. Go.\nIf your ward network holds — if the grey recedes — send word to this place.\nMy children have never known a world without the Fading.\nI would like them to.",
                        "on_enter": [
                            {"action": "set_flag", "flag": "choice.spider_queen_spared", "value": True},
                            {"action": "set_flag", "flag": "boss.spider_queen.defeated", "value": True},
                        ],
                        "choices": [{"text": "We'll send word.", "next": None}],
                    },
                    "fight": {
                        "speaker": "The Spider Queen",
                        "text": "Then I defend what is mine.\nAs I always have.",
                        "choices": [{"text": "[Begin combat]", "next": None}],
                    },
                },
            },
        },
    ],

    # ─────────────────────────────────────────────────────────
    #  KORRATH — Abandoned Mine boss
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
        # Act 2 — after visiting Ruins of Ashenmoor
        {
            "conditions": [{"flag": "boss_defeated.ruins_ashenmoor", "op": "==", "value": True}],
            "tree": {"id": "theron_act2", "loop": True, "nodes": {
                "start": {"speaker": "Elder Theron",
                    "text": "The Ruins of Ashenmoor. Word came from the east — you cleared it. "
                            "That's the second Hearthstone fragment, if I'm counting right. "
                            "Woodhaven has been sending prayers to whatever's out there listening. "
                            "I think something is.",
                    "choices": [
                        {"text": "Three more to find.", "next": "three_more"},
                        {"text": "The Fading is retreating.", "next": "retreating"},
                    ]},
                "three_more": {"speaker": "Elder Theron",
                    "text": "Then go find them. Woodhaven will hold. We've held for two hundred "
                            "years against worse than this — or at least, against things we "
                            "understood less. Knowing what hunts you is half the battle.",
                    "choices": [{"text": "We'll be back.", "next": None}]},
                "retreating": {"speaker": "Elder Theron",
                    "text": "I feel it. The eastern grove — the sick trees near the old "
                            "Warden markers. They're greening again. Slowly. But they are. "
                            "Thank you for what you've done.",
                    "choices": [{"text": "There's more to do.", "next": None}]},
            }},
        },
        # Spider's Nest cleared — major local win
        {
            "conditions": [{"flag": "boss_defeated.spiders_nest", "op": "==", "value": True}],
            "tree": {"id": "theron_post_spiders", "loop": True, "nodes": {
                "start": {"speaker": "Elder Theron",
                    "text": "The web cave to the north is cleared. I sent a patrol up the "
                            "Thornwood path this morning for the first time in a season. "
                            "They came back whole and intact. That hasn't happened in a long time. "
                            "What's your next move?",
                    "choices": [
                        {"text": "The Abandoned Mine north of Ironhearth.", "next": "mine"},
                        {"text": "We follow where the Fading leads.", "next": "fading"},
                    ]},
                "mine": {"speaker": "Elder Theron",
                    "text": "The Abandoned Mine — north of Ironhearth, in the dwarven hills. "
                            "A Warden garrison held it. Word stopped "
                            "coming about a month ago. We'd assumed the worst. "
                            "If you can find out what happened — and if there's a "
                            "fragment there — then go.\n"
                            "Stop in Ironhearth first. The dwarves keep good stock "
                            "and better steel. You'll want both.",
                    "choices": [{"text": "We'll head to Ironhearth first.", "next": None}]},
                "fading": {"speaker": "Elder Theron",
                    "text": "Then you lead, and Woodhaven follows in prayers. "
                            "We are a small place. Our contribution is endurance — "
                            "surviving long enough for warriors like you to do your work.",
                    "choices": [{"text": "Survive and thrive.", "next": None}]},
            }},
        },
        # Default
        {
            "conditions": [],
            "tree": {"id": "theron_default", "loop": True, "nodes": {
                "start": {"speaker": "Elder Theron",
                    "text": "Welcome to Woodhaven. The grove provides shelter, but "
                            "these are troubled times. How may I help you?",
                    "on_enter": [{"action": "meet_npc", "npc": "elder_theron"}],
                    "choices": [
                        {"text": "Tell me about Woodhaven.", "next": "woodhaven"},
                        {"text": "What's the biggest threat here?", "next": "threat"},
                        {"text": "Goodbye.", "next": None},
                    ]},
                "woodhaven": {"speaker": "Elder Theron",
                    "text": "A lumber town, mostly — but one with a long memory. "
                            "The old Warden Order had a garrison here during the last Fading, "
                            "sixty years ago. Some of their records are still in the archive. "
                            "The Fading is back now. I think those records matter again.",
                    "choices": [{"text": "We're Warden recruits.", "next": None}]},
                "threat": {"speaker": "Elder Theron",
                    "text": "Two threats. The Spider's Nest to the north has been expanding — "
                            "the colony has grown far beyond its old bounds. "
                            "And the Fading from the east is killing the old grove trees. "
                            "Both are getting worse.",
                    "choices": [{"text": "We'll address both.", "next": None}]},
            }},
        },
    ],

    # ─────────────────────────────────────────────────────────
    #  SYLLA — Woodhaven Herbalist
    # ─────────────────────────────────────────────────────────
    "sylla": [
        # Spider's Nest cleared — her herbs are growing back
        {
            "conditions": [{"flag": "boss_defeated.spiders_nest", "op": "==", "value": True}],
            "tree": {"id": "sylla_post_spiders", "loop": True, "nodes": {
                "start": {"speaker": "Sylla",
                    "text": "You cleared the web caves to the north. I can already tell — "
                            "the brambleleaf is coming back along the eastern path. "
                            "The spiders had been eating the root systems for two seasons. "
                            "I'd forgotten what the forest smelled like before the webs.",
                    "choices": [
                        {"text": "The Queen was changed by the Fading.", "next": "queen"},
                        {"text": "What do you use brambleleaf for?", "next": "herb"},
                        {"text": "Good to hear.", "next": None},
                    ]},
                "queen": {"speaker": "Sylla",
                    "text": "I know. The spiders near the Nest weren't hunting normally — "
                            "they were defending something. The queen had been changed. "
                            "I've seen the same thing with the wolves further east. "
                            "The Fading doesn't just kill. It transforms.",
                    "choices": [{"text": "We're seeing that everywhere.", "next": None}]},
                "herb": {"speaker": "Sylla",
                    "text": "Fever reduction, wound poultice, tea for sleeplessness. "
                            "Half my stock depends on the eastern path being clear. "
                            "You've done more for my business than you know.",
                    "choices": [{"text": "A side benefit.", "next": None}]},
            }},
        },
        # Goblin Warren cleared — road safer for travel
        {
            "conditions": [{"flag": "boss_defeated.goblin_warren", "op": "==", "value": True}],
            "tree": {"id": "sylla_post_warren", "loop": True, "nodes": {
                "start": {"speaker": "Sylla",
                    "text": "Ah, adventurers — the ones who cleared the Warren? Good. "
                            "I've been unable to get my southern herb supply for weeks. "
                            "The goblin raids made the Thornwood trail too dangerous "
                            "for any merchant to risk it. Mind the dryin' stalks.",
                    "choices": [
                        {"text": "What herbs can't you get?", "next": "herbs"},
                        {"text": "The trail should be clear now.", "next": None},
                    ]},
                "herbs": {"speaker": "Sylla",
                    "text": "Stoneroot from the southern ridge — it's the only thing that "
                            "works on the Fading-cough the miners keep getting. "
                            "And silvermoss, for burns. I've been making do with substitutes "
                            "but they're not as effective.",
                    "choices": [{"text": "We'll keep the road clear.", "next": None}]},
            }},
        },
        # Default
        {
            "conditions": [],
            "tree": {"id": "sylla_default", "loop": True, "nodes": {
                "start": {"speaker": "Sylla",
                    "text": "Ah, adventurers! You look like you could use a poultice. Or three. "
                            "Come in, come in — mind the drying stalks.",
                    "on_enter": [{"action": "meet_npc", "npc": "sylla"}],
                    "choices": [
                        {"text": "What herbs do you work with?", "next": "herbs"},
                        {"text": "Have you noticed anything strange?", "next": "strange"},
                        {"text": "Just browsing.", "next": None},
                    ]},
                "herbs": {"speaker": "Sylla",
                    "text": "Whatever the Thornwood provides. Fewer things every season — "
                            "the spider infestation north has been eating root systems, "
                            "and the Fading has blackened half the eastern grove. "
                            "I make do.",
                    "choices": [{"text": "We'll look into the spiders.", "next": None}]},
                "strange": {"speaker": "Sylla",
                    "text": "The Fading. It's in the plants now — I found a batch of "
                            "healer's leaf last week that had gone completely grey. "
                            "No smell, no effect, just grey. The land's forgetting "
                            "what it's supposed to do.",
                    "choices": [{"text": "We're trying to stop it.", "next": None}]},
            }},
        },
    ],

    # ─────────────────────────────────────────────────────────
    #  FORGEMASTER DUNN — Ironhearth
    # ─────────────────────────────────────────────────────────
    "forgemaster_dunn": [
        # Mine cleared — supply chains restored
        {
            "conditions": [{"flag": "boss_defeated.abandoned_mine", "op": "==", "value": True}],
            "tree": {"id": "dunn_post_mine", "loop": True, "nodes": {
                "start": {"speaker": "Forgemaster Dunn",
                    "text": "You cleared the Abandoned Mine. I heard about Warden Korrath — "
                            "died at his post, holding the anchor. That's the old code. "
                            "We honour that here. And now the ore carts are moving again. "
                            "Don't mistake the two — both matter.",
                    "choices": [
                        {"text": "What was Korrath's anchor?", "next": "anchor"},
                        {"text": "How does the ore supply help?", "next": "ore"},
                    ]},
                "anchor": {"speaker": "Forgemaster Dunn",
                    "text": "Ward anchor — a Warden technique. You hold a physical point "
                            "against the Fading, prevent it from spreading through that "
                            "location. It requires someone to stay present. Korrath stayed. "
                            "The Mine's been clean since you went in.",
                    "choices": [{"text": "He bought us time.", "next": None}]},
                "ore": {"speaker": "Forgemaster Dunn",
                    "text": "Iron and coal for weapons, armour, tools. The eastern villages "
                            "have been starving for metalwork since the Mine went dark. "
                            "Three months of backlog. We're working through it now. "
                            "Whatever you need — you've earned a discount.",
                    "choices": [{"text": "Appreciated.", "next": None}]},
            }},
        },
        # Ironhearth visited — first meeting
        {
            "conditions": [{"flag": "town.ironhearth.visited", "op": "!=", "value": True}],
            "tree": {"id": "dunn_first_visit", "loop": True, "nodes": {
                "start": {"speaker": "Forgemaster Dunn",
                    "text": "Welcome to Ironhearth. First time in the forge district? "
                            "Best steel in Aldenmere. We've kept the fires burning "
                            "through two Fading waves and we'll burn through a third. "
                            "What do you need?",
                    "on_enter": [
                        {"action": "set_flag", "flag": "town.ironhearth.visited", "value": True},
                        {"action": "meet_npc", "npc": "forgemaster_dunn"},
                    ],
                    "choices": [
                        {"text": "Tell me about Ironhearth.", "next": "ironhearth"},
                        {"text": "How's the Mine situation?", "next": "mine"},
                        {"text": "Just looking.", "next": None},
                    ]},
                "ironhearth": {"speaker": "Forgemaster Dunn",
                    "text": "Dwarven founded, human expanded. The forge district is the oldest "
                            "quarter — those buildings pre-date the kingdom. The mine north "
                            "of here used to supply half the region's iron. Used to. "
                            "Warden garrison went silent a month ago.",
                    "choices": [{"text": "We'll investigate the mine.", "next": None}]},
                "mine": {"speaker": "Forgemaster Dunn",
                    "text": "The Abandoned Mine, they're calling it now. It wasn't abandoned — "
                            "the Wardens held it as an anchor point. Now we don't know "
                            "what's in there. And without that ore, we're melting down "
                            "old tools to keep production going.",
                    "choices": [{"text": "We'll look into it.", "next": None}]},
            }},
        },
        # Default
        {
            "conditions": [],
            "tree": {"id": "dunn_default", "loop": True, "nodes": {
                "start": {"speaker": "Forgemaster Dunn",
                    "text": "Welcome to the forge. I make the finest steel in Aldenmere. "
                            "What do you need?",
                    "choices": [
                        {"text": "Tell me about Ironhearth.", "next": "ironhearth"},
                        {"text": "How's business?", "next": "business"},
                        {"text": "Goodbye.", "next": None},
                    ]},
                "ironhearth": {"speaker": "Forgemaster Dunn",
                    "text": "Holding on. The Mine north of us went silent — no ore shipments "
                            "for a month. We're burning through reserves. And the Fading "
                            "is playing hell with the smelting temperatures. Strange days.",
                    "choices": [{"text": "We'll look into the mine.", "next": None}]},
                "business": {"speaker": "Forgemaster Dunn",
                    "text": "Weapons are selling, which is never a good sign. "
                            "When times are safe, I sell tools and cookware. "
                            "When times are bad, I sell blades. Business is very good.",
                    "choices": [{"text": "We'll need good blades.", "next": None}]},
            }},
        },
    ],

    # ─────────────────────────────────────────────────────────
    #  KIRA — Traveling Merchant, Ironhearth
    # ─────────────────────────────────────────────────────────
    "merchant_kira": [
        # After mine + act 1 done — trade routes open
        {
            "conditions": [{"flag": "boss_defeated.abandoned_mine", "op": "==", "value": True}],
            "tree": {"id": "kira_act1_done", "loop": True, "nodes": {
                "start": {"speaker": "Kira",
                    "text": "The trade route north is open again. I've already made two runs "
                            "to Ironhearth and back since the mine cleared. You have no idea "
                            "what that means for my margins. What can I do for you?",
                    "choices": [
                        {"text": "What rare things do you have now?", "next": "rare"},
                        {"text": "What news from the road?", "next": "road"},
                        {"text": "Just looking.", "next": None},
                    ]},
                "rare": {"speaker": "Kira",
                    "text": "Eastern goods from past the Ashenmoor — dust crystals, "
                            "preserved void-moss, a few items I'm not sure what to call. "
                            "Found them in a cache east of the ruins. Took the risk, "
                            "figured someone like you would want them.",
                    "choices": [{"text": "You guessed right.", "next": None}]},
                "road": {"speaker": "Kira",
                    "text": "Fewer monsters between here and Woodhaven since you cleared "
                            "the warren and the spiders. Three caravans came through "
                            "last week that couldn't have made it a month ago. "
                            "The common folk are noticing.",
                    "choices": [{"text": "Good.", "next": None}]},
            }},
        },
        # Spider's Nest cleared — mentions road improvement
        {
            "conditions": [{"flag": "boss_defeated.spiders_nest", "op": "==", "value": True}],
            "tree": {"id": "kira_post_spiders", "loop": True, "nodes": {
                "start": {"speaker": "Kira",
                    "text": "Well met, travelers! Kira's Curiosities — I deal in the rare "
                            "and the unusual. The road between Woodhaven and Ironhearth "
                            "is passable again now the spider cave is cleared. "
                            "I made it in one day instead of two. You saved me more "
                            "than you know.",
                    "choices": [
                        {"text": "Any news from the road?", "next": "road"},
                        {"text": "Just looking.", "next": None},
                    ]},
                "road": {"speaker": "Kira",
                    "text": "Refugees coming in from the east — Fading spreading in the "
                            "Ashenmoor region. Bring what they can carry. "
                            "Also: whoever's been burning goblin warrens is a hero. "
                            "Tell them a trader named Kira says so.",
                    "choices": [{"text": "Consider it relayed.", "next": None}]},
            }},
        },
        # Default
        {
            "conditions": [],
            "tree": {"id": "kira_default", "loop": True, "nodes": {
                "start": {"speaker": "Kira",
                    "text": "Well met, travelers! Kira's Curiosities, at your service. "
                            "I deal in the rare, the unusual, and the occasionally illegal. "
                            "Everything's legal here, before you ask.",
                    "on_enter": [{"action": "meet_npc", "npc": "merchant_kira"}],
                    "choices": [
                        {"text": "Where do you travel?", "next": "travel"},
                        {"text": "Any news from the road?", "next": "road"},
                        {"text": "Just looking.", "next": None},
                    ]},
                "travel": {"speaker": "Kira",
                    "text": "Everywhere the roads allow. The Warren east of Briarhollow "
                            "has been a problem — goblins raiding caravans. And the spider "
                            "cave north of Woodhaven means I have to take the long way "
                            "around. Bad for business.",
                    "choices": [{"text": "We'll deal with those.", "next": None}]},
                "road": {"speaker": "Kira",
                    "text": "More refugees from the east. The Fading is worse in the "
                            "Ashenmoor basin than anyone's admitting. I've been watching "
                            "it for six months. Something's accelerating it.",
                    "choices": [{"text": "We're looking into it.", "next": None}]},
            }},
        },
    ],

    # ─────────────────────────────────────────────────────────
    #  SCOUT FERYN — Greenwood, forest warden
    # ─────────────────────────────────────────────────────────
    "priestess_alia": [
        # Multiple hearthstones found
        {
            "conditions": [{"flag": "item.hearthstone.3", "op": "==", "value": True}],
            "tree": {"id": "alia_hearthstone3", "loop": True, "nodes": {
                "start": {"speaker": "Priestess Alia",
                    "text": "Three Hearthstones. Half of them. I feel it even here — "
                            "the temple's altar has been warmer to the touch these last weeks. "
                            "The flame responds to the wards being restored. "
                            "What you're doing is working.",
                    "choices": [
                        {"text": "Two more to find.", "next": "two_more"},
                        {"text": "Tell me about the flame.", "next": "flame"},
                    ]},
                "two_more": {"speaker": "Priestess Alia",
                    "text": "Then go. The flame will be here when you return. "
                            "Speak to it if you need strength — prayer is not weakness, "
                            "it's focusing what you already have.",
                    "choices": [{"text": "Thank you, Priestess.", "next": None}]},
                "flame": {"speaker": "Priestess Alia",
                    "text": "The flame predates any god's name. The Warden Order didn't "
                            "worship it — they tended it, the way you tend a hearth. "
                            "It doesn't grant miracles. It reminds you that something "
                            "has burned longer than your fear.",
                    "choices": [{"text": "That's enough.", "next": None}]},
            }},
        },
        # First hearthstone — she knows what it means
        {
            "conditions": [{"flag": "item.hearthstone.1", "op": "==", "value": True}],
            "tree": {"id": "alia_hearthstone1", "loop": True, "nodes": {
                "start": {"speaker": "Priestess Alia",
                    "text": "You've recovered a Hearthstone. I can tell — there's something "
                            "different in the quality of light around you. "
                            "The old texts speak of this. The stone remembers what the land "
                            "has forgotten. Carry it carefully.",
                    "choices": [
                        {"text": "What can you tell us about them?", "next": "about"},
                        {"text": "We'll find the rest.", "next": None},
                    ]},
                "about": {"speaker": "Priestess Alia",
                    "text": "Anchors against forgetting. The Fading is a kind of dissolution — "
                            "the world losing coherence. The Hearthstones hold pattern. "
                            "They were placed by the first Wardens in the ancient nodes, "
                            "the places where reality is thinnest. Restore them all "
                            "and the Fading can be sealed.",
                    "choices": [{"text": "We understand.", "next": None}]},
            }},
        },
        # After Spider's Nest
        {
            "conditions": [{"flag": "boss_defeated.spiders_nest", "op": "==", "value": True}],
            "tree": {"id": "alia_post_spiders", "loop": True, "nodes": {
                "start": {"speaker": "Priestess Alia",
                    "text": "Blessings upon your path, wanderers. The flame burns for all "
                            "who seek its light. Word reached me that you cleared the "
                            "spider cave to the north. Several of my parishioners couldn't "
                            "reach the temple from Woodhaven. They can come again now.",
                    "choices": [
                        {"text": "The Spider Queen was corrupted by the Fading.", "next": "queen"},
                        {"text": "We're glad the path is clear.", "next": None},
                    ]},
                "queen": {"speaker": "Priestess Alia",
                    "text": "The flame shows what is — including what should not be. "
                            "Corruption and transformation are not the same thing. "
                            "Something changed her nature against her nature's will. "
                            "That is a cruelty I would not wish on anything.",
                    "choices": [{"text": "We agree.", "next": None}]},
            }},
        },
        # Default
        {
            "conditions": [],
            "tree": {"id": "alia_default", "loop": True, "nodes": {
                "start": {"speaker": "Priestess Alia",
                    "text": "Blessings upon your path, wanderers. The flame of Aldenmere burns "
                            "for all who seek its light. How may I serve you today?",
                    "choices": [
                        {"text": "What do you know about the Fading?", "next": "fading"},
                        {"text": "Can you heal us?", "next": "healing"},
                        {"text": "Tell me about this temple.", "next": "temple"},
                        {"text": "Farewell, Priestess.", "next": None},
                    ]},
                "fading": {"speaker": "Priestess Alia",
                    "text": "The Fading... yes. I have felt it in my prayers for months — "
                            "a silence where the divine once answered. Something unravels the "
                            "very fabric of the world. Find others who understand it. "
                            "Trust the flame.",
                    "choices": [{"text": "We're trying.", "next": None}]},
                "healing": {"speaker": "Priestess Alia",
                    "text": "The temple offers restoration to those who need it. "
                            "Speak to the altar — the flame will do the rest.",
                    "choices": [{"text": "Thank you.", "next": None}]},
                "temple": {"speaker": "Priestess Alia",
                    "text": "This temple has stood in Woodhaven for three hundred years. "
                            "Built by the first settlers as a promise — that even in the "
                            "wildest frontier, they would tend the light.",
                    "choices": [{"text": "A good promise.", "next": None}]},
            }},
        },
    ],
    "ranger_cael": [
        # After Spider's Nest cleared
        {
            "conditions": [{"flag": "boss_defeated.spiders_nest", "op": "==", "value": True}],
            "tree": {
                "id": "ranger_cael_post_spiders",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Ranger Cael",
                        "text": "The web cave to the northwest — you cleared it? We've been "
                                "avoiding that whole stretch for weeks. The path to Ironhearth "
                                "is safer now. You've done the Thornwood a real service.",
                        "choices": [
                            {"text": "What's still out there?", "next": "threats"},
                            {"text": "We heard there's a mine north of Ironhearth.", "next": "mine"},
                            {"text": "Just doing what needed doing.", "next": None},
                        ],
                    },
                    "threats": {
                        "speaker": "Ranger Cael",
                        "text": "The Fading keeps pushing from the east. We hold the western "
                                "tree line but we're spread thin. The goblins were bad enough — "
                                "now we're seeing things that used to be deer. Dead things walking.",
                        "choices": [{"text": "We'll keep watch.", "next": None}],
                    },
                    "mine": {
                        "speaker": "Ranger Cael",
                        "text": "Abandoned Mine north of Ironhearth. Bad place. A Warden garrison "
                                "used to hold it — they're gone now. Something in there killed them. "
                                "If you go, take torches. Lots of them.",
                        "choices": [{"text": "Understood.", "next": None}],
                    },
                },
            },
        },
        # After Goblin Warren — pre spider's nest
        {
            "conditions": [{"flag": "boss_defeated.goblin_warren", "op": "==", "value": True}],
            "tree": {
                "id": "ranger_cael_post_warren",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Ranger Cael",
                        "text": "You cleared the Goblin Warren. The patrols have confirmed it — "
                                "the goblin raids have stopped cold. I've started sending scouts "
                                "back on the Thornwood trail. Good work.",
                        "choices": [
                            {"text": "There's still a cave to the northwest.", "next": "cave"},
                            {"text": "The goblins were being driven out by something.", "next": "driven"},
                            {"text": "Thanks.", "next": None},
                        ],
                    },
                    "cave": {
                        "speaker": "Ranger Cael",
                        "text": "The web cave, yes. We've marked it on patrol maps. "
                                "Giant spiders — bigger than wolves. We don't have the numbers "
                                "to clear it ourselves. If you're looking for your next challenge, "
                                "that's northwest of here on the Thornwood path.",
                        "choices": [{"text": "We'll deal with it.", "next": None}],
                    },
                    "driven": {
                        "speaker": "Ranger Cael",
                        "text": "They were. I've been saying it for months — something pushed "
                                "them out of the Warren. The Fading moves creatures like water "
                                "moves silt. When it spreads, everything runs ahead of it.",
                        "choices": [{"text": "We'll look into it.", "next": None}],
                    },
                },
            },
        },
        # Default — before any progress
        {
            "conditions": [],
            "tree": {
                "id": "ranger_cael_default",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Ranger Cael",
                        "text": "Welcome to the Scout Hall. We track patrols, log sightings, "
                                "coordinate with the Ranger's Guild. If you want honest work "
                                "in the Thornwood, you've come to the right place.",
                        "on_enter": [{"action": "meet_npc", "npc": "ranger_cael"}],
                        "choices": [
                            {"text": "What kind of work?", "next": "work"},
                            {"text": "What have you been seeing out there?", "next": "sightings"},
                            {"text": "We're tracking goblin activity.", "next": "goblins"},
                            {"text": "Just looking around.", "next": None},
                        ],
                    },
                    "work": {
                        "speaker": "Ranger Cael",
                        "text": "Patrol reports. Monster sightings logged and verified. "
                                "Dungeon clearances when we can get someone willing. "
                                "Right now the Goblin Warren east of Briarhollow is the priority — "
                                "raids have been getting bolder every week.",
                        "choices": [{"text": "We'll look into the Warren.", "next": None}],
                    },
                    "sightings": {
                        "speaker": "Ranger Cael",
                        "text": "Shadow-touched animals moving north from the Fading zones. "
                                "Goblins pushed out of their usual range and raiding settlements. "
                                "And something deeper in the Thornwood that we haven't identified — "
                                "webs the size of fishing nets covering the northwest trail.",
                        "choices": [{"text": "Something made those webs.", "next": "cave"}],
                    },
                    "cave": {
                        "speaker": "Ranger Cael",
                        "text": "A cave to the northwest. The children call it the web cave. "
                                "Nobody goes near it anymore. We've lost two scouts in that direction "
                                "in the last month. Big things moved on that trail.",
                        "choices": [{"text": "Noted.", "next": None}],
                    },
                    "goblins": {
                        "speaker": "Ranger Cael",
                        "text": "The Warren east of Briarhollow is the source. Something drove them "
                                "out — they're raiding because they're afraid, not because they're "
                                "bold. Clear the Warren and the raids stop. That's my read.",
                        "choices": [{"text": "We'll handle it.", "next": None}],
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
                "loop": True,
                "loop": True,
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

    # ─────────────────────────────────────────────────────────
    #  OLD MOSS — Greenwood's ancient hermit druid
    #  Knows the forest and the Fading better than anyone.
    #  Doesn't give quest text — gives lore, observation, weight.
    # ─────────────────────────────────────────────────────────


    # ─────────────────────────────────────────────────────────
    #  GOVERNOR ALDRIC — Thornhaven capital, Iron tier
    # ─────────────────────────────────────────────────────────

    # ─────────────────────────────────────────────────────────
    #  GUILD COMMANDER VAREK — Thornhaven adventurers' guild
    # ─────────────────────────────────────────────────────────

    # ─────────────────────────────────────────────────────────
    #  COURT MAGE SIRA — Thornhaven, Maren's Act II reveal
    # ─────────────────────────────────────────────────────────

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
                            {"text": "Karreth-sol-Amendar. Guardian whose fire remembers warmth.",
                             "next": "true_name_path",
                             "condition": {"flag": "lore.karreth_true_name", "op": "==", "value": True}},
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
                    "true_name_path": {
                        "speaker": "Karreth",
                        "text": "The grey-green eye goes dark.\n"
                                "The silence that follows is so total the volcanic vents seem to hold their breath.\n"
                                "Then, slowly, both eyes open — and for the first time, both are the same colour: "
                                "deep amber, old and clear.\n"
                                "The voice that comes out is different. Lower. Older. Without the corruption's echo.\n"
                                "You found it. The name.\n"
                                "I... had forgotten it. What I was called when I chose this.\n"
                                "Before the Fading found me.",
                        "choices": [
                            {"text": "You can rest now. We'll carry the stone.", "next": "peaceful_release"},
                            {"text": "Do you remember who asked you to guard it?",  "next": "memory"},
                        ],
                    },
                    "memory": {
                        "speaker": "Karreth",
                        "text": "A woman. Old. She smelled of cold stone and burned sage.\n"
                                "She said: the world will break. When it does, keep the light warm until "
                                "someone comes to carry it again.\n"
                                "I asked how I would know the right someone.\n"
                                "She said: they will know your name.\n"
                                "The amber eyes hold yours for a long moment.\n"
                                "She was right.",
                        "next": "peaceful_release",
                    },
                    "peaceful_release": {
                        "speaker": "Karreth",
                        "text": "Take it. It was always meant to move on.\n"
                                "I was only ever meant to be the bridge between its last keeper and its next.\n"
                                "The vast body lowers, slowly, until the Hearthstone is within reach. "
                                "Karreth does not move as you take it. The amber light in both eyes "
                                "dims — not like death, but like a lantern being set down after a long walk.\n"
                                "You have the stone. And something else — a single scale, shed willingly, "
                                "still warm.",
                        "on_enter": [
                            {"action": "set_flag", "flag": "choice.karreth_spared",  "value": True},
                            {"action": "set_flag", "flag": "boss.karreth.defeated",  "value": True},
                            {"action": "set_flag", "flag": "lore.karreth_freed",     "value": True},
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
    "briarhollow": ["maren", "captain_rowan", "bess", "old_petra", "young_tomas", "elder_thom", "captain_aldric", 'warden_liaison'],
    "woodhaven":   ["elder_theron", "sylla", "warden_liaison"],
    "ironhearth":  ["forgemaster_dunn", "merchant_kira", "warden_liaison"],
    "greenwood":   ["scout_feryn", "old_moss", "warden_liaison"],
    "saltmere":    ["guildmaster_sable", "tide_priest_oran", "dockhand_riv", "warden_liaison"],
    "sanctum":     ["high_priest_aldara", "warden_liaison"],
    "crystalspire": ["archmage_solen", "teleport_master", "warden_liaison", "crystalspire_priest"],
    "thornhaven":  ["governor_aldric", "guild_commander_varek", "court_mage_sira",
                   "city_guard_thornhaven", "refugee_elder", "innkeeper_thornhaven", "warden_liaison"],
    "emberveil":   ["renn_emberveil", "warden_liaison"],
    "the_anchorage": ["vaethari_anchorage", "warden_liaison"],
    "the_holdfast":  ["dael_holdfast", "sarev_holdfast", "warden_liaison"],
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
        # Hybrid class hints
        "There's a fighter in the guild who prays before every battle. They say she can channel holy fire now. Called a Paladin, or something close.",
        "I knew a thief who studied shadow-walking long enough to become something else. A Phantom, the guild called her. Moves through darkness like it's water.",
        "The old Warden traditions talked about warriors who crossed paths — soldiers who learned the arcane, or mages who learned the blade. The guild calls it a transition.",
        "My uncle was a ranger who spent years with a shaman in the hills. Came back changed. Said he could feel the land breathing. Never fought the same way again.",
        "The Crystalspire Mages say there's a discipline beyond pure magic — something that fuses it with devotion. A Mystic, they call it. Rare. Harder than either alone.",
        # New settlement hints
        "There's a mining post near the Dragon's Tooth — Emberveil, they call it. Volcanic rock, sulphur smell, and a blacksmith who knows more about the Warden routes than he lets on.",
        "A fishing village on the mainland coast near the Windswept Isle. The Anchorage. Half researchers, half fisherfolk. An old elf there has lived long enough to remember the Wardens.",
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
        # New settlement hints
        "There's a rebel camp in the Ashlands — the Holdfast. They've been holding the Fading back by sheer stubbornness. The last Warden initiate runs supplies there.",
        "The Holdfast is northeast of Thornhaven, deep in the Ashlands. Dangerous road but they'll take any help they can get. The commander there knows the Spire's layout.",
        "A smith in Emberveil — Renn — says there's a back way into Dragon's Tooth. Lava tube on the east face. Skips the first floor entirely.",
        "The elf at the Anchorage is three hundred years old. Knew the Keeper of Windswept Isle personally. If anyone knows how to reach her, it's them.",
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
            {
                "floor": 3,
                "title": "Grak's War-Marks",
                "text": "Carved in a clumsy but deliberate hand beside the chief's chamber door: "
                        "a list of names, each with a small tally beside it. "
                        "Not enemies killed — the marks beside each are too small, too sad. "
                        "These are goblins who didn't make it here. "
                        "The ones who died in the flight from the Fading. "
                        "Grak has been keeping count.",
                "lore_id": "grak_memorial",
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
                "floor": 1,
                "title": "Exterminator's Contract",
                "text": "A crumpled work order stamped with the Greenwood Guild seal: "
                        "'Authorization for pest removal — Spider's Nest cavern system, "
                        "eastern approach. Payment: 40 silver upon proof of queen's death. "
                        "Note: previous two teams have not returned. "
                        "Contractor assumes all risk.' "
                        "Below, scrawled in panicked handwriting: "
                        "'They knew we were coming. They were waiting at the entrance. "
                        "The silk — it's not natural. It pulled Aldous off the path. "
                        "I'm going back. I'm not going back.'",
                "lore_id": None,
            },
            {
                "floor": 2,
                "title": "Researcher's Notes",
                "text": "The specimens exhibit clear mutagenic effects consistent with "
                        "prolonged exposure to ward-decay energy. The Fading doesn't just "
                        "destroy — it transforms. These creatures are adapting to exist "
                        "between realities. — E.V.",
                "lore_id": "spider_queen_observed",
            },
            {
                "floor": 3,
                "title": "E.V.'s Final Entry",
                "text": "The same hand as the Researcher's Notes, now shaking: "
                        "'She is aware of me. Has been, I think, since I arrived. "
                        "She watches through the web — I can feel it. "
                        "She is not mindless. She is not simply territorial. "
                        "She is protecting something and she knows exactly what it is. "
                        "The stone at the nest's center is feeding her awareness. "
                        "She may be more than a spider now. "
                        "She may be more than anything I have a word for. "
                        "I am going to try to speak with her. "
                        "E.V.' — The initials match Valdris's early research logs.",
                "lore_id": "spider_queen_sapient",
                "on_find": [{"action": "set_flag", "flag": "lore.spider_queen_sapient", "value": True}],
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
            4: "The air here is wrong — too clean, too still. The dust should "
               "have settled decades ago. Something is keeping this floor in a kind of "
               "stasis. Korrath's work extends further than the records said.",
            5: "The deepest chamber. The original ward-anchor is here — "
               "cracked, dark, but not destroyed. Whatever Valdris's people extracted, "
               "they couldn't take this. Korrath stands over it. "
               "He has stood over it for twenty years.",
        },
        "journal_entries": [
            {
                "floor": 1,
                "title": "Foreman's Last Report",
                "text": "Scrawled on the back of a work roster: "
                        "'Workers refusing to go past level 2. Say the stone talks at night. "
                        "Pay them double and they still won't go. "
                        "Valdris's men arrived yesterday — said they have authorization from "
                        "the order to inspect the anchor. "
                        "Something about their eyes isn't right. "
                        "Sending the crew home. Posting this at the entrance. "
                        "If anyone from the Guild reads this: don't open what they sealed.'",
                "lore_id": None,
            },
            {
                "floor": 2,
                "title": "Dwarven Inscription",
                "text": "Translated from Old Dwarvish: 'Here lies the charge of Warden "
                        "Korrath, sealed until the world has need again. "
                        "Let the stone judge the worthy.'",
                "lore_id": None,
            },
            {
                "floor": 3,
                "title": "Valdris's Field Notes",
                "text": "Dense, precise handwriting on oilskin paper: "
                        "'The Hearthstone fragment here is the most intact I've found. "
                        "Extraction would require bypassing the ward-guardian — Korrath, "
                        "if the records are right. He is listed as 'sealed,' not 'dead.' "
                        "There is a difference. "
                        "My team will attempt extraction on the third night. "
                        "If the guardian wakes, we fall back to contingency. "
                        "The fragment must not be left here. He will corrupt it eventually.'",
                "lore_id": "valdris_mine_notes",
                "on_find": [{"action": "set_flag", "flag": "lore.valdris_mine_notes", "value": True}],
            },
            {
                "floor": 4,
                "title": "Korrath's Ward-Log",
                "text": "Etched directly into the stone wall — years of marks: "
                        "'Year 1: Valdris's men came. Drove them back. Stone is safe. "
                        "Year 3: They came again with shadow-weapons. Lost my left arm at the elbow. "
                        "Stone is safe. "
                        "Year 7: No one came. Beginning to wonder if the order still exists. "
                        "Year 12: A Warden passed through. She left quickly. Didn't explain. "
                        "Year 19: Something changes in the stone. The network is strained. "
                        "I am still here. "
                        "Stone is safe.'",
                "lore_id": "korrath_ward_log",
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
                "floor": 1,
                "title": "Imperial Survey Report",
                "text": "Stamped with a faded Imperial seal: "
                        "'Site assessment, Ashenmoor — declared uninhabitable following "
                        "the ward-collapse event of Year 14 I.R. "
                        "Structural instability throughout. Residual magical energy readings "
                        "exceed safe thresholds. Population: none surviving. "
                        "Cause of collapse: under investigation. "
                        "Recommendation: seal all entrances. "
                        "Note appended in different ink: "
                        "Warden Valdris was seen in the area three days before the collapse. "
                        "This information is not to be included in the official record.'",
                "lore_id": "ashenmoor_survey",
                "on_find": [{"action": "set_flag", "flag": "lore.ashenmoor_survey", "value": True}],
            },
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
            {
                "floor": 4,
                "title": "Ashvar's Private Letter",
                "text": "Written to no recipient, never sent: "
                        "'I signed the order. I accused him publicly. "
                        "I told the Council what happened. "
                        "What I didn't tell them: Valdris came to me the night before the collapse. "
                        "He told me the anchor was failing — that it had been failing for a year "
                        "and the order refused to act. He was trying to fix it. "
                        "He failed. "
                        "Two hundred people died. "
                        "He failed. "
                        "But I'm not sure I was right to call it murder. "
                        "I am not sure what I would call it. "
                        "I have been here for twelve years and I am still not sure.'",
                "lore_id": "ashvar_doubt",
                "on_find": [{"action": "set_flag", "flag": "lore.ashvar_doubt", "value": True}],
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
            {
                "floor": 2,
                "title": "Warden Field Notes — Expedition 7",
                "text": "Scrawled in the margin of an official expedition report, in a "
                        "different hand from the main text: "
                        "'The old texts call it by a different name — not Karreth, which "
                        "is just what the sailors called the island. "
                        "The binding inscription in the vault below gives its true name: "
                        "Karreth-sol-Amendar. "
                        "In Old Draconic: the guardian whose fire remembers warmth. "
                        "The ward scholars believed that speaking a bound guardian's true name "
                        "in the old tongue could reach the creature beneath the corruption — "
                        "not override its oath, but remind it who it was before. "
                        "This was never tested. The order collapsed before we could return. "
                        "If someone finds this: the name is the key. Speak it clearly. "
                        "Do not flinch.'",
                "lore_id": "karreth_true_name",
                "on_find": [{"action": "set_flag", "flag": "lore.karreth_true_name", "value": True}],
            },
            {
                "floor": 3,
                "title": "Scratched on the Hoard Room Doorframe",
                "text": "Cut into the volcanic rock at shoulder height — "
                        "someone standing in the entrance, watching the dragon sleep: "
                        "'I could see the stone from here. Glowing. Beautiful. "
                        "Karreth moved when I stepped inside and I ran. "
                        "Ran all the way back to the shore. "
                        "But I stood there for a long time first. "
                        "Looking. "
                        "I keep thinking about how it curled around the light. "
                        "Like it was keeping it warm. "
                        "Like it remembered what warm meant.'",
                "lore_id": None,
            },
        ],
        "boss_dialogue": "karreth",
    },

    # ── ACT 3 DUNGEONS ─────────────────────────────────────────────

    "pale_coast": {
        "floor_messages": {
            1: "The catacombs beneath the Pale Coast are half-flooded. "
               "Salt water drips from ceilings carved by hands long dead. "
               "Bodies from a dozen ages line the walls — all the same expression. "
               "All looking inward.",
            2: "Deeper now, and drier. The flooding stops at what appears to be "
               "an old ward-line — still active, still holding the sea back. "
               "Someone maintained this. Someone who knew what they were doing.",
            3: "The sound of the sea vanishes here. The silence is total. "
               "On the wall, carved in precise Warden script: "
               "'I chose this. I am not a victim. I am the last lock. "
               "Turn back if you are not the ones who carry the light.'",
            4: "The Sentinel's chamber. She stands exactly as she has for decades — "
               "armored, unmoving, facing the Hearthstone at the room's center. "
               "As you enter, she turns. She has been waiting. She has always been waiting.",
        },
        "journal_entries": [
            {
                "floor": 1,
                "title": "Hermit's Note",
                "text": "Found pinned to a driftwood marker at the cave entrance: "
                        "'The Pale Sentinel turns away all who come alone or wounded. "
                        "She will only yield to those who have already done the work. "
                        "Three stones and a clear conscience, the old texts say. "
                        "I have neither. I am turning back.'",
                "lore_id": None,
            },
            {
                "floor": 2,
                "title": "Warden Archive Fragment",
                "text": "A preserved scroll in a warded alcove: "
                        "'Warden Sirenne of the Pale Coast ward-station elected voluntary isolation "
                        "rather than risk corruption as the Fading advanced. "
                        "She sealed herself into the catacombs with the Hearthstone. "
                        "Her last communication stated: I will hold it until the order sends "
                        "someone worthy to continue the work. "
                        "No such person has come.'",
                "lore_id": "pale_sentinel_sirenne",
            },
            {
                "floor": 3,
                "title": "Sirenne's Journal — Final Entry",
                "text": "The ink is old but clear: "
                        "'I have been here a very long time. The Fading has not reached me "
                        "— the stone keeps it at bay. Or perhaps I keep it at bay. "
                        "We have reached a kind of accord, the stone and I. "
                        "I no longer know which of us is guardian and which is the guarded. "
                        "I do not think it matters. What matters is that the next one carries it better than I have.'",
                "lore_id": None,
            },
        ],
        "boss_dialogue": "pale_sentinel",
    },

    "windswept_isle": {
        "floor_messages": {
            1: "The ruins are old — older than the Empire, possibly older than Aldenmere itself. "
               "The wind here is constant, as if the island is breathing. "
               "Carved into the archway above the entrance: one word, in a language "
               "your party cannot read. The translation in Maren's notes reads: 'Remembrance.'",
            2: "The storm grows inside the ruins, not outside. The sky above is calm. "
               "Arcane instruments — long dead — line the walls of what was once a study. "
               "Scattered among them, notes in a hand identical to nothing in your knowledge. "
               "The ward-station's original operator. A keeper with no name.",
            3: "The innermost chamber. The fifth Hearthstone rests on a stone pedestal, "
               "undisturbed for centuries. Around it, an elemental storm that has spun "
               "for just as long, bound by orders it never questioned. "
               "It has no malice. It has no mercy. It has a purpose.",
        },
        "journal_entries": [
            {
                "floor": 1,
                "title": "Explorer's Field Notes",
                "text": "Margins annotated in three different hands: "
                        "'The ward-station was built before the Warden order was formalized. "
                        "Whoever placed the keeper here did so with no intention of ever retrieving it. "
                        "The Hearthstone and the guardian were meant to outlast everything else. "
                        "They appear to be succeeding.'",
                "lore_id": None,
            },
            {
                "floor": 2,
                "title": "Keeper's Log (Last Entry)",
                "text": "The paper is barely paper anymore, more mineral than organic: "
                        "'The order has not come. I do not believe the order will come. "
                        "I do not believe the order still exists. "
                        "My purpose does not require the order to exist. "
                        "I am the lock. The stone is the key. "
                        "The key does not leave with anyone. "
                        "This entry requires no response.'",
                "lore_id": "windswept_keeper",
            },
            {
                "floor": 3,
                "title": "Warden Survey — Site Designation W-7",
                "text": "A formal assessment, ink still sharp after centuries: "
                        "'The elemental bound here is not a construct — it is a Will, "
                        "recruited rather than manufactured. It had a name once. "
                        "It requested, before binding, that the name not be recorded. "
                        "It said: the purpose is enough. I should not be remembered for what I guard. "
                        "I should be remembered for guarding it. "
                        "We have honored this. "
                        "The surveyor notes, in a smaller hand below the seal: "
                        "I think about this one sometimes.'",
                "lore_id": None,
            },
        ],
        "boss_dialogue": "isle_keeper",
    },

    "shadow_throne": {
        "floor_messages": {
            1: "The Shadow Throne. The name is metaphor made architecture — "
               "shadow given weight, given walls, given purpose. "
               "The Fading doesn't just exist here. It was invited. "
               "Valdris built this place as a vessel.",
            2: "Research chambers. The work here is meticulous, obsessive. "
               "Notes on ward-failure rates, on Fading progression, on Warden bloodlines. "
               "He was not trying to destroy the world. "
               "He was trying to understand why it was already dying.",
            3: "The first Warden echoes begin appearing here — "
               "former members of the order who followed Valdris, then were consumed. "
               "They wear the order's colors. They do not recognize you.",
            4: "Halfway up. The shadow here is dense enough to see — "
               "not darkness, but something with texture, with will. "
               "It watches. It has been watching since you entered.",
            5: "A gallery of portraits, all defaced — the original Warden order. "
               "One face has been untouched. Maren's mother. "
               "The resemblance to Maren is unmistakable.",
            6: "The upper chambers. More personal now. A bedroom. Books read to pieces. "
               "A child's drawing, framed. The inscription: 'For Father, from M.' "
               "Maren was here. Often. For years.",
            7: "The anteroom to the throne chamber. Maren stands at the far end. "
               "She turns when she hears you. Her expression is not surprise. "
               "She has been waiting for this conversation for a very long time.",
            8: "The throne chamber. Valdris waits — or what remains of him. "
               "The shadow that wears his face turns slowly. "
               "Somewhere inside it, the man who broke the world is still present. "
               "Maren stands beside you. The choice is here.",
        },
        "journal_entries": [
            {
                "floor": 1,
                "title": "Valdris — Personal Notes, Year 1",
                "text": "The Fading is not entropy. Entropy is passive. This has direction. "
                        "Something is extracting the ward-energy deliberately. "
                        "My colleagues believe I have become obsessive. "
                        "They are correct. Obsession is the appropriate response.",
                "lore_id": "valdris_notes_1",
            },
            {
                "floor": 2,
                "title": "Valdris — Personal Notes, Year 7",
                "text": "I have found the mechanism. The ward-network requires continuous Warden sacrifice "
                        "to maintain — slow, invisible, but real. The order knew this and said nothing. "
                        "Every Warden who ever served has been slowly diminished. "
                        "Maren's mother died of it. She thought she was ill. "
                        "I am going to find another way.",
                "lore_id": "valdris_notes_2",
            },
            {
                "floor": 3,
                "title": "Valdris — Personal Notes, Year 12",
                "text": "Ashenmoor was an accident. "
                        "I did not believe the anchor would fail that way. "
                        "I did not believe two hundred people lived in the collapse radius. "
                        "I have spent eleven years telling myself that the alternative — "
                        "the slow bleeding of every Warden for centuries — was worse. "
                        "I am no longer certain I believe that.",
                "lore_id": "valdris_notes_3",
            },
            {
                "floor": 4,
                "title": "Valdris — Personal Notes, Year 19",
                "text": "The Fading has begun to respond to me. "
                        "I do not mean that it is slowing — I mean that it moves differently "
                        "when I am present. Toward me, sometimes. As if recognizing something. "
                        "My colleague Sira believes I have been compromised. "
                        "She is probably correct. "
                        "I find I am no longer frightened by this. "
                        "I find that I am no longer certain what frightened me means. "
                        "I find that this itself does not alarm me. "
                        "I find that this itself does not alarm me. "
                        "I have written that sentence twice. I am not sure when.",
                "lore_id": None,
            },
            {
                "floor": 5,
                "title": "Maren — Unsent Letter",
                "text": "Written in Maren's hand, addressed to no one: "
                        "'Father. I have the Hearthstones. I have the ritual. "
                        "I know what it requires. "
                        "I keep thinking about what you told me before Ashenmoor: "
                        "that there is no solution that doesn't cost something real. "
                        "I finally believe you. "
                        "I'm sorry it took this long. "
                        "I'm sorry about what I'm going to do. "
                        "I think you would understand. "
                        "I think that's the worst part.'",
                "lore_id": "maren_unsent",
            },
            {
                "floor": 7,
                "title": "The Order's Last Record",
                "text": "An official document, Imperial seal intact: "
                        "'Warden Valdris is hereby declared Oathbreaker and enemy of the realm. "
                        "His research is to be destroyed. His name is stricken. "
                        "His daughter is to have no contact with the order. "
                        "By order of the Grand Council of Wardens — "
                        "The last document entered before the order's dissolution, one year later.'",
                "lore_id": "valdris_oathbreaker",
            },
        ],
        "boss_dialogue": "valdris_pre_fight",
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
    """Get a random rumor for the current act, weighted toward story-relevant ones."""
    import random
    from core.story_flags import get, get_flag, check_conditions

    if act is None:
        act = get("act", 1)
    base_pool = list(TAVERN_RUMORS.get(act, TAVERN_RUMORS[1]))

    # Story-conditional bonus rumors — appear 3× more likely when conditions are met.
    # Each entry: (conditions_list, rumor_text)
    STORY_RUMORS = [
        # Act 1 reactivity
        ([{"flag": "boss_defeated.goblin_warren", "op": "==", "value": True}],
         "They say those adventurers cleared the goblin warren. Captain Aldric looked almost relieved."),
        ([{"flag": "boss_defeated.goblin_warren", "op": "==", "value": True}],
         "The road east is safer now. Still won't go at night, but safer."),
        ([{"flag": "boss_defeated.spiders_nest", "op": "==", "value": True}],
         "Old Petra's crowing about the spider cave. Says she told everyone and nobody listened. She's right."),
        ([{"flag": "boss_defeated.spiders_nest", "op": "==", "value": True}],
         "The Thornwood path is clear. Whatever was in that cave is gone. Petra says it was the Fading."),
        ([{"flag": "item.hearthstone.1", "op": "==", "value": True}],
         "Word is they found one of those old ward-stones in the mine. Living magic, they say. Warm to the touch."),
        ([{"flag": "boss_defeated.abandoned_mine", "op": "==", "value": True}],
         "The abandoned mine's clear. Whatever Valdris put in there is gone. The tanner's already talking about reopening."),
        # Act 2 reactivity
        ([{"flag": "boss_defeated.ruins_ashenmoor", "op": "==", "value": True}],
         "Ashenmoor's been quiet. No more lights, no more sounds. Whatever woke up in there has been put back to sleep."),
        ([{"flag": "item.hearthstone.2", "op": "==", "value": True}],
         "Two ward-stones found. The mages in Crystalspire are apparently measuring something in the ley lines. Numbers going up."),
        ([{"flag": "item.hearthstone.3", "op": "==", "value": True}],
         "Three stones. Half the set. Someone in the Guild is keeping count on a chalkboard. People stop and look."),
        ([{"flag": "boss_defeated.dragons_tooth", "op": "==", "value": True}],
         "They made peace with the dragon. Or killed it. Accounts differ. Either way — the volcano's quiet."),
        ([{"flag": "maren.left", "op": "==", "value": True}],
         "Maren left town. Didn't say goodbye. Bess says she left a note but won't show it to anyone."),
        ([{"flag": "maren.left", "op": "==", "value": True}],
         "I heard the scholar went to the Spire herself. Alone. Either very brave or very desperate."),
        # Act 3 reactivity
        ([{"flag": "item.hearthstone.4", "op": "==", "value": True}],
         "Four stones. The Pale Sentinel yielded hers. Sixty years guarding a stone for people who finally came."),
        ([{"flag": "item.hearthstone.5", "op": "==", "value": True}],
         "All five. I didn't think I'd live to hear that. Whatever happens next, at least someone tried."),
        ([{"flag": "boss_defeated.shadow_valdris", "op": "==", "value": True}],
         "The Fading's stopped. Just... stopped. I woke up this morning and the sky looked right again."),
        ([{"flag": "boss_defeated.shadow_valdris", "op": "==", "value": True}],
         "They came back from the Spire. All of them. That's not supposed to happen."),

        # ── DIRECTIONAL NEXT-STEP RUMORS ────────────────────────────
        # These fire when a main quest is active but the objective is
        # elsewhere — giving the player a concrete town/NPC pointer
        # even if they don't talk to a Warden Liaison.
        ([{"flag": "quest.main_meet_maren.state", "op": ">=", "value": 1},
          {"flag": "quest.main_meet_maren.state", "op": "!=", "value": -2}],
         "That scholar woman — Maren — keeps asking about the old Wardens. She's at the Wanderer's Rest in Briarhollow if you want to hear her out."),
        ([{"flag": "quest.main_goblin_warren.state", "op": ">=", "value": 1},
          {"flag": "quest.main_goblin_warren.state", "op": "!=", "value": -2},
          {"flag": "boss_defeated.goblin_warren",   "op": "not_exists"}],
         "Maren's been sending folks east of Briarhollow, into the Goblin Warren. Nobody's come back with good news yet."),
        ([{"flag": "quest.main_hearthstone_1.state", "op": ">=", "value": 1},
          {"flag": "quest.main_hearthstone_1.state", "op": "!=", "value": -2},
          {"flag": "boss_defeated.abandoned_mine",   "op": "not_exists"}],
         "Scholar says the first ward-stone's in the Abandoned Mine — north of Ironhearth. You'll want the mine key the Spider Queen carries."),
        ([{"flag": "quest.main_spiders_nest.state", "op": ">=", "value": 1},
          {"flag": "quest.main_spiders_nest.state", "op": "!=", "value": -2},
          {"flag": "boss_defeated.spiders_nest",    "op": "not_exists"}],
         "Elder Theron in Woodhaven's offering coin for anyone fool enough to clear the Spider's Nest in the Thornwood. Good luck."),
        ([{"flag": "quest.main_ashenmoor.state", "op": ">=", "value": 1},
          {"flag": "quest.main_ashenmoor.state", "op": "!=", "value": -2},
          {"flag": "boss_defeated.ruins_ashenmoor", "op": "not_exists"}],
         "The Ruins of Ashenmoor are east past Ironhearth, where the trees die. Maren in Briarhollow knows more — she's the one sending people there."),
        ([{"flag": "quest.main_hearthstone_2.state", "op": ">=", "value": 1},
          {"flag": "quest.main_hearthstone_2.state", "op": "!=", "value": -2},
          {"flag": "boss_defeated.sunken_crypt",     "op": "not_exists"}],
         "Tide Priest Oran in Saltmere keeps muttering about the Sunken Crypt and old Order wards. If you're headed that way, he's who to ask."),
        ([{"flag": "quest.main_hearthstone_3.state", "op": ">=", "value": 1},
          {"flag": "quest.main_hearthstone_3.state", "op": "!=", "value": -2},
          {"flag": "boss_defeated.dragons_tooth",    "op": "not_exists"}],
         "Dockhand Riv at Saltmere Docks runs the Tiderunner route. He's the only one fool enough to sail to Dragon's Tooth."),
        ([{"flag": "quest.main_thornhaven.state", "op": ">=", "value": 1},
          {"flag": "quest.main_thornhaven.state", "op": "!=", "value": -2}],
         "Archmage Solen's been sending folks east to Thornhaven — wants them in front of Governor Aldric. Road goes through Crystalspire."),
        ([{"flag": "quest.main_maren_truth.state", "op": ">=", "value": 1},
          {"flag": "quest.main_maren_truth.state", "op": "!=", "value": -2}],
         "The Court Mage in Thornhaven's been digging into old records. Scholar Maren's name keeps coming up. She's still at the Wanderer's Rest in Briarhollow last I heard."),
        ([{"flag": "quest.main_act2_pursuit.state", "op": ">=", "value": 1},
          {"flag": "quest.main_act2_pursuit.state", "op": "!=", "value": -2}],
         "Scholar Maren left in a hurry — headed north toward the Spire. Guild Commander Varek in Thornhaven's coordinating whoever wants to follow."),
        ([{"flag": "quest.main_act3_spire.state", "op": ">=", "value": 1},
          {"flag": "quest.main_act3_spire.state", "op": "!=", "value": -2},
          {"flag": "boss_defeated.valdris_spire",  "op": "not_exists"}],
         "Guild Commander Varek's taking names at the Thornhaven hall. Says the Spire won't clear itself."),
        ([{"flag": "quest.main_pale_coast.state", "op": ">=", "value": 1},
          {"flag": "quest.main_pale_coast.state", "op": "!=", "value": -2},
          {"flag": "boss_defeated.pale_coast",    "op": "not_exists"}],
         "They say there's a fourth ward-stone in the Pale Coast Catacombs. Varek's people are prepping at the Thornhaven guild hall."),
        ([{"flag": "quest.main_windswept_isle.state", "op": ">=", "value": 1},
          {"flag": "quest.main_windswept_isle.state", "op": "!=", "value": -2},
          {"flag": "boss_defeated.windswept_isle",    "op": "not_exists"}],
         "Fifth ward-stone's on the Windswept Isle — ruins out in open ocean. Any of the three main docks can sail you there."),
        ([{"flag": "quest.main_act3_finale.state", "op": ">=", "value": 1},
          {"flag": "quest.main_act3_finale.state", "op": "!=", "value": -2}],
         "All five ward-stones. That's the whole set. If anyone's going up the Spire, it's happening soon."),
    ]

    # Build weighted pool: base rumors × 1, matching story rumors × 3
    pool = list(base_pool)
    for conds, text in STORY_RUMORS:
        if check_conditions(conds):
            pool.extend([text, text, text])  # weight 3×

    return random.choice(pool)


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
                "loop": True,
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
                "loop": True,
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
                "loop": True,
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Captain Aldric",
                        "text": "I'm the town guard captain. Twelve men, one broken crossbow, and a gate that sticks. If trouble comes, I'm counting on adventurers more than I should be.",
                        "choices": [
                            {"text": "What kind of trouble?", "next": "trouble"},
                            {"text": "Any missing patrols?", "next": "patrol"},
                            {"text": "The mine — what do you know about it?", "next": "mine"},
                            {"text": "Old Petra mentioned spiders on the Thornwood path.", "next": "spiders",
                             "conditions": [{"flag": "npc.old_petra.met", "op": "==", "value": True},
                                            {"flag": "boss_defeated.spiders_nest", "op": "not_exists"}]},
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
                    "spiders": {
                        "speaker": "Captain Aldric",
                        "text": "Petra's been saying that for weeks. I thought it was her eyes. "
                                "But two of my guards won't take the eastern watch anymore — "
                                "won't say why, just won't. Cave east of town, past the old mill. "
                                "I'd consider it a personal favour if you looked in.",
                        "on_enter": [{"action": "start_quest", "quest": "main_spiders_nest"}],
                        "choices": [{"text": "We'll check it out.", "next": None}],
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
                "loop": True,
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
                "loop": True,
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
                "loop": True,
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
                        "text": "Six months ago she was just a big spider. Now she's the size of a cart horse and her brood covers the whole northwest slope. Something's feeding her growth. The same thing that's killing the trees, maybe.",
                        "choices": [{"text": "We'll find out.", "next": None}],
                    },
                },
            },
        },
        {
            "conditions": [],
            "tree": {
                "id": "lyric_default",
                "loop": True,
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
                        "text": "Check the job board. Guildmaster Oren posts contracts. But between us — the real problem is the spider nest to the northwest. It's getting out of hand.",
                        "choices": [{"text": "We'll look into it.", "next": None}],
                    },
                },
            },
        },
    ],

    "old_moss": [
        # Spider's Nest AND Warren cleared — forest recovering
        {
            "conditions": [
                {"flag": "boss_defeated.spiders_nest", "op": "==", "value": True},
                {"flag": "boss_defeated.goblin_warren", "op": "==", "value": True},
            ],
            "tree": {"id": "moss_recovery", "loop": True, "nodes": {
                "start": {"speaker": "Old Moss",
                    "text": "The western forest breathes easier. The goblins are gone, "
                            "the spider colony is collapsed. Three hundred years I've "
                            "watched this forest and it always comes back. "
                            "But it needs someone to stop the harm first. "
                            "You stopped the harm. The forest will do the rest.",
                    "choices": [
                        {"text": "The Fading is still spreading east.", "next": "east"},
                        {"text": "The tree you mentioned — the Warden tree.", "next": "tree"},
                    ]},
                "east": {"speaker": "Old Moss",
                    "text": "I know. I feel it every morning. The recovery in the west "
                            "is real — but it's happening against resistance from the east. "
                            "Whatever the source is, find it. The forest can endure "
                            "for a time. Not forever.",
                    "choices": [{"text": "We're on our way.", "next": None}]},
                "tree": {"speaker": "Old Moss",
                    "text": "Still there. Still untouched by the Fading. "
                            "I've been watching it — it grows toward the east, "
                            "as if it's reaching for something. "
                            "Or pointing at something.",
                    "on_enter": [{"action": "set_flag", "flag": "lore.greenwood_warden_tree", "value": True}],
                    "choices": [{"text": "The Hearthstones.", "next": None}]},
            }},
        },
        # Spider's Nest cleared alone
        {
            "conditions": [{"flag": "boss_defeated.spiders_nest", "op": "==", "value": True}],
            "tree": {"id": "moss_post_spiders", "loop": True, "nodes": {
                "start": {"speaker": "Old Moss",
                    "text": "The spider queen is dead. I felt it — like a knot releasing "
                            "in the root network. The Fading had her, you know. "
                            "She wasn't malicious. She was desperate. "
                            "Desperate creatures do harm. You ended the harm.",
                    "choices": [
                        {"text": "How did you feel it in the roots?", "next": "roots"},
                        {"text": "Is the forest recovering?", "next": "recover"},
                    ]},
                "roots": {"speaker": "Old Moss",
                    "text": "The old trees are connected below ground. Information passes "
                            "through them — slowly, like sap in winter. I've been reading "
                            "the roots for two hundred years. You learn to listen.",
                    "choices": [{"text": "What are they saying now?", "next": None}]},
                "recover": {"speaker": "Old Moss",
                    "text": "The western groves, yes. The eastern ones — not yet. "
                            "The Fading is still feeding from the east. "
                            "Clearing the spiders was necessary. Not sufficient.",
                    "choices": [{"text": "We'll keep going.", "next": None}]},
            }},
        },
        # Act 2+ — has felt the Fading spread
        {
            "conditions": [
                {"flag": "quest.main_ashenmoor.state", "op": ">=", "value": 1},
            ],
            "tree": {"id": "moss_act2", "nodes": {
                "start": {"speaker": "Old Moss",
                    "text": "Three hundred years I've tended this forest. "
                            "Watched it breathe. Watched it dream. "
                            "Now it's forgetting itself. The old trees — the ones that remember "
                            "before the kingdoms — they're the first to go quiet.",
                    "choices": [
                        {"text": "Can you feel where the Fading is worst?", "next": "worst"},
                        {"text": "Is there anything the forest can do?", "next": "forest"},
                        {"text": "I'm sorry.", "next": "sorry"},
                    ]},
                "worst": {"speaker": "Old Moss",
                    "text": "East. Always east now. There's a silence there that shouldn't exist — "
                            "no wind, no insects, no sense of time. "
                            "Whatever broke the wards broke them hardest in that direction.",
                    "on_enter": [{"action": "discover_lore", "lore": "fading_east_origin"}],
                    "end": True},
                "forest": {"speaker": "Old Moss",
                    "text": "The forest doesn't fight the way soldiers fight. "
                            "It endures. It waits. It remembers. "
                            "Restore the wards and it will come back.",
                    "end": True},
                "sorry": {"speaker": "Old Moss",
                    "text": "Don't be sorry. Be effective. "
                            "The forest doesn't need your grief. It needs the wards back.",
                    "end": True},
            }},
        },
        # First meeting
        {
            "conditions": [
                {"flag": "npc.old_moss.met", "op": "not_exists"},
            ],
            "tree": {"id": "moss_intro", "nodes": {
                "start": {"speaker": "Old Moss",
                    "text": "You smell like the road. And something older. "
                            "Blood from before the kingdoms, if I'm reading you right. "
                            "Warden blood. Haven't smelled that in a long time.",
                    "on_enter": [{"action": "meet_npc", "npc": "old_moss"}],
                    "choices": [
                        {"text": "You know about the Wardens?", "next": "wardens"},
                        {"text": "What are you?", "next": "what"},
                        {"text": "Just passing through.", "next": "bye"},
                    ]},
                "wardens": {"speaker": "Old Moss",
                    "text": "I knew the last generation of them. One planted a tree in the "
                            "southern grove that still grows. The Fading hasn't touched it. "
                            "I think it's waiting for someone.",
                    "on_enter": [{"action": "discover_lore", "lore": "wardens_greenwood_tree"}],
                    "next": "wardens2"},
                "wardens2": {"speaker": "Old Moss",
                    "text": "The tree is still there. Still untouched. I watered it every year, "
                            "hoping they'd come back for it.",
                    "on_enter": [{"action": "set_flag", "flag": "lore.greenwood_warden_tree", "value": True}],
                    "end": True},
                "what": {"speaker": "Old Moss",
                    "text": "Old. That's the simplest answer. I've been called a druid, "
                            "a hermit, a forest spirit. The trees know me. That's enough.",
                    "end": True},
                "bye": {"speaker": "Old Moss",
                    "text": "No one just passes through Greenwood. "
                            "You came here for a reason. You'll remember it eventually.",
                    "end": True},
            }},
        },
        {
            "conditions": [],
            "tree": {
                "id": "moss_default",
                "nodes": {
                    "start": {
                        "speaker": "Old Moss",
                        "text": "The forest is listening. It always is. "
                                "What do you want to know?",
                        "choices": [
                            {"text": "What's happening to the animals?", "next": "animals"},
                            {"text": "Can you read the Fading somehow?", "next": "fading"},
                            {"text": "Nothing. Just wanted to say hello.", "next": "bye"},
                        ],
                    },
                    "animals": {
                        "speaker": "Old Moss",
                        "text": "Shadow energy gets into them. The ones close to Fading zones "
                                "start hearing something the rest of us can't — a kind of pulling. "
                                "It doesn't hurt them at first. Then it changes them. "
                                "I've been watching it for months. It's getting faster.",
                        "end": True,
                    },
                    "fading": {
                        "speaker": "Old Moss",
                        "text": "Not read, exactly. But I can feel where the quiet is wrong. "
                                "There are places in this forest where even the wind goes still "
                                "without cause. Those are the edges. Stay away from them. "
                                "Or don't, if you're the type who moves toward trouble.",
                        "end": True,
                    },
                    "bye": {
                        "speaker": "Old Moss",
                        "text": "Hello. "
                                "The trees say hello too.",
                        "end": True,
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
                "loop": True,
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
                        "text": "Check the job board outside. I post what comes in. Right now it's mostly patrol work and pest control. The spider situation to the northwest is getting serious — I'm offering a premium for proof of the nest being cleared.",
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
                "loop": True,
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
                "loop": True,
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
                "loop": True,
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
        # Mine cleared
        {
            "conditions": [{"flag": "boss_defeated.abandoned_mine", "op": "==", "value": True}],
            "tree": {"id": "durk_post_mine", "loop": True, "nodes": {
                "start": {"speaker": "Miner Durk",
                    "text": "You cleared the Mine. I worked the second level for eight years. "
                            "Knew every crossbeam and airshaft. When the Wardens stopped "
                            "answering, I thought that was it. Gone forever. "
                            "Can we go back in?",
                    "choices": [
                        {"text": "The upper levels should be clear.", "next": "safe"},
                        {"text": "Be careful. The Fading has changed things.", "next": "changed"},
                    ]},
                "safe": {"speaker": "Miner Durk",
                    "text": "Then I'm going back. Half my crew is waiting on word. "
                            "We can have ore moving in a week if the shafts are intact. "
                            "Ironhearth will breathe again. What you've done — "
                            "it's not nothing.",
                    "choices": [{"text": "Good luck, Durk.", "next": None}]},
                "changed": {"speaker": "Miner Durk",
                    "text": "Changed how? The passages, the rock, the air? "
                            "I've worked in bad air before. I've worked in collapsing shafts. "
                            "I haven't worked in Fading-touched stone. "
                            "...I'll take a priest with me.",
                    "choices": [{"text": "Wise decision.", "next": None}]},
            }},
        },
        # Explored the mine
        {
            "conditions": [{"flag": "explored.abandoned_mine.floor1", "op": "==", "value": True}],
            "tree": {"id": "durk_explored", "loop": True, "nodes": {
                "start": {"speaker": "Miner Durk",
                    "text": "You've been in the Mine? What's in there? The Wardens — "
                            "are they... is there anything left?",
                    "choices": [
                        {"text": "There's a Warden named Korrath holding an anchor.", "next": "korrath"},
                        {"text": "It's not safe yet.", "next": "not_safe"},
                    ]},
                "korrath": {"speaker": "Miner Durk",
                    "text": "Korrath. I know that name — he was the garrison commander. "
                            "Old-school Warden, twenty years of service. "
                            "He's still in there? Holding alone?",
                    "choices": [{"text": "He held as long as he could.", "next": None}]},
                "not_safe": {"speaker": "Miner Durk",
                    "text": "Then we wait. I've been waiting three months — "
                            "I can wait a bit longer. Come back when it's done.",
                    "choices": [{"text": "We will.", "next": None}]},
            }},
        },
        # Default
        {
            "conditions": [],
            "tree": {"id": "durk_default", "loop": True, "nodes": {
                "start": {"speaker": "Miner Durk",
                    "text": "Waiting for the Mine to reopen. Eight years I worked that mountain. "
                            "Now nobody'll go near it. The Wardens went in a month ago "
                            "and haven't come out.",
                    "on_enter": [{"action": "meet_npc", "npc": "miner_durk"}],
                    "choices": [
                        {"text": "What happened to the Wardens?", "next": "wardens"},
                        {"text": "What's in the mine?", "next": "mine"},
                        {"text": "We'll look into it.", "next": None},
                    ]},
                "wardens": {"speaker": "Miner Durk",
                    "text": "Twelve of them went in. Commander Korrath, seasoned veterans. "
                            "We stopped hearing from them after the first week. "
                            "The Fading's bad in there — you can feel it from the entrance. "
                            "Like the air's wrong.",
                    "choices": [{"text": "We're going to investigate.", "next": None}]},
                "mine": {"speaker": "Miner Durk",
                    "text": "Iron ore, mainly. Ironhearth runs on it. Three shafts, "
                            "five levels, been producing for sixty years. "
                            "The lower levels hit a void-crystal seam two years ago — "
                            "that's when things started getting strange.",
                    "choices": [{"text": "Void crystals and the Fading.", "next": None}]},
            }},
        },
    ],

    "apprentice_tova": [
        {
            "conditions": [],
            "tree": {
                "id": "tova_default",
                "loop": True,
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
        # ── Abandoned Mine cleared (Act 1 complete) ─────────────────
        {
            "conditions": [{"flag": "boss_defeated.abandoned_mine", "op": "==", "value": True}],
            "tree": {
                "id": "feryn_post_mine",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Scout Feryn",
                        "text": "The Abandoned Mine north of Ironhearth — word came down the trade road. "
                                "A Warden garrison went in and never came out. You went in and came back. "
                                "That means something. The eastern forest has been quieter since. "
                                "Not safe — but quieter.",
                        "choices": [
                            {"text": "Something in that mine was driving the Fading.", "next": "fading"},
                            {"text": "We found a Hearthstone fragment.", "next": "stone"},
                            {"text": "What's your next concern out here?", "next": "next"},
                        ],
                    },
                    "fading": {
                        "speaker": "Scout Feryn",
                        "text": "That tracks with what I've been seeing. The black-root spread slowed around the old stone "
                                "markers the week after you went in. Didn't know what caused it. Now I do.",
                        "choices": [{"text": "There are more of them to find.", "next": None}],
                    },
                    "stone": {
                        "speaker": "Scout Feryn",
                        "text": "A Hearthstone. I've heard the old stories — the Warden Order used them as anchors. "
                                "They sealed the Fading last time it came. How many are there?",
                        "choices": [{"text": "Five. We need all of them.", "next": None}],
                    },
                    "next": {
                        "speaker": "Scout Feryn",
                        "text": "South. Something is moving in the marshes past the river — big, slow, and wrong. "
                                "I've been tracking it for two weeks and I still don't know what it is. "
                                "My guess: it came from the Fading zone to the east.",
                        "choices": [{"text": "We'll investigate.", "next": None}],
                    },
                },
            },
        },
        # ── Spider's Nest cleared ────────────────────────────────────
        {
            "conditions": [{"flag": "boss_defeated.spiders_nest", "op": "==", "value": True}],
            "tree": {
                "id": "feryn_post_spiders",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Scout Feryn",
                        "text": "The Spider's Nest is cleared — I confirmed it personally yesterday. "
                                "The eastern trail is open again. You have no idea what that means for patrol routes. "
                                "We've been skirting that whole stretch for two seasons.",
                        "choices": [
                            {"text": "The Queen was changed by something.", "next": "queen"},
                            {"text": "What's north of Ironhearth?", "next": "north"},
                            {"text": "Good. What's next?", "next": "next"},
                        ],
                    },
                    "queen": {
                        "speaker": "Scout Feryn",
                        "text": "I know. I saw the body on the way in. That wasn't a natural spider — "
                                "whatever the Fading touches, it doesn't just kill it. It transforms it. "
                                "Makes it more. Worse.",
                        "choices": [{"text": "We're learning that too.", "next": None}],
                    },
                    "north": {
                        "speaker": "Scout Feryn",
                        "text": "Abandoned Mine, past Ironhearth. A Warden garrison held it until a month ago. "
                                "No word since. That's where your trail leads next, if you're following the Fading.",
                        "choices": [{"text": "Thanks.", "next": None}],
                    },
                    "next": {
                        "speaker": "Scout Feryn",
                        "text": "The Fading is still spreading east. The spiders were a symptom. "
                                "Clearing them bought us time, not a solution. If you've got the stomach for more — "
                                "the mine north of Ironhearth needs looking at.",
                        "choices": [{"text": "We'll go.", "next": None}],
                    },
                },
            },
        },
        # ── Goblin Warren cleared, Spider's Nest not yet ─────────────
        {
            "conditions": [{"flag": "boss_defeated.goblin_warren", "op": "==", "value": True}],
            "tree": {
                "id": "feryn_post_warren",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Scout Feryn",
                        "text": "Heard about the Goblin Warren. Good. Goblins were the least of the problems "
                                "but clearing them opened the southern trail. "
                                "The Spider's Nest to the east is still a problem — a big one.",
                        "choices": [
                            {"text": "Tell me about the Spider's Nest.", "next": "spiders"},
                            {"text": "We have a mine key from the spiders.", "next": "key"},
                            {"text": "What else is out there?", "next": "else"},
                        ],
                    },
                    "spiders": {
                        "speaker": "Scout Feryn",
                        "text": "Massive web cave, northeast of here. The colony is old — been there for decades, "
                                "mostly harmless. Two months ago they started expanding. Lost two rangers "
                                "scouting it. Whatever changed them, it came from inside.",
                        "choices": [{"text": "We'll go in.", "next": None}],
                    },
                    "key": {
                        "speaker": "Scout Feryn",
                        "text": "A mine key. Then you've been to the Spider's Nest already. "
                                "That key goes to the Abandoned Mine north of Ironhearth — "
                                "Warden garrison held it until recently. Something happened to them.",
                        "choices": [{"text": "We're on it.", "next": None}],
                    },
                    "else": {
                        "speaker": "Scout Feryn",
                        "text": "The whole eastern forest is wrong. Animals acting strangely, "
                                "old stone markers going black at the roots. The Fading is "
                                "coming from somewhere specific — I just can't get close enough to find out.",
                        "choices": [{"text": "We're working on it.", "next": None}],
                    },
                },
            },
        },
        # ── Default (first meeting) ──────────────────────────────────
        {
            "conditions": [],
            "tree": {
                "id": "feryn_default",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Scout Feryn",
                        "text": "You made it out here. Good. These woods get worse every season — "
                                "even the birds have been acting strange. I scout this territory "
                                "and I've been doing it fifteen years. Something has changed.",
                        "on_enter": [{"action": "set_flag", "flag": "npc.feryn.met", "value": True}],
                        "choices": [
                            {"text": "What's changed specifically?", "next": "changed"},
                            {"text": "Any threats we should know about?", "next": "threats"},
                        ],
                    },
                    "changed": {
                        "speaker": "Scout Feryn",
                        "text": "The spider population tripled in two seasons. Wolves are ranging further than "
                                "I've ever seen. And there's a low sound in the deep forest, just at the edge "
                                "of hearing. The trees around the old stone sites have all gone black at the root.",
                        "choices": [{"text": "Old stone sites?", "next": "stones"}],
                    },
                    "stones": {
                        "speaker": "Scout Feryn",
                        "text": "Places the old settlers marked. Rings of flat stones, mostly grown over now. "
                                "I leave them alone. Started going wrong around the time workers showed up "
                                "from the capital. Coincidence, maybe.",
                        "choices": [{"text": "Probably not a coincidence.", "next": None}],
                    },
                    "threats": {
                        "speaker": "Scout Feryn",
                        "text": "Giant spiders to the east — I mean giant, house-sized. Don't go alone. "
                                "To the north, wolves that don't run when you shout at them. "
                                "And something worse I can't pin down, south of the river.",
                        "choices": [{"text": "We'll stay sharp.", "next": None}],
                    },
                },
            },
        },
    ],

    "trapper_holt": [
        # After Spider's Nest AND Warren cleared
        {
            "conditions": [
                {"flag": "boss_defeated.spiders_nest", "op": "==", "value": True},
                {"flag": "boss_defeated.goblin_warren", "op": "==", "value": True},
            ],
            "tree": {"id": "holt_both_cleared", "loop": True, "nodes": {
                "start": {"speaker": "Trapper Holt",
                    "text": "The spiders are gone and the goblins are gone. I pulled four decent "
                            "pelts yesterday — first time in two seasons. The animals are "
                            "calmer. Still some wrong ones further east, but the western "
                            "Thornwood is recovering. I owe you a drink.",
                    "choices": [
                        {"text": "What's still wrong in the east?", "next": "east"},
                        {"text": "Glad things are improving.", "next": None},
                    ]},
                "east": {"speaker": "Trapper Holt",
                    "text": "Shadow-touched animals. I know the signs now — pupils wrong, "
                            "movements too deliberate. They don't run from fire. "
                            "Whatever the Fading is doing to the forest, it's still doing it "
                            "east of the river. Everything there is changed.",
                    "choices": [{"text": "We'll follow the Fading east.", "next": None}]},
            }},
        },
        # After Spider's Nest cleared
        {
            "conditions": [{"flag": "boss_defeated.spiders_nest", "op": "==", "value": True}],
            "tree": {"id": "holt_post_spiders", "loop": True, "nodes": {
                "start": {"speaker": "Trapper Holt",
                    "text": "The spider cave is cleared? I can go back to the northern trails. "
                            "I haven't been able to set traps north of the ridge for months. "
                            "The spiders were taking everything — even my steel traps. "
                            "I found three of them dissolved in web.",
                    "choices": [
                        {"text": "The Queen was enormous.", "next": "queen"},
                        {"text": "The trail's yours again.", "next": None},
                    ]},
                "queen": {"speaker": "Trapper Holt",
                    "text": "I saw her once, from a distance. Big as a barn. Moving wrong — "
                            "too intentional for an animal, even a smart one. "
                            "Whatever changed her, it wasn't natural.",
                    "choices": [{"text": "The Fading changed her.", "next": None}]},
            }},
        },
        # Default
        {
            "conditions": [],
            "tree": {"id": "holt_default", "loop": True, "nodes": {
                "start": {"speaker": "Trapper Holt",
                    "text": "Haven't pulled a decent pelt in three weeks. Animals are either "
                            "gone or wrong. Found a fox last Tuesday — twice normal size, "
                            "moving like a drunk. Left it alone.",
                    "on_enter": [{"action": "meet_npc", "npc": "trapper_holt"}],
                    "choices": [
                        {"text": "Something's affecting the animals?", "next": "animals"},
                        {"text": "Any idea what's causing it?", "next": "cause"},
                    ]},
                "animals": {"speaker": "Trapper Holt",
                    "text": "The spiders north are worst. The colony expanded — they're "
                            "in territory they've never touched before. And the web trail "
                            "south suggests they're pushing outward, not just growing. "
                            "Something's driving them.",
                    "choices": [{"text": "We'll clear the spider nest.", "next": None}]},
                "cause": {"speaker": "Trapper Holt",
                    "text": "The Fading, most likely. I've been a trapper for twenty years — "
                            "I know what forest sickness looks like. This is different. "
                            "The animals aren't sick. They're... changed.",
                    "choices": [{"text": "We're investigating.", "next": None}]},
            }},
        },
    ],

    # ── Saltmere ───────────────────────────────────────────

    "shady_figure": [
        {
            "conditions": [],
            "tree": {
                "id": "shady_default",
                "loop": True,
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
                "loop": True,
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
                "id": "oran_default",
                "loop": True,             "nodes": {
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
                "loop": True,
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
            "conditions": [{"flag": "boss_defeated.shadow_valdris", "op": "==", "value": True}],
            "tree": {
                "id": "knight_post_valdris",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Holy Knight",
                        "text": "The Order received word from the Spire. The High Priest has declared a day of silence in your honour. We do not do that for the living. Consider it unusual.",
                        "choices": [
                            {"text": "What happens to the Order now?", "next": "order"},
                            {"text": "We didn't do it for recognition.", "next": "recognition"},
                        ],
                    },
                    "order": {
                        "speaker": "Holy Knight",
                        "text": "We rebuild. The cathedral has stood for four centuries — it will stand four more. But the threat we were founded to watch for has arrived and passed. We need to decide what we are when the vigil is over.",
                        "choices": [{"text": "A harder question than fighting.", "next": None}],
                    },
                    "recognition": {
                        "speaker": "Holy Knight",
                        "text": "No. I know that. That's why the silence is for you and not the other kind of ceremony. We honour what was done, not the names attached to it. The Light doesn't need names. Neither do you, apparently.",
                        "choices": [{"text": "Thank you.", "next": None}],
                    },
                },
            },
        },
        {
            "conditions": [],
            "tree": {
                "id": "knight_default",
                "loop": True,
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
                "loop": True,
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
            "conditions": [
                {"flag": "item.hearthstone.5", "op": "==", "value": True},
            ],
            "tree": {
                "id": "aldara_all_stones",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "High Priest Aldara",
                        "text": "All five.\nI felt the last one settle into the network — like a bone "
                                "snapping back into place.\n"
                                "You must go to Valdris' Spire. To the north-east, beyond the "
                                "Holdfast. The Hearthstones must be restored to the First Stone "
                                "at the Spire's heart — together, in sequence. "
                                "Maren will know the order. Do not attempt it without her.",
                        "choices": [
                            {"text": "What will happen when they're restored?", "next": "restoration"},
                            {"text": "Is Valdris there?",                        "next": "valdris"},
                            {"text": "We leave at once.",                         "next": None},
                        ],
                    },
                    "restoration": {
                        "speaker": "High Priest Aldara",
                        "text": "The wards seal. The wound between planes closes. "
                                "The Fading stops spreading — and what it has already taken "
                                "may, slowly, return.\n"
                                "I said may. I will not promise what is beyond my knowledge.",
                        "choices": [{"text": "That's enough.", "next": None}],
                    },
                    "valdris": {
                        "speaker": "High Priest Aldara",
                        "text": "Almost certainly. He's been working from inside the Spire — "
                                "using its ley anchor to direct the Fading outward while "
                                "keeping himself shielded.\n"
                                "He will not step aside. Be ready for that.",
                        "choices": [{"text": "We're ready.", "next": None}],
                    },
                },
            },
        },
        {
            "conditions": [
                {"flag": "item.hearthstone.1", "op": "==", "value": True},
                {"flag": "item.hearthstone.5", "op": "!=", "value": True},
            ],
            "tree": {
                "id": "aldara_knows_fragment",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "High Priest Aldara",
                        "text": "You carry it.\nI can feel it from here — the resonance is unmistakable. "
                                "A Hearthstone fragment.\n"
                                "Do you understand what you're holding? "
                                "These stones are the anchors the first Wardens placed "
                                "when they built the barrier. "
                                "Every one you recover strengthens what remains.",
                        "on_enter": [
                            {"action": "meet_npc", "npc": "high_priest_aldara"},
                            {"action": "set_flag", "flag": "npc.high_priest_aldara.met", "value": True},
                            {"action": "discover_lore", "lore": "lore.aldara_relic"},
                        ],
                        "choices": [
                            {"text": "How many are there?",            "next": "count"},
                            {"text": "Can you tell us more about them?","next": "lore"},
                            {"text": "We could use a blessing.",        "next": "blessing"},
                        ],
                    },
                    "count": {
                        "speaker": "High Priest Aldara",
                        "text": "Five. Scattered when the Order fell — the last Wardens hid them "
                                "rather than let Valdris consolidate them.\n"
                                "The Reliquary here holds maps of the old ward-anchor sites. "
                                "They may narrow your search.",
                        "choices": [
                            {"text": "We'll look at the maps.", "next": None},
                            {"text": "A blessing first.",       "next": "blessing"},
                        ],
                    },
                    "lore": {
                        "speaker": "High Priest Aldara",
                        "text": "Each stone is keyed to a ward-anchor point. "
                                "They don't merely store power — they resonate with each other. "
                                "As you recover more, the network strengthens, "
                                "and the Fading slows near the anchor sites.\n"
                                "You'll feel it. Your people will feel it. That's how you know "
                                "you're winning.",
                        "choices": [{"text": "Good to know.", "next": None}],
                    },
                    "blessing": {
                        "speaker": "High Priest Aldara",
                        "text": "Kneel.\nLight of the First Ward, carried by these five against the dark — "
                                "let them pass unseen where shadow gathers, "
                                "let them strike true where it matters most, "
                                "and let them find their way back when it is done.\n"
                                "Go. And do not waste it.",
                        "on_enter": [
                            {"action": "set_flag", "flag": "blessing.cathedral", "value": True},
                        ],
                        "choices": [{"text": "Thank you.", "next": None}],
                    },
                },
            },
        },
        {
            "conditions": [
                {"flag": "maren.left", "op": "==", "value": True},
            ],
            "tree": {
                "id": "aldara_act3",
                "nodes": {
                    "start": {
                        "speaker": "High Priest Aldara",
                        "text": "We have seen a thousand pilgrims a day since the eastern sky went dark. "
                                "People want somewhere to pray. I cannot tell them their prayers will be enough. "
                                "I can only tell them they are not alone in the dark.",
                        "choices": [
                            {"text": "Are you afraid?", "next": "afraid"},
                            {"text": "We're going to the Spire.", "next": "spire"},
                            {"text": "We need absolution before we go.", "next": "absolution"},
                        ],
                    },
                    "afraid": {
                        "speaker": "High Priest Aldara",
                        "text": "Every day for forty years I have stood in front of people in pain "
                                "and told them the light holds. Today I believe it more than I ever have. "
                                "Not because the evidence is good — it isn't. "
                                "Because you are still standing.",
                        "end": True,
                    },
                    "spire": {
                        "speaker": "High Priest Aldara",
                        "text": "Then go. The Cathedral's blessing goes with you, "
                                "for whatever weight that carries in a place of shadow. "
                                "Come back. If you can, come back.",
                        "on_enter": [{"action": "set_flag", "flag": "blessing.cathedral", "value": True}],
                        "end": True,
                    },
                    "absolution": {
                        "speaker": "High Priest Aldara",
                        "text": "Kneel, then. All of you. "
                                "Whatever you have done, whatever choices you made to survive this far — "
                                "you made them trying to save a world that doesn't deserve saving half as much "
                                "as it deserves people like you trying to save it. "
                                "Go. Be absolved.",
                        "on_enter": [
                            {"action": "set_flag", "flag": "blessing.absolution", "value": True},
                            {"action": "discover_lore", "lore": "aldara_absolution"},
                        ],
                        "end": True,
                    },
                },
            },
        },
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
        {
            "conditions": [{"flag": "lore.fading_basics", "op": "==", "value": True}],
            "tree": {
                "id": "aldara_knows",
                "loop": True,
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
                "loop": True,
                "loop": True,
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

    # ── Crystalspire ───────────────────────────────────────

    "apprentice_mage": [
        {
            "conditions": [{"flag": "boss_defeated.shadow_valdris", "op": "==", "value": True}],
            "tree": {
                "id": "app_mage_post_valdris",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Apprentice Mage",
                        "text": "The ley line readings normalized last night. I've been logging them every six hours for eight months. Last night they just — came back. Not fully. But the decay curve reversed. The Archmage cried. I've never seen him cry.",
                        "choices": [
                            {"text": "The Hearthstone network is holding.", "next": "holding"},
                            {"text": "What does this mean for your research?", "next": "research"},
                        ],
                    },
                    "holding": {
                        "speaker": "Apprentice Mage",
                        "text": "We know. Solen explained it. Five stones, five anchors, the ward-grid reconstructed from scratch. The theory was right — the extraction was killing it. You proved the extraction was killing it. My thesis thanks you.",
                        "choices": [{"text": "Don't let them bury it this time.", "next": None}],
                    },
                    "research": {
                        "speaker": "Apprentice Mage",
                        "text": "It means I can publish. It means the administration can't bury it anymore because the evidence just became visible to anyone with a measuring rod. It means I graduate. Eventually.",
                        "choices": [{"text": "Good luck.", "next": None}],
                    },
                },
            },
        },
        {
            "conditions": [{"flag": "item.hearthstone.5", "op": "==", "value": True}],
            "tree": {
                "id": "app_mage_all_stones",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Apprentice Mage",
                        "text": "Five stones. I ran the numbers three times. The resonance coming off the network right now is — it's loud. Beautifully loud. The crystals in the city have been humming for the last hour. Most people don't notice. I notice.",
                        "choices": [
                            {"text": "What happens when the network is complete?", "next": "complete"},
                            {"text": "We have one more thing to do.", "next": "spire"},
                        ],
                    },
                    "complete": {
                        "speaker": "Apprentice Mage",
                        "text": "In theory? The Fading loses its hold. The extracted energy is returned to the ley lines. The decay reverses. In practice — I've never seen a complete network. Nobody alive has. We're about to find out.",
                        "choices": [{"text": "We're going to find out.", "next": None}],
                    },
                    "spire": {
                        "speaker": "Apprentice Mage",
                        "text": "I know. Solen told us. Go. Whatever's waiting up there — the math is on your side now. The network is ready. You just have to finish it.",
                        "choices": [{"text": "That's the plan.", "next": None}],
                    },
                },
            },
        },
        {
            "conditions": [],
            "tree": {
                "id": "app_mage_default",
                "loop": True,
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
            "conditions": [{"flag": "boss_defeated.shadow_valdris", "op": "==", "value": True}],
            "tree": {
                "id": "scholar_post_valdris",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Crystal Scholar",
                        "text": "The resonator is singing. I mean that literally — there's a frequency coming off the crystals right now that's audible if you stand in the central plaza at dawn. People keep thinking it's the bells. It isn't the bells.",
                        "choices": [
                            {"text": "The ward-grid is restored.", "next": "restored"},
                            {"text": "Is the city safe now?", "next": "safe"},
                        ],
                    },
                    "restored": {
                        "speaker": "Crystal Scholar",
                        "text": "Restored and self-sustaining, if the models hold. The Hearthstones aren't drawing from the ley lines anymore — they're feeding back into them. The network is generating its own resonance. The founders built something that could outlast its makers. It almost did.",
                        "choices": [{"text": "Almost.", "next": None}],
                    },
                    "safe": {
                        "speaker": "Crystal Scholar",
                        "text": "From the Fading? Yes. From everything else — still working on that. But the specific extinction-level collapse I've been modelling for two years is no longer on the projection chart. I slept for eleven hours last night. First time in months.",
                        "choices": [{"text": "You've earned it.", "next": None}],
                    },
                },
            },
        },
        {
            "conditions": [{"flag": "item.hearthstone.5", "op": "==", "value": True}],
            "tree": {
                "id": "scholar_all_stones",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Crystal Scholar",
                        "text": "Five Hearthstones in the network simultaneously. I didn't think I'd ever see this data. The resonator is amplifying the combined signal — the whole city is acting as a single antenna pointed at the Spire. Whatever is anchoring the Fading up there is about to have a very bad time.",
                        "choices": [
                            {"text": "That's the idea.", "next": None},
                            {"text": "We're going there now.", "next": "going"},
                        ],
                    },
                    "going": {
                        "speaker": "Crystal Scholar",
                        "text": "Then go quickly. The signal is at peak resonance now — and it won't hold forever. The network is ready. It's been ready and waiting for someone to use it for a thousand years.",
                        "choices": [{"text": "We won't waste it.", "next": None}],
                    },
                },
            },
        },
        {
            "conditions": [],
            "tree": {
                "id": "scholar_default",
                "loop": True,
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
        # Act 3 — All 5 stones, Maren left: send-off
        {
            "conditions": [
                {"flag": "item.hearthstone.5", "op": "==",    "value": True},
                {"flag": "maren.left",         "op": "==",    "value": True},
            ],
            "tree": {
                "id": "solen_all_stones",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Archmage Solen",
                        "text": "Five stones. The full network. I confess I did not think "
                                "you would assemble them in time. The resonance from here is "
                                "extraordinary — the ward-grid is almost whole. "
                                "Now go. The Spire is north of Thornhaven. "
                                "Whatever Valdris is doing at the summit, "
                                "you need to reach him before the network seals.",
                        "choices": [
                            {"text": "What will we find at the top?",    "next": "top"},
                            {"text": "What about Maren?",                "next": "maren"},
                            {"text": "We're going now.",                 "next": "bye"},
                        ],
                    },
                    "top": {
                        "speaker": "Archmage Solen",
                        "text": "A man who spent thirty years studying the ward-network "
                                "and then decided he understood it well enough to tear it apart. "
                                "Whether what remains of him is still human is a question "
                                "I cannot answer from here.",
                        "next": "start",
                    },
                    "maren": {
                        "speaker": "Archmage Solen",
                        "text": "She has been inside the Spire for days. "
                                "I have watched the resonance patterns shift — she is working "
                                "the stones somehow, trying to stabilise something from within. "
                                "Whether she can be reached, I do not know. "
                                "But she has not collapsed the network. Not yet.",
                        "next": "start",
                    },
                    "bye": {
                        "speaker": "Archmage Solen",
                        "text": "Then go. I will watch the instruments. "
                                "If the network holds, I will know you succeeded.",
                        "end": True,
                    },
                },
            },
        },
        # Act 3 — Fewer than 5 stones, Maren left: urgent warning + guidance
        {
            "conditions": [
                {"flag": "maren.left",         "op": "==",        "value": True},
                {"flag": "item.hearthstone.5", "op": "not_exists"},
            ],
            "tree": {
                "id": "solen_act3_warning",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Archmage Solen",
                        "text": "She is gone. I know. And I know you are thinking about "
                                "going after her directly. I am telling you: do not. "
                                "Not yet. If you enter the Spire with fewer than five stones, "
                                "Valdris has more power than you. You will not come back.",
                        "choices": [
                            {"text": "We don't have time to collect more stones.",  "next": "no_time"},
                            {"text": "Where are the remaining stones?",             "next": "where"},
                            {"text": "What exactly is at the Spire?",               "next": "spire_info"},
                            {"text": "We'll be careful.",                           "next": "bye"},
                        ],
                    },
                    "no_time": {
                        "speaker": "Archmage Solen",
                        "text": "You have more time than you think. Maren entering the Spire "
                                "is not the end — she is trying to negotiate something, or "
                                "she would not have gone alone. She is buying time for you. "
                                "Use it. Two more stones. Pale Coast, then the Windswept Isle.",
                        "next": "where",
                    },
                    "where": {
                        "speaker": "Archmage Solen",
                        "text": "The fourth stone is held by the Pale Sentinel — "
                                "a Warden who sealed herself at the Pale Coast Catacombs "
                                "rather than risk corruption. She may yield it peacefully "
                                "if you can demonstrate you are worthy of the ward-network's trust. "
                                "The fifth is on the Windswept Isle — bound to a pre-order "
                                "elemental that will not reason with you. That one you fight.",
                        "next": "start",
                    },
                    "spire_info": {
                        "speaker": "Archmage Solen",
                        "text": "Valdris was the last Warden before the order dissolved. "
                                "He did not break the ward-network out of malice. "
                                "He broke it because he believed the Fading was a natural process — "
                                "that the world needed to forget and begin again. "
                                "He may still believe that. Or the Fading may have changed him. "
                                "I do not know which Valdris you will find.",
                        "next": "start",
                    },
                    "bye": {
                        "speaker": "Archmage Solen",
                        "text": "Careful does not save you from a collapsed ley network. "
                                "Five stones. Pale Coast, then the Isle. Then the Spire.",
                        "end": True,
                    },
                },
            },
        },
        {
            "conditions": [
                {"flag": "explored.abandoned_mine.floor3", "op": "==", "value": True},
                {"flag": "explored.sunken_crypt.floor2",   "op": "==", "value": True},
                {"flag": "explored.ruins_ashenmoor.floor2","op": "==", "value": True},
                {"flag": "quest.side_academy_research.state", "op": "!=", "value": -2},
            ],
            "tree": {
                "id": "solen_research_done",
                "loop": True,
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
                "loop": True,
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
                "loop": True,
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
                "loop": True,
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
                "loop": True,
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

    # ─────────────────────────────────────────────────────────
    #  WOODHAVEN NPCs
    # ─────────────────────────────────────────────────────────
    "innkeeper_jessa": [
        {
            "conditions": [{"flag": "boss_defeated.spiders_nest", "op": "==", "value": True}],
            "tree": {"id": "jessa_post_spiders", "loop": True, "nodes": {
                "start": {
                    "speaker": "Innkeeper Jessa",
                    "text": "The northwest trail is open again, they tell me. The web cave cleared.\n"
                            "I've had guests for the first time in three weeks. You did that, I expect.\n"
                            "Room's on me tonight.",
                    "choices": [
                        {"text": "Happy to help.", "next": None},
                        {"text": "The forest is still dangerous.", "next": "still_dangerous"},
                    ],
                },
                "still_dangerous": {
                    "speaker": "Innkeeper Jessa",
                    "text": "It always is. But dangerous and impassable are different things. "
                            "We can work with dangerous.",
                    "choices": [{"text": "Fair enough.", "next": None}],
                },
            }},
        },
        {
            "conditions": [],
            "tree": {"id": "jessa_default", "loop": True, "nodes": {
                "start": {
                    "speaker": "Innkeeper Jessa",
                    "text": "Welcome to the Canopy Rest. The northwest trail's been closed for weeks "
                            "— web cave, they say. So it's quiet. Too quiet for an inn.\n"
                            "Rest up. You'll want it.",
                    "choices": [
                        {"text": "What do you know about the area?", "next": "area"},
                        {"text": "We're looking for work.", "next": "work"},
                        {"text": "Just a room, thanks.", "next": None},
                    ],
                },
                "area": {
                    "speaker": "Innkeeper Jessa",
                    "text": "Thornwood paths go east and northwest. East connects to Ironhearth "
                            "eventually — hard road, dwarf country. Northwest is the web cave. "
                            "Nobody goes there now. The Rangers have stopped patrolling it entirely.",
                    "choices": [{"text": "Noted.", "next": None}],
                },
                "work": {
                    "speaker": "Innkeeper Jessa",
                    "text": "Talk to Guildmaster Oren at the guild hall. He posts contracts. "
                            "Or the Scout Hall — Ranger Cael tracks patrols and bounties. "
                            "Either way you'll find something.",
                    "choices": [{"text": "Thanks.", "next": None}],
                },
            }},
        },
    ],

    "trader_finn": [
        {
            "conditions": [],
            "tree": {"id": "finn_default", "loop": True, "nodes": {
                "start": {
                    "speaker": "Trader Finn",
                    "text": "Best ranger supplies this side of Ironhearth. Arrows, rope, trail "
                            "rations, the works. Supply lines to the city have been patchy "
                            "with the road conditions — but I've got what you need.",
                    "choices": [
                        {"text": "What's coming through from the east?", "next": "east"},
                        {"text": "Heard anything useful lately?", "next": "rumour"},
                        {"text": "Just browsing.", "next": None},
                    ],
                },
                "east": {
                    "speaker": "Trader Finn",
                    "text": "Less than usual. Dwarf merchants from Ironhearth have been cutting "
                            "trips short — something about the mine road being unsafe. "
                            "They won't say why, but they're nervous. That's not a good sign.",
                    "choices": [{"text": "Interesting.", "next": None}],
                },
                "rumour": {
                    "speaker": "Trader Finn",
                    "text": "Ranger brought in a dead Fading-touched wolf last week. "
                            "Twice the normal size, black around the eyes. "
                            "They've been getting bigger. Whatever's driving them, "
                            "it's not getting weaker.",
                    "choices": [{"text": "We'll keep that in mind.", "next": None}],
                },
            }},
        },
    ],

    "druid_rowan": [
        {
            "conditions": [{"flag": "boss_defeated.goblin_warren", "op": "==", "value": True}],
            "tree": {"id": "rowan_post_warren", "loop": True, "nodes": {
                "start": {
                    "speaker": "Druid Rowan",
                    "text": "The grove felt the change when the Warren cleared. Something "
                            "shifted in the Fading pressure — a brief easing, like a held "
                            "breath released.\nThe Hearthstones anchor that balance. "
                            "Each one you recover matters to every living thing in this forest.",
                    "choices": [
                        {"text": "Can the forest recover?", "next": "recover"},
                        {"text": "What can you tell us about the Fading?", "next": "fading"},
                        {"text": "Thank you.", "next": None},
                    ],
                },
                "recover": {
                    "speaker": "Druid Rowan",
                    "text": "With the wards restored? Yes. Slowly, but yes. "
                            "The corruption retreats when the anchor holds. "
                            "That's why the Hearthstones matter.",
                    "choices": [{"text": "We'll keep working.", "next": None}],
                },
                "fading": {
                    "speaker": "Druid Rowan",
                    "text": "The grove speaks to me in impressions, not words. "
                            "What I feel: something old and patient. Not malicious — "
                            "it doesn't hate. It simply consumes. Like rot, not fire.",
                    "choices": [{"text": "That's unsettling.", "next": None}],
                },
            }},
        },
        {
            "conditions": [],
            "tree": {"id": "rowan_default", "loop": True, "nodes": {
                "start": {
                    "speaker": "Druid Rowan",
                    "text": "This grove has stood for two hundred years. I've tended it "
                            "for thirty.\nThe Fading has been moving through the root network "
                            "for months now — I can feel it in the older trees. "
                            "Something needs to change or the forest won't survive another season.",
                    "choices": [
                        {"text": "Is there anything we can do?", "next": "help"},
                        {"text": "What does the Fading feel like?", "next": "feel"},
                        {"text": "We'll look into it.", "next": None},
                    ],
                },
                "help": {
                    "speaker": "Druid Rowan",
                    "text": "The Warden Order speaks of Hearthstones that once anchored "
                            "the boundary. If that's true, recovering them would help. "
                            "Beyond that — clear the corruption at its source. "
                            "The Goblin Warren east of Briarhollow is where I'd start.",
                    "choices": [{"text": "We're on it.", "next": None}],
                },
                "feel": {
                    "speaker": "Druid Rowan",
                    "text": "Like watching colour drain from something. "
                            "The grove is still alive, but it's less vivid than it was. "
                            "Less present. I find myself wondering if I'm imagining things — "
                            "then a branch falls that should have held for another century.",
                    "choices": [{"text": "We'll do what we can.", "next": None}],
                },
            }},
        },
    ],

    "barkeep_holt": [
        # After Act 1 complete
        {
            "conditions": [{"flag": "boss_defeated.abandoned_mine", "op": "==", "value": True}],
            "tree": {"id": "holt_act1_done", "loop": True, "nodes": {
                "start": {"speaker": "Barkeep Holt",
                    "text": "Three dungeons, three clearings. You're buying your own drinks "
                            "for the rest of the month if you come through here again. "
                            "What else can I get you? I'm hearing things from the east "
                            "you should probably know.",
                    "choices": [
                        {"text": "What are you hearing?", "next": "east_news"},
                        {"text": "Just the usual.", "next": None},
                    ]},
                "east_news": {"speaker": "Barkeep Holt",
                    "text": "A merchant came through two days ago from the Ashenmoor basin. "
                            "Said the ruins there are active — Fading energy, he called it. "
                            "Also said he saw something moving in the marshes south of "
                            "Crystalspire that was... wrong. His word. I believe him. "
                            "He's not the type to make things up.",
                    "choices": [{"text": "We'll investigate both.", "next": None}]},
            }},
        },
        # After goblin warren cleared
        {
            "conditions": [{"flag": "boss_defeated.goblin_warren", "op": "==", "value": True}],
            "tree": {"id": "holt_post_warren", "loop": True, "nodes": {
                "start": {"speaker": "Barkeep Holt",
                    "text": "The Warren's cleared? First round's on me. I've had three "
                            "merchant caravans cancel bookings because of the goblin raids. "
                            "That's three months of revenue, gone. "
                            "If you cleared that, you cleared my ledger too.",
                    "choices": [
                        {"text": "What's the talk in the tavern?", "next": "talk"},
                        {"text": "We'll drink to it.", "next": None},
                    ]},
                "talk": {"speaker": "Barkeep Holt",
                    "text": "Mostly about what you've been doing. Stories get bigger "
                            "every telling — by next week you'll have killed a dragon. "
                            "But the news that matters: something's wrong north of Woodhaven. "
                            "Hunters aren't coming back from the spider territory.",
                    "choices": [{"text": "We'll deal with the spiders next.", "next": None}]},
            }},
        },
        # Default
        {
            "conditions": [],
            "tree": {"id": "holt_default", "loop": True, "nodes": {
                "start": {"speaker": "Barkeep Holt",
                    "text": "What'll it be? The usual, something strong, or something "
                            "interesting? I keep a shelf of the interesting stuff "
                            "in the back — trade goods, rare finds, things travelers "
                            "bring in and don't take back out.",
                    "on_enter": [{"action": "meet_npc", "npc": "barkeep_holt"}],
                    "choices": [
                        {"text": "What's the news in town?", "next": "news"},
                        {"text": "Any work available?", "next": "work"},
                        {"text": "Just a drink.", "next": None},
                    ]},
                "news": {"speaker": "Barkeep Holt",
                    "text": "The Warren east of town has the militia worried. Goblin raids "
                            "on the southern road — three caravans hit this month. "
                            "And a hunter came in last night who said the spider cave "
                            "north of Woodhaven is expanding. Wouldn't say how he knew. "
                            "Walked very carefully.",
                    "choices": [{"text": "We'll look into both.", "next": None}]},
                "work": {"speaker": "Barkeep Holt",
                    "text": "Check the job board outside the guild. I post the overflow "
                            "here when it's full — which it usually is. "
                            "Everything pays in gold except the Fading-related ones. "
                            "Those pay in gratitude. Which is worth less, but there's more of it.",
                    "choices": [{"text": "Noted.", "next": None}]},
            }},
        },
    ],

    "smith_wren": [
        {
            "conditions": [],
            "tree": {"id": "wren_default", "loop": True, "nodes": {
                "start": {
                    "speaker": "Smith Wren",
                    "text": "Ranger's Forge. I make what rangers need — "
                            "arrowheads, light blades, field repairs.\n"
                            "Don't ask me for plate armour. Wrong forge, wrong smith.",
                    "choices": [
                        {"text": "What do you know about the area?", "next": "area"},
                        {"text": "Seen any unusual materials come through?", "next": "materials"},
                        {"text": "Just looking.", "next": None},
                    ],
                },
                "area": {
                    "speaker": "Smith Wren",
                    "text": "Forest work mostly. The Thornwood runs northeast from here "
                            "toward the old Warden patrol routes. Those routes haven't been "
                            "properly maintained in years. You can still follow them, "
                            "but don't expect the trail markers to be upright.",
                    "choices": [{"text": "Good to know.", "next": None}],
                },
                "materials": {
                    "speaker": "Smith Wren",
                    "text": "Ranger brought in chitin plates last week — from one of those "
                            "Fading-touched spiders. Harder than standard shell, "
                            "and there's something wrong with the colour. "
                            "I'm not working with it until I know more about what it does.",
                    "choices": [{"text": "Wise.", "next": None}],
                },
            }},
        },
    ],

    # ─────────────────────────────────────────────────────────
    #  IRONHEARTH NPCs
    # ─────────────────────────────────────────────────────────
    "innkeeper_bron": [
        {
            "conditions": [{"flag": "boss_defeated.abandoned_mine", "op": "==", "value": True}],
            "tree": {"id": "bron_post_mine", "loop": True, "nodes": {
                "start": {
                    "speaker": "Innkeeper Bron",
                    "text": "Word came down from the mine road. Korrath is gone. "
                            "Took long enough — that garrison's been a black mark on "
                            "Ironhearth's history for twenty years.\n"
                            "Drinks are on the house. And I mean it.",
                    "choices": [
                        {"text": "What happened to the garrison?", "next": "garrison"},
                        {"text": "Thank you.", "next": None},
                    ],
                },
                "garrison": {
                    "speaker": "Innkeeper Bron",
                    "text": "Warden garrison. Held the mine as an anchor point when the "
                            "old wards started failing. They held for months. "
                            "The Fading took them one by one. Korrath was the last.\n"
                            "Nobody went in after that. Nobody wanted to know.",
                    "choices": [{"text": "They held as long as they could.", "next": None}],
                },
            }},
        },
        {
            "conditions": [],
            "tree": {"id": "bron_default", "loop": True, "nodes": {
                "start": {
                    "speaker": "Innkeeper Bron",
                    "text": "Ironhearth. You made it in one piece — the road isn't kind "
                            "to outsiders.\nThe Forge City, they call it. Stone and fire "
                            "and the smell of hot metal. You'll get used to it.",
                    "choices": [
                        {"text": "Tell me about Ironhearth.", "next": "city"},
                        {"text": "What's the situation with the mine?", "next": "mine"},
                        {"text": "A room and quiet.", "next": None},
                    ],
                },
                "city": {
                    "speaker": "Innkeeper Bron",
                    "text": "Dwarven construction — you can tell from the stonework. "
                            "Three forge guilds, two trade houses, one temple that "
                            "everyone pretends is for the dwarven ancestors but is really "
                            "just where the forgemasters argue about ore grades.\n"
                            "Good city if you respect the work.",
                    "choices": [{"text": "Thanks for the overview.", "next": None}],
                },
                "mine": {
                    "speaker": "Innkeeper Bron",
                    "text": "The Abandoned Mine north of here. Nobody goes there. "
                            "Used to be a Warden garrison — they sealed it when things "
                            "went wrong. Whatever went wrong is still in there.\n"
                            "Foreman Drek at the mines office knows more than he tells.",
                    "choices": [{"text": "We'll talk to him.", "next": None}],
                },
            }},
        },
    ],

    "merchant_gilda": [
        {
            "conditions": [],
            "tree": {"id": "gilda_default", "loop": True, "nodes": {
                "start": {
                    "speaker": "Merchant Gilda",
                    "text": "Ironhearth Trading Post. We carry forge goods, "
                            "Dwarven metalwork, standard adventuring supplies.\n"
                            "Don't haggle. The prices are what they are.",
                    "choices": [
                        {"text": "What's moving well these days?", "next": "moving"},
                        {"text": "Heard anything from the eastern roads?", "next": "east"},
                        {"text": "Just looking.", "next": None},
                    ],
                },
                "moving": {
                    "speaker": "Merchant Gilda",
                    "text": "Torches and oil. Always torches and oil. "
                            "The mine road brings out the paranoid and the reckless in equal measure. "
                            "Both groups buy the same supplies.",
                    "choices": [{"text": "Practical.", "next": None}],
                },
                "east": {
                    "speaker": "Merchant Gilda",
                    "text": "Imperial patrols have been pushing further west than they should. "
                            "Asking about trade routes, ore shipments, population numbers. "
                            "The kind of questions you ask before you decide to take something.",
                    "choices": [{"text": "That sounds like more than trade interest.", "next": "imperial"},
                                {"text": "Noted.", "next": None}],
                },
                "imperial": {
                    "speaker": "Merchant Gilda",
                    "text": "It is. But I sell goods, not opinions. "
                            "The Guild Secretary would know more — Hald keeps track of who's "
                            "asking what in this city.",
                    "choices": [{"text": "We'll find him.", "next": None}],
                },
            }},
        },
    ],

    "priest_korvan": [
        {
            "conditions": [{"flag": "boss_defeated.abandoned_mine", "op": "==", "value": True}],
            "tree": {"id": "korvan_post_mine", "loop": True, "nodes": {
                "start": {
                    "speaker": "Priest Korvan",
                    "text": "The old prayers we speak here include the garrison. "
                            "Twenty-three names. We've spoken them every Forge-day "
                            "for fifteen years.\nKorrath is among them. "
                            "Whatever he was at the end — he was a Warden first. "
                            "Thank you for giving him peace.",
                    "choices": [
                        {"text": "He held his post as long as he could.", "next": None},
                        {"text": "He asked us to free him.", "next": "asked"},
                    ],
                },
                "asked": {
                    "speaker": "Priest Korvan",
                    "text": "That sounds like a Warden. They always had more dignity than the "
                            "rest of us managed.\nWe'll add the date to the memorial. "
                            "It deserves to be complete.",
                    "choices": [{"text": "It does.", "next": None}],
                },
            }},
        },
        {
            "conditions": [],
            "tree": {"id": "korvan_default", "loop": True, "nodes": {
                "start": {
                    "speaker": "Priest Korvan",
                    "text": "The Forge Shrine tends to all who work stone and fire. "
                            "Travellers are welcome, though we don't often see them.\n"
                            "This city runs on hard work and harder faith. "
                            "What can I do for you?",
                    "choices": [
                        {"text": "Tell me about the abandoned garrison.", "next": "garrison"},
                        {"text": "What do you know about the Wardens?", "next": "wardens"},
                        {"text": "Just passing through.", "next": None},
                    ],
                },
                "garrison": {
                    "speaker": "Priest Korvan",
                    "text": "Twenty-three names on the memorial stone outside. "
                            "The Warden garrison that held the mine anchor point "
                            "when the wards began failing. We speak their names every Forge-day.\n"
                            "The last survivor — Korrath — is still up there. "
                            "Changed. We don't send anyone to find out how.",
                    "choices": [{"text": "We'll go.", "next": None}],
                },
                "wardens": {
                    "speaker": "Priest Korvan",
                    "text": "The Order of Wardens kept the boundary between this world "
                            "and the Shadow Realm for centuries. When they failed, "
                            "we called it the Collapse. The Fading is the result.\n"
                            "The dwarves of Ironhearth remember it differently. "
                            "They call it the Breaking of the Deep Wards. "
                            "Same event. Different scars.",
                    "choices": [{"text": "Thank you.", "next": None}],
                },
            }},
        },
    ],

    "barkeep_magda": [
        # After Dragon's Tooth
        {
            "conditions": [{"flag": "boss_defeated.dragons_tooth", "op": "==", "value": True}],
            "tree": {"id": "magda_post_dragon", "loop": True, "nodes": {
                "start": {"speaker": "Barkeep Magda",
                    "text": "Dragon's Tooth. You came back from Dragon's Tooth. "
                            "I've served drinks to twelve people who said they were going there. "
                            "You're the first I've seen come back. "
                            "Whatever you want. No charge.",
                    "choices": [
                        {"text": "What do you know about the island?", "next": "island"},
                        {"text": "What's the news from the sea?", "next": "sea"},
                        {"text": "Just a drink.", "next": None},
                    ]},
                "island": {"speaker": "Barkeep Magda",
                    "text": "Old sailors say the Tooth has always been strange — before "
                            "the Fading, before the kingdom. The volcano doesn't behave "
                            "like volcanoes should. And whatever lives in the caldera "
                            "isn't anything the naturalists have catalogued.",
                    "choices": [{"text": "We found out what lives there.", "next": None}]},
                "sea": {"speaker": "Barkeep Magda",
                    "text": "The Fading is in the water now — the harbormasters have "
                            "been logging it for months. Tide patterns are wrong. "
                            "Fish schooling in places they never did. "
                            "The sea knows something is wrong too.",
                    "choices": [{"text": "We're trying to fix it.", "next": None}]},
            }},
        },
        # After reaching Saltmere
        {
            "conditions": [{"flag": "boss_defeated.abandoned_mine", "op": "==", "value": True}],
            "tree": {"id": "magda_act2", "loop": True, "nodes": {
                "start": {"speaker": "Barkeep Magda",
                    "text": "Word from the mainland — three dungeons cleared up north. "
                            "That'd be you lot, then. Saltmere doesn't get many Warden types. "
                            "No judgement. We don't get many law-abiding types either. "
                            "What can I get you?",
                    "choices": [
                        {"text": "What's Saltmere like?", "next": "saltmere"},
                        {"text": "Any news from the sea routes?", "next": "sea"},
                        {"text": "Just a drink.", "next": None},
                    ]},
                "saltmere": {"speaker": "Barkeep Magda",
                    "text": "No questions asked, reasonable prices, good security if "
                            "you pay for it. Half the port is Thieves' Guild territory — "
                            "the other half pretends it isn't. Guildmaster Sable runs "
                            "a tight operation. If you need passage east, talk to her.",
                    "choices": [{"text": "We need to reach Dragon's Tooth.", "next": None}]},
                "sea": {"speaker": "Barkeep Magda",
                    "text": "Fading in the water. The fishing boats are finding dead zones — "
                            "patches of ocean where nothing lives. Moving westward slowly. "
                            "The sailors are scared. Sailors don't scare easy.",
                    "choices": [{"text": "We're working on it.", "next": None}]},
            }},
        },
        # Default
        {
            "conditions": [],
            "tree": {"id": "magda_default", "loop": True, "nodes": {
                "start": {"speaker": "Barkeep Magda",
                    "text": "Welcome to the Salt Anchor. Drinks, food, rooms — "
                            "no questions asked about any of it. "
                            "That's the Saltmere way.",
                    "on_enter": [{"action": "meet_npc", "npc": "barkeep_magda"}],
                    "choices": [
                        {"text": "What's the news in Saltmere?", "next": "news"},
                        {"text": "Who should we talk to about ship passage?", "next": "passage"},
                        {"text": "Just a drink.", "next": None},
                    ]},
                "news": {"speaker": "Barkeep Magda",
                    "text": "Ships are spooked about the eastern islands. Dragon's Tooth, "
                            "mainly — something changed there. Three ships didn't make it "
                            "back this season. The Guildmaster controls passage now. "
                            "You need to go through her.",
                    "choices": [{"text": "Where do we find her?", "next": None}]},
                "passage": {"speaker": "Barkeep Magda",
                    "text": "Guildmaster Sable, at the Crossed Anchors. You can't miss it — "
                            "nicest building in a port full of bad buildings. "
                            "She'll negotiate. Bring something to negotiate with.",
                    "choices": [{"text": "Thanks.", "next": None}]},
            }},
        },
    ],

    "master_smith_thardin": [
        {
            "conditions": [],
            "tree": {"id": "thardin_default", "loop": True, "nodes": {
                "start": {
                    "speaker": "Master Smith Thardin",
                    "text": "The Grand Forge has stood for four hundred years. "
                            "Every blade worth carrying in this region started here.\n"
                            "State your business. I'm not a sightseer.",
                    "choices": [
                        {"text": "Tell me about Ironhearth's forges.", "next": "forges"},
                        {"text": "We're looking for information on the mine.", "next": "mine"},
                        {"text": "What do you make here?", "next": "makes"},
                        {"text": "Sorry to disturb you.", "next": None},
                    ],
                },
                "forges": {
                    "speaker": "Master Smith Thardin",
                    "text": "Three guilds. The Grand Forge handles weapons and heavy armour. "
                            "The Vein Hall does precision work — mechanisms, locks, fine instruments. "
                            "The Soot Guild takes everything else.\n"
                            "We cooperate on large contracts and compete on everything else. "
                            "That tension is why the work is good.",
                    "choices": [{"text": "Healthy competition.", "next": None}],
                },
                "mine": {
                    "speaker": "Master Smith Thardin",
                    "text": "The Abandoned Mine is the Grand Forge's oldest wound. "
                            "That ore fed our furnaces for two centuries. "
                            "When the garrison fell we lost half our supply lines.\n"
                            "If you're going up there — and I can see you're thinking it — "
                            "take fire. The things in there don't like fire.",
                    "choices": [{"text": "Fire. Noted.", "next": None}],
                },
                "makes": {
                    "speaker": "Master Smith Thardin",
                    "text": "Iron and steel, mainly. Some alloy work when the ore "
                            "from the eastern veins comes through — "
                            "they run cold, which makes for harder edges.\n"
                            "We've been experimenting with Fading-touched chitin. "
                            "Results are... mixed. The hardness is exceptional. "
                            "The material has a temperament.",
                    "choices": [{"text": "Interesting.", "next": None}],
                },
            }},
        },
    ],

    "armorer_ygrith": [
        {
            "conditions": [],
            "tree": {"id": "ygrith_default", "loop": True, "nodes": {
                "start": {
                    "speaker": "Armorer Ygrith",
                    "text": "Ironhearth Armory. "
                            "What you see is what's in stock. "
                            "Custom orders take three weeks and half up front.",
                    "choices": [
                        {"text": "Any advice for someone heading to the mine?", "next": "mine"},
                        {"text": "What sells here?", "next": "sells"},
                        {"text": "Just browsing.", "next": None},
                    ],
                },
                "mine": {
                    "speaker": "Armorer Ygrith",
                    "text": "Don't go light. Whatever's up there hits hard — "
                            "I've repaired enough gear from people who came back.\n"
                            "The ones who didn't come back were usually the ones "
                            "who thought their speed would save them. "
                            "Speed doesn't help you if you can't see it coming.",
                    "choices": [{"text": "Heavy armour it is.", "next": None}],
                },
                "sells": {
                    "speaker": "Armorer Ygrith",
                    "text": "Heavy plate to the garrison soldiers. "
                            "Chain and leather to the mine workers who still go north. "
                            "And lately a lot of repair work — "
                            "shields and breastplates coming back with marks "
                            "I don't recognise. Shadow damage, the priests call it. "
                            "I call it bad news.",
                    "choices": [{"text": "We'll keep that in mind.", "next": None}],
                },
            }},
        },
    ],

    "guildmaster_ironhearth": [
        {
            "conditions": [{"flag": "boss_defeated.abandoned_mine", "op": "==", "value": True}],
            "tree": {"id": "hald_post_mine", "loop": True, "nodes": {
                "start": {
                    "speaker": "Guild Secretary Hald",
                    "text": "The mine has been cleared — word came down an hour ago. "
                            "You're the ones responsible, I assume.\n"
                            "The Guild will log this. Formally. That matters more than "
                            "you might think when the historians write it up.",
                    "choices": [
                        {"text": "What happens now?", "next": "now"},
                        {"text": "We appreciate the acknowledgment.", "next": None},
                    ],
                },
                "now": {
                    "speaker": "Guild Secretary Hald",
                    "text": "The forgemasters will petition to reopen the northern veins. "
                            "The Warden Order — what remains of it — "
                            "will want to re-examine the anchor point. "
                            "And the city will breathe a little easier.\n"
                            "Your work here is done. The rest is administration.",
                    "choices": [{"text": "Good luck with that.", "next": None}],
                },
            }},
        },
        {
            "conditions": [],
            "tree": {"id": "hald_default", "loop": True, "nodes": {
                "start": {
                    "speaker": "Guild Secretary Hald",
                    "text": "Guild Hall. I manage trade records, guild contracts, "
                            "and visitor registrations for the city.\n"
                            "If you're conducting business in Ironhearth, "
                            "I should know about it.",
                    "choices": [
                        {"text": "We're investigating the abandoned mine.", "next": "mine"},
                        {"text": "What do you track here?", "next": "track"},
                        {"text": "Just passing through.", "next": None},
                    ],
                },
                "mine": {
                    "speaker": "Guild Secretary Hald",
                    "text": "Then you'll need to know: the mine road is officially "
                            "unsafe north of the second waystone. "
                            "Guild does not cover contracts in that zone.\n"
                            "Unofficially — the Imperial agents who came through "
                            "last month were asking about the same road. "
                            "Whatever they're looking for, they didn't find it. "
                            "That made them irritable.",
                    "choices": [{"text": "What were they after?", "next": "imperial"},
                                {"text": "Noted.", "next": None}],
                },
                "imperial": {
                    "speaker": "Guild Secretary Hald",
                    "text": "Ore manifests. Specifically, records of what was mined "
                            "from the deep veins before the garrison fell. "
                            "I gave them nothing — those records are sealed. "
                            "But they'll come back.",
                    "choices": [{"text": "Interesting.", "next": None}],
                },
                "track": {
                    "speaker": "Guild Secretary Hald",
                    "text": "Trade volume, contract disputes, visitor registrations, "
                            "and anything that looks like it might become a contract dispute "
                            "in the next six months. "
                            "Ironhearth runs on paper as much as on fire.",
                    "choices": [{"text": "Good to know.", "next": None}],
                },
            }},
        },
    ],

    "foreman_drek": [
        {
            "conditions": [{"flag": "boss_defeated.abandoned_mine", "op": "==", "value": True}],
            "tree": {"id": "drek_post_mine", "loop": True, "nodes": {
                "start": {
                    "speaker": "Foreman Drek",
                    "text": "They tell me it's cleared. "
                            "Twenty years I've kept this office, and not once did I "
                            "think I'd live to hear those words.\n"
                            "I've got three crews ready. We're going back in tomorrow. "
                            "Some of us have been waiting a long time for this.",
                    "choices": [
                        {"text": "What's the plan?", "next": "plan"},
                        {"text": "Take care in there.", "next": None},
                    ],
                },
                "plan": {
                    "speaker": "Foreman Drek",
                    "text": "Upper shafts first. See what's still sound. "
                            "The old gang-boards should hold — dwarven construction, "
                            "they build for the long term. "
                            "Lower veins we'll assess before we touch anything.\n"
                            "There's ore in those walls that's been waiting twenty years. "
                            "We can be patient another week.",
                    "choices": [{"text": "Good luck.", "next": None}],
                },
            }},
        },
        {
            "conditions": [],
            "tree": {"id": "drek_default", "loop": True, "nodes": {
                "start": {
                    "speaker": "Foreman Drek",
                    "text": "Mines Office. We manage the active shafts south and east.\n"
                            "The northern shafts have been sealed for twenty years. "
                            "I don't discuss what's up there. "
                            "Everyone who asked before you found out why we don't discuss it.",
                    "choices": [
                        {"text": "We're going to the Abandoned Mine.", "next": "going"},
                        {"text": "What happened to the garrison?", "next": "garrison"},
                        {"text": "We understand.", "next": None},
                    ],
                },
                "going": {
                    "speaker": "Foreman Drek",
                    "text": "Then I'll tell you what I tell everyone: "
                            "the mine key is the least of your problems. "
                            "Getting past the door is easy.\n"
                            "What Korrath became after the Fading took him — "
                            "that's what the key doesn't prepare you for. "
                            "He was the best of them. Now he's the worst of it.",
                    "choices": [{"text": "We'll be ready.", "next": None}],
                },
                "garrison": {
                    "speaker": "Foreman Drek",
                    "text": "They held the anchor point when the wards started failing. "
                            "Sent out progress reports for six months. "
                            "Then the reports stopped.\n"
                            "We sent one recovery team. They came back without the team. "
                            "After that we sealed the road and filed the paperwork "
                            "and I've been looking at that sealed door every morning for two decades.",
                    "choices": [{"text": "That's a long time to carry.", "next": None}],
                },
            }},
        },
    ],

    # ─────────────────────────────────────────────────────────
    #  GUILD TRAINERS — Greenwood, Sanctum, Crystalspire
    # ─────────────────────────────────────────────────────────
    "trainer_greenwood": [
        {
            "conditions": [],
            "tree": {"id": "trainer_greenwood_default", "loop": True, "nodes": {
                "start": {
                    "speaker": "Ranger Warden",
                    "text": "Greenwood Outpost. We train rangers and track the "
                            "Fading boundary across the western forest line.\n"
                            "We can sharpen your skills if you have the aptitude.",
                    "choices": [
                        {"text": "What training is available?", "next": "train"},
                        {"text": "What can you tell us about the western boundary?", "next": "boundary"},
                        {"text": "Just looking.", "next": None},
                    ],
                },
                "train": {
                    "speaker": "Ranger Warden",
                    "text": "Tracking, survival, ranged precision. "
                            "The outpost specialises in forest combat — "
                            "positioning, cover use, reading enemy movement before it happens.\n"
                            "If you want heavy combat training, Ironhearth is better suited. "
                            "We train you to not need it.",
                    "choices": [{"text": "We're interested.", "next": None}],
                },
                "boundary": {
                    "speaker": "Ranger Warden",
                    "text": "The Fading boundary shifts. We map it every season "
                            "and every season it's further west than last.\n"
                            "Three settlements have been abandoned in the last two years. "
                            "The people moved. The buildings stayed. "
                            "The buildings are still there — most of them.",
                    "choices": [{"text": "What happens to the buildings?", "next": "buildings"},
                                {"text": "We'll do what we can.", "next": None}],
                },
                "buildings": {
                    "speaker": "Ranger Warden",
                    "text": "They fade. Literally. Become less solid. "
                            "Then one morning you ride past and there's just a "
                            "foundation and an outline in the soil where the walls were.\n"
                            "It takes time. But not as much time as it used to.",
                    "choices": [{"text": "We'll find the Hearthstones.", "next": None}],
                },
            }},
        },
    ],

    "trainer_sanctum": [
        {
            "conditions": [],
            "tree": {"id": "trainer_sanctum_default", "loop": True, "nodes": {
                "start": {
                    "speaker": "Chapter Master Aldren",
                    "text": "The Sanctum chapter has maintained divine and healing "
                            "arts in this region for a century.\n"
                            "We train clerics, paladins, and those with the will "
                            "to face what the Fading sends.",
                    "choices": [
                        {"text": "What training do you offer?", "next": "train"},
                        {"text": "What does the Sanctum know about the Fading?", "next": "fading"},
                        {"text": "Just passing through.", "next": None},
                    ],
                },
                "train": {
                    "speaker": "Chapter Master Aldren",
                    "text": "Divine channelling, restoration, ward maintenance. "
                            "The practical arts — healing under fire, "
                            "turning shadow-touched enemies, keeping the party alive "
                            "when everything else has gone wrong.\n"
                            "We also train the harder skill: "
                            "knowing when to act and when to hold.",
                    "choices": [{"text": "That last one is harder than it sounds.", "next": None}],
                },
                "fading": {
                    "speaker": "Chapter Master Aldren",
                    "text": "The Fading is not evil. That distinction matters.\n"
                            "It is entropy given direction. It doesn't choose to consume — "
                            "it simply does, wherever the boundary wards fail to hold it.\n"
                            "The Hearthstones anchor those wards. Whoever Valdris is "
                            "and whatever his reasons — he understood that. "
                            "Which means he intended the collapse.",
                    "choices": [
                        {"text": "You think it was deliberate?", "next": "deliberate"},
                        {"text": "We'll stop him.", "next": None},
                    ],
                },
                "deliberate": {
                    "speaker": "Chapter Master Aldren",
                    "text": "The Warden Order doesn't fail by accident. "
                            "Not one this complete. Not one that leaves a single survivor "
                            "in the right position to work against the repairs.\n"
                            "We've been studying this for twenty years. "
                            "Find Valdris. Ask him yourself.",
                    "choices": [{"text": "We will.", "next": None}],
                },
            }},
        },
    ],

    "trainer_crystalspire": [
        {
            "conditions": [],
            "tree": {"id": "trainer_crystalspire_default", "loop": True, "nodes": {
                "start": {
                    "speaker": "Arcanist Veleth",
                    "text": "Crystalspire Arcane Guild. We research, we train, "
                            "and we argue about theory.\n"
                            "The arguing is mostly at mealtimes. The rest of the time "
                            "we're quite productive.",
                    "choices": [
                        {"text": "What training is available?", "next": "train"},
                        {"text": "What does the Guild know about the Fading?", "next": "fading"},
                        {"text": "Just passing through.", "next": None},
                    ],
                },
                "train": {
                    "speaker": "Arcanist Veleth",
                    "text": "Arcane disciplines — standard spell theory, "
                            "combat application, identification, wand attunement. "
                            "We also teach counter-magic and "
                            "recognition of Fading-touched corruption in spellwork.\n"
                            "That last course has become rather popular recently.",
                    "choices": [{"text": "I can imagine why.", "next": None}],
                },
                "fading": {
                    "speaker": "Arcanist Veleth",
                    "text": "The Fading interacts with arcane energy in three documented ways: "
                            "it destabilises sustained spell effects, "
                            "it amplifies shadow-element spells unpredictably, "
                            "and it corrupts spell anchors if left in contact long enough.\n"
                            "The third effect is what destroyed the old wards. "
                            "Someone patient and very skilled could have engineered it.",
                    "choices": [
                        {"text": "Valdris?", "next": "valdris"},
                        {"text": "How would you counter that?", "next": "counter"},
                    ],
                },
                "valdris": {
                    "speaker": "Arcanist Veleth",
                    "text": "The last Senior Warden. Yes.\n"
                            "He had the access and the knowledge. "
                            "Whether he had the motive — I leave that to philosophers. "
                            "My concern is understanding the mechanism so we can reverse it.",
                    "choices": [{"text": "The Hearthstones.", "next": None}],
                },
                "counter": {
                    "speaker": "Arcanist Veleth",
                    "text": "New anchors. Properly placed and shielded this time.\n"
                            "The Hearthstone fragments are exactly that — "
                            "they were designed as anchor points, not just relics. "
                            "Whoever created them understood the problem.",
                    "choices": [{"text": "We're finding them.", "next": None}],
                },
            }},
        },
    ],

        "innkeeper_thornhaven": [
        {
            "conditions": [{"flag": "boss_defeated.shadow_valdris", "op": "==", "value": True}],
            "tree": {
                "id": "innkeeper_post_valdris",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Innkeeper Brann",
                        "text": "You're the ones who went north. I heard what you did up there. I don't have words for it, so I'll settle for this: your coin is no good in this inn. Not now, not ever.",
                        "choices": [
                            {"text": "We appreciate it.", "next": None},
                        ],
                    },
                },
            },
        },
        {
            "conditions": [{"flag": "item.hearthstone.5", "op": "==", "value": True}],
            "tree": {
                "id": "innkeeper_all_stones",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Innkeeper Brann",
                        "text": "The word spreading through the taproom is that someone collected all five stones. If that's true — and it sounds mad, so it probably is — then Valdris' hold on the Fading is broken. Whatever he does next, he does it without that power. That changes things.",
                        "choices": [
                            {"text": "We still need to stop him.", "next": "stop"},
                            {"text": "Just drinks, please.", "next": None},
                        ],
                    },
                    "stop": {
                        "speaker": "Innkeeper Brann",
                        "text": "Then go. I'll keep a room warm. Something about this place has always drawn people who finish what they start. You look like that kind.",
                        "choices": [{"text": "We'll be back.", "next": None}],
                    },
                },
            },
        },
        {
            "conditions": [{"flag": "maren.left", "op": "==", "value": True}],
            "tree": {
                "id": "innkeeper_maren_left",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Innkeeper Brann",
                        "text": "That scholar woman came through last night. Left before dawn. Didn't pay, but I didn't ask — she had the look of someone who'd paid enough already. You're looking for her, I assume. North road, then the old garrison trail. After that the maps run out.",
                        "choices": [
                            {"text": "Thank you.", "next": None},
                        ],
                    },
                },
            },
        },
        {
            "conditions": [],
            "tree": {
                "id": "innkeeper_thornhaven_default",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Innkeeper Brann",
                        "text": "Capital's been busier than it should be. Refugees from the east — I've given rooms to twelve families this month alone. Good people. Scared. If you're heading east, be careful. The Fading doesn't announce itself.",
                        "choices": [
                            {"text": "What have you heard about the eastern situation?", "next": "east"},
                            {"text": "We'll be careful.", "next": None},
                        ],
                    },
                    "east": {
                        "speaker": "Innkeeper Brann",
                        "text": "Villages going quiet — no battle, no warning. Traders stop coming back. I had a regular, Adric, from Millstone. Three years coming through every month. Stopped last autumn. No note, no word. That happens once, it's bad luck. Happens to fifty villages, it's something else.",
                        "choices": [{"text": "We're looking into it.", "next": None}],
                    },
                },
            },
        },
    ],

    "refugee_elder": [
        {
            "conditions": [{"flag": "boss_defeated.shadow_valdris", "op": "==", "value": True}],
            "tree": {
                "id": "refugee_post_valdris",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Elder Somi",
                        "text": "My village was called Ashbury. Three hundred people. We heard a sound like the world forgetting itself — and then nothing. We ran. Forty-two of us made it here. You stopped the thing that took our home. I don't know if the land will come back. But the thing that took it is gone. That has to be enough.",
                        "choices": [
                            {"text": "We're sorry for what was lost.", "next": None},
                        ],
                    },
                },
            },
        },
        {
            "conditions": [{"flag": "item.hearthstone.3", "op": "==", "value": True}],
            "tree": {
                "id": "refugee_three_stones",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Elder Somi",
                        "text": "The guards say people like you have been weakening the Fading. I can feel it — the grey taste in the air is lighter than it was. My people can feel it too. They don't know why. I do. Whatever you're carrying north, carry it fast. Two more. Then end this.",
                        "choices": [
                            {"text": "How do you know about the stones?", "next": "know"},
                            {"text": "We intend to.", "next": None},
                        ],
                    },
                    "know": {
                        "speaker": "Elder Somi",
                        "text": "I was keeper of the village shrine — old Warden design, we thought it was just decoration. When the first stone was restored, the shrine lit up for three days. Ancient knowledge, waking up. The stones are anchors. Five of them hold the world in place. Valdris pulled them loose.",
                        "choices": [{"text": "He won't pull any more.", "next": None}],
                    },
                },
            },
        },
        {
            "conditions": [{"flag": "maren.left", "op": "==", "value": True}],
            "tree": {
                "id": "refugee_maren_left",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Elder Somi",
                        "text": "The Fading is weakening — I can feel the air changing. But the source is still there, somewhere north. I've seen the maps. Valdris' Spire. We all know about it. The question is whether someone goes there before he finishes what he started. Are you that someone?",
                        "choices": [
                            {"text": "Yes.", "next": "yes"},
                            {"text": "We're working on it.", "next": None},
                        ],
                    },
                    "yes": {
                        "speaker": "Elder Somi",
                        "text": "Then go. My people have nowhere else to be. We'll wait.",
                        "choices": [{"text": "We'll come back.", "next": None}],
                    },
                },
            },
        },
        {
            "conditions": [],
            "tree": {
                "id": "refugee_elder_default",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Elder Somi",
                        "text": "I led my village for twenty years. Buried my husband in that soil. Our shrine is a thousand years old — older than the city. The Fading took it in a night. We're camping in the Governor's courtyard. Forty-two of us from three hundred. If you're heading east, understand what you're walking toward.",
                        "choices": [
                            {"text": "We understand the stakes.", "next": None},
                            {"text": "What can you tell us about the Fading?", "next": "fading"},
                        ],
                    },
                    "fading": {
                        "speaker": "Elder Somi",
                        "text": "It doesn't destroy. It unmakes. Things touched by it don't leave ruins — they leave absence. A field where nothing grows, not even weeds. A village where even the foundations are gone. Whatever is causing it isn't just powerful. It's wrong in a way that goes deeper than power.",
                        "choices": [{"text": "We're going to stop it.", "next": None}],
                    },
                },
            },
        },
    ],

    "city_guard_thornhaven": [
        # After Shadow Valdris defeated
        {
            "conditions": [{"flag": "boss_defeated.shadow_valdris", "op": "==", "value": True}],
            "tree": {"id": "guard_endgame", "loop": True, "nodes": {
                "start": {"speaker": "City Guard",
                    "text": "Warden-Commander. The title's been empty for a generation. "
                            "The watch has orders to give you full passage — anywhere in "
                            "the city, any time. Governor Aldric's standing orders, "
                            "before the end. He was many things. At the last, he kept his word.",
                    "choices": [
                        {"text": "What's the city's state?", "next": "city"},
                        {"text": "Thank you.", "next": None},
                    ]},
                "city": {"speaker": "City Guard",
                    "text": "Stable. The Fading is retreating in the eastern districts. "
                            "Refugees are starting to return to their homes. "
                            "It'll be months before things are normal, but for the first "
                            "time since this started — I think normal is possible.",
                    "choices": [{"text": "That's enough.", "next": None}]},
            }},
        },
        # Thornhaven visited, post-Ashenmoor (Act 2)
        {
            "conditions": [
                {"flag": "town.thornhaven.visited", "op": "==", "value": True},
                {"flag": "boss_defeated.ruins_ashenmoor", "op": "==", "value": True},
            ],
            "tree": {"id": "guard_act2", "loop": True, "nodes": {
                "start": {"speaker": "City Guard",
                    "text": "The Ashenmoor report reached the watch. Second Hearthstone recovered. "
                            "I've been in the city watch for twelve years — I know when news "
                            "matters. That news matters. The Fading in the eastern quarter "
                            "is still spreading, but slower now.",
                    "choices": [
                        {"text": "Three more to find.", "next": "three"},
                        {"text": "What's the Governor's position?", "next": "governor"},
                    ]},
                "three": {"speaker": "City Guard",
                    "text": "Then do it. The city watch will hold the capital. "
                            "You hold whatever's out there. That's the division of labour.",
                    "choices": [{"text": "Agreed.", "next": None}]},
                "governor": {"speaker": "City Guard",
                    "text": "The Governor... officially supports the Warden effort. "
                            "Off the record, there are questions about what he knows "
                            "and when he knew it. Questions above my rank. Watch yourself.",
                    "choices": [{"text": "Noted.", "next": None}]},
            }},
        },
        # First visit to Thornhaven
        {
            "conditions": [{"flag": "town.thornhaven.visited", "op": "!=", "value": True}],
            "tree": {"id": "guard_first_visit", "loop": True, "nodes": {
                "start": {"speaker": "City Guard",
                    "text": "Keep your weapons sheathed in the capital. The watch doesn't "
                            "ask twice. You're registered with the Warden Order, so you "
                            "get some latitude. Don't abuse it.",
                    "on_enter": [{"action": "set_flag", "flag": "town.thornhaven.visited", "value": True}],
                    "choices": [
                        {"text": "What's the situation in the city?", "next": "situation"},
                        {"text": "What's happening in the Ashlands?", "next": "ashlands"},
                        {"text": "We understand.", "next": None},
                    ]},
                "situation": {"speaker": "City Guard",
                    "text": "Tense. The Fading is in the eastern districts now — the old "
                            "market quarter is half-abandoned. The Governor has the castle "
                            "locked down. Refugees are coming in from the countryside. "
                            "The city watch is stretched thin.",
                    "choices": [{"text": "We're here to help.", "next": None}]},
                "ashlands": {"speaker": "City Guard",
                    "text": "Bad. Worse than the official reports say. The eastern roads are "
                            "impassable — Fading-touched creatures on the main highway. "
                            "The Ashenmoor ruins are a focal point. Whatever the Fading "
                            "wants, it wants it there.",
                    "choices": [{"text": "We'll investigate.", "next": None}]},
            }},
        },
        # Default
        {
            "conditions": [],
            "tree": {"id": "guard_default", "loop": True, "nodes": {
                "start": {"speaker": "City Guard",
                    "text": "Keep your weapons sheathed in the capital. The city watch "
                            "doesn't ask twice. You're registered with the Warden Order, "
                            "so you get some latitude.",
                    "choices": [
                        {"text": "What's the situation in the city?", "next": "situation"},
                        {"text": "What's happening in the Ashlands?", "next": "ashlands"},
                        {"text": "We understand.", "next": None},
                    ]},
                "situation": {"speaker": "City Guard",
                    "text": "Tense. The Fading is in the eastern districts. The Governor "
                            "has the castle locked down. Refugees coming in daily.",
                    "choices": [{"text": "We'll help.", "next": None}]},
                "ashlands": {"speaker": "City Guard",
                    "text": "Bad. Worse than the official reports. The Ashenmoor ruins "
                            "are a focal point for Fading activity.",
                    "choices": [{"text": "We'll investigate.", "next": None}]},
            }},
        },
    ],

    "imperial_crier": [
        {
            "conditions": [{"flag": "boss_defeated.shadow_valdris", "op": "==", "value": True}],
            "tree": {
                "id": "crier_post_valdris",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Imperial Crier",
                        "text": "HEAR YE! By order of the Governor, the state of civic emergency in the eastern territories has been formally lifted. Citizens displaced by the Fading are invited to register for resettlement assistance at the Guild Hall. That's the official announcement. Off the record — well done.",
                        "choices": [
                            {"text": "What does 'resettlement assistance' mean?", "next": "resettle"},
                            {"text": "How are people taking the news?", "next": "news"},
                        ],
                    },
                    "resettle": {
                        "speaker": "Imperial Crier",
                        "text": "Food, tools, temporary shelter, and a land grant if there's anything left to grant. For most of them there isn't. The land came back but the villages didn't. They're rebuilding from nothing.",
                        "choices": [{"text": "It's a start.", "next": None}],
                    },
                    "news": {
                        "speaker": "Imperial Crier",
                        "text": "Quietly. People who've been through something like this don't celebrate loudly. They just... breathe differently. You can hear it in the market. It sounds less like people waiting for more bad news.",
                        "choices": [{"text": "That's enough.", "next": None}],
                    },
                },
            },
        },
        {
            "conditions": [{"flag": "maren.left", "op": "==", "value": True}],
            "tree": {
                "id": "crier_maren_left",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Imperial Crier",
                        "text": "HEAR YE! The Governor's office is offering a reward for information regarding — actually, I've been asked to stop reading that one. Sensitive operation. Carry on.",
                        "choices": [
                            {"text": "What was the full announcement?", "next": "full"},
                            {"text": "Understood.", "next": None},
                        ],
                    },
                    "full": {
                        "speaker": "Imperial Crier",
                        "text": "A missing scholar, headed north. Warden-affiliated. The Governor's office wants her found. I get the impression they want her found before whatever she's walking into finds her first.",
                        "choices": [{"text": "We're on it.", "next": None}],
                    },
                },
            },
        },
        {
            "conditions": [],
            "tree": {
                "id": "crier_default",
                "loop": True,
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
            "conditions": [{"flag": "boss_defeated.shadow_valdris", "op": "==", "value": True}],
            "tree": {
                "id": "noble_post_valdris",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Merchant Noble",
                        "text": "The eastern routes are open again. I've had three supply caravans move through Ashford Road without incident — first time in two years. I'm not sentimental about it. I am extremely pleased about it.",
                        "choices": [
                            {"text": "Commerce as usual, then.", "next": "commerce"},
                            {"text": "The people rebuilding those roads matter too.", "next": "people"},
                        ],
                    },
                    "commerce": {
                        "speaker": "Merchant Noble",
                        "text": "Commerce as usual is civilization as usual. Don't underestimate it. When the markets move, it means people believe tomorrow exists. That's not a small thing after two years of everyone acting like it might not.",
                        "choices": [{"text": "Fair point.", "next": None}],
                    },
                    "people": {
                        "speaker": "Merchant Noble",
                        "text": "Yes. I know. I'm funding three of the resettlement cooperatives, though I'd prefer you didn't spread that around — it complicates negotiations. I have a reputation for being difficult to maintain.",
                        "choices": [{"text": "Your secret is safe.", "next": None}],
                    },
                },
            },
        },
        {
            "conditions": [],
            "tree": {
                "id": "noble_default",
                "loop": True,
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
            "conditions": [{"flag": "boss_defeated.shadow_valdris", "op": "==", "value": True}],
            "tree": {
                "id": "refugee_post_valdris",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Refugee",
                        "text": "The sky looks different. You notice? The grey at the edges — it's pulling back. I've watched it every morning for two years. I know what it looked like. It looks different now.",
                        "choices": [
                            {"text": "The Fading has been stopped.", "next": "stopped"},
                            {"text": "We hope it holds.", "next": "hope"},
                        ],
                    },
                    "stopped": {
                        "speaker": "Refugee",
                        "text": "Stopped. Not fixed. Not undone. Ashford is still gone. My neighbours are still gone. But stopped — I'll take stopped. Stopped is something I didn't think I'd live to see.",
                        "choices": [{"text": "It won't be forgotten.", "next": "forget"}],
                    },
                    "hope": {
                        "speaker": "Refugee",
                        "text": "Mm. Good answer. Honest. I've had enough of people who say 'it's over' about things that aren't over. You did something real. What comes after is just — what comes after.",
                        "choices": [{"text": "That's the most we can promise.", "next": "forget"}],
                    },
                    "forget": {
                        "speaker": "Refugee",
                        "text": "I'm going back. To where Ashford was. I don't know if there's anything left. I'm going to find out.",
                        "choices": [{"text": "Safe travels.", "next": None}],
                    },
                },
            },
        },
        {
            "conditions": [],
            "tree": {
                "id": "refugee_default",
                "loop": True,
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
                "loop": True,
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
            "conditions": [{"flag": "maren.left", "op": "==", "value": True}],
            "tree": {
                "id": "aldric_maren_left",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Governor Aldric",
                        "text": "I heard the scholar left. Alone, at night, headed north. My people tried to follow — she was gone before they reached the gate. She knows something she hasn't shared with you, doesn't she.",
                        "choices": [
                            {"text": "She's trying to end this herself.", "next": "herself"},
                            {"text": "We're not sure what she knows.", "next": "unsure"},
                        ],
                    },
                    "herself": {
                        "speaker": "Governor Aldric",
                        "text": "Brave. Possibly foolish. Possibly both. If she has a plan, I hope it's better than mine was — which was 'wait and see.' I've been waiting for three years. The seeing hasn't improved.",
                        "choices": [{"text": "We're going after her.", "next": "going"}],
                    },
                    "unsure": {
                        "speaker": "Governor Aldric",
                        "text": "In my experience, when someone knows something and doesn't share it, one of two things is true: they don't trust you, or the knowledge would break you. Given what she's walked into — probably both.",
                        "choices": [{"text": "We're still going after her.", "next": "going"}],
                    },
                    "going": {
                        "speaker": "Governor Aldric",
                        "text": "Then go. Varek can give you Guild support to the border. After that you're on your own — I have no authority in the Ashlands. I'll hold the city. I'll be here when you come back.",
                        "choices": [{"text": "We'll be back.", "next": None}],
                    },
                },
            },
        },
        {
            "conditions": [],
            "tree": {
                "id": "aldric_default",
                "loop": True,
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
        # After 4 stones — final push, one stone left (Dragon's Tooth)
        {
            "conditions": [
                {"flag": "item.hearthstone.4", "op": "==", "value": True},
                {"flag": "item.hearthstone.5", "op": "not_exists"},
                {"flag": "boss_defeated.shadow_valdris", "op": "not_exists"},
            ],
            "tree": {
                "id": "varek_penultimate",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Guild Commander Varek",
                        "text": "Four stones. One left — the Dragon's Tooth, the volcanic island east of the coast. My operative confirmed the last stone is in the deepest chamber. The guardian there is unlike anything else. Prepare accordingly. After that, the Spire. You're close.",
                        "choices": [
                            {"text": "How do we reach Dragon's Tooth?", "next": "reach"},
                            {"text": "What do you know about the guardian?", "next": "guardian"},
                            {"text": "We're ready.", "next": None},
                        ],
                    },
                    "reach": {
                        "speaker": "Guild Commander Varek",
                        "text": "Eastport, then by ship. It's a half-day sail in good weather. The island is active — volcanic vents, unstable ground. The ruins predate the Warden order. Whatever's down there sealed itself in voluntarily.",
                        "choices": [{"text": "Understood.", "next": None}],
                    },
                    "guardian": {
                        "speaker": "Guild Commander Varek",
                        "text": "Old. Ancient, even by Warden standards. The reports call it Karreth — a name, not a title. It responds to something called a 'true name' — some kind of ancient binding. If you have that, the fight may be shorter. If not, expect it to be very long.",
                        "choices": [{"text": "We'll find a way.", "next": None}],
                    },
                },
            },
        },
        # After getting 3 stones — send to Pale Coast and Windswept Isle
        {
            "conditions": [
                {"flag": "item.hearthstone.3", "op": "==", "value": True},
                {"flag": "item.hearthstone.4", "op": "not_exists"},
            ],
            "tree": {
                "id": "varek_act3_stones",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Guild Commander Varek",
                        "text": "Three stones. I've had people watching — you've done what nobody else managed in a decade. There are two left. My operative found them: the Pale Coast Catacombs to the southwest, and the Windswept Isle ruins — accessible from the coast by ship. Get both. Then go north.",
                        "on_enter": [
                            {"action": "start_quest", "quest": "main_act3_spire"},
                            {"action": "start_quest", "quest": "main_pale_coast"},
                            {"action": "start_quest", "quest": "main_windswept_isle"},
                        ],
                        "choices": [
                            {"text": "What do you know about the Pale Coast guardian?", "next": "pale"},
                            {"text": "What's on the Windswept Isle?", "next": "isle"},
                            {"text": "Understood. We'll move.", "next": None},
                        ],
                    },
                    "pale": {
                        "speaker": "Guild Commander Varek",
                        "text": "A Warden. One of the original order — she sealed herself in decades ago to protect the stone. She may still be alive, or she may have become something else. My operative couldn't get close enough to tell. Approach with caution. If she's coherent, she may yield willingly.",
                        "choices": [{"text": "And the isle?", "next": "isle"}, {"text": "We'll handle it.", "next": None}],
                    },
                    "isle": {
                        "speaker": "Guild Commander Varek",
                        "text": "An elemental guardian. Pre-order — bound before Wardens existed. It doesn't negotiate and it doesn't retreat. It's also immune to the Fading entirely, which is the only reason the stone there survived. You'll need to fight it straight.",
                        "choices": [{"text": "Understood.", "next": None}],
                    },
                },
            },
        },
        # After getting all 5 stones — point to the Spire and Shadow Throne
        {
            "conditions": [
                {"flag": "item.hearthstone.5", "op": "==", "value": True},
                {"flag": "boss_defeated.shadow_valdris", "op": "not_exists"},
            ],
            "tree": {
                "id": "varek_send_north",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Guild Commander Varek",
                        "text": "All five. I won't pretend I expected that. Valdris' Spire is north of Thornhaven — past the last garrison, past the last road. Below the Spire is the Shadow Throne — that's where he actually lives. The Spire is the lock. The Throne is the man. Go.",
                        "choices": [
                            {"text": "What do we do when we find him?", "next": "choice"},
                            {"text": "We're ready.", "next": None},
                        ],
                    },
                    "choice": {
                        "speaker": "Guild Commander Varek",
                        "text": "That's between you and him and whatever Maren is planning. I've heard she's already inside. Whatever she wants — I'd think carefully before agreeing to it. She's her father's daughter in more ways than she admits.",
                        "choices": [{"text": "Noted.", "next": None}],
                    },
                },
            },
        },
        # Default
        {
            "conditions": [],
            "tree": {
                "id": "varek_default",
                "loop": True,
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
                        "on_enter": [
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
        # Act 3 — the Fading is critical, Sira is doing final calculations
        {
            "conditions": [
                {"flag": "maren.left", "op": "==", "value": True},
            ],
            "tree": {
                "id": "sira_act3",
                "nodes": {
                    "start": {
                        "speaker": "Court Mage Sira",
                        "text": "I have eight days of barrier integrity left on my projections. "
                                "Maybe ten if you're lucky. After that the outer wards collapse entirely "
                                "and the Fading accelerates beyond any ability to reverse it. "
                                "Whatever Maren is attempting in that Spire — she's running the same "
                                "numbers I am. She knows this too.",
                        "choices": [
                            {"text": "Is there anything you can do from here?", "next": "here"},
                            {"text": "What happens if she fails?", "next": "fail"},
                            {"text": "We're heading to the Spire now.", "next": "godspeed"},
                        ],
                    },
                    "here": {
                        "speaker": "Court Mage Sira",
                        "text": "I've been feeding power into the ley lines for three days without sleep. "
                                "It's like patching a crumbling dam with your hands. "
                                "I can buy you hours, not days. "
                                "Go. Be faster than the math.",
                        "end": True,
                    },
                    "fail": {
                        "speaker": "Court Mage Sira",
                        "text": "If she fails and all five stones are spent? "
                                "I think the Fading completes. Everything fades — "
                                "not destroyed, not dead. Unmade. As if it never was. "
                                "The records suggest it happened to three other worlds before this one.",
                        "on_enter": [{"action": "discover_lore", "lore": "fading_other_worlds"}],
                        "next": "godspeed",
                    },
                    "godspeed": {
                        "speaker": "Court Mage Sira",
                        "text": "For what it's worth — I've been running every calculation, "
                                "every model, every simulation I know. "
                                "Every version where the world survives has you at the center of it. "
                                "That's not prophecy. It's just the only variable that keeps changing. "
                                "Don't waste it.",
                        "end": True,
                    },
                },
            },
        },
        # After Maren reveal — Sira knows more and can be pressed
        {
            "conditions": [
                {"flag": "lore.maren_origin", "op": "==", "value": True},
                {"flag": "npc.court_mage_sira.debriefed", "op": "not_exists"},
            ],
            "tree": {
                "id": "sira_post_reveal",
                "nodes": {
                    "start": {
                        "speaker": "Court Mage Sira",
                        "text": "You know now. Good. I wasn't sure how long I could hold that. "
                                "Ask what you need to.",
                        "choices": [
                            {"text": "What do you know about Valdris's ritual?", "next": "ritual"},
                            {"text": "Can we trust Maren at all?", "next": "trust"},
                            {"text": "Why didn't you tell us sooner?", "next": "sooner"},
                        ],
                    },
                    "ritual": {
                        "speaker": "Court Mage Sira",
                        "text": "Valdris believed the Hearthstones could be used not just to restore "
                                "the wards — but to permanently seal the Shadow realm itself. "
                                "Not just hold it back. End the threat forever. "
                                "He was right. The mathematics work. "
                                "What he miscalculated was the cost.",
                        "next": "ritual2",
                    },
                    "ritual2": {
                        "speaker": "Court Mage Sira",
                        "text": "The ritual consumes whoever performs it. Not just magically — "
                                "erased. The stones use the performer's existence as fuel. "
                                "Valdris lost his nerve at the last moment and broke the ritual. "
                                "That breaking is what started the Fading.",
                        "on_enter": [{"action": "discover_lore", "lore": "valdris_ritual_cost"}],
                        "end": True,
                    },
                    "trust": {
                        "speaker": "Court Mage Sira",
                        "text": "Maren has spent her entire life trying to fix what her father broke. "
                                "She genuinely wants to save the world. "
                                "The question is whether she's decided to sacrifice you to do it, "
                                "or whether she hasn't made that choice yet. "
                                "Those are very different problems.",
                        "on_enter": [{"action": "set_flag", "flag": "npc.court_mage_sira.debriefed", "value": True}],
                        "end": True,
                    },
                    "sooner": {
                        "speaker": "Court Mage Sira",
                        "text": "Because I wasn't certain. And because Maren has done more to stop "
                                "the Fading than anyone else living. I didn't want to burn that "
                                "before I had to. "
                                "I'm telling you now because you're close enough to the end that "
                                "you need every piece of this.",
                        "on_enter": [{"action": "set_flag", "flag": "npc.court_mage_sira.debriefed", "value": True}],
                        "end": True,
                    },
                },
            },
        },
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
                "loop": True,
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Court Mage Sira",
                        "text": "The readings are worse today. I say that every day now, "
                                "and every day it's true.",
                        "choices": [
                            {"text": "What are you tracking?", "next": "tracking"},
                            {"text": "What does the Governor make of all this?", "next": "governor"},
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
                    "governor": {
                        "speaker": "Court Mage Sira",
                        "text": "He understands the numbers. That's more than most. "
                                "What he can't accept is that there is no military solution to this. "
                                "You cannot march soldiers against entropy. "
                                "He's still looking for something to fight.",
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

    # ── ACT 3 BOSS & STORY DIALOGUES ────────────────────────

    # Pale Sentinel — fires before boss fight on floor 4
    "pale_sentinel": [
        # If party has 3+ Hearthstones — she yields, no fight needed
        {
            "conditions": [
                {"flag": "item.hearthstone.3", "op": "==", "value": True},
            ],
            "tree": {
                "id": "sentinel_yields",
                "nodes": {
                    "start": {
                        "speaker": "The Pale Sentinel",
                        "text": "You carry three stones already. Then you are the ones I was told to wait for.\nI have kept this one safe for forty-three years. I am tired.\nTake it. Do not waste what I gave up to protect it.",
                        "on_enter": [
                            {"action": "set_flag", "flag": "boss_defeated.pale_coast", "value": True},
                            {"action": "set_flag", "flag": "sentinel.yielded", "value": True},
                        ],
                        "choices": [
                            {"text": "You'll be free now.", "next": "free"},
                            {"text": "Thank you, Warden.", "next": "warden"},
                        ],
                    },
                    "free": {
                        "speaker": "The Pale Sentinel",
                        "text": "Free. I no longer know what that means.\nI have been the lock for so long I forgot I was ever anything else.\nPerhaps that is the answer to a question I stopped asking.\nGo. The world needs you more than this cave needs me.",
                        "choices": [{"text": "Farewell.", "next": None}],
                    },
                    "warden": {
                        "speaker": "The Pale Sentinel",
                        "text": "The order is gone. I know that. I kept the name because the name still meant something — to me, if to no one else.\nYou carry the order's purpose now. Whether you want it or not.\nDo better than we did.",
                        "choices": [{"text": "We'll try.", "next": None}],
                    },
                },
            },
        },
        # Default — must fight
        {
            "conditions": [],
            "tree": {
                "id": "sentinel_fight",
                "nodes": {
                    "start": {
                        "speaker": "The Pale Sentinel",
                        "text": "You are not the ones I was told to wait for.\nThe order said: three stones and a clear conscience.\nYou do not carry three stones. Therefore I cannot know what you carry in the other.\nLeave. Or prove you are worth the cost of what I guard.",
                        "choices": [
                            {"text": "We need that stone.", "next": "need"},
                            {"text": "We'll leave.", "next": "leave"},
                        ],
                    },
                    "need": {
                        "speaker": "The Pale Sentinel",
                        "text": "Everyone who has come here needed it. That is not sufficient.\nI am not blocking your path out of malice. I am a lock.\nIf you want to know why, find the other stones first. Then come back. I will still be here.\nI have always been here.",
                        "choices": [
                            {"text": "[FIGHT] We don't have time.", "next": None},
                            {"text": "We understand. We'll return.", "next": None},
                        ],
                    },
                    "leave": {
                        "speaker": "The Pale Sentinel",
                        "text": "That is the first wise thing anyone has said to me in twenty years.\nLeave. Come back when you are ready.",
                        "choices": [{"text": "We'll return.", "next": None}],
                    },
                },
            },
        },
    ],

    # Isle Keeper — mindless elemental guardian, no negotiation possible
    # Fires before boss fight on windswept_isle floor 3
    "isle_keeper": [
        {
            "conditions": [],
            "tree": {
                "id": "isle_keeper_encounter",
                "nodes": {
                    "start": {
                        "speaker": "The Last Keeper",
                        "text": "...\n\n[The Keeper does not speak. It does not see you as a person. It sees something approaching the stone it has protected for centuries.]\n[Its purpose and its awareness have collapsed into a single point. There is nothing left to reason with.]\n[It begins to move.]",
                        "on_enter": [{"action": "set_flag", "flag": "isle_keeper.encountered", "value": True}],
                        "choices": [
                            {"text": "[FIGHT] Stand your ground.", "next": None},
                        ],
                    },
                },
            },
        },
    ],

    # Shadow Valdris — post-phase-2 dialogue (Valdris the Broken)
    # The man beneath the shadow speaks. This sets the ending path.
    "shadow_valdris": [
        # If party chose the redemption path before the fight
        {
            "conditions": [
                {"flag": "ending.path", "op": "==", "value": "redemption"},
            ],
            "tree": {
                "id": "valdris_redemption",
                "nodes": {
                    "start": {
                        "speaker": "Valdris the Broken",
                        "text": "The avatar is gone.\nI can... think again. It has been a long time since I could think.\nYou came with the stones. All five. My daughter calculated it — the full set, the original anchor structure...\nIt might actually work. My first theory. Before everything else.\nI never thought anyone would be standing here with all of them.",
                        "choices": [
                            {"text": "It can work. But you have to choose it.", "next": "choose"},
                            {"text": "You caused Ashenmoor.", "next": "ashenmoor"},
                        ],
                    },
                    "ashenmoor": {
                        "speaker": "Valdris the Broken",
                        "text": "Yes.\nTwo hundred and fourteen people. I know the number. I have known it every day for twelve years.\nI cannot fix that. I can only — possibly — make certain that what they died to prevent, never happens.\nThat does not make it right. It makes it the only direction left.",
                        "choices": [{"text": "Then choose it. Now.", "next": "choose"}],
                    },
                    "choose": {
                        "speaker": "Valdris the Broken",
                        "text": "I choose it.\nI, Valdris — Warden, Oathbreaker, Father — choose to give the network what it was always meant to receive willingly.\nNot sacrifice. Not blood taken without consent.\nA gift. Freely given.\nTell Maren... tell her the first theory was right.",
                        "on_enter": [
                            {"action": "set_flag", "flag": "choice.ending", "value": "redemption"},
                            {"action": "set_flag", "flag": "valdris.redeemed", "value": True},
                            {"action": "complete_quest", "quest": "main_act3_finale"},
                        ],
                        "choices": [{"text": "We will.", "next": None}],
                    },
                },
            },
        },
        # Default — heroic or sacrifice path
        {
            "conditions": [],
            "tree": {
                "id": "valdris_end",
                "nodes": {
                    "start": {
                        "speaker": "Valdris the Broken",
                        "text": "The shadow is gone. I can see your faces.\nI haven't seen anything clearly in... years.\nAm I dying? I think I might be dying.\nI want to ask you something, before I do.",
                        "choices": [
                            {"text": "Ask.", "next": "ask"},
                            {"text": "You don't have much time.", "next": "time"},
                        ],
                    },
                    "ask": {
                        "speaker": "Valdris the Broken",
                        "text": "Is it enough? The work. The stones. What you've done.\nIs the world going to hold?",
                        "choices": [
                            {"text": "Yes. The wards are restored.", "next": "restored"},
                            {"text": "It'll hold long enough.", "next": "long_enough"},
                        ],
                    },
                    "time": {
                        "speaker": "Valdris the Broken",
                        "text": "Then I'll be quick.\nI spent thirty years trying to save the world without paying the cost the world required.\nDid I waste all of it?",
                        "choices": [
                            {"text": "No. The stones are back. The wards hold.", "next": "restored"},
                            {"text": "You saved Maren. She finished it.", "next": "maren_finish"},
                        ],
                    },
                    "maren_finish": {
                        "speaker": "Valdris the Broken",
                        "text": "I taught her everything she used against me.\nThat seems... appropriate.\nShe's better than I was. Tell her I said so.",
                        "on_enter": [{"action": "set_flag", "flag": "valdris.last_words", "value": "maren"}],
                        "choices": [{"text": "We'll tell her.", "next": "end"}],
                    },
                    "restored": {
                        "speaker": "Valdris the Broken",
                        "text": "Good.\nThe network will hold without blood now. No more Wardens dying slowly in sealed rooms.\nSomebody finally got it right.\nI'm glad it wasn't me. I would have — found a way to ruin it.",
                        "choices": [{"text": "Rest now.", "next": "end"}],
                    },
                    "long_enough": {
                        "speaker": "Valdris the Broken",
                        "text": "Long enough is all any of us ever managed.\nAll right.\nThat'll do.",
                        "choices": [{"text": "Rest now.", "next": "end"}],
                    },
                    "end": {
                        "speaker": "Valdris the Broken",
                        "text": "...\n\n[Valdris exhales once. He does not speak again.\nIn the throne chamber, the shadow lifts. The Fading has no anchor here anymore.\nThe stones in your possession hum briefly, then go quiet.\nThe network holds.]",
                        "on_enter": [
                            {"action": "set_flag", "flag": "choice.ending", "value": "heroic"},
                            {"action": "complete_quest", "quest": "main_act3_finale"},
                        ],
                        "choices": [{"text": "Leave the Throne.", "next": None}],
                    },
                },
            },
        },
    ],

    # Valdris pre-fight — fires on Shadow Throne floor 7 (Maren is present)
    "valdris_pre_fight": [
        {
            "conditions": [],
            "tree": {
                "id": "valdris_final_scene",
                "nodes": {
                    "start": {
                        "speaker": "Maren",
                        "text": "You came.\nI hoped you would. I also hoped you wouldn't. Both things are true.\nHe's through those doors. What remains of him.\nI need to explain something before you go in, and I need you to actually hear it.",
                        "choices": [
                            {"text": "We're listening.", "next": "maren_explains"},
                            {"text": "We already know about the ritual.", "next": "know_already"},
                        ],
                    },
                    "maren_explains": {
                        "speaker": "Maren",
                        "text": "The ward network requires living sacrifice to maintain. Small amounts, continuously, from every Warden who serves. My father discovered it. He couldn't live with it.\nHis solution caused Ashenmoor. I know. I have spent my entire life knowing.\nMy solution is different. It requires willing sacrifice — once, completely. It makes the network self-sustaining afterward. Forever.\nIt requires Warden blood. It requires all of you.",
                        "choices": [
                            {"text": "You're asking us to die.", "next": "die"},
                            {"text": "There has to be another way.", "next": "another_way"},
                            {"text": "What about Valdris?", "next": "valdris_question"},
                        ],
                    },
                    "know_already": {
                        "speaker": "Maren",
                        "text": "Then you know what I'm going to ask. And you know I'm not asking it lightly.\nI've been carrying this since I was nineteen years old. I know what it costs. I know it isn't fair.\nBut I don't know another way that works.",
                        "choices": [
                            {"text": "What about Valdris?", "next": "valdris_question"},
                            {"text": "And if we refuse?", "next": "refuse"},
                        ],
                    },
                    "die": {
                        "speaker": "Maren",
                        "text": "Yes.\nI'm not going to dress it differently. You would die, and the world would live, and in a hundred years no one would know your names except possibly the Archmage, who would write a paper about it.\nI understand if the answer is no.",
                        "choices": [
                            {"text": "[REFUSE] No. There's another way.", "next": "refuse"},
                            {"text": "[AGREE] Tell us what we have to do.", "next": "agree"},
                            {"text": "What about Valdris?", "next": "valdris_question"},
                        ],
                    },
                    "another_way": {
                        "speaker": "Maren",
                        "text": "I looked. For fifteen years I looked.\nIf there's a path I missed, I haven't found it. But you have the Hearthstones. All five.\nMy father's original theory — the one before Ashenmoor — said a complete set might allow redemption of the anchor structure rather than sacrifice. He never tested it. He ran out of time.\nI don't know if it works.",
                        "on_enter": [{"action": "set_flag", "flag": "maren.offered_redemption", "value": True}],
                        "choices": [
                            {"text": "[REDEMPTION PATH] We try his way.", "next": "redemption"},
                            {"text": "[REFUSE] We destroy Valdris and stop this.", "next": "refuse"},
                            {"text": "[AGREE] If it doesn't work, we do your ritual.", "next": "agree"},
                        ],
                    },
                    "redemption": {
                        "speaker": "Maren",
                        "text": "Then we need him. Not destroyed — freed. The shadow that wears his face has to go, but the man underneath has to choose to let it go.\nThat is harder than killing him. Possibly impossible.\nBut if you have all five stones and he's willing — it might close everything. Permanently. No sacrifice. No broken ritual.\nI'll be with you.",
                        "on_enter": [{"action": "set_flag", "flag": "ending.path", "value": "redemption"}],
                        "choices": [{"text": "Then let's go.", "next": None}],
                    },
                    "refuse": {
                        "speaker": "Maren",
                        "text": "I expected that answer.\nDestroy him. Seal what you can with the stones. The network will hold for a generation — maybe two.\nAfter that — someone else's problem. The same problem it's always been.\nI won't stop you. I'm not sure I even disagree.",
                        "on_enter": [{"action": "set_flag", "flag": "ending.path", "value": "heroic"}],
                        "choices": [{"text": "Stand back.", "next": None}],
                    },
                    "agree": {
                        "speaker": "Maren",
                        "text": "You're certain?\nI need you to be certain. I've been certain for fifteen years and I still have nightmares about asking someone this.\nIf you're certain — then after Valdris, we perform the ritual together. All of us. I'll explain every step.\nThank you. I mean that. Even if I hate that I have to.",
                        "on_enter": [{"action": "set_flag", "flag": "ending.path", "value": "sacrifice"}],
                        "choices": [{"text": "Let's end this.", "next": None}],
                    },
                    "refuse": {
                        "speaker": "Maren",
                        "text": "I expected that answer.\nDestroy him. Seal what you can with the stones. The network will hold for a generation — maybe two.\nAfter that — someone else's problem.\nI won't stop you.",
                        "on_enter": [{"action": "set_flag", "flag": "ending.path", "value": "heroic"}],
                        "choices": [{"text": "Stand back.", "next": None}],
                    },
                    "valdris_question": {
                        "speaker": "Maren",
                        "text": "He's in there. What's left of him.\nThe shadow consumed most of what he was. But there's still a man inside it — exhausted, guilty, probably relieved someone finally got here.\nKilling the shadow frees him. What the freed man chooses to do is the question I've been afraid to answer for twenty years.",
                        "choices": [
                            {"text": "What does he want?", "next": "valdris_want"},
                            {"text": "And the ritual?", "next": "maren_explains"},
                        ],
                    },
                    "valdris_want": {
                        "speaker": "Maren",
                        "text": "To be forgiven. For Ashenmoor. For me. For all of it.\nI don't know if I can give him that. I've been working on it.\nBut what he wants, ultimately, is the same thing we want — for the Fading to stop. He just broke the world trying to get there.\nSo did I, almost.",
                        "choices": [
                            {"text": "Let's go face him.", "next": None},
                        ],
                    },
                },
            },
        },
    ],

    "crystalspire_priest": [
        # Act 3 — all stones found, the Spire is the destination
        {
            "conditions": [
                {"flag": "item.hearthstone.5", "op": "==", "value": True},
            ],
            "tree": {
                "id": "priest_act3",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Priest Sael",
                        "text": "Five Hearthstones. I felt the last one settle into the network "
                                "from here — like a chord completing.\n"
                                "The Shrine has been quiet for four hundred years. "
                                "For the first time since I began studying the wards, "
                                "I believe they can be healed.\n"
                                "Valdris' Spire is to the north-east, beyond the Holdfast. "
                                "Whatever you find there — the network is ready. Go.",
                        "choices": [
                            {"text": "Will the wards hold once we restore them?", "next": "wards_hold"},
                            {"text": "What do you know about the Spire?",         "next": "the_spire"},
                            {"text": "We go.",                                    "next": None},
                        ],
                    },
                    "wards_hold": {
                        "speaker": "Priest Sael",
                        "text": "The original architecture was sound. "
                                "The Fading didn't break the system — it exploited a wound "
                                "that was already there.\n"
                                "Seal that wound and the wards will hold. "
                                "Not forever. Nothing holds forever. "
                                "But long enough for whatever comes next.",
                        "end": True,
                    },
                    "the_spire": {
                        "speaker": "Priest Sael",
                        "text": "It was the anchor point for the whole network — "
                                "built before the Order, before the towns, before most of what "
                                "you'd recognize as civilization in this region.\n"
                                "Valdris made it his seat because he understood what it was. "
                                "He understood everything about the wards. "
                                "That's what makes him so dangerous.",
                        "end": True,
                    },
                },
            },
        },
        # Post-HS2 — Sunken Crypt cleared, heading for Dragon's Tooth
        {
            "conditions": [
                {"flag": "item.hearthstone.2", "op": "==", "value": True},
                {"flag": "item.hearthstone.3", "op": "!=", "value": True},
            ],
            "tree": {
                "id": "priest_post_crypt",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Priest Sael",
                        "text": "Two stones recovered. The Shrine is more... present than it was. "
                                "The resonance is building.\n"
                                "Dragon's Tooth next — the fragment there is the oldest. "
                                "The Shrine's records call it a 'first anchor.' "
                                "Whatever that means, it predates everything the Order built.\n"
                                "Sea passage from Saltmere is your route south.",
                        "choices": [
                            {"text": "What do the Shrine's records say about Dragon's Tooth?", "next": "records"},
                            {"text": "We sail south.",                                         "next": None},
                        ],
                    },
                    "records": {
                        "speaker": "Priest Sael",
                        "text": "Very little. The Shrine's records begin with the Order's founding "
                                "— anything before that is inference and fragment.\n"
                                "What I can tell you: the first anchor was placed by something "
                                "that wasn't human and wasn't a Warden. "
                                "Whatever it was, it understood the Fading before anyone had a name for it.",
                        "choices": [{"text": "We'll find out.", "next": None}],
                    },
                },
            },
        },
        # Post-HS1 — Mine cleared, Ashenmoor/Crypt ahead
        {
            "conditions": [
                {"flag": "item.hearthstone.1", "op": "==", "value": True},
                {"flag": "item.hearthstone.2", "op": "!=", "value": True},
            ],
            "tree": {
                "id": "priest_post_mine",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Priest Sael",
                        "text": "The first fragment. I can feel it from here — "
                                "a faint resonance through the Shrine's foundation stones.\n"
                                "Four remain. The Ruins of Ashenmoor first — "
                                "there's a ward-sealed crypt beneath the Pale Coast that "
                                "cannot be opened without a Crypt Amulet from those ruins. "
                                "Clear Ashenmoor before you attempt the Crypt.\n"
                                "The Shrine will be watching.",
                        "choices": [
                            {"text": "What can you tell us about the Crypt?",    "next": "about_crypt"},
                            {"text": "What is the Shrine of Arcane Truth?",      "next": "about_shrine"},
                            {"text": "We understand. Farewell.",                  "next": None},
                        ],
                    },
                    "about_crypt": {
                        "speaker": "Priest Sael",
                        "text": "A drowned Warden stronghold. The garrison sealed the "
                                "Hearthstone fragment and stayed with it when the Fading came.\n"
                                "The ward on the entrance is old Order work — "
                                "almost impossible to break by force. The Crypt Amulet "
                                "is the correct key. Without it, the entrance will not open.",
                        "choices": [{"text": "Understood. Ashenmoor first.", "next": None}],
                    },
                    "about_shrine": {
                        "speaker": "Priest Sael",
                        "text": "We study the ward network as a sacred object — "
                                "not in the way the Wardens did, as infrastructure, "
                                "or as the Order did, as duty.\n"
                                "We study it the way you study a cathedral. "
                                "As something built by minds that understood things "
                                "we are still learning to ask questions about.",
                        "choices": [{"text": "Farewell.", "next": None}],
                    },
                },
            },
        },
        # Default — before any hearthstones
        {
            "conditions": [],
            "tree": {
                "id": "priest_default",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Priest Sael",
                        "text": "The Shrine of Arcane Truth has studied the ward network "
                                "for three hundred years.\n"
                                "We are not the Warden Order — we don't maintain the wards, "
                                "we don't hold rank, we don't take oaths. "
                                "We simply try to understand what the wards are and what "
                                "built them.\n"
                                "In three hundred years, we've answered perhaps a third "
                                "of those questions. The Fading is answering some of the rest "
                                "in ways we would have preferred not to learn.",
                        "choices": [
                            {"text": "What do you know about the Hearthstones?", "next": "hearthstones"},
                            {"text": "What is causing the Fading?",              "next": "fading"},
                            {"text": "Farewell.",                                "next": None},
                        ],
                    },
                    "hearthstones": {
                        "speaker": "Priest Sael",
                        "text": "Anchor points for the ward network. "
                                "Five of them, distributed across the region. "
                                "The network functions only when all five are active — "
                                "like a circuit.\n"
                                "One failed. We don't know why. "
                                "The Fading is what happens when the circuit is broken.",
                        "choices": [{"text": "Farewell.", "next": None}],
                    },
                    "fading": {
                        "speaker": "Priest Sael",
                        "text": "The honest answer: we don't know. "
                                "The Shrine's best theory is that something interfered "
                                "with one of the Hearthstone anchors deliberately.\n"
                                "The ward network doesn't fail randomly. "
                                "It was designed not to. "
                                "Something with knowledge of the system caused this.",
                        "choices": [{"text": "Farewell.", "next": None}],
                    },
                },
            },
        },
    ],
}

# Merge into main NPC_DIALOGUES
NPC_DIALOGUES.update(_NEW_DIALOGUES)

# ══════════════════════════════════════════════════════════════
#  AMBIENT NPC DIALOGUES — Generic flavour NPCs in towns
# ══════════════════════════════════════════════════════════════

_AMBIENT_DIALOGUES = {
    "ambient_townsfolk": [
        {
            "conditions": [],
            "tree": {
                "id": "ambient_townsfolk_default",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Townsperson",
                        "text": "Troubling times. But life goes on, doesn't it? It has to.",
                        "choices": [
                            {"text": "Have you noticed anything strange lately?", "next": "strange"},
                            {"text": "Indeed. Take care.", "next": "bye"},
                        ],
                    },
                    "strange": {
                        "speaker": "Townsperson",
                        "text": "Strange? Aye. The nights are darker than they should be. "
                                "Animals acting up. Old folks say it's like the last time the "
                                "world went quiet before something big happened. "
                                "I try not to think about it.",
                        "next": "bye",
                    },
                    "bye": {
                        "speaker": "Townsperson",
                        "text": "Watch yourself out there.",
                        "end": True,
                    },
                },
            },
        },
    ],
    "ambient_guard": [
        {
            "conditions": [],
            "tree": {
                "id": "ambient_guard_default",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Guard",
                        "text": "Move along, please. Nothing to see here. "
                                "If you're looking for trouble, look elsewhere. "
                                "If you need directions, I can help with that.",
                        "choices": [
                            {"text": "What should I know about this town?", "next": "town_info"},
                            {"text": "Anything unusual happening?",          "next": "unusual"},
                            {"text": "Just passing through.",               "next": "bye"},
                        ],
                    },
                    "town_info": {
                        "speaker": "Guard",
                        "text": "Guild's always looking for capable folk. Inn's the safest "
                                "place to sleep if you're new. Don't cause trouble and "
                                "we won't have a problem.",
                        "next": "start",
                    },
                    "unusual": {
                        "speaker": "Guard",
                        "text": "Define unusual. Everything's unusual these days. "
                                "I keep my head down and my post. That's all I can do.",
                        "next": "bye",
                    },
                    "bye": {
                        "speaker": "Guard",
                        "text": "On your way.",
                        "end": True,
                    },
                },
            },
        },
    ],
    "ambient_merchant": [
        {
            "conditions": [],
            "tree": {
                "id": "ambient_merchant_default",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Merchant",
                        "text": "Finest goods this side of the capital, if you're buying. "
                                "If you're just browsing, try not to touch anything.",
                        "choices": [
                            {"text": "How's business?",          "next": "business"},
                            {"text": "Heard any news on the road?", "next": "news"},
                            {"text": "Just looking.",             "next": "bye"},
                        ],
                    },
                    "business": {
                        "speaker": "Merchant",
                        "text": "Slow. The roads aren't safe like they were. Bandits, "
                                "strange creatures, caravans going missing. "
                                "Hard to turn a profit when half your shipments don't arrive.",
                        "next": "start",
                    },
                    "news": {
                        "speaker": "Merchant",
                        "text": "Word from the last trader through: the roads east of Thornhaven "
                                "are worse than ever. Something out there's spooking the horses "
                                "before you can even see what it is. Stay on the main paths.",
                        "next": "start",
                    },
                    "bye": {
                        "speaker": "Merchant",
                        "text": "Come back when your purse is heavier.",
                        "end": True,
                    },
                },
            },
        },
    ],
    "ambient_scholar": [
        {
            "conditions": [],
            "tree": {
                "id": "ambient_scholar_default",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Scholar",
                        "text": "Hmm? Oh — sorry, deep in thought. "
                                "The Fading does strange things to the ley lines. "
                                "I've been trying to document it but the patterns keep shifting.",
                        "choices": [
                            {"text": "What can you tell me about the Fading?", "next": "fading"},
                            {"text": "Don't let me interrupt.",                "next": "bye"},
                        ],
                    },
                    "fading": {
                        "speaker": "Scholar",
                        "text": "It's not just decay — it's erasure. Magic forgets itself. "
                                "Creatures mutate toward entropy. The Hearthstones were built "
                                "to anchor the ley network, prevent exactly this. "
                                "Without them, the world slowly... unmakes.",
                        "next": "start",
                    },
                    "bye": {
                        "speaker": "Scholar",
                        "text": "Of course. Do be careful — knowledge is only useful "
                                "if you survive to apply it.",
                        "end": True,
                    },
                },
            },
        },
    ],
    "ambient_harbormaster": [
        {
            "conditions": [],
            "tree": {
                "id": "ambient_harbormaster_default",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Harbor Master",
                        "text": "All ships register here. No exceptions. "
                                "You want to cross the strait, you file the paperwork first.",
                        "choices": [
                            {"text": "What ships are in port?",       "next": "ships"},
                            {"text": "Is the sea route safe?",        "next": "safe"},
                            {"text": "What's east of here?",          "next": "east_ports"},
                            {"text": "Just passing through.",         "next": "bye"},
                        ],
                    },
                    "ships": {
                        "speaker": "Harbor Master",
                        "text": "Two merchants, one fishing boat, and a vessel I've been told "
                                "to ask no questions about. That last one troubles me.",
                        "next": "start",
                    },
                    "safe": {
                        "speaker": "Harbor Master",
                        "text": "Define safe. The water's calm enough. It's what's under it "
                                "that's changed. Captains are reporting lights in the deep "
                                "that follow the hull. I'm keeping my own feet on dry land.",
                        "next": "start",
                    },
                    "east_ports": {
                        "speaker": "Harbor Master",
                        "text": "Two places worth knowing. Emberveil, on the Dragon's Tooth "
                                "island — volcanic mining post, maybe two hundred souls. "
                                "The smith there, Renn, knows those lava-cave routes better "
                                "than anyone.\n"
                                "And the Anchorage, on the mainland coast opposite the "
                                "Windswept Isle. Crystalspire researchers and fisherfolk. "
                                "There is an elf there, Elder Vaethari — very old, very sharp. "
                                "Worth speaking to if you are headed for the Isle.",
                        "next": "start",
                    },
                    "bye": {
                        "speaker": "Harbor Master",
                        "text": "Right. Don't block the dock.",
                        "end": True,
                    },
                },
            },
        },
    ],
}

NPC_DIALOGUES.update(_AMBIENT_DIALOGUES)


# ══════════════════════════════════════════════════════════════
#  POST-BOSS DIALOGUES
#  These fire after the boss combat victory, before loot screen.
#  Two variants per boss: "fight" (killed) and "peaceful" (spared).
#  Only bosses with something worth saying get entries.
# ══════════════════════════════════════════════════════════════

BOSS_POST_DIALOGUES = {

    "goblin_warren": {
        "fight": {
            "id": "grak_aftermath",
            "speaker": "",
            "lines": [
                "Grak falls. The goblins do not rush you. They stand in silence, "
                "watching their king die with the quiet resignation of people "
                "who have lost everything before and know exactly what losing looks like.",
                "In his clenched fist: the Hearthstone Fragment.\n"
                "It comes free easily. As if it was always meant to.",
                "Behind you, someone — one of the younger goblins — begins to keen. "
                "Low, rhythmic, grief-shaped.",
                "You leave with the stone.\nThe crying follows you up the tunnel for a long time.",
            ],
        },
    },

    "spiders_nest": {
        "fight": {
            "id": "spider_queen_aftermath",
            "speaker": "",
            "lines": [
                "The Spider Queen collapses inward — not quite like a creature dying, "
                "but like a knot being untied. The iridescent shimmer bleeds out of "
                "the webs around her.",
                "The light that was wrong about this place — the colours that shifted "
                "between frames — fades. The Fading energy that mutated the nest "
                "dissipates slowly, like mist burning off in morning sun.",
                "The remaining spiders scatter. They are small, natural, confused. "
                "Without the Queen's fading-warped will driving them, they are just "
                "animals again. They want nothing from you.",
                "Whatever the Fading made her into, it is over.\nThe nest goes quiet.",
            ],
        },
    },

    "abandoned_mine": {
        "fight": {
            "id": "korrath_aftermath",
            "speaker": "Korrath the Stone Warden",
            "lines": [
                "Korrath falls to one knee. The stone form cracks — not breaking, "
                "but releasing. Like a fist finally unclenching after four hundred years.",
                "\"You are... as strong as I hoped.\"\nHe looks down at his hands "
                "as the stone crumbles away from them, revealing something underneath. "
                "Not flesh. Just the shape of a man, briefly, in the dark.",
                "\"The stone is yours. The oath is... satisfied.\"\nHis voice is "
                "already fading. Not death — something more like relief.\n"
                "\"Tell them I held it. To the end.\"",
                "He dissolves.\nNot violently. Not painfully.\n"
                "The way a watch-fire goes out when morning comes and it is no longer needed.",
                "The Hearthstone Fragment glows warmly in the chamber where it has "
                "rested for four centuries.\nKorrath is gone. His duty is not.",
            ],
        },
    },

    "ruins_ashenmoor": {
        "fight": {
            "id": "ashvar_aftermath",
            "speaker": "Commander Ashvar",
            "lines": [
                "Ashvar staggers. The ash that formed him scatters, briefly, "
                "then coheres again — but weaker. He looks at his own hands "
                "as if he can't remember how long they've been made of smoke and sorrow.",
                "\"You fight like Wardens.\"\nA pause.\n\"That is not an insult. "
                "That is the only compliment I know how to give.\"",
                "\"Valdris... what he did here. It must not be forgotten. "
                "There are records in the lower vault. Sealed. "
                "I have been keeping them. In case someone came who could act on them.\"\n"
                "\"You can act on them. I could not.\"",
                "He doesn't fall so much as disperse — the ash releasing upward, "
                "slowly, like incense. The long-held tension of two hundred years "
                "going out of the room.",
                "He is gone.\nThe ruins feel, for the first time, like ruins — "
                "sad and old, instead of angry.",
            ],
        },
    },

    "dragons_tooth": {
        "fight": {
            "id": "karreth_aftermath_fight",
            "speaker": "",
            "lines": [
                "Karreth falls.\nThe grey-green eye goes dark first, then the amber. "
                "The enormous body settles into the volcanic rock as if the island "
                "itself is accepting it back.",
                "The Hearthstone Fragment pulses once — as if acknowledging the passing "
                "of its oldest guardian — and then rests.",
                "You take the stone. It is warm in a way that has nothing to do with "
                "the volcano beneath you.",
                "On the way out, you pass the carvings on the hoard room doorframe — "
                "the scratched note about a figure curled around a glowing light. "
                "Like it remembered what warm meant.",
                "You understand that better now.",
            ],
        },
        "peaceful": {
            "id": "karreth_aftermath_peaceful",
            "speaker": "",
            "lines": [
                "Karreth does not move as you carry the stone out of the chamber. "
                "The amber light in both enormous eyes watches you go — calm, clear, "
                "no longer fractured by grey-green.",
                "At the tunnel entrance, you look back.\n"
                "Karreth has lowered its head to the volcanic floor. "
                "Eyes still open. Still watching.",
                "It does not follow you.\nIt does not need to.\nIts purpose is finished.",
                "The island feels different on the way out. "
                "The sulfur smell is still there. The black glass is still underfoot. "
                "But the weight that sat over the caldera — the wrong-feeling pressure "
                "that had been building since you arrived — is gone.",
                "You also carry a single dragon scale, shed freely. "
                "It is still warm.\nIt will not stop being warm for a very long time.",
            ],
        },
    },

    "sunken_crypt": {
        "fight": {
            "id": "sunken_warden_aftermath",
            "speaker": "The Sunken Warden",
            "lines": [
                "The Sunken Warden dissolves into the water that fills the lower chamber — "
                "not destroyed, but released. The binding that held Deren here for two "
                "centuries finally unravels.",
                "As he goes, something like a voice comes from everywhere and nowhere:\n"
                "\"Thank you.\"\nTwo words. Very quietly.",
                "\"Tell the order — if there is still an order — that the stone was "
                "protected. That Deren held.\"\n"
                "\"That someone finally came.\"",
                "The water stills.\nThe crypt is just a crypt now.\n"
                "And the Hearthstone Fragment floats, gently, to the surface.",
            ],
        },
    },

    "pale_coast": {
        "fight": {
            "id": "sentinel_aftermath_fight",
            "speaker": "The Pale Sentinel",
            "lines": [
                "The Sentinel goes down slowly — not like defeat, but like a vigil ending. "
                "She never stops facing you, never turns away. Even in falling, she is "
                "exactly what she was: present, resolved, done.",
                "\"I... did not expect you to be worthy.\"\nHer voice is already "
                "fading at the edges. \"I expected to hold forever. "
                "The order never said anyone would come.\"",
                "\"The stone is yours.\"\nA pause. Something shifts in her face. "
                "\"I am... glad. That this ended.\"",
                "The armor stays. The woman inside it goes somewhere quieter.",
            ],
        },
        "peaceful": {
            "id": "sentinel_aftermath_peaceful",
            "speaker": "",
            "lines": [
                "Warden Sirenne of the Pale Coast steps back from the Hearthstone "
                "pedestal and does not look back at it. After forty-three years, "
                "she faces outward for the first time.",
                "She walks to the cave entrance with you.\nAt the threshold, "
                "she stops. Looks at the sea. The real sea, not the stone ceiling "
                "above the catacombs.",
                "She stands there for a long time.",
                "You don't ask what she's going to do next. It doesn't feel like "
                "the right question. People who have been the lock for four decades "
                "need to find out for themselves what they are when the door is gone.",
                "She lets you leave first.\nWhen you look back from the path, "
                "she is still standing at the entrance, face turned toward the horizon, "
                "hands open at her sides.",
            ],
        },
    },

    "windswept_isle": {
        "fight": {
            "id": "isle_keeper_aftermath",
            "speaker": "",
            "lines": [
                "The Keeper disperses. Not like a defeat — more like a door opening "
                "and the wind finally passing through. The storm inside the ruins "
                "quiets. The arcane instruments on the walls go still.",
                "On the pedestal where the Hearthstone rests, you find something "
                "the Keeper left behind — placed deliberately, not dropped. "
                "A seal with no name on it.",
                "It chose not to be remembered by name. But it left this. "
                "Perhaps that was the only kind of name it wanted.",
                "The fifth stone.\nAll of them, now, in your hands.\n"
                "The weight of what you're carrying has not changed. "
                "But the shape of it has.",
            ],
        },
    },
}


# ══════════════════════════════════════════════════════════════
#  PEACEFUL RESOLUTION DEFINITIONS
#  Specifies what flags signal a peaceful outcome and what the
#  party receives in lieu of fighting the boss.
#  hearthstone_num: int or None (which hearthstone to collect)
#  bonus_loot: list of unique_keys from UNIQUE_ITEMS to grant
# ══════════════════════════════════════════════════════════════

BOSS_PEACEFUL_RESOLUTIONS = {
    "spiders_nest": {
        "flag":          "choice.spider_queen_spared",
        "hearthstone":   None,          # Spider's Nest holds no Hearthstone
        "hearthstone_name": None,
        "bonus_loot":    [],
        "boss_npc":      "spider_queen",
        "world_key":     "mine_key",    # unlocks Abandoned Mine
    },
    "goblin_warren": {
        "flag":          "choice.grak_spared",
        "hearthstone":   1,
        "hearthstone_name": "Hearthstone Fragment (Warren)",
        "bonus_loot":    [],           # Grak has no unique equip worth granting on peace
        "boss_npc":      "grak",
        "world_key":     "thornwood_map",
    },
    "dragons_tooth": {
        "flag":          "choice.karreth_spared",
        "hearthstone":   3,
        "hearthstone_name": "Hearthstone Fragment (Dragon's Tooth)",
        "bonus_loot":    ["karreth_scale"],
        "boss_npc":      "karreth",
        "world_key":     "dragon_scale",
    },
    "pale_coast": {
        "flag":          "sentinel.yielded",
        "hearthstone":   4,
        "hearthstone_name": "Hearthstone Fragment (Pale Coast)",
        "bonus_loot":    ["sirenne_buckler"],
        "boss_npc":      "pale_sentinel",
        "world_key":     "pale_coast_cleared",
    },
}


def get_boss_post_dialogue(dungeon_id, peaceful=False):
    """Return post-boss dialogue dict for a dungeon, or None if none defined."""
    entry = BOSS_POST_DIALOGUES.get(dungeon_id)
    if not entry:
        return None
    if peaceful and "peaceful" in entry:
        return entry["peaceful"]
    return entry.get("fight")


def get_peaceful_resolution(dungeon_id):
    """Return peaceful resolution spec for a dungeon, or None."""
    return BOSS_PEACEFUL_RESOLUTIONS.get(dungeon_id)


# ═══════════════════════════════════════════════════════════════
#  TRAINER NPC DIALOGUES  (class transition guidance)
# ═══════════════════════════════════════════════════════════════

_TRAINER_DIALOGUES = {
    "trainer_briarhollow": [
        {
            "conditions": [],
            "tree": {
                "id": "trainer_briarhollow",
                "nodes": {
                    "start": {
                        "speaker": "Guildmaster Oren",
                        "text": "Experience forges new paths, adventurer. When your abilities are seasoned "
                                "enough — around level 10 — you may find yourself capable of walking between "
                                "disciplines.",
                        "next": "node2",
                    },
                    "node2": {
                        "speaker": "Guildmaster Oren",
                        "text": "A Fighter who hones both sword and holy conviction can become a Paladin. "
                                "A Thief who masters the shadows becomes something far more dangerous. "
                                "The Guild calls these transitions.",
                        "next": "node3",
                    },
                    "node3": {
                        "speaker": "Guildmaster Oren",
                        "text": "Visit the class board in any guild hall when your party reaches level 10. "
                                "Your attributes must meet the demands of the new path — and not all roads "
                                "are open to all.",
                        "end": True,
                    },
                },
            },
        },
    ],
    "trainer_ironhearth": [
        {
            "conditions": [],
            "tree": {
                "id": "trainer_ironhearth",
                "nodes": {
                    "start": {
                        "speaker": "Guildmaster Dorric",
                        "text": "Aye, I've trained a few who went beyond their first calling. "
                                "It's not about forgetting what you were — it's about becoming more.",
                        "next": "node2",
                    },
                    "node2": {
                        "speaker": "Guildmaster Dorric",
                        "text": "I've seen Fighters who studied the arcane become Spellblades. Monks who "
                                "found the divine and became Templar. And Rangers who walked the shadow — "
                                "best not ask what became of them.",
                        "next": "node3",
                    },
                    "node3": {
                        "speaker": "Guildmaster Dorric",
                        "text": "Get to level 10, keep your stats sharp, and talk to the class board in "
                                "the guild. The old masters say there's a path beyond that too — at "
                                "level 15 — but I've never seen it.",
                        "end": True,
                    },
                },
            },
        },
    ],
    # ── Ambient NPC types for new settlements ───────────────────────────────
    "ambient_fisher": [
        {"conditions": [], "tree": {"id": "ambient_fisher_default", "loop": True, "nodes": {
            "start": {"speaker": "Fisher", "text": "The currents have been strange lately. Something under the water is restless.",
                      "choices": [{"text": "Stay safe.", "next": None}]},
        }}},
    ],
    "ambient_miner": [
        {"conditions": [], "tree": {"id": "ambient_miner_default", "loop": True, "nodes": {
            "start": {"speaker": "Miner", "text": "Dragon's Tooth has been groaning for weeks. I give it a month before she blows.",
                      "choices": [{"text": "Take care.", "next": None}]},
        }}},
    ],
    "ambient_rebel": [
        {"condition": None, "lines": [
            "We didn't choose this fight. The Fading chose it for us.",
        ]},
    ],
    "ambient_scout": [
        {"condition": None, "lines": [
            "The perimeter's clear for now. Won't stay that way if Valdris pushes south.",
        ]},
    ],

    # ── Emberveil Warden contact ──────────────────────────────────────────────
    "renn_emberveil": [
        # ── After Shadow Valdris defeated ────────────────────────────────────
        {
            "conditions": [{"flag": "boss_defeated.shadow_valdris", "op": "==", "value": True}],
            "tree": {
                "id": "renn_emberveil_post_valdris",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Master Forger Renn",
                        "text": "Word came down from the Spire. The Shadow is gone.\n"
                                "I've been forging in this caldera for twenty years waiting "
                                "to hear something like that.\n"
                                "The Fading fog is already lighter on the eastern ridge. "
                                "Give it a season.",
                        "choices": [
                            {"text": "It's over.", "next": "its_over"},
                            {"text": "Farewell, Renn.", "next": None},
                        ],
                    },
                    "its_over": {
                        "speaker": "Master Forger Renn",
                        "text": "For now. The wards need tending, same as always.\n"
                                "But at least there's someone tending them again.\n"
                                "My grandmother would've approved of you.",
                        "end": True,
                    },
                },
            },
        },
        # ── Inside Valdris' Spire ─────────────────────────────────────────────
        {
            "conditions": [{"flag": "explored.valdris_spire.floor1", "op": "==", "value": True}],
            "tree": {
                "id": "renn_emberveil_in_spire",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Master Forger Renn",
                        "text": "You're inside the Spire. Or you were.\n"
                                "I've heard the sounds from the caldera at night — "
                                "something resonating in the rock itself.\n"
                                "That's the wards straining. Don't take long.",
                        "choices": [
                            {"text": "What's the fastest path through?", "next": "path"},
                            {"text": "We know what we're doing.", "next": "bye"},
                        ],
                    },
                    "path": {
                        "speaker": "Master Forger Renn",
                        "text": "The anchor chamber is at the apex — straight up the central shaft.\n"
                                "The Shadow will be between you and it. My grandmother "
                                "never faced a corrupted Warden. I don't know what that means for tactics.\n"
                                "Trust your instincts. And your Hearthstones.",
                        "end": True,
                    },
                    "bye": {
                        "speaker": "Master Forger Renn",
                        "text": "Then go. I'll keep the forge burning until you're back.",
                        "end": True,
                    },
                },
            },
        },
        # ── All five Hearthstones — ready for the Spire ───────────────────────
        {
            "conditions": [{"flag": "item.hearthstone.5", "op": "==", "value": True}],
            "tree": {
                "id": "renn_emberveil_all_stones",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Master Forger Renn",
                        "text": "Five stones. You actually got all five.\n"
                                "The Spire is northeast of here — you've probably seen it "
                                "on the ridge. The entrance is warded, but the Hearthstones "
                                "will key it open.\n"
                                "Whatever's inside has been waiting a long time. "
                                "Don't let it wait any longer.",
                        "choices": [
                            {"text": "What do you know about what's inside?", "next": "inside"},
                            {"text": "We're ready.", "next": "bye"},
                        ],
                    },
                    "inside": {
                        "speaker": "Master Forger Renn",
                        "text": "Something that was once a Warden named Valdris.\n"
                                "Corrupted by the Fading, but not consumed — he chose this.\n"
                                "My grandmother's notes call it the Shadow Compact: "
                                "a Warden who fed the Fading instead of fighting it, "
                                "buying himself a kind of immortality.\n"
                                "She wrote that the only way out of that bargain is through it.",
                        "end": True,
                    },
                    "bye": {
                        "speaker": "Master Forger Renn",
                        "text": "Come back when it's done. I'll have a drink waiting.\n"
                                "Something from before the volcano started smelling like this.",
                        "end": True,
                    },
                },
            },
        },
        # ── Dragon's Tooth cleared, knows about Spire ────────────────────────
        {
            "conditions": [{"flag": "boss_defeated.dragons_tooth", "op": "==", "value": True}],
            "tree": {
                "id": "renn_emberveil_tooth_cleared",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Master Forger Renn",
                        "text": "Karreth is gone. Good. He was making the caldera unstable — "
                                "something about a corrupted drake that size absorbing "
                                "the volcanic heat differently.\n"
                                "You need the Hearthstones from the remaining dungeons. "
                                "The Spire is the endgame. "
                                "Get to Windswept Isle and the Ruins of Ashenmoor — "
                                "there are stones in both.",
                        "choices": [
                            {"text": "Tell me about the Spire.", "next": "spire"},
                            {"text": "We'll keep moving.", "next": "bye"},
                        ],
                    },
                    "spire": {
                        "speaker": "Master Forger Renn",
                        "text": "Valdris' Spire. The old Warden anchor tower — "
                                "where the great ward network was maintained.\n"
                                "The Shadow corrupted it from the inside. "
                                "Five Hearthstones will restore the anchor. "
                                "Then you face whatever Valdris became.",
                        "end": True,
                    },
                    "bye": {
                        "speaker": "Master Forger Renn",
                        "text": "The stones won't collect themselves. Move.",
                        "end": True,
                    },
                },
            },
        },
        # ── Default ───────────────────────────────────────────────────────────
        {
            "conditions": [],
            "tree": {
                "id": "renn_emberveil_default",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Master Forger Renn",
                        "text": "Name's Renn. I run the forge — and I keep an eye on "
                                "Dragon's Tooth for the old Order.\n"
                                "There's a back way into the Tooth. "
                                "Lava tube, third vent on the east face.",
                        "choices": [
                            {"text": "Tell me more about the back entrance.",
                             "next": "back_way"},
                            {"text": "What's your connection to the Warden Order?",
                             "next": "warden"},
                            {"text": "Any news from the Ashlands?", "next": "ashlands"},
                            {"text": "Thanks for the tip.", "next": "bye"},
                        ],
                    },
                    "back_way": {
                        "speaker": "Master Forger Renn",
                        "text": "Third vent on the east face — you'll know it by the "
                                "blue-edged smoke. Bypasses the first floor entirely, "
                                "puts you in the mid-caves.\n"
                                "My terms: clear whatever's nesting near the caldera. "
                                "The smoke's changed colour and that means something "
                                "moved in.",
                        "next": "start",
                    },
                    "warden": {
                        "speaker": "Master Forger Renn",
                        "text": "My grandmother was a Warden-Commander. "
                                "She taught me the signs and the routes before she died.\n"
                                "The Order's gone, but the information isn't. "
                                "Seems worth passing on.",
                        "next": "start",
                    },
                    "ashlands": {
                        "speaker": "Master Forger Renn",
                        "text": "The Fading fog is visible from the caldera on a clear day. "
                                "Getting closer every month.\n"
                                "If what's in Valdris' Spire doesn't get stopped, "
                                "Emberveil becomes an island in a sea of nothing. "
                                "I'd prefer that not happen.",
                        "next": "start",
                    },
                    "bye": {
                        "speaker": "Master Forger Renn",
                        "text": "Come back when you've cleared the caldera. "
                                "I'll have something worth your while.",
                        "end": True,
                    },
                },
            },
        },
    ],

    # ── The Anchorage Warden contact ──────────────────────────────────────────
    "vaethari_anchorage": [
        # ── After Shadow Valdris defeated ─────────────────────────────────────
        {
            "conditions": [{"flag": "boss_defeated.shadow_valdris", "op": "==", "value": True}],
            "tree": {
                "id": "vaethari_post_valdris",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Elder Vaethari",
                        "text": "I felt it when it happened. Three hundred years of watching "
                                "the wards decay, and then — a moment of clarity.\n"
                                "The anchor holds. The binding is restored.\n"
                                "You have done what the Wardens could not.",
                        "choices": [
                            {"text": "It cost us.", "next": "cost"},
                            {"text": "The world should know.", "next": "know"},
                            {"text": "Farewell, Elder.", "next": None},
                        ],
                    },
                    "cost": {
                        "speaker": "Elder Vaethari",
                        "text": "It always does. The Fading does not give back what it takes.\n"
                                "But the debt is settled. The world will not remember — "
                                "it never does — but I will.\n"
                                "Three hundred years is long enough to learn what matters.",
                        "end": True,
                    },
                    "know": {
                        "speaker": "Elder Vaethari",
                        "text": "The world will know in its own way. The fog will lift. "
                                "The crops will be better next season. Children will be born "
                                "without the shadow-sickness.\n"
                                "They won't know why. That is as it should be.",
                        "end": True,
                    },
                },
            },
        },
        # ── All five Hearthstones — guidance to the Spire ─────────────────────
        {
            "conditions": [{"flag": "item.hearthstone.5", "op": "==", "value": True}],
            "tree": {
                "id": "vaethari_all_stones",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Elder Vaethari",
                        "text": "All five Hearthstones. The full set — I did not think "
                                "I would live to see it.\n"
                                "The Spire anchor chamber is at the tower's apex. "
                                "Place each stone in the ward array. "
                                "The binding will begin.\n"
                                "Valdris will try to prevent it. He has had a long time "
                                "to prepare.",
                        "choices": [
                            {"text": "How do we fight something like him?", "next": "fight"},
                            {"text": "We're going now.", "next": "going"},
                        ],
                    },
                    "fight": {
                        "speaker": "Elder Vaethari",
                        "text": "The corruption is old but the Warden beneath it is older.\n"
                                "I have read what records survived the Order's fall. "
                                "Valdris was strongest in his certainty — he believed "
                                "what he did was necessary. That belief is also his weakness.\n"
                                "He chose this. Remind him of that, if words are still possible. "
                                "If not — the Hearthstones will hold him long enough.",
                        "end": True,
                    },
                    "going": {
                        "speaker": "Elder Vaethari",
                        "text": "Then go. I have watched this world for three hundred years.\n"
                                "I would like to see what it looks like without the shadow for a while.",
                        "end": True,
                    },
                },
            },
        },
        # ── Windswept Isle cleared — heading toward endgame ───────────────────
        {
            "conditions": [{"flag": "boss_defeated.windswept_isle", "op": "==", "value": True}],
            "tree": {
                "id": "vaethari_isle_cleared",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Elder Vaethari",
                        "text": "The Keeper is at rest. I felt that too — three hundred "
                                "years and I still felt her go.\n"
                                "What remains?\n"
                                "Ashenmoor, if you haven't cleared it. Then the Spire.",
                        "choices": [
                            {"text": "Tell us about Ashenmoor.", "next": "ashenmoor"},
                            {"text": "We head for the Spire.", "next": "spire"},
                        ],
                    },
                    "ashenmoor": {
                        "speaker": "Elder Vaethari",
                        "text": "A ruined Warden outpost in the Ashlands. "
                                "The last Hearthstone is there, in the commander's vault.\n"
                                "The Fading has been thick over it for years. "
                                "I do not know what you will find.\n"
                                "Go carefully.",
                        "end": True,
                    },
                    "spire": {
                        "speaker": "Elder Vaethari",
                        "text": "You will need all five Hearthstones before the anchor "
                                "will accept your offering. Do not go before you have them all.\n"
                                "Valdris will be waiting regardless. No need to arrive unprepared.",
                        "end": True,
                    },
                },
            },
        },
        # ── After meeting Maren — Act 2/3 threshold ───────────────────────────
        {
            "conditions": [{"flag": "npc.maren.met", "op": "==", "value": True}],
            "tree": {
                "id": "vaethari_maren_met",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Elder Vaethari",
                        "text": "You've spoken with the scholar. Good.\n"
                                "Maren understands the Hearthstone mechanism better than "
                                "anyone living — she has spent twenty years reconstructing "
                                "what the Order destroyed in its fall.\n"
                                "Follow where she points. She is rarely wrong about the old things.",
                        "choices": [
                            {"text": "What can you tell us about the dungeons ahead?", "next": "dungeons"},
                            {"text": "Thank you, Elder.", "next": None},
                        ],
                    },
                    "dungeons": {
                        "speaker": "Elder Vaethari",
                        "text": "The Spiders' Nest holds a Hearthstone beneath the queen's lair. "
                                "The Abandoned Mine hides another in its deepest chamber.\n"
                                "Beyond that — Dragon's Tooth in the Ashlands, "
                                "Windswept Isle across the grey water, "
                                "and the Ruins of Ashenmoor where the old Order fell.\n"
                                "Five stones. Five dungeons. The world does not make things easy.",
                        "end": True,
                    },
                },
            },
        },
        # ── Default ───────────────────────────────────────────────────────────
        {
            "conditions": [],
            "tree": {
                "id": "vaethari_anchorage_default",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Elder Vaethari",
                        "text": "I have watched three hundred years of this world. "
                                "The Fading is not new — the wards have frayed before.\n"
                                "But this outbreak is different. Something with will "
                                "is driving it, not merely entropy.",
                        "choices": [
                            {"text": "Tell us about Windswept Isle.",
                             "next": "about_isle"},
                            {"text": "What do you know about Valdris?",
                             "next": "about_valdris"},
                            {"text": "What are the Hearthstones?", "next": "hearthstones"},
                            {"text": "Thank you, Elder.", "next": "bye"},
                        ],
                    },
                    "about_isle": {
                        "speaker": "Elder Vaethari",
                        "text": "The Keeper of Windswept Isle is an old friend. "
                                "Or was, before the Fading took her.\n"
                                "She would not harm you willingly. "
                                "Whatever she has become, part of her remembers.\n"
                                "Approach the central shrine. "
                                "Speak the old words: Aethen, sol vareth, kai.\n"
                                "She will hear you. Whether she answers — "
                                "that I cannot promise.",
                        "next": "start",
                    },
                    "about_valdris": {
                        "speaker": "Elder Vaethari",
                        "text": "Valdris was a Senior Warden. Brilliant and reckless "
                                "in equal measure.\n"
                                "He believed the wards could be strengthened permanently — "
                                "not just maintained, but made eternal. "
                                "He attempted a ritual that required a sacrifice of will.\n"
                                "The Fading claimed him before the ritual completed. "
                                "What remains is something that was Valdris "
                                "and chose not to end.",
                        "next": "start",
                    },
                    "hearthstones": {
                        "speaker": "Elder Vaethari",
                        "text": "Ward anchor points — crystallised concentrations of "
                                "the original binding magic.\n"
                                "Each stone reinforces a section of the great ward network. "
                                "Scattered when the Order fell, "
                                "but recoverable if someone knows where to look.\n"
                                "You have them, I presume, or you would not be here. "
                                "Good. Take them to the Spire anchor points. "
                                "The binding will complete itself.",
                        "next": "start",
                    },
                    "bye": {
                        "speaker": "Elder Vaethari",
                        "text": "Three hundred years of watching, and still the young "
                                "ones have to be the ones who act.\n"
                                "Go well.",
                        "end": True,
                    },
                },
            },
        },
    ],

    # ── The Holdfast Warden contacts ──────────────────────────────────────────
    # ── Quartermaster Dael — last Warden initiate, camp quartermaster ─────────
    "dael_holdfast": [
        # After Maren entered the Spire — different framing
        {
            "conditions": [{"flag": "maren.left", "op": "==", "value": True}],
            "tree": {
                "id": "dael_holdfast_maren_gone",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Quartermaster Dael",
                        "text": "Warden Initiate Dael. You must be the Wardens Maren "
                                "told me to watch for.\n"
                                "She left a note at the camp entrance — said you'd come eventually. "
                                "I've been holding it.",
                        "choices": [
                            {"text": "What does the note say?", "next": "the_note"},
                            {"text": "When did she arrive here?", "next": "when_arrived"},
                            {"text": "What do you know about the Spire?", "next": "spire_info"},
                            {"text": "We need supplies for the Spire approach.", "next": "supplies"},
                        ],
                    },
                    "the_note": {
                        "speaker": "Quartermaster Dael",
                        "text": "Here.\n\n"
                                "[The note reads: 'They will come from the south. "
                                "Tell them the Spire wards are still active — "
                                "that means he hasn't completed the ritual yet. "
                                "There is still time. I went ahead to find the anchor points. "
                                "I did not go in fear. Do not come in fear either. — M']",
                        "next": "start",
                    },
                    "when_arrived": {
                        "speaker": "Quartermaster Dael",
                        "text": "About a week ago. Stayed one night, traded some coin for "
                                "supplies, and left before dawn.\n"
                                "Scout Mira watched her go. Said she walked toward the Spire "
                                "like someone walking to a meeting they'd been dreading "
                                "for years. Calm. Deliberate.\n"
                                "None of us have seen anyone come back out. "
                                "But the tower wards are still intact — "
                                "that means whatever she went in to stop hasn't happened yet.",
                        "next": "start",
                    },
                    "spire_info": {
                        "speaker": "Quartermaster Dael",
                        "text": "The Spire draws on something called the Lingering Will — "
                                "a consciousness that refused the Fading and bound itself "
                                "to the tower instead.\n"
                                "My training said: don't let it speak at length. "
                                "It uses grief. It finds the thing you most regret "
                                "and it offers to fix it.\n"
                                "Don't bargain. Don't hesitate. "
                                "The wards can still be restored if you reach the top floor.",
                        "next": "start",
                    },
                    "supplies": {
                        "speaker": "Quartermaster Dael",
                        "text": "We're thin but we share what we have. "
                                "Sarev has authorised a resupply for any Warden-aligned party "
                                "heading for the Spire.\n"
                                "The Shadow Throne is beyond the Spire to the northeast — "
                                "don't attempt it before the Spire is cleared. "
                                "The Throne is sealed until the Lingering Will is broken.",
                        "next": "bye",
                    },
                    "bye": {
                        "speaker": "Quartermaster Dael",
                        "text": "Go in angry, not afraid. That's the only advice I have "
                                "that's worth anything.",
                        "end": True,
                    },
                },
            },
        },
        # Default — before Maren left
        {
            "conditions": [],
            "tree": {
                "id": "dael_holdfast_default",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Quartermaster Dael",
                        "text": "Warden Initiate Dael. Last one standing, near as I can tell.\n"
                                "I never finished my training — the Order fell before I could "
                                "take my oaths. But I know enough to keep this camp alive.",
                        "choices": [
                            {"text": "What can you tell us about the Spire?", "next": "spire_info"},
                            {"text": "What's the situation here at the Holdfast?",
                             "next": "situation"},
                            {"text": "Stay safe.", "next": "bye"},
                        ],
                    },
                    "spire_info": {
                        "speaker": "Quartermaster Dael",
                        "text": "Valdris' Spire is north of here, in the deep Ashlands. "
                                "You can't miss it — black stone, no windows, "
                                "wards that make your teeth ache.\n"
                                "The Lingering Will inside it is what's driving the Fading. "
                                "Stop that, and the worst of it should ease.",
                        "next": "start",
                    },
                    "situation": {
                        "speaker": "Quartermaster Dael",
                        "text": "We hold this position as long as we can. "
                                "Every day we hold it is another day for the villages "
                                "further south to evacuate.\n"
                                "The Fading pushes harder each week. "
                                "Whatever you're doing out there — do it faster.",
                        "next": "start",
                    },
                    "bye": {
                        "speaker": "Quartermaster Dael",
                        "text": "Watch the Ashlands fog. It's not natural.",
                        "end": True,
                    },
                },
            },
        },
    ],

    # ── Commander Sarev — rebel leader, pragmatist ──────────────────────────
    "sarev_holdfast": [
        # After Maren entered — knows she went in
        {
            "conditions": [{"flag": "maren.left", "op": "==", "value": True}],
            "tree": {
                "id": "sarev_holdfast_act3",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Commander Sarev",
                        "text": "You're the Wardens she mentioned. Good.\n"
                                "The scholar — Maren — entered the Spire six days ago. "
                                "No one's come out. But the wards are still up, "
                                "which means the ritual hasn't completed.\n"
                                "You still have a window.",
                        "choices": [
                            {"text": "What do you know about the Spire's defenses?",
                             "next": "defenses"},
                            {"text": "Tell me about the Shadow Throne.", "next": "throne"},
                            {"text": "Why are you helping us?", "next": "why_help"},
                            {"text": "We're ready to move.", "next": "ready"},
                        ],
                    },
                    "defenses": {
                        "speaker": "Commander Sarev",
                        "text": "Six floors, each one worse than the last. "
                                "The Spire summons things — echoes of fallen Wardens, "
                                "mostly. Corrupted, angry, lethal.\n"
                                "The thing at the top is what she calls a Lingering Will. "
                                "My scouts say it projects illusions. "
                                "Don't trust what you see on the upper floors.",
                        "next": "start",
                    },
                    "throne": {
                        "speaker": "Commander Sarev",
                        "text": "The Shadow Throne is northeast of the Spire — "
                                "about four hours on foot through the Ashlands.\n"
                                "It's sealed while the Lingering Will exists. "
                                "Break that first. Then the Throne becomes accessible.\n"
                                "That's where the Fading began, and where it can end. "
                                "The Hearthstones you carry are the key.",
                        "next": "start",
                    },
                    "why_help": {
                        "speaker": "Commander Sarev",
                        "text": "Because I want the Ashlands free. "
                                "Not free of Valdris only — free of the empire too, "
                                "eventually.\n"
                                "But one problem at a time. "
                                "Valdris is killing my people faster than the empire is. "
                                "You stop the Fading, and I'll owe you a debt. "
                                "I pay my debts.",
                        "next": "start",
                    },
                    "ready": {
                        "speaker": "Commander Sarev",
                        "text": "Then go. The Spire is north-northeast, "
                                "two hours through the Ashlands.\n"
                                "I'll keep a light burning here. "
                                "If you're not back in three days — "
                                "well. I'll think of something to tell the survivors.",
                        "end": True,
                    },
                },
            },
        },
        # Default
        {
            "conditions": [],
            "tree": {
                "id": "sarev_holdfast_default",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Commander Sarev",
                        "text": "The empire calls us rebels. Valdris calls us insurgents.\n"
                                "We call ourselves alive — which is more than most "
                                "Ashlanders can say.",
                        "choices": [
                            {"text": "What's your goal here?", "next": "goal"},
                            {"text": "Can you tell us about Valdris' Spire?",
                             "next": "spire"},
                            {"text": "We may need your help soon.", "next": "help"},
                            {"text": "We'll be in touch.", "next": "bye"},
                        ],
                    },
                    "goal": {
                        "speaker": "Commander Sarev",
                        "text": "Simple: protect what's left of the Ashlands. "
                                "When the Fading passes — if it passes — "
                                "we want to still be standing here.\n"
                                "The empire can negotiate with survivors. "
                                "They can't negotiate with ash.",
                        "next": "start",
                    },
                    "spire": {
                        "speaker": "Commander Sarev",
                        "text": "Black tower, north of here. Six floors of things "
                                "that want you dead, and something at the top "
                                "that wants worse than that.\n"
                                "My scouts don't go within half a mile. "
                                "Not after what happened to the last ones.",
                        "next": "start",
                    },
                    "help": {
                        "speaker": "Commander Sarev",
                        "text": "You want my help, help us first. "
                                "Hold the perimeter, clear a route through the Ashlands, "
                                "or just survive long enough to matter.\n"
                                "Prove you're worth backing. Then we talk.",
                        "next": "start",
                    },
                    "bye": {
                        "speaker": "Commander Sarev",
                        "text": "Don't get killed before you're useful.",
                        "end": True,
                    },
                },
            },
        },
    ],

    # ── Scout Mira — witnessed Maren's approach to the Spire ────────────────
    "ambient_scout": [
        {
            "conditions": [{"flag": "maren.left", "op": "==", "value": True}],
            "tree": {
                "id": "scout_mira_maren_witness",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Scout Mira",
                        "text": "I watched that scholar — Maren — walk toward the Spire "
                                "about a week ago.\n"
                                "She didn't run. She didn't look scared. "
                                "She walked like someone who'd already made their peace "
                                "and was just finishing the last errand.",
                        "choices": [
                            {"text": "Did she say anything before she went?",
                             "next": "last_words"},
                            {"text": "What happened at the Spire entrance?",
                             "next": "entrance"},
                            {"text": "Thank you.", "next": "bye"},
                        ],
                    },
                    "last_words": {
                        "speaker": "Scout Mira",
                        "text": "She stopped at the edge of the Ashlands fog and looked back. "
                                "I thought she was going to change her mind.\n"
                                "She just said: 'Tell them the wards are still up.' "
                                "Then she walked into the fog and I lost sight of her.",
                        "next": "start",
                    },
                    "entrance": {
                        "speaker": "Scout Mira",
                        "text": "The Spire gate opened for her. Just — opened. "
                                "No key, no force. Like it knew her.\n"
                                "The wards didn't pulse or react. "
                                "Whatever's in there, it let her in willingly.\n"
                                "That worries me more than if it had fought her.",
                        "next": "start",
                    },
                    "bye": {
                        "speaker": "Scout Mira",
                        "text": "Bring her back if you can. "
                                "She had kind eyes, for someone carrying that much.",
                        "end": True,
                    },
                },
            },
        },
        {
            "conditions": [],
            "tree": {
                "id": "scout_mira_default",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Scout Mira",
                        "text": "Just back from the Ashlands perimeter. "
                                "The fog is pushing further south every week.\n"
                                "We can't hold the line forever. "
                                "Someone needs to stop it at the source.",
                        "choices": [
                            {"text": "What's the perimeter situation?", "next": "perimeter"},
                            {"text": "Stay safe.", "next": "bye"},
                        ],
                    },
                    "perimeter": {
                        "speaker": "Scout Mira",
                        "text": "We've lost three miles of ground since last month. "
                                "The Fading corrupts everything it touches — "
                                "animals, plants, even the stones start to shimmer.\n"
                                "The Spire is the source. Everyone knows it. "
                                "Nobody's done anything about it yet.",
                        "next": "bye",
                    },
                    "bye": {
                        "speaker": "Scout Mira",
                        "text": "Eyes open out there.",
                        "end": True,
                    },
                },
            },
        },
    ],

    # ── Ambient rebel fighter — Holdfast background ──────────────────────────
    "ambient_rebel": [
        {
            "conditions": [],
            "tree": {
                "id": "ambient_rebel_default",
                "loop": True,
                "nodes": {
                    "start": {
                        "speaker": "Rebel Fighter",
                        "text": "We didn't choose this fight. The Fading chose it for us.\n"
                                "But here we are.",
                        "choices": [
                            {"text": "How long have you been here?", "next": "how_long"},
                            {"text": "Stay strong.", "next": "bye"},
                        ],
                    },
                    "how_long": {
                        "speaker": "Rebel Fighter",
                        "text": "Six months. Used to be a farmer in the eastern Ashlands. "
                                "My fields faded in a night — just gone, "
                                "like they'd never been there.\n"
                                "Sarev found me on the road and gave me a blade. "
                                "Here I am.",
                        "next": "bye",
                    },
                    "bye": {
                        "speaker": "Rebel Fighter",
                        "text": "Kill whatever's in that tower. "
                                "Do it for all of us.",
                        "end": True,
                    },
                },
            },
        },
    ],

}

NPC_DIALOGUES.update(_TRAINER_DIALOGUES)


# ══════════════════════════════════════════════════════════════
#  DIALOGUE EXIT PATCHER — added Session 19
#  Adds a "Farewell." exit option to every choice node that
#  had choices but no exit path (next=None).  Runs once at
#  module load.  Do not remove — prevents dialogue dead-ends.
# ══════════════════════════════════════════════════════════════
def _patch_dialogue_exits(dialogues):
    _farewell = {"text": "Farewell.", "next": None}
    for branches in dialogues.values():
        for branch in branches:
            nodes = branch.get("tree", {}).get("nodes", {})
            for node in nodes.values():
                choices = node.get("choices")
                if choices and not any(c.get("next") is None for c in choices):
                    choices.append(dict(_farewell))

_patch_dialogue_exits(NPC_DIALOGUES)
