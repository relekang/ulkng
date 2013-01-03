# -*- coding: utf8 -*-
import hashlib
from redis import ConnectionPool
from redis.client import Redis
import web
from web import form

PREFIX = "ulkng:"

web.config.debug = False
render = web.template.render('templates/')
redis_pool = ConnectionPool(host='localhost', port=6379, db=1)

urls = (
    '/', 'NotFound',
    '/add', 'Add',
    '/(.*)/\+', 'Details',
    '/(.*)/', 'Redirect',
    '/(.*)', 'Redirect',
)

url_form = form.Form(
    form.Textbox("url"),
)

class Add:
    def GET(self):
        form = url_form()
        return render.formtest(form)

    def POST(self):
        r = Redis(connection_pool=redis_pool)

        if web.input().token != r.get("%stoken" % PREFIX):
            raise web.notfound()

        form = url_form()

        if not form.validates():
            return render.formtest(form)

        url = form['url'].value
        token = hashlib.sha1()
        token.update(url.replace('http(s)?://', '').strip())
        key = token.hexdigest()[:6]
        print key + url
        r.set(key, url)
        r.set('%scount' % key, 0)

        raise web.seeother('/%s/+' % key)

class Redirect:
    def GET(self, key):
        r = Redis(connection_pool=redis_pool)
        url = r.get(key)
        if url:
            r.incr('%scount' % key)
            raise web.seeother(url)
        else:
            raise web.notfound()

class Details:
    def GET(self, key):
        print "details"
        r = Redis(connection_pool=redis_pool)
        url = r.get(key)
        if url:
            count = r.get('%scount' % key)

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