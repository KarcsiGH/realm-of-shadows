"""
Realm of Shadows — Life Path Event Data
Complete branching event tree for character generation.

Structure:
  Each event is a dict with:
    id          - unique string key
    phase       - "childhood", "youth", "adult"
    slot        - 1-3 within phase (1=event1, 2=event2, 3=defining_moment)
    stream      - primary stream ("rural","urban","military","noble","any")
    title       - short title shown to player
    text        - narrative paragraph
    stats       - dict of stat bonuses
    backstory   - sentence fragment for compiled backstory
    random      - optional dict with "chance" (0-1), "success"/"fail" dicts
                  each with "text", "stats", "backstory"
    unlocks     - list of event IDs this opens (crossovers)
    requires    - list of event IDs (any one must be in history) or [] for default
    tags        - list of string tags for filtering
"""

# ════════════════════════════════════════════════════════════════
# PHASE 1: CHILDHOOD
# ════════════════════════════════════════════════════════════════

# ── Slot 1: Origin ─────────────────────────────────────────────

ORIGINS = [
    {
        "id": "origin_rural",
        "phase": "childhood", "slot": 1, "stream": "rural",
        "title": "A Farming Village on the Frontier",
        "text": (
            "You grew up in a small village at the edge of the known lands. "
            "Days were spent hauling water, mending fences, and chasing goats "
            "through muddy fields. The work was hard, but the land was honest. "
            "At night, the elders told stories of what lurked beyond the treeline."
        ),
        "stats": {"STR": 1, "CON": 2, "WIS": 1},
        "backstory": "Born to a farming family on the frontier,",
        "tags": ["rural"],
    },
    {
        "id": "origin_urban",
        "phase": "childhood", "slot": 1, "stream": "urban",
        "title": "The Crowded Streets of a Port City",
        "text": (
            "You grew up in the tangled streets of Saltmere, where the air "
            "smelled of fish, tar, and opportunity. Every alley was a shortcut, "
            "every market stall a lesson in watching and waiting. You learned "
            "early that the quick eat and the slow go hungry."
        ),
        "stats": {"DEX": 2, "INT": 1, "WIS": 1},
        "backstory": "Raised in the crowded port city of Saltmere,",
        "tags": ["urban"],
    },
    {
        "id": "origin_military",
        "phase": "childhood", "slot": 1, "stream": "military",
        "title": "A Garrison Town in the Borderlands",
        "text": (
            "You grew up in the shadow of fortress walls, where soldiers drilled "
            "at dawn and trumpets marked the hours. Your parents served the "
            "garrison — whether as soldiers, smiths, or cooks, the military "
            "rhythm shaped your days. You learned to stand straight before "
            "you learned to read."
        ),
        "stats": {"STR": 2, "CON": 1, "PIE": 1},
        "backstory": "Raised in a borderlands garrison town,",
        "tags": ["military"],
    },
    {
        "id": "origin_noble",
        "phase": "childhood", "slot": 1, "stream": "noble",
        "title": "A Noble Estate in the Heartlands",
        "text": (
            "You grew up behind high stone walls, surrounded by servants, "
            "tutors, and expectations. Your family's name carried weight — "
            "and burden. Meals were formal, lessons were strict, and every "
            "interaction was a small performance. You learned manners before "
            "you learned to play."
        ),
        "stats": {"INT": 2, "PIE": 1, "WIS": 1},
        "backstory": "Born into a noble family of the Heartlands,",
        "tags": ["noble"],
    },
]

# ── Slot 2: Childhood Event ───────────────────────────────────

CHILDHOOD_EVENTS = [
    # ── Rural ──
    {
        "id": "rc2_tend_fields",
        "phase": "childhood", "slot": 2, "stream": "rural",
        "title": "You Helped Tend the Animals and Fields",
        "text": (
            "From the moment you could carry a bucket, you worked. Feeding "
            "livestock before dawn, pulling weeds until your hands cracked, "
            "hauling harvest to the storehouse. It was grueling, but your "
            "body grew strong and your patience deep."
        ),
        "stats": {"STR": 1, "CON": 2},
        "backstory": "you spent your childhood working the land.",
        "requires": ["origin_rural"],
        "tags": ["rural", "labor"],
    },
    {
        "id": "rc2_wandered_woods",
        "phase": "childhood", "slot": 2, "stream": "rural",
        "title": "You Wandered the Woods Alone for Hours",
        "text": (
            "While other children played in the village square, you slipped "
            "into the forest. You learned which berries were safe, where the "
            "deer trails led, how to read weather in the leaves. The woods "
            "felt more like home than home did."
        ),
        "stats": {"WIS": 2, "DEX": 1},
        "backstory": "you spent your days exploring the deep woods alone.",
        "requires": ["origin_rural"],
        "unlocks": ["urban_youth"],  # could run away later
        "tags": ["rural", "nature", "solitary"],
    },
    {
        "id": "rc2_stranger_taught",
        "phase": "childhood", "slot": 2, "stream": "rural",
        "title": "A Stranger Taught You Something",
        "text": (
            "A wandering traveler sheltered in your village for a season. "
            "They spoke of distant cities and strange ideas. They taught you "
            "letters, or card tricks, or a fighting stance — something that "
            "cracked open your small world."
        ),
        "stats": {"INT": 2, "DEX": 1},
        "backstory": "a passing stranger opened your eyes to the wider world.",
        "requires": ["origin_rural"],
        "unlocks": ["noble_youth", "military_youth"],
        "tags": ["rural", "education", "outsider"],
    },

    # ── Urban ──
    {
        "id": "uc2_street_gang",
        "phase": "childhood", "slot": 2, "stream": "urban",
        "title": "You Ran with a Gang of Street Kids",
        "text": (
            "There was safety in numbers and mischief in plenty. You learned "
            "to climb walls, squeeze through windows, and vanish into crowds. "
            "Loyalty was everything — betray the gang and you'd sleep alone."
        ),
        "stats": {"DEX": 2, "STR": 1},
        "backstory": "you ran with a gang of street children,",
        "requires": ["origin_urban"],
        "tags": ["urban", "crime", "social"],
    },
    {
        "id": "uc2_worked_shop",
        "phase": "childhood", "slot": 2, "stream": "urban",
        "title": "You Worked in a Shop or Tavern",
        "text": (
            "A merchant or innkeeper took you on — sweeping floors, carrying "
            "crates, serving customers. You learned to count coins, read "
            "people's faces, and keep your mouth shut when it mattered."
        ),
        "stats": {"INT": 1, "WIS": 1, "PIE": 1},
        "backstory": "you worked in a merchant's shop, learning trade and people,",
        "requires": ["origin_urban"],
        "unlocks": ["noble_youth"],
        "tags": ["urban", "honest", "trade"],
    },
    {
        "id": "uc2_begged",
        "phase": "childhood", "slot": 2, "stream": "urban",
        "title": "You Begged on the Streets",
        "text": (
            "No one looked after you. You slept in doorways, ate what you "
            "could find or charm out of strangers, and learned that pity is "
            "a resource like any other. The world was brutal, but you were stubborn."
        ),
        "stats": {"CON": 2, "WIS": 1},
        "backstory": "you survived alone on the streets, begging and scrounging,",
        "requires": ["origin_urban"],
        "tags": ["urban", "poverty", "survival"],
    },

    # ── Military ──
    {
        "id": "mc2_trained_garrison",
        "phase": "childhood", "slot": 2, "stream": "military",
        "title": "You Trained with the Garrison Children",
        "text": (
            "The soldiers let the children drill alongside them — wooden "
            "swords, formation marching, basic commands. Most kids treated "
            "it as a game. You took it seriously."
        ),
        "stats": {"STR": 2, "CON": 1},
        "backstory": "you trained alongside soldiers from a young age,",
        "requires": ["origin_military"],
        "tags": ["military", "combat", "discipline"],
    },
    {
        "id": "mc2_infirmary",
        "phase": "childhood", "slot": 2, "stream": "military",
        "title": "You Spent Time in the Garrison Infirmary",
        "text": (
            "Whether from illness or curiosity, you ended up helping the "
            "healers. You learned to clean wounds, mix poultices, and sit "
            "with the dying. It changed how you saw the cost of war."
        ),
        "stats": {"WIS": 2, "PIE": 1},
        "backstory": "you helped the garrison healers tend the wounded,",
        "requires": ["origin_military"],
        "tags": ["military", "healing", "spiritual"],
    },
    {
        "id": "mc2_veteran_stories",
        "phase": "childhood", "slot": 2, "stream": "military",
        "title": "You Befriended a Veteran",
        "text": (
            "An old soldier, scarred and half-blind, sat on the same bench "
            "every evening. You brought them food and they gave you stories — "
            "battles, betrayals, distant lands, hard truths about glory and death."
        ),
        "stats": {"WIS": 1, "INT": 1, "CON": 1},
        "backstory": "an old veteran's stories filled your imagination,",
        "requires": ["origin_military"],
        "tags": ["military", "wisdom", "stories"],
    },

    # ── Noble ──
    {
        "id": "nc2_excelled_studies",
        "phase": "childhood", "slot": 2, "stream": "noble",
        "title": "You Excelled at Your Studies",
        "text": (
            "Languages, history, mathematics, natural philosophy — your tutors "
            "praised your sharp mind. Your family expected nothing less, but "
            "privately, you enjoyed the learning for its own sake."
        ),
        "stats": {"INT": 2, "WIS": 1},
        "backstory": "you excelled in your studies under private tutors,",
        "requires": ["origin_noble"],
        "tags": ["noble", "scholarly", "intellectual"],
    },
    {
        "id": "nc2_house_guard",
        "phase": "childhood", "slot": 2, "stream": "noble",
        "title": "You Trained with the House Guard",
        "text": (
            "Against your family's wishes — or perhaps at their insistence — "
            "you spent afternoons in the training yard. The master-at-arms "
            "didn't care about your bloodline, only whether you could hold "
            "a blade properly."
        ),
        "stats": {"STR": 2, "DEX": 1},
        "backstory": "you trained in arms with the household guard,",
        "requires": ["origin_noble"],
        "unlocks": ["military_youth"],
        "tags": ["noble", "combat", "discipline"],
    },
    {
        "id": "nc2_snuck_out",
        "phase": "childhood", "slot": 2, "stream": "noble",
        "title": "You Snuck Out to Play with Common Children",
        "text": (
            "The estate was suffocating. You climbed the garden wall and found "
            "a different world — rougher, louder, more alive. You learned to "
            "hide your accent, throw a punch, and keep secrets from your parents."
        ),
        "stats": {"DEX": 2, "CON": 1},
        "backstory": "you escaped the estate walls to play with common children,",
        "requires": ["origin_noble"],
        "unlocks": ["urban_youth"],
        "tags": ["noble", "rebellious", "street"],
    },
]

