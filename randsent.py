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
        self.sum_dict = {} # added
        self._load_rules_from_file(grammar_file)

    def _load_rules_from_file(self, grammar_file):
        """
        Read grammar file and store its rules in self.rules

        Args:
            grammar_file (str): Path to the raw grammar file 
        """
        with open(grammar_file) as grammar_file:
            for line in grammar_file:
                line = line.partition("#")[0]
                line = line.strip()
                if not line or line[0] == "#":
                    continue
                elements = line.split("\t")
                if elements[1] in self.sum_dict.keys():
                    self.sum_dict[elements[1]] += int(elements[0])
                else:
                    self.sum_dict[elements[1]] = int(elements[0])
                
                # adding dash around non-terminals for quicker split later
                words = elements[2].split(" ")
                for i in range(len(words)):
                    if not words[i].islower():
                        words[i] = "-" + words[i] + "-"
                elements[2] = " ".join(words)
                if elements[1] in self.rules:
                    self.rules[elements[1]].append(tuple([elements[2], elements[0]]))
                else:
                    self.rules[elements[1]] = [tuple([elements[2], elements[0]])]
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
        root_word = "ROOT"
        choice_option = [element[0] for element in self.rules[root_word]]
        
        # Note: random.choice can't use weights. Unsure if weights have to add to 1 If they don,'t, we don't need t keep track of self.sumd_dict
        sentence = random.choices(choice_option,
                       weights=[int(element[1]) for element in self.rules[root_word]],
                       k=1)[0]
        
        # print(choice_option)
        print(sentence)
        num_iterations = 1
        while num_iterations < self.max_expansions:
            sentence.split()
            
            if word.startswith('/') and word.endswith('/')
            
            
            
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
