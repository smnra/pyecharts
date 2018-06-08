#!usr/bin/env python
#-*- coding:utf-8 _*-

"""
@author:Administrator
@file: echarts.py
@time: 2018/05/{DAY}
描述:

"""
from sqlToDatafream import *
import os,math
from pyecharts import *


tdate = getDateRange()  # 初始化日期
tdate['startDate'] = '20180528'
tdate['endDate'] = '20180606'
# tdate['now'] = None  #为 None时  不生产excel文件

sqls = sqlCollated(os.path.abspath(r'./sql/lte'), '.mysql')  # 整理sql脚本
print(sqls)
# conStr = 'oracle://omc:omc@10.100.162.10:1521/oss'                #Oracle连接字符串
conStr = 'mysql+pymysql://root:planet@127.0.0.1:10010/4g_kpi_browsing?charset=utf8'
sqlDatafream = executeSQL(sqls, conStr, tdate)  # 连接数据库,执行sql 并返回 Datafream

dft = sqlDatafream[0]

df = dft[1].sort_values(by=['地市','日期'])      #把dft[1] 排序
#df.columns #列名的集合
#df.index   #索引的集合
#df[df['CITY'] == 'Baoji'][1:10][['RANKS', 'RRC连接成功率']]



'''
line1 = df[df['地市'] == '咸阳FDD'][['日期', 'rrc建立成功率']]
line2 = df[df['地市'] == '宝鸡FDD'][['日期', 'rrc建立成功率']]
line3 = df[df['地市'] == '西安FDD'][['日期', 'rrc建立成功率']]
page = Page()
bar = Bar('RRC建立成功率:', dft[0])   # 图表 line的标题和副标题
bar_2 = Bar('RRC建立成功率2:', dft[0])   # 图表 line的标题和副标题
line = Line('RRC建立成功率:', dft[0])   # 图表 line的标题和副标题
line_2 = Line('RRC建立成功率line2:', dft[0])   # 图表 line的标题和副标题


line.add('咸阳FDD', line1['日期'], line1['rrc建立成功率'], mark_line=["rrc建立成功率"], mark_point=["max", "min"], yaxis_min=90, is_more_utils=True)
line.add('宝鸡FDD', line2['日期'], line2['rrc建立成功率'], mark_line=["rrc建立成功率"], mark_point=["max", "min"], yaxis_min=90, is_more_utils=True)
line.add('西安FDD', line3['日期'], line3['rrc建立成功率'], mark_line=["rrc建立成功率"], mark_point=["max", "min"], yaxis_min=90, is_more_utils=True)
bar.add('咸阳FDD', line1['日期'], line1['rrc建立成功率'], mark_line=["rrc建立成功率"], mark_point=["max", "min"], yaxis_min=90, is_more_utils=True)
bar.add('宝鸡FDD', line2['日期'], line2['rrc建立成功率'], mark_line=["rrc建立成功率"], mark_point=["max", "min"], yaxis_min=90, is_more_utils=True)
bar.add('西安FDD', line3['日期'], line3['rrc建立成功率'], mark_line=["rrc建立成功率"], mark_point=["max", "min"], yaxis_min=90, is_more_utils=True)
line_2.add('咸阳FDD', line1['日期'], line1['rrc建立成功率'], mark_line=["rrc建立成功率"], mark_point=["max", "min"], yaxis_min=90, is_more_utils=True)
line_2.add('宝鸡FDD', line2['日期'], line2['rrc建立成功率'], mark_line=["rrc建立成功率"], mark_point=["max", "min"], yaxis_min=90, is_more_utils=True)
line_2.add('西安FDD', line3['日期'], line3['rrc建立成功率'], mark_line=["rrc建立成功率"], mark_point=["max", "min"], yaxis_min=90, is_more_utils=True)
bar_2.add('咸阳FDD', line1['日期'], line1['rrc建立成功率'], mark_line=["rrc建立成功率"], mark_point=["max", "min"], yaxis_min=90, is_more_utils=True)
bar_2.add('宝鸡FDD', line2['日期'], line2['rrc建立成功率'], mark_line=["rrc建立成功率"], mark_point=["max", "min"], yaxis_min=90, is_more_utils=True)
bar_2.add('西安FDD', line3['日期'], line3['rrc建立成功率'], mark_line=["rrc建立成功率"], mark_point=["max", "min"], yaxis_min=90, is_more_utils=True)

page.add(line)
page.add(line_2)
page.add(bar)
page.add(bar_2)

page.render(r'./HTML/pyecharts_2.html')  # 保存为本地HTML单文件
'''




