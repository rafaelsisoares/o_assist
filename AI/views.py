from google import genai
from dotenv import load_dotenv
import os


def generate_text(user_input):
    load_dotenv()
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    interaction = client.interactions.create(
        model="gemini-3.1-flash-lite",
        input=user_input
    )

    return interaction.output_text
