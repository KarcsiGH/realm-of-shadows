# REALM OF SHADOWS — Combat System Design
## Draft v3.0

### Changes from v2.0:
- Complete position-to-position modifier system for melee, ranged, thrown, reach
- Crossbows get slight edge at extreme positions
- Enemy grouping system: 3 rows, 2 groups per row, multiple enemies per group
- Single-target attacks pick a group, overflow damage lost (can only kill one per hit)
- Four spell targeting scopes: Individual → Group → Row → All
- Healing/buff spells: Individual or All Party only
- Status spells follow same progression as damage spells
- Cleric restricted to Divine damage only
- Ranger utility-focused spells only (Druid gets full Nature offense)
- Party limited to 6 characters plus summoned/conjured creatures
- All formulas designed for easy tuning during playtesting

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

## 3. BATTLEFIELD LAYOUT

### Structure
```
[Player Back] [Player Mid] [Player Front] ←→ [Enemy Front] [Enemy Mid] [Enemy Back]
```

Each side has three rows. Each row can hold up to **two groups**.
A group is one or more combatants of the same type.

### Player Side
Maximum 6 player characters plus any summoned/conjured creatures.
Each row can hold two groups.
```
Example:
  Player Front:  [2 Fighters]  [1 Monk]
  Player Mid:    [1 Ranger]    [1 Thief]
  Player Back:   [1 Mage]      [1 Cleric]
```

### Enemy Side
Enemies organized in three rows with two groups per row maximum.
No fixed limit on number of enemies per group.
Larger enemies take more space (future: slot system per row).
```
Example:
  Enemy Front:   [4 Goblin Warriors]  [2 Orc Fighters]
  Enemy Mid:     [3 Goblin Archers]
  Enemy Back:    [1 Goblin Shaman]    [1 Orc Mage]
```

---

## 4. POSITION-TO-POSITION COMBAT MODIFIERS

The effectiveness of every attack depends on BOTH the attacker's position
and the defender's position. Listed from best to worst for each weapon type.

### Standard Melee (swords, daggers, maces, fists)
Based on distance — closer is better for melee.
```
Attacker → Target    | Damage Mod | Accuracy Mod | Notes
Front → Front        |   100%     |    +0%       | Closest distance, ideal
Front → Mid          |    90%     |    -5%       | Reaching past front line
Mid → Front          |    85%     |    -5%       | Stepping forward to strike
Mid → Mid            |    80%     |   -10%       | Moderate distance
Back → Front         |    70%     |   -15%       | Far from action
Mid → Back           |    65%     |   -15%       | Reaching deep
Back → Mid           |    55%     |   -20%       | Very far
Back → Back          |    40%     |   -25%       | Nearly impossible
```

### Reach Melee (polearms, halberds, spears)
Longer weapons excel at mid-range, awkward up close.
```
Attacker → Target    | Damage Mod | Accuracy Mod | Notes
Mid → Front          |   100%     |    +5%       | Ideal reach distance
Mid → Mid            |    95%     |    +0%       | Good leverage
Front → Front        |    85%     |    -5%       | Crowded for long weapon
Front → Mid          |    90%     |    +0%       | Decent reach
Mid → Back           |    80%     |    -5%       | Extended reach
Back → Front         |    75%     |   -10%       | Far but weapon helps
Front → Back         |    70%     |   -10%       | Overextended
Back → Mid           |    60%     |   -15%       | Too far even with reach
Back → Back          |    45%     |   -20%       | Extreme distance
```

### Ranged (bows, crossbows, slings)
Need distance to aim — too close or too far is bad.
```
Attacker → Target    | Damage Mod | Accuracy Mod | Notes
Mid → Front          |   100%     |    +5%       | Perfect range, clear target
Mid → Mid            |    95%     |    +0%       | Solid distance
Back → Front         |    95%     |    +0%       | Far but clear sight line
Mid → Back           |    85%     |    -5%       | Shooting past their line
Back → Mid           |    85%     |    -5%       | Getting far
Front → Mid          |    75%     |   -10%       | Crowded by melee
Front → Back         |    70%     |   -10%       | Crowded AND target far
Back → Back          |    70%     |   -15%       | Very far, hard to reach
Front → Front        |    60%     |   -20%       | Can't aim, too close
```

**Crossbow Exception:** At the extreme positions (Front→Front and Back→Back),
crossbows suffer less penalty than bows/slings due to mechanical nature:
```
Crossbow Front → Front:  70% damage, -15% accuracy (vs 60%/-20% for bows)
Crossbow Back → Back:    75% damage, -10% accuracy (vs 70%/-15% for bows)
```

