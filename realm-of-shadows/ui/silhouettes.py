"""
Realm of Shadows — Procedural Silhouette Renderer

Draws class-specific character and enemy silhouettes using pure pygame shapes.
All silhouettes are drawn into a Surface of the requested size and returned.

Character silhouettes reflect:
  - Class archetype (body proportions, stance, held weapon shape)
  - Equipped weapon slot (swapped shape element)
  - Armor tier (affects body bulk)

Enemy silhouettes reflect:
  - Creature type (proportions, posture, distinguishing features)
  - Knowledge tier (low tier = blurry/dim, high tier = crisp and coloured)
"""

import pygame
import math


# ─────────────────────────────────────────────────────────────
#  PALETTE
# ─────────────────────────────────────────────────────────────

_DARK  = (15,  12,  22)
_DIM   = (40,  35,  55)

# Character class accent colours (match CLASSES colors in core/classes.py where possible)
CLASS_COLORS = {
    # Base
    "Fighter":      (180, 100,  60),
    "Mage":         ( 80, 120, 220),
    "Cleric":       (220, 200, 100),
    "Thief":        (100, 180, 120),
    "Ranger":       ( 80, 160,  80),
    "Monk":         (200, 140,  60),
    # Hybrid
    "Warder":       (160,  80,  40),
    "Paladin":      (220, 200, 140),
    "Assassin":     ( 60, 160,  80),
    "Warden":       ( 60, 140,  60),
    "Spellblade":   (100, 100, 200),
    "Templar":      (200, 160,  80),
    # Advanced
    "Champion":     (220, 120,  60),
    "Crusader":     (240, 220, 140),
    "Shadow Master":(  40, 140,  80),
    "Beastlord":    ( 80, 160,  80),
    "Archmage":     ( 80, 100, 240),
    "High Priest":  (240, 220, 160),
    # Special
    "Witch":        (160,  80, 200),
    "Necromancer":  ( 80,  60, 160),
}

# Enemy silhouette tints by knowledge tier
TIER_TINTS = {
    -1: (50, 45, 60),    # unseen — very dim
     0: (80, 75, 95),    # seen   — muted grey-purple
     1: (140,130,150),   # known  — clearer, near-grey
     2: (200,190,210),   # full   — crisp, near-white
}


# ─────────────────────────────────────────────────────────────
#  UTILITY HELPERS
# ─────────────────────────────────────────────────────────────

def _col(base, alpha=255):
    """Return RGBA tuple from RGB."""
    return (*base, alpha)


def _tinted(color, tint, strength=1.0):
    """Blend color toward tint."""
    return tuple(int(c + (t - c) * strength) for c, t in zip(color, tint))


def _surface(w, h):
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    return s


# ─────────────────────────────────────────────────────────────
#  CHARACTER SILHOUETTES
# ─────────────────────────────────────────────────────────────

