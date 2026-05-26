import subprocess
import webbrowser
import requests
import json
import os
import time
import sys
import pyttsx3

# =========================================================
# CONFIGURATION
# =========================================================

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3:latest"
MEMORY_FILE = "memory.json"

MAX_HISTORY = 6
AI_TIMEOUT = 120

# =========================================================
# MEMORY SYSTEM
# =========================================================

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except:
            pass

    return {
        "name": "Mr.Nilanjan",
        "chat_history": []
    }


def save_memory(memory):
    try:
        with open(MEMORY_FILE, "w") as f:
            json.dump(memory, f, indent=4)
    except:
        pass


memory = load_memory()

# =========================================================
# UI SYSTEM
# =========================================================

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def slow_print(text, delay=0.02):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def boot_screen():
    clear_screen()
    slow_print("J A R V I S", 0.05)
    time.sleep(0.3)
    slow_print("STATUS: ONLINE 🟢", 0.03)
    time.sleep(0.3)
    print()
    slow_print(f"Jarvis is now online. Welcome, {memory['name']}. We are now ready.", 0.02)
    print()

# =========================================================
# VOICE ENGINE
# =========================================================

engine = pyttsx3.init()
engine.setProperty("rate", 175)


def speak(text):
    print(f"\nJARVIS: {text}")
    engine.say(text)
    engine.runAndWait()

# =========================================================
# SYSTEM COMMAND ENGINE
# =========================================================

def open_application(app_name):
    try:
        subprocess.Popen(app_name, shell=True)
        return True
    except:
        return False


def run_system_command(command):
    c = command.lower()

    # ---------------- APPLICATIONS ----------------
    if "open chrome" in c:
        open_application("start chrome")
        return "Opening Chrome"

    if "open notepad" in c:
        open_application("notepad")
        return "Opening Notepad"

    if "open calculator" in c:
        open_application("calc")
        return "Opening Calculator"

    # ---------------- WEB ----------------
    if "open youtube" in c:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube"

    if "open google" in c:
        webbrowser.open("https://google.com")
        return "Opening Google"

    if "open github" in c:
        webbrowser.open("https://github.com")
        return "Opening GitHub"

    if "open instagram" in c:
        webbrowser.open("https://instagram.com")
        return "Opening Instagram"

    # ---------------- SYSTEM CONTROL (SAFE) ----------------
    if "shutdown" in c:
        return "Shutdown blocked for safety"

    if "restart" in c:
        return "Restart blocked for safety"

    return None

# =========================================================
# AI CORE ENGINE
# =========================================================

def build_prompt(prompt):
    system_prompt = f"""
You are JARVIS, a highly intelligent AI assistant.

User: {memory['name']}

Rules:
- Be natural
- Be helpful
- Keep responses moderately short
- Be accurate
"""

    history = ""
    for msg in memory["chat_history"][-MAX_HISTORY:]:
        if "user" in msg:
            history += f"User: {msg['user']}\n"
        if "jarvis" in msg:
            history += f"Jarvis: {msg['jarvis']}\n"

    full_prompt = system_prompt + "\n" + history + f"\nUser: {prompt}\nJarvis:"
    return full_prompt


def ask_ai(prompt):
    payload = {
        "model": MODEL,
        "prompt": build_prompt(prompt),
        "stream": False,
        "options": {
            "num_predict": 300,
            "temperature": 0.7
        }
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=AI_TIMEOUT
        )
        return response.json().get("response", "NO RESPONSE FROM AI")

    except Exception as e:
        return f"AI ERROR: {str(e)}"

# =========================================================
# MEMORY HANDLER
# =========================================================

def add_to_memory(user, response):
    memory["chat_history"].append({
        "user": user,
        "jarvis": response
    })
    save_memory(memory)

# =========================================================
# INPUT HANDLER
# =========================================================

def get_input():
    try:
        return input("\nroot@jarvis:// ").strip()
    except:
        return ""

# =========================================================
# RESPONSE HANDLER
# =========================================================

def handle_response(user_input):
    if user_input.lower() in ["exit", "quit", "stop"]:
        speak("Session terminated.")
        return False

    system_result = run_system_command(user_input)

    if system_result:
        print(system_result)
        return True

    print("\nprocessing...\n")
    reply = ask_ai(user_input)
    add_to_memory(user_input, reply)
    print("JARVIS:", reply)
    return True

# =========================================================
# MAIN ENGINE
# =========================================================

def main():
    boot_screen()
    speak(f"System online. Welcome back {memory['name']}.")

    print("\n====================================")
    print("   J A R V I S")
    print("   STATUS: ONLINE 🟢")
    print("====================================")

    while True:
        user_input = get_input()

        if not user_input:
            continue

        if not handle_response(user_input):
            break

# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":
    main()
