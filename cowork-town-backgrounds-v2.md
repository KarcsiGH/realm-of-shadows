# Realm of Shadows — Town Background Images (v2)
## REPLACEMENT BRIEF — Previous images were wrong resolution

---

## THE PROBLEM WITH THE PREVIOUS IMAGES

The previous images used pixel blocks of ~24 real pixels each, giving an effective resolution of only 60×37 visual pixels on a 1440×900 canvas. Stretched to fill the screen, they look blurry and undetailed.

**This was wrong.**

---

## WHAT THE CHARACTER SPRITES ACTUALLY LOOK LIKE

The existing character sprites (Paladin.png, Necromancer.png, Fighter.png, etc.) are **1024×1024 PNG files drawn at full resolution** — every pixel in the file is 1 real pixel. They look like pixel art because of the artistic choices: flat colour fills within areas, hard edges between colours, limited palette, deliberate blocky shapes. But the detail level is HIGH — look closely at the Paladin and you can see individual armour plates, facial features, sun symbols, sword details.

**The backgrounds must match this quality level.**

---

## CORRECT STYLE SPECIFICATION

Draw at **full canvas resolution** (1440×900 for towns, 864×900 for buildings).

The pixel art aesthetic is achieved through ARTISTIC CHOICES, not through artificially large pixel blocks:

- **Flat colour fills** — each material (stone, wood, sky, fabric) uses a small number of distinct colours with no gradient within a block
- **Hard edges** — colour zones meet with a clean 1-2px edge, no smooth blending or anti-aliasing between major regions
- **Limited palette per image** — 16-24 colours maximum, used consistently
- **Deliberate dithering** sparingly — where you want a texture (rough stone, grass), use a fine 2-3px checkerboard dither pattern between two close colours, not large blocks
- **Clean, confident line work** — architectural details (window frames, roof lines, door frames) drawn with 1-2px lines
- **Characters as silhouettes** — any people in scenes are 8-16px tall silhouettes with clear shape, not blobs

Think of the quality level of **RPG Maker MV tilesets**, **Stardew Valley backgrounds**, or **Octopath Traveler** town views — that level of pixel art detail and craft, at full resolution.

---

## WHAT EACH IMAGE SHOULD CONTAIN

The atmosphere descriptions from the original brief remain valid. The change is only resolution and detail level. Reproduce the same scenes but with:
- Buildings that have clearly readable architecture (individual windows, doors, roof shapes)
- Sky with atmosphere (clouds, stars, fog rendered in fine pixel detail)
- Ground surfaces with texture (cobblestone = regular small rectangles, grass = fine dithered pattern)
- Foreground/midground/background depth layers clearly readable

---

## CANVAS SIZES (unchanged)

- **Town exteriors:** 1440 × 900 pixels
- **Building interiors:** 864 × 900 pixels

---

## SCENES TO GENERATE

### TOWN EXTERIORS — `assets/backgrounds/towns/`

**`briarhollow.png`** — Stone-and-timber village at forest edge. Evening light. An inn with a hanging lantern sign, a smithy with a chimney, a well in the muddy square. Dense forest pressing in from three sides, fog at the treeline. Warm amber lantern glow against cool dusk sky.
Palette: stone `#8A8070`, timber `#6B4020`, moss `#4A5530`, fog `#C8C8C0`, lantern `#D08020`, mud `#7A6040`, sky `#4A5870`

**`woodhaven.png`** — Village woven into massive ancient trees. Rope bridges between platforms in the branches. Carved wooden totems. Communal fire pit in a clearing below. Canopy so dense it filters the light green. Evening, warm fire below cold canopy.
Palette: deep forest `#2A4020`, bark `#5A3818`, filtered light `#C0A040`, fire `#E06020`, shadow `#1A2810`

**`ironhearth.png`** — Dwarven mining town in a mountain valley. Low reinforced stone buildings with iron-banded shutters. A great chimney belching forge-smoke. Mining cart tracks through the street. Iron bracket lanterns. Soot on everything. Mountain walls close on both sides.
Palette: soot grey `#4A4040`, iron `#707070`, forge smoke `#D06020`, coal `#1E1818`, stone `#686060`, lantern `#C08020`

**`crystalspire.png`** — City of arcane towers. Slender spires topped with crystal observatories. Blue geometric ley line patterns inlaid in cobblestones, glowing faintly. Robed scholars as silhouettes in tower windows. Stars visible faintly even in the day sky. Blue-silver light everywhere.
Palette: midnight `#1A1840`, crystal `#6080C0`, tower stone `#505060`, arcane glow `#80A0FF`, silver `#C0C8D0`

