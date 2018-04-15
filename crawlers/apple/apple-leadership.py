'''
Created on Nov 23, 2017

@author: yingc
'''
from selenium import webdriver
import urllib

import time

import matplotlib.pyplot as plt
import networkx as nx

chrome_options  = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(executable_path='D:/geckodriver/chromedriver.exe', chrome_options=chrome_options)

driver.get("https://www.apple.com/leadership/")

figures = driver.find_elements_by_css_selector("li.profile-list-item figure" )
names  = driver.find_element_by_css_selector("li.profile-list-item h3")
links  = driver.find_elements_by_css_selector("li.profile-list-item a")


for link in links:
    print link.get_attribute('href')
edges = []
CEO='Tim Cook'
for figure in figures:
    pic =  figure.value_of_css_property("background-image").lstrip('url("').rstrip('")')
    name = figure.find_element_by_css_selector("h3").text
    title = figure.find_element_by_css_selector("h4").text
    edges.append((CEO,name))
    print title
    urllib.urlretrieve(pic,'pictures/'+'%s.jpg' % name)
print edges
#time.sleep(2)
driver.quit()

g=nx.Graph()
g.add_edges_from(edges)
print g.edges()

d = nx.degree(g)
print d
dd={}
for e in d:
    dd[e[0]]=e[1]
print dd
d=dd
values = [x/10.0 for x in d.values()]
print values

nx.draw(g, node_size=[v * 200 for v in d.values()],with_labels=True, node_color='crimson')
plt.savefig('E:/workspace/IntelBase/static/images/apple_leadership.png')
plt.show()
'''
link = driver.find_element_by_css_selector(".page-overview .image-ceo").value_of_css_property("background-image")
link= str(link.lstrip('url("').rstrip('")'))
print link
name  = driver.find_element_by_css_selector(".page-overview .image-ceo h3").text
print name
urllib.urlretrieve(link,'pictures/'+'%s.jpg' % name)
'''