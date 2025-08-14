import streamlit as st
from gtts import gTTS
import os
import time

# Birthday message
message = """
💖 Happy Birthday Mom! You mean the world to me...
"""

# Generate TTS only once
TTS_FILE = "birthday_message.mp3"
if not os.path.exists(TTS_FILE):
    tts = gTTS(text=message, lang='en')
    tts.save(TTS_FILE)

# Streamlit page settings
st.set_page_config(page_title="Birthday Surprise", layout="centered")

# Show typewriter effect
placeholder = st.empty()
typed = ""
for char in message:
    typed += char
    placeholder.markdown(typed)
    time.sleep(0.03)

# Audio player (visible)
st.markdown("### 🎵 Click below to hear your surprise!")
audio_file = open(TTS_FILE, 'rb')
st.audio(audio_file.read(), format='audio/mp3')
