# coding = utf-8
# -*- coding: utf-8 -*-
import sys
import os

#获取当前脚本运行时的参数 如果只有1个参数(脚本自身),则打印提示信息
if len(sys.argv) == 1 :
    print('Not Find Path, arg1 is path of the ".tgz" file path.')
    #从参数获取保存压缩包的路径
    basePath = '.\\'
elif len(sys.argv) > 1 :
    #如果路径不存在 则打印'Path Is Not Exist!' 退出脚本
    if not os.path.exists(sys.argv[1]) :
        print('Path Does Not Exist!')
        basePath = '.\\'
        #从参数获取保存压缩包的路径
    else :
        basePath = sys.argv[1]

def mkdir(path):

    if not os.path.isfile(path):
        dirPath = os.path.abspath(path)
    else:
        dirPath = os.path.split(os.path.abspath(path))[0]
    if not os.path.exists(dirPath):
        os.mkdir(dirPath)
        print(u"文件夹不存在,已经创建!" ,dirPath)
    return dirPath

def getTypeFileList(basePath = basePath, *typeList):    #默认参数为脚本所在路径
    '''

    :param basePath: 为路径字符串,
    :param typeList: 为文件类型的列表 即,可以接收多个文件类型参数
    :return: 返回路径下的指定类型的文件的列表
    '''
    FlieList = []
    typeList = [n.lower() for n  in typeList]    #将列表转化为小写
    if os.path.isfile(basePath):                  #如果basePath 是一个文件
        if os.path.splitext(basePath)[1].lower() in typeList :       # 判断文件的扩展名是否在typeList 中
            return [os.path.abspath(basePath)]      # 返回文件绝对路径的列表
        else:
            return None                             # 返回 None

    #遍历压缩包所在路径,把  .tar.gz .tgz 和 .tar.gzip 文件路径保存到 zipFileList
    for path,dirs,files in os.walk(basePath):
        #path,dirs,files 对应os.walk()的返回值 元祖 的三个元素边,分别为当前路径,文件夹列表 和 文件列表
        for file in files:
            #对文件列表files进行遍历
            if os.path.splitext(file)[1].lower()  in  typeList :
                #如果扩展名为 在列表fileList 中( ['.gz', '.gzip', 'tgz']), 则把路径和文件名进行组合,并添加到zipFileList列表中
                FlieList.append(os.path.join(path, file))
    return FlieList


if __name__ == '__main__':
    getTypeFileList(basePath,'.gz', '.gzip', '.tgz')
