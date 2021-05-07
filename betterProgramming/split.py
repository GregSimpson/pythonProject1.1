
'''
This function is mostly used while taking the user input using the input() function. It takes the object as a string and splits the object based on anything.
If you want to split a string with the keyword “f,” you can pass this inside the split(“f”) function.

'''

txt = "welcome to the medium"
x = txt.split()
print(x)

txt = "2 6 9 5 8 14 25 -15"
x = [int(i)*10 for i in txt.split()]
print(x)
