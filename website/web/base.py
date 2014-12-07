#!/usr/bin/env python
#-*- coding:utf-8 -*-

import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.context = {}
        i = self.request.uri.find("?")
        if i >= 0:
            self.context['uri'] = self.request.uri[0:i]
        else:
            self.context['uri'] = self.request.uri

        

