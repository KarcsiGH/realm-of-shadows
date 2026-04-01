"""
sprite_loader.py — PNG sprite loader for Realm of Shadows

Loads AI-generated PNG sprites from assets/sprites/.
Falls back to procedural wiz_sprites.py drawing if file is absent.

Public API (same signatures as wiz_sprites.py):
    draw_character_silhouette(surface, rect, class_name, ...)
    draw_enemy_silhouette(surface, rect, template_key, ...)
"""

import os
import pygame

# ── Paths ────────────────────────────────────────────────────────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))
_BASE = os.path.join(_HERE, '..', 'assets', 'sprites')
_CHAR_DIR  = os.path.normpath(os.path.join(_BASE, 'characters'))
_ENEMY_DIR = os.path.normpath(os.path.join(_BASE, 'enemies'))

# ── Cache ────────────────────────────────────────────────────────────────────
_char_cache:  dict = {}   # class_name → Surface | None
_enemy_cache: dict = {}   # filename   → Surface | None
_effect_cache: dict = {}  # (filename, dead, hover, tier) → Surface

# ── Filename mappings ─────────────────────────────────────────────────────────
# Maps class_name → PNG filename (without .png)
_CHAR_FILES = {
    "Fighter":       "Fighter",
    "Mage":          "Mage",
    "Cleric":        "Cleric",
    "Thief":         "Thief",
    "Ranger":        "Ranger",
    "Monk":          "Monk",
    "Paladin":       "Paladin",
    "Warder":        "Warder",
    "Archmage":      "Archmage",
    "Necromancer":   "Necromancer",
    "Spellblade":    "Spellblade",
    "Champion":      "Champion",
    "Assassin":      "Assassin",
    "Warden":        "Warden",
    "Witch":         "Witch",
    "Beastlord":     "Beastlord",
    "Crusader":      "Crusader",
    "High Priest":   "High_Priest",
    "Shadow Master": "Shadow_Master",
    "Templar":       "Templar",
}

