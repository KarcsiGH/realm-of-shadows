# REALM OF SHADOWS — Combat System Design
## Draft v2.0 (Revised)

### Changes from v1.0:
- Removed Magic Missile auto-hit. Now +15% accuracy bonus instead.
- Revised position modifiers: ranged weapons best from Back, penalized from Front.
- Added physical damage subtypes (Piercing/Slashing/Blunt).
- Added elemental damage types on spells (see Elemental Design doc).
- Revised critical hit system: Precision (DEX/WIS), Power (STR), Ki (WIS).
- Expanded status effects including Petrified, Frozen, Burning, Silenced.
- Added bestiary/enemy knowledge system.
- Added loot system with trapped chests.
- Added requirement for status display on all combatants.
- Ongoing elemental effects (burning, frostbitten) reduce accuracy.
- Potions and status effects are designed to be expandable.
- All formulas are designed to be easily adjustable during playtesting.

---

## 1. SPEED & TURN ORDER

### Speed Stat
```
Speed = (DEX × 2) + (WIS × 0.5) + Level + Equipment Bonus
```

Ties broken by DEX, then random roll.

### Speed Modifiers
- Haste: +50% speed for 2 turns
- Slowed/Frostbitten: -25% to -50% speed
- Stunned/Frozen/Petrified: Speed = 0 (skip turn)
- Burning/Poisoned: No speed effect (but -5% accuracy)
- Heavy armor: Speed penalty (future milestone)

### Turn Structure
1. Calculate speed for all combatants (base + modifiers)
2. Sort highest first
3. Each combatant acts in order
4. End of round: regeneration, status ticks, buff/debuff expiry
5. Next round

---

## 2. ACTIONS

On their turn, a combatant does ONE of:

**Basic Attack** — Melee or ranged physical attack. Free (no resource cost).
**Use Ability** — Cast spell or combat skill. Costs MP/SP/Ki.
**Use Item** — Potion, scroll, bomb. Consumes item.
**Defend** — Skip attack. +50% defense, +25% resistance until next turn. -15% enemy accuracy vs you.
**Move Position** — Shift one step (Front↔Mid↔Back). Costs full action.
**Switch Weapon** — Change equipped weapon. Costs full action.

---

## 3. POSITION SYSTEM (REVISED)

### Three Positions: Front, Mid, Back

**Melee Weapon Position Modifiers:**
```
Front:  100% melee damage
Mid:     85% melee damage
Back:    65% melee damage
```

**Ranged Weapon Position Modifiers:**
```
Back:   100% ranged damage (ideal range, best vantage)
Mid:     95% ranged damage
Front:   70% ranged damage, -15% accuracy (hard to aim in melee)
```

**Spells: 100% from any position. No modifier.**

### Targeting Priority (Enemy Melee AI)
```
Front:  50% targeted       (No Front: Mid 60%, Back 40%)
Mid:    30% targeted       (No Front or Mid: Back 100%)
Back:   20% targeted
```

Enemy ranged/magic: equal chance for all positions.

### Future: Exploration Marching Order
Same positions determine trap triggers, ambush reactions, detection chances.

---

## 4. DAMAGE FORMULAS (REVISED)

### Physical Damage — Melee
```
Stat Damage   = (Weapon Primary Stat × Primary Weight) 
                + (Weapon Secondary Stat × Secondary Weight)
Raw Damage    = Stat Damage + Weapon Base Damage + Enhancement Bonus
Position Mod  = Front 1.0 / Mid 0.85 / Back 0.65
Variance      = random(0.85 to 1.15)
Type Modifier = Enemy resistance to weapon's physical subtype
                (Piercing/Slashing/Blunt)

Physical Result = (Raw × Position × Variance × Type Modifier) - Enemy Defense
Minimum = 1

+ Elemental Damage (if enchanted weapon):
  Elemental Result = Enchantment Power × Enemy Elemental Resistance
  
Total Damage = Physical Result + Elemental Result
```

