#-*-encoding:utf-8-*-

from pdTransform import loadData,saveData
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt

def departData(data,colName):
	allData=[]
	for value in data[colName].unique():
		siData=data[data[colName]==value]
		allData.append(siData)
	return allData

def descData(data,cols):
	description=np.zeros((6,len(cols)))
	for i,col in enumerate(cols):
		description[:,i]=data[col].describe().values[1:7]
	descData=pd.DataFrame(description,columns=cols)
	return descData

def compareData(datalist,cols):
	description=np.zeros((len(datalist),len(cols)))
	indexs=[]
	for i,data in enumerate(datalist):
		name=data['cluster'].values[1]
		indexs.append(name)
		for j,col in enumerate(cols):
			description[i,j]=data[col].describe().values[1]

	descData=pd.DataFrame(description,columns=cols,index=indexs)
	return descData







	
	
	
header=re.sub(' |\t','','id|gender|age|height|edu|salary|car|house|body|hair|\
		        smoke|drink|child|bmi|where0|where1|\
			        marriage0|marriage1|where2|cluster').split('|')

data=loadData('/home/idanan/jiayuan/code/resources/cluster_female.txt',header)
descs=descData(data,header[2:-1])
saveData(descs,'/home/idanan/jiayuan/code/resources/female_desc.txt',True)
allData=departData(data,'cluster')
for cluster in allData:
	name=cluster['cluster'].values[0]
	description=descData(cluster,header[2:-1])
	saveData(description,'/home/idanan/jiayuan/code/resources/cluster_%d.txt'%name,True)


descs=compareData(allData,header[2:-1])
print descs
descs.sort_index().T.plot(kind='bar')
plt.show()
saveData(descs,'/home/idanan/jiayuan/code/resources/female_compare.txt',True)
