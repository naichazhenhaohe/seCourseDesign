# -*- coding: utf-8 -*-

"""
@author: kwonjiyong

对sthml文件预处理 获取页面的keyword/title/url以及主要的新闻内容并生成对应的txt文件 ,保存于target目录下

Step Two

"""

import os
from bs4 import BeautifulSoup as bs
import re


def getFileNames():
    #get shtml files
    filePath = '../docs/ori/'
    files = os.listdir(filePath)
    return files

#保存为txt文件
def saveFile(con,filePath):
    wFile = open(filePath, 'w', encoding='utf8')
    wFile.write('keywords: '+'/'.join(con[0])+'\r\n'+'title: '+''.join(con[1])+'\r\n'+'url: '+''.join(con[2])+'\r\n'+'content:\r\n'+con[3])
    wFile.close()
    
#清扫content
def sweep(content):
    #remove the title in the article
    content = re.sub(r'<p>　　原标题.*?</p>','',content)
    #remove <script></script>
    re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)
    content = re_script.sub('',content)
    #remove the author info
    content = re.sub(r'<p class="show_author">.*?</p>','',content)
    #remove label
    content = re.sub(r'<.*?>','',content)
    #remove '\n' and '\r\n'
    content = content.replace("\n","")
    content = content.replace("\r\n","")
    return content

#get the main content of the news
def getInfo(fileContent):
    res = []
    #keyword
    res.append(re.findall(r'<meta name="keywords" content="(.*?)" />', fileContent))
    #title
    res.append(re.findall(r'<meta property="og:title" content="(.*?)" />', fileContent))
    #url
    res.append(re.findall(r'<meta property="og:url" content="(.*?)" />', fileContent))
    return res

#convert into text file
def getProcessedFile():
    res = []
    files = getFileNames()
    for item in range(len(files)):
        #source file
        file = open('../docs/ori/'+files[item], 'r', encoding='utf8')
        fileContent = file.read()
        res = getInfo(fileContent)
        soup  = bs(fileContent,"html.parser")
        temp = str(soup.find(id='article'))
        res.append(sweep(temp))
        saveFile(res,'../docs/target/'+files[item][:-6]+'.txt')
        file.close()
        

getProcessedFile()







