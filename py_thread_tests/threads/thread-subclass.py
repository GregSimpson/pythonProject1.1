# https://www.bogotobogo.com/python/Multithread/python_multithreading_Thread_Local_Specific_Data.php

import threading
import logging
import random

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',)

def show(d):
    try:
        val = d.val
    except AttributeError:
        logging.debug('No value yet')
    else:
        logging.debug('value=%s', val)

def f(d):
    show(d)
    d.value = random.randint(1, 100)
    logging.debug('val of d.value: %r', d.value)
    show(d)

class MyLocal(threading.local):
    def __init__(self, v):
        logging.debug('Initializing %r', self)
        logging.debug('val of v: %r', v)
        self.val = v

if __name__ == '__main__':
    d = MyLocal(999)
    show(d)

    for i in range(2):
        t = threading.Thread(target=f, args=(d,))
        t.start()
