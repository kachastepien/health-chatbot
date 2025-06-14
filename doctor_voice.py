#Step 1a Setup Text to Speech-TTS-model (gTTS)
import os
from gtts import gTTS
from dotenv import load_dotenv
load_dotenv()

def text_to_speech_with_gtts_old(input_text, output_filepath):
    language= 'pl'
    audioobj= gTTS(
        text =input_text,
        lang = language,
        slow = False
    )
    audioobj.save(output_filepath)

input_text= "tekst do przeczytania"

# text_to_speech_with_gtts_old(
#     input_text= input_text,
#     output_filepath="gtts_testing.mp3"
# )
#Step 1b Setup Text to Speech-TTS-model  (ElevenLabs)
import elevenlabs
from elevenlabs import ElevenLabs

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

def text_to_speech_with_elevenlabs_old(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.text_to_speech.convert(
        text=input_text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        output_format="mp3_22050_32",
        model_id="eleven_multilingual_v2",
    )
    elevenlabs.save(audio, output_filepath)

# text_to_speech_with_elevenlabs_old(input_text, output_filepath="elevenlabs_testing.mp3")
#Step 2 Use Model for Text output to Voice
import subprocess
import platform

def text_to_speech_with_gtts(input_text, output_filepath):
    language= 'pl'
    audioobj= gTTS(
        text =input_text,
        lang = language,
        slow = False
    )
    audioobj.save(output_filepath)
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

# text_to_speech_with_gtts(
#     input_text= input_text,
#     output_filepath="gtts_testing_AUTOPLAY.mp3"
# )

input_text = "Jakis tekst!"

def text_to_speech_with_elevenlabs(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.text_to_speech.convert(
        text=input_text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        output_format="mp3_22050_32",
        model_id="eleven_multilingual_v2",
    )
    elevenlabs.save(audio, output_filepath)
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

#text_to_speech_with_elevenlabs(input_text, output_filepath="elevenlabs_testing_AUTOPLAY.mp3")
