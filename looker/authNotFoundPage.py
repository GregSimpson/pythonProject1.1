import looker_sdk

# For this to work you must either have set environment variables or created a looker.ini as described below in "Configuring the SDK"
#sdk = looker_sdk.init40()  # or init31() for the older v3.1 API
sdk = looker_sdk.init31()  # or init31() for the older v3.1 API

my_user = sdk.me()

# output can be treated like a dictionary
print(my_user["first_name"])
print(my_user["last_name"])
# or a model instance (User in this case)
print(my_user.first_name)
print(my_user.last_name)