### Physical Damage — Ranged
```
Stat Damage   = (DEX × Weapon Weight) + (STR × Secondary Weight if bow)
Raw Damage    = Stat Damage + Weapon Base Damage + Enhancement Bonus
Position Mod  = Back 1.0 / Mid 0.95 / Front 0.70
Variance      = random(0.90 to 1.10)
Type Modifier = Enemy resistance to Piercing (most ranged is piercing)

Physical Result = (Raw × Position × Variance × Type Modifier) - Enemy Defense
```

### Magic Damage (REVISED — no auto-hit for any spell)
```
Stat Damage   = (Casting Stat × 1.5) + Focus Item Bonus
Raw Damage    = Stat Damage + Spell Power
Variance      = random(0.90 to 1.10)
Type Modifier = Enemy resistance to spell's elemental type

Magic Result  = (Raw × Variance × Type Modifier) - Enemy Magic Resistance
Minimum = 1
```

### Healing
```
Heal Amount = (PIE × 2.0) + Spell Power + Focus Bonus + random(0 to PIE/2)
```
No resistance reduction. Always applies in full.

---

## 5. ACCURACY SYSTEM (REVISED)

### Physical Accuracy
```
Base:     75%
DEX Mod:  + (Attacker DEX - Defender DEX) × 2%
Weapon:   + Weapon Accuracy Modifier
Enhance:  + Enhancement Bonus to hit
Status:   - 5% if Burning, Poisoned, or Frostbitten
          - 10% if Shocked
          - 30% if Blinded
Minimum:  30%
Maximum:  95%
```

### Ranged Accuracy from Front Row
```
Standard ranged accuracy - 15% (fighting in melee range)
```

### Magic Accuracy (REVISED — applies to ALL spells)
```
Base:     80%
Stat Mod: + (Casting Stat - Defender WIS) × 2%
Spell:    + Spell-specific accuracy modifier
Focus:    + Focus item accuracy bonus
Status:   Same as physical
Minimum:  30%
Maximum:  95%

Magic Missile: +15% accuracy bonus (reliable but NOT auto-hit)
Fireball:      +0% (standard)
Frost Bolt:    +5% (precise targeting)
Lightning Bolt: -5% (wild energy, hard to aim)
```

---

## 6. CRITICAL HIT SYSTEM (REVISED)

### Critical Hit Types

**Precision Critical (DEX or WIS based):**
```
Chance = 5% + (DEX / 8)%
Used by: Thieves, Rangers, Monks (finding gaps, vital spots)
Multiplier: 2.0x for Thieves/Assassins, 1.5x for others
Weapons: Daggers, bows get +3% crit chance
```

**Power Critical (STR based):**
```
Chance = 5% + (STR / 10)%
Used by: Fighters (overwhelming force, breaking defenses)
Multiplier: 1.5x but partially ignores armor (reduce Defense by 50% on crit)
Weapons: Broadswords, maces get +2% crit chance
```

**Ki Critical (WIS based):**
```
Chance = 5% + (WIS / 8)%
Used by: Monks (channeling energy into perfect strike)
Multiplier: 1.75x
Applies to: Ki abilities only
```

**Spell Critical (Casting Stat based):**
```
Chance = 5% + (Casting Stat / 10)%
Multiplier: 1.5x damage
```

**Heal Critical:**
```
Chance = 5% + (PIE / 10)%
Multiplier: 1.5x healing
```

---

## 7. DEFENSE & RESISTANCE

### Physical Defense
```
Defense = (CON × 0.5) + Armor Value + Shield Value + Buffs
```

### Magic Resistance
```
Magic Resistance = (WIS × 0.5) + Equipment Bonus + Buffs
```

