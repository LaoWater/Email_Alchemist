import time
import mysql.connector
from langdetect import detect, LangDetectException
from nltk.corpus import words as nltk_words


def is_english(text):
    """Check if the text is detected as English using langdetect."""
    try:
        if detect(text) == 'en':
            return True
    except LangDetectException:
        return False
    return False


def filter_and_store_english_words(valid_words):
    """Filter words of length 3 from nltk, check if langdetect recognizes them as English, and store them."""
    count = 0

    for word in valid_words:
        if len(word) == 4 and not is_english(word):
            count += 1
            print(f"NLTK Valid but Invalid on LangDetect: {word} at count {count}")


# Load valid English words from nltk
valid_words = set(nltk_words.words())
filter_and_store_english_words(valid_words)
