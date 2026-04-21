# app.py
import streamlit as st
from PIL import Image
import numpy as np
from fer import FER
import pandas as pd
import webbrowser

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(
    page_title="Emotion Music AI Lite",
    page_icon="🎵",
    layout="centered"
)

st.title("🎵 Emotion Based Music Recommendation")
st.write("Take a selfie → Detect mood → Open Spotify playlist")

# ------------------------------
# LOAD FER MODEL
# ------------------------------
detector = FER()

# ------------------------------
# PLAYLISTS
# ------------------------------
playlists = {
    "happy": "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC",
    "sad": "https://open.spotify.com/playlist/37i9dQZF1DX7qK8ma5wgG1",
    "angry": "https://open.spotify.com/playlist/37i9dQZF1DWYNSmSSRFIWg",
    "neutral": "https://open.spotify.com/playlist/37i9dQZF1DX2sUQwD7tbmL",
    "fear": "https://open.spotify.com/playlist/37i9dQZF1DX4fpCWaHOned",
    "surprise": "https://open.spotify.com/playlist/37i9dQZF1DXa2PvUpywmrr"
}

# ------------------------------
# CAMERA INPUT
# ------------------------------
img_file = st.camera_input("Take a selfie")

if img_file is not None:
    # Read image with PIL
    image = Image.open(img_file)

    # Show image
    st.image(image, caption="Captured Image", use_container_width=True)

    # Convert to RGB numpy array
    img_array = np.array(image.convert("RGB"))

    # Detect emotions
    result = detector.detect_emotions(img_array)

    if result:
        emotions = result[0]["emotions"]
        dominant_emotion = max(emotions, key=emotions.get)
        confidence = emotions[dominant_emotion] * 100

        st.success(f"Detected Emotion: {dominant_emotion.upper()}")
        st.info(f"Confidence: {confidence:.2f}%")

        # Chart
        st.subheader("Emotion Scores")
        df = pd.DataFrame(
            list(emotions.items()),
            columns=["Emotion", "Score"]
        )
        st.bar_chart(df.set_index("Emotion"))

        # Open Spotify
        playlist = playlists.get(
            dominant_emotion,
            playlists["neutral"]
        )

        if st.button("🎧 Open Spotify Playlist"):
            webbrowser.open(playlist)

    else:
        st.warning("No face detected. Try again.")
