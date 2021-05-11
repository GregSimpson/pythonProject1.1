
# https://betterprogramming.pub/5-advanced-python-function-concepts-explained-with-examples-dcf10389ac9a

dict(a=1, b=2, c=3)

dict(a=4, b=5, c=6)


# >>> # Example with a custom function
def send_info(**kwargs):
    for key, value in kwargs.items():
        print(f"parameter name: {key}; value: {value}")
...

send_info(name="John", age=16)
send_info(first_name="John", last_name="Smith")
