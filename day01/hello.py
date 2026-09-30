import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.models.generate_content(
    model=os.getenv("GEMINI_MODEL"),
    contents="Explain what an AI agent is in one sentence."
)

print(response.text)
print(response.usage_metadata)