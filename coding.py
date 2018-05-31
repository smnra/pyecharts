#!usr/bin/env python  
#-*- coding:utf-8 _*-  

""" 
@author:SMnRa
@file: coding.py 
@time: 2018/05/{DAY} 
描述: 本模块用于对位置编码格式的unicode str字符串 或者
      二进制bytes 格式 数据进行转化为  utf-8 或者二进制bytes格式数据
"""
import chardet

def to_str(bytes_or_str):
    """
    不管输入的参数 bytes_or_str 是 二进制的 bytes 还是
    unicode utf-8 格式的 str,函数的返回值 均为unicode utf-8 的str
    """
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value

def to_bytes(bytes_or_str):
    """
    不管输入的参数 bytes_or_str 是 二进制的 bytes 还是
    unicode utf-8 格式的 str,函数的返回值 均为二进制的bytes
    """
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode('utf-8')
    else:
        value = bytes_or_str
    return value


if __name__=='__main__':
    print("""
    此模块包含两个函数:
    to_str(bytes_or_str)
    不管输入的参数 bytes_or_str 是 二进制的 bytes 还是
    unicode utf-8 格式的 str,函数的返回值 均为unicode utf-8 的str.
    
    to_bytes(bytes_or_str)
    不管输入的参数 bytes_or_str 是 二进制的 bytes 还是
    unicode utf-8 格式的 str,函数的返回值 均为二进制的bytes.
    """)
