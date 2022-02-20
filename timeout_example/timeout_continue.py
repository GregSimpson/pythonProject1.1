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


def do_actions():
	"""
	Function that should timeout after 5 seconds. It simply prints a number and waits 1 second.
	:return:
	"""
	i = 0
	while True:
		i += 1
		print(i)
		#time.sleep(1)
		sometimes_hangs()

		# Here we make the check if the other thread sent a signal to stop execution.
		if stop_event.is_set():
			break


def sometimes_hangs():
	# import random
	import random

	# prints a random value from the list
	list1 = [1, 2, 3, 4, 5, 6]
	list2 = range(1, 10)
	sleep_number = random.choice(list2)
	print("sometimes_hangs sleeping for %s".format(sleep_number))
	time.sleep(sleep_number)



if __name__ == '__main__':
	# We create another Thread
	action_thread = Thread(target=do_actions)

	# Here we start the thread and we wait 5 seconds before the code continues to execute.
	action_thread.start()
	action_thread.join(timeout=5)

	# We send a signal that the other thread should stop.
	stop_event.set()

	print("Hey there! I timed out! You can do things after me!")
