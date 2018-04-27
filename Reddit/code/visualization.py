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
from textblob import TextBlob


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

def comment_network_visual_dynamic():
    """Plot comment network graph by the id and pid pairs
        
    """
    t = time() 
    filename = 'comment_network.txt'
    filepath_name = os.path.join(file_dir, filename)
    
    ndtype = 'S10, S10' 
    names = 'parent_id, id'
    ps = np.genfromtxt(filepath_name, dtype=ndtype, names=names, delimiter='\t')

    edges = zip(ps['parent_id'], ps['id'])
    print edges
    d=[]
    
    for item in edges:
        d.append(item)
        g = nx.Graph(d)
        
        #pos = nx.shell_layout(g)
    #nx.draw(g)
        nx.draw_networkx(g)
        
        plt.pause(0.5)
        plt.clf()
    #plt.show()

    print "comment network visualization total run time:"
    print time()-t
    
    
    

def comment_network_visual_category():
    """CATEGORY
        
    """
    t = time() 
    subpath = 'comment_network'
    filename = 'submission_all_info.txt'
    filepath_name = os.path.join(file_dir,subpath, filename)
    infile_subm = open(filepath_name,'r+')
    subm_all = infile_subm.readlines()
    
    subm = subm_all[0].split('\t')
    subm_id = subm[0]
    subm_title = subm[1]
    subm_text = subm[2]
    subm_index = subm[3]
    subm_score = subm[4]
    subm_time = subm[5]
    subm_gilded = subm[6]
    subm_num_comments = subm[7]
    subreddit_index = subm[8]
    subreddit_id = subm[9]
    
    subm_filename = subm_id+'.txt'
    filepath_name = os.path.join(file_dir, subpath, subm_filename)
    
    ndtype = 'S10,S10,i,i,i,i,S20,S1000' 
    names = 'cid, pid, time, controversiality, score, gilded, author, body'
     
    k=200
    
    ps = np.genfromtxt(filepath_name, dtype=ndtype, names=names, delimiter='\t',comments='{[#%]}')[1:k]

    controversiality = map(int, ps['controversiality'])+[0]
    created_utc = map(int, ps['time'])+[int(subm_time)]
    score =  map(int, ps['score'])+[10]
    gilded = map(int, ps['gilded'])
    author = ps['author']
    body = np.append(ps['body'], subm_title)

    edges = zip(ps['pid'], ps['cid'])
    g = nx.Graph(edges)
    nodes = np.append(ps['cid'], subm_id)
    nodes=nodes.tolist()
    
    polarity = [TextBlob(item.decode('utf-8')).polarity for item in body]
    subjectivity = [TextBlob(item.decode('utf-8')).subjectivity for item in body]

    created_utc_diff = [item-int(subm_time) for item in created_utc]
    created_utc_degrade = [item/60+1 for item in created_utc_diff]
    
    text = body

    wordcloud = WordCloud(width=1600, height=800).generate(" ".join(text))

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.tight_layout(pad=0)
    plt.axis("off")
    plt.show()
        
    plt.savefig(file_dir+'\\graphs\\'+prefix_time()+'_subreddit_title_wordcloud'+'.png', facecolor='k', bbox_inches='tight')
    '''
    degree = g.degree()
    size = [50*(degree[n]+1.0) for n in nodes]
    pos=nx.spring_layout(g)
    degree_ordered =  [degree[n] for n in nodes]
    plt.plot(score,label="score")  
    plt.plot(polarity,label="polarity") 
    plt.plot(subjectivity,label="subjectivity") 
    plt.plot(degree_ordered,label="degree") 
    plt.savefig(file_dir+'\\graphs\\'+prefix_time()+'_comment_network_visual_category'+'.png')
    plt.legend(fontsize=16)

    plt.show()
    
    
    nx.draw_networkx(g)
    plt.savefig(file_dir+'\\graphs\\'+prefix_time()+'_comment_network_visual_category'+'.png')
    plt.title('submission-comment network')
    plt.show()
    
    plt.clf()
    nx.draw(g,nodelist=nodes, with_labels=False, pos=pos, node_size=size, arrows=True, title='Scaling by connections')
    plt.savefig(file_dir+'\\graphs\\'+prefix_time()+'_comment_network_visual_category'+'.png')
    plt.title('Scaling by connections')
    plt.show()
    
    plt.clf()
    colors = controversiality
    nx.draw(g,nodelist=nodes, node_color=[i for i in colors], with_labels=False,  cmap=plt.cm.Reds, pos=pos, node_size=size, arrows=True)
    plt.savefig(file_dir+'\\graphs\\'+prefix_time()+'_comment_network_visual_category'+'.png')
    plt.title('Colored by controversiality')
    plt.show()
    
    plt.clf()
    colors = score
    nx.draw(g,nodelist=nodes, node_color=[i for i in colors], with_labels=False,  cmap=plt.cm.Reds, pos=pos, node_size=size, arrows=True)
    plt.savefig(file_dir+'\\graphs\\'+prefix_time()+'_comment_network_visual_category'+'.png')
    plt.title('Colored by score')
    plt.show()
    

    plt.clf()
    colors = polarity
    nx.draw(g,nodelist=nodes, node_color=[i for i in colors], with_labels=False,  cmap=plt.cm.Reds, pos=pos, node_size=size, arrows=True)
    plt.savefig(file_dir+'\\graphs\\'+prefix_time()+'_comment_network_visual_category'+'.png')
    plt.title('colored by polarity')
    plt.show()
    
    plt.clf()
    colors = subjectivity
    nx.draw(g,nodelist=nodes, node_color=[i for i in colors], with_labels=False,  cmap=plt.cm.Reds, pos=pos, node_size=size, arrows=True)
    plt.savefig(file_dir+'\\graphs\\'+prefix_time()+'_comment_network_visual_category'+'.png')
    plt.title('colored by subjectivity')
    plt.show()
    
    
    plt.clf()
    colors = created_utc_degrade
    nx.draw(g,nodelist=nodes, node_color=[-i for i in colors], with_labels=False,  cmap=plt.cm.Reds, pos=pos, node_size=size, arrows=True)
    plt.savefig(file_dir+'\\graphs\\'+prefix_time()+'_comment_network_visual_category'+'.png')
    plt.title('Evloving by time')
    plt.show()
    '''

    print "comment network visualization category total run time:"
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

