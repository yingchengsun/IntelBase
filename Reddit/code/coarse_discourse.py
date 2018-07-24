'''
Created on Jul 19, 2018

@author: yingc
'''
import json
import numpy as np

import os
from collections import OrderedDict
import logging

import codecs
file_dir = 'E:\\Reddit'


def argument_extr():
    filename='coarse_discourse_dataset.json'
    filepath_name = os.path.join(file_dir, 'data','coarse_discourse',filename)
   
    with open(file_dir+'\\coarse_discourse\\'+'argument_data.txt','w+') as outfile:
        with open(filepath_name,'r') as infile:
            count=0
            for line in infile:
                print line
                #data_item = json.loads(line, object_pairs_hook=OrderedDict) 
                if 'agree' in line:
                    outfile.write('%s'%line)
                    count+=1
            print count
                    

'''
data_item.keys()
[u'subreddit', u'is_self_post', u'url', u'title', u'posts']

data_item['posts'][0].keys()
[u'id', u'annotations', u'majority_link', u'majority_type', u'is_first_post']

data_item['posts'][1].keys() 
[u'in_reply_to', u'post_depth', u'id', u'majority_link', u'annotations']
or
[u'in_reply_to', u'post_depth', u'id', u'majority_link', u'majority_type', u'annotations']

'''
def annotations_extr():
    filename='argument_data.txt'
    filepath_name = os.path.join(file_dir, 'data','coarse_discourse',filename)
    with open(filepath_name,'r') as infile:
        count=0
        for line in infile:
            data_item = json.loads(line, object_pairs_hook=OrderedDict) 
            
            #print len(data_item['posts'])
            for post in data_item['posts']:
                for annotation in post['annotations']:
                    #for annotation_item in annotation
                    if annotation['main_type'] == 'agreement':
                        print post
            count+=1
            if count>0:
                exit()
    
if __name__ == '__main__':
    #argument_extr()
    annotations_extr()
