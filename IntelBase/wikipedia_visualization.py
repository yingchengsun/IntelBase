'''
Created on Dec 14, 2017

@author: yingc
'''
from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import networkx as nx

domain = 'https://en.wikipedia.org'

''' get soup '''
def get_soup(url):
    # get contents from url
    content = requests.get(url).content
    # get soup
    return BeautifulSoup(content,'lxml') # choose lxml parser


''' return a list of links to other wiki articles '''
def extract_articles(url):
    # get soup
    soup = get_soup(url)
    # find all the paragraph tags
    p_tags = soup.findAll('p')
    # gather all <a> tags 
    a_tags = []
    for p_tag in p_tags:
        a_tags.extend(p_tag.findAll('a'))
    # filter the list : remove invalid links
    a_tags = [ a_tag for a_tag in a_tags if 'title' in a_tag.attrs and 'href' in a_tag.attrs ]
    # get all the article titles
    titles = [ a_tag.get('title') for a_tag in a_tags ] 
    # get all the article links
    links  = [ a_tag.get('href')  for a_tag in a_tags ] 
    # get own title
    self_title = soup.find('h1', {'class' : 'firstHeading'}).text
    return self_title, titles, links

def concept_connections(starturl, query):
    items = []
    title, ext_titles, ext_links = extract_articles(url=start_url)
    items.extend(zip([title]*len(ext_titles), ext_titles))
    for ext_link in ext_links:
        print('Items : {}'.format(len(items)))
        title, ext_titles, ext_links = extract_articles(domain + ext_link)
        items.extend(zip([title]*len(ext_titles), ext_titles))
        if len(items) > 30:
            break
    # write to file
    
    with open('wiki_concept_links_'+query+'.csv','w') as f:
        for item in items:
            f.write(item[0].encode('utf-8') + ',' + item[1].encode('utf-8') + '\n')
    
    edges=items
    g=nx.Graph()
    g.add_edges_from(edges)
    degree_list = nx.degree(g)
    
    degree_dict={}
    print degree_list
    for d in degree_list:
        degree_dict[d[0]]=d[1]
    
    #nx.draw(g, node_size=[v * 200 for v in d.values()], cmap=plt.get_cmap('OrRd'), with_labels=True, node_color='r')
    nx.draw(g, node_size=[v*10  for v in degree_dict.values()], with_labels=True, node_color='r')
    plt.savefig('E:/workspace/IntelBase/static/images/wiki_concept_links_'+query+'.png')
    plt.show()
''' main section '''
if __name__ == '__main__':
    # list of scraped items
    start_url = 'https://en.wikipedia.org/wiki/IPhone_8'
    query='IPhone 8'
    concept_connections(start_url, query)
    
    