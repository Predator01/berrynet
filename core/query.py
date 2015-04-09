# -*- coding: utf-8 -*-

from db.manager import Manager
from extract import Extractor
from extract import download_book
from db.models import *

class Query(object):

    def __init__(self, text_dir, db_url, book_url):
        """
        init for querys
        """
        self.text_dir = text_dir
        self.db_url = db_url
        self.book_url = book_url
        self.manager = Manager(db_url)
        self.extractor = Extractor(db_url)
    
    def configure(self):
        filename = self.extractor.download_book(self.book_url, True)
        self.words = self.extractor.read_text(filename)
        
    def word_categories(self):
        """
        For every word in the database returns a dictionary of word->category
        according to the rates in the books.
        """
        categories = {}
        rates = {word: (float(count) / len(self.words)) 
            for word, count in self.words}
        words = self.manager.session.query(Word).all()
        low = self.manager.session.query(Category).filter(
            Category.description=='low').one()

        #sacando todas las palabras con category low
        for word in words:
            # sacar cada rate a qué categoría pertenece
            if word.text in rates:
                categories[word] = self.manager.session.query(WordCategory)\
                    .filter(WordCategory.min_rate < rates[word.text])\
                    .filter(WordCategory.max_rate >= rates[word.text])\
                    .one()
                word_categories = self.manager.session.query(
                    WordCategory).filter_by(word).all()
                for category in word_categories:
                    if rates[word.text] > category.min_rate and \
                    rates[word.text] < category.max_rate:
                        categories[word] = category
                        break
            else:
                # Obtener todas las palabras de la BD y asignar a low
                low_category = self.manager.session.query(
                    WordCategory).filter(word, low).one()
                ##id word - id cat
                categories[word] = low_category
        
        return categories
        
        #TODO No se estan eliminando las palabras que no aparecen o si?
        
    @staticmethod
    def conditional_probability(word, category, period):
        probability = self.manager.session.query(
            WordConditionalProbability).filter(
                word==word,
                period==eliz_period,
                category==category
                ).one()
        return probability
    
    def word_conditional_probabilities(self, word_cat):
        """
        get all the probabilities for every word in 
        """
        word_prob_periods = {}
        for word, category in words_cat.iteritems():
            elizabethan_probability = conditional_probability(
                word, category, elizabethan_period())
            romantic_probability = conditional_probability(
                word, category, romantic_period())
            word_prob_periods[word] = {
                'category': category,
                'elizabethan': elizabethan_probability,
                'romantic': romantic_probability}
        
        return word_prob_periods
    
    @staticmethod
    def period_book_count(period):
        return self.manager.session.query(
            Book).filter(period==period).count()
        
                
    def probabilities(self, conditional_probabilities):
        """
        Receives a dictionary such that
        {word: {'category': c, 'elizabethan': e, 'romantic': r}}.
        
        Returns dictionary such that
        {'elizabethan': elizabethan_rate, 'romantic': romantic_rate}
        """
        elizabethan_book_count = period_book_count(self.manager.elizabethan_period)
        romantic_book_count = period_book_count(self.manager.romantic_period)
        total_books = elizabethan_book_count + romantic_book_count
        elizabethan_probability = float(elizabethan_book_count) / total_books
        romantic_probability = float(romantic_book_count) / total_books
        elizabethan_factor = 1
        for word, c in conditional_probabilities:
            elizabethan_factor *= c['elizabethan'] * elizabethan_probability
        romantic_factor = 1
        for word, c in conditional_probabilities:
            romantic_probability *= c['romantic'] * romantic_probability
        
        return {'elizabethan': elizabethan_factor, 'romantic': romantic_factor}
    
    def run(self):
        words_category = self.word_categories()
        word_prob_periods = self.word_conditional_probabilities(words_category)
        result = self.probabilities(word_prob_periods)
        print result
    
    