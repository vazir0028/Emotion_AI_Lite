import streamlit as st
import cv2
import numpy as np
from fer import FER
import pandas as pd
import webbrowser

st.set_page_config(page_title="Emotion Music Lite", layout="centered")

st.title("🎧 Emotion Based Music Recommendation")
st.write("Take selfie → Detect mood → Get Spotify songs")

detector = FER(mtcnn=True)

playlists = {
    "happy": "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC",
    "sad": "https://open.spotify.com/playlist/37i9dQZF1DX7qK8ma5wgG1",
    "angry": "https://open.spotify.com/playlist/37i9dQZF1DWYNSmSSRFIWg",
    "neutral": "https://open.spotify.com/playlist/37i9dQZF1DX2sUQwD7tbmL",
    "surprise": "https://open.spotify.com/playlist/37i9dQZF1DXa2PvUpywmrr",
    "fear": "https://open.spotify.com/playlist/37i9dQZF1DX4fpCWaHOned"
}

img = st.camera_input("Take a selfie")

if img:
    bytes_data = img.getvalue()
    np_arr = np.frombuffer(bytes_data, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = detector.detect_emotions(rgb)

    if result:
        emotions = result[0]["emotions"]
        emotion = max(emotions, key=emotions.get)
        confidence = emotions[emotion] * 100

        st.success(f"Detected Emotion: {emotion.upper()}")
        st.info(f"Confidence: {confidence:.2f}%")

        if st.button("🎵 Open Spotify Playlist"):
            webbrowser.open(playlists.get(emotion, playlists["neutral"]))

        st.subheader("📊 Emotion Scores")
        df = pd.DataFrame(
            emotions.items(),
            columns=["Emotion", "Score"]
        )
        st.bar_chart(df.set_index("Emotion"))

    else:
        st.warning("No face detected. Try again.")
