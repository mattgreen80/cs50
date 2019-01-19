#caesar.c ported to python 3#
#############################

import sys
import cs50


def main(argv):
    # get key as second argument and convert to int
    if len(sys.argv) != 2:
        print("caesar.py <key>")
        sys.exit(1)

    key = int(sys.argv[1])

    # prompt until user gives a string
    while True:
        plntxt = cs50.get_string("plaintext: ")
        if plntxt != None:
            break
        print("Plaintext only")

    # for each char in plaintext, determine type, convert to number and calculate,
    # then convert back to char and print
    print("ciphertext: ", end='')
    result = []
    for c in plntxt:
        if c.isalpha and c.isupper():
            result = (ord(c) - 65 + key) % 26 + 65
        elif c.isalpha and c.islower():
            result = (ord(c) - 97 + key) % 26 + 97
        else:
            result = ord(c)
        print(chr(result), end='')
    print()


if __name__ == "__main__":
    main(sys.argv)