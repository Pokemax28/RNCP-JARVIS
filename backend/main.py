from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from imapclient import IMAPClient
from dotenv import load_dotenv
from routes import sport
app.include_router(sport.router)
load_dotenv()

ACCOUNT = 'ORANGE'  # Change to 'GMAIL' if needed
EMAIL_ADDRESS = os.getenv(f"{ACCOUNT}_EMAIL")
EMAIL_PASSWORD = os.getenv(f"{ACCOUNT}_PASSWORD")
IMAP_SERVER = os.getenv(f"{ACCOUNT}_IMAP")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

if not all([EMAIL_ADDRESS, EMAIL_PASSWORD, IMAP_SERVER, GOOGLE_CLIENT_ID]):
    raise ValueError("Required environment variables are not set.")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users = []

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str

class GoogleAuthRequest(BaseModel):
    id_token: str

@app.get("/")
def root():
    return {"message": "Backend is working"}

@app.post("/register")
def register(data: RegisterRequest):
    for user in users:
        if user["username"] == data.username:
            raise HTTPException(status_code=400, detail="Username already exists")
    users.append({"username": data.username, "password": data.password})
    return {"message": "User registered successfully"}

@app.post("/login")
def login(data: LoginRequest):
    for user in users:
        if user["username"] == data.username and user["password"] == data.password:
            return {"token": "session-token-for-" + data.username}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/auth/google")
def auth_google(data: GoogleAuthRequest):
    response = requests.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={data.id_token}")
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid Google token")
    token_info = response.json()
    if token_info.get("aud") != GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=401, detail="Token audience mismatch")
    return {"token": "session-token-for-" + token_info.get("email")}

@app.get("/emails")
def get_emails():
    try:
        with IMAPClient(IMAP_SERVER) as client:
            client.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            folders = client.list_folders()
            print("Folders found:", [folder[2].decode() for folder in folders])

            email_data = {}

            for flags, delimiter, folder_name in folders:
                decoded_folder = folder_name.decode()
                print(f"Processing folder: {decoded_folder}")

                if decoded_folder.lower() in ["[gmail]/all mail", "[gmail]/trash"]:
                    continue

                client.select_folder(decoded_folder, readonly=True)
                messages = client.search(['ALL'])
                response = client.fetch(messages, ['ENVELOPE'])

                emails = []
                for msgid, data in response.items():
                    envelope = data[b'ENVELOPE']
                    emails.append({
                        "id": msgid,
                        "subject": envelope.subject.decode() if envelope.subject else "(No Subject)",
                        "from": envelope.from_[0].mailbox.decode() + "@" + envelope.from_[0].host.decode(),
                        "date": str(envelope.date)
                    })

                email_data[decoded_folder] = emails

            return email_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/email/{folder}/{msgid}")
def get_email_detail(folder: str, msgid: int):
    try:
        with IMAPClient(IMAP_SERVER) as client:
            client.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            client.select_folder(folder)
            response = client.fetch([msgid], ['RFC822'])
            raw_email = response[msgid][b'RFC822'].decode(errors='ignore')
            return {"id": msgid, "content": raw_email}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
