import pyautogui
import os
import time

SAVE_DIR = "./capture/screenshots"

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def capture_screenshot():
    """Takes a screenshot and saves it with a timestamp."""
    file_path = os.path.join(SAVE_DIR, "screenshot.png")
    screenshot = pyautogui.screenshot()
    screenshot.save(file_path)
    print(f"Screenshot saved: {file_path}")
