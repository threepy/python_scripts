# -*- coding: utf-8 -*-
import urllib2
import urllib
import cookielib

hosturl = "https://github.com/login"
posturl = 'https://github.com/session'

#获取cookie,并在发送请求时自动发送cookie
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.open(hosturl)
urllib2.install_opener(opener)

#定义headers
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
headers = { 'User-Agent': user_agent,
        'Referer': 'https://github.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Cookie': cj,
        }

#post数据
values = {'login': 'threepy',
        'passowrd': 'mm02205164'}
data = urllib.urlencode(values)

#Request对象
def login():
    req = urllib2.Request(posturl, data, headers)

    try:
        respon = opener.open(req)
        print respon.read()
        respon.close()
    except urllib2.HTTPError,e:
        print 'get http eror:', e.code, e.reason
    except urllib2.URLError, e:
        print 'get URLError:', e.reason
        raise

if __name__ == "__main__":
    login()

