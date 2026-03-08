# REALM OF SHADOWS — Elemental & Enchantment System Design
## Draft v1.0

---

## OVERVIEW

All damage in Realm of Shadows has a **type**. Physical damage has subtypes
based on weapon (Piercing, Slashing, Blunt). Magic damage has elemental types
(Fire, Ice, Lightning, Divine, Shadow, Nature, Arcane). Enemies have resistances
and vulnerabilities to specific types, creating tactical depth in weapon and
spell selection. Enchanted weapons and items bridge physical and elemental
systems by adding elemental effects to physical attacks.

---

## 1. DAMAGE TYPES

### Physical Subtypes (determined by weapon)
```
Piercing:   Daggers, arrows, crossbow bolts, spears, rapiers
            - Strong vs: Unarmored, fleshy targets
            - Weak vs: Skeletons (gaps between bones), heavy armor
            
Slashing:   Swords (short, long, broad), axes
            - Moderate all-around
            - Weak vs: Skeletons, stone creatures

Blunt:      Maces, hammers, fists, staves
            - Strong vs: Skeletons (shatters bones), armored (dents plate)
            - Weak vs: Oozes/amorphous (absorb impact)
```

### Elemental Types (determined by spell, enchantment, or innate ability)
```
Fire:       Burns, ongoing damage, illumination
            - Strong vs: Ice creatures, undead, trolls (stops regen), plants
            - Weak vs: Fire elementals, dragons, demons

Ice:        Slows, freezes, shatters
            - Strong vs: Fire creatures, reptiles, water creatures
            - Weak vs: Ice elementals, undead (no blood to freeze)

Lightning:  Shock, disruption, chains
            - Strong vs: Armored (conducts), water creatures
            - Weak vs: Earth creatures, rubber/insulated

Divine:     Holy radiance, purification
            - Strong vs: Undead (+50%), demons, shadow creatures
            - Weak vs: Celestial beings
            - Neutral vs: Living creatures

Shadow:     Darkness, corruption, fear
            - Strong vs: Living creatures, celestial beings
            - Weak vs: Undead (already dead), shadow creatures

Nature:     Growth, decay, primal force
            - Strong vs: Constructs, urban creatures
            - Weak vs: Nature spirits, plants, beasts

Arcane:     Pure magical force, raw energy
            - No specific strengths or weaknesses
            - Not resisted by anything special, not bonus against anything
            - The "reliable neutral" magic type
```

---

## 2. RESISTANCE & VULNERABILITY SYSTEM

### How It Works
Each enemy has a resistance profile:
```
Immune:       Takes 0% damage of that type
Resistant:    Takes 50% damage of that type
Neutral:      Takes 100% damage (default)
Vulnerable:   Takes 150% damage of that type
Very Vulnerable: Takes 200% damage of that type
```

### Example Enemy Profiles
```
Skeleton Warrior:
  Piercing: Resistant (50%)     — arrows pass through gaps
  Slashing: Resistant (50%)     — no flesh to cut
  Blunt: Vulnerable (150%)      — shatters bones
  Fire: Neutral (100%)
  Ice: Resistant (50%)          — no blood to freeze
  Divine: Very Vulnerable (200%) — holy energy destroys undead
  Shadow: Immune (0%)           — already a creature of death

Troll:
  Piercing: Neutral (100%)
  Slashing: Neutral (100%)
  Blunt: Neutral (100%)
  Fire: Vulnerable (150%)       — stops regeneration for 2 turns
  Ice: Neutral (100%)
  Nature: Resistant (50%)       — natural creature

Fire Elemental:
  All Physical: Resistant (50%) — semi-corporeal
  Fire: Immune (0%)             — IS fire
  Ice: Very Vulnerable (200%)   — opposite element
  Lightning: Neutral (100%)
  Water/Nature: Vulnerable (150%)

Ghost:
  All Physical: Immune (0%)     — incorporeal!
  All Magic: Neutral (100%)
  Divine: Vulnerable (150%)
  Shadow: Resistant (50%)
```

### Player Armor Resistances (Future Milestone)
Armor can also provide elemental resistances:
```
Fireproof Cloak:    Fire Resistant (take 50% fire damage)
Insulated Boots:    Lightning Resistant
Blessed Shield:     Shadow Resistant
```

---

## 3. SPELL FLAVOR & ELEMENTS

