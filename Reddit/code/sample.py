#!/usr/bin/env python
#coding:utf-8
'''
Created on Mar 23, 2018

@author: yingc
'''
import json
import networkx as nx
import matplotlib.pyplot as plt
from collections import OrderedDict
from scipy.stats.mstats_basic import threshold

'''
[(u'archived', False), (u'author', u'ThucydidesJones'), (u'author_flair_css_class', None), (u'author_flair_text', None), 
(u'brand_safe', False), (u'contest_mode', False), (u'created_utc', 1519776000), (u'distinguished', None), (u'domain', u'self.xdag'), 
(u'edited', 1519776189.0), (u'gilded', 0), (u'hidden', False), (u'hide_score', False), (u'id', u'80rgry'), (u'is_crosspostable', False), 
(u'is_reddit_media_domain', False), (u'is_self', True), (u'is_video', False), (u'link_flair_css_class', None), (u'link_flair_text', None), 
(u'locked', False), (u'media', None), (u'media_embed', OrderedDict()), (u'no_follow', True), (u'num_comments', 6), (u'num_crossposts', 0), 
(u'over_18', False), (u'parent_whitelist_status', None), (u'permalink', u'/r/xdag/comments/80rgry/new_miner_in_town_should_i_use_cpu_or_gpu/'), 
(u'pinned', False), (u'retrieved_on', 1520606335), (u'score', 2), (u'secure_media', None), (u'secure_media_embed', OrderedDict()), 
(u'selftext', u"i7 3820 or\nGTX 1080 FTW\n\nI'm mining via CPU right now since that was easier to set up, but would I be better of utilizing the GPU?"), 
(u'send_replies', True), (u'spoiler', False), (u'stickied', False), (u'subreddit', u'xdag'), (u'subreddit_id', u't5_bxyiw'), 
(u'subreddit_type', u'public'), (u'suggested_sort', None), (u'thumbnail', u'self'), (u'thumbnail_height', None), (u'thumbnail_width', None), 
(u'title', u'New miner in town, should I use CPU or GPU?'), (u'url', u'https://www.reddit.com/r/xdag/comments/80rgry/new_miner_in_town_should_i_use_cpu_or_gpu/'), 
(u'whitelist_status', None)]
'''

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

'''
[(u'author', u'vortex30'), (u'author_flair_css_class', None), (u'author_flair_text', None), 
(u'body', u'People loooooove quoting Warren Buffett here.'), (u'can_gild', True), 
(u'controversiality', 0), (u'created_utc', 1519776000), (u'distinguished', None), (u'edited', 1519776490), 
(u'gilded', 0), (u'id', u'duxmu9j'), (u'is_submitter', False), (u'link_id', u't3_80pua7'), (u'parent_id', u't1_duxkd5c'), 
(u'permalink', u'/r/weedstocks/comments/80pua7/maricann_faces_osc_scrutiny_over_bought_deal/duxmu9j/'), (u'retrieved_on', 1520324632), 
(u'score', 3), (u'stickied', False), (u'subreddit', u'weedstocks'), (u'subreddit_id', u't5_2zfqj'), (u'subreddit_type', u'public')])
'''
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

'''
[(u'header_img', u'http://a.thumbs.redditmedia.com/gq9561mrzeY9TrVx.png'), (u'submit_link_label', u'Submit a new post'),
 (u'name', u't5_2qgzg'), (u'description', u'/r/business brings you the best of your business section.'), (u'suggested_comment_sort', None), 
 (u'subscribers', 201926), (u'header_title', u'/r/business brings you the best of your business section.'), (u'header_size', [1, 1]), 
 (u'public_traffic', False), (u'description_html', u'a href="/r/business"&gt;\gt'),(u'title', u'business'), 
 (u'subreddit_type', u'public'), (u'url', u'/r/business/'), (u'wiki_enabled', False), (u'submission_type', u'any'), 
 (u'public_description_html', u'&lt;!-- SC_OFF --&gt;&lt'), (u'comment_score_hide_mins', 0), (u'quarantine', False), 
 (u'display_name', u'business'), (u'collapse_deleted_comments', False), (u'banner_img', u''), (u'over18', False)]
'''
    
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

def Visualize():
    edges=[]
    count = 0
    with open('E:\\Reddit\\data\\parent_comment.txt','r') as ps:
        for line in ps:
            edge = line.split('\t')
            edge[1] = edge[1].strip('\n')
            edges.append(edge)
            count+=1
            if count >1000:
                break
    print edges    
    g = nx.graph(edges)
    nx.draw_networkx(g)
    plt.show()

if __name__ == '__main__':
    #RS()
    #RC()
    #Subreddits()
    Visualize()
    #Comment()
    
    print 'All done!'
