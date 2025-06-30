# @ Author: Penna_Wld
# @ Create Time: 2025-03-03 02:05:57
# @ Modified by: Penna_Wld
# @ Modified time: 2025-04-14 14:47:24
# @ Description:  物料耗用数据处理

import io
import streamlit as st
import pandas as pd
from DP import dp1

from login import check_password
if not check_password():  
    st.stop()
    
# 初始化 session state
if 'res_yl' not in st.session_state:
    st.session_state.res_yl = None
if 'res_bc' not in st.session_state:
    st.session_state.res_bc = None

# 继续子页面内容   
st.header("物料耗用数据统计", divider="rainbow")
with st.expander(label='说明'):
    st.markdown('''
                - ###### 数据来源：ERP `cux.库存事务处理查询XML` 来源名称 **5** (生产任务Job or Schedule)
                - ###### 以SKU维度从口腔（JKC、JKY）及 洗护（JKH）不同账套下分别对原辅料、包材的耗用数据(发料到生产批-从生产批退回)进行统计
                - ###### 注意上传Excel文件后缀需为 `.xlsx` 格式
                ''')    

with st.container(border=True):
    engine = dp1.create_mysql_engine()
    query1 = "SELECT DISTINCT UpdateDate FROM `category`"
    df = dp1.execute_query(engine, query1)
    dp1.check_data_update_status(df)

    # 划分两列，宽度比例为 1:2
    col1, col2, col3 = st.columns([1, 2.5, 1])
    with col1:
        st.markdown('''
        ##### 1. 选择组织:
        ''')
    with col2:
        Org = st.selectbox(label=" ",options=["口腔(JKC、JKY)","洗护(JKH)"])
        if Org == "口腔(JKC、JKY)":
            org = '口腔'
            query3 = f''' SELECT c.MCode '物料编码', c.MCategory '物料类别' FROM `category` c  WHERE c.`Org`='{org}' AND c.MCategory IN ('原辅料','包材')'''
        else:
            org = '洗护'
            query3 = f''' SELECT c.MCode '物料编码', c.MCategory '物料类别' FROM `category` c  WHERE c.`Org`='{org}' AND c.MCategory IN ('原辅料','包材')'''
        df_category = dp1.execute_query(engine, query3)

    col4, col5, clo6 = st.columns([1, 2.5, 1])
    with col4:
        st.markdown('''
        ##### 2. 上传文件:
        ''')
    with col5:
        # 创建多文件上传组件，限制文件类型为 XLSX
        uploaded_files = st.file_uploader(
            " ",
            type=["xlsx"],
            accept_multiple_files=True  # 启用多文件上传
        )
        if uploaded_files:
            if st.button(label="数据处理", type="primary", key="data_process"):
                df_all = dp1.load_excel_files(uploaded_files)
                df_all = dp1.process_data(df_all)
                # 将两表的物料编码列转为字符串，并去除前后空格
                df_all['物料编码'] = df_all['物料编码'].astype(str).str.strip()
                df_category['物料编码'] = df_category['物料编码'].astype(str).str.strip()
                # 连接两表保留能匹配到类别的数据
                df_all = df_all.merge(
                        df_category,        # 关联的类别表
                        on='物料编码',      # 基于物料编码关联
                        how='left'          # 左连接保留所有summary_df的行
                    ).dropna(subset=['物料类别'])
                res_df = df_all.groupby(['物料编码', '物料说明', '单位(主)','物料类别'])['数量(主)'].sum().reset_index()
                res_df['数量(主)'] = -res_df['数量(主)'] 
                st.session_state.res_yl = res_df[res_df['物料类别'] == '原辅料']
                st.session_state.res_bc = res_df[res_df['物料类别'] == '包材']
                st.success("数据处理完成!")
        else:
            st.info("请先上传数据文件!")
            st.session_state.res_yl = None
            st.session_state.res_bc = None
    
    if uploaded_files and st.session_state.res_yl is not None and st.session_state.res_bc is not None:
        st.markdown('''
        ##### 3. 结果下载:
        ''')
        # 创建 Excel 文件并写入数据
        def create_excel():
            # 创建一个 BytesIO 对象来存储 Excel 数据
            output = io.BytesIO()
            # 使用 BytesIO 对象作为写入目标
            writer = pd.ExcelWriter(output, engine='openpyxl')
            st.session_state.res_yl.to_excel(writer, sheet_name=f"{Org}-原料耗用统计", index=False)
            st.session_state.res_bc.to_excel(writer, sheet_name=f"{Org}-包材耗用统计", index=False)
            # 保存数据到 BytesIO 对象
            writer.close()
            # 将指针移到 BytesIO 对象的开头
            output.seek(0)
            return output.getvalue()

        # 添加下载按钮
        st.download_button(
            label="下载结果",
            type="primary",
            data=create_excel(),
            file_name=f"{Org}-物料耗用统计.xlsx",
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        st.markdown(
            '''
            ###### 结果预览
            '''
        )
        tab_list = ['原辅料','包材']
        tab1, tab2 = st.tabs(tab_list)
        with tab1:
            if st.session_state.res_yl is not None:
                st.dataframe(st.session_state.res_yl, hide_index=True, width= 720)
            else:
                st.info("暂无原辅料数据")
        with tab2:
            if st.session_state.res_bc is not None:
                st.dataframe(st.session_state.res_bc, hide_index=True, width= 720)
            else:
                st.info("暂无包材数据")
        