# Maps template_key → PNG filename (without .png)
# Only entries with actual files; everything else falls back to procedural
_ENEMY_FILES = {
    # Direct matches
    "Death Knight":          "Death_Knight",
    "Skeleton Warrior":      "Skeleton_Warrior",
    "Zombie":                "Zombie",
    "Giant Spider":          "Giant_Spider",
    "Marsh Troll":           "Marsh_Troll",
    "Fading Wraith":         "Fading_Wraith",
    "Karreth":               "Karreth",
    "Corrupted Hatchling":   "Corrupted_Hatchling",
    "Stone Sentinel":        "Stone_Sentinel",
    "Fading Cultist":        "Fading_Cultist",
    "Bandit Mage":           "Bandit_Mage",
    "Commander Ashvar":      "Commander_Ashvar",
    "Fading Hound":          "Fading_Hound",
    "Wolf":                  "Wolf",
    "Void Tendril":          "Void_Tendril",
    "Kobold Firebrand":      "Kobold_Firebrand",
    "Cave Bat":              "Cave_Bat",
    "Rabid Rat":             "Rabid_Rat",
    "Swamp Leech":           "Swamp_Leech",
    "Tunnel Lurker":         "Tunnel_Lurker",
    "Shadow Valdris":        "Shadow_Valdris",
    "Valdris the Broken":    "Shadow_Valdris",
    "Valdris, Shadow Avatar":"Shadow_Valdris",
    "Crypt Paladin":         "Crypt_Paladin",
    "High Cultist":          "High_Cultist",
    "Ash Revenant":          "Ash_Revenant",
    "Fading Abomination":    "Fading_Abomination",
    "Fading Bear":           "Fading_Bear",
    # Pass 2 sprites
    "Goblin Warrior":        "Goblin_Warrior",
    "Goblin Archer":         "Goblin_Archer",
    "Goblin Shaman":         "Goblin_Shaman",
    "Goblin Scout":          "Goblin_Shaman",
    "Goblin Drummer":        "Goblin_Shaman",
    "Goblin Trapper":        "Goblin_Shaman",
    "Goblin King":           "Goblin_King",
    "Orc Fighter":           "Orc_Fighter",
    "Bandit":                "Bandit",
    "Highway Bandit":        "Bandit",
    "Ashenmoor Bandit":      "Bandit",
    "Bandit Fighter":        "Bandit_Fighter",
    "Bandit Crossbowman":    "Bandit_Crossbowman",
    "Ruin Archer":           "Bandit_Crossbowman",
    "Ashenmoor Crossbowman": "Bandit_Crossbowman",
    "Bandit Thief":          "Bandit_Thief",
    "Bandit Captain":        "Bandit_Captain",
    "Ghoul":                 "Ghoul",
    "Plague Bearer":         "Ghoul",
    "Drowned Revenant":      "Ghoul",
    "Gargoyle":              "Gargoyle",
    "Cave-in Beetle":        "Cave-in_Beetle",
    "Lava Beetle":           "Cave-in_Beetle",
    "Fungal Crawler":        "Cave-in_Beetle",
    "Egg Sac":               "Egg_Sac",
    "Mercenary Monk":        "Mercenary_Monk",
    "Mercenary War-Cleric":  "Mercenary_War-Cleric",
    # Best-fit matches for remaining procedural enemies
    "Bone Colossus":         "Skeleton_Warrior",
    "Skeletal Archer":       "Skeleton_Warrior",
    "Goblin Brute":          "Goblin_Warrior",    # large goblin, best available
    "Orc Chieftain":         "Orc_Fighter",       # upgrade when pass3 available
    "Imperial Soldier":      "Bandit_Fighter",
    "Imperial Archer":       "Bandit_Crossbowman",
    "Imperial Court Mage":   "Bandit_Mage",
    "Imperial Inquisitor":   "Crypt_Paladin",
    "Pirate Deckhand":       "Bandit_Fighter",
    "Pirate Markswoman":     "Bandit_Crossbowman",
    "Pirate First Mate":     "Bandit_Captain",
    "Pirate Captain":        "Bandit_Captain",
    "Pirate Witch Doctor":   "Bandit_Mage",
    "Mercenary Scout":       "Bandit_Crossbowman",
    "Mercenary Spellblade":  "Bandit_Mage",
    "Sellsword":             "Bandit_Fighter",
    "Crypt Ranger":          "Bandit_Crossbowman",
    "Crypt Archmage":        "High_Cultist",
    "Cultist Hexblade":      "Bandit_Mage",
    "Korrath the Stone Warden": "Stone_Sentinel",
    "The Last Keeper":       "Stone_Sentinel",
    "Stone Guardian":        "Stone_Sentinel",
    "Living Tome":           "Fading_Cultist",
    "Fading Stag":           "Fading_Bear",       # fading large animal
    "Reality Fracture":      "Void_Tendril",
    # Variants sharing the same sprite
    "Volcanic Troll":        "Marsh_Troll",
    "Dire Wolf":             "Wolf",
    "Fading Wolf":           "Wolf",
    "Crypt Shade":           "Fading_Wraith",
    "Dust Wraith":           "Fading_Wraith",
    "Wailing Spirit":        "Fading_Wraith",
    "Shadow Stalker":        "Fading_Wraith",
    "Shadow Brute":          "Fading_Wraith",
    "Isle Shade":            "Fading_Wraith",
    "Saltwater Shade":       "Fading_Wraith",
    "Throne Shade":          "Fading_Wraith",
    "Tide Wraith":           "Fading_Wraith",
    "Wind Wraith":           "Fading_Wraith",
    "Lingering Will":        "Fading_Wraith",
    "Kobold Miner":          "Kobold_Firebrand",
    "Kobold Trapsmith":      "Kobold_Firebrand",
    "Cinder Drake":          "Corrupted_Hatchling",
    "Animated Armor":        "Stone_Sentinel",
    "Mine Golem":            "Stone_Sentinel",
    "Coral Golem":           "Stone_Sentinel",
    "Storm Golem":           "Stone_Sentinel",
    "Flesh Golem":           "Stone_Sentinel",
    "Arcane Sentry":         "Stone_Sentinel",
    "Vault Automaton":       "Stone_Sentinel",
    "Dwarven Forge Guard":   "Stone_Sentinel",
    "Crystal Elemental":     "Stone_Sentinel",
    "Giant Spider Queen":    "Giant_Spider",
    "Broodmother Guard":     "Giant_Spider",
    "Spiderling":            "Giant_Spider",
    "Web Spinner":           "Giant_Spider",
    "Phase Spider":          "Giant_Spider",
    "Venomfang Spider":      "Giant_Spider",
    "Warden Revenant":       "Zombie",
    "Drowned Revenant":      "Zombie",
    "Cultist Warrior":       "Fading_Cultist",
    "Cultist Initiate":      "Fading_Cultist",
    "Cult Sorcerer":         "High_Cultist",
    "Dark Consecrator":      "High_Cultist",
    "Undead Foreman":        "Death_Knight",
    "Ruin Sentinel":         "Death_Knight",
    "Fallen Warden":         "Death_Knight",
    "Oathbreaker Knight":    "Death_Knight",
    "Corrupted Scholar":     "Death_Knight",
    "Crypt Soldier":         "Death_Knight",
    "Imperial Commander":    "Death_Knight",
    "The Pale Sentinel":     "Fading_Wraith",
    "Corrupted Warden Echo": "Fading_Wraith",
    "Stone Warden Ghost":    "Fading_Wraith",
    "Iron Ridge Shade":      "Fading_Wraith",
    "Shadow Warden":         "Fading_Wraith",
    "Warden Shade":          "Fading_Wraith",
    "Tempest Sprite":        "Cave_Bat",
    "Arcane Wisp":           "Cave_Bat",
    "Mine Rat Swarm":        "Rabid_Rat",
    "Tower Rat":             "Rabid_Rat",
    "Fading Boar":           "Fading_Hound",
}


