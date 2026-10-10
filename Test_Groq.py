import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("Sending request to Groq...", flush=True)

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {"role": "user", "content": "Say hello in one short sentence."}
    ],
    max_completion_tokens=100,
)

print("Response received.", flush=True)
print("Finish reason:", response.choices[0].finish_reason)
print("Full response:", response.choices[0].message)
