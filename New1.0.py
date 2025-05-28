import time
import random
from pynput.keyboard import Key, Controller

keyboard = Controller()

# === CONFIGURABLE SETTINGS ===
# --- General ---
initial_delay = 5              # Seconds before script starts
vscode_session_duration = 60   # Seconds
chrome_tab_session_duration = 56  # Seconds per tab
chrome_tab_switch_reserved = 4    # Reserved seconds for Ctrl+Home and Ctrl+Tab
chrome_tab_min = 2
chrome_tab_max = 5

# --- VS Code Settings ---
vscode_press_min = 2
vscode_press_max = 4
vscode_wait_min = 8
vscode_wait_max = 10
vscode_key_interval_min = 0.1
vscode_key_interval_max = 0.2

# --- Chrome Settings ---
chrome_press_min = 2
chrome_press_max = 5
chrome_wait_min = 8
chrome_wait_max = 10
chrome_key_interval_min = 0.1
chrome_key_interval_max = 0.2

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

    while time.time() - start_time < vscode_session_duration:
        press_count = random.randint(vscode_press_min, vscode_press_max)
        print("   ⏱️ Waiting before VS Code scroll set")
        time.sleep(random.randint(vscode_wait_min, vscode_wait_max))

        for _ in range(press_count):
            press_down_arrow()
            time.sleep(random.uniform(vscode_key_interval_min, vscode_key_interval_max))

    print("✅ VS Code Session Completed\n")

# === Level 3: Chrome Tab Activity ===
def chrome_tab_session():
    print("📑 Chrome Tab Session Started")
    tab_start = time.time()

    while time.time() - tab_start < chrome_tab_session_duration:
        press_count = random.randint(chrome_press_min, chrome_press_max)
        print("   ⏱️ Waiting before Chrome scroll set")
        time.sleep(random.randint(chrome_wait_min, chrome_wait_max))

        for _ in range(press_count):
            press_down_arrow()
            time.sleep(random.uniform(chrome_key_interval_min, chrome_key_interval_max))

    press_ctrl_home()
    time.sleep(1)
    switch_to_next_tab()
    time.sleep(2)
    print("✅ Chrome Tab Session Completed\n")

# === Level 2: Chrome Control ===
def control_chrome():
    print("🌐 Starting Chrome Control")
    alt_tab()
    tab_count = random.randint(chrome_tab_min, chrome_tab_max)

    for tab_num in range(tab_count):
        print(f"🔁 Tab #{tab_num+1} of {tab_count}")
        chrome_tab_session()

    print("✅ Chrome Session Completed\n")

# === Main Loop ===
def main_simulator():
    print("🚀 Welcome to the Automated Activity Simulator")
    print("🔁 Starting Simulated Activity")
    print(f"⏳ Waiting {initial_delay} seconds before starting...")
    for i in range(initial_delay, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    count = 1
    try:
        while True:
            print(f"\n🎬 ROUND #{count}")
            control_vscode()
            control_chrome()
            print(f"🌀 ROUND #{count} Completed\n")
            count += 1
    except KeyboardInterrupt:
        print("\n🛑 Simulation Stopped by User")

# === Run ===
main_simulator()
