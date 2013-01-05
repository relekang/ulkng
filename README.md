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

    virtualenv venv                        # Create virtualenv
    source venv/bin/activate               # Activate it
    pip install -r requirements.txt        # Install python dependencies
    redis-cli set ulkng:token "your token" # Set the token used for auth

## Usage
    python ulkng.py