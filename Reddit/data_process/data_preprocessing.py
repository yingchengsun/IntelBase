# -*- coding:utf-8 -*-
'''
Created on Apr 9, 2018

@author: yingc
'''
import bz2file
import zipfile  
import os
import json
from collections import OrderedDict
import numpy as np
import logging


file_dir = 'E:\\Reddit'

def read_file(filetype, year, month, ext):
    """ Read compressed file and return a file object
    
        Args: 
            filetype = 'RS_', year = 2005, month = 1
            ext: can be .bz2 or .zip format
        Returns:
            file object which can be read by iteration
    """
    
    sub_dir = 'raw_data'
    if str(year).strip() == '' and str(month).strip() =='':
        filename = filetype + ext
    else:
        filename = filetype + str(year) + '-' + str(month).zfill(2) + ext
    filepath_name = os.path.join(file_dir, sub_dir, filename)
    
    if ext =='.bz2':
        file_object = bz2file.open(filepath_name,'r')
    elif ext =='.zip':
        infile = zipfile.ZipFile(filepath_name, "r")
        file_object = infile.open(infile.getinfo(infile.namelist()[0]))
    else:
        return NameError
    return file_object




'''
Subreddit JSON file format

[(u'header_img', u'http://a.thumbs.redditmedia.com/gq9561mrzeY9TrVx.png'), (u'submit_link_label', u'Submit a new post'),
 (u'name', u't5_2qgzg'), (u'description', u'/r/business brings you the best of your business section.'), (u'suggested_comment_sort', None), 
 (u'subscribers', 201926), (u'header_title', u'/r/business brings you the best of your business section.'), (u'header_size', [1, 1]), 
 (u'public_traffic', False), (u'description_html', u'a href="/r/business"&gt;\gt'),(u'title', u'business'), 
 (u'subreddit_type', u'public'), (u'url', u'/r/business/'), (u'wiki_enabled', False), (u'submission_type', u'any'), 
 (u'public_description_html', u'&lt;!-- SC_OFF --&gt;&lt'), (u'comment_score_hide_mins', 0), (u'quarantine', False), 
 (u'display_name', u'business'), (u'collapse_deleted_comments', False), (u'banner_img', u''), (u'over18', False)]
'''
        
def Subreddits():
    """ Extract subreddit fields useful for our research from raw dataset
    
        Extract subreddit id into 'subreddits_id.txt'
            title and publicDescription into 'subreddits_index-title-publicDescription.txt'
            display name, subscribers and time into 'subreddits_index-displayname-subscribers-time.txt'
            
    """
    file_object = read_file(filetype='subreddits', year='', month='', ext='.zip')
    
    logger.info('Processing: subreddits')
    try: 
        #outfile_id = open(file_dir+'\\data\\subreddits_id.txt','a+')
        outfile_index_title_description = open(file_dir+'\\data\\subreddits_title-publicDescription.txt','a+')
        #outfile_index_title_description = open(file_dir+'\\data\\subreddits_index-title-publicDescription.txt','a+')
        #outfile_index_displayname_subscribers_time = open(file_dir+'\\data\\subreddits_index-displayname-subscribers-time.txt','a+')
        index = 0
        for line in file_object:
            data_item = json.loads(line, object_pairs_hook=OrderedDict)
            
            title = data_item['title']
            if title:
                title =' '.join(data_item['title'].split())
               
            public_description = data_item['public_description']
            
            if public_description:
                public_description =' '.join(data_item['public_description'].split())    
            
            if data_item['subscribers']:
                subscribers = int(data_item['subscribers'])
                
            time = int(data_item['created_utc'])
            
            #outfile_id.write((u'%s\n' %(data_item['id'])).encode('utf-8'))
            #outfile_index_title_description.write((u'%i\t%s\t%s\n' %(index, title, public_description )).encode('utf-8'))
            outfile_index_title_description.write((u'%s ' %(title)).encode('utf-8'))
            #outfile_index_displayname_subscribers_time.write((u'%i\t%s\t%i\t%i\n' %(index, data_item['display_name'].strip('\n'), subscribers, time)).encode('utf-8'))
            
            index+=1
            if index%100000 == 0:
                logger.info(str(index)+' recodes have been processed!')
                print index,' recodes have been processed!'
                            
    finally:
        file_object.close()
        #outfile_id.close()
        outfile_index_title_description.close()
        #outfile_index_displayname_subscribers_time.close()
        logger.info('By now, '+str(index)+' recodes have been processed!')
        print 'In total: ' + str(index) +' subreddits recodes have been processed !'
    

