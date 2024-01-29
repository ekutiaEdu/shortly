from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.urls import Base

database_url = f"sqlite:///shortly.db"
engine = create_engine(database_url)

Base.metadata.create_all(bind=engine)

session_maker = sessionmaker(engine)
