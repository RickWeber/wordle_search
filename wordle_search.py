#!/usr/bin/python3
import re, os, random
#from english_words import english_words_lower_alpha_set as words
#words = [w for w in words if len(w) == 5]

# Word setup
words = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
    "wordle_wordlist"),
    "r"
    ).read().split("\n")
words = list(set(words))
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

# Take input, allow exit or ask for help
# deal with incorrect syntax and simple fix
# for input in wrong order
def take_input(first = True):
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
#####
# NOTE:
# Somewhere in here, some letters aren't being fully filtered out.
success = lambda f: f == "22222"
include_reg = lambda c: "[" + c + "]+"
exclude_reg = lambda c: "[^" + c + "]"
wrap_up = lambda guess, flags: enumerate(zip([c for c in guess.lower()], [f for f in flags]))
def reg_filter(regex, selected_words):
    return [w for w in selected_words if re.search(regex, w)]

def filter_correct_positions(guess, flags, selected_words = words):
    pos_reg = re.compile("".join([c if f == "2" else '.' for c, f in zip(guess, flags)]))
    return reg_filter(pos_reg, selected_words)

def filter_wrong_positions(guess, flags, selected_words = words):
    pos_reg = re.compile("".join([exclude_reg(c) if f == "1" else '.' for c, f in zip(guess, flags)]))
    return reg_filter(pos_reg, selected_words)

def filter_correct_letters(guess, flags, selected_words = words):
    correct_letters = [c for c, f in zip(guess, flags) if int(f) > 0]
    for l in correct_letters:
        has_letter = re.compile(include_reg(l))
        selected_words = reg_filter(has_letter, selected_words)
    return selected_words

letter_freq = lambda s: [s.count(c) for c in s]
duplicates = lambda word: [c for c, d in zip(word, letter_freq(word)) if d > 1]

def filter_wrong_letters(guess, flags, selected_words = words):
    wrong_letters = "".join([c for c, f in zip(guess, flags) if f == "0"])
    # only exclude the wrong letters from places where we don't already know what goes there.
    pos = [exclude_reg(wrong_letters) if f != "2" else '.' for c, f in zip(guess, flags)]
    pos_reg = re.compile("".join(pos))
    return reg_filter(pos_reg, selected_words)

def check_guess(guess, flags, selected_words = words):
    selected_words = filter_correct_positions(guess, flags, selected_words)
    selected_words = filter_wrong_positions(guess, flags, selected_words)
    selected_words = filter_correct_letters(guess, flags, selected_words)
    selected_words = filter_wrong_letters(guess, flags, selected_words)
    return selected_words

def maximum_entropy_words(word_list):
    """prefer words with more different letters, and more likely letters"""
    return word_list # TODO: Implement!

def play_round(selected_words):
    guess, flags = take_input(False)
    return check_guess(guess, flags, [w for w in selected_words])

def user_loop():
    possible_words = words
    print(help_text)
    #print("\nHere are some random words to consider as a first guess\n")
    #print(random.choices(possible_words, k = 30))
    for r in range(6):
        print("Round " + str(r) + ":\n")
        possible_words = play_round(possible_words)
        #word_sample = random.choices(possible_words, k = 10)
        #print(word_sample)
        print(possible_words)
        if len(possible_words) < 2:
            break

if __name__ == "__main__":
    user_loop()
