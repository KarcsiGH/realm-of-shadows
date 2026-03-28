"""
core/item_slot_fixer.py
Infer and apply missing 'slot' fields to item dicts based on type + subtype.
Called at data-load time so no item reaches the UI without a slot.
"""

# Subtype → slot mapping (case-insensitive key lookup)
SUBTYPE_TO_SLOT = {
    # Weapons — always slot=weapon regardless of subtype
    "dagger": "weapon", "short sword": "weapon", "shortsword": "weapon",
    "long sword": "weapon", "longsword": "weapon", "broadsword": "weapon",
    "greatsword": "weapon", "axe": "weapon", "greataxe": "weapon",
    "mace": "weapon", "hammer": "weapon", "warhammer": "weapon",
    "club": "weapon", "spear": "weapon", "staff": "weapon",
    "wand": "weapon", "rod": "weapon", "orb": "weapon",
    "shortbow": "weapon", "longbow": "weapon", "crossbow": "weapon",
    "sword": "weapon", "blade": "weapon", "pick": "weapon",
    "saber": "weapon", "rapier": "weapon", "scimitar": "weapon",
    "flail": "weapon", "halberd": "weapon", "lance": "weapon",
    "bow": "weapon", "tome": "weapon", "grimoire": "weapon",
    "fetish": "weapon", "scepter": "weapon", "focus": "weapon",
    # Off-hand / shields
    "shield": "off_hand", "buckler": "off_hand", "off_hand": "off_hand",
    "targe": "off_hand",
    # Head
    "helmet": "head", "helm": "head", "crown": "head", "circlet": "head",
    "hat": "head", "hood": "head", "coif": "head", "cap": "head",
    # Body
    "body_armor": "body", "plate": "body", "mail": "body", "chainmail": "body",
    "leather": "body", "robe": "body", "cloak": "body", "vest": "body",
    "breastplate": "body", "coat": "body", "tunic": "body",
    "heavy armor": "body", "heavy_armor": "body",
    # Hands
    "gloves": "hands", "gauntlets": "hands", "bracers": "hands",
    "handwraps": "hands", "mittens": "hands",
    # Feet
    "boots": "feet", "shoes": "feet", "greaves": "feet",
    "sandals": "feet", "sabaton": "feet",
    # Accessories — neck/crown go to specific slots; rings/trinkets use "accessory"
    # so equip_item auto-fills ring1→ring2→ring3
    "ring": "accessory", "band": "accessory",
    "amulet": "neck", "necklace": "neck", "pendant": "neck", "talisman": "neck",
    "holy symbol": "neck",
    "circlet": "crown", "diadem": "crown", "coronet": "crown",
    "trinket": "accessory", "charm": "accessory", "totem": "accessory",
    "coin": "accessory", "seal": "accessory", "beads": "accessory",
    "medal": "accessory", "token": "accessory",
}

def infer_slot(item):
    """Return the correct slot string for an item, or '' if not equippable."""
    itype   = item.get("type", "").lower()
    subtype = item.get("subtype", "").lower()

    if itype == "weapon":
        return "weapon"

    if itype == "armor":
        # Try subtype lookup first
        slot = SUBTYPE_TO_SLOT.get(subtype, "")
        if slot:
            return slot
        # Fallback by subtype keywords
        for kw, sl in [("shield","off_hand"),("buckler","off_hand"),
                       ("helm","head"),("crown","head"),("circlet","head"),
                       ("boot","feet"),("shoe","feet"),("greave","feet"),
                       ("glove","hands"),("gauntlet","hands"),("bracer","hands"),
                       ("robe","body"),("plate","body"),("mail","body"),
                       ("cloak","body"),("vest","body"),("leather","body")]:
            if kw in subtype:
                return sl
        return "body"   # default armor slot

    if itype == "accessory":
        # Neck/crown → specific fixed slots
        if any(kw in subtype for kw in ("amulet","necklace","pendant","talisman","holy symbol")):
            return "neck"
        if any(kw in subtype for kw in ("circlet","crown","diadem","coronet")):
            return "crown"
        # Rings, trinkets, charms, coins, beads etc → generic "accessory"
        # so equip_item auto-fills ring1 → ring2 → ring3
        return "accessory"

    return ""   # consumables, materials, key items — no slot


def ensure_slot(item):
    """Add 'slot' to item in-place if it's missing and equippable. Returns item."""
    if item.get("slot"):
        return item   # already set
    slot = infer_slot(item)
    if slot:
        item["slot"] = slot
    return item


def fix_loot_table(loot_table):
    """Apply ensure_slot to every item in a loot_table list."""
    for drop in (loot_table or []):
        item = drop.get("item")
        if isinstance(item, dict):
            ensure_slot(item)
    return loot_table


def fix_item_list(items):
    """Apply ensure_slot to a flat list of item dicts."""
    for item in (items or []):
        if isinstance(item, dict):
            ensure_slot(item)
    return items
