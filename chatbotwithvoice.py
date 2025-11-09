# ---------------------------------------------------------------
# 🤖 AI Voice Assistant (Server-side mic recording)
# - Streamlit UI (text chat + server-side recording)
# - Records local mic using sounddevice (reliable for demos)
# - Transcribes with OpenAI (Whisper / gpt-4o-mini-transcribe)
# - Uses OpenAI GPT (gpt-4o-mini) for replies
# - Speaks replies locally with pyttsx3 (direct playback)
# ---------------------------------------------------------------

import os
import tempfile
import time
from datetime import datetime
from dotenv import load_dotenv
import streamlit as st

# Audio recording libs
try:
    import sounddevice as sd
    import soundfile as sf
    HAVE_SOUNDDEVICE = True
except Exception:
    sd = None
    sf = None
    HAVE_SOUNDDEVICE = False

# TTS (Text-to-Speech) converts written text into spoken audio 🗣️
try:
    import pyttsx3
    HAVE_TTS = True
except Exception:
    pyttsx3 = None
    HAVE_TTS = False

# OpenAI client
from openai import OpenAI

# -------------------------------
# Load env
# -------------------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("⚠️ Please add your OpenAI API key to a .env file (OPENAI_API_KEY=sk-...) and restart the app.")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)

# -------------------------------
# Page UI config
# -------------------------------
st.set_page_config(page_title="AI Voice Assistant", page_icon="🎙️", layout="centered")
st.title("🎙️ AI Voice Assistant")
st.write("Record with the Record button, or type. The AI replies and speaks back locally.")

# -------------------------------
# Session state
# -------------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": "You are a helpful, concise AI assistant."}]
if "last_record_path" not in st.session_state:
    st.session_state["last_record_path"] = None

# -------------------------------
# Helpers
# -------------------------------
def record_local(duration_seconds: int = 4, samplerate: int = 44100):
    """Record audio from the default input device and save to a temp wav file.
    Returns the temp file path or None on error.
    """
    if not HAVE_SOUNDDEVICE:
        st.error("sounddevice or soundfile not installed. Install: pip install sounddevice soundfile")
        return None
    try:
        # Inform user and record
        recording = sd.rec(int(duration_seconds * samplerate), samplerate=samplerate, channels=1, dtype="float32")
        sd.wait()
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        sf.write(tmp.name, recording, samplerate)
        return tmp.name
    except Exception as e:
        st.error(f"Recording failed: {e}")
        return None

def transcribe_with_openai_whisper(wav_path: str):
    """Transcribe file using OpenAI audio transcription endpoint (Whisper/gpt-4o-mini-transcribe)."""
    try:
        with open(wav_path, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",  # or "whisper-1"
                file=f
            )
        return transcript.text.strip()
    except Exception as e:
        st.error(f"Transcription error: {e}")
        return None

def speak_text_local(text: str, rate: int = 160):
    """Speak text via pyttsx3 on the machine running Streamlit."""
    if not HAVE_TTS:
        return False
    try:
        engine = pyttsx3.init()
        try:
            engine.setProperty("rate", rate)
        except Exception:
            pass
        engine.say(text)
        engine.runAndWait()
        engine.stop()
        del engine
        return True
    except Exception as e:
        st.warning(f"TTS error: {e}")
        return False

