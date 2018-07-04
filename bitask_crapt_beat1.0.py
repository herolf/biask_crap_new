# coding: utf-8
from pymongo import MongoClient
from bson.objectid import ObjectId
import requests
import re
from bs4 import BeautifulSoup
from bs4 import NavigableString
from bs4 import Tag
import pprint
import pymongo

#from 607bitask_zip import get_question_askregion
#from 607bitask_zip import get_answers_region

def getHtml(url):
    try:
        html = requests.get(url)
        bsObj = BeautifulSoup(html.text,'lxml')
        Html = bsObj
    except AttributeError as e:
        return None
    return Html

def get_ask_region(url):
    html = getHtml(url)
    asker_region_dict={}
    asker_head=html.body.find('dd',class_='pull-left')
    #asker_foot=html.body.find('div',class_='mod-footer')

    if asker_head != None :
        asker_name=asker_head.a.string
    else :
        asker_name=None
    question_region=html.body.find_all(class_='aw-mod aw-question-detail aw-item')
    times=0
    question_title_string=None
    question_date_string=None
    question_content_list = []
    for i in question_region:
        if times==0:                    
            question_title          = i.h1.contents
            question_title_Nstring  = question_title[0].string                                                
            question_title_string   = str(question_title_Nstring).strip()
            question_contents=i.find_all(text=re.compile(''))
            foot=i.find('div',class_='mod-footer')
            date=foot.div.span
            #print (type(date))
            question_date=date.contents
            question_date_string=question_date[0].string
            #print (date.contents)
            ii_times=0
            for ii in question_contents:
                if ii_times>=1 and re.match(r'<',ii)==None and ii!=r" 站内邀请 " and ii != " end 站内邀请 " and ii !="没有找到相关结果" and ii != "与内容相关的链接" and ii != "&yen; 打赏"\
                and ii != r"\s"  and  ii != "添加评论" and ii != "置顶" and ii !="分享\t\t\t\t\t\t\t\t\t" and ii != " 相关链接 " and ii != " end 相关链接 " and ii != "提交" and ii !="\n"\
                and re.match(r'^ <',ii)==None and re.search(r'转账|已邀请',ii)==None and ii !=r"\n" and ii !=r"\t": 
                    question_content_list.append(ii)
                    #print (repr(ii))
                    #print (type(ii))
                ii_times+=1
    #print (asker_foot)
    #question_date_string=asker_foot.find('span',class_='text-color-999').get_text().strip()
    

    asker_region_dict['_id']=url
    #asker_region_dict['question_url']=url
    asker_region_dict['question_title']=question_title_string
    asker_region_dict['question_asker']=asker_name
    asker_region_dict['question_content']=question_content_list
    asker_region_dict['date_time']=question_date_string
    return asker_region_dict

def get_answers_region(url):
    #
    alert=None
    #

    html = getHtml(url)
    answers_region_list=[]
    #回答区域
    answers_head=html.body.find(class_="mod-body aw-feed-list")
    if answers_head is  None:
        print ("Error,answers_head is  None!Please check!")
        answer=None
    else:
        answer=answers_head.find(class_="aw-item")
    flag=1
    while answer!=None:
        print (flag)  
        #print (answer)                                                                   
        if (isinstance(answer,Tag)):
            single_reply_dict={}
            #"问题标识  answer_id"
            answer_id = answer.get('id')  
            #print (answer_id)    
            #内容 answer_content
            answer_contents=None
            answer_contents=answer.find(class_="mod-body clearfix")
            if answer_contents is not None:
                answer_contenttemp=answer_contents.get_text().split('\n')                         
            #回答者：answer_man
            answer_man_temp=None
            answer_man_temp=answer.find(class_="aw-user-name")
            if answer_man_temp != None:
                answer_man=answer_man_temp.get_text().strip()
                
            #回答时间：answer_time
            answer_time_temp=None
            answer_time_temp=answer.find(class_="text-color-999 pull-right")
            if answer_time_temp != None:
                answer_time = answer_time_temp.get_text().strip()
            #点赞者：voter_list
            answer_voter_temp=None 
            answer_voters=None
            answer_voters_temp=answer.find(class_="text-color-999 aw-agree-by")
            if answer_voters_temp !=None:
                answer_voters=answer_voters_temp               
            voter_list=[]
            if (isinstance(answer_voters,Tag)):
                answer_voter_search=answer_voters.find_all(class_="aw-user-name")
                for answer_voter in answer_voter_search:
                    voter_list.append(answer_voter.get_text())
            alert=html.body.find(class_="alert alert-warning fade in")
            #if alert !=None:
            #    single_reply_dict['_id']=answer_id+str(url)+str(flag)
            #else :
            #    single_reply_dict['_id']=str(answer_id)+str(answer_man)+str(url+"alert")+str(flag)
            single_reply_dict['answer_id']=answer_id
            single_reply_dict['answer_content']=answer_contenttemp
            single_reply_dict['answer_man']=answer_man
            single_reply_dict['voter_list']=voter_list
            single_reply_dict['datatime']=answer_time
            single_reply_dict['url']=url
            answers_region_list.append(single_reply_dict)
        answer = answer.next_sibling
        flag+=1
    return answers_region_list
