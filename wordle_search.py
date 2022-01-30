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

def letters_in_pos(**letterAndPosition):
    rex = ['.' for i in range(5)]
    for i in range(5):
        if letterAndPosition[i]:
            rex[i] + letterAndPosition[i]
    rex = re.compile("".join(rex))
    return [w for w in words if re.search(rex, w)]
