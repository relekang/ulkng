# -*- coding: utf8 -*-
import hashlib
from redis import ConnectionPool
from redis.client import Redis
from utils import render_template, check_token, notfound
from settings import REDIS_HOST, REDIS_PORT, REDIS_DB, URL_HASH_NAME, COUNT_HASH_NAME, LOG_HASH_NAME, TOKEN_HASH_NAME, DEBUG
import web
from web import form

web.config.debug = DEBUG
redis_pool = ConnectionPool(
    host=REDIS_HOST, 
    port=REDIS_PORT, 
    db=REDIS_DB
)

urls = (
    '/', 'Index',
    '/favicon.ico', 'NotFound',
    '/add/', 'Add',
    '/all/', 'ViewAll',
    '/(.*)/\+', 'ViewDetails',
    '/(.*)/', 'Redirect',
    '/(.*)', 'Redirect',
)

url_form = form.Form(
    form.Textbox("url"),
)

class Index:
    def GET(self):
        r = Redis(connection_pool=redis_pool)

        count = 0
        for key in r.hgetall(URL_HASH_NAME):
            count += 1

        return render_template('index.html', count=count, section_class='index', user_id=None)

class ViewAll:
    def GET(self):
        r = Redis(connection_pool=redis_pool)
        user_id = check_token(r)

        all_keys = r.hgetall(URL_HASH_NAME)
        url_list = []

        for key in all_keys:
            url_list.append(
                (
                    all_keys[key].replace('http://', '').replace('https://', ''),
                    key, r.hget(COUNT_HASH_NAME, key) or 0,
                    r.hget(LOG_HASH_NAME, key) or ''
                ),
            )

        return render_template('list.html', user_id=user_id, list=url_list, is_all=True)

class Add:
    def GET(self):
        r = Redis(connection_pool=redis_pool)
        user_id = check_token(r)

        form = url_form()
        return render_template('add.html',
            form=form,
            user_id=user_id,
            is_add=True,
        )

    def POST(self):
        r = Redis(connection_pool=redis_pool)

        user_id = check_token(r)

        form = url_form()

        if not form.validates():
            return render_template('add.html',
                form=form,
                user_id=user_id,
                is_add=True,
            )

        url = form['url'].value
        token = hashlib.sha1()
        token.update(url.replace('http(s)?://', '').strip())
        key = token.hexdigest()[:6]
        print key + url
        if not r.hget(URL_HASH_NAME, key):
            r.hset(URL_HASH_NAME, key, url)
            r.hset(COUNT_HASH_NAME, key, 0)
            if user_id[1]:
                r.hset(LOG_HASH_NAME, key, r.hget(TOKEN_HASH_NAME, web.input().token))

        if user_id[1] == '':
            raise web.seeother('/%s/+' % key)
        else:
            raise web.seeother('/%s/+?token=%s' % (key, user_id[1]))

class Redirect:
    def GET(self, key):
        r = Redis(connection_pool=redis_pool)
        url = r.hget(URL_HASH_NAME, key)
        if url:
            r.hincrby(COUNT_HASH_NAME, key)
            raise web.seeother(url)
        else:
            raise notfound()

class ViewDetails:
    def GET(self, key):
        r = Redis(connection_pool=redis_pool)

        user_id = check_token(r)

        url = r.hget(URL_HASH_NAME, key)
        if url:
            count = r.hget(COUNT_HASH_NAME, key)

            return render_template('details.html',
                user_id=user_id,
                key=key,
                url=url,
                count=count,
                section_class='index'
            )
        else:
            raise notfound()

class NotFound:
    def GET(self):
        raise notfound()

app = web.application(urls, globals())

application = app.wsgifunc()

if __name__ == "__main__":
    print 'DEBUG=%s' % DEBUG
    app.run()