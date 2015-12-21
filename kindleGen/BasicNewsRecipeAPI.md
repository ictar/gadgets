BaicNewsRecipe定义的编写recipe的API

class calibre.web.feeds.news.**BasicNewsRecipe**(options, log, progress_reporter)
	基类。包含所有recipe所需的逻辑。通过逐步覆盖这个类中的大部分功能，可以编写更多自定义/强有力的recipe。创建recipe的入门教程，查看[增加你喜欢的新闻网站](http://manual.calibre-ebook.com/news.html)
	
	abort_article(msg=None)
		在任意预处理方法中调用此方法来中止当前文章的下载。对于跳过那些包含例如纯视频文章等的不适当的内容是有用的。

	abort_recipe_processing(msg)
		引发recipe下载系统停止这个recipe的下载。向用户展示一个简单的回馈信息。

	add_toc_thumbnail(article, src)
		Call this from populate_article_metadata with the src attribute of an <img> tag from the article that is appropriate for use as the thumbnail representing the article in the Table of Contents. Whether the thumbnail is actually used is device dependent (currently only used by the Kindles). Note that the referenced image must be one that was successfully downloaded, otherwise it will be ignored.

	classmethod adeify_images(soup)
		If your recipe when converted to EPUB has problems with images when viewed in Adobe Digital Editions, call this method from within postprocess_html().

	canonicalize_internal_url(url, is_link=True)
		Return a set of canonical representations of url. The default implementation uses just the server hostname and path of the URL, ignoring any query parameters, fragments, etc. The canonical representations must be unique across all URLs for this news source. If they are not, then internal links may be resolved incorrectly.

		Parameters:	is_link – Is True if the URL is coming from an internal link in an HTML file. False if the URL is the URL used to download an article.
	
	cleanup()
		在所有的文章下载结束后调用。用它进行一些例如登出订阅网站等的清理工作。

	clone_browser(br)
		Clone the browser br. Cloned browsers are used for multi-threaded downloads, since mechanize is not thread safe. The default cloning routines should capture most browser customization, but if you do something exotic in your recipe, you should override this method in your recipe and clone manually.

		Cloned browser instances use the same, thread-safe CookieJar by default, unless you have customized cookie handling.

	default_cover(cover_file)
		为一个没有封面的recipe创建一个通用封面。

	download()
		Download and pre-process all articles from the feeds in this recipe. This method should be called only once on a particular Recipe instance. Calling it more than once will lead to undefined behavior. :return: Path to index.html

	extract_readable_article(html, url)
		从html中提取主要的文章内容，清理并返回一个元组(article_html, extracted_title)。基于Arc90的原始可读算法。

	get_article_url(article)[source]
		Override in a subclass to customize extraction of the URL that points to the content for each article. Return the article URL. It is called with article, an object representing a parsed article from a feed. See feedparser. By default it looks for the original link (for feeds syndicated via a service like feedburner or pheedo) and if found, returns that or else returns article.link.

	get_browser(*args, **kwargs)
		返回一个用来从web抽取文档的浏览器实例。默认情况下，它返回一个[mechanize](http://wwwsearch.sourceforge.net/mechanize/)浏览器实例，这个实例支持cookies, 忽略robots.txt，处理刷新及拥有一个mozilla firefox用户代理。
		
		如果你的recipe要求你先登录，那么在你的子类中重写这个方法。例如，下面New York Times recipe中的代码用来登录以获取全面接入：
		
		```python
		def get_browser(self):
			br = BasicNewsRecipe.get_browser(self)
			if self.username is not None and self.password is not None:
				br.open('http://www.nytimes.com/auth/login')
				br.select_form(name='login')
				br['USERID']   = self.username
				br['PASSWORD'] = self.password
				br.submit()
			return br
		```
	get_cover_url()[source]
		Return a URL to the cover image for this issue or None. By default it returns the value of the member self.cover_url which is normally None. If you want your recipe to download a cover for the e-book override this method in your subclass, or set the member variable self.cover_url before this method is called.

	get_feeds()[source]
		Return a list of RSS feeds to fetch for this profile. Each element of the list must be a 2-element tuple of the form (title, url). If title is None or an empty string, the title from the feed is used. This method is useful if your recipe needs to do some processing to figure out the list of feeds to download. If so, override in your subclass.

	get_masthead_title()[source]
		Override in subclass to use something other than the recipe title

	get_masthead_url()[source]
		Return a URL to the masthead image for this issue or None. By default it returns the value of the member self.masthead_url which is normally None. If you want your recipe to download a masthead for the e-book override this method in your subclass, or set the member variable self.masthead_url before this method is called. Masthead images are used in Kindle MOBI files.

	get_obfuscated_article(url)[source]
		If you set articles_are_obfuscated this method is called with every article URL. It should return the path to a file on the filesystem that contains the article HTML. That file is processed by the recursive HTML fetching engine, so it can contain links to pages/images on the web.

		This method is typically useful for sites that try to make it difficult to access article content automatically.

	classmethod image_url_processor(baseurl, url)[source]
		Perform some processing on image urls (perhaps removing size restrictions for dynamically generated images, etc.) and return the precessed URL.

	index_to_soup(url_or_raw, raw=False, as_tree=False)[source]
		Convenience method that takes an URL to the index page and returns a BeautifulSoup of it.

		url_or_raw: Either a URL or the downloaded index page as a string

	is_link_wanted(url, tag)[source]
		Return True if the link should be followed or False otherwise. By default, raises NotImplementedError which causes the downloader to ignore it.

		Parameters:	
		url – The URL to be followed
		tag – The Tag from which the URL was derived
	
	javascript_login(browser, username, password)[source]
		This method is used to login to a website that uses javascript for its login form. After the login is complete, the cookies returned from the website are copied to a normal (non-javascript) browser and the download proceeds using those cookies.

		An example implementation:

		def javascript_login(self, browser, username, password):
			browser.visit('http://some-page-that-has-a-login')
			form = browser.select_form(nr=0) # Select the first form on the page
			form['username'] = username
			form['password'] = password
			browser.submit(timeout=120) # Submit the form and wait at most two minutes for loading to complete
		Note that you can also select forms with CSS2 selectors, like this:

		browser.select_form('form#login_form')
		browser.select_from('form[name="someform"]')
	
	parse_feeds()
		根据BasicNewsRecipe.get_feeds()返回的feed列表创建文章列表。返回一个Feed对象列表。

	parse_index()
		recipe应该实现这个方法来解析一个网站，而不是使用feed来产生文章列表。典型的应用是对那些拥有一个"打印版本"的网页来展示所有文章的打印版本的新闻源。若实现此方法，将优先于BasicNewsRecipe.parse_feeds()使用此方法。

		它必须返回一个列表。列表中的每个元素必须包含一个形式为('feed标题'， 文章列表)的二元元组。

		每个文章列表必须包含如下形式的字典。
		
		```python
		{
		'title'       : article title,
		'url'         : URL of print version,
		'date'        : The publication date of the article as a string,
		'description' : A summary of the article
		'content'     : The full article (can be an empty string). Obsolete
						do not use, instead save the content to a temporary
						file and pass a file:///path/to/temp/file.html as
						the URL.
		}
		```
		举个栗子，看看用来下载The Atlantic的recipe。另外，你可以为文章增加"作者"。一个常用的例子是：

		如果出于某些原因，你想要中止处理，并且让calibre向用户展示一个简单的消息，而不是一个错误，调用abort_recipe_processing()。

	populate_article_metadata(article, soup, first)
		当下载每一个属于文章的HTML页面时调用。用来尝试从解析的HTML (soup)中获取文章的元数据，例如作者/总结等。
		
		:param article: calibre.web.feeds.Article类的一个对象。如果你修改了summary，记得也要修改text_summary。
		param soup: 这个文章的解析后的HTML
		:param first: 若解析的HTML是文章的第一个页面，设为True.

	postprocess_book(oeb, opts, log)[source]
		Run any needed post processing on the parsed downloaded e-book.

		Parameters:	
		oeb – An OEBBook object
		opts – Conversion options
	
	postprocess_html(soup, first_fetch)[source]
		This method is called with the source of each downloaded HTML file, after it is parsed for links and images. It can be used to do arbitrarily powerful post-processing on the HTML. It should return soup after processing it.

		Parameters:	
		soup –
		A BeautifulSoup instance containing the downloaded HTML.
		first_fetch – True if this is the first page of an article.
	
	preprocess_html(soup)
		这个方法被每一个下载的HTML文件源代码在解析链接和图片前所调用。它在由例如remove_tags所指定的清理后调用。它可以用来对HTML进行任意强大的预处理。在处理它之后，应该返回一个soup对象。

		soup: 一个BeautifulSoup实例，它包含下载的HTML。

	preprocess_raw_html(raw_html, url)
		This method is called with the source of each downloaded HTML file, before it is parsed into an object tree. raw_html is a unicode string representing the raw HTML downloaded from the web. url is the URL from which the HTML was downloaded.

		Note that this method acts before preprocess_regexps.

		This method must return the processed raw_html as a unicode object.

	classmethod print_version(url)
		接收一个指向文章内容的网页的url，返回一个指向文章打印版本的url。默认不做任何操作。例如：
		```python
		def print_version(self, url):
			return url + '?&pagewanted=print'
		```
	skip_ad_pages(soup)[source]
	This method is called with the source of each downloaded HTML file, before any of the cleanup attributes like remove_tags, keep_only_tags are applied. Note that preprocess_regexps will have already been applied. It is meant to allow the recipe to skip ad pages. If the soup represents an ad page, return the HTML of the real page. Otherwise return None.

	soup: A BeautifulSoup instance containing the downloaded HTML.

	sort_index_by(index, weights)[source]
	Convenience method to sort the titles in index according to weights. index is sorted in place. Returns index.

	index: A list of titles.

	weights: A dictionary that maps weights to titles. If any titles in index are not in weights, they are assumed to have a weight of 0.

	classmethod tag_to_string(tag, use_alt=True, normalize_whitespace=True)[source]
	Convenience method to take a BeautifulSoup Tag and extract the text from it recursively, including any CDATA sections and alt tag attributes. Return a possibly empty unicode string.

	use_alt: If True try to use the alt attribute for tags that don’t have any textual content

	tag: BeautifulSoup Tag

	articles_are_obfuscated = False
		设为True，然后实现get_obfuscated_article()来处理那些难以抓取内容的网站。

	auto_cleanup = False
		Automatically extract all the text from downloaded article pages. Uses the algorithms from the readability project. Setting this to True, means that you do not have to worry about cleaning up the downloaded HTML manually (though manual cleanup will always be superior).

	auto_cleanup_keep = None
		指定自动清理算法不应该移除的元素。语法为一个XPath表达式。例如：

		`auto_cleanup_keep = '//div[@id="article-image"]'` 将保留所有拥有 id="article-image"的div标签
		`auto_cleanup_keep = '//*[@class="important"]'` 将保留所有拥有属性class="important"的元素
		`auto_cleanup_keep = '//div[@id="article-image"]|//span[@class="important"]'`将保留所有拥有属性id="article-image"的div元素及拥有属性class="important"的span元素。
						  
	center_navbar = True
		If True the navigation bar is center aligned, otherwise it is left aligned

	compress_news_images = False
		Set this to False to ignore all scaling and compression parameters and pass images through unmodified. If True and the other compression parameters are left at their default values, jpeg images will be scaled to fit in the screen dimensions set by the output profile and compressed to size at most (w * h)/16 where w x h are the scaled image dimensions.

	compress_news_images_auto_size = 16
		The factor used when auto compressing jpeg images. If set to None, auto compression is disabled. Otherwise, the images will be reduced in size to (w * h)/compress_news_images_auto_size bytes if possible by reducing the quality level, where w x h are the image dimensions in pixels. The minimum jpeg quality will be 5/100 so it is possible this constraint will not be met. This parameter can be overridden by the parameter compress_news_images_max_size which provides a fixed maximum size for images. Note that if you enable scale_news_images_to_device then the image will first be scaled and then its quality lowered until its size is less than (w * h)/factor where w and h are now the scaled image dimensions. In other words, this compression happens after scaling.

	compress_news_images_max_size = None
	Set jpeg quality so images do not exceed the size given (in KBytes). If set, this parameter overrides auto compression via compress_news_images_auto_size. The minimum jpeg quality will be 5/100 so it is possible this constraint will not be met.

	conversion_options = {}
	Recipe specific options to control the conversion of the downloaded content into an e-book. These will override any user or plugin specified values, so only use if absolutely necessary. For example:

	conversion_options = {
	  'base_font_size'   : 16,
	  'tags'             : 'mytag1,mytag2',
	  'title'            : 'My Title',
	  'linearize_tables' : True,
	}
	cover_margins = (0, 0, '#ffffff')
	By default, the cover image returned by get_cover_url() will be used as the cover for the periodical. Overriding this in your recipe instructs calibre to render the downloaded cover into a frame whose width and height are expressed as a percentage of the downloaded cover. cover_margins = (10, 15, ‘#ffffff’) pads the cover with a white margin 10px on the left and right, 15px on the top and bottom. Color names defined at http://www.imagemagick.org/script/color.php Note that for some reason, white does not always work on windows. Use #ffffff instead

	delay = 0
		连续下载之间的延迟，以秒为单位。该参数可以是一个浮点数来表示一个更精确的时间。

	description = u''
		A couple of lines that describe the content this recipe downloads. This will be used primarily in a GUI that presents a list of recipes.

	encoding = None
		Specify an override encoding for sites that have an incorrect charset specification. The most common being specifying latin1 and using cp1252. If None, try to detect the encoding. If it is a callable, the callable is called with two arguments: The recipe object and the source to be decoded. It must return the decoded source.

	extra_css = None
		为下载的HTML文件增加指定的任意额外的CSS。它将被插入到出现在</head>标签前的<style>标签中，因此，会覆盖除了那些在HTML标签内使用style属性声明的所有的CSS样式。例如：

		`extra_css = '.heading { font: serif x-large }'`
	
	feeds = None
		待下载的feed列表。格式可以是 [url1, url2, ...] 或者 [('title1', url1), ('title2', url2),...]

	filter_regexps = []
		List of regular expressions that determines which links to ignore. If empty it is ignored. Used only if is_link_wanted is not implemented. For example:

		filter_regexps = [r'ads\.doubleclick\.net']
		will remove all URLs that have ads.doubleclick.net in them.

		Only one of BasicNewsRecipe.match_regexps or BasicNewsRecipe.filter_regexps should be defined.

	ignore_duplicate_articles = None
		忽略那些出现一个以上元素重复的文章。一个重复的文章指的是那些拥有相同的title或者/和url的文章。要忽略具有相同标题的文章，则设置它为：

		`ignore_duplicate_articles = {'title'}`
		
		用URL代替，则设置它为：
		`ignore_duplicate_articles = {'url'}`
		
		要匹配标题或者URL，则设置它为：
		``ignore_duplicate_articles = {'title', 'url'}``
	
	keep_only_tags = []
		只保留指定的标签及他们的子标签。指定一个标签的格式，请参考BasicNewsRecipe.remove_tags. 若此列表非空，那么<body>标签将会被清空，然后重新填入匹配此列表中项的标签。例如：

		`keep_only_tags = [dict(id=['content', 'heading'])]`
		会只保留属性id为“content” 或 “heading”的标签。

	language = 'und'
		The language that the news is in. Must be an ISO-639 code either two or three characters long

	masthead_url = None
		By default, calibre will use a default image for the masthead (Kindle only). Override this in your recipe to provide a url to use as a masthead.

	match_regexps = []
		正则表达式列表，用来指定follow的链接。若为空，则忽略它。只有当is_link_wanted未实现时才使用它。例如：

		`match_regexps = [r'page=[0-9]+']`
		将匹配所有拥有page=数字的URL

		只能定义BasicNewsRecipe.match_regexps 或 BasicNewsRecipe.filter_regexps。

	max_articles_per_feed = 100
		每一个feed下载的最大文章数。这个对于那些没有文章日期的feed来说是很有用。对于大多数的feed，你应该使用BasicNewsRecipe.oldest_article。

	needs_subscription = False
		此项若为True，在下载的时候，界面将会询问用户的用户名和密码。若设置为“optional”，用户名密码则可选。

	no_stylesheets = False
		便捷标记，用来禁用加载那些具有过于复杂而不适合转换为电子书格式的样式的网站的样式。如果取值为True，则样式不会被下载处理。

	oldest_article = 7.0
		从新闻源下载的最老的文章。以天为单位。

	preprocess_regexps = []
		List of regexp substitution rules to run on the downloaded HTML. Each element of the list should be a two element tuple. The first element of the tuple should be a compiled regular expression and the second a callable that takes a single match object and returns a string to replace the match. For example:

	preprocess_regexps = [
	   (re.compile(r'<!--Article ends here-->.*</body>', re.DOTALL|re.IGNORECASE),
		lambda match: '</body>'),
	]
		将移除<!–Article ends here–> 与 </body>之间的任何东西。

	publication_type = 'unknown'
		Publication type Set to newspaper, magazine or blog. If set to None, no publication type metadata will be written to the opf file.

	recipe_disabled = None
		Set to a non empty string to disable this recipe. The string will be used as the disabled message

	recursions = 0
		Number of levels of links to follow on article webpages

	remove_attributes = []
		从所有标签中移除的属性列表。例如：

		`remove_attributes = ['style', 'font']`
		
	remove_empty_feeds = False
		If True empty feeds are removed from the output. This option has no effect if parse_index is overridden in the sub class. It is meant only for recipes that return a list of feeds using feeds or get_feeds(). It is also used if you use the ignore_duplicate_articles option.

	remove_javascript = True
		Convenient flag to strip all javascript tags from the downloaded HTML

	remove_tags = []
		所有要移除的标签。指定从下载的HTML中要移除的标签。一个标签以一个字典的形式标明：
		```python
		{
		 name      : 'tag name',   #e.g. 'div'
		 attrs     : a dictionary, #e.g. {class: 'advertisment'}
		}
		```
		所有的键都是可选的。查看[Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/bs3/documentation.html#Searching%20the%20Parse%20Tree),获得搜索标准的完整说明。一个常用的例子是：

		`remove_tags = [dict(name='div', attrs={'class':'advert'})]`
		
		这将从下载的HTML中移除所有的<div class="advert">标签及其子标签。

	remove_tags_after = None
		移除所有在指定标签后出现的标签。查看[BasicNewsRecipe.remove_tags](http://manual.calibre-ebook.com/news_recipe.html#calibre.web.feeds.news.BasicNewsRecipe.remove_tags)以获取指定一个标签的格式。例如：

		`remove_tags_after = [dict(id='content')]`
		将会移除第一个出现具有id="content"属性的标签后的所有标签。

	remove_tags_before = None
		移除所有在指定标签前出现的标签。查看[BasicNewsRecipe.remove_tags](http://manual.calibre-ebook.com/news_recipe.html#calibre.web.feeds.news.BasicNewsRecipe.remove_tags)以获取指定一个标签的格式。例如：

		remove_tags_before = dict(id='content')
		将会移除第一个出现具有id="content"属性的标签前的所有标签。

	requires_version = (0, 6, 0)
		使用这个recipe需要的最小calibre版本。

	resolve_internal_links = False
		If set to True then links in downloaded articles that point to other downloaded articles are changed to point to the downloaded copy of the article rather than its original web URL. If you set this to True, you might also need to implement canonicalize_internal_url() to work with the URL scheme of your particular website.

	reverse_article_order = False
		将每个feed中文章逆序

	scale_news_images = None
		Maximum dimensions (w,h) to scale images to. If scale_news_images_to_device is True this is set to the device screen dimensions set by the output profile unless there is no profile set, in which case it is left at whatever value it has been assigned (default None).

	scale_news_images_to_device = True
		Rescale images to fit in the device screen dimensions set by the output profile. Ignored if no output profile is set.

	simultaneous_downloads = 5
		Number of simultaneous downloads. Set to 1 if the server is picky. Automatically reduced to 1 if BasicNewsRecipe.delay > 0

	summary_length = 500
		简述中的最大字数。

	template_css = u'\n .article_date {\n color: gray; font-family: monospace;\n }\n\n .article_description {\n text-indent: 0pt;\n }\n\n a.article {\n font-weight: bold; text-align:left;\n }\n\n a.feed {\n font-weight: bold;\n }\n\n .calibre_navbar {\n font-family:monospace;\n }\n '
		用来为template提供样式的CSS，例如，导航条和内容表。相较于覆盖这个变量，你应该在你的recipe中使用extra_css来定制样式。

	timefmt = ' [%a, %d %b %Y]'
		首页显示的日期格式。默认是: Day_Name, Day_Number Month_Name Year

	timeout = 120.0
		从服务器抽取文件的超时时间，以秒为单位。

	title = u'Unknown News Source'
		电子书使用的标题

	use_embedded_content = None
		Normally we try to guess if a feed has full articles embedded in it based on the length of the embedded content. If None, then the default guessing is used. If True then the we always assume the feeds has embedded content and if False we always assume the feed does not have embedded content.

	use_javascript_to_login = False
		If you set this True, then calibre will use javascript to login to the website. This is needed for some websites that require the use of javascript to login. If you set this to True you must implement the javascript_login() method, to do the actual logging in.