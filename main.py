import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def show_verbose(user_prompt, prompt_tokens, response_tokens):
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")


def main():
    if len(sys.argv) < 2:
        sys.exit(1)

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    user_prompt = sys.argv[1]

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
    )

    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        show_verbose(
            user_prompt, 
            response.usage_metadata.prompt_token_count,
            response.usage_metadata.candidates_token_count
        )

if __name__ == "__main__":
    main()