# Installation Guide

## Prerequisites
- Python 3.12+
- `ffmpeg` installed on your system (required for speech processing).

## 1. Clone the repository
Navigate to the directory where you want to install the project.
```bash
cd /home/crdy/testing/SE_lab/APP/
```

## 2. Set up Virtual Environment
We recommend using `uv` for fast dependency resolution.
```bash
uv venv
source .venv/bin/activate
```

## 3. Install Dependencies
```bash
uv pip install fastapi uvicorn pydantic faster-whisper edge-tts pytest python-multipart httpx jinja2
```

## 4. Start the Server
```bash
uvicorn main:app --reload
```
You can now access the app at `http://127.0.0.1:8000`.
