from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

db_name = 'database_mining.sqlite'
db_prefix = 'sqlite:///'
engine = create_engine('sqlite:///../database_mining.sqlite')


Base.metadata.create_all(engine)

def create_session():
	Session = sessionmaker() 
	Session.configure(bind=engine)
	session = Session()
	return session
