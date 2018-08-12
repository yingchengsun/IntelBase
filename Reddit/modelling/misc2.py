'''
Created on Aug 9, 2018

@author: yingc
'''
import numpy as np
import matplotlib.pyplot as plt
import math

def f_testset_word_count(testset):                                   
    '''reture the sum of words in testset which is the denominator of the formula of Perplexity'''
    return (len(testset.split()))


def graph_draw(topic,perplexity):        
    x=topic
    y=perplexity
    plt.plot(x,y,marker="*",color="red",linewidth=2)
    plt.xlabel("Number of Topic")
    plt.ylabel("Perplexity")
    plt.show()


phi = np.loadtxt('test_data/model-final.phi')
word_topic = {}
f = open('test_data/model-final.tassign')
patterns = f.read().split()
f = open('test_data/model-final.tassign')
testset_word_count = f_testset_word_count(f.read())

# ÓÃ×÷Ñ­»·
_topic=[]
perplexity_list=[]

_topic.append(10)
for pattern in patterns:
    word = int(pattern.split(':')[0])
    topic = int(pattern.split(':')[1])
    pattern = pattern.replace(':','_')
    if not word_topic.has_key(pattern)==True:
        word_topic[pattern] = phi[topic][word]

duishu = 0.0
for frequency in word_topic.values():
    duishu += -math.log(frequency)
kuohaoli = duishu/testset_word_count
perplexity = math.exp(kuohaoli)
perplexity_list.append(perplexity)

graph_draw(_topic,perplexity_list)
