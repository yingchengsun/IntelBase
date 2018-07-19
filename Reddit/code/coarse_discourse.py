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


def read_file():
    filename='coarse_discourse_dataset.json'
    file=filepath_name = os.path.join(file_dir, filename)
    count=0
    with open(file,'r+') as data_file:
        for line in data_file:
            print line
            data_item = json.loads(line, object_pairs_hook=OrderedDict) 

            #print data_item.keys()
            #print data_item['posts']
            if count>5:
                exit()
            count+=1

def read_file2():
    filename = 'coarse_discourse_dataset.json'
    filepath_name = os.path.join(file_dir, filename)
    with open(file_dir+'\\coarse_discourse\\'+'argument_data.txt','r+') as outfile:
        with open(filepath_name) as infile:
            prior = ''
            count = 0
            count2 = 0
            for line in infile:
                data_item = json.loads(line)
                posterior = data_item['subreddit']
                if 'agree' in line:
                    #outfile.write('%s'%line)
                    count+=1
                    if 'politics' in posterior:
                        print posterior
                        count2 += 1
            print count
            print count2
            '''
                if 'politics' in posterior:
                    #print data_item
                    outfile.write('%s'%line)
                if prior !=posterior:
                    prior=posterior
                    
                    #outfile.write('%s\n'%posterior)
            '''

if __name__ == '__main__':
    read_file()