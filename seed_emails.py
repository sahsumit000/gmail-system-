import os
import json
import uuid
from datetime import datetime, timedelta
import random

STORAGE_DIR = "storage"
if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

emails_data = {
    "inbox": [
        {"sender": "boss@company.com", "subject": "Project Update", "body": "Please provide an update on the SE lab project by tomorrow. This is critical for the upcoming presentation.", "starred": True},
        {"sender": "hr@company.com", "subject": "Holiday Schedule", "body": "Here is the holiday schedule for the upcoming year. Please review it carefully.", "starred": False},
        {"sender": "newsletter@techdaily.com", "subject": "Top 10 Tech Trends", "body": "Check out the latest trends in AI and software engineering.", "starred": False},
        {"sender": "noreply@github.com", "subject": "Action Required: Security Alert", "body": "We found a vulnerability in one of your dependencies. Please update immediately.", "starred": True},
        {"sender": "billing@aws.amazon.com", "subject": "Your Monthly Invoice", "body": "Your invoice for this month is attached. The total is $12.45.", "starred": False},
        {"sender": "mom@family.com", "subject": "Dinner this weekend?", "body": "Are you free for dinner this Sunday? Let me know!", "starred": True},
        {"sender": "marketing@store.com", "subject": "Flash Sale Weekend!", "body": "Save up to 50% on all items this weekend only.", "starred": False},
        {"sender": "support@bank.com", "subject": "Your account statement", "body": "Your monthly statement is ready to view online.", "starred": True},
        {"sender": "colleague@company.com", "subject": "Lunch?", "body": "Hey, do you want to grab lunch today?", "starred": False},
    ],
    "sent": [
        {"recipient": "boss@company.com", "subject": "Re: Project Update", "body": "I will have the report ready by 10 AM tomorrow.", "starred": True},
        {"recipient": "team@company.com", "subject": "Weekly Sync Notes", "body": "Here are the notes from our weekly sync. Good job everyone.", "starred": False},
        {"recipient": "support@software.com", "subject": "Bug Report", "body": "I found a bug when trying to compose an email.", "starred": False},
        {"recipient": "mom@family.com", "subject": "Re: Dinner this weekend?", "body": "Yes, Sunday works for me. See you then!", "starred": True},
        {"recipient": "landlord@apartments.com", "subject": "Maintenance Request", "body": "The sink is leaking again, please send someone to fix it.", "starred": False},
        {"recipient": "colleague@company.com", "subject": "Re: Lunch?", "body": "Sure, let's go at 12:30.", "starred": False},
    ],
    "drafts": [
        {"recipient": "client@business.com", "subject": "Proposal for Q3", "body": "Hello, attached is our proposal for Q3...", "starred": False},
        {"recipient": "friend@gmail.com", "subject": "Trip planning", "body": "Hey, are we still going on that trip next month?", "starred": False},
        {"recipient": "colleague@company.com", "subject": "Code Review", "body": "I took a look at your PR. I have a few comments.", "starred": False},
        {"recipient": "", "subject": "Ideas", "body": "1. Voice composer\n2. Real-time NLP\n3. Awesome UI", "starred": False},
        {"recipient": "professor@university.edu", "subject": "Question regarding Assignment", "body": "Dear Professor, I had a question about the latest assignment.", "starred": False},
        {"recipient": "support@internet.com", "subject": "Cancellation", "body": "I would like to cancel my subscription.", "starred": False},
    ],
    "spam": [
        {"sender": "winner@lottery.xyz", "subject": "YOU WON $1,000,000", "body": "Click here to claim your prize immediately!", "starred": False},
        {"sender": "prince@nigeria.com", "subject": "Urgent Business Transfer", "body": "I need your help transferring some funds.", "starred": False},
        {"sender": "sales@cheapmeds.ru", "subject": "Cheap Medications", "body": "Buy now at a 90% discount!", "starred": False},
        {"sender": "crypto@scam.io", "subject": "Double your Bitcoin", "body": "Send 1 BTC and get 2 BTC back!", "starred": False},
        {"sender": "hotdeals@buy-now.net", "subject": "LAST CHANCE: 99% OFF", "body": "Everything must go! Click here.", "starred": False},
        {"sender": "seo-expert@marketing.co", "subject": "Boost your traffic", "body": "We guarantee page 1 on Google within 24 hours.", "starred": False},
    ],
    "trash": [
        {"sender": "old-newsletter@junk.com", "subject": "Last month's news", "body": "Old news from last month.", "starred": False},
        {"sender": "noreply@social.com", "subject": "Someone liked your post", "body": "John liked your post from 3 years ago.", "starred": False},
        {"sender": "auto-alert@system.local", "subject": "Disk space warning", "body": "Your disk is 80% full.", "starred": False},
        {"recipient": "wrong-address@email.com", "subject": "Test", "body": "This was a test email.", "starred": False},
        {"sender": "food-delivery@app.com", "subject": "Your receipt", "body": "Here is your receipt for last week's pizza.", "starred": False},
        {"sender": "random@random.com", "subject": "Hello", "body": "Just saying hi.", "starred": False},
    ]
}

for folder, emails in emails_data.items():
    for data in emails:
        email_id = str(uuid.uuid4())
        
        email_schema = {
            "id": email_id,
            "sender": data.get("sender", "me@voice.local"),
            "recipient": data.get("recipient", "me@voice.local"),
            "subject": data.get("subject", "No Subject"),
            "body": data.get("body", ""),
            "timestamp": (datetime.now() - timedelta(days=random.randint(0, 14), hours=random.randint(0, 23))).isoformat(),
            "folder": folder,
            "read": random.choice([True, False]) if folder == "inbox" else True,
            "starred": data.get("starred", False),
            "important": data.get("starred", False), # Important flag tied to starred for demo
            "archived": False,
            "deleted": folder == "trash",
            "spam": folder == "spam"
        }
        
        with open(os.path.join(STORAGE_DIR, f"mail_{email_id}.json"), "w") as f:
            json.dump(email_schema, f, indent=4)

print("Seed data successfully populated.")
