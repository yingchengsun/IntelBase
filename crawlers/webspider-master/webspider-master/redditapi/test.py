'''
Created on Dec 7, 2017

@author: yingc
'''
import os
import datetime
writepath = 'some/path/to/file.txt'
sub='fuck'
today = datetime.date.today().strftime("%Y%m%d")
f= open('api_json/sub_{}_{}.json'.format(sub, today), 'w')
f.write('Hello, world!\n')