### Armor System (to be expanded in equipment milestone)
```
Clothing:       Defense +1 to +3    (Mage, Thief)
Light Armor:    Defense +4 to +8    (Thief, Ranger, Monk)
Medium Armor:   Defense +8 to +14   (Ranger, Cleric, Fighter)
Heavy Armor:    Defense +14 to +22  (Fighter, Cleric)
                Speed penalty: -2 to -5
Shields:        Defense +2 to +8    (Fighter, Cleric)
```

Class armor proficiencies (non-proficient = penalty):
```
Fighter:  All armor, all shields
Cleric:   Up to heavy armor, shields
Ranger:   Up to medium armor, no shields (needs hands for bow)
Thief:    Up to light armor, no shields (needs mobility)
Monk:     Clothing only, no shields (armor disrupts Ki)
Mage:     Clothing only, no shields (armor disrupts spellcasting)
```

### Defend Action Bonus
- Physical Defense × 1.5 until next turn
- Magic Resistance × 1.25 until next turn
- Enemies have -15% accuracy against defending character

---

## 8. RESOURCE REGENERATION IN COMBAT

Applied at end of each round:
```
Per turn: +(Relevant Stat ÷ 4) + 3% of max resource

STR-SP: based on STR
DEX-SP: based on DEX
INT-MP: based on INT
WIS-MP: based on WIS
PIE-MP: based on PIE
Ki:     based on WIS (Monk gets 25% bonus: 3.75% of max)

HP does NOT regenerate in combat (only via healing spells/potions)
```

---

## 9. POTION SYSTEM (EXPANDABLE)

### Diminishing Returns
```
1st use: 100% effectiveness
2nd use:  75%
3rd use:  56%
4th use:  42%
5th use:  32%
```
Resets between combats.

### Starter Potions
```
Minor Health Potion:    +30 HP     (20 gold)
Minor Mana Potion:      +25 MP     (20 gold)
Minor Stamina Potion:   +20 SP     (20 gold)
Minor Ki Potion:        +20 Ki     (25 gold)
```

### Future Potions (add as needed — system supports unlimited types)
```
Health Potion:          +60 HP
Greater Health Potion:  +120 HP
Antidote:               Removes Poisoned status
Thawing Draught:        Removes Frozen/Frostbitten
Burn Salve:             Removes Burning
Stone Salve:            Removes Petrified
Speed Potion:           +25% speed for 3 turns
Strength Elixir:        +20% physical damage for 3 turns
Mage's Focus:           +15% spell damage for 3 turns
Fire Resistance Potion: -50% fire damage for 4 turns
Ice Resistance Potion:  -50% ice damage for 4 turns
Invisibility Potion:    Invisible for 2 turns (Thief-like)
```

All potions use the same diminishing returns system.
Adding new potions requires only adding a data entry — no code changes.

---

## 10. STATUS EFFECTS (EXPANDABLE)

See Elemental & Enchantment Design doc for full list.
System is designed so new status effects can be added as data entries.

Key design rule: any status that prevents action (Stun, Frozen, Petrified)
sets Speed to 0 and skips the affected combatant's turn.

Any status that causes ongoing damage or distraction (Burning, Frostbitten,
Poisoned) applies -5% accuracy to represent the distraction.

---

## 11. DEATH & DEFEAT

### Character at 0 HP
- Falls **unconscious** (not dead)
- Cannot act, cannot be targeted by most attacks
- Revivable by healing spell (restores with healed amount as HP)
- If not healed by end of combat: revives with 1 HP

### Total Party Defeat
- Game Over screen with options:
  - Retry the battle (fresh encounter)
  - Return to last town (lose some gold, keep XP)
  - Load last save (future milestone)

### Enemy Death
- Removed from combat at 0 HP
- Generates loot (see Loot System in Elemental Design doc)
- Grants XP after combat ends

---

## 12. COMBAT UI REQUIREMENTS

