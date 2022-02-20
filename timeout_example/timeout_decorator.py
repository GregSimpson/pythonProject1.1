from functools import wraps
import errno
import os
import signal
import time

#Source: http://stackoverflow.com/questions/2281850/timeout-function-if-it-takes-too-long-to-finish
# https://gist.github.com/plutec/2fc31233612528f9181a

class TimeoutError(Exception):
    pass

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator

@timeout(6)
def long_time_function():
    time.sleep(4) #Works

@timeout(4)
def long_time_function2():
    time.sleep(5) #Doesn't work

if __name__ == '__main__':
    long_time_function()
    long_time_function2()
