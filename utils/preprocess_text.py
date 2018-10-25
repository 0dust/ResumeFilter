#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 11:18:01 2018

@author: himanshu
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 10:01:53 2018

@author: himanshu
"""

import nltk
import os
import re
import inflect
import unicodedata
from nltk.tokenize import word_tokenize
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer


# SCRIPT NEEDS UPDATION, MAKE PREPROCESSING LESS VIGOROUS
class Preprocess():
    def __init__(self):
        self.text = None
#        self.text = text
        
    def process(self,text):
        self.tokens = self.tokenize(text)
        self.clean_tokens = self.remove_non_ascii(self.tokens)
#        self.new_tokens = self.remove_punctuation_and_more(self.clean_tokens)
    #        self.new_tokens_without_stopwords = self.remove_stopwords(self.new_tokens)
    #        self.new_tokens_ready = self.stem_and_lemmatize(self.new_tokens_without_stopwords)
        self.new_text = ' '.join(self.clean_tokens)
        
        return self.new_text
    
    def remove_non_ascii(self,words):
        new_words = []
        for word in words:
            new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
            new_words.append(new_word)
        return new_words   
    
    def tokenize(self,text):
        tokens = word_tokenize(text)
        tokens = [token.lower() for token in tokens]
        return tokens
    
    def remove_punctuation_and_more(self,tokens):
        p = inflect.engine()
        new_tokens = []
        for token in tokens:

            if token.replace('.','').isdigit():
                token = temp
                match = re.match(r'.*([1-2][0/9][0-9]{2})', token)
                if match is None:
                    new_token = p.number_to_words(token,group =2, decimal = 'point', threshold = 20000).replace(',','')
                    new_tokens.append(new_token)
                else:
                    new_tokens.append('year'+' '+token)
            else:
                new_token = re.sub(r'[^\w\s]', ' ', token)
                new_tokens.append(new_token)
        return new_tokens   
    
    def remove_stopwords(self,new_tokens):
        new_tokens_without_stopwords = [token for token in new_tokens if token not in stopwords.words('english')]
        return new_tokens_without_stopwords

    def stem_and_lemmatize(self,new_tokens_without_stopwords):
        tokens = new_tokens_without_stopwords
        stemmer = LancasterStemmer()
        new_tokens = [stemmer.stem(token) for token in tokens]
        lemmatizer = WordNetLemmatizer()
        new_words = [lemmatizer.lemmatize(token, pos = 'v') for token in new_tokens]
        
        return new_words

        