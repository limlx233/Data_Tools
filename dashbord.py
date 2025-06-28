# import streamlit as st
# from pyecharts import options as opts
# from pyecharts.charts import Bar, Line, Pie, Gauge, Grid, Timeline
# from pyecharts.commons.utils import JsCode
# from pyecharts.globals import ThemeType
# import random
# import pandas as pd
# import numpy as np
# from streamlit_echarts import st_pyecharts
# import json

# # 设置页面布局
# # st.set_page_config(layout="wide", page_title="数据大屏-示例")

# # 生成模拟数据（固定随机种子保证数据一致性）
# def generate_data():
#     # 固定随机种子
#     random.seed(42)
#     np.random.seed(42)
    
#     # 产品类别和颜色映射
#     categories = ['智能手机', '笔记本电脑', '平板电脑', '智能手表', '耳机', '智能家居']
#     colors = ['#c23531','#2f4554','#61a0a8','#d48265','#91c7ae','#749f83']
#     color_map = {cat: colors[i] for i, cat in enumerate(categories)}
    
#     # 季度数据
#     quarters = ['Q1', 'Q2', 'Q3', 'Q4']
    
#     # 生成季度销售数据
#     sales_data = []
#     for q in quarters:
#         quarter_data = {
#             'quarter': q,
#             'total_sales': random.randint(5000, 10000),
#             'products': {}
#         }
#         for cat in categories:
#             quarter_data['products'][cat] = {
#                 'sales': random.randint(500, 2000),
#                 'revenue': random.randint(50000, 200000),
#                 'growth': round(random.uniform(-0.1, 0.3), 2)
#             }
#         sales_data.append(quarter_data)
    
#     # 生成月度销售趋势
#     months = [f'2023-{str(m).zfill(2)}' for m in range(1, 13)]
#     monthly_trend = {
#         '智能手机': [random.randint(800, 1200) for _ in range(12)],
#         '笔记本电脑': [random.randint(400, 800) for _ in range(12)],
#         '平板电脑': [random.randint(300, 600) for _ in range(12)],
#         '智能手表': [random.randint(200, 500) for _ in range(12)],
#         '耳机': [random.randint(500, 900) for _ in range(12)],
#         '智能家居': [random.randint(300, 700) for _ in range(12)]
#     }
    
#     return {
#         'categories': categories,
#         'color_map': color_map,
#         'quarters': quarters,
#         'sales_data': sales_data,
#         'monthly_trend': monthly_trend,
#         'months': months
#     }

# data = generate_data()

# # 页面标题
# st.title("数据大屏-示例")
# st.markdown("---")

# # 第一行：KPI指标
# st.subheader("指标展示")
# col1, col2, col3, col4 = st.columns(4)

# total_sales = sum([q['total_sales'] for q in data['sales_data']])
# total_revenue = sum([sum([p['revenue'] for p in q['products'].values()]) for q in data['sales_data']])
# avg_growth = np.mean([p['growth'] for q in data['sales_data'] for p in q['products'].values()])
# top_product = max(
#     [(cat, sum([q['products'][cat]['sales'] for q in data['sales_data']])) 
#         for cat in data['categories']],
#     key=lambda x: x[1]
# )[0]

# with col1:
#     st.metric("年度总销量", f"{total_sales:,}", "12%")
# with col2:
#     st.metric("年度总收入", f"¥{total_revenue:,}", "8.5%")
# with col3:
#     st.metric("平均增长率", f"{avg_growth:.1%}", f"{avg_growth:.1%}")
# with col4:
#     st.metric("最畅销产品", top_product)

# st.markdown("---")

# # 第二行：仪表盘和产品销量排行
# col1, col2 = st.columns([1, 2])

# with col1:
#     # 销售目标完成率仪表盘
#     completion_rate = min(1.0, total_sales / 30000)
#     gauge = (
#         Gauge(init_opts=opts.InitOpts(theme=ThemeType.DARK))
#         .add(
#             series_name="完成率",
#             data_pair=[("销售目标", round(completion_rate * 100, 1))],
#             min_=0,
#             max_=100,
#             split_number=10,
#             axisline_opts=opts.AxisLineOpts(
#                 linestyle_opts=opts.LineStyleOpts(
#                     color=[(0.3, "#67e0e3"), (0.7, "#37a2da"), (1, "#fd666d")], width=30
#                 )
#             ),
#             detail_label_opts=opts.LabelOpts(formatter="{value}%"),
#             title_label_opts=opts.LabelOpts(
#                 font_size=20, font_weight="bolder", color="#fff"
#             ),
#         )
#         .set_global_opts(
#             title_opts=opts.TitleOpts(title="年度销售目标完成率", pos_left="center"),
#             legend_opts=opts.LegendOpts(is_show=False),
#         )
#     )
#     st_pyecharts(gauge, height=400)

