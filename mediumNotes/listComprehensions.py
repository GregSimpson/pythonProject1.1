
# [ expression for item in list if conditional ]

mylist = [i for i in range(10)]
print(mylist)



squares = [x**2 for x in range(10)]
print(squares)


def some_function(a):
    return (a + 5) / 2


my_formula = [some_function(i) for i in range(10)]
print(my_formula)

filtered = [i for i in range(20) if i%2==0]
print(filtered)
