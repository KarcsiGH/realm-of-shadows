# REALM OF SHADOWS — GAME BIBLE
**Master Design Reference** | Last updated: 2026-04-04

This document captures the highest-level design decisions for the game. It exists
so that no critical design intent is ever lost between sessions. When in doubt,
this document is the authority.

---

## 1. POWER TIERS (Warden Rank / Planar Tier)

Characters have **two progression axes**: a numeric level (1–30) and a **Warden Rank** (planar tier).
The rank represents standing within the Warden order and grants passive stat bonuses.

### Warden Rank Ladder
| Rank              | Tier # | All-Stat Bonus | Other Bonuses              | Unlock Condition           |
|-------------------|--------|----------------|----------------------------|----------------------------|
| Initiate          | 0      | +0             | —                          | Default                    |
| Scout             | 1      | +1 all stats   | +5% XP                     | Hearthstone 1 recovered    |
| Warden            | 2      | +2 all stats   | +5% HP, +10% XP            | Hearthstone 3 recovered    |
| Senior Warden     | 3      | +4 all stats   | +10% HP, +5% dmg, +15% XP  | Hearthstone 5 recovered    |
| Warden-Commander  | 4      | +6 all stats   | +15% HP, +10% dmg          | Valdris defeated           |

These bonuses apply to ALL stats via `effective_stats()`.

### Planar Tier (Broad Classification)
| Tier     | Description |
|----------|-------------|
| Bronze   | Starting tier. All player characters begin here. |
| Iron     | Elite tier. The ceiling for mortal NPCs on Game 1 plane. |
| Steel    | Legendary tier. Unreachable by players in Game 1. |
| Silver   | Mythic tier. Heroes of legend, demigods. |
| Gold     | Divine tier. Minor gods, avatars. |
| Platinum | Transcendent tier. Greater gods. |
| Diamond  | Absolute tier. The foundations of reality itself. |

**Players in Game 1 are Bronze tier.** Iron-tier NPCs have narrative immunity to direct Bronze combat.

---

## 2. CLASS SYSTEM (27 Classes)

### Base Classes (6) — Level 1+
Fighter, Mage, Cleric, Thief, Ranger, Monk

### Hybrid Classes (15) — Level 10 Transitions
Each hybrid class requires two specific base classes in the party (one character
must be each base class) AND stat minimums on the transitioning character.

| Hybrid Class   | Base Classes           | Key Stat Requirements     |
|----------------|------------------------|---------------------------|
| Paladin        | Fighter + Cleric       | PIE ≥ 14                  |
| Spellblade     | Fighter + Mage         | INT ≥ 14                  |
| Warder         | Fighter + Thief        | DEX ≥ 14                  |
| Strider        | Fighter + Ranger       | DEX ≥ 13                  |
| Guardian       | Fighter + Monk         | CON ≥ 20                  |
| Witch          | Mage + Cleric          | WIS ≥ 14, PIE ≥ 12        |
| Necromancer    | Mage + Thief           | INT ≥ 16                  |
| Druid          | Mage + Ranger          | WIS ≥ 16                  |
| Mystic         | Mage + Monk            | INT ≥ 14, WIS ≥ 12        |
| Warden (class) | Cleric + Ranger        | WIS ≥ 14, PIE ≥ 12        |
| Inquisitor     | Cleric + Thief         | DEX ≥ 12, PIE ≥ 14        |
| Templar        | Cleric + Monk          | CON ≥ 14, PIE ≥ 12        |
| Assassin       | Ranger + Thief         | DEX ≥ 16                  |
| Phantom        | Thief + Monk           | WIS ≥ 12                  |
| Shaman         | Ranger + Monk          | WIS ≥ 14                  |

### Apex Classes (6) — Level 15 Transitions
Reachable in late Game 1 for completionists; full showcase in Game 2.

