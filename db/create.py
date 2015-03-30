import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

# TODO delete
from contextlib import contextmanager

from core.settings import BASE_DIR
from models import Base


def db_url(filename):
    url = "sqlite:///%s" % db_file_path(filename)
    return url


def db_file_path(filename):
    return os.path.join(BASE_DIR, filename)


def set_engine(filename):
    file_path = db_file_path(filename)
    url = db_url(filename)
    engine = create_engine(url)
    return engine


def create_database(filename):
    print "SESSION NAMEE     " + filename
    engine = set_engine(filename)
    Base.metadata.create_all(engine)


def delete_database(filename):
    if os.path.exists(filename):
        os.remove(filename)


def create_session(filename):
    print "SESSION NAMEE     " + filename
    engine = set_engine(filename)
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    session_obj = Session()
    return session_obj
