#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
sys.path.insert(0, "../")

from website import *

def get_data(filename=None):
    if not filename:
        print "Usage: %s filename day" % sys.argv[0]
        sys.exit(1)
    data = []
    with open(filename) as fp:
        for li in fp:
            args = []
            if li.find("\t") >= 0:
                args = li.rstrip().split("\t")
            elif li.find(",") >= 0:
                args = li.rstrip().split(",")
            if len(args) != 21:
                print "Waring:(wrong line %s)='%s'" % (len(args), li.rstrip())
                continue
            if not args[0].isdigit():
                print "Waring:(wrong line)='%s'" % li.rstrip()
                continue
            args = [i.strip().rstrip() for i in args]
            kwargs = {}
            is_suspend_trading = False
            if args[11] == '--':
                is_suspend_trading = True
            kwargs['is_suspend_trading'] = is_suspend_trading
            kwargs['code'] = args[0]
            kwargs['name'] = args[1]
            kwargs['p_open'] = float(args[11]) if not is_suspend_trading else None
            kwargs['p_close'] = float(args[4]) 
            kwargs['p_high'] = float(args[12]) if not is_suspend_trading else None
            kwargs['p_low'] = float(args[13]) if not is_suspend_trading else None
            kwargs['p_inc'] = float(args[5]) if not is_suspend_trading else None
            kwargs['p_earning_ratio'] = float(args[15]) if args[15] != '--' else None
            kwargs['trade_count'] = int(args[8]) if not is_suspend_trading else None
            kwargs['trade_money'] = args[16] if not is_suspend_trading else None
            if is_suspend_trading:
                kwargs['market_value'] = None
            else:
                #if args[18][-3:] == '亿':
                kwargs['market_value'] = float(args[19][:-3])
            kwargs['area'] = args[18]
            kwargs['market_day'] = args[20]

            
            data.append(kwargs)
    return data



if __name__ == "__main__":
    session = create_session()
    session.close()
    
        