### Thrown Weapons (knives, axes, javelins)
Short-range projectiles — closer is better.
```
Attacker → Target    | Damage Mod | Accuracy Mod | Notes
Front → Front        |   100%     |    +5%       | Close range, easy toss
Front → Mid          |    95%     |    +0%       | Short throw
Mid → Front          |    90%     |    +0%       | Good distance
Mid → Mid            |    85%     |    -5%       | Moderate throw
Front → Back         |    75%     |   -10%       | Longer throw
Back → Front         |    70%     |   -10%       | Getting far for a throw
Mid → Back           |    65%     |   -15%       | Extended range
Back → Mid           |    60%     |   -15%       | Too far
Back → Back          |    50%     |   -20%       | Max range, very hard
```

### Spells
**No position modifier.** Magic ignores physical distance.
100% damage and standard accuracy from any position to any position.

### Enemies Use Same Rules
All position-to-position modifiers apply equally to enemies.
An enemy melee fighter in their front row has reduced effectiveness
against player characters in the back row, and vice versa.

---

## 5. TARGETING

### Single-Target Attacks (Melee, Ranged, Individual Spells)
1. Player selects target ROW
2. Player selects target GROUP within that row
3. Attack resolves against one individual in that group
4. If the individual dies, overflow damage is LOST (not carried to next)
5. Dead individuals are removed; group count decreases

### Enemy Targeting (AI)
Enemies select targets based on AI behavior + position weighting:
```
Melee enemy targeting player side:
  Front characters:  50% chance    (No Front: Mid 60%, Back 40%)
  Mid characters:    30% chance    (No Front or Mid: Back 100%)
  Back characters:   20% chance

Ranged/Magic enemy: Equal chance for all positions.
```
Within the selected row, AI picks a group based on behavior type:
- Aggressive: targets highest-damage group
- Defensive: targets lowest-HP group
- Tactical: targets healers/mages
- Random: random group

### Row Capacity
No hard limit on enemies per group for now. Large creatures
(Orc Chieftain, Troll) effectively count as multiple in a group.
Dragons or Giants may fill an entire row solo.

---

## 6. SPELL TARGETING SCOPES

All damage spells and status spells follow the same four-scope progression.
Higher-level versions of the same element expand targeting scope.

### Four Scopes
```
Individual:   Hits one enemy in one group.
Group:        Hits all enemies in one group.
Row:          Hits all enemies in one row (both groups).
All:          Hits every enemy in every row.
```

### Elemental Spell Progressions
```
Fire:      Firebolt (Individual) → Fireball (Group) → Fireswarm (Row) → Inferno (All)
Ice:       Frost Bolt (Individual) → Ice Storm (Group) → Blizzard (Row) → Absolute Zero (All)
Lightning: Shock (Individual) → Lightning Bolt (Group) → Chain Lightning (Row) → Tempest (All)
Divine:    Smite (Individual) → Holy Blast (Group) → Divine Wrath (Row) → Judgment (All)
Shadow:    Dark Bolt (Individual) → Shadow Burst (Group) → Darkness (Row) → Void (All)
Nature:    Thorn (Individual) → Entangle (Group) → Bramblestorm (Row) → Earthquake (All)
Arcane:    Magic Missile (Individual) → Arcane Blast (Group) → Arcane Storm (Row) → Cataclysm (All)
```

### Status Spell Progressions
```
Sleep:     Sleep (Individual) → Mass Sleep (Group) → Deep Slumber (Row) → ???
Poison:    Poison (Individual) → Toxic Cloud (Group) → Miasma (Row) → Plague (All)
Slow:      Slow (Individual) → Mass Slow (Group) → Time Warp (Row) → ???
Stun:      Stun (Individual) → Mass Stun (Group) → Shockwave (Row) → ???
Fear:      Frighten (Individual) → Terror (Group) → Dread (Row) → Panic (All)
```

### Healing & Buff Spells (Individual or All Party ONLY)
```
Healing:   Heal (Individual) → Mass Heal (All Party)
Curing:    Purify (Individual) → Mass Purify (All Party)
Bless:     Bless (Individual) → Divine Blessing (All Party)
Resist:    Fire Resist (Individual) → Mass Fire Resist (All Party)
           (same pattern for Ice Resist, Lightning Resist, etc.)
```

