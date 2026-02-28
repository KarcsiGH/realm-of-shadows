"""
Run this from your RealmOfShadows folder:
  cd ~/Documents/RealmOfShadows
  python3 apply_all_fixes.py
"""
import os, sys

fixes_applied = []
fixes_failed  = []

def patch(filepath, old, new, name):
    if not os.path.exists(filepath):
        fixes_failed.append(f"{name}: file not found — {filepath}")
        return
    with open(filepath, "r") as f:
        src = f.read()
    if new in src:
        fixes_applied.append(f"{name}: already applied")
        return
    if old not in src:
        fixes_failed.append(f"{name}: old pattern not found in {filepath}")
        return
    src = src.replace(old, new, 1)
    with open(filepath, "w") as f:
        f.write(src)
    fixes_applied.append(f"{name}: FIXED")

# ── 1. classes.py: Ranger starting ability Track → Splitting Arrow ──
patch("core/classes.py",
    '            {"name": "Track", "cost": 5, "resource": "WIS-MP",\n'
    '             "desc": "Locate nearby enemies and resources."},',
    '            {"name": "Splitting Arrow", "cost": 8, "resource": "DEX-SP",\n'
    '             "desc": "Arrow pierces front row, hitting back row too. Reduced damage."},',
    "Ranger Track→Splitting Arrow (classes.py)"
)

# ── 2. abilities.py: Track → Splitting Arrow ──
patch("core/abilities.py",
    '        {"name": "Track",            "cost": 5,  "resource": "WIS-MP", "type": "buff",\n'
    '         "level": 1, "buff": "tracking", "duration": 5, "desc": "Heighten awareness. Reveal hidden enemies."},',
    '        {"name": "Splitting Arrow",  "cost": 8,  "resource": "DEX-SP", "type": "attack",\n'
    '         "level": 1, "power": 0.8, "pierce_rows": True, "desc": "Arrow pierces front row, hitting back row too. Reduced damage."},',
    "Ranger Track→Splitting Arrow (abilities.py)"
)

# ── 3. abilities.py: Arcane Shield self_only ──
patch("core/abilities.py",
    '        {"name": "Arcane Shield",    "cost": 10, "resource": "INT-MP", "type": "buff",\n'
    '         "level": 1, "buff": "magic_shield", "duration": 3, "desc": "Magical barrier absorbing damage."},',
    '        {"name": "Arcane Shield",    "cost": 10, "resource": "INT-MP", "type": "buff",\n'
    '         "level": 1, "buff": "magic_shield", "duration": 3, "self_only": True,\n'
    '         "desc": "Erect a personal arcane barrier. Reduces all damage taken for 3 turns."},',
    "Arcane Shield self_only (abilities.py)"
)

# ── 4. abilities.py: Iron Skin self_only ──
patch("core/abilities.py",
    '        {"name": "Iron Skin",        "cost": 10, "resource": "Ki", "type": "buff",\n'
    '         "level": 1, "buff": "iron_skin", "duration": 3, "desc": "Harden body, reducing physical damage taken."},',
    '        {"name": "Iron Skin",        "cost": 10, "resource": "Ki", "type": "buff",\n'
    '         "level": 1, "buff": "iron_skin", "duration": 3, "self_only": True,\n'
    '         "desc": "Harden the body. Reduces physical damage taken for 3 turns (self only)."},',
    "Iron Skin self_only (abilities.py)"
)

# ── 5. classes.py: Arcane Shield self_only ──
patch("core/classes.py",
    '            {"name": "Arcane Shield", "cost": 10, "resource": "INT-MP",',
    '            {"name": "Arcane Shield", "cost": 10, "resource": "INT-MP", "self_only": True,',
    "Arcane Shield self_only (classes.py)"
)

