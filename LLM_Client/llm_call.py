import os
from dotenv import load_dotenv
from openai import OpenAI
from .prompt import get_prompt

# Load environment variables from .env
load_dotenv()

# Get the key from .env
api_key = os.getenv("OPENAI_API_KEY")

# Debug: Check if API key is loaded
print(f"API Key loaded: {'Yes' if api_key else 'No'}")
print(f"API Key length: {len(api_key) if api_key else 0}")

# Create the OpenAI client
client = OpenAI(api_key=api_key)

# Example call with web search preview enabled
try:
    response = client.responses.create(
        model="gpt-5-nano",
        reasoning={"effort": "medium"},
        tools=[{"type": "web_search"}],
        input=get_prompt()
    )
    print(response.output_text)
except Exception as e:
    print(f"Error: {e}")
