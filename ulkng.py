# -*- coding: utf8 -*-
import hashlib

import web
from web import form
from redis.client import Redis

web.config.debug = False
render = web.template.render('templates/')

urls = (
    '/', 'Add',
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
        form = url_form()

        if not form.validates():
            return render.formtest(form)

        r = Redis()
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
        r = Redis()
        url = r.get(key)
        if url:
            r.incr('%scount' % key)
            raise web.seeother(url)
        else:
            raise web.notfound()

class Details:
    def GET(self, key):
        print "details"
        r = Redis()
        url = r.get(key)
        if url:
            count = r.get('%scount' % key)

            return render.details(key, url, count)
        else:
            raise web.notfound()


app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()