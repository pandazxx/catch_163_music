# -*- coding:utf8 -*-
import search

url4album = 'http://music.163.com/api/artist/albums/%d?limit=%d&offset=%d'

class Artist(object):
    """Get Detail of Artist"""

    def __init__(self, name = '', id = 0):
        self.name = name
        self.__search(name)
        pass

    def __search(self, name):
        res = search.search(name, 'artist')
        self.count = res['artistCount']
        self.artists = res['artists']
        self.fit = self.get_best()
        pass

    def __id(self, art):
        return art['id']
        pass

    def get_all(self):
        return self.artists
        pass

    def get_best(self):
        return self.artists[0]
        pass

    def get_top(self, top):
        pass

    def get_albums(self, limit = 10):
        url = url4album % (self.__id(self.fit), limit, 0)
        return search.get(url)
        pass

def main():
    a = Artist('beyond')
    print a.get_albums()
    pass

if __name__ == '__main__':
    main()        