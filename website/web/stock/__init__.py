#!/usr/bin/env python
from .daily import DailyHandler
stock_handlers = [
    ('/stock/daily', DailyHandler),
    
    ]
