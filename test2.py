from streamlit_modal import Modal
import streamlit as st

modal = Modal("确认对话框", key="demo-modal")

open_modal = st.button("打开确认对话框")
if open_modal:
    modal.open()

if modal.is_open():
    with modal.container():
        st.write("确认要执行此操作吗？")
        if st.button("确认"):
            st.feedback("thumbs")
            st.toast("操作已确认")
            modal.close()
            
        if st.button("取消"):
            modal.close()