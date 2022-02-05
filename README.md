# wordle_search
A python script to help me narrow down my wordle guesses.

At the terminal run:

```
$ python ./wordle_search.py
```

You can evaluate starting words against possible targets (menu option 1), or get help choosing your subsequent guesses (menu option 2).

With the first option, you can compare a list of options (for example, if you want to dunk on your friends for using 'peppy' as their starting word), or get a random set of starting words ranked from best to worst.

For getting help with subsequent guesses, you'll enter your word and a series of flags to represent letter matches (where 0, 1, and 2 correspond with grey, yellow, and green squares).

For example, on February 1st, my favorite starter word ('chaos') returned
"02011" where 0 is a grey square (no match), 1 is a yellow square (right letter,
wrong place), and 2 is a green square (right letter, right place). 

After getting that result from the Wordle site, type `chaos 02011` into the
program and it will return a list of viable guesses:

`['shoji', 'ghost', 'shone', 'shove', 'those', 'shout', 'showy', 'short', 'whose', 'shore', 'shown']`

Continuing this way will return shorter and shorter lists until you've got a
winning guess. Hopefully it happens quickly enough for a win!