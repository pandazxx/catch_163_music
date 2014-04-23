#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'pandazxx'

import requests

import util


class Session(object):
    __BASE_REFERER = "http://music.163.com/"
    __MY_REFERER = __BASE_REFERER + "my"
    __API_URL = 'http://music.163.com/api/'
    __API_LOGIN_URL = __API_URL + 'login'
    __USER_PLAY_LIST_PATH = 'user/playlist'

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
        headers = Session.__BASE_HEADERS

        post_data = {
            'username': username,
            'password': util.get_md5(password),
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
        headers = Session.__BASE_HEADERS
        headers.update({"Referer": Session.__MY_REFERER})

        resp = requests.get(Session.__API_URL + Session.__USER_PLAY_LIST_PATH, params=paramers, headers=headers)

        return resp


def main():
    from sys import argv

    if len(argv) < 3:
        print("Usage: username password")
        exit(1)

    username = argv[1]
    password = argv[2]

    print("username: {0}\npassword: {1}".format(username, password))

    s = Session()
    s.login(username, password)
    print(s.get_collections().json()['playlist'][0])


if __name__ == '__main__':
    main()