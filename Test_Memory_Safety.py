from unittest.mock import patch
from Agent.Brain import LearningAgent
from Agent.Memory import load_memory, save_memory

agent = LearningAgent()
original_memory = load_memory().copy()
try:
    # Test 1: Save a new fact without calling Groq.
    with patch.object(
        agent,
        "interpret_memory",
        return_value={
            "action": "remember",
            "key": "test fact",
            "value": "This is a test",
        },
    ):
        result = agent.handle_memory("test")
        assert result == "I've saved test fact: This is a test"
        assert load_memory().get("test fact") == "This is a test"
    print("PASS: Saving a fact")
    # Test 2: Reject an empty value.
    with patch.object(
        agent,
        "interpret_memory",
        return_value={
            "action": "remember",
            "key": "empty test",
            "value": "",
        },
    ):
        result = agent.handle_memory("test")
        assert result is None
        assert "empty test" not in load_memory()
    print("PASS: Rejecting empty facts")
    # Test 3: Do not delete a nonexistent fact.
    with patch.object(
        agent,
        "interpret_memory",
        return_value={
            "action": "forget",
            "key": "fact that does not exist",
        },
    ):
        result = agent.handle_memory("test")
        assert result == "I couldn't find that fact in memory."
        assert "test fact" in load_memory()
    print("PASS: Protecting unrelated memories")
    # Test 4: Forget the test fact.
    with patch.object(
        agent,
        "interpret_memory",
        return_value={
            "action": "forget",
            "key": "test fact",
        },
    ):
        result = agent.handle_memory("test")
        assert result == "I've forgotten test fact."
        assert "test fact" not in load_memory()
    print("PASS: Forgetting a fact")
finally:
    # Restore the exact original memory file.
    save_memory(original_memory)
print("\nAll memory safety tests passed.")