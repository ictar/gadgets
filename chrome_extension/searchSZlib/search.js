/**
 * Get the current title.
 *
 * @param {function(string)} callback - called when the title of the current tab
 *   is found.
 */
function getCurrentTabTitle(callback) {
	// Query filter to be passed to chrome.tabs.query - see
  	// https://developer.chrome.com/extensions/tabs#method-query
	var queryInfo = {
		active: true,
		currentWindow: true
	};
	
	chrome.tabs.query(queryInfo, function(tabs){
		// A window can only have one active tab at a time, so the array consists of
		// exactly one tab.
		var tab = tabs[0];

		// A tab is a plain object that provides information about the tab.
    	// See https://developer.chrome.com/extensions/tabs#type-Tab
    	var title = tab.title;
    	console.assert(typeof title == "string", "tab.title should be a string");
    	console.log("search title: " + title);
    	if (title.indexOf("(豆瓣)") != -1) {
    		title = title.substr(0, title.indexOf("(豆瓣)")).trim()
    	}
    	callback(title);
	})
}

/**
 * @param {string} searchTerm - Search term for szlib search.
 * @param {function(string)} callback - Called when the booklist has
 *   been found. The callback gets booklist.
 * @param {function(string)} errorCallback - Called when the booklist is not found.
 *   The callback gets a string that describes the failure reason.
 */
function getSzlibBookList(searchTerm, callback, errorCallback) {
	var szlib = "http://www.szlib.org.cn"
	var searchUrl = szlib + "/Search/searchshow.jsp?v_tablearray=bibliosm,serbibm,apabibibm,mmbibm,&v_index=title&v_value=" + encodeURIComponent(searchTerm) + "&sortfield=score&sorttype=desc";

	$.ajax({
		type: 'GET',
		url: searchUrl,
		dataType: 'html',
		success: function(data){
			var booklist = $(data).find(".booklist")
			if (booklist.length == 0) {
				errorCallback("搜无此书！");
				return;
			}
			callback(szlib, booklist[0]);
		},
		error: function(){
			errorCallback("网络错误。");
		}

	});
}

function renderStatus(statusText) {
	$('#status').html(statusText);
}

function renderSearchResult(domain, booklist) {
	console.log(booklist)
	var result = $('#searchresult');
	// each detail
	$(booklist).find("a").each(function(){
		var href = $(this).attr("href");
		$(this).attr("target", "")
		if (href.startsWith("searchdetail.jsp")) {
			$(this).attr("href", domain+"/Search/"+href)
			
		}
		if (href.startsWith("../")) {
			$(this).attr("href", domain+href);
			$(this).attr("target", "");
		}
		if (href.startsWith("#")) {
			$(this).remove();
		}
	});	
	result.html(booklist);
	$(".booklist").css("padding", 0)
	$(".booklist>li").css("margin-bottom", 15)
	result.show();
}

document.addEventListener('DOMContentLoaded', function() {
	getCurrentTabTitle(function(title){
		getSzlibBookList(title, function(domain, result){
			renderStatus("在" + domain + "中搜索图书：" + title)
			renderSearchResult(domain, result)
		}, function(errMsg){
			renderStatus("找不到这本书T_T " + errMsg);
		});
	});
});