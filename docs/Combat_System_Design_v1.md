# REALM OF SHADOWS — Combat System Design
## Draft v1.0

---

## OVERVIEW

Turn-based party combat. 6 party members vs. a group of enemies.
Each round, every combatant acts once in speed order.
Combat ends when all enemies are defeated or all party members fall.

---

## 1. SPEED & TURN ORDER

### Speed Stat
Every combatant has a **Speed** value that determines turn order.
Highest speed acts first each round.

**Base Speed Formula:**
```
Speed = (DEX × 2) + (WIS × 0.5) + Level + Equipment Bonus
```

DEX is the primary driver, with a small WIS contribution (awareness/reaction).
Level gives a small natural improvement over time.
Equipment (boots, rings, etc.) can modify speed in future milestones.

**Ties:** Broken by DEX, then by random roll.

### Speed Modifiers
Speed can be temporarily changed by:
- **Spells/Abilities:** Haste (+50% speed), Slow (-50% speed)
- **Potions:** Speed Potion (+25% speed for 3 turns)
- **Status Effects:** Stunned (skip turn), Paralyzed (speed = 0)
- **Encumbrance:** Heavy armor reduces speed (future milestone)

### Turn Structure
Each round:
1. Calculate speed for all combatants (base + modifiers)
2. Sort by speed, highest first
3. Each combatant takes one action in order
4. After all have acted, the round ends
5. Apply end-of-round effects (regeneration, poison ticks, buff expiry)
6. Next round begins

---

## 2. ACTIONS

On their turn, a combatant can do ONE of:

### Basic Attack
- Melee or ranged physical attack (based on equipped weapon)
- Costs nothing — always available
- Damage formula below

### Use Ability
- Cast a spell or use a combat skill
- Costs resources (STR-SP, DEX-SP, INT-MP, WIS-MP, PIE-MP, or Ki)
- Must have the ability equipped (within slot limit)

### Use Item
- Drink a potion, use a scroll, throw a bomb
- Consumes the item
- Potion diminishing returns apply (per design doc: 25% reduction per use in same battle)

### Defend
- Skip attack, gain +50% defense until next turn
- Also grants +25% to all resistance
- Good for: low-resource situations, waiting for healer, protecting weakened character

### Move Position
- Change position (Front ↔ Mid ↔ Back)
- Can only move one step per turn (Front→Mid or Mid→Back, not Front→Back)
- Takes your full action — no attack this turn
- Useful for: retreating a wounded frontliner, moving a melee fighter forward

---

## 3. POSITION SYSTEM

### Three Positions: Front, Mid, Back

**Default party formation (set before combat):**
- Players assign each of their 6 characters to Front, Mid, or Back
- Can be changed between combats freely
- During combat, changing position costs your action

### Targeting Priority (Enemy AI)
When an enemy chooses who to attack with melee:
```
Front:  50% chance of being targeted
Mid:    30% chance of being targeted
Back:   20% chance of being targeted
```

For ranged/magic enemy attacks: equal chance for all positions.

If a position is empty (e.g., all Front characters are down), redistribute:
```
No Front: Mid becomes 60%, Back becomes 40%
No Front or Mid: Back becomes 100%
```

### Melee Effectiveness by Position
Characters attacking with melee weapons/abilities:
```
Front:  100% melee damage
Mid:     85% melee damage
Back:    65% melee damage
```

Ranged attacks and spells: **100% from any position.**

### Future: Exploration Marching Order
Same Front/Mid/Back positions will determine:
- Trap triggers (Front takes full, Mid partial, Back avoids)
- Ambush reactions (Back gets free turn)
- Detection chances (position + relevant stat)
(Implementation in a later milestone)

---

## 4. DAMAGE FORMULAS

### Physical Damage (Melee)
```
Raw Damage = (STR × 1.5) + Weapon Damage + Ability Bonus
Position Modifier = 1.0 (Front), 0.85 (Mid), 0.65 (Back)
Damage Variance = Raw × random(0.85 to 1.15)

Final Damage = (Raw Damage × Position Modifier × Variance) - Enemy Defense
Minimum damage = 1 (attacks always do at least 1)
```

### Physical Damage (Ranged)
```
Raw Damage = (DEX × 1.5) + Weapon Damage + Ability Bonus
No position modifier (full damage from any position)
Damage Variance = Raw × random(0.90 to 1.10)  [more consistent]

Final Damage = (Raw Damage × Variance) - Enemy Defense
Minimum damage = 1
```

