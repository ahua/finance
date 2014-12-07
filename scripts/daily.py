#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
sys.path.insert(0, "../")

from website import *
from lib import get_data

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage %s filename day" % sys.argv[0]
        sys.exit(1)
    filename = sys.argv[1]
    day = sys.argv[2]
    if len(day) != 8:
        print "len(day) != 8"
        sys.exit(1)

    data = get_data(filename)
    session = create_session()
    for i in data:
        o = DailyData()
        o.day = day
        o.code = i['code']
        o.p_open = i['p_open']
        o.p_close = i['p_close']
        o.p_high = i['p_high']
        o.p_low = i['p_low']
        o.p_inc = i['p_inc']
        o.p_earning_ratio = i['p_earning_ratio']
        o.trade_count = i['trade_count']
        o.trade_money = i['trade_money']
        o.market_value = i['market_value']
        o.is_suspend_trading = i['is_suspend_trading']
        session.add(o)
    session.commit()
    session.close()
    
        
