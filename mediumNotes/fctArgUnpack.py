
# You can unpack a dictionary for use with named keywords by using the ** prefix:
def f(a, b):
    print(a, b)

args = { "a": 1, "b": 2 }
print ( f(**args) )
# 1 2


# similarly, we can use a single * to unpack an array and feed its content as positional arguments to a function:
def f(a, b, c):
    print(a, b, c)

l = [1, 2, 3]
print ( f(*l) )
# 1 2 3

