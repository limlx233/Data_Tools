import io
import streamlit as st
import pandas as pd
from DP import dp1,dp2
import openpyxl  # 添加这行导入语句
from openpyxl.utils import get_column_letter  # 或者直接导入需要的函数

from login import check_password
if not check_password():  
    st.stop()

# 初始化 session state
if 'res_jkh' not in st.session_state:
    st.session_state.res_jkh = None

# 继续子页面内容   
st.header("洗护耗用数据统计", divider="rainbow")
with st.expander(label='说明'):
    st.markdown('''
                - ###### 数据来源：  
                    1. ERP `cux.库存事务处理查询XML` 来源名称 **`5`** (生产任务Job or Schedule)          
                    2. ERP `任务批配料消耗明细表`  期间自:`自行选择` 期间到:`自行选择`  是否分页：`否`
                - ###### 不同生产单元分不同工单对应的批次对物料损耗率统计(注：少数结果需人工核对修正)
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
        ##### 1. 组织:
        ''')
    with col2:
        Org = st.selectbox(label=" ",options=["洗护(JKH)"])
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
        uploaded_file1 = st.file_uploader(
            "任务批配料消耗明细表.xlsx",
            type=["xlsx"],
            accept_multiple_files=False  # 不启用多文件上传
        )
        uploaded_file2 = st.file_uploader(
            "库存事务处理查询XML.xlsx",
            type=["xlsx"],
            accept_multiple_files=False  # 不启用多文件上传
        )
        if uploaded_file1 and uploaded_file2:
            df1 = dp2.load_excel_file1(uploaded_file1)
            df1 = dp2.p1(df1)
            df2 = dp2.load_excel_file2(uploaded_file2)
            df2 = dp2.p2(df2)
            query1 = ''' SELECT * FROM `category` c WHERE c.Org = '洗护' '''
            df_category = dp1.execute_query(engine, query1)
            df_merge1 = pd.merge(
                            df1,
                            df2,
                            on = '单据号',
                            how = 'left')
            df_merge1['配料/产品ID'] = df_merge1['配料/产品ID'].apply(
                        lambda x: str(int(x)) if isinstance(x, (int, float)) else str(x).strip())
            df_category['MCode'] = df_category['MCode'].apply(
                                    lambda x: str(int(x)) if isinstance(x, (int, float)) else str(x).strip())
            df_merge2 = pd.merge(
                            df_merge1,
                            df_category,
                            left_on = '配料/产品ID',
                            right_on = 'MCode',
                            how = 'left')
            df_merge2 = dp2.classify_materials(df_merge2)
            res = dp2.calculate_loss_rate(df_merge2)
            columns_to_keep = [
                '生产批前缀',
                '单据号',
                '配方名称',
                '生产工序',
                '产品编码',
                '入库批号',
                '配料/产品ID',
                '配料/产品名称',
                '单位',
                'WIP计划数量',
                '实际用量',
                '产品入库数量',
                '单位(主)',
                '物料分类',
                '理论耗用量',
                '损耗率(%)'
            ]
            # 保留指定列
            res = res[columns_to_keep]
            st.session_state.res_jkh = res
            
    if uploaded_file1 and uploaded_file2 and st.session_state.res_jkh is not None:
        st.markdown('''
        ##### 3. 结果下载:
        ''')
        # 创建 Excel 文件并写入数据
        def create_excel():
            # 创建 BytesIO 对象
            output = io.BytesIO()
            
            # 使用上下文管理器确保 writer 正确保存和关闭
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                # 写入原始数据（不修改 DataFrame）
                st.session_state.res_jkh.to_excel(writer, sheet_name=f"{Org}-物料损耗率统计", index=False)
                
                # 获取 workbook 和 worksheet
                workbook = writer.book
                worksheet = writer.sheets[f"{Org}-物料损耗率统计"]
                
                # 设置百分比格式（保留4位小数）
                percentage_format = '0.0000%'
                
                if '损耗率(%)' in st.session_state.res_jkh.columns:
                    col_idx = st.session_state.res_jkh.columns.get_loc('损耗率(%)') + 1  # Excel列从1开始
                    for row in worksheet.iter_rows(min_row=2, min_col=col_idx, max_col=col_idx):
                        for cell in row:
                            cell.number_format = percentage_format
            
            # 将指针移到 BytesIO 开头（关键步骤！）
            output.seek(0)
            return output.getvalue()

        # 添加下载按钮
        st.download_button(
            label="下载Excel文件",
            type="primary",
            data=create_excel(),
            file_name=f"{Org}-物料损耗率统计.xlsx",
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        st.markdown(
            '''
            ###### 结果预览
            '''
        )
        st.dataframe(st.session_state.res_jkh, hide_index=True)




