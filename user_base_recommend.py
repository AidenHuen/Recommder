#-*-encoding:utf-8-*-
__author__ = 'Aiden'
import csv
import random
import math
def Read_Data():#通过csv来读取dat中的数据
    database0=[]
    csvfile = file('F:\\recommend system\\ml-1m\\ratings.dat', 'rb')
    database = csv.reader(csvfile)
    for i in database:
        database0.append(i)
    for i in range(len(database0)):
        database0[i]=database0[i][0].split('::')
        for j in range(len(database0[i])):
            database0[i][j]=int(database0[i][j])
    print 'Read_Data_End'
    return database0

def Creat_train_text(data,M):#随机生成训练集&测试集
    train,text=[],[]
    for i in range(len(data)):
        s=random.randint(1,M)
        if(s==M):text.append(data[i])
        else:train.append(data[i])
    print len(train),len(text)
    return train,text

def moive_user(data):#生成电影——用户矩阵，第一列第一行无意义。
    #max_moive=data[0][1]
    max_moive=3952
    a=[]
    #for i in data:
        #if(max_moive<i[1]):max_moive=i[1]
    for i in range(max_moive+1):
        a.append([])
    for i in range(len(data)):
        a[data[i][1]].append(data[i][0])
    print 'moive_user_end'
    return a

def create_usertouser(data):#初始化用户相似度矩阵
    max_user=6040
    #for i in data:
        #for j in i:
            #if(max_user<j):max_user=j
    user_to_user=[[0]*(max_user+1) for row in range(max_user+1)]
    print 'create_usertouser_end'
    return user_to_user

def user_moive(data):#生成用户-电影矩阵
    user_moive0=[[] for i in range(6041)]
    for i in range(len(data)):
        user_moive0[data[i][0]].append(data[i][1])
    return user_moive0

def userSimilarity(train):#计算各用户相似度
    moive_user0=moive_user(train)
    user_to_user=create_usertouser(moive_user0)
    user_moive0=user_moive(train)
    user_moive0_long=[0 for i in range(6041)]
    for i in range(len(user_moive0)):
        user_moive0_long[i]=len(user_moive0[i])
        #print user_moive0_long[i]
    for i in moive_user0:
        for user1 in range(0,len(i)):
            for user2 in range(user1+1,len(i)):
                user_to_user[i[user1]][i[user2]]+=1.0
                user_to_user[i[user2]][i[user1]]+=1.0
    print '1.OK'
    for i in range(1,len(user_to_user)):
        for j in range(1,len(user_to_user[i])):
            user_to_user[i][j]=user_to_user[i][j]/math.sqrt(user_moive0_long[i]*user_moive0_long[j])
    print '2.OK'
    return user_to_user,user_moive0

def similar_user(user_to_user,K):#找出所有用户相似度最高的K个用户
    user_similaruser=[[] for i in range(6041)]
    for i in range(1,len(user_to_user)):
        max_three=[]
        for p in range(K):
            max=0.0
            max_mark=0
            for j in range(1,len(user_to_user)):
                if((user_to_user[i][j] not in max_three) and (user_to_user[i][j]>max)):
                    max_mark=j
                    max=user_to_user[i][j]
            max_three.append(max)
            user_similaruser[i].append(max_mark)
    #for i in user_similaruser:
        #print i
    print '3.OK'
    return user_similaruser
def user_allrecommend(user_similaruser,user_moive,user_to_user):#给每个用户分配可推荐的电影，以及计算每部电影的感兴趣度。
    user_recommedmoive=[{} for i in range(6041)]#新建一个list，其中每个元素都为一个字典
    for i in range(1,len(user_recommedmoive)):
        for similar_user in user_similaruser[i]:
            for moive in user_moive[similar_user]:
                if ((moive not in user_recommedmoive[i]) and (moive not in user_moive[i])):
                    user_recommedmoive[i][moive]=user_to_user[i][similar_user]
                if(moive in user_recommedmoive[i]):
                    user_recommedmoive[i][moive]+=user_to_user[i][similar_user]
    print '4.OK'
    return user_recommedmoive
def create_TopN(user_recommendmoive):#初始化TopN表，经排序后，生成各用户的TopN表。
    TopN=[[] for i in range(6041)]
    user_interestscore=[[] for i in range(6041)]
    for i in range(1,len(TopN)):#将电影，兴趣度一对一的放入两个list中。
        for key in user_recommendmoive[i].keys():
            TopN[i].append(key)
            user_interestscore[i].append(user_recommendmoive[i][key])
    for i in range(1,len(TopN)):
        for x in range(len(user_interestscore[i])):#用冒泡法进行排序
            max=0
            max_mark=0
            for y in range(x,len(user_interestscore[i])):
                if(user_interestscore[i][y]>max):
                    max=user_interestscore[i][y]
                    max_mark=y
            user_interestscore[i][x],user_interestscore[i][max_mark]=user_interestscore[i][max_mark],user_interestscore[i][x]
            TopN[i][x],TopN[i][max_mark]=TopN[i][max_mark],TopN[i][x]
    #for i in range(len(user_interestscore)):
        #print user_interestscore[i]
        #print TopN[i]
    return TopN
#__________main__________#
M=8
data=Read_Data()
a=Creat_train_text(data,M)
train=a[0]
result=userSimilarity(train)
user_to_user=result[0]
user_moive=result[1]
K=4
user_similaruser=similar_user(user_to_user,K)
user_recommedmoive_score=user_allrecommend(user_similaruser,user_moive,user_to_user)
TopN=create_TopN(user_recommedmoive_score)
for i in TopN:#输出每个用户的推荐榜单。
    print i
