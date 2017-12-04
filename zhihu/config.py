LoginUrl = "https://www.zhihu.com/api/v3/oauth/sign_in"


QueAnsUrl = "https://www.zhihu.com/api/v4/questions/{}/answers"
QuestionIds = [39910834, 28070701, 19855515, 22464714, 26811466, ]
#AnsInclude = "data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,upvoted_followees;data[*].mark_infos[*].url;data[*].author.follower_count,badge[?(type=best_answerer)].topics"

AnsInclude = "data[*].is_normal,suggest_edit,comment_count,content,editable_content,voteup_count,created_time,updated_time,question,excerpt,relationship.is_authorized,data[*].mark_infos[*].url;badge[?(type=best_answerer)].topics"

AnsHeaders = {
	#"accept": "application/json, text/plain, */*",
	"Host": "www.zhihu.com",
	"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
	"Cookie": '_za=dd17cef0-8d79-4518-9321-b7a8511b40ab; udid="ABDAVfoOlQmPTiHZV75PM7_lITesn_Vfrn8=|1457662693"; d_c0="ABAAD97YqQmPTrBwVMc2omnjxXl52dnXVVQ=|1458797071"; _zap=b6c7feae-126e-4da7-8317-2a88e8bea0a1; _ga=GA1.2.223891058.1470978247; aliyungf_tc=AQAAACproETREwQA27EPtw0gitu/2g0h; acw_tc=AQAAAPg9VykZiwIAYECNPXyS3OIuqC2y; s-t=autocomplete; s-q=%E9%A5%AD%E5%90%A6; s-i=1; sid=fimh83do; r_cap_id="YTkyYTFhNDYxYmI2NDdkOGFhM2U4NjU4MTMzZjQ2YTY=|1502246428|24bfd0aacad03d9b57e942df70ffdade10b4fb33"; cap_id="NmYzM2NjNWIxMmU3NDJiOWFjODA3MzI2ZjQ4YjZiOTk=|1502246428|509d4eb24fc2cd44835ec6d9ea00f4a9fa181b18"; z_c0=Mi4wQUJDS3JLMGFCQWtBRUFBUDN0aXBDUmNBQUFCaEFsVk5KZ095V1FBRzhpOE9GTGQ3ZWRESzA4emI3dEVMdDUyMktn|1502246438|a82daac8b2eb657ddc6eb52c6bef1b55a5cfbf77; q_c1=15aa1c13682247d5a11f8e6b7f73081f|1502673406000|1457401969000; __utma=51854390.223891058.1470978247.1502963238.1503032829.208; __utmc=51854390; __utmz=51854390.1503032829.208.48.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.100--|2=registration_date=20151116=1^3=entry_date=20151116=1; _xsrf=894804e5599d3ed50816a9226518be6c',
}