# REALM OF SHADOWS — GAME BIBLE
**Master Design Reference** | Last updated: 2026-03-08

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
Each requires base stats meeting minimum thresholds.

| Hybrid Class  | Base Class | Key Stat Requirements |
|---------------|------------|-----------------------|
| Paladin       | Fighter    | PIE ≥ 14              |
| Spellblade    | Fighter    | INT ≥ 14              |
| Warder        | Fighter    | DEX ≥ 14              |
| Strider       | Fighter    | DEX ≥ 13              |
| Guardian      | Fighter    | CON ≥ 20              |
| Witch         | Mage       | WIS ≥ 14, PIE ≥ 12    |
| Necromancer   | Mage       | INT ≥ 16              |
| Druid         | Mage       | WIS ≥ 16              |
| Mystic        | Mage       | INT ≥ 14, WIS ≥ 12    |
| Warden (class)| Cleric     | WIS ≥ 14, PIE ≥ 12    |
| Inquisitor    | Cleric     | DEX ≥ 12, PIE ≥ 14    |
| Templar       | Cleric     | CON ≥ 14, PIE ≥ 12    |
| Assassin      | Thief      | DEX ≥ 16              |
| Phantom       | Thief      | WIS ≥ 12              |
| Shaman        | Ranger     | WIS ≥ 14              |

### Apex Classes (6) — Level 15 Transitions (Game 2 milestone)
Knight (Fighter), Archmage (Mage), High Priest (Cleric),
Shadow Master (Thief), Beastlord (Ranger), Ascetic (Monk)

### How Transitions Work
- `apply_class_transition(character, class_name)` in `core/progression.py`
- Validates: base class match, level gate, stat minimums
- Preserves all known abilities, adds new starting abilities
- Guild screen (VIEW_CLASSTREE) shows clickable transition buttons
- Trainer NPCs in Briarhollow and Ironhearth explain the system

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
- **WIS duration reduction**: Mind debuffs (Fear, Slow, Stun, Silence, Charm...) reduced by 1 turn per 8 WIS above 10

---

## 4. TRILOGY STRUCTURE

### Game 1 — Mortal Plane (current)
**"Fix the wound."** 5 Hearthstones scattered across 10 dungeons. The Fading tears the land.
Governor Valdris secretly orchestrates it to seize power. Maren is an ally from the outset.
Party ends ~L10–11, Warden-Commander rank. Apex classes (L15) are a teaser for Game 2.

### Game 2 — Five Elemental Planes (planned)
**"Chase the cause."** The Fading had a deeper source — a wound between planes.
Bronze→Iron tier arc. Apex classes become the L15 milestone. Five plane-themed dungeons.

### Game 3 — Shadow Plane (planned)
**"Enter the source."** Iron→Steel tier. The true nature of the Shadow is revealed.

---

## 5. NARRATIVE OVERVIEW

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
Her confession dialogue (post Spider's Nest) reveals Valdris' Spire location.

### Hearthstone Fragments (5)
| Fragment | Dungeon               | Notes                                |
|----------|-----------------------|--------------------------------------|
| 1        | Abandoned Mine        | Act 1 culmination                    |
| 2        | Sunken Crypt          | Revealed after Ruins of Ashenmoor    |
| 3        | Dragon's Tooth        | Act 2, volcanic island               |
| 4        | Pale Coast            | Act 2, coastal dungeon               |
| 5        | Windswept Isle        | Act 2, sea crossing required         |
Final: Hearthstone restoration at Valdris' Spire (Act 3 climax).

---

## 6. WORLD STRUCTURE

8 walkable towns: Briarhollow (starting village), Woodhaven (ranger), Ironhearth (dwarven),
Greenwood (forest), Saltmere (coastal), Sanctum (holy city), Crystalspire (mage city), Thornhaven (capital).

10 dungeons: Goblin Warren, Spider's Nest, Abandoned Mine, Ruins of Ashenmoor,
Dragon's Tooth, Pale Coast, Wailing Tomb, Thornhaven Sewers, Forsaken Temple, Valdris' Spire.

---

## 7. COMBAT SYSTEM

Turn-based, row-based (Front/Mid/Back). Initiative from DEX + speed.
Physical damage: STR × power × type modifiers. Magic damage: INT or PIE × power × element modifiers.
Status effects: Poison (CON resist), Disease (CON resist), Fear/Stun/Slow (PIE/WIS resist).
Relics: stack `healing_received_bonus` and `fear_resist_bonus` on top of stat scaling.

### AI Types
- **random**: picks random target
- **aggressive**: highest-threat target + 30% chance to use offensive ability
- **defensive**: targets lowest-HP player (finish them off)
- **tactical**: smart targeting + ability use when outnumbered
- **supportive**: heal allies first, then offensive ability, then attack
- **boss**: buff allies → smart targeting (phases handled separately)

---

## 8. ITEM SYSTEM

### Rarity Tiers
Common → Uncommon → Rare → Legendary

### Key Item Types
- **Training books**: Permanently +1 to a stat. Drop from dungeon bosses (15% chance), found in deep secret rooms.
- **Relics / Religious items**: Accessories with PIE/fear resist or healing bonuses.
- **Panacea**: Rare consumable. Cures both Poison and Disease. Available at Sanctum and Thornhaven shops.
- **Hearthstone Fragments**: Key items. Story-critical. Boss-guaranteed drops.

---

## 9. DESIGN PRINCIPLES

1. **Exploration is rewarded.** High WIS = better loot from chests. Secret doors detected by WIS. INT unlocks enemy info.
2. **Stats have personality.** PIE = faith and the divine (discounts at temples, fear resist). WIS = clarity of mind (duration reduction, trap sense). Not just damage numbers.
3. **Dual progression.** Level up *and* Warden rank up. Both matter. Both are visible.
4. **No filler.** Every dungeon has a story hook. Every town has a named NPC with something to say.
5. **One plane per game.** Game 1 = mortal plane only. The Five Planes are a promise, not a distraction.
