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
    "main_hearthstone_3": {
        "name": "Fire and Salt",
        "description": "The third Hearthstone lies somewhere in the Dragon's Tooth archipelago. "
                       "Arrange passage from Saltmere and survive whatever waits there.",
        "act": 2,
    },
    "main_thornhaven": {
        "name": "Audience with the Governor",
        "description": "Travel to Thornhaven and secure the support of the Imperial Governor. "
                       "His archives may hold the locations of the remaining Hearthstones.",
        "act": 2,
    },
    "main_maren_truth": {
        "name": "The Scholar's Secret",
        "description": "Court Mage Sira has revealed that Maren is the daughter of Valdris, "
                       "the Traitor Warden. Confront Maren about what she truly intends "
                       "to do with the Hearthstones.",
        "act": 2,
    },
    "side_guild_initiation": {
        "name": "Proving Ground",
        "description": "Guildmaster Sable of the Saltmere Thieves' Guild wants proof "
                       "of your capabilities before offering real work.",
        "act": 2,
    },
    "side_academy_research": {
        "name": "Data for the Archmage",
        "description": "Archmage Solen wants ley line readings from three locations "
                       "near active Fading zones. Dangerous work, but the Academy pays well.",
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
                        "text": "My daughter's little helpers. She sent you ahead, didn't she? "
                                "To weaken me before she arrives. I taught her that. "
                                "I am almost proud.",
                        "choices": [
                            {"text": "Maren didn't send us. We're stopping you both if we have to.", "next": "defiant"},
                            {"text": "What are you trying to do?", "next": "plan"},
                            {"text": "You're the one who caused all of this.", "next": "accuse"},
                        ],
                    },
                    "defiant": {
                        "speaker": "Valdris",
                        "text": "Brave. Foolish. You have no idea what you're standing between. "
                                "The Shadow Realm is not the enemy — it is the solution. "
                                "The Fading is not decay. It is transformation. "
                                "What I am doing will save this world. "
                                "You are too small to see it.",
                        "next": "response",
                    },
                    "plan": {
                        "speaker": "Valdris",
                        "text": "I am completing what the original Wardens were too frightened "
                                "to attempt. A true merger. Not a barrier between worlds — "
                                "a bridge. Shadow and light. Unified. Eternal. "
                                "No more Fading. No more dissolution. "
                                "One world, stronger than either alone.",
                        "on_enter": [{"action": "discover_lore", "lore": "valdris_true_plan"}],
                        "next": "response",
                    },
                    "accuse": {
                        "speaker": "Valdris",
                        "text": "Caused it. Yes. The wards were a cage. What I 'caused' "
                                "was the first honest look at what lies beyond them. "
                                "The Fading is the natural result of a world that has been "
                                "starved of Shadow for a thousand years. I gave it what it needed.",
                        "next": "response",
                    },
                    "response": {
                        "speaker": "Valdris",
                        "text": "You cannot stop the process now. Not without the Hearthstones. "
                                "And if you have them — then you understand exactly what I mean "
                                "to do with them. Let us see if you have the will to use them "
                                "differently.",
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
    "saltmere":    ["guildmaster_sable", "tide_priest_oran"],
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
        "boss_dialogue": None,
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
