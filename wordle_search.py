#!/usr/bin/python3
import re
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
