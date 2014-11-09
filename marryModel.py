#-*-encoding:utf-8 -*-
import re
import numpy as np
import pandas as pd
from pdTransform import saveData
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA,FactorAnalysis
from sklearn.preprocessing import scale
from sklearn.tree import DecisionTreeClassifier as DecisionClassifier
from functools import partial
from sklearn.externals.six import StringIO
import pydot
from sklearn import tree


def matchDict(fpath):
	matches={}
	with open(fpath) as f:
		for line in f:
			li=line.strip().split(' ')
			if len(li)==3:
				matches[int(li[1])]=int(li[2])
			if len(li)==2:
				matches[int(li[1])]=0
	return matches

def match(x,matches):
	return matches.get(int(x),0)

def departData(dataSet,rate):
	trainLen=int(len(dataSet)*rate)
	trainData=dataSet[:trainLen]
	testData=dataSet[trainLen+1:]
	return trainData,testData


def concatData(female,male):
	data=pd.merge(male,female,on='id')
	return data

def scaleData(data,filters):
	new_data=data.drop(labels=filters,axis=1)
	new_data=new_data.fillna(0).astype(float).values
	new_data[:,:-1]=scale(new_data[:,:-1])
	return new_data

def test(classifier,testData):
	X=testData[:,:-1]
	Y=testData[:,-1]
	t=0.0
	for x,y in zip(X,Y):
		result=classifier.predict(x)
		if np.abs(result[0]-y)<0.5:
			t+=1
	true_rate=t/len(Y)
	return true_rate


def factors(data,components,method='pca'):
	if method=='pca':
		pca=PCA(n_components=components).fit(data)
	if method=='factor':
		pca=FactorAnalysis(n_components=components,svd_method='randomized').fit(data)	
	return pca

def kmeansModel(data,n_digits,initValue='k-means++'):
	def bench_k_means(estimator,data):
		estimator.fit(data)
		return estimator.labels_
	results=bench_k_means(KMeans(init=initValue,n_clusters=n_digits,n_init=10),data)
	return results


def decisionModel(data):
	X=data[:,:-1]
	Y=data[:,-1]
	classifier=DecisionClassifier()
	classifier=classifier.fit(X,Y)
	return classifier


def main():
	header=re.sub(' |\t','','id|gender|age|height|edu|salary|nation|car|house|body|face|hair|\
	smoke|drink|child|parent|bmi|where0|where1|\
	marriage0|marriage1|look0|look1|where2').split('|')
	data=pd.read_csv('/home/idanan/jiayuan/code/resources/transed_F.txt',names=header,sep='|')
	new_data=scaleData(data,['id','gender'])
	pca=factors(new_data,18)
	print 'PCA explained variance:', sum(pca.explained_variance_ratio_)
	new_data=pca.transform(new_data)
	results=kmeansModel(new_data,6)
	data['cluster']=results
	saveData(data,'/home/idanan/jiayuan/code/resources/cluster_female.txt')

def mainTree():
	header=re.sub(' |\t','','id|gender|age|height|edu|salary|nation|car|house|body|face|hair|\
	smoke|drink|child|parent|bmi|where0|where1|\
	marriage0|marriage1|look0|look1|where2').split('|')
	MaleData=pd.read_csv('/home/idanan/jiayuan/code/resources/transed_M.txt',names=header,sep='|')
	FemaleData=pd.read_csv('/home/idanan/jiayuan/code/resources/cluster_female.txt',names=header+['class'],sep='|')
	matches=matchDict('/home/idanan/jiayuan/code/resources/lovers_ids.txt')
	FemaleData['id']=FemaleData['id'].map(partial(match,matches=matches))
	FemaleClass=FemaleData[['id','class']]
	newMaleData=concatData(MaleData,FemaleClass)
	MaleArrays=scaleData(newMaleData,['id','gender'])
	pca=factors(MaleArrays[:,:-1],17)
	print 'PCA explained variance:', sum(pca.explained_variance_ratio_)
	pcaMaleArray=pca.transform(MaleArrays[:,:-1])
	MaleArrays=np.c_[pcaMaleArray,MaleArrays]


	trainData,testData=departData(MaleArrays,0.9)
	trainModel=decisionModel(trainData)

	dot_data = StringIO()
	tree.export_graphviz(trainModel, out_file=dot_data)
	graph = pydot.graph_from_dot_data(dot_data.getvalue())
	graph.write_pdf("/home/idanan/jiayuan/code/resources/marriage.pdf") 
	

	rate=test(trainModel,testData)
	print 'Decision Model true rate',rate

mainTree()




	
