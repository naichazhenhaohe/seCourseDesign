# -*- coding: utf-8 -*-
"""
@author: kwonjiyong

计算每篇文章中 tfidf值最高的20个词，并记录

Step Six
"""

import jieba
import jieba.analyse
import os


def writeFiles(top):
    lines = []
    wordList = []
    tfidfs = []
    for item in top:
        line = ''
        words = ''
        tfidf = ''
        for i in range(len(item)):
            line += item[i][0] + ' ' + str(item[i][1]) + ' ' 
            words += item[i][0] + ' '
            tfidf += str(item[i][1]) + ' '
        lines.append(line)
        wordList.append(words)
        tfidfs.append(tfidf)
    with open('../docs/tfidf/tfidf-words.txt','w') as wf:
        con = '\n'.join(lines)
        wf.write(con)
    with open('../docs/tfidf/words.txt','w') as wwf:
        con = '\n'.join(wordList)
        wwf.write(con)
    with open('../docs/tfidf/tfidf.txt','w') as twf:
        con = '\n'.join(tfidfs)
        twf.write(con)

def getTfidf():
    path = '../docs/segmented/'
    files = os.listdir(path)
    top = []
    for file in files:
        #windows
        with open(path+file, 'r', encoding='gbk') as f:
        #linux
#        with open(path+file, 'r', encoding='utf8') as f:
            content = f.readlines()[-1]
            top.append(jieba.analyse.extract_tags(content,topK=20,withWeight=True,allowPOS=(),withFlag=False))
    writeFiles(top)
    
getTfidf()