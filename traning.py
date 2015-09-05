#!/usr/bin/env python
#-*- coding:utf-8 -*-

import datetime
import sys
import math

class Traning:

    def assert_test(self):
        days = []
        test_day = self.valid_days[-1]
        while test_day:
            days.insert(0, test_day)
            test_day = self._get_previous_day(test_day)
        weeks = []
        test_week = self.valid_weeks[-1]
        while test_week:
            weeks.insert(0, test_week)
            test_week = self._get_previous_week(test_week)
        months = []
        test_month = self.valid_months[-1]
        while test_month:
            months.insert(0, test_month)
            test_month = self._get_previous_month(test_month)

        assert days == self.valid_days
        assert weeks == self.valid_weeks
        assert months == self.valid_months

        
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
        d["date"] = datetime.datetime.strptime(d["date"], "%Y/%m/%d").strftime("%Y/%m/%d")
        return {d["date"]: d}

    
    def _init_data(self):
        with open(self.day_file) as fp:
            for line in fp:
                values = line.rstrip().split(";")
                if self.header is None:
                    self.col_width = len(values)
                    self.header = line.rstrip()
                else:
                    assert len(values) == self.col_width
                    self.day_datas.update(self._line_to_dict(values))
                    
        self.header = None
        self.col_width = None
        with open(self.week_file) as fp:
            for line in fp:
                values = line.rstrip().split(";")
                if self.header is None:
                    self.col_width = len(values)
                    self.header = line.rstrip()
                else:
                    assert len(values) == self.col_width
                    self.week_datas.update(self._line_to_dict(values))

        self.header = None
        self.col_width = None
        with open(self.month_file) as fp:
            for line in fp:
                values = line.rstrip().split(";")
                if self.header is None:
                    self.col_width = len(values)
                    self.header = line.rstrip()
                else:
                    assert len(values) == self.col_width
                    self.month_datas.update(self._line_to_dict(values))
                    

    def _init_ema(self):
        # 第一天等于close
        for keys, datas in [(self.valid_days, self.day_datas),
                            (self.valid_weeks, self.week_datas),
                            (self.valid_months, self.month_datas)]:
            for i in xrange(0, len(keys)):
                k = keys[i]
                c_close = float(datas[k]["c.close"])
                if i == 0:
                    datas[k]["ema12"] = c_close
                    datas[k]["ema26"] = c_close
                else:
                    previous_k = keys[i-1]
                    previous_ema12 = datas[previous_k]["ema12"]
                    previous_ema26 = datas[previous_k]["ema26"]
                    datas[k]["ema12"] = 11.0/13 * previous_ema12 + 2.0 / 13 * c_close
                    datas[k]["ema26"] = 25.0/27 * previous_ema26 + 2.0 / 27 * c_close
                    
                
    def __init__(self, day_file="day.csv", week_file="week.csv", month_file="month.csv"):
        self.day_datas = {}
        self.week_datas = {}
        self.month_datas = {}
        self.day_file = day_file
        self.week_file = week_file
        self.month_file = month_file
        self.col_width = None
        self.header = None
        self._init_data()
        self.valid_days = sorted(self.day_datas.keys())
        self.valid_weeks = sorted(self.week_datas.keys())
        self.valid_months = sorted(self.month_datas.keys())
        self._init_ema()
        self.min_day = self.valid_days[0]
        self.max_day = self.valid_days[-1]
        self.min_week = self.valid_weeks[0]
        self.max_week = self.valid_weeks[-1]
        self.min_month = self.valid_months[0]
        self.max_month = self.valid_months[-1]


    def _get_c_close(self, dd, cycle='day'):
        assert cycle in ['day', 'week', 'month']
        if isinstance(dd, datetime.datetime):
            dd = dd.strftime("%Y/%m/%d")
        if cycle == 'day':
            datas = self.day_datas
        elif cycle == 'week':
            datas = self.week_datas
        else:
            datas = self.month_datas
        return float(datas[dd]["c.close"])

    def _get_ma(self, dd, c, cycle='day'):
        assert cycle in ['day', 'week', 'month']
        assert c in [5, 10, 20, 60, 120, 250]
        if isinstance(dd, datetime.datetime):
            dd = dd.strftime("%Y/%m/%d")
        if cycle == 'day':
            datas = self.day_datas
        elif cycle == 'week':
            datas = self.week_datas
        else:
            datas = self.month_datas
        return float(datas[dd]["ma%s" % c])
        
    def _get_high_and_low(self, dd, cycle='day', c=9):
        assert cycle in ['day', 'week', 'month']
        if isinstance(dd, datetime.datetime):
            dd = dd.strftime("%Y/%m/%d")
        if cycle == 'day':
            idx = self.valid_days.index(dd)
            keys = self.valid_days
            datas = self.day_datas
        elif cycle == 'week':
            idx = self.valid_weeks.index(dd)
            keys = self.valid_weeks
            datas = self.week_datas
        else:
            idx = self.valid_months.index(dd)
            keys = self.valid_months
            datas = self.month_datas
        high, low = None, None
        while c > 0:
            dd = keys[idx]
            c_high, c_low = float(datas[dd]["c.high"]), float(datas[dd]["c.low"])
            if high is None:
                high, low = c_high, c_low
            else:
                if c_high > high:
                    high = c_high
                if c_low < low:
                    low = c_low    
            c -= 1
            idx = idx - 1
        return high, low
            

    def _get_kdj(self, dd, cycle='day'):
        assert cycle in ['day', 'week', 'month']
        if isinstance(dd, datetime.datetime):
            dd = dd.strftime("%Y/%m/%d")
        if cycle == 'day':
            datas = self.day_datas
        elif cycle == 'week':
            datas = self.week_datas
        else:
            datas = self.month_datas
        return float(datas[dd]["kdj.k"]), float(datas[dd]["kdj.d"])

    
    def _bsearch(self, k, sorted_list):
        '''
        返回index, 最后一个小于k
        '''
        if not sorted_list:
            return None
        if k <= sorted_list[0]:
            return None
        if sorted_list[-1] < k:
            return len(sorted_list) - 1
        left, right = 0, len(sorted_list) - 1
        while left <= right:
            mid = (left + right)/2
            if k <= sorted_list[mid]:
                right = mid - 1
            else:
                # sorted_list[mid] < k
                if sorted_list[mid+1] >= k:
                    return mid
                else:
                    left = mid + 1
        return left
            
            
    def _get_previous_day(self, dd):
        '''
        获取dd之前的某一天合法的数据, 或者None
        '''
        if isinstance(dd, datetime.datetime):
            dd = datetime.datetime.strftime(dd, "%Y/%m/%d")
        if dd <= self.min_day:
            return None
        if self._valid_day(dd):
            idx = self.valid_days.index(dd) - 1
        else:
            idx = self._bsearch(dd, self.valid_days)
        if idx < 0:
            return None
        return self.valid_days[idx]


    def _get_previous_week(self, dd):
        '''
        获取dd之前的某一天合法的数据, 或者None
        '''
        if isinstance(dd, datetime.datetime):
            dd = datetime.datetime.strftime(dd, "%Y/%m/%d")
        if dd <= self.min_week:
            return None
        if self._valid_week(dd):
            idx = self.valid_weeks.index(dd) - 1
        else:
            idx = self._bsearch(dd, self.valid_weeks)
        if idx < 0:
            return None
        return self.valid_weeks[idx]

    
    def _get_previous_month(self, dd):
        '''
        获取dd之前的某一天合法的数据, 或者None
        '''
        if isinstance(dd, datetime.datetime):
            dd = datetime.datetime.strftime(dd, "%Y/%m/%d")
        if dd <= self.min_month:
            return None
        if self._valid_month(dd):
            idx = self.valid_months.index(dd) - 1
        else:
            idx = self._bsearch(dd, self.valid_months)
        if idx < 0:
            return None
        return self.valid_months[idx]


    def _valid_day(self, dd):
        if isinstance(dd, str):
            return dd in self.valid_days
        if isinstance(dd, datetime.datetime):
            return dd.strftime("%Y/%m/%d") in self.valid_days
        raise Exception("unknown dd type.")


    def _valid_week(self, dd):
        if isinstance(dd, str):
            return dd in self.valid_weeks
        if isinstance(dd, datetime.datetime):
            return dd.strftime("%Y/%m/%d") in self.valid_weeks
        raise Exception("unknown dd type.")


    def _valid_month(self, dd):
        if isinstance(dd, str):
            return dd in self.valid_months
        if isinstance(dd, datetime.datetime):
            return dd.strftime("%Y/%m/%d") in self.valid_months
        raise Exception("unknown dd type.")
    

    def _calc_ma(self, year=None, month=None, day=None, c=None, cycle=None):
        assert c in [5, 10, 20, 60, 120, 250, 12, 26, 9]
        assert cycle in ['day', 'week', 'month']
        datas = []
        if cycle == 'day':
            dd = datetime.datetime(year, month, day)
            i = 0
            while i < c and dd:
                if self._valid_day(dd):
                    datas.insert(0, self._get_c_close(dd))
                    i += 1
                dd = self._get_previous_day(dd)
        elif cycle == 'week':
            dd = datetime.datetime(year, month, day)
            if not self._valid_week(dd):
                dd = self._get_previous_week(dd)
            i = 0
            while i < c and dd:
                if self._valid_week(dd):
                    datas.insert(0, self._get_c_close(dd))
                    i += 1
                dd = self._get_previous_week(dd)
        else:
            dd = datetime.datetime(year, month, day)
            if not self._valid_month(dd):
                dd = self._get_previous_month(dd)
            i = 0
            while i < c and dd:
                if self._valid_day(dd):
                    datas.insert(0, self._get_c_close(dd))
                    i += 1
                dd = self._get_previous_month(dd)
        if len(datas) != c:
            return ''
        return round(sum([float(i) for i in datas]) / c, 2)
    
            
    def _calc_kdj(self, year=None, month=None, day=None, cycle=None):
        assert cycle in ['day', 'week', 'month']
        dd = datetime.datetime(year, month, day)
        if cycle == 'day':
            if not self._valid_day(dd):
                dd = self._get_previous_day(dd)
            previous_dd = self._get_previous_day(dd)
        elif cycle == 'week':
            if not self._valid_week(dd):
                dd = self._get_previous_week(dd)
            previous_dd = self._get_previous_week(dd)
        else:
            if not self._valid_month(dd):
                dd = self._get_previous_month(dd)
            previous_dd = self._get_previous_month(dd)
        print dd, previous_dd
        c_close = self._get_c_close(dd, cycle)
        c_high, c_low = self._get_high_and_low(dd, cycle=cycle, c=9)
        rsv = (1.0 * (c_close - c_low) / (c_high - c_low)) * 100
        previous_k, previous_d = self._get_kdj(previous_dd, cycle=cycle)
        k = round(previous_k * 2/3.0 + rsv/3.0, 2)
        d = round(previous_d * 2/3.0 + k/3.0, 2)
        j = round(3*k - 2*d, 2)
        return k, d, j
        

    def _calc_boll(self, year=None, month=None, day=None, cycle=None):
        '''
        N取20, k取
        '''
        N, k = 20, 2
        assert cycle in ['day', 'week', 'month']
        dd = datetime.datetime(year, month, day)
        if cycle == 'day':
            if not self._valid_day(dd):
                dd = self._get_previous_day(dd)
        elif cycle == 'week':
            if not self._valid_week(dd):
                dd = self._get_previous_week(dd)
        else:
            if not self._valid_month(dd):
                dd = self._get_previous_month(dd)
        dds = [dd]
        for i in xrange(1, N):
            if cycle == 'day':
                previous_dd = self._get_previous_day(dds[0])
            elif cycle == 'week':
                previous_dd = self._get_previous_week(dds[0])
            else:
                previous_dd = self._get_previous_month(dds[0])
            dds.insert(0, previous_dd)
        c_closes = [self._get_c_close(i, cycle=cycle) for i in dds]
        ma = self._get_ma(dds[-1], c=N, cycle=cycle)
        mb = self._get_ma(dds[-2], c=N, cycle=cycle)
        md = math.sqrt(sum([(c_close - ma)*(c_close-ma) for c_close in c_closes])*1.0/N)
        up = round(mb + 2 * md, 2)
        dn = round(mb - 2 * md, 2)
        return ma, up, dn

                          
    def calc_boll_of_day(self, year=None, month=None, day=None):
        return self._calc_boll(year, month, day, "day")

    def calc_boll_of_week(self, year=None, month=None, day=None):
        return self._calc_boll(year, month, day, "week")

    def calc_boll_of_month(self, year=None, month=None, day=None):
        return self._calc_boll(year, month, day, "month")

    
    def _calc_macd(self, year=None, month=None, day=None, cycle=None):
        assert cycle in ['day', 'week', 'month']
        dd = datetime.datetime(year, month, day).strftime("%Y/%m/%d")
        if cycle == 'day':
            if not self._valid_day(dd):
                dd = self._get_previous_day(dd)
            previous_dd = self._get_previous_day(dd)
            datas = self.day_datas
        elif cycle == 'week':
            if not self._valid_week(dd):
                dd = self._get_previous_week(dd)
            previous_dd = self._get_previous_week(dd)
            datas = self.week_datas
        else:
            if not self._valid_month(dd):
                dd = self._get_previous_month(dd)
            previous_dd = self._get_previous_month(dd)
            datas = self.month_datas

        c_close = self._get_c_close(dd)
        ema12 = datas[dd]["ema12"]
        ema26 = datas[dd]["ema26"]
        diff = round(ema12 - ema26, 2)
        previous_dea = round(float(datas[previous_dd]["macd.dea"]), 2)
        dea = round(previous_dea * 8.0 / 10 + diff * 2.0 / 10, 2)
        bar = round(2 * (diff - dea), 2)
        return diff, dea, bar


    def calc_macd_of_day(self, year=None, month=None, day=None):
        return self._calc_macd(year, month, day, "day")

    def calc_macd_of_week(self, year=None, month=None, day=None):
        return self._calc_macd(year, month, day, "week")

    def calc_macd_of_month(self, year=None, month=None, day=None):
        return self._calc_macd(year, month, day, "month")
    
    
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


    def calc_kdj_of_day(self, year, month, day):
        return self._calc_kdj(year, month, day, cycle="day")
    
    def calc_kdj_of_week(self, year, month, day):
        return self._calc_kdj(year, month, day, cycle="week")

    def calc_kdj_of_month(self, year, month, day):
        return self._calc_kdj(year, month, day, cycle="month")
    
    
    
    
if __name__ == "__main__":
    t = Traning()

    # t.assert_test()
    print 'assert test ok.'
    
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

    print
    print t.calc_kdj_of_day(year, month, day)
    print t.calc_kdj_of_week(year, month, day)
    print t.calc_kdj_of_month(year, month, day)

    print 
    print t.calc_macd_of_day(year, month, day)
    print t.calc_macd_of_week(year, month, day)
    print t.calc_macd_of_month(year, month, day)
    
    print
    print t.calc_boll_of_day(year, month, day)
    print t.calc_boll_of_week(year, month, day)
    print t.calc_boll_of_month(year, month, day)
    