# ── Slot 3: Childhood Defining Moment ─────────────────────────

CHILDHOOD_DEFINING = [
    # ── Rural ──
    {
        "id": "rdm_forest_fire",
        "phase": "childhood", "slot": 3, "stream": "rural",
        "title": "The Forest Fire",
        "text": (
            "A wildfire swept through the valley. While adults panicked, you "
            "helped herd animals to safety, carried water, and guided younger "
            "children to the river. When it was over, the village elder said "
            "you had the heart of a protector."
        ),
        "stats": {"CON": 2, "WIS": 1, "STR": 1},
        "backstory": "When wildfire threatened the village, you helped save lives.",
        "requires": ["origin_rural"],
        "tags": ["rural", "heroic", "nature"],
    },
    {
        "id": "rdm_found_fae",
        "phase": "childhood", "slot": 3, "stream": "rural",
        "title": "Found by the Fae",
        "text": (
            "You wandered too deep into the woods one twilight and stumbled "
            "into a ring of pale mushrooms. Strange lights danced. Voices "
            "whispered things you almost understood. You were returned to the "
            "village edge at dawn with no memory of the night — but something "
            "had changed inside you."
        ),
        "stats": {"WIS": 2, "PIE": 2},
        "backstory": "One night the fae found you in the woods, and you were never quite the same.",
        "requires": ["origin_rural"],
        "tags": ["rural", "mystical", "spiritual"],
    },
    {
        "id": "rdm_wolf_attack",
        "phase": "childhood", "slot": 3, "stream": "rural",
        "title": "The Wolf Attack",
        "text": (
            "A pack of wolves came down from the mountains in a hard winter. "
            "They killed livestock and circled the village at night. When one "
            "cornered you behind the barn, you fought it off with a pitchfork."
        ),
        "stats": {"STR": 2, "CON": 1, "DEX": 1},
        "backstory": "You fought off a wolf as a child and carry the scar to prove it.",
        "requires": ["origin_rural"],
        "random": {
            "chance": 0.6,
            "success": {
                "text": "You drove the wolf away and stood bloodied but triumphant.",
                "stats": {},
                "backstory": "",
            },
            "fail": {
                "text": "The wolf's teeth found your arm before you drove it off. The scar never fully healed, but neither did your fear.",
                "stats": {"CON": 1},
                "backstory": " The wound left a lasting scar.",
            },
        },
        "tags": ["rural", "combat", "survival"],
    },

    # ── Urban ──
    {
        "id": "udm_caught_mercy",
        "phase": "childhood", "slot": 3, "stream": "urban",
        "title": "Caught Stealing — and Shown Mercy",
        "text": (
            "You lifted a purse from the wrong person — a retired adventurer "
            "who caught your wrist like a vice. But instead of turning you in, "
            "they bought you a meal and told you there were better uses for "
            "quick hands. You never forgot it."
        ),
        "stats": {"DEX": 1, "WIS": 2, "PIE": 1},
        "backstory": "A stranger's mercy after catching you stealing changed something in you.",
        "requires": ["origin_urban"],
        "tags": ["urban", "crime", "redemption"],
    },
    {
        "id": "udm_witnessed",
        "phase": "childhood", "slot": 3, "stream": "urban",
        "title": "Witnessed Something You Shouldn't Have",
        "text": (
            "Down a midnight alley, you saw something terrible — a murder, a "
            "dark ritual, a deal between people who wear respectable faces by "
            "day. You ran. You hid. You never told anyone. But you've been "
            "watching more carefully ever since."
        ),
        "stats": {"INT": 2, "WIS": 1, "DEX": 1},
        "backstory": "You witnessed something terrible in the city's shadows and learned to watch carefully.",
        "requires": ["origin_urban"],
        "tags": ["urban", "dark", "awareness"],
    },
    {
        "id": "udm_saved_stranger",
        "phase": "childhood", "slot": 3, "stream": "urban",
        "title": "Saved by a Stranger",
        "text": (
            "You were cornered — by older kids, by a merchant you'd robbed, "
            "by something worse. A stranger intervened, someone powerful and "
            "strange. They said nothing, handled the situation, and vanished. "
            "You've been trying to be worthy of that rescue ever since."
        ),
        "stats": {"PIE": 2, "CON": 1, "STR": 1},
        "backstory": "A mysterious stranger saved your life, and you've tried to be worthy of it since.",
        "requires": ["origin_urban"],
        "tags": ["urban", "faith", "debt"],
    },

    # ── Military ──
    {
        "id": "mdm_border_raid",
        "phase": "childhood", "slot": 3, "stream": "military",
        "title": "The Border Raid",
        "text": (
            "Raiders struck the garrison at night. In the chaos, you grabbed "
            "a real sword for the first time. You didn't fight well — you were "
            "terrified — but you stood your ground when others ran. "
            "The commander noticed."
        ),
        "stats": {"STR": 1, "CON": 2, "PIE": 1},
        "backstory": "When raiders attacked the garrison, you stood your ground despite your fear.",
        "requires": ["origin_military"],
        "tags": ["military", "combat", "courage"],
    },
    {
        "id": "mdm_friend_killed",
        "phase": "childhood", "slot": 3, "stream": "military",
        "title": "A Friend Was Killed",
        "text": (
            "Another garrison child, your closest friend, was killed — in a "
            "raid, by a training accident, or by illness the healers couldn't "
            "stop. You learned what loss means before you were old enough "
            "to understand it."
        ),
        "stats": {"WIS": 2, "CON": 1, "PIE": 1},
        "backstory": "The death of your closest friend taught you about loss before you were ready.",
        "requires": ["origin_military"],
        "tags": ["military", "loss", "emotional"],
    },
    {
        "id": "mdm_hidden_passage",
        "phase": "childhood", "slot": 3, "stream": "military",
        "title": "You Found a Hidden Passage",
        "text": (
            "Exploring the old fortress, you discovered a sealed room behind "
            "a crumbling wall. Inside: old weapons, strange books, a map to "
            "somewhere. You had to decide — tell the commander, or keep "
            "the secret."
        ),
        "stats": {"INT": 2, "DEX": 1, "WIS": 1},
        "backstory": "You found a hidden chamber in the old fortress,",
        "requires": ["origin_military"],
        "random": {
            "chance": 0.5,
            "success": {
                "text": "You told the commander, who rewarded your honesty and let you keep a small token from the room.",
                "stats": {"PIE": 1},
                "backstory": " and honestly reported your discovery.",
            },
            "fail": {
                "text": "You kept the secret, returning alone to study the strange books by candlelight.",
                "stats": {"INT": 1},
                "backstory": " and kept its secrets for yourself.",
            },
        },
        "tags": ["military", "discovery", "choice"],
    },

    # ── Noble ──
    {
        "id": "ndm_family_betrayed",
        "phase": "childhood", "slot": 3, "stream": "noble",
        "title": "Your Family Was Betrayed",
        "text": (
            "A rival house moved against your family — politically, financially, "
            "or with steel in the night. You saw your parents humbled, your "
            "home threatened. It taught you that power is fragile and enemies "
            "are patient."
        ),
        "stats": {"INT": 2, "WIS": 1, "CON": 1},
        "backstory": "When your family was betrayed by rivals, you learned that power is fragile.",
        "requires": ["origin_noble"],
        "tags": ["noble", "political", "loss"],
    },
    {
        "id": "ndm_stood_up",
        "phase": "childhood", "slot": 3, "stream": "noble",
        "title": "You Stood Up to Your Parents",
        "text": (
            "There was a moment — a punishment you refused to accept, a cruelty "
            "to a servant you wouldn't allow, a path they chose for you that "
            "you rejected. You defied them and accepted the consequences. It "
            "was the first time you felt like yourself."
        ),
        "stats": {"PIE": 2, "STR": 1, "WIS": 1},
        "backstory": "You defied your parents over a matter of principle and bore the consequences.",
        "requires": ["origin_noble"],
        "tags": ["noble", "rebellion", "character"],
    },
    {
        "id": "ndm_servant_taught",
        "phase": "childhood", "slot": 3, "stream": "noble",
        "title": "A Servant Taught You the Real World",
        "text": (
            "Your nursemaid, your stable hand, a kitchen cook — someone beneath "
            "your family's notice became the most important person in your life. "
            "They taught you things no tutor would: how common people live, what "
            "hunger feels like, why walls exist from both sides."
        ),
        "stats": {"WIS": 2, "CON": 1, "PIE": 1},
        "backstory": "A humble servant showed you truths your tutors never would.",
        "requires": ["origin_noble"],
        "tags": ["noble", "empathy", "wisdom"],
    },
]


