# Realm of Shadows — Development Plan (Updated)

## Current State — Feature Complete (Pre-Launch Polish)

The game is content-complete and mechanically functional. 290/290 tests pass.
All core systems are implemented and wired together.

---

## Content Totals

| System | Count |
|---|---|
| Dungeons | 10 / 10 |
| Main quests | 14 (Act 1: 6, Act 2: 8) |
| Act 3 quests | 9 |
| Side quests | 9 |
| Job board contracts | 39 (across 8 towns) |
| NPC dialogues | 57 named NPCs |
| World locations | 23 |
| Walkable towns | 8 |
| Enemies | 196 encounter variants |
| Player abilities | 170 (base + hybrid + apex) |
| Achievements | 21 |

---

## Completed Systems

### Core Gameplay
- [x] 6-character party creation with life paths and backstories
- [x] Row-based turn combat — attack, ability, defend, flee, items, weapon swap
- [x] 3D raycasting dungeon renderer (numpy/surfarray, ~58 FPS)
- [x] World map with fog of war, sea travel, port unlocking
- [x] 8 fully walkable towns (shop, inn, temple, tavern, guild, forge)
- [x] Save/load with multiple slots and world state
- [x] Full screen settings, key rebinding, SFX/music volume

### Character Progression
- [x] 6 base classes (Fighter, Mage, Cleric, Thief, Ranger, Monk)
- [x] 15 hybrid classes (level 10 transition) — each with 6 unique abilities
- [x] 6 apex classes (level 15 transition) — each with 5 unique abilities
- [x] Branch ability choice at levels 3, 7, 10 per base class
- [x] Class transition UI (guild screen)
- [x] Branch choice UI (inn/guild screen)
- [x] Planar tier system (Bronze → Iron → Steel → Mithril → Adamantine)
- [x] Warden Order rank display (Initiate through Commander)

### Ability System
- [x] All 6 base classes: 6–10 abilities each, 3 branch levels each
- [x] All 15 hybrid classes: 6 abilities each (170 total across all classes)
- [x] All 6 apex classes: 5 abilities each
- [x] Turn Undead: applies Fear + 50% attack reduction to all undead
- [x] Mass Resurrection: revives all fallen allies at 50% HP simultaneously
- [x] Full AoE, heal, buff, debuff, cure, revive, taunt, special types

### Story & Quests
- [x] 3-act narrative: Maren, the Hearthstones, the Fading, Valdris
- [x] 23 quests total, all wired with start/complete dialogue triggers
- [x] 57 NPCs with conditional dialogue trees
- [x] 39 job board contracts across 8 towns
- [x] Branching dialogues (goblin peace, Maren fate, governor conspiracy)
- [x] Full ending sequence with multiple outcome text variations

### Equipment & Economy
- [x] Tiered equipment (T1–T4) with class restrictions and stats
- [x] Item identification system with party knowledge sharing
- [x] Cursed items and Remove Curse
- [x] Unique items and 2-piece set bonuses (Warden set, Ashenmoor set)
- [x] Durability system with repair
- [x] Enchanting scrolls (existing)

### Combat Engine
- [x] Physical/magic accuracy, crits, row/range modifiers
- [x] Status effects: Stunned, Poisoned, Burning, Slowed, Fear, Silenced, Cursed, Taunted, Blessed
- [x] Enemy AI (aggressive, defensive, support, balanced, flee behaviors)
- [x] Boss encounters with unique mechanics
- [x] Flee with opportunity attacks
- [x] Knowledge tier system (enemies reveal info across 3 tiers)

### UI
- [x] Combat UI: character cards, enemy rows, scrollable log, popover abilities, AoE routing
- [x] Camp UI: stats tab (tier badge, resistances, abilities, equipment), manual (8 pages, M/F1)
- [x] Quest log with bestiary tab
- [x] Post-combat UI: XP/gold awards, loot assignment, level-up fanfare
- [x] In-game manual (8 pages, accessible via M key / F1)

### Infrastructure
- [x] Story flags: get/set, quest state, condition evaluation
- [x] Achievement system: 21 achievements, toast notifications
- [x] Character export for New Game+ / cross-game import
- [x] 290/290 automated tests

---

## Remaining Work (Estimated Sessions)

### Must-Have Before Launch (2–3 sessions)

**Playtesting pass** (1–2 sessions)
- End-to-end playthrough: verify all 3 acts flow correctly
- Test class transitions at level 10/15 in real gameplay
- Verify all 9 Act 3 quests trigger and complete correctly
- Confirm ending screen export button works
- Balance check: enemy difficulty scaling, XP curve, gold economy

**Day/night cycle** (0.5 sessions) *(low complexity — mostly visual)*
- Tint world map and town overlays based on game_time flag
- Inn rest advances time (dawn → dusk or vice versa)
- Some NPCs only appear at certain times (flavour, not blocking)

### Post-Launch (Future sessions)

**Crafting and enchanting** (~2 sessions)
- Reagent drops from specific enemies
- Town forge UI for combining items
- Enchant weapons/armor with elemental effects

**New Game+ / Game 2 import** (1 session when Game 2 exists)
- `import_party()` already built in `core/save_load.py`
- Game 2 new-game screen needs "Import from Realm of Shadows" option
- Imported characters start at scaled-down level (e.g. ÷2 + 5)

**Controller support** (~2 sessions, post-launch if requested)
- D-pad navigation for all menus
- Button mapping (A=confirm, B=cancel, X=attack, Y=abilities)
- "Focused element" cursor system for combat targeting

**Weather system** (~1 session, post-launch)
- Rain/fog visual overlay on world map and dungeon
- Minor gameplay effect (reduced accuracy in storms)

---

## Architecture Notes

- Entry point: `main.py` — single Game class, state machine (S_* constants)
- State constants: S_CAMP=22, S_COMBAT=8, S_DUNGEON=13, S_WORLD_MAP=3, S_TOWN=4, S_ENDING=19
- Screen: 1440×900, party size 6, max level 30
- Save dir: `~/Documents/RealmOfShadows/saves/`
- Export file: `~/Documents/RealmOfShadows/party_export.json`
- Key APIs: `apply_level_up(char, free_stat)`, `apply_class_transition(char, class_name)`,
  `CombatState(party, enc_key)`, `save_game(party, world_state, slot_name)`,
  `export_party(party, filepath)`, `import_party(filepath)`
