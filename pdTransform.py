#-*-encoding:utf-8-*-
#!env /usr/bin/python
'''
Author:wenter.woo
Email:airywent@gmail.com
'''
import pandas as pd
import numpy as np
import re
from functools import partial

def loadMapping(fpath):
	mapping={}
	with open(fpath) as f:
		for line in f:
			key,value=line.strip().split(':')
			mapping[key]=value
	return mapping


def loadData(fpath,header):
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
			return 0 
	for col in columns:
		data[col]=data[col].map(search)
	return data

def convertWhere(data,fpath):
	def loadDict(fpath):
		fmap={}
		with open(fpath) as f:
			for line in f:
				s=line.strip()
				s=re.split('\t| ',s)
				key=s[0]
				if len(s)>1:
					fmap[key]=s[-1]
				else:
					fmap[key]='0,0,0'
		return fmap
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

def extract(value,number):
	if value!='NA' and type(value)==str:
		values=value.split(',')
		return values[number]
	else:
		return 0




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
	data.to_csv(fpath,sep='|',index=False,header=True)
	
	
def parse(gender):
	data=loadData(user_info,header)
	female,male=departData(data)
	if gender=='F':
		data=female
	if gender=='M':
		data=male

	data=transform(data,mapping)
	data=nummeric(data,['age','height','weight'])
	data=calbmi(data)
	data=convertWhere(data,'/home/idanan/jiayuan/code/from_dict.txt')
	data['nation']=data['nation'].map(lambda x:{'汉族':1}.get(x,0))
	data.drop(labels=['place','personality','weight','job'],axis=1,inplace=True)
	for col in ['where','marriage','look']:
		for i in range(2):
			new_col=col+str(i)
			data[new_col]=data[col].map(partial(extract,number=i))
	data['where2']=data['where'].map(partial(extract,number=2))
	data.drop(labels=['where','marriage','look'],axis=1,inplace=True)
	data.replace('NA',0,inplace=True)
	saveData(data,'/home/idanan/jiayuan/code/transed_{0}.txt'.format(gender))
	
#pd.set_option('mode.chained_assignment',None)
#header=['id','gender','age','where','height','edu',\
#		'marriage','salary','nation','job',\
#                'car','house','look','body','face',\
#                'hair','weight','place','smoke','drink',\
#                'personality','child','parent']
#user_info='/home/idanan/jiayuan/user_info.txt'
#mapping=loadMapping('/home/idanan/jiayuan/code/femaleMapping.txt')
#parse('F')
#
	
