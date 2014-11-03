#-*-encoding:utf-8-*-
#!env /usr/bin/python
'''
Author:wenter.woo
Email:airywent@gmail.com
'''
import pandas as pd
import numpy as np
import re
import xlwt



header=['id','gender','age','where','height','edu',\
		'marriage','salary','nation','job',\
                'car','house','look','body','face',\
                'hair','weight','place','smoke','drink',\
                'personality','child','parent']



#The string in text is decoded as utf-8,while the string in shell need to be decode to utf-8

mapping={'愿意':'1','不愿意':'-1','视情况而定':'0','暂未购车':'-1','已经购车':'1',\
	'已购住房':'1','暂未购房':'0','需要时购置':'0','与父母同住':'0','住亲朋家':'0','住单位家':'0',\
       '住单位房':0,'与人合租':'0','独自租房':'0',\
       '中专或相当学历':'1','大专':'2','本科':'3','双学士':'4','硕士':'5','博士':'6','博士后':'7',\
       '未婚':'0,0','离异,无小孩':'1,0','离异,有小孩归自己':'1,1','离异':'1,1','离异,有小孩归对方':'1,1',\
       '丧偶,无小孩':'1,0','丧偶,有小孩归自己':'1,1','丧偶,有小孩归对方':'1,1',\
       '苗条':'-1','高挑':'-1','匀称':'0','丰满':'1','健壮':'2','魁梧':'2',\
       '方脸型':'1','国字脸型':'1','菱形脸型':'1','三角脸型':'1','圆脸型':'0','鸭蛋脸型':'0','瓜子脸型':'0','长脸型':'1',\
	'不吸，很反感吸烟':'3','不吸，但不反感':'1','社交时偶尔吸':'-1','每周吸几次':'-2','每天都吸':'-4','有烟瘾':'-5',\
	'社交需要时喝':'0','有兴致时喝':'-1','每天都离不开酒':'-4','不喝':'1',\
	 '光头':'0','很短':'1','短发':'2','中等长度':'3','卷曲长发':'5','顺直长发':'5',\
	 '淡雅如菊':'1,0','娇小依人':'0,0','眉清目秀':'1,0','明眸善睐':'0,1','成熟魅力':'1,1','青春活泼':'0,0',\
	 '秀外慧中':'0,1','雍容华贵':'1,1','女':'M','未填':'NA','保密':'NA',
	 '10000～20000元':'2','20000元以上':'3','2000元以下':'-1','2000～5000元':'0','5000～10000元':'1'}


def loadDict(fpath):
	fmap={}
	with open(fpath) as f:
		for line in f:
			s=line.strip().split(' ')
			if len(s)>1:
				fmap[s[0]]=s[-1]
			else:
				fmap[s[0]]='0,0,0'
	return fmap


def loadData(fpath):
	data=pd.read_csv(fpath,names=header,sep='|')
	return data

def departData(data):
	female=data[data['gender']=='女']
	male=data[data['gender']=='男']
	return female,male

#convert the values of columns from continus to descrete,and filter the outliers.

def nummeric(data,columns):
	def search(x):
		result=re.search('(\d+)',str(x))
		if result:
			return result.group()
		else:
			return -1
	for col in columns:
		data[col]=data[col].map(search)
	return data

def convertWhere(data,fpath):
	fmap=loadDict(fpath)
	def imap(x):
		return fmap.get(x,'0,0,0')
	fromwhere=data['where'].map(lambda x:re.sub('来自','',x))
	data['where']=fromwhere.map(imap)
	return data


def quantize(data,columns):
	for col in columns:
		data[col]=data[col].astype(int)
		values=data[col].describe()
		rates=[values['min'],values['25%'],values['50%'],values['75%'],values['max']]
		data[col]=pd.cut(data[col],rates,labels=[-1,0,1,2])
	return data

def calbmi(data):
	def bmi(w,h):
		try:
			w=int(w)
			h=int(h)
			if w!=0 and h!=0:
				return float(w)/(h*h/10000)
			else:
				return -1
		except:
			return -1
	f=lambda x:bmi(x['weight'],x['height'])
	data['bmi']=data.apply(f,axis=1)
	return data


#map data to transform from string to nummeric
def transform(data,mapping):
	def xmap(x):
		if x in mapping:
			return mapping[x]
		else:
			return x
	for col in header:
		data[col]=data[col].map(xmap)
	return data


def saveData(data,fpath):
	data.to_csv(fpath+'.txt',sep='|',index=False,header=True)
	
	

user_info='/home/idanan/jiayuan/user_info.txt'
pd.set_option('mode.chained_assignment',None)
data=loadData(user_info)
female,male=departData(data)
female=transform(female,mapping)
female=nummeric(female,['age','height','weight'])
female=calbmi(female)
female=quantize(female,['age','height','weight','bmi'])
female=convertWhere(female,'/home/idanan/jiayuan/code/from_dict.txt')
female['nation']=female['nation'].map(lambda x:{'汉族':1}.get(x,0))
female.drop(labels=['place','personality','weight'],axis=1,inplace=True)
saveData(female,'/home/idanan/jiayuan/code/pd_female')

#female=quantize(female,['height','weight'])
#saveData(transform(female,mapping),'/home/idanan/jiayuan/transed_female.txt')
