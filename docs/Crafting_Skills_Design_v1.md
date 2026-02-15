# REALM OF SHADOWS — Out-of-Combat Skills & Crafting System Design
## Draft v1.0

---

## OVERVIEW

Every class has meaningful activities outside of combat. No one sits idle
while the party explores, rests, or visits town. Skills range from healing
and detection to full crafting systems. Crafting uses a dual progression
where character level sets the ceiling and crafting experience determines
how close you get to that ceiling.

---

## 1. OUT-OF-COMBAT HEALING (Every Class)

Every archetype has a way to help the party recover between fights.
Each uses different flavor and different stats.

```
Fighter type:    Wound Binding
                 Bandaging, field medicine, setting bones.
                 Based on: STR/CON
                 Heals: Moderate HP to one character.
                 Cost: STR-SP + Bandage materials

Thief type:      Wound Binding (Precise)
                 Careful stitching, precise pressure.
                 Based on: DEX
                 Heals: Moderate HP to one character.
                 Cost: DEX-SP + Bandage materials

Ranger type:     Herbal Remedy
                 Applying poultices, natural medicines.
                 Based on: WIS
                 Heals: Moderate HP + can cure Poison.
                 Cost: WIS-MP + Gathered herbs

Cleric type:     Divine Healing
                 Prayer and holy energy.
                 Based on: PIE
                 Heals: Best healing efficiency of all classes.
                 Cost: PIE-MP (no materials needed — divine power)

Monk type:       Ki Healing
                 Hands-on energy transfer, Miyagi-style.
                 Based on: WIS
                 Heals: Good HP + can ease pain (minor status cure).
                 Cost: Ki

Mage type:       Cannot heal directly.
                 Compensates by crafting potions and scrolls 
                 that others can use (see Crafting section).
                 Can use: Arcane Restoration — minor self-heal only,
                 channeling magic to accelerate own natural healing.
                 Cost: INT-MP (self only, less efficient than others)
```

### Resource Recovery Outside Combat
All resource pools regenerate faster outside combat than in combat:
```
Out of combat: +(Relevant Stat ÷ 2) + 5% of max per minute of travel
Resting:       Full restoration after a proper rest period
```

Healing spells cost the same MP whether in or out of combat.
The tradeoff is that out-of-combat MP regeneration is faster,
so the effective cost is lower over time.

---

## 2. DETECTION & AWARENESS SKILLS

### Ranger
```
Track:             Detect nearby enemies before encounter.
                   WIS check. Success = party is warned, may avoid
                   or prepare (set formation, pre-buff).
                   Can reveal enemy count and general type.
                   
Animal Sense:      Detect traps and ambushes in wilderness.
                   Passive WIS check when entering new areas.
                   Higher skill = earlier warning.
                   
Identify Plants:   Recognize useful and dangerous flora.
                   Supports herbalism and foraging.
```

### Thief
```
Detect Traps:      Spot mechanical and some magical traps.
                   INT/DEX check. Best trap detection in game.
                   +25% detection bonus over other classes.
                   
Detect Magic:      Sense magical auras on items, doors, traps.
                   INT check. Identifies enchantments, wards,
                   magical traps.
                   
Appraise:          Estimate value of items and treasure.
                   INT check. Better prices when selling.
                   
Scout Ahead:       Move silently to observe next room/area.
                   DEX check. Reveals enemy positions and count
                   without triggering encounter.
```

### Mage
```
Detect Magic:      Sense and analyze magical auras.
                   INT check. More detailed analysis than Thief —
                   identifies specific spell types, enchantment 
                   levels, and magical trap mechanisms.
                   
Identify:          Reveal full properties of a magic item.
                   INT check + INT-MP cost.
                   Alternative to paying a shopkeeper.
                   
Analyze:           Study an enemy (in or out of combat).
                   +1 bestiary knowledge tier.
                   INT-MP cost.
```

### Cleric
```
Sense Undead:      Detect undead presence nearby.
                   PIE check. Passive when entering areas.
                   
Sense Evil:        Detect evil intent or cursed objects.
                   PIE check. Can warn of ambush by evil creatures
                   or identify cursed items before equipping.

Divine Insight:    Brief flash of guidance.
                   PIE-MP cost. Hints about puzzles, hidden paths,
                   or danger in current area.
```

