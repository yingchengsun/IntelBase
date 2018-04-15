'''
Created on Oct 25, 2017

@author: yingc
'''
from urllib2 import urlopen
import sys
from collections import deque
import urllib

import re
from bs4 import BeautifulSoup
import lxml
import sqlite3
import jieba
import MySQLdb
'''
safelock=input('Do you want to build a lexicon? (y/n)')
if safelock!='y':
    sys.exit('exit!')
'''
url='https://en.wikipedia.org/wiki/IPhone_8'#Entrance

queue=deque()
visited=set()
queue.append(url)

try:
    conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='',port=3306)  #Connects to MySQLdb
    cur=conn.cursor()
    cur.execute('create database if not exists viewsdu')  #Creates schema
    conn.select_db('viewsdu')
    cur.execute('drop table doc')
    cur.execute('create table if not exists doc (id int primary key,link varchar(50))')
    cur.execute('drop table word')
    cur.execute('create table  if not exists word (term varchar(25) primary key,list varchar(50) )')
    conn.commit()
    conn.close()
except MySQLdb.Error,e:  #If error occurs while inserting records
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])        


print('***************Started!***************************************************')
cnt=0

while queue:
    url=queue.popleft()
    visited.add(url)
    cnt+=1
    print('Start to scrape the',cnt,'link:',url)

    try:
        response=urlopen(url)
        content=response.read()

    except:
        continue
    
    m=re.findall(r'<a href=',content,re.I)
    print m
    for x in m:
        if re.match(r'https.+',x):
            if not re.match(r'https\:\/\/www\.yahoo\.com\/.+',x):
                continue
        '''
        elif re.match(r'\/new\/.+',x):
            x='http://www.view.sdu.edu.cn'+x
        else:
            x='http://www.view.sdu.edu.cn/new/'+x
        '''
        if (x not in visited) and (x not in queue):
            queue.append(x)

    
    soup=BeautifulSoup(content,'lxml')
    title=soup.title
    article=soup.find('div',class_='text_s',id='content')
    author=soup.find('div',class_='text_c')

    if title==None and article==None and author==None:
        print('Empty page.')
        continue

    elif article==None and author==None:
        print('Only title.')
        title=title.text
        title=''.join(title.split())
        article=''
        author=''


    elif article==None:
        print('No content')
        title=soup.h1.text
        title=''.join(title.split())
        article=''
        author=author.get_text("",strip=True)
        author=''.join(author.split())

    elif author==None:
        print('No author')
        title=soup.h1.text
        title=''.join(title.split())
        article=article.get_text("",strip=True)
        article=''.join(article.split())
        author=''

    else:
        title=soup.h1.text
        title=''.join(title.split())
        article=article.get_text("",strip=True)
        article=''.join(article.split())
        author=author.find_next_sibling('div',class_='text_c').get_text("",strip=True)
        author=''.join(author.split())

    print('Title:',title)

    seggen=jieba.cut_for_search(title)
    seglist=list(seggen)
    seggen=jieba.cut_for_search(article)
    seglist+=list(seggen)
    seggen=jieba.cut_for_search(author)
    seglist+=list(seggen)


    conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='',port=3306)  #Connects to MySQLdb
    conn.select_db('viewsdu')
    cur=conn.cursor()
    
    cur.execute('insert into doc values (%s,%s)',(int(cnt),url))
    
    for word in seglist:
        #print(word)
        cur.execute('select list from word where term= %s',(word,))
        result=cur.fetchall()

        if len(result)==0:
            docliststr=str(cnt)
            cur.execute('insert into word values(%s,%s)',(word,docliststr))

        else:
            docliststr=result[0][0]
            docliststr+=' '+str(cnt)
            cur.execute('update word set list=? where term=?',(docliststr,word))

    conn.commit()
    conn.close()
    print('Done!=======================================================')