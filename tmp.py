"""Logic module for the search engine."""
# from .InverseIndex import InverseIndex
from pathlib import Path
# from typing import Union

# from Config import DOCUMENT_FOLDER

from sympy.core.symbol import Symbol
from sympy.logic import simplify_logic

idx = {}  # Dict(DOCUMENT_FOLDER)


class Sentence(Symbol):
    """Represents a keyword search."""

    def __init__(self, arg: str):
        """Initialize a sentence with a keyword."""
        print("Constructing sentence with: ", arg)
        self.arg = arg

    def search(self) -> set[Path]:
        """Search the sentence for keyword instances."""
        return idx[self.arg]


class And(Sentence):
    """Represents an AND search."""

    def __init__(self, *args: Sentence):
        """Initialize an AND search with a list of keywords."""
        print("Constructing AND with: ", *args)
        self.args = args

    def search(self):
        """Search the sentence for keyword instances."""
        return set.intersection(*(arg.search() for arg in self.args))


class Or(Sentence):
    """Represents an OR search."""

    def __init__(self, *args: Sentence):
        """Initialize an OR search with a list of keywords."""
        print("Constructing OR with: ", *args)
        self.args = args

    def search(self):
        """Search the sentence for keyword instances."""
        return set.union(*(arg.search() for arg in self.args))


class Not(Sentence):
    """Represents a NOT search."""

    def __init__(self, arg: Sentence):
        """Initialize a NOT search with a keyword."""
        print("Constructing NOT with: ", arg)
        self.arg = arg

    def search(self):
        """Search the sentence for keyword instances."""
        all_files = set(file for files in idx.values() for file in files)

        return all_files - idx[self.arg]


class Conditional(Sentence):
    """Represents a conditional search."""

    def __init__(self, arg1: Sentence, arg2: Sentence):
        """Initialize a NOT search with a keyword."""
        self.arg1 = arg1
        self.arg2 = arg2

    def search(self):
        """Search the sentence for keyword instances."""
        return Or(Not(self.arg1), self.arg2).search()


x = Sentence("a") >> ~Sentence("a")

print(type(x))

print(simplify_logic(x))
