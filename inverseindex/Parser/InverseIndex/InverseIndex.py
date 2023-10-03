"""File that implements an inverse index class."""

from .tokenizer import tokenize, normalize, is_relevant
from pathlib import Path
from collections import defaultdict

from typing import Optional

from functools import cache

import logging

from Config import DOCUMENT_FOLDER, STOP_WORDS_FOLDER


def key_format(key: str) -> str:
    """Format a keyword to be used in a search."""
    if not is_relevant(key):
        raise ValueError(f'"{key}" is not a valid search term.')
    return normalize(key)


class InverseIndex:
    """A dictionary that maps words to a list of documents."""

    def __init__(self, documents: str, stop_words: Optional[str] = None):
        """Create an inverse index from a list of documents and stop words."""
        # https://docs.python.org/3/library/collections.html#collections.defaultdict
        self.index = defaultdict(set)
        self.ocurrences: dict[str, int] = defaultdict(int)

        documents_path = Path(documents)
        for file in documents_path.iterdir():
            if file.is_file():
                with open(file, "r") as r_file:
                    doc = r_file.read()
                    for word in tokenize(doc):
                        self.index[word].add(file.name)
                        self.ocurrences[word] += 1

        logging.info("Inverse index created.")
        logging.info(f"Number of words: {len(self.index)}")
        logging.info(
            f"Number of documents: {len(list(documents_path.iterdir()))}")

    @cache
    def __getitem__(self, key: str) -> set[str]:
        """Return the list of documents that contain the given word."""
        return self.index[key]

    def keys(self):
        """Return all the words in the index."""
        return self.index.keys()

    def values(self):
        """Forward the values method of the internal dictionary."""
        return self.index.values()


idx = InverseIndex(documents=DOCUMENT_FOLDER, stop_words=STOP_WORDS_FOLDER)
