# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 16:37:01 2017

@author: SKJ
"""

#ID3算法计算给定数据集的熵
from math import log
from imp import reload
import operator

def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet: #按行循环
        currentLabel = featVec[-1] #取遍每行最后一个值，即Label
        if currentLabel not in labelCounts.keys():  #如果当前的label字典中还没有
            labelCounts[currentLabel] = 0 #则先赋0创建
        labelCounts[currentLabel] += 1 #统计每类label的数量
    shannonEnt = 0.0
    for key in labelCounts:  #遍历每类label
        prob = float(labelCounts[key])/numEntries #各类label累加
        shannonEnt -= prob * log(prob,2) #ID3信息熵公式
    return shannonEnt

#鱼鉴定数据集    
def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    return dataSet, labels

#按照给定特征划分数据集
def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis] #存储该特征之前的特征
            reducedFeatVec.extend(featVec[axis+1:]) #存储该特征之后的特征
            retDataSet.append(reducedFeatVec)
    return retDataSet


#选择最好的数据集划分方式
def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]#创建唯一的分类标签列表
        uniqueVals = set(featList)
        newEntropy = 0.0
        for value in uniqueVals: #计算每种分类的信息熵
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if (infoGain > bestInfoGain):  #计算最好的信息增益
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys(): 
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.items(),\
                              key = operator.itemgetter(1), reverse = True)
    return sortedClassCount[0][0]

#创建树的函数代码
def creatTree(dataSet,labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = creatTree(splitDataSet\
              (dataSet,bestFeat,value),subLabels)
    return myTree




