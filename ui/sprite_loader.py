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
_NPC_DIR   = os.path.normpath(os.path.join(_BASE, 'npcs'))

# ── Cache ────────────────────────────────────────────────────────────────────
_char_cache:  dict = {}   # class_name → Surface | None
_enemy_cache: dict = {}   # filename   → Surface | None
_npc_cache:   dict = {}   # npc_name   → Surface | None
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
    # ── Direct / unique sprite matches ──────────────────────────────────────
    "Death Knight":             "Death_Knight",
    "Skeleton Warrior":         "Skeleton_Warrior",
    "Skeletal Archer":          "Skeletal_Archer",
    "Bone Colossus":            "Bone_Colossus",
    "Zombie":                   "Zombie",
    "Giant Spider":             "Giant_Spider",
    "Giant Spider Queen":       "Giant_Spider_Queen",
    "Broodmother Guard":        "Broodmother_Guard",
    "Phase Spider":             "Phase_Spider",
    "Venomfang Spider":         "Venomfang_Spider",
    "Spiderling":               "Giant_Spider",
    "Web Spinner":              "Giant_Spider",
    "Marsh Troll":              "Marsh_Troll",
    "Volcanic Troll":           "Volcanic_Troll",
    "Fading Wraith":            "Fading_Wraith",
    "Karreth":                  "Karreth",
    "Corrupted Hatchling":      "Corrupted_Hatchling",
    "Cinder Drake":             "Cinder_Drake",
    "Stone Sentinel":           "Stone_Sentinel",
    "Stone Guardian":           "Stone_Guardian",
    "Animated Armor":           "Animated_Armor",
    "Vault Automaton":          "Vault_Automaton",
    "Arcane Sentry":            "Arcane_Sentry",
    "Storm Golem":              "Storm_Golem",
    "Coral Golem":              "Coral_Golem",
    "Crystal Elemental":        "Crystal_Elemental",
    "Mine Golem":               "Stone_Sentinel",
    "Dwarven Forge Guard":      "Dwarven_Forge_Guard",
    "Fading Cultist":           "Fading_Cultist",
    "Cultist Warrior":          "Cultist_Warrior",
    "Cultist Initiate":         "Fading_Cultist",
    "Bandit Mage":              "Bandit_Mage",
    "Commander Ashvar":         "Commander_Ashvar",
    "Fading Hound":             "Fading_Hound",
    "Wolf":                     "Wolf",
    "Dire Wolf":                "Dire_Wolf",
    "Fading Wolf":              "Fading_Wolf",
    "Void Tendril":             "Void_Tendril",
    "Reality Fracture":         "Reality_Fracture",
    "Kobold Firebrand":         "Kobold_Firebrand",
    "Kobold Miner":             "Kobold_Firebrand",
    "Kobold Trapsmith":         "Kobold_Firebrand",
    "Cave Bat":                 "Cave_Bat",
    "Tempest Sprite":           "Tempest_Sprite",
    "Arcane Wisp":              "Arcane_Wisp",
    "Rabid Rat":                "Rabid_Rat",
    "Mine Rat Swarm":           "Rabid_Rat",
    "Tower Rat":                "Rabid_Rat",
    "Swamp Leech":              "Swamp_Leech",
    "Tunnel Lurker":            "Tunnel_Lurker",
    "Shadow Valdris":           "Shadow_Valdris",
    "Valdris the Broken":       "Shadow_Valdris",
    "Valdris, Shadow Avatar":   "Shadow_Valdris",
    "Lingering Will":           "Lingering_Will",
    "Crypt Paladin":            "Crypt_Paladin",
    "Imperial Inquisitor":      "Imperial_Inquisitor",
    "High Cultist":             "High_Cultist",
    "Cult Sorcerer":            "Cult_Sorcerer",
    "Dark Consecrator":         "Cult_Sorcerer",
    "Crypt Archmage":           "Cult_Sorcerer",
    "Living Tome":              "Living_Tome",
    "Ash Revenant":             "Ash_Revenant",
    "Fading Abomination":       "Fading_Abomination",
    "Corrupted Treant":         "Corrupted_Treant",
    "Fading Bear":              "Fading_Bear",
    "Fading Stag":              "Fading_Stag",
    "Fading Boar":              "Fading_Boar",
    "Goblin Warrior":           "Goblin_Warrior",
    "Goblin Brute":             "Goblin_Brute",
    "Goblin Archer":            "Goblin_Archer",
    "Goblin Shaman":            "Goblin_Shaman",
    "Goblin Scout":             "Goblin_Shaman",
    "Goblin Drummer":           "Goblin_Shaman",
    "Goblin Trapper":           "Goblin_Shaman",
    "Goblin King":              "Goblin_King",
    "Orc Fighter":              "Orc_Fighter",
    "Orc Chieftain":            "Orc_Chieftain",
    "Bandit":                   "Bandit",
    "Highway Bandit":           "Bandit",
    "Ashenmoor Bandit":         "Bandit",
    "Bandit Fighter":           "Bandit_Fighter",
    "Bandit Crossbowman":       "Bandit_Crossbowman",
    "Bandit Archer":            "Bandit_Crossbowman",
    "Ruin Archer":              "Skeletal_Archer",
    "Ashenmoor Crossbowman":    "Bandit_Crossbowman",
    "Bandit Thief":             "Bandit_Thief",
    "Bandit Captain":           "Bandit_Captain",
    "Ghoul":                    "Ghoul",
    "Plague Bearer":            "Plague_Bearer",
    "Drowned Revenant":         "Drowned_Revenant",
    "Warden Revenant":          "Warden_Revenant",
    "Gargoyle":                 "Gargoyle",
    "Cave-in Beetle":           "Cave-in_Beetle",
    "Lava Beetle":              "Lava_Beetle",
    "Fungal Crawler":           "Fungal_Crawler",
    "Egg Sac":                  "Egg_Sac",
    "Mercenary Monk":           "Mercenary_Monk",
    "Mercenary War-Cleric":     "Mercenary_War-Cleric",
    "Flesh Golem":              "Flesh_Golem",
    "Imperial Soldier":         "Imperial_Soldier",
    "Imperial Commander":       "Imperial_Commander",
    "Sellsword":                "Sellsword",
    "Pirate Captain":           "Pirate_Captain",
    # ── Warden undead — now unique sprites ──────────────────────────────────
    "Fallen Warden":            "Fallen_Warden",
    "Oathbreaker Knight":       "Oathbreaker_Knight",
    "Korrath the Stone Warden": "Korrath_Stone_Warden",
    "Undead Foreman":           "Undead_Foreman",
    "Ruin Sentinel":            "Death_Knight",
    "Crypt Soldier":            "Death_Knight",
    "Corrupted Scholar":        "Death_Knight",
    # ── Shadow enemies — now unique sprites ─────────────────────────────────
    "Shadow Brute":             "Shadow_Brute",
    "Shadow Warden":            "Shadow_Warden",
    "Shadow Stalker":           "Shadow_Stalker",
    "Iron Ridge Shade":         "Iron_Ridge_Shade",
    "Stone Warden Ghost":       "Stone_Warden_Ghost",
    "The Pale Sentinel":        "The_Pale_Sentinel",
    "The Last Keeper":          "The_Last_Keeper",
    # ── Still sharing Fading_Wraith ─────────────────────────────────────────
    "Crypt Shade":              "Fading_Wraith",
    "Dust Wraith":              "Fading_Wraith",
    "Wailing Spirit":           "Fading_Wraith",
    "Isle Shade":               "Fading_Wraith",
    "Saltwater Shade":          "Fading_Wraith",
    "Throne Shade":             "Fading_Wraith",
    "Tide Wraith":              "Fading_Wraith",
    "Wind Wraith":              "Fading_Wraith",
    "Corrupted Warden Echo":    "Fading_Wraith",
    "Warden Shade":             "Fading_Wraith",
    # ── Boss special ────────────────────────────────────────────────────────
    "Lingering Will":           "Lingering_Will",
    "Warden Revenant":          "Warden_Revenant",
    # ── Remaining best-fit (reasonable shares) ───────────────────────────────
    "Imperial Archer":          "Bandit_Crossbowman",
    "Imperial Court Mage":      "Bandit_Mage",
    "Pirate Deckhand":          "Bandit_Fighter",
    "Pirate Markswoman":        "Bandit_Crossbowman",
    "Pirate First Mate":        "Bandit_Captain",
    "Pirate Witch Doctor":      "Bandit_Mage",
    "Mercenary Scout":          "Bandit_Crossbowman",
    "Mercenary Spellblade":     "Bandit_Mage",
    "Crypt Ranger":             "Bandit_Crossbowman",
    "Cultist Hexblade":         "Bandit_Mage",
}