# with col2:
#     # 产品类别销量排行条形图（颜色统一）
#     product_sales = {
#         cat: sum([q['products'][cat]['sales'] for q in data['sales_data']]) 
#         for cat in data['categories']
#     }
#     sorted_products = sorted(
#         [(cat, sales) for cat, sales in product_sales.items()],
#         key=lambda x: x[1],
#         reverse=False
#     )
    
#     categories_sorted = [x[0] for x in sorted_products]
#     sales_sorted = [x[1] for x in sorted_products]
    
#     # 构造颜色映射的JS对象
#     color_js_entries = [f"'{k}': '{v}'" for k, v in data['color_map'].items()]
#     color_js_str = "{" + ", ".join(color_js_entries) + "}"
    
#     bar_rank = (
#         Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
#         .add_xaxis(categories_sorted)
#         .add_yaxis(
#             "销量", 
#             sales_sorted,
#             label_opts=opts.LabelOpts(
#                 position="right",
#                 formatter=JsCode("function(params){return params.value.toLocaleString();}")
#             ),
#             itemstyle_opts=opts.ItemStyleOpts(
#                 color=JsCode(
#                     f"function(params) {{"
#                     f"    var colorMap = {color_js_str};"
#                     f"    return colorMap[params.name];"
#                     f"}}"
#                 ),
#             ),
#         )
#         .reversal_axis()
#         .set_global_opts(
#             title_opts=opts.TitleOpts(title="产品类别销量排行", pos_left="center"),
#             xaxis_opts=opts.AxisOpts(
#                 name="销量",
#                 name_location="middle",
#                 name_gap=30,
#                 splitline_opts=opts.SplitLineOpts(is_show=True),
#             ),
#             yaxis_opts=opts.AxisOpts(
#                 axislabel_opts=opts.LabelOpts(interval=0),
#                 is_inverse= False
#             ),
#             tooltip_opts=opts.TooltipOpts(
#                 formatter=JsCode(
#                     """function(params) {
#                         return params.name + ': ' + params.value.toLocaleString();
#                     }"""
#                 )
#             ),
#             legend_opts=opts.LegendOpts(
#                 pos_bottom="0%",
#                 orient="horizontal"
#             ),
#         )
#     )
#     st_pyecharts(bar_rank, height=400)

# # 第三行：折线图和柱状图
# col1, col2 = st.columns(2)

# with col1:
#     # 月度销售趋势折线图（颜色统一）
#     line = (
#         Line(init_opts=opts.InitOpts(theme=ThemeType.DARK))
#         .add_xaxis(data['months'])
#     )
    
#     for cat in data['categories']:
#         line.add_yaxis(
#             series_name=cat,
#             y_axis=data['monthly_trend'][cat],
#             is_smooth=True,
#             symbol="circle",
#             symbol_size=8,
#             label_opts=opts.LabelOpts(is_show=False),
#             linestyle_opts=opts.LineStyleOpts(
#                 color=data['color_map'][cat], 
#                 width=3
#             ),
#             itemstyle_opts=opts.ItemStyleOpts(
#                 color=data['color_map'][cat]
#             ),
#         )
    
#     line.set_global_opts(
#         title_opts=opts.TitleOpts(title="月度产品销售趋势", pos_left="center"),
#         tooltip_opts=opts.TooltipOpts(trigger="axis"),
#         legend_opts=opts.LegendOpts(
#             pos_bottom="0%",
#             orient="horizontal"
#         ),
#         xaxis_opts=opts.AxisOpts(
#             type_="category",
#             axislabel_opts=opts.LabelOpts(rotate=45),
#             boundary_gap=False,
#         ),
#         yaxis_opts=opts.AxisOpts(
#             name="销量",
#             name_location="middle",
#             name_gap=40,
#             splitline_opts=opts.SplitLineOpts(is_show=True),
#         ),
#     )
#     st_pyecharts(line, height=400)

# with col2:
#     # 季度产品销量柱状图（颜色统一）
#     bar_data = {cat: [q['products'][cat]['sales'] for q in data['sales_data']] for cat in data['categories']}
    
