# wordle_search
Python script to help me narrow down my wordle guesses.

In it's current state it will work if you run `python ./wordle_search.py` in the
appropriate directory. Start by playing your favorite starter word on Wordle,
then type that word followed by a string of digits indicating how your word was
evaluated.

For example, on February 1st, my favorite starter word ('chaos') returned
"02011" where 0 is a grey square (no match), 1 is a yellow square (right letter,
wrong place), and 2 is a green square (right letter, right place). 

After getting that result from the Wordle site, type `chaos 02011` into the
program and it will return a list of viable guesses:

`['shoji', 'ghost', 'shone', 'shove', 'those', 'shout', 'showy', 'short', 'whose', 'shore', 'shown']`

Continuing this way will return shorter and shorter lists until you've got a
winning guess. Hopefully it happens quickly enough for a win!

To evaluate a starting word, you can run `word_evaluator.py`. At the terminal
prompt, run the following command for help.

```
$ python ./word_evaluator.py -h
```

If you give it a single word, it will tell you how many words that guess will
eliminate from the list of possibilities on average. (Higher scores are better). 

If you give it a pair of words, it will tell you how many words are eliminated
by making both of those guesses. Putting in the same word twice should give you
the same results as putting it in once.
