import pandas as pd
from sklearn import svm
from numpy import *
from sklearn import tree
import random
import time 

def time_cost(func):
    def inner(arg):
        start=time.time()
        func(arg)
        end=time.time()
        print func.__name__,end-start
    return inner

#load data set from excel,according to excel file path,excel'sheet name,and the column names
def loadData(excelfile,sheet,labels):
    xl=pd.ExcelFile(excelfile)
    dataSet=xl.parse(sheet)
    dataSet=dataSet[labels]
    return dataSet


#subject to train rate,get the train data set,test data set  
def departData(dataSet,rate):
    trainLen=int(len(dataSet)*rate)
    trainData=dataSet[:trainLen]
    testData=dataSet[trainLen+1:]
    return trainData,testData


#separate data by Y value's label.
def classifyData(dataSet,ylabel,value):
    labelData=dataSet[dataSet[ylabel]==value]
    nolabelData=dataSet[dataSet[ylabel]!=value]
    return labelData,nolabelData

def banlance(dataSet,ylabel,yValue,rate):
    labelSet=dataSet[dataSet[ylabel]==yValue]
    nolabelSet=dataSet[dataSet[ylabel]!=yValue]
    a=int(len(labelSet)*rate)
    nolabel=nolabelSet.ix[random.sample(nolabelSet.index,a)]
    banlancedSet=pd.concat([labelSet,nolabel])
    return banlancedSet
    
#test classify function
def test(classify,dataSet,labels):
    X=dataSet[labels[:-1]].values
    Y=dataSet[labels[-1]].values 
    error=0.0
    for test_x,test_y in zip(X,Y):
        result=classify.predict(test_x)
        if round(result)!=test_y:
            error+=1
    error_rate=error/len(Y)
    return error_rate


#sample weights svm
def clf_weight(dataSet,labels,yValue,weight):
    labelData,nolabelData=classifyData(dataSet,labels[-1],yValue)
    dataSet=pd.concat([labelData,nolabelData])
    a=len(labelData)
    b=len(dataSet)
    sample_weights=ones(b)
    sample_weights[:a-1]*=weight
    X=dataSet[labels[:-1]].values
    Y=dataSet[labels[-1]].values
    clf_weights=svm.SVC().fit(X, Y,sample_weight=sample_weights)
    return clf_weights

def clf_svm(dataSet,labels):
    X=dataSet[labels[:-1]].values
    Y=dataSet[labels[-1]].values
    clf=svm.SVC().fit(X,Y)
    return clf

def decisionTree(dataSet,labels):
    X=dataSet[labels[:-1]].values
    Y=dataSet[labels[-1]].values
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X, Y)
    return clf
    

@time_cost
def svmWeightClassify(excel):
    dataSet=loadData(*excel)
    labels=excel[-1]
    ylabel=labels[-1]
    trainSet,testSet=departData(dataSet,0.8)
    clf=clf_weight(trainSet,labels,1,150)
    error_rate=test(clf,testSet[testSet[ylabel]==1],labels)
    error_rate2=test(clf,testSet,labels)
    print ' clf_svmWeight: classified to be 0 while y=1 :',error_rate,' total error:',error_rate2

@time_cost
def svmClassify(excel):
    dataSet=loadData(*excel)
    labels=excel[-1]
    ylabel=labels[-1]
    trainSet,testSet=departData(dataSet,0.8)
    banlancedTrain=banlance(trainSet,ylabel,1,1)
    clf=clf_svm(banlancedTrain,labels)
    error_rate=test(clf,testSet[testSet[ylabel]==1],labels)
    error_rate2=test(clf,testSet,labels)
    print ' clf_svm: classified to be 0 while y=1 :',error_rate,' total error:',error_rate2
   

@time_cost
def treeClassify(excel):
    dataSet=loadData(*excel)
    labels=excel[-1]
    ylabel=labels[-1]
    trainSet,testSet=departData(dataSet,0.8)
    banlancedTrain=banlance(trainSet,ylabel,1,2.4)
    clf=decisionTree(banlancedTrain,labels)
    error_rate=test(clf,testSet[testSet[ylabel]==1],labels)
    error_rate2=test(clf,testSet,labels)
    print ' Decision : classified to be 0 while y=1 :',error_rate,' total error:',error_rate2


treeClassify(['/home/wenter/test.xls','sheet1',['ROA','TLTA','WCTA','MB','AT','RETA','default']])
svmClassify(['/home/wenter/test.xls','sheet1',['ROA','TLTA','WCTA','MB','AT','RETA','default']])
svmWeightClassify(['/home/wenter/test.xls','sheet1',['ROA','TLTA','WCTA','MB','AT','RETA','default']])

