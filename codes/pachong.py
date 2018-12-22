# -*- coding: utf-8 -*-

'''
@author: hankai liu

爬取新浪新闻

Step One

'''
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import re
import os

import urllib.request

def getHTML(htmlurl):
    html = urllib.request.urlopen(htmlurl).read()
    return html
def saveHTML(file_name,file_content):
    with open(file_name,'wb') as f:
        f.write(file_content)


newsurl = "http://news.sina.com.cn/c/nd/2018-06-08/doc-ihcscwxa1809510.shtml"
commenturl = "http://comment5.news.sina.com.cn/page/info?version=1&format=json&channel=gn&newsid=comos-{}&group=undefined&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=3&t_size=3&h_size=3&thread=1"
def getcommentcounts(newsurl):
    m = re.compile('doc-i(.*?).shtml').findall(newsurl) #m hcscwxa1809510 list
    newsid = m[0] #hcscwxa1809510
    comments = requests.get(commenturl.format(newsid))#requests.get()方法请求了站点的网址,然后打印出了返回结果的类型,状态码,编码方式,Cookies等内容
    jd = json.loads(comments.text) #将json类型的数据转化为字典类型
    return jd['result']['count']['total']

def getnewsdetail(newsurl):
    result = {}
    res = requests.get(newsurl)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    try:
        result['title'] = soup.select('.main-title')[0].text
        timesource = soup.select('.date-source span')[0].text
        result['time'] = datetime.strptime(timesource, '%Y年%m月%d日 %H:%M').strftime('%Y-%m-%d')
        result['place'] = soup.select('.source')[0].text  # 新闻来源
        article = []
        for p in soup.select('#article p')[:-1]:  # 去除一行最后一个字符（换行符）
            article.append(p.text.strip())  # 去除空格
        articleall = ''.join(article)  # 将一维list转化为str字符串
        result['article'] = articleall
        result['editor'] = soup.select('#article p')[-1].text.strip()
        result['comments'] = getcommentcounts(newsurl)
    except:
        print("出现异常!")
    return result

# 存储一个网页上的所有url
urlslist = []
url='http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page={}&callback=newsloadercallback&_=1528548757769'
def parseListLinks(url):
    res=requests.get(url)
    jd=json.loads(res.text.lstrip('  newsloadercallback(').rstrip(');'))
    for ent in jd['result']['data']:
        print(ent['url'])
        # ent['url']网页的url  downloadurl保存到本地的地址
        lasturl = ent['url'].replace('/', '_')
        relasturl = ''.join(re.findall(r'([1-2].*?\.shtml)',lasturl))
        #存到上级目录下的docs/ori目录中
        downloadurl = os.path.abspath(os.path.join(os.getcwd(), ".."))+"/docs/ori/"+relasturl
        html = getHTML(ent['url'])
        saveHTML(downloadurl,html)
        urlslist.append(ent['url'])
        # newsdetail.append(getnewsdetail(ent['url']))
    # return newsdetail

news_total =[]

for i in range(1,3000):#控制爬取网页的深度
    newsurl = url.format(i)
    newsary = parseListLinks(newsurl)
    news_total.append(newsary)
