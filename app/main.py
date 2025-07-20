from fastapi import FastAPI
from .routes import upload, analysis

app = FastAPI(title="Multimodal Interview Scorer API")

app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(analysis.router, prefix="/analyze", tags=["Analysis"])