# ════════════════════════════════════════════════════════════════
# PHASE 2: YOUTH
# ════════════════════════════════════════════════════════════════

# ── Slot 4: Youth Event 1 ─────────────────────────────────────

YOUTH_EVENTS_1 = [
    # ── Rural ──
    {
        "id": "ry1_apprentice",
        "phase": "youth", "slot": 4, "stream": "rural",
        "title": "Apprenticed to a Local Trade",
        "text": (
            "The blacksmith, the carpenter, the herbalist — someone in the "
            "village took you on as an apprentice. The work was specific and "
            "demanding, but you developed real skill."
        ),
        "stats": {"STR": 1, "INT": 1, "CON": 1},
        "backstory": "As a youth you apprenticed to a village tradesperson.",
        "requires": ["origin_rural"],
        "tags": ["rural", "trade", "labor"],
    },
    {
        "id": "ry1_hunter",
        "phase": "youth", "slot": 4, "stream": "rural",
        "title": "Became a Hunter and Tracker",
        "text": (
            "With the older hunters, you ranged further from the village than "
            "you'd ever been. You learned to read tracks, set snares, move "
            "silently through undergrowth, and kill cleanly."
        ),
        "stats": {"DEX": 2, "WIS": 1},
        "backstory": "You took up hunting and learned to track through the wilds.",
        "requires": ["origin_rural"],
        "tags": ["rural", "hunting", "nature"],
    },
    {
        "id": "ry1_village_attacked",
        "phase": "youth", "slot": 4, "stream": "rural",
        "title": "The Village Was Attacked",
        "text": (
            "Bandits, or raiders, or something worse came to your village. "
            "Whether you fought, hid, or ran, nothing was the same afterward. "
            "Some people were taken. Some didn't come back."
        ),
        "stats": {"CON": 1, "STR": 1, "WIS": 1},
        "backstory": "Your village was attacked and nothing was ever the same.",
        "requires": ["origin_rural"],
        "unlocks": ["military_youth", "urban_youth"],
        "tags": ["rural", "violence", "turning_point"],
    },

    # ── Urban ──
    {
        "id": "uy1_fence",
        "phase": "youth", "slot": 4, "stream": "urban",
        "title": "Worked for a Fence or Smuggler",
        "text": (
            "You graduated from petty theft to real criminal enterprise. A "
            "fence taught you the value of goods, how to move stolen "
            "merchandise, and — most importantly — who not to cross."
        ),
        "stats": {"INT": 2, "DEX": 1},
        "backstory": "You worked for a smuggler, learning the value of secrets and goods.",
        "requires": ["origin_urban"],
        "tags": ["urban", "crime", "trade"],
    },
    {
        "id": "uy1_thieves_guild",
        "phase": "youth", "slot": 4, "stream": "urban",
        "title": "Joined a Thieves' Guild as Apprentice",
        "text": (
            "The guild found you — or you found them. Either way, you were "
            "tested, accepted, and trained. Lockpicking, pickpocketing, "
            "surveillance, escape routes. Professional crime."
        ),
        "stats": {"DEX": 2, "INT": 1},
        "backstory": "The thieves' guild took you in and trained you in their craft.",
        "requires": ["origin_urban"],
        "tags": ["urban", "crime", "guild"],
    },
    {
        "id": "uy1_went_straight",
        "phase": "youth", "slot": 4, "stream": "urban",
        "title": "Tried to Go Straight",
        "text": (
            "You got tired of looking over your shoulder. A merchant, a "
            "shipwright, a baker — someone gave you honest work. The pay "
            "was worse but the sleep was better."
        ),
        "stats": {"CON": 1, "PIE": 1, "STR": 1},
        "backstory": "You tried honest work for a time, seeking a different life.",
        "requires": ["origin_urban"],
        "unlocks": ["military_youth", "noble_youth"],
        "tags": ["urban", "honest", "change"],
    },

    # ── Military ──
    {
        "id": "my1_cadet",
        "phase": "youth", "slot": 4, "stream": "military",
        "title": "Formally Enlisted as a Cadet",
        "text": (
            "Old enough now to join properly, you entered training. Real "
            "weapons, real formations, real consequences for failure. The "
            "drill instructors didn't care about your childhood; they cared "
            "about what you could become."
        ),
        "stats": {"STR": 2, "CON": 1},
        "backstory": "You formally enlisted and endured the rigors of cadet training.",
        "requires": ["origin_military"],
        "tags": ["military", "training", "discipline"],
    },
    {
        "id": "my1_scout_duty",
        "phase": "youth", "slot": 4, "stream": "military",
        "title": "Assigned to Scout Duty",
        "text": (
            "They needed young eyes and quick legs on the frontier patrols. "
            "You spent weeks in the wilderness between forts, watching for "
            "threats, living off the land, reporting what you found."
        ),
        "stats": {"DEX": 1, "WIS": 2},
        "backstory": "You served as a frontier scout, patrolling the wild borderlands.",
        "requires": ["origin_military"],
        "unlocks": ["rural_youth"],
        "tags": ["military", "scouting", "nature"],
    },
    {
        "id": "my1_quartermaster",
        "phase": "youth", "slot": 4, "stream": "military",
        "title": "Served in the Quartermaster's Office",
        "text": (
            "Not every soldier fights. You learned logistics, supply chains, "
            "record keeping, and the art of making things work behind the "
            "scenes. Unglamorous, but you understood how armies actually function."
        ),
        "stats": {"INT": 2, "WIS": 1},
        "backstory": "You served in logistics, learning how armies truly operate.",
        "requires": ["origin_military"],
        "tags": ["military", "logistics", "intellectual"],
    },

    # ── Noble ──
    {
        "id": "ny1_page",
        "phase": "youth", "slot": 4, "stream": "noble",
        "title": "Sent to Court as a Page",
        "text": (
            "Your family sent you to serve a higher-ranking noble. You carried "
            "messages, observed politics, learned etiquette, and discovered "
            "that smiles could be weapons sharper than swords."
        ),
        "stats": {"INT": 1, "PIE": 2},
        "backstory": "You served as a page at court, learning politics and intrigue.",
        "requires": ["origin_noble"],
        "tags": ["noble", "political", "social"],
    },
    {
        "id": "ny1_military_academy",
        "phase": "youth", "slot": 4, "stream": "noble",
        "title": "Sent to a Military Academy",
        "text": (
            "Your family wanted you hardened. The academy was cold, strict, "
            "and competitive. Nobility meant nothing there — only performance. "
            "You learned to fight, to lead, and to endure."
        ),
        "stats": {"STR": 2, "CON": 1},
        "backstory": "Your family sent you to a military academy where nobility meant nothing.",
        "requires": ["origin_noble"],
        "unlocks": ["military_adult"],
        "tags": ["noble", "military", "discipline"],
    },
    {
        "id": "ny1_ran_away",
        "phase": "youth", "slot": 4, "stream": "noble",
        "title": "Ran Away from Home",
        "text": (
            "You couldn't take it anymore — the expectations, the politics, "
            "the gilded cage. You fled with nothing but the clothes on your "
            "back. For the first time, you were nobody. It was terrifying "
            "and exhilarating."
        ),
        "stats": {"DEX": 1, "CON": 1, "WIS": 1},
        "backstory": "You ran away from your noble family, seeking freedom,",
        "requires": ["origin_noble"],
        "unlocks": ["urban_youth", "rural_youth"],
        "tags": ["noble", "rebellion", "freedom"],
    },
]

