#!/usr/bin/env python

import os
import tornado.ioloop
import tornado.web

import website.settings
import website.admin

if __name__ == "__main__":
    settings = website.settings.init_app_settings()
    handlers = website.admin.web_handlers
    app = tornado.web.Application(handlers, **settings)
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
