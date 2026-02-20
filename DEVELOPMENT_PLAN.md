# Realm of Shadows — Master Development Plan

## Current State (M5 Complete)
- 6-character party creation with life paths and backstories
- 120×120 procedural overworld with 5 towns, 5 dungeons, ports, secrets
- Wizardry-style grid dungeon crawling (3D placeholder renderer)
- Row-based combat with individual enemy targeting, abilities, status effects
- Equipment, identification, party knowledge, save/load
- Town services: shop (with buyback), temple, inn (rest + level up), tavern
- Economy balanced for first dungeon arc

## What's Missing
The game has systems but no soul. No story pulls the player forward. No NPCs have
names or agendas. Dungeons exist as disconnected combat zones. The title "Realm of
Shadows" means nothing yet.

---

## THE STORY: THE FADING

### Premise
The world of Aldenmere is dying. Not from war or plague, but from **the Fading** — a
creeping magical entropy where reality itself dissolves at the edges. Villages
disappear overnight. People forget their own names. The sun dims a little more each
season. Ancient wards that once held the darkness back are failing, one by one.

Your party are **Wardens** — an ancient order thought extinct, whose bloodlines carry
the ability to resist the Fading. You were recruited (or conscripted) in Briarhollow
after a Fading event consumed a nearby hamlet. A mysterious figure named **Maren** — a
scholar of the old wards — believes the Fading can be reversed, but only by restoring
the five **Hearthstones**: ancient artifacts hidden in the deepest dungeons of
Aldenmere, each guarded by a corrupted Warden who succumbed to the Shadow.

### Three-Act Structure

**Act I: The Awakening (Levels 1-5)**
- The party learns about the Fading from Maren in Briarhollow
- First quest: clear the Goblin Warren (goblins are refugees displaced by the Fading)
- Discovery: Grak the Goblin King has a fragment of a Hearthstone — he didn't steal
  it, he was *protecting* it. Moral ambiguity begins.
- Spider's Nest reveals that the spiders are mutated by Fading energy
- First Hearthstone recovered from the Abandoned Mine, guarded by a dwarven Warden
  ghost who tests the party before yielding it
- Act I climax: Briarhollow is attacked by Shadow creatures. The party must defend
  the town. Maren reveals more about the old order.

**Act II: The Corruption (Levels 5-10)**
- Travel to Ironhearth, Eastport, and beyond
- Ruins of Ashenmoor: discover that the Wardens didn't just *fail* — one of them
  deliberately broke the wards. A traitor Warden named **Valdris** sought to harness
  the Shadow as a power source.
- Sunken Crypt: recover the second Hearthstone from an undead Warden who begs for
  death. The crypt contains journals revealing Valdris was Maren's former mentor.
- Dragon's Tooth: A dragon corrupted by Shadow energy guards the third stone. Can be
  fought or negotiated with if the party found the dragon's true name in lore.
- Maren's behavior becomes suspicious — she's been marking locations, performing
  rituals. Is she helping or pursuing her own agenda?
- Act II climax: Maren betrays the party (or appears to). She takes two Hearthstones
  and vanishes. The party must decide: pursue her or continue seeking the remaining
  stones.

**Act III: The Shadow Throne (Levels 10-15)**
- The Fading accelerates. Towns begin disappearing from the world map.
- Party discovers Valdris is still alive — sustained by Shadow energy in a fortress
  beyond the mountains
- The Pale Coast and Windswept Isle hold the fourth stone, guarded by sea creatures
  and a Warden who chose isolation over corruption
- Maren's true plan revealed: she's Valdris's daughter, trying to save her father by
  completing his ritual *correctly* — not to harness Shadow, but to seal it forever.
  But her method requires sacrificing the Wardens (your party).
