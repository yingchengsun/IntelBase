from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import networkx as nx
start_url = 'https://en.wikipedia.org/wiki/IPhone_6'
domain = 'https://en.wikipedia.org'

''' get soup '''
def get_soup(url):
    # get contents from url
    content = requests.get(url).content
    # get soup
    return BeautifulSoup(content,'lxml') # choose lxml parser


''' return a list of links to other wiki articles '''
def extract_articles(url=start_url):
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


''' main section '''
if __name__ == '__main__':
    # list of scraped items
    items = []
    title, ext_titles, ext_links = extract_articles(url=start_url)
    items.extend(zip([title]*len(ext_titles), ext_titles))
    for ext_link in ext_links:
        print('Items : {}'.format(len(items)))
        title, ext_titles, ext_links = extract_articles(domain + ext_link)
        items.extend(zip([title]*len(ext_titles), ext_titles))
        if len(items) > 10:
            break
    # write to file
 
    edges=items
    g=nx.Graph()
    g.add_edges_from(edges)

    d = nx.degree(g)
    dd={}
    for e in d:
        dd[e[0]]=e[1]

    d=dd
    values = [x/10.0 for x in d.values()]
    print values
    
    #nx.draw(g, node_size=[v * 200 for v in d.values()], cmap=plt.get_cmap('OrRd'), with_labels=True, node_color='r')
    nx.draw(g, node_size=[v for v in d.values()], with_labels=True, node_color='r')
    plt.savefig('E:/workspace/IntelBase/static/images/wiki_concept_links.png')
    plt.show()
    with open('wiki-result.csv','w') as f:
        for item in items:
            f.write(item[0].encode('utf-8') + ',' + item[1].encode('utf-8') + '\n')