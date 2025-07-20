import os
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from ..services.media_handler import extract_media
from ..utils.id_generator import generate_session_id

router = APIRouter()

@router.post("")
async def upload_video(video: UploadFile = File(...), reference: str = Form(default="",description="Reference question (optional)")):
    session_id = generate_session_id(video.filename)
    save_dir = f"sample_data/{session_id}"
    os.makedirs(save_dir, exist_ok=True)

    video_path = os.path.join(save_dir, "video.mp4")
    with open(video_path, "wb") as f:
        f.write(video.file.read())

    extract_media(video_path, save_dir)

    if reference:
        with open(os.path.join(save_dir, "reference.txt"), "w") as f:
            f.write(reference)

    return JSONResponse({
        "Session_ID": session_id,
        "Message": "Upload successful. Proceed with analysis using this session ID."
    })