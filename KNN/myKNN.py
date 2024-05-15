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
import random


# 构建 KNN 分类器
# inX 用于接受分类的 NumPy 数组，dataSet 为训练样本集，labels 为对应标签，k 表示选择最近邻居的数目
def classify0(inX, dataSet, labels, k):
    """
    Classify data
    :param inX: ndarray, 分类数据
    :param dataSet: ndarray, 训练样本集
    :param labels: list, 样本集对应的标签
    :param k: 选择最近邻居的数目
    :return: 预测的标签
    """
    # numTestSamples = inX.shape[0]  # 获取分类集大小
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


# TODO: 距离权值优化
def f(x, a=1.0, b=1.0):
    return a / (x + b)


def classify1(inX, dataSet, labels, k):
    """
        分类器，使用距离权值优化，距离越近权值越大
        :param inX: ndarray, 分类数据
        :param dataSet: ndarray, 训练样本集
        :param labels: list, 样本集对应的标签
        :param k: 选择最近邻居的数目
        :return: 预测的标签
        """
    # numTestSamples = inX.shape[0]  # 获取分类集大小
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
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + f(distances[sortedDistIndicies[i]])
        # classCount 加上加权距离
    # 使用字典统计标签出现的频率
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    # 按照出现频率逆序排列，返回频率最高的类标签
    return sortedClassCount[0][0]

