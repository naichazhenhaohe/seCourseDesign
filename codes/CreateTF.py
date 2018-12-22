# -*- coding: utf-8 -*-
'''
@author hankai liu

计算tf 存于tfidfList.txt
并记录每篇文章中出现的频率最高的20个词 存于wordList.txt
'''

import jieba
import jieba.analyse
import os


def write_word_list_file(s, filepath):    # 将分词写入文件，一个网页对应一行
    fp = open(filepath, "a+")
    fp.writelines(str(s)+' ')

def write_line():
    fp = open("../docs/wordList.txt", "a+")
    fp_tf = open('../docs/tfidfList.txt', "a+")
    fp.writelines('\n')
    fp_tf.writelines('\n')

path = '../docs/segmented/'
files = os.listdir(path)
for file in files:
    name = file.title()
    fp = open(path+file,'r',encoding='utf-8')
    con = fp.readlines()
    content = con[-1]
    sentence = name[:-4] + content
    topk = jieba.analyse.extract_tags(sentence,topK=20,withWeight=True,allowPOS=(),withFlag=False)
    for top in topk:#将分词和tf-idf分别存入两个文件
        write_word_list_file(top[0],'../docs/wordList.txt')
        write_word_list_file(top[1],'../docs/tfidfList.txt')
    write_line()
