#!/usr/bin/env python
#-*- coding: utf-8 -*-
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.sql import func

MysqlBase = declarative_base()

__all__ = ['Category', 'Area', 'Stock', 'DailyData', 'create_session']

class Category(MysqlBase):
    __tablename__ = 'category'
    id = Column(Integer, nullable=False, autoincrement=False, primary_key=True)
    pid = Column(Integer, nullable=False)
    name = Column(String(30), nullable=False)
    is_leaf_node = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now)

    @classmethod
    def get_all_leaf_cat(cls, pid_list, session):
        id_list = []
        while pid_list:
            tmp_pid_list = []
            _qs = session.query(cls).filter(cls.pid.in_(pid_list))
            for o in _qs:
                # pid == id
                if not o.is_leaf_node and o.id in pid_list:
                    continue
                if o.is_leaf_node:
                    id_list.append(o.id)
                else:
                    tmp_pid_list.append(o.id)
            pid_list = tmp_pid_list
        return id_list

    @classmethod
    def get_all_top_cat(cls, session):
        _qs = session.query(cls).filter(cls.pid==cls.id)
        return _qs


class Area(MysqlBase):
    __tablename__ = 'area'
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    name = Column(String(30), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now)


class Stock(MysqlBase):
    __tablename__ = 'stock'
    code = Column(String(6), nullable=False, autoincrement=False, primary_key=True)
    category_id = Column(Integer, nullable=False)
    area_id = Column(Integer, nullable=False)
    name = Column(String(30), nullable=False)
    market_day = Column(String(6), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now)

    @classmethod
    def get_all_stock(cls, cat_list, session):
        _qs = session.query(cls).filter(cls.category_id.in_(cat_list))
        return _qs

    
class DailyData(MysqlBase):
    __tablename__ = 'daily_data'
    day = Column(String(8), nullable=False, autoincrement=False, primary_key=True)
    code = Column(String(6), nullable=False, autoincrement=False, primary_key=True)
    p_open = Column(Float, nullable=True)
    p_close = Column(Float, nullable=True)
    p_high = Column(Float, nullable=True)
    p_low = Column(Float, nullable=True)
    p_inc = Column(Float, nullable=True)
    p_earning_ratio = Column(Float, nullable=True)
    trade_count = Column(Integer, nullable=True)       
    trade_money = Column(Float, nullable=True)   # 单位：亿
    market_value = Column(Float, nullable=True)  # 单位：亿
    is_suspend_trading = Column(Boolean, nullable=False) # 停牌?    

    @classmethod
    def get_daily_data(cls, code_list, day, session):
        _qs = session.query(cls).filter(cls.day==day, cls.code.in_(code_list))
        return _qs

    @classmethod
    def get_sum_column(cls, code_list, day, column, session):
        _qs = session.query(func.sum(column)).filter(cls.day==day, cls.code.in_(code_list)).all()
        return round(_qs[0][0], 2)

    @classmethod
    def get_latest_day(cls, session):
        _qs = session.query(cls.day).distinct().all()
        
        # _qs = [(u'20141202',), (u'20141204',), (u'20141205',)]
        return _qs[-1][0]
        


class Chinese(MysqlBase):
    __tablename__ = 'chinese'
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    title = Column(String(100), nullable=False)
    author = Column(String(30), nullable=True)
    content = Column(String(10000), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now)
    

_engine = _Session = None    
def create_session():
    global _engine, _Session
    if not _engine or not _Session:
        _engine = create_engine('mysql+mysqldb://admin:admin@localhost:3306/finance?charset=utf8',
                                encoding="utf8",
                                echo=False,
                                pool_size=5,
                                pool_recycle=10)
        MysqlBase.metadata.create_all(_engine)
        _Session = sessionmaker()
        _Session.configure(bind=_engine)
        
    return _Session()


if __name__ == "__main__":
    session = create_session()
    session.close()
    