**`thornhaven.png`** — Imperial walled capital. Wide cobblestone boulevard. Imperial banners (deep red, gold sun). Lamp posts. Guard towers flanking a grand gatehouse. Noble townhouses with arched windows. A cracked fountain. Wealth visible, tension palpable.
Palette: imperial red `#802020`, gold `#C09020`, cobblestone `#787060`, stone `#908880`, dark window `#1A1820`

**`sanctum.png`** — Holy city dominated by the Grand Cathedral. Long processional avenue, cathedral facade visible at the end — soaring white stone, tall stained windows (pixel art coloured patterns: red, gold, blue). Thousands of candle-stands. Pilgrim silhouettes. Sky behind Cathedral almost too bright.
Palette: white stone `#E8E0D0`, candle `#D08820`, pilgrim `#787070`, processional stone `#B0A898`, holy light `#F8F0C0`

**`saltmere.png`** — Rough port town on a grey sea. Weathered wooden docks into dark water. Fishing boats, one scarred merchant vessel. Rope, nets, barrels. Rain-slicked cobbles. Tavern sign visible over a low building. Grey water to the horizon.
Palette: sea grey `#607080`, wet wood `#4A3828`, rope `#9A8050`, dark water `#283848`, lantern `#C07820`, seafoam `#90A8B0`

**`greenwood.png`** — Remote wilderness outpost, more camp than town. Clearing in deep forest. A few sturdy buildings — ranger post, supply cache, small shrine. Firepit with cooking pot in centre. Forest wild and close around the clearing. Vulnerable feeling.
Palette: deep forest `#283820`, firepit `#C06820`, timber `#6B4020`, parchment `#C0A870`, shadow `#1A2810`, earth `#5A4030`

**`emberveil.png`** — Volcanic outpost. Dark basalt buildings against a volcanic ridge. Lava channels between rocks glowing intense orange. Sky orange-red with ash haze. Steam vents. Renn's Forge the dominant structure. Everything on fire adjacent.
Palette: basalt `#201818`, lava `#E05020`, ash sky `#706060`, steam `#D0C8C0`, forge fire `#FF6010`, sulphur `#C0A020`

**`the_anchorage.png`** — Tiny fishing village on a coastal promontory. A handful of weathered buildings. Fishing boats above the tideline. A telescope on a tripod outside one building. Driftwood fences. Sea huge and dark in every direction. Wind-bent trees.
Palette: sea blue-grey `#4A6070`, driftwood `#8A8068`, salt white `#D0CEC0`, dark sea `#203040`, building stone `#706860`

**`the_holdfast.png`** — Fortified ruin in scorched Ashlands. Crumbling walls reinforced with salvage. Barricades of broken furniture and stone. Campfires inside. Exhausted soldier silhouettes. Fading corruption — darkness eating the sky — visible in the distance. Desperate last stand.
Palette: ash `#605850`, corruption void `#0A0810`, campfire `#C06020`, crumbling stone `#787068`, soot `#201818`, lantern `#D09030`

---

### BUILDING INTERIORS — `assets/backgrounds/buildings/`

Each interior is 864×900. The left 40% of this image will be covered by a dark UI panel in-game — put the most interesting detail in the **right 60%** (x > 345px). The left side should still be drawn (it shows at the edges of the panel blend) but can be simpler.

---

## INN INTERIORS (11 images)

