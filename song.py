# -*- coding:utf8 -*-

import search
import urllib2

url_detail = 'http://music.163.com/api/song/detail/?id=%d&ids=[%d]'

class Song(object):
    def __init__(self, id = 0):
        self.__get_detail(id)
        pass

    def __get_detail(self, id):
        if not self.__valid_id(id):
            return

        ret = search.get(url_detail % (id, id))
        song = ret['songs'][0]
        self.title = song['lMusic']['name']
        self.artists = [a['id'] for a in song['artists']]
        self.url = song['mp3Url']
        pass

    def get_artists(self):
        return self.artists
        pass

    def get_title(self):
        return self.title
        pass

    def __valid_id(self, id):
        return id
        pass

    def down_load(self, id = 0):
        self.__get_detail(id)

        song_file = self.title + '.mp3'

        for old in ('/', '\\', ':', '?', '<', '>', '"', '|'):
            song_file = song_file.replace(old, '')
        f = urllib2.urlopen(self.url)
        open(song_file, "wb").write(f.read())
        pass

def main():
    s = Song(26269002)
    print s.down_load()
    pass

if __name__ == '__main__':
    main()