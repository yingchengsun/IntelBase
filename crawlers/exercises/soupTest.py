import os
import urllib

import re
import threading
import urllib2
from bs4 import BeautifulSoup  
import json

with open('tieba.txt','r') as tieba:
    soup = BeautifulSoup(tieba,'html')
#fuck = soup.find_all(class_ = "search_main_wrap", limit = 3,recursive = False)
'''
import ast
fuck="{'a': 'ffffff', 'b': 2}"
print type(fuck)
result = ast.literal_eval("{'a': 'ffffff', 'b': 2}")
print result['a']
'''
i=1
for f in soup.find_all(class_ = "l_post l_post_bright j_l_post clearfix "):
    print f
    '''
    ddd =  json.loads(f['data-field'])['content']['content']
    soupp= BeautifulSoup(ddd,"html.parser")
    
    if soupp.img == None:
        continue
    else:
        dddd = soupp.img['src']
        print dddd
        urllib.urlretrieve(dddd, './pic'+ "/"+str(i)+'.jpg')
        i=i+1
        '''
