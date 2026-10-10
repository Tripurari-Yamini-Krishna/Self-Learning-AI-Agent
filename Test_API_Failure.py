from unittest.mock import patch

from Agent.Brain import LearningAgent
from Agent.Memory import load_memory


agent = LearningAgent()
original_memory = load_memory()

with patch.object(
    agent.client.chat.completions,
    "create",
    side_effect=RuntimeError("Simulated API failure"),
):
    try:
        agent.chat("What is machine learning?")
    except RuntimeError as error:
        assert str(error) == "Simulated API failure"
        print("PASS: API failure is raised without being hidden.")
    else:
        raise AssertionError("Expected the simulated API failure.")

assert load_memory() == original_memory
print("PASS: Saved memory remains unchanged after API failure.")

print("\nAll API failure tests passed.")
