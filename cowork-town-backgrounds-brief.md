# Realm of Shadows — Town Background Images
## Cowork Session Brief: 57 Background Images

---

## CRITICAL STYLE RULES — Read First

These images are backgrounds for a pixel art RPG. They must match the visual language of the existing character sprites (chunky retro pixel art, ~20-32px per visual dot, hard edges, flat colour fills, limited palettes).

### Canvas size
- **Town exteriors:** 1440 × 900 pixels (landscape, full screen)
- **Building interiors:** 864 × 900 pixels (landscape, right-side panel — 60% of the 1440 screen)

### Style requirements
- **Chunky pixel art** — each "pixel" in the design is a large square block, roughly 20-32 real pixels per dot. No smooth gradients within blocks. Hard edges everywhere.
- **No anti-aliasing on pixel boundaries** — colour transitions are abrupt, step-by-step
- **Limited palettes** — 8-14 distinct colours per image. Flat fills inside each block.
- **Dark atmospheric tone** — this is a dark fantasy game. Even warm inn interiors should feel slightly dim and aged. No bright cheerful cartoon colours.
- **Pure white (#FFFFFF) or transparent background is NOT used** — these are scene images, not character sprites. Fill the entire canvas. No empty space.
- **No text, no UI elements, no title cards** — pure environmental art only.

### What these images look like in-game
- **Town exteriors** sit as the full-screen backdrop of the town hub menu. A semi-transparent dark panel overlays the left 42% of the screen (where buttons appear). Your image should be most interesting on the **right 58%**.
- **Building interiors** fill the right 60% of the screen while the functional UI sits on the left 40%. Composition should be most interesting in the **centre and right** of the image.

---

## PART 1: TOWN EXTERIOR BACKGROUNDS (11 images)
### Save location: `assets/backgrounds/towns/{town_id}.png`

These are wide establishing shots of each town — the view a traveller would have arriving at or standing in the town centre. Think of them as the "title card" image for each location.

---

### `briarhollow.png`
**The starting town. A quiet village at the edge of wild lands.**
Stone-and-timber buildings with mossy roofs cluster around a muddy central square. An old well. The Wanderer's Rest inn visible with a hanging lantern sign. Dense forest presses in on three sides. Fog at the treeline. Late afternoon light, warm but tired. A weathervane shaped like a crow.
**Palette:** Stone grey `#8A8070`, timber brown `#6B4020`, moss green `#4A5530`, fog white `#C8C8C0`, lantern amber `#D08020`, muddy path `#7A6040`.

---

### `woodhaven.png`
**A village woven into a great forest — buildings half-grown from living trees.**
Massive ancient trees with platforms and rope bridges connecting upper-storey homes. The forest floor below is dappled with filtered green light. Carved wooden totems mark the paths. A communal fire pit in the clearing. The canopy overhead is dense enough to feel like a ceiling.
**Palette:** Deep forest green `#2A4020`, bark brown `#5A3818`, moss `#3D5028`, filtered light gold `#C0A040`, carved wood `#8B5E30`, shadow `#1A2810`.

---

### `ironhearth.png`
**A dwarven mining town buried in a mountain valley. Always smells of iron and coal.**
Low stone buildings with reinforced doors and iron-banded shutters. A great chimney belching orange-grey smoke dominates the skyline — the Deep Forge. Mining cart tracks cut through the central street. Lanterns hang on iron brackets. The mountain walls are close on both sides. Everything is covered in a thin layer of soot and proud of it.
**Palette:** Soot grey `#4A4040`, iron `#707070`, forge orange `#D06020`, coal black `#1E1818`, stone `#686060`, lantern gold `#C08020`.

---

### `crystalspire.png`
**A city of arcane towers with ley lines visible as faint blue light in the streets.**
Slender towers topped with crystal observatories. Glowing blue geometric patterns inlaid in the cobblestones — ley line channelling arrays. Robed scholars visible as silhouettes in tower windows. A grand gate to the Mage Academy visible in the background. The sky seems slightly wrong here — the stars appear even during the day, faintly.
**Palette:** Midnight blue `#1A1840`, crystal blue `#6080C0`, tower stone `#505060`, arcane glow `#80A0FF`, silver `#C0C8D0`, scholar robe `#303050`.

---

### `thornhaven.png`
**The Imperial capital — a proper walled city with guard towers and cobbled boulevards.**
A wide cobblestone boulevard with Imperial banners (deep red with a gold sun) hanging between lamp posts. Guard towers flank a grand gatehouse in the background. Noble townhouses with arched windows. A fountain (currently dry and cracked). The wealth is real but the tension is palpable — the city knows something is wrong.
**Palette:** Imperial red `#802020`, gold banner `#C09020`, cobblestone grey `#787060`, stone `#908880`, dark window `#1A1820`, faded gold `#A08030`.

---

### `sanctum.png`
**A holy city — the Grand Cathedral of Light dominates everything.**
The Cathedral's facade is visible at the end of a long processional avenue, all white stone with tall stained-window arches (stained glass rendered in pixel art as coloured block patterns). Thousands of candles in stands line the avenue. Pilgrims as silhouetted figures in the distance. Everything points toward the Cathedral. The sky behind it is too bright.
**Palette:** Cathedral white `#E8E0D0`, candle gold `#D08820`, pilgrim grey `#787070`, processional stone `#B0A898`, shadow `#282020`, holy light `#F8F0C0`.

---

### `saltmere.png`
**A rough port town on a grey sea. Docks, ships, and secrets.**
Weathered wooden docks extending into dark choppy water. Fishing boats and one scarred merchant vessel. Rope, nets, and barrels stacked everywhere. The Bilge tavern sign over a low building with one broken window. Seagulls as pixel silhouettes. The horizon is grey water all the way to the edge. Rain-slicked cobbles.
**Palette:** Sea grey `#607080`, wet wood `#4A3828`, rope tan `#9A8050`, dark water `#283848`, lantern amber `#C07820`, sea foam `#90A8B0`.

---

### `greenwood.png`
**A remote wilderness outpost. More of a camp than a town.**
A clearing in deep forest with a few sturdy buildings — the ranger's post, a supply cache, a small shrine. Scouting reports pinned to a board. A large map of the surrounding wilderness on one wall. Firepit in the centre with a cooking pot. The forest around is wild and close. Feels exposed.
**Palette:** Deep forest `#283820`, firepit orange `#C06820`, post timber `#6B4020`, map parchment `#C0A870`, shadow green `#1A2810`, earth brown `#5A4030`.

---

### `emberveil.png`
**A volcanic outpost. Everything is slightly on fire.**
Low stone buildings built against a volcanic ridge, lava visible in deep channels between rocks. The sky is orange-red with ash haze. Steam vents in the ground. Renn's Forge is easily the biggest structure, with a massive chimney. The buildings are made of volcanic rock — dark basalt with heat-cracked surfaces. Hot and hostile.
**Palette:** Basalt black `#201818`, lava orange `#E05020`, ash grey `#706060`, steam white `#D0C8C0`, forge fire `#FF6010`, sulphur yellow `#C0A020`.

---

### `the_anchorage.png`
**A tiny fishing village on the edge of the known sea. Research outpost.**
A handful of weathered buildings at the end of a windswept coastal promontory. Fishing boats dragged above the tideline. A telescope on a tripod outside one building (the Crystalspire researchers). Salt-bleached driftwood fences. The sea is huge and dark in every direction except the land side. Wind-bent trees.
**Palette:** Sea grey-blue `#4A6070`, driftwood `#8A8068`, salt white `#D0CEC0`, dark sea `#203040`, building stone `#706860`, research light `#A0C0E0`.

---

### `the_holdfast.png`
**The last safe ground before the Spire. A fortified ruin in the Ashlands.**
Scorched earth and ash as far as can be seen. The Holdfast is a half-ruined fort — walls crumbling but reinforced with whatever could be salvaged, barricades of broken furniture and stone. Campfires inside the walls. A few exhausted soldiers and survivors as silhouetted figures. The Fading corruption is visible in the distance as darkness eating the sky. Desperate.
**Palette:** Ash grey `#605850`, corruption void `#0A0810`, campfire amber `#C06020`, crumbling stone `#787068`, soot black `#201818`, survivor lantern `#D09030`.

---

## PART 2: BUILDING INTERIOR IMAGES (46 images)
### Save location: `assets/backgrounds/buildings/{town_id}_{type}.png`

These are viewed on the right 60% of the screen while the functional UI is on the left 40%. Composition should work as a **wide scene viewed from outside** — like looking into the building through a window, or an establishing shot of the interior.

Key principle: **same building type, different town = same function but different character.** The Ironhearth forge is grander and more industrial than the Briarhollow smithy. The Sanctum temple is breathtaking. The Holdfast inn is a sleeping-bag-on-a-cot situation.

---

## INN INTERIORS (11 images — one per town)

**What all inns have:** A hearth, some kind of sleeping arrangement, a bar or counter, warm lighting. The vibe ranges from cozy (briarhollow) to desperate (the_holdfast).

### `briarhollow_inn.png`
Warm stone hearth dominating one wall, fire crackling. Rough wooden tables, a bar made from a single thick timber plank. Candles in iron holders. Deer antlers on the wall. Worn but clean. The definitive "starting town inn" — humble and welcoming.
**Palette:** Warm amber `#C08020`, stone `#787060`, timber `#6B3818`, firelight `#E06010`, cream plaster `#C8B890`, shadow `#2A1E10`.

### `woodhaven_inn.png`
The common room has been carved into and around a living tree — the trunk rises through the floor and ceiling. Hanging lanterns made from hollowed gourds. Carved wooden furniture. The sleeping area visible through a round doorway at the back. Everything smells of pine and woodsmoke.
**Palette:** Living wood `#5A3818`, green light `#607840`, gourd lantern `#C09030`, bark `#4A2E10`, shadow `#1A2010`, warm amber `#C08040`.

### `ironhearth_inn.png`
The Anvil & Hearth is a dwarven inn — everything oversized and heavily built. Stone benches instead of chairs. The hearth is massive, industrial. Ale barrels stacked floor to ceiling on one wall. Low ceilings with iron chandeliers. A dwarven drinking song carved into one wall in runic script (rendered as decorative block patterns, not readable text).
**Palette:** Iron `#707070`, forge stone `#606060`, hearth fire `#D05010`, ale barrel `#6B3810`, iron chandelier `#404040`, dark stone `#282828`.

### `crystalspire_inn.png`
The Ley Line Lodge — the hearth here channels ley line energy so the fire is blue-white instead of orange. Crystal fixtures on the walls glow faintly. The furniture is elegant, dark lacquered wood. Bookshelves visible through an archway. Feels more like a scholar's lounge than a tavern.
**Palette:** Midnight blue `#1A1840`, crystal glow `#7090FF`, blue flame `#90B0FF`, dark lacquer `#201820`, silver accent `#B0B8C8`, arcane light `#6080E0`.

### `thornhaven_inn.png`
The Governor's Rest — by far the most expensive-looking inn. Red velvet curtains. A formal dining room visible through double doors. Portraits on the walls (obscured faces, just vague Imperial-looking figures). A doorman's stand near the entrance. Clean to the point of intimidation.
**Palette:** Velvet red `#802030`, gold trim `#C09020`, dark mahogany `#3A1E0E`, portrait grey `#808080`, cream wall `#D0C8A0`, chandelier gold `#D0A020`.

### `sanctum_inn.png`
The Pilgrim's House — not really an inn, more like church accommodation. Simple stone cells visible through a corridor. A single long refectory table. Candles everywhere. A prayer alcove in one corner with a symbol of the Light. Very clean, very quiet. The hospitality of the devout.
**Palette:** Cathedral white `#E0D8C8`, candle gold `#C08020`, grey stone `#808878`, prayer alcove `#604828`, shadow `#282020`, holy light `#F0E8C0`.

### `saltmere_inn.png`
The Saltwater Bunk — hammocks stacked in a low-ceilinged room. Rough-hewn plank floor, salt-stained everything. A single oil lamp. Ropes coiled on pegs. It smells of fish and brine. Absolutely no frills. The bar is a plank over two barrels. You sleep with your gear.
**Palette:** Salt-grey wood `#787060`, hammock rope `#9A8848`, oil lamp amber `#C07820`, brine stain `#607880`, dark shadow `#201818`, rope `#A89060`.

### `greenwood_inn.png`
The Ranger's Post common room — more like a base camp than an inn. Field maps pinned to the walls. Bedrolls on elevated wooden platforms. A central firepit (open, not a hearth — this building has a smoke hole in the roof). Hunting trophies and trail gear hanging on pegs. Functional and rugged.
**Palette:** Pine green `#3A4820`, firepit `#C06820`, timber `#6B4020`, map parchment `#C0A870`, gear leather `#7A5030`, smoke shadow `#282018`.

### `emberveil_inn.png`
The Ash Bunk — everything is made of basalt and iron. No wood (it would catch fire). Sleeping platforms carved from stone with thin bedrolls. A small geothermal vent in one corner provides warmth (and occasional sulphur). The walls glow faintly orange from the volcanic rock itself.
**Palette:** Basalt `#201818`, lava-warm glow `#804010`, iron fitting `#606060`, sulphur `#808010`, bedroll `#6A5040`, volcanic rock glow `#602808`.

### `the_anchorage_inn.png`
The Researcher's Bunk — a converted fishing shed. Half the room is still a working research space — charts, samples in jars, notes pinned everywhere. The sleeping area is partitioned off with a curtain. A small stove, not a hearth. Through the window (a small porthole) you can see the dark sea.
**Palette:** Weathered wood `#6A5840`, research paper `#C0B890`, jar glass `#708890`, sea-view dark `#203040`, stove iron `#404040`, curtain `#8A7060`.

### `the_holdfast_inn.png`
The Commander's Quarters — not really an inn. This is a military bunkroom in a crumbling fort. Stone walls with cracks showing the Ashlands outside. Bedrolls on stone platforms. A map of the Spire approach pinned to one wall. A single lantern. Through a broken window: ash and darkness. People sleep here because there is nowhere else.
**Palette:** Crumbling stone `#605850`, lantern amber `#C05820`, ash grey `#787068`, map parchment `#B0A070`, bedroll `#5A4A38`, void dark `#0A0810`.

---

## STORE INTERIORS (8 images — not all towns have a store)

**What all stores have:** Shelves of goods, a counter, lighting, the visual texture of commerce. Tone varies from general provisions to specialised.

### `briarhollow_store.png`
Harrow's Trading Post — a cluttered general store. Wooden shelves packed with barrels, crates, bundled herbs, coils of rope. A counter with scales and a ledger. Lanterns hung from the low ceiling. Pelts and dried goods hanging from the rafters. The floor is bare earth. Homely disorder.
**Palette:** Timber `#6B3818`, barrel wood `#7A4820`, herb green `#5A6830`, pelt brown `#8A6040`, lantern gold `#C08020`, earth floor `#6A5030`.

### `woodhaven_store.png`
Mira's Forest Goods — an organic-feeling store woven into a tree space. Goods displayed on natural-shaped shelves made from curved branches. Everything is foraged, grown, or handmade — no imported metal goods. Baskets, roots, carved wooden tools, leather pouches. A cat sits on the counter.
**Palette:** Branch shelf `#7A5028`, basket `#C0A060`, foliage green `#4A5A28`, leather `#8A6040`, cat grey `#808080`, filtered light `#B0A060`.

### `ironhearth_store.png`
Stonebacker's Goods — a dwarven supply house. Everything is heavier and better-made than you'd find elsewhere. Metal shelving. Goods in locked glass-front cases. A mechanical counter (gears, levers). Ingots and raw ore visible in a back rack. The quality is obviously superior. Expensive.
**Palette:** Iron shelving `#606060`, ore grey `#5A5050`, dark stone `#303030`, glass front `#7090A0`, gold case trim `#C09020`, ingot silver `#B0B0A8`.

### `crystalspire_store.png`
Arcane Provisions — a shop for mages. Glowing component samples in sealed jars. Shelves of rare reagents, each labelled in precise script (block patterns, not readable text). Focus crystals displayed under illuminated cases. The shop itself is very tidy, very precise. A magical catalogue system (a glowing orb you tap).
**Palette:** Crystal blue `#6080C0`, jar glow `#90B0FF`, dark shelving `#202040`, reagent amber `#C09040`, label white `#E0E8F0`, arcane light `#7090E0`.

### `thornhaven_store.png`
Imperial Supply House — a large, well-organised Imperial procurement depot. Military-grade supplies alongside civilian goods. Stamped Imperial seals on crates. A formal counter staffed by a clerk in Imperial livery (silhouetted). Items in proper display cases with typed labels. Everything has a tax stamp.
**Palette:** Imperial red accent `#802020`, dark wood shelving `#3A2010`, supply grey `#808080`, crate `#7A6040`, gold seal `#C09020`, counter marble `#D0C8C0`.

### `saltmere_store.png`
Finn's Dockside Goods — a cramped waterfront shop that smells of fish and salt. Goods jumbled on mismatched shelves. Salvage items mixed with supplies. A suspicious pile of things in the corner with no labels. The shopkeeper isn't here; a sign says "TAKE WHAT YOU NEED, PAY THE BOWL." A chipped bowl on the counter.
**Palette:** Salt-worn wood `#787060`, rope tan `#9A8848`, salvage mixed `#808070`, dark corner `#201818`, bowl clay `#9A7050`, sea-damp `#607880`.

### `greenwood_store.png`
Trail Cache — a supply cache in a fortified store-room. Metal-reinforced shelves. Everything is for survival in the wilderness — rations, rope, medicine, arrows. Functional labelling (block patterns). A locked cabinet for the expensive things. Sparse. No frills. Well-organised because your life depends on finding things fast.
**Palette:** Metal shelf `#606060`, lock iron `#404040`, ration pack `#8A7040`, medicine green `#5A7840`, rope `#A09050`, stone wall `#686058`.

### `emberveil_store.png`
Renn's Supplies — the only general store near a volcano. Heavily heat-resistant containers. Volcanic mineral reagents on one shelf (glowing faintly). Fire-resistant materials. Renn's forge is visible through an open doorway at the back, lit bright orange. The shop is compact and practical.
**Palette:** Basalt `#201818`, volcanic mineral glow `#A04010`, heat container `#706060`, fire through doorway `#E05010`, iron shelf `#504040`, practical grey `#686060`.

---

## FORGE INTERIORS (7 images — not all towns have a forge)

**What all forges have:** A main forge fire, anvils, tools, hanging weapons/armour. The difference is scale, style, and heat level.

### `briarhollow_forge.png`
Aldric's Smithy — a village forge. One main anvil, a coal forge with bellows, tools hung neatly on pegboard. Unfinished blades cooling in a trough. Horseshoes and farming implements alongside adventurer gear. Small but capable. Soot on every surface. The forge fire is warm orange.
**Palette:** Forge fire `#E05010`, coal black `#1E1818`, anvil iron `#5A5850`, trough water `#405060`, tool grey `#808078`, soot `#302820`.

### `woodhaven_forge.png`
Oakbrand Smithy — unusual: the forge is partially open-air, built against a standing stone that acts as the chimney. Specialises in weapons decorated with natural motifs — leaves, vines, antlers etched into blades visible on the display rack. A large tree-stump workbench. The fire here burns with a faint green tinge from the wood.
**Palette:** Green-tinge fire `#809010`, standing stone `#706060`, stump bench `#6B4020`, leaf-etched blade `#A0A090`, vine display `#4A5A28`, open sky behind `#304028`.

### `ironhearth_forge.png`
The Deep Forge — a masterwork of dwarven engineering. Multiple forge stations with bellows systems. A mechanical hammer arm (a pulley-and-wheel system, pixel art industrial). Racks of work-in-progress: armour plates, weapons, tools. The temperature is visibly intense — heat shimmer conveyed through pixel distortion lines near the forges. This is the finest forge in the game.
**Palette:** Intense forge white-orange `#FF8020`, dwarven iron `#484040`, mechanical gear `#707070`, armour rack `#808080`, heat shimmer red `#D04010`, dark forge stone `#282020`.

### `crystalspire_forge.png`
Resonance Forge — an arcane forge that uses focused ley line energy instead of coal. The fire is blue-white, intensely bright. Crystal resonators mounted on the walls amplify the heat through magical focus. The work here is enchanting-grade — weapons emit a faint glow after passing through this forge. Extremely precise, almost clinical.
**Palette:** Arcane fire blue-white `#C0D0FF`, resonator crystal `#8090D0`, forge stone `#303050`, enchanted blade glow `#7090FF`, arcane heat `#A0B0E0`, dark stone `#181828`.

### `thornhaven_forge.png`
Tanner's Armory — an Imperial-contracted forge. Multiple workers (silhouettes) at different stations. Organised racks of standard Imperial-issue equipment alongside custom work. Imperial insignia on some pieces. A quality-control bench with inspection tools. Industrial-scale for a city forge but not as specialised as Ironhearth.
**Palette:** Imperial red tools `#802020`, iron `#686060`, working forge orange `#D05010`, rack steel `#909090`, stone floor `#787068`, dark ceiling `#282020`.

### `saltmere_forge.png`
Harker's Rivet Shop — a ship-repair forge that also does weapons. Everything smells of salt and oil. Rivets and ship fittings share the racks with swords and daggers. A crude but effective forge station. Salvaged metal in bins. The work is functional, not pretty. A few improvised tools made from ship parts.
**Palette:** Rust orange `#907040`, salt-corroded iron `#707868`, rivet bins `#5A5048`, oily dark `#201818`, crude forge fire `#C05818`, sea-metal `#6A7870`.

### `emberveil_forge.png`
Renn's Forge — the highest-quality forge in Act 3. Built directly over a natural lava channel — the forge uses volcanic heat, not fuel. The blade rack holds weapons of exceptional quality. Renn's workbench is covered in Act 3 materials. The lava channel is visible through a grate in the floor, glowing intense orange-red. Masterwork.
**Palette:** Lava channel `#E03008`, volcanic heat `#C04010`, master blade `#A0A0B0`, basalt floor `#201818`, grate iron `#404040`, intense orange `#FF5010`.

---

## TEMPLE INTERIORS (6 images — not all towns have a temple)

**What all temples have:** Candles/light sources, an altar or shrine, religious iconography (abstract pixel art — not specific real-world religion). Tone varies from intimate (greenwood) to vast (sanctum).

### `briarhollow_temple.png`
Temple of the Flame — a small village temple. Stone walls with candles in every niche. A simple altar with an abstract flame symbol carved in relief. Healing herbs drying on a rack. A triptych painting (pixelated, abstract shapes) above the altar. Intimate and worn with use.
**Palette:** Candle gold `#C08020`, stone grey `#787060`, altar cloth `#8A4030`, flame symbol `#E06010`, herb green `#5A6830`, shadow `#201820`.

### `woodhaven_temple.png`
Grove Shrine — almost entirely outdoors, or feels like it. The "temple" is a cleared area between massive trees with a central standing stone carved with spiral patterns. Offerings of fruit and flowers at the base (pixel art). Filtered green light through the canopy. No ceiling — the trees are the roof.
**Palette:** Standing stone `#706860`, spiral carving `#504848`, forest green `#2A4020`, offering colour `#A06030`, filtered light `#90A040`, deep shadow `#1A2010`.

### `ironhearth_temple.png`
Hall of the Stone Father — a dwarven religious space. The icon here is not a flame but a mountain shape carved in relief across the entire back wall. Stone benches in rows. Iron lanterns hanging very low. The ceiling is vaulted stone with visible chisel marks — dwarven reverence for the mountain itself. Austere and powerful.
**Palette:** Dark stone `#383030`, mountain carving `#504848`, iron lantern `#C07820`, carved ceiling `#484040`, lantern warm `#D09030`, deep shadow `#201818`.

### `crystalspire_temple.png`
The Spire Shrine — less religious, more arcane-philosophical. Abstract ley line diagrams on the walls glow faintly. The altar holds a crystal sphere. Bookshelves flank the sides. Students and scholars treat this as both a shrine and a study space. The iconography is geometric and precise — sacred patterns in pure mathematics.
**Palette:** Crystal sphere `#90B0FF`, ley diagram `#6080D0`, dark stone `#202040`, candle silver `#C0C8E0`, geometric light `#8090C0`, shadow `#101830`.

### `sanctum_temple.png`
The Grand Cathedral — the most magnificent space in the game. Soaring vaulted ceiling, impossibly tall. Stained windows (pixel art coloured-glass patterns in red, gold, white) that cast coloured light on the stone floor in long beams. Thousands of candles. Rows of pews receding into the distance. The altar is enormous, gold-covered. This should feel awe-inspiring even in pixel art.
**Palette:** Cathedral gold `#C09020`, stained red `#901820`, stained blue `#2040A0`, cream stone `#D0C8B0`, candle warm `#E08020`, deep shadow `#181010`.

### `greenwood_temple.png`
Wayside Shrine — a travelling shrine, not a building. A carved stone post with a flame symbol, some candles, a small carved wooden figure as an offering. Set in a forest clearing. Modest. The kind of shrine you find on a road. One person can pray here; that's enough.
**Palette:** Shrine stone `#706858`, candle flame `#C07820`, carved figure `#8A6040`, forest around `#2A4020`, earth `#5A4030`, sky through trees `#304028`.

---

## TAVERN INTERIORS (8 images — not all towns have a tavern)

**What all taverns have:** Tables, a bar, drinks, some patrons as silhouettes, atmosphere. The key differentiator is the crowd and the vibe.

### `briarhollow_tavern.png`
The Mossy Flagon — a small, dim, friendly tavern. Stone walls with ivy in the cracks. Wooden tables with candles in bottles. A bar along one wall with barrels behind it. Three or four patron silhouettes in various states of relaxation. A notice board with hand-written flyers. A fireplace at the back. Comfortable.
**Palette:** Dim amber `#C07820`, stone `#787060`, dark wood table `#4A3018`, barrel `#7A4820`, ivy green `#4A5828`, shadow `#201810`.

### `woodhaven_tavern.png`
The Hollow Stump — literally inside a hollowed ancient tree stump, expanded. The curved wooden walls have been carved with scenes of the forest. The bar is a section of root. Glowing mushrooms provide additional light alongside candles. Rustic and magical simultaneously.
**Palette:** Curved wood `#5A3818`, mushroom glow `#90A020`, root bar `#6B4020`, candle `#C07820`, bark shadow `#2A1808`, carved scene `#4A3018`.

### `ironhearth_tavern.png`
The Iron Mug — a dwarven drinking establishment. Everything is built for durability — iron tables bolted to the floor. Enormous ale mugs. A challenge board on the wall (drinking contest records). The barkeep is large and extremely no-nonsense. Loud. Warm. A fight may or may not be happening in the corner.
**Palette:** Iron table `#505048`, dark stone `#303028`, ale amber `#C07020`, fire in hearth `#D05010`, shadow `#1E1818`, barkeep silhouette `#282020`.

### `crystalspire_tavern.png`
The Flickering Glass — a mage's tavern. Drinks that glow faintly in crystal goblets. Animated discussions at every table (silhouettes gesturing). Chalkboards covered in equations and diagrams on the walls. The bar serves potions alongside ale. The light is blue-white from crystal fixtures. Intellectual and slightly pretentious.
**Palette:** Crystal goblet `#7090FF`, glow drink `#90B0FF`, dark wood `#201830`, chalkboard `#303840`, chalk marks `#D0D8E0`, arcane fixture `#6080D0`.

### `thornhaven_tavern.png`
The Bronze Lantern — a prosperous city tavern with some Imperial patronage. Better furniture than Briarhollow, worse than the inn. Bronze lanterns overhead (distinctive). Political pamphlets on a rack near the door. A stage in the corner (currently unused). Booths for private conversations. Busy.
**Palette:** Bronze lantern `#C08030`, dark booth `#2A1E10`, city table `#5A4020`, stone floor `#787068`, pamphlet rack `#8A7040`, warm light `#D08020`.

### `saltmere_tavern.png`
The Bilge — the worst tavern, and therefore the most interesting. Sticky floor. Low ceiling with hanging rope and ship parts. Every patron is a silhouette with a story. A bar made from a ship's rail. Old nautical maps on the walls (stained). The strongest drink in the game is served here with no name. One flickering oil lamp.
**Palette:** Sticky dark `#1E1818`, oil lamp `#C06818`, ship-rail bar `#5A4828`, map stain `#7A6840`, rope `#9A8848`, patron dark `#282020`.

### `sanctum_tavern.png`
The Quiet Cup — near the Cathedral, this tavern is surprisingly subdued. Pilgrims and priests drink quietly. Whispering. The decor nods toward the Cathedral — candles in religious holders, a painted eye above the bar (abstract, not specific). Clean, respectable. Good wine. No fights.
**Palette:** Cathedral cream `#D0C8A8`, candle gold `#C08020`, dark wood `#3A2818`, painted eye `#806040`, quiet shadow `#201820`, wine red `#602020`.

### `the_anchorage_tavern.png`
The Salt & Scholar — half tavern, half research common room. One side has fishing nets and maritime paraphernalia; the other has charts and specimen jars on shelves. The clientele is half fishermen, half Crystalspire researchers. A large porthole window shows the dark sea. A functional space for two groups that barely understand each other.
**Palette:** Maritime rope `#9A8848`, research shelf `#607060`, porthole sea `#203040`, chart paper `#C0B890`, specimen jar `#708890`, shadow `#201818`.

---

## JOB BOARD INTERIORS (4 images)

**What all job boards have:** A physical board with posted notices, a counter or desk, a functional workspace. The visual key is the notices on the board — render these as small illegible block patterns, not readable text.

### `briarhollow_jobboard.png`
Aldric's Notice Board — actually just outside the guard post, but covered. A large corkboard packed with notices (block-pattern rectangles, different colours, different sizes). A counter with a logbook. A guard post visible through a window. Functional.
**Palette:** Cork board `#9A7848`, notice paper `#C0B890`, guard grey `#707068`, counter `#6A4820`, logbook `#D0C8A0`, post wall `#787060`.

### `woodhaven_jobboard.png`
Village Notice Post — a carved wooden post in the village centre, visible through the window of the administrative building. Notices tied with twine (block patterns). A village elder's desk with maps.
**Palette:** Carved post `#6B4020`, twine `#A09050`, notice `#C0B890`, map `#B0A070`, elder desk `#5A3818`, village light `#C0A040`.

### `crystalspire_jobboard.png`
Academy Commission Board — the job board is a magical display: a large slate board where commissions appear inscribed in glowing text (block patterns in blue). Multiple students studying the board. An administrative counter staffed by an Academy functionary. Highly organised.
**Palette:** Magic slate `#303050`, glowing text `#7090FF`, counter stone `#4A4860`, student silhouette `#282040`, academy blue `#5070A0`, parchment `#C0C8E0`.

### `thornhaven_jobboard.png`
Imperial Contracts Office — a formal government office with numbered windows. Imperial seals everywhere. Notices in formal type (block patterns). A queue system. Maps of the realm on the walls. Bureaucratic and intimidating. The most organised board in the game.
**Palette:** Imperial red `#802020`, formal dark wood `#3A2010`, government white `#D0C8B8`, seal gold `#C09020`, map wall `#A09060`, shadow `#201818`.

---

## DELIVERY CHECKLIST

Save files exactly as named. All paths relative to the game root `~/Documents/RealmOfShadows/`:

**Town exteriors — `assets/backgrounds/towns/`:**
- [ ] briarhollow.png
- [ ] woodhaven.png
- [ ] ironhearth.png
- [ ] crystalspire.png
- [ ] thornhaven.png
- [ ] sanctum.png
- [ ] saltmere.png
- [ ] greenwood.png
- [ ] emberveil.png
- [ ] the_anchorage.png
- [ ] the_holdfast.png

**Building interiors — `assets/backgrounds/buildings/`:**
- [ ] briarhollow_inn.png / woodhaven_inn.png / ironhearth_inn.png / crystalspire_inn.png / thornhaven_inn.png / sanctum_inn.png / saltmere_inn.png / greenwood_inn.png / emberveil_inn.png / the_anchorage_inn.png / the_holdfast_inn.png
- [ ] briarhollow_store.png / woodhaven_store.png / ironhearth_store.png / crystalspire_store.png / thornhaven_store.png / saltmere_store.png / greenwood_store.png / emberveil_store.png
- [ ] briarhollow_forge.png / woodhaven_forge.png / ironhearth_forge.png / crystalspire_forge.png / thornhaven_forge.png / saltmere_forge.png / emberveil_forge.png
- [ ] briarhollow_temple.png / woodhaven_temple.png / ironhearth_temple.png / crystalspire_temple.png / sanctum_temple.png / greenwood_temple.png
- [ ] briarhollow_tavern.png / woodhaven_tavern.png / ironhearth_tavern.png / crystalspire_tavern.png / thornhaven_tavern.png / saltmere_tavern.png / sanctum_tavern.png / the_anchorage_tavern.png
- [ ] briarhollow_jobboard.png / woodhaven_jobboard.png / crystalspire_jobboard.png / thornhaven_jobboard.png

**After delivery — no code changes needed. The game finds images by filename automatically.**
**Run to verify:** `cd ~/Documents/RealmOfShadows && python3 -c "from ui.town_backgrounds import get_town_bg; import pygame; pygame.init(); print('OK')"`

---

## DELIVERY — HOW TO SAVE AND PUSH

After generating all images, save them to the correct folders on your Mac (paths are relative to the game root `~/Documents/RealmOfShadows/`):

- Town exteriors → `assets/backgrounds/towns/`
- Building interiors → `assets/backgrounds/buildings/`

Then push everything to git in one step:

```bash
cd ~/Documents/RealmOfShadows
git add assets/backgrounds/
git commit -m "Add town and building background images (57 files)"
git push origin main
```

That's it. The next development session pulls from main and the images appear automatically — no further steps needed.
