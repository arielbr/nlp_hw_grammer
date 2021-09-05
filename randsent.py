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
"""
import os
import sys
import random
import argparse
import pdb
import re

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
        self.isterminal = False
        if self.name == 'ROOT':
            self.isroot = True
        else:
            self.isroot = False
            
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
        self.sum_dict = {}
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
                    self.sum_dict[elements[1]] += float(elements[0])
                else:
                    self.sum_dict[elements[1]] = float(elements[0])
                
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
        self.traverse(self.root, max_expansions)
        return self.traverse_output

    # recursive function to help traversing 
    def traverse(self, node, remaining_expansions):
        remaining_expansions -= 1
        if remaining_expansions <= 0:
            self.traverse_output = self.traverse_output + "..." + ") "
        else: 
            if len(self.traverse_output) > 0 and self.traverse_output[-1] == ")":
                self.traverse_output += " "
            self.traverse_output = self.traverse_output + "(" + node.name + " "
            # select one expansion rule by relative odds
            choice_options = []
            weights = []
            for elements in self.rules[node.name].keys():
                weights.append(self.rules[node.name][elements])
                choice_options.append(elements)
            sample = random.choices(choice_options, weights=weights, k=1)[0]

            splitted = sample.split("/")
            for i in range(len(splitted)):
                child = splitted[i]
                if child == "" or child == " ":
                    continue
                child = child.strip(" ")
                child_node = Node(child)
                if child in self.nonterminals:
                    child_node.isterminal = False
                    node.add_children(child_node)
                    child_node.parent = node
                    self.traverse(child_node, remaining_expansions) 
                else:
                    child_node.isterminal = True
                    node.add_children(child_node)
                    child_node.parent = node
                    if self.traverse_output[-1] == ")":
                        self.traverse_output += " "
                    if i == len(splitted) - 1:
                        self.traverse_output = self.traverse_output + child_node.name + ")"
                        return
                    else:
                        self.traverse_output = self.traverse_output + child_node.name + " "
            self.traverse_output += ")"


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
            prettyprint_path = os.path.join(os.getcwd(), 'prettyprint')
            t = os.system(f"echo '{sentence}' | perl {prettyprint_path}")
        else:
            print(sentence)


if __name__ == "__main__":
    main()
