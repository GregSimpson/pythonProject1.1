
# importing the requests library
import io
import requests

# api-endpoint
URL = "https://maps.googleapis.com/maps/api/geocode/json"

# https://console.cloud.google.com/apis/credentials?referrer=search&project=woven-solution-357815&supportedpurview=project

API_KEY = "<pswd here">"
# gjs-service-1@woven-solution-357815.iam.gserviceaccount.com


# location given here
location = "delhi technological university"

# defining a params dict for the parameters to be sent to the API
PARAMS = {'address':location, 'key': API_KEY}

# sending get request and saving the response as response object
r = requests.get(url = URL, params = PARAMS)

# extracting data in json format
data = r.json()

print(data)

## extracting latitude, longitude and formatted address
## of the first matching location
#latitude = data['results'][0]['geometry']['location']['lat']
#longitude = data['results'][0]['geometry']['location']['lng']
#formatted_address = data['results'][0]['formatted_address']

## printing the output
#print("Latitude:%s\nLongitude:%s\nFormatted Address:%s"
#      %(latitude, longitude,formatted_address))
