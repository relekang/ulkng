# -*- coding: utf8 -*-
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 1

USE_TOKENS = True
DEBUG = False

PREFIX = "ulkng:"
URL_HASH_NAME = "url"
COUNT_HASH_NAME = "url:count"
LOG_HASH_NAME = "url:log"
TOKEN_HASH_NAME = "ulkng:tokens"

try:
	import local_settings
except ImportError:
	pass