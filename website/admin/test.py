#!/usr/bin/env python

from website.base import BaseHandler

class TestHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('admin/test.html')
