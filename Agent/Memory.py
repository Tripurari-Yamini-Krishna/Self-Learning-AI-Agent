import json
from pathlib import Path

MEMORY_FILE = (
    Path(__file__).resolve().parent.parent
    / "Data"
    / "memory.json"
)

def load_memory():
    if not MEMORY_FILE.exists():
        return {}
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            memory = json.load(file)
        if isinstance(memory, dict):
            return memory
        return {}
    except (OSError, json.JSONDecodeError):
        return {}

def save_memory(memory):
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory, file, indent=4, ensure_ascii=False)

def remember(key, value):
    memory = load_memory()
    memory[key.lower()] = value
    save_memory(memory)

def recall(key):
    memory = load_memory()
    return memory.get(key.lower())