| Apex Class   | Base Class |
|--------------|------------|
| Knight       | Fighter    |
| Archmage     | Mage       |
| High Priest  | Cleric     |
| Shadow Master| Thief      |
| Beastlord    | Ranger     |
| Ascetic      | Monk       |

### How Transitions Work
- `apply_class_transition(character, class_name)` in `core/progression.py`
- Validates: base class match, level gate, stat minimums
- Preserves all known abilities; adds new class starting abilities
- Entry point: Guild → **"Choose Advanced Class ✦"** card (VIEW_CLASS_CHOOSE)
  — a full-screen selection UI with class cards, stat requirement display,
  ability preview, close button, and a two-pass draw order (selected card
  always renders on top of collapsed cards below it)
- Also accessible from View Abilities → classtree transition bar
- Warden Liaison dialogue explains the system and awards rank badges

---

## 3. STAT SYSTEM

| Stat | Primary Effect | Secondary Effects |
|------|----------------|-------------------|
| STR  | Physical damage | — |
| DEX  | Accuracy, initiative | Trap detect/disarm bonus |
| CON  | Defense, HP | Poison/disease resist (+2%/pt above 10) |
| INT  | Mage casting stat | Enemy recognition (INT≥14), universal ID (INT≥10), minor magic resist |
| WIS  | Ki/Ranger accuracy | Magic resist (×0.5), mind-effect duration reduction (−1 per 8 WIS above 10), trap detect bonus, chest loot bonus (WIS≥15), secret door detection |
| PIE  | Cleric casting stat | Heal output/received (+1.5%/pt above 10), fear resist (+2%/pt above 10), temple discounts (PIE≥15, up to 20% off), Divine Lore (PIE≥10) |

### Cross-Stat Effects (WIS/PIE Passives)
- **WIS ≥ 15**: +4% bonus item chance per WIS above 14 when opening chests (cap 40%)
- **PIE ≥ 15**: Temple and holy services discounted (2% per PIE above 14, cap 20%)
- **WIS duration reduction**: Mind debuffs (Fear, Slow, Stun, Silence, Charm…) reduced by 1 turn per 8 WIS above 10

---

## 4. XP PACING (Option C — current calibration)

Enemy XP rewards were reduced 45% and floor bonuses cut 50% to pace levelling correctly.

| Act         | Target Level Range | Key milestone                        |
|-------------|-------------------|--------------------------------------|
| Act 1 end   | L7–8              | Abandoned Mine cleared, HS 1 found   |
| Mid Act 2   | L10               | Hybrid class transitions available   |
| Act 2 end   | L12–13            | All 5 Hearthstones found             |
| Late Game 1 | L15+              | Apex classes reachable for completionists |

---

## 5. TRILOGY STRUCTURE

### Game 1 — Mortal Plane (current)
**"Fix the wound."** 5 Hearthstones scattered across 10 dungeons. The Fading tears the land.
Governor Valdris secretly orchestrates it to seize power. Maren is an ally from the outset.
Party targets L12–13 by game end. Hybrid classes unlock at L10. Apex classes (L15) are
reachable for completionists and serve as a teaser for Game 2.

### Game 2 — Five Elemental Planes (planned)
**"Chase the cause."** The Fading had a deeper source — a wound between planes.
Bronze→Iron tier arc. Apex classes become the primary L15 milestone. Five plane-themed dungeons.

### Game 3 — Shadow Plane (planned)
**"Enter the source."** Iron→Steel tier. The true nature of the Shadow is revealed.

---

## 6. NARRATIVE OVERVIEW

### The Fading
A magical blight draining life from the land. NPCs die slowly. The Hearthstones anchor
reality — once all 5 are restored to the First Hearthstone (in Valdris' Spire), the Fading
can be sealed. The Fading is not the true villain — it's a symptom of something older.

### Governor Valdris
The acting governor of Aldenmere. He is secretly using the Fading to consolidate power —
keeping Hearthstone fragments out of Warden hands so only those loyal to him survive.
His HQ is Valdris' Spire (Act 3 dungeon, revealed by Maren's confession dialogue).
Phase 3 boss fight; Phase 4 he is consumed by the Shadow itself.

