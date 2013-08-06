from urllib import urlencode
import cookielib
import urllib2
import hashlib


def __getmd5(src):
    return hashlib.new('md5', src).hexdigest()
    pass

def login(username, password):
    cj = cookielib.LWPCookieJar() 
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj)) 
    urllib2.install_opener(opener) 
    user_data = {'username': username, 
                'password': __getmd5(password), 
                'rememberLogin':'true'
                }
    url_data = urlencode(user_data) 

    login_r = opener.open('http://music.163.com/api/login/', url_data)
    return login_r.read()


def main():
    print login('xx', 'xxx')
    pass

if __name__ == '__main__':
    main()