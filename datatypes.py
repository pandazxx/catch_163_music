#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'pandazxx'

import json


class StdData(dict):
    def __init__(self, **kwargs):

        for val in dir(self):
            if val.startswith('_'):
                continue

            attr = getattr(self, val)

            if not callable(attr) and not (isinstance(attr, type) and issubclass(attr, StdData)):
                self.__dict__[val] = kwargs.get(val, None)

            elif isinstance(attr, type) and issubclass(attr, StdData):
                data = kwargs.get(val, {})
                if isinstance(data, dict):
                    self.__dict__[val] = attr(**data)

    def __repr__(self):

        return self.__str__()

    def __str__(self):

        return str(self.to_dict())

    def to_dict(self):
        """ 转为dict """
        props = self.__dict__.copy()

        for key, value in props.items():

            prop_type = type(value)

            if value is None:
                value = ''

            elif prop_type is bool:
                value = str(value).lower()

            elif prop_type is dict:
                value = json.dumps(value)

            elif prop_type is list:
                lst = []
                for item in value:
                    if isinstance(item, StdData):
                        item = item.to_dict()
                    lst.append(item)
                value = json.dumps(lst)

            elif isinstance(value, StdData):
                value = value.to_dict()

            props[key] = value

        return props
