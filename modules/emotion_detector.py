import os
from deepface import DeepFace
from collections import Counter

def analyze_emotions(frame_folder):
    frame_skip = 2
    emotion_list = []

    frame_files = sorted([f for f in os.listdir(frame_folder) if f.endswith(".jpg")])

    for i, file in enumerate(frame_files):
        if i % frame_skip != 0:
            continue

        frame_path = os.path.join(frame_folder, file)

        try:
            result = DeepFace.analyze(
                img_path=frame_path,
                actions=["emotion"],
                enforce_detection=False
            )
            result = result[0]

            emotion = result['dominant_emotion']
            emotion_list.append(emotion)
            print(f"[✓] {file} → Emotion: {emotion}")

        except Exception as e:
            print(f"[x] {file} → Error: {e}")

    emotion_counts = dict(Counter(emotion_list))
    dominant_emotion = max(emotion_counts, key=emotion_counts.get) if emotion_counts else "unknown"
    total_frames = len(emotion_list)

    confident_emotions = ["neutral", "happy"]
    confident_count = sum(emotion_counts.get(e, 0) for e in confident_emotions)
    confidence_score = round((confident_count / total_frames) * 100, 2) if total_frames else 0

    return {
        "emotion_counts": {k: int(v) for k, v in emotion_counts.items()},
        "dominant_emotion": str(dominant_emotion),
        "total_frames_analyzed": int(total_frames),
        "confidence_score": float(confidence_score)
    }