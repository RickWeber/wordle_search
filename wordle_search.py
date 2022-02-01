#!/usr/bin/python3
import re, sys
from english_words import english_words_lower_alpha_set as words

words = [w for w in words if len(w) == 5]
def words_with_letters(letters):
    rex = re.compile("[" + letters + "]{5}")
    return [w for w in words if re.search(rex, w)]

def words_without_letters(letters):
    rex = re.compile("[^" + letters + "]{5}")
    return [w for w in words if re.search(rex, w)]

def letters_in_position(l1='.',l2='.',l3='.',l4='.',l5='.'):
    rex = re.compile("["+l1+l2+l3+l4+l5+"]")
    return [w for w in words if re.search(rex, w)]

def guess_and_flags(guess, flags):
    if flags == "22222":
        print("Congratulations!")
    stuff = enumerate(zip([c for c in guess], [f for f in flags]))
    regex = ['.' for i in range(5)]
    exclude = []
    include = []
    for i, c, f in stuff:
        if f == 0:
            exclude.append(c)
        if f == 1:
            include.append(c)
            regex[i] = "[^" + c + "]"
        if f == 2:
            regex[i] = c
    if exclude:
        exclude_clause = re.compile("[^" + "".join(exclude) + "]")
        words = [w for w in words if re.search(exclude_clause, w)]
    if include:
        include_clause = re.compile("[" + "".join(include) + "]")
        words = [w for w in words if re.search(include_clause, w)]
    positional_clause = re.compile("[" + "".join(regex) + "]")
    words = [w for w in words if re.search(positional_clause, w)]
    return words

def maximum_entropy_words(word_list):
    """prefer words with more different letters, and more likely letters"""

help_text = """Please enter your initial guess and the results in the following form:

guess 00122

replacing "guess" with the word you guessed, and the digits corresponding with 
the results of your guess. "0" representing letters that aren't present (grey squares),
"1" representing letters that are in the wrong place (yellow squares) and "2" 
representing letters that are in the correct place (green squares).
"""


def main():
    if sys.argv[1] == "help":
        print(help_text)
    if sys.argv[1].lower() in ["q","quit"]:
        exit
    guess = sys.argv[1]
    flags = sys.argv[2]
    print(letters_in_position(guess))


if __name__ == "__main__":
    main()