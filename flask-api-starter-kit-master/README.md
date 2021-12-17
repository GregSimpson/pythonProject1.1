# Flask API Starter Kit


cd pythonProject1.1/flask-api-starter-kit-master  
clear; pipenv run python -m unittest



cd /home/gsimpson/gjs/git_stuff/pythonProject1.1/flask-api-starter-kit-master  
pipenv run python -m flask run

 - threaded example
 - https://gist.github.com/vickumar1981/c3607805e2dd234c686eb6ca6c370ca2

 - flask-api-starter example
 - https://github.com/bajcmartinez/flask-api-starter-kit


Sample API layout structure to be used as a baseline for other apps

## Dependencies

- [flask](https://palletsprojects.com/p/flask/): Python server of choise
- [flasgger](https://github.com/flasgger/flasgger): Used to generate the swagger documentation
- [flask-marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/): My favourite serializer
- [apispec](https://apispec.readthedocs.io/en/latest/): Required for the integration between marshmallow and flasgger

## Set Up

1. Check out the code
2. Install requirements
    ```
    pipenv install
    ```
3. Start the server with:
    ```
   pipenv run python -m flask run
    ```
   
4. Visit http://localhost/api for the home api

4. Visit http://localhost/apidocs for the swagger documentation
   
## Tests

The code is covered by tests, to run the tests please execute

```
pipenv run python -m unittest
```