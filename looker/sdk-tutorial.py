import looker_sdk #Note that the pip install required a hyphen but the import is an underscore.

import os #We import os here in order to manage environment variables for the tutorial. You don't need to do this on a local system or anywhere you can more conveniently set environment variables.

import json #This is a handy library for doing JSON work.

#os.environ["LOOKERSDK_BASE_URL"] = "https://<projectroot>.looker.com" #If your looker URL has .cloud in it (hosted on GCP), do not include :19999 (ie: https://your.cloud.looker.com).
#os.environ["LOOKERSDK_API_VERSION"] = "3.1" #3.1 is the default version. You can change this to 4.0 if you want.
#os.environ["LOOKERSDK_VERIFY_SSL"] = "true" #Defaults to true if not set. SSL verification should generally be on unless you have a real good reason not to use it. Valid options: true, y, t, yes, 1.
#os.environ["LOOKERSDK_TIMEOUT"] = "120" #Seconds till request timeout. Standard default is 120.
#
##Get the following values from your Users page in the Admin panel of your Looker instance > Users > Your user > Edit API keys. If you know your user id, you can visit https://your.looker.com/admin/users/<your_user_id>/edit.
#os.environ["LOOKERSDK_CLIENT_ID"] =  "<api key numeric>>" #No defaults.
#os.environ["LOOKERSDK_CLIENT_SECRET"] = "<api value>>" #No defaults. This should be protected at all costs. Please do not leave it sitting here, even if you don't share this document.
#
#print("All environment variables set.")


sdk = looker_sdk.init40()  # or init31() for the older v3.1 API
my_user = sdk.me()

# output can be treated like a dictionary
print(my_user["first_name"])
# or a model instance (User in this case)
print(my_user.first_name)


#sdk = looker_sdk.init31()
#print('Looker SDK 3.1 initialized successfully.')

#Uncomment out the lines below if you want to instead initialize the 4.0 SDK. It's that easy— Just replace init31 with init40.
#sdk = looker_sdk.init40()
#print('Looker SDK 4.0 initialized successfully.')


#sdk.test_connection_config("realplay_dce1_dev")
#my_user = sdk.me()

#Output is an instance of the User model, but can also be read like a python dict. This applies to all Looker API calls that return Models.
#Example: The following commands return identical output. Feel free to use whichever style is more comfortable for you.

print(my_user.first_name) #Model dot notation
print(my_user["first_name"]) #Dictionary