### Maren
A Warden-trained scholar. Knows the truth about the Hearthstones and about Valdris.
Appears early in Briarhollow and is a recurring companion/ally throughout Act 1–2.
Her betrayal/confession arc (mid-Act 2, after multiple Hearthstones recovered) reveals
Valdris' Spire location. She has 12 conditional dialogue branches tracking full story arc.

### Hearthstone Fragments (5)
| Fragment | Dungeon        | Act | Notes                                    |
|----------|----------------|-----|------------------------------------------|
| 1        | Abandoned Mine | 1   | Act 1 culmination; requires Mine Key     |
| 2        | Sunken Crypt   | 2   | Beneath the Pale Coast                   |
| 3        | Dragon's Tooth | 2   | Volcanic island; sea passage required    |
| 4        | Pale Coast     | 2   | Coastal dungeon                          |
| 5        | Windswept Isle | 2   | Sea crossing required                    |

Final: Hearthstone restoration at Valdris' Spire (Act 3 climax).

---

## 7. WORLD STRUCTURE

### Walkable Towns (11)
| Town           | Character        | Notes                              |
|----------------|------------------|------------------------------------|
| Briarhollow    | Starting village | Maren, Captain Rowan, Bess         |
| Woodhaven      | Ranger town      | Elder Theron, Sylla, Priestess Alia|
| Ironhearth     | Dwarven forge    | Forgemaster Dunn, Miner Durk       |
| Greenwood      | Forest outpost   | Scout Feryn, Old Moss, Trapper Holt|
| Saltmere       | Coastal port     | Guildmaster Sable, Tide Priest Oran|
| Sanctum        | Holy city        | High Priest Aldara (plot-critical) |
| Crystalspire   | Mage city        | Archmage Solen, Teleport Master    |
| Thornhaven     | Capital city     | Governor Aldric, Guild Commander   |
| Emberveil      | Volcanic island  | Master Forger Renn                 |
| The Anchorage  | Sea waypoint     | Elder Vaethari                     |
| The Holdfast   | Frontier outpost | Dael Holdfast, Sarev Holdfast      |

### Dungeons (10)
| Dungeon           | Level | Act | Hearthstone | Boss                |
|-------------------|-------|-----|-------------|---------------------|
| Goblin Warren     | 1     | 1   | —           | Grak                |
| Spider's Nest     | 2     | 1   | —           | Spider Queen        |
| Abandoned Mine    | 3     | 1   | HS 1        | Warden Korrath      |
| Sunken Crypt      | 4     | 2   | HS 2        | Sunken Warden       |
| Ruins of Ashenmoor| 5     | 2   | —           | Ashvar              |
| Dragon's Tooth    | 6     | 2   | HS 3        | Karreth             |
| Pale Coast        | 7     | 2   | HS 4        | —                   |
| Windswept Isle    | 8     | 2   | HS 5        | —                   |
| Valdris' Spire    | 9     | 3   | Final       | Valdris / Shadow    |
| The Shadow Throne | 10    | 3   | —           | True Shadow form    |

**Note:** Wailing Tomb, Thornhaven Sewers, and Forsaken Temple appeared in early
design drafts but were replaced by Sunken Crypt, Windswept Isle, and The Shadow Throne.

---

## 8. COMBAT SYSTEM

Turn-based, row-based (Front/Mid/Back). Initiative from DEX + speed.
Physical damage: STR × power × type modifiers. Magic damage: INT or PIE × power × element modifiers.
Status effects: Poison (CON resist), Disease (CON resist), Fear/Stun/Slow (PIE/WIS resist).
Relics: stack `healing_received_bonus` and `fear_resist_bonus` on top of stat scaling.

