# -*- coding:utf8 -*-

import urllib2
import urllib
import json


def get(url):
    return json.loads(urllib2.urlopen(url).read())
    pass

def search(name, t = 'song'):

    type_dict = {'song':'1', 'alubm':'10','artist':'100', 'playlist':'1000', 'user':'1002'}

    data = {'s': name,
            '_page':'search',
            'type': type_dict[t],
            'limit':'90',
            'offset':'0',
            'total':'true'}
    f = urllib2.urlopen(
        url  = 'http://music.163.com/api/search/get',
        data = urllib.urlencode(data))

    return json.loads(f.read())['result']
    pass
