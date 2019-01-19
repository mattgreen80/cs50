# Mario program ported to python #
##################################

import cs50

while True:
    # prompt for input and then convert string to int, if not in the range then prompt again
    height = cs50.get_int("height: ")
    if height < 24 and height >= 0:
        break
    print("Please enter a number between 0 and 23")

# iterate until x is equal to height. because x steps one value until it reaches height
# it can be used to represent rows.
for x in range(height):
    print(" "*(height-(x+1)) + "#"*(x+1) + "  " + "#"*(x+1))