**Party order in combat matches camp reorder** — `self.party` list order is authoritative.

### AI Types
- **random**: picks random target
- **aggressive**: highest-threat target + 30% chance to use offensive ability
- **defensive**: targets lowest-HP player (finish them off)
- **tactical**: smart targeting + ability use when outnumbered
- **supportive**: heal allies first, then offensive ability, then attack
- **boss**: buff allies → smart targeting (phases handled separately)

### New Ability Mechanics (added Session 18)
- `lifesteal`: heals attacker % of damage dealt
- `armor_pierce`: zeroes target defence during calc
- `hot_duration`: applies Regenerating HoT status
- `dark_bargain`: spends 15% max HP, restores MP, applies damage boost
- `death_pact`: auto-revive marker on caster
- `perfect_defense`: negate next incoming hit (ki_deflect)
- 15 new buff types in `_active_buff_mods`

---

## 9. ITEM SYSTEM

### Rarity Tiers
Common → Uncommon → Rare → Legendary

### Key Item Types
- **Training books**: Permanently +1 to a stat. Drop from dungeon bosses (15% chance), found in deep secret rooms.
- **Relics / Religious items**: Accessories with PIE/fear resist or healing bonuses.
- **Panacea**: Rare consumable. Cures both Poison and Disease. Available at Sanctum and Thornhaven shops.
- **Hearthstone Fragments**: Key items. Story-critical. Boss-guaranteed drops.
- **Mine Key**: Dropped by Spider Queen. Required to enter Abandoned Mine.

---

## 10. NPC DIALOGUE SYSTEM

All dialogue lives in `data/story_data.py` — `NPC_DIALOGUES` dict and `TOWN_NPCS` dict.

### Conditional Branch Priority
Branches are evaluated top-to-bottom; first matching condition fires.
Most-advanced story state → least-advanced → always (fallback).

### NPCs with Full Progression Awareness (as of Session 18)
The following NPCs have 3–4 conditional branches reacting to story flags:
young_tomas, old_petra, sylla, elder_theron, forgemaster_dunn, merchant_kira,
priestess_alia, miner_durk, trapper_holt, city_guard_thornhaven, barkeep_holt,
barkeep_magda, old_moss, maren (12 branches), captain_rowan, bess, warden_liaison (9 branches),
scout_feryn, archmage_solen, guildmaster_sable, dockhand_riv, innkeeper_thornhaven,
guild_commander_varek, governor_aldric, refugee_elder.

### Warden Liaison Branch Priority Order
[0] endgame (shadow_valdris defeated)
[1] rank3 (hearthstone.5)
[2] rank2 (hearthstone.3)
[3] rank1 (hearthstone.1 = mine cleared) ← must precede dungeon-completion branches
[4] ironhearth reached, spiders NOT cleared
[5] spiders cleared, mine NOT cleared ← guarded with abandoned_mine != True
[6] warren cleared, spiders not
[7] maren met, warren not
[8] fallback

---

## 11. DESIGN PRINCIPLES

1. **Exploration is rewarded.** High WIS = better loot from chests. Secret doors detected by WIS. INT unlocks enemy info.
2. **Stats have personality.** PIE = faith and the divine (discounts at temples, fear resist). WIS = clarity of mind (duration reduction, trap sense). Not just damage numbers.
3. **Dual progression.** Level up *and* Warden rank up. Both matter. Both are visible.
4. **No filler.** Every dungeon has a story hook. Every town has a named NPC with something to say.
5. **One plane per game.** Game 1 = mortal plane only. The Five Planes are a promise, not a distraction.
6. **NPCs know the world.** Every named NPC reacts to at least 2 story milestones. No static characters after Session 18.
7. **Class advancement is earned.** Hybrid classes at L10 require specific party composition AND stat thresholds. Apex at L15. The selection UI (VIEW_CLASS_CHOOSE) shows full ability preview before committing.
