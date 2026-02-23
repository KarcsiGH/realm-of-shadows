# REALM OF SHADOWS — GAME BIBLE
**Master Design Reference** | Last updated: 2026-02-23

This document captures the highest-level design decisions for the game. It exists
so that no critical design intent is ever lost between sessions. When in doubt,
this document is the authority.

---

## 1. POWER TIERS (Character Rank)

Characters have **two progression axes**: a numeric level (1–30) and a **Power Tier**.
The tier represents a fundamental classification of power that transcends levels.

### Tier Ladder
| Tier     | Description |
|----------|-------------|
| Bronze   | Starting tier. All player characters begin here. Common adventurers, militia, minor monsters. |
| Iron     | Elite tier. Master knights, senior mages, powerful monsters. The highest NPCs on the mortal plane in Game 1. |
| Steel    | Legendary tier. Generals, archmages, ancient creatures. Unreachable by players in Game 1. |
| Silver   | Mythic tier. Heroes of legend, demigods, elder beings. |
| Gold     | Divine tier. Minor gods, avatars, plane-walkers. |
| Platinum | Transcendent tier. Greater gods, cosmic entities. |
| Diamond  | Absolute tier. The foundations of reality itself. |

### Rules
- **Players in Game 1 are Bronze tier.** They never surpass Bronze in this game, no matter how high their numeric level.
- **The ceiling for mortal NPCs on this plane is Iron.** The most powerful human figures — the Emperor's Governor in the capital city, high priests, legendary guild masters — are Iron tier. Players cannot defeat them in direct combat at Bronze tier (they would need to be clever, use environment, have story advantages, etc.).
- **Tier affects more than stats.** Iron-tier NPCs may have abilities, resistances, or narrative immunity that Bronze characters simply can't overcome through raw combat.
- **Future games** will allow players to ascend tiers. Game 2 may begin at Iron, or allow Bronze→Iron ascension during play.

### Why This Matters for Design
- Keeps the world feeling vast — players know there are forces beyond them.
- Gives meaning to the Governor's presence in the capital: he's not a boss to defeat, he's a power to navigate around or work with.
- Sets up the stakes for plane ascension: reaching Iron tier may be a requirement for moving to the next plane.

---

## 2. ACTS & NARRATIVE STRUCTURE

### Game 1 Structure
The first game (this game) takes place entirely on **the Mortal Plane**.

**Act 1 — The Wilds** (Levels 1–10, early game)
- Setting: The frontier regions — Briarhollow, Woodhaven, and nearby wilderness.
- Tone: Discovery, survival, building a party reputation.
- Stakes: Local threats — goblin incursions, bandit lords, haunted ruins.
- Ends: Party establishes themselves as serious adventurers; a larger threat becomes visible.

**Act 2 — The Realm** (Levels 11–20, mid game)
- Setting: The wider continent, including Ironhearth and the capital city.
- Tone: Political intrigue, larger conspiracies, travel to distant lands.
- Stakes: Continental — something is destabilizing the plane itself.
- Key NPC: The Emperor's Governor in the capital. Iron tier. He is not a villain per se, but represents the established order the party must navigate.
- Ends: The threat is identified as coming from another plane. Ascension becomes possible/necessary.

**[Future] Plane Ascension** (Beyond Game 1)
- After Acts 1 & 2 on the Mortal Plane, the story opens to other planes.
- Characters must reach a threshold (possibly Iron tier, or have completed specific quests) to ascend.
- The nature of other planes and what awaits there is to be designed in future sessions.

---

## 3. WORLD — TOWNS (8 Total)

The game world has **8 towns**. As of now, 3 are implemented and 5 are placeholders.

### Implemented (3)
| Town | Region | Specialty | Notes |
|------|--------|-----------|-------|
| Briarhollow | Central plains | Starter town | Complete basics, beginner-friendly |
| Woodhaven | Western forest | Ranger/nature focus | Forest-edge settlement |
| Ironhearth | Northern mountains | Warrior/blacksmith focus | Industrial, mining region |

