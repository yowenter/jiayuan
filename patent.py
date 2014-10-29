# -*- coding: utf-8 -*-

import requests
import os
import codecs
from bs4 import BeautifulSoup as soup
from threading import Thread
from time import sleep
import re
import platform
import getpass
import xlwt

system=platform.uname()[0]
username=getpass.getuser()

if system=='Windows':
    patent_path='d:/patents'
else:
    patent_path='/home/'+username+'/patent'
if not os.path.exists(patent_path):
    os.mkdir(patent_path)
    
result_url='http://www.pss-system.gov.cn/sipopublicsearch/search/executeGeneralSearch-returnResultOnly.shtml'
home_headers='''
Accept:text/html, */*
Accept-Encoding:gzip,deflate,sdch
Accept-Language:zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2,ru;q=0.2
Connection:keep-alive
Content-Length:235
Content-Type:application/x-www-form-urlencoded
Host:www.pss-system.gov.cn
Origin:http://www.pss-system.gov.cn
Referer:http://www.pss-system.gov.cn/sipopublicsearch/search/searchHome-searchIndex.shtml
User-Agent:Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36
X-Requested-With:XMLHttpRequest
'''


search_data='''
searchCondition.searchExp:申请（专利权）人=(%s)
searchCondition.dbId:VDB
searchCondition.searchType:Sino_foreign
wee.bizlog.modulelevel:0200101
'''

#the post data :pagenumber*10;patent owner;
page_data='''
resultPagination.limit:10
resultPagination.start:{0}
searchCondition.searchType:Sino_foreign
searchCondition.dbId:
searchCondition.searchExp:申请（专利权）人=({1})
searchCondition.strategy:
wee.bizlog.modulelevel:0200101
searchCondition.executableSearchExp:VDB:(PAVIEW='{2}')'''

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
    
        

#change string to dictionary
def dicts(s):
    s=s.strip().split('\n')
    h={}
    for i in s:
        key,value=i.split(':',1)
        h[key]=value
    return h

def page_number(html):
    div=html.find('div',attrs={'align':'center','style':'padding-top: 10px;'}).div
    last_page=str(div.find_all('a')[-1])
    last=re.search('(\d+)',last_page).group()
    last=int(last)
    return last

#search someone ,return pages number .
def search_people(name):
    data=dicts(search_data%name)
    headers=dicts(home_headers)
    session=requests.Session()
    r=session.post(result_url,headers=headers,data=data)
    html=soup(r.text)
    last_number=page_number(html)
    return last_number

#five threads download page.
def fetch_byname(name):
    threads=[]
    name_path=patent_path+'/'+name
    if not os.path.exists(name_path):
            os.mkdir(name_path)
    total_number=search_people(name)/10
    numbers=[i for i in range(0,total_number+1)]
    numbers=map(lambda x:str(x)+'0',numbers)
    
    def fetch_nums(numbers):
        for number in numbers:
            if int(number)/1000==0:
                sleep(100)
            data=dicts(page_data.format(number,name,name))
            headers=dicts(home_headers)
            session=requests.Session()
            r=session.post(result_url,headers=headers,data=data)
            text=r.text
            save_page(text,name_path,number)
            
    multi_threads(fetch_nums,numbers)


def save_page(text,fpath,fname):
    f=codecs.open(fpath+'/'+fname+'.html',mode='w',encoding='utf-8')
    f.write(text)
    f.close()

def convert_txt(fpath):
    with open(fpath,'r') as f:
        text=f.read()
        html=soup(text)
        return html



def rmspace(s):
    s=re.sub('\n|\t| ','',s)
    return s


'''
申请号­: CNXXXXX
申请日:XXXX
公开（公告）号­: XXXX
公开（公告）日: XXXX
发明名称: XXXX
IPC分类号: XXX
申请（专利权）人:XXX
发明人: XXX
优先权号:
优先权日:
'''
#']':'\xe3\x80\x91'
#'[':'\xe3\x80\x90'

def parse(html):
    all_patents=[]
    patents=html.find_all('div',attrs={'style':'float: left; width: 600px;'})
    h3s=html.find_all('h3',class_='sqh')
    h3s=map(lambda x:re.sub('\t|\n| ','',x.text.encode('utf-8')),h3s)
    if len(h3s)==len(patents):
        length=len(h3s)
        for i in range(length):
            si_patent=[]
            try:
                kind=re.search('\xe3\x80\x90(.*)\xe3\x80\x91',h3s[i]).group()
            except:
                kind='\xe3\x80\x90UNKNOWN\xe3\x80\x91'
            si_patent.append(kind)
            infos=patents[i].find_all('div',class_='conter_talbe')
            for info in infos:
                info=rmspace(str(info.text.encode('utf-8'))).split(':')[1]
                si_patent.append(info)
            all_patents.append(si_patent)
    else:
        all_patents=[]
    return all_patents

def save_patent(patents,fpath,fname):
    with open(fpath+'/'+fname+'.txt','a') as f:
        for patent in patents:
            info=' | '.join(patent)
            f.write(info+'\n')


def multi_parse(folder,fname):
    files=os.listdir(folder)
    files=map(lambda x:folder+'/'+x,files)
    def parse_files(files):
        total_patents=[]
        for f in files:
            html=convert_txt(f)
            patents=parse(html)
            total_patents=total_patents+patents
        save_patent(total_patents,patent_path,fname)

    multi_threads(parse_files,files)

def save_excel(fpath,name,lists):
    workbook=xlwt.Workbook()
    sheet=workbook.add_sheet(name)
    height=len(lists)
    for i in range(height):
        li=lists[i]
        width=len(li)
        for j in range(width):
		string=li[j].decode('utf-8')
		sheet.write(i,j,string)
    workbook.save(fpath+'/'+name+'.xls')

def read_txt(fpath):
    with open(fpath,'r') as f:
        all_infos=[]
        for line in f:
            infos=line.strip().split(' |')
            all_infos.append(infos)
        return all_infos

def txt_excel(source,target,name):
    infos=read_txt(source)
    save_excel(target,name,infos)
    
            


txt_excel('/home/idanan/jiayuan/user_infos(3).txt','/home/idanan/jiayuan','user_info')            
    

#fetch_byname('浙江吉利')

#multi_parse('d:/patent/zhejiang','zhejiang3')

#txt_excel('d:/patent/zhejiang3.txt','d:/patent','zhejiang')


            
    


            
        
        