---

## 3. UTILITY SKILLS

### Mage (Utility Magic)
```
Light:             Illuminate dark areas. INT-MP cost, lasts long.
Knock:             Magically open a locked door/chest. INT-MP cost.
                   Can fail on high-quality locks.
Levitate:          Cross a gap or reach high place. INT-MP cost.
Teleport:          Return to last visited town. High INT-MP cost.
                   High level spell.
Read Languages:    Decipher ancient texts, foreign writing.
```

### Ranger (Travel & Survival)
```
Forage:            Find food and herbs in the wilderness.
                   WIS check. Supplies materials for crafting.
                   Party doesn't need to buy as many supplies.
                   
Navigate:          Prevent getting lost. Faster overworld travel.
                   WIS check. Failed navigation = random encounter.
                   
Mapping:           Automatically maps explored areas.
                   Passive skill. Higher skill = more detail on map.
                   
Set Camp:          Establish a safe rest point in wilderness.
                   Better camp = faster rest recovery, lower 
                   chance of night ambush.
                   
Weather Sense:     Predict weather changes that affect travel.
```

### Thief (Infiltration & Information)
```
Lockpicking:       Open locked doors and chests without magic.
                   DEX check. Quality lockpicks improve chance.
                   
Pickpocket:        Steal from NPCs. Risky — failure has consequences.
                   DEX check.
                   
Disarm Traps:      Disable detected traps safely.
                   DEX check. +30% bonus over other classes.
                   Failure triggers trap.
                   
Gather Info:       Learn rumors and secrets in towns/taverns.
                   INT/DEX check. Can reveal quest hints,
                   enemy weaknesses, hidden locations.
                   
Hide in Shadows:   Avoid detection during exploration.
                   DEX check. Can bypass encounters or 
                   position for ambush.
```

### Fighter (Social & Physical)
```
Intimidate:        Force information from NPCs or scare off 
                   weak enemies before combat.
                   STR check.

Gather Info:       Learn things in taverns through camaraderie.
                   Similar to Thief but different flavor —
                   buying rounds, arm wrestling, soldier talk.
                   STR/CON check.
                   
Force Door:        Break down a stuck or locked door physically.
                   STR check. Loud — may alert enemies.
                   
Appraise Weapons:  Evaluate quality of weapons and armor.
                   Useful at shops and with found loot.
```

### Monk
```
Meditation:        Accelerate rest recovery for entire party.
                   Ki cost. Party recovers faster during rest.
                   
Sense Ki:          Detect living creatures nearby.
                   Passive WIS check. Different from Track —
                   senses life energy, works underground and 
                   in buildings where animal tracking doesn't.
                   
Inner Peace:       Remove Fear and mental status effects 
                   from self or one ally outside combat.
                   Ki cost.
```

### Cleric (Town Services)
```
Cheaper Resurrection: At temples, Cleric reduces cost of
                      resurrection services through religious 
                      connections.
                      
Remove Curse:     Remove permanent status effects (Petrified,
                  Cursed items) at temples with PIE-MP cost.
                  Cheaper than paying temple fees.
                  
Consecrate:       Bless a rest area. Undead cannot ambush
                  party during rest in consecrated area.
                  PIE-MP cost.

Diplomacy:        Better relationships with religious NPCs,
                  access to temple services and quests.
```

---

## 4. TOWN/CITY INTERACTION SKILLS

### Charisma Effects
Note: The game does not have a Charisma stat. Instead, relevant class
skills provide charisma-like effects in specific contexts:

```
Thief Gather Info:      Better info from underworld contacts
Fighter Intimidate:     Better prices through intimidation
Cleric Diplomacy:       Better prices at temples and holy shops
Ranger Herbalism:       Better prices at herbalist shops
Mage Identify:          Save money by identifying items yourself

Ongoing skill/spell:    Certain buffs could improve shop prices
                        (e.g., Mage "Charm" spell, Thief "Silver 
                        Tongue" passive skill)
```

### Tavern Activities
```
Fighter/Thief:    Gather Info (learn rumors, quest hooks, 
                  enemy weaknesses)
All classes:      Rest and recover (faster than camping)
Monk:             Tea house variant — meditation + info
Cleric:           Temple visits — healing, removal, resurrection
```

