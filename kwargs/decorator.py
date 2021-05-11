
 # In the previous section, we discussed closures. We should understand that closures
 # are just a general technical implementation approach that can be used for different
 # purposes. One particular purpose is to create decorators in Python. As indicated by
 # their name, decorators are higher-order functions that apply additional functionalities
 # (i.e. decorations) without changing the original functions’ intended jobs. Let’s see the
 # following code snippet before we explain what they are:

import time
def logging_time(func):
    """Decorator that logs time"""
    def logger():
        """Function that logs time"""
        start = time.time()
        func()
        print(f"Calling {func.__name__}: {time.time() - start:.5f}")

    return logger

@logging_time
def calculate_sum():
    return sum(range(10000))

calculate_sum()


