"""
Thin module that lets dialogue actions access the current party.
town_ui sets _party before opening a dialogue; resets after.
"""
_party = None

def set_party(party):
    global _party
    _party = party

def get_party():
    return _party
