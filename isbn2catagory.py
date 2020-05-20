#-*- coding: utf-8 -*-
import json
import requests
from lxml import etree

url = "http://opac.calis.edu.cn/opac/doSimpleQuery.do"

def queryCatagory(isbn):
    data = {
        "actionType": "doSimpleQuery",
        "pageno": 1,
        "pagingType": 0,
        "operation": "searchRetrieve",
        "version": 1.1,
        "query": '(bath.isbn="{0}*")'.format(isbn),
        "sortkey": "title",
        "maximumRecords": 50,
        "startRecord": 1,
        "dbselect": "all",
        "langBase": "default",
        "conInvalid": "检索条件不能为空",
        "indexkey": "bath.isbn|frt",
        "condition": isbn,
    }
    #print "request:", data
    
    resp = requests.post(url, data)
    if resp.status_code != 200: return "not found"
    #print resp.text
    page = etree.HTML(resp.text)
    info = page.xpath('//*[@id="browser"]/li/span/a/u')
    #print info
    if info:
        return info[0].text
    return "not found"

def handelDoubanBooks(path):
    dest = path + ".withcatagory"
    with open(path) as f, open(dest, "w") as f1:
        for item in f:
            try:
                book = json.loads(item)
                if "morePub" in book:
                    # get isdn
                    isbn = book["morePub"][-2].strip()
                    if isbn:
                        catagory = queryCatagory(isbn)
                        book["catagory"] = catagory
                f1.write(json.dumps(book))
                f1.write("\n")
            except Exception as e:
                print "handle ", item, " error: ", e
            


if __name__ == '__main__':
    print queryCatagory('9787508638119')
