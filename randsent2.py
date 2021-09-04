#!/usr/bin/env python
"""
601.465/665 — Natural Language Processing
Assignment 1: Designing Context-Free Grammars

Assignment written by Jason Eisner
Modified by Kevin Duh
Re-modified by Alexandra DeLucia

Code template written by Alexandra DeLucia,
based on the submitted assignment with Keith Harrigian
and Carlos Aguirre Fall 2019
hello this is don
"""
import os
import sys
import random
import argparse
import pdb

# Want to know what command-line arguments a program allows?
# Commonly you can ask by passing it the --help option, like this:
#     python randsent.py --help
# This is possible for any program that processes its command-line
# arguments using the argparse module, as we do below.
# 
# NOTE: When you use the Python argparse module, parse_args() is the
# traditional name for the function that you create to analyze the
# command line.  Parsing the command line is different from parsing a
# natural-language sentence.  It's easier.  But in both cases,
# "parsing" a string means identifying the elements of the string and
# the roles they play.

def parse_args():
    """
    Parse command-line arguments.

    Returns:
        args (an argparse.Namespace): Stores command-line attributes
    """
    # Initialize parser
    parser = argparse.ArgumentParser(description="Generate random sentences from a PCFG")
    # Grammar file (required argument)
    parser.add_argument(
        "-g",
        "--grammar-file", 
        type=str, required=True, 
        help="Path to grammar file",
    )
    # Start symbol of the grammar
    parser.add_argument(
        "-s",
        "--start-symbol", 
        type=str,
        help="Start symbol of the grammar",
        default="ROOT",
    )
    # Number of sentences
    parser.add_argument(
        "-n",
        "--number-of-sentences",
        type=int,
        help="Number of sentences to generate",
        default=1,
    )
    # Maximum number of nonterminal expansions when generating the sentence
    parser.add_argument(
        "-M",
        "--max-expansions",
        type=int,
        help="Max number of nonterminal expansions when generating the sentence",
        default=450,
    )
    # Print the derivation tree for each generated sentence
    parser.add_argument(
        "-t",
        "--tree",
        action="store_true",
        help="Print the derivation tree for each generated sentence",
        default=False,
    )
    return parser.parse_args()

class Node(object):
    def __init__(self,name):
        self.name = name
        
        self.parent = None
        self.children = []
        self.explored = False
        if self.name == 'ROOT':
            self.isroot = True
            self.isterminal = False
        else:
            self.isroot = False
            self.isterminal = False
            

    def add_children(self,node):
            self.children.append(node)
        
class Grammar:
    def __init__(self, grammar_file):
        """
        Context-Free Grammar (CFG) Sentence Generator

        Args:
            grammar_file (str): Path to a .gr grammar file
        
        Returns:
            self
        """
        # Parse the input grammar file
        self.rules = {}
        self.nonterminals = set()
        self.sum_dict = {} # added
        self._load_rules_from_file(grammar_file)

    def _load_rules_from_file(self, grammar_file):
        """
        Read grammar file and store its rules in self.rules

        Args:
            grammar_file (str): Path to the raw grammar file 
        """
        # get all the terminal symbols out:
        left_hand_side = set()
        right_hand_side = set()
        with open(grammar_file) as grammar_file1:
            for line in grammar_file1:
                line = line.partition("#")[0]
                line = line.strip()
                if not line or line[0] == "#":
                    continue
                elements = line.split("\t")
                left_hand_side.add(elements[1])
                words = elements[2].split(" ")
                right_hand_side.union(set(words))
        for word in left_hand_side:
            if word not in right_hand_side:
                self.nonterminals.add(word)
        
        with open(grammar_file) as grammar_file2:
            for line in grammar_file2:
                line = line.partition("#")[0]
                line = line.strip()
                if not line or line[0] == "#":
                    continue
                #pdb.set_trace()
                elements = line.split("\t")
                 
                if elements[1] in self.sum_dict.keys():
                    # I think we should use counts here instead of adding probs
                    self.sum_dict[elements[1]] += int(elements[0])
                else:
                    self.sum_dict[elements[1]] = int(elements[0])
                
                # adding dash around non-terminals for quicker split later
                words = elements[2].split(" ")
                for i in range(len(words)):
                    if words[i] in self.nonterminals:
                        words[i] = "/" + words[i] + "/"        
                elements[2] = " ".join(words)
                if elements[1] in self.rules:
                    self.rules[elements[1]][elements[2]] = float(elements[0])
                else:
                    self.rules[elements[1]] = {elements[2]: float(elements[0])}
        print(self.sum_dict)
        print(self.rules)

    def sample(self, derivation_tree, max_expansions):
        """
        Sample a random sentence from this grammar

        Args:
            derivation_tree (bool): if true, the returned string will represent 
                the tree (using bracket notation) that records how the sentence 
                was derived
                               
            max_expansions (int): max number of nonterminal expansions we allow
        
        Returns:
            str: the random sentence or its derivation tree
        """
        self.traverse_output = ""

        # depth-first expantion
        self.root = Node("ROOT") # starting node
        self.root.explored = True
        self.traverse(self.root)
        print(self.traverse_output)   
    # recursive function to help traversing 
    def traverse(self, node):
        #pdb.set_trace()
        if node.name in self.nonterminals:
            self.traverse_output = self.traverse_output + "(" + node.name
            choice_options = []
            weights = []
            for elements in self.rules[node.name].keys():
                weights.append(self.rules[node.name][elements])
                choice_options.append(elements)
            sample = random.choices(choice_options, weights=weights, k=1)[0]
            #print('sample:', sample)
            print(self.traverse_output) 
            for child in sample.split(" "):
                child = Node(child)
                if child.name.strip('/') in self.nonterminals:
                    child.name = child.name.strip('/')
                    child.isterminal = False
                    node.add_children(child)
                    child.parent = node
                    self.traverse(child) 
                    
                else:
                    child.isterminal = True
                    node.add_children(child)
                    child.parent = node
                    self.traverse_output = self.traverse_output + " " +child.name + ")"
                
                
        else:
            self.traverse_output = self.traverse_output + " "+ child.name + ")"
         



####################
### Main Program
####################
def main():
    # Parse command-line options
    args = parse_args()

    # Initialize Grammar object
    grammar = Grammar(args.grammar_file)

    # Generate sentences
    for i in range(args.number_of_sentences):
        # Use Grammar object to generate sentence
        sentence = grammar.sample(
            derivation_tree=args.tree, max_expansions=args.max_expansions
        )

        # Print the sentence with the specified format.
        # If it's a tree, we'll pipe the output through the prettyprint script.
        if args.tree:
            t = os.system(f"echo '{sentence}' | ./prettyprint")
        else:
            print(sentence)


if __name__ == "__main__":
    main()
