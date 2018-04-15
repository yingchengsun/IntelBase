'''
Created on Nov 18, 2017

@author: yingc
'''

from bs4 import BeautifulSoup as BSHTML
import urllib
page = urllib.urlopen('http://www.youtube.com/')
soup = BSHTML(page)
images = soup.findAll('img')
i=10
for image in images:
    #print image source
    print image
    #urllib.urlretrieve(image['data-thumb'], './pic'+ "/"+str(i)+'.gif')
    #print alternate text
    
    i=i+1

'''
html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""
from bs4 import BeautifulSoup
import re
soup = BeautifulSoup(html)
#print soup.find_all(href = re.compile('elsie'))
print soup.select('.story')
'''