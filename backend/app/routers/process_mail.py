from fastapi import APIRouter
from pydantic import BaseModel
from backend.logger import get_logger
from app.services.nlp_service import analyze_mail_intent
from app.services.llm import generate_custom_reply

logger = get_logger()
router = APIRouter()

class ProcessMailRequest(BaseModel):
    subject: str
    body: str
    sender_name: str | None = None
    sender_email: str | None = None

@router.post("/process-mail")
async def process_mail(request: ProcessMailRequest):
    logger.info(f"Processing mail from: {request.sender_email or 'Unknown Sender'}")

    intent = analyze_mail_intent(request.subject + " " + request.body)
    logger.info(f"Detected intent: {intent}")

    reply = generate_custom_reply(request.subject, request.body, request.sender_name, request.sender_email)

    return {
        "intent": intent,
        "reply": reply
    }
