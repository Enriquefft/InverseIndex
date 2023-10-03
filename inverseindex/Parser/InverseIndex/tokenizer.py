"""This module contains the tokenizer for the IR system."""
from nltk import word_tokenize, corpus, stem, download as nltk_download
import logging
from typing import Optional, Final

from string import punctuation

nltk_download("stopwords")
nltk_download("wordnet")
nltk_download("punkt")

Debug: Final[bool] = True


def is_relevant(word: str) -> bool:
    """Check if a  word is relevant."""
    return True


def clean_str(word: str) -> str:
    """Normalize a word."""
    result = ""
    for char in word:
        if char in punctuation:
            pass
        elif char.isupper():
            result += char.lower()
        else:
            result += char
    return result


stemmer = stem.SnowballStemmer("spanish")


def normalize(word: str) -> str:
    """Normalize a word by cleaning it and applying stemming."""
    return stemmer.stem(clean_str(word))


def tokenize(document: str,
             stopwords_doc: Optional[set[str]] = None) -> set[str]:
    """Tokenize a document into a list of sorted words.

    Args:
        document (str): The document to tokenize as a string.
        stopwords ([str]): A list of stopwords to remove.

    Process:
    1. Tokenize the document.
    2. Remove non-alphabetic words. # Currently diabled
    3. Normalize the words. (lowercase and remove punctuation)
    4. Apply Snowball Stemming.
    5. Remove stopwords.
    """
    # Get the stopwords to be used
    stop_words = corpus.stopwords.words("spanish")
    if stopwords_doc is not None:
        # Merge the stopwords from the document with the default stopwords.
        stop_words = set(stop_words).union(stopwords_doc)
    logging.debug(f"Using {len(stop_words)} stopwords.")

    # Tokenization
    words: set[str] = word_tokenize(document)
    logging.debug(f"Tokenized {len(words)} words.")

    # Remove non-alphabetic words && apply lematization
    words = {normalize(word) for word in words if is_relevant(word)}

    logging.debug(f"Relevant tokens: {len(words)}")

    # Trim stopwords
    words = {word for word in words if word not in stop_words}

    logging.debug(f"Tokens after stopword removal: {len(words)}")

    return words
