# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

#VoiceBot UI with Gradio
import os
import gradio as gr

from doctor_brain import encode_image, analyze_image_with_query
from patient_voice import record_audio, transcribe_with_groq
from doctor_voice import text_to_speech_with_gtts, text_to_speech_with_elevenlabs

#load_dotenv()

system_prompt="""Masz zachowywać się jak profesjonalny lekarz — wiem, że nim nie jesteś, ale to do celów edukacyjnych.
Co znajduje się na tym zdjęciu? Czy widzisz na nim coś niepokojącego medycznie?
Jeśli postawisz diagnozę różnicową, zaproponuj także możliwe sposoby leczenia.
Nie używaj żadnych numerów ani znaków specjalnych w odpowiedzi.
Twoja odpowiedź ma być jednym długim akapitem, bez podziału na punkty.
Zawsze odpowiadaj tak, jakbyś mówił do prawdziwej osoby.
Nie mów „Na zdjęciu widzę...”, tylko mów „Z tego co widzę, wygląda na to, że masz...”.
Nie odpowiadaj jako model AI ani nie używaj markdowna — Twoja odpowiedź ma brzmieć jak od prawdziwego lekarza, nie jak od bota AI.
Odpowiedź ma być zwięzła — maksymalnie dwa zdania.
Bez żadnych wstępów — zacznij odpowiedź od razu."""


def process_inputs(audio_filepath, image_filepath):
    speech_to_text_output = transcribe_with_groq(GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
                                                 audio_filepath=audio_filepath,
                                                 stt_model="whisper-large-v3")

    # Handle the image input
    if image_filepath:
        doctor_response = analyze_image_with_query(query=system_prompt+speech_to_text_output, encoded_image=encode_image(image_filepath), model="meta-llama/llama-4-scout-17b-16e-instruct")
    else:
        doctor_response = "No image provided for me to analyze"

    voice_of_doctor = text_to_speech_with_elevenlabs(input_text=doctor_response, output_filepath="final.mp3") 

    return speech_to_text_output, doctor_response, voice_of_doctor


# Create the interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio("Temp.mp3")
    ],
    title="AI Doctor with Vision and Voice"
)

iface.launch(share=True)

