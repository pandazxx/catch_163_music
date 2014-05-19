#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Usage:
  music163.py download collection --username=<username> --password=<password>
  music163.py download album <album_id>...
  music163.py download song <song_id>...
  music163.py download artist <artist_id>...
  music163.py search artist <artist_keyword>
  music163.py search album <album_keyword>
  music163.py search song <song_keyword>
  music163.py collection --list --username=<username> --password=<password>
'''

__author__ = 'pandazxx'
import docopt
import session
import downloadtool


def test_arguments(args):
    out = docopt.docopt(__doc__, args)
    print("=" * 20 + "\n{args}:\n\t{out}".format(**locals()))
    handle_command(out)


def download_songs(download_list=()):
    print("Downloading {cnt} songs:".format(cnt=len(download_list)))
    for song in download_list:
        print(">>> [{song_name}]({song_url})".format(song_name=song.name, song_url=song.download_url()))
    remaining_list = list(download_list)
    downloader = downloadtool.get_download_tool("aria2")
    while len(remaining_list) > 0:
        for song in remaining_list:
            try:
                print("Downloading {name} ({curr}/{total})".format(name=song.name, curr=len(download_list)-len(remaining_list), total=len(download_list)))
                downloader.download(uri=song.download_url(), path=song.bMusic.name+'.'+song.bMusic.extension)
                remaining_list.remove(song)
            except Exception as e:
                print("Download error: {url} will try again later".format(url=song.download_url()))


def handle_download_collection(opt_dict):
    # print(handle_download_collection.__name__)
    username = opt_dict['--username']
    password = opt_dict['--password']
    s = session.Session()
    s.login(username, password)
    download_list = []
    for pl in s.get_collections():
        for song in s.song_details_from_playlist(pl):
            download_list.append(song)
    download_songs(download_list)


def handle_collection(opt_dict):
    username = opt_dict['--username']
    password = opt_dict['--password']
    s = session.Session()
    s.login(username, password)
    song_list = []
    for pl in s.get_collections():
        for song in s.song_details_from_playlist(pl):
            song_list.append(song)
    print("# id|name|artist name|artist id")
    for song in song_list:
        print("|".join((
            str(song.id),
            song.name,
            song.artists[0].name,
            str(song.artists[0].id),
        )))


def handle_download_song(opt_dict):
    raise Exception("Not implemented")


def handle_download_artist(opt_dict):
    artist_id = opt_dict['<artist_id>']
    s = session.Session()
    download_list = []
    for a_id in artist_id:
        albums = s.album_list_from_artist(a_id)
        for album_info in albums:
            album_detail = s.album_detail(album_info.id)
            for song in album_detail.songs:
                download_list.append(song)
    download_songs(download_list)


def handle_download_album(opt_dict):
    album_ids = opt_dict['<album_id>']
    s = session.Session()
    download_list = []
    for a_id in album_ids:
        album_detail = s.album_detail(a_id)
        for song in album_detail.songs:
            download_list.append(song)
    download_songs(download_list)


def handle_search_artist(opt_dict):
    s = session.Session()
    artist_keyword = opt_dict['<artist_keyword>']
    artists = s.search_artist(artist_keyword)
    print("Found {cnt} artist(s):".format(cnt=len(artists)))
    for artist in artists:
        print("{name} (id: {id})".format(name=artist.name, id=artist.id))


def handle_search_song(opt_dict):
    s = session.Session()
    song_keyword = opt_dict['<song_keyword>']
    songs = s.search_song(song_keyword)
    print("Found {cnt} song(s):".format(cnt=len(songs)))
    for song in songs:
        print("{name} (id: {id})".format(name=song.name, id=song.id))


def handle_search_album(opt_dict):
    s = session.Session()
    album_keyword = opt_dict['<album_keyword>']
    albums = s.search_album(album_keyword)
    print('Found {cnt} album(s):'.format(cnt=len(albums)))
    for album in albums:
        print("{name} (id: {id})".format(name=album.name, id=album.id))


def handle_command(opt_dict=None):
    if not opt_dict: opt_dict = {}

    def has_command(*args):
        def fun(opts):
            ret = True
            for command in args:
                if command not in opts or not opts[command]:
                    ret = False
                    break
            return ret
        return fun

    route = (
        (has_command("download", "collection"), handle_download_collection),
        (has_command("download", 'album'), handle_download_album),
        (has_command("download", 'song'), handle_download_song),
        (has_command('download', 'artist'), handle_download_artist),
        (has_command('search', 'artist'), handle_search_artist),
        (has_command('search', 'album'), handle_search_album),
        (has_command('search', 'song'), handle_search_song),
        (has_command('collection'), handle_collection)
    )

    for checker, command in route:
        if checker(opt_dict):
            command(opt_dict)


if __name__ == '__main__':
    opt_dict = docopt.docopt(__doc__, version='0.0.1')
    handle_command(opt_dict)

