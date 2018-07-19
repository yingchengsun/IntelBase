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
                    


if __name__ == '__main__':
    argument_extr()