# ── Image loading ─────────────────────────────────────────────────────────────
def _load(path: str) -> pygame.Surface | None:
    """Load a PNG, return Surface or None if file missing."""
    if not os.path.exists(path):
        return None
    try:
        surf = pygame.image.load(path)
        try:
            return surf.convert()
        except Exception:
            return surf  # headless / no display mode
    except Exception:
        return None


def _get_char(class_name: str) -> pygame.Surface | None:
    if class_name not in _char_cache:
        fname = _CHAR_FILES.get(class_name)
        if fname:
            _char_cache[class_name] = _load(
                os.path.join(_CHAR_DIR, fname + '.png'))
        else:
            _char_cache[class_name] = None
    return _char_cache[class_name]


def _get_enemy(template_key: str) -> pygame.Surface | None:
    fname = _ENEMY_FILES.get(template_key)
    if fname is None:
        # Try partial match
        lo = template_key.lower()
        for k, v in _ENEMY_FILES.items():
            if lo in k.lower() or k.lower() in lo:
                fname = v
                break
    if fname is None:
        return None
    if fname not in _enemy_cache:
        _enemy_cache[fname] = _load(
            os.path.join(_ENEMY_DIR, fname + '.png'))
    return _enemy_cache[fname]


# ── Post-processing ───────────────────────────────────────────────────────────
def _apply_effects(surf: pygame.Surface, dead=False,
                   hover=False, tier=-1) -> pygame.Surface:
    """Apply dead/hover/fog tints — same visual contract as wiz_sprites."""
    out = surf.copy()
    try:
        import numpy as np
        arr = pygame.surfarray.pixels3d(out)
        if dead:
            grey = np.clip(
                arr[:,:,0]*0.22 + arr[:,:,1]*0.22 + arr[:,:,2]*0.22 + 14,
                0, 255).astype(np.uint8)
            arr[:,:,0] = grey; arr[:,:,1] = grey
            arr[:,:,2] = np.clip(grey.astype(np.int16)+8, 0, 255).astype(np.uint8)
        elif hover:
            arr[:,:,0] = np.clip(arr[:,:,0].astype(np.int16)+25, 0, 255).astype(np.uint8)
            arr[:,:,1] = np.clip(arr[:,:,1].astype(np.int16)+20, 0, 255).astype(np.uint8)
            arr[:,:,2] = np.clip(arr[:,:,2].astype(np.int16)+15, 0, 255).astype(np.uint8)
        del arr
    except Exception:
        pass

    if tier == -1:
        ov = pygame.Surface(out.get_size(), pygame.SRCALPHA)
        ov.fill((6, 4, 14, 155))
        out.blit(ov, (0, 0))
    return out


# ── Blit helper ───────────────────────────────────────────────────────────────
def _draw_png(surface: pygame.Surface, rect: pygame.Rect,
              src: pygame.Surface, dead=False, hover=False, tier=0) -> None:
    """Scale src to rect (fit-to-height, centre-crop) and blit."""
    sw, sh = src.get_width(), src.get_height()
    # Fit to height
    scale = rect.h / sh
    nw, nh = max(1, int(sw * scale)), rect.h
    scaled = pygame.transform.smoothscale(src, (nw, nh))
    # Centre-crop to rect width
    ox = max(0, (nw - rect.w) // 2)
    crop = pygame.Rect(ox, 0, rect.w, rect.h)
    tmp = pygame.Surface((rect.w, rect.h))
    tmp.fill((6, 6, 10))
    tmp.blit(scaled, (0, 0), crop)
    tmp = _apply_effects(tmp, dead=dead, hover=hover, tier=tier)
    surface.blit(tmp, rect.topleft)


# ── Public API ────────────────────────────────────────────────────────────────
def draw_character_silhouette(surface: pygame.Surface, rect: pygame.Rect,
                               class_name: str, equipped_weapon=None,
                               armor_tier=None, highlight=False) -> bool:
    """
    Draw character sprite. Returns True if PNG was used, False if fell back.
    Fallback is handled by caller (pixel_art.py delegates here first).
    """
    src = _get_char(class_name)
    if src is None:
        return False
    _draw_png(surface, rect, src,
              dead=False, hover=False, tier=highlight and 1 or 0)
    if highlight:
        ov = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        ov.fill((255, 240, 140, 28))
        surface.blit(ov, rect.topleft)
    return True


def draw_enemy_silhouette(surface: pygame.Surface, rect: pygame.Rect,
                           template_key: str, knowledge_tier=0,
                           hover=False, dead=False) -> bool:
    """
    Draw enemy sprite. Returns True if PNG was used, False if fell back.
    """
    src = _get_enemy(template_key)
    if src is None:
        return False
    _draw_png(surface, rect, src,
              dead=dead, hover=hover, tier=knowledge_tier)
    return True
