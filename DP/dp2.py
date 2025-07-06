# @ Author: Penna_Wld
# @ Create Time: 2025-07-03 16:25:48
# @ Modified by: Penna_Wld
# @ Modified time: 2025-07-03 16:25:51
# @ Description: 用于 Page3 数据处理

import numpy as np
import pandas as pd
import streamlit as st
from DP import dp1


# 使用缓存来存储处理后的 DataFrame
@st.cache_data
def load_excel_file1(uploaded_file):
    df = pd.read_excel(uploaded_file, header=2) # 第3行作为表头
    df['配料/产品ID'] = df['配料/产品ID'].astype(str) # 确保物料编码列是字符串格式
    return df

@st.cache_data
def load_excel_file2(uploaded_file2):
    df = pd.read_excel(uploaded_file2, header=20) # 第21行开始作为表头
    df = df.copy()
    # # 处理可能的空列名
    df = dp1.reset_columns(df)
    df.columns = df.columns.astype(str)  # 确保所有列名是字符串
    return df

def convert_unit(unit_text, quantity_list, df):
    """
    根据单位字段转换数量值
    
    参数:
    unit_text (str): 单位字段的列名
    quantity_list (list): 待计算数量的列名列表
    df (pd.DataFrame): 数据源DataFrame
    
    返回:
    pd.DataFrame: 转换后的DataFrame
    """
    # 复制原始数据避免修改
    result_df = df.copy()
    # 标记以W开头的单位（处理NaN）
    is_w_unit = result_df[unit_text].fillna('').str.startswith('W')
    # 批量转换数量列（向量化操作）
    for quantity_col in quantity_list:
        # 确保数据类型为数值
        if pd.api.types.is_object_dtype(result_df[quantity_col]):
            result_df[quantity_col] = pd.to_numeric(result_df[quantity_col], errors='coerce')
        # 根据单位标记转换数量
        result_df[f"{quantity_col}"] = np.where(
            is_w_unit, 
            result_df[quantity_col] * 10000, 
            result_df[quantity_col]
        )
    # 处理单位列：移除所有W（根据实际需求调整正则）
    result_df[f"{unit_text}"] = result_df[unit_text].fillna('').str.replace("W", "", regex=False)
    return result_df


def p1(df):
    '''
    处理任务批配料消耗明细表
    '''
    df = df.copy()
    df = df[df['批状态'] != 'WIP'] # 保留已关闭的单据号
    cols_to_keep = ['生产批前缀','单据号','配方名称','生产工序', '配料/产品ID', '配料/产品名称','单位','WIP计划数量', '领料数量', '实际用量']
    df_filter = df[cols_to_keep]
    df_res = convert_unit('单位', ['WIP计划数量', '实际用量'], df_filter)
    return df_res


def p2(df2):
    '''
    处理库存事务处理查询XML
    '''
    df2 = df2.copy()
    df2 = df2.dropna(subset=['数量(主)', '创建人', '创建日期'])
    df2['物料编码'] = df2['物料编码'].astype(str) 
    df2['批号'] = df2['批号'].astype(str) 
    df2 = df2[df2['交易类型'].isin(['.生产批产品完工入库WIP Completion','.生产批产品完工返工WIP Completion Return'])]
    df2['单据号'] = df2['来源名称'].str.extract(r'^([^:]+):', expand=False)
    cols_to_keep2 = ['单据号','物料编码','批号','数量(主)', '单位(主)']
    grouped_df = df2.groupby(['单据号', '物料编码', '批号', '单位(主)'])['数量(主)'].sum().reset_index()
    grouped_df = grouped_df[grouped_df['数量(主)'] > 0 ]
    grouped_df = grouped_df.rename(columns={'物料编码':'产品编码','批号':'入库批号','数量(主)':'产品入库数量' })
    res = convert_unit('单位(主)',['产品入库数量'],grouped_df)
    return res

