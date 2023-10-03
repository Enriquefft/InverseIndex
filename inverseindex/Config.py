"""Config file for the project."""
import logging
from typing import Final

logging.basicConfig(level=logging.INFO)

DOCUMENT_FOLDER: Final[str] = "Books"
STOP_WORDS_FOLDER: Final[str | None] = None
