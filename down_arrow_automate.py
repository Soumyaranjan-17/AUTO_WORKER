import time
import random
from pynput.keyboard import Key, Controller

def endless_down_arrow_spammer(min_interval=10, max_interval=20, presses_per_interval=3):
    keyboard = Controller()

    print("🔁 Starting endless Down Arrow key simulation")
    print(f"⏱️  Time interval between sets: {min_interval}–{max_interval} seconds")
    print(f"⬇️  Key presses per set: {presses_per_interval}\n")

    count = 1
    while True:
        wait_time = random.randint(min_interval, max_interval)
        print(f"🕒 Set #{count}: Waiting {wait_time} seconds...")
        time.sleep(wait_time)

        print(f"🎯 Set #{count}: Pressing DOWN ARROW {presses_per_interval} times:")
        for i in range(1, presses_per_interval + 1):
            print(f"   ↳ Press #{i}")
            keyboard.press(Key.down)
            time.sleep(0.05)  # Hold key briefly
            keyboard.release(Key.down)
            time.sleep(0.1)   # Small gap between presses

        print(f"✅ Set #{count} completed.\n")
        count += 1

# === Parameters (you can customize these) ===
min_interval = 20          # Minimum wait time between sets (in seconds)
max_interval = 25         # Maximum wait time between sets (in seconds)
presses_per_interval = 3   # Number of Down Arrow presses per set

endless_down_arrow_spammer(min_interval, max_interval, presses_per_interval)
