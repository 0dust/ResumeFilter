#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 11:18:01 2018

@author: himanshu
"""

'''

 Utility script to convert *.pdf and *.docx files  to *.txt format.
 
'''
import os
import sys
import docx
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from preprocess_text import Preprocess
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

#SCRIPT NEEDS UPDATION IF preprocess_text.py IS MODIFIED.

#######################
## .pdf to text
#######################
def pdf2txt(file_path):
    result = []
    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams = LAParams())
    interpreter = PDFPageInterpreter(manager, converter)
    
    with open(file_path, 'rb') as input_file:
        for page in PDFPage.get_pages(input_file):
            interpreter.process_page(page)
       
    converter.close()
    text  = output.getvalue()
    output.close()
    
    pre = Preprocess()
    for line in text.split('\n'):
        new_line = line.strip()
        if new_line != '':
            new_line = pre.process(new_line)
            result.append(new_line)
    return result        


#######################
## .docx to text    
#######################
def docx2txt(file_path):
    result = []
    document = docx.Document(file_path)
    pre = Preprocess()
    for para in document.paragraphs:
        text = para.text.strip()
        if text != '':
            text = pre.process(text)
            result.append(text)
    return result  



    
    