#!/usr/bin/env python3

# https://www.practicepython.org/
'''
Ask the user for a number. Depending on whether the number is even or odd,
print out an appropriate message to the user.
Hint: how does an even / odd number react differently when divided by 2?

Extras:

If the number is a multiple of 4, print out a different message.
Ask the user for two numbers: one number to check (call it num)
and one number to divide by (check).

If check divides evenly into num, tell that to the user.
If not, print a different appropriate message.
'''

num  = int(input("Give me a number to check  : "))

#print("{0} is an {1} number".format(num, ("Odd" if num % 2 else "Even")))
print("{0} is an {1} number".format(num, ("4" if num == 4 else "odd" if num % 2 else "Even")))

age = 14
print(('true', 'false')[age < 20])
age = 214
print(('true', 'false')[age < 20])

x=3
print (100 if x > 42 else 42 if x == 42 else 0 )
x=42
print (100 if x > 42 else 42 if x == 42 else 0 )
x=45
print (100 if x > 42 else 42 if x == 42 else 0 )

x=3
print("no") if x > 42 else print("yes") if x == 42 else print("maybe")
x=42
print("no") if x > 42 else print("yes") if x == 42 else print("maybe")
x=45
print("no") if x > 42 else print("yes") if x == 42 else print("maybe")



#b = int(input("Enter value for b: "))
#print( "neg" if b < 0 else "pos" if b > 0 else "zero")

numerator = int(input(  "enter Numerator  : "))
denominator = int(input("enter Denominator: "))

#print("{0} is an {1} number".format(num, ("Odd" if num % 2 else "Even")))
#print("{0} is an {1} number".format(num, ("4" if num == 4 else "odd" if num % 2 else "Even")))
#result = (numerator / denominator)
print("{0}   {1} divide evenly into {2}".format(denominator, "does NOT" if (numerator / denominator) % 1 else "does", numerator))

