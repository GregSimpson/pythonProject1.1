# https://betterprogramming.pub/9-handy-python-functions-for-programmers-cc391a59acc7

a = ("John", "Charles", "Mike")
b = ("Jenny", "Christy", "Monica")
x = zip(a, b)
print(tuple(x))

(('John', 'Jenny'), ('Charles', 'Christy'), ('Mike', 'Monica'))
a = ["John", "Charles", "Mike"]
b = ["Jenny", "Christy", "Monica"]
for i,j in zip(a,b):
    print(f"{i} will marry {j}")
