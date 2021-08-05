import looker_sdk #Note that the pip install required a hyphen but the import is an underscore.

import os #We import os here in order to manage environment variables for the tutorial. You don't need to do this on a local system or anywhere you can more conveniently set environment variables.

import json #This is a handy library for doing JSON work.



class Looker:
  def __init__(self):
    #self.host = LOOKER_EMBED_HOST
    #self.secret = LOOKER_EMBED_SECRET
    self.gjs = 'gjs'

def get_all_users(sdk):
    # https://docs.looker.com/reference/api-and-integration/api-reference/v3.1/user#get_all_users
    return sdk.all_users()

def show_names(user_array):
    for each_user in user_array:
        #print(each_user["email"])
        if ( (each_user.is_disabled == False) and (each_user["email"] != '') ):
            print(each_user["email"])



def show_info(my_user):
    # output can be treated like a dictionary
    print(my_user["first_name"])
    # or a model instance (User in this case)
    print(my_user.first_name)

    print(my_user.first_name) #Model dot notation
    print(my_user["first_name"]) #Dictionary

    print(my_user.locale)


if __name__ == "__main__":

    sdk = looker_sdk.init40()  # or init31() for the older v3.1 API
    my_user = sdk.me()

    #show_info(my_user)
    show_names( get_all_users(sdk) )


