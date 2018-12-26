# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 00:14:26 2018

@author: kwonjiyong

将每个文章的最总要的20个词及其所在文档名及其tfidf存入数据库

Step Eight
"""

import pymysql as mdb

def store():
    filePath = '../docs/tfidf/tfidf-words.txt'
    db = mdb.connect('localhost', 'root', 'Wang4250', 'se')
    cursor = db.cursor()
    
    with open(filePath, 'r', encoding='utf8') as f:
        count = 0
        flag = 0
        filename = ''
#        lens = []
#        sum = 0
        for line in f:
            flag += 1
            count += 1
            if count == 1:
                filename = line[:-1]
            if count == 2:
                count = 0
                wordsInfo = line[:-1]
                wordsInfo = wordsInfo.split(' ')
                while '' in wordsInfo:
                    wordsInfo.remove('')
                for i in range(len(wordsInfo) / 2):
                    sql = 'INSERT INTO tfidf (`filename`, `word`, `tfidf`) VALUES (\'%s\',\'%s\',\'%s\');' % (filename, wordsInfo[i*2], wordsInfo[i*2+1])
                    try:
                        cursor.execute(sql)
                        db.commit()
                    except:
                        db.rollback()
                        print('insert error')
#                lens.append(len(wordsInfo))
#        print(set(lens))
#                if len(wordsInfo) == 41:
#                    sum+=1
#        print(sum)
    db.close()
    
    
store()