#     bar = (
#         Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
#         .add_xaxis(data['quarters'])
#     )
    
#     for cat in data['categories']:
#         bar.add_yaxis(
#             series_name=cat,
#             y_axis=bar_data[cat],
#             label_opts=opts.LabelOpts(is_show=False),
#             itemstyle_opts=opts.ItemStyleOpts(
#                 opacity=0.8,
#                 color=data['color_map'][cat],
#             ),
#         )
    
#     bar.set_global_opts(
#         title_opts=opts.TitleOpts(title="季度产品销量对比", pos_left="center"),
#         tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="shadow"),
#         legend_opts=opts.LegendOpts(
#             pos_bottom="0%",
#             orient="horizontal"
#         ),
#         xaxis_opts=opts.AxisOpts(
#             axislabel_opts=opts.LabelOpts(rotate=0),
#             boundary_gap=True,
#         ),
#         yaxis_opts=opts.AxisOpts(
#             name="销量",
#             name_location="middle",
#             name_gap=40,
#             splitline_opts=opts.SplitLineOpts(is_show=True),
#         ),
#     )
#     st_pyecharts(bar, height=400)

# # 第四行：折柱混合图（颜色统一）
# st.subheader("季度销量分析")
# quarters = data['quarters']
# categories = data['categories']

# product_sales_by_quarter = {
#     cat: [q['products'][cat]['sales'] for q in data['sales_data']] 
#     for cat in categories
# }

# total_sales_by_quarter = [
#     sum(q['products'][cat]['sales'] for cat in categories)
#     for q in data['sales_data']
# ]

# bar = (
#     Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
#     .add_xaxis(quarters)
# )

# for cat in categories:
#     bar.add_yaxis(
#         series_name=cat,
#         y_axis=product_sales_by_quarter[cat],
#         yaxis_index=0,
#         label_opts=opts.LabelOpts(is_show=False),
#         itemstyle_opts=opts.ItemStyleOpts(color=data['color_map'][cat]),
#         z=1
#     )

# line = (
#     Line(init_opts=opts.InitOpts(theme=ThemeType.DARK))
#     .add_xaxis(quarters)
#     .add_yaxis(
#         series_name="季度总销量",
#         y_axis=total_sales_by_quarter,
#         yaxis_index=1,
#         label_opts=opts.LabelOpts(is_show=False),
#         linestyle_opts=opts.LineStyleOpts(width=4),
#         symbol="diamond",
#         symbol_size=12,
#         itemstyle_opts=opts.ItemStyleOpts(color="#FFA500"),
#         z=2
#     )
# )

# bar.overlap(line)

# bar.set_global_opts(
#     title_opts=opts.TitleOpts(title="季度产品销量与总销量趋势", pos_left="center"),
#     tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
#     legend_opts=opts.LegendOpts(
#         pos_bottom="0%",
#         orient="horizontal"
#     ),
#     xaxis_opts=opts.AxisOpts(
#         axislabel_opts=opts.LabelOpts(rotate=0),
#         boundary_gap=True,
#     ),
#     yaxis_opts=opts.AxisOpts(
#         name="产品销量",
#         name_location="middle",
#         name_gap=40,
#         splitline_opts=opts.SplitLineOpts(is_show=True),
#     ),
# )

# bar.extend_axis(
#     yaxis=opts.AxisOpts(
#         name="总销量",
#         name_location="middle",
#         name_gap=50,
#         splitline_opts=opts.SplitLineOpts(is_show=False),
#     )
# )

# st_pyecharts(bar, height=500)

# # 底部信息
# st.markdown("---")
# st.markdown("**数据说明**: 所有数据均为模拟生成，仅用于演示目的。")

import streamlit as st
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Gauge
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType
from sqlalchemy import create_engine, text
import pandas as pd
import numpy as np
from streamlit_echarts import st_pyecharts

# ----------------------
# 数据库连接配置
# ----------------------
# 从Streamlit Secrets获取配置
db_config = st.secrets.get("database", {})
DB_URL = f"mysql+pymysql://{db_config.get('user', '')}:{db_config.get('password', '')}@{db_config.get('host', '')}:{db_config.get('port', 3306)}/{db_config.get('database', '')}"

# 定义颜色映射（与原始版本完全一致）
CATEGORY_COLOR_MAP = {
    "智能手机": "#c23531",
    "笔记本电脑": "#2f4554",
    "平板电脑": "#61a0a8",
    "智能手表": "#d48265",
    "耳机": "#91c7ae",
    "智能家居": "#749f83"
}