# 加载数据
def file2matrix(filename):
    """
    :param filename:
    :return: dataSet, labels, headers
    """
    with open(filename, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        data = list(csvreader)

        headers = data[0]
        data = data[1:]  # 去除数据的表头部分

        # dataSet = np.array(data[1:][:4])  # 创建 ndarray 对象存储特征值
        dataSet = np.array([row[:-1] for row in data], dtype=float)
        # 这里需要指定dtype，否则函数自动推断类型会有误
        labels = [row[-1] for row in data]
        # labels = list(data[1:][4])  # 创建存放标签的列表
        # headers = list(data[0][:4])  # 创建存放表头的列表

    return dataSet, labels, headers


# 数据预处理 MinMax归一化
def autoNorm(dataSet):
    minVals = dataSet.min(axis=0)  # 按列统计所有列的最小值
    maxVals = dataSet.max(axis=0)
    ranges = maxVals - minVals
    normDataSet = dataSet - minVals
    normDataSet /= ranges
    # 利用广播机制计算
    return normDataSet, minVals, ranges

# 数据集划分
def dataSetSplit(dataSet, labels, testRatio=0.2):
    """
    使用索引随机排序来重新排列 dataSet 和 labels，并划分数据集
    :param dataSet: ndarray, 包含所有样本的特征数据
    :param labels: list, 每个样本对应的标签
    :param testRatio:
    :return: xTrain, yTrain, xTest, yTest
    """
    dataSize = dataSet.shape[0]  # 获取数据集长度

    indices = list(range(dataSize))
    random.shuffle(indices)
    # 创建一个随机排列

    shuffledDataSet = dataSet[indices]
    shuffledLabels = [labels[i] for i in indices]
    # 随机排列 dataSet 和 labels

    numTest = int(dataSize * testRatio)
    xTest, yTest = shuffledDataSet[:numTest], shuffledLabels[:numTest]
    xTrain, yTrain = shuffledDataSet[numTest:], shuffledLabels[numTest:]
    # 划分训练集和测试集

    return xTrain, yTrain, xTest, yTest


# TODO 单次测试分类器

def Test0(dataSet, labels, testRatio=0.2):
    '''
    随机划分测试集和训练集，返回错误个数和错误率
    :param dataSet:
    :param labels:
    :param testRatio:
    :return: errorCount, errorRate
    '''
    xTrain, yTrain, xTest, yTest = dataSetSplit(dataSet, labels, testRatio)

    errorCount = 0
    for x, y in zip(xTest, yTest):
        yForecast = classify0(x, xTrain, yTrain, k)
        errorCount += yForecast != y
        # print("The classifier came back with %s, the real answer is: %s" % (yForecast, y))

    numTest = int(dataSet.shape[0] * testRatio)
    # print("numTest is", numTest)
    # print("The total error rate is: {:.2%}".format(errorCount / float(numTest)))
    # print("The total error number is:", errorCount)
    return errorCount, errorCount / float(numTest)


# TODO 单次测试分类器，加权距离优化
def Test1(dataSet, labels, testRatio=0.2):
    '''
    随机划分测试集和训练集，返回错误个数和错误率
    :param dataSet:
    :param labels:
    :param testRatio:
    :return: errorCount, errorRate
    '''
    xTrain, yTrain, xTest, yTest = dataSetSplit(dataSet, labels, testRatio)

    errorCount = 0
    for x, y in zip(xTest, yTest):
        yForecast = classify1(x, xTrain, yTrain, k)
        errorCount += yForecast != y
        # print("The classifier came back with %s, the real answer is: %s" % (yForecast, y))

    numTest = int(dataSet.shape[0] * testRatio)
    # print("numTest is", numTest)
    # print("The total error rate is: {:.2%}".format(errorCount / float(numTest)))
    # print("The total error number is:", errorCount)
    return errorCount, errorCount / float(numTest)

# TODO 测试加权优化分类器性能
def KNNTest1(filename, k, testRatio=0.2, testTimes = 10):
    """
    首先读入数据，进行标准化；
    然后进行10次随机划分测试，输出每次错误个数和错误率；
    最后输出总错误个数以及平均错误率；
    :param filename:
    :param k:
    :return:
    """

    print("\nTest the classifier performance on " + filename + " with optimization")
    print("parameter: k = {:}, test ratio = {:}".format(k, testRatio))

    dataSet, labels, headers = file2matrix(filename)
    normdataSet, minVals, ranges = autoNorm(dataSet)

    totalErrorCount = 0
    averageErrorRate = 0.0
    for _ in range(0, testTimes):
        errorCount, errorRate = Test1(normdataSet, labels, testRatio)

        # print("The {:}th error number is: {:}, error rate is: {:.2%}".format(_ + 1, errorCount, errorRate))

        totalErrorCount += errorCount
        averageErrorRate += errorRate / float(testTimes)

    print("The total error times is: ", totalErrorCount)
    print("The average error is: {:.2%}".format(averageErrorRate))

# 测试普通分类器性能
def KNNTest0(filename, k, testRatio=0.2, testTimes = 10):
    """
    首先读入数据，进行标准化；
    然后进行10次随机划分测试，输出每次错误个数和错误率；
    最后输出总错误个数以及平均错误率；
    :param filename:
    :param k:
    :return:
    """

    print("\nTest the classifier performance on " + filename + "with no optimization")
    print("parameter: k = {:}, test ratio = {:}".format(k, testRatio))

    dataSet, labels, headers = file2matrix(filename)
    normdataSet, minVals, ranges = autoNorm(dataSet)

    totalErrorCount = 0
    averageErrorRate = 0.0
    for _ in range(0, testTimes):
        errorCount, errorRate = Test0(normdataSet, labels, testRatio)

        # print("The {:}th error number is: {:}, error rate is: {:.2%}".format(_ + 1, errorCount, errorRate))

        totalErrorCount += errorCount
        averageErrorRate += errorRate / float(testTimes)

    print("The total error times is: ", totalErrorCount)
    print("The average error is: {:.2%}".format(averageErrorRate))

# TODO 加权距离优化分类器性能测试

# 应用分类器
def classifyFlowers(dataFile, forecastFile, k):
    """
    从CSV文件中读取10个鸢尾花的数据，预测并输出比较结果
    :param dataFile: 数据集文件
    :param forecastFile: 分类集文件，表头与dataFile相同
    :param k:
    :return: None
    """

    print("Applying classifier on", forecastFile)

    dataSet, labels, headers = file2matrix(dataFile)
    normdataSet, minVals, ranges = autoNorm(dataSet)

    # 读取分类集数据
    with open(forecastFile, newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)

        headers = data[0]
        data = data[1:]
        # 获取并去除表头

        flowers = np.array([row[:-1] for row in data], dtype=float)
        names = [row[-1] for row in data]

    flowers = (flowers - minVals) / ranges
    # 使用训练集参数，对测试集进行归一化

    # 进行预测
    for x, y in zip(flowers, names):
        flowerForecast = classify1(x, normdataSet, labels, k)
        print("The classifier came back with %s, the real flower is: %s" % (flowerForecast, y))


filename = 'iris.csv'
k = 3
testRatio = 0.2
testfilename = 'simulated_iris_data0.csv'

# 使用不同的 k 值测试普通分类器
# for k0 in range(1, 20, 2):
    # KNNTest0(filename, k0, testRatio)

# 使用不同的 k 值测试加权距离优化分类器
# for k1 in range(1, 20, 2):
    # KNNTest1(filename, k1, testRatio)

# 对比普通分类器以及优化分类器的性能
for k2 in range(1, 20, 2):
    KNNTest0(filename, k2, testRatio)
    KNNTest1(filename, k2, testRatio)

# 应用分类器分类
print("\nApplying classifier")
# classifyFlowers(filename, testfilename, k)
