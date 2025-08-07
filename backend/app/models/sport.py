from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from app.database import Base

class SportSession(Base):
    __tablename__ = "sport_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    title = Column(String)
    date = Column(DateTime)
    duration = Column(Integer)
    details = Column(String)
    muscle_group = Column(String)
    intensity = Column(String)
    was_done = Column(Boolean, default=False)
    feedback = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
