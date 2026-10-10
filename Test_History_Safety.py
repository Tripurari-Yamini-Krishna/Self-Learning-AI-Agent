import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from Agent.Brain import LearningAgent


agent = LearningAgent()

with tempfile.TemporaryDirectory() as temp_dir:
    test_file = Path(temp_dir) / "conversation_history.json"

    test_cases = [
        ("Empty history", "[]", []),
        ("Wrong data type", '{"user": "hello"}', []),
        ("Corrupted JSON", "{broken json", []),
    ]

    for name, content, expected in test_cases:
        test_file.write_text(content, encoding="utf-8")

        with patch("Agent.Brain.HISTORY_FILE", test_file):
            result = agent.load_conversation_history()

        assert result == expected, f"{name} failed: {result}"
        print(f"PASS: {name}")

print("\nAll conversation-history safety tests passed.")
