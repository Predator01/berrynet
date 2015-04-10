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
    __tablename__ = 'word'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    books = relationship(
        'Book',
        secondary='word_count'
    )

"""
Primary tables
"""

class SentenceLength(Base):
    __tablename__ = 'sentence_length'
    id = Column(Integer, primary_key=True)
    length = Column(String)

class TwoWord(Base):
    __tablename__ = 'two_word'
    id = Column(Integer, primary_key=True)
    two_word = Column(String)

class Period(Base):
    __tablename__ = 'period'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    author = Column(String)
    id_period = Column(Integer, 
        ForeignKey('period.id'))
    period = relationship(
        Period,
        backref=backref('books',uselist=True,cascade='delete,all'))
    words = relationship(Word,secondary='word_count')
    total_words = Column(Integer)
    sentence_total = Column(Integer)


"""
Link Word - Book
"""
class WordCount(Base):
    __tablename__ = 'word_count'
    id_word = Column(Integer, ForeignKey('word.id'), primary_key=True)
    id_book = Column(Integer, ForeignKey('book.id'), primary_key=True)    
    count = Column(Integer)
    rate = Column(FLOAT)
    book = relationship(Book, backref=backref("book_assoc"))
    word = relationship(Word, backref=backref("word_assoc"))

class SentenceLengthBook(Base):
    __tablename__ = 'sentence_length_book'
    id = Column(Integer, primary_key=True)
    id_sen_length = Column(Integer, 
        ForeignKey('sentence_length.id') )
    id_book = Column(Integer, ForeignKey('book.id') )
    count = Column(Integer)

class TwoWordBook(Base):
    __tablename__ = 'two_word_book'
    id = Column(Integer, primary_key=True)
    id_two_word = Column(Integer, 
        ForeignKey('two_word.id') )
    id_book = Column(Integer, ForeignKey('book.id') )
    count = Column(Integer)

"""
Secondary tables
"""
class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    description = Column(String)

class WordCategory(Base):
    __tablename__ = 'word_category'
    id_word = Column(Integer, 
        ForeignKey('word.id'),
        primary_key=True )
    id_category = Column(Integer,  
        ForeignKey('category.id'),
        primary_key=True )
    min_range = Column(FLOAT)
    max_range = Column(FLOAT)
    category = relationship(Category, backref=backref("category_assoc"))
    word = relationship(Word, backref=backref("word_category_assoc"))

class WordConditionalProbability(Base):
    __tablename__ = 'word_conditional_probability'
    id_word = Column(Integer, 
        ForeignKey('word.id'),
        primary_key=True )
    id_category = Column(Integer,  
        ForeignKey('category.id'),
        primary_key=True )
    id_period = Column(Integer,
        ForeignKey('period.id'),
        primary_key=True)
    probability = Column(FLOAT)
    category = relationship(Category, backref=backref("wcp_category_assoc"))
    word = relationship(Word, backref=backref("wcp_word_assoc"))
    period = relationship(Period, backref=backref("wcp_period_assoc"))

