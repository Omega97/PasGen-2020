""" 27/7/2019
                        PasGen 2020

- Generate password given "lock sequence" and key text
- compile with Python, not PyCharm
- print master password, then "string" or "string" + " " + "length"

!note: works only in an external console
"""
from random import randrange, seed, shuffle
import msvcrt
import sys


def alpha():
    """ list of chars that can be used in a password"""
    numbers = ''.join([chr(i) for i in range(48, 58)])
    upper_case = ''.join([chr(i) for i in range(65, 91)])
    lower_case = ''.join([chr(i) for i in range(97, 123)])
    chars = '!"#$%&' + "'" + '()*+,-./:;<=>?@[' + '\\' + ']^_`{|}~'
    return [numbers, upper_case, lower_case, chars]


def keyboard_input():
    """ input from keyboard (without print, works only in an external console) """
    out = []
    while True:
        try:
            key = msvcrt.getch()
        except UnicodeDecodeError:
            key = b' '
        if key == b'\r':     # Enter end the input
            break
        elif key == b'\x08':     # Backspace deletes the last char
            if len(out) > 0:
                out = out[:-1]
        else:
            out += [key]
    out = ''.join([str(i) for i in out])
    return out if len(out) else keyboard_input()


def random_char(num=None):
    """ random char from alphabet """
    num = randrange(0, 4) if num is None else num   # pick a random category
    return alpha()[num][randrange(len(alpha()[num]))]


def gen(length=20):
    """ generate string of random char using alphabet """
    types = [1, 2, 0, 3] + [randrange(len(alpha())) for _ in range(length - 4)]    # default: Aa0$****************
    chars = [random_char(i) for i in types]
    shuffle(chars)
    return ''.join(chars)


def get_length(v, default=20):
    """ extract the number at the end of a list of bytes (aster a space) : 'name 22' -> 22 """
    s = ''.join([str(i) for i in v])
    s = s.replace("b'", "")
    s = s.replace("'", "")
    try:
        s = s.split()[-1]
    except IndexError:
        return default
    try:
        return int(s)
    except ValueError:
        return default


if __name__ == "__main__":

    NICKNAME = keyboard_input()
    seed(NICKNAME)

    # user's hash (user can check that the username is correct)
    print('['
          + ''.join([random_char(0) for _ in range(2)]) + '-'
          + ''.join([random_char(2) for _ in range(3)]) + '-'
          + ''.join([random_char(0) for _ in range(2)]) + ']\n')

    # input keywords and return passwords indefinitely
    while True:
        KEY = keyboard_input()
        seed(NICKNAME + KEY)
        print(gen(length=get_length(KEY)))
