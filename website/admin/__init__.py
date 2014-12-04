from .handlers import *
from .test import *

web_handlers = [
    ('/admin', IndexHandler),
    ('/admin/english', EnglishHandler),
    ('/admin/chinese', ChineseHandler),
    ('/test', TestHandler)
    ]
