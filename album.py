# -*- coding:utf8 -*-
import search
import song

url_album_detail = 'http://music.163.com/api/album/%d'

class Album(object):
    """Get Detail of Album"""

    def __init__(self, name = '', id = 0):
        if id:
            self.id(id)
            pass
        pass

    def id(self, id):
        self.fit = search.get(url_album_detail % (id))
        pass

    def get_fit(self):
        return self.fit
        pass

    def get_songs(self, newdir = True):
        path = newdir and self.fit['album']['name'] or './'
        s = song.Song()
        [s.down_load(one['id'], path) for one in self.fit['album']['songs']]
        pass

def main():
    a = Album(id = 28285)
    print a.get_songs()
    pass

if __name__ == '__main__':
    main()