# https://gist.github.com/eriky/dbe771a65e12a9fbe7b082da4a72241c#file-return_multiple_variables-py

def get_user(id):
    # fetch user from database
    # ....
    name = "somebody"
    birthdate = "1/1/2021"
    return name, birthdate

name, birthdate = get_user(4)

print ( name + " + " + birthdate)