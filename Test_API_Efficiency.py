from unittest.mock import patch, MagicMock
from Agent.Brain import LearningAgent

agent = LearningAgent()
# Test 1: Ordinary questions should skip memory interpretation.
with patch.object(
    agent,
    "interpret_memory",
    side_effect=AssertionError("Memory interpreter should not run"),
):
    with patch.object(agent.client.chat.completions, "create") as mock_api:
        mock_api.return_value.choices = [
            MagicMock(
                message=MagicMock(content="Machine learning teaches computers from data.")
            )
        ]
        response = agent.chat("What is machine learning?")
        assert "Machine learning" in response
        assert mock_api.call_count == 1
print("PASS: Ordinary messages use only one API call.")
# Test 2: A clear memory-style message should use the memory interpreter.
with patch.object(
    agent,
    "interpret_memory",
    return_value={
        "action": "remember",
        "key": "temporary test fact",
        "value": "temporary value",
    },
):
    with patch.object(agent, "save_conversation_history"):
        response = agent.chat("Remember this test fact.")
        assert response == "I've saved temporary test fact: temporary value"
print("PASS: Memory-style messages reach the memory handler.")
# Clean up the temporary test memory without calling the API.
from Agent.Memory import load_memory, save_memory
memory = load_memory()
memory.pop("temporary test fact", None)
save_memory(memory)
print("All API-efficiency tests passed.")