# app.py
import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
import random
from datetime import datetime

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Emotion Music AI Pro",
    page_icon="🎧",
    layout="wide"
)

# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg,#0f172a,#1e293b);
    color: white;
}
.block-container {
    padding-top: 2rem;
}
.title {
    text-align:center;
    font-size:42px;
    font-weight:700;
    color:#22c55e;
}
.subtitle {
    text-align:center;
    color:#cbd5e1;
    margin-bottom:30px;
}
.card {
    background:#111827;
    padding:20px;
    border-radius:18px;
    box-shadow:0 0 12px rgba(0,0,0,0.25);
}
.small {
    color:#94a3b8;
    font-size:14px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.markdown('<div class="title">🎧 Emotion Music AI Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI Powered Emotion + Personalized Music Recommendation</div>', unsafe_allow_html=True)

# -------------------------------------------------
# PLAYLIST DATABASE
# -------------------------------------------------
playlists = {
    "happy": "37i9dQZF1DXdPec7aLTmlC",
    "sad": "37i9dQZF1DX7qK8ma5wgG1",
    "neutral": "37i9dQZF1DX2sUQwD7tbmL",
    "angry": "37i9dQZF1DWYNSmSSRFIWg",
    "fear": "37i9dQZF1DX4fpCWaHOned",
    "surprise": "37i9dQZF1DXa2PvUpywmrr"
}

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------------------------------
# SIMPLE IMAGE-BASED MOOD DETECTION
# -------------------------------------------------
def detect_mood(img):
    gray = np.array(img.convert("L"))
    avg = gray.mean()

    if avg > 180:
        return "happy"
    elif avg > 140:
        return "neutral"
    elif avg > 100:
        return "sad"
    else:
        return "angry"

# -------------------------------------------------
# WELLNESS QUOTES
# -------------------------------------------------
quotes = {
    "sad": "🌈 Tough times never last. Better days are coming.",
    "angry": "🧘 Take a deep breath. Relax your mind.",
    "happy": "✨ Keep smiling and enjoy the moment!",
    "neutral": "🌿 Stay balanced and peaceful.",
    "fear": "💪 You are stronger than your fears.",
    "surprise": "🎉 Life is full of beautiful surprises!"
}

# -------------------------------------------------
# SIDEBAR OPTIONS
# -------------------------------------------------
st.sidebar.header("🎛 Personal Preferences")

genre = st.sidebar.selectbox(
    "Select Genre",
    ["Pop", "Lo-fi", "Romantic", "Workout", "Classical", "Bollywood"]
)

language = st.sidebar.selectbox(
    "Select Language",
    ["English", "Hindi", "Punjabi", "Marathi"]
)

energy = st.sidebar.slider(
    "Energy Level",
    1, 10, 5
)

# -------------------------------------------------
# MAIN LAYOUT
# -------------------------------------------------
col1, col2 = st.columns([1,1])

with col1:
    st.markdown("### 📷 Capture Your Mood")
    img = st.camera_input("Take a selfie")

with col2:
    st.markdown("### 📌 Recommendation Details")
    st.write(f"🎵 Genre: **{genre}**")
    st.write(f"🌍 Language: **{language}**")
    st.write(f"⚡ Energy Level: **{energy}/10**")

# -------------------------------------------------
# PROCESS IMAGE
# -------------------------------------------------
if img:
    image = Image.open(img)
    st.image(image, caption="Captured Image", use_container_width=True)

    mood = detect_mood(image)

    emoji = {
        "happy":"😊",
        "sad":"😢",
        "neutral":"😐",
        "angry":"😠"
    }

    # Save History
    st.session_state.history.append(mood)

    # Result Card
    st.markdown("## 🎯 Mood Detection Result")
    st.success(f"{emoji[mood]} Detected Mood: {mood.upper()}")

    # Quote
    st.info(quotes.get(mood, "Enjoy your music!"))

    # Spotify Playlist
    pid = playlists[mood]

    st.markdown("## 🎵 Recommended Playlist")

    st.components.v1.iframe(
        f"https://open.spotify.com/embed/playlist/{pid}",
        height=420
    )

# -------------------------------------------------
# ANALYTICS
# -------------------------------------------------
if st.session_state.history:
    st.markdown("## 📊 Mood Analytics Dashboard")

    df = pd.DataFrame(
        st.session_state.history,
        columns=["Mood"]
    )

    chart = df["Mood"].value_counts()

    st.bar_chart(chart)

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown("---")
st.caption("Developed by Prem | Final Year B.Tech Project")
