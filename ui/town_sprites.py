"""
town_sprites.py — Ultima-style pixel art figures for town walk map and world map.

All figures are drawn natively at 16×24px and placed on the tile surface.
No scaling is done — each pixel is intentional at the target size.

Public API:
    draw_npc_figure(surface, cx, cy, tile_size, npc_type, npc_color)
    draw_party_figure(surface, cx, cy, tile_size, facing)
"""

import pygame


# ── NPC type → sprite parameters ─────────────────────────────────────────────
# Maps npc_type string (from town_maps.py) to drawing parameters.
# body_col  : main clothing colour
# hair_col  : hair / fur colour (None = no hair drawn)
# hat       : None | 'pointy' | 'helmet' | 'hood' | 'wide' | 'cap'
# accessory : None | 'apron' | 'sash' | 'robe' | 'pack' | 'staff'

_NPC_PARAMS = {
    "innkeeper":  dict(body_col=(185, 130,  70), hair_col=(120,  80, 40),
                       hat="cap",     accessory="apron"),
    "merchant":   dict(body_col=(100, 140, 180), hair_col=( 60,  45, 30),
                       hat="wide",    accessory="pack"),
    "barkeep":    dict(body_col=(160,  90,  40), hair_col=( 80,  55, 30),
                       hat=None,      accessory="apron"),
    "priestess":  dict(body_col=(230, 225, 190), hair_col=(220, 200, 120),
                       hat="hood",    accessory="robe"),
    "forger":     dict(body_col=(130,  80,  40), hair_col=( 80,  60, 40),
                       hat=None,      accessory="apron"),
    "guildmaster":dict(body_col=( 80, 100, 140), hair_col=( 60,  50, 40),
                       hat="helmet",  accessory="sash"),
    "mage":       dict(body_col=(100,  60, 160), hair_col=(180, 170, 200),
                       hat="pointy",  accessory="robe"),
    "guard":      dict(body_col=(100, 120, 150), hair_col=( 60,  50, 40),
                       hat="helmet",  accessory="sash"),
    "elder":      dict(body_col=(130, 110,  90), hair_col=(200, 195, 185),
                       hat=None,      accessory="staff"),
    "warden":     dict(body_col=( 70, 110,  70), hair_col=( 80,  65, 45),
                       hat=None,      accessory="sash"),
    "youth":      dict(body_col=(160, 180, 140), hair_col=(140, 110,  60),
                       hat=None,      accessory=None),
    # fallback for any unrecognised type
    "default":    dict(body_col=(150, 140, 130), hair_col=(100,  80,  60),
                       hat=None,      accessory=None),
}

# Party figure parameters
_PARTY_PARAMS = dict(
    body_col=( 80,  80, 160),
    hair_col=(100,  75,  45),
    hat=None,
    accessory="sash",
)


# ── Core drawing function ─────────────────────────────────────────────────────

