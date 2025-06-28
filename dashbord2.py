import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from pyecharts import options as opts
from pyecharts.charts import Line, Bar, Pie, Gauge
from streamlit_echarts import st_pyecharts

# 页面配置
st.set_page_config(
    page_title="计划运营数字看板",
    page_icon="📊",
    layout="wide"
)

# 科技蓝主题CSS
st.markdown("""
<style>
body, .stApp {
    background: linear-gradient(135deg, #0a1a2f 0%, #183c5a 100%) !important;
    color: #eaf6ff;
}
.stApp {
    padding: 0;
}
.header-bar {
    width: 100%;
    background: linear-gradient(90deg, #1e4c7a 0%, #0a1a2f 100%);
    padding: 24px 0 12px 0;
    text-align: center;
    color: #6ecaff;
    font-size: 2.2rem;
    font-weight: bold;
    letter-spacing: 6px;
    border-bottom: 2px solid #2e6fa3;
    box-shadow: 0 2px 8px #0a1a2f44;
}
.date-bar {
    position: absolute;
    right: 40px;
    top: 32px;
    color: #b2e0ff;
    font-size: 1.1rem;
}
.card {
    background: rgba(20,40,80,0.85);
    border: 1.5px solid #2e6fa3;
    border-radius: 12px;
    box-shadow: 0 2px 12px #0a1a2f33;
    padding: 18px 10px 10px 18px;
    margin-bottom: 12px;
}
.card-title {
    color: #6ecaff;
    font-size: 1.1rem;
    font-weight: bold;
    margin-bottom: 8px;
}
.card-value {
    color: #fff;
    font-size: 1.7rem;
    font-weight: bold;
}
.card-sub {
    color: #6ecaff;
    font-size: 0.9rem;
}
.divider {
    border-bottom: 2px solid #2e6fa3;
    margin: 18px 0 18px 0;
}
</style>
""", unsafe_allow_html=True)

# 顶部横幅
st.markdown('<div class="header-bar">计划运营数字看板</div>', unsafe_allow_html=True)
st.markdown(f'<div class="date-bar">{datetime.now().strftime("%Y.%m.%d %A")}</div>', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# 核心指标卡片区
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">需求计划量</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-value">10,336,348</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-sub">同比 +5.0%</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">累计订单量</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-value">12,536,505</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-sub">环比 +1.7%</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">生产进度</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-value">1,855K</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-sub">本月产量</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">物料齐套率</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-value">73.96%</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-sub">T+5 齐套率</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# 主体分区
# 1. 需求计划分析（折线图）
col1, col2 = st.columns([2,1])
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">需求计划分析</div>', unsafe_allow_html=True)
    x = [f"{i+1}月" for i in range(12)]
    y1 = np.random.randint(8000000, 12000000, 12)
    y2 = np.random.randint(9000000, 13000000, 12)
    line = (
        Line()
        .add_xaxis(x)
        .add_yaxis("预测需求", y1.tolist(), is_smooth=True, linestyle_opts=opts.LineStyleOpts(width=3, color="#6ecaff"), label_opts=opts.LabelOpts(is_show=False))
        .add_yaxis("实际订单", y2.tolist(), is_smooth=True, linestyle_opts=opts.LineStyleOpts(width=3, color="#00ffe7"), label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            legend_opts=opts.LegendOpts(pos_top="5%", textstyle_opts=opts.TextStyleOpts(color="#6ecaff")),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(color="#b2e0ff")),
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(color="#b2e0ff")),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            title_opts=opts.TitleOpts(is_show=False),
            datazoom_opts=[opts.DataZoomOpts()],
        )
    )
    st_pyecharts(line, height="260px")
    st.markdown('</div>', unsafe_allow_html=True)

# 2. 生产进度跟踪（环形仪表盘）
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">生产进度跟踪</div>', unsafe_allow_html=True)
    gauge = (
        Gauge()
        .add(
            "", [("完成率", 74)],
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(
                    color=[(0.74, "#6ecaff"), (1, "#2e6fa3")], width=18)),
            detail_label_opts=opts.LabelOpts(font_size=18, color="#6ecaff"),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(is_show=False),
        )
    )
    st_pyecharts(gauge, height="260px")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# 3. 订单进度分析（折线图）+ 资源负荷分析（条形图）
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">订单进度分析</div>', unsafe_allow_html=True)
    x = [str(i+1) for i in range(12)]
    y = np.random.randint(8000000, 12000000, 12)
    line2 = (
        Line()
        .add_xaxis(x)
        .add_yaxis("月累计订单", y.tolist(), is_smooth=True, linestyle_opts=opts.LineStyleOpts(width=3, color="#6ecaff"), label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(color="#b2e0ff")),
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(color="#b2e0ff")),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            title_opts=opts.TitleOpts(is_show=False),
        )
    )
    st_pyecharts(line2, height="220px")
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">资源负荷分析</div>', unsafe_allow_html=True)
    bar = (
        Bar()
        .add_xaxis([f"产线{i+1}" for i in range(5)])
        .add_yaxis("月度负荷", [61.59, 57.3, 55.81, 47.99, 39.73],
                   itemstyle_opts=opts.ItemStyleOpts(color="#6ecaff"),
                   label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(color="#b2e0ff")),
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(color="#b2e0ff")),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            title_opts=opts.TitleOpts(is_show=False),
        )
    )
    st_pyecharts(bar, height="220px")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# 4. 底部表格区
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-title">在执行订单全链路跟踪</div>', unsafe_allow_html=True)
data = {
    "订单号": [f"CF-YZCZB-20250212-0{i:02d}" for i in range(1, 7)],
    "计划量": [60048, 30000, 50000, 504, 38400, 292800],
    "未结订单": [14791334, 80000, 50000, 504, 38400, 292800],
    "工单": [17321012, 30000, 50000, 0, 0, 292800],
    "已完工": [0, 0, 0, 0, 0, 0],
}
df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True, height=220)
st.markdown('</div>', unsafe_allow_html=True)