# ── Slot 5: Youth Event 2 ─────────────────────────────────────

YOUTH_EVENTS_2 = [
    # ── Rural ──
    {
        "id": "ry2_traveled_town",
        "phase": "youth", "slot": 5, "stream": "rural",
        "title": "Traveled to a Nearby Town",
        "text": (
            "The village sent you to trade, or you went on your own. The town "
            "was overwhelming — so many people, so much noise, so many things "
            "you'd never seen. You came back changed, restless."
        ),
        "stats": {"INT": 1, "WIS": 1},
        "backstory": "A trip to town showed you how much world existed beyond the village.",
        "requires": ["origin_rural"],
        "unlocks": ["urban_adult"],
        "tags": ["rural", "travel", "awakening"],
    },
    {
        "id": "ry2_hermit_student",
        "phase": "youth", "slot": 5, "stream": "rural",
        "title": "A Hermit Took You as a Student",
        "text": (
            "Deep in the hills, a recluse — a former monk, a hedge wizard, "
            "an old druid — agreed to teach you. The lessons were strange: "
            "meditation, herb lore, reading the wind. Half of it made no "
            "sense. Years later, all of it would."
        ),
        "stats": {"WIS": 2, "PIE": 1},
        "backstory": "A hermit in the hills taught you strange and ancient things.",
        "requires": ["origin_rural"],
        "tags": ["rural", "mystical", "training"],
    },
    {
        "id": "ry2_militia",
        "phase": "youth", "slot": 5, "stream": "rural",
        "title": "You Joined the Village Militia",
        "text": (
            "After the attacks — or in preparation for the next one — you "
            "joined the village militia. Farmers with spears, but you drilled "
            "seriously. An old soldier who'd retired to the village taught "
            "you what he knew."
        ),
        "stats": {"STR": 1, "CON": 1, "DEX": 1},
        "backstory": "You joined the village militia and learned the basics of real combat.",
        "requires": ["origin_rural"],
        "unlocks": ["military_adult"],
        "tags": ["rural", "military", "defense"],
    },

    # ── Urban ──
    {
        "id": "uy2_went_to_sea",
        "phase": "youth", "slot": 5, "stream": "urban",
        "title": "You Went to Sea as Cabin Boy/Girl",
        "text": (
            "The docks were always calling. A captain needed young hands. The "
            "ship was filthy, the crew was rough, and the sea was merciless — "
            "but you saw places you'd only heard of in drunken sailors' tales."
        ),
        "stats": {"CON": 2, "DEX": 1},
        "backstory": "You went to sea, learning the sailor's hard life.",
        "requires": ["origin_urban"],
        "tags": ["urban", "sea", "adventure"],
    },
    {
        "id": "uy2_got_caught",
        "phase": "youth", "slot": 5, "stream": "urban",
        "title": "You Got Caught and Did Time",
        "text": (
            "The law caught up. Months in a cell, or a work camp, or indentured "
            "to a merchant as punishment. It was miserable, but you survived "
            "it and came out harder and warier."
        ),
        "stats": {"CON": 2, "WIS": 1},
        "backstory": "You were caught and punished, emerging harder and wiser.",
        "requires": ["origin_urban"],
        "random": {
            "chance": 0.5,
            "success": {
                "text": "The experience hardened your body and your resolve.",
                "stats": {"STR": 1},
                "backstory": "",
            },
            "fail": {
                "text": "The months of confinement sharpened your mind as you plotted your next move.",
                "stats": {"INT": 1},
                "backstory": "",
            },
        },
        "tags": ["urban", "crime", "prison"],
    },
    {
        "id": "uy2_mentor",
        "phase": "youth", "slot": 5, "stream": "urban",
        "title": "You Found a Mentor in the Underworld",
        "text": (
            "A master thief, a con artist, an information broker — someone "
            "experienced took an interest in you. Their lessons went beyond "
            "technique into strategy, patience, and knowing when to walk away."
        ),
        "stats": {"INT": 1, "DEX": 1, "WIS": 1},
        "backstory": "An underworld mentor taught you craft, patience, and strategy.",
        "requires": ["origin_urban"],
        "tags": ["urban", "crime", "mentorship"],
    },

    # ── Military ──
    {
        "id": "my2_first_battle",
        "phase": "youth", "slot": 5, "stream": "military",
        "title": "Survived Your First Real Battle",
        "text": (
            "Not a raid, not a skirmish — a proper engagement with banners "
            "and shield walls and screaming. You saw people die. You didn't "
            "run. Afterward, your hands wouldn't stop shaking for a week."
        ),
        "stats": {"CON": 2, "STR": 1},
        "backstory": "You survived your first real battle, shaken but unbroken.",
        "requires": ["origin_military"],
        "random": {
            "chance": 0.5,
            "success": {
                "text": "You emerged from the battle with a quiet confidence you hadn't felt before.",
                "stats": {"STR": 1},
                "backstory": "",
            },
            "fail": {
                "text": "The nightmares lasted weeks, but they taught you something about yourself.",
                "stats": {"WIS": 1},
                "backstory": "",
            },
        },
        "tags": ["military", "combat", "trauma"],
    },
    {
        "id": "my2_weapon_master",
        "phase": "youth", "slot": 5, "stream": "military",
        "title": "Trained Under a Weapon Master",
        "text": (
            "A renowned instructor selected you for advanced training. Weeks "
            "of brutal drills, technique refinement, and sparring against "
            "opponents who were always better than you. Until they weren't."
        ),
        "stats": {"STR": 1, "DEX": 2},
        "backstory": "A weapon master honed your skills beyond the basics.",
        "requires": ["origin_military"],
        "tags": ["military", "combat", "mastery"],
    },
    {
        "id": "my2_protect_diplomat",
        "phase": "youth", "slot": 5, "stream": "military",
        "title": "Assigned to Protect a Diplomat",
        "text": (
            "Escort duty. Boring, you thought — until the ambush, the "
            "poisoning attempt, or the tense negotiations where the wrong "
            "word meant war. You learned that fighting isn't always about swords."
        ),
        "stats": {"INT": 1, "WIS": 1, "PIE": 1},
        "backstory": "Guarding a diplomat taught you that battles aren't always fought with steel.",
        "requires": ["origin_military"],
        "unlocks": ["noble_adult"],
        "tags": ["military", "political", "guard"],
    },

    # ── Noble ──
    {
        "id": "ny2_political_scheme",
        "phase": "youth", "slot": 5, "stream": "noble",
        "title": "Entangled in a Political Scheme",
        "text": (
            "Your family — or their rivals — drew you into an intrigue. Forged "
            "letters, secret meetings, alliances brokered in shadowed gardens. "
            "You learned that information is power and trust is a liability."
        ),
        "stats": {"INT": 2, "WIS": 1},
        "backstory": "Political intrigue showed you that information is the truest power.",
        "requires": ["origin_noble"],
        "tags": ["noble", "political", "intrigue"],
    },
    {
        "id": "ny2_fell_in_love",
        "phase": "youth", "slot": 5, "stream": "noble",
        "title": "Fell in Love with Someone Inappropriate",
        "text": (
            "A servant, a rival's child, a commoner, a foreigner — someone "
            "your family would never accept. Whether it lasted or ended in "
            "heartbreak, it cracked open your understanding of the world "
            "beyond your walls."
        ),
        "stats": {"PIE": 1, "WIS": 2},
        "backstory": "A forbidden love opened your heart to the world beyond your station.",
        "requires": ["origin_noble"],
        "tags": ["noble", "love", "growth"],
    },
    {
        "id": "ny2_family_secret",
        "phase": "youth", "slot": 5, "stream": "noble",
        "title": "Discovered a Family Secret",
        "text": (
            "In your father's study, your mother's locked chest, or a whispered "
            "conversation you weren't meant to hear — you learned something "
            "about your family that changed everything. A hidden debt, a crime, "
            "a forbidden allegiance, a sibling you never knew about."
        ),
        "stats": {"INT": 1, "WIS": 1, "DEX": 1},
        "backstory": "You discovered a dark secret hidden in your family's past.",
        "requires": ["origin_noble"],
        "random": {
            "chance": 0.5,
            "success": {
                "text": "You confronted your family with what you knew. The aftermath was painful but honest.",
                "stats": {"PIE": 1},
                "backstory": "",
            },
            "fail": {
                "text": "You kept the knowledge to yourself, a card to play when the time was right.",
                "stats": {"INT": 1},
                "backstory": "",
            },
        },
        "tags": ["noble", "secret", "family"],
    },
]

