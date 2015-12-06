把指定网站/博客下前一天的所有文章变成一本带目录的书(.mobi)，然后推送到kindle

# 思路
1. 抓取指定网站/博客下前一天的所有文章：使用Calibre
2. 生成YYYYMMDD_blogs.mobi文件：使用Calibre
3. 使用邮箱推送到kindle：使用Calibre
4. 设置定时任务，每天凌晨xx的时候执行：使用cronb

# 参考
1. [用calibre抓取RSS新闻制作电子书及推送到kindle](http://pangyi.github.io/blog/20141208/yong-calibrezhua-qu-rssxin-wen-zhi-zuo-dian-zi-shu-ji-tui-song-dao-kindle/)
2. [抓取网页内容生成Kindle电子书](http://blog.codinglabs.org/articles/convert-html-to-kindle-book.html)

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

附：
1. 博客园新闻： http://feed.cnblogs.com/news/rss(当前无法使用)
2. FreeBuf：http://www.freebuf.com/feed
3. Woo Yun知识库：http://drops.wooyun.org/feed
4. HACKDAY ：https://hackaday.com/blog/feed/
5. InfoQ ：http://www.infoq.com/cn/feed
6. 极客公园：http://www.geekpark.net/rss
7. 译言网：http://feed.yeeyan.org/latest