"""
Realm of Shadows — Character Model
"""
import random
from core.classes import (
    STAT_NAMES, CLASSES, CLASS_ORDER,
    get_all_resources, get_class_fit,
)
from core.equipment import (
    empty_equipment, STARTING_EQUIPMENT, ARMOR,
    equip_item, calc_equipment_stat_bonuses,
    calc_equipment_defense, calc_equipment_magic_resist,
    calc_equipment_speed,
)

# XP required per level: level 2 = 100, level 3 = 250, etc.
from core.progression import XP_TABLE

# Stat growth per level based on growth tier
GROWTH_AMOUNTS = {"high": (1, 2), "medium": (0, 1), "low": (0, 0)}


class Character:
    def __init__(self, name="", class_name=None, race_name="Human"):
        self.name = name
        self.class_name = class_name
        self.race_name = race_name
        self.level = 1
        self.xp = 0
        self.gold = 0
        self.inventory = []       # list of item dicts
        self.equipment = empty_equipment()
        self.stats = {s: 5 for s in STAT_NAMES}  # base before life path
        self.life_path = []       # list of event dicts chosen
        self.backstory_parts = [] # narrative snippets
        self.resources = {}
        self.abilities = []
        self.quick_rolled = False
        self.human_bonus_stat = None  # which stat the Human player boosted
        self.planar_tier = 0
        self.combat_row  = "front"   # formation position: "front" | "mid" | "back"          # Initiate(0) → Scout(1) → Warden(2) → Senior Warden(3) → Warden-Commander(4)

    def apply_stat_bonus(self, bonuses: dict):
        """Apply stat bonuses from a life path event."""
        for stat, val in bonuses.items():
            if stat in self.stats:
                self.stats[stat] += val

    def apply_random_seasoning(self):
        """Add +0 to +1 random bonus per stat after life path."""
        for stat in STAT_NAMES:
            self.stats[stat] += random.randint(0, 1)

    def quick_roll(self, class_name):
        """Skip life path: use class starting stats + small random bonus + racial mods."""
        self.class_name = class_name
        self.quick_rolled = True
        start = CLASSES[class_name]["starting_stats"]
        for stat in STAT_NAMES:
            self.stats[stat] = start[stat] + random.randint(0, 2)
        # Apply racial stat modifiers
        from core.races import apply_racial_stats
        apply_racial_stats(self.stats, self.race_name)
        self._finalize()

    def finalize_with_class(self, class_name):
        """After life path is complete, assign class and calculate everything."""
        self.class_name = class_name
        self.apply_random_seasoning()
        # Apply racial stat modifiers
        from core.races import apply_racial_stats
        apply_racial_stats(self.stats, self.race_name)
        self._finalize()

    def _finalize(self):
        """Calculate resources and assign starting abilities and equipment."""
        cls = CLASSES[self.class_name]
        self.resources = get_all_resources(self.class_name, self.stats, self.level)
        # Populate abilities from the full CLASS_ABILITIES dicts (not the stubs in CLASSES).
        # The stubs in classes.py lack type/buff/self_only fields, which breaks combat routing.
        from core.abilities import CLASS_ABILITIES as _CA
        full_lookup = {a["name"]: a for a in _CA.get(self.class_name, [])}
        self.abilities = []
        for stub in cls["starting_abilities"]:
            full = full_lookup.get(stub["name"])
            self.abilities.append(dict(full) if full else dict(stub))
        # Equip starting gear
        self.equipment = empty_equipment()
        from core.party_knowledge import mark_item_identified
        # Armor
        starting = STARTING_EQUIPMENT.get(self.class_name, {})
        for slot, armor_key in starting.items():
            if armor_key in ARMOR:
                armor_item = dict(ARMOR[armor_key])
                armor_item["identified"] = True
                self.equipment[slot] = armor_item
                mark_item_identified(armor_key)
        # Weapon
        from data.weapons import STARTING_WEAPONS, get_weapon
        weapon_key = STARTING_WEAPONS.get(self.class_name)
        if weapon_key:
            weapon_data = get_weapon(weapon_key)
            weapon_data["identified"] = True
            weapon_data["slot"] = "weapon"
            self.equipment["weapon"] = weapon_data
            mark_item_identified(weapon_key)

    def effective_stats(self):
        """Base stats + equipment bonuses + Warden rank bonus. Used for combat calculations."""
        bonuses = calc_equipment_stat_bonuses(self)
        result = {}
        for stat in STAT_NAMES:
            result[stat] = self.stats[stat] + bonuses.get(stat, 0)
        # Warden rank all_stats bonus (Scout +1, Warden +2, Senior Warden +4, Warden-Commander +6)
        from core.progression import get_tier_bonus
        flat = get_tier_bonus(getattr(self, "planar_tier", 0)).get("all_stats", 0)
        if flat:
            for stat in STAT_NAMES:
                result[stat] += flat
        return result

    def equipment_defense(self):
        """Total defense from equipped armor/shields."""
        return calc_equipment_defense(self)

    def equipment_magic_resist(self):
        """Total magic resist from equipment."""
        return calc_equipment_magic_resist(self)

    def equipment_speed(self):
        """Total speed modifier from equipment."""
        return calc_equipment_speed(self)

    def get_backstory_text(self):
        """Compile life path choices into a narrative paragraph."""
        if self.quick_rolled:
            return f"{self.name} arrived with little history to tell — a wanderer whose past is their own business."
        if not self.backstory_parts:
            return ""
        return " ".join(self.backstory_parts)

    def get_class_recommendations(self):
        """Return list of (class_name, fit_category, score) sorted by fit."""
        return get_class_fit(self.stats)

    def stat_total(self):
        return sum(self.stats.values())

    def xp_to_next_level(self):
        """XP needed for the next level."""
        return XP_TABLE.get(self.level + 1, 99999)

    def xp_progress(self):
        """Returns (current_xp, xp_needed) for progress display."""
        return self.xp, self.xp_to_next_level()

    def add_xp(self, amount):
        """Add XP (with racial multiplier + planar tier bonus). Leveling happens at the inn.
        Returns True if character is now eligible to level up."""
        from core.races import get_racial_xp_multiplier
        from core.progression import get_tier_xp_mult
        tier_mult = get_tier_xp_mult(getattr(self, "planar_tier", 0))
        adjusted = int(amount * get_racial_xp_multiplier(self.race_name) * tier_mult)
        self.xp += adjusted
        return self.xp >= self.xp_to_next_level() and self.level < 30
        self.xp += adjusted
        return self.xp >= self.xp_to_next_level() and self.level < 30

    def _level_up(self):
        """DEPRECATED — use core.progression.apply_level_up instead.
        Kept for backwards compatibility but should not be called."""
        pass

    def add_gold(self, amount):
        self.gold += amount

    def add_item(self, item):
        """Add an item to inventory. Stackable items merge. Mundane items auto-identify."""
        # Auto-identify non-magical items (pelts, common weapons, materials, etc.)
        from core.identification import auto_identify_mundane
        auto_identify_mundane(item)

        if _is_stackable(item):
            # Find existing stack of same name
            for inv_item in self.inventory:
                if inv_item.get("name") == item.get("name") and _is_stackable(inv_item):
                    inv_item["stack"] = inv_item.get("stack", 1) + item.get("stack", 1)
                    return
        # No existing stack or not stackable — add as new entry
        if _is_stackable(item) and "stack" not in item:
            item["stack"] = 1
        self.inventory.append(item)


def _is_stackable(item):
    """Items that can stack: consumables, materials, misc. NOT weapons/armor."""
    item_type = item.get("type", "")
    slot = item.get("slot", "")
    # Equipment doesn't stack
    if slot in ("weapon", "body", "head", "off_hand", "feet", "hands",
                "accessory1", "accessory2", "accessory"):
        return False
    if item_type in ("weapon", "armor", "shield"):
        return False
    # Everything else stacks (potions, materials, misc loot)
    return True

    def to_dict(self):
        """Serialize for save/display."""
        return {
            "name": self.name,
            "class": self.class_name,
            "level": self.level,
            "xp": self.xp,
            "gold": self.gold,
            "stats": dict(self.stats),
            "resources": dict(self.resources),
            "abilities": [a["name"] for a in self.abilities],
            "inventory": len(self.inventory),
        }
