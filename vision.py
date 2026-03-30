import cv2
import numpy as np
import pyautogui
from config import *

def screenshot(region=None):
    img = pyautogui.screenshot(region=region)
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

def split_tiles(fishing_img):
    tiles = []
    h, w, _ = fishing_img.shape
    tile_w = w // GRID_COLS
    tile_h = h // GRID_ROWS

    idx = 1
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            crop = fishing_img[
                r*tile_h:(r+1)*tile_h,
                c*tile_w:(c+1)*tile_w
            ]
            tiles.append({
                "index": idx,
                "image": crop,
                "grid_pos": (r, c)
            })
            idx += 1
    return tiles