### Planned (5 — to be designed)
The original design specified 6 towns in early sessions (Millhaven, Ironforge, Crystalspire, Sanctum, Greenwood, Saltmere). The world was later judged too small and expanded to 8. The final 8 towns need to be confirmed and mapped. Candidates based on design history:

| Candidate | Type | Notes |
|-----------|------|-------|
| The Capital | Large city | Act 2 hub; contains the Governor's castle; largest city on the map; Iron-tier NPCs present |
| Saltmere / Port city | Coastal | Rogue/thief specialty, black market, sea travel hub |
| Crystalspire / Mage city | Interior | Magic academy, teleport network hub, INT-focused |
| Sanctum / Holy city | Southern | Divine specialty, grand cathedral, WIS-focused |
| Greenwood / Wilderness outpost | Southwest | Nature specialty, limited halls, DEX/WIS focus |

**�  ACTION NEEDED:** Confirm final names and positions of all 8 towns in a future session. This list is candidates, not confirmed.

---

## 4. THE CAPITAL CITY

The capital is the largest settlement on the map — visibly bigger than other towns on the world map.

- **The Governor's Castle** sits within the capital. The Emperor's Governor resides here.
- The Governor is **Iron tier** — the highest-power human NPC the players will encounter in Game 1.
- The capital has: the Mage Academy's main teleport hub, the primary Thieves' Guild chapter, the imperial marketplace (best shop inventory in the game), and the largest temple.
- Reaching the capital is an Act 2 milestone.
- The capital's name is **TBD** — to be named in a future session.

---

## 5. CLASS ICON ART NOTE

*(Saved from a prior session — do not lose this)*

For the dedicated art milestone, class icons will use **colored geometric shapes**:
- Fighter: Sword (shape)
- Mage: Star
- Cleric: Cross
- Thief: Diamond/dagger
- Ranger: Bow/leaf
- Monk: Circle/fist

Each class gets a distinctive color + shape combination so they're readable at a glance.

---

## 6. TRAVEL SYSTEMS

*(From World_Systems_Design_v2.md — summarized here for reference)*

- **Walking**: Default, 1 tile/step.
- **Horse**: 200g at stables, 2x speed on roads.
- **Boat**: 500g at ports; required for islands and coastal travel.
- **Flying Carpet**: Rare/expensive, ignores terrain.
- **Magical Rail**: Fixed routes between Mage Guild cities; requires guild membership quest.
- **Teleport Network**: Attune to circles at each Mage Academy; 50g/jump; instant travel.

---

## 7. SILVER WEAPONS & UNDEAD

- Only **magic** and **silver weapons** can damage ghosts/incorporeal undead.
- Silver weapons deal slightly less damage than equivalent steel (-10%) but get bonuses vs. undead, vampires, and werewolves.
- **Silvering Potion** (Mage-crafted): Temporarily coats any weapon in silver for one combat.
- Any weapon type can be made from silver (Silver Longsword, Silver Arrows, etc.).

---

## 8. ELEMENTAL MATERIALS

Elemental metals exist alongside standard tiers, carrying inherent elemental properties:

| Material | Element | Found In |
|----------|---------|----------|
| Flamesteel | Fire | Near volcanoes |
| Frostsilver | Ice | Frozen caverns |
| Stormite | Lightning | High mountains |
| Shadowmere | Shadow | Deep underground |
| Solarium | Divine | Holy sites |
| Livingwood | Nature | Ancient forests |

An elemental material weapon carries base elemental damage before enchanting.

---

## 9. KEY DESIGN PRINCIPLES

- **No content should feel wasted.** Every region, dungeon, and NPC should serve a purpose in the story or progression.
- **Power tiers create awe.** Bronze players should feel the weight of being on a tier 1 world with tier 2 figures in it.
- **The world is bigger than this game.** Hints of other planes, other tiers, future conflicts should be seeded throughout.
- **Class identity matters.** Every class should have a reason to exist in both combat AND the overworld.

---

## REVISION HISTORY
- 2026-02-23: Initial creation. Captured tier system, acts, 8-town plan, capital, class icons, travel, silver/elemental materials from conversation and prior design docs.
