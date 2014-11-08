#-*-encoding:utf-8-*-
import re

PATH='/home/idanan/jiayuan/user_infos.txt'
header=['id','gender','age','where','height','edu',\
		'marriage','marr2','salary','nation','job',\
		'car','house','look','look2','body','face',\
		'hair','weight','place','smoke','drink',\
		'personality','child','parent']
MAPPY={'愿意':'1','不愿意':'-1','视情况而定':'0','暂未购车':'-1','已经购车':'1',\
		'已购住房':'1','暂未购房':'0','需要时购置':'0','与父母同住':'0','住亲朋家':'0','住单位家':'0',\
		'住单位房':0,'与人合租':'0','独自租房':'0',\
		'中专或相当学历':'1','大专':'2','本科':'3','双学士':'4','硕士':'5','博士':'6','博士后':'7',\
		'未婚':'0,0','离异,无小孩':'1,0','离异,有小孩归自己':'1,1','离异':'1,1','离异,有小孩归对方':'1,1',\
		'丧偶,无小孩':'1,0','丧偶,有小孩归自己':'1,1','丧偶,有小孩归对方':'1,1','丧偶':'-1,0',\
		'苗条':'-1','高挑':'-1','匀称':'0','丰满':'1','健壮':'2','魁梧':'2',\
		'方脸型':'1','国字脸型':'1','菱形脸型':'1','三角脸型':'1','圆脸型':'0','鸭蛋脸型':'0','瓜子脸型':'0',\
		'不吸，很反感吸烟':'3','不吸，但不反感':'1','社交时偶尔吸':'-1','每周吸几次':'-2','每天都吸':'-4','有烟瘾':'-5',\
		'社交需要时喝':'0','有兴致时喝':'-1','每天都离不开酒':'-4','不喝':'1',\
		'光头':'0','很短':'1','短发':'2','中等长度':'3','卷曲长发':'5','顺直长发':'5',\
		'淡雅如菊':'1,0','娇小依人':'0,0','眉清目秀':'1,0','明眸善睐':'0,1','成熟魅力':'1,1','青春活泼':'0,0',\
		'秀外慧中':'0,1','雍容华贵':'1,1','未填':'NA','10000～20000元':'2','20000元以上':'3','2000元以下':'-1',\
		'2000～5000元':'0','5000～10000元':'1','女':'M'}


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
	new_data=[]
	for info in data:
		new_info=map(mapping,info)
		new_data.append(new_info)
	return new_data


def saveData(data,path):
	with open(path,'w') as f:
		f.write('|'.join(header)+'\n')
		for line in data:
			s=[str(i) for i in line]
			f.write('|'.join(s)+'\n')


def nummeric(data,columns):
	def search(x):
		result=re.search('(\d+)',x)
		if result:
			return result.group()
		else:
			return 0

	for i,row in enumerate(data):
		for j in columns:
			data[i][j]=search(row[j])
	return data

def addColumn(data,columns,dims=2):
	for i,row in enumerate(data):
		for j in columns:
			if row[j]=='NA':
				if dims=2:
					data[i][j]='NA|NA'
				if dims=3:
					data[i][j]='NA|NA|NA'
			else:
				data[i][j]=re.sub(',','|',row[j])
	return data


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


def descCol(data,column):
	col=[]
	for row in data:
		col.append(row[column])
	col=filter(lambda x:x!='NA',col)
	values=pd.DataFrame(col).astype(int).describe()
	bins=[values['min'],values['25%'],values['50%'],values['75%'],values['max']]
	return bins

def calBMI(x,y):
	if x!='NA' and y!='NA':
		if int(x)!=0 and int(y)!=0:
			t=float(y)*int(y)/10000
			return int(x)/t
		else:
			return 0
	else:
		return 0

def appendBMI(data):
	for row in data:
		bmi=calBMI(row[16],row[4])
		row.append(bmi)
	return data

def test(fpath,width):
	with open(fpath,'r') as f:
		for line in f:
			length=len(line.strip().split('|'))
			if width!=length:
				print length,line

def save_excel(fpath,name,lists):
	workbook=xlwt.Workbook()
        sheet=workbook.add_sheet(name)
	for i,row in enumerate(lists): 
		for j,e in enumerate(row):
			element=e.decode('utf-8')
			sheet.write(i,j,element)
	workbook.save(fpath+'/'+name+'.xls')

def apply(fpath,dpath,func,args):
	data=loadData(fpath)
	data=func(data,args)
	saveData(data,dpath)

#data=loadData('/home/idanan/jiayuan/user_info.txt')
#male,female=departData(data)
#female=nummeric(female,[2,4,16])
#female=transform(female,MAPPY)
#saveData(female,'/home/idanan/jiayuan/transed_female.txt')

#data=loadData('/home/idanan/jiayuan/transed_female.txt')
#data=addColumn(data,[6,18])
#data=loadData('/home/idanan/jiayuan/transed_female.txt')
#data=appendBMI(data)
#data=loadData('/home/idanan/jiayuan/parsed_female2.txt')
#data=addColumn(data,[6,12])
#saveData(data,'/home/idanan/jiayuan/parsed_female3.txt')
#

#test('/home/idanan/jiayuan/parsed_female3.txt',26)
