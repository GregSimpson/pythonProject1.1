
# Python isn’t the only language that has the concept of closures.
# Many other mainstream languages (e.g. Swift) share the feature of closures.
# In essence, closures are inner functions that capture non-local variables
# defined in outer functions. Let’s take a look at the following code example:

def make_incrementer(step):
    # Track the count
    counter = 0
    #print(" outer ")
    #print(counter)
    # Define the incrementer function
    def incrementer():
        nonlocal counter
        counter += step
        #print (" inner ")
        #print(counter)
        return counter
    # Return the incrementer function
    #print ( incrementer )
    return incrementer

incrementer_ten = make_incrementer(10)

print (incrementer_ten.__closure__[0].cell_contents)