# ── 6. classes.py: Iron Skin self_only ──
patch("core/classes.py",
    '            {"name": "Iron Skin", "cost": 8, "resource": "Ki",',
    '            {"name": "Iron Skin", "cost": 8, "resource": "Ki", "self_only": True,',
    "Iron Skin self_only (classes.py)"
)

# ── 7. progression.py: Kill trickle regen ──
patch("core/progression.py",
    'def apply_step_regen(character, max_resources):\n'
    '    """Apply per-step resource trickle. Call after each movement step."""\n'
    '    for res_name, current in character.resources.items():\n'
    '        max_val = max_resources.get(res_name, 0)\n'
    '        if max_val <= 0 or current >= max_val:\n'
    '            continue\n'
    '        if res_name == "HP":\n'
    '            gain = max(1, int(max_val * TRICKLE_HP_PCT))\n'
    '        elif "MP" in res_name or res_name == "Ki":\n'
    '            gain = max(1, int(max_val * TRICKLE_MP_PCT))\n'
    '        elif "SP" in res_name:\n'
    '            gain = max(1, int(max_val * TRICKLE_SP_PCT))\n'
    '        else:\n'
    '            continue\n'
    '        character.resources[res_name] = min(max_val, current + gain)',
    'def apply_step_regen(character, max_resources):\n'
    '    """No trickle regen — resources only restored at camp, inn, or via spells/potions."""\n'
    '    pass',
    "Kill trickle regen (progression.py)"
)

# ── 8. main.py: Kill combat music ──
patch("main.py",
    '            sfx.stop_ambient()\n'
    '            sfx.play_music("combat_music")\n'
    '            sfx.play("combat_start")',
    '            sfx.stop_ambient()\n'
    '            sfx.stop_music()\n'
    '            sfx.play("combat_start")',
    "Kill combat music (main.py)"
)

# ── 9. main.py: Kill world/dungeon ambient ──
patch("main.py",
    '            sfx.play_ambient("world_ambient")',
    '            pass  # ambient disabled',
    "Kill world ambient (main.py)"
)
patch("main.py",
    '            sfx.play_ambient("dungeon_ambient")',
    '            pass  # ambient disabled',
    "Kill dungeon ambient (main.py)"
)

# ── 10. combat_engine.py: attack_damage int vs tuple in enemy scale ──
patch("core/combat_engine.py",
    '                    e["attack_damage"] = (\n'
    '                        int(e["attack_damage"][0] * scale),\n'
    '                        int(e["attack_damage"][1] * scale),\n'
    '                    )',
    '                    ad = e["attack_damage"]\n'
    '                    if isinstance(ad, (list, tuple)):\n'
    '                        e["attack_damage"] = (int(ad[0] * scale), int(ad[1] * scale))\n'
    '                    else:\n'
    '                        e["attack_damage"] = (int(ad * scale), int(ad * scale))',
    "attack_damage tuple fix in scaling (combat_engine.py)"
)

# ── 11. combat_engine.py: attack_damage tuple in resolve_enemy_attack ──
patch("core/combat_engine.py",
    '    # Enemy damage: attack_damage + STR scaling + variance - defense\n'
    '    base_dmg = attacker.get("attack_damage", 5)\n'
    '    str_bonus = attacker["stats"].get("STR", 0) * 0.3\n'
    '    raw = (base_dmg + str_bonus) * pos_dmg',
    '    # Enemy damage: attack_damage + STR scaling + variance - defense\n'
    '    ad = attacker.get("attack_damage", 5)\n'
    '    if isinstance(ad, (list, tuple)):\n'
    '        base_dmg = random.randint(int(ad[0]), max(int(ad[0]), int(ad[1])))\n'
    '    else:\n'
    '        base_dmg = int(ad)\n'
    '    str_bonus = attacker["stats"].get("STR", 0) * 0.3\n'
    '    raw = (base_dmg + str_bonus) * pos_dmg',
    "attack_damage tuple in resolve_enemy_attack (combat_engine.py)"
)

