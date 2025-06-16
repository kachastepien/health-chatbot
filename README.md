# 🩺 AI Health Chatbot

A voice- and image-enabled AI chatbot designed to support medical conversations in a natural, human-like way. Built for educational purposes and powered by OpenAI, Groq, Meta LLaMA, and ElevenLabs APIs.

## 💡 What it does

- Accepts **voice input** from the user describing symptoms  
- Accepts **image input** (e.g. a rash, wound, or medical photo)  
- Transcribes voice to text using **Groq Whisper**  
- Analyzes the image + query using **LLaMA 4**  
- Responds like a doctor (in natural language) with **context-aware diagnosis**  
- Converts the response to **natural-sounding speech** via ElevenLabs  
- Includes a **text-only OpenAI chat** for fast Q&A

> Built with Gradio, Python, and lots of medical curiosity 🧠

## ⚙️ Stack

- `Python 3.10+`
- `Gradio` – UI framework  
- `OpenAI` – chat-based Q&A  
- `Groq (Whisper)` – audio transcription  
- `Meta LLaMA` – image + text analysis  
- `ElevenLabs` – text-to-speech  
- `.env` – secrets & API keys

## 🔐 Login flow

Users must log in (via email & password) to unlock the chatbot and chat functionality.  
Fake auth for demo/testing purposes – no database storage involved.

## 🧪 How to run

1. Clone the repo  
2. Create a `.env` file with:
    ```env
    OPENAI_API_KEY=your_key_here
    GROQ_API_KEY=your_key_here
    ELEVEN_API_KEY=your_key_here
    ```
3. Run the app:
    ```bash
    python app.py
    ```
4. The Gradio interface will launch in your browser (with a public share link if needed).

## 🤖 System Prompt

The image-analyzing LLaMA model is guided with a carefully-crafted **medical system prompt**:
- Speaks like a real doctor  
- Offers differentials and potential treatments  
- Always direct, no markdown, no "As an AI..." disclaimers

## 🌍 Language

The app is currently in **Polish**, but can easily be adapted for multilingual use.

---

## 🚧 Disclaimer

This project is **for educational and demo purposes only**. It does **not provide real medical advice** and should not be used for actual diagnosis or treatment.