---

## 5. CRAFTING SYSTEM

### Dual Progression
Character level sets the MAXIMUM tier you can potentially reach.
Crafting skill determines what you ACTUALLY unlock within that cap.

```
Character Level → Maximum Crafting Tier:
  Level 1-4:     Tier 1 (Crude/Rustic)
  Level 5-9:     Tier 2 (Iron)
  Level 10-14:   Tier 3 (Steel)
  Level 15-19:   Tier 4 (Fine Steel)
  Level 20-24:   Tier 5 (Mithril)
  Level 25-29:   Tier 6 (Adamantine)
  Level 30+:     Tier 7 (Legendary)

Crafting Skill → Actual Tier Unlocked (within level cap):
  Novice:        Tier 1
  Apprentice:    Tier 2 (if level allows)
  Journeyman:    Tier 3 (if level allows)
  Expert:        Tier 4 (if level allows)
  Master:        Tier 5 (if level allows)
  Grandmaster:   Tier 6 (if level allows)
  Legendary:     Tier 7 (if level allows)
```

A Level 5 Fighter who has never crafted: Novice skill, can only do Tier 1.
A Level 5 Fighter who has practiced: Apprentice skill, can do Tier 2 (Iron).
A Level 5 Fighter cannot reach Tier 3 regardless of skill — level cap.

### Crafting Skill Advancement
Skill improves through practice:
```
Each successful craft:  +crafting XP
Failed crafts:          +small crafting XP (learn from mistakes)
Higher difficulty:      +more crafting XP
Recipes found/learned:  +crafting XP bonus
```

### Recipe System
Even with skill and level, you need the recipe for specific items.

```
Recipes obtained by:
  Bought:        From blacksmiths, guilds, magic shops, specialists
  Found:         Dungeon loot, enemy drops, treasure chests
  Learned:       NPC teachers, quest rewards, guild advancement
  Discovered:    Experimentation at high crafting skill (rare)
```

### Materials
Crafting requires MP/SP/Ki AND physical materials:
```
Material Sources:
  Enemy drops:     Bone fragments, pelts, fangs, magical essences
  Gathering:       Ranger foraging, mining nodes, herb patches
  Purchased:       Shops sell basic materials
  Salvaged:        Breaking down unwanted equipment
```

---

## 6. CRAFTING BY CLASS

### Fighter — Smithing (Forge required for advanced work)
```
Field crafting:    Basic weapon/armor repair (partial restoration)
                   Sharpen weapons (+1 temporary damage bonus)

Forge crafting:    Forge new weapons and armor from materials
                   Repair damaged equipment to full quality
                   Reinforce armor (+defense bonus)
                   Improve weapon quality (Iron → Steel with recipe)
                   
Cost:              STR-SP + materials + gold (forge rental)
```

### Mage — Alchemy & Scribing (UNIQUE: can craft in the field)
```
Field crafting:    Brew potions (mana, speed, resistance, etc.)
                   Scribe scrolls (one-use versions of known spells)
                   This is the Mage's UNIQUE advantage — no other 
                   class can create consumables outside of town.
                   Cost is lower than buying in town.

Workshop crafting: Enchant weapons (add elemental damage/effects)
                   Enchant armor (add elemental resistance)
                   Create wands and orbs (focus items)
                   Empower existing enchantments (upgrade tier)
                   
Cost:              INT-MP + materials
                   Scrolls also require blank scroll + ink
                   Enchanting requires magical essences
```

### Cleric — Sacred Crafting
```
Field crafting:    Create health scrolls (one-use healing)
                   Create cure scrolls (remove status)
                   Create holy water (throwable, bonus vs undead)
                   Create blessed bandages (improved wound binding)

Temple crafting:   Bless weapons (add Divine damage/effects)
                   Bless armor (add Divine resistance)
                   Create holy symbols (Cleric focus items)
                   Consecrate items (protection from evil/curses)
                   
Cost:              PIE-MP + materials
                   Holy water requires blessed vial + pure water
```

