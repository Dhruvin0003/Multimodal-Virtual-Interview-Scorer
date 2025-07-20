import streamlit as st
import requests
import os
import matplotlib.pyplot as plt

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Interview Scorer", layout="centered")
st.title("Welcome to Multimodal Interview Scorer")
st.subheader("Please select any one option:")

option = st.radio("Select Mode:", ["Review Old Interview", "Review New Interview"])

if option == "Review Old Interview":
    st.subheader("🔑 Enter Interview ID:")
    session_id = st.text_input("Interview ID")

    if st.button("Submit ID"):
        if session_id.strip() == "":
            st.warning("Please enter a valid ID.")
        else:
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            SAMPLE_DATA_DIR = os.path.join(BASE_DIR, "sample_data")
            path = os.path.join(SAMPLE_DATA_DIR, session_id)

            if os.path.isdir(path):
                st.success("✅ ID found!")
                st.session_state["session_id"] = session_id
            else:
                st.error("❌ ID not found!")

if option == "Review New Interview":
    st.subheader("📤 Upload Interview")
    video_file = st.file_uploader("Upload interview video (.mp4)", type=["mp4"])
    reference_question = st.text_input("Reference Question (Optional)")

    session_id = None
    if video_file and st.button("Upload"):
        files = {"video": video_file}
        data = {"reference": reference_question}
        with st.spinner("Uploading video..."):
            res = requests.post(f"{API_URL}/upload", files=files, data=data)
        if res.status_code == 200:

            session_id = res.json()["Session_ID"]
            st.success("Upload successful")
            st.subheader(f"Your Interview ID: {session_id}")
            st.write("You can use this ID to directly analyze your uploaded interview.")
            st.session_state["session_id"] = session_id
        else:
            st.error("Upload failed")
        
# Analysis options
if "session_id" in st.session_state:
    session_id = st.session_state.get("session_id")
    st.subheader("🔍 Choose Analysis Type")
    col1, col2, col3, col4 = st.columns(4)
    if col1.button("Full Analysis"):
        with st.spinner("Running full analysis..."):
            res = requests.get(f"{API_URL}/analyze/full", params={"session_id": session_id})
        if res.status_code == 200:
            data=res.json()

            audio = data.get("audio_analysis", {})
            emotion = data.get("facial_analysis", {})
            text = data.get("text_analysis", {})
            final = data.get("final_score", {})

            st.subheader("📊 Audio Metrics")  #Audio Metrics
            st.write("Transcript:", audio.get("transcript", "N/A"))
            st.write("Word Count:", audio.get("word_count", "N/A"))
            st.write("Filler Words:", audio.get("filler_words"))
            st.write("Filler Ratio:", audio.get("filler_ratio", "N/A"),"%")
            st.write("WPM (Words Per Minute):", audio.get("wpm", "N/A"))
            st.write("Clarity Score:", audio.get("clarity_score", "N/A"),"%")
            st.write("Pitch Variation:", audio.get("pitch_variation", "N/A"),"%")
            st.write("Pause Count:", audio.get("pause_count", "N/A"))
            st.write("Average Energy:", audio.get("average_energy", "N/A"))
            if "energy_series" in audio:
                energy_series = audio.get("energy_series")
                st.subheader("Energy Over Time")
                fig, ax = plt.subplots()
                ax.plot(energy_series, color='steelblue')
                ax.set_xlabel("Frame Index")
                ax.set_ylabel("Energy")
                ax.set_title("Energy Variation Throughout Audio")
                st.pyplot(fig)

            st.subheader("📊 Emotion Metrics")  #Emotion Metrics
            st.write("Emotion Counts:")
            emotion_counts = emotion.get("emotion_counts", {})
            if emotion_counts:
                for emo, count in emotion_counts.items():
                    st.write(f"- {emo.capitalize()}: {count}")
            else:
                st.write("No emotions detected.")
            st.write("Dominant Emotion:",str(emotion.get("dominant_emotion", "N/A")).capitalize())
            st.write("Total Frame Analyzed:",emotion.get("total_frames_analyzed", "N/A"))
            st.write("Confidence Score:",emotion.get("confidence_score", "N/A"),"%")

            st.subheader("📊 Text Metrics")  #Text Metrics
            st.write("Word Count:", text.get("word_count", "N/A"))
            st.write("Vocabulary Richness:", text.get("vocab_richness", "N/A"),"%")
            st.write("Coherence Score:", data.get("coherence_score"), "%" if isinstance(data.get("coherence_score"), float) else "")

            st.subheader("🎯 Final Score")  #Final Score
            st.write("Overall Score:", final.get("score", "N/A"),"%")
        else:
            st.error("Analysis failed. Try again.")

    if col2.button("Audio Analysis"):
        with st.spinner("Running audio analysis..."):
            res = requests.get(f"{API_URL}/analyze/audio", params={"session_id": session_id})
        if res.status_code == 200:
            data = res.json()
            st.subheader("📊 Audio Metrics")
            st.write("Transcript:", data.get("transcript", "N/A"))
            st.write("Word Count:", data.get("word_count", "N/A"))
            st.write("Filler Words:",data.get("filler_words", "N/A"))
            st.write("Filler Ratio:", data.get("filler_ratio", "N/A"),"%")
            st.write("WPM (Words Per Minute):", data.get("wpm", "N/A"))
            st.write("Clarity Score:", data.get("clarity_score", "N/A"),"%")
            st.write("Pitch Variation:", data.get("pitch_variation", "N/A"),"%")
            st.write("Pause Count:", data.get("pause_count", "N/A"))
            st.write("Average Energy:", data.get("average_energy", "N/A"))
            if "energy_series" in data:
                energy_series = data.get("energy_series")
                st.subheader("Energy Over Time")
                fig, ax = plt.subplots()
                ax.plot(energy_series, color='steelblue')
                ax.set_xlabel("Frame Index")
                ax.set_ylabel("Energy")
                ax.set_title("Energy Variation Throughout Audio")
                st.pyplot(fig)

        else:
            st.error("Analysis failed. Try again.")

    if col3.button("Emotion Analysis"):
        with st.spinner("Running emotion analysis..."):
            res = requests.get(f"{API_URL}/analyze/emotion", params={"session_id": session_id})
        if res.status_code==200:
            data=res.json()
            st.subheader("📊 Emotion Metrics")
            st.write("Emotion Counts:")
            emotion_counts = data.get("emotion_counts", {})
            if emotion_counts:
                for emotion, count in emotion_counts.items():
                    st.write(str(emotion).capitalize(),":", count)
            else:
                st.write("No emotions detected.")
            st.write("Dominant Emotion:",str(data.get("dominant_emotion", "N/A")).capitalize())
            st.write("Total Frame Analyzed:",data.get("total_frames_analyzed", "N/A"))
            st.write("Confidence Score:",data.get("confidence_score", "N/A"),"%")
        else:
            st.error("Analysis failed. Try again.")
            
    if col4.button("Text Analysis"):
        with st.spinner("Running text analysis..."):
            res = requests.get(f"{API_URL}/analyze/text", params={"session_id": session_id})
        if res.status_code==200:
            data=res.json()
            st.subheader("📊 Text Metrics")
            st.write("word Count:", data.get("word_count", "N/A"))
            st.write("Vocabulary Richness:", data.get("vocab_richness", "N/A"),"%")
            st.write("Coherence Score:", data.get("coherence_score"), "%" if isinstance(data.get("coherence_score"), float) else "")

        else:
            st.error("Analysis failed. Try again.")