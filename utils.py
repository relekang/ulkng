# -*- coding: utf8 -*-
from jinja2 import Environment, FileSystemLoader
import os
import web


PREFIX = "ulkng:"
URL_HASH_NAME = "url"
COUNT_HASH_NAME = "url:count"
LOG_HASH_NAME = "url:log"
TOKEN_HASH_NAME = "ulkng:tokens"


def check_token(r):
    tokens = r.hgetall(TOKEN_HASH_NAME)
    try:
        if web.input().token in tokens:
            return (tokens[web.input().token], web.input().token)
        else:
            raise web.notfound()
    except AttributeError:
        raise web.notfound()

def render_template(template_name, **context):
    extensions = context.pop('extensions', [])
    globals = context.pop('globals', {})

    jinja_env = Environment(
        loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
        extensions=extensions,
    )
    jinja_env.globals.update(globals)

    return jinja_env.get_template(template_name).render(context)