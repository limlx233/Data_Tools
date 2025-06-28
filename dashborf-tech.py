import streamlit as st
import pandas as pd
import numpy as np
from pyecharts.charts import Line, Bar, Gauge
from pyecharts import options as opts

st.set_page_config(layout="wide", page_title="科技数据大屏")

# ================== 数据准备 ==================
@st.cache_data
def load_data():
    data = pd.DataFrame({
        'Month': pd.date_range(start='2023-01', periods=12, freq='M'),
        'Sales': np.random.randint(100, 1000, 12),
        'Users': np.random.randint(50, 500, 12),
        'Revenue': np.random.uniform(1000, 5000, 12)
    })
    data['Month'] = data['Month'].dt.strftime('%Y-%m')
    return data

df = load_data()

# ================== 图表生成 ==================
def get_line_chart():
    line = (
        Line()
        .add_xaxis(df['Month'].tolist())
        .add_yaxis("销售额", df['Sales'].tolist(), is_smooth=True, 
                   linestyle_opts=opts.LineStyleOpts(width=3), 
                   itemstyle_opts=opts.ItemStyleOpts(color='#4facfe'))
        .add_yaxis("用户数", df['Users'].tolist(), is_smooth=True, 
                   linestyle_opts=opts.LineStyleOpts(width=3), 
                   itemstyle_opts=opts.ItemStyleOpts(color='#00f2fe'))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="趋势分析", title_textstyle_opts=opts.TextStyleOpts(color='#fff')),
            legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color='#fff')),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(color='#fff')),
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(color='#fff')),
            background_color='rgba(0,0,0,0)'
        )
    )
    return line.render_embed()

def get_bar_chart():
    categories = ['A类', 'B类', 'C类', 'D类', 'E类']
    values = np.random.randint(100, 1000, size=5)
    sorted_data = sorted(zip(categories, values), key=lambda x: x[1], reverse=True)
    sorted_categories, sorted_values = zip(*sorted_data)
    bar = (
        Bar()
        .add_xaxis(list(sorted_categories))
        .add_yaxis("数量", list(sorted_values), itemstyle_opts=opts.ItemStyleOpts(color='#4facfe'))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="数据分布", title_textstyle_opts=opts.TextStyleOpts(color='#fff')),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(color='#fff')),
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(color='#fff')),
            legend_opts=opts.LegendOpts(is_show=False),
            background_color='rgba(0,0,0,0)'
        )
    )
    return bar.render_embed()

def get_gauge_chart():
    gauge = (
        Gauge()
        .add(
            series_name="完成率",
            data_pair=[("达成率", 78)],
            min_=0,
            max_=100,
            detail_label_opts=opts.LabelOpts(formatter="{value}%", color="#fff"),
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(
                    color=[(0.3, "#00f2fe"), (0.7, "#4facfe"), (1, "#ff4500")],
                    width=30
                )
            )
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="年度目标", title_textstyle_opts=opts.TextStyleOpts(color='#fff')),
            legend_opts=opts.LegendOpts(is_show=False),
            background_color='rgba(0,0,0,0)'
        )
    )
    return gauge.render_embed()

# ================== 页面HTML+CSS ==================
st.markdown("""
<style>
body, .stApp {
    background: linear-gradient(135deg, #0a1633 0%, #020a1a 100%) !important;
    color: #fff;
}
.big-title {
    font-size: 3em;
    font-weight: bold;
    text-align: center;
    margin: 30px 0 20px 0;
    background: linear-gradient(90deg, #00f2fe, #4facfe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 8px;
    text-shadow: 0 0 30px #00f2fe;
}
.flex-row {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    margin-bottom: 30px;
}
.card {
    flex: 1;
    background: rgba(16, 32, 71, 0.85);
    border-radius: 18px;
    margin: 0 18px;
    padding: 30px 0 20px 0;
    box-shadow: 0 4px 30px rgba(0, 242, 254, 0.15);
    border: 1px solid rgba(79, 172, 254, 0.25);
    text-align: center;
    min-width: 0;
}
.card h3 {
    font-size: 1.3em;
    margin-bottom: 10px;
    color: #fff;
    letter-spacing: 2px;
}
.card .value {
    font-size: 2.5em;
    font-weight: bold;
    margin-bottom: 0;
}
.card .value.blue { color: #4facfe; }
.card .value.cyan { color: #00f2fe; }
.card .value.red { color: #ff4500; }
.charts-row {
    display: flex;
    flex-direction: row;
    margin-bottom: 30px;
}
.chart-box {
    background: rgba(16, 32, 71, 0.85);
    border-radius: 18px;
    margin: 0 18px;
    padding: 18px 10px 10px 10px;
    box-shadow: 0 4px 30px rgba(0, 242, 254, 0.10);
    border: 1px solid rgba(79, 172, 254, 0.18);
    flex: 1;
    min-width: 0;
}
.chart-box-half {
    flex: 2;
}
.chart-box-small {
    flex: 1;
}
@media (max-width: 1200px) {
    .flex-row, .charts-row { flex-direction: column; }
    .card, .chart-box, .chart-box-half, .chart-box-small { margin: 18px 0; }
}
</style>
""", unsafe_allow_html=True)

# ================== 页面内容 ==================
st.markdown('<div class="big-title">科技数据大屏</div>', unsafe_allow_html=True)

# 指标卡片
st.markdown(f"""
<div class="flex-row">
    <div class="card">
        <h3>总销售额</h3>
        <div class="value blue">¥ {df['Sales'].sum()/100:.1f}万</div>
    </div>
    <div class="card">
        <h3>总用户数</h3>
        <div class="value cyan">{df['Users'].sum()}</div>
    </div>
    <div class="card">
        <h3>总收入</h3>
        <div class="value red">¥ {df['Revenue'].sum()/1000:.1f}万</div>
    </div>
</div>
""", unsafe_allow_html=True)

# 主趋势图
st.markdown('<div class="chart-box" style="margin-bottom:30px;">', unsafe_allow_html=True)
st.components.v1.html(get_line_chart(), height=420, scrolling=False)
st.markdown('</div>', unsafe_allow_html=True)

# 下方条形图+仪表盘
st.markdown("""
<div class="charts-row">
    <div class="chart-box chart-box-half">
""", unsafe_allow_html=True)
st.components.v1.html(get_bar_chart(), height=340, scrolling=False)
st.markdown("""
    </div>
    <div class="chart-box chart-box-small">
""", unsafe_allow_html=True)
st.components.v1.html(get_gauge_chart(), height=340, scrolling=False)
st.markdown("""
    </div>
</div>
""", unsafe_allow_html=True)