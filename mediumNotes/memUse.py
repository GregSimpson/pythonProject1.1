import sys

mylist = range(0, 10000)
print(sys.getsizeof(mylist))
# 48

myreallist = [x for x in range(0, 10000)]
print(sys.getsizeof(myreallist))
# 87632
