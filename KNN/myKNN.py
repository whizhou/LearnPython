# KNN 实现鸢尾花数据分类
# 功能包括：加载数据，KNN算法实现，数据归一化，数据集划分，测试分类器性能，应用分类器
# 随机取 20% 数据用于测试，另外 80% 用于训练
# 自己设计 10 个 鸢尾花数据进行分类
# 从 CSV 文件中读入数据
# 数据包括四个特征：sepal_length, sepal_width, petal_length, petal_width
# 和一个标签：species

import csv
import numpy as np
import operator


# TODO: 构建 KNN 分类器
# inX 用于接受分类的 NumPy 数组，dataSet 为训练样本集，labels 为对应标签，k 表示选择最近邻居的数目
def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]  # 获取样本数量
    diffMat = np.tile(inX, (dataSetSize, 1)) - dataSet
    # 手动扩展分类集以匹配样本集
    sqDiffMat = diffMat ** 2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances ** .5
    # 计算距离
    sortedDistIndicies = distances.argsort()
    # argsort() 返回将数组值升序排序后的索引值
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    # 使用字典统计标签出现的频率
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    # 按照出现频率逆序排列，返回频率最高的类标签
    return sortedClassCount[0][0]


# TODO: 加载数据
def file2matrix(filename):
    with open(filename, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        dataSet = np.array(csvreader[1:, 0:3])  # 创建 ndarray 对象存储特征值
        labels = list(csvreader[1:, 4])  # 创建存放标签的列表
        headers = list(csvreader[0, 0:4])  # 创建存放表头的列表

    return dataSet, labels, headers


# TODO: 数据预处理 MinMax归一化
def autoNorm(dataSet):
    minVals = dataSet.min(axis=0)  # 按列统计所有列的最小值
    maxVals = dataSet.max(axis=0)
    ranges = maxVals - minVals
    normDataSet = dataSet - minVals
    normDataSet /= ranges
    return normDataSet, ranges, minVals, maxVals

# TODO: 数据集划分

