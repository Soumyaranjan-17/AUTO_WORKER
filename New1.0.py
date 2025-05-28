import time
import random
from pynput.keyboard import Key, Controller

keyboard = Controller()

# === Low-Level Utility ===
def press_key_combination(*keys):
    for key in keys:
        keyboard.press(key)
    time.sleep(0.1)
    for key in reversed(keys):
        keyboard.release(key)
    time.sleep(0.3)

def press_down_arrow():
    keyboard.press(Key.down)
    time.sleep(0.05)
    keyboard.release(Key.down)
    print("   ⬇️  Pressed Down Arrow")

def press_ctrl_home():
    print("   ⬆️  Pressing Ctrl + Home")
    press_key_combination(Key.ctrl, Key.home)

def switch_to_next_tab():
    print("   🔄 Switching Tab (Ctrl + Tab)")
    press_key_combination(Key.ctrl, Key.tab)

def alt_tab():
    print("   🔄 Switching Window (Alt + Tab)")
    press_key_combination(Key.alt, Key.tab)

# === Level 2: VS Code Control ===
def control_vscode():
    print("🧠 Starting VS Code Control")
    alt_tab()
    start_time = time.time()
    duration = 60  # 1 minute

    while time.time() - start_time < duration:
        press_count = random.randint(2, 4)
        print(f"   ⏱️ Waiting before VS Code scroll set")
        time.sleep(random.randint(8, 10))

        for _ in range(press_count):
            press_down_arrow()
            time.sleep(random.uniform(0.1, 0.2))

    print("✅ VS Code Session Completed\n")

# === Level 3: Chrome Tab Activity (1 Minute) ===
def chrome_tab_session():
    print("📑 Chrome Tab Session Started")
    tab_start = time.time()
    tab_duration = 56  # Reserve 4 seconds for Ctrl+Home + Ctrl+Tab

    while time.time() - tab_start < tab_duration:
        press_count = random.randint(2, 5)
        print("   ⏱️ Waiting before Chrome scroll set")
        time.sleep(random.randint(8, 10))

        for _ in range(press_count):
            press_down_arrow()
            time.sleep(random.uniform(0.1, 0.2))

    press_ctrl_home()
    time.sleep(1)
    switch_to_next_tab()
    time.sleep(2)
    print("✅ Chrome Tab Session Completed\n")

# === Level 2: Chrome Control ===
def control_chrome():
    print("🌐 Starting Chrome Control")
    alt_tab()
    tab_count = random.randint(2, 5)  # Random number of tabs to simulate

    for tab_num in range(tab_count):
        print(f"🔁 Tab #{tab_num+1} of {tab_count}")
        chrome_tab_session()

    print("✅ Chrome Session Completed\n")

# === Main Loop (Level 1) ===
def main_simulator():
    print("🚀 Welcome to the Automated Activity Simulator"  )
    print("🔁 Starting Simulated Activity\n")
    print("Waiting for 5 seconds before starting...")
    print("Move to Chrome")
    print("⏳ 5 seconds countdown:")
    for i in range(5, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    count = 1
    try:
        while True:
            print(f"🎬 ROUND #{count}")
            control_vscode()
            control_chrome()
            print(f"🌀 ROUND #{count} Completed\n")
            count += 1
    except KeyboardInterrupt:
        print("\n🛑 Simulation Stopped by User")

# === Run ===
main_simulator()
