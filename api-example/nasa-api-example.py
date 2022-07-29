# https://rapidapi.com/blog/how-to-use-an-api-with-python/
# NASA developer key

# You can start using this key to make web service requests. Simply pass your key in the URL when making a web request. Here's an example:
# https://api.nasa.gov/planetary/apod?api_key=liU2fLR9wSlxYvOXTuo2yZXozOXw9fxt8RonNxSC

# nasaAPI= 'https://NasaAPIdimasV1.p.rapidapi.com/getAPICEarthImagery'
nasaAPI = 'https://api.nasa.gov/planetary/apod'
xRapidApiKey = 'liU2fLR9wSlxYvOXTuo2yZXozOXw9fxt8RonNxSC'

response =
    unirest.post(nasaAPI, headers={ 'api_key': nasaAPI})


