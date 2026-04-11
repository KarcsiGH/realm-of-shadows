# Missing Hybrid Class Sprites (3 images)

## HOW TO DO THIS JOB

You will generate 3 images using ChatGPT's image generation. Follow these steps for EVERY image:

**STEP 1:** Open ChatGPT in the browser at https://chatgpt.com
**STEP 2:** Start a new conversation
**STEP 3:** Upload these two files as style reference images:
  - ~/Documents/RealmOfShadows/assets/sprites/characters/Paladin.png
  - ~/Documents/RealmOfShadows/assets/sprites/characters/Spellblade.png
**STEP 4:** Tell ChatGPT: "These are the style reference images. Generate all future images in exactly this pixel art style."
**STEP 5:** Paste the image prompt for each image
**STEP 6:** Download the generated image using the download button
**STEP 7:** Move and rename the downloaded file to the exact path shown
**STEP 8:** Confirm the file exists before moving to the next image

Do NOT use Python to draw images. Do NOT use PIL or any drawing library.
Use ChatGPT image generation ONLY.
Do each image one at a time.

---

## IMAGE 1

**Save to:** ~/Documents/RealmOfShadows/assets/sprites/characters/Druid.png

**Paste this into ChatGPT:**
Pixel art character portrait in the exact same style as the reference images I uploaded, 1024x1024 pixels, white background. A nature spellcaster druid. Robed figure in green and brown woodland attire with an antler or leaf crown. Holding a gnarled wooden staff topped with a glowing green nature sigil. Flowing robes with bark-like texture at the edges. Emerald green eyes. The portrait dissolves into scattered leaves, roots, and nature elements toward the bottom of the image, exactly like the reference images dissolve into scattered pieces. Chunky pixel art style, hard stepped edges, flat colour fills, dark outlines, no anti-aliasing, white background.

---

## IMAGE 2

**Save to:** ~/Documents/RealmOfShadows/assets/sprites/characters/Mystic.png

**Paste this into ChatGPT:**
Pixel art character portrait in the exact same style as the reference images I uploaded, 1024x1024 pixels, white background. An arcane ki master mystic. Lean figure in deep teal and silver robes with geometric arcane patterns. Hands glowing with blue-white ki energy. Eyes with an intense inner light of focused concentration. Combines the appearance of a scholar and a martial artist. The portrait dissolves into floating geometric arcane fragments and energy sparks toward the bottom of the image, exactly like the reference images dissolve into scattered pieces. Chunky pixel art style, hard stepped edges, flat colour fills, dark outlines, no anti-aliasing, white background.

---

## IMAGE 3

**Save to:** ~/Documents/RealmOfShadows/assets/sprites/characters/Shaman.png

**Paste this into ChatGPT:**
Pixel art character portrait in the exact same style as the reference images I uploaded, 1024x1024 pixels, white background. A wilderness spirit-caller shaman. Weathered leather and fur garments with spirit totems hanging from the belt. One hand raised with a faint ghostly animal spirit manifesting above it. Earthy greens, browns, and muted gold colours. Face marked with ritual paint. The portrait dissolves into spirit wisps, feathers, and natural fragments toward the bottom of the image, exactly like the reference images dissolve into scattered pieces. Chunky pixel art style, hard stepped edges, flat colour fills, dark outlines, no anti-aliasing, white background.

---

## AFTER ALL 3 IMAGES ARE SAVED

Run in Terminal to confirm all 3 files exist:
ls ~/Documents/RealmOfShadows/assets/sprites/characters/ | grep -E "Druid|Mystic|Shaman"

Expected output:
Druid.png
Mystic.png
Shaman.png

Then push to git:
cd ~/Documents/RealmOfShadows
git add assets/sprites/characters/
git commit -m "Add missing hybrid class sprites: Druid, Mystic, Shaman"
git push origin main