# ── Slot 6: Youth Defining Moment ─────────────────────────────

YOUTH_DEFINING = [
    # ── Rural ──
    {
        "id": "rydm_left_village",
        "phase": "youth", "slot": 6, "stream": "rural",
        "title": "Left the Village for Good",
        "text": (
            "Something called you away — wanderlust, a burned home, a promise "
            "to someone lost. You packed what little you had and walked down "
            "the road without looking back. The village was behind you now. "
            "Everything else was ahead."
        ),
        "stats": {"CON": 2, "WIS": 1, "DEX": 1},
        "backstory": "You left the village for good, carrying nothing but determination.",
        "requires": ["origin_rural"],
        "tags": ["rural", "departure", "freedom"],
    },
    {
        "id": "rydm_sacred_vow",
        "phase": "youth", "slot": 6, "stream": "rural",
        "title": "Made a Vow at a Sacred Place",
        "text": (
            "Deep in the woods, at an ancient stone circle or a forgotten "
            "shrine, you knelt and swore an oath. To protect the land. To "
            "find what was lost. To become something more. The wind answered, "
            "or maybe it was just the wind."
        ),
        "stats": {"PIE": 2, "WIS": 2},
        "backstory": "At an ancient shrine, you swore a sacred oath that still binds you.",
        "requires": ["origin_rural"],
        "tags": ["rural", "spiritual", "oath"],
    },
    {
        "id": "rydm_killed_beast",
        "phase": "youth", "slot": 6, "stream": "rural",
        "title": "Tracked and Killed a Dangerous Beast",
        "text": (
            "Something was preying on the village — a great wolf, a monstrous "
            "boar, something with too many eyes. You tracked it for three days "
            "and two nights. When you came back, bloody and exhausted, you "
            "carried its head."
        ),
        "stats": {"STR": 2, "DEX": 1, "WIS": 1},
        "backstory": "You hunted and killed a terrible beast that threatened your people.",
        "requires": ["origin_rural"],
        "tags": ["rural", "hunting", "heroic"],
    },

    # ── Urban ──
    {
        "id": "uydm_heist",
        "phase": "youth", "slot": 6, "stream": "urban",
        "title": "Pulled Off a Legendary Heist",
        "text": (
            "The job of a lifetime — a merchant's vault, a noble's treasury, "
            "a ship's cargo hold. The planning took weeks. The execution took "
            "minutes. When it was done, you had more gold than you'd ever "
            "seen — and a reputation to match."
        ),
        "stats": {"DEX": 2, "INT": 2},
        "backstory": "You pulled off a heist that became legend in the underworld.",
        "requires": ["origin_urban"],
        "tags": ["urban", "crime", "legendary"],
    },
    {
        "id": "uydm_betrayed",
        "phase": "youth", "slot": 6, "stream": "urban",
        "title": "Betrayed by Someone You Trusted",
        "text": (
            "Your partner, your mentor, your closest friend — they sold you "
            "out. For money, for safety, for reasons you'll never understand. "
            "You survived, but something in you calcified. Trust became a "
            "currency you spend very carefully."
        ),
        "stats": {"WIS": 2, "INT": 1, "CON": 1},
        "backstory": "A betrayal by someone close taught you to guard your trust carefully.",
        "requires": ["origin_urban"],
        "tags": ["urban", "betrayal", "hardening"],
    },
    {
        "id": "uydm_helped_someone",
        "phase": "youth", "slot": 6, "stream": "urban",
        "title": "Helped Someone at Great Cost",
        "text": (
            "You could have walked away. Should have, probably. But someone "
            "was in trouble — a child, a debtor about to lose everything, a "
            "stranger targeted by the guild — and you stepped in. It cost "
            "you dearly. You'd do it again."
        ),
        "stats": {"PIE": 2, "STR": 1, "WIS": 1},
        "backstory": "You risked everything to help someone in need, and paid dearly for it.",
        "requires": ["origin_urban"],
        "tags": ["urban", "sacrifice", "heroic"],
    },

    # ── Military ──
    {
        "id": "mydm_held_position",
        "phase": "youth", "slot": 6, "stream": "military",
        "title": "Held a Position Against Impossible Odds",
        "text": (
            "Your unit was overrun, your commander was down, and retreat was "
            "the smart move. You didn't retreat. Somehow — stubbornness, terror, "
            "something deeper — you held. When reinforcements arrived, you "
            "were still standing."
        ),
        "stats": {"CON": 2, "STR": 1, "PIE": 1},
        "backstory": "When all was lost, you held your position against impossible odds.",
        "requires": ["origin_military"],
        "tags": ["military", "heroic", "endurance"],
    },
    {
        "id": "mydm_disobeyed",
        "phase": "youth", "slot": 6, "stream": "military",
        "title": "Disobeyed an Order to Save Lives",
        "text": (
            "The command was clear and the command was wrong. Civilians would "
            "have died, or prisoners executed, or the retreat would have been "
            "a slaughter. You disobeyed. There were consequences. You'd "
            "accept them again."
        ),
        "stats": {"PIE": 2, "WIS": 1, "STR": 1},
        "backstory": "You disobeyed a wrong order to save lives, and accepted the consequences.",
        "requires": ["origin_military"],
        "tags": ["military", "moral", "courage"],
    },
    {
        "id": "mydm_promotion",
        "phase": "youth", "slot": 6, "stream": "military",
        "title": "Earned a Battlefield Promotion",
        "text": (
            "In the chaos, when leadership faltered, you stepped forward. "
            "You rallied others, made a decision, gave an order — and it "
            "worked. People followed you because in that moment, you were "
            "the one who knew what to do."
        ),
        "stats": {"STR": 1, "INT": 1, "PIE": 1, "WIS": 1},
        "backstory": "You earned a battlefield promotion through decisive leadership.",
        "requires": ["origin_military"],
        "tags": ["military", "leadership", "promotion"],
    },

    # ── Noble ──
    {
        "id": "nydm_shamed_enemies",
        "phase": "youth", "slot": 6, "stream": "noble",
        "title": "Publicly Shamed Your Family's Enemies",
        "text": (
            "At a feast, a tournament, a court proceeding — you outmaneuvered "
            "a rival family so cleanly that everyone saw it. Your parents were "
            "proud. Your enemies took note. You learned the taste of public victory."
        ),
        "stats": {"INT": 2, "PIE": 1, "DEX": 1},
        "backstory": "You publicly outmaneuvered a rival family, earning respect and enemies alike.",
        "requires": ["origin_noble"],
        "tags": ["noble", "political", "victory"],
    },
    {
        "id": "nydm_renounced",
        "phase": "youth", "slot": 6, "stream": "noble",
        "title": "Renounced Your Title",
        "text": (
            "You walked away from everything — the name, the wealth, the "
            "expectations. Maybe in anger, maybe in principle, maybe because "
            "you wanted to know who you were without it. The world outside "
            "the walls was colder and harder than you imagined."
        ),
        "stats": {"CON": 2, "WIS": 1, "STR": 1},
        "backstory": "You renounced your noble title and stepped into the unknown.",
        "requires": ["origin_noble"],
        "unlocks": ["urban_adult", "rural_adult", "military_adult"],
        "tags": ["noble", "sacrifice", "freedom"],
    },
    {
        "id": "nydm_assassination",
        "phase": "youth", "slot": 6, "stream": "noble",
        "title": "Survived an Assassination Attempt",
        "text": (
            "Poison in your wine, a blade in the dark, a 'hunting accident' — "
            "someone wanted you dead. You survived through luck, instinct, or "
            "the sacrifice of someone loyal. Nothing felt safe afterward."
        ),
        "stats": {"DEX": 2, "CON": 1, "WIS": 1},
        "backstory": "You survived an assassination attempt and learned that safety is an illusion.",
        "requires": ["origin_noble"],
        "tags": ["noble", "danger", "survival"],
    },
]


