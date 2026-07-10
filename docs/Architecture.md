# System Architecture

This application follows a Model-View-Controller (MVC) architecture, heavily relying on FastAPI for routing and Jinja2 for view rendering.

## 1. Presentation Layer
- **Templates**: `Jinja2` templates located in `templates/`. A base `layout.html` provides the sidebar, header, and player infrastructure. Content is injected into `{% block content %}`.
- **Static Assets**: Native CSS in `static/css/style.css` matching a Gmail-like aesthetic. Native JS in `static/js/app.js` handles audio recording and frontend logic.

## 2. API & Routing Layer
- **FastAPI**: Handles request parsing, query parameters, and JSON serialization.
- **Routers**: Divided into `emails.py`, `speech.py`, and `view_routes.py` for modularity.

## 3. Business Logic Layer
- **Intent Parser**: Uses Regular Expressions to determine the user's intent from the transcribed voice command.
- **Speech Engines**:
  - `faster-whisper`: Converts spoken audio (WebM) into raw text strings.
  - `edge-tts`: Converts raw text strings back into MP3 audio files for playback.

## 4. Data Access Layer
- **StorageService**: An abstract class specifying standard CRUD operations.
- **LocalStorageService**: A concrete implementation that stores each email as an individual JSON file inside the `storage/` directory.
