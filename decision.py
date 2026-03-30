from config import *
import random

def choose_tile(tiles):
    # Desired fish tiles
    fish_tiles = [t for t in tiles if t["fish"] in FISH_PRIORITY and not t["mine"]]
    if fish_tiles:
        fish_tiles.sort(key=lambda t: FISH_PRIORITY[t["fish"]], reverse=True)
        top_priority = FISH_PRIORITY[fish_tiles[0]["fish"]]
        candidates = [t for t in fish_tiles if FISH_PRIORITY[t["fish"]] == top_priority]
        return random.choice(candidates)

    # Water tiles (empty, no mine, no undesired fish)
    water_tiles = [t for t in tiles if t.get("water", False) and not t["mine"]]
    if water_tiles:
        return random.choice(water_tiles)

    # Fallback: pick any safe tile (rare)
    safe_tiles = [t for t in tiles if not t["mine"]]
    return random.choice(safe_tiles)