Each spell now has an elemental type that determines which resistances apply:

### Mage Spells (INT-based, INT-MP cost)
```
Magic Missile:    Arcane type.  Reliable, no special strengths/weaknesses.
Fireball:         Fire type.    AoE. Strong vs undead, trolls, ice creatures.
Frost Bolt:       Ice type.     Single target. Chance to apply Slowed/Frozen.
Lightning Bolt:   Lightning.    Single target, high damage. Bonus vs armored.
Arcane Shield:    Arcane type.  Defensive buff.
```

### Cleric Spells (PIE-based, PIE-MP cost)
```
Smite:            Divine type.  Devastating vs undead and demons.
Heal:             Divine type.  Restores HP (no resistance applies).
Bless:            Divine type.  Buff: accuracy and damage boost.
Turn Undead:      Divine type.  Fear effect on undead enemies.
Purify:           Divine type.  Removes poison, burning, other debuffs.
```

### Ranger Spells (WIS-based, WIS-MP cost)
```
Entangle:         Nature type.  Chance to immobilize enemy (skip turn).
Nature's Mending: Nature type.  Minor heal over time.
Track:            Nature type.  Reveals enemy info (see Bestiary system).
Poison Arrow:     Nature type.  Ranged attack + poison DoT.
```

### Monk Abilities (WIS-based, Ki cost)
```
Flurry of Blows:  Physical (Blunt). Multiple hits.
Iron Skin:        None (self buff). Increases defense.
Stunning Strike:  Physical (Blunt) + chance to Stun.
Ki Blast:         Arcane type.  Ranged Ki projectile.
```

---

## 4. ENCHANTED WEAPONS

### Enhancement Tiers
```
Standard:     No bonus.             "Iron Longsword"
+1:           +1 hit, +1 damage.    "Iron Longsword +1"
+2:           +2 hit, +2 damage.    "Steel Longsword +2"
+3:           +3 hit, +3 damage.    "Fine Steel Longsword +3"
+4:           +4 hit, +4 damage.    Rare.
+5:           +5 hit, +5 damage.    Legendary.
```

### Elemental Enchantments
An enchanted weapon adds elemental damage ON TOP of physical damage.
The elemental portion is checked against the enemy's elemental resistance
separately from the physical portion.

```
Damage Calculation for Enchanted Weapon:
  Physical Damage = normal weapon formula → vs Physical Defense
  Elemental Damage = Enchantment Power    → vs Elemental Resistance
  Total Damage = Physical Result + Elemental Result
```

### Elemental Weapon Tiers

**Fire Weapons:**
```
Weapon of Sparks:       +2 fire damage per hit
Weapon of Flame:        +5 fire damage, 10% chance: Burning (2 turns)
Weapon of Inferno:      +8 fire damage, 20% chance: Burning (3 turns)
Greater Weapon of Inferno: +12 fire, 30% chance: Burning (4 turns)
```

**Ice Weapons:**
```
Weapon of Chill:        +2 ice damage per hit
Weapon of Frost:        +5 ice damage, 10% chance: Slowed (2 turns)
Weapon of Deep Frost:   +8 ice damage, 20% chance: Frozen (1 turn)
Greater Weapon of Frost: +12 ice, 25% chance: Frozen (2 turns)
```

**Lightning Weapons:**
```
Weapon of Static:       +2 lightning damage per hit
Weapon of Storms:       +5 lightning damage, 10% chance: Shocked (1 turn)
Weapon of Thunder:      +8 lightning, 15% chance: Shocked + Stunned (1 turn)
```

**Divine Weapons (typically maces/hammers):**
```
Blessed Weapon:         +3 divine damage per hit
Holy Weapon:            +6 divine damage, +10% damage vs undead
Sacred Weapon:          +10 divine damage, +25% damage vs undead,
                        10% chance: Turn Undead (fear, 2 turns)
```

**Shadow Weapons (typically daggers):**
```
Weapon of Darkness:     +3 shadow damage per hit
Weapon of Dread:        +6 shadow, 10% chance: Fear (1 turn)
Weapon of the Void:     +10 shadow, 15% chance: Weakness (2 turns)
```

