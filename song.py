# -*- coding:utf8 -*-
import os.path
import search
import urllib2
import mypath
import time

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

    def __get_full_path(self, path, filename):
        return os.path.join(mypath.get_store_dir(path), filename)
        pass

    def down_load(self, id = 0, path = './'):
        self.__get_detail(id)
        song_file = self.title + '.mp3'
        song_file = mypath.make_valid(song_file)

        request = urllib2.Request(self.url)
        # request.add_header('Host', 'music.163.com')
        # request.add_header('Referer', 'http://music.163.com/')
        request.add_header('Connection', 'keep-alive')
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36')
        f = urllib2.urlopen(request)
        time.sleep(10)

        open(self.__get_full_path(path, song_file), "wb").write(f.read())
        pass

def main():
    s = Song(26269002)
    print s.down_load()
    pass

if __name__ == '__main__':
    main()