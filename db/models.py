from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import FLOAT
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
 
Base = declarative_base()


"""
Intermediary
"""
class Word(Base):
    __tablename__ = 'words'
    id = Column(Integer, 
        primary_key=True)
    text = Column(String)

"""
Primary tables
"""

class SentenceLength(Base):
    __tablename__ = 'sentence_lengths'
    id = Column(Integer, primary_key=True)
    length = Column(String)

class TwoWord(Base):
    __tablename__ = 'two_words'
    id = Column(Integer, primary_key=True)
    two_word = Column(String)

class Period(Base):
    __tablename__ = 'periods'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    author = Column(String)
    id_period = Column(Integer, 
        ForeignKey('periods.id') )
    total_words = Column(Integer)
    sentence_total = Column(Integer)

class WordCount(Base):
    __tablename__ = 'words_counts'
    id = Column(Integer, primary_key=True)
    id_word = Column(Integer, ForeignKey('words.id') )
    id_book = Column(Integer, ForeignKey('books.id') )    
    count = Column(Integer)

class SentenceLengthBook(Base):
    __tablename__ = 'sentence_length_book'
    id = Column(Integer, primary_key=True)
    id_sen_length = Column(Integer, 
        ForeignKey('sentence_length.id') )
    id_book = Column(Integer, ForeignKey('books.id') )
    count = Column(Integer)

class TwoWordBook(Base):
    __tablename__ = 'two_word_book'
    id = Column(Integer, primary_key=True)
    id_two_word = Column(Integer, 
        ForeignKey('two_words.id') )
    id_book = Column(Integer, ForeignKey('books.id') )
    count = Column(Integer)

"""
Secondary tables
"""
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    description = Column(String)

class WordCategory(Base):
    __tablename__ = 'word_category'
    id_word = Column(Integer, 
        ForeignKey('words.id'),
        primary_key=True )
    id_category = Column(Integer,  
        ForeignKey('category.id'),
        primary_key=True )
    min_range = Column(FLOAT)
    max_range = Column(FLOAT)

class WordConditionalProbability(Base):
    __tablename__ = 'word_conditional_probability'
    id_word = Column(Integer, 
        ForeignKey('words.id'),
        primary_key=True )
    id_category = Column(Integer,  
        ForeignKey('category.id'),
        primary_key=True )
    period = Column(Integer,
        ForeignKey('periods.id'))
    probability = Column(FLOAT)
