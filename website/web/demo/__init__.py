#!/usr/bin/env python

import os

from ..base import BaseHandler

__all__ = ['demo_handlers']

class IndexHandler(BaseHandler):
    def get(self, *args, **kwargs):
        what = self.get_argument('what', '')
        template_path = self.application.settings['template_path']

        _dirpath = os.path.join(template_path, 'demo')
        demos = filter(lambda i: os.path.isdir(os.path.join(_dirpath, i)), os.listdir(_dirpath))
        _dirpath = os.path.join(_dirpath, what)
        htmls = filter(lambda i: not os.path.isdir(os.path.join(_dirpath, i)), os.listdir(_dirpath))
        htmls = map(lambda i: os.path.join('/demo/%s' % what, i), htmls)
        self.render('demo/index.html', demos=demos, htmls=htmls, what=what, 
                    **self.context)

    

class StaticFileHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render(self.context['uri'][1:])

demo_handlers = [
    (r'/demo/index', IndexHandler),
    (r'/demo/.*', StaticFileHandler),
    ]

