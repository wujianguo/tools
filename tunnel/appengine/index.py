#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import tornado.ioloop
import tornado.web
import tornado.wsgi

peers = set()

class PingHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("hello")
        # peers.update()
        # self.write(json.dumps([peers]))


def apps():
    settings = {"debug": True}
    application = tornado.web.Application([
        (r"/", PingHandler),
    ], **settings)
    return application

def main():
    apps().listen(8888)
    tornado.ioloop.IOLoop.instance().start()


application = tornado.wsgi.WSGIAdapter(apps())

if __name__=='__main__':
    main()