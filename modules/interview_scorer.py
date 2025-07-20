def compute_final_score(audio, text, face, weights=(0.45, 0.35, 0.2)):
    # ----- AUDIO SCORING -----
    clarity = audio.get("clarity_score", 0)
    pitch = audio.get("pitch_variation", 0)
    wpm = audio.get("wpm", 0)
    pause_count = audio.get("pause_count", 0)
    avg_energy = audio.get("average_energy", 0)
    filler_ratio = audio.get("filler_ratio", 0)

    if pitch is not None and pitch > 0:
        pitch_score = max(0, 100 - ((pitch - 130) ** 2) / 25)
    else:
        pitch_score = 0

    wpm_score = max(0, 100 - ((wpm - 130) ** 2) / 16)
    pause_score = max(0, 100 - (pause_count * 10))
    energy_score = min(avg_energy / 0.02, 1.0) * 100

    filler_penalty = min(filler_ratio * 100, 10) if filler_ratio > 0.05 else 0

    audio_score = (
        0.4 * clarity +
        0.2 * pitch_score +
        0.2 * wpm_score +
        0.1 * pause_score +
        0.1 * energy_score -
        filler_penalty
    )
    audio_score = min(100, max(0, audio_score))

    # ----- TEXT SCORING -----
    coherence = text.get("coherence_score", None)
    word_count = text.get("word_count", 0)
    vocab_richness = text.get("vocab_richness", 0)

    wc_score = min(word_count / 20, 1.0) * 100
    vocab_score = vocab_richness * 100

    if isinstance(coherence, (int, float)):
        scaled_coherence = min(max((coherence - 0.4) / 0.55, 0), 1.0)
        text_score = (
        0.6 * scaled_coherence * 100 +
        0.2 * wc_score +
        0.2 * vocab_score
        )
    else:
        # Redistribute coherence weight equally
        text_score = (
        0.5 * wc_score +
        0.5 * vocab_score
        )
    text_score = min(100, text_score)

    # ----- EMOTION SCORING -----
    emotion_map = {
        "happy": 100,
        "neutral": 80,
        "surprise": 70,
        "sad": 60,
        "fear": 30,
        "angry": 30,
        "disgust": 20,
        "unknown": 50
    }

    emotion = face.get("dominant_emotion", "unknown")
    confidence_score = face.get("confidence_score", 50)
    frames_analyzed = face.get("total_frames_analyzed", 1)

    emotion_val = emotion_map.get(emotion, 50)
    if emotion == "neutral" and confidence_score >= 75:
        emotion_val += 10

    trust_factor = min(frames_analyzed / 10, 1.0)
    base_emotion_score = emotion_val * trust_factor

    emotion_score = 0.6 * base_emotion_score + 0.4 * confidence_score
    emotion_score = min(100, emotion_score)

    # ----- FINAL SCORING -----
    final_score = (
        weights[0] * audio_score +
        weights[1] * text_score +
        weights[2] * emotion_score
    )

    return {"score": float(round(final_score, 2))}
