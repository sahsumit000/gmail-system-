# Future Gmail API Integration Guide

This project is architected with an abstract `StorageService`. To integrate the real Gmail API without rewriting the entire frontend or routing logic, follow these steps:

## Step 1: Create `GmailStorageService`
Create a new file `app/services/gmail_storage.py` that implements the `StorageService` interface.

```python
from googleapiclient.discovery import build
from .storage import StorageService

class GmailStorageService(StorageService):
    def __init__(self, credentials):
        self.service = build('gmail', 'v1', credentials=credentials)

    def get_emails(self):
        # Call Google API: self.service.users().messages().list(userId='me').execute()
        # Map response to our internal dictionary schema (subject, body, folder)
        pass

    def save_email(self, data):
        # Call Google API to send or save draft
        pass
        
    def update_email(self, email_id, data):
        # Call Google API to modify labels/folders
        pass
```

## Step 2: Swap the implementation
In `app/api/emails.py` and `app/api/view_routes.py`, change the import:
```python
# Old:
# from app.services.storage import storage_service

# New:
from app.services.gmail_storage import GmailStorageService
storage_service = GmailStorageService(credentials)
```

Because the frontend and the FastAPI routes only care about the internal dictionary schema (`id`, `subject`, `body`, `folder`, `read`, etc.), the rest of the application will continue functioning as normal.
