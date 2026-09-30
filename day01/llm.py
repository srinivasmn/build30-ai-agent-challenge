import os

from dotenv import load_dotenv
from google import genai

from tracker import log_usage


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def ask_gemini(prompt: str):
    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL"),
        contents=prompt,
    )

    usage = response.usage_metadata
    log_usage(usage)

    return response.text, usage