- Final dungeon: The Shadow Throne — a massive dungeon beneath the mountains where
  Valdris waits. Multiple endings based on player choices:
  1. **Destroy Valdris, save the world** — classic heroic ending
  2. **Help Maren's ritual** — world saved but party sacrificed (bittersweet)
  3. **Convince Maren to find another way** — requires finding all 5 stones +
     hidden lore. True ending: Valdris redeemed, Fading sealed, party survives.
  4. **Embrace the Shadow** — dark ending, party becomes new Shadow Wardens

### Lore Delivery Methods
- **Dungeon journals/scrolls**: Found on bodies, shelves, walls. Short, atmospheric.
- **Boss dialogue**: Pre-fight conversations that reveal story. Some bosses can be
  reasoned with.
- **Town NPCs**: Named characters with quests and evolving dialogue based on story
  progress.
- **Tavern rumors**: Tied to story progression — rumors change as the Fading spreads.
- **Environmental storytelling**: Faded zones in dungeons (distorted tiles, missing
  walls), abandoned towns on the world map that weren't there before.
- **Party knowledge journal**: Collected lore readable from the menu.

---

## MILESTONE PLAN

### M6: Story Foundation + NPC System
**Goal: Make the world feel alive and give the player a reason to explore.**

- [ ] Story flag system (tracks quest progress, choices, lore discovered)
- [ ] NPC dialogue system with branching based on flags
- [ ] Named NPCs for each town:
  - Briarhollow: Maren (quest giver), Captain Aldric (guard captain, different from
    party Aldric), Innkeeper Bess
  - Woodhaven: Elder Theron (druid), Sylla (herbalist)
  - Ironhearth: Forgemaster Dunn, Merchant Kira
- [ ] Quest log UI (accessible from menu)
- [ ] Tavern rumors tied to story progression
- [ ] Dungeon story events (journals, inscriptions, NPC encounters mid-dungeon)
- [ ] Opening narrative sequence (new game intro)
- [ ] Goblin Warren story integration: Grak dialogue before boss fight

**Estimated scope: 4-5 sessions**

### M7: 3D Dungeon Renderer
**Goal: Transform dungeon exploration from functional to atmospheric.**

- [ ] Textured walls (stone, brick, cave, crypt variants per dungeon theme)
- [ ] Floor and ceiling rendering
- [ ] Proper lighting (torch glow, darkness ahead, ambient)
- [ ] Visible doors (closed/open states)
- [ ] Visible stairs (up/down)
- [ ] Visible chests and interactable objects
- [ ] Visible enemies ahead in corridors (sprites)
- [ ] Fading visual effects (distorted textures, color desaturation for corrupted
  zones)
- [ ] Smooth movement animation between tiles
- [ ] Minimap overlay

**Estimated scope: 3-4 sessions**

### M8: Advanced Equipment + Crafting
**Goal: Make loot exciting and give materials a purpose.**