def draw_character_silhouette(surface, rect, class_name, equipped_weapon=None,
                               armor_tier=None, highlight=False):
    """Draw a character silhouette into rect on surface.
    
    rect: pygame.Rect — where to draw
    class_name: e.g. "Fighter", "Archmage"
    equipped_weapon: weapon dict or None
    armor_tier: "clothing" | "light" | "medium" | "heavy" | None
    highlight: if True, draw with active glow
    """
    spr = _surface(rect.w, rect.h)
    w, h = rect.w, rect.h

    color = CLASS_COLORS.get(class_name, (160, 150, 170))
    if highlight:
        # Brighten for active turn
        color = tuple(min(255, c + 60) for c in color)

    dim = tuple(c // 3 for c in color)

    # Body bulk from armor tier
    bulk = {"clothing": 0, "light": 1, "medium": 2, "heavy": 4}.get(armor_tier or "clothing", 0)

    # Dispatch to class-specific drawer
    drawer = _CHARACTER_DRAWERS.get(class_name, _draw_generic_fighter)
    drawer(spr, w, h, color, dim, bulk, equipped_weapon)

    surface.blit(spr, rect.topleft)


def _head(spr, cx, top, r, color, dim):
    pygame.draw.circle(spr, color, (cx, top + r), r)
    pygame.draw.circle(spr, dim,   (cx, top + r), r, 1)


def _body(spr, cx, top, w, h, color, dim, bulk=0):
    bw = w + bulk * 2
    pygame.draw.rect(spr, color, (cx - bw//2, top, bw, h), border_radius=3)
    pygame.draw.rect(spr, dim,   (cx - bw//2, top, bw, h), 1, border_radius=3)


def _arm(spr, sx, sy, ex, ey, color, thick=2):
    pygame.draw.line(spr, color, (sx, sy), (ex, ey), thick)


def _leg(spr, sx, sy, ex, ey, color, thick=2):
    pygame.draw.line(spr, color, (sx, sy), (ex, ey), thick)


def _sword(spr, x, y, length, angle_deg, color):
    """Draw a sword from base (x,y) at angle."""
    a = math.radians(angle_deg)
    ex = int(x + math.cos(a) * length)
    ey = int(y - math.sin(a) * length)
    pygame.draw.line(spr, color, (x, y), (ex, ey), 2)
    # Guard
    gx = int(x + math.cos(a) * length * 0.25)
    gy = int(y - math.sin(a) * length * 0.25)
    pygame.draw.line(spr, color,
                     (int(gx + math.cos(a + math.pi/2) * 4), int(gy - math.sin(a + math.pi/2) * 4)),
                     (int(gx - math.cos(a + math.pi/2) * 4), int(gy + math.sin(a + math.pi/2) * 4)), 2)


def _staff(spr, x, y, length, color):
    pygame.draw.line(spr, color, (x, y), (x, y - length), 2)
    # Orb at top
    pygame.draw.circle(spr, color, (x, y - length), 4)
    pygame.draw.circle(spr, (255,255,255), (x, y - length), 2)


def _bow(spr, x, y, length, color):
    arc_rect = pygame.Rect(x - 3, y - length, 6, length)
    pygame.draw.arc(spr, color, arc_rect, 0, math.pi, 2)
    pygame.draw.line(spr, color, (x - 3, y - length), (x - 3, y), 1)


def _dagger(spr, x, y, length, color):
    pygame.draw.line(spr, color, (x, y), (x, y - length), 2)
    pygame.draw.line(spr, color, (x - 3, y - length // 3),
                     (x + 3, y - length // 3), 1)


def _shield(spr, x, y, size, color, dim):
    pts = [(x, y - size), (x - size//2, y), (x, y + size//4), (x + size//2, y)]
    pygame.draw.polygon(spr, color, pts)
    pygame.draw.polygon(spr, dim, pts, 1)


# ── Base class drawers ──────────────────────────────────────

def _draw_fighter(spr, w, h, color, dim, bulk, weapon):
    cx = w // 2
    # Head
    hr = max(4, w // 8)
    _head(spr, cx, 2, hr, color, dim)
    # Body — broad shoulders
    by = 2 + hr * 2
    bh = h * 2 // 5
    _body(spr, cx, by, w // 3 + 2, bh, color, dim, bulk)
    # Legs
    legy = by + bh
    legh = h - legy - 2
    _leg(spr, cx - 4, legy, cx - 5, h - 2, color)
    _leg(spr, cx + 4, legy, cx + 5, h - 2, color)
    # Sword arm (raised)
    ax = cx + w // 4
    _sword(spr, ax, by + 4, h // 3, 60, color)
    # Shield arm (left)
    _shield(spr, cx - w // 3, by + bh // 2, w // 8, color, dim)


def _draw_mage(spr, w, h, color, dim, bulk, weapon):
    cx = w // 2
    hr = max(4, w // 9)
    _head(spr, cx, 2, hr, color, dim)
    # Robed body — narrow top, flared robe bottom
    by = 2 + hr * 2
    bh = h * 2 // 5
    # Robe trapezoid
    robe_top = w // 4
    robe_bot = w // 2
    pts = [(cx - robe_top, by), (cx + robe_top, by),
           (cx + robe_bot, h - 2), (cx - robe_bot, h - 2)]
    pygame.draw.polygon(spr, color, pts)
    pygame.draw.polygon(spr, dim, pts, 1)
    # Staff (right side, tall)
    _staff(spr, cx + w // 3, h - 4, h * 3 // 5, color)
    # Floating sparkle
    pygame.draw.circle(spr, (200, 200, 255), (cx - w // 4, by + 4), 2)


def _draw_cleric(spr, w, h, color, dim, bulk, weapon):
    cx = w // 2
    hr = max(4, w // 8)
    _head(spr, cx, 2, hr, color, dim)
    # Body with simple robe
    by = 2 + hr * 2
    bh = h * 2 // 5
    _body(spr, cx, by, w // 3, bh, color, dim, bulk)
    # Robe skirt below body
    pts = [(cx - w//3, by + bh), (cx + w//3, by + bh),
           (cx + w//2, h - 2), (cx - w//2, h - 2)]
    pygame.draw.polygon(spr, color, pts)
    # Cross / holy symbol on chest
    sym_y = by + bh // 3
    pygame.draw.line(spr, dim, (cx, sym_y - 4), (cx, sym_y + 4), 2)
    pygame.draw.line(spr, dim, (cx - 3, sym_y), (cx + 3, sym_y), 2)
    # Mace held up
    _sword(spr, cx + w // 3, by + 4, h // 4, 70, color)


def _draw_thief(spr, w, h, color, dim, bulk, weapon):
    cx = w // 2
    hr = max(3, w // 9)
    # Crouched — head lower, body leaning
    _head(spr, cx + 3, 4, hr, color, dim)
    by = 4 + hr * 2
    bh = h // 3
    # Lean body
    _body(spr, cx + 2, by, w // 4, bh, color, dim, 0)
    # Legs bent
    legy = by + bh
    pygame.draw.line(spr, color, (cx - 2, legy), (cx - 6, legy + h // 5), 2)
    pygame.draw.line(spr, color, (cx - 6, legy + h // 5), (cx - 4, h - 2), 2)
    pygame.draw.line(spr, color, (cx + 5, legy), (cx + 8, legy + h // 5), 2)
    pygame.draw.line(spr, color, (cx + 8, legy + h // 5), (cx + 6, h - 2), 2)
    # Two daggers
    _dagger(spr, cx + w // 3, by + 2, h // 3, color)
    _dagger(spr, cx - 2, by + 4, h // 4, color)


def _draw_ranger(spr, w, h, color, dim, bulk, weapon):
    cx = w // 2
    hr = max(4, w // 8)
    _head(spr, cx, 2, hr, color, dim)
    by = 2 + hr * 2
    bh = h * 2 // 5
    # Lean body
    _body(spr, cx, by, w // 4, bh, color, dim, 0)
    # Legs (walking stance)
    legy = by + bh
    pygame.draw.line(spr, color, (cx - 2, legy), (cx - 4, h - 2), 2)
    pygame.draw.line(spr, color, (cx + 2, legy), (cx + 5, h - 2), 2)
    # Bow
    _bow(spr, cx + w // 3, by + bh // 2, h // 3, color)
    # Arrow nocked
    pygame.draw.line(spr, dim, (cx, by + bh // 3), (cx + w // 3 - 3, by + bh // 2), 1)


def _draw_monk(spr, w, h, color, dim, bulk, weapon):
    cx = w // 2
    hr = max(4, w // 8)
    _head(spr, cx, 2, hr, color, dim)
    by = 2 + hr * 2
    bh = h * 2 // 5
    # Lean body, wide stance
    _body(spr, cx, by, w // 4, bh, color, dim, 0)
    # Fighting stance legs
    legy = by + bh
    pygame.draw.line(spr, color, (cx - 2, legy), (cx - 8, h - 2), 2)
    pygame.draw.line(spr, color, (cx + 2, legy), (cx + 8, h - 2), 2)
    # Raised fist
    arm_x = cx + w // 3
    arm_y = by + 4
    pygame.draw.line(spr, color, (cx + 4, by + bh // 3), (arm_x, arm_y), 2)
    pygame.draw.circle(spr, color, (arm_x, arm_y), 3)
    # Ki aura glow
    pygame.draw.circle(spr, (*color[:3], 60), (cx, by + bh // 2), w // 3)


# ── Hybrid class drawers (mix of base archetypes) ────────────

def _draw_paladin(spr, w, h, color, dim, bulk, weapon):
    # Heavy fighter with holy symbol and glowing aura
    _draw_fighter(spr, w, h, color, dim, bulk + 2, weapon)
    cx = w // 2
    # Halo
    pygame.draw.circle(spr, (*color[:3], 80), (cx, max(4, w // 8) + 2), w // 4)


def _draw_assassin(spr, w, h, color, dim, bulk, weapon):
    # Crouched thief, darker, cloak
    _draw_thief(spr, w, h, color, dim, 0, weapon)
    cx = w // 2
    # Hood / cloak shadow
    pts = [(cx - w//3, 0), (cx + w//3, 0), (cx + w//2, h//2), (cx - w//2, h//2)]
    pygame.draw.polygon(spr, (*dim, 120), pts)


def _draw_spellblade(spr, w, h, color, dim, bulk, weapon):
    # Mage-body + sword
    _draw_mage(spr, w, h, color, dim, bulk, weapon)
    cx = w // 2
    by = 2 + max(4, w//9) * 2
    # Also holds sword
    _sword(spr, cx - w//4, by + 4, h // 3, 120, color)


def _draw_warden(spr, w, h, color, dim, bulk, weapon):
    # Ranger with nature elements — antlers on head
    _draw_ranger(spr, w, h, color, dim, 0, weapon)
    cx = w // 2
    hr = max(4, w // 8)
    # Antler branches
    pygame.draw.line(spr, color, (cx - 2, 2), (cx - 6, -3), 2)
    pygame.draw.line(spr, color, (cx - 6, -3), (cx - 9, 0), 1)
    pygame.draw.line(spr, color, (cx + 2, 2), (cx + 6, -3), 2)
    pygame.draw.line(spr, color, (cx + 6, -3), (cx + 9, 0), 1)


def _draw_warder(spr, w, h, color, dim, bulk, weapon):
    _draw_fighter(spr, w, h, color, dim, bulk + 1, weapon)


def _draw_templar(spr, w, h, color, dim, bulk, weapon):
    _draw_cleric(spr, w, h, color, dim, bulk + 2, weapon)
    cx = w // 2
    hr = max(4, w // 8)
    # Helmet plume
    pygame.draw.line(spr, color, (cx, 0), (cx + 4, -5), 2)


# ── Advanced class drawers ───────────────────────────────────

def _draw_champion(spr, w, h, color, dim, bulk, weapon):
    # Massive fighter — very broad bulk
    _draw_fighter(spr, w, h, color, dim, bulk + 4, weapon)
    cx = w // 2
    # Battle aura
    pygame.draw.circle(spr, (*color[:3], 40), (cx, h // 2), w // 2)


def _draw_archmage(spr, w, h, color, dim, bulk, weapon):
    _draw_mage(spr, w, h, color, dim, 0, weapon)
    cx = w // 2
    # Arcane circle
    pygame.draw.circle(spr, (*color[:3], 50), (cx, h // 2), w // 2 - 2)
    pygame.draw.circle(spr, (*color[:3], 120), (cx, h // 2), w // 2 - 2, 1)
    # Second floating orb
    pygame.draw.circle(spr, (200, 200, 255), (cx - w // 3, h // 3), 3)


def _draw_shadow_master(spr, w, h, color, dim, bulk, weapon):
    _draw_assassin(spr, w, h, color, dim, 0, weapon)
    cx = w // 2
    # Shadow tendrils
    for i in range(3):
        sx = cx + (i - 1) * w // 4
        pygame.draw.line(spr, (*dim, 100), (sx, h * 2 // 3), (sx + (i-1)*4, h - 2), 1)


def _draw_beastlord(spr, w, h, color, dim, bulk, weapon):
    _draw_warden(spr, w, h, color, dim, 1, weapon)
    cx = w // 2
    by = 2 + max(4, w // 8) * 2
    # Fur/cloak shoulders
    pygame.draw.arc(spr, color,
                    pygame.Rect(cx - w//2, by, w, h // 4),
                    0, math.pi, 3)


def _draw_high_priest(spr, w, h, color, dim, bulk, weapon):
    _draw_cleric(spr, w, h, color, dim, bulk + 1, weapon)
    cx = w // 2
    # Radiant crown
    for i in range(5):
        a = math.radians(-90 + i * 36)
        r1, r2 = w // 6, w // 4
        pygame.draw.line(spr, color,
                         (int(cx + math.cos(a) * r1), int(2 + math.sin(a) * r1)),
                         (int(cx + math.cos(a) * r2), int(2 + math.sin(a) * r2)), 1)


def _draw_crusader(spr, w, h, color, dim, bulk, weapon):
    _draw_paladin(spr, w, h, color, dim, bulk + 2, weapon)


# ── Special class drawers ────────────────────────────────────

def _draw_witch(spr, w, h, color, dim, bulk, weapon):
    _draw_mage(spr, w, h, color, dim, 0, weapon)
    cx = w // 2
    # Pointed hat
    hat_pts = [(cx - w//3, max(4, w//9) * 2 + 2),
               (cx + w//3, max(4, w//9) * 2 + 2),
               (cx, -4)]
    pygame.draw.polygon(spr, color, hat_pts)
    pygame.draw.polygon(spr, dim, hat_pts, 1)


def _draw_necromancer(spr, w, h, color, dim, bulk, weapon):
    _draw_mage(spr, w, h, color, dim, 0, weapon)
    cx = w // 2
    # Skull motif
    skull_y = 2 + max(4, w // 9)
    pygame.draw.circle(spr, dim, (cx, skull_y), max(3, w // 10))
    pygame.draw.line(spr, dim, (cx - 2, skull_y + 1), (cx - 2, skull_y + 3), 1)
    pygame.draw.line(spr, dim, (cx + 2, skull_y + 1), (cx + 2, skull_y + 3), 1)


def _draw_generic_fighter(spr, w, h, color, dim, bulk, weapon):
    _draw_fighter(spr, w, h, color, dim, bulk, weapon)


_CHARACTER_DRAWERS = {
    "Fighter":      _draw_fighter,
    "Mage":         _draw_mage,
    "Cleric":       _draw_cleric,
    "Thief":        _draw_thief,
    "Ranger":       _draw_ranger,
    "Monk":         _draw_monk,
    "Warder":       _draw_warder,
    "Paladin":      _draw_paladin,
    "Assassin":     _draw_assassin,
    "Warden":       _draw_warden,
    "Spellblade":   _draw_spellblade,
    "Templar":      _draw_templar,
    "Champion":     _draw_champion,
    "Crusader":     _draw_crusader,
    "Shadow Master":_draw_shadow_master,
    "Beastlord":    _draw_beastlord,
    "Archmage":     _draw_archmage,
    "High Priest":  _draw_high_priest,
    "Witch":        _draw_witch,
    "Necromancer":  _draw_necromancer,
}


# ─────────────────────────────────────────────────────────────
#  ENEMY SILHOUETTES
# ─────────────────────────────────────────────────────────────

def draw_enemy_silhouette(surface, rect, enemy_template_key, knowledge_tier=0,
                           hover=False, dead=False):
    """Draw an enemy silhouette into rect on surface.
    
    Knowledge tier affects clarity and colour:
      -1/0 : blurry grey blob with vague outline
       1   : cleaner shape, muted colour
       2   : full crisp silhouette
    """
    spr = _surface(rect.w, rect.h)
    w, h = rect.w, rect.h

    tier = max(-1, min(2, knowledge_tier))
    tint = TIER_TINTS[tier]

    if dead:
        tint = (50, 45, 55)

    if hover:
        tint = tuple(min(255, c + 40) for c in tint)

    drawer = _ENEMY_DRAWERS.get(enemy_template_key, _draw_enemy_unknown)
    drawer(spr, w, h, tint)

    # Low-tier blur effect: overlay semi-transparent dim layer
    if tier <= 0 and not dead:
        blur = pygame.Surface((w, h), pygame.SRCALPHA)
        blur.fill((10, 8, 20, 160 if tier < 0 else 80))
        spr.blit(blur, (0, 0))

    surface.blit(spr, rect.topleft)


# ── Enemy shape helpers ──────────────────────────────────────

def _draw_enemy_unknown(spr, w, h, c):
    """Generic blob for unrecognized enemy types."""
    cx, cy = w // 2, h // 2
    pygame.draw.ellipse(spr, c, (cx - w//3, cy - h//3, w*2//3, h*2//3))
    pygame.draw.circle(spr, c, (cx, h//5), w//5)


def _draw_goblin_warrior(spr, w, h, c):
    cx = w // 2
    hr = max(3, w // 8)
    # Short, hunched
    _head(spr, cx + 2, h//6, hr, c, tuple(x//2 for x in c))
    hy = h//6 + hr * 2
    # Hunched body
    _body(spr, cx, hy, w//4, h//3, c, tuple(x//2 for x in c), 0)
    # Short legs wide
    pygame.draw.line(spr, c, (cx - 2, hy + h//3), (cx - 6, h - 2), 2)
    pygame.draw.line(spr, c, (cx + 2, hy + h//3), (cx + 6, h - 2), 2)
    # Crude weapon
    pygame.draw.line(spr, c, (cx + w//3, hy), (cx + w//3 + 2, h//3), 2)


def _draw_goblin_archer(spr, w, h, c):
    _draw_goblin_warrior(spr, w, h, c)
    cx = w // 2
    _bow(spr, cx - w//3, h//4, h//3, c)


def _draw_goblin_brute(spr, w, h, c):
    cx = w // 2
    hr = max(4, w // 7)
    _head(spr, cx, h//8, hr, c, tuple(x//2 for x in c))
    hy = h//8 + hr * 2
    # Much wider body
    _body(spr, cx, hy, w//2, h//2, c, tuple(x//2 for x in c), 4)
    pygame.draw.line(spr, c, (cx - 4, hy + h//2), (cx - 8, h - 2), 3)
    pygame.draw.line(spr, c, (cx + 4, hy + h//2), (cx + 8, h - 2), 3)
    # Club
    pygame.draw.line(spr, c, (cx + w//3, hy - 4), (cx + w//2, hy + h//3), 3)
    pygame.draw.circle(spr, c, (cx + w//2, hy + h//3), 4)


def _draw_orc_warrior(spr, w, h, c):
    cx = w // 2
    hr = max(4, w // 7)
    _head(spr, cx, h//10, hr, c, tuple(x//2 for x in c))
    hy = h//10 + hr * 2
    # Wide, muscular
    _body(spr, cx, hy, w//3, h*2//5, c, tuple(x//2 for x in c), 3)
    pygame.draw.line(spr, c, (cx - 4, hy + h*2//5), (cx - 7, h - 2), 3)
    pygame.draw.line(spr, c, (cx + 4, hy + h*2//5), (cx + 7, h - 2), 3)
    _sword(spr, cx + w//3, hy, h//3, 75, c)


def _draw_skeleton_warrior(spr, w, h, c):
    cx = w // 2
    hr = max(3, w // 9)
    # Bony skull
    pygame.draw.circle(spr, c, (cx, h//8 + hr), hr)
    pygame.draw.circle(spr, tuple(x//2 for x in c), (cx, h//8 + hr), hr, 1)
    # Eye sockets
    pygame.draw.circle(spr, tuple(x//3 for x in c), (cx - 2, h//8 + hr - 1), 1)
    pygame.draw.circle(spr, tuple(x//3 for x in c), (cx + 2, h//8 + hr - 1), 1)
    hy = h//8 + hr * 2
    # Ribcage lines
    for i in range(3):
        ry = hy + i * (h // 6)
        pygame.draw.line(spr, c, (cx - w//4, ry), (cx + w//4, ry), 1)
    # Thin arm/leg bones
    pygame.draw.line(spr, c, (cx, hy), (cx, hy + h*2//5), 1)
    pygame.draw.line(spr, c, (cx - 2, hy + h*2//5), (cx - 4, h - 2), 1)
    pygame.draw.line(spr, c, (cx + 2, hy + h*2//5), (cx + 4, h - 2), 1)
    _sword(spr, cx + w//3, hy, h//3, 70, c)


def _draw_zombie(spr, w, h, c):
    cx = w // 2
    hr = max(4, w // 8)
    _head(spr, cx - 2, h//8, hr, c, tuple(x//2 for x in c))
    hy = h//8 + hr * 2
    _body(spr, cx, hy, w//3, h//3, c, tuple(x//2 for x in c), 1)
    # Shambling arm extended
    pygame.draw.line(spr, c, (cx + 4, hy + 4), (cx + w//2, hy - 2), 2)
    pygame.draw.line(spr, c, (cx - 2, hy + h//3), (cx - 4, h - 2), 2)
    pygame.draw.line(spr, c, (cx + 2, hy + h//3), (cx + 4, h - 2), 2)


def _draw_giant_spider(spr, w, h, c):
    cx, cy = w // 2, h // 2
    # Body — two ellipses
    pygame.draw.ellipse(spr, c, (cx - w//4, cy - h//5, w//2, h//3))
    pygame.draw.ellipse(spr, c, (cx - w//5, cy + h//8, w//2//2*2, h//4))
    # 8 legs
    for i in range(4):
        a = math.radians(20 + i * 35)
        lx = int(cx + math.cos(a) * w//2)
        ly = int(cy + math.sin(a) * h//3 - h//8)
        pygame.draw.line(spr, c, (cx + w//5, cy), (lx, ly), 1)
        pygame.draw.line(spr, c, (cx - w//5, cy), (w - lx, ly), 1)


def _draw_troll(spr, w, h, c):
    cx = w // 2
    hr = max(5, w // 6)
    _head(spr, cx, 2, hr, c, tuple(x//2 for x in c))
    hy = 2 + hr * 2
    _body(spr, cx, hy, w//2, h*2//5, c, tuple(x//2 for x in c), 5)
    # Huge arms
    pygame.draw.line(spr, c, (cx - w//2, hy + 4), (cx - w//2 - 4, hy + h//4), 3)
    pygame.draw.line(spr, c, (cx + w//2, hy + 4), (cx + w//2 + 4, hy + h//4), 3)
    # Legs
    pygame.draw.line(spr, c, (cx - 4, hy + h*2//5), (cx - 6, h - 2), 3)
    pygame.draw.line(spr, c, (cx + 4, hy + h*2//5), (cx + 6, h - 2), 3)


def _draw_dark_mage(spr, w, h, c):
    _draw_mage(spr, w, h, c, tuple(x//2 for x in c), 0, None)
    cx = w // 2
    # Dark aura tendrils
    for i in range(4):
        a = math.radians(i * 90 + 45)
        ex = int(cx + math.cos(a) * w//3)
        ey = int(h//2 + math.sin(a) * h//4)
        pygame.draw.line(spr, c, (cx, h//2), (ex, ey), 1)


def _draw_vampire(spr, w, h, c):
    cx = w // 2
    hr = max(4, w // 8)
    _head(spr, cx, h//8, hr, c, tuple(x//2 for x in c))
    hy = h//8 + hr * 2
    # Cape — wide trapezoid
    cape_pts = [(cx - w//4, hy), (cx + w//4, hy),
                (cx + w//2, h - 2), (cx - w//2, h - 2)]
    pygame.draw.polygon(spr, tuple(x//2 for x in c), cape_pts)
    pygame.draw.polygon(spr, c, cape_pts, 1)
    # Fangs
    pygame.draw.line(spr, c, (cx - 2, h//8 + hr * 2), (cx - 2, h//8 + hr * 2 + 3), 1)
    pygame.draw.line(spr, c, (cx + 2, h//8 + hr * 2), (cx + 2, h//8 + hr * 2 + 3), 1)


def _draw_dragon(spr, w, h, c):
    cx, cy = w // 2, h * 2 // 3
    # Body
    pygame.draw.ellipse(spr, c, (cx - w//3, cy - h//4, w*2//3, h//3))
    # Head
    pygame.draw.ellipse(spr, c, (cx + w//4, cy - h//3, w//3, h//5))
    # Wings
    wing_pts_l = [(cx, cy - h//6), (cx - w//2, cy - h//2), (cx - w//4, cy)]
    wing_pts_r = [(cx, cy - h//6), (cx + w//2, cy - h//2), (cx + w//4, cy)]
    pygame.draw.polygon(spr, tuple(x * 2 // 3 for x in c), wing_pts_l)
    pygame.draw.polygon(spr, tuple(x * 2 // 3 for x in c), wing_pts_r)
    pygame.draw.polygon(spr, c, wing_pts_l, 1)
    pygame.draw.polygon(spr, c, wing_pts_r, 1)
    # Tail
    pygame.draw.line(spr, c, (cx - w//3, cy), (cx - w//2, cy + h//4), 2)
    pygame.draw.line(spr, c, (cx - w//2, cy + h//4), (cx - w//3, cy + h//3), 2)


def _draw_abomination(spr, w, h, c):
    cx, cy = w // 2, h // 2
    # Massive irregular blob
    pygame.draw.ellipse(spr, c, (cx - w//2 + 2, cy - h//3, w - 4, h*2//3))
    # Extra limbs
    for i in range(3):
        a = math.radians(i * 60)
        lx = int(cx + math.cos(a) * w//2)
        ly = int(cy + math.sin(a) * h//3)
        pygame.draw.line(spr, c, (cx, cy), (lx, ly), 3)
        pygame.draw.circle(spr, c, (lx, ly), 3)
    # Eyes
    pygame.draw.circle(spr, (255, 80, 80), (cx - 6, cy - 4), 2)
    pygame.draw.circle(spr, (255, 80, 80), (cx + 6, cy - 4), 2)
    pygame.draw.circle(spr, (255, 80, 80), (cx, cy + 4), 2)


def _draw_boss_valdris(spr, w, h, c):
    # Imposing armored figure — like champion fighter but larger
    cx = w // 2
    hr = max(5, w // 7)
    _head(spr, cx, 2, hr, c, tuple(x//2 for x in c))
    hy = 2 + hr * 2
    # Horned helmet
    pygame.draw.line(spr, c, (cx - 4, 2), (cx - 8, -4), 2)
    pygame.draw.line(spr, c, (cx + 4, 2), (cx + 8, -4), 2)
    _body(spr, cx, hy, w//3, h*2//5, c, tuple(x//2 for x in c), 5)
    legy = hy + h*2//5
    pygame.draw.line(spr, c, (cx - 4, legy), (cx - 6, h - 2), 3)
    pygame.draw.line(spr, c, (cx + 4, legy), (cx + 6, h - 2), 3)
    # Great sword
    pygame.draw.line(spr, c, (cx + w//3, hy - 2), (cx + w//3 + 2, h*2//3), 3)
    # Aura
    pygame.draw.circle(spr, (*c, 40), (cx, h//2), w//2)


# Map template keys → drawers
_ENEMY_DRAWERS = {
    "Goblin Warrior":       _draw_goblin_warrior,
    "Goblin Archer":        _draw_goblin_archer,
    "Goblin Brute":         _draw_goblin_brute,
    "Orc Warrior":          _draw_orc_warrior,
    "Skeleton Warrior":     _draw_skeleton_warrior,
    "Zombie":               _draw_zombie,
    "Giant Spider":         _draw_giant_spider,
    "Troll":                _draw_troll,
    "Dark Mage":            _draw_dark_mage,
    "Vampire":              _draw_vampire,
    "Dragon Wyrmling":      _draw_dragon,
    "Abomination":          _draw_abomination,
    "Boss Valdris":         _draw_boss_valdris,
    # Fallback for anything not listed
    "default":              _draw_enemy_unknown,
}

# Allow partial key matching — enemy template keys can have spaces/cases
def get_enemy_drawer(template_key):
    if template_key in _ENEMY_DRAWERS:
        return _ENEMY_DRAWERS[template_key]
    # Try case-insensitive match
    lower = template_key.lower()
    for k, v in _ENEMY_DRAWERS.items():
        if k.lower() == lower:
            return v
    # Try partial match
    for k, v in _ENEMY_DRAWERS.items():
        if lower in k.lower() or k.lower() in lower:
            return v
    return _draw_enemy_unknown
