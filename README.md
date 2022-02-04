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

The wordlist is shamelessly ripped off from wordle.

## The state of the project:
I've got the basic logic sorted out and it works as an interactive command line
program if you run it at the terminal. That's `wordle_search.py`. Requiring the
user to type a string of flags (the tri-nary number that looks this: 00212) is a
bit annoying. Ideally I'd just pull the information directly from the dom on the
game you're playing. That could be addressed with a browser plugin that pulls
updated values directly from the page. 

`word_evaluator.py` is a script I'm currently working on. It will try to find an
optimal strategy for wordle. Or at least a good first guess. Currently, there's
logic to evaluate individual words relative to each other, given any particular
target word (meaning 12973 guesses to test against 12973 possible targets).
There's also logic to evaluate a pair of words to be used one after another. I
wonder if a not-good strategy is to guess something like "light" followed by
"saint" where both guesses are too similarly to be useful as a pair. Is there a
best pair of words that covers as much of the set of words as possible? 

In both scripts, I'm working on cleaning up the code. Deleting vestigial
lambdas, adjusting function names so I don't need to comment the code, etc.
