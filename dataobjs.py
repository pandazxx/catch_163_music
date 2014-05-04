__author__ = 'pandazxx'

import datatypes
import util
import base64

class PlayList(datatypes.DictData):
    id = -1
    name = ""

class MusicInfo(datatypes.DictData):
    id = -1
    extension = 'mp3'
    size = -1
    dfsId = ""
    name = ""
    bitrate = -1

class Song(datatypes.DictData):
    id = -1
    bMusic = MusicInfo()

    def download_url(self):
        base_url = 'http://m2.music.126.net'
        enId = self._encrypted_id(str(self.bMusic.dfsId))
        return '%s/%s/%s.%s' % (base_url, enId, self.bMusic.dfsId, self.bMusic.extension)

    @staticmethod
    def _encrypted_id(song_dfsId):
        byte1 = bytearray(b'3go8&$8*3*3h0k(2)2')
        byte2 = bytearray(song_dfsId.encode('utf-8'))
        byte1_len = len(byte1)
        for i in range(len(byte2)):
            byte2[i] = byte2[i] ^ byte1[i % byte1_len]
        result = base64.b64encode(util.get_md5(byte2)).decode('ascii')
        result = result.replace('/', '_')
        result = result.replace('+', '-')
        return result

class AlbumInfo(datatypes.DictData):
    name = ""
    id = -1

class AlbumDetail(datatypes.DictData):
    name = ""
    id = -1
    songs = datatypes.ArrayObject(Song)
    # def __init__(self, **kwargs):
    #     dict = kwargs
    #     super(AlbumDetail, self).__init__(**dict)

    # @property
    # def song_list(self):
    #     return self.__song_list

if __name__ == '__main__':
    print(Song._encrypted_id('2097868185814800'))