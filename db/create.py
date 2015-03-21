from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

engine = create_engine('sqlite:///../database_mining.sqlite')

session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)

