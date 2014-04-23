#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'pandazxx'

import hashlib


def get_md5(src):
    return hashlib.new('md5', src.encode('utf-8')).hexdigest()