# ----------------------
# 数据获取函数
# ----------------------
@st.cache_data(ttl=3600)
def fetch_data():
    """从数据库获取大屏所需数据（数据结构与原始版本完全一致）"""
    try:
        engine = create_engine(DB_URL, pool_recycle=3600)
        with engine.connect() as conn:
            
            # 1. 获取产品类别（修正ORDER BY问题）
            categories = pd.read_sql(
                text("SELECT DISTINCT category_name FROM product_categories ORDER BY category_name"),
                conn
            )["category_name"].astype(str).tolist()
            
            # 2. 获取季度数据
            quarters = pd.read_sql(
                text("SELECT quarter FROM quarterly_sales ORDER BY quarter_id"),
                conn
            )["quarter"].astype(str).tolist()
            
            # 3. 获取销售明细数据
            sales_df = pd.read_sql(text("""
                SELECT 
                    q.quarter, 
                    p.category_name, 
                    ps.sales_volume AS sales,
                    ps.revenue AS revenue,
                    ps.growth_rate AS growth
                FROM product_sales ps
                JOIN quarterly_sales q ON ps.quarter_id = q.quarter_id
                JOIN product_categories p ON ps.category_id = p.category_id
                ORDER BY q.quarter_id, p.category_id
            """), conn)
            
            # 4. 获取月度销售趋势数据
            monthly_df = pd.read_sql(text("""
                SELECT 
                    p.category_name, 
                    DATE_FORMAT(m.sales_month, '%Y-%m') AS sales_month,
                    m.sales_volume
                FROM monthly_sales_trend m
                JOIN product_categories p ON m.category_id = p.category_id
                ORDER BY m.sales_month, p.category_id
            """), conn)
            
            # 转换为与原始版本完全一致的数据结构
            sales_data = []
            for q in quarters:
                quarter_data = {
                    'quarter': q,
                    'total_sales': sales_df[sales_df['quarter'] == q]['sales'].sum(),
                    'products': {}
                }
                for cat in categories:
                    cat_data = sales_df[(sales_df['quarter'] == q) & (sales_df['category_name'] == cat)]
                    quarter_data['products'][cat] = {
                        'sales': cat_data['sales'].values[0] if not cat_data.empty else 0,
                        'revenue': cat_data['revenue'].values[0] if not cat_data.empty else 0,
                        'growth': cat_data['growth'].values[0] if not cat_data.empty else 0.0
                    }
                sales_data.append(quarter_data)
            
            # 处理月度趋势数据
            monthly_trend = {
                cat: monthly_df[monthly_df['category_name'] == cat]['sales_volume'].tolist()
                for cat in categories
            }
            months = monthly_df['sales_month'].unique().tolist()
            
            return {
                'categories': categories,
                'color_map': CATEGORY_COLOR_MAP,
                'quarters': quarters,
                'sales_data': sales_data,
                'monthly_trend': monthly_trend,
                'months': months
            }
    
    except Exception as e:
        st.error(f"数据库操作失败：{str(e)}")
        return None

# ----------------------
# 图表渲染函数（保持与原始版本完全一致的逻辑）
# ----------------------
def render_kpi_metrics(data):
    """渲染KPI指标区域（与原始版本完全一致）"""
    if data is None or not data["sales_data"]:
        st.warning("数据为空，无法渲染指标")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("年度总销量", "0", "0%")
        with col2:
            st.metric("年度总收入", "¥0", "0%")
        with col3:
            st.metric("平均增长率", "0.0%", "0.0%")
        with col4:
            st.metric("最畅销产品", "无")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_sales = sum([q['total_sales'] for q in data['sales_data']])
    total_revenue = sum([sum([p['revenue'] for p in q['products'].values()]) for q in data['sales_data']])
    avg_growth = np.mean([p['growth'] for q in data['sales_data'] for p in q['products'].values()])
    top_product = max(
        [(cat, sum([q['products'][cat]['sales'] for q in data['sales_data']])) 
         for cat in data['categories']],
        key=lambda x: x[1]
    )[0]

    with col1:
        st.metric("年度总销量", f"{total_sales:,}", "12%")
    with col2:
        st.metric("年度总收入", f"¥{total_revenue:,}", "8.5%")
    with col3:
        st.metric("平均增长率", f"{avg_growth:.1%}", f"{avg_growth:.1%}")
    with col4:
        st.metric("最畅销产品", top_product)

