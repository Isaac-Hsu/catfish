import random
import time
from config import *
from ui_state import find_on_screen
from human_input import gaussian_click

EPHEMERAL_COORDS = (713, 959)

def check_and_clear_ephemeral():
    pos = find_on_screen("templates/ui/ephemeral.png", threshold=0.85)
    if pos:
#        print("ephemeral msg, removing")   #### debug msg
        gaussian_click(*EPHEMERAL_COORDS)
        return True
    return False


def maybe_take_break():
    if random.random() < BREAK_PROBABILITY:
        time.sleep(random.randint(BREAK_MIN_SEC, BREAK_MAX_SEC))
