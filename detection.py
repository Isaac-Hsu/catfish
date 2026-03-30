import cv2
import os
from config import *

def load_templates(folder):
    
    # Loads all PNGs in a folder.
    # Groups them by base name (before _1, _2, ...).
    # Returns a dict: {fish_name: [list of images]}
    templates = {}
    for f in os.listdir(folder):
        if f.endswith(".png"):
            # Extract base name: gorgolox_1.png -> gorgolox
            base_name = f.split("_")[0]
            tmpl = cv2.imread(os.path.join(folder, f))  # keep BGR
            if base_name not in templates:
                templates[base_name] = []
            templates[base_name].append(tmpl)
    return templates



FISH_TEMPLATES = load_templates("templates/fish")
MINE_TEMPLATES = load_templates("templates/mines")
WATER_TEMPLATES = load_templates("templates/water")

def match_any_template(tile_img, templates):
    #Returns the highest match score across all templates.
    #templates: {name: [list of images]}
    
    best_score = 0.0
    best_name = None

    for name, tmpl_list in templates.items():
        for tmpl in tmpl_list:
            res = cv2.matchTemplate(tile_img, tmpl, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(res)
            if max_val > best_score:
                best_score = max_val
                best_name = name

    return best_name, best_score


def match_tile_in_screen(full_img, templates):
    #Returns (best_template_name, score, top-left coords)
    
    best = (None, 0.0, (0, 0))

    for name, tmpl_list in templates.items():
        for tmpl in tmpl_list:
            res = cv2.matchTemplate(full_img, tmpl, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)
            if max_val > best[1]:
                best = (name, max_val, max_loc)

    return best




def analyze_fishing_screen(full_img):
    #Detects fish, mines, and water in the full fishing image
    #Returns a list of 9 tiles with info: index, fish, mine, water, scores
    
    tile_w = FISHING_IMAGE_REGION[2] // GRID_COLS
    tile_h = FISHING_IMAGE_REGION[3] // GRID_ROWS

    # Fish detection
    fish_name, fish_score, fish_pos = match_tile_in_screen(full_img, FISH_TEMPLATES)
    if fish_name not in FISH_PRIORITY or fish_score < FISH_MATCH_THRESHOLD:
        fish_name = None

    # Mine detection
    mine_name, mine_score, mine_pos = match_tile_in_screen(full_img, MINE_TEMPLATES)
    mine_detected = mine_score > MINE_MATCH_THRESHOLD

    tiles = []
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            idx = r * GRID_COLS + c + 1

            # Extract tile image
            tile_img = full_img[
                r*tile_h:(r+1)*tile_h,
                c*tile_w:(c+1)*tile_w
            ]

            # Fish
            fish_in_tile = False
            if fish_name:
                fx, fy = fish_pos
                if c*tile_w <= fx < (c+1)*tile_w and r*tile_h <= fy < (r+1)*tile_h:
                    fish_in_tile = True
                    # water_in_tile = False

            # Mine
            mine_in_tile = False
            if mine_detected:
                mx, my = mine_pos
                if c*tile_w <= mx < (c+1)*tile_w and r*tile_h <= my < (r+1)*tile_h:
                    mine_in_tile = True

            # Water (per-tile, multi-template)
            water_name, water_score = match_any_template(tile_img, WATER_TEMPLATES)
            water_in_tile = water_score > 0.93
            
            # Resolve fish vs water conflict
            if fish_in_tile:
                # If fish is confidently detected, it overrides water
                if fish_score >= FISH_MATCH_THRESHOLD or fish_score > water_score:
                    water_in_tile = False

            tiles.append({
                "index": idx,
                "grid_pos": (r, c),
                "fish": fish_name if fish_in_tile else None,
                "fish_score": fish_score if fish_in_tile else 0.0,
                "mine": mine_in_tile,
                "mine_score": mine_score if mine_in_tile else 0.0,
                "water": water_in_tile,
                "water_score": water_score if water_in_tile else 0.0
            })


    return tiles