### Thief — Alchemy & Tinkering
```
Field crafting:    Craft poisons (coat weapons for extra effects)
                     Weakening poison (-damage dealt)
                     Slowing poison (-speed)
                     Sleep poison (chance to sleep on hit)
                     Lethal poison (damage over time)
                   Craft lockpicks (varying quality)
                   Craft smoke bombs (blind/escape)
                   
Workshop crafting: Craft traps (set before combat or in dungeons)
                     Caltrops (slow enemies entering area)
                     Snare trap (immobilize one enemy)
                     Poison trap (poison AoE on trigger)
                     Explosive trap (damage AoE)
                   Modify light armor (add hidden pockets, etc.)
                   Craft disguise kits
                   
Cost:              DEX-SP + materials
                   Poisons require plant extracts + vials
```

### Ranger — Woodcraft & Herbalism
```
Field crafting:    Craft arrows and bolts (including specialty)
                     Fire arrows (minor fire damage)
                     Poison arrows (applies poison)
                     Blunt arrows (for stun, non-lethal)
                     Silver arrows (bonus vs undead/werewolves)
                   Herbal remedies (healing + poison cure)
                   Antidotes (cure poison, crafted from herbs)
                   Craft simple traps (larger/cruder than Thief)
                     Bear trap (high damage + immobilize)
                     Pit trap (requires time to prepare)
                     Snare (immobilize, simpler than Thief version)
                   
Workshop crafting: Craft bows and crossbows
                   Craft and repair leather armor
                   Bowstring crafting (different materials for bonuses)
                   
Cost:              WIS-MP + materials
                   Ranger foraging skill helps gather own materials
```

### Monk — Ki Crafting
```
Field crafting:    Ki Stones (stat boost items, equippable by anyone)
                     Stone of Strength (+1 STR)
                     Stone of Agility (+1 DEX)
                     Stone of Endurance (+1 CON)
                     Stone of Insight (+1 INT)
                     Stone of Awareness (+1 WIS)
                     Stone of Spirit (+1 PIE)
                     Greater versions: +2 (higher skill)
                     Supreme versions: +3 (master crafter)
                   Specialized Ki Stones:
                     Stone of Swiftness (+3 Speed)
                     Stone of Fortitude (+10% HP)
                     Stone of the Mind (+10% MP)
                     Stone of Clarity (+5% accuracy)
                     Stone of Warding (+3 Defense)
                   
                   Meditation incense (faster party rest recovery)
                   Healing salves (Ki-based topical healing)
                   Focus beads (temporary accuracy or speed boost)
                   
                   Tea Brewing:
                     Clarity tea (+INT for a period)
                     Vitality tea (+CON for a period)
                     Focus tea (+WIS for a period)
                     Strength tea (+STR for a period)
                     
Field only:        Monk does NOT need a workshop. All crafting is
                   through meditation and Ki channeling. This is the 
                   Monk's crafting advantage — like the Mage with 
                   potions, Monks craft Ki Stones anywhere.

Cost:              Ki + meditation time + materials
                   Ki Stones require gemstones + Ki
                   Teas require herbs + water + Ki
```

### Ki Stone Equipment Rules
```
Ki Stones are equipped in head slots:
  Head Slot 1: Helmet OR Accessory
  Head Slot 2: Accessory only (cannot duplicate Slot 1 item)
  Exception: Ki Stones CAN be in both slots (two different stones)
  
Maximum: 2 Ki Stones per character
Any class can USE Ki Stones, only Monks can CRAFT them
```

---

## 7. MATERIAL TIERS

### Standard Materials
```
Tier 1: Crude/Rustic    Wood, bone, hide, scrap metal
Tier 2: Iron            Iron ore, basic leather, common wood
Tier 3: Steel           Steel alloy, hardened leather, quality wood
Tier 4: Fine Steel      Refined steel, exotic leather, rare wood
Tier 5: Mithril         Mithril ore (light, strong, magical)
Tier 6: Adamantine      Adamantine ore (extremely hard, rare)
Tier 7: Legendary       Unique materials from quests/world bosses
```

### Elemental Materials
Found in specific environments. Carry inherent elemental properties.
Equipment crafted from these has BUILT-IN elemental effects before
any enchanting.

