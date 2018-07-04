# coding: utf-8


from bson.objectid import ObjectId
import re
from pymongo import MongoClient
import pprint
import pymongo

from pandas import Series,DataFrame
import pandas as pd

from Answer import BitastPerson 



def get_db(db_name):
    #setup
    client = MongoClient("localhost",27017)
    db=client[db_name]
    return db

def get_collection(db,collection_name):
    coll=db[collection_name]
    return coll

db=get_db("biask")
collect=get_collection(db,"answers_region")
ask=get_collection(db,"ask_region")


#按日期统计问题数"date_time":"2018-06-06"
'''
a=ask.find({})
list=[]
for i in a :
    b=i["date_time"]
    if list == []:
        list.append(b)
        dict[b]=1
    elif b not in list:
        list.append(b)
        dict[b]=1
    else :
        dict[b]+=1
print (dict)
   '''      
    



def person_stats(name):
#赞数统计#

    a=BitastPerson(name,collect)

    b=a.get_answers_voters(name,collect)
    c=0
    for i in b:
        for key,value in i.items():
            c+=value
    #print("被赞数(总)",c)   #总被赞数
    #print (b)


    #总回答数get_contents_num

    d=a.get_contents_num(name,collect)
    print("被赞数(总)",c)
    print ("回答问题数",d)
    #文章排序
    e=a.get_contents_wordcount(name,collect)

    #总字数

    e=e[0][name]
    print ("回答总字数",e) 

    #平均字数
    f=int(e/d)
    print ("回答平均字数",f)

    #平均获赞数
    g=c/d
    print("每个回答平均获赞数",g)

    h={}
    for i in b:
        for key,value in i.items():
            h[key]=value
    #print (d)

    i=Series(h)
    iobj=i.sort_values(ascending=False)
    print (iobj)

def all_voters(name):
#赞数统计#

    a=BitastPerson(name,collect)

    b=a.get_answers_voters(name,collect)
    c=0
    h={}
    for i in b:
        for key,value in i.items():
            c+=value
            h[key]=value
    #print("被赞数(总)",c)   #总被赞数
    #print (b)


    #总回答数get_contents_num

    d=a.get_contents_num(name,collect)
    print("被赞数(总)",c)
    print ("回答问题数",d)
    #文章排序
    #e=a.get_contents_wordcount(name,collect)

    #总字数

    #e=e[0]
    #print ("回答总字数",e) 

    #平均字数
    #f=int(e/d)
    #print ("回答平均字数",f)

    #平均获赞数
    g=c/d
    print("每个回答平均获赞数",g)

    print (h)
    return h
'''
    h={}
    for i in b:
        for key,value in i.items():
            h[key]=value
    #print (d)

    i=Series(h)
    iobj=i.sort_values(ascending=False)
    print (iobj)
'''







h=all_voters("all")
db=get_db("biask")
coll=get_collection(db,"name_voter_dict")

coll.insert_one(h)
'''
#list=['风青萍','liaobtc','狼三','旧童','karma','变色龙','成天乐','七叔之家',"有问必答","Tracy","smallgrass","猴子哥","橡皮擦","币圈行者","虫二呐","区链茶社","Yuanyyy","提提卡卡","一字千金","太毛顾问","小三爷","Louiy","矿圈韬哥","jubi","WeiDeng556","何立币圈","zhm123","DK","jqrtvb","bobdos","mlhdy01","卡洛孙","一枚小花马甲","半步江南","小玖不爱喝可乐","Wolkin","didiaoleiren","梦枕天下","杰罗姆","单边酒窝儿"]
list=["scisan","梦枕天下","蒙特卡洛","lancy","佩佩"]
flag=1
for i in list:
    print(i)#("威望排名第"+str(flag)+":"+i)
    person_stats(i)
    print("==========================================================================================")
    print(" ")
    flag+=1
'''    









