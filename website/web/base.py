#!/usr/bin/env python
#-*- coding:utf-8 -*-

import json
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


    def reply(self, code=0, detail={}):
        self.set_header('Content-Type', 'text/plain')
        self.write(json.dumps(
                {'code': code,
                 'detail': detail
                 }, encoding='utf-8', ensure_ascii=True))
        self.finish()
        
