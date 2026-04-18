"""
Realm of Shadows — Shop Inventory Data
Items available for purchase at shops, organized by tier/location.
"""

from core.equipment import ARMOR

# ═══════════════════════════════════════════════════════════════
#  GENERAL STORE — Weapons, Armor, Basic Supplies
# ═══════════════════════════════════════════════════════════════

GENERAL_STORE = {
    "name": "General Store",
    "welcome": "Welcome, travelers. Browse my wares.",

    # Weapons for sale (dict format matching loot items)
    "weapons": [
        {"name": "Iron Dagger", "type": "weapon", "slot": "weapon",
         "subtype": "Dagger", "rarity": "common", "damage": 10,
         "damage_stat": {"DEX": 0.4},
         "phys_type": "piercing", "range": "melee",
         "description": "A simple iron dagger. Quick but light.",
         "buy_price": 15, "sell_price": 6, "identified": True},

        {"name": "Short Sword", "type": "weapon", "slot": "weapon",
         "subtype": "Short Sword", "rarity": "common", "damage": 13,
         "damage_stat": {"DEX": 0.4},
         "phys_type": "slashing", "range": "melee",
         "description": "A reliable short sword.",
         "buy_price": 30, "sell_price": 12, "identified": True},

        {"name": "Longsword", "type": "weapon", "slot": "weapon",
         "subtype": "Longsword", "rarity": "common", "damage": 18,
         "damage_stat": {"DEX": 0.28, "STR": 0.12},
         "phys_type": "slashing", "range": "melee",
         "description": "A well-forged longsword. Standard fighter's weapon.",
         "buy_price": 60, "sell_price": 25, "identified": True},

        {"name": "Hand Axe", "type": "weapon", "slot": "weapon",
         "subtype": "Axe", "rarity": "common", "damage": 16,
         "damage_stat": {"STR": 0.3, "DEX": 0.12},
         "phys_type": "slashing", "range": "melee",
         "description": "A sturdy hand axe.",
         "buy_price": 40, "sell_price": 16, "identified": True},

        {"name": "Mace", "type": "weapon", "slot": "weapon",
         "subtype": "Mace", "rarity": "common", "damage": 14,
         "damage_stat": {"STR": 0.4},
         "phys_type": "blunt", "range": "melee",
         "description": "A heavy iron mace. Good against armored foes.",
         "buy_price": 35, "sell_price": 14, "identified": True},

        {"name": "Shortbow", "type": "weapon", "slot": "weapon",
         "subtype": "Shortbow", "rarity": "common", "damage": 16,
         "damage_stat": {"STR": 0.4},
         "phys_type": "piercing", "range": "ranged",
         "description": "A simple shortbow for ranged attacks.",
         "buy_price": 25, "sell_price": 10, "identified": True},

        {"name": "Longbow", "type": "weapon", "slot": "weapon",
         "subtype": "Longbow", "rarity": "common", "damage": 20,
         "damage_stat": {"DEX": 0.35, "STR": 0.08},
         "phys_type": "piercing", "range": "ranged",
         "description": "A proper longbow with good range and power.",
         "buy_price": 55, "sell_price": 22, "identified": True},

        {"name": "Wooden Staff", "type": "weapon", "slot": "weapon",
         "subtype": "Staff", "max_charges": 30, "rarity": "common", "damage": 14,
         "enchant_element": "arcane",
         "on_hit_effect": {"status": "Slowed", "chance": 0.20, "duration": 1},
         "damage_stat": {"DEX": 0.35, "STR": 0.08},
         "phys_type": "blunt", "range": "melee",
         "stat_bonuses": {"INT": 1},
         "description": "A carved wooden staff. Enhances spellcasting.",
         "buy_price": 20, "sell_price": 8, "identified": True},

        {"name": "Spear", "type": "weapon", "slot": "weapon",
         "subtype": "Spear", "rarity": "common", "damage": 17,
         "damage_stat": {"STR": 0.16, "INT": 0.24},
         "phys_type": "piercing", "range": "reach",
         "description": "A long spear. Reach weapon — effective from mid row.",
         "buy_price": 35, "sell_price": 14, "identified": True},
    ],

    # Armor — pull from ARMOR database and add prices
    "armor": [],  # populated at import time below

    "consumables": [
        {"name": "Minor Healing Potion", "type": "consumable", "subtype": "potion",
         "rarity": "common", "heal_amount": 25,
         "description": "Restores 25 HP to one character.",
         "buy_price": 10, "sell_price": 4, "identified": True},

        {"name": "Healing Potion", "type": "consumable", "subtype": "potion",
         "rarity": "common", "heal_amount": 50,
         "description": "Restores 50 HP to one character.",
         "buy_price": 25, "sell_price": 10, "identified": True},

        {"name": "Mana Crystal", "type": "material", "subtype": "reagent",
         "rarity": "uncommon", "quantity": 1,
         "description": "A dense crystal of condensed arcane energy. Recharges 5 charges on a focus weapon.",
         "buy_price": 55, "sell_price": 20, "identified": True},
        {"name": "Venom Vial", "type": "material", "subtype": "reagent",
         "rarity": "uncommon", "quantity": 1,
         "description": "A sealed vial of concentrated venom. Refills 5 charges on a venom reservoir weapon.",
         "buy_price": 40, "sell_price": 15, "identified": True},
        {"name": "Antidote", "type": "consumable", "subtype": "potion",
         "rarity": "common", "cures": ["Poison"],
         "description": "Cures poison.",
         "buy_price": 15, "sell_price": 6, "identified": True},
    ],
}

