# https://www.geeksforgeeks.org/synchronization-by-using-semaphore-in-python/

# importing the modules
from random import randint
from threading import *
import time
from time import sleep

# creating thread instance where count = 3
# In this case, a Semaphore object can be accessed by n Threads at a time.
# The remaining Threads have to wait until releasing the semaphore.
obj = Semaphore(5)

# creating instance
def display(x,name):

    ## calling acquire method
    #obj.acquire()
    for y in range(1):
        #print(f'\t\t{x} - {y}\tHello, {name}\n', end = '')
        ##print(f'\t\t{x} - {y}\tHello, {name}\n', end = f'gjs {x}\n')
        time.sleep(randint(1,3))
        print(f'\t\tEnding display {name} - {x} : {y}')

        # calling release method
        #obj.release()


def thread_process(name):
    # calling acquire method
    obj.acquire()
    for x in range (200):
        #print(f'{x} : {name}\n')

        sleep_num = randint(1,5)
        ##print(f'{x} : thread_process file {name} - sleeping {sleep_num}\n')
        display(x,name)
        sleep(sleep_num)
        ##print(f'\tEnding thread_process {name} - {x}')

        # calling release method
        obj.release()
    print(f'\t\t\tEXITING thread_process {name} - {x}\n')



# creating multiple thread
t1 = Thread(target = thread_process , args = ('Thread-1',))
t2 = Thread(target = thread_process , args = ('Thread-2',))
t3 = Thread(target = thread_process , args = ('Thread-3',))
t4 = Thread(target = thread_process , args = ('Thread-4',))
t5 = Thread(target = thread_process , args = ('Thread-5',))

# calling the threads
t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