'''
Reddit Submission JSON data format:

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
    """ Extract submission fields useful for our current research from raw dataset
    
        Extract submission id into 'RS_date_id.txt'
            index and author into 'RS_date_index-author.txt'
            index, title, selftext into 'RS_date_index-title-text.txt'
            index, score, created_utc, gilded, num_comments, subreddit_id into 'RS_date_index-score-time-gilded-num_comments-subreddit.txt'
        Meanwhile, update the subreddit id list and its file when some new subreddits come out
    """

    filetype = 'RS_'
    #ext = '.zip'
    ext = '.bz2'
    subm_index = open(file_dir+'\\data\\'+'subm_index.txt','a+')
    temp = subm_index.readlines()
    if temp ==[]:
        index = 0
    else:
        index = int(temp[-1])
        
    for year in range(2013,2014):
        for month in range(2,3):
            
            #file_object = read_file(filetype+'V2_', year, month, ext)
            file_object = read_file(filetype, year, month, ext)
            prefix = filetype+str(year)+'-'+str(month).zfill(2)
            
            logger.info('Processing:'+prefix)
            try: 
                infile_subr_id = np.genfromtxt(file_dir+'\\data\\'+'subreddits_id.txt', dtype='S10')
                outfile_new_subr_id = open(file_dir+'\\data\\'+'subreddits_id.txt','a+')
                outfile_new_subr_dname = open(file_dir+'\\data\\subreddits_new\\'+prefix+'_new_subr-index-dname.txt','a+')
                
                outfile_subm_id  = open(file_dir+'\\data\\RS_id\\'+prefix+'_id.txt','a+')
                outfile_subm_author = open(file_dir+'\\data\\RS_author\\'+prefix+'_index-author.txt','a+')
                outfile_subm_title_text = open(file_dir+'\\data\\RS_title_text\\'+prefix+'_index-title-text.txt','a+')
                outfile_subm_score_time_gilded_numofcomm_subreddit = open(file_dir+'\\data\\RS_matrix\\'+prefix+'_index-score-time-gilded-num_comments-subreddit.txt','a+')
                    
                subr_id_len = len(infile_subr_id)
                ids = dict(zip(infile_subr_id,range(subr_id_len)))
                
                count=0
                for line in file_object:
                    
                    line = line.decode('utf-8').replace('\0', '')
                    data_item = json.loads(line)
                    
                    if not data_item.has_key('subreddit_id') or not data_item['subreddit_id']:
                        subreddit_id = '0'
                        subreddit_name='0'
                    else:
                        subreddit_id = (data_item['subreddit_id'].split('_', 1)[-1]).encode('utf-8')
                        subreddit_name=data_item['subreddit']

                    
                    if not ids.has_key(subreddit_id):
                        outfile_new_subr_id.write(subreddit_id+'\n')
                        outfile_new_subr_dname.write((u'%i\t%s\n' %(subr_id_len, subreddit_name)).encode('utf-8'))
                        ids[subreddit_id]=subr_id_len
                        subr_id_len+=1
                    
                    if not data_item.has_key('score') or not data_item['score']:
                        score = 0
                    else:
                        score = int(data_item['score'])
                        
                    time = int(data_item['created_utc'])
                    numofcomm = int(data_item['num_comments'])
                    
                    if data_item.has_key('gilded'):
                        gilded = int(data_item['gilded'])
                    else:
                        gilded=0
                   
                    if data_item.has_key('author'):
                        author = data_item['author']
                    else:
                        author=''
                        
                    title = data_item['title']
                    if title:
                        title =' '.join(data_item['title'].split())
                    text = data_item['selftext']
                    
                    if text:
                        text =' '.join(data_item['title'].split())
                    
                    outfile_subm_id.write((u'%s\n' %(data_item['id'])).encode('utf-8'))
                    outfile_subm_author.write((u'%i\t%s\n' %(index, author)).encode('utf-8'))
                    outfile_subm_title_text.write((u'%i\t%s\t%s\n' %(index, title, text )).encode('utf-8'))
                    outfile_subm_score_time_gilded_numofcomm_subreddit.write((u'%i\t%i\t%i\t%i\t%i\t%i\n' %(index, score, time, gilded, numofcomm, ids[subreddit_id])).encode('utf-8'))
                    
                    count+=1
                    index+=1
                    if index%10000 == 0:
                        logger.info(str(index)+' recodes have been processed!')
                        print index,' recodes have been processed!'
              
            finally:
                              
                file_object.close()
                
                outfile_new_subr_id.close()
                outfile_new_subr_dname.close()
                
                outfile_subm_id.close()
                outfile_subm_author.close()
                outfile_subm_title_text.close()
                outfile_subm_score_time_gilded_numofcomm_subreddit.close()
                
                logger.info('Done: ' + str(count) +' RS recodes have been processed !')
                logger.info('By now, '+str(index)+' recodes have been processed!')
                print prefix+' done: ' + str(count) +' RS recodes have been processed !'
    
    subm_index.write(str(index))
    subm_index.close()


'''
Reddit Comment JSON data format:

