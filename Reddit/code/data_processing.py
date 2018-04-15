'''
Created on Apr 9, 2018

@author: yingc
'''
import bz2file
import zipfile  
import os
import json
from collections import OrderedDict
from Reddit.LDA import stop

file_dir = 'E:\\Reddit'

def ReadFile(filetype = 'RS_', year = 2005, month = 1, ext = '.bz2'):
    sub_dir = 'raw_data'
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
    filetype = 'RS_v2_'
    year = 2008
    month = 1
    ext = '.zip'

    file_object = ReadFile(filetype, year, month, ext)
    prefix = file_dir+'\\data\\'+filetype+str(year)+'-'+str(month).zfill(2)
    
    try: 
        outfile_id  = open(prefix+'_id.txt','a+')
        outfile_author = open(prefix+'_author.txt','a+')
        outfile_index_score_time_gilded_numofcomm_subreddit = open(prefix+'_index-score-time-gilded-numofcomm-subreddit.txt','a+')
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
            gilded = int(data_item['gilded'])
            numofcomm = int(data_item['num_comments'])
            gilded = int(data_item['gilded'])
            
            outfile_id.write((u'%i\t%s\n' %(index, id)).encode('utf-8'))
            outfile_author.write((u'%i\t%s\n' %(index, data_item['author'])).encode('utf-8'))
            #outfile_index_score_time_gilded_numofcomm_subreddit.write(u'%i\t%i\t%i\t%i\t%i\t%i\n' %(index, score, time, parent, submission, subreddit)).encode('utf-8'))

            if index%100000 == 0:
                print index,' recodes have been processed!'
            
            index+=1
    finally:
        file_object.close()
        outfile_id.close()
        outfile_author.close()
        outfile_index_score_time_gilded_numofcomm_subreddit.close()
        print 'In total: ' + str(index-1) +' RC recodes have been processed !'

'''
[(u'author', u'vortex30'), (u'author_flair_css_class', None), (u'author_flair_text', None), 
(u'body', u'People loooooove quoting Warren Buffett here.'), (u'can_gild', True), 
(u'controversiality', 0), (u'created_utc', 1519776000), (u'distinguished', None), (u'edited', 1519776490), 
(u'gilded', 0), (u'id', u'duxmu9j'), (u'is_submitter', False), (u'link_id', u't3_80pua7'), (u'parent_id', u't1_duxkd5c'), 
(u'permalink', u'/r/weedstocks/comments/80pua7/maricann_faces_osc_scrutiny_over_bought_deal/duxmu9j/'), (u'retrieved_on', 1520324632), 
(u'score', 3), (u'stickied', False), (u'subreddit', u'weedstocks'), (u'subreddit_id', u't5_2zfqj'), (u'subreddit_type', u'public')])
'''
def RC():
    filetype = 'RC_'
    year = 2008
    month = 1
    ext = '.bz2'
    file_object = ReadFile(filetype, year, month, ext)
    prefix = file_dir+'\\data\\'+filetype+str(year)+'-'+str(month).zfill(2)
    try: 
        #outfile_body = open(prefix+'_body.txt','a+')
        outfile_index_id  = open(prefix+'_id.txt','a+')
        outfile_index_author = open(prefix+'_author.txt','a+')
        outfile_index_score_time_parent_submission_subreddit = open(prefix+'_index-score-time-parent-submission-subreddit.txt','a+')
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
        outfile_index_score_time_parent_submission_subreddit.close()
        print 'In total: ' + str(index-1) +' RC recodes have been processed !'

    

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
    sub_dir = 'raw_data'
    filename = 'subreddits.zip'
    filepath_name = os.path.join(file_dir, sub_dir, filename)
    infile = zipfile.ZipFile(filepath_name, "r")
    file_object = infile.open(infile.getinfo(infile.namelist()[0]))

    try: 
        #outfile_index_title_description = open(file_dir+'\\data\\subreddits_index-title-publicDescription.txt','a+')
        outfile_index_id = open(file_dir+'\\data\\subreddits_index-id.txt','a+')
        outfile_index_dname_subscribers_time = open(file_dir+'\\data\\subreddits_index-dname-subscribers-time.txt','a+')
        index = 1
        for line in file_object:
            data_item = json.loads(line, object_pairs_hook=OrderedDict)
            '''
            title = data_item['title']
            if title:
                title =' '.join(data_item['title'].split())
               
            public_description = data_item['public_description']
            if public_description:
                public_description =' '.join(data_item['public_description'].split())    
            '''
            if data_item['subscribers']:
                subscribers = int(data_item['subscribers'])
            time = int(data_item['created_utc'])
        
            #outfile_index_title_description.write((u'%i\t%s\t%s\n' %(index, title, public_description )).encode('utf-8'))
            outfile_index_id.write((u'%i\t%s\n' %(index, data_item['id'])).encode('utf-8'))
            #outfile_index_dname_subscribers_time.write((u'%i\t%s\t%i\t%i\n' %(index, data_item['display_name'].strip('\n'), subscribers, time)).encode('utf-8'))
            
            if index%100000 == 0:
                print index,' recodes have been processed!'
            index+=1
            
    finally:
        file_object.close()
        #outfile_index_title_description.close()
        outfile_index_id.close()
        outfile_index_dname_subscribers_time.close()
    print 'In total: ' + str(index-1) +' subreddits recodes have been processed !'


if __name__ == "__main__":
    #RS()
    #RC()
    Subreddits()
