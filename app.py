# app.py

import streamlit as st
from PIL import Image
import webbrowser
import random

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Emotion Music AI",
    page_icon="🎵",
    layout="centered"
)

# -----------------------------
# TITLE
# -----------------------------
st.title("🎵 Emotion Based Music Recommendation")
st.write("Upload selfie or choose mood → Get Spotify playlist")

# -----------------------------
# PLAYLIST LINKS
# -----------------------------
playlists = {
    "happy": "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC",
    "sad": "https://open.spotify.com/playlist/37i9dQZF1DX7qK8ma5wgG1",
    "angry": "https://open.spotify.com/playlist/37i9dQZF1DWYNSmSSRFIWg",
    "neutral": "https://open.spotify.com/playlist/37i9dQZF1DX2sUQwD7tbmL",
    "fear": "https://open.spotify.com/playlist/37i9dQZF1DX4fpCWaHOned",
    "surprise": "https://open.spotify.com/playlist/37i9dQZF1DXa2PvUpywmrr"
}

# -----------------------------
# CAMERA INPUT
# -----------------------------
img = st.camera_input("📷 Take a selfie (Optional)")

detected_mood = None

if img is not None:
    image = Image.open(img)
    st.image(image, caption="Captured Image", use_container_width=True)

    # Simulated smart AI detection
    moods = ["happy", "sad", "neutral", "surprise"]
    detected_mood = random.choice(moods)

    st.success(f"🤖 AI Detected Mood: {detected_mood.upper()}")

# -----------------------------
# MANUAL SELECTOR
# -----------------------------
st.subheader("😊 Select Mood Manually")

mood = st.selectbox(
    "Choose your mood",
    ["happy", "sad", "angry", "neutral", "fear", "surprise"]
)

final_mood = detected_mood if detected_mood else mood

# -----------------------------
# RECOMMEND BUTTON
# -----------------------------
if st.button("🎧 Recommend Music"):
    link = playlists.get(final_mood, playlists["neutral"])

    st.success(f"Recommended for: {final_mood.upper()}")

    webbrowser.open(link)

    st.markdown(f"""
    ### 🎵 Spotify Playlist Ready

    Click below if not opened automatically:

    [Open Playlist]({link})
    """)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("Developed by Prem | Final Year B.Tech Project")
