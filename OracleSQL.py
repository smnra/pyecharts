# coding = utf-8
# -*- coding: utf-8 -*-
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.AL32UTF8'            #设置环境变量
#os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.ZHS16GBK'
os.environ["PATH"] = 'D:\\instantclient_12_1' + ';' +os.environ["PATH"]  #给PATH中添加 ''D:\instantclient_12_1'
os.path.sys.path.insert(0, 'D:\\instantclient_12_1')
os.environ['ORACLE_HOME'] = 'D:\\instantclient_12_1'
os.environ['TNS_ADMIN'] = 'D:\\instantclient_12_1'


import coding
import cx_Oracle
import arrow         #导入 时间日期 模块
import pandas as pd
import getfiles
from sqlalchemy import create_engine #mysql 支持
from pyecharts import Bar





def getDateRange():
    '''
    获取参数(默认为当天)所在月份的第一个完整周 周一的日期
    此函数返回一个字典,格式为
    {'yesday': '20180528',  #昨天的日期
     'today': '20180529',   #今天的日期
     'startDate': '20180501', #开始的日期
     'endDate': '20180601'  #结束的日期
    }
    '''
    now = arrow.now()                                                        #当前时间
    rangeDate={}                                                             #定义返回值  字典
    rangeDate['today'] = arrow.now().format('YYYYMMDD')                 #今日的日期
    rangeDate['yesday'] = arrow.now().replace(days = -1).format('YYYYMMDD')  # 昨天日的日期
    rangeDate['now'] = arrow.now().format('YYYYMMDDHHMISS')

    lastMonth_1st_day = now.floor('month').replace(months = -1)             #上个月1号的日期
    thisMonth_1st_day = now.floor('month')                                  #这个月1号的日期
    nextMonth_1st_day = now.floor('month').replace(months = +1)             #下个月1号的日期
    lastWeek_Monday = now.replace(weeks = -1).floor('week')             #上一周周一的日期
    thisWeek_Monday = now.floor('week')                                 #这一周周一的日期
    if thisMonth_1st_day.isoweekday() == 1 :                                #如果这个月的1号是周一,
        thisMonth_1st_Monday = now.floor('month')                           #则这个月的第一个完整周 的 周一的日期 就是当月的1号的日期
    else :
        thisMonth_1st_Monday = now.floor('month').replace(weeks = +1).floor('week')      #否则这个月的第一个完整周 的 周一的日期 就是当月1号所在的下一周的周一的日期

    if thisWeek_Monday - thisMonth_1st_Monday == thisWeek_Monday - thisWeek_Monday :       #如果 这一周周一的日期  减去这个月的第一个完整周 周一的日期 如果结果等于0
        rangeDate['startDate'] = lastMonth_1st_day.format('YYYYMMDD')               #开始时间就是上个月1号
        rangeDate['endDate'] = thisMonth_1st_Monday.format('YYYYMMDDH')               #结束时间就是这个月的第一个完整周 周一的日期
    else :
        rangeDate['startDate'] = thisMonth_1st_day.format('YYYYMMDD')               #开始时间就是这个月1号
        rangeDate['endDate'] = nextMonth_1st_day.format('YYYYMMDD')                 #结束时间就是这个月的第一个完整周 周一的日期

    return rangeDate

tdate = getDateRange()  #初始化日期

