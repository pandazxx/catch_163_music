#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'pandazxx'

import json


class DictData(object):
    def __init__(self, **kwargs):
        dict = kwargs
        if not dict or len(dict) == 0:
            return
        required_attr_names = [x for x in dir(self) if not x.startswith('_')]
        for attr_name in required_attr_names:
            attr = getattr(self.__class__, attr_name)
            if callable(attr) \
                    or isinstance(attr, type)\
                    or type(attr) is property:
                continue
            if not attr_name in dict:
                print(type(attr))
                raise AttributeError('Required attribute "{0}" not found'.format(attr_name))
            value = dict[attr_name]
            if isinstance(attr, DictData):
                if not isinstance(value, type(dict)):
                    raise TypeError('Wrong type of value found when building <{class_name}> attribute "{attr_name}", '
                                    'required <{required_type}>, '
                                    'found <{real_type}>'.format(class_name=type(attr).__name__,
                                                                attr_name=attr_name,
                                                                required_type=type(dict).__name__,
                                                                real_type=type(value).__name__))
                self.__dict__[attr_name] = type(attr)(**value)
            else:
                self.__dict__[attr_name] = value
        for remaining_attr_name in dict.keys() - required_attr_names:
            if remaining_attr_name.startswith('_'):
                continue
            self.__dict__[remaining_attr_name] = dict.get(remaining_attr_name, None)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        props = self.__dict__.copy()
        for key, value in props.items():
            if isinstance(value, DictData):
                props[key] = value.to_dict()
        return props


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


def main():
    class test_cls1(DictData):
        required1 = None
        required2 = DictData()
        required3 = {}
        def not_required1(self): print("not_required1")
        def _not_required2(self): print("_not_required2")
        __not_required3 = '__not_required3'
        def test_desc(self):
            t1 = self
            print('required1: {0}'.format(str(self.required1)))
            print('required2: {0}'.format(str(self.required2)))
            print('required3: {0}'.format(str(self.required3)))
            print('not_required1: {0}'.format(str(self.not_required1)))
            print('_not_required2: {0}'.format(str(self._not_required2)))
            print('__not_required3: {0}'.format(str(self.__not_required3)))
            print('dict: {0}'.format(str(self.to_dict())))

    dict1 = {
        'required1': 'required1_val',
        'required2': {'extra1': 'extra1_val'},
        'required3': {'required3': 'required3_val'},
        'not_required1': "not_required1_val",
        '_not_required2': "_not_required2_val",
        '__not_required3': '__not_required3_val',
        'extra2': 'extra2_val',
        '_extra3': 'extra3_val',
    }

    dict2 = {
        'required1': 'required1_val',
        'required2': 'required2_val',
        'required3': {'required3': 'required3_val'},
        'not_required1': "not_required1_val",
        '_not_required2': "_not_required2_val",
        '__not_required3': '__not_required3_val',
        'extra2': 'extra2_val',
    }

    dict3 = {
        'required2': {'extra1': 'extra1_val'},
        'required3': {'required3': 'required3_val'},
        'not_required1': "not_required1_val",
        '_not_required2': "_not_required2_val",
        '__not_required3': '__not_required3_val',
        'extra2': 'extra2_val',
    }
    try:
        t1 = test_cls1(dict1)
        t1.test_desc()
        print('t1.required2.extra1: {0}'.format(t1.required2.extra1))
    except Exception as e:
        import traceback
        print(e)
        traceback.print_exc()
    try:
        t1 = test_cls1(dict2)
        t1.test_desc()
        print('t1.required2.extra1: {0}'.format(t1.required2.extra1))
    except Exception as e:
        import traceback
        print(e)
        traceback.print_exc()
    try:
        t1 = test_cls1(dict3)
        t1.test_desc()
        print('t1.required2.extra1: {0}'.format(t1.required2.extra1))
    except Exception as e:
        import traceback
        print(e)
        traceback.print_exc()


    pass

if __name__ == '__main__':
    main()