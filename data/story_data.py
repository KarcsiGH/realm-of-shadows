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
    "main_meet_maren": {
        "name": "The Scholar's Plea",
        "description": "Meet Maren at the tavern in Briarhollow to learn about the Fading.",
        "act": 1,
    },
    "main_goblin_warren": {
        "name": "The Goblin Problem",
        "description": "Investigate the Goblin Warren east of Briarhollow. "
                       "The goblins have been raiding farms, but Maren suspects "
                       "there's more to it.",
        "act": 1,
    },
    "main_hearthstone_1": {
        "name": "The First Hearthstone",
        "description": "Explore the Abandoned Mine and recover the first Hearthstone. "
                       "Maren believes a dwarven Warden once guarded it.",
        "act": 1,
    },
    "main_spiders_nest": {
        "name": "Unnatural Growth",
        "description": "The Spider's Nest is filled with creatures mutated by the Fading. "
                       "Investigate the source of the corruption.",
        "act": 1,
    },
    "side_wolf_pelts": {
        "name": "Pelts for the Tanner",
        "description": "Collect 5 wolf pelts and bring them to the tanner in Briarhollow.",
        "act": 1,
    },
    "side_missing_patrol": {
        "name": "The Missing Patrol",
        "description": "Captain Aldric's patrol never returned from the eastern road. "
                       "Find out what happened to them.",
        "act": 1,
    },
    "main_ashenmoor": {
        "name": "Secrets of Ashenmoor",
        "description": "The Ruins of Ashenmoor hold the truth about why the wards failed. "
                       "Maren insists the answers are buried there.",
        "act": 2,
    },
    "main_hearthstone_2": {
        "name": "The Sunken Stone",
        "description": "Descend into the Sunken Crypt to recover the second Hearthstone "
                       "from the undead Warden who guards it.",
        "act": 2,
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

    # ─── Dungeon NPCs ───
    "grak": {
        "name": "Grak the Goblin King",
        "title": "King of the Warren",
        "location": "goblin_warren",
        "portrait_color": (100, 140, 60),  # goblin green
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
}


# ═══════════════════════════════════════════════════════════════
#  TOWN NPC ASSIGNMENTS
#  Maps town_id → list of NPC IDs available there
# ═══════════════════════════════════════════════════════════════

TOWN_NPCS = {
    "briarhollow": ["maren", "captain_rowan", "bess"],
    "woodhaven": ["elder_theron", "sylla"],
    "ironhearth": ["forgemaster_dunn", "merchant_kira"],
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
                "lore_id": None,
            },
        ],
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
    },
    "ashenmoor": {
        "floor_messages": {
            1: "The ruins still smolder with a heat that has no source. "
               "This place was destroyed by magic, not fire.",
            2: "Faded murals line the halls — scenes of Wardens performing rituals. "
               "One figure stands apart from the others. His hands glow with shadow.",
            3: "You find a sealed chamber. The door bears the mark of the Wardens, "
               "broken deliberately. Someone wanted what was inside.",
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
            },
        ],
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
        "boss_dialogue": None,  # Boss speaks via floor_message on floor 6
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
