"""
Realm of Shadows — Dynamic Tavern Recruits

Generates a roster of adventurers for each town, scaled to the current
party's average level. Recruits are real Character objects with proper
stats, abilities, and equipment — not stat dicts.

Called when the player opens the Adventurers tab in any tavern.
Roster is cached until party average level shifts by 2 or more.
"""

import random

# ═══════════════════════════════════════════════════════════════
#  TOWN ROSTER TEMPLATES
#  Each entry: (name, class_name, race_name, color_rgb, pitch)
# ═══════════════════════════════════════════════════════════════

TOWN_ROSTERS = {
    "briarhollow": [
        ("Tomas",  "Fighter", "Human",    (210, 130,  60), "Did some soldiering up north. It didn't take."),
        ("Nessa",  "Thief",   "Halfling", (130, 180, 130), "Good with locks. And I'm quiet about it."),
        ("Gorum",  "Ranger",  "Half-Orc", (140, 175,  90), "I know the eastern woods. Spiders don't spook me."),
        ("Seela",  "Cleric",  "Human",    (200, 195, 110), "The temple sent me out to do good. Still figuring out what that means."),
    ],
    "woodhaven": [
        ("Brant",  "Ranger",  "Human",    (120, 180,  90), "Grew up in these woods. Spider country doesn't scare me."),
        ("Lirel",  "Mage",    "Elf",      (110, 140, 210), "Three hundred years of theory. Time to test it."),
        ("Corra",  "Thief",   "Human",    (140, 160, 120), "I scout ahead. Find the traps before they find you."),
        ("Durric", "Fighter", "Dwarf",    (200, 150,  70), "Followed the ore seams this far. Might as well keep going."),
    ],
    "ironhearth": [
        ("Kelvar", "Fighter", "Dwarf",    (210, 140,  50), "Swung a pickaxe in every shaft here. A sword's not much different."),
        ("Tira",   "Monk",    "Human",    (160, 130, 195), "The mines teach discipline. So does fighting."),
        ("Oswin",  "Cleric",  "Human",    (195, 185, 100), "The miners needed a healer. Dungeons do too, I expect."),
        ("Vael",   "Mage",    "Gnome",    (100, 160, 200), "Underground acoustics are fascinating. So is evocation."),
    ],
    "greenwood": [
        ("Sylva",  "Ranger",  "Elf",      (100, 195, 120), "The forest speaks. I translate."),
        ("Baren",  "Mage",    "Human",    (110, 155, 170), "Nature magic isn't gentle. Don't let anyone tell you otherwise."),
        ("Tem",    "Thief",   "Halfling", (160, 190, 110), "Learned to move quietly in the canopy. Everything else came natural."),
        ("Wren",   "Cleric",  "Human",    (195, 200, 120), "The old shrines need tending. Some need defending."),
    ],
    "saltmere": [
        ("Crag",   "Fighter", "Half-Orc", (170, 120,  80), "Two tours on merchant ships. Boarding's just a dungeon with waves."),
        ("Mirren", "Thief",   "Human",    (120, 155, 165), "I know who's moving what through this port. Knowledge costs."),
        ("Seff",   "Mage",    "Gnome",    (100, 145, 200), "The sea teaches patience. Magic teaches the rest."),
        ("Lenna",  "Ranger",  "Human",    (130, 185, 110), "Coast guard. Until the shadows started coming in with the tide."),
    ],
    "sanctum": [
        ("Davan",  "Fighter", "Human",    (210, 180,  90), "I took the pilgrim oath. Left out the part where I stop fighting."),
        ("Seraph", "Cleric",  "Elf",      (220, 215, 130), "The divine speaks through me. Sometimes it asks me to hit things."),
        ("Tavin",  "Monk",    "Human",    (160, 125, 200), "Four years in the monastery. One year wondering what it was for."),
        ("Oria",   "Mage",    "Human",    (110, 140, 215), "The Cathedral library has everything. Including the grimoires they hide."),
    ],
    "crystalspire": [
        ("Zara",   "Mage",    "Elf",      (100, 130, 220), "I failed my practical exams. Turns out I'm better at applied magic."),
        ("Torin",  "Fighter", "Human",    (200, 130,  60), "I'm the Academy's security. They forget to pay me sometimes."),
        ("Nym",    "Thief",   "Gnome",    (140, 180, 140), "Information broker. The Academy doesn't know half of what I know."),
        ("Fara",   "Cleric",  "Human",    (210, 200, 110), "Chaplain to the students. They need it more than they admit."),
    ],
    "thornhaven": [
        ("Voss",   "Fighter", "Human",    (200, 120,  50), "Former imperial guard. Discharged for asking questions."),
        ("Renna",  "Ranger",  "Half-Orc", (140, 180,  90), "The empire sends scouts into shadow zones. I survived."),
        ("Cassia", "Mage",    "Human",    (110, 130, 210), "Imperial court mage. Past tense."),
        ("Idris",  "Cleric",  "Dwarf",    (195, 180,  90), "The empire's gods and I had a falling out. The old ones still listen."),
    ],
}

