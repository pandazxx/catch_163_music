__author__ = 'pandazxx'

import datatypes


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