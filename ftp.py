# -*- coding: utf-8 -*-
import ftplib

host = '192.168.100.145'
username = 'dev'
password = 'dev'
remotefile = '镜头1.MOV'
localfile = 'download.MOV'


try:
	# get ftp object and login
	ftp = ftplib.FTP(host)
	ftp.login(username, password)
	print ftp.getwelcome()
except ftplib.all_errors as e:
	print u'ftp 连接失败', e

# download file as ascii mode
def downloadfile_ascii(localfile, remotefile):
	# open local file
	f = open(localfile, 'wb')
	# open remote file and write to local file
	ftp.retrlines('RETR ' + remotefile, f.write)
	f.close()
	print u'下载完成'

# download file as binary mode
def downloadfile_bin(localfile, remotefile):
	f = open(localfile, 'wb')
	ftp.retrbinary('RETR ' + remotefile, f.write)
	f.close()
	print u'download ok'

# upload file as binary mode
def uploadfile_bin(localile):
	f = open(localfile, 'rb')
	ftp.storbinary('STOR ' + localfile, f)
	f.close()
	print 'upload ok'

if __name__ == "__main__":
	 downloadfile_bin(localfile, remotefile)
	 ftp.quit()