# ── Image loading ─────────────────────────────────────────────────────────────
def _load(path: str) -> pygame.Surface | None:
    """Load a PNG, return Surface or None if file missing."""
    if not os.path.exists(path):
        return None
    try:
        surf = pygame.image.load(path)
        try:
            return surf.convert_alpha()   # preserve transparency
        except Exception:
            return surf
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
    """Scale src to rect (fit-to-height, centre-crop) and blit with alpha."""
    sw, sh = src.get_width(), src.get_height()
    # Fit to height
    scale = rect.h / sh
    nw, nh = max(1, int(sw * scale)), rect.h
    scaled = pygame.transform.smoothscale(src, (nw, nh))
    # Centre-crop to rect width onto transparent surface
    ox = max(0, (nw - rect.w) // 2)
    crop = pygame.Rect(ox, 0, rect.w, rect.h)
    tmp = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
    tmp.fill((0, 0, 0, 0))           # fully transparent base
    tmp.blit(scaled, (0, 0), crop)
    tmp = _apply_effects(tmp, dead=dead, hover=hover, tier=tier)
    surface.blit(tmp, rect.topleft)


# ── Public API ────────────────────────────────────────────────────────────────
def _get_npc(npc_name: str) -> pygame.Surface | None:
    """Load NPC portrait PNG. Filename: NPC name with spaces→underscores."""
    if npc_name not in _npc_cache:
        fname = npc_name.replace(' ', '_').replace("'", '').replace(',', '')
        path = os.path.join(_NPC_DIR, fname + '.png')
        _npc_cache[npc_name] = _load(path)
    return _npc_cache[npc_name]


def draw_npc_portrait(surface: pygame.Surface, rect: pygame.Rect,
                      npc_name: str, hover=False) -> bool:
    """
    Draw NPC portrait PNG. Returns True if PNG used, False if no file found.
    Caller handles fallback.
    """
    src = _get_npc(npc_name)
    if src is None:
        return False
    _draw_png(surface, rect, src, dead=False, hover=hover, tier=0)
    return True


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
