#-*-encoding:utf-8-*-
import pandas as pd
import numpy as np
import xlwt

PATH='/home/idanan/jiayuan/user_infos.txt'
header=['id','gender','age','where','height','edu',\
		'marriage','salary','nation','job',\
		'car','house','look','body','face',\
		'hair','weight','place','smoke','drink',\
		'personality','child','parent']
MAPPY={'愿意':'1','不愿意':'-1','视情况而定':'0','暂未购车':'-1','已经购车':'1','已购住房':'1','暂未购房':'0','需要时购置':'0','与父母同住':'0','住亲朋家':'0','住单位家':'0','住单位房':0,'与人合租':'0','独自租房':'0','中专或相当学历':'1','大专':'2','本科':'3','双学士':'4','硕士':'5','博士':'6','博士后':'7','未婚':'0,0','离异,无小孩':'1,0','离异,有小孩归自己':'1,1','离异':'1,1','离异,有小孩归对方':'1,1','丧偶,无小孩':'1,0','丧偶,有小孩归自己':'1,1','丧偶,有小孩归对方':'1,1','苗条':'-1','高挑':'-1','匀称':'0','丰满':'1','健壮':'2','魁梧':'2','方脸型':'1','国字脸型':'1','菱形脸型':'1','三角脸型':'1','圆脸型':'0','鸭蛋脸型':'0','瓜子脸型':'0','不吸，很反感吸烟':'3','不吸，但不反感':'1','社交时偶尔吸':'-1','每周吸几次':'-2','每天都吸':'-4','有烟瘾':'-5','社交需要时喝':'0','有兴致时喝':'-1','每天都离不开酒':'-4','不喝':'1','光头':'0','很短':'1','短发':'2','中等长度':'3','卷曲长发':'5','顺直长发':'5','淡雅如菊':'1,0','娇小依人':'0,0','眉清目秀':'1,0','明眸善睐':'0,1','成熟魅力':'1,1','青春活泼':'0,0','秀外慧中':'0,1','雍容华贵':'1,1','未填':'NA'}

def loadDict(fpath):
	mappy={}
	with open(fpath,'r') as f:
		for line in f:
			try:
				key,value=line.strip().split(':')
				mappy[key]=value
			except:
				pass
	return mappy


def loadData(path):
	infos=[]
	with open(path) as f:
		for line in f:
			info=line.strip().split('|')
			infos.append(info)
	return infos

def departData(infos):
	male=[]
	female=[]
	for info in infos:
		if info[1]=='女':
			female.append(info)
		else:
			male.append(info)
	
	return male,female


def transform(data,mappy):
	def mapping(x):
		if x in mappy.keys():
			return mappy[x]
		else:
			return x
#	def departInfo(info,filters):
#		info1=[info[i] for i in filters]
#		info2=[info[i] for i  in range(23) if i not in FILTERS]
#		return [info1,info2]
	new_data=[]
	for info in data:
		new_info=map(mapping,info)
		new_data.append(new_info)
	return new_data


def saveData(data,path):
	with open(path,'w') as f:
		for line in data:
			s=[str(i) for i in line]
			f.write('|'.join(s)+'\n')


def quantile(array,quantiles):
	for p,v in enumerate(array):
		rate=0
		for i in quantiles:
			if v>i:
				rate+=1
			else:
				break
		array[p]=rate
	return array
def save_excel(fpath,name,lists):
	workbook=xlwt.Workbook()
        sheet=workbook.add_sheet(name)
	height=len(lists)
	width=len(lists[1])
	for i in range(height):
		li=lists[i]
		for j in range(width):
			string=li[j].decode('utf-8')
			sheet.write(i,j,string)
			workbook.save(fpath+'/'+name+'.xls')

infos=loadData('/home/idanan/jiayuan/parsed_female_info.txt')
save_excel('/home/idanan/jiayuan','parsed_female',infos)

	

						
