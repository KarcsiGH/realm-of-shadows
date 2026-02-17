# REALM OF SHADOWS — World Systems Design v2

## Overview of Changes
This document covers three interconnected systems being added to Milestone 3:
1. Realistic terrain generation with biome transitions
2. Travel methods (horses, boats, magical rail, teleport network)
3. Hybrid region/dungeon gating (open world + narrative keys)

---

## 1. TERRAIN GENERATION REWORK

### Core Principle
Terrain should follow geographic logic:
- Mountains create rain shadows → forest on one side, desert on the other
- Rivers flow FROM mountains TO coast, collecting into lakes
- Biomes transition gradually (no desert next to dense forest)
- Coastlines are natural, with bays, peninsulas, and islands

### Biome Transition Rules
```
Adjacent biomes must be "compatible". Allowed transitions:

DESERT     ↔ SCRUBLAND ↔ GRASS ↔ FOREST ↔ DENSE_FOREST
DESERT     ↔ HILL (arid hills)
GRASS      ↔ HILL ↔ MOUNTAIN
FOREST     ↔ HILL
SWAMP      ↔ GRASS, FOREST, SHORE (lowland only)
SHORE      ↔ GRASS, FOREST, SWAMP, WATER
WATER      ↔ SHORE only (no land directly touching deep water)
RIVER      ↔ any land type (rivers cut through terrain)
ROAD       ↔ any passable land type

FORBIDDEN adjacencies (hard rule):
- DESERT next to FOREST or DENSE_FOREST
- MOUNTAIN next to SWAMP or WATER  
- DESERT next to SWAMP
```

### New Terrain: SCRUBLAND
Added as transition between desert and grassland:
- Dry, sparse vegetation
- Medium encounter rate
- Normal movement speed
- Visual: tan-green with small bush dots

### Generation Algorithm (Revised)
1. Generate heightmap using diamond-square or simplex noise
2. Place water at lowest elevations → creates ocean, lakes
3. Place mountains at highest elevations
4. Generate moisture map (distance from water + rain shadow from mountains)
5. Assign biomes based on (elevation × moisture):
   - High elevation + any moisture = Mountain/Hill
   - Low elevation + high moisture = Swamp
   - Mid elevation + high moisture = Forest/Dense Forest
   - Mid elevation + low moisture = Grass/Scrubland
   - Mid elevation + very low moisture = Desert
   - Elevation 0 near water = Shore
6. River generation: start from mountain peaks, flow downhill to water
7. Smooth passes to enforce transition rules
8. Place locations on appropriate terrain
9. Carve roads between towns

### Water Features
- OCEAN: deep water surrounding continent, impassable without boat
- LAKE: inland water body, 5-15 tiles, formed in low elevation
- RIVER: flows from mountains to ocean/lake, 1-2 tiles wide
- SHORE: always borders water, transition to land

### Islands
- 3-5 small islands (5-15 tiles each) off the coast
- Accessible only by boat
- Contain hidden locations, treasure, or secret dungeons
- One island has a major late-game dungeon

### Continent Geography (Revised Layout)
```
                    IRON RIDGE
                   (mountains, mines)
                  /               \
    THORNWOOD ──── BRIARHOLLOW ──── ASHLANDS
    (deep forest)  (starting area)   (desert, east
     west side)    (central plains)   of mountains)
         \              |              /
      PALE COAST ── MIREHOLLOW ── EASTERN SHORE
      (south-west)   (swamp,       (docks, islands)
                     south-central)

    ~~~~ OCEAN (south + east edges) ~~~~
    
    ISLANDS:
    - Windswept Isle (south, medium difficulty)
    - Dragon's Tooth (far east, high difficulty)  
    - Hermit's Rock (small, secret)
```

---

## 2. TRAVEL METHODS

### Walking (Default)
- 1 tile per step
- Terrain affects fatigue (swamp/desert drain minor HP over time)
- Available immediately

