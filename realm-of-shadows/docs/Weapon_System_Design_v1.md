# REALM OF SHADOWS — Weapon System Design
## Draft v1.0

---

## OVERVIEW

Weapons determine a character's basic attack damage, range (melee vs ranged),
and which stat drives the damage formula. Every class can use certain weapon
types, and some weapons have minimum stat requirements.

---

## 1. WEAPON PROPERTIES

Each weapon has:
```
Name            - Display name
Type            - Category (see Section 2)
Damage          - Base damage value added to formula
Damage Stat     - Which stat drives the damage (STR, DEX, or split)
Range           - Melee or Ranged
Speed Modifier  - Affects turn order (+/- to Speed)
Accuracy Mod    - Bonus or penalty to hit chance
Crit Modifier   - Bonus to critical hit chance
Stat Requirement- Minimum stat needed to equip
Weight Class    - Light, Medium, Heavy (affects position penalty)
```

---

## 2. WEAPON TYPES

### MELEE WEAPONS

**FISTS / UNARMED**
- Damage Stat: STR (50%) + DEX (50%)
- Range: Melee
- Always available, no requirements
- Monks get scaling unarmed damage (base + Level × 2)
- Everyone else: very low base damage (3)
- Speed Mod: +2 (fastest melee option)
- Accuracy Mod: +5%
```
Non-Monk Unarmed:  Damage 3, no requirements
Monk Unarmed:      Damage 3 + (Level × 2), no requirements
```

**DAGGERS / KNIVES**
- Damage Stat: DEX
- Range: Melee
- Light, fast, low damage, high crit
- Speed Mod: +2
- Accuracy Mod: +5%
- Crit Mod: +5%
- No position penalty from any row (quick jabbing)
```
Rusty Knife:       Damage 4, no requirement
Iron Dagger:       Damage 6, DEX 8
Fine Stiletto:     Damage 8, DEX 12
Assassin's Blade:  Damage 12, DEX 16
```

**SHORT SWORDS**
- Damage Stat: DEX (70%) + STR (30%)
- Range: Melee
- Balanced speed and damage
- Speed Mod: +1
- Accuracy Mod: +0%
```
Worn Short Sword:  Damage 6, DEX 8
Iron Short Sword:  Damage 9, DEX 10
Steel Rapier:      Damage 12, DEX 13, STR 8
Dueling Blade:     Damage 15, DEX 15, STR 10
```

**LONGSWORDS**
- Damage Stat: STR (70%) + DEX (30%)
- Range: Melee
- Good damage, moderate speed
- Speed Mod: 0
- Accuracy Mod: +0%
```
Worn Longsword:    Damage 8, STR 10
Iron Longsword:    Damage 11, STR 12
Steel Longsword:   Damage 14, STR 14
Knight's Blade:    Damage 18, STR 16, DEX 10
```

**BROADSWORDS / GREATSWORDS**
- Damage Stat: STR
- Range: Melee
- Heavy, slow, high damage
- Speed Mod: -2
- Accuracy Mod: -5%
- Weight Class: Heavy (extra position penalty from Back row)
```
Iron Broadsword:   Damage 14, STR 13
Steel Greatsword:  Damage 18, STR 16
War Blade:         Damage 22, STR 18
Executioner's Sword: Damage 28, STR 22
```

**MACES / HAMMERS**
- Damage Stat: STR
- Range: Melee
- Good vs armored enemies (partial armor bypass: ignore 30% of Defense)
- Speed Mod: -1
- Accuracy Mod: -5%
```
Wooden Club:       Damage 6, STR 8
Iron Mace:         Damage 10, STR 11
War Hammer:        Damage 15, STR 15
Holy Mace:         Damage 13, STR 12, PIE 12 (bonus vs undead)
```

**STAVES**
- Damage Stat: STR (40%) + INT (60%) for mages, STR (40%) + WIS (60%) for monks/clerics
- Range: Melee
- Low physical damage but can channel magical energy
- Speed Mod: 0
- Accuracy Mod: +0%
- Special: Adds bonus to spell damage when equipped
```
Walking Stick:     Damage 3, no requirement, Spell Bonus +2
Wooden Staff:      Damage 5, INT 8 or WIS 8, Spell Bonus +4
Arcane Staff:      Damage 7, INT 12, Spell Bonus +8
Staff of the Wild: Damage 7, WIS 12, Spell Bonus +8
Sacred Staff:      Damage 7, PIE 12, Spell Bonus +8
```