def render_sales_completion_gauge(total_sales):
    """渲染销售目标完成率仪表盘（与原始版本完全一致）"""
    completion_rate = min(1.0, total_sales / 30000)
    gauge = (
        Gauge(init_opts=opts.InitOpts(theme=ThemeType.DARK))
        .add(
            series_name="完成率",
            data_pair=[("销售目标", round(completion_rate * 100, 1))],
            min_=0,
            max_=100,
            split_number=10,
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(
                    color=[(0.3, "#67e0e3"), (0.7, "#37a2da"), (1, "#fd666d")], width=30
                )
            ),
            detail_label_opts=opts.LabelOpts(formatter="{value}%"),
            title_label_opts=opts.LabelOpts(
                font_size=20, font_weight="bolder", color="#fff"
            ),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="年度销售目标完成率", pos_left="center"),
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )
    return gauge

def render_product_sales_rank(data):
    """渲染产品销量排行条形图（与原始版本完全一致）"""
    if data is None or not data["sales_data"]:
        return None
    
    product_sales = {
        cat: sum([q['products'][cat]['sales'] for q in data['sales_data']]) 
        for cat in data['categories']
    }
    sorted_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=False)
    categories_sorted = [x[0] for x in sorted_products]
    sales_sorted = [x[1] for x in sorted_products]
    
    color_js_entries = [f"'{k}': '{v}'" for k, v in data['color_map'].items()]
    color_js_str = "{" + ", ".join(color_js_entries) + "}"
    
    bar_rank = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
        .add_xaxis(categories_sorted)
        .add_yaxis(
            "销量", 
            sales_sorted,
            label_opts=opts.LabelOpts(
                position="right",
                formatter=JsCode("function(params){return params.value.toLocaleString();}")
            ),
            itemstyle_opts=opts.ItemStyleOpts(
                color=JsCode(
                    f"function(params) {{"
                    f"    var colorMap = {color_js_str};"
                    f"    return colorMap[params.name];"
                    f"}}"
                ),
            ),
        )
        .reversal_axis()
        .set_global_opts(
            title_opts=opts.TitleOpts(title="产品类别销量排行", pos_left="center"),
            xaxis_opts=opts.AxisOpts(
                name="销量",
                name_location="middle",
                name_gap=30,
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            yaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(interval=0),
                is_inverse= False
            ),
            tooltip_opts=opts.TooltipOpts(
                formatter=JsCode(
                    """function(params) {
                    return params.name + ': ' + params.value.toLocaleString();
                    }"""
                )
            ),
            legend_opts=opts.LegendOpts(
                pos_bottom="0%",
                orient="horizontal"
            ),
        )
    )
    return bar_rank

def render_monthly_trend_line(data):
    """渲染月度销售趋势折线图（与原始版本完全一致）"""
    if data is None or not data["months"]:
        return None
    
    line = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.DARK))
        .add_xaxis(data['months'])
    )
    
    for cat in data['categories']:
        line.add_yaxis(
            series_name=cat,
            y_axis=data['monthly_trend'][cat],
            is_smooth=True,
            symbol="circle",
            symbol_size=8,
            label_opts=opts.LabelOpts(is_show=False),
            linestyle_opts=opts.LineStyleOpts(
                color=data['color_map'][cat], 
                width=3
            ),
            itemstyle_opts=opts.ItemStyleOpts(
                color=data['color_map'][cat]
            ),
        )
    
    line.set_global_opts(
        title_opts=opts.TitleOpts(title="月度产品销售趋势", pos_left="center"),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        legend_opts=opts.LegendOpts(
            pos_bottom="0%",
            orient="horizontal"
        ),
        xaxis_opts=opts.AxisOpts(
            type_="category",
            axislabel_opts=opts.LabelOpts(rotate=45),
            boundary_gap=False,
        ),
        yaxis_opts=opts.AxisOpts(
            name="销量",
            name_location="middle",
            name_gap=40,
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
    )
    return line

def render_quarterly_sales_bar(data):
    """渲染季度产品销量柱状图（与原始版本完全一致）"""
    if data is None or not data["quarters"]:
        return None
    
    bar_data = {cat: [q['products'][cat]['sales'] for q in data['sales_data']] for cat in data['categories']}
    
    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
        .add_xaxis(data['quarters'])
    )
    
    for cat in data['categories']:
        bar.add_yaxis(
            series_name=cat,
            y_axis=bar_data[cat],
            label_opts=opts.LabelOpts(is_show=False),
            itemstyle_opts=opts.ItemStyleOpts(
                opacity=0.8,
                color=data['color_map'][cat],
            ),
        )
    
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title="季度产品销量对比", pos_left="center"),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="shadow"),
        legend_opts=opts.LegendOpts(
            pos_bottom="0%",
            orient="horizontal"
        ),
        xaxis_opts=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(rotate=0),
            boundary_gap=True,
        ),
        yaxis_opts=opts.AxisOpts(
            name="销量",
            name_location="middle",
            name_gap=40,
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
    )
    return bar

