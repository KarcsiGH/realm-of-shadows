"""
Session 3 fixes — run from your RealmOfShadows folder:
  cd ~/Documents/RealmOfShadows
  python3 fix_session3.py
"""
import os

fixed, failed = [], []

def patch(filepath, old, new, name):
    if not os.path.exists(filepath):
        failed.append(f"{name}: file not found"); return
    with open(filepath) as f: src = f.read()
    if new.strip() in src:
        fixed.append(f"{name}: already applied"); return
    if old not in src:
        failed.append(f"{name}: pattern not found in {filepath}"); return
    with open(filepath, "w") as f: f.write(src.replace(old, new, 1))
    fixed.append(f"{name}: FIXED")

# ── 1. S_CAMP constant collision (was 16, same as S_RACE → triggered char creation) ──
patch("main.py",
    "S_CAMP        = 16   # full camp screen (dungeon/overworld)",
    "S_CAMP        = 22   # full camp screen (dungeon/overworld)",
    "S_CAMP constant (no more char duplication)"
)

# ── 2. No doors on corners ──
patch("data/dungeon.py",
    '''def _pick_door(tiles, candidates, rng):
    """From a list of wall positions in a contiguous corridor segment,
    pick one to become a door (prefer the middle)."""
    if not candidates:
        return
    if rng.random() < 0.3:
        return  # 30% chance no door at all for this entry
    # Pick the middle candidate
    mid = len(candidates) // 2
    x, y = candidates[mid]
    tiles[y][x]["type"] = DT_DOOR''',
    '''def _pick_door(tiles, candidates, rng):
    """From a list of wall positions in a contiguous corridor segment,
    pick one to become a door (prefer the middle). Never place at a corner."""
    if not candidates:
        return
    if rng.random() < 0.3:
        return  # 30% chance no door at all for this entry
    def is_corner(x, y):
        h = len(tiles); w = len(tiles[0])
        neighbors = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
        wall_neighbors = sum(
            1 for nx,ny in neighbors
            if 0<=nx<w and 0<=ny<h and tiles[ny][nx]["type"] == DT_WALL
        )
        return wall_neighbors >= 3
    valid = [(x,y) for x,y in candidates if not is_corner(x,y)]
    if not valid:
        return
    mid = len(valid) // 2
    x, y = valid[mid]
    tiles[y][x]["type"] = DT_DOOR''',
    "No doors at corners"
)

# ── 3. Splitting Arrow — feedback when piercing ──
patch("core/combat_engine.py",
    '''        # Splitting Arrow: also hit mid/back row enemies at reduced power
        if ability.get("pierce_rows") and total_damage > 0 and all_enemies:
            pierced = [e for e in all_enemies
                       if e["alive"] and e["row"] in (MID, BACK) and e not in aoe_targets]
            for ptgt in pierced[:2]:
                pdmg, _, pmsgs = _apply_physical_hit(ptgt, 0.6)
                result["messages"].extend(pmsgs)
                result["damage"] += pdmg
                if not ptgt["alive"]:
                    _log_death(ptgt)''',
    '''        # Splitting Arrow: pierce through front row and hit mid/back enemies
        if ability.get("pierce_rows") and total_damage > 0 and all_enemies:
            pierced = [e for e in all_enemies
                       if e["alive"] and e["row"] in (MID, BACK) and e not in aoe_targets]
            if pierced:
                result["messages"].append(f"The arrow pierces through!")
                for ptgt in pierced[:2]:
                    pdmg, _, pmsgs = _apply_physical_hit(ptgt, 0.6)
                    result["messages"].extend(pmsgs)
                    result["damage"] += pdmg
                    if not ptgt["alive"]:
                        _log_death(ptgt)
            else:
                result["messages"].append(f"No enemies in back rows to pierce.")''',
    "Splitting Arrow pierce feedback"
)

# ── 4. Enemy front-row fix ──
patch("core/combat_engine.py",
    '''        # Ensure at least one enemy is in FRONT — promote the closest row if needed
        alive_enemies = [e for e in self.enemies if e.get("alive", True)]
        rows_used = {e["row"] for e in alive_enemies}
        if rows_used and FRONT not in rows_used:
            # Find the "closest" occupied row and promote it to FRONT
            promote = MID if MID in rows_used else BACK
            for e in self.enemies:
                if e["row"] == promote:
                    e["row"] = FRONT
                    e["preferred_row"] = FRONT''',
    '''        # Ensure at least one enemy is in FRONT — promote the closest row if needed
        alive_enemies = [e for e in self.enemies if e.get("alive", True)]
        rows_used = {e["row"] for e in alive_enemies}
        if rows_used and FRONT not in rows_used:
            promote = MID if MID in rows_used else BACK
            for e in self.enemies:
                if e["row"] == promote:
                    e["row"] = FRONT
                    e["preferred_row"] = FRONT''',
    "Enemy front row fix (already clean)"
)

