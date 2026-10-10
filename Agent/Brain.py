import json
import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

from Agent.Memory import load_memory, save_memory

load_dotenv()

PROJECT_DIR = Path(__file__).resolve().parent.parent
HISTORY_FILE = PROJECT_DIR / "Data" / "conversation_history.json"
MODEL = "openai/gpt-oss-20b"


class LearningAgent:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env")

        self.client = Groq(api_key=api_key)
        self.memory = load_memory()
        self.conversation_history = self.load_conversation_history()

    def load_conversation_history(self):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as file:
                history = json.load(file)

            return history if isinstance(history, list) else []

        except (OSError, json.JSONDecodeError):
            return []

    def save_conversation_history(self):
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        self.conversation_history = self.conversation_history[-20:]

        temporary_file = HISTORY_FILE.with_suffix(".tmp")

        with open(temporary_file, "w", encoding="utf-8") as file:
            json.dump(
                self.conversation_history,
                file,
                indent=4,
                ensure_ascii=False,
            )
            file.flush()
            os.fsync(file.fileno())

        os.replace(temporary_file, HISTORY_FILE)

    def interpret_memory(self, message):
        prompt = f"""
You manage memory for a personal AI assistant.

Existing memory:
{json.dumps(self.memory, ensure_ascii=False)}

Return ONLY valid JSON using one of these formats:
Save or update:
{{"action":"remember","key":"short descriptive key","value":"fact"}}

Forget:
{{"action":"forget","key":"existing memory key"}}

No memory action:
{{"action":"none"}}

Instructions:
- Save stable personal facts and facts the user asks you to remember.
- Understand natural language, not just explicit "remember" requests.
- Recognize preferences, identity, studies, work, location, interests,
  and other useful long-term personal facts.
- Examples include:
  "Java is my favourite programming language."
  "I'm a computer science student."
  "I switched to Java recently."
  "Actually, I prefer C++ now."
  "Call me Mini."
  "I don't use Python anymore; I prefer Java."
- When a fact corrects or replaces an existing fact, update its existing
  key rather than creating a duplicate.
- If a statement clearly says an existing fact is no longer true, update
  or remove that fact as appropriate.
- Only forget a fact when the user clearly asks to forget or remove it,
  or clearly withdraws that fact.
- Do not save ordinary questions, hypothetical situations, quoted examples,
  or temporary remarks as personal facts.
- Never invent personal facts.
- For a forget action, use the existing memory key.
- If uncertain whether the message should change memory, return action "none".

User message: {message}
"""

        response = self.client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=500,
        )

        try:
            result = json.loads(response.choices[0].message.content or "")

            if isinstance(result, dict):
                return result

        except (json.JSONDecodeError, TypeError):
            pass

        return {"action": "none"}

    def handle_memory(self, message):
        result = self.interpret_memory(message)

        if not isinstance(result, dict):
            return None

        action = result.get("action")
        self.memory = load_memory()

        if action == "remember":
            key = result.get("key")
            value = result.get("value")

            if not isinstance(key, str) or not isinstance(value, str):
                return None

            key = key.strip().lower()
            value = value.strip()

            if not key or not value:
                return None

            existing_key = next(
                (
                    saved
                    for saved in self.memory
                    if saved.lower() == key
                ),
                None,
            )

            if existing_key is not None:
                key = existing_key

            self.memory[key] = value
            save_memory(self.memory)

            return f"I've saved {key}: {value}"

        if action == "forget":
            key = result.get("key")

            if not isinstance(key, str):
                return None

            key = key.strip().lower()

            existing_key = next(
                (
                    saved
                    for saved in self.memory
                    if saved.lower() == key
                ),
                None,
            )

            if existing_key is None:
                return "I couldn't find that fact in memory."

            del self.memory[existing_key]
            save_memory(self.memory)

            return f"I've forgotten {existing_key}."

        return None

    def chat(self, message):
        self.memory = load_memory()
        message_lower = message.lower().strip()

        memory_phrases = (
            "remember ",
            "don't forget ",
            "do not forget ",
            "forget ",
            "my name is ",
            "call me ",
            "you can call me ",
            "my favourite ",
            "my favorite ",
            "my new favourite ",
            "my new favorite ",
            "my fav ",
            "my new fav ",
            "i prefer ",
            "i like ",
            "i love ",
            "i live in ",
            "i work as ",
            "i work at ",
            "i study ",
            "i am studying ",
            "i'm studying ",
            "i am a ",
            "i'm a ",
            "i switched to ",
            "i have switched to ",
            "i changed to ",
            "i no longer ",
            "i don't use ",
            "i do not use ",
            "i stopped using ",
            "i started using ",
            "i'm no longer ",
            "i am no longer ",
            "my current ",
            "my updated ",
            "from now on, i ",
            "from now on i ",
            "actually, i prefer ",
            "actually i prefer ",
            "actually, i ",
            "actually i ",
        )

        memory_patterns = (
            " is my favourite ",
            " is my favorite ",
            " is my fav ",
            " is my new favourite ",
            " is my new favorite ",
            " is my new fav ",
            " is no longer my ",
            " isn't my favourite ",
            " isn't my favorite ",
            " is not my favourite ",
            " is not my favorite ",
            " has changed to ",
        )

        should_check_memory = (
            message_lower.startswith(memory_phrases)
            or any(
                pattern in message_lower
                for pattern in memory_patterns
            )
        )

        memory_response = None

        if should_check_memory:
            memory_response = self.handle_memory(message)

        if memory_response:
            answer = memory_response

        else:
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful personal AI assistant. Use saved "
                        "memory when relevant. Never invent personal facts or "
                        "claim to remember unavailable information. Be honest "
                        "when uncertain.\n\nSaved memory:\n"
                        + json.dumps(
                            self.memory,
                            ensure_ascii=False,
                            indent=2,
                        )
                    ),
                }
            ]

            for item in self.conversation_history[-10:]:
                if not isinstance(item, dict):
                    continue

                if isinstance(item.get("user"), str):
                    messages.append({
                        "role": "user",
                        "content": item["user"],
                    })

                if isinstance(item.get("assistant"), str):
                    messages.append({
                        "role": "assistant",
                        "content": item["assistant"],
                    })

            messages.append({
                "role": "user",
                "content": message,
            })

            response = self.client.chat.completions.create(
                model=MODEL,
                messages=messages,
                max_completion_tokens=700,
            )

            answer = (
                response.choices[0].message.content
                or "I couldn't generate a response."
            )

        self.conversation_history.append({
            "user": message,
            "assistant": answer,
        })

        self.save_conversation_history()

        return answer
