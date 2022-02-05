import argparse
import json
import random

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, prog="Termle", 
                            description="Termle: Tiny Wordle clone written in Python.",
                            epilog="in-game commands: Use '!' to pass commands while playing:\n  !quit, !q: Quits the game.\n  !restart, !r: Restart with a new word.\n  !d: See the current size of the word dictionary")
parser.add_argument('--length','-l', default=5, required=False, type=int, help="Length of the words. (Ensure that the dictionary has words with the same length)")
parser.add_argument('--guesses','-g', default=6, required=False, type=int, help="Number of guesses allowed per game.")
parser.add_argument('--dictionary','-d', default='./dictionary.json', required=False, help="Dictionary file to use, defaults to dictionary.json in the current folder. The file is a list of strings.")
args = parser.parse_args()

try:
    from colorama import Back, Fore, Style, init
    init(autoreset=True)
except:
    print("Termle cannot import `Colorama`— this module allows Termle to show colors when you enter words. You can install it using 'pip3 install colorama'")
    exit(-1)

TERMLE_LEN = args.length
NUM_GUESSES = args.guesses
DICTIONARY_FILE = args.dictionary

class Word:
    # Stores the state of the word and the truth state of each letter (0, 1 or 2).
    def __init__(self, word=None, truth=None):
        '''__init__ Function definition. '''
        if not truth:
            # 0 for wrong, 1 for wrong position and 2 for correct
            truth = [0 for _ in range(TERMLE_LEN)]
        self.word = word
        self.truth = truth
    def __repr__(self):
        '''__repr__ Function definition. '''
        if self.word:
            return self.word
        else:
            return "'N/A'"
 
class Board:
    # Collection of Words making up a single game.
    def __init__(self, words, dictionary):
        '''__init__ Function definition. '''
        if len(dictionary) == 0:
            raise IndexError("Dictionary Empty")
        elif len(dictionary[0] > TERMLE_LEN):
            raise AssertionError("Passed word length doesn't match the dictionary word length.")
        self.words = words
        # print(">>>INIT ", self.words)
        self.guesses = NUM_GUESSES
        self.dictionary = dictionary
        self.solve_word = random.choice(self.dictionary)

    def add(self, word):
        '''add Function definition. '''
        self.words[NUM_GUESSES - (self.guesses)] = word
        # print("Storing at index: ", NUM_GUESSES - (self.guesses))
        # print(">>>STORE ", self.words)
        self.guesses -= 1
        if self.guesses == 0 and sum(word.truth)!= 2*len(word.truth): # Every truth value is not 2 and no guesses left.
            self.print(msg=Fore.RED + f"You Lost :( The word was: {self.solve_word}")
        elif sum(word.truth) == 2*len(word.truth): # Every truth value is 2, i.e. all letters are at the correct position
            self.print(msg=Fore.GREEN + "Nice!")

    def print(self, msg=None):
        '''print Function definition. Prints each word, along with the color of each letter.'''
        for word in self.words:
            if not word.word:
                for _ in range(TERMLE_LEN):
                    print(Back.RED + Fore.WHITE + ' ' + Style.RESET_ALL + ' ', end='')
                print()
            else:
                for idx,char in enumerate(word.word):
                    if word.truth[idx] == 0:
                        print(Back.RED + Fore.WHITE + char + Style.RESET_ALL + ' ', end='')
                    elif word.truth[idx] == 1:
                        print(Back.YELLOW + Fore.BLACK + char + Style.RESET_ALL + ' ', end='')
                    else:
                        print(Back.GREEN + Fore.WHITE + char + Style.RESET_ALL + ' ', end='')
                print()
        print()
        if not msg:
            print(Fore.BLUE + f'Guesses Left: {self.guesses}')
        print()

    def get_guess(self, guess):
        '''get_guess Function definition. '''
        valid = True
        guess = guess.lower().strip()
        if guess not in self.dictionary or not guess.isalpha():
            print(Fore.RED + f"{guess} not in dictionary\n")
            return
        truth = []
        seen = {i: False for i in self.solve_word}
        for idx, c in enumerate(guess):
            # print(c, self.solve_word[idx], seen)
            if c == self.solve_word[idx]:
                truth.append(2)
                seen[c] = True
            elif c in self.solve_word and c in seen and not seen[c]:
                truth.append(1)
                seen[c] = True
            else:
                truth.append(0)
        if valid:
            self.add(Word(guess, truth))
            

board = None
def initialize_board(dictionary, words=None):
    '''initialize_board Function definition. Creates an empty board with an empty list of words with the number of words defined by the NUM_GUESSES parameter'''
    global board
    if not words:
        board = Board([Word() for _ in range(NUM_GUESSES)], dictionary)
        board.print()

with open(DICTIONARY_FILE, 'r') as loadf:
    words = json.load(loadf)

initialize_board(words)

def parse_command(command):
    '''parse_command Function definition. This handles words that start with an exclamation point.'''
    command = command[1:]
    global board
    if command in ['quit', 'q']:
        exit()
    elif command in ['restart', 'r']:
        print(f"The word was: {board.solve_word}. Starting a new game.\n")
        initialize_board(words)
    elif command == 'dict':
        print(f"Dictionary Size: {len(words)}\n")

while board.guesses > 0:
    ip = input('>')
    # Parse words starting with ! as commands instead of words
    if ip.strip().lower()[0] == '!':
        parse_command(ip)
    else:
        board.get_guess(ip)
        board.print()
