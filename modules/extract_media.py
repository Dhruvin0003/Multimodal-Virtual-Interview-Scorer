import os
import cv2
from moviepy import VideoFileClip

def extract_audio(video_path, output_audio_path):
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(output_audio_path, codec='pcm_s16le')

def extract_frames(video_path, output_folder, fps=1):
    os.makedirs(output_folder, exist_ok=True)
    cap = cv2.VideoCapture(video_path)

    video_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(video_fps // fps)

    count = 0
    saved = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if count % frame_interval == 0:
            frame_path = os.path.join(output_folder, f"frame_{saved}.jpg")
            cv2.imwrite(frame_path, frame)
            saved += 1
        count += 1

    cap.release()