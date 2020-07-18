#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 12:38:46 2018

@author: himanshu
"""

import os
import pandas as pd
import nltk
import collections
import tensorflow as tf

line_labels = {0: 'experience', 1: 'knowledge', 2: 'education', 3: 'project', 4: 'others'}
line_labels_rev = {v:k for k,v in line_labels.items()}

line_types = {0: 'header', 1: 'meta', 2: 'content'}
line_types_rev = {v:k for k,v in line_types.items()}


def essentials(data_dir_path, max_vocab_size = None, label_column_name = None):
    if label_column_name is None:
        label_column_name = 'type'
    if max_vocab_size is None:
        max_vocab_size = 10000
    labels = dict()
    vocab = []
    text_max_len = 0
    labels = dict()
    for file in os.listdir(data_dir_path):
        data_file_path = os.path.join(data_dir_path,file)
        if os.path.isfile(data_file_path) and file.lower().endswith('.csv'):
            file_data = pd.read_csv(data_file_path)
            
            for index,line in file_data.iterrows():
                text = line['text']
                line_type = line['type']
                line_label = line['label']                
                tokens = tf.keras.preprocessing.text.text_to_word_sequence(text,lower = True)
                text_max_len = max(text_max_len,len(tokens))
                vocab.extend(tokens)
    tokens_wth_freq = collections.Counter(vocab)
    word2idx =  collections.defaultdict(int)
    
    for idx,word in enumerate(tokens_wth_freq.most_common(max_vocab_size)):
        word2idx[word[0]] = idx
    idx2word = {idx:word for word,idx in word2idx.items()}
    
    vocab_size = len(word2idx) + 1
    
    model_essentials_dict = dict()
    if label_column_name == 'type':
        model_essentials_dict['labels'] = line_types
    elif label_column_name == 'label':
        model_essentials_dict['labels'] = line_labels
    model_essentials_dict['word2idx'] = word2idx
    model_essentials_dict['idx2word'] = idx2word
    model_essentials_dict['vocab_size'] = vocab_size
    model_essentials_dict['text_max_len'] = text_max_len


    return model_essentials_dict
            
                