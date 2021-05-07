
'''
brain teaser: calculate a letter grade given a decimal value between 0.0 .. 1.0 without using any if statements.
Grades should correspond to this scale:
A: 0.9 <= x <= 1.0
B: 0.8 <= x < 0.9
C: 0.7 <= x < 0.8
D: 0.6 <= x < 0.7
F: otherwise

Bonus:
See if you can get away with not using any comparison operators either!

#print("\tgrades1\t{:.{}f}\t-\tletter : {}".format(grade,2, scale.get(max(round(grade, 1), 0.5), "A")))
'''
import frange as frange


def printme():
    numeric_list = ([round(x * 0.01, 3) for x in range(50, 100)])

    print (numeric_list)

    #graded1 = map(grades1, numeric_list)
    #list (graded1)

    print(list(map(grades1, numeric_list)))
    print( "\n\n" )
    print(list(map(grades2, numeric_list)))
    print("\n\n")
    print(list(map(grades3, numeric_list)))
    print("\n\n")
    #print(list(map(grades4(scale), numeric_list)))


def grades1(grade=0.80):

    scale={0.9:"A",0.8:"B",0.7:"C", 0.6:"D",0.5:"F"}
    print ("grade1\t:\t{}\t--\tletter\t{}".format (grade, scale.get(max(round(grade,1), 0.5), "A") ))
    return scale.get(max(round(grade,1), 0.5), "A")


def grades3(grade=0.80):
    scale={0.9:"A",0.8:"B",0.7:"C", 0.6:"D",0.5:"F"}
    print("grade3\t:\t{}\t--\tletter\t{}".format(grade, scale.get(max(round(grade,1), 0.5), 0.9)))
    return scale.get(max(round(grade,1), 0.5), 0.9)


def grades2(grade=0.80):
    scale={0.9:"A",0.8:"B",0.7:"C", 0.6:"D",0.5:"F"}
    print("grade2\t:\t{}\t--\tletter\t{}".format(grade, scale[min(max(round(grade,1), 0.5), 0.9)]))
    return scale[min(max(round(grade,1), 0.5), 0.9)]


import math
def grades4(grade):
    print("grade4\t:\t{}\t--\tletter\t{}".format(grade, min('F', chr(math.ceil(74-10*grade)))))
    return min('F', chr(math.ceil(74-10*grade)))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #scale = {0.9: "A", 0.8: "B", 0.7: "C", 0.6: "D", 0.5: "F"}

    #print(grades4(scale, 0.3))
    printme()