### Horse
- Purchase: 200g at any town stable
- Speed: 2 tiles per step on road/grass, 1 tile on rough terrain
- Cannot enter: dungeons, dense forest, swamp, mountains
- Must be left at dungeon entrance (stays there)
- Can be stolen if left in dangerous area (small chance)
- Party shares one horse (it's a pack horse + riding)

### Boat
- Purchase: 500g at port towns (Briarhollow docks area, Eastern Shore)
- Or rent: 50g per trip between ports
- Travel: coastal routes between port towns, river travel, to islands
- Types:
  - Rowboat (rent): slow, coastal only, 1 tile per step on water
  - Sailing ship (buy): faster, open ocean capable, 2 tiles per step
- Boat docks at port — you walk from there
- Random sea encounters (pirates, sea creatures) on longer voyages

### Magical Rail
- Fixed routes between major cities with Mage Guild presence
- Requires: Mage Guild membership (quest unlock, ~level 5-8)
- Cost: 25g per trip
- Instant travel between connected stations
- Stations: Briarhollow, Woodhaven, Ironhearth (3 initial)
- More stations unlock as you progress (Ashlands ruins, etc.)
- Lore: Ancient ley lines channeled by the Mage Academies

### Flying Carpet
- Rare item, found in late-game dungeon or purchased for 2000g
- Ignores all terrain, flies over mountains and water
- 3 tiles per step
- Random sky encounters (rare): griffins, air elementals
- Cannot be used in dungeons

### Teleport Network
- Each major town has a Teleport Circle at its Mage Academy
- Must physically visit and "attune" to each circle first
- Requires: complete a short quest per town to activate
- Cost: 50g + mage in party spends MP (or 100g without mage)
- Instant travel between any two attuned circles
- Lore: The circles are ancient, the academies maintain them

### Travel UI
- When moving on world map, current travel mode shown in HUD
- Button to toggle: Walk / Horse / Carpet (if owned)
- Port towns show "Dock" option → opens sea travel route map
- Mage rail stations show "Rail" option → pick destination
- Teleport circles show "Teleport" option → pick attuned destination

---

## 3. HYBRID GATING SYSTEM

### Open World (Soft Gates)
The overworld is fully explorable from the start. Difficulty scales
by region. Players can wander into dangerous areas and face the
consequences. Warnings are provided:

```
Region approach warnings (shown when entering region):
- "The air grows hot and dry. Your party feels the desert's bite."
- "Dark trees close in around you. Something watches from the shadows."
- "The ground trembles. Orcish war drums echo from the peaks."
```

Enemy difficulty by region (expected party level):
- Briarhollow:  Level 1-4  (easy)
- Pale Coast:   Level 2-5  (easy-medium)
- Thornwood:    Level 3-7  (medium)
- Mirehollow:   Level 4-8  (medium-hard)
- Iron Ridge:   Level 6-10 (hard)
- Ashlands:     Level 8-12 (hard)
- Islands:      Level 5-15 (varies)

### Narrative Gates (Hard Gates for Dungeons)
Specific dungeons and locations require keys/quest items:

```
Goblin Warren:     OPEN (starting dungeon, no key needed)
Spider's Nest:     Requires: "Thornwood Map" from Woodhaven guild
Abandoned Mine:    Requires: "Mine Key" from Ironhearth mayor quest
Ruins of Ashenmoor: Requires: "Ashenmoor Seal" from desert hermit
Sunken Crypt:      Requires: "Crypt Amulet" from Mirehollow priest
Dragon's Tooth:    Requires: boat + "Dragon Scale" from Iron Ridge boss

Hidden/Secret locations: discovered by exploration, no key needed
```

### Gate Items
- Quest items that persist in a special "Key Items" inventory
- Cannot be sold, dropped, or traded
- Obtained by completing specific quests in towns
- Each gate quest has a recommended level but isn't level-locked
  (a skilled level 3 party could do a level 6 quest if they're good)

---

## 4. IMPLEMENTATION ORDER

### Phase 1: Terrain Rework
- New heightmap-based generation
- Biome assignment from elevation + moisture
- River systems (mountain to coast)
- Lakes
- Islands
- Shore/coast improvements
- Biome transition smoothing
- New terrain type: Scrubland

### Phase 2: Travel Methods
- Horse (purchase at stable, speed boost)
- Boat (port towns, coastal routes, islands)
- Travel mode toggle in HUD
- Sea encounter tables

### Phase 3: Fast Travel
- Magical rail (fixed routes, quest unlock)
- Teleport network (attune circles, instant travel)
- Travel UI for selecting destinations

### Phase 4: Gating
- Key Items inventory
- Dungeon entry checks
- Region warning messages
- Gate quest stubs (actual quests in Milestone 5)

---

## 5. DATA STRUCTURES

### Key Items (new)
```python
party.key_items = [
    {"id": "thornwood_map", "name": "Thornwood Map", "desc": "..."},
    {"id": "mine_key", "name": "Mine Key", "desc": "..."},
]
```

### Travel State (new)
```python
world_state.travel = {
    "has_horse": False,
    "has_boat": False,       # owns a sailing ship
    "has_carpet": False,
    "travel_mode": "walk",   # walk, horse, carpet
    "boat_location": None,   # port where boat is docked
    "attuned_circles": [],   # list of town IDs
    "rail_unlocked": False,  # mage guild quest complete
}
```

### Port Routes (new)
```python
PORT_ROUTES = {
    "briarhollow_dock": ["pale_coast_dock", "windswept_isle"],
    "eastern_shore_dock": ["dragons_tooth", "hermits_rock"],
    "pale_coast_dock": ["briarhollow_dock", "windswept_isle"],
}
```
