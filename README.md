# Termle

Tiny Wordle clone written in Python.

## Usage

`python termle.py [-h] [--length LENGTH] [--guesses GUESSES] [--dictionary DICTIONARY]`

### Arguments

1. -l or --length: Length of the words to be generated. (default: 5).
2. -g or --guesses: Number of guesses allowed before the game ends. (default: 6)
3. -d or --dictionary: Dictionary file to be used (default: ./dictionary.json)

## In-game commands

When in an game, you can use the following commands:

1. !quit or !q: Quit the game
2. !restart or !r: Restart the game
3. !d: Show the size of the dictionary

## Dependencies

`colorama==0.4.4`

## Future Improvements

- [ ] Dependency-less mode

- [ ] Automatically use the in-built system dictionary
