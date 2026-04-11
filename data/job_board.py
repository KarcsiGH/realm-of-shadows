"""
Realm of Shadows — Job Board System

Repeatable and one-time jobs posted at town job boards.
Jobs track progress via story_flags and reward gold/XP on completion.

Job types:
  - bounty: kill N enemies of a type (tracked by enemy kill flags)
  - fetch: collect N items and turn them in
  - explore: visit a specific dungeon floor
"""

from core.story_flags import get_flag, set_flag, get_quest_state, set_quest_state

# ═══════════════════════════════════════════════════════════════
#  JOB DEFINITIONS
# ═══════════════════════════════════════════════════════════════

JOBS = {
    # ── Briarhollow Jobs ──
    "bh_goblin_ears": {
        "name": "Goblin Bounty",
        "town": "briarhollow",
        "description": "The village council pays for goblin ears. "
                       "Bring back 5 to prove the warren is being cleared.",
        "type": "fetch",
        "item_name": "Goblin Ear",
        "required": 5,
        "reward_gold": 80,
        "reward_xp": 60,
        "repeatable": True,
        "level_req": 1,
    },
    "bh_wolf_pelts": {
        "name": "Pelts for the Tanner",
        "town": "briarhollow",
        "description": "The tanner needs wolf pelts for leather. "
                       "Bring 3 pelts from the eastern woods.",
        "type": "fetch",
        "item_name": "Wolf Pelt",
        "required": 3,
        "reward_gold": 60,
        "reward_xp": 45,
        "repeatable": True,
        "level_req": 1,
    },
    "bh_warren_scout": {
        "name": "Scout the Warren",
        "town": "briarhollow",
        "description": "Reach floor 2 of the Goblin Warren and return alive. "
                       "The council needs to know how deep the tunnels go.",
        "type": "explore",
        "dungeon_id": "goblin_warren",
        "floor_required": 2,
        "reward_gold": 100,
        "reward_xp": 80,
        "repeatable": False,
        "level_req": 1,
    },
    "bh_rat_problem": {
        "name": "Rat Infestation",
        "town": "briarhollow",
        "description": "Giant rats from the warren are spreading into the cellars. "
                       "Kill 8 of them in the first floor.",
        "type": "bounty",
        "enemy_name": "Rabid Rat",
        "required": 8,
        "reward_gold": 40,
        "reward_xp": 30,
        "repeatable": True,
        "level_req": 1,
    },
    "bh_bat_wings": {
        "name": "Bat Extermination",
        "town": "briarhollow",
        "description": "Cave bats carry disease. The apothecary pays for proof of culling. "
                       "Kill 10 cave bats.",
        "type": "bounty",
        "enemy_name": "Cave Bat",
        "required": 10,
        "reward_gold": 50,
        "reward_xp": 40,
        "repeatable": True,
        "level_req": 1,
    },

    # ── Woodhaven Jobs ──
    "wh_spider_silk": {
        "name": "Spider Silk Collection",
        "town": "woodhaven",
        "description": "The weaver needs spider silk for enchanted cloth. "
                       "Bring 4 bundles from the Spider's Nest.",
        "type": "fetch",
        "item_name": "Spider Silk",
        "required": 4,
        "reward_gold": 120,
        "reward_xp": 80,
        "repeatable": True,
        "level_req": 2,
    },
    "wh_dire_wolves": {
        "name": "Dire Wolf Threat",
        "town": "woodhaven",
        "description": "Dire wolves are menacing the trade roads. "
                       "Kill 5 of them to make the forest safe.",
        "type": "bounty",
        "enemy_name": "Dire Wolf",
        "required": 5,
        "reward_gold": 150,
        "reward_xp": 100,
        "repeatable": True,
        "level_req": 3,
    },
    "wh_nest_scout": {
        "name": "Map the Spider's Nest",
        "town": "woodhaven",
        "description": "Rangers need to know how extensive the nest is. "
                       "Reach floor 3 and return.",
        "type": "explore",
        "dungeon_id": "spiders_nest",
        "floor_required": 3,
        "reward_gold": 180,
        "reward_xp": 120,
        "repeatable": False,
        "level_req": 2,
    },

    # ── Ironhearth Jobs ──
    "ih_mine_clearance": {
        "name": "Mine Clearance",
        "town": "ironhearth",
        "description": "Kobolds have overrun the lower shafts. "
                       "Kill 6 kobold miners to reclaim the tunnels.",
        "type": "bounty",
        "enemy_name": "Kobold Miner",
        "required": 6,
        "reward_gold": 140,
        "reward_xp": 90,
        "repeatable": True,
        "level_req": 3,
    },
    "ih_ore_recovery": {
        "name": "Ore Recovery",
        "town": "ironhearth",
        "description": "Bring 3 pieces of Leather Scraps from the mine. "
                       "The forge needs raw materials.",
        "type": "fetch",
        "item_name": "Leather Scraps",
        "required": 3,
        "reward_gold": 100,
        "reward_xp": 70,
        "repeatable": True,
        "level_req": 2,
    },
    "ih_deep_mine": {
        "name": "Reach the Deep Shafts",
        "town": "ironhearth",
        "description": "The foreman's last report came from floor 4 of the mine. "
                       "Reach that depth and report back.",
        "type": "explore",
        "dungeon_id": "abandoned_mine",
        "floor_required": 4,
        "reward_gold": 250,
        "reward_xp": 160,
        "repeatable": False,
        "level_req": 3,
    },

    # ── Crystalspire ────────────────────────────────────────────────────────
    "cs_shadow_samples": {
        "name": "Fading Specimen Collection",
        "town": "crystalspire",
        "description": "The Academy needs samples of shadow-touched material "
                       "from the Ashenmoor ruins. Bring back 4 Fading Shards "
                       "for the research archive.",
        "type": "fetch",
        "item_name": "Fading Shard",
        "required": 4,
        "reward_gold": 280,
        "reward_xp": 200,
        "repeatable": False,
        "level_req": 5,
    },
    "cs_crypt_survey": {
        "name": "Survey the Sunken Crypt",
        "town": "crystalspire",
        "description": "The Cathedral has sealed records about the Sunken Crypt. "
                       "The Academy wants an independent survey. "
                       "Reach floor 3 and report back.",
        "type": "explore",
        "dungeon_id": "sunken_crypt",
        "floor_required": 3,
        "reward_gold": 400,
        "reward_xp": 280,
        "repeatable": False,
        "level_req": 6,
    },
    "cs_shadow_mages": {
        "name": "Shadow-Corrupted Mages",
        "town": "crystalspire",
        "description": "Three Academy mages went to study the Ashenmoor ruins "
                       "and did not return. The Academy fears the worst. "
                       "Eliminate any corrupted mage threats in the ruins.",
        "type": "bounty",
        "enemy_name": "Corrupted Mage",
        "required": 3,
        "reward_gold": 320,
        "reward_xp": 240,
        "repeatable": False,
        "level_req": 5,
    },

    # ── Thornhaven ──────────────────────────────────────────────────────────
    "th_deserter_hunt": {
        "name": "Imperial Deserters",
        "town": "thornhaven",
        "description": "Three Imperial soldiers abandoned their posts on the "
                       "Pale Coast road. The Governor wants them found — "
                       "alive or otherwise. Hunt down 3 Deserters.",
        "type": "bounty",
        "enemy_name": "Imperial Deserter",
        "required": 3,
        "reward_gold": 350,
        "reward_xp": 260,
        "repeatable": False,
        "level_req": 6,
    },
    "th_pale_coast_report": {
        "name": "Pale Coast Intelligence",
        "town": "thornhaven",
        "description": "The Governor needs a first-hand report on conditions "
                       "at the Pale Coast Catacombs. Reach floor 2 and return.",
        "type": "explore",
        "dungeon_id": "pale_coast",
        "floor_required": 2,
        "reward_gold": 500,
        "reward_xp": 350,
        "repeatable": False,
        "level_req": 7,
    },
    "th_undead_suppression": {
        "name": "Undead Suppression",
        "town": "thornhaven",
        "description": "Reports of risen dead near the Pale Coast are alarming "
                       "the citizenry. Eliminate 5 Risen Soldiers to demonstrate "
                       "the threat is contained.",
        "type": "bounty",
        "enemy_name": "Risen Soldier",
        "required": 5,
        "reward_gold": 300,
        "reward_xp": 220,
        "repeatable": True,
        "level_req": 6,
    },

    # ── Saltmere ────────────────────────────────────────────────────────────
    "sm_sea_creature_parts": {
        "name": "Deep Sea Specimen",
        "town": "saltmere",
        "description": "Something's been attacking the fishing boats. "
                       "Bring back a Deep Crawler Claw as proof — "
                       "the fishermen's guild is paying well.",
        "type": "fetch",
        "item_name": "Deep Crawler Claw",
        "required": 3,
        "reward_gold": 220,
        "reward_xp": 160,
        "repeatable": True,
        "level_req": 5,
    },
    "sm_pirate_bounty": {
        "name": "Pirate Suppression",
        "town": "saltmere",
        "description": "The Dockmaster is paying for pirate scalps — "
                       "metaphorically. Eliminate 4 Pirates operating "
                       "near the coast.",
        "type": "bounty",
        "enemy_name": "Saltmere Pirate",
        "required": 4,
        "reward_gold": 260,
        "reward_xp": 180,
        "repeatable": True,
        "level_req": 4,
    },

    # ── Sanctum ─────────────────────────────────────────────────────────────
    "sa_crypt_relics": {
        "name": "Recover the Holy Relics",
        "town": "sanctum",
        "description": "Sacred relics were stored in the Sunken Crypt before "
                       "it was sealed. The Cathedral wants them recovered. "
                       "Bring back 2 Sanctified Relics.",
        "type": "fetch",
        "item_name": "Sanctified Relic",
        "required": 2,
        "reward_gold": 450,
        "reward_xp": 320,
        "repeatable": False,
        "level_req": 7,
    },
    "sa_undead_purge": {
        "name": "Purge the Risen",
        "town": "sanctum",
        "description": "The Light demands the undead be put to rest. "
                       "Destroy 6 Risen in the Sunken Crypt or nearby ruins "
                       "as an act of holy service.",
        "type": "bounty",
        "enemy_name": "Risen",
        "required": 6,
        "reward_gold": 340,
        "reward_xp": 250,
        "repeatable": True,
        "level_req": 6,
    },

    # ── Emberveil ────────────────────────────────────────────────────────────
    "ev_volcanic_samples": {
        "name": "Volcanic Reagent Run",
        "town": "emberveil",
        "description": "Renn needs volcanic mineral samples from the deeper "
                       "caldera caves. Collect 5 Magma Cores — the forge "
                       "work won't wait.",
        "type": "fetch",
        "item_name": "Magma Core",
        "required": 5,
        "reward_gold": 380,
        "reward_xp": 280,
        "repeatable": True,
        "level_req": 8,
    },
    "ev_drake_suppression": {
        "name": "Drake Culling",
        "town": "emberveil",
        "description": "Young drakes from the Dragon's Tooth caldera are "
                       "raiding the settlement. Eliminate 4 Young Drakes "
                       "before the next raid.",
        "type": "bounty",
        "enemy_name": "Young Drake",
        "required": 4,
        "reward_gold": 420,
        "reward_xp": 300,
        "repeatable": True,
        "level_req": 9,
    },
}


