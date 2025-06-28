import pandas as pd
import streamlit as st
import DP.dataprocess as dp
import io
from login import check_password
if not check_password():  
    st.stop()
# 初始化会话状态
if 'selected_month_str' not in st.session_state:
    st.session_state.selected_month_str = None

st.subheader("产能符合率-数据处理", divider="grey")

file1 = st.file_uploader(label="台班数据文件上传", accept_multiple_files=False, type=["xlsx"])
if file1:
    df1 = dp.load_file(file1)
    # 将日期列转换为日期时间类型
    df1['日期'] = pd.to_datetime(df1['日期'])
    # 提取月份信息并转换为带 "月" 的字符串格式
    months = df1['日期'].dt.month.unique().tolist()
    months.sort()
    month_strings = [f"{month}月" for month in months]
    # 增加 "全部" 选项
    options = ["全部"] + month_strings
    # 在 Streamlit 中创建 selectbox，默认选择 "全部"
    col1, col2 = st.columns(2, gap="medium", vertical_alignment="bottom")
    with col1:
        selected_month_str = st.selectbox('请选择月份', options, index=0)
        # 将选择的值存储到会话状态中
        st.session_state.selected_month_str = selected_month_str

    # 根据用户选择的月份筛选数据
    if st.session_state.selected_month_str == "全部":
        filtered_df = df1
        tab_list = [f"{st.session_state.selected_month_str}月份汇总", f"{st.session_state.selected_month_str}月份产量数据明细"]
    else:
        # 从选择的字符串中提取月份数字
        selected_month = int(st.session_state.selected_month_str[:-1])
        filtered_df = df1[df1['日期'].dt.month == selected_month]
        tab_list = [f"{selected_month}月份汇总", f"{selected_month}产量数据明细"]

    with col2:
        # 创建 Excel 文件并写入数据
        def create_excel():
            # 创建一个 BytesIO 对象来存储 Excel 数据
            output = io.BytesIO()
            # 使用 BytesIO 对象作为写入目标
            writer = pd.ExcelWriter(output, engine='openpyxl')
            result = dp.calculate_result(filtered_df)
            if st.session_state.selected_month_str == "全部":
                result.to_excel(writer, sheet_name=f"{st.session_state.selected_month_str}月份汇总", index=False)
            else:
                selected_month = int(st.session_state.selected_month_str[:-1])
                result.to_excel(writer, sheet_name=f"{selected_month}月份汇总", index=False)
            filtered_df.to_excel(writer, sheet_name="产量数据明细", index=False)
            # 保存数据到 BytesIO 对象
            writer.close()
            # 将指针移到 BytesIO 对象的开头
            output.seek(0)
            return output.getvalue()
        # 添加下载按钮
        st.download_button(
            label="下载结果",
            data=create_excel(),
            file_name=f"{st.session_state.selected_month_str}-产能负荷率.xlsx",
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    tab1, tab2 = st.tabs(tab_list)
    with tab1:
        if file1:
            result = dp.calculate_result(filtered_df)
            st.dataframe(result, hide_index=True)
            dp.plot_production_line_load_rate(result, st.session_state.selected_month_str)
    with tab2:
        if file1:
            st.dataframe(filtered_df)