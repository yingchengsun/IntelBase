import numpy as np
import guidedlda

from math import log
from sklearn.metrics import mutual_info_score, normalized_mutual_info_score
from bokeh.layouts import row
'''
signals = [0, 0, 1,1,1]
labels = ['a','b','c','d','e']
print mutual_info_score(labels, signals)
print normalized_mutual_info_score(labels, signals)
'''
'''
from gensim.test.utils import datapath
from gensim.models.word2vec import Text8Corpus
from gensim.models.phrases import Phrases, Phraser

sentences = Text8Corpus('testcorpus.txt')

phrases = Phrases(sentences, min_count=1, threshold=1)  # train model

#print phrases[[ u'What', u'concept', u'completely', u'blows', u'your', u'mind?']]  # apply model to sentence
'''

'''
import wikiwords
print 1./len("puerto")
print wikiwords.freq("puerto", lambda x: 1./len(x))
print wikiwords.freq("puerto")


import ngram
#print ngram.NGram.compare('hong','kong',N=2)
G = ngram.NGram(['joe','joseph','jon','john','sally'])
print G
print G.find('jon')
'''
'''
input_list = ['all', 'this', 'happened', 'more', 'or', 'less']

def find_bigrams(input_list, n):
  return zip(*[input_list[i:] for i in range(n)])
print find_bigrams(input_list, 3)

from ngram import NGram

print NGram.compare('spam', 'spam')
'''


    
from palmettopy.palmetto import Palmetto
import numpy as np

palmetto = Palmetto()
#words = ["cake", "apple", "banana", "cherry", "chocolate"]
#words = ["like", "brown", "need", "really", "guy", "think", "read", "worth", "super","they're"]

'''
#our model
corpus = [
            [['confession', 'video', 'tape', 'blowing', 'made', 'need', 'texas', 'bomber', 'serial', 'evil'],
             ['super', 'brown', 'bowl', 'winning', 'chance', 'like', 'morning', 'every', 'take', 'bowl'],
             ['see', 'ever', 'chance', 'video', 'read', 'need', 'reading', 'worth', 'life', 'evil']],
          
            [['light', 'universe', 'still', "can't", 'concept', 'mind', 'completely', 'light', 'speed', 'blow'],
             ['universe', 'light', 'speed', 'away', 'never', 'see', 'concept', 'observable', 'reach', "can't"],
             ['speed', 'light', 'universe', 'faster', 'away', 'observable', 'space', 'expanding', 'going', 'light']],
          
            [['would', 'id', 'card', 'need', 'think', 'people', 'nation', 'immigrant', 'worker', 'much'],
             ['would', 'immigration', 'people', 'illegal', 'new', 'long', 'worker', 'allowed', 'law', 'term'],
             ['would', 'id', 'immigration', 'people', 'national', 'need', 'voter', 'American', 'job', 'immigrant']]
          ]

'''
'''
 

#LDA
corpus = [
            [['btk', 'people', 'got', 'made', 'guy', 'like', 'play', 'going', "they're", 'brown'],
             ['read', 'transcript', 'reading', 'like', "i'm", 'need', 'brown', 'it', 'evil', 'want'],
             ['guy', 'like', 'brown', 'one', 'crime', "they'll", 'chance', 'think', 'say', 'get']],
          
            [["light", "away", "like", "universe", "moving", "space", "speed", "light.", "still", "faster"],
             ["speed", "light", "away", "universe", "faster", "u", "still", "light.", "galaxy", "observable"],
             ["faster", "away", "universe", "space", "observable", "can\'t", "moving", "speed", "u", "light"]],
           
          
            [["would", "people", "immigration", "national", "id", "like", "number", "country", "already", "see"],
             ["people", "would", "need", "id", "even", "voter", "immigrant", "law", "think", "million"],
             ["id", "people", "need", "would", "make", "cost", "i.d.", "get", "voter", "work"]]
          ]

'''
'''
#PTM
corpus = [
            [['like', 'brown', 'read', 'think', 'people', 'going', 'get', 'really', "want", "i'm"],
             ['guy', 'need', 'it', 'see', "go", 'one', 'made', 'something', 'btk', 'life'],
             ['transcript', 'tape', 'crime', "they'll", 'would', "got", "they're", 'ever', "can't", 'chance']],
          
            [["away", "faster", "u", "still", "expanding", "object", "see", "never", "can't", "one"],
             ["space", "stuff", "thing", "way", "billion", "mean", "make", "actually.", "year", "everything"],
             ["speed", "light", "universe", "moving", "light", "observable", "galaxy", "going", "could", "ever"]],
          
            [["make", "work", "get", "number", "state", "without", "become", "time", "economic", "everyone"],
             ["would", "immigrant", "country", "much", "law", "population", "million", "job", "think", "actually"],
             ["people", "would", "id", "immigration", "need", "voter", "even", "already", "national", "like"]]
          ]
'''
'''

            [['guy', 'like', 'get', 'people', 'actually', 'think', 'them', 'fucked', "them", "transcript"],
             ['tape', 'life', 'bittaker', 'reading', "killer", 'need', 'made', 'transcript', 'read', 'crime'],
             ["they'll", 'drug', 'homeless', "like", 'something', "get", "i've", 'gang', "got", 'crime']],
          
          '''
#BTM
corpus = [
            [["speed", "away", "light", "moving", "u", "stuff", "faster", "light", "object", "space"],
             ["faster", "universe", "space", "still", "expanding", "speed", "i'm", "light", "know", "moving"],
             ["light", "universe", "speed", "still", "galaxy", "going", "billion", "way", "faster", "observable"]],
          
            [["would", "immigration", "people", "make", "allowed", "number", "job", "also", "business", "american"],
             ["people", "country", "immigrant", "would", "population", "world", "new", "work", "need", "child"],
             ["people", "id", "million", "would", "need", "voter", "even", "law", "think", "national"]]
          ]



measures = ['cv','cp','uci','umass','npmi','ca']
#measures = ['cp','uci','umass','npmi','ca']
#measures = ['cp']          
for c in corpus:
    results = [[None]*3 for i in range(6)]
    for row, m in enumerate(measures):
        for col, words in enumerate(c):
            print m, words
            r = palmetto.get_coherence(words, coherence_type = m)
            print r
            results[row][col] = r
    
    print results
    ave = np.mean(results, axis = 1)
    print [float("%.4f" %a) for a in ave]


