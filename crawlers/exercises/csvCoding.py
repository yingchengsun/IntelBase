'''
Created on Dec 4, 2017

@author: yingc
'''

import csv
import unicodecsv
import json
a = {u'name': u'FC Bayern M\xfcnchen', u'age': 24}
aa= [[u'name', u'FC Bayern M\xfcnchen'], [u'age', 24]]

aaa = {'has_media': True, 'is_reply': False}

b = {u'name': u'John Doe', u'age': 24}
b = {u'name': u'John Doe', u'age': 24}
'''
for key, value in a.items():

    if type(a[key]) == unicode:
        #value = unicode(value, "utf-8")
        a[key] = a[key].encode("utf-8")

    print a[key], type(a[key])
'''

'''
with open('mycsvfile.csv', 'wb') as f:  # Just use 'w' mode in 3.x
    f.write(u'\ufeff'.encode('utf8'))
    #w = csv.writer(f)
    w = csv.DictWriter(f, a.keys())
    #w = csv.DictWriter(f, b.keys())
    #w = csv.DictWriter(f, a.keys())
    w.writeheader()
    w.writerow(a)
 
'''
from collections import OrderedDict
#dictinfo= json.loads(a,object_pairs_hook=OrderedDict)
a={u'a':4,u'b':2,u'c':3}
#aa = OrderedDict(sorted(a.items()))
aa = OrderedDict(a)
print aa

with open('results.csv','wb') as f:
    w = unicodecsv.writer(f,encoding='utf-8-sig')
    #w = csv.DictWriter(f, a.keys())
    #w.writeheader()
    #w.writerows(aa)
    w.writerow(aa.keys())
    w.writerow(aa.values())
