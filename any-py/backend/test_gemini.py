from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

# Get the API key from environment variables
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=GEMINI_API_KEY)

prompt = 'Create a simple JSON object with skills for web development. Return only valid JSON with no extra text.'

model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content(prompt)

print("Response text:", repr(response.text))
print("Response text clean:", response.text)