### Example: Sword of Flame +2 vs Skeleton Warrior
```
Fighter (STR 18, DEX 12) with Sword of Flame +2:
  Physical: Longsword formula → 27.2 + 2 (enhancement) = 29.2
    vs Skeleton Slashing Resistance (50%) → 14.6
    minus Skeleton Defense (10) → 4.6 physical damage

  Fire: +5 fire damage
    vs Skeleton Fire Neutral (100%) → 5 fire damage

  Total: ~10 damage per hit
  
  Compare to: Iron Mace (Blunt) vs same Skeleton:
  Physical: Mace formula → ~20
    vs Skeleton Blunt Vulnerability (150%) → 30
    minus Defense (10) → 20 physical damage
    
  The mace is MUCH better here because of Blunt vs Skeleton.
  But the Sword of Flame is better vs a Troll (fire stops regen).
  This creates real weapon-swapping decisions!
```

---

## 5. ENCHANTED CASTER ITEMS

### Wands (Mage focus items)
Boost specific spell types. Equipped in off-hand or as primary weapon.
```
Wand of Sparks:         +3 fire spell damage
Wand of Fireballs:      +6 fire spell damage, -2 MP cost for fire spells
Wand of the Inferno:    +10 fire spell damage, -3 MP cost, +5% fire accuracy
Wand of Frost:          +6 ice spell damage, +10% freeze chance
Wand of Lightning:      +6 lightning spell damage, chain to second target (50%)
```

### Orbs (Generalist caster focus)
Boost overall casting without element-specific bonuses.
```
Crystal Orb:            +2 all spell damage, +3% accuracy
Mystic Orb:             +4 all spell damage, +5% accuracy, +5 max MP
Archmage's Orb:         +8 all spell damage, +8% accuracy, +10 max MP
```

### Holy Symbols (Cleric focus)
```
Wooden Holy Symbol:     +2 divine spell damage, +5 heal amount
Silver Holy Symbol:     +5 divine spell damage, +10 heal amount
Gold Holy Symbol:       +8 divine, +20 heal, -2 MP cost for heals
Sacred Relic:           +12 divine, +30 heal, +25% vs undead
```

### Staves (Hybrid weapon/focus)
Already defined in weapon doc. Staves provide both physical damage AND
spell bonuses simultaneously, making them the "I can do a bit of both" option.

---

## 6. STATUS EFFECTS (EXPANDED)

### Ongoing Elemental Effects
```
Burning:      Fire damage per turn for X turns.
              -5% accuracy (pain/distraction).
              Removed by: Ice spell, Purify, water, or expiry.

Frostbitten:  Ice damage per turn for X turns.
              -25% speed (slowed movement).
              -5% accuracy (numbness).
              Removed by: Fire spell, Purify, or expiry.

Shocked:      No ongoing damage.
              -10% accuracy for 1 turn (disoriented).
              Applied by lightning attacks.

Poisoned:     Nature/Shadow damage per turn for X turns.
              -5% accuracy (nausea).
              Removed by: Antidote potion, Purify, or expiry.
```

### Control Effects
```
Stunned:      Skip 1 turn. Speed = 0 for duration.
              Applied by: Stunning Strike, critical hits, 
              some enchanted weapons.

Frozen:       Skip 1-2 turns. Speed = 0.
              +25% physical damage taken (brittle).
              Applied by: Frost spells, Greater Frost weapons.
              Removed by: Fire damage (instantly thaws + extra damage).

Petrified:    Skip 2-4 turns. Speed = 0.
              +50% physical damage taken (brittle stone).
              Immune to poison, burning, bleeding during petrification.
              Applied by: Petrify spell (high level), Basilisk gaze,
              Medusa gaze, certain traps.
              Removed by: Stone to Flesh spell, special potion, or expiry.

Fear:         Flee or skip turn for 1-2 turns.
              -20% damage dealt (trembling).
              Applied by: Shadow spells, Turn Undead (vs undead),
              some boss abilities, Dread weapons.
              Removed by: Bless spell, high PIE save, or expiry.

Blinded:      -30% accuracy for 2 turns.
              Applied by: Flash spell, sand attack, some traps.
              
Silenced:     Cannot cast spells for 2-3 turns. 
              Physical attacks unaffected.
              Applied by: Silence spell, certain enemy abilities.
```

