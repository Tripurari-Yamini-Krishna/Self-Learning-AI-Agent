from pathlib import Path

from groq import APIConnectionError, APIStatusError, RateLimitError

from Agent.Brain import LearningAgent
from Agent.Memory import load_memory

HISTORY_FILE = (
    Path(__file__).resolve().parent
    / "Data"
    / "conversation_history.json"
)


def main():
    agent = LearningAgent()

    print("Hi, I am your personal agent. Type '/help' to see commands.\n")

    while True:
        user_message = input("You: ").strip()
        command = user_message.lower()

        if command == "exit":
            print("Agent: See you next time!")
            break

        if command == "/help":
            print("\nAvailable commands:")
            print("  /help         - Show available commands")
            print("  /memory       - View saved facts")
            print("  /history      - View recent conversations")
            print("  /clearhistory - Clear conversation history")
            print("  exit          - Close the agent\n")
            continue

        if command == "/memory":
            memory = load_memory()

            if memory:
                print("\nAgent's saved memory:")
                for key, value in memory.items():
                    print(f"- {key}: {value}")
            else:
                print("\nAgent: My memory is empty.")

            print()
            continue

        if command == "/history":
            history = agent.load_conversation_history()

            if history:
                print("\nRecent conversation history:")
                for item in history[-10:]:
                    if not isinstance(item, dict):
                        continue

                    if isinstance(item.get("user"), str):
                        print(f"\nYou: {item['user']}")

                    if isinstance(item.get("assistant"), str):
                        print(f"Agent: {item['assistant']}")
            else:
                print("\nAgent: No conversation history yet.")

            print()
            continue

        if command == "/clearhistory":
            confirmation = input(
                "Clear all conversation history? Type YES to confirm: "
            ).strip()

            if confirmation == "YES":
                HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
                HISTORY_FILE.write_text("[]", encoding="utf-8")
                agent.conversation_history = []
                print(
                    "Agent: Conversation history cleared. "
                    "Saved memories remain intact.\n"
                )
            else:
                print("Agent: History was not cleared.\n")

            continue

        if not user_message:
            continue

        try:
            response = agent.chat(user_message)
            print(f"\nAgent: {response}\n")

        except RateLimitError:
            print(
                "\nAgent: I've hit the API usage limit. "
                "Please wait a bit and try again.\n"
            )

        except APIConnectionError:
            print(
                "\nAgent: I couldn't connect to the AI service. "
                "Check your internet connection and try again.\n"
            )

        except APIStatusError as error:
            print(
                f"\nAgent: The AI service returned an error "
                f"(HTTP {error.status_code}). Please try again later.\n"
            )

        except Exception as error:
            print(
                f"\nAgent: Something unexpected went wrong "
                f"({type(error).__name__}). Please try again.\n"
            )


if __name__ == "__main__":
    main()
