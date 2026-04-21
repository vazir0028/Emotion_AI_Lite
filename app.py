# app.py
# Emotion Music AI Pro - Version 5 Final Year Premium

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from PIL import Image
import numpy as np
import random

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Emotion Music AI Premium",
    page_icon="🎧",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg,#0f172a,#111827);
    color: white;
}
.block-container {
    padding-top: 2rem;
}
h1 {
    text-align:center;
    color:#22c55e;
}
.card {
    background:#1f2937;
    padding:20px;
    border-radius:18px;
}
</style>
""", unsafe_allow_html=True)

st.title("🎧 Emotion Music AI Premium")
st.write("AI Based Emotion Recognition + Personalized Music Therapy System")

# ---------------------------------------------------
# DATABASE
# ---------------------------------------------------
conn = sqlite3.connect("emotion_data.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS history (
id INTEGER PRIMARY KEY AUTOINCREMENT,
date TEXT,
emotion TEXT,
genre TEXT,
language TEXT
)
""")
conn.commit()

# ---------------------------------------------------
# PLAYLISTS
# ---------------------------------------------------
playlists = {
    "happy": "37i9dQZF1DXdPec7aLTmlC",
    "sad": "37i9dQZF1DX7qK8ma5wgG1",
    "neutral": "37i9dQZF1DX2sUQwD7tbmL",
    "angry": "37i9dQZF1DWYNSmSSRFIWg"
}

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.header("🎛 Personalization")

genre = st.sidebar.selectbox(
    "Select Genre",
    ["Pop", "Lo-fi", "Workout", "Bollywood", "Romantic", "Classical"]
)

language = st.sidebar.selectbox(
    "Select Language",
    ["English", "Hindi", "Punjabi", "Marathi"]
)

# ---------------------------------------------------
# SIMPLE MOOD DETECTION
# ---------------------------------------------------
def detect_emotion(image):
    gray = np.array(image.convert("L"))
    avg = gray.mean()

    if avg > 180:
        return "happy"
    elif avg > 130:
        return "neutral"
    elif avg > 90:
        return "sad"
    else:
        return "angry"

# ---------------------------------------------------
# QUOTES
# ---------------------------------------------------
quotes = {
    "happy": "✨ Keep smiling and spread positivity.",
    "sad": "🌈 Better days are coming.",
    "neutral": "🌿 Stay calm and balanced.",
    "angry": "🧘 Relax. Take a deep breath."
}

# ---------------------------------------------------
# MAIN TABS
# ---------------------------------------------------
tab1, tab2, tab3 = st.tabs(
    ["🎥 Live Detection", "📊 Dashboard", "ℹ About Project"]
)

# ---------------------------------------------------
# TAB 1
# ---------------------------------------------------
with tab1:

    st.subheader("📷 Camera Input")

    img = st.camera_input("Take a selfie")

    if img:

        image = Image.open(img)
        st.image(image, width=350)

        emotion = detect_emotion(image)

        st.success(f"Detected Mood: {emotion.upper()}")

        st.info(quotes[emotion])

        # Save to DB
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            "INSERT INTO history(date,emotion,genre,language) VALUES (?,?,?,?)",
            (now, emotion, genre, language)
        )
        conn.commit()

        # Spotify
        st.subheader("🎵 Recommended Playlist")

        pid = playlists[emotion]

        st.components.v1.iframe(
            f"https://open.spotify.com/embed/playlist/{pid}",
            height=420
        )

# ---------------------------------------------------
# TAB 2
# ---------------------------------------------------
with tab2:

    st.subheader("📊 Mood Analytics")

    df = pd.read_sql_query("SELECT * FROM history", conn)

    if len(df) > 0:

        st.write("### Recent Records")
        st.dataframe(df.tail(10), use_container_width=True)

        st.write("### Emotion Count")
        st.bar_chart(df["emotion"].value_counts())

        st.write("### Language Preference")
        st.bar_chart(df["language"].value_counts())

        st.write("### Genre Preference")
        st.bar_chart(df["genre"].value_counts())

    else:
        st.warning("No data available yet.")

# ---------------------------------------------------
# TAB 3
# ---------------------------------------------------
with tab3:

    st.subheader("🎓 Final Year Project Details")

    st.markdown("""
### Project Title:
AI Based Emotion Recognition and Personalized Music Therapy System

### Technologies Used:
- Python
- Streamlit
- SQLite
- NumPy
- Pandas
- Spotify Embed API

### Modules:
1. Camera Input  
2. Emotion Detection  
3. Recommendation Engine  
4. Database Logging  
5. Analytics Dashboard

### Future Scope:
- Real Face Detection AI
- Deep Learning Model
- Voice Emotion Detection
- Mobile App Deployment
""")

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("---")
st.caption("Developed by Prem | Final Year B.Tech Project")
