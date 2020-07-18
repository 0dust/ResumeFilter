#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 16:04:23 2018

@author: himanshu
"""
import os
import sys
import pandas as pd
import tensorflow as tf
from classifier.lstm import BidirectionalLstm
from utils.model_essentials import essentials
from utils.load_training_data import load_final_data
from utils.parsing_rules import *
line_labels = {0: 'experience', 1: 'knowledge', 2: 'education', 3: 'project', 4: 'others'}
line_types = {0: 'header', 1: 'meta', 2: 'content'}

class ResumeParser():
    def __init__(self):
        self.email = None
        self.gender = None
        self.education = []
        self.experience = []
        self.project = []
        self.meta = []
        self.header = []
        self.skills = []
        self.line_label_classifier = BidirectionalLstm()
        self.line_type_classifier = BidirectionalLstm()
        
    def load_model(self, model_dir_path):
        self.line_label_classifier.load_model(model_dir_path=os.path.join(model_dir_path, 'label'))
        self.line_type_classifier.load_model(model_dir_path=os.path.join(model_dir_path, 'type'))
        
    def fit(self, training_data_dir_path, model_dir_path, batch_size = 128, epochs = 10,
            train_test_split_ratio= 0.3,random_state = 2018,dropout_rate = None,use_pretrained_embedd = False,embedding_size = None):
        
        line_label_fitted_model = self.fit_line_label_classifier(training_data_dir_path, model_dir_path, 
                                                             batch_size, epochs, train_test_split_ratio,random_state,
                                                             dropout_rate,use_pretrained_embedd, embedding_size)
        
        line_type_fitted_model = self.fit_line_type_classifier(training_data_dir_path, model_dir_path, batch_size, epochs,
                                                           train_test_split_ratio, random_state,
                                                           dropout_rate,use_pretrained_embedd, embedding_size)
        
        all_fitted_models = [line_label_fitted_model,line_type_fitted_model]
        
        return all_fitted_models
    
    def fit_line_label_classifier(self,training_data_dir_path, model_dir_path,batch_size,epochs,train_test_split_ratio,
                                  random_state,dropout_rate, use_pretrained_embedd,embedding_size):
        
        model_essentials_dict = essentials(training_data_dir_path,label_column_name = 'label')
        final_training_data = load_final_data(training_data_dir_path, label_column_name = 'label')
        print('###################### Training for line label ###########################')
        fitted_model = self.line_label_classifier.fit(model_dir_path+'/label', model_essentials_dict,
                                                      final_training_data,batch_size,epochs,
                                                      train_test_split_ratio, random_state ,dropout_rate,
                                                      use_pretrained_embedd,embedding_size)
        
        return fitted_model
        
    def fit_line_type_classifier(self,training_data_dir_path, model_dir_path, batch_size, epochs, train_test_split_ratio,
                                 random_state,dropout_rate, use_pretrained_embedd, embedding_size):
        
        model_essentials_dict = essentials(training_data_dir_path, label_column_name = 'type')
        final_training_data = load_final_data(training_data_dir_path, label_column_name  = 'type')
        print('################### Training for label type #############################')
        fitted_model = self.line_type_classifier.fit(model_dir_path+'/type', model_essentials_dict,
                                                     final_training_data,batch_size ,epochs,
                                                     train_test_split_ratio, random_state,dropout_rate,
                                                      use_pretrained_embedd,embedding_size)
        
        return fitted_model
        
        
    @staticmethod
    def get_education(line_label,line):
        if line_label == 'education':
            return line
        return None
    @staticmethod
    def get_experience(line_label,line):
        if line_label == 'experience':
            return line
        return None
    @staticmethod
    def get_project(line_label,line):
        if line_label == 'project':
            return line
        return None
    @staticmethod
    def get_skills(line_label,line):
        if line_label == 'skill':
            return line
        return None

    def parse(self,text):
        self.raw_text = text
        for line in text:
            tokens = tf.keras.preprocessing.text.text_to_word_sequence(line)
            line_label = self.line_label_classifier.predict_class(line)
            line_type =  self.line_type_classifier.predict_class(line)
#            print(line_label)
#            print(line_type)
            email = get_email(line)
            gender = get_gender(line)
            education = self.get_education(line_label,line)
            experience = self.get_experience(line_label,line)
            project = self.get_project(line_label,line)
            skill = self.get_skills(line_label,line)
            
            if email is not None:
                self.email = email
            if gender is not None:
                self.gender = gender
            if education is not None:
                self.education.append(education)
            if experience is not None:
                self.experience.append(experience)
            if project is not None:
                self.project.append(project)
            if skill is not None:
                self.skills.append(skill)
            
            if line_type == 'meta':
                self.meta.append(line)
            if line_type == 'header':
                self.header.append(line)
#            print('-----------------parsed------------------')
 
    def return_parsed_resume(self):
        result = dict()
        if self.email:
            result['email'] = self.name
        if self.gender:
            result['gender'] = self.gender
        if self.education:
            result['education'] = self.education
        if self.experience:
            result['experience'] = self.experience
        if self.project:
            result['project'] = self.project
        if self.skills:
            result['skills'] = self.skills
        if self.meta:
            result['meta'] = self.meta
        if self.header:
            result['header'] = self.header
        return result