**`briarhollow_inn.png`** — Stone hearth dominating one wall, fire crackling. Rough wooden tables, timber-plank bar. Candles in iron holders. Deer antlers. Worn clean stairs to rooms. The essential "starting inn."
**`woodhaven_inn.png`** — Common room carved around a living tree trunk rising through floor and ceiling. Hanging gourd lanterns. Round doorway to sleeping area. Everything smells of pine.
**`ironhearth_inn.png`** — Dwarven inn: stone benches, massive hearth, ale barrels floor to ceiling. Iron chandeliers hung low. Runic carved decorations (abstract block patterns) on one wall. Built for people who don't complain.
**`crystalspire_inn.png`** — Scholar's lounge. Blue-white fireplace (ley energy). Crystal wall fixtures glowing. Dark lacquered furniture. Bookshelf through an archway. Refined.
**`thornhaven_inn.png`** — Expensive city inn. Red velvet curtains, formal dining room visible through double doors. Portraits on walls (obscured faces). Doorman's stand. Intimidatingly clean.
**`sanctum_inn.png`** — Pilgrim's House: stone cells visible through a corridor. Long refectory table. Candles. A prayer alcove with an abstract Light symbol. Quiet and devout.
**`saltmere_inn.png`** — Saltwater Bunk: hammocks stacked in a low-ceilinged room. Salt-stained planks. Single oil lamp. Rope on pegs. Completely no-frills. You sleep with your gear.
**`greenwood_inn.png`** — Ranger base camp: field maps on walls, bedrolls on elevated platforms, central open firepit with smoke hole in roof. Hunting trophies and trail gear. Functional and rugged.
**`emberveil_inn.png`** — Everything basalt and iron (no wood — fire risk). Stone sleeping platforms with thin bedrolls. Geothermal vent providing warmth. Walls glow faintly orange from volcanic rock.
**`the_anchorage_inn.png`** — Converted fishing shed: half research space (charts, jars, notes pinned up), half sleeping area behind a curtain. Small stove. Porthole window showing dark sea.
**`the_holdfast_inn.png`** — Military bunkroom in crumbling fort. Stone platforms with bedrolls. Map of Spire approach pinned to wall. Single lantern. Through a broken section of wall: ash and darkness.

---

## STORE INTERIORS (8 images)

**`briarhollow_store.png`** — Cluttered general store. Shelves of barrels, crates, herbs, rope. Scales and ledger on counter. Lanterns from low ceiling. Pelts and dried goods in rafters. Homely disorder.
**`woodhaven_store.png`** — Organic store in tree space. Natural-shaped shelves of curved branches. Baskets, roots, carved tools, leather pouches. A cat on the counter. Everything foraged or handmade.
**`ironhearth_store.png`** — Dwarven supply house. Heavy metal shelving. Goods in locked glass-front cases. Mechanical counter (gear mechanisms). Ingots and ore in a back rack. Obviously superior quality.
**`crystalspire_store.png`** — Arcane provisions shop. Glowing component jars. Shelves of rare reagents. Focus crystals in illuminated cases. A glowing catalogue orb. Tidy and precise.
**`thornhaven_store.png`** — Imperial supply depot. Military-grade supplies alongside civilian goods. Imperial seals on crates. A formal counter. Everything stamped.
**`saltmere_store.png`** — Cramped waterfront shop. Goods jumbled on mismatched shelves. Salvage mixed with supplies. A suspicious pile with no labels. A bowl: "TAKE WHAT YOU NEED, PAY THE BOWL."
**`greenwood_store.png`** — Survival cache in a fortified storeroom. Metal-reinforced shelves. Rations, rope, medicine, arrows. A locked cabinet for expensive items. Spare and organised.
**`emberveil_store.png`** — Volcanic supply shop with heat-resistant containers. Volcanic mineral reagents glowing faintly on a shelf. Fire-resistant materials. Renn's forge visible orange through a back doorway.

---

## FORGE INTERIORS (7 images)

**`briarhollow_forge.png`** — Village smithy. One anvil, coal forge with bellows, tools on pegboard. Cooling blades in a trough. Horseshoes and farm implements alongside adventurer gear. Soot on every surface. Warm orange fire.
**`woodhaven_forge.png`** — Open-air forge against a standing stone chimney. Specialises in nature-motif weapons (leaf/vine/antler etchings visible on blade display rack). Tree-stump workbench. Fire burns with faint green tinge.
**`ironhearth_forge.png`** — MASTERWORK dwarven forge. Multiple forge stations with bellows systems. A mechanical hammer pulley system. Racks of armour plates and weapons in progress. Heat-shimmer visible near forges. The finest forge in the game. This image should feel IMPRESSIVE.
**`crystalspire_forge.png`** — Arcane forge with ley line energy instead of coal. Blue-white fire intensely bright. Crystal resonators on walls. Weapons glow faintly after passing through. Clinical precision.
**`thornhaven_forge.png`** — Imperial armory forge. Multiple worker silhouettes at stations. Organised racks of standard equipment alongside custom work. Imperial insignia on some pieces. Quality-control bench.
**`saltmere_forge.png`** — Ship-repair forge that also does weapons. Rivets and ship fittings alongside swords. Salvaged metal in bins. Crude but effective. Everything smells of salt and oil.
**`emberveil_forge.png`** — MASTERWORK volcanic forge. Built over a natural lava channel visible through a floor grate, glowing intense orange-red. Highest-quality blades on the rack. This is Renn's life work. Should feel powerful and dangerous.

---

## TEMPLE INTERIORS (6 images)

