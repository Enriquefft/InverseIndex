"""Module to parse an input query."""

from Parser.InverseIndex.InverseIndex import idx
from Parser.InverseIndex.tokenizer import normalize, is_relevant
from Parser.InverseIndex.optimizer import Optimize

from nltk import ChartParser, word_tokenize, corpus, CFG
from nltk.tree import Tree

from sympy import symbols

from typing import Union

from pprint import pformat

import logging

words = idx.keys()


def generate_WORD(words: list[str]) -> str:
    """Generate the production rule for the WORD non-terminal."""
    return " | ".join([f'"{word}"' for word in words])


grammar_str = f"""
    S ->  WORD | And | Or | Not
    And -> S "and" S | S "but" Not
    Or -> S "or" S
    Not -> "not" S
    WORD -> {generate_WORD(words)}
"""

# Define your grammar production rules
grammar = CFG.fromstring(grammar_str)

parser = ChartParser(grammar)


def tokenize(query: str) -> list[str]:
    """Tokenize a document as a list to mantain lexical order."""
    stop_words = corpus.stopwords.words("spanish")
    words: [str] = word_tokenize(query)
    words = [normalize(word) for word in words if is_relevant(word)]
    # Disable normalization for better position tagging
    words = [word for word in words if word not in stop_words]
    return words


def parse(query: str) -> list[str]:
    """Parse a query and returns the logical expression's output."""

    logging.info(f"Query: {query}")

    tokens = tokenize(query)

    logging.debug(f"Tokens: {tokens}")

    parse_tree = list(parser.parse(tokens))

    if not parse_tree:
        raise ValueError(
            "Input could not be parsed, is the searched word present in the documents?"
        )

    # Extract the structure of the parse tree
    tree = parse_tree[0]

    logging.info(f"Parse tree: {tree}")

    def create_expression(node: Union[str, Tree]):
        """Given a tree, returns the object (And, Or, etc..) constructed recursively from its nodes."""
        if node.label() != 'Not':  # Handle the 'but Not' case
            node = node[0]
        if isinstance(node, Tree):
            # If the node is a Tree, check its label to determine what kind of object to create.
            if node.label() == 'WORD':
                # Create a Sentence object for it.
                return symbols(node[0])
            elif node.label() == 'And':
                # Create an And object
                return create_expression(node[0]) & create_expression(node[2])
            elif node.label() == 'Or':
                # Creating an Not object
                return create_expression(node[0]) | create_expression(node[2])
            elif node.label() == 'Not':
                return ~create_expression(node[1])
        else:
            raise ValueError(f"Unexpected node type: {type(node)}")

    # Use the recursive function to create the expression
    expression = create_expression(tree)
    logging.debug(f"Expression: {expression}")

    return Optimize(expression)