### Cost Scaling
Each scope increase roughly doubles the MP cost:
```
Individual:  Base cost (e.g., Firebolt 8 MP)
Group:       ~2x base (e.g., Fireball 16 MP)
Row:         ~3.5x base (e.g., Fireswarm 28 MP)
All:         ~5x base (e.g., Inferno 40 MP)
```

---

## 7. CLASS SPELL DESIGN

### Mage (INT-based, INT-MP)
Full elemental versatility. Access to Fire, Ice, Lightning, Arcane, Shadow.
Damage spells follow the full Individual → Group → Row → All progression.
Status spells: Sleep, Slow, Silence, Blindness.
Utility: Detect Magic, Knock, Light, Identify, Analyze.

### Cleric (PIE-based, PIE-MP)
**Divine damage ONLY.** No elemental spells.
Offensive: Smite → Holy Blast → Divine Wrath → Judgment.
Healing: Heal → Mass Heal.
Buffs: Bless → Divine Blessing. Resist (Individual) → Mass Resist (All).
Curing: Purify → Mass Purify.
Status: Turn Undead (fear on undead, Group target).
Utility: Bless items, create holy water.

### Ranger (WIS-based, WIS-MP)
**Utility-focused only.** No direct damage spells.
Offensive utility: Poison Arrow (adds poison to physical attack), Entangle (immobilize).
Detection: Track (reveal enemy info), Animal Sense (detect ambush/traps).
Healing: Nature's Mending (small HoT), Cure Poison.
Druid (advanced class) gets full Nature offense, summoning, and powerful status.

### Monk (WIS-based, Ki)
Combat abilities, not traditional spells.
Offensive: Flurry of Blows, Stunning Strike, Ki Blast.
Defensive: Iron Skin, Ki Healing.
Utility: Meditation (faster rest recovery), Ki Infusion (crafting).

### Fighter (STR-based, STR-SP)
Combat skills, no spells.
Offensive: Power Strike, Cleave (hit 2 enemies), Shield Bash.
Defensive: Defensive Stance, Rally (minor party buff).
Utility: Wound Binding (out of combat healing), Intimidate.

### Thief (DEX-based, DEX-SP)
Combat skills + tricks, no spells.
Offensive: Quick Strike, Backstab (bonus from stealth), Poison Strike.
Defensive: Evade, Smoke Bomb (blind enemies).
Utility: Detect Traps, Disarm Traps, Lockpicking, Poison crafting.

---

## 8. DAMAGE FORMULAS

### Physical Melee
```
Stat Damage    = (Weapon Primary Stat × Primary Weight)
                 + (Weapon Secondary Stat × Secondary Weight)
Raw Damage     = Stat Damage + Weapon Base Damage + Enhancement Bonus
Position Mod   = Position-to-Position table value (Section 4)
Variance       = random(0.85 to 1.15)
Phys Type Mod  = Enemy resistance to Piercing/Slashing/Blunt
Elemental Dmg  = Enchantment power × Enemy elemental resistance (if enchanted)

Physical Result = (Raw × Position Mod × Variance × Phys Type Mod) - Enemy Defense
Total Damage    = max(1, Physical Result) + Elemental Damage
```

### Physical Ranged
```
Same formula as melee but uses ranged position-to-position table.
Thrown weapons use thrown position-to-position table.
Reach weapons use reach position-to-position table.
```

### Magic Damage
```
Stat Damage    = (Casting Stat × 1.5) + Focus Item Bonus
Raw Damage     = Stat Damage + Spell Power
Variance       = random(0.90 to 1.10)
Elem Type Mod  = Enemy resistance to spell's elemental type
No position modifier (spells ignore distance)

Magic Result   = (Raw × Variance × Elem Type Mod) - Enemy Magic Resistance
Total Damage   = max(1, Magic Result)
```

### Healing
```
Heal Amount = (PIE × 2.0) + Spell Power + Focus Bonus + random(0 to PIE/2)
```
No resistance. Always full effect.

---

## 9. ACCURACY SYSTEM

### Physical Accuracy
```
Base:      75%
DEX Mod:   + (Attacker DEX - Defender DEX) × 2%
Weapon:    + Weapon Accuracy Modifier
Enhance:   + Enhancement Bonus
Position:  + Position-to-Position Accuracy Modifier (Section 4)
Status:    - 5% if Burning, Poisoned, Frostbitten
           - 10% if Shocked
           - 30% if Blinded
Minimum:   30%
Maximum:   95%
```

