import time
from timeout_gjs import timeout

def outer_method():
	"""
	Function that should timeout after 5 seconds. It simply prints a number and waits 1 second.
	:return:
	"""
	try:
		i = 0
		while i < 10 :
			i += 1
			print(i)
			#time.sleep(1)
			sometimes_hangs()

	except Exception as error:
		print("\t\touter method Exception  {}".format(error))
	except TimeoutError as error:
		print("\t\touter method TimeoutError  {}".format(error))
		#logging.error(data)
		#return '{}'


@timeout(5)
def sometimes_hangs():
	# import random
	import random

	try:
		# prints a random value from the list
		list1 = [1, 2, 3, 4, 5, 6]
		list2 = range(1, 10)
		sleep_number = random.choice(list2)
		print("\tsometimes_hangs sleeping for {}".format(sleep_number))
		time.sleep(sleep_number)

	except Exception as error:
		print("\t\t\tsometimes_hangs method Exception  {}".format(error))
	except TimeoutError as error:
		print("\t\t\tsometimes_hangs method TimeoutError  {}".format(error))


def after_timeoout():
	# import random
	import random

	# prints a random value from the list
	list1 = [1, 2, 3, 4, 5, 6]
	list2 = range(1, 10)
	sleep_number = random.choice(list2)
	print("\tsometimes_hangs sleeping for {}".format(sleep_number))
	time.sleep(sleep_number)

if __name__ == '__main__':

    outer_method()
    after_timeoout()



