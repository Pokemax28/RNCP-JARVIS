from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.sport import SportSession
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/sessions", tags=["Sport Sessions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class SportSessionCreate(BaseModel):
    user_id: str
    title: str
    date: datetime
    duration: int
    details: str
    muscle_group: str
    intensity: str

@router.post("/add")
def add_session(session: SportSessionCreate, db: Session = Depends(get_db)):
    new_session = SportSession(**session.dict())
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

@router.get("/get/{user_id}")
def get_sessions(user_id: str, db: Session = Depends(get_db)):
    return db.query(SportSession).filter(SportSession.user_id == user_id).all()