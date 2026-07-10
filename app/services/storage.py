import os
import json
import uuid
from pathlib import Path
from datetime import datetime
from abc import ABC, abstractmethod

class StorageService(ABC):
    @abstractmethod
    def save_email(self, data: dict) -> dict: pass
    
    @abstractmethod
    def get_emails(self) -> list: pass
    
    @abstractmethod
    def get_email(self, email_id: str) -> dict: pass
    
    @abstractmethod
    def update_email(self, email_id: str, data: dict) -> bool: pass

class LocalStorageService(StorageService):
    def __init__(self, storage_path: str | None = None):
        if storage_path is None:
            project_root = Path(__file__).resolve().parents[2]
            storage_path = str(project_root / "storage")
        self.storage_path = storage_path
        os.makedirs(self.storage_path, exist_ok=True)

    def _get_filepath(self, email_id: str) -> str:
        return os.path.join(self.storage_path, f"mail_{email_id}.json")

    def save_email(self, data: dict) -> dict:
        email_id = data.get("id", str(uuid.uuid4()))
        email = {
            "id": email_id,
            "sender": data.get("sender", "me@demo.com"),
            "recipient": data.get("recipient", ""),
            "subject": data.get("subject", "(No Subject)"),
            "body": data.get("body", ""),
            "timestamp": data.get("timestamp", datetime.now().isoformat()),
            "labels": data.get("labels", []),
            "folder": data.get("folder", "inbox"), # inbox, sent, drafts, trash, spam
            "read": data.get("read", False),
            "starred": data.get("starred", False),
            "important": data.get("important", False),
            "archived": data.get("archived", False),
            "deleted": data.get("deleted", False),
            "spam": data.get("spam", False)
        }
        with open(self._get_filepath(email_id), 'w') as f:
            json.dump(email, f)
        return email

    def get_emails(self) -> list:
        emails = []
        for filename in os.listdir(self.storage_path):
            if filename.startswith("mail_") and filename.endswith(".json"):
                try:
                    with open(os.path.join(self.storage_path, filename), 'r') as f:
                        email = json.load(f)
                        emails.append(email)
                except Exception:
                    pass
        emails.sort(key=lambda x: x["timestamp"], reverse=True)
        return emails

    def get_email(self, email_id: str) -> dict:
        filepath = self._get_filepath(email_id)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return None

    def update_email(self, email_id: str, data: dict) -> bool:
        email = self.get_email(email_id)
        if email:
            email.update(data)
            with open(self._get_filepath(email_id), 'w') as f:
                json.dump(email, f)
            return True
        return False

storage_service = LocalStorageService()
