# -*- coding: utf8 -*-
from jinja2 import Environment, FileSystemLoader
import os
import web
import settings

def check_token(r):
    if not getattr(settings, 'USE_TOKENS', True):
        return ('anonymous', '')
        
    tokens = r.hgetall(settings.TOKEN_HASH_NAME)
    try:
        auth_token = web.input().token
        if auth_token in tokens:
            return (tokens[auth_token], auth_token)
        else:
            raise notfound()
    except AttributeError:
        raise notfound()

def render_template(template_name, **context):
    extensions = context.pop('extensions', [])
    globals = context.pop('globals', {})

    jinja_env = Environment(
        loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
        extensions=extensions,
    )
    jinja_env.globals.update(globals)

    return jinja_env.get_template(template_name).render(context)

def notfound():
    return web.notfound(render_template('404.html', user_id=None, section_class='alert alert-error'))