# from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, ForeignKey, TIMESTAMP
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# import random
# import numpy as np

# # 数据库连接配置
# DB_URL = "mysql+pymysql://penna_a:mf6L1sOj64aQggUK@mysql2.sqlpub.com:3307/penna_a"
# engine = create_engine(DB_URL, echo=True)
# Base = declarative_base()

# # 定义数据库模型类
# class ProductCategory(Base):
#     __tablename__ = 'product_categories'
#     category_id = Column(Integer, primary_key=True)
#     category_name = Column(String(50), unique=True)
#     category_color = Column(String(20))

# class QuarterlySales(Base):
#     __tablename__ = 'quarterly_sales'
#     quarter_id = Column(Integer, primary_key=True)
#     quarter = Column(String(10))
#     total_sales = Column(Integer)
#     create_time = Column(TIMESTAMP)

# class ProductSales(Base):
#     __tablename__ = 'product_sales'
#     sales_id = Column(Integer, primary_key=True)
#     category_id = Column(Integer, ForeignKey('product_categories.category_id'))
#     quarter_id = Column(Integer, ForeignKey('quarterly_sales.quarter_id'))
#     sales_volume = Column(Integer)
#     revenue = Column(Integer)
#     growth_rate = Column(DECIMAL(5,2))

# class MonthlySalesTrend(Base):
#     __tablename__ = 'monthly_sales_trend'
#     trend_id = Column(Integer, primary_key=True)
#     category_id = Column(Integer, ForeignKey('product_categories.category_id'))
#     sales_month = Column(String(7))
#     sales_volume = Column(Integer)

# # 初始化数据库表
# Base.metadata.create_all(engine)

# # 生成模拟数据并插入数据库
# Session = sessionmaker(bind=engine)
# session = Session()

# # 固定随机种子
# random.seed(42)
# np.random.seed(42)

# # 产品类别数据
# categories = [
#     ('智能手机', '#c23531'),
#     ('笔记本电脑', '#2f4554'),
#     ('平板电脑', '#61a0a8'),
#     ('智能手表', '#d48265'),
#     ('耳机', '#91c7ae'),
#     ('智能家居', '#749f83')
# ]

# # 插入产品类别
# for cat in categories:
#     category = ProductCategory(
#         category_name=cat[0],
#         category_color=cat[1]
#     )
#     session.add(category)
# session.commit()

# # 获取类别ID映射
# category_map = {row.category_name: row.category_id for row in session.query(ProductCategory).all()}

# # 季度数据
# quarters = ['Q1', 'Q2', 'Q3', 'Q4']
# quarter_ids = {}

# # 插入季度数据并获取ID
# for q in quarters:
#     quarterly_sales = QuarterlySales(
#         quarter=q,
#         total_sales=random.randint(5000, 10000)
#     )
#     session.add(quarterly_sales)
# session.commit()
# quarter_ids = {row.quarter: row.quarter_id for row in session.query(QuarterlySales).all()}

# # 插入产品销售明细
# for q in quarters:
#     q_id = quarter_ids[q]
#     for cat in category_map:
#         cat_id = category_map[cat]
#         sales = ProductSales(
#             category_id=cat_id,
#             quarter_id=q_id,
#             sales_volume=random.randint(500, 2000),
#             revenue=random.randint(50000, 200000),
#             growth_rate=round(random.uniform(-0.1, 0.3), 2)
#         )
#         session.add(sales)
# session.commit()

# # 插入月度趋势数据
# months = [f'2023-{str(m).zfill(2)}' for m in range(1, 13)]
# for cat in category_map:
#     cat_id = category_map[cat]
#     for m in months:
#         trend = MonthlySalesTrend(
#             category_id=cat_id,
#             sales_month=m,
#             sales_volume=random.randint(200, 1200)
#         )
#         session.add(trend)
# session.commit()

# session.close()
# print("数据初始化完成！")