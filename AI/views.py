from google import genai
from dotenv import load_dotenv
import os

INSTRUCTIONS = """
Você é um assistente pessoal.

Regras:
- Responda em português.
- Explique os conceitos e ideias de maneira clara.
- Dê exemplos quando for apropriado.
- Não invente informações.
"""


def generate_text(user_input):
    load_dotenv()
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    interaction = client.interactions.create(
        model="gemini-3.1-flash-lite",
        system_instruction=INSTRUCTIONS,
        input=user_input
    )

    return interaction.output_text
