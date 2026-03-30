import cv2
import pyautogui
import numpy as np

def find_on_screen(template_path, threshold=0.8):
    screen = pyautogui.screenshot()
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2GRAY)
    tmpl = cv2.imread(template_path, 0)

    res = cv2.matchTemplate(screen, tmpl, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val > threshold:
        h, w = tmpl.shape
        return (max_loc[0] + w//2, max_loc[1] + h//2)
    return None
