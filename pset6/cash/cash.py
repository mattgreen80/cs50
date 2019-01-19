#cash program ported to python 3#
#################################
import cs50

# use mod to get remainder and only divide by that, adding to coin count on the way.
def greedy(change):
    coins = change // 25
    remain = change % 25
    coins += remain // 10
    remain = remain % 10
    coins += remain // 5
    remain = remain % 5
    coins += remain
    return coins

while True:
    # prompt for input and then convert string to int, if not in the range then prompt again
    fchg = cs50.get_float("Change owed: ")
    if fchg > 0:
        break
    print("Please enter a positive number")

# take float input and convert to integer (cents)
ichg = round(fchg * 100)
print(greedy(ichg))

 