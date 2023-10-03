"""Generate 15 files with random words."""

import random
import nltk
from nltk.corpus import words

# Download the words corpus if not already downloaded
nltk.download('words')

# Get a list of all English nouns
all_nouns = [word for word in words.words() if word.isalpha()]


def generate_files(num_files, num_nouns, words_per_file):
    # Select a specified number of random nouns
    selected_nouns = random.sample(all_nouns, num_nouns)

    # Create a dictionary to keep track of how many times each noun has been used
    noun_counts = {noun: 0 for noun in selected_nouns}

    # Ensure each noun is in at least one file
    for i, noun in enumerate(selected_nouns):
        with open(f'Tests/file{i%num_files+1}.txt', 'a') as f:
            f.write(noun + "\n")
        noun_counts[noun] += 1

    # Fill the rest of the files with random nouns
    for i in range(num_files):
        with open(f'Tests/file{i+1}.txt', 'a') as f:
            for _ in range(
                    words_per_file -
                    len(open(f'Tests/file{i+1}.txt').read().split("\n")) + 1):
                noun = random.choice(selected_nouns)
                # Ensure the noun has not been used more than 7 times
                while noun_counts[noun] >= 7:
                    noun = random.choice(selected_nouns)
                f.write(noun + "\n")
                noun_counts[noun] += 1


# Call the function with your desired parameters
generate_files(num_files=15, num_nouns=20, words_per_file=5)
