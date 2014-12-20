#!/usr/bin/env python

import json

from website.models import *
from ..base import BaseHandler

class DailyHandler(BaseHandler):
    def get(self, *args, **kwargs):
        d = []
        day = DailyData.get_latest_day(self.mysql_session)
        topcat = []
        top_cat_list = Category.get_all_top_cat(self.mysql_session)
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
        self.context['doughnut_data'] = json.dumps(t)
        self.context['market_value_data'] = json.dumps(market_value_data)
        self.context['topcat'] = topcat
        self.render('stock/daily.html', **self.context)

