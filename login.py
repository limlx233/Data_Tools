import time
import hmac
import streamlit as st

def check_password():
    # 初始化密码验证状态
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False

    # 如果已经通过验证直接返回
    if st.session_state.password_correct:
        return True

    # 登录表单
    def show_login_form():
        with st.form("Credentials"):
            # 布局调整
            cols = st.columns([0.6, 0.4, 2])
            cols[1].image("./pics/数据赋能 数据应用.png", width=66)
            cols[2].markdown("## 数据工具箱")

            # 输入字段
            username = st.text_input("账号名称:", key="login_username")
            password = st.text_input("账号密码:", type="password", key="login_password")
            
            col1, col2, col3 = st.columns([2,2,1])
            with col1:
                st.empty()
            with col2:
                st.empty()
            with col3:
                # 登录按钮
                if st.form_submit_button("登录"):
                    # 验证凭证
                    if validate_credentials(username, password):
                        st.session_state.password_correct = True
                        st.query_params = {"logged_in": "true"}
                        
                        # 清空表单并显示成功消息
                        placeholder = st.empty()
                        placeholder.success('登陆成功!' )
                        time.sleep(1)  # 让用户看到成功消息
                        placeholder.empty()
                        st.rerun()
                    else:
                        st.error("😕 账号不存在或密码不正确")
        return False

    # 凭证验证函数
    def validate_credentials(username, password):
        if not username or not password:
            return False
        if username in st.secrets.get("passwords", {}):
            return hmac.compare_digest(
                password,
                st.secrets.passwords[username]
            )
        return False

    # 检查 URL 参数
    query_params = st.query_params
    if "logged_in" in query_params and query_params["logged_in"] == "true":
        st.session_state.password_correct = True
        return True

    # 显示登录表单
    return show_login_form()