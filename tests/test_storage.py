import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from app.services.storage import storage_service

def test_save_and_get_email():
    email = storage_service.save_email({
        "sender": "me@demo.com",
        "recipient": "test@demo.com",
        "subject": "Test Subject",
        "body": "Test Body"
    })
    
    assert email["id"] is not None
    assert email["subject"] == "Test Subject"
    assert email["deleted"] is False
    
    fetched = storage_service.get_email(email["id"])
    assert fetched is not None
    assert fetched["subject"] == "Test Subject"

def test_update_email():
    email = storage_service.save_email({
        "sender": "me@demo.com",
        "recipient": "test2@demo.com",
        "subject": "Update Me",
        "body": "Update Body"
    })
    
    success = storage_service.update_email(email["id"], {"deleted": True, "folder": "trash"})
    assert success is True
    
    fetched = storage_service.get_email(email["id"])
    assert fetched["deleted"] is True
    assert fetched["folder"] == "trash"
