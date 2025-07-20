import os
from modules.audio_analysis import analyze_audio
from modules.emotion_detector import analyze_emotions
from modules.text_scorer import analyze_text
from modules.interview_scorer import compute_final_score

def run_audio_analysis(session_id):
    audio_path = f"sample_data/{session_id}/audio.wav"
    return analyze_audio(audio_path)

def run_emotion_analysis(session_id):
    frame_dir = f"sample_data/{session_id}/frames"
    return analyze_emotions(frame_dir)

def run_text_analysis(session_id):
    audio_path = f"sample_data/{session_id}/audio.wav"
    transcript = analyze_audio(audio_path)["transcript"]
    reference_path = f"sample_data/{session_id}/reference.txt"
    reference = open(reference_path).read() if os.path.exists(reference_path) else None
    return analyze_text(transcript, reference)

def run_full_analysis(session_id):
    audio_path = f"sample_data/{session_id}/audio.wav"
    frame_dir = f"sample_data/{session_id}/frames"
    reference_path = f"sample_data/{session_id}/reference.txt"
    
    audio_result = analyze_audio(audio_path)
    face_result = analyze_emotions(frame_dir)
    reference = open(reference_path).read() if os.path.exists(reference_path) else None
    text_result = analyze_text(audio_result["transcript"], reference)
    final_score = compute_final_score(audio_result, text_result, face_result)

    return {
        "audio_analysis": audio_result,
        "facial_analysis": face_result,
        "text_analysis": text_result,
        "final_score": final_score
    }