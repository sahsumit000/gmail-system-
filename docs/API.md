# API Documentation

## View Routes
- `GET /`, `GET /dashboard`: Returns the dashboard template.
- `GET /inbox`: Returns the Inbox template (uses `folder.html`).
- `GET /sent`: Returns the Sent template.
- `GET /drafts`: Returns the Drafts template.
- `GET /trash`: Returns the Trash template.
- `GET /spam`: Returns the Spam template.
- `GET /starred`: Returns the Starred template.
- `GET /compose`: Returns the Compose email template.
- `GET /settings`: Returns the Settings template.
- `GET /history`: Returns the History template.

## Data Routes
- `GET /api/emails/`: Returns a JSON array of all emails.
- `POST /api/emails/`: Creates a new email in local storage.
- `PATCH /api/emails/{id}`: Updates an email (e.g. marking as read, moving to folder).
- `DELETE /api/emails/{id}`: Soft deletes an email (moves it to trash).

## Speech Routes
- `POST /api/transcribe`: Accepts a WebM audio file and returns the transcribed text and calculated intent.
- `POST /api/speak`: Accepts a JSON body with `{"text": "something"}` and returns an MP3 audio file of the synthesized speech.