### Finesse Damage (Thief/Assassin)
```
Raw Damage = (DEX × 1.5) + Weapon Damage + Ability Bonus
Position Modifier = same as melee
Critical Chance = 10% + (DEX / 4)%
Critical Multiplier = 2.0x

Final Damage = (Raw × Position × Variance) - Enemy Defense
If critical: Final Damage × 2.0
```

### Magic Damage
```
Raw Damage = (Casting Stat × 2.0) + Spell Power
Casting Stat = INT (arcane), WIS (nature), PIE (divine)
No position modifier
Damage Variance = Raw × random(0.90 to 1.10)

Final Damage = (Raw Damage × Variance) - Enemy Magic Resistance
Minimum damage = 1
```

### Ki Ability Damage
```
Raw Damage = (Primary Class Stat × 1.5) + (Ki Spent × 0.5)
No position modifier for ranged Ki abilities
Melee Ki abilities use position modifier

Final Damage = (Raw Damage × Variance) - relevant enemy defense
```

### Healing
```
Heal Amount = (PIE × 2.0) + Spell Power + random(0 to PIE/2)
```

No defense reduction. Healing always applies in full.

---

## 5. TO-HIT / ACCURACY SYSTEM

Every attack (physical and magical) must pass an accuracy check.

### Physical Accuracy
```
Hit Chance = 75% + (Attacker DEX - Defender DEX) × 2%
```

- Base 75% chance to hit
- Each point of DEX advantage adds 2%
- Each point of DEX disadvantage subtracts 2%
- Minimum hit chance: 30% (even clumsy attacks can land)
- Maximum hit chance: 95% (always a small chance to miss)

**Example:**
Attacker DEX 14 vs. Defender DEX 10:
= 75% + (14 - 10) × 2% = 75% + 8% = 83% hit chance

### Magic Accuracy
```
Hit Chance = 80% + (Attacker Casting Stat - Defender WIS) × 2%
```

- Base 80% (magic is more reliable than swords)
- Defender's WIS represents magical awareness/resistance
- Same min 30% / max 95% bounds

### Ability Accuracy Modifiers
Some abilities modify accuracy:
- Aimed Shot (Ranger): +15% accuracy
- Quick Strike (Thief): -5% accuracy, but acts earlier in turn
- Magic Missile (Mage): auto-hit (ignores accuracy roll)
- Power Strike (Fighter): -10% accuracy, but +50% damage

### Defending Bonus
Characters who chose "Defend" last turn:
- Enemy attacks against them suffer -15% accuracy
- Stacks with DEX advantage

### Evasion (Passive)
Some classes gain passive evasion:
- Monk: +5% base evasion (enemies have -5% hit chance against them)
- Thief: +3% base evasion
- Increases with level (future milestone)

---

## 6. DEFENSE & RESISTANCE

### Physical Defense
```
Defense = (CON × 0.5) + Armor Value + Shield Value + Buff Bonuses
```
Reduces physical damage taken (subtracted from final damage).

### Magic Resistance
```
Magic Resistance = (WIS × 0.5) + Equipment Bonus + Buff Bonuses
```
Reduces magic damage taken.

### Defend Action Bonus
When a character uses the Defend action:
- Physical Defense × 1.5 until their next turn
- Magic Resistance × 1.25 until their next turn

---

## 7. CRITICAL HITS

### Critical Chance
```
Base Critical Chance = 5%
DEX Bonus = +(DEX / 10)%   (e.g., DEX 16 = +1.6%)
Ability Bonus = varies (some abilities have higher crit chance)
```

### Critical Damage
```
Critical Multiplier = 1.5x for most classes
Thief/Assassin Multiplier = 2.0x
```

### Critical Heals
Healing spells can also crit:
```
Crit Chance = 5% + (PIE / 10)%
Crit Heal = 1.5x healing
```

---

## 8. RESOURCE REGENERATION IN COMBAT

From the design doc, applied at end of each round:

### Standard Classes
```
Per turn: +(Relevant Stat ÷ 4) + 3% of max resource
```

Each resource regenerates independently:
- STR-SP regenerates based on STR
- DEX-SP regenerates based on DEX
- INT-MP regenerates based on INT
- WIS-MP regenerates based on WIS
- PIE-MP regenerates based on PIE
- Ki regenerates based on WIS (for all classes)
- HP does NOT regenerate in combat (only via healing spells/potions)

