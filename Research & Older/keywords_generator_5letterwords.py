import time
import mysql.connector
from langdetect import detect, LangDetectException
from nltk.corpus import words as nltk_words


def connect_to_database():
    """Connect to the MariaDB database."""
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="email_generation",
        charset='utf8mb4',  # Set the charset
        collation='utf8mb4_general_ci'  # Set a compatible collation
    )
    return conn


def create_table(cur):
    """Drop and create the 3-letter words table."""
    # Drop the table if it exists
    cur.execute('DROP TABLE IF EXISTS 5letters_words')

    # Create table for storing valid 3-letter words
    cur.execute('''
    CREATE TABLE IF NOT EXISTS 5letters_words (
        id INT AUTO_INCREMENT PRIMARY KEY,
        word VARCHAR(10) NOT NULL,
        count INT NOT NULL
    );
    ''')


def is_english(text):
    """Check if the text is detected as English using langdetect."""
    try:
        if detect(text) == 'en':
            return True
    except LangDetectException:
        return False
    return False


def filter_and_store_english_words(cur, valid_words):
    """Filter words of length 3 from nltk, check if langdetect recognizes them as English, and store them."""
    count = 0

    for word in valid_words:
        if len(word) == 5 and is_english(word):
            count += 1
            print(f"Valid Word found! {word} at count {count}")

            # Insert the valid word and count into the database
            cur.execute("INSERT INTO 5letters_words (word, count) VALUES (%s, %s)", (word, count))


def main():
    """Main function to execute the script."""
    start_time = time.time()

    # Connect to the database
    conn = connect_to_database()
    cur = conn.cursor()

    # Drop and create table
    create_table(cur)
    conn.commit()

    # Load valid English words from nltk
    valid_words = set(nltk_words.words())

    # Filter words of length 3 and check if they're English
    filter_and_store_english_words(cur, valid_words)

    # Commit all the changes and close the connection
    conn.commit()
    cur.close()
    conn.close()

    end_time = time.time() - start_time
    print(f"Compute Time: {end_time} seconds")


if __name__ == "__main__":
    main()
