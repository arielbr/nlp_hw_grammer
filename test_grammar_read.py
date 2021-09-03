# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 12:51:32 2021

@author: donho
"""

import os
# import numpy as np
# 1mport pandas as pd


os.chdir(r"C:\Users\donho\Documents\JHU Classes\2021 Fall NLP\HW1\hw-grammar")

grammar_lines = []
with open("grammar.gr") as grammar:
    for line in grammar:
            line = line.partition("#")[0]
            line = line.rstrip()
            if line:
                grammar_lines.append(line.split('\t'))
                
                # data = line.split()
                # print(data)
    grammar.close()
print(grammar_lines)


print('\n')
print(grammar_lines)

print(pd.dataframe(grammar_lines))