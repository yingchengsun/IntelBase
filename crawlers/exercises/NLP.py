#coding:utf-8
'''
Created on Dec 5, 2017

@author: yingc
'''
from __future__ import print_function, unicode_literals, division

from bz2 import BZ2File
import time
import plac
import ujson

from spacy.matcher import PhraseMatcher
import spacy

from nltk import Tree


en_nlp = spacy.load('en')

doc = en_nlp("The quick brown fox jumps over the lazy dog.")

def to_nltk_tree(node):
    if node.n_lefts + node.n_rights > 0:
        return Tree(node.orth_, [to_nltk_tree(child) for child in node.children])
    else:
        return node.orth_


[to_nltk_tree(sent.root).pretty_print() for sent in doc.sents]