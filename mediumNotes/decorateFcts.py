

def print_argument(func):
    def wrapper(the_number):
        print("Argument for",
              func.__name__,
              "is", the_number)
        return func(the_number)
    return wrapper

@print_argument
def add_one(x):
    return x + 1
print(add_one(1))


##  gjs stuff

def wrap_2(func):
    def wrapper2(the_number):
        print("2: Argument for",
              func.__name__,
              "is", the_number)
        return func(the_number)
    return wrapper2

@wrap_2
def wrap_1(func):
    def wrapper(the_number):
        print("1: Argument for",
              func.__name__,
              "is", the_number)
        return func(the_number)
    return wrapper

@wrap_1
def gjs_add_one(x):
    return x + 1
print(gjs_add_one(5))



