#!/usr/bin/python
#-*- coding:utf-8 -*-

# calibre recipes
receipes = [
	"./recipes/ItComm.recipe", 
	"./recipes/ItSecurity.recipe", 
	"./recipes/Others.recipe"
]


# push mail configuration
# Source Mail config
SrcSMTPServerDomain = "smtp.163.com"
SrcSMTPServerPort = 25
SrcUsername = "xxxx@163.com"
SrcPwd = "1234567"
# Encryption method to use when connecting to relay. Choices are TLS, SSL and NONE. Default  is  TLS.
encryption_method = "NONE"
# Destination Mail Config
DstUsername = ["xxxxx@kindle.cn"]


# Mail Infomation
subject = "convert"
mailcontent = ""