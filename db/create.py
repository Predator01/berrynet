from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from core.settings import BASE_DIR
import os
from sqlalchemy.orm import scoped_session, sessionmaker
from contextlib import contextmanager

db_name = 'database_mining.sqlite'
db_prefix = 'sqlite:///'

def delete_database():
    if os.path.exists(path_folder):
        os.remove(path_folder)

def set_engine():
    path_folder = os.path.join(BASE_DIR,db_name)
    path = db_prefix + path_folder
    engine = create_engine(path)    
    return engine

def create_database():
    engine = set_engine()
    Base.metadata.create_all(engine)

def create_session():
    engine = set_engine()
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    session_obj = Session()
    return session_obj
