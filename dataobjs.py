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


class Artist(datatypes.DictData):
    id = -1
    name = ""


class ArtistDescriptable(object):
    def __artist_description(self):
        if not hasattr(self, "artist") or not self.artists or len(self.artists) == 0:
            return "Unknown"
        elif len(self.artists) == 1:
            return self.artists[0].name
        else:
            return "Various Artist"

    artist_description = property(fget=__artist_description)



class AlbumInfo(datatypes.DictData, ArtistDescriptable):
    name = ""
    id = -1
    artists = datatypes.ArrayObject(Artist)


class Song(datatypes.DictData, ArtistDescriptable):
    id = -1
    bMusic = MusicInfo()
    name = ""
    artists = datatypes.ArrayObject(Artist)
    album = AlbumInfo()

    def download_url(self):
        base_url = 'http://m2.music.126.net'
        en_id = self._encrypted_id(str(self.bMusic.dfsId))
        return '%s/%s/%s.%s' % (base_url, en_id, self.bMusic.dfsId, self.bMusic.extension)


    @staticmethod
    def _encrypted_id(song_dfs_id):
        byte1 = bytearray(b'3go8&$8*3*3h0k(2)2')
        byte2 = bytearray(song_dfs_id.encode('utf-8'))
        byte1_len = len(byte1)
        for i in range(len(byte2)):
            byte2[i] = byte2[i] ^ byte1[i % byte1_len]
        result = base64.b64encode(util.get_md5(byte2)).decode('ascii')
        result = result.replace('/', '_')
        result = result.replace('+', '-')
        return result


class AlbumDetail(datatypes.DictData, ArtistDescriptable):
    name = ""
    id = -1
    songs = datatypes.ArrayObject(Song)


class ArtistSearchInfo(datatypes.DictData):
    name = ""
    id = -1


class AlbumSearchInfo(datatypes.DictData):
    name = ""
    id = -1


class SongSearchInfo(datatypes.DictData):
    name = ""
    id = -1
    artists = datatypes.ArrayObject(ArtistSearchInfo)
    album = AlbumSearchInfo()
