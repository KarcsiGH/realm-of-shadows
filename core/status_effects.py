"""
Realm of Shadows — Status Effects System (M4)

Manages persistent status effects on characters:
- Poison (step-based DOT, timed expiry)
- Curses (persistent until cured)
- Resurrection sickness (until inn rest)
- Combat debuffs (worn off after combat)

Called by: dungeon movement, world map movement, combat engine, temple services
"""

# ═══════════════════════════════════════════════════════════════
#  STATUS EFFECT DEFINITIONS
# ═══════════════════════════════════════════════════════════════

POISON_EFFECTS = {
    "poison_weak": {
        "name": "Weak Poison", "tier": 1,
        "dmg_per_tick": 4, "tick_every_steps": 3, "total_ticks": 4,
        "save_stat": "CON", "save_threshold": 60,
    },
    "poison_strong": {
        "name": "Strong Poison", "tier": 2,
        "dmg_per_tick": 10, "tick_every_steps": 3, "total_ticks": 6,
        "save_stat": "CON", "save_threshold": 45,
    },
    "poison_deadly": {
        "name": "Deadly Poison", "tier": 3,
        "dmg_per_tick": 18, "tick_every_steps": 3, "total_ticks": 8,
        "save_stat": "CON", "save_threshold": 30,
    },
}

CURSE_EFFECTS = {
    "curse_weakness":  {"name": "Weakness",  "effect": "dmg_dealt_mult",  "value": 0.80, "tier": 2},
    "curse_fragility": {"name": "Fragility", "effect": "max_hp_mult",     "value": 0.80, "tier": 2},
    "curse_silence":   {"name": "Silence",   "effect": "no_spells",       "value": True,  "tier": 3},
    "curse_jinx":      {"name": "Jinx",      "effect": "accuracy_penalty","value": 0.85, "tier": 2},
    "curse_doom":      {"name": "Doom",       "effect": "hp_drain",       "value": 1, "drain_steps": 10, "tier": 4},
}


# ═══════════════════════════════════════════════════════════════
#  CHARACTER STATUS MANAGEMENT
# ═══════════════════════════════════════════════════════════════

def get_status_effects(character):
    """Get the status_effects list from a character, creating if needed."""
    if not hasattr(character, 'status_effects'):
        character.status_effects = []
    return character.status_effects

def has_status(character, effect_id):
    """Check if character has a specific status effect."""
    for s in get_status_effects(character):
        if s.get("id") == effect_id:
            return True
    return False

def add_poison(character, poison_id):
    """Apply a poison effect to a character. Returns True if applied."""
    if poison_id not in POISON_EFFECTS:
        return False
    pdef = POISON_EFFECTS[poison_id]
    effects = get_status_effects(character)
    # Don't stack same poison, but replace with stronger
    for i, s in enumerate(effects):
        if s.get("type") == "poison":
            old_tier = s.get("tier", 0)
            if pdef["tier"] > old_tier:
                effects[i] = {
                    "id": poison_id, "type": "poison",
                    "name": pdef["name"], "tier": pdef["tier"],
                    "dmg": pdef["dmg_per_tick"],
                    "tick_every": pdef["tick_every_steps"],
                    "ticks_left": pdef["total_ticks"],
                    "steps_since_tick": 0,
                }
                return True
            return False  # already have equal or stronger
    effects.append({
        "id": poison_id, "type": "poison",
        "name": pdef["name"], "tier": pdef["tier"],
        "dmg": pdef["dmg_per_tick"],
        "tick_every": pdef["tick_every_steps"],
        "ticks_left": pdef["total_ticks"],
        "steps_since_tick": 0,
    })
    return True

def add_curse(character, curse_id):
    """Apply a curse effect. Returns True if applied."""
    if curse_id not in CURSE_EFFECTS:
        return False
    cdef = CURSE_EFFECTS[curse_id]
    effects = get_status_effects(character)
    # Don't stack same curse
    for s in effects:
        if s.get("id") == curse_id:
            return False
    effects.append({
        "id": curse_id, "type": "curse",
        "name": cdef["name"], "tier": cdef["tier"],
        "effect": cdef["effect"], "value": cdef["value"],
        "steps_active": 0,
    })
    return True

def add_resurrection_sickness(character):
    """Apply resurrection sickness (clears at inn rest)."""
    effects = get_status_effects(character)
    for s in effects:
        if s.get("id") == "resurrection_sickness":
            return
    effects.append({
        "id": "resurrection_sickness", "type": "debuff",
        "name": "Resurrection Sickness",
        "stat_penalty_pct": 15,
    })

