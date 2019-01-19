# natural language tool kit (nltk.org)
from nltk.tokenize import sent_tokenize

# a function that splits a string up into all possible strings of length num
def strenu(str,num):
    lst = []
    for i in range(len(str)):
        # if the length of the string is greater than or equal to the current position (given as 
        # the current place in the string plus the specified length (num)) then append to a list
        # a sliced portion of the string of the specified length (num). 
        if len(str)+1 >= i+num+1:
            lst.append(str[i:i+num])
    return (lst)


def lines(a, b):
    """Return lines in both a and b"""

    # split strings by line delimiter and store in lists
    l1 = a.split('\n')
    l2 = b.split('\n')

    # create a sets from lists (this will remove duplicates)
    s1 = set(l1)
    s2 = set(l2)
    
    # create a list putting logic in brackets. called a "list comprehension"
    l3 = [x for x in s1 for y in s2 if x == y]
    
    return l3


def sentences(a, b):
    """Return sentences in both a and b"""

    # split strings by sentence using the nltk.tokensize package (natural language toolkit)
    l1 = sent_tokenize(a)
    l2 = sent_tokenize(b)

    # create a sets from lists (this will remove duplicates)
    s1 = set(l1)
    s2 = set(l2)
    
    # create a list putting logic in brackets. called a "list comprehension"
    l3 = [x for x in s1 for y in s2 if x == y]
    
    return l3


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    
    # call strenu function defined above to create substring list
    l1 = strenu(a,n)
    l2 = strenu(b,n)
    # put list of substrings into a set to remove duplicates
    s1 = set(l1)
    s2 = set(l2)
    # compare substrings and create list containing the identical substrings from a and b
    l3 = [x for x in s1 for y in s2 if x == y]
    return l3

# Use below if you do not want to implement a function
#    lst = []
#    for i in range(len(a)):
#        # to stop it going beyond length of string
#        if len(a)+1 >= i+n+1:
            # append each string slice to the list
#            lst.append(a[i:i+n])