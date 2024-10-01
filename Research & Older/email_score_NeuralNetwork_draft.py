import random
import string

# Allowed Gmail characters
ALLOWED_CHARACTERS = string.ascii_lowercase + string.digits + "._-"

# Some common words/names
COMMON_WORDS = ["john", "jane", "love", "peace", "happy", "alex", "star", "light", "sun", "moon"]

# Weights for different conditions (tune these based on experimentation)
WEIGHT_WORD_MATCH = 2.0
WEIGHT_PATTERN = 1.5
WEIGHT_CONSECUTIVE_PENALTY = -1.0
WEIGHT_STARTS_WITH_LETTERS = 1.8


# Function to check if a string contains a common word
def contains_word(email):
    for word in COMMON_WORDS:
        if word in email:
            return True
    return False


# Function to check for human-like patterns
def is_human_pattern(email):
    # Simple example: check for "name.number" pattern or "first.last"
    if any(char.isdigit() for char in email) and '.' in email:
        return True
    if '.' in email and email.count('.') == 1:
        return True
    return False


# Function to penalize for consecutive same-type characters
def has_consecutive_characters(email):
    for i in range(len(email) - 2):
        if email[i].isalpha() and email[i + 1].isalpha() and email[i + 2].isalpha():
            return True
        if email[i].isdigit() and email[i + 1].isdigit() and email[i + 2].isdigit():
            return True
    return False


# Function to score the email based on the criteria
def score_email(email):
    score = 0

    # Add weight if it contains a common word
    if contains_word(email):
        score += WEIGHT_WORD_MATCH

    # Add weight for human-like patterns
    if is_human_pattern(email):
        score += WEIGHT_PATTERN

    # Penalize for consecutive characters
    if has_consecutive_characters(email):
        score += WEIGHT_CONSECUTIVE_PENALTY

    # Add weight if it starts with letters
    if email[:2].isalpha():
        score += WEIGHT_STARTS_WITH_LETTERS

    return score


########################
## Main Script Starts ##
########################



# Generate and score 10 emails
for _ in range(10):
    score = score_email()
    print(f"Generated email: {email}, Score: {score}")
