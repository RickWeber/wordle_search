#!/usr/bin/python3
import random
import argparse
import sys
import numpy as np
import wordle_search as ws
# import words
words = ws.words

# See how many words we have this evaluation of a guess compared to what we started with
words_dropped = lambda g, f, w: len(w) - len(ws.filter_based_on_guess(g, f, w))

# Try a word against a few random words, see how much it narrows the range on average
def sample_score(word, wordlist, k = 20):
    """Try a word against k targets randomly chosen from our wordlist.
    Return the average number of words removed from the wordlist by the word for these targets."""
    tgts = random.choices([w for w in wordlist], k = k)
    scores = np.array([words_dropped(word, ws.find_flags(word, target), wordlist) for target in tgts])
    return np.mean(scores)

def score_pair(guess1, guess2, target, wordlist):
    """Try a pair of words and see how much they narrow the range"""
    next_wordlist = ws.filter_based_on_guess(guess1, ws.find_flags(guess1, target), wordlist)
    return words_dropped(guess1, target, wordlist) + words_dropped(guess2, target, next_wordlist)

# Try a pair of words against a few random targets.
def sample_score_pair(guess1, guess2, wordlist, k = 20):
    """Try a pair of words against a few random targets."""
    targets = random.choices([w for w in wordlist], k = k)
    scores = np.array([score_pair(guess1, guess2, target, words) for target in targets])
    return np.mean(scores)

# CLI setup
help_text = """ A program to help you make better initial guesses.
Enter one word to see how many words it eliminates from the word list on average. 
The higher the number, the better that guess is.

Enter two words to do the same thing for your first two guesses.

"A program to help you choose a better first guess word for Wordle. Higher scores are better"
"""
parser = argparse.ArgumentParser(description=help_text)
parser.add_argument("guess1", nargs = 1, metavar = "word1", type = str)
parser.add_argument("guess2", nargs = "?", metavar = "word2", type = str)
#parer.add_argument("--compare") compare a list of first guesses against each other.
args = parser.parse_args()

def user_loop():
    answer = sample_score(args.guess1, words)
    print(answer, file = sys.stdout)

if __name__ == "__main__":
    user_loop()
