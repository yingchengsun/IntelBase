'''
Created on Apr 19, 2018

@author: yingc
'''
import json
import numpy as np
import bz2file
import zipfile  
import os
from collections import OrderedDict
import logging
from itertools import izip  

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
    
def rank_num_comments():
    """Rank submissions by the number of its comments, and group submissions by their number of comments
    
    """
    
    num_comments_file_dict={}
    k_num_comments_dict={}
    k=20
    for i in range(k+1):
        num_comments_file_dict[i] = open(file_dir+'\\data\\num_comments\\'+str(i)+'_num_comments.txt','w+')
        k_num_comments_dict[i] = 0
    
    num_comments_dict=OrderedDict()
    
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
            
            with open(filename,'r+') as infile:
                for line in infile:
                    subm_matrix = line.rstrip('\n').split('\t')
                    num_comments = int(subm_matrix[4])
                    
                    if 0<=num_comments <= k:
                        num_comments_file_dict[num_comments].write(subm_matrix[0]+'\n')
                        k_num_comments_dict[num_comments]+=1
                    elif num_comments>0:
                        index = int(subm_matrix[0])
                        if not num_comments_dict.has_key(num_comments):
                            num_comments_dict[num_comments]=set([index])
                        else:
                            num_comments_dict[num_comments].add(index)
                
    sorted_dict= OrderedDict(sorted(num_comments_dict.items(),key = lambda t:t[0]))
    sorted_dict_reversed= OrderedDict(sorted(num_comments_dict.items(),key = lambda t:-t[0]))
    logger.info('Subtotal for'+ str(len(sorted_dict)) +'different numbers of comments!')
    
    sorted_k_dict= OrderedDict(sorted(k_num_comments_dict.items(),key = lambda t:t[0]))
    
    with open(file_dir+'\\data\\num_comments\\'+'sorted_num_comments_count.txt','w+') as outfile:
        for key,value in sorted_k_dict.items():
            #print key, value
            outfile.write('%i\t%i\n' %(key,value))
        
        for key,value in sorted_dict.items():
            outfile.write('%i\t%i\n' %(key,len(value)))
       
    for i in range(k+1):
        num_comments_file_dict[i].close()

    with open(file_dir+'\\data\\num_comments\\'+'r_sorted_num_comments.txt','w+') as outfile:
        for key,value in sorted_dict_reversed.items():
            #print key, value
            outfile.write('%i\t%s\n' %(key,list(value)))
    print 'Rank number of comments done!'


        
def generate_submr_id_text_list():
    """Generate submission id list and corresponding title and text given its index
    
    """

    infile_submr_index = open(file_dir+'\\data\\num_comments\\'+'r_sorted_num_comments.txt','r+')
    line_count=0
    submr_index_list=[]
    for line in infile_submr_index:
        line = line.split('\t')
        submr_index_list =submr_index_list+line[1].strip().lstrip('[').rstrip(']').split(',')
        line_count+=1
        if line_count ==20:
            break
    submr_index_list = [item.strip() for item in submr_index_list] 
    print submr_index_list
    
    infile_subr_id = open(file_dir+'\\data\\'+'subreddits_id.txt','r+')
    subr_id_list = infile_subr_id.readlines()
    
    outfile_idlist = open(file_dir+'\\data\\submr_allinfo_list.txt','w+')
    
    count=0
    filetype = 'RS_'
    index_old = index ='0'
    for year in range(2005,2006):
        print year
        for month in range(1,13):
            if year == 2005:
                month+=5
            if month>12 or (year == 2018 and month>2):
                break
            print month
            
            prefix = filetype+str(year)+'-'+str(month).zfill(2)
            filename_id = file_dir+'\\data\\RS_id\\'+prefix+'_id.txt'
            filename_text = file_dir+'\\data\\\RS_title_text\\'+prefix+'_index-title-text.txt'
            filename_matrix = file_dir+'\\data\\\\RS_matrix\\'+prefix+'_index-score-time-gilded-num_comments-subreddit.txt'
            
            logger.info('Processing:'+filename_id)
            logger.info('Processing:'+filename_text)
            logger.info('Processing:'+filename_matrix)
            
            
            #The main requirement to use this tech is all input files or lists have the same length
            with open(filename_id,'r+') as infile_id, open (filename_text,'r+') as infile_text, open (filename_matrix,'r+') as infile_matrix:
                for line_id,line_text,line_matrix in izip(infile_id, infile_text,infile_matrix): 
                    line_matrix_list = line_matrix.rstrip('\n').split('\t')

                    index_old=index

                    index = line_matrix_list[0] 
                    if int(index_old)!= int(index)-1:
                        
                        print 'index_old',index_old
                        print 'index',index
                        
                    #if str(count) in submr_index_list:
                    if index in submr_index_list:
                        submr_id = line_id.strip()
                        outfile_idlist.write(submr_id)
                        outfile_idlist.write('\t')
                        
                        line_text_list = line_text.rstrip('\n').split('\t')
                        title=line_text_list[1]
                        text=line_text_list[2]
                        outfile_idlist.write(title+'\t'+text)  
                        outfile_idlist.write('\t')
                        
                        line_matrix_list = line_matrix.rstrip('\n').split('\t')

                        #index = line_matrix_list[0]
                        score = line_matrix_list[1]
                        time = line_matrix_list[2]
                        gilded = line_matrix_list[3]
                        num_comments = line_matrix_list[4]
                        subreddit  = int(line_matrix_list[5])
                        outfile_idlist.write(line_matrix.rstrip('\n')) 
                        outfile_idlist.write('\t')
                        outfile_idlist.write(subr_id_list[subreddit]) 

                    count+=1
                    
    infile_submr_index.close()
    infile_subr_id.close()
    outfile_idlist.close()
    
    print str(count)+' submission id records have been processed!'
          
    print 'generate_submr_id_text_list done'
    

    
    
    
