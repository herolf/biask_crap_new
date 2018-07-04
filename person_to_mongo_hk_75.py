from pymongo import MongoClient
from bson.objectid import ObjectId
import requests
import re
from bs4 import BeautifulSoup
from bs4 import NavigableString
from bs4 import Tag
import pprint
import pymongo
import json

from pandas import Series,DataFrame
import pandas as pd

from Answer import BitastPerson 

#from 607bitask_zip import get_question_askregion
#from 607bitask_zip import get_answers_region

def get_db(db_name):
    #setup
    client = MongoClient("localhost",27017)
    db=client[db_name]
    return db

def get_collection(db,collection_name):
    coll=db[collection_name]
    return coll


def getHtml(url):
    try:
        html = requests.get(url)
        bsObj = BeautifulSoup(html.text,'lxml')
        Html = bsObj
    except AttributeError as e:
        return None
    return Html

def person_stats(name,collect):
#赞数统计#
    dict={}
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
    e=0
    e=a.get_contents_wordcount(name,collect)
    #总字数
    if  type(e) == list and e != [] :
        print(type(e))
        print(e)
        e=e[0][name]
        print ("回答总字数",e) 
        dict["回答总字数"]=e
    #平均字数
        f=int(e/d)
        print ("回答平均字数",f)
        dict["回答平均字数"]=f
    #平均获赞数
        g=c/d
        print("每个回答平均获赞数",g)
        dict["每个回答平均获赞数"]=g
        h={}
        for i in b:
            for key,value in i.items():
                h[key]=value
    #lobj=a.sort_dict(h)//列表中包着字典，mongdb中难以引导
    #print (d)
    #i=Series(h)
    #iobj=i.sort_values(ascending=False)
    #print (iobj)
        dict["点赞人排名"]=h
    else :
        dict["回答总字数"]=0
        dict["回答平均字数"]=0
        dict["每个回答平均获赞数"]=0
        dict["点赞人排名"]=0

    return dict