# ── 4b. Don't remove last FRONT enemy in count variation ──
patch("core/combat_engine.py",
    '''            elif tweak == -1 and len(self.enemies) > 1:
                # Remove a random non-unique enemy
                self.enemies.pop(_rnd.randrange(len(self.enemies)))

        # Scale enemy power to party average level''',
    '''            elif tweak == -1 and len(self.enemies) > 1:
                # Never remove the last FRONT enemy
                front_enemies = [e for e in self.enemies if e["row"] == FRONT]
                removable = self.enemies if len(front_enemies) > 1 else [
                    e for e in self.enemies if e["row"] != FRONT
                ]
                if removable:
                    self.enemies.remove(_rnd.choice(removable))

        # After count variation, ensure FRONT row is still occupied
        alive_after = [e for e in self.enemies if e.get("alive", True)]
        if alive_after and not any(e["row"] == FRONT for e in alive_after):
            promote = MID if any(e["row"] == MID for e in alive_after) else BACK
            for e in self.enemies:
                if e["row"] == promote:
                    e["row"] = FRONT
                    e["preferred_row"] = FRONT
                    break

        # Scale enemy power to party average level''',
    "Never remove last FRONT enemy + post-variation front row check"
)

# ── 5. Sprite visuals ──
patch("ui/dungeon_ui.py",
    '''                elif icon_key in (DT_STAIRS_DOWN, DT_STAIRS_UP, DT_INTERACTABLE):
                    # Stairs — stacked horizontal lines
                    steps = 4
                    sw = max(4, surf_w * 3 // 4)
                    sh = max(2, surf_h // (steps + 1))
                    ox = (surf_w - sw) // 2
                    for si in range(steps):
                        sy_ = surf_h - (si + 1) * (surf_h // steps)
                        iw_ = sw * (si + 1) // steps
                        pygame.draw.rect(spr, c_a, (ox + (sw - iw_)//2, sy_, iw_, max(2, sh)))

                elif icon_key == DT_TREASURE:
                    # Treasure chest — rectangle with lid line
                    cw, ch_ = max(6, surf_w*3//4), max(4, surf_h*3//5)
                    ox, oy = (surf_w-cw)//2, (surf_h-ch_)//2
                    pygame.draw.rect(spr, dim, (ox, oy, cw, ch_), border_radius=2)
                    pygame.draw.rect(spr, c_a, (ox, oy, cw, ch_), 2, border_radius=2)
                    pygame.draw.line(spr, c_a, (ox, oy + ch_//3), (ox+cw, oy + ch_//3), 2)
                    # Lock dot
                    pygame.draw.circle(spr, c_a, (surf_w//2, oy + ch_//2), max(2, r//4))

                elif icon_key in ("enemy", "boss"):
                    # Menacing skull-ish shape
                    er = max(3, r * 3 // 4)
                    pygame.draw.circle(spr, dim, (surf_w//2, surf_h//2 - er//4), er)
                    pygame.draw.circle(spr, c_a, (surf_w//2, surf_h//2 - er//4), er, 2)
                    # Eye dots
                    ew = max(1, er//3)
                    pygame.draw.circle(spr, c_a, (surf_w//2 - er//3, surf_h//2 - er//3), ew)
                    pygame.draw.circle(spr, c_a, (surf_w//2 + er//3, surf_h//2 - er//3), ew)

                elif icon_key == DT_TRAP:
                    # Warning triangle
                    pts = [(surf_w//2, 2), (surf_w-2, surf_h-2), (2, surf_h-2)]
                    pygame.draw.polygon(spr, dim, pts)
                    pygame.draw.polygon(spr, c_a, pts, 2)
                    pygame.draw.line(spr, c_a, (surf_w//2, surf_h//4), (surf_w//2, surf_h*2//3), 2)''',
    '''                elif icon_key == DT_STAIRS_DOWN:
                    # Downward stairs: wide at top, narrow at bottom
                    steps = 5
                    sw = max(6, surf_w * 4 // 5)
                    ox = (surf_w - sw) // 2
                    for si in range(steps):
                        frac = (steps - si) / steps
                        iw_ = max(2, int(sw * frac))
                        sy_ = surf_h - (si + 1) * surf_h // (steps + 1)
                        sh_ = max(2, surf_h // (steps + 2))
                        pygame.draw.rect(spr, dim, (ox + (sw - iw_)//2, sy_, iw_, sh_))
                        pygame.draw.rect(spr, c_a, (ox + (sw - iw_)//2, sy_, iw_, sh_), 1)

                elif icon_key == DT_STAIRS_UP:
                    # Upward stairs: narrow at top, wide at bottom
                    steps = 5
                    sw = max(6, surf_w * 4 // 5)
                    ox = (surf_w - sw) // 2
                    for si in range(steps):
                        frac = (si + 1) / steps
                        iw_ = max(2, int(sw * frac))
                        sy_ = si * surf_h // (steps + 1)
                        sh_ = max(2, surf_h // (steps + 2))
                        pygame.draw.rect(spr, dim, (ox + (sw - iw_)//2, sy_, iw_, sh_))
                        pygame.draw.rect(spr, c_a, (ox + (sw - iw_)//2, sy_, iw_, sh_), 1)

                elif icon_key == DT_INTERACTABLE:
                    # Shrine/fountain: circular basin + vertical pillar
                    bw = max(6, surf_w * 3 // 4)
                    bh = max(3, surf_h // 5)
                    ox = (surf_w - bw) // 2
                    pygame.draw.ellipse(spr, dim, (ox, surf_h - bh - 2, bw, bh))
                    pygame.draw.ellipse(spr, c_a, (ox, surf_h - bh - 2, bw, bh), 2)
                    pw = max(2, surf_w // 6)
                    pygame.draw.rect(spr, dim, ((surf_w - pw)//2, surf_h//4, pw, surf_h//2))
                    pygame.draw.rect(spr, c_a, ((surf_w - pw)//2, surf_h//4, pw, surf_h//2), 1)
                    pygame.draw.circle(spr, c_a, (surf_w//2, surf_h//5), max(2, surf_w//8))

                elif icon_key == DT_TREASURE:
                    # Chest: grounded at floor, wood+metal
                    cw = max(6, surf_w * 3 // 4)
                    ch_ = max(4, surf_h * 2 // 5)
                    ox = (surf_w - cw) // 2
                    oy = surf_h - ch_ - 2
                    pygame.draw.rect(spr, dim, (ox, oy + ch_//3, cw, ch_ * 2//3))
                    pygame.draw.rect(spr, c_a, (ox, oy + ch_//3, cw, ch_ * 2//3), 2)
                    pygame.draw.rect(spr, (int(color[0]*0.7), int(color[1]*0.7), int(color[2]*0.7), alpha),
                                     (ox - 1, oy, cw + 2, ch_//3 + 2), border_radius=1)
                    pygame.draw.rect(spr, c_a, (ox - 1, oy, cw + 2, ch_//3 + 2), 1, border_radius=1)
                    pygame.draw.circle(spr, c_a, (surf_w//2, oy + ch_//2), max(2, cw//8))
                    pygame.draw.line(spr, c_a, (ox, oy + ch_//3 + ch_//4), (ox+cw, oy + ch_//3 + ch_//4), 1)

                elif icon_key in ("enemy", "boss"):
                    # Menacing skull shape
                    er = max(3, r * 3 // 4)
                    pygame.draw.circle(spr, dim, (surf_w//2, surf_h//2 - er//4), er)
                    pygame.draw.circle(spr, c_a, (surf_w//2, surf_h//2 - er//4), er, 2)
                    ew = max(1, er//3)
                    pygame.draw.circle(spr, c_a, (surf_w//2 - er//3, surf_h//2 - er//3), ew)
                    pygame.draw.circle(spr, c_a, (surf_w//2 + er//3, surf_h//2 - er//3), ew)

                elif icon_key == DT_TRAP:
                    # Floor spike plate — ground level
                    pw = max(6, surf_w * 4 // 5)
                    ph = max(3, surf_h // 6)
                    ox = (surf_w - pw) // 2
                    oy = surf_h - ph - 1
                    pygame.draw.rect(spr, dim, (ox, oy, pw, ph))
                    pygame.draw.rect(spr, c_a, (ox, oy, pw, ph), 1)
                    num_spikes = max(3, pw // 5)
                    spike_h = max(3, surf_h // 3)
                    for si in range(num_spikes):
                        sx_ = ox + (si * pw // num_spikes) + pw // (num_spikes * 2)
                        pts = [(sx_-2, oy), (sx_+2, oy), (sx_, oy - spike_h)]
                        pygame.draw.polygon(spr, c_a, pts)''',
    "Sprite visuals: floor spikes, grounded chest, distinct stairs, shrine pillar"
)

print("=" * 55)
for msg in fixed:
    print(f"  {'✓' if 'FIXED' in msg or 'already' in msg else '?'}  {msg}")
for msg in failed:
    print(f"  ✗  {msg}")
print(f"\n{len(fixed)} applied/confirmed, {len(failed)} failed")
if not failed:
    print("\nAll fixes applied! Run: python3 main.py")
