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

from gensim.test.utils import common_corpus, common_dictionary
from gensim.models import HdpModel


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
                    
def Post_ID_extr():
    """ Extract raw post ID from raw data file
        
    """
    filename='coarse_discourse_dataset.json'
    filepath_name = os.path.join(file_dir, 'data','coarse_discourse',filename)
    #with open(file_dir+'\\data\\coarse_discourse\\'+'raw_postID.txt','w+') as raw_ID_out:
    with open(file_dir+'\\data\\coarse_discourse\\'+'postID.txt','w+') as ID_out:
        with open(filepath_name,'r') as infile:
            for line in infile:
                data_item = json.loads(line, object_pairs_hook=OrderedDict) 
                raw_id = data_item['posts'][0]['id'].encode('utf-8')
                id = raw_id.split('_', 1)[-1]
                #raw_ID_out.write('%s\n' %raw_id)
                ID_out.write('%s\n' %id)
    print 'Done'
            

    
def Post_ID_match():
    """ Extract raw RS data with the same ID in raw_postID list
        
    """
    
    filetype = 'RS_v2_'
    ext = '.zip'
    #ext = '.bz2'

    for year in range(2006,2011):
        for month in range(1,13):
            
            #file_object = read_file(filetype+'V2_', year, month, ext)
            file_object = read_file(filetype, year, month, ext)
            prefix = filetype+str(year)+'-'+str(month).zfill(2)
            
            print 'Processing: '+prefix
            
            try: 
                infile_raw_postID = np.genfromtxt(file_dir+'\\data\\coarse_discourse\\'+'postID.txt', dtype='S10')
                outfile_raw_post = open(file_dir+'\\data\\coarse_discourse\\'+'outfile_raw_post.txt','a+')
                
                count=0
              
                for line in file_object:
                    line = line.decode('utf-8').replace('\0', '')
                    data_item = json.loads(line)
                    
                    id = data_item['id']
                    
                    if id in infile_raw_postID:
                        print id
                        outfile_raw_post.write((u'%s' %line).encode('utf-8'))
                    count+=1
                    
            finally:
                              
                file_object.close()
                outfile_raw_post.close()
                print prefix+' done: ' + str(count) +' RS recodes have been processed !'


def Comment_ID_match():
    """ Extract raw RC data with the same post ID in raw_postID list
        
    """
    
    filetype = 'RC_'
    #ext = '.zip'
    ext = '.bz2'

    for year in range(2006,2018):
        for month in range(1,13):
            
            #file_object = read_file(filetype+'V2_', year, month, ext)
            file_object = read_file(filetype, year, month, ext)
            prefix = filetype+str(year)+'-'+str(month).zfill(2)
            
            print 'Processing: '+prefix
            
            try: 
                infile_raw_postID = np.genfromtxt(file_dir+'\\data\\coarse_discourse\\'+'postID.txt', dtype='S10')
                outfile_raw_comment = open(file_dir+'\\data\\coarse_discourse\\'+'outfile_raw_comment.txt','a+')
                outfile_commentID_found = open(file_dir+'\\data\\coarse_discourse\\'+'outfile_commentID_found.txt','a+')
                count=0
              
                for line in file_object:
                    line = line.decode('utf-8').replace('\0', '')
                    data_item = json.loads(line)
                    
                    id = (data_item['link_id'].split('_', 1)[-1]).encode('utf-8')
                    
                    if id in infile_raw_postID:
                        print id
                        outfile_commentID_found.write((u'%s' %line).encode('utf-8'))
                        count+=1
                    
            finally:
                              
                file_object.close()
                outfile_raw_comment.close()
                outfile_commentID_found.close()
                print prefix+' done: ' + str(count) +' RC recodes have been processed !'
                
            
def test():
    hdp = HdpModel(common_corpus, common_dictionary)
    unseen_document = [(1, 3.), (2, 4)]
    doc_hdp = hdp[unseen_document]
    topic_info = hdp.print_topics(num_topics=20, num_words=10)
    print unseen_document
    print topic_info


