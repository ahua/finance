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

    def get_dailysum(self):
        d = []
        day = DailyData.get_latest_day(self.mysql_session)
        topcat = []
        topcat_id = int(self.get_argument('topcat', '-1'))
        if topcat_id == -1:
            top_cat_list = Category.get_all_top_cat(self.mysql_session)
        else:
            top_cat_list = Category.get_all_direct_child(topcat_id, self.mysql_session)
        for cat in top_cat_list:
            topcat.append(cat.as_dict())
            leaf_cat_list = Category.get_all_leaf_cat([cat.id], self.mysql_session)
            if cat.is_leaf_node:
                leaf_cat_list.append(cat.id)
            _qs = Stock.get_all_stock(cat_list=leaf_cat_list, session=self.mysql_session)
            code_list = [i.code for i in _qs]
            market_value = DailyData.get_sum_column(code_list, day, DailyData.market_value, self.mysql_session)
            d.append({'name': cat.name, 'market_value': market_value})

        d = sorted(d, key=lambda i: i['market_value'], reverse=True)
        labels = []
        data = []
        for i in d:
            labels.append(i['name'])
            data.append(i['market_value'])
        market_value_data = {
            "labels" : labels,
            "datasets" : [
                {"data" : data},
                ]
            }

        def random_color():
            import random
            r = lambda: random.randint(0,255)
            s = '#%02X%02X%02X' % (r(),r(),r())
            return s
        t = []
        total_market_value = sum(data)
        for i in d:
            t.append({'value': round(i['market_value']/total_market_value * 100, 2),
                      'label': i['name'],
                      'color': random_color(),
                      'highlight': random_color()})
        self.context['doughnut_data'] = t
        self.context['market_value_data'] = market_value_data
        self.reply(0, self.context)
        
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
        elif action == 'dailysum':
            self.get_dailysum()
        else:
            self.reply(1, {'err_content': 'wrong action.'})
        
