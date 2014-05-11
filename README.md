# music163

A python script set to download high quality music from [Netease Music](music.163.com). Including login and personal collection download.

## Usage

```
  music163.py download collection --username=<username> --password=<password>
  music163.py download album <album_id>...
  music163.py download song <song_id>...
  music163.py download artist <artist_id>...
  music163.py search artist <artist_keyword>
  music163.py search album <album_keyword>
  music163.py search song <song_keyword>
```

## TODO

1. Support more download tools
2. Update ID3 tags according to the music infomation provided by the Netease Music API
3. Save username & password
4. Configureable output dir pattern
