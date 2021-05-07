
def f(*, a, b):
    print(a, b)

#  f(1, 2)  - this fails

print ( f(a=1, b=2) )
