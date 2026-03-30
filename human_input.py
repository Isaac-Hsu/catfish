import pyautogui
import random
import time
import math
from config import *

def gaussian_delay():
    delay = random.gauss(REACTION_MEAN_MS, REACTION_STD_MS)
    time.sleep(max(delay, 200) / 1000)

def gaussian_delay_custom(mean_ms, std_ms):
    delay = random.gauss(mean_ms, std_ms)
    time.sleep(max(delay, 50) / 1000)  # ensure at least 50ms

def gaussian_click(x, y):
    pyautogui.moveTo(x, y, duration=0.05)
    pyautogui.click()
