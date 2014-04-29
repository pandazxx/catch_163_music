#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'pandazxx'

import requests
import util
import datatypes
import dataobjs


class Session(object):
    __BASE_REFERER = "http://music.163.com/"
    __MY_REFERER = __BASE_REFERER + "my"
    __API_URL = 'http://music.163.com/api/'
    __API_LOGIN_URL = __API_URL + 'login'
    __USER_PLAY_LIST_PATH = 'user/playlist'
    __PLAY_LIST_DETAIL_URL = __API_URL + 'playlist/detail'  #

    __BASE_HEADERS = {
        'Content-Type': 'application/x-www-form-urlencoded',
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1)"
                      " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36",
        "Accept-Language": "zh-cn",
        "Accept-Encoding": "gzip;deflate",
        "Connection": "keep-alive",
        "Referer": __BASE_REFERER,
    }

    def __init__(self):
        self.__profile = {}
        self.__csrf = ""
        self.__user_playlist = {}
        pass

    def login(self, username, password):
        headers = Session.__BASE_HEADERS.copy()

        post_data = {
            'username': username,
            'password': util.byte_array_to_str(util.get_md5(password)),
            'rememberLogin': 'true'
        }

        resp = requests.post(Session.__API_LOGIN_URL, data=post_data, headers=headers)

        self.__profile = resp.json()['profile']
        self.__csrf = resp.cookies['__csrf']

    @property
    def csrf(self):
        return self.__csrf

    @property
    def uid(self):
        return self.__profile['userId']

    def get_collections(self):
        paramers = {
            'offset': '0',
            'limit': '500',
            'uid': self.uid
        }
        headers = Session.__BASE_HEADERS.copy()
        headers.update({"Referer": Session.__MY_REFERER})

        resp = requests.get(Session.__API_URL + Session.__USER_PLAY_LIST_PATH, params=paramers, headers=headers)

        ret = []
        for pl_dict in resp.json()['playlist']:
            playlist = dataobjs.PlayList(pl_dict)
            ret.append(playlist)

        return ret

    def song_details_from_playlist(self, playlist):
        params = {
            'id': playlist.id,
            'offset': 0,
            'total': 'true',
            'limit': 500
        }
        headers = Session.__BASE_HEADERS.copy()
        headers.update({"Referer": Session.__MY_REFERER})
        resp = requests.get(Session.__PLAY_LIST_DETAIL_URL, params=params, headers=headers)
        # print(resp.json()['result']['tracks'][0]['hMusic'])
        # print(type(resp.json()['result']['tracks'][0]['hMusic']))
        ret = []
        for song_dict in resp.json()['result']['tracks']:
            try:
                song = dataobjs.Song(song_dict)
                ret.append(song)
            except Exception as e:
                print("Error loading song due to {error}".format(error=e))
                print("     Dict Value: {value}".format(value=song_dict))
        return ret


def main():
    from sys import argv

    if len(argv) < 3:
        print("Usage: username password")
        exit(1)

    username = argv[1]
    password = argv[2]

    s = Session()
    s.login(username, password)
    # print(s.get_collections().json()['playlist'][0])
    # d = datatypes.DictData(s.get_collections().json()['playlist'][0])
    # print(d.name)
    # print(d.id)

    download_list = []
    dest_dir = "/tmp/"
    for pl in s.get_collections():
        print('Playlist({id}): {name}'.format(id=pl.id, name=pl.name))
        for song in s.song_details_from_playlist(pl):
            print('Song({id})<{bit_rate}> {name}: {url}'.format(id=song.id,
                                                                name=song.bMusic.name,
                                                                bit_rate=song.bMusic.bitrate,
                                                                url=song.download_url()))
            download_list.append(song)
            # if song.bMusic.bitrate != 320000:
            #     print('Song<{name}> hMusic:<{hMusic}>'.format(name=song.bMusic.name, hMusic=song.hMusic))
            #     print('Song<{name}> mMusic:<{hMusic}>'.format(name=song.bMusic.name, hMusic=song.mMusic))
            #     print('Song<{name}> lMusic:<{hMusic}>'.format(name=song.bMusic.name, hMusic=song.lMusic))
    import downloadtool
    download_tool = downloadtool.get_download_tool("aria2")
    for song in download_list[0:1]:
        download_tool.download(uri=song.download_url(), path=song.bMusic.name+'.'+song.bMusic.extension)


if __name__ == '__main__':
    main()