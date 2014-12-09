#!/usr/bin/env python

from ..base import BaseHandler

class TestHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('test/%s' % args[0])
