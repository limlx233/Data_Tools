import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.pyplot as plt

def load_file(files):
    xlsx = pd.ExcelFile(files)
    all_sheet_names = xlsx.sheet_names
    # 筛选出包含“线”字的表名
    line_sheet_names = [sheet_name for sheet_name in all_sheet_names if '线' in sheet_name]

    # 用于存储每个工作表对应 DataFrame 的列表
    dfs = []
    cols_to_keep = ['日期','产线','班级','香型','规格','批号','产量定额','产量合计']
    # 遍历筛选后的表名
    for sheet_name in line_sheet_names:
        # 读取当前工作表数据
        df = xlsx.parse(sheet_name)
        # 添加新列“产线”，其值为当前工作表名
        df['产线'] = sheet_name
        df = df[cols_to_keep]
        df = df.dropna(subset=['日期','产量定额'])
        # 将批号列转换为字符串类型
        df['批号'] = df['批号'].astype(str)
        # 筛选 12小时的 "大班"
        condition = df['班级'].str.startswith('大')
        # 根据条件更新产量定额列
        df.loc[condition, '产量定额'] = df.loc[condition, '产量定额'] * 1.5
        # 将处理后的 DataFrame 添加到列表中
        dfs.append(df)
    if dfs:
        combined_df = pd.concat(dfs, ignore_index=True)
        return combined_df
    else:
        return None


def calculate_result(df):
    result = df.groupby('产线').agg({'产量合计': 'sum','产量定额': 'sum' }).reset_index()
    result['产能负荷率'] = result['产量合计'] / result['产量定额']
    # 将产能负荷率转换为百分比格式
    result['产能负荷率'] = result['产能负荷率'].apply(lambda x: '{:.2f}%'.format(x * 100))  
    return result

import matplotlib.font_manager as fm

# 添加字体搜索路径
font_path = "font/MSYH.TTC"
fm.fontManager.addfont(font_path)
# 设置使用该字体
plt.rcParams['font.family'] = 'Microsoft YaHei'  # 替换为字体的名称
# 设置 matplotlib 支持中文显示
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

def plot_production_line_load_rate(df, mon,line_column='产线', load_rate_column='产能负荷率'):
    # 将包含百分比的字符串转换为浮点数
    df[load_rate_column] = df[load_rate_column].str.rstrip('%').astype(float) / 100
    # 设置图片清晰度
    plt.rcParams['figure.dpi'] = 300
    # 创建一个图形对象
    plt.figure(figsize=(10, 6))
    # 使用 seaborn 绘制柱形图
    ax = sns.barplot(x=line_column, y=load_rate_column, data=df)
    # 添加数据标签
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2%}', 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', 
                    fontsize=10, color='black', 
                    xytext=(0, 5), textcoords='offset points')
    # 设置图表标题和坐标轴标签
    plt.title(f'{mon}-各{line_column}{load_rate_column}')
    plt.xlabel(line_column)
    plt.ylabel(load_rate_column)
    # 在 Streamlit 中显示图表
    st.pyplot(plt.gcf())
    plt.close()