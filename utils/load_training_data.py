#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 11:02:52 2018

@author: himanshu
"""

import os
import pandas as pd

'''

Returns a list of tuples, each tuple containes text and corresponding label.

'''
def load_final_data(data_dir_path, label_column_name = None ):
    result = []
    if label_column_name is None:
        label_column_name = 'type'
    if not os.path.isdir(data_dir_path):
        print('data_dir_path is not valid')
    else:
        for file in os.listdir(data_dir_path):
            data_file_path = os.path.join(data_dir_path,file)
            if os.path.isfile(data_file_path) and file.lower().endswith('.csv'):
                data = pd.read_csv(data_file_path)
                for index,row in data.iterrows():
                    if label_column_name == 'type':
                        result.append((row['text'],row['type']))
                    elif label_column_name == 'label':
                        result.append((row['text'],row['label']))
                
        return result