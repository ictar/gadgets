#!/usr/bin/python
#-*- coding:utf-8 -*-

import subprocess
from time import time
from settings import *

# generate mobi file
def genMobi(receipe):
	mobiName = "{0}_{1}.mobi".format(receipe.split("/")[-1].split(".")[0],int(time()))
	rc = subprocess.call([
			'ebook-convert', receipe, mobiName,
		])
	return (rc, mobiName)

# push mobi file toKindle
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

def removeMobi(mobiName):
	rc = subprocess.call([
		'rm',mobiName
		])
	return rc
	
if __name__ == "__main__":
	for receipe in receipes:
		print u"generate ", receipe
		rc, mobiname = genMobi(receipe)
		if rc == 0:
			print u"generate %s successfully, now begin to push~" % mobiname
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
			if rc ==0: 
				print u"push successfully~~"
				removeMobi(mobiname)