def sqlCollated(sqlFilePath,extensionFileName):
    '''
    此函数的功能为 查找给出参数路径下的 '.SQL' 文件,并返回 文件名字(不包含扩展名) 和 文件内容的元组构成的列表
    :param sqlFilePath: 存储 .SQL 文件的 路径
    :return: 为一个二元列表 [('文件名1', '文件内容1'), ('文件名2', '文件内容2'), ('文件名n', '文件内容n')]
    '''
    sqlFiles = getfiles.getTypeFileList(os.path.abspath(sqlFilePath), extensionFileName)  #获取 '.SQL' 文件列表 此处不区分大小写
    sqls = []    #存储sql脚本的列表
    sqlFileNames = [] #存储sql文件的文件名 ,不包含 扩展名.SQL
    for i,sqlFile in enumerate(sqlFiles) :
        #此处为遍历找到的.SQL文件,并将sql语句存入slqs列表中
        #将文件名存入sheetName 列表中
        sqlFileNames.append(os.path.basename(sqlFile).split(".")[0])    #将文件名添加到sqlFileNames 列表
        tmp = open(sqlFile,mode='r', encoding='utf-8')
        try:
            sqls.append(tmp.read())
        except Exception as e :
            print(str(e))
        finally:
            tmp.close()
    return  list(zip(sqlFileNames,sqls))


def proessSQL(sql) :
    #此函数为替换plsql脚本中的变量 为  &start_datetime 为 start_datetime的值
    newsql = sql.replace('&start_datetime',tdate['yesday'])
    newsql = newsql.replace('&end_datetime',tdate['today'])
    #newsql = newsql.decode('utf-8')
    return newsql

def executeSQL(sqls,conStr,excelFileName=r'./output/' + tdate['today'] ):
    '''

    :param sqls: 为一个二元列表 [('sqlName1', 'sqlScript1'), ('sqlName2', 'sqlScript2'), ('sqlNameN', 'sqlScriptN')].
    :param conStr: 为Oracle 连接的字符串,例如:conStr = 'oracle://omc:omc@10.100.162.10:1521/oss'
            ('oracle://user:password@ip:port/servicename') 默认端口1521可以省略.
            或者 'mysql+pymysql://root:planet@127.0.0.1:10010/4g_kpi_browsing?charset=utf8'
    :param excelFileName  可选参数,默认值为 (r'./output/' + tdate['today'] + '/excel.xlsx') 即将结果保存为excel 文件的路径
            excelFileName 为 None 时 不保存excel文件.
    :return: 返回 (文件名,Datafream) 的 列表 文件名为参数中的sql文件名,
             Datafream 为从数据库中取得的表转化为Datafream
    '''
    engine = create_engine(conStr)  #创建数据库引擎
    if excelFileName != None:
        getfiles.mkdir(os.path.abspath(excelFileName))  # 确认文件夹存在,不存在则建立此文件夹
        fileName = os.path.join(os.path.abspath(excelFileName), tdate['yesday'] + "_" + tdate['today'] + "_" + tdate['now'] + ".xlsx")
        excelWriter = pd.ExcelWriter(fileName)  # 创建 excelWriter
    else:
        excelWriter = None

    tables = []   #保存DataFream的数组
    for i,sql in enumerate(sqls) :
        #遍历执行每一个sql语句,并将结果转化为Datafream对象  添加到列表 tables 中
        df = pd.read_sql(proessSQL(sql[1]), engine)  # read_sql直接返回一个DataFrame对象
        tables.append(df)                           #将df添加到tables 列表
        if excelWriter:
            tables[i].to_excel(excelWriter,sql[0])    # 给excelWriter 添加sheet
    if  excelWriter:
        excelWriter.save()  # 保存excel文件 注意: 此处保存excelWriter 需要等待所有sheet均写入后
                            #  一次保存 否则 excelWriter 关闭后只能有一个sheet
    return list(zip([name[0] for name in sqls],tables))  # 返回 (文件名,Datafream) 的 列表




if __name__=='__main__':
    sqls = sqlCollated(os.path.abspath(r'./sql/lte'),'.mysql')    #整理sql脚本
    print(sqls)
    #conStr = 'oracle://omc:omc@10.100.162.10:1521/oss'                #Oracle连接字符串
    conStr = 'mysql+pymysql://root:planet@127.0.0.1:10010/4g_kpi_browsing?charset=utf8'
    sqlDf = executeSQL(sqls,conStr)                         #连接数据库,执行sql 并返回 Datafream














































