'''
Created on Apr 9, 2018

@author: yingc
'''
import networkx as nx
import matplotlib.pyplot as plt
import os
import numpy as np
from time import time 
from collections import OrderedDict

file_dir = 'E:\\Reddit'
sub_dir = 'data'

def normfun(x,mu,sigma):
   pdf = np.exp(-((x-mu)**2)/(2*sigma**2))/(sigma*np.sqrt(2*np.pi))
   return pdf
def Subreddits():
    filename = 'subreddits_id-name-subscribers-time.txt'
    filepath_name = os.path.join(file_dir, sub_dir, filename)
    ndtype = 'i,S10,S10,i,i'
    names = 'index, id, name, subscribers, time'
    s = np.genfromtxt(filepath_name, dtype=ndtype, names=names, delimiter='\t')
    print s['id']
    print s['name']
    mean = s['subscribers'].mean()  
    sd = s['subscribers'].std() 
    max = s['subscribers'].max()
    min = s['subscribers'].min() 
    print max, min
    
    x = range(len(s['name']))
    y = normfun(x,mean,sd)
    plt.plot(x,y) 
    plt.show()    

    plt.hist(s['subscribers'], bins = 100,rwidth=0.9,normed=True) 
    plt.xlabel(u'subreddits') 
    plt.ylabel(u'subscribers')
    plt.show()  

    s_arg = np.argsort(-s['subscribers'])
    s =  s[s_arg][0:100]
    s = s[np.argsort(s['subscribers'])]
    
    s1 =  np.array([s['name']]).T
    s2 =  np.array([s['subscribers']]).T

    #x = range(len(s['c']))
    x=range(100)

    plt.barh(x, s2,color='r')
    plt.yticks(x,s1)
    plt.show()

    print 'Subreddits_id-name-subscribers-time done!'

def RC_MonthlyCount():
    filename = 'monthlyCount.txt'
    filepath_name = os.path.join(file_dir, sub_dir, filename)
    ndtype = 'S10, i'
    names = 'month, count'
    s = np.genfromtxt(filepath_name, dtype=ndtype, names=names, delimiter='\t')
    print np.array([s['count']]).T
    x = range(len(s['month']))
    
    plt.plot(x,s['count']) 
    #plt.xticks(x,s['month'])
    plt.show()    
    print 'RC_MonthlyCount done!'

def RR():
    filename = 'subreddits_title-publicDescription.txt'
    filepath_name = os.path.join(file_dir, sub_dir, filename)
    ndtype = 'i, S20, S100' 
    names = 'count, title, description'
    try:
        s = np.genfromtxt(filepath_name, dtype=ndtype, names=names, delimiter='\t',comments='{[#%]}')
        print np.array([s['count']]).T
    finally:
        print 'stop'
   
    print 'RR done!'

def RC_body():
    filename = 'RC_2008-01_body.txt'
    filepath_name = os.path.join(file_dir, sub_dir, filename)
    ndtype = 'i, S100' 
    names = 'count, body'
    try:
        s = np.genfromtxt(filepath_name, dtype=ndtype, names=names, delimiter='\t',comments='{[#%]}')
        print np.array([s['count']]).T
    finally:
        print 'stop'
   
    print 'RC_body done!'
    
'''
def RC():
    filename = 'RC_2008-01_id-author-score-parentID-linkID-subredditID-subreddit-time.txt'
    filepath_name = os.path.join(file_dir, sub_dir, filename)
    ndtype = 'i, S10, S10, S10, S10, S10, S10, S10, S10' 
    names = 'count,id,author,score,parentID,linkID,subredditID,subreddit,time'
    try:
        s = np.genfromtxt(filepath_name, dtype=ndtype, names=names, delimiter='\t',comments='{[#%]}')
        print np.array([s['count']]).T
    finally: 
        print 'RC done!'
     
def RC():
    filename = 'RC_2008-01_subredditID-subreddit.txt'
    filepath_name = os.path.join(file_dir, sub_dir, filename)
    ndtype = 'i, S10, S10' 
    names = 'count,subredditID,subreddit'
    try:
        s = np.genfromtxt(filepath_name, dtype=ndtype, names=names, delimiter='\t',comments='{[#%]}')
        print s['subreddit']
        #print np.array([s['subreddit']]).T
    finally: 
        print 'RC done!'
   '''

def RC():
    filename = 'RC_2008-01_score-time-author-score-id-parentID-linkID.txt'
    filepath_name = os.path.join(file_dir, sub_dir, filename)
    ndtype = 'i,i,i,S10, S10,S10,S10' 
    names = 'count,score,time,author,id,parentID,linkID'
    try:
        s = np.genfromtxt(filepath_name, dtype=ndtype, names=names, delimiter='\t',comments='{[#%]}')
        print s['author']
        #print np.array([s['subreddit']]).T
    finally: 
        print 'RC done!'
    
def Visualize():
    t = time() 
    filename = 'parent_comment.txt'
    filepath_name = os.path.join(file_dir, sub_dir, filename)
    edges=[]
    count = 0
    with open(filepath_name,'r') as ps:
        for line in ps:
            edge = line.split('\t')
            edge[1] = edge[1].strip('\n')
            edges.append(edge)
            '''
            count+=1
            if count >1000:
                break
            '''
    g = nx.Graph(edges)
    #nx.draw(g)
    nx.draw_networkx(g)
    #plt.show()
    print "V total run time:"
    print time()-t


