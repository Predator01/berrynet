from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
 
Base = declarative_base()
 
class Words(Base):
    __tablename__ = 'Words'
    idWord = Column(Integer, primary_key=True)
    text = Column(String)

class SentenceLength(Base):
    __tablename__ = 'SentenceLength'
    idSenLength = Column(Integer, primary_key=True)
    length = Column(String)

class Two_Word(Base):
    __tablename__ = 'Two_Word'
    idTwoWord = Column(Integer, primary_key=True)
    TwoWord = Column(String)

class Periods(Base):
    __tablename__ = 'Periods'
    idPeriod = Column(Integer, primary_key=True)
    name = Column(String)

class Book(Base):
    __tablename__ = 'Book'
    idBook = Column(Integer, primary_key=True)
    name = Column(String)
    author = Column(String)
    idPeriod = Column(Integer, 
        ForeignKey('Periods.idPeriod') )
    TotalWords = Column(Integer)
    SentenceTotal = Column(Integer)

class WordCount(Base):
    __tablename__ = 'WordCount'
    id = Column(Integer, primary_key=True)
    idBook = Column(Integer, ForeignKey('Words.idWord') )
    idWord = Column(Integer, ForeignKey('Book.idBook') )    
    count = Column(Integer)

class SentenceLengthBook(Base):
    __tablename__ = 'SentenceLengthBook'
    id = Column(Integer, primary_key=True)
    idSenLength = Column(Integer, 
        ForeignKey('SentenceLength.idSenLength') )
    idbook = Column(Integer, ForeignKey('Book.idBook') )
    count = Column(Integer)

class TwoWordBook(Base):
    __tablename__ = 'TwoWordBook'
    id = Column(Integer, primary_key=True)
    idTwoWord = Column(Integer, 
        ForeignKey('Two_Word.idTwoWord') )
    idbook = Column(Integer, ForeignKey('Book.idBook') )
    count = Column(Integer)




