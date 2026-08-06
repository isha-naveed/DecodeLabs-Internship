from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def get_ai_response(messages):
    """
    Sends conversation history to the Groq model
    and returns the assistant's reply.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
    )

    return response.choices[0].message.content