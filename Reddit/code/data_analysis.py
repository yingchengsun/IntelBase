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

    submr_index_infile = open(file_dir+'\\data\\'+'r_sorted_num_comments.txt','a+')
    line_count=0
    submr_index_list=[]
    for line in submr_index_infile:
        line = line.split('\t')
        line_count+=1
        if line_count ==2:
            submr_index_list =submr_index_list+line[1].strip().lstrip('[').rstrip(']').split(',')
            break
    submr_index_list = [item.strip() for item in submr_index_list] 
    print submr_index_list
    submr_id_list=[]
    
    count=0
    filetype = 'RS_'
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
            logger.info('Processing:'+filename_id)
            logger.info('Processing:'+filename_text)
            
            #The main requirement to use this tech is all input files or lists have the same length
            with open(filename_id,'r+') as infile_id, open (filename_text,'r+') as infile_text:
                for line_id,line_text in izip(infile_id, infile_text):  
                    if str(count) in submr_index_list:
                        submr_id = line_id.strip()
                        submr_id_list.append(submr_id)
                        
                        line_text_list = line_text.rstrip('\n').split('\t')
                        title=line_text_list[1]
                        text=line_text_list[2]
                        print title,text     
                                         
                    count+=1
    submr_index_infile.close()
    print str(count)+' submission id records have been processed!'
    
    with open(file_dir+'\\data\\submr_id_list.txt','w+') as outfile_idlist:
        for item in submr_id_list:
            outfile_idlist.write(item+'\n')                 
    print 'generate_submr_id_text_list done'
    

    
    
    
def comment_network():
    """Generate the comment and its parent comment pairs given submission id
    
        Extract both id and text body of comment 
    
    """
    submr_id_list = np.genfromtxt(file_dir+'\\data\\submr_id_list.txt', dtype='S10')
   
    print submr_id_list
    
    comment_network_file = open(file_dir+'\\data\\'+'comment_network.txt','w+')
    
    count=0
    filetype = 'RC_'
    ext = '.bz2'
    for year in range(2005,2007):
        print year
        for month in range(1,13):
            if year == 2005:
                month+=11
            if month>12 or (year == 2018 and month>2):
                break
            print month
            
            prefix = filetype+str(year)+'-'+str(month).zfill(2)
            filename = file_dir+'\\data\\raw_data\\'+prefix+'_id.txt'
            logger.info('Processing:'+filename)
            
            file_object = read_file(filetype, year, month, ext)
          
            for line in file_object:
                data_item = json.loads(line, object_pairs_hook=OrderedDict)                
                if data_item['link_id'].split('_', 1)[-1] in submr_id_list:

                    comment_network_file.write((u'%s\t%s\n' %(data_item['parent_id'].split('_', 1)[-1],data_item['id'] )).encode('utf-8'))
                    print data_item['body'].encode('utf-8')
                count+=1
                if count%10000 == 0:
                    print count,' recodes have been processed!'
                
    comment_network_file.close()
    file_object.close()
  
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


    rank_num_comments()
    #num_comment_statics()
    #generate_submr_id_text_list()
    #comment_network()
    print 'All done!'

