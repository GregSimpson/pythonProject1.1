
# https://github.community/t/how-to-timeout-kill-and-retry-a-python-function-using-threading-windows/221048/2

from multiprocessing import Process
from time import sleep


def keep_sleeping():
    while True:
        sleep(1)
        print('still sleeping')


if __name__ == '__main__':
    p = Process(target=keep_sleeping)
    p.start()
    sleep(30)
    print('terminating process')
    p.terminate()
    p.join()

