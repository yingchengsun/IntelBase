'''
Created on Jul 19, 2018

@author: yingc
'''
import json
import numpy as np

import os
from collections import OrderedDict
import logging

from data_preprocessing import read_file



file_dir = 'E:\\Reddit'


def argument_extr():
    """ Extract data from raw data file with argument(agreement/disagreement) annotation
        
        argument_data_loose: posts with at least one argument annotation within all its comments
        argument_data_tight: posts with all comments having argument annotation (not the majority annotation, as long as one argument within three annotations ) 
        data_anno: majority annotations for posts their comments
       
        Data Format: 
        
        data_item.keys()
        [u'subreddit', u'is_self_post', u'url', u'title', u'posts']
        
        data_item['posts'][0].keys()
        [u'id', u'annotations', u'majority_link', u'majority_type', u'is_first_post']
        
        data_item['posts'][1].keys() 
        [u'in_reply_to', u'post_depth', u'id', u'majority_link', u'annotations']
        or
        [u'in_reply_to', u'post_depth', u'id', u'majority_link', u'majority_type', u'annotations']

    
    """
    filename='coarse_discourse_dataset.json'
    filepath_name = os.path.join(file_dir, 'data','coarse_discourse',filename)
    data_anno = open(file_dir+'\\data\\coarse_discourse\\'+'data_anno.txt','w+') 
    with open(file_dir+'\\data\\coarse_discourse\\'+'argument_data_tight.txt','w+') as outfile:
        with open(filepath_name,'r') as infile:
            count=0
            for line in infile:
                data_item = json.loads(line, object_pairs_hook=OrderedDict) 
                post_argu_flag = []
                post_argu_label = []
                all_data_anno = []
                for post in data_item['posts'][1:]:
                    if post.has_key('majority_type'):
                        all_data_anno.append(post['majority_type'])
                    else:
                        all_data_anno.append('')
                    anno_argu = False
                    label=''
                    
                    for annotation in post['annotations']:
                        if 'agree' in annotation['main_type']:
                            anno_argu = True
                            label = annotation['main_type']
                            
                    post_argu_label.append(label)
                    post_argu_flag.append(anno_argu)

                data_anno.write('%s\n'%all_data_anno)
                if False in post_argu_flag:
                    pass
                else:
                    count+=1
                    outfile.write('%s'%line)

            print count
                    
def ID_extr():
    """ Extract raw post ID from raw data file
        
    """
    filename='coarse_discourse_dataset.json'
    filepath_name = os.path.join(file_dir, 'data','coarse_discourse',filename)
    with open(file_dir+'\\data\\coarse_discourse\\'+'raw_postID.txt','w+') as raw_ID_out:
        with open(filepath_name,'r') as infile:
            for line in infile:
                data_item = json.loads(line, object_pairs_hook=OrderedDict) 
                raw_id = data_item['posts'][0]['id'].encode('utf-8')
                #id = raw_id.split('_', 1)[-1]
                raw_ID_out.write('%s\n' %raw_id)
    print 'Done'
            

    
def ID_match():
    filetype = 'RS_'
    #ext = '.zip'
    ext = '.bz2'
    subm_index = open(file_dir+'\\data\\'+'subm_index.txt','a+')
    temp = subm_index.readlines()
    if temp ==[]:
        index = 0
    else:
        index = int(temp[-1])
        
    for year in range(2001,2001):
        for month in range(1,2):
            
            #file_object = read_file(filetype+'V2_', year, month, ext)
            file_object = read_file(filetype, year, month, ext)
            prefix = filetype+str(year)+'-'+str(month).zfill(2)

            try: 
                infile_subr_id = np.genfromtxt(file_dir+'\\data\\'+'subreddits_id.txt', dtype='S10')
                
                outfile_subm_title_text = open(file_dir+'\\data\\RS_title_text\\'+prefix+'_index-title-text.txt','a+')
               
                subr_id_len = len(infile_subr_id)
                ids = dict(zip(infile_subr_id,range(subr_id_len)))
                
                count=0
                for line in file_object:
                    
                    line = line.decode('utf-8').replace('\0', '')
                    data_item = json.loads(line)
                    
                 
                        
                    title = data_item['title']
                    if title:
                        title =' '.join(data_item['title'].split())
                    text = data_item['selftext']
                    
                    if text:
                        text =' '.join(data_item['title'].split())
             
                    outfile_subm_title_text.write((u'%i\t%s\t%s\n' %(index, title, text )).encode('utf-8'))
                     
                    count+=1
                    index+=1
                   
              
            finally:
                              
                file_object.close()
                
                outfile_subm_title_text.close()
       
                print prefix+' done: ' + str(count) +' RS recodes have been processed !'
    
    subm_index.write(str(index))
    subm_index.close()
            
            
def test():
    pass


    
if __name__ == '__main__':
    #argument_extr()
    #ID_match()
    ID_extr()
