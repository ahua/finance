#!/usr/bin/env python

from website.base import BaseHandler

__all__ = ['IndexHandler', 'EnglishHandler', 'ChineseHandler']

class IndexHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('admin/index.html', **self.context)

class EnglishHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('admin/english.html', **self.context)

class ChineseHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('admin/chinese.html', **self.context)
