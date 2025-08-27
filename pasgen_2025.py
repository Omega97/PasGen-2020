""" 27/08/2025
                        PasGen 2025

- Generate password given "lock sequence" (name of the file) and key text
- compile with Python, not PyCharm
- print master password, then "string" or "string" + " " + "length"
- example: "Google", "Google 30"

"""
import random
import os
from typing import Tuple


class Alpha:
    """ List of chars that can be used in a password (similar characters are excluded)"""
    upper_case = 'ACDEFGHJKLMNPRSTWXYZ'  # 20 capital letters
    lower_case = 'abcdefghkmnpqrstwxyz'  # 20 lower-case letters
    chars = '!@#$%&*+.-?='  # 12 symbols
    numbers = '23456789'  # 8 digits
    categories = (upper_case, lower_case, chars, numbers)

    @staticmethod
    def get_char(category: int) -> str:
        return Alpha.categories[category % len(Alpha.categories)]

    @staticmethod
    def get_random_char(category: int, rng=random) -> str:
        """ random char from a category using provided random generator """
        return rng.choice(Alpha.categories[category])

    @staticmethod
    def generate_string(length=20, rng=random) -> str:
        """ generate string of random char using alphabet and given random generator """
        types = [i % len(Alpha.categories) for i in range(length)]
        chars = [Alpha.get_random_char(i, rng) for i in types]
        rng.shuffle(chars)
        return ''.join(chars)


def split_key_and_length(s: str, default=20) -> Tuple[str, int]:
    """ Extract the number at the end of a string (after a space): 'key_name 24' -> ('key_name', 24) """
    key = s.lower()
    length = default
    v = key.split(" ")
    
    if len(v) > 1:
        key, length = key.rsplit()
        try:
            length = int(v[-1])
        except ValueError:
            key = "".join(v)
    else:
        key = "".join(v)
    
    return key, length


def get_file_name() -> str:
    return os.path.basename(__file__)


def main():
    master_key = get_file_name().lower()
    print(f"\033[93mMaster key = {master_key}\033[0m")

    while True:
        # Read the key
        key_input = input(f"\033[94m\n Input key: \033[0m").strip()
        if not key_input:
            break
        
        key, length = split_key_and_length(key_input)
        
        # Generate the password using a seeded random generator
        rng = random.Random(master_key + key)
        password = Alpha.generate_string(length, rng)
        print()
        print(password)


if __name__ == "__main__":
    main()
