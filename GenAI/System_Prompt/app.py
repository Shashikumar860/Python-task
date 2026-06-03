# ============================================================
# Install Packages:
# pip install google-genai python-dotenv
# ============================================================

import os
from google import genai
from google.genai import errors
from dotenv import load_dotenv

# ============================================================
# Load Environment Variables
# ============================================================

load_dotenv()

# ============================================================
# Generate Response
# ============================================================

def generate(question: str):

    # Gemini Client
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.0-flash"

    # Combined System Prompt with Classification & Generation
    system_prompt = """
    You are an AI learning assistant.
    
    FIRST, check if the question is related to:
    - Python
    - Python Programming
    - FastAPI
    - Flask
    - AI/ML
    - Programming concepts
    - Technical topics
    
    If YES, respond with a clear, concise, beginner-friendly explanation.
    
    If NO (greetings, random text, personal conversation, non-technical topics):
    Respond with: I'm currently designed to provide responses only for python platform-related learning queries. Please contact the administration team for further assistance.
    
    Be clear and structured in your response.
    """

    full_prompt = f"""
    {system_prompt}

    User Question:
    {question}
    """

    try:
        # Streaming Response
        print()
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=full_prompt,
        ):
            if chunk.text:
                print(chunk.text, end="")
        print("\n")
        
    except errors.ClientError as e:
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            print(
                "\n❌ API Quota Exceeded\n"
                "You've reached the free tier limit for today (20 requests/day).\n"
                "Please try again tomorrow or upgrade your plan at https://ai.google.dev\n"
            )
        else:
            print(f"\n❌ API Error: {str(e)}\n")
    except Exception as e:
        print(f"\n❌ Unexpected Error: {str(e)}\n")

# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    question = input("Enter your question: ")

    generate(question)