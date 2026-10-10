import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("API key not found. Check your .env file.")
else:
    client = genai.Client(api_key=api_key)
try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Reply with exactly:I am connected."
    )
    print("Gemini response:")
    print(response.text)
except Exception as error:
    print("Gemini connection failed.")
    print(error)