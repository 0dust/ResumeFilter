#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 18:50:04 2018

@author: himanshu
"""

import re
from keras.preprocessing.text import text_to_word_sequence

def get_email(line):
    email = None
    match = re.search(r'[\w\.-]+@[\w\.-]+',line)
    if match is not None:
        email = match.group(0)
    return email

def get_gender(line):
    parts = text_to_word_sequence(line)
    gender = None
    if 'male' in parts:
        gender = 'male'
        return gender
    elif 'female' in parts:
        gender = 'female'
        return gender
    elif 'trans' in parts:
        gender = 'trans'
        return gender
    else:
        return 'Not Found.'
 