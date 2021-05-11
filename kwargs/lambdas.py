
# https://betterprogramming.pub/5-advanced-python-function-concepts-explained-with-examples-dcf10389ac9a

# Create a list of numbers for sorting
numbers = [3, 11, 7, 5]
# Sort the numbers by default
print (sorted(numbers))

# Sort the numbers by their remainders when divided by 3
print (sorted(numbers, key=lambda x:x % 3) )


##   In data science, we often use the pandas library for data processing.
# Lambda functions can also be useful for extracting information from existing
# data columns. The following code shows you a trivial example that uses a lambda
# function to map data with a pandas Series data object:
import pandas as pd
# Create a data series
old_ids = pd.Series("prefix1001 prefix1002 prefix1003".split(), name="old_id")
print(old_ids)

new_ids = old_ids.map(lambda x: int(x[6:]))
print(new_ids)