# ════════════════════════════════════════════════════════════════
# PHASE 3: EARLY ADULTHOOD
# ════════════════════════════════════════════════════════════════

# ── Slot 7: Early Adult Event 1 ───────────────────────────────

ADULT_EVENTS_1 = [
    # ── Rural ──
    {
        "id": "ra1_frontier_guard",
        "phase": "adult", "slot": 7, "stream": "rural",
        "title": "Joined the Frontier Guard",
        "text": (
            "The borderlands needed wardens. You signed on — long patrols "
            "through empty country, watching for threats that might never "
            "come, or might come tonight. The solitude suited you."
        ),
        "stats": {"CON": 1, "WIS": 1, "STR": 1},
        "backstory": "You joined the frontier guard, patrolling the lonely borderlands.",
        "requires": ["origin_rural"],
        "tags": ["rural", "military", "patrol"],
    },
    {
        "id": "ra1_herbalist",
        "phase": "adult", "slot": 7, "stream": "rural",
        "title": "Became a Traveling Herbalist",
        "text": (
            "Your knowledge of plants and remedies earned you a welcome in "
            "every village. You wandered from settlement to settlement, trading "
            "cures for meals and shelter. People began to seek you out."
        ),
        "stats": {"WIS": 2, "PIE": 1},
        "backstory": "You became a wandering healer, trading cures and wisdom.",
        "requires": ["origin_rural"],
        "tags": ["rural", "healing", "travel"],
    },
    {
        "id": "ra1_wilderness_guide",
        "phase": "adult", "slot": 7, "stream": "rural",
        "title": "Set Out as a Wilderness Guide",
        "text": (
            "Merchants, pilgrims, and fools needed someone who knew the wild "
            "roads. You hired out your skills — navigation, survival, protection. "
            "Every journey was different. Some clients didn't make it."
        ),
        "stats": {"DEX": 1, "WIS": 1, "INT": 1},
        "backstory": "You guided travelers through the wilds for pay and purpose.",
        "requires": ["origin_rural"],
        "tags": ["rural", "guide", "travel"],
    },

    # ── Urban ──
    {
        "id": "ua1_guild_official",
        "phase": "adult", "slot": 7, "stream": "urban",
        "title": "Joined a Thieves' Guild Officially",
        "text": (
            "No more freelancing. You took the oaths, learned the signs, and "
            "gained access to the network — jobs, fences, safe houses, "
            "information. The guild took a cut, but the work was steadier."
        ),
        "stats": {"DEX": 2, "INT": 1},
        "backstory": "You became a full member of the thieves' guild.",
        "requires": ["origin_urban"],
        "tags": ["urban", "crime", "guild"],
    },
    {
        "id": "ua1_privateer",
        "phase": "adult", "slot": 7, "stream": "urban",
        "title": "Went to Sea with a Privateer Crew",
        "text": (
            "Not quite pirates, not quite navy — letters of marque made it "
            "legal, barely. The ship was fast, the captain was clever, and "
            "the prizes were rich. You learned to fight on a rolling deck."
        ),
        "stats": {"DEX": 1, "CON": 1, "STR": 1},
        "backstory": "You sailed with privateers, living between law and piracy.",
        "requires": ["origin_urban"],
        "tags": ["urban", "sea", "combat"],
    },
    {
        "id": "ua1_robbed_bank",
        "phase": "adult", "slot": 7, "stream": "urban",
        "title": "Robbed a Bank",
        "text": (
            "The big score. Weeks of planning, a team of specialists, one "
            "night of execution. Everything depended on timing, nerve, and "
            "a little luck."
        ),
        "stats": {"DEX": 1, "INT": 1},
        "backstory": "You attempted the ultimate score — a bank robbery.",
        "requires": ["origin_urban"],
        "random": {
            "chance": 0.5,
            "success": {
                "text": "The vault opened like a whisper. You walked out rich and unseen.",
                "stats": {"DEX": 1, "INT": 1},
                "backstory": " It succeeded brilliantly.",
            },
            "fail": {
                "text": "Alarms, guards, a frantic escape — you barely got out, and spent months lying low.",
                "stats": {"CON": 1, "WIS": 1},
                "backstory": " It went badly, but you survived.",
            },
        },
        "tags": ["urban", "crime", "heist"],
    },

    # ── Military ──
    {
        "id": "ma1_army",
        "phase": "adult", "slot": 7, "stream": "military",
        "title": "Joined a Professional Army",
        "text": (
            "Not a militia, not a garrison — a proper fighting force. You "
            "marched, you drilled, you waited, and eventually you fought. "
            "The army was your family now, for better and worse."
        ),
        "stats": {"STR": 1, "CON": 2},
        "backstory": "You joined a professional army and learned what true soldiering means.",
        "requires": ["origin_military"],
        "tags": ["military", "army", "combat"],
    },
    {
        "id": "ma1_military_scout",
        "phase": "adult", "slot": 7, "stream": "military",
        "title": "Trained as a Military Scout",
        "text": (
            "They needed sharp eyes more than strong arms. You learned to move "
            "unseen, survive alone, and bring back intelligence that saved "
            "lives. The work was lonely but essential."
        ),
        "stats": {"DEX": 2, "WIS": 1},
        "backstory": "You trained as a military scout, operating alone behind enemy lines.",
        "requires": ["origin_military"],
        "tags": ["military", "scouting", "stealth"],
    },
    {
        "id": "ma1_navy",
        "phase": "adult", "slot": 7, "stream": "military",
        "title": "Joined the Navy as Midshipman",
        "text": (
            "The sea called, or the army didn't want you. Naval discipline "
            "was its own world — tighter quarters, harsher rules, and nowhere "
            "to desert to."
        ),
        "stats": {"INT": 1, "CON": 1, "DEX": 1},
        "backstory": "You served at sea as a naval officer, learning discipline and navigation.",
        "requires": ["origin_military"],
        "tags": ["military", "navy", "sea"],
    },

    # ── Noble ──
    {
        "id": "na1_arcane_academy",
        "phase": "adult", "slot": 7, "stream": "noble",
        "title": "Enrolled in the Academy of Arcane Arts",
        "text": (
            "Your family's wealth opened doors that talent alone couldn't. "
            "The academy was rigorous — theory, practice, and the very real "
            "danger of magic gone wrong. Not every student graduated. Not "
            "every student survived."
        ),
        "stats": {"INT": 2, "WIS": 1},
        "backstory": "You studied at an academy of arcane arts, where magic was deadly serious.",
        "requires": ["origin_noble"],
        "tags": ["noble", "magic", "academic"],
    },
    {
        "id": "na1_family_lands",
        "phase": "adult", "slot": 7, "stream": "noble",
        "title": "Took Over Management of Family Lands",
        "text": (
            "Whether by death, disgrace, or duty, the estate fell to you. "
            "Suddenly you were responsible for hundreds of people — tenants, "
            "servants, soldiers. The ledgers alone were overwhelming."
        ),
        "stats": {"INT": 1, "WIS": 1, "PIE": 1},
        "backstory": "You took charge of the family estate and its people.",
        "requires": ["origin_noble"],
        "tags": ["noble", "leadership", "responsibility"],
    },
    {
        "id": "na1_holy_order",
        "phase": "adult", "slot": 7, "stream": "noble",
        "title": "Dedicated Yourself to a Holy Order",
        "text": (
            "Faith called — or politics demanded it — and you entered a "
            "religious order. The transition from silk to simple robes was "
            "jarring. The prayers, the fasting, the service to others... "
            "some of it felt like punishment. Some of it felt like freedom."
        ),
        "stats": {"PIE": 2, "WIS": 1},
        "backstory": "You dedicated yourself to a holy order, seeking meaning in faith.",
        "requires": ["origin_noble"],
        "tags": ["noble", "spiritual", "devotion"],
    },
]

# ── Slot 8: Early Adult Event 2 ───────────────────────────────