```
Flamesteel:     Fire-infused metal. Found near volcanoes, fire dungeons.
                Built-in: Minor fire damage on weapons, fire resist on armor.

Frostsilver:    Ice-infused metal. Found in frozen caverns, ice peaks.
                Built-in: Minor ice damage, ice resist on armor.

Stormite:       Lightning-infused. Found on high mountains, storm areas.
                Built-in: Minor lightning damage, lightning resist on armor.

Shadowmere:     Shadow-infused. Found in deep underground, shadow realms.
                Built-in: Minor shadow damage, shadow resist on armor.

Solarium:       Divine-infused. Found at holy sites, ancient temples.
                Built-in: Minor divine damage, divine resist on armor.

Livingwood:     Nature-infused. Grown in ancient forests, druid groves.
                Built-in: Minor nature damage, nature resist on armor.
                Special: Weapons slowly regenerate (self-repair).
```

### Stacking: Material + Enchantment + Blessing
A weapon can benefit from all three layers:
```
1. Base material provides inherent properties
2. Mage enchantment adds/amplifies elemental effects
3. Cleric blessing adds Divine properties

Example progression:
  Flamesteel Longsword          (built-in minor fire damage)
  → Mage enchants with fire     (stronger fire + burn chance)
  → Cleric blesses              (adds Divine damage)
  = Blessed Flamesteel Longsword of Inferno
```

### Enchanting Tiers (Mage)
```
Tier 1: Minor      (+1 enhance, basic elemental)
Tier 2: Standard   (+2, moderate elemental + low proc chance)
Tier 3: Greater    (+3, strong elemental + moderate proc)
Tier 4: Superior   (+4, powerful elemental + high proc)
Tier 5: Supreme    (+5, legendary enchantments)
```

### Blessing Tiers (Cleric)
```
Tier 1: Blessed       (minor Divine bonus)
Tier 2: Sanctified    (moderate Divine, minor undead bonus)
Tier 3: Holy          (strong Divine, good undead bonus)
Tier 4: Sacred        (powerful Divine, strong undead bonus)
Tier 5: Exalted       (legendary Divine power)
```

---

## 8. ONGOING VS DIRECT SKILLS/SPELLS

### Direct Use
Activated, resolved immediately, cost taken at time of use.
```
Examples: Heal, Detect Traps, Knock, Identify, Wound Binding
Cost: Taken immediately from resource pool
Recovery: Normal regeneration while traveling or resting
```

### Ongoing Effects
Activated, cost taken at casting, then runs for a duration.
Resource cost is paid once but the effect persists.
```
Examples: 
  Light (illumination lasts until dismissed or duration ends)
  Charm/Silver Tongue (better shop prices for duration)
  Track (awareness of nearby enemies for a period)
  Consecrate (protected rest area until broken)
  
Cost: Taken at activation
Duration: Time-based (minutes of travel/exploration)
Can be dismissed early
Cannot stack same effect
```

---

## 9. FIELD CRAFTING VS TOWN CRAFTING

### Field Crafting Advantages
```
Mage potions/scrolls:    Cheaper than buying in town
Cleric health scrolls:   Available between dungeon floors
Ranger arrows/remedies:  Keep party supplied in wilderness
Monk Ki Stones:          Craft anywhere through meditation
Thief poisons:           Prepare before entering dangerous areas
Fighter repairs:         Partial fix without returning to town
```

### Town/Workshop Advantages
```
Full forge access:       Create new equipment, major repairs
Enchanting workshop:     Full enchantment capabilities
Temple:                  Blessing, resurrection, curse removal
Better materials:        Shops sell higher quality supplies
Recipes available:       Learn new crafting recipes
Guild services:          Advance crafting skill through training
```

### Cost Comparison
```
Field-crafted items:     MP/SP/Ki cost + materials
                         NO gold cost (you're doing the work)
                         Limited by materials on hand
                         
Town-purchased items:    Gold cost only (no resource cost)
                         Higher price than crafting cost
                         Immediately available
                         
Town-crafted items:      Resource cost + materials + gold (facility)
                         Access to higher tier recipes
                         Full quality (no field penalties)
```

---

*End of Out-of-Combat Skills & Crafting System Design — Draft v1.0*
*Connects to: Combat Design, Weapon Design, Elemental Design, Equipment System (future)*
