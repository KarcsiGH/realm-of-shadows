"""
Realm of Shadows — Dungeon Visual Effects
Procedural textures, particle system, and atmospheric effects.
"""
import pygame, math, random

# ═══════════════════════════════════════════════════════════════
#  TEXTURE GENERATION (cached)
# ═══════════════════════════════════════════════════════════════

_texture_cache = {}


def gen_wall_texture(theme, w, h):
    """Generate a procedural brick/stone wall texture."""
    key = (id(theme), w, h)
    if key in _texture_cache:
        return _texture_cache[key]

    surf = pygame.Surface((w, h))
    surf.fill(theme["wall"])
    rng = random.Random(hash((w, h, theme["wall"][0])))

    bh = max(8, h // 6)
    bw = max(12, w // 5)

    for row in range(0, h, bh):
        off = bw // 2 if (row // bh) % 2 else 0
        for bx in range(off, w, bw):
            bww = min(bw - 2, w - bx - 1)
            if bww > 4:
                rv = rng.randint(-8, 8)
                bc = tuple(max(0, min(255, c + rv)) for c in theme["wa"])
                pygame.draw.rect(surf, bc, (bx + 1, row + 1, bww, bh - 2))
                pygame.draw.rect(surf, theme["wd"], (bx + 1, row + 1, bww, bh - 2), 1)
        pygame.draw.line(surf, theme["wl"], (0, row), (w, row), 1)

    # Cracks
    crack = tuple(max(0, c - 25) for c in theme["wd"])
    for _ in range(max(1, w * h // 2000)):
        cx, cy = rng.randint(0, w - 1), rng.randint(0, h - 1)
        for _ in range(rng.randint(5, 18)):
            nx = cx + rng.randint(-1, 1)
            ny = cy + rng.randint(0, 2)
            if 0 <= nx < w and 0 <= ny < h:
                surf.set_at((nx, ny), crack)
                cx, cy = nx, ny

    # Moss patches
    moss = tuple(max(0, min(255, c + v)) for c, v in zip(theme["wall"], (-20, 10, -15)))
    for _ in range(max(1, w * h // 5000)):
        mx, my = rng.randint(0, w - 1), rng.randint(0, h - 1)
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx * dx + dy * dy <= 4:
                    px, py = mx + dx, my + dy
                    if 0 <= px < w and 0 <= py < h and rng.random() < 0.5:
                        surf.set_at((px, py), moss)

    _texture_cache[key] = surf
    return surf


# ═══════════════════════════════════════════════════════════════
#  PARTICLE SYSTEM
# ═══════════════════════════════════════════════════════════════

class Particle:
    __slots__ = ('x', 'y', 'vx', 'vy', 'life', 'max_life', 'color', 'size')

    def __init__(self, x, y, vx, vy, life, color, size=2):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.life = self.max_life = life
        self.color = color
        self.size = size


class ParticleSystem:
    """Lightweight ambient particle system."""

    def __init__(self, vp_x, vp_y, vp_w, vp_h):
        self.particles = []
        self.vp_x, self.vp_y = vp_x, vp_y
        self.vp_w, self.vp_h = vp_w, vp_h

    def emit_dust(self, count=1):
        for _ in range(count):
            x = random.randint(self.vp_x + 40, self.vp_x + self.vp_w - 40)
            y = random.randint(self.vp_y + 40, self.vp_y + self.vp_h - 40)
            vx = random.uniform(-0.15, 0.15)
            vy = random.uniform(-0.25, -0.03)
            life = random.uniform(2.0, 5.0)
            br = random.randint(55, 90)
            self.particles.append(Particle(x, y, vx, vy, life, (br, br - 8, br - 16), 1))

    def emit_torch(self, x, y, count=2):
        for _ in range(count):
            px = x + random.randint(-4, 4)
            py = y + random.randint(-8, 0)
            vx = random.uniform(-0.3, 0.3)
            vy = random.uniform(-0.8, -0.2)
            life = random.uniform(0.2, 0.6)
            self.particles.append(
                Particle(px, py, vx, vy, life, (255, random.randint(140, 200), 40), 2))

    def emit_fading(self, count=1):
        """Purple Fading effect particles."""
        for _ in range(count):
            x = random.randint(self.vp_x + 20, self.vp_x + self.vp_w - 20)
            y = random.randint(self.vp_y + 20, self.vp_y + self.vp_h - 20)
            vx = random.uniform(-0.3, 0.3)
            vy = random.uniform(-0.4, 0.4)
            life = random.uniform(1.5, 3.5)
            self.particles.append(
                Particle(x, y, vx, vy, life, (120, 50, 180), 3))

    def update(self, dt_sec):
        alive = []
        for p in self.particles:
            p.life -= dt_sec
            if p.life > 0:
                p.x += p.vx
                p.y += p.vy
                alive.append(p)
        self.particles = alive[-80:]  # cap particle count

    def draw(self, surface):
        for p in self.particles:
            alpha = max(0, min(255, int(200 * (p.life / p.max_life))))
            s = pygame.Surface((p.size * 2, p.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*p.color[:3], alpha), (p.size, p.size), p.size)
            surface.blit(s, (int(p.x) - p.size, int(p.y) - p.size))


def draw_vignette(surface, vp_x, vp_y, vp_w, vp_h, strength=60):
    """Dark edge vignette for atmosphere."""
    vig = pygame.Surface((vp_w, vp_h), pygame.SRCALPHA)
    depth = 25
    for i in range(depth):
        a = int(strength * (1.0 - i / depth))
        pygame.draw.rect(vig, (0, 0, 0, a), (0, i, vp_w, 1))
        pygame.draw.rect(vig, (0, 0, 0, a), (0, vp_h - 1 - i, vp_w, 1))
        pygame.draw.rect(vig, (0, 0, 0, a), (i, 0, 1, vp_h))
        pygame.draw.rect(vig, (0, 0, 0, a), (vp_w - 1 - i, 0, 1, vp_h))
    surface.blit(vig, (vp_x, vp_y))
