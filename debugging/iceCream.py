

num1 = 30
num2 = 40

print(num1)
print(num2)

#---------
# !pip install icecream

from icecream import ic

def plus_five(num):
    return num + 5

ic(plus_five(4))
ic(plus_five(5))

#-------------
def hello(user: bool):
 if user:
  print("I'm user")
 else:
  print("I'm not user")


hello(user=True)

#-----------
from icecream import ic

def hello(user:bool):
    if user:
        ic()
    else:
        ic()

hello(user=True)

#---------------------
from datetime import datetime
from icecream import ic
import time

def time_format():
    return f'{datetime.now()}|> '

ic.configureOutput(prefix=time_format)

for _ in range(3):
    time.sleep(1)
    ic('Hello')

#------------
from icecream import ic

def plus_five(num):
    return num + 5

ic.configureOutput(includeContext=True)
ic(plus_five(4))
ic(plus_five(5))

#-----------
from icecream import ic

def plus_five(num):
    return num + 5

ic(plus_five(4))
ic(plus_five(5))

for i in range(10):
    print(f'****** Training model {i} ******')

#------------



