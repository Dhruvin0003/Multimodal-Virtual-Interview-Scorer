import librosa
from transformers import TFWav2Vec2ForCTC, Wav2Vec2Processor
import tensorflow as tf
import numpy as np

processor = Wav2Vec2Processor.from_pretrained("models/wav2vec2")
model = TFWav2Vec2ForCTC.from_pretrained("models/wav2vec2")

def analyze_audio(audio_path):
    transcript = transcribe_audio(audio_path)
    word_stats = analyze_transcript(transcript)
    wpm = estimate_wpm(audio_path, word_stats["word_count"])

    y, sr = librosa.load(audio_path, sr=16000)

    pitch_std = pitch_variation(y, sr)
    pause_count = detect_pauses(y, sr)
    avg_energy, energy_series = energy_score(y)

    clarity_score = 100
    penalties = 0

    if wpm > 160 or wpm < 90:
        penalties += 20
    if word_stats["filler_ratio"] > 0.05:
        penalties += 10
    if pitch_std < 5:
        penalties += 10
    if pause_count > 3:
        penalties += 10
    if avg_energy < 0.01:
        penalties += 10

    clarity_score = max(0, clarity_score - penalties)

    return {
        "transcript": transcript,
        "word_count": int(word_stats["word_count"]),
        "filler_words": int(word_stats["filler_words"]),
        "filler_ratio": float(word_stats["filler_ratio"]),
        "wpm": float(wpm),
        "clarity_score": float(clarity_score),
        "pitch_variation": round(float(pitch_std),2) if pitch_std is not None else None,
        "pause_count": int(pause_count),
        "average_energy": float(avg_energy),
        "energy_series": [float(e) for e in energy_series]
    }

def transcribe_audio(audio_path):
    audio, sr = librosa.load(audio_path, sr=16000)
    input_values = processor(audio, sampling_rate=16000, return_tensors="tf").input_values
    logits = model(input_values).logits
    predicted_ids = tf.argmax(logits, axis=-1)
    transcription = processor.batch_decode(predicted_ids)[0]
    return transcription.lower()

def analyze_transcript(transcript):
    words = transcript.split()
    total_words = len(words)
    filler_words = sum(1 for w in words if w in ["uh", "um", "like", "you know", "i mean", "so"])

    return {
        "word_count": total_words,
        "filler_words": filler_words,
        "filler_ratio": round((filler_words / total_words)*100,2) if total_words else 0
    }

def estimate_wpm(audio_path, word_count):
    audio, sr = librosa.load(audio_path, sr=16000)
    duration = librosa.get_duration(y=audio, sr=sr)
    wpm = (word_count / duration) * 60 if duration else 0
    return round(wpm, 2)

def pitch_variation(audio, sr):
    pitches, magnitudes = librosa.piptrack(y=audio, sr=sr)
    pitch_values = []

    max_mag = np.max(magnitudes) if np.max(magnitudes) > 0 else 1e-6

    for t in range(pitches.shape[1]):
        index = magnitudes[:, t].argmax()
        pitch = pitches[index, t]
        magnitude = magnitudes[index, t]

        if (magnitude > max_mag * 0.1 and 75 <= pitch <= 300 and not np.isnan(pitch) and pitch > 0):
            pitch_values.append(pitch)

    if not pitch_values:
        return None

    variation = np.std(pitch_values)
    return round(variation, 2) if not np.isnan(variation) else None

def detect_pauses(audio, sr, min_pause_duration=0.37):
    intervals = librosa.effects.split(audio, top_db=48)
    total_pauses = 0
    for i in range(1, len(intervals)):
        gap = (intervals[i][0] - intervals[i-1][1]) / sr
        if gap >= min_pause_duration:
            total_pauses += 1
    return total_pauses

def energy_score(audio):
    rms = librosa.feature.rms(y=audio)[0]
    avg_eng = float(np.mean(rms))
    return round(avg_eng,2),rms.tolist()