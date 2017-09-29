# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 15:44:26 2017

@author: SKJ
"""

from numpy import *
from os import listdir
import operator
import sys
import kNN


#定义输出结果
def creatDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group,lables

#kNN算法
def classify0(intX,dataSet,labels,k):#输入向量，训练样本集，标签，近邻数目
    dataSetSize = dataSet.shape[0]#shape[0]表示求矩阵行数
    #距离计算
    diffMat = tile(intX,(dataSetSize,1)) - dataSet#tile在行的方向上重复intX  dataSetSize次，列方向上1次
    sqDiffmat = diffMat**2
    sqDistances = sqDiffmat.sum(axis=1)
    distances = sqDistances**0.5
    
    sortedDistIndicies = distances.argsort()#对计算出的距离从小到大排序
    classCount={}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1 #选择距离最小的k个点
    sortedClassCount = sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)#itemgetter方法，按第二个元素次序排序
    return sortedClassCount[0][0]    #返回发生频率最高的元素标签

#文本转换
def file2matrix(filename):
    fr = open(filename)
    arrayOLines = fr.readlines()#读取行数 存在数组中 其中 导入后每行中用\t隔开 两行之间用\n换行
    numberOfLines = len(arrayOLines)
    returnMat = zeros((numberOfLines,3))
    classLabelVector = []
    index = 0
    for line in arrayOLines:
        line = line.strip()#删除回车符
        listFromLine = line.split('\t')#识别到\t的地方就切片
        returnMat[index,:] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))#列表最后一列
        index += 1
    return  returnMat,classLabelVector  

#原始数据归一化newValue=(oldValue-min)/(max-min)
def autoNorm(dataSet):
    minVals = dataSet.min(0)#每列最小值
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataset = zeros(shape(dataSet))#shape求dataSet的维数
    m = dataSet.shape[0]#计算dataSet的行数
    normDataSet = dataSet - tile(minVals,(m,1))#tile重复m行
    normDataSet = normDataSet/tile(ranges,(m,1))
    return normDataSet,ranges,minVals

#分类器针对约会网站的测试代码
def datingClassTest():
    #选取10%的数据测试分类器
    hoRatio = 0.10
    #原始文本转换
    datingDataMat,datingLabels = kNN.file2matrix('datingTestSet2.txt')
    #归一化
    normMat,ranges,minVals = autoNorm(datingDataMat)
    #设置测试个数
    m = normMat.shape[0]
    numTestVecs = int(m*hoRatio)
    
    errorCount = 0.0
    for i in range(numTestVecs):
        #分类算法
        classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],\
                                     datingLabels[numTestVecs:m],3)
        print ("the classifier came back with: %d, the real answer is: %d"\
                % (classifierResult , datingLabels[i]))
        if (classifierResult != datingLabels[i]): 
            errorCount += 1.0
    print ("the total error rate is:%f" % (errorCount/float(numTestVecs)))
    #print errorCount
    
    
#原始图像已经处理成黑白32*32像素10的矩阵
#先把矩阵格式化转换为1*1024的向量
def img2vector(filename):
    returnVect = zeros((1,1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):#循环读出文件前32行
            returnVect[0,32*i+j] = int(lineStr[j])#将32*32矩阵转成1*1024的向量
    return returnVect

def handwritingClassTest():
    hwLabels = []
    trainingFileList = listdir('trainingDigits')#获取文件目录列表
    m = len(trainingFileList)
    trainingMat = zeros((m,1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]#对文件名进行处理，如原文件名为9_45.txt
        classNumStr = int(fileStr.split('_')[0])#提取出数字1,2,3.....
        hwLabels.append(classNumStr)
        trainingMat[i,:] = img2vector(r'trainingDigits\%s' % fileNameStr)
    testFileList = listdir('testDigits')
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2vector(r'testDigits\%s' % fileNameStr)
        classifierResult = classify0(vectorUnderTest,trainingMat,hwLabels,3)
        print("the classifier came back with: %d, thereal answer is: %d"\
              % (classifierResult,classNumStr))
        if (classifierResult!=classNumStr):
            errorCount += 1.0
    print("\nthe total number of errors is: %d" % errorCount)
    print("\nthe total rate is: %f" % (errorCount/float(mTest)))
        


