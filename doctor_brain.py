#Setup GROQ API key
import os 
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
#Convert image to required format
import base64

image_path="acne.jpg"
image_file = open(image_path, "rb")
encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

#Setup Multimodal LLM
from groq import Groq

client = Groq()
query = "is there something wrong on my face?"
model = "meta-llama/llama-4-scout-17b-16e-instruct"
messages = [
    {
        "role": "user",
        "content":[
            {
                "type": "text",
                "text": query
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": "data:image/jpeg;base64, {base64_image}",
                },
            },
        ],
    }
]

chat_completion = client.chat.completions.create(
    model=model,
    messages=messages
)
#Print the response
print(chat_completion)