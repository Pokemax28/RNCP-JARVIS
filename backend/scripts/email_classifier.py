import os
from imapclient import IMAPClient
import pyzmail
from transformers import pipeline
from dotenv import load_dotenv
import re

load_dotenv()

ACCOUNT = 'ORANGE'  # Change to 'GMAIL' if needed
EMAIL_ADDRESS = os.getenv(f"{ACCOUNT}_EMAIL")
EMAIL_PASSWORD = os.getenv(f"{ACCOUNT}_PASSWORD")
IMAP_SERVER = os.getenv(f"{ACCOUNT}_IMAP")

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

from transformers import pipeline

# Chargement du modèle BART-MNLI (à faire une seule fois)
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def is_whitelisted(email_domain):
    for pattern in WHITELIST_DOMAINS:
        if re.match(pattern, email_domain):
            return True
    return False

WHITELIST_DOMAINS = [
        # Télécoms / Services Internet
        r"orange\.fr", r"free\.fr", r"sfr\.fr", r"bouyguestelecom\.fr", r"orangebank\.fr",

        # Paiement / Banque / Fintech
        r"paypal\.fr", r"lydia-app\.(com|fr|io|net|org)", r"revolut\.com", r"boursorama\.info",
        r"n26\.com", r"fortuneo\.fr", r"ing\.fr", r"hellobank\.fr", r"banquepopulaire\.fr",
        r"cic\.fr", r"labanquepostale\.fr", r"bpce\.fr", r"credit-agricole\.fr",
        r"younited-credit\.(com|fr)",r"@info.sumeria\.(eu|com|fr|io|net|org)", r"@mail.sumeria\.(eu|com|fr|io|net|org)",

        # E-mails / Messagerie
        r"outlook\.com", r"hotmail\.com", r"yahoo\.com", r"icloud\.com", r"gmail\.com",
        r"laposte\.net", r"orange\.fr", r"sfr\.fr", r"free\.fr",

        # E-commerce / Ventes / Marketplaces
        r"amazon\.fr", r"leboncoin\.fr", r"vinted\.fr", r"rakuten\.fr",
        r"fnac\.com", r"darty\.com", r"cdiscount\.com", r"shein\.com", r"zalando\.fr",

        # Santé / Médical
        r"doctolib\.fr", r"maiia\.com", r"keldoc\.com", r"ameli\.fr",

        # Mobilité / Transports
        r"velib-metropole\.fr", r"tier\.app", r"uber\.com", r"sncf-connect\.com",
        r"oui\.sncf", r"blablacar\.fr",

        # Livraison / Poste
        r"chronopost\.fr", r"laposte\.fr", r"colissimo\.fr",

        # Voyages / Locations
        r"airbnb\.fr", r"booking\.com", r"expedia\.fr",

        # Administratif / Gouvernement
        r"moncompteformation\.gouv\.fr", r"impots\.gouv\.fr", r"urssaf\.fr", r"banque-france\.fr",

        # Réseaux Sociaux / Plateformes
        r"linkedin\.com", r"twitter\.com", r"x\.com", r"facebook\.com", r"instagram\.com",
        r"discord\.com", r"twitch\.tv", r"youtube\.com",

        # Cloud / Collaboration
        r"icloud\.com", r"gmail\.com", r"outlook\.com", r"microsoft\.com", r"teams\.microsoft\.com",
        r"zoom\.us",

        # Musique / Streaming
        r"spotify\.com", r"deezer\.com",

        # Gaming / Plateformes Jeux
        r"epicgames\.com", r"steamcommunity\.com", r"store\.steampowered\.com",
        r"playstation\.com", r"xbox\.com", r"nintendo\.com",

        # Courses / Drive / Hypermarchés
        r"carrefour\.fr", r"leclercdrive\.fr", r"intermarche\.com", r"monoprix\.fr",
        r"drive\.intermarche\.com", r"auchandrive\.fr",

        # CPRISM All Variants
        r"cprism\.(com|fr|io|net|org)", r"mail\.cprism\.com", r"info\.cprism\.com", r"support\.cprism\.com",

        # SUMMERIA All Variants
        r"summeria\.(fr|com|io|net|org|app)", r"app\.summeria\.fr", r"mail\.summeria\.com",
        r"info\.summeria\.io", r"support\.summeria\.net",

        # Divers / Autres
        r"stake\.com", r"shotgun\.live", r"mail\.stake\.com", r"info\.stake\.com",
        r"support\.stake\.com", r"stripe\.com", r"info\.lydia\.me"
    ]

WHITELIST_EMAILS = [
    "cprism@cprism.com"
]

def classify_email(subject, body, sender_email):
    domain = sender_email.split("@")[-1]

    # 1. Hard Rule : Whitelist
    if any(re.match(pattern, domain) for pattern in WHITELIST_DOMAINS) or sender_email in WHITELIST_EMAILS:
        print(f"Mail whitelisted (domain : {domain})")
        return "À traiter", 1.0

    # 2. Zero-Shot Classification (3 catégories)
    candidate_labels = ["Phishing", "Spam", "À traiter", "À vérifier manuellement"]
    text = f"Voici un email reçu :\nSujet : {subject}\nMessage : {body}"

    result = classifier(text, candidate_labels)
    predicted_label = result['labels'][0]
    confidence_score = result['scores'][0]
    

    # Règle stricte : si confiance < 0.50 → Spam
    if confidence_score < 0.50:
        predicted_label = "Spam"
    elif confidence_score < 0.60:
        predicted_label = "À vérifier manuellement"

    return predicted_label, confidence_score





def ensure_folder_exists(client, folder_name):
    folders = [f[2] for f in client.list_folders()]  # f[2] contient le nom du dossier IMAP
    if folder_name not in folders:
        client.create_folder(folder_name)
        print(f"Dossier '{folder_name}' créé.")

def move_email(client, uid, destination_folder):
    destination_folder_full = f"INBOX/{destination_folder}"
    ensure_folder_exists(client, destination_folder_full)
    client.move([uid], destination_folder_full)
    print(f"Mail déplacé vers '{destination_folder_full}'")


def process_emails(limit=10000):
    with IMAPClient(IMAP_SERVER) as client:
        client.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        client.select_folder('INBOX', readonly=False)

        messages = client.search(['UNSEEN'])
        print(f"Found {len(messages)} unread emails in {ACCOUNT}")

        for uid in messages[:limit]:
            raw_message = client.fetch([uid], ['BODY[]', 'FLAGS'])[uid][b'BODY[]']
            message = pyzmail.PyzMessage.factory(raw_message)

            subject = message.get_subject()
            sender_email = message.get_addresses('from')[0][1]
            
            if message.text_part:
                charset = message.text_part.charset or 'utf-8'
                body = message.text_part.get_payload().decode(charset)
            elif message.html_part:
                charset = message.html_part.charset or 'utf-8'
                body = message.html_part.get_payload().decode(charset)
            else:
                body = ""

            label, score = classify_email(subject, body, sender_email)

            print(f"\nMail de {sender_email} - Sujet: {subject}")
            print(f"Classé comme : {label.upper()} (confiance {round(score * 100, 2)}%)")

            move_email(client, uid, label)

if __name__ == "__main__":
    process_emails(limit=10000)