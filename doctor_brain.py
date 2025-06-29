import os
import base64
from groq import Groq

# Set API keys early
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")

# Encode image
#image_path = "acne.jpg"

def encode_image(image_path):   
    image_file=open(image_path, "rb")
    return base64.b64encode(image_file.read()).decode('utf-8')

#Step3: Setup Multimodal LLM 
from groq import Groq

query="Is there something wrong with my face?"
model = "meta-llama/llama-4-scout-17b-16e-instruct"
#model="llama-3.2-90b-vision-preview" #Deprecated

def analyze_image_with_query(query, model, encoded_image=None):
    from groq import Groq
    client = Groq()

    # Przygotuj wiadomość — zawsze dodaj tekst
    content = [{"type": "text", "text": query}]

    # Dodaj obraz tylko jeśli istnieje
    if encoded_image:
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{encoded_image}",
            },
        })

    messages = [{
        "role": "user",
        "content": content
    }]

    # Teraz wyślij zapytanie
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )

    return response.choices[0].message.content