def classify_materials(df):
    """
    根据MCategory、单位和配料/产品名称对物料进行分类
    
    参数:
    df (pd.DataFrame): 包含物料信息的DataFrame，需包含'配料/产品名称'、'MCategory'和'单位'列
    
    返回:
    pd.DataFrame: 添加了'物料分类'列的DataFrame
    """
    # 复制原始数据避免修改
    result_df = df.copy()
    
    # 定义包材分类函数
    def classify_packaging(name):
        if '纸箱' in name:
            return '纸箱'
        elif '纸盒' in name:
            return '纸盒'
        elif '瓶子' in name:
            return '瓶子'
        elif '瓶盖' in name:
            return '瓶盖'
        elif '泵头' in name:
            return '泵头'
        else:
            return '包材'
    
    # 根据规则创建物料分类列
    result_df['物料分类'] = ''
    
    # 1. MCategory为"产成品"的物料分类为"产成品"
    result_df.loc[result_df['MCategory'] == '产成品', '物料分类'] = '产成品'
    
    # 2. MCategory为"中间产品"的分类处理
    intermediate_mask = result_df['MCategory'] == '中间产品'
    result_df.loc[intermediate_mask & (result_df['单位'] == 'Kg'), '物料分类'] = '膏体'
    result_df.loc[intermediate_mask & (result_df['单位'] != 'Kg'), '物料分类'] = '半成品'
    
    # 3. MCategory为"原辅料"的物料分类为"原辅料"
    result_df.loc[result_df['MCategory'] == '原辅料', '物料分类'] = '原辅料'
    
    # 4. MCategory为"包材"的分类处理
    packaging_mask = result_df['MCategory'] == '包材'
    result_df.loc[packaging_mask, '物料分类'] = result_df.loc[packaging_mask, '配料/产品名称'].apply(classify_packaging)
    
    return result_df


def calculate_loss_rate(df):
    """
    计算不同物料分类的损耗率
    
    参数:
    df (pd.DataFrame): 包含物料信息的DataFrame
    
    返回:
    pd.DataFrame: 添加了损耗率列的DataFrame
    """
    result_df = df.copy()
    
    # 1. 提取单据号中的Spec和BoxSpec信息并计算理论耗用量
    doc_info = df.groupby('单据号').agg({
        'Spec': lambda x: x.loc[x.first_valid_index()] if x.first_valid_index() is not None else 1,
        'BoxSpec': lambda x: x.loc[x.first_valid_index()] if x.first_valid_index() is not None else 1
        }).reset_index()
    
    # 合并单据信息到原DataFrame
    result_df = pd.merge(result_df, doc_info, on='单据号', suffixes=('', '_doc'))
    
    # 2. 初始化计算列
    result_df['理论耗用量'] = 0.0  # 使用float类型
    result_df['损耗率'] = 0.0
    
    # 3. 安全除法函数
    def safe_divide(a, b):
        return np.where(b != 0, a/b, 0)
    
    # 4. 从 secrets.toml 读取密度数据
    density_data = st.secrets["JKH_paste_density"]  
    # 转换为 DataFrame
    df_density = pd.DataFrame.from_dict(density_data, orient='index', columns=['密度'])
    df_density.index.name = 'MCode'
    df_density.reset_index(inplace=True)
    
    # 合并密度数据到结果DataFrame
    result_df = pd.merge(result_df, df_density, on='MCode', how='left')
    # 填充缺失的密度值为1
    result_df['密度'] = result_df['密度'].fillna(1)
    
    # 5. 根据物料分类计算理论耗用量
    # 膏体：Spec_doc * 产品入库数量/1000 * 密度
    mask_cream = result_df['物料分类'] == '膏体'
    result_df.loc[mask_cream, '理论耗用量'] = (
        result_df.loc[mask_cream, 'Spec_doc'] * 
        result_df.loc[mask_cream, '产品入库数量'] / 1000 *
        result_df.loc[mask_cream, '密度']
    )
    
    # 纸箱：产品入库数量 / BoxSpec_doc
    mask_box = result_df['物料分类'] == '纸箱'
    result_df.loc[mask_box, '理论耗用量'] = (
        result_df.loc[mask_box, '产品入库数量'] / 
        result_df.loc[mask_box, 'BoxSpec_doc']
    )
    
    # 其他类别：产品入库数量
    mask_other = ~result_df['物料分类'].isin(['膏体', '纸箱'])
    result_df.loc[mask_other, '理论耗用量'] = result_df.loc[mask_other, '产品入库数量']
    
    # 6. 根据物料分类计算损耗率
    # 膏体和纸箱：(实际用量-理论耗用量)/理论耗用量
    mask_cream_box = result_df['物料分类'].isin(['膏体', '纸箱'])
    result_df.loc[mask_cream_box, '损耗率'] = safe_divide(
        result_df.loc[mask_cream_box, '实际用量'] - 
        result_df.loc[mask_cream_box, '理论耗用量'],
        result_df.loc[mask_cream_box, '理论耗用量']
    )
    
    # 原辅料：(实际用量-WIP计划数量)/WIP计划数量
    mask_raw = result_df['物料分类'] == '原辅料'
    result_df.loc[mask_raw, '损耗率'] = safe_divide(
        result_df.loc[mask_raw, '实际用量'] - 
        result_df.loc[mask_raw, 'WIP计划数量'],
        result_df.loc[mask_raw, 'WIP计划数量']
    )
    
    # 其他类别：(实际用量-产品入库数量)/产品入库数量
    result_df.loc[mask_other, '损耗率'] = safe_divide(
        result_df.loc[mask_other, '实际用量'] - 
        result_df.loc[mask_other, '产品入库数量'],
        result_df.loc[mask_other, '产品入库数量']
    )
    
    # 7. 将损耗率结果保留6位小数点 流式数据写入到 Excel中时 再做格式转化
    result_df['损耗率(%)'] = (result_df['损耗率']).map('{:.6f}'.format)
    
    return result_df
    
