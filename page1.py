# @ Author: Penna_Wld
# @ Create Time: 2025-03-03 02:05:57
# @ Modified by: Penna_Wld
# @ Modified time: 2025-04-14 14:47:24
# @ Description: 更换说明为 每月物料数据处理 模块

import streamlit as st


from login import check_password
if not check_password():  
    st.stop()
# 继续子页面内容   
st.header("111", divider="rainbow")
st.subheader("说明", divider="grey")
with st.container(border=True):
    st.write("1.要求上传Excel文件中应含有如图所示表单:")
# st.image(pic1_path)
# st.write("2.要求上传Excel文件中的Sheet应含有如图所示字段:")
# st.image(pic2_path)
# st.write("需包含:blue[日期、班级、产量定额、产量合计]四个必须字段。")
# st.write("3.:red[注意:]")
# st.write("当打开app如图表示程序处于休眠状态,点击下图蓝色按钮稍后即可唤醒。")
# st.image(pic3_path)
