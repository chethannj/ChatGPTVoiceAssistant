🤖 AI Voice Assistant using Python + ChatGPT + Streamlit

Build your own Talking ChatGPT — an AI assistant that listens 🎤, understands 🧠, and talks back 🔊 — all built in Python using Streamlit and OpenAI GPT.

This project was created live on the ChethanAI Chronicles channel 🎥

🚀 Features

✅ Record your voice locally using sounddevice
✅ Transcribe audio to text using OpenAI Whisper / GPT-4o-mini-transcribe
✅ Send the transcribed text to OpenAI GPT for responses
✅ Convert GPT’s text reply to speech using pyttsx3 (TTS)
✅ Fully interactive Streamlit UI with text + voice chat
✅ Perfect for AI beginners, developers, and live demos

🧩 Tech Stack
Component	Purpose
Python 3.8+	Programming language
Streamlit	Frontend web UI
OpenAI GPT-4o-mini	Generates chatbot replies
OpenAI Whisper	Transcribes voice to text
sounddevice / soundfile	Local microphone recording
pyttsx3	Text-to-speech (offline, local playback)
🛠️ Installation

1️⃣ Clone the repo:

git clone https://github.com/chethannj/ChatGPTVoiceAssistant
cd ChatGPTVoiceAssistant

2️⃣ Create a virtual environment:

python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows

3️⃣ Install dependencies:

pip install -r requirements.txt

4️⃣ Add your OpenAI API Key:
Create a file named .env in the root folder:

OPENAI_API_KEY=sk-your-key-here

5️⃣ Run the app:

streamlit run app.py
👋 requirements.txt
streamlit
python-dotenv
openai
sounddevice
soundfile
pyttsx3

(Optionally add SpeechRecognition if you plan to use the STT fallback.)

🖙️ Usage

Click “Record” to capture your voice.

The app transcribes your speech → text using OpenAI Whisper.

GPT-4o-mini generates a reply 💬.

The reply is spoken out loud 🖙️ using pyttsx3.

You can also type messages directly in the chat box.

🎥 Live Demo

Watch the full 1-hour build + walkthrough on YouTube:
🔗 I Built a Talking ChatGPT in Python (1-Hour Course)

🧠 Architecture
User 🎤 → Streamlit UI → Python Backend → OpenAI GPT → pyttsx3 → Spoken Output 🔊 → User 👂
Flow Diagram:
┌──────────────────────┐        ┌─────────────────────────┐
│     User / Viewer    │        │    Streamlit Frontend   │
│  🎤 Speaks or types  │ ───→   │  - Chat text box        │
│                      │        │  - Record voice button  │
└──────────────────────┘        │  - Message display area  │
                                └──────────┬──────────────┘
                                           │
                                           ▼
                            ┌────────────────────────────┐
                            │ Streamlit App (Python)     │
                            │ - Saves voice input        │
                            │ - Transcribes (STT)        │
                            │ - Sends to GPT model       │
                            │ - Gets AI response         │
                            │ - Calls pyttsx3 (TTS)      │
                            └──────────┬─────────────────┘
                                       │
                                       ▼
                            ┌────────────────────────┐
                            │    User Output         │
                            │ - Hears AI reply 🔊    │
                            │ - Sees chat message 💬 │
                            └────────────────────────┘
💬 Example Prompts

Try asking:

“Hey, how are you doing today?”

“Tell me a fun fact about AI.”

“Explain recursion like I’m 5.”

“What’s your favorite programming language?”

🔥 Future Improvements

Add browser-based mic input using streamlit-webrtc

Use ElevenLabs or OpenAI TTS for natural voices

Add multi-language speech support

Integrate persistent chat history (SQLite / MongoDB)

🙌 Credits

Built by ChethanAI Chronicles
🎥 Live AI Coding | ChatGPT Projects | Voice Assistants | Python Tutorials

🧠 License

MIT License © 2025 — ChethanAI Chronicles
