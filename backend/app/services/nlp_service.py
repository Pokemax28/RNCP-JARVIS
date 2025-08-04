from transformers import pipeline
from backend.logger import get_logger

logger = get_logger()

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def analyze_mail_intent(text: str) -> str:
    candidate_labels = [
        "Email frauduleux (phishing)",
        "Publicité non désirée (spam)",
        "Email important à lire"
    ]
    prompt = f"Voici un email reçu : {text}. Classifie cet email parmi : Email frauduleux (phishing), Publicité non désirée (spam), Email important à lire."

    result = classifier(prompt, candidate_labels)
    predicted_label = result['labels'][0]
    confidence_score = result['scores'][0]

    if confidence_score < 0.60:
        predicted_label = "À vérifier manuellement"

    return predicted_label