# ── 12. combat_engine.py: attack_damage tuple in AI estimate ──
patch("core/combat_engine.py",
    '    estimated_dmg = enemy.get("attack_damage", 5) + enemy["stats"].get("STR", 0) * 0.3',
    '    _ad = enemy.get("attack_damage", 5)\n'
    '    _ad_val = ((_ad[0] + _ad[1]) / 2) if isinstance(_ad, (list, tuple)) else _ad\n'
    '    estimated_dmg = _ad_val + enemy["stats"].get("STR", 0) * 0.3',
    "attack_damage tuple in AI estimate (combat_engine.py)"
)

# ── 13. combat_engine.py: add Splitting Arrow pierce logic ──
patch("core/combat_engine.py",
    '        result["damage"]  = total_damage\n'
    '        result["is_crit"] = any_crit\n'
    '        result["hit"]     = total_damage > 0 or any_crit\n\n'
    '        # Self-damage recoil (Reckless Charge)',
    '        result["damage"]  = total_damage\n'
    '        result["is_crit"] = any_crit\n'
    '        result["hit"]     = total_damage > 0 or any_crit\n\n'
    '        # Splitting Arrow: also hit mid/back row enemies at reduced power\n'
    '        if ability.get("pierce_rows") and total_damage > 0 and all_enemies:\n'
    '            pierced = [e for e in all_enemies\n'
    '                       if e["alive"] and e["row"] in (MID, BACK) and e not in aoe_targets]\n'
    '            for ptgt in pierced[:2]:\n'
    '                pdmg, _, pmsgs = _apply_physical_hit(ptgt, 0.6)\n'
    '                result["messages"].extend(pmsgs)\n'
    '                result["damage"] += pdmg\n'
    '                if not ptgt["alive"]:\n'
    '                    _log_death(ptgt)\n\n'
    '        # Self-damage recoil (Reckless Charge)',
    "Splitting Arrow pierce logic (combat_engine.py)"
)

# ── 14. combat_engine.py: enemy scaling + row fix + count variation ──
patch("core/combat_engine.py",
    '        # Build enemies\n'
    '        self.enemies, self.encounter_name = build_encounter(encounter_key)\n\n'
    '        # Initial turn order',
    '        # Build enemies\n'
    '        self.enemies, self.encounter_name = build_encounter(encounter_key)\n\n'
    '        # If all enemies share the same non-FRONT row, push them to FRONT\n'
    '        alive_enemies = [e for e in self.enemies if e.get("alive", True)]\n'
    '        rows_used = {e["row"] for e in alive_enemies}\n'
    '        if rows_used and FRONT not in rows_used:\n'
    '            for e in self.enemies:\n'
    '                e["row"] = FRONT\n'
    '                e["preferred_row"] = FRONT\n\n'
    '        # Vary enemy counts ±1-2 for flavour (not for boss encounters)\n'
    '        import random as _rnd\n'
    '        if not any("boss" in e.get("template_key","").lower() or\n'
    '                   "king" in e.get("template_key","").lower() or\n'
    '                   "queen" in e.get("template_key","").lower()\n'
    '                   for e in self.enemies):\n'
    '            tweak = _rnd.randint(-1, 2)\n'
    '            if tweak > 0:\n'
    '                candidates = [e for e in self.enemies]\n'
    '                for _ in range(tweak):\n'
    '                    if candidates:\n'
    '                        from data.enemies import create_enemy_instance\n'
    '                        base = _rnd.choice(candidates)\n'
    '                        uid = max(e["uid"] for e in self.enemies) + 1\n'
    '                        extra = create_enemy_instance(base["template_key"], uid)\n'
    '                        extra["row"] = base["row"]\n'
    '                        extra["preferred_row"] = base["preferred_row"]\n'
    '                        self.enemies.append(extra)\n'
    '            elif tweak == -1 and len(self.enemies) > 1:\n'
    '                self.enemies.pop(_rnd.randrange(len(self.enemies)))\n\n'
    '        # Scale enemy power to party average level\n'
    '        if party_chars:\n'
    '            avg_level = sum(getattr(c, "level", 1) for c in party_chars) / len(party_chars)\n'
    '            scale = max(1.0, avg_level * 0.65)\n'
    '            for e in self.enemies:\n'
    '                if "boss" not in e.get("template_key", "").lower():\n'
    '                    e["hp"]      = max(1, int(e["hp"]     * scale))\n'
    '                    e["max_hp"]  = max(1, int(e["max_hp"] * scale))\n'
    '                    ad = e["attack_damage"]\n'
    '                    if isinstance(ad, (list, tuple)):\n'
    '                        e["attack_damage"] = (int(ad[0] * scale), int(ad[1] * scale))\n'
    '                    else:\n'
    '                        e["attack_damage"] = (int(ad * scale), int(ad * scale))\n\n'
    '        # Initial turn order',
    "Enemy scaling + row fix + count variation (combat_engine.py)"
)