**`briarhollow_temple.png`** — Small village temple. Candles in every stone niche. Simple altar with flame symbol carved in relief. Healing herbs drying. Worn triptych painting above altar (abstract pixel shapes). Intimate.
**`woodhaven_temple.png`** — Grove shrine, almost outdoors. A cleared area between massive trees with a central carved standing stone, spiral patterns. Offerings of fruit and flowers. Filtered green light. Trees are the ceiling.
**`ironhearth_temple.png`** — Hall of the Stone Father. A mountain shape carved in relief across the entire back wall. Stone benches in rows. Iron lanterns hung very low. Vaulted stone ceiling with visible chisel marks. Austere power.
**`crystalspire_temple.png`** — Arcane-philosophical shrine. Ley line diagrams glow on walls. Crystal sphere on the altar. Bookshelves flanking sides. Sacred geometric patterns. Students treat it as both shrine and study space.
**`sanctum_temple.png`** — The Grand Cathedral. This should be the most impressive interior in the game. Soaring vaulted ceiling. Impossibly tall stained windows casting coloured light (red, gold, blue beams on the stone floor). Thousands of candles. Rows of pews receding into distance. Enormous gold-covered altar. AWE-INSPIRING.
**`greenwood_temple.png`** — A wayside shrine: a carved stone post with a flame symbol, some candles, a small carved wooden figure as offering. Forest clearing. One person can pray here. Modest but earnest.

---

## TAVERN INTERIORS (8 images)

**`briarhollow_tavern.png`** — The Mossy Flagon. Stone walls with ivy in cracks. Wooden tables with candles in bottles. Barrels behind a timber bar. 3-4 patron silhouettes. Notice board. Fireplace at back. Comfortable and dim.
**`woodhaven_tavern.png`** — Hollow Stump: inside a carved-out ancient tree stump, expanded. Curved wooden walls with carved forest scenes. Bar is a root section. Glowing mushrooms plus candles for light. Rustic and magical.
**`ironhearth_tavern.png`** — The Iron Mug. Iron tables bolted to the floor. Enormous ale mugs. A challenge board (drinking contest records). The barkeep silhouette large and no-nonsense. Loud and warm. A fight in progress in the corner (silhouettes).
**`crystalspire_tavern.png`** — The Flickering Glass. Faintly glowing drinks in crystal goblets. Patron silhouettes gesticulating in debate. Chalkboards covered in equations and diagrams. The bar serves potions alongside ale. Blue-white lighting.
**`thornhaven_tavern.png`** — The Bronze Lantern. Better furniture than Briarhollow. Distinctive bronze lanterns overhead. Political pamphlets rack near door. A stage in a corner (unused). Private booths. Busy.
**`saltmere_tavern.png`** — The Bilge. Sticky floor. Low ceiling hung with rope and ship parts. Every patron a silhouette with a story. Bar made from a ship's rail. Old nautical maps (stained) on walls. One flickering oil lamp. The strongest drink in the game served here with no name.
**`sanctum_tavern.png`** — The Quiet Cup. Subdued pilgrims and priests drinking quietly, whispering. Candles in religious holders. A painted eye above the bar (abstract). Clean, respectable. Good wine. No fights.
**`the_anchorage_tavern.png`** — The Salt & Scholar. Half nautical paraphernalia (nets, ropes, maritime maps), half research common room (charts, specimen jars). A porthole showing dark sea. Fishermen and Crystalspire researchers barely understanding each other.

---

## JOB BOARD INTERIORS (4 images)

**`briarhollow_jobboard.png`** — Notice board packed with paper slips (small coloured rectangles, illegible). A counter with a logbook. Guard post window behind. Functional.
**`woodhaven_jobboard.png`** — A carved wooden post in the village centre visible through administrative building window. Notices tied with twine. A village elder's desk with maps.
**`crystalspire_jobboard.png`** — A magical slate board where commissions appear inscribed in glowing blue script (block patterns). Administrative counter. Students studying the board.
**`thornhaven_jobboard.png`** — Formal government office. Imperial seals everywhere. Numbered service windows. Notices in formal type. Queue system. Maps of the realm on walls. Bureaucratic and imposing.

---

## DELIVERY

Save files to the correct folders in `~/Documents/RealmOfShadows/`:
- Town exteriors → `assets/backgrounds/towns/`  
- Building interiors → `assets/backgrounds/buildings/`

Use the EXACT same filenames as before (replacing the previous images).

Then push to git:
```bash
cd ~/Documents/RealmOfShadows
git add assets/backgrounds/
git commit -m "Replace town backgrounds with high-resolution versions"
git push origin main
```
