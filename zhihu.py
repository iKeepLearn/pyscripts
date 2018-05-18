#coding=utf-8
import requests,re,sys,json,os


def strip_tags(html):
	dr = re.compile(r'<[^>]+>',re.S)
	dd = dr.sub('',html)
	dd=dd.replace('&amp;','&')
	return dd

class Zhihu(object):

	status=0
	headers={
		'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
		'authorization':'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
	}
	questions=[]

	def print_questions(self):
		os.system('clear')
		for i in self.questions:
			print("<"+i['qid']+"> "+i['title'])

	def cmd(self):

		if self.status==0:	 #提问
			q='search question'
		elif self.status==1: #选择问题
			q='select question'
		
		c=input(q+" >")

		if not c:
			return

		if c=='q':
			if self.status==0:
				exit()
			self.status=0
			return

		if not re.findall('^[0-9]+$',c):
			self.status=0

		if self.status==0:	 #提问
			r=self.search_question(c)
			if not r:
				print('no questions')
				return
			self.questions=r
			self.status=1
			self.print_questions()
		elif self.status==1: #选择问题
			self.get_answer(c)

	def search_question(self,q):
		url="https://www.zhihu.com/api/v4/search_v3?t=general&q="+q+"&correction=1&offset=0&limit=40&search_hash_id="

		r=requests.get(url,headers=self.headers).content
		r=json.loads(str(r))

		if 'data' not in r:
			print(r)
			exit()

		r=r['data']
	
		result=[]
		for i in r:
			if 'highlight' not in i:continue
			if 'question' not in i['object']:continue
			qid=i['object']['question']['id']
			title=i['highlight']['title'].replace('<em>','').replace('</em>','')
			url="https://www.zhihu.com/question/"+i['object']['question']['id']
			comment_count=str(i['object']['comment_count'])
			result.append({
				"qid":qid,
				"title":title,
				"url":url,
				"comment_count":comment_count
			})
		return result

	def get_answer(self,qid):
		url='https://www.zhihu.com/api/v4/questions/'+qid+'/answers?sort_by=default&include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[*].mark_infos[*].url;data[*].author.follower_count,badge[?(type=best_answerer)].topics&limit=1000&offset=0'
		r=requests.get(url,headers=self.headers).content
		try:
			r=json.loads(str(r))['data']
		except:
			print('get answer error')
			return
		for i in r:
			aid=str(i['id'])
			content=strip_tags(i['content'])

			print("<comment id:"+aid+">")
			print(content)

			c=input('>')
			if c=='q':
				self.print_questions()
				return
		print("<end>")
		input("")
		self.print_questions()

	def __init__(self):
		while True:
			self.cmd()

if __name__ == "__main__":
	try:
		Zhihu()
	except Exception as e:
		print(e)
