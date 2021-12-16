to set up run the install script. If that doesn't work for whatever reason do the following

1. curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
2. export PATH="$HOME/.poetry/bin:$PATH"
3. cd into the root directory of the project
4. make (if you don't have make then poetry install)

to run the project:

poetry run uvicorn shift_service.server:app --host 0.0.0.0 --port 8000 

documentation for the apis are at:
https://0.0.0.0:8000/docs


to run unit tests:
  make test

Steps to making shifts:
1. create a user
2. log in as the user
3. make a shift for that user or any other user provided user level is 2
3a. If user level is 1 all non get apis will fail

