#-*- coding: utf-8 -*-
# this script is used to crawl the newest books in book.dangdang.com, render those which is not in the records to content.html and send the result to specific email address.
# besides, the books' information, inculding url and date, will be stored using "shelve" and those outdated books in db file will be deleted later.
import settings
from datetime import date, datetime, timedelta
class BookItem(object):
	def __init__(self,*args, **kwargs):
		self.title = kwargs.get("title", "")
		self.url = kwargs.get("url", "")
		self.id = kwargs.get("id", "")
		self.author = kwargs.get("author", "")
		self.pubdate = kwargs.get("pubdate", "")
		if not self.pubdate: self.pubdate = str(date.today())
		self.pubdate = str(datetime.strptime(self.pubdate, "%Y-%m-%d").date())
		self.publisher = kwargs.get("publisher", "")
		self.detail = kwargs.get("detail", "")
		self.price = kwargs.get("price","")
		self.subtitle = kwargs.get("subtitle", "")
		self.coverurl = kwargs.get("coverurl", "")

class NextPage(object):
	def __init__(self, current, next):
		self.current = current
		self.next = next
		
import requests
def crawl(urls, preprocess=None):
	'''
	{urls} could be a list or a string
	crawl the urls and {preprocess} the response body
	'''
	#if preprocess is None: preprocess = lambda text
	if isinstance(urls,list):
		for url in urls:
			yield requests.get(url)		
	elif isinstance(urls, str):
		yield requests.get(urls)
	else:
		raise TypeError("urls passed to crawl() should be a list or a string!")

def filterBook(dbname=None):
	'''
	filter those which is in the records
	'''
	def decorator(func):
		def wrapper(*args, **kwargs):
			db = loadInfo(dbname)
			def ninRecord(item):
				if isinstance(item, BookItem): 
					return item.url not in db.get(item.pubdate,[])
				if isinstance(item, NextPage): return True
				raise TypeError("item should be the instance of BookItem")
			items = func(*args, **kwargs)
			return filter(ninRecord,items)
		return wrapper
	return decorator

import re
from lxml import etree
from urlparse import urljoin
@filterBook(dbname=None)
def parse(response):
	'''
	parse {raw_html} and return {BookItem} and nextPageUrl if any
	'''
	html = etree.HTML(response.text)
	lines = html.xpath("//div[@class='tushu']")
	get_index = lambda iter,index=0,default="":(iter[index:index+1] or [default])[0]
	outdated = lambda pubdate: settings.common.get("oldest_day") < (date.today()- datetime.strptime(pubdate, "%Y-%m-%d").date()).days
	for line in lines:
		pubinfo = get_index(line.xpath("div[@class='tushu_right']/div[@class='intro']/div[1]/text()"),1).strip()
		pubdate = get_index(re.findall(r"\d+-\d+-\d+", pubinfo))
		if pubdate and outdated(pubdate): continue
		title = get_index(line.xpath("div[@class='tushu_right']/div[@class='name']/a/text()")).strip()
		url = get_index(line.xpath("div[@class='tushu_right']/div[@class='name']/a/@href")).split("#")[0].strip()
		id = get_index(re.findall("/(\d+).htm", url)).strip()
		author = get_index(line.xpath("div[@class='tushu_right']/div[@class='intro']/div[1]/text()")).strip()
		publisher = get_index(pubinfo.split()).strip()
		detail = "".join(line.xpath("div[@class='tushu_right']/div[@class='intro']/div[@class='p2']/text()")+line.xpath("div[@class='tushu_right']/div[@class='intro']/div[@class='p2']/child::node()/text()")).strip()
		price = get_index(line.xpath("div[@class='tushu_right']/div[@class='goumai']/span"))
		coverurl = get_index(line.xpath("div[@class='cover']/a/img/@src"),0,"#")
		yield BookItem(**locals())
	nextPage = get_index(html.xpath("//img[@id='next']/ancestor::a/@href"))
	if nextPage:
		yield NextPage(response.url, urljoin(response.url, nextPage))


from jinja2 import Environment, FileSystemLoader
def show(items, title, template_name="content.html", **kwargs):
	'''
	render the {items} to {template_name} and generate the result page
	'''
	if kwargs.get('template_path') is None: template_path = settings.common.get("template_path")
	env = Environment(
		loader = FileSystemLoader(template_path)
	)
	template = env.get_template(template_name)	
	return template.render({"title":title,"books":items})

import smtplib
from email.mime.text import MIMEText
def sendEmail(filename, mail_host, mail_user, mail_pass, mailto_list):
	'''
	send email to {receiverAddr}
	'''
	user = "ele"+"<"+mail_user+">"
	with open(filename) as f:
		msg = MIMEText(f.read(), _subtype='html', _charset='utf-8')
	msg['Subject'] = filename[:-4]
	msg['From'] = user
	msg['To'] = ";".join(mailto_list)
	try:
		s = smtplib.SMTP()
		s.connect(mail_host)
		s.login(mail_user, mail_pass)
		s.sendmail(user, mailto_list, msg.as_string())
		s.close()
		return 0
	except Exception, e:
		print str(e)
		return -1

import shelve
def loadInfo(dbname=None):
	'''
	'''
	if dbname is None: dbname = settings.common.get("db_name")
	db = shelve.open(dbname, "c", writeback=True)
	return db
	
def saveInfo(items, dbname=None):
	'''
	save the {items} to {dbname}
	'''
	db = loadInfo(dbname)
	for item in items:
		if isinstance(item, BookItem):
			db.setdefault(item.pubdate, set())
			db[item.pubdate].add(item.url)
		else:
			raise TypeError("item saved into db should be a instance of class BookItem.")
	else:
		db.sync()

def delInfo(datestr, dbname=None):
	'''
	delete the record whose key is {datestr}
	'''
	db = loadInfo(dbname)
	if db.get(datestr, None) is not None: db.pop(datestr)
	db.sync()

def main():
	url = [item[1] for item in settings.menus]
	uniquebooks = set() # filter the duplicate
	items = []
	while True:
		print "begin to crawl...."
		responses = crawl(url)
		print "end crawl. now begin to parse...."
		url = []
		for response in responses:
			parseresult = parse(response)
			for item in parseresult:
				if isinstance(item, BookItem) and item.url not in uniquebooks:
					items.append(item)
					uniquebooks.add(item.url)
				if isinstance(item, NextPage):
					url.append(item.next)
		if url == []: break
	print "parse finished, now let's show"
	if len(items):
		contentTitle = u"{} {}".format(str(date.today()),u"当当新书速递")
		html = show(items, contentTitle)
		with open(contentTitle+".html", "w") as f:
			f.write(html.encode("utf-8"))
		saveInfo(items)
		return contentTitle+".html"
	else: print "no item to show~~"

if __name__ == '__main__':
	contentName = main()
	if contentName:
		rc = sendEmail(
				filename=contentName, 
				#mail_subject=settings.mail_subject, 
				mail_host=settings.mail_host, 
				mail_user=settings.mail_user, 
				mail_pass=settings.mail_pass, 
				mailto_list=settings.mailto_list
			)
		if rc == 0:
			print "push mail successfully~ now begin to delete the old records..."
			deldate = date.today()+timedelta(-3-settings.common.get("oldest_day",1))
			delInfo(str(deldate))
			# delete page
			import os
			os.remove(contentName)
	