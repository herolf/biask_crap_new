class BitastPerson () :

    def __init__(self,name,collect):
        self.name=name
        self.collect=collect

    def numtodate(self,num):
        ma=re.match(r'([0-9]{4})([0-9]{2})([0-9]{2})',num)
        year=ma.group(1)
        month=ma.group(2)
        day=ma.group(3)
        date=str(year)+'-'+str(month)+'-'+str(day)
        return date


    def sort_dict(self,dict):
        sort_dict = []
        #print(len(dict))
        all_vote=0
        for i in range(len(dict)):
            flag=0
            max=0
            
            for key,value in dict.items() :
                if flag == 0:
                    max=int(value)
                    temp=key
                    flag +=1
                elif int(value) > max:
                    max=int(value)
                    temp=key
                    flag +=1
            sort_dict.append({temp:max})
            dict.pop(temp)
            all_vote+=max
        #sort_dict.append({"总点赞数":all_vote})
        #print (sort_dict)
        return (sort_dict)



    def get_answers_voters(self,name,collect):
        answer_man=name
        if answer_man == "all":
            search_answers={}
        else:
            search_answers={"answer_man":answer_man}
        docs= collect.find(search_answers)
        list=[]
        dict={}
        times=0
        emptimes=0
        #voter count and list #所有点赞人：点赞数
        for doc in docs:
            #a=pprint.pprint(doc["voter_list"])
            a=doc["voter_list"]
            if a == [] :
                emptimes+=1
            for i in a:
                print (i)
                flag=0
                for ii in list:
                    if ii==i:
                        flag+=1
                        dict[i]+=1
                        continue
                if flag==0:
                    list.append(i)
                    dict[i]=1
            times +=1
        #print (list)
        #print (dict)
        #print (emptimes)
        #print (times)
        #print (len(list))
        dict1=self.sort_dict(dict)
        return dict1



    def get_contents_wordcount(self,name,collect):
        answer_man=name
        if name == "all":
            search_answers={}
        else:
            search_answers={"answer_man":answer_man}
        docs=collect.find(search_answers)
        times=0
        content_dict={}
        #dict_sort={}
        if docs is not None:
            for doc in docs:
            #pprint.pprint(doc["answer_content"])
                a=doc["answer_content"]
                if a==[]:
                    emptimes+=1
                for i in a:
                    for ii in i:
                        times+=1
                content_dict[doc["answer_man"]]=times
            dict_sort=self.sort_dict(content_dict)
        
            return dict_sort  

    def get_contents_num(self,name,collect):
        answer_man=name
        if name == "all":
            search_answers={}
        else:
            search_answers={"answer_man":answer_man}
        docs=collect.find(search_answers)
        times=0
        content_dict={}
        #dict_sort={}
        for doc in docs:
            times+=1
        return (times)
    