# ── 15. dungeon.py: bigger goblin_warren map ──
patch("data/dungeon.py",
    '    "goblin_warren": {\n        "name": "Goblin Warren",\n        "floors": 3,\n        "width": 30, "height": 25,',
    '    "goblin_warren": {\n        "name": "Goblin Warren",\n        "floors": 3,\n        "width": 50, "height": 40,',
    "Bigger goblin_warren map (dungeon.py)"
)

# ── 16. dungeon.py: more rooms ──
patch("data/dungeon.py",
    '    max_rooms = 6 + floor_num * 2\n    min_room = 4\n    max_room = 8',
    '    max_rooms = 10 + floor_num * 2\n    min_room = 5\n    max_room = 10',
    "More dungeon rooms (dungeon.py)"
)

# ── 17. dungeon.py: more traps ──
patch("data/dungeon.py",
    '        # ── Place traps (deeper floors = more traps) ──\n'
    '        trap_count = floor_num\n'
    '        placed_traps = 0\n'
    '        for y in range(height):\n'
    '            for x in range(width):\n'
    '                if placed_traps >= trap_count:\n'
    '                    break\n'
    '                if tiles[y][x]["type"] == DT_CORRIDOR and rng.random() < 0.03:\n'
    '                    tiles[y][x]["type"] = DT_TRAP\n'
    '                    trap_tier = min(5, max(1, floor_num + _dungeon_trap_offset(dungeon_id)))\n'
    '                    tiles[y][x]["event"] = _make_tiered_trap(trap_tier, rng)\n'
    '                    placed_traps += 1',
    '        # ── Place traps (floor 1: 3 traps, scales up) ──\n'
    '        trap_count = 2 + floor_num * 2\n'
    '        placed_traps = 0\n'
    '        trap_tiles = []\n'
    '        for y in range(height):\n'
    '            for x in range(width):\n'
    '                if tiles[y][x]["type"] in (DT_CORRIDOR, DT_FLOOR):\n'
    '                    trap_tiles.append((x, y))\n'
    '        rng.shuffle(trap_tiles)\n'
    '        for tx2, ty2 in trap_tiles:\n'
    '            if placed_traps >= trap_count:\n'
    '                break\n'
    '            if tiles[ty2][tx2]["type"] in (DT_CORRIDOR, DT_FLOOR):\n'
    '                tiles[ty2][tx2]["type"] = DT_TRAP\n'
    '                trap_tier = min(5, max(1, floor_num + _dungeon_trap_offset(dungeon_id)))\n'
    '                tiles[ty2][tx2]["event"] = _make_tiered_trap(trap_tier, rng)\n'
    '                placed_traps += 1',
    "More traps (dungeon.py)"
)

