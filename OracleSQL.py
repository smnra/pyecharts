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


tdate = getDateRange()
start_datetime = tdate['yesday']  # 昨天的日期 '20180529'
end_datetime = tdate['today'] # 今天的日期 '20180530'


def sqlCollated(sqlFilePath):
    '''
    此函数的功能为 查找给出参数路径下的 '.SQL' 文件,并返回 文件名字(不包含扩展名) 和 文件内容的元组构成的列表
    :param sqlFilePath: 存储 .SQL 文件的 路径
    :return: 为一个二元列表 [('文件名1', '文件内容1'), ('文件名2', '文件内容2'), ('文件名n', '文件内容n')]
    '''
    sqlFiles = getfiles.getTypeFileList(os.path.abspath(sqlFilePath), '.SQL')  #获取 '.SQL' 文件列表 此处不区分大小写
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
    newsql = sql.replace('&start_datetime',start_datetime)
    newsql = newsql.replace('&end_datetime',end_datetime)
    #newsql = newsql.decode('utf-8')
    return newsql

sqls = sqlCollated(os.path.abspath(r'./sql/lte'))

def executeSQL(sqls,conStr,excelFileName=r'./output/' + tdate['today'] + '/excel.xlsx', htmlFileName=r'./output/' + tdate['today']):
    '''

    :param sqls: 为一个二元列表 [('sqlName1', 'sqlScript1'), ('sqlName2', 'sqlScript2'), ('sqlNameN', 'sqlScriptN')].
    :param conStr: 为Oracle 连接的字符串,例如:conStr = 'omc/omc@10.100.162.10/oss'
            ('user/password@host:port/servicename') 默认端口1521可以省略.
    :param excelFileName  可选参数,默认值为 (r'./output/' + tdate['today'] + '/excel.xlsx') 即将结果保存为excel 文件的路径
            excelFileName 为 None 时 不保存excel文件.
    :return: 返回 (文件名,Datafream) 的 列表 文件名为参数中的sql文件名,
             Datafream 为从数据库中取得的表转化为Datafream
    '''
    conn = cx_Oracle.connect(conStr)       #建立与oracle数据库的连接, 格式为  'user/password@IP/servicename'
    cursor = conn.cursor()																  #连接的游标

    tables = []   #保存DataFream的数组
    for i,sql in enumerate(sqls) :
        #遍历执行每一个sql语句,并将结果转化为Datafream对象  添加到列表 tables 中
        cursor.execute(proessSQL(sql[1]))  # 执行的sql语句
        rows = cursor.fetchall()        #一次取回所有记录,保存到rows中. rows为一个 列表, rows的元素还是一个列表,所以他的结构 就是 rows的每一个元素为一个列表(一行记录)
        col = [str[0] for str in cursor.description]       #col 为字段名的 列表
        df = pd.DataFrame(rows,columns = col)         #转化为DataFream  并添加 列表 col 为列名
        tables.append(df)                           #将df添加到tables 列表
        if excelFileName!=None:
            excelFileName = os.path.abspath(excelFileName)      #转化为绝对路径
            df.to_excel(excelFileName,sheet_name=sql[0],columns=col, header=True, index=False)    #保存为excel文件

        if htmlFileName!=None:
            htmlFileName = os.path.abspath(htmlFileName)  # 转化为绝对路径
            #下面为图表:
            dfec = tables[0].loc[df['CITY'] == 'Baoji', ['RANKS', 'RRC连接成功率']]    #选取tables[0] 中 CITY='Baoji' 的 'CITY', 'RRC连接成功率' 两列数据
            dfec = tables[0].loc[df['RANKS'] == 1, ['CITY', 'RRC连接成功率']]
            bar = Bar(sql[0],col[5])
            bar.add(col[5], dfec['CITY'], dfec[ 'RRC连接成功率'], mark_line=["average"], mark_point=["max", "min"])
            #bar.render()
            bar.render(r'./HTML/pyecharts_2.html')      #保存为本地HTML单文件

    cursor.close()                    #关闭游标
    conn.close()						 #关闭数据库连接
    zip([name[0] for name in sqls],tables)

    return list(zip([name[0] for name in sqls],tables))  # 返回 (文件名,Datafream) 的 列表







if __name__=='__main__':
    sqls = sqlCollated(os.path.abspath(r'./sql/lte'))
    print(sqls)
    conStr = 'omc/omc@10.100.162.10/oss'