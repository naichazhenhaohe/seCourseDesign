# -*- coding: utf-8 -*-
"""
@author: kwonjiyong

将文件信息存入数据库

Step Seven
"""

import os
import pymysql as mdb

#获取分好词的文件的文件名
def getFileNames():
    filePath = '../docs/segmented/'
    files = os.listdir(filePath)
    return files    

#将文件的名称和文件的来源网页地址以元组和列表的形式记录
def getFileInfo():
    res = []
    files = getFileNames()
    for file in files:
        with open('../docs/segmented/'+file, 'r', encoding='utf-8') as f:
            temp = (file, f.readlines()[2][5:-1])
            res.append(temp)
    return res

#将文件的名称和来源网址存入数据库
def store():
    res = getFileInfo()
    db = mdb.connect('localhost', 'root', 'Wang4250', 'se')
    cursor = db.cursor()
    for i in res:
      sql = 'INSERT INTO files (`name`, `url`) VALUES (\'%s\',\'%s\');' % (i[0], i[1])
      try:
        cursor.execute(sql)
        db.commit()
      except:
          db.rollback()
          print('insert error!')  
    db.close()

store()