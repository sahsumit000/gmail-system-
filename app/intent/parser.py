import re
from enum import Enum

class Intent(Enum):
    COMPOSE = "COMPOSE"
    OPEN_FOLDER = "OPEN_FOLDER"
    READ_LATEST = "READ_LATEST"
    READ_UNREAD = "READ_UNREAD"
    READ_NEXT = "READ_NEXT"
    READ_PREV = "READ_PREV"
    STOP_READING = "STOP_READING"
    SEARCH = "SEARCH"
    CLEAR_SEARCH = "CLEAR_SEARCH"
    DELETE = "DELETE"
    ARCHIVE = "ARCHIVE"
    RESTORE = "RESTORE"
    MARK_IMPORTANT = "MARK_IMPORTANT"
    MARK_READ = "MARK_READ"
    SAVE_DRAFT = "SAVE_DRAFT"
    SEND = "SEND"
    GO_SETTINGS = "GO_SETTINGS"
    UNKNOWN = "UNKNOWN"

class IntentParser:
    def __init__(self):
        self.rules = [
            (r"(?i)(?:compose|write)\s*(?:mail|email|compose)?", Intent.COMPOSE),
            (r"(?i)create.*draft", Intent.COMPOSE),
            (r"(?i)(?:open|opens|show)\s+(inbox|drafts|trash|trashcan|bin|spam|sent|send|starred|start|star|mail|mails|email|emails|history|settings)", Intent.OPEN_FOLDER),
            (r"(?i)read.*latest.*", Intent.READ_LATEST),
            (r"(?i)read.*unread.*", Intent.READ_UNREAD),
            (r"(?i)read.*next.*", Intent.READ_NEXT),
            (r"(?i)read.*prev.*", Intent.READ_PREV),
            (r"(?i)stop.*reading", Intent.STOP_READING),
            (r"(?i)clear\s+search", Intent.CLEAR_SEARCH),
            (r"(?i)search\s+(?:for\s+)?(.*)", Intent.SEARCH),
            (r"(?i)delete.*", Intent.DELETE),
            (r"(?i)archive.*", Intent.ARCHIVE),
            (r"(?i)restore.*", Intent.RESTORE),
            (r"(?i)mark.*important", Intent.MARK_IMPORTANT),
            (r"(?i)mark.*read", Intent.MARK_READ),
            (r"(?i)save.*draft", Intent.SAVE_DRAFT),
            (r"(?i)send.*email", Intent.SEND),
            (r"(?i)go.*settings", Intent.GO_SETTINGS),
        ]

    def parse(self, text: str) -> dict:
        text = text.strip()
        for pattern, intent in self.rules:
            match = re.search(pattern, text)
            if match:
                entities = {}
                if intent == Intent.OPEN_FOLDER and match.groups():
                    folder = match.group(1).lower()
                    if folder in ["mail", "mails", "email", "emails"]:
                        folder = "inbox"
                    elif folder in ["trashcan", "bin"]:
                        folder = "trash"
                    elif folder == "send":
                        folder = "sent"
                    elif folder in ["start", "star"]:
                        folder = "starred"
                    entities["folder"] = folder
                if intent == Intent.SEARCH and match.groups():
                    entities["query"] = match.group(1).strip()
                return {"intent": intent.value, "entities": entities}
        return {"intent": Intent.UNKNOWN.value, "entities": {}}

parser = IntentParser()
