'''
Created on Apr 17, 2018

@author: yingc
'''
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from time import time 
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
'''

text=['aa','bb','cc']

tt= " ".join(text)
print type(tt)
