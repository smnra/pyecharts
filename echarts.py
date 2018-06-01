#!usr/bin/env python  
#-*- coding:utf-8 _*-  

""" 
@author:Administrator 
@file: echarts.py 
@time: 2018/05/{DAY} 
描述: 

"""
from OracleSQL import *
import os
from pyecharts import Bar,Line,Pie

attr = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
v1 = [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]
v2 = [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3]
bar = Bar("Bar chart", "precipitation and evaporation one year")
bar.add("precipitation", attr, v1, mark_line=["average"], mark_point=["max", "min"])
bar.add("evaporation", attr, v2, mark_line=["average"], mark_point=["max", "min"])
#bar.render()
bar.render(r'./HTML/pyecharts_2.html')      #保存为本地HTML单文件
bar                               #在jupyter 中 显示


sqls = sqlCollated(os.path.abspath(r'./sql/lte'))  # 整理sql脚本
#print(sqls)
conStr = 'omc/omc@10.100.162.10/oss'  # Oracle连接字符串
sqlDf = executeSQL(sqls, conStr)  # 连接数据库,执行sql 并返回 Datafream






dft = sqlDf[0]
df = dft[1].sort_values(by=['CITY','RANKS'])      #把dft[1] 排序
df.columns #列名的集合
df.index   #索引的集合


#df[df['CITY'] == 'Baoji'][1:10][['RANKS', 'RRC连接成功率']]
# 下面为图表:
bar = Bar(dft[0],'Baoji')
bar.add('Baoji', df[df['CITY'] == 'Baoji'][1:10]['RANKS'], df[df['CITY'] == 'Baoji'][1:10]['RRC连接成功率'], mark_line=["RRC连接成功率"], mark_point=["max", "min"])# bar.render()
bar.render(r'./HTML/pyecharts_2.html')  # 保存为本地HTML单文件

line = Line('Top_N统计:', dft[0])
line.add('Baoji',  df[df['CITY'] == 'Baoji'][1:10]['RANKS'], df[df['CITY'] == 'Baoji'][1:10]['RRC连接成功率'], mark_line=["RRC连接成功率"], mark_point=["max", "min"], yaxis_min=90, is_more_utils=True)
line.add('Xian',  df[df['CITY'] == 'Xian'][1:10]['RANKS'], df[df['CITY'] == 'Xian'][1:10]['RRC连接成功率'], mark_line=["RRC连接成功率"], mark_point=["max", "min"], yaxis_min=90)
line.add('Xianyang',  df[df['CITY'] == 'Xianyang'][1:10]['RANKS'], df[df['CITY'] == 'Xianyang'][1:10]['RRC连接成功率'], mark_line=["RRC连接成功率"], mark_point=["max", "min"], yaxis_min=90)



pie = Pie('Top_N统计:')
pie.add('Baoji',  df[df['CITY'] == 'Baoji'][1:10]['RANKS'], df[df['CITY'] == 'Baoji'][1:10]['RRC连接成功率'], mark_line=["RRC连接成功率"], mark_point=["max", "min"], yaxis_min=90, is_more_utils=True)
pie.render(r'./HTML/pyecharts_2.html')  # 保存为本地HTML单文件











