#!/bin/bash -xe 

$(which curl) -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

export PATH="$HOME/.poetry/bin:$PATH"

$(which poetry) install

