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
running = False

# --- Logic Functions ---
def press_down(t, log):
    for i in range(1, t + 1):
        log(f"\u2193 Pressing DOWN ARROW #{i}")
        keyboard.press(Key.down)
        time.sleep(0.05)
        keyboard.release(Key.down)
        time.sleep(0.1)

def smooth_mouse_move_to(x_target, y_target, duration=0.5, steps=30):
    current_x, current_y = mouse.position
    dx = (x_target - current_x) / steps
    dy = (y_target - current_y) / steps
    delay = duration / steps
    for _ in range(steps):
        current_x += dx
        current_y += dy
        mouse.position = (int(current_x), int(current_y))
        time.sleep(delay)

def random_mouse_action(probability, log):
    if random.random() < (probability / 100.0):
        action = random.choice(['scroll', 'move'])
        if action == 'scroll':
            scroll_amount = random.randint(-3, 3)
            log(f"🖱️ Scrolling by {scroll_amount}")
            mouse.scroll(0, scroll_amount)
        elif action == 'move':
            screen_width, screen_height = pyautogui.size()
            x_offset = random.randint(-100, 100)
            y_offset = random.randint(-100, 100)
            current_x, current_y = mouse.position
            new_x = max(0, min(current_x + x_offset, screen_width))
            new_y = max(0, min(current_y + y_offset, screen_height))
            log(f"🖱️ Moving mouse smoothly to ({new_x}, {new_y})")
            smooth_mouse_move_to(new_x, new_y, duration=random.uniform(0.4, 1.0), steps=random.randint(25, 40))
    else:
        log("🖱️ No mouse movement this round.")

def start_simulation(min_i, max_i, presses, mouse_prob, log):
    global running
    running = True
    count = 1
    log("✅ Automation started\n")
    while running:
        wait_time = random.randint(min_i, max_i)
        log(f"⏳ Set #{count} waiting {wait_time}s...")
        time.sleep(wait_time)
        log(f"⚙️ Executing Set #{count}")
        press_down(presses, log)
        random_mouse_action(mouse_prob, log)
        log(f"✅ Completed Set #{count}\n")
        count += 1
    log("⏹️ Automation stopped.")

def stop_simulation():
    global running
    running = False

def run_in_thread(*args):
    thread = Thread(target=start_simulation, args=args, daemon=True)
    thread.start()

# --- GUI Setup ---
def create_gui():
    root = tk.Tk()
    root.title("Down Arrow + Mouse Automator")
    root.geometry("600x550")
    root.configure(bg='#f0f2f5')

    style = ttk.Style()
    style.configure("TLabel", font=("Segoe UI", 10))
    style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
    style.configure("TEntry", padding=4)

    def labeled_entry(label_text, default_value):
        frame = ttk.Frame(root)
        frame.pack(pady=5)
        label = ttk.Label(frame, text=label_text)
        label.pack(side='left', padx=5)
        entry = ttk.Entry(frame, width=10)
        entry.insert(0, default_value)
        entry.pack(side='left')
        return entry

    min_entry = labeled_entry("Minimum Interval (s):", "10")
    max_entry = labeled_entry("Maximum Interval (s):", "20")
    press_entry = labeled_entry("Key Presses per Interval:", "3")
    mouse_prob_entry = labeled_entry("Mouse Movement Probability (%):", "30")

    log_label = ttk.Label(root, text="Activity Log:", font=("Segoe UI", 10, "bold"))
    log_label.pack(pady=5)

    log_box = tk.Text(root, height=15, width=70, state='disabled', bg="#ffffff", fg="#333333", font=("Consolas", 10))
    log_box.pack(padx=10, pady=5)

    def log(msg):
        log_box.configure(state='normal')
        log_box.insert(tk.END, msg + '\n')
        log_box.see(tk.END)
        log_box.configure(state='disabled')

    button_frame = ttk.Frame(root)
    button_frame.pack(pady=15)

    def on_start():
        try:
            min_val = int(min_entry.get())
            max_val = int(max_entry.get())
            presses = int(press_entry.get())
            mouse_prob = float(mouse_prob_entry.get())
            if min_val > max_val:
                log("❌ Min interval must be <= Max interval.")
                return
            run_in_thread(min_val, max_val, presses, mouse_prob, log)
        except ValueError:
            log("❌ Invalid input. Please enter valid numbers.")

    start_btn = ttk.Button(button_frame, text="▶ Start", command=on_start)
    stop_btn = ttk.Button(button_frame, text="⏹ Stop", command=stop_simulation)
    start_btn.pack(side='left', padx=15)
    stop_btn.pack(side='right', padx=15)

    root.mainloop()

create_gui()
