""" This module defines methods to play a simple game of Hangman. """

__author__ = 'Anand'

import random
import os


def readfile(filename) -> list:
    """ Reads a dictionary file and returns a list of words.

    :rtype : list
    :param filename: the file that is read.
    """
    with open(filename) as file:
        lst = file.readlines()
    lst = [x.strip('\n') for x in lst]
    return lst


def generator(word_list) -> str:
    """ Generates word to be used in hangman.

    :type word_list: list
    :param word_list: the dictionary of words to be used.
    :rtype : str
    :return : a mystery word.
    """
    word = random.choice(word_list)
    while illegal(word):
        word = random.choice(word_list)
    return word


def illegal(word) -> bool:
    """ This method checks if the parameter word contains non-alphabetical characters.

    :rtype : bool
    :param word: this word is checked for non-alphabetical characters.
    :return: True if the word contains non-alphabetical characters, which in this case is only the
    '\'' character, and False otherwise.
    """
    if word.__contains__('\''):
        return True
    else:
        return False


def guess(char, char_list, word) -> list:
    """ This method guesses a user-specified character and updates the list containing known and
    unknown characters of the mystery word.

    :rtype : list
    :param char: the character guess.
    :param char_list: the list containing known and unknown characters of the mystery word in the
    current game state.
    :param word: the mystery word.
    :return: a list containing known and unknown characters of the mystery word in the current game
    state.
    """
    for i in range(0, len(word)):
        if char_list[i] == '_':
            if word[i] == char:
                char_list[i] = char
    return char_list


def won(char_list) -> bool:
    """ This method checks if the game has been won by checking if there are any unknown characters
    left.

    :rtype : bool
    :param char_list: the list containing known and unknown characters of the mystery word in the
    current game state.
    :return: True if the game has been won, and False otherwise.
    """
    if char_list.__contains__('_'):
        return False
    else:
        return True


def char_string(char_list) -> str:
    """ This method returns a string representing the known and unknown characters in the current
    game state.

    :rtype : str
    :param char_list: the list containing known and unknown characters of the mystery word in the
    current game state.
    :return: a string representing the known and unknown characters in the current game state.
    """
    string = ''
    for char in char_list:
        string += char + ' '
    return string


def gallows(bad_guesses) -> None:
    """ This method prints to the console an illustration of the gallows in the current game state.

    :rtype : None
    :param bad_guesses: the number of bad guesses in the current game state.
    """
    with open('gallows/state{0}.txt'.format(str(bad_guesses))) as file:
        print(file.read())


def play() -> str:
    """ This method simply employs the previously defined methods to play a game of Hangman. A word
    is first randomly selected from the provided word list, after which it is hidden from the
    player and illustrated as a string of '_', above which is an illustration of the gallows in the
    ground state. The game starts with the player making a guess, which results in the following
    outcomes:

    I. The player makes a correct guess:
        - The string of '_' representing the unknown characters is updated to reflect known
        characters. For example, if our word is given as _ _ _ _ , and a guess of 'a' correctly
        identifies the second character of the mystery word, then the unknown characters are
        updated to _ a _ _ . The guess is appended to a list containing unique previous guesses to
        prevent the player from making the same guess later on in the game. If the player makes a
        guess that pushes the game into a solved state, the player is congratulated, and the game
        ends. The illustration of the gallows remains the same.

    II. The player makes an incorrect guess:
        - The guess is appended to a list containing unique previous guesses, as discussed in (I),
        and the gallows is incremented to the next state. If the player makes a guess that pushes
        the game into the final state, the illustration of the gallows is incremented to the final
        state, and the player is informed that he has lost, and the game subsequently ends.

    III. The player repeats a previous guess:
        - The player is informed that he has already made the guess, and is then prompted to make
        another valid guess.

    :rtype : str
    :return: returns 'CONGRATS! YOU WIN!' if the game is won, and 'GAME OVER! YOU LOST!' if the
    game is lost.
    """
    # Generating word and hidden string of '_' . #
    word = generator(DICTIONARY)
    hidden_word = list('_' * len(word))

    # The list and integer representing unique character guesses and the number of bad guesses #
    # respectively. #
    guessed_chars = []
    bad_guesses = 0

    # The ground state of the game is illustrated first. #
    gallows(0)
    print('\n' + char_string(hidden_word) + '\n')
    print('Guessed letters: ')

    while not won(hidden_word):
        char_guess = input('Enter a guess: ').lower()

        # Checking outcome (III) #
        if guessed_chars.__contains__(char_guess):
            print('You already guessed that.\n')
        elif len(char_guess) > 1 or not 97 <= ord(char_guess) <= 122:
            print('Illegal character. Please choose an alphabet character.')

        # Checking outcome (I) or (II) #
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            guessed_chars.append(char_guess)

            # Checking outcome (II) #
            if not word.__contains__(char_guess):
                bad_guesses += 1

                # Final state #
                if bad_guesses == 8:
                    gallows(bad_guesses)
                    return '\nGame over. You lost.\nThe word was: ' + word

                gallows(bad_guesses)
                print('\n' + char_string(hidden_word) + '\n')
                print('Guessed letters: ' + char_string(guessed_chars))

            # Checking outcome (I) #
            else:
                gallows(bad_guesses)
                print('\n' + char_string(guess(char_guess, hidden_word, word)) + '\n')
                print('Guessed letters: ' + char_string(guessed_chars))

    # The while loop is active only when the game is not won, thus a win naturally results when #
    # we exit this loop. #
    return '\nCongrats. You\'ve won.'

# Game is initiated #
DICTIONARY = readfile('words.txt')

os.system('cls' if os.name == 'nt' else 'clear')
print(play())

while 'y' == input('\nDo you want to play again? (y / n)\n'):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(play())

print('\nThanks for playing!\n')
