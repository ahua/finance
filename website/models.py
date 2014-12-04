#!/usr/bin/env python
#-*- coding: utf-8 -*-
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean

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

_engine = _Session = None    
def create_session():
    global _engine, _Session
    if not _engine or not _Session:
        _engine = create_engine('mysql+mysqldb://admin:admin@localhost:3306/finance?charset=utf8',
                                encoding="utf8",
                                echo=True,
                                pool_size=5,
                                pool_recycle=10)
        MysqlBase.metadata.create_all(_engine)
        _Session = sessionmaker()
        _Session.configure(bind=_engine)
        
    return _Session()


if __name__ == "__main__":
    session = create_session()
    session.close()
    
