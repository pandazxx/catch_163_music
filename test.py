# -*- coding:utf8 -*-

import urllib2
import urllib
import json
from urlparse import urlsplit 

def search_playlist(name):
    data = {'s': name,
            '_page':'search',
            'type':'1000',
            'limit':'30',
            'offset':'0',
            'total':'true'}
    f = urllib2.urlopen(
        url  = 'http://music.163.com/api/search/get',
        data = urllib.urlencode(data))

    return f.read()
    pass

def parse_playlist_search(pl_org):
    p = json.loads(pl_org)['result']
    list_count = p['playlistCount']
    lists = p['playlists']
    return lists
    pass

def get_best(pls):
    bookCount = 0
    for l in pls:
        if l['bookCount'] > bookCount:
            best = l
            bookCount = l['bookCount']

    return best['id']
    pass 

def get_playlist_detail(id):
    f = urllib2.urlopen('http://music.163.com/api/playlist/detail?id=' + str(id))
    return f.read()
    pass

def parse_playlist(pl_org):
    p = json.loads(pl_org)['result']
    ret = []
    for o in p['tracks']:
        ret.append({'title':o['lMusic']['name'], 'url':o['mp3Url']})

    return ret
    pass

def download_song(song):
    song_file = song['title'] + '.mp3'

    request = urllib2.Request(song['url'])
    request.add_header('Host', 'music.163.com')
    request.add_header('Referer', 'http://music.163.com/')
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36')
    f = urllib2.urlopen(request)
    open(song_file, "wb").write(f.read())
    pass
    

search_res_org = search_playlist('日系经典纯音')
pls = parse_playlist_search(search_res_org)
best = get_best(pls)

playlist_org = get_playlist_detail(2190115)
pls = parse_playlist(playlist_org)

for p in pls:
    download_song(p)
# download_song(pls)
