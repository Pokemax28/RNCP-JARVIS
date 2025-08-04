# RNCP-JARVIS : Email Processor & Dashboard

Projet RNCP de traitement intelligent des e-mails :

* Tri automatique des e-mails (Phishing, Spam, Transports, Stake, etc.) via NLP (facebook/bart-large-mnli)
* Génération de réponses personnalisées via un LLM local (Ollama/Mistral)
* Intégration IMAP/SMTP pour Gmail et Orange Mail
* Dashboard React complet pour la gestion et visualisation des e-mails triés

## Fonctionnalités (État actuel)

* Récupération des e-mails via IMAP (Orange Mail & Gmail)
* Classification des e-mails selon leur intention (Phishing, Spam, Transport, Finance, etc.)
* Déplacement automatique des e-mails dans des sous-dossiers après tri
* Génération de réponse automatique via endpoint `/process-mail`
* Dashboard React complet : affichage des e-mails, dossiers, tri, prévisualisation des réponses générées
* Authentification (Login/Register + Google OAuth)

## Architecture du projet

```
📂 RNCP-JARVIS/
├── 📂 backend/
│   ├── main.py                  # FastAPI app (API endpoints)
│   ├── classify.py              # Classification NLP (BART NLI)
│   ├── generate_response.py     # Génération de réponses (Ollama/Mistral)
│   ├── imap_client.py           # Connexion IMAP/SMTP
│   ├── utils.py                 # Fonctions utilitaires
│   ├── scripts/
│   │   ├── email_classifier.py  # Script de batch classification (manuel)
│   │   └── move_email.py        # Déplacement des e-mails
│   └── requirements.txt         # Dépendances Python
├── 📂 frontend/
│   ├── 📂 src/
│   │   ├── App.js               # Point d'entrée avec Auth Guard
│   │   ├── components/
│   │   │   ├── Header.js        # Header avec logo 'Jarvis'
│   │   │   ├── Sidebar.js       # Dossiers IMAP (Inbox, Spam, À Traiter...)
│   │   │   ├── EmailList.js     # Liste des e-mails (filtrage/catégories)
│   │   │   ├── EmailViewer.js   # Affichage du mail sélectionné
│   │   │   └── ResponseModal.js # Génération & prévisualisation de réponse
│   │   ├── pages/
│   │   │   ├── Login.js         # Page de connexion
│   │   │   ├── Register.js      # Page d’inscription
│   │   │   └── Dashboard.js     # Page principale (après login)
│   │   ├── api.js               # API calls vers le backend
│   │   └── auth.js              # Gestion Auth Token + Redirects
│   └── package.json             # Dépendances React
├── README.md
└── .env                         # Variables d'environnement (IMAP, SMTP, API KEYS)
```

## Installation

In terminal after Downloads olloma 
ollama pull mistral

```bash
# Clone du projet
git clone https://github.com/ton-username/RNCP-JARVIS.git
cd RNCP-JARVIS/backend

# Backend Python
python -m venv .venv
source .venv/Scripts/activate  # (Windows)
# ou
source .venv/bin/activate      # (Linux/Mac)
pip install -r requirements.txt

# Frontend React
cd ../frontend
npm install
```

## Lancement du projet

```bash
# Backend (FastAPI)
cd backend
uvicorn main:app --reload

# Frontend (React)
cd ../frontend
npm start
```

## Endpoints FastAPI

| Méthode | URL           | Description                                         |
| ------- | ------------- | --------------------------------------------------- |
| POST    | /process-mail | Prend un e-mail brut et retourne la réponse générée |
| GET     | /fetch-mails  | Récupère la liste des e-mails triés par catégorie   |

## Fonctionnalités du Dashboard

* Authentification sécurisée (Token, Google OAuth)
* Sidebar : Liste des dossiers IMAP (Inbox, Spam, À Traiter, Phishing, etc.)
* Email List : Liste des e-mails avec filtres (par catégories, date, etc.)
* Email Viewer : Visualisation du contenu complet de l’e-mail sélectionné
* Response Modal : Génération automatique d’une réponse personnalisée (modifiable avant envoi)
* Bouton "Répondre" : Déplace l’e-mail dans le dossier "Répondu" après validation

## Variables d'environnement (.env)

```
IMAP_HOST=imap.orange.fr
IMAP_USER=ton.email@orange.fr
IMAP_PASS=ton_mot_de_passe
SMTP_HOST=smtp.orange.fr
SMTP_PORT=465
OLLAMA_API=http://localhost:11434/api/generate
```

## Stack Technique

* **Python 3.10+ (FastAPI, HuggingFace Transformers, IMAPLib, SMTP, etc.)**
* **Ollama (Mistral 7B)**
* **React (Frontend avec Tailwind CSS, Shadcn/UI)**
* **IMAP/SMTP (Orange & Gmail OAuth2)**

## Roadmap (Prochaines étapes)

* [x] IMAP/SMTP Orange
* [x] Tri automatique des e-mails via NLP
* [x] Déplacement des e-mails dans les sous-dossiers
* [x] Génération de réponse automatisée
* [x] Dashboard React (complet)
* [x] Intégration Gmail OAuth2 (IMAP/SMTP)
* [ ] Ajout d’une base de connaissances locale pour enrichir les réponses
* [ ] Notifications / Rappels d’e-mails non traités

## Auteur

Maxime Cornu - B3 DDIA Alternant
---


