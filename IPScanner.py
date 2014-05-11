#-*- encode:utf-8 -*-
import os

#scanning survival hosts for the specified segment

#test: print addIP("255.255.255.255",2)
def addIP(ip,inc):
	res = ""
	tmp = ip.split(".")
	sum = int(tmp[3]) + inc
	fourth = sum % 255
	sum = sum / 255 + int(tmp[2])
	third = sum % 255
	sum = sum /255 + int(tmp[1])
	second = sum % 255
	sum = sum / 255 + int(tmp[0])
	first = sum % 255
	if sum > 255:
		res = "-1"
	else:
		res = str(first) + "." + str(second) + "." + str(third) + "." + str(fourth)

	return res

#test: print cmpIP("10.10.10.10","10.1.10.10")
def cmpIP(a,b):
	a = int(a.replace(".",""))
	b = int(b.replace(".",""))
	if a > b:
		return 1
	elif a == b:
		return 0
	else:
		return -1

def validIP(ip):
	ip = ip.split(".")
	if len(ip) != 4:
		return False
	if int(ip[0]) > 256 or int(ip[1]) > 256 or int(ip[2]) > 256 or int(ip[3]) > 256:
		return False
	if int(ip[0]) < 0 or int(ip[1]) < 0 or int(ip[2]) < 0 or int(ip[3]) < 0:
		return False
	return True

#paras: begin, end : scanning the ip between begin and end, the format is xxx.xxx.xxx.xxx, string
def usePing(begin, end):
	survival = []
	if validIP(begin) is not True or validIP(end) is not True:
		return survival
	ip = begin
	#print ip
	while cmpIP(ip,end) != 1:
		#ping
		tmp = os.popen("ping " + ip).readlines()
		if "0" not in tmp[8]:#if os.system("ping " + ip) != 1:
			survival.append(ip)
		ip = addIP(ip,1)
		#print ip
		if "-1" == ip:
			break

	return survival


begin = raw_input("please input the begin IP you want to scan (e.g. 127.0.0.1): ")
end = raw_input("please input the end IP you want to scan (e.g. 127.0.0.5): ")
survival = usePing(begin, end)
for ip in survival:
	print ip