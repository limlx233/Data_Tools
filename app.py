import streamlit as st
from login import check_password


# 检查登录状态
is_logged_in = check_password()

if not is_logged_in:
    st.stop()

# 页面配置
st.set_page_config(
    page_title="数据工具箱",
    layout="centered",
    initial_sidebar_state="expanded"
)
# ========== 主界面逻辑 ==========
# img = "pics\数据logo.png"
# st.logo(img, size='large',)

# 保存和恢复会话状态
def save_state():
    st.session_state['saved_state'] = st.session_state.to_dict()

def restore_state():
    if 'saved_state' in st.session_state:
        for key, value in st.session_state['saved_state'].items():
            st.session_state[key] = value

def logout():# 侧边栏 账号登出管理
    st.session_state.clear()  # 完全清除会话状态
    st.query_params.clear()
    pg = st.navigation([st.Page("login.py", title="登陆界面")])
    st.rerun()  # 重新运行应用

pages = {
    "物料耗用": [st.Page("page1.py", title="耗用数据统计")],
    # "库存现有量": [st.Page("page3.py", title="库存数据处理")],
    "产能负荷率": [st.Page("page2.py", title="台班数据处理")],
    # "成品异常库存": [st.Page("page4.py", title="成品库存处理")],
    # "物料异常库存": [st.Page("page5.py", title="物料库存处理")],
    "登出账号": [st.Page(logout, title="退出登陆", icon=":material/logout:")]
}
# 创建导航组件
restore_state()
pg = st.navigation(pages)

# 监听导航切换事件
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = pg.title

if pg.title != st.session_state['current_page']:
    save_state()
    st.session_state['current_page'] = pg.title

# 显示当前页面
pg.run()