def num_comments_plot():
    filename = 'k_num_comments.txt'
    sub_dir = 'num_comments'
    filepath_name = os.path.join(file_dir, sub_dir, filename)
    ndtype = 'i, i'
    names = 'num_comment, quantity'
    s = np.genfromtxt(filepath_name, dtype=ndtype, names=names)
    #print np.array([s['count']]).T
    x = range(len(s['num_comment']))
    print 'mean: '+str(s['num_comment'].mean())
    
    plt.plot(x,s['quantity']) 
    #plt.xticks(x,s['month'])
    #plt.xticks(x,s['month'],rotation=17 )
    
    plt.savefig(file_dir+'\\graphs\\'+prefix_time()+'_num_comments'+'.png')
    plt.show()    
    plt.close("all")
    print 'num_comments_plot done!'

def num_comments_pie():
    filename = 'k_num_comments.txt'
    sub_dir = 'num_comments'
    filepath_name = os.path.join(file_dir, sub_dir, filename)
    ndtype = 'i, i'
    names = 'num_comment, quantity'
    s = np.genfromtxt(filepath_name, dtype=ndtype, names=names)
    
    #print np.array([s['count']]).T
    x = s['quantity'][1:-1]
    s_length = len(x)
    labels1=['']*s_length
    explode1=[0]*s_length
    labels1[0]=1
    labels1[1]=2
    labels1[2]=3
    #explode1[0]=0.08
    #explode1[1]=0.05
    plt.axes(aspect=1)
    plt.pie(x,autopct='%.0f%%',shadow=True,explode=explode1,labels=labels1, textprops = {'fontsize':14, 'color':'k'})
    plt.pie
    #plt.xticks(x,s['month'])
    #plt.xticks(x,s['month'],rotation=17 )
    
    plt.savefig(file_dir+'\\graphs\\'+prefix_time()+'_num_comments_pie'+'.png')
    plt.show()    
    
    data=s['num_comment']

    #plt.boxplot(data,sym='o',whis=1.5,labels=labes)
    plt.boxplot(data)
    plt.savefig(file_dir+'\\graphs\\'+prefix_time()+'_num_comments_box'+'.png')
    plt.show()
    plt.close("all")

    print 'num_comments_pie done!'
    
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
    #comment_network_visual_dynamic()
    #num_comments_pie()
    comment_network_visual_category()
    #num_comments_plot()
    print 'All done!'
        
