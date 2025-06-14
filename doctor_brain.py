import os
import base64
from groq import Groq

# Set API keys early
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")
# OPENAI_API_KEY = "..." # Not needed unless you're using OpenAI too

# Encode image
image_path = "acne.jpg"
with open(image_path, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

# Setup Groq client
client = Groq(api_key=GROQ_API_KEY)

query = "co ja mam kurwa na twarzy? czy to trądzik? co mam z tym zrobić?"
model = "meta-llama/llama-4-scout-17b-16e-instruct"

messages = [
    {
        "role": "system",
        "content": "Ej, ziomuś – masz odpowiadać jak kumpel z osiedla: na luzie, swojsko, bez zadęcia. Jak trzeba, to rzucaj luźnym tekstem, ale dalej konkretnie i pomocnie, okej?"
    },
    {
        "role": "user",
        "content": [
            {"type": "text", "text": query},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{encoded_image}",
                },
            },
        ],
    }
]

chat_completion = client.chat.completions.create(
    model=model,
    messages=messages
)

print(chat_completion.choices[0].message.content)
