#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
sys.path.insert(0, "../")

from website import *
from lib import get_data

if __name__ == "__main__":
    data = get_data()
    session = create_session()
    area_set = set([i['area'] for i in data])
    for area in area_set:
        o = Area()
        o.name = area
        session.add(o)
    session.commit()
    session.close()
