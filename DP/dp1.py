# @ Author: Penna_Wld
# @ Create Time: 2025-06-30 16:00:24
# @ Modified by: Penna_Wld
# @ Modified time: 2025-06-30 16:00:28
# @ Description: page1 中物料耗用数据统计的数据处理功能


from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from typing import List, Dict, Any, Optional
import pandas as pd
import streamlit as st
from datetime import datetime
from io import BytesIO


db_credentials = st.secrets["sqlpub"]
usr = db_credentials['user']
pwd = db_credentials['password']
host = db_credentials['host']
port = db_credentials['port']
database = db_credentials['database']

# 使用你提供的实际数据库连接字符串
DB_URL = f"mysql+pymysql://{usr}:{pwd}@{host}:{port}/{database}"

def create_mysql_engine() -> create_engine:
    engine = create_engine(DB_URL, pool_pre_ping=True)  # 直接使用全局变量
    return engine

def execute_query(engine: create_engine, query: str) -> pd.DataFrame:
    """
    执行 SQL 查询并以 DataFrame 格式返回结果
    
    参数:
        engine: SQLAlchemy 数据库引擎
        query: SQL 查询语句
    
    返回:
        查询结果的 DataFrame
    """
    with sessionmaker(bind=engine)() as session:
        try:
            result = session.execute(text(query))
            return pd.DataFrame(result.fetchall(), columns=result.keys())
        except Exception as e:
            session.rollback()
            error_msg = f"查询执行失败: {str(e)}"
            st.error(error_msg)  # 适用于Streamlit应用，普通Python应用可改为print
            raise
        finally:
            session.close()


def check_data_update_status(df):
    """
    检查数据更新状态
    
    参数:
    df -- 包含'UpdateDate'列的DataFrame
    
    功能:
    计算DataFrame中日期与当前日期的相隔天数，
    如果相隔天数大于27天则打印警告信息，否则打印确认信息
    """
    # 确保DataFrame中有UpdateDate列
    if 'UpdateDate' not in df.columns:
        print("错误：DataFrame中缺少'UpdateDate'列")
        return
    
    # 获取当前日期
    current_date = datetime.now().date()
    
    # 提取DataFrame中的日期
    update_date = df['UpdateDate'].iloc[0]
    
    try:
        # 计算日期差
        delta = current_date - update_date
        days_diff = delta.days
        
        # 根据条件打印结果
        if days_diff > 27:
            with st.container(border=True):
                st.warning(f"注意：产品分类数据最近一次更新时间较远, 时间为:{update_date}")
        else:
            with st.container():
                st.warning(f"注意：产品分类数据为近期更新, 时间为:{update_date}")
            
    except ValueError as e:
        print(f"日期格式错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")



def reset_columns(df):
    '''
    用于处理从Excel读取到的dataframe的字段列是由两行合并而来，重置其列名
    '''
    # 遍历第一行的数据
    for i, value in enumerate(df.iloc[0]):
        if pd.notna(value):  # 如果第一行的值非空
            df.columns.values[i] = value  # 替换原来的列名
    # 删除第一行
    df = df.drop(df.index[0])
    # 重置索引（可选）
    df = df.reset_index(drop=True)
    return df

# 使用缓存来存储处理后的 DataFrame
@st.cache_data
def load_excel_files(uploaded_files):
    dfs = {}
    for uploaded_file in uploaded_files:
        df = pd.read_excel(uploaded_file, header=20) # 第21行开始作为表头
        df = reset_columns(df)
        dfs[uploaded_file.name] = df
    return dfs


# 使用缓存来存储处理后的数据
@st.cache_data
def process_data(dfs):
    df_lst = []
    for df in dfs.values():
        df = df.dropna(subset=['单位(主)', '创建人', '创建日期'])
        # 对关键列进行保留
        cols_to_keep = ['库存', '物料编码', '物料说明', '批号', '数量(主)', '单位(主)',
                        '创建日期', '来源类型','交易类型', '交易日期', '原因代码说明']
        df = df[cols_to_keep]
        df = df[(df['交易类型'].isin(['.发料到生产批WIP Issue','.从生产批退料到仓库WIP Return']))]
        df_lst.append(df)
    df_all = pd.concat(df_lst, axis=0)
    return df_all

# 将 Pandas DataFrame 对象转换为 Excel 文件格式的字节流
@st.cache_resource
def to_excel(df1, df3 ,df2,sheet_name1='物料',sheet_name3='成品',sheet_name2='异常类别定义'):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    df2.to_excel(writer, index=False, header=False,sheet_name=sheet_name2)
    df1.to_excel(writer, index=False, sheet_name=sheet_name1)
    df3.to_excel(writer, index=False, sheet_name=sheet_name3)




