# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 10:41:43 2018

@author: kwonjiyong

网页去重
使用K-shingle算法
"""

def K_Shingle(str, kNum):
    resList = list()
    for i in range(len(str) - kNum + 1):
        s1 = str[i:i+kNum]
        resList.append(s1)
    return resList

def getSimilarity(str1, str2, kNum):
    s1 = K_Shingle(str1, kNum)
    s2 = K_Shingle(str2, kNum)
    num1 = set(s1) & set(s2)
    num2 = set(s1) | set(s2)
    res = 1.0*len(num1) / len(num2)
    return res;