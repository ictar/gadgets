#-*- coding: utf-8 -*-
import time
import json
import requests
from lxml import etree
import traceback

class Book(object):
	def __init__(self, raw, name, img="", holdings=None):
		self.raw = raw
		self.name = name
		self.img_link = img
		self.holdings = holdings
	
	@staticmethod
	def _parse_bookinfo(bookinfo):
		try:
			name = bookinfo.find("h3[@class='title']").text
			img_link = bookinfo.find("div[@class='infocon']/div[@class='infoleft']/img").get("src")
		except Exception as e:
			print traceback.format_exc()
		return name, img_link
	
	@staticmethod
	def _parse_holdings(infolist):
		holdings = {}
		shows = infolist.findall("div[@class='infoslide']/div[@class='infoshow']")
		for show in shows:
			titles = show.findall("div[@class='tab_4_title']/a")
			texts = show.findall("div[@class='tab_4_show']/div[@class='tab_4_text']")
			for i, title in enumerate(titles):
				holdings[title.get("title")] = [HoldingItem.build(tr) for tr in texts[i].findall("table/tbody/tr")]
				
		return holdings
	
	@classmethod
	def build(cls, booksinfo, infolist):
		try:
			raw = {"booksinfo":booksinfo, "infolist":infolist} 
			name, img_link = cls._parse_bookinfo(booksinfo[0])
			holdings = cls._parse_holdings(infolist[0])
			return cls(raw, name, img_link, holdings)
		except Exception as e:
			print traceback.format_exc()
			
		

class HoldingItem(object):
	def __init__(self, **info):
		self.barcode = info.get("bar", "") # 条码号
		self.isdn = info.get("isdn", "") # 索书号
		self.location = info.get("locate", "") # 所在地点
		self.status = info.get("status", "")# 馆藏状态
		self.volume = info.get("volume", "")# 卷期
		self.type = info.get("type", "")# 流通类别
		self.shelf = info.get("shelf", "")# 架位
	
	@classmethod
	def build(cls, raw):
		info = {}
		items = raw.findall("td")
		try:
			info["bar"] = items[0].text.encode("utf-8") if items[0].text else items[0].text
			info["isdn"] = items[1].text.encode("utf-8") if items[1].text else items[1].text
			info["locate"] = items[2].text.encode("utf-8") if items[2].text else items[2].text
			info["status"] = items[3].text.encode("utf-8") if items[3].text else items[3].text
			info["volume"] = items[4].text.encode("utf-8") if items[4].text else items[4].text
			info["type"] = items[5].text.encode("utf-8") if items[5].text else items[5].text
			info["shelf"] = items[5].text.encode("utf-8") if items[5].text else items[5].text
		except Exception as e:
			print traceback.format_exc()
			print etree.tostring(raw)
		
		return HoldingItem(**info)
	
	def __repr__(self):
		return "BAR: {} ISDN: {} LOCATE: {} STATUS: {}".format(self.barcode, self.isdn, self.location, self.status)

def get_info(url):
	"""根据url获取图书信息和馆藏信息
	"""
	info = {"booksinfo":"", "infolist":""}
	try:
		resp = requests.get(url)
		if resp.status_code != 200:
			return info
	except Exception as e:
		print e
		return info
	
	content = etree.HTML(resp.content)
	info["booksinfo"] = content.xpath("//div[@class='booksinfo']")
	info["infolist"] = content.xpath("//div[@class='infolist']")
	return info

def getbooks(urls):
	"""根据图书url构建图书信息。
	这里的urls可以进入我的收藏夹，然后用
	Array.from($(".pagemain>table>tbody>tr>td:nth-child(3)>a")).forEach( element => console.log($(element).attr('href')));
	进行获取
	"""
	books = []
	for url in urls:
		try:
			info = get_info(url)
			book = Book.build(**info)
			books.append(book)
		except Exception as e:
			print url, traceback.format_exc()

		time.sleep(1)
	return books

from collections import defaultdict
def groupby_library(books):
	"""根据图书馆分组
	"""
	libs = defaultdict(list)
	print "total: ", len(books)
	for book in books:
		for k, h in book.holdings.items():
			locat = k.split(" ")[0]
			libs[locat].append((book.name, h[0]))

	# show
	sorted(libs)
	for loc, bks in libs.items():
		print loc, "->"
		for bk in bks:
			print "\t", bk[0], "\t", bk[1]
		print "=" * 80


if __name__ == '__main__':
	pass
