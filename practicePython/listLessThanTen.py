#!/usr/bin/env python3

# https://www.practicepython.org/
'''
Take a list, say for example this one:

  a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
and write a program that prints out all the elements of the list that are less than 5.

Extras:
Instead of printing the elements one by one, make a new list that has all
the elements less than 5 from this list in it and print out this new list.
Write this in one line of Python.

Ask the user for a number and return a list that contains only elements
from the original list a that are smaller than that number given by the user.
'''

#num  = int(input("Give me a number to check  : "))
##print("{0} is an {1} number".format(num, ("Odd" if num % 2 else "Even")))
#print("{0} is an {1} number".format(num, ("4" if num == 4 else "odd" if num % 2 else "Even")))

x = [i for i in range(10)]
print (x)

num = 4
print ([x for x in range(10) if x > num])
print ([x+y for x in [10,30,50] for y in [20,40,60]])

import random
randomlist = random.sample(range(1, 100), 35)
print(randomlist)

list2 = [x for x in randomlist if x < 5]
print (list2)

entries = int(input("\n\nHow many elements       : "))
splits  = int(input("What is the split point : "))
randomlist = random.sample(range(1, entries), entries-1)
print(randomlist)

print("elements  > {0} : {1} ".format(splits, [x for x in randomlist if x >  splits]))
print("elements <= {0} : {1} ".format(splits, [x for x in randomlist if x <= splits]))
#print ([x for x in randomlist if x > splits])
#print ([x for x in randomlist if x <= splits])


