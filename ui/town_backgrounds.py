"""
ui/town_backgrounds.py
======================
Background image loader for town hub and building interiors.

Naming convention:
  assets/backgrounds/towns/{town_id}.png          — town exterior
  assets/backgrounds/buildings/{town_id}_{type}.png — building interior

  e.g.  assets/backgrounds/towns/briarhollow.png
        assets/backgrounds/buildings/briarhollow_inn.png
        assets/backgrounds/buildings/ironhearth_forge.png

All images are loaded once and cached. Missing images return None — the
caller falls back to the plain dark background gracefully.
"""

import pygame
import os

_CACHE: dict = {}   # (town_id, image_type) → Surface | None

_BASE   = os.path.join(os.path.dirname(__file__), '..', 'assets', 'backgrounds')
_TOWNS  = os.path.join(_BASE, 'towns')
_BLDS   = os.path.join(_BASE, 'buildings')


def _load(path: str) -> "pygame.Surface | None":
    """Load and return a surface, or None if the file doesn't exist."""
    if not os.path.isfile(path):
        return None
    try:
        return pygame.image.load(path).convert()
    except Exception:
        return None


def get_town_bg(town_id: str, target_w: int, target_h: int) -> "pygame.Surface | None":
    """Return the exterior background for a town, scaled to target size."""
    key = ("town", town_id, target_w, target_h)
    if key not in _CACHE:
        raw = _load(os.path.join(_TOWNS, f"{town_id}.png"))
        if raw is not None:
            raw = pygame.transform.scale(raw, (target_w, target_h))
        _CACHE[key] = raw
    return _CACHE[key]


def get_building_bg(town_id: str, building_type: str,
                    target_w: int, target_h: int) -> "pygame.Surface | None":
    """Return the interior background for a specific town+building, scaled.

    building_type: 'inn' | 'store' | 'forge' | 'temple' | 'tavern' | 'jobboard'
    Falls back to None if image not found — caller draws plain background.
    """
    key = ("bld", town_id, building_type, target_w, target_h)
    if key not in _CACHE:
        path = os.path.join(_BLDS, f"{town_id}_{building_type}.png")
        raw  = _load(path)
        if raw is not None:
            raw = pygame.transform.scale(raw, (target_w, target_h))
        _CACHE[key] = raw
    return _CACHE[key]


def clear_cache() -> None:
    """Call this on window resize or when backgrounds need reloading."""
    _CACHE.clear()
