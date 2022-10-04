"""Generate Markov text from text files."""

from fileinput import filename
from random import choice
import sys


def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    poem = ""
    for line in open(file_path):
        line = line.rstrip()
        poem = poem + line + ' '
    
    poem.rstrip()

    return poem


def make_chains(text_string, n_gram = 2):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains('hi there mary hi there juanita')

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']

        >>> chains[('there','juanita')]
        [None]
    """

    chains = {}

    poem = text_string.split(' ')

    count = 1
    while count < len(poem) - 1:
        # print(f"line 54 count: {count}")
        tup = (poem[count - 1], poem[count])
        value = chains.get(tup,[])
        value.append(poem[count + 1])
        chains[tup] = value
        count += 1

    return chains


def make_text(chains):
    """Return text from chains."""

    words = []

    starting_point = choice(list(chains.keys()))  #get a tuple of words
    words.extend([starting_point[0], starting_point[1]])

    while True:
        tup = (words[-2], words[-1])
        try:
            value = chains[tup]
            words.append(choice(value))
        except: break

    return ' '.join(words)


# input_path = 'green-eggs.txt'
# input_path = 'gettysburg.txt'
input_path = sys.argv[1]

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

# Get a Markov chain
chains = make_chains(input_text)

# Produce random text
random_text = make_text(chains)

print(random_text)
