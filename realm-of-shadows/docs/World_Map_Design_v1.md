# REALM OF SHADOWS — World Map Design v1

## OVERVIEW

A 120×120 tile overworld map with pseudo-3D angled perspective (Dragon Warrior style).
The party is represented as a single token moving tile-by-tile.
Exploration, discovery, random encounters, and camping are core mechanics.

---

## 1. MAP STRUCTURE

### Grid
- 120×120 tiles
- Each tile has: terrain_type, elevation (0-3), discovered (bool), 
  location_id (if town/dungeon/POI), encounter_zone (str)

### Terrain Types
```
GRASS       — open plains, easy travel, low encounter rate
FOREST      — wooded areas, normal travel, medium encounters
DENSE_FOREST— thick woods, slow travel, higher encounters, may hide secrets
MOUNTAIN    — impassable peaks (must go around)
HILL        — elevated terrain, slightly slow, medium encounters
SWAMP       — wet lowlands, slow travel, high encounters, poison risk
DESERT      — arid wasteland, slow travel, medium encounters, heat risk
WATER       — ocean/lakes, impassable (future: boat)
RIVER       — shallow water, slow crossing, low encounters
ROAD        — paved paths between towns, fast travel, low encounters
BRIDGE      — crosses rivers, normal speed
SHORE       — beach/coast, normal speed, occasional encounters
```

### Movement Speed (steps per move action)
```
Road:          1 tile, no fatigue
Grass/Shore:   1 tile, minimal fatigue
Hill/Forest:   1 tile, light fatigue  
Dense Forest:  1 tile, moderate fatigue
Swamp/Desert:  1 tile, heavy fatigue (HP drain over time)
Mountain:      IMPASSABLE
Water:         IMPASSABLE
```

### Elevation
- 0: sea level (water, shore, swamp)
- 1: lowlands (grass, forest, road)
- 2: highlands (hill, dense forest)
- 3: peaks (mountain — impassable)

---

## 2. VISUAL STYLE (Pseudo-3D Angled)

### Rendering
- Camera follows party, showing ~20×14 visible tiles
- Tiles rendered with slight vertical offset based on elevation
- Higher tiles overlap lower tiles (painter's algorithm, back-to-front)
- Each terrain type has a distinct color palette + simple icon/pattern
- Party token centered on screen

### Tile Appearance (colored rectangles with texture patterns)
```
Grass:        Green shades with small dot patterns
Forest:       Dark green with triangle tree shapes
Dense Forest: Darker green, more trees, shadowed
Mountain:     Grey/brown with peaked triangle tops
Hill:         Light brown/green, gentle slopes
Swamp:        Dark green-brown with wavy lines
Desert:       Tan/yellow with dot patterns
Water:        Blue with wave patterns
River:        Light blue, narrower
Road:         Brown/tan straight lines
Shore:        Tan meeting blue
Bridge:       Brown planks over blue
```

### Fog of War
- Unexplored tiles: solid dark (near-black)
- Explored but not visible: dimmed/desaturated
- Currently visible (within sight range): full color
- Sight range: 4 tiles (reduced in forest: 3, dense forest: 2)

---

## 3. REGIONS

The continent is divided into themed regions:

### Briarhollow Region (Starting Area — center-south)
- Terrain: Grass, light forest, roads
- Town: Briarhollow (starting town)
- Encounters: Goblins, wolves, bandits (easy)
- Dungeon: Goblin Warren (easy, 3 floors)

### The Thornwood (West)
- Terrain: Dense forest, hills
- Town: Woodhaven
- Encounters: Wolves, spiders, forest spirits (medium)
- Dungeon: Spider's Nest (medium, 4 floors)
- Hidden: Druid's Grove (secret location)

### Iron Ridge (North)
- Terrain: Mountains, hills, mines
- Town: Ironhearth
- Encounters: Orcs, trolls, rock elementals (hard)
- Dungeon: Abandoned Mine (hard, 5 floors)
- Hidden: Dragon's Rest (legendary cave)

### The Ashlands (East)
- Terrain: Desert, scorched earth
- Encounters: Skeletons, fire elementals (hard)
- Dungeon: Ruins of Ashenmoor (hard, 4 floors)
- Hidden: Buried Temple (secret)

### Mirehollow Swamp (Southeast)
- Terrain: Swamp, rivers
- Encounters: Lizardfolk, undead, swamp creatures (medium-hard)
- Dungeon: Sunken Crypt (medium, 4 floors)

### The Pale Coast (South edge)
- Terrain: Shore, grass, cliffs
- Encounters: Pirates, sea creatures (medium)
- Hidden: Smuggler's Cove

---

## 4. ENCOUNTER SYSTEM

### Random Encounters
- Each tile has an encounter_zone that maps to an encounter table
- Step counter: every N steps, roll for encounter
- Base rates by terrain:
```
Road:          1 in 25 steps
Grass:         1 in 15 steps
Forest/Hill:   1 in 12 steps
Dense Forest:  1 in 8 steps
Swamp/Desert:  1 in 6 steps
Shore:         1 in 18 steps
```

### Encounter Tables per Region
Each region has easy/medium/hard tiers with weighted random selection.
Deeper into dangerous terrain = harder encounters.

---

## 5. CAMPING SYSTEM

### Setting Up Camp
- Player can camp on any non-water, non-mountain tile
- Camping takes "time" (abstract — advances step counter)
- Effects:
  - HP: Restore 25% of max HP per rest cycle
  - MP/SP: Restore 15% of max per rest cycle  
  - Can rest multiple cycles (each cycle = ambush check)

### Ambush Risk
- Base ambush chance per rest cycle depends on terrain:
```
Road:          5%
Grass:         10%
Forest:        15%
Dense Forest:  25%
Swamp:         30%
Desert:        15%
Hill:          12%
```
- Modifiers:
  - Ranger in party: -5% (awareness)
  - Cleric Consecrate (future): -10%
  - Night camping (future): +10%

### Ambush Encounters
- If ambush triggered: combat starts with enemies getting a surprise round
- Party starts with randomized (possibly bad) positioning
- Can't flee on first round

---

## 6. DISCOVERABLE LOCATIONS

### Discovery Mechanic
- Hidden locations have a discovery_radius (usually 1-2 tiles)
- When party steps within radius, roll discovery check:
  - Base: 15% per adjacent step
  - Thief in party: +10%
  - Ranger in party: +10% (in forest/wilderness)
  - Mage in party: +5% (magical detection)
- Discovered locations appear on map permanently

### Location Types
- Towns: Always visible, marked on map
- Dungeons: Some visible, some hidden
- Points of Interest: Hidden shrines, treasure caches, NPC hermits
- Secret Areas: Very low discovery chance, high reward

---

## 7. IMPLEMENTATION PHASES

### Phase 1: Core Map (THIS BUILD)
- Map data structure and generation
- Tile rendering with pseudo-3D
- Party movement (arrow keys / WASD)
- Fog of war
- Basic terrain types
- Transition to town (step on town tile)
- Transition to combat (random encounters)
- Camp action (basic heal)

### Phase 2: Content
- Full region terrain painting
- All encounter tables populated
- Dungeon entrances on map
- Multiple towns

### Phase 3: Dungeons
- Dungeon map system (separate grids per floor)
- Floor transitions (stairs)
- Fixed encounters + random encounters
- Treasure rooms
- Boss floors

### Phase 4: Polish
- Terrain animations (water shimmer, tree sway)
- Day/night cycle
- Weather effects
- Mini-map
- Fast travel between discovered towns
