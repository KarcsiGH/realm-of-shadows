"""
Realm of Shadows — Dialogue Engine

Data-driven dialogue system. Conversations are trees of nodes.
Each node has text, optional speaker, optional choices, and optional
flag effects (set flags when a node is reached or choice is made).

Dialogue Tree format:
{
    "id": "maren_intro",
    "nodes": {
        "start": {
            "speaker": "Maren",
            "text": "You're the ones they sent? I expected... more.",
            "next": "explain",          # auto-advance to next node
        },
        "explain": {
            "speaker": "Maren",
            "text": "The Fading is consuming everything...",
            "choices": [
                {"text": "What is the Fading?", "next": "fading_explain"},
                {"text": "What do you need from us?", "next": "mission"},
                {"text": "We're not interested.", "next": "refuse"},
            ],
        },
        "fading_explain": {
            "speaker": "Maren",
            "text": "Reality is dissolving...",
            "on_enter": [{"action": "set_flag", "flag": "lore.fading_basics", "value": True}],
            "next": "mission",
        },
        "refuse": {
            "speaker": "Maren",
            "text": "Then the world dies. Think on that.",
            "end": True,
        },
        ...
    }
}

Nodes can have:
  - "conditions": list of conditions required to show this node/choice
  - "on_enter": list of actions to execute when entering this node
  - "choices": list of {text, next, conditions?, on_select?}
  - "next": auto-advance to another node
  - "end": True to end the conversation
"""

from core.story_flags import check_conditions, set_flag, start_quest, \
    complete_quest, discover_lore, meet_npc, defeat_boss, set_quest_state


# ═══════════════════════════════════════════════════════════════
#  DIALOGUE STATE
# ═══════════════════════════════════════════════════════════════

class DialogueState:
    """Manages an active dialogue conversation."""

    def __init__(self, tree):
        self.tree = tree
        self.nodes = tree["nodes"]
        self.current_node_id = "start"
        self.current_node = self.nodes["start"]
        self.finished = False
        self.log = []  # list of (speaker, text) for scroll-back

        # Execute on_enter for start node
        self._enter_node(self.current_node)

    def _enter_node(self, node):
        """Process entering a node: execute actions, record in log."""
        speaker = node.get("speaker", "")
        text = node.get("text", "")
        if text:
            self.log.append((speaker, text))

        # Execute on_enter actions
        for action in node.get("on_enter", []):
            _execute_action(action)

        # Check if this is an end node
        if node.get("end"):
            self.finished = True

    def get_speaker(self):
        return self.current_node.get("speaker", "")

    def get_text(self):
        return self.current_node.get("text", "")

    def get_choices(self):
        """Get available choices, filtered by conditions."""
        raw = self.current_node.get("choices", [])
        result = []
        for choice in raw:
            conds = choice.get("conditions", [])
            if check_conditions(conds):
                result.append(choice)
        return result

    def has_choices(self):
        return len(self.get_choices()) > 0

    def should_auto_advance(self):
        """True if this node has no choices and a 'next' field."""
        if self.finished:
            return False
        return not self.has_choices() and "next" in self.current_node

    def advance(self):
        """Auto-advance to the next node (for nodes without choices)."""
        next_id = self.current_node.get("next")
        if next_id and next_id in self.nodes:
            self.current_node_id = next_id
            self.current_node = self.nodes[next_id]
            self._enter_node(self.current_node)
            return True
        self.finished = True
        return False

    def select_choice(self, choice_idx):
        """Player selects a choice. Returns True if conversation continues."""
        choices = self.get_choices()
        if choice_idx >= len(choices):
            return False

        choice = choices[choice_idx]

        # Record what the player said
        self.log.append(("You", choice["text"]))

        # Execute on_select actions
        for action in choice.get("on_select", []):
            _execute_action(action)

        # Go to next node
        next_id = choice.get("next")
        if next_id and next_id in self.nodes:
            self.current_node_id = next_id
            self.current_node = self.nodes[next_id]
            self._enter_node(self.current_node)
            return True

        self.finished = True
        return False


# ═══════════════════════════════════════════════════════════════
#  ACTION EXECUTION
# ═══════════════════════════════════════════════════════════════

def _execute_action(action):
    """Execute a dialogue action (set flag, start quest, etc.)."""
    act = action.get("action", "")

    if act == "set_flag":
        set_flag(action["flag"], action.get("value", True))
    elif act == "start_quest":
        start_quest(action["quest"])
    elif act == "complete_quest":
        complete_quest(action["quest"])
    elif act == "set_quest":
        set_quest_state(action["quest"], action["state"])
    elif act == "discover_lore":
        discover_lore(action["lore"])
    elif act == "meet_npc":
        meet_npc(action["npc"])


# ═══════════════════════════════════════════════════════════════
#  DIALOGUE SELECTION
# ═══════════════════════════════════════════════════════════════

def select_dialogue(npc_id, dialogue_list):
    """
    Given an NPC's list of dialogue trees (ordered by priority),
    return the first one whose conditions are met.

    Each entry: {"conditions": [...], "tree": {...}}
    Later entries are fallbacks.
    """
    for entry in dialogue_list:
        conds = entry.get("conditions", [])
        if check_conditions(conds):
            tree = entry["tree"]
            return DialogueState(tree)
    return None