### Monk Special
```
Ki per turn: +(WIS ÷ 4) + 3.75% of max Ki (25% bonus)
```

### Example
Level 5 Mage (INT 16, max INT-MP 130):
```
Per turn: (16 ÷ 4) + (130 × 0.03) = 4 + 3.9 = ~8 INT-MP recovered
```

---

## 9. POTION SYSTEM IN COMBAT

From the design doc:

### Diminishing Returns
```
1st potion: 100% effectiveness
2nd potion:  75% effectiveness
3rd potion:  56% effectiveness
4th potion:  42% effectiveness
5th potion:  32% effectiveness
```

Each subsequent potion is 75% as effective as the previous.
Counter resets between combats.

### Potion Types (Starter Set)
```
Minor Health Potion:  +30 HP base     (20 gold)
Minor Mana Potion:    +25 MP base     (20 gold)
Minor Stamina Potion: +20 SP base     (20 gold)
Minor Ki Potion:      +20 Ki base     (25 gold)
```

Using a potion consumes the character's turn.

---

## 10. STATUS EFFECTS

### Negative Status Effects
```
Poisoned:    -5% max HP per turn for 3 turns
Stunned:     Skip next turn (1 turn duration)
Slowed:      -50% Speed for 2 turns
Weakened:    -25% damage dealt for 3 turns
Blinded:     -30% accuracy for 2 turns
```

### Positive Status Effects (Buffs)
```
Shielded:    +25% defense for 3 turns
Hasted:      +50% speed for 2 turns
Blessed:     +15% accuracy and +10% damage for 3 turns
Regenerating: +5% max HP per turn for 3 turns
```

### Applying Status Effects
Some abilities inflict status effects:
- Stunning Strike (Monk): chance to Stun
- Poison Strike (Assassin): applies Poisoned
- Smite (Cleric): chance to Weaken undead
- Slow (Mage): applies Slowed

Hit chance for status effects:
```
Status Chance = Ability Base Chance + (Attacker Stat - Defender Stat) × 2%
```

---

## 11. DEATH & DEFEAT

### Character at 0 HP
- Falls **unconscious** (not dead)
- Cannot act, cannot be targeted by most abilities
- Can be revived in combat by healing (Heal spell restores them with healed amount as HP)
- If not healed by end of combat: revives with 1 HP after combat

### Total Party Defeat
- If all 6 party members fall unconscious in combat:
- **Game Over screen** with options:
  - Retry the battle (start the same encounter fresh)
  - Return to last town (lose some gold as penalty, keep XP)
  - Load last save (future milestone)

### Enemy Death
- Enemies at 0 HP are dead and removed from combat
- Drop loot and grant XP after combat ends

---

## 12. ENEMY DESIGN (Starter Roster)

### Enemy Stats
Each enemy has:
- HP, Speed, Physical Defense, Magic Resistance
- Attack Damage (and type: melee or ranged)
- DEX (for accuracy calculations)
- WIS (for magic defense calculations)
- Special abilities (if any)
- AI behavior type
- XP reward, Gold reward, Loot table

### AI Behavior Types
```
Aggressive:  Attacks highest-damage party member
Defensive:   Attacks weakest (lowest HP) party member
Random:      Attacks random party member (weighted by position)
Tactical:    Prioritizes healers and mages (back row)
Cowardly:    Flees when below 25% HP
```

### Starter Enemies

#### GOBLIN (Weak Mob)
```
HP: 25    Speed: 14    Defense: 2    Magic Resist: 1
Attack: 8 melee    DEX: 12    WIS: 6
AI: Random
XP: 15    Gold: 5-10
Special: None
Appears: Groups of 2-4
```
Fodder enemy. Low stats, low threat. Good for learning combat.

#### BANDIT (Standard Melee)
```
HP: 45    Speed: 12    Defense: 5    Magic Resist: 2
Attack: 14 melee    DEX: 11    WIS: 8
AI: Aggressive
XP: 30    Gold: 10-25
Special: Power Strike (uses occasionally, +50% damage, -10% accuracy)
Appears: Groups of 2-3
```
Bread-and-butter enemy. Decent damage, targets your strongest.

#### WOLF (Fast Attacker)
```
HP: 30    Speed: 20    Defense: 3    Magic Resist: 2
Attack: 12 melee    DEX: 16    WIS: 10
AI: Defensive (targets weakest)
XP: 25    Gold: 0-5
Special: Pack Tactics (+10% damage per other wolf alive)
Appears: Groups of 3-5
```
Fast and targets your weak characters. Dangerous in packs.

