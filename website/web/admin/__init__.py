from .handlers import *

admin_handlers = [
    ('/admin', IndexHandler),
    ('/admin/english', EnglishHandler),
    ('/admin/chinese', ChineseHandler),
    ]
