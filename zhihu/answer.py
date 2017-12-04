#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8') 
import requests
import json
import html2text
import time
import random
import config

from urllib import urlencode

ans_tpl_str = """[原答案]({url}) by [{author_name}]({author_url})   ({voteup_count}人赞同了该答案)


{content}
---

"""
que_tpl_str = """问题：[{title}]({url})
---

"""
class AnawerItem(object):
	def __init__(self, **kws):
		self._metas = kws
		self._h = html2text.HTML2Text()
		self._h.body_width = 0

	@property
	def question(self):
		return self._metas.get("question", {})

	@property
	def question_url(self):
		return "https://www.zhihu.com/question/{}".format(self.question.get("id", 0))
	
	@property
	def question_title(self):
		return self.question.get("title", "unknown").strip()
	
	@property
	def url(self):
		return self._metas.get("url", "#")

	@property
	def author(self):
		return self._metas.get("author", {})

	@property
	def author_name(self):
		return self.author.get("name", "")

	@property
	def author_url(self):
		return "https://www.zhihu.com/people/" + self.author.get("url_token", "#")
	
	@property
	def voteup_count(self):
		return self._metas.get("voteup_count", "*")
	
	@property
	def content(self):
		return self._metas.get("content", "")
	
	def to_markdown(self):
		return ans_tpl_str.format(url=self.url, author_name=self.author_name,
				author_url=self.author_url, voteup_count=self.voteup_count, content=self._h.handle(self.content))
	def question_to_markdown(self):
		return que_tpl_str.format(title=self.question_title, url=self.question_url)


class AnswerList(object):
	def __init__(self, questionId):
		self.qid = questionId
		self.payload = {"sort_by": "default", "include": config.AnsInclude, "limit":50, "offset": 0}
		self.baseUrl = config.QueAnsUrl.format(self.qid)

	@property
	def next_url(self):
		try:
			if self._content:
				if self._content.get("paging", {}).get("next", ""):
					tmp = self._content["paging"]["next"]
					if tmp.startswith("http:"):
						tmp = tmp.replace("http:", "https:")
					return tmp
		except Exception, e:
			print "get next url exception:", e
		
		return "{}?{}".format(self.baseUrl, urlencode(self.payload))
	
	@property
	def is_end(self):
		try:
			if self._content:
				if self._content.get("paging", {}).get("is_end", ""):
					return self._content["paging"]["is_end"]
		except Exception, e:
			print "get is_end exception:", e
		
		return False
	
	def _make_request(self, url, data, method="GET"):
		try:
			func = getattr(requests, method.lower(), requests.get)
			#print "make a request to", url, " data is ", data
			resp = func(url, data=data, headers=config.AnsHeaders) if data else func(url, headers=config.AnsHeaders)
			#print resp.status_code
			if resp.status_code != 200:
				print "request", url, "error, response:", resp.content
			self._content = resp.json()
		except Exception as e:
			print method, url, "exception: ", e
			self._content = {}
		

	def get_next_answer(self):
		#import pdb;pdb.set_trace()
		while not self.is_end:
			self._make_request(self.next_url, None)
			data = self._content.get("data", [])
			for item in data:
				yield AnawerItem(**item)
			time.sleep(random.randint(1, 10))

def main():
	for q in config.QuestionIds:
		ans = AnswerList(q).get_next_answer()
		index = 1
		print "Begin to fetch answers for quesiton No.", q
		for item in ans:
			print "Answer No.", index, " for Question No.", q
			with open(u"{}.md".format(item.question_title), "a+") as f:
				if index == 1:
					f.write(item.question_to_markdown())
				f.write(item.to_markdown())
				index += 1


if __name__ == '__main__':
	main()
