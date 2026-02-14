"""
Realm of Shadows — Character Model
"""
import random
from core.classes import (
    STAT_NAMES, CLASSES, CLASS_ORDER,
    get_all_resources, get_class_fit,
)


class Character:
    def __init__(self, name="", class_name=None):
        self.name = name
        self.class_name = class_name
        self.level = 1
        self.stats = {s: 5 for s in STAT_NAMES}  # base before life path
        self.life_path = []       # list of event dicts chosen
        self.backstory_parts = [] # narrative snippets
        self.resources = {}
        self.abilities = []
        self.quick_rolled = False

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
        """Skip life path: use class starting stats + small random bonus."""
        self.class_name = class_name
        self.quick_rolled = True
        start = CLASSES[class_name]["starting_stats"]
        for stat in STAT_NAMES:
            self.stats[stat] = start[stat] + random.randint(0, 2)
        self._finalize()

    def finalize_with_class(self, class_name):
        """After life path is complete, assign class and calculate everything."""
        self.class_name = class_name
        self.apply_random_seasoning()
        self._finalize()

    def _finalize(self):
        """Calculate resources and assign starting abilities."""
        cls = CLASSES[self.class_name]
        self.resources = get_all_resources(self.class_name, self.stats, self.level)
        self.abilities = [a.copy() for a in cls["starting_abilities"]]

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

    def to_dict(self):
        """Serialize for save/display."""
        return {
            "name": self.name,
            "class": self.class_name,
            "level": self.level,
            "stats": dict(self.stats),
            "resources": dict(self.resources),
            "abilities": [a["name"] for a in self.abilities],
        }
