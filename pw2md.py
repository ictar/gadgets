#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8') 
import re
import requests
from lxml import etree
from html2text import html2text

# 获取第一个issue
def get_first_issue(url):
    resp = requests.get(url)
    page = etree.HTML(resp.text)
    issue_list = page.xpath("//ul[@id='archive-list']/div[@class='display_archive']/li/a")
    fst_issue = issue_list[0].attrib
    fst_issue["text"] = issue_list[0].text
    return fst_issue


# 获取issue的内容，并专程markdown
def get_issue_md(url):
    resp = requests.get(url)
    page = etree.HTML(resp.text)
    content = page.xpath("//td[@class='defaultText']")[0]#'//table[@class="bodyTable"]')[0]
    return html2text(etree.tostring(content))

subtitle_mapping = {
    '**From Our Sponsor**': '# 来自赞助商',
    '**News**': '# 新闻',
    '**Articles**,** Tutorials and Talks**': '# 文章，教程和讲座',
    '**Books**': '# 书籍',
    '**Interesting Projects, Tools and Libraries**': '# 好玩的项目，工具和库',
    '**Python Jobs of the Week**': '# 本周的Python工作',
    '**New Releases**': '# 最新发布',
    '**Upcoming Events and Webinars**': '# 近期活动和网络研讨会',
}
def clean_issue(content):
    # 去除‘Share Python Weekly’及后面部分
    content = re.sub('\*\*Share Python Weekly.*', '', content, flags=re.IGNORECASE)
    # 预处理标题
    for k, v in subtitle_mapping.items():
        content = content.replace(k, v)
    return content

tpl_str = """原文：[{title}]({url})
---

{content}
"""
def run():
	issue_list_url = "http://us2.campaign-archive2.com/home/?u=e2e180baf855ac797ef407fc7&id=9e26887fc5"
	print "开始获取最新的issue……"
	fst = get_first_issue(issue_list_url)
	print "获取完毕。开始截取最新的issue内容并将其转换成markdown格式"
	content = get_issue_md(fst['href'])
	print "开始清理issue内容"
	content = clean_issue(content)

	print "清理完毕，准备写入文件"
	title = fst['title'].replace('- ', '')
	with open(title+'.md', "wb") as f:
	    f.write(tpl_str.format(title=fst['title'], url=fst['href'], content=content))
	print "恭喜，完成啦。文件保存至%s.md" % title

if __name__ == '__main__':
	run()