# ═══════════════════════════════════════════════════════════════
#  JOB STATE MANAGEMENT
# ═══════════════════════════════════════════════════════════════

# States: 0=available, 1=accepted, -2=completed, -3=completed+repeatable (can retake)

def get_town_jobs(town_id):
    """Return list of (job_id, job_data, state) for a town."""
    results = []
    for job_id, job in JOBS.items():
        if job["town"] != town_id:
            continue
        state = get_flag(f"job.{job_id}.state", 0)
        # If repeatable and completed, reset to available
        if state == -2 and job.get("repeatable"):
            state = 0
            set_flag(f"job.{job_id}.state", 0)
            # Reset progress counters
            set_flag(f"job.{job_id}.progress", 0)
        results.append((job_id, job, state))
    return results


def accept_job(job_id):
    """Accept a job from the board."""
    set_flag(f"job.{job_id}.state", 1)
    set_flag(f"job.{job_id}.progress", 0)


def get_job_progress(job_id):
    """Get current progress count for a job."""
    return get_flag(f"job.{job_id}.progress", 0)


def add_job_progress(job_id, amount=1):
    """Increment job progress (e.g., killed an enemy, found an item)."""
    cur = get_flag(f"job.{job_id}.progress", 0)
    set_flag(f"job.{job_id}.progress", cur + amount)


