# -*- coding: utf-8 -*-
"""
@author: kwonjiyong

清扫无内容的文件，针对网页丢失的新闻

Step Four
"""

import os

def getFileNames():
    #get shtml files
    filePath = '../docs/segmented/'
    files = os.listdir(filePath)
    return files

def clean():
    filePaths = getFileNames()
    for item in filePaths:
        with open('../docs/segmented/'+item, 'r', encoding='gbk') as f :
            lines = f.readlines()
            if len(lines) == 3 and len(lines[0]) == 11:
                os.remove('../docs/segmented/'+item)
 
clean()