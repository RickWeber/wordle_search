#!/usr/bin/python
import re, os, random
import numpy as np
# Word setup
words = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
    "wordle_wordlist"),
    "r"
    ).read().split("\n")
words = set(words)
num_words = len(words)
# letter frequency
letter_freq = lambda s: [s.count(c) for c in s]
duplicates = lambda word: [c for c, d in zip(word, letter_freq(word)) if d > 1]

def flag(guess, target):
    guess = np.array([c for c in guess])
    target = np.array([c for c in target])
    # easy cases
    return_flag = np.array([2 if g == t else 0 for g, t in zip(guess, target)])
    # right letter, wrong position, not already accounted for
    trimmed_target = np.array(target)[return_flag != 2]
    f1 = [1 if (g in trimmed_target) and (f != 2) else 0 for g, f in zip(guess, return_flag)]
    return_flag += f1
    return stringify(return_flag)

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
    new_count = len(check_guess(guess, flag(guess, target), wordlist))
    return initial_count - new_count

def sample_score(word, wordlist, k = 20):
    score = 0
    random_targets = random.choices([w for w in wordlist if w != word], k = k)
    for t in random_targets:
        score += words_dropped(word, t, wordlist) / k
    return score

def score_pair(guess1, guess2, target, wordlist):
    next_wordlist = check_guess(guess1, flag(guess1, target), wordlist)
    return words_dropped(guess1, target, wordlist) + words_dropped(guess2, target, next_wordlist)

def sample_score_pair(guess1, guess2, wordlist, k = 20):
    score = 0
    random_targets = random.choices([w for w in wordlist if w not in [guess1, guess2]]))
    for t in random_targets:
        score += score_pair(guess1, guess2, t, wordlist)
    return score

# Initial analysis:
# See which words from our wordlist, when applied to a random sample of other words, cuts the wordlist by the most?
layer1_scores = [sample_score(w, words, k=20) for w in words]
# check pairs of guesses
layer2_scores = [[g1, g2, sample_score_pair(g1, g2, words, k = 20)] for g1 in words for g2 in words if g1 != g2]
layer2_scores.sort(lambda pair: pair[2],reverse=True)

