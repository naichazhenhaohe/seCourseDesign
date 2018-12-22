# -*- coding: utf-8 -*-
"""
@author: kwonjiyong

网页去重 

因为在第三步时已经进行了分词，所以则直接利用已分词进行比较

Step Five
"""

import os

def getFileNames():
    filePath = '../docs/segmented/'
    files = os.listdir(filePath)
    return files

#delete the duplicate files
def deleteFile(filesToBeDeleted):
    for i in filesToBeDeleted:
        os.remove('../docs/segmented/'+i)

def compare():
    filesToBeDeleted = []
    fileNames = getFileNames()
    #用于帮助只和当前文件之后的文件比较
    count = -1
    for item in fileNames:
        count += 1
        #windows
        with open('../docs/segmented/'+item, 'r', encoding='gbk') as f:
        #linux
#        with open('../docs/segmented/'+item, 'r', encoding='utf8') as f:
            lines = f.readlines()
            currentWords = lines[-1].strip(' ').split(' ')
            for i in fileNames[count+1:]:
                #windows
                with open('../docs/segmented/'+i, 'r', encoding='gbk') as cFile:
                #linux
#                with open('../docs/segmented/'+i, 'r', encoding='utf8') as cFile:
                  cLines = cFile.readlines()
                  cWords = cLines = cLines[-1].strip(' ').split(' ')
                  res1 = set(currentWords) & set(cWords)
                  res2 = set(currentWords) | set(cWords)
                  res = 1.0 * len(res1) / len(res2)
                  #reocord the file name if the similarity is bigger than 0.9
                  if res > 0.9:
                      filesToBeDeleted.append(item)
                      print(item + '   ->   ' + i)
    print(filesToBeDeleted)
    deleteFile(filesToBeDeleted)


compare()














