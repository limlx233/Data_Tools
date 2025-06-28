from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import random
import numpy as np

# 数据库连接配置
DB_URL = "mysql+pymysql://penna_a:mf6L1sOj64aQggUK@mysql2.sqlpub.com:3307/penna_a"
engine = create_engine(DB_URL, echo=True)
Base = declarative_base()