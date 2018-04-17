'''
Created on Mar 28, 2018

@author: yingc
'''
'''
List=[1,2,2,2,2,3,3,3,4,4,4,4]
a = {}
for i in List:
    if List.count(i)>=1:
        a[i] = List.count(i)
print (a)

a=[(1,1),(2,3)]

a.append((1,1))
if (1,1) in a:
    print a
else:
    print 2333
'''
#print data_item['author'],['created_utc'],['domain'],['score'],['subreddit'],['selftext'],['subreddit_id'],['num_comments']
'''
file_object = open('E:\\Reddit\\RC_2018-02-28','rU')
try: 
    for line in file_object:
        print line
finally:
    file_object.close()
'''
import gzip
import os
filename = 'E:\\Reddit\\RC_2018-02.xz'
filename1 = 'E:\\Reddit\\RC_2008-01.bz2'
filename2 = 'E:\\Reddit\\raw_data\\RC_2005-12.zip'
'''

fp = open(filename, 'rb')
data = fp.read()
archive = lzma(data)
print archive


file_object = open(filename,'rU')
try: 
    for line in file_object:
        archive = lzma(line)
        print archive
finally:
    file_object.close()

#!/usr/bin/python
# -*- coding: UTF-8 -*-

import zipfile  
import os

if __name__ == "__main__":
    inpath = os.path.join(".", "data", filename2)
    infile = zipfile.ZipFile(inpath, "r")
    a = infile.read(infile.namelist()[0]).decode('utf-8')
    #print(a)

    file_object = infile.open(infile.getinfo(infile.namelist()[0]))
    
    try: 
        for line in file_object:
            print line
    finally:
        file_object.close()
    #print(b.read().decode('utf-8'))


import bz2file
import os

if __name__ == "__main__":

    file_object = bz2file.open(filename1,'r')
    try: 
        for line in file_object:
            print line
    finally:
        file_object.close()
    
import networkx as nx
import matplotlib.pyplot as plt

edges = [['80rgu1', 'duxmurx'], ['80rgu1', 'duxmv55'], ['80rgyf', 'duxmzpp'], ['80rgu1', 'duxmzx4']]
g = nx.graph(edges)
nx.draw_networkx(g)
plt.show()


import networkx as nx           
import matplotlib.pyplot as plt 
edges = [['80rgu1', 'duxmurx'], ['80rgu1', 'duxmv55'], ['80rgyf', 'duxmzpp'], ['80rgu1', 'duxmzx4']]
g = nx.Graph(edges)
#g.add_edges_from(edges)
nx.draw_networkx(g)
plt.show()                       
'''

with open('hello.log','a+') as hello:
    print hello.read()
    
