#!/usr/bin/env python
from .daily import DailyHandler
from .api import ApiHandler
stock_handlers = [
    ('/stock/daily', DailyHandler),
    ('/stock/api', ApiHandler),
    ]