ADULT_EVENTS_2 = [
    # ── Rural ──
    {
        "id": "ra2_ancient_ruins",
        "phase": "adult", "slot": 8, "stream": "rural",
        "title": "Discovered Ancient Ruins",
        "text": (
            "Deep in uncharted territory, you found something old — crumbling "
            "walls covered in symbols, a sealed door, the remains of something "
            "that shouldn't exist this far from civilization."
        ),
        "stats": {"INT": 2, "WIS": 1},
        "backstory": "You discovered ancient ruins in the wilderness, hinting at forgotten powers.",
        "requires": ["origin_rural"],
        "tags": ["rural", "discovery", "ancient"],
    },
    {
        "id": "ra2_brutal_winter",
        "phase": "adult", "slot": 8, "stream": "rural",
        "title": "Survived a Brutal Winter Alone",
        "text": (
            "Cut off by storms, injured, or simply lost — you spent weeks "
            "alone in the wild with dwindling supplies. You ate things you'd "
            "rather forget. You talked to yourself. But spring came, and so "
            "did you."
        ),
        "stats": {"CON": 2, "WIS": 1},
        "backstory": "A brutal winter alone in the wilds tested everything you had.",
        "requires": ["origin_rural"],
        "tags": ["rural", "survival", "endurance"],
    },
    {
        "id": "ra2_earned_respect",
        "phase": "adult", "slot": 8, "stream": "rural",
        "title": "Earned the Respect of a Community",
        "text": (
            "Through deeds, not words — a rescue, a defense, a problem solved "
            "— you became someone people trusted. They came to you for advice, "
            "for protection, for leadership you never asked for."
        ),
        "stats": {"PIE": 1, "STR": 1, "WIS": 1},
        "backstory": "You earned the trust and respect of a frontier community.",
        "requires": ["origin_rural"],
        "tags": ["rural", "leadership", "community"],
    },

    # ── Urban ──
    {
        "id": "ua2_informants",
        "phase": "adult", "slot": 8, "stream": "urban",
        "title": "Built a Network of Informants",
        "text": (
            "You realized information was worth more than gold. Slowly, "
            "carefully, you cultivated sources — beggars, servants, merchants, "
            "guards. A whisper network with you at its center."
        ),
        "stats": {"INT": 2, "WIS": 1},
        "backstory": "You built a network of informants, becoming a broker of secrets.",
        "requires": ["origin_urban"],
        "tags": ["urban", "information", "network"],
    },
    {
        "id": "ua2_deadly_rival",
        "phase": "adult", "slot": 8, "stream": "urban",
        "title": "Narrowly Escaped a Deadly Rival",
        "text": (
            "Someone wanted your territory, your reputation, or your life. "
            "The confrontation came close — too close. You survived through "
            "speed, cunning, and doing what they didn't expect."
        ),
        "stats": {"DEX": 2, "CON": 1},
        "backstory": "You barely escaped a deadly rival who wanted you eliminated.",
        "requires": ["origin_urban"],
        "tags": ["urban", "danger", "escape"],
    },
    {
        "id": "ua2_revolutionary",
        "phase": "adult", "slot": 8, "stream": "urban",
        "title": "Fell in with a Revolutionary Movement",
        "text": (
            "Not just crime for profit — crime for a cause. The group wanted "
            "to change things: overthrow a corrupt official, free imprisoned "
            "dissidents, redistribute hoarded wealth. The idealism was "
            "infectious. The danger was real."
        ),
        "stats": {"PIE": 1, "INT": 1, "STR": 1},
        "backstory": "You joined a revolutionary movement, fighting for change.",
        "requires": ["origin_urban"],
        "tags": ["urban", "political", "idealist"],
    },

    # ── Military ──
    {
        "id": "ma2_led_squad",
        "phase": "adult", "slot": 8, "stream": "military",
        "title": "Led a Squad on a Dangerous Mission",
        "text": (
            "Behind enemy lines, into hostile territory, or through "
            "monster-infested ruins — your unit was given a job no one "
            "else wanted. You brought most of them back."
        ),
        "stats": {"STR": 1, "INT": 1, "PIE": 1},
        "backstory": "You led a squad through a mission no one expected you to survive.",
        "requires": ["origin_military"],
        "tags": ["military", "leadership", "danger"],
    },
    {
        "id": "ma2_wounded",
        "phase": "adult", "slot": 8, "stream": "military",
        "title": "Wounded in Battle and Recovered",
        "text": (
            "Steel or magic or claws — something put you down hard. The "
            "recovery was long and humbling. Healers patched your body; "
            "you had to rebuild your confidence yourself."
        ),
        "stats": {"CON": 2, "WIS": 1},
        "backstory": "A serious wound in battle taught you humility and endurance.",
        "requires": ["origin_military"],
        "tags": ["military", "wound", "recovery"],
    },
    {
        "id": "ma2_corruption",
        "phase": "adult", "slot": 8, "stream": "military",
        "title": "Uncovered Corruption in the Ranks",
        "text": (
            "An officer selling supplies, a commander betraying positions, "
            "bribes flowing from enemy coffers. You found the proof. What "
            "you did with it defined you."
        ),
        "stats": {"INT": 1, "WIS": 1, "PIE": 1},
        "backstory": "You uncovered corruption among your own officers.",
        "requires": ["origin_military"],
        "random": {
            "chance": 0.5,
            "success": {
                "text": "You reported it to the highest authority you trusted. Justice was slow, but it came.",
                "stats": {"PIE": 1},
                "backstory": " You chose justice.",
            },
            "fail": {
                "text": "You kept the evidence hidden, waiting for the right moment to use it.",
                "stats": {"INT": 1},
                "backstory": " You kept the leverage.",
            },
        },
        "tags": ["military", "corruption", "choice"],
    },

    # ── Noble ──
    {
        "id": "na2_alliance",
        "phase": "adult", "slot": 8, "stream": "noble",
        "title": "Negotiated a Critical Alliance",
        "text": (
            "Your family needed friends, and you were sent to broker the "
            "deal. Weeks of negotiation, veiled threats, calculated "
            "generosity — and finally, an agreement."
        ),
        "stats": {"INT": 1, "WIS": 1, "PIE": 1},
        "backstory": "You negotiated a crucial alliance that changed the balance of power.",
        "requires": ["origin_noble"],
        "tags": ["noble", "political", "diplomacy"],
    },
    {
        "id": "na2_duel",
        "phase": "adult", "slot": 8, "stream": "noble",
        "title": "Fought a Duel of Honor",
        "text": (
            "Someone insulted your family, your honor, or your principles. "
            "Steel was drawn. The duel was formal, witnessed, and very real."
        ),
        "stats": {"STR": 1, "DEX": 2},
        "backstory": "You fought a formal duel of honor.",
        "requires": ["origin_noble"],
        "random": {
            "chance": 0.6,
            "success": {
                "text": "Your blade found its mark. You won cleanly, and your name was spoken with new respect.",
                "stats": {"STR": 1},
                "backstory": " You won.",
            },
            "fail": {
                "text": "You lost, but you stood and fought without flinching. Even your opponent respected that.",
                "stats": {"PIE": 1},
                "backstory": " You lost, but with honor.",
            },
        },
        "tags": ["noble", "combat", "honor"],
    },
    {
        "id": "na2_pilgrimage",
        "phase": "adult", "slot": 8, "stream": "noble",
        "title": "Went on a Pilgrimage",
        "text": (
            "For penance, for seeking, or for escape — you left everything "
            "behind and walked the ancient pilgrim roads. Months of simple "
            "living, quiet reflection, and encounters with strangers who "
            "owed you nothing."
        ),
        "stats": {"WIS": 2, "PIE": 1},
        "backstory": "A pilgrimage stripped away everything but what truly mattered.",
        "requires": ["origin_noble"],
        "tags": ["noble", "spiritual", "journey"],
    },
]

# ── Slot 9: Early Adult Defining Moment ───────────────────────

