#!/usr/bin/python
#-*- coding:utf-8 -*-

import subprocess
from time import time
from settings import *

# 生成电子杂志
def genMobi(receipe):
	mobiName = "{0}_{1}.mobi".format(receipe.split(".")[0],int(time()))
	rc = subprocess.call([
			'ebook-convert', receipe, mobiName,
		])
	return (rc, mobiName)

# 推送到Kindle
def push2Kindle(mobiName, relay, port, username, password, encryptMethod, dstusername, content, subject):
	'''
	calibre-smtp --attachment xxx.mobi --relay smtp.163.com --port 25 --username xxxxx@163.com --password "xxxxxx" --encryption-method TLS xxxxx@163.com xxxxxx@kindle.cn "xxxxxx" -v -s "convert"
	'''
	rc = subprocess.call([
			'calibre-smtp', '--attachment', str(mobiName),
			'--relay', str(relay),
			'--port', str(port),
			'--username', str(username),
			'--password', str(password),
			'--encryption-method', str(encryptMethod),
			str(username), str(dstusername), str(content),
			'-v', '-s', str(subject)
		])
	return rc
	
if __name__ == "__main__":
	print u"生成", receipe
	rc, mobiname = genMobi(receipe)
	if rc == 0:
		print u"成功生成%s，现在开始推送" % mobiname
		rc = push2Kindle(
				mobiName=mobiname,
				relay=SrcSMTPServerDomain, 
				port=SrcSMTPServerPort, 
				username=SrcUsername, 
				password=SrcPwd, 
				encryptMethod=encryption_method, 
				dstusername=" ".join(DstUsername), 
				content=mailcontent, 
				subject=subject
			)
		if rc ==0: print u"推送成功~~"
