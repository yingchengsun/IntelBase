'''
Created on Dec 4, 2017

@author: yingc
'''

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# image from http://matplotlib.sourceforge.net/users/image_tutorial.html
img1=mpimg.imread('pictures/Tim Cook.jpg')
img2=mpimg.imread('pictures/Alan Dye.jpg')

g = nx.Graph()
g.add_edges_from([(1,2), (1,3), (1,4)])
H=nx.path_graph(10)
print g.node()
print nx.clustering(g)
d = nx.degree(g)
dd={}
for e in d:
    dd[e[0]]=e[1]

d=dd
values = [x/10.0 for x in d.values()]
print values
#nx.draw_networkx(G, pos, arrows, with_labels=True)
nx.draw(g, nodelist=d.keys(), node_size=[v * 200 for v in d.values()],  with_labels=True, node_color='aqua')
plt.show()
#node_color='deeppink'
