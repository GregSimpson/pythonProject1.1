# https://betterprogramming.pub/an-alternative-to-python-dictionaries-5d54aa4c5a6

number_list = [7,2,2,4,2,5,7,10,2,9,2,8,5,3,4,2,4,2,4,8,2,1,2,5,6,7,9,4,1,8]

dict_ = {}

for number in number_list:
    if number not in dict_:
        dict_[number] = 0
    dict_[number] += 1
print(dict_)

# mydict = {}
# mydict[1]

#---------
from collections import defaultdict

def default_value():
    return "Not Present Yet"
mydict1 = defaultdict(default_value)

mydict = defaultdict(lambda: "Not Present Yet" )

mydict["cat"] = 2
mydict["dog"] = 4

print(mydict["cat"])
print(mydict["dog"])

print(mydict["pig"])
print(mydict["rabbit"])
print(mydict)

#-------------
dict2 = defaultdict(lambda: 0)

for number in number_list:
    dict2[number] += 1
print("dict2")
print(dict2)