def is_job_accepted(job_id):
    return get_flag(f"job.{job_id}.state", 0) == 1


def is_job_complete(job_id):
    return get_flag(f"job.{job_id}.state", 0) == -2


def check_job_ready(job_id, party):
    """Check if an accepted job can be turned in."""
    job = JOBS.get(job_id)
    if not job:
        return False
    state = get_flag(f"job.{job_id}.state", 0)
    if state != 1:
        return False

    if job["type"] == "bounty":
        progress = get_job_progress(job_id)
        return progress >= job["required"]

    elif job["type"] == "fetch":
        # Count matching items across all party inventories
        item_name = job["item_name"]
        count = 0
        for c in party:
            for item in c.inventory:
                if item.get("name") == item_name:
                    count += item.get("stack", 1)
        return count >= job["required"]

    elif job["type"] == "explore":
        flag_key = f"explored.{job['dungeon_id']}.floor{job['floor_required']}"
        return get_flag(flag_key, False)

    return False


def complete_job(job_id, party):
    """Turn in a completed job. Returns reward dict or None."""
    job = JOBS.get(job_id)
    if not job or not check_job_ready(job_id, party):
        return None

    # Remove fetch items from inventory
    if job["type"] == "fetch":
        remaining = job["required"]
        item_name = job["item_name"]
        for c in party:
            new_inv = []
            for item in c.inventory:
                if item.get("name") == item_name and remaining > 0:
                    stack = item.get("stack", 1)
                    if stack <= remaining:
                        remaining -= stack
                        continue  # consume entire stack
                    else:
                        item["stack"] = stack - remaining
                        remaining = 0
                new_inv.append(item)
            c.inventory = new_inv

    # Mark complete
    set_flag(f"job.{job_id}.state", -2)

    # Distribute rewards
    gold = job.get("reward_gold", 0)
    xp = job.get("reward_xp", 0)
    if party:
        gold_each = gold // len(party)
        xp_each = xp // len(party)
        for c in party:
            c.gold += gold_each
            c.xp += xp_each

    return {"gold": gold, "xp": xp}


def on_enemy_killed(enemy_name):
    """Called after combat to update bounty jobs."""
    for job_id, job in JOBS.items():
        if job["type"] != "bounty":
            continue
        if not is_job_accepted(job_id):
            continue
        if job["enemy_name"] == enemy_name:
            add_job_progress(job_id)


def on_dungeon_floor_reached(dungeon_id, floor_num):
    """Called when player enters a dungeon floor — updates explore jobs."""
    set_flag(f"explored.{dungeon_id}.floor{floor_num}", True)
