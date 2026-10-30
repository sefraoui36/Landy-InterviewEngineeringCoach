from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# On stocke la base dans le dossier data/ (déjà ignoré par Git)
DATABASE_URL = "sqlite:///../data/landy.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class DBSession(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, default="local_user")  # Prévu pour ta règle V3
    created_at = Column(DateTime, default=datetime.utcnow)

    # On stocke les données complexes en JSON pour l'instant
    plan_json = Column(JSON)
    history_json = Column(JSON)
    current_index = Column(Integer, default=0)


def init_db():
    Base.metadata.create_all(bind=engine)