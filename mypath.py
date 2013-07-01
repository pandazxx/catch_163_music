# -*- coding:utf8 -*-

import os

def get_store_dir(path = './'):
    path = os.path.join('/Users/QQ/Documents/Music/', path)
    if not os.path.exists(path):
        os.makedirs(path)

    return path
    pass