#### SKELETON WARRIOR (Armored)
```
HP: 40    Speed: 8    Defense: 10    Magic Resist: 3
Attack: 16 melee    DEX: 8    WIS: 5
AI: Random
XP: 35    Gold: 15-30
Special: Resistant to physical (-25% physical damage), Weak to divine (+50% PIE-MP damage)
Appears: Groups of 2-3
```
Slow but tough. Encourages using magic and Cleric abilities.

#### ORC CHIEFTAIN (Mini-Boss)
```
HP: 120   Speed: 10   Defense: 8    Magic Resist: 5
Attack: 22 melee    DEX: 10   WIS: 9
AI: Tactical (targets healers)
XP: 100   Gold: 50-80
Special: War Cry (buffs all other enemies +25% damage for 2 turns, uses once),
         Cleave (hits 2 front-row characters at once)
Appears: Solo or with 2 Goblins
```
First real challenge. High HP, dangerous abilities, smart targeting.

---

## 13. ENCOUNTER STRUCTURE

### Pre-Combat
1. Show enemy group with names and count
2. Player can rearrange party position (Front/Mid/Back)
3. "Fight!" button to begin

### Combat Loop
1. Calculate all speeds
2. Display turn order bar at top of screen
3. Current actor highlighted
4. If party member: show action menu (Attack, Ability, Item, Defend, Move)
5. If enemy: AI selects action, brief animation/text
6. Apply damage/effects
7. Check for deaths
8. Next actor
9. After all have acted: end-of-round (regeneration, status ticks, buff expiry)
10. Check for victory/defeat
11. Next round

### Post-Combat
1. "Victory!" screen
2. Show XP gained per character
3. Show gold found
4. Show any items dropped
5. All characters restore to proportional resources (out-of-combat regen kicks in)

---

## 14. COMBAT UI LAYOUT (Pygame)

```
┌─────────────────────────────────────────────────┐
│  Turn Order Bar: [Gareth] [Wolf] [Lyra] [Wolf]  │
│                                                   │
│  ┌─────────────────┐  ┌─────────────────────┐   │
│  │                  │  │                      │   │
│  │   ENEMY SIDE     │  │   PARTY SIDE         │   │
│  │                  │  │                      │   │
│  │  Goblin  25/25   │  │  [F] Gareth  128/128 │   │
│  │  Goblin  25/25   │  │  [F] Marcus  158/158 │   │
│  │  Bandit  45/45   │  │  [M] Lyra    103/103 │   │
│  │                  │  │  [M] Bran    118/118 │   │
│  │                  │  │  [B] Sera     83/83  │   │
│  │                  │  │  [B] Kael     73/73  │   │
│  └─────────────────┘  └─────────────────────┘   │
│                                                   │
│  ┌──────────────────────────────────────────────┐│
│  │  ACTION MENU (when party member's turn)      ││
│  │  [Attack]  [Ability]  [Item]  [Defend] [Move]││
│  │                                               ││
│  │  Combat Log:                                  ││
│  │  > Gareth attacks Goblin for 14 damage!       ││
│  │  > Wolf bites Lyra for 8 damage!              ││
│  └──────────────────────────────────────────────┘│
└─────────────────────────────────────────────────┘
```

---

## 15. IMPLEMENTATION PRIORITY

For Milestone 2 (first combat build):
```
Must Have:
  ✓ Speed-based turn order
  ✓ Basic Attack action with to-hit rolls
  ✓ Physical damage formula with position modifiers
  ✓ Defend action
  ✓ HP tracking and unconscious state
  ✓ Enemy AI (Random and Aggressive)
  ✓ 2-3 enemy types (Goblin, Bandit, Wolf)
  ✓ Victory/defeat conditions
  ✓ Combat log showing what happened
  ✓ End-of-round resource regeneration

Nice to Have:
  - Use Ability action (1-2 abilities per class)
  - Use Item action (health potions with diminishing returns)
  - Status effects (Stunned from Monk, basic Poison)
  - Move Position action
  - Orc Chieftain mini-boss

Future Milestones:
  - Full ability system with all class spells
  - All status effects
  - Equipment affecting combat stats
  - Enemy loot drops
  - XP and leveling
  - Advanced enemy AI (Tactical, Cowardly)
```

---

*End of Combat Design Document — Draft v1.0*
*Ready for review and revision before implementation*
