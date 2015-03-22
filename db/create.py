from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from core.settings import BASE_DIR
import os

db_name = 'database_mining.sqlite'
db_prefix = 'sqlite:///'

def create_database():
	path_folder = os.path.join(BASE_DIR,db_name)
	path = db_prefix + path_folder
	engine = create_engine(path)	
	Base.metadata.create_all(engine)	

def create_session():
	Session = sessionmaker() 
	Session.configure(bind=engine)
	session = Session()
	return session
