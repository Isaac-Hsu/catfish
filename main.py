from vision import screenshot
from detection import analyze_fishing_screen
from decision import choose_tile
from human_input import gaussian_delay, gaussian_delay_custom, gaussian_click
from ui_state import find_on_screen
from utils import maybe_take_break, check_and_clear_ephemeral
from config import *
import time, random, os, cv2, sys
from datetime import datetime
import keyboard

os.makedirs("captures/fish_caught", exist_ok=True)  # for debug screenshots
os.makedirs("captures/water_caught", exist_ok=True) # for debug screenshots

# User setup 
print("Select fishing tool (bow/rod/harp):")
tool = input(">> ").strip().lower()
if tool == "bow":
    TIMEOUT_MEAN = 4.7
    TIMEOUT_MIN = 4.2
elif tool == "harp":
    TIMEOUT_MEAN = 7.6
    TIMEOUT_MIN = 7.3
else:  # rod or default
    TIMEOUT_MEAN = 8.6
    TIMEOUT_MIN = 8.3

enable_breaks = input("rare breaks? (y/n): ").strip().lower() == "y"

TIMEOUT_STD = 0.35  # gaussian variation

# Global state 
last_action_time = time.time()
last_screen = None
frozen_counter = 0

# Helper functions 

def gaussian_timeout():
    return max(TIMEOUT_MIN, random.gauss(TIMEOUT_MEAN, TIMEOUT_STD))

def mark_action():
    global last_action_time
    last_action_time = time.time()

def cooldown_sleep(seconds=0.2):
    time.sleep(seconds)

def force_fish_catch_if_frozen(current_img):
    global last_screen, frozen_counter
    if last_screen is not None:
        diff = cv2.absdiff(current_img, last_screen)
        if diff.mean() < 2.0:  # almost no change
            frozen_counter += 1
        else:
            frozen_counter = 0
    last_screen = current_img
    if frozen_counter >= 100:  # ~20s assuming 0.2s per loop
        print("screen change not detected, rerunning /fish catch")
        import pyautogui
        pyautogui.typewrite("/fish catch", interval=0.2)
        pyautogui.typewrite("\n", interval=0.1)
        pyautogui.typewrite("\n", interval=0.1)
        #pyautogui.typewrite("+:", interval=0.1)
        #time.sleep(0.2)
        #pyautogui.click(762, 422)
        time.sleep(3.0)
        pyautogui.click(778, 930)
        #pyautogui.click(616, 903)
        time.sleep(0.2)
        frozen_counter = 0
        return True
    return False

def wait_and_click_fish_again(timeout):
    start = time.time()
    while time.time() - start < timeout:
        timer_pos = find_on_screen("templates/ui/timer_1s.png", threshold=0.85)
        if timer_pos:
            # small chance to break
            fish_again = find_on_screen("templates/ui/fish_again.png", threshold=0.8)
            if fish_again:
                gaussian_delay()
                gaussian_click(*fish_again)
                mark_action()
                return True
        cooldown_sleep(0.1)
    return False

def terminate():
    print("hotkey termination")
    os._exit(0)

# Ctrl+C works globally, even if the game is focused
keyboard.add_hotkey("ctrl+c", terminate)


# Main loop 
print("starting")
try:
    while True:
        # Ephemeral check 
        if check_and_clear_ephemeral():
            cooldown_sleep(0.1)
            wait_and_click_fish_again(timeout=0.5)
            continue

        # Fish again / timer check 
        wait_and_click_fish_again(timeout=0.2)

        # Screenshot and frozen check 
        fishing_img = screenshot(FISHING_IMAGE_REGION)
        if force_fish_catch_if_frozen(fishing_img):
            cooldown_sleep(0.2)
            continue

        # Fishing grid detection 
        grid_pos = find_on_screen("templates/ui/fishing_grid.png", threshold=0.85)
        if grid_pos:
            gaussian_delay_custom(350, 80)
            mark_action()

            # Analyze tiles 
            tiles = analyze_fishing_screen(fishing_img)
            ### debugging
            print("Tile certainties:")
            for i, t in enumerate(tiles, start=1):
                print(
                    f"  Tile {i}: "
                    f"fish={t['fish_score']:.3f} "
                    f"mine={t['mine_score']:.3f} "
                    f"water={t['water_score']:.3f}"
                )
            

            # Skip if all zero confidence (avoid unloaded image)
            if all(t["fish_score"] == 0.0 and t["mine_score"] == 0.0 and t["water_score"] == 0.0 for t in tiles):
                print("all tiles zero confidence, rerunning")
                cooldown_sleep(0.2)
                continue

            # Decide tile 
            chosen = choose_tile(tiles)

            # prioritize buttons 5/6 if water
            if chosen.get("water", False) and chosen["index"] not in [5,6]:
                for idx in [5,6]:
                    if tiles[idx-1].get("water", False) and not tiles[idx-1]["mine"]:
                        chosen = tiles[idx-1]
                        break

            button_x, button_y = CATCH_BUTTON_COORDS[chosen["index"]]

            print(f"Chosen tile: {chosen['index']} | fish={chosen['fish']} mine={chosen['mine']} water={chosen['water']}")    #### debugging msg

            # Screenshot before click 
            pre_click_img = fishing_img

            # Click 
            gaussian_delay_custom(250, 120)
            gaussian_click(button_x, button_y)
            mark_action()

            ##### debug, screenshots
            # Save screenshot 
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            folder = "fish_caught" if chosen.get("fish") else "water_caught"
            out_path = f"captures/{folder}/{timestamp}.png"
            cv2.imwrite(out_path, pre_click_img)
            

            # Small break chance after catch 
            if enable_breaks and random.random() < BREAK_PROBABILITY:
                print("break")
                maybe_take_break()

            # Wait TIMEOUT before next fish_again check 
            timeout_wait = gaussian_timeout()
            wait_and_click_fish_again(timeout=timeout_wait)

        # Short cooldown 
        cooldown_sleep(0.2)

except KeyboardInterrupt:
    print("stopped.")
    sys.exit(0)