# def calculate_loss_rate(df):
#     """
#     计算不同物料分类的损耗率
    
#     参数:
#     df (pd.DataFrame): 包含物料信息的DataFrame
    
#     返回:
#     pd.DataFrame: 添加了损耗率列的DataFrame
#     """
#     result_df = df.copy()
    
#     # 1. 提取单据号中的Spec和BoxSpec信息并计算理论耗用量
#     doc_info = df.groupby('单据号').agg({
#         'Spec': lambda x: x.loc[x.first_valid_index()] if x.first_valid_index() is not None else 1,
#         'BoxSpec': lambda x: x.loc[x.first_valid_index()] if x.first_valid_index() is not None else 1
#         }).reset_index()
    
#     # 合并单据信息到原DataFrame
#     result_df = pd.merge(result_df, doc_info, on='单据号', suffixes=('', '_doc'))
    
#     # 2. 根据物料分类计算理论耗用量
#     result_df['理论耗用量'] = 0
    
#     # 膏体：Spec唯一值 * 产品入库数量/1000
#     mask_cream = result_df['物料分类'] == '膏体'
#     result_df.loc[mask_cream, '理论耗用量'] = result_df.loc[mask_cream, 'Spec_doc'] * result_df.loc[mask_cream, '产品入库数量'] / 1000
    
#     # 纸箱：产品入库数量 / BoxSpec唯一值
#     mask_box = result_df['物料分类'] == '纸箱'
#     result_df.loc[mask_box, '理论耗用量'] = result_df.loc[mask_box, '产品入库数量'] // result_df.loc[mask_box, 'BoxSpec_doc'] # 使用整除法（生产入库零头不需要使用纸箱，按照入库量换算纸箱需舍弃小数点）
    
#     # 其他类别：产品入库数量
#     mask_other = ~result_df['物料分类'].isin(['膏体', '纸箱'])
#     result_df.loc[mask_other, '理论耗用量'] = result_df.loc[mask_other, '产品入库数量']
    
#     # 3. 根据物料分类计算损耗率
#     result_df['损耗率'] = 0.0 # 改为 float 类型
    
#     # 膏体和纸箱：(实际用量-理论耗用量)/理论耗用量
#     mask_cream_box = result_df['物料分类'].isin(['膏体', '纸箱'])
#     result_df.loc[mask_cream_box, '损耗率'] = (result_df.loc[mask_cream_box, '实际用量'] - 
#                                                 result_df.loc[mask_cream_box, '理论耗用量']) / \
#                                                 result_df.loc[mask_cream_box, '理论耗用量']
    
#     # 原辅料：(实际用量-WIP计划数量)/WIP计划数量
#     mask_raw = result_df['物料分类'] == '原辅料'
#     result_df.loc[mask_raw, '损耗率'] = (result_df.loc[mask_raw, '实际用量'] - 
#                                         result_df.loc[mask_raw, 'WIP计划数量']) / \
#                                         result_df.loc[mask_raw, 'WIP计划数量']
    
#     # 其他类别：(实际用量-产品入库数量)/产品入库数量
#     result_df.loc[mask_other, '损耗率'] = (result_df.loc[mask_other, '实际用量'] - 
#                                             result_df.loc[mask_other, '产品入库数量']) / \
#                                             result_df.loc[mask_other, '产品入库数量']
    
#     # 4. 处理特殊情况（如除零错误）并转换为百分比格式
#     result_df['损耗率'] = np.where(
#         result_df['理论耗用量'] == 0,  # 针对膏体和纸箱的除零情况
#         np.where(result_df['WIP计划数量'] == 0,  # 针对原辅料的除零情况
#                     0, 
#                     (result_df['实际用量'] - result_df['WIP计划数量']) / 0.001),
#         result_df['损耗率']
#     )
    
#     # 5. 格式化为百分比并保留三位小数
#     result_df['损耗率(%)'] = (result_df['损耗率'] ).map('{:.6f}'.format)
    
#     # 6. 清理临时列
#     # result_df = result_df.drop(columns=['Spec_doc', 'BoxSpec_doc', '理论耗用量', '损耗率'])
    
#     return result_df
