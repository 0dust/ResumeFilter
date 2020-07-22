#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 14:07:49 2018

@author: himanshu
"""

import urllib
import numpy as np
import os
import re
import zipfile

#NEEDS UPDATION.(done)

       
            
class GloveVector():
    def __init__(self,embedding_size):
        if embedding_size == None:
            embedding_size = 50
        self.embedding_size = embedding_size
#   
    @staticmethod
    def prepare_embedding(embedding_size, download ):
        if not os.path.exists(os.path.join(os.getcwd() + '/data') + '/glove.6B/glove.6B.' + str(embedding_size) + 'd.txt' ):
            print(os.path.join(os.getcwd() +'/data') + '/glove.6B/glove.6B.' + str(embedding_size) + 'd.txt' )
            print('Glove.6B.zip is being downloaded>>>>')
            data_dir_path = os.path.join(os.getcwd() + '../','data')
            glove_zip = os.path.join(data_dir_path , 'glove.6B.zip')
            urllib.request.urlretrieve(url='http://nlp.stanford.edu/data/glove.6B.zip', filename= 'data/glove.6B.zip')
            zipped = zipfile.ZipFile(glove_zip,mode = 'r')
            zipped.extractall()
            zipped.close()
        data_dir_path = os.path.join(os.getcwd() + '/data')
        glove_file_path =  data_dir_path + '/glove.6B/glove.6B.' + str(embedding_size) + 'd.txt'
        embedding_dict = {}
        with open(glove_file_path,'r') as file:
            for line in file:
                word = line.strip().split(' ')[0]
                embed = np.array(line.strip().split(' ')[1:], dtype = np.float32)
                embedding_dict[word] = embed
                
        return embedding_dict    
            
      
    def create_embedding_matrix(self,word2idx):
        embedding_matrix = np.zeros((len(word2idx)+1,self.embedding_size))
        embedding_dict = self.prepare_embedding(self.embedding_size,download = False)
        for word,i in word2idx.items():
            embedding_vector = embedding_dict.get(word)
            if embedding_vector is not None:
                embedding_matrix[i] = embedding_vector
        return embedding_matrix

        

