from .index import IndexHandler
from .test import TestHandler

handlers = [
    ('/admin', IndexHandler),
    ('/test', TestHandler)
    ]
