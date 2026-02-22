# Realm of Shadows — DEVLOG

## Current State
**Session 1B complete — Walkable Town Engine (M12 partial)**

## Sprint Plan
- **Sprint 1:** M11 (Races) + M12 (Walkable Towns) + Briarhollow prototype
- **Sprint 2:** M13 (Quest System) + M14 (Training Locations)
- **Sprint 3:** M15 (All Settlements) + M16 (Side Quests) + M17 (Dungeons)
- **Sprint 4:** M18 (Act 2) + M19 (Polish) + M20 (Steam Prep)

## Completed
### Session 1B — Walkable Town Engine ✅
- Tile-based walkable town maps replace menu-driven hub
- data/town_maps.py: tile types (grass, wall, door, tree, water, path, exit, sign, fence)
- Briarhollow: 24x20 map with 6 buildings (Inn, Shop, Temple, Tavern, Forge, Elder's House)
- 3 NPCs placed on map (Maren, Captain Aldric, Elder Thom)
- Job Board sign placed (UI framework coming in Sprint 2)
- WASD/arrow movement, ENTER to interact, ESC to leave
- Context-sensitive prompts at bottom of screen
- All existing service UIs (shop, temple, inn, forge, tavern) work unchanged
- _return_to_town() routes back to walk or menu based on town type
- Fallback: towns without walkable maps still use old menu hub
- Files: data/town_maps.py (new), ui/town_ui.py (modified), main.py (modified)

### M11 — Race System ✅

## Next Up: Session 1C
- Build walkable maps for remaining 7 towns
- World map location updates for new settlements
- Unique buildings per settlement (Monastery, Fighter's Guild, Mage University, etc.)- 7 races: Human, Elf, Dwarf, Halfling, Half-Orc, Gnome, Fading-Touched
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
