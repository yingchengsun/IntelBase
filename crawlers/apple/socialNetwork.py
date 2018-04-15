#coding:utf-8
'''
Created on Nov 26, 2017

@author: yingc
'''

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# image from http://matplotlib.sourceforge.net/users/image_tutorial.html
img1=mpimg.imread('pictures/Tim Cook.jpg')
img2=mpimg.imread('pictures/Alan Dye.jpg')
G=nx.complete_graph(4)

G.node[0]['image']=img1
G.node[1]['image']=img2
G.node[2]['image']=img1
G.node[3]['image']=img2

pos=nx.spring_layout(G)

fig=plt.figure(figsize=(5,5))
ax=plt.subplot(111)
ax.set_aspect('equal')
d = nx.degree(G)

'''
plt.xlim(-0.5,1.5)
plt.ylim(-0.5,1.5)
'''
trans=ax.transData.transform
trans2=fig.transFigure.inverted().transform

piesize=0.2 # this is the image size
p2=piesize/2.0
for n in G:
   xx,yy=trans(pos[n]) # figure coordinates
   xa,ya=trans2((xx,yy)) # axes coordinates
   a = plt.axes([xa-p2,ya-p2, piesize, piesize])
   a.set_aspect('equal')
   a.imshow(G.node[n]['image'])
   a.axis('off')


plt.show()  
#print G.nodes()

'''
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


#G = nx.random_graphs.barabasi_albert_graph(100,1)   #生成一个BA无标度网络G
G = nx.Graph()
a = [2,3]
H = nx.path_graph(10)
e = (2,3)
G.add_nodes_from(H)
n = 10
H = nx.path_graph(n)
G.add_edges_from(H.edges()) 
print G.number_of_nodes() #查看点的数量
print G.number_of_edges() #查看边的数量
print G.nodes() #返回所有点的信息(list)
print G.edges() #返回所有边的信息(list中每个元素是一个tuple)
G.add_node('benz', money=10000, fuel="1.5L")
print G.node['benz'] # {'fuel': '1.5L', 'money': 10000}
print G.node['benz']['money'] # 10000
print G.nodes(data=True)


nx.draw_spectral(G)                            
plt.show()


'''
'''
img=mpimg.imread('pictures/Tim Cook.jpg')
# draw graph without images
G =nx.Graph()
G.add_edge(0,1,image=img,size=0.1)
G.add_edge(1,2,image=img,size=0.1)
G.add_edge(2,3,image=img,size=0.1)
G.add_edge(3,4,image=img,size=0.1)

pos=nx.spring_layout(G)
nx.draw(G,pos)

# add images on edges
ax=plt.gca()
fig=plt.gcf()
label_pos = 0.5 # middle of edge, halfway between nodes
trans = ax.transData.transform
trans2 = fig.transFigure.inverted().transform
imsize = 0.1 # this is the image size
for (n1,n2) in G.edges():
    (x1,y1) = pos[n1]
    (x2,y2) = pos[n2]
    (x,y) = (x1 * label_pos + x2 * (1.0 - label_pos),
             y1 * label_pos + y2 * (1.0 - label_pos))
    xx,yy = trans((x,y)) # figure coordinates
    xa,ya = trans2((xx,yy)) # axes coordinates
    imsize = G[n1][n2]['size']
    img =  G[n1][n2]['image']
    a = plt.axes([xa-imsize/2.0,ya-imsize/2.0, imsize, imsize ])
    a.imshow(img)
    a.set_aspect('equal')
    a.axis('off')
plt.savefig('pictures/result.jpg') 
'''