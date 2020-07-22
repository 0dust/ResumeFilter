#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 01:22:01 2018

@author: himanshu
"""


import sys
import os


def main():
    sys.path.append(os.path.dirname(__file__))

    from dl_parser import ResumeParser
    from utils.read_input import read_docx_and_pdf

    current_dir = os.path.dirname(__file__)
    current_dir = current_dir if current_dir is not '' else '.'
    data_dir_path = current_dir + '/data/resume_to_parse' # directory to scan for any pdf and docx files

    def parse_resume(index,file_path, file_content):
        print('parsing file: ', file_path)

        parser = ResumeParser()
        parser.load_model(current_dir + '/models')
        parser.parse(file_content)
#        print(parser.raw_text)  # print out the raw contents extracted from pdf or docx files

        parsed_info = parser.return_parsed_resume()
        for heading,info in parsed_info.items():
            print(heading,'\n')
            if(type(info) == type(list())):
                for i,s in enumerate(info):
                    print(i+1,'.',s,'\n')
            else:
                print('1.',info,'\n')
                
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++')

    collected = read_docx_and_pdf(data_dir_path, verbose =False, callback=lambda index, file_path, file_content: {
        parse_resume(index,file_path, file_content)
    })

    print('count: ', len(collected))
   


if __name__ == '__main__':
    main()