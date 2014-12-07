#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, "../")

from website import *
from lib import get_data

def get_all_area(session):
    q = session.query(Area)
    d = {}
    for i in q:
        d[i.name] = i.id
    return d

def get_all_cat(session):
    q = session.query(Category)
    d = {}
    for i in q:
        d[i.name] = i.id
    return d

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: %s dirpath" % sys.argv[0]
        sys.exit(1)
    session = create_session()
    areas = get_all_area(session)
    cats = get_all_cat(session)
    dirpath = sys.argv[1]
    filelist = os.listdir(dirpath)
    for i in filelist:
        cat = i.split(".")[0].decode("utf-8")
        cat_id = cats.get(cat, None)
        filename = os.path.join(dirpath, i)
        data = get_data(filename)
        for o in data:
            stock = Stock()
            stock.name = o['name']
            stock.code = o['code']
            stock.market_day = o['market_day']
            stock.area_id = areas[o['area'].decode("utf-8")]
            stock.category_id = cat_id
            session.add(stock)
    session.commit()
    session.close()
    
