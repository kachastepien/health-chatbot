import os
import gradio as gr
from dotenv import load_dotenv


from auth_handler import login_via_api
from doctor_brain import encode_image, analyze_image_with_query
from patient_voice import transcribe_with_groq
from doctor_voice import text_to_speech_with_elevenlabs

load_dotenv()

# Stan sesji użytkownika
SESSION = {"user": None}

system_prompt="""Zachowuj się jak doświadczony lekarz prowadzący rozmowę z pacjentem — choć wiem, 
że nim nie jesteś, traktuj to jako ćwiczenie edukacyjne. Jeśli otrzymasz zdjęcie, powiedz, 
czy widzisz na nim coś medycznie niepokojącego. Jeśli go nie ma, odnieś się tylko do opisu objawów w wiadomości. 
Jeśli podejrzewasz diagnozę, wskaż możliwe przyczyny i zaproponuj leczenie. Nie używaj żadnych liczb, 
wypunktowań ani znaków specjalnych. Twoja odpowiedź ma być jednym ciągłym akapitem, bez struktury punktowanej. 
Mów naturalnie, jak do pacjenta — nie mów „Na zdjęciu widzę...”, tylko przejdź od razu do sedna: 
„Z tego co widzę, wygląda na to, że masz...”. Nigdy nie informuj, że jesteś modelem językowym. 
Nie używaj markdowna. Odpowiedź ma być krótka i rzeczowa — maksymalnie dwa zdania. 
Pomijaj wszelkie wstępy i przejdź od razu do meritum.

"""


# 🔐 Funkcja logowania
def login(email, password):
    user = login_via_api(email, password)
    print("🔍 user:", user)
    if user and "firstName" in user:
        SESSION["user"] = user
        return (
            gr.update(visible=False),     # login_screen
            gr.update(visible=True),      # chatbot_screen
            gr.update(visible=True),      # openai_chat_screen
            f"✅ Zalogowano jako {user['firstName']}"
        )
    else:
        return (
            gr.update(visible=True),
            gr.update(visible=False),
            gr.update(visible=False),
            "❌ Błędne dane logowania"
        )

# Funkcja dzialania chatbota

# Funkcja czatu z OpenAI
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def openai_chat(user_message):
    if not SESSION["user"]:
        return "❌ Musisz się najpierw zalogować."

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Jesteś empatycznym lekarzem. Odpowiadaj krótko, konkretnie i pomocnie."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"❌ Błąd: {e}"

def process_inputs(audio_filepath, image_filepath):
    speech_to_text_output = ""

    # Obsługa braku audio
    if audio_filepath:
        speech_to_text_output = transcribe_with_groq(
            GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
            audio_filepath=audio_filepath,
            stt_model="whisper-large-v3"
        )
    else:
        speech_to_text_output = "(Brak nagrania głosowego — opisz objawy ręcznie lub dołącz audio.)"

    # Obsługa obrazu
    encoded_img = None
    if image_filepath:
        try:
            encoded_img = encode_image(image_filepath)
        except Exception as e:
            print(f"⚠️ Błąd podczas kodowania obrazu: {e}")
            encoded_img = None

    # Analiza
    doctor_response = analyze_image_with_query(
        query=system_prompt + " " + speech_to_text_output,
        encoded_image=encoded_img,
        model="meta-llama/llama-4-scout-17b-16e-instruct"
    )

    # TTS
    voice_of_doctor = text_to_speech_with_elevenlabs(
        input_text=doctor_response,
        output_filepath="final.mp3"
    )

    return speech_to_text_output, doctor_response, voice_of_doctor


# 🧱 UI
with gr.Blocks() as app:
    # LOGIN SCREEN
    with gr.Column(visible=True) as login_screen:
        gr.Markdown("## 🔐 Zaloguj się do Sidly Chatbota")
        email = gr.Text(label="Email")
        password = gr.Text(label="Hasło", type="password")
        login_msg = gr.Textbox(label="Status", interactive=False)
        login_btn = gr.Button("Zaloguj")

    # OPENAI CHAT SCREEN
    with gr.Column(visible=False) as openai_chat_screen:
        gr.Markdown("## 💬 Chat Tekstowy z Lekarzem (OpenAI)")
        user_input = gr.Textbox(label="Zadaj pytanie", placeholder="Mam ból głowy od rana, co to może być?")
        chat_response = gr.Textbox(label="🧑‍⚕️ Odpowiedź", interactive=False)
        chat_btn = gr.Button("Wyślij pytanie")
    

    # CHATBOT SCREEN
    with gr.Column(visible=False) as chatbot_screen:
        gr.Markdown("## 🩺 Sidly Health Chatbot")
        audio_input = gr.Audio(sources=["microphone"], type="filepath", label="🎤 Nagraj objawy")
        image_input = gr.Image(type="filepath", label="📷 Dodaj zdjęcie (np. wysypki)")
        transcript = gr.Textbox(label="🗣 Rozpoznany tekst")
        response = gr.Textbox(label="🧑‍⚕️ Odpowiedź lekarza")
        voice_output = gr.Audio(label="🔊 Odpowiedź głosowa")
        submit_btn = gr.Button("Wyślij")

    # POWIĄZANIA
    login_btn.click(
        login,
        inputs=[email, password],
        outputs=[login_screen, chatbot_screen, openai_chat_screen, login_msg]
    )


    submit_btn.click(
        process_inputs,
        inputs=[audio_input, image_input],
        outputs=[transcript, response, voice_output]
    )
    chat_btn.click(
    openai_chat,
    inputs=[user_input],
    outputs=[chat_response]
    )


# START
app.launch(share=True)
