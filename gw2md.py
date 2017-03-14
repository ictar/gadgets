#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8') 
import re
import requests
from lxml import etree
from html2text import html2text

# 获取最新的issue
get_latest_issue = lambda url: requests.get(url)

sec_tpl = """
## {name}

{content}

"""
item_tpl = """
[{name}]({url})   {tag}

{content}

_{source}_
"""
tag_mapping = {
	"story": "",
	"tutorial": "教程",
	"code": "代码",
	"video": "视频",
	"opinion": "观点",
	"tools": "工具",
}
# 处理单个item
def do_with_item(item):
    try:
        link = item.xpath(".//td[@class='link']")[0]
        name = link.xpath(".//a/text()")[0]
        url = link.xpath(".//a/@href")[0]
        tag = link.xpath(".//span")
        if tag:
            tag = "**[{}]**".format(tag[0].xpath("text()")[0].strip())
        else:
            tag = ""
        try:
            content = html2text(etree.tostring(item.xpath(".//td[@class='body']/div")[0])).strip()
        except Exception, e:
            content = ""
        
        try:
            source = item.xpath(".//td[@class='source']/div/text()")[0].strip()
        except Exception, e:
            source = ""
        
        return item_tpl.format(name=name, url=url, tag=tag, content=content, source=source)
    except Exception, e:
        print e
    return ""

# 处理section
def do_with_section(name, contents):
    items = contents.getchildren()
    return sec_tpl.format(name=name, content="\n".join(do_with_item(item) for item in items))

# 获取issue的内容和标题，并转成markdown
def get_issue_md(content):
    page = etree.HTML(content)
    title = page.xpath("//title/text()")[0]
    content = page.xpath("//table[@class='container blocklogo go']/tr/td")[0]

    section_list = content.getchildren()
    return title, "\n".join(
        (
            do_with_section(
                section.xpath(".//td[@class='name']/span/text()")[0],
                section.xpath(".//td[@class='contents']")[0]
            ) for section in section_list
        )
    )

subtitle_mapping = {
    '# Featured': '# 特选',
    '# Jobs': '# 工作',
    '# In Brief': '# 简言之',
}
def clean_issue(content):
    content = content.replace('|', '').replace('---', '').replace("  \n  \n", "\n")
    # 预处理标题
    for k, v in subtitle_mapping.items():
        content = content.replace(k, v)
    return content

tpl_str = """原文：[{title}]({url})
---

{content}
"""
def run():
    base_url = "http://golangweekly.com"
    issue_list_url = "{base}/issues".format(base=base_url)
    latest_issue_url = "{base}/latest".format(base=base_url)
    print "开始获取最新的issue……"
    resp = get_latest_issue(latest_issue_url)
    print "获取完毕。开始截取最新的issue内容并将其转换成markdown格式"
    title, content = get_issue_md(resp.content)
    title = title[:title.find(":")]
    print "开始清理issue内容"
    content = clean_issue(content)

    print "清理完毕，准备写入文件"
    with open(title+'.md', "wb") as f:
        f.write(tpl_str.format(title=title, url=resp.url, content=content))
    print "恭喜，完成啦。文件保存至%s.md" % title

if __name__ == '__main__':
    run()