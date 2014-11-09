#-*-encoding:utf-8 -*-
import numpy as np
import pandas as pd
from pdTransform import saveData
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA,FactorAnalysis
from sklearn.preprocessing import scale
import re

def matchDict(fpath):
	matches={}
	with open(fpath) as f:
		for line in f:
			li=line.strip().split(' ')
			if len(li)==3:
				matches[li[1]]=li[2]
			else:
				maches[li[1]]=0
	return matches

def concatData(female,male,matches):
	female['id']=female['id'].map(matches)
	data=pd.merge(male,female,on='id')
	return data

def factors(data,components,method='pca'):
	if method=='pca':
		pca=PCA(n_components=components).fit(data)
	if method=='factor':
		pca=FactorAnalysis(n_components=components,svd_method='randomized').fit(data)	
	return pca

def scaleData(data,filters):
	new_data=data.drop(labels=filters,axis=1)
	new_data=new_data.fillna(0).astype(float).values
	new_data=scale(new_data)
	return new_data

def kmeansModel(data,n_digits,initValue='k-means++'):
	def bench_k_means(estimator,data):
		estimator.fit(data)
		return estimator.labels_
	results=bench_k_means(KMeans(init=initValue,n_clusters=n_digits,n_init=10),data)
	return results


def decisionModel(data):
	pass


def main():
	header=re.sub(' |\t','','id|gender|age|height|edu|salary|nation|car|house|body|face|hair|\
	smoke|drink|child|parent|bmi|where2|where0|where1|\
	marriage0|marriage1|look0|look1').split('|')
	data=pd.read_csv('/home/idanan/jiayuan/code/pd_female1.txt',names=header,sep='|')
	new_data=scaleData(data,['id','gender'])
	pca=factors(new_data,18)
	print 'PCA explained variance:', sum(pca.explained_variance_ratio_)
	new_data=pca.transform(new_data)
	results=kmeansModel(new_data,6)
	data['cluster']=results
	saveData(data,'/home/idanan/jiayuan/code/cluster_female2.txt')

