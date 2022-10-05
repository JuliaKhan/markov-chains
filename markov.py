"""Generate Markov text from text files."""

from fileinput import filename
from random import choice
from re import L
import sys

#how long is the n-gram?
n_gram = int(sys.argv[2])


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


def make_chains(text_string, n_gram = n_gram):
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

    poem = text_string.split()  #w/o arg it accepts any amount of whitespace

    count = n_gram
    while count < len(poem):
        subcount = n_gram
        gram = []
        while subcount > 0:
            gram.append(poem[count - subcount])
            subcount -= 1
        tup = tuple(gram)
        value = chains.get(tup,[])
        value.append(poem[count])
        chains[tup] = value
        count += 1

    return chains


def make_text(chains, n_gram = n_gram):
    """Return text from chains."""

    cap_words = []
    capitals = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for key in chains.keys():
        if key[0][0] in capitals:
            cap_words.append(key)       #makes sure first word is capitalized
    starting_point = choice(cap_words)  #get a tuple of words
    
    words = list(starting_point)

    while True:
        tup = []
        for i in range(0,n_gram):
            tup.append(words[i - n_gram])
        tup = tuple(tup)
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
