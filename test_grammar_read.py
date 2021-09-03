# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 12:51:32 2021

@author: donho
"""

import os


os.chdir('nlp_hw_grammer')

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

