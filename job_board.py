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

    # ── Greenwood Jobs ──
    # Greenwood is a druid outpost deep in the western forest. The Fading corrupts
    # the woods and twists animals. Rangers and druids are desperate for help.
    "gw_shadow_beasts": {
        "name": "Shadow-Touched Animals",
        "town": "greenwood",
        "description": "Fading corruption is twisting the forest animals into shadow-touched "
                       "horrors. Kill 5 Fading Wolves before they reach the outpost — "
                       "the rangers can't hold the line alone.",
        "type": "bounty",
        "enemy_name": "Fading Wolf",
        "required": 5,
        "reward_gold": 130,
        "reward_xp": 90,
        "repeatable": True,
        "level_req": 3,
    },
    "gw_corrupted_hounds": {
        "name": "Hound Pack from the East",
        "town": "greenwood",
        "description": "Fading Hounds have been circling the outpost at night. "
                       "The scouts have tracked the pack to the eastern tree line. "
                       "Put down 6 of them before they grow bolder.",
        "type": "bounty",
        "enemy_name": "Fading Hound",
        "required": 6,
        "reward_gold": 110,
        "reward_xp": 75,
        "repeatable": True,
        "level_req": 2,
    },
    "gw_spider_scouts": {
        "name": "Spider Scouts",
        "town": "greenwood",
        "description": "Giant spiders from the Nest have been scouting southward. "
                       "The druids believe they're following Fading energy trails. "
                       "Bring back 4 Giant Spider fangs as proof they've been driven back.",
        "type": "fetch",
        "item_name": "Spider Fang",
        "required": 4,
        "reward_gold": 160,
        "reward_xp": 110,
        "repeatable": True,
        "level_req": 3,
    },

    # ── Saltmere Jobs ──
    # Saltmere is a port town with a strong thieves' guild and sea-trade culture.
    # Ships vanish, strange things wash ashore, and the tides run wrong.
    "sm_drowned_crew": {
        "name": "Drowned Crew",
        "town": "saltmere",
        "description": "Three weeks ago a trade galleon went down in calm water. "
                       "Now the crew are back — Drowned Revenants walking the shallows. "
                       "Kill 5 of them and put them to rest.",
        "type": "bounty",
        "enemy_name": "Drowned Revenant",
        "required": 5,
        "reward_gold": 175,
        "reward_xp": 120,
        "repeatable": True,
        "level_req": 4,
    },
    "sm_tide_wraiths": {
        "name": "Tide Wraith Attacks",
        "town": "saltmere",
        "description": "Tide Wraiths are capsizing small fishing boats in the harbour mouth. "
                       "The Tide Priest says they're drawn to Fading energy in the water. "
                       "Kill 4 and the fishing fleet can work again.",
        "type": "bounty",
        "enemy_name": "Tide Wraith",
        "required": 4,
        "reward_gold": 200,
        "reward_xp": 135,
        "repeatable": True,
        "level_req": 4,
    },
    "sm_pale_coast_scouting": {
        "name": "Scout the Pale Coast",
        "town": "saltmere",
        "description": "Ships that pass the Pale Coast have stopped returning. "
                       "The Guild needs to know if the harbor there is viable. "
                       "Reach the Pale Coast and report back alive.",
        "type": "explore",
        "dungeon_id": "pale_coast",
        "floor_required": 1,
        "reward_gold": 320,
        "reward_xp": 200,
        "repeatable": False,
        "level_req": 6,
    },

    # ── Sanctum Jobs ──
    # Sanctum is a holy cathedral city — the seat of the Church of the Eternal Flame.
    # Faith is shaken, pilgrims are endangered, and the Fading encroaches on sacred ground.
    "sc_undead_cleared": {
        "name": "Sanctify the Crypts",
        "town": "sanctum",
        "description": "Shadow energy is reanimating bodies in the outer crypts. "
                       "Skeleton Warriors walk where pilgrims should rest in peace. "
                       "Clear 6 of them and the Cathedral will bless your arms.",
        "type": "bounty",
        "enemy_name": "Skeleton Warrior",
        "required": 6,
        "reward_gold": 150,
        "reward_xp": 100,
        "repeatable": True,
        "level_req": 3,
    },
    "sc_crypt_investigation": {
        "name": "Reach the Deep Vault",
        "town": "sanctum",
        "description": "The Sunken Crypt was sealed by the Church two hundred years ago. "
                       "High Priest Aldara needs someone to reach the second level and "
                       "confirm what the old records say is there. Don't open anything.",
        "type": "explore",
        "dungeon_id": "sunken_crypt",
        "floor_required": 2,
        "reward_gold": 280,
        "reward_xp": 180,
        "repeatable": False,
        "level_req": 5,
    },
    "sc_wailing_spirits": {
        "name": "The Wailing Pilgrims",
        "town": "sanctum",
        "description": "Wailing Spirits have been following pilgrims on the road to the Cathedral. "
                       "Three pilgrims have gone mad from the haunting. "
                       "Banish 5 of them and the road will be safe.",
        "type": "bounty",
        "enemy_name": "Wailing Spirit",
        "required": 5,
        "reward_gold": 160,
        "reward_xp": 110,
        "repeatable": True,
        "level_req": 4,
    },

    # ── Crystalspire Jobs ──
    # Crystalspire is the mage-city — arcane towers, Fading-disrupted ley lines,
    # dangerous experiments, and scholars who care more about data than survival.
    "cs_arcane_sentries": {
        "name": "Rogue Arcane Sentries",
        "town": "crystalspire",
        "description": "Three experimental Arcane Sentries escaped containment and are "
                       "wandering the ruins to the east. They'll attack on sight. "
                       "Destroy them before they cause a diplomatic incident.",
        "type": "bounty",
        "enemy_name": "Arcane Sentry",
        "required": 3,
        "reward_gold": 220,
        "reward_xp": 150,
        "repeatable": True,
        "level_req": 4,
    },
    "cs_crystal_shards": {
        "name": "Crystal Elemental Shards",
        "town": "crystalspire",
        "description": "The Academy needs raw elemental crystal, but the local elementals "
                       "have been driven berserk by Fading energy. "
                       "Bring back 3 Crystal Elemental shards — collected the hard way.",
        "type": "fetch",
        "item_name": "Elemental Shard",
        "required": 3,
        "reward_gold": 260,
        "reward_xp": 170,
        "repeatable": True,
        "level_req": 5,
    },
    "cs_ruins_data": {
        "name": "Data from Ashenmoor",
        "town": "crystalspire",
        "description": "Scholar Petra needs readings from inside the Ruins of Ashenmoor. "
                       "Reach the second level — the ley line readings are stronger there. "
                       "Return with anything inscribed on the walls.",
        "type": "explore",
        "dungeon_id": "ruins_ashenmoor",
        "floor_required": 2,
        "reward_gold": 300,
        "reward_xp": 190,
        "repeatable": False,
        "level_req": 5,
    },

    # ── Thornhaven Jobs ──
    # Thornhaven is the imperial military capital — fortress-city, garrison culture,
    # political intrigue, and an empire that knows the Fading is winning.
    "th_fading_bears": {
        "name": "Fading Bear Threat",
        "town": "thornhaven",
        "description": "Shadow-corrupted bears have been destroying supply caravans on the "
                       "eastern road. The garrison can't spare soldiers for wildlife. "
                       "Kill 3 Fading Bears and the road opens again.",
        "type": "bounty",
        "enemy_name": "Fading Bear",
        "required": 3,
        "reward_gold": 240,
        "reward_xp": 160,
        "repeatable": True,
        "level_req": 5,
    },
    "th_ash_revenants": {
        "name": "Revenants from Ashenmoor",
        "town": "thornhaven",
        "description": "Ash Revenants from the ruins are ranging this far east now — "
                       "they've killed two of our outriders. Commander Varek needs proof "
                       "the incursion is being pushed back. Bring 5 of them down.",
        "type": "bounty",
        "enemy_name": "Ash Revenant",
        "required": 5,
        "reward_gold": 280,
        "reward_xp": 185,
        "repeatable": True,
        "level_req": 5,
    },
    "th_ruins_floor3": {
        "name": "Ashenmoor Third Level",
        "town": "thornhaven",
        "description": "Imperial command wants to know the full extent of the Ruins. "
                       "Our last scouting team made it to floor 2. "
                       "Reach the third level and return. The Governor will reward this personally.",
        "type": "explore",
        "dungeon_id": "ruins_ashenmoor",
        "floor_required": 3,
        "reward_gold": 400,
        "reward_xp": 250,
        "repeatable": False,
        "level_req": 6,
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
