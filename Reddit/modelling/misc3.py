'''
Created on 
@author: yingc
'''
import math

from collections import Counter

import matplotlib.pyplot as plt


file_dir = 'E:\\Reddit\\data'
from datetime import datetime
import itertools
from datetime import datetime
import numpy as np

def prefix_time():
    prefix_time = datetime.now().strftime('%Y%m%d%H%M%S')
    return prefix_time

scaled_degree=[]
#node_degrees = [101, 100, 12, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 55, 44, 28, 3, 2, 1, 6, 1, 1, 1, 1, 1, 1, 11, 5, 4, 3, 2, 1, 10, 3, 2, 1, 2, 1, 4, 3, 1, 2, 1, 4, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 2, 1, 1, 1, 1, 1, 1, 8, 7, 4, 3, 1, 1, 2, 1, 2, 1, 22, 9, 3, 1, 1, 5, 1, 1, 1, 1, 1, 1, 1, 5, 4, 3, 1, 1, 1, 1, 1, 1]
node_degrees = [101, 100, 50, 24, 5, 1, 1, 1, 1, 11, 6, 4, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 1, 1, 4, 3, 1, 1, 2, 1, 2, 1, 4, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 49, 38, 34, 7, 2, 1, 4, 3, 2, 1, 1, 4, 2, 1, 1, 1, 4, 3, 2, 1, 7, 6, 5, 3, 2, 1, 1, 4, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 10, 9, 6, 5, 2, 1, 1, 1, 2, 1]
   
node_heights = [11, 10, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 8, 7, 3, 2, 1, 2, 1, 1, 1, 1, 1, 1, 6, 5, 4, 3, 2, 1, 5, 3, 2, 1, 2, 1, 4, 3, 1, 2, 1, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 2, 1, 1, 1, 1, 1, 1, 5, 4, 3, 2, 1, 1, 2, 1, 2, 1, 4, 3, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 3, 2, 1, 1, 1, 1, 1, 1]
for d in node_degrees:
    scaled_degree.append(math.pow(d, 0.5 ))

normalized_scaled_degree=[]   
m = max(scaled_degree)
for d in scaled_degree:
    normalized_scaled_degree.append(float(d)/m)
        
print normalized_scaled_degree

'''    
scaled = []
for i, w in enumerate(node_degrees):
    #print w,  node_heights[i]
    scaled.append( w/math.pow( node_heights[i], 0.5 ))
#scaled = sorted(scaled, reverse  =True)
print scaled
'''

docs  =[[(0, 0.9987439)],[(0, 0.9996473)],[(0, 0.011705653), (1, 0.9882943)],[(0, 0.87343156), (1, 0.12656844)]]
docs  =[(0, 0.011705653), (1, 0.9882943)]


'''
matched=[]
topic_assign = max([d for d in docs], key=lambda item: (item[1]))
print topic_assign

for i, doc in enumerate(docs):
    print doc
    topic_assign = max([d for d in doc], key=lambda item: (item[1]))
    topic_converted = topics_label[topic_assign[0]]

    if topic_converted == lables[i]:
        matched.append(1)
    else:
        matched.append(0)

accuracy = float(sum(matched))/len(matched)
print accuracy
'''
    
    