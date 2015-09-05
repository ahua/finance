#!/usr/bin/env python
#-*- coding:utf-8 -*-

import datetime
import sys

class Traning:

    def _line_to_dict(self, values):
        keys = [
            "date",
            "c.open",
            "c.high",
            "c.low",
            "c.close",
            "volume",
            "ma5",
            "ma10",
            "ma20",
            "ma60",
            "ma120",
            "ma250",
            "ma.7",
            "ma.8",
            "ma.9",
            "ma.10",
            "vol.volume",
            "vol.ma5",
            "vol.ma10",
            "kdj.k",
            "kdj.d",
            "kdj.j",
            "boll.boll",
            "boll.up",
            "boll.lb",
            "macd.dif",
            "macd.dea",
            "macd.macd",
        ]
        d = {}
        for i in xrange(len(keys)):
            d[keys[i]] = values[i]
        return {d["date"]: d}

    
    def _init_data(self):
        with open(self.datapath) as fp:
            for line in fp:
                values = line.rstrip().split(";")
                if self.header is None:
                    self.col_width = len(values)
                    self.header = line.rstrip()
                else:
                    assert len(values) == self.col_width
                    self.datas.update(self._line_to_dict(values))
    

    def __init__(self, datapath="day.csv"):
        self.datas = {}
        self.datapath = datapath
        self.col_width = None
        self.header = None
        self._init_data()
        self.valid_days = self.datas.keys()
        self.min_day = datetime.datetime.strptime(min(self.valid_days), "%Y/%m/%d")
        self.max_day = datetime.datetime.strptime(max(self.valid_days), "%Y/%m/%d")


    def _get_c_close(self, dd):
        if isinstance(dd, str):
            return self.datas[dd]["c.close"]
        if isinstance(dd, datetime.datetime):
            return self.datas[dd.strftime("%Y/%m/%d")]["c.close"]
        raise Exception("unknown dd type.")


    def _get_previous_valid_dd(self, dd):
        '''
        获取dd之前的某一天合法的数据, 或者None
        '''
        if isinstance(dd, str):
            dd = datetime.datetime.strptime(dd, "%Y/%m/%d")
        while dd > self.min_day:
            dd -= datetime.timedelta(days=1)
            if self._valid_dd(dd):
                return dd
        return None

    def _get_week_dd(self, dd):
        if isinstance(dd, str):
            dd = datetime.datetime.strptime(dd, "%Y/%m/%d")
        current_week = dd.isocalendar()[1]
        while dd > self.min_day:
            week = dd.isocalendar()[1]
            if week != current_week:
                break
            if self._valid_dd(dd):
                return dd
            dd -= datetime.timedelta(days=1)
        return None

    
    def _get_previous_week_dd(self, dd):
        if isinstance(dd, str):
            dd = datetime.datetime.strptime(dd, "%Y/%m/%d")
        current_week = dd.isocalendar()[1]
        while dd > self.min_day:
            dd -= datetime.timedelta(days=1)
            week = dd.isocalendar()[1]
            if week != current_week and self._valid_dd(dd):
                return dd
        return None


    def _get_month_dd(self, dd):
        if isinstance(dd, str):
            dd = datetime.datetime.strptime(dd, "%Y/%m/%d")
        current_month = dd.month
        while dd > self.min_day:
            month = dd.month
            if current_month != month:
                break
            if self._valid_dd(dd):
                return dd
            dd -= datetime.timedelta(days=1)
        return None
        
    
    def _get_previous_month_dd(self, dd):
        if isinstance(dd, str):
            dd = datetime.datetime.strptime(dd, "%Y/%m/%d")
        dd = dd.replace(day=1) - datetime.timedelta(days=1)
        while dd > self.min_day:
            if self._valid_dd(dd):
                return dd
            dd -= datetime.timedelta(days=1)
        return None


    def _valid_dd(self, dd):
        if isinstance(dd, str):
            return dd in self.valid_days
        if isinstance(dd, datetime.datetime):
            return dd.strftime("%Y/%m/%d") in self.valid_days
        raise Exception("unknown dd type.")
        
        
    def _calc_ma(self, year=None, month=None, day=None, c=None, cycle=None):
        assert c in [5, 10, 20, 60, 120, 250]
        assert cycle in ['day', 'week', 'month']
        datas = []
        if cycle == 'day':
            dd = datetime.datetime(year, month, day)
            i = 0
            while i < c and dd:
                if self._valid_dd(dd):
                    datas.insert(0, self._get_c_close(dd))
                    i += 1
                dd = self._get_previous_valid_dd(dd)
        elif cycle == 'week':
            dd = self._get_week_dd(datetime.datetime(year, month, day))
            if not dd:
                dd = self._get_previous_week_dd(dd)
            i = 0
            while i < c and dd:
                if self._valid_dd(dd):
                    datas.insert(0, self._get_c_close(dd))
                    i += 1
                dd = self._get_previous_week_dd(dd)
        else:
            dd = self._get_month_dd(datetime.datetime(year, month, day))
            if not dd:
                dd = self._get_previous_month_dd(datetime.datetime(year, month, day))
            i = 0
            while i < c and dd:
                if self._valid_dd(dd):
                    datas.insert(0, self._get_c_close(dd))
                    i += 1
                dd = self._get_previous_month_dd(dd)
        if len(datas) != c:
            return ''
        return str(round(sum([float(i) for i in datas]) / c, 2))
    
            
            
    def _calc_kdj(self):
        pass

    def _calc_boll(self):
        pass

    def _calc_macd(self):
        pass
    

    def calc_ma5_of_day(self, year, month, day):
        return self._calc_ma(year=year, month=month, day=day, c=5, cycle="day")

    def calc_ma10_of_day(self, year, month, day):
        return self._calc_ma(year=year, month=month, day=day, c=10, cycle="day")

    def calc_ma20_of_day(self, year, month, day):
        return self._calc_ma(year=year, month=month, day=day, c=20, cycle="day")

    def calc_ma60_of_day(self, year, month, day):
        return self._calc_ma(year=year, month=month, day=day, c=60, cycle="day")    

    def calc_ma120_of_day(self, year, month, day):
        return self._calc_ma(year=year, month=month, day=day, c=120, cycle="day")    

    def calc_ma250_of_day(self, year, month, day):
        return self._calc_ma(year=year, month=month, day=day, c=250, cycle="day")    

    
    def calc_ma5_of_week(self, year, month, day):
        return self._calc_ma(year=year, month=month, day=day, c=5, cycle="week")

    def calc_ma10_of_week(self, year, month, day):
        return self._calc_ma(year=year, month=month, day=day, c=10, cycle="week")

    def calc_ma20_of_week(self, year, month, day):
        return self._calc_ma(year=year, month=month, day=day, c=20, cycle="week")

    def calc_ma60_of_week(self, year, month, day):
        return self._calc_ma(year=year, month=month, day=day, c=60, cycle="week")

    def calc_ma120_of_week(self, year, month, day):
        return self._calc_ma(year=year, month=month, day=day, c=120, cycle="week")

    def calc_ma250_of_week(self, year, month, day):
        return self._calc_ma(year=year, month=month, day=day, c=250, cycle="week")

    
    def calc_ma5_of_month(self, year, month, day):
        return self._calc_ma(year=year, month=month, day=day, c=5, cycle="month")

    def calc_ma10_of_month(self, year, month, day):
        return self._calc_ma(year=year, month=month, day=day, c=10, cycle="month")

    def calc_ma20_of_month(self, year, month, day):
        return self._calc_ma(year=year, month=month, day=day, c=20, cycle="month")

    def calc_ma60_of_month(self, year, month, day):
        return self._calc_ma(year=year, month=month, day=day, c=60, cycle="month")
    
    def calc_ma120_of_month(self, year, month, day):
        return self._calc_ma(year=year, month=month, day=day, c=120, cycle="month")

    def calc_ma250_of_month(self, year, month, day):
        return self._calc_ma(year=year, month=month, day=day, c=250, cycle="month")

    
    
    
    
if __name__ == "__main__":
    t = Traning()

    if len(sys.argv) >= 4:
        year, month, day = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    else:
        year, month, day = 2015, 9, 1
    print t.calc_ma5_of_day(year, month, day)
    print t.calc_ma10_of_day(year, month, day)
    print t.calc_ma20_of_day(year, month, day)
    print t.calc_ma60_of_day(year, month, day)
    print t.calc_ma120_of_day(year, month, day)
    print t.calc_ma250_of_day(year, month, day)

    print 
    
    print t.calc_ma5_of_week(year, month, day)
    print t.calc_ma10_of_week(year, month, day)
    print t.calc_ma20_of_week(year, month, day)
    print t.calc_ma60_of_week(year, month, day)
    print t.calc_ma120_of_week(year, month, day)
    print t.calc_ma250_of_week(year, month, day)

    print
    
    print t.calc_ma5_of_month(year, month, day)
    print t.calc_ma10_of_month(year, month, day)
    print t.calc_ma20_of_month(year, month, day)
    print t.calc_ma60_of_month(year, month, day)
    print t.calc_ma120_of_month(year, month, day)
    print t.calc_ma250_of_month(year, month, day)

