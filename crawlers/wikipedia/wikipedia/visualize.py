'''
Created on Dec 14, 2017

@author: yingc
'''
import matplotlib.pyplot as plt
import networkx as nx
#edges=[(0,1), (0,2), (3,2), (2,1)]
edges = [('a','b'),('a','c'),('d','b'),('c','b')]
g=nx.Graph()
g.add_edges_from(edges)
print g.edges()

d = nx.degree(g)
print d
dd={}
for e in d:
    dd[e[0]]=e[1]
print dd
d=dd
values = [x/10.0 for x in d.values()]
print values

nx.draw(g, node_size=[v * 200 for v in d.values()], cmap=plt.get_cmap('OrRd'), with_labels=True, node_color=values)
plt.show()
'''
xx = [x[0] for x in edges]
print xx
yy = [x[1] for x in edges]
print yy
line = plt.plot(xx, yy, 'ro-')
plt.show()
'''

