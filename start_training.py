#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 00:24:26 2018

@author: himanshu
"""

import numpy as np
import sys
import os


def main():
    sys.path.append(os.path.dirname(__file__))

    from dl_parser import ResumeParser

    random_state = 430
    np.random.seed(random_state)

    current_dir = os.path.dirname(__file__)
    current_dir = current_dir if current_dir is not '' else '.'
    output_dir_path = current_dir + '/models'
    training_data_dir_path = current_dir + '/data/training_data'

    classifier = ResumeParser()
    batch_size = 64
    epochs = 100
    history = classifier.fit(training_data_dir_path=training_data_dir_path,
                             model_dir_path=output_dir_path,
                             batch_size=batch_size,
                             epochs=epochs,
                             train_test_split_ratio=0.3,
                             random_state=random_state,
                             dropout_rate = None,
                             use_pretrained_embedd = True,
                             embedding_size = 50)


if __name__ == '__main__':
    main()
