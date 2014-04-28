#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'pandazxx'

import hashlib

def byte_array_to_str(b_array):
    return ''.join('{:02x}'.format(x) for x in b_array)

def get_md5(src):
    i = src
    if type(src) is str:
        i = src.encode('utf-8')
    return hashlib.new('md5', i).digest()