### Must Display:
```
Party Side:
  - Character portrait/sprite
  - Name, class
  - HP bar with numbers
  - Active status effects with icons and remaining duration
  - Active buffs with icons and remaining duration  
  - Position indicator [F] [M] [B]
  - Current equipped weapon

Enemy Side:
  - Enemy portrait/sprite
  - Name (or description if Tier 0 knowledge)
  - HP bar (hidden at Tier 0, visible at Tier 1+)
  - Active status effects (visible once applied)
  - Knowledge tier indicator

Top:
  - Turn order bar showing upcoming actions

Bottom:
  - Action menu (when party member's turn)
  - Combat log showing recent events
```

### Portraits / Sprites
- Each class gets a distinct character sprite
- Each enemy type gets a distinct sprite
- Style: Retro pixel art (Wizardry/Phantasy Star inspired)
- Sprites shown alongside health bars, not just text lists

---

## 13. ENEMY DESIGN (Starter Roster)

### Starter Enemies for Milestone 2

#### GOBLIN
```
HP: 25  Speed: 14  Defense: 2  Magic Resist: 1
Attack: 8 melee (Slashing - crude sword)  DEX: 12  WIS: 6
AI: Random
Resistances: None special
XP: 15  Gold: 5-10
Loot: Rusty Knife (common), Goblin Ear (crafting, common)
Groups: 2-4
```

#### BANDIT
```
HP: 45  Speed: 12  Defense: 5  Magic Resist: 2
Attack: 14 melee (Slashing)  DEX: 11  WIS: 8
AI: Aggressive (targets highest damage dealer)
Resistances: None special
XP: 30  Gold: 10-25
Loot: Worn Short Sword (uncommon), Leather Scraps (common)
Special: Power Strike (occasional, +50% damage, -10% accuracy)
Groups: 2-3, sometimes with Bandit Archer
```

#### WOLF
```
HP: 30  Speed: 20  Defense: 3  Magic Resist: 2
Attack: 12 melee (Piercing - bite)  DEX: 16  WIS: 10
AI: Defensive (targets lowest HP)
Resistances: None special
XP: 25  Gold: 0-5
Loot: Wolf Pelt (common), Wolf Fang (uncommon)
Special: Pack Tactics (+10% damage per other wolf alive)
Groups: 3-5
```

#### SKELETON WARRIOR
```
HP: 40  Speed: 8  Defense: 10  Magic Resist: 3
Attack: 16 melee (Slashing)  DEX: 8  WIS: 5
AI: Random
Resistances: Piercing 50%, Slashing 50%, Blunt 150%,
             Divine 200%, Shadow Immune, Ice 50%
XP: 35  Gold: 15-30
Loot: Rusted Chainmail (uncommon), Bone Fragments (common),
      Worn Longsword (uncommon)
Groups: 2-3, sometimes with Skeleton Mage
```

#### ORC CHIEFTAIN (Mini-Boss)
```
HP: 120  Speed: 10  Defense: 8  Magic Resist: 5
Attack: 22 melee (Slashing - great axe)  DEX: 10  WIS: 9
AI: Tactical (targets healers, then mages)
Resistances: None special
XP: 100  Gold: 50-80
Loot: Orc War Axe (rare), Heavy Shield (uncommon),
      Iron Helm (uncommon), chance of Iron Chest
Special: War Cry (buffs allies +25% damage, 2 turns, once per fight),
         Cleave (hits 2 front-row characters)
Groups: Solo or with 2 Goblins
```

---

## 14. DESIGN PRINCIPLES FOR EXPANDABILITY

### Easy to Tune
All formulas live in centralized config files. Changing a multiplier
is a one-line edit. A debug/tuning mode will show all math in real-time.

### Easy to Expand
Enemies, potions, status effects, weapons, and spells are all data-driven.
Adding a new one means adding a data entry, not rewriting code.

### Easy to Balance
Playtesting mode will show: damage dealt, accuracy rolls, resource
spending, and turn-by-turn combat flow. Can adjust any number and
immediately see the impact.

---

*End of Combat System Design — Draft v2.0*
