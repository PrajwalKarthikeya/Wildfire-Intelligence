import os
from sqlalchemy import create_engine, Column, String, Float, DateTime, Integer, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import datetime

load_dotenv()

# We use SQLite for local development if no POSTGRES URL is provided.
# When ready for Supabase, just put the Supabase POSTGRES connection string in .env
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/wildfire.db")

# In SQLite, DateTime is stored as string/timestamp, which SQLAlchemy handles.
# If connecting to postgres, ensure the URL starts with 'postgresql://' not 'postgres://' (SQLAlchemy 1.4+)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class FireDetection(Base):
    __tablename__ = "fire_detections"

    id = Column(String, primary_key=True, index=True) # fire_id
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True)
    satellite = Column(String)
    brightness = Column(Float)
    frp = Column(Float)
    confidence = Column(Float)
    daynight = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class RiskPrediction(Base):
    __tablename__ = "risk_predictions"

    id = Column(String, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True)
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False) # LOW, MODERATE, HIGH, EXTREME
    model_version = Column(String, nullable=False)

class ModelRun(Base):
    __tablename__ = "model_runs"

    id = Column(String, primary_key=True, index=True)
    model_version = Column(String, nullable=False)
    trained_at = Column(DateTime, default=datetime.datetime.utcnow)
    metrics = Column(JSON)
    feature_list = Column(JSON)

def init_db():
    Base.metadata.create_all(bind=engine)
    print(f"Database initialized at {DATABASE_URL}")

if __name__ == "__main__":
    init_db()
