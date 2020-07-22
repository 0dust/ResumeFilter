#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 16:07:22 2018

@author: himanshu
"""
import numpy as np
import tensorflow as tf
from nltk import word_tokenize
from sklearn.model_selection import train_test_split
from utils.glovemodel import GloveVector

class BidirectionalLstm():
    def __init__(self):
        self.essentials = None
        self.vocab_size = None
        self.max_len = None
        self.labels = None
        self.word2idx = None
        self.idx2word = None
        self.embedding_matrix = None
    @staticmethod
    def get_architect_file_path(model_dir_path):
        return model_dir_path + '/BidirectionalLstm_architecture.json'

    @staticmethod
    def get_weight_file_path(model_dir_path):
        return model_dir_path + '/BidirectionalLstm_weights.h5'

    @staticmethod
    def get_config_file_path(model_dir_path):
        return model_dir_path + '/BidirectionalLstm_config.npy'

    def load_model(self,model_dir_path):
        json = open(self.get_architect_file_path(model_dir_path), 'r').read()
        self.model = tf.keras.models.model_from_json(json)
        self.model.load_weights(self.get_weight_file_path(model_dir_path))
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        config_file_path = self.get_config_file_path(model_dir_path)

        self.essentials = np.load(config_file_path, allow_pickle = True).item()
        self.idx2word = self.essentials['idx2word']
        self.word2idx = self.essentials['word2idx']
        self.max_len = self.essentials['text_max_len']
        self.vocab_size = self.essentials['vocab_size']
        self.labels = self.essentials['labels']
        
    
    def create_model(self,use_pretrained_embedd,embedding_size):
        dropout_rate = 0.2
        print(embedding_size,self.max_len,self.vocab_size)
        self.model = tf.keras.models.Sequential()
        if use_pretrained_embedd:
            self.model.add(tf.keras.layers.Embedding(input_dim = self.vocab_size,output_dim = embedding_size,input_length = self.max_len,weights = [self.embedding_matrix],trainable = False))
        else:
            self.model.add(tf.keras.layers.Embedding(input_dim = self.vocab_size,output_dim = embedding_size,input_length = self.max_len))
        self.model.add(tf.keras.layers.Dropout(dropout_rate))
        self.model.add(tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(units = 64, dropout = 0.2, recurrent_dropout = 0.2, input_shape = (self.max_len,embedding_size))))
        self.model.add(tf.keras.layers.Dense(len(self.labels),activation = 'softmax'))
        
        self.model.compile(optimizer = 'rmsprop',loss = 'categorical_crossentropy',metrics = ['accuracy'])
  
    def pad_data(self,training_data):
        x = []
        y = []
        for text, label in training_data:
            tokens = tf.keras.preprocessing.text.text_to_word_sequence(text)
            
            word_idx_list = []
           
            for token in tokens:
                word_idx = 0
                if token in self.word2idx:
                    word_idx = self.word2idx[token]
                word_idx_list.append(word_idx)
            x.append(word_idx_list)
            y.append(label)
        X = tf.keras.preprocessing.sequence.pad_sequences(x, maxlen = self.max_len)
        Y  = tf.keras.utils.to_categorical(y,len(self.labels))
        return X,Y
    
            
    
    def fit(self,model_dir_path, model_essentials,training_data,batch_size,epochs,
            train_test_split_ratio , random_state ,dropout_rate ,use_pretrained_embedd ,embedding_size):
      
        self.essentials = model_essentials
        np.save(self.get_config_file_path(model_dir_path),self.essentials) 
        self.idx2word = self.essentials['idx2word']
        self.word2idx = self.essentials['word2idx']
        self.max_len = self.essentials['text_max_len']
        self.vocab_size = self.essentials['vocab_size']
        self.labels = self.essentials['labels']
        X,Y = self.pad_data(training_data)
        print('ready to fit training data..')
        x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=train_test_split_ratio, random_state=random_state)
        print('shape of x_train,x_test,y_train,y_test>>',x_train.shape, x_test.shape, y_train.shape, y_test.shape)

        if(use_pretrained_embedd):
            print('loading embeddings...')
            glove = GloveVector(embedding_size)
            self.embedding_matrix = glove.create_embedding_matrix(self.word2idx)
            print('embedding size >>',embedding_size)
            
        
        self.create_model(use_pretrained_embedd,embedding_size)
        json_model = self.model.to_json()
        model_architect_file = self.get_architect_file_path(model_dir_path)
        with open(model_architect_file,'w') as file:
            file.write(json_model)
        
        model_weight_file = self.get_weight_file_path(model_dir_path)
        checkpoint = tf.keras.callbacks.ModelCheckpoint(model_weight_file)
        
        fitted_model = self.model.fit(x = x_train, y = y_train, batch_size = batch_size, epochs = epochs,
                                      validation_data = [x_test,y_test], callbacks = [checkpoint],verbose = 1)
        self.model.save_weights(model_weight_file)
        
        
        np.save(model_dir_path + '/BidirectionalLstm_history.npy', fitted_model.history)

        validation_score = self.model.evaluate(x=x_test, y=y_test, batch_size=batch_size, verbose=1)
        print('score: ', validation_score[0])
        print('accuracy: ', validation_score[1])

        return fitted_model
    
    def predict(self, sentence):
        x = []
        tokens = [w.lower() for w in word_tokenize(sentence)]
        word_idx = [self.word2idx[token] if token in self.word2idx else 0 for token in tokens]
        x.append(word_idx)
        X = tf.keras.preprocessing.sequence.pad_sequences(x, self.max_len)
        output = self.model.predict(X)
        return output[0]

    def predict_class(self, sentence):
        predicted = self.predict(sentence)
        return self.labels[np.argmax(predicted)]

    def test(self, sentence):
        print(self.predict(sentence))


def main():
    app = BidirectionalLstm()
    app.test('I Love Dogs.')


if __name__ == '__main__':
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>Inside lstm.py<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    main()
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>Exited lstm.py<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
       
