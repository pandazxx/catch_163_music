__author__ = 'pandazxx'

import api_data_example
import music163
import dataobjs

if __name__ == '__main__':
    song = dataobjs.Song(**api_data_example.song_data)
    print(music163._get_download_path(song, "./", "{song.album.artist_description}/{song.album.name}/{song.name}"))
