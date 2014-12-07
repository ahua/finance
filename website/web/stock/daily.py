#!/usr/bin/env python

from ..base import BaseHandler

class DailyHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('stock/daily.html', **self.context)
