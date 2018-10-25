#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 13:27:57 2018

@author: himanshu
"""

import os 
import sys
from tkinter import *
import tkinter.font as tkFont
import pandas as pd
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from read_input import read_docx_and_pdf 

line_labels = {0: 'experience', 1: 'knowledge', 2: 'education', 3: 'project', 4: 'others'}
line_labels_reverse = {v:k for k,v in line_labels.items()}
line_types = {0: 'header', 1: 'meta', 2: 'content'}
line_types_reverse = {v:k for k,v in line_types.items()}

class LabelResume(Frame):
    def __init__(self, master , lines_with_dummy_labels):
        Frame.__init__(self, master = master)
        
        self.CustomFont = tkFont.Font(family = 'Helvetica', size = 13)
        self.master.title('Label Resume Lines')
        self.master.rowconfigure(0,weight = 1)
        self.master.columnconfigure(0, weight = 1)
        self.grid(sticky = W + E + N + S)

        self.lineIndex_list = []
        self.lineContent_list = []
        self.type_button_list = []
        self.label_button_list = []
        
        for line_number, line in enumerate(lines_with_dummy_labels):
            self.build_line(lines_with_dummy_labels, line_number, line)
        
        self.rowconfigure(1, weight = 1)
        self.columnconfigure(1, weight = 1)
        
    def build_line(self, lines_with_dummy_labels, line_number, line):
        line_text = line[0]
     
        lineIndex = Label(self, width = 10, height = 1, text = str(line_number))
        lineIndex.grid(row = line_number, column = 0,sticky = W+E+N+S)
         
        lineContent = Text(self, width = 100, height = 1)
        lineContent.insert(INSERT, line_text)
        lineContent.grid(row = line_number, column = 1, sticky = W+E+N+S)
     
        def change_type_dropdown(*args):
            curr_type_value = tkvar_types.get()
            lines_with_dummy_labels[line_number][1] = line_types_reverse[curr_type_value]

            
        def change_label_dropdown(*args):
            curr_label_value = tkvar_labels.get()
            lines_with_dummy_labels[line_number][2] = line_labels_reverse[curr_label_value]
            
        tkvar_types = StringVar(self.master)
        type_choices = {'header','meta','content'}
        tkvar_types.set('None') # set the default option
        popupMenu = OptionMenu(self, tkvar_types, *type_choices)
        popupMenu.grid(row=line_number, column=2, sticky=W + E + N + S) 
        tkvar_types.trace('w', change_type_dropdown)
        
        tkvar_labels = StringVar(self.master)
        label_choices = {'experience','knowledge','education','project','others'}
        tkvar_labels.set('None') # set the default option
        popupMenu = OptionMenu(self, tkvar_labels, *label_choices)
        popupMenu.grid(row=line_number, column=3, sticky=W + E + N + S) 
        tkvar_labels.trace('w', change_label_dropdown)



def resume_gui(training_data_dir_path, index, file_path, file_content):
    lines_with_dummy_labels = [[line, -1, -1] for line in file_content]
    
    master = Tk()
    gui = LabelResume(master, lines_with_dummy_labels)
    
    def callback():
        master.destroy()
        output_file_path = os.path.join(training_data_dir_path, str(index)+'.csv')
        if os.path.exists(output_file_path):
            return
        data = pd.DataFrame.from_records(lines_with_dummy_labels,columns = ['text','type','label'])
        rows_to_drop = data.loc[((data['type']== -1) | (data['label'] == -1))].index
        data.drop(data.index[rows_to_drop],inplace = True,axis = 0)
        data.to_csv(output_file_path,index = False)


    master.protocol("WM_DELETE_WINDOW", callback)
    gui.mainloop()


def main():
    data_dir_path = os.path.abspath(__file__ + '/../../' + '/data')  # directory to scan for any pdf and docx files
    training_data_dir_path = data_dir_path + '/training_data'
    collected = read_docx_and_pdf(training_data_dir_path, verbose =True, callback=lambda index, file_path, file_content: {
        resume_gui(training_data_dir_path, index, file_path, file_content)
    })
    
    print('count: ', len(collected))


if __name__ == '__main__':
    main()
       