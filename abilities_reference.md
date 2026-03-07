# Realm of Shadows — Abilities & Spells Reference

**Generated from:** `core/abilities.py`, `core/combat_engine.py`

> ⚠ = Discrepancy between description and implementation  |  ✓ = Matches description

---
## Discrepancy Summary

| Class | Ability | Issue |
|-------|---------|-------|
| Monk | Pressure Point | Says 'target deals 30% less damage' — applies a debuff status, but _active_buff_mods has n |
| Paladin | Holy Nova | Says 'damages all enemies AND heals all allies' — typed as aoe, not aoe+heal; only damages |
| Assassin | Shadow Step | Says 'next attack is a guaranteed backstab' — applies the shadow_step buff (×1.50 damage)  |
| Assassin | Death Mark | Says 'if target dies while marked, reset cooldowns' — mark is applied, death-trigger coold |
| Assassin | Fan of Knives | Says '20% bleed chance on each hit' — bleed status is not in apply_poison or _inflict_spec |
| Warden | Call of the Wild | Says 'damages all enemies AND heals all allies' — typed as aoe; only damages enemies, the  |
| Spellblade | Blade Barrier | Says 'reflect 25% of incoming damage' — reflect_pct field exists in ability data but _appl |
| Archmage | Spell Mastery | Typed as 'passive' — same issue as Last Stand; falls through to is_offensive if activated. |
| Archmage | Wish | Typed as 'special' — special types fall through to is_offensive; cast as an attack with no |
| High Priest | Mass Resurrection | Says 'revive ALL fallen allies' — typed as revive; code only finds the first fallen ally ( |
| High Priest | Miracle | Typed as 'special' — same issue as Wish; treated as offensive. Full party HP+MP restore is |

---

## Fighter

### ✓ Power Strike

**Type:** attack  **Resource:** STR-SP  **Cost:** 10  **Unlock Level:** 1

**Description (shown to player):** Heavy melee attack dealing 60% bonus damage.

**Mechanical fields:** `power: 1.6`

**What the code actually does:**
> Physical melee hit using attacker STR vs target DEF; applies bonus_crit, execute_threshold, stun/slow/poison on hit

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True → _apply_physical_hit(target, power=1.6)
```

**Analysis:** ✓ Matches description

---

### ✓ Defensive Stance

**Type:** buff  **Resource:** STR-SP  **Cost:** 8  **Unlock Level:** 1

**Description (shown to player):** Reduce incoming damage for 2 turns.

**Mechanical fields:** `buff: defense_up`, `duration: 2 turns`

**What the code actually does:**
> Applies named status to self or all_allies for duration turns; mechanical effect driven by _active_buff_mods

**Relevant code path:**
```python
# resolve_ability() → is_buff=True
apply_status_effect(attacker, 'defense_up', 2)
# Effect in _active_buff_mods():
  def_reduce += 5  # flat damage reduction per hit
```

**Analysis:** ✓ Matches description

---

### ✓ Shield Bash

**Type:** attack  **Resource:** STR-SP  **Cost:** 12  **Unlock Level:** 3

**Description (shown to player):** Bash with shield. 35% chance to stun.

**Mechanical fields:** `power: 1.3`, `stun: 35%`

**What the code actually does:**
> Physical melee hit using attacker STR vs target DEF; applies bonus_crit, execute_threshold, stun/slow/poison on hit

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True → _apply_physical_hit(target, power=1.3)
if random.random() < 0.35: apply_status_effect(target, 'Stunned', 1)
```

**Analysis:** ✓ Matches description

---

### ✓ Cleave

**Type:** aoe  **Resource:** STR-SP  **Cost:** 18  **Unlock Level:** 5

**Description (shown to player):** Wide slash hitting all front-row enemies.

**Mechanical fields:** `power: 1.0`

**What the code actually does:**
> Hits all living enemies; magic or physical determined by resource type; no per-target accuracy roll

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True, is_aoe=True
# aoe_targets = all living enemies
for tgt in aoe_targets:
    _apply_physical_hit(tgt, power=1.0)  # element=physical
```

**Analysis:** ✓ Matches description

---

### ✓ War Cry

**Type:** buff  **Resource:** STR-SP  **Cost:** 15  **Unlock Level:** 8  **Targets:** all_allies

**Description (shown to player):** Inspire allies, boosting damage for 3 turns.

**Mechanical fields:** `buff: war_cry`, `duration: 3 turns`

**What the code actually does:**
> Applies named status to self or all_allies for duration turns; mechanical effect driven by _active_buff_mods

**Relevant code path:**
```python
# resolve_ability() → is_buff=True
apply_status_effect(all_players, 'war_cry', 3)
# Effect in _active_buff_mods():
  atk_mult *= 1.25  # all allies
```

**Analysis:** Inspire *allies* — says all allies get boost

---

### ✓ Executioner

**Type:** attack  **Resource:** STR-SP  **Cost:** 25  **Unlock Level:** 12

**Description (shown to player):** Devastating blow. Instant kill if target below 25% HP.

**Mechanical fields:** `power: 2.5`, `execute below 25% HP`

**What the code actually does:**
> Physical melee hit using attacker STR vs target DEF; applies bonus_crit, execute_threshold, stun/slow/poison on hit

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True → _apply_physical_hit(target, power=2.5)
if hp_pct <= 0.25 and alive: target['hp']=0; target['alive']=False  # EXECUTE
```

**Analysis:** Says 'instant kill if below 25% HP' — executes AFTER damage, not instead of it

---


## Mage

### ✓ Magic Missile

**Type:** spell  **Resource:** INT-MP  **Cost:** 8  **Unlock Level:** 1  **Element:** arcane

**Description (shown to player):** Unerring arcane bolt. Very high hit chance.

**Mechanical fields:** `power: 1.0`

**What the code actually does:**
> Magic hit using attacker INT/PIE vs target MDEF; same special effect chain as attack

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True → _apply_magic_hit(target, power=1.0)
```

**Analysis:** ✓ Matches description

---

### ✓ Arcane Shield

**Type:** buff  **Resource:** INT-MP  **Cost:** 10  **Unlock Level:** 1

**Description (shown to player):** Erect a personal arcane barrier. Reduces all damage taken for 3 turns.

**Mechanical fields:** `buff: magic_shield`, `duration: 3 turns`

**What the code actually does:**
> Applies named status to self or all_allies for duration turns; mechanical effect driven by _active_buff_mods

**Relevant code path:**
```python
# resolve_ability() → is_buff=True
apply_status_effect(attacker, 'magic_shield', 3)
# Effect in _active_buff_mods():
  def_reduce += 6
```

**Analysis:** ✓ Matches description

---

### ✓ Firebolt

**Type:** spell  **Resource:** INT-MP  **Cost:** 10  **Unlock Level:** 2  **Element:** fire

**Description (shown to player):** Fire bolt that sets the target ablaze for 2 turns.

**Mechanical fields:** `power: 1.3`

**What the code actually does:**
> Magic hit using attacker INT/PIE vs target MDEF; same special effect chain as attack

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True → _apply_magic_hit(target, power=1.3)
```

**Analysis:** ✓ Matches description

---

### ✓ Frostbolt

**Type:** spell  **Resource:** INT-MP  **Cost:** 10  **Unlock Level:** 2  **Element:** ice

**Description (shown to player):** Ice bolt. 50% chance to slow target.

**Mechanical fields:** `power: 1.2`, `slow: 50%`

**What the code actually does:**
> Magic hit using attacker INT/PIE vs target MDEF; same special effect chain as attack

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True → _apply_magic_hit(target, power=1.2)
if random.random() < 0.5: apply_status_effect(target, 'Slowed', 2)
```

**Analysis:** ✓ Matches description

---

### ✓ Fireball

**Type:** aoe  **Resource:** INT-MP  **Cost:** 20  **Unlock Level:** 4  **Element:** fire

**Description (shown to player):** Explosive fire blast hitting all enemies in a row.

**Mechanical fields:** `power: 1.4`

**What the code actually does:**
> Hits all living enemies; magic or physical determined by resource type; no per-target accuracy roll

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True, is_aoe=True
# aoe_targets = all living enemies
for tgt in aoe_targets:
    _apply_magic_hit(tgt, power=1.4)  # element=fire
```

**Analysis:** ✓ Matches description

---

### ✓ Ice Lance

**Type:** spell  **Resource:** INT-MP  **Cost:** 14  **Unlock Level:** 5  **Element:** ice

**Description (shown to player):** Piercing ice shard. 40% chance to slow.

**Mechanical fields:** `power: 1.5`, `slow: 40%`

**What the code actually does:**
> Magic hit using attacker INT/PIE vs target MDEF; same special effect chain as attack

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True → _apply_magic_hit(target, power=1.5)
if random.random() < 0.4: apply_status_effect(target, 'Slowed', 2)
```

**Analysis:** ✓ Matches description

---

### ✓ Deep Freeze

**Type:** spell  **Resource:** INT-MP  **Cost:** 18  **Unlock Level:** 7  **Element:** ice

**Description (shown to player):** Freezes target solid. 35% chance to stun for 1 turn.

**Mechanical fields:** `power: 1.6`, `stun: 35%`

**What the code actually does:**
> Magic hit using attacker INT/PIE vs target MDEF; same special effect chain as attack

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True → _apply_magic_hit(target, power=1.6)
if random.random() < 0.35: apply_status_effect(target, 'Stunned', 1)
```

**Analysis:** ✓ Matches description

---

### ✓ Chain Lightning

**Type:** aoe  **Resource:** INT-MP  **Cost:** 25  **Unlock Level:** 8  **Element:** lightning

**Description (shown to player):** Lightning arcing between all enemies.

**Mechanical fields:** `power: 1.3`

**What the code actually does:**
> Hits all living enemies; magic or physical determined by resource type; no per-target accuracy roll

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True, is_aoe=True
# aoe_targets = all living enemies
for tgt in aoe_targets:
    _apply_magic_hit(tgt, power=1.3)  # element=lightning
```

**Analysis:** ✓ Matches description

---

### ✓ Meteor

**Type:** aoe  **Resource:** INT-MP  **Cost:** 40  **Unlock Level:** 12  **Element:** fire

**Description (shown to player):** Apocalyptic fire from the sky.

**Mechanical fields:** `power: 1.8`

**What the code actually does:**
> Hits all living enemies; magic or physical determined by resource type; no per-target accuracy roll

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True, is_aoe=True
# aoe_targets = all living enemies
for tgt in aoe_targets:
    _apply_magic_hit(tgt, power=1.8)  # element=fire
```

**Analysis:** ✓ Matches description

---


## Cleric

### ✓ Heal

**Type:** heal  **Resource:** PIE-MP  **Cost:** 10  **Unlock Level:** 1

**Description (shown to player):** Restore HP to one ally.

**Mechanical fields:** `power: 1.0`

**What the code actually does:**
> Heals single ally; crit possible; if target is down, revives them at 0 then heals

**Relevant code path:**
```python
# resolve_ability() → is_heal=True
heal_targets = [target or attacker]
amount = calc_healing(attacker, {'power': cost * 1.0})
target['hp'] = min(target['max_hp'], target['hp'] + amount)
```

**Analysis:** ✓ Matches description

---

### ✓ Smite

**Type:** spell  **Resource:** PIE-MP  **Cost:** 12  **Unlock Level:** 1  **Element:** divine

**Description (shown to player):** Holy damage. Bonus vs undead.

**Mechanical fields:** `power: 1.4`

**What the code actually does:**
> Magic hit using attacker INT/PIE vs target MDEF; same special effect chain as attack

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True → _apply_magic_hit(target, power=1.4)
```

**Analysis:** ✓ Matches description

---

### ✓ Cure Poison

**Type:** cure  **Resource:** PIE-MP  **Cost:** 8  **Unlock Level:** 3

**Description (shown to player):** Remove poison from one ally.

**Mechanical fields:** `cures: poison`

**What the code actually does:**
> Removes matching status from target; Remove Curse also lifts cursed equipment

**Relevant code path:**
```python
# resolve_ability() → is_cure=True
# Removes 'poison' status from target
```

**Analysis:** ✓ Matches description

---

### ✓ Prayer of Healing

**Type:** aoe_heal  **Resource:** PIE-MP  **Cost:** 20  **Unlock Level:** 5

**Description (shown to player):** Heal all allies for a moderate amount.

**Mechanical fields:** `power: 1.0`

**What the code actually does:**
> Heals all living allies by calc_healing(); crit heal possible

**Relevant code path:**
```python
# resolve_ability() → is_heal=True
heal_targets = [p for p in all_players if p['alive']]
amount = calc_healing(attacker, {'power': cost * 1.0})
target['hp'] = min(target['max_hp'], target['hp'] + amount)
```

**Analysis:** ✓ Matches description

---

### ✓ Turn Undead

**Type:** debuff  **Resource:** PIE-MP  **Cost:** 15  **Unlock Level:** 5  **Targets:** undead

**Description (shown to player):** Force undead to flee for 3 turns.

**Mechanical fields:** (none beyond type handling)

**What the code actually does:**
> Magic accuracy roll; on hit applies named status for duration turns; no special mechanical modifier unless name matches _active_buff_mods

**Relevant code path:**
```python
# resolve_ability() → is_debuff=True
# magic accuracy roll → apply_status_effect(target, 'Turn Undead', )
```

**Analysis:** Says 'force undead to flee for 3 turns' — applies a generic debuff status, no undead-only filter; works on any enemy

---

### ✓ Remove Curse

**Type:** cure  **Resource:** PIE-MP  **Cost:** 18  **Unlock Level:** 7

**Description (shown to player):** Lift a curse from one ally, freeing any cursed equipment they wear.

**Mechanical fields:** `cures: curse`

**What the code actually does:**
> Removes matching status from target; Remove Curse also lifts cursed equipment

**Relevant code path:**
```python
# resolve_ability() → is_cure=True
# Removes 'curse' status from target
# Also lifts curse_lifted flag on equipped cursed items
```

**Analysis:** ✓ Matches description

---

### ✓ Divine Wrath

**Type:** aoe  **Resource:** PIE-MP  **Cost:** 30  **Unlock Level:** 10  **Element:** divine

**Description (shown to player):** Holy fire consumes all enemies.

**Mechanical fields:** `power: 1.8`

**What the code actually does:**
> Hits all living enemies; magic or physical determined by resource type; no per-target accuracy roll

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True, is_aoe=True
# aoe_targets = all living enemies
for tgt in aoe_targets:
    _apply_magic_hit(tgt, power=1.8)  # element=divine
```

**Analysis:** ✓ Matches description

---


## Thief

### ✓ Quick Strike

**Type:** attack  **Resource:** DEX-SP  **Cost:** 8  **Unlock Level:** 1

**Description (shown to player):** Fast strike with +15% crit chance.

**Mechanical fields:** `power: 1.3`, `+15% crit`

**What the code actually does:**
> Physical melee hit using attacker STR vs target DEF; applies bonus_crit, execute_threshold, stun/slow/poison on hit

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True → _apply_physical_hit(target, power=1.3)
crit_chance += ability['bonus_crit']  # +15%
```

**Analysis:** ✓ Matches description

---

### ✓ Evade

**Type:** buff  **Resource:** DEX-SP  **Cost:** 6  **Unlock Level:** 1

**Description (shown to player):** Greatly increase dodge chance for 2 turns.

**Mechanical fields:** `buff: evasion`, `duration: 2 turns`

**What the code actually does:**
> Applies named status to self or all_allies for duration turns; mechanical effect driven by _active_buff_mods

**Relevant code path:**
```python
# resolve_ability() → is_buff=True
apply_status_effect(attacker, 'evasion', 2)
# Effect in _active_buff_mods():
  45% chance to dodge incoming hit
```

**Analysis:** ✓ Matches description

---

### ✓ Backstab

**Type:** attack  **Resource:** DEX-SP  **Cost:** 14  **Unlock Level:** 3

**Description (shown to player):** Vicious strike. +25% crit, huge damage on crit.

**Mechanical fields:** `power: 2.0`, `+25% crit`

**What the code actually does:**
> Physical melee hit using attacker STR vs target DEF; applies bonus_crit, execute_threshold, stun/slow/poison on hit

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True → _apply_physical_hit(target, power=2.0)
crit_chance += ability['bonus_crit']  # +25%
```

**Analysis:** ✓ Matches description

---

### ✓ Poison Blade

**Type:** attack  **Resource:** DEX-SP  **Cost:** 12  **Unlock Level:** 5

**Description (shown to player):** Envenomed strike. Applies Weak Poison.

**Mechanical fields:** `power: 1.2`

**What the code actually does:**
> Physical melee hit using attacker STR vs target DEF; applies bonus_crit, execute_threshold, stun/slow/poison on hit

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True → _apply_physical_hit(target, power=1.2)
```

**Analysis:** ✓ Matches description

---

### ✓ Smoke Bomb

**Type:** buff  **Resource:** DEX-SP  **Cost:** 16  **Unlock Level:** 8  **Targets:** all_allies

**Description (shown to player):** All allies gain evasion for 2 turns.

**Mechanical fields:** `buff: smoke_screen`, `duration: 2 turns`

**What the code actually does:**
> Applies named status to self or all_allies for duration turns; mechanical effect driven by _active_buff_mods

**Relevant code path:**
```python
# resolve_ability() → is_buff=True
apply_status_effect(all_players, 'smoke_screen', 2)
# Effect in _active_buff_mods():
  45% chance to dodge — all allies
```

**Analysis:** Says 'all allies' — correctly applied to all_allies, but smoke_screen evasion is 45%, not stated

---

### ✓ Assassinate

**Type:** attack  **Resource:** DEX-SP  **Cost:** 30  **Unlock Level:** 12

**Description (shown to player):** All-in lethal strike. Massive damage.

**Mechanical fields:** `power: 3.0`, `+30% crit`

**What the code actually does:**
> Physical melee hit using attacker STR vs target DEF; applies bonus_crit, execute_threshold, stun/slow/poison on hit

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True → _apply_physical_hit(target, power=3.0)
crit_chance += ability['bonus_crit']  # +30%
```

**Analysis:** ✓ Matches description

---


## Ranger

### ✓ Aimed Shot

**Type:** attack  **Resource:** DEX-SP  **Cost:** 10  **Unlock Level:** 1

**Description (shown to player):** Carefully aimed ranged attack. +20% accuracy.

**Mechanical fields:** `power: 1.5`

**What the code actually does:**
> Physical melee hit using attacker STR vs target DEF; applies bonus_crit, execute_threshold, stun/slow/poison on hit

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True → _apply_physical_hit(target, power=1.5)
```

**Analysis:** ✓ Matches description

---

### ✓ Splitting Arrow

**Type:** attack  **Resource:** DEX-SP  **Cost:** 8  **Unlock Level:** 1

**Description (shown to player):** Arrow pierces front row, hitting back row too. Reduced damage.

**Mechanical fields:** `power: 0.8`

**What the code actually does:**
> Physical melee hit using attacker STR vs target DEF; applies bonus_crit, execute_threshold, stun/slow/poison on hit

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True → _apply_physical_hit(target, power=0.8)
```

**Analysis:** Says 'reduced damage' to back row — back row actually receives 0.6× power, not reduced original

---

### ✓ Entangle

**Type:** debuff  **Resource:** WIS-MP  **Cost:** 12  **Unlock Level:** 3  **Element:** nature

**Description (shown to player):** Roots slow a target for 2 turns.

**Mechanical fields:** (none beyond type handling)

**What the code actually does:**
> Magic accuracy roll; on hit applies named status for duration turns; no special mechanical modifier unless name matches _active_buff_mods

**Relevant code path:**
```python
# resolve_ability() → is_debuff=True
# magic accuracy roll → apply_status_effect(target, 'Entangle', )
```

**Analysis:** Says 'roots slow a target for 2 turns' — applies a generic debuff with no slow_ modifier; does not reduce enemy speed stat

---

### ✓ Barrage

**Type:** aoe  **Resource:** DEX-SP  **Cost:** 18  **Unlock Level:** 5

**Description (shown to player):** Rapid volley of arrows at all enemies.

**Mechanical fields:** `power: 1.0`

**What the code actually does:**
> Hits all living enemies; magic or physical determined by resource type; no per-target accuracy roll

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True, is_aoe=True
# aoe_targets = all living enemies
for tgt in aoe_targets:
    _apply_physical_hit(tgt, power=1.0)  # element=physical
```

**Analysis:** ✓ Matches description

---

### ✓ Nature's Balm

**Type:** heal  **Resource:** WIS-MP  **Cost:** 14  **Unlock Level:** 5

**Description (shown to player):** Herbal remedy. Heals and cures poison.

**Mechanical fields:** `power: 1.0`, `cures: poison`

**What the code actually does:**
> Heals single ally; crit possible; if target is down, revives them at 0 then heals

**Relevant code path:**
```python
# resolve_ability() → is_heal=True
heal_targets = [target or attacker]
amount = calc_healing(attacker, {'power': cost * 1.0})
target['hp'] = min(target['max_hp'], target['hp'] + amount)
```

**Analysis:** ✓ Matches description

---

### ✓ Lethal Shot

**Type:** attack  **Resource:** DEX-SP  **Cost:** 25  **Unlock Level:** 10

**Description (shown to player):** Perfect shot for massive damage.

**Mechanical fields:** `power: 2.5`

**What the code actually does:**
> Physical melee hit using attacker STR vs target DEF; applies bonus_crit, execute_threshold, stun/slow/poison on hit

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True → _apply_physical_hit(target, power=2.5)
```

**Analysis:** ✓ Matches description

---


## Monk

### ✓ Flurry of Blows

**Type:** attack  **Resource:** Ki  **Cost:** 8  **Unlock Level:** 1

**Description (shown to player):** Three rapid strikes at reduced power each.

**Mechanical fields:** `power: 0.6`, `hits: 3`

**What the code actually does:**
> Physical melee hit using attacker STR vs target DEF; applies bonus_crit, execute_threshold, stun/slow/poison on hit

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True → _apply_physical_hit(target, power=0.6)
```

**Analysis:** Says 'three rapid strikes' — POWER: 0.6 divided across 3 hits means each hit is 0.2× base; total 0.6× base

---

### ✓ Iron Skin

**Type:** buff  **Resource:** Ki  **Cost:** 10  **Unlock Level:** 1

**Description (shown to player):** Harden the body. Reduces physical damage taken for 3 turns (self only).

**Mechanical fields:** `buff: iron_skin`, `duration: 3 turns`

**What the code actually does:**
> Applies named status to self or all_allies for duration turns; mechanical effect driven by _active_buff_mods

**Relevant code path:**
```python
# resolve_ability() → is_buff=True
apply_status_effect(attacker, 'iron_skin', 3)
# Effect in _active_buff_mods():
  def_reduce += 8
```

**Analysis:** ✓ Matches description

---

### ✓ Stunning Fist

**Type:** attack  **Resource:** Ki  **Cost:** 12  **Unlock Level:** 3

**Description (shown to player):** Precise strike. 45% chance to stun.

**Mechanical fields:** `power: 1.3`, `stun: 45%`

**What the code actually does:**
> Physical melee hit using attacker STR vs target DEF; applies bonus_crit, execute_threshold, stun/slow/poison on hit

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True → _apply_physical_hit(target, power=1.3)
if random.random() < 0.45: apply_status_effect(target, 'Stunned', 1)
```

**Analysis:** ✓ Matches description

---

### ✓ Inner Peace

**Type:** heal  **Resource:** Ki  **Cost:** 15  **Unlock Level:** 5

**Description (shown to player):** Meditate to restore own HP.

**Mechanical fields:** `power: 1.2`

**What the code actually does:**
> Heals single ally; crit possible; if target is down, revives them at 0 then heals

**Relevant code path:**
```python
# resolve_ability() → is_heal=True
heal_targets = [target or attacker]
amount = calc_healing(attacker, {'power': cost * 1.2})
target['hp'] = min(target['max_hp'], target['hp'] + amount)
```

**Analysis:** ✓ Matches description

---

### ⚠ Pressure Point

**Type:** debuff  **Resource:** Ki  **Cost:** 18  **Unlock Level:** 8

**Description (shown to player):** Strike nerve clusters. Target deals 30% less damage.

**Mechanical fields:** (none beyond type handling)

**What the code actually does:**
> Magic accuracy roll; on hit applies named status for duration turns; no special mechanical modifier unless name matches _active_buff_mods

**Relevant code path:**
```python
# resolve_ability() → is_debuff=True
# magic accuracy roll → apply_status_effect(target, 'Pressure Point', )
```

**Analysis:** Says 'target deals 30% less damage' — applies a debuff status, but _active_buff_mods has no 'Pressure Point' handler; damage reduction is NOT applied

---

### ✓ Dragon Strike

**Type:** attack  **Resource:** Ki  **Cost:** 30  **Unlock Level:** 12  **Element:** fire

**Description (shown to player):** Channel ki into a devastating fire strike.

**Mechanical fields:** `power: 2.8`

**What the code actually does:**
> Physical melee hit using attacker STR vs target DEF; applies bonus_crit, execute_threshold, stun/slow/poison on hit

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True → _apply_physical_hit(target, power=2.8)
```

**Analysis:** ✓ Matches description

---


## Knight

### ✓ Heavy Strike

**Type:** attack  **Resource:** STR-SP  **Cost:** 12  **Unlock Level:** 1

**Description (shown to player):** Powerful armored blow dealing heavy physical damage.

**Mechanical fields:** `power: 1.7`

**What the code actually does:**
> Physical melee hit using attacker STR vs target DEF; applies bonus_crit, execute_threshold, stun/slow/poison on hit

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True → _apply_physical_hit(target, power=1.7)
```

**Analysis:** ✓ Matches description

---

### ✓ Bulwark

**Type:** buff  **Resource:** STR-SP  **Cost:** 10  **Unlock Level:** 1

**Description (shown to player):** Full defensive stance — absorb the next attack for an ally.

**Mechanical fields:** `buff: bulwark`, `duration: 3 turns`

**What the code actually does:**
> Applies named status to self or all_allies for duration turns; mechanical effect driven by _active_buff_mods

**Relevant code path:**
```python
# resolve_ability() → is_buff=True
apply_status_effect(attacker, 'bulwark', 3)
# Effect in _active_buff_mods():
  absorb next physical hit entirely (self only)
```

**Analysis:** Says 'absorb next attack for an ally' — absorbs ONE hit for whichever combatant has the buff (self-only); 'for an ally' is misleading

---

### ✓ Challenge

**Type:** taunt  **Resource:** STR-SP  **Cost:** 8  **Unlock Level:** 3

**Description (shown to player):** Force an enemy to target you for 2 turns.

**Mechanical fields:** (none beyond type handling)

**What the code actually does:**
> Applies Taunted status and sets taunt_target_uid on enemy

**Relevant code path:**
```python
# resolve_ability() → is_taunt=True
apply_status_effect(target, 'Taunted', 2)
target['taunt_target_uid'] = attacker['uid']
```

**Analysis:** ✓ Matches description

---

### ✓ Armor Crush

**Type:** attack  **Resource:** STR-SP  **Cost:** 16  **Unlock Level:** 5

**Description (shown to player):** Strike reduces enemy defense by 4 permanently.

**Mechanical fields:** `power: 1.4`, `armor shred: -4 DEF permanently`

**What the code actually does:**
> Physical melee hit using attacker STR vs target DEF; applies bonus_crit, execute_threshold, stun/slow/poison on hit

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True → _apply_physical_hit(target, power=1.4)
```

**Analysis:** ✓ Matches description

---

### ✓ Rally

**Type:** buff  **Resource:** STR-SP  **Cost:** 20  **Unlock Level:** 8  **Targets:** all_allies

**Description (shown to player):** Inspire party — all allies deal bonus damage for 3 turns.

**Mechanical fields:** `buff: rally`, `duration: 3 turns`

**What the code actually does:**
> Applies named status to self or all_allies for duration turns; mechanical effect driven by _active_buff_mods

**Relevant code path:**
```python
# resolve_ability() → is_buff=True
apply_status_effect(all_players, 'rally', 3)
# Effect in _active_buff_mods():
  atk_mult *= 1.25  # all allies
```

**Analysis:** Says 'all allies deal bonus damage' — rally is handled in _active_buff_mods at ×1.25

---

### ✓ Unbreakable

**Type:** buff  **Resource:** STR-SP  **Cost:** 35  **Unlock Level:** 10

**Description (shown to player):** Become virtually invincible for 2 turns. Survive any hit with at least 1 HP.

**Mechanical fields:** `buff: unbreakable`, `duration: 2 turns`

**What the code actually does:**
> Applies named status to self or all_allies for duration turns; mechanical effect driven by _active_buff_mods

**Relevant code path:**
```python
# resolve_ability() → is_buff=True
apply_status_effect(attacker, 'unbreakable', 2)
# Effect in _active_buff_mods():
  def_reduce += 20; survive fatal hit at 1 HP
```

**Analysis:** ✓ Matches description

---


## Warder

### ✓ Holy Blade

**Type:** attack  **Resource:** STR-SP  **Cost:** 14  **Unlock Level:** 8  **Element:** divine

**Description (shown to player):** Weapon infused with holy energy. Bonus vs corrupted.

**Mechanical fields:** `power: 1.6`

**What the code actually does:**
> Physical melee hit using attacker STR vs target DEF; applies bonus_crit, execute_threshold, stun/slow/poison on hit

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True → _apply_physical_hit(target, power=1.6)
```

**Analysis:** ✓ Matches description

---

### ✓ Lay on Hands

**Type:** heal  **Resource:** PIE-MP  **Cost:** 12  **Unlock Level:** 8

**Description (shown to player):** Channel divine energy to restore an ally's HP.

**Mechanical fields:** `power: 1.5`

**What the code actually does:**
> Heals single ally; crit possible; if target is down, revives them at 0 then heals

**Relevant code path:**
```python
# resolve_ability() → is_heal=True
heal_targets = [target or attacker]
amount = calc_healing(attacker, {'power': cost * 1.5})
target['hp'] = min(target['max_hp'], target['hp'] + amount)
```

**Analysis:** ✓ Matches description

---

### ✓ Warden's Mark

**Type:** debuff  **Resource:** PIE-MP  **Cost:** 10  **Unlock Level:** 9

**Description (shown to player):** Mark a target — all party attacks against it deal +20% damage.

**Mechanical fields:** (none beyond type handling)

**What the code actually does:**
> Magic accuracy roll; on hit applies named status for duration turns; no special mechanical modifier unless name matches _active_buff_mods

**Relevant code path:**
```python
# resolve_ability() → is_debuff=True
# magic accuracy roll → apply_status_effect(target, 'Warden's Mark', )
```

**Analysis:** Says '+20% damage from all party attacks' — mark_crit_bonus field not present; mark currently only adds damage on crits, no flat +20% non-crit bonus

---

### ✓ Consecrate

**Type:** aoe  **Resource:** PIE-MP  **Cost:** 20  **Unlock Level:** 10  **Element:** divine

**Description (shown to player):** Holy fire damages all enemies. Bonus vs undead/shadow.

**Mechanical fields:** `power: 1.4`

**What the code actually does:**
> Hits all living enemies; magic or physical determined by resource type; no per-target accuracy roll

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True, is_aoe=True
# aoe_targets = all living enemies
for tgt in aoe_targets:
    _apply_magic_hit(tgt, power=1.4)  # element=divine
```

**Analysis:** ✓ Matches description

---

### ✓ Divine Shield

**Type:** buff  **Resource:** PIE-MP  **Cost:** 25  **Unlock Level:** 12  **Targets:** all_allies

**Description (shown to player):** Surround all allies in divine light — reduce all incoming damage for 2 turns.

**Mechanical fields:** `buff: divine_shield`, `duration: 2 turns`

**What the code actually does:**
> Applies named status to self or all_allies for duration turns; mechanical effect driven by _active_buff_mods

**Relevant code path:**
```python
# resolve_ability() → is_buff=True
apply_status_effect(all_players, 'divine_shield', 2)
# Effect in _active_buff_mods():
  def_reduce += 12
```

**Analysis:** ✓ Matches description

---


## Paladin

### ✓ Crusader Strike

**Type:** attack  **Resource:** STR-SP  **Cost:** 15  **Unlock Level:** 8  **Element:** divine

**Description (shown to player):** Holy-blessed melee attack. Extra damage vs undead.

**Mechanical fields:** `power: 1.8`

**What the code actually does:**
> Physical melee hit using attacker STR vs target DEF; applies bonus_crit, execute_threshold, stun/slow/poison on hit

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True → _apply_physical_hit(target, power=1.8)
```

**Analysis:** ✓ Matches description

---

### ✓ Remove Curse

**Type:** cure  **Resource:** PIE-MP  **Cost:** 18  **Unlock Level:** 8

**Description (shown to player):** Lay on hands to lift a curse from one ally, freeing any cursed equipment they wear.

**Mechanical fields:** `cures: curse`

**What the code actually does:**
> Removes matching status from target; Remove Curse also lifts cursed equipment

**Relevant code path:**
```python
# resolve_ability() → is_cure=True
# Removes 'curse' status from target
# Also lifts curse_lifted flag on equipped cursed items
```

**Analysis:** ✓ Matches description

---

### ✓ Aura of Courage

**Type:** buff  **Resource:** PIE-MP  **Cost:** 18  **Unlock Level:** 8  **Targets:** all_allies

**Description (shown to player):** Holy aura — party immune to Fear and Confusion for 4 turns.

**Mechanical fields:** `buff: courage_aura`, `duration: 4 turns`

**What the code actually does:**
> Applies named status to self or all_allies for duration turns; mechanical effect driven by _active_buff_mods

**Relevant code path:**
```python
# resolve_ability() → is_buff=True
apply_status_effect(all_players, 'courage_aura', 4)
# Effect in _active_buff_mods():
  no mechanical effect — status only, fear/confusion not in system
```

**Analysis:** ✓ Matches description

---

### ✓ Judgment

**Type:** attack  **Resource:** PIE-MP  **Cost:** 20  **Unlock Level:** 9  **Element:** divine

**Description (shown to player):** Holy judgment on a singled-out enemy. Massive divine damage.

**Mechanical fields:** `power: 2.2`

**What the code actually does:**
> Physical melee hit using attacker STR vs target DEF; applies bonus_crit, execute_threshold, stun/slow/poison on hit

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True → _apply_magic_hit(target, power=2.2)
```

**Analysis:** ✓ Matches description

---

### ⚠ Holy Nova

**Type:** aoe  **Resource:** PIE-MP  **Cost:** 28  **Unlock Level:** 11  **Element:** divine

**Description (shown to player):** Radiant explosion. Damages all enemies, heals all allies.

**Mechanical fields:** `power: 1.6`

**What the code actually does:**
> Hits all living enemies; magic or physical determined by resource type; no per-target accuracy roll

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True, is_aoe=True
# aoe_targets = all living enemies
for tgt in aoe_targets:
    _apply_magic_hit(tgt, power=1.6)  # element=divine
```

**Analysis:** Says 'damages all enemies AND heals all allies' — typed as aoe, not aoe+heal; only damages enemies, heal half is NOT implemented

---

### ✓ Resurrection

**Type:** revive  **Resource:** PIE-MP  **Cost:** 40  **Unlock Level:** 13

**Description (shown to player):** Revive a fallen ally at 50% HP.

**Mechanical fields:** `revive at 50% HP`

**What the code actually does:**
> Sets first fallen ally alive=True at revive_hp_pct * max_hp

**Relevant code path:**
```python
# resolve_ability() → is_revive=True
target['alive'] = True
target['hp'] = int(target['max_hp'] * 0.5)
```

**Analysis:** Correctly revives at 50% HP — matches code

---


## Assassin

### ⚠ Shadow Step

**Type:** buff  **Resource:** DEX-SP  **Cost:** 12  **Unlock Level:** 8

**Description (shown to player):** Teleport behind a target — next attack is a guaranteed backstab.

**Mechanical fields:** `buff: shadow_step`

**What the code actually does:**
> Applies named status to self or all_allies for duration turns; mechanical effect driven by _active_buff_mods

**Relevant code path:**
```python
# resolve_ability() → is_buff=True
apply_status_effect(attacker, 'shadow_step', )
# Effect in _active_buff_mods():
  atk_mult *= 1.50  # NOT a guaranteed crit
```

**Analysis:** Says 'next attack is a guaranteed backstab' — applies the shadow_step buff (×1.50 damage) but does NOT guarantee a crit; backstab guarantee is not implemented

---

### ✓ Crippling Strike

**Type:** attack  **Resource:** DEX-SP  **Cost:** 15  **Unlock Level:** 8

**Description (shown to player):** Hamstring strike. Target speed reduced for 3 turns.

**Mechanical fields:** `power: 1.5`

**What the code actually does:**
> Physical melee hit using attacker STR vs target DEF; applies bonus_crit, execute_threshold, stun/slow/poison on hit

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True → _apply_physical_hit(target, power=1.5)
```

**Analysis:** Says 'target speed reduced for 3 turns' — applies a generic debuff; speed stat is not used in combat, so the speed reduction has no mechanical effect

---

### ⚠ Death Mark

**Type:** debuff  **Resource:** DEX-SP  **Cost:** 16  **Unlock Level:** 9

**Description (shown to player):** Mark for death — if target dies while marked, reset cooldowns.

**Mechanical fields:** (none beyond type handling)

**What the code actually does:**
> Magic accuracy roll; on hit applies named status for duration turns; no special mechanical modifier unless name matches _active_buff_mods

**Relevant code path:**
```python
# resolve_ability() → is_debuff=True
# magic accuracy roll → apply_status_effect(target, 'Death Mark', )
```

**Analysis:** Says 'if target dies while marked, reset cooldowns' — mark is applied, death-trigger cooldown reset is NOT implemented

---

### ⚠ Fan of Knives

**Type:** aoe  **Resource:** DEX-SP  **Cost:** 22  **Unlock Level:** 10

**Description (shown to player):** Rain of blades hits all enemies. Each has 20% bleed chance.

**Mechanical fields:** `power: 1.2`

**What the code actually does:**
> Hits all living enemies; magic or physical determined by resource type; no per-target accuracy roll

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True, is_aoe=True
# aoe_targets = all living enemies
for tgt in aoe_targets:
    _apply_physical_hit(tgt, power=1.2)  # element=physical
```

**Analysis:** Says '20% bleed chance on each hit' — bleed status is not in apply_poison or _inflict_special_effects for this ability; bleed chance is NOT applied

---

### ✓ Throat Cut

**Type:** attack  **Resource:** DEX-SP  **Cost:** 35  **Unlock Level:** 12

**Description (shown to player):** Attempt to silence a target. Massive damage. Silenced targets can't use abilities.

**Mechanical fields:** `power: 3.5`

**What the code actually does:**
> Physical melee hit using attacker STR vs target DEF; applies bonus_crit, execute_threshold, stun/slow/poison on hit

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True → _apply_physical_hit(target, power=3.5)
```

**Analysis:** Says 'silenced targets can't use abilities' — Silence status is not in the status effect system; no silence immunity check exists

---


## Warden

### ✓ Spirit Bond

**Type:** buff  **Resource:** WIS-MP  **Cost:** 14  **Unlock Level:** 8  **Targets:** all_allies

**Description (shown to player):** Bond party spirits — all allies share 20% of healing received.

**Mechanical fields:** `buff: spirit_bond`, `duration: 3 turns`

**What the code actually does:**
> Applies named status to self or all_allies for duration turns; mechanical effect driven by _active_buff_mods

**Relevant code path:**
```python
# resolve_ability() → is_buff=True
apply_status_effect(all_players, 'spirit_bond', 3)
# Effect in _active_buff_mods():
  atk_mult *= 1.10  # all allies
```

**Analysis:** ✓ Matches description

---

### ✓ Nature Strike

**Type:** attack  **Resource:** DEX-SP  **Cost:** 12  **Unlock Level:** 8  **Element:** nature

**Description (shown to player):** Channel nature energy — deals bonus damage to corrupted/shadow enemies.

**Mechanical fields:** `power: 1.5`

**What the code actually does:**
> Physical melee hit using attacker STR vs target DEF; applies bonus_crit, execute_threshold, stun/slow/poison on hit

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True → _apply_physical_hit(target, power=1.5)
```

**Analysis:** ✓ Matches description

---

### ✓ Fading Ward

**Type:** buff  **Resource:** PIE-MP  **Cost:** 20  **Unlock Level:** 9  **Targets:** all_allies

**Description (shown to player):** Ancient Warden ward — party gains resistance to Fading effects and shadow damage.

**Mechanical fields:** `buff: fading_ward`, `duration: 3 turns`

**What the code actually does:**
> Applies named status to self or all_allies for duration turns; mechanical effect driven by _active_buff_mods

**Relevant code path:**
```python
# resolve_ability() → is_buff=True
apply_status_effect(all_players, 'fading_ward', 3)
# Effect in _active_buff_mods():
  def_reduce += 8  # NOT shadow-specific
```

**Analysis:** Says 'resistance to Fading effects and shadow damage' — applies fading_ward buff; _active_buff_mods gives flat 8-pt damage reduction, not element-specific shadow resistance

---

### ⚠ Call of the Wild

**Type:** aoe  **Resource:** WIS-MP  **Cost:** 18  **Unlock Level:** 10  **Element:** nature

**Description (shown to player):** Summon nature's fury. Deals nature damage to all enemies, heals all allies.

**Mechanical fields:** `power: 1.3`

**What the code actually does:**
> Hits all living enemies; magic or physical determined by resource type; no per-target accuracy roll

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True, is_aoe=True
# aoe_targets = all living enemies
for tgt in aoe_targets:
    _apply_magic_hit(tgt, power=1.3)  # element=nature
```

**Analysis:** Says 'damages all enemies AND heals all allies' — typed as aoe; only damages enemies, the heal is NOT implemented

---

### ✓ Anchor the Wards

**Type:** buff  **Resource:** PIE-MP  **Cost:** 30  **Unlock Level:** 12  **Targets:** all_allies

**Description (shown to player):** Invoke old Warden magic. Party immune to status effects for 5 turns.

**Mechanical fields:** `buff: ward_anchor`, `duration: 5 turns`

**What the code actually does:**
> Applies named status to self or all_allies for duration turns; mechanical effect driven by _active_buff_mods

**Relevant code path:**
```python
# resolve_ability() → is_buff=True
apply_status_effect(all_players, 'ward_anchor', 5)
# Effect in _active_buff_mods():
  def_reduce += 6
```

**Analysis:** ✓ Matches description

---


## Spellblade

### ✓ Arcane Edge

**Type:** attack  **Resource:** INT-MP  **Cost:** 14  **Unlock Level:** 8  **Element:** arcane

**Description (shown to player):** Imbue blade with arcane energy — magical melee strike ignores physical defense.

**Mechanical fields:** `power: 1.8`

**What the code actually does:**
> Physical melee hit using attacker STR vs target DEF; applies bonus_crit, execute_threshold, stun/slow/poison on hit

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True → _apply_magic_hit(target, power=1.8)
```

**Analysis:** ✓ Matches description

---

### ✓ Runic Armor

**Type:** buff  **Resource:** INT-MP  **Cost:** 12  **Unlock Level:** 8

**Description (shown to player):** Inscribe runes on armor — reduces both physical and magical damage taken.

**Mechanical fields:** `buff: runic_armor`, `duration: 4 turns`

**What the code actually does:**
> Applies named status to self or all_allies for duration turns; mechanical effect driven by _active_buff_mods

**Relevant code path:**
```python
# resolve_ability() → is_buff=True
apply_status_effect(attacker, 'runic_armor', 4)
# Effect in _active_buff_mods():
  def_reduce += 10
```

**Analysis:** ✓ Matches description

---

### ✓ Spellstrike

**Type:** attack  **Resource:** INT-MP  **Cost:** 20  **Unlock Level:** 9  **Element:** arcane

**Description (shown to player):** Deliver a spell through your weapon — melee hit triggers a bonus arcane explosion.

**Mechanical fields:** `power: 2.0`

**What the code actually does:**
> Physical melee hit using attacker STR vs target DEF; applies bonus_crit, execute_threshold, stun/slow/poison on hit

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True → _apply_magic_hit(target, power=2.0)
```

**Analysis:** ✓ Matches description

---

### ⚠ Blade Barrier

**Type:** buff  **Resource:** INT-MP  **Cost:** 22  **Unlock Level:** 10

**Description (shown to player):** Rotating blades of arcane force. Reflect 25% of incoming damage.

**Mechanical fields:** `buff: blade_barrier`, `duration: 2 turns`

**What the code actually does:**
> Applies named status to self or all_allies for duration turns; mechanical effect driven by _active_buff_mods

**Relevant code path:**
```python
# resolve_ability() → is_buff=True
apply_status_effect(attacker, 'blade_barrier', 2)
# Effect in _active_buff_mods():
  absorb next hit; reflect_pct NOT implemented
```

**Analysis:** Says 'reflect 25% of incoming damage' — reflect_pct field exists in ability data but _apply_physical_hit/_apply_magic_hit have no reflect logic; reflection is NOT implemented

---

### ✓ Annihilate

**Type:** attack  **Resource:** INT-MP  **Cost:** 40  **Unlock Level:** 12  **Element:** arcane

**Description (shown to player):** Total arcane destruction channeled through the blade. Ignores all defenses.

**Mechanical fields:** `power: 3.2`

**What the code actually does:**
> Physical melee hit using attacker STR vs target DEF; applies bonus_crit, execute_threshold, stun/slow/poison on hit

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True → _apply_magic_hit(target, power=3.2)
```

**Analysis:** Says 'ignores all defenses' — typed as offensive arcane attack; no armor-bypass flag, uses standard _apply_magic_hit which DOES apply magic defense

---


## Templar

### ✓ Holy Wrath

**Type:** attack  **Resource:** PIE-MP  **Cost:** 16  **Unlock Level:** 8  **Element:** divine

**Description (shown to player):** Armored charge infused with divine fire. Devastating to undead.

**Mechanical fields:** `power: 1.9`

**What the code actually does:**
> Physical melee hit using attacker STR vs target DEF; applies bonus_crit, execute_threshold, stun/slow/poison on hit

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True → _apply_magic_hit(target, power=1.9)
```

**Analysis:** ✓ Matches description

---

### ✓ Battle Prayer

**Type:** buff  **Resource:** PIE-MP  **Cost:** 14  **Unlock Level:** 8  **Targets:** all_allies

**Description (shown to player):** Short prayer before battle — all allies regenerate HP for 3 turns.

**Mechanical fields:** `buff: battle_prayer`, `duration: 3 turns`

**What the code actually does:**
> Applies named status to self or all_allies for duration turns; mechanical effect driven by _active_buff_mods

**Relevant code path:**
```python
# resolve_ability() → is_buff=True
apply_status_effect(all_players, 'battle_prayer', 3)
# Effect in _active_buff_mods():
  def_reduce += 4; heals ~8% max_hp per round
```

**Analysis:** ✓ Matches description

---

### ✓ Smite Evil

**Type:** attack  **Resource:** PIE-MP  **Cost:** 18  **Unlock Level:** 9  **Element:** divine

**Description (shown to player):** Overwhelming holy force. 50% bonus damage vs undead and shadow-touched.

**Mechanical fields:** `power: 2.4`

**What the code actually does:**
> Physical melee hit using attacker STR vs target DEF; applies bonus_crit, execute_threshold, stun/slow/poison on hit

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True → _apply_magic_hit(target, power=2.4)
```

**Analysis:** Says '50% bonus damage vs undead and shadow-touched' — typed as offensive spell; no enemy-type check, deals flat power regardless of enemy type

---

### ✓ Shield of Faith

**Type:** buff  **Resource:** PIE-MP  **Cost:** 20  **Unlock Level:** 10  **Targets:** all_allies

**Description (shown to player):** Divine protection — reduce all incoming damage by 30% for 3 turns.

**Mechanical fields:** `buff: shield_of_faith`, `duration: 3 turns`

**What the code actually does:**
> Applies named status to self or all_allies for duration turns; mechanical effect driven by _active_buff_mods

**Relevant code path:**
```python
# resolve_ability() → is_buff=True
apply_status_effect(all_players, 'shield_of_faith', 3)
# Effect in _active_buff_mods():
  def_reduce += 14
```

**Analysis:** ✓ Matches description

---

### ✓ Holy Avenger

**Type:** attack  **Resource:** PIE-MP  **Cost:** 35  **Unlock Level:** 13  **Element:** divine

**Description (shown to player):** Empowered holy strike. On kill, triggers holy explosion hitting all enemies.

**Mechanical fields:** `power: 2.8`

**What the code actually does:**
> Physical melee hit using attacker STR vs target DEF; applies bonus_crit, execute_threshold, stun/slow/poison on hit

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True → _apply_magic_hit(target, power=2.8)
```

**Analysis:** Says 'on kill, triggers holy explosion hitting all enemies' — no on-kill trigger implemented; deals flat power to single target only

---


## Champion

### ✓ Titanfall

**Type:** attack  **Resource:** STR-SP  **Cost:** 20  **Unlock Level:** 15

**Description (shown to player):** Gravity-assisted leap strike. 50% stun.

**Mechanical fields:** `power: 2.5`, `stun: 50%`

**What the code actually does:**
> Physical melee hit using attacker STR vs target DEF; applies bonus_crit, execute_threshold, stun/slow/poison on hit

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True → _apply_physical_hit(target, power=2.5)
if random.random() < 0.5: apply_status_effect(target, 'Stunned', 1)
```

**Analysis:** ✓ Matches description

---

### ✓ Last Stand

**Type:** passive  **Resource:** STR-SP  **Cost:** 0  **Unlock Level:** 15

**Description (shown to player):** Below 25% HP — deal double damage.

**Mechanical fields:** (none beyond type handling)

**What the code actually does:**
> NOT handled — falls through to is_offensive block, treated as a physical attack

**Relevant code path:**
```python
# ⚠ TYPE='passive' — no passive handler in resolve_ability()
# Falls through to is_offensive=True → attempts physical attack
# These should be always-on modifiers, not usable actions
```

**Analysis:** Typed as 'passive' — passive types fall through to is_offensive; if used as an active ability it would attempt an attack. Correct behavior is passive-only; should not appear in action menu

---

### ✓ Whirlwind

**Type:** aoe  **Resource:** STR-SP  **Cost:** 30  **Unlock Level:** 16

**Description (shown to player):** Spinning blade attack hitting every enemy.

**Mechanical fields:** `power: 1.8`

**What the code actually does:**
> Hits all living enemies; magic or physical determined by resource type; no per-target accuracy roll

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True, is_aoe=True
# aoe_targets = all living enemies
for tgt in aoe_targets:
    _apply_physical_hit(tgt, power=1.8)  # element=physical
```

**Analysis:** ✓ Matches description

---

### ✓ Blade Storm

**Type:** aoe  **Resource:** STR-SP  **Cost:** 45  **Unlock Level:** 18

**Description (shown to player):** Unstoppable flurry — hits every enemy twice.

**Mechanical fields:** `power: 2.2`, `hits: 2`

**What the code actually does:**
> Hits all living enemies; magic or physical determined by resource type; no per-target accuracy roll

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True, is_aoe=True
# aoe_targets = all living enemies
for tgt in aoe_targets:
    _apply_physical_hit(tgt, power=2.2)  # element=physical
```

**Analysis:** Says 'hits every enemy twice' — implemented correctly: hits=2 with AOE

---

### ✓ Conqueror

**Type:** buff  **Resource:** STR-SP  **Cost:** 50  **Unlock Level:** 20

**Description (shown to player):** Legendary form — max damage on all attacks for 5 turns.

**Mechanical fields:** `buff: conqueror`, `duration: 5 turns`

**What the code actually does:**
> Applies named status to self or all_allies for duration turns; mechanical effect driven by _active_buff_mods

**Relevant code path:**
```python
# resolve_ability() → is_buff=True
apply_status_effect(attacker, 'conqueror', 5)
# Effect in _active_buff_mods():
  atk_mult *= 2.00  # self
```

**Analysis:** Says 'max damage on all attacks' — applies conqueror buff at ×2.00 multiplier; 'max damage' is interpreted as double damage, which is correct

---


## Archmage

### ⚠ Spell Mastery

**Type:** passive  **Resource:** INT-MP  **Cost:** 0  **Unlock Level:** 15

**Description (shown to player):** All spells cost 25% less and deal 25% more damage.

**Mechanical fields:** (none beyond type handling)

**What the code actually does:**
> NOT handled — falls through to is_offensive block, treated as a physical attack

**Relevant code path:**
```python
# ⚠ TYPE='passive' — no passive handler in resolve_ability()
# Falls through to is_offensive=True → attempts physical attack
# These should be always-on modifiers, not usable actions
```

**Analysis:** Typed as 'passive' — same issue as Last Stand; falls through to is_offensive if activated. Also, the stated 25% cost reduction is NOT applied in the resource cost block

---

### ✓ Time Stop

**Type:** buff  **Resource:** INT-MP  **Cost:** 50  **Unlock Level:** 15  **Targets:** all_enemies

**Description (shown to player):** Freeze time — all enemies skip their next turn.

**Mechanical fields:** `buff: time_stop`, `duration: 1 turns`

**What the code actually does:**
> Applies named status to self or all_allies for duration turns; mechanical effect driven by _active_buff_mods

**Relevant code path:**
```python
# resolve_ability() → is_buff=True
apply_status_effect(attacker, 'time_stop', 1)
# Effect in _active_buff_mods():
  all enemies skip their turn while status active
```

**Analysis:** ✓ Matches description

---

### ✓ Arcane Torrent

**Type:** aoe  **Resource:** INT-MP  **Cost:** 35  **Unlock Level:** 16  **Element:** arcane

**Description (shown to player):** Wave of pure arcane annihilation.

**Mechanical fields:** `power: 2.0`

**What the code actually does:**
> Hits all living enemies; magic or physical determined by resource type; no per-target accuracy roll

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True, is_aoe=True
# aoe_targets = all living enemies
for tgt in aoe_targets:
    _apply_magic_hit(tgt, power=2.0)  # element=arcane
```

**Analysis:** Correctly implemented as AOE arcane attack

---

### ⚠ Wish

**Type:** special  **Resource:** INT-MP  **Cost:** 80  **Unlock Level:** 18

**Description (shown to player):** Bend reality — fully heal the party, or deal maximum damage to all enemies.

**Mechanical fields:** (none beyond type handling)

**What the code actually does:**
> NOT handled — falls through to is_offensive block, treated as a physical attack

**Relevant code path:**
```python
# ⚠ TYPE='special' — no special handler in resolve_ability()
# Falls through to is_offensive=True → treated as physical attack
# Unique effect described ("Bend reality — fully heal the party, or deal maximum damage ") is NOT implemented
```

**Analysis:** Typed as 'special' — special types fall through to is_offensive; cast as an attack with no special branching. Dual-mode behavior (heal party OR nuke all) is NOT implemented

---


## High Priest

### ⚠ Mass Resurrection

**Type:** revive  **Resource:** PIE-MP  **Cost:** 60  **Unlock Level:** 15

**Description (shown to player):** Revive all fallen allies at 30% HP.

**Mechanical fields:** `revive at 30% HP`

**What the code actually does:**
> Sets first fallen ally alive=True at revive_hp_pct * max_hp

**Relevant code path:**
```python
# resolve_ability() → is_revive=True
target['alive'] = True
target['hp'] = int(target['max_hp'] * 0.3)
# ⚠ BUG: code uses next() — only revives FIRST fallen ally, not all
```

**Analysis:** Says 'revive ALL fallen allies' — typed as revive; code only finds the first fallen ally (next()). Does NOT revive all

---

### ✓ Divine Intervention

**Type:** buff  **Resource:** PIE-MP  **Cost:** 50  **Unlock Level:** 15  **Targets:** all_allies

**Description (shown to player):** Direct divine protection — party cannot die for 3 turns (survives any hit at 1 HP).

**Mechanical fields:** `buff: divine_intervention`, `duration: 3 turns`

**What the code actually does:**
> Applies named status to self or all_allies for duration turns; mechanical effect driven by _active_buff_mods

**Relevant code path:**
```python
# resolve_ability() → is_buff=True
apply_status_effect(all_players, 'divine_intervention', 3)
# Effect in _active_buff_mods():
  def_reduce += 20; survive fatal hit at 1 HP
```

**Analysis:** ✓ Matches description

---

### ✓ Holy Word

**Type:** aoe  **Resource:** PIE-MP  **Cost:** 40  **Unlock Level:** 16  **Element:** divine

**Description (shown to player):** The word of light made manifest — devastating holy damage to all enemies.

**Mechanical fields:** `power: 2.5`

**What the code actually does:**
> Hits all living enemies; magic or physical determined by resource type; no per-target accuracy roll

**Relevant code path:**
```python
# resolve_ability() → is_offensive=True, is_aoe=True
# aoe_targets = all living enemies
for tgt in aoe_targets:
    _apply_magic_hit(tgt, power=2.5)  # element=divine
```

**Analysis:** ✓ Matches description

---

### ⚠ Miracle

**Type:** special  **Resource:** PIE-MP  **Cost:** 70  **Unlock Level:** 18

**Description (shown to player):** Divine miracle — fully restore all party HP and MP.

**Mechanical fields:** (none beyond type handling)

**What the code actually does:**
> NOT handled — falls through to is_offensive block, treated as a physical attack

**Relevant code path:**
```python
# ⚠ TYPE='special' — no special handler in resolve_ability()
# Falls through to is_offensive=True → treated as physical attack
# Unique effect described ("Divine miracle — fully restore all party HP and MP.") is NOT implemented
```

**Analysis:** Typed as 'special' — same issue as Wish; treated as offensive. Full party HP+MP restore is NOT implemented

---

