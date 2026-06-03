# To run this code you need to install the following dependencies:
# pip install google-genai python-dotenv
 
import os
from pathlib import Path
from google import genai
from dotenv import load_dotenv
 
dotenv_path = Path(__file__).resolve().with_name(".env")
load_dotenv(dotenv_path=dotenv_path)
 
def generate(question: str):
    api_key = os.environ.get("GEMINI_API_KEY")
 
    client = genai.Client(
        api_key=api_key,
    )
 
    model = "gemini-3-flash-preview"
 
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=question,
    ):
        if text := chunk.text:
            print(text, end="")
 
if __name__ == "__main__":
    question = input("Enter your question: ")
    generate(question)