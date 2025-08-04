from fastapi import APIRouter, Query
from typing import List

router = APIRouter()

# Simulation de liste d’e-mails analysés (plus tard connecté au script)
analyzed_mails = [
    {
        "account": "Orange",
        "sender": "example@example.com",
        "subject": "Test Mail",
        "body": "Ceci est un exemple d’email.",
        "intent": "À traiter"
    }
]

@router.get("/mails")
async def get_mails(limit: int = Query(5)):
    return analyzed_mails[-limit:]
