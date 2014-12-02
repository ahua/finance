from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random

engine = create_engine('mysql+mysqldb://admin:admin@127.0.0.1:3306/finance?charset=utf8',
                       encoding="utf8",
                       echo=True,
                       pool_size=5,
                       pool_recycle=10)
MysqlBase.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

session.close()

