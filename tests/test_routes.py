import os
import sys
import pytest
from fastapi.testclient import TestClient
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from main import app

client = TestClient(app)

def test_dashboard_route():
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert b"Dashboard" in response.content

def test_inbox_route():
    response = client.get("/inbox")
    assert response.status_code == 200
    assert b"Inbox" in response.content

def test_api_emails():
    response = client.get("/api/emails/")
    assert response.status_code == 200
