# 相似性度量函数， 输入列向量, 归一化 0-1
from numpy import *
import numpy as np
from numpy import linalg as la

def ecludSim(inA, inB):
    '''
    基于欧式距离度量
    '''
    distance = la.norm(inA, inB)
    return 1.0 / (1.0 + distance)

def cosSim(inA, inB):
    '''
    基于余弦相似性度量
    '''
    sim = float(inA.T* inB) / la.norm(inA) * la.norm(inB)
    return 0.5 + 0.5 * sim

def svdMethod(dataMat, simMeas, user, item):
    '''
    输入：
        见recommend函数
    输出：
        Score(double): user对item的评分
    算法流程：
        1. for item_other in allItem
        2. if haveBeenScore(item_other)
        3.    compute_Simliar_Score(item, item_other)
        4. return Score
    '''
    N = shape(dataMat)[1]
    simTotal = 0.0
    ratSimTotal = 0.0
    U, Sigma, I_t = la.svd(dataMat)
    k = 0
    while sum(Sigma[:k]) < sum(Sigma) * 0.9:
        k = k+ 1
    SigK = getSigK(Sigma, k)
    itemFeature = dataMat.T * U[:,:k] * SigK.I
    for j in range(N):
        if dataMat[user,j] == 0 or j == item:
            continue
        sim = simMeas(itemFeature[item,:].T, itemFeature[j,:].T)
        # print("the similarity between {} and {} is {}".format(j,item, sim))
        ratSim = dataMat[user, j] * sim
        simTotal += sim
        ratSimTotal += ratSim
    if simTotal == 0:
        return 0
    return ratSimTotal / simTotal

def recommedCourse(dataMat, user, N=3, simMeas=cosSim, estMethod=svdMethod):
    '''
    输入：
        dataMat(mat)(M,N): 评分矩阵.
        use(int): 想推荐的用户id.
        N(int): 为用户推荐的未评分的商品个数
        simMeas(double): 两个特征向量的相似度评价函数
        estMethod(double)：推荐核心方法，计算商品对于用户的分数的函数
    输出：
        N * (item, 评分)： N个商品以及其的评分
    算法流程：
        1. 找到所有未评分的商品
        2. 若没有未评分商品，退出
        3. 遍历未评分商品.
        4. 计算用户可能对该商品的评分
        5. 排序取前N个输出.
    '''
    if estMethod is 'None':
        print("请给出推荐方法")
        return None
    unRatedItems = nonzero(dataMat[user,:] == 0)[1]
    if len(unRatedItems) == 0:
        print("没有未评分商品")
        return None
    item_and_score = []
    for item in unRatedItems:
        score = estMethod(dataMat, simMeas, user, item)
        item_and_score.append((item, score))
    return sorted(item_and_score, key=lambda k: k[1], reverse=True)[:N]

def recommedStudent(dataMat, user, N=3, simMeas=cosSim, estMethod=svdMethod):
    pass

def toBarJson(data, dict2id):
    """

    :param data: [(0, 5.0), (1, 5.0), (2, 5.0)]
    :return::
    {
        "source": [
            [2.3, "计算机视觉"],
            [1.1, "自然语言处理"],
            [2.4, "高等数学"],
            [3.1, "线性代数"],
            [4.7, "计算机网络"],
            [5.1, "离散数学"]
        ]
     }
    """
    jsonData = {"source":[]}
    for each in data:
        unit = [each[1], dict2id[each[0]]]
        jsonData['source'].append(unit)
    return jsonData