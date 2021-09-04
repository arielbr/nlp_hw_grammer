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
    def __init__(self,terminal):
        self.isroot = False
        self.isterminal = False
        self.parent = None
        self.children = []

    def add_children(self,nodes):
        for i in nodes:
            self.children.append(i)
        
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
                    self.rules[elements[1]].append({elements[2]:int(elements[0])})
                else:
                    self.rules[elements[1]] = [{elements[2]: int(elements[0])}]
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
    #     self.fully_explored = {}
    #     self.parent = {}
    #     self.traverse_output = []

    #     # depth-first expantion
    #     root = "ROOT" # starting node
    #     if not self.traverse_output:
    #         # initialize nodes: not visited yet and no parent relation
    #         for node in self.rules.keys():
    #             self.parent[node] = None 
    #             self.fully_explored[node] = False
            
    #         # sample a root node
    #         self.traverse(node)
    #     else:
    #         # sample a non root node
    #         self.traverse(node)
            
    # # recursive function to help traversing 
    # def traverse(self, node):
    #     if  self.fully_explored[node] == False:
    #         for i in self.node_dict[node]:
    #             self.traverse_output.append(i)
    #             self.parent[i] = node
    #     self.traverse(node)
                
        raise NotImplementedError



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
