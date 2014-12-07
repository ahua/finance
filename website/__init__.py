from models import *

from web.admin import admin_handlers
from web.stock import stock_handlers
from web.test import test_handlers
from web.demo import demo_handlers

handlers = admin_handlers + stock_handlers + test_handlers + demo_handlers

