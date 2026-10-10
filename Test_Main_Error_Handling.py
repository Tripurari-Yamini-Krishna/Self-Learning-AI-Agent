
from unittest.mock import MagicMock, patch
from groq import RateLimitError
import main

response = MagicMock()
response.request = MagicMock()
rate_limit_error = RateLimitError(
    "Simulated rate limit",
    response=response,
    body=None,
)
with patch(
    "builtins.input",
    side_effect=["What is machine learning?", "exit"],
):
    with patch("main.LearningAgent") as mock_agent:
        mock_agent.return_value.chat.side_effect = rate_limit_error
        with patch("builtins.print") as mock_print:
            main.main()
            printed_output = "\n".join(
                " ".join(str(arg) for arg in call.args)
                for call in mock_print.call_args_list
            )
            assert "API usage limit" in printed_output
            assert "See you next time!" in printed_output
print("PASS: API rate limits are handled gracefully.")
print("PASS: The agent continues and exits without crashing.")
print("\nAll main error-handling tests passed.")