#!/usr/bin/env python

from website.base import BaseHandler

class IndexHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('admin/index.html')
