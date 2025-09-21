import os
from dotenv import load_dotenv
import openai

# Load environment variables from .env
load_dotenv()

# Get the key from .env
api_key = os.getenv("OPENAI_API_KEY")

# Debug: Check if API key is loaded
print(f"API Key loaded: {'Yes' if api_key else 'No'}")
print(f"API Key length: {len(api_key) if api_key else 0}")

# Set the API key
openai.api_key = api_key

# Example call
try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say hello!"}]
    )
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Error: {e}")