def call_openai_chat(messages):
    """Call OpenAI chat completions and return assistant text (or None)."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.6,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"OpenAI call failed: {e}")
        return None

# -------------------------------
# Sidebar controls
# -------------------------------
st.sidebar.header("Settings")
model = st.sidebar.selectbox("Model (chat)", ["gpt-4o-mini"], index=0)
tts_rate = st.sidebar.slider("TTS rate (speed)", 120, 200, 160)
record_seconds = st.sidebar.number_input("Record duration (sec)", min_value=1, max_value=20, value=4)
auto_speak = st.sidebar.checkbox("Auto speak AI replies (local)", value=True if HAVE_TTS else False)
st.sidebar.markdown("---")
if not HAVE_SOUNDDEVICE:
    st.sidebar.warning("sounddevice/soundfile not installed. Run: pip install sounddevice soundfile")
if not HAVE_TTS:
    st.sidebar.info("pyttsx3 not installed: pip install pyttsx3 to enable local speech")

# -------------------------------
# Show chat history
# -------------------------------
for msg in st.session_state["messages"][1:]:
    st.chat_message(msg["role"]).markdown(msg["content"])

# -------------------------------
# Recording controls (server-side)
# -------------------------------
st.subheader("🎤 Record from your computer")
st.markdown("Press Record, speak for the chosen duration, and the app will transcribe & send to GPT.")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🔴 Record"):
        if not HAVE_SOUNDDEVICE:
            st.error("sounddevice not available. Install sounddevice and soundfile.")
        else:
            st.info(f"Recording for {record_seconds} seconds — please speak now...")
            wav_path = record_local(duration_seconds=record_seconds)
            if wav_path:
                st.success("Recording finished, saved to temp file.")
                st.audio(wav_path)
                st.markdown(f"Saved file: `{wav_path}`")
                st.session_state["last_record_path"] = wav_path
                # Transcribe automatically
                st.info("Transcribing with OpenAI Whisper...")
                text = transcribe_with_openai_whisper(wav_path)
                if text:
                    st.chat_message("user").markdown(f"**(Voice)** {text}")
                    user_input = text
                    # Add to messages and process (reuse below flow)
                    st.session_state["messages"].append({"role": "user", "content": user_input})
                    # Generate reply
                    with st.chat_message("assistant"):
                        with st.spinner("Thinking... 💭"):
                            reply = call_openai_chat(st.session_state["messages"])
                            if reply is None:
                                reply = "⚠️ Could not get a reply from OpenAI."
                            st.markdown(reply)
                            st.session_state["messages"].append({"role": "assistant", "content": reply})
                            # Speak reply locally if enabled
                            if auto_speak and HAVE_TTS:
                                speak_text_local(reply, rate=tts_rate)
                else:
                    st.warning("Could not transcribe the recording. Try again.")
with col2:
    if st.button("🧹 Clear last recording"):
        if st.session_state.get("last_record_path"):
            try:
                os.remove(st.session_state["last_record_path"])
            except Exception:
                pass
        st.session_state["last_record_path"] = None
        st.info("Cleared last recording (if any).")

# -------------------------------
# Text chat input (fallback)
# -------------------------------
text_input = st.chat_input("Or type your message here...")
if text_input:
    user_text = text_input.strip()
    st.session_state["messages"].append({"role": "user", "content": user_text})
    st.chat_message("user").markdown(user_text)

    with st.chat_message("assistant"):
        with st.spinner("Thinking... 💭"):
            reply = call_openai_chat(st.session_state["messages"])
            if reply is None:
                reply = "⚠️ Could not get a reply from OpenAI."
            st.markdown(reply)
            st.session_state["messages"].append({"role": "assistant", "content": reply})
            if auto_speak and HAVE_TTS:
                speak_text_local(reply, rate=tts_rate)

# -------------------------------
# Clear chat
# -------------------------------
if st.button("🧹 Clear Chat"):
    st.session_state["messages"] = [st.session_state["messages"][0]]
    st.session_state["last_record_path"] = None
    st.experimental_rerun()

# -------------------------------
# Footer / notes
# -------------------------------
st.markdown("---")
st.write("Notes:")
st.write("- This app records using your computer mic (server-side). Keep the Streamlit tab open and run locally.")
st.write("- For transcription we use OpenAI’s transcription endpoint (Whisper/gpt-4o-mini-transcribe).")
st.write("- TTS uses pyttsx3 and plays on the same machine running the app.")
st.caption(f"AI Voice Assistant • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
