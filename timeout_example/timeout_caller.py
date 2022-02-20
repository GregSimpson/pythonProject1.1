import time
import errno
import os
import signal
import functools

from timeout import timeout

## Timeout a long running function with the default expiry of 10 seconds.
#@timeout
#def long_running_function1():
#    ...

## Timeout after 5 seconds
#@timeout(5)
#def long_running_function2():
#    ...

# Timeout after 30 seconds, with the error "Connection timed out"
#@timeout(30, os.strerror(errno.ETIMEDOUT))
#def long_running_function3():
@timeout(6)
def long_time_function():
	time.sleep(4)  # Works
	print("long_time_function1 returing")

@timeout(4)
def long_time_function2():
	time.sleep(5)  # Doesn't work
	print("long_time_function2 returing")

@timeout(7, os.strerror(errno.ETIMEDOUT))
def long_time_function3():
	time.sleep(10)  # Doesn't work
	print("long_time_function3 returing")


if __name__ == '__main__':
	long_time_function()
	long_time_function2()
	long_time_function3()
