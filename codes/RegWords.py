# -*- coding: utf-8 -*-
"""
@author: hankai liu & kwonjiyong

对新闻内容进行分词并去停用词

Step Three

"""

import jieba
import os

def getFileNames():
    filePath = '../docs/target/'
    files = os.listdir(filePath)
    return files

def saveSegfile(content,filepath):
    with open(filepath,'w') as f:
        f.write(content)

def writeURL(url):
    fp = open("../docs/urls.txt",'w',encoding='utf8')
    while url.count('\n') > 0:
        for i in url:
            if i == '\n':
                url.remove(i)
    res = ''.join(url)
    fp.write(res)
    fp.close()
    
def checkChinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def readFile():
    files = getFileNames()
    urls = []
    stopwords = [line.strip() for line in open('../docs/stopwordlist.txt','r',encoding='utf-8').readlines()]
    for file in files:
        filepath = '../docs/target/'+file
        afterfilepath = '../docs/segmented/' + file
        with open(filepath,'r',encoding='utf8') as fp:
            lines = fp.readlines()
            #windows
            url = lines[4]
            #linux
            #url = lines[2]
            urls.append(url[5:])
            content = lines[-1]
            content = jieba.cut(content)
            content2 = ""
            for item in content:
                if item.isdigit():
                    continue
                if item not in stopwords and item!='|' and checkChinese(item):
                    content2 = content2+item+' '
            #windows
            content2 = lines[0] + lines[2] + lines[4] + content2
            #liunx
            #content2 = lines[0] + lines[1] + lines[2] + content2
            saveSegfile(content2,afterfilepath)
    writeURL(urls)

readFile()