#!/usr/bin/env python3

# https://www.practicepython.org/
'''
Create a program that asks the user for a number and then prints out a list of all the
divisors of that number. (If you don’t know what a divisor is, it is a number that divides
evenly into another number. For example, 13 is a divisor of 26 because 26 / 13 has no remainder.)
'''


target = int(input("\n\nTarget number : "))
candidate_list = [i for i in range(1,round(((target + .5) / 2) + 1 ))]
candidate_list.append(target)
print("2 steps range append target : {0} ".format(candidate_list))

import itertools
candidate_list2 = ([i for i in itertools.chain(range(1,round(((target + .5) / 2) + 1 )), [target] ) ] )
print("1 step range chain target   : {0} ".format(candidate_list2))

print("candidate divisors for : {0} : {1} ".format(target, candidate_list))
print("\t\tall  mod remainders : {0}".format([target % item for item in candidate_list] ))
print("\t\tzero mod remainders : {0}".format([target % item == 0 for item in candidate_list]  ))
print("\t\tdivisors compression: {0}".format( [n  for n in candidate_list if target % n  == 0] ) )

divisorList = []
for number in candidate_list:
    if target % number == 0:
        divisorList.append(number)
print("\t\tdivisors for loop   : {0}".format( divisorList ))