def remove_status(character, effect_id):
    """Remove a specific status effect."""
    effects = get_status_effects(character)
    character.status_effects = [s for s in effects if s.get("id") != effect_id]

def remove_all_poison(character):
    """Remove all poison effects."""
    effects = get_status_effects(character)
    character.status_effects = [s for s in effects if s.get("type") != "poison"]

def remove_all_curses(character):
    """Remove all curse effects."""
    effects = get_status_effects(character)
    character.status_effects = [s for s in effects if s.get("type") != "curse"]

def remove_resurrection_sickness(character):
    """Clear resurrection sickness (called on inn rest)."""
    remove_status(character, "resurrection_sickness")

def clear_all_statuses(character):
    """Nuclear option — clear everything."""
    character.status_effects = []


# ═══════════════════════════════════════════════════════════════
#  STEP-BASED TICKING (called per movement step)
# ═══════════════════════════════════════════════════════════════

def tick_step(character):
    """Process one movement step for status effects.
    Returns list of message strings describing what happened."""
    messages = []
    effects = get_status_effects(character)
    to_remove = []

    for s in effects:
        if s["type"] == "poison":
            s["steps_since_tick"] = s.get("steps_since_tick", 0) + 1
            if s["steps_since_tick"] >= s["tick_every"]:
                s["steps_since_tick"] = 0
                s["ticks_left"] -= 1
                dmg = s["dmg"]
                character.resources["HP"] = character.resources.get("HP", 0) - dmg
                messages.append(f"{character.name} takes {dmg} {s['name']} damage! ({s['ticks_left']} ticks left)")

                if character.resources["HP"] <= 0:
                    messages.append(f"{character.name} collapses from poison!")

                if s["ticks_left"] <= 0:
                    to_remove.append(s["id"])
                    messages.append(f"{character.name}'s {s['name']} wears off.")

        elif s["type"] == "curse" and s.get("effect") == "hp_drain":
            s["steps_active"] = s.get("steps_active", 0) + 1
            drain_every = s.get("drain_steps", 10)
            if s["steps_active"] % drain_every == 0:
                character.resources["HP"] = character.resources.get("HP", 0) - s["value"]
                messages.append(f"{character.name} feels the Doom curse drain their life...")

    for rid in to_remove:
        remove_status(character, rid)

    return messages


# ═══════════════════════════════════════════════════════════════
#  STATUS DISPLAY HELPERS
# ═══════════════════════════════════════════════════════════════

def get_status_display(character):
    """Return list of (name, color) for UI display."""
    display = []
    for s in get_status_effects(character):
        if s["type"] == "poison":
            display.append((s["name"], (120, 200, 50)))  # green
        elif s["type"] == "curse":
            display.append((s["name"], (180, 50, 180)))  # purple
        elif s["id"] == "resurrection_sickness":
            display.append(("Res. Sickness", (150, 150, 100)))  # tan
        elif s.get("name") == "Stun" or s.get("name") == "Stunned":
            display.append(("Stunned", (255, 220, 50)))  # yellow
        elif s.get("name") == "Frozen" or s.get("name") == "Freeze":
            display.append(("Frozen", (100, 200, 255)))  # ice blue
        elif s.get("name") == "Burning" or s.get("name") == "On Fire":
            display.append(("Burning", (255, 120, 30)))  # orange
        elif s.get("name") == "Petrified":
            display.append(("Stoned", (160, 160, 160)))  # grey
        elif s.get("name") == "Sleep":
            display.append(("Asleep", (150, 130, 200)))  # lavender
        else:
            display.append((s.get("name", "???"), (200, 200, 200)))

    # Show "Ok" if no negative statuses
    if not display:
        display.append(("Ok", (100, 200, 100)))  # green

    return display

def is_silenced(character):
    """Check if character is silenced (can't cast spells)."""
    for s in get_status_effects(character):
        if s.get("effect") == "no_spells":
            return True
    return False

def get_damage_mult(character):
    """Get damage multiplier from curses."""
    mult = 1.0
    for s in get_status_effects(character):
        if s.get("effect") == "dmg_dealt_mult":
            mult *= s["value"]
    return mult

def get_accuracy_mult(character):
    """Get accuracy multiplier from curses."""
    mult = 1.0
    for s in get_status_effects(character):
        if s.get("effect") == "accuracy_penalty":
            mult *= s["value"]
    return mult