def _draw_figure(surface, ox, oy,
                 body_col, hair_col=None, hat=None, accessory=None,
                 shadow=True):
    """
    Draw a 16×24 Ultima-style pixel art humanoid at pixel offset (ox, oy).
    All coordinates are absolute pixel positions on `surface`.
    """
    # Derived colours
    bc   = body_col
    sc   = tuple(max(0, c - 50) for c in bc)    # body shadow
    hl   = tuple(min(255, c + 20) for c in bc)  # body highlight
    hc   = (215, 185, 150)                       # skin
    hout = tuple(max(0, c - 40) for c in hc)    # skin outline

    # ── Ground shadow ─────────────────────────────────────────────────
    if shadow:
        shd = pygame.Surface((14, 4), pygame.SRCALPHA)
        pygame.draw.ellipse(shd, (0, 0, 0, 55), (0, 0, 14, 4))
        surface.blit(shd, (ox + 1, oy + 21))

    # ── Legs ──────────────────────────────────────────────────────────
    leg   = tuple(max(0, c - 30) for c in bc)
    legdk = tuple(max(0, c - 60) for c in bc)
    # left leg
    pygame.draw.rect(surface, leg,   (ox + 3,  oy + 17, 4, 5))
    pygame.draw.rect(surface, legdk, (ox + 3,  oy + 17, 1, 5))
    # right leg
    pygame.draw.rect(surface, leg,   (ox + 9,  oy + 17, 4, 5))
    pygame.draw.rect(surface, legdk, (ox + 12, oy + 17, 1, 5))
    # feet
    pygame.draw.rect(surface, legdk, (ox + 2,  oy + 21, 5, 1))
    pygame.draw.rect(surface, legdk, (ox + 9,  oy + 21, 5, 1))

    # ── Body ──────────────────────────────────────────────────────────
    pygame.draw.rect(surface, bc, (ox + 3, oy + 9, 10, 9))
    pygame.draw.line(surface, sc, (ox + 3, oy + 9), (ox + 3, oy + 17), 1)
    pygame.draw.line(surface, hl, (ox + 4, oy + 9), (ox + 4, oy + 17), 1)

    # ── Arms ──────────────────────────────────────────────────────────
    pygame.draw.rect(surface, bc, (ox + 1,  oy + 10, 3, 5))
    pygame.draw.rect(surface, sc, (ox + 1,  oy + 10, 1, 5))
    pygame.draw.rect(surface, bc, (ox + 12, oy + 10, 3, 5))
    pygame.draw.rect(surface, hl, (ox + 14, oy + 10, 1, 5))

    # ── Neck ──────────────────────────────────────────────────────────
    pygame.draw.rect(surface, hc, (ox + 6, oy + 7, 4, 3))

    # ── Head ──────────────────────────────────────────────────────────
    pygame.draw.rect(surface, hc,   (ox + 4, oy + 1, 8, 7))
    pygame.draw.rect(surface, hout, (ox + 4, oy + 1, 8, 7), 1)
    pygame.draw.line(surface,
                     tuple(min(255, c + 20) for c in hc),
                     (ox + 5, oy + 2), (ox + 5, oy + 7), 1)   # left highlight
    # eyes
    pygame.draw.rect(surface, (40, 30, 20), (ox + 5, oy + 4, 2, 1))
    pygame.draw.rect(surface, (40, 30, 20), (ox + 9, oy + 4, 2, 1))

    # ── Hair ──────────────────────────────────────────────────────────
    if hair_col:
        pygame.draw.rect(surface, hair_col, (ox + 4,  oy + 1, 8, 2))
        pygame.draw.rect(surface, hair_col, (ox + 4,  oy + 1, 1, 4))
        pygame.draw.rect(surface, hair_col, (ox + 11, oy + 1, 1, 4))

    # ── Hat ───────────────────────────────────────────────────────────
    if hat == "pointy":
        pygame.draw.polygon(surface, bc,
            [(ox + 8, oy - 5), (ox + 3, oy + 1), (ox + 13, oy + 1)])
        pygame.draw.rect(surface, sc, (ox + 2, oy, 12, 2))
    elif hat == "helmet":
        pygame.draw.rect(surface, (130, 140, 160), (ox + 3, oy,     10, 4))
        pygame.draw.rect(surface, (100, 110, 130), (ox + 3, oy,     10, 4), 1)
        pygame.draw.rect(surface, (100, 110, 130), (ox + 5, oy + 3,  6, 2))
    elif hat == "hood":
        vl = pygame.Surface((12, 10), pygame.SRCALPHA)
        pygame.draw.ellipse(vl, (240, 235, 200, 180), (0, 0, 12, 10))
        surface.blit(vl, (ox + 3, oy - 1))
    elif hat == "wide":
        pygame.draw.ellipse(surface,
                            tuple(max(0, c - 30) for c in bc),
                            (ox + 1, oy - 1, 14, 4))
        pygame.draw.rect(surface, bc, (ox + 4, oy - 3, 8, 4))
    elif hat == "cap":
        pygame.draw.rect(surface, (235, 230, 215), (ox + 4, oy, 8, 2))

    # ── Accessory ─────────────────────────────────────────────────────
    if accessory == "apron":
        pygame.draw.rect(surface, (235, 230, 215), (ox + 5, oy + 11, 6, 5))
    elif accessory == "sash":
        pygame.draw.line(surface, (200, 180, 60),
                         (ox + 3, oy + 9), (ox + 12, oy + 17), 2)
    elif accessory == "robe":
        pygame.draw.rect(surface,
                         tuple(max(0, c + 20) for c in bc),
                         (ox + 5, oy + 11, 6, 6))
    elif accessory == "pack":
        pygame.draw.rect(surface, (140, 100,  50), (ox + 12, oy + 9, 3, 5))
        pygame.draw.rect(surface, (100,  70,  30), (ox + 12, oy + 9, 3, 5), 1)
    elif accessory == "staff":
        pygame.draw.line(surface, (160, 120, 60),
                         (ox + 13, oy + 3), (ox + 14, oy + 22), 2)
        pygame.draw.circle(surface, (210, 175, 80), (ox + 13, oy + 3), 2)


# ── Public API ────────────────────────────────────────────────────────────────

def draw_npc_figure(surface, cx, cy, tile_size, npc_type, npc_color):
    """
    Draw an Ultima-style NPC figure centred at pixel (cx, cy).

    Parameters
    ----------
    surface   : pygame.Surface to draw on
    cx, cy    : pixel centre of the tile (not tile coords)
    tile_size : tile size in pixels (used to position the figure)
    npc_type  : npc_type string from town NPC data
    npc_color : color tuple from npc["color"] (used as body_col override
                only for "default" type; named types use their own palette)
    """
    params = dict(_NPC_PARAMS.get(npc_type, _NPC_PARAMS["default"]))

    # For unrecognised types, tint the body with the NPC's colour
    if npc_type not in _NPC_PARAMS:
        params["body_col"] = npc_color

    # Native figure size: 16 wide, 24 tall
    # Place so feet sit near the bottom of the tile
    native_h = 24
    ox = cx - 8                           # centre horizontally (16/2 = 8)
    oy = cy + tile_size // 2 - native_h   # feet near bottom of tile

    _draw_figure(surface, ox, oy, **params)


def draw_party_figure(surface, cx, cy, tile_size, facing):
    """
    Draw the party figure centred at pixel (cx, cy).

    Parameters
    ----------
    surface   : pygame.Surface to draw on
    cx, cy    : pixel centre of the tile
    tile_size : tile size in pixels
    facing    : one of 'up' | 'down' | 'left' | 'right'
    """
    native_h = 24
    ox = cx - 8
    oy = cy + tile_size // 2 - native_h

    _draw_figure(surface, ox, oy, **_PARTY_PARAMS)

    # Facing indicator — small bright dot in the direction the party faces
    _FACING_OFFSET = {
        "up":    (0, -3),
        "down":  (0,  3),
        "left":  (-3, 0),
        "right": ( 3, 0),
    }
    fdx, fdy = _FACING_OFFSET.get(facing, (0, 3))
    # Dot on the head (head top is at oy+1, head centre at oy+4)
    dot_x = cx + fdx
    dot_y = oy + 4 + fdy
    pygame.draw.circle(surface, (255, 240, 120), (dot_x, dot_y), 2)
