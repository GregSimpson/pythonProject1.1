cd ~/gjs/git_stuff/pythonProject1.1/flask-api-starter-kit-master

# start the server
clear ;pipenv run python -m flask run

# run any or all of these
curl -X GET "http://127.0.0.1:5000/api/async_example/" -H "accept: application/json"
curl -X GET "http://127.0.0.1:5000/api/auth0_async/" -H "accept: application/json"
curl -X GET "http://127.0.0.1:5000/api/auth0_sync/" -H "accept: application/json"
curl -X GET "http://127.0.0.1:5000/api/logtest/" -H "accept: application/json"
curl -X GET "http://127.0.0.1:5000/apidocs/" -H "accept: application/json"


# dont need the server running for this
#  BUT because of the threads, you need to hit ctrl-c
clear ;pipenv run python -m unittest

