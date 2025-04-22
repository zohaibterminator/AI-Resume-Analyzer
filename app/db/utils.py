import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_client():
    return genai.GenerativeModel(
        model_name="gemini-1.5-pro",
    )