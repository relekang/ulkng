# -*- coding: utf8 -*-
import hashlib
from redis import ConnectionPool
from redis.client import Redis
import web
from web import form

PREFIX = "ulkng:"
URL_HASH_NAME = "url"
COUNT_HASH_NAME = "url:count"

web.config.debug = False
render = web.template.render('templates/', base='base')
redis_pool = ConnectionPool(host='localhost', port=6379, db=1)

def check_token(r):
    try:
        if web.input().token != r.get("%stoken" % PREFIX):
            raise web.notfound()
    except AttributeError:
        raise web.notfound()

urls = (
    '/', 'NotFound',
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

class ViewAll:
    def GET(self):
        r = Redis(connection_pool=redis_pool)
        check_token(r)

        all_keys = r.hgetall(URL_HASH_NAME)
        url_list = []

        for key in all_keys:
            url_list.append(
                (all_keys[key], key, r.hget(COUNT_HASH_NAME, key) or 0),
            )

        return render.list(url_list)

class Add:
    def GET(self):
        r = Redis(connection_pool=redis_pool)
        check_token(r)

        form = url_form()
        return render.formtest(form)

    def POST(self):
        r = Redis(connection_pool=redis_pool)

        check_token(r)

        form = url_form()

        if not form.validates():
            return render.formtest(form)

        url = form['url'].value
        token = hashlib.sha1()
        token.update(url.replace('http(s)?://', '').strip())
        key = token.hexdigest()[:6]
        print key + url
        r.hset(URL_HASH_NAME, key, url)
        r.hset(COUNT_HASH_NAME, key, 0)

        raise web.seeother('/%s/+' % key)

class Redirect:
    def GET(self, key):
        r = Redis(connection_pool=redis_pool)
        url = r.hget(URL_HASH_NAME, key)
        if url:
            r.hincrby(COUNT_HASH_NAME, key)
            raise web.seeother(url)
        else:
            raise web.notfound()

class ViewDetails:
    def GET(self, key):
        print "details"
        r = Redis(connection_pool=redis_pool)
        url = r.hget(URL_HASH_NAME, key)
        if url:
            count = r.hget(COUNT_HASH_NAME, key)

            return render.details(key, url, count)
        else:
            raise web.notfound()

class NotFound:
    def GET(self):
        raise web.notfound()

app = web.application(urls, globals())

application = app.wsgifunc()

if __name__ == "__main__":
    app.run()