import random

# screen-relative bounding box of fishing image
#FISHING_IMAGE_REGION = (529, 253, 393, 393)  # x, y, w, h, 1 bait 
#FISHING_IMAGE_REGION = (529, 233, 393, 393)  # x, y, w, h, 2 baits
FISHING_IMAGE_REGION = (529, 275, 393, 393)  # x, y, w, h, 2 baits, no alert


# tile grid
GRID_ROWS = 3
GRID_COLS = 3

# Tile index is 1–9, left-to-right, top-to-bottom
# Values are (x, y) screen coordinates of the center of the catch button

'''
CATCH_BUTTON_COORDS = { ## w/ alert
    1: (557, 767),
    2: (634, 767),
    3: (711, 767),
    4: (556, 816),
    5: (634, 816),
    6: (711, 816),
    7: (557, 861),
    8: (616, 851),
    9: (733, 861),
}
'''

CATCH_BUTTON_COORDS = { ## wo/ alert
    1: (571, 812),
    2: (648, 812),
    3: (725, 812),
    4: (571, 861),
    5: (648, 861),
    6: (725, 861),
    7: (571, 906),
    8: (630, 896),
    9: (747, 906),
}

# gaussian click behavior
CLICK_SIGMA_PX = 7
REACTION_MEAN_MS = 450
REACTION_STD_MS = 80

# rare long breaks
BREAK_PROBABILITY = 0.0023
BREAK_MIN_SEC = 60
BREAK_MAX_SEC = 421

# fish priority (higher = more important)
FISH_PRIORITY = {
    #"gorgolox": 100,
    #"seareal": 80,
    #"witch": 60,
    #"blackneon": 101,
    "koi": 150,
    "spectral": 100, 
    "snappingturtle": 50,
    "flying": 50,
    "goldfish": 20,
    "guppy": 20,
    "crappie": 20,
    "item": 1,
}

# template matching thresholds
FISH_MATCH_THRESHOLD = 0.93
MINE_MATCH_THRESHOLD = 0.93