def Visualize0():
    t = time() 
    filename = 'test.txt'
    filepath_name = os.path.join(file_dir, sub_dir, filename)
    edges=[]
    count = 0
    with open(filepath_name,'r') as ps:
        for line in ps:
            edge = line.split('\t')
            edge[1] = edge[1].strip('\n')
            edges.append(edge)
            '''
            count+=1
            if count >1000:
                break
            '''
    g = nx.Graph(edges)
    #nx.draw(g)
    nx.draw_networkx(g)
    #plt.show()
    print "V0 total run time:"
    print time()-t

def Visualize1():
    t = time() 
    filename = 'test.txt'
    filepath_name = os.path.join(file_dir, sub_dir, filename)
    edges=[]
    count = 0
    ndtype = 'i, i' 
    names = 'a, b'
    ps = np.genfromtxt(filepath_name, dtype=ndtype, names=names, delimiter='\t',comments='{[#%]}')
    
    edges = zip(ps['a'], ps['b'])

    g = nx.Graph(edges)
    #nx.draw(g)
    nx.draw_networkx(g)
    #plt.show()

    print "V1 total run time:"
    print time()-t
    
def Visualize2():
    t = time() 
    filename = 'parent_comment.txt'
    filepath_name = os.path.join(file_dir, sub_dir, filename)
    edges=[]
    count = 0
    ndtype = 'S10, S10' 
    names = 'a, b'
    ps = np.genfromtxt(filepath_name, dtype=ndtype, names=names, delimiter='\t',comments='{[#%]}')
    
    #edges = zip(ps['a'], ps['b'])
    edges = zip(range(2002),range(2002))
    print len(edges)
    g = nx.Graph(edges)
    #nx.draw(g)
    nx.draw_networkx(g)
    plt.show()
    print 'v2'
    print "total run time:"
    print time()-t

def Visualize3():
   
    filename = 'parent_comment.txt'
    test_file = 'test.txt'
    ttt=  open(test_file,'a+')
    filepath_name = os.path.join(file_dir, sub_dir, filename)
    edges=[]
    count = 0
    ndtype = 'S10, S10' 
    names = 'a, b'
    ps = np.genfromtxt(filepath_name, dtype=ndtype, names=names, delimiter='\t',comments='{[#%]}')
    length = len(ps['a'])
    print length
    newa = ps['b']
    print newa
    #p = np.array(range(length))
    #print p.shape
    
    #nn = zip(ps['a'],range(length))
    #ddd = np.array(list(zip(newa,p)))
    
    #ids = dict(ddd)
    print {k: v for v, k in enumerate(newa)}
    print (zip(newa,range(len(newa))))
    #ids = dict(nn)

    #for key,value in ids.items():
    #    ttt.write(str(value)+'\n')
    #print ids
    '''
    print len(edges)
    t = time() 
    g = nx.Graph(edges)
    #nx.draw(g)
    nx.draw_networkx(g)
    plt.show()
    print 'v2'
    print "total run time:"
    print time()-t
    '''
def Visualize4():
   
    filename = 'parent_comment.txt'
    filepath_name = os.path.join(file_dir, sub_dir, filename)
    test_file = 'test.txt'
    test_output=  open(test_file,'a+')
    ndtype = 'S10, S10' 
    names = 'a, b'
    ps = np.genfromtxt(filepath_name, dtype=ndtype, names=names, delimiter='\t',comments='{[#%]}')
    ids = ps['a']
    pids =ps['b']
    ids_pids = np.append(ids,pids)

    id_set = set(ids_pids)
    
    #convert list to dict

    id_dict = dict(zip(id_set,range(len(id_set))))

    '''
     replace elements in a list using dictionary lookup
    
    '''
    ids_rep = [id_dict[x] if x in id_dict else x for x in ids]
    pids_rep = [id_dict[x] if x in id_dict else x for x in pids]

    edges = zip(ids_rep,pids_rep)

    for item in edges:
        test_output.write('%i\t%i\n' %(item[0],item[1]))
    test_output.close()
    t = time()
    g = nx.Graph(edges)
    #nx.draw(g)
    nx.draw_networkx(g)
    #plt.show()
    
    print 'v2'
    print "total run time:"
    print time()-t
    
def idTest():
    filename = 'subreddits_index-id.txt'
    filepath_name = os.path.join(file_dir, sub_dir, filename)
    ndtype = 'i, S10' 
    names = 'index, id'
    try:
        s = np.genfromtxt(filepath_name, dtype=ndtype, names=names, delimiter='\t',comments='{[#%]}')
        #print np.array([s['id']]).T
        print s
        print s[1156307]
        index = np.where(s['id']=='3f9eq')  
        print index[0][0]
        print type(index[0][0])
    finally:
        print 'stop'
   
    print 'RC_body done!'

def idTest2():
    filename = 'subreddits_id.txt'
    filepath_name = os.path.join(file_dir, sub_dir, filename)
    ndtype = 'S10' 
    names = 'id'
    try:
        id = np.genfromtxt(filepath_name, dtype=ndtype)

        #print np.array([s['id']]).T
        print id


        index = np.where(id=='3f9eq')  
        print index
        print index[0]
        print type(index[0][0])

    finally:
        print 'stop'
   
    print 'RC_body done!'

if __name__ == '__main__':
    Visualize()
    Visualize0()
    Visualize1()
    #Comment()
    #Subreddits()     
    #RC_MonthlyCount()
    #RC()
    #idTest2()
    print 'All done!'