def update_answers_region(url):
    #
    alert=None
    #

    html = getHtml(url)
    answers_region_list=[]
    #回答区域
    answers_head=html.body.find(class_="mod-body aw-feed-list")
    if answers_head is  None:
        print ("Error,answers_head is  None!Please check!")
        answer=None
    else:
        answer=answers_head.find(class_="aw-item")
    flag=1
    while answer!=None:
        print (flag)  
        #print (answer)                                                                   
        if (isinstance(answer,Tag)):
            single_reply_dict={}
            #"问题标识  answer_id"
            answer_id = answer.get('id')  
            #print (answer_id)    
            #内容 answer_content
            answer_contents=None
            answer_contents=answer.find(class_="mod-body clearfix")
            if answer_contents is not None:
                answer_contenttemp=answer_contents.get_text().split('\n')                         
            #回答者：answer_man
            answer_man_temp=None
            answer_man_temp=answer.find(class_="aw-user-name")
            if answer_man_temp != None:
                answer_man=answer_man_temp.get_text().strip()
                
            #回答时间：answer_time
            answer_time_temp=None
            answer_time_temp=answer.find(class_="text-color-999 pull-right")
            if answer_time_temp != None:
                answer_time = answer_time_temp.get_text().strip()
            #点赞者：voter_list
            answer_voter_temp=None 
            answer_voters=None
            answer_voters_temp=answer.find(class_="text-color-999 aw-agree-by")
            if answer_voters_temp !=None:
                answer_voters=answer_voters_temp               
            voter_list=[]
            if (isinstance(answer_voters,Tag)):
                answer_voter_search=answer_voters.find_all(class_="aw-user-name")
                for answer_voter in answer_voter_search:
                    voter_list.append(answer_voter.get_text())
            #alert=html.body.find(class_="alert alert-warning fade in")
            #if alert !=None:
            #    single_reply_dict['_id']=answer_id+str(url)+str(flag)
            #else :
            #    single_reply_dict['_id']=str(answer_id)+str(answer_man)+str(url+"alert")+str(flag)
            
            single_reply_dict['answer_id']=answer_id
            single_reply_dict['answer_content']=answer_contenttemp
            single_reply_dict['answer_man']=answer_man
            single_reply_dict['voter_list']=voter_list
            single_reply_dict['datatime']=answer_time
            single_reply_dict['url']=url
            answers_region_list.append(single_reply_dict)
        answer = answer.next_sibling
        flag+=1
    return answers_region_list
def get_db(db_name):
    #setup
    client = MongoClient("localhost",27017)
    db=client[db_name]
    return db

def get_collection(db,collection_name):
    coll=db[collection_name]
    return coll

