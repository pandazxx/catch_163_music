# -*- coding:utf8 -*-

import os
import platform

sysname = platform.system()

if 'Darvin' == sysname:
    basedir = '/Users/QQ/Documents/Music/'
elif 'Windows' == sysname:
    basedir = 'D:/Music'
    pass


def strB2Q(ustring):
    """把字符串半角转全角"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code<0x0020 or inside_code>0x7e:      #不是半角字符就返回原来的字符
            rstring += uchar
        if inside_code==0x0020: #除了空格其他的全角半角的公式为:半角=全角-0xfee0
            inside_code=0x3000
        else:
            inside_code+=0xfee0
        rstring += unichr(inside_code)
    return rstring

def make_valid(path):
    for old in ('/', '\\', ':', '<', '>', '"', '|'):
        path = path.replace(old, '')
    path = path.replace('?', strB2Q('?'))
    return path
    pass

def get_store_dir(path = './'):
    global basedir
    path = os.path.join(basedir, path)

    if not os.path.exists(path):
        os.makedirs(path)

    return path
    pass
