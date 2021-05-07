#!/usr/bin/env python3

# https://www.practicepython.org/exercise/2014/01/29/01-character-input.html
'''
Create a program that asks the user to enter their name and their age.
Print out a message addressed to them that tells them the year that they will turn 100 years old.

Extras:

Add on to the previous program by asking the user for another number and printing out
that many copies of the previous message. (Hint: order of operations exists in Python)
Print out that many copies of the previous message on separate lines.
(Hint: the string "\n is the same as pressing the ENTER button)
'''

print('%d %s cost $%.2f' % (6, 'bananas', 1.74))
print('{0} {1} cost ${2}'.format(6, 'bananas', 1.74))

name = input("\n\nGive me your name: ")
age  = int(input("Give me your age : "))
num  = int(input("How many copies  : "))

print(num * ("\nYour name is " + name))
print(num * ("\nYour age  is %d" % ( age )))
print(num * ("\nYou will be 100 y/o in {0} years".format(100 - age)))

for x in range (num):
    print(("\n" + str(x+1) + "\tYour name is " + name))
    print(("%d\tYour age  is %d" % (x+1, age)))
    print("{1}\tYou will be 100 y/o in {0} years".format( (100 - age), x+1) )

