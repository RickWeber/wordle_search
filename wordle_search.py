#!/usr/bin/python3
import random
import re
import numpy as np
#from english_words import english_words_lower_alpha_set as words
#words = [w for w in words if len(w) == 5]

# Word setup
with open("wordle_wordlist") as file:
    words = file.read().split("\n")

# Instructions for users
help_text = """Please enter your initial guess and the results in the following form:

guess 00122

replacing "guess" with the word you guessed, and the digits corresponding with 
the results of your guess. "0" representing letters that aren't present (grey squares),
"1" representing letters that are in the wrong place (yellow squares) and "2" 
representing letters that are in the correct place (green squares).

Don't put either part of your guess in quotation marks.

Enter "exit" to exit the program.
"""

def main_menu():
    """offer the user a set of options, and set them up to use 
    that option."""
    print("Welcome. Would you like to find a good starter word [1] or find some follow-up guesses?")
    move = input("Please enter 1, 2, or quit: ")
    if move.lower() in ["q","quit","exit","x","stop"]:
        quit()
    if move not in ['1', '2']:
        print("I didn't understand your input. Let's try this again...")
        main_menu()
    if move == '1':
        compare_words_menu()
    elif move == '2':
        play_round_menu()
    else:
        quit()

def compare_words_menu():
    print("Do you have a word (or a few words) in mind that you'd like to check?")
    given_words = input("Please enter yes or no: ")
    if 'y' in given_words.lower():
        print("I'm ready when you are. Type in your words, separated by spaces, then hit 'Enter'")
        guesses = input('> ')
    else:
        print("Here are ten random words, and their score (higher is better):")
        guesses = random.choices(words, k=10)
    results = [[g, sample_score(g, words)] for g in guesses]
    print(results)

def play_round(wordlist):
    guess, flags = take_input(False)
    return filter_based_on_guess(guess, flags, [w for w in wordlist])

def play_round_menu():
    possible_words = words
    print(help_text)
    print("\nHere are some random words to consider as a first guess\n")
    print(random.choices(possible_words, k = 10))
    for r in range(5):
        print("Round " + str(r) + ":\n")
        possible_words = play_round(possible_words)
        #print(possible_words)
        print(random.choices(possible_words, k = 9))
        if len(possible_words) < 1:
            break

def take_input(first = True):
    """Take input, allow exit or ask for help
    deal with incorrect syntax and simple fix
    for input in wrong order"""
    if first:
        print(help_text)
        data = input("> ")
    else:
        data = input("> ")
    if data.lower() in ["q","quit","exit","x","stop"]:
        quit()
    if data.lower() in ["h", "help"]:
        print(help_text)
        data = take_input(False)
    while len(data) != 11: 
        print("Your guess, and the flags should each be 5 characters long.")
        print("incorrect syntax, please try again...")
        data = take_input(False)
    if data[5] != ' ':
        print("Your guess and the flags should be separated by one space.")
        print("incorrect syntax, please try again...")
        data = take_input(False)
    guess, flags = data.split(' ')
    if flags.isalpha() and guess.isdigit():
        guess, flags = flags, guess
    if not flags.isdigit() or not guess.isalpha():
        print("Your guess should be made up only of letters")
        print("Your flags should be made up only of the digits 0, 1, and 2")
        print("incorrect syntax, please try again...")
        data = take_input(False)
    return guess, flags

# Functions to narrow word set
success = lambda f: f == "22222"
include_reg = lambda c: "[" + c + "]+"
exclude_reg = lambda c: "[^" + c + "]"
wrap_up = lambda guess, flags: enumerate(zip([c for c in guess.lower()], [f for f in flags]))
reg_filter = lambda regex, wordlist: [w for w in wordlist if re.search(regex, w)]

def filter_correct_positions(guess, flags, wordlist = words):
    """filter wordlist to those with letters in the right place"""
    pos_reg = re.compile("".join([c if f == "2" else '.' for c, f in zip(guess, flags)]))
    return reg_filter(pos_reg, wordlist)

def filter_wrong_positions(guess, flags, wordlist = words):
    """filter wordlist to cut out letters in known wrong places"""
    pos_reg = re.compile("".join([exclude_reg(c) if f == "1" else '.' for c, f in zip(guess, flags)]))
    return reg_filter(pos_reg, wordlist)

def filter_correct_letters(guess, flags, wordlist = words):
    """filter wordlist to those with the right letters, somewhere in there."""
    correct_letters = [c for c, f in zip(guess, flags) if int(f) > 0]
    for l in correct_letters: # For each letter we know belongs:
        has_letter = re.compile(include_reg(l))
        wordlist = reg_filter(has_letter, wordlist) # make sure there's at least one of this letter
    return wordlist

# Create an appropriate set of flags given a guess and target
def find_flags(guess, target):
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
    f1 = np.array(f1)
    return_flag += f1
    "".join(map(str, return_flag.tolist())) # Convert to compact string.

### Tests
#flag("guess", "stash") == 00021
#flag("guess", "atash") == 00020
#flag("guess", "stach") == 00011 # I can't think how you would choose which s to give it to without making things needlessly complicated.

def filter_wrong_letters(guess, flags, wordlist = words):
    """filter letters that don't belong, but take account of green squares."""
    wrong_letters = "".join([c for c, f in zip(guess, flags) if f == "0"])
    # only exclude the wrong letters from places where we don't already know what goes there.
    pos = [exclude_reg(wrong_letters) if f != "2" else '.' for c, f in zip(guess, flags)]
    pos_reg = re.compile("".join(pos))
    return reg_filter(pos_reg, wordlist)

def filter_based_on_guess(guess, flags, wordlist = words):
    wordlist = filter_correct_positions(guess, flags, wordlist)
    wordlist = filter_wrong_positions(guess, flags, wordlist)
    wordlist = filter_correct_letters(guess, flags, wordlist)
    wordlist = filter_wrong_letters(guess, flags, wordlist)
    return wordlist

def maximum_entropy_words(word_list):
    """prefer words with more different letters, and more likely letters"""
    return word_list


# See how many words we have this evaluation of a guess compared to what we started with
words_dropped = lambda g, f, w: len(w) - len(ws.filter_based_on_guess(g, f, w))

# Try a word against a few random words, see how much it narrows the range on average
def sample_score(word, wordlist, k = 20):
    """Try a word against k targets randomly chosen from our wordlist.
    Return the average number of words removed from the wordlist by the word for these targets."""
    targets = random.choices([w for w in wordlist], k = k)
    scores = np.array([words_dropped(word, ws.find_flags(word, target), wordlist) for target in targets])
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


if __name__ == "__main__":
    main_menu()