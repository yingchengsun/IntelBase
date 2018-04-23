# -*- coding:utf-8 -*-
'''
Created on Apr 16, 2018

@author: yingc
'''


import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from time import time 
from numpy import savetxt

import collections

'''
a = {'a':1,'b':2}
if not a.has_key(''):
    a['']=3
    print a
    
for year in range(2017,2019):
        for month in range(1,2):
            print year
            if year == 2017:
                month+=9
                print month


for month in range(1,2):
    print month
    


l=[1,1,3,4,5]
c= Counter(l)
print c[1]
ll = np.array(l)
print len(ll[ll<3])
print [x if x < 3 else x for x in l]

rate = [1,1,2,3,4,5,5,6]
plt.hist(rate, bins = 6,range=[2,6],rwidth=0.9,normed=True) 


plt.xlabel(u'subreddits') 
plt.ylabel(u'subscribers')
plt.show()  


text=['aa','bb','cc']

tt= " ".join(text)
print type(tt)

import logging
 
def t():
    logger.info('dddd')  
    
if __name__ == "__main__":
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
     
    # create a file handler
     
    handler = logging.FileHandler('hello.log')
    handler.setLevel(logging.INFO)
     
    # create a logging format
     
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
     
    # add the handlers to the logger
     
    logger.addHandler(handler)
     
    logger.info('Hello baby')
    t()

dict = {1: set([2]), 6: set([2, 4]), 4: set([0,1,3]), 5: set([32, 44])}
d={'d': 75, 'b': 66, 'c': 93, 'x': 73, 'y': 71, 'z': 72}  
print d.keys()
cc= collections.OrderedDict(sorted(d.items(),key = lambda t:t[0]))

ccc = collections.OrderedDict(sorted(dict.items(),key = lambda t:len(t[1])))


if not dict.has_key(1):
    dict[1]=set([2])
else:
    dict[1].add(3)

np.savez('oo.txt',dict.keys(),dict.values())

r = np.load('oo.txt.npz')
print r['arr_0']

d= sorted(dict.items(),key = lambda x : -x[0])  
        

with open('out.txt','w+') as outfile:
    for key,value in ccc.items():
        print key,value
        outfile.write('%i\t%s\n' %(key,list(value)))

with open('out.txt','r+') as infile:
    for line in infile:
        print line.rstrip('\n').split('\t')[1]

print d
print dict(d)
with open('out.txt','w+') as outfile:
    for i in range(len(d)):
        outfile.write('%i\t%s\n' %(d[i][0],list(d[i][1])))

          
l = np.genfromtxt('out.txt', dtype='i,S10', delimiter='\t',names='a,b')
print l['a']
print int(l['b'][0].lstrip('[').rstrip(']').split(',')[0])



with open('out.txt') as infile:
    for line in infile.readlines():
        print line.split(',')
                     

print dict
a = set([1,2,3])

print tuple(a)
with open('out.txt','w+') as out:
    for key, value in dict.items():
        #out.write('%d\t%s\n' %(key,str((value))))

        out.write('%s\n' %(list(value)))
    
with open('out.txt') as infile:
    for line in infile.readlines():
        print list(line)

'''

num_comments_file_dict={}
k_num_comments_dict={}
k=20
for i in range(k+1):
    num_comments_file_dict[i]=str(i)+'_num_comments.txt'
    k_num_comments_dict[i]=0
print num_comments_file_dict

num_comments=0
if 0<=num_comments <= k:
    print 'num_comments'