# Fallback if town_id not in TOWN_ROSTERS
_FALLBACK_ROSTER = [
    ("Aldric", "Fighter", "Human",    (200, 120, 60), "Looking for work. Good with a blade."),
    ("Vespa",  "Thief",   "Human",    (120, 160, 140), "Locks, traps, shadows. Whatever you need."),
    ("Sorel",  "Mage",    "Human",    (100, 130, 200), "I can cast. That's more than most."),
    ("Brynn",  "Cleric",  "Human",    (200, 190, 100), "Healer and fighter both. Fair rate."),
]


def _make_recruit_char(name, cls, race, target_level):
    """Build a properly levelled Character for a recruit."""
    from core.character import Character
    from core.classes import get_all_resources, CLASSES
    from core.progression import apply_level_up, xp_for_level, CLASS_TRANSITIONS

    # Use base class for any hybrid/apex target
    base_cls = cls
    if cls not in CLASSES:
        trans = CLASS_TRANSITIONS.get(cls)
        base_cls = trans["base_classes"][0] if trans and trans.get("base_classes") else "Fighter"

    c = Character(name, base_cls, race)
    c.quick_roll(base_cls)
    c.resources = get_all_resources(base_cls, c.stats, 1)

    # Level up to target, auto-assigning primary stat each time
    target_level = max(1, target_level)
    if target_level > 1:
        c.xp = xp_for_level(target_level)
        for _ in range(target_level - 1):
            apply_level_up(c)   # no free_stat → auto-assigns primary stat
        c.resources = get_all_resources(base_cls, c.stats, c.level)

    # Give recruits a bit of starting gold proportional to level
    c.gold = target_level * 8 + random.randint(0, 20)

    return c


def generate_recruits(party, town_id):
    """
    Return a list of recruit dicts for the given town, scaled to party level.
    Each dict has all fields the draw code expects, plus _char = Character.

    Level range: [max(1, avg-1) .. avg+1], each recruit gets a random level
    in that range so they're not all identical.
    """
    if not party:
        avg = 1
    else:
        avg = max(1, round(sum(c.level for c in party) / len(party)))

    lo = max(1, avg - 1)
    hi = avg + 1

    roster = TOWN_ROSTERS.get(town_id, _FALLBACK_ROSTER)
    recruits = []
    rng = random.Random(town_id + str(avg))   # deterministic per town+level

    for name, cls, race, color, pitch in roster:
        level = rng.randint(lo, hi)
        try:
            char = _make_recruit_char(name, cls, race, level)
        except Exception:
            # Never crash the game for recruits
            from core.character import Character
            from core.classes import get_all_resources
            char = Character(name, cls, race)
            char.quick_roll(cls)
            char.resources = get_all_resources(cls, char.stats, 1)

        recruits.append({
            "name":       char.name,
            "race_name":  race,
            "class_name": cls,
            "level":      char.level,
            "color":      color,
            "pitch":      pitch,
            "stats":      {k: char.stats[k] for k in ("STR","DEX","CON","INT","WIS","PIE")},
            "_char":      char,
        })

    return recruits


def avg_party_level(party):
    """Return rounded average party level, or 1 for empty party."""
    if not party:
        return 1
    return max(1, round(sum(c.level for c in party) / len(party)))
