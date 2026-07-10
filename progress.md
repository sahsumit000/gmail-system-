# Voice Controlled Email Assistant - Progress Log

## Milestones
- [x] Project Setup (FastAPI + Jinja2)
- [x] Backend Services Implementation (LocalStorageService)
- [x] Voice Intent Engine Refactoring
- [x] Speech Processing (Whisper + Edge-TTS) integration
- [x] FastAPI Endpoints & Jinja Templates
- [x] User Interface (Modern Gmail Clone)
- [x] Hands-free Voice Activity Detection (VAD) & Text-to-Speech (TTS) Feedback
- [x] Flexible Triggers & Requirements File
- [x] Interactive Voice Compose State Machine
- [x] Testing & Documentation

## Completed Work
- Added `requirements.txt` via `uv pip freeze`.
- Implemented Voice Activity Detection (VAD) in `static/js/app.js` using `AnalyserNode` to continuously listen and upload speech once silence is detected.
- Added Voice Feedback (TTS) logic using `localStorage` to bridge page redirects.
- Upgraded the `IntentParser` to flexibly handle inputs like "open mail", "opens emails", "show inbox", routing everything gracefully.
- Expanded folder intents to support "open start/star" (Starred), "open send" (Sent), "open trashcan/bin", and "compose compose".
- Implemented a fully interactive **Voice Composer State Machine** in `app.js` that talks to the user to fill out To, Subject, and Body fields with confirmation steps before sending.

## Current Work
- Documenting project functionality, voice control mechanics, and architecture in this progress file.

## Remaining Work
- None.

## Commands Executed
- `source .venv/bin/activate && uv pip freeze > requirements.txt`

## Design Decisions
- Allowed Voice Mode (Auto) as default for a hands-free smart assistant experience.
- Mapped vague terms like "email" or "mail" to the `inbox` folder so users aren't strictly bound to saying "inbox".

## Known Issues
- Requires microphone access.
- Requires `ffmpeg` installed on the host machine.

## Completion Percentage
100%

---

# Developer Reference

## How This Project Works
This system runs on a **FastAPI** backend serving **Jinja2 HTML templates**. 
1. **Frontend (Browser)**: Requests microphone permissions. `static/js/app.js` actively monitors the mic input volume. When you speak and pause for 1.5 seconds, it takes that audio chunk and POSTs it to the backend.
2. **Speech-to-Text**: The `/api/transcribe` endpoint takes the `.webm` audio chunk and processes it using the local `faster-whisper` AI model to convert it to text.
3. **Intent Parsing**: That text is routed through `app/intent/parser.py`, which uses Regex to deduce the command (e.g. "COMPOSE", "OPEN_FOLDER", "SEARCH").
4. **Action**: The backend returns this intent to the frontend, which handles the redirection (e.g., `window.location.href = '/compose'`).
5. **Text-to-Speech**: After navigating, the frontend asks the backend (`/api/speak`) to synthesize an audio response using `edge-tts` (e.g. "Opened inbox") and plays it.

## How to Add New Triggers
Triggers dictate how the AI understands text. To add new commands, edit `app/intent/parser.py`:

1. Open `app/intent/parser.py`.
2. Add a new `Intent` enum if it's a completely new action (e.g. `Intent.MARK_SPAM`).
3. Add a new Regex tuple to the `self.rules` array inside `IntentParser.__init__`.
   *Example:* `(r"(?i)mark.*spam", Intent.MARK_SPAM)`
4. If the intent requires entities (like extracting a folder name or search query), modify the `parse` method to extract `match.groups()` and insert them into the `entities` dictionary.
5. Finally, update `handleIntent()` inside `static/js/app.js` to execute frontend logic when that new intent is received.

## How to Control Voice Systems
The voice system consists of two parts:
1. **Frontend Control (VAD & Recording)**: You can adjust the silence sensitivity and delay in `static/js/app.js`. Look for `analyser.minDecibels = -70` to adjust mic sensitivity, or `average > 10` to adjust the volume threshold required to trigger "speech detected."
2. **Backend Engine (Whisper & TTS)**:
   - **Whisper (STT)**: Located in `app/speech/whisper_engine.py`. You can change the model size (e.g. `base`, `small`, `medium`) to trade speed for accuracy.
   - **Edge-TTS (TTS)**: Located in `app/speech/tts_engine.py`. You can change the voice string (e.g. `en-US-ChristopherNeural` or `en-GB-SoniaNeural`) to alter the accent and gender of the AI.

## Project Structure
```text
/home/crdy/testing/SE_lab/APP/
├── main.py                    # Main FastAPI server entrypoint
├── requirements.txt           # Python dependencies (pip install -r)
├── progress.md                # Development log and architecture guide (this file)
├── .venv/                     # Python virtual environment
├── docs/                      # General Documentation (API, Report, etc.)
├── storage/                   # Local database (JSON files for each email)
├── tests/                     # Unit testing scripts (run with pytest)
├── static/                    # Frontend assets
│   ├── css/style.css          # Gmail-like CSS
│   └── js/app.js              # Audio recording & Frontend routing logic
├── templates/                 # Jinja2 HTML templates (dashboard, folder, compose)
└── app/                       # Python Backend
    ├── api/                   # FastAPI routers (emails, speech, views)
    ├── intent/                # Natural Language Parser (Regex Intent logic)
    ├── services/              # Storage interface (Local JSON handler)
    └── speech/                # Audio processing wrappers (Whisper / Edge TTS)
```
