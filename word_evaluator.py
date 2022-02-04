#!/usr/bin/python3
import random
import argparse
import sys
import numpy as np
import wordle_search as ws
# import words
words = ws.words

# See how many words we have this evaluation of a guess compared to what we started with
words_dropped = lambda g, f, w: len(w) - len(ws.check_guess(g, f, w))

# Try a word against a few random words, see how much it narrows the range on average
def sample_score(word, wordlist, k = 20):
    """Try a word against k targets randomly chosen from our wordlist.
    Return the average number of words removed from the wordlist by the word for these targets."""
    targets = random.choices([w for w in wordlist], k = k)
    scores = np.array([words_dropped(word, ws.find_flags(word, target), wordlist) for target in targets])
    return np.mean(scores)

def score_pair(guess1, guess2, target, wordlist):
    """Try a pair of words and see how much they narrow the range"""
    next_wordlist = ws.check_guess(guess1, ws.find_flags(guess1, target), wordlist)
    return words_dropped(guess1, target, wordlist) + words_dropped(guess2, target, next_wordlist)

# Try a pair of words against a few random targets.
def sample_score_pair(guess1, guess2, wordlist, k = 20):
    """Try a pair of words against a few random targets."""
    targets = random.choices([w for w in wordlist], k = k)
    scores = np.array([score_pair(guess1, guess2, target, words) for target in targets])
    return np.mean(scores)

# CLI setup
parser = argparse.ArgumentParser(description="A program to help you choose a better first guess word for Wordle. Higher scores are better")
parser.add_argument("guess1", nargs = 1, metavar = "word1", type = str)
parser.add_argument("guess2", nargs = "?", metavar = "word2", type = str)
args = parser.parse_args()

def user_loop():
    if args.guess2:
        answer = sample_score_pair(words[0], words[1], words)
    else:
        answer = sample_score(args.guess1, words)
    print(answer, file = sys.stdout)

if __name__ == "__main__":
    user_loop()

# Initial analysis:
# See which words from our wordlist, when applied to a random sample of other words, cuts the wordlist by the most?
#layer1_scores = {w: sample_score(w, words, k=20) for w in words}
#layer1_sorted = dict(sorted(layer1_scores.items(), key = lambda x:x[1])) # sort words by scores and put back into dict
# check pairs of guesses
#layer2_scores = {g1: {g2: sample_score_pair(g1, g2, words, k = 20)} for g1 in words for g2 in words if g1 != g2}
#top_scores = sorted(layer2_scores.values().values()) # will this work?
