import pyautogui
import time
import random
import tkinter as tk
from PIL import ImageChops, Image

# --- Globals ---
old_ss = None
custom_interval = (15, 20)
keypress_range = (2, 4)

# --- Functions ---

def random_key_presses():
    count = random.randint(*keypress_range)
    for _ in range(count):
        pyautogui.press('down')
        time.sleep(random.randint(*custom_interval))

def random_mouse_move():
    screen_width, screen_height = pyautogui.size()
    pyautogui.moveTo(
        random.randint(100, screen_width - 100),
        random.randint(100, screen_height - 100),
        duration=0.5
    )

def take_screenshot(filename="screenshot.png"):
    ss = pyautogui.screenshot()
    ss.save(filename)
    return filename

def images_are_same(img1_path, img2_path):
    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)
    diff = ImageChops.difference(img1, img2)
    return not diff.getbbox()

def check_page_end():
    global old_ss
    new_ss_path = take_screenshot("new.png")
    
    if old_ss is not None and images_are_same(old_ss, new_ss_path):
        pyautogui.hotkey('ctrl', 'home')
        pyautogui.hotkey('ctrl', 'tab')
        return True
    
    old_ss = new_ss_path
    return False

def perform_cycle():
    for _ in range(5):
        random_key_presses()
        random_mouse_move()
        if check_page_end():
            break

# --- GUI ---

def start_script():
    global custom_interval
    min_sec = int(min_entry.get())
    max_sec = int(max_entry.get())
    custom_interval = (min_sec, max_sec)
    perform_cycle()

root = tk.Tk()
root.title("Office Break Helper")

tk.Label(root, text="Min Interval (s):").pack()
min_entry = tk.Entry(root)
min_entry.insert(0, "15")
min_entry.pack()

tk.Label(root, text="Max Interval (s):").pack()
max_entry = tk.Entry(root)
max_entry.insert(0, "20")
max_entry.pack()

tk.Button(root, text="Start", command=start_script).pack()

root.mainloop()
