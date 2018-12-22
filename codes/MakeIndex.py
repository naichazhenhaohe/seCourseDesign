import jieba.analyse
import re
def makeIndex(filepath):
    index = {}
    with open(filepath) as handle:
        for i,ln in enumerate(handle):
            for word in re.compile("\w+").findall(ln):
                index.setdefault(word,[]).append(i+1)#添加键、值
    return index

def indexQuery(index,*words):#可容纳多个变量组成的lis   ('台湾',)<class 'tuple'>元祖
    found = None#美国[4, 15, 19, 25, 33, 65, 67, 67, 67, 67, 67, 67]
    for word in words:
        got = index.get(word, [])
        if not got:#wordlist里面没有
            return None
        if not found:
            found = set(got)#转化为集合
        else:
            found &= set(got)#去重复元素
    return list(found)


def getLine(filepath, line_num):#获得指定行的内容
    if line_num<1:
        return ''
    for cur_line_num,line in enumerate(open(filepath,'r')):
        if (cur_line_num/2) == line_num-1: #/2的原因是读的两每行对应实际urls.txt的一个url
            return line
    return ''


def count_tfidf(locations,keywords):
    location_dic = {}
    for i,location in enumerate( locations):#循环关键词所在的每篇文档
        temp = 0
        word_line = getLine('D:/综合课设二/word_list.txt',location)#word_list.txt的地址
        words = word_line.split()
        for j,word in enumerate(words):#所在文章中的每个单词 0~19
            for top in keywords:
                if word == top[0]:
                    tf_idf_line = getLine("D:/综合课设二/word_list_tf.txt",location) #获取该篇文章20个词的tf行
                    tf_idf = tf_idf_line.split()
                    tf = float(tf_idf[j])*float(top[1]) #将word_list和keyword中的tf相乘后累加
                    temp = temp + tf
        location_dic[location] = temp
    return location_dic


def print_location(location_sort):
    i = 0
    print("共搜索到:"+str(len(location_sort))+"个结果:")
    for location in location_sort:
        url = getLine("D:/综合课设二/urls.txt",location)
        if(url!=""):
            i = i+1
            print(url)
    print(i)

#传入一个字典，返回一个一维list代表按tf-idf排序后的索引结果
def sortlocation(location_dic):
    sorted_location = {}
    for key,value in location_dic.items():
        if(value>0):
            sorted_location[key] = value
    after = sorted(sorted_location.values(),reverse=True)
    after_sort = []
    for i in after:
        for item in sorted_location.items():
            if i == item[1]:
                after_sort.append(item[0])
    return after_sort





word_list_path = 'D:\综合课设二\word_list.txt'
index = makeIndex(word_list_path)
userinput = input("请输入关键字:")
keywords = jieba.analyse.extract_tags(userinput,topK=5,withWeight=True,allowPOS=(),withFlag=False)
print(keywords)
locations = []

for top in keywords:#检索每个词获取文档下标
    location = indexQuery(index,top[0])# top[0] str
    print(location)
    if location!=None:
        locations.extend(location)
    else:
        print('对不起，您输入的关键词不在检索范围内!')

print("locations:")
print(locations)
location_dic = count_tfidf(locations,keywords)

print(location_dic)
# location_sort = sorted(location_dic.keys(),reverse=True)
# location_sort = sorted(location_dic.keys())
sortedlocation = sortlocation(location_dic)
# print(location_sort)
print_location(sortedlocation)
