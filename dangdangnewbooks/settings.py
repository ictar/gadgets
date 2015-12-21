#-*- coding: utf-8 -*-
common = {
	'template_path':'./',
	'db_name':'books.db',
	'oldest_day': 1,
}

# push mail configuration
# Source Mail config
mail_host = u"smtp.163.com"
mail_user = u"xxxx@163.com"
mail_pass = u"1234567"
# Encryption method to use when connecting to relay. Choices are TLS, SSL and NONE. Default  is  TLS.
# Destination Mail Config
mailto_list = ["xxxxx@qq.com"]


# Mail Infomation
mail_subject = u"Dangdang books daily update"
mail_content = u"Dangdang books daily update"

menus = [
	(r"管理", r"http://book.dangdang.com/list/newRelease_C01.22.htm"),
	(r"成功励志", r"http://book.dangdang.com/list/newRelease_C01.21.htm"),
	(r"历史", r"http://book.dangdang.com/list/newRelease_C01.36.htm"),
	(r"哲学/宗教", r"http://book.dangdang.com/list/newRelease_C01.28.htm"),
	(r"保健养生", r"http://book.dangdang.com/list/newRelease_C01.18.htm"),
	(r"传记", r"http://book.dangdang.com/list/newRelease_C01.38.htm"),
]