def op(url_temp,num,pages_to_screp):
    #url="https://www.bitask.org/question/"+str(0+num)
    db=get_db("biask")
    ask=get_collection(db,"ask_region")
    answers=get_collection(db,"answers_region")
    for i in range(pages_to_screp):
        url=url_temp+str(i+num)
        print (url)
        exist=ask.find_one({'_id':url})
       # print (exist)
       # print (exist['question_asker'])
        if exist is not None:
            if exist['question_asker'] is not None:
                continue
            else:
                single_askregion=get_ask_region(url)
                single_answers_region=get_answers_region(url) 
                if (single_askregion is not None) and (single_askregion != {}) :
                
                    ask.update_one(
                        {'_id':url},
                        {"$set":single_askregion}
                    )
                    #没有加入问题区的升级，因为_id没有统一格式，这一版暂不更新，下一版加入评论区的采集方法，一起更
                continue
        single_askregion=get_ask_region(url)
        single_answers_region=get_answers_region(url) 
        if (single_askregion is not None) and (single_askregion != {}) :
            ask.insert_one(single_askregion)
            if single_answers_region is not None and (single_answers_region != []) :
                print (single_answers_region)
                print ("========================================================")
                print (single_askregion)
                answers.insert_many(single_answers_region)

url="https://www.bitask.org/question/"
op(url,11000,15000)
#0-1172
'''  1344    Traceback (most recent call last):
  File "g:\workdir\pachong\mongo_test.py", line 155, in <module>
    op(url,115,7000)#150  #10034-10190  #9000-9490 #9491-10034 #8000-8495 8496-8889 8890-9000 7000-7980  1-114
  File "g:\workdir\pachong\mongo_test.py", line 152, in op
    answers.insert_many(single_answers_region)
  File "D:\ProgramData\Anaconda3\lib\site-packages\pymongo\collection.py", line 711, in insert_many
    blk.execute(self.write_concern.document)
  File "D:\ProgramData\Anaconda3\lib\site-packages\pymongo\bulk.py", line 493, in execute
    return self.execute_command(sock_info, generator, write_concern)
  File "D:\ProgramData\Anaconda3\lib\site-packages\pymongo\bulk.py", line 331, in execute_command
    raise BulkWriteError(full_result)
pymongo.errors.BulkWriteError: batch op errors occurred

1757      File "g:\workdir\pachong\mongo_test.py", line 166, in <module>
    op(url,1535,1000)#150  #10034-10190  #9000-9490 #9491-10034 #8000-8495 8496-8889 8890-9000 7000-7980  1-114(DuplicateKeyError)  115-1344-1403-1426
  File "g:\workdir\pachong\mongo_test.py", line 163, in op
    answers.insert_many(single_answers_region)
  File "D:\ProgramData\Anaconda3\lib\site-packages\pymongo\collection.py", line 711, in insert_many
    blk.execute(self.write_concern.document)
  File "D:\ProgramData\Anaconda3\lib\site-packages\pymongo\bulk.py", line 493, in execute
    return self.execute_command(sock_info, generator, write_concern)
  File "D:\ProgramData\Anaconda3\lib\site-packages\pymongo\bulk.py", line 331, in execute_command
    raise BulkWriteError(full_result)
pymongo.errors.BulkWriteError: batch op errors occurred
'''

'''
db=get_db("biask")
ask=get_collection(db,"ask_region")
answers=get_collection(db,"answers_region")

#a={"_id":"https://www.bitask.org/question/8560"}

#doc= ask.find_one(a)
#print (doc["question_asker"])

#b={"answer_man":"karma"}

b={"datatime":"2018-06-06"}
docs= answers.find(b)

times=0
list=[]
dict={}
for doc in docs:
    a=pprint.pprint(doc["voter_list"])
    a=doc["voter_list"]
    for i in a:
        flag=0
        for ii in list:
            if ii==i:
                flag+=1
                dict[i]+=1
                continue
        if flag==0:
            list.append(i)
            dict[i]=1


    print(len(a))
    times+=len(a)
    print (type(a))
    #$print(a[1])
print (times)
print (dict)
print (list)
'''


#更新数据











