# u.lkng
A personal url-shortener. I wrote this to play with web.py and Redis

**Why the name?** Simply because of the url [u.lkng.me](http://u.lkng.me)

## Dependencies
* Redis
* web.py
* redis-py

## Installation
### Install redis if you do not have it

Download it from [redis.io](http://redis.io) or install it with apt-get, Homebrew or something similar.

### Create virtualenvironment and install python dependencies

    virtualenv venv                                          # Create virtualenv
    source venv/bin/activate                                 # Activate it
    pip install -r requirements.txt                          # Install python dependencies
    redis-cli hset ulkng:tokens <your token> "<your email>"  # Set the token used for auth

## Usage
    python ulkng.py

## Settings
It is possible to add custom settings by adding a file `local_settings.py`

`USE_TOKENS` - Default: True, when false no token is necessary to add, list all and view details about urls.