### Positive Buffs
```
Shielded:     +25% physical defense for 3 turns.
Hasted:       +50% speed for 2 turns.
Blessed:      +15% accuracy, +10% damage for 3 turns.
Regenerating: +5% max HP per turn for 3 turns.
Fire Resist:  -50% fire damage taken for 4 turns.
Ice Resist:   -50% ice damage taken for 4 turns.
Lightning Resist: -50% lightning damage taken for 4 turns.
Shadow Resist: -50% shadow damage taken for 4 turns.
Invisible:    Enemies cannot target you for 1-2 turns (Thief ability).
              Broken by attacking or casting.
```

---

## 7. BESTIARY / ENEMY KNOWLEDGE SYSTEM

### Knowledge Tiers
Characters learn about enemies through repeated encounters:

```
Tier 0 — Unknown (first encounter):
  Display: Vague description only.
           "A shambling undead creature in rusted armor"
  HP bar:  Hidden. Only shows "Healthy/Wounded/Near Death"
  Info:    No resistances, weaknesses, or abilities shown.

Tier 1 — Recognized (2nd encounter OR successful Track/Identify):
  Display: Name revealed. "Skeleton Warrior"
  HP bar:  Visible with numbers.
  Info:    Basic attack type shown (melee/ranged).

Tier 2 — Studied (3rd encounter OR high INT/WIS character):
  Display: Full name and variant.
  HP bar:  Full numbers.
  Info:    Resistances and vulnerabilities revealed.
           Attack patterns shown.
           
Tier 3 — Mastered (5+ encounters):
  Display: Everything.
  Info:    Exact stats, loot tables, ability details.
           "You know this enemy inside and out."
```

### Accelerating Knowledge
```
Ranger "Track":     +1 knowledge tier for current combat.
                    WIS check: if passed, +2 tiers.
Mage "Analyze":     +1 knowledge tier (future ability).
High INT (16+):     Automatic +1 tier after first encounter.
High WIS (16+):     Estimate HP range even at Tier 0.
```

### Bestiary Log
Encountered enemies are recorded in a journal/bestiary.
Players can review known enemies between combats.
Knowledge persists across the entire game.

---

## 8. LOOT SYSTEM

### Post-Combat Loot
After every combat, loot is generated:

```
Currency:     Always drops. Amount based on enemy type and count.
              Gold is shared across the party.

Common Items: High drop chance (60-80%).
              Potions, basic ammunition, crafting materials,
              food/supplies.

Uncommon Items: Moderate drop chance (20-40%).
              Better potions, scrolls, basic equipment upgrades.

Rare Items:   Low drop chance (5-15%).
              Enchanted weapons/armor, valuable gems, rare materials.

Enemy Equipment: Some enemies drop what they use.
              Skeleton Warrior → Rusted Chainmail, Worn Sword
              Bandit Archer → Short Bow, Leather Armor
              Orc Chieftain → War Axe, Heavy Shield
              Goblin Shaman → Cracked Wand, Herb Pouch
              Enemy Mage → Damaged Staff, Spell Scroll
              Quality varies: usually worn/damaged versions.
```

### Treasure Chests
Found after boss encounters, in dungeon rooms, or as rare field finds.

```
Chest Discovery:
  1. Chest appears after combat or during exploration.
  2. Visual indicator of chest quality (wooden, iron, ornate, magical).

Trap Detection:
  3. Any character can attempt to detect traps.
     Detection Chance = 30% + (INT × 2%) + (DEX × 1%)
     Thief bonus: +25% detection chance (trained eye).
     Ranger bonus: +10% (awareness).
  4. If trap detected: description of trap type shown.
     "You notice a thin wire connected to the latch."
     "The lock glows faintly — magical ward."

Trap Disarming:
  5. Thief or any character can attempt to disarm.
     Disarm Chance = 20% + (DEX × 3%)
     Thief bonus: +30% disarm chance.
  6. Success: Trap removed, chest opens safely.
  7. Failure: Trap triggers.
     Physical trap: Damage to opener (and possibly front row).
     Poison trap: Poison status to opener.
     Magic trap: AoE damage or status effect to party.
     Alarm trap: Triggers additional combat encounter.

Chest Contents:
  8. Wooden chest: 1-2 items, common to uncommon quality.
  9. Iron chest: 2-3 items, uncommon to rare quality.
  10. Ornate chest: 2-4 items, rare quality, guaranteed enchanted item.
  11. Magical chest: 3-5 items, rare to legendary, unique items possible.
```

---

*End of Elemental & Enchantment System Design — Draft v1.0*
*Connects to: Combat Design, Weapon Design, Enemy Design (future)*
