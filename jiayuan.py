import requests
import codecs
from threading import Thread
from time import sleep


login_url='https://passport.jiayuan.com/dologin.php'
love_url='http://love.jiayuan.com/result.php?from_search=2&&p=%d'
#love_url%(1-3509)

user_infos='/home/idanan/jiayuan/user_infos'
id_path='/home/idanan/jiayuan/lovers_ids.txt'

login_data='''
name:2512346040@qq.com
password:dandan123
'''
headers='''
Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Encoding:gzip,deflate,sdch
Accept-Language:zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2,ru;q=0.2
Cache-Control:max-age=0
Connection:keep-alive
Host:www.jiayuan.com
User-Agent:Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'''


login_headers='''
Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Encoding:gzip,deflate,sdch
Accept-Language:zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2,ru;q=0.2
Cache-Control:max-age=0
Connection:keep-alive
Content-Length:139
Content-Type:application/x-www-form-urlencoded
Host:passport.jiayuan.com
Origin:http://login.jiayuan.com
Referer:http://login.jiayuan.com/
User-Agent:Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'''


love_headers='''Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Encoding:gzip,deflate,sdch
Accept-Language:zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2,ru;q=0.2
Cache-Control:max-age=0
Connection:keep-alive
Host:love.jiayuan.com
User-Agent:Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'''


def dicts(s):
	s=s.strip().split('\n')
	h={}
	for i in s:
		key,value=i.split(':',1)
		h[key]=value
	return h

def login(url,data,headers):
	data=dicts(data)
	headers=dicts(headers)
	s=requests.Session()
	r=s.post(url,data=data,headers=headers)
	cookies=r.cookies
	return cookies

def fetch(url,headers,cookies=None):
	headers=dicts(headers)
	r=requests.get(url,headers=headers)
	return r.text


def fetch_id(uid,cookies):
	url='http://www.jiayuan.com/'+str(uid)
	try:
		r=requests.get(url,headers=dicts(headers),cookies=cookies,timeout=5)
		html=r.text
	except Exception as e:
		log(str(e))
		html='None'
	return html
	

def log(error):
	with open('/home/idanan/jiayuan/error.log','a') as f:
		f.write(error)

def save_page(text,fpath,fname):
	f=codecs.open(fpath+'/'+fname+'.html',mode='w',encoding='utf-8')
	f.write(text)
	f.close()


def fetch_lovers(fpath,urls):
	for url in urls:
		page=fetch(url,love_headers)
		fname=url[39:]
		save_page(page,fpath,fname)
		if int(fname)%100==0:
			sleep(5)




def multi_fetch_lovers():
	fpath='/home/idanan/jiayuan/lovers'
	page_number=3509
	urls=[]
	for i in range(1,6):
		si_urls=[num for num in range(i,3509,5)]
		si_urls=map(lambda x:love_url%x,si_urls)
		urls.append(si_urls)

	threads=[]
	for url_list in urls:
		thread=Thread(target=fetch_lovers,args=(fpath,url_list,))
		threads.append(thread)

	for i in threads:
		i.start()
		sleep(3)
	for i in threads:
		i.join()


def read_lovers(fpath):
	urls=[]
	with open(fpath,'r') as f:
		for line in f:
			url=line.strip()
			urls.append(url)
	return urls

def read_ids(fpath):
	ids=[]
	with open(fpath,'r') as f:
		for line in f:
			try:
				date,id1,id2=line.strip().split(' ',2)
				ids=ids+[id1,id2]
			except:
				pass
	return ids

def fetch_ids(ids):
	cookies=login(login_url,login_data,login_headers)
	for i in ids:
		info=fetch_id(i,cookies)
		save_page(info,user_infos,str(i))

def part_list(lists):
	length=len(lists)
	step=length/5
	new_list=[]
	for i in range(0,length,step):
		si_list=lists[i:i+step]
		new_list.append(si_list)
	return new_list

def multi_fetch_ids():
	threads=[]
	ids=read_ids(id_path)
	ids=part_list(ids)
	for si_ids in ids:
		thread=Thread(target=fetch_ids,args=(si_ids,))
		threads.append(thread)
	for i in threads:
		i.start()
		sleep(3)
	for i in threads:
		i.join()




def fetch_loverspage():
	fpath='/home/idanan/jiayuan/lovers_page'
	urls=read_lovers('/home/idanan/jiayuan/lovers_space.txt')
	new_urls=part_list(urls)
	threads=[]
	for url_list in new_urls:
		thread=Thread(target=fetch_lovers,args=(fpath,url_list,))
		threads.append(thread)

	for i in threads:
		i.start()
		sleep(3)
	for i in threads:
		i.join()




	
#multi_fetch_lovers()
#fetch_loverspage()
#cookies=login(login_url,login_data,login_headers)
#
#r=requests.get('http://www.jiayuan.com/2138205?from=story&fxly=cp-pd-cggs',cookies=cookies)
#save_page(r.text,'/home/idanan/','text')
#

#multi_fetch_ids()
#:print 'ok'
