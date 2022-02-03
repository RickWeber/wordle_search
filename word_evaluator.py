#!/usr/bin/python3
import functools
import re, os, random, argparse, sys
import numpy as np
import wordle_search as ws
# Word setup
words = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), # is there a better way to do this?
    "wordle_wordlist"),
    "r"
    ).read().split("\n")
words = [word.strip() for word in words]
num_words = len(words)

# letter frequency
letter_freq = lambda s: [s.count(c) for c in s]
duplicates = lambda word: [c for c, d in zip(word, letter_freq(word)) if d > 1]

# Create an appropriate set of flags given a guess and target
def flag(guess, target):
    guess = np.array([c for c in guess])
    target = np.array([c for c in target])
    # easy cases
    return_flag = np.array([2 if g == t else 0 for g, t in zip(guess, target)])
    # right letter, wrong position, not already accounted for
    if any(return_flag == 2):
        trimmed_target = np.array(target)[return_flag != 2]
        f1 = [1 if (g in trimmed_target) and (f != 2) else 0 for g, f in zip(guess, return_flag)]
    else:
        f1 = [1 if g in target else 0 for g in guess]
    return_flag += f1
    return stringify(return_flag)

# Convert those flags into a string
def stringify(nparr):
    lst = nparr.tolist()
    return "".join(map(str, lst))

### Tests
#flag("guess", "stash") == 00021
#flag("guess", "atash") == 00020
#flag("guess", "stach") == 00011 # I can't think how you would choose which s to give it to without making things needlessly complicated.

# For a given word, and a given target see how much it narrows the range of possible words
def words_dropped(guess, target, wordlist):
    flags = flag(guess, target)
    initial_count = len(wordlist)
    new_count = len(ws.check_guess(guess, flags, wordlist))
    return initial_count - new_count

# Try a word against a few random words, see how much it narrows the range on average
def sample_score(word, wordlist, k = 20):
    random_targets = random.choices([w for w in wordlist if w != word], k = k)
    scores = np.array([words_dropped(word, target, wordlist) for target in random_targets])
    return np.mean(scores)

# Try a pair of words (in order) and see how much they narrow the range
def score_pair(guess1, guess2, target, wordlist):
    next_wordlist = ws.check_guess(guess1, flag(guess1, target), wordlist)
    return words_dropped(guess1, target, wordlist) + words_dropped(guess2, target, next_wordlist)

# Try a pair of words against a few random targets.
def sample_score_pair(guess1, guess2, wordlist, k = 20):
    score = 0
    random_targets = random.choices([w for w in wordlist if w not in [guess1, guess2]])
    for t in random_targets:
        score += score_pair(guess1, guess2, t, wordlist)
    return score

# Initial analysis:
# See which words from our wordlist, when applied to a random sample of other words, cuts the wordlist by the most?
#layer1_scores = {w: sample_score(w, words, k=20) for w in words}
#layer1_sorted = dict(sorted(layer1_scores.items(), key = lambda x:x[1])) # sort words by scores and put back into dict
# check pairs of guesses
#layer2_scores = {g1: {g2: sample_score_pair(g1, g2, words, k = 20)} for g1 in words for g2 in words if g1 != g2}
#top_scores = sorted(layer2_scores.values().values()) # will this work?

# CLI setup
parser = argparse.ArgumentParser(description="A program to help you choose a better first guess word for Wordle. Higher scores are better")
parser.add_argument("guess", nargs = 1, metavar = "word", type = str)
args = parser.parse_args()

def user_loop():
    answer = sample_score(args.guess, words, 100)
    print(answer, file = sys.stdout)

if __name__ == "__main__":
    user_loop()
