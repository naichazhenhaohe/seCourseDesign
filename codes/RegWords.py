# -*- coding: utf-8 -*-
"""
@author: hankai liu

对新闻内容进行分词并去停用词

3
"""

import jieba
import os
import re

def getFileNames():
    filePath = '../docs/target/'
    files = os.listdir(filePath)
    return files

def saveSegfile(content,filepath):
    with open(filepath,'wb') as f:
        f.write(content)

def writeURL(url):
    fp = open("../docs/urls.txt",'a+')
    fp.write(url)
    
def checkChinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def readFile():
    files = getFileNames()
    stopwords = [line.strip() for line in open('../docs/stopwordlist.txt','r',encoding='utf-8').readlines()]
    for file in files:
        filepath = '../docs/target/'+file
        afterfilepath = '../docs/segmented/' + file
        with open(filepath,'rb') as fp:
            keywords = fp.readline()
            url = fp.readline()
            writeURL(url.decode(encoding='utf-8'))
            title = fp.readline()
            content = fp.read()
            content = content.replace("\n".encode(),"".encode())
            content = content.replace("\r\n".encode(),"".encode())
            content = content.replace("content: \r\r\r".encode(),"".encode())
            content = content.replace("\r".encode(),"".encode())
            content = content.replace("content".encode(), "".encode())
            content = jieba.cut(content)
#            content = re.sub(r'[0-9a-zA-Z]','',content.decode())
#            content = re.sub(r' +', ' ', content)
            content2 = ""
            for item in content:
                if item.isdigit():
                    continue
                if item not in stopwords and item!='|' and checkChinese(item):
                    content2 = content2+item+' '
            content2 = content2.encode()
            content2 = keywords+url+title+content2
            saveSegfile(content2,afterfilepath)

readFile()