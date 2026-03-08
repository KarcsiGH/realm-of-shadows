# Realm of Shadows

**Advanced Class System Party-Based RPG**

A retro-style, turn-based RPG built with Python and Pygame featuring deep character customization, a branching life-path character generation system, and 27 total classes.

## Current Build: Milestone 1 — Character Creation

### Features
- **Life Path System** — Shape your character through 9 branching life events across childhood, youth, and early adulthood. Your choices determine your stats and generate a unique backstory.
- **4 Life Streams** — Rural/Wilderness, Urban/Criminal, Military, and Noble — with crossover points where characters can shift between paths.
- **Random Outcomes** — Some events have success/fail rolls that change your story and stats.
- **6 Base Classes** — Fighter, Mage, Cleric, Thief, Ranger, Monk — each with unique stat priorities, resource pools, Ki formulas, and starting abilities.
- **Class Recommendations** — After your life path, the game suggests which classes fit your stats best.
- **Quick Roll Option** — Skip the life path and jump straight into class selection.
- **Party of 6** — Build a full adventuring party before setting out.

### How to Run

**Requirements:** Python 3, Pygame

```bash
pip install pygame
cd realm-of-shadows
python3 main.py
```

### Game Systems (Designed, Implementation in Progress)

- 6 base stats: STR, DEX, CON, INT, WIS, PIE
- 7 resource pools: HP, Ki, INT-MP, WIS-MP, PIE-MP, STR-SP, DEX-SP
- 27 total classes (6 basic + 6 advanced + 15 hybrid)
- Hybrid Ki formulas with stat overlap bonuses
- Equipment slot scaling (6→20 by level)
- Potion diminishing returns system
- Stat training with location-based limits
- Cumulative ability learning across class changes
- 6+ specialized towns with unique class halls

### Roadmap

- [x] Milestone 1: Character creation and life path
- [ ] Milestone 2: Basic combat system
- [ ] Milestone 3: Abilities, spells, and Ki usage
- [ ] Milestone 4: Town hub — shops, guilds, stat training
- [ ] Milestone 5: World map and exploration
- [ ] Milestone 6: Advanced and hybrid classes
- [ ] Milestone 7: Save/load system
- [ ] Milestone 8: Polish, balancing, and content

### Project Structure

```
realm-of-shadows/
├── main.py                  # Game entry point
├── core/
│   ├── classes.py           # Class definitions, stats, resource formulas
│   └── character.py         # Character model and life path tracking
├── data/
│   └── life_path_events.py  # Branching event tree (100 events)
├── ui/
│   └── renderer.py          # Retro UI rendering helpers
└── docs/
    ├── REALM_OF_SHADOWS_Design.docx    # Complete game design document
    └── Life_Path_Design_v1.md          # Life path system design
```

### Design Documents

See the `docs/` folder for the complete game design document covering all classes, formulas, world structure, and systems.