ADULT_DEFINING = [
    # ── Rural ──
    {
        "id": "radm_dark_stirred",
        "phase": "adult", "slot": 9, "stream": "rural",
        "title": "Something Dark Stirred in the Wilderness",
        "text": (
            "The animals fled. The rivers ran strange. At night, the darkness "
            "felt thicker. Something is wrong in the wild places, and you're "
            "one of the few who can feel it. You gathered your gear and headed "
            "toward the source, not away from it."
        ),
        "stats": {"WIS": 2, "CON": 1, "STR": 1},
        "backstory": "When darkness stirred in the wilderness, you walked toward it.",
        "requires": ["origin_rural"],
        "tags": ["rural", "darkness", "quest"],
    },
    {
        "id": "radm_plea_help",
        "phase": "adult", "slot": 9, "stream": "rural",
        "title": "You Received a Desperate Plea for Help",
        "text": (
            "A message — from your old village, from a friend in trouble, "
            "from a stranger who somehow knew your name. They need you. The "
            "journey will be dangerous. You went anyway."
        ),
        "stats": {"PIE": 2, "STR": 1, "CON": 1},
        "backstory": "A desperate call for help set you on the path to adventure.",
        "requires": ["origin_rural"],
        "tags": ["rural", "call", "heroic"],
    },
    {
        "id": "radm_found_map",
        "phase": "adult", "slot": 9, "stream": "rural",
        "title": "You Found a Map to Something Legendary",
        "text": (
            "In the ruins, in a dead traveler's pack, in the pages of a "
            "crumbling book — a map. It points to something that shouldn't "
            "exist: a lost city, a forgotten weapon, a truth someone buried "
            "long ago. You couldn't leave it alone."
        ),
        "stats": {"INT": 2, "WIS": 1, "DEX": 1},
        "backstory": "A mysterious map sent you chasing legends.",
        "requires": ["origin_rural"],
        "tags": ["rural", "discovery", "quest"],
    },

    # ── Urban ──
    {
        "id": "uadm_impossible_job",
        "phase": "adult", "slot": 9, "stream": "urban",
        "title": "The Guild Gave You an Impossible Job",
        "text": (
            "The target is heavily guarded, the deadline is impossible, and "
            "failure means death — yours. But the reward would set you up "
            "for life. You said yes before you thought it through."
        ),
        "stats": {"DEX": 2, "INT": 1, "CON": 1},
        "backstory": "An impossible job from the guild launched you into the unknown.",
        "requires": ["origin_urban"],
        "tags": ["urban", "crime", "quest"],
    },
    {
        "id": "uadm_left_crime",
        "phase": "adult", "slot": 9, "stream": "urban",
        "title": "You Chose to Leave the Criminal Life",
        "text": (
            "Enough blood, enough fear, enough looking over your shoulder. "
            "You walked away from everything — the connections, the money, "
            "the identity. Starting over with nothing but your skills and "
            "your scars."
        ),
        "stats": {"WIS": 2, "PIE": 1, "CON": 1},
        "backstory": "You left the criminal life behind, seeking something better.",
        "requires": ["origin_urban"],
        "tags": ["urban", "redemption", "change"],
    },
    {
        "id": "uadm_dying_secret",
        "phase": "adult", "slot": 9, "stream": "urban",
        "title": "A Dying Person Gave You a Secret",
        "text": (
            "In an alley, in a tavern back room, in a prison cell — someone "
            "with their last breath told you something that could shake "
            "kingdoms. A name, a location, a truth. They made you promise "
            "to act on it."
        ),
        "stats": {"INT": 2, "WIS": 1, "PIE": 1},
        "backstory": "A dying stranger entrusted you with a secret that could change everything.",
        "requires": ["origin_urban"],
        "tags": ["urban", "mystery", "quest"],
    },

    # ── Military ──
    {
        "id": "madm_unit_destroyed",
        "phase": "adult", "slot": 9, "stream": "military",
        "title": "Your Unit Was Destroyed",
        "text": (
            "Ambush, betrayal, overwhelming force — your company was shattered. "
            "You crawled out of the wreckage, one of a handful of survivors. "
            "The army considers you dead. You're not sure they're wrong."
        ),
        "stats": {"CON": 2, "WIS": 1, "STR": 1},
        "backstory": "Your unit was destroyed. You survived, and now walk a different path.",
        "requires": ["origin_military"],
        "tags": ["military", "loss", "rebirth"],
    },
    {
        "id": "madm_special_mission",
        "phase": "adult", "slot": 9, "stream": "military",
        "title": "Given a Special Mission",
        "text": (
            "High command selected you personally. The mission is classified, "
            "dangerous, and vital. You were given supplies, a destination, and "
            "orders to trust no one."
        ),
        "stats": {"STR": 1, "INT": 1, "DEX": 1, "WIS": 1},
        "backstory": "A classified mission from high command sent you into the shadows.",
        "requires": ["origin_military"],
        "tags": ["military", "mission", "quest"],
    },
    {
        "id": "madm_deserted",
        "phase": "adult", "slot": 9, "stream": "military",
        "title": "You Deserted",
        "text": (
            "You broke your oath. The penalty is death. Whatever you saw, "
            "whatever was ordered, whatever you learned — it was enough to "
            "make you throw away everything you'd built. You don't talk "
            "about why."
        ),
        "stats": {"DEX": 1, "WIS": 2, "CON": 1},
        "backstory": "You deserted the army for reasons you keep to yourself.",
        "requires": ["origin_military"],
        "tags": ["military", "desertion", "mystery"],
    },

    # ── Noble ──
    {
        "id": "nadm_family_destroyed",
        "phase": "adult", "slot": 9, "stream": "noble",
        "title": "Your Family Was Destroyed",
        "text": (
            "Fire, political purge, assassination, bankruptcy — it doesn't "
            "matter how. Everything is gone. The name that once opened doors "
            "now closes them. You have your education, your training, your "
            "wits, and nothing else."
        ),
        "stats": {"CON": 2, "WIS": 1, "INT": 1},
        "backstory": "Your family was destroyed, leaving you with nothing but your wits.",
        "requires": ["origin_noble"],
        "tags": ["noble", "loss", "rebirth"],
    },
    {
        "id": "nadm_vision",
        "phase": "adult", "slot": 9, "stream": "noble",
        "title": "You Received a Vision",
        "text": (
            "In the temple, in a dream, from a dying seer — you were told "
            "something impossible about your destiny. You don't entirely "
            "believe it. But you can't stop thinking about it, and it's "
            "pulling you toward something."
        ),
        "stats": {"WIS": 2, "PIE": 1, "INT": 1},
        "backstory": "A vision of your destiny set you on an uncertain path.",
        "requires": ["origin_noble"],
        "tags": ["noble", "prophecy", "quest"],
    },
    {
        "id": "nadm_ancient_legacy",
        "phase": "adult", "slot": 9, "stream": "noble",
        "title": "You Uncovered an Ancient Family Legacy",
        "text": (
            "In the family vault, in a sealed letter from a dead ancestor, "
            "in ruins beneath your estate — evidence that your bloodline is "
            "connected to something ancient and powerful. And dangerous. "
            "And unfinished."
        ),
        "stats": {"INT": 2, "PIE": 1, "WIS": 1},
        "backstory": "An ancient family legacy drew you into a quest beyond your imagining.",
        "requires": ["origin_noble"],
        "tags": ["noble", "legacy", "quest"],
    },
]


# ════════════════════════════════════════════════════════════════
# EVENT REGISTRY — All events organized by slot
# ════════════════════════════════════════════════════════════════

ALL_EVENTS_BY_SLOT = {
    1: ORIGINS,
    2: CHILDHOOD_EVENTS,
    3: CHILDHOOD_DEFINING,
    4: YOUTH_EVENTS_1,
    5: YOUTH_EVENTS_2,
    6: YOUTH_DEFINING,
    7: ADULT_EVENTS_1,
    8: ADULT_EVENTS_2,
    9: ADULT_DEFINING,
}

SLOT_TITLES = {
    1: "Origin",
    2: "Childhood",
    3: "Childhood — Defining Moment",
    4: "Youth",
    5: "Youth",
    6: "Youth — Defining Moment",
    7: "Early Adulthood",
    8: "Early Adulthood",
    9: "Early Adulthood — Defining Moment",
}

PHASE_FOR_SLOT = {
    1: "Childhood", 2: "Childhood", 3: "Childhood",
    4: "Youth", 5: "Youth", 6: "Youth",
    7: "Early Adulthood", 8: "Early Adulthood", 9: "Early Adulthood",
}


def get_available_events(slot, chosen_history):
    """
    Return the list of events available for a given slot,
    filtered by the character's history (previous choices).

    chosen_history: list of event dicts the character has already chosen.
    """
    all_events = ALL_EVENTS_BY_SLOT.get(slot, [])

    if slot == 1:
        # Origins — all available
        return all_events

    # Determine the character's stream from origin
    origin = chosen_history[0] if chosen_history else None
    if not origin:
        return all_events

    origin_stream = origin.get("stream", "any")

    # Collect all unlocked streams from history
    unlocked_tags = set()
    for ev in chosen_history:
        for u in ev.get("unlocks", []):
            unlocked_tags.add(u)

    # Filter events
    available = []
    for event in all_events:
        ev_stream = event.get("stream", "any")

        # Check requires — must have at least one required event in history
        requires = event.get("requires", [])
        if requires:
            history_ids = [e["id"] for e in chosen_history]
            # Check if origin matches (requires often reference origin)
            origin_match = any(r in history_ids for r in requires)
            # Also check if stream was unlocked via crossover
            stream_unlocked = f"{ev_stream}_youth" in unlocked_tags or \
                              f"{ev_stream}_adult" in unlocked_tags or \
                              f"{ev_stream}_childhood" in unlocked_tags
            if not origin_match and not stream_unlocked:
                # Special: if event stream matches origin stream, allow it
                if ev_stream != origin_stream:
                    continue

        available.append(event)

    # If somehow nothing is available (shouldn't happen), return all for the slot
    if not available:
        return [e for e in all_events if e.get("stream") == origin_stream]

    return available