[(u'author', u'vortex30'), (u'author_flair_css_class', None), (u'author_flair_text', None), 
(u'body', u'People loooooove quoting Warren Buffett here.'), (u'can_gild', True), 
(u'controversiality', 0), (u'created_utc', 1519776000), (u'distinguished', None), (u'edited', 1519776490), 
(u'gilded', 0), (u'id', u'duxmu9j'), (u'is_submitter', False), (u'link_id', u't3_80pua7'), (u'parent_id', u't1_duxkd5c'), 
(u'permalink', u'/r/weedstocks/comments/80pua7/maricann_faces_osc_scrutiny_over_bought_deal/duxmu9j/'), (u'retrieved_on', 1520324632), 
(u'score', 3), (u'stickied', False), (u'subreddit', u'weedstocks'), (u'subreddit_id', u't5_2zfqj'), (u'subreddit_type', u'public')])
'''
def RC():
    """ Extract comment fields useful for our current research from raw dataset
    
        Extract comment id into 'RC_date_id.txt'
            index and author into 'RC_date_index-author.txt'
            index, body into 'RS_date_index-body.txt'
            index, score, created_utc, parent_id, link_id, subreddit_id into 'RS_date_index-score-time-gilded-num_comments-subreddit.txt'
        Meanwhile, update the subreddit id list and its file when some new subreddits come out
    """
    filetype = 'RC_'
    year = 2008
    month = 1
    ext = '.bz2'
    file_object = read_file(filetype, year, month, ext)
    prefix = file_dir+'\\data\\'+filetype+str(year)+'-'+str(month).zfill(2)
    try: 
        #outfile_body = open(prefix+'_body.txt','a+')
        outfile_index_id  = open(prefix+'_id.txt','a+')
        outfile_index_author = open(prefix+'_author.txt','a+')
        outfile_index_score_controv_time_parent_subm = open(prefix+'_index-score-controv-time-parent-subm.txt','a+')
        index = 1
        for line in file_object:
            data_item = json.loads(line, object_pairs_hook=OrderedDict)
            '''
            body = data_item['body']
            if body:
                body =' '.join(data_item['body'].split())
            '''
            score = int(data_item['score'])
            time = int(data_item['created_utc'])
            id = data_item['id']
            #outfile_body.write((u'%i\t%s\n' %(count, body)).encode('utf-8'))
            outfile_index_id.write((u'%i\t%s\n' %(index, id)).encode('utf-8'))
            outfile_index_author.write((u'%i\t%s\n' %(index, data_item['author'])).encode('utf-8'))
            #outfile_index_score_time_parent_submission_subreddit.write(u'%i\t%i\t%i\t%i\t%i\t%i\n' %(index, score, time, parent, submission, subreddit)).encode('utf-8'))
            if index%100000 == 0:
                print index,' recodes have been processed!'
            
            index+=1
    finally:
        file_object.close()
        #outfile_body.close()
        outfile_index_id.close()
        outfile_index_author.close()
        outfile_index_score_controv_time_parent_subm.close()
        print 'In total: ' + str(index-1) +' RC recodes have been processed !'

    
if __name__ == "__main__":
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(file_dir+'\\data\\logs\\'+'reddit_data_prepocessing.log')
    handler.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
    handler.setFormatter(formatter)
     
    logger.addHandler(handler)
    logger.info('starts!')
    
    #RS()
    #RR()
    #RC()
    Subreddits()
