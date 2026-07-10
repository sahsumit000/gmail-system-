from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.services.storage import storage_service

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def filter_emails(folder: str, search: str = None):
    emails = storage_service.get_emails()
    if search:
        search = search.lower()
        emails = [e for e in emails if search in e.get('subject', '').lower() or search in e.get('body', '').lower()]
    
    for e in emails:
        e.setdefault('folder', 'inbox')
        e.setdefault('deleted', False)
        e.setdefault('archived', False)
        e.setdefault('spam', False)
        e.setdefault('starred', False)

    if folder == 'inbox':
        return [e for e in emails if e['folder'] == 'inbox' and not e['deleted'] and not e['archived']]
    elif folder == 'sent':
        return [e for e in emails if e['folder'] == 'sent' and not e['deleted']]
    elif folder == 'drafts':
        return [e for e in emails if e['folder'] == 'drafts' and not e['deleted']]
    elif folder == 'trash':
        return [e for e in emails if e['deleted']]
    elif folder == 'spam':
        return [e for e in emails if e['folder'] == 'spam' and not e['deleted']]
    elif folder == 'starred':
        return [e for e in emails if e['starred'] and not e['deleted']]
    elif folder == 'archived':
        return [e for e in emails if e['archived'] and not e['deleted']]
    return emails

@router.get("/")
@router.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="dashboard.html")

@router.get("/inbox")
async def inbox(request: Request, q: str = None):
    emails = filter_emails('inbox', q)
    return templates.TemplateResponse(request=request, name="folder.html", context={"emails": emails, "folder": "Inbox", "q": q})

@router.get("/sent")
async def sent(request: Request, q: str = None):
    emails = filter_emails('sent', q)
    return templates.TemplateResponse(request=request, name="folder.html", context={"emails": emails, "folder": "Sent", "q": q})

@router.get("/drafts")
async def drafts(request: Request, q: str = None):
    emails = filter_emails('drafts', q)
    return templates.TemplateResponse(request=request, name="folder.html", context={"emails": emails, "folder": "Drafts", "q": q})

@router.get("/trash")
async def trash(request: Request, q: str = None):
    emails = filter_emails('trash', q)
    return templates.TemplateResponse(request=request, name="folder.html", context={"emails": emails, "folder": "Trash", "q": q})

@router.get("/spam")
async def spam(request: Request, q: str = None):
    emails = filter_emails('spam', q)
    return templates.TemplateResponse(request=request, name="folder.html", context={"emails": emails, "folder": "Spam", "q": q})

@router.get("/starred")
async def starred(request: Request, q: str = None):
    emails = filter_emails('starred', q)
    return templates.TemplateResponse(request=request, name="folder.html", context={"emails": emails, "folder": "Starred", "q": q})

@router.get("/compose")
async def compose(request: Request):
    return templates.TemplateResponse(request=request, name="compose.html")

@router.get("/settings")
async def settings(request: Request):
    return templates.TemplateResponse(request=request, name="settings.html")

@router.get("/history")
async def history(request: Request):
    return templates.TemplateResponse(request=request, name="history.html")
