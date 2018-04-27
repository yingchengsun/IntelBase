'''
Created on Apr 26, 2018

@author: yingc
'''
import networkx as nx
import pylab as plt
from networkx.drawing.nx_agraph import graphviz_layout


G = nx.DiGraph()
G.add_node(1,level=1)
G.add_node(2,level=2)
G.add_node(3,level=2)
G.add_node(4,level=3)

G.add_edge(1,2)
G.add_edge(1,3)
G.add_edge(2,4)

nx.draw(G, pos=graphviz_layout(G), node_size=1600, cmap=plt.cm.Blues,
        node_color=range(len(G)),
        prog='dot')
plt.show()
