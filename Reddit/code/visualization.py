'''
Created on Apr 9, 2018

@author: yingc
'''
import networkx as nx
import matplotlib.pyplot as plt
import os
import numpy as np
from time import time 
from datetime import datetime
from wordcloud import WordCloud



file_dir = 'E:\\Reddit\\data'

def prefix_time():
    prefix_time = datetime.now().strftime('%Y%m%d%H%M%S')
    return prefix_time

def subreddit_subscribers_bar():
    """ Top K subreddits with most subscribers
        Plot bar chart
    """
    k=100
    sub_dir = 'subreddits_original'
    filename = 'subreddits_index-displayname-subscribers-time.txt'
    filepath_name = os.path.join(file_dir, sub_dir,filename)
    ndtype = 'i,S10,i,i'
    names = 'index, name, subscribers, time'
    s = np.genfromtxt(filepath_name, dtype=ndtype, names=names, delimiter='\t')
    
    #sort the number of subscribers in reverse order and pick up the top K
    s_arg = np.argsort(-s['subscribers'])
    s =  s[s_arg][0:k]
    #we want to plot the bar chart in vertical way, so sort again in order from smallest to largest
    s = s[np.argsort(s['subscribers'])]
    
    s1 =  np.array([s['name']]).T
    s2 =  np.array([s['subscribers']]).T

    x=range(k)
    
    plt.barh(x, s2,color='r')
    plt.yticks(x,s1)
    plt.show()
    
    plt.savefig(file_dir+'\\graphs\\'+prefix_time()+'_subreddit_subscribers_bar'+'.png')
    
    print 'subreddit subscribers bar graph done!'

def subredsubreddit_subscribers_distribution():
    """compute the statistical results of subredsubreddit subscribers 
        
    """
    sub_dir = 'subreddits_original'
    filename = 'subreddits_index-displayname-subscribers-time.txt'
    filepath_name = os.path.join(file_dir, sub_dir,filename)
    ndtype = 'i,S10,i,i'
    names = 'index, name, subscribers, time'
    s = np.genfromtxt(filepath_name, dtype=ndtype, names=names, delimiter='\t')
    
    s_quantity = len(s['subscribers'])
    s_mean = s['subscribers'].mean()  
    s_max = s['subscribers'].max()
    s_min = s['subscribers'].min() 

    print s_quantity, s_max, s_min, s_mean
    
    print 'subreddits subscribers distribution done!'


def subreddit_title_wordcloud():
    """Plot the wordcloud graph of all word in subreddit title 
        
    """
    filename = 'subreddits_index-title-publicDescription.txt'
    sub_dir = 'subreddits_original'
    filepath_name = os.path.join(file_dir, sub_dir, filename)
    ndtype = 'i, S20, S100' 
    names = 'count, title, description'
    try:
        s = np.genfromtxt(filepath_name, dtype=ndtype, names=names, delimiter='\t',comments='{[#%]}')
        #print np.array([s['count']]).T
        text = s['title']

        wordcloud = WordCloud(width=1600, height=800).generate(" ".join(text))

        # Display the generated image:
        # the matplotlib way:
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.tight_layout(pad=0)
        plt.axis("off")
        plt.show()
        
        plt.savefig(file_dir+'\\graphs\\'+prefix_time()+'_subreddit_title_wordcloud'+'.png', facecolor='k', bbox_inches='tight')

    finally:
        print 'subreddit title wordcloud done!'

def RC_monthly_count():
    """Plot the count of comments by months
        
    """
    filename = 'monthlyCount.txt'
    sub_dir = 'RC'
    filepath_name = os.path.join(file_dir, sub_dir, filename)
    ndtype = 'S10, i'
    names = 'month, count'
    s = np.genfromtxt(filepath_name, dtype=ndtype, names=names)
    #print np.array([s['count']]).T
    x = range(len(s['month']))
    
    plt.plot(x,s['count']) 
    #plt.xticks(x,s['month'])
    #plt.xticks(x,s['month'],rotation=17 )
    
    plt.savefig(file_dir+'\\graphs\\'+prefix_time()+'_subreddit_subscribers_bar'+'.png')
    plt.show()    
    plt.close("all")
    print 'RC monthly count done!'
    


def comment_network_visual():
    """Plot comment network graph by the id and pid pairs
        
    """
    t = time() 
    filename = 'comment_network.txt'
    filepath_name = os.path.join(file_dir, filename)
    
    ndtype = 'S10, S10' 
    names = 'parent_id, id'
    ps = np.genfromtxt(filepath_name, dtype=ndtype, names=names, delimiter='\t')

    edges = zip(ps['parent_id'], ps['id'])
    g = nx.Graph(edges)
    #nx.draw(g)
    nx.draw_networkx(g)
    plt.show()

    print "comment network visualization total run time:"
    print time()-t

  
def comment_network_visual_indexing_version():
    """Use the property of set to eliminate the repetition and give all ids an index, 
        and use the new indexes to plot comment network graph
        
    """
   
    filename = 'comment_network.txt'
    filepath_name = os.path.join(file_dir, filename)

    ndtype = 'S10, S10' 
    names = 'parent_id, id'
    ps = np.genfromtxt(filepath_name, dtype=ndtype, names=names, delimiter='\t')
    ids = ps['id']
    pids =ps['parent_id']
    
    ids_pids = np.append(ids,pids)
    
    #Use the property of set to eliminate the repetition i ids_pids
    id_set = set(ids_pids)

    #convert list to dict
    id_dict = dict(zip(id_set,range(len(id_set))))
    
    #replace elements in a list using dictionary lookup    
    ids_rep = [id_dict[x] if x in id_dict else x for x in ids]
    pids_rep = [id_dict[x] if x in id_dict else x for x in pids]

    edges = zip(ids_rep,pids_rep)
    
    new_filename = 'comment_network_visual_indexing_version.txt'
    new_filepath_name = os.path.join(file_dir, new_filename)
    np.savetxt(new_filepath_name, edges,fmt='%i',delimiter='\t')   # x,y,z equal sized 1D arrays

    t = time()
    g = nx.Graph(edges)
    #nx.draw(g)
    nx.draw_networkx(g)
    plt.show()
    
    print "comment network visualization indexing version total run time:"
    print time()-t
    
def RC_body():
    filename = 'RC_2008-01_body.txt'
    sub_dir = 'RC'
    filepath_name = os.path.join(file_dir, sub_dir, filename)
    ndtype = 'i, S100' 
    names = 'count, body'
    try:
        s = np.genfromtxt(filepath_name, dtype=ndtype, names=names, delimiter='\t',comments='{[#%]}')
        print np.array([s['count']]).T
    finally:
        print 'stop'
   
    print 'RC_body done!'
    
    

if __name__ == '__main__':
    
    #subreddit_subscribers_bar()
    #subredsubreddit_subscribers_distribution()
    #subreddit_title_wordcloud()
    #RC_monthly_count()
    #comment_network_visual()
    #comment_network_visual_indexing_version()
    RC_body()
    print 'All done!'
        
