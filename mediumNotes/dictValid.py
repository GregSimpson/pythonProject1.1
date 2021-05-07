
a = { 'sub_dict': { 'b': True }, 'mylist': [100, 200, 300] }
print ( a['sub_dict']['b'] )
# True
print (a['mylist'][0] )
# 100

# A dictionary requires a key and a value. Otherwise, it’s the same trick again:
print ( {x: x**2 for x in (2, 4, 6)} )

# { <expression> for item in list if <conditional> }
print ( {s for s in range(1,5) if s % 2} )
