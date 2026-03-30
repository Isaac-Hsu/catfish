import os
import time
from PIL import ImageGrab
import pytesseract
import cv2
import numpy as np
from difflib import SequenceMatcher

# config
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Words to detect
TARGET_WORDS = ["catch", "catcn"] 
# Similarity threshold (0.0–1.0). Higher = stricter match
FUZZY_THRESHOLD = 0.7

CAPTURE_DIR = "captures"
os.makedirs(CAPTURE_DIR, exist_ok=True)

# helper
def similar(a, b):
    # return similarity ratio between two strings (0.0–1.0)
    return SequenceMatcher(None, a, b).ratio()

# take screenshot
time.sleep(1)  # time to switch to the target window
screenshot = ImageGrab.grab()
img = np.array(screenshot)

# convert to grayscale (better for OCR)
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

# threshold to improve text visibility
_, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)

#  OCR
data = pytesseract.image_to_data(thresh, output_type=pytesseract.Output.DICT)

# detection loop
hits = 0
for i, text in enumerate(data["text"]):
    word = text.lower().strip()
    # check similarity with all target words
    if any(similar(word, target.lower()) >= FUZZY_THRESHOLD for target in TARGET_WORDS):
        x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
        # rectangle on original RGB image
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(img, text, (x, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        hits += 1

# save output; debug for now
timestamp = time.strftime("%Y%m%d_%H%M%S")
output_path = os.path.join(CAPTURE_DIR, f"ocr_capture_{timestamp}.png")
cv2.imwrite(output_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

print(f"Done! Detected {hits} instance(s) of target words: {TARGET_WORDS}")
print(f"Saved annotated screenshot to: {output_path}")

# print(data["text"])
