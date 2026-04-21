import streamlit as st
from PIL import Image
import numpy as np

st.set_page_config(page_title="Emotion Music AI", page_icon="🎧")

st.title("🎧 Emotion Music AI")
st.write("Take selfie → Mood detected → Music starts")

playlists = {
    "happy":"37i9dQZF1DXdPec7aLTmlC",
    "sad":"37i9dQZF1DX7qK8ma5wgG1",
    "neutral":"37i9dQZF1DX2sUQwD7tbmL",
    "angry":"37i9dQZF1DWYNSmSSRFIWg"
}

def detect_mood(img):
    arr = np.array(img.convert("L"))  # grayscale
    brightness = arr.mean()

    if brightness > 170:
        return "happy"
    elif brightness > 120:
        return "neutral"
    elif brightness > 80:
        return "sad"
    else:
        return "angry"

img = st.camera_input("📷 Take Selfie")

if img:
    image = Image.open(img)
    st.image(image, use_container_width=True)

    mood = detect_mood(image)

    emoji = {
        "happy":"😊",
        "sad":"😢",
        "neutral":"😐",
        "angry":"😠"
    }

    st.success(f"Detected Mood: {emoji[mood]} {mood.upper()}")

    pid = playlists[mood]

    # Auto show player instantly
    st.components.v1.iframe(
        f"https://open.spotify.com/embed/playlist/{pid}",
        height=430
    )
