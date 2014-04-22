import hashlib
import requests


def __getmd5(src):
    return hashlib.new('md5', src).hexdigest()
    pass


def login(username, password):
    user_data = {'username': username,
                 'password': __getmd5(password),
                 'rememberLogin': 'true'}
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
      "Accept": "*/*",
      "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1)"
                    " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36",
      "Accept-Language": "zh-cn",
      "Accept-Encoding": "gzip;deflate",
      "Connection": "keep-alive",
      "Referer": "http://music.163.com/"
    }

    post_data = {
      'username': username,
      'password': __getmd5(password),
      'rememberLogin': 'true'
    }

    # data = 'username=pandazxx%40163.com&password=a165968b0a8084a041aed89bf40d581f&rememberLogin=true'

    resp = requests.post('http://music.163.com/api/login', data=post_data, headers=headers)

    return resp
    # print(resp)
    # print resp.text
    # print resp.cookies
    #
    # playlist = requests.get('http://music.163.com/api/user/playlist/', headers=headers, cookies=resp.cookies)
    #
    # print playlist
    # print playlist.text


def main():
    # print login('xx', 'xxx')
    pass

if __name__ == '__main__':
    main()