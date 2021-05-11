
# snoop — Print the Lines of Code being Executed in a Function
# What if there is no error in the code, but we want to figure out what is going on in the code? That is when snoop comes in handy.
# snoop is a Python package that prints the lines of code being executed along with the values of each variable by adding only one decorator.

import snoop

@snoop
def factorial(x: int):
    if x == 1:
        return 1
    else:
        return (x * factorial(x - 1))


if __name__ == "__main__":
    num = 5
    print(f"The factorial of {num} is {factorial(num)}")