# Populate armor shop from ARMOR database
for name, data in ARMOR.items():
    shop_item = dict(data)
    shop_item["type"] = "armor" if data["slot"] == "body" else data["slot"]
    shop_item["buy_price"] = data.get("value", 10)
    shop_item["sell_price"] = max(1, data.get("value", 10) // 3)
    shop_item["identified"] = True
    GENERAL_STORE["armor"].append(shop_item)


# ═══════════════════════════════════════════════════════════════
#  TEMPLE — Healing, Identification, Curse Removal
# ═══════════════════════════════════════════════════════════════

TEMPLE = {
    "name": "Temple of Light",
    "welcome": "Blessings upon you, travelers. How may the Temple serve?",

    "services": {
        "cure_poison": {
            "name": "Cure Poison",
            "description": "Purge all poisons from one character.",
            "cost": 30,
            "action": "cure_poison",
        },
        "remove_curse": {
            "name": "Remove Curse",
            "description": "Lift a curse from one character.",
            "cost": 100,
            "action": "remove_curse",
        },
        "resurrect": {
            "name": "Resurrect",
            "description": "Revive a fallen party member. Cost scales with level.",
            "cost": 200,  # base — actual cost = 200 + 100*level
            "action": "resurrect",
        },
        "identify_item": {
            "name": "Identify Item",
            "description": "Fully identify one item (magical and material properties).",
            "cost": 15,
            "action": "identify",
        },
        "blessing": {
            "name": "Temple Blessing",
            "description": "Receive a minor blessing for your next venture. (+5% accuracy for next dungeon)",
            "cost": 50,
            "action": "blessing",
        },
    },
}


# ═══════════════════════════════════════════════════════════════
#  TAVERN — Info, Rumors, Flavor
# ═══════════════════════════════════════════════════════════════

TAVERN = {
    "name": "The Shadowed Flagon",
    "welcome": "Pull up a chair! What'll it be?",
    "drink_cost": 2,

    "patrons": [
        {
            "name": "Old Varta",
            "role": "regular",
            "description": "A weathered woman nursing the same cup she arrived with.",
            "color": (160, 140, 110),
            "sober": [
                "I've been coming here thirty years. Seen worse than whatever's troubling you.",
                "Order something or stop blocking the light.",
                "The road south was clear this morning. North... I wouldn't.",
            ],
            "drunk": [
                "Y'know, I used t'think I'd seen everything. Then everything got worse.",
                "My granddaughter wants to be an adventurer. I told her — do it now, before your knees go.",
                "The Fading, they call it. My father called it the Greying. His father called it something else.",
            ],
        },
        {
            "name": "Brennan the Peddler",
            "role": "merchant",
            "description": "A traveling merchant with ink-stained fingers and a nervous habit of checking the door.",
            "color": (120, 155, 130),
            "sober": [
                "Trade's bad. Everything west of Ironhearth takes twice as long to move now.",
                "I don't ask what's in the crates anymore. Makes the job easier.",
                "There's work if you're not picky.",
            ],
            "drunk": [
                "I'll tell you something I shouldn't. The Governor's been moving gold east. A lot of it.",
                "Someone's buying weapons in bulk. Not swords — ritual stuff. Doesn't go to any army I know.",
                "Last month I saw Warden markings on a crate headed for Valdris' Spire. Didn't ask questions.",
            ],
        },
        {
            "name": "Silas",
            "role": "drifter",
            "description": "A young man with the look of someone who left somewhere in a hurry.",
            "color": (140, 120, 160),
            "sober": [
                "Don't ask where I'm from. Drink your drink.",
                "Funny place, this. Everyone passes through. Nobody stays.",
                "I heard there's work north. Haven't decided if I'm desperate enough yet.",
            ],
            "drunk": [
                "I left Thornhaven when the black-cloaks started recruiting. Some of my friends said yes.",
                "You know what no one tells you about running away? You have to keep running.",
                "There's a cult, or there was. Preaching about the Fading as a gift. They're still out there.",
            ],
        },
        {
            "name": "Marta Holt",
            "role": "farmer",
            "description": "A farmer with flour on her boots, taking a rare evening off.",
            "color": (190, 160, 100),
            "sober": [
                "Harvest was good this year, at least. Small mercies.",
                "My husband says the east field soil has gone grey. Never seen that before.",
                "Whatever you lot are doing about the shadows — keep doing it.",
            ],
            "drunk": [
                "My youngest saw something in the north field last harvest. Won't say what. Won't go back.",
                "The old shrine near our farm — the one nobody tends — it's been lit at night. Nobody knows who.",
                "You want to know why people don't talk about the Fading? Because talking about it makes it real.",
            ],
        },
    ],

    "rumors": [
        "I heard goblins have been massing in the eastern woods. More than usual.",
        "A merchant was robbed on the north road last week. Bandits are getting bolder.",
        "They say the old mine is haunted. Strange lights at night.",
        "The orc chieftain in the hills has been gathering warriors. Trouble's coming.",
        "A traveling mage passed through here. Said something about shadow magic growing stronger.",
        "The wolves have been unusually aggressive this season. Something's driving them.",
        "The temple priests seem worried. They won't say about what.",
        "An old adventurer told me there's a forgotten dungeon beneath the ruins to the south.",
        "The blacksmith says ore quality has dropped. Something's wrong with the mines.",
        "I've seen strange folk in dark robes passing through at night. Gives me the chills.",
    ],

    "recruits": [
        {
            "name": "Aldric",
            "race_name": "Human",
            "class_name": "Fighter",
            "level": 2,
            "color": (200, 120, 60),
            "pitch": "I know which end of a sword to hold. Pay's fair and I won't run.",
            "stats": {"STR": 16, "DEX": 12, "CON": 14, "INT": 8, "WIS": 8, "PIE": 6},
            "_char": None,
        },
        {
            "name": "Vespa",
            "race_name": "Human",
            "class_name": "Thief",
            "level": 2,
            "color": (120, 160, 140),
            "pitch": "Locks, traps, back entrances. I don't ask what's inside.",
            "stats": {"STR": 10, "DEX": 18, "CON": 10, "INT": 12, "WIS": 12, "PIE": 5},
            "_char": None,
        },
        {
            "name": "Sorel",
            "race_name": "Human",
            "class_name": "Mage",
            "level": 2,
            "color": (100, 130, 200),
            "pitch": "Three years at the academy. I can cast. That's more than most.",
            "stats": {"STR": 6, "DEX": 11, "CON": 8, "INT": 18, "WIS": 14, "PIE": 8},
            "_char": None,
        },
        {
            "name": "Brynn",
            "race_name": "Human",
            "class_name": "Cleric",
            "level": 2,
            "color": (200, 190, 100),
            "pitch": "The light provides. So do I — if you treat the wounded.",
            "stats": {"STR": 10, "DEX": 10, "CON": 12, "INT": 10, "WIS": 14, "PIE": 16},
            "_char": None,
        },
        {
            "name": "Kael",
            "race_name": "Human",
            "class_name": "Ranger",
            "level": 3,
            "color": (120, 180, 100),
            "pitch": "Tracked prey through three kingdoms. Dungeons are just smaller forests.",
            "stats": {"STR": 12, "DEX": 16, "CON": 12, "INT": 10, "WIS": 14, "PIE": 7},
            "_char": None,
        },
        {
            "name": "Mira",
            "race_name": "Human",
            "class_name": "Monk",
            "level": 3,
            "color": (160, 120, 200),
            "pitch": "I don't need a weapon. I've never needed a weapon.",
            "stats": {"STR": 11, "DEX": 14, "CON": 13, "INT": 11, "WIS": 18, "PIE": 10},
            "_char": None,
        },
    ],
}


# ═══════════════════════════════════════════════════════════════
#  PER-TOWN TAVERN PATRONS
# ═══════════════════════════════════════════════════════════════

TOWN_TAVERN_PATRONS = {
    "briarhollow": TAVERN["patrons"],   # default — used as fallback too

    "woodhaven": [
        {
            "name": "Petra the Trapper",
            "role": "trapper",
            "description": "A leathery woman who sets snares in the Thornwood.",
            "color": (140, 160, 110),
            "sober": [
                "Spiders are getting bigger out there. Saw one drag off a hare last week.",
                "The Thornwood used to be safe after dawn. Not anymore.",
                "If you're heading northwest, don't go alone.",
            ],
            "drunk": [
                "I told the Rangers. They wrote it down. Nothing happened. I hate it here.",
                "My grandmother saw the Greying once — that's what she called it. Said it smelled like rain before a storm. Dry rain.",
                "There's something in the web cave that isn't a spider. Bigger. Quieter.",
            ],
        },
        {
            "name": "Corvin the Scout",
            "role": "ranger",
            "description": "An off-duty Warden scout with ink-stained fingers and tired eyes.",
            "color": (100, 140, 120),
            "sober": [
                "I've mapped every trail in the Thornwood. The northwest one I won't walk again.",
                "The Order doesn't have the people it used to. We're spread thin.",
                "Don't mistake quiet for safe.",
            ],
            "drunk": [
                "There are Warden patrol markers on trees the Rangers don't know about. I know what they mean. Not sharing.",
                "Someone's been maintaining the old ward-stones in secret. Not us. Not the mages. Someone else.",
                "I found a camp east of the Thornwood. Fresh fire. Warden colours. Nobody there.",
            ],
        },
        {
            "name": "Nessa",
            "role": "woodcutter",
            "description": "A young woodcutter taking a break from a long shift.",
            "color": (190, 155, 100),
            "sober": [
                "Work's good if you don't mind the quiet.",
                "The trees at the forest edge are going wrong. Grey bark. Won't burn right.",
                "I just want a drink and not to think about it.",
            ],
            "drunk": [
                "My father says the forest used to sing. I don't know what that means but I believe him.",
                "Saw something last week between the trees. Just standing there. Not moving. Not anything I know.",
                "Druid Rowan prays every morning at the old oak. She thinks nobody sees. We all see.",
            ],
        },
    ],

    "ironhearth": [
        {
            "name": "Harn the Forgehand",
            "role": "forgehand",
            "description": "A thick-armed dwarf with scorched knuckles and a permanent squint.",
            "color": (180, 130, 70),
            "sober": [
                "Three furnaces running tonight. Don't tell me about tired.",
                "The ore from the eastern veins is coming up grey. Something's wrong with the seams.",
                "You want conversation, buy a drink. You want quiet, buy two.",
            ],
            "drunk": [
                "Twenty years ago the deep veins sang. Now they just groan. The forgemasters pretend not to hear.",
                "I was in the mine when they sealed it. Fifteen years ago. We ran. I didn't look back. I should have looked back.",
                "The Fading doesn't care about iron or stone. My granddad built this hall to last forever. Nothing lasts forever.",
            ],
        },
        {
            "name": "Elswyn the Cartographer",
            "role": "cartographer",
            "description": "A precise woman with rolled maps in every pocket.",
            "color": (160, 170, 130),
            "sober": [
                "The eastern roads have shifted. Literally — landmarks that were there last season aren't.",
                "I'm updating six maps. They were current six months ago. The world moves faster now.",
                "Ask me about roads. Don't ask me about what I've found at the end of them.",
            ],
            "drunk": [
                "Two villages I've mapped aren't there anymore. Not abandoned — gone. The ground is wrong where they were.",
                "There's a road north of the mine that doesn't appear on any charter. Old paving. Warden work. Where does it go? I've been trying not to find out.",
                "My mentor said the Fading takes edges first. Borders, thresholds, shorelines. Then it comes for the middle.",
            ],
        },
        {
            "name": "Brek",
            "role": "miner",
            "description": "A young miner who doesn't look like he's slept in days.",
            "color": (130, 115, 100),
            "sober": [
                "New shift in two hours. Just getting warm.",
                "Heard noises in shaft three. Foreman says it's the rock settling. Foreman wasn't in shaft three.",
                "Don't go near the sealed section. Even the rats don't.",
            ],
            "drunk": [
                "Something tapped on my helmet from inside a sealed wall last month. Three times. Evenly spaced.",
                "We found tools in the deep section. Old tools. The kind the garrison would have used. Fifteen years they've been down there and they're still sharp.",
                "The mine wants to be left alone. I know that sounds mad. But it wants to be left alone.",
            ],
        },
    ],

    "greenwood": [
        {
            "name": "Farren the Huntsman",
            "role": "huntsman",
            "description": "A lean man who speaks carefully and misses nothing.",
            "color": (120, 155, 100),
            "sober": [
                "Game's moving east. Something's pushing it out of the western valleys.",
                "The Fading boundary is two leagues closer than it was in spring.",
                "Ask me what I've seen. Don't ask me what I think it means.",
            ],
            "drunk": [
                "I tracked a Fading-touched stag for three days. When I caught up to it, it was standing still at the boundary edge. Waiting. I turned around.",
                "There's a clearing in the western forest where nothing grows anymore. Not even moss. The soil just stopped.",
                "The Warden outpost south of here has been abandoned for a year. Someone's been leaving firewood at the door.",
            ],
        },
        {
            "name": "Sylva",
            "role": "herbalist",
            "description": "A herbalist who knows which mushrooms are which — very precisely.",
            "color": (160, 200, 130),
            "sober": [
                "Half my herb patches have gone grey. Still growing, just wrong.",
                "The remedies I know don't work on Fading sickness. I've been looking for ones that do.",
                "If you find anything unusual growing near the boundary, don't touch it.",
            ],
            "drunk": [
                "I've made something that slows Fading corruption. On plants. I'm working on the rest. Don't tell anyone. The Mage Guild would want it and I'm not ready.",
                "You know what the Fading-touched plants taste like? Nothing. Absolutely nothing. That's the worst part.",
                "There's an old Warden herb garden behind the eastern outpost. Still alive. Still producing. Like it knows what's at stake.",
            ],
        },
    ],

    "saltmere": [
        {
            "name": "Dorin the Sailor",
            "role": "sailor",
            "description": "A weathered mariner nursing something dark and strong.",
            "color": (100, 140, 170),
            "sober": [
                "Three ships gone this season. No storm. No wreck. Just gone.",
                "The sea's wrong east of the pale coast. Colour, depth, current. All of it.",
                "I've sailed these waters twenty years. I won't take passengers past the inlet anymore.",
            ],
            "drunk": [
                "We pulled something up in the net two weeks ago. Not a fish. Not anything with a name I know. We threw it back and said nothing to the harbour master.",
                "The Isle to the west. Something on it is different. The light hits it wrong. Like it's slightly further away than it should be.",
                "Old sailors say the Fading started at sea. That the first thing it took was the horizon.",
            ],
        },
        {
            "name": "Callie the Dockmaster",
            "role": "dockmaster",
            "description": "A sharp-eyed woman who knows every ship in every port.",
            "color": (170, 150, 110),
            "sober": [
                "I track what comes in and goes out. Mostly it balances. Lately it doesn't.",
                "The Imperial agents were here last month. Looking at cargo manifests. Didn't like what they found.",
                "If you need passage east, the Pale Gull will take you. If you can afford her.",
            ],
            "drunk": [
                "The Governor's been moving gold east for six months. Before that it was weapons. Before that it was something I didn't look at closely enough.",
                "There's a courier who arrives here every two weeks with a sealed pouch. Goes straight to the harbour master's office. Never waits for a receipt.",
                "I've been offered a lot of money to stop asking questions. Haven't taken it yet.",
            ],
        },
    ],

    "sanctum": [
        {
            "name": "Brother Aldwyn",
            "role": "pilgrim",
            "description": "A cathedral novice on a supply errand, grateful for a warm corner.",
            "color": (160, 160, 200),
            "sober": [
                "The cathedral has a thousand pilgrims a day now. A month ago it was two hundred.",
                "People come to pray when they don't know what else to do. I understand that.",
                "The Chapter Master says prayer holds the world in shape. I believe that more than I used to.",
            ],
            "drunk": [
                "They brought in a Fading-touched body for study last week. The scholars spent six hours on it. Then they burned it and didn't write down what they found.",
                "There's a vault under the cathedral that nobody opens anymore. The senior brothers avoid walking over it. I've noticed.",
                "Chapter Master Aldren hasn't slept in two weeks. I can tell. Someone who doesn't sleep like that is waiting for something.",
            ],
        },
        {
            "name": "Mira the Scribe",
            "role": "scribe",
            "description": "A cathedral archivist taking a rare evening away from her desk.",
            "color": (190, 180, 220),
            "sober": [
                "Thirty years of records in the cathedral archive. Most of them say the same thing: we knew, and we didn't act.",
                "The Warden histories are technically restricted. They're also the most read documents in the archive. Make of that what you will.",
                "Someone requested everything we had on Valdris three months before the first Fading report. We filled the request. I wish we hadn't.",
            ],
            "drunk": [
                "The Warden Order had a succession plan. Someone was supposed to carry it on. The records are very specific about this. The records don't say who.",
                "I found a prayer in the oldest section of the archive that predates the Cathedral by two centuries. It asks for protection from someone called the Last Warden. That's what it says. The Last Warden.",
                "We have a letter from Valdris. Written forty years ago, when he was still a junior Warden. He writes about the Fading like he already knows what it will do. I've read it fifty times.",
            ],
        },
    ],

    "crystalspire": [
        {
            "name": "Novice Ren",
            "role": "apprentice",
            "description": "A young mage apprentice with chalk dust on everything.",
            "color": (160, 140, 220),
            "sober": [
                "Third failed transmutation today. I'm buying a drink before I try again.",
                "The ley lines are flickering. The senior mages pretend they're not.",
                "Don't ask what my thesis is on. It's embarrassing.",
            ],
            "drunk": [
                "The Archmage ran the numbers three times and got three different answers. That doesn't happen. Arcane math doesn't do that unless the substrate is changing.",
                "I overheard two senior mages arguing about whether the Fading is a natural process or an engineered one. The one who said engineered won the argument. They both looked terrified.",
                "My binding circle failed yesterday. First time in two years. The spell didn't go wrong — it just stopped. Like the magic forgot what it was supposed to do.",
            ],
        },
        {
            "name": "Voss the Artificer",
            "role": "artificer",
            "description": "A practical enchanter who repairs more than he creates these days.",
            "color": (140, 170, 200),
            "sober": [
                "Wands are coming in with charge loss I can't explain. Not use — spontaneous drain.",
                "The enchantments I placed on the west gate pillars last year are failing. They were rated for a century.",
                "Magic works differently near the Fading boundary. Not worse. Just differently. That's almost scarier.",
            ],
            "drunk": [
                "I've been quietly reinforcing the city's ward anchors on my own time. Nobody asked me to. Nobody told me to stop.",
                "The Arcane Containment Crystal — the type the Court Mages use? It's not for storage. Not originally. It was designed to capture and hold Fading energy. That's what the old design notes say.",
                "Whoever made the Hearthstones understood something about permanent enchantment that we've lost. I've been trying to reverse-engineer one. The magic is older than the methods we have to study it.",
            ],
        },
    ],

    "thornhaven": [
        {
            "name": "Aldric the Soldier",
            "role": "soldier",
            "description": "An off-duty Imperial soldier who looks like he has regrets.",
            "color": (160, 140, 100),
            "sober": [
                "Don't ask me about the Governor. Off duty.",
                "The eastern roads are dangerous. We've lost two squads this month.",
                "I joined for the structure. I didn't think the structure would look like this.",
            ],
            "drunk": [
                "The Governor knows more than he says. The orders that come down don't make sense unless someone at the top knows what's coming.",
                "We were told to stop a group of travellers carrying ward-stones. We let them through. My squad decided together. None of us reported it.",
                "There's a rumour that the black-cloaks are recruiting. I've heard the pitch. It's compelling if you're scared enough. I'm not. Not yet.",
            ],
        },
        {
            "name": "Innkeeper Brann",   # the famous one
            "role": "innkeeper",
            "description": "The innkeeper of the Silver Anchor, taking a rare seat at someone else's bar.",
            "color": (180, 155, 100),
            "sober": [
                "Strange to be on this side of the counter.",
                "My inn sees everyone who passes through. Lately they all have the same look.",
                "The Fading's close enough to feel now. Not see — feel. Like standing near something very cold.",
            ],
            "drunk": [
                "Twenty years I've run that inn. Never asked questions. Fed people, rested them, sent them on. Lately I find myself asking what happened to them after.",
                "Maren stayed three nights. Barely slept. Kept writing. Left before dawn. Didn't pay — I didn't ask. Some bills you just forgive.",
                "I have guests who fight the Fading and guests who serve it and I can't always tell which is which until they're gone.",
            ],
        },
    ],
}


def get_tavern_patrons(town_id):
    """Return the patron list for the given town, falling back to Briarhollow."""
    return TOWN_TAVERN_PATRONS.get(town_id, TOWN_TAVERN_PATRONS["briarhollow"])


# ═══════════════════════════════════════════════════════════════
#  SELL PRICE CALCULATOR
# ═══════════════════════════════════════════════════════════════

def get_sell_price(item):
    """Calculate sell price for an item. Identified items sell for more."""
    if "sell_price" in item:
        return item["sell_price"]
    # Estimate from buy price or value — coerce to int in case stored as string
    value = item.get("buy_price", item.get("estimated_value", item.get("value", 5)))
    try:
        value = int(value)
    except (TypeError, ValueError):
        value = 5
    if item.get("identified"):
        return max(1, int(value * 0.40))  # 40% for identified items
    else:
        return max(1, int(value * 0.20))  # 20% for unidentified items


# ═══════════════════════════════════════════════════════════════
#  TOWN-SPECIFIC SHOP INVENTORY
# ═══════════════════════════════════════════════════════════════

# Town shop profiles: which categories to stock, price modifiers, bonus items
TOWN_SHOP_PROFILES = {
    "briarhollow": {
        "name": "Briarhollow General Store",
        "welcome": "Welcome to Briarhollow! We've got the basics.",
        "tier": "village",
        "max_weapon_price": 60,   # only cheap weapons
        "max_armor_price": 50,
        "price_mult": 1.0,        # standard prices
        "bonus_items": [
            {"name": "Torch", "type": "consumable", "subtype": "light",
             "rarity": "common", "description": "Lights dark areas. Lasts one floor.",
             "buy_price": 5, "sell_price": 1, "identified": True},
            {"name": "Rope", "type": "consumable", "subtype": "tool",
             "rarity": "common", "description": "50ft of hempen rope.",
             "buy_price": 8, "sell_price": 2, "identified": True},
        ],
    },
    "woodhaven": {
        "name": "Woodhaven Trading Post",
        "welcome": "Forest goods and ranger supplies. Take a look.",
        "tier": "town",
        "max_weapon_price": 100,
        "max_armor_price": 80,
        "price_mult": 0.95,        # slightly cheaper
        "bonus_items": [
            {"name": "Ranger's Cloak", "type": "armor", "slot": "body",
             "rarity": "uncommon", "defense": 3, "magic_resist": 2,
             "description": "A forest cloak that helps avoid detection.",
             "buy_price": 75, "sell_price": 30, "identified": True},
            {"name": "Herbal Poultice", "type": "consumable", "subtype": "potion",
             "rarity": "common", "heal": 35, "cures": ["Poison"],
             "description": "Heals 35 HP and cures mild poison.",
             "buy_price": 30, "sell_price": 12, "identified": True},
            {"name": "Hunter's Bow", "type": "weapon", "slot": "weapon",
             "subtype": "Longbow", "rarity": "uncommon", "damage": 18,
             "phys_type": "piercing", "range": "ranged",
             "description": "A well-crafted forest bow. +1 accuracy.",
             "accuracy_bonus": 5,
             "buy_price": 80, "sell_price": 32, "identified": True},
        ],
    },
    "ironhearth": {
        "name": "Ironhearth Forge & Armory",
        "welcome": "Dwarven steel, finest in Aldenmere. Name your needs.",
        "tier": "city",
        "max_weapon_price": 999,   # everything available
        "max_armor_price": 999,
        "price_mult": 1.10,        # premium prices
        "bonus_items": [
            {"name": "Dwarven War Hammer", "type": "weapon", "slot": "weapon",
             "subtype": "Mace", "rarity": "uncommon", "damage": 14,
             "damage_stat": {"STR": 0.4},
             "phys_type": "blunt", "range": "melee",
             "special": {"armor_bypass": 0.20},
             "description": "Heavy dwarven hammer. Bypasses 20% armor.",
             "buy_price": 120, "sell_price": 50, "identified": True},
            {"name": "Steel Breastplate", "type": "armor", "slot": "body",
             "rarity": "uncommon", "defense": 10, "magic_resist": 2,
             "description": "Solid dwarven steel armor. Premium protection.",
             "buy_price": 150, "sell_price": 60, "identified": True},
            {"name": "Runic Amulet", "type": "accessory", "slot": "ring1",
             "rarity": "uncommon", "magic_resist": 4,
             "stat_bonuses": {"INT": 2},
             "description": "A dwarf-forged amulet inscribed with protective runes.",
             "buy_price": 100, "sell_price": 40, "identified": True},
            {"name": "Greater Healing Potion", "type": "consumable", "subtype": "potion",
             "rarity": "uncommon", "heal": 100,
             "description": "Restores 100 HP to one character.",
             "buy_price": 60, "sell_price": 24, "identified": True},
        ],
    },
    "greenwood": {
        "name": "Greenwood Ranger Supplies",
        "welcome": "Basic supplies. Don't expect luxury out here.",
        "tier": "village",
        "max_weapon_price": 70,
        "max_armor_price": 60,
        "price_mult": 0.90,       # cheaper, remote frontier pricing
        "bonus_items": [
            {"name": "Camouflage Cloak", "type": "armor", "slot": "body",
             "rarity": "common", "defense": 2, "magic_resist": 1,
             "description": "Blends with the forest. Hard to spot at range.",
             "buy_price": 45, "sell_price": 18, "identified": True},
            {"name": "Herbal Antidote", "type": "consumable", "subtype": "potion",
             "rarity": "common", "cures": ["Poison", "Disease"],
             "description": "Brewed from forest roots. Cures poison and disease.",
             "buy_price": 20, "sell_price": 8, "identified": True},
        ],
    },
    "saltmere": {
        "name": "Saltmere Trader",
        "welcome": "Ask no questions, I'll tell no lies. What do you need?",
        "tier": "town",
        "max_weapon_price": 120,
        "max_armor_price": 100,
        "price_mult": 0.85,       # black market discount — some things fell off a ship
        "bonus_items": [
            {"name": "Smuggler's Blade", "type": "weapon", "slot": "weapon",
             "subtype": "Dagger", "rarity": "uncommon", "damage": 14,
             "damage_stat": {"DEX": 0.4},
             "phys_type": "piercing", "range": "melee",
             "special": {"first_strike": True},
             "description": "A thin blade easy to hide. Always strikes first.",
             "buy_price": 90, "sell_price": 36, "identified": True},
            {"name": "Smoke Bomb", "type": "consumable", "subtype": "thrown",
             "rarity": "common",
             "description": "Fills an area with smoke. Enemies lose accuracy for 2 turns.",
             "buy_price": 25, "sell_price": 10, "identified": True},
        ],
    },
    "sanctum": {
        "name": "Sacred Goods of Sanctum",
        "welcome": "May your purchases bring you peace and protection.",
        "tier": "city",
        "max_weapon_price": 150,
        "max_armor_price": 200,
        "price_mult": 1.05,
        "bonus_items": [
            {"name": "Holy Water (Flask)", "type": "consumable", "subtype": "potion",
             "rarity": "uncommon", "damage_undead": 60,
             "description": "Blessed water. Deals 60 holy damage to undead. No effect on living.",
             "buy_price": 35, "sell_price": 14, "identified": True},
            {"name": "Sanctified Shield", "type": "armor", "slot": "offhand",
             "rarity": "uncommon", "defense": 6, "magic_resist": 5,
             "special": {"undead_resist": 0.20},
             "description": "A shield blessed by the High Priest. +20% resist to undead abilities.",
             "buy_price": 140, "sell_price": 56, "identified": True},
            {"name": "Pilgrim's Staff", "type": "weapon", "slot": "weapon",
             "subtype": "Staff", "max_charges": 30, "rarity": "uncommon", "damage": 13,
             "phys_type": "blunt", "range": "melee",
             "special": {"heal_on_kill": 15},
             "description": "A blessed walking staff. Restores 15 HP to the wielder on each kill.",
             "buy_price": 110, "sell_price": 44, "identified": True},
        ],
    },
    "crystalspire": {
        "name": "Components & Curios",
        "welcome": "Rare components and spell tomes. Knowledge has its price.",
        "tier": "city",
        "max_weapon_price": 999,
        "max_armor_price": 999,
        "price_mult": 1.15,       # premium — mage city prices
        "bonus_items": [
            {"name": "Spell Tome: Fireball", "type": "consumable", "subtype": "tome",
             "rarity": "rare", "teaches_spell": "fireball",
             "description": "Teaches the Fireball spell. Mages only.",
             "buy_price": 200, "sell_price": 80, "identified": True},
            {"name": "Crystal Focus", "type": "accessory", "slot": "ring1",
             "rarity": "uncommon", "magic_resist": 3,
             "stat_bonuses": {"INT": 3, "WIS": 1},
             "description": "A crystal lens that sharpens magical focus. +3 INT, +1 WIS.",
             "buy_price": 180, "sell_price": 72, "identified": True},
            {"name": "Mana Vial", "type": "consumable", "subtype": "potion",
             "rarity": "uncommon", "restore_mp": 60,
             "description": "Crystallized mana. Restores 60 MP to one character.",
             "buy_price": 55, "sell_price": 22, "identified": True},
            {"name": "Mana Crystal", "type": "material", "subtype": "reagent",
             "rarity": "uncommon", "quantity": 1,
             "description": "A dense crystal of condensed arcane energy. Recharges 5 charges on a wand, rod, orb, or staff when used at camp or a forge.",
             "buy_price": 50, "sell_price": 20, "identified": True},
            {"name": "Scroll of Identify", "type": "consumable", "subtype": "scroll",
             "rarity": "common",
             "description": "Identifies one unknown item instantly.",
             "buy_price": 30, "sell_price": 12, "identified": True},
            {"name": "Scroll of Remove Curse", "type": "consumable", "subtype": "scroll",
             "effect": "remove_curse", "rarity": "uncommon",
             "description": "Lifts all curses from one character, freeing any cursed equipment.",
             "buy_price": 90, "sell_price": 36, "identified": True},
        ],
    },
    "thornhaven": {
        "name": "Imperial Marketplace",
        "welcome": "The finest goods in Aldenmere. The Governor shops here himself.",
        "tier": "capital",
        "max_weapon_price": 999,
        "max_armor_price": 999,
        "price_mult": 1.20,       # capital prices — everything available but costly
        "bonus_items": [
            {"name": "Imperial Longsword", "type": "weapon", "slot": "weapon",
             "subtype": "Longsword", "rarity": "rare", "damage": 16,
             "damage_stat": {"STR": 0.3, "DEX": 0.12},
             "phys_type": "slashing", "range": "melee",
             "stat_bonuses": {"STR": 1},
             "description": "An imperial-forged blade bearing the seal of Aldenmere. +1 STR.",
             "buy_price": 280, "sell_price": 112, "identified": True},
            {"name": "Aldenmere Plate", "type": "armor", "slot": "body",
             "rarity": "rare", "defense": 14, "magic_resist": 4,
             "description": "Full plate armor from the imperial armory. The finest protection available.",
             "buy_price": 320, "sell_price": 128, "identified": True},
            {"name": "Ring of the Realm", "type": "accessory", "slot": "ring1",
             "rarity": "rare",
             "stat_bonuses": {"STR": 1, "INT": 1, "WIS": 1, "DEX": 1, "CON": 1},
             "description": "Bearing the imperial crest. Grants +1 to all stats.",
             "buy_price": 350, "sell_price": 140, "identified": True},
            {"name": "Elixir of Champions", "type": "consumable", "subtype": "potion",
             "rarity": "rare", "heal": 200, "restore_mp": 100,
             "description": "Restores 200 HP and 100 MP. The finest restorative in the realm.",
             "buy_price": 120, "sell_price": 48, "identified": True},
        ],
    },
}


def get_town_shop(town_id, party_classes=None):
    """Return a shop inventory tailored to the given town.
    Falls back to GENERAL_STORE if town not defined.
    party_classes: list of class names to filter class-specific items.
    """
    from data.advanced_equipment import get_shop_weapons, get_shop_armor, get_shop_accessories
    profile = TOWN_SHOP_PROFILES.get(town_id)
    if not profile:
        return GENERAL_STORE

    max_wpn = profile["max_weapon_price"]
    max_arm = profile["max_armor_price"]
    mult = profile.get("price_mult", 1.0)

    shop = {
        "name": profile["name"],
        "welcome": profile["welcome"],
        "weapons": [],
        "armor": [],
        "consumables": [],
    }

    tier = profile.get("tier", "village")

    # Class-specific weapons from advanced catalog
    seen_names = set()
    for item in get_shop_weapons(tier, party_classes):
        if item["buy_price"] <= max_wpn and item["name"] not in seen_names:
            it = dict(item)
            it["buy_price"] = int(it["buy_price"] * mult)
            it["sell_price"] = it["buy_price"] // 4
            shop["weapons"].append(it)
            seen_names.add(item["name"])

    # Generic weapons from GENERAL_STORE as variety fallback
    for item in GENERAL_STORE.get("weapons", []):
        if item.get("buy_price", 0) <= max_wpn and item["name"] not in seen_names:
            it = dict(item)
            it["buy_price"] = int(it["buy_price"] * mult)
            shop["weapons"].append(it)
            seen_names.add(item["name"])

    # Class-specific armor + accessories
    seen_names = set()
    for item in get_shop_armor(tier, party_classes):
        if item["buy_price"] <= max_arm and item["name"] not in seen_names:
            it = dict(item)
            it["buy_price"] = int(it["buy_price"] * mult)
            it["sell_price"] = it["buy_price"] // 4
            shop["armor"].append(it)
            seen_names.add(item["name"])

    for item in get_shop_accessories(tier, party_classes):
        if item["buy_price"] <= max_arm and item["name"] not in seen_names:
            it = dict(item)
            it["buy_price"] = int(it["buy_price"] * mult)
            it["sell_price"] = it["buy_price"] // 4
            shop["armor"].append(it)
            seen_names.add(item["name"])

    # GENERAL_STORE armor fallback
    for item in GENERAL_STORE.get("armor", []):
        if item.get("buy_price", 0) <= max_arm and item["name"] not in seen_names:
            it = dict(item)
            it["buy_price"] = int(it["buy_price"] * mult)
            shop["armor"].append(it)
            seen_names.add(item["name"])

    # Always include all consumables
    for item in GENERAL_STORE.get("consumables", []):
        it = dict(item)
        it["buy_price"] = int(it["buy_price"] * mult)
        shop["consumables"].append(it)

    # Add bonus items to appropriate category
    for bonus in profile.get("bonus_items", []):
        it = dict(bonus)
        if it.get("type") == "weapon":
            shop["weapons"].append(it)
        elif it.get("type") in ("armor", "accessory"):
            shop["armor"].append(it)
        else:
            shop["consumables"].append(it)

    return shop


# ── Fix missing slot fields on all shop item lists ─────────────
from core.item_slot_fixer import fix_item_list as _fix_items
_fix_items(GENERAL_STORE.get("weapons", []))
_fix_items(GENERAL_STORE.get("armor", []))
_fix_items(GENERAL_STORE.get("accessories", []))
for _town_id, _town_data in TOWN_SHOP_PROFILES.items():
    _fix_items(_town_data.get("bonus_items", []))
    _fix_items(_town_data.get("weapons", []))
    _fix_items(_town_data.get("armor", []))