### Magic Accuracy (applies to ALL spells — no auto-hit)
```
Base:      80%
Stat Mod:  + (Casting Stat - Defender WIS) × 2%
Spell:     + Spell-specific modifier (Magic Missile +15%, etc.)
Focus:     + Focus item bonus
Status:    Same penalties as physical
Minimum:   30%
Maximum:   95%
```

---

## 10. CRITICAL HIT SYSTEM

### Precision Critical (Thieves, Rangers, Monks)
```
Chance = 5% + (DEX / 8)%
Also possible: 5% + (WIS / 8)% for Monks (finding the right spot)
Multiplier: 2.0x for Thieves/Assassins, 1.5x for others
Piercing weapons (daggers, arrows): +3% crit chance
```

### Power Critical (Fighters)
```
Chance = 5% + (STR / 10)%
Multiplier: 1.5x but ignores 50% of enemy Defense on crit
Heavy weapons (broadswords, maces): +2% crit chance
```

### Ki Critical (Monks)
```
Chance = 5% + (WIS / 8)%
Multiplier: 1.75x
Applies to Ki abilities only
```

### Spell Critical
```
Chance = 5% + (Casting Stat / 10)%
Multiplier: 1.5x damage
```

### Heal Critical
```
Chance = 5% + (PIE / 10)%
Multiplier: 1.5x healing
```

---

## 11. DEFENSE & RESISTANCE

### Physical Defense
```
Defense = (CON × 0.5) + Armor Value + Shield Value + Buffs
```

### Magic Resistance
```
Magic Resistance = (WIS × 0.5) + Equipment Bonus + Buffs
```

### Defend Action
- Physical Defense × 1.5 until next turn
- Magic Resistance × 1.25 until next turn
- Enemies have -15% accuracy against defending character

---

## 12. RESOURCE REGENERATION IN COMBAT

End of each round:
```
Per turn: +(Relevant Stat ÷ 4) + 3% of max resource
Monk Ki: +(WIS ÷ 4) + 3.75% of max Ki (25% bonus)
HP does NOT regenerate in combat
```

---

## 13. POTION SYSTEM (EXPANDABLE)

### Diminishing Returns
```
1st: 100%, 2nd: 75%, 3rd: 56%, 4th: 42%, 5th: 32%
```
Resets between combats.

System designed so new potions are added as data entries only.
See Crafting Design doc for potion creation.

---

## 14. STATUS EFFECTS (EXPANDABLE)

See Elemental & Enchantment Design doc for full list.
System designed so new status effects are added as data entries only.
All statuses that prevent action set Speed = 0 and skip turn.
All ongoing damage statuses apply -5% accuracy (distraction).

---

## 15. DEATH & DEFEAT

### Character at 0 HP
- Falls unconscious. Cannot act.
- Revivable by healing spell (restores with healed amount as HP)
- If not healed by end of combat: revives with 1 HP

### Total Party Defeat
- Retry battle, return to last town (lose gold), or load save

### Enemy Death
- Removed at 0 HP
- Generates loot (currency, items, equipment, possible chests)
- Grants XP after combat

---

## 16. COMBAT UI REQUIREMENTS

### Must Display (Both Sides)
- Character/enemy portrait or sprite
- Name (or vague description if enemy unknown — see Bestiary)
- HP bar (hidden for unknown enemies)
- Active status effects with icons and remaining duration
- Position indicator [F] [M] [B]
- Group count for enemy groups (e.g., "Goblins ×4")

### Turn order bar at top
### Action menu at bottom (party member's turn)
### Combat log showing recent events

---

## 17. ENEMY STARTER ROSTER

(See v2.0 for full enemy stats — unchanged)
Goblin, Bandit, Wolf, Skeleton Warrior, Orc Chieftain.
Enemy grouping examples:
```
Easy:     [3 Goblins] front
Medium:   [3 Goblins][1 Bandit] front, [2 Goblin Archers] mid
Hard:     [2 Orc Fighters] front, [3 Goblin Archers] mid, [1 Orc Mage] back
Boss:     [1 Orc Chieftain][2 Goblins] front, [1 Goblin Shaman] back
```

---

## 18. DESIGN PRINCIPLES

- All formulas in centralized config files — one-line edits to tune
- Debug mode shows all math in real-time during combat
- Enemies, potions, status effects, spells are all data-driven
- Adding new content = adding data entries, not rewriting code
- Position-to-position system uses same rules for both sides

---

*End of Combat System Design — Draft v3.0*
