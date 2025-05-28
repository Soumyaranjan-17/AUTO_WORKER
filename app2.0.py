import tkinter as tk
from tkinter import ttk
from threading import Thread
import time
import random
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Controller as MouseController
import pyautogui
from PIL import ImageChops

# Global variables
keyboard = KeyboardController()
mouse = MouseController()
old_ss = None

# Default parameters
params = {
    'min_keys': 2,
    'max_keys': 4,
    'min_interval': 15,
    'max_interval': 20,
    'check_every_n_sets': 5,
    'diff_threshold': 10,
    'pixel_diff_value': 20
}

# Take full-screen screenshot
def take_fullscreen_screenshot():
    screen_width, screen_height = pyautogui.size()
    return pyautogui.screenshot(region=(0, 0, screen_width, screen_height)).convert("RGB")

# Compare screenshots to detect end of page
def compare_changes(img1, img2, diff_threshold=10, pixel_diff_threshold=20):
    diff = ImageChops.difference(img1, img2).convert('L')
    diff_pixels = sum(1 for pixel in diff.getdata() if pixel > pixel_diff_threshold)
    total_pixels = diff.size[0] * diff.size[1]
    percent_diff = (diff_pixels / total_pixels) * 100
    return percent_diff <= diff_threshold

# Simulate key presses and page end logic
def simulate_key_presses():
    global old_ss
    set_counter = 0

    while True:
        set_counter += 1
        num_keys = random.randint(params['min_keys'], params['max_keys'])

        for _ in range(num_keys):
            keyboard.press(Key.down)
            keyboard.release(Key.down)
            time.sleep(random.uniform(params['min_interval'], params['max_interval']))

        if set_counter % params['check_every_n_sets'] == 0:
            new_ss = take_fullscreen_screenshot()
            if old_ss and compare_changes(old_ss, new_ss, params['diff_threshold'], params['pixel_diff_value']):
                keyboard.press(Key.ctrl)
                keyboard.press(Key.home)
                keyboard.release(Key.home)
                keyboard.release(Key.ctrl)
                time.sleep(1)
                keyboard.press(Key.ctrl)
                keyboard.press(Key.tab)
                keyboard.release(Key.tab)
                keyboard.release(Key.ctrl)
            old_ss = new_ss

# Start automation in a separate thread
def start_automation():
    Thread(target=simulate_key_presses, daemon=True).start()

# GUI setup
def create_gui():
    def update_param(name, entry):
        try:
            params[name] = int(entry.get())
        except ValueError:
            pass

    root = tk.Tk()
    root.title("Office Break Automation")
    root.geometry("400x400")

    ttk.Label(root, text="Min Keys:").pack()
    min_keys_entry = ttk.Entry(root)
    min_keys_entry.insert(0, str(params['min_keys']))
    min_keys_entry.pack()

    ttk.Label(root, text="Max Keys:").pack()
    max_keys_entry = ttk.Entry(root)
    max_keys_entry.insert(0, str(params['max_keys']))
    max_keys_entry.pack()

    ttk.Label(root, text="Min Interval (s):").pack()
    min_interval_entry = ttk.Entry(root)
    min_interval_entry.insert(0, str(params['min_interval']))
    min_interval_entry.pack()

    ttk.Label(root, text="Max Interval (s):").pack()
    max_interval_entry = ttk.Entry(root)
    max_interval_entry.insert(0, str(params['max_interval']))
    max_interval_entry.pack()

    def on_start():
        update_param('min_keys', min_keys_entry)
        update_param('max_keys', max_keys_entry)
        update_param('min_interval', min_interval_entry)
        update_param('max_interval', max_interval_entry)
        start_automation()
        start_btn.config(state='disabled')

    start_btn = ttk.Button(root, text="Start Automation", command=on_start)
    start_btn.pack(pady=20)

    root.mainloop()

# Run GUI
if __name__ == '__main__':
    create_gui()
