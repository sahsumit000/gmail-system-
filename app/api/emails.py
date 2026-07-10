from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.services.storage import storage_service

router = APIRouter()

@router.get("/")
def get_all_emails():
    return storage_service.get_emails()

@router.post("/")
def create_email(data: Dict[str, Any]):
    return storage_service.save_email(data)

@router.patch("/{email_id}")
def update_email(email_id: str, data: Dict[str, Any]):
    if storage_service.update_email(email_id, data):
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Email not found")

@router.delete("/{email_id}")
def delete_email(email_id: str):
    if storage_service.update_email(email_id, {"deleted": True, "folder": "trash"}):
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Email not found")
