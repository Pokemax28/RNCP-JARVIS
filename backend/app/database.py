from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Adapte selon ta config MAMP
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/rncp_jarvis"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()