#!/usr/bin/env python
#-*- coding:utf-8 -*-

import tornado.web
from ..models import *

class BaseHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.context = {}
        i = self.request.uri.find("?")
        if i >= 0:
            self.context['uri'] = self.request.uri[0:i]
        else:
            self.context['uri'] = self.request.uri

    @property
    def mysql_session(self):
        if not hasattr(self, "_mysql_session"):
            self._mysql_session = create_session()
        return self._mysql_session


