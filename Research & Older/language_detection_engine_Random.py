import random
import string
from langdetect import detect, LangDetectException
from nltk.corpus import words as nltk_words  # Use nltk words corpus if available

import nltk
nltk.download('words')


# Load a dictionary of valid words (Using nltk corpus)
valid_words = set(nltk_words.words())


# Function to check if a string is valid English
def is_valid_english_word(text):
    # Check if the string is in the valid words list (word length >= 3)
    return text in valid_words


# Function to check if a part is detected as English using langdetect
def is_english(text):
    try:
        if detect(text) == 'en':
            return True
    except LangDetectException:
        return False
    return False


# Generate 20,000 random 3-letter strings
count = 0
vowels = set("aeiou")

for _ in range(20000):
    random_string = ''.join(random.choices(string.ascii_lowercase, k=3))
    count += 1

    # Ensure the string has at least one vowel
    if not any(v in random_string for v in vowels):
        continue

    # Check if it's a valid English word
    if (is_english(random_string)
            and is_valid_english_word(random_string)):
        print(f"Valid Word found! {random_string} at count {count}")