def comment_network():
    """Generate the comment and its parent comment pairs given submission id
    
        Extract both id and text body of comment 
    
    """
    #submr_id_list = np.genfromtxt(file_dir+'\\data\\submr_id_list.txt', dtype='S10')
    infile_sid = open(file_dir+'\\data\\submr_id_list.txt','r+')
    submr_id_list = infile_sid.readlines()
    submr_id_list = [item.rstrip('\n') for item in submr_id_list] 
    print submr_id_list
    
    #comment_network_file = open(file_dir+'\\data\\comment_network\\'+'comment_network.txt','w+')
    outfile_dict={}
    for id in submr_id_list:
        outfile_dict[id] = open(file_dir+'\\data\\comment_network\\'+id+'.txt','w+')
    
    count=0
    filetype = 'RC_'
    ext = '.bz2'
    for year in range(2010,2019):
        print year
        for month in range(1,13):
            if year == 2010:
                month+=7
            if month>12 or (year == 2018 and month>2):
                break
            if (year == 2017 and month==12) or (year == 2018):
                ext = '.zip'
                
            print month
            
            prefix = filetype+str(year)+'-'+str(month).zfill(2)
        
            logger.info('Processing:'+filetype+prefix+ext)
            
            file_object = read_file(filetype, year, month, ext)
          
            for line in file_object:
                data_item = json.loads(line, object_pairs_hook=OrderedDict)           
                sid = data_item['link_id'].split('_', 1)[-1]     
                if sid in submr_id_list:
                    print sid
                    cid=data_item['id']
                    pid=data_item['parent_id'].split('_', 1)[-1]
                    
                    if not data_item.has_key('author') or not data_item['author']:
                        author = ''
                    else:
                        author = data_item['author']
                    
                    body = data_item['body']
                    if body:
                        body=' '.join(data_item['body'].split())
                    
                    time = int(data_item['created_utc'])
                    
                    if not data_item.has_key('controversiality') or not data_item['controversiality']:
                        controversiality = 0
                    else:
                        controversiality = int(data_item['controversiality'])
                    
                    
                    if not data_item.has_key('score') or not data_item['score']:
                        score = 0
                    else:
                        score = int(data_item['score'])
                    
                    if not data_item.has_key('gilded') or not data_item['gilded']:
                        gilded = 0
                    else:
                        gilded = int(data_item['gilded'])
                    
                    
                    outfile_dict[sid].write((u'%s\t%s\t%i\t%i\t%i\t%i\t%s\t%s\n' %(cid, pid, time, controversiality, score, gilded, author, body )).encode('utf-8'))
                   
                count+=1
                if count%10000 == 0:
                    print count,' recodes have been processed!'
                
    #comment_network_file.close()
            file_object.close()
            
    infile_sid.close()
    for id in submr_id_list:
        outfile_dict[id].close()
  
    print 'comment network done!'

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


    #rank_num_comments()
    #num_comment_statics()
    generate_submr_id_text_list()
    #comment_network()
    print 'All done!'

