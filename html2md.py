#-*- coding: utf-8 -*-
import html2text
import requests
import os
import sys
from lxml import etree

tpl_str = u"""原文：[{title}]({url})

---

{content}
"""

def get_md(url):
    resp = requests.get(url)
    page = etree.HTML(resp.text)
    h = html2text.HTML2Text()
    h.body_width=0 # 不自动换行
    return h.handle(etree.tostring(page))

def main(url, savepath, title):
    content = tpl_str.format(title=title, content=get_md(url), url=url)
    #print content
    with open(os.path.join(savepath, title)+".md", "w") as f:
        f.write(content.encode("utf8"))
    
def usage():
    print """
    Usage: python html2md.py <url> <title> <save>
    """

if __name__ == '__main__':
    if len(sys.argv) < 4:
        usage()
        exit()
    
    url, title, savepath = sys.argv[1], sys.argv[2], sys.argv[3]
    main(url, savepath, title)