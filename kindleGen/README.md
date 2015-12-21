把指定网站/博客下前一天的所有文章变成一本带目录的书(.mobi)，然后推送到kindle

# 思路
1. 抓取指定网站/博客下前一天的所有文章：使用Calibre
2. 生成{name}_{timestamp}.mobi文件：使用Calibre
3. 使用邮箱推送到kindle：使用Calibre
4. 设置定时任务，每天凌晨xx的时候执行：使用cronb

# 参考
1. [用calibre抓取RSS新闻制作电子书及推送到kindle](http://pangyi.github.io/blog/20141208/yong-calibrezhua-qu-rssxin-wen-zhi-zuo-dian-zi-shu-ji-tui-song-dao-kindle/)
2. [抓取网页内容生成Kindle电子书](http://blog.codinglabs.org/articles/convert-html-to-kindle-book.html)
3. [Customizing the fetch process using Calibre](http://manual.calibre-ebook.com/news.html#customizing-the-fetch-process)
4. [API Documentation for recipes](http://manual.calibre-ebook.com/news_recipe.html)

# 使用的第三方工具
1. Calibre: `apt-get install calibre`

# 使用方法
1. 修改settings.py文件
2. 设置定时任务：
```
#!/bin/sh
#file: blogPush.sh
cd /home/ele/git/Gadgets/kindleGen
python kindleBlogUpdate.py
```
然后
`30 0 * * * /root/timeSchedule/blogPush.sh`

# 碎碎念
2015.12.10 只从被calibre折腾了一段时间，现在处于看到线上啥好文档都想爬下来推送到kindle的阶段，Orz...

# 附：
## ItComm.recipe
1. 博客园新闻： http://feed.cnblogs.com/news/rss(当前无法使用)
2. HACKDAY ：https://hackaday.com/blog/feed/
3. 极客公园：http://www.geekpark.net/rss
4. 爱范儿：http://www.ifanr.com/feed

## ItSecurity.recipe
1. FreeBuf：http://www.freebuf.com/feed
2. Woo Yun知识库：http://drops.wooyun.org/feed

## Others.recipe
1. 译言网：http://feed.yeeyan.org/latest
2. 知乎每日精选（强烈推荐）：http://www.zhihu.com/rss
3. 战隼的学习探索（效率生活）: http://www.read.org.cn/feed
4. GFW与XX：http://www.chinagfw.org/feeds/posts/default?alt=rss

## PythonTutorial.recipe
Python官方教程生成的电子书

## Twisted-intro-cn.recipe
(Twisted与异步编程入门)[https://likebeta.gitbooks.io/twisted-intro-cn/content/index.html]