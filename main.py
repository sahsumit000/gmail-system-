import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api import emails, speech, view_routes

app = FastAPI(title="Voice Controlled Mail System")

# Ensure directories exist
os.makedirs("storage", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(emails.router, prefix="/api/emails", tags=["API Emails"])
app.include_router(speech.router, prefix="/api", tags=["API Speech"])
app.include_router(view_routes.router, tags=["Views"])