def person_collect_to_mongo (person_name,voter_count):
    print("===============",person_name)
    db=get_db("biask")
    coll=get_collection(db,"answers_region")

    person_coll=get_collection(db,"person_region")


    dict={}
    url="https://www.biask.com/people/"+person_name

    print (url)

    html=getHtml(url)
    dict_q_to_person_page=person_stats(person_name,coll)

    #div.meta:nth-child(1) > span:nth-child(1) > em:nth-child(2)   div.meta:nth-child(1) > span:nth-child(2) > em:nth-child(2)     div.meta:nth-child(1) > span:nth-child(3) > em:nth-child(2)   div.meta:nth-child(1) > span:nth-child(4) > em:nth-child(2)
    person_head=html.select("div.meta > span > em ")
    if person_head != [] and person_head != None:
        person_prestige=person_head[0].text
        person_agree = person_head[1].text
        person_energe = person_head[2].text
        person_temp = person_head[3].text
        ma = re.match(r'\d+',person_temp)
        person_yoyow=ma.group() 
        print (person_prestige,"  ",person_agree,"  ", person_energe, "   ",person_yoyow)
    else:
        person_prestige=None
        person_agree =  None
        person_energe = None
        person_temp =   None
        #ma = re.match(r'\d+',person_temp)
        person_yoyow=   None 

    ##page_articles > span
    if html.select("#page_questions > span") !=[] and html.select("#page_questions > span") != None:
        person_ask=html.select("#page_questions > span")[0].text
    else:
        person_ask=     None
    if html.select("#page_answers > span")  != [] and html.select("#page_answers > span") !=None:
        person_answer=html.select("#page_answers > span")[0].text
    else:
        person_answer=  None
    if html.select("#page_articles > span") !=[] and html.select("#page_articles > span") != None:
        person_articles=html.select("#page_articles > span")[0].text
    else:
        person_articles=None
    if html.select("body > div.aw-container-wrap > div > div > div > \
    div.col-sm-12.col-md-3.aw-side-bar > div > div > span > em") !=[] and html.select("body > div.aw-container-wrap > div > div > div > \
    div.col-sm-12.col-md-3.aw-side-bar > div > div > span > em") !=None :
        person_follow=html.select("body > div.aw-container-wrap > div > div > div > div.col-sm-12.col-md-3.aw-side-bar > div > div > span > em")[0].text
    else:
        person_follow=  None
    if html.select("body > div.aw-container-wrap >\
    div > div > div > div.col-sm-12.col-md-3.aw-side-bar > div > div > span > em") !=[] and html.select("body > div.aw-container-wrap >\
    div > div > div > div.col-sm-12.col-md-3.aw-side-bar > div > div > span > em") !=None:
        person_follow_by=html.select("body > div.aw-container-wrap > div > div > div > div.col-sm-12.col-md-3.aw-side-bar > div > div > span > em")[1].text
    else:
        person_follow_by=None
    if html.select("#overview > div > div.mod-body > ul > li > p > span") !=[] and html.select("#overview > div > div.mod-body > ul > li > p > span") != None:
        person_last_answer=html.select("#overview > div > div.mod-body > ul > li > p > span")[0].text
    else :
        person_last_answer = None
    print(person_last_answer)
    print (person_ask, person_answer,person_articles, person_follow,person_follow_by,person_last_answer)

        
    print(type(person_prestige))
    print(person_prestige)
    dict["_id"]=person_name
    dict["给他人点赞数"]=voter_count
    dict["赞同"]=person_agree
    dict["点赞能量"]=person_energe
    dict["收益"]=person_yoyow
    dict["发问数"]=person_ask
    dict["回复数"]=person_answer
    dict["文章数"]=person_articles
    dict["被关注"]= person_follow
    dict["关注他人"]=person_follow_by
    dict["最后一次回复的日期"]=person_last_answer
    dict["回答总字数"]=dict_q_to_person_page["回答总字数"]
    dict["回答平均字数"]=dict_q_to_person_page["回答平均字数"]
    dict["每个回答平均获赞数"]=dict_q_to_person_page["每个回答平均获赞数"]
    dict["点赞人排名"]=dict_q_to_person_page["点赞人排名"]

    print (dict)
    exist= person_coll.find_one({'_id':person_name})
    if exist is not None:
        print("已有，开始更新")
        person_coll.update_one({'_id':person_name},{"$set":dict})
    else:         
        print("不存在，首次写入")
        person_coll.insert_one(dict) 
    
    #person_coll.update_one({'_id':person_name},{"$set":dict})
    

    #for i in person_prestige:
        #print(i)


    '''
    person_head=html.body.find('div',class_="meta")
    print (person_head)
    if person_head is  None:
        print ("Error,answers_head is  None!Please check!")
        person_top=None
    else:
        person_prestige=person_head.span.em
        print(person_prestige)
        print(person_prestige.text)
        person_agree=person_head.span[2].em
        print(person_agree)
    '''


db=get_db("biask")
coll=get_collection(db,"name_voter_dict")
ready_coll=get_collection(db,"person_region")
list_voter=coll.find({})

for i in list_voter:
    list_voter=i
count1=0
count2=0
for key,value in list_voter.items():
#print (list_voter)
    if key != "_id":
        #key="小原子"
        #print (key)
        url="https://www.biask.com/people/"+key
        html_temp=getHtml(url)
        if html_temp.select("#page_questions > span") == [] or html_temp.select("#page_questions > span") == None:
            count1 += 1
            print ("用户被删除，跳过!","第",count1,"个")
            continue
        if ready_coll.find_one({"_id":key}):
            #a=ready_coll.find_one({"_id":key})
            #print(a)
            count2 += 1
            print ("用户已经存在，跳过!","第",count2,"个")
            person_collect_to_mongo(key,value)
            continue
        person_collect_to_mongo(key,value)



    








  
