#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 10:55:13 2018

@author: himanshu
"""

import os 
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from other_formats_to_text import pdf2txt, docx2txt
'''
 Extract text form files in .pdf and .docx format.
 
 Arguements:
     'data_dir_path' : path to folder having pdf and docx files,
     'result': a dictionary with file path as keys and text as values,
     'verbose' : print progress,
     'callback' : fuction to perform additional operations. Check create_training_data.py where
     it has been used to load data in tkinter gui (inside main()) .
'''
def read_docx_and_pdf(data_dir_path, result = None, verbose = False, callback = None):
    if result is None:
        result = dict()
    for f in os.listdir(data_dir_path):
        file_path = os.path.join(data_dir_path, f)
        if os.path.isfile(file_path):
            text = None
            if f.lower().endswith('.pdf'):
                if verbose == True:
                    print('Extracting text from pdf:',file_path)
                text = pdf2txt(file_path)
            elif f.lower().endswith('.docx'):
                if verbose == True:
                    print('Extracting text from docx:',file_path)
                text = docx2txt(file_path)
            if  text is not None and len(text)>0:
                if callback is not None:
                    callback(len(result), file_path, text)
                result[file_path] = text
        elif os.path.isdir(file_path):
             read_docx_and_pdf(file_path, result, verbose, callback)         
    return result        