#-*-encoding:utf-8-*-


PATH='/home/idanan/jiayuan/user_infos.txt'
FILTERS=[5]
mappy={'中专或相当学历':1,'大专':2,'本科':3,'硕士':4,'双学士':5,'博士':6,'博士后':7,'未填':0}
def loadData(path):
	infos=[]
	with open(path) as f:
		for line in f:
			info=line.strip().split(' |')
			infos.append(info)
	return infos

def mapping(x):
	if x in mappy.keys():
		return mappy[x]
	else:
		return x

def departInfo(info,filters):
	info1=[info[i] for i in filters]
	info2=[info[i] for i  in range(23) if i not in FILTERS]
	return [info1,info2]

def transform(data):
	new_data=[]
	for info in data:
		if info[1]=='女':
			info1,info2=departInfo(info,FILTERS)
			new_info=info2+map(mapping,info1)
			new_data.append(new_info)
	return new_data


def saveData(data,path):
	with open(path,'w') as f:
		for line in data:
			s=[str(i) for i in line]
			f.write(' |'.join(s)+'\n')


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

			

data=loadData(PATH)
data=transform(data)
saveData(data,'/home/idanan/test.txt')

			