def Add_raw_post_to_PCA():
    """
        PCA: Post-Comments-Annotation
        
    """
    folder = 'raw_PCA'
    path = os.path.join(file_dir, 'data','coarse_discourse',folder)
   
    infile_raw_post = open(file_dir+'\\data\\coarse_discourse\\'+'outfile_raw_post.txt','r')
    count = 0
    for line in infile_raw_post:
        data_item = json.loads(line.decode('utf-8').replace('\0', '')) 
        filename = path+"\\"+data_item['id']+'.txt'
        if os.path.isfile(filename):
            print filename
        else:
            file = open(filename,'w+')
            file.write(line)
            file.close()
        count+=1
    print count

def Add_raw_Comments_to_PCA():
    """
        PCA: Post-Comments-Annotation
        
    """
    folder = 'raw_PCA'
    path = os.path.join(file_dir, 'data','coarse_discourse',folder)
    infile_raw_comment = open(file_dir+'\\data\\coarse_discourse\\'+'outfile_raw_comment.txt','r')
    out_dict_file =  open(file_dir+'\\data\\coarse_discourse\\'+'post_dict.json','w')
    
    comment_count = 0
    total_count = 0
    post_dict={}
    for line in infile_raw_comment:
        data_item = json.loads(line.decode('utf-8').replace('\0', ''))
        id = (data_item['link_id'].split('_', 1)[-1]).encode('utf-8')
        filename = path+"\\"+id+'.txt'
        if os.path.isfile(filename):
            file = open(filename,'a+')
            file.write(line)
            file.close()
            if not post_dict.has_key(id):
                post_dict[id] = 1
            else:
                post_dict[id]+=1
        else:
            print filename
        
        total_count+=1
    
    out_dict_file.write(json.dumps(post_dict))
    out_dict_file.close()
    print len(post_dict)
    print "Total Comments: " + str(total_count)


def Add_raw_Annotation_to_PCA():
    """
        PCA: Post-Comments-Annotation
        
    """
    folder = 'raw_PCA'
    path = os.path.join(file_dir, 'data','coarse_discourse',folder)
   
    anno_filename='coarse_discourse_dataset.json'
    anno_filepath_name = os.path.join(file_dir, 'data','coarse_discourse',anno_filename)
    
    count = 0
    with open(anno_filepath_name,'r') as infile:
        for line in infile:
            data_item = json.loads(line, object_pairs_hook=OrderedDict) 
            raw_id = data_item['posts'][0]['id'].encode('utf-8')
            id = raw_id.split('_', 1)[-1]
            filename = path+"\\"+id+'.txt'
            
            if os.path.isfile(filename):
                file = open(filename,'a+')
                file.write(line)
                file.close()
            else:
                print filename
        
            count+=1
    print count
    
    
def Read_PCA():
    """
        PCA: Post-Comments-Annotation
        
    """
    folder = 'raw_PCA'
    path = os.path.join(file_dir, 'data','coarse_discourse',folder)
    
    files= os.listdir(path) 
    s = []
    for file in files: 
        if not os.path.isdir(file):
            f = open(path+"/"+file); 
            iter_f = iter(f); 
            str = ""
            for line in iter_f:
                print line
                #str = str + line
            #s.append(str)
    print(s) 
    
def Stat():
    """
        PCA: Post-Comments-Annotation
        
    """
    
    infile_post_dict =  open(file_dir+'\\data\\coarse_discourse\\'+'post_dict.json','r')
    post_dict = json.load(infile_post_dict)
    #print post_dict
    comment_count = post_dict.values()
    
    comment_count_dict = {}
    for key in comment_count:
        comment_count_dict[key] = comment_count_dict.get(key, 0) + 1
   
    sorted_dict= OrderedDict(sorted(comment_count_dict.items(),key = lambda t:-t[0]))
    sorted_dict2= OrderedDict(sorted(post_dict.items(),key = lambda t:-t[1]))
    for key,value in sorted_dict2.items():
        print key,value


if __name__ == '__main__':
    #argument_extr()
    #Post_ID_extr()
    #Post_ID_match()
    #Comment_ID_match()
    #test()
    #Add_raw_post_to_PCA()
    #Add_raw_Comments_to_PCA()
    #Add_raw_Annotation_to_PCA()
    Stat()
    #Read_PCA()