**SPEARS**
- Damage Stat: STR (60%) + DEX (40%)
- Range: Melee (but reduced position penalty — reach weapon)
- Position Modifier: Front 100%, Mid 95%, Back 75% (better than normal melee from Mid)
- Speed Mod: 0
- Accuracy Mod: +5% (reach advantage)
```
Wooden Spear:      Damage 7, STR 9
Iron Spear:        Damage 10, STR 11, DEX 9
War Pike:          Damage 14, STR 14, DEX 10
Halberd:           Damage 18, STR 16, DEX 12
```

### RANGED WEAPONS

**SLINGS**
- Damage Stat: DEX
- Range: Ranged (100% damage from any position)
- Low damage but available to almost any class
- Speed Mod: 0
- Accuracy Mod: -5% (harder to aim)
- Ammo: Stones (cheap, unlimited for now)
```
Simple Sling:      Damage 4, DEX 8
Hunter's Sling:    Damage 7, DEX 11
War Sling:         Damage 10, DEX 14
```

**BOWS**
- Damage Stat: DEX (80%) + STR (20%) (need strength to draw)
- Range: Ranged
- Good damage, good accuracy at range
- Speed Mod: 0
- Accuracy Mod: +5%
```
Short Bow:         Damage 6, DEX 10, STR 8
Hunting Bow:       Damage 9, DEX 12, STR 9
Long Bow:          Damage 13, DEX 14, STR 11
Composite Bow:     Damage 17, DEX 16, STR 13
```

**CROSSBOWS**
- Damage Stat: flat (mostly mechanical, less stat-dependent)
- Range: Ranged
- High damage, slow reload
- Speed Mod: -3 (slow to reload)
- Accuracy Mod: +10% (mechanical precision)
```
Light Crossbow:    Damage 12, DEX 8
Heavy Crossbow:    Damage 18, DEX 10, STR 10
Siege Crossbow:    Damage 24, DEX 12, STR 14
```

**THROWN WEAPONS**
- Damage Stat: DEX (60%) + STR (40%)
- Range: Ranged
- Moderate damage, fast, consumable in future
- Speed Mod: +1
- Accuracy Mod: +0%
```
Throwing Knife:    Damage 5, DEX 10
Throwing Axe:      Damage 8, DEX 11, STR 10
Javelin:           Damage 11, DEX 12, STR 12
```

---

## 3. CLASS WEAPON PROFICIENCIES

Each class can use certain weapon types. Using a weapon you're not
proficient with incurs: -20% damage, -15% accuracy, -2 Speed.

```
             Fists  Dag  Short  Long  Broad  Mace  Staff  Spear  Sling  Bow  Xbow  Thrown
Fighter:       ✓     ✓     ✓     ✓      ✓     ✓     -      ✓      -     -    ✓      ✓
Mage:          ✓     ✓     -     -      -     -     ✓      -      ✓     -    -      -
Cleric:        ✓     -     -     -      -     ✓     ✓      -      ✓     -    -      -
Thief:         ✓     ✓     ✓     -      -     -     -      -      ✓     ✓    -      ✓
Ranger:        ✓     ✓     ✓     ✓      -     -     ✓      ✓      -     ✓    ✓      ✓
Monk:          ✓     -     -     -      -     -     ✓      ✓      -     -    -      -
```

### Design Notes:
- **Fighter**: Broadest melee selection. Can use almost anything with a blade or handle.
  No bows (that's the Ranger's territory) but can use crossbows (mechanical, no finesse needed).
- **Mage**: Limited to daggers (emergency defense), staves (spell amplification), and slings (ranged option from back row). Cannot use real weapons effectively.
- **Cleric**: Maces fit the holy warrior archetype. Staves for casting. Slings for range. No edged weapons (religious restriction — a classic RPG tradition).
- **Thief**: Fast, light weapons. Daggers, short swords, slings, bows, thrown weapons. Nothing heavy — they rely on speed and precision, not brute force.
- **Ranger**: Most versatile. Good with bows (primary), melee backup with swords and spears, and familiar with most ranged options.
- **Monk**: Fists are primary. Staves and spears complement martial arts. Nothing else — monks reject conventional weapons as a philosophical choice.

---

## 4. DAMAGE FORMULA (REVISED WITH WEAPONS)

