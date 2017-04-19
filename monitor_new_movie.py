#-*- coding: utf-8 -*-
"""
监控电影天堂(dytt8.net)等网站上传的新电影
"""
import requests
from lxml import etree

class MovieItem(object):
    def __init__(self, name, datetime, url, description=None):
        self.name = name
        self.dt = datetime
        self.url = url
        self.desc = description
        
    def __repr__(self):
        print "name: {}\ndatetime: {}\nurl: {}\ndescription: {}".format(self.name, self.dt, self.url, self.desc)



dytt_movie_index = "http://www.ygdy8.net/html/gndy/dyzz/index.html"

def get_movie_list(url):
    """获取电影列表"""
    resp = requests.get(url)
    page = etree.HTML(resp.text)
    movie_list = page.xpath("//div[@class='co_content8']/ul/td/table")
    return movie_list

def _parse_movie_item(movie_item):
    """解析单个电影项信息，返回MovieItem实例"""
    name = movie_item.xpath("tr[2]/td[2]/b/a/text()")[0].encode("gbk")
    url = movie_item.xpath("tr[2]/td[2]/b/a/@href")
    dt = "".join(movie_item.xpath("tr[3]/td[2]/font/text()"))
    desc = "".join(movie_item.xpath("tr[4]/td/text()"))
    print name, dt, url, desc
    return MovieItem(name, dt, url, desc)

def main():
    movie_list = get_movie_list(dytt_movie_index)
    _parse_movie_item(movie_list[0])

if __name__ == '__main__':
    main()