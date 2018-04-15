'''
Created on Apr 4, 2018

@author: yingc
'''
import json
import networkx as nx
import matplotlib.pyplot as plt
from collections import OrderedDict

def Topic():
    data = []
    count = 0
    with open('E:\\Reddit\\RC_2018-02-28','r') as raw_data_file:
       
        for line in raw_data_file:
            data_item = json.loads(line, object_pairs_hook=OrderedDict)
            if data_item['link_id'].split('_', 1)[-1] == '80rgsx':
                document = (data_item['body'].encode('utf-8'))
                print document
                data.append(document)
                count+=1
                if count%10 == 0:
                    print count,' recodes have been processed!'
                if count > 50:
                    break
    print len(data)
    print data
       




if __name__ == '__main__':
    
    Topic()
    
    print 'All done!'