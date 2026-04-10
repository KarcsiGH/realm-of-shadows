# SESSION 5: Job Board Interior Backgrounds (4 images)

## HOW TO DO THIS JOB

You will generate 4 images using ChatGPT's image generation. Follow these steps for EVERY image:

**STEP 1:** Open ChatGPT in the browser at https://chatgpt.com
**STEP 2:** Start a new conversation
**STEP 3:** Paste the image prompt provided below
**STEP 4:** Wait for ChatGPT to generate the image
**STEP 5:** Download the image using the download button
**STEP 6:** Move and rename the downloaded file to the exact path shown
**STEP 7:** Confirm the file exists at the correct path before moving to the next image

Do NOT use Python to draw images. Do NOT use PIL or any drawing library.
Use ChatGPT image generation ONLY.
Do each image one at a time.

All images: 864 x 900 pixels (tall/portrait). Put the most interesting detail in the RIGHT HALF.

---

## IMAGE 1

**Save to:** ~/Documents/RealmOfShadows/assets/backgrounds/buildings/briarhollow_jobboard.png

**Paste this into ChatGPT:**
Pixel art interior background for a dark fantasy RPG game, 864x900 pixels, portrait orientation. A village administrative room. The centrepiece is a large corkboard notice board packed with paper slips in various colours and sizes — overlapping notices for jobs, bounties, and community postings, illegible but clearly very busy. A wooden counter with an open logbook. A guard post window behind with a guard silhouette visible through it. Warm amber lantern light. Chunky pixel art style, hard stepped edges, flat colour fills, dark outlines, no anti-aliasing. Functional and slightly chaotic village administration.

---

## IMAGE 2

**Save to:** ~/Documents/RealmOfShadows/assets/backgrounds/buildings/woodhaven_jobboard.png

**Paste this into ChatGPT:**
Pixel art interior background for a dark fantasy RPG game, 864x900 pixels, portrait orientation. A small village administrative room. Through a window on the right a carved wooden post is visible as the village notice board with notices and papers tied with twine hanging from it. Inside the room: a village elder's desk covered in hand-drawn local maps. A wooden chair. A small carved animal figure on the desk. Warm wood interior with filtered light. Chunky pixel art style, hard stepped edges, flat colour fills, dark outlines, no anti-aliasing. Homemade community administration atmosphere.

---

## IMAGE 3

**Save to:** ~/Documents/RealmOfShadows/assets/backgrounds/buildings/crystalspire_jobboard.png

**Paste this into ChatGPT:**
Pixel art interior background for a dark fantasy RPG game, 864x900 pixels, portrait orientation. An academy commission hall. A large slate board on the right wall with commissions inscribed in glowing blue arcane script — abstract glowing blue text patterns, clearly organised and precise. An administrative counter with a serious functionary silhouette behind it. Student silhouettes examining the board on the right. Benches for waiting on the left. Cold blue ambient lighting. Chunky pixel art style, hard stepped edges, flat colour fills, dark outlines, no anti-aliasing. Formal and academic atmosphere.

---

## IMAGE 4

**Save to:** ~/Documents/RealmOfShadows/assets/backgrounds/buildings/thornhaven_jobboard.png

**Paste this into ChatGPT:**
Pixel art interior background for a dark fantasy RPG game, 864x900 pixels, portrait orientation. An imperial government contracts office. Dark wood panelling on all walls. Numbered service windows along the right wall with official plaque signs above each one. Imperial seal insignia throughout. Formal notice boards with stamped official documents. Queue management rope system in the foreground. Maps on the left wall. A clerk silhouette at the nearest service window. Chunky pixel art style, hard stepped edges, flat colour fills, dark outlines, no anti-aliasing. Bureaucratic and imposing atmosphere.

---

## AFTER ALL 4 IMAGES ARE SAVED

Run in Terminal to confirm all 4 job board images exist:
ls ~/Documents/RealmOfShadows/assets/backgrounds/buildings/ | grep "_jobboard"

Then confirm the TOTAL building count is correct (should be 44 total):
ls ~/Documents/RealmOfShadows/assets/backgrounds/buildings/ | wc -l

Then push to git:
cd ~/Documents/RealmOfShadows
git add assets/backgrounds/buildings/
git commit -m "Session 5: 4 job board interior backgrounds, ChatGPT pixel art"
git push origin main