def render_combined_chart(data):
    """渲染折柱混合图（与原始版本完全一致）"""
    if data is None or not data["quarters"]:
        return None
    
    product_sales_by_quarter = {
        cat: [q['products'][cat]['sales'] for q in data['sales_data']] 
        for cat in data['categories']
    }

    total_sales_by_quarter = [
        sum(q['products'][cat]['sales'] for cat in data['categories'])
        for q in data['sales_data']
    ]

    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
        .add_xaxis(data['quarters'])
    )

    for cat in data['categories']:
        bar.add_yaxis(
            series_name=cat,
            y_axis=product_sales_by_quarter[cat],
            yaxis_index=0,
            label_opts=opts.LabelOpts(is_show=False),
            itemstyle_opts=opts.ItemStyleOpts(color=data['color_map'][cat]),
            z=1
        )

    line = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.DARK))
        .add_xaxis(data['quarters'])
        .add_yaxis(
            series_name="季度总销量",
            y_axis=total_sales_by_quarter,
            yaxis_index=1,
            label_opts=opts.LabelOpts(is_show=False),
            linestyle_opts=opts.LineStyleOpts(width=4),
            symbol="diamond",
            symbol_size=12,
            itemstyle_opts=opts.ItemStyleOpts(color="#FFA500"),
            z=2
        )
    )

    bar.overlap(line)

    bar.set_global_opts(
        title_opts=opts.TitleOpts(title="季度产品销量与总销量趋势", pos_left="center"),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        legend_opts=opts.LegendOpts(
            pos_bottom="0%",
            orient="horizontal"
        ),
        xaxis_opts=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(rotate=0),
            boundary_gap=True,
        ),
        yaxis_opts=opts.AxisOpts(
            name="产品销量",
            name_location="middle",
            name_gap=40,
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
    )

    bar.extend_axis(
        yaxis=opts.AxisOpts(
            name="总销量",
            name_location="middle",
            name_gap=50,
            splitline_opts=opts.SplitLineOpts(is_show=False),
        )
    )

    return bar

# ----------------------
# 主程序（布局与原始版本完全一致）
# ----------------------
def main():
    # 设置页面布局
    st.set_page_config(layout="wide", page_title="数据大屏-示例")

    # 检查数据库配置
    if not all([db_config.get(k) for k in ["user", "password", "host", "database"]]):
        st.error("请在.secrets.toml中填写完整的数据库配置")
        return

    # 获取数据
    data = fetch_data()
    if data is None:
        return

    # 页面标题（与原始版本完全一致）
    st.title("数据大屏-示例")
    st.markdown("---")

    # 第一行：KPI指标
    st.subheader("指标展示")
    render_kpi_metrics(data)
    st.markdown("---")

    # 第二行：仪表盘和产品销量排行
    col1, col2 = st.columns([1, 2])

    with col1:
        gauge = render_sales_completion_gauge(
            sum([q['total_sales'] for q in data['sales_data']])
        )
        st_pyecharts(gauge, height=400)

    with col2:
        bar_rank = render_product_sales_rank(data)
        st_pyecharts(bar_rank, height=400)

    # 第三行：折线图和柱状图
    col1, col2 = st.columns(2)

    with col1:
        line = render_monthly_trend_line(data)
        st_pyecharts(line, height=400)

    with col2:
        bar = render_quarterly_sales_bar(data)
        st_pyecharts(bar, height=400)

    # 第四行：折柱混合图
    st.subheader("季度销量分析")
    combined = render_combined_chart(data)
    st_pyecharts(combined, height=500)

    # 底部信息
    st.markdown("---")
    st.markdown("**数据说明**: 本数据来自公司销售数据库。")

if __name__ == "__main__":
    main()