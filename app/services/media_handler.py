import os
from modules.extract_media import extract_audio, extract_frames

def extract_media(video_path, output_dir):
    audio_path = os.path.join(output_dir, "audio.wav")
    frame_folder = os.path.join(output_dir, "frames")
    extract_audio(video_path, audio_path)
    extract_frames(video_path, frame_folder)
