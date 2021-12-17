# https://hackernoon.com/threaded-asynchronous-magic-and-how-to-wield-it-bba9ed602c32

from threading import Thread
import asyncio
import time


async def do_some_work(x):
    print("Waiting " + str(x))
    await asyncio.sleep(x)

def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

def more_work(x):
  print("More work %s" % x)
  time.sleep(x)
  print("Finished more work %s" % x)


'''
def send_notification(email):
    """Generate and send the notification email"""

loop = asyncio.get_event_loop()
loop.run_until_complete(do_some_work(5))
#---------
tasks = [asyncio.ensure_future(do_some_work(2)),
         asyncio.ensure_future(do_some_work(5))]
# asyncio.gather() function enables results aggregation. It waits for several tasks in the same thread to complete and puts the results in a list.
loop.run_until_complete(asyncio.gather(*tasks))
'''

'''
# What if instead of doing everything in the current thread, we spawn a separate Thread to do the work for us.
Notice that this time we created a new event loop through asyncio.new_event_loop(). The idea is to spawn a new thread, pass it that new loop and then call thread-safe functions (discussed later) to schedule work.

The advantage of this method is that work executed by the other event loop will not block execution in the current thread. Thereby allowing the main thread to manage the work, and enabling a new category of execution mechanisms.
'''
new_loop = asyncio.new_event_loop()
t = Thread(target=start_loop, args=(new_loop,))
t.start()

# it’s best to use their _threadsafe alternatives. Let’s see how that looks:

new_loop.call_soon_threadsafe(more_work, 6)
new_loop.call_soon_threadsafe(more_work, 3)

'''
Now we’re talking! Executing this code does not block the main interpreter, allowing us to give it more work. Since the work executes in order, we now essentially have a task queue.

We just went to multi-threaded execution of single-threaded code, but isn’t concurrency part of what we get with asyncio? Sure it is! That loop on the worker thread is still async, so let’s enable parallelism by giving it awaitable coroutines.
'''



new_loop.call_soon_threadsafe(more_work, 20)
asyncio.run_coroutine_threadsafe(do_some_work(5), new_loop)
asyncio.run_coroutine_threadsafe(do_some_work(10), new_loop)
'''
These instructions illustrate how python is going about execution. The first call to more_work blocks for 20 seconds, while the calls to do_some_work execute in parallel immediately after more_work finishes.
'''


'''
notifications by email
'''
'''
# Do some work to get email body
message = "say stuff here"

# Connect to the server
server = smtplib.SMTP("smtp.gmail.com:587")
server.ehlo()
server.starttls()
server.login(username, password)

# Send the email
server.sendmail(from_addr, email, message)
server.quit()


def start_email_worker(loop):
    """Switch to new event loop and run forever"""

    asyncio.set_event_loop(loop)
    loop.run_forever()

# Create the new loop and worker thread
worker_loop = asyncio.new_event_loop()
worker = Thread(target=start_email_worker, args=(worker_loop,))

# Start the thread
worker.start()

# Assume a Flask restful interface endpoint
@app.route("/notify")
def notify(email):
    """Request notification email"""

worker_loop.call_soon_threadsafe(send_notification, email)
'''




print("ALL Finished ")