#作图
# grid = Grid()   #将多张图合并为一张的容器
page = Page()   #将多张图放到一个网页
timeline = Timeline(is_auto_play=True, timeline_bottom=0)

lines = []
lineXianyang = []
lineBaoji = []
lineXian = []

style = Style()

#line的样式
line_style = style.add(
    mark_point=["max", "min"],      # Line中显示最大值和最小值的标签
    is_smooth=True,                 # 平滑曲线
    is_more_utils=True,             # 图表显示工具栏
    mark_point_symbol='pin',         # 标记点图形，，默认为'pin'，有'circle', 'rect', 'roundRect', 'triangle', 'diamond', 'pin', 'arrow'可选
    mark_point_symbolsize=60,        # 标记点图形大小 默认为50
    # yaxis_max="dataMax",           # Y 坐标轴刻度最大值，默认为自适应。使用特殊值 "dataMax" 可自定以数据中最小值为 x 轴最大值。
    # yaxis_min="dataMin",           #  Y 坐标轴刻度最小值，
    is_splitline_show=False,          # 是否显示 y 轴网格线，默认为 True。
    xaxis_rotate=45,                 # X轴标签旋转度数
    is_datazoom_show=True,          #显示图表缩放工具
    datazoom_type='both',           #缩放类型
    datazoom_range=[0, 100],          # 默认的缩放范围
    datazoom_orient='vertical'       #datazoom 组件在直角坐标系中的方向，默认为 'horizontal'，效果显示在 x 轴。如若设置为 'vertical' 的话效果显示在 y 轴。
)

for i,kpiName in enumerate(df.columns):
    if i>=2:
        #选取指定KPI的数据
        lineXianyang.append(df[df['地市'] == '咸阳FDD'][['日期', kpiName]])
        lineBaoji.append(df[df['地市'] == '宝鸡FDD'][['日期', kpiName]])
        lineXian.append(df[df['地市'] == '西安FDD'][['日期', kpiName]])

        #确定Y轴的最大值和最小值
        line_style['yaxis_max'] = math.ceil(df[kpiName].max() + (df[kpiName].max() -df[kpiName].min())*0.5)
        line_style['yaxis_min'] = math.floor(df[kpiName].min() - (df[kpiName].max() -df[kpiName].min())*0.5)

        #给chart中添加line
        lines.append(Line(kpiName, dft[0], height=400 ))  # 图表 line的标题和副标题
        lines[i-2].add('咸阳FDD', lineXianyang[i-2]['日期'], lineXianyang[i-2][kpiName], mark_line=[kpiName], **line_style)
        lines[i-2].add('宝鸡FDD', lineBaoji[i-2]['日期'], lineBaoji[i-2][kpiName], mark_line=[kpiName], **line_style)
        lines[i-2].add('西安FDD', lineXian[i-2]['日期'], lineXian[i-2][kpiName], mark_line=[kpiName], **line_style)


        # grid.add(lines[i-2])
        page.add(lines[i-2])
        timeline.add(lines[i-2], kpiName)

# grid.render(r'./HTML/grid.html')  # 保存为本地HTML单文件
page.render(r'./HTML/page.html')  # 保存为本地HTML单文件
timeline.render(r'./HTML/timeline.html')




