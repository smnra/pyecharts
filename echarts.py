#!usr/bin/env python  
#-*- coding:utf-8 _*-  

""" 
@author:Administrator 
@file: echarts.py 
@time: 2018/05/{DAY} 
描述: 

"""

import pandas as pd
from pyecharts import Bar



attr = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
v1 = [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]
v2 = [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3]
bar = Bar("Bar chart", "precipitation and evaporation one year")
bar.add("precipitation", attr, v1, mark_line=["average"], mark_point=["max", "min"])
bar.add("evaporation", attr, v2, mark_line=["average"], mark_point=["max", "min"])
#bar.render()
bar.render(r'./HTML/pyecharts_2.html')      #保存为本地HTML单文件
bar                               #在jupyter 中 显示



if htmlFileName != None:
    htmlFileName = os.path.abspath(htmlFileName)  # 转化为绝对路径
    # 下面为图表:
    dfec = tables[0].loc[
        df['CITY'] == 'Baoji', ['RANKS', 'RRC连接成功率']]  # 选取tables[0] 中 CITY='Baoji' 的 'CITY', 'RRC连接成功率' 两列数据
    dfec = tables[0].loc[df['RANKS'] == 1, ['CITY', 'RRC连接成功率']]
    bar = Bar(sql[0], col[5])
    bar.add(col[5], dfec['CITY'], dfec['RRC连接成功率'], mark_line=["average"], mark_point=["max", "min"])
    # bar.render()
    bar.render(r'./HTML/pyecharts_2.html')  # 保存为本地HTML单文件

