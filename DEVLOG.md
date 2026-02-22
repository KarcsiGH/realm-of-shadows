# Realm of Shadows — DEVLOG

## Current State
**Session 1A complete — Race System (M11)**

## Sprint Plan
- **Sprint 1:** M11 (Races) + M12 (Walkable Towns) + Briarhollow prototype
- **Sprint 2:** M13 (Quest System) + M14 (Training Locations)
- **Sprint 3:** M15 (All Settlements) + M16 (Side Quests) + M17 (Dungeons)
- **Sprint 4:** M18 (Act 2) + M19 (Polish) + M20 (Steam Prep)

## Completed
### M11 — Race System ✅
- 7 races: Human, Elf, Dwarf, Halfling, Half-Orc, Gnome, Fading-Touched
- Race selection screen in character creation (between name and lifepath/class)
- Human gets +1 to any stat (player picks)
- Racial stat mods applied at character creation
- Combat passives:
  - Human: +5% XP
  - Elf: +15% secret door detection, 15% shadow resist
  - Dwarf: +12% trap detection, 30% poison resist
  - Halfling: +5% crit, +8% dodge
  - Half-Orc: +8% physical damage
  - Gnome: -1 MP cost on spells, 15% arcane resist
  - Fading-Touched: 35% shadow resist, +10% shadow damage, 15% divine vulnerability
- Save/load preserves race
- Party review and summary screens show race
- Files: core/races.py (new), core/character.py, core/combat_engine.py, core/save_load.py, data/dungeon.py, main.py

### Previous Milestones (M1-M10 + Tower)
- 20K+ lines of code
- 69 enemies, 93 encounters, 6 dungeons
- Full combat, equipment, crafting, enchanting
- Procedural dungeons with secret rooms
- World map, 3 towns (menu-driven), story system
- Sound engine

## Next Up: Session 1B — Walkable Town Engine
- Tile-based town renderer (reuse dungeon tile system)
- Town map format: hand-crafted tile grids
- Building interiors as separate "rooms"
- NPC placement and interaction
- Door/entrance tiles connecting buildings to town
- Briarhollow as first walkable town

## Design Decisions
- 8 settlements: 3 villages, 3 towns, 2 cities
- Ultima-style walkable towns replace menu system
- Level cap: 15 for Game 1
- Multi-game structure with character import
- Planar ascension ranking: Bronze → Iron → Steel → etc.
- Game 1 ends with Valdris betrayal
- Target: 12-18 hours, $9.99-$14.99 on Steam

## File Counts
- core/: character.py, classes.py, combat_engine.py, crafting.py, equipment.py, progression.py, races.py, save_load.py, sound.py, etc.
- data/: bestiary_m9.py, dungeon.py, enemies.py, life_path_events.py, magic_items.py, story_data.py, tower_data.py, weapons.py, world_map.py
- ui/: combat_ui.py, dungeon_ui.py, inventory_ui.py, post_combat_ui.py, town_ui.py, world_map_ui.py
