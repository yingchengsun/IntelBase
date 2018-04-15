'''
Created on Dec 4, 2017

@author: yingc
'''
'''
from textblob import TextBlob
t = TextBlob("This is fuck!!!")

print t.sentiment



from pattern.web    import Google, Bing, plaintext
from pattern.en     import parsetree
from pattern.search import search
from pattern.graph  import Graph
  
g = Graph()
for i in range(10):
    for result in Google().search('"fuck"', start=i+1, count=10):
        s = result.text.lower() 
        s = plaintext(s)
        s = parsetree(s)
        p = '{NP} (VP) fuck {NP}'
        for m in search(p, s):
            x = m.group(1).string # NP left
            y = m.group(2).string # NP right
            if x not in g:
                g.add_node(x)
            if y not in g:
                g.add_node(y)
            g.add_edge(g[x], g[y], stroke=(0,0,0,0.75)) # R,G,B,A
 
g = g.split()[0] # Largest subgraph.
print g

for n in g.sorted()[:40]: # Sort by Node.weight.
    n.fill = (0, 0.5, 1, 0.75 * n.weight)

g.export('test3', directed=True, weighted=0.6)
'''

from pattern.graph import Graph,CANVAS
 
g = Graph()
for n1, n2 in (
  ('cat', 'tail'), ('cat', 'purr'), ('purr', 'sound'),
  ('dog', 'tail'), ('dog', 'bark'), ('bark', 'sound')):
    g.add_node(n1)
    g.add_node(n2)
    g.add_edge(n1, n2, weight=0.0, type='is-related-to')

for n in sorted(g.nodes, key=lambda n: n.weight):
    print '%.2f' % n.weight, n

g.export('sound1', directed=True)

import cherrypy

class Visualization(object):
    def index(self):
        return (
            '<html>'
            '<head>'
            '<script src="sound1/canvas.js"></script>'
            '<script src="sound1/graph.js"></script>'
            '</head>'
            '<body>' + g.serialize(CANVAS, directed=True) +
            '</body>'
            '</html>'
        )
    index.exposed = True

cherrypy.quickstart(Visualization())