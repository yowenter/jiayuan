#-*-encoding:utf-8-*-
from bs4 import BeautifulSoup as soup
import os
import re
from time import sleep
from threading import Thread
import codecs

secret='\xe4\xbf\x9d\xe5\xaf\x86'
links=[]
jiayuan='/home/idanan/jiayuan'
lovers='/home/idanan/jiayuan/lovers'
lovers_page='/home/idanan/jiayuan/lovers_page'
USER_INFOS='/home/idanan/jiayuan/user_infos'
log_file='/home/idanan/jiayuan/parse_error.log'

def log(error):
	with open(log_file,'a') as f:
		f.write(error+'\n')


def depart(lists):
    length=len(lists)
    step=length/5
    new_list=[]
    for i in range(0,length,step):
        si_list=lists[i:i+step]
        new_list.append(si_list)
    return new_list

def multi_threads(function,lists):
    lists=depart(lists)
    threads=[]
    for li in lists:
        threads.append(Thread(target=function,args=(li,)))
    for i in threads:
        i.start()
        sleep(5)
    for i in threads:
        i.join()
    


def convert_txt(fpath):
	with open(fpath,'r') as f:
		text=f.read()
		html=soup(text)
		return html

def parse_lover(html):
	dls=html.find_all('dl',class_='list')
	links=[]
	for dl in dls:
		if secret not in dl.text.encode('utf-8'):
			link=re.search("window\.open\(\\'(.*?)\\'",str(dl)).groups()[0]
			links.append(link)
	return links

def parse_person(html):
	colon='\xef\xbc\x9a'
        comma='\xef\xbc\x8c'
	sid=html.find('p',class_='user_id').text.encode('utf-8').split(colon)[1]
	myInfo=html.find('div',class_='my_information')
	baseInfo=myInfo.h2.text.encode('utf-8')[20:].split(comma)
	del(baseInfo[2])
	f=lambda x:map(lambda x:x.text.encode('utf-8').split(colon)[1],x)
	detailsA,detailsB=myInfo.find('ul',class_='details').find_all('li')
	detailsA=detailsA.find_all('span')
	detailsB=detailsB.find_all('span')
	detailsA=f(detailsA)
	detailsB=f(detailsB)
	look=html.find('div',class_='aspect claim').ul.find_all('li')
	look=f(look)
	look=look[:6]
	del(look[4])
	work_content=html.find('div',class_='work_life_content')\
			.ul.find_all('li')
	work_content=f(work_content)
	filts=[2,18,19,20,23,26]
	work_content=[work_content[i] for i in filts]

	all_info=[sid]+baseInfo+detailsA+detailsB+look+work_content
	all_info=' |'.join(all_info)


	return all_info


def parse_loverspage(html):
	try:
		dl=html.find('dl',class_='zrg') 
		hrefs=list(set(re.findall('''a href="(.*?)" target="_blank''',str(dl))))
		date='-'.join(re.search('(\d{4})\xe5\xb9\xb4(\d{2})\xe6\x9c\x88(\d{2})',dl.text.encode('utf-8')).groups())
		search=lambda x:re.sub('\D','',x)
		ids=map(search,hrefs)
		info=[date]+ids
	except:
		info=None
	
	return info

def save_links(links):
	with open(jiayuan+'/'+'lovers_space.txt','w') as f:
		for link in links:
			f.write(link+'\n')
def save_lovers(infos):
	with open(jiayuan+'/'+'lovers_ids.txt','a') as f:
		for info in infos:
			f.write(' '.join(info)+'\n')

def saveInfos(infos):
	f=codecs.open(jiayuan+'/user_infos.txt','a','utf-8')
	for info in infos:
		f.write(info.decode('utf-8')+'\n')
	f.close()


def extract_infos(files):
	infos=[]
	for f in files:
		html=convert_txt(USER_INFOS+'/'+f)
		try:
			info=parse_person(html)
			infos.append(info)
		except Exception as e:
			log(str(f)+str(e))


	saveInfos(infos)

def extract_links():
	files=os.listdir(lovers)
	for f in files:
		html=convert_txt(lovers+'/'+f)
		links=parse_lover(html)
	save_links(links)


def extract_lovers(files):
	infos=[]
	for f in files:
		html=convert_txt(lovers_page+'/'+f)
		info=parse_loverspage(html)
		if info is not None :
			infos.append(info)

	save_lovers(infos)


def multi_extract(folder,function):
	files=os.listdir(folder)
	multi_threads(function,files)

extract_infos(os.listdir(USER_INFOS))
