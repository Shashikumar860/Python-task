# To run this code you need to install the following dependencies:
# pip install google-genai
# pip install python-dotenv

from importlib.resources import contents
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate(question: str):
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-3-flash-preview"

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=question,
    ):
        if text := chunk.text:
            print(text, end="")

if __name__ == "__main__":
    question = "Define Python in 3 lines"
    generate(question)