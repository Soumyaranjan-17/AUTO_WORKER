import tkinter as tk
from tkinter import ttk
from threading import Thread
import time
import random
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Controller as MouseController
import pyautogui

# Controllers
keyboard = KeyboardController()
mouse = MouseController()

# Flag for controlling the endless loop
running = False

def press_down(t, log_callback):
    for i in range(1, t + 1):
        log_callback(f"   ↳ Pressing DOWN ARROW #{i}")
        keyboard.press(Key.down)
        time.sleep(0.05)
        keyboard.release(Key.down)
        time.sleep(0.1)
def smooth_mouse_move_to(x_target, y_target, duration=0.5, steps=30):
    """Move the mouse smoothly to (x_target, y_target) over 'duration' seconds in 'steps'."""
    current_x, current_y = mouse.position
    dx = (x_target - current_x) / steps
    dy = (y_target - current_y) / steps
    delay = duration / steps

    for _ in range(steps):
        current_x += dx
        current_y += dy
        mouse.position = (int(current_x), int(current_y))
        time.sleep(delay)

def random_mouse_action(probability, log_callback):
    if random.random() < (probability / 100.0):
        action = random.choice(['scroll', 'move'])

        if action == 'scroll':
            scroll_amount = random.randint(-3, 3)
            log_callback(f"   🖱️ Scrolling mouse by {scroll_amount}")
            mouse.scroll(0, scroll_amount)

        elif action == 'move':
            screen_width, screen_height = pyautogui.size()
            x_offset = random.randint(-100, 100)
            y_offset = random.randint(-100, 100)
            current_x, current_y = mouse.position
            new_x = max(0, min(current_x + x_offset, screen_width))
            new_y = max(0, min(current_y + y_offset, screen_height))
            log_callback(f"   🖱️ Smoothly moving mouse to: ({new_x}, {new_y})")
            smooth_mouse_move_to(new_x, new_y, duration=random.uniform(0.4, 1.0), steps=random.randint(25, 40))
    else:
        log_callback("   🖱️ Skipping mouse action this time.")

def start_simulation(min_interval, max_interval, presses, mouse_prob, log_callback):
    global running
    running = True
    count = 1
    log_callback("✅ Simulation started.\n")
    while running:
        wait_time = random.randint(min_interval, max_interval)
        log_callback(f"🕒 Set #{count}: Waiting {wait_time} seconds...")
        time.sleep(wait_time)

        log_callback(f"🎯 Set #{count}: Executing actions:")
        press_down(presses, log_callback)
        random_mouse_action(mouse_prob, log_callback)
        log_callback(f"✅ Set #{count} completed.\n")
        count += 1
    log_callback("⏹️ Simulation stopped.\n")

def stop_simulation():
    global running
    running = False

def run_in_thread(*args):
    thread = Thread(target=start_simulation, args=args, daemon=True)
    thread.start()

# ==== GUI ====
def create_gui():
    root = tk.Tk()
    root.title("⬇️ Down Arrow Key + Mouse Automator")

    root.geometry("500x450")
    root.resizable(False, False)

    # Labels + Inputs
    ttk.Label(root, text="Min Interval (sec):").pack()
    min_entry = ttk.Entry(root)
    min_entry.insert(0, "10")
    min_entry.pack()

    ttk.Label(root, text="Max Interval (sec):").pack()
    max_entry = ttk.Entry(root)
    max_entry.insert(0, "20")
    max_entry.pack()

    ttk.Label(root, text="Key Presses per Interval:").pack()
    presses_entry = ttk.Entry(root)
    presses_entry.insert(0, "3")
    presses_entry.pack()

    ttk.Label(root, text="Mouse Movement Probability (%):").pack()
    mouse_prob_entry = ttk.Entry(root)
    mouse_prob_entry.insert(0, "30")
    mouse_prob_entry.pack()

    # Log Display
    log_box = tk.Text(root, height=15, width=60, wrap=tk.WORD, state='disabled', bg="#f4f4f4")
    log_box.pack(pady=10)

    def log_callback(message):
        log_box.configure(state='normal')
        log_box.insert(tk.END, message + "\n")
        log_box.see(tk.END)
        log_box.configure(state='disabled')

    # Buttons
    button_frame = ttk.Frame(root)
    button_frame.pack(pady=5)

    def on_start():
        try:
            min_val = int(min_entry.get())
            max_val = int(max_entry.get())
            presses = int(presses_entry.get())
            mouse_prob = float(mouse_prob_entry.get())

            if min_val > max_val:
                log_callback("❌ Min interval cannot be greater than max.")
                return

            run_in_thread(min_val, max_val, presses, mouse_prob, log_callback)
        except ValueError:
            log_callback("❌ Invalid input. Please enter valid numbers.")

    start_btn = ttk.Button(button_frame, text="▶ Start", command=on_start)
    start_btn.pack(side='left', padx=10)

    stop_btn = ttk.Button(button_frame, text="⏹ Stop", command=stop_simulation)
    stop_btn.pack(side='right', padx=10)

    root.mainloop()

create_gui()
