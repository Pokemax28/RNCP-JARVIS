import requests
from backend.scripts.logger import get_logger

logger = get_logger()

def extract_name_from_email(email: str) -> str:
    if email:
        local_part = email.split("@")[0]
        name_parts = local_part.replace(".", " ").replace("_", " ").split()
        name = " ".join([part.capitalize() for part in name_parts])
        return name
    return ""

def generate_custom_reply(subject: str, body: str, sender_name: str = None, sender_email: str = None) -> str:
    if not sender_name and sender_email:
        sender_name = extract_name_from_email(sender_email)

    prompt = f"""
    Tu es un assistant professionnel. Tu dois répondre à ce mail de manière polie, concise et naturelle.
    L'expéditeur s'appelle {sender_name if sender_name else "le client"}.

    Sujet : {subject}
    Message reçu : {body}

    Rédige une réponse professionnelle en incluant le prénom de l'expéditeur si possible.
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    logger.debug(f"Ollama API response: {response.json()}")
    return response.json()["response"].strip()
