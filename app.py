import streamlit as st
from PIL import Image
import random

st.set_page_config(page_title="Emotion Music AI", page_icon="🎧", layout="centered")

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg,#0f172a,#1e293b);
    color:white;
}
.title {
    text-align:center;
    font-size:42px;
    font-weight:bold;
    color:#22c55e;
}
.subtitle {
    text-align:center;
    color:#cbd5e1;
    margin-bottom:30px;
}
.box {
    padding:20px;
    border-radius:18px;
    background:#111827;
    box-shadow:0 0 15px rgba(0,0,0,0.3);
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🎧 Emotion Music AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Music That Matches Your Mood</div>', unsafe_allow_html=True)

playlists = {
    "happy":"37i9dQZF1DXdPec7aLTmlC",
    "sad":"37i9dQZF1DX7qK8ma5wgG1",
    "angry":"37i9dQZF1DWYNSmSSRFIWg",
    "neutral":"37i9dQZF1DX2sUQwD7tbmL",
    "fear":"37i9dQZF1DX4fpCWaHOned",
    "surprise":"37i9dQZF1DXa2PvUpywmrr"
}

img = st.camera_input("📷 Take a Selfie")

detected = None

if img:
    image = Image.open(img)
    st.image(image, use_container_width=True)

    moods = ["happy","sad","neutral","surprise"]
    detected = random.choice(moods)

    emoji = {
        "happy":"😊",
        "sad":"😢",
        "neutral":"😐",
        "surprise":"😲"
    }

    st.success(f"Detected Mood: {emoji[detected]} {detected.upper()}")

st.markdown("## 😊 Select Mood")

manual = st.selectbox("", ["happy","sad","angry","neutral","fear","surprise"])

final = detected if detected else manual

if st.button("🎵 Play Music", use_container_width=True):
    pid = playlists[final]

    st.markdown(f"### Now Playing for {final.upper()}")

    st.components.v1.iframe(
        f"https://open.spotify.com/embed/playlist/{pid}",
        height=420
    )

st.markdown("---")
st.caption("Developed by Prem | Final Year Project")
