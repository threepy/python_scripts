from urllib2 import HTTPPasswordMgrWithDefaultRealm
from urllib2 import HTTPBasicAuthHandler
import urllib2

pass_mgr = HTTPPasswordMgrWithDefaultRealm()
uri = 'http://www.baidu.com'
username = 'lxg'
password = 'lxg'
pass_mgr.add_password(None, uri, username, password)
#print pass_mgr.find_user_password(None, uri)

handler = HTTPBasicAuthHandler(pass_mgr)

opener = urllib2.build_opener(handler)
f = opener.open('http://www.baidu.com')
print f.read()