# ── 18. dungeon_ui.py: visible wood-colour doors ──
patch("ui/dungeon_ui.py",
    '    if is_door:\n'
    '        surf.fill(tuple(int(v * 0.85) for v in wall_light))\n'
    '        for py in range(0, TEX_H, 12):\n'
    '            pygame.draw.line(surf, tuple(int(v*0.55) for v in wall_light), (0,py),(TEX_W,py))\n'
    '        for px in range(0, TEX_W, 8):\n'
    '            c = tuple(int(v*(0.7+rng.random()*0.25)) for v in wall_light)\n'
    '            pygame.draw.line(surf, c, (px,0),(px,TEX_H))\n'
    '        return surf',
    '    if is_door:\n'
    '        WOOD_BASE  = (120, 75, 35)\n'
    '        WOOD_DARK  = (80,  50, 20)\n'
    '        WOOD_LIGHT = (160, 105, 55)\n'
    '        surf.fill(WOOD_BASE)\n'
    '        for px in range(0, TEX_W, 6):\n'
    '            tone = rng.uniform(0.85, 1.15)\n'
    '            c = tuple(min(255, int(v * tone)) for v in WOOD_BASE)\n'
    '            pygame.draw.line(surf, c, (px, 0), (px, TEX_H))\n'
    '        for py in [TEX_H//6, TEX_H//2, TEX_H*5//6]:\n'
    '            pygame.draw.rect(surf, WOOD_DARK, (0, py-2, TEX_W, 4))\n'
    '            pygame.draw.rect(surf, WOOD_LIGHT, (0, py-3, TEX_W, 1))\n'
    '        pygame.draw.circle(surf, (200, 160, 40), (TEX_W*3//4, TEX_H//2), 4)\n'
    '        pygame.draw.circle(surf, (240, 200, 80), (TEX_W*3//4, TEX_H//2), 3)\n'
    '        return surf',
    "Wood door texture (dungeon_ui.py)"
)

# ── 19. town_ui.py: always open hub, safe walk defaults ──
patch("ui/town_ui.py",
    '        # ── Walkable town state ──\n'
    '        from data.town_maps import get_town_data\n'
    '        self.town_data = get_town_data(town_id)\n'
    '        if self.town_data:\n'
    '            self.view = self.VIEW_WALK\n'
    '            self.walk_x, self.walk_y = self.town_data["spawn"]\n'
    '            self.walk_facing = "down"\n'
    '            self.walk_interact_msg = ""   # message shown at bottom\n'
    '            self.walk_interact_timer = 0\n'
    '            # Dynamic tile size: bigger map = smaller tiles so it fits\n'
    '            tw = self.town_data["width"]\n'
    '            if tw >= 40:\n'
    '                self.walk_tile_size = 20\n'
    '            elif tw >= 30:\n'
    '                self.walk_tile_size = 24\n'
    '            else:\n'
    '                self.walk_tile_size = 28\n'
    '            self.walk_anim_t = 0\n'
    '        else:\n'
    '            self._return_to_town()',
    '        # Always use hub menu — walkable town removed\n'
    '        self.town_data = None\n'
    '        self.walk_x = 0\n'
    '        self.walk_y = 0\n'
    '        self.walk_facing = "down"\n'
    '        self.walk_anim_t = 0\n'
    '        self.walk_interact_msg = ""\n'
    '        self.walk_interact_timer = 0\n'
    '        self.walk_tile_size = 24\n'
    '        self._return_to_town()',
    "Town always hub + safe walk defaults (town_ui.py)"
)

print("=" * 50)
print("RESULTS:")
for msg in fixes_applied:
    print(f"  {'✓' if 'FIXED' in msg or 'already' in msg else '?'}  {msg}")
for msg in fixes_failed:
    print(f"  ✗  {msg}")
print()
print(f"{len(fixes_applied)} patches applied/confirmed, {len(fixes_failed)} failed")
if not fixes_failed:
    print("\nAll fixes applied! Run: python3 main.py")
else:
    print("\nSome patches failed — check output above.")
