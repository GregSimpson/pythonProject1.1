

# Partial functions are functions that utilize existing functions by applying partial arguments.
# This definition doesn’t sound very straightforward. It’s better understood with a simple example:

# Create a function that accepts two arguments
def greeting(word, person):
    print(f"{word}, {person}!")
    ...
greeting("Hi", "John")


greeting("Hi", "Danny")

# Create a partial function
from functools import partial
say_hi = partial(greeting, "Hi")
say_hi("John")

say_hi("Danny")


