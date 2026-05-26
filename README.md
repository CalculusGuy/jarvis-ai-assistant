# JARVIS — Local Terminal AI Assistant

> "System online. Welcome back, Mr. Nilanjan."

A terminal-based personal AI assistant built in Python — combining local LLM intelligence, voice output, system execution, and memory into one lightweight agent.

---

## Features

- 🔊 **Voice greeting** — speaks on startup using text-to-speech
- 🤖 **Local LLM brain** — powered by Ollama (no cloud APIs needed)
- 💻 **System execution** — open Chrome, YouTube, Instagram, Calculator via terminal commands
- 🧠 **Memory system** — remembers your name and recent interactions via JSON
- 🖥️ **Clean terminal UI** — `root@jarvis://` prompt with status display

---

## How It Works
User input → Command Router
↓
Known command? → Execute on system (open app/website)
Unknown input? → Forward to local LLM → Jarvis-style response

---

## Setup

```bash
# Install Ollama and pull a model
ollama pull llama3

# Install dependencies
pip install pyttsx3

# Run JARVIS
python JARVIS.py
```

---

## Built With

- Python 3
- Ollama (local LLM)
- pyttsx3 (text-to-speech)
- subprocess / webbrowser (system execution)
- JSON (memory persistence)

---

*Built by Nilanjan Chowdhury — github.com/CalculusGuy*