- [ ] Cursed items (can't unequip without Remove Curse)
- [ ] Elemental properties on weapons/armor (fire, ice, lightning, shadow)
- [ ] Enemy elemental resistances/weaknesses
- [ ] Crafting system:
  - Combine materials at a crafting station (new town building)
  - Recipes discovered via lore scrolls or experimentation
  - Material drops from enemies (wolf pelts, goblin teeth, shadow essence)
- [ ] Enchanting: add elemental effects to existing gear
- [ ] Item weight/encumbrance system
- [ ] Rare/unique named weapons with lore descriptions
- [ ] Hearthstone fragments as key items (story integration)

**Estimated scope: 3-4 sessions**

### M9: Class Progression + Ability Trees
**Goal: Make character builds feel distinct and meaningful.**

- [ ] Ability trees per class (2 branches each):
  - Fighter: Guardian (tank/protect) vs Berserker (damage/rage)
  - Mage: Elementalist (damage spells) vs Enchanter (buffs/debuffs)
  - Cleric: Healer (restoration) vs Smiter (holy damage)
  - Thief: Assassin (crit/poison) vs Shadow (stealth/evasion)
  - Ranger: Marksman (ranged mastery) vs Beastmaster (summon/companion)
  - Monk: Way of Iron (melee power) vs Way of Wind (speed/evasion)
- [ ] Branch choice at level 5 (Guild training in towns)
- [ ] Advanced class transitions at level 10:
  - Fighter + Cleric training → Paladin
  - Thief + Mage training → Spellblade
  - Ranger + Monk training → Warden (story connection)
  - etc.
- [ ] Guild buildings in towns (new location type)
- [ ] Class-specific quest requirements for advancement

**Estimated scope: 3-4 sessions**

### M10: World Expansion + Dynamic Events
**Goal: Make the overworld feel like a living, changing place.**

- [ ] 3-4 additional towns with unique services and NPCs
- [ ] 3-4 additional dungeons (story-critical and optional)
- [ ] Sea travel between ports (ship encounters, island exploration)
- [ ] Dynamic Fading events: locations change/disappear based on story progress
- [ ] World map encounters: caravans, refugees, bandits, Fading creatures
- [ ] Camp system improvements: cooking, crafting at camp
- [ ] Day/night cycle affecting encounters and town services
- [ ] Weather system (affects visibility, combat modifiers)

**Estimated scope: 4-5 sessions**

### M11: Boss Encounters + Dialogue Combat
**Goal: Make boss fights memorable story moments.**

- [ ] Pre-boss dialogue sequences with player choices
- [ ] Boss-specific mechanics (phases, special attacks, terrain effects)
- [ ] Boss AI patterns (not just "hit hardest target")
- [ ] Post-boss story reveals (cutscene-like text sequences)
- [ ] Optional boss negotiations (spare/recruit/bargain)
- [ ] Corrupted Warden bosses with unique abilities per Act
- [ ] Final boss: Valdris with multiple phases tied to Hearthstones

**Estimated scope: 3-4 sessions**

### M12: Audio + Visual Polish
**Goal: Atmosphere and immersion.**

- [ ] Procedural ambient music (dungeon, town, overworld, combat themes)
- [ ] Sound effects (footsteps, combat, UI, environment)
- [ ] Particle effects (torches, magic, Fading particles)
- [ ] Screen transitions (fade in/out between locations)
- [ ] Title screen with new game / continue / settings
- [ ] Credits / ending sequences
- [ ] Character portraits (generated or template-based)

**Estimated scope: 3-4 sessions**

### M13: Endgame + Multiple Endings
**Goal: Deliver on the story's promise.**

- [ ] Act III dungeons and story content
- [ ] The Shadow Throne (final dungeon, 10+ floors)
- [ ] Four ending paths based on accumulated choices
- [ ] New Game+ mode (carry over levels, face harder enemies)
- [ ] Achievement/completion tracking
- [ ] Final balance pass (all dungeons, all encounters, economy)

**Estimated scope: 4-5 sessions**

---

## PRIORITY ORDER

The milestones above are roughly in dependency order, but some can be parallelized.
Recommended execution:

1. **M6 (Story)** — Everything else builds on this foundation
2. **M7 (3D Renderer)** — Biggest visual impact, needed for environmental storytelling
3. **M8 (Equipment)** — Cursed items + crafting + elements make loot exciting
4. **M9 (Classes)** — Ability trees give long-term character investment
5. **M10 (World)** — Content expansion, dynamic events
6. **M11 (Bosses)** — Story climax moments
7. **M12 (Polish)** — Audio/visual atmosphere
8. **M13 (Endgame)** — Final content and endings

**Total estimated scope: 27-35 sessions**

---

## TECHNICAL NOTES

Current codebase: ~14,800 lines across 27 Python files.
Key architectural decisions:
- Story flags stored in save file alongside party + knowledge
- NPC dialogue as data-driven JSON/dict trees (not hardcoded)
- 3D renderer as standalone module replacing current dungeon_ui renderer
- Crafting recipes as data files (easy to expand)
- Ability trees as class data extensions (not engine changes)
- Dynamic world events as triggers checked on world map movement