### Physical Melee Attack
```
Stat Damage = (Primary Weapon Stat × Weapon Stat Weight) + (Secondary × Secondary Weight)
Raw Damage  = Stat Damage + Weapon Base Damage + Ability Bonus (if using ability)
Position Mod = based on position and weapon weight class
Variance    = random(0.85 to 1.15)

Final Damage = (Raw Damage × Position Mod × Variance) - Enemy Defense
Minimum = 1
```

### Example: Fighter with Iron Longsword (STR 18, DEX 12)
```
Stat Damage = (18 × 0.70) + (12 × 0.30) = 12.6 + 3.6 = 16.2
Raw Damage  = 16.2 + 11 (weapon) = 27.2
Position    = 1.0 (Front)
vs Goblin   = 27.2 × 1.0 × ~1.0 - 2 = ~25 damage
```

### Example: Mage with Simple Sling (DEX 6, from Back row)
```
Stat Damage = 6 × 1.0 = 6
Raw Damage  = 6 + 4 (weapon) = 10
Position    = 1.0 (ranged — no penalty)
vs Goblin   = 10 × 1.0 × ~1.0 - 2 = ~8 damage
```
Not great, but it's something — and it doesn't spend any MP.

### Example: Mage casting Fireball (INT 15)
```
Stat Damage = 15 × 1.5 + Staff Spell Bonus 4 = 26.5
Spell Power = 20
Raw Damage  = 26.5 + 20 = 46.5
vs Goblin   = 46.5 - 1 (magic resist) = ~45 damage
```

---

## 5. DUAL WIELDING / OFF-HAND (Future Milestone)

Not for Milestone 2, but planned:
- Some classes (Thief, Ranger) could dual-wield light weapons
- Main hand does 100% damage, off-hand does 50%
- Off-hand attack is a separate hit (can miss independently)
- Requires both weapons to be Light weight class
- Replaces shield slot

---

## 6. WEAPON SWITCHING

- Characters can equip one weapon at a time (for now)
- Switching weapons in combat costs your action (like changing position)
- Between combats: free to change
- Future: weapon slots / quick-swap system

---

## 7. STARTING WEAPONS BY CLASS

Each class begins with a basic weapon appropriate to their style:

```
Fighter:  Worn Longsword (Damage 8, STR 10)
Mage:     Walking Stick (Damage 3, Spell Bonus +2) + Simple Sling (Damage 4, DEX 8)
Cleric:   Wooden Club (Damage 6, STR 8) + Simple Sling (Damage 4, DEX 8)
Thief:    Rusty Knife (Damage 4) + Simple Sling (Damage 4, DEX 8)
Ranger:   Short Bow (Damage 6, DEX 10) + Worn Short Sword (Damage 6, DEX 8)
Monk:     Unarmed (Damage 3 + Level×2 = 5 at Level 1)
```

Note: Mage, Cleric, and Thief start with a sling as their ranged backup option.
Rangers start with both melee and ranged weapons.
Monks start empty-handed (and prefer it that way).

---

## 8. ENEMY GROUPINGS (Conceptual — Detail Later)

Enemies appear in logical groups based on who would actually be together:

**Wilderness encounters:**
- Wolves (pack of 3-5)
- Bandits + Bandit Archer (2 melee + 1 ranged)
- Bears (solo or mother + cubs)

**Dungeon encounters:**
- Skeletons + Skeleton Mage (melee + caster)
- Goblins + Goblin Shaman (fodder + healer/buffer)
- Orc Warriors + Orc Chieftain (soldiers + leader)

**Urban encounters:**
- Thieves + Assassin (fast + deadly)
- City Guard patrol (disciplined, tanky)
- Gang + Gang Boss (numbers + leader)

**Future enemy archetypes that mirror player mechanics:**
- Enemy Mages (cast spells, weak to melee, stay in back)
- Enemy Monks (fast, dodge, Ki abilities)
- Enemy Healers (heal other enemies, priority targets)
- Trolls (regenerate HP each turn, weak to fire)
- Ghosts (immune to physical, only magic works)
- Dragons (massive HP, AoE breath, multiple attacks per turn)

These create tactical puzzles:
- Troll regenerating? Better have fire magic.
- Enemy healer keeping warriors alive? Take out the healer first.
- Ghost immune to swords? Hope your Mage has MP left.
- Mixed group with casters in back? Ranger picks them off with bow.

---

*End of Weapon System Design — Draft v1.0*
*Connects to: Combat Design, Class Design, Equipment System (future)*
