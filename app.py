# app.py
# Emotion Music AI Pro - Version 4 Live Pro

import streamlit as st
import cv2
import av
import numpy as np
from fer import FER
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(page_title="Emotion Music AI Pro", page_icon="🎧", layout="wide")

# ---------------------------------------------------
# CSS
# ---------------------------------------------------
st.markdown("""
<style>
.main {background:#0f172a;color:white;}
h1 {text-align:center;color:#22c55e;}
.sidebar .sidebar-content {background:#111827;}
</style>
""", unsafe_allow_html=True)

st.title("🎧 Emotion Music AI Pro")
st.write("Live Face Detection + Emotion Based Music Recommendation")

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
genre = st.sidebar.selectbox(
    "🎵 Select Genre",
    ["Pop", "Lo-fi", "Workout", "Romantic", "Bollywood", "Classical"]
)

language = st.sidebar.selectbox(
    "🌍 Select Language",
    ["English", "Hindi", "Punjabi", "Marathi"]
)

# ---------------------------------------------------
# PLAYLISTS
# ---------------------------------------------------
playlists = {
    "happy": "37i9dQZF1DXdPec7aLTmlC",
    "sad": "37i9dQZF1DX7qK8ma5wgG1",
    "neutral": "37i9dQZF1DX2sUQwD7tbmL",
    "angry": "37i9dQZF1DWYNSmSSRFIWg",
    "fear": "37i9dQZF1DX4fpCWaHOned",
    "surprise": "37i9dQZF1DXa2PvUpywmrr"
}

# ---------------------------------------------------
# FACE DETECTOR
# ---------------------------------------------------
faceCascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

detector = FER(mtcnn=False)

# ---------------------------------------------------
# VIDEO PROCESSOR
# ---------------------------------------------------
class EmotionProcessor(VideoProcessorBase):

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(60, 60)
        )

        for (x, y, w, h) in faces:
            # GREEN BOX
            cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 2)

            face = img[y:y+h, x:x+w]

            try:
                result = detector.top_emotion(face)

                if result:
                    emotion, score = result
                    text = f"{emotion} ({score:.2f})"

                    cv2.putText(
                        img,
                        text,
                        (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0,255,0),
                        2
                    )

                    st.session_state["emotion"] = emotion

            except:
                pass

        if len(faces) == 0:
            st.session_state["emotion"] = "No Face Detected"

        return av.VideoFrame.from_ndarray(img, format="bgr24")

# ---------------------------------------------------
# LIVE CAMERA
# ---------------------------------------------------
st.subheader("📷 Live Webcam")

ctx = webrtc_streamer(
    key="emotion-ai",
    video_processor_factory=EmotionProcessor,
    rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    },
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)

# ---------------------------------------------------
# RESULT
# ---------------------------------------------------
emotion = st.session_state.get("emotion", "No Face Detected")

st.subheader("🎯 Detected Emotion")
st.success(emotion)

# ---------------------------------------------------
# MUSIC
# ---------------------------------------------------
if emotion in playlists:

    st.subheader("🎵 Recommended Music")

    pid = playlists[emotion]

    st.components.v1.iframe(
        f"https://open.spotify.com/embed/playlist/{pid}",
        height=420
    )

else:
    st.warning("Please face camera properly.")

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("---")
st.caption("Developed by Prem | Final Year B.Tech Project")
