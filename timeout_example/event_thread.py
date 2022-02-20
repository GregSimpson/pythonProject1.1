from threading import Thread, Event
import time
# https://www.codespeedy.com/timeout-a-function-in-python/

# It sends signals from one to another thread
bridge = Event()


def func():
	print('func() is started')
	"""
	func will timeout after 3 seconds it will print a number starting from 1 and wait for 1 second 
	"""
	x = 0
	while True:
		x += 1
		print(x)
		time.sleep(1)

		# Ensures whether the other thread sends the signals or not
		if bridge.is_set():
			break


import time
import errno
import os
import signal
import functools

from timeout import timeout

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


# https://dreamix.eu/blog/webothers/timeout-function-in-python-3

from threading import Thread, Event
import time

# Event object used to send signals from one thread to another
stop_event = Event()


def my_actions():
	"""
	Function that should timeout after 5 seconds. It simply prints a number and waits 1 second.
	:return:
	"""
	i = 0
	while True:
		i += 1
		print(i)
		##time.sleep(1)
		#sometimes_hangs()
		# We create another Thread
		my_thread2 = Thread(target=sometimes_hangs)

		# Here we start the thread and we wait 5 seconds before the code continues to execute.
		my_thread2.start()
		my_thread2.join(timeout=5)

		# We send a signal that the other thread should stop.
		#stop_event.set()

		# Here we make the check if the other thread sent a signal to stop execution.
		if stop_event.is_set():
			break


	print("MY_ACTIONS do things after me!")


def outer_method():
	"""
	Function that should timeout after 5 seconds. It simply prints a number and waits 1 second.
	:return:
	"""
	try:
		i = 0
		while i < 12 :
			i += 1
			print(i)
			#time.sleep(1)
			sometimes_hangs()

			## Here we make the check if the other thread sent a signal to stop execution.
			#if stop_event.is_set():
			#	#break
			#	print("\tstop_event.is_set() triggered :  i = {}".format(i))
			#	continue

	except Exception as error:
		print("\t\touter method exception  {}".format(error))
		#logging.error(data)
		#return '{}'



def sometimes_hangs():
	# import random
	import random

	# prints a random value from the list
	list1 = [1, 2, 3, 4, 5, 6]
	list2 = range(1, 10)
	sleep_number = random.choice(list2)
	print("\tsometimes_hangs sleeping for {}".format(sleep_number))
	time.sleep(sleep_number)



if __name__ == '__main__':
	# We create another Thread
	action_thread = Thread(target=outer_method)

	# Here we start the thread and we wait 5 seconds before the code continues to execute.
	action_thread.start()
	action_thread.join(timeout=5)

	# We send a signal that the other thread should stop.
	stop_event.set()

	print("Hey there! I timed out! You can do things after me!")

##if __name__ == '__main__':
#	# Creating the main thread that executes the function
#	main_thread = Thread(target=func)

#	# We start the thread and will wait for 3 seconds then the code will continue to execute
#	main_thread.start()
#	main_thread.join(timeout=3)

#	# sends the signal to stop other thread
#	bridge.set()

	print("The function is timed out, you can continue performing your other task")


#	long_time_function()
#	long_time_function2()
#	long_time_function3()
