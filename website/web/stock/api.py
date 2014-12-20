#!/usr/bin/env python

import json

from website.models import *
from ..base import BaseHandler

class ApiHandler(BaseHandler):

    def get_topcat(self):
        cats = Category.get_all_top_cat(self.mysql_session)
        detail = {}
        detail['cats'] = []
        for i in cats:
            detail['cats'].append(i.as_dict())
        detail['count'] = len(detail['cats'])
        self.reply(0, detail)    

    def get_childcat(self):
        id = int(self.get_argument('catid', '-1'))
        if id == -1:
            self.reply(0, {'count': 0, 'cats': []})
            return
        cats = Category.get_all_direct_child(id, self.mysql_session)
        detail = {}
        detail['cats'] = []
        for i in cats:
            detail['cats'].append(i.as_dict())
        detail['count'] = len(detail['cats'])
        self.reply(0, detail)
        
    def get_dailystock(self):
        topcat = int(self.get_argument('topcat', '-1'))
        secondcat = int(self.get_argument('secondcat', '-1'))
        thirdcat = int(self.get_argument('thirdcat', '-1'))

        if thirdcat != -1:
            cat_list = [thirdcat]
        elif secondcat != -1:
            cat_list = Category.get_all_leaf_cat([secondcat], self.mysql_session)
            cat = self.mysql_session.query(Category).filter(Category.id==secondcat).first()
            if cat.is_leaf_node and cat.id not in cat_list:
                cat_list.append(cat.id)
        elif topcat != -1:
            cat_list = Category.get_all_leaf_cat([topcat], self.mysql_session)
            cat = self.mysql_session.query(Category).filter(Category.id==topcat).first()
            if cat.is_leaf_node and cat.id not in cat_list:
                cat_list.append(cat.id)
        else:
            cat_list = []
        print cat_list
        day = DailyData.get_latest_day(self.mysql_session)
        code_list = Stock.get_code_list(cat_list, self.mysql_session)
        qs = DailyData.get_daily_data(code_list, day, self.mysql_session)
        page = int(self.get_argument('page', 1))
        psize = int(self.get_argument('psize', 100))
        qs = qs.offset((page-1) * psize).limit(psize)
        detail = {}
        detail['data'] = []
        for i in qs:
            stock = self.mysql_session.query(Stock).filter(Stock.code == i.code).first()
            kwargs = stock.as_dict()
            kwargs.update(i.as_dict())
            detail['data'].append(kwargs)
        detail['count'] = len(detail['data'])
        self.reply(0, detail)


    def get(self, *args, **kwargs):
        action = self.get_argument('action', '')
        if action == 'topcat':
            self.get_topcat()
        elif action == 'childcat':
            self.get_childcat()
        elif action == 'dailystock':
            self.get_dailystock()
        else:
            self.reply(1, {'err_content': 'wrong action.'})
        
