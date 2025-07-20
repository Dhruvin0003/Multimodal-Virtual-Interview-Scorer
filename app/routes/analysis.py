from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from ..services.analysis_runner import run_audio_analysis, run_emotion_analysis, run_text_analysis, run_full_analysis

router = APIRouter()

@router.get("/audio")
def audio(session_id: str = Query(...)):
    return JSONResponse(run_audio_analysis(session_id))

@router.get("/emotion")
def emotion(session_id: str = Query(...)):
    return JSONResponse(run_emotion_analysis(session_id))

@router.get("/text")
def text(session_id: str = Query(...)):
    return JSONResponse(run_text_analysis(session_id))

@router.get("/full")
def full(session_id: str = Query(...)):
    return JSONResponse(run_full_analysis(session_id))