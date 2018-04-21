'''
Created on Apr 19, 2018

@author: yingc
'''
import json
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from collections import OrderedDict
import logging

file_dir = 'E:\\Reddit'
    
def rank_num_comments():
    
    num_comments_dict=OrderedDict()
    Zero_num_comments = open(file_dir+'\\data\\'+'Zero_num_comments.txt','a+')
    filetype = 'RS_'
    for year in range(2005,2006):
        print year
        for month in range(1,13):
            if year == 2005:
                month+=5
            if month>12 or (year == 2018 and month>2):
                break
            print month
            #RS_2007-03_index-score-time-gilded-num_comments-subreddit
            prefix = filetype+str(year)+'-'+str(month).zfill(2)
            filename = file_dir+'\\data\\RS_matrix\\'+prefix+'_index-score-time-gilded-num_comments-subreddit.txt'
            logger.info('Processing:'+filename)
            ndtype = 'i,i,i,i,i,i' 
            names='index, score, time, gilded, num_comments, subreddit_id'
            subm_matrix = np.genfromtxt(filename, dtype=ndtype, names=names, delimiter='\t')
            with open(filename,'r+') as infile:
                for line in infile:
                    subm_matrix = line.rstrip('\n').split('\t')
                    num_comments = int(subm_matrix[4])
                    
                    if num_comments == 0:
                        Zero_num_comments.write(subm_matrix[0]+'\n')
                    else:
                        index = int(subm_matrix[0])
                        if not num_comments_dict.has_key(num_comments):
                            num_comments_dict[num_comments]=set([index])
                        else:
                            num_comments_dict[num_comments].add(index)
                
    sorted_dict= OrderedDict(sorted(num_comments_dict.items(),key = lambda t:-t[0]))
    Zero_num_comments.close()
    
    with open(file_dir+'\\data\\'+'sorted_num_comments.txt','w+') as outfile:
        for key,value in sorted_dict.items():
            #print key, value
            outfile.write('%i\t%s\n' %(key,list(value)))
    
        
def RS():
    #threshold of number of comments
    th_num_comments = 100
    th_num_records = 1000
    count = 0
    with open('E:\\Reddit\\RS_2018-02-28','r') as raw_data_file:
        new_data_file = open('E:\\Reddit\\submission_topic.txt','a+')
        new_data_file2 = open('E:\\Reddit\\submission.txt','a+')
        for line in raw_data_file:
            data_item = json.loads(line, object_pairs_hook=OrderedDict)
    
            #score = data_item['score']
            if data_item['num_comments'] >= th_num_comments:
                #new_data_file.write((u'%s\t%s\n' %(data_item['id'], data_item['title'] )).encode('utf-8'))
                new_data_file2.write((u'%s\n' %(data_item['id'] )).encode('utf-8'))
                count+=1
                if count % 100 == 0:
                    print count,' recodes have been processed!'
                if count > th_num_records:
                    break
            
    new_data_file2.close()
    print 'RS done!'


def RC():
    th_num_records = 1000
    s_with_c_over_100=[]
    count = 0
    with open('E:\\Reddit\\submission.txt','r') as ps:
        for line in ps:
            line = line.strip('\n')
            s_with_c_over_100.append(line)
        
    with open('E:\\Reddit\\RC_2018-02-28','r') as raw_data_file:
        new_data_file = open('E:\\Reddit\\parent_comment.txt','a+')
      
        for line in raw_data_file:
            data_item = json.loads(line, object_pairs_hook=OrderedDict)
            if data_item['link_id'].split('_', 1)[-1] in s_with_c_over_100:
                new_data_file.write((u'%s\t%s\n' %(data_item['parent_id'].split('_', 1)[-1],data_item['id'] )).encode('utf-8'))
                count+=1
                if count%100 == 0:
                    print count,' recodes have been processed!'
                if count > th_num_records:
                    break
        new_data_file.close()
    raw_data_file.close()
  
    print 'RC done!'

def Comment():
    th_num_records = 100
    s_with_c_over_100=[]
    count = 0
    with open('E:\\Reddit\\submission.txt','r') as ps:
        for line in ps:
            line = line.strip('\n')
            s_with_c_over_100.append(line)
    print s_with_c_over_100[0]       
      
    with open('E:\\Reddit\\RC_2018-02-28','r') as raw_data_file:
        new_data_file = open('E:\\Reddit\comments.txt','a+')
        
        for line in raw_data_file:
            data_item = json.loads(line, object_pairs_hook=OrderedDict)
            if data_item['link_id'].split('_', 1)[-1] == s_with_c_over_100[0]:
                new_data_file.write((u'%s\n' %(data_item['body'] )).encode('utf-8'))
                count+=1
                if count%10 == 0:
                    print count,' recodes have been processed!'
                if count > th_num_records:
                    break
        new_data_file.close()
    raw_data_file.close()
    
    print 'Comment done!'

    
def Subreddits():
    count = 0
    with open('E:\\Reddit\\subreddits','r') as raw_data_file:
        new_data_file = open('E:\\Reddit\\subreddits_title.txt','a+')
        for line in raw_data_file:
            print line
            data_item = json.loads(line, object_pairs_hook=OrderedDict)
            new_data_file.write((u'%s\t%s\n' %(data_item['name'],data_item['title'] )).encode('utf-8'))
            count+=1
            if count%100 == 0:
                print count,' recodes have been processed!'
            if count>1000:
                break
    new_data_file.close()
    print 'Subreddits done!'


    
if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(file_dir+'\\data\\logs\\'+'reddit_data_prepocessing.log')
    handler.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
    handler.setFormatter(formatter)
     
    logger.addHandler(handler)
    logger.info('starts!')
    #RS()
    #RC()
    #Subreddits()

    #Comment()
    rank_num_comments()
    